# -*- coding: utf-8 -*-
"""`KQ-019` — kiểm `BG-017` *(`WO-008`: chữ trên màn sau một cú bỏ ghép)*.

⭐ Hai loại bài trong tệp này:

ⓐ **XANH** — chỗ bài của Dev **⛔ chạm tới**:
   · Mọi bài màn của `WO-008` **thay `HT.mo`/`HT.hoi` bằng bẫy** *(`BAY_HOP`)*
     ⇒ ⛔ bài nào chứng minh hộp **THẬT** *(`hop_thoai.js`)* dựng ra đúng tiêu đề
     + đúng **một** nút. Bài ở đây nạp `hop_thoai.js` thật, ⛔ thay hàm nào.
   · Bài `AC-1`/`AC-2` của Dev đo **4** dòng tự soạn + **một** dòng B dựng trên
     kho TEST. Bài ở đây đưa **toàn bộ nhật ký SỔ THẬT** *(chỉ đọc —
     `noi_chi_doc`, qua **hàm đọc thật** `doc_nhat_ky` của cửa `/journal`)* vào
     **màn thật** và đo **quan hệ** *(⛔ hằng số — sổ trôi thì bài vẫn đúng)*.

ⓑ **`xfail(strict=True)`** — phát hiện `F-1`…`F-4` của `KQ-019`, **ĐỎ trên
   mã hôm nay** *(`66cda8e`)*. Dev sửa ⇒ bài **XPASS** ⇒ `strict` làm nó đỏ
   ⇒ `fls-test` gỡ dấu *(như `KQ-005`/`KQ-007`)*. ⛔ Ai sửa bài cho xanh.

   ⛔⛔ Cả bốn là lớp *"khuôn thử tự nhét"* *(`11` §6)*: bài của Dev đút sẵn
   `HT.hoi` ⇒ ⛔ thấy `HT.hoi` **⛔ tồn tại** trong `hop_thoai.js`; đút sẵn
   thân `itl-candidates` ⇒ ⛔ thấy `mo_lenh` ném thì hộp ⛔ mở; ⛔ bài nào đọc
   màn **SAU** cú bỏ gán ⇒ ⛔ thấy màn vẫn nói *"Đang gán"*.
   Đo thật trên máy `8099` *(kho TEST, Chrome headless, 02/10)*: chùm ⇒
   `Uncaught TypeError: HT.hoi is not a function`, `/unmatch` **0** lượt; sau
   bỏ gán thành công ⇒ khối *"✓ Đang gán với giao dịch … bỏ gán"* còn nguyên,
   bấm lại ⇒ `409` im lặng; cắt mạng ⇒ `Uncaught LoiCua` — màn ⛔ hiện gì.
"""
from __future__ import annotations

import json
import re
from html.parser import HTMLParser

import pytest

from fls.db.kho import dsn_that, noi_chi_doc
from fls.repo import doc_bao_cao as bc
from fls.repo.pham_vi import chi_nap_that
from tests.web.khung_node import _VE, _chay, can_node
from tests.web.test_drawer_f02 import _BAM, DONG_DAY

#: ⭐ Nhãn — chép nguyên văn `BA-06` **v4.9** *(đính chính `TL-016`)*.
NHAN_MAY = "máy gợi ý · không đổi Final"
NHAN_NGUOI = "người sửa"
RUT = "rút gợi ý"
#: ⭐ *(`KQ-061`, `BA-06` v4.12 dòng "F02 · nhật ký" ⓑ ⓒ — chép nguyên văn)*.
DAO = "đảo — giá trị này hết hiệu lực"
XOA_O = "xoá ô"

#: ⭐ Đúng thứ tự `index.html` — có **`hop_thoai.js` THẬT**.
TEP = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
       "man_f01_lenh.js", "man_f01.js", "man_f01_ghep.js"]

