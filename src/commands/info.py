import os
import pathlib
import platform
from datetime import datetime

from errors.shell_errors import ShellError
from src.constants import RIGHTS
from src.history import create_history_record, get_last_history_number
from src.utils import ensure_exists, normalize


def cmd_pwd(args):
    """
    Печатает текущую рабочую директорию.

    args: список аргументов команды pwd (должен быть пустым).

    Вызывает ShellError, если переданы лишние аргументы.
    Создает запись в истории команд.
    """
    if len(args) > 0:
        raise ShellError('pwd: too many arguments')
    last_cmd_num = get_last_history_number() + 1
    record = {"cmd":"pwd", "num":last_cmd_num,"user_input": "pwd"}
    create_history_record(record)
    print(pathlib.Path().cwd())

def cmd_ls_detailed_info(item):
    """
        Возвращает подробную информацию о файле или директории.

        item: pathlib.Path объекта файла или директории

        Формат возвращаемой строки:
            права доступа, владелец, группа, размер, дата изменения, имя
    """
    stats = item.stat()

    if platform.system() == "Windows":
        output_r = 'd' if item.is_dir() else '-'
        perms = ""
        perms += "r" if os.access(item, os.R_OK) else "-"
        perms += "w" if os.access(item, os.W_OK) else "-"
        perms += "x" if os.access(item, os.X_OK) else "-"
        output_r += perms * 3
    else:
        rights = str(oct(stats.st_mode)[-3:])
        output_r = ""
        if item.is_dir():
            output_r += 'd'
        if item.is_file():
            output_r += '-'
        for k in rights:
            for bit in [4, 2, 1]:
                output_r += RIGHTS[bit] if (int(k) & bit) else '-'

    try:
        owner = item.owner()
    except Exception:
        owner = "unknown"
    try:
        group = item.group()
    except Exception:
        group = "unknown"
    size = stats.st_size
    mtime = datetime.fromtimestamp(stats.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    name = item.name

    return f"{output_r} {owner} {group} {size} {mtime} {name}"

def cmd_ls(args):
    """
    Выводит содержимое текущей или указанной директории.

    args: список аргументов команды ls
        - '-l' для подробного вывода
        - '-a' для вывода файлов, включая скрытые
        - '-la' для подробного вывода файлов, включая скрытые

    Вызывает ShellError, если указанный путь не является директорией.
    Создает запись в истории команд.
    """
    path = pathlib.Path().cwd()
    detailed = False
    hidden = False
    if args and '-l' in args:
        detailed = True
    if args and '-a' in args:
        hidden = True
    if args and '-la' in args:
        hidden = True
        detailed = True
    clean_args = [i for i in args if i not in ['-l', '-a', '-la']]
    if not clean_args:
        items = list(path.iterdir())
        if not hidden:
            items = [i for i in items if not i.name.startswith('.')]
        if items and not detailed:
            max_len = max(len(item.name) for item in items)
            for i, item in enumerate(sorted(items)):
                print(f"{item.name:<{max_len}}", end="  ")
                if (i + 1) % 5 == 0:
                    print()
            print()
        for item in sorted(items):
            if detailed:
                print(cmd_ls_detailed_info(item))


    if clean_args:
        for path in clean_args:
            p = ensure_exists(normalize(path),"ls")
            if p.is_dir():
                if len(args) > 1:
                    print(f"{p}: ")
                items = list(p.iterdir())
                if not hidden:
                    items = [i for i in list(p.iterdir()) if not i.name.startswith('.')]
                if items and not detailed:
                    max_len = max(len(item.name) for item in items)
                    for i, item in enumerate(sorted(items)):
                        print(f"{item.name:<{max_len}}", end="  ")
                        if (i + 1) % 5 == 0:
                            print()
                    print()
                for item in sorted(items):
                    if detailed:
                        print(cmd_ls_detailed_info(item))
            else:
                raise ShellError(f"ls: '{p}' is not a directory")
    last_cmd_num = get_last_history_number() + 1
    record = {"cmd":"ls","number":last_cmd_num,"user_input": "ls " + " ".join(args)}
    create_history_record(record)
