# -*- coding: utf-8 -*-
"""`WO-023` `(c)` + `(d)` phía **màn** · `BA-06` **v4.11** `ⓕ3` · `ⓕ4`.

  `(c)` cửa **GHI** có hạn chờ *(`30 s` — một hằng, bài đặt nhỏ)* ⇒ `LoiCua`
        mã **`FLS-HET-GIO`** *(mã phía màn)*; ⛔ được nói *"chưa xảy ra"*: lượt
        ghi có thể **đã** vào sổ. Cửa **đọc** ⛔ có hạn.
  `(d)` `goi_cua.js::CAU` ba câu mới **nguyên văn** `ⓕ4`.

⛔⛔ Lỗi gốc *(mã khi nhận `7e67a09`)*: `fls/web/tep` **0** dòng `timeout` /
`AbortController` *(đo `BA-06` v4.11, 02/10)* ⇒ một lượt ghi treo giữ hộp `ⓕ2`
**mãi**; ba mã `409` mới ⛔ có câu ⇒ `LoiCua` in *"Lỗi chưa được mô tả: …"*.

⭐ Chữ **nguyên văn** lấy từ **chính** `06_SCREEN_SPEC.md` *(oracle đọc bảng
`ⓕ3`/`ⓕ4`)* — ⛔ chép tay vào bài: spec đổi chữ thì bài đỏ, ⛔ xanh trên bản
chép cũ. ⚠ `goi_cua.js` ⛔ có hàm `dich` *(`grep -n "function dich"` **0**;
chú thích `:26` nhắc tên ấy)* — phép dịch nằm ở **hàm dựng `LoiCua`** *(mã
⛔ khai ⇒ `cau = 'Lỗi chưa được mô tả: <mã>'` + `console.error`)*.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo023 import dung_ca_wo023
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, _may
from tests.web.test_wo023_ab_hop_modal_va_hop_cho_cua import (
    CHUM2, TEP_F01, VO_F01, _ghep, _lenh)

pytestmark = [can_node]

SPEC = Path(__file__).resolve().parents[2] / "docs" / "ITL" / "02_BA" / "06_SCREEN_SPEC.md"


def _dong_spec(nhan: str) -> str:
    dong = [d for d in SPEC.read_text(encoding="utf-8").splitlines()
            if d.startswith("| " + nhan + " |")]
    assert len(dong) == 1, (nhan, len(dong))
    return dong[0]


def _cau_f4() -> dict:
    """`{mã: (cau, lam_gi)}` từ dòng `ⓕ4` — khuôn `` `MÃ` *"câu"* / *"làm gì"* ``."""
    d = _dong_spec("ⓕ4")
    ra = {m: (c, l) for m, c, l in re.findall(
        r"`(FLS-[A-Z-]+)` \*\"([^\"]+)\"\* / \*\"([^\"]+)\"\*", d)}
    assert set(ra) == {"FLS-DA-GHEP", "FLS-KHONG-CON-MOI-NOI", "FLS-CHUA-XONG"}, ra
    return ra


def _cau_f3() -> tuple[str, str]:
    d = _dong_spec("ⓕ3")
    c = re.search(r"câu \*\"([^\"]+)\"\*", d).group(1)
    l = re.search(r"`lam_gi` \*\"([^\"]+)\"\*", d).group(1)
    return c, l


def test_AC4_ba_ma_moi_CAU_nguyen_van_BA06_f4():
    """Mỗi mã ⇒ `LoiCua.cau` / `lam_gi` **trùng từng byte** `ⓕ4`. ⛔ Chiều ĐỎ:
    thiếu câu ⇒ `cau = 'Lỗi chưa được mô tả: …'`."""
    mong = _cau_f4()
    r = _chay("""
      const ra = {};
      for (const m of %s) { const e = new FLS.LoiCua(m, 409); ra[m] = [e.cau, e.lam_gi]; }
      ra.cu = [new FLS.LoiCua('FLS-CONFLICT-SOURCE', 409).cau];
      return ra;
    """ % json.dumps(sorted(mong)), tep=TEP_F01, vo=VO_F01)
    for m, (c, l) in mong.items():
        assert r[m] == [c, l], (m, r[m], (c, l))
    assert r["cu"] == ["Giá trị bạn gõ khác với giá trị nguồn đang có."], r["cu"]


# ══ (c) hạn chờ cửa GHI ═════════════════════════════════════════════════

_TREO = """
  globalThis.fetch = function () { return new Promise(() => {}); };
  FLS.ghi = (d, t) => { _GOI.push(['ghi', d, t]); return FLS.goi(d, {phuong_thuc: 'POST', than: t}); };
  FLS.HAN_CHO.ghi_ms = 40;
