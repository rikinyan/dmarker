import argparse
import os
import fileinput
from collections import namedtuple

Marker = namedtuple("Marker", ["name", "path_string"])

def get_argment_parser():
    parser = argparse.ArgumentParser(
        prog="dmarker",
        description="create dir marker and you can jump to dir by marker you created.",
    )

    return parser

def save_markers(markers):
    print("save")
    open_mode = "a"
    if not os.path.exists("dmarker.txt"):
        open_mode = "w"
    
    with open("dmarker.txt", mode=open_mode) as data_file:
        markers = get_markers()
        for m in markers:
            data_file.write("{marker.name}:{marker.path}")
        data_file.flush()
        os.fsync(data_file)

def delete_marker(marker_name):
    markers = get_markers()
    for m in markers:
        if m.name == marker_name:
            markers.remove(m)
    save_markers(markers)


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
    print("hello!")