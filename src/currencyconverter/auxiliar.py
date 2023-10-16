import tkinter.filedialog

import customtkinter as ctk


def browse_folder(folder_path_entry: ctk.CTkEntry) -> None:
    """
    Open a file dialog to browse for a folder and update a custom tkinter entry widget with the
    selected folder path.

    Parameters:
        folder_path_entry (ctk.CTkEntry): The custom tkinter entry widget where the selected folder
        path will be displayed.
    """
    folder_path = tkinter.filedialog.askdirectory()
    if folder_path:
        folder_path_entry.delete(0, ctk.END)
        folder_path_entry.insert(0, folder_path)


def read_from_file_by_line(file_path: str, mode: str = 'r') -> list[str]:
    """
    Read content from a file and split it into lines.

    Parameters:
        file_path (str): The path to the file to be read.
        mode (str, optional): The mode in which the file should be opened.

    Returns:
        list[str]: A list of strings where each string represents a line from the file.

    Note:
    - If the file is not found, a message is printed to the console, and an empty list is returned.
    """
    try:
        with open(file_path, mode) as file:
            file_content = file.read().splitlines()
    except FileNotFoundError:
        print(f'File not found: {file_path}')

    return file_content
