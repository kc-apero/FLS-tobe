import os, sys, json, base64, urllib.parse
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
s = AuthorizedSession(service_account.Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]))
sid, rng = sys.argv[1], sys.argv[2]
r = s.get(f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{urllib.parse.quote(rng)}", params={"valueRenderOption": "FORMULA"}, timeout=120)
print(r.status_code)
v = r.json().get("values", [])
def col(i):
    s=''; i+=1
    while i: i, q = divmod(i-1, 26); s = chr(65+q)+s
    return s
off = 49  # AX = cột 50 ⇒ chỉ số 49
want = {"AZ","BC","BF","BI","BL","BM","BQ","BT"}
r0 = int(sys.argv[3])
for k, h in enumerate(v):
    for j, x in enumerate(h):
        c = col(off + j)
        if c in want: print(f"{c}{r0+k}: {str(x)[:220]}")
