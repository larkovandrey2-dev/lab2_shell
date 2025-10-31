import pathlib
import os
import sys
import tempfile
import shutil
from unittest.mock import patch
import pytest
root = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))
import src.history as history # noqa: E402



@pytest.fixture
def temp_dir():
    temp = tempfile.mkdtemp()
    yield temp
    shutil.rmtree(temp)

@pytest.fixture()
def mock_create_history_record():
    patches = [
        patch("src.commands.filesystem.create_history_record"),
        patch("src.commands.grep.create_history_record"),
        patch("src.commands.info.create_history_record"),
        patch("src.commands.tar_archives.create_history_record"),
        patch("src.commands.undo.create_history_record"),
        patch("src.commands.viewer.create_history_record"),
        patch("src.commands.zip_archives.create_history_record"),
    ]
    mocks = [p.start() for p in patches]
    for mock in mocks:
        mock.return_value = "fake history"
    yield mocks[4]
    for p in patches:
        p.stop()

@pytest.fixture()
def mock_history_path(monkeypatch):
    import src.commands.viewer as viewer
    import src.commands.undo as undo
    tmp = tempfile.NamedTemporaryFile(delete=False)
    tmp.close()
    fake_path = tmp.name

    monkeypatch.setattr(history, "HISTORY_PATH", fake_path)
    monkeypatch.setattr(viewer, "create_history_record", history.create_history_record)
    monkeypatch.setattr(viewer, "get_last_history", history.get_last_history)
    monkeypatch.setattr(viewer, "get_last_history_number", history.get_last_history_number)
    monkeypatch.setattr(undo, "get_last_history_undo_cmd", history.get_last_history_undo_cmd)
    monkeypatch.setattr(undo, "remove_history_records", history.remove_history_records)
    monkeypatch.setattr(undo, "create_history_record", history.create_history_record)
    yield

    os.remove(fake_path)
@pytest.fixture
def mock_trash(monkeypatch):
    import src.commands.filesystem as fs  # noqa: E402
    import src.utils.helpers as helpers  # noqa: E402
    tmp_trash = tempfile.mkdtemp()
    monkeypatch.setattr(helpers, "TRASH_PATH", tmp_trash)
    monkeypatch.setattr(fs, "move_to_trash", helpers.move_to_trash)
