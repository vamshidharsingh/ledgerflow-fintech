# Reconciliation Batches

Manual reconciliation checkpoints for imported statements.

| Field | Type | Constraint |
| --- | --- | --- |
| `name` | string | Required |
| `expected_cents` | integer | Required |
| `observed_cents` | integer | Required |
| `status` | string | pending, reviewed |

Read endpoint: `GET /api/resources/reconciliation_batches`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/reconciliation_batches.json`. Repository exact-match helper: `find_by_name`.
Test module: `tests/test_reconciliation_batches.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
