# -*- coding: utf-8 -*-
"""F7 (ISP 3.1.2 · Step 40 · `WO-273`) — SCR-F08: **ký bản Daily Report 3** (`IX.TMP`, C13).

⭐ Tích hợp THẬT, ⛔ cửa giả (khuôn `test_isp_f08_ky_pg.py`): máy chủ thử (`cua.dung_may`, kho
TEST, cửa GHI mở) phục vụ chính `index.html` + `man_f08.js`; Chromium headless bấm như người.
Dữ liệu 2 phiên bản đưa vào bằng HÀM MỨC REPO của C13 (`dua_ban_ky`/`ky_ban` — ⛔ tuyến ghi
thứ ba). Mỗi bài chọn một `{ky}` CHƯA có bản *(Đ3: mẫu số ≠ rỗng; kho chỉ-THÊM ⇒ ⛔ dọn được)*.
Ca lỗi `404`/`400`/`500`/mạng dựng bằng `page.route` *(tuyến thật không sinh được ở màn)*;
`401` + `400` + `409` đi qua cửa thật.
"""
from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import subprocess
import threading
import time
import uuid
from pathlib import Path

import psycopg
import pytest

from fls.api import cua, the
from fls.cau_hinh import ban_ky
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from fls.web.phuc_vu import lam_nguoi_phuc_vu
from tests.web.than_sinh import than_sinh

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
KHOA = "khoa-thu-cong-f08-ky-ban-bo-test-dai-hon-ba-muoi-hai-ky-tu"
NGUOI_KY = "ke.toan.f7@vi-du.invalid"
NGUOI_CU = "nguoi.ky.ban1@vi-du.invalid"
NODE = shutil.which("node")
can_node = pytest.mark.skipif(NODE is None, reason="⛔ máy ⛔ có `node` — cổng BỎ QUA, ⛔ đạt")


