import importlib.util
import pytest

bittensor_missing = importlib.util.find_spec("bittensor") is None

@pytest.mark.skipif(bittensor_missing, reason="bittensor not installed")
def test_validator_import():
    import neurons.validator as v
    assert hasattr(v, "Validator")
