import argparse
import os
import fileinput
from pathlib import Path
from enum import Enum
import sys
import dmarker_config as config

def get_argment_parser():
    parser = argparse.ArgumentParser(
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

if __name__ == "__main__":
    parser = get_argment_parser()
    args = parser.parse_args()

    # 順序    # 2. コマンドからCommandTypeを作成する
    # 3. CommandType.work実行  