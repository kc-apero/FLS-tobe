# -*- coding: utf-8 -*-
"""DT1b — XUẤT bản đọc khoá (`tools/xuat_khoa_dt1b.py`): đọc `ITL Ledge` (.xlsx) + `Transaction
Mapping L1` (.csv) ⇒ CSV 7 cột cho `phan_loai_ly_do.py --khoa`.

ISP 3.1.2 · Step 5 · DT1b · phiếu `WO-127` / `BG-128` · AP v3.1.2 §5.3.1 HD1 ★.

⛔⛔ Khoá THẬT ⛔ đọc được ở container (`B-DATA-2`): `[Master] ITL_Ledge_raw.xlsx` + `Transaction
   Mapping L1` chỉ có trên máy owner (O10). ⇒ MỌI bài ở đây dựng xlsx/CSV TỔNG HỢP trong `tmp_path`
   bằng `zipfile` + `csv` (⛔ một giá trị thật nào): Số CT tổng hợp mang tiền tố `SYN`/`POISON`/`DECOY`
   hoặc số 16 chữ số dựng tay; tiền `'2,730,128.00'` là HÌNH của fixture, ⛔ trị thật.

⛔⛔ Mỗi bài canh một cái bẫy CÓ THẬT của WO-127:
  · `AC-1` — cột theo TÊN TIÊU ĐỀ (⛔ chữ cái cột): bộ dựng ĐẶT 5 tiêu đề ở cột RẢI + xen cột `Diễn
    giải`/`Email Address` phải bị BỎ; `dong` = HÀNG EXCEL (bỏ hàng trống 8·9, dữ liệu từ 10); ô thô
    xuất NGUYÊN (số `<v>` ⛔ qua float). Thiếu cột ⇒ lỗi CÓ TÊN, mã ≠ 0.
  · `AC-2` — CSV L1 (hình Google Sheets tải về: tiêu đề ở hàng 3, hàng 4 trống): `dong` = số hàng
    sheet; cột theo tên.
  · `AC-3` — RIÊNG TƯ (CLAUDE.md): ⛔ một giá trị ô nào lên stdout/stderr (ca PHÁ: giá trị SỐNG trong
    TỆP RA mà ⛔ trong màn); ra mặc định `hien_vat/` (gitignore); TỪ CHỐI đường ra trong repo ⛔ gitignore.
  · `AC-4` — NỐI: xuất ⇒ `phan_loai_ly_do.py --khoa` chạy được; và Số CT SỐ `4366190000000000` (phía
    SO) ↔ dạng khoa học `4.36619E+15` (phía L1 — hình Sheets) gỡ về CÙNG khoá (canon_ref), ⇒ xuất
    NGUYÊN `<v>` là đủ cho một bản khai chuẩn hoá duy nhất ở `phan_loai_ly_do.py`.

Mã thoát (khai trong công cụ): 0 xuất xong · 1 lỗi đọc/định dạng · 2 sai cách gọi.
"""
from __future__ import annotations

import csv
import importlib.util
import io
import os
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "xuat_khoa_dt1b.py"
TOOL_PL = GOC / "tools" / "phan_loai_ly_do.py"

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"
NS_WS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet"
NS_SST = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings"

TIEU_DE = {"so_ct": "Số chứng từ", "ps_no": "PS Nợ", "ps_co": "PS Có",
           "tk": "Tài khoản", "tien_te": "Đơn vị tiền tệ"}
COT_RA = ("bang", "dong", "so_ct", "ps_no", "ps_co", "tk", "tien_te")


# ═════════════════════════════════════════════════════════════════════════ trợ thủ
def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, capture_output=True,
                          text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})


def _chay_pl(*doi_so: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL_PL), *doi_so], cwd=GOC, capture_output=True,
                          text=True, encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})


