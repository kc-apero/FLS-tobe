# -*- coding: utf-8 -*-
"""XUẤT BẢN ĐỌC KHOÁ cho DT1b — đọc 5 cột khoá của `ITL Ledge` (.xlsx) + `Transaction Mapping L1`
(.csv owner tải từ Google Sheets) ⇒ CSV định dạng đóng mà `tools/phan_loai_ly_do.py --khoa` ăn được.

ISP 3.1.2 · Step 5 · DT1b · phiếu `WO-127` / `BG-128`. Công cụ RIÊNG (⛔ nhập chung tool phân loại).

⭐ Vì sao có tệp này. `phan_loai_ly_do.py` nhận ĐẦU VÀO là một CSV 7 cột
   `bang,dong,so_ct,ps_no,ps_co,tk,tien_te` (HAI bảng `SO`+`L1` xếp chồng, giá trị THÔ). Nhưng khoá
   THẬT chỉ có trên máy owner (O10 · `B-DATA-2`): `Input_Raw/[Master] ITL_Ledge_raw.xlsx` (sổ `ITL
   Ledge`) + tab `Transaction Mapping L1` của RAW `1md85t…` (`fls/oracle/nguon.py` `BAN_SAO_RAW`). Tệp
   này là cầu: owner chạy nó trên máy để sinh CSV ấy, rồi chạy `phan_loai_ly_do.py` trên CSV đó.

⛔ CHỈ thư viện chuẩn — `zipfile` + `xml.etree.ElementTree` (⛔ `openpyxl`, ⛔ cài gói mới): owner chạy
   trong `.venv` của repo, ⛔ chắc có `openpyxl`; và một gói đọc xlsx thừa là một mặt phá mới.

⭐ ĐỌC .xlsx bằng tay (OOXML / SpreadsheetML):
   · `xl/workbook.xml` khai danh sách sheet kèm `r:id`; `xl/_rels/workbook.xml.rels` nối `r:id` →
     đường tệp worksheet. ⇒ TÌM sheet THEO TÊN `ITL Ledge` (⛔ "sheet đầu" — tệp owner có nhiều sheet).
   · Ô chuỗi: `t="s"` trỏ chỉ mục `xl/sharedStrings.xml`; `t="inlineStr"` mang `<is><t>` tại chỗ;
     `t="str"` (kết quả công thức) mang `<v>`. Ô SỐ: ⛔ `t` (hoặc `t="n"`) ⇒ `<v>` là chuỗi số.
   · Cột theo TÊN TIÊU ĐỀ nguyên văn (`fls/canon/spec.py`), TÌM trong ~12 hàng đầu — ⛔ gõ cứng chữ
     cái cột (khuôn `ITL Ledge` 64 cột, tiêu đề ở hàng 7+8; CLAUDE.md Đ4). `dong` = SỐ HÀNG EXCEL
     (thuộc tính `r` của `<row>`), CÙNG hệ với `dong_sheet` của ảnh 26/08 (hàng dữ liệu 10…9976).

⭐ Số CT dài XUẤT NGUYÊN chuỗi `<v>` — ⛔ qua `float`. Lý do (chứng minh bằng bài nối
   `test_AC4_*`): `float("4366190000000000")` tuy đúng trị nhưng `str()` của số lớn có thể sinh dạng
   khoa học / mất chữ số; giữ NGUYÊN `<v>` thì `canon_ref` của `phan_loai_ly_do.py` gỡ về khoá chuẩn.
   Phía L1 (CSV Google Sheets tải về) thì Số CT dài LẠI hiện dạng khoa học `4.36619E+15` — `canon_ref`
   gỡ cả hai dạng về CÙNG một khoá `4366190000000000` (y bài `tests/adapters/test_pm_join.py:58`). ⇒
   công cụ này ⛔ chuẩn hoá gì — chỉ xuất THÔ, để `phan_loai_ly_do.py` giữ một bản khai chuẩn hoá duy nhất.

⛔ Riêng tư (CLAUDE.md §Riêng tư & tiền thật · WO-127):
   · ⛔ IN giá trị ô — chỉ in SỐ ĐẾM (số hàng SO · L1, số hàng có ≥1 ô khoá / 0 ô khoá `DT1BT-R1-02`,
     số ô rỗng mỗi cột). Giá trị thô chỉ sống trong bộ nhớ và trong tệp ra.
   · Đường ra mặc định `hien_vat/khoa_dt1b.csv` (`.gitignore:17` — "để gửi đi" nên bị bỏ qua). TỪ CHỐI
     ghi vào chỗ TRONG repo mà ⛔ bị `.gitignore` (một `git add -A` là Số CT + tiền thật lên lịch sử) —
     y luật R8 của `phan_loai_ly_do.py` (`_trong_repo_khong_ignore`), fail-ĐÓNG: ⛔ chứng minh được
     `.gitignore` che ⇒ coi như nguy (Đ5 — phép ⛔ đo được là ĐỎ).
   · ⛔ cột `Diễn giải`, ⛔ `Email Address` — chỉ 5 cột khoá. (Cột `Diễn giải`/email có trong sổ
     nhưng công cụ ⛔ bao giờ đọc tới — nó tìm ĐÚNG 5 tên tiêu đề.)

Chạy (từ gốc repo; owner: Windows PowerShell, xem `docs/ITL/03_Dev/isp-3.1/HUONG_DAN_NHAN_THAT_DT1b.md`):
  python tools/xuat_khoa_dt1b.py --xlsx <đường ITL_Ledge_raw.xlsx> --l1 <đường l1.csv>
  python tools/xuat_khoa_dt1b.py --xlsx … --l1 … --ra hien_vat/khoa_dt1b.csv   # (mặc định đã là đó)
Mã thoát: 0 xuất xong · 1 lỗi ĐỌC/ĐỊNH DẠNG (sheet ⛔ thấy · thiếu cột · xlsx hỏng · CSV thiếu cột) ·
          2 sai cách gọi (đầu vào ⛔ thấy · đường ra là thư mục · đường ra trong repo mà ⛔ .gitignore).
"""
from __future__ import annotations

