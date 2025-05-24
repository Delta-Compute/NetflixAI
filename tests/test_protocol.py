from template import protocol

def test_video_submission_status_enum():
    assert protocol.VideoSubmissionStatus.PENDING.value == "pending"


def test_video_metadata_fields():
    meta = protocol.VideoMetadata(ipfs_hash="abc")
    assert meta.ipfs_hash == "abc"
