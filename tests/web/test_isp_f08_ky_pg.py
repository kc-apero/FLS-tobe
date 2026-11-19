# -*- coding: utf-8 -*-
"""F5 (ISP 3.1.2 · Step 37 · `WO-253`) — SCR-F08: **ký tháng tỷ giá** (D1) có hộp xác nhận.

⭐ Tích hợp THẬT, ⛔ cửa giả: máy chủ thử (`cua.dung_may`, kho TEST, cửa GHI mở) phục vụ
chính `index.html` + `man_f08.js`; Chromium headless (Playwright của node) bấm như người.
Mỗi bài nạp `IX.FX` với USD NGẪU NHIÊN ⇒ dấu vân mọi tháng đổi ⇒ mọi tháng *chưa ký*
(kho chỉ-THÊM, ⛔ dọn được; bài chạy lại được). Cuối bộ trả lại ảnh ĐẦY ĐỦ.

Chữ lỗi qua `goi_cua.js` *(`FLS-CAUHINH-DA-KY`)*; ⛔ gửi `actor` trong thân *(cửa trả 400 —
`AC-5`)*; người ký lấy từ THẺ *(`ke.toan@apero.vn`)*.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import shutil
import subprocess
import threading
import time
import uuid
from pathlib import Path

import psycopg
import pytest

from fls.api import cua, the
from fls.cau_hinh import fx
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from fls.web.phuc_vu import lam_nguoi_phuc_vu
from tests.web.than_sinh import than_sinh

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
ANH = GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json"
KHOA = "khoa-thu-cong-f08-ky-bo-test-dai-hon-ba-muoi-hai-ky-tu-oke"
V = cua.bang_tuyen.TIEN_TO
NGUOI_KY = "ke.toan.f5@vi-du.invalid"
NODE = shutil.which("node")
can_node = pytest.mark.skipif(NODE is None, reason="⛔ máy ⛔ có `node` — cổng BỎ QUA, ⛔ đạt")


def _nap(duong: Path) -> None:
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_fx(c, str(duong), actor="bo-test-f5", thang_dau=202401,
                      nguon="tests/fixture/cau_hinh/ix_fx.json")


@pytest.fixture(autouse=True)
def _tuoi(tmp_path):
    """USD ngẫu nhiên ⇒ mọi tháng chưa ký; xong thì trả ảnh đầy đủ."""
    anh = json.loads(ANH.read_text(encoding="utf-8"))
    for r in anh["dong"]:
        r["USD"] = str(10000 + uuid.uuid4().int % 90000)
    p = tmp_path / "ix_fx_f5.json"
    p.write_text(json.dumps(anh), encoding="utf-8")
    _nap(p)
    yield
    _nap(ANH)


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
  const goc = process.env.GOC, anh = process.env.ANH_DIR || '';
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1100, height: 800 }, deviceScaleFactor: 1 });
  const post = [];
  p.on('request', r => { if (r.method() === 'POST') post.push({ u: r.url(), than: r.postData() }); });
  await p.goto(goc + '/');
  await p.click('button[data-s="man-f08"]');
  await p.waitForSelector('tr[data-thang="202510"]');
  const hang = async t => p.$eval('tr[data-thang="' + t + '"]', r => ({
      txt: r.textContent.replace(/\s+/g, ' ').trim(),
      nut: [...r.querySelectorAll('button')].map(x => ({ chu: x.textContent, tat: x.disabled })) }));
  const hop = async () => p.$eval('#scrim', s => ({ mo: s.classList.contains('on'),
      txt: s.textContent.replace(/\s+/g, ' ').trim() }));
  const nut_ky = t => p.locator('tr[data-thang="' + t + '"] button').first();
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
  kq.truoc = await hang('202510');
  await chup('f5_truoc_ky');
  await nut_ky('202510').click();
  await p.waitForSelector('#scrim.on');
  kq.hop = await hop();
  kq.post_truoc_xn = post.length;                 // hộp mở nhưng CHƯA xác nhận
  await p.click('#dlg-f button.pri');
  await p.waitForFunction(() => { const r = document.querySelector('tr[data-thang="202510"]');
      return r && r.textContent.includes('đã ký'); });
  kq.sau = await hang('202510');
  kq.hop_sau = await hop();
  await chup('f5_sau_ky');
"""
KB_F2 = r"""
  await nut_ky('202511').click();
  await p.waitForSelector('#scrim.on');
  // người khác ký 202511 NGAY SAU KHI màn đã vẽ (màn cũ) — cùng cửa, cùng thẻ
  kq.ky_ngoai = await p.evaluate(async (g) => {
    const r = await fetch(g, { method: 'POST', headers: { 'Authorization': 'Bearer ' + window.FLS_PHIEN.the,
        'Content-Type': 'application/json' }, body: '{}' });
    return r.status; }, '/api/fls/v1/config/fx/202511/sign');
  await p.click('#dlg-f button.pri');
  await p.waitForFunction(() => document.querySelector('#scrim .note.crit'));
  kq.hop = await hop();
"""
KB_F3 = r"""
  await nut_ky('202512').click();
  await p.waitForSelector('#scrim.on');
  await p.click('#dlg-f button:not(.pri)');
  await p.waitForFunction(() => !document.querySelector('#scrim').classList.contains('on'));
  kq.hang = await hang('202512');
  kq.hop = await hop();
"""
KB_AC5 = r"""
  kq.tra = await p.evaluate(async () => {
    const r = await fetch('/api/fls/v1/config/fx/202509/sign', { method: 'POST',
      headers: { 'Authorization': 'Bearer ' + window.FLS_PHIEN.the, 'Content-Type': 'application/json' },
      body: JSON.stringify({ actor: 'nguoi-gia-mao' }) });
    return { s: r.status, j: await r.json() }; });
"""


