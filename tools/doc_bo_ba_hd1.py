# -*- coding: utf-8 -*-
"""ĐỌC MỘT LƯỢT + đóng băng bộ ba HD1 *(sổ · L1 canon · PM)* và bộ C5c *(615 · DR2 · 2 tab số dư)* từ NGUỒN SỐNG — `WO-353`.

⭐ Vì sao có tệp này *(⛔ để script ở scratchpad như WO-345 — `SONG-R1-05`: R1 ⛔ chạy lại được từng byte)*:
  · C1 = ⓐ *(chủ 23/11)*: bộ ba HD1 tháng 8 ⛔ có khuôn ⇒ đọc sổ `ITL Ledge` *(ADJUSTED)* + `Transaction Mapping L1` +
    `[Importrange]PM_Unpivot` *(RAW)* MỘT lượt, rồi chạy 3 khuôn `itl_ledge_adjustment` · `l1_canon` · `pm_join`.
  · C3 = ⓐ: đáp án 615 + DR2 + số dư `2. CCR` · `2. CCR Cash` *(A-CCR)* CÙNG một lượt ⇒ 4 khuôn `ccr_daily_report_song` ·
    `ccr_daily_report_2_song` · `ccr_so_du_ccr` · `ccr_so_du_cash` *(giờ đọc từng tab ghi ở `luot_ccr.json` + `doc_luc` từng ảnh)*.

⛔⛔ Khoá SA CHỈ-ĐỌC *(`FLS_GSHEETS_SA_JSON_B64` / `FLS_GSHEETS_SA_JSON`)*, scope `spreadsheets.readonly`; ⛔ ghi sheet *(`QĐ-ITL-34`)*.
⛔⛔ Bản thô CHỈ ở `--tho` *(mặc định `/tmp/wo353`, thư mục 700 · tệp 600)*, ⛔ trong repo; xoá sau dùng *(`--xoa-tho`)*.
   Sổ: ⛔ đọc cột `C` *(Diễn giải)*. PM: bản thô ĐÃ CHIẾU 14 vị trí `PM_TIEU_DE_MONG_DOI` trước khi chạm đĩa ⇒ `Email Address` ·
   Tên/Số tài khoản · Ghi chú ⛔ ghi ra đâu. L1: mang `C` ở bản thô *(`bank.nap` đòi cả hàng A:AL)* — khuôn ⛔ chép.
⛔ In giá trị ô: chỉ in SỐ ĐẾM hàng.

    python tools/doc_bo_ba_hd1.py --phan ccr hd1           # đọc ⇒ bản thô /tmp/wo353 (⛔ đóng băng)
    python tools/doc_bo_ba_hd1.py --chi-dong-bang --ghi    # bản thô có sẵn ⇒ 7 khuôn ⇒ 7 ảnh `RA` của khuôn
Exit: 0 = mọi khuôn ĐẠT · 1 = có khuôn ĐỎ/TỪ CHỐI *(in tên)*.
"""
from __future__ import annotations

import argparse
import base64
import datetime
import json
import os
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

RAW = "1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E"     # = fls.oracle.nguon.BAN_SAO_RAW
ADJ = "1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA"     # = fls.oracle.nguon.SO_GOC_ADJUSTED
CCR = "1ycMOKKZg5rraLAYW-HuZDp9k3RPzr0H-iyPs_0IKL5Q"     # A-CCR_V2_Working
CACH = "Sheets API v4 values.get · UNFORMATTED_VALUE · SERIAL_NUMBER · khoá SA chỉ-đọc"
LAT = 2500
CCR_TAB = (("ccr_daily_report", "5. Daily Report", "A1:AR12521"), ("ccr_daily_report_2", "5. Daily Report 2", "A1:AR1114"),
           ("ccr_so_du_ccr", "2. CCR", "A1:ABM240"), ("ccr_so_du_cash", "2. CCR Cash", "A1:ABM240"))
#: (khuôn, bản thô, cách tính `--mong` = số dòng ảnh) — số dòng mong của mỗi khuôn khai ở `MONG_DONG_ANH`.
KHUON = (("itl_ledge_adjustment", "itl_ledge.json"), ("l1_canon", "l1.json"), ("pm_join", "pm_chieu.json"),
         ("ccr_daily_report_song", "ccr_daily_report.json"), ("ccr_daily_report_2_song", "ccr_daily_report_2.json"),
         ("ccr_so_du_ccr", "ccr_so_du_ccr.json"), ("ccr_so_du_cash", "ccr_so_du_cash.json"))
#: ⭐ Đ5 — số dòng ẢNH mong *(`--mong` của `dong_bang_sheet`)*, đo lượt `WO-353` 23/11 rồi khai.
#: 615: 22/11 2.057 → 2.056 *(hàng `Daily Transactions:No` mang chữ ⇒ tiêu đề)* · DR2 · số dư = 22/11 · sổ/L1/PM = khuôn tương ứng.
MONG_DONG_ANH: dict[str, int] = {"itl_ledge_adjustment": 12722, "l1_canon": 12601, "pm_join": 3909,
                                 "ccr_daily_report_song": 2056, "ccr_daily_report_2_song": 846,
                                 "ccr_so_du_ccr": 191, "ccr_so_du_cash": 62}
