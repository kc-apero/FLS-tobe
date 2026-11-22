"""ISP 3.1.2 · Step 30 · CG2 (`WO-208`) — cổng HD2 theo gói vào `GET /gates`.

Khuôn `test_isp_gates_hd1.py` (CG1): bài qua TUYẾN THẬT (HTTP + thẻ + vỏ), tệp đo TRUYỀN VÀO
(`dung_may(tep_hd2=…)`) — ba đường khác nhau *(tệp thật · tệp vắng · tệp phá ở `tmp_path`)*.

⭐ Cổng = HỢP của gói KHAI SẴN mức cha (`WP-C2` · `WP-C3` · `WP-C4` · `WP-C5`) và gói con CÓ trong
tệp (`WP-C3a` · `WP-C3b`; về sau `WP-C3c` · `WP-C4a`…). Cha `dat` = gộp con (con `false` ⇒ `false`;
còn con `null` ⇒ `null`; còn lại `true`). Gói con mới tự hiện — ⛔ sửa mã (AC-4).
Mỗi số nói NÓ ĐẾM GÌ (Đ4): cổng gói lá đếm Ô đáp án; cổng cha đếm GÓI CON (+ Σ ô).
`MONG` khai TRƯỚC, nguồn thứ hai = chính `hd2_cong.json` đọc ngoài mã (Đ2).
"""
from __future__ import annotations

import contextlib
import copy
import http.client
import json
import re
import os
import threading
import time
from pathlib import Path

import pytest

from fls.api import cua, the
from fls.db.kho import dsn_test, noi_chi_doc
from fls.repo import doc_bao_cao as bc

GOC = Path(__file__).resolve().parents[2]
TEP_HD2_THAT = GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"
KHOA = "khoa-thu-cong-hd2-cg2-bo-test-dai-hon-ba-muoi-hai-ky-tu"
V = cua.bang_tuyen.TIEN_TO

# ══ MONG — khai TRƯỚC (Đ5) ═══════════════════════════════════════════════════════════════════
# Tệp thật (H4 · H5 · H6, đo 18/11): WP-C2 (cấp cao nhất) + WP-C3a + WP-C3b, cả ba `dat=true`.
# Gộp H9 (19/11): + WP-C4a (`tong_o`/`khop` = 420/420 ô so, 196 ô ⛔ so được nằm NGOÀI mẫu số).
# Gộp H10 (19/11, `H10-R2-01`): + WP-C4b (`tong_o`/`khop` = 1981/1981 ô so, 945 ô ⛔ so được nằm NGOÀI mẫu số).
# Gộp H7 (19/11, WO-245): + WP-C3c (`tong_o` 888 = GL HR 240 + CFA3 648; `khop` 835 = ô khớp THẬT; 53 lệch có chủ đích).
# Gộp H11 (19/11, `WO-233`; sửa `KQ-236` H11-R1-02): + WP-C4c (`khop` 19.591 = ô khớp THẬT · `tong_o` 19.894 = ô so ·
#   303 lệch nguồn CÓ TÊN (52 OMC + 251 SC) ở `lech_co_chu_dich` · 8.611 ô đáp án RỖNG đếm ở `o_trong_dap_an`;
#   ô ⛔ so được P chữ ngoài mẫu số).
# Gộp H8 (22/11, WO-277): + WP-C3d (`tong_o` 1.289.415 = 6 tab PLA × 12 khối; `khop` 1.287.624 = ô khớp THẬT;
#   1.791 lệch có chủ đích — 8 ô 416 `GAC` thiếu `CXA` + 1.783 ô AS-IS 72 cột 2024 trước `CA` của 416).
# H12 (22/11, WO-291): + WP-C5a (`tong_o` 45.674 = ô ATL so; `khop` 39.843 = ô khớp THẬT; 5.831 lệch có chủ đích —
#   AS-IS BẬT phân bổ 2025 4.932 + 72 cột 2024 lan từ H8 675 + 224 ô từng ô: −0,5 tay GROUP · NB by LE SGO1).
# ⭐ vòng sửa R1 H12 (KQ-293, 22/11): cổng đo ở cờ BẬT ký 2025 ⇒ `khop` 40.556 · 5.118 lệch có chủ đích (lớp gán bằng phép đo).
# H13 (22/11, WO-307): + WP-C5b (`tong_o` 4.102 = ô DÒNG PL so; `khop` 3.179 = khớp THẬT 884 + 0=0 2.295; 923 lệch có
#   chủ đích — MỌI ô thừa kế lớp từ lá C5a; lệch FLS 0).
# 4 cha khai sẵn + 9 con có trong tệp = 13 cổng. WP-C4 (cha, 3 con) ⇒ true; WP-C5 (cha, 2 con C5a · C5b) ⇒ true.
MONG_THAT = {
    "HD2_WP_C2": True, "HD2_WP_C3": True, "HD2_WP_C3A": True, "HD2_WP_C3B": True, "HD2_WP_C3C": True, "HD2_WP_C3D": True,
    "HD2_WP_C4": True, "HD2_WP_C4A": True, "HD2_WP_C4B": True, "HD2_WP_C4C": True, "HD2_WP_C5": True, "HD2_WP_C5A": True,
    "HD2_WP_C5B": True,
}
MONG_CHA_KHAI_SAN = ("HD2_WP_C2", "HD2_WP_C3", "HD2_WP_C4", "HD2_WP_C5")
MONG_O_C2 = "63016/63016 ô"          # `hd2_cong.json` WP-C2 khop/tong_o (BM…BT × 7877 dòng)
# ⭐ KQ-231 (Đ4): tử số = ô KHỚP đáp án THẬT; mẫu số 205.175 gồm 35 ô lệch có chủ đích (ITE) khai riêng
MONG_O_C3A = "205140/205175 ô"
MONG_O_C3B = "11543/11585 ô"
MONG_O_C3C = "835/888 ô"             # WP-C3c khop/tong_o (ô khớp THẬT; + 53 lệch có chủ đích — kỳ đáp án ≠ nguồn)
MONG_O_C3D = "1287624/1289415 ô"     # WP-C3d khop/tong_o (ô khớp THẬT; + 1791 lệch có chủ đích — AS-IS 416)
MONG_O_C4B = "1981/1981 ô"           # `hd2_cong.json` WP-C4b khop/tong_o (209 Vendor-tháng × 14 − 945 ô P chữ)
# ⭐ KQ-236 H11-R1-02: tử số = ô KHỚP THẬT; mẫu số 19.894 gồm 303 lệch nguồn CÓ TÊN (52 OMC + 251 SC) khai riêng
MONG_O_C4C = "19591/19894 ô đáp án khớp + 303 lệch có chủ đích"
MONG_O_C5A = "40556/45674 ô"         # WP-C5a khop/tong_o — cờ BẬT ký 2025 (vòng sửa R1 KQ-293); + 5118 lệch có chủ đích (lớp đo)
MONG_O_C5B = "3179/4102 ô"          # WP-C5b khop/tong_o — dòng PL IX.PL trên ATL của FLS; + 923 lệch thừa kế lớp từ lá
MONG_O_C4A = "420/420 ô"             # `hd2_cong.json` WP-C4a khop/tong_o (44 Vendor-tháng × 14 − 196 ô P chữ)


