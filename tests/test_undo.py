from src.utils import normalize
from src.commands.undo import cmd_undo
from src.commands.filesystem import cmd_cp,cmd_mv,cmd_rm
from unittest.mock import patch


def test_undo_cp(temp_dir,mock_history_path):
    temp_path = normalize(temp_dir)
    src1 = temp_path / "file1.txt"
    src1.write_text("test")
    dest1 = temp_path / "file1_copy.txt"

    cmd_cp([str(src1),str(dest1)])
    assert dest1.exists()
    cmd_undo([])
    assert not dest1.exists()

def test_undo_cp_multi(temp_dir,mock_history_path):
    temp_path = normalize(temp_dir)
    src1 = temp_path / "file1.txt"
    src1.write_text("test1")
    src2 = temp_path / "file2.txt"
    src2.write_text("test2")
    dest = temp_path / "copy_dir"
    dest.mkdir()
    cmd_cp(["-r",str(src1),str(src2),str(dest)])
    cmd_undo([])
    assert not (dest/src1.name).exists()
    assert not (dest/src2.name).exists()

def test_undo_mv(temp_dir,mock_history_path):
    temp_path = normalize(temp_dir)
    src1 = temp_path / "file1.txt"
    src1.write_text("test1")
    dest1 = temp_path / "file1_moved.txt"
    cmd_mv([str(src1),str(dest1)])
    assert dest1.exists() and (not src1.exists())
    cmd_undo([])
    assert not (dest1.exists()) and src1.exists()
def test_undo_rm(temp_dir,mock_history_path,mock_trash):
    temp_path = normalize(temp_dir)
    src1 = temp_path / "file1.txt"
    src1.write_text("test1")
    with patch("builtins.input",return_value="y"):
        cmd_rm([str(src1)])
    assert not src1.exists()
    cmd_undo([])
    assert src1.exists()
