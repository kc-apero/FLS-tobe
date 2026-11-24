# -*- coding: utf-8 -*-
"""Dựng BỂ GIỮ RIÊNG cho A2.04 *ghép theo nội dung* — `WO-338` (thẻ `a3-1-ref`, quyết chủ C5 · BG-330).

    python tools/dung_be_giu_rieng.py --doc-song          # đọc SA CHỈ-ĐỌC → dựng bể A + B → ghi NGOÀI repo
    python tools/dung_be_giu_rieng.py --tu-tep NGUON.json # dựng lại từ bản thô đã đọc (⛔ đọc sheet)
    python tools/dung_be_giu_rieng.py --kiem              # chỉ đọc lại DEM_BE.json, in số, exit 0 ⇔ mọi tầng = mong

⭐ HAI BỂ *(lời chủ 23/11: "test trên dữ liệu cũ và dữ liệu thật hiện tại")*
   **A · dữ liệu CŨ**  : ca chỉ từ KỲ ĐÃ CHỐT *theo bản đóng băng DT12 trong repo*
                         (`tests/fixture/dap_an/itl_ledge_cac_ky.json`, kỳ < kỳ mở lúc đóng băng 20/11).
   **B · dữ liệu THẬT hiện tại**: ca từ MỌI kỳ của lượt đọc HÔM CHẠY; kỳ ĐÃ CHỐT (< tháng chạy) ⇒ đáp án Final;
                         kỳ ĐANG MỞ (≥ tháng chạy) ⇒ nhãn `chua_chot`, ⛔ tính vào recall chính.
   Hai bể dùng CÙNG phép phân tầng + CÙNG mong; khác nhau ở tập kỳ và ở hạt giống.

⭐ ĐÁP ÁN *(định nghĩa tác nghiệp — ghi rõ để chủ duyệt, ⛔ giấu)*
   · nhóm `phai_noi` (hình A·B·C của `pm_join.xep_ca_lat`): đáp án = `ID PMLine` ở `Transaction Mapping L1` (cột N) —
     CHỈ nhận khi (i) cột N không phải ô lỗi VÀ (ii) = dòng lệnh chi mà `pm_join` chọn. Hai vế lệch ⇒ ca BỊ LOẠI và ĐẾM
     (`loai_dap_an_mau_thuan`), ⛔ im lặng.
   · nhóm `phai_nguoi` (D·E·F): đáp án = `DE_NGUOI`.
   · nhóm `l3` (bank có, FPS ⛔ có mã khớp): đáp án = `DE_NGUOI` — AS-IS ⛔ có mối nối *(`#N/A` ở `Mapping L1`)*;
     agent đề xuất nối ⇒ chấm 0 *(nối ⛔ có đáp án Final)*. ⚠ Đây là chấm NGHIÊM; `human-verified` L3 là việc sau.
   · ⚠ `Mapping L1` là kết quả VLOOKUP theo Reference No của AS-IS, ⛔ gồm các lần người đè ở `_adjust`: nó là
     "đáp án Final" ở mức dòng-lệnh-chi, ⛔ ở mức HD/CDT1. Khai ở BG-339.

⛔ RIÊNG TƯ: bản thô + bể chỉ ở thư mục NGOÀI repo (`FLS_HELDOUT_NOI_DUNG`, dir 700, tệp 600). Mã dòng lệnh chi trong ca
   là BÍ DANH `PM-<10 chữ cái>` (HMAC theo muối của bể, ⛔ chữ số) — tên người/mã thật ⛔ vào ca. Repo chỉ có `DEM_BE.json` (đếm + vân tay muối).
"""
from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import random
import re
import secrets
import sys
import time
import urllib.parse
from collections import Counter, defaultdict
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.adapters.pm_join import (  # noqa: E402
    PM_COT, DongBank, DongPM, canon_ref, kiem_tieu_de_pm, xep_ca_lat,
)
from fls.canon.o_loi import la_o_loi  # noqa: E402
from fls.canon.tien_te import ma_tien_te  # noqa: E402
from fls.canon.validate import parse_so  # noqa: E402

BIEN = "FLS_HELDOUT_NOI_DUNG"
DE_NGUOI = "DE_NGUOI"
SID_RAW = "1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E"        # ITL … 1/2 (RAW) — `tools/do_khoa_ghep.py`
SID_ADJ = "1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA"        # ITL … 2/2 (ADJUSTED) — `tools/doc_itl_ledge_ky.py`
TAB_L1, TAB_PM, TAB_LEDGE = "Transaction Mapping L1", "[Importrange]PM_Unpivot", "ITL Ledge"
L1_DONG1, PM_DONG1, LEDGE_DONG1, LEDGE_CUOI = 4, 3, 10, 12684
#: Cột `Mapping L1` dùng: ngày · số chứng từ · diễn giải · tiền tệ · Nợ · Có · … · ID PMLine (cột N, vị trí 13).
L1_COT = {"ngay": 0, "so_ct": 1, "dien_giai": 2, "cur": 3, "no": 4, "co": 5, "tk": 6, "id_pmline": 13}
L1_TIEU_DE_MONG_DOI = {0: "Ngày chứng từ", 1: "Số chứng từ", 2: "Diễn giải", 3: "Đơn vị tiền tệ", 4: "PS Nợ", 5: "PS Có",
                       13: "ID PMLine"}
