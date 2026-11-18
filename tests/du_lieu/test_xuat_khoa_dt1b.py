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
              ten_sheet: str = "ITL Ledge", rels_ledge_tuyet_doi: bool = False,
              rels_ledge_tgt: str | None = None) -> Path:
    """Dựng .xlsx TỐI THIỂU HỢP LỆ: sheet decoy `Bìa` (ĐỨNG TRƯỚC) + sheet `ten_sheet` mang `grid_ledge`.
    ⇒ công cụ phải TÌM SHEET THEO TÊN, ⛔ lấy sheet đầu.

    `rels_ledge_tuyet_doi=True`: đích rels của sheet `ten_sheet` viết TUYỆT ĐỐI `"/xl/worksheets/sheet2.xml"`
    (dạng openpyxl & vài thư viện/dịch vụ sinh) thay vì tương đối `"worksheets/sheet2.xml"` (dạng Excel) —
    `DT1BT-R1-01`: công cụ phải đọc được CẢ HAI dạng.

    `rels_ledge_tgt=<chuỗi>`: GHI ĐÈ nguyên văn đích rels của sheet `ten_sheet` (để thử các dạng NGOÀI
    hai loại trên — `DT1BT-R2-02`: `xl/…` đã có tiền tố · `./…` · `../xl/…`). Ưu tiên hơn `rels_ledge_tuyet_doi`."""
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
    if rels_ledge_tgt is not None:
        tgt_ledge = rels_ledge_tgt
    else:
        tgt_ledge = "/xl/worksheets/sheet2.xml" if rels_ledge_tuyet_doi else "worksheets/sheet2.xml"
    rels = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<Relationships xmlns="{NS_PKG}">'
            f'<Relationship Id="rId1" Type="{NS_WS}" Target="worksheets/sheet1.xml"/>'
            f'<Relationship Id="rId2" Type="{NS_WS}" Target="{tgt_ledge}"/>'
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


# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║  VÒNG SỬA SAU R1 (KQ-129) — DT1BT-R1-01 · -02 · -03 · -04 · -05                                 ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝
SENTINEL = "SECRET_GIA_TRI_O_9988"      # chuỗi canh: giá trị ô THÔ — ⛔ BAO GIỜ được lên stdout/stderr


def _xlsx_thay_phan(src: Path, path: Path, thay: dict[str, bytes | None]) -> Path:
    """Chép mọi phần của `src` sang `path`, THAY (hoặc BỎ nếu None) các phần trong `thay`. Dựng tệp .xlsx
    HỎNG MỘT PHẦN (workbook/worksheet/sst XML hỏng · rels thiếu) để đo đường LỖI."""
    with zipfile.ZipFile(src) as zin:
        ten = zin.namelist()
        noi = {n: zin.read(n) for n in ten}
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        for n in ten:
            if n in thay:
                if thay[n] is None:
                    continue                      # BỎ phần này (vd rels thiếu)
                zout.writestr(n, thay[n])
            else:
                zout.writestr(n, noi[n])
    return path


def _l1_ok(tmp_path: Path) -> Path:
    return _lam_l1(tmp_path / "l1_ok.csv", [list(TIEU_DE.values()), ["x", "1", "2", "1121", "VND"]])


def _xlsx_co_sentinel(tmp_path: Path, ten_sheet: str = "ITL Ledge") -> Path:
    """xlsx HỢP LỆ, nhưng ô dữ liệu (10,1) mang SENTINEL ⇒ nếu công cụ in giá trị ở đường lỗi thì lộ."""
    g = dict(_TD_LEDGE)
    g.update({(10, 1): SENTINEL, (10, 3): "VND", (10, 4): "1", (10, 5): "2", (10, 6): "1121"})
    return _lam_xlsx(tmp_path / "ledge.xlsx", g, ten_sheet=ten_sheet)


# ── casau LỖI: mỗi hàm dựng (xlsx, l1) với MỘT đầu vào hỏng; sentinel nằm trong tệp hỏng ───────────
def _ca_workbook_xml_hong(tmp_path):
    ok = _xlsx_co_sentinel(tmp_path)
    xlsx = _xlsx_thay_phan(ok, tmp_path / "hong.xlsx",
                           {"xl/workbook.xml": f"<workbook>{SENTINEL}<broken".encode()})
    return xlsx, _l1_ok(tmp_path)


