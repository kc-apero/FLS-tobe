"""`KQ-005 · F-1` — bỏ ghép phải đảo **MỌI** gợi ý gắn sự kiện `match` của dòng,
kể cả gợi ý đã bị một gợi ý MỚI HƠN đè lên *(gợi ý chồng)*.

⛔⛔⛔ **Đo được 01/10/2026 trên kho TEST** *(`fls-test`, kịch bản phá `BG-004`
"Dev tự thấy còn yếu" mục 1)*.

Khung xem `fls_may_goi_y` *(migration `0025`)* = gợi ý **mới nhất chưa đảo** của
ô. `bo_moi_noi` *(`fls/repo/ghi_tay.py`, `WO-003`)* lọc tập *"còn hiệu lực"*
bằng **chính khung xem ấy** ⇒ chỉ đảo **lớp trên cùng**. Lớp dưới — một gợi ý
của một sự kiện `match` khác, ⛔ đảo — **nổi lên lại** trong `fls_may_goi_y`
**sau** khi dòng đã ⛔ còn mối nối nào:

    ghép TAY (hd=HD-CU)  → tools/goi_y_lai.py --ghi sau khi ảnh PM đổi hd
    (ghi_goi_y_may: hd=HD-MOI, value_before=HD-CU, sự kiện `match` MỚI của may@fls)
    → bỏ ghép  ⇒ đảo HD-MOI + cdt1;  HD-CU ⛔ đảo  ⇒  fls_may_goi_y = {hd: HD-CU}
      với 0 mối nối hiệu lực = gợi ý MỒ CÔI — đúng thứ `WO-003 AC-7` cấm.

⭐ Dev đã nghi đúng chỗ này *(`BG-004` mục 1)* nhưng kết luận *"đường mới ⛔ sinh
ra ca này"* — **sai**: `tools/goi_y_lai.py` đọc mọi mối nối **còn hiệu lực**
*(`fls_moi_noi`, kể cả `hinh='T'`)* với ảnh PM **mới nhất**, và luật
`loc_goi_y` *(`DT-I14` nhánh 3: gợi ý đang có ≠ `v` ⇒ GHI)* chồng một lớp lên.
Đường máy thuần *(hai lần `ghi_goi_y_may` trên một dòng `hinh='A'`)* cũng ra y hệt.

Kho THẬT hôm nay *(đo 01/10, chỉ đọc)*: ô có ≥ 2 lớp gợi ý chưa đảo = **0** /
`4.424` gợi ý ⇒ chưa ai dính; lỗ mở ra ở lần đầu `goi_y_lai --ghi` sau khi một
dòng lệnh đổi `hd`/`cdt1`.

Căn cứ: `BA-09` v0.5 `SM-I06` *(unmatch: "**đảo** mọi gợi ý còn hiệu lực gắn sự
kiện `match` của dòng")* · `WO-003 AC-7` *("`fls_may_goi_y` của dòng về **0**")*
⟷ `BA-10` v0.6 `DT-I14` nhánh 7 *("bị gợi ý mới hơn đè ⇒ ⛔ làm gì")* — chính
nhánh 7 + ngữ nghĩa "lớp trên cùng" của khung xem đẻ ra lỗ ⇒ gửi cả `DEV` lẫn `BA`.
"""
from __future__ import annotations

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.may_ghep import ghi_goi_y_may
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import (ACTOR, D, _mot_dong,  # noqa: F401
                                                        conn)

pytestmark = pytest.mark.pg

_LY_DO = ("KQ-005 F-1 (01/10): bo ghep chi dao LOP TREN CUNG cua goi y chong — "
          "lop duoi noi len thanh goi y mo coi. ⛔ strict — khi DEV/BA va, "
          "XPASS ⇒ ĐỎ ⇒ fls-test go dau xfail.")


def _goi_y(conn, i: int) -> dict:
    return dict(conn.execute("SELECT field, value_after FROM fls_may_goi_y"
                             " WHERE itl_id=%s", (i,)).fetchall())


def _moi_noi(conn, i: int) -> int:
    return conn.execute("SELECT count(*) FROM fls_moi_noi WHERE itl_id=%s",
                        (i,)).fetchone()[0]


# ✅ `KQ-007` (01/10 tối, `fls-test`): GỠ dấu `xfail` — đỏ trên `38a6b08`/`48fb68f`
#   (KQ-005), xanh trên `5fbc29c` (`BG-006`), và ĐỎ LẠI đúng thông điệp khi đột
#   biến mã mới về phép chọn qua khung xem / `bo_qua` từ bút toán máy.
def test_ghep_TAY_roi_goi_y_lai_CHONG__bo_ghep_KHONG_de_goi_y_mo_coi(conn):  # noqa: F811
    _run, i, ma = _mot_dong(conn, hd="HD-CU", cdt1="CDT-1")
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR)
    # ⭐ đúng lời gọi của `tools/goi_y_lai.py:82` sau khi ảnh PM mới đổi `hd`
    g = ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-MOI",
                                             "cdt1": "CDT-1"}])
    assert [x["field"] for x in g["but_toan"]] == ["hd"], \
        f"⛔ không đo được: ⛔ dựng được gợi ý chồng — {g}"
    assert _goi_y(conn, i) == {"hd": "HD-MOI", "cdt1": "CDT-1"}

    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR)

    assert _moi_noi(conn, i) == 0, "⛔ không đo được: bỏ ghép ⛔ bỏ hết mối nối"
    con = _goi_y(conn, i)
    assert con == {}, (
        f"⛔⛔ bỏ ghép xong, dòng ⛔ còn mối nối nào mà `fls_may_goi_y` vẫn "
        f"còn {con} — gợi ý lớp dưới NỔI LÊN LẠI (mồ côi)")


# ✅ `KQ-007` (01/10 tối, `fls-test`): GỠ dấu `xfail` — đỏ trên `38a6b08`/`48fb68f`
#   (KQ-005), xanh trên `5fbc29c` (`BG-006`), và ĐỎ LẠI đúng thông điệp khi đột
#   biến mã mới về phép chọn qua khung xem / `bo_qua` từ bút toán máy.
def test_dong_MAY_ghep_goi_y_CHONG_hai_lop__bo_ghep_ve_0(conn):  # noqa: F811
    run, i, ma = _mot_dong(conn, hd="HD-CU", cdt1="CDT-1")
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)",
                 (i, ma, D("5000000.00"), run))
    for hd in ("HD-CU", "HD-MOI"):
        ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": hd,
                                             "cdt1": "CDT-1"}], run_pm=run)
    assert _goi_y(conn, i) == {"hd": "HD-MOI", "cdt1": "CDT-1"}, \
        "⛔ không đo được: ⛔ dựng được gợi ý chồng"

    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR)

    assert _moi_noi(conn, i) == 0
    con = _goi_y(conn, i)
    assert con == {}, f"⛔⛔ gợi ý MỒ CÔI sau bỏ ghép: {con}"


def test_DOI_CHUNG_goi_y_MOT_lop__bo_ghep_ve_0(conn):  # noqa: F811
    """⭐ Chiều ngược (`Đ5`): cùng khung đo, ⛔ chồng lớp ⇒ phải về 0 — bài trên
    đỏ VÌ lớp chồng, ⛔ vì khung đo hỏng."""
    _run, i, ma = _mot_dong(conn, hd="HD-CU", cdt1="CDT-1")
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR)
    assert _goi_y(conn, i) == {"hd": "HD-CU", "cdt1": "CDT-1"}
    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR)
    assert _moi_noi(conn, i) == 0 and _goi_y(conn, i) == {}
