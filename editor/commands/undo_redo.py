from .command import BaseCommand

class UndoCommand(BaseCommand):
    def execute(self):
        command = self.app.history.get_undo()

        if command is None:
            print("No more undo!")
            return False

        command.undo()
        return False

class RedoCommand(BaseCommand):
    def execute(self):
        command = self.app.history.get_redo()
        
        if command is None:
            print("No more redo!")
            return False
        
        command.execute()
        return False
