# -*- coding: utf-8 -*-
"""`IX.FX` — nạp + kiểm tỷ giá tháng *(ISP 3.1.2 · Step 2 · `C1` · `WO-075`)*.

⛔⛔ **Vì sao bộ bài này tồn tại** — AP v3.1.2 §3.2.4, dòng *"bảng tỷ giá"*: ở AS-IS
   bảng `9.2.Exchange Rate` được tra bằng `SUMIFS(tháng)` ⇒ **tháng thiếu ⇒ `SUMIFS`
   = 0 ⇒ mất số không báo**; **tháng nhập hai dòng ⇒ cộng đôi**. Cả hai lỗi đều
   **IM LẶNG** — trang tính vẫn ra một con số, chỉ là con số sai. Một bảng config
   TO-BE phải nói hai chuyện ấy ra thành **TRƯỜNG RIÊNG** (`thieu` · `trung` · `lac`),
   ⛔ biến chúng thành `0` hay thành một tổng.

Test ID = ISP mục 6: `C1-B1` · `C1-B2` · `C1-B3` · `C1-B5`.
*(`C1-B4` — tuyến HTTP — ở `tests/api/test_isp_config_fx.py`.)*

⭐ Bài `test_phu_*` — **bổ sung NGOÀI mục 6**, phủ phần *"kiểm"* mà phạm vi `C1` khai
   *(một dòng/tháng · VND = 1 · đủ 5 tiền tệ · thiếu/trùng/lạc)* nhưng mục 6 ⛔ có ID
   riêng: lạc · VND ≠ 1 · thiếu tiền tệ · tập rỗng. Một nhánh kiểm ⛔ có bài là một
   nhánh **chưa biết có chạy** *(bia `bien_ban` ở `fls/api/bao.py`)*.

⛔ Mọi tỷ giá trong tệp này là số **BỊA có chủ đích** — khuôn `2000k` · `900k` ·
   `7.0k` · `300k` để ⛔ ai nhầm với tỷ giá thật *(thật chỉ vào ở `DT2` → `C5`)*.
"""
from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
from decimal import Decimal as D
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]

# Tên hợp đồng tầng 10 — chép NGUYÊN VĂN từ `.importlinter` *(S0 khai)*.
HOP_DONG_10 = "fls.cau_hinh la config thuan, khong duoc biet tang kho"


def _fx():
    """Nạp **TRỄ** `fls.cau_hinh.fx`.

    ⭐ Vì sao ⛔ nạp ở đầu tệp: trước khi có mã, một `import` đầu tệp làm **cả tệp**
      thành MỘT lỗi thu thập — che mất từng test ID. Nạp trễ ⇒ mỗi bài đỏ RIÊNG
      bằng đúng câu `ModuleNotFoundError: No module named 'fls.cau_hinh.fx'`, tức
      đỏ vì **thiếu hành vi**, ⛔ vì lỗi dựng bài.
    """
    return importlib.import_module("fls.cau_hinh.fx")


def _dong(yyyymm: int | str, k: int = 1, **doi: object) -> dict:
    """Một dòng TỔNG HỢP. `doi` ghi đè/thêm ô; `doi[x] = BO` ⇒ gỡ hẳn cột `x`."""
    d: dict = {"yyyymm": yyyymm, "USD": f"2000{k}", "SGD": f"900{k}",
               "COP": f"7.0{k}", "VND": "1", "HKD": f"300{k}"}
    for ten, gia_tri in doi.items():
        if gia_tri is BO:
            d.pop(ten)
        else:
            d[ten] = gia_tri
    return d


BO = object()                     # dấu "gỡ cột" cho `_dong`
# ⭐ `yyyymm` là SỐ NGUYÊN *(hợp đồng liên làn: engine H1 `fls/bao_cao/gl.py` khoá
#   tỷ giá theo `int` yyyymm — orchestrator 16/11)*.
BON_THANG = (202406, 202407, 202408, 202409)


def _bon() -> list[dict]:
    """Bốn tháng LIỀN, hợp lệ — nền cho B2 · B3 · các bài phụ."""
    return [_dong(m, k=i + 1) for i, m in enumerate(BON_THANG)]


