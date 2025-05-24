"""Database utilities using SQLite."""

from __future__ import annotations

import sqlite3
from typing import Any
import time


class Database:
    """Lightweight SQLite database wrapper."""

    def __init__(self, db_path: str = "subnet89.db", pool_size: int = 5) -> None:
        self.db_path = db_path
        self._pool: list[sqlite3.Connection] = [
            sqlite3.connect(self.db_path) for _ in range(pool_size)
        ]
        self.migrate()

    def connect(self) -> sqlite3.Connection:
        """Get a database connection from the pool or create a new one."""
        if self._pool:
            return self._pool.pop()
        return sqlite3.connect(self.db_path)

    def release(self, conn: sqlite3.Connection) -> None:
        """Return a connection to the pool."""
        self._pool.append(conn)

    def close_all(self) -> None:
        """Close all pooled connections."""
        while self._pool:
            self._pool.pop().close()

    def create_tables(self) -> None:
        """Create database tables if they do not exist."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submission_id TEXT UNIQUE,
                ipfs_hash TEXT,
                status TEXT,
                created_at REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS engagement_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post_id TEXT,
                platform TEXT,
                views INTEGER,
                likes INTEGER,
                comments INTEGER,
                shares INTEGER,
                timestamp REAL
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS validation_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                submission_id TEXT,
                validation_type TEXT,
                result TEXT,
                score REAL,
                timestamp REAL
            )
            """
        )
        conn.commit()
        self.release(conn)

    def insert_submission(
        self, submission_id: str, ipfs_hash: str, status: str = "pending"
    ) -> None:
        """Insert a new submission record."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO submissions (submission_id, ipfs_hash, status, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (submission_id, ipfs_hash, status, time.time()),
        )
        conn.commit()
        self.release(conn)

    def update_submission_status(self, submission_id: str, status: str) -> None:
        """Update the status of an existing submission."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "UPDATE submissions SET status = ? WHERE submission_id = ?",
            (status, submission_id),
        )
        conn.commit()
        self.release(conn)

    def get_pending_submissions(self) -> list[tuple[str, str]]:
        """Return list of (submission_id, ipfs_hash) for pending submissions."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT submission_id, ipfs_hash FROM submissions WHERE status = 'pending'"
        )
        rows = cur.fetchall()
        self.release(conn)
        return rows

    def insert_engagement_metrics(
        self, post_id: str, platform: str, views: int, likes: int, comments: int, shares: int
    ) -> None:
        """Store engagement metrics for a post."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO engagement_metrics (
                post_id, platform, views, likes, comments, shares, timestamp
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (post_id, platform, views, likes, comments, shares, time.time()),
        )
        conn.commit()
        self.release(conn)

    def get_submission_history(self, limit: int = 100) -> list[tuple]:
        """Retrieve recent submission records."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "SELECT submission_id, ipfs_hash, status, created_at FROM submissions ORDER BY created_at DESC LIMIT ?",
            (limit,),
        )
        rows = cur.fetchall()
        self.release(conn)
        return rows

    def cleanup_old_records(self, max_age: float) -> None:
        """Remove records older than max_age seconds."""
        cutoff = time.time() - max_age
        conn = self.connect()
        cur = conn.cursor()
        cur.execute("DELETE FROM submissions WHERE created_at < ?", (cutoff,))
        cur.execute("DELETE FROM engagement_metrics WHERE timestamp < ?", (cutoff,))
        cur.execute("DELETE FROM validation_results WHERE timestamp < ?", (cutoff,))
        conn.commit()
        self.release(conn)

    def backup(self, backup_path: str) -> None:
        """Create a backup copy of the database."""
        conn = self.connect()
        with sqlite3.connect(backup_path) as bck:
            conn.backup(bck)
        self.release(conn)

    def create_indexes(self) -> None:
        """Ensure helpful indexes exist."""
        conn = self.connect()
        cur = conn.cursor()
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_submissions_status ON submissions(status)"
        )
        cur.execute(
            "CREATE INDEX IF NOT EXISTS idx_metrics_post_platform ON engagement_metrics(post_id, platform)"
        )
        conn.commit()
        self.release(conn)

    def migrate(self) -> None:
        """Run migrations to ensure tables and indexes exist."""
        self.create_tables()
        self.create_indexes()