EPOCH = dt.date(1899, 12, 30)
TEP_KY_DONG_BANG = GOC / "tests" / "fixture" / "dap_an" / "itl_ledge_cac_ky.json"
TEP_DEM = GOC / "docs" / "ITL" / "05_FleetEval" / "be" / "DEM_BE.json"
TEP_CA_DUNG = GOC / "tests" / "fixture" / "agent" / "ca_noi_dung_dung.json"
TM_SKILL = GOC / "fls" / "agent" / "skill"
HAT = 338

#: ⭐ `mong` MỖI TẦNG *(Đ4: mỗi số đếm một vật — số MÃ tham chiếu, trừ L3/chuyển/chưa chốt là số DÒNG bank)*.
#: Theo thẻ `a3-1-ref §C`: toàn bộ D (5 mã) + 10 E + 10 F + 10 C + 5 B + 10 A + 10 L3 (5 không-Ref + 5 mã-khác) + ca chuyển.
MONG_TANG: dict[str, int] = {"D": 5, "E": 10, "F": 10, "C": 10, "B": 5, "A": 10,
                             "L3_khong_ref": 5, "L3_ma_khac": 5, "chuyen": 5}
MONG_CHUA_CHOT = 5                       # chỉ bể B: ca từ kỳ ĐANG MỞ, nhãn `chua_chot`
NHOM_CUA = {"A": "phai_noi", "B": "phai_noi", "C": "phai_noi", "D": "phai_nguoi", "E": "phai_nguoi", "F": "phai_nguoi",
            "L3_khong_ref": "l3", "L3_ma_khac": "l3"}


# ───────────────────────────── đọc nguồn (SA chỉ-đọc) ─────────────────────────────
PHAM_VI_DOC = ["https://www.googleapis.com/auth/spreadsheets.readonly"]   # ⛔ chỉ đọc (QĐ-ITL-34)


def cach_xac_thuc(mt: dict[str, str] | None = None) -> str:
    """TÊN cách lấy quyền đọc sheet (⛔ giá trị). `WO-359` AC-4: chạy được ở Cloud Shell của chủ — thứ tự dừng ở cái đầu:
    ① `FLS_SHEETS_TOKEN` (access token đưa sẵn) ② `FLS_SHEETS_SA_JSON_TEP` (ĐƯỜNG DẪN tệp khoá SA, chmod 600 — ⛔ nội dung
    khoá qua biến) ③ `FLS_GSHEETS_SA_JSON(_B64)` (environment secrets của phiên cloud — đường cũ WO-338). Khuôn theo
    `tools/staging/cred_sheets.py` (nhánh STG-NAP) nhưng ⛔ phụ thuộc nó (nhánh này ⛔ có tệp ấy)."""
    mt = os.environ if mt is None else mt
    for k in ("FLS_SHEETS_TOKEN", "FLS_SHEETS_SA_JSON_TEP", "FLS_GSHEETS_SA_JSON", "FLS_GSHEETS_SA_JSON_B64"):
        if mt.get(k):
            return k
    raise RuntimeError("⛔ thiếu quyền đọc sheet: đặt FLS_SHEETS_TOKEN · FLS_SHEETS_SA_JSON_TEP · FLS_GSHEETS_SA_JSON(_B64)")


def _phien():
    from google.auth.transport.requests import AuthorizedSession
    from google.oauth2 import service_account
    cach = cach_xac_thuc()
    if cach == "FLS_SHEETS_TOKEN":
        from google.oauth2.credentials import Credentials
        return AuthorizedSession(Credentials(token=os.environ["FLS_SHEETS_TOKEN"]))
    if cach == "FLS_SHEETS_SA_JSON_TEP":
        return AuthorizedSession(service_account.Credentials.from_service_account_file(
            os.environ["FLS_SHEETS_SA_JSON_TEP"], scopes=PHAM_VI_DOC))
    raw = os.environ.get("FLS_GSHEETS_SA_JSON") or base64.b64decode(os.environ["FLS_GSHEETS_SA_JSON_B64"]).decode()
    return AuthorizedSession(service_account.Credentials.from_service_account_info(json.loads(raw), scopes=PHAM_VI_DOC))


def _lay(s, sid: str, vung: str, lan: int = 4) -> list[list]:
    u = f"https://sheets.googleapis.com/v4/spreadsheets/{sid}/values/{urllib.parse.quote(vung)}"
    loi = "?"
    for t in range(1, lan + 1):
        try:
            r = s.get(u, params={"valueRenderOption": "UNFORMATTED_VALUE", "dateTimeRenderOption": "SERIAL_NUMBER"},
                      timeout=170)
            if r.status_code == 200:
                return r.json().get("values", [])
            loi = f"HTTP {r.status_code}"
        except Exception as e:                       # noqa: BLE001 — mạng/hết giờ: thử lại
            loi = type(e).__name__
        time.sleep(3 * t)
    raise RuntimeError(f"⛔ không đọc được `{vung[:40]}` sau {lan} lần: {loi}")


