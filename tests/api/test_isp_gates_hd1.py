"""ISP 3.1.2 · Step 7 · CG1 (`WO-101`) — cổng HD1 vào `GET /gates`.

Ô chờ `FINAL` *(trước CG1: luôn `dat=None` — "chạy ngoài kho trên ảnh chụp sổ gốc")* thành **số đo**
đọc từ tệp đo `voi_so_luong.json` (H2 · `tools/do_voi_so_luong.py`), và thêm cổng `HD1_THANG`
*(AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10)*.

⭐ Đường dẫn tệp đo **TRUYỀN VÀO** — y khuôn kết nối kho (hợp đồng tầng 7 của `.importlinter`):
`tools/chay_cua.py` → `cua.dung_may(tep_do=…)` → `YeuCau.tep_do` → `doc_bao_cao.doc_cong(…, tep_do)`.
⛔ Gõ cứng ở `fls/`: bộ bài này truyền **ba** đường khác nhau *(tệp thật · tệp vắng · tệp bị phá ở
`tmp_path`)* qua **cùng** tuyến — một đường gõ cứng sẽ trả cùng một đáp án cho cả ba ⇒ ĐỎ.

⛔⛔ Bài qua **tuyến thật** *(HTTP + thẻ + bảng tuyến + vỏ `{data,error,meta}`)*, ⛔ gọi hàm xử lý —
cùng lý do với `test_cua_pg.py`: cái phải chứng minh là *"số ra được qua HTTP"*. Phần ca phá tệp đo
gọi thẳng `bc.doc_cong_tep_do` *(hàm thuần, ⛔ cần kho)* cho nhanh; MỘT ca phá đi lại qua tuyến thật
để chứng minh tuyến đọc ĐÚNG tệp được truyền (`CG1-B4`).

`MONG` khai TRƯỚC, độc lập với mã đang kiểm (Đ5) — nguồn ghi cạnh từng số; mỗi số nói NÓ ĐẾM GÌ (Đ4).
"""
from __future__ import annotations

import contextlib
import copy
import http.client
import json
import os
import re
import threading
import time
from pathlib import Path

import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import doc_bao_cao as bc

GOC = Path(__file__).resolve().parents[2]
# ⭐ Tệp đo THẬT = ảnh tĩnh đã commit (sinh máy: `python tools/do_voi_so_luong.py --ghi`). Bài chọn
#    đường ⇒ ⛔ `fls/` chọn.
TEP_DO_THAT = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
# Hiện vật DT1a (`tools/phan_loai_dong_thieu.py --ghi`) — nguồn THỨ HAI của `MONG_KY_DO` (Đ2).
TEP_DT1A = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"

KHOA = "khoa-thu-cong-hd1-cg1-bo-test-dai-hon-ba-muoi-hai-ky-tu"
V = cua.bang_tuyen.TIEN_TO

