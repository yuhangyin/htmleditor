import os

import editor

from test_utils import create_file_hash


def test_insert_html():
    f0 = "tests/test_html/undo_redo.html"
    f1 = "tests/test_html/undo_redo_out.html"

    commands = [
        "read tests/test_html/test.html",
        'insert li item2 item3 "Item B"',
        'insert li item1 item2 "Item A"',
        "undo",
        'append li item4 item-list "Item D"',
        "undo",
        "redo",
        "save tests/test_html/undo_redo_out.html"
    ]

    app = editor.App()

    for command in commands:
        app.execute_from_text(command)

    h0 = create_file_hash(f0)
    h1 = create_file_hash(f1)

    os.remove(f1)

    assert h0 == h1