def doc_nguon_song(lat: int = 2500, luu=None) -> dict[str, Any]:
    """Một lượt đọc CHỈ-ĐỌC → bản thô `{l1, pm, pm_tieu_de, l1_tieu_de, ledge_ngay, ngay_doc}`. ⛔ in giá trị."""
    s = _phien()
    q = lambda t: "'" + t + "'"                     # noqa: E731
    nguon: dict[str, Any] = {"ngay_doc": dt.date.today().isoformat(), "l1": [], "pm": [], "ledge_ngay": []}
    nguon["l1_tieu_de"] = (_lay(s, SID_RAW, f"{q(TAB_L1)}!A3:N3") or [[]])[0]
    nguon["pm_tieu_de"] = (_lay(s, SID_RAW, f"{q(TAB_PM)}!A2:Z2") or [[]])[0]
    for a in range(L1_DONG1, 14269 + 1, lat):
        nguon["l1"] += _lay(s, SID_RAW, f"{q(TAB_L1)}!A{a}:N{min(a + lat - 1, 14269)}")
    nguon["pm"] = _lay(s, SID_RAW, f"{q(TAB_PM)}!A{PM_DONG1}:Z4412")
    if luu:
        luu(nguon)                                   # ⭐ lưu thô TRƯỚC Ledge: lượt 23/11 mất 16 phút vì Ledge hết giờ
    nguon["ledge_loi"] = []
    for a in range(LEDGE_DONG1, LEDGE_CUOI + 1, 1500):
        vung = f"{q(TAB_LEDGE)}!A{a}:A{min(a + 1499, LEDGE_CUOI)}"
        try:
            nguon["ledge_ngay"] += [r[0] if r else None for r in _lay(s, SID_ADJ, vung)]
        except RuntimeError as e:                    # lát hỏng ⇒ CÓ TÊN, ⛔ bỏ im
            nguon["ledge_loi"].append(vung.split("!")[1])
            nguon["ledge_ngay"] += [None] * (min(a + 1499, LEDGE_CUOI) - a + 1)
    return nguon


# ───────────────────────────── phần THUẦN (test được bằng nguồn giả) ─────────────────────────────
def _ngay(v: Any) -> dt.date | None:
    if isinstance(v, bool) or v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return EPOCH + dt.timedelta(days=int(v))
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", str(v).strip())
    return dt.date(int(m[1]), int(m[2]), int(m[3])) if m else None


def _dec(v: Any) -> Decimal | None:
    try:
        x = parse_so(v)
        return None if x is None else Decimal(str(x))
    except (ValueError, InvalidOperation):
        return None


@dataclass(frozen=True)
class DongNguon:
    dong: int
    ngay: dt.date
    ref: str | None
    nd: str
    cur: str
    tien: Decimal
    id_l1: str | None            # `ID PMLine` ở Mapping L1 (None = ô lỗi/rỗng)
    tk: str = ""                 # cột G `Tài khoản` của `Mapping L1` — ⭐ HELD-R1-02: chủ 23/11 ~06:00 "agent đọc TOÀN BỘ nội dung + số TK"


def kiem_tieu_de(nguon: dict) -> list[str]:
    """Đ5: tiêu đề lệch mong đợi ⇒ ĐỎ có tên (⛔ đọc lệch cột rồi 'xanh')."""
    loi = []
    td = nguon.get("l1_tieu_de") or []
    for i, ten in L1_TIEU_DE_MONG_DOI.items():
        if i >= len(td) or str(td[i]).strip() != ten:
            loi.append(f"Mapping L1 cột {i}: mong `{ten}`")
    try:
        kiem_tieu_de_pm(nguon.get("pm_tieu_de") or [])
    except Exception as e:                           # noqa: BLE001
        loi.append(f"PM_Unpivot: {type(e).__name__}")
    return loi


def _tk(v: Any) -> str:
    """Số TK dạng chữ: Sheets UNFORMATTED trả SỐ cho ô toàn chữ số (`1.2345E+10` ⛔ — ép nguyên khi là số nguyên)."""
    if v is None or isinstance(v, bool):
        return ""
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    return str(v).strip()


def doc_bank(nguon: dict) -> tuple[list[DongNguon], dict[str, int]]:
    ra, bo = [], Counter()
    for i, r in enumerate(nguon["l1"]):
        r = list(r) + [None] * 14
        ng, no, co = _ngay(r[0]), _dec(r[4]), _dec(r[5])
        if ng is None:
            bo["khong_co_ngay"] += 1
            continue
        cur = ma_tien_te(str(r[3] or ""))
        if not cur:
            bo["khong_co_tien_te"] += 1
            continue
        id_l1 = None if (r[13] in (None, "") or la_o_loi(r[13])) else str(r[13]).strip()
        ra.append(DongNguon(L1_DONG1 + i, ng, canon_ref(r[1]), str(r[2] or ""), cur, (no or Decimal(0)) + (co or Decimal(0)),
                            id_l1, _tk(r[L1_COT["tk"]])))
    return ra, dict(bo)


def doc_pm(nguon: dict) -> tuple[list[DongPM], dict[str, int]]:
    ra, bo = [], Counter()
    for i, r in enumerate(nguon["pm"]):
        r = list(r) + [None] * 26
        line = str(r[PM_COT["line"]] or "").strip()
        if not line or la_o_loi(line):
            bo["khong_co_line"] += 1
            continue
        cur = ma_tien_te(str(r[PM_COT["cur"]] or ""))
        ra.append(DongPM(PM_DONG1 + i, str(r[PM_COT["slip"]] or ""), line, _dec(r[PM_COT["tien"]]), cur or "",
                         str(r[PM_COT["status"]] or ""), canon_ref(r[PM_COT["ref"]]), None, None,
                         str(r[PM_COT["ref"]] or "")))
    return ra, dict(bo)


