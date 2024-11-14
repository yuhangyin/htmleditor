import os

import editor

from test_utils import create_file_hash


def test_insert_html():
    f0 = "tests/test_html/edit.html"
    f1 = "tests/test_html/edit_out.html"

    commands = [
        "read tests/test_html/test.html",
        "edit-id intro description",
        "edit-id item3 item1",
        'edit-text item1 "Item A"',
        'edit-text header "Welcome to My Webpage"',
        "save tests/test_html/edit_out.html",
    ]

    app = editor.App()

    for command in commands:
        app.execute_from_text(command)

    h0 = create_file_hash(f0)
    h1 = create_file_hash(f1)

    os.remove(f1)

    assert h0 == h1