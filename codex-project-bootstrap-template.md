# Codex Project Bootstrap: TP2 Connected Vehicle Lab

Use this as the initial bootstrap prompt for future Codex workspaces that need to operate this specific TP2 project. This is no longer a generic template; it is the project-specific bootstrap contract for the current four-machine lab.

It is written as a copy-paste prompt for another Codex workspace, but it is grounded in the real system design, machine roles, and Jira workflow already established for this project.

---

## Copy-Paste Input

You are bootstrapping a Codex-first repository for the TP2 connected-vehicle lab. Your task is to create or update the repository contracts, operational docs, MCP wiring, and execution workflow so future Codex sessions can safely operate the real four-machine system and keep Jira in sync with technical progress.

### Objective

Set up this repository so future Codex sessions can:

- understand the real machine topology and service ownership,
- follow the agreed deployment sequence from network bring-up to end-to-end validation,
- use Jira MCP to review, update, and close project work in the `TP2` Jira project,
- avoid leaking credentials or breaking lab connectivity,
- keep planning, validation, and operational runbooks current.

### Real Project Context

- Project name: `Taller de Proyectos II (TP2) - Vehiculo conectado`
- Product summary:
  - Build a working 4G-connected vehicle demonstrator using a custom LTE lab network.
  - The car sends camera frames over the LTE network to backend services.
  - A Jetson runs the traffic-sign inference model, and the backend returns movement commands to the car.
- Deployment model:
  - On-prem lab deployment
  - Four physical machines
  - EPC is the main application host
  - Jetson is the inference accelerator
- High-risk domains:
  - LTE core and SDR networking
  - Remote machine administration over SSH
  - Safety of remote motion commands
  - Secret handling for SSH and external services
  - Cross-machine orchestration and recovery

### System Topology

This project consists of four machines with strict role separation:

1. `PC EPC`

- Runs `srsepc`
- Owns LTE core responsibilities: `MME + HSS + SPGW`
- Owns NAT, IP forwarding, and UE-side DNS if needed
- Hosts the main application services:
  - backend API
  - MQTT broker
  - database
  - frame storage

2. `PC eNodeB`

- Runs `srsenb`
- Owns the `bladeRF`
- Provides LTE radio access only
- Does not host backend, DB, MQTT, or IA

3. `Jetson`

- Runs the inference service only
- Loads the traffic-sign model at startup
- Exposes an HTTP inference API to the EPC backend
- Should remain minimal and focused on inference

4. `Coche`

- Runs a lightweight Python control agent
- Captures frames from the camera
- Sends frames to the EPC backend by HTTP
- Receives commands from MQTT
- Adapts the commands to the existing movement scripts
- Must include a watchdog-safe fallback behavior

### Network Contract

Use this topology as the default source of truth unless the operator explicitly changes it:

- EPC <-> eNodeB backhaul:
  - network: `10.10.10.0/24`
  - EPC: `10.10.10.1`
  - eNodeB: `10.10.10.2`

- EPC SGi side:
  - interface IP: `172.16.0.1`
  - UE addresses come from `172.16.0.0/24`

- Jetson:
  - must be reachable from the EPC over the lab LAN or upstream network
  - do not assume the car talks directly to the Jetson

### Service Contract Per Machine

Treat these allocations as mandatory unless the operator explicitly approves a redesign.

#### PC EPC

- Host services:
  - `srsepc`
  - IP forwarding
  - NAT (`iptables` or `nftables`)
  - `dnsmasq` if UE DNS is needed
- Application services:
  - `FastAPI` backend
  - `Mosquitto`
  - `PostgreSQL`
  - local frame storage under `/srv/tp2/`

#### PC eNodeB

- `srsenb`
- `bladeRF`
- No application stack

#### Jetson

- `FastAPI` or equivalent inference service
- `PyTorch`
- `OpenCV`
- `TensorRT` only if later optimization is required
- Prefer `venv + systemd` over Docker unless CUDA packaging is already stable

#### Coche

- Python capture process
- HTTP client for frame upload
- MQTT client for command reception and acknowledgements
- Adapter to the existing movement scripts
- Safety watchdog

### Architecture Rules

These are non-negotiable operating rules:

- The car sends frames to the EPC backend, not to the Jetson directly.
- The EPC calls the Jetson for inference and decides the final action.
- Images travel over HTTP, not MQTT.
- MQTT is reserved for commands, acknowledgements, status, and light telemetry.
- The eNodeB remains radio-only.
- The EPC never becomes the inference host.
- Never write SSH passwords, tokens, or secrets into repository files.

### Current Technical Plan Baseline

Use the repository `PLAN.md` as the technical source of truth for the deployment sequence. The current intended order is:

1. Stabilize LTE (`srsepc` + `srsenb`)
2. Validate UE connectivity and routing
3. Bring up backend services on the EPC
4. Bring up inference on the Jetson
5. Connect EPC backend to Jetson inference
6. Implement and validate command publication
7. Implement and validate the car agent
8. Run end-to-end validation
9. Add hardening, fallbacks, and demo runbook

Future Codex sessions must preserve this phase order unless the operator explicitly changes the architecture.

### Jira MCP Requirements

Jira is part of the operational loop for this project.

- Jira site: `https://tp2-2026.atlassian.net`
- Jira project key: `TP2`
- Required MCP server: `atlassian`
- Future Codex sessions must:
  - check Jira before starting non-trivial work,
  - identify the relevant issue(s),
  - align technical work with the current Jira state,
  - add comments with progress and validation notes when meaningful,
  - transition issues only when the technical state actually matches the Jira state.

Use these issues as the likely anchors for the current machine-based work, but always re-check their live status first:

- `TP2-75`: project planning
- `TP2-16`: 4G infrastructure
- `TP2-17`: IA / signal detection
- `TP2-137`: CORE implementation (PC EPC)
- `TP2-138`: eNodeB implementation (PC eNodeB)
- `TP2-139`: car implementation
- `TP2-140`: Jetson implementation

When working through a concrete technical milestone:

- read the relevant Jira issue first,
- confirm the issue is still open or in progress,
- make the technical change,
- validate the change,
- add a Jira comment summarizing:
  - what changed,
  - what was validated,
  - any remaining blockers,
- only mark the issue complete if the acceptance condition is truly met.

### SSH / Remote Access Rules

This project uses real remote machines. Future Codex sessions must treat that as a first-class constraint.

- Use existing SSH access and the operator's existing connection path.
- Prefer the already-established SSH route to the EPC, then hop to the eNodeB if needed.
- Do not persist credentials in docs, scripts, or config files.
- Before making remote changes:
  - inspect the current state,
  - avoid restarting working services unnecessarily,
  - prefer read-only checks before modifications.
- If a remote step is destructive, stop and ask first.

### Required Deliverables

Create or update the following files and folders so they become the source of truth for future Codex work on this project:

1. Root governance

- `AGENTS.md`
- `ARCHITECTURE.md`
- `RUNBOOK.md`
- `MACHINES.md`

2. Core docs

- `PLAN.md` (keep as the canonical technical phase plan)
- `docs/DESIGN.md`
- `docs/NETWORK.md`
- `docs/INFERENCE.md`
- `docs/CAR-AGENT.md`
- `docs/SECURITY.md`
- `docs/RELIABILITY.md`
- `docs/JIRA-WORKFLOW.md`

3. Operational references

- `docs/references/tooling-and-mcp.md`
- `docs/references/ssh-and-remote-ops.md`
- `docs/references/test-and-validation.md`

4. Logging structure

- `docs/logs/index.md`
- `docs/logs/changelog/`
- `docs/logs/validations/`
- `docs/logs/incidents/`

### AGENTS.md Requirements

Author or update `AGENTS.md` so it enforces:

- the four-machine architecture as the baseline contract,
- mandatory read order before non-trivial changes:
  - `PLAN.md`
  - `ARCHITECTURE.md`
  - `RUNBOOK.md`
  - relevant machine or service runbook
- strict separation of responsibilities across EPC, eNodeB, Jetson, and car,
- a repeatable delivery loop:
  - identify the highest-priority unblocked task,
  - check the corresponding Jira issue,
  - inspect the current machine state,
  - implement the change,
  - validate with the appropriate runtime checks,
  - update docs,
  - update Jira,
  - stop only when blocked or when the milestone is fully complete,
- explicit stop conditions for:
  - missing credentials
  - risky remote changes
  - ambiguous machine state
  - incomplete validation