import argparse
import csv
import posixpath
import subprocess
import sys
import zipfile
import zlib
from pathlib import Path
from urllib.parse import unquote
from xml.etree import ElementTree as ET

GOC = Path(__file__).resolve().parents[1]
RA_MAC_DINH = GOC / "hien_vat" / "khoa_dt1b.csv"

# Tên tiêu đề nguyên văn — `fls/canon/spec.py` `_TEN` (BASE, nguồn `Transaction Original`). ⛔ gõ lại
# bằng tay ở nơi khác: 5 chuỗi này PHẢI trùng tuyệt đối với tiêu đề trong sổ, nên chép đúng một lần.
TIEU_DE = {
    "so_ct": "Số chứng từ",
    "ps_no": "PS Nợ",
    "ps_co": "PS Có",
    "tk": "Tài khoản",
    "tien_te": "Đơn vị tiền tệ",
}
COT_RA = ("bang", "dong", "so_ct", "ps_no", "ps_co", "tk", "tien_te")   # định dạng đóng của phan_loai_ly_do
COT_KHOA = ("so_ct", "ps_no", "ps_co", "tk", "tien_te")
HANG_TIM_TIEU_DE = 12          # tiêu đề `ITL Ledge` ở hàng 7+8 ⇒ quét 12 hàng đầu là đủ, ⛔ chạm dữ liệu

NS_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
NS_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_PKG = "http://schemas.openxmlformats.org/package/2006/relationships"


class LoiDoc(ValueError):
    """Lỗi ĐỌC/ĐỊNH DẠNG đầu vào. Câu lỗi chỉ mang TÊN CỘT / tên sheet / số hàng — ⛔ giá trị ô."""


# ═════════════════════════════════════════════════════════════════════════ đọc .xlsx bằng tay
def _cot_tu_ref(ref: str) -> int:
    """`"A1"` → 0 · `"B7"` → 1 · `"AA3"` → 26. Chỉ lấy phần chữ cái ở đầu ref ô."""
    i = 0
    while i < len(ref) and ref[i].isalpha():
        i += 1
    chu = ref[:i].upper()
    n = 0
    for c in chu:
        n = n * 26 + (ord(c) - ord("A") + 1)
    return n - 1


