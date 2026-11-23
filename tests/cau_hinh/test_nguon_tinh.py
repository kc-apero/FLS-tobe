# -*- coding: utf-8 -*-
"""`fls/cau_hinh/nguon_tinh.py` — luật **MỘT chỗ** cho đường *nguồn tĩnh* *(ISP 3.1.2 ·
Step 2 · `C1` · vòng sửa sau R1 — `C1-R1-02`, `KQ-077`)*.

⛔⛔ **Vì sao bộ bài này tồn tại** — R1 dựng 4 tuyến cố ý khai sai `Tuyen.nguon_tinh`
   rồi hỏi hai cổng *(bản sao, ⛔ kho)*:
     · **A** hàm `so` *(đọc `fls_itl`)* · `bang=()` · `nguon_tinh=('pyproject.toml',)`
       ⇒ `kiem_bang_tuyen` **XANH**;
     · **B** `nguon_tinh=('CLAUDE.md',)` ⇒ **cả hai cổng XANH**;
     · **D** `nguon_tinh=('../../../../../../../../etc/hostname',)` *(ra NGOÀI repo)*
       ⇒ **cả hai cổng XANH**;
     · **C** `nguon_tinh` là CHUỖI *(quên dấu phẩy tuple)* ⇒ `kiem_bang_tuyen` XANH,
       `soi` đỏ bằng **32** câu rác *(một câu mỗi ký tự)*.
   Gốc: ngoại lệ `nguon_tinh` của `C1` chỉ hỏi *"tệp có tồn tại"* ⇒ nó **nới** cổng ⓓ
   *("một đường ⛔ nói nó chạm gì")* cho **mọi tệp có thật** trên máy. Và `doc_tep`
   cũ đọc `_GOC_REPO / duong` — `Path / '/etc/hostname'` là `/etc/hostname`.

⇒ Thư mục nguồn tĩnh khai **MỘT chỗ** (`THU_MUC`), và một luật đường dùng chung cho
  `kiem_bang_tuyen` · `soi_bang_tuyen` · `fx.doc_tep`. `C4` *(`GET /config/hd` "tĩnh từ
  ảnh")* sẽ là người dùng thứ hai — dùng lại, ⛔ chép.
"""
from __future__ import annotations

import importlib
import os
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
# Chép NGUYÊN VĂN — ⛔ đọc lại từ hằng: bài canh chính hằng ấy.
THU_MUC = "fls/cau_hinh/tinh"
# ⭐⭐ `C5` (`WO-142`): ẢNH TĨNH *(`mau.json` …)* đã GỠ — luật ĐƯỜNG `nguon_tinh`
#   vẫn là hợp đồng của `Tuyen` *(phòng thủ cho tuyến tĩnh tương lai)*. Bài canh HÌNH
#   đường ⇒ mẫu chỉ cần ĐÚNG KHUÔN, ⛔ cần tệp có thật; phép `giai` *(đòi tệp)* dựng
#   tệp tạm qua `goc=tmp_path`.
MAU = "fls/cau_hinh/tinh/mau.json"


def _nt():
    """Nạp TRỄ *(cùng lý do `test_fx._fx`: trước khi có mã, mỗi bài đỏ RIÊNG bằng
    `ModuleNotFoundError` — thiếu hành vi, ⛔ lỗi dựng bài)*."""
    return importlib.import_module("fls.cau_hinh.nguon_tinh")


def test_thu_muc_khai_MOT_cho_va_duong_dung_khuon_hop_le(tmp_path):
    nt = _nt()
    assert nt.THU_MUC == THU_MUC
    # ⛔ `Đ3`: luật đường nào cũng "xanh" nếu ⛔ có đường hợp lệ nào đi qua nó.
    assert nt.kiem_duong(MAU) == []
    assert nt.kiem_khai((MAU,)) == []
    assert nt.kiem_khai(()) == [], "() = tuyến ⛔ có nguồn tĩnh — hợp lệ"
    # `giai` đòi tệp CÓ THẬT — dựng repo giả ở `tmp_path` *(ảnh tĩnh đã GỠ ở `C5`)*.
    tinh = tmp_path / THU_MUC
    tinh.mkdir(parents=True)
    (tinh / "mau.json").write_text("{}", encoding="utf-8")
    p = nt.giai(MAU, goc=tmp_path)
    assert p.is_file() and p == (tmp_path / MAU).resolve(), p


