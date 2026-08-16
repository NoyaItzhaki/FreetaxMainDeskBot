

import os, json, urllib.request, urllib.error, dotenv
import gazitCaller
from dotenv import dotenv_values, load_dotenv

load_dotenv()
def show(label):
    print(f"\n=== {label} ===")

BODY = {
    "lastname":"itzhaki1",
    "firstname":"noya1",
    "mobile":"+972542419048"
}
METHOD = "POST"
ENDPOINT = os.environ.get("LEAD_CREATE" , "").rstrip("/")

res = gazitCaller.call(ENDPOINT,METHOD,BODY)

show(res)