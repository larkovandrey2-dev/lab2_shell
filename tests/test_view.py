import pytest

from src.commands.viewer import cmd_cd,cmd_cat,cmd_history
from errors.shell_errors import ShellError
from src.history import create_history_record
import pathlib
from src.utils import normalize

def test_cd(temp_dir,mock_create_history_record):
    temp_path = normalize(temp_dir)
    src_dir = temp_path / "src"
    src_dir.mkdir()
    old_dir = pathlib.Path().cwd()
    cmd_cd([str(src_dir)])
    assert pathlib.Path().cwd() == src_dir
    cmd_cd([str(old_dir)])

def test_cd_invalid_path():
    with pytest.raises(ShellError):
        cmd_cd([str("/unknown/path/test")])

def test_cat(temp_dir,capsys,mock_create_history_record):
    temp_path = normalize(temp_dir)
    file_p = temp_path / "file.txt"
    file_p.write_text("test text")
    cmd_cat([str(file_p)])
    output = capsys.readouterr()
    assert output.out == "test text\n"

def test_cat_multiple(temp_dir,capsys,mock_create_history_record):
    temp_path = normalize(temp_dir)
    f1 = temp_path / "file1.txt"
    f2 = temp_path / "file2.txt"
    f1.write_text("test1")
    f2.write_text("test2")
    cmd_cat([str(f1), str(f2)])
    output = capsys.readouterr()
    assert "test1" in output.out and "test2" in output.out

def test_history_records(capsys,mock_history_path):
    create_history_record({
         "cmd": "cp",
         "user_input": "cp 123 33.txt",
         "src": "123",
         "dest": "33.txt",
         "number": 1
     })
    create_history_record({
         "cmd": "mv",
         "user_input": "mv 88 33.txt",
         "src": "88",
         "dest": "33.txt",
         "number": 2
     })
    cmd_history([])
    output = capsys.readouterr().out
    assert "mv 88 33.txt" in output and "cp 123 33.txt" in output
def test_history_records_multiple(capsys,mock_history_path):
    for i in range(2):
        create_history_record({
            "cmd": "cp",
            "user_input": f"cp {i} {i}.txt",
            "number": i
        })
    cmd_history(['2'])
    output = capsys.readouterr().out
    assert "cp 0 0.txt" in output
    assert "cp 1 1.txt" in output
    assert "cp 2 2.txt" not in output
