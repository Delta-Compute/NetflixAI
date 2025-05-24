import importlib.util
import pytest

bittensor_missing = importlib.util.find_spec("bittensor") is None
if bittensor_missing:
    pytest.skip("bittensor not installed", allow_module_level=True)

from template import protocol

@pytest.mark.skipif(bittensor_missing, reason="bittensor not installed")
def test_video_submission_status_enum():
    assert protocol.VideoSubmissionStatus.PENDING.value == "pending"


@pytest.mark.skipif(bittensor_missing, reason="bittensor not installed")
def test_video_metadata_fields():
    meta = protocol.VideoMetadata(ipfs_hash="abc")
    assert meta.ipfs_hash == "abc"


@pytest.mark.skipif(bittensor_missing, reason="bittensor not installed")
def test_social_post_synapse():
    syn = protocol.SocialPostSynapse(submission_id="s", post_id="p", platform="x")
    assert syn.post_id == "p"