def _q(ten: str) -> str:
    return f"{{{NS_MAIN}}}{ten}"


def _text_si(si: ET.Element) -> str:
    """Gộp MỌI `<t>` trong một `<si>` / `<is>` (chuỗi giàu định dạng tách thành nhiều `<r><t>`)."""
    return "".join(t.text or "" for t in si.iter(_q("t")))


def _parse_xml(data: bytes, mo_ta: str) -> ET.Element:
    """`ET.fromstring` CÓ BỌC: XML hỏng ⇒ `LoiDoc` MỘT DÒNG (`DT1BT-R1-04`). `ParseError` để tràn ra
    sẽ in Traceback mà owner (⛔ lập trình viên) ⛔ đọc được; `from None` cắt chuỗi ngoại lệ (⛔ byte dữ liệu)."""
    try:
        return ET.fromstring(data)
    except ET.ParseError:
        raise LoiDoc(f"{mo_ta}: XML hỏng — ⛔ phải tệp .xlsx hợp lệ") from None


def _doc_phan_zip(z: zipfile.ZipFile, ten: str) -> bytes:
    """`z.read(ten)` CÓ BỌC luồng giải nén. `DT1BT-R2-03` (lớp lỗi lặp của `R1-04`): `zipfile.BadZipFile`
    chỉ bị bắt lúc MỞ archive, ⛔ lúc ĐỌC từng phần — một phần có local header đúng nhưng luồng nén / CRC
    hỏng ⇒ `zlib.error` (luồng deflate hỏng) · `BadZipFile` ('Bad CRC-32') · `EOFError` (cụt) ⇒ nếu để
    tràn ra thì owner (⛔ lập trình viên) thấy Traceback. ⇒ gói CẢ cây lỗi giải nén thành `LoiDoc` MỘT
    DÒNG (⛔ byte, ⛔ giá trị ô). `KeyError` (⛔ có phần ấy) để nơi gọi tự xử — mỗi phần một câu lỗi riêng."""
    try:
        return z.read(ten)
    except (zipfile.BadZipFile, zlib.error, EOFError):
        raise LoiDoc(f"{ten}: luồng nén hỏng — ⛔ phải tệp .xlsx hợp lệ (tải/chép lại tệp)") from None


def _chuan_dich_rels(tgt: str) -> str:
    """Chuẩn hoá đích `Target` của rels về đường trong zip (gốc = thư mục chứa archive).
    · TUYỆT ĐỐI `"/xl/worksheets/sheet1.xml"` (openpyxl & một số thư viện/dịch vụ sinh) ⇒ đã là đường
      gốc zip ⇒ CHỈ bỏ `/` đầu.
    · TƯƠNG ĐỐI `"worksheets/sheet1.xml"` (dạng Excel) ⇒ tương đối với thư mục `xl/` của `workbook.xml`
      ⇒ nối `xl/`.
    `DT1BT-R1-01`: bản cũ nối `xl/` cho CẢ hai dạng ⇒ tuyệt đối thành `xl/xl/worksheets/sheet1.xml`
    ⇒ `exit 1` trên tệp do openpyxl sinh (bước (c) của owner chết ngay nếu `[Master] …xlsx` ⛔ do Excel ghi).

    `DT1BT-R2-02`: chịu được các dạng NGOÀI hai loại trên (vài bộ sinh ⛔ theo OPC chuẩn):
    · `%20`/`%xx` trong tên tệp ⇒ `unquote` (tên zip là chuỗi nguyên văn, ⛔ phần trăm-mã).
    · đã mang tiền tố `xl/` ⇒ ⛔ nối lần nữa thành `xl/xl/…` (bản cũ đọc được ⇒ hồi quy).
    · `./` · `../xl/…` ⇒ `posixpath.normpath` gộp; kết quả PHẢI còn trong gốc zip (⛔ thoát bằng `..`),
      ⛔ thì `LoiDoc` (một dòng, ⛔ lộ giá trị). Chuẩn hoá áp cho CẢ dạng tuyệt đối (gộp `//`, `.`)."""
    tgt = unquote(tgt.strip())
    if tgt.startswith("/"):
        duong = tgt.lstrip("/")                      # tuyệt đối ⇒ đã gốc zip
    elif tgt == "xl" or tgt.startswith("xl/"):
        duong = tgt                                  # đã mang tiền tố gốc-zip ⇒ ⛔ nối lần nữa
    else:
        duong = "xl/" + tgt                          # tương đối thư mục workbook.xml ⇒ nối xl/
    duong = posixpath.normpath(duong)                # gộp ./ ../ //
    if duong == ".." or duong.startswith("../") or duong.startswith("/"):
        raise LoiDoc(f"rels: đích {tgt!r} thoát khỏi gốc gói — ⛔ phải tệp .xlsx hợp lệ")
    return duong


