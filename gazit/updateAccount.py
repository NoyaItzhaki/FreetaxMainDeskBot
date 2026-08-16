

import os, json, urllib.request, urllib.error, dotenv
import gazitCaller
from dotenv import dotenv_values, load_dotenv

load_dotenv()
def show(label):
    print(f"\n=== {label} ===")

BODY = {
    "record":22386,
    "cnpj_number": "", 
    "obligo_max": "500.000",
    "email": "",
    "mobile": "0542419047"

}
METHOD = "POST"
ENDPOINT = os.environ.get("ACCOUNT_UPDATE" , "").rstrip("/")

res = gazitCaller.call(ENDPOINT,METHOD,BODY)

show(res)