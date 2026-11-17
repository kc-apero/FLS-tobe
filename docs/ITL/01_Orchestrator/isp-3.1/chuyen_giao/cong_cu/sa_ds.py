import os, json, base64
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
cr = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/drive.metadata.readonly"])
s = AuthorizedSession(cr)
r = s.get("https://www.googleapis.com/drive/v3/files", params={"q":"mimeType='application/vnd.google-apps.spreadsheet' and trashed=false","pageSize":200,"fields":"files(id,name)","includeItemsFromAllDrives":"true","supportsAllDrives":"true"}, timeout=60)
print(r.status_code)
if r.status_code==200:
    for f in r.json()["files"]: print(f["id"], "|", f["name"])
else: print(r.text[:400])
