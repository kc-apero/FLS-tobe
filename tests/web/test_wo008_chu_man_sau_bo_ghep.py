# -*- coding: utf-8 -*-
"""`WO-008` — chữ trên màn sau một cú bỏ ghép *(`KQ-007` `F-1`…`F-3`)*.

Spec: `BA-06` **v4.8** — dòng *"F02 · nhật ký trong drawer"* *(`F-1`)* · dòng
*"F01/F02 · nút Bỏ ghép"* *(`F-2`)* · mục ⓔ *Hộp thoại BỎ GÁN* đoạn *"v4.8 —
BÁO SAU khi bỏ gán"* *(`F-3`)*; `BA-10` **v0.8** `DT-I14` *"Nhật ký của bản
đảo — đọc thế nào"* + *Định nghĩa `bo_qua`*.

⛔⛔ **Ba lỗ, cả ba ĐÃ ĐO trên kho TEST** *(`KQ-007`, máy `8099`, dòng **B**)*:

  ⓐ `F-1` — bản đảo một gợi ý máy ghi nhật ký `value_after = NULL` *(luật ghi
    ⛔ đổi — `BA-10` v0.8)*. Màn `F02` ⑦ in nguyên ô **trống** ⇒ người đọc từ
    trên xuống thấy *"ô hd thành trống"* và **tưởng giá trị mình vừa gõ đã
    mất** — trong khi gợi ý máy **⛔ bao giờ** là Final *(`QĐ-ITL-149`)*.
  ⓑ `F-2` — hộp *"Đã bỏ ghép"* in tên ô theo **bút toán**: dòng 2 ô ra
    *"cdt1, hd, hd, cdt1"* ⇒ người đọc đếm ra **4** ô.
  ⓒ `F-3` — nút `Bỏ gán` của màn ghép **bỏ** thân trả ⇒ `bo_qua` *(giá trị
    người máy ⛔ rút)* **⛔ hiện**, dù `BA-06` nói nó *"phải hiện"*.

⭐ Mỗi bài đếm **mẫu số ≠ 0** trước khi kết luận *(`Đ3`)*; chiều ĐỎ của từng
bài ghi ở docstring và đã **chạy thật** trên mã cũ *(`BG` của phiếu này)*.

⚠ Ký hiệu `⛔` **⛔ được** hiện trên `man_f02.js` *(`test_luat_ky_hieu_man_
hinh.py` — `CAM`)* ⇒ nhãn spec *"máy gợi ý · ⛔ đổi Final"* hiện thành chữ
trơn **"máy gợi ý · không đổi Final"** *(`WO-008` Rủi ro 1: "ký hiệu ngoài danh
mục thì dùng chữ trơn")*. `man_f01.js` ⛔ trong `THEO_LUAT` ⇒ `↩` giữ.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser

from tests.web.khung_node import _VE, _chay, can_node
from tests.web.test_drawer_f02 import _BAM, DONG_DAY

# ── nhãn — khai MỘT chỗ ở bài, so nguyên văn với màn ───────────────────────
NHAN_MAY = "máy gợi ý · không đổi Final"
NHAN_NGUOI = "người sửa"
RUT = "rút gợi ý"


class _Bang(HTMLParser):
    """Đọc **chữ từng ô** của một bảng HTML — DOM giả ⛔ phân tích HTML."""

    def __init__(self) -> None:
        super().__init__()
        self.hang: list[list[str]] = []
        self._o: list[str] | None = None
        self._trong_than = False

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self._trong_than = True
        elif tag == "tr" and self._trong_than:
            self.hang.append([])
        elif tag == "td" and self._trong_than:
            self._o = []

    def handle_endtag(self, tag):
        if tag == "td" and self._o is not None:
            self.hang[-1].append("".join(self._o).strip())
            self._o = None
        elif tag == "tbody":
            self._trong_than = False

    def handle_data(self, data):
        if self._o is not None:
            self._o.append(data)


def _bang_nhat_ky(chu_panel: str) -> list[list[str]]:
    """Cắt đúng khối ⑦ của panel rồi đọc bảng. ⛔ thấy khối ⇒ NỔ *(`Đ5`)*."""
    i = chu_panel.find("⑦ Nhật ký")
    assert i >= 0, "⛔ không đo được: panel ⛔ có khối ⑦ Nhật ký"
    p = _Bang()
    p.feed(chu_panel[i:])
    return p.hang


#: ⭐ Bốn loại dòng nhật ký `AUD-1` — đúng bốn ca `BA-06` v4.8 khai.
NK_BON = [
    {"at": "2026-10-01T09:00:00", "field": "hd", "value_before": None,
     "value_after": "HD-A", "actor": "ke-toan@apero.vn",
     "value_source": "may_goi_y", "reason": "suy tu dong lenh"},
    {"at": "2026-10-01T09:05:00", "field": "hd", "value_before": "HD-A",
     "value_after": None, "actor": "ke-toan@apero.vn",
     "value_source": "may_goi_y", "reason": "dao but toan suy tu phep ghep da bo"},
    {"at": "2026-10-01T09:10:00", "field": "cdt1", "value_before": None,
     "value_after": "C-NGUOI", "actor": "kt2@apero.vn",
     "value_source": "sua_tay", "reason": "go tay"},
    {"at": "2026-10-01T09:15:00", "field": "cdt1", "value_before": "C-NGUOI",
     "value_after": None, "actor": "kt2@apero.vn",
     "value_source": "sua_tay", "reason": "xoa"},
]


def _mo_drawer(nk: list[dict]) -> list[list[str]]:
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: %s}};
      HT.mo = () => ({dong(){}});
    """ % (json.dumps(DONG_DAY, ensure_ascii=False),
           json.dumps(nk, ensure_ascii=False))) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    return _bang_nhat_ky(ra)


