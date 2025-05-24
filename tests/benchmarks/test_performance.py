import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
import time

def test_dummy_benchmark(benchmark):
    def work():
        sum(range(1000))
    benchmark(work)
