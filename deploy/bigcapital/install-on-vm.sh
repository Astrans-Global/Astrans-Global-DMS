#!/usr/bin/env bash
# Run on the Ubuntu VM (VirtualBox or later dedicated PC).
set -euo pipefail

INSTALL_DIR="${INSTALL_DIR:-/opt/bigcapital}"
REPO_URL="${REPO_URL:-https://github.com/bigcapitalhq/bigcapital.git}"
BRANCH="${BRANCH:-main}"

echo "==> Installing Bigcapital into ${INSTALL_DIR}"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker is required. Install Docker Engine + Compose plugin first."
  exit 1
fi

if ! docker compose version >/dev/null 2>&1; then
  echo "Docker Compose plugin is required (docker compose)."
  exit 1
fi

sudo mkdir -p "$(dirname "$INSTALL_DIR")"
if [ ! -d "$INSTALL_DIR/.git" ]; then
  sudo git clone --depth 1 -b "$BRANCH" "$REPO_URL" "$INSTALL_DIR"
  sudo chown -R "$USER":"$USER" "$INSTALL_DIR"
else
  cd "$INSTALL_DIR"
  git fetch --depth 1 origin "$BRANCH"
  git checkout "$BRANCH"
  git pull --ff-only origin "$BRANCH" || true
fi

cd "$INSTALL_DIR"

if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    cp .env.example .env
  else
    echo "Missing .env.example — create .env manually from deploy/bigcapital/.env.template"
    exit 1
  fi
  echo "==> Created .env from .env.example — EDIT SECRETS before relying on this install."
fi

echo "==> Pulling and starting production compose"
docker compose --file docker-compose.prod.yml pull
docker compose --file docker-compose.prod.yml up -d

echo "==> Container status"
docker compose --file docker-compose.prod.yml ps

echo "==> Migration containers (should exit after success)"
docker ps -a --filter "name=bigcapital-database" --format "table {{.Names}}\t{{.Status}}" || true

echo ""
echo "Next:"
echo "  1) curl -I http://127.0.0.1:${PUBLIC_PROXY_PORT:-80}/"
echo "  2) Point Cloudflare Tunnel books.astransdms.xyz -> http://127.0.0.1:80"
echo "  3) Create first admin, currency LKR, then follow docs/bigcapital/CHART_OF_ACCOUNTS.md"
