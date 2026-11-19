# -*- coding: utf-8 -*-
"""F4 (ISP 3.1.2 · Step 18 · `WO-160`) — SCR-F08 Cấu hình: bảng `IX.FX` CHỈ ĐỌC.

⭐ Cùng khuôn `test_isp_f03_hd.py`: **máy chủ thử THẬT** (`cua.dung_may`, chỉ đọc kho
TEST) ⇒ `GET /config/fx` lấy envelope THẬT, rồi nuôi vào `man_f08.js` qua node
headless. Hai vế — tuyến ĐỌC, màn VẼ — đối chiếu bằng CHÍNH `thieu`/`trung`/`lac`
của tuyến, ⛔ hằng gõ tay (spec §9: *"màn **đọc** ba mảng, ⛔ tự suy"*).

⛔ Kho config chỉ-THÊM ⇒ ⛔ dọn được; mỗi bài nạp lại ảnh nó cần, và bộ bài trả
lại ảnh ĐẦY ĐỦ (37 dòng) khi xong để ⛔ làm lệch bộ bài sau.
`TRÙNG` ⛔ nạp được vào kho (kho khoá theo `yyyymm`) ⇒ bài đó nuôi envelope trực
tiếp — mẫu `trung[]` do bài khai, màn chỉ được VẼ nó.
"""
from __future__ import annotations

import contextlib
import http.client
import json
import os
import subprocess
import threading
import time
from pathlib import Path

import psycopg
import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import cau_hinh_repo as chc
from fls.web.phuc_vu import lam_nguoi_phuc_vu
from tests.web import khung_node as kn
from tests.web.than_sinh import than_sinh

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]
ANH = GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json"
KHOA = "khoa-thu-cong-f08-bo-test-dai-hon-ba-muoi-hai-ky-tu-oke"
V = cua.bang_tuyen.TIEN_TO
TEP_F08 = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f08.js"]


def _nap(duong: Path) -> None:
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        chc.nap_ix_fx(c, str(duong), actor="bo-test-f08", thang_dau=202401,
                      nguon="tests/fixture/cau_hinh/ix_fx.json")


@pytest.fixture(autouse=True)
def _tra_anh_day_du():
    _nap(ANH)
    yield
    _nap(ANH)


@contextlib.contextmanager
def _may():
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA

    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    tok = the.dong_the({"sub": "ke.toan@apero.vn", "exp": int(time.time()) + 600,
                        "vai": ["ke_toan"]}, KHOA.encode())
    m = cua.dung_may(mo, cong=0, phuc_vu_tep=lam_nguoi_phuc_vu(
        {"the": tok, "actor": "ke.toan@apero.vn", "cho_ghi": False},
        than_sinh=than_sinh()))
    t = threading.Thread(target=m.serve_forever, daemon=True)
    t.start()
    try:
        yield m, tok
    finally:
        m.shutdown()
        m.server_close()
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu


def _config_fx() -> dict:
    with _may() as (m, tok):
        c = http.client.HTTPConnection(*m.server_address, timeout=10)
        try:
            c.request("GET", f"{V}/config/fx",
                      headers={"Authorization": f"Bearer {tok}"})
            r = c.getresponse()
            than = r.read()
            assert r.status == 200, (r.status, than[:200])
            return json.loads(than)["data"]
        finally:
            c.close()


def _ve(data: dict) -> dict:
    """Render `man_f08.js` với `data` làm thân `GET /config/fx`; trả các hàng."""
    kb = (
        "_TRA['/config/fx'] = {data: %s};"
        "const o = document.createElement('div'); o.id = 'than-f08';"
        "document.body.appendChild(o);"
        "await F08.ve(o);"
        "return {hang: [...document.querySelectorAll('[data-thang]')].map("
        "  r => ({thang: r.dataset.thang, txt: r.textContent,"
        "         nhan: [...r.querySelectorAll('.nhan-fx')].map(x => x.textContent)})),"
        " nut: document.querySelectorAll('button').length};"
        % json.dumps(data, ensure_ascii=False))
    return kn._chay(kb, tep=TEP_F08, vo="")


def _hang(ve: dict, thang: str) -> dict:
    hit = [h for h in ve["hang"] if h["thang"] == thang]
    assert len(hit) == 1, (thang, [h["thang"] for h in ve["hang"]])   # Đ5: khớp đúng 1
    return hit[0]


