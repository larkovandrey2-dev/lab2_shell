import getpass
import logging
import pathlib
import shlex
import socket

import src.commands as com
from errors.shell_errors import ShellError

commands = {
    "ls": com.cmd_ls,
    "pwd": com.cmd_pwd,
    "cd": com.cmd_cd,
    "cat": com.cmd_cat,
    "cp": com.cmd_cp,
    "mv": com.cmd_mv,
    "rm": com.cmd_rm,
    "history": com.cmd_history,
    "undo": com.cmd_undo,
    "zip": com.cmd_zip,
    "unzip": com.cmd_unzip,
    "tar": com.cmd_tar,
    "untar": com.cmd_untar,
    "grep": com.cmd_grep,
}

logging.basicConfig(
    filename='shell.log',
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


if __name__ == "__main__":
    host = socket.gethostname()
    user = getpass.getuser()
    while True:
        cwd = str(pathlib.Path.cwd()).replace(str(pathlib.Path().home()),"~")
        user_input = input(f"{user}@{host}:{cwd}$ ")
        command = shlex.split(user_input)
        if command and command[0] in commands:
            try:
                commands[command[0]](command[1:])
                logging.info(f"SUCCESS: {user_input}")
            except ShellError as e:
                print(e)
                logging.error(f"ERROR: {e}")
            except Exception as e:
                print("mini-shell: system error")
                logging.error(f"ERROR: {command}: {e}")
        elif not command:
            continue
        else:
            print(f'{user_input}: unknown command')
            logging.error(f"ERROR: {user_input} is not a valid command")
