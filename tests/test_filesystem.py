from src.commands.filesystem import cmd_rm,cmd_cp,cmd_mv
from src.utils import normalize,ensure_exists
from unittest.mock import patch

def test_cp(temp_dir, mock_create_history_record):
    temp_path = normalize(temp_dir)
    src = temp_path / "src_file.txt"
    src.write_text("test text")
    dest = temp_path / "src_copy.txt"
    cmd_cp([str(src), str(dest)])
    assert ensure_exists(dest, "cp")
    assert dest.read_text() == "test text"


def test_cp_recursive(temp_dir,mock_create_history_record):
    temp_path = normalize(temp_dir)
    src = temp_path / "src_dir"
    src.mkdir()
    (src / "file.txt").write_text("test text")
    dest = temp_path / "src_dir_copied"
    cmd_cp([str(src), str(dest), "-r"])
    assert (dest / "file.txt").exists()
def test_mv(temp_dir,mock_create_history_record):
    temp_path = normalize(temp_dir)
    src = temp_path / "src_file.txt"
    src.write_text("test text")
    dest = temp_path / "src_move.txt"
    cmd_mv([str(src), str(dest)])
    assert ensure_exists(dest, "mv")
    assert not src.exists()
    assert dest.read_text() == "test text"

def test_rm(temp_dir,mock_create_history_record, mock_trash):
    temp_path = normalize(temp_dir)
    src = temp_path / "src_file.txt"
    src.write_text("test text")
    with patch("builtins.input",return_value="y"):
        cmd_rm([str(src)])
    assert not src.exists()

def test_rm_recursive(temp_dir, mock_create_history_record, mock_trash):
    temp_path = normalize(temp_dir)
    src = temp_path / "src_dir"
    src.mkdir()
    (src / "file.txt").write_text("test text")
    with patch("builtins.input",return_value="y"):
        cmd_rm([str(src),"-r"])
    assert not src.exists()

def test_rm_without_ask(temp_dir, mock_create_history_record, mock_trash):
    temp_path = normalize(temp_dir)
    src = temp_path / "src_file.txt"
    src.write_text("test text")
    cmd_rm([str(src),"-f"])
    assert not src.exists()
