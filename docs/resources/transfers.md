# Transfers

Idempotent wallet-to-wallet movements with a request fingerprint.

| Field | Type | Constraint |
| --- | --- | --- |
| `source_id` | string | Reference to `accounts` |
| `target_id` | string | Reference to `accounts` |
| `amount_cents` | integer | Required |
| `key` | string | Required |
| `status` | string | completed |

Read endpoint: `GET /api/resources/transfers`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["key"]`.
Fixture file: `fixtures/transfers.json`. Repository exact-match helper: `find_by_source_id`.
Test module: `tests/test_transfers.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
