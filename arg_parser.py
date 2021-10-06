from argparse import ArgumentParser

def dmarker_arg_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="dmarker",
        description="create dir marker and you can jump to dir by marker you created.",
    )

    parser.add_argument(
        "work",
        choices=["add", "delete", "list"],
    )

    parser.add_argument(
        "-m", "--marker",
        type=str
    )

    parser.add_argument(
        "-p", "--path",
        type=Path,
        required=False,
        default=os.getcwd()
    )

    return parser