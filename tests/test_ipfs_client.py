import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.ipfs_client import IPFSClient

def test_init():
    client = IPFSClient("http://localhost:5001")
    assert client.gateway_url == "http://localhost:5001"
