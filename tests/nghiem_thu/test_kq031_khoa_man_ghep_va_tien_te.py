# -*- coding: utf-8 -*-
"""`KQ-031` *(kiểm `BG-030` — `WO-022` vòng 3)* · đo **mọi** hàm màn `F01L` +
`F01G` đọc thân cửa so với khoá **cửa thật**, và phép lệch của hộp *"Tìm tiền"*
khi ứng viên **khác tiền tệ**.

⭐ Cách đo *(`fls-test`, 02/10, máy `8088` sổ thật — chỉ `GET`)*: gom thân **89**
lượt gọi cửa thật *(`lenh-cho` 8 biến thể · `lenh-da-gan` · `itl-candidates` /
`lenh/{id}` ×34 lệnh · `/so` ×6 · `/chum` ×4)*, rồi với **28** cặp *(hàm, biến)*
của hai màn đếm mỗi khoá màn đọc có mặt ở bao nhiêu phần tử thân cửa *(mẫu số
in kèm)*. `F01L`: **0** khoá thiếu ở **14** cặp *(mẫu số 1…1.468)*. `F01G`: hai
chỗ — dưới đây.

ⓐ **`F-3` *(`NHE`)*** — khối *"✓ Đang gán với giao dịch"* `F01G.ve_dang_gan`
   đọc `g.khoa_to` *(tô `<mark>` bằng chứng)*, nhưng `the.gd` của **cả hai** cửa
   danh sách ⛔ bao giờ mang khoá ấy *(`fls/api/xu_ly.py::_gan_gd` dựng `gd` bằng
   `khuon_ung_vien` **không** qua `_gan_khoa_to`)*: sổ thật **0/768** `gd`. Bài
   Dev của khối này **tự nhét** `"khoa_to": ["LUONG"]`
   *(`tests/web/test_b3_cuon_va_khoi_dang_gan.py:34`)* — **lần thứ ba** cùng lớp
   *"khuôn thử tự nhét che chỗ màn đọc khoá cửa ⛔ trả"* *(`KQ-019` `HT.hoi` ·
   `KQ-029` `F-1`)*. Hậu quả nhẹ: chữ ⛔ được tô — ⛔ sai số.
ⓑ **`F-2` *(`NHE`)*** — ứng viên bậc `ma` luôn có `lech = null`
   *(`lenh_cho.py:420`)*, kể cả khi tiền **khác** tiền lệnh; `BA-07 §4h ⓵` khai
   `lech` = *"amount ứng viên − dòng lệnh · `null` khi **khớp tuyệt đối**"*. Sổ
   thật, **268** lệnh rổ `may`: bậc `ma` **448** ứng viên, **338** có tiền ≠
   tiền lệnh mà `lech = null` ⇒ cột `Lệch` hộp `F01L` in `—`, nhãn xác nhận
   `F01G.ve_thanh` bỏ mất *"(lệch …)"*.
ⓒ **`F-1` *(`NHE`)*** — `F01L._drawer_tim_tien::_tinh` trừ tiền **hai đơn vị
   khác nhau** *(⛔ so `u.curr` với `r.curr`; `F01G.khop_dung_tien` thì có so)*.
   Sổ thật: **165/5.360** ứng viên khác tiền tệ lệnh *(lệch in ra vô nghĩa, vd.
   `14.800 HKD ↔ 1.910 USD` ⇒ *"lệch 12.890,00"*)*, và **4** lệnh có ứng viên
   bậc `ma` **cùng số khác tiền tệ** ⇒ hộp in *"lệch 0 ⇒ trong dung sai"* *(lớp
   `note ok`)* cho một cặp **cửa ghi từ chối** *(`ghi_tay.ghep_lenh` ⓔ
   `KhacTienTe`)* — đo Chrome `8088` lệnh `PM00329-1` *(`100.000 VND` ↔ ứng
   viên `100.000,00` USD)*. Lỗi có từ trước vòng 3, nhưng trước vòng 3 hộp nói
   *"VƯỢT"* với **mọi** ứng viên nên ca này **bị che**; vòng 3 làm nó lộ ra.

Dữ liệu: kho **TEST** *(assert `current_database() = 'fls_test'`)*, run
`NAP-2000-01-01-T…`, cửa thật qua HTTP. Tiền ngẫu nhiên mỗi lần *(kho TEST
phình — `BG-030` yếu #7)*.
"""
from __future__ import annotations