def _ky_trong() -> int:
    """Một kỳ `yyyymm` (2000…2099) CHƯA có bản nào — Đ3: ⛔ tin mẫu mà ⛔ đo mẫu số."""
    with noi_chi_doc(dsn_test()) as c:
        for _ in range(200):
            n = uuid.uuid4().int
            ky = (2000 + n % 100) * 100 + 1 + (n // 100) % 12
            if not chc.doc_ban_ky(c, ky):
                return ky
    raise AssertionError("⛔ không tìm được kỳ trống")


def _dua(ky: int, **noi_dung) -> None:
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.dua_ban_ky(c, ky, noi_dung, actor="engine-thu-f7")


def _ky_cu(ky: int) -> None:
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.ky_ban(c, ky, actor=NGUOI_CU)


def _hai_ban() -> int:
    """Kỳ có 2 phiên bản: bản 1 ĐÃ ký (NGUOI_CU), bản 2 chưa."""
    ky = _ky_trong()
    _dua(ky, o=uuid.uuid4().hex)
    _ky_cu(ky)
    _dua(ky, o=uuid.uuid4().hex)
    return ky


def _ban(ky: int) -> list:
    with noi_chi_doc(dsn_test()) as c:
        return chc.doc_ban_ky(c, ky)


@contextlib.contextmanager
def _may():
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA

    @contextlib.contextmanager
    def mo_doc():
        c = noi_chi_doc(dsn_test())
        try:
            yield c
        finally:
            c.close()

    @contextlib.contextmanager
    def mo_ghi():
        c = psycopg.connect(dsn_test(), autocommit=True)
        try:
            yield c
        finally:
            c.close()

    tok = the.dong_the({"sub": NGUOI_KY, "exp": int(time.time()) + 600,
                        "vai": ["ke_toan"]}, KHOA.encode())
    m = cua.dung_may(mo_doc, cong=0, mo_ghi=mo_ghi, phuc_vu_tep=lam_nguoi_phuc_vu(
        {"the": tok, "actor": NGUOI_KY, "cho_ghi": True}, than_sinh=than_sinh()))
    threading.Thread(target=m.serve_forever, daemon=True).start()
    try:
        yield m, tok
    finally:
        m.shutdown()
        m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


# ── Kịch bản Playwright (node). Mỗi kịch bản trả MỘT dòng JSON. ───────────────────────
_DAU = r"""
const { chromium } = require('playwright');
(async () => {
  const goc = process.env.GOC, anh = process.env.ANH_DIR || '', KY = process.env.KY;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 900 }, deviceScaleFactor: 1 });
  const post = [];
  p.on('request', r => { if (r.method() === 'POST') post.push({ u: r.url(), than: r.postData() }); });
  await p.goto(goc + '/');
  await p.click('button[data-s="man-f08"]');
  await p.waitForSelector('#ban-ky');
  const xem = async ky => { await p.fill('#ban-ky', ky); await p.click('#ban-xem'); };
  const ds = () => p.$eval('#ban-ds', d => ({
      txt: d.textContent.replace(/\s+/g, ' ').trim(),
      hang: [...d.querySelectorAll('tr[data-ban]')].map(r => ({ pb: r.dataset.ban,
          txt: r.textContent.replace(/\s+/g, ' ').trim(),
          ck: (r.querySelector('.ck') || {}).title || '' })),
      nut: [...d.querySelectorAll('button')].map(x => ({ chu: x.textContent.trim(), tat: x.disabled })) }));
  const hop = () => p.$eval('#scrim', s => ({ mo: s.classList.contains('on'),
      txt: s.textContent.replace(/\s+/g, ' ').trim(),
      nut: [...s.querySelectorAll('#dlg-f button')].map(x => ({ chu: x.textContent, tat: x.disabled })) }));
  const nut_ky = () => p.locator('#ban-ds button.nut-ky-ban');
  const chup = async ten => { if (anh) await p.screenshot({ path: anh + '/' + ten + '.png' }); };
  let kq = {};
"""
_CUOI = r"""
  kq.post = post.map(x => ({ u: x.u.replace(goc, ''), than: x.than }));
  console.log(JSON.stringify(kq));
  await b.close();
})().catch(e => { console.error(e); process.exit(1); });
"""

KB_F1 = r"""
  await xem(KY);
  await p.waitForSelector('tr[data-ban="2"]');
  kq.truoc = await ds();
  await chup('f7_truoc_ky');
  await nut_ky().click();
  await p.waitForSelector('#scrim.on');
  kq.hop = await hop();
  kq.post_truoc_xn = post.length;
  await p.dblclick('#dlg-f button.pri');                 // bấm KÉP nhanh
  await p.waitForFunction(() => { const r = document.querySelector('tr[data-ban="2"]');
      return r && r.textContent.includes('đã ký'); });
  kq.sau = await ds();
  kq.hop_sau = await hop();
  await chup('f7_sau_ky');
"""
KB_RONG = r"""
  await xem(KY);
  await p.waitForFunction(() => document.querySelector('#ban-ds .ban-rong'));
  kq.ds = await ds();
"""
KB_HUY = r"""
  await xem(KY);
  await p.waitForSelector('tr[data-ban="2"]');
  await nut_ky().click();
  await p.waitForSelector('#scrim.on');
  await p.click('#dlg-f button:not(.pri)');              // Huỷ bằng nút
  await p.waitForFunction(() => !document.querySelector('#scrim').classList.contains('on'));
  kq.tieu_diem_huy = await p.evaluate(() => document.activeElement.className);
  await nut_ky().click();
  await p.waitForSelector('#scrim.on');
  await p.keyboard.press('Enter');                       // Enter ⛔ là phím xác nhận
  kq.hop_enter = await hop();
  await p.keyboard.press('Escape');                      // Esc đóng hộp, 0 POST
  await p.waitForFunction(() => !document.querySelector('#scrim').classList.contains('on'));
  kq.tieu_diem_esc = await p.evaluate(() => document.activeElement.className);
  kq.ds = await ds();
"""
KB_409 = r"""
  await xem(KY);
  await p.waitForSelector('tr[data-ban="2"]');
  await nut_ky().click();
  await p.waitForSelector('#scrim.on');
  kq.ky_ngoai = await p.evaluate(async (g) => {          // người khác ký ngay sau khi màn vẽ
    const r = await fetch(g, { method: 'POST', headers: { 'Authorization': 'Bearer ' + window.FLS_PHIEN.the,
        'Content-Type': 'application/json' }, body: '{}' });
    return r.status; }, '/api/fls/v1/report/snapshot/' + KY + '/sign');
  await p.click('#dlg-f button.pri');
  await p.waitForFunction(() => document.querySelector('#scrim .note.crit'));
  kq.hop = await hop();
  await p.waitForFunction(() => [...document.querySelectorAll('tr[data-ban]')]
      .every(r => r.textContent.includes('đã ký')), null, { timeout: 5000 }).catch(() => {});
  kq.ds = await ds();
"""
KB_LOI = r"""
  const chu_loi = {};
  await xem(KY);
  await p.waitForSelector('tr[data-ban="1"]');
  for (const [ten, tt] of [['404', 404], ['400', 400], ['500', 500]]) {
    await p.route('**/report/snapshot/*/sign', r => r.fulfill({ status: tt, contentType: 'application/json',
      body: JSON.stringify({ data: null, error: { code: tt === 404 ? 'FLS-NOT-FOUND'
        : tt === 400 ? 'FLS-BAD-REQUEST' : 'FLS-INTERNAL', detail: 'x' }, meta: {} }) }));
    await nut_ky().click();
    await p.waitForSelector('#scrim.on');
    await p.click('#dlg-f button.pri');
    await p.waitForSelector('#scrim .note.crit');
    chu_loi[ten] = await hop();
    await p.click('#dlg-f button:not(.pri)');
    await p.waitForFunction(() => !document.querySelector('#scrim').classList.contains('on'));
    await p.unroute('**/report/snapshot/*/sign');
  }
  await p.route('**/report/snapshot/*/sign', r => r.abort());   // lỗi mạng
  await nut_ky().click();
  await p.waitForSelector('#scrim.on');
  await p.click('#dlg-f button.pri');
  await p.waitForSelector('#scrim .note.crit');
  chu_loi.mang = await hop();
  kq.chu_loi = chu_loi;
"""
KB_GET = r"""
  await xem('2025-12');                                  // 400 — sai khuôn yyyymm
  await p.waitForSelector('#ban-ds .tt-loi');
  kq.g400 = await ds();
  await p.evaluate(() => { window.FLS_PHIEN.the = ''; });
  await xem(KY);                                         // 401 — thiếu thẻ
  await p.waitForFunction(() => /401/.test(document.querySelector('#ban-ds').textContent));
  kq.g401 = await ds();
"""
KB_AC5 = r"""
  kq.tra = await p.evaluate(async (g) => {
    const r = await fetch(g, { method: 'POST', headers: { 'Authorization': 'Bearer ' + window.FLS_PHIEN.the,
      'Content-Type': 'application/json' }, body: JSON.stringify({ actor: 'nguoi-gia-mao' }) });
    return { s: r.status }; }, '/api/fls/v1/report/snapshot/' + KY + '/sign');
"""


def _chay(kb: str, cong: int, ky: int | str = 0, anh_dir: str = "") -> dict:
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env = dict(os.environ, NODE_PATH=npm, GOC=f"http://127.0.0.1:{cong}", ANH_DIR=anh_dir,
               KY=str(ky))
    r = subprocess.run([NODE, "-e", _DAU + kb + _CUOI], capture_output=True, text=True,
                       encoding="utf-8", env=env, timeout=120)
    assert r.returncode == 0, f"⛔ playwright NỔ:\n{r.stdout}\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


# ══ AC-1 · F7-F1 ════════════════════════════════════════════════════════════
@can_node
def test_AC1_F7_F1_ky_ban2_hop_xac_nhan_roi_ca_hai_da_ky_checksum_khac_ban1_giu_nguyen():
    ky = _hai_ban()
    nen = _ban(ky)
    assert [b.trang_thai for b in nen] == ["da_ky", "chua_ky"]      # Đ3: nền = 2 bản, 1 đã ký
    with _may() as (m, _):
        kq = _chay(KB_F1, m.server_address[1], ky, os.environ.get("F7_ANH_DIR", ""))
    # trước: danh sách 2 phiên bản đọc từ cửa — phiên bản · checksum rút gọn · trạng thái · người ký · ngày
    h1, h2 = kq["truoc"]["hang"]
    assert h1["pb"] == "1" and "đã ký" in h1["txt"] and NGUOI_CU in h1["txt"], h1
    assert nen[0].checksum[:12] in h1["txt"] and nen[0].checksum not in h1["txt"], h1  # rút gọn
    assert h1["ck"] == nen[0].checksum                              # title = đủ 64 ký tự
    assert nen[0].ky_luc[:10] in h1["txt"], h1
    assert h2["pb"] == "2" and "chưa ký" in h2["txt"] and nen[1].checksum[:12] in h2["txt"], h2
    assert kq["truoc"]["nut"] == [{"chu": "Ký bản", "tat": False}], kq["truoc"]["nut"]
    # hộp xác nhận nêu kỳ + phiên bản; chưa xác nhận thì ⛔ POST
    assert kq["hop"]["mo"] and str(ky) in kq["hop"]["txt"] and "phiên bản 2" in kq["hop"]["txt"]
    assert kq["post_truoc_xn"] == 0
    # AC-3: bấm KÉP nhanh ⇒ ĐÚNG một POST, thân rỗng (AC-5)
    assert len(kq["post"]) == 1, kq["post"]
    assert kq["post"][0]["u"].endswith(f"/report/snapshot/{ky}/sign")
    assert json.loads(kq["post"][0]["than"]) == {}
    # sau: cả hai 'đã ký', checksum KHÁC nhau, bản 1 giữ nguyên người ký/ngày
    s1, s2 = kq["sau"]["hang"]
    assert "đã ký" in s1["txt"] and "đã ký" in s2["txt"], kq["sau"]
    assert s1["ck"] != s2["ck"] and len(s1["ck"]) == len(s2["ck"]) == 64
    assert NGUOI_CU in s1["txt"] and nen[0].ky_luc[:10] in s1["txt"]            # bản 1 NGUYÊN
    assert NGUOI_KY in s2["txt"], s2                                            # AC-5: từ THẺ
    assert kq["sau"]["nut"] == [{"chu": "Ký bản", "tat": True}]                 # AC-2: mới nhất đã ký ⇒ khoá
    assert not kq["hop_sau"]["mo"]
    # kho THẬT: bản 1 y nguyên, bản 2 do thẻ ký, đúng 1 sự kiện ký mới
    sau = _ban(ky)
    assert (sau[0].actor, sau[0].ky_luc, sau[0].checksum) == (nen[0].actor, nen[0].ky_luc, nen[0].checksum)
    assert sau[1].trang_thai == "da_ky" and sau[1].actor == NGUOI_KY


# ══ AC-2 ════════════════════════════════════════════════════════════════════
@can_node
def test_AC2_ky_chua_co_ban_chu_trang_thai_rong_co_ten_nut_ky_khoa():
    ky = _ky_trong()
    assert _ban(ky) == []                                           # Đ3: nền = kỳ RỖNG thật
    with _may() as (m, _):
        kq = _chay(KB_RONG, m.server_address[1], ky)
    d = kq["ds"]
    assert d["hang"] == []
    assert "chưa có bản" in d["txt"] and str(ky) in d["txt"], d     # chữ có tên, ⛔ bảng trống im lặng
    assert all(n["tat"] for n in d["nut"]), d["nut"]                # nút ký ẩn hoặc khoá
    assert kq["post"] == []


# ══ AC-3 · huỷ + AC-6 · phím ═════════════════════════════════════════════════
@can_node
def test_AC3_AC6_huy_o_hop_0_POST_esc_enter_khong_ky_tieu_diem_ve_nut():
    ky = _hai_ban()
    with _may() as (m, _):
        kq = _chay(KB_HUY, m.server_address[1], ky)
    assert kq["post"] == [], kq["post"]                             # đếm request: 0
    assert "nut-ky-ban" in kq["tieu_diem_huy"], kq["tieu_diem_huy"]
    assert kq["hop_enter"]["mo"], kq["hop_enter"]                   # Enter ⛔ xác nhận hộp
    assert "nut-ky-ban" in kq["tieu_diem_esc"], kq["tieu_diem_esc"]
    assert kq["ds"]["hang"][1]["txt"].count("chưa ký") == 1
    assert [b.trang_thai for b in _ban(ky)] == ["da_ky", "chua_ky"]


# ══ AC-4 · 409 chữ ngữ cảnh BẢN BÁO CÁO (đóng C13-R1-04) ════════════════════
@can_node
def test_AC4_C13_R1_04_409_chu_ngu_canh_ban_bao_cao_khong_noi_ty_gia_man_ve_lai():
    ky = _hai_ban()
    with _may() as (m, _):
        kq = _chay(KB_409, m.server_address[1], ky)
    assert kq["ky_ngoai"] == 201, kq["ky_ngoai"]                    # Đ3: lượt ký trước THÀNH CÔNG
    txt = kq["hop"]["txt"]
    assert kq["hop"]["mo"] and "bản báo cáo" in txt and "đã được ký" in txt, txt
    assert "tỷ giá" not in txt.lower() and "FLS-CAUHINH-DA-KY" not in txt, txt   # ⛔ chữ của C7
    assert all(not n["tat"] for n in kq["hop"]["nut"]), kq["hop"]["nut"]         # ⛔ treo nút
    assert all("đã ký" in h["txt"] for h in kq["ds"]["hang"]), kq["ds"]          # tải lại từ cửa
    assert len([p for p in kq["post"] if p["u"].endswith(f"/{ky}/sign")]) == 2


@can_node
def test_AC4_404_400_500_mang_chu_tieng_viet_hop_o_nguyen_nut_khong_treo():
    ky = _hai_ban()
    with _may() as (m, _):
        kq = _chay(KB_LOI, m.server_address[1], ky)
    assert set(kq["chu_loi"]) == {"404", "400", "500", "mang"}      # Đ3: đủ 4 ca
    for ten, h in kq["chu_loi"].items():
        assert h["mo"], (ten, h)
        assert not re.search(r"FLS-[A-Z-]+", h["txt"]), (ten, h["txt"])          # ⛔ mã thô
        assert re.search(r"[ăâđêôơưáàảãạ]", h["txt"]), (ten, h["txt"])           # chữ tiếng Việt
        assert "undefined" not in h["txt"] and "[object" not in h["txt"], (ten, h["txt"])
        assert any(not n["tat"] for n in h["nut"]), (ten, h["nut"])              # ⛔ treo nút
    assert [b.trang_thai for b in _ban(ky)] == ["da_ky", "chua_ky"]              # ⛔ ghi gì


@can_node
def test_AC4_GET_400_sai_khuon_va_401_thieu_the_chu_tieng_viet():
    ky = _hai_ban()
    with _may() as (m, _):
        kq = _chay(KB_GET, m.server_address[1], ky)
    for k in ("g400", "g401"):
        t = kq[k]["txt"]
        assert re.search(r"[ăâđêôơưáàảãạ]", t) and "undefined" not in t, (k, t)
    assert "400" in kq["g400"]["txt"] and kq["g400"]["hang"] == []
    assert "401" in kq["g401"]["txt"] and kq["g401"]["hang"] == []


# ══ AC-5 ════════════════════════════════════════════════════════════════════
@can_node
def test_AC5_cua_tra_400_khi_than_co_actor_va_man_khong_gui_actor():
    ky = _hai_ban()
    with _may() as (m, _):
        kq = _chay(KB_AC5, m.server_address[1], ky)
    assert kq["tra"]["s"] == 400, kq["tra"]
    assert [b.trang_thai for b in _ban(ky)] == ["da_ky", "chua_ky"]  # ⛔ ghi gì khi bị từ chối
    ma = (GOC / "fls" / "web" / "tep" / "man_f08.js").read_text(encoding="utf-8")
    assert not re.search(r"\bactor\s*:", ma), "⛔ man_f08.js gửi `actor` trong thân"
    assert ban_ky.BANG == "IX.TMP"
