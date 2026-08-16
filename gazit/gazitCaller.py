

import os, json, urllib.request, urllib.error, dotenv
from dotenv import dotenv_values, load_dotenv
load_dotenv()
BASE = os.environ.get("GAZIT_DEMO_BASE", "").rstrip("/")
HEADERS = {
    "Api-Key": os.environ.get("GAZIT_DEMO_KEY", ""),
    "Api-Id": os.environ.get("GAZIT_DEMO_ID", ""),
    "Api-Username": os.environ.get("GAZIT_DEMO_USER", ""),
    "Content-Type": "application/json",
}

def call(ENDPOINT,METHOD,BODY):
    url = f"{BASE}/{ENDPOINT}"
    data = json.dumps(BODY or {}).encode()
    req = urllib.request.Request(url, data=data, headers=HEADERS, method=METHOD)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            raw = r.read().decode()
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
    except Exception as e:
        return {"_transport_error": str(e)}
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"_non_json": raw[:800]}


