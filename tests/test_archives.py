import pathlib
from src.commands import cmd_zip, cmd_unzip, cmd_tar, cmd_untar
from src.utils import normalize
import os
def create_test_structure(base):
    base_p = normalize(base)
    base_p.mkdir()
    os.chdir(base_p)
    (base_p / "file1.txt").write_text("file1")
    (base_p / "file2.txt").write_text("file2")
    sub_dir = base_p / "subdir"
    sub_dir.mkdir()
    (sub_dir / "file3.txt").write_text("file3")
    return base_p

def compare_dirs_content(path1,path2):
    for p in path1.rglob("*"):
        rel = p.relative_to(path1)
        p2 = path2 / rel
        assert p2.exists()
        if p.is_file():
            assert p.read_text() == p2.read_text()

def test_zip_unzip(temp_dir,mock_create_history_record):
    project_cwd = os.getcwd()
    base = create_test_structure(str(normalize(temp_dir) / "src"))
    dest_arch = normalize(str(normalize(temp_dir) / "archive.zip"))
    cmd_zip([str(base),str(dest_arch)])
    assert dest_arch.exists()
    extract_dir = normalize(str(normalize(temp_dir) / "extracted"))
    extract_dir.mkdir()
    os.chdir(extract_dir)
    cmd_unzip([str(dest_arch)])
    extracted_base = pathlib.Path(temp_dir) / base.name
    assert extracted_base.exists()
    compare_dirs_content(base, extracted_base)
    os.chdir(project_cwd)
def test_tar_and_untar(temp_dir, mock_create_history_record):
    project_cwd = os.getcwd()
    base = create_test_structure(normalize(temp_dir) / "src_tar")
    archive = normalize(temp_dir) / "archive.tar.gz"
    cmd_tar([str(base), str(archive)])
    assert archive.exists()
    extract_dir = normalize(temp_dir) / "extracted_tar"
    extract_dir.mkdir()
    os.chdir(extract_dir)
    cmd_untar([str(archive)])
    extracted_base = pathlib.Path(temp_dir) / base.name
    assert extracted_base.exists()
    compare_dirs_content(base, extracted_base)
    os.chdir(project_cwd)
