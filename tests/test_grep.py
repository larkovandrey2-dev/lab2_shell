
from src.utils import normalize
from src.commands import cmd_grep

def test_grep_basic(temp_dir, capsys,mock_create_history_record):
    temp_path = normalize(temp_dir)
    src = temp_path / "file.txt"
    src.write_text("Hello \n hellow test")
    cmd_grep(["Hello",str(src)])
    output = capsys.readouterr().out
    assert "Hello" in output

def test_grep_flag_ignore_case(temp_dir, capsys, mock_create_history_record):
    temp_path = normalize(temp_dir)
    src1 = temp_path / "file.txt"
    src1.write_text("Hello \n test")
    cmd_grep(["-i","hello",str(src1)])
    output = capsys.readouterr().out
    assert "Hello" in output
def test_grep_flag_recursive(temp_dir, capsys, mock_create_history_record):
    temp_path = normalize(temp_dir)
    src1 = temp_path / "dir1"
    src1.mkdir()
    (src1 / "file1.txt").write_text("Hello1 \n test")
    (src1 / "file2.txt").write_text("Hello2 \n test")
    cmd_grep(["-r","Hello",str(src1)])
    output = capsys.readouterr().out
    assert "Hello1" in output
    assert "Hello2" in output
