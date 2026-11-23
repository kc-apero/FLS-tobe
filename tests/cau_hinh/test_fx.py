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
def test_C1_B1_nap_BON_thang_hop_le():
    """Kiểm một bảng **4 tháng LIỀN hợp lệ**.

    ⭐⭐ `C5` (`WO-142`): nguồn TĨNH `ix_fx_mau.json` + `doc_tep()` đã GỠ *(tuyến
       đọc KHO — `tests/cau_hinh/test_kho_cau_hinh_pg.py`)*. Lõi `kiem` giữ nguyên,
       nên bài này **giữ nguyên lo** — chỉ đổi nguồn vào thành `_bon()` *(⛔ tệp)*.

    ⚠ `Đ3`: *"`thieu = trung = lac = []`"* chỉ có nghĩa khi phép kiểm đã chạy trên
      một tập KHÁC RỖNG ⇒ đếm mẫu số trước: **4** dòng · **4** tháng khác nhau.
    """
    fx = _fx()
    b = fx.kiem(_bon(), thang_dau=BON_THANG[0], nguon="bai-thu")

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
    assert b.nguon == "bai-thu"


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
    # Tỷ giá ÂM ⇒ bị TỪ CHỐI — ca này chỉ hỏi tháng + cột, ⛔ hỏi LÝ DO: mã hôm nay
    # chặn bằng chốt `> 0`; gỡ chốt ấy thì khuôn thập phân *(⛔ dấu `-`)* bắt thay và
    # ca này vẫn xanh *(R2 `C1-R2-01`: nhãn cũ "tỷ giá ≤ 0" hứa biên `0` mà ⛔ đưa `0`)*.
    # Biên `0` + lý do `> 0` ⇒ `test_R2_01_ty_gia_BANG_0_thi_NO_va_NOI_lon_hon_0`.
    (202409, {"USD": "-5"}, "USD"),
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
    """Tháng sai khuôn ⇒ `LoiFX` nói ra giá trị.

    ⚠ Câu cũ ở đây *("`True` … ⛔ được lọt thành tháng `1`")* **SAI cơ chế** —
      `C1-R1-04` *(KQ-077)*: `_thang` đọc qua `str(v)` ⇒ `'True'` vốn trượt khuôn,
      có chốt `bool` hay ⛔. Ca `True` ở đây chỉ ghim *"bị từ chối"*; **chốt** `bool`
      được ghim riêng ở `test_R1_04_bool_o_cot_THANG_bi_chan_TUONG_MINH_co_ten`.
    """
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


# ══ Vòng sửa sau R1 (`KQ-077`) ══════════════════════════════════════════════
#
# ⛔⛔ Vì sao khối này tồn tại: R1 đột biến `fx.py` trên bản sao — **13** đột biến,
#    bộ 22 bài trên **chỉ bắt 5**. Tám đột biến SỐNG đều là nhánh mà mã làm ĐÚNG
#    nhưng ⛔ bài nào ghim — tức một nhánh *"chưa biết có còn chạy"* sau lần sửa kế.
#    Nặng nhất: **M3** *(vòng `thieu` bắt đầu từ tháng nhỏ nhất của DỮ LIỆU thay cho
#    `thang_dau`)* làm tháng đầu dải thiếu **BIẾN MẤT im lặng** — đúng lớp lỗi
#    `SUMIFS = 0` bước này sinh ra để chặn — mà 22/22 bài vẫn xanh.
#    Mỗi bài dưới ghi **đột biến nó giết** *(log: `BG-076` mục "Vòng sửa sau R1")*.


# ── C1-R1-01 · hai nhánh của `thieu` *(NÊN SỬA)* ─────────────────────────────
@pytest.mark.parametrize("thang,dau,mong", [
    # Bài R1 đề xuất, chép nguyên: lỗ ở tháng 1 năm sau.
    ((202411, 202412, 202502), 202411, (202501,)),
    # Lật năm LIỀN: ⛔ lỗ nào. Dưới M1 vòng đi 202413 → 202500 ⇒ 88 tháng ma.
    ((202412, 202501), 202412, ()),
])
def test_R1_01a_thieu_QUA_NAM_dung_thang_1_nam_sau(thang, dau, mong):
    """Dải tháng **qua tháng 12** *(giết M1: `_thang_ke` ⇒ `return m + 1`)*.

    Ảnh thật của `IX.FX` *(AP §3.2.1: 37 dòng `202401 → 202612`)* qua **2** lần lật
    năm; mọi bài trước R1 dùng dải `202406…202409` — ⛔ chạm biên nào.
    """
    b = _fx().kiem([_dong(m) for m in thang], thang_dau=dau, nguon="bai-thu")
    assert b.thieu == mong, b.thieu


