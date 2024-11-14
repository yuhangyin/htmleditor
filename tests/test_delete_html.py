import os

import editor

from test_utils import create_file_hash


def test_insert_html():
    f0 = "tests/test_html/delete.html"
    f1 = "tests/test_html/delete_out.html"

    commands = [
        "read tests/test_html/test.html",
        "delete item-list",
        "delete footer-text",
        "delete intro",
        "save tests/test_html/delete_out.html",
    ]

    app = editor.App()

    for command in commands:
        app.execute_from_text(command)

    h0 = create_file_hash(f0)
    h1 = create_file_hash(f1)

    os.remove(f1)

    assert h0 == h1