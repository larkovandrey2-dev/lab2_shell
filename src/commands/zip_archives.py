import os
import pathlib
import zipfile

from errors.shell_errors import ShellError
from src.history import create_history_record, get_last_history_number
from src.utils import ensure_exists, normalize


def cmd_zip(args):
    """
    Создает zip-архив из указанной директории.

    args: список аргументов команды zip
        - args[0]: путь к директории для архивации
        - args[1]: путь и имя создаваемого архива (.zip)

    Вызывает ShellError при:
        - неправильном количестве аргументов
        - если исходная директория не существует
        - если указанный путь не является директорией
        - при ошибках создания архива

    Создает запись в истории команд.
    """
    if len(args) != 2:
        raise ShellError("Usage: zip <folder> <archive.zip>")
    src = ensure_exists(normalize(args[0]),"zip")
    dest = normalize(args[1])
    if not src.is_dir():
        raise ShellError(f"zip: {src} is not a directory")
    try:
        with zipfile.ZipFile(dest, "w", zipfile.ZIP_DEFLATED) as zf:
            for root, _, files in os.walk(src):
                for file in files:
                    full_p = pathlib.Path(root) / file
                    archive_p = full_p.relative_to(src)
                    zf.write(full_p, archive_p)
        last_cmd_number = get_last_history_number() + 1
        record = {"cmd": "zip", "src": str(src), "user_input": "zip " + " ".join(args), "number": last_cmd_number}
        create_history_record(record)
    except Exception as e:
        raise ShellError(f"zip: {e}")

def cmd_unzip(args):
    """
    Распаковывает zip-архив в текущую директорию.

    args: список аргументов команды unzip
        - args[0]: путь к архиву (.zip)

    Вызывает ShellError при:
        - неправильном количестве аргументов
        - если архив не существует
        - при ошибках распаковки

    Создает запись в истории команд.
    """
    if len(args) != 1:
        raise ShellError("Usage: unzip <archive.zip>")
    archive_path = ensure_exists(normalize(args[0]),"unzip")

    try:
        with zipfile.ZipFile(archive_path, "r") as zf:
            zf.extractall(pathlib.Path.cwd())
        last_cmd_number = get_last_history_number() + 1
        record = {"cmd": "unzip", "src": str(archive_path), "number": last_cmd_number, "user_input": "unzip " + " ".join(args)}
        create_history_record(record)
    except Exception as e:
        raise ShellError(f"unzip: {e}")