@pytest.mark.parametrize("thang,mong", [
    # Bài R1 đề xuất, chép nguyên: dữ liệu bắt đầu SAU `thang_dau` một tháng.
    ((202407, 202408, 202409), (202406,)),
    # Hai tháng đầu dải cùng thiếu.
    ((202408, 202409), (202406, 202407)),
])
def test_R1_01b_lo_DAU_dai_tu_thang_dau_la_THIEU(thang, mong):
    """Dải bắt đầu từ **`thang_dau`**, ⛔ từ tháng nhỏ nhất của dữ liệu *(giết M3)*.

    ⛔ Đây là nửa *"dải bắt đầu ở `thang_dau`"* của định nghĩa orchestrator chốt
      *(Q2 của `BG-076`)* — trước R1 ⛔ bài nào ghim. Dưới M3 tháng `202406` biến
      khỏi `thieu` **im lặng** ⇒ `fx_cua()` của C7 ⛔ có tên tháng để CHẶN.
    """
    b = _fx().kiem([_dong(m) for m in thang], thang_dau=202406, nguon="bai-thu")
    assert b.thieu == mong, b.thieu
    assert [d.yyyymm for d in b.ky] == list(thang), "⛔ bịa dòng cho tháng thiếu"


# ── C1-R1-04 · sáu đột biến sống *(GHI NHẬN — làm luôn)* ─────────────────────
@pytest.mark.parametrize("x", ["NaN", "Infinity", "-Infinity", "sNaN"])
def test_R1_01c_so_KHONG_huu_han_thi_NO(x):
    """Bài R1 đề xuất *(giết M2: bỏ `is_finite()`)* + câu nổ phải NÓI *"hữu hạn"*.

    Dưới M2: `'Infinity'` qua được `> 0`; `'NaN'` ném `InvalidOperation` ⛔ có tên
    *(⛔ `LoiFX`)* — luật `H1-R1-02` được mã áp mà ⛔ bài ghim.
    """
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem([_dong(202406, USD=x)], thang_dau=202406, nguon="bai-thu")
    cau = str(e.value)
    assert "202406" in cau and "USD" in cau and "hữu hạn" in cau, cau


def test_R1_01d_ky_SAP_theo_thang_du_dau_vao_dao():
    """Bài R1 đề xuất *(giết M4: bỏ sắp `ky`)* — mọi bài trước R1 nạp dữ liệu ĐÃ sắp."""
    b = _fx().kiem([_dong(m) for m in (202409, 202406, 202408, 202407)],
                   thang_dau=202406, nguon="bai-thu")
    assert [d.yyyymm for d in b.ky] == [202406, 202407, 202408, 202409]


def test_R1_04_bool_o_cot_THANG_bi_chan_TUONG_MINH_co_ten():
    """Chốt `bool` ở `_thang` *(giết M5)*.

    ⛔ Câu cũ *"`True` … sẽ lọt thành tháng 1 nếu ⛔ chặn tường minh"* SAI: `str(True)`
      = `'True'` vốn trượt khuôn. Cái chốt làm được — và bài này ghim — là **gọi đúng
      tên nguyên nhân**: một ô `bool` *(ô tick ở sheet)* lọt vào cột tháng, ⛔ câu
      chung chung *"⛔ đúng khuôn yyyymm"* *(luật `S0-R1-04`: nguyên nhân đọc được)*.
    """
    fx = _fx()
    for sai in ({"dong": _bon() + [_dong(True)], "dau": 202406},
                {"dong": _bon(), "dau": True}):
        with pytest.raises(fx.LoiFX) as e:
            fx.kiem(sai["dong"], thang_dau=sai["dau"], nguon="bai-thu")
        assert "bool" in str(e.value) and "True" in str(e.value), str(e.value)