# ── C1-B1 ─────────────────────────────────────────────────────────────────
def test_C1_B1_nap_BON_thang_hop_le_tu_nguon_tinh():
    """Nạp **nguồn tĩnh thật của bước** (`fls/cau_hinh/tinh/ix_fx_mau.json`).

    ⚠ `Đ3`: *"`thieu = trung = lac = []`"* chỉ có nghĩa khi phép kiểm đã chạy trên
      một tập KHÁC RỖNG ⇒ đếm mẫu số trước: **4** dòng · **4** tháng khác nhau.
    """
    fx = _fx()
    b = fx.doc_tep()

    assert len(b.ky) == 4, f"⛔ mong 4 dòng, đo {len(b.ky)}"
    thang = [d.yyyymm for d in b.ky]
    assert len(set(thang)) == 4, f"⛔ mong 4 tháng khác nhau, đo {thang}"
    assert thang == sorted(thang), f"⛔ `ky` phải theo thứ tự tháng: {thang}"

    for d in b.ky:
        # ⭐ SỐ NGUYÊN *(⛔ `bool`)* — hợp đồng liên làn với engine H1.
        assert type(d.yyyymm) is int, (d.yyyymm, type(d.yyyymm))
        assert set(d.ty_gia) == set(fx.TIEN_TE), (d.yyyymm, sorted(d.ty_gia))
        assert d.ty_gia["VND"] == D(1), (d.yyyymm, d.ty_gia["VND"])
        # ⛔ `float` ⛔ bao giờ đứng giữa nguồn và kho — luật `fls/api/bao.py`.
        assert all(isinstance(v, D) for v in d.ty_gia.values()), d
        # C1 ⛔ có ký *(ký là C7 — D1)* ⇒ MỌI tháng đều `chua_ky`.
        assert d.trang_thai == "chua_ky", (d.yyyymm, d.trang_thai)

    assert (b.thieu, b.trung, b.lac) == ((), (), ())
    assert b.nguon == fx.NGUON_TINH == "fls/cau_hinh/tinh/ix_fx_mau.json"


def test_C1_B1_nguon_tinh_TU_KHAI_la_so_TONG_HOP():
    """⛔ Nguồn tĩnh của C1 là **số bịa có chủ đích** — tệp phải TỰ NÓI điều ấy.

    Một tệp tỷ giá ⛔ ghi gì về gốc của nó thì người sau sẽ tưởng đó là số thật.
    """
    fx = _fx()
    tho = json.loads((GOC / fx.NGUON_TINH).read_text(encoding="utf-8"))
    assert tho.get("tong_hop") is True, sorted(tho)
    assert "TỔNG HỢP" in tho.get("ghi_chu", ""), tho.get("ghi_chu")


# ── C1-B2 ─────────────────────────────────────────────────────────────────
def test_C1_B2_thang_202407_HAI_dong_thi_TRUNG_va_KHONG_cong_doi():
    fx = _fx()
    dong = _bon() + [_dong(202407, k=8)]
    b = fx.kiem(dong, thang_dau=202406, nguon="bai-thu")

    assert b.trung == (202407,)
    # ⭐ CẢ HAI dòng hiện ra — ⛔ im lặng chọn một, ⛔ gộp thành một.
    hai = [d for d in b.ky if d.yyyymm == 202407]
    assert len(hai) == 2, [d.yyyymm for d in b.ky]
    assert sorted(d.ty_gia["USD"] for d in hai) == [D("20002"), D("20008")]
    # ⛔⛔ CỘNG ĐÔI: đúng lỗi `SUMIFS` của AS-IS (AP §3.2.4).
    tong = D("20002") + D("20008")
    assert all(d.ty_gia["USD"] != tong for d in b.ky), "⛔ có dòng mang TỔNG"
    assert len(b.ky) == 5, f"⛔ 5 dòng vào ⇒ 5 dòng ra, đo {len(b.ky)}"
    assert (b.thieu, b.lac) == ((), ())


# ── C1-B3 ─────────────────────────────────────────────────────────────────
def test_C1_B3_thieu_202408_GIUA_dai_thi_THIEU():
    fx = _fx()
    dong = [d for d in _bon() if d["yyyymm"] != 202408]
    b = fx.kiem(dong, thang_dau=202406, nguon="bai-thu")

    assert b.thieu == (202408,)
    # ⛔ ⛔ bịa một dòng `0` cho 202408 — đúng lỗi `SUMIFS = 0` của AS-IS.
    assert [d.yyyymm for d in b.ky] == [202406, 202407, 202409]
    assert (b.trung, b.lac) == ((), ())


# ── bổ sung ngoài mục 6: phủ phần "kiểm" của phạm vi C1 ──────────────────
def test_phu_thang_LAC_truoc_thang_dau_hien_ra_rieng_va_KHONG_lam_phinh_thieu():
    """`202306` của nguồn thật *(AP §3.2.1: "kể cả dòng lạc 202306")* — dựng lại
    bằng số bịa: một tháng nằm TRƯỚC `thang_dau` là **lạc**, ⛔ kéo theo
    `202307…202405` vào `thieu`.
    """
    fx = _fx()
    b = fx.kiem(_bon() + [_dong(202306, k=6)], thang_dau=202406,
                nguon="bai-thu")
    assert b.lac == (202306,)
    assert b.thieu == (), f"⛔ dòng lạc làm phình `thieu`: {b.thieu}"
    # ⭐ dòng lạc vẫn HIỆN trong `ky` — ⛔ vứt im lặng.
    assert 202306 in [d.yyyymm for d in b.ky]
    assert b.trung == ()