def _ca_worksheet_xml_hong(tmp_path):
    ok = _xlsx_co_sentinel(tmp_path)
    xlsx = _xlsx_thay_phan(ok, tmp_path / "hong.xlsx",
                           {"xl/worksheets/sheet2.xml": f'<worksheet><v>{SENTINEL}</v><broken'.encode()})
    return xlsx, _l1_ok(tmp_path)


def _ca_sharedstrings_hong(tmp_path):
    ok = _xlsx_co_sentinel(tmp_path)
    xlsx = _xlsx_thay_phan(ok, tmp_path / "hong.xlsx",
                           {"xl/sharedStrings.xml": f'<sst><si><t>{SENTINEL}</t><broken'.encode()})
    return xlsx, _l1_ok(tmp_path)


def _ca_rels_thieu(tmp_path):
    ok = _xlsx_co_sentinel(tmp_path)
    xlsx = _xlsx_thay_phan(ok, tmp_path / "hong.xlsx", {"xl/_rels/workbook.xml.rels": None})
    return xlsx, _l1_ok(tmp_path)


def _ca_zip_hong(tmp_path):
    p = tmp_path / "hong.xlsx"
    p.write_bytes(f"PK-gia-{SENTINEL}-khong-phai-zip".encode())     # ⛔ phải zip ⇒ BadZipFile
    return p, _l1_ok(tmp_path)


def _xlsx_lat_byte_nen(src: Path, path: Path, ten_phan: str, so_byte: int = 8) -> Path:
    """Chép `src` → `path` rồi LẬT `so_byte` byte ở GIỮA luồng NÉN của phần `ten_phan` (⛔ chạm cấu trúc
    zip: local header, central dir còn nguyên) ⇒ `z.read(ten_phan)` ném `zlib.error` (hoặc `BadZipFile`
    'Bad CRC-32') — chỉ phát ở lúc ĐỌC, ⛔ lúc MỞ zip. Dựng ca `DT1BT-R2-03`.

    Đọc local file header (30 byte cố định + n byte tên + m byte extra) để tìm đầu vùng dữ liệu nén."""
    raw = bytearray(src.read_bytes())
    with zipfile.ZipFile(src) as z:
        zi = z.getinfo(ten_phan)
    assert zi.compress_type == zipfile.ZIP_DEFLATED, ten_phan     # phải NÉN mới có luồng để lật
    off = zi.header_offset
    n = int.from_bytes(raw[off + 26:off + 28], "little")
    m = int.from_bytes(raw[off + 28:off + 30], "little")
    data_bd = off + 30 + n + m
    data_kt = data_bd + zi.compress_size
    giua = data_bd + max(0, zi.compress_size // 2 - so_byte // 2)
    for i in range(giua, min(giua + so_byte, data_kt)):
        raw[i] ^= 0xFF                                            # lật mọi bit của byte
    path.write_bytes(bytes(raw))
    return path


def _ca_zlib_hong(tmp_path):
    """xlsx HỢP LỆ mở được, nhưng luồng nén của `xl/worksheets/sheet2.xml` bị lật byte ⇒ `zlib.error`
    khi đọc worksheet. SENTINEL sống trong `sharedStrings.xml` (đọc TRƯỚC, nguyên) ⇒ ca này còn chứng
    minh: shared strings đã nạp vào bộ nhớ ⛔ lộ khi một phần SAU hỏng."""
    ok = _xlsx_co_sentinel(tmp_path)
    xlsx = _xlsx_lat_byte_nen(ok, tmp_path / "zlib_hong.xlsx", "xl/worksheets/sheet2.xml")
    return xlsx, _l1_ok(tmp_path)


def _ca_thieu_sheet(tmp_path):
    return _xlsx_co_sentinel(tmp_path, ten_sheet="Sheet La"), _l1_ok(tmp_path)


def _ca_thieu_cot(tmp_path):
    g = dict(_TD_LEDGE)
    del g[(7, 6)]                                     # bỏ tiêu đề 'Tài khoản'
    g.update({(10, 1): SENTINEL, (10, 3): "VND", (10, 4): "1", (10, 5): "2"})
    return _lam_xlsx(tmp_path / "ledge.xlsx", g), _l1_ok(tmp_path)


def _ca_l1_khong_utf8(tmp_path):
    p = tmp_path / "l1_bad.csv"
    p.write_bytes(("Số chứng từ,PS Nợ,PS Có,Tài khoản,Đơn vị tiền tệ\n" + SENTINEL + ",").encode("utf-8")
                  + b"\xf4\xf4,2,1121,VND\n")         # byte 0xf4 ⇒ ⛔ UTF-8
    return _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong()), p