#: Vỏ: `#scrim` dựng sẵn ba ô *(DOM giả ⛔ phân tích `innerHTML`)* — `HT._khung`
#: thấy `#scrim` thì dùng luôn, nên mọi thứ còn lại là mã thật.
VO = """
const man = d.document.createElement('section'); man.id = 'man-f01';
man.className = 'screen';
const tf = d.document.createElement('div'); tf.id = 'than-f01';
man.appendChild(tf); d.body.appendChild(man);
const scrim = d.document.createElement('div'); scrim.id = 'scrim';
for (const id of ['dlg-t', 'dlg-b', 'dlg-f']) {
  const e = d.document.createElement('div'); e.id = id; scrim.appendChild(e);
}
d.body.appendChild(scrim);
const man2 = d.document.createElement('section'); man2.id = 'man-ghep';
man2.className = 'screen on';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
man2.appendChild(goc); d.body.appendChild(man2); d.body.appendChild(tim);
"""

#: Đọc **hộp thật** + **màn ghép** sau kịch bản.
DOC_HOP = """
  const s = document.getElementById('scrim');
  const hop = {mo: s.classList.contains('on'),
               t: document.getElementById('dlg-t').textContent,
               b: document.getElementById('dlg-b').textContent,
               nut: document.getElementById('dlg-f').children.map(x => x.textContent)};
  const man = document.getElementById('ghep-goc').textContent;
"""

#: Lệnh **một** dòng tiền, đang gán — đủ trường để màn vẽ khối *"Đang gán"*.
LENH = {"ma_lenh": "PWB-1", "noi_dung": "x", "so_tien": "5000000.00",
        "curr": "VND", "trang_thai": "da_gan", "trang_thai_nhan": "Đã gán",
        "trang_thai_mau": "good", "loai_phieu": "PM", "itl_da_gan": [4242],
        "nhom_du_truong": [],
        "gd_ds": [{"itl_id": 4242, "bac": "tien", "doc_no": "FT-K7B",
                   "amount": "5000000.00", "curr": "VND",
                   "doc_date": "2026-09-01", "da_gan": True}]}

#: Thân `unmatch` THẬT của dòng B *(máy `8099`, `KQ-019`: `but_toan_dao`
#: `[cdt1, hd, cdt1, hd, cdt1]`, `bo_qua` `[(hd, HD-NGUOI-B2)]`)*.
THAN_B = {
    "itl_id": 4242, "da_bo": [{"pm_line_id": "PWB-1"}], "ve_hang_cho": True,
    "but_toan_dao": [{"field": f, "dao_cua": i} for i, f in
                     enumerate(["cdt1", "hd", "cdt1", "hd", "cdt1"], 11)],
    "bo_qua": [{"field": "hd", "nguon": "sua_tay", "value_after": "HD-NGUOI-B2",
                "adj_id": 20}],
}


def _bo_gan(*, than=None, lenh=None, chum=None, unmatch_no=None,
            ung_vien_no=False, cho_xong=True) -> dict:
    """Chạy `F01G.bo_gan` THẬT với `hop_thoai.js` THẬT; trả hộp + màn + lỗi."""
    lenh = lenh or LENH
    chum = chum or {"can_hoi": False, "so_dong": 1, "dong_lenh": []}
    tra = [f"_TRA['/queue/4242/chum'] = {{data: {json.dumps(chum, ensure_ascii=False)}}};"]
    if unmatch_no:
        tra.append("_TRA['/queue/4242/unmatch'] = {no: %s};"
                   % json.dumps(unmatch_no, ensure_ascii=False))
    else:
        tra.append("_TRA['/queue/4242/unmatch'] = {data: %s};"
                   % json.dumps(than if than is not None else THAN_B,
                                ensure_ascii=False))
    duong_uv = "/queue/lenh/PWB-1/itl-candidates"
    tra.append(f"_TRA['{duong_uv}'] = "
               "{data: {ung_vien: [{itl_id: 7, bac: 'tien', amount: '1.00', curr: 'VND'}]}};")
    # ⭐ Lỗi vẽ lại chỉ bật **SAU** lần mở lệnh đầu — lần đầu phải vẽ được
    sau_mo = (f"_TRA['{duong_uv}'] = {{no: {{cau: 'Máy gặp lỗi bên trong.'}}}};"
              if ung_vien_no else "")
    return _chay("\n".join(tra) + """
      F01G.ST.dong = [%s];
      await F01G.mo_lenh('PWB-1');
      const truoc = document.getElementById('ghep-goc').textContent;
      %s
      globalThis._LOI = null;
      const p = F01G.bo_gan(F01G.ST.dong[0]).catch(e => { _LOI = String(e && (e.cau || e.message) || e); });
      if (%s) await p;
      await new Promise(r => setTimeout(r, 150));
    """ % (json.dumps(lenh, ensure_ascii=False), sau_mo,
           "true" if cho_xong else "false")
        + DOC_HOP + """
      return {hop, man, truoc, loi: _LOI,
              unmatch: _GOI.filter(g => g[0] === 'ghi' && /unmatch/.test(g[1])).length};
    """, tep=TEP, vo=VO)


