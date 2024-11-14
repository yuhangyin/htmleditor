class BaseNode:
    def __init__(self, name, *, data=None, text=""):
        self.name = name  # 标签名称，例如 "h1"
        self.data = data if data is not None else {}  # 附加数据，例如 {"id": "title"}
        self.text = text.strip()  # 标签内容，例如 "Welcome to my webpage"
        self.parent = None
        self.children = []


    def accept(self, v):
        cls_name = self.__class__.__name__.lower()
        visit = getattr(v, "do_for_" + cls_name, None)

        if visit is not None:
            return visit(self)

        return v.do_for_node(self)

    def add_child(self, node):
        if isinstance(node, BaseNode):
            node.parent = self
            self.children.append(node)

    def remove_child(self, node_id):
        node_to_remove = None
        for child in self.children:
            if child.data.get('id') == node_id:
                node_to_remove = child
                break
        self.children.remove(node_to_remove)

    def copy(self):
        node_cls = self.__class__
        node = node_cls(self.name, data=self.data, text=self.text)

        for child in self.children:
            node.add_child(child.copy())

        return node
    
    def insert_before(self, new_node, existing_node):
        if existing_node in self.children:
            # 找到要插入的节点位置
            index = self.children.index(existing_node)
            # 插入新节点
            self.children.insert(index, new_node)
            new_node.parent = self
        else:
            print(f"无法找到节点 {existing_node.name} 在子节点列表中。")

    @property
    def depth(self):
        if self.parent is None:
            return 0
        return self.parent.depth + 1

    @property
    def tag_representation(self):
        """用于格式化输出，包含标签名和 ID（如存在）"""
        id_str = f"#{self.data['id']}" if 'id' in self.data else ""
        return f"{self.name}{id_str}"


class BaseTree:
    def __init__(self, root):
        self.root = root

    def find(self, data):
        for node in self.traverse():
            if node.data.get('id') == data:
                return node

    def traverse(self):
        """深度优先遍历树的所有节点"""
        nodes = [self.root]
        while nodes:
            node = nodes.pop()
            for child in reversed(node.children):
                nodes.append(child)
            yield node


class BaseVisitor:
    def do_for_node(self, node):
        """处理通用节点"""
        pass

    def do_for_text_node(self, node):
        """处理文本节点"""
        pass