def _tool():
    """Nạp công cụ TRONG thân bài (⛔ ở mức mô-đun): công cụ chưa có thì bài FAILED vì thiếu hành vi."""
    spec = importlib.util.spec_from_file_location("_xuat_khoa_dt1b", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _doc_csv(p: Path) -> list[list[str]]:
    with p.open(encoding="utf-8", newline="") as f:
        return list(csv.reader(f))


def _esc(s) -> str:
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _chu_cot(c0: int) -> str:
    s, c = "", c0 + 1
    while c:
        c, r = divmod(c - 1, 26)
        s = chr(65 + r) + s
    return s


def _o_xml(row: int, col0: int, val, shared: dict[str, int]) -> str:
    """Một `<c>`. `val`: str ⇒ sharedString · ('n',t) số thô · ('inline',t) · ('str',t) công thức."""
    ref = f"{_chu_cot(col0)}{row}"
    if isinstance(val, tuple):
        kind, text = val
        if kind == "n":
            return f'<c r="{ref}"><v>{_esc(text)}</v></c>'
        if kind == "str":
            return f'<c r="{ref}" t="str"><v>{_esc(text)}</v></c>'
        if kind == "inline":
            return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{_esc(text)}</t></is></c>'
        raise ValueError(kind)
    if val not in shared:
        shared[val] = len(shared)
    return f'<c r="{ref}" t="s"><v>{shared[val]}</v></c>'


def _ws_xml(grid: dict[tuple[int, int], object], shared: dict[str, int]) -> str:
    theo_hang: dict[int, list[tuple[int, object]]] = {}
    for (r, c), v in grid.items():
        theo_hang.setdefault(r, []).append((c, v))
    rows = []
    for r in sorted(theo_hang):
        o = "".join(_o_xml(r, c, v, shared) for c, v in sorted(theo_hang[r]))
        rows.append(f'<row r="{r}">{o}</row>')
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<worksheet xmlns="{NS_MAIN}"><sheetData>{"".join(rows)}</sheetData></worksheet>')


def _lam_xlsx(path: Path, grid_ledge: dict, grid_bia: dict | None = None,
              ten_sheet: str = "ITL Ledge") -> Path:
    """Dựng .xlsx TỐI THIỂU HỢP LỆ: sheet decoy `Bìa` (ĐỨNG TRƯỚC) + sheet `ten_sheet` mang `grid_ledge`.
    ⇒ công cụ phải TÌM SHEET THEO TÊN, ⛔ lấy sheet đầu."""
    shared: dict[str, int] = {}
    ws_bia = _ws_xml(grid_bia or {}, shared)
    ws_ledge = _ws_xml(grid_ledge, shared)
    sst_si = "".join(f'<si><t xml:space="preserve">{_esc(t)}</t></si>'
                     for t in sorted(shared, key=lambda k: shared[k]))
    sst = f'<?xml version="1.0"?><sst xmlns="{NS_MAIN}" count="{len(shared)}" uniqueCount="{len(shared)}">{sst_si}</sst>'
    workbook = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                f'<workbook xmlns="{NS_MAIN}" xmlns:r="{NS_REL}"><sheets>'
                f'<sheet name="Bìa" sheetId="1" r:id="rId1"/>'
                f'<sheet name="{_esc(ten_sheet)}" sheetId="2" r:id="rId2"/>'
                f'</sheets></workbook>')
    rels = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_PKG}">'
            f'<Relationship Id="rId1" Type="{NS_WS}" Target="worksheets/sheet1.xml"/>'
            f'<Relationship Id="rId2" Type="{NS_WS}" Target="worksheets/sheet2.xml"/>'
            f'<Relationship Id="rId3" Type="{NS_SST}" Target="sharedStrings.xml"/>'
            f'</Relationships>')
    ct = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          f'<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
          f'<Default Extension="xml" ContentType="application/xml"/>'
          f'<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
          f'</Types>')
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", ct)
        z.writestr("xl/workbook.xml", workbook)
        z.writestr("xl/_rels/workbook.xml.rels", rels)
        z.writestr("xl/sharedStrings.xml", sst)
        z.writestr("xl/worksheets/sheet1.xml", ws_bia)
        z.writestr("xl/worksheets/sheet2.xml", ws_ledge)
    return path