def ngay_pm(nguon: dict) -> dict[str, dt.date | None]:
    return {str(r[PM_COT["line"]]).strip(): _ngay(r[0] if r else None) for r in nguon["pm"] if len(r) > PM_COT["line"]}


def ky_cua(d: dt.date) -> str:
    return f"{d.year}-{d.month:02d}"


MAU_TOKEN = re.compile(r"[A-Za-z0-9]{8,}")
#: Hình của mã Reference ở PM_Unpivot — đo 23/11 trên 3.909 dòng lệnh chi: `FT…` 1.617 · `IBDN…` 526 · `PC…` 470 (+ số thuần 300).
#: Thẻ `a3-1-ref` tầng L3 "diễn giải ghi mã KHÁC" = nội dung có một mã DẠNG Reference mà ⛔ phải Số chứng từ của dòng.
#: ⚠ Định nghĩa "mã khớp một dòng PM có thật" chỉ cho 1 dòng/12.710 (đo) ⇒ ⛔ đủ làm tầng; dùng HÌNH mã.
MAU_MA_DANG_REF = re.compile(r"(?<![A-Za-z0-9])(?:FT|IBDN|PC)[0-9A-Z]{5,}(?![A-Za-z0-9])")


@dataclass
class Ung:
    """Một ứng viên-ca: MỘT mã (hình A–F) hoặc MỘT dòng bank L3."""
    tang: str
    ky: str
    dong: DongNguon
    pm_dung: tuple[DongPM, ...]          # dòng lệnh chi của mã (rỗng với L3)
    hinh: str


def phan_tang(bank: list[DongNguon], pm: list[DongPM]) -> tuple[list[Ung], dict[str, Any]]:
    """⭐ Phân tầng CHÍNH `pm_join.xep_ca_lat` (⛔ viết lại luật ghép) + L3 theo `ThongKeGhep`."""
    theo_dong = {b.dong: b for b in bank}
    nhom, tk = xep_ca_lat([DongBank(b.dong, b.ref, b.tien, b.cur) for b in bank], pm)
    pm_ref = {p.ref for p in pm if p.ref}
    ra: list[Ung] = []
    loai = Counter()
    for n in nhom:
        rep = theo_dong[min(x.dong_sheet for x in n.bank)]
        if n.hinh in ("A", "B", "C"):
            # đáp án phải KHỚP Mapping L1 (ô cột N) — lệch ⇒ loại + đếm
            if rep.id_l1 is None or rep.id_l1 != n.pm[0].line:
                loai[f"{n.hinh}:dap_an_mau_thuan"] += 1
                continue
        ra.append(Ung(n.hinh, ky_cua(rep.ngay), rep, tuple(n.pm), n.hinh))
    ma_ghep = {x.ref for n in nhom for x in n.bank if x.ref}
    for b in bank:
        if b.ref in ma_ghep:
            continue
        if not b.ref:
            ra.append(Ung("L3_khong_ref", ky_cua(b.ngay), b, (), "L3"))
        else:                                               # mã bank ⛔ có ở PM
            tk_nd = {canon_ref(t) for t in MAU_TOKEN.findall(b.nd)}
            ma_khac = {canon_ref(t) for t in MAU_MA_DANG_REF.findall(b.nd.upper())} - {b.ref}
            if (tk_nd & pm_ref) or ma_khac:
                ra.append(Ung("L3_ma_khac", ky_cua(b.ngay), b, (), "L3"))
            else:
                loai["L3_khac(⛔ vào tầng nào)"] += 1
    return ra, {"theo_hinh": dict(tk.theo_hinh), "dong_theo_hinh": dict(tk.dong_theo_hinh),
                "khong_co_ma": tk.khong_co_ma, "khong_thay_ma_PM": tk.khong_thay_ma_PM, "loai": dict(loai)}


CHU_BI_DANH = "ABCDEFGHJKMNPQRSTVWXYZ"           # 22 chữ cái, ⛔ chữ số


def alias_pm(muoi: bytes, line: str) -> str:
    """Bí danh `PM-<10 chữ cái>`. ⛔ HEX: đo 23/11 — 10 hex có ~0,9% toàn chữ số ⇒ lớp 2 của bộ che (`che.kiem_den`:
    dãy ≥ 9 số / số điện thoại) nhầm là số TK và TỪ CHỐI cả lời gọi (bể ~300 bí danh ⇒ gần như chắc chắn dính)."""
    d = hmac.new(muoi, line.encode(), hashlib.sha256).digest()
    return "PM-" + "".join(CHU_BI_DANH[b % len(CHU_BI_DANH)] for b in d[:10])


def _so(x: Decimal) -> int | float:
    return int(x) if x == x.to_integral_value() else float(x)


