# -*- coding: utf-8 -*-
"""`KQ-050` *(kiểm `BG-048` — `WO-045`)* · vùng ứng viên `F01G` khi lượt **ô tìm**
là lượt mới nhất.

⭐ Cách tìm *(`fls-test` 05/10, đọc diff `2b804e3` `man_f01_ghep.js`)*: `WO-045`
cho `mo_lenh` và ô tìm chung **một** bộ đếm `_luot_uv` *(đúng)*, và thêm khung
`Đang hỏi sổ…` *(`ST.dang_tai_uv = true`)* khi đổi lệnh. Nhưng **chỉ** `mo_lenh`
có nhánh `catch` đặt lỗi lên màn *(`_loi_uv`)*; `_tai_toan_so` lỗi thì **ném**
lên trình nghe `input` *(`setTimeout` async — ⛔ ai bắt)*, ⛔ tắt
`ST.dang_tai_uv`, ⛔ đặt `ST.loi_uv`. Hai hệ quả, hai bài:

  `F-2` · đổi lệnh *(khung `Đang hỏi sổ…` bật)*, gõ ô tìm trong lúc lệnh mới
        đang tải ⇒ lượt chữ **thay** lượt lệnh *(đúng `ⓦ` ①)*; lượt chữ ấy
        **lỗi** ⇒ khung `Đang hỏi sổ…` **treo mãi** — ⛔ còn lượt nào bay, ⛔
        câu lỗi. `WO-045` bảng *Màn hình*: lỗi = *"lỗi của lượt **mới nhất**"*;
        `BA-06` v4.21 `ⓦ` ④ hàng *lỗi*: *"✅ câu"* *(và nút `Thử lại` của nó
        nói rõ *"ô tìm có chữ ⇒ tra lại chữ ấy"* — tức lượt chữ **có** trạng
        thái lỗi)*.
  `F-3` · lựa chọn `ST.ung_vien_chon` là **chỉ số** vào danh sách; lượt chữ
        mới nhất thay danh sách mà ⛔ bỏ lựa chọn ⇒ hàng người **đã bấm**
        *(của kết quả chữ trước)* thành **một hàng khác** của kết quả chữ mới,
        được tô sẵn; `Gán` gửi `itl_id` người ⛔ chọn. Cùng lệnh *(⛔ sai cặp
        lệnh)*, có từ trước `WO-045`.

⛔ Ghi **kho TEST** *(ca `dung_ca_cung_te` — `assert current_database()`)*. Thân
cửa **thật** *(HTTP `_may()` kho TEST)*, độ trễ **có kiểm soát** *(cửa giả giữ —
`tests/web/khung_giu.py`)*.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo032 import goi_ok
from tests.nghiem_thu.test_kq050_cap_sai_cung_tien_te import dung_ca_cung_te
from tests.web.khung_giu import CUA_GIU, nap
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = [pytest.mark.pg, can_node]

#: ⭐ Trình nghe ô tìm chạy trong `setTimeout(async …)`: lỗi nó ném là
#: `Uncaught (in promise)` trên trình duyệt *(màn sống tiếp)*, nhưng trong khung
#: `node` `vm` nó **làm sập** tiến trình ⇒ bài ⛔ đo được gì. Bọc `setTimeout`
#: của **khung** *(⛔ mã màn)* để ghi lỗi lại như console trình duyệt — chính nó
#: là bằng chứng `Uncaught` *(`ⓦ` ⑤ ⓑ — `WO-023` `(h)`, ⛔ điều bài này đòi)*.
_BAT = """
globalThis._KHONG_BAT = [];
{
  const st = globalThis.setTimeout;
  globalThis.setTimeout = function (f, ms) {
    return st(function () {
      const r = f();
      if (r && typeof r.catch === 'function')
        r.catch(e => _KHONG_BAT.push(String(e && e.message || e)));
    }, ms);
  };
}
"""


@pytest.fixture(scope="module")
def ca_tra():
    # ⚠ ca **nhỏ** *(2 dòng tiền VND)*, ⛔ `dung_ca_wo045` *(58 dòng VND)*: kho
    #   TEST dùng chung phạm vi `chi_nap_that` cho mọi lần nạp ⇒ thêm một bộ
    #   58 dòng ở đây làm bài Dev `test_AC7_doi_MUC_PHU_*` ra *"⛔ không đo
    #   được: 50% ⛔ khác tất cả"* *(đo 05/10 — `KQ-050 F-4`)*.
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_cung_te(c)
    ca["lenh"] = {"A": ca["lenh"]["X"], "B": ca["lenh"]["Y"]}
    ca["doc"] = {"A": ca["doc"]["X"], "B": ca["doc"]["Y"]}
    L, doc = ca["lenh"], ca["doc"]
    A, B = L["A"], L["B"]
    D = {
        "g_nguoi": "/queue/lenh-cho?ro=nguoi&limit=500",
        "g_may": "/queue/lenh-cho?ro=may&tu_chung=0&limit=500",
        "uv_A": f"/queue/lenh/{A}/itl-candidates",
        "uv_B": f"/queue/lenh/{B}/itl-candidates",
        "so_B_qA": f"/queue/lenh/{B}/so?q={doc['A']}",
        "so_B_qB": f"/queue/lenh/{B}/so?q={doc['B']}",
    }
    with _may() as m:
        TRA = {d: goi_ok(m, d) for d in D.values()}
    return ca, D, TRA


def _ids(env: dict) -> list:
    return [u["itl_id"] for u in (env["data"] or {}).get("ung_vien") or []]


def _js(tra: dict, kich_ban: str) -> dict:
    return _chay(_BAT + CUA_GIU + nap(tra) + kich_ban, tep=TEP_F01, vo=VO_F01)


_GO = """
  const go = async (q) => {
    _ban('input', {target: {id: 'ghep-tim', value: q}});
    await new Promise(r => setTimeout(r, F01G.TRE_TIM + 80)); await _cho();
  };