def _lam_l1(path: Path, hang: list[list[str]]) -> Path:
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(hang)
    return path


# Tiêu đề rải ở CỘT KHÁC NHAU (⛔ theo thứ tự) + cột Diễn giải/Email xen vào ⇒ phải bị bỏ.
# col:  B=1 Số CT · C=2 Diễn giải · D=3 Đơn vị tiền tệ · E=4 PS Nợ · F=5 PS Có · G=6 Tài khoản · U=20 Email
_TD_LEDGE = {(7, 1): "Số chứng từ", (7, 2): "Diễn giải", (7, 3): "Đơn vị tiền tệ",
             (7, 4): "PS Nợ", (7, 5): "PS Có", (7, 6): "Tài khoản", (7, 20): "Email Address"}


def _ledge_ba_dong() -> dict:
    """Tiêu đề hàng 7 · hàng 9 TRỐNG HẲN (bị bỏ) · dữ liệu hàng 10·11·12 (dong = hàng Excel)."""
    g = dict(_TD_LEDGE)
    g[(9, 6)] = ("inline", "")                     # hàng trống hẳn ⇒ công cụ BỎ (⛔ thành dòng dữ liệu)
    # hàng 10: Số CT là SỐ (⛔ qua float) · tiền '2,730,128.00' chuỗi · PS Có TRỐNG · TK inline · Diễn giải + email phải biến mất
    g.update({(10, 1): ("n", "4366190000000000"), (10, 2): "Chi tiền A — BÍ MẬT",
              (10, 3): "VND", (10, 4): "2,730,128.00", (10, 6): ("inline", "1121"),
              (10, 20): "ke-toan@cong-ty.vn"})
    g.update({(11, 1): "SYN000011", (11, 3): "USD", (11, 4): "0", (11, 5): "500", (11, 6): "3311"})
    g.update({(12, 1): ("inline", "SYN000012"), (12, 3): "VND", (12, 5): ("n", "123.45"), (12, 6): "1121"})
    return g


# ═════════════════════════════════════════════════════════════════════════ AC-1 · xlsx ⇒ 7 cột
def test_AC1_xlsx_ra_7_cot_dong_hang_excel_o_tho(tmp_path):
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    l1 = _lam_l1(tmp_path / "l1.csv", [["Số chứng từ", "PS Nợ", "PS Có", "Tài khoản", "Đơn vị tiền tệ"]])
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (kq.returncode, kq.stdout, kq.stderr)
    bang = _doc_csv(ra)
    assert bang[0] == list(COT_RA)                                   # đúng 7 cột, đúng thứ tự
    so = [r for r in bang[1:] if r[0] == "SO"]
    # dong = HÀNG EXCEL 10·11·12 (bỏ hàng trống 8·9) — ⛔ 1·2·3
    assert [r[1] for r in so] == ["10", "11", "12"], so
    # hàng 10: so_ct SỐ xuất NGUYÊN (⛔ '4.36619e+15', ⛔ '...0.0') · ps_co TRỐNG · tk inline
    assert so[0] == ["SO", "10", "4366190000000000", "2,730,128.00", "", "1121", "VND"], so[0]
    assert so[1] == ["SO", "11", "SYN000011", "0", "500", "3311", "USD"], so[1]
    assert so[2] == ["SO", "12", "SYN000012", "", "123.45", "1121", "VND"], so[2]
    # Diễn giải + Email ⛔ BAO GIỜ lọt (cột ngoài 5 khoá)
    tho = ra.read_text(encoding="utf-8")
    assert "BÍ MẬT" not in tho and "ke-toan@cong-ty.vn" not in tho


