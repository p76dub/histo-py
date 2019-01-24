# -*- coding: utf-8 -*-


class Command(object):
    """
    Base class for commands.
    """

    def __init__(self, name):
        """
        Create a new command with the provided name.
        :param name: the command's name
        :type name: str
        """
        self.name = name

    def execute(self, *args, **kwargs):
        """
        Execute the command with the provided arguments
        :param args: a list of arguments
        :param kwargs: named arguments
        """
        raise NotImplementedError()

    def undo(self, *args, **kwargs):
        """
        Undo the command. Provided arguments can be used to perform the undo action.
        :param args: a list of args
        :param kwargs: named arguments
        """
        raise NotImplementedError()

    def redo(self, *args, **kwargs):
        """
        redo command. By default, same as :meth:`Command.execute`.
        :param args: a list of arguments
        :param kwargs: named arguments
        """
        self.execute(*args, **kwargs)


class CommandInstance(object):
    """
    A CommandInstance is an object designed to hold command data in an history. It posses a reference to the command and
    two properties named :prop:`args` and :prop:`kwargs`. This two properties are arguments passed to the
    :meth:`Command.do` or :meth:`Command.undo` methods.
    """

    def __init__(self, command, *args, **kwargs):
        """
        Create a new CommandInstance with the provided reference to a command and, optionally, arguments to fill
        :prop:`args` and :prop:`kwargs` properties.
        :param command: a reference to a command object
        :type command: Command
        :param args: a list of arguments
        :param kwargs: named arguments
        """
        self._command = command
        self.args = args
        self.kwargs = kwargs

    @property
    def command(self):
        """
        Get the command this object is referencing.
        :return: the command object
        :rtype: Command
        """
        return self._command
