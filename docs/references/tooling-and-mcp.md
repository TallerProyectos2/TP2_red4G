# Tooling And MCP Reference

## Primary Tooling

- `atlassian` MCP
- `ssh`
- `docker`
- `docker compose`
- `python3`
- `curl`
- `mosquitto_pub`
- `mosquitto_sub`
- `psql`

## MCP Servers

## `atlassian`

- Use for:
  - reading Jira projects and issues
  - adding comments
  - updating issue state
- Prefer it whenever a task maps to a Jira issue.
- Validate the live technical state before changing Jira.
- If it is unavailable:
  - record the intended Jira update in local notes
  - do not invent state transitions

## `chrome-devtools`

- Use for:
  - future dashboard validation
  - local UI checks if a web interface is added
- Not required for the current backend-only phases

## `github`

- Use only if repository or PR workflows become part of the operational flow.
- Not required for machine bring-up itself.

## CLI Usage Matrix

## `ssh`

- Primary tool for live machine inspection and changes
- Prefer read-only commands first

## `docker` / `docker compose`

- Use for EPC application stack lifecycle
- Avoid changes that implicitly rewrite EPC routing assumptions

## `python3`

- Use for backend, Jetson, and car-agent development or one-off checks

## `curl`

- Use for HTTP endpoint validation

## `mosquitto_pub` / `mosquitto_sub`

- Use for MQTT smoke tests

## `psql`

- Use for PostgreSQL connectivity and schema validation

