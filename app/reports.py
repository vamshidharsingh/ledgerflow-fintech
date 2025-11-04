from .workflows import rows
from .schema import all_schemas
from .repository import Repository

def dashboard(conn):
    counts = {name: Repository(conn, name).count() for name in all_schemas()}
    accounts = rows(conn, 'accounts')
    expenses = rows(conn, 'expenses')
    budgets = rows(conn, 'budgets')
    totals = {currency: sum((r['balance_cents'] for r in accounts if r['currency'] == currency)) for currency in sorted({r['currency'] for r in accounts})}
    utilization = [dict(label=b['month'] + ' / ' + b['category_id'], value=sum((e['amount_cents'] for e in expenses if e['category_id'] == b['category_id'] and e['date'][:7] == b['month'] and (next((a['customer_id'] for a in accounts if a['id'] == e['account_id']), None) == b['customer_id']))), target=b['limit_cents']) for b in budgets]
    ledger = rows(conn, 'ledger_entries')
    return dict(counts=counts, metrics=[dict(label='Wallet balances (cents)', value=totals), dict(label='Completed transfers', value=counts['transfers']), dict(label='Ledger net (cents)', value=sum((r['signed_cents'] for r in ledger))), dict(label='Open risk alerts', value=sum((r['status'] == 'open' for r in rows(conn, 'risk_alerts'))))], bars=utilization)
