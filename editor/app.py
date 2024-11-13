from collections import Counter
from editor import commands

# 定义命令字典，映射命令字符串到相应的命令类
COMMANDS = {
    "read": commands.OpenCommand,
    "save": commands.SaveCommand,
    "insert": commands.InsertElementCommand,
    "append": commands.AppendElementCommand,
    "edit-id": commands.EditIdCommand,
    "edit-text": commands.EditTextCommand,
    "delete": commands.DeleteElementCommand,
    "undo": commands.UndoCommand,
    "redo": commands.RedoCommand,
    "print-indent": commands.ShowIndentCommand,
    "print-tree": commands.ShowTreeCommand,
    "spell-check": commands.SpellCheckCommand,
    "init": commands.InitCommand
}

class App:
    def __init__(self):
        self.tree = None  # HTML 树结构
        self.history = commands.CommandHistory()  # 用于存储历史命令
        self.current_file = None  # 当前文件路径
        self.dirty = False  # 标记是否有未保存的更改
        self.commands = COMMANDS  # 命令字典

    def execute_from_text(self, text):
        # 解析输入的命令文本
        command_name, args = commands.parse_command_text(text)
        command_class = self.commands.get(command_name, None)

        if command_class is None:
            print(f"{command_name} is not a valid command!")
            return

        # 创建命令实例并执行
        command = command_class(self, args)

        if command.execute():
            self.history.add(command)
            self.dirty = True

    def main(self):
        # 主循环，等待用户输入命令
        while True:
            text = input("Enter command: ")
            self.execute_from_text(text)