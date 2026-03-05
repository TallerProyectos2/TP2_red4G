# TP2 Design Notes

## Functional Design

The design intentionally separates transport, inference, orchestration, and motion execution:

- LTE core and routing are isolated on the EPC and eNodeB.
- Inference is isolated on the Jetson.
- Motion decisions are centralized in the EPC backend.
- The car stays lightweight and reactive.

## Why The EPC Hosts The Application Stack

The EPC machine is the most capable host and already sits at the center of network routing. Hosting the backend, MQTT broker, and database there reduces cross-machine dependencies and keeps the Jetson focused on GPU-bound work.

## Why The Jetson Is Inference-Only

The Jetson is the best place for model execution, but it should avoid carrying the rest of the platform:

- less operational complexity
- simpler failure isolation
- easier GPU/runtime management

## Why HTTP For Frames

Frame upload should be explicit and bounded:

- better control over payload size
- easier retries
- easier logging
- cleaner separation from command traffic

## Why MQTT For Commands

MQTT fits low-latency, lightweight control messages:

- command dispatch
- acknowledgement
- car status
- light telemetry

## Data Ownership

- Filesystem on the EPC:
  - frame images
  - validation artifacts
- PostgreSQL:
  - structured metadata and events

