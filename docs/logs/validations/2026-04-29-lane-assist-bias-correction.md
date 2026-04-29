# 2026-04-29 - Lane assist bias correction hardening

## Scope

- Kept EPC as the only car control runtime.
- Hardened `servicios/lane_detector.py` for the live taped track where the right lane line can exit the camera frame.
- Preserved the steering convention: smaller steering values turn right, so lane corrections and `TP2_STEERING_TRIM=-0.08` compensate the physical left drift to the right.
- Prevented stale lane memory from refreshing itself indefinitely.
- Lane assist still does not apply during open turn actions.
- No firmware changes.

## Validation

- Local real-frame replay using EPC captures from `/srv/tp2/frames/autonomous/20260429-092908/images/`:
  - Before: `no-plausible-lane-width`.
  - After: `pair`, `confidence=0.84`, `correction=-0.05` on sampled frames.
- Local MacBook:
  - `PYTHONPATH=servicios python -m compileall -q servicios tests`
  - `PYTHONPATH=servicios python -m unittest discover -s tests`
  - Result: 39 tests OK.

## EPC note

At initial inspection `tp2-car-control.service` was inactive, while `tp2-srsepc.service` and `mosquitto.service` were active. Deployment validation must include starting/restarting the car runtime.