def _tim_duong_sheet(z: zipfile.ZipFile, ten_sheet: str) -> str:
    """Tìm đường tệp worksheet của sheet TÊN `ten_sheet`, qua `workbook.xml` + rels. ⛔ "sheet đầu"."""
    try:
        raw_wb = _doc_phan_zip(z, "xl/workbook.xml")
    except KeyError:
        raise LoiDoc("xlsx ⛔ có xl/workbook.xml — ⛔ phải tệp .xlsx hợp lệ") from None
    wb = _parse_xml(raw_wb, "xl/workbook.xml")
    rid = None
    for s in wb.iter(_q("sheet")):
        if (s.get("name") or "").strip() == ten_sheet:
            rid = s.get(f"{{{NS_REL}}}id")
            break
    if rid is None:
        ten_co = [(s.get("name") or "").strip() for s in wb.iter(_q("sheet"))]
        raise LoiDoc(f"⛔ thấy sheet tên {ten_sheet!r}; sheet có: {ten_co}")
    try:
        raw_rels = _doc_phan_zip(z, "xl/_rels/workbook.xml.rels")
    except KeyError:
        raise LoiDoc("xlsx ⛔ có xl/_rels/workbook.xml.rels — ⛔ phải tệp .xlsx hợp lệ") from None
    rels = _parse_xml(raw_rels, "xl/_rels/workbook.xml.rels")
    for r in rels.iter(f"{{{NS_PKG}}}Relationship"):
        if r.get("Id") == rid:
            return _chuan_dich_rels(r.get("Target") or "")
    raise LoiDoc(f"rels ⛔ có quan hệ {rid!r} cho sheet {ten_sheet!r}")


def _shared_strings(z: zipfile.ZipFile) -> list[str]:
    try:
        raw = _doc_phan_zip(z, "xl/sharedStrings.xml")
    except KeyError:
        return []
    sst = _parse_xml(raw, "xl/sharedStrings.xml")
    return [_text_si(si) for si in sst.findall(_q("si"))]


def _gia_tri_o(c: ET.Element, shared: list[str]) -> str:
    """Giá trị THÔ của một ô, đúng như ô hiện — ⛔ ép kiểu, ⛔ qua float. Ô trống ⇒ `""`."""
    t = c.get("t")
    if t == "inlineStr":
        isn = c.find(_q("is"))
        return _text_si(isn) if isn is not None else ""
    v = c.find(_q("v"))
    if t == "s":                                    # chỉ mục sharedStrings
        if v is None or not (v.text or "").strip().lstrip("-").isdigit():
            return ""
        idx = int(v.text)
        return shared[idx] if 0 <= idx < len(shared) else ""
    # t in {None, "n", "str", "b", "e", …}: `<v>` là chuỗi số / chuỗi công thức / "0"/"1" / mã lỗi
    return (v.text or "") if v is not None else ""


