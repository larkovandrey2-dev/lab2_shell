import json
import pathlib

from src.constants import HISTORY_PATH


def create_history_record(record: dict):
    """
    Добавляет запись в историю команд.

    record: словарь с данными команды, например:
        {
            "cmd": "cp",
            "src": "...",
            "dest": "...",
            "number": 1,
            "user_input": "cp a b"
        }
    """
    with open(HISTORY_PATH, 'a') as f:
        f.write(json.dumps(record) + '\n')

def get_last_history_number():
    """
    Возвращает номер последней команды в истории.

    Если история пуста, возвращает 0.
    """
    data = pathlib.Path(HISTORY_PATH).read_text().splitlines()
    if not data:
        return 0
    last_number = 0
    for line in data:
        line = line.strip()
        if not line:
            continue
        cmd_data = json.loads(line)
        if "number" in cmd_data and cmd_data["number"]:
            last_number = max(int(cmd_data["number"]),last_number)
    return last_number

def get_last_history(n=10):
    """
    Возвращает последние n команд из истории.

    n: количество последних команд для вывода (по умолчанию 10)

    Возвращает список кортежей (номер_команды, user_input)
    """
    data = pathlib.Path(HISTORY_PATH).read_text().splitlines()
    res = []
    if len(data) - n - 1 < 1:
        n = len(data) - 1
    if not data:
        return res
    for i,line in enumerate(data[len(data) - n - 1:]):
        line = line.strip()
        if not line:
            continue
        cmd_data = json.loads(line)
        res.append((cmd_data["number"], cmd_data["user_input"]))
    return sorted(set(res),key=lambda x:x[0])

def get_last_history_undo_cmd():
    """
    Возвращает последнюю команду undo-доступного типа (cp, mv, rm) для отмены.

    Если команда была многокомандной (multi), возвращает все связанные записи.

    Возвращает список словарей с данными команд или None, если подходящих команд нет.
    """
    data = pathlib.Path(HISTORY_PATH).read_text().splitlines()
    res = []
    if not data:
        return []
    for i,line in enumerate(data[::-1]):
        line = line.strip()
        if not line:
            continue
        cmd_data = json.loads(line)
        if cmd_data["cmd"] not in ["rm","cp","mv"]:
            continue
        if "multi" not in cmd_data:
            res.append(cmd_data)
            return res
        else:
            multi_cmd_number = int(cmd_data["multi"])
            res.append(cmd_data)
            for bias in range(1,multi_cmd_number):
                res.append(json.loads(data[::-1][i+bias]))
            return res
    return []

def remove_history_records(number:int):
    """
    Удаляет записи истории с указанным номером команды.

    number: номер команды, которую нужно удалить
    """
    history_file = pathlib.Path(HISTORY_PATH)
    if not history_file.exists():
        return
    lines = history_file.read_text().splitlines()
    filtered = []
    for line in lines:
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if int(record.get("number", -1)) != number:
            filtered.append(line)
    history_file.write_text("\n".join(filtered) + ("\n" if filtered else ""))
