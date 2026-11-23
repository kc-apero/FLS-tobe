# -*- coding: utf-8 -*-
"""`WO-037` — màn `F01G` vẽ từ thân **CỬA THẬT** trên **kho TEST**: ô `Giao dịch
đã gán` câu thứ sáu *(`g`)* · khối *"Đang gán"* bậc `khac_tien_te` *(`c`)* + bậc
lạ in nguyên tên *(`e`)* · màu chú giải + ô `.tg` *(`f`)*.

⛔⛔ **Luật của tệp** *(`BA-07` v3.9 §4h ⓵ — luật bài thử)*: thân dùng để vẽ màn
lấy từ **cửa HTTP thật** *(ca `tests/web/ca_wo037.py`, `assert current_database()
= 'fls_test'`)*, đưa **nguyên văn** vào `_TRA` của khung node. ⛔ Một khoá do bài
đặt — ca bậc lạ `AC-6` đổi **giá trị** `bac` *(⛔ thêm khoá)*, như `KQ-036 F-3`.
Lớp lỗi *"khuôn thử tự nhét"* đã sống sót **ba lần** *(`KQ-019` · `KQ-029 F-1` ·
`KQ-031 F-3`)*.

⭐ Mỗi bài ghi **chiều ĐỎ** đã chạy trên mã `HEAD` khi nhận phiếu *(`8d7bea2`)*.
"""
from __future__ import annotations

import json
import os
import re

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.web import phuc_vu as pv
from tests.web.ca_wo032 import goi_ok, hang
from tests.web.ca_wo037 import dung_ca_wo037
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg

D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"
D_DA_GAN = "/queue/lenh-da-gan?limit=500"


@pytest.fixture(scope="module")
def ca_tra():
    """`(ca, {đường MÀN gọi: thân 'data' cửa thật})` — đúng chuỗi `F01G` gọi
    *(chip `Chưa gán` = `ro=nguoi` ＋ `ro=may&tu_chung=0`; chip `Đã gán`)*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo037(c)
    L = ca["lenh"]
    duong = [D_NGUOI, D_MAY, D_DA_GAN]
    for k in "KYG":
        duong += [f"/queue/lenh/{L[k]}/itl-candidates"]
    with _may() as m:
        tra = {d: goi_ok(m, d)["data"] for d in duong}
    return ca, tra


def _nap(tra: dict) -> str:
    return ("const TRA = %s;\n"
            "for (const k of Object.keys(TRA)) _TRA[k] = {data: TRA[k]};\n"
            % json.dumps(tra, ensure_ascii=False, default=str))


def _f01g(tra: dict, than: str) -> str:
    return _nap(tra) + " await F01G.mo_man();\n" + than


# ═══ AC-8 *(g)* — ô `Giao dịch đã gán` in câu `vi_sao` của CỬA ════════════════
_O_GD = """
  const b = F01G.ve_bang();
  const i = F01G.COT_BANG.findIndex(c => c[0] === 'gd');
  const h = b.querySelectorAll('.mrow').find(r => r.textContent.includes(%(ma)s));
  if (!h) return {loi: 'không có hàng'};
  const o = h.children[i];
  return {chu: o.textContent,
          lop: o.children.map(c => c.className || ''),
          title: o.children.map(c => c.getAttribute('title') || null)};
