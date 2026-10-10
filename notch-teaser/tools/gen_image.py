#!/usr/bin/env python3
"""Generate / edit a character image with Gemini 3 Pro Image (Nano Banana Pro) via the treg CLI.

Usage:
  python3 gen_image.py out.png "prompt" [reference_url ...]

~$0.03 per 2K image (reAPI provider). Prints the public output URL, which you can pass
as a reference_url to the next call (e.g. to make pose variants of the same character).
Reference URLs must return raw image bytes (CDN links work; `treg host` does NOT exist).
"""
import json
import subprocess
import sys
import time
import urllib.request


def treg(*args):
    r = subprocess.run(["treg", "call", *args], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return d.get("body", d)


import os
SIZE = os.environ.get("SIZE", "9:16")
out, prompt, refs = sys.argv[1], sys.argv[2], sys.argv[3:]
body = {"model": "gemini-3-pro-image-preview", "prompt": prompt, "size": SIZE, "resolution": "2K"}
if refs:
    body["image_urls"] = refs
task = treg("reapi.image-gen.gemini-3-pro-image", "--data", json.dumps(body))["id"]
for _ in range(60):
    b = treg("reapi.tasks.get", "--query", f"id={task}")
    if b.get("status") == "completed":
        url = b["output"]["image_urls"][0]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(out, "wb").write(urllib.request.urlopen(req).read())
        print(url)
        sys.exit(0)
    if b.get("status") == "failed":
        sys.exit(f"failed: {b.get('error')}")
    time.sleep(6)
sys.exit("timed out")
