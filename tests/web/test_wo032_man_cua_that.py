# -*- coding: utf-8 -*-
"""`WO-032` — hai màn ghép `F01L` / `F01G` *(và `F01`, `F04`)* vẽ từ thân
**CỬA THẬT** trên **kho TEST**: khác tiền tệ · lệch mọi bậc · `khoa_to` · bậc
toàn sổ · trạng thái rỗng · `title` ô tiền · ô lý do tuỳ ý.

⛔⛔ **Luật của tệp** *(`BA-07` v3.7 §4h ⓵ — luật bài thử)*: thân dùng để vẽ màn
lấy từ **cửa HTTP thật** *(ca `tests/web/ca_wo032.py`, `assert current_database()
= 'fls_test'`)*, đưa **nguyên văn** vào `_TRA` của khung node. ⛔ Một khoá do
bài đặt — trừ thao tác DOM của **khung hộp** *(`#sig-l`, ô chọn, ô lý do: DOM
giả ⛔ phân tích `innerHTML` — đầu `dom_gia.js`)*, như `KQ-029`/`KQ-031` đã chấp.
Lớp lỗi *"khuôn thử tự nhét"* đã sống sót **ba lần** *(`KQ-019` · `KQ-029 F-1`
· `KQ-031 F-3`)* đúng vì bài đặt **cả** câu hỏi **lẫn** câu trả lời.

⭐ Mỗi bài ghi **chiều ĐỎ** đã chạy *(JS/mã `HEAD` khi nhận phiếu, `a718142`)*.
"""
from __future__ import annotations

import json
import math
import os
import re
import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.web import phuc_vu as pv
from tests.web.ca_wo032 import dung_ca, goi_ok, hang
from tests.web.khung_node import TEP_F04, VO_F04, _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg

D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"
D_DA_GAN = "/queue/lenh-da-gan?limit=500"
D_LUOI = "/queue/lenh-cho?limit=50&curr=VND"


def _so_vn(n: int) -> str:
    return f"{n:,}".replace(",", ".")


@pytest.fixture(scope="module")
def ca_tra():
    """`(ca, {đường MÀN gọi: thân 'data' cửa thật})` — ⭐ đúng chuỗi màn gọi
    *(⛔ thêm `limit`: `F01L`/`F01G` gọi `itl-candidates` trần)*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca(c)
    L = ca["lenh"]
    duong = [D_NGUOI, D_MAY, D_DA_GAN, D_LUOI]
    for k in "ABXY":
        duong += [f"/queue/lenh/{L[k]}/itl-candidates", f"/queue/lenh/{L[k]}"]
    duong += [f"/queue/lenh/{L['A']}/so?q={ca['h']}"]
    with _may() as m:
        tra = {d: goi_ok(m, d)["data"] for d in duong}
    return ca, tra


def _nap(tra: dict) -> str:
    """Kịch bản: đưa NGUYÊN thân cửa thật vào `_TRA`."""
    return ("const TRA = %s;\n"
            "for (const k of Object.keys(TRA)) _TRA[k] = {data: TRA[k]};\n"
            % json.dumps(tra, ensure_ascii=False, default=str))


# ══ F01L — hộp Tìm tiền ════════════════════════════════════════════════════
_HOP_F01L = """
  const s = document.createElement('div'); s.id = 'sig-l';
  document.body.appendChild(s);
  await F01L._drawer_tim_tien(%(dong)s);
  const b = document.getElementById('dlg-b');
  const c = document.createElement('input');
  c.type = 'radio'; c.name = 'uv'; c.checked = true; c.dataset.i = '%(i)d';
  b.appendChild(c);
  (b._nghe.change || []).forEach(f => f({target: b}));
  return {hop: b.innerHTML, sig: s.innerHTML, lop: s.className};
