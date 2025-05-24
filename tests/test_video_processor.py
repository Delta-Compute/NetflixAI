import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils.video_processor import VideoProcessor

def test_validate_format():
    vp = VideoProcessor()
    assert vp.validate_format("movie.mp4", ["mp4", "mkv"])
    assert not vp.validate_format("movie.avi", ["mp4"])
