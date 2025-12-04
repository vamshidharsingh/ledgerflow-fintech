"""Currency-specific wallets. Balances change only through transfers or simulated deposits."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'accounts'

    def find_by_customer_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['customer_id'] == value]
