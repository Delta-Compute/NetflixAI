# The MIT License (MIT)
# Copyright © 2024 Your Organization

import typing
from enum import Enum
import bittensor as bt
from pydantic import Field


class VideoSubmissionStatus(Enum):
    """Status values for video submission lifecycle."""
    PENDING = "pending"
    VALIDATING = "validating"
    COMPLETED = "completed"
    FAILED = "failed"


class VideoMetadata(bt.Synapse):
    """Metadata information for a submitted video."""

    ipfs_hash: str = Field("", title="IPFS Hash", frozen=False)
    post_id: str = Field("", title="Post ID", frozen=False)
    platform: str = Field("", title="Platform", frozen=False)
    title: str = Field("", title="Title", frozen=False)
    description: str = Field("", title="Description", frozen=False)
    duration_seconds: int = Field(0, title="Duration Seconds", frozen=False)
    file_size_bytes: int = Field(0, title="File Size Bytes", frozen=False)
    mime_type: str = Field("", title="MIME Type", frozen=False)

VideoMetadata.required_hash_fields = ["ipfs_hash"]

class QuerySynapse(bt.Synapse):
    """
    A basic query synapse for subnet communication.
    Modify this based on your subnet's specific needs.
    """
    query: str = Field("", title="Query", frozen=False)
    response: typing.Dict = Field(default_factory=dict, title="Response", frozen=False)
    successfully_processed: bool = Field(False, title="Successfully Processed", frozen=False)
    error_message: str = Field("", title="Error Message", frozen=False)
    computed_body_hash: str = Field("", title="Computed Body Hash", frozen=False)

QuerySynapse.required_hash_fields = ["query"]

class DataSynapse(bt.Synapse):
    """
    A synapse for exchanging data between neurons.
    Customize fields based on your subnet requirements.
    """
    data: typing.List[typing.Dict] = Field(default_factory=list, title="Data", frozen=False)
    metadata: typing.Dict = Field(default_factory=dict, title="Metadata", frozen=False)
    successfully_processed: bool = Field(False, title="Successfully Processed", frozen=False)
    error_message: str = Field("", title="Error Message", frozen=False)
    computed_body_hash: str = Field("", title="Computed Body Hash", frozen=False)

DataSynapse.required_hash_fields = ["data"]


class VideoSubmissionSynapse(bt.Synapse):
    """Synapse for submitting video data."""

    video_metadata: VideoMetadata = Field(
        default_factory=VideoMetadata,
        title="Video Metadata",
        frozen=False,
    )
    submission_id: str = Field("", title="Submission ID", frozen=False)
    miner_uid: int = Field(0, title="Miner UID", frozen=False)
    timestamp: float = Field(0.0, title="Timestamp", frozen=False)
    status: VideoSubmissionStatus = Field(
        VideoSubmissionStatus.PENDING,
        title="Status",
        frozen=False,
    )
    successfully_processed: bool = Field(False, title="Successfully Processed", frozen=False)
    error_message: str = Field("", title="Error Message", frozen=False)
    computed_body_hash: str = Field("", title="Computed Body Hash", frozen=False)

VideoSubmissionSynapse.required_hash_fields = ["submission_id"]
class EngagementMetricsSynapse(bt.Synapse):
    """Synapse for retrieving engagement metrics."""
    post_id: str = Field("", title="Post ID", frozen=False)
    platform: str = Field("", title="Platform", frozen=False)
    views: int = Field(0, title="Views", frozen=False)
    likes: int = Field(0, title="Likes", frozen=False)
    comments: int = Field(0, title="Comments", frozen=False)
    shares: int = Field(0, title="Shares", frozen=False)
    engagement_rate: float = Field(0.0, title="Engagement Rate", frozen=False)
    timestamp: float = Field(0.0, title="Timestamp", frozen=False)
    successfully_processed: bool = Field(False, title="Successfully Processed", frozen=False)
    error_message: str = Field("", title="Error Message", frozen=False)
    computed_body_hash: str = Field("", title="Computed Body Hash", frozen=False)

EngagementMetricsSynapse.required_hash_fields = ["post_id", "platform"]



class VideoValidationSynapse(bt.Synapse):
    """Synapse for validation of submitted videos."""
    submission_id: str = Field("", title="Submission ID", frozen=False)
    validation_type: str = Field("", title="Validation Type", frozen=False)
    validation_result: str = Field("", title="Validation Result", frozen=False)
    score: float = Field(0.0, title="Score", frozen=False)
    successfully_processed: bool = Field(False, title="Successfully Processed", frozen=False)
    error_message: str = Field("", title="Error Message", frozen=False)
    computed_body_hash: str = Field("", title="Computed Body Hash", frozen=False)

VideoValidationSynapse.required_hash_fields = ["submission_id"]
