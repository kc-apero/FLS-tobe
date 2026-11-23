# -*- coding: utf-8 -*-
"""FG (ISP 3.1.2 · Step 9 · `WO-116`) — F03 'Cổng hôm nay' hiện cổng HD1 **đọc
tuyến thật**.

⛔⛔ **Vì sao bài này đi QUA MÁY CHỦ THỬ (`fls/web/phuc_vu.py` + `fls/api/cua.py`),
⛔ gọi `doc_cong` thẳng.** `B2` phải chứng minh *một vòng tròn*: vỏ màn ra được,
một cửa thật (`GET /gates`) trả được, và `man_f03.js` vẽ **đúng** cái cửa ấy trả.
Một bài gọi hàm Python rồi tự dựng envelope ⛔ chứng minh được điều đó — nó thử
một con số **bài tự bịa**, ⛔ phải con số TUYẾN trả. Nên ở đây:
  · `FG-F1`/`FG-F2`: **chạy máy thật** với `tep_do` (thật / vắng) ⇒ `GET /gates`
    lấy envelope THẬT, rồi nuôi envelope ấy vào `man_f03.js` render qua **node
    headless** (`khung_node._chay` + `dom_gia.js`). Hai vế — tuyến ĐO, màn VẼ —
    đối chiếu bằng CHÍNH chuỗi tuyến trả (`da_do`, `chua_do_duoc`), ⛔ hằng số gõ
    tay.
  · `FG-F3`: *"23 kỳ ở 390 px ⛔ tràn ngang"* là câu hỏi **pixel bố cục** — và
    `dom_gia.js` khai thẳng (dòng 11-16) rằng pixel *"⛔ kiểm được, còn nằm ở
    `B7 · UAT`"*. ⇒ bài này đo bằng **Chromium thật** (headless, tất định), đo
    `scrollWidth ≤ clientWidth` của CHÍNH thẻ HD1 ở bề rộng 390 px. ⚠ ⛔ có
    Chromium ⇒ BỎ QUA (⛔ xanh giả — Đ5), ⛔ phải "không thấy tràn".
  · `FG-F4`: *"bộ `tests/web` sẵn có xanh"* = **hồi quy**, đo bằng `--duong-nen`
    của nhánh (⛔ một bài mới ở đây — một bài mới chép lại suite là bài thừa).

⭐ Đo nền (phiên cloud 17/11, cụm 5436, `tep_do` THẬT = `docs/ITL/_tools/
voi_so_luong.json` của nhánh): `GET /gates` ⇒ `FINAL dat=True · 69.510/69.510 ô`,
`HD1_THANG dat=False · 5/23 kỳ đạt (kỳ đỏ 18/23)`, `chua_do_duoc=4`. `tep_do`
vắng ⇒ cả hai `dat=None`, `chua_do_duoc=6` (+2). Thẻ F03 KHÔNG tràn ở 390/360 px
(gate `scrollWidth==clientWidth`) ⇒ `man_f03.js` ⛔ cần sửa (`ISP §3`: "gấp/mở
NẾU CẦN"). Mỗi khẳng định ở đây đã **chứng minh ĐỎ bằng phá → chạy → cắn → trả**
(ghi trong `BG-117`).
"""
from __future__ import annotations

import contextlib
import glob
import http.client
import json
import os
import shutil
import subprocess
import threading
import time

import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.web import phuc_vu as pv
from fls.web.phuc_vu import lam_nguoi_phuc_vu
from tests.web import khung_node as kn
from tests.web.than_sinh import than_sinh

pytestmark = pytest.mark.pg

KHOA = "khoa-thu-cong-f03-bo-test-dai-hon-ba-muoi-hai-ky-tu-oke"
V = cua.bang_tuyen.TIEN_TO

# Gốc repo = …/fls/web/phuc_vu.py → …/fls/web → …/fls → gốc.
_GOC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(pv.__file__))))
REAL_TEP_DO = os.path.join(_GOC, "docs", "ITL", "_tools", "voi_so_luong.json")

