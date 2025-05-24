import time

def test_dummy_benchmark(benchmark):
    @benchmark
    def _():
        time.sleep(0.01)
