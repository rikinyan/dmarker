import os

def yes_or_no_ui(question_string: str):
    true_answer_list = ["yes", "YES", "y", "Y"]

    print("{} :[y/n]".format(question_string))
    user_input = os.read()
    
    return (user_input in true_answer_list)