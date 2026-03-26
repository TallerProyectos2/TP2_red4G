# TP2 Machine Inventory

## Purpose

Record current machine roles, addressing, and access paths for the live lab.

Do not store passwords here.

## PC EPC

- Role:
  - LTE core host
  - main script runtime host
- Hostname:
  - `tp2-EPC`
- Services:
  - `srsepc`
  - NAT / IP forwarding
  - optional `dnsmasq`
  - control scripts from `servicios/`
  - local inference endpoint from `servicios/`
- Known addresses:
  - upstream (`eno1`): `10.0.128.174/24` (DHCP)
  - backhaul (`enp1s0`): `10.10.10.1/24`
  - Tailscale: `100.97.19.112`
  - SGi (`srs_spgw_sgi`): `172.16.0.1/24`
- Script runtime references:
  - repository path: `servicios/`
  - deployed path used in recent validations: `/home/tp2/TP2_red4G/servicios/`
- Access path:
  - primary remote entrypoint
  - SSH to EPC first

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
  - operator path: Tailscale SSH to `tp2@100.97.19.112` on EPC, then SSH from EPC to `tp2@10.10.10.2`
  - `tp2@EPC -> tp2@eNodeB` key-based SSH hop validated (`2026-03-04`)

## Jetson

- Role:
  - inference-only node (pending integration)
- Hostname:
  - `tp2-jetson`
- SSH user:
  - `grupo4`
- Target use:
  - offload inference from EPC when required
  - keep control path anchored on EPC
- Runbook:
  - `docs/JETSON.md`
- Addressing:
  - management LAN IP: `192.168.72.127`
  - Tailscale IP: `100.115.99.8`
  - must be reachable from EPC
- Access path:
  - primary SSH: `ssh grupo4@tp2-jetson`
  - Tailscale direct SSH: `ssh grupo4@100.115.99.8`
  - management LAN SSH: `ssh grupo4@192.168.72.127`

## Coche

- Role:
  - mobile client
- Services:
  - sends sensor payloads to EPC control scripts
  - executes steering/throttle commands from EPC
- Connectivity:
  - attaches as LTE UE
  - receives address from EPC UE pool `172.16.0.0/24`
  - observed IMSI: `901650000052126`
  - static UE assignment on EPC: `901650000052126 -> 172.16.0.2`
- Control transport:
  - UDP payload stream to EPC control scripts
  - UDP control packets returned by EPC

## Ownership Rules

- EPC owns orchestration and control runtime.
- eNodeB owns radio only.
- Jetson owns inference only when integrated.
- Car owns capture/sensor emission and command execution only.
