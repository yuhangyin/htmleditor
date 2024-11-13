from editor.utils.pretty_tree import PrettyTreeVisitor
from spellchecker import SpellChecker
from .command import BaseCommand

class HtmlSpellChecker:
    def __init__(self):
        self.spell = SpellChecker()

    def check_text(self, text):
        words = text.split()
        misspelled = self.spell.unknown(words)
        return misspelled

class SpellCheckVisitor(PrettyTreeVisitor):
    def __init__(self):
        super().__init__()
        self.spell_checker = HtmlSpellChecker()
        self.results = []

    def do_for_node(self, node):
        # 只检查包含文本内容的节点
        if hasattr(node, 'text') and node.text:
            misspelled_words = self.spell_checker.check_text(node.text)
            if misspelled_words:
                self.results.append(f"Text: '{node.text}' contains misspelled words: {', '.join(misspelled_words)}")

    def visit(self, node, *, last=True):
        # 调用 do_for_node 来检查当前节点
        self.do_for_node(node)

        # 递归访问子节点
        is_last = lambda i: i == len(node.children) - 1

        for i, child in enumerate(node.children):
            self.visit(child, last=is_last(i))

    def print_results(self):
        if self.results:
            print("Spell-check results:")
            for result in self.results:
                print(result)
        else:
            print("No spelling errors found.")

class SpellCheckCommand(BaseCommand):
    def execute(self):
        spell_checker = SpellCheckVisitor()
        spell_checker.visit(self.app.tree.root)
        spell_checker.print_results()