def _ca_l1_co_nul(tmp_path):
    p = tmp_path / "l1_nul.csv"
    p.write_bytes(("Số chứng từ,PS Nợ,PS Có,Tài khoản,Đơn vị tiền tệ\n" + SENTINEL).encode("utf-8")
                  + b"\x00X,1,2,1121,VND\n")           # ký tự NUL ⇒ csv.Error
    return _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong()), p


def _ca_l1_truong_qua_dai(tmp_path):
    dai = SENTINEL + "A" * 200000                      # > 131 072 ký tự ⇒ _csv.Error
    p = _lam_l1(tmp_path / "l1_dai.csv",
                [list(TIEU_DE.values()), [dai, "1", "2", "1121", "VND"]])
    return _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong()), p


# DT1BT-R1-03: quét giá trị ô cho ĐƯỜNG LỖI (≥ các ca R1 dùng). Mỗi ca nhúng SENTINEL ⇒ 0 lần ở màn.
_CA_RORI = {
    "xml_workbook_hong": _ca_workbook_xml_hong,
    "xml_worksheet_hong": _ca_worksheet_xml_hong,
    "zip_hong": _ca_zip_hong,
    "zlib_hong": _ca_zlib_hong,
    "thieu_sheet": _ca_thieu_sheet,
    "thieu_cot": _ca_thieu_cot,
    "csv_khong_utf8": _ca_l1_khong_utf8,
    "csv_co_nul": _ca_l1_co_nul,
}


@pytest.mark.parametrize("ten_ca", list(_CA_RORI))
def test_DT1BT_R1_03_duong_loi_khong_lo_gia_tri_o(tmp_path, ten_ca):
    """RIÊNG TƯ — đường LỖI ⛔ lộ giá trị ô. Mỗi tệp hỏng mang SENTINEL; khẳng định SENTINEL ∉ stdout+stderr
    và mã thoát ≠ 0. ĐỎ dưới M6 (câu lỗi nối hàng dữ liệu) · M14 (nhánh `except` in giá trị)."""
    xlsx, l1 = _CA_RORI[ten_ca](tmp_path)
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode != 0, (ten_ca, kq.returncode, kq.stdout, kq.stderr)
    man = kq.stdout + kq.stderr
    assert SENTINEL not in man, f"[{ten_ca}] giá trị ô {SENTINEL!r} LỌT ra màn: {man!r}"
    assert not (tmp_path / "k.csv").exists(), f"[{ten_ca}] tệp ra ⛔ được tạo khi lỗi"


# DT1BT-R1-04: mọi tệp hỏng ⇒ MỘT dòng lỗi CÓ TÊN + mã ≠ 0, ⛔ Traceback; UnicodeDecodeError ⛔ in byte/vị trí.
_CA_HONG = {
    "xml_workbook_hong": _ca_workbook_xml_hong,
    "xml_worksheet_hong": _ca_worksheet_xml_hong,
    "xml_sharedstrings_hong": _ca_sharedstrings_hong,
    "rels_thieu": _ca_rels_thieu,
    "zip_hong": _ca_zip_hong,
    "zlib_hong": _ca_zlib_hong,
    "csv_khong_utf8": _ca_l1_khong_utf8,
    "csv_co_nul": _ca_l1_co_nul,
    "csv_truong_qua_dai": _ca_l1_truong_qua_dai,
}


@pytest.mark.parametrize("ten_ca", list(_CA_HONG))
def test_DT1BT_R1_04_tep_hong_mot_dong_khong_traceback(tmp_path, ten_ca):
    xlsx, l1 = _CA_HONG[ten_ca](tmp_path)
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 1, (ten_ca, kq.returncode, kq.stdout, kq.stderr)
    assert "Traceback" not in kq.stderr, f"[{ten_ca}] có Traceback:\n{kq.stderr}"
    assert kq.stderr.startswith("LOI"), f"[{ten_ca}] câu lỗi ⛔ bắt đầu bằng 'LOI': {kq.stderr!r}"
    # MỘT dòng (1 ký tự xuống dòng ở cuối, ⛔ chồng ngăn xếp nhiều dòng)
    assert kq.stderr.strip().count("\n") == 0, f"[{ten_ca}] lỗi NHIỀU dòng:\n{kq.stderr}"


