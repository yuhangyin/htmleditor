class PrettyTreeStyle:
    SIBLING = "│  "
    CHILD = "├─ "
    LAST_CHILD = "└─ "
    EMPTY = "   "


class PrettyTreeVisitor:
    def __init__(self, *, style=None, show_root=False):
        self.style = style or PrettyTreeStyle()
        self.show_root = show_root
        self._out_lines = []
        self._indent = []

    def indent(self, indent):
        self._indent.append(indent)

    def dedent(self):
        self._indent.pop()

    def do_for_node(self, node):
        line = "{0}{1}".format(self.indentation, node.name)
        self._out_lines.append(line)

    def visit(self, node, *, last=True):
        indent = self.style.EMPTY if node.name == "html" else (self.style.LAST_CHILD if last else self.style.CHILD)
        self.indent(indent)
        self.do_for_node(node)  # 处理当前节点
        self.dedent()

        if hasattr(node, 'text') and node.text:
            indent = self.style.EMPTY if last else self.style.SIBLING  # 使用 LAST_CHILD 符号
            self.indent(indent)
            text_indent = self.style.CHILD if node.children else self.style.LAST_CHILD
            text_line = f"{self.indentation}{text_indent}{node.text.strip()}"
            self._out_lines.append(text_line)
            self.dedent()

        is_last = lambda i: i == len(node.children) - 1

        for i, child in enumerate(node.children):

            indent = self.style.EMPTY if last else self.style.SIBLING

            self.indent(indent)
            self.visit(child, last=is_last(i))
            self.dedent()

        return self

    def print(self, **kwargs):
        print(self.out_text, **kwargs)

    @property
    def indentation(self):
        if not self.show_root and self._indent:
            return "".join(self._indent[1:])
        return "".join(self._indent)

    @property
    def out_text(self):
        if not self.show_root and self._out_lines:
            return "\n".join(self._out_lines[1:])
        return "\n".join(self._out_lines)

