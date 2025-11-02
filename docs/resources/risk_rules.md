# Risk Rules

Configurable risk thresholds for manual analyst review.

| Field | Type | Constraint |
| --- | --- | --- |
| `name` | string | Required |
| `threshold_cents` | integer | Required |
| `severity` | string | low, medium, high |

Read endpoint: `GET /api/resources/risk_rules`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/risk_rules.json`. Repository exact-match helper: `find_by_name`.
Test module: `tests/test_risk_rules.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