# ══ MONG — khai TRƯỚC (Đ5) ═══════════════════════════════════════════════════════════════════
# `FINAL` · ISP Step 7 §2 "69.510/69.510 ô (ĐẠT)" — ĐO LẠI 16/11 (WO-101: "đo lại, ⛔ tin") bằng
#   script độc lập đọc thẳng `tests/fixture/itl_ledge_adjustment.json` + `final_rule.tinh_final`
#   + `tu_soi.soi_mot_dong` *(⛔ qua `tools/do_voi_so_luong.py`)*: 69.510/69.510 = ô của 7 khối ×
#   9.930 dòng GIỮ sau tự soi (9.967 dòng sổ − 37 dòng tự soi loại, cả 37 ở 2026-07; ô lỗi Sheets 0).
#   Cùng phép ấy trên MỌI dòng: 69.706/69.769 *(= KQ-092 đo (b))* ⇒ mẫu số KHÁC ⇒ nhãn bắt buộc (Đ4).
MONG_FINAL_DA_DO_DAU = "69.510/69.510 ô"
MONG_FINAL_NHAN_DEM = "7 khối × 9.930 dòng"
MONG_FINAL_O_SO = "69.769 ô"                      # 9.967 dòng × 7 khối — mẫu số "CÓ" của AP Figure 2.2
MONG_FINAL_TU_SOI = "37 dòng tự soi loại"
# `HD1_THANG` · ISP Step 7 §2 "'5/23 kỳ đạt' (KHÔNG ĐẠT)". Kỳ ĐỎ + số dòng thiếu mỗi kỳ:
#   `MONG["phan_bo_ky_thieu"]` của DT1a (`tools/phan_loai_dong_thieu.py:128`, BG-081 §Bảng đếm) —
#   18 kỳ, Σ 122; xếp theo thời gian. Bài `test_MONG_ky_do_TRUNG_hien_vat_DT1a` so nguồn thứ hai.
# ⛔ I1-R1-01: mẫu số in RÕ — 23 kỳ đo được đủ hai vế · 26 kỳ có ảnh (`tu_sinh`)
MONG_HD1_DA_DO = "5 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh"
MONG_KY_DAT = ("2024-10", "2024-11", "2024-12", "2025-03", "2025-04")
MONG_KY_DO = (
    ("2025-01", 1), ("2025-02", 2), ("2025-05", 1), ("2025-06", 3), ("2025-07", 4),
    ("2025-08", 4), ("2025-09", 4), ("2025-10", 9), ("2025-11", 14), ("2025-12", 5),
    ("2026-01", 4), ("2026-02", 5), ("2026-03", 5), ("2026-04", 8), ("2026-05", 5),
    ("2026-06", 12), ("2026-07", 23), ("2026-08", 13),
)
# Ngày ảnh — ISP Step 7 §3 "số là của ảnh 26/08 — `ly_do` ghi ngày ảnh".
MONG_NGAY_ANH = "2026-08-26"
# Bốn cổng LUÔN `dat=None` sau CG1 (`DIF_BANK` · `VI` · `DONG_BO` · `BON_DUONG`) — luật `doc_cong`:
#   ⛔ bao giờ trả danh sách toàn xanh. `FINAL` rời nhóm này CHỈ khi tệp đo đọc được.
MONG_LUON_CHUA_DO = {"DIF_BANK", "VI", "DONG_BO", "BON_DUONG"}

# Mẫu cặp "kỳ: số dòng thiếu" trong `ly_do` — `yyyy-mm` + `:` ⇒ ⛔ khớp ngày ảnh `2026-08-26`.
_CAP_KY = re.compile(r"(\d{4}-\d{2}): (\d+)")


# ── máy thật ─────────────────────────────────────────────────────────────────────────────────
@contextlib.contextmanager
def _may(tep_do):
    """Máy THẬT trên cổng tuỳ hệ điều hành, kết nối CHỈ ĐỌC vào kho TEST, tệp đo = `tep_do`."""
    @contextlib.contextmanager
    def mo():
        conn = noi_chi_doc(dsn_test())
        try:
            yield conn
        finally:
            conn.close()

    cu = os.environ.get(the.BIEN_KHOA)
    os.environ[the.BIEN_KHOA] = KHOA
    try:
        m = cua.dung_may(mo, cong=0, tep_do=tep_do)
    finally:
        # khoá được đọc MỘT lần lúc dựng máy (`the.khoa()`) ⇒ trả biến môi trường ngay
        if cu is None:
            os.environ.pop(the.BIEN_KHOA, None)
        else:
            os.environ[the.BIEN_KHOA] = cu
    t = threading.Thread(target=m.serve_forever, daemon=True)
    t.start()
    try:
        yield m
    finally:
        m.shutdown()
        m.server_close()


def _gates(tep_do) -> dict:
    """`GET /gates` qua HTTP thật ⇒ `data` (đòi 200 + vỏ đủ ba phần)."""
    with _may(tep_do) as m:
        c = http.client.HTTPConnection(*m.server_address, timeout=30)
        try:
            the_song = the.dong_the({"sub": "ke.toan@apero.vn", "exp": int(time.time()) + 300,
                                     "vai": ["ke_toan"]}, KHOA.encode())
            c.request("GET", f"{V}/gates", headers={"Authorization": f"Bearer {the_song}"})
            r = c.getresponse()
            than = json.loads(r.read())
        finally:
            c.close()
    assert r.status == 200, than
    assert set(than) == {"data", "error", "meta"} and than["error"] is None, than
    return than["data"]


def _theo_ma(data: dict) -> dict[str, dict]:
    ra = {c["ma"]: c for c in data["cong"]}
    assert len(ra) == len(data["cong"]), "mã cổng trùng"
    return ra


