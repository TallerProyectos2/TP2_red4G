# Script de control manual con PS4 en EPC

- Fecha: `2026-03-17`
- Maquina: `tp2-EPC`

## Objetivo

Anadir un script de control manual de car1 que preserve el flujo actual de teclado y que tambien acepte un mando PS4 en el EPC.

## Evidencia de ejecucion

- Nuevo script anadido al repo:
  - `servicios/prueba_ps4.py`
- Script desplegado en la ruta actual de runtime del EPC:
  - `/home/tp2/TP2_red4G/servicios/prueba_ps4.py`
- Validacion local de sintaxis:
  - `python3 -m py_compile servicios/prueba_ps4.py`
- Validacion de sintaxis en EPC:
  - `python3 -m py_compile /home/tp2/TP2_red4G/servicios/prueba_ps4.py`
- Imports de runtime en EPC validados dentro del entorno Conda `tp2`:
  - `evdev`
  - `cv2`
  - `numpy`
  - `pynput`
- Validacion de arranque:
  - `DISPLAY=:1 timeout 6s conda run -n tp2 python -u /home/tp2/TP2_red4G/servicios/prueba_ps4.py`
  - `ss -lunp` mostro el listener:
    - `172.16.0.1:20001`

## Notas operativas

- El script autodetecta dispositivos tipo PS4 a partir de nombres `evdev` de Linux (`Wireless Controller`, `DualShock`, `Sony`, `PS4`).
- La entrada por teclado sigue disponible al mismo tiempo.
- Mapeo de control PS4:
  - stick izquierdo: direccion
  - `R2`: avance
  - `L2`: marcha atras
  - `R1` / `L1`: boost de avance/reversa
  - `X`: neutro de emergencia
- Durante esta tarea se observo al usuario `tp2` del EPC sin el grupo `input`, por lo que el acceso a eventos PS4 puede requerir un cambio unico por operador:
  - `sudo usermod -aG input tp2`
  - despues iniciar una nueva sesion/login antes de volver a ejecutar el script
- No se requieren cambios de configuracion en el lado del coche mas alla de la ruta manual/cloud existente.

## Resultado

- `prueba_ps4.py` esta listo en el EPC y mantiene el bind actual del control manual de car1 en `172.16.0.1:20001`.
- El control por teclado funciona mediante el flujo actual de operador en EPC.
- El soporte PS4 esta implementado y deberia funcionar una vez que el mando este conectado al EPC y la cuenta del operador pueda leer `/dev/input/event*`.