def test_R1_04_bool_o_cot_TY_GIA_bi_chan_TUONG_MINH_co_ten():
    """Chốt `bool` ở `_so` *(giết M6)* — cùng lý do bài trên: `Decimal('True')` vốn
    ném `InvalidOperation`, chốt chỉ đáng giữ nếu nó nói ra **`bool`**."""
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem(_bon()[:1] + [_dong(202407, USD=True)], thang_dau=202406,
                nguon="bai-thu")
    cau = str(e.value)
    assert "202407" in cau and "USD" in cau and "bool" in cau, cau


def _van_ban(**doi: object) -> str:
    """Một nguồn JSON hợp lệ dạng VĂN BẢN *(⛔ đi qua `dict` — `C1-R1-06` ⓐ cần
    giữ được khoá trùng, mà `dict` Python đã nuốt mất trước khi tới `json`)*."""
    goc = {"bang": "IX.FX", "thang_dau": 202406, "dong": _bon()}
    goc.update(doi)
    return json.dumps(goc, ensure_ascii=False)


def test_R1_04_doc_van_ban_BANG_sai_thi_NO():
    """`doc_tep` kiểm `bang == 'IX.FX'` *(giết M9)* — một tệp của bảng KHÁC đặt nhầm
    tên ⛔ được đọc thành tỷ giá. *(Lõi đọc tách thành `doc_van_ban` để bài khỏi phải
    ghi tệp vào `fls/cau_hinh/tinh/` — thư mục duy nhất `doc_tep` nay chịu đọc,
    `C1-R1-02`.)*"""
    fx = _fx()
    assert len(fx.doc_van_ban(_van_ban(), nguon="bai-thu").ky) == 4   # Đ3: nền xanh
    with pytest.raises(fx.LoiFX) as e:
        fx.doc_van_ban(_van_ban(bang="IX.FY"), nguon="bai-thu")
    assert "IX.FX" in str(e.value), str(e.value)


def test_R1_04_doc_van_ban_ty_gia_SO_JSON_vao_Decimal_KHONG_qua_float():
    """Tỷ giá ghi bằng **số** JSON *(`"COP": 5.01`, ⛔ nháy)* phải ra `Decimal('5.01')`
    nguyên chữ số *(giết M10: bỏ `parse_float=Decimal` ⇒ `float` ⇒ bị từ chối)*."""
    fx = _fx()
    van_ban = _van_ban().replace('"COP": "7.01"', '"COP": 5.01')
    assert van_ban.count('"COP": 5.01') == 1, "⛔ dựng bài hỏng: mẫu khớp ≠ 1 lần"
    b = fx.doc_van_ban(van_ban, nguon="bai-thu")
    cop = b.ky[0].ty_gia["COP"]
    assert type(cop) is D and cop == D("5.01") and str(cop) == "5.01", repr(cop)


# ── C1-R1-06 · lối vào nguồn đi qua im lặng hay méo *(GHI NHẬN — làm luôn)* ──
def test_R1_06_khoa_JSON_TRUNG_trong_mot_dong_thi_NO_co_ten():
    """ⓐ `{"USD": "1", "USD": "999"}` — `json.loads` mặc định **giữ bản CUỐI, im
    lặng**: cùng họ *"hai giá trị cho một ô, một cái biến mất"* mà bước này chặn ở
    mức tháng *(trùng)*. ⇒ NỔ, nói **khoá nào · tháng nào**."""
    fx = _fx()
    van_ban = _van_ban().replace('"USD": "20001"', '"USD": "20001", "USD": "999"')
    assert van_ban.count('"USD": "999"') == 1, "⛔ dựng bài hỏng"
    with pytest.raises(fx.LoiFX) as e:
        fx.doc_van_ban(van_ban, nguon="bai-thu")
    cau = str(e.value)
    assert "USD" in cau and "202406" in cau and "trùng" in cau, cau
    assert "\n" not in cau, cau


def test_R1_06_khoa_JSON_TRUNG_o_DAU_tep_cung_NO():
    """Khoá trùng ở **vỏ** tệp *(hai `thang_dau`)* — giữ bản cuối là đổi dải kiểm im lặng."""
    fx = _fx()
    van_ban = _van_ban().replace('"thang_dau": 202406',
                                 '"thang_dau": 202406, "thang_dau": 202408')
    with pytest.raises(fx.LoiFX) as e:
        fx.doc_van_ban(van_ban, nguon="bai-thu")
    assert "thang_dau" in str(e.value), str(e.value)