"""


def _hop_f01l(ca, tra, ma: str, itl_id: int) -> dict:
    """Mở hộp *Tìm tiền* THẬT bằng **chính hàng** cửa danh sách lệnh trả, chọn
    dòng tiền `itl_id`."""
    uv = tra[f"/queue/lenh/{ma}/itl-candidates"]["ung_vien"]
    ids = [u["itl_id"] for u in uv]
    assert itl_id in ids, f"⛔ không đo được: cửa ⛔ trả {itl_id} trong {ids}"
    dong = hang(tra[D_LUOI], ma)
    return _chay(_nap(tra) + _HOP_F01L % {
        "dong": json.dumps(dong, ensure_ascii=False, default=str),
        "i": ids.index(itl_id)}, tep=TEP_F01, vo=VO_F01)


def _o_hang(hop: str, i: int) -> list[str]:
    """Các ô `<td class="r num">` *(Tiền, Lệch)* của hàng ứng viên `i`."""
    m = re.search(r'data-i="%d">.*?</tr>' % i, hop, flags=re.S)
    assert m, f"⛔ không đo được: hàng {i} ⛔ có trong hộp"
    return re.findall(r'<td class="r num">(.*?)</td>', m.group(0))


@can_node
def test_AC1_tim_tien_VND_USD_cung_so_noi_KHAC_TIEN_TE_crit(ca_tra):
    """Lệnh `X` VND `<n>` ↔ dòng tiền **USD** `<n>.00` cùng số CT *(bậc `ma` —
    hình `PM00329-1` sổ thật)* ⇒ `#sig-l` `crit`, *"khác tiền tệ … TỪ CHỐI"*;
    ô `Lệch` = `khác tiền tệ`; ô `Tiền` = `<n>,00 USD`.

    ⛔ Chiều ĐỎ *(JS `a718142`)*: `_tinh` ⛔ so mã ⇒ `lệch 0,00 ⇒ trong dung
    sai`, lớp `ok` ⇒ ĐỎ; ô `Lệch` `—` ⇒ ĐỎ; ô `Tiền` `<n>,00` ⛔ mã ⇒ ĐỎ."""
    ca, tra = ca_tra
    L, n = ca["lenh"], ca["tien"]["X"]
    r = _hop_f01l(ca, tra, L["X"], ca["i_x"])
    assert "crit" in r["lop"].split(), r
    assert "khác tiền tệ" in r["sig"] and "TỪ CHỐI" in r["sig"], r["sig"]
    assert "trong dung sai" not in r["sig"] and "lệch 0" not in r["sig"], r["sig"]
    assert (_so_vn(n) + " VND") in r["sig"] and (_so_vn(n) + ",00 USD") in r["sig"]
    i = [u["itl_id"] for u in
         tra[f"/queue/lenh/{L['X']}/itl-candidates"]["ung_vien"]].index(ca["i_x"])
    tien, lech = _o_hang(r["hop"], i)
    assert tien == _so_vn(n) + ",00 USD", tien
    assert lech == "khác tiền tệ", lech


@can_node
def test_AC3_tim_tien_bac_MA_lech_1_trieu_o_Lech_CO_SO(ca_tra):
    """Lệnh `A` ↔ dòng tiền bậc `ma` lệch `1.000.000` ⇒ ô `Lệch` `1.000.000`.

    ⛔ Chiều ĐỎ *(mã `a718142`)*: cửa trả `lech = null` ở bậc `ma` ⇒ `—` ⇒ ĐỎ."""
    ca, tra = ca_tra
    L = ca["lenh"]
    r = _hop_f01l(ca, tra, L["A"], ca["i_a"])
    i = [u["itl_id"] for u in
         tra[f"/queue/lenh/{L['A']}/itl-candidates"]["ung_vien"]].index(ca["i_a"])
    tien, lech = _o_hang(r["hop"], i)
    assert lech == "1.000.000", lech
    assert tien == _so_vn(ca["tien"]["A"] + 1_000_000) + " VND", tien
    # ⭐ cùng tiền tệ ⇒ câu so `WO-022` ⛔ đổi *(VƯỢT dung sai)*
    assert "lệch <b>1.000.000</b>" in r["sig"] and "VƯỢT" in r["sig"], r["sig"]


# ══ F01G — màn ghép ═══════════════════════════════════════════════════════
def _f01g(tra: dict, than: str) -> str:
    return _nap(tra) + " await F01G.mo_man();\n" + than


def _chon_va_bam_gan(ma: str, itl_id: int) -> str:
    """Mở lệnh, **bấm** dòng ứng viên `itl_id` *(người nghe `click` thật)*, bấm
    `Gán` lần một *(ca lệch ⇒ ⛔ ghi, chờ xác nhận)*, trả chữ thanh hành động."""
    return """
      await F01G.mo_lenh(%(ma)s);
      const i = F01G.ST.ung_vien.findIndex(u => u.itl_id === %(id)d);
      if (i < 0) return {loi: 'không có ứng viên'};
      const c = document.querySelectorAll('.cand')[i];
      c._nghe.click[0]({target: c});
      const lenh = F01G.ST.dong.find(d => d.ma_lenh === %(ma)s);
      await F01G.gan(lenh);
      return {act: document.querySelector('.act').textContent,
              ghi: _GOI.filter(g => g[0] === 'ghi').length};
    """ % {"ma": json.dumps(ma), "id": itl_id}


@can_node
def test_AC3_F01G_nhan_xac_nhan_bac_MA_co_LECH_va_khac_tien_te_KHONG_lech(ca_tra):
    """`ve_thanh` sau cú bấm thứ nhất: ứng viên bậc `ma` lệch `1.000.000` ⇒
    *"(lệch 1.000.000 VND)"*; ứng viên USD cạnh lệnh VND ⇒ *"khác tiền tệ"*,
    ⛔ *"(lệch"*. ⛔ Ghi gì ở cú thứ nhất.

    ⛔ Chiều ĐỎ *(`a718142`)*: bậc `ma` `lech = null` ⇒ nhãn ⛔ có *"(lệch"* ⇒
    ĐỎ; khác tiền tệ ⇒ nhãn ⛔ nói *"khác tiền tệ"* ⇒ ĐỎ."""
    ca, tra = ca_tra
    L = ca["lenh"]
    a = _chay(_f01g(tra, _chon_va_bam_gan(L["A"], ca["i_a"])),
              tep=TEP_F01, vo=VO_F01)
    assert "(lệch 1.000.000 VND)" in a["act"], a
    assert a["ghi"] == 0, a
    x = _chay(_f01g(tra, _chon_va_bam_gan(L["X"], ca["i_x"])),
              tep=TEP_F01, vo=VO_F01)
    assert "khác tiền tệ" in x["act"] and "(lệch" not in x["act"], x
    assert x["ghi"] == 0, x


_DANG_GAN = """
  await F01G.doi_chip('da_gan');
  await F01G.mo_lenh(%s);
  const m = document.querySelector('.mblock');
  const dg = document.querySelector('.mblock .mdg');
  const l = document.querySelector('.mblock .lech');
  return {co: !!m, dg: dg ? dg.innerHTML : null, lech: l ? l.textContent : null};
