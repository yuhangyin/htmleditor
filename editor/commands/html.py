from .command import BaseCommand
from editor.core import HtmlNode


class InsertElementCommand(BaseCommand):
    def execute(self):
        tag_name, id_value, insert_location, *text_content = self.args
        text_content = text_content[0] if text_content else "" 
        
        # 找到插入位置的父节点
        insert_location_node = self.app.tree.find(insert_location)
        
        if not insert_location_node:
            print(f"Element with id {insert_location} not found!")
            return False

        # 创建新元素并插入
        new_element = HtmlNode(tag_name, data={'id': id_value}, text=text_content)
        insert_location_node.parent.insert_before(new_element, insert_location_node)
        self.inserted_element = new_element
        return True

    def undo(self):
        # 撤销插入操作
        self.inserted_element.parent.remove_child(self.inserted_element)


class AppendElementCommand(BaseCommand):
    def execute(self):
        tag_name, id_value, parent_element, *text_content = self.args
        text_content = text_content[0] if text_content else ""
        
        # 找到父元素
        parent_node = self.app.tree.find(parent_element)
        
        if not parent_node:
            print(f"Parent element with id {parent_element} not found!")
            return False

        # 创建新元素并追加到父节点中
        new_element = HtmlNode(tag_name, id=id_value, text=text_content)
        parent_node.add_child(new_element)
        self.appended_element = new_element
        return True

    def undo(self):
        # 撤销追加操作
        self.appended_element.parent.remove_child(self.appended_element)


class EditIdCommand(BaseCommand):
    def execute(self):
        old_id, new_id = self.args
        element = self.app.tree.find(old_id)
        
        if not element:
            print(f"Element with id {old_id} not found!")
            return False

        if self.app.tree.find(new_id):
            print(f"Element with id {new_id} already exists!")
            return False

        # 修改 id
        element.id = new_id
        self.old_id = old_id
        self.new_id = new_id
        return True

    def undo(self):
        # 撤销 id 修改
        element = self.app.tree.find(self.new_id)
        if element:
            element.id = self.old_id


class EditTextCommand(BaseCommand):
    def execute(self):
        element_id, *new_text_content = self.args
        new_text_content = new_text_content[0] if new_text_content else ""

        # 查找元素
        element = self.app.tree.find(element_id)
        
        if not element:
            print(f"Element with id {element_id} not found!")
            return False

        # 修改文本内容
        self.old_text = element.text
        element.text = new_text_content
        return True

    def undo(self):
        # 撤销文本修改
        element = self.app.tree.find(self.args[0])
        if element:
            element.text = self.old_text


class DeleteElementCommand(BaseCommand):
    def execute(self):
        element_id = self.args[0]
        element = self.app.tree.find(element_id)

        if not element:
            print(f"Element with id {element_id} not found!")
            return False

        # 删除元素并记录
        self.deleted_element = element
        self.deleted_element_parent = element.parent
        element.parent.remove_child(element)
        return True

    def undo(self):
        # 撤销删除
        self.deleted_element_parent.add_child(self.deleted_element)