# ═══ AC-1 · (a) `F-1` — nhật ký `F02` ⑦ đọc theo `value_source` ════════════
@can_node
def test_AC1_nhat_ky_BON_loai_dong__thanh_va_nguon_doc_theo_value_source():
    """⭐⭐ Bốn loại dòng ⇒ ô **thành** *"gợi ý: X"* · *"rút gợi ý"* · `X` ·
    trống; ô **nguồn** *"máy gợi ý · không đổi Final"* ×2 · *"người sửa"* ×2.

    Cột: `lúc · ô · từ · thành · ai · nguồn · vì sao` ⇒ chỉ số `3` và `5`.

    ⛔ Chiều ĐỎ: trả ô thành về `TP.chu(x.value_after)` ⇒ hàng 2 rỗng ⇒ ĐỎ;
    in `value_source` thô ⇒ ô nguồn `may_goi_y` ⇒ ĐỎ.
    """
    hang = _mo_drawer(NK_BON)
    assert len(hang) == 4, f"⛔ không đo được: bảng vẽ {len(hang)} hàng, mong 4"
    thanh = [h[3] for h in hang]
    nguon = [h[5] for h in hang]
    assert thanh == ["gợi ý: HD-A", RUT, "C-NGUOI", ""], thanh
    assert nguon == [NHAN_MAY, NHAN_MAY, NHAN_NGUOI, NHAN_NGUOI], nguon


@can_node
def test_AC1_nguon_LA_thi_in_NGUYEN_MA_khong_doan_nhan():
    """`BA-06` v4.8: *"mã khác ⇒ in nguyên mã (⛔ đoán nhãn)"*. Nguồn lạ
    *(vd. `UNMAPPED` mà bài `test_drawer_f02` dùng)* + nguồn rỗng ⇒ ô thành
    in giá trị như nay, ⛔ *"gợi ý:"*, ⛔ *"rút gợi ý"*."""
    nk = [dict(NK_BON[0], value_source="UNMAPPED", value_after="A"),
          dict(NK_BON[1], value_source=None, value_after=None)]
    hang = _mo_drawer(nk)
    assert len(hang) == 2, hang
    assert [h[5] for h in hang] == ["UNMAPPED", ""], hang
    assert [h[3] for h in hang] == ["A", ""], hang