import json
import os
import random
import uuid
from decimal import Decimal as D

import pytest

from fls.adapters.pm_join import DongPM, canon_ref
from fls.ledger.build import NgucCanh
from fls.repo import ghi_tay as gt
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import mot_lan_nap
from fls.web import phuc_vu as pv_web
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import conn  # noqa: F401
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01
from tests.web.test_wo022_v3_tim_tien_cua_that import _than_ham, khoa_man_doc

pytestmark = pytest.mark.pg

TEP_F01G = os.path.join(pv_web.THU_MUC, "man_f01_ghep.js")
ACTOR = "fls-test@apero.vn"


def _tien(conn, run: str, khoa: str, so: int, tien: str, curr: str,  # noqa: F811
          doc: str) -> int:
    """Một dòng `fls_itl` chưa nối, nguồn **đúng khuôn** `<tk>_<bank> <curr>_<le>`
    *(⇒ `nguon` tách được, ⛔ `loi_nguon`)*; ⛔ chụp ⇒ `dien_giai = null`."""
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW',%s,%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, khoa, so, run, doc, curr, D(tien))).fetchone()[0]


@pytest.fixture()
def ca(conn, may):  # noqa: F811
    """Ba lệnh trong **một** lần nạp *(ảnh PM hiệu lực của máy thử)*:

      `A` VND `<a>`        ↔ dòng tiền VND `<a>+1.000.000` mang ĐÚNG số CT ⇒ bậc `ma`, tiền lệch
      `B` VND `<b>`        ↔ dòng tiền VND `<b>` — **đã gán** *(`ghep_lenh` thật)*
      `X` HKD `<m>.00`     ↔ dòng tiền **USD** `<m>.00` mang ĐÚNG số CT ⇒ bậc `ma`, khác tiền tệ
    """
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ bài này chỉ dựng trên kho TEST, gặp {db!r}"
    run = "NAP-2000-01-01-T" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    a = random.randint(1_000, 8_999) * 1000
    b = random.randint(1_000, 8_999) * 1000
    m = random.randint(1_000, 8_999)
    h = uuid.uuid4().hex[:8].upper()
    doc_a, doc_b, doc_x = "FTA" + h, "FTB" + h, "FTX" + h
    nguon_vnd = "R | 123456789_VPB VND_KQ31" + h
    nguon_usd = "R | 987654321_OCBC USD_KQ31" + h
    i_a = _tien(conn, run, nguon_vnd, 1, f"{a + 1_000_000}.00", "VND", doc_a)
    i_b = _tien(conn, run, nguon_vnd, 2, f"{b}.00", "VND", doc_b)
    i_x = _tien(conn, run, nguon_usd, 3, f"{m}.00", "USD", doc_x)
    la, lb, lx = ("PA" + h[:6] + "-1", "PB" + h[:6] + "-1", "PX" + h[:6] + "-1")
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3, la.split("-")[0], la, D(f"{a}.00"), "VND", "Approve",
               canon_ref(doc_a), "HD-K31", "C-K31", ref_tho=doc_a),
        DongPM(4, lb.split("-")[0], lb, D(f"{b}.00"), "VND", "Approve",
               canon_ref(doc_b), "HD-K31", "C-K31", ref_tho=doc_b),
        DongPM(5, lx.split("-")[0], lx, D(f"{m}.00"), "HKD", "Approve",
               canon_ref(doc_x), "HD-K31", "C-K31", ref_tho=doc_x),
    ])
    gt.ghep_lenh(conn, mot_lan_nap(run), i_b, [lb], actor=ACTOR,
                 reason="KQ-031 bai nghiem thu - kho TEST")
    return {"run": run, "a": a, "m": m, "la": la, "lb": lb, "lx": lx,
            "i_a": i_a, "i_b": i_b, "i_x": i_x}


def _goi_ok(may, duong: str) -> dict:  # noqa: F811
    ok, r = _goi(may, V + duong)
    assert ok == 200, (duong, r)
    return r


