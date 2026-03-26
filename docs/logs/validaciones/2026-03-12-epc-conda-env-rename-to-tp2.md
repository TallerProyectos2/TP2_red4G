# Renombrado del entorno Conda del EPC a tp2

- Fecha: `2026-03-12`
- Maquina: `tp2-EPC`

## Objetivo

Renombrar el entorno Conda de control manual de car 1 de `tp2-car1-control` a `tp2`.

## Evidencia de ejecucion

- Lista de entornos antes del cambio:
  - `base`
  - `tp2-car1-control`
- Nuevo entorno creado por clonacion:
  - `tp2`
- Validacion dentro del entorno renombrado con display X activo:
  - `DISPLAY=:1 conda run -n tp2 python -c "import cv2, numpy, pynput; ..."`
  - observado:
    - `cv2 4.10.0`
    - `numpy 2.2.6`
    - el import de `pynput` tuvo exito
- Validacion del bind en runtime:
  - `DISPLAY=:1 timeout 8s conda run -n tp2 python -u /home/tp2/servicios_tp2/prueba.py`
  - `ss -lunp` mostro el listener:
    - `172.16.0.1:20001`
- Entorno antiguo eliminado tras la validacion:
  - `conda remove -y -n tp2-car1-control --all`
- Lista de entornos despues del cambio:
  - `base`
  - `tp2`

## Resultado

- El entorno Conda del EPC para el control manual de car 1 ahora se llama `tp2`.
- `prueba.py` sigue arrancando correctamente desde el entorno renombrado y enlaza `172.16.0.1:20001`.
