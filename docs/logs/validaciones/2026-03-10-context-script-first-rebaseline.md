# Reajuste de contexto al modelo script-first

- Fecha: `2026-03-10`
- Alcance: actualizacion del contexto y la planificacion del repositorio

## Disparador

El contexto operativo cambio:

- el modelo/servicio de inferencia esta disponible en EPC,
- los scripts existentes en `servicios/` son la linea base operativa,
- EPC + eNodeB + coche se consideran configurados,
- la integracion con Jetson es el principal bloque de implementacion pendiente.

## Evidencia revisada

- Log de validacion existente de Codex:
  - `docs/logs/validations/2026-03-05-epc-inferencia-local.md`
- Ultimo commit del paquete de scripts:
  - `61a9b85` (`scripts IA`) con `servicios/*.py`
- Contexto LTE/UE actual:
  - `docs/logs/validations/2026-03-10-car-ue-ip-assignment.md`

## Cambios aplicados en el repo

- Reorganizacion del plan global:
  - `PLAN.md`
- Actualizacion del contexto central de referencia:
  - `ARCHITECTURE.md`
  - `RUNBOOK.md`
  - `MACHINES.md`
- Actualizacion de documentacion de maquina/red/runtime:
  - `docs/EPC.md`
  - `docs/NETWORK.md`
  - `docs/INFERENCE.md`
  - `docs/CAR-AGENT.md`
  - `docs/DESIGN.md`
  - `docs/RELIABILITY.md`

## Resultado

El contexto del repositorio ahora refleja el modelo operativo real:

- runtime script-first en EPC,
- ninguna nueva API backend obligatoria en la ruta critica actual,
- Jetson queda registrado como la siguiente etapa de integracion sin romper la linea base validada EPC+eNodeB+coche.