Make `AGENTS.md` operational, not generic.

### Planning Model Requirements

Use a planning model that matches the actual lab workflow:

- `PLAN.md` remains the technical phase source of truth.
- Major milestones must map back to Jira issues in `TP2`.
- Local technical phases and Jira state must not drift silently.
- Each meaningful milestone should document:
  - goal
  - machine(s) affected
  - validation criteria
  - rollback or safe fallback
  - linked Jira issue(s)

### Validation Requirements

Bake in a validation standard that matches this project:

- configuration verification before service restarts,
- process and port checks after each service change,
- network reachability checks between the correct machines,
- runtime endpoint checks for backend and inference APIs,
- MQTT publish/subscribe validation,
- database connectivity checks,
- end-to-end checks once integration begins,
- explicit evidence logged in `docs/logs/validations/`.

For this project:

- LTE changes require real service and connectivity checks.
- Backend changes require HTTP and database checks.
- Jetson changes require inference endpoint checks with known images.
- Car-agent changes require command reception and watchdog behavior checks.
- Jira updates should reflect validated state, not intended state.

### MCP and Tooling Setup Requirements

Define the project-specific tooling stack in `docs/references/tooling-and-mcp.md`.

Required MCP servers:

- `atlassian`
- `chrome-devtools` (for any local dashboard or web UI later)
- `github` only if repository or PR workflows become part of the execution path

Required CLIs:

- `ssh`
- `docker`
- `docker compose`
- `python3`
- `curl`
- `mosquitto_pub`
- `mosquitto_sub`
- `psql`

Recommended local skills:

- `skill-installer` (to install additional skills if needed)
- `skill-creator` only when formalizing reusable project skills

For each MCP/CLI, document:

- what it is used for,
- when to prefer it,
- auth or setup prerequisites,
- safe operating path,
- fallback behavior if it is unavailable.

### Codex Local Setup Tasks

After authoring or updating the docs, perform the local bootstrap where possible:

1. Inspect local Codex setup:

- list configured MCP servers
- verify `atlassian` MCP auth
- verify the Jira `TP2` project is reachable

2. Verify required CLIs:

- `ssh`
- `docker`
- `docker compose`
- `python3`
- `curl`

3. Verify remote operation prerequisites where possible:

- confirm SSH access path still works
- confirm the EPC can still be reached safely

4. Report:

- what is configured correctly,
- what is installed but still blocked,
- what needs operator credentials,
- what remote machine assumptions remain unverified.

### Safety Rules

- Never commit secrets.
- Never write SSH passwords, API tokens, or private endpoints that are not already intentionally documented.
- Prefer read-only checks first.
- For remote restarts, destructive actions, or service-impacting changes, stop and ask if the risk is not clearly acceptable.
- If a machine is already working, inspect before touching it.
- If Jira and the technical state disagree, do not blindly change Jira; verify first.

### Output Requirements

Execute the work; do not only describe it.

At the end:

- summarize created or updated files,
- summarize MCP servers verified or configured,
- summarize the Jira issues reviewed or touched,
- summarize any blocked items (auth, remote access, missing binaries, machine state),
- give the next concrete commands or checks the operator should run.

### Additional Project-Specific Constraints

Apply these constraints while bootstrapping:

- Machine boundaries:
  - EPC is the application hub
  - eNodeB is radio-only
  - Jetson is inference-only
  - car is agent-only
- Data handling:
  - store frame files on the EPC, not in the database by default
  - store metadata and events in PostgreSQL
- Deployment caveats:
  - protect working LTE connectivity while adding higher-level services
  - do not let Docker networking break EPC routing assumptions
- Naming rules:
  - use explicit machine-oriented names such as `epc-backend`, `jetson-inference`, `car-agent`

If a required detail is missing, make the most conservative assumption, document it, and continue without inventing secrets.

---

## Minimal Variant

Bootstrap this TP2 repository as a Codex-operated four-machine connected-vehicle lab. Preserve the existing `PLAN.md` as the technical source of truth, formalize the EPC/eNodeB/Jetson/car service boundaries, wire in Jira MCP for the `TP2` project, require safe SSH-based remote operations, and make future Codex sessions validate real machine state before updating docs or closing Jira work.
