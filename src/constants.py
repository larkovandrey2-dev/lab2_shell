import pathlib
RIGHTS = {4:'r',2:'w',1:'x'}
ROOT_DIR = pathlib.Path(__file__).resolve().parent
PROJECT_ROOT = ROOT_DIR.parent
TRASH_PATH = PROJECT_ROOT / "src" / ".trash"
HISTORY_PATH = PROJECT_ROOT / "src" / ".history"
LOG_FILE = PROJECT_ROOT / "src" / "shell.log"
TRASH_PATH.mkdir(exist_ok=True)
