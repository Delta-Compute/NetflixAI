import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from neurons.validator import Validator


def test_validator_init():
    val = Validator(config=type("Cfg", (), {})())
    assert val.ipfs is not None
