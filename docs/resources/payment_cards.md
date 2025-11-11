# Payment Cards

Masked card reference metadata. Full card numbers are never stored.

| Field | Type | Constraint |
| --- | --- | --- |
| `account_id` | string | Reference to `accounts` |
| `label` | string | Required |
| `last_four` | string | Required |
| `status` | string | active, locked |

Read endpoint: `GET /api/resources/payment_cards`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/payment_cards.json`. Repository exact-match helper: `find_by_account_id`.
Test module: `tests/test_payment_cards.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
