# Validacion del salto SSH de EPC a eNodeB

- Fecha: `2026-03-04`
- Alcance: ruta de acceso del operador entre `tp2-EPC` y `tp2-ENB`

## Cambio aplicado

- Se genero una clave SSH `ed25519` para `tp2` en el EPC porque antes no existia ninguna clave privada
- Se instalo esa clave publica en la cuenta `tp2` del eNodeB

## Validacion

- El acceso SSH por Tailscale al EPC funciona con `ssh tp2@100.97.19.112`
- El acceso SSH directo por backhaul desde el EPC funciona con `ssh tp2@10.10.10.2`
- El hostname del eNodeB reportado a traves del salto validado es `tp2-ENB`

## Resultado operativo

Las sesiones futuras pueden alcanzar el eNodeB a traves del EPC con la ruta estandar de operador en dos pasos y no deberian necesitar volver a introducir una contrasena para el salto de `tp2` a `tp2`.
