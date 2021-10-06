import argparse
import os
import fileinput
from pathlib import Path
from enum import Enum
import sys
import dmarker_config as config
from arg_parser import dmarker_arg_parser

if __name__ == "__main__":
    parser = dmarker_arg_parser()
    parser.print_help()