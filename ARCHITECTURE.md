# TP2 System Architecture

## Overview

TP2 is a connected-vehicle demonstrator built around a private LTE lab network. The system is split across four machines, with a strict separation between radio, core networking, inference, and vehicle control.

The EPC is the central host for both LTE core services and the main application stack. The eNodeB exposes the radio network. The Jetson performs inference only. The car is the mobile endpoint that captures frames and executes movement commands.

## Machine Responsibilities

## PC EPC

- `srsepc` (`MME + HSS + SPGW`)
- UE IP allocation
- NAT and IP forwarding
- Optional UE DNS
- Main application services:
  - backend API
  - MQTT broker
  - PostgreSQL
  - frame storage

## PC eNodeB

- `srsenb`
- `bladeRF`
- Radio access only

## Jetson

- Inference API
- Model loading and execution
- No DB, no MQTT broker, no main backend

## Coche

- Camera capture
- Frame upload over HTTP
- MQTT command reception
- Movement adapter over the existing Python scripts
- Safety watchdog

## Network Topology

## EPC <-> eNodeB Backhaul

- Network: `10.10.10.0/24`
- EPC: `10.10.10.1`
- eNodeB: `10.10.10.2`

This link carries S1 control and user-plane traffic between `srsepc` and `srsenb`.

## UE Side

- SGi interface: `172.16.0.1`
- UE pool: `172.16.0.0/24`

The car attaches to LTE and receives a UE-side IP from the EPC.

## Jetson Reachability

The Jetson must be reachable from the EPC over the lab LAN or upstream network. The car should not talk to the Jetson directly.

## Data Flow

1. The car attaches to LTE and gets a UE IP.
2. The car uploads a frame to the EPC backend by HTTP.
3. The EPC backend stores the frame metadata and file path.
4. The EPC backend sends the frame to the Jetson inference API.
5. The Jetson returns the detected class, confidence, and latency.
6. The EPC backend decides the final action.
7. The EPC backend publishes the action by MQTT.
8. The car receives the command and invokes the movement adapter.
9. The car publishes status or acknowledgement.

## Protocol Contract

- HTTP:
  - frame upload
  - backend health
  - Jetson inference
- MQTT:
  - command publish
  - acknowledgement
  - status
  - light telemetry
- PostgreSQL:
  - events
  - sessions
  - detections
  - commands

## Storage Contract

- Frame files live on the EPC filesystem.
- Structured metadata lives in PostgreSQL.
- Avoid storing bulk frame blobs in the database.

## Ports

- `36412/SCTP`: S1-MME
- `2152/UDP`: GTP-U
- `53/TCP,UDP`: optional UE DNS
- `8000/TCP`: EPC backend API
- `1883/TCP`: MQTT broker
- `5432/TCP`: PostgreSQL (internal only)
- `9000/TCP`: suggested Jetson inference API

## Invariants

- eNodeB is radio-only.
- Jetson is inference-only.
- EPC is the orchestration hub.
- Images do not travel over MQTT.
- The final motion command is decided centrally at the EPC backend.

