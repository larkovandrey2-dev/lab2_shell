import pathlib
import shutil

from errors.shell_errors import ShellError
from src.history import create_history_record, get_last_history_number
from src.utils import ensure_exists, move_to_trash, normalize


def cmd_cp(args):
    """
    Копирует файлы или каталоги.

    args: список аргументов команды cp.
        Если указан '-r', копируется директория.

    Вызывает ошибку ShellError при неправильных аргументах или попытке копирования директории без '-r'.
    Создает запись в истории команд.
    """
    clean_args = [i for i in args if i != '-r']

    if len(clean_args) < 2:
        raise ShellError(f"cp: not enough arguments: '{args}'")
    if len(clean_args) > 2:
        dest = normalize(clean_args[-1])
        if not dest.is_dir():
            raise ShellError(f"cp: not a directory: '{dest}'")
        last_cmd_number = get_last_history_number() + 1
        for p in clean_args[:-1]:
            src = ensure_exists(normalize(p), "cp")
            if src.is_dir() and '-r' not in args:
                raise ShellError(f"cp: is a directory: '{src}'. Use -r option.")
            elif src.is_dir():
                target = dest / src.name
                if target.exists():
                    raise ShellError(f"cp: destination directory '{target}' already exists.")
                shutil.copytree(src, target)

            else:
                shutil.copy(src, dest / src.name)
            record = {"cmd": "cp", "src": str(src), "dest": str(dest / src.name),
                      "user_input": "cp " + " ".join(args), "number": last_cmd_number, "multi": len(clean_args)-1}
            create_history_record(record)
    else:
        if '-r' in args:
            src = ensure_exists(normalize(clean_args[0]), "cp")
            dest = normalize(clean_args[1])
            if src.is_dir() and dest.exists() and dest.is_file():
                raise ShellError(f"cp: cannot overwrite non-directory '{dest}' with directory '{src}'")
            try:
                if src.is_dir() and dest.resolve().is_relative_to(src.resolve()):
                    raise ShellError(f"cp: cannot copy a directory, '{src}', into itself, '{dest}'")
            except Exception:
                pass
            if dest.exists() and dest.is_dir():
                dest = dest / src.name

            if src == dest:
                raise ShellError(f"cp: '{src}' and '{dest}' are identical (not copied).")
            if not dest.parent.exists():
                raise ShellError(f"cp: no such directory: '{dest}'")
            if not src.is_dir():
                shutil.copy(src, dest)
                last_cmd_number = get_last_history_number() + 1
                record = {"cmd": "cp", "src": str(src), "dest": str(dest), "is_dir": False,
                          "user_input": "cp " + " ".join(args), "number": last_cmd_number}
                create_history_record(record)
            else:
                if dest.exists():
                    raise ShellError(f"cp: destination directory '{dest}' already exists.")
                shutil.copytree(src, dest)
                last_cmd_number = get_last_history_number() + 1
                record = {"cmd": "cp", "src": str(src), "dest": str(dest), "is_dir": True,
                          "user_input": "cp " + " ".join(args), "number": last_cmd_number}
                create_history_record(record)

        else:
            src = ensure_exists(normalize(args[0]), "cp")
            dest = pathlib.Path(args[1]).expanduser().resolve()
            if src.is_dir():
                raise ShellError(f"cp: is a directory: '{src}'. Use -r option.")
            shutil.copy(src, dest)
            last_cmd_number = get_last_history_number() + 1
            record = {"cmd": "cp", "src": str(src), "dest": str(dest), "is_dir": False,
                      "user_input": "cp " + " ".join(args), "number": last_cmd_number}
            create_history_record(record)


