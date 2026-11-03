"""`KQ-002 · F-3` — màn ghép ĐANG TẢI ⛔ không được nói *"Hàng chờ đã sạch."*

⛔⛔⛔ **Đo được 01/10/2026 trên máy THẬT** *(`http://127.0.0.1:8088/`, chỉ đọc,
Chrome headless qua CDP, mở tab `man-ghep`)*:

    300ms · 800ms · 1500ms · 2500ms   "0 dòng (⛔ đã chạm trần 3000)"  +  "Hàng chờ đã sạch."
    4000ms trở đi                     "736 dòng"

⇒ Suốt **~2,5–4 giây** đầu, trước **736** lệnh chi đang chờ, màn nói hàng chờ
**đã sạch** — đúng câu sai mà `B3` đã "vá" *(chú thích `man_f01_ghep.js:620`,
`ung_dung.js:80`)*. Và nó còn tự mâu thuẫn: `0 dòng` mà *"đã chạm trần 3000"*.

⭐ Gốc: `mo_man()` và `doi_chip()` gọi `ve()` **TRƯỚC** khi `tai_danh_sach()`
kịp đặt `ST.dang_tai = true` ⇒ lượt vẽ đầu thấy `dong=[]`, `dang_tai=false`,
`het=false` ⇒ nhánh *"đã sạch"* + *"chạm trần"*. Nhánh `Đang hỏi sổ…`
(`man_f01_ghep.js:1127`) có thật nhưng ⛔ **không lượt vẽ nào tới được nó**:
lượt vẽ kế tiếp chỉ chạy **sau** khi tải xong.

⭐ Vì sao bộ cũ xanh: cửa giả của `khung_node` trả `Promise.resolve` **ngay**,
nên bài chỉ nhìn được trạng thái **sau** tải. Bài này cho cửa **⛔ không bao
giờ trả lời** — đúng chế độ `?gia_lap=tai` của sản phẩm — rồi nhìn màn.
"""
from __future__ import annotations

import pytest

from tests.web.khung_node import _chay, can_node

VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

_TREO = ("FLS.doc = function (d) { _GOI.push(['doc', d]);"
         " return new Promise(() => {}); };")
_NHIN = ("await new Promise(r => setTimeout(r, 30));"
         "return {chu: document.querySelector('#ghep-goc').textContent,"
         "        goi: _GOI.filter(g => g[0] === 'doc').length,"
         "        dang_tai: F01G.ST.dang_tai};")

_LY_DO = ("KQ-002 F-3 (01/10): ve() chạy trước khi đặt dang_tai. ⛔ strict — "
          "khi DEV vá, XPASS ⇒ ĐỎ ⇒ fls-test gỡ dấu xfail.")


def _kiem(r: dict, cau_sai: str) -> None:
    # ⛔ Đ3/Đ5: màn PHẢI đang hỏi thật — ⛔ không gọi cửa nào thì bài vô nghĩa.
    assert r["goi"] >= 1 and r["dang_tai"] is True, f"⛔ không đo được: {r}"
    assert cau_sai not in r["chu"], (
        f"⛔⛔ màn ĐANG TẢI mà nói «{cau_sai}» — {r['chu'][:200]!r}")
    assert "chạm trần" not in r["chu"], f"⛔ '0 dòng' mà 'đã chạm trần': {r['chu'][:200]!r}"
    assert "Đang hỏi sổ" in r["chu"], f"⛔ không có dấu đang tải: {r['chu'][:200]!r}"


@can_node
# ✅ KQ-005 (fls-test 01/10): go dau xfail — WO-003 da va (ma 48fb68f), do lai do tren c1fb250 + xanh tren 4b2b2e8.
def test_MO_MAN_khi_cua_chua_tra_loi_KHONG_noi_hang_cho_da_sach():
    r = _chay(_TREO + " F01G.mo_man();" + _NHIN, tep=TEP, vo=VO)
    _kiem(r, "đã sạch")


@can_node
# ✅ KQ-005 (fls-test 01/10): go dau xfail — WO-003 da va (ma 48fb68f), do lai do tren c1fb250 + xanh tren 4b2b2e8.
def test_DOI_CHIP_khi_cua_chua_tra_loi_KHONG_noi_khong_co_dong_nao():
    r = _chay(_TREO + " F01G.doi_chip('khong_gan_duoc');" + _NHIN,
              tep=TEP, vo=VO)
    _kiem(r, "Không có dòng nào")
