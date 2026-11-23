import os, sys, json, base64
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
s = AuthorizedSession(service_account.Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]))
r = s.get(f"https://sheets.googleapis.com/v4/spreadsheets/{sys.argv[1]}", params={"fields": "sheets.properties(title,gridProperties(rowCount,columnCount))"}, timeout=60)
for sh in r.json()["sheets"]:
    p = sh["properties"]; print(p["gridProperties"].get("rowCount"), p["gridProperties"].get("columnCount"), "|", p["title"])