def test_DT1BT_R1_04_unicode_khong_lo_byte_vi_tri(tmp_path):
    """`UnicodeDecodeError` ⛔ in byte (vd `0xf4`) / vị trí — chỉ câu chữa (Sheets › Tải xuống › CSV)."""
    xlsx, l1 = _ca_l1_khong_utf8(tmp_path)
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 1, (kq.returncode, kq.stdout, kq.stderr)
    low = kq.stderr.lower()
    assert "0x" not in low and "position" not in low and "vị trí" not in low and "byte" not in low, kq.stderr
    assert "utf-8" in low, kq.stderr                 # câu chữa CÓ nhắc UTF-8


# DT1BT-R1-01: đọc được rels đích TUYỆT ĐỐI lẫn TƯƠNG ĐỐI.
@pytest.mark.parametrize("tuyet_doi", [False, True], ids=["rels_tuong_doi", "rels_tuyet_doi"])
def test_DT1BT_R1_01_rels_tuyet_doi_va_tuong_doi(tmp_path, tuyet_doi):
    """`Target="/xl/worksheets/sheet2.xml"` (openpyxl) ⇒ xưa nối thành `xl/xl/…` ⇒ exit 1. Nay đọc được
    CẢ HAI dạng ⇒ exit 0 + 3 hàng SO đúng."""
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong(), rels_ledge_tuyet_doi=tuyet_doi)
    l1 = _lam_l1(tmp_path / "l1.csv", [list(TIEU_DE.values())])
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (tuyet_doi, kq.returncode, kq.stdout, kq.stderr)
    so = [r for r in _doc_csv(ra) if r[0] == "SO"]
    assert [r[1] for r in so] == ["10", "11", "12"], so


def test_DT1BT_R1_01_chuan_dich_rels_don_vi():
    mod = _tool()
    assert mod._chuan_dich_rels("worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"   # tương đối ⇒ nối xl/
    assert mod._chuan_dich_rels("/xl/worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"  # tuyệt đối ⇒ bỏ /
    assert mod._chuan_dich_rels("/xl/sharedStrings.xml") == "xl/sharedStrings.xml"


# DT1BT-R1-02: in SỐ ĐẾM chẩn đoán "hàng có ≥1 ô khoá / hàng 0 ô khoá" (CHỈ số — ⛔ giá trị).
def test_DT1BT_R1_02_in_so_dem_hang_khoa_khong_lo_gia_tri(tmp_path):
    """Hàng 11 CHỈ có ô ở cột NGOÀI 5 khoá (Email, công thức) ⇒ thành 'hàng dữ liệu' nhưng 0 ô khoá.
    Công cụ in `SO: 1 / 1` (≥1 khoá / 0 khoá) — số, ⛔ giá trị `FORMULA_SECRET`."""
    g = dict(_TD_LEDGE)
    g.update({(10, 1): "SYN10", (10, 3): "VND", (10, 4): "1", (10, 5): "2", (10, 6): "1121"})
    g[(11, 20)] = ("str", "FORMULA_SECRET")           # chỉ ô ở cột 20 (Email, ngoài khoá) — 0 ô khoá
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", g)
    l1 = _lam_l1(tmp_path / "l1.csv", [list(TIEU_DE.values()), ["x", "1", "2", "1121", "VND"]])
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout, kq.stderr)
    assert "hàng có ≥1 ô khoá / hàng 0 ô khoá — SO: 1 / 1" in kq.stdout, kq.stdout
    assert "L1: 1 / 0" in kq.stdout, kq.stdout
    assert "FORMULA_SECRET" not in (kq.stdout + kq.stderr)    # chỉ SỐ ĐẾM, ⛔ giá trị ô


# DT1BT-R1-05: ghim M8 (tiêu đề hai hàng) · M12 (đường ra là thư mục) · M16 (khoảng trắng tiêu đề L1).
def test_DT1BT_R1_05_M8_tieu_de_rai_hai_hang(tmp_path):
    """Tiêu đề rải HÀNG 7 (Số CT · Đơn vị) + HÀNG 8 (PS Nợ · PS Có · Tài khoản) ⇒ `hang_tieu_de` = 8.
    Dữ liệu từ hàng 10. M8 (`max`→`min`) ⇒ hàng 8 (còn tiêu đề) thành 'dữ liệu' ⇒ ĐỎ."""
    g = {(7, 1): "Số chứng từ", (7, 3): "Đơn vị tiền tệ",
         (8, 4): "PS Nợ", (8, 5): "PS Có", (8, 6): "Tài khoản"}
    g.update({(10, 1): "SYN10", (10, 3): "VND", (10, 4): "1", (10, 5): "2", (10, 6): "1121"})
    g.update({(11, 1): "SYN11", (11, 3): "USD", (11, 4): "0", (11, 5): "5", (11, 6): "3311"})
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", g)
    hang = _tool().doc_xlsx_ledge(xlsx)
    assert [h["dong"] for h in hang] == [10, 11], hang      # hàng 8 ⛔ thành dữ liệu
    assert all(h["dong"] != 8 for h in hang)


def test_DT1BT_R1_05_M12_ra_la_thu_muc_ma_2(tmp_path):
    """`--ra` trỏ THƯ MỤC ⇒ exit 2 'TỪ CHỐI'. M12 (bỏ chốt 'đường ra là thư mục') ⇒ sập khi ghi ⇒ ĐỎ."""
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    l1 = _lam_l1(tmp_path / "l1.csv", _l1_hinh_sheets())
    thu_muc = tmp_path / "ra_dir"
    thu_muc.mkdir()
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(thu_muc))
    assert kq.returncode == 2, (kq.returncode, kq.stdout, kq.stderr)
    assert "TỪ CHỐI" in kq.stderr and "Traceback" not in kq.stderr, kq.stderr


