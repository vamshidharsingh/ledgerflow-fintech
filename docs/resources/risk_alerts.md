# Risk Alerts

Human-entered review cases; no machine-learning fraud claims.

| Field | Type | Constraint |
| --- | --- | --- |
| `account_id` | string | Reference to `accounts` |
| `reason` | string | Required |
| `severity` | string | low, medium, high |
| `status` | string | open, resolved |

Read endpoint: `GET /api/resources/risk_alerts`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/risk_alerts.json`. Repository exact-match helper: `find_by_account_id`.
Test module: `tests/test_risk_alerts.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
