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