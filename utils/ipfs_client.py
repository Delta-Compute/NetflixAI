"""IPFS client utilities for uploading and downloading files."""

from __future__ import annotations

import os
import time
import requests
from typing import Optional, Callable, Iterator


class IPFSClient:
    """Simple IPFS client wrapper."""

    def __init__(self, gateway_url: str):
        self.gateway_url = gateway_url.rstrip("/")

    def upload_file(self, file_path: str) -> Optional[str]:
        """Upload a file to the IPFS gateway and return the hash."""
        if not os.path.isfile(file_path):
            raise FileNotFoundError(file_path)
        def _reader(fp: str, chunk_size: int = 1024 * 1024) -> Iterator[bytes]:
            with open(fp, "rb") as f:
                while True:
                    chunk = f.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk

        url = f"{self.gateway_url}/api/v0/add"
        last_error: Optional[Exception] = None
        for _ in range(3):
            try:
                with open(file_path, "rb") as file_obj:
                    files = {"file": (os.path.basename(file_path), file_obj)}
                    response = requests.post(url, files=files)
                response.raise_for_status()
                return response.json().get("Hash")
            except Exception as e:
                last_error = e
                time.sleep(1)
        raise RuntimeError(f"Failed to upload {file_path}: {last_error}")

    def download_file(
        self,
        ipfs_hash: str,
        dest_path: str,
        progress_callback: Optional[Callable[[int, int], None]] = None,
    ) -> None:
        """Download a file from the IPFS gateway."""
        url = f"{self.gateway_url}/ipfs/{ipfs_hash}"
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total = int(response.headers.get("content-length", 0))
        downloaded = 0
        with open(dest_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)

    def get_file_info(self, ipfs_hash: str) -> Optional[dict]:
        """Retrieve information about a file from IPFS."""
        url = f"{self.gateway_url}/api/v0/object/stat?arg={ipfs_hash}"
        try:
            response = requests.post(url)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def test_connection(self) -> bool:
        """Check if the IPFS gateway is reachable."""
        url = f"{self.gateway_url}/api/v0/version"
        try:
            response = requests.post(url)
            return response.status_code == 200
        except Exception:
            return False

    def cleanup(self, path: str) -> None:
        """Remove a temporary file if it exists."""
        try:
            if os.path.isfile(path):
                os.remove(path)
        except Exception:
            pass
