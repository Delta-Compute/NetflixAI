import time
import pytest

benchmark_missing = False
try:
    import pytest_benchmark  # noqa: F401
except Exception:
    benchmark_missing = True
    pytest.skip("pytest-benchmark not installed", allow_module_level=True)

def test_dummy_benchmark(benchmark):
    @benchmark
    def _():
        time.sleep(0.01)
