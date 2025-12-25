"""Reference-only integer exchange quotes in millionths; transfers remain same-currency."""
from app.repository import Repository

class ResourceRepository(Repository):
    resource = 'exchange_rates'

    def find_by_base(self, value):
        """Return exact matches, independent of the paginated UI listing."""
        rows = self.conn.execute('SELECT id FROM records WHERE resource=? ORDER BY id', (self.resource,))
        return [item for row in rows if (item := self.get(row['id']))['base'] == value]