def test_DT1BT_R1_05_M16_l1_tieu_de_co_khoang_trang(tmp_path):
    """Tiêu đề L1 có khoảng trắng thừa ('  Tài khoản ') vẫn KHỚP (`.strip()` tiêu đề). M16 (bỏ strip) ⇒
    ⛔ thấy cột ⇒ exit 1 ⇒ ĐỎ."""
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong())
    hdr = [" Số chứng từ ", "Diễn giải", "Đơn vị tiền tệ  ", "PS Nợ", "PS Có", "  Tài khoản"]
    l1 = _lam_l1(tmp_path / "l1.csv", [hdr, ["4.36619E+15", "mô tả", "VND", "2730128", "0", "1121"]])
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (kq.returncode, kq.stdout, kq.stderr)
    l1r = [r for r in _doc_csv(ra) if r[0] == "L1"]
    assert len(l1r) == 1 and l1r[0][5] == "1121", l1r      # cột 'Tài khoản' khớp dù có khoảng trắng


# DT1BT-R1-09: dữ liệu thô owner đặt ở `Input_Raw/` phải BỊ `.gitignore` (cùng tinh thần `hien_vat/`).
def test_DT1BT_R1_09_input_raw_bi_gitignore():
    """`git check-ignore` cho một đường mẫu: `Input_Raw/[Master] ITL_Ledge_raw.xlsx` + CSV bất kỳ phải
    ignored (⛔ một `git add -A` đưa sổ thật lên git); `hien_vat/` vẫn ignored."""
    assert mod_ignore(GOC / "Input_Raw" / "[Master] ITL_Ledge_raw.xlsx"), "Input_Raw/xlsx ⛔ bị gitignore"
    assert mod_ignore(GOC / "Input_Raw" / "bat_ky.csv"), "Input_Raw/*.csv ⛔ bị gitignore"
    assert mod_ignore(GOC / "hien_vat" / "khoa_dt1b.csv"), "hien_vat/ ⛔ còn bị gitignore"


# ╔═══════════════════════════════════════════════════════════════════════════════════════════════╗
# ║  VÒNG SỬA SAU R2 (KQ-130) — DT1BT-R2-02 (rels dạng ngoài) · R2-03 (zlib luồng nén)              ║
# ╚═══════════════════════════════════════════════════════════════════════════════════════════════╝

