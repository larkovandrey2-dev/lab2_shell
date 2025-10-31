import os
import re

from errors.shell_errors import ShellError
from src.history import create_history_record, get_last_history_number
from src.utils import normalize


def search_in_file(path,pattern_re):
    """
    Ищет строки в файле, которые соответствуют регулярному выражению.

    path: путь к файлу
    pattern_re: объект re.Pattern для поиска

    Возвращает генератор кортежей (номер_строки, строка).
    """
    try:
        with open(path,"r",encoding='utf-8') as f:
            for i,line in enumerate(f,1):
                if pattern_re.search(line):
                    yield i, line.rstrip("\n")
    except Exception:
        return

def cmd_grep(args):
    """
    Ищет строки, содержащие шаблон, в файлах или директориях.

    args: список аргументов команды grep
        - '-r' для рекурсивного поиска в директориях
        - '-i' для игнорирования регистра
        - первый аргумент без флагов: шаблон
        - второй аргумент без флагов: путь к файлу или директории

    Вызывает ShellError при:
        - недостаточном количестве аргументов
        - некорректном регулярном выражении
        - неверном пути
    Создает запись в истории команд.
    """
    if len(args) < 2:
        raise ShellError("Usage: grep [-r] [-i] <pattern> <path>")
    recursive = '-r' in args
    ignore_case = '-i' in args
    without_flags = [i for i in args if i not in ['-r','-i']]
    pattern = without_flags[0]
    path = normalize(without_flags[1])
    try:
        pattern_re = re.compile(pattern, re.IGNORECASE if ignore_case else 0)
    except re.error:
        raise ShellError(f"grep: invalid pattern '{pattern}'")
    if path.is_file():
        for ln,text in search_in_file(path,pattern_re):
            output = f"{path}:{ln}: {text}"
            print(output)
    elif path.is_dir():
        if recursive:
            for root, dirs, files in os.walk(path):
                for filename in files:
                    file_path = path / filename
                    if file_path.is_file():
                        for ln, text in search_in_file(file_path, pattern_re):
                            output = f"{file_path}:{ln}: {text}"
                            print(output)
    else:
        raise ShellError(f"grep: invalid path '{path}'")
    record = {"cmd": "grep","user_input": "grep " + " ".join(args), "number": get_last_history_number() + 1}
    create_history_record(record)
