import argparse
import os
import fileinput
from collections import namedtuple
from pathlib import Path
from enum import Enum
import sys
import dmarker_config as config

# workのenumを作ること
# そろそろファイル分けたほうがいい

class CommandType(Enum):
    ADD = "add"
    DELETE = "delete"
    LIST = "list"

    @classmethod
    def init_by_str(cls, str):
        for member_var in list(cls):
            if member_var.value == str:
                return member_var

    def work(self):
        pass

# 何もしない。コマンドをポリモーフィズムで扱いたいがためだけに作った
class CommandTypeInterface():
    command_str = None

    def work(self, marker):
        pass

class AddCommand(CommandTypeInterface):
    command_str = "add"

    def work(self, marker):
        save_markers(marker)
        
class DeleteCommand(CommandTypeInterface):
    command_str = "delete"

    def work(self, marker):
        delete_marker(marker.name)

class ListCommand(CommandTypeInterface):
    command_str = "list"

    def work(self, marker=None):
        return get_markers()

class Marker:
    def __init__(self, name, path_string):
        self.name = name
        self.path_string = path_string
    
    def is_same_name_marker(self, marker: Marker):
        return self.name == marker.name

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

def work(parsed_args):
    if parsed_args.work == "add":
        if parsed_args.marker != None and parsed_args.path != None :
            marker = Marker(parsed_args.marker, parsed_args.path)
            save_markers(marker)
    elif parsed_args.work == "delete":
       if parsed_args.marker != None :
            delete_marker(parsed_args.marker)
    elif parsed_args.work == "list":
        print(get_markers())

def save_markers(marker):
    # マーカー重複時の削除のロジックを描くのが面倒だったので、
    # ひとまずデータ全体を引っ張ってきて、そこから重複していたら削除or上書きをして、
    # そのデータを用いてデータファイル全てを上書きし直している。

    existing_makers = get_markers()
    duplicated_maker = None
    for existing_marker in existing_makers:
        if existing_makers.is_same_name_marker(marker):
            # ここでデータをセーブするロジックとUI表示が混じってしまっているので、                
            # いつかこのUIを分離するべき。
            question_string =  config.save_marker_duplication_question\
                                        .format(existing_marker.path_string, marker.path_string)
            if yes_or_no_ui(question_string):
                duplicated_maker = existing_marker
            else:
                return
    
    existing_makers.remove(duplicated_maker)
    existing_makers.append(marker)
    saved_markers = existing_makers
        
    with open(config.data_file_name, mode="w") as data_file:
        for marker in saved_markers:
            data_file.write("{}:{}\n".format(marker.name, marker.path_string))
        data_file.flush()
        os.fsync(data_file)

def delete_marker(marker_name):
    markers = get_markers()
    for m in markers:
        if m.name == marker_name:
            markers.remove(m)
    
    with open(config.data_file_name, mode="w") as data_file:
        for m in markers:
            data_file.write("{}:{}\n".format(m.name, m.path_string))
        data_file.flush()
        os.fsync(data_file)

def print_marker():
    markers = get_markers()
    for marker in markers:
        print("{}: {}".format(marker.name, marker.path_string))

def get_markers() -> list[Marker]:
    print("markers")
    if not os.path.exists(config.data_file_name):
        return []

    markers = []
    for line in fileinput.input(files=config.data_file_name):
        data = line.split(":")
        markers.append(Marker(data[0], data[1]))
    return markers

def get_path(marker_name):
    markers = get_markers()
    for m in markers:
        if m.name == marker_name:
            return m

def yes_or_no_ui(question_string: str):
    true_answer_list = ["yes", "YES", "y", "Y"]

    print("{} :[y/n]".format(question_string))
    user_input = os.read()
    
    return (user_input in true_answer_list)


if __name__ == "__main__":
    parser = get_argment_parser()
    args = parser.parse_args()

    # 順序
    # 1. 必要に応じてmarkerを作成する
    # 2. コマンドからCommandTypeを作成する
    # 3. CommandType.work実行
    
    work(args)
    
    