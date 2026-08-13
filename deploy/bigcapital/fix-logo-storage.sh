#!/usr/bin/env bash
# Fix Bigcapital logo/uploads by adding MinIO + S3 env (run on Ubuntu VM).
set -euo pipefail

cd /opt/bigcapital

echo "==> Restoring docker-compose.prod.yml if broken"
if ! docker compose --file docker-compose.prod.yml config >/dev/null 2>&1; then
  git checkout -- docker-compose.prod.yml
fi

echo "==> Writing docker-compose.minio.yml"
cat > docker-compose.minio.yml <<'EOF'
services:
  minio:
    container_name: bigcapital-minio
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: astransminio
      MINIO_ROOT_PASSWORD: AstransMinio2026
    volumes:
      - minio:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - bigcapital_network
    restart: on-failure

volumes:
  minio:
    name: bigcapital_prod_minio
    driver: local
EOF

echo "==> Ensuring S3_FORCE_PATH_STYLE is passed to server container"
if ! grep -q 'S3_FORCE_PATH_STYLE' docker-compose.prod.yml; then
  # Insert after S3_BUCKET env line inside server service
  python3 - <<'PY'
from pathlib import Path
p = Path("docker-compose.prod.yml")
text = p.read_text()
needle = "- S3_BUCKET=${S3_BUCKET}"
insert = "- S3_BUCKET=${S3_BUCKET}\n      - S3_FORCE_PATH_STYLE=${S3_FORCE_PATH_STYLE}"
if needle in text and "S3_FORCE_PATH_STYLE=${S3_FORCE_PATH_STYLE}" not in text:
    text = text.replace(needle, insert, 1)
    p.write_text(text)
    print("Inserted S3_FORCE_PATH_STYLE into docker-compose.prod.yml")
else:
    print("S3_FORCE_PATH_STYLE already present or S3_BUCKET line not found")
PY
fi

echo "==> Updating .env S3 settings"
python3 - <<'PY'
from pathlib import Path
p = Path(".env")
lines = p.read_text().splitlines()
wanted = {
    "S3_REGION": "us-east-1",
    "S3_ACCESS_KEY_ID": "astransminio",
    "S3_SECRET_ACCESS_KEY": "AstransMinio2026",
    "S3_ENDPOINT": "http://minio:9000",
    "S3_BUCKET": "bigcapital",
    "S3_FORCE_PATH_STYLE": "true",
}
keys = set(wanted)
out = []
seen = set()
for line in lines:
    if not line or line.lstrip().startswith("#") or "=" not in line:
        out.append(line)
        continue
    k = line.split("=", 1)[0].strip()
    if k in keys:
        out.append(f"{k}={wanted[k]}")
        seen.add(k)
    else:
        out.append(line)
for k, v in wanted.items():
    if k not in seen:
        out.append(f"{k}={v}")
p.write_text("\n".join(out) + "\n")
print("Updated .env S3 keys")
PY

echo "==> Validating compose"
docker compose --file docker-compose.prod.yml --file docker-compose.minio.yml config >/dev/null
echo "Compose OK"

echo "==> Starting stack + MinIO"
docker compose --file docker-compose.prod.yml --file docker-compose.minio.yml up -d

echo "==> Waiting for MinIO"
for i in $(seq 1 30); do
  if curl -sf http://127.0.0.1:9000/minio/health/live >/dev/null 2>&1; then
    echo "MinIO is up"
    break
  fi
  sleep 2
done

echo "==> Creating bucket 'bigcapital' if missing"
docker run --rm --network bigcapital_bigcapital_network \
  -e MC_HOST_local=http://astransminio:AstransMinio2026@minio:9000 \
  minio/mc:latest \
  mb --ignore-existing local/bigcapital || true

# Anonymous download helps browser display logos (private bucket often breaks UI)
docker run --rm --network bigcapital_bigcapital_network \
  -e MC_HOST_local=http://astransminio:AstransMinio2026@minio:9000 \
  minio/mc:latest \
  anonymous set download local/bigcapital || true

echo "==> Restarting Bigcapital server to pick up S3 env"
docker compose --file docker-compose.prod.yml --file docker-compose.minio.yml up -d server

sleep 5
echo "==> Status"
docker ps --format 'table {{.Names}}\t{{.Status}}\t{{.Ports}}' | grep -E 'bigcapital|minio|NAMES' || true
echo
echo "Done. Retry company logo upload on https://books.astransdms.xyz"
echo "MinIO console (optional): ssh -p 2222 -L 9001:127.0.0.1:9001 astrans@127.0.0.1"
echo "then open http://127.0.0.1:9001  user=astransminio pass=AstransMinio2026"
