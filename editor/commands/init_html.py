from .command import BaseCommand
from editor.core import HtmlReader

inithtml_content = """
<html>
    <head>
        <title></title>
    </head>
    <body></body>
</html>
"""

class InitCommand(BaseCommand):
    def execute(self):
        if self.app.dirty:
            print("请先保存您的工作，再打开其他文件！")
            return False

        self.app.tree = HtmlReader().read_html(inithtml_content)
        self.app.history.clear()
        print("成功初始化文件 。")


        return True