#!/usr/bin/env python3
"""Configure Bigcapital MAIL_* on the VM and restart the server.

Usage (from Windows, with VM SSH on 127.0.0.1:2222):

  python deploy/bigcapital/configure-smtp.py ^
    --host smtp.gmail.com --port 587 --user astransdb@gmail.com ^
    --password "xxxx xxxx xxxx xxxx" --from-address astransdb@gmail.com

Does not print the password. Updates /opt/bigcapital/.env only.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request

import paramiko

ENV_PATH = "/opt/bigcapital/.env"
KEYS = [
    "MAIL_HOST",
    "MAIL_PORT",
    "MAIL_SECURE",
    "MAIL_USERNAME",
    "MAIL_PASSWORD",
    "MAIL_FROM_NAME",
    "MAIL_FROM_ADDRESS",
    "BASE_URL",
]


def upsert_env(text: str, updates: dict[str, str]) -> str:
    lines = text.splitlines()
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        if not line.strip() or line.lstrip().startswith("#") or "=" not in line:
            out.append(line)
            continue
        key, _ = line.split("=", 1)
        if key in updates:
            out.append(f"{key}={updates[key]}")
            seen.add(key)
        else:
            out.append(line)
    for key, value in updates.items():
        if key not in seen:
            out.append(f"{key}={value}")
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", required=True, help="SMTP host, e.g. smtp.gmail.com")
    ap.add_argument("--port", default="587")
    ap.add_argument("--secure", default="false", choices=["true", "false"])
    ap.add_argument("--user", required=True, help="SMTP username / login email")
    ap.add_argument("--password", required=True, help="SMTP password or app password")
    ap.add_argument("--from-name", default="Astrans Books")
    ap.add_argument("--from-address", default="", help="Defaults to --user")
    ap.add_argument("--base-url", default="https://books.astransdms.xyz")
    ap.add_argument("--ssh-host", default="127.0.0.1")
    ap.add_argument("--ssh-port", type=int, default=2222)
    ap.add_argument("--ssh-user", default="astrans")
    ap.add_argument("--ssh-password", default="Astrans")
    ap.add_argument("--test-email", default="", help="Send forgot-password API call to this email")
    args = ap.parse_args()

    from_address = args.from_address or args.user
    # Gmail app passwords often pasted with spaces — strip them.
    smtp_password = re.sub(r"\s+", "", args.password)

    updates = {
        "MAIL_HOST": args.host,
        "MAIL_PORT": str(args.port),
        "MAIL_SECURE": args.secure,
        "MAIL_USERNAME": args.user,
        "MAIL_PASSWORD": smtp_password,
        "MAIL_FROM_NAME": args.from_name,
        "MAIL_FROM_ADDRESS": from_address,
        "BASE_URL": args.base_url,
    }

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

    sftp = client.open_sftp()
    with sftp.open(ENV_PATH, "r") as f:
        current = f.read().decode("utf-8", "replace")
    # backup
    with sftp.open(ENV_PATH + ".bak-mail", "w") as f:
        f.write(current)
    new_text = upsert_env(current, updates)
    with sftp.open(ENV_PATH, "w") as f:
        f.write(new_text)
    sftp.close()
    print(f"Updated {ENV_PATH} (backup: {ENV_PATH}.bak-mail)")
    for key in KEYS:
        if key == "MAIL_PASSWORD":
            print(f"  {key}=*** ({len(smtp_password)} chars)")
        else:
            print(f"  {key}={updates[key]}")

    def run(cmd: str, timeout: int = 180) -> tuple[int, str]:
        print(f"\n$ {cmd}")
        _i, o, e = client.exec_command(cmd, timeout=timeout)
        out = o.read().decode("utf-8", "replace")
        err = e.read().decode("utf-8", "replace")
        code = o.channel.recv_exit_status()
        if out.strip():
            print(out.strip()[:3000])
        if err.strip():
            print(err.strip()[:1500])
        return code, out

    run(
        "cd /opt/bigcapital && docker compose "
        "-f docker-compose.prod.yml -f docker-compose.minio.yml "
        "-f docker-compose.webapp-patch.yml -f docker-compose.server-patch.yml "
        "-f docker-compose.restart.yml -f branding/docker-compose.branding.yml "
        "up -d --force-recreate server"
    )
    time.sleep(8)
    run(
        "docker exec bigcapital-server sh -c "
        "'printenv MAIL_HOST MAIL_PORT MAIL_SECURE MAIL_USERNAME MAIL_FROM_ADDRESS BASE_URL; "
        "printenv MAIL_PASSWORD | wc -c'"
    )

    test_email = args.test_email or args.user
    print(f"\nTriggering send_reset_password for {test_email} ...")
    body = json.dumps({"email": test_email}).encode()
    req = urllib.request.Request(
        f"{args.base_url.rstrip('/')}/api/auth/send_reset_password",
        data=body,
        headers={"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            print("API", resp.status, resp.read().decode()[:300])
    except urllib.error.HTTPError as ex:
        print("API ERR", ex.code, ex.read().decode()[:500])
        client.close()
        return 1

    time.sleep(3)
    run(
        "docker logs bigcapital-server --since 2m 2>&1 | "
        "grep -iE 'mail|smtp|reset|ECONNREFUSED|Invalid login|Username and Password' | tail -30"
    )
    client.close()
    print(
        "\nDone. If logs show no SMTP error, check the inbox (and spam) for the reset link."
    )
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