# ── máy thật ─────────────────────────────────────────────────────────────────────────────────
@contextlib.contextmanager
def _may(tep_hd2):
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
        m = cua.dung_may(mo, cong=0, tep_hd2=tep_hd2)
    finally:
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


def _gates(tep_hd2) -> dict:
    with _may(tep_hd2) as m:
        c = http.client.HTTPConnection(*m.server_address, timeout=30)
        try:
            tk = the.dong_the({"sub": "ke.toan@apero.vn", "exp": int(time.time()) + 300,
                               "vai": ["ke_toan"]}, KHOA.encode())
            c.request("GET", f"{V}/gates", headers={"Authorization": f"Bearer {tk}"})
            r = c.getresponse()
            than = json.loads(r.read())
        finally:
            c.close()
    assert r.status == 200, than
    assert set(than) == {"data", "error", "meta"} and than["error"] is None, than
    return than["data"]


def _hd2(data: dict) -> dict[str, dict]:
    ra = {c["ma"]: c for c in data["cong"] if c["ma"].startswith("HD2_")}
    return ra


def _that() -> dict:
    return json.loads(TEP_HD2_THAT.read_text(encoding="utf-8"))


def _tep(tmp_path: Path, pha) -> Path:
    d = _that()
    pha(d)
    p = tmp_path / "hd2_cong.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


def _dat(c) -> dict:
    return {x.ma: x.dat for x in c}


# ══ CG2-R2-03 · HỢP ĐỒNG KHỐI GÓI (H4): MỌI khối gói của tệp THẬT khai `tong_o` + `khop` ═══════════════
# Lỗi đã xảy ra: gộp H9 (`WP-C4a` chỉ có `o_so`/`lech`) ⇒ cổng `HD2_WP_C4A` = null (⛔ tin mù) mà không
# bài nào quét TỆP. Quét theo khoá `WP-C\d+[a-z]*` + khối gốc; Đ3: tập ⛔ rỗng (≥ 4 khối).
def test_CG2_R2_03_MOI_khoi_goi_cua_tep_THAT_khai_tong_o_va_khop():
    d = _that()
    khoi = {"WP-C2": d, **{k: v for k, v in d.items() if re.fullmatch(r"WP-C\d+[a-z]+", k)}}
    assert set(khoi) >= {"WP-C2", "WP-C3a", "WP-C3b", "WP-C3c", "WP-C3d", "WP-C4a", "WP-C4b", "WP-C4c", "WP-C5a", "WP-C5b"}, sorted(khoi)     # Đ3: mẫu số ⛔ rỗng
    thieu = {g: [k for k in ("tong_o", "khop") if type(b.get(k)) is not int] for g, b in khoi.items()}
    assert {g: t for g, t in thieu.items() if t} == {}, thieu
    assert all(b["khop"] <= b["tong_o"] and b["tong_o"] > 0 for b in khoi.values())


@pytest.mark.pg
def test_CG2_R2_03_cong_tuyen_THAT_moi_goi_con_trong_tep_deu_hien_va_khong_null():
    """Tập cổng ĐỌC TỪ TỆP: 4 cha khai sẵn + mỗi gói con của tệp; mọi cha đều có con ⇒ 0 null (H12: + C5a · H13: + C5b)."""
    d = _that()
    con = sorted(k for k in d if re.fullmatch(r"WP-C\d+[a-z]+", k))
    mong = {"HD2_WP_C2", "HD2_WP_C3", "HD2_WP_C4", "HD2_WP_C5", *(bc._ma_hd2(k) for k in con)}
    h = _hd2(_gates(TEP_HD2_THAT))
    assert set(h) == mong and len(h) == 13, sorted(h)      # 4 cha + 9 con (C3a·b·c·d · C4a·b·c · C5a·b)
    assert sorted(m for m, c in h.items() if c["dat"] is None) == []


