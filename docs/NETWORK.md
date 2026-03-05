# TP2 Network Contract

## Backhaul

- Network: `10.10.10.0/24`
- EPC: `10.10.10.1`
- eNodeB: `10.10.10.2`

This is the dedicated link between `srsepc` and `srsenb`.

## EPC Interfaces

- Hostname:
  - `tp2-EPC`
- Backhaul side:
  - interface: `enp1s0`
  - `10.10.10.1`
- SGi side:
  - interface: `srs_spgw_sgi`
  - `172.16.0.1`
- External or upstream side:
  - interface: `eno1`
  - the interface used for NAT and any upstream reachability

## UE Addressing

- UE pool: `172.16.0.0/24`
- The car receives its IP dynamically from the EPC unless an explicit static assignment is added to the HSS.

## Service Reachability

- The car must reach the EPC backend over HTTP.
- The car must reach the EPC MQTT broker.
- The EPC must reach the Jetson inference API.
- The car should not call the Jetson directly.

## Core Ports

- `36412/SCTP`: S1-MME
- `2152/UDP`: GTP-U
- `53/TCP,UDP`: DNS if enabled
- `8000/TCP`: backend API
- `1883/TCP`: MQTT
- `5432/TCP`: PostgreSQL internal access
- `9000/TCP`: suggested Jetson inference API

## Validation Checklist

- EPC can ping eNodeB
- eNodeB can reach the EPC S1 endpoint
- UE receives an IP
- UE can reach `172.16.0.1`
- EPC can reach the Jetson service IP
- EPC Phase 0 baseline is documented in `docs/EPC.md`