def test_AC1_doc_xlsx_ledge_dong_la_hang_excel_va_o_tho(tmp_path):
    mod = _tool()
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    hang = mod.doc_xlsx_ledge(xlsx)
    assert [h["dong"] for h in hang] == [10, 11, 12]
    assert hang[0] == {"dong": 10, "so_ct": "4366190000000000", "ps_no": "2,730,128.00",
                       "ps_co": "", "tk": "1121", "tien_te": "VND"}


def test_AC1_tim_sheet_theo_ten_khong_lay_sheet_dau(tmp_path):
    """Sheet decoy `Bìa` ĐỨNG TRƯỚC, mang CÙNG 5 tiêu đề + dữ liệu DECOY ⇒ công cụ phải đọc `ITL Ledge`."""
    bia = {(7, 1): "Số chứng từ", (7, 3): "Đơn vị tiền tệ", (7, 4): "PS Nợ", (7, 5): "PS Có",
           (7, 6): "Tài khoản", (10, 1): "DECOY_CT", (10, 4): "9", (10, 6): "9999", (10, 3): "XXX"}
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong(), grid_bia=bia)
    hang = _tool().doc_xlsx_ledge(xlsx)
    assert all(h["so_ct"] != "DECOY_CT" for h in hang)
    assert {h["so_ct"] for h in hang} == {"4366190000000000", "SYN000011", "SYN000012"}


def test_AC1_thieu_cot_bao_loi_co_ten_ma_khac_0(tmp_path):
    g = _ledge_ba_dong()
    del g[(7, 6)]                                   # bỏ tiêu đề 'Tài khoản'
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", g)
    l1 = _lam_l1(tmp_path / "l1.csv", [list(TIEU_DE.values())])
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 1, (kq.returncode, kq.stdout, kq.stderr)
    assert "Tài khoản" in kq.stderr                 # lỗi CÓ TÊN
    assert not (tmp_path / "k.csv").exists()


def test_AC1_sheet_sai_ten_bao_loi(tmp_path):
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong(), ten_sheet="Sheet khác")
    l1 = _lam_l1(tmp_path / "l1.csv", [list(TIEU_DE.values())])
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 1 and "ITL Ledge" in kq.stderr, (kq.returncode, kq.stderr)


# ═════════════════════════════════════════════════════════════════════════ AC-2 · CSV L1
def _l1_hinh_sheets() -> list[list[str]]:
    # Hình Google Sheets tải về: hàng 1 tiêu đề báo cáo · hàng 2 trống · hàng 3 TIÊU ĐỀ · hàng 4 trống · 5+ dữ liệu
    return [
        ["Transaction Mapping L1", "", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["Số chứng từ", "Diễn giải", "Đơn vị tiền tệ", "PS Nợ", "PS Có", "Tài khoản"],
        ["", "", "", "", "", ""],
        ["4.36619E+15", "mô tả", "VND", "2730128", "0", "1121"],
        ["SYN000011", "mô tả 2", "USD", "0", "500", "3311"],
    ]


def test_AC2_l1_csv_ra_hang_L1_dong_la_hang_sheet(tmp_path):
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    l1 = _lam_l1(tmp_path / "l1.csv", _l1_hinh_sheets())
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout, kq.stderr)
    l1r = [r for r in _doc_csv(ra) if r[0] == "L1"]
    assert [r[1] for r in l1r] == ["5", "6"]        # dong = hàng SHEET (hàng 5·6)
    assert l1r[0] == ["L1", "5", "4.36619E+15", "2730128", "0", "1121", "VND"], l1r[0]
    assert l1r[1] == ["L1", "6", "SYN000011", "0", "500", "3311", "USD"], l1r[1]
    assert "mô tả" not in ra.read_text(encoding="utf-8")   # Diễn giải bị bỏ


