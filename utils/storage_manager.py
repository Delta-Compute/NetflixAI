"""Simple storage management with LRU eviction."""

import os
import shutil
import time
from collections import OrderedDict
from typing import Optional, Dict


class StorageManager:
    """Manage local video storage."""

    def __init__(self, root: str = "storage", max_size: int = 0) -> None:
        self.root = root
        self.max_size = max_size
        self.metadata: OrderedDict[str, Dict] = OrderedDict()
        os.makedirs(self.root, exist_ok=True)

    def get_storage_path(self, filename: str) -> str:
        """Return absolute path for a stored file."""
        return os.path.join(self.root, filename)

    def _current_size(self) -> int:
        return sum(meta["size"] for meta in self.metadata.values())

    def _evict_if_needed(self) -> None:
        while self.max_size and self._current_size() > self.max_size and self.metadata:
            oldest, _ = self.metadata.popitem(last=False)
            path = self.get_storage_path(oldest)
            try:
                os.remove(path)
            except FileNotFoundError:
                pass

    def store_file(self, source_path: str, name: Optional[str] = None) -> str:
        """Store a file and return its storage path."""
        if name is None:
            name = os.path.basename(source_path)
        dest = self.get_storage_path(name)
        shutil.copy2(source_path, dest)
        size = os.path.getsize(dest)
        self.metadata[name] = {"size": size, "last_access": time.time()}
        self.metadata.move_to_end(name, last=True)
        self._evict_if_needed()
        return dest

    def get_file(self, name: str) -> Optional[str]:
        """Retrieve a file path and update access time."""
        path = self.get_storage_path(name)
        if os.path.isfile(path):
            if name in self.metadata:
                self.metadata[name]["last_access"] = time.time()
                self.metadata.move_to_end(name, last=True)
            return path
        return None

    def delete_file(self, name: str) -> None:
        """Delete a stored file."""
        path = self.get_storage_path(name)
        if os.path.isfile(path):
            os.remove(path)
        self.metadata.pop(name, None)

    def storage_size(self) -> int:
        """Return total size used by storage."""
        return self._current_size()

    def cleanup_old_files(self, max_age: float) -> None:
        """Remove files not accessed within max_age seconds."""
        cutoff = time.time() - max_age
        for name in list(self.metadata.keys()):
            if self.metadata[name]["last_access"] < cutoff:
                self.delete_file(name)

    def stats(self) -> Dict[str, int]:
        """Return statistics about storage."""
        return {"count": len(self.metadata), "size": self._current_size()}

    def backup(self, dest_dir: str) -> None:
        """Backup stored files to another directory."""
        os.makedirs(dest_dir, exist_ok=True)
        for name in self.metadata:
            shutil.copy2(self.get_storage_path(name), os.path.join(dest_dir, name))

    def detect_corruption(self) -> Dict[str, bool]:
        """Check that all metadata files exist on disk."""
        status = {}
        for name in list(self.metadata.keys()):
            path = self.get_storage_path(name)
            status[name] = os.path.isfile(path)
            if not status[name]:
                self.metadata.pop(name, None)
        return status
