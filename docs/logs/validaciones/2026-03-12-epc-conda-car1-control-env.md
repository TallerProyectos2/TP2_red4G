# Entorno Conda del EPC para control manual de Car1

- Fecha: `2026-03-12`
- Maquina: `tp2-EPC`

## Objetivo

Aprovisionar un entorno Conda aislado en el EPC para `servicios/prueba.py` (control manual de car 1) y validar que el script puede arrancar enlazando la direccion del lado LTE.

## Evidencia de ejecucion

- `conda` no estaba presente inicialmente en el EPC.
- Miniforge instalado en:
  - `/home/tp2/miniforge3`
- Entorno Conda creado:
  - `tp2-car1-control`
- Script desplegado en la ruta de runtime:
  - `/home/tp2/servicios_tp2/prueba.py`
- Los hashes del script fuente y del desplegado coinciden:
  - `sha256 d4ec3b7f34ffcf3c9575881a5db9585ac943ccab305ab70d52b44cf36e7d9c71`
- Validacion de paquetes/imports dentro del nuevo entorno con display X activo:
  - `cv2 4.10.0`
  - `numpy 2.2.6`
  - el import de `pynput` tuvo exito cuando `DISPLAY=:1`
- Validacion del bind en runtime:
  - `DISPLAY=:1 timeout 8s conda run -n tp2-car1-control python -u /home/tp2/servicios_tp2/prueba.py`
  - `ss -lunp` mostro el listener:
    - `172.16.0.1:20001`

## Notas operativas

- Las sesiones SSH entran al EPC sin `DISPLAY`, pero la maquina tiene una sesion grafica activa en `:1`.
- `pynput` requiere un display X valido; sin `DISPLAY=:1` el import falla aunque el paquete este instalado.

## Resultado

- El EPC dispone ahora de un entorno Conda dedicado para el control manual de car 1.
- `prueba.py` arranca correctamente y enlaza `172.16.0.1:20001` cuando se lanza con `DISPLAY=:1`.
