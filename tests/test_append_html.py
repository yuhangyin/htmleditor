import os

import editor

from test_utils import create_file_hash


def test_insert_html():
    f0 = "tests/test_html/append.html"
    f1 = "tests/test_html/append_out.html"

    commands = [
        "read tests/test_html/test.html",
        'append li item4 item-list "Item D"',
        'append p footer-text2 footer "Hello nice to meet ya"',
        "save tests/test_html/append_out.html",
    ]

    app = editor.App()

    for command in commands:
        app.execute_from_text(command)

    h0 = create_file_hash(f0)
    h1 = create_file_hash(f1)

    os.remove(f1)

    assert h0 == h1