@pytest.mark.parametrize("thang,doi,phai_noi", [
    (202407, {"VND": "2"}, "VND"),            # VND ⛔ = 1
    (202408, {"HKD": BO}, "HKD"),             # thiếu hẳn cột tiền tệ
    (202408, {"HKD": ""}, "HKD"),             # ô rỗng ⛔ thành 0
    (202408, {"HKD": None}, "HKD"),
    (202409, {"USD": "abc"}, "USD"),          # ⛔ phải số
    (202409, {"USD": "-5"}, "USD"),           # tỷ giá ≤ 0
    (202409, {"USD": 20001.5}, "USD"),        # ⛔ float — qua float là mất chữ số
    (202406, {"EUR": "1"}, "EUR"),            # cột lạ ⛔ bỏ qua im lặng
])
def test_phu_dong_SAI_thi_NO_co_ten_thang_va_cot(thang, doi, phai_noi):
    """⛔ Một ô sai ⛔ được thành `0` hay bị bỏ qua: NỔ, và câu nổ nói **tháng nào ·
    cột nào** *(luật phòng tái phạm `S0-R1-04`: nguyên nhân đọc được trong một dòng)*.
    """
    fx = _fx()
    dong = [_dong(d["yyyymm"], k=i + 1, **doi) if d["yyyymm"] == thang else d
            for i, d in enumerate(_bon())]
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem(dong, thang_dau=202406, nguon="bai-thu")
    cau = str(e.value)
    assert str(thang) in cau and phai_noi in cau, cau
    assert "\n" not in cau, f"⛔ câu nổ phải MỘT dòng: {cau!r}"


@pytest.mark.parametrize("sai", [202413, "202413", "2024-07", 2024071, True])
def test_phu_thang_SAI_khuon_thi_NO(sai):
    """⛔ `True` là `int` trong Python — ⛔ được lọt thành tháng `1`."""
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem(_bon() + [_dong(sai)], thang_dau=202406, nguon="bai-thu")
    assert str(sai) in str(e.value), str(e.value)


def test_phu_yyyymm_CHUOI_sau_chu_so_chuan_ve_SO_NGUYEN():
    """Nguồn có thể ghi tháng là chuỗi `"202407"` *(ô văn bản ở sheet)* — mô hình
    luôn ra `int`, và kết quả TRÙNG KHÍT bản nạp bằng số nguyên."""
    fx = _fx()
    chuoi = [dict(d, yyyymm=str(d["yyyymm"])) for d in _bon()]
    a = fx.kiem(chuoi, thang_dau="202406", nguon="bai-thu")
    b = fx.kiem(_bon(), thang_dau=202406, nguon="bai-thu")
    assert [type(d.yyyymm) for d in a.ky] == [int] * 4
    assert a == b


@pytest.mark.parametrize("dong", [
    [],                                   # ⛔ dòng nào
    [_dong(202306)],                      # có dòng nhưng ⛔ tháng nào ≥ thang_dau
])
def test_phu_tap_RONG_thi_NO_chu_KHONG_xanh_tren_tap_rong(dong):
    """`Đ3`: *"thiếu = trùng = lạc = rỗng"* trên **0** tháng là xanh trên tập rỗng."""
    fx = _fx()
    with pytest.raises(fx.LoiFX):
        fx.kiem(dong, thang_dau=202406, nguon="bai-thu")


# ── C1-B5 ─────────────────────────────────────────────────────────────────
def test_C1_B5_fls_cau_hinh_KHONG_biet_tang_kho__lint_imports():
    """Hợp đồng tầng 10 *(cấm `psycopg` · `fls.repo` · `fls.db`)* phải `KEPT`.

    ⛔ `Đ5`: ⛔ thấy `lint-imports` là ĐỎ *(phép ⛔ đo được)*, ⛔ bỏ qua; dòng hợp
      đồng phải khớp ĐÚNG MỘT lần — `0` hay `≥2` lần là đo hỏng.
    ⭐ Đường gọi theo hệ điều hành: container `.venv/bin/lint-imports` · máy owner
      `.venv/Scripts/lint-imports.exe` *(bẫy `kiem_so_song` gọi cứng đường Windows).*
    """
    exe = Path(sys.executable).parent / (
        "lint-imports.exe" if os.name == "nt" else "lint-imports")
    assert exe.is_file(), f"⛔ ⛔ thấy {exe} ⇒ phép đo CHƯA CHẠY"
    r = subprocess.run([str(exe)], cwd=GOC, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=300,
                       env={**os.environ, "PYTHONUTF8": "1"})
    ra = r.stdout + r.stderr
    dong = [x.strip() for x in ra.splitlines()
            if x.strip().startswith(HOP_DONG_10)]
    assert len(dong) == 1, f"⛔ dòng hợp đồng 10 khớp {len(dong)} lần:\n{ra[-1500:]}"
    assert dong[0].endswith(" KEPT"), dong[0]
