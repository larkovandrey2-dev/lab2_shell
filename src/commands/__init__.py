from .filesystem import cmd_cp, cmd_mv, cmd_rm
from .grep import cmd_grep
from .info import cmd_ls, cmd_pwd
from .tar_archives import cmd_tar, cmd_untar
from .undo import cmd_undo
from .viewer import cmd_cat, cmd_cd, cmd_history
from .zip_archives import cmd_unzip, cmd_zip

commands = {
    "cp": cmd_cp,
    "mv": cmd_mv,
    "rm": cmd_rm,
    "ls": cmd_ls,
    "pwd": cmd_pwd,
    "cd": cmd_cd,
    "cat": cmd_cat,
    "history": cmd_history,
    "undo": cmd_undo,
    "zip": cmd_zip,
    "unzip": cmd_unzip,
    "tar": cmd_tar,
    "untar": cmd_untar,
    "grep": cmd_grep,
}

__all__ = [
    "commands",
]
