# Car Agent Contract

## Purpose

The car agent is the mobile client that captures frames, sends them to the EPC backend, receives control commands, and maps those commands onto the existing movement scripts.

## Logical Components

- `camera-capture`
  - captures frames at a bounded rate

- `frame-uploader`
  - uploads frames to the EPC backend over HTTP

- `mqtt-client`
  - subscribes to command topics
  - publishes acknowledgements and status

- `movement-adapter`
  - translates abstract actions into calls to the existing Python movement scripts

- `safety-watchdog`
  - stops or slows the vehicle when commands become stale

## Behavioral Rules

- The car does not perform final action selection.
- The car executes commands coming from the EPC backend.
- The watchdog must be active during all remote-control or autonomous tests.

## Validation

- Receive a manual MQTT command
- Execute a known movement action
- Upload at least one frame successfully
- Confirm watchdog fallback triggers when command flow stops