@pytest.mark.parametrize("x", [
    "1e4", "1E+4",               # số mũ ⇒ cũ in ra `"1E+4"`
    "１２３",                     # chữ số TOÀN KHỔ ⇒ cũ nhận thành 123
    "٣",                          # chữ số Ả-rập ⇒ `Decimal` cũng nhận
    "+10001",                     # dấu `+`
    D("1E+4"),                    # `Decimal` dạng mũ
])
def test_R1_06_ty_gia_KHONG_dung_khuon_thap_phan_ASCII_thi_NO(x):
    """ⓑ Tỷ giá phải là **thập phân ASCII trơn** `^[0-9]+(\\.[0-9]+)?$`. `Decimal`
    nhận chữ số Unicode và số mũ ⇒ bản cũ để `'１２３'` thành `123`, `'1e4'` đi
    nguyên ra JSON tuyến thành `"1E+4"`."""
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem([_dong(202406, USD=x)], thang_dau=202406, nguon="bai-thu")
    cau = str(e.value)
    assert "202406" in cau and "USD" in cau and "khuôn" in cau, cau


@pytest.mark.parametrize("sai", [
    "000001",       # năm 0000 ⇒ cũ thành `lac = [1]`
    "199912",       # ngoài dải năm
    "210001",
    "２０２４06",    # năm chữ số TOÀN KHỔ, tháng ASCII ⇒ cũ nhận thành 202406
])
def test_R1_06_yyyymm_NGOAI_dai_nam_hay_chu_so_ngoai_ASCII_thi_NO(sai):
    """ⓒ `yyyymm` phải là `20YY` + tháng `01…12`, chữ số **ASCII** — khuôn cũ `\\d`
    nhận chữ số Unicode, và năm `0000` lọt thành tháng `1`."""
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem(_bon() + [_dong(sai)], thang_dau=202406, nguon="bai-thu")
    assert repr(sai) in str(e.value), str(e.value)


# ── C1-R1-02 · luật ĐƯỜNG nguồn tĩnh ──────────────────────────────────────────
#   ⭐⭐ `C5` (`WO-142`): `doc_tep` đã GỠ. Luật đường *(⛔ `..`, ⛔ tuyệt đối, ⛔
#   ngoài `tinh/`)* vẫn sống ở `fls/cau_hinh/nguon_tinh.giai` và được canh ở
#   `tests/cau_hinh/test_nguon_tinh.py::test_duong_SAI_thi_co_ly_do_MOT_dong` —
#   ⛔ bản chép ở đây.


# ══ Vòng sửa sau R2 (`KQ-078`) ══════════════════════════════════════════════
#
# ⛔⛔ Vì sao khối này tồn tại: R2 đột biến bản sao `59d4a39` *(bộ 150 bài offline)* —
#    **`d <= 0 → d < 0`** và **gỡ hẳn** chốt `> 0` của `_so` đều `150 passed`. Dưới cả
#    hai, tỷ giá **`'0'`** khớp khuôn `[0-9]+` ⇒ được NHẬN thành **0** — đúng lỗi AP
#    §3.2.4 *"tháng thiếu ⇒ `SUMIFS = 0` ⇒ mất số không báo"* mà bước này sinh ra để
#    chặn, chỉ là đi cửa khác *(một ô `0`, ⛔ phải một tháng thiếu)*. Vòng sửa R1 đặt
#    `<= 0` TRƯỚC khuôn, mà khuôn đã từ chối dấu `-` ⇒ việc **RIÊNG** của chốt chỉ còn
#    là số **0** — và grep `tests/` ca tỷ giá `"0"` = **0** chỗ *(R2 đo)*.
#    Mỗi bài dưới ghi **đột biến nó giết** *(log: `BG-076` mục "Vòng sửa sau R2")*.


