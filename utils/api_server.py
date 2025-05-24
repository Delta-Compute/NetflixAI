"""FastAPI server for subnet 89."""

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def validate_request(request: Request, call_next):
    """Simple request validation placeholder."""
    # Here you could add authentication or size checks
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
    """Handle video submission."""
    # In a real implementation, save or process the file
    return {"filename": file.filename}


@app.get("/status")
async def status() -> dict:
    """Return service status."""
    return {"status": "ok"}


@app.get("/metrics")
async def metrics() -> dict:
    """Return dummy metrics."""
    return {"uptime": 0}

