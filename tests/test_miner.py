import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from neurons.miner import Miner


def test_miner_init():
    miner = Miner(config=type("Cfg", (), {})())
    assert miner.ipfs is not None
