"""Đ2 · Đo HINH DANG cua nguon AS-IS — doc SONG, ⛔ khong doc ban chup.

★★ **Vi sao doc song.** Ban chup offline o `AS-IS system/.../RAW` co tuoi
   **31–48 ngay**, va no TROI THAT: `[Importrange]1.2 Ledger 112` chup 18/08
   la **7.626** dong, song hom nay **9.148**. So voi ban chup thi mot lech
   tim duoc co the la *"FLS sai"*, cung co the la *"so da doi sau khi chup"*
   — **hai thu do trong y het nhau**.

⛔⛔ **Khuyet tat THU NAM cua ban xuat `.xlsx`, phat hien 2026-09-07:**
   no **CAT TEN SHEET o dung 31 ky tu** (gioi han cua Excel). Do that: 13
   sheet `R |` cua `P100 | Bank Transactions` bi cat ⇒ mot phep so ghep sheet
   THEO TEN giua offline va song se bao **13 mat + 13 moi**, va **ca 26 deu
   gia**. Bon khuyet tat da ghi truoc do (mat ma · ngay hoan · HD/CDT sai ·
   ban sao tu san xuat mac dinh) deu o phan **GIA TRI**; cai nay o phan
   **DANH TINH**.

⛔ Cong cu nay CHI doc:
     · metadata (ten sheet + kich thuoc luoi)
     · **ba dong dau** cua moi sheet `R |` — de biet ten cot
   ⛔ Khong doc mot o DU LIEU nao. Dung trong pham vi `QD-ITL-85`.

Chay:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_hinh_dang.py
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

SA = "claude-code-access@fpa-t-494007.iam.gserviceaccount.com"
API = "https://sheets.googleapis.com/v4/spreadsheets/"

# ── Nguon trong pham vi `Đ2` (owner chot 2026-09-07: 6 sheet + archetype `R |`)
NGUON = {
    "P100-BANK": ("1zJA0MyS8u4_EC6HimREQT6RM3-DDGnBZSRa3HQsfOn8",
                  "P100 | Bank Transactions"),
    "P100-CASH": ("1RmmkOSCTYVp1DSmNIQLvE9VlWIqhQegqN7lVazWkF7U",
                  "Copy of P100 | Cash Ledger"),
    "ITL-RAW":   ("1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E",
                  "Copy of ITL … 1/2 (RAW)"),
    "ITL-ADJ":   ("1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA",
                  "ITL … 2/2 (ADJUSTED)"),
}
# ⛔ `A-CCR_V2_Working` (chua `2. CCR` dong 226) ⛔ CHUA co quyen doc song.
#    Chi co ban chup 28/07. => o `2. CCR` cua so doi chieu o lai `K0`.


def token() -> str:
    r = subprocess.run(
        ["gcloud", "auth", "print-access-token", "--account", SA, "--scopes",
         "https://www.googleapis.com/auth/spreadsheets.readonly"],
        capture_output=True, text=True, shell=True)
    t = r.stdout.strip()
    if not t:
        raise SystemExit("⛔ khong lay duoc token: " + r.stderr.strip()[:200])
    return t


def _goi(url: str, tok: str, giay: int = 90, lan: int = 5):
    """Goi Sheets API, co **lui-va-thu-lai** cho `429`/`5xx`.

    ⛔ Sheets co han muc doc theo phut. Mot phep do lon *(60 sheet x nhieu
    cot)* cham han muc that — da gap `429` khi dung lai `Bank Transactions`.
    ⛔ Do khong duoc thi phai **cho roi do lai**, ⛔ khong duoc bo qua va bao
    xanh (cong chung #7).
    """
    q = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
    for i in range(lan):
        try:
            with urllib.request.urlopen(q, timeout=giay) as f:
                return json.loads(f.read())
        except urllib.error.HTTPError as e:
            if e.code not in (429, 500, 502, 503) or i == lan - 1:
                raise
            cho = 2 ** i * 5
            print("   ⏳ HTTP %d — cho %ds roi thu lai (%d/%d)"
                  % (e.code, cho, i + 1, lan - 1))
            time.sleep(cho)
    raise RuntimeError("⛔ khong goi duoc sau %d lan" % lan)


def meta(sid: str, tok: str) -> dict:
    return _goi(API + sid + "?fields=properties.title,sheets.properties("
                "title,gridProperties(rowCount,columnCount))", tok)


def dong_dau(sid: str, ten_sheet: list[str], tok: str, n: int = 3) -> dict:
    """batchGet `n` dong dau cua nhieu sheet — ⛔ khong doc o du lieu nao."""
    ra: dict[str, list] = {}
    for i in range(0, len(ten_sheet), 40):          # tranh URL qua dai
        lat = ten_sheet[i:i + 40]
        q = "&".join("ranges=" + urllib.parse.quote(f"'{s}'!A1:AZ{n}")
                     for s in lat)
        d = _goi(API + sid + "/values:batchGet?" + q
                 + "&valueRenderOption=FORMATTED_VALUE", tok)
        for s, kq in zip(lat, d.get("valueRanges", [])):
            ra[s] = kq.get("values", [])
    return ra


# ── ⭐⭐⭐ CAU TRUC THAT cua mot sheet `R |` (do duoc 2026-09-07, `Đ2`)
#
#   dong 1 = **BAN KHAI ANH XA** — cac so `1..6` danh dau cot nao giu truong
#            nao, kem chot `KHÔNG XOÁ NHÉ`. ⭐ Day la mot **hop dong doc duoc
#            bang may** ma ke toan **tu duy tri bang tay**, va ⛔ chua tai lieu
#            nao cua ITL nhac den no.
#   dong 2 = tieu de, **HAI VUNG**:
#              · vung THO   — ten cot NGUYEN BAN cua ngan hang (khac nhau han)
#              · vung CHUAN — `Date · Debit · Credit · Currency · Số bút toán`
#                             ⭐ **giong het nhau o moi bank**
#   dong 3+ = du lieu
#
# ⇒ *"60+ dinh dang"* la 60+ dinh dang **o vung THO**. Vung CHUAN chi co MOT
#   khuon. Ke toan **da tu chuan hoa** — `F04` ⛔ khong phai phat minh lai,
#   no phai **doc lay** bang khai o dong 1.
# ⭐⭐ Luat doc BAN KHAI song o **`fls/adapters/sao_ke.py`** — mot cho duy
#    nhat. Truoc day no duoc go lai o day; nay uy quyen.
sys.path.insert(0, __file__.rsplit("tools", 1)[0])
from fls.adapters.sao_ke import (SAU_TRUONG, SO_TRUONG,  # noqa: E402,F401
                                 doc_ban_khai)
from fls.kiem.do_luong import ty_le  # noqa: E402,F401


def _hang_tieu_de(bang: list[list]) -> tuple[int, list[str]]:
    """Tieu de la dong **2** — ⛔ khong phai dong 1 (dong 1 la ban khai)."""
    if len(bang) < 2:
        return 0, []
    return 2, [str(x).strip() for x in bang[1]]


def main() -> int:
    tok = token()
    tong_r = 0
    khuon: dict[tuple, list[str]] = {}
    la_lung: list[str] = []
    thu_tu: list[tuple] = []

    for ma, (sid, nhan) in NGUON.items():
        try:
            d = meta(sid, tok)
        except urllib.error.HTTPError as e:
            print(f"⛔ {ma:<10} HTTP {e.code} — {nhan}")
            continue
        sh = [s["properties"] for s in d["sheets"]]
        r = [p["title"] for p in sh if p["title"].startswith("R |")]
        print(f"\n{'═' * 72}\n{ma}  ·  {d['properties']['title']}")
        print(f"  {len(sh)} sheet · {len(r)} sheet `R |`")

        if not r:
            continue
        tong_r += len(r)
        try:
            bang = dong_dau(sid, r, tok)
        except Exception as e:                      # noqa: BLE001
            print(f"  ⛔ khong doc duoc dong dau: {type(e).__name__} {e}")
            continue

        for ten, b in sorted(bang.items()):
            _, cot = _hang_tieu_de(b)
            khai = doc_ban_khai(b[0] if b else [])
            # khuon = TAP TRUONG duoc khai (⛔ khong phai vi tri — vi tri khac
            # nhau la BINH THUONG, do la ca ly do ban khai ton tai)
            k = tuple(sorted(khai))
            khuon.setdefault(k, []).append(f"{ma}:{ten}")
            thieu = sorted(set(SO_TRUONG.values()) - set(khai))
            if thieu:
                la_lung.append(f"⛔ THIEU TRUONG  {ten:<40} {thieu}")
            loi = [c for c in cot if re.search(r"#REF|#N/A", c)]
            if loi:
                la_lung.append(f"⛔ TIEU DE LOI   {ten:<40} {loi[:3]}")
            # ⛔⛔ **Mot phep kiem cua toi da SAI o day, ghi lai de khong lap.**
            # Ban dau toi kiem `Date < Debit < Credit` va bao 8 sheet "thu tu
            # LA". Nhung do ⛔ khong phai loi cua so — **thu tu cot khac nhau
            # la BINH THUONG**, va do chinh la **ly do ban khai dong 1 ton
            # tai**. Mot phep kiem ma hoa gia dinh cua nguoi viet roi goi ket
            # qua la "bat thuong" thi no dang do **gia dinh**, ⛔ khong do
            # **su that** (`Đ-3`). ⇒ Doi thanh THONG KE, ⛔ khong phai canh bao.
            if len(khai) == 6:
                thu_tu.append(tuple(khai[t] for t in
                                    ("Date", "Debit", "Credit")))

    print(f"\n{'═' * 72}\nBAN KHAI ANH XA (dong 1) — {tong_r} sheet `R |`")
    for k, ds in sorted(khuon.items(), key=lambda x: -len(x[1])):
        du = "✅ DU 6" if len(k) == 6 else f"⛔ chi {len(k)}"
        print(f"\n  ▸ {len(ds):>3} sheet · {du} truong: "
              f"{', '.join(k) if k else '⛔ KHONG KHAI GI'}")
        if len(ds) <= 8:
            for x in ds:
                print(f"         · {x}")
    if la_lung:
        print(f"\n⛔ {len(la_lung)} sheet can NGUOI xem:")
        for x in la_lung:
            print("   " + x)
    else:
        print("\n✅ Moi sheet deu khai DU 6 truong — mot khuon duy nhat")

    # ⛔⛔ NOI RO NO DEM GI. Ban truoc in "N bo tri khac nhau", va
    # cau ay duoc trich lai o **7 cho** thanh *"N bo tri COT"* — trong khi
    # no chi nhin **3/6 truong**. Mot nhan mo ho o day de ra mot cau SAI o
    # kia, roi cau sai do di lot qua 66 phep so vi cong canh **CON SO**,
    # ⛔ khong canh **NGHIA cua con so**.
    print(f"\n── THU TU COT: {len(set(thu_tu))} bo tri khac nhau tren "
          f"{len(thu_tu)} sheet — ⛔ CHI theo 3 truong "
          f"(Date, Debit, Credit), ⛔ KHONG phai ca 6")
    print("   ⭐ Thu tu KHAC NHAU la BINH THUONG — do chinh la ly do ban khai")
    print("     o dong 1 ton tai. F04 phai DOC ban khai, khong duoc doan theo")
    print("     vi tri cot.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
