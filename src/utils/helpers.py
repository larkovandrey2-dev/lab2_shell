import pathlib
import shutil
import uuid

from errors.shell_errors import ShellError
from src.constants import TRASH_PATH


def normalize(path: str) -> pathlib.Path:
    """
    Преобразует путь в абсолютный и расширяет ~ до домашней директории.

    path: строка с путем к файлу или директории

    Возвращает pathlib.Path с абсолютным путем.
    """
    return pathlib.Path(path).expanduser().resolve()

def ensure_exists(path: pathlib.Path, cmd: str):
    """
    Проверяет, что путь существует.

    path: путь к файлу или директории
    cmd: имя команды, для которой проверяется путь

    Вызывает ShellError, если путь не существует.
    Возвращает path, если проверка успешна.
    """
    if not path.exists():
        raise ShellError(f"{cmd}: no such file or directory: {path}")
    return path

def move_to_trash(src: pathlib.Path) -> pathlib.Path:
    """
    Перемещает файл или директорию в корзину.

    src: путь к файлу или директории для перемещения в корзину

    Возвращает путь к файлу в корзине.
    """
    trash_name = f"{src.name}__{uuid.uuid4()}"
    trash_target = pathlib.Path(TRASH_PATH) / trash_name
    shutil.move(src, trash_target)
    return trash_target
