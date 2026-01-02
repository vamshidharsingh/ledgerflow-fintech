# Ledger Entries

Signed double-entry records created atomically with a transfer.

| Field | Type | Constraint |
| --- | --- | --- |
| `account_id` | string | Reference to `accounts` |
| `transfer_id` | string | Reference to `transfers` |
| `signed_cents` | integer | Required |
| `memo` | string | Required |

Read endpoint: `GET /api/resources/ledger_entries`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/ledger_entries.json`. Repository exact-match helper: `find_by_account_id`.
Test module: `tests/test_ledger_entries.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
