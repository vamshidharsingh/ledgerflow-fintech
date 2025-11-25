from app.workflows import execute, rows, update
from app.repository import Repository
from app.errors import AppError, Conflict, Forbidden, NotFound
from tests.helpers import DatabaseCase

class WorkflowTests(DatabaseCase):

    def transfer(self, amount=5000, key='test-key'):
        return execute(self.conn, 'transfer', dict(source_id='account-1', target_id='account-2', amount_cents=amount, key=key))

    def test_double_entry_and_total_conservation(self):
        before = sum((r['balance_cents'] for r in rows(self.conn, 'accounts')))
        event = self.transfer()
        ledger = rows(self.conn, 'ledger_entries')
        self.assertEqual(sum((r['balance_cents'] for r in rows(self.conn, 'accounts'))), before)
        self.assertEqual(sum((r['signed_cents'] for r in ledger)), 0)
        self.assertEqual(len(ledger), 2)
        self.assertTrue(all((r['transfer_id'] == event['id'] for r in ledger)))

    def test_retry_returns_same_result(self):
        first = self.transfer()
        second = self.transfer()
        self.assertEqual(first['id'], second['id'])
        self.assertEqual(len(rows(self.conn, 'ledger_entries')), 2)

    def test_changed_retry_conflicts(self):
        self.transfer()
        with self.assertRaises(Conflict):
            self.transfer(6000)

    def test_insufficient_funds_rolls_back(self):
        before = rows(self.conn, 'accounts')
        with self.assertRaises(Conflict):
            self.transfer(999999999)
        self.assertEqual(before, rows(self.conn, 'accounts'))
        self.assertEqual(rows(self.conn, 'ledger_entries'), [])

    def test_cross_currency_rejected(self):
        target = Repository(self.conn, 'accounts').get('account-2')
        update(self.conn, 'accounts', target, currency='EUR')
        with self.assertRaises(AppError):
            self.transfer()

    def test_frozen_account_rejected(self):
        source = Repository(self.conn, 'accounts').get('account-1')
        update(self.conn, 'accounts', source, status='frozen')
        with self.assertRaises(Conflict):
            self.transfer()

    def test_same_account_rejected(self):
        with self.assertRaises(AppError):
            execute(self.conn, 'transfer', dict(source_id='account-1', target_id='account-1', amount_cents=1, key='same'))

    def test_deposit_is_simulated_and_idempotent(self):
        payload = dict(account_id='account-1', amount_cents=100, reference='cash-demo')
        before = Repository(self.conn, 'accounts').get('account-1')['balance_cents']
        execute(self.conn, 'deposit', payload)
        execute(self.conn, 'deposit', payload)
        self.assertEqual(Repository(self.conn, 'accounts').get('account-1')['balance_cents'], before + 100)

    def test_deposit_changed_reference_rejected(self):
        execute(self.conn, 'deposit', dict(account_id='account-1', amount_cents=100, reference='cash-demo'))
        with self.assertRaises(Conflict):
            execute(self.conn, 'deposit', dict(account_id='account-1', amount_cents=200, reference='cash-demo'))

    def test_zero_negative_float_and_bool_rejected(self):
        for value in (0, -1, 1.5, True):
            with self.assertRaises(AppError):
                self.transfer(value)

    def test_new_wallet_starts_at_zero(self):
        account = execute(self.conn, 'open_account', dict(customer_id='customer-1', name='New wallet', currency='EUR'))
        self.assertEqual(account['balance_cents'], 0)
        self.assertEqual(account['currency'], 'EUR')

    def test_freeze_workflow_blocks_transfer(self):
        execute(self.conn, 'set_account_status', dict(account_id='account-1', status='frozen'))
        with self.assertRaises(Conflict):
            self.transfer()
