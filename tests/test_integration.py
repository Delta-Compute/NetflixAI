import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.ipfs_client import IPFSClient
from utils.storage_manager import StorageManager


def test_integration_tmp(tmp_path):
    sm = StorageManager(root=tmp_path)
    ipfs = IPFSClient("http://localhost:5001")
    assert ipfs.gateway_url
    assert sm.root == tmp_path