def test_AC2_l1_thieu_cot_bao_loi(tmp_path):
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    xau = [r[:5] for r in _l1_hinh_sheets()]        # cắt cột cuối ⇒ thiếu 'Tài khoản'
    l1 = _lam_l1(tmp_path / "l1.csv", xau)
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 1 and "Tài khoản" in kq.stderr, (kq.returncode, kq.stderr)


# ═════════════════════════════════════════════════════════════════════════ AC-3 · riêng tư
def test_AC3_khong_lo_gia_tri_o_stdout_stderr_ca_pha(tmp_path):
    """Giá trị ô ⛔ lên màn. Ca PHÁ: những sentinel này SỐNG trong TỆP RA (đường đo thật) — nếu công cụ
    in giá trị thì bài này ĐỎ; chúng vắng ở stdout/stderr nhưng CÓ ở tệp ra ⇒ phép quét có nghĩa."""
    g = dict(_TD_LEDGE)
    g.update({(10, 1): "POISON_CT_9988", (10, 3): "POISON_TTE", (10, 4): "POISON_NO",
              (10, 5): "POISON_CO", (10, 6): "POISON_TK", (10, 2): "POISON_DIENGIAI",
              (10, 20): "poison@secret.vn"})
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", g)
    l1 = _lam_l1(tmp_path / "l1.csv",
                 [list(TIEU_DE.values()), ["POISON_L1CT", "POISON_L1NO", "0", "1121", "VND"]])
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout, kq.stderr)
    man = kq.stdout + kq.stderr
    for s in ("POISON_CT_9988", "POISON_TTE", "POISON_NO", "POISON_CO", "POISON_TK",
              "POISON_DIENGIAI", "poison@secret.vn", "POISON_L1CT", "POISON_L1NO"):
        assert s not in man, f"giá trị ô {s!r} LỌT ra màn"
    tho = ra.read_text(encoding="utf-8")            # ca phá: giá trị SỐNG trong tệp ra (⛔ Diễn giải/email)
    assert "POISON_CT_9988" in tho and "POISON_L1CT" in tho
    assert "POISON_DIENGIAI" not in tho and "poison@secret.vn" not in tho
    assert "SO 1 hàng" in kq.stdout and "L1 1 hàng" in kq.stdout   # chỉ SỐ ĐẾM lên màn


def test_AC3_ra_mac_dinh_trong_hien_vat_va_duoc_phep():
    mod = _tool()
    assert mod.RA_MAC_DINH == GOC / "hien_vat" / "khoa_dt1b.csv"
    assert mod._trong_repo_khong_ignore(mod.RA_MAC_DINH) is False     # hien_vat/ BỊ gitignore ⇒ cho ghi


def test_AC3_ra_mac_dinh_chay_that_roi_don(tmp_path):
    """Chạy ⛔ --ra ⇒ ghi vào hien_vat/khoa_dt1b.csv (gitignore). Dọn sau."""
    mac_dinh = GOC / "hien_vat" / "khoa_dt1b.csv"
    co_truoc = mac_dinh.exists()
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    l1 = _lam_l1(tmp_path / "l1.csv", _l1_hinh_sheets())
    try:
        kq = _chay("--xlsx", str(xlsx), "--l1", str(l1))
        assert kq.returncode == 0, (kq.stdout, kq.stderr)
        assert mac_dinh.exists() and [r[0] for r in _doc_csv(mac_dinh)][0] == "bang"
    finally:
        if not co_truoc and mac_dinh.exists():
            mac_dinh.unlink()


def test_AC3_tu_choi_duong_ra_trong_repo_khong_gitignore(tmp_path):
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    l1 = _lam_l1(tmp_path / "l1.csv", _l1_hinh_sheets())
    nguy = GOC / "tools" / "_ro_ri_dt1b.csv"         # TRONG repo, ⛔ bị gitignore
    assert not mod_ignore(nguy)
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(nguy))
    assert kq.returncode == 2, (kq.returncode, kq.stdout, kq.stderr)
    assert "TỪ CHỐI" in kq.stderr
    assert not nguy.exists(), "đường ra nguy ⛔ được tạo"


