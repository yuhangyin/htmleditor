from bs4 import BeautifulSoup
from editor.utils.tree import BaseNode, BaseTree, BaseVisitor

class HtmlNode(BaseNode):
    """表示 HTML 标签节点。"""
    def __init__(self, name, *, data=None, text=""):
        super().__init__(name, data=data)
        self.text = text.strip()  # 存储标签内容（如果有的话）

class HtmlRoot(HtmlNode):
    def __init__(self):
        super().__init__("[[ROOT]]")

class HtmlTree(BaseTree):
    def __init__(self):
        super().__init__(HtmlRoot())

    def to_html(self, path):
        v = ToHtmlVisitor()

        v.visit(self.root)

        with open(path, "w") as fp:
            fp.write(v.html_text)

class HtmlReader:

    def read_html(self, html_content):
        """解析 HTML 字符串内容并返回 HtmlTree"""
        tree = HtmlTree()
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 创建并添加 HTML 根节点
        if soup.html:
            html_node = self._create_node(soup.html)
            tree.root.add_child(html_node)
            self._build_tree(soup.html, html_node)

        return tree

    def _build_tree(self, soup_node, parent_node):
        """递归地将 BeautifulSoup 解析的节点添加到树中。"""
        for child in soup_node.children:
            if child.name:  # 如果子节点是标签
                node = self._create_node(child)
                parent_node.add_child(node)
                self._build_tree(child, node)
            elif child.string and child.string.strip():  # 如果子节点是文本
                # 将文本直接存储到父节点的 text 属性中
                parent_node.text = (parent_node.text or "") + " " + child.string.strip()
                parent_node.text = parent_node.text.strip()  # 去除多余空格


    def _create_node(self, soup_node):
        """根据 BeautifulSoup 标签创建 HtmlNode 节点"""
        node_name = soup_node.name
        node_id = soup_node.get("id", "")
        data = {"id": node_id} if node_id else {}
        node_text = soup_node.string.strip() if not soup_node.contents else ""
        return HtmlNode(name=node_name, data=data, text=node_text)

class ToHtmlVisitor(BaseVisitor):
    def __init__(self):
        self._html_lines = []
        self._level = -1
        
    def visit(self, node, indent_index = 2):
        if node.name == "[[ROOT]]":
            # 根节点不需要输出，直接返回
            for child in node.children:
                self.visit(child, indent_index)
            return
        self._level += 1
        indent = ' ' * self._level * int(indent_index)

        opening_tag = f"<{node.name}"
        if 'id' in node.data:
            opening_tag += f" id=\"{node.data['id']}\""
        opening_tag += ">"

        # 判断是否需要在同一行输出闭合标签
        if node.text and not node.children:
            # 如果有文本且没有子节点，开标签、文本和闭合标签在同一行
            line = f"{indent}{opening_tag}{node.text.strip()}</{node.name}>"
            self._html_lines.append(line)

        else:
            # 输出开标签
            self._html_lines.append(f"{indent}{opening_tag}")
            
            # 输出文本内容
            if node.text:
                self._html_lines.append(f"{indent}    {node.text.strip()}")
            
            # 递归访问子节点
            for child in node.children:
                self.visit(child, indent_index)

            # 输出闭合标签
            self._html_lines.append(f"{indent}</{node.name}>")

        self._level -= 1

    @property
    def html_text(self):
        return "\n".join(self._html_lines)

