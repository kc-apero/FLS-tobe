# -*- coding: utf-8 -*-
"""`WO-037` **vòng 2** `(i)` · `AC-12` — băng *"Việc của bạn hôm nay"* + bảng rổ
của `F01L` vẽ từ thân **`/lenh-cho/ro` CỬA THẬT** trên **kho TEST**
*(`BA-06` **v4.17** `§4.5 ⓤ` — chữ nguyên văn)*.

⛔⛔ Lỗi gốc *(`BG-039` yếu #1)*: dòng 2 của băng nói *"Chưa có số chứng từ"*
cho cả rổ `nguoi` — sổ thật 02/10 sai **84 / 616**; dòng ghi chú `may −
tu_chung` nói *"lệch tiền"* cho cả nhóm — đúng **78 / 120**. Màn nay nói **hai**
câu theo `a = nguoi − nguoi_khac_tien_te` · `b = nguoi_khac_tien_te` **của
cửa** — ⛔ màn tự đếm *(nó chỉ thấy một trang)*.

⛔ Luật của tệp *(`BA-07` §4h ⓵ — luật bài thử)*: thân lấy từ **cửa HTTP thật**
*(ca `tests/web/ca_wo037.dung_ca_wo037_v2`)*, đưa **nguyên văn** vào `_TRA`. Ca
biên `b = 0` đổi **giá trị** khoá của thân thật *(⛔ thêm / bớt khoá)*.

⭐ Chiều ĐỎ đã chạy trên JS khi nhận vòng 2 *(`4c3b2ae`)*: tiêu đề cũ *"CẦN BẠN
tra bằng tiền + ngày"* · `hint` cũ *"⛔ Chưa có số chứng từ…"* ⇒ ĐỎ.
"""
from __future__ import annotations

import json

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo032 import goi_ok
from tests.web.ca_wo037 import dung_ca_wo037_v2
from tests.web.khung_node import _chay, can_node
from tests.web.test_luat_ky_hieu_man_hinh import CAM
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg

RO = "/queue/lenh-cho/ro"

#: Chữ **nguyên văn** `BA-06` v4.17 `§4.5 ⓤ` *(chép từ spec — ⛔ đọc từ JS)*.
TIEU_DE = "CẦN BẠN tra — máy chưa đề xuất được dòng tiền"
CAU_1 = "{a} dòng chưa có số chứng từ: tra bằng tiền + ngày."
CAU_2 = (" {b} dòng có số chứng từ nhưng dòng tiền khớp mang tiền tệ khác: "
         "cửa ghi chưa ghép được hai tiền tệ.")
#: ⚠ *(`WO-042 (b)` ⓐ — `BA-06` **v4.18** `§4.5 ⓤ`, `KQ-041 F-1`)*: dòng ghi
#: chú đổi sang câu chung `LY_DO_LO` — chữ v4.17 *(biên bản: "… lệch tiền,
#: nhiều dòng tiền cùng mã, hoặc vướng một cổng khác của cửa ghi.")* gọi
#: `chum_lech_tien` sai tên và ⛔ nói cổng `co_dong_chua_duyet`. Lo gốc của bài
#: **giữ nguyên**: `c` là số **cửa** trả, ⛔ màn đếm; ba chuỗi còn lại vẫn v4.17.
#: Chữ chép **nguyên văn** từ spec v4.18 *(⛔ đọc từ JS)* — bài `WO-042`
#: `test_wo042_bon_chuoi_f01l_cua_that.py` canh thêm ⓑ ⓒ ⓓ.
GHI_CHU = ("Còn {c} dòng khớp số chứng từ cùng tiền tệ nhưng cửa ghi chưa nhận "
           "theo lô — lệch tiền, nhiều dòng tiền cùng mã, một dòng tiền mang mã "
           "của nhiều dòng lệnh mà tổng các dòng lệnh khác tiền bank, có dòng "
           "lệnh cùng chùm chưa được duyệt, hoặc vướng một cổng khác của cửa "
           "ghi. Phải mở từng dòng.")
RO_NGUOI = ("Máy chưa đề xuất được dòng tiền — chưa có số chứng từ, hoặc số "
            "chứng từ khớp một dòng tiền bằng tiền tệ khác. Mỗi dòng nói vì sao.")


@pytest.fixture(scope="module")
def than_ro():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        dung_ca_wo037_v2(c)
    with _may() as m:
        return goi_ok(m, RO)["data"]


