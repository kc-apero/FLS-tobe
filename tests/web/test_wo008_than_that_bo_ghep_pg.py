# -*- coding: utf-8 -*-
"""`WO-008` `AC-2` — dòng **B** của `KQ-007` dựng **từ CỬA THẬT** trên kho TEST,
rồi đưa **chính thân trả** vào ba chỗ màn của phiếu.

⛔⛔ **Vì sao phải có bài này ngoài `test_wo008_chu_man_sau_bo_ghep.py`.** Bài
DOM kia đút sẵn bốn dòng nhật ký và một thân `unmatch` chép tay. `11` §6 đã ghi
một lỗi thật cùng lớp: *"khuôn thử tự nhét state che mất chỗ màn ⛔ gọi cửa"*
*(màn `B3` sống trọn chặng mà ⛔ gọi cửa)*. Ở đây cái có thể lệch là **tên
trường** *(`value_source` hay `nguon`? `field` hay `truong`?)* và **hình dạng**
bản đảo *(`value_after` là `null` hay `''`?)* — khuôn tự nhét trả đúng cái người
viết bài **tưởng**, cửa thật trả cái nó trả.

Kịch bản *(`WO-008` Phạm vi — "ghép → `ghi_goi_y_may` chồng lớp → người
`/adjust` → bỏ ghép")*, mọi bước GHI đi qua **HTTP thật** trừ lớp gợi ý máy
*(⛔ có cửa — nhịp máy gọi thẳng `ghi_goi_y_may`, đúng như kho thật)*:

  ① `POST /queue/{id}/match`         — ghép tay ⇒ 2 gợi ý `hd`·`cdt1`
  ② `ghi_goi_y_may` lớp A            — 2 gợi ý chồng `HD-B`·`C-2`
  ③ `POST /ledger/{id}/adjust` `hd`  — NGƯỜI gõ `HD-K7B` *(force)*
  ④ `ghi_goi_y_may` lớp B            — người đã chốt `hd` ⇒ chỉ `cdt1`
  ⑤ `POST /queue/{id}/unmatch`       — bỏ ghép
  ⑥ `GET /journal?itl_id=`           — nhật ký đưa vào màn `F02` ⑦
"""
from __future__ import annotations

import json

import pytest

from fls.repo.may_ghep import ghi_goi_y_may
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import _mot_dong, conn  # noqa: F401
from tests.web.khung_node import _VE, can_node, _chay
from tests.web.test_drawer_f02 import _BAM, DONG_DAY
from tests.web.test_vong_f02_pg import V, _goi, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import (NHAN_MAY, NHAN_NGUOI, RUT,
                                                      _bang_nhat_ky, _bo_gan,
                                                      _hop_bo_ghep, _not_dao)

pytestmark = pytest.mark.pg


@pytest.fixture()
def dong_B(conn, may):  # noqa: F811
    """Dựng dòng B qua cửa thật; trả `(itl_id, than_unmatch, nhat_ky, so_dao)`."""
    _r, i, ma = _mot_dong(conn, hd="HD-A", cdt1="C-1")
    ok, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": [ma]})
    assert ok == 200, r
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-B",
                                         "cdt1": "C-2"}])
    ok, r = _goi(may, f"{V}/ledger/{i}/adjust", pt="POST",
                 than={"field": "hd", "value": "HD-K7B", "reason": "go tay",
                       "force": True})
    assert ok == 200, r
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-C",
                                         "cdt1": "C-3"}])
    ok, bo = _goi(may, f"{V}/queue/{i}/unmatch", pt="POST", than={})
    assert ok == 200, bo
    ok, nk = _goi(may, f"{V}/journal?itl_id={i}")
    assert ok == 200, nk
    # mẫu số (`Đ3`): số BẢN ĐẢO của dòng trong bảng gốc
    so_dao = conn.execute("SELECT count(*) FROM fls_adjustment WHERE itl_id=%s"
                          " AND reversal_of IS NOT NULL", (i,)).fetchone()[0]
    return i, bo["data"], nk["data"]["rows"], so_dao