@pytest.fixture(scope="module")
def gates_that():
    return _gates(TEP_DO_THAT)


# ══ CG1-B1 · tệp đo thật ⇒ FINAL ĐẠT · HD1_THANG KHÔNG ĐẠT ════════════════════════════════════
@pytest.mark.pg
def test_CG1_B1_FINAL_DAT_69510_tren_69510_o_va_noi_DEM_O_GI(gates_that):
    """`FINAL` dat true · `da_do` = số ô đo + NHÃN đếm gì (khối × dòng), ngay chỗ in (Đ4)."""
    f = _theo_ma(gates_that)["FINAL"]
    assert f["dat"] is True and f["nhan"] == "DAT", f
    assert f["da_do"].startswith(MONG_FINAL_DA_DO_DAU), f["da_do"]
    assert MONG_FINAL_NHAN_DEM in f["da_do"], f["da_do"]
    # mẫu số bị bỏ phải NÓI RA: ô sổ có 69.769 · 37 dòng tự soi loại ⛔ vào mẫu số
    assert MONG_FINAL_O_SO in f["ly_do"] and MONG_FINAL_TU_SOI in f["ly_do"], f["ly_do"]


@pytest.mark.pg
def test_CG1_B1_HD1_THANG_KHONG_DAT_5_tren_23_ky_va_liet_ke_18_ky_do(gates_that):
    """`HD1_THANG` dat false · `da_do '5/23 kỳ đạt'` · `ly_do` liệt kê ĐỦ 18 kỳ đỏ + số dòng thiếu."""
    h = _theo_ma(gates_that)["HD1_THANG"]
    assert h["dat"] is False and h["nhan"] == "KHONG DAT", h
    assert h["da_do"] == MONG_HD1_DA_DO, h["da_do"]
    cap = tuple((k, int(n)) for k, n in _CAP_KY.findall(h["ly_do"]))
    assert cap == MONG_KY_DO, (cap, h["ly_do"])
    # ⛔ kỳ ĐẠT nào bị kể là đỏ
    assert not {k for k, _ in cap} & set(MONG_KY_DAT)


@pytest.mark.pg
def test_CG1_B1_ly_do_ghi_NGAY_ANH_o_ca_hai_cong(gates_that):
    """ISP §3 giới hạn: *"số là của ảnh 26/08 — `ly_do` ghi ngày ảnh"* — ⛔ để số ảnh trông như số sống."""
    c = _theo_ma(gates_that)
    for ma in ("FINAL", "HD1_THANG"):
        assert MONG_NGAY_ANH in c[ma]["ly_do"], (ma, c[ma]["ly_do"])


@pytest.mark.pg
def test_CG1_B1_ba_con_so_tom_DEM_DUNG_danh_sach_cong(gates_that):
    """`dat` · `khong_dat` · `chua_do_duoc` của tuyến = đếm lại trên chính danh sách cổng."""
    d = gates_that
    dat = [c["dat"] for c in d["cong"]]
    assert (d["dat"], d["khong_dat"], d["chua_do_duoc"]) == (
        dat.count(True), dat.count(False), sum(1 for x in dat if x is None))
    c = _theo_ma(d)
    assert {m for m in MONG_LUON_CHUA_DO if c[m]["dat"] is None} == MONG_LUON_CHUA_DO


