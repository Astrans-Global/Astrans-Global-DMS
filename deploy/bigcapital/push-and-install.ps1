# Copy Bigcapital install helpers to the Ubuntu VM over SSH, then print run steps.
# Example:
#   .\deploy\bigcapital\push-and-install.ps1 -SshTarget "astrans@127.0.0.1" -Port 2222

param(
  [string]$SshTarget = "astrans@127.0.0.1",
  [int]$Port = 2222
)

$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path

Write-Host "Copying install-on-vm.sh and .env.template to ${SshTarget}:/tmp (port $Port)..."
scp -P $Port `
  (Join-Path $here "install-on-vm.sh") `
  (Join-Path $here ".env.template") `
  "${SshTarget}:/tmp/"

Write-Host ""
Write-Host "SSH in and run:"
Write-Host "  ssh -p $Port $SshTarget"
Write-Host "  chmod +x /tmp/install-on-vm.sh"
Write-Host "  /tmp/install-on-vm.sh"
Write-Host "  nano /opt/bigcapital/.env   # set DB passwords, JWT, BASE_URL=https://books.astransdms.xyz"
Write-Host "  cd /opt/bigcapital && docker compose --file docker-compose.prod.yml up -d"
Write-Host ""
Write-Host "Then Cloudflare Tunnel: books.astransdms.xyz -> http://127.0.0.1:80"
Write-Host "Then: docs/bigcapital/CONFIGURE_COA_RUNBOOK.md"
