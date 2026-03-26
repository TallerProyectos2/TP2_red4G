# Car Runtime Contract (Current)

## Purpose

Document the current car-side interaction model used by existing EPC scripts.

## Control Model

The active operational model is UDP stream + UDP control:

- Car sends payloads to EPC control server.
- EPC script processes payloads and returns control command.

No new backend API is required to run this path.

## Script Endpoints In Use

Control servers available in `servicios/`:

- `car1_cloud_control_server.py`
- `car1_cloud_control_server_real_time_control.py`
- `car1_manual_control_server.py`
- `prueba.py`
- `coche.py`
- `prueba_ps4.py`
- `car3_cloud_control_server.py`
- `car3_cloud_control_server_real_time_control.py`
- `car3_manual_control_server.py`

Shared control logic:

- `artemis_autonomous_car.py`

## UDP Packet Contract (As Implemented)

- Incoming payload discriminator (first byte):
  - `I`: camera image payload
  - `L`: lidar payload
  - `B`: battery level
  - `D`: reserved/other data path
- Payload body is deserialized with `pickle.loads(...)` in current scripts.
- Outgoing control packet type:
  - `C` + steering (`double`) + throttle (`double`)

## Runtime Modes

- Manual mode:
  - keyboard-driven steering/throttle
  - camera/LIDAR display for operator feedback
  - optional PS4 controller input on EPC when using `coche.py`
  - optional Roboflow inference overlay on live camera frames
- Autonomous mode:
  - image/LIDAR processed by `artemis_autonomous_car`
  - steering/throttle computed automatically
- Real-time autonomous mode:
  - keyboard switches route/behavior mode while autonomous loop runs

## LTE Binding Context

- Car attaches as UE in EPC network.
- Current static mapping:
  - IMSI `901650000052126` -> `172.16.0.2`

## Minimum Validation

1. Start LTE (`srsepc` + `srsenb`) and verify UE attach.
2. Start chosen EPC control script.
3. Confirm script receives UDP payloads from car.
4. Confirm control packets are returned and car responds.

## EPC Operator Notes

- Current car1 LTE-side manual bind is `172.16.0.1:20001`.
- `prueba.py` is the EPC-safe manual script for keyboard control.
- `coche.py` is the preferred car1 runtime when using keyboard/PS4 control plus Roboflow inference.
- `prueba_ps4.py` is now a compatibility wrapper that starts `coche.py`.
- PS4 input may require the EPC operator account to have access to `/dev/input/event*` (for example, membership in the `input` group).
- When the final Jetson path is enabled, the EPC still owns control and only offloads inference by setting `ROBOFLOW_LOCAL_API_URL=http://<JETSON_IP>:9001`.
