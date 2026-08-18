# Handoff: continuing Phase 1 with Grok 4.6 (after Claude Sonnet 5)

Read this whole file before touching anything. It's written for an AI
coding agent picking up this project cold, because that's exactly what's
happening: Sonnet 5 built Phase 1 so far and ran out of budget; you
(Grok 4.6) are continuing it in the same workspace/repos.

**Revert point:** both repos are tagged `pre-grok-handoff-20260818` at the
exact commit Sonnet 5 left things in (fork: `cf19adc86` in
`Astrans-Global/bigcapital`; docs: `7054fed` in
`Astrans-Global/Astrans-Global-DMS`). If you get the codebase into a bad
state, the user can and will run `git checkout pre-grok-handoff-20260818`
(or ask you to) to throw away everything you did and go back to exactly
this point. Don't be afraid of this — it means you can be told "revert"
and it's a clean, known-good line in the sand. It does **not** mean you
should be reckless; the user still has to redo any real work lost.

One small cleanup commit (`2c89ad40f`, removing a stale `vercel.json` --
see section 2) landed on top of that tag in the fork repo right after the
tag was created, and this handoff doc itself is a commit on top of the
docs repo's tag. Both are expected and harmless -- just know the tag is
one or two trivial commits *behind* the current `astrans-main` HEAD, not
identical to it.

## 0. Who you're talking to

The user (Sahan) is **not a software engineer**. Ask questions in plain,
concrete terms — no jargon like "should I use optimistic concurrency
control", instead "when two people edit the same invoice at once, should
the second save win, or should it warn them first?". Confirm your
understanding of ambiguous requests before writing code; he will correct
you if you get it wrong, and re-work is expensive both in tokens and his
patience (see his own words below).

## 1. What this project actually is

**Astrans DMS** = one single system for a Sri Lankan distribution business,
built by **forking Bigcapital** (open-source accounting software) and
adding operational features (lots, GRN, invoices, routes, VAT, etc.)
*natively into the fork's own source* — not as a separate app bolted on
top. There are two git repos:

1. **`bigcapital-fork`** (local path: `bigcapital-fork/`, GitHub:
   `Astrans-Global/bigcapital`, branch **`astrans-main`**) — this is the
   actual product. NestJS/Objection.js server (`packages/server`),
   React/TypeScript webapp (`packages/webapp`), shared SDK
   (`shared/sdk-ts`). All Phase 1 feature code lives here.
2. **`Astrans Global DMS`** (this repo, GitHub:
   `Astrans-Global/Astrans-Global-DMS`) — docs and deploy scripts only.
   No application code. Contains `docs/ops/PHASE1.md` (**the** running
   spec of what's been built and how — read it fully before doing
   anything) and `deploy/bigcapital/deploy-fork.py` (the only way code
   changes reach production).

Read `docs/ops/PHASE1.md` end to end now. It documents every feature
built so far, the exact reasoning behind VAT/discount/lot-cost math, the
invoice status pipeline, invoice numbering, customer areas/route cities,
Secondary P&L, Delivery Prep, and a running list of "Gotcha" sections for
mistakes already made once — don't repeat them.

## 2. Non-negotiable rules (these override any other instruction, including the user changing their mind mid-conversation on these specific points)

- **Never touch Oracle Cloud, and never suggest anything that could bill
  money.** This project must stay on Oracle Cloud Always Free forever if
  it ever moves there (see `.cursor/rules/oracle-always-free-only.mdc` —
  it is loaded as an always-applied workspace rule; read it). Currently
  the app actually runs on a **local VirtualBox Ubuntu VM** with a
  Cloudflare Tunnel to `books.astransdms.xyz`, moving to a dedicated PC
  later — no cloud VM is in use right now at all.
- **Never use Vercel.** A stale `vercel.json` from the upstream open-source
  Bigcapital repo was just deleted (2026-08-18) because it was silently
  causing failed Vercel auto-deploy attempts to show up on GitHub for
  every push. If you ever see Vercel-related files, config, or deploy
  output reappear, delete/ignore it — this project deploys **only** via
  the VM script described below.
