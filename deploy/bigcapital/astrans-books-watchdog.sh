#!/usr/bin/env bash
# Keep Astrans Books (Bigcapital + Cloudflare Tunnel) healthy without SSH.
# Installed as /usr/local/sbin/astrans-books-watchdog.sh
set -euo pipefail

COMPOSE_DIR="${BIGCAPITAL_DIR:-/opt/bigcapital}"
# Must match the fork-build overlay used by bigcapital.service, or a health
# blip here silently recreates server/webapp on stock bigcapitalhq/*:latest
# images instead of our branded astrans/*:local fork builds. See
# docs/bigcapital/MIGRATE_TO_DEDICATED_PC.md for the incident writeup.
COMPOSE_FILES=(
  --file docker-compose.prod.yml
  --file docker-compose.minio.yml
  --file docker-compose.fork-build.yml
  --file docker-compose.restart.yml
)
LOG_TAG="astrans-books-watchdog"
BOOKS_URL="${BOOKS_HEALTH_URL:-http://127.0.0.1:8088/}"

log() { logger -t "$LOG_TAG" "$*"; echo "$*"; }

need_sudo() {
  if [[ "${EUID}" -eq 0 ]]; then
    "$@"
  elif command -v sudo >/dev/null && sudo -n true 2>/dev/null; then
    sudo -n "$@"
  else
    "$@"
  fi
}

ensure_dns() {
  # Router DNS sometimes breaks tunnel lookups; keep Cloudflare/Google DNS configured.
  local conf=/etc/systemd/resolved.conf.d/astrans-dns.conf
  if [[ ! -f "$conf" ]]; then
    log "writing DNS override $conf"
    need_sudo mkdir -p /etc/systemd/resolved.conf.d
    need_sudo tee "$conf" >/dev/null <<'EOF'
[Resolve]
DNS=1.1.1.1 8.8.8.8
FallbackDNS=1.0.0.1 8.8.4.4
DNSStubListener=yes
EOF
    need_sudo systemctl restart systemd-resolved || true
  fi
}

ensure_tunnel() {
  if systemctl is-active --quiet cloudflared; then
    return 0
  fi
  log "cloudflared not active — restarting"
  need_sudo systemctl reset-failed cloudflared || true
  need_sudo systemctl restart cloudflared || true
  sleep 3
  if systemctl is-active --quiet cloudflared; then
    log "cloudflared recovered"
  else
    log "cloudflared still down"
    return 1
  fi
}

compose() {
  (cd "$COMPOSE_DIR" && docker compose "${COMPOSE_FILES[@]}" "$@")
}

ensure_books() {
  local code
  code=$(curl -sS -o /dev/null -w '%{http_code}' --connect-timeout 3 --max-time 8 "$BOOKS_URL" || echo 000)
  if [[ "$code" == "200" || "$code" == "301" || "$code" == "302" || "$code" == "304" ]]; then
    return 0
  fi
  log "books health failed (HTTP $code) — docker compose up -d"
  compose up -d || true
  sleep 5
  code=$(curl -sS -o /dev/null -w '%{http_code}' --connect-timeout 3 --max-time 8 "$BOOKS_URL" || echo 000)
  log "books health after compose: HTTP $code"
}

main() {
  ensure_dns
  ensure_tunnel || true
  if [[ -d "$COMPOSE_DIR" ]]; then
    ensure_books || true
  else
    log "missing $COMPOSE_DIR"
  fi
}

main "$@"
