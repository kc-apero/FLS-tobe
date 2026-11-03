# -*- coding: utf-8 -*-
"""⛔⛔ **CỔNG RA của `B2` ở tầng MÀN HÌNH** — khối ghép LÔ của `F01`.

Lộ trình `13` §1 chặng ① khai cổng của `B2` bằng bốn câu, và **một trong bốn
câu là một câu về MÀN HÌNH**:

    *"⛔ Và nó **⛔ không phải** đòn chính — nói thẳng con số **8,0%** trên màn"*

⇒ Nên bài này ⛔ không kiểm *"nút có bấm được ⛔ không"*. Nó kiểm **màn hình có
  NÓI RA phần việc ⛔ không thuộc cửa này** — vì đó là chỗ duy nhất mà một
  người dùng thật sẽ đọc con số, và một màn hiện `68 dòng ghép được` mà ⛔ không
  hiện `6.577 dòng thiếu dữ liệu lệnh chi` sẽ làm cả đội tưởng cửa này là câu
  trả lời.

★ Cửa được **giả lập**: câu hỏi ở đây là *"màn vẽ đúng ⛔ không"*. Câu *"cửa trả
  đúng ⛔ không"* là việc của `tests/api/test_cua_ghep_lo_pg.py` — chạy trên kho
  THẬT qua HTTP THẬT.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay, can_node

# ⭐ Hình số CỐ Ý giống kho thật 09/09: **68** tự chứng trong **7.329** dòng
#   chưa nối, và **6.577** dòng nút-thắt-thật. Một bộ số mẫu tròn trịa
#   *(10/100)* sẽ ⛔ không lộ ra chuyện màn hình vẽ **con số nào** ở đâu.
_TU_CHUNG = {
    "tu_chung": [{"itl_id": 101, "pm_line_ids": ["PM-1"]},
                 {"itl_id": 102, "pm_line_ids": ["PM-2", "PM-3"]}],
    "khong": [
        {"itl_id": 201, "ly_do": "mot_dong_lech_tien",
         "cau": "dung MOT dong PM mang ma ay ma so tien lech"},
        {"itl_id": 202, "ly_do": "mot_dong_lech_tien",
         "cau": "dung MOT dong PM mang ma ay ma so tien lech"},
        {"itl_id": 203, "ly_do": "khac_tien_te",
         "cau": "⛔ khong dong nao CUNG TIEN TE voi dong tien"},
        {"itl_id": 204, "ly_do": "co_dong_chua_duyet",
         "cau": "chum co it nhat mot dong `status` ⛔ khong phai `Approve`"},
    ],
    "so_dong_xet": 7329,
    "vi_sao": {"khong_co_so_chung_tu": 100, "ma_khong_chuan_hoa_duoc": 0,
               "PM_khong_mang_ma_nay": 6577, "PM_co_ma_nay": 652},
    "pham_vi": "chi lan nap that",
}

VO_F01 = """
const man = d.document.createElement('section'); man.id = 'man-f01';
man.className = 'screen on';
const than = d.document.createElement('div'); than.id = 'than-f01';
man.appendChild(than);
d.body.appendChild(man);