"""


def test_AC3_GHI_treo_qua_han__FLS_HET_GIO_cau_nguyen_van__DOC_treo_KHONG_het_gio():
    """⛔ Chiều ĐỎ: bỏ hạn chờ ⇒ ⛔ lỗi ⇒ `ghi` ⛔ xong; hạn chờ áp cả cửa đọc ⇒
    `doc` ra `FLS-HET-GIO` ⇒ ĐỎ."""
    c, l = _cau_f3()
    r = _chay(_TREO + """
      const ghi = FLS.goi('/queue/1/unmatch', {phuong_thuc: 'POST', than: {}})
        .then(() => 'xong', e => [e.ma, e.cau, e.lam_gi]);
      let doc = 'chua';
      FLS.goi('/queue').then(() => { doc = 'xong'; }, e => { doc = e.ma; });
      await new Promise(r => setTimeout(r, 150));
      return {ghi: await Promise.race([ghi, new Promise(r => setTimeout(() => r('treo'), 50))]),
              doc, han: (() => { FLS.HAN_CHO.ghi_ms = 30000; return true; })()};
    """, tep=TEP_F01, vo=VO_F01)
    assert r["ghi"] == ["FLS-HET-GIO", c, l], r
    assert r["doc"] == "chua", f"⛔ cửa ĐỌC cũng bị hạn chờ: {r['doc']}"


def test_AC3_hang_HAN_mac_dinh_la_30_giay():
    r = _chay("return FLS.HAN_CHO.ghi_ms;", tep=TEP_F01, vo=VO_F01)
    assert r == 30000, r


def test_AC3_HET_GIO_trong_hop_GO_CA_N__loi_trong_hop_nut_mo_lai():
    c, _ = _cau_f3()
    r = _ghep("man_truoc", _TREO + """
      _bam_man('Bỏ gán'); await _ngu(30);
      const p = _bam_hop('Gỡ cả 2'); await _ngu(150); await p; await _ngu(20);
      return {h: _hop(), unmatch: _dem(/\\/unmatch$/)};
    """)
    assert r["unmatch"] == 1, r
    assert r["h"]["mo"] is True and c in r["h"]["b"], r["h"]
    assert not any(d for _, d in r["h"]["nut"]), r["h"]


def test_AC3_HET_GIO_ngoai_hop_ca5__CHUA_RO_bo_gan_da_xay_ra_chua():
    """Ca ⑤ *(một dòng tiền, ⛔ chùm ⇒ ghi ngay, ⛔ hộp)*. ⛔ Chiều ĐỎ: in
    *"Bỏ gán chưa xảy ra"* khi ⛔ biết."""
    r = _ghep("man_truoc", _TREO + """
      await (async () => { _bam_man('Bỏ gán'); })(); await _ngu(150); await _ngu(20);
      return {man: document.getElementById('ghep-goc').textContent, unmatch: _dem(/\\/unmatch$/)};
    """, tra={"/queue/4242/chum": {"itl_id": 4242, "can_hoi": False, "so_dong": 1,
                                   "dong_lenh": []}})
    assert r["unmatch"] == 1, r
    assert "Chưa rõ bỏ gán đã xảy ra chưa — Cửa lỗi: Máy chưa trả lời sau 30 giây" in r["man"], r["man"][-400:]
    assert "Bỏ gán chưa xảy ra" not in r["man"], r["man"][-400:]


def test_AC3_HET_GIO_cu_GAN__CHUA_RO_gan_da_xay_ra_chua():
    """`ⓕ3` *"⛔ được nói chưa xảy ra"* cho cú `Gán` *(khuôn chữ theo `Bỏ gán`
    — `HOI-056`)*. ⛔ Chiều ĐỎ: `Gán chưa xảy ra` khi ⛔ biết."""
    r = _ghep("man_truoc", _TREO + """
      F01G.ST.ung_vien = [{itl_id: 7, bac: 'tien', amount: '5000000.00', curr: 'VND'}];
      F01G.ST.ung_vien_chon = 0; F01G.ve();
      await F01G.gan(F01G.ST.dong[0]); await _ngu(20);
      return {man: document.getElementById('ghep-goc').textContent, ghi: _dem(/\\/match$/)};
    """, dong=[_lenh("PWB-1", [])])
    assert r["ghi"] == 1, r
    assert "Chưa rõ gán đã xảy ra chưa — Cửa lỗi: Máy chưa trả lời sau 30 giây" in r["man"], r["man"][-300:]
    assert "Gán chưa xảy ra" not in r["man"], r["man"][-300:]


@pytest.mark.pg
def test_AC3_rui_ro_3_het_gio_roi_BAM_LAI__409_moi_noi_dung_chuyen():
    """`WO-023` Rủi ro 3: lượt đầu **đã** vào sổ mà màn hết giờ ⇒ bấm lại ⇒
    cửa `409` `FLS-KHONG-CON-MOI-NOI` — **câu đúng**. Thân `409` **từ cửa
    thật** kho TEST *(`unmatch` một dòng ⛔ mối nối)*. Mong *(`AC-4` ca **K**)*:
    `#ghep-goc` chứa *"…không còn gán với lệnh nào — có thể vừa có người bỏ gán
    trước bạn."*; ⛔ *"Giá trị bạn gõ khác"*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo023(c)
    with _may() as m:
        st, than = _goi(m, f"{V}/queue/{ca['i']['M3']}/unmatch", pt="POST", than={})
    assert st == 409, (st, than)
    cau = _cau_f4()["FLS-KHONG-CON-MOI-NOI"][0]
    r = _ghep("man_truoc", """
      let lan = 0;
      const TRA_409 = %s;
      globalThis.fetch = function () {
        lan++;
        if (lan === 1) return new Promise(() => {});
        return Promise.resolve({status: 409, ok: false, json: async () => TRA_409});
      };
      FLS.ghi = (d, t) => { _GOI.push(['ghi', d, t]); return FLS.goi(d, {phuong_thuc: 'POST', than: t}); };
      FLS.HAN_CHO.ghi_ms = 40;
      _bam_man('Bỏ gán'); await _ngu(150);
      const lan1 = document.getElementById('ghep-goc').textContent;
      _bam_man('Bỏ gán'); await _ngu(60);
      return {lan1, lan2: document.getElementById('ghep-goc').textContent,
              unmatch: _dem(/\\/unmatch$/)};
    """ % json.dumps(than, ensure_ascii=False),
        tra={"/queue/4242/chum": {"itl_id": 4242, "can_hoi": False, "so_dong": 1,
                                  "dong_lenh": []}})
    assert r["unmatch"] == 2, r
    assert "Chưa rõ bỏ gán đã xảy ra chưa" in r["lan1"], r["lan1"][-300:]
    assert "Bỏ gán chưa xảy ra — Cửa lỗi: " + cau in r["lan2"], r["lan2"][-300:]
    assert "Giá trị bạn gõ khác" not in r["lan2"], r["lan2"][-300:]
