from pkg_resources import resource_filename

import sys

from trac.core import *
from trac.ticket import Ticket
from trac.util.text import printout, to_unicode
from trac.admin import IAdminCommandProvider

class TicketAdmin(Component):

    implements(IAdminCommandProvider)

    # IAdminCommandProvider methods
    def get_admin_commands(self):
        """Return a list of available admin commands."""

        yield('ticket_comment add', '[ticket id] [comment]', 'Adds a comment to a ticket.', None, self._add_comment)
        yield('ticket_resolve', '[ticket_id] [resolution] [user] [comment]', 'Resolve a ticket with an optional comment.', None, self._resolve)

    def _add_comment(self, ticket_id, user, comment):
        """Add a comment to a ticket"""

        try:
            ticket = Ticket(self.env, ticket_id)
            self._save_ticket(ticket, user, comment)
            printout('Added comment to ticket %s' % ticket_id)
        except:
            # if no such ticket then add comment.
            printout('Unable to add comment.')
        
    def _resolve(self, ticket_id, resolution=None, user=None, comment=None):
        """Resolve a ticket and add an optional comment"""

        try:
            resolutions = self._get_resolutions()
            if resolution not in resolutions:
                printout('invalid resolution')
                return

            ticket = Ticket(self.env, ticket_id)
            ticket['status'] = 'closed'
            ticket['resolution'] = resolution

            self._save_ticket(ticket, user, comment)
            printout('Resolved ticket %s using resolution %s' % (ticket_id, resolution))
        except Exception, e:
            printout('Failed to modify ticket. Reason: %s' % e)

    def _save_ticket(self, ticket, user=None, comment=None):
        #todo convert email to trac user when possible

        if comment is not None:
            comment = to_unicode(comment.decode("string-escape"))

        ticket.save_changes(user, comment)
        # todo add a ticket change entry 

    def _get_resolutions(self):
        """return the possible resolutions"""

        db = self.env.get_read_db()
        cursor = db.cursor()
        cursor.execute("SELECT name FROM enum WHERE type='resolution'")
        return set([str(x) for x, in cursor.fetchall()])