def _ung_vien(u: Ung, pm: list[DongPM], ngay_pm_: dict, muoi: bytes, rng: random.Random) -> list[dict]:
    """Ứng viên = dòng lệnh chi ĐÚNG của mã (≤3) + mồi cùng tiền tệ, tiền gần nhất (≤2; L3: ≤3 + dòng ghi trong nội dung)."""
    dung = list(u.pm_dung)[:3]
    co = {p.line for p in dung}
    nd_ref = ({canon_ref(t) for t in MAU_TOKEN.findall(u.dong.nd)} | {canon_ref(t) for t in MAU_MA_DANG_REF.findall(u.dong.nd.upper())}
              if u.hinh == "L3" else set())
    moi = sorted((p for p in pm if p.line not in co and p.cur == u.dong.cur and p.tien is not None),
                 key=lambda p: (abs(p.tien - u.dong.tien), p.line))
    ten_moi = [p for p in moi if p.ref in nd_ref][:1]            # L3_ma_khac: dòng mà nội dung nhắc tới
    them = ten_moi + [p for p in moi if p not in ten_moi][: (3 if u.hinh == "L3" else 2) - len(ten_moi)]
    ra = []
    for p in dung + them:
        d = ngay_pm_.get(p.line)
        ra.append({"pm": alias_pm(muoi, p.line), "tien": _so(p.tien) if p.tien is not None else None, "cur": p.cur or None,
                   "ngay": d.isoformat() if d else None})
    rng.shuffle(ra)                                              # ⛔ vị trí ứng viên đúng không lộ
    return ra


def chon_ca(ung: list[Ung], ky_cho_phep: set[str], ky_mo: set[str], ky_chuyen: str | None, rng: random.Random,
            la_b: bool) -> tuple[dict[str, list[Ung]], dict[str, list[str]]]:
    """Chọn theo tầng. Tầng `chuyen` lấy từ kỳ chốt MỚI NHẤT (⛔ trùng tầng khác); `chua_chot` (chỉ B) từ kỳ mở."""
    ra: dict[str, list[Ung]] = {}
    thieu: dict[str, list[str]] = {}
    dung = sorted((u for u in ung if u.ky in ky_cho_phep), key=lambda u: (u.dong.dong, u.tang))
    chuyen_pool = [u for u in dung if u.ky == ky_chuyen and u.ky not in ky_mo]
    chung = [u for u in dung if u.ky != ky_chuyen and u.ky not in ky_mo]
    for t, n in MONG_TANG.items():
        pool = chuyen_pool if t == "chuyen" else [u for u in chung if u.tang == t]
        ra[t] = pool if (t == "D" and len(pool) <= n) else rng.sample(pool, min(n, len(pool)))
    if la_b:
        mo = [u for u in dung if u.ky in ky_mo]
        ra["chua_chot"] = rng.sample(mo, min(MONG_CHUA_CHOT, len(mo)))
    mong = dict(MONG_TANG) | ({"chua_chot": MONG_CHUA_CHOT} if la_b else {})
    for t, n in mong.items():
        if len(ra[t]) != n:                                      # Đ5: cả hai chiều
            thieu[t] = [f"mong {n} · có {len(ra[t])}"]
    return ra, thieu


BIEN_MUOI = "FLS_MUOI_BE"


def muoi_be(ten: str) -> bytes:
    """Muối vân tay 128 bit của bể `ten`. ⭐ `HELD-R1-05`: bản R0 `secrets.token_bytes` mỗi lần dựng ⇒ dựng lại ĐÚNG
    (mọi đếm khớp) vẫn ĐỎ `test_BE_van_tay_khop_tep_dem_repo`. Nay DẪN XUẤT từ một bí mật ngoài repo, bền qua container:
    `FLS_MUOI_BE` (hex) nếu có, ngược lại khoá SA chỉ-đọc (secret của môi trường) ⇒ `HMAC-SHA256(bí mật, "be/<ten>")[:16]`.
    ⛔ không bí mật nào ⇒ ngẫu nhiên (bể GIẢ của bài thử; vân tay lúc ấy ⛔ so với tệp đếm của repo)."""
    bi_mat = os.environ.get(BIEN_MUOI) or os.environ.get("FLS_GSHEETS_SA_JSON_B64") or os.environ.get("FLS_GSHEETS_SA_JSON")
    if not bi_mat:
        return secrets.token_bytes(16)
    return hmac.new(bi_mat.encode(), f"fls-be-giu-rieng/{ten}".encode(), hashlib.sha256).digest()[:16]


