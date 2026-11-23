"""`KQ-002 · F-1` — THÂN mà màn ghép gửi phải QUA được cửa THẬT.

⛔⛔⛔ **Lỗ đo được 01/10/2026** *(`fls-test`, đối chiếu hiện trạng)*.

Màn `SCR-F01` (`fls/web/tep/man_f01_ghep.js`) gửi:

    gan()    → POST /queue/{itl}/match    thân {pm_line_ids: [ma]}      ⛔ không `reason`
    bo_gan() → POST /queue/{itl}/unmatch  thân {}                       ⛔ không `reason`

Cửa thật (`fls/api/xu_ly.py::ghep` + `::bo_ghep`) gọi `_chu(yc.than, "reason")`
— **bắt buộc** ⇒ cả hai trả `400 FLS-BAD-REQUEST "thiếu reason"` **trước khi
chạm kho**. ⇒ Trên máy thật, hai nút `Gán` và `Bỏ gán` của màn ghép **⛔ không
bao giờ ghi được**.

⭐ Vì sao **⛔ không bài nào thấy**: mọi bài màn (`tests/web/test_b3_*`) thay
`FLS.ghi` bằng cửa GIẢ chỉ **đếm** lượt gọi — ⛔ không bài nào đưa thân ấy vào
hàm xử lý thật; còn mọi bài cửa (`tests/web/test_vong_f01_pg.py`) tự gửi
`{"reason": "x"}`. Hai nửa đều xanh, cái khớp giữa chúng ⛔ không ai đo — đúng
lớp `GAP-API-09/10` và *"khuôn thử tự nhét state"* (`11_BOI_CANH_TU_MEMORY` §6).
Cú UAT 01/10 (`itl_id 27728`) cũng đi đường **có** `reason` *(sổ vết ghi
"UAT 01/10 - thu duong ghi man ghep…")* ⇒ ⛔ không phải qua màn.

⭐ Bài này **⛔ không chọn bên sửa**: nó lấy thân **từ chính màn** *(chạy
`man_f01_ghep.js` thật trong khung node)* rồi đưa vào **hàm xử lý thật**. Màn
thêm `reason` → xanh. Cửa nới `reason` *(như `BA-07` v3.0 §4h ⓻ⓑ đã khai cho
`unmatch`)* → xanh. Chỉ khi **hai bên vẫn lệch** thì đỏ.

Cách đo "qua kiểm thân": gọi với `conn=None`. Cửa từ chối thân ⇒ `LoiCua`
`FLS-BAD-REQUEST` (ĐỎ). Thân qua ⇒ hàm đi tiếp tới kho và nổ `AttributeError`
trên `None` — ⛔ không mở kết nối nào, ⛔ không ghi gì.
"""
from __future__ import annotations

import pytest

from fls.api import xu_ly
from fls.repo.pham_vi import chi_nap_that
from tests.web.khung_node import _chay, can_node

VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

_LENH = ("{ma_lenh: 'PM9-1', so_tien: '1000.00', curr: 'USD',"
         " trang_thai: 'chua_gan', itl_da_gan: [5]}")
_UV = ("{itl_id: 5, amount: '1000.00', curr: 'USD', bac: 'ma',"
       " doc_no: 'FT1', doc_date: '2026-09-01'}")


def _than_man_gui(ham: str, duoi: str) -> dict:
    """Chạy `F01G.<ham>` THẬT, bắt lượt `FLS.ghi` có đường kết thúc `duoi`."""
    r = _chay(
        "F01G.ST.dong = [" + _LENH + "];"
        "F01G.ST.ung_vien = [" + _UV + "]; F01G.ST.ung_vien_chon = 0;"
        "_TRA['/queue/5/chum'] = {data: {itl_id: 5, dong_lenh: [],"
        " so_dong: 1, can_hoi: false}};"
        "try { await F01G." + ham + "(" + _LENH + "); } catch (e) {}"
        "return _GOI.filter(g => g[0] === 'ghi');",
        tep=TEP, vo=VO)
    ghi = [g for g in r if str(g[1]).endswith(duoi)]
    # ⛔ Đ5: khớp 0 hoặc >=2 lượt ghi là ⛔ KHÔNG ĐO ĐƯỢC ⇒ ĐỎ, ⛔ không xanh.
    assert len(ghi) == 1, f"⛔ không đo được: màn ghi {len(ghi)} lượt `{duoi}` — {r}"
    return ghi[0][2] or {}


def _qua_kiem_than(ham, than: dict) -> None:
    yc = xu_ly.YeuCau(conn=None, pv=chi_nap_that(), q={},
                      tham={"itl_id": "5"}, actor="fls-test@apero.vn",
                      than=than)
    try:
        ham(yc)
    except AttributeError:
        return            # ⭐ đã QUA kiểm thân, nổ ở chỗ chạm kho `None`
    except Exception as e:  # noqa: BLE001
        pytest.fail(
            f"⛔⛔ cửa THẬT từ chối đúng thân màn gửi {than!r}: "
            f"{type(e).__name__} {getattr(e, 'ma', '')} {e} — nút trên màn "
            "⛔ không bao giờ ghi được (KQ-002 F-1)")
    pytest.fail("⛔ không đo được: hàm ⛔ chạm tới kho `None` mà vẫn không nổ")


_LY_DO_DO = ("KQ-002 F-1 (01/10): cửa đòi `reason`, màn ⛔ gửi. ⛔ strict — "
             "khi DEV/BA vá, bài này XPASS ⇒ ĐỎ ⇒ fls-test gỡ dấu xfail.")


@can_node
# ✅ KQ-005 (fls-test 01/10): go dau xfail — WO-003 da va (ma 48fb68f), do lai do tren c1fb250 + xanh tren 4b2b2e8.
def test_than_GAN_cua_man_ghep_QUA_duoc_kiem_than_cua_match():
    than = _than_man_gui("gan", "/match")
    assert than.get("pm_line_ids") == ["PM9-1"], than   # ⭐ đúng đường, đúng lệnh
    _qua_kiem_than(xu_ly.ghep, than)


@can_node
# ✅ KQ-005 (fls-test 01/10): go dau xfail — WO-003 da va (ma 48fb68f), do lai do tren c1fb250 + xanh tren 4b2b2e8.
def test_than_BO_GAN_cua_man_ghep_QUA_duoc_kiem_than_cua_unmatch():
    """`BA-07` v3.3 §4h ⓻ⓑ: *"`reason` trong thân ⇒ TUỲ CHỌN — `QĐ-ITL-137`
    đã hoãn cột lý do ⇒ màn ⛔ không thu lý do nào"*."""
    than = _than_man_gui("bo_gan", "/unmatch")
    _qua_kiem_than(xu_ly.bo_ghep, than)


def test_DOI_CHUNG_than_CO_reason_thi_qua_kiem_than():
    """⭐ Chiều ngược (`Đ5`): bài trên đỏ phải VÌ thiếu `reason`, ⛔ vì khung
    đo hỏng. Thân có `reason` ⇒ phải qua."""
    _qua_kiem_than(xu_ly.ghep, {"pm_line_ids": ["PM9-1"], "reason": "x"})
    _qua_kiem_than(xu_ly.bo_ghep, {"reason": "x"})
