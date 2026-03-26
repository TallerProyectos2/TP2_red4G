# Asignacion de IP de la UE del coche

- Fecha: `2026-03-10`
- Maquina: `tp2-EPC`

## Objetivo

Confirmar la IP LTE asignada actualmente a la UE del coche y fijarla a una direccion estable en la configuracion HSS del EPC.

## Evidencia de ejecucion

- El log de `srsepc` muestra una sesion UE correcta para el IMSI `901650000052126` con:
  - `IMSI: 901650000052126, UE IP: 172.16.0.2`
- Base de datos HSS del EPC (`/home/tp2/.config/srsran/user_db.csv`) antes del cambio:
  - el IMSI `901650000052126` tenia `IP_alloc=dynamic`
- Base de datos HSS del EPC despues del cambio:
  - el IMSI `901650000052126` se fijo en `IP_alloc=172.16.0.2`
- Copia de seguridad creada antes de editar:
  - `/home/tp2/.config/srsran/user_db.csv.bak_static_ip_20260310_115235`

## Resultado

- La UE del coche queda ahora mapeada explicitamente a `172.16.0.2` en la base de datos de usuarios del EPC.
- No se forzo ningun reinicio de servicio durante esta comprobacion; el mapeo fijo queda persistido para ciclos de attach posteriores.