# ══ AC-1 · F4-F1 ════════════════════════════════════════════════════════════
@kn.can_node
def test_AC1_F4_F1_37_dong_va_202306_nhan_LAC():
    d = _config_fx()
    assert len(d["ky"]) == 37 and d["lac"] == [202306], d["lac"]   # Đ3: nền ≠ rỗng
    ve = _ve(d)
    assert len(ve["hang"]) == 37, len(ve["hang"])
    assert "LẠC" in _hang(ve, "202306")["nhan"]
    # ⛔ nhãn LẠC chỉ ở tháng tuyến khai lạc — hai chiều (Đ5)
    assert sum("LẠC" in h["nhan"] for h in ve["hang"]) == 1
    assert not any("CHẶN" in h["nhan"] or "TRÙNG" in h["nhan"] for h in ve["hang"])
    # số của màn = số của tuyến (⛔ hằng gõ tay): ô USD của dòng đầu
    ky0 = d["ky"][0]
    assert str(ky0["USD"]) in ve["hang"][0]["txt"].replace(".", "").replace(",", "")
    # Step 18 loại trừ ký (nút = 0); từ F5 (`WO-253`) mỗi dòng SẠCH chưa ký có đúng một nút
    # `Ký tháng` — đếm theo CHÍNH `ky[]`/`lac[]` của tuyến (⛔ hằng gõ tay), mẫu ≠ rỗng (Đ3).
    sach = [k for k in d["ky"] if k["trang_thai"] != "da_ky" and k["yyyymm"] not in d["lac"]]
    assert len(sach) == 36, len(sach)
    assert ve["nut"] == len(sach), (ve["nut"], len(sach))


# ══ AC-2 · F4-F2 ════════════════════════════════════════════════════════════
@kn.can_node
def test_AC2_F4_F2_thieu_202408_nhan_CHAN(tmp_path):
    anh = json.loads(ANH.read_text(encoding="utf-8"))
    anh["dong"] = [r for r in anh["dong"] if r["Month"] != "202408"]
    assert len(anh["dong"]) == 36
    p = tmp_path / "ix_fx_thieu.json"
    p.write_text(json.dumps(anh, ensure_ascii=False), encoding="utf-8")
    _nap(p)
    d = _config_fx()
    assert [str(x) for x in d["thieu"]] == ["202408"], d["thieu"]   # nền ≠ rỗng
    ve = _ve(d)
    assert "CHẶN" in _hang(ve, "202408")["nhan"]
    assert sum("CHẶN" in h["nhan"] for h in ve["hang"]) == 1
    assert len(ve["hang"]) == 37      # tháng thiếu vẫn có HÀNG — ⛔ biến mất im lặng


@kn.can_node
def test_AC2_F4_F2_trung_nhan_TRUNG_man_khong_cong_khong_chon_ho():
    d = _config_fx()
    ky = d["ky"] + [dict(d["ky"][3], USD="99999")]     # hai dòng 202404
    ve = _ve({**d, "ky": ky, "trung": [d["ky"][3]["yyyymm"]]})
    t = str(d["ky"][3]["yyyymm"])
    hang = [h for h in ve["hang"] if h["thang"] == t]
    assert len(hang) == 2, hang                         # ⛔ không gộp, ⛔ không chọn hộ
    assert all("TRÙNG" in h["nhan"] for h in hang)
    assert sum("TRÙNG" in h["nhan"] for h in ve["hang"]) == 2


# ══ AC-3 · bốn trạng thái ═══════════════════════════════════════════════════
@kn.can_node
def test_AC3_bon_trang_thai_qua_trang_thai_js():
    kb = (
        "const o = document.createElement('div'); document.body.appendChild(o);"
        "const lay = _TRA => 0;"
        "const ra = {};"
        # ⓐ đang tải: cửa không bao giờ xong
        "FLS.doc = () => new Promise(() => {});"
        "F08.ve(o); await Promise.resolve();"
        "ra.tai = !!o.querySelector('.tt-tai');"
        # ⓑ rỗng
        "FLS.doc = () => Promise.resolve({data: {ky: [], thieu: [], trung: [], lac: []}, meta: {}});"
        "await F08.ve(o); ra.rong = !!o.querySelector('.tt-rong');"
        "ra.rong_hang = o.querySelectorAll('[data-thang]').length;"
        # ⓒ lỗi có tên — kho chưa nạp (409)
        "FLS.doc = () => Promise.reject(new FLS.LoiCua('FLS-CAUHINH-CHUA-KHAI', 409, 'kho chua nap'));"
        "await F08.ve(o); const e = o.querySelector('.tt-loi');"
        "ra.loi = !!e; ra.loi_ten = e ? e.innerHTML : '';"
        "ra.loi_hang = o.querySelectorAll('[data-thang]').length;"
        "ra.loi_bang = o.querySelectorAll('table').length;"
        # ⓓ có số
        "FLS.doc = () => Promise.resolve({data: {ky: [{yyyymm: 202401, USD: '1', SGD: '2', COP: '3', VND: '1', HKD: '4', trang_thai: 'chua_ky'}], thieu: [], trung: [], lac: []}, meta: {}});"
        "await F08.ve(o); ra.co = o.querySelectorAll('[data-thang]').length;"
        "return ra;")
    ra = kn._chay(kb, tep=TEP_F08, vo="")
    assert ra["tai"] is True, ra
    assert ra["rong"] is True and ra["rong_hang"] == 0, ra
    assert ra["loi"] is True and "FLS-CAUHINH-CHUA-KHAI" in ra["loi_ten"], ra
    assert ra["loi_hang"] == 0 and ra["loi_bang"] == 0, ra   # ⛔ bảng trống im lặng
    assert ra["co"] == 1, ra


