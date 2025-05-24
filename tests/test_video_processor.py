from utils.video_processor import VideoProcessor


def test_validate_format():
    vp = VideoProcessor()
    assert vp.validate_format("video.mp4", ["mp4", "mov"])
    assert not vp.validate_format("video.avi", ["mp4"]) 