# ══ CG2-B1 · tệp thật ⇒ cổng theo gói; gói chưa đo ⇒ null ══════════════════════════════════════
@pytest.mark.pg
def test_CG2_B1_tep_that_qua_tuyen_9_cong_dung_dat_C5_null():
    h = _hd2(_gates(TEP_HD2_THAT))
    assert {m: c["dat"] for m, c in h.items()} == MONG_THAT, h
    assert MONG_O_C5A in h["HD2_WP_C5A"]["da_do"] and "5118 lệch có chủ đích" in h["HD2_WP_C5A"]["da_do"]
    assert MONG_O_C5B in h["HD2_WP_C5B"]["da_do"] and "923 lệch có chủ đích" in h["HD2_WP_C5B"]["da_do"]
    assert h["HD2_WP_C5"]["da_do"].startswith("2/2 gói con đạt (WP-C5a · WP-C5b)"), h["HD2_WP_C5"]
    assert MONG_O_C4A in h["HD2_WP_C4A"]["da_do"] and "3/3 gói con đạt (WP-C4a · WP-C4b · WP-C4c)" in h["HD2_WP_C4"]["da_do"]
    assert MONG_O_C4B in h["HD2_WP_C4B"]["da_do"] and MONG_O_C4C in h["HD2_WP_C4C"]["da_do"]
    assert MONG_O_C2 in h["HD2_WP_C2"]["da_do"]
    assert MONG_O_C3A in h["HD2_WP_C3A"]["da_do"] and MONG_O_C3B in h["HD2_WP_C3B"]["da_do"]
    assert MONG_O_C3C in h["HD2_WP_C3C"]["da_do"] and "53 lệch có chủ đích" in h["HD2_WP_C3C"]["da_do"]
    assert MONG_O_C3D in h["HD2_WP_C3D"]["da_do"] and "1791 lệch có chủ đích" in h["HD2_WP_C3D"]["da_do"]


@pytest.mark.pg
def test_CG2_B1_nguon_thu_hai_dat_cua_tep_THAT_khop_mong():
    """Đ2: `MONG_THAT` ↔ chính tệp (⛔ qua mã). Mẫu số ⛔ rỗng (Đ3): 3 gói đo."""
    d = _that()
    goi = {"WP-C2": d["dat"], "WP-C3a": d["WP-C3a"]["dat"], "WP-C3b": d["WP-C3b"]["dat"],
           "WP-C4a": d["WP-C4a"]["dat"], "WP-C4b": d["WP-C4b"]["dat"], "WP-C4c": d["WP-C4c"]["dat"]}
    assert goi == {"WP-C2": True, "WP-C3a": True, "WP-C3b": True, "WP-C4a": True, "WP-C4b": True, "WP-C4c": True}
    assert (d["WP-C4c"]["khop"], d["WP-C4c"]["lech_co_chu_dich"], d["WP-C4c"]["tong_o"]) == (19591, 303, 19894)
    assert d["WP-C4c"]["tong_o"] == d["WP-C4c"]["o_so"] and d["WP-C4c"]["o_trong_dap_an"] == 8611
    assert (d["WP-C4b"]["khop"], d["WP-C4b"]["tong_o"]) == (1981, 1981) == (d["WP-C4b"]["o_so"] - d["WP-C4b"]["lech"], d["WP-C4b"]["o_so"])
    assert (d["WP-C4a"]["khop"], d["WP-C4a"]["tong_o"]) == (420, 420) == (d["WP-C4a"]["o_so"] - d["WP-C4a"]["lech"], d["WP-C4a"]["o_so"])
    assert (d["khop"], d["tong_o"]) == (63016, 63016)
    assert (d["WP-C3a"]["khop"], d["WP-C3a"]["lech_co_chu_dich"], d["WP-C3a"]["tong_o"]) == (205140, 35, 205175)
    assert (d["WP-C3b"]["khop"], d["WP-C3b"]["lech_co_chu_dich"], d["WP-C3b"]["tong_o"]) == (11543, 42, 11585)
    assert (d["WP-C3c"]["khop"], d["WP-C3c"]["lech_co_chu_dich"], d["WP-C3c"]["tong_o"], d["WP-C3c"]["dat"]) == (835, 53, 888, True)
    assert (d["WP-C3d"]["khop"], d["WP-C3d"]["lech_co_chu_dich"], d["WP-C3d"]["tong_o"], d["WP-C3d"]["dat"]) == (1287624, 1791, 1289415, True)
    assert (d["WP-C5a"]["khop"], d["WP-C5a"]["lech_co_chu_dich"], d["WP-C5a"]["tong_o"], d["WP-C5a"]["dat"]) == (40556, 5118, 45674, True)
    assert (d["WP-C5b"]["khop"], d["WP-C5b"]["lech_co_chu_dich"], d["WP-C5b"]["tong_o"], d["WP-C5b"]["dat"]) == (3179, 923, 4102, True)


def test_CG2_B1_tep_CHI_co_C2_cac_goi_khac_null(tmp_path):
    def pha(d):
        d.pop("WP-C3a"), d.pop("WP-C3b"), d.pop("WP-C3c"), d.pop("WP-C3d"), d.pop("WP-C4a"), d.pop("WP-C4b"), d.pop("WP-C4c")
        d.pop("WP-C5a"), d.pop("WP-C5b")
    c = bc.doc_cong_hd2(_tep(tmp_path, pha))
    assert _dat(c) == {"HD2_WP_C2": True, "HD2_WP_C3": None, "HD2_WP_C4": None, "HD2_WP_C5": None}
    assert [x.ma for x in c] == list(MONG_CHA_KHAI_SAN)


def test_CG2_B1_C2_theo_PhanXu_khong_dat_thi_false_kem_ly_do(tmp_path):
    def pha(d):
        d["dat"] = False
        d["ly_do"] = ["3/63016 o LECH"]
        d["khop"] = d["tong_o"] - 3
    x = {c.ma: c for c in bc.doc_cong_hd2(_tep(tmp_path, pha))}["HD2_WP_C2"]
    assert x.dat is False and "3/63016 o LECH" in x.ly_do, x