def doc_xlsx_ledge(duong: Path, ten_sheet: str = "ITL Ledge") -> list[dict]:
    """Đọc sheet `ITL Ledge` → danh sách `{"dong": <hàng Excel>, <5 cột khoá>: <thô>}`, MỌI hàng dữ liệu.

    Cột theo TÊN TIÊU ĐỀ (12 hàng đầu); `dong` = thuộc tính `r` của `<row>`. Thiếu tên tiêu đề ⇒ `LoiDoc`.
    """
    try:
        z = zipfile.ZipFile(duong)
    except zipfile.BadZipFile:
        raise LoiDoc(f"{duong.name}: ⛔ phải tệp .xlsx hợp lệ (⛔ giải nén được)") from None
    with z:
        duong_sheet = _tim_duong_sheet(z, ten_sheet)
        shared = _shared_strings(z)
        try:
            raw_ws = _doc_phan_zip(z, duong_sheet)
        except KeyError:
            raise LoiDoc(f"xlsx ⛔ có tệp worksheet {duong_sheet!r}") from None
        ws = _parse_xml(raw_ws, "worksheet")
        rows = ws.find(_q("sheetData"))
        if rows is None:
            raise LoiDoc(f"sheet {ten_sheet!r} ⛔ có <sheetData>")

        # ① gom 12 hàng đầu để tìm tiêu đề; đồng thời giữ mọi hàng để xuất.
        hang_o: list[tuple[int, dict[int, str]]] = []
        for row in rows.findall(_q("row")):
            try:
                rn = int(row.get("r"))
            except (TypeError, ValueError):
                continue
            o: dict[int, str] = {}
            for c in row.findall(_q("c")):
                ref = c.get("r")
                if not ref:
                    continue
                o[_cot_tu_ref(ref)] = _gia_tri_o(c, shared)
            hang_o.append((rn, o))

        # ② cột theo tên: mỗi tên tiêu đề → ĐÚNG MỘT chỉ số cột, tìm trong 12 hàng đầu (theo số hàng Excel).
        #    Tiêu đề `ITL Ledge` rải ở hàng 7+8 ⇒ `hang_tieu_de` = hàng LỚN NHẤT có một tiêu đề khoá.
        cot: dict[str, int] = {}
        hang_dau = sorted(hang_o, key=lambda x: x[0])[:HANG_TIM_TIEU_DE]
        hang_tieu_de = 0
        for khoa, ten in TIEU_DE.items():
            thay = sorted({(rn, ci) for rn, o in hang_dau for ci, v in o.items() if (v or "").strip() == ten})
            cols = sorted({ci for _, ci in thay})
            if len(cols) == 0:
                raise LoiDoc(f"sheet {ten_sheet!r}: ⛔ thấy tiêu đề cột {ten!r} trong {HANG_TIM_TIEU_DE} hàng đầu")
            if len(cols) > 1:
                raise LoiDoc(f"sheet {ten_sheet!r}: tiêu đề {ten!r} xuất hiện ở {len(cols)} cột — ⛔ phân định được")
            cot[khoa] = cols[0]
            hang_tieu_de = max(hang_tieu_de, max(rn for rn, _ in thay))

        # ③ hàng dữ liệu = mọi hàng Excel SAU hàng tiêu đề mà có ≥1 ô ⛔ rỗng (bỏ hàng trống hẳn, vd hàng 9).
        ra: list[dict] = []
        for rn, o in sorted(hang_o, key=lambda x: x[0]):
            if rn <= hang_tieu_de:
                continue
            if not any((v or "").strip() for v in o.values()):
                continue
            ra.append({"dong": rn, **{k: o.get(cot[k], "") for k in COT_KHOA}})
        return ra


