# Astrans Global DMS

Distribution management for Astrans, built as a native fork of [Bigcapital](https://github.com/bigcapitalhq/bigcapital) — one system, not a separate app.

**Repo:** [Astrans-Global/Astrans-Global-DMS](https://github.com/Astrans-Global/Astrans-Global-DMS)

## Architecture (current direction)

- **One system:** a maintained source fork of Bigcapital (server + webapp), extended with Phase 1 distribution-ops features (item price-lots, GRN VAT handling, invoice status workflow, per-area numbering, customer risk grading, Secondary P&L, Delivery Prep, VAT/Non-VAT invoicing) built natively into its existing modules.
- **Hosting:** VirtualBox Ubuntu VM / Coolify (move to dedicated PC later), Cloudflare Tunnel (`books.astransdms.xyz`).
- There is no separate Next.js "Astrans DMS" application anymore — see [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for what was retired and why.

See [docs/bigcapital/README.md](docs/bigcapital/README.md) for the accounting core docs.

## What's in this repo

- `docs/` — architecture, chart of accounts, VAT policy, event-posting matrix, Phase 1 spec.
- `deploy/bigcapital/` — VM install/deploy tooling, branding, patches, and (once created) the Bigcapital fork build pipeline.
- `resources/` — sample VAT / Non-VAT invoice formats used to build the invoice output templates.

## Bigcapital on the VM

Follow [docs/bigcapital/DEPLOY_COOLIFY.md](docs/bigcapital/DEPLOY_COOLIFY.md) and run [deploy/bigcapital/install-on-vm.sh](deploy/bigcapital/install-on-vm.sh) **on the Ubuntu VM**.

Then configure COA: [docs/bigcapital/CONFIGURE_COA_RUNBOOK.md](docs/bigcapital/CONFIGURE_COA_RUNBOOK.md).

## Docs

- [docs/bigcapital/](docs/bigcapital/) — books, COA, deploy, VAT 1B, event matrix, scope
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — single-system rules
- [docs/ops/PHASE1.md](docs/ops/PHASE1.md) — Phase 1 operational spec
- [docs/BACKUP.md](docs/BACKUP.md) — backups

## Status

Bigcapital is live on the VM. Phase 1 native buildout (see the project plan) is in progress: item price-lots, GRN handling, invoice workflow, customer risk grading, Secondary P&L, Delivery Prep, and VAT/Non-VAT invoice output are being added directly into a Bigcapital source fork.
