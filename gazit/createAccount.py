

import os, json, urllib.request, urllib.error, dotenv
import gazitCaller
from dotenv import dotenv_values, load_dotenv

load_dotenv()
def show(label):
    print(f"\n=== {label} ===")

BODY = {
    "accountname":"Domino's"
}
METHOD = "POST"
ENDPOINT = os.environ.get("ACCOUNT_CREATE" , "").rstrip("/")

res = gazitCaller.call(ENDPOINT,METHOD,BODY)

show(res)