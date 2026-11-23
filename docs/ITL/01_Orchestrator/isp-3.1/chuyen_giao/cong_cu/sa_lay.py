"""Đọc một vùng Google Sheets bằng khoá SA (UNFORMATTED_VALUE) -> JSON {nguon, doc_luc, cach_doc, values}. ⛔ in giá trị."""
import os, sys, json, base64, urllib.parse, datetime
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
cr = service_account.Credentials.from_service_account_info(json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"])
s = AuthorizedSession(cr)
sid, rng, out = sys.argv[1], sys.argv[2], sys.argv[3]
u = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{urllib.parse.quote(rng)}"
r = s.get(u, params={"valueRenderOption": "UNFORMATTED_VALUE", "dateTimeRenderOption": "SERIAL_NUMBER", "majorDimension": "ROWS"}, timeout=120)
if r.status_code != 200:
    print(f"[ĐỎ] {rng}: HTTP {r.status_code} {r.text[:200]}"); sys.exit(1)
j = r.json(); v = j.get("values", [])
json.dump({"spreadsheet_id": sid, "nguon": j.get("range"), "doc_luc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
           "cach_doc": "Sheets API v4 values.get · UNFORMATTED_VALUE · SERIAL_NUMBER · khoá SA chỉ-đọc", "values": v},
          open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"[ĐẠT] {j.get('range')}: {len(v)} hàng · {sum(1 for h in v if any(str(x).strip() for x in h))} hàng có dữ liệu -> {os.path.basename(out)}")
