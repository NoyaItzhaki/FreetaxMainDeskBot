

import os, json, urllib.request, urllib.error, dotenv
import gazitCaller
from dotenv import dotenv_values, load_dotenv

load_dotenv()
def show(label):
    print(f"\n=== {label} ===")

BODY = {
    "view_id": 0,
    "search_needle": "noya"
}
METHOD = "POST"
ENDPOINT = os.environ.get("ACCOUNT_GET_ALL" , "").rstrip("/")

res = gazitCaller.call(ENDPOINT,METHOD,BODY)

show(res)