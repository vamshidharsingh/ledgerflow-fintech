# Deposits

Simulated cash-in events, never real payment settlement.

| Field | Type | Constraint |
| --- | --- | --- |
| `account_id` | string | Reference to `accounts` |
| `amount_cents` | integer | Required |
| `reference` | string | Required |

Read endpoint: `GET /api/resources/deposits`. A local operator bearer token is required.
This resource is read-only through the generic HTTP API. Use the documented business workflows so derived state remains consistent.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["reference"]`.
Fixture file: `fixtures/deposits.json`. Repository exact-match helper: `find_by_account_id`.
Test module: `tests/test_deposits.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
