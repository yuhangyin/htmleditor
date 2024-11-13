import re

def unquoted(text):
    """Remove leading and trailing quotes from a string."""
    return text.strip('"')

def parse_command_text(text):
    """Parse command input, return command and argument list."""
    command, *remaining = text.split(" ", 1)
    if not remaining:
        return command, []

    args = []
    remaining = remaining[0].strip()

    # Find matches for arguments wrapped in quotes or separated by spaces
    matches = re.finditer(r'"[^"]*"|\S+', remaining)
    for match in matches:
        arg = match.group(0)
        args.append(unquoted(arg) if arg.startswith('"') else arg)

    return command, args

class BaseCommand:
    """A base command structure for the application commands."""
    def __init__(self, app, args):
        self.app = app
        self.args = args

    def execute(self):
        """Executes the command. To be overridden by subclasses."""
        return False

    def undo(self):
        """Undo the command. To be implemented by subclasses if needed."""
        raise NotImplementedError("Undo is not implemented for this command.")

class CommandHistory:
    """History manager for storing command actions."""
    def __init__(self):
        self.commands = []
        self._undos = []

    def add(self, command):
        """Add a command to history and clear the redo stack."""
        self.commands.append(command)
        self._undos.clear()

    def clear(self):
        """Clear command and undo history."""
        self.commands.clear()
        self._undos.clear()

    def get_undo(self):
        """Get the last command for undo, and move it to the redo stack."""
        if self.commands:
            command = self.commands.pop()
            self._undos.append(command)
            return command
        return None

    def get_redo(self):
        """Get the last undone command for redo, and return it to history."""
        if self._undos:
            command = self._undos.pop()
            self.commands.append(command)
            return command
        return None
