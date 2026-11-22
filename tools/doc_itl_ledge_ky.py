"""ĐỌC sổ ADJUSTED tab `ITL Ledge` THEO KỲ và đóng băng MỖI kỳ ≠ 2026-03 thành ảnh *(ISP 3.1.2 · DT12 · `WO-265`)*.

    FLS_GSHEETS_SA_JSON_B64=… REQUESTS_CA_BUNDLE=… python -I tools/doc_itl_ledge_ky.py --mong-ky 26

Vòng làm: ① đọc hàng 7+8 *(chỉ in TÊN cột)* ② đọc cột `A` *(ngày)* theo LÁT hàng ⇒ đếm kỳ ĐỘC LẬP *(`mong` của mỗi kỳ)*
③ mỗi kỳ: đọc `A` + `R:AT` đúng dải hàng của kỳ *(lát ≤ `LAT` hàng, mỗi lát ≤ 3 lần thử)*, dựng bản thô, chạy
`tools/dong_bang_sheet.py itl_ledge_ky … --mong <số ở ②>` ④ ghi `tests/fixture/dap_an/itl_ledge_cac_ky.json`:
kỳ đọc được · kỳ **hỏng = `blocked` CÓ TÊN** *(⛔ bỏ im, ⛔ ảnh rỗng)* · tổng kích thước. Exit 0 ⇔ cổng kỳ ĐẠT.

⛔⛔ PII: bản thô chỉ ở `/tmp/dt12_tho` *(chmod 600, XOÁ cuối lượt)*; mọi dòng in chỉ là TÊN cột hay SỐ ĐẾM.
Cột đọc: `A` · `R:AT` — ⛔ `B` Số chứng từ · `C` Diễn giải.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.parse
from collections import OrderedDict
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "tools" / "khuon_dong_bang"))
import itl_ledge_ky as K  # noqa: E402
from fls.canon.o_loi import la_o_loi  # noqa: E402

SID = "1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA"
TAB = "ITL Ledge"
HANG_DAU = 10                # hàng dữ liệu đầu *(hàng 7·8 = tiêu đề; 9 = trống — đo 20/11)*
HANG_CUOI = 12684            # lưới
LAT = 1500
BO_QUA = {"2026-03": "ảnh có sẵn — ⛔ đụng"}
TMP = Path("/tmp/dt12_tho")
RA_DIR = GOC / "tests" / "fixture" / "dap_an"
EPOCH = datetime.date(1899, 12, 30)
# Vị trí tên cột ở `A1:AT8` *(0-based)*: A=0 · R=17 · nhãn khối ở V W AA AE AI AM AQ · phân khối S…AT = 18…45.
VT_NHAN = (21, 22, 26, 30, 34, 38, 42)


def _phien():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
    return AuthorizedSession(service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]))


def lay(s, rng: str):
    """Một vùng, tối đa `K.so_lan_thu` lần; hỏng ⇒ chuỗi lý do *(⛔ ném)*."""
    u = f"https://sheets.googleapis.com/v4/spreadsheets/{SID}/values/{urllib.parse.quote(rng)}"
    err = "?"
    for t in range(1, K.so_lan_thu + 1):
        try:
            r = s.get(u, params={"valueRenderOption": "UNFORMATTED_VALUE", "dateTimeRenderOption": "SERIAL_NUMBER",
                                 "majorDimension": "ROWS"}, timeout=120)
            if r.status_code == 200:
                return r.json().get("values", [])
            err = f"HTTP {r.status_code}"
        except Exception as e:                    # noqa: BLE001 — mạng/hết giờ: thử lại
            err = type(e).__name__
        time.sleep(2 * t)
    return err


def _tieu_de(v: list[list]) -> list[str]:
    a7, a8 = v[6] + [""] * 46, v[7] + [""] * 46
    td = [str(a7[17]), str(a7[0])]
    for j in range(7):
        for p in range(4):
            td.append(f"{a7[VT_NHAN[j]]} · {a8[18 + 4 * j + p]}")
    return td


def _ky(serial) -> str:
    d = EPOCH + datetime.timedelta(days=int(serial))
    return f"{d.year}-{d.month:02d}"


def ghi_anh_chuan(cong: dict, ra: Path) -> dict:
    """Ảnh của cổng `dong_bang_sheet` → ghi ảnh HÌNH 2026-03 ở `ra` *(`K.chuan_hoa_anh`)* + mục manifest *(cổng · cột · checksum
    của lượt đóng băng, byte/sha256 của ảnh GHI RA)*. `DT12-R1-01`: ⛔ sửa tay JSON — mọi ảnh đi qua đây."""
    anh = K.chuan_hoa_anh(cong)
    ra.write_text(json.dumps(anh, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    hang = [r["dong_sheet"] for r in anh["dong"]]
    return {"so_dong": anh["so_dong"], "hang_sheet": [min(hang), max(hang)],
            "itl_id_loi": sum(1 for r in anh["dong"] if la_o_loi(r["itl_id_sheet"])),
            "checksum_noi_dung": cong["checksum_noi_dung"], "cong": cong["cong"], "cot": cong["cot"],
            "bytes": ra.stat().st_size, "sha256": hashlib.sha256(ra.read_bytes()).hexdigest()}


def chuan_hoa_anh_cu() -> int:
    """MỘT LẦN: ảnh đã đóng băng ở hình `{"chu"}` *(lượt `BG-266`)* → hình 2026-03, ⛔ đọc lại sổ. Khứ hồi: mỗi ô `_chuan` TRƯỚC =
    SAU và checksum tính lại từ ảnh mới = checksum cũ, nếu không ⇒ exit 1 *(⛔ ghi)*. Ảnh đã đúng hình ⇒ bỏ qua *(idempotent)*."""
    mp = RA_DIR / "itl_ledge_cac_ky.json"
    m = json.loads(mp.read_text(encoding="utf-8"))
    mau = json.loads((GOC / "tests" / "fixture" / "itl_ledge_2026_03.json").read_text(encoding="utf-8"))
    o_truoc = o_sau = n_ky = 0
    chuan_o = lambda v: "" if v is None else (str(int(v)) if isinstance(v, float) and v.is_integer() else str(v).strip())  # noqa: E731
    moi: dict[str, dict] = {}
    for ky in sorted(m["anh"]):
        p = RA_DIR / f"itl_ledge_{ky}.json"
        cong = json.loads(p.read_text(encoding="utf-8"))
        if "thu_tu" not in cong["dong"][0]:
            print(f"[{ky}] đã đúng hình — bỏ qua"); continue
        anh = K.chuan_hoa_anh(cong)
        if K.loi_hinh(anh, mau):
            print(f"[ĐỎ] {ky}: sau chuẩn hoá vẫn sai hình {K.loi_hinh(anh, mau)}"); return 1
        for rc, ra_ in zip(cong["dong"], anh["dong"]):
            for c in K.COT:
                o_truoc += 1
                u = rc[c]["chu"] if isinstance(rc[c], dict) else rc[c]
                o_sau += 1
                if chuan_o(u) != chuan_o(ra_[c]):
                    print(f"[ĐỎ] {ky}: ô `{c}` đổi giá trị qua chuẩn hoá"); return 1
        if len(cong["dong"]) != len(anh["dong"]):
            print(f"[ĐỎ] {ky}: số dòng đổi"); return 1
        moi[ky] = cong
        n_ky += 1
    for ky, cong in moi.items():
        m["anh"][ky] = ghi_anh_chuan(cong, RA_DIR / f"itl_ledge_{ky}.json")
        if m["anh"][ky]["checksum_noi_dung"] != cong["checksum_noi_dung"]:
            print(f"[ĐỎ] {ky}: checksum đổi"); return 1
    m["tong_bytes"] = sum(x["bytes"] for x in m["anh"].values())
    m["anh_lon_hon_2MB"] = [k for k, x in m["anh"].items() if x["bytes"] > 2 * 1024 * 1024]
    m["hinh_anh"] = "= ảnh 2026-03 {nguon, ky, dong_du_lieu_bat_dau, so_dong, ghi_chu, dong} · DT12-R1-01"
    mp.write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[khứ hồi] {n_ky} kỳ · {o_truoc} ô trước = {o_sau} ô sau · mọi `_chuan` khớp · {m['tong_bytes']:,} byte")
    return 0 if n_ky else 1


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--chuan-hoa-anh-cu", action="store_true", help="đổi ảnh `{\"chu\"}` đã có sang hình 2026-03 (⛔ đọc sổ)")
    ap.add_argument("--giu-tho", action="store_true", help="⛔ xoá bản thô cuối lượt — cờ này chỉ để gỡ lỗi")
    ap.add_argument("--mong-ky", type=int, required=False, help="Đ5: số kỳ của sổ (gồm 2026-03)")
    a = ap.parse_args()
    if a.chuan_hoa_anh_cu:
        return chuan_hoa_anh_cu()
    if a.mong_ky is None:
        ap.error("--mong-ky bắt buộc (trừ --chuan-hoa-anh-cu)")
    s = _phien()
    v = lay(s, f"'{TAB}'!A1:AT8")
    if isinstance(v, str):
        print(f"[ĐỎ] tiêu đề {TAB}: {v}"); return 1
    td = _tieu_de(v)
    print(f"[tiêu đề] 30 tên cột đọc từ hàng 7·8 — khớp khuôn: {tuple(td) == K.TIEU_DE}")
    if tuple(td) != K.TIEU_DE:
        print("[ĐỎ] tên cột ≠ khuôn — ⛔ đóng băng"); return 1
    # ② cột A → số kỳ độc lập
    hang_ky: dict[str, list[int]] = OrderedDict()
    for lo in range(HANG_DAU, HANG_CUOI + 1, LAT):
        hi = min(lo + LAT - 1, HANG_CUOI)
        c = lay(s, f"'{TAB}'!A{lo}:A{hi}")
        if isinstance(c, str):
            print(f"[ĐỎ] cột A hàng {lo}…{hi} hỏng sau {K.so_lan_thu} lần: {c} — số kỳ ⛔ đo được"); return 1
        for i, r in enumerate(c):
            if r and r[0] != "":
                if isinstance(r[0], bool) or not isinstance(r[0], (int, float)):
                    print(f"[ĐỎ] hàng {lo + i}: cột A ⛔ phải số ngày"); return 1
                hang_ky.setdefault(_ky(r[0]), []).append(lo + i)
    mong = {k: len(x) for k, x in sorted(hang_ky.items())}
    print(f"[kỳ] cột A: {sum(mong.values())} hàng có ngày · {len(mong)} kỳ {min(mong)}…{max(mong)} (mong {a.mong_ky})")
    if len(mong) != a.mong_ky:
        print(f"[ĐỎ] số kỳ đo {len(mong)} ≠ --mong-ky {a.mong_ky}"); return 1
    # ③ từng kỳ
    TMP.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(TMP, 0o700)
    ngay_doc = datetime.date.today().isoformat()
    doc: dict[str, int | None] = {}
    anh: dict[str, dict] = {}
    ly_do: dict[str, str] = {}
    for ky, hs in sorted(hang_ky.items()):
        if ky in BO_QUA:
            continue
        lo, hi = min(hs), max(hs)
        hang, hong = [], None
        for b in range(lo, hi + 1, LAT):
            e = min(b + LAT - 1, hi)
            ca, cr = lay(s, f"'{TAB}'!A{b}:A{e}"), lay(s, f"'{TAB}'!R{b}:AT{e}")
            if isinstance(ca, str) or isinstance(cr, str):
                hong = ca if isinstance(ca, str) else cr
                break
            for i in range(e - b + 1):
                ra_ = ca[i] if i < len(ca) else []
                if ra_ and ra_[0] != "" and _ky(ra_[0]) == ky:
                    rr = cr[i] if i < len(cr) else []
                    hang.append([b + i, ra_[0], *(rr + [""] * 29)[:29]])
        if hong is not None:
            doc[ky] = None
            ly_do[ky] = hong
            print(f"[blocked] {ky}: đọc hỏng sau {K.so_lan_thu} lần — {hong}")
            continue
        p = TMP / f"tho_{ky}.json"
        p.write_text(json.dumps({"nguon": f"{TAB} (sổ ADJUSTED) · kỳ {ky} · hàng {lo}…{hi}", "doc_luc": ngay_doc,
                                 "cach_doc": "Sheets API v4 values.get theo lát hàng · UNFORMATTED_VALUE · SERIAL_NUMBER "
                                             "· khoá SA chỉ-đọc · chỉ cột A + R:AT",
                                 "ky": ky, "tieu_de": td, "hang": hang}, ensure_ascii=False), encoding="utf-8")
        os.chmod(p, 0o600)
        ra = RA_DIR / f"itl_ledge_{ky}.json"
        cong_p = TMP / f"cong_{ky}.json"          # ảnh của cổng *(checksum · cổng)* — trung gian, xoá cùng `TMP`
        r = subprocess.run([sys.executable, str(GOC / "tools" / "dong_bang_sheet.py"), "itl_ledge_ky", str(p),
                            "--mong", str(mong[ky]), "--ra", str(cong_p)], capture_output=True, text=True, cwd=GOC)
        dat = r.returncode == 0
        print(f"[{ky}] cổng exit {r.returncode} · {len(hang)} hàng đọc · mong {mong[ky]}"
              + ("" if dat else " — " + (r.stdout.strip().splitlines() or [r.stderr.strip()[:200]])[-1][:200]))
        if not dat:
            doc[ky] = None
            ly_do[ky] = f"cổng exit {r.returncode}"
            continue
        j = json.loads(cong_p.read_text(encoding="utf-8"))
        doc[ky] = j["so_dong"]
        anh[ky] = ghi_anh_chuan(j, ra)             # hình 2026-03; cổng/checksum ⇒ manifest
    if not a.giu_tho:
        shutil.rmtree(TMP, ignore_errors=True)
    kq = K.phan_loai_ky(doc, mong=a.mong_ky - len(BO_QUA))
    m = {"spreadsheet_id": SID, "tab": TAB,
         "nguon": "ITL I Input Transaction Ledger File 2/2 (ADJUSTED) > ITL Ledge",
         "vung": f"A{HANG_DAU}:A{HANG_CUOI} (ngày) · R{HANG_DAU}:AT{HANG_CUOI} (itl_id + 28 cột)",
         "doc_luc": ngay_doc, "so_ky_cua_so": len(mong), "mong_so_ky_cua_so": a.mong_ky,
         "dong_theo_ky_o_cot_A": mong, "ky_bo_qua": BO_QUA, "doc_duoc": kq["doc_duoc"],
         "hong": {k: {"trang_thai": "blocked", "ly_do": ly_do.get(k, "?")} for k in kq["hong"]},
         "anh": anh, "tong_bytes": sum(x["bytes"] for x in anh.values()),
         "anh_lon_hon_2MB": [k for k, x in anh.items() if x["bytes"] > 2 * 1024 * 1024]}
    (RA_DIR / "itl_ledge_cac_ky.json").write_text(json.dumps(m, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"[cổng kỳ] {'ĐẠT' if kq['dat'] else 'ĐỎ — ' + ' · '.join(kq['ly_do'])}: đọc được {len(kq['doc_duoc'])} + hỏng "
          f"{len(kq['hong'])} + bỏ qua {len(BO_QUA)} = {len(mong)} kỳ · {sum(kq['doc_duoc'].values())} dòng · "
          f"{m['tong_bytes']:,} byte")
    return 0 if kq["dat"] else 1


if __name__ == "__main__":
    sys.exit(main())
