"""Render the launch creatives to PNG with headless Chrome.

Chrome writes the screenshot but does not exit cleanly in this container, so we
poll for the output file and terminate the process once it has been written.
"""

import pathlib
import shutil
import subprocess
import tempfile
import time

OUT = pathlib.Path(__file__).resolve().parents[1] / "creatives"
CHROME = "google-chrome"
FLAGS = [
    "--headless=new", "--disable-gpu", "--no-sandbox", "--no-first-run",
    "--disable-dev-shm-usage", "--disable-extensions", "--hide-scrollbars",
    "--force-device-scale-factor=1", "--virtual-time-budget=3000",
    "--default-background-color=00000000",
]


def render(name: str, html: str, width: int, height: int,
           timeout: float = 45.0) -> pathlib.Path:
    OUT.mkdir(parents=True, exist_ok=True)
    target = OUT / f"{name}.png"
    if target.exists():
        target.unlink()

    tmp = pathlib.Path(tempfile.mkdtemp())
    try:
        src = tmp / "asset.html"
        src.write_text(html, encoding="utf-8")
        proc = subprocess.Popen(
            [CHROME, *FLAGS, f"--window-size={width},{height}",
             f"--screenshot={target}", f"--user-data-dir={tmp}/profile",
             src.as_uri()],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
        )
        deadline = time.time() + timeout
        stable = 0
        last = -1
        while time.time() < deadline:
            time.sleep(0.35)
            if target.exists():
                size = target.stat().st_size
                # wait for the file size to settle before killing Chrome
                stable = stable + 1 if size == last and size > 0 else 0
                last = size
                if stable >= 2:
                    break
            if proc.poll() is not None and target.exists():
                break
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except subprocess.TimeoutExpired:
            proc.kill()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    if not target.exists() or target.stat().st_size == 0:
        raise RuntimeError(f"render failed: {name}")
    print(f"  {name}.png  {width}x{height}  {target.stat().st_size // 1024} KB")
    return target