// ⭐⭐ Khung HOP THOAI dung san — va day la mot **gioi han co chu y cua khung
//    DOM gia**, ⛔ khong phai mot cai vong ne.
//
// `dom_gia.js` khai thang o dau tep: *"⛔ ⛔ Khong PHAN TICH HTML — bai kiem
// nao can cau truc that thi phai dung createElement"*. `hop_thoai._khung()`
// dung `innerHTML` de dung ba o `#dlg-t`/`#dlg-b`/`#dlg-f`, nen tren khung gia
// chung ⛔ **khong ton tai** va `HT.mo` NO ngay dong dau. ⇒ Dung san ba o ay
// (cung khuon voi `VO_F04` dung san tam o `nap-*`), roi `_khung()` thay
// `#scrim` da co va **bo qua** cau `innerHTML`.
//
// ⚠ Va o nhap `#o-ly-do-lo` cung phai dung san, vi than hop thoai cung di qua
//   `innerHTML`. Do la cho phep do nay **⛔ khong voi toi**: no ⛔ khong chung
//   minh duoc rang chuoi HTML kia co chua dung o do. Cai no chung minh — va la
//   cai dat nhat — la **than yeu cau gui len mang gi**.
const scrim = d.document.createElement('div'); scrim.id = 'scrim';
for (const id of ['dlg-t', 'dlg-b', 'dlg-f']) {
  const e = d.document.createElement('div'); e.id = id; scrim.appendChild(e);
}
d.body.appendChild(scrim);
const inp = d.document.createElement('input'); inp.id = 'o-ly-do-lo';
d.body.appendChild(inp);
"""

TEP_F01 = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
           "man_f01.js"]


def _ve(kich_ban: str, *, tra: dict | None = None, phien=None):
    dat = {"/queue/tu-chung": {"data": _TU_CHUNG}}
    dat.update(tra or {})
    mo = "".join(
        "_TRA[%s] = %s;\n" % (json.dumps(k), json.dumps(v, ensure_ascii=False))
        for k, v in dat.items())
    return _chay(mo + """
      const o = document.querySelector('#than-f01');
      const the = document.createElement('div'); o.appendChild(the);
      await F01.ve_lo(the);
    """ + kich_ban, tep=TEP_F01, vo=VO_F01, phien=phien)


@can_node
def test_nut_mang_DUNG_so_dong_tu_chung():
    r = _ve("return {nhan: document.querySelector('#lo-nut-ghep').textContent,"
            " tat: document.querySelector('#lo-nut-ghep').disabled};")
    assert "2" in r["nhan"] and r["tat"] is False


@can_node
def test_man_NOI_RA_nut_that_KHONG_thuoc_cua_nay():
    """⭐⭐⭐ Câu cổng của `B2`: *"nói thẳng con số nhỏ trên màn"*.

    ⛔⛔ Bài này ⛔ không kiểm một lớp CSS — nó kiểm **ba con số cùng có mặt**:
    tổng dòng chưa nối, số dòng cửa này dọn được, và **nút thắt thật**. Thiếu
    con số thứ ba thì màn hình ⛔ không nói dối câu nào, nhưng nó **để người
    đọc tự suy ra một điều sai**.
    """
    r = _ve("return document.querySelector('#lo-ghi-chu-nut-that')"
            ".textContent;")
    assert "7.329" in r, r
    assert "6.577" in r, r
    assert "A3" in r, r


@can_node
def test_bang_TU_CHOI_gop_theo_LY_DO_va_moi_ly_do_mot_CAU():
    """⛔ Bốn lý do ⇒ **bốn đường sửa**. Gộp chúng thành một con số là bỏ đi
    đúng phần thông tin người đọc cần để đi tiếp."""
    # ⚠ Doc `innerHTML` chu ⛔ khong `tBodies`: khung DOM gia **co y ⛔ khong
    #   phan tich HTML** (*"bai nao can cau truc that thi phai dung
    #   createElement"* — dau `dom_gia.js`). Bang nay dung `innerHTML` giong moi
    #   bang khac cua `F02`/`F03`, nen phep do o day la phep do CHUOI.
    r = _ve("return document.querySelector('table').innerHTML;")
    # ⭐ gop DUNG: hai dong `mot_dong_lech_tien` ⇒ **mot hang, so 2**
    assert "mot_dong_lech_tien" in r and "<b>2</b>" in r, r
    assert "khac_tien_te" in r and "co_dong_chua_duyet" in r, r
    # ⛔ Moi ly do mang mot CAU — ⛔ khong hang nao chi co ma
    assert "CUNG TIEN TE" in r and "Approve" in r, r
    # ⛔ Va `ung_vien_da_bi_ghep` (0 dong) ⛔ KHONG duoc ve mot hang rong
    assert "ung_vien_da_bi_ghep" not in r, r


@can_node
def test_KHONG_dong_nao_tu_chung_thi_nut_TAT_ma_khoi_VAN_VE():
    """⛔⛔ `0` dòng tự chứng ⛔ **KHÔNG** phải trạng thái RỖNG.

    Đúng lúc ấy khối này mới cần nói *"việc nằm ở chỗ khác"*. Nếu coi `0` là
    rỗng thì màn hình biến mất **đúng vào ngày** cửa ghép lô hết việc — và
    ⛔ không ai còn thấy `6.577` dòng nút thắt.
    """
    r = _ve("return {tat: document.querySelector('#lo-nut-ghep').disabled,"
            " ghi: !!document.querySelector('#lo-ghi-chu-nut-that')};",
            tra={"/queue/tu-chung": {"data": dict(_TU_CHUNG, tu_chung=[])}})
    assert r["tat"] is True and r["ghi"] is True


@can_node
def test_cua_CHI_DOC_thi_nut_TAT_truoc_khi_nguoi_bam():
    r = _ve("return document.querySelector('#lo-nut-ghep').disabled;",
            phien={"actor": "lan@apero.vn", "cho_ghi": False})
    assert r is True


@can_node
def test_than_GUI_LEN_chi_co_itl_ids_va_reason__KHONG_pm_line_ids():
    """⭐⭐⭐ Bài đắt nhất của tệp: soi **thân yêu cầu thật sự gửi lên**.

    ⛔⛔ Màn hình **CÓ** danh sách `pm_line_ids` trong tay *(cửa đọc trả nó ra
    để vẽ số mối nối)*. Nên chuyện gửi kèm nó lên là một dòng code **rất dễ
    thêm vào**, và nếu thêm thì cú bấm LÔ lặng lẽ biến thành *"N phép ghép tay
    ⛔ không ai xem"* — máy ⛔ không còn đo lại gì. Bài này ghim chỗ đó.
    """
    r = _ve("""
      document.querySelector('#lo-nut-ghep').onclick();
      document.querySelector('#o-ly-do-lo').value = 'bai kiem';
      const nut = [...document.querySelectorAll('button')]
        .find(b => b.textContent === 'Ghép cả lô');
      await nut.onclick();
      return _GOI.filter(g => g[0] === 'ghi');
    """)
    assert len(r) == 1, r
    _, duong, than = r[0]
    assert duong == "/queue/match-lo"
    assert sorted(than) == ["itl_ids", "reason"], than
    assert than["itl_ids"] == [101, 102]


@can_node
def test_thieu_LY_DO_thi_KHONG_goi_cua():
    r = _ve("""
      document.querySelector('#lo-nut-ghep').onclick();
      const nut = [...document.querySelectorAll('button')]
        .find(b => b.textContent === 'Ghép cả lô');
      await nut.onclick();
      // ⚠ ⛔ Không đọc giá trị trả về của `nut.onclick`: `hop_thoai` **bọc**
      //   hàm của màn trong một hàm riêng và giá trị `false` **⛔ không ra
      //   ngoài**. Đó là một chỗ phép đo ⛔ không với tới — nên bài này đo
      //   **hai dấu vết CÓ thể đo**: ⛔ không cú ghi nào, và ô nhập được đưa
      //   con trỏ về (`focus`), tức màn đã **chỉ cho người chỗ phải gõ**.
      return {ghi: _GOI.filter(g => g[0] === 'ghi').length,
              da_focus: !!document.querySelector('#o-ly-do-lo')._focus};
    """)
    assert r["ghi"] == 0, r
    assert r["da_focus"] is True, r
