import shutil

from errors.shell_errors import ShellError
from src.history import get_last_history_undo_cmd, remove_history_records, get_last_history_number, \
    create_history_record
from src.utils import normalize


def undo_cp(dest):
    """
    Отменяет команду cp, удаляя скопированный файл или директорию.

    dest: путь к скопированному файлу или директории
    """
    dest = normalize(dest)
    if dest.is_file():
        dest.unlink()
    if dest.is_dir():
        shutil.rmtree(dest)

def undo_rm(trash_path,src):
    """
    Отменяет команду rm, возвращая файл или директорию из корзины.

    trash_path: путь в корзине, куда был перемещён файл
    src: исходный путь, куда нужно восстановить файл

    Вызывает ShellError, если файл полностью удалён и восстановить его нельзя.
    """
    trash_path = normalize(trash_path)
    src = normalize(src)
    if not trash_path.exists():
        raise ShellError("undo: this file/directory was completely deleted; can't undo")
    else:
        shutil.move(trash_path, src)

def undo_mv(src,dest):
    """
    Отменяет команду mv, перемещая файл или директорию обратно на исходное место.

    src: исходный путь, куда нужно вернуть файл
    dest: путь к текущему местоположению файла

    Вызывает ShellError, если файл был изменён или удалён после перемещения.
    """
    src = normalize(src)
    dest = normalize(dest)
    if not dest.exists():
        raise ShellError(f"undo: moved file '{dest}' was changed or deleted; can't undo")
    shutil.move(dest, src)

def cmd_undo(args):
    """
    Отменяет последнюю выполненную команду cp, rm или mv.

    args: список аргументов команды undo (должен быть пустым или содержать только 'undo')

    Вызывает ShellError, если передано больше одного аргумента.
    Обновляет историю команд после отмены.
    """
    if len(args) > 1:
        raise ShellError(f"undo: too many arguments: '{args}'. This command can only be used with 'undo'")
    last_cmd = get_last_history_undo_cmd()
    showed_info = False
    if not last_cmd:
        raise ShellError("undo: nothing to undo")
    for data in last_cmd:
        if data['cmd'] == 'cp':
            undo_cp(data['dest'])
            remove_history_records(data['number'])
        if data['cmd'] == 'rm' and "skipped" not in data:
            undo_rm(data['trash_path'],data['src'])
            remove_history_records(data['number'])
        elif data['cmd'] == 'rm':
            remove_history_records(data['number'])
        if data['cmd'] == 'mv':
            undo_mv(data['src'],data['dest'])
            remove_history_records(data['number'])
        if not showed_info:
            record = {"cmd":"undo", "number":get_last_history_number()+1,"user_input":"undo"}
            create_history_record(record)
            print(f"undo: cancelled command '{data["user_input"]}'")
            showed_info = True