# ══ CG2-B2 · lát bỏ > 0 ⇒ false (⛔ "100 %") ═══════════════════════════════════════════════════
def test_CG2_B2_lat_bo_lon_hon_0_la_false_du_tep_ghi_dat_true(tmp_path):
    def pha(d):
        d["lat_bo"] = 2          # tệp vẫn ghi dat=true — cổng ⛔ tin mù
    x = {c.ma: c for c in bc.doc_cong_hd2(_tep(tmp_path, pha))}["HD2_WP_C2"]
    assert x.dat is False and "2 lát" in x.ly_do, x


def test_CG2_B2_lat_bo_o_goi_con_keo_cha_false_con_kia_van_true(tmp_path):
    def pha(d):
        d["WP-C3a"]["lat_bo"] = 1
    c = _dat(bc.doc_cong_hd2(_tep(tmp_path, pha)))
    assert c["HD2_WP_C3A"] is False and c["HD2_WP_C3"] is False and c["HD2_WP_C3B"] is True


def test_CG2_B2_lat_bo_0_khong_lam_do(tmp_path):
    c = _dat(bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("lat_bo", 0))))
    assert c["HD2_WP_C2"] is True


@pytest.mark.parametrize("v", [-1, True, "2", 1.5])
def test_CG2_B2_lat_bo_sai_kieu_la_null_khong_phai_0(tmp_path, v):
    x = {c.ma: c for c in bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("lat_bo", v)))}
    assert x["HD2_WP_C2"].dat is None and "lat_bo" in x["HD2_WP_C2"].ly_do, x["HD2_WP_C2"]


# ══ CG2-B3 · tệp vắng / hỏng / không truyền ⇒ 4 cổng null + lý do có tên ═══════════════════════
@pytest.mark.pg
@pytest.mark.parametrize("ca", ["khong_truyen", "duong_khong_co_tep"])
def test_CG2_B3_tep_VANG_qua_tuyen_4_cong_null_ly_do_co_ten(tmp_path, ca):
    tep = None if ca == "khong_truyen" else tmp_path / "thu_muc_rieng" / "hd2_cong.json"
    h = _hd2(_gates(tep))
    assert tuple(h) == MONG_CHA_KHAI_SAN, tuple(h)
    for m, c in h.items():
        assert c["dat"] is None and c["nhan"] == "CHUA DO DUOC" and c["ly_do"], (m, c)
        assert "hd2_cong.json" in c["ly_do"] or "được truyền" in c["ly_do"], c["ly_do"]
        assert "thu_muc_rieng" not in c["ly_do"] and str(tmp_path) not in c["ly_do"]


@pytest.mark.parametrize("nd", [b"{ khong phai json", b"[1, 2]", b"", b"\xff\xfe\x00"])
def test_CG2_B3_tep_HONG_4_cong_null_va_KHONG_no(tmp_path, nd):
    p = tmp_path / "hd2_cong.json"
    p.write_bytes(nd)
    c = bc.doc_cong_hd2(p)
    assert [x.ma for x in c] == list(MONG_CHA_KHAI_SAN)
    assert all(x.dat is None and "hd2_cong.json" in x.ly_do for x in c), c


# ══ AC-4 · gói con mới TỰ hiện; gộp cha/con ═════════════════════════════════════════════════════
def _them(d, ten, **ghi):
    b = copy.deepcopy(d["WP-C3b"])
    b["bang"], b["goi"] = f"HD2.{ten}", ten
    b.update(ghi)
    d[ten] = b


def test_AC4_goi_con_MOI_tu_hien_khong_sua_ma(tmp_path):
    def pha(d):
        _them(d, "WP-C3c")
        _them(d, "WP-C4a")
        d.pop("WP-C4b"), d.pop("WP-C4c"), d.pop("WP-C3d"), d.pop("WP-C5a"), d.pop("WP-C5b")   # tệp thật đã có C4b · C4c · C3d · C5a · C5b — ca này đo riêng C4a
    c = bc.doc_cong_hd2(_tep(tmp_path, pha))
    assert [x.ma for x in c] == ["HD2_WP_C2", "HD2_WP_C3", "HD2_WP_C3A", "HD2_WP_C3B", "HD2_WP_C3C",
                                 "HD2_WP_C4", "HD2_WP_C4A", "HD2_WP_C5"]
    assert _dat(c)["HD2_WP_C3C"] is True and _dat(c)["HD2_WP_C4A"] is True
    assert _dat(c)["HD2_WP_C4"] is True and _dat(c)["HD2_WP_C5"] is None   # C4 = gộp con C4a


def test_AC4_gop_mot_con_false_thang_con_null_con_null_thang_true(tmp_path):
    def pha(d):
        _them(d, "WP-C3c", dat=False, ly_do=["7/11585 o LECH"], khop=11578)
        _them(d, "WP-C4a")
        _them(d, "WP-C4b")
        del d["WP-C4b"]["dat"]                      # con thiếu `dat` ⇒ null
    c = {x.ma: x for x in bc.doc_cong_hd2(_tep(tmp_path, pha))}
    assert c["HD2_WP_C3"].dat is False and "WP-C3c" in c["HD2_WP_C3"].ly_do     # false thắng true
    assert c["HD2_WP_C4B"].dat is None and c["HD2_WP_C4"].dat is None           # null thắng true
    assert "WP-C4b" in c["HD2_WP_C4"].ly_do


def test_AC4_con_false_va_con_null_thi_cha_false(tmp_path):
    def pha(d):
        _them(d, "WP-C3c", dat=False, ly_do=["x LECH"])
        _them(d, "WP-C3d")
        del d["WP-C3d"]["dat"]
    c = _dat(bc.doc_cong_hd2(_tep(tmp_path, pha)))
    assert c["HD2_WP_C3"] is False and c["HD2_WP_C3D"] is None