# ══ CG1-B2 · tệp đo VẮNG ⇒ cả hai null · chua_do_duoc tăng ĐÚNG 2 · ⛔ 200 toàn xanh ═══════════
@pytest.mark.pg
@pytest.mark.parametrize("ca", ["khong_truyen", "duong_khong_co_tep"])
def test_CG1_B2_tep_do_VANG_hai_cong_null_chua_do_duoc_tang_DUNG_2(gates_that, tmp_path, ca):
    tep = None if ca == "khong_truyen" else tmp_path / "voi_so_luong.json"     # ⛔ tạo tệp
    vang = _gates(tep)
    a, b = _theo_ma(gates_that), _theo_ma(vang)
    for ma in ("FINAL", "HD1_THANG"):
        assert b[ma]["dat"] is None and b[ma]["nhan"] == "CHUA DO DUOC", b[ma]
        assert "vắng" in b[ma]["ly_do"] or "⛔ được truyền" in b[ma]["ly_do"], b[ma]["ly_do"]
    assert vang["chua_do_duoc"] - gates_that["chua_do_duoc"] == 2, (vang, gates_that)
    # "tăng đúng 2" phải là ĐÚNG HAI cổng ấy — ⛔ một cổng khác bù trừ
    null_a = {m for m, x in a.items() if x["dat"] is None}
    null_b = {m for m, x in b.items() if x["dat"] is None}
    assert null_b - null_a == {"FINAL", "HD1_THANG"} and null_a <= null_b
    assert {m: x["dat"] for m, x in a.items() if m not in ("FINAL", "HD1_THANG")} == \
           {m: x["dat"] for m, x in b.items() if m not in ("FINAL", "HD1_THANG")}
    # ⛔ 200 toàn xanh (Đ5)
    assert vang["dat"] < len(vang["cong"]) and vang["chua_do_duoc"] >= len(MONG_LUON_CHUA_DO) + 2


@pytest.mark.pg
def test_CG1_B2_ly_do_tep_vang_KHONG_lo_duong_dan_may(tmp_path):
    """Lý do đi ra HTTP ⇒ chỉ TÊN tệp, ⛔ đường dẫn tuyệt đối (một đường dẫn là bản đồ máy —
    cùng lý do `cua._di` ⛔ trả vết ngăn xếp)."""
    tep = tmp_path / "thu_muc_rieng_cua_may" / "voi_so_luong.json"
    c = _theo_ma(_gates(tep))
    for ma in ("FINAL", "HD1_THANG"):
        assert "voi_so_luong.json" in c[ma]["ly_do"], c[ma]["ly_do"]
        assert "thu_muc_rieng_cua_may" not in c[ma]["ly_do"] and str(tmp_path) not in c[ma]["ly_do"]


# ══ CG1-B4 · cổng ĐỎ được — và đỏ QUA TUYẾN THẬT với tệp được truyền vào ════════════════════════
def _tep_pha(tmp_path: Path, pha) -> Path:
    d = json.loads(TEP_DO_THAT.read_text(encoding="utf-8"))
    pha(d)
    p = tmp_path / "voi_so_luong.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


def _moi_ky_dat(d: dict) -> None:
    h = d["dat_hd1"]
    for k in h["theo_ky"]:
        h["theo_ky"][k]["dat"] = True
    h["ky_dat"] = sorted(h["theo_ky"])
    h["so_ky_dat"] = len(h["ky_dat"])
    # I1-R1-01: ảnh `tu_sinh` chỉ phủ đúng 23 kỳ của cổng ⇒ mọi kỳ ĐO ĐƯỢC (còn 26 ⇒ `dat=None`)
    for k in ("2026-09", "2026-10", "2026-11"):
        d["tu_sinh"]["theo_ky"].pop(k)
    d["tu_sinh"]["so_ky_co_anh"] = len(d["tu_sinh"]["theo_ky"])


@pytest.mark.pg
def test_CG1_B4_tep_PHA_qua_tuyen_that_HAI_CHIEU(tmp_path):
    """Một tệp bị phá ở `tmp_path`, truyền qua `dung_may` ⇒ tuyến đọc ĐÚNG tệp ấy:
    FINAL lệch 1 ô ⇒ ĐỎ; mọi kỳ đạt ⇒ HD1_THANG ĐẠT `23/23 kỳ đạt` (chiều ngược — Đ5 hai chiều)."""
    def pha(d):
        d["tong"]["o_parity_khop"] -= 1
        _moi_ky_dat(d)
    c = _theo_ma(_gates(_tep_pha(tmp_path, pha)))
    assert c["FINAL"]["dat"] is False and "1/69.510 ô LỆCH" in c["FINAL"]["ly_do"], c["FINAL"]
    assert c["HD1_THANG"]["dat"] is True and c["HD1_THANG"]["da_do"] == "23 kỳ đạt / 23 kỳ đo được / 23 kỳ có ảnh", c["HD1_THANG"]


# ══ hàm thuần `doc_cong_tep_do` — ca phá tệp đo (⛔ cần kho) ════════════════════════════════════
def _hai(tep) -> dict[str, bc.Cong]:
    ra = {c.ma: c for c in bc.doc_cong_tep_do(tep)}
    assert set(ra) == {"FINAL", "HD1_THANG"}, set(ra)
    return ra


def test_ham_thuan_TEP_THAT_cung_dap_an_voi_tuyen():
    c = _hai(TEP_DO_THAT)
    assert c["FINAL"].dat is True and c["FINAL"].da_do.startswith(MONG_FINAL_DA_DO_DAU)
    assert c["HD1_THANG"].dat is False and c["HD1_THANG"].da_do == MONG_HD1_DA_DO


@pytest.mark.parametrize("noi_dung", [b"{ khong phai json", b"[1, 2, 3]", b"", b"\xff\xfe\x00"])
def test_tep_HONG_ca_hai_None_va_KHONG_no(tmp_path, noi_dung):
    p = tmp_path / "voi_so_luong.json"
    p.write_bytes(noi_dung)
    for c in _hai(p).values():
        assert c.dat is None and "voi_so_luong.json" in c.ly_do, c


def test_FINAL_lech_MOT_o_thi_DO_va_noi_so_o_lech(tmp_path):
    """Chiều ĐỎ của `FINAL` trên hàm thuần (chiều qua tuyến: `CG1-B4`) — lệch 1 ô là đủ."""
    def pha(d):
        d["tong"]["o_parity_khop"] = d["tong"]["o_parity"] - 1
    c = _hai(_tep_pha(tmp_path, pha))["FINAL"]
    assert c.dat is False and c.ly_do.startswith("1/69.510 ô LỆCH"), c
    assert c.da_do.startswith("69.509/69.510 ô"), c.da_do


def test_FINAL_mau_so_0_o_la_CHUA_DO_DUOC_khong_phai_100(tmp_path):
    """Đ3: `0/0` ⛔ 100 % — tập rỗng là KẾT QUẢ, ⛔ nền."""
    def pha(d):
        d["tong"]["o_parity"] = d["tong"]["o_parity_khop"] = 0
    c = _hai(_tep_pha(tmp_path, pha))["FINAL"]
    assert c.dat is None and "0 ô" in c.ly_do, c


@pytest.mark.parametrize("ten,pha", [
    ("khop_lon_hon_mau_so", lambda d: d["tong"].__setitem__("o_parity_khop", d["tong"]["o_parity"] + 1)),
    ("o_nhieu_hon_7_khoi_x_dong_giu", lambda d: d["tong"].__setitem__("o_parity", d["tong"]["o_parity"] + 7_000)),
    ("dem_la_bool", lambda d: d["tong"].__setitem__("o_parity_khop", True)),
    ("dem_la_chuoi", lambda d: d["tong"].__setitem__("o_parity", "69510")),
    ("dem_am", lambda d: d["tong"].__setitem__("loai_tu_soi", -1)),
    ("thieu_khoi_tong", lambda d: d.pop("tong")),
])
def test_FINAL_tep_TU_MAU_THUAN_hay_SAI_KIEU_la_CHUA_DO_DUOC(tmp_path, ten, pha):
    c = _hai(_tep_pha(tmp_path, pha))["FINAL"]
    assert c.dat is None and c.ly_do, (ten, c)


def test_HD1_mau_so_0_ky_la_CHUA_DO_DUOC(tmp_path):
    def pha(d):
        h = d["dat_hd1"]
        h["mau_so"]["so_ky"] = h["so_ky_dat"] = 0
        h["theo_ky"], h["ky_dat"] = {}, []
    c = _hai(_tep_pha(tmp_path, pha))["HD1_THANG"]
    assert c.dat is None and "0 kỳ" in c.ly_do, c


