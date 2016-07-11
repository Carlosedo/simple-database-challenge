import sys


class SimpleDatabase(object):
    """A simple database"""

    def __init__(self):
        self.db_state = {}
        self.num_equal_to = {}

    def _unknown_command(self, *command):
        print "Unknown command"

    def _decrease_previous_numequalto_count(self, name):
        previous_value = self.db_state.get(name, None)
        if previous_value:
            self.num_equal_to[previous_value] -= 1

    def _increase_numequalto_count(self, value):
        self.num_equal_to[value] = self.num_equal_to.get(value, 0) + 1

    def set(self, name, value):
        self._decrease_previous_numequalto_count(name)
        self._increase_numequalto_count(value)
        self.db_state[name] = value

    def get(self, name):
        print self.db_state.get(name, 'NULL')

    def unset(self, name):
        self._decrease_previous_numequalto_count(name)
        self.db_state.pop(name, None)

    def numequalto(self, name):
        print self.num_equal_to.get(name, 0)


    def read_command(self, user_input):
        command = user_input.split(' ')

        command_call = getattr(self, command[0].lower(), self._unknown_command)
        command_call(*command[1:])



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
