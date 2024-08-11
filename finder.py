import re
import pathlib
import os
import argparse
import sys
import docx

def _init_menu():
    """
    initialize the command line parameter menu.
    """
    menu_parser = argparse.ArgumentParser()
    menu_parser.add_argument("-f", "--file", metavar='', help = "File name to search for. Enter 'unknown' if unknown.")
    menu_parser.add_argument("-s", "--string", metavar='', help = "The string to search for. Enter 'none' if not desired.")
    menu_parser.add_argument("-p", "--path", metavar='', help = "Directory path to search in.")
    menu_parser.add_argument("-o", "--output", metavar='', help = "Absolute file path to save output")#Need to add support for this.
    return menu_parser
def _menu(menu_parser):
    """
    Parser for the command line parameter menu and calls the appropriate functions.
    :param menu_parser: the argparse menu as created with '_init_menu()'
    """
    args = menu_parser.parse_args()
    if args.file:
        question_file_name = args.file
    if args.string:
        string_search = args.string
    if args.path:
        question_file_path = args.path
    ##Still need to add output support
    return question_file_path, question_file_name, string_search
def question_answers(file_path, file_name, stng):
    """
    function that emulates Linux utilities 'grep' and 'find'
    sets fn and stng to 'none' in case 'Enter' is pressed instead of
    entering 'none'.
    """
    print("\n\n\n\n\n")
    file_path = pathlib.Path(file_path)
    file_name = file_name.lower()
    if not file_name.strip():
        file_name = 'none'
    if not stng.strip():
        stng = 'none'
    stng = stng.lower()
    return file_path, file_name, stng
def list_dir(file_path, file_name):
    """
    checks if no filename was given and searches for the directory
    if directory exists and is found, prints all contents recursively
    """
    try:
        if file_name == 'none':
            if not file_path.is_dir():
                print(f"The directory {file_path} does not exist.")
            for entry in file_path.iterdir():
                if entry.is_file():
                    print(f"File: {entry}")
                elif entry.is_dir():
                    print(f"Directory: {entry}")
    except Exception as exception:
        print("The search for the directory faile. It may be a permissions issue")
        print(exception)
def find_file(file_path, file_name):
    """
    checks if filename was given and searches for the file
    if file is not found, prints it is not a valid filename
    """
    try:
        if file_name not in ['none', 'unknown']:
            file_path_name = file_path / file_name
            if file_path_name.is_file():
                full_path = file_path_name
                print("I found the file!!!!!!!")
                print(str(file_path_name) + "\n")
                return full_path
            elif file_path.is_dir():
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        if file_name in file:
                            full_path = pathlib.Path(os.path.join(root, file))
                            print("I found the file!!!!!!")
                            print(os.path.join(root, file) + "\n")
                            return full_path
                        else:
                            file_pattern = f'(.*?{file_name}.*?)'
                            if re.findall(file_pattern, file, flags=re.IGNORECASE):
                                full_path = pathlib.Path(os.path.join(root, file))
                                print("I found the file!!!!!!")
                                print(os.path.join(root, file) + "\n")
                                return full_path
            else:
                print(f"{file_name} is not a valid filename.")
    except Exception as exception:
        print("There has been an error. This might be a permissions error")
        print(exception)
def grep(file_name, stng):
    """
    checks if there was a string given to search
    if the string is found, prints the lines that contain the string
    if it is not found, prints that it can't be found or doesn't exist
    """
    if stng not in ['none', 'unkown']:
        ext = pathlib.Path(file_name).suffix.lower()
        pattern = f'(.*?{stng}.*?)'
        if ext in ['.txt', '.docx']:
            if ext == '.txt':
                content = pathlib.Path(file_name).read_text()
                search = re.findall(pattern, content, flags=re.IGNORECASE)
            elif ext == '.docx':
                doc = docx.Document(file_name).paragraphs
                search = []
                for paragraph in doc:
                    text_search = (re.findall(pattern, paragraph.text, flags=re.IGNORECASE))
                    if len(text_search) != 0:
                        search.append(text_search)
        if len(search) != 0:
            results_list = []
            for lines in search:
                results_list.append(str(lines))
            clean_results = "\n".join(results_list)
            print(f"I found '{stng}' {len(search)} times!")
            print("Here are all the lines that is was found on.\n")
            print(clean_results.strip())
        else:
            print(f"The string {stng} was not found")
def mystery_file(file_path, stng):
    """Looking for a unknown filename inside parent
    dir using a known string within the file
    """
    parent_path = pathlib.Path(file_path)
    if parent_path.is_dir():
        for root, dirs, files in os.walk(parent_path):
            for file in files:
                path = os.path.join(root, file)
                ext = pathlib.Path(file).suffix.lower()
                strng_pattern = f'(.*?{stng}.*?)'
                if ext in ['.txt', '.docx']:
                    if ext == '.txt':
                        try:
                            fh = pathlib.Path(root) / file
                            fc = fh.read_text()
                            lines = fc.split('\n')
                            doc_list = []
                            for line in lines:
                                if not fh in doc_list:
                                    if re.match(strng_pattern, line, flags=re.IGNORECASE):
                                        doc_list.append(fh)
                                        print(os.path.join(root, file))
                        except:
                            pass
                    elif ext == '.docx':
                        try:
#                        word_doc = docx.Document(os.path.join(root, file))
#                        for line in word_doc.paragraphs:
#                            if re.match(strng_pattern, line.text, flags=re.IGNORECASE):
#                                print(os.path.join(root, file))
                            doc = docx.Document(path)
                            list_of_docs = []
                            if doc not in list_of_docs:
                                for paragraph in doc.paragraphs:
                                    if re.search(rf'(.*{stng}.*)', paragraph.text, flags=re.IGNORECASE):
                                        list_of_docs.append(file)
                                        print(path)
                        except:
                            pass
if __name__ == '__main__':
    """
    questions for the user on what directory, filename, and/or string to search for
    """
    if len(sys.argv) == 1:
        print("This program is able to list the contents of a directory,")
        print("search for a file by name recursively from a known directory,")
        print("search for a string in a known file and directory,")
        print("or find an unknown file based on a known string when given")
        print("a parent directory.\n\n")
        question_file_name = input("What is the name of the file that you would like to find?\nIf you are not looking for a specific file enter 'None', if name is unkown, enter 'Unknown'.\n")
        print("\n\nWhat is the file path you would like for me to search? Be as specific as possible.", end="")
        question_file_path = input("The more broad the search, the longer and more likely for falses.\n ie 'C:\\Users\\%USER%\\Downloads'.\n")
        string_search = input("\n\nWhat is the string you want to search for? default is 'None'.\n")
    else:
        question_file_path, question_file_name, string_search = _menu(_init_menu())
    file_path, file_name, stng = question_answers(question_file_path, question_file_name, string_search)
    if question_file_path and not question_file_name and not stng:
        list_dir(file_path, file_name)
    elif question_file_name and question_file_path and (string_search == 'none' or string_search != string_search.strip()):
        find_file(file_path, file_name)
    elif question_file_name.lower() == 'unknown':
        mystery_file(file_path, stng)
    elif question_file_path and question_file_name and string_search != 'none':
        grep(find_file(file_path, file_name), stng)
        