@can_node
def test_AC1_rong_van_noi_nhat_ky_trong():
    """Trạng thái **rỗng** *(`WO-008` Màn hình)* ⛔ đổi."""
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: []}};
      HT.mo = () => ({dong(){}});
    """ % json.dumps(DONG_DAY, ensure_ascii=False)) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    assert "nhật ký trống — chưa ai sửa dòng này" in ra


# ═══ AC-3 · (b) `F-2` — hộp "Đã bỏ ghép" nói theo Ô ══════════════════════
VO_F01 = """
const man = d.document.createElement('section'); man.id = 'man-f01';
man.className = 'screen on';
const than = d.document.createElement('div'); than.id = 'than-f01';
man.appendChild(than); d.body.appendChild(man);
const scrim = d.document.createElement('div'); scrim.id = 'scrim';
for (const id of ['dlg-t', 'dlg-b', 'dlg-f']) {
  const e = d.document.createElement('div'); e.id = id; scrim.appendChild(e);
}
d.body.appendChild(scrim);
const man2 = d.document.createElement('section'); man2.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man2); d.body.appendChild(goc); d.body.appendChild(tim);
"""

#: ⭐ Đúng thứ tự `index.html` — màn ghép nạp **SAU** `man_f01.js`.
TEP_F01 = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
           "man_f01_lenh.js", "man_f01.js", "man_f01_ghep.js"]

#: ⭐ Máy đếm hộp: ghi lại MỌI lần mở, rồi gọi **xuyên** xuống `HT.mo` THẬT.
#:
#: ⛔⛔ Bản vòng 1 *(`69f03f6`)* **thay** `HT.mo` bằng bẫy và **tự định nghĩa**
#:    thêm một hàm hỏi trên `HT` mà `hop_thoai.js` ⛔ bao giờ xuất *(nó trả
#:    đúng `{ mo, dong, loi_trong_hop }`)*, trả sẵn `true`. Bẫy ấy **che
#:    đúng chỗ thiếu**: trên trình duyệt thật, bỏ gán chùm chết ở `TypeError`
#:    — `KQ-019 F-1`, máy `8099`; lớp lỗi *"khuôn thử tự nhét"* của `11` §6.
#: ⭐ Viết lại vòng 2 *(`WO-008` Phạm vi (d))* **giữ nguyên lo gốc** — đếm
#:    hộp *"Đã bỏ ghép"*, đọc tiêu đề / thân / nút — nhưng hộp nay là của
#:    **hàm thật** *(`#scrim` · `#dlg-*` do `HT.mo` thật dựng)*, và ⛔ còn
#:    hàm nào trên `HT` do bài đặt ra. Bài `test_AC8_KHONG_con_HT_hoi__…` của
#:    `test_wo008_v2_nam_ca_bo_gan.py` canh để bẫy ấy ⛔ quay lại.
BAY_HOP = """
  globalThis._HOP = [];
  const _mo_that = HT.mo;
  HT.mo = (t, b, n) => { _HOP.push({k: 'mo', t, b, n: (n || []).map(x => x[0])});
                          return _mo_that(t, b, n); };