#: Hai khuôn số dư *(dùng chung với ảnh 22/11)* ghi vào ảnh `_20261123` của WO-345: lượt `WO-353` 12:11:48–49Z ra ĐÚNG TỪNG
#: BYTE ảnh ấy *(sha256 `f7a826fe…` · `59030e93…` — đo 23/11)* ⇒ G1 *(≡ ⇒ ⛔ tệp mới)*: một tệp, hai lượt chứng cùng nội dung.
RA_SO_DU = {"ccr_so_du_ccr": "tests/fixture/dau_vao/ccr_so_du_ccr_20261123.json",
            "ccr_so_du_cash": "tests/fixture/dau_vao/ccr_so_du_cash_20261123.json"}


def _bay_gio() -> str:
    return datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")


def _phien():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
    return AuthorizedSession(service_account.Credentials.from_service_account_info(
        json.loads(raw), scopes=["https://www.googleapis.com/auth/spreadsheets.readonly"]))


def _lay(s, sid: str, rng: str, lan: int = 5, cho: int = 240) -> list[list]:
    u = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{urllib.parse.quote(rng)}"
    for i in range(1, lan + 1):
        t = time.time()
        try:
            r = s.get(u, params={"valueRenderOption": "UNFORMATTED_VALUE", "dateTimeRenderOption": "SERIAL_NUMBER",
                                 "majorDimension": "ROWS"}, timeout=cho)
            if r.status_code == 200:
                v = r.json().get("values", [])
                print(f"  {rng[:52]:52s} {len(v):6d} hàng {time.time() - t:5.1f}s", flush=True)
                return v
            print(f"  {rng[:52]:52s} lần {i}/{lan} HTTP {r.status_code}", flush=True)
        except Exception as e:                                   # timeout · mạng — nguồn chậm khi nguội
            print(f"  {rng[:52]:52s} lần {i}/{lan} {type(e).__name__}", flush=True)
        time.sleep(5 * i)
    raise SystemExit(f"⛔ đọc {rng} hỏng {lan} lần")


def _ghi(tho: Path, ten: str, d: dict) -> None:
    p = tho / ten
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False)
    print(f"  [bản thô] {ten}")


def _theo_lat(s, sid: str, tab: str, a: str, b: str, dau: int, n: int | None = None) -> list[list]:
    """Đọc dần. `n` biết trước *(sổ — từ cột A)* ⇒ đệm hàng rỗng cuối lát *(API cắt hàng cuối rỗng ⇒ lệch số hàng IM LẶNG)*.
    ⛔ biết ⇒ như `nap_that.doc_nguon` *(lát ngắn = hết)*; cột A đếm lại ở `_kiem_cot_a` *(Đ1 — hai nguồn)*."""
    hang, lo = [], dau
    while True:
        hi = lo + LAT - 1 if n is None else min(lo + LAT - 1, dau + n - 1)
        v = _lay(s, sid, f"'{tab}'!{a}{lo}:{b}{hi}")
        if n is not None:
            v = v + [[] for _ in range(hi - lo + 1 - len(v))]
        hang.extend(v)
        if (n is None and len(v) < LAT) or (n is not None and hi >= dau + n - 1):
            return hang
        lo += LAT


def doc_ccr(s, tho: Path) -> None:
    luot = {"bat_dau": _bay_gio()}
    for ten, tab, vung in CCR_TAB:
        dl = _bay_gio()
        v = _lay(s, CCR, f"'{tab}'!{vung}")
        _ghi(tho, f"{ten}.json", {"spreadsheet_id": CCR, "nguon": f"'{tab}'!{vung}", "doc_luc": dl, "cach_doc": CACH, "values": v})
        luot[ten] = dl
    luot["ket_thuc"] = _bay_gio()
    _ghi(tho, "luot_ccr.json", luot)


def chieu_pm(tieu_de: list, values: list[list]) -> tuple[list, list[list]]:
    """Giữ ĐÚNG 14 vị trí `PM_TIEU_DE_MONG_DOI` *(⛔ ô/tên khác — `Email Address` · tên/số TK · ghi chú)*; độ dài hàng giữ nguyên."""
    from fls.adapters.pm_join import PM_TIEU_DE_MONG_DOI as G
    td = [(x if j in G else "") for j, x in enumerate(tieu_de)]
    return td, [[(x if j in G else None) for j, x in enumerate(h)] for h in values]


