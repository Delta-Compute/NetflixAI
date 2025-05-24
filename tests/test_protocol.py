import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from template.protocol import VideoSubmissionStatus

def test_submission_status():
    assert VideoSubmissionStatus.FAILED.value == "failed"
