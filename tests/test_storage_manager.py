import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.storage_manager import StorageManager
import os
import tempfile


def test_store_and_get(tmp_path):
    sm = StorageManager(root=tmp_path, max_size=1024)
    temp_file = tmp_path / "foo.txt"
    temp_file.write_text("data")
    sm.store_file(str(temp_file))
    assert sm.get_file("foo.txt")
