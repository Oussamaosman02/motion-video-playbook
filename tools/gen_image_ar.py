#!/usr/bin/env python3
"""gen_image.py with a selectable aspect ratio (Gemini 3 Pro Image via treg, ~$0.03 per 2K image).

Canonical copy of the per-format variants (notch-teaser/tools/gen_image.py with SIZE,
whiteboard-ad/tools/gen_image_916.py with IMG_SIZE, founder-depth-type/tools/gen_image_ar.py with --ar).
The original tools/gen_image.py stays unchanged (it hard-codes 2:3).

Usage:
  python3 gen_image_ar.py out.png "prompt" [--ar 9:16] [reference_url ...]
Aspect ratio priority: --ar, then $IMG_SIZE, then $SIZE, then 9:16 (vertical, full frame).

Prints the public output URL (valid ~7 days); pass it as a reference_url to the next call
to make aligned edits (pose variants, empty board, mouth-open, ...).
If a poll fails ("treg pool saturated"), re-run with --task <id> to fetch the finished image
instead of paying for a new one:  python3 gen_image_ar.py out.png --task <id>
"""
import json
import os
import subprocess
import sys
import time
import urllib.request


def treg(*args):
    r = subprocess.run(["treg", "call", *args], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return d.get("body", d)


args = sys.argv[1:]
ar = os.environ.get("IMG_SIZE") or os.environ.get("SIZE") or "9:16"
if "--ar" in args:
    i = args.index("--ar"); ar = args[i + 1]; del args[i:i + 2]
task = None
if "--task" in args:
    i = args.index("--task"); task = args[i + 1]; del args[i:i + 2]
out = args[0]
if task is None:
    prompt, refs = args[1], args[2:]
    body = {"model": "gemini-3-pro-image-preview", "prompt": prompt, "size": ar, "resolution": "2K"}
    if refs:
        body["image_urls"] = refs
    task = treg("reapi.image-gen.gemini-3-pro-image", "--data", json.dumps(body))["id"]
    print(f"task {task}", file=sys.stderr)
for _ in range(80):
    try:
        b = treg("reapi.tasks.get", "--query", f"id={task}")
    except subprocess.CalledProcessError as e:  # transient poll error: keep polling, don't regenerate
        print(f"poll error, retrying: {e.stderr[:200]}", file=sys.stderr); time.sleep(10); continue
    if b.get("status") == "completed":
        url = b["output"]["image_urls"][0]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(out, "wb").write(urllib.request.urlopen(req).read())
        print(url)
        sys.exit(0)
    if b.get("status") == "failed":
        sys.exit(f"failed: {b.get('error')}")
    time.sleep(6)
sys.exit(f"timed out; fetch later with --task {task}")
