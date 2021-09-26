import argparse
import os
import fileinput
from collections import namedtuple
from pathlib import Path
import sys

Marker = namedtuple("Marker", ["name", "path_string"])

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
            markers = [
                Marker(parsed_args.marker, parsed_args.path)
            ]
            save_markers(markers)
    elif parsed_args.work == "delete":
       if parsed_args.marker != None :
            delete_marker(parsed_args.marker)
    elif parsed_args.work == "list":
        print(get_markers())

def save_markers(markers):
    print("save")
    open_mode = "a"
    if not os.path.exists("dmarker.txt"):
        open_mode = "w"
    
    with open("dmarker.txt", mode=open_mode) as data_file:
        for m in markers:
            data_file.write("{}:{}\n".format(m.name, m.path_string))
        data_file.flush()
        os.fsync(data_file)

def delete_marker(marker_name):
    markers = get_markers()
    for m in markers:
        if m.name == marker_name:
            markers.remove(m)
    
    with open("dmarker.txt", mode="w") as data_file:
        for m in markers:
            data_file.write("{}:{}\n".format(m.name, m.path_string))
        data_file.flush()
        os.fsync(data_file)


def get_markers() -> list[Marker]:
    print("markers")
    if not os.path.exists("dmarker.txt"):
        return []

    markers = []
    for line in fileinput.input(files="dmarker.txt"):
        data = line.split(":")
        markers.append(Marker(data[0], data[1]))
    return markers

def get_path(marker_name):
    markers = get_markers()
    for m in markers:
        if m.name == marker_name:
            return m

if __name__ == "__main__":
    parser = get_argment_parser()
    args = parser.parse_args()
    work(args)
    
    