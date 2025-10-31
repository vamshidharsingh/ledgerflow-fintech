# Invoices

Manual payable and receivable records.

| Field | Type | Constraint |
| --- | --- | --- |
| `customer_id` | string | Reference to `customers` |
| `number` | string | Required |
| `amount_cents` | integer | Required |
| `status` | string | draft, sent, paid |
| `due_date` | string | date |

Read endpoint: `GET /api/resources/invoices`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `["number"]`.
Fixture file: `fixtures/invoices.json`. Repository exact-match helper: `find_by_customer_id`.
Test module: `tests/test_invoices.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
