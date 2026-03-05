# Jetson Inference Service

## Purpose

The Jetson hosts the traffic-sign inference runtime and exposes it as an HTTP service to the EPC backend.

## Scope

Allowed on the Jetson:

- model loading
- preprocessing
- inference
- confidence scoring
- latency reporting

Not allowed on the Jetson by default:

- main backend orchestration
- MQTT broker
- primary database
- frame archive

## Suggested API

- `GET /health`
  - returns service health and model readiness

- `POST /infer`
  - accepts a frame payload or file reference
  - returns:
    - predicted label
    - confidence
    - latency

## Operational Requirements

- Load the model once at startup.
- Keep the service minimal and deterministic.
- Log startup, model load, and inference errors clearly.
- Expose a stable port reachable from the EPC.

## Validation

- One health call
- One known-image inference call
- Measured latency recorded in validation notes

