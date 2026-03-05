# TP2 Codex Operating Contract

## Mission

This repository operates a four-machine connected-vehicle lab:

- `PC EPC`: LTE core plus the main application host
- `PC eNodeB`: LTE radio access with `bladeRF`
- `Jetson`: inference-only node
- `Coche`: camera, telemetry, and motion-control client

Future Codex sessions must treat this repository as the control plane for that real lab, not as an isolated code sandbox.

## Mandatory Read Order

Before any non-trivial change, read these files in order:

1. `PLAN.md`
2. `ARCHITECTURE.md`
3. `RUNBOOK.md`
4. `MACHINES.md`
5. The relevant service or machine runbook under `docs/`

## Source Of Truth

- `PLAN.md`: canonical technical phase plan
- `ARCHITECTURE.md`: system boundaries and data flow
- `RUNBOOK.md`: startup, shutdown, and operating sequence
- `MACHINES.md`: machine ownership, addressing, and access path
- `docs/JIRA-WORKFLOW.md`: Jira/MCP execution loop

Do not silently diverge from these documents. If the real system changes, update the docs in the same task.

## Architecture Contract

- The car sends frames to the EPC backend by HTTP.
- The EPC backend calls the Jetson for inference.
- The EPC backend decides the final action and publishes it by MQTT.
- The car receives commands by MQTT and maps them to the movement scripts.
- The eNodeB remains radio-only.
- The Jetson remains inference-only.
- The EPC does not become the inference host.
- MQTT is not used to transport images.

## Default Delivery Loop

For any non-trivial task:

1. Identify the highest-priority unblocked task in `PLAN.md` and the matching Jira issue.
2. Inspect the current state first:
   - local repo state
   - relevant remote machine state
   - current Jira issue status
3. Implement the change end-to-end for the affected machine or service.
4. Validate with the correct runtime checks.
5. Update docs if the operating model changed.
6. Add evidence to the appropriate log file if the change is material.
7. Update Jira only after validation confirms the technical state.

Do not mark work complete based on intent alone.

## Jira MCP Rules

- Use the `atlassian` MCP server for Jira operations.
- Project key: `TP2`
- Operational Jira scope is restricted to the five implementation parent tasks and their direct subtasks:
  - `TP2-137` `Implementación CORE (Ordenador 1)`
  - `TP2-138` `Implementación EnodeB (Ordenador 2)`
  - `TP2-139` `Implementación Coche`
  - `TP2-140` `Implementación Jetson`
  - `TP2-165` `Implementación Integración`
- Canonical Jira filter for this repository:
  - `project = TP2 AND (issuekey in (TP2-137, TP2-138, TP2-139, TP2-140, TP2-165) OR parent in (TP2-137, TP2-138, TP2-139, TP2-140, TP2-165))`
- For Jira reads, comments, edits, and transitions, operate only inside that filter unless the user explicitly expands scope.
- When a task says "check Jira" or "continue with the next task", start from the canonical filter above, not from the full project backlog.
- Check the relevant Jira issue before starting non-trivial work.
- Add a progress comment when:
  - a real milestone was completed,
  - validation was run,
  - a blocker was found.
- Transition an issue only when its acceptance criteria are actually met.

## Remote Machine Rules

- Prefer read-only checks first.
- Use the established SSH path to the EPC first, then hop to the eNodeB if needed.
- Do not store passwords, tokens, or secrets in repository files.
- Do not restart already-working services unless the task requires it.
- Never update firmware on any component under any circumstance.
- For any risky remote action, stop and ask if the blast radius is unclear.

## Validation Minimums

- LTE work:
  - config check
  - process check
  - port check
  - reachability check
- Backend work:
  - HTTP health check
  - DB connectivity check
  - storage path check
- Jetson work:
  - inference health check
  - known-image inference check
- Car-agent work:
  - command reception
  - movement adapter path
  - watchdog fallback

End-to-end changes should include the full path:

- frame upload
- inference request
- action decision
- MQTT publish
- command execution

## Non-Negotiables

- Never commit secrets.
- Never update firmware on the `bladeRF`, modem, Jetson, car, or any other component.
- Never write SSH passwords into docs, scripts, or comments.
- Never treat Jira as the source of truth over the live system.
- Never move the eNodeB into hosting application services.
- Never push image traffic through MQTT.

## Stop Conditions

Stop and escalate when:

- credentials are missing,
- the remote machine state is ambiguous,
- a destructive action is required,
- validation cannot be completed,
- Jira and the live technical state disagree and the difference is unclear.
