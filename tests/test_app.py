import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "server"))

import app as app_module  # noqa: E402


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setattr(app_module, "API_TOKEN", "secret")

    def fake_download(url, fmt, workdir):
        out = workdir / f"test.{fmt}"
        out.write_bytes(b"audio")
        return out

    monkeypatch.setattr(app_module, "download_audio", fake_download)
    monkeypatch.setattr(app_module.shutil, "which", lambda name: "/usr/bin/ffmpeg")
    return TestClient(app_module.app)


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_rejects_missing_token(client):
    r = client.get("/audio", params={"url": "https://youtu.be/dQw4w9WgXcQ"})
    assert r.status_code == 401


def test_rejects_non_youtube_url(client):
    r = client.get(
        "/audio",
        params={"url": "http://169.254.169.254/latest/meta-data"},
        headers={"X-API-Token": "secret"},
    )
    assert r.status_code == 400


def test_rejects_lookalike_host(client):
    r = client.get(
        "/audio",
        params={"url": "https://youtube.com.evil.example/watch?v=x"},
        headers={"X-API-Token": "secret"},
    )
    assert r.status_code == 400


def test_returns_audio_file(client):
    r = client.get(
        "/audio",
        params={"url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"},
        headers={"X-API-Token": "secret"},
    )
    assert r.status_code == 200
    assert r.content == b"audio"
    assert r.headers["content-type"] == "audio/mpeg"


def test_m4a_still_available(client):
    r = client.get(
        "/audio",
        params={"url": "https://youtu.be/dQw4w9WgXcQ", "format": "m4a"},
        headers={"X-API-Token": "secret"},
    )
    assert r.status_code == 200
    assert r.headers["content-type"] == "audio/mp4"


def test_rejects_bad_format(client):
    r = client.get(
        "/audio",
        params={"url": "https://youtu.be/dQw4w9WgXcQ", "format": "exe"},
        headers={"X-API-Token": "secret"},
    )
    assert r.status_code == 422