"""


@can_node
def test_AC8_o_GIAO_DICH_lenh_khop_ma_khac_tien_te_in_DUNG_cau_vi_sao_cua_cua(ca_tra):
    """Lệnh `K` *(VND, khớp mã chỉ dòng USD — hình `PM00329-1`)*: ô in **đúng**
    câu `vi_sao` cửa trả *(so chuỗi)*, ⛔ `đề xuất:`, ⛔ `— chưa chọn`; chữ ⛔ lớp
    `none` *(`--faint` **2,17 : 1** — `NFR-I29`)*.

    ⛔ Chiều ĐỎ: ⓐ mã cửa `8d7bea2` ⇒ `K` ở rổ `may`, ô *"đề xuất: …"* USD ⇒ ĐỎ;
    ⓑ JS `8d7bea2` trên cửa mới ⇒ `— chưa chọn` ⇒ ĐỎ."""
    ca, tra = ca_tra
    x = hang(tra[D_NGUOI], ca["lenh"]["K"])
    vs = x["vi_sao"]
    assert vs and "USD" in vs, f"⛔ không đo được: cửa ⛔ trả câu vi_sao: {vs!r}"
    r = _chay(_f01g(tra, _O_GD % {"ma": json.dumps(ca["lenh"]["K"])}),
              tep=TEP_F01, vo=VO_F01)
    assert r.get("chu") == vs, r
    assert "đề xuất:" not in r["chu"] and "chưa chọn" not in r["chu"], r
    assert not any("none" in l.split() for l in r["lop"]), r
    assert r["title"] == [vs], r


@can_node
def test_AC8_o_GIAO_DICH_nam_cau_cu_KHONG_doi(ca_tra):
    """⛔ hồi quy *(`BA-06` v4.16: ⛔ đổi năm câu kia)*: lệnh `M` rổ `may`
    *(khớp mã VND, lệch ngoài dung sai ⇒ ⛔ `tu_chung` ⇒ chip `Chưa gán`)* ⇒ ô
    `đề xuất: …`, ⛔ câu `vi_sao`."""
    ca, tra = ca_tra
    r = _chay(_f01g(tra, _O_GD % {"ma": json.dumps(ca["lenh"]["M"])}),
              tep=TEP_F01, vo=VO_F01)
    assert r.get("chu", "").startswith("đề xuất: "), r


# ═══ AC-4 *(c)* + AC-6 *(e)* — khối "Đang gán" ════════════════════════════════
_CHIP_DANG_GAN = """
  await F01G.doi_chip('da_gan');
  await F01G.mo_lenh(%s);
  // ⚠ DOM giả chỉ hiểu bộ chọn HAI tầng (`dom_gia.js::khop`)
  const c = document.querySelector('.mh .chip');
  return {co: !!document.querySelector('.mblock'),
          chip: c ? c.textContent : null, title: c ? c.getAttribute('title') : null};