def test_AC4_cha_ghi_NHAN_DEM_goi_con_khong_nham_voi_o(tmp_path):
    """Đ4: cổng cha đếm GÓI CON (và Σ ô); cổng lá đếm Ô."""
    c = {x.ma: x for x in bc.doc_cong_hd2(TEP_HD2_THAT)}
    assert c["HD2_WP_C3"].da_do.startswith("4/4 gói con"), c["HD2_WP_C3"].da_do
    assert "1505142/1507063 ô" in c["HD2_WP_C3"].da_do   # 205140 + 11543 + 835 + 1287624 / 205175 + 11585 + 888 + 1289415
    assert "1921 lệch có chủ đích" in c["HD2_WP_C3"].da_do                      # 35 + 42 + 53 + 1791 — ⛔ giấu (ITE-R1-01)
    assert c["HD2_WP_C2"].da_do.startswith(MONG_O_C2)


# ══ chiều ĐỎ · tệp tự mâu thuẫn / mẫu số 0 ⇒ null (Đ3 · Đ5) ═══════════════════════════════════
@pytest.mark.parametrize("ten,pha", [
    ("dat_true_nhung_khop_it_hon", lambda d: d.__setitem__("khop", d["tong_o"] - 1)),
    ("tong_o_0", lambda d: d.update(tong_o=0, khop=0)),
    ("khop_lon_hon_tong", lambda d: d.__setitem__("khop", d["tong_o"] + 1)),
    ("thieu_tong_o", lambda d: d.pop("tong_o")),
    ("dat_khong_phai_bool", lambda d: d.__setitem__("dat", 1)),
    ("goi_khong_khop_khoa", lambda d: d.__setitem__("goi", "WP-C9")),
    ("tong_o_la_bool", lambda d: d.__setitem__("tong_o", True)),
])
def test_tep_TU_MAU_THUAN_goi_do_la_null_cac_goi_khac_doc_lap(tmp_path, ten, pha):
    c = {x.ma: x for x in bc.doc_cong_hd2(_tep(tmp_path, lambda d: pha(d)))}
    assert c["HD2_WP_C2"].dat is None and c["HD2_WP_C2"].ly_do, (ten, c["HD2_WP_C2"])
    assert c["HD2_WP_C3A"].dat is True and c["HD2_WP_C3B"].dat is True


def test_goi_con_hong_chi_C3A_null_cha_null(tmp_path):
    c = _dat(bc.doc_cong_hd2(_tep(tmp_path, lambda d: d["WP-C3a"].__setitem__("tong_o", 0))))
    assert c["HD2_WP_C3A"] is None and c["HD2_WP_C3"] is None and c["HD2_WP_C3B"] is True


# ══ AC-5 · hợp đồng cũ giữ — chỉ THÊM ═════════════════════════════════════════════════════════
@pytest.mark.pg
def test_AC5_gates_cu_chi_THEM_phan_tu_va_3_con_so_tom_dem_dung():
    a = _gates(None)
    b = _gates(TEP_HD2_THAT)
    cu = [c["ma"] for c in a["cong"] if not c["ma"].startswith("HD2_")]
    assert "FINAL" in cu and "KHO_SACH" in cu and "HD1_THANG" in cu
    assert [c["ma"] for c in b["cong"] if not c["ma"].startswith("HD2_")] == cu
    assert {c["ma"] for c in b["cong"]} >= set(cu) | set(MONG_THAT)
    # `None` ⇒ 4 cổng HD2 null; tệp thật ⇒ 13 true + 0 null (H12: C5 có con C5a · H13: + C5b): chua_do_duoc GIẢM đúng 4
    for d in (a, b):
        dat = [c["dat"] for c in d["cong"]]
        assert (d["dat"], d["khong_dat"], d["chua_do_duoc"]) == (
            dat.count(True), dat.count(False), sum(1 for x in dat if x is None))
    assert b["dat"] - a["dat"] == 13 and b["chua_do_duoc"] - a["chua_do_duoc"] == -4


def test_chay_cua_MAC_DINH_tro_DUNG_tep_hd2_that():
    from tools import chay_cua
    assert TEP_HD2_THAT.is_file()
    assert Path(chay_cua.TEP_HD2_MAC_DINH).resolve() == TEP_HD2_THAT.resolve()


# ══ CG2-R1-01 · `lat_bo` VẮNG ⇒ cổng NÓI THẲNG (⛔ `true` im lặng) · `KQ-210` ═══════════════════
# `do_hd2.py` ⛔ cắt lát (`lat_truot=0` gõ cứng) ⇒ khoá `lat_bo` có 0 lần ở tệp thật. Vắng ⇒ coi 0
# NHƯNG cổng khai điều đó (`da_do` + trường máy đọc `lat_bo_nguon` = "vang" | "khai" | "sai_kieu").
_LOI_VANG = "lat_bo vắng ⇒ coi 0 (phép đo HD2 ⛔ cắt lát)"


def _nguon(c) -> dict:
    return {x.ma: x.lat_bo_nguon for x in c}


def test_CG2_R1_01_tep_THAT_khong_co_khoa_lat_bo_mau_so_khong_rong():
    """Đ3: tập ⛔ rỗng — ba gói đo, và CẢ BA vắng khoá ⇒ ca 'vắng' là ca THẬT."""
    d = _that()
    khoi = [d, d["WP-C3a"], d["WP-C3b"], d["WP-C3c"], d["WP-C3d"], d["WP-C4a"], d["WP-C4b"], d["WP-C4c"], d["WP-C5a"], d["WP-C5b"]]
    assert len(khoi) == 10 and all("lat_bo" not in b for b in khoi)


