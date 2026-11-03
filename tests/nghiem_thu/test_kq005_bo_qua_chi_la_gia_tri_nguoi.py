"""`KQ-005 · F-2` — `bo_qua` của bỏ ghép CHỈ được chứa giá trị NGƯỜI đã gõ.

⛔⛔ **Đo được 01/10/2026 trên kho TEST** *(`fls-test`, kịch bản phá `BG-004`
"Dev tự thấy còn yếu" mục 2)*.

Spec: `BA-06` v4.7 `:1174` — *"`bo_qua` = cái máy ⛔ KHÔNG rút **(người đã gõ
tay)** — **phải hiện**"*; `BA-09` v0.5 `SM-I06 F-8` + `BA-10` v0.6 `DT-I14` dòng
cuối: `bo_qua` khai **giá trị người**. Màn `F01` in nguyên mảng ấy dưới câu
*"⛔ KHÔNG đảo N ô — **người** đã gõ tay lên đó sau khi ghép"*
(`fls/web/tep/man_f01.js` `_bao_bo_ghep`).

Mã (`fls/repo/ghi_tay.py::bo_moi_noi`) còn bỏ vào `bo_qua` **mọi** bút toán
gắn sự kiện `match` đã bị đảo từ lượt trước ⇒ đúng đường mà `QĐ-ITL-69` khuyên
*("muốn đổi một dòng lệnh: bỏ cả chùm rồi ghép lại")*:

    ghép → bỏ ghép → ghép lại → bỏ ghép   (⛔ AI gõ tay ô nào)
    ⇒ bo_qua = [cdt1, hd]  ⇒ màn: "⛔ KHÔNG đảo 2 ô — người đã gõ tay lên đó"

— một câu **bịa** về việc người đã làm, trên sổ chỉ 2–3 kế toán dùng
*(`QĐ-ITL-27`: kiểm soát nằm trong máy — ⛔ bịa)*. ⚠ Có **từ trước** `WO-003`
*(Dev tự khai, `BG-004` mục 2)* — nhưng `WO-003` làm ghép lại sau bỏ thành
đường thường ngày *(màn nay ghi được)*.
"""
from __future__ import annotations

import pytest

from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import chi_nap_that
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import ACTOR, _mot_dong, conn  # noqa: F401

pytestmark = pytest.mark.pg


# ✅ `KQ-007` (01/10 tối, `fls-test`): GỠ dấu `xfail` — đỏ trên `38a6b08`/`48fb68f`
#   (KQ-005), xanh trên `5fbc29c` (`BG-006`), và ĐỎ LẠI đúng thông điệp khi đột
#   biến mã mới về phép chọn qua khung xem / `bo_qua` từ bút toán máy.
def test_ghep_BO_ghep_lai_BO__khong_ai_go_tay__bo_qua_RONG(conn):  # noqa: F811
    _run, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR)
    gt.bo_moi_noi(conn, pv, i, actor=ACTOR)
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR)
    ra = gt.bo_moi_noi(conn, pv, i, actor=ACTOR)

    assert len(ra["but_toan_dao"]) == 2, f"⛔ không đo được: {ra['but_toan_dao']}"
    nguoi = conn.execute("SELECT count(*) FROM fls_sua_tay WHERE itl_id=%s",
                         (i,)).fetchone()[0]
    assert nguoi == 0, "⛔ không đo được: dòng có giá trị người"
    assert ra["bo_qua"] == [], (
        f"⛔⛔ ⛔ ai gõ tay mà `bo_qua` có {len(ra['bo_qua'])} mục "
        f"{[(x['field'], x.get('nguon')) for x in ra['bo_qua']]} — màn F01 sẽ in "
        "'người đã gõ tay lên đó'")


def test_DOI_CHUNG_nguoi_go_THAT_thi_bo_qua_CO(conn):  # noqa: F811
    """⭐ Chiều ngược (`Đ5`): có người gõ thật ⇒ `bo_qua` PHẢI có ô ấy."""
    _run, i, ma = _mot_dong(conn)
    pv = chi_nap_that()
    gt.ghep_lenh(conn, pv, i, [ma], actor=ACTOR)
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-NGUOI", actor="kt2@apero.vn",
                    reason="go lai")
    ra = gt.bo_moi_noi(conn, pv, i, actor=ACTOR)
    assert [x["field"] for x in ra["bo_qua"] if x.get("nguon") == "sua_tay"] == ["hd"]