# DT1BT-R2-02: `_chuan_dich_rels` phải chịu được các dạng NGOÀI "tuyệt đối" / "tương đối":
#   · `xl/worksheets/…` đã mang tiền tố gốc-zip ⇒ ⛔ nối thành `xl/xl/…` (bản cũ đọc được ⇒ hồi quy);
#   · `./` · `../xl/` ⇒ chuẩn hoá bằng posixpath.normpath (giữ trong gốc zip);
#   · `%20` trong tên ⇒ urllib.parse.unquote.
def test_DT1BT_R2_02_chuan_dich_rels_dang_ngoai():
    mod = _tool()
    # đã có tiền tố xl/ (vài bộ sinh) ⇒ ⛔ nối thành xl/xl/
    assert mod._chuan_dich_rels("xl/worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"
    assert mod._chuan_dich_rels("xl/sharedStrings.xml") == "xl/sharedStrings.xml"
    # ./ và ../ ⇒ normpath gộp, kết quả vẫn trong gốc zip
    assert mod._chuan_dich_rels("./worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"
    assert mod._chuan_dich_rels("../xl/worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"
    # %20 ⇒ unquote (tên tệp worksheet có khoảng trắng)
    assert mod._chuan_dich_rels("worksheets/sheet%201.xml") == "xl/worksheets/sheet 1.xml"
    assert mod._chuan_dich_rels("/xl/worksheets/sheet%201.xml") == "xl/worksheets/sheet 1.xml"
    # hai dạng cũ VẪN đúng (hồi quy ngược)
    assert mod._chuan_dich_rels("worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"
    assert mod._chuan_dich_rels("/xl/worksheets/sheet1.xml") == "xl/worksheets/sheet1.xml"


@pytest.mark.parametrize("tgt", [
    "xl/worksheets/sheet2.xml",       # đã có tiền tố xl/ ⇒ ⛔ nối thành xl/xl/ (bản cũ đọc được)
    "./worksheets/sheet2.xml",        # ./ ⇒ normpath
    "../xl/worksheets/sheet2.xml",    # ../ ⇒ normpath
], ids=["xl_tien_to", "cham", "cham_cham"])
def test_DT1BT_R2_02_rels_dang_ngoai_doc_duoc(tmp_path, tgt):
    """Đích rels của sheet `ITL Ledge` viết ở dạng NGOÀI hai loại cũ ⇒ công cụ vẫn đọc đúng (exit 0, 3 hàng
    SO 10·11·12). ĐỎ-trước: bản cũ nối `xl/` cứng ⇒ `xl/xl/…`/`xl/./…`/`xl/../…` ⇒ KeyError ⇒ exit 1."""
    xlsx = _lam_xlsx(tmp_path / "ledge.xlsx", _ledge_ba_dong(), rels_ledge_tgt=tgt)
    l1 = _lam_l1(tmp_path / "l1.csv", [list(TIEU_DE.values())])
    ra = tmp_path / "khoa.csv"
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(ra))
    assert kq.returncode == 0, (tgt, kq.returncode, kq.stdout, kq.stderr)
    so = [r for r in _doc_csv(ra) if r[0] == "SO"]
    assert [r[1] for r in so] == ["10", "11", "12"], so


# DT1BT-R2-03: lật byte luồng NÉN của worksheet ⇒ `zlib.error`/CRC hỏng lúc ĐỌC ⇒ MỘT dòng LOI, exit 1,
# ⛔ Traceback, ⛔ giá trị ô. (Lớp lỗi lặp của R1-04 — `BadZipFile` chỉ bắt lúc MỞ, ⛔ lúc đọc.)
def test_DT1BT_R2_03_zlib_luong_nen_mot_dong(tmp_path):
    xlsx, l1 = _ca_zlib_hong(tmp_path)
    kq = _chay("--xlsx", str(xlsx), "--l1", str(l1), "--ra", str(tmp_path / "k.csv"))
    assert kq.returncode == 1, (kq.returncode, kq.stdout, kq.stderr)
    assert "Traceback" not in kq.stderr, kq.stderr
    assert kq.stderr.startswith("LOI"), kq.stderr
    assert kq.stderr.strip().count("\n") == 0, f"lỗi NHIỀU dòng:\n{kq.stderr}"
    assert SENTINEL not in (kq.stdout + kq.stderr), "giá trị ô LỌT ra màn"
    assert not (tmp_path / "k.csv").exists()