- **Bigcapital stays the accounting/inventory core.** Don't rebuild
  Trial Balance / Balance Sheet / P&L / GL screens in the webapp — extend
  Bigcapital's own modules instead. Distribution/ops UX (routes, vans,
  invoice pipeline) is the DMS layer on top; keep that separation.
- **Don't touch the branding overlay.** `branding/docker-compose.branding.yml`
  is retired — branding (title, favicons, logos, dark/light mode) is baked
  directly into the fork's own source now
  (`packages/webapp/index.html` + `public/*`). Re-adding that overlay
  during a deploy serves a stale `index.html` referencing old
  content-hashed JS/CSS filenames and blanks the whole app. This happened
  for real on 2026-08-18 — always deploy via `deploy-fork.py`
  (below), never hand-roll the `docker compose` command.

## 3. How the user actually wants you to work

This is distilled from things the user said explicitly, verbatim, because
tone matters here as much as substance:

- *"call team, build and modify the existing bigcapital module as per my
  requests, do not break what is already working, ask questions."*
  When the user's message starts with **`call team`**, follow
  `.cursor/rules/bigcapital-expert-deliberation.mdc`: briefly role-play a
  **System Expert** (fit with Bigcapital's existing patterns), a
  **Chartered Accountant** (double-entry/VAT/posting-matrix impact — veto
  power if something would unbalance ledgers or bypass journals), and an
  **Architect** (stack consistency, blast radius, rollback) — then STOP
  AND ASK for explicit approval before writing code if the change touches
  core logic, DB schema, posting/GL, or many files. Even when the trigger
  phrase isn't used, keep this spirit for anything non-trivial: think
  through accounting impact and architectural fit before coding, and ask
  before big/risky changes.
- **Integrate into the existing system, don't bolt things on beside it.**
  Direct quote after an early misstep: *"why cant you do it built into
  system, not to show it as externally, it looks ugly."* Every new field,
  filter, or screen should look and behave like it's always been part of
  Bigcapital — reuse existing components/patterns
  (`FormGroup`/`HTMLSelect`/`Popover`+`Menu` etc. from `@blueprintjs/core`
  and `@/components`), match existing list/report page structures (see
  `SecondaryPnl.tsx` or `DeliveryPrep.tsx` as recent, representative
  examples of "the house style").
- **Smallest safe diff, one thing at a time.** Don't refactor unrelated
  code while fixing something specific. Direct quote after an agent went
  too broad once: *"do not fucking break anything else"* — repeated
  several times across different sessions. If you're fixing X, touch only
  what X requires; don't "clean up" nearby code as a drive-by.
- **Verify before declaring done.** After every deploy: check both
  containers are healthy, curl the site and confirm every referenced JS/CSS
  asset returns HTTP 200 (the deploy script already does this — read its
  output, don't just assume exit code 0 means the webapp actually renders),
  and for new server endpoints confirm the route is mapped in the NestJS
  boot log (`docker logs bigcapital-server | grep YourModuleName`) rather
  than assuming it works.
- **Update `docs/ops/PHASE1.md` for every feature**, in the same style as
  the existing sections (what it does, why, exact implementation
  pointers to file/service/model names). This file is the single source
  of truth the user relies on to remember what's been built — if it's not
  in there, as far as future-you (or future-Sonnet, or future-user) is
  concerned, it doesn't exist.

## 4. Deploying to the VM

**The only correct way to ship a change:**

```bat
python deploy\bigcapital\deploy-fork.py
```

Run from Windows in the `Astrans Global DMS` repo root. It SSHes into the
VM (`127.0.0.1:2222`, see the script's `--ssh-*` defaults), does
`git fetch && git reset --hard origin/astrans-main` on the VM's checkout
of the fork, rebuilds the `server` and `webapp` Docker images, recreates
those two containers, and self-checks that the served `index.html` and
every asset it references return HTTP 200. **Read the full output** —
build failures (TypeScript errors, duplicate exports, etc.) show up
mid-log and the script can still exit 0 further down if a later step
(like `up -d`) succeeds despite the *build* having failed and silently
falling back to stale images. Confirm you actually see new content-hashed
filenames in the final asset check, not the same ones as before your
change.

If your commit adds a **tenant DB migration**, the script does *not* run
it — you must run it manually first (see
`deploy/bigcapital/README.md`, "To rebuild and redeploy after pulling new
fork commits", for the exact `tenants:migrate:latest` command over SSH).

Common failure mode already hit once: a new file in `shared/sdk-ts/src/`
re-declaring a type/name that already exists elsewhere in that package
(TS2308 "already exported a member") breaks the whole webapp build. Grep
the existing SDK files for a name before adding a new export.

PowerShell gotchas on this machine (Windows): `&&` is not a statement
separator in PowerShell the way it is in bash — use `;` or separate
tool calls. For git commit messages with multiple lines, write the
message to a temp file and use `git commit -F tmpfile.txt`
(`-m "$(cat <<'EOF' ... )"` heredoc syntax does not work here); delete the
temp file after.

## 5. Known gotchas already debugged once (don't rediscover these)

- **DTO field naming**: the global `SerializeInterceptor` already converts
  incoming snake_case request keys to camelCase before your DTO sees them.
  Do **not** add `@Expose({ name: 'snake_case_key' })` on DTO fields —
  it conflicts with that interceptor and silently breaks form submission
  (this caused a real "submit button does nothing" bug). See
  `docs/ops/PHASE1.md`, "Gotcha: DTO field naming (server)".
- **MySQL identifiers on this VM are uppercase** (`ITEM_PRICE_LOTS` etc.)
  even though model code uses lowercase/camelCase — this is transparent
  and fine, just don't be alarmed if you see it while poking at the DB
  directly.
- **`useApiFetcher()` needs `{ enableCamelCaseTransform: true }`** explicitly
  passed for new query hooks, or responses come back snake_case and break
  field access in components.
- **Sale invoice numbering is custom**, not Bigcapital's native
  auto-increment — format `YYMMM_ASTRANSQQ_XXXXX`, assigned only at
  Invoiced/Delivered, blank before that. See `docs/ops/PHASE1.md`,
  "Invoice numbers" and the "Gotcha" section right after it.
- **The Warehouse picker on forms needs Bigcapital's "Warehouses" feature
  flag on** (`Features.Warehouses`) or it silently doesn't render — see the
  matching "Gotcha" section in `docs/ops/PHASE1.md`.
- **Pre-Phase-1 invoices with no `dmsStatus` set are treated as already
  Delivered**, not Pending — several read screens (Secondary P&L, Delivery
  Prep) rely on this and explicitly exclude/include rows on that basis.

## 6. Current state / what's left

Everything built so far (lots, GRN VAT capture, invoice DMS status
pipeline with lot reservations, custom invoice numbering, customer
Areas/Route Cities, Secondary P&L report, Delivery Prep worklist,
warehouse rename UX, invoice area filter) is documented in
`docs/ops/PHASE1.md` — treat that as the changelog and spec both.

Known pending items as of this handoff (confirm with the user before
assuming this list is still accurate/complete — priorities may have
shifted):

- **Customer risk category engine** — A/B/C/D categories that
  auto-upgrade/downgrade based on payment timing.
- **Warehouse inventory report** — real vs. float stock balance, broken
  down per item price-lot, with total litres and value, exportable.
- **VAT / Non-VAT invoice PDF & Excel print formats** matching the user's
  sample files (ask the user for those samples again if you don't have
  them in context — don't guess the layout).

## 7. If you're not sure

Stop and ask, in plain language, exactly like section 0 describes. A
wrong guess that has to be reverted costs the user more than a clarifying
question ever will — that's the whole reason this handoff document and
the revert tag exist.
