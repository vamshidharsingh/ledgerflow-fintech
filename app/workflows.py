"""Transactional domain commands. Generic CRUD never writes derived state."""
import uuid
from datetime import date, datetime, timezone
from .repository import Repository
from .db import transaction
from .errors import AppError, Conflict, Forbidden

def rows(conn, name):
    repo = Repository(conn, name)
    return [repo.get(r['id']) for r in conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (name,))]

def find(conn, name, **criteria):
    return next((r for r in rows(conn, name) if all((r.get(k) == v for k, v in criteria.items()))), None)

def update(conn, name, row, **changes):
    data = {k: v for k, v in row.items() if k not in ('id', '_version')}
    data.update(changes)
    return Repository(conn, name).update(row['id'], data, row['_version'])

def positive(value, name='quantity'):
    if type(value) is not int or not 0 < value <= 10 ** 12:
        raise AppError(name + ' must be a positive integer')
    return value

def text(value, name):
    if not isinstance(value, str) or not value.strip() or len(value) > 200:
        raise AppError(name + ' must be non-empty text (max 200)')
    return value

def execute(conn, action, data):
    if not isinstance(data, dict):
        raise AppError('JSON object required')
    if action not in ACTIONS:
        raise AppError('Unknown workflow')
    with transaction(conn):
        try:
            return ACTIONS[action](conn, data)
        except KeyError as exc:
            raise AppError('Missing workflow field: ' + str(exc.args[0]))

def transfer(conn, data):
    source_id = text(data['source_id'], 'source_id')
    target_id = text(data['target_id'], 'target_id')
    amount = positive(data['amount_cents'], 'amount_cents')
    key = text(data['key'], 'key')
    prior = find(conn, 'transfers', key=key)
    if prior:
        if (prior['source_id'], prior['target_id'], prior['amount_cents']) != (source_id, target_id, amount):
            raise Conflict('Idempotency key reused with different transfer')
        return prior
    if source_id == target_id:
        raise AppError('Source and target must differ')
    source = Repository(conn, 'accounts').get(source_id)
    target = Repository(conn, 'accounts').get(target_id)
    if source['currency'] != target['currency']:
        raise AppError('Cross-currency transfers are not supported')
    if source['status'] != 'active' or target['status'] != 'active':
        raise Conflict('Both accounts must be active')
    if source['balance_cents'] < amount:
        raise Conflict('Insufficient funds')
    movement = Repository(conn, 'transfers').create(dict(source_id=source_id, target_id=target_id, amount_cents=amount, key=key, status='completed'))
    update(conn, 'accounts', source, balance_cents=source['balance_cents'] - amount)
    update(conn, 'accounts', target, balance_cents=target['balance_cents'] + amount)
    for account, sign in ((source_id, -1), (target_id, 1)):
        Repository(conn, 'ledger_entries').create(dict(account_id=account, transfer_id=movement['id'], signed_cents=sign * amount, memo='Internal wallet transfer'))
    return movement

def deposit(conn, data):
    account_id = text(data['account_id'], 'account_id')
    amount = positive(data['amount_cents'], 'amount_cents')
    reference = text(data['reference'], 'reference')
    prior = find(conn, 'deposits', reference=reference)
    if prior:
        if (prior['account_id'], prior['amount_cents']) != (account_id, amount):
            raise Conflict('Reference reused with different deposit')
        return prior
    account = Repository(conn, 'accounts').get(account_id)
    if account['status'] != 'active':
        raise Conflict('Account is frozen')
    event = Repository(conn, 'deposits').create(dict(account_id=account_id, amount_cents=amount, reference=reference))
    update(conn, 'accounts', account, balance_cents=account['balance_cents'] + amount)
    return event
ACTIONS = {'transfer': transfer, 'deposit': deposit}

def open_account(conn, data):
    customer_id = text(data['customer_id'], 'customer_id')
    name = text(data['name'], 'name')
    currency = text(data['currency'], 'currency')
    return Repository(conn, 'accounts').create(dict(customer_id=customer_id, name=name, currency=currency, balance_cents=0, status='active'))

def set_account_status(conn, data):
    account = Repository(conn, 'accounts').get(text(data['account_id'], 'account_id'))
    status = text(data['status'], 'status')
    if status not in ('active', 'frozen'):
        raise AppError('Invalid account status')
    return update(conn, 'accounts', account, status=status)
ACTIONS.update(open_account=open_account, set_account_status=set_account_status)
