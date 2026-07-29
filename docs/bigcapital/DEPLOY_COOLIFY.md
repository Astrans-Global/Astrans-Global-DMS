# Deploy Bigcapital on Coolify (VirtualBox Ubuntu)

Host now: **Oracle VirtualBox** Ubuntu + Coolify (tunnel `astransdms.xyz`).  
Later: move same Docker stack to a dedicated PC.

Official docs: [Docker deployment](https://docs.bigcapital.app/deployment/docker) · [Setup script](https://docs.bigcapital.app/deployment/setup-script)

Coolify has **no official Bigcapital template** and community reports registration/DB auth pain when forcing a “native Coolify service”. Prefer **Docker Compose on the VM** (Coolify can still manage the host; Bigcapital runs as compose). Expose via Cloudflare Tunnel hostname (e.g. `books.astransdms.xyz` → VM port `80`).

## Prerequisites on the VM

- Docker + Docker Compose plugin  
- Disk free ≥ 20 GB recommended  
- Do **not** bind MySQL/Redis ports publicly  

## Option A — Official setup (recommended)

SSH into the VM, then:

```bash
sudo mkdir -p /opt/bigcapital && sudo chown "$USER":"$USER" /opt/bigcapital
cd /opt/bigcapital
curl -fsSL https://raw.githubusercontent.com/bigcapitalhq/bigcapital/master/package/docker-start.sh -o docker-start.sh
# If the setup script URL changes, use:
# git clone --depth 1 -b main https://github.com/bigcapitalhq/bigcapital.git .
# cp .env.example .env
# nano .env
# docker compose --file docker-compose.prod.yml up -d
```

Or clone + compose (stable path):

```bash
cd /opt
git clone --depth 1 -b main https://github.com/bigcapitalhq/bigcapital.git
cd bigcapital
cp .env.example .env
```

Edit `.env` at minimum:

| Variable | Guidance |
|----------|----------|
| `DB_USER` / `DB_PASSWORD` / `DB_ROOT_PASSWORD` | Strong unique passwords |
| `JWT_SECRET` | Long random string |
| `BASE_URL` | Final public URL, e.g. `https://books.astransdms.xyz` |
| `PUBLIC_PROXY_PORT` | `80` (tunnel targets this) |
| Mail vars | Can be dummy for first boot; fix before production invites |

Start:

```bash
docker compose --file docker-compose.prod.yml up -d
docker compose --file docker-compose.prod.yml ps
docker ps -a | grep bigcapital-database-migration
# check migration logs until success
```

Local check on VM:

```bash
curl -I http://127.0.0.1:80/
```

## Option B — Coolify “Docker Compose” resource

1. Coolify → Project **Astrans DMS** → **+ Resource** → **Docker Compose**  
2. Paste / upload compose based on upstream `docker-compose.prod.yml`  
3. Set same env as `.env`  
4. **Important:** do not publish MySQL/Redis ports to the internet  
5. Map public hostname via Coolify proxy **or** Cloudflare Tunnel to the proxy service port  

If registration hangs, check MySQL logs for auth errors (known Coolify pitfall) and fall back to Option A on the host.

## Cloudflare Tunnel

After containers are healthy on localhost:80:

1. Cloudflare Zero Trust → Tunnel `astrans-dms`  
2. Public hostname: `books.astransdms.xyz` → `http://127.0.0.1:80` (or Docker host IP if needed)  
3. Keep Coolify on `astransdms.xyz` as today  

## First login

1. Open Bigcapital URL  
2. Create the **first admin** immediately (no default user)  
3. Set organization currency **LKR**  
4. Follow [CHART_OF_ACCOUNTS.md](CHART_OF_ACCOUNTS.md)  

Optional: disable public signup after first user (`SIGNUP_DISABLED=true`, recreate/restart).

## Helper files in this repo

| Path | Purpose |
|------|---------|
| [../../deploy/bigcapital/README.md](../../deploy/bigcapital/README.md) | Short deploy checklist |
| [../../deploy/bigcapital/.env.template](../../deploy/bigcapital/.env.template) | Env keys to copy |
| [../../deploy/bigcapital/install-on-vm.sh](../../deploy/bigcapital/install-on-vm.sh) | Run on the Ubuntu VM |

## Verify success

- [ ] `docker compose ps` shows webapp, server, mysql, redis, proxy running  
- [ ] Migration container exited 0  
- [ ] Browser reaches Bigcapital login/signup  
- [ ] Can create org with LKR  
