# Notifications

Local inbox records, never actual email or SMS.

| Field | Type | Constraint |
| --- | --- | --- |
| `customer_id` | string | Reference to `customers` |
| `message` | string | Required |
| `status` | string | unread, read |

Read endpoint: `GET /api/resources/notifications`. A local operator bearer token is required.
Create, update and delete are supported by the operator resource API. PUT is a full replacement and requires `_version`; deletes require a version query parameter.

Foreign keys are checked before writes; referenced records cannot be deleted. Unique constraints: `[]`.
Fixture file: `fixtures/notifications.json`. Repository exact-match helper: `find_by_customer_id`.
Test module: `tests/test_notifications.py` checks persistence, validation, duplicate rollback and fixture compatibility.
Every fixture is synthetic and is safe to reset in a disposable local database.