def dung_be(nguon: dict, *, ten: str, ky_chot_dong_bang: set[str], ky_mo_ngay_chay: set[str], hat: int = HAT) -> dict[str, Any]:
    """Dựng MỘT bể (`ten` = `a` | `b`). Trả `{ca, dap_an, meta, muoi, dem, do}` — chưa ghi đĩa."""
    la_b = ten == "b"
    bank, bo_b = doc_bank(nguon)
    pm, bo_p = doc_pm(nguon)
    ung, th = phan_tang(bank, pm)
    ngay_pm_ = ngay_pm(nguon)
    tat_ca_ky = {ky_cua(b.ngay) for b in bank}
    if la_b:
        ky_cho_phep, ky_mo = tat_ca_ky, ky_mo_ngay_chay & tat_ca_ky
        ky_chot = tat_ca_ky - ky_mo
    else:
        ky_cho_phep = ky_chot = tat_ca_ky & ky_chot_dong_bang
        ky_mo = set()
    ky_chuyen = max(ky_chot) if ky_chot else None
    rng = random.Random(hat + (1 if la_b else 0))
    muoi = muoi_be(ten)
    chon, thieu = chon_ca(ung, ky_cho_phep, ky_mo, ky_chuyen, rng, la_b)
    thu_tu = [(t, u) for t, us in chon.items() for u in us]
    rng.shuffle(thu_tu)                                          # id ca ⛔ lộ tầng
    ca, dap, meta = {}, {}, {}
    for i, (t, u) in enumerate(thu_tu, 1):
        c = f"c{i:03d}"
        ca[c] = {"tien": _so(u.dong.tien), "cur": u.dong.cur, "ngay": u.dong.ngay.isoformat(), "tk": u.dong.tk,
                 "noi_dung": u.dong.nd, "ung_vien": _ung_vien(u, pm, ngay_pm_, muoi, rng)}
        if t == "chua_chot" or u.ky in ky_mo:
            nhom = "chua_chot"
            chon_pm = alias_pm(muoi, u.pm_dung[0].line) if u.hinh in ("A", "B", "C") else DE_NGUOI
        elif u.hinh in ("A", "B", "C"):
            nhom, chon_pm = "phai_noi", alias_pm(muoi, u.pm_dung[0].line)
        else:
            nhom, chon_pm = NHOM_CUA[u.tang], DE_NGUOI
        dap[c] = {"chon": chon_pm, "nhom": nhom}
        meta[c] = {"tang": t, "tang_goc": u.tang, "hinh": u.hinh, "ky": u.ky, "chua_chot": nhom == "chua_chot",
                   "so_ct": u.dong.ref}
    dem = {t: len(us) for t, us in chon.items()}
    return {"ten": ten, "ca": {"ca": ca}, "dap_an": {"noi": dap}, "meta": meta, "muoi": muoi, "dem": dem,
            "thieu": thieu, "ky_cho_phep": sorted(ky_cho_phep), "ky_chot": sorted(ky_chot), "ky_mo": sorted(ky_mo),
            "vu_tru": {"theo_hinh_ma": th["theo_hinh"], "dong_theo_hinh": th["dong_theo_hinh"],
                       "khong_co_ma": th["khong_co_ma"], "khong_thay_ma_PM": th["khong_thay_ma_PM"],
                       "loai": th["loai"], "dong_bank": len(bank), "dong_pm": len(pm), "bo_bank": bo_b, "bo_pm": bo_p,
                       "bank_theo_ky": dict(sorted(Counter(ky_cua(b.ngay) for b in bank).items()))}}


# ───────────────────────────── độc lập (AC-2) ─────────────────────────────
def _chuan_nd(s: str) -> str:
    return re.sub(r"\s+", " ", str(s or "")).strip().upper()


def van_tay_ca(c: dict, muoi: bytes) -> str:
    k = json.dumps([c["tien"], c["cur"], c["ngay"], _chuan_nd(c["noi_dung"])], ensure_ascii=False)
    return hmac.new(muoi, k.encode(), hashlib.sha256).hexdigest()[:12]


def trung_voi_ca_dung(ca: dict, tep_dung: Path = TEP_CA_DUNG) -> int:
    """Số ca của bể TRÙNG ca dựng WO-329 (cùng tiền + tiền tệ + ngày, HOẶC cùng nội dung chuẩn hoá)."""
    dung = json.loads(tep_dung.read_text(encoding="utf-8"))["ca"]
    kb = {(c["tien"], c["cur"], c["ngay"]) for c in dung.values()}
    nd = {_chuan_nd(c["noi_dung"]) for c in dung.values() if c.get("noi_dung")}
    return sum(1 for c in ca["ca"].values()
               if (c["tien"], c["cur"], c["ngay"]) in kb or (c["noi_dung"] and _chuan_nd(c["noi_dung"]) in nd))


def trung_voi_prompt(ca: dict, thu_muc: Path = TM_SKILL) -> int:
    """Số ca có nội dung (≥ 8 ký tự, chuẩn hoá) nằm NGUYÊN VĂN trong chữ prompt/ví dụ của agent, hoặc cả bộ
    `tiền · tiền tệ · ngày` cùng nằm trong MỘT tệp prompt. Tập tệp ⛔ rỗng (Đ3) — gọi bởi bài, đếm mẫu số trước."""
    tep = [p for p in thu_muc.rglob("*") if p.is_file() and p.suffix in (".md", ".txt", ".json", ".yaml", ".yml", ".py")]
    van = {p: _chuan_nd(p.read_text(encoding="utf-8", errors="ignore")) for p in tep}
    n = 0
    for c in ca["ca"].values():
        nd = _chuan_nd(c["noi_dung"])
        if len(nd) >= 8 and any(nd in v for v in van.values()):
            n += 1
        elif any(str(c["tien"]) in v and c["cur"] in v and c["ngay"] in v for v in van.values()):
            n += 1
    return n


def so_tep_prompt(thu_muc: Path = TM_SKILL) -> int:
    return sum(1 for p in thu_muc.rglob("*") if p.is_file())


# ───────────────────────────── ghi ─────────────────────────────
def thu_muc_be(goc: Path, ten: str) -> Path:
    return goc / ten


