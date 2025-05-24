from utils.storage_manager import StorageManager


def test_store_and_retrieve(tmp_path):
    sm = StorageManager(str(tmp_path), max_size=1024)
    src = tmp_path / "file.txt"
    src.write_text("data")
    stored = sm.store_file(str(src))
    assert sm.get_file(src.name) == stored
    sm.delete_file(src.name)
    assert sm.get_file(src.name) is None
