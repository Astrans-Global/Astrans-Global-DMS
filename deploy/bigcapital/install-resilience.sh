#!/usr/bin/env bash
# Install Bigcapital resilience on the Ubuntu VM. Run as astrans (with sudo).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
BIGCAPITAL_DIR="${BIGCAPITAL_DIR:-/opt/bigcapital}"

if [[ ! -d "$BIGCAPITAL_DIR" ]]; then
  echo "Missing $BIGCAPITAL_DIR" >&2
  exit 1
fi

sudo mkdir -p /etc/systemd/resolved.conf.d
sudo tee /etc/systemd/resolved.conf.d/astrans-dns.conf >/dev/null <<'EOF'
[Resolve]
DNS=1.1.1.1 8.8.8.8
FallbackDNS=1.0.0.1 8.8.4.4
DNSStubListener=yes
EOF
sudo systemctl restart systemd-resolved || true

sudo cp "$ROOT/docker-compose.restart.yml" "$BIGCAPITAL_DIR/docker-compose.restart.yml"
sudo cp "$ROOT/astrans-books-watchdog.sh" /usr/local/sbin/astrans-books-watchdog.sh
sudo chmod 755 /usr/local/sbin/astrans-books-watchdog.sh

sudo cp "$ROOT/systemd/bigcapital.service" /etc/systemd/system/bigcapital.service
sudo cp "$ROOT/systemd/astrans-books-watchdog.service" /etc/systemd/system/astrans-books-watchdog.service
sudo cp "$ROOT/systemd/astrans-books-watchdog.timer" /etc/systemd/system/astrans-books-watchdog.timer

# cloudflared: force http2 (QUIC flaps on VirtualBox NAT) + restart forever
sudo mkdir -p /etc/systemd/system/cloudflared.service.d
sudo cp "$ROOT/systemd/cloudflared-override.conf" /etc/systemd/system/cloudflared.service.d/override.conf

sudo systemctl daemon-reload
sudo systemctl enable --now bigcapital.service
sudo systemctl enable --now cloudflared.service || true
sudo systemctl enable --now astrans-books-watchdog.timer

# Apply unless-stopped and ensure stack is up
cd "$BIGCAPITAL_DIR"
sudo -u astrans docker compose \
  --file docker-compose.prod.yml \
  --file docker-compose.minio.yml \
  --file docker-compose.webapp-patch.yml \
  --file docker-compose.server-patch.yml \
  --file docker-compose.restart.yml \
  up -d

# Or if astrans owns the dir / docker group:
docker compose \
  --file docker-compose.prod.yml \
  --file docker-compose.minio.yml \
  --file docker-compose.webapp-patch.yml \
  --file docker-compose.server-patch.yml \
  --file docker-compose.restart.yml \
  up -d || true

sudo systemctl start astrans-books-watchdog.service || true

echo "OK — enabled: bigcapital.service, astrans-books-watchdog.timer, cloudflared, DNS override"
systemctl is-enabled bigcapital.service astrans-books-watchdog.timer cloudflared
systemctl list-timers astrans-books-watchdog.timer --no-pager
curl -sS -o /dev/null -w "local books: %{http_code}\n" http://127.0.0.1:8088/ || true
