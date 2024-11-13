from .command import BaseCommand
from editor.utils.pretty_tree import PrettyTreeVisitor
from editor.core import ToHtmlVisitor

class PrettyHtmlTree(PrettyTreeVisitor):
    def __init__(self):
        super().__init__()

    def do_for_node(self, node):

        node_info = f"{node.name}"
        if node.data.get("id"):
            node_info += f"#{node.data['id']}"
        
        line = f"{self.indentation}{node_info}"
        self._out_lines.append(line)

class ShowTreeCommand(BaseCommand):
    def execute(self):
        PrettyHtmlTree().visit(self.app.tree.root).print()
        return False

class ShowIndentCommand(BaseCommand):
    def execute(self):
        indent_idx = self.args[0]
        visitor = ToHtmlVisitor()
        visitor.visit(self.app.tree.root, indent_idx)
        print(visitor.html_text)
