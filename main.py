import argparse
import editor

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="htmleditor v1.0",
        description="A CLI that manages your hmtl in .html file format",
    )
    parser.add_argument("html_file", nargs="?", default=None)

    args = parser.parse_args()
    app = editor.App()

    if args.html_file:
        app.execute_from_text("read {0}".format(args.html_file))

    app.main()
