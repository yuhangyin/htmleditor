import os
from .command import BaseCommand
from editor.core import HtmlReader,ToHtmlVisitor

class OpenCommand(BaseCommand):
    def execute(self):
        if self.app.dirty:
            print("请先保存您的工作，再打开其他文件！")
            return False

        path = self.args[0]

        if not os.path.exists(path):
            dir, name = os.path.split(path)
            try:
                open(path, "w").close()
                print(f"创建了文件 {name} 于 {dir if dir else '当前目录'}。")
            except IOError as e:
                print(f"无法创建文件 {name}:{e}")
                return False
        try:
            with open(path, "r", encoding="utf-8") as file:
                content = file.read()  # 读取文件内容
            self.app.tree = HtmlReader().read_html(content)
            self.app.current_file = path
            self.app.history.clear()
            print(f"成功打开文件 {path}。")
        except Exception as e:
            print(f"无法读取文件 {path}:{e}")
            return False

        return True


class SaveCommand(BaseCommand):
    def execute(self):

        path = self.args[0] if self.args else self.app.current_file

        if not os.path.exists(path):
            dir, name = os.path.split(path)
            try:
                open(path, "w").close()
                print(f"创建了文件 {name} 于 {dir if dir else '当前目录'}。")
            except IOError as e:
                print(f"无法创建文件 {name}:{e}")
                return False

        try:
            self.app.tree.to_html(path)
            self.app.dirty = False
            print(f"成功保存到 {path}")
        except Exception as e:
            print(f"无法保存文件 {path}:{e}")
            return False

        return True
