"""Idempotent wallet-to-wallet movements with a request fingerprint."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'transfers'

    def find_by_source_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['source_id'] == value]
