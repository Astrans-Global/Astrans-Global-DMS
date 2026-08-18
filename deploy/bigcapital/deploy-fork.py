#!/usr/bin/env python3
"""Pull the latest Astrans-Global/bigcapital fork source, rebuild the
server+webapp images, and recreate them on the VM.

This is the ONE canonical way to ship a new fork commit to
books.astransdms.xyz. Run it from Windows, with the VM reachable at
127.0.0.1:2222 over SSH (VirtualBox port-forward):

    python deploy/bigcapital/deploy-fork.py

Deliberately does NOT include `branding/docker-compose.branding.yml` --
that runtime overlay is retired (see README.md / RESILIENCE.md). Branding
(title, favicons, manifest, logos, dark/light preload) is baked natively
into the fork source (`packages/webapp/index.html` + `public/*`) and is
always correct on every fresh build. Re-adding that overlay bind-mounts a
stale, hand-generated `index.html` that still references the *previous*
build's content-hashed JS/CSS filenames -- since those hashes change on
every webapp rebuild, the mismatch 404s the main bundle and the whole app
renders as a blank page. This exact incident happened on 2026-08-18;
don't re-add the overlay to fix branding drift -- fix/re-bake the source
webapp/index.html + public/* assets instead.

Migrations: this script does NOT run `tenants:migrate:latest` -- if your
fork commit adds a tenant migration, run it manually first (see
README.md "To rebuild and redeploy after pulling new fork commits").
"""
from __future__ import annotations

import argparse
import sys
import time

import paramiko

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

COMPOSE_FILES = (
    "-f /opt/bigcapital/docker-compose.prod.yml "
    "-f /opt/bigcapital/docker-compose.minio.yml "
    "-f /opt/bigcapital/docker-compose.fork-build.yml "
    "-f /opt/bigcapital/docker-compose.restart.yml"
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ssh-host", default="127.0.0.1")
    ap.add_argument("--ssh-port", type=int, default=2222)
    ap.add_argument("--ssh-user", default="astrans")
    ap.add_argument("--ssh-password", default="Astrans")
    ap.add_argument(
        "--skip-pull",
        action="store_true",
        help="Rebuild/redeploy the currently checked-out commit on the VM without git fetch/reset first.",
    )
    args = ap.parse_args()

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        args.ssh_host,
        port=args.ssh_port,
        username=args.ssh_user,
        password=args.ssh_password,
        timeout=25,
        allow_agent=False,
        look_for_keys=False,
    )

    def run(cmd: str, timeout: int = 1800) -> int:
        print(f"\n$ {cmd}", flush=True)
        _i, o, e = client.exec_command(cmd, timeout=timeout)
        while not o.channel.exit_status_ready():
            while o.channel.recv_ready():
                print(o.channel.recv(4096).decode("utf-8", "replace"), end="", flush=True)
            time.sleep(0.5)
        while o.channel.recv_ready():
            print(o.channel.recv(4096).decode("utf-8", "replace"), end="", flush=True)
        code = o.channel.recv_exit_status()
        err = e.read().decode("utf-8", "replace")
        if err.strip():
            print("STDERR:", err.strip()[:3000], flush=True)
        print(f"[exit={code}]", flush=True)
        return code

    if not args.skip_pull:
        code = run(
            "cd /home/astrans/bigcapital-src && git fetch origin && "
            "git reset --hard origin/astrans-main && git log --oneline -3"
        )
        if code != 0:
            print("git pull failed, aborting.")
            client.close()
            return 1

    for service in ("server", "webapp"):
        code = run(
            f"cd /opt/bigcapital && docker compose {COMPOSE_FILES} build {service} 2>&1 | tail -n 100"
        )
        if code != 0:
            print(f"{service} build failed, aborting.")
            client.close()
            return 1

    run(f"cd /opt/bigcapital && docker compose {COMPOSE_FILES} up -d --force-recreate server webapp")
    time.sleep(10)
    run("docker ps --format '{{.Names}}\\t{{.Status}}' | grep bigcapital")
    run(
        "curl -s https://books.astransdms.xyz/ | "
        "grep -oE '(src|href)=\"[^\"]*\\.(js|css)\"|<title>[^<]*</title>'"
    )
    run(
        "curl -s -o /dev/null -w 'index.html: HTTP:%{http_code}\\n' https://books.astransdms.xyz/ && "
        "for f in $(curl -s https://books.astransdms.xyz/ | grep -oE '/assets/[^\"]+\\.(js|css)'); do "
        "curl -s -o /dev/null -w \"$f: HTTP:%{http_code}\\n\" \"https://books.astransdms.xyz$f\"; done"
    )

    client.close()
    print("\nDone. Confirm every asset above returned HTTP:200 before calling this deploy good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