# ── C1-R2-01 · biên `0` của tỷ giá *(NÊN SỬA)* ────────────────────────────────
@pytest.mark.parametrize("x", [
    "0", "00", "0.0", "0.00",      # chuỗi — 4 ca R2 đề xuất, chép nguyên
    0,                             # SỐ JSON `0` ⇒ `json.loads` trả `int` 0
    D("0.0"),                      # SỐ JSON `0.0` ⇒ `parse_float=Decimal` trả `Decimal`
], ids=["s0", "s00", "s0.0", "s0.00", "int0", "Decimal0.0"])
def test_R2_01_ty_gia_BANG_0_thi_NO_va_NOI_lon_hon_0(x):
    """Tỷ giá **đúng tại biên** `0` ⇒ `LoiFX`, câu nói tháng · cột · **lý do `> 0`**
    *(giết R2-f7 `d <= 0 → d < 0` và R2-f9 gỡ hẳn chốt)*.

    ⭐ Vì sao đòi chữ **`> 0`** *(⛔ chỉ tháng + cột như ca `-5`)*: luật phòng tái
      phạm `C1-R2-01` — *"ngưỡng của bộ kiểm phải có bài ĐÚNG TẠI BIÊN và bài phải hỏi
      LÝ DO có tên; ca xa biên có thể bị chốt khác bắt thay mà ⛔ ai thấy"*. Ca `-5`
      chính là ca ấy: gỡ chốt `> 0` thì khuôn bắt nó, bài vẫn xanh.
    ⭐ Hai ca SỐ *(`int` · `Decimal`)*: nguồn JSON ghi `"USD": 0` hay `0.0` *(⛔ nháy)*
      đi vào `_so` dưới dạng số, ⛔ chuỗi — cùng biên, lối vào khác.
    """
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem([_dong(202406, USD=x)], thang_dau=202406, nguon="bai-thu")
    cau = str(e.value)
    assert "202406" in cau and "USD" in cau and "> 0" in cau, cau
    assert "\n" not in cau, f"⛔ câu nổ phải MỘT dòng: {cau!r}"


def test_R2_01_ty_gia_0_DAU_PHAY_thap_phan_thi_NO_co_ten():
    """`'0,00'` *(số 0 viết kiểu dấu phẩy thập phân — ô sheet theo vùng VN/EU)* ⇒
    `LoiFX` có tên, ⛔ thành `0`.

    Khác bốn ca trên ở **LÝ DO**: `Decimal('0,00')` ⛔ đọc được ⇒ chốt đầu tiên
    *"⛔ phải số"* bắt, ⛔ tới `> 0`. Khuôn tỷ giá là thập phân ASCII **dấu chấm**
    *(`C1-R1-06` ⓑ — ảnh `DT2` 185/185 ô dùng dấu chấm)* ⇒ dấu phẩy ⛔ được chuẩn hoá
    ngầm thành dấu chấm. Bài ghim: câu nói giá trị **nguyên văn** + lý do *"phải số"*.
    """
    fx = _fx()
    with pytest.raises(fx.LoiFX) as e:
        fx.kiem([_dong(202406, USD="0,00")], thang_dau=202406, nguon="bai-thu")
    cau = str(e.value)
    assert "202406" in cau and "USD='0,00'" in cau and "phải số" in cau, cau


# ── C1-R2-02 · `strip()` là CỐ Ý — ghim *(GHI NHẬN — làm luôn)* ────────────────
def test_R2_02c_khoang_trang_DAU_CUOI_o_thang_va_ty_gia_duoc_NHAN_co_y():
    """`_thang`/`_so` cắt khoảng trắng đầu/cuối **có chủ đích** *(`BG-076` yếu #4 vòng
    R1: ô sheet hay dính dấu cách)* — R2 đột biến bỏ `strip()` ở từng hàm *(R2-f2 ·
    R2-f3)* ⇒ `150 passed`: một quyết định ⛔ bài nào ghim. Giết cả hai.

    ⚠ Hai mức khắt khe khác nhau, cố ý: luật ĐƯỜNG `nguon_tinh` thì ⛔ nhận khoảng
      trắng *(`fls/cau_hinh/nguon_tinh.py`)*. Ảnh thật `DT2`: **0/185** ô có khoảng
      trắng *(R2 đo)* ⇒ hôm nay 0 tác động; bài này chỉ để quyết định ⛔ đổi im lặng.
    """
    fx = _fx()
    b = fx.kiem([_dong(" 202406 ", USD=" 20001 ")], thang_dau=202406,
                nguon="bai-thu")
    assert [d.yyyymm for d in b.ky] == [202406], [d.yyyymm for d in b.ky]
    usd = b.ky[0].ty_gia["USD"]
    assert usd == D("20001") and str(usd) == "20001", repr(usd)
