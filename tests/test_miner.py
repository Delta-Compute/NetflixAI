import importlib.util
import pytest

bittensor_missing = importlib.util.find_spec("bittensor") is None

@pytest.mark.skipif(bittensor_missing, reason="bittensor not installed")
def test_miner_import():
    import neurons.miner as m
    assert hasattr(m, "Miner")
