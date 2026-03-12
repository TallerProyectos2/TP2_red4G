#!/usr/bin/env bash
set -euo pipefail

# Instala Tailscale en Jetson ARM64 usando el tarball estatico oficial.
# Evita apt para no bloquearse con dependencias rotas de CUDA/NVIDIA.
#
# Uso:
#   bash scripts/install_tailscale_jetson.sh
#
# Opcional:
#   TAILSCALE_VERSION=1.94.2 bash scripts/install_tailscale_jetson.sh
#   TAILSCALE_AUTHKEY=tskey-xxxx bash scripts/install_tailscale_jetson.sh
#   TAILSCALE_HOSTNAME=tp2-jetson bash scripts/install_tailscale_jetson.sh

TAILSCALE_VERSION="${TAILSCALE_VERSION:-1.94.2}"
TAILSCALE_HOSTNAME="${TAILSCALE_HOSTNAME:-}"
TAILSCALE_AUTHKEY="${TAILSCALE_AUTHKEY:-}"

if [[ "$(uname -m)" != "aarch64" ]]; then
  echo "ERROR: este script esta pensado para Jetson/ARM64. Arquitectura detectada: $(uname -m)" >&2
  exit 1
fi

TMP_DIR="$(mktemp -d /tmp/tailscale-install.XXXXXX)"
PKG="tailscale_${TAILSCALE_VERSION}_arm64.tgz"
PKG_URL="https://pkgs.tailscale.com/stable/${PKG}"
SHA_URL="${PKG_URL}.sha256"

cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

echo "[1/9] Comprobando herramientas base..."
command -v curl >/dev/null
command -v tar >/dev/null
command -v sha256sum >/dev/null
command -v systemctl >/dev/null

echo "[2/9] Cargando modulo tun si existe..."
sudo modprobe tun || true

echo "[3/9] Descargando paquete estatico de Tailscale ${TAILSCALE_VERSION}..."
cd "${TMP_DIR}"
curl -fsSLO "${PKG_URL}"
curl -fsSLo "${PKG}.sha256" "${SHA_URL}"

echo "[4/9] Verificando checksum..."
EXPECTED_SHA="$(tr -d '\r' < "${PKG}.sha256" | awk '{print $1; exit}')"
ACTUAL_SHA="$(sha256sum "${PKG}" | awk '{print $1}')"

if [[ -z "${EXPECTED_SHA}" ]]; then
  echo "ERROR: no se pudo extraer el checksum esperado desde ${SHA_URL}" >&2
  exit 1
fi

if [[ "${EXPECTED_SHA}" != "${ACTUAL_SHA}" ]]; then
  echo "ERROR: checksum incorrecto para ${PKG}" >&2
  echo "Esperado: ${EXPECTED_SHA}" >&2
  echo "Actual:    ${ACTUAL_SHA}" >&2
  exit 1
fi

echo "[5/9] Extrayendo binarios..."
tar xzf "${PKG}"
cd "tailscale_${TAILSCALE_VERSION}_arm64"

echo "[6/9] Instalando tailscale y tailscaled en /usr/local/bin..."
sudo install -m 0755 tailscale /usr/local/bin/tailscale
sudo install -m 0755 tailscaled /usr/local/bin/tailscaled

echo "[7/9] Preparando estado y servicio systemd..."
sudo install -d -m 0755 /var/lib/tailscale

sudo tee /etc/systemd/system/tailscaled.service >/dev/null <<'SERVICE'
[Unit]
Description=Tailscale node agent
Documentation=https://tailscale.com/kb/
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/usr/local/bin/tailscaled --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock
ExecStop=/usr/bin/env pkill -x tailscaled
Restart=on-failure
RestartSec=5
RuntimeDirectory=tailscale

[Install]
WantedBy=multi-user.target
SERVICE

echo "[8/9] Habilitando y arrancando tailscaled..."
sudo systemctl daemon-reload
sudo systemctl enable --now tailscaled
sudo systemctl --no-pager --full status tailscaled

echo "[9/9] Conectando la Jetson al tailnet..."
UP_CMD=(sudo /usr/local/bin/tailscale up --ssh)

if [[ -n "${TAILSCALE_HOSTNAME}" ]]; then
  UP_CMD+=(--hostname="${TAILSCALE_HOSTNAME}")
fi

if [[ -n "${TAILSCALE_AUTHKEY}" ]]; then
  UP_CMD+=(--authkey="${TAILSCALE_AUTHKEY}")
fi

echo "Ejecutando: ${UP_CMD[*]}"
"${UP_CMD[@]}"

echo
echo "Tailscale instalado y configurado."
echo "Comprobaciones recomendadas:"
echo "  tailscale status"
echo "  tailscale ip -4"
echo
echo "Si Tailscale SSH esta habilitado en tu tailnet, podras entrar con:"
echo "  ssh grupo2tpii@<tailscale-ip>"