"""


@can_node
def test_AC3_AC4_khoi_DANG_GAN_than_cua_that_co_chip_LECH_va_MARK_so_CT(ca_tra):
    """Lệnh `B` *(đã gán, lệch `500`, diễn giải chứa số CT)*: khối *"Đang gán"*
    có chip `.lech` *"lệch 500 VND"* và `<mark>` quanh số CT — **thân cửa thật**.

    ⛔ Chiều ĐỎ *(`a718142`)*: `gd.lech = null` ⇒ ⛔ chip; `gd` ⛔ `khoa_to` ⇒
    ⛔ `<mark>` ⇒ ĐỎ cả hai."""
    ca, tra = ca_tra
    r = _chay(_f01g(tra, _DANG_GAN % json.dumps(ca["lenh"]["B"])),
              tep=TEP_F01, vo=VO_F01)
    assert r["co"], r
    assert r["lech"] == "lệch 500 VND", r
    assert ("<mark>" + ca["doc"]["B"] + "</mark>") in (r["dg"] or ""), r


_TOAN_SO = """
  await F01G.mo_lenh(%(ma)s);
  F01G.ST.tim = %(q)s;
  await F01G.tai_toan_so(%(ma)s);
  F01G.ST.toan_so = true;
  F01G.ve();
  const ra = [];
  document.querySelectorAll('.cand').forEach((c, i) => {
    const t = c.querySelector('.tg');
    ra.push({id: F01G.ST.ung_vien[i].itl_id, k: t.textContent,
             title: t.getAttribute('title')});
  });
  return ra;