_VE = """
  const TRA = %(than)s;
  _TRA['/queue/lenh-cho/ro'] = {data: TRA};
  const o = document.createElement('div'); document.body.appendChild(o);
  await F01L.ve_viec(o);
  const v = o.querySelectorAll('.viec');
  const d2 = v[1] ? v[1].children[1] : null;
  const ghi = o.querySelectorAll('.note');
  const r = document.createElement('div'); document.body.appendChild(r);
  await F01L.ve_ro(r);
  const tr = r.querySelectorAll('tr').filter(x => x.textContent.includes('cần người tra'));
  return {so_viec: v.length,
          tieu_de: d2 ? d2.children[0].textContent : null,
          hint: d2 ? d2.children[1].textContent : null,
          ghi_chu: ghi.map(x => x.textContent),
          ro_nguoi: tr.length ? tr[0].children[2].textContent : null,
          goi: _GOI.map(g => g[1])};
"""


def _ve(than: dict) -> dict:
    return _chay(_VE % {"than": json.dumps(than, ensure_ascii=False)},
                 tep=TEP_F01, vo=VO_F01)


def _cam(*s: str) -> list[str]:
    return sorted({ch for x in s for ch in (x or "") if ch in CAM})


@can_node
def test_AC12_bang_F01L_DUNG_chu_v4_17_so_tu_CUA(than_ro):
    """Ca `K N T M` ⇒ `a = 2 · b = 1 · c = 1`. Bốn chuỗi **=** chữ `§4.5 ⓤ`;
    **0** ký tự `CAM`; màn chỉ gọi `/lenh-cho/ro` *(⛔ tự đếm từ trang)*."""
    d = than_ro
    a, b = d["nguoi"] - d["nguoi_khac_tien_te"], d["nguoi_khac_tien_te"]
    c = d["may"] - d["tu_chung"]
    print(f"WO-037 AC-12 · /ro {d} ⇒ a {a} · b {b} · c {c}")
    assert (a, b, c) == (2, 1, 1), ("⛔ ca dựng sai — không đo được", d)
    r = _ve(d)
    assert r["so_viec"] == 3, r
    assert r["tieu_de"] == TIEU_DE, r
    assert r["hint"] == CAU_1.format(a=a) + CAU_2.format(b=b), r
    assert r["ghi_chu"] == [GHI_CHU.format(c=c) + " Xem 1 dòng"], r
    assert r["ro_nguoi"] == RO_NGUOI, r
    assert "lệch tiền — trả nhiều đợt" not in json.dumps(r, ensure_ascii=False)
    assert not _cam(r["tieu_de"], r["hint"], *r["ghi_chu"], r["ro_nguoi"]), r
    assert set(r["goi"]) == {RO}, r["goi"]


@can_node
def test_AC12_b_BANG_0_chi_cau_MOT(than_ro):
    """Ca biên `b = 0` *(đổi **giá trị** khoá thân thật)* ⇒ `hint` **chỉ** câu
    ①, với `a = nguoi` *(⛔ giấu câu khi `a = 0` — xem bài dưới)*."""
    d = dict(than_ro, nguoi_khac_tien_te=0)
    r = _ve(d)
    assert r["hint"] == CAU_1.format(a=d["nguoi"]), r


@can_node
def test_AC12_a_BANG_0_van_in_cau_MOT(than_ro):
    """Ca biên `a = 0 ∧ b > 0` ⇒ câu ① in `0 dòng…` *(`§4.5 ⓤ`: một con số `0`
    là một câu trả lời)* ＋ câu ②."""
    d = dict(than_ro, nguoi_khac_tien_te=than_ro["nguoi"])
    r = _ve(d)
    assert r["hint"] == CAU_1.format(a=0) + CAU_2.format(b=d["nguoi"]), r


@can_node
def test_AC12_so_LA_DOC_TU_THAN_cua(than_ro):
    """⛔ Chiều ĐỎ *"màn tự đếm `b`"*: đổi **giá trị** `nguoi_khac_tien_te` của
    thân thật sang một số ⛔ trang nào cho ra *(`nguoi` giữ nguyên)* ⇒ `hint`
    phải in **đúng** số ấy."""
    d = dict(than_ro, nguoi=1234, nguoi_khac_tien_te=1000)
    r = _ve(d)
    assert r["hint"] == CAU_1.format(a="234") + CAU_2.format(b="1.000"), r
