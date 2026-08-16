

import os, json, urllib.request, urllib.error, dotenv
import gazitCaller
from dotenv import dotenv_values, load_dotenv

load_dotenv()
def show(label):
    print(f"\n=== {label} ===")

BODY = {
    "record":22384
}
METHOD = "POST"
ENDPOINT = os.environ.get("LEAD_CONVERT" , "").rstrip("/")

res = gazitCaller.call(ENDPOINT,METHOD,BODY)

show(res)