"""Bài thử bước 05 — `WO-334` AC-2/3/4/7: `nap_nguon_that.py` · `05_nap_nguon_that.sh` · `cred_sheets.py`.

Sheets = máy chủ GIẢ HTTP thật (`sheets_gia.py`); PG = cụm THẬT của phiên (kho scratch). Nguồn "CŨ" = PHÁT LẠI ảnh đóng băng
`tests/fixture/pm_join.json` *(9.992 dòng bank-canon · 3.703 dòng PM, khoá = số dòng sheet)*.

⛔ Giới hạn đã đo (Đ1): ảnh commit KHÔNG có lưới thô 38 cột của `Transaction Mapping L1` — chỉ 4 trường/dòng bank
`(dong, ref_tho, cur, tien)` + 8 trường/dòng PM. ⇒ phát lại dựng lại lưới với ngày/tài khoản TỔNG HỢP *(chỉ ghép/đếm/Σ tiền là
số thật của ảnh)*; ⛔ số theo kỳ không khẳng định ở đây.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import psycopg
import pytest

from fls.canon.spec import CANON_COLS
from fls.adapters.pm_join import PM_COT, PM_DONG_DAU, PM_DONG_TIEU_DE, PM_TIEU_DE_MONG_DOI
from fls.adapters.mapping_master import COT as MM_COT, DONG_DAU as MM_DONG_DAU, TAB as MM_TAB
from fls.oracle.nguon import BAN_SAO_RAW
from tests.staging import ho_tro as H
from tests.staging.sheets_gia import SheetsGia

GOC = H.GOC
ANH = json.loads((GOC / "tests" / "fixture" / "pm_join.json").read_text(encoding="utf-8"))
VSL = json.loads((GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json").read_text(encoding="utf-8"))
from tools.do_bat_bien_ngam import BANK as BANK_ID, QUY as QUY_ID   # ID THẬT làm khoá của máy chủ giả ⇒ tiến trình con (05.sh) cũng đi đúng đường
CT = "tools/staging/nap_nguon_that.py"
EMAIL_GIA = "nguoi.gia.thu@example.invalid"
TEN_TK_GIA = "TEN-TK-GIA-GIU"


# ───────────────────────── dựng nguồn GIẢ từ ảnh ─────────────────────────
def _luoi_tml() -> list[list]:
    luoi: list[list] = [[""] * 38 for _ in range(2)]
    luoi.append([c.name for c in CANON_COLS])                       # dòng 3 = tiêu đề canon
    luoi.append([""] * 38)                                          # dòng 4 TRỐNG (BAN_SAO_RAW.dong_dau = 5)
    for r in sorted(ANH["bank"], key=lambda x: x["dong"]):
        assert len(luoi) + 1 == r["dong"], "ảnh bank phải liền mạch từ dòng 5"
        o = [""] * 38
        o[0], o[1], o[3] = 45000 + (r["dong"] % 700), r["ref_tho"], r["cur"]
        o[4], o[5], o[6] = float(r["tien"]), 0, f"R | IMG{r['dong']}"    # tài khoản TỔNG HỢP duy nhất mỗi dòng
        luoi.append(o)
    return luoi


def _luoi_pm() -> list[list]:
    n = 29
    tde = [""] * n
    for i, t in PM_TIEU_DE_MONG_DOI.items():
        tde[i] = t
    tde[26], tde[27] = "Email Address", "Tên tài khoản"            # cột riêng tư (CẤM) + cột GIỮ
    luoi = [[""] * n, tde]
    for r in sorted(ANH["pm"], key=lambda x: x["dong"]):
        assert len(luoi) + 1 == r["dong"], "ảnh PM phải liền mạch từ dòng 3"
        o = [""] * n
        o[PM_COT["slip"]], o[PM_COT["line"]], o[PM_COT["cur"]] = r["slip"], r["line"], r["cur"]
        o[PM_COT["tien"]], o[PM_COT["status"]], o[PM_COT["ref"]] = float(r["tien"]), r["status"], r["ref_tho"]
        o[PM_COT["hd"]], o[PM_COT["cdt1"]] = r.get("hd") or "", r.get("cdt1") or ""
        o[26], o[27] = EMAIL_GIA, TEN_TK_GIA
        luoi.append(o)
    return luoi


def _luoi_mm() -> list[list]:
    """Mapping Master tổng hợp 6 mã (dòng 7+): cột H = hd_code duy nhất."""
    luoi = [[""] * 20 for _ in range(MM_DONG_DAU - 1)]
    for k in range(6):
        o = [""] * 20
        o[7] = f"HD{k:02d} | Mã giả {k}"
        o[10], o[11] = ("Yes", "Equal") if k % 2 == 0 else ("No need", "")
        luoi.append(o)
    return luoi


def _luoi_r(so_dong: int, quy: bool = False) -> list[list]:
    """Sheet `R |` tổng hợp: dòng 1 = bản khai số 1..6, dòng 2 = tiêu đề, dòng 3+ = dữ liệu."""
    khai = ["1", "2", "3", "4", "5", "6"]
    luoi = [khai, ["Date", "Description", "Currency", "Debit", "Credit", "Reference number"]]
    for i in range(so_dong):
        luoi.append([45000 + i, f"dien giai gia {i}", "VND", float(100 + i), "", f"REF{i:04d}"])
    return luoi


def dung_nguon(rong_anh: bool = False) -> SheetsGia:
    g = SheetsGia()
    g.kho[BAN_SAO_RAW.spreadsheet_id] = {BAN_SAO_RAW.sheet: _luoi_tml(), "[Importrange]PM_Unpivot": _luoi_pm(),
                                         MM_TAB: _luoi_mm()}
    g.kho[BANK_ID] = {"R | AAA": _luoi_r(5), "R | BBB": _luoi_r(3), "R | CCC": _luoi_r(0), "Index": [["x"]]}
    g.kho[QUY_ID] = {"R | Q1": _luoi_r(4), "Index": [["x"]]}
    return g


@pytest.fixture(scope="module")
def nguon():
    g = dung_nguon()
    goc = g.bat()
    yield g, goc
    g.tat()


@pytest.fixture()
def moi_truong(monkeypatch, nguon):
    g, goc = nguon
    monkeypatch.setenv("FLS_SHEETS_API_GOC", goc)
    monkeypatch.setenv("FLS_SHEETS_TOKEN", "token-gia")
    for k in ("FLS_GSHEETS_SA_JSON", "FLS_GSHEETS_SA_JSON_B64", "FLS_SHEETS_SA_JSON_TEP", "FLS_SHEETS_ADC"):
        monkeypatch.delenv(k, raising=False)
    # `tools.do_hinh_dang.API` được chốt lúc nhập — trỏ lại về máy chủ giả
    import tools.do_hinh_dang as dh
    monkeypatch.setattr(dh, "API", goc)
    # sàn của cổng đọc-đủ đo trên NGUỒN THẬT — nguồn tổng hợp không có Budget Code…: hạ sàn CHỈ ở bài nào nói rõ (`san_0`)
    return g


@pytest.fixture()
def san_0(monkeypatch):
    from fls.oracle import doc_du
    for k in list(doc_du.NGUONG_SAN):
        monkeypatch.setitem(doc_du.NGUONG_SAN, k, 0)


def _kho(ten: str) -> str:
    from fls.db.kho import doi_ten_kho, dsn_that, dung_lai_kho_test
    dsn = doi_ten_kho(dsn_that(), ten)
    dung_lai_kho_test(dsn)
    return dsn


@pytest.fixture()
def kho():
    ten = f"fls_stg_n5_{os.getpid()}"
    dsn = _kho(ten)
    yield dsn
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {ten} WITH (FORCE)")


def _chay(monkeypatch, dsn: str, *args: str, ghi: bool = True, tep_json: Path | None = None):
    sys.path.insert(0, str(GOC))
    from tools.staging import nap_nguon_that as nn
    monkeypatch.setenv("PG_DSN", dsn)
    if ghi:
        monkeypatch.setenv("FLS_CHO_GHI_THAT", "1")
    else:
        monkeypatch.delenv("FLS_CHO_GHI_THAT", raising=False)
    a = list(args) + (["--json", str(tep_json)] if tep_json else [])
    return nn.main(a)


def _dem(dsn: str, sql: str) -> int:
    with psycopg.connect(dsn, autocommit=True) as c:
        return int(c.execute(sql).fetchone()[0])


# ═══ ⓐ DỮ LIỆU CŨ — phát lại ảnh đóng băng, khớp 100 % số đã đo (AC-7 · AC-3) ═══
def test_CU_phat_lai_anh_nap_vao_kho_khop_100pct_so_da_do(monkeypatch, moi_truong, san_0, kho, tmp_path, capsys):
    j = tmp_path / "bc.json"
    rc = _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu", "--bo-buoc", "khai,mapping,chup", tep_json=j)
    out = capsys.readouterr().out
    so = json.loads(j.read_text(encoding="utf-8"))["so"]
    assert rc == 0, out
    # (Đ3) mẫu số ≠ 0 TRƯỚC khi tin các phép "= 0"
    assert so["so_vao"] == ANH["so_dong_bank"] == 9992 and so["pm_dong"] == ANH["so_dong_pm"] == 3703
    # số ĐÃ ĐO (voi_so_luong.json) — phát lại ảnh qua ĐÚNG đường đọc→canon→ghép ⇒ trùng từng số
    assert so["pm_dong"] == VSL["pm_tong"]["so_dong_pm"]
    assert so["pm_co_ref"] == VSL["pm_tong"]["pm_co_ref"] == 3173
    bt = so["bac_thang_nay"]
    assert bt["dong_bank"] == VSL["bank_tong"]["dong_bank"] == 9992
    assert bt["khong_co_ma"] == VSL["bank_tong"]["khong_co_ma"] == 105
    assert bt["khong_thay_ma_PM"] == VSL["bank_tong"]["khong_thay_ma_PM"] == 6532
    assert bt["dong_theo_hinh"] == VSL["bank_tong"]["dong_theo_hinh"]
    # CŨ ↔ HIỆN TẠI: ảnh phát lại ⇒ 0 mất · 0 lệch · 0 mới
    for k in ("bank_mat", "bank_lech_ref", "bank_lech_cur", "bank_lech_tien", "bank_mat_noi_dung", "pm_mat", "pm_lech_ref",
              "pm_lech_slip", "pm_lech_line", "pm_lech_cur", "pm_lech_status", "pm_lech_hd", "pm_lech_cdt1", "pm_lech_tien"):
        assert so[k] == 0, (k, so[k])
    assert so["bank_moi"] == 0 and so["pm_moi"] == 0
    # kho: Σ nguồn = Σ kho
    # 7 dòng ảnh có tiền 0 ⇒ tầng sổ loại "PS Nợ và PS Có" (adapter vẫn cho qua: canon 9.992): Σ sổ + loại = 9.992 = ảnh
    from decimal import Decimal
    khong = sum(1 for r in ANH["bank"] if Decimal(str(r["tien"])) == 0)
    assert khong == 7 and so["so_ra"] == 9992 and so["so_loai"] == 0
    assert _dem(kho, "SELECT count(*) FROM fls_itl") == 9992 - khong
    assert _dem(kho, "SELECT count(*) FROM fls_reject") == khong
    assert _dem(kho, "SELECT count(*) FROM fls_pm_line") == 3703


def test_CHAY_LAI_khong_nhan_doi_fls_itl_chi_THEM(monkeypatch, moi_truong, san_0, kho, capsys):
    a = ("--nap", "--nguoi-nap", "khanh.thu", "--bo-buoc", "khai,mapping,chup")
    assert _chay(monkeypatch, kho, *a) == 0
    n1 = _dem(kho, "SELECT count(*) FROM fls_itl")
    capsys.readouterr()
    assert _chay(monkeypatch, kho, *a) == 0, capsys.readouterr().out
    assert _dem(kho, "SELECT count(*) FROM fls_itl") == n1 == 9985          # lần 2 ⛔ nhân đôi (9.992 − 7 dòng tiền 0 bị loại)
    assert _dem(kho, "SELECT count(*) FROM fls_pm_line") == 3703


# ═══ Đ5 — ĐỎ hai chiều: sửa MỘT dòng ở nguồn ⇒ ĐỎ có tên (nguồn "bị sửa sau chốt") ═══
def _doi(g: SheetsGia, sid, tab, i, j, v):
    cu = g.kho[sid][tab][i][j]
    g.kho[sid][tab][i][j] = v
    return cu


def test_DO_sua_mot_tien_bank_sau_chot_thi_do_dung_ten(monkeypatch, moi_truong, san_0, kho, tmp_path, capsys):
    g = moi_truong
    cu = _doi(g, BAN_SAO_RAW.spreadsheet_id, BAN_SAO_RAW.sheet, 99, 4, 123456789.0)      # dòng sheet 100
    try:
        j = tmp_path / "bc.json"
        rc = _chay(monkeypatch, kho, "--kiem", "--bo-buoc", "khai,mapping,chup", ghi=False, tep_json=j)
        out = capsys.readouterr().out
        so = json.loads(j.read_text(encoding="utf-8"))["so"]
        assert rc == 1 and so["bank_lech_tien"] == 1 and so["bank_mat_noi_dung"] == 1, out
        assert re.search(r"\[ĐỎ\] dòng bank ảnh LỆCH `tien` ở nguồn sống \(đếm\)\s+1\s+\(mong 0\)", out), out
        assert "LỆCH `ref`" in out and so["bank_lech_ref"] == 0            # chỉ ĐÚNG trường bị sửa đỏ
    finally:
        _doi(g, BAN_SAO_RAW.spreadsheet_id, BAN_SAO_RAW.sheet, 99, 4, cu)


def test_DO_xoa_mot_dong_PM_thi_do_MAT_va_sua_hd_thi_do_hd(monkeypatch, moi_truong, san_0, kho, tmp_path, capsys):
    g = moi_truong
    pm = g.kho[BAN_SAO_RAW.spreadsheet_id]["[Importrange]PM_Unpivot"]
    cu_hd = pm[10][PM_COT["hd"]]
    pm[10][PM_COT["hd"]] = "HD-DA-SUA"
    luu = pm.pop()                                                         # mất dòng cuối
    try:
        j = tmp_path / "bc.json"
        rc = _chay(monkeypatch, kho, "--kiem", "--bo-buoc", "khai,mapping,chup", ghi=False, tep_json=j)
        so = json.loads(j.read_text(encoding="utf-8"))["so"]
        assert rc == 1 and so["pm_mat"] == 1 and so["pm_lech_hd"] == 1 and so["pm_lech_tien"] == 0, capsys.readouterr().out
    finally:
        pm.append(luu)
        pm[10][PM_COT["hd"]] = cu_hd


def test_DO_dong_MOI_sau_anh_dem_RIENG_khong_do(monkeypatch, moi_truong, san_0, kho, tmp_path, capsys):
    g = moi_truong
    tml = g.kho[BAN_SAO_RAW.spreadsheet_id][BAN_SAO_RAW.sheet]
    them = [""] * 38
    them[0], them[1], them[3], them[4], them[5], them[6] = 47000, "FT-MOI-0001", "VND", 5000.0, 0, "R | MOI1"
    tml.append(them)
    try:
        j = tmp_path / "bc.json"
        rc = _chay(monkeypatch, kho, "--kiem", "--bo-buoc", "khai,mapping,chup", ghi=False, tep_json=j)
        so = json.loads(j.read_text(encoding="utf-8"))["so"]
        out = capsys.readouterr().out
        assert rc == 0 and so["bank_moi"] == 1 and so["so_vao"] == 9993, out
        ky = so["theo_ky_canon"]
        assert "2028-01" in str(ky) or sum(ky.values()) == 9993           # kỳ mới ghi nhãn riêng
        assert "MỚI — dòng canon nguồn sống ⛔ có trong ảnh (đếm, nhãn riêng)" in out
    finally:
        tml.pop()


def test_DO_cong_doc_du_do_thi_KHONG_ghi_mot_dong_nhung_van_do(monkeypatch, moi_truong, kho, tmp_path, capsys):
    """Sàn thật (3.300…) trên nguồn tổng hợp ⇒ cổng đọc-đủ ĐỎ: ⛔ ghi `fls_itl`, VẪN đếm nguồn (như nguồn sống 23/11)."""
    j = tmp_path / "bc.json"
    rc = _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu", "--bo-buoc", "khai,mapping,chup", tep_json=j)
    out = capsys.readouterr().out
    so = json.loads(j.read_text(encoding="utf-8"))["so"]
    assert rc == 1, out
    assert re.search(r"\[ĐỎ\] cổng đọc-đủ \(nguồn có đủ ô so với sàn đã đo 27/08\)\s+False", out), out
    assert "[ĐỎ] KHO: sổ ĐÃ ghi" in out
    assert _dem(kho, "SELECT count(*) FROM fls_itl") == 0                  # ⛔ ghi
    assert so["so_vao"] == 9992                                            # …nhưng ĐÃ đo nguồn


# ═══ Đ5 — quyền đọc: 403 một workbook ⇒ ĐỎ có tên, phần ấy DỪNG, phần khác vẫn chạy ═══
def test_DO_403_workbook_bank_thi_dung_phan_khai_va_chup_con_so_van_chay(monkeypatch, moi_truong, san_0, kho, capsys):
    g = moi_truong
    g.cam.add(BANK_ID)
    try:
        rc = _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu")
        out = capsys.readouterr().out
        assert rc == 1, out
        assert re.search(r"\[ĐỎ\] HTTP đọc workbook BANK \(60 sheet `R \|` ngân hàng\)\s+403", out), out
        assert re.search(r"\[ĐỎ\] bước khai chạy được — DỪNG vì ⛔ quyền đọc workbook BANK", out), out
        assert re.search(r"\[ĐỎ\] bước chup chạy được — DỪNG", out), out
        assert re.search(r"\[ĐẠT\] HTTP đọc workbook RAW", out)
        assert _dem(kho, "SELECT count(*) FROM fls_itl") == 9985           # sổ vẫn được nạp
        assert _dem(kho, "SELECT count(*) FROM fls_source WHERE src_type IN ('Bank','Cash')") == 0
    finally:
        g.cam.discard(BANK_ID)


# ═══ AC-2 — bốn bước chạy thật trên nguồn tổng hợp (khai · mapping · chụp có nguồn 0 dòng) ═══
def test_BON_BUOC_tong_hop_so_nguon_bang_so_kho_va_nguon_0_dong_van_co_mat(monkeypatch, moi_truong, san_0, kho, tmp_path, capsys):
    j = tmp_path / "bc.json"
    rc = _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu", tep_json=j)
    out = capsys.readouterr().out
    so = json.loads(j.read_text(encoding="utf-8"))["so"]
    assert rc == 0, out
    assert (so["khai_bank"], so["khai_quy"]) == (3, 1)
    assert _dem(kho, "SELECT count(*) FROM fls_source WHERE src_type IN ('Bank','Cash')") == 4
    assert _dem(kho, "SELECT count(*) FROM fls_khai_cot") == 4 * 6
    assert so["mm_ma"] == 6 == _dem(kho, "SELECT count(*) FROM fls_mapping_master")
    assert so["chup_sheet"] == 3 and so["chup_dong"] == 8 and so["chup_rong"] == 1       # AAA 5 + BBB 3 + CCC 0
    assert _dem(kho, "SELECT count(*) FROM fls_chup_nguon") == 3 and _dem(kho, "SELECT count(*) FROM fls_chup_dong") == 8
    assert _dem(kho, "SELECT count(*) FROM fls_chup_nguon n WHERE NOT EXISTS (SELECT 1 FROM fls_chup_dong d"
                " WHERE d.chup_id = n.chup_id AND d.source_id = n.source_id)") == 1


# ═══ AC-4 — riêng tư ═══
def test_RIENG_TU_Email_Address_khong_vao_kho_con_Ten_tai_khoan_GIU(monkeypatch, moi_truong, san_0, kho, capsys):
    assert _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu", "--bo-buoc", "khai,mapping,chup") == 0
    out = capsys.readouterr().out
    n = _dem(kho, "SELECT count(*) FROM fls_pm_line")
    assert n == 3703                                                       # (Đ3) mẫu số ≠ 0
    assert _dem(kho, "SELECT count(*) FROM fls_pm_line WHERE tho::jsonb ? 'Email Address'") == 0
    assert _dem(kho, f"SELECT count(*) FROM fls_pm_line WHERE tho::text LIKE '%{EMAIL_GIA}%'") == 0
    assert _dem(kho, "SELECT count(*) FROM fls_pm_line WHERE tho::jsonb ? 'Tên tài khoản'") == n      # GIỮ (QĐ 11/09)
    assert EMAIL_GIA not in out and TEN_TK_GIA not in out                  # BÁO CÁO ⛔ in nội dung
    assert "Email Address" in out and "(đếm)" in out


def test_RIENG_TU_cot_email_lot_vao_kho_thi_DO(monkeypatch, moi_truong, san_0, kho, capsys):
    monkeypatch.setenv("PG_DSN", kho)                                       # `cong_pg()` đọc cổng từ đây
    H.chay_quan_tri('ALTER TABLE fls_run ADD COLUMN "Email Address" text', re.search(r"/(\w+)$", kho).group(1))
    rc = _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu", "--bo-buoc", "khai,mapping,chup")
    assert rc == 1 and "[ĐỎ] cột tên có 'email' (đếm, ⛔ vào kho)" in capsys.readouterr().out


def test_BAO_CAO_chi_so_dem_khong_ro_ri_thong_tin(monkeypatch, moi_truong, san_0, kho, capsys):
    _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu")
    out = capsys.readouterr().out
    for xau in ("Bearer", "token-gia", EMAIL_GIA, TEN_TK_GIA, "MKGIA", "FT-MOI", "dien giai gia"):
        assert xau not in out, xau
    for r in ANH["pm"][:50] + ANH["bank"][:50]:                           # mẫu: tiền dòng / mã tham chiếu ⛔ xuất hiện
        assert str(r["ref_tho"]) not in out or len(str(r["ref_tho"])) < 6


# ═══ luật ghi ═══
def test_TU_CHOI_thieu_cong_ghi_nguoi_nap_xau_va_kho_5433(monkeypatch, moi_truong, kho):
    sys.path.insert(0, str(GOC))
    from tools.staging import nap_nguon_that as nn
    monkeypatch.setenv("PG_DSN", kho)
    monkeypatch.delenv("FLS_CHO_GHI_THAT", raising=False)
    with pytest.raises(SystemExit, match="FLS_CHO_GHI_THAT"):
        nn.main(["--nap", "--nguoi-nap", "khanh.thu"])
    monkeypatch.setenv("FLS_CHO_GHI_THAT", "1")
    for xau in ("", "a@b.com", "x;rm"):
        with pytest.raises(SystemExit, match="nguoi-nap"):
            nn.main(["--nap", "--nguoi-nap", xau])
    monkeypatch.setenv("PG_DSN", "postgresql://fls:x@localhost:5433/fls")
    with pytest.raises(SystemExit, match="5433"):
        nn.main(["--nap", "--nguoi-nap", "khanh.thu"])


def test_KHONG_GHI_ve_sheet_may_chu_khong_thay_yeu_cau_ghi_va_ma_khong_co_duong_ghi(monkeypatch, moi_truong, san_0, kho, nguon):
    g, _ = nguon
    _chay(monkeypatch, kho, "--nap", "--nguoi-nap", "khanh.thu", "--bo-buoc", "chup")
    assert g.so_goi > 0 and g.ghi_phat_hien == 0
    for tep in ("tools/staging/nap_nguon_that.py", "tools/staging/cred_sheets.py", "tools/nap_that.py", "tools/nap_mapping_master.py",
                "tools/chup_sao_ke.py", "tools/nap_nguon_va_khai.py", "tools/nap_sao_ke.py"):
        ma = "\n".join(l for l in (GOC / tep).read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))
        ma = re.sub(r'"""[\s\S]*?"""', "", ma)
        assert not re.search(r'method\s*=\s*["\'](POST|PUT|PATCH|DELETE)|:append|values:update|:batchUpdate|\.clear\b', ma), tep
    # phạm vi chỉ-đọc (⛔ `spreadsheets` đầy đủ, ⛔ `drive` đầy đủ)
    cred = (GOC / "tools/staging/cred_sheets.py").read_text(encoding="utf-8")
    assert "spreadsheets.readonly" in cred and "drive.metadata.readonly" in cred
    assert not re.search(r'auth/spreadsheets["\']|auth/drive["\']', cred)


# ═══ token: một chỗ, có tên đường, ⛔ lộ giá trị ═══
def test_cred_sheets_thu_tu_va_khong_lo_gia_tri(monkeypatch):
    from tools.staging import cred_sheets as c
    for k in ("FLS_SHEETS_TOKEN", "FLS_SHEETS_SA_JSON_TEP", "FLS_GSHEETS_SA_JSON", "FLS_GSHEETS_SA_JSON_B64", "FLS_SHEETS_ADC"):
        monkeypatch.delenv(k, raising=False)
    assert c.kieu() == "gcloud-cu"
    monkeypatch.setenv("FLS_SHEETS_ADC", "1")
    assert c.kieu() == "adc"
    monkeypatch.setenv("FLS_GSHEETS_SA_JSON_B64", "xx")
    assert c.kieu() == "sa-env-b64"
    monkeypatch.setenv("FLS_SHEETS_SA_JSON_TEP", "/x")
    assert c.kieu() == "sa-tep"
    monkeypatch.setenv("FLS_SHEETS_TOKEN", "BI-MAT-123")
    assert c.kieu() == "token-dua-san" and c.lay_token() == "BI-MAT-123" and "BI-MAT-123" not in c.mo_ta()


def test_cac_cong_cu_nap_di_qua_MOT_cho_lay_token():
    """Đ1 (cả hai nơi): không công cụ nạp nào còn tự gọi `gcloud … --account <SA>` ngoài hàm tương thích `_token_cu`."""
    for tep in ("tools/nap_that.py", "tools/nap_mapping_master.py", "tools/do_hinh_dang.py"):
        ma = (GOC / tep).read_text(encoding="utf-8")
        assert "cred_sheets" in ma, tep
    th = (GOC / "tools/do_hinh_dang.py").read_text(encoding="utf-8")
    assert "if _lay_token is not None:" in th


# ═══ 05_nap_nguon_that.sh ═══
S05 = "05_nap_nguon_that.sh"


@pytest.fixture(scope="module")
def kho_05(kho_san):
    return kho_san


def _chay05(mt, goc_api, *args, ghi=True, tok=True, env_them=None):
    env = {"FLS_SHEETS_API_GOC": goc_api}
    if tok:
        env["FLS_SHEETS_TOKEN"] = "token-gia"
    else:                                   # ⛔ khoá SA của container (nếu có) làm nhiễu phép thử "chưa khai cách cấp quyền"
        env.update(FLS_SHEETS_TOKEN="", FLS_GSHEETS_SA_JSON_B64="", FLS_GSHEETS_SA_JSON="")
    if ghi:
        env["FLS_CHO_GHI_THAT"] = "1"
    if env_them:
        env.update(env_them)
    return H.chay_script(S05, mt["gia"], mt["kho"], mt["qt"], *args, env_them=env, thoi_gian=420)


def test_05_sh_tu_choi_dung_luat_va_khong_goi_gcloud(kho_05, nguon):
    g, goc = nguon
    mt = kho_05
    mt["gia"]["gcloud_log"].write_text("")
    cases = [(("--nguoi-nap", "khanh.thu"), False, True, "FLS_CHO_GHI_THAT"),
             ((), True, True, "--nguoi-nap"), (("--nguoi-nap", "a@b.com"), True, True, "--nguoi-nap"),
             (("--nguoi-nap", "khanh.thu"), True, False, "chưa khai cách cấp quyền"),
             (("--nguoi-nap", "khanh.thu", "--adc", "--sa-json-tep", "/x"), True, True, "MỘT cách"),
             (("--nguoi-nap", "khanh.thu", "--sa-json-tep", "/khong/co/tep"), True, True, "không thấy tệp khoá")]
    for args, ghi, tok, loi in cases:
        r = _chay05(mt, goc, *args, ghi=ghi, tok=tok)
        assert r.returncode == 2 and loi in r.stderr, (args, r.returncode, r.stderr)
    assert mt["gia"]["gcloud_log"].read_text() == ""                       # từ chối TRƯỚC mọi lệnh gcloud


def test_05_sh_kiem_chi_doc_khong_ghi_mot_dong(kho_05, nguon):
    g, goc = nguon
    mt = kho_05
    r = _chay05(mt, goc, "--kiem", ghi=False)
    out = r.stdout
    assert "SELECT" not in r.stderr
    assert re.search(r"chế độ\s+CHỈ ĐỌC", out), out + r.stderr
    log = mt["gia"]["gcloud_log"].read_text()
    assert "fls-staging-pg-fls_ghi" in log and "fls_doc" not in log and "fls_admin" not in log and "postgres" not in log.replace("sql instances", "")
    assert "token-gia" not in out + r.stderr and "MKGIA" not in out + r.stderr


def test_05_sh_nap_that_bang_fls_ghi_qua_proxy_cong_doc_du_do_chan_so_con_lai_vao_va_chay_lai_khong_nhan_doi(kho_05, nguon):
    """Nguồn tổng hợp ⛔ đạt sàn đọc-đủ (3.300…) ⇒ sổ ⛔ ghi + ĐỎ có tên; ba bước kia vào kho bằng vai `fls_ghi` THẬT qua proxy GIẢ.
    Chạy lại ⇒ số dòng ⛔ đổi (mapping thay trọn; nguồn/khai `đã có`)."""
    g, goc = nguon
    mt = kho_05
    r1 = _chay05(mt, goc, "--nguoi-nap", "khanh.thu")
    assert r1.returncode == 1, r1.stdout + r1.stderr                  # cổng đọc-đủ ĐỎ ⇒ cả lượt ĐỎ
    assert "[ĐỎ] cổng đọc-đủ" in r1.stdout and "[ĐỎ] KHO: sổ ĐÃ ghi" in r1.stdout, r1.stdout
    assert "du-an-gia:asia-southeast1:fls-staging" in mt["gia"]["proxy_log"].read_text()
    ds = {k: _dem_kho(mt, q) for k, q in (("itl", "SELECT count(*) FROM fls_itl"), ("src", "SELECT count(*) FROM fls_source WHERE src_type IN ('Bank','Cash')"),
                                           ("khai", "SELECT count(*) FROM fls_khai_cot"), ("mm", "SELECT count(*) FROM fls_mapping_master"))}
    assert ds == {"itl": 0, "src": 4, "khai": 24, "mm": 6}, ds
    r2 = _chay05(mt, goc, "--nguoi-nap", "khanh.thu")
    assert r2.returncode == 1
    assert ds == {k: _dem_kho(mt, q) for k, q in (("itl", "SELECT count(*) FROM fls_itl"), ("src", "SELECT count(*) FROM fls_source WHERE src_type IN ('Bank','Cash')"),
                                                   ("khai", "SELECT count(*) FROM fls_khai_cot"), ("mm", "SELECT count(*) FROM fls_mapping_master"))}
    assert "token-gia" not in r1.stdout + r1.stderr + r2.stdout + r2.stderr and "MKGIA" not in r1.stdout + r1.stderr


def _dem_kho(mt, sql):
    return int(H.chay_quan_tri(sql, mt["kho"]))
