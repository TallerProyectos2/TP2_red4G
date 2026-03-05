# TP2 Operating Runbook

## Purpose

This runbook defines the standard operating sequence for bringing the lab up, validating it, and shutting it down cleanly.

## Startup Order

1. Validate network connectivity between EPC and eNodeB.
2. Start `srsepc` on the EPC.
3. Start `srsenb` on the eNodeB.
4. Verify S1 setup is established.
5. Start the application stack on the EPC:
   - backend
   - MQTT
   - PostgreSQL
6. Start the inference service on the Jetson.
7. Verify the Jetson health endpoint.
8. Start the car agent.
9. Verify the car can attach to LTE and reach the EPC backend.

## Shutdown Order

1. Stop the car agent.
2. Stop the application stack on the EPC.
3. Stop the Jetson inference service.
4. Stop `srsenb`.
5. Stop `srsepc`.
6. Capture logs or validation artifacts if the session changed system state.

## Default Validation Sequence

## LTE Validation

- Confirm EPC and eNodeB configs are aligned.
- Confirm `srsenb` reaches `srsepc`.
- Confirm S1 setup completes.
- Confirm the UE can attach.

## EPC Application Validation

- Check backend health endpoint.
- Check MQTT publish/subscribe.
- Check PostgreSQL connectivity.
- Check frame storage path exists and is writable.

## Jetson Validation

- Check `GET /health`.
- Run one known-image inference request.
- Record latency.

## Car Validation

- Confirm HTTP frame upload succeeds.
- Confirm MQTT command reception.
- Confirm the movement adapter runs.
- Confirm the watchdog fallback is active.

## End-To-End Validation

- Upload frame
- Trigger inference
- Publish action
- Receive command
- Execute movement
- Record acknowledgement

## Operational Rules

- Prefer read-only inspection first.
- Avoid restarting healthy services unless needed for the task.
- Do not change more than one layer at once during troubleshooting.
- If LTE is unstable, do not continue to backend or car-level debugging.
- Firmware updates are forbidden on all components during this project.

## Troubleshooting Order

When the system fails, debug in this order:

1. EPC and eNodeB process state
2. Backhaul network reachability
3. UE attachment and routing
4. EPC backend health
5. Jetson inference health
6. MQTT flow
7. Car-agent execution path

## Escalation Conditions

Stop and escalate if:

- remote credentials are missing,
- a change risks breaking working LTE connectivity,
- a task appears to require a firmware update,
- service restarts are required but current state is not understood,
- Jira state suggests work is done but runtime validation fails.
