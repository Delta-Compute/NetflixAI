"""FastAPI server for subnet 89."""

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.config import Config
from utils.video_processor import VideoProcessor
from utils.storage_manager import StorageManager
import os
import tempfile


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

video_processor = VideoProcessor()
storage = StorageManager("api_storage", max_size=Config.MAX_STORAGE_SIZE)


@app.middleware("http")
async def validate_request(request: Request, call_next):
    """Validate basic request properties like size limits."""
    length = request.headers.get("content-length")
    if length is not None:
        try:
            if int(length) > Config.MAX_VIDEO_SIZE:
                return JSONResponse(
                    status_code=413,
                    content={"error": "file too large"},
                )
        except ValueError:
            pass
    response = await call_next(request)
    return response


@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    """Basic auth check."""
    if "authorization" not in request.headers:
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=401, content={"error": "unauthorized"})
    return await call_next(request)


_last_request_time: dict[str, float] = {}


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Simple rate limiting using in-memory timestamps."""
    import time

    addr = request.client.host if request.client else "anon"
    now = time.time()
    last = _last_request_time.get(addr, 0)
    if now - last < 1:  # one request per second
        from fastapi.responses import JSONResponse

        return JSONResponse(status_code=429, content={"error": "rate limited"})
    _last_request_time[addr] = now
    return await call_next(request)


@app.post("/submit")
async def submit_file(file: UploadFile = File(...)):
    """Handle video submission with basic validation and storage."""
    ext = file.filename.split(".")[-1].lower()
    if ext not in [fmt.lower() for fmt in Config.SUPPORTED_VIDEO_FORMATS]:
        return JSONResponse(status_code=400, content={"error": "unsupported format"})

    fd, tmp_path = tempfile.mkstemp(suffix=f".{ext}")
    with os.fdopen(fd, "wb") as buffer:
        buffer.write(await file.read())

    if os.path.getsize(tmp_path) > Config.MAX_VIDEO_SIZE:
        os.remove(tmp_path)
        return JSONResponse(status_code=413, content={"error": "file too large"})

    if not video_processor.validate_video_file(tmp_path, Config.MAX_VIDEO_SIZE, Config.SUPPORTED_VIDEO_FORMATS):
        os.remove(tmp_path)
        return JSONResponse(status_code=400, content={"error": "invalid video"})

    stored_path = storage.store_file(tmp_path, name=file.filename)
    os.remove(tmp_path)
    return {"filename": file.filename, "path": stored_path}


@app.get("/status")
async def status() -> dict:
    """Return service status."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> dict:
    """Return dummy metrics."""
    return {"uptime": 0}


@app.get("/health")
async def health() -> dict:
    """Simple health check."""
    return {"ok": True}

