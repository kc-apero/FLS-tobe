import os, sys, json, base64, urllib.parse, re
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
s = AuthorizedSession(service_account.Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]))
sid = sys.argv[1]
rng = "'Report I General Ledger'!AX10:BT7892"
r = s.get(f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{urllib.parse.quote(rng)}", params={"valueRenderOption": "FORMULA"}, timeout=300)
v = r.json().get("values", [])
def col(i):
    s=''; i+=1
    while i: i, q = divmod(i-1, 26); s = chr(65+q)+s
    return s
# khuôn: thay số hàng bằng {r}, {p}=r-1; so với khuôn của hàng 11 (hàng 10 là hạt giống)
mau = {}
la = []; dem = 0
for k, h in enumerate(v):
    rr = 10 + k
    for j, x in enumerate(h):
        c = col(49 + j); x = str(x)
        chuan = re.sub(r'(?<=[A-Z$])' + str(rr) + r'\b', '{r}', x)
        chuan = re.sub(r'(?<=[A-Z$])' + str(rr-1) + r'\b', '{p}', chuan)
        if rr == 11: mau[c] = chuan; continue
        if rr == 10: continue
        dem += 1
        if c in mau and chuan != mau[c]:
            la.append((c, rr, x[:200]))
print("hàng đọc:", len(v), "· ô so khuôn:", dem, "· ô lệch khuôn:", len(la))
for c, rr, x in la[:60]: print(f"{c}{rr}: {x}")
