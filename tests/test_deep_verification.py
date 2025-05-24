from utils.deep_verification import DeepVerificationPipeline


def test_pipeline_basic():
    pipeline = DeepVerificationPipeline()
    result = pipeline.verify_post("post", "youtube", "user")
    assert set(result.keys()) == {"tag_valid", "history_analyzed", "gaming_detected"}
