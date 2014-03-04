import logging
import sqlite3
import os.path
import time

from itertools import groupby
from functools import reduce

from reminisc.core.processing.commands import NewMessage
from datetime import datetime

logger = logging.getLogger(__name__)

source = 'Gajim'

# In sqlite3, autoincrement primary index is guaranteed to be monotonically increasing
# and that the selected row id has never been used in the same table before.
# This allows us to sort by log_line_id instead of time, which is significantly faster.
#
# Only kinds (3, 4, 5, 6) are interesting now - they represent received end sent single
# and chat messages.
query_messages = """select
        log_line_id,
        subject,
        message,
        time,
        kind,
        re.name as contact_name,
        j.jid as contact_jid,
        aj.jid as account_jid
    from logs

    left join jids as j on logs.jid_id = j.jid_id
    left join roster_entry as re on logs.jid_id = re.jid_id
    join jids as aj on re.account_jid_id = aj.jid_id

    where log_line_id > :last_id
    and kind in (3, 4, 5, 6)
    order by log_line_id
    limit :batch_size
"""


class IterativeImporter(object):
    def __init__(self, module_config, dbconfig, command_queue):
        self.module_config = module_config
        self.command_queue = command_queue
        self.dbconfig = dbconfig

    def start(self):
        database_path = self.module_config.get('gajim', 'database_file')

        # in case path uses '~'
        database_path = os.path.expanduser(database_path)

        self.conn = sqlite3.connect(database_path)
        self.conn.row_factory = sqlite3.Row

        self.dbconfig.connect()

        # will sleep that long between consecutive queries to logs
        polling_interval = float(self.module_config.get('history', 'polling_interval', fallback=1))

        while True:
            logger.debug("Importing next batch.")
            self.__import_next_batch()
            time.sleep(polling_interval)

    def __import_next_batch(self):
        try:
            last_id = self.dbconfig.get('last_message_processed_id')
        except KeyError:
            last_id = 0

        statement = self.conn.execute(query_messages, {'last_id': last_id, 'batch_size': 1000})
        rows = statement.fetchall()

        # map rows into commands
        groups = groupby(rows, lambda r: r['log_line_id'])

        for group in groups:
            lg = list(group[1])
            account_handles = [r['account_jid'] for r in lg]

            row = lg[0]
            self.__create_command(row, account_handles)

        if len(rows) > 0:
            new_last_id = rows[-1]['log_line_id']
            self.dbconfig.save('last_message_processed_id', new_last_id)


    def __create_command(self, row, account_handles):
        additional_arguments = {
            'contact_name': row['contact_name'],
            'protocol': 'XMPP',
        }

        direction = NewMessage.Direction.RECEIVED if row['kind'] in (3, 4) else NewMessage.Direction.SENT

        cmd = NewMessage(
            source=source,
            account_ids=account_handles,
            contact_id=row['contact_jid'],
            datetime=datetime.fromtimestamp(row['time']),
            message=row['message'],
            direction=direction,
            **additional_arguments)

        self.command_queue.put(cmd)