@can_node
def test_AC2_nhat_ky_THAT_cua_dong_B__moi_ban_dao_may_in_RUT_GOI_Y(dong_B):
    """⭐⭐ Mọi hàng `may_goi_y` có `value_after` rỗng in *"rút gợi ý"*; **0**
    hàng `may_goi_y` in ô thành trống; hàng người gõ in giá trị người.

    ⛔ Chiều ĐỎ *(như `AC-1`)*: ô thành về `TP.chu(x.value_after)` ⇒ đếm
    *"rút gợi ý"* = 0 ≠ số bản đảo ⇒ ĐỎ.
    """
    _i, _bo, nk, so_dao = dong_B
    assert so_dao >= 4, f"⛔ không đo được: dòng B chỉ có {so_dao} bản đảo"
    # hình dạng cửa thật — tên trường màn đọc (`AUD-1`)
    rut_kho = [x for x in nk if x["value_source"] == "may_goi_y"
               and x["value_after"] in (None, "")]
    assert len(rut_kho) == so_dao, (
        f"⛔ nhật ký có {len(rut_kho)} dòng rút gợi ý, bảng gốc {so_dao} bản đảo")

    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: %s}};
      HT.mo = () => ({dong(){}});
    """ % (json.dumps(DONG_DAY, ensure_ascii=False),
           json.dumps(nk, ensure_ascii=False, default=str))) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    hang = _bang_nhat_ky(ra)
    assert len(hang) == len(nk), (len(hang), len(nk))
    may_ = [h for h in hang if h[5] == NHAN_MAY]
    assert sum(h[3] == RUT for h in may_) == so_dao, [h[3] for h in may_]
    assert [h for h in may_ if h[3] == ""] == [], \
        "⛔⛔ hàng máy gợi ý in ô thành TRỐNG — người đọc tưởng ô bị xoá"
    # ⭐ Hàng NGƯỜI gõ in **giá trị người**, ⛔ "gợi ý:", ⛔ nhãn máy.
    # ⚠⚠ Đo thật *(`HOI-016` ⓑ)*: TRƯỚC `WO-018` `fls_journal.value_source`
    #   của một cú `/adjust` = nguồn của giá trị **TRƯỚC** khi gõ
    #   *(`ghi_tay.truoc_khi_go` — `nguon` · `may_goi_y` *(cột `*_thyt`)* ·
    #   `sua_tay` · `UNMAPPED`)*, ⛔ phải "ai ghi dòng này". Dòng B: ô `hd`
    #   trước khi gõ ⛔ có gì ở ba lớp `truoc_khi_go` đọc *(gợi ý của phép ghép
    #   nằm ở `fls_may_goi_y`, ⛔ ở `hd_thyt`)* ⇒ `UNMAPPED`, in nguyên mã.
    #   Bài từng GHIM `("HD-K7B", "UNMAPPED")` để ai đổi luật ghi thì phải đọc
    #   `HOI-016` — và `TL-016` đổi đúng luật ấy.
    # ⭐⭐ `WO-018` *(`BA-05` v0.34 `DD-I15 ⓓe`)*: nhật ký mang **lớp của chính
    #   dòng** ⇒ cú gõ người = `sua_tay` ⇒ màn in *"người sửa"*. Lo gốc của bài
    #   GIỮ: hàng người in **giá trị người** *(`HD-K7B`)*, ⛔ "gợi ý:", ⛔ nhãn
    #   máy, và nhãn *"người sửa"* xuất hiện **đúng 1** lần *(dòng B chỉ có
    #   MỘT cú gõ người — nhãn ấy ở hàng nào khác là bịa việc người làm)*.
    nguoi = [h for h in hang if h[1] == "hd" and h[5] != NHAN_MAY]
    assert [(h[3], h[5]) for h in nguoi] == [("HD-K7B", NHAN_NGUOI)], nguoi
    assert [h[5] for h in hang].count(NHAN_NGUOI) == 1, \
        "⛔ dòng B có đúng MỘT cú gõ người — nhãn 'người sửa' phải đúng 1 hàng"


@can_node
def test_AC3_than_unmatch_THAT_dong_B__hop_noi_2_o(dong_B):
    """Thân `unmatch` thật ⇒ hộp *"Đã bỏ ghép"*: **2 ô**, mỗi tên ô đúng 1 lần,
    đuôi *"M bút toán"* với M = `len(but_toan_dao)` > 2."""
    _i, bo, _nk, so_dao = dong_B
    dao = bo["but_toan_dao"]
    assert len(dao) == so_dao and len(dao) > 2, dao
    assert {x["field"] for x in dao} == {"hd", "cdt1"}, dao
    cau = _not_dao(_hop_bo_ghep(bo)[0]["b"])
    assert "2 ô" in cau and f"{len(dao)} bút toán" in cau, cau
    assert cau.count("cdt1") == 1 and cau.count("hd") == 1, cau


@can_node
def test_AC4_than_unmatch_THAT_dong_B__man_ghep_bao_bo_qua(dong_B):
    """Thân thật mang `bo_qua=[hd · HD-K7B]` ⇒ màn ghép mở **1** hộp, nút duy
    nhất `Đã hiểu`, chứa `hd` và `HD-K7B`."""
    _i, bo, _nk, _s = dong_B
    assert [(x["field"], x["value_after"]) for x in bo["bo_qua"]] == \
        [("hd", "HD-K7B")], bo["bo_qua"]
    r = _bo_gan(bo)
    assert r["unmatch"] == 1 and len(r["hop"]) == 1, r
    h = r["hop"][0]
    assert h["n"] == ["Đã hiểu"] and "HD-K7B" in h["b"], h
