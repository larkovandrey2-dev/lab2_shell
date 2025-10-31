import os
import pathlib

from errors.shell_errors import ShellError
from src.history import create_history_record, get_last_history, get_last_history_number
from src.utils import ensure_exists,normalize

def cmd_cd(args):
    """
    Переходит в указанную директорию.

    args: список аргументов команды cd
        - если пустой, переходит в домашнюю директорию
        - если один аргумент, переходит в указанный путь

    Вызывает ShellError при:
        - передаче более одного аргумента
        - если путь не существует или не является директорией

    Создает запись в истории команд.
    """
    if len(args) > 1:
        raise ShellError(f"cd: {args} : too many arguments")
    if len(args) == 0:
        return os.chdir(pathlib.Path().home())
    path = ensure_exists(normalize(args[0]),"cd")
    if not path.is_dir():
        raise ShellError(f"cd: not a directory: '{path}'")
    last_cmd_num = get_last_history_number() + 1
    record = {"cmd":"cd","user_input": "cd " + " ".join(args),"number":last_cmd_num}
    create_history_record(record)
    return os.chdir(path)

def cmd_cat(args):
    """
    Выводит содержимое одного или нескольких файлов.

    args: список файлов для вывода

    Вызывает ShellError при:
        - если файл не существует
        - если путь не является файлом
        - при ошибках доступа (PermissionError)

    Создает запись в истории команд для каждого файла.
    """
    if len(args) == 0:
        raise ShellError("cat: empty arguments")
    for path in args:
        p = ensure_exists(normalize(path),"cat")
        if not p.is_file():
            raise ShellError(f"cat: '{p}' is not a file")
        try:
            with p.open("r") as f:
                content = f.read()
                print(content)
            last_cmd_num = get_last_history_number() + 1
            record = {"cmd": "cat","user_input": "cat " + " ".join(args),"number": last_cmd_num}
            create_history_record(record)
        except PermissionError:
            raise ShellError(f"cat: Permission denied: '{p}'")

def cmd_history(args):
    """
    Выводит последние команды из истории.

    args: список аргументов команды history
        - если указан один аргумент, выводит указанное число последних команд
        - если пустой, выводит последние 10 команд

    Вызывает ShellError при:
        - передаче более одного аргумента
        - если аргумент не является числом

    Выводит список команд с их номерами.
    """
    history_list_number = 10
    if len(args) > 1:
        raise ShellError(f"history: too many arguments: '{args}'")
    if len(args) == 1:
        if not args[0].isdecimal():
            raise ShellError(f"history: invalid argument: '{args[0]}'")
        history_list_number = int(args[0])
    history_list = get_last_history(history_list_number)
    for history in history_list:
        print(history[0],history[1])
    record = {
        "cmd": "history",
        "user_input": "history " + " ".join(args),
        "number": get_last_history_number() + 1,
    }
    create_history_record(record)
