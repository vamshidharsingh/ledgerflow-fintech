"""Standing payment planning metadata; no scheduler executes these rules."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'recurring_rules'

    def find_by_account_id(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['account_id'] == value]