# ═════════════════════════════════════════════════════════════════════════ đọc .csv `Transaction Mapping L1`
def doc_l1_csv(duong: Path) -> list[dict]:
    """Đọc CSV tab `Transaction Mapping L1` (Google Sheets tải về) → `{"dong": <số hàng sheet>, 5 cột}`.

    Cột theo TÊN TIÊU ĐỀ (12 hàng đầu); `dong` = số hàng CSV = số hàng sheet (CHỈ để định danh trong tệp).
    """
    # Ký tự NUL ⇒ TỪ CHỐI MINH BẠCH: `csv.reader` (Python 3.13) NUỐT NUL vào trong trường thay vì báo lỗi
    # ⇒ một tệp hỏng lọt qua im lặng (Đ5 — phép ⛔ chứng minh sạch là ĐỎ). `DT1BT-R1-03`/`-04`: một dòng, ⛔ byte.
    if b"\x00" in duong.read_bytes():
        raise LoiDoc(f"{duong.name}: CSV có ký tự NUL — ⛔ phải CSV văn bản sạch, tải lại từ Sheets") from None
    try:
        with duong.open(encoding="utf-8-sig", newline="") as f:
            hang = list(csv.reader(f))
    except UnicodeDecodeError:
        # `DT1BT-R1-04`: ⛔ in `e.object`/byte/vị trí — chỉ câu chữa. Một tệp "CSV" Excel Windows có thể
        # là cp1258/BOM lạ ⇒ tải lại đúng CSV UTF-8 từ Sheets.
        raise LoiDoc(f"{duong.name}: CSV ⛔ phải UTF-8 — ở Google Sheets dùng Tệp › Tải xuống › "
                     f"Giá trị phân tách bằng dấu phẩy (.csv), ⛔ xuất từ Excel sang mã khác") from None
    except csv.Error:
        # trường > 131 072 ký tự, hay ô mang ký tự NUL ⇒ `_csv.Error`. Một dòng, ⛔ giá trị ô.
        raise LoiDoc(f"{duong.name}: CSV hỏng (trường quá dài hoặc có ký tự NUL) — tải lại từ Sheets") from None
    if not hang:
        raise LoiDoc(f"{duong.name}: CSV rỗng")
    cot: dict[str, int] = {}
    hang_tieu_de = -1
    for khoa, ten in TIEU_DE.items():
        thay = None
        for i, h in enumerate(hang[:HANG_TIM_TIEU_DE]):
            vi = [j for j, v in enumerate(h) if (v or "").strip() == ten]
            if len(vi) > 1:
                raise LoiDoc(f"L1 CSV: tiêu đề {ten!r} xuất hiện {len(vi)} lần ở hàng {i + 1} — ⛔ phân định được")
            if vi:
                thay = (i, vi[0])
                break
        if thay is None:
            raise LoiDoc(f"L1 CSV: ⛔ thấy tiêu đề cột {ten!r} trong {HANG_TIM_TIEU_DE} hàng đầu")
        cot[khoa] = thay[1]
        hang_tieu_de = max(hang_tieu_de, thay[0])

    ra: list[dict] = []
    for i, h in enumerate(hang):
        if i <= hang_tieu_de:
            continue
        if not any((v or "").strip() for v in h):
            continue
        ra.append({"dong": i + 1, **{k: (h[cot[k]] if cot[k] < len(h) else "") for k in COT_KHOA}})
    return ra


# ═════════════════════════════════════════════════════════════════════════ ghi + từ chối đường nguy
def _trong_repo_khong_ignore(duong: Path) -> bool:
    """R8 (y `phan_loai_ly_do.py`) — True nếu `duong` TRONG repo mà CHƯA chứng minh được đã bị `.gitignore`
    (⇒ TỪ CHỐI ghi). `git check-ignore -q` trả 0 khi BỊ bỏ qua (an toàn). git ⛔ chạy được ⇒ FAIL-ĐÓNG."""
    try:
        duong.resolve().relative_to(GOC)
    except (ValueError, OSError):
        return False                 # ⛔ trong repo ⇒ chốt này ⛔ lo
    try:
        r = subprocess.run(["git", "-C", str(GOC), "check-ignore", "-q", str(duong.resolve())])
    except OSError:
        return True                  # TRONG repo mà git ⛔ chạy được ⇒ ⛔ chứng minh an toàn ⇒ từ chối
    return r.returncode != 0


def ghi_csv(duong_ra: Path, so: list[dict], l1: list[dict]) -> None:
    duong_ra.parent.mkdir(parents=True, exist_ok=True)
    with duong_ra.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(COT_RA)
        for r in so:
            w.writerow(["SO", r["dong"], *[r[k] for k in COT_KHOA]])
        for r in l1:
            w.writerow(["L1", r["dong"], *[r[k] for k in COT_KHOA]])


def _dem_rong(hang: list[dict]) -> dict[str, int]:
    return {k: sum(1 for r in hang if not (r[k] or "").strip()) for k in COT_KHOA}