"""


def _hop_bo_ghep(than: dict) -> dict:
    return _chay(BAY_HOP + """
      F01._bao_bo_ghep(%s);
      await new Promise(r => setTimeout(r, 120));
      return _HOP;
    """ % json.dumps(than, ensure_ascii=False), tep=TEP_F01, vo=VO_F01)


def _not_dao(body: str) -> str:
    """Nốt `↩` — câu đảo — cắt tới hết `</div>` của nó."""
    m = re.search(r"↩(.*?)</div>", body, re.S)
    assert m, f"⛔ không đo được: hộp ⛔ có nốt ↩: {body[:200]!r}"
    return re.sub(r"<[^>]+>", "", m.group(1))


#: ⭐ Thân trả THẬT của dòng B *(`KQ-007` — `but_toan_dao` `[cdt1, hd, hd,
#:    cdt1]`, `bo_qua` `[hd · sua_tay · HD-K7B]`)*. Bài `_pg` cùng phiếu dựng
#:    lại thân này **từ cửa thật** trên kho TEST.
THAN_B = {
    "da_bo": [{"pm_line_id": "PWB-1"}], "ve_hang_cho": True,
    "but_toan_dao": [{"field": "cdt1", "dao_cua": 11}, {"field": "hd", "dao_cua": 12},
                     {"field": "hd", "dao_cua": 13}, {"field": "cdt1", "dao_cua": 14}],
    "bo_qua": [{"field": "hd", "nguon": "sua_tay", "value_after": "HD-K7B",
                "adj_id": 15}],
}


@can_node
def test_AC3_hop_bo_ghep_HAI_lop__2_o_4_but_toan_moi_ten_o_DUNG_mot_lan():
    """⛔ Chiều ĐỎ: trả về `dao.map(...).join(', ')` ⇒ `hd` đếm **2** ⇒ ĐỎ."""
    hop = _hop_bo_ghep(THAN_B)
    assert len(hop) == 1 and hop[0]["k"] == "mo", hop
    cau = _not_dao(hop[0]["b"])
    assert "2 ô" in cau, cau
    assert "4 bút toán" in cau, cau
    assert "gồm lớp gợi ý cũ bị đè" in cau, cau
    assert cau.count("cdt1") == 1 and cau.count("hd") == 1, cau
    # thứ tự xuất hiện ĐẦU TIÊN trong `but_toan_dao`
    assert cau.index("cdt1") < cau.index("hd"), cau
    # khối `bo_qua` GIỮ *(cảnh báo "người đã gõ tay")*, ⛔ lẫn vào câu đảo
    assert "HD-K7B" not in cau and "người" in hop[0]["b"], hop[0]["b"]


@can_node
def test_AC3_hop_bo_ghep_MOT_lop__2_o_KHONG_duoi_but_toan():
    hop = _hop_bo_ghep({"da_bo": [{}], "bo_qua": [],
                        "but_toan_dao": [{"field": "cdt1"}, {"field": "hd"}]})
    cau = _not_dao(hop[0]["b"])
    assert "2 ô" in cau, cau
    assert "bút toán" not in cau, f"⛔ một lớp mà vẫn in đuôi bút toán: {cau}"
    assert cau.count("cdt1") == 1 and cau.count("hd") == 1, cau


# ═══ AC-4 · (c) `F-3` — màn ghép BÁO SAU khi bỏ gán nếu `bo_qua` ⛔ rỗng ══
LENH = {"ma_lenh": "PWB-1", "noi_dung": "x", "so_tien": "5000000.00",
        "curr": "VND", "trang_thai": "da_gan", "trang_thai_nhan": "da gan",
        "trang_thai_mau": "", "loai_phieu": "PM", "itl_da_gan": [4242],
        "nhom_du_truong": []}


def _bo_gan(than: dict | None, *, no: bool = False) -> dict:
    tra = ("_TRA['/queue/4242/unmatch'] = {no: {cau: 'Máy gặp lỗi bên trong.'}};"
           if no else
           "_TRA['/queue/4242/unmatch'] = {data: %s};"
           % json.dumps(than, ensure_ascii=False))
    return _chay(BAY_HOP + tra + """
      _TRA['/queue/4242/chum'] = {data: {can_hoi: false, so_dong: 1}};
      _TRA['/queue/lenh/PWB-1/itl-candidates'] = {data: {ung_vien: []}};
      _TRA['/queue/lenh/PWB-1/so'] = {data: {ung_vien: []}};
      F01G.ST.dong = [%s];
      // ⭐ vòng 2: MỞ lệnh trước — nút `Bỏ gán` chỉ sống ở view ② *(khối
      //   hành động)*, và dòng lỗi ca ⑤ vẽ ở đó; view ① ⛔ có nút ấy.
      await F01G.mo_lenh('PWB-1');
      let loi = null;
      try { await F01G.bo_gan(F01G.ST.dong[0]); } catch (e) { loi = String(e && e.cau || e); }
      await new Promise(r => setTimeout(r, 120));
      return {hop: _HOP, loi,
              man: document.getElementById('ghep-goc').textContent,
              unmatch: _GOI.filter(g => g[0] === 'ghi' && /unmatch/.test(g[1])).length};
    """ % json.dumps(LENH, ensure_ascii=False), tep=TEP_F01, vo=VO_F01)


@can_node
def test_AC4_bo_gan_bo_qua_CO_muc__MOT_hop_bao_mot_nut_Da_hieu():
    """⛔ Chiều ĐỎ: bỏ đọc thân *(`await FLS.ghi(...)` ⛔ gán)* ⇒ **0** hộp ⇒ ĐỎ."""
    r = _bo_gan(THAN_B)
    assert r["unmatch"] == 1, "⛔ không đo được: màn ⛔ gọi cửa unmatch"
    assert len(r["hop"]) == 1, r["hop"]
    h = r["hop"][0]
    assert h["k"] == "mo" and h["t"] == "Đã bỏ ghép", h
    assert h["n"] == ["Đã hiểu"], h["n"]
    # `AC-4` mong: hộp chứa `hd` **và** `HD-K7B` *(giá trị người — `HOI-016`
    # ⓐ: khối `bo_qua` in thêm giá trị bên cạnh tên ô)*.
    assert "hd" in h["b"] and "HD-K7B" in h["b"], h["b"]


@can_node
def test_AC4_bo_gan_bo_qua_RONG__KHONG_hop_nao():
    """⛔ Chiều ĐỎ: mở hộp cả khi `bo_qua` rỗng ⇒ ĐỎ *(tiếng ồn — `BA-06` v4.8)*."""
    r = _bo_gan(dict(THAN_B, bo_qua=[]))
    assert r["unmatch"] == 1, "⛔ không đo được: màn ⛔ gọi cửa unmatch"
    assert r["hop"] == [], r["hop"]


@can_node
def test_AC4_cua_unmatch_LOI__KHONG_mo_hop_da_bo_ghep():
    """Trạng thái **lỗi** *(`WO-008` Màn hình)*: ⛔ thân trả ⇒ ⛔ hộp *"Đã bỏ
    ghép"*; và lỗi cửa **⛔ bị nuốt**.

    ⭐ Viết lại vòng 2 — **giữ hai lo gốc** *(⛔ hộp "Đã bỏ ghép" khi cửa lỗi ·
    lỗi ⛔ được biến mất)*, đổi **chỗ** lỗi hiện ra. Bản vòng 1 đòi lỗi
    *"đi như nay (ném lên người gọi)"* — tiền đề ấy **sai**: trên máy `8099`
    cú ném rơi ra trình nghe `click` thành `Uncaught (in promise) LoiCua`, màn
    ⛔ một chữ *(`KQ-019 F-3`)*. `BA-06` **v4.10** ca ⑤ đính chính: lỗi thành
    **dòng chữ** *"Bỏ gán chưa xảy ra — Cửa lỗi: …"* trên màn, `bo_gan`
    ⛔ ném. ⇒ *"lỗi ⛔ bị nuốt"* nay đo bằng **chữ trên màn**, ⛔ bằng ngoại
    lệ. Bài đủ năm ca ở `test_wo008_v2_nam_ca_bo_gan.py::test_AC11_*`."""
    r = _bo_gan(None, no=True)
    assert r["unmatch"] == 1
    assert r["loi"] is None, f"⛔ lỗi rơi ra trình nghe click: {r['loi']}"
    assert "Bỏ gán chưa xảy ra — Cửa lỗi: Máy gặp lỗi bên trong." in r["man"], \
        "⛔ lỗi cửa bị nuốt — màn ⛔ nói gì"
    assert [h for h in r["hop"] if h["t"] == "Đã bỏ ghép"] == [], r["hop"]
