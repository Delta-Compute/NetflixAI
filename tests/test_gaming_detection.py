from utils.gaming_detection import GamingDetector

def test_detect_normal():
    detector = GamingDetector(like_view_ratio_threshold=0.5)
    metrics = {"views": 100, "likes": 40}
    assert not detector.detect(metrics)


def test_detect_gaming():
    detector = GamingDetector(like_view_ratio_threshold=0.5)
    metrics = {"views": 10, "likes": 9}
    assert detector.detect(metrics)
