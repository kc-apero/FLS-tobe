"""`G-MOD-3` — *"đủ trường như ggsheet"* thành **một phép trừ tập hợp**.

⭐⭐⭐ Owner đòi *"đủ các trường như trong ggsheet"* cho màn ghép. Câu ấy
**⛔ không audit được** khi nó là một **cảm giác**; nó đo được khi ta khai
**VŨ TRỤ** rồi **trừ** đi.

    vũ trụ = 28 cột CÓ TÊN của `PM_Unpivot`
           = `PM_COT` (14 đặt kiểu)
           + `PM_COT_RIENG_TU` (1 cấm)
           + `PM_COT_CHUA_DAT_KIEU` (13, mỗi cái một LÝ DO)

⛔⛔ **Một cột ⛔ không nằm trong rổ nào là một LỖ IM LẶNG.** Đó đúng cái đã
xảy ra: `tho` mới thêm 11/09, và trước đó **20 cột biến mất ngay lúc đọc** —
⛔ không ai biết chúng tồn tại.

⇒ Nguồn thêm một cột ⇒ cổng **ĐỎ** cho tới khi có người **phân loại và ghi
  lý do**. ⛔ Đây ⛔ không phải danh sách *"sẽ làm sau"*: nó là danh sách
  **đã nhìn thấy và đã quyết**.

⛔ **Vũ trụ đo từ KHO, ⛔ không gõ tay** *(`Đ1`: một con số gõ tay già theo
  giờ)*. Tệp `.xlsx` nguồn nằm **ngoài repo** và bị `gitignore`, nên cổng
  ⛔ không đọc nó — nó đọc **khoá `tho` thật** cộng bản cấm.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.adapters.pm_join import (PM_COT, PM_COT_CHUA_DAT_KIEU,
                                  PM_COT_RIENG_TU, PM_TIEU_DE_MONG_DOI)
from fls.db.kho import dsn_that

# ⛔ Đo 17/09 trên `A _ PAY100 _ PM11 Entry Data` ▸ `PM_Unpivot` hàng 2.
SO_COT_CO_TEN = 28


@pytest.fixture(scope="module")
def khoa_tho() -> set[str]:
    """Mọi khoá `tho` CÓ THẬT trong kho."""
    with psycopg.connect(dsn_that(), connect_timeout=5) as c:
        ra = {r[0] for r in c.execute(
            "select distinct k from fls_pm_line, lateral json_object_keys(tho) k")}
    if not ra:
        pytest.fail("⛔ 0 khoá `tho` — phép phân hoạch sẽ XANH trên TẬP RỖNG "
                    "(`Đ3`: mẫu số `0` là KẾT QUẢ, ⛔ không phải nền)")
    return ra


def _dat_kieu() -> set[str]:
    """Tên cột nguồn mà `PM_COT` đang đọc — ⛔ suy từ bản khai, ⛔ không gõ."""
    return {PM_TIEU_DE_MONG_DOI[v] for v in PM_COT.values()}


def _vu_tru(khoa_tho: set[str]) -> set[str]:
    # ⛔ Bản CẤM ⛔ không bao giờ vào kho, nên nó ⛔ không có trong `tho` —
    #   phải cộng lại, ⛔ không thì vũ trụ thiếu đúng cái ta cố tình bỏ.
    return khoa_tho | set(PM_COT_RIENG_TU)


def test_vu_tru_dung_28_cot_co_ten(khoa_tho):
    n = len(_vu_tru(khoa_tho))
    assert n == SO_COT_CO_TEN, (
        f"⛔ vũ trụ đo được {n} cột, bản khai nói {SO_COT_CO_TEN}. "
        "Nguồn đổi hình ⇒ đo lại rồi sửa **cả hai** chỗ, "
        "⛔ đừng sửa một chỗ cho vừa")


def test_G_MOD_3_ba_ro_PHAN_HOACH_dung_vu_tru(khoa_tho):
    """⭐⭐⭐ Cổng chính: ⛔ không thừa, ⛔ không thiếu, ⛔ không chồng."""
    vu_tru = _vu_tru(khoa_tho)
    dat, cam, chua = _dat_kieu(), set(PM_COT_RIENG_TU), set(PM_COT_CHUA_DAT_KIEU)

    ro_roi = sorted(vu_tru - dat - cam - chua)
    assert not ro_roi, (
        f"⛔⛔ {len(ro_roi)} cột của nguồn ⛔ KHÔNG nằm trong rổ nào — "
        f"chúng đang vào `tho` rồi nằm im: {ro_roi}. "
        "⇒ Phân loại và **ghi lý do** vào `PM_COT_CHUA_DAT_KIEU`, "
        "hoặc đọc chúng vào `PM_COT`.")

    ma_khong_co = sorted((dat | chua) - vu_tru)
    assert not ma_khong_co, (
        f"⛔ bản khai nhắc {len(ma_khong_co)} cột mà kho ⛔ KHÔNG có: "
        f"{ma_khong_co} — nguồn đã bỏ cột, hay ta gõ sai tên?")

    for a, b, ten in ((dat, cam, "đặt kiểu ↔ cấm"),
                      (dat, chua, "đặt kiểu ↔ chưa đặt kiểu"),
                      (cam, chua, "cấm ↔ chưa đặt kiểu")):
        assert not (a & b), f"⛔ hai rổ CHỒNG nhau ({ten}): {sorted(a & b)}"


def test_moi_truong_CHUA_dat_kieu_deu_co_LY_DO():
    """⛔ Một trường ⛔ không lý do là *"sẽ làm sau"* đội lốt một quyết định."""
    thieu = sorted(k for k, v in PM_COT_CHUA_DAT_KIEU.items()
                   if len((v or "").strip()) < 20)
    assert not thieu, (
        f"⛔ {len(thieu)} trường khai mà lý do rỗng/quá ngắn: {thieu}")


def test_ban_CAM_that_su_KHONG_co_trong_kho(khoa_tho):
    """⛔ `PM_COT_RIENG_TU` là một lời hứa — bài này ĐO nó, ⛔ không tin nó."""
    lot = sorted(set(PM_COT_RIENG_TU) & khoa_tho)
    assert not lot, (
        f"⛔⛔ BẢN CẤM ĐÃ LỌT VÀO KHO: {lot}. Đây là dữ liệu người — "
        "xem `pm_join.PM_COT_RIENG_TU` và `.gitignore`")


def test_con_so_DA_DAT_KIEU_noi_dung_no_dem_gi():
    """⭐ `Đ4` — một con số phải nói NÓ ĐẾM GÌ.

    `14` ở đây là **số CỘT NGUỒN đang được đọc**, ⛔ không phải số trường của
    `DongPM` *(16)*, ⛔ không phải số cột của `fls_pm_line` *(18)*. Ba con số
    khác nhau, và trộn chúng là đúng lớp lỗi `52 = 38+14` vs `24+28`.
    """
    assert len(_dat_kieu()) == len(PM_COT) == 14