def cmd_mv(args):
    """
        Перемещает файлы или каталоги.

        args: список аргументов команды mv.
            Последний аргумент — путь назначения.

        Вызывает ShellError при ошибках аргументов или при попытке перемещения директории в саму себя.
        Создает запись в истории команд.
        """
    if len(args) < 2:
        raise ShellError(f"mv: not enough arguments: '{args}'")
    elif len(args) > 2:
        dest = normalize(args[-1])
        if not dest.is_dir():
            raise ShellError(f"mv: not a directory: '{dest}'")
        last_cmd_number = get_last_history_number() + 1
        for p in args[:-1]:
            src = ensure_exists(normalize(p), "mv")
            if src.is_dir():
                try:
                    if dest.relative_to(src):
                        raise ShellError(f"mv: cannot move directory into itself: '{dest}'")
                except ValueError:
                    pass
            else:
                dest = dest / src.name
            shutil.move(src, dest)
            record = {"cmd": "mv", "src": str(src), "dest": str(dest),
                      "user_input": "mv " + " ".join(args), "number": last_cmd_number, "multi": len(args)}
            create_history_record(record)
    else:
        src = ensure_exists(normalize(args[0]), "mv")
        dest = pathlib.Path(args[1]).expanduser().resolve()
        if src == dest:
            raise ShellError(f"mv: '{src}' and '{dest}' are identical (not moved).")
        if src.is_dir() and dest.is_file():
            raise ShellError(f"mv: cannot overwrite non-directory '{dest}' with directory '{src}'")
        if str(dest.resolve()).startswith(str(src.resolve()) + "/"):
            raise ShellError(f"mv: cannot move directory into itself: '{dest}'")
        if src.is_dir() and dest.is_file():
            raise ShellError(f"mv: cannot overwrite non-directory '{dest}' with directory '{src}'")
        if src.is_file() and dest.is_dir():
            dest = dest / src.name
        shutil.move(src, dest)
        last_cmd_number = get_last_history_number() + 1
        record = {"cmd": "mv", "src": str(src), "dest": str(dest),
                  "user_input": "mv " + " ".join(args), "number": last_cmd_number}
        create_history_record(record)


def cmd_rm(args):
    """
    Удаляет файлы или директории с подтверждением.

    args: список аргументов команды rm.
        Если указан '-r', можно удалять директории.
        Если указан '-f', удаление происходит без подтверждения.

    Вызывает ShellError при неправильных аргументах или попытке удалить директорию без '-r'.
    Нельзя удалять родительские ('..') и корневые ('/') каталоги.
    Перемещает файлы в корзину и создает запись в истории команд.
    """
    recursive = '-r' in args or '-rf' in args
    without_ask = '-f' in args or '-rf' in args
    clean_args = [i for i in args if i not in ['-r','-f','-rf']]
    if len(clean_args) == 0:
        raise ShellError(f"rm: not enough arguments: '{args}'")
    else:
        if not recursive:
            last_cmd_number = get_last_history_number() + 1
            for path in clean_args:
                src = ensure_exists(normalize(path), "rm")
                if src.resolve() == pathlib.Path('/'):
                    raise ShellError("rm: forbidden to delete root directory '/'")
                if src.resolve() == pathlib.Path('..').resolve():
                    raise ShellError("rm: forbidden to delete parent directory '..'")
                if src.is_dir():
                    raise ShellError(f"rm: '{src}' is a directory. Use '-r' option.")
                if src.is_file():
                    ans = 'y'
                    if not without_ask:
                        ans = input(f"rm: delete file: '{src}'? [y/n] ")
                    if ans.lower() == "y":
                        trash_path = move_to_trash(src)
                        record = {"cmd": "rm", "src": str(src), "trash_path": str(trash_path),
                                  "user_input": "rm " + " ".join(args), "number": last_cmd_number,"multi":len(clean_args)}
                        create_history_record(record)
                    else:
                        print(f"rm: skipped file: '{src}'")
                        record = {"cmd": "rm", "skipped": True, "user_input": "rm " + " ".join(args),
                                  "number": last_cmd_number,"multi": len(clean_args)}
                        create_history_record(record)
        elif '-r' in args:
            last_cmd_number = get_last_history_number() + 1
            for path in clean_args:
                src = ensure_exists(normalize(path), "rm")
                ans = 'y'
                if not without_ask:
                    ans = input(f"rm: delete file/directory: '{src}'? [y/n] ")
                if ans.lower() == "y":
                    trash_path = move_to_trash(src)
                    record = {"cmd": "rm", "src": str(src), "trash_path": str(trash_path),
                              "user_input": "rm " + " ".join(args), "number": last_cmd_number,"multi":len(clean_args)}
                    create_history_record(record)
                else:
                    print(f"rm: skipped file/directory: '{src}'")
                    record = {"cmd": "rm", "skipped": True, "user_input": "rm " + " ".join(args),
                              "number": last_cmd_number,"multi":len(clean_args)}
                    create_history_record(record)
