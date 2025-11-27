"""Configurable risk thresholds for manual analyst review."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'risk_rules'

    def find_by_name(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['name'] == value]