@pytest.mark.parametrize("duong,phai_noi", [
    ("pyproject.toml", "NGAY dưới"),                            # R1 · A
    ("CLAUDE.md", "NGAY dưới"),                                 # R1 · B
    ("../../../../../../../../etc/hostname", "khúc rỗng"),      # R1 · D — `..`
    ("fls/cau_hinh/tinh", "tên tệp"),                           # R1 · E — thư mục
    ("fls/cau_hinh/tinh/", "khúc rỗng"),
    ("/etc/hostname", "TUYỆT ĐỐI"),
    (str(GOC / MAU), "TUYỆT ĐỐI"),                         # dù đúng tệp
    ("fls/cau_hinh/tinh/../../../CLAUDE.md", "khúc rỗng"),      # `..` giữa đường
    ("fls/cau_hinh/tinh/./mau.json", "khúc rỗng"),        # `.`
    ("fls//cau_hinh/tinh/mau.json", "khúc rỗng"),
    ("fls/cau_hinh/tinh/con/mau.json", "NGAY dưới"),      # thư mục con
    ("fls\\cau_hinh\\tinh\\mau.json", "POSIX"),
    ("C:/fls/cau_hinh/tinh/mau.json", "TUYỆT ĐỐI"),       # ổ đĩa Windows
    ("fls/cau_hinh/tinh/mau.txt", "tên tệp"),             # ⛔ `.json`
    ("fls/cau_hinh/tinh/IX FX.json", "tên tệp"),                # ngoài `[a-z0-9_]`
    (" fls/cau_hinh/tinh/mau.json", "khoảng trắng"),
    ("", "rỗng"),
])
def test_duong_SAI_thi_co_ly_do_MOT_dong(duong, phai_noi):
    """Mỗi đường sai ⇒ lý do **gọi đúng tên** luật nó phạm *(⛔ chỉ "có lỗi")* — để
    một luật bị gỡ ⛔ được luật bên cạnh che *(vd `..` cũng phạm "⛔ NGAY dưới")*."""
    nt = _nt()
    ly_do = nt.kiem_duong(duong)
    assert ly_do, f"⛔ {duong!r} lọt luật đường"
    assert any(phai_noi in x for x in ly_do), ly_do
    assert all("\n" not in x for x in ly_do), ly_do
    with pytest.raises(nt.LoiNguonTinh) as e:
        nt.giai(duong)
    assert "\n" not in str(e.value), str(e.value)


@pytest.mark.parametrize("sai", [Path(MAU), None, MAU.encode(), 1])
def test_duong_SAI_KIEU_thi_mot_ly_do_noi_kieu(sai):
    nt = _nt()
    ly_do = nt.kiem_duong(sai)
    assert len(ly_do) == 1 and type(sai).__name__ in ly_do[0], ly_do


@pytest.mark.parametrize("khai,phai_noi", [
    (MAU, "str"),                  # R1 · C — quên dấu phẩy tuple
    ([MAU], "list"),
    ((Path(MAU),), "PosixPath" if os.name != "nt" else "WindowsPath"),
    ((MAU, MAU), "trùng"),
])
def test_khai_SAI_KIEU_thi_MOT_dong_KHONG_mot_cau_moi_ky_tu(khai, phai_noi):
    """R1 · C: `soi` cũ lặp trên CHUỖI ⇒ **32** câu rác. Luật mới: sai kiểu ⇒ **một**
    lý do, nói kiểu đo được."""
    nt = _nt()
    ly_do = nt.kiem_khai(khai)
    assert len(ly_do) == 1, ly_do
    assert phai_noi in ly_do[0] and "\n" not in ly_do[0], ly_do


def test_giai_DUONG_THAT_qua_lien_ket_ra_ngoai_thi_TU_CHOI(tmp_path):
    """*"Giải đường thật"*: một liên kết mềm ĐÚNG khuôn tên trong thư mục tĩnh mà trỏ
    ra ngoài ⇒ từ chối. Dựng một repo giả ở `tmp_path` *(⛔ ghi vào repo thật)*."""
    nt = _nt()
    tinh = tmp_path / THU_MUC
    tinh.mkdir(parents=True)
    (tmp_path / "ngoai.json").write_text("{}", encoding="utf-8")
    (tinh / "that.json").write_text("{}", encoding="utf-8")
    (tinh / "lot.json").symlink_to(tmp_path / "ngoai.json")

    # Đ3: nền — tệp thật cùng thư mục thì qua.
    assert nt.kiem_duong(f"{THU_MUC}/that.json", goc=tmp_path) == []
    assert nt.giai(f"{THU_MUC}/that.json", goc=tmp_path).is_file()
    ly_do = nt.kiem_duong(f"{THU_MUC}/lot.json", goc=tmp_path)
    assert ly_do and any("ngoài" in x for x in ly_do), ly_do


def test_giai_THU_MUC_tinh_la_lien_ket_ra_ngoai_thi_TU_CHOI(tmp_path):
    """Chính thư mục `fls/cau_hinh/tinh` là liên kết mềm ra ngoài repo ⇒ mọi tệp
    "trong" nó thật ra nằm ngoài ⇒ từ chối."""
    nt = _nt()
    ngoai = tmp_path / "ngoai"
    ngoai.mkdir()
    (ngoai / "x.json").write_text("{}", encoding="utf-8")
    (tmp_path / "fls" / "cau_hinh").mkdir(parents=True)
    (tmp_path / THU_MUC).symlink_to(ngoai, target_is_directory=True)
    assert nt.kiem_duong(f"{THU_MUC}/x.json", goc=tmp_path), "⛔ lọt qua liên kết"


def test_giai_tep_KHONG_co_that_thi_TU_CHOI():
    """Khuôn đúng mà tệp ⛔ có ⇒ `giai` từ chối *(`kiem_duong` chỉ xét HÌNH — sự có
    mặt là phép canh của `soi` và của lúc đọc)*."""
    nt = _nt()
    d = f"{THU_MUC}/khong_co_that.json"
    assert nt.kiem_duong(d) == []
    with pytest.raises(nt.LoiNguonTinh) as e:
        nt.giai(d)
    assert "khong_co_that.json" in str(e.value), str(e.value)