"""


# ✅ *(`KQ-061`, 05/10)* dấu `xfail(strict)` GỠ — XPASS đúng lý do: xanh @ `d1cea7c`, đỏ @ `7e67a09` (`khung chờ TREO sau khi lượt mới nhất đã lỗi`). Lý do cũ: KQ-050 F-2 (NHE → DEV): lượt ô tìm  lỗi khi lệnh mới đang tải ⇒ khung 'Đang hỏi sổ…' treo, ⛔  câu lỗi — man_f01_ghep.js _tai_toan_so ⛔ _loi_uv
def test_F2_tim_LOI_khi_lenh_moi_dang_tai_KHUNG_TAI_khong_duoc_treo(ca_tra):
    """`A` đã mở *(danh sách về)*. `j`-tương-đương: `mo_lenh(B)` với
    `itl-candidates` của `B` bị **giữ** ⇒ khung `Đang hỏi sổ…`. Gõ số CT của
    `B` vào ô tìm *(quá `TRE_TIM`)* ⇒ lượt chữ là lượt **mới nhất**; cửa `/so`
    **lỗi**; rồi thả lượt lệnh `B` *(đã bị thay — đúng phải bị bỏ)*.

    Mong *(`WO-045` bảng Màn hình hàng lỗi · `BA-06` v4.21 `ⓦ` ④)*: ⛔ còn
    `Đang hỏi sổ…`; vùng ứng viên in `⛔ Cửa lỗi: <câu>` của lượt chữ.
    ⛔ Chiều ĐỎ *(mã `2b804e3`)*: `ST.dang_tai_uv` vẫn `true`, khung chờ treo,
    ⛔ câu lỗi; lỗi chỉ rơi ra `unhandledRejection`."""
    ca, D, TRA = ca_tra
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    assert _ids(TRA[D["uv_A"]]) and _ids(TRA[D["uv_B"]]), "⛔ không đo được: rỗng"
    r = _js(TRA, _GO + f"""
      await F01G.mo_man(); await _cho();
      await F01G.mo_lenh({A!r}); await _cho();
      const truoc = F01G.ST.ung_vien.length;
      _GIU.push('/itl-candidates'); _GIU.push('/so?');
      const pb = F01G.mo_lenh({B!r}).catch(e => 'ném: ' + e.message); await _cho();
      const khung_dau = document.querySelector('.cands').textContent;
      await go({ca['doc']['B']!r});
      const bay = _doc('/so?');
      await _no('/so?', new FLS.LoiCua('FLS-INTERNAL', 500, 'kq050'));
      await _tha('/lenh/{B}/itl-candidates');
      await new Promise(r => setTimeout(r, 50)); await _cho();
      return {{truoc, khung_dau, bay, ra_b: await pb, mo: F01G.ST.mo,
               dang: F01G.ST.dang_tai_uv, loi_uv: F01G.ST.loi_uv,
               cands: document.querySelector('.cands').textContent,
               khong_bat: _KHONG_BAT}};
    """)
    # ⭐ tự chứng kịch bản đúng ca *(Đ3 — mẫu số)*
    assert r["truoc"] > 0, r
    assert "Đang hỏi sổ…" in r["khung_dau"], ("⛔ không đo được: khung tải "
                                             "⛔ bật khi đổi lệnh", r)
    assert len(r["bay"]) == 1, ("⛔ không đo được: lượt chữ ⛔ bay", r["bay"])
    assert r["mo"] == B, r
    # ⭐ mong
    assert "Đang hỏi sổ…" not in r["cands"], ("⛔ khung chờ TREO sau khi lượt "
                                              "mới nhất đã lỗi", r)
    assert not r["dang"], r
    assert "⛔ Cửa lỗi: Máy gặp lỗi bên trong." in r["cands"], r["cands"][-300:]


# ✅ *(`KQ-061`, 05/10)* dấu `xfail(strict)` GỠ — XPASS đúng lý do: xanh @ `d1cea7c`, đỏ @ `7e67a09` (`Gán gửi itl_id người ⛔ chọn: /queue/1696/match (đã bấm 1695)`). Lý do cũ: KQ-050 F-3 (NHE → BA): lượt ô tìm  mới nhất thay danh sách mà ⛔ bỏ ST.ung_vien_chon (chỉ số)  ⇒ Gán gửi itl_id người ⛔ chọn
def test_F3_chon_hang_roi_luot_tim_moi_ve_GAN_khong_gui_hang_nguoi_khong_chon(ca_tra):
    """Mở `B`; gõ `q1` *(số CT dòng tiền `A`)* ⇒ kết quả `q1` lên màn; gõ `q2`
    *(số CT `B`)* — lượt `q2` **giữ**; trong lúc chờ, người bấm hàng **đầu**
    của danh sách đang hiện *(kết quả `q1`)*; thả `q2`; bấm `Gán` *(hai lần nếu
    xác nhận lệch)*.

    Mong: cú ghi *(nếu có)* chỉ mang `itl_id` **người đã bấm**; danh sách mới
    thay ⇒ lựa chọn bỏ *(`ST.ung_vien_chon = null` — "⛔ chọn sẵn")*.
    ⛔ Chiều ĐỎ *(mã `2b804e3`, và `db0adae`)*: `ung_vien_chon` giữ chỉ số `0`
    ⇒ hàng đầu của `q2` được tô, `Gán` gửi nó."""
    ca, D, TRA = ca_tra
    B = ca["lenh"]["B"]
    k1, k2 = _ids(TRA[D["so_B_qA"]]), _ids(TRA[D["so_B_qB"]])
    assert k1 and k2 and not set(k1) & set(k2), ("⛔ không đo được: hai kết quả "
                                                  "tìm rỗng hoặc chồng", k1, k2)
    r = _js(TRA, _GO + f"""
      await F01G.mo_man(); await _cho();
      await F01G.mo_lenh({B!r}); await _cho();
      await go({ca['doc']['A']!r});
      const q1 = F01G.ST.ung_vien.map(u => u.itl_id);
      _GIU.push('/so?');
      await go({ca['doc']['B']!r});
      const hang = document.querySelectorAll('.cands .cand');
      const da_bam = q1[0];
      _bam(hang[0]); await _cho();
      const chon_truoc = F01G.ST.ung_vien_chon;
      await _tha('q={ca['doc']['B']}');
      const sau = {{uv: F01G.ST.ung_vien.map(u => u.itl_id), chon: F01G.ST.ung_vien_chon}};
      for (let k = 0; k < 2 && !_ghi().length; k++) {{
        const g = document.querySelectorAll('.act button')[0];
        _bam(g); await _cho();
      }}
      return {{q1, da_bam, chon_truoc, sau, ghi: _ghi()}};
    """)
    assert r["q1"] == k1, ("⛔ không đo được: danh sách q1 ⛔ lên màn", r)
    assert r["chon_truoc"] == 0, ("⛔ không đo được: cú bấm hàng ⛔ chọn", r)
    assert r["sau"]["uv"] == k2, r
    sai = [g for g in r["ghi"] if int(g[0].split("/")[2]) != r["da_bam"]]
    assert not sai, (f"⛔ Gán gửi itl_id người ⛔ chọn: {sai} "
                     f"(đã bấm {r['da_bam']})")
    assert r["sau"]["chon"] is None, r["sau"]