# ═══ ⓐ XANH ════════════════════════════════════════════════════════════════
@can_node
def test_bo_gan_bo_qua_CO__HOP_THAT_mot_tieu_de_mot_nut_noi_theo_o():
    """`AC-4` + `AC-3` qua **`HT.mo` THẬT**: hộp mở *(`#scrim.on`)*, tiêu đề
    *"Đã bỏ ghép"*, **đúng một** nút *"Đã hiểu"*, có `hd = HD-NGUOI-B2`, câu
    đảo *"2 ô"* · *"5 bút toán"*, mỗi tên ô **một** lần trong câu đảo.

    Chứng minh ĐỎ *(`KQ-019`, bản sao cây `66cda8e`)*: bỏ đọc thân trong
    `bo_gan` ⇒ `mo=False`; trả câu đảo về `dao.map(...).join` ⇒ `hd` đếm 2.
    """
    r = _bo_gan()
    assert r["unmatch"] == 1, "⛔ không đo được: màn ⛔ gọi cửa unmatch"
    h = r["hop"]
    assert h["mo"] is True, f"⛔ hộp THẬT ⛔ mở: {h}"
    assert h["t"] == "Đã bỏ ghép", h
    assert h["nut"] == ["Đã hiểu"], h["nut"]
    assert "hd = HD-NGUOI-B2" in h["b"], h["b"]
    m = re.search(r"↩(.*?)</div>", h["b"], re.S)
    assert m, f"⛔ không đo được: hộp ⛔ có nốt ↩: {h['b'][:300]!r}"
    cau = re.sub(r"<[^>]+>", "", m.group(1))
    assert "2 ô" in cau and "5 bút toán" in cau, cau
    assert cau.count("cdt1") == 1 and cau.count("hd") == 1, cau


@can_node
def test_bo_gan_bo_qua_RONG__HOP_THAT_khong_mo():
    """`bo_qua` rỗng ⇒ **0** hộp *(`BA-06` mục ⓔ v4.8)*. Mẫu số: cửa
    `unmatch` được gọi **1** lần *(`Đ3`)*."""
    r = _bo_gan(than=dict(THAN_B, bo_qua=[]))
    assert r["unmatch"] == 1, "⛔ không đo được: màn ⛔ gọi cửa unmatch"
    assert r["hop"]["mo"] is False, r["hop"]
    assert r["loi"] is None, r["loi"]


def _nhat_ky_so_that() -> list[dict]:
    """Toàn bộ nhật ký sổ THẬT qua **hàm đọc thật** của cửa `/journal`.

    ⛔ Kho tắt ⇒ bài ĐỎ *(`Đ5`: ⛔ đo được ≠ ⛔ thấy lệch)*."""
    with noi_chi_doc(dsn_that()) as c:
        pv = chi_nap_that()
        ids = [r[0] for r in c.execute(
            "SELECT DISTINCT itl_id FROM fls_journal ORDER BY 1").fetchall()]
        rows: list[dict] = []
        for i in ids:
            rows.extend(bc.doc_nhat_ky(c, pv, i))
        so = c.execute("SELECT count(*) FROM fls_journal").fetchone()[0]
    assert len(rows) == so, f"⛔ hàm đọc trả {len(rows)} / bảng {so} dòng"
    return rows