def _dem_khoa(hang: list[dict]) -> tuple[int, int]:
    """(số hàng có ≥1 trong 5 ô khoá ⛔ rỗng, số hàng 0 ô khoá). CHỈ SỐ ĐẾM — ⛔ giá trị ô.

    `DT1BT-R1-02`: định nghĩa "hàng dữ liệu" GIỮ NGUYÊN (≥1 ô BẤT KỲ ⛔ rỗng), nhưng in thêm số này để
    owner/orchestrator thấy K11 lệch vì đâu *không cần* mở tệp: nếu `K11` ĐỎ ở bước (d) mà "hàng 0 khoá" > 0
    thì đuôi sổ mang ô công thức ở cột NGOÀI 5 khoá đã bị đếm thành "hàng dữ liệu" (Đ4 — số nói nó đếm gì)."""
    co = sum(1 for r in hang if any((r[k] or "").strip() for k in COT_KHOA))
    return co, len(hang) - co


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="XUẤT bản đọc khoá cho DT1b (ITL Ledge .xlsx + Transaction Mapping L1 .csv) → CSV 7 cột.")
    ap.add_argument("--xlsx", type=Path, required=True, help="đường tới [Master] ITL_Ledge_raw.xlsx")
    ap.add_argument("--l1", type=Path, required=True, help="đường tới CSV tab Transaction Mapping L1 (tải từ Sheets)")
    ap.add_argument("--ra", type=Path, default=RA_MAC_DINH, help="đường ra (mặc định hien_vat/khoa_dt1b.csv)")
    ap.add_argument("--sheet", default="ITL Ledge", help="tên sheet sổ (mặc định 'ITL Ledge')")
    a = ap.parse_args(argv)

    for nhan, p in (("--xlsx", a.xlsx), ("--l1", a.l1)):
        if not p.is_file():
            print(f"⛔ TỪ CHỐI: ⛔ thấy tệp {nhan} tại {p.resolve()}", file=sys.stderr)
            return 2
    if a.ra.exists() and not a.ra.is_file():
        print(f"⛔ TỪ CHỐI: đường ra {a.ra.resolve()} CÓ nhưng ⛔ phải TỆP thường", file=sys.stderr)
        return 2
    if _trong_repo_khong_ignore(a.ra):
        print(f"⛔ TỪ CHỐI: đường ra mang giá trị THÔ nằm trong repo mà ⛔ bị .gitignore ({a.ra.resolve()}) — "
              f"dùng hien_vat/khoa_dt1b.csv (một `git add -A` là Số CT + tiền thật lên lịch sử)", file=sys.stderr)
        return 2

    try:
        so = doc_xlsx_ledge(a.xlsx, a.sheet)
        l1 = doc_l1_csv(a.l1)
    except LoiDoc as e:
        print(f"LOI đọc: {' '.join(str(e).split())}", file=sys.stderr)   # ⛔ traceback — một dòng, ⛔ giá trị ô
        return 1
    except OSError as e:
        # vd. xlsx đang MỞ trong Excel ⇒ Windows khoá tệp (PermissionError). Một dòng, ⛔ giá trị ô.
        print(f"LOI mở tệp (đóng Excel nếu đang mở .xlsx?): {type(e).__name__}: "
              f"{' '.join(str(e).split())}", file=sys.stderr)
        return 1

    ghi_csv(a.ra, so, l1)
    # ⛔ IN giá trị ô — chỉ SỐ ĐẾM: số hàng mỗi bảng + chẩn đoán hàng-khoá + số ô rỗng mỗi cột.
    rs, rl = _dem_rong(so), _dem_rong(l1)
    ks_co, ks_khong = _dem_khoa(so)
    kl_co, kl_khong = _dem_khoa(l1)
    print(f"✅ xuất {a.ra} — SO {len(so)} hàng · L1 {len(l1)} hàng (7 cột {','.join(COT_RA)})")
    print(f"   hàng có ≥1 ô khoá / hàng 0 ô khoá — SO: {ks_co} / {ks_khong} · L1: {kl_co} / {kl_khong}")
    print("   ô rỗng/cột — SO: " + " · ".join(f"{k} {rs[k]}" for k in COT_KHOA))
    print("   ô rỗng/cột — L1: " + " · ".join(f"{k} {rl[k]}" for k in COT_KHOA))
    print(f"   ▶ bước kế: python tools/phan_loai_ly_do.py --khoa {a.ra}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
