#!/usr/bin/env python3
"""gen_image.py with a selectable aspect ratio (Gemini 3 Pro Image via treg, ~$0.03).

Usage: python3 gen_image_ar.py out.png "prompt" [--ar 9:16] [reference_url ...]
Prints the public output URL (valid ~7 days) so it can be fed back as a reference for edits.
"""
import json, subprocess, sys, time, urllib.request

def treg(*args):
    r = subprocess.run(["treg", "call", *args], capture_output=True, text=True, check=True)
    d = json.loads(r.stdout)
    return d.get("body", d)

args = sys.argv[1:]
ar = "9:16"
if "--ar" in args:
    i = args.index("--ar"); ar = args[i + 1]; del args[i:i + 2]
out, prompt, refs = args[0], args[1], args[2:]
body = {"model": "gemini-3-pro-image-preview", "prompt": prompt, "size": ar, "resolution": "2K"}
if refs:
    body["image_urls"] = refs
task = treg("reapi.image-gen.gemini-3-pro-image", "--data", json.dumps(body))["id"]
for _ in range(80):
    b = treg("reapi.tasks.get", "--query", f"id={task}")
    if b.get("status") == "completed":
        url = b["output"]["image_urls"][0]
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        open(out, "wb").write(urllib.request.urlopen(req).read())
        print(url); sys.exit(0)
    if b.get("status") == "failed":
        sys.exit(f"failed: {b.get('error')}")
    time.sleep(6)
sys.exit("timed out")