def _chay(kb: str, cong: int, anh_dir: str = "") -> dict:
    npm = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    env = dict(os.environ, NODE_PATH=npm, GOC=f"http://127.0.0.1:{cong}", ANH_DIR=anh_dir)
    r = subprocess.run([NODE, "-e", _DAU + kb + _CUOI], capture_output=True, text=True,
                       encoding="utf-8", env=env, timeout=120)
    assert r.returncode == 0, f"⛔ playwright NỔ:\n{r.stdout}\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


def _da_ky() -> dict:
    """Tháng → chữ ký ĐANG HIỆU LỰC — cùng luật cửa (`xu_ly.ty_gia`): chữ ký chỉ tính khi
    còn phủ đúng dấu vân tỷ giá hiện hành. ⛔ đọc thô: bài C7 để lại chữ ký lệch dấu vân
    (kho chỉ-THÊM) và nó làm tiền đề `chưa ký` sai trong bộ bài đầy đủ (đo 19/11)."""
    with noi_chi_doc(dsn_test()) as c:
        ky = chc.doc_ky_fx(c)
        return {d.yyyymm: ky[d.yyyymm] for d in chc.doc_fx(c).ky
                if d.yyyymm in ky and ky[d.yyyymm].dau_van_tay == fx.dau_van_tay(d)}


# ══ AC-1 · F5-F1 ════════════════════════════════════════════════════════════
@can_node
def test_AC1_F5_F1_ky_202510_hop_xac_nhan_roi_da_ky_nut_khoa():
    assert 202510 not in _da_ky()                      # Đ3: nền = CHƯA ký (mẫu ≠ rỗng)
    with _may() as (m, _):
        kq = _chay(KB_F1, m.server_address[1], os.environ.get("F5_ANH_DIR", ""))
    # trước: dòng có đúng MỘT nút 'Ký tháng', chưa khoá
    assert kq["truoc"]["nut"] == [{"chu": "Ký tháng", "tat": False}], kq["truoc"]
    # hộp xác nhận nêu THÁNG và CÁI SẼ XẢY RA; chưa xác nhận thì ⛔ POST
    assert kq["hop"]["mo"] and "202510" in kq["hop"]["txt"], kq["hop"]
    assert kq["post_truoc_xn"] == 0
    # xác nhận ⇒ ĐÚNG một POST, thân rỗng (⛔ actor)
    assert len(kq["post"]) == 1 and kq["post"][0]["u"].endswith("/config/fx/202510/sign")
    assert json.loads(kq["post"][0]["than"]) == {}
    # sau: 'đã ký · người ký (từ thẻ) · ngày', nút khoá, hộp đóng
    sau = kq["sau"]
    assert "đã ký" in sau["txt"] and NGUOI_KY in sau["txt"], sau
    assert time.strftime("%Y") in sau["txt"] or "-" in sau["txt"]
    assert sau["nut"] and all(n["tat"] for n in sau["nut"]), sau["nut"]
    assert not kq["hop_sau"]["mo"]
    # kho THẬT khớp: người ký = thẻ
    assert _da_ky()[202510].actor == NGUOI_KY


# ══ AC-2 · F5-F2 ════════════════════════════════════════════════════════════
@can_node
def test_AC2_F5_F2_ky_lai_409_chu_tieng_viet_khong_ma_tho():
    with _may() as (m, _):
        kq = _chay(KB_F2, m.server_address[1])
    assert kq["ky_ngoai"] == 201, kq["ky_ngoai"]       # Đ3: lượt ký trước THÀNH CÔNG
    txt = kq["hop"]["txt"]
    assert kq["hop"]["mo"]                              # hộp ở nguyên, báo ngay trong hộp
    assert "đã được ký rồi" in txt, txt
    assert "FLS-CAUHINH-DA-KY" not in txt and "409" not in txt.split("đã được ký")[0], txt
    assert len([p for p in kq["post"] if p["u"].endswith("/202511/sign")]) == 2  # ngoài + màn


# ══ AC-3 · F5-F3 ════════════════════════════════════════════════════════════
@can_node
def test_AC3_F5_F3_huy_o_hop_xac_nhan_khong_goi_POST():
    with _may() as (m, _):
        kq = _chay(KB_F3, m.server_address[1])
    assert kq["post"] == [], kq["post"]                # đếm request: 0
    assert not kq["hop"]["mo"]
    h = kq["hang"]
    assert "đã ký" not in h["txt"] and h["nut"] == [{"chu": "Ký tháng", "tat": False}], h
    assert 202512 not in _da_ky()


# ══ AC-5 ════════════════════════════════════════════════════════════════════
@can_node
def test_AC5_cua_tra_400_khi_than_co_actor_va_man_khong_gui_actor():
    with _may() as (m, _):
        kq = _chay(KB_AC5, m.server_address[1])
    assert kq["tra"]["s"] == 400, kq["tra"]
    assert 202509 not in _da_ky()                      # ⛔ ghi gì khi bị từ chối
    # màn: thân POST của F1 đã khẳng `{}` — ở đây chặn tĩnh: mã màn ⛔ nhắc `actor` ở thân
    ma = (GOC / "fls" / "web" / "tep" / "man_f08.js").read_text(encoding="utf-8")
    import re
    assert not re.search(r"\bactor\s*:", ma), "⛔ man_f08.js gửi `actor` trong thân"
