# EPC Machine Specification

## Scope

This document records the Phase 0 baseline for the EPC host and acts as the machine-specific source of truth for its fixed addressing, storage layout, and service contract.

## Phase 0 Baseline

- Validation date: `2026-03-04`
- Jira scope: `TP2-141` (`EPC-Fase 0. Base de red y estructura del nodo`)
- Hostname: `tp2-EPC`

## Network Bindings

- Upstream interface:
  - `eno1`
  - current address: `10.0.128.174/24` (DHCP)
- eNodeB backhaul:
  - interface: `enp1s0`
  - fixed address: `10.10.10.1/24`
  - NetworkManager profile: `Conexión cableada 2`
  - IPv4 mode: `manual`
- SGi side:
  - interface: `srs_spgw_sgi`
  - fixed address: `172.16.0.1/24`
  - NetworkManager profile: `srs_spgw_sgi`
  - IPv4 mode: `manual`
- Remote access:
  - `tailscale0`
  - address: `100.97.19.112/32`

## Service Port Contract

- `36412/SCTP`: `srsepc` S1-MME
- `2152/UDP`: `srsepc` GTP-U
- `53/TCP,UDP`: optional `dnsmasq`
- `8000/TCP`: `backend-api`
- `1883/TCP`: `mosquitto`
- `5432/TCP`: `postgres` (internal only)

These ports stay reserved for the EPC role even when the corresponding services are not started yet.

## Storage And Log Paths

- Base path: `/srv/tp2`
- Ownership: `tp2:tp2`
- Frame storage: `/srv/tp2/frames`
- Runtime and validation logs: `/srv/tp2/logs`
- Container manifests and overrides: `/srv/tp2/docker`
- Host-specific generated configs and service copies: `/srv/tp2/config`
- Current `srsRAN` config path on the machine: `/home/tp2/.config/srsran/epc.conf`
- Current `srsRAN` operational logs: `/srv/tp2/logs/srsepc.log` for the manual Phase 1 launch, or `journalctl -u srsepc` once the service is moved under `systemd`

## Version Baseline

- `srsRAN EPC`: build commit `6bcbd9e5b` captured from `srsepc --version` on `2026-03-04`

## Phase 1 LTE Core Baseline

- Validation date: `2026-03-04`
- Jira scope: `TP2-142` (`EPC-Fase 1. Core LTE operativo`)
- Active config file: `/home/tp2/.config/srsran/epc.conf`
- Runtime start command currently in use: `srsepc /home/tp2/.config/srsran/epc.conf`
- Current operational model:
  - `srsepc` is started manually on the EPC
  - automatic supervision remains deferred to Phase 9

## Phase 1 Config Contract

- `[mme]`
  - `mme_bind_addr = 10.10.10.1`
- `[hss]`
  - `db_file = /home/tp2/.config/srsran/user_db.csv`
- `[spgw]`
  - `gtpu_bind_addr = 10.10.10.1`
  - `sgi_if_addr = 172.16.0.1`
  - `sgi_if_name = srs_spgw_sgi`
- `[log]`
  - `filename = /srv/tp2/logs/srsepc.log`

## Phase 1 UE Provisioning Baseline

- Provisioning file: `/home/tp2/.config/srsran/user_db.csv`
- Confirmed provisioned entries:
  - `ue1`
  - `ue2`

The Phase 1 requirement is satisfied as long as at least one known-good UE remains in this file and the EPC keeps pointing to this absolute path.

## Phase 0 Validation

- `hostnamectl --static` reports `tp2-EPC`
- `nmcli` shows `enp1s0` pinned to `10.10.10.1/24` with `ipv4.method manual`
- `nmcli` shows `srs_spgw_sgi` pinned to `172.16.0.1/24` with `ipv4.method manual`
- `ping -c 2 -W 1 10.10.10.2` succeeds from the EPC with `0%` packet loss
- `/srv/tp2`, `/srv/tp2/frames`, `/srv/tp2/logs`, `/srv/tp2/docker`, and `/srv/tp2/config` exist on the EPC with owner `tp2:tp2`
- The `tp2` user can write to `/srv/tp2/frames` and `/srv/tp2/logs`

## Phase 1 Validation

- `srsepc` starts cleanly after the Phase 1 controlled restart
- `ss` confirms:
  - `10.10.10.1:36412/SCTP` is listening
  - `10.10.10.1:2152/UDP` is listening
- `lsof -p 30003` shows `/srv/tp2/logs/srsepc.log` open for write
- The last observed successful S1 establishment in the EPC logs includes:
  - `Received S1 Setup Request`
  - `Sending S1 Setup Response`
  - peer eNodeB name `srsenb01`
- No EPC-side reconfiguration is required before the next manual start because the HSS database path is now absolute in `epc.conf`

## Operational Note

Phase 0 for the EPC is complete when these bindings and paths remain stable. Future phases can add services on top of this baseline, but they should not move these addresses or relocate the `/srv/tp2` working tree unless there is an incident with a documented rollback.