# ══ F4-R1-01 · `KQ-162` — Chromium thật, 390 px ═════════════════════════════
def _do_390() -> dict:
    """Mở trang thật ở 390 px, bấm tab ⑥, đợi 37 hàng; đo CẢ TRANG
    (`documentElement`) và CHÍNH khung bọc bảng. Dùng lại bộ dò node/playwright/
    Chromium của `test_isp_f03_hd.py` (một nguồn)."""
    from tests.web import test_isp_f03_hd as f3
    if f3.NODE is None or f3.PW is None or f3.CHROME is None:
        pytest.skip("thiếu node / playwright / Chromium")
    mjs = (
        "import pkg from %(pw)s; const { chromium } = pkg;\n"
        "const b = await chromium.launch({ executablePath: %(cr)s,"
        " args: ['--no-sandbox'], headless: true });\n"
        "const pg = await b.newPage({ viewport: { width: 390, height: 820 },"
        " deviceScaleFactor: 1 });\n"
        "await pg.goto(%(url)s);\n"
        "await pg.click('button[data-s=\"man-f08\"]');\n"
        "await pg.waitForSelector('#than-f08 [data-thang]', { timeout: 15000 });\n"
        "const res = await pg.evaluate(() => {\n"
        "  const de = document.documentElement;\n"
        "  const t = document.querySelector('#than-f08 table');\n"
        "  const kh = t.parentElement;\n"
        "  return { iw: window.innerWidth, sw: de.scrollWidth, cw: de.clientWidth,\n"
        "    hang: document.querySelectorAll('#than-f08 [data-thang]').length,\n"
        "    bang_w: t.getBoundingClientRect().width,\n"
        "    kh_sw: kh.scrollWidth, kh_cw: kh.clientWidth,\n"
        "    kh_ox: getComputedStyle(kh).overflowX };\n"
        "});\n"
        "console.log(JSON.stringify(res));\n"
        "await b.close();\n"
        % {"pw": json.dumps(f3.PW), "cr": json.dumps(f3.CHROME),
           "url": json.dumps(_do_390.url)}
    )
    r = subprocess.run([f3.NODE, "--input-type=module", "-e", mjs],
                       capture_output=True, text=True, encoding="utf-8",
                       timeout=90)
    assert r.returncode == 0, f"⛔ node/chromium NO:\n{r.stdout}\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


def test_F4_R1_01_bang_IXFX_khong_tran_ngang_o_390px():
    """⛔ Trang ⛔ tràn ngang ở 390 px (mã cũ: `scrollWidth 475 > clientWidth 390`).
    Bảng 7 cột rộng hơn màn ⇒ phải cuộn TRONG khung riêng. Đo ba thứ: trang
    (`sw ≤ cw`), 37 hàng thật (Đ3: ⛔ đo trên bảng rỗng), và bảng THẬT rộng hơn
    khung `kh_cw` (⇒ khung đang cuộn thật, ⛔ bảng bị cắt/ép nhỏ — Đ5 hai chiều)."""
    with _may() as (m, _tok):
        _do_390.url = "http://%s:%d/" % m.server_address
        res = _do_390()
    assert res["hang"] == 37, res                        # Đ3: mẫu số ≠ 0
    assert res["bang_w"] > res["kh_cw"], res             # bảng thật rộng hơn khung
    assert res["kh_ox"] in ("auto", "scroll"), res       # khung cuộn riêng
    assert res["sw"] <= res["cw"], (
        "trang TRÀN ngang ở 390 px: scrollWidth=%(sw)d > clientWidth=%(cw)d" % res)