def doc_hd1(s, tho: Path) -> None:
    luot = {"bat_dau": _bay_gio()}
    td = _lay(s, ADJ, "'ITL Ledge'!A7:AT8")
    n = len(_lay(s, ADJ, "'ITL Ledge'!A10:A40000"))
    _ghi(tho, "itl_ledge.json", {
        "spreadsheet_id": ADJ, "nguon": f"'ITL Ledge'!A10:B{9 + n} · D10:G{9 + n} · R10:AT{9 + n} (⛔ C)", "doc_luc": _bay_gio(),
        "cach_doc": CACH, "tieu_de": (td + [[], []])[:2], "dong_dau": 10,
        "AB": _theo_lat(s, ADJ, "ITL Ledge", "A", "B", 10, n), "DG": _theo_lat(s, ADJ, "ITL Ledge", "D", "G", 10, n),
        "RAT": _theo_lat(s, ADJ, "ITL Ledge", "R", "AT", 10, n)})
    luot["so"] = _bay_gio()
    h3 = _lay(s, RAW, "'Transaction Mapping L1'!A3:AL3")
    l1 = _theo_lat(s, RAW, "Transaction Mapping L1", "A", "AL", 5)
    _ghi(tho, "l1.json", {"spreadsheet_id": RAW, "nguon": f"'Transaction Mapping L1'!A5:AL{4 + len(l1)}", "doc_luc": _bay_gio(),
                          "cach_doc": CACH, "header": h3[0] if h3 else [], "dong_dau": 5, "values": l1})
    luot["l1"] = _bay_gio()
    h2 = _lay(s, RAW, "'[Importrange]PM_Unpivot'!A2:AC2")
    pm = _theo_lat(s, RAW, "[Importrange]PM_Unpivot", "A", "AC", 3)
    tdc, pmc = chieu_pm(h2[0] if h2 else [], pm)
    _ghi(tho, "pm_chieu.json", {"spreadsheet_id": RAW, "nguon": f"'[Importrange]PM_Unpivot'!A3:AC{2 + len(pm)} (chiếu 14 cột)",
                                "doc_luc": _bay_gio(), "cach_doc": CACH + " · CHIẾU 14 vị trí PM_TIEU_DE_MONG_DOI",
                                "tieu_de": tdc, "dong_dau": 3, "values": pmc})
    luot["ket_thuc"] = _bay_gio()
    _ghi(tho, "luot_hd1.json", luot)


def dong_bang(tho: Path, ghi: bool) -> int:
    """7 khuôn qua `tools/dong_bang_sheet.py` *(⛔ đường thứ hai)*: `--mong` = `MONG_DONG_ANH`; `--ghi` ⇒ `--ra` = `RA` của khuôn
    *(hai số dư: `RA_SO_DU`)*, ⛔ thì ra `/tmp`."""
    do = []
    for k, f in KHUON:
        mong = MONG_DONG_ANH.get(k)
        if mong is None:
            do.append(f"{k}: MONG_DONG_ANH ⛔ khai"); continue
        sys.path.insert(0, str(GOC / "tools"))
        import dong_bang_sheet as t
        ra = (RA_SO_DU.get(k) or t.nap_khuon(k).ra) if ghi else str(tho / f"anh_{k}.json")
        r = subprocess.run([sys.executable, str(GOC / "tools" / "dong_bang_sheet.py"), k, str(tho / f), "--mong", str(mong),
                            "--ra", str(GOC / ra) if ghi else ra], capture_output=True, text=True, cwd=GOC)
        cuoi = [x for x in r.stdout.splitlines() if x.startswith(("[ĐẠT]", "[ĐỎ]", "⛔"))] + r.stderr.strip().splitlines()[-1:]
        print(f"  {k:26s} exit {r.returncode} · {(cuoi or ['?'])[0][:160]}")
        if r.returncode != 0:
            do.append(f"{k}: exit {r.returncode}")
    # ⭐ rào DT13: ảnh DR2 chụp lại CHỈ là đầu vào 615 *(khuôn `ccr_daily_report_2_song` khai cùng rào khuôn cũ)* — kiểm NGAY sau
    #    khi đóng băng, để lượt nào đổi rào thì lượt ấy ĐỎ *(⛔ chờ engine đọc mới biết)*.
    from tools.khuon_dong_bang._rao_dau_vao import DauVaoSaiChoError, kiem_dau_vao_hop_le
    kiem_dau_vao_hop_le("ccr_daily_report_2_song", "615")
    try:
        kiem_dau_vao_hop_le("ccr_daily_report_2_song", "610")
        do.append("rào DT13 ⛔ chặn DR2 sống → 610")
    except DauVaoSaiChoError:
        pass
    if do:
        print("⛔ ĐỎ: " + " · ".join(do))
    return 1 if do else 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--tho", default="/tmp/wo353")
    p.add_argument("--phan", nargs="*", default=["ccr", "hd1"], choices=["ccr", "hd1"])
    p.add_argument("--chi-dong-bang", action="store_true")
    p.add_argument("--ghi", action="store_true")
    p.add_argument("--xoa-tho", action="store_true")
    a = p.parse_args(argv)
    tho = Path(a.tho)
    tho.mkdir(mode=0o700, parents=True, exist_ok=True)
    os.chmod(tho, 0o700)
    if not a.chi_dong_bang:
        s = _phien()
        if "ccr" in a.phan:
            doc_ccr(s, tho)
        if "hd1" in a.phan:
            doc_hd1(s, tho)
    kq = dong_bang(tho, a.ghi)
    if a.xoa_tho:
        for f in tho.glob("*.json"):
            f.unlink()
        print(f"  đã xoá bản thô ở {tho}")
    return kq


if __name__ == "__main__":
    raise SystemExit(main())
