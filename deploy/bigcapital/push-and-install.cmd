@echo off
REM Copy install script + env template to the VM, then SSH and run install.
REM Usage (from Windows, with your working SSH alias/key):
REM   deploy\bigcapital\push-and-install.cmd astrans@127.0.0.1 -p 2222

if "%~1"=="" (
  echo Usage: push-and-install.cmd user@host [ssh options...]
  echo Example: push-and-install.cmd -p 2222 astrans@127.0.0.1
  exit /b 1
)

set REMOTE=%*
scp -P 2222 "%~dp0install-on-vm.sh" "%~dp0.env.template" astrans@127.0.0.1:/tmp/ 2>nul
if errorlevel 1 (
  echo scp with -P 2222 failed — retrying with args: %REMOTE%
  scp %REMOTE% "%~dp0install-on-vm.sh" "%~dp0.env.template" :/tmp/
)

echo.
echo Now SSH to the VM and run:
echo   sudo mkdir -p /opt/bigcapital-helpers ^&^& sudo mv /tmp/install-on-vm.sh /tmp/.env.template /opt/bigcapital-helpers/
echo   chmod +x /opt/bigcapital-helpers/install-on-vm.sh
echo   /opt/bigcapital-helpers/install-on-vm.sh
echo Then edit /opt/bigcapital/.env and set BASE_URL + DB passwords.
