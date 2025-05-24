# API Endpoints

- `POST /submit` - upload a video file (supports formats: `mp4`, `mov`, `mkv`)
- `GET /status` - service status
- `GET /metrics` - basic metrics
- `GET /health` - health check

Uploads larger than the configured limit (1GB by default) are rejected with
HTTP 413. Successful uploads return the stored path of the file.
