# -*- coding: utf-8 -*-
"""`WO-018` `AC-1` — ca xấu của `HOI-016` ⓑ dựng **từ CỬA THẬT** trên kho TEST,
rồi đưa **chính thân `GET /journal`** vào màn `F02` ⑦.

⛔⛔ **Ca xấu** *(`HOI-016` ⓑ, `fls-dev` 02/10 — sổ thật **0** dòng như thế
hôm nay, vì **0 / 8.387** dòng `fls_itl` có cột `*_thyt` khác `NULL`)*: một dòng
có `hd_thyt = 'HD-MAY'` *(máy gợi ý ở cột `*_thyt`)*; người gõ `hd = HD-NGUOI`
*(`force` + lý do)*. Trước `WO-018`, `ghi_but_toan` ghi
`fls_journal.value_source = truoc_khi_go(...)["value_source"]` = **nguồn TRƯỚC
khi gõ** = `may_goi_y` ⇒ màn `F02` ⑦ *(đọc `value_source` như "lớp của chính
dòng" — `BA-06` v4.9)* in **"gợi ý: HD-NGUOI" · "máy gợi ý · không đổi Final"**
cho một giá trị **NGƯỜI**, **là Final** — đúng lớp lỗi `KQ-007 F-1` muốn xoá,
theo chiều ngược.

⭐ `BA-05` v0.34 `DD-I15 ⓓe`: `value_source` = **lớp của CHÍNH dòng** *(ai nói
`value_after`)* ⇒ cú gõ của người ghi `sua_tay`. Màn ⛔ đổi một chữ — nhãn
đúng **vì cửa ghi đúng**.

⭐ Thân trả của `/adjust` *(`KetQuaGhi.value_source`)* **GIỮ** nghĩa *"nguồn
đang có trước khi gõ"* *(`US-025` — câu của modal `409` / `before-edit`)* —
bài này ghim luôn vế ấy, để ai "sửa cho đồng bộ" thì đỏ ngay ở đây chứ ⛔ phải
đợi `tests/api/test_cua_ghi_pg.py`.

⛔ Chiều ĐỎ *(đã chạy thật trên mã trước `WO-018` — `BG` của phiếu)*: trả
`ghi_tay.py` `ghi_but_toan` về `value_source=t["value_source"]` ⇒ nhật ký mang
`may_goi_y` ⇒ hàng in *"gợi ý: HD-NGUOI"* · *"máy gợi ý · không đổi Final"* ⇒ ĐỎ.
"""
from __future__ import annotations

import json

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.khung_node import _VE, _chay, can_node
from tests.web.test_drawer_f02 import _BAM, DONG_DAY
from tests.web.test_vong_f02_pg import V, _goi, du_lieu, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import (NHAN_MAY, NHAN_NGUOI,
                                                      _bang_nhat_ky)

pytestmark = pytest.mark.pg


def _dem_nhat_ky(itl_id: int) -> list[tuple]:
    with psycopg.connect(dsn_test()) as c:
        return c.execute(
            "SELECT jrn_id, field, value_after, value_source FROM fls_journal"
            " WHERE itl_id=%s ORDER BY jrn_id", (itl_id,)).fetchall()


@pytest.fixture()
def ca_xau(may, du_lieu):  # noqa: F811
    """Người `/adjust` đè `hd_thyt='HD-MAY'` bằng `HD-NGUOI` qua HTTP thật."""
    i = du_lieu["may"]
    truoc = _dem_nhat_ky(i)
    ok, r = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-NGUOI", "force": True,
                       "reason": "PM xác nhận lại — WO-018 AC-1"})
    assert ok == 200, r
    sau = _dem_nhat_ky(i)
    ok, nk = _goi(may, f"{V}/journal?itl_id={i}")
    assert ok == 200, nk
    return i, r["data"], truoc, sau, nk["data"]["rows"]


def test_AC1_cu_go_nguoi_tren_o_co_thyt__nhat_ky_ghi_SUA_TAY(ca_xau):
    """⭐ Đúng **1** dòng nhật ký mới, `value_source = 'sua_tay'`; thân trả
    `/adjust` vẫn nói nguồn **trước** khi gõ = `may_goi_y` *(`AC-4`)*."""
    _i, than, truoc, sau, _nk = ca_xau
    assert truoc == [], f"⛔ không đo được: dòng mới mà đã có nhật ký {truoc}"
    moi = sau[len(truoc):]
    assert len(moi) == 1, f"⛔ mong đúng 1 dòng nhật ký mới, thấy {moi}"
    _j, field, after, vs = moi[0]
    assert (field, after) == ("hd", "HD-NGUOI"), moi
    assert vs == "sua_tay", (
        f"⛔⛔ nhật ký của cú gõ NGƯỜI mang value_source={vs!r} — "
        "`BA-05` v0.34 `DD-I15 ⓓe`: lớp của CHÍNH dòng (người ⇒ sua_tay)")
    # ⭐ cửa ⛔ đổi: thân trả giữ "nguồn đang có trước khi gõ" (`US-025`)
    assert than["value_source"] == "may_goi_y", than
    assert than["value_before"] == "HD-MAY", than


@can_node
def test_AC1_man_F02_in_NGUOI_SUA__khong_in_goi_y(ca_xau):
    """Thân `GET /journal` thật ⇒ màn `F02` ⑦: hàng `hd` ô **thành** =
    `HD-NGUOI`, ô **nguồn** = *"người sửa"*; **0** hàng chứa *"gợi ý: HD-NGUOI"*."""
    _i, _than, _t, _s, nk = ca_xau
    assert len(nk) == 1, f"⛔ không đo được: cửa trả {len(nk)} dòng nhật ký"
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: %s}};
      HT.mo = () => ({dong(){}});
    """ % (json.dumps(DONG_DAY, ensure_ascii=False),
           json.dumps(nk, ensure_ascii=False, default=str))) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    hang = _bang_nhat_ky(ra)
    assert len(hang) == 1, hang
    h = hang[0]
    assert (h[1], h[3], h[5]) == ("hd", "HD-NGUOI", NHAN_NGUOI), h
    assert [x for x in hang if any("gợi ý: HD-NGUOI" in o for o in x)] == [], \
        "⛔⛔ màn gọi giá trị NGƯỜI (là Final) là 'gợi ý' của máy"
    assert NHAN_MAY not in {x[5] for x in hang}, hang
