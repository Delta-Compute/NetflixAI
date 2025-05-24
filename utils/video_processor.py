"""Video processing utilities."""

class VideoProcessor:
    """Video processing helper class."""

    def validate_format(self, file_path: str, allowed_formats: list[str]) -> bool:
        """Check if file extension is in the allowed list."""
        ext = file_path.split('.')[-1].lower()
        return ext in [fmt.lower() for fmt in allowed_formats]

    def get_video_metadata(self, file_path: str) -> dict:
        """Extract basic metadata from a video file using ffprobe."""
        import subprocess
        import json

        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=width,height,codec_name",
            "-of",
            "json",
            file_path,
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return {}

        data = json.loads(result.stdout)
        try:
            duration = float(data.get("format", {}).get("duration", 0))
        except (ValueError, TypeError):
            duration = 0.0

        streams = data.get("streams", [])
        width = height = 0
        codec = ""
        if streams:
            stream = streams[0]
            width = int(stream.get("width", 0) or 0)
            height = int(stream.get("height", 0) or 0)
            codec = stream.get("codec_name", "")

        data["duration"] = duration
        data["resolution"] = f"{width}x{height}" if width and height else ""
        data["codec"] = codec
        return data

    def validate_video_file(
        self,
        file_path: str,
        max_size_bytes: int,
        allowed_formats: list[str],
    ) -> bool:
        """Validate file size and format."""
        import os

        if not os.path.isfile(file_path):
            return False

        if os.path.getsize(file_path) > max_size_bytes:
            return False

        return self.validate_format(file_path, allowed_formats)

    def compress_video(
        self,
        input_path: str,
        output_path: str,
        target_bitrate: str,
        progress_callback=None,
    ) -> bool:
        """Compress a video using ffmpeg."""
        import subprocess

        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-b:v",
            str(target_bitrate),
            output_path,
        ]

        process = subprocess.Popen(
            cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True
        )
        if progress_callback:
            duration = self.get_video_metadata(input_path).get("duration", 0)
            while True:
                line = process.stderr.readline()
                if not line:
                    break
                if "time=" in line:
                    time_str = line.split("time=")[-1].split(" ")[0]
                    h, m, s = 0, 0, 0.0
                    try:
                        hms = time_str.split(":")
                        if len(hms) == 3:
                            h, m, s = int(hms[0]), int(hms[1]), float(hms[2])
                        current = h * 3600 + m * 60 + s
                        progress_callback(min(current, duration), duration)
                    except Exception:
                        pass

        process.wait()
        return process.returncode == 0

    def extract_thumbnail(
        self, input_path: str, time_position: float, output_path: str
    ) -> bool:
        """Extract a thumbnail from a video at a given time."""
        import subprocess

        cmd = [
            "ffmpeg",
            "-y",
            "-ss",
            str(time_position),
            "-i",
            input_path,
            "-vframes",
            "1",
            output_path,
        ]
        result = subprocess.run(cmd, capture_output=True)
        return result.returncode == 0

    def calculate_hash(self, file_path: str) -> str:
        """Return SHA256 hash of the video file."""
        import hashlib

        sha256 = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(1024 * 1024), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