def test_CG2_R1_01_vang_thi_true_nhung_da_do_noi_thang_va_nguon_vang():
    c = bc.doc_cong_hd2(TEP_HD2_THAT)
    x = {y.ma: y for y in c}
    assert _nguon(c) == {"HD2_WP_C2": "vang", "HD2_WP_C3": "vang", "HD2_WP_C3A": "vang",
                         "HD2_WP_C3B": "vang", "HD2_WP_C3C": "vang", "HD2_WP_C3D": "vang", "HD2_WP_C4": "vang", "HD2_WP_C4A": "vang", "HD2_WP_C4B": "vang",
                         "HD2_WP_C4C": "vang", "HD2_WP_C5": "vang", "HD2_WP_C5A": "vang",
                         "HD2_WP_C5B": "vang"}
    for m in ("HD2_WP_C2", "HD2_WP_C3A", "HD2_WP_C3B", "HD2_WP_C3C", "HD2_WP_C3D", "HD2_WP_C3", "HD2_WP_C4A", "HD2_WP_C4B", "HD2_WP_C4C",
              "HD2_WP_C4", "HD2_WP_C5A", "HD2_WP_C5B", "HD2_WP_C5"):
        assert x[m].dat is True and _LOI_VANG in x[m].da_do, x[m]
    assert x["HD2_WP_C2"].da_do.startswith(MONG_O_C2)          # nhãn Đ4 cũ giữ nguyên


def test_CG2_R1_01_khai_0_thi_nguon_khai_va_khong_co_cau_vang(tmp_path):
    c = bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("lat_bo", 0)))
    x = {y.ma: y for y in c}
    assert x["HD2_WP_C2"].dat is True and x["HD2_WP_C2"].lat_bo_nguon == "khai"
    assert _LOI_VANG not in x["HD2_WP_C2"].da_do
    assert x["HD2_WP_C3A"].lat_bo_nguon == "vang" and x["HD2_WP_C3"].lat_bo_nguon == "vang"


def test_CG2_R1_01_khai_2_thi_false_nguon_khai(tmp_path):
    c = bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("lat_bo", 2)))
    x = {y.ma: y for y in c}
    assert x["HD2_WP_C2"].dat is False and x["HD2_WP_C2"].lat_bo_nguon == "khai"


@pytest.mark.parametrize("v", [None, -1, True, "0", 0.0])
def test_CG2_R1_01_khoa_co_nhung_hong_thi_null_ly_do_co_ten_nguon_sai_kieu(tmp_path, v):
    x = {y.ma: y for y in bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("lat_bo", v)))}
    c2 = x["HD2_WP_C2"]
    assert c2.dat is None and "`lat_bo`" in c2.ly_do and c2.lat_bo_nguon == "sai_kieu", c2


@pytest.mark.pg
def test_CG2_R1_01_qua_tuyen_truong_lat_bo_nguon_THEM_vao_hop_dong():
    """Hợp đồng `/gates` chỉ THÊM: mọi cổng có khoá `lat_bo_nguon`; 4 khoá cũ còn nguyên."""
    h = _hd2(_gates(TEP_HD2_THAT))
    assert {m: c["lat_bo_nguon"] for m, c in h.items()} == {
        "HD2_WP_C2": "vang", "HD2_WP_C3": "vang", "HD2_WP_C3A": "vang", "HD2_WP_C3B": "vang",
        "HD2_WP_C3C": "vang", "HD2_WP_C3D": "vang", "HD2_WP_C4": "vang", "HD2_WP_C4A": "vang", "HD2_WP_C4B": "vang", "HD2_WP_C4C": "vang", "HD2_WP_C5": "vang",
        "HD2_WP_C5A": "vang", "HD2_WP_C5B": "vang"}
    assert all({"ma", "ten", "dat", "nhan", "da_do", "ly_do"} <= set(c) for c in h.values())
    assert _LOI_VANG in h["HD2_WP_C2"]["da_do"]


# ══ CG2-R1-02 · khối gói mang KIỂU HỎNG ⇒ cổng con HIỆN, null + lý do (⛔ biến mất im) ═══════════
@pytest.mark.parametrize("v", [[1], None, "x", 5, True])
def test_CG2_R1_02_khoi_goi_con_sai_kieu_hien_null_cha_null_khong_true(tmp_path, v):
    c = {y.ma: y for y in bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("WP-C3a", v)))}
    assert "HD2_WP_C3A" in c, list(c)                     # ⛔ biến mất im
    assert c["HD2_WP_C3A"].dat is None and "WP-C3a" in c["HD2_WP_C3A"].ly_do, c["HD2_WP_C3A"]
    assert c["HD2_WP_C3"].dat is None, c["HD2_WP_C3"]       # ⛔ `true` (trước: C3 `true` nhờ mỗi C3b)
    assert c["HD2_WP_C3B"].dat is True


def test_CG2_R1_02_goi_con_moi_sai_kieu_cung_hien(tmp_path):
    c = {y.ma: y for y in bc.doc_cong_hd2(_tep(tmp_path, lambda d: d.__setitem__("WP-C4a", [1])))}
    assert c["HD2_WP_C4A"].dat is None and c["HD2_WP_C4"].dat is None


# ══ `-04` · ghim `goi ≠ khoá` ở GÓI CON (đột biến M8 sống ở R1) ════════════════════════════════
def test_CG2_R1_04_goi_con_ghi_goi_khac_khoa_thi_null_ly_do_noi_goi(tmp_path):
    c = {y.ma: y for y in bc.doc_cong_hd2(
        _tep(tmp_path, lambda d: d["WP-C3a"].__setitem__("goi", "WP-C3b")))}
    assert c["HD2_WP_C3A"].dat is None and "`goi`" in c["HD2_WP_C3A"].ly_do, c["HD2_WP_C3A"]
    assert c["HD2_WP_C3"].dat is None and c["HD2_WP_C3B"].dat is True


# ══ `-05` · ghim dây `tools/chay_cua.py` → `dung_may(tep_hd2=…)` (đột biến M13 sống ở R1) ═════════
class _Dung(Exception):
    pass