"""


@can_node
def test_AC5_toan_so_dong_USD_canh_lenh_VND_chip_KHAC_TIEN_TE_va_bac_la_in_nguyen_ten(
        ca_tra):
    """Toàn sổ của lệnh `A` *(VND)*: dòng USD `X` ⇒ ký hiệu `≠`, `title`
    *"khác tiền tệ"*. Cùng thân, đổi **giá trị** `bac` thành `'xyz'` *(⛔ thêm
    khoá)* ⇒ ô in `xyz`, ⛔ *"cùng đơn vị tiền"*.

    ⛔ Chiều ĐỎ *(`a718142`)*: cửa dán `cung_tien_te` ⇒ `④`/*"cùng đơn vị
    tiền"* ⇒ ĐỎ; `|| BAC.cung_tien_te` ⇒ `xyz` in `④` ⇒ ĐỎ."""
    ca, tra = ca_tra
    ma, q = ca["lenh"]["A"], ca["h"]
    k = f"/queue/lenh/{ma}/so?q={q}"
    r = _chay(_f01g(tra, _TOAN_SO % {"ma": json.dumps(ma), "q": json.dumps(q)}),
              tep=TEP_F01, vo=VO_F01)
    x = {d["id"]: d for d in r}
    assert ca["i_x"] in x, f"⛔ không đo được: toàn sổ ⛔ vẽ {ca['i_x']}: {r}"
    assert x[ca["i_x"]]["title"] == "khác tiền tệ", x[ca["i_x"]]
    assert x[ca["i_x"]]["k"] == "≠", x[ca["i_x"]]
    la = json.loads(json.dumps(tra, default=str))
    for u in la[k]["ung_vien"]:
        if u["itl_id"] == ca["i_x"]:
            u["bac"] = "xyz"
    r2 = _chay(_f01g(la, _TOAN_SO % {"ma": json.dumps(ma), "q": json.dumps(q)}),
               tep=TEP_F01, vo=VO_F01)
    y = {d["id"]: d for d in r2}[ca["i_x"]]
    assert y["k"] == "xyz" and y["title"] == "xyz", y
    assert "cùng đơn vị tiền" not in json.dumps(y, ensure_ascii=False), y


# ══ AC-6 · trạng thái RỖNG của màn vẽ được ════════════════════════════════
#: ⭐ Đúng hàm `GIA_LAP.rong.lam` của `ung_dung.js` — bài dưới đọc nguồn để
#: hai chỗ ⛔ trôi khỏi nhau.
_RONG = "FLS.doc = () => Promise.resolve({ data: null, meta: {} });\n"


def test_AC6_che_do_gia_lap_RONG_cua_vo_tra_data_null():
    src = open(os.path.join(pv.THU_MUC, "ung_dung.js"), encoding="utf-8").read()
    m = re.search(r"rong:\s*\{.*?lam:\s*\(\)\s*=>\s*(Promise\.resolve\(\{[^)]*\}\))",
                  src, flags=re.S)
    assert m, "⛔ không đo được: `GIA_LAP.rong.lam` ⛔ tìm thấy"
    assert re.sub(r"\s", "", m.group(1)) == "Promise.resolve({data:null,meta:{}})", m


@can_node
def test_AC6_tim_tien_RONG_mo_hop_voi_cau_rong_KHONG_TypeError(ca_tra):
    """⛔ Chiều ĐỎ *(`a718142`)*: `d.ung_vien` khi `d = null` ⇒ `TypeError` ⇒
    node nổ ⇒ ĐỎ."""
    ca, tra = ca_tra
    dong = hang(tra[D_LUOI], ca["lenh"]["A"])
    r = _chay(_RONG + """
      await F01L._drawer_tim_tien(%s);
      return {hop: document.getElementById('dlg-b').innerHTML,
              mo: document.getElementById('scrim').className};
    """ % json.dumps(dong, ensure_ascii=False, default=str),
        tep=TEP_F01, vo=VO_F01)
    assert "Không có dòng tiền nào ứng" in r["hop"], r["hop"][:300]


@can_node
def test_AC6_F04_nap_sao_ke_RONG_cau_rong_KHONG_TypeError():
    """`④ Nạp sao kê` ở `?gia_lap=rong` ⇒ `#nap-chon` câu rỗng; `#nap-doc` câu
    rỗng. ⛔ Chiều ĐỎ *(`a718142`)*: `d.nguon` khi `d = null` ⇒ `TypeError`."""
    r = _chay(_RONG + """
      await F04.ve();
      return {chon: document.getElementById('nap-chon').textContent,
              doc: document.getElementById('nap-doc').textContent};
    """, tep=TEP_F04, vo=VO_F04)
    assert "Kho chưa có nguồn nào" in r["chon"], r
    assert "Chưa có lần đọc nào" in r["doc"], r


# ══ AC-7 · `.cand-cols` + `title` ════════════════════════════════════════
def test_AC7_cot_tien_cand_cols_CA_BA_khai_bao_du_ngan_sach_18_ky_tu():
    """Cột số tiền *(cột cuối)* ở **cả ba** khai báo `.cand-cols` trừ `18px`
    *(ô `Nợ/Có`)* + `5px` *(khe)* ≥ `ceil(18 × 0,6 × fs_than)` — `fs_than`
    **đọc** từ `tokens.css`. ⛔ Chiều ĐỎ: hạ cột về `150px` ⇒ `127 < 135` ⇒ ĐỎ."""
    tok = open(os.path.join(pv.THU_MUC, "tokens.css"), encoding="utf-8").read()
    fs = float(re.search(r"--fs-than:\s*([\d.]+)px", tok).group(1))
    can = math.ceil(18 * 0.6 * fs)
    css = open(os.path.join(pv.THU_MUC, "hinh.css"), encoding="utf-8").read()
    khai = re.findall(r"\.cand-cols\{[^}]*?grid-template-columns:([^;}]+)", css)
    assert len(khai) == 3, f"⛔ không đo được: {len(khai)} khai báo `.cand-cols`"
    for k in khai:
        cuoi = int(re.findall(r"(\d+)px", k)[-1])
        assert cuoi - 18 - 5 >= can, (k.strip(), cuoi, can)


@can_node
def test_AC7_o_tien_ung_vien_co_TITLE_dung_chuoi_in_than_cua_that(ca_tra):
    """`.cand .amt>span[title]` = đúng chuỗi in *(`TP.tien(v, c) + ' ' + c`)*.
    ⛔ Chiều ĐỎ *(`a718142`)*: ⛔ `title` ⇒ ĐỎ."""
    ca, tra = ca_tra
    ma = ca["lenh"]["A"]
    r = _chay(_f01g(tra, """
      await F01G.mo_lenh(%s);
      return [...document.querySelectorAll('.cand')].map((c, i) => {
        const s = c.querySelector('.amt').children[0];
        return {id: F01G.ST.ung_vien[i].itl_id, chu: s.textContent,
                title: s.getAttribute('title')};
      });
    """ % json.dumps(ma)), tep=TEP_F01, vo=VO_F01)
    assert r, "⛔ không đo được: 0 ứng viên"
    assert all(x["title"] == x["chu"] for x in r), r
    a = {x["id"]: x for x in r}[ca["i_a"]]
    assert a["title"] == _so_vn(ca["tien"]["A"] + 1_000_000) + " VND", a


# ══ AC-8 · ô lý do ghép TUỲ Ý ═════════════════════════════════════════════
@pytest.fixture()
def ca_ghi():
    """Hai cặp VND khớp đúng *(G cho `F01` Ghép + Bỏ cả chùm, H cho `F01L`
    Ghép)* trên kho TEST, và máy **ghi được** trỏ kho TEST."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        db = c.execute("SELECT current_database()").fetchone()[0]
        assert db == "fls_test", db
        from tests.web.ca_wo032 import _tien
        from fls.adapters.pm_join import DongPM, canon_ref
        from fls.ledger.build import NgucCanh
        from fls.repo.chay_nap import chen_dong_pm
        h = uuid.uuid4().hex[:8].upper()
        run = "NAP-2000-01-01-T8" + h[:6]
        c.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                  " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        import random
        z, w = (random.randint(1_000, 8_999) * 1000 for _ in range(2))
        nguon = "R | 123456789_VPB VND_K8" + h
        i_g = _tien(c, run, nguon, 1, f"{z}.00", "VND", "FTG" + h)
        i_h = _tien(c, run, nguon, 2, f"{w}.00", "VND", "FTH" + h)
        lg, lh = "PG" + h[:6] + "-1", "PH" + h[:6] + "-1"
        chen_dong_pm(c, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
            DongPM(3, lg[:-2], lg, D(f"{z}.00"), "VND", "Approve",
                   canon_ref("FTG" + h), "HD-K8", "C-K8", ref_tho="FTG" + h),
            DongPM(4, lh[:-2], lh, D(f"{w}.00"), "VND", "Approve",
                   canon_ref("FTH" + h), "HD-K8", "C-K8", ref_tho="FTH" + h)])
        with _may() as m:
            yield {"c": c, "m": m, "i_g": i_g, "i_h": i_h, "lg": lg, "lh": lh}


def _ghi_cua_that(ca: dict, ghi: list) -> str:
    """Gửi **đúng** `(đường, thân)` màn vừa gửi lên cửa THẬT kho TEST; trả
    `reason` sự kiện mới nhất của dòng tiền ấy."""
    assert len(ghi) == 1, f"⛔ mong MỘT POST, gặp {len(ghi)}: {ghi}"
    _, duong, than = ghi[0]
    ok, r = _goi(ca["m"], V + duong, pt="POST", than=than)
    assert ok == 200, (duong, than, r)
    itl = int(duong.split("/")[2])
    return ca["c"].execute(
        "SELECT reason FROM fls_queue_event WHERE itl_id=%s"
        " ORDER BY evt_id DESC LIMIT 1", (itl,)).fetchone()[0]


_BAM_NUT_CUOI = """
  const nut = document.getElementById('dlg-f').children
    .filter(x => x.tagName === 'BUTTON');
  let loi = null;
  try { await nut[nut.length - 1].onclick(); } catch (e) { loi = String(e); }
  return {ghi: _GOI.filter(g => g[0] === 'ghi'), loi: loi,
          ph: (document.getElementById('dlg-b').innerHTML.match(
                 /placeholder="([^"]*)"/g) || [])};
"""

_O = """
  const o = document.createElement('input'); o.id = %s; o.value = '';
  document.getElementById('dlg-b').appendChild(o);
"""


@can_node
def test_AC8_BA_hop_ghep_O_LY_DO_TRONG_van_GUI_va_cua_ghi_may_dien(ca_ghi):
    """F01 *Ghép* · F01 *Bỏ cả chùm* · F01L *Ghép* — ô lý do trống ⇒ **một**
    `POST`, thân ⛔ mang `reason`; gửi đúng thân ấy lên cửa thật kho TEST ⇒
    `fls_queue_event.reason` bắt đầu `"(may dien) "`; placeholder ⛔
    `BẮT BUỘC`.

    ⛔ Chiều ĐỎ *(`a718142`)*: `if (!v) … return false` ở cả ba ⇒ **0** POST ⇒
    ĐỎ."""
    ca = ca_ghi
    m = ca["m"]
    ok, pmc = _goi(m, V + f"/queue/{ca['i_g']}/pm-candidates")
    assert ok == 200, pmc
    uv = pmc["data"]["ung_vien"]
    i = [u["pm_line_id"] for u in uv].index(ca["lg"])
    # ① F01 Ghép
    r = _chay(_nap({f"/queue/{ca['i_g']}/pm-candidates": pmc["data"]}) + """
      const sig = document.createElement('div'); sig.id = 'sig';
      document.body.appendChild(sig);
      await F01._drawer_ghep({itl_id: %d});
      const b = document.getElementById('dlg-b');
      const c = document.createElement('input');
      c.type = 'checkbox'; c.checked = true; c.dataset.i = '%d';
      c.dataset.a = %s; b.appendChild(c);
    """ % (ca["i_g"], i, json.dumps(str(uv[i]["amount"])))
        + _O % json.dumps("o-vi-sao")
        + " if (typeof b.onchange === 'function') b.onchange({target: b});"
        + _BAM_NUT_CUOI, tep=TEP_F01, vo=VO_F01)
    assert r["loi"] is None, r
    assert not any("BẮT BUỘC" in p for p in r["ph"]), r["ph"]
    assert "reason" not in r["ghi"][0][2], r["ghi"]
    assert _ghi_cua_that(ca, r["ghi"]).startswith("(may dien) "), r
    # ② F01 Bỏ cả chùm *(dòng `G` vừa ghép thật ở ①)*
    r = _chay("await (async () => { F01._bo_ghep({itl_id: %d}); })();"
              % ca["i_g"] + _O % json.dumps("o-vi-sao") + _BAM_NUT_CUOI,
              tep=TEP_F01, vo=VO_F01)
    assert r["loi"] is None, r
    assert not any("BẮT BUỘC" in p for p in r["ph"]), r["ph"]
    assert r["ghi"][0][1] == f"/queue/{ca['i_g']}/unmatch", r
    assert "reason" not in r["ghi"][0][2], r["ghi"]
    assert _ghi_cua_that(ca, r["ghi"]).startswith("(may dien) "), r
    # ③ F01L Ghép ở hộp Tìm tiền
    ok, uvh = _goi(m, V + f"/queue/lenh/{ca['lh']}/itl-candidates")
    assert ok == 200, uvh
    ok, ds = _goi(m, V + "/queue/lenh-cho?limit=50&curr=VND")
    dong = hang(ds["data"], ca["lh"])
    j = [u["itl_id"] for u in uvh["data"]["ung_vien"]].index(ca["i_h"])
    r = _chay(_nap({f"/queue/lenh/{ca['lh']}/itl-candidates": uvh["data"]})
              + _HOP_F01L.split("return")[0] % {
                  "dong": json.dumps(dong, ensure_ascii=False, default=str),
                  "i": j}
              + _O % json.dumps("o-vi-sao-l") + _BAM_NUT_CUOI,
              tep=TEP_F01, vo=VO_F01)
    assert r["loi"] is None, r
    assert not any("BẮT BUỘC" in p for p in r["ph"]), r["ph"]
    assert r["ghi"][0][1] == f"/queue/{ca['i_h']}/match", r
    assert "reason" not in r["ghi"][0][2], r["ghi"]
    assert _ghi_cua_that(ca, r["ghi"]).startswith("(may dien) "), r


@can_node
def test_AC8_HOAN_va_MO_LAI_o_trong_GIU_bat_buoc_0_POST():
    """Hai hộp ⛔ thuộc lời owner `QĐ-ITL-149 ⓑ` ⇒ ô trống ⇒ **0** `POST`.
    ⛔ Chiều ĐỎ: bỏ chặn ở `Hoãn` ⇒ một `POST` ⇒ ĐỎ."""
    hoan = _chay("""
      F01._hoan({itl_id: 9});
      const d = document.createElement('input'); d.id = 'o-den';
      d.value = '2026-12-01'; document.getElementById('dlg-b').appendChild(d);
    """ + _O % json.dumps("o-vi-sao") + _BAM_NUT_CUOI, tep=TEP_F01, vo=VO_F01)
    assert hoan["loi"] is None and hoan["ghi"] == [], hoan
    mo = _chay("F01._mo_lai({itl_id: 9});" + _O % json.dumps("o-vi-sao")
               + _BAM_NUT_CUOI, tep=TEP_F01, vo=VO_F01)
    assert mo["loi"] is None and mo["ghi"] == [], mo
