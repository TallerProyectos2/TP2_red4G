# Integracion de control del coche en EPC e inferencia en Jetson

## Fecha

- `2026-03-17`

## Alcance

- unificar el control manual de car1 en un nuevo script de runtime del EPC
- mantener la propiedad del control en el EPC
- conectar la inferencia Roboflow en vivo mediante el mismo contrato de configuracion usado por las herramientas de inferencia existentes
- preparar la ruta final en la que la inferencia se descarga a Jetson sin mover la orquestacion fuera del EPC

## Cambios en el repo

- anadido `servicios/coche.py`
  - control manual de car1 en `172.16.0.1:20001`
  - entrada por teclado + PS4
  - overlay de inferencia Roboflow en vivo sobre los frames entrantes de camara
- anadido `servicios/roboflow_runtime.py`
  - helpers compartidos de configuracion/cliente de inferencia reutilizados por el control en vivo y las herramientas offline
- cambiado `servicios/prueba_ps4.py`
  - ahora actua como wrapper de compatibilidad hacia `coche.py`
- cambiado `servicios/inferencia.py`
  - ahora reutiliza los helpers compartidos de runtime Roboflow
- cambiado `servicios/inferencia_gui_web.py`
  - ahora reutiliza los helpers compartidos de runtime Roboflow
- cambiado `servicios/environment-tp2.yml`
  - declara `gradio` e `inference-sdk` en la definicion del entorno `tp2`

## Validacion en EPC

- sintaxis local:
  - `python3 -m py_compile servicios/coche.py servicios/prueba_ps4.py servicios/roboflow_runtime.py servicios/inferencia.py servicios/inferencia_gui_web.py`
  - resultado: OK
- scripts actualizados desplegados en EPC:
  - `/home/tp2/TP2_red4G/servicios/`
- validado el entorno conda `tp2` en EPC con `PYTHONNOUSERSITE=1`
  - import de `gradio`: OK
  - import de `InferenceHTTPClient` desde `inference_sdk`: OK
  - `requests`, `aiohttp`, `supervision`: OK
- sintaxis remota en EPC:
  - `PYTHONNOUSERSITE=1 /home/tp2/miniforge3/envs/tp2/bin/python -m py_compile coche.py prueba_ps4.py roboflow_runtime.py inferencia.py inferencia_gui_web.py`
  - resultado: `EPC_PYCOMPILE_OK`
- comprobacion de bind en runtime sobre EPC:
  - se lanzo `coche.py` con `DISPLAY=:1`
  - endpoint de inferencia configurado para la ruta Jetson:
    - `TP2_INFERENCE_MODE=local`
    - `TP2_INFERENCE_TARGET=model`
    - `ROBOFLOW_LOCAL_API_URL=http://192.168.72.127:9001`
  - salida de arranque observada:
    - `Manual control server listening on 172.16.0.1:20001`
    - `Inference: enabled (local/model) endpoint=http://192.168.72.127:9001`
    - controlador PS4 detectado en la pila de entrada del EPC
  - `ss -lunp` confirmo:
    - `172.16.0.1:20001` en escucha con el nuevo script

## Validacion en Jetson

- comprobado desde EPC:
  - `curl http://192.168.72.127:9001/openapi.json`
  - resultado: timeout
- comprobado desde EPC por Tailscale hacia Jetson:
  - `curl http://100.115.99.8:9001/openapi.json`
  - resultado: connection refused
- comprobado directamente en Jetson:
  - `curl http://127.0.0.1:9001/openapi.json`
  - resultado: connection refused
  - `systemctl status tp2-roboflow-inference.service`
  - resultado: unit not found
  - `docker ps`
  - resultado: ningun contenedor exponiendo `9001`

## Conclusion operativa actual

- El lado EPC esta listo para la arquitectura final:
  - el control del coche permanece en EPC
  - la ruta MQTT/Mosquitto permanece sin cambios
  - el control manual en vivo puede invocar un endpoint de inferencia compatible con Roboflow por configuracion
- La inferencia en Jetson aun no esta activa:
  - no hay servicio activo en el puerto `9001`
  - no se encontro checkout del repo en Jetson
  - no se encontro runtime Python de `inference` en Jetson
  - no se encontro `ROBOFLOW_API_KEY` definido en el entorno de shell comprobado en Jetson

## Bloqueo para la inferencia Jetson extremo a extremo

El nuevo runtime del EPC ya esta listo para llamar a Jetson, pero Jetson todavia necesita que su servicio de inferencia Roboflow este arrancado y configurado con el modelo/API key del usuario para que la inferencia de frames pueda completarse extremo a extremo.