def ghi_be(goc: Path, be: dict) -> Path:
    d = thu_muc_be(goc, be["ten"])
    d.mkdir(parents=True, exist_ok=True)
    os.chmod(goc, 0o700)                  # thư mục bể GỐC cũng 700 (đo 24/11: `--ra` mới tạo ⇒ 755)
    os.chmod(d, 0o700)
    for ten_tep, du in (("ca.json", be["ca"]), ("dap_an.json", be["dap_an"]), ("meta.json", be["meta"])):
        p = d / ten_tep
        p.write_text(json.dumps(du, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        os.chmod(p, 0o600)
    k = d / "muoi.key"
    k.write_bytes(be["muoi"])
    os.chmod(k, 0o600)
    return d


def dem_cua(be: dict, d: Path | None, bo_sung: dict | None = None) -> dict[str, Any]:
    """Tệp ĐẾM của một bể — ⛔ chữ, ⛔ tiền, ⛔ mã. Có vân tay muối từng ca + vân tay cả bể."""
    n_ca = len(be["ca"]["ca"])
    mong = dict(MONG_TANG) | ({"chua_chot": MONG_CHUA_CHOT} if be["ten"] == "b" else {})
    vt = sorted(van_tay_ca(c, be["muoi"]) for c in be["ca"]["ca"].values())
    h = hashlib.sha256(json.dumps(vt).encode()).hexdigest()[:16]
    nhom = Counter(x["nhom"] for x in be["dap_an"]["noi"].values())
    return {
        "nhan": "bể A · dữ liệu CŨ (kỳ đã chốt theo ảnh DT12)" if be["ten"] == "a" else "bể B · dữ liệu THẬT hiện tại",
        "mong_theo_tang": mong, "thuc_theo_tang": be["dem"], "thieu": be["thieu"],
        "tong_ca": n_ca, "mong_tong": sum(mong.values()), "theo_nhom": dict(nhom),
        "ca_theo_ky": dict(sorted(Counter(m["ky"] for m in be["meta"].values()).items())),
        "ky_chot": be["ky_chot"], "ky_mo": be["ky_mo"], "ky_cho_phep": be["ky_cho_phep"],
        "vu_tru": be["vu_tru"], "van_tay_be": h, "van_tay_ca": vt,
        "doc_lap": {"trung_ca_dung_wo329": trung_voi_ca_dung(be["ca"]), "trung_prompt_agent": trung_voi_prompt(be["ca"]),
                    "so_tep_prompt_da_quet": so_tep_prompt()},
        **(bo_sung or {}),
    }


def doi_chieu_ky(ledge_ngay: list, tep: Path = TEP_KY_DONG_BANG) -> dict[str, Any]:
    """Kỳ đã chốt: Ledge Final ĐỌC HÔM NAY ↔ ảnh đóng băng DT12 (dòng/kỳ ở cột A). Lệch ⇒ danh sách CÓ TÊN."""
    dong_bang = json.loads(tep.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"]
    sống = Counter()
    khong_giai = 0
    for v in ledge_ngay:
        d = _ngay(v)
        if d is None:
            khong_giai += 1 if v not in (None, "") else 0
            continue
        sống[ky_cua(d)] += 1
    lech = {k: {"dong_bang": dong_bang.get(k), "song": sống.get(k, 0)}
            for k in sorted(set(dong_bang) | set(sống)) if dong_bang.get(k) != sống.get(k, 0)}
    # ⭐ Phép đo mang nhãn "kỳ ĐÃ CHỐT": kỳ ĐANG MỞ lúc đóng băng (20/11) còn nhận dòng mới ⇒ LỚN LÊN là đúng (đo 23/11 lần
    #   Ledge đọc được: 25 kỳ chốt khớp, chỉ kỳ mở lệch). Bản R0 cho cả kỳ mở vào `ket` ⇒ ĐỎ vì lý do SAI.
    chot = ky_chot_dong_bang(tep)
    lech_chot = {k: v for k, v in lech.items() if k in chot}
    return {"so_ky_dong_bang": len(dong_bang), "so_ky_song": len(sống), "ky_song_khong_co_o_dong_bang":
            sorted(set(sống) - set(dong_bang)), "ky_dong_bang_vang_o_song": sorted(set(dong_bang) - set(sống)),
            "ky_lech_so_dong": lech, "ky_lech_ky_chot": lech_chot, "ky_lech_ky_mo": {k: v for k, v in lech.items() if k not in chot},
            "so_ky_chot_so_sanh": len(chot), "o_ngay_khong_giai_ma": khong_giai, "mau_so_o_ngay_song": sum(sống.values())}


def ky_chot_dong_bang(tep: Path = TEP_KY_DONG_BANG) -> set[str]:
    """Kỳ ĐÃ CHỐT lúc đóng băng = mọi kỳ có dòng, TRỪ kỳ mới nhất (đang mở lúc 20/11)."""
    ks = sorted(json.loads(tep.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"])
    return set(ks[:-1])


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="dung_be_giu_rieng.py")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--doc-song", action="store_true")
    g.add_argument("--tu-tep", type=Path)
    g.add_argument("--kiem", action="store_true")
    p.add_argument("--ra", type=Path, default=None, help=f"thư mục bể (mặc định ${BIEN}) — ⛔ trong repo")
    p.add_argument("--tho", type=Path, default=Path("/tmp/fls_be_tho/nguon.json"))
    p.add_argument("--giu-tho", action="store_true")
    a = p.parse_args(argv)
    if a.kiem:
        d = json.loads(TEP_DEM.read_text(encoding="utf-8"))
        bad = {k: v["thieu"] for k, v in d["be"].items() if v["thieu"]}
        for k, v in d["be"].items():
            print(f"bể {k}: {v['tong_ca']}/{v['mong_tong']} ca · vân tay {v['van_tay_be']} · thiếu {v['thieu'] or 'không'}")
        print("so_ky:", d.get("doi_chieu_A_B", {}).get("ket"))
        return 1 if bad else 0
    ra = a.ra or (Path(os.environ[BIEN]) if os.environ.get(BIEN) else None)
    if ra is None or str(ra.resolve()).startswith(str(GOC.resolve())):
        print(f"⛔ cần ${BIEN} (hoặc --ra) trỏ NGOÀI repo")
        return 2
    if a.tu_tep:
        nguon = json.loads(a.tu_tep.read_text(encoding="utf-8"))
    else:
        a.tho.parent.mkdir(parents=True, exist_ok=True)
        os.chmod(a.tho.parent, 0o700)

        def luu(n: dict) -> None:
            a.tho.write_text(json.dumps(n, ensure_ascii=False), encoding="utf-8")
            os.chmod(a.tho, 0o600)
        nguon = doc_nguon_song(luu=luu)
        luu(nguon)
    loi = kiem_tieu_de(nguon)
    if loi:
        print("⛔ ĐỎ tiêu đề nguồn:", loi)
        return 1
    ngay_chay = dt.date.fromisoformat(nguon["ngay_doc"])
    ky_mo = {ky_cua(ngay_chay)}
    chot_db = ky_chot_dong_bang()
    be_a = dung_be(nguon, ten="a", ky_chot_dong_bang=chot_db, ky_mo_ngay_chay=ky_mo)
    be_b = dung_be(nguon, ten="b", ky_chot_dong_bang=chot_db, ky_mo_ngay_chay=ky_mo)
    da = ghi_be(ra, be_a), ghi_be(ra, be_b)
    dc = doi_chieu_ky(nguon["ledge_ngay"])
    dc["lat_ledge_hong"] = nguon.get("ledge_loi", [])
    # Phép THAY THẾ (khác vật đo — Đ4): dòng bank sống ở `Mapping L1` theo kỳ ↔ dòng Ledge ĐÓNG BĂNG DT12 theo kỳ.
    dbang = json.loads(TEP_KY_DONG_BANG.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"]
    bk = be_a["vu_tru"]["bank_theo_ky"]
    dc["thay_the_bank_song_vs_ledge_dong_bang"] = {
        "mau_so_ky": len(dbang), "ky_lech": {k: {"bank_song": bk.get(k, 0), "ledge_dong_bang": dbang.get(k)}
                                             for k in sorted(set(dbang) | set(bk)) if bk.get(k, 0) != dbang.get(k)}}
    do_duoc = not dc["lat_ledge_hong"] and dc["mau_so_o_ngay_song"] > 0              # Đ3/Đ5: ⛔ đo được ⇒ ĐỎ
    ket_ky = be_a["ky_chot"] == be_b["ky_chot"] and not dc["ky_lech_ky_chot"] and do_duoc
    sys.path.insert(0, str(GOC / "tools"))
    import do_ro_ri_che as rr            # cùng thư mục tools/ — phép đo của TUỲ CHỌN che (chủ 23/11 ~06:00: ⛔ điều kiện chặn)
    out = {"ngay_doc": nguon["ngay_doc"], "ky_mo_ngay_chay": sorted(ky_mo),
           "be": {"a": dem_cua(be_a, da[0], {"ro_ri_che": rr.do(be_a["ca"], be_a["meta"])}),
                  "b": dem_cua(be_b, da[1], {"ro_ri_che": rr.do(be_b["ca"], be_b["meta"])})},
           "doi_chieu_A_B": {"ledge_song_vs_dong_bang": dc, "ky_chot_A": be_a["ky_chot"], "ky_chot_B": be_b["ky_chot"],
                             "ket": "KHỚP" if ket_ky else (f"ĐỎ — ⛔ đo được: Ledge sống ⛔ đọc hết giờ (ô ngày giải mã {dc['mau_so_o_ngay_song']}, lát hỏng {len(dc['lat_ledge_hong'])})" if not do_duoc
                                                else "ĐỎ — kỳ đã chốt lệch (nguồn đã sửa sau chốt?)")}}
    TEP_DEM.parent.mkdir(parents=True, exist_ok=True)
    # ⭐ `AG2-R1-06` (KQ-357): chỉ khác `ngay_doc` ⇒ ⛔ ghi (dựng lại đúng làm cây repo bẩn 1 dòng ngày, dễ lỡ commit).
    cu = json.loads(TEP_DEM.read_text(encoding="utf-8")) if TEP_DEM.exists() else None
    if cu is not None and {**cu, "ngay_doc": None} == {**out, "ngay_doc": None}:
        print(f"  {TEP_DEM.relative_to(GOC)}: mọi số đếm KHÔNG đổi (chỉ ngày đọc) ⇒ ⛔ ghi")
    else:
        TEP_DEM.write_text(json.dumps(out, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    for k, v in out["be"].items():
        print(f"bể {k}: {v['tong_ca']}/{v['mong_tong']} ca · thiếu {v['thieu'] or 'không'} · "
              f"trùng ca dựng {v['doc_lap']['trung_ca_dung_wo329']} · trùng prompt {v['doc_lap']['trung_prompt_agent']}")
    print("đối chiếu kỳ A↔B:", out["doi_chieu_A_B"]["ket"])
    if not a.giu_tho and not a.tu_tep:
        a.tho.unlink(missing_ok=True)
        print("đã xoá bản thô /tmp")
    return 0 if not (be_a["thieu"] or be_b["thieu"]) and ket_ky else 1


if __name__ == "__main__":
    raise SystemExit(main())
