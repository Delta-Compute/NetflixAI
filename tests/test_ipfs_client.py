import importlib.util
import pytest

requests_missing = importlib.util.find_spec("requests") is None
if requests_missing:
    pytest.skip("requests not installed", allow_module_level=True)

from utils.ipfs_client import IPFSClient


@pytest.mark.skipif(requests_missing, reason="requests not installed")
def test_ipfs_client_cleanup(tmp_path):
    f = tmp_path / "file.txt"
    f.write_text("hello")
    client = IPFSClient("http://localhost:1234")
    client.cleanup(str(f))
    assert not f.exists()


@pytest.mark.skipif(requests_missing, reason="requests not installed")
def test_ipfs_connection_fail():
    client = IPFSClient("http://localhost:1234")
    assert client.test_connection() is False
