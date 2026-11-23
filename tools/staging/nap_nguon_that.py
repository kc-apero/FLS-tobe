# -*- coding: utf-8 -*-
"""STAGING bước 05 — nạp DỮ LIỆU NGUỒN THẬT (sổ + PM + 68 dòng chảy + Mapping Master + ảnh chụp 60 sao kê) · `WO-334` AC-2/3/4/7/8.

    FLS_CHO_GHI_THAT=1 PG_DSN=… python tools/staging/nap_nguon_that.py --nap --nguoi-nap <tên.người> [--json tệp]
    PG_DSN=…            python tools/staging/nap_nguon_that.py --kiem          # CHỈ ĐỌC nguồn + đo kho, ⛔ ghi

⭐ **ĐIỀU PHỐI MỎNG** *(Đ1 — đo 23/11: `grep -rn "def main" tools/nap_that.py tools/nap_mapping_master.py tools/nap_nguon_va_khai.py tools/chup_sao_ke.py`)*:
   gọi ĐÚNG các công cụ nạp sẵn có theo ĐÚNG thứ tự phụ thuộc, ⛔ viết lại đường đọc/ghi nào:
     ① `nap_nguon_va_khai` — 68 dòng chảy → `fls_source` + `fls_khai_cot` (⛔ phải có TRƯỚC ④: bản khai là bản đồ cột)
     ② `nap_mapping_master` — tab `Mapping Master` → `fls_mapping_master` (thay trọn, ⛔ nạp rỗng)
     ③ `nap_that.chay_that` — `Transaction Mapping L1` + `[Importrange]PM_Unpivot` → `fls_itl` · `fls_reject` · `fls_pm_line`
     ④ `chup_sao_ke` — vùng CHUẨN 60 sheet `R |` → `fls_chup*` (ảnh chụp F04)
   Token Sheets: `tools/staging/cred_sheets.py` *(tham số/ADC/SA — ⛔ gắn cứng)*. ⛔ CHỈ-ĐỌC Sheets *(`QĐ-ITL-34`)*.

⛔ LUẬT: ghi đòi `FLS_CHO_GHI_THAT=1` · ⛔ kho `fls-pg-1` *(cổng 5433)* · `fls_itl` chỉ-THÊM *(`INV-I08`)* ⇒ chạy lại ⛔ nhân đôi ·
   `PM_COT_RIENG_TU = {"Email Address"}` ⛔ vào kho · BÁO CÁO ⛔ in tên người / số TK / tiền dòng — CHỈ số đếm.
   Một nguồn ⛔ đọc được ⇒ ĐỎ CÓ TÊN, các nguồn khác vẫn đo *(⛔ bỏ qua im lặng, ⛔ nổ cả lượt)*.
   Cổng đọc-đủ của `nap_that` ĐỎ ⇒ sổ ⛔ ghi, NHƯNG vẫn đo chỉ-đọc *(số đếm nguồn mới vẫn vào BÁO CÁO)*.

BÁO CÁO có hai tầng, mỗi hàng `mong` + nhãn nó ĐẾM GÌ *(Đ4)*, mẫu số ≠ 0 *(Đ3)*, phép ⛔ đo được ⇒ ĐỎ *(Đ5)*:
   ⓐ **Σ nguồn = Σ kho** — `mong` = số vừa đọc từ nguồn ở chính lượt này (động);
   ⓑ **CŨ ↔ HIỆN TẠI** — ảnh đóng băng `tests/fixture/pm_join.json` *(9.992 dòng bank-canon · 3.703 dòng PM, khoá = SỐ DÒNG SHEET)*:
      dòng ĐÃ có trong ảnh phải y hệt ở nguồn sống *(`mong` lệch = 0 — lệch ⇒ ĐỎ: nguồn bị sửa sau chốt)*; dòng ⛔ có trong ảnh
      ⇒ đếm RIÊNG, nhãn `MỚI`; số đã đo `docs/ITL/_tools/voi_so_luong.json` in cạnh để đọc.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import traceback
from collections import Counter
from datetime import date, timedelta
from decimal import Decimal
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC))

ANH_PM_JOIN = GOC / "tests" / "fixture" / "pm_join.json"
VOI_SO_LUONG = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
BIEN_CHO_GHI = "FLS_CHO_GHI_THAT"
CONG_KHO_THAT_FLS_PG_1 = "5433"          # `fls-pg-1` (Docker của chủ) — ⛔ ghi
PM_COT_RIENG_TU = {"Email Address"}      # chép tên; bài `test_anh_rieng_tu` đối chiếu với `pm_join.PM_COT_RIENG_TU`


# ──────────────────────────────── BÁO CÁO ────────────────────────────────
class Bao:
    """Hàng `(nhóm, nhãn, đo, mong)`. `mong=None` ⇒ chỉ ĐO (in, ⛔ chấm). `đo=None` ⇒ ⛔ đo được ⇒ ĐỎ."""

    def __init__(self) -> None:
        self.hang: list[tuple[str, str, object, object]] = []
        self.so: dict[str, object] = {}

    def do(self, nhom: str, nhan: str, gt, mong=None, *, khoa: str | None = None) -> None:
        self.hang.append((nhom, nhan, gt, mong))
        if khoa:
            self.so[khoa] = gt

    def do_ro(self, nhom: str, nhan: str, ly_do: str) -> None:
        """Phép ⛔ đo được ⇒ ĐỎ (Đ5). `ly_do` chỉ chứa TÊN lỗi / mã HTTP — ⛔ nội dung ô."""
        self.hang.append((nhom, nhan, None, "đo được"))
        self.so["do_ro:" + nhan] = ly_do

    @staticmethod
    def dat(gt, mong) -> bool:
        return mong is None or (gt is not None and gt == mong)

    def so_do(self) -> int:
        return sum(1 for _, _, g, m in self.hang if not self.dat(g, m))

    def in_ra(self) -> str:
        out, nhom = [], None
        for n, nhan, gt, mong in self.hang:
            if n != nhom:
                out.append(f"\n── {n}")
                nhom = n
            if mong is None:
                out.append(f"   {nhan:78}  {gt}")
            else:
                ok = self.dat(gt, mong)
                out.append(f"   [{'ĐẠT' if ok else 'ĐỎ'}] {nhan:74}  {gt!r}  (mong {mong!r})")
        do = self.so_do()
        out.append(f"\n══ KẾT: {'ĐẠT' if do == 0 else f'ĐỎ — {do} mục khác mong'}")
        return "\n".join(out)


def _loi_ten(e: BaseException) -> str:
    """Tên lỗi + mã HTTP, ⛔ thân phản hồi (có thể kèm tên tệp/người)."""
    ma = getattr(e, "code", None)
    return type(e).__name__ + (f" HTTP {ma}" if ma else "")


# ──────────────────────────────── ẢNH CŨ ────────────────────────────────
def doc_anh_cu(duong: Path = ANH_PM_JOIN) -> dict:
    return json.loads(duong.read_text(encoding="utf-8"))


def _d(x) -> Decimal | None:
    try:
        return None if x in (None, "") else Decimal(str(x))
    except Exception:
        return None


def so_voi_anh(bank, pm, anh: dict) -> dict:
    """⭐ Pure. So nguồn hiện tại với ảnh đóng băng, khoá = SỐ DÒNG SHEET. Chỉ trả SỐ ĐẾM.

    `lech_*` đếm dòng ĐÃ CÓ trong ảnh mà nguồn hiện tại khác *(⇒ bị sửa/dời sau ảnh)*; `mat` = dòng ảnh mà nguồn hiện tại ⛔ có
    dòng canon/PM nào ở đúng số dòng ấy; `moi` = dòng nguồn hiện tại ⛔ có trong ảnh. ⛔ so GIÁ TRỊ nào ngoài chính 3 trường
    của ảnh *(`ref_tho` · `cur` · `tien`)*.
    """
    from fls.adapters.pm_join import canon_ref
    b_anh = {r["dong"]: r for r in anh["bank"]}
    b_nay = {b.dong_sheet: b for b in bank}
    lech = Counter()
    mat = 0
    for dong, r in b_anh.items():
        b = b_nay.get(dong)
        if b is None:
            mat += 1
            continue
        if b.ref != canon_ref(r["ref_tho"]):
            lech["ref"] += 1
        if b.cur != str(r["cur"]).strip():
            lech["cur"] += 1
        if _d(r["tien"]) != b.tien:
            lech["tien"] += 1
    # ⭐ so THEO NỘI DUNG (bỏ vị trí): bộ ba (ref, cur, tien) của ảnh phải còn đủ ở nguồn sống — phân biệt "sheet bị SẮP LẠI/CHÈN
    #   dòng" *(vị trí lệch, nội dung còn)* với "dòng bị SỬA/MẤT" *(nội dung mất)*.
    ba_anh = Counter((canon_ref(r["ref_tho"]), str(r["cur"]).strip(), _d(r["tien"])) for r in anh["bank"])
    ba_nay = Counter((b.ref, b.cur, b.tien) for b in bank)
    mat_nd = sum((ba_anh - ba_nay).values())
    p_anh = {r["dong"]: r for r in anh["pm"]}
    p_nay = {p.dong_sheet: p for p in pm}
    lech_pm = Counter()
    mat_pm = 0
    for dong, r in p_anh.items():
        p = p_nay.get(dong)
        if p is None:
            mat_pm += 1
            continue
        for k, a, b in (("ref", r["ref_tho"], p.ref_tho), ("slip", r["slip"], p.slip), ("line", r["line"], p.line),
                        ("cur", r["cur"], p.cur), ("status", r["status"], p.status),
                        ("hd", r.get("hd"), p.hd), ("cdt1", r.get("cdt1"), p.cdt1)):
            if (a or None) != (b or None):
                lech_pm[k] += 1
        if _d(r["tien"]) != p.tien:
            lech_pm["tien"] += 1
    return {"bank_anh": len(b_anh), "bank_nay": len(b_nay), "bank_mat": mat, "bank_moi": len(set(b_nay) - set(b_anh)),
            "bank_lech": dict(lech), "bank_mat_noi_dung": mat_nd, "bank_khop": len(b_anh) - mat,
            "pm_anh": len(p_anh), "pm_nay": len(p_nay), "pm_mat": mat_pm, "pm_moi": len(set(p_nay) - set(p_anh)),
            "pm_lech": dict(lech_pm)}


def bac_thang_tu_anh(anh: dict) -> dict:
    """Phát lại ảnh qua ĐÚNG `xep_ca_lat` ⇒ `bank_tong` của `voi_so_luong.json` — bằng chứng ảnh còn dùng được."""
    from fls.adapters.pm_join import DongBank, DongPM, canon_ref, xep_ca_lat
    bank = [DongBank(r["dong"], canon_ref(r["ref_tho"]), Decimal(str(r["tien"])), r["cur"]) for r in anh["bank"]]
    pm = [DongPM(dong_sheet=r["dong"], slip=r["slip"], line=r["line"], tien=_d(r["tien"]), cur=r["cur"],
                 status=r["status"], ref=canon_ref(r["ref_tho"]), hd=r.get("hd"), cdt1=r.get("cdt1"),
                 ref_tho=r["ref_tho"]) for r in anh["pm"]]
    _, tkg = xep_ca_lat(bank, pm)
    return {"dong_bank": tkg.dong_bank, "khong_co_ma": tkg.khong_co_ma, "khong_thay_ma_PM": tkg.khong_thay_ma_PM,
            "dong_theo_hinh": dict(tkg.dong_theo_hinh), "can": tkg.can(), "so_dong_pm": len(pm),
            "pm_co_ref": sum(1 for p in pm if p.ref)}


def ky_cua(serial) -> str | None:
    """Số sê-ri ngày Sheets → `YYYY-MM`. ⛔ đoán: ô không phải số ⇒ `None` (đếm riêng, ⛔ dồn vào một kỳ)."""
    if isinstance(serial, bool) or not isinstance(serial, (int, float)):
        return None
    d = date(1899, 12, 30) + timedelta(days=int(serial))
    return f"{d.year:04d}-{d.month:02d}"


# ──────────────────────────────── ĐẾM KHO ────────────────────────────────
def dem(conn, sql: str, args=()) -> int | None:
    try:
        with conn.cursor() as c:
            c.execute(sql, args or None)   # ⛔ `()` làm psycopg đọc `%e` trong ILIKE '%email%' là tham số
            return int(c.fetchone()[0])
    except Exception:
        try:
            conn.rollback()
        except Exception:
            pass
        return None


def dem_kho(conn) -> dict:
    return {
        "itl": dem(conn, "SELECT count(*) FROM fls_itl"),
        "reject": dem(conn, "SELECT count(*) FROM fls_reject"),
        "pm_line": dem(conn, "SELECT count(*) FROM fls_pm_line"),
        "source": dem(conn, "SELECT count(*) FROM fls_source WHERE src_type IN ('Bank','Cash')"),
        "khai": dem(conn, "SELECT count(*) FROM fls_khai_cot"),
        "mapping": dem(conn, "SELECT count(*) FROM fls_mapping_master"),
        "chup": dem(conn, "SELECT count(*) FROM fls_chup"),
        "chup_dong": dem(conn, "SELECT count(*) FROM fls_chup_dong"),
        "chup_nguon": dem(conn, "SELECT count(*) FROM fls_chup_nguon"),
        "cot_email": dem(conn, "SELECT count(*) FROM information_schema.columns WHERE table_schema='public'"
                               " AND column_name ILIKE '%email%'"),
    }


def do_quyen(bao: Bao, tok: str) -> dict[str, bool]:
    """Quyền ĐỌC từng workbook nguồn: HTTP 200 mới đi tiếp. ⛔ 403/404 ⇒ ĐỎ CÓ TÊN + các bước dùng workbook ấy DỪNG (⛔ im lặng)."""
    import urllib.request

    from tools.do_bat_bien_ngam import BANK, QUY
    from tools.staging import cred_sheets
    from fls.oracle.nguon import BAN_SAO_RAW
    N = "0b · QUYỀN ĐỌC từng workbook nguồn (HTTP; ⛔ nội dung)"
    ok: dict[str, bool] = {}
    for ten, sid in (("RAW (sổ ITL · PM · Mapping Master)", BAN_SAO_RAW.spreadsheet_id),
                     ("BANK (60 sheet `R |` ngân hàng)", BANK), ("QUỸ (8 sheet `R |` quỹ)", QUY)):
        q = urllib.request.Request(cred_sheets.api_goc() + sid + "?fields=spreadsheetId",
                                   headers={"Authorization": "Bearer " + tok})
        try:
            with urllib.request.urlopen(q, timeout=60) as f:
                ma = f.status
        except Exception as e:                       # noqa: BLE001
            ma = getattr(e, "code", None) or type(e).__name__
        ok[ten.split()[0]] = ma == 200
        bao.do(N, f"HTTP đọc workbook {ten}", ma, 200)
    return ok


# ──────────────────────────────── CÁC BƯỚC ────────────────────────────────
def buoc_khai(bao: Bao, tok: str, dsn: str, ghi: bool) -> dict:
    import psycopg
    from tools import nap_nguon_va_khai as nk
    N = "① 68 dòng chảy + bản khai (nap_nguon_va_khai)"
    thu = nk.thu_thap(tok)
    n_ban = sum(1 for v in thu.values() if v[0] == "Bank")
    n_quy = sum(1 for v in thu.values() if v[0] == "Cash")
    so_khai = sum(len(v[1]) for v in thu.values())
    bao.do(N, "NGUỒN: sheet `R |` sổ Bank (đếm sheet)", n_ban, khoa="khai_bank")
    bao.do(N, "NGUỒN: sheet `R |` sổ Quỹ (đếm sheet)", n_quy, khoa="khai_quy")
    bao.do(N, "mẫu số: dòng chảy đọc được ≠ 0", len(thu) > 0, True)
    if ghi:
        with psycopg.connect(dsn, autocommit=True) as conn:
            d = nk.nap(conn, thu)
            k = dem_kho(conn)
        bao.do(N, "sheet THIẾU trường — ⛔ nạp (đếm)", d["thieu_truong"], 0)
        bao.do(N, "KHO: `fls_source` Bank+Cash (đếm) = Σ nguồn", k["source"], len(thu))
        bao.do(N, "KHO: `fls_khai_cot` (đếm) = Σ trường khai ở nguồn", k["khai"], so_khai)
    return thu


def buoc_mapping(bao: Bao, tok: str, dsn: str, ghi: bool) -> None:
    import psycopg

    from fls.adapters.mapping_master import COT, doc_cot, tom_tat
    from fls.repo.nap_mapping import nap_mapping_master
    from tools import nap_mapping_master as nm
    N = "② Mapping Master (nap_mapping_master)"
    tho = {ch: nm._cot(tok, ch) for ch in COT}
    dong, loai = doc_cot(tho)
    t = tom_tat(dong)
    bao.do(N, "NGUỒN: mã `hd` đọc được (đếm)", t["ma"], khoa="mm_ma")
    bao.do(N, "NGUỒN: dòng bị loại (đếm, mỗi cái có lý do)", len(loai), khoa="mm_loai")
    bao.do(N, "NGUỒN: cần phân bổ / có phương pháp (đếm)", f"{t['can_phan_bo']} / {t['co_phuong_phap']}")
    bao.do(N, "mẫu số: mã đọc được ≠ 0", t["ma"] > 0, True)
    if ghi:
        with psycopg.connect(dsn, autocommit=True) as conn:
            nap_mapping_master(conn, dong, bi_loai=len(loai))
            k = dem_kho(conn)
        bao.do(N, "KHO: `fls_mapping_master` (đếm) = Σ nguồn đọc được", k["mapping"], t["ma"])


def buoc_so_pm(bao: Bao, tok: str, dsn: str, ghi: bool, anh: dict) -> dict:
    import psycopg

    from tools import nap_that as nt
    N = "③ sổ ITL + PM (nap_that.chay_that)"
    truoc = None
    if ghi:
        with psycopg.connect(dsn, autocommit=True) as conn:
            truoc = dem_kho(conn)
    r = nt.chay_that(tok, ghi=ghi, dsn=dsn)
    tk, tkg = r["tk"], r["tkg"]
    bao.do(N, "NGUỒN `Transaction Mapping L1`: dòng đọc (đếm)", tk.vao, khoa="so_vao")
    bao.do(N, "   = canon (đếm)", tk.ra, khoa="so_ra")
    bao.do(N, "   + loại có lý do (đếm)", tk.loai, khoa="so_loai")
    bao.do(N, "   + rỗng (đếm)", tk.rong, khoa="so_rong")
    bao.do(N, "mẫu số: dòng đọc ≠ 0", tk.vao > 0, True)
    bao.do(N, "ba đường adapter cân (vào = canon + loại + rỗng)", tk.can(), True)
    bao.do(N, "NGUỒN `[Importrange]PM_Unpivot`: dòng đọc (đếm)", len(r["pm"]), khoa="pm_dong")
    bao.do(N, "   trong đó có mã tham chiếu (đếm)", sum(1 for p in r["pm"] if p.ref), khoa="pm_co_ref")
    bao.do(N, "mẫu số PM ≠ 0", len(r["pm"]) > 0, True)
    bao.do(N, "bốn đường ghép PM cân", tkg.can(), True)
    for n in r["doc_du"]["dem"]:
        bao.do(N, f"cổng đọc-đủ · {n.ten}: theo HÀNG / theo CỘT / sàn", f"{n.lan_lat} / {n.lan_cot} / {n.toi_thieu}")
    # Đ5: phép chặn ghi ĐỎ có tên — mong = đạt
    bao.do(N, "cổng đọc-đủ (nguồn có đủ ô so với sàn đã đo 27/08)", r["doc_du"]["dat"], True)
    for ly in r["doc_du"]["ly_do"]:
        bao.do(N, "   ⛔ lý do cổng: " + re.sub(r"\s+", " ", ly)[:150], "ĐỎ")
    if ghi and r["da_ghi"]:
        kq = r["kq"]
        with psycopg.connect(dsn, autocommit=True) as conn:
            sau = dem_kho(conn)
        bao.do(N, "KẾT QUẢ nạp: bốn đường cân (kq.can())", kq.can(), True)
        d_itl, d_rej = sau["itl"] - truoc["itl"], sau["reject"] - truoc["reject"]
        # ⭐ Σ SAU (⛔ Δ): `fls_itl` chỉ-THÊM và `fls_reject` chống trùng ⇒ chạy lại Δ = 0 mà Σ vẫn phải khớp. Đúng khi kho chỉ chứa
        #   nguồn này (staging: kho trắng + 04 ⛔ ghi sổ). Nguồn bị SỬA/MẤT dòng sau lần nạp trước ⇒ Σ lệch ⇒ ĐỎ (tín hiệu thật).
        bao.do(N, "KHO: `fls_itl` + `fls_reject` (đếm, SAU nạp) = dòng KHÔNG rỗng của nguồn (canon + loại)",
               sau["itl"] + sau["reject"], tk.ra + tk.loai)
        bao.do(N, "   trong đó `fls_itl` (đếm, sau)", sau["itl"])
        bao.do(N, "   trong đó `fls_reject` (đếm, sau; = loại ở adapter + loại ở tầng sổ)", sau["reject"])
        bao.do(N, "   lần này: `fls_itl` tăng · `fls_reject` tăng · bỏ-qua-trùng (đếm)", f"{d_itl} · {d_rej} · {kq.bo_qua_trung}")
        bao.do(N, "KHO: `fls_pm_line` (đếm) = dòng PM đọc", sau["pm_line"], len(r["pm"]))
        bao.do(N, "chạy-lại: bỏ-qua-trùng (đếm; lần đầu = 0, lần sau = canon)", kq.bo_qua_trung)
    elif ghi:
        bao.do(N, "KHO: sổ ĐÃ ghi (cổng đọc-đủ/ba đường chặn ⇒ ⛔)", False, True)

    # ⓑ CŨ ↔ HIỆN TẠI
    N2 = "ⓑ CŨ (ảnh đóng băng) ↔ HIỆN TẠI (nguồn sống)"
    s = so_voi_anh(r["bank"], r["pm"], anh)
    bao.do(N2, "mẫu số: dòng bank trong ảnh (đếm)", s["bank_anh"], anh["so_dong_bank"])
    bao.do(N2, "dòng bank ảnh ⛔ còn ở đúng số dòng nguồn (MẤT, đếm)", s["bank_mat"], 0, khoa="bank_mat")
    for k in ("ref", "cur", "tien"):
        bao.do(N2, f"dòng bank ảnh LỆCH `{k}` ở nguồn sống (đếm)", s["bank_lech"].get(k, 0), 0, khoa=f"bank_lech_{k}")
    bao.do(N2, "bộ ba (ref,cur,tien) của ảnh ⛔ còn ở nguồn sống — SO THEO NỘI DUNG, bỏ vị trí (đếm)", s["bank_mat_noi_dung"], 0,
           khoa="bank_mat_noi_dung")
    bao.do(N2, "MỚI — dòng canon nguồn sống ⛔ có trong ảnh (đếm, nhãn riêng)", s["bank_moi"], khoa="bank_moi")
    bao.do(N2, "mẫu số: dòng PM trong ảnh (đếm)", s["pm_anh"], anh["so_dong_pm"])
    bao.do(N2, "dòng PM ảnh ⛔ còn ở đúng số dòng nguồn (MẤT, đếm)", s["pm_mat"], 0, khoa="pm_mat")
    for k in ("ref", "slip", "line", "cur", "status", "hd", "cdt1", "tien"):
        bao.do(N2, f"dòng PM ảnh LỆCH `{k}` ở nguồn sống (đếm)", s["pm_lech"].get(k, 0), 0, khoa=f"pm_lech_{k}")
    bao.do(N2, "MỚI — dòng PM nguồn sống ⛔ có trong ảnh (đếm, nhãn riêng)", s["pm_moi"], khoa="pm_moi")
    # số cũ in cạnh (ảnh `voi_so_luong.json`)
    vsl = json.loads(VOI_SO_LUONG.read_text(encoding="utf-8"))
    bao.do(N2, "CŨ `voi_so_luong.pm_tong.so_dong_pm` ↔ HIỆN TẠI PM đọc", f"{vsl['pm_tong']['so_dong_pm']} ↔ {len(r['pm'])}")
    bao.do(N2, "CŨ `bank_tong.dong_bank` ↔ HIỆN TẠI canon", f"{vsl['bank_tong']['dong_bank']} ↔ {tk.ra}")
    theo_ky = Counter()
    for _d_, row in r["ra"]:
        theo_ky[ky_cua(row.at(0)) or "(ngày không đọc được)"] += 1
    bao.so["theo_ky_canon"] = dict(sorted(theo_ky.items()))
    ky_cu = set(vsl["ky"])
    bao.do(N2, "HIỆN TẠI canon thuộc kỳ ĐÃ CHỐT trong ảnh (23 kỳ; đếm)", sum(v for k, v in theo_ky.items() if k in ky_cu))
    bao.do(N2, "HIỆN TẠI canon thuộc kỳ MỚI sau ảnh (đếm, nhãn riêng)", sum(v for k, v in theo_ky.items()
                                                                           if k not in ky_cu and not k.startswith("(")))
    bao.do(N2, "HIỆN TẠI canon ⛔ đọc được ngày (đếm)", sum(v for k, v in theo_ky.items() if k.startswith("(")))
    bao.so["bac_thang_nay"] = {"dong_theo_hinh": dict(tkg.dong_theo_hinh), "khong_co_ma": tkg.khong_co_ma,
                               "khong_thay_ma_PM": tkg.khong_thay_ma_PM, "dong_bank": tkg.dong_bank}
    return r


def buoc_chup(bao: Bao, tok: str, dsn: str, ghi: bool, thu: dict | None) -> None:
    import psycopg

    from fls.repo import chup as ch
    from tools.do_bat_bien_ngam import BANK
    from tools.nap_sao_ke import TRUONG_MAC_DINH, doc_vung_chuan, khai_day_du, ten_sheet_r
    N = "④ ảnh chụp 60 sheet `R |` (chup_sao_ke)"
    ten_r = ten_sheet_r(BANK, tok)
    bao.do(N, "NGUỒN: sheet `R |` của sổ Bank (đếm)", len(ten_r), khoa="chup_sheet")
    bao.do(N, "mẫu số: sheet ≠ 0", len(ten_r) > 0, True)
    if ghi:
        khai = khai_day_du(ten_r, dsn)
        khai_cot = {t: b.cot for t, b in khai.items()}
    else:
        if not thu:
            raise RuntimeError("⛔ --kiem ④ cần bản khai ở ① (đọc dòng 1)")
        khai = None
        khai_cot = {t: thu[t][1] for t in ten_r if t in thu}
        thieu = [t for t in ten_r if t not in khai_cot]
        bao.do(N, "sheet `R |` ⛔ có bản khai ở ① (đếm)", len(thieu), 0)
        if thieu:
            return
    o_theo, _ = doc_vung_chuan(BANK, tok, ten_r, TRUONG_MAC_DINH, khai_cot)
    so_dong = sum(len(v) for v in o_theo.values())
    n0 = sum(1 for t in ten_r if not o_theo[t])
    bao.do(N, "NGUỒN: Σ dòng vùng CHUẨN (đếm)", so_dong, khoa="chup_dong")
    bao.do(N, "NGUỒN: sheet ra 0 dòng (đếm — VẪN phải có mặt ở kho)", n0, khoa="chup_rong")
    if ghi:
        dong = [(khai[t].source_id, j, o) for t in ten_r for j, o in enumerate(o_theo[t])]
        nguon = {khai[t].source_id: khai[t].version for t in ten_r}
        with psycopg.connect(dsn, autocommit=True) as conn:
            kq = ch.ghi_chup(conn, spreadsheet_id=BANK, lan="Bank", actor="tools/staging/nap_nguon_that.py",
                             giay=0.0, nguon=nguon, dong=dong)
        bao.do(N, "KHO: ảnh chụp — nguồn (đếm) = sheet đọc", kq.so_nguon, len(ten_r))
        bao.do(N, "KHO: ảnh chụp — dòng (đếm) = Σ nguồn", kq.so_dong, so_dong)
        bao.do(N, "KHO: nguồn ra 0 dòng VẪN có mặt (đếm)", sum(1 for n in kq.nguon if n.so_dong == 0), n0)


def do_rieng_tu(bao: Bao, dsn: str) -> None:
    import psycopg
    N = "⑤ RIÊNG TƯ (đếm; ⛔ in nội dung)"
    with psycopg.connect(dsn, autocommit=True) as conn:
        k = dem_kho(conn)
        bao.do(N, "MẪU SỐ — cột của kho (đếm)", dem(conn, "SELECT count(*) FROM information_schema.columns"
                                                          " WHERE table_schema='public'") or 0)
        bao.do(N, "cột tên có 'email' (đếm, ⛔ vào kho)", k["cot_email"], 0)
        # `fls_pm_line.tho` là `json` (0022, giữ thứ tự cột) khoá theo TÊN cột ⇒ ép `::jsonb` để dùng toán tử `?`: ⛔ có khoá `Email Address`
        for c in sorted(PM_COT_RIENG_TU):
            n = dem(conn, "SELECT count(*) FROM fls_pm_line WHERE tho::jsonb ? %s", (c,))
            bao.do(N, f"dòng PM mang khoá `{c}` (đếm)", n, 0)
        mau = dem(conn, "SELECT count(*) FROM fls_pm_line")
        bao.do(N, "mẫu số PM trong kho (đếm; 0 ⇒ phép trên ⛔ chứng minh gì — Đ3)", mau)


# ──────────────────────────────── MAIN ────────────────────────────────
def kiem_dsn(dsn: str) -> None:
    m = re.search(r"@[^:/]+:(\d+)/", dsn)
    if m and m.group(1) == CONG_KHO_THAT_FLS_PG_1:
        raise SystemExit("⛔ PG_DSN trỏ cổng 5433 = kho THẬT `fls-pg-1` — ⛔ ghi. Dùng cụm của phiên (5434–5437…) hoặc proxy staging.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1], add_help=True)
    ap.add_argument("--kiem", action="store_true", help="CHỈ ĐỌC (mặc định)")
    ap.add_argument("--nap", action="store_true", help="GHI vào kho PG_DSN (đòi FLS_CHO_GHI_THAT=1)")
    ap.add_argument("--nguoi-nap", default="")
    ap.add_argument("--json", default="", help="ghi SỐ ĐẾM (⛔ dữ liệu) ra tệp")
    ap.add_argument("--bo-buoc", default="", help="vd `chup` — bỏ bước (chỉ để thử; BÁO CÁO nói rõ)")
    ap.add_argument("--anh-cu", default=str(ANH_PM_JOIN))
    a = ap.parse_args(argv)
    ghi = a.nap and not a.kiem
    if a.nap and a.kiem:
        raise SystemExit("⛔ --nap và --kiem loại trừ nhau")
    dsn = os.environ.get("PG_DSN", "")
    if ghi:
        if os.environ.get(BIEN_CHO_GHI) != "1":
            raise SystemExit(f"⛔ nạp là GHI — đòi {BIEN_CHO_GHI}=1")
        if not re.fullmatch(r"[A-Za-z0-9._-]+", a.nguoi_nap or ""):
            raise SystemExit("⛔ cần --nguoi-nap <tên.người> ([A-Za-z0-9._-], ⛔ email/rỗng)")
        if not dsn:
            raise SystemExit("⛔ thiếu PG_DSN")
        kiem_dsn(dsn)
    from tools.staging import cred_sheets
    anh = doc_anh_cu(Path(a.anh_cu))
    bao = Bao()
    bao.do("0 · THÔNG TIN", "đường thông tin xác thực Sheets (⛔ giá trị)", cred_sheets.kieu())
    bao.do("0 · THÔNG TIN", "chế độ", "NẠP" if ghi else "CHỈ ĐỌC (--kiem)")
    skip = {x for x in a.bo_buoc.split(",") if x}
    if skip:
        bao.do("0 · THÔNG TIN", "bước BỊ BỎ (chỉ để thử)", ",".join(sorted(skip)))
    t0 = time.time()
    tok = cred_sheets.lay_token()
    thu = None
    quyen = do_quyen(bao, tok)
    can = {"khai": ("BANK", "QUỸ"), "mapping": ("RAW",), "so_pm": ("RAW",), "chup": ("BANK", "QUỸ")}
    for ten, f in (("khai", lambda: buoc_khai(bao, tok, dsn, ghi)),
                   ("mapping", lambda: buoc_mapping(bao, tok, dsn, ghi)),
                   ("so_pm", lambda: buoc_so_pm(bao, tok, dsn, ghi, anh)),
                   ("chup", lambda: buoc_chup(bao, tok, dsn, ghi, thu))):
        if ten in skip:
            continue
        thieu_q = [w for w in can[ten] if not quyen.get(w, False)]
        if thieu_q:                                  # DỪNG phần ấy, ĐỎ có tên (WO-334 §Ràng buộc)
            bao.do_ro(f"bước {ten}", f"bước {ten} chạy được — DỪNG vì ⛔ quyền đọc workbook {'+'.join(thieu_q)}",
                      "thiếu quyền đọc " + "+".join(thieu_q))
            continue
        try:
            tok = cred_sheets.lay_token()          # làm mới (token ~60 phút)
            r = f()
            if ten == "khai":
                thu = r
        except SystemExit as e:                    # nguồn thiếu quyền / hình dạng đổi — ĐỎ có tên, các bước khác vẫn chạy
            bao.do_ro(f"bước {ten}", f"bước {ten} chạy được", "SystemExit: " + re.sub(r"\s+", " ", str(e))[:160])
        except Exception as e:                     # noqa: BLE001
            bao.do_ro(f"bước {ten}", f"bước {ten} chạy được", _loi_ten(e))
            traceback.print_exc(file=sys.stderr)
    if ghi:
        try:
            do_rieng_tu(bao, dsn)
        except Exception as e:                     # noqa: BLE001
            bao.do_ro("⑤ RIÊNG TƯ", "đo riêng tư", _loi_ten(e))
    bao.do("Z · THỜI GIAN", "giây (đo)", round(time.time() - t0, 1))
    print(bao.in_ra())
    if a.json:
        Path(a.json).write_text(json.dumps({"so": bao.so, "do": bao.so_do()}, ensure_ascii=False, indent=1, default=str),
                                encoding="utf-8")
    return 1 if bao.so_do() else 0


if __name__ == "__main__":
    raise SystemExit(main())
