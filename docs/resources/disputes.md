# Disputes

Support dispute tracking without payment-network integration.

| Field | Type | Constraint |
| --- | --- | --- |
| `customer_id` | string | Reference to `customers` |
| `subject` | string | Required |
| `amount_cents` | integer | Required |
| `status` | string | open, closed |

Read endpoint: `GET /api/resources/disputes`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/disputes.json`. Repository exact-match helper: `find_by_customer_id`.
Test module: `tests/test_disputes.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
