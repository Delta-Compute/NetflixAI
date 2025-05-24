from utils.ipfs_client import IPFSClient


def test_ipfs_client_cleanup(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello")
    client = IPFSClient("http://localhost:1234")
    client.cleanup(str(f))
    assert not f.exists()


def test_ipfs_connection_fail():
    client = IPFSClient("http://localhost:1234")
    assert client.test_connection() is False
