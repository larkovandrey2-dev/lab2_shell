import pathlib
from unittest.mock import patch
from errors.shell_errors import ShellError
from src.commands.info import cmd_pwd,cmd_ls
from src.utils.helpers import normalize

def test_pwd(capsys, mock_create_history_record):
    with patch("src.commands.info.create_history_record") as mock_create_history_record:
        mock_create_history_record.return_value = "fake history"
        cmd_pwd([])
        mock_create_history_record.assert_called()
    captured = capsys.readouterr()
    output = captured.out.strip()
    assert pathlib.Path(output).exists()

def test_ls_basic(capsys, temp_dir, mock_create_history_record):
    temp_path = normalize(temp_dir)
    (temp_path / "referat.txt").write_text("my text")
    cmd_ls([str(temp_dir)])
    output = capsys.readouterr().out
    assert "referat.txt" in output

def test_ls_l_flag(capsys, temp_dir, mock_create_history_record):
    temp_path = normalize(temp_dir)
    (temp_path / "referat.txt").write_text("my text")
    cmd_ls([str(temp_path), "-l"])
    output = capsys.readouterr().out
    assert "referat.txt" in output
    assert any(right in output for right in ["r", "w", "x", "-"])

def test_ls_a_flag(capsys, temp_dir, mock_create_history_record):
    temp_path = normalize(temp_dir)
    (temp_path / ".secret").write_text("important info")
    cmd_ls([str(temp_dir), "-a"])
    output = capsys.readouterr().out
    print(output)
    assert ".secret" in output

def test_ls_la_flag(capsys, temp_dir, mock_create_history_record):
    temp_path = normalize(temp_dir)
    (temp_path / ".secret").write_text("important info")
    cmd_ls([str(temp_path), "-la"])
    output = capsys.readouterr().out
    assert ".secret" in output
    assert any(right in output for right in ["r", "w", "x", "-"])

def test_missing_dir():
    try:
        cmd_ls(["/not_existing_path"])
    except ShellError as e:
        assert "no such" in str(e)
