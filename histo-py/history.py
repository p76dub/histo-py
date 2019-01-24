# -*- coding: utf-8 -*-
import command


class NothingToUndoException(Exception):
    def __init__(self):
        super(NothingToUndoException, self).__init__("There is command to undo.")


class NothingToRedoException(Exception):
    def __init__(self):
        super(NothingToRedoException, self).__init__("There is nothing to redo.")


class EmptyHistoryException(Exception):
    def __init__(self):
        super(EmptyHistoryException, self).__init__("There is no items in this history.")


class History(object):
    """
    History objects are design to keep track of executed commands in order to undo or redo them.
    """

    def append(self, e):
        """
        Push an element in the history, being the first command to undo if the user request so and execute it.
        :param e: the command
        :type e: command.CommandInstance
        """
        raise NotImplementedError()

    def back(self):
        """
        Move the internal cursor backward, executing an undo on the previously selected command. If no more commands
        exists, meaning you reached the oldest command, method raise an exception.
        :raises NothingToUndoException, EmptyHistoryException
        """
        raise NotImplementedError()

    def forth(self):
        """
        Move forward in history, moving the cursor first and executing a redo then. Fail if no commands
        can be redo.
        :raises EmptyHistoryException, NothingToRedoException
        """
        raise NotImplementedError()

    def item(self):
        """
        Get the current selected command.
        :raise EmptyHistoryException
        :return: the selected command or None if not command is selected
        :rtype: None|command.CommandInstance
        """
        raise NotImplementedError()

    def can_undo(self):
        """
        Say if a command can be undone.
        :return: True if it can, else False
        :rtype: bool
        """
        raise NotImplementedError()

    def can_redo(self):
        """
        Say if a command can be redo.
        :return: True if it is possible, else False
        :rtype: bool
        """
        raise NotImplementedError()

    def clear(self):
        """
        Clear this history, removing all stored commands.
        """
        raise NotImplementedError()

    def __len__(self):
        """
        Return the number of commands stored in this history.
        :return: history's lenght
        :rtype: int
        """
        raise NotImplementedError()


class BoundedHistory(History):
    """
    BoundedHistory is an History with a capacity. Once this capacity is reached, oldest elements are removed.
    """

    def __init__(self, capacity):
        """
        Create a new BoundedHistory with the provided capacity.
        :param capacity: history's capacity
        """
        self._capacity = capacity

    @property
    def capacity(self):
        """
        Get this history's capacity.
        :return: history's capacity
        :rtype: int
        """
        return self._capacity


class DoubleStackHistory(History):
    """
    An implementation of History using stacks. The first one is used as the primary stack. When new elements are added
    to the history, they are pushed to the primary stack. When a call is made to back, top element is retrieved and
    pushed on the second stack. While the user is keeping calling back, elements are added to the second stack. If a
    call to add is made, second stack is cleared. Calls to forth pop elements of the second one and push them on the
    primary one.
    """

    def __init__(self):
        """
        Create a new DoubleStackHistory without any command.
        """
        self._primary = []
        self._secondary = []

    def append(self, e):
        # Clear secondary
        self._secondary.clear()

        # Append element to the primary stack and execute command
        self._primary.append(e)
        e.command.execute(*e.args, **e.kwargs)

    def back(self):
        if len(self._primary) == 0:
            if len(self._secondary) == 0:
                raise EmptyHistoryException()
            raise NothingToUndoException()

        # Add last element to the secondary stack
        self._secondary.append(self._primary[-1])

        # Pop and undo command
        c = self._primary.pop()
        c.command.undo(*c.args, **c.kwargs)

    def forth(self):
        if len(self._secondary) == 0:
            if len(self._primary) == 0:
                raise EmptyHistoryException()
            raise NothingToRedoException()

        # Add last element to primary stack
        self._primary.append(self._secondary[-1])

        # Pop element and execute redo
        c = self._secondary.pop()
        c.command.redo(*c.args, **c.kwargs)

    def item(self):
        if len(self._primary) == 0 and len(self._secondary) == 0:
            raise EmptyHistoryException()
        return self._primary[-1] if len(self._primary) > 0 else None

    def can_undo(self):
        return len(self._primary) > 0

    def can_redo(self):
        return len(self._secondary) > 0

    def clear(self):
        self._primary.clear()
        self._secondary.clear()

    def __len__(self):
        return len(self._primary) + len(self._secondary)
