# -*- coding: utf-8 -*-
"""`KQ-061` — kiểm `WO-023` *(`BG-052`…`BG-059`)*: phát hiện `F-1`.

⛔⛔ `BA-06` **v4.23** `ⓕ3`: lượt GHI quá hạn `30 s` ⇒ `FLS-HET-GIO`, và màn
**⛔ được** nói *"chưa xảy ra"* — lượt ghi **có thể đã** vào sổ. `fls-ba` đếm
nơi in tiền tố *"… chưa xảy ra — "* ⇒ **2** *(`F01G` `Gán` · `Bỏ gán`)*. Phép
đếm ấy đếm **một cách viết**; màn `F02` nói **cùng một khẳng định bằng chữ
khác** ở lô lưu *(`man_f02.js::_bay` → `_bao_hong` + dòng trạng thái)*:
*"1 ô dưới đây CHƯA vào sổ"* · *"1 ô CHƯA vào sổ"* — cho cả ô mà cửa ghi
**hết giờ**.

Đo thật *(`KQ-061`, Chrome 154 headless trên **8099 kho TEST**, hạn chờ THẬT
`30 s`, CDP `Fetch` giữ `POST /ledger/1/adjust`)*: sau **32,5 s** hộp *"Lô lưu
DỪNG giữa chừng"* in **cả hai** câu cạnh nhau — *"Máy chưa trả lời sau 30 giây
— chưa biết lượt ghi đã vào sổ hay chưa."* rồi *"1 ô dưới đây CHƯA vào sổ —
… dòng 1 · ô hd → "HD-KQ061-T""*; thả lượt ⇒ cửa trả **`200`**, kho TEST có
bút toán `adj_id 4312` *(ô **đã** vào sổ)*. Gõ lại / `Thử lại` ⇒ phép hỏi lại
cửa thấy `tay = HD-KQ061-T` ≠ ảnh lúc tải ⇒ hộp *"Ô này đã có NGƯỜI KHÁC gõ … Máy
chưa ghi gì cả"* cho **chính** giá trị người vừa gõ *(⛔ ghi đôi — phép hỏi lại
chặn được)*.

Bài dưới dựng ca ấy trên **`man_f02.js` THẬT** *(khuôn `test_lo_luu_f02.py`
ca ⓑ)*, chỉ thay lớp lỗi: ô thứ hai ném `FLS-HET-GIO` *(chính `LoiCua` mà
`goi_cua.js::goi` ném khi quá `HAN_CHO.ghi_ms`)*. Mẫu số *(`Đ3`)*: cùng ca với
`FLS-MAT-KET-NOI` ⇒ câu *"CHƯA vào sổ"* **có** *(bài đo được chữ ấy)*.

⛔ Chữ đúng là việc của `fls-ba` *(khuôn chung `ⓕ3` cho lô lưu `F02`)* — bài chỉ
đòi điều luật đã nói: với `FLS-HET-GIO`, màn **⛔** khẳng định ô **chưa** vào sổ.
"""
from __future__ import annotations

import pytest

from tests.web.khung_node import _VE_GO as _VE, _chay, can_node

#: Hai ô của dòng 101 / 102 vào hàng chờ *(khuôn `test_lo_luu_f02._HAI_O`)*.
_HAI_O = _VE + """
  F02.ST.ly_do = 'đối soát tháng 8';
  const h = luoi.children.filter(c=>c.tagName==='THEAD')[0].rows[0].cells;
  const i = h.findIndex(c => c.textContent.startsWith('Budget Code'));
  const a = than.rows[0].cells[i], b = than.rows[1].cells[i];
  F02._dat(a, 'HD-A'); F02._dat(b, 'HD-B');
  _TRA['/ledger/101/fields/hd'] = {data:{gia_tri:null, value_source:'UNMAPPED'}};
  _TRA['/ledger/102/fields/hd'] = {data:{gia_tri:null, value_source:'UNMAPPED'}};
"""


def _lo(ma: str) -> dict:
    return _chay(_HAI_O + """
      const hop = [];
      HT.mo = (t, b, n) => { hop.push([t, b]); return {dong(){}}; };
      let lan = 0;
      const ghi_that = FLS.ghi;
      FLS.ghi = function (duong, t) {
        lan++;
        if (lan === 2) return Promise.reject(new FLS.LoiCua('%s', 0,
          'quá 30 s chưa có trả lời — POST ' + duong));
        return ghi_that(duong, t);
      };
      await F02._bay();
      return {hop, lan, cho: [...F02.ST.cho.keys()],
              tt: document.querySelector('#so-tt').textContent};
    """ % ma)


@can_node
def test_MAU_SO_mat_ket_noi__lo_luu_NOI_o_nao_chua_vao_so():
    """Mẫu số: phép đo đọc được chữ *"CHƯA vào sổ"* trong hộp + dòng trạng
    thái *(nếu bài dưới xanh vì ⛔ đọc được gì thì bài này đỏ)*."""
    r = _lo("FLS-MAT-KET-NOI")
    assert r["lan"] == 2, "⛔ không đo được: lô ⛔ gửi ô thứ hai"
    assert r["hop"], "⛔ không đo được: ⛔ hộp nào"
    assert "CHƯA vào sổ" in r["hop"][0][1]
    assert "CHƯA vào sổ" in r["tt"]


@can_node
@pytest.mark.xfail(strict=True, reason="KQ-061 F-1 (NHE → BA → DEV): lô lưu F02 "
                   "gặp FLS-HET-GIO vẫn khẳng định ô 'CHƯA vào sổ' (BA-06 v4.23 ⓕ3: "
                   "⛔ được nói chưa xảy ra) — đo 8099: ô ấy ĐÃ vào sổ (adj 4312)")
def test_F1_HET_GIO_lo_luu_F02_KHONG_noi_o_CHUA_vao_so():
    r = _lo("FLS-HET-GIO")
    assert r["lan"] == 2, "⛔ không đo được: lô ⛔ gửi ô thứ hai"
    assert r["hop"], "⛔ không đo được: ⛔ hộp nào"
    tieu_de, than = r["hop"][0]
    assert "Máy chưa trả lời sau 30 giây" in than, than[:300]
    assert "CHƯA vào sổ" not in than, ("⛔ hộp khẳng định ô CHƯA vào sổ cho "
                                      "một lượt ghi hết giờ", than[:400])
    assert "CHƯA vào sổ" not in r["tt"], ("⛔ dòng trạng thái khẳng định ô "
                                         "CHƯA vào sổ", r["tt"])
