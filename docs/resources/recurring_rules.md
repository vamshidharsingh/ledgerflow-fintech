# Recurring Rules

Standing payment planning metadata; no scheduler executes these rules.

| Field | Type | Constraint |
| --- | --- | --- |
| `account_id` | string | Reference to `accounts` |
| `name` | string | Required |
| `amount_cents` | integer | Required |
| `frequency` | string | weekly, monthly |

Read endpoint: `GET /api/resources/recurring_rules`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/recurring_rules.json`. Repository exact-match helper: `find_by_account_id`.
Test module: `tests/test_recurring_rules.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
