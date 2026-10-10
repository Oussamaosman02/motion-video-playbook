#!/usr/bin/env python3
"""index.tpl + assets/mouth_env.json -> index.html (inlines the lip-flap envelope)."""
import json, re
src = open("index.tpl", encoding="utf-8").read()
env = json.dumps(json.load(open("assets/mouth_env.json")), separators=(",", ":"))
open("index.html", "w", encoding="utf-8").write(re.sub(r"/\*ENV\*/.*?/\*ENV\*/", lambda m: f"/*ENV*/{env}/*ENV*/", src))
print("index.html written")
