# TP2 Reliability Model

## Reliability Goals

- LTE can be brought up repeatably.
- The application stack can start without disturbing LTE routing.
- The Jetson can answer inference requests predictably.
- The car falls back safely when command flow breaks.

## Primary Failure Domains

- EPC and eNodeB configuration drift
- `bladeRF` startup instability
- Docker networking interfering with EPC routing
- Jetson model or runtime failure
- MQTT path failure
- Car-agent watchdog disabled or misconfigured

## Fallback Rules

- If the Jetson fails:
  - degrade to `SLOW` or `STOP`

- If MQTT fails:
  - the car watchdog must stop movement

- If the backend is unavailable:
  - do not keep executing stale commands indefinitely

## Operational Logging

Capture evidence for:

- service start and stop
- connectivity checks
- inference latency
- published commands
- watchdog-triggered fallbacks

## Troubleshooting Strategy

Fix one layer at a time:

1. LTE transport
2. UE routing
3. EPC application services
4. Jetson inference
5. MQTT control path
6. Car execution path

