from athena.cli.commands.base import BaseCommand
from athena.cli.commands import ManageDbBootCommand
from athena.exceptions.base import BaseException
from athena.logger import logger, setup_cli as setup_logger
from athena.utils import root_path

class Cli(object):

    default_command = 'default'

    def __init__(self, parser, subparser, commands=None):
        self.parser = parser
        self.subparser = subparser
        self.commands = commands or {}
        self.args = {}

    def run(self):
        # run the first command
        logger().debug('Attempting to run...')

        args = self.parser.parse_args()
        # get rid of namespace object
        self.args = dict(vars(args))
        logger().debug('Setting up logger...')
        setup_logger(root_path('athena.log'))

        self.boot_manager()

        try:
            if 'command' not in self.args:
                result = self.run_default(self.args)
            elif self.has_command(self.args['command']):
                result = self.run_command(self.args['command'], self.args)
            else:
                print("Command '{}' not found!".format(self.args['command']))
                self.parser.print_help()
                return 1
        except BaseException as e:
            print('[!] An Exception occurred while running a command!')
            raise e

        # allow commands to trigger other commands
        while True:
            if isinstance(result, BaseCommand):
                try:
                    result = self.call_command(result)
                except BaseException as e:
                    print('[!] An Exception occurred while running a command!')
                    raise e
            if not isinstance(result, BaseCommand):
                break

        # return the result of the last command
        return result

    def boot_manager(self):
        boot_command = ManageDbBootCommand.make(self.args)
        boot_command.run()

    def boot_project(self):
        pass

    # make the command instance and call it
    def run_command(self, name, args):
        command_cls = self.commands[name]
        command = command_cls.make(args)
        return self.call_comamnd(command)

    def call_comamnd(self, command):
        # call the instance of a command
        return command.run()

    # run the default command, handle non registered commands
    def run_default(self, args):
        if self.has_default_command():
            return self.run_command(self.default_command, args)
        print("No default command registered!")
        self.parser.print_help()
        return 0

    def register(self, name, command):
        command_parser = self.subparser.add_parser(name)
        command.configure_parser(command_parser)
        self.commands[name] = command

    # helpers
    def get_default_command(self):
        return self.commands[self.default_command]

    def has_command(self, name):
        if name not in self.commands.keys():
            return False
        return True

    def has_default_command(self):
        if self.has_args():
            return self.default_command in self.commands.keys()
        return False

    def has_args(self):
        return self.args is not {}
