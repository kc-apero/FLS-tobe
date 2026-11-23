# -*- coding: utf-8 -*-
"""⛔⛔ CỔNG CANH **CÚ CẮT DÂY** của `CR#11` task `3` — quét MÃ NGUỒN.

Từ 08/09 đường nạp lấy bản khai ánh xạ cột **từ kho** *(`fls_khai_cot`)*, ⛔
**không** từ dòng 1 của sheet nữa. Đó là cả lý do `QĐ-ITL-105` tồn tại: bỏ
Google Sheets khỏi đường nạp.

⭐⭐ **Vì sao phải là một CỔNG, ⛔ không phải một lời dặn.** Cú cắt này ⛔ không
   để lại dấu vết nào ở đầu ra: **nối lại dây vẫn cho đúng `8.338/8.338`** —
   vì hôm nay kho và dòng 1 **giống hệt nhau** *(kho được trích TỪ dòng 1)*.
   ⇒ Một bài test đo **con số** ⛔ **không bao giờ** bắt được việc nối lại. Chỉ
   có quét **mã nguồn** mới bắt được.

⚠ Và cách nối lại dễ nhất ⛔ không phải cố ý: người sau gặp lỗi *"thiếu bản
  khai trong kho"*, thấy `doc_ban_khai` nằm sẵn trong `import`, gọi nó — ba
  dòng, chạy được ngay, cổng vẫn xanh. ⇒ Cách chữa là **gỡ luôn đường ấy khỏi
  tệp**, rồi canh bằng bài này.
"""
from __future__ import annotations

import ast
import pathlib

GOC = pathlib.Path(__file__).resolve().parents[2]
NAP = GOC / "tools" / "nap_sao_ke.py"

# ⛔ Hai cái tên này là **đường đọc dòng 1 của sheet**.
DUONG_SHEET = frozenset({"doc_ban_khai", "dong_dau"})


def _ten_duoc_goi(cay: ast.AST) -> set[str]:
    ra: set[str] = set()
    for n in ast.walk(cay):
        if isinstance(n, ast.Call):
            f = n.func
            if isinstance(f, ast.Name):
                ra.add(f.id)
            elif isinstance(f, ast.Attribute):
                ra.add(f.attr)
    return ra


def _ten_duoc_import(cay: ast.AST) -> set[str]:
    ra: set[str] = set()
    for n in ast.walk(cay):
        if isinstance(n, (ast.Import, ast.ImportFrom)):
            for a in n.names:
                ra.add(a.asname or a.name.split(".")[0])
    return ra


def _cay():
    return ast.parse(NAP.read_text(encoding="utf-8"), filename=str(NAP))


def test_duong_nap_KHONG_CON_doc_dong_1():
    """⛔ `tools/nap_sao_ke.py` ⛔ không được GỌI đường đọc dòng 1."""
    xau = sorted(_ten_duoc_goi(_cay()) & DUONG_SHEET)
    assert xau == [], (
        "⛔ duong nap goi lai duong doc dong 1: %s. Ban khai phai den tu KHO "
        "(`fls_khai_cot`) — do la ca ly do `QĐ-ITL-105` ton tai. Neu kho thieu "
        "ban khai thi phai NO, ⛔ khong duoc lui ve sheet." % xau)


def test_duong_nap_KHONG_CON_giu_san_duong_ay_trong_import():
    """⛔⛔ Cũng ⛔ không được **giữ sẵn** nó trong `import`.

    Một `import` ⛔ không ai gọi trông vô hại, nhưng nó là **một cánh cửa hé
    mở**: người sau chỉ cần gõ thêm một lời gọi. Cửa đóng thì họ phải viết
    thêm dòng `import` — và lúc ấy họ sẽ **dừng lại nghĩ**.
    """
    xau = sorted(_ten_duoc_import(_cay()) & DUONG_SHEET)
    assert xau == [], (
        "⛔ duong nap van giu san %s trong import — go han di, ⛔ khong de mot "
        "canh cua he mo" % xau)


def test_duong_nap_THAT_SU_doc_tu_kho():
    """⛔ Cổng chung #7 — chứng minh bài trên ⛔ **không xanh vì trống rỗng**.

    Nếu ⓐ nó ⛔ không gọi đường sheet **và** ⓑ nó cũng ⛔ không gọi đường kho,
    thì hai bài trên xanh mà **⛔ không có gì được bảo vệ**.
    """
    goi = _ten_duoc_goi(_cay())
    assert "doc_khai" in goi, "⛔ duong nap ⛔ khong he doc kho"
    assert "khai_tu_kho" in goi, "⛔ `nap()` ⛔ khong he goi `khai_tu_kho()`"


def test_thieu_ban_khai_thi_NO_chu_KHONG_lui_ve_sheet():
    """⭐⭐ Đường nổ phải **nói ra phải làm gì**, ⛔ không chỉ nói *"lỗi"*.

    Một thông báo cụt sẽ đẩy người đọc đi tìm đường vòng — và đường vòng gần
    nhất chính là **đọc lại dòng 1**.
    """
    src = NAP.read_text(encoding="utf-8")
    assert "nap_nguon_va_khai.py" in src, (
        "⛔ loi 'thieu ban khai' phai neu TEN LENH chay lai")
    assert "KHÔNG lùi về dòng 1" in src, (
        "⛔ phai noi THANG rang ⛔ khong co duong lui — de nguoi sau ⛔ khong "
        "tu nghi ra mot duong lui")