# ⭐ Bộ tệp của F03 — ⛔ `TEP` (mặc định F02) của `khung_node`: `man_f03.js` chỉ
# cần `TP`·`TT`·`FLS` (`thanh_phan`·`trang_thai`·`goi_cua`). Thêm `man_f02.js` là
# nuôi màn KHÁC. `khung_node._chay` nạp các tệp này theo `pv.THU_MUC` (cwd).
TEP_F03 = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f03.js"]

_TEN_FINAL = "Luat Final tai hien tung o"          # `doc_bao_cao._TEN_FINAL`
_TEN_HD1 = "HD1 theo tháng"                          # đầu `doc_bao_cao._TEN_HD1`


@contextlib.contextmanager
def _may(tep_do):
    """Máy chủ thử CHẠY THẬT với `tep_do` cho trước — cổng `0` (HĐH chọn), chỉ
    đọc kho TEST. Trả `(may, the)`."""
    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA

    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    tok = the.dong_the({"sub": "ke.toan@apero.vn",
                        "exp": int(time.time()) + 600,
                        "vai": ["ke_toan"]}, KHOA.encode())
    m = cua.dung_may(
        mo, cong=0, tep_do=tep_do,
        phuc_vu_tep=lam_nguoi_phuc_vu(
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


def _gates(m, tok) -> dict:
    """`GET /gates` qua HTTP thật ⇒ envelope `{data, meta}`."""
    c = http.client.HTTPConnection(*m.server_address, timeout=10)
    try:
        c.request("GET", f"{V}/gates", headers={"Authorization": f"Bearer {tok}"})
        r = c.getresponse()
        than = r.read()
        assert r.status == 200, (r.status, than[:200])
        return json.loads(than)
    finally:
        c.close()


def _ve_f03(gates_data: dict) -> dict:
    """Render `man_f03.js` qua node headless, nuôi bằng envelope THẬT của tuyến.

    `_TRA['/gates']` đặt NGAY trong kịch bản (cùng ngữ cảnh `vm` của `khung_node`)
    ⇒ `FLS.doc('/gates')` (cửa giả của khung) trả đúng dữ liệu tuyến. Trả về các
    thẻ `.gate` (lớp + văn bản) và dòng tóm `.note`.
    """
    kb = (
        "_TRA['/gates'] = {data: %s};"
        "const o = document.createElement('div'); o.id = 'than-f03';"
        "document.body.appendChild(o);"
        "await F03.ve_cong(o);"
        "return {gates: [...document.querySelectorAll('.gate')].map("
        "  g => ({cls: g.className, txt: g.textContent})),"
        " note: (document.querySelector('.note') || {}).textContent || ''};"
        % json.dumps(gates_data, ensure_ascii=False)
    )
    return kn._chay(kb, tep=TEP_F03, vo="")


def _lop(g) -> list[str]:
    return (g["cls"] or "").split()


def _the(ve: dict, ten: str) -> dict:
    """ĐÚNG MỘT thẻ chứa tên cổng — `≥2` hay `0` là ĐỎ (Đ5: mẫu khớp phải `1`)."""
    hit = [g for g in ve["gates"] if ten in g["txt"]]
    assert len(hit) == 1, (ten, [g["txt"][:48] for g in ve["gates"]])
    return hit[0]


# ══ FG-F1 ═══════════════════════════════════════════════════════════════════
@kn.can_node
def test_FG_F1_tep_do_that_FINAL_dat_HD1_khong_dat_5_tren_23():
    """Mở F03 qua máy thật + `tep_do` THẬT: thẻ `FINAL` ĐẠT; `HD1_THANG` KHÔNG
    ĐẠT kèm `5/23`; **danh sách kỳ đỏ trong `ly_do` có mặt ĐẦY ĐỦ trên thẻ HD1**
    (FG-R2-01 · `KQ-119`); và **cả ba** số dòng tóm (`đạt`/`không đạt`/`chưa đo
    được`) = số tuyến trả (FG-R2-02 · `KQ-119` — Đ4: mỗi số một nhãn)."""
    with _may(REAL_TEP_DO) as (m, tok):
        env = _gates(m, tok)
    d = env["data"]
    g = {x["ma"]: x for x in d["cong"]}

    # ── ① vế TUYẾN đo (nền của phép so — Đ3: mẫu số ⛔ rỗng) ───────────────
    assert g["FINAL"]["dat"] is True, g["FINAL"]
    assert g["HD1_THANG"]["dat"] is False, g["HD1_THANG"]
    assert g["HD1_THANG"]["da_do"] == "5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh", g["HD1_THANG"]["da_do"]
    assert d["chua_do_duoc"] > 0, d           # tập 'chưa đo được' KHÔNG rỗng
    assert d["dat"] >= 1 and d["khong_dat"] >= 1, d

    # ── ② vế MÀN vẽ — đối chiếu bằng CHÍNH chuỗi tuyến trả ────────────────
    ve = _ve_f03(d)
    final = _the(ve, _TEN_FINAL)
    assert "pass" in _lop(final) and "unk" not in _lop(final), final["cls"]
    assert "ĐẠT" in final["txt"]
    assert g["FINAL"]["da_do"] in final["txt"], final["txt"]

    hd1 = _the(ve, _TEN_HD1)
    assert "fail" in _lop(hd1) and "unk" not in _lop(hd1), hd1["cls"]
    assert "KHÔNG ĐẠT" in hd1["txt"]
    assert g["HD1_THANG"]["da_do"] in hd1["txt"], hd1["txt"]   # "5/23 kỳ đạt"

    # ── FG-R2-01 (`KQ-119`): danh sách kỳ đỏ trong `ly_do` có mặt ĐẦY ĐỦ trên
    #    thẻ HD1 — so với CHÍNH chuỗi tuyến trả (⛔ hằng gõ tay). Trước R2, bài
    #    chỉ canh `da_do` ("5/23") chứ ⛔ `ly_do`, nên đột biến N9 (bỏ cả khối
    #    `ly_do` khỏi `_the_cong`) / N11 (`ly_do.slice(0,40)`) SỐNG — xanh trên
    #    một thẻ ⛔ còn lý do 23 kỳ nào. Đ3: tuyến phải trả `ly_do` KHÔNG rỗng
    #    trước đã, nếu không `"" in txt` là phép so xanh trên tập rỗng.
    ly_do = g["HD1_THANG"]["ly_do"]
    assert ly_do and len(ly_do) >= 50, ly_do                   # mẫu số ⛔ rỗng (Đ3)
    assert ly_do in hd1["txt"], (ly_do, hd1["txt"])

    # ── ③ ba số DÒNG TÓM = số TUYẾN trả (⛔ hằng số gõ tay). Đ4: dòng tóm ba số
    #    ⇒ canh CẢ BA. FG-R2-02 (`KQ-119`): số `đạt`/`không đạt` trước R2 ⛔ có
    #    bài ⇒ đột biến N10 (chip 'đạt' in `data.khong_dat`) SỐNG. `đạt` ≠
    #    `không đạt` ở nền (tuyến trả `dat=1 · khong_dat=2`) ⇒ N10 ⇒ ĐỎ.
    assert ("%d đạt" % d["dat"]) in ve["note"], ve["note"]
    assert ("%d không đạt" % d["khong_dat"]) in ve["note"], ve["note"]
    assert ("%d ⛔ chưa đo được" % d["chua_do_duoc"]) in ve["note"], ve["note"]


# ══ FG-F2 ═══════════════════════════════════════════════════════════════════
@kn.can_node
def test_FG_F2_tep_do_vang_hai_the_KHONG_DO_DUOC_khong_xanh(tmp_path):
    """Tệp đo VẮNG ⇒ `FINAL` + `HD1_THANG` thành hai thẻ lớp `.gate.unk` 'KHÔNG
    ĐO ĐƯỢC' — ⛔ xanh. Luật số 1: cổng ⛔ đo gì nguy hơn cổng đỏ."""
    vang = str(tmp_path / "khong-co-tep-do.json")
    assert not os.path.exists(vang)
    with _may(vang) as (m, tok):
        env = _gates(m, tok)
    d = env["data"]
    g = {x["ma"]: x for x in d["cong"]}

    assert g["FINAL"]["dat"] is None, g["FINAL"]
    assert g["HD1_THANG"]["dat"] is None, g["HD1_THANG"]

    ve = _ve_f03(d)
    for ten in (_TEN_FINAL, _TEN_HD1):
        card = _the(ve, ten)
        assert "unk" in _lop(card), (ten, card["cls"])
        assert "pass" not in _lop(card), (ten, card["cls"])   # ⛔ xanh
        assert "KHÔNG ĐO ĐƯỢC" in card["txt"], card["txt"]


# ══ FG-F3 — Chromium thật, pixel ở 390 px ═══════════════════════════════════
NODE = shutil.which("node")


def _pw_index() -> str | None:
    # FG-R1-03 (`KQ-118`): đường gõ cứng Linux có thể GHI ĐÈ bằng `FLS_PW_INDEX`
    #   (máy owner / bố cục khác). Đường ⛔ hợp lệ ⇒ rơi về dò mặc định — giữ
    #   nguyên chuỗi *thiếu ⇒ None ⇒ skip ⇒ `--duong-nen` ĐỎ* (Đ5).
    rieng = os.environ.get("FLS_PW_INDEX")
    if rieng and os.path.isfile(rieng):
        return rieng
    for p in ("/opt/node-tools/node_modules/playwright/index.js",):
        if os.path.isfile(p):
            return p
    if NODE:
        try:
            r = subprocess.run(
                [NODE, "-e", "process.stdout.write(require.resolve('playwright'))"],
                capture_output=True, text=True, timeout=20)
            if r.returncode == 0 and r.stdout.strip():
                return r.stdout.strip()
        except Exception:
            pass
    return None


def _chromium() -> str | None:
    # FG-R1-03 (`KQ-118`): ghi đè bằng `FLS_CHROMIUM`. ⛔ đặt hoặc đường ⛔ chạy
    #   được ⇒ rơi về glob mặc định — giữ chuỗi *thiếu ⇒ None ⇒ skip ⇒ ĐỎ* (Đ5).
    rieng = os.environ.get("FLS_CHROMIUM")
    if rieng and os.access(rieng, os.X_OK):
        return rieng
    hits = sorted(h for h in glob.glob(
        "/opt/pw-browsers/chromium-*/chrome-linux64/chrome") if os.access(h, os.X_OK))
    return hits[-1] if hits else None


PW = _pw_index()
CHROME = _chromium()
can_browser = pytest.mark.skipif(
    NODE is None or PW is None or CHROME is None,
    reason="⛔ thiếu node / playwright / Chromium ⇒ bỏ qua (pixel ở B7·UAT)")


def _do_tran(url: str, w: int) -> dict:
    """Mở F03 bằng Chromium thật ở bề rộng `w` px; trả `iw` (`innerWidth`) và các
    thẻ `.gate` kèm HAI vế của 'tràn': `over` (`scrollWidth > clientWidth` — nội
    dung vượt THẺ) và `r`/`l` (`getBoundingClientRect().right`/`.left` — mép thẻ
    so với KHUNG NHÌN). Đo của CHÍNH thẻ, ⛔ của cả trang."""
    mjs = (
        "import pkg from %(pw)s; const { chromium } = pkg;\n"
        "const b = await chromium.launch({ executablePath: %(cr)s,"
        " args: ['--no-sandbox'], headless: true });\n"
        "const pg = await b.newPage({ viewport: { width: %(w)d, height: 820 },"
        " deviceScaleFactor: 1 });\n"
        "await pg.goto(%(url)s);\n"
        "await pg.waitForSelector('#than-f03 .gate', { timeout: 15000 });\n"
        "const res = await pg.evaluate(() => ({\n"
        "  iw: window.innerWidth,\n"
        "  gates: [...document.querySelectorAll('#than-f03 .gate')].map(g => {\n"
        "    const rc = g.getBoundingClientRect();\n"
        "    return { cls: g.className, over: g.scrollWidth > g.clientWidth,\n"
        "      sw: g.scrollWidth, cw: g.clientWidth,\n"
        "      r: rc.right, l: rc.left, txt: (g.textContent || '') };\n"
        "  })\n"
        "}));\n"
        "console.log(JSON.stringify(res));\n"
        "await b.close();\n"
        % {"pw": json.dumps(PW), "cr": json.dumps(CHROME),
           "w": w, "url": json.dumps(url)}
    )
    r = subprocess.run([NODE, "--input-type=module", "-e", mjs],
                       capture_output=True, text=True, encoding="utf-8",
                       timeout=90)
    assert r.returncode == 0, f"⛔ node/chromium NO:\n{r.stdout}\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


@can_browser
def test_FG_F3_ly_do_23_ky_khong_tran_ngang_o_390px():
    """Lý do HD1 (18/23 kỳ đỏ, ~400 ký tự) ở bề rộng 390 px ⇒ thẻ HD1 ⛔ tràn
    ngang. ⭐ Đo CHÍNH thẻ, và bắt thẻ ấy THẬT mang chuỗi 23-kỳ (`5/23`) để phép
    so ⛔ xanh trên một thẻ rỗng (Đ3).

    ⭐ 'tràn ngang' có HAI vế (FG-R1-01 · `KQ-118`): ① nội dung ⛔ vượt THẺ
    (`scrollWidth ≤ clientWidth`) **và** ② thẻ ⛔ vượt KHUNG NHÌN
    (`getBoundingClientRect().right ≤ innerWidth`, `left ≥ 0`). Chỉ đo vế ① thì
    phép so XANH cả khi thẻ rộng hơn màn mà tự giãn (min-width ⇒ `sw == cw` mãi);
    đột biến M4 (`.gate{min-width:520px}`) sống đúng vì thế — phải đo cả hai vế
    (Đ5: đột biến phải phủ cả hai chiều của lớp lỗi)."""
    with _may(REAL_TEP_DO) as (m, tok):
        url = "http://%s:%d/" % m.server_address
        env = _gates(m, tok)          # CHÍNH chuỗi tuyến trả (⛔ hằng gõ tay)
        res = _do_tran(url, 390)
    g_hd1 = {x["ma"]: x for x in env["data"]["cong"]}["HD1_THANG"]

    hd1 = [x for x in res["gates"] if _TEN_HD1 in x["txt"]]
    assert len(hd1) == 1, [x["txt"][:48] for x in res["gates"]]
    assert "5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh" in hd1[0]["txt"], hd1[0]["txt"][:120]        # tập ⛔ rỗng
    # ── FG-R2-01 (`KQ-119`): thẻ HD1 THẬT mang danh sách kỳ đỏ (`ly_do` ĐẦY ĐỦ)
    #    TRƯỚC khi đo tràn — ⛔ đo tràn trên một thẻ đã cụt lý do (Đ3). Bài tên
    #    "lý do 23 kỳ ⛔ tràn" phải khẳng định lý do 23 kỳ CÓ trên thẻ, so với
    #    CHÍNH chuỗi `GET /gates` trả. N9/N11 (xem FG-F1) ⇒ ĐỎ cả ở đây.
    ly_do = g_hd1["ly_do"]
    assert ly_do and len(ly_do) >= 50, ly_do
    assert ly_do in hd1[0]["txt"], (ly_do, hd1[0]["txt"][:200])
    # ── vế ①: nội dung ⛔ vượt THẺ ────────────────────────────────────────
    assert hd1[0]["over"] is False, (
        "thẻ HD1 TRÀN ngang ở 390 px: sw=%(sw)d > cw=%(cw)d" % hd1[0])
    # ── vế ②: thẻ ⛔ vượt KHUNG NHÌN (FG-R1-01) ───────────────────────────
    assert hd1[0]["r"] <= res["iw"], (
        "thẻ HD1 vượt mép PHẢI khung nhìn ở 390 px: right=%.1f > innerWidth=%d"
        % (hd1[0]["r"], res["iw"]))
    assert hd1[0]["l"] >= 0, (
        "thẻ HD1 tràn mép TRÁI khung nhìn ở 390 px: left=%.1f < 0" % hd1[0]["l"])
