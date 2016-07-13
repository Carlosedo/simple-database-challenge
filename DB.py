import sys


class SimpleDatabase(object):
    """A simple database"""

    def __init__(self):
        self.db_state = {}
        self.db_transactions = []
        self.num_equal_to = {}

    def _unknown_command(self):
        print "UNKNOWN COMMAND"

    def _save_data_to_transaction(self, record, table, table_name):
        # if there is an active transaction, we have to save the previous value
        if self.db_transactions:
            # we only have to save the original value, only the first time it is changed
            if record not in self.db_transactions[-1][table_name]:
                # if the value was not in the database, we save a None in order to delete it later
                self.db_transactions[-1][table_name][record] = table.get(record, None)

    def _decrease_previous_numequalto_count(self, name):
        previous_db_value = self.db_state.get(name, None)
        if previous_db_value:
            self._save_data_to_transaction(previous_db_value, self.num_equal_to, 'num_equal_to')
            self.num_equal_to[previous_db_value] -= 1

    def _increase_numequalto_count(self, value):
        self._save_data_to_transaction(value, self.num_equal_to, 'num_equal_to')
        self.num_equal_to[value] = self.num_equal_to.get(value, 0) + 1

    def set(self, name, value):
        self._decrease_previous_numequalto_count(name)
        self._increase_numequalto_count(value)
        self._save_data_to_transaction(name, self.db_state, 'db_state')
        self.db_state[name] = value

    def get(self, name):
        print self.db_state.get(name, 'NULL')

    def unset(self, name):
        self._decrease_previous_numequalto_count(name)
        self._save_data_to_transaction(name, self.db_state, 'db_state')
        self.db_state.pop(name, None)

    def numequalto(self, name):
        print self.num_equal_to.get(name, 0)

    def begin(self):
        # appends a new transaction object
        self.db_transactions.append({
            'db_state': {},
            'num_equal_to': {}
        })

    def commit(self):
        # deletes all the transactions, all the changes are permanently applied
        if self.db_transactions:
            self.db_transactions = []
        else:
            print 'NO TRANSACTION'

    def rollback(self):
        # returns the database to where it was before the last BEGIN, only if there is a transaction
        if self.db_transactions:
            for name, value in self.db_transactions[-1]['db_state'].iteritems():
                # a record saved with None as value means it wasn't present before so I delete it
                if value:
                    self.db_state[name] = value
                else:
                    self.db_state.pop(name)

            for name, value in self.db_transactions[-1]['num_equal_to'].iteritems():
                if value:
                    self.num_equal_to[name] = value
                else:
                    self.num_equal_to.pop(name)

            # the previous code is repeated two times, but taking it into a function won't save much
            # and would affect legibility

            self.db_transactions.pop()
        else:
            print 'NO TRANSACTION'

    def read_command(self, user_input):
        command = user_input.split(' ')
        command_call = getattr(self, command[0].lower(), self._unknown_command)

        try:
            command_call(*command[1:])
        except TypeError:
            print 'WRONG SYNTAX'


if __name__ == "__main__":
    database = SimpleDatabase()

    if len(sys.argv) > 1:
        with open(sys.argv[1]) as command_file:
            for line in command_file:
                if line == 'END':
                    break
                else:
                    database.read_command(line.strip())
    else:
        while True:
            db_input = raw_input()

            if db_input == 'END':
                break
            else:
                database.read_command(db_input.strip())
