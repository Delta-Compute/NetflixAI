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
        cmd = [
            "ffprobe",
            "-v",
            "error",
            "-show_entries",
            "format=duration:stream=width,height",
            "-of",
            "json",
            file_path,
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            return {}
        import json
        data = json.loads(result.stdout)
        try:
            duration = float(data.get("format", {}).get("duration", 0))
        except (ValueError, TypeError):
            duration = 0.0
        data["duration"] = duration
        return data
