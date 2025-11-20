from concurrent.futures import ThreadPoolExecutor
import threading
from app.db import connect
from app.workflows import execute, rows, update
from app.repository import Repository
from app.errors import Conflict
from tests.helpers import DatabaseCase

class ConcurrencyTests(DatabaseCase):

    def run_parallel(self, tasks):
        barrier = threading.Barrier(len(tasks))

        def worker(task):
            conn = connect(self.db_path)
            try:
                barrier.wait(timeout=5)
                try:
                    execute(conn, task[0], task[1])
                    return 'ok'
                except Conflict:
                    return 'conflict'
            finally:
                conn.close()
        with ThreadPoolExecutor(max_workers=len(tasks)) as pool:
            return list(pool.map(worker, tasks))

    def test_concurrent_commands_preserve_domain_invariant(self):
        source = Repository(self.conn, 'accounts').get('account-1')
        update(self.conn, 'accounts', source, balance_cents=10)
        tasks = [('transfer', dict(source_id='account-1', target_id='account-2', amount_cents=6, key='concurrent-' + str(i))) for i in range(2)]
        outcomes = self.run_parallel(tasks)
        self.assertEqual(outcomes.count('ok'), 1)
        self.assertEqual(Repository(self.conn, 'accounts').get('account-1')['balance_cents'], 4)