"""


@can_node
def test_AC4_khoi_DANG_GAN_dong_USD_khac_ma_duoi_lenh_VND_chip_KHAC_TIEN_TE(ca_tra):
    """⛔ Chiều ĐỎ *(mã cửa `8d7bea2`)*: `_bac` ⇒ `cung_tien_te` ⇒ chip
    *"④ cùng đơn vị tiền"* cạnh dòng USD ⇒ ĐỎ."""
    ca, tra = ca_tra
    r = _chay(_f01g(tra, _CHIP_DANG_GAN % json.dumps(ca["lenh"]["G"])),
              tep=TEP_F01, vo=VO_F01)
    assert r["co"], r
    assert r["chip"] == "≠ khác tiền tệ" and r["title"] == "khác tiền tệ", r


@can_node
def test_AC6_khoi_DANG_GAN_bac_LA_in_NGUYEN_TEN(ca_tra):
    """Cùng thân cửa thật, đổi **giá trị** `bac` của `G` thành `'xyz'` ⇒ chip
    in `xyz` *(⛔ `null` — `BA-07` §4h ⓵ dòng `bac` v3.9: **mọi** hàm vẽ)*.

    ⛔ Chiều ĐỎ *(JS `8d7bea2`)*: `if (b) {…}` bỏ chip ⇒ `chip null` ⇒ ĐỎ."""
    ca, tra = ca_tra
    la = json.loads(json.dumps(tra, default=str))
    doi = 0
    for x in la[D_DA_GAN]["rows"]:
        if x.get("pm_line_id") == ca["lenh"]["G"]:
            for g in [x["the"]["gd"]] + list(x["the"].get("gd_ds") or []):
                g["bac"] = "xyz"
            doi += 1
    assert doi == 1, f"⛔ không đo được: thân lenh-da-gan ⛔ có {ca['lenh']['G']}"
    r = _chay(_f01g(la, _CHIP_DANG_GAN % json.dumps(ca["lenh"]["G"])),
              tep=TEP_F01, vo=VO_F01)
    assert r["co"], r
    assert r["chip"] and "xyz" in r["chip"] and r["title"] == "xyz", r


# ═══ AC-7 *(f)* — tương phản chữ chú giải + ô `.tg` (`NFR-I29`) ═══════════════
def _tep(ten: str) -> str:
    return open(os.path.join(pv.THU_MUC, ten), encoding="utf-8").read()


def _mau_cua(css: str, chon: str) -> str:
    """Tên token màu chữ khai cho **đúng** bộ chọn `chon` *(một khối)*."""
    k = re.findall(r"(?m)^" + re.escape(chon) + r"\{([^}]*)\}", css)
    assert len(k) == 1, f"⛔ không đo được: `{chon}{{…}}` khớp {len(k)} lần"
    m = re.findall(r"(?<![\w-])color:var\((--[\w-]+)\)", k[0])
    assert len(m) == 1, f"⛔ không đo được: `{chon}` khai {len(m)} màu chữ"
    return m[0]


def _hex(tok: str) -> str:
    # ⚠ Khai **đầu tiên** trong tệp = `:root` *(nền sáng — `fls/web` ⛔ có khối
    #   nền tối, `NFR-I27`)*; hex 3 ký tự *(`--surface:#fff`)* nở ra 6.
    v = re.findall(r"(?m)^\s*" + re.escape(tok)
                   + r":\s*#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\s*;", _tep("tokens.css"))
    assert v, f"⛔ không đo được: token {tok} ⛔ khai hex ở tokens.css"
    h = v[0] if len(v[0]) == 6 else "".join(c * 2 for c in v[0])
    return "#" + h


def _l(h: str) -> float:
    def k(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
    return 0.2126 * k(r) + 0.7152 * k(g) + 0.0722 * k(b)


def tuong_phan(a: str, b: str) -> float:
    """Tỷ số WCAG 2.x giữa hai màu hex."""
    x, y = sorted((_l(a), _l(b)), reverse=True)
    return (x + 0.05) / (y + 0.05)


@pytest.mark.parametrize("chon, nen, nguong", [
    (".tlegend", "--page", 4.5),        # chữ NGHĨA của chú giải
    (".cand .tg", "--surface", 3.0),    # ký hiệu một ký tự, có chú giải cùng màn
])
def test_AC7_tuong_phan_chu_chu_giai_va_o_tg_DAT_NFR_I29(chon, nen, nguong):
    """Đọc nguồn: màu khai ở `hinh.css` → hex ở `tokens.css` → tỷ số WCAG trên
    nền khai. Mong *(`BA-06` v4.16)*: **4,92** · **5,59**.

    ⛔ Chiều ĐỎ *(mã `8d7bea2`)*: `.tlegend{color:var(--faint)}` **2,17** ·
    `.cand .tg` `--faint` **2,47** ⇒ ĐỎ."""
    css = _tep("hinh.css")
    tok = _mau_cua(css, chon)
    t = tuong_phan(_hex(tok), _hex(nen))
    print(f"WO-037 AC-7 · {chon} {tok} trên {nen} = {t:.2f} : 1 (ngưỡng {nguong})")
    assert t >= nguong, f"{chon} {tok} trên {nen} = {t:.2f} < {nguong}"


def test_AC7_cong_tuong_phan_BAT_DUOC_faint():
    """⭐ Cổng phải ĐỎ được *(`Đ5`)*: `--faint` trên `--page` = **2,17** < 4,5."""
    assert round(tuong_phan(_hex("--faint"), _hex("--page")), 2) == 2.17
    assert round(tuong_phan(_hex("--faint"), _hex("--surface")), 2) == 2.47
    assert round(tuong_phan(_hex("--muted"), _hex("--page")), 2) == 4.92