def _dong(may, duong: str, ma: str) -> dict:  # noqa: F811
    """**Hàng** lệnh `ma` *(nguyên văn cửa trả — `F01L` đọc hàng, `F01G` đọc
    `hàng.the`)* trong cửa danh sách, lật trang ≤ 20. ⛔ Thấy ⇒ ĐỎ `Đ3`."""
    con_tro = None
    for _ in range(20):
        r = _goi_ok(may, duong + ("&cursor=" + con_tro if con_tro else ""))
        for x in r["data"].get("rows") or []:
            t = x.get("the") or {}
            if t.get("ma_lenh") == ma or x.get("pm_line_id") == ma:
                return x
        con_tro = (r.get("meta") or {}).get("next_cursor") or r["data"].get("next_cursor")
        if not con_tro:
            break
    raise AssertionError(f"⛔ không đo được: cửa {duong} ⛔ trả lệnh {ma}")


def _the(may, duong: str, ma: str) -> dict:  # noqa: F811
    """Thẻ `the` của hàng — khuôn `F01G` đọc."""
    t = _dong(may, duong, ma).get("the")
    assert t, f"⛔ không đo được: hàng {ma} ở {duong} ⛔ có `the`"
    return t


def _than_uv(may, ma: str) -> dict:  # noqa: F811
    """Thân `data` **nguyên văn** của cửa ứng viên."""
    return _goi_ok(may, f"/queue/lenh/{ma}/itl-candidates?limit=50")["data"]


def _ung_vien(may, ma: str) -> list[dict]:  # noqa: F811
    return _than_uv(may, ma)["ung_vien"]


#: Khoá màn khối "đang gán" đọc từ `g` *(`ve_dang_gan` + `ve_o_gd`)* — gom từ
#: **mã nguồn**. Khoá có điều kiện theo `BA-07 §4h ⓵` *(`loi_nguon` — CHỈ khi
#: `nguon` null)* ⛔ đòi; `khoa_to` tách riêng ở bài `F-3`.
CO_DIEU_KIEN = {"loi_nguon"}


def _khoa_khoi_dang_gan() -> set[str]:
    nguon = open(TEP_F01G, encoding="utf-8").read()
    k = khoa_man_doc(_than_ham(nguon, "ve_dang_gan"), "g") \
        | khoa_man_doc(_than_ham(nguon, "ve_o_gd"), "g")
    assert len(k) >= 8, f"⛔ không đo được: chỉ gom {sorted(k)}"
    return k


# ═══ ⓐ CANH — khối "đang gán" đọc đúng khuôn `gd` cửa thật (trừ `khoa_to`) ═══
def test_khoi_DANG_GAN_doc_khoa_gd_CUA_THAT_tru_khoa_to(ca, may):  # noqa: F811
    """⭐ Xanh hôm nay. Mọi khoá `ve_dang_gan`/`ve_o_gd` đọc từ `g` *(trừ
    `khoa_to` — `F-3`, và khoá có điều kiện)* có trong `the.gd` của **cả hai**
    cửa danh sách. ⛔ Chiều ĐỎ: màn đọc một khoá `gd` ⛔ có *(vd. `g.tien`)*."""
    doc = _khoa_khoi_dang_gan() - {"khoa_to"} - CO_DIEU_KIEN
    for duong, ma in (("/queue/lenh-cho?limit=500&ro=may&tu_chung=0", ca["la"]),
                      ("/queue/lenh-da-gan?limit=500", ca["lb"])):
        gd = _the(may, duong, ma).get("gd")
        assert gd, f"⛔ không đo được: {duong} trả thẻ {ma} ⛔ có `gd`"
        assert not (doc - set(gd)), (duong, sorted(doc - set(gd)), sorted(gd))


# ═══ ⓑ F-3 — `gd` ⛔ mang `khoa_to` mà màn đọc ═══════════════════════════════
# ⭐ KQ-036 (02/10): gỡ dấu xfail(strict) — `WO-032` vá F-3; trên `a718142` bài ĐỎ đúng lý do, trên `932d8a4` xanh.
def test_F3_gd_hai_cua_danh_sach_MANG_khoa_to_ma_khoi_dang_gan_doc(ca, may):  # noqa: F811
    assert "khoa_to" in _khoa_khoi_dang_gan(), "màn ⛔ còn đọc khoa_to — bài lỗi thời"
    for duong, ma in (("/queue/lenh-cho?limit=500&ro=may&tu_chung=0", ca["la"]),
                      ("/queue/lenh-da-gan?limit=500", ca["lb"])):
        gd = _the(may, duong, ma)["gd"]
        assert "khoa_to" in gd, (duong, sorted(gd))


