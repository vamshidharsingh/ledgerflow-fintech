# LedgerFlow — Fintech Operations Workspace

Trace every cent. Reconcile every movement.

A runnable local portfolio project. Python serves a framework-free REST API, SQLite stores validated domain records, and a responsive JavaScript interface exposes dashboards, resource management, business workflows and CSV exports.

## What you can demonstrate

- **Transfer between wallets**: `transfer` with `{"source_id": "account-1", "target_id": "account-2", "amount_cents": 2500, "key": "transfer-demo-1"}`.
- **Simulate a deposit**: `deposit` with `{"account_id": "account-1", "amount_cents": 10000, "reference": "deposit-demo-1"}`.
- **Open a zero-balance wallet**: `open_account` with `{"customer_id": "customer-1", "name": "Travel wallet", "currency": "EUR"}`.
- **Freeze or activate a wallet**: `set_account_status` with `{"account_id": "account-1", "status": "frozen"}`.

All 20 resource types have documented schemas, deterministic fixtures, exact-match repositories and contract tests. Generic resource CRUD supports optimistic versions and foreign-key checks. Business commands use one SQLite transaction to enforce domain invariants and record changes atomically.

## Run in two commands

Install Python 3.12 or newer. No third-party runtime packages are needed.

```bash
cd ledgerflow-fintech
python -B -m app
```

Open **http://127.0.0.1:8011**. Select **Access token**, enter `demo-local-token`, and press **Connect**. All first-run records are synthetic. The application seeds an empty database once and preserves later edits between restarts.

Windows: use `py -3 -B -m app` if `python` is unavailable. Run commands inside the project folder, not inside `app/`.

## Verify

```bash
python -B -m unittest discover -s tests -v
python -B scripts/smoke_test.py
python -B scripts/verify_files.py
```

The unit suite covers resource contracts, invalid data, foreign-key constraints, optimistic concurrency, atomic rollback, access control and domain behavior. A separate concurrency test uses independent connections racing against the same database. The HTTP smoke script starts a temporary server and checks all 20 resource routes. `verify_files.py` checks exact inventory and SHA-256 integrity. Test outputs are captured in the bundle's `VERIFICATION.md`.

## Architecture

| Layer | Responsibility |
| --- | --- |
| `web/` | Accessible static operator interface, resource forms, charts and workflow forms |
| `app/http.py` | Token-protected routes, bounded JSON requests and safe static files |
| `app/workflows.py` | Atomic domain operations and retry rules |
| `app/repositories/` | Resource-specific exact-match queries on a common repository |
| `schemas/` | Required fields, types, formats, unique tuples and reference targets |
| `fixtures/` | Explicitly fictional, dependency-ordered starting data |
| `tests/` | Real persistence, HTTP and concurrent command tests |
| `docs/` | Setup, API, architecture, security and 20 resource guides |

SQLite uses a compact generic record table with JSON payloads, rather than claiming a normalized enterprise database. Schemas are enforced by the application; direct SQL writes bypass them. `BEGIN IMMEDIATE` serializes writes, and versions protect operator edits from stale data.

## Scope

Local finance sandbox. No bank integration, real payments, KYC, currency conversion or scheduled execution. Wallet transfers use integer cents and paired ledger entries; simulated deposits are recorded separately. Manual expenses do not change wallet balances.

This bundle does not claim deployment, independent past contributions, benchmark results or professional experience. Customize the code and explain the tests before presenting it as portfolio work.

## Configuration and operations

Set environment variables listed in `.env.example` before launch. The file is an example and is **not automatically loaded**. The default server binds only to loopback. `APP_DB` chooses a persistent local database path. `APP_TOKEN` controls one local operator credential.

```bash
python -B scripts/export_data.py customers runtime/export.csv
python -B scripts/backup.py runtime/backup.sqlite3
```

Reset only a disposable demo: stop the application and remove its `runtime/` database directory, then restart. This deletes your local edits. Container setup is optional and documented in [docs/setup.md](docs/setup.md). Container execution was not tested in the delivery environment.

## File inventory

20 schema files + 20 fixtures + 20 repository modules + 20 resource tests + 20 resource guides + 60 application, UI, infrastructure, script, test and documentation files = **160 files**.

`PROJECT_MANIFEST.json` includes every delivered path and hashes for the other 159 files. Its own hash is null to avoid self-reference. Generated databases, Python caches, virtual environments and Git metadata are not source files and are not included in the ZIP.

## License

MIT. See [LICENSE](LICENSE). The username is the requested portfolio destination; no GitHub account access or publication is performed by this archive.