class _Bang(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hang: list[list[str]] = []
        self._o: list[str] | None = None
        self._than = False

    def handle_starttag(self, tag, attrs):
        if tag == "tbody":
            self._than = True
        elif tag == "tr" and self._than:
            self.hang.append([])
        elif tag == "td" and self._than:
            self._o = []

    def handle_endtag(self, tag):
        if tag == "td" and self._o is not None:
            self.hang[-1].append("".join(self._o).strip())
            self._o = None
        elif tag == "tbody":
            self._than = False

    def handle_data(self, data):
        if self._o is not None:
            self._o.append(data)


@can_node
def test_nhat_ky_SO_THAT_qua_man_THAT__nhan_khop_value_source_tung_dong():
    """⭐⭐ Lăng kính **dữ liệu × màn**: mọi dòng nhật ký sổ thật đi qua bảng ⑦.

    Quan hệ *(⛔ hằng số)*: hàng `may_goi_y` có giá trị ⇒ ô thành
    *"gợi ý: X"* đúng `X`; `may_goi_y` rỗng ⇒ *"rút gợi ý"*; `sua_tay` ⇒ nguồn
    *"người sửa"*; mã khác ⇒ nguyên mã. Mẫu số: `may_goi_y` có giá trị **> 0**
    *(02/10: **4.424** / **4.428**)*.

    Chứng minh ĐỎ: ô thành về `TP.chu(x.value_after)` ⇒ *"gợi ý:"* **0**
    hàng; nguồn in mã thô ⇒ nhãn máy **0** hàng.

    ⭐⭐ **Viết lại theo `BA-06` v4.12** *(`KQ-061`, 05/10 — `TL-058` giao
    `fls-test`; lo gốc **giữ**: nhãn khớp `value_source` từng dòng sổ thật)*.
    Oracle cũ *(v4.8: bản đảo `sua_tay` ⇒ ô trống, "chấp nhận · tập đóng")*
    đã bị v4.12 **lật** *(tập mở — nút `Đảo` trên mọi bút toán)*. Bốn đổi:
      ① gom theo **`(value_source, value_after, la_ban_dao)`** — hai dòng cùng
         `(nguồn, giá trị)` có thể khác `la_ban_dao` *(bản đảo người ↔ cú xoá
         ô: cả hai `sua_tay`, rỗng)*; gom hai trục là **⛔ thấy** trục thứ ba.
      ② ô **thành**: `la_ban_dao` ∧ `may_goi_y` ⇒ *"rút gợi ý"* · `la_ban_dao`
         ∧ `sua_tay` ⇒ *"đảo — giá trị này hết hiệu lực"* · ⛔ `la_ban_dao` ∧
         `sua_tay` ∧ rỗng ⇒ *"xoá ô"* · còn lại như v4.8. Cột **nguồn** ⛔ đổi.
      ③ **tiền đề đo được**: `la_ban_dao` là `bool` *(⛔ thiếu, ⛔ `null`)* ở
         **mọi** dòng hàm thật trả — ⛔ có ⇒ ĐỎ *"⛔ không đo được"*, ⛔ rơi im
         vào nhánh ⓔ của spec *(in như v4.8)*.
      ④ **tự chứng** *(quan hệ, ⛔ hằng)*: số dòng `la_ban_dao = true` = số
         bút toán đảo `fls_adjustment.reversal_of IS NOT NULL` *(mỗi bút toán
         một dòng nhật ký — đếm ở bảng KHÁC, ⛔ dựng lại câu `EXISTS`)* và
         **> 0** *(mẫu số nhánh ⓑ — `Đ3`)*; số hàng màn in *"đảo — …"* = số
         dòng `sua_tay` ∧ `la_ban_dao` *(theo bội số)*. Đo 05/10: `true`
         **2** / 4.428 *(UAT `27728` `cdt1` + `hd`)* · cú xoá ô người **0**.
    Chứng ĐỎ/XANH *(`KQ-061`)*: xanh @ `d1cea7c`; đỏ @ `7e67a09` ở tiền đề ③
    *(`KeyError`/thiếu `la_ban_dao`)*; đỏ trên `doc_bao_cao` mới ＋ `man_f02.js`
    @ `7e67a09` *(hai hàng `27728` in ô trống — đúng chiều `KQ-025 F-3`)*.
    """
    tat_ca = _nhat_ky_so_that()
    co_gt = sum(1 for x in tat_ca if x["value_source"] == "may_goi_y"
                and x["value_after"] not in (None, ""))
    assert co_gt > 0, "⛔ không đo được: sổ thật ⛔ có dòng máy gợi ý nào"
    # ③ tiền đề: trường `la_ban_dao` có mặt và là bool ở MỌI dòng.
    thieu = [x.get("jrn_id") for x in tat_ca
             if not isinstance(x.get("la_ban_dao"), bool)]
    assert thieu == [], (f"⛔ không đo được: {len(thieu)}/{len(tat_ca)} dòng "
                         f"hàm thật trả ⛔ có `la_ban_dao` bool: {thieu[:5]}")
    # ④ tự chứng: đếm bản đảo ở bảng KHÁC (`fls_adjustment`).
    with noi_chi_doc(dsn_that()) as c:
        so_dao = c.execute("SELECT count(*) FROM fls_adjustment"
                           " WHERE reversal_of IS NOT NULL").fetchone()[0]
    n_dao = sum(1 for x in tat_ca if x["la_ban_dao"])
    assert n_dao == so_dao, (f"⛔ la_ban_dao=true {n_dao} dòng ≠ bút toán đảo "
                             f"{so_dao} — phép nối nhật ký ↔ bút toán hỏng")
    assert n_dao > 0, "⛔ không đo được: sổ thật ⛔ có bản đảo nào (nhánh ⓑ rỗng)"
    # ⚠ 4.428 dòng ⇒ dòng lệnh `node -e` quá dài *(WinError 206)*. Ô thành/nguồn
    #   là hàm THUẦN của `(value_source, value_after, la_ban_dao)` ⇒ vẽ mỗi
    #   **dạng** một lần, đếm lại theo bội số. Mọi dòng sổ thật vẫn rơi vào
    #   một dạng đã vẽ.
    boi: dict[tuple, int] = {}
    mau: dict[tuple, dict] = {}
    for x in tat_ca:
        k = (x["value_source"], x["value_after"], x["la_ban_dao"])
        boi[k] = boi.get(k, 0) + 1
        mau.setdefault(k, x)
    nk = [mau[k] for k in boi]
    assert sum(boi.values()) == len(tat_ca)
    ra = _chay(("""
      _TRA['/ledger/101'] = {data: %s};
      _TRA['/journal'] = {data: {rows: %s}};
      HT.mo = () => ({dong(){}});
    """ % (json.dumps(DONG_DAY, ensure_ascii=False),
           json.dumps(nk, ensure_ascii=False, default=str))) + _VE + _BAM + """
      return document.querySelector('#so-panel').textContent;
    """)
    i = ra.find("⑦ Nhật ký")
    assert i >= 0, "⛔ không đo được: panel ⛔ có khối ⑦"
    p = _Bang()
    p.feed(ra[i:])
    hang = p.hang
    assert len(hang) == len(nk), (len(hang), len(nk))
    sai = []
    for x, h in zip(nk, hang):
        vs, va, dao = x["value_source"], x["value_after"], x["la_ban_dao"]
        rong = va in (None, "")
        if vs == "may_goi_y":
            mong = (RUT if (rong or dao) else f"gợi ý: {va}", NHAN_MAY)
        elif vs == "sua_tay":
            if dao:
                thanh = DAO
            elif rong:
                thanh = XOA_O
            else:
                thanh = str(va)
            mong = (thanh, NHAN_NGUOI)
        else:
            mong = ("" if rong else str(va), "" if vs is None else str(vs))
        if (h[3], h[5]) != mong:
            sai.append((x.get("itl_id"), x["field"], vs, dao, (h[3], h[5]), mong))
    assert sai == [], f"⛔ {len(sai)}/{len(nk)} dạng in sai: {sai[:5]}"
    so_goi_y = sum(boi[(x["value_source"], x["value_after"], x["la_ban_dao"])]
                   for x, h in zip(nk, hang) if h[3].startswith("gợi ý: "))
    assert so_goi_y == co_gt, (so_goi_y, co_gt)
    # ④ hàng màn in "đảo — …" = số dòng `sua_tay` ∧ `la_ban_dao` (bội số).
    so_dao_man = sum(boi[(x["value_source"], x["value_after"], x["la_ban_dao"])]
                     for x, h in zip(nk, hang) if h[3] == DAO)
    so_dao_nguoi = sum(1 for x in tat_ca
                       if x["value_source"] == "sua_tay" and x["la_ban_dao"])
    assert so_dao_man == so_dao_nguoi, (so_dao_man, so_dao_nguoi)


# ═══ ⓑ PHÁT HIỆN `KQ-019` — ✅ đã vá `9dae3ac` *(`WO-008` vòng 2)*; dấu `xfail(strict)`
#      GỠ ở `KQ-021` *(02/10 tối)*: cả 5 XPASS đúng lý do — đỏ trên `124a067`, đột biến
#      `M6`/`M11`/`M13` của `BG-020` làm `F2`/`F3`/`F4` đỏ lại. Giữ làm bài canh. ═════
@can_node
@pytest.mark.parametrize("ca", ["chum", "da_giao_dich"])
def test_F1_bo_gan_chum__HOI_TRUOC_that_su_hien(ca):
    """`BA-06` mục ⓔ: chùm ⇒ **hỏi trước** *(liệt kê tên)*; lệnh gắn ≥ 2 giao
    dịch ⇒ nói *"bỏ gán từ màn Sổ ITL"*. Mã gọi `HT.hoi(...)` — hàm ⛔ có ⇒
    `TypeError` trước cả `unmatch`. Sổ thật 02/10: **88 / 2.219** lệnh đã gán
    *(4,0%)* đi đường này."""
    if ca == "chum":
        r = _bo_gan(chum={"can_hoi": True, "so_dong": 2, "dong_lenh": [
            {"pm_line_id": "PWB-1", "amount": "3000000.00", "curr": "VND"},
            {"pm_line_id": "PWB-2", "amount": "2000000.00", "curr": "VND"}]},
            cho_xong=False)
        can = "CẢ 2"
    else:
        r = _bo_gan(lenh=dict(LENH, itl_da_gan=[4242, 4243]), cho_xong=False)
        can = "2 giao dịch"
    assert "is not a function" not in str(r["loi"]), r["loi"]
    h = r["hop"]
    assert h["mo"] is True and can in (h["t"] + h["b"]), h


@can_node
def test_F2_sau_bo_gan_THANH_CONG__man_khong_con_noi_DANG_GAN():
    """`bo_qua` rỗng *(02/10: **100%** cú bỏ gán trên sổ thật — `fls_sua_tay`
    **0**)* ⇒ ⛔ hộp; nếu màn cũng vẫn vẽ *"✓ Đang gán … bỏ gán"* thì người
    bấm **⛔ có một tín hiệu nào** rằng bỏ gán đã xảy ra. Mẫu số: khối có mặt
    **trước** cú bấm."""
    r = _bo_gan(than=dict(THAN_B, bo_qua=[]))
    assert "Đang gán với giao dịch" in r["truoc"], \
        "⛔ không đo được: màn ⛔ vẽ khối Đang gán trước cú bấm"
    assert r["unmatch"] == 1
    assert "Đang gán với giao dịch" not in r["man"], \
        "⛔ cửa đã bỏ gán, màn vẫn nói 'Đang gán'"


@can_node
def test_F3_bo_gan_cua_LOI__nguoi_THAY_loi():
    """`WO-008` Màn hình: *"mất kết nối — như nay (⛔ Cửa lỗi: Không nối được
    tới máy chủ FLS.)"*. Đo `8099` cắt mạng: `Uncaught (in promise) LoiCua` —
    ⛔ chữ nào trên màn."""
    cau = "Không nối được tới máy chủ FLS."
    r = _bo_gan(unmatch_no={"cau": cau, "ma": "FLS-MAT-KET-NOI"})
    assert r["unmatch"] == 1
    assert r["hop"]["t"] != "Đã bỏ ghép"
    assert cau in (r["hop"]["b"] if r["hop"]["mo"] else "") + r["man"], \
        "⛔ cửa lỗi mà màn ⛔ nói gì"


@can_node
def test_F4_ve_lai_lenh_LOI_sau_bo_gan__hop_bo_qua_VAN_mo():
    """Bỏ gán **đã ghi** *(cửa 200, `bo_qua` có giá trị người)*; vẽ lại lệnh
    lỗi *(`itl-candidates` 500)* ⇒ `bo_qua` vẫn *"phải hiện"* *(`BA-06`)*."""
    r = _bo_gan(ung_vien_no=True)
    assert r["unmatch"] == 1
    assert r["hop"]["mo"] is True and "HD-NGUOI-B2" in r["hop"]["b"], r