# ═══ ⓒ F-2 — bậc `ma` lệch tiền mà `lech = null` ═══════════════════════════
# ⭐ KQ-036 (02/10): gỡ dấu xfail(strict) — `WO-032` vá F-2; trên `a718142` bài ĐỎ đúng lý do, trên `932d8a4` xanh.
def test_F2_ung_vien_bac_MA_tien_LECH_thi_lech_KHONG_null(ca, may):  # noqa: F811
    uv = {u["itl_id"]: u for u in _ung_vien(may, ca["la"])}
    assert ca["i_a"] in uv, f"⛔ không đo được: cửa ⛔ trả dòng tiền {ca['i_a']}"
    u = uv[ca["i_a"]]
    assert u["bac"] == "ma", u
    assert u["lech"] is not None, u
    assert abs(D(str(u["lech"]))) == D("1000000"), u


# ═══ ⓓ F-1 — hộp Tìm tiền: khác tiền tệ cùng số ⇒ ⛔ được nói "trong dung sai" ═
def test_F1_CANH_cua_ghi_TU_CHOI_cap_khac_tien_te(ca, conn):  # noqa: F811
    """⭐ Xanh — **mỏ neo sự thật** của bài dưới: cửa ghi thật từ chối cặp
    `X` *(HKD)* ↔ dòng tiền USD cùng số *(cổng ⓔ)*. ⛔ Ghi gì: nó ném trước."""
    with pytest.raises(gt.KhacTienTe):
        gt.ghep_lenh(conn, mot_lan_nap(ca["run"]), ca["i_x"], [ca["lx"]],
                     actor=ACTOR, reason="KQ-031 thu cua ghi - kho TEST")
    n = conn.execute("SELECT count(*) FROM fls_moi_noi WHERE itl_id = %s",
                     (ca["i_x"],)).fetchone()[0]
    assert n == 0, n


@can_node
# ⭐ KQ-036 (02/10): gỡ dấu xfail(strict) — `WO-032` vá F-1; trên `a718142` bài ĐỎ đúng lý do, trên `932d8a4` xanh.
def test_F1_tim_tien_KHAC_TIEN_TE_cung_so_KHONG_noi_trong_dung_sai(ca, may):  # noqa: F811
    """Thân **cửa thật** *(ứng viên + dòng danh sách lệnh)* đưa nguyên vào
    `F01L._drawer_tim_tien`, chọn ứng viên bậc `ma` USD ⇒ câu `#sig-l` ⛔ được
    là *"trong dung sai"* *(lớp `ok`)*. ⛔ Chiều ĐỎ: hôm nay."""
    than = _than_uv(may, ca["lx"])
    uv = than["ung_vien"]
    ids = [u["itl_id"] for u in uv]
    assert ca["i_x"] in ids, f"⛔ không đo được: cửa ⛔ trả {ca['i_x']} trong {ids}"
    assert uv[ids.index(ca["i_x"])]["curr"] == "USD"
    dong = _dong(may, "/queue/lenh-cho?limit=50&curr=HKD", ca["lx"])
    r = _chay("""
      const MA = %s;
      _TRA['/queue/lenh/' + MA + '/itl-candidates'] = {data: %s};
      _TRA['/queue/lenh/' + MA] = {no: {cau: 'x'}};
      const s = document.createElement('div'); s.id = 'sig-l';
      document.body.appendChild(s);
      await F01L._drawer_tim_tien(%s);
      const b = document.getElementById('dlg-b');
      const c = document.createElement('input');
      c.type = 'radio'; c.name = 'uv'; c.checked = true; c.dataset.i = '%d';
      b.appendChild(c);
      (b._nghe.change || []).forEach(f => f({target: b}));
      return {sig: s.innerHTML, lop: s.className};
    """ % (json.dumps(ca["lx"]),
           json.dumps(than, ensure_ascii=False, default=str),
           json.dumps(dong, ensure_ascii=False, default=str), ids.index(ca["i_x"])),
        tep=TEP_F01, vo=VO_F01)
    assert "trong dung sai" not in r["sig"], r
    assert "ok" not in r["lop"].split(), r
