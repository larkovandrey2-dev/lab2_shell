import tarfile
from pathlib import Path

from errors.shell_errors import ShellError
from src.history import create_history_record, get_last_history_number
from src.utils import normalize


def cmd_tar(args):
    """
    Создает tar.gz архив из указанной директории.

    args: список аргументов команды tar
        - args[0]: путь к директории для архивации
        - args[1]: путь и имя создаваемого архива (.tar.gz)

    Вызывает ShellError при:
        - неправильном количестве аргументов
        - если исходная директория не существует
        - при ошибках создания архива
    Создает запись в истории команд.
    """
    if len(args) != 2:
        raise ShellError("Usage: tar <folder> <archive.tar.gz>")

    src = normalize(args[0])
    dest = normalize(args[1])
    if not src.exists() or not src.is_dir():
        raise ShellError(f"tar: {src} is not a directory")

    try:
        with tarfile.open(dest, "w:gz") as tf:
            tf.add(str(src), arcname=src.name)
        record = {
            "cmd": "tar",
            "number": get_last_history_number() + 1,
            "user_input": "tar " + " ".join(args),
        }
        create_history_record(record)
    except Exception as e:
        raise ShellError(f"tar: error: {e}")


def cmd_untar(args):
    """
    Распаковывает tar.gz архив в текущую директорию.

    args: список аргументов команды untar
        - args[0]: путь к архиву (.tar.gz)

    Вызывает ShellError при:
        - неправильном количестве аргументов
        - если архив не найден
        - при ошибках распаковки
    Создает запись в истории команд.
    """
    if len(args) != 1:
        raise ShellError("Usage: untar <archive.tar.gz>")

    archive = Path(args[0])
    if not archive.exists():
        raise ShellError(f"untar: {archive} not found")

    try:
        with tarfile.open(archive, "r:gz") as tf:
            tf.extractall(Path().cwd())
        record = {
            "cmd": "untar",
            "num": get_last_history_number() + 1,
            "user_input": " ".join(["untar", str(archive)]),
            "status": "OK"
        }
        create_history_record(record)
    except Exception as e:
        raise ShellError(f"untar: error: {e}")
