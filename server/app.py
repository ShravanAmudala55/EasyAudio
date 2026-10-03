"""EasyAudio: a tiny HTTP API that turns a YouTube link into an audio file via yt-dlp."""

import logging
import os
import secrets
import shutil
import tempfile
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

import yt_dlp
from fastapi import BackgroundTasks, FastAPI, Header, HTTPException, Query
from fastapi.responses import FileResponse

log = logging.getLogger("EasyAudio")

API_TOKEN = os.getenv("AUDIO_API_TOKEN", "")
MAX_DURATION_SECONDS = int(os.getenv("MAX_DURATION_SECONDS", "3600"))

ALLOWED_HOSTS = {
    "youtube.com",
    "www.youtube.com",
    "m.youtube.com",
    "music.youtube.com",
    "youtu.be",
}

MEDIA_TYPES = {
    ".m4a": "audio/mp4",
    ".mp3": "audio/mpeg",
    ".webm": "audio/webm",
    ".opus": "audio/ogg",
}

app = FastAPI(title="EasyAudio", version="0.1.0")


def check_token(provided: Optional[str]) -> None:
    """Reject the request unless the token matches. No-op when no token is configured."""
    if not API_TOKEN:
        return
    if not provided or not secrets.compare_digest(provided, API_TOKEN):
        raise HTTPException(status_code=401, detail="Invalid or missing X-API-Token header")


def validate_url(raw: str) -> str:
    """Only accept plain http(s) links to known YouTube hosts."""
    parsed = urlparse(raw)
    host = (parsed.hostname or "").lower()
    if parsed.scheme not in ("http", "https") or host not in ALLOWED_HOSTS:
        raise HTTPException(status_code=400, detail="Only YouTube URLs are supported")
    return raw


def download_audio(url: str, fmt: str, workdir: Path) -> Path:
    """Download the audio track of `url` into `workdir` and return the file path."""
    opts = {
        "format": "bestaudio[ext=m4a]/bestaudio/best",
        "outtmpl": str(workdir / "%(title).80B [%(id)s].%(ext)s"),
        "noplaylist": True,
        "restrictfilenames": True,
        "quiet": True,
        "no_warnings": True,
        "match_filter": yt_dlp.utils.match_filter_func(f"duration <= {MAX_DURATION_SECONDS}"),
    }
    if fmt == "mp3":
        opts["format"] = "bestaudio/best"
        opts["postprocessors"] = [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])

    files = [p for p in workdir.iterdir() if p.is_file()]
    if not files:
        raise RuntimeError("No file was produced (the video may be too long or unavailable)")
    return files[0]


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/audio")
def audio(
    background_tasks: BackgroundTasks,
    url: str = Query(..., description="YouTube video URL"),
    format: str = Query("mp3", pattern="^(m4a|mp3)$"),
    x_api_token: Optional[str] = Header(default=None),
):
    check_token(x_api_token)
    validate_url(url)

    if format == "mp3" and shutil.which("ffmpeg") is None:
        raise HTTPException(status_code=501, detail="mp3 needs ffmpeg installed on the server")

    workdir = Path(tempfile.mkdtemp(prefix="EasyAudio-"))
    try:
        path = download_audio(url, format, workdir)
    except yt_dlp.utils.DownloadError as exc:
        shutil.rmtree(workdir, ignore_errors=True)
        log.warning("download failed: %s", exc)
        raise HTTPException(status_code=422, detail="Could not download that video") from exc
    except Exception as exc:
        shutil.rmtree(workdir, ignore_errors=True)
        log.exception("unexpected error")
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    background_tasks.add_task(shutil.rmtree, workdir, True)
    return FileResponse(
        path,
        media_type=MEDIA_TYPES.get(path.suffix.lower(), "application/octet-stream"),
        filename=path.name,
    )
