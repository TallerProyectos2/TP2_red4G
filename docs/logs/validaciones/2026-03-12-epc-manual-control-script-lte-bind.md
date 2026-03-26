# Bind LTE del script de control manual en EPC

- Fecha: `2026-03-12`
- Maquina: `tp2-EPC`

## Objetivo

Anadir una variante del script de control manual que enlace la direccion LTE del EPC `172.16.0.1` sin modificar los scripts legacy originales.

## Evidencia de ejecucion

- La interfaz del lado UE del EPC se confirmo durante esta tarea:
  - `srs_spgw_sgi` presente con `172.16.0.1/24`
- Nuevo script anadido al repo:
  - `servicios/car1_manual_control_server_epc_lte.py`
- Nuevo script desplegado en la ruta de runtime del EPC:
  - `/home/tp2/servicios_tp2/car1_manual_control_server_epc_lte.py`
- Validacion de sintaxis completada:
  - local: `python3 -m py_compile servicios/car1_manual_control_server_epc_lte.py`
  - EPC: `python3 -m py_compile /home/tp2/servicios_tp2/car1_manual_control_server_epc_lte.py`
- Comprobacion de ocupacion de puertos en EPC antes de ejecutar:
  - no se encontro ningun listener activo en `20001/UDP` ni `20003/UDP` en el momento de la validacion

## Resultado

- Ya hay disponible un script de control manual dedicado a LTE/EPC con bind por defecto `172.16.0.1:20001`.
- Los scripts originales permanecen intactos por seguridad de rollback.
- En esta tarea no se ejecuto ninguna prueba de movimiento real del coche, por lo que el movimiento extremo a extremo sigue pendiente de una ejecucion por operador.