def mod_ignore(p: Path) -> bool:
    r = subprocess.run(["git", "-C", str(GOC), "check-ignore", "-q", str(p.resolve())])
    return r.returncode == 0


def test_AC3_dau_vao_vang_ma_2(tmp_path):
    l1 = _lam_l1(tmp_path / "l1.csv", _l1_hinh_sheets())
    kq = _chay("--xlsx", str(tmp_path / "khong_co.xlsx"), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 2 and "⛔ thấy tệp --xlsx" in kq.stderr, (kq.returncode, kq.stderr)


# ═════════════════════════════════════════════════════════════════════════ AC-4 · nối phan_loai_ly_do
def _xlsx_csv_noi(tmp_path):
    """Một cặp GHÉP ĐƯỢC: phía SO Số CT là SỐ `4366190000000000`, phía L1 dạng khoa học `4.36619E+15`;
    bốn trường còn lại viết KHÁC DẠNG (trống↔'0', '2,730,128.00'↔'2730128', hoa↔thường) nhưng cùng khoá."""
    g = dict(_TD_LEDGE)
    g.update({(10, 1): ("n", "4366190000000000"), (10, 3): "VND",
              (10, 4): "2,730,128.00", (10, 6): "1121"})           # ps_co TRỐNG
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", g)
    l1 = _lam_l1(tmp_path / "l1.csv",
                 [list(TIEU_DE.values()), ["4.36619E+15", "2730128", "0", "1121", " vnd"]])
    return xlsx, l1


def test_AC4_so_ct_so_va_khoa_hoc_gop_cung_khoa(tmp_path):
    xlsx, l1 = _xlsx_csv_noi(tmp_path)
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout, kq.stderr)
    # xuất NGUYÊN `<v>` (⛔ float): so_ct phía SO đúng chuỗi 16 chữ số
    so = [r for r in _doc_csv(ra) if r[0] == "SO"][0]
    assert so[2] == "4366190000000000", so
    # nối: nạp phan_loai_ly_do, chuẩn hoá hai phía ⇒ CÙNG khoá
    spec = importlib.util.spec_from_file_location("_pl_noi", TOOL_PL)
    pl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pl)
    vao = pl.doc_khoa(ra)
    assert len(vao["so"]) == 1 and len(vao["l1"]) == 1
    (k_so,), (k_l1,) = list(vao["so"].values()), list(vao["l1"].values())
    assert k_so == k_l1, (k_so, k_l1)               # Số CT số ↔ khoa học gỡ về cùng khoá
    assert k_so[0] == "4366190000000000"


def test_AC4_xuat_roi_phan_loai_chay_duoc(tmp_path):
    """Nối end-to-end: xuất ⇒ `phan_loai_ly_do.py --khoa` CHẠY (mã 1/3/4 tuỳ dữ liệu — ⛔ đòi 0, ⛔ 2,
    ⛔ traceback). Dữ liệu tổng hợp ⛔ khớp 9.967/122 thật ⇒ công cụ ĐỎ ở cổng K11 (tập dong_sheet) — đó
    là 'chạy được + chẩn đoán', ⛔ phải sập."""
    xlsx, l1 = _xlsx_csv_noi(tmp_path)
    ra = tmp_path / "khoa.csv"
    assert _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra)).returncode == 0
    kq = _chay_pl("--khoa", str(ra))
    assert kq.returncode in (1, 3, 4), (kq.returncode, kq.stdout, kq.stderr)
    assert "Traceback" not in kq.stderr              # ⛔ sập — chẩn đoán một dòng
    assert "MẪU SỐ" in kq.stdout or "mẫu số" in kq.stderr or "dong_sheet" in kq.stderr
