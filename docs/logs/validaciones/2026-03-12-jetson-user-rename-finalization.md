# Finalizacion del renombrado de usuario en Jetson

- Fecha: `2026-03-12`
- Jira: `N/A (Atlassian MCP no disponible en esta sesion)`
- Maquina: `tp2-jetson`
- Alcance:
  - sustituir la cuenta temporal `grupo4` por los datos del usuario original de Jetson
  - dejar solo la cuenta final `grupo4` en la maquina

## Estado inicial

- El hostname y el hostname de Tailscale ya estaban configurados como `tp2-jetson`.
- El acceso SSH ya funcionaba como `grupo4@tp2-jetson`, pero esa cuenta `grupo4` seguia siendo el usuario temporal de migracion.
- La cuenta original seguia existiendo como:
  - usuario: `grupo2tpii`
  - uid: `1000`
  - home: `/home/grupo2tpii`
- Tambien existia una cuenta admin temporal:
  - `tp2admin`

## Cambio aplicado

- Se confirmo que ya no quedaban sesiones activas de `grupo2tpii`.
- Se elimino la cuenta temporal `grupo4` y su directorio home.
- Se renombro el grupo principal original:
  - `grupo2tpii` -> `grupo4`
- Se renombro el usuario original:
  - `grupo2tpii` -> `grupo4`
- Se movio el directorio home original:
  - `/home/grupo2tpii` -> `/home/grupo4`
- Se actualizo el metadata de cuenta de escritorio:
  - `/var/lib/AccountsService/users/grupo4`
- Se actualizaron los mapeos subordinados de uid/gid:
  - `/etc/subuid`
  - `/etc/subgid`
- Se actualizo el campo GECOS/comentario de la cuenta final a `grupo4`.
- Se elimino el usuario administrador temporal:
  - `tp2admin`

## Validacion

- El acceso SSH final funciona:
  - `ssh grupo4@tp2-jetson`
- Identidad final de la cuenta:
  - usuario: `grupo4`
  - uid: `1000`
  - gid: `1000`
  - home: `/home/grupo4`
- Usuario antiguo eliminado:
  - `getent passwd grupo2tpii` -> sin resultado
- Usuario temporal eliminado:
  - `getent passwd tp2admin` -> sin resultado
- Directorios home:
  - `/home` contiene solo `grupo4`
- `sudo` funciona con la cuenta final.
- `sudo apt-get check` completa sin errores de dependencias.

## Acceso final

- Principal:
  - `ssh grupo4@tp2-jetson`
- Alternativo:
  - `ssh grupo4@100.115.99.8`
  - `ssh grupo4@192.168.72.127`
