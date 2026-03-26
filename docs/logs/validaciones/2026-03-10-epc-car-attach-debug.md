# Depuracion de attach del coche en EPC

- Fecha: `2026-03-10`
- Maquina: `tp2-EPC` (con comprobaciones de salto a `tp2-ENB`)

## Objetivo

Identificar la IP LTE actual de la UE del coche y diagnosticar el fallo de attach.

## Evidencia de ejecucion

- EPC accesible por Tailscale y `srsepc` en ejecucion:
  - `srsepc` escuchando en `10.10.10.1:36412/SCTP`
  - `srsepc` escuchando en `10.10.10.1:2152/UDP`
- eNodeB accesible desde EPC:
  - asociacion S1 al EPC establecida desde `10.10.10.2` hasta `10.10.10.1:36412`
  - `bladeRF` detectado (`Nuand bladeRF 2.0 micro`)
  - dos instancias de `srsenb` encontradas ejecutandose al mismo tiempo (`pid 12340` y `pid 23086`)
- Los logs de attach del EPC (`/srv/tp2/logs/srsepc.log`) muestran:
  - `Attach request -- IMSI: 901650000052126`
  - `UL NAS: Authentication Failure` repetido
  - `Non-EPS authentication unacceptable`
- Estado de la interfaz UE del EPC:
  - `srs_spgw_sgi` presente con `172.16.0.1/24`
  - sin entradas vecinas de UE en `srs_spgw_sgi`
  - no se observo ninguna direccion UE asignada en los logs

## Resultado

- No se pudo obtener la IP del coche porque el attach de la UE no llega a completarse.
- El estado tecnico actual es: la senalizacion de radio llega al EPC, pero la autenticacion NAS falla antes de la sesion PDN/asignacion de IP.
- Riesgo adicional: procesos `srsenb` duplicados pueden causar comportamiento inestable y deberian reducirse a una unica instancia activa.
