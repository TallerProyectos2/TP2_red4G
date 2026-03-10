# TP2 Machine Inventory

## Purpose

This file records the role, addressing, and access path for each machine in the TP2 lab.

Do not store passwords here.

## PC EPC

- Role:
  - LTE core host
  - main application host
- Hostname:
  - `tp2-EPC`
- Services:
  - `srsepc`
  - NAT / IP forwarding
  - optional `dnsmasq`
  - backend API
  - `Mosquitto`
  - `PostgreSQL`
- Known addresses:
  - upstream (`eno1`): `10.0.128.174/24` (DHCP)
  - backhaul: `10.10.10.1`
  - Tailscale: `100.97.19.112`
  - SGi: `172.16.0.1`
- Interface bindings:
  - backhaul (`enp1s0`): static `10.10.10.1/24`
  - SGi (`srs_spgw_sgi`): static `172.16.0.1/24`
- Access path:
  - primary remote entrypoint
  - SSH to the EPC first

## PC eNodeB

- Role:
  - LTE radio access
- Hostname:
  - `tp2-ENB`
- Services:
  - `srsenb`
  - `bladeRF`
- Known addresses:
  - backhaul: `10.10.10.2`
  - Tailscale: `100.69.186.34`
- Access path:
  - primary operator path: Tailscale SSH to `tp2@100.97.19.112` on the EPC, then SSH from the EPC to `tp2@10.10.10.2`
  - `tp2@EPC -> tp2@eNodeB` key-based SSH hop was validated on `2026-03-04`

## Jetson

- Role:
  - inference-only node
- Services:
  - inference API
  - model runtime
- Addressing:
  - must be reachable from the EPC
  - keep its active IP documented in `docs/NETWORK.md` if it changes

## Coche

- Role:
  - mobile client
- Services:
  - camera capture
  - frame upload
  - MQTT command handling
  - movement adapter
- Connectivity:
  - attaches as an LTE UE
  - receives an address from the EPC
  - observed IMSI during attach attempts: `901650000052126`
  - UE pool on EPC: `172.16.0.0/24`
  - static UE assignment configured on EPC (`2026-03-10`): `901650000052126 -> 172.16.0.2`
  - latest observed UE IP in `srsepc` log (`2026-03-10`): `172.16.0.2`

## Ownership Rules

- EPC owns orchestration.
- eNodeB owns radio only.
- Jetson owns inference only.
- Coche owns frame capture and motion execution only.
