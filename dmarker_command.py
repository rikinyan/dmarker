
import os
from dmarker import get_markers
import dmarker_config as config
from Marker import Marker
import user_interface as ui
import dmarker_data as data_store

# コマンドの引数のinterface
class CommandArgmentList:
    command_args = {}
    def __init__(self, arg_list):
        pass

class AddCommandArgmentList(CommandArgmentList):

    def __init__(self, arg_list: dict) -> None:
        self.command_args = {
            "marker_name": arg_list["marker_name"],
            "marker_path": arg_list["marker_path"]
        }

class DeleteCommandArgmentList(CommandArgmentList):

    def __init__(self, arg_list: dict) -> None:
        self.command_args = {
            "marker_name": arg_list["marker_name"]
        }

class ListCommandArgmentList(CommandArgmentList):
    def __init__(self, arg_list: dict) -> None:
        self.command_args = {}


# 何もしない。コマンドをポリモーフィズムで扱いたいがためだけに作った
class CommandTypeInterface():
    COMMAND_STRING = None

    def __init__(self, commandArgument: CommandArgmentList) -> None:
        self.commandArgument = commandArgument

    def work(self):
        pass

class AddCommand(CommandTypeInterface):
    COMMAND_STRING = "add"

    def work(self):
        arg_list = AddCommandArgmentList(self.commandArgument)
        added_marker = Marker(arg_list["marker_name"], arg_list["marker_path"])

        existing_makers = get_markers()
        for existing_marker in existing_makers:
            if existing_marker.is_same_name_marker(added_marker):
                question_string =  config.save_marker_duplication_question\
                                            .format(existing_marker.path_string, added_marker.path_string)
                if ui.yes_or_no_ui(question_string):
                    break
                else:
                    return

        data_store.save_markers(added_marker)
        
class DeleteCommand(CommandTypeInterface):
    COMMAND_STRING = "delete"

    def work(self):
        arg_list = AddCommandArgmentList(self.commandArgument)
        marker_name = arg_list["marker_name"]
        data_store.delete_marker(marker_name)

class ListCommand(CommandTypeInterface):
    COMMAND_STRING = "list"

    def work(self):
        markers = data_store.get_markers()
        for marker in markers:
            print("{}: {}".format(marker.name, marker.path_string))