@pytest.mark.parametrize("argv,mong", [
    ([], str(TEP_HD2_THAT)),
    (["--tep-hd2", "/x/khac.json"], "/x/khac.json"),
    (["--tep-hd2", ""], None),
])
def test_CG2_R1_05_chay_cua_truyen_DUNG_tep_hd2_vao_dung_may(monkeypatch, argv, mong):
    from tools import chay_cua
    bat = {}

    def gia(*a, **k):
        bat.update(k)
        raise _Dung

    monkeypatch.setenv("PG_DSN", "postgresql://x:y@localhost:1/z")
    monkeypatch.setattr(chay_cua.cua, "dung_may", gia)
    monkeypatch.setattr("sys.argv", ["chay_cua.py", *argv])
    with pytest.raises(_Dung):
        chay_cua.main()
    assert "tep_hd2" in bat, bat
    got = bat["tep_hd2"]
    assert (None if got is None else str(Path(got).resolve() if mong == str(TEP_HD2_THAT) else got)
            ) == (None if mong is None else str(Path(mong).resolve() if mong == str(TEP_HD2_THAT) else mong))


# ══ ITE-R1-01 (`KQ-231`) · Ô LỆCH CÓ CHỦ ĐÍCH hiện thành TRƯỜNG RIÊNG của cổng ═══════════════════
# Lỗi đã xảy ra: `khop` cộng cả 35/42 ô lệch ITE ⇒ cổng in `205175/205175 ô đáp án khớp` — sai 35 ô, người xem
# `/gates` ⛔ thấy lệch. Nay `khop` = ô KHỚP đáp án thật; `lech_co_chu_dich` (số ô) + `mong_lech_co_chu_dich`
# (khai trước) là hai khoá riêng. `dat` khi `khop + lech == tong_o` VÀ `lech == mong`; cha = Σ con.
def _c3a(tmp_path, pha) -> dict:
    return {x.ma: x for x in bc.doc_cong_hd2(_tep(tmp_path, pha))}


def test_ITE_R1_01_tep_THAT_ba_cong_C3_khai_35_42_77_va_khop_la_khop_that():
    """Đ3: mẫu số ⛔ rỗng — 2 khối đo có lệch > 0 trong tệp thật; câu in đọc ĐÚNG cột đếm."""
    d = _that()
    assert (d["WP-C3a"]["lech_co_chu_dich"], d["WP-C3b"]["lech_co_chu_dich"]) == (35, 42)
    x = {c.ma: c for c in bc.doc_cong_hd2(TEP_HD2_THAT)}
    assert [x[m].lech_co_chu_dich for m in ("HD2_WP_C3A", "HD2_WP_C3B", "HD2_WP_C3C", "HD2_WP_C3D", "HD2_WP_C3")] == [35, 42, 53, 1791, 1921]
    assert x["HD2_WP_C3A"].dat is x["HD2_WP_C3B"].dat is x["HD2_WP_C3"].dat is True
    assert "205140/205175 ô đáp án khớp + 35 lệch có chủ đích" in x["HD2_WP_C3A"].da_do
    assert "11543/11585 ô đáp án khớp + 42 lệch có chủ đích" in x["HD2_WP_C3B"].da_do
    assert "205175/205175" not in x["HD2_WP_C3A"].da_do          # ⛔ câu cũ (tử số cộng lệch)
    # cổng ⛔ có lệch có chủ đích ⇒ 0, ⛔ in cụm "lệch có chủ đích"
    for m in ("HD2_WP_C2", "HD2_WP_C4A", "HD2_WP_C4B"):
        assert x[m].lech_co_chu_dich == 0 and "lệch có chủ đích" not in x[m].da_do, m
    # ⭐ KQ-236 H11-R1-02: WP-C4c khai 303 lệch nguồn CÓ TÊN (52 OMC + 251 SC) ⇒ /gates hiện số lệch; cha C4 = Σ con
    assert (x["HD2_WP_C4C"].lech_co_chu_dich, x["HD2_WP_C4"].lech_co_chu_dich) == (303, 303)
    assert x["HD2_WP_C4C"].dat is True and "19591/19894 ô đáp án khớp + 303 lệch có chủ đích" in x["HD2_WP_C4C"].da_do
    assert "19591/19591" not in x["HD2_WP_C4C"].da_do                  # ⛔ câu cũ (mẫu số trừ lệch)


def test_ITE_R1_01_ca_0_khoa_vang_goi_cu_coi_0_va_dat_nhu_cu(tmp_path):
    def pha(d):
        for g in ("WP-C3a", "WP-C3b", "WP-C3c", "WP-C3d"):    # gói CŨ: khop cộng lệch, ⛔ khai trường mới
            d[g]["khop"] = d[g]["tong_o"]
            d[g].pop("lech_co_chu_dich"), d[g].pop("mong_lech_co_chu_dich")
    x = _c3a(tmp_path, pha)
    assert x["HD2_WP_C3A"].dat is True and x["HD2_WP_C3A"].lech_co_chu_dich == 0
    assert x["HD2_WP_C3"].lech_co_chu_dich == 0 and "205175/205175 ô đáp án khớp" in x["HD2_WP_C3A"].da_do


def test_ITE_R1_01_ca_khai_DUNG_true_va_cha_la_tong_con(tmp_path):
    x = _c3a(tmp_path, lambda d: None)
    assert x["HD2_WP_C3A"].dat is True and x["HD2_WP_C3"].lech_co_chu_dich == 35 + 42 + 53 + 1791


@pytest.mark.parametrize("pha", [
    lambda d: d["WP-C3a"].__setitem__("mong_lech_co_chu_dich", 34),          # mong ≠ thực
    lambda d: d["WP-C3a"].__setitem__("mong_lech_co_chu_dich", 36),
    lambda d: d["WP-C3a"].pop("mong_lech_co_chu_dich"),                      # lệch có mà ⛔ khai mong ⇒ mong 0
])
def test_ITE_R1_01_ca_khai_SAI_mong_khac_thuc_thi_FALSE_ca_hai_chieu_va_cha(tmp_path, pha):
    x = _c3a(tmp_path, pha)
    assert x["HD2_WP_C3A"].dat is False and "mong" in x["HD2_WP_C3A"].ly_do, x["HD2_WP_C3A"]
    assert x["HD2_WP_C3"].dat is False and x["HD2_WP_C3B"].dat is True       # cha ⛔ xanh nhờ con kia


def test_ITE_R1_01_ca_khai_SAI_tong_khong_khop_khop_cong_lech_ne_tong_o_thi_null(tmp_path):
    x = _c3a(tmp_path, lambda d: d["WP-C3a"].__setitem__("lech_co_chu_dich", 34))   # 205140 + 34 ≠ 205175
    assert x["HD2_WP_C3A"].dat is None and "205140" in x["HD2_WP_C3A"].ly_do and x["HD2_WP_C3"].dat is None


@pytest.mark.parametrize("ten", ["lech_co_chu_dich", "mong_lech_co_chu_dich"])
@pytest.mark.parametrize("v", [None, -1, True, "35", 35.0, [35]])
def test_ITE_R1_01_ca_HONG_khoa_co_ma_khong_phai_so_nguyen_ge_0_thi_null_co_ten(tmp_path, ten, v):
    x = _c3a(tmp_path, lambda d: d["WP-C3a"].__setitem__(ten, v))
    assert x["HD2_WP_C3A"].dat is None and f"`{ten}`" in x["HD2_WP_C3A"].ly_do, x["HD2_WP_C3A"]
    assert x["HD2_WP_C3"].dat is None and x["HD2_WP_C3B"].dat is True


@pytest.mark.pg
def test_ITE_R1_01_qua_tuyen_THAT_gates_co_truong_lech_co_chu_dich_THEM_vao_hop_dong():
    h = _hd2(_gates(TEP_HD2_THAT))
    assert {m: c["lech_co_chu_dich"] for m, c in h.items()} == {
        "HD2_WP_C2": 0, "HD2_WP_C3": 1921, "HD2_WP_C3A": 35, "HD2_WP_C3B": 42, "HD2_WP_C3C": 53, "HD2_WP_C3D": 1791,
        "HD2_WP_C4": 303, "HD2_WP_C4A": 0, "HD2_WP_C4B": 0, "HD2_WP_C4C": 303, "HD2_WP_C5": 6041, "HD2_WP_C5A": 5118,
        "HD2_WP_C5B": 923}
    assert all({"ma", "ten", "dat", "nhan", "da_do", "ly_do", "lat_bo_nguon"} <= set(c) for c in h.values())
    assert "35 lệch có chủ đích" in h["HD2_WP_C3A"]["da_do"] and "1921 lệch có chủ đích" in h["HD2_WP_C3"]["da_do"]
    assert all(type(c["lech_co_chu_dich"]) is int for c in h.values())


# ══ H7-R1-02 (`KQ-247`, Đ4) · nhãn "835/888" tách ô CÓ SỐ khỏi ô 0 = 0 ═══════════════════════════
# Lỗi đã xảy ra: `835/888 ô khớp` đếm cả **619** ô `0 = 0` ⇒ đầu đề nghe "94 % khớp" trong khi khớp thật
# **216/269** ô có số. Ba khoá THÊM `o_co_so`/`khop_co_so`/`o_0_0`; `khop` GIỮ nghĩa hợp đồng CG2 (`khop + lech =
# tong_o`) = `khop_co_so + o_0_0`. Có khoá mà mâu thuẫn / thiếu / sai kiểu ⇒ `null` có tên (Đ5).
def test_H7_R1_02_tep_THAT_C3c_tach_nhan_o_co_so_khoi_o_0_0():
    d = _that()["WP-C3c"]
    assert (d["tong_o"], d["o_co_so"], d["khop_co_so"], d["o_0_0"], d["lech_co_chu_dich"]) == (888, 269, 216, 619, 53)
    assert d["khop"] == d["khop_co_so"] + d["o_0_0"] == 835 and d["o_co_so"] + d["o_0_0"] == d["tong_o"]
    assert d["khop_co_so"] + d["lech_co_chu_dich"] == d["o_co_so"]            # 216 + 53 = 269
    x = {c.ma: c for c in bc.doc_cong_hd2(TEP_HD2_THAT)}
    assert "835/888 ô đáp án khớp [khớp thật 216/269 ô có số · 619 ô 0 = 0] + 53 lệch có chủ đích" in x["HD2_WP_C3C"].da_do
    assert x["HD2_WP_C3C"].dat is True and "khớp thật" not in x["HD2_WP_C3A"].da_do      # gói cũ: câu cũ


@pytest.mark.parametrize("pha", [
    lambda b: b.__setitem__("o_0_0", 618),                       # 216 + 618 ≠ 835
    lambda b: b.__setitem__("o_co_so", 270),                     # 270 + 619 ≠ 888
    lambda b: b.pop("khop_co_so"),                               # thiếu một trong ba
    lambda b: b.__setitem__("o_0_0", "619"),                     # sai kiểu
    lambda b: b.__setitem__("khop_co_so", -1),
])
def test_H7_R1_02_nhan_mau_thuan_thieu_sai_kieu_thi_NULL_co_ten(tmp_path, pha):
    x = _c3a(tmp_path, lambda d: pha(d["WP-C3c"]))
    assert x["HD2_WP_C3C"].dat is None and ("nhãn ô" in x["HD2_WP_C3C"].ly_do or "o_co_so" in x["HD2_WP_C3C"].ly_do), x["HD2_WP_C3C"]
    assert x["HD2_WP_C3"].dat is None                                            # cha: con null ⇒ null