@pytest.mark.parametrize("ten,pha", [
    ("so_ky_dat_lech_ky_dat", lambda d: d["dat_hd1"].__setitem__("so_ky_dat", 6)),
    ("ky_dat_lech_theo_ky", lambda d: d["dat_hd1"]["theo_ky"]["2025-01"].__setitem__("dat", True)),
    ("mau_so_lech_so_ky", lambda d: d["dat_hd1"]["mau_so"].__setitem__("so_ky", 24)),
    ("ky_dat_trung", lambda d: d["dat_hd1"].__setitem__("ky_dat", d["dat_hd1"]["ky_dat"][:4] + ["2024-10"])),
    ("dat_khong_phai_bool", lambda d: d["dat_hd1"]["theo_ky"]["2025-01"].__setitem__("dat", 0)),
    ("thieu_am", lambda d: d["dat_hd1"]["theo_ky"]["2025-01"].__setitem__("thieu", -1)),
    ("thieu_khoi_dat_hd1", lambda d: d.pop("dat_hd1")),
])
def test_HD1_tep_TU_MAU_THUAN_hay_SAI_KIEU_la_CHUA_DO_DUOC_ma_FINAL_van_do(tmp_path, ten, pha):
    """CG1 ⛔ tự tính lại luật kỳ (WO-101) — nhưng một tệp tự mâu thuẫn thì ⛔ được ra số. Và
    hỏng ở khối `dat_hd1` ⛔ được kéo `FINAL` (khối `tong`) theo: hai cổng, hai khối, độc lập."""
    c = _hai(_tep_pha(tmp_path, pha))
    assert c["HD1_THANG"].dat is None and c["HD1_THANG"].ly_do, (ten, c["HD1_THANG"])
    assert c["FINAL"].dat is True, (ten, c["FINAL"])


def test_HD1_ky_do_co_0_dong_thieu_VAN_duoc_ke_ra(tmp_path):
    """Sau `H2-R1-01` một kỳ có thể đỏ vì vế ô dù 0 dòng thiếu ⇒ vẫn phải có tên trong `ly_do`."""
    def pha(d):
        h = d["dat_hd1"]
        h["theo_ky"]["2024-10"]["dat"] = False
        h["ky_dat"] = [k for k in h["ky_dat"] if k != "2024-10"]
        h["so_ky_dat"] = len(h["ky_dat"])
    c = _hai(_tep_pha(tmp_path, pha))["HD1_THANG"]
    assert c.dat is False and c.da_do == "4 kỳ đạt / 23 kỳ đo được / 26 kỳ có ảnh", c
    cap = dict((k, int(n)) for k, n in _CAP_KY.findall(c.ly_do))
    assert cap.get("2024-10") == 0 and len(cap) == 19, c.ly_do


def test_HD1_thieu_NGAY_ANH_thi_noi_ra_khong_im_lang(tmp_path):
    c = _hai(_tep_pha(tmp_path, lambda d: d["nguon"].pop("so_dong_bang")))
    for x in c.values():
        assert "ngày ảnh" in x.ly_do and MONG_NGAY_ANH not in x.ly_do, x


# ══ rìa · `tools/chay_cua.py` truyền ĐÚNG tệp ══════════════════════════════════════════════════
def test_chay_cua_MAC_DINH_tro_DUNG_tep_do_that():
    """Mặc định nằm ở RÌA (`tools/chay_cua.py`, cùng chỗ chuỗi kết nối kho) — ⛔ trong `fls/`. Và nó
    phải trỏ tệp CÓ THẬT: trỏ sai thì cửa thật im lặng ra hai cổng "CHƯA ĐO ĐƯỢC" — an toàn (⛔ xanh),
    nhưng `FINAL` sẽ ⛔ bao giờ lên màn F03 mà ⛔ ai biết vì sao."""
    from tools import chay_cua

    assert TEP_DO_THAT.is_file()
    assert Path(chay_cua.TEP_DO_MAC_DINH).resolve() == TEP_DO_THAT.resolve()


# ══ Đ2 · MONG của bài ↔ nguồn thứ hai ══════════════════════════════════════════════════════════
def test_MONG_ky_do_TRUNG_hien_vat_DT1a():
    """`MONG_KY_DO` (gõ từ `MONG` DT1a) = hiện vật DT1a `phan_loai_dong_thieu.json` (sinh máy);
    và 5 kỳ đạt = đúng 5 kỳ ⛔ có dòng thiếu (sổ lý do còn RỖNG). Mẫu số ⛔ rỗng (Đ3): 23 kỳ."""
    dt = json.loads(TEP_DT1A.read_text(encoding="utf-8"))["theo_ky"]
    assert len(dt) == 23
    assert tuple((k, v["thieu"]) for k, v in sorted(dt.items()) if v["thieu"]) == MONG_KY_DO
    assert tuple(k for k, v in sorted(dt.items()) if not v["thieu"]) == MONG_KY_DAT
    assert sum(n for _, n in MONG_KY_DO) == 122
