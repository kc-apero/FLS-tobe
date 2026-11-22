"""ẢNH ĐÁP ÁN còn thiếu cho H14 — PD 607 · 608 · 609 *(P&L Report)* + 615 *(A-CCR)* — `DT11-R1-02` *(`KQ-271`, orchestrator quyết
22/11: đóng băng THÊM)*. Khuôn riêng `daily_report_3_fs2` · `daily_report_3_fs1` · `daily_report_3_gop` · `ccr_daily_report`
+ thân chung `_dr_luoi.py`; ⛔ sửa khuôn/ảnh `daily_report_2` · `daily_report_3` · 22 ảnh cũ.

⭐ Số đo 22/11 *(khoá SA chỉ-đọc; mỗi số đếm MỘT vật — Đ4)*:
  | ảnh | tab · lưới sheet | dòng ảnh | cột ảnh | ô SỐ ≠ rỗng *(⛔ ô lỗi)* | ô lỗi |
  | `daily_report_3_fs2` PD 607 | `[FS2]5. Daily Report 3` · P&L Report · 1424×40 | 1.236 | 41 | 27.290 | 0 |
  | `daily_report_3_fs1` PD 608 | `[FS1]5. Daily Report 3` · P&L Report · 1092×40 | 921 | 41 | 17.962 | 0 |
  | `daily_report_3_gop` PD 609 | `5. Daily Report 3` · P&L Report · 1940×40 | 1.742 | 41 | 35.542 | 0 |
  | `ccr_daily_report` PD 615 | `5. Daily Report` · A-CCR · 12521×44 *(API trả 2.502 hàng)* | 2.057 | 41 | 48.021 | 127 |
"""
from __future__ import annotations

import datetime
import hashlib
import importlib.util
import json
import pathlib
import sys
from collections import Counter

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
F = GOC / "tests" / "fixture" / "dap_an"
KH = GOC / "tools" / "khuon_dong_bang"
TEN = ("daily_report_3_fs2", "daily_report_3_fs1", "daily_report_3_gop", "ccr_daily_report")

#: ⭐ số DÒNG ảnh *(hàng sheet có ≥ 1 ô số/lỗi)* · số cột ảnh *(khoá + chọn)* · ô SỐ ≠ rỗng *(⛔ ô lỗi — mẫu số, Đ3)*.
MONG = {"daily_report_3_fs2": (1236, 41, 27290), "daily_report_3_fs1": (921, 41, 17962),
        "daily_report_3_gop": (1742, 41, 35542), "ccr_daily_report": (2057, 41, 48021)}
CHECKSUM = {"daily_report_3_fs2": "a1c97597ece5ff24", "daily_report_3_fs1": "8c7617a6e2a55f0f",
            "daily_report_3_gop": "7a76faa90919bf03", "ccr_daily_report": "14f965a9b8f7a4e8"}
#: ô số-hoặc-lỗi ở `F…AL` của BẢN ĐỌC THÔ *(Đ4: ⛔ cột nhãn `A…E`)* — bảo toàn: chính + `tieu_de` = số này.
SO_THO_F_AL = {"daily_report_3_fs2": 27605, "daily_report_3_fs1": 18199, "daily_report_3_gop": 35860, "ccr_daily_report": 48758}
#: sha256 ghim *(⛔ đổi byte nào — ảnh DT11 đã R1 ĐẠT đọc-lại-bằng-SA)*.
SHA_DT11 = {"daily_report_2.json": "38a26e3b656064ba76604f122fd965f56015c3d853c132d91b4afb3dc13324d8",
            "daily_report_3.json": "04abe48f871f0cdc1ebba44dfe76e1269a9dc769d178cf7b3c3163056e0ab6cb"}
#: dải ngày — hàng tiêu đề ngày · `From`/`To` *(`C2`·`C3`, serial)* · cột ngày cuối THẬT · số ô ở `AK` *(Đ4)*.
NGAY = {"daily_report_3_fs2": (5, 45962, 45991, "AJ", 395), "daily_report_3_fs1": (5, 45962, 45991, "AJ", 395),
        "daily_report_3_gop": (5, 45992, 46022, "AK", 395), "ccr_daily_report": (5, 46327, 46356, "AJ", 922)}
#: kỳ/cột 0 ô — có tên *(Đ5)*; ccr không có.
CHUA = {"daily_report_3_fs2": ("F", "AL"), "daily_report_3_fs1": ("F", "AL"), "daily_report_3_gop": ("F", "AL"),
        "ccr_daily_report": ()}
#: hàng ảnh KHÔNG có mã `ma` *(chỉ có số, nhãn rỗng/`.`)* — khai thay vì để im.
KHONG_MA = {"daily_report_3_fs2": 17, "daily_report_3_fs1": 12, "daily_report_3_gop": 37, "ccr_daily_report": 38}
#: ô LỖI Sheets ở vùng giá trị theo LOẠI — ghi nguyên chuỗi *(`#REF!`/`#N/A` giữ nguyên)*.
LOAI_LOI = {"daily_report_3_fs2": {}, "daily_report_3_fs1": {}, "daily_report_3_gop": {},
            "ccr_daily_report": {"#DIV/0!": 84, "#N/A": 16, "#REF!": 18, "#VALUE!": 9}}
#: ảnh > 2 MB *(luật `DT4-R1-07`: ảnh lớn ⇒ KHAI)*: tên → byte *(đo 22/11)*. Khác ⇒ ĐỎ cả hai chiều.
ANH_LON = {"ccr_daily_report": 2242856}


def _doc(ten: str) -> dict:
    return json.loads((F / f"{ten}.json").read_text(encoding="utf-8"))


def _checksum_lai(anh: dict) -> str:
    """⭐ TÍNH LẠI checksum từ `dong` + `phu` của CHÍNH tệp ảnh *(⛔ chỉ so chữ ghi sẵn — `DT11-R1-01`)*."""
    phu = tuple({"phu": ten, "dong": r} for ten, b in anh.get("phu", {}).items() for r in b["dong"])
    return AnhChup(run_id=f"dong_bang_sheet:{anh['khuon']}",
                   ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _nap(ten: str):
    spec = importlib.util.spec_from_file_location(f"kh_{ten}_h14", KH / f"{ten}.py")
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module", params=TEN)
def bo(request):
    return request.param, _doc(request.param), _nap(request.param)


def _cot_gt(K):
    return K.COT[8:]                                                    # f…al *(sau phan·khoi·ma·nhan_a…e)*


def _td(a: dict) -> dict:
    return {(int(r["dong_sheet"]), r["cot"]["chu"]): r["gia_tri"] for r in a["phu"]["tieu_de"]["dong"]}


def _la_loi(v) -> bool:
    return isinstance(v, dict) and v["chu"].startswith("#") and v["chu"].split(" ")[0] in {"#DIV/0!", "#N/A", "#REF!", "#VALUE!", "#NAME?", "#NULL!", "#NUM!", "#ERROR!"}


# ── AC-1 · số dòng · cột · ô ≠ 0 khai `mong`; checksum TÍNH LẠI ──────────────

def test_AC1_anh_dong_cot_o_khac_0_va_cong_dat(bo):
    ten, a, K = bo
    n, c, o = MONG[ten]
    assert a["so_dong"] == len(a["dong"]) == n and a["cong"]["dat"] is True and a["cong"]["mong"] == n
    assert len(a["cot"]) == c and o > 0                                   # Đ3: mẫu số ≠ 0
    so = sum(1 for d in a["dong"] for x in _cot_gt(K) if d[x] is not None and not _la_loi(d[x]))
    assert so == o
    assert a["thieu"] == [] and a["trung"] == [] and a["o_rong"] == [] and a["bang"] == K.BANG
    assert a["khoa"] == "dong_sheet" and len({d["dong_sheet"] for d in a["dong"]}) == n


def test_AC1_checksum_TINH_LAI_tu_noi_dung_khop_ghim(bo):
    ten, a, K = bo
    assert a["checksum_noi_dung"] == _checksum_lai(a) == CHECKSUM[ten]


@pytest.mark.parametrize("ten", TEN)
def test_AC1_PHA_doi_mot_o_thi_checksum_tinh_lai_DO(ten):
    """Đột biến của R1: +1 một ô số ở bảng chính ⇒ checksum tính lại ⛔ còn bằng ghim; bảng phụ cũng vậy."""
    a = _doc(ten)
    assert _checksum_lai(a) == CHECKSUM[ten]                              # nền XANH trước khi phá
    d = next(d for d in a["dong"] if d["g"] is not None and not _la_loi(d["g"]))
    cu = d["g"]
    d["g"] = str(float(cu) + 1)
    assert _checksum_lai(a) != CHECKSUM[ten]
    d["g"] = cu
    a["phu"]["tieu_de"]["dong"][0]["gia_tri"] = {"chu": "đã bị sửa"}
    assert _checksum_lai(a) != CHECKSUM[ten]


# ── Bảo toàn · không mất ô nào ──────────────────────────────────────────────

def test_bao_toan_o_so_hoac_loi_chinh_cong_tieu_de_bang_ban_tho(bo):
    """Mọi ô số/lỗi `F…AL` của bản đọc thô nằm ở bảng chính HOẶC `tieu_de` *(Đ4: ⛔ gồm cột nhãn A…E)*; ô chữ/bool ở `o_khong_so`."""
    ten, a, K = bo
    chinh = sum(1 for d in a["dong"] for x in _cot_gt(K) if d[x] is not None)
    cot_ok = {c.upper() for c in _cot_gt(K)}
    tieu = sum(1 for (_, c), v in _td(a).items() if c in cot_ok and not isinstance(v, (dict, bool)) or
               (c in cot_ok and isinstance(v, dict) and v["chu"].startswith("#") and _la_loi(v)))
    assert chinh + tieu == SO_THO_F_AL[ten]
    assert a["phu"]["o_khong_so"]["so_dong"] == len(a["phu"]["o_khong_so"]["dong"]) == a["phu"]["o_khong_so"]["mong"]


# ── AC-2 · nhãn từng số (Đ4) ────────────────────────────────────────────────

def test_AC2_nhan_tung_so_moi_cot_co_so_deu_co_tieu_de_va_hang_khong_ma_khai(bo):
    ten, a, K = bo
    td = _td(a)
    cot_so = [c for c in _cot_gt(K) if any(d[c] is not None for d in a["dong"])]
    assert cot_so and not [c for c in cot_so if not any(k[1] == c.upper() and k[0] >= 5 for k in td)]   # cột có số ⇒ có tiêu đề
    assert sum(1 for d in a["dong"] if d["ma"] is None) == KHONG_MA[ten]
    ngay = NGAY[ten]
    h, frm, to, cuoi, ak = ngay
    # trục ngày: hàng `h` cột `G…cuối` = From…To (serial liên tục) · ⛔ `AK` lẫn vào ngày khi nó KHÔNG phải ngày
    seq = [td[(h, c)] for c in ("G", "H", "I", "J")]
    assert td[(2, "C")] == str(frm) and td[(3, "C")] == str(to) and seq[0] == str(frm)
    assert td[(h, cuoi.upper())] == str(to)
    assert ((h, "AK") in td) == (cuoi == "AK")                            # AK có tiêu đề ngày ⇔ AK là ngày thật
    n_ak = sum(1 for d in a["dong"] if d["ak"] is not None)
    assert n_ak == ak > 0


def test_AC2_ak_khong_ngay_co_ten_khi_khong_co_tieu_de_ngay(bo):
    """`DT11-R1-04` áp lại: cột `AK` ⛔ có tiêu đề ngày ở hàng ngày ⇒ gọi `khong_ngay` *(vết kéo công thức)*, ⛔ "ngày 31"."""
    ten, a, K = bo
    h, frm, to, cuoi, ak = NGAY[ten]
    td = _td(a)
    assert (cuoi == "AJ") == ((h, "AK") not in td)
    assert (to - frm + 1) == (31 if cuoi == "AK" else 30)                 # số ngày From…To khớp cột cuối thật


# ── AC-4 · cột 0 ô có tên ───────────────────────────────────────────────────

def test_AC4_chua_co_du_lieu_co_ten_va_PHA_xoa_cot_thi_DO(bo):
    ten, a, K = bo
    assert K.CHUA_CO_DU_LIEU == CHUA[ten]
    chua_do = tuple(c.upper() for c in _cot_gt(K) if all(d[c] is None for d in a["dong"]))
    assert chua_do == CHUA[ten]
    d2 = json.loads(json.dumps(a["dong"]))
    assert K.thieu_lac(d2)["thieu"] == []                                 # nền XANH
    for d in d2:
        d["h"] = None                                                     # xoá cả cột `H`
    r = K.thieu_lac(d2)
    assert r["thieu"] and any("chua_co_du_lieu" in x for x in r["thieu"])


def test_AC4_D3_tap_rong_va_mong_chua_khai_deu_do(bo, monkeypatch):
    ten, a, K = bo
    with pytest.raises(ValueError):
        K.thieu_lac([])
    monkeypatch.setattr(K, "MONG_COT", {})
    with pytest.raises(ValueError):
        K.thieu_lac(json.loads(json.dumps(a["dong"])))


def test_AC4_PHA_doi_mot_o_so_thi_MONG_COT_DO(bo):
    """Đ5 hai chiều: thêm một ô số ở cột đang rỗng / bớt một ô ⇒ ĐỎ *(⛔ cổng chỉ-đếm-tổng xanh mãi)*."""
    ten, a, K = bo
    d2 = json.loads(json.dumps(a["dong"]))
    d = next(d for d in d2 if d["g"] is not None and not _la_loi(d["g"]))
    d["g"] = None
    assert any("cột G" in x for x in K.thieu_lac(d2)["thieu"])
    d2 = json.loads(json.dumps(a["dong"]))
    d2[0]["al"] = "1"
    assert K.thieu_lac(d2)["thieu"]


# ── AC-5 · ô lỗi ghi nguyên + đếm theo cột ──────────────────────────────────

def test_AC5_o_loi_dem_theo_cot_ghim_phan_bo_va_giu_nguyen_chuoi(bo):
    ten, a, K = bo
    gt = set(_cot_gt(K))
    assert set(a["loi_mong"]) == set(a["loi_theo_cot"]) == gt             # khai RÕ RÀNG cả 33 cột (0 hoặc phân bố)
    dem = Counter(d[c]["chu"].split(" ")[0] for d in a["dong"] for c in gt if _la_loi(d[c]))
    assert dict(dem) == LOAI_LOI[ten] and len(a["o_loi"]) == sum(LOAI_LOI[ten].values())
    # mỗi cột: phân bố trong ảnh == LOI_MONG của khuôn *(khuôn khai dict theo loại · hoặc 0)*
    for c in gt:
        mong = K.LOI_MONG[c]
        got = Counter(d[c]["chu"].split(" ")[0] for d in a["dong"] if _la_loi(d[c]))
        assert (dict(got) == mong) if isinstance(mong, dict) else (sum(got.values()) == mong == 0), c
    # chuỗi GHI NGUYÊN — ⛔ rút gọn: còn nguyên phần ngoặc của Sheets
    if LOAI_LOI[ten]:
        assert any("(Cannot find range or sheet for imported range.)" in v["chu"] for d in a["dong"] for v in (d[c] for c in gt) if _la_loi(v))
        assert any(v["chu"] == "#N/A" for d in a["dong"] for v in (d[c] for c in gt) if _la_loi(v))


def test_AC5_PHA_cot_khong_loi_gap_loi_thi_cong_DO():
    """Chèn `#REF!` vào một cột khai 0 ⇒ tool đóng băng ĐỎ *(`LOI_MONG` khác đo)*: kiểm bằng chính hàm `_so_loi` của công cụ."""
    spec = importlib.util.spec_from_file_location("dong_bang_sheet_h14", GOC / "tools" / "dong_bang_sheet.py")
    t = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = t
    spec.loader.exec_module(t)
    K = _nap("daily_report_3_fs2")
    assert K.LOI_MONG["g"] == 0
    assert t._tong_loi_mong(K.LOI_MONG["g"]) == 0 and t._tong_loi_mong({"#REF!": 1}) == 1   # 0 ≠ 1 ⇒ ĐỎ ở công cụ


def test_chuan_bi_giu_nguyen_o_loi_va_dua_chu_bool_ra_phu():
    """Thân chung: `#REF!` GIỮ NGUYÊN ở cột giá trị; chữ/bool ⇒ `o_khong_so`; số ở cột nhãn A ⇒ chuỗi; 0 hàng ⇒ ValueError."""
    spec = importlib.util.spec_from_file_location("kh_dr_luoi_t", KH / "_dr_luoi.py")
    G = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = G
    spec.loader.exec_module(G)
    ch = G.CauHinh(n_hang=14, n_dau=2, vung="A1:AL14")
    V = [["T"], ["tieu"], [], [], [], [], [], [],
         ["GROUP"], [7, "GI | x", "", "", "", "chu", 1.5, "#REF! (loi)", None],
         ["", "NB | y", "", "", "", True, 2, "#N/A"], [], [], []]
    r = G.chuan_bi({"values": V}, ch, "thử")
    cot = r["cot"]
    d = {k: v for k, v in zip(cot, r["dong"][0])}
    assert d["nhan_a"] == "7" and d["ma"] == "GI" and d["f"] is None and d["g"] == 1.5 and d["h"] == "#REF! (loi)"
    assert [(x["cot"], x["gia_tri"]) for x in r["phu"]["o_khong_so"]] == [("F", "chu"), ("F", True)]
    d2 = {k: v for k, v in zip(cot, r["dong"][1])}
    assert d2["g"] == 2 and d2["h"] == "#N/A" and d2["ma"] == "NB"
    # chữ/bool ở `G…AL` ⇒ hàng TIÊU ĐỀ *(⛔ vào bảng chính)*
    V2 = [list(h) for h in V]
    V2[9][8] = "H1"
    r2 = G.chuan_bi({"values": V2}, ch, "thử")
    assert len(r2["dong"]) == 1 and any(x["cot"] == "I" and x["gia_tri"] == "H1" for x in r2["phu"]["tieu_de"])
    with pytest.raises(ValueError):
        G.chuan_bi({"values": [[]] * 14}, ch, "rỗng")                     # Đ3: 0 hàng dữ liệu
    with pytest.raises(ValueError):
        G.chuan_bi({"values": V[:5]}, ch, "sai số hàng")


# ── AC-6 · khuôn mới = tệp riêng; ảnh cũ đúng từng byte; kích thước ─────────

def test_AC6_khuon_la_tep_rieng_va_than_chung_khong_sua_khuon_cu():
    for ten in TEN:
        assert (KH / f"{ten}.py").is_file()
    assert (KH / "_dr_luoi.py").is_file() and (KH / "_daily_report.py").is_file()


def test_AC6_anh_DT11_va_cong_cu_chung_dung_tung_byte():
    for k, sha in SHA_DT11.items():
        assert hashlib.sha256((F / k).read_bytes()).hexdigest() == sha, k
    assert hashlib.sha256((GOC / "tools" / "dong_bang_sheet.py").read_bytes()).hexdigest() == \
        "2d8c1724f8403608ffdc1766f148c8c01e22e6da914bb64b701aba4f3cd291c9"


def test_AC6_anh_khong_mang_email_hay_cot_rieng_tu(bo):
    ten, a, K = bo
    assert not any("email" in c.casefold() for c in a["cot"]) and a["cot_khong_chon"] == []
    ung = [v for d in a["dong"] for v in d.values() if isinstance(v, dict) and "@" in v.get("chu", "")]
    ung += [v for b in a["phu"].values() for r in b["dong"] for v in r.values() if isinstance(v, dict) and "@" in str(v.get("chu", ""))]
    assert ung == []


def test_kich_thuoc_anh_lon_hon_2MB_phai_khai_luat_DT4_R1_07(bo):
    ten, a, K = bo
    n = (F / f"{ten}.json").stat().st_size
    if ten in ANH_LON:
        assert n == ANH_LON[ten] and n >= 2 * 1024 * 1024                 # khai ⇒ phải THẬT SỰ lớn (⛔ khai thừa)
    else:
        assert n < 2 * 1024 * 1024
    assert n < 3 * 1024 * 1024                                            # trần cứng: > 3 MB ⇒ chia ảnh


# ── Riêng tư · số TK cá nhân che NGAY ở khuôn ───────────────────────────────

#: số TK cá nhân đã che ở ảnh *(`R | <số>_<NH> <TT>_CN` → `TK_CA_NHAN_<n>`; Đ4: SỐ KHÁC NHAU, ⛔ số chỗ)* — A-CCR có **11** *(4 nhãn `_CN` + 7 nhãn `PO USD` có hậu tố tên người — `DT11-R2-02`, KQ-272)*; P&L Report 0.
SO_TK_CHE = {"daily_report_3_fs2": 0, "daily_report_3_fs1": 0, "daily_report_3_gop": 0, "ccr_daily_report": 11}


def test_PII_anh_khong_mang_so_tk_ca_nhan_va_che_dung_so_khai(bo):
    ten, a, K = bo
    spec = importlib.util.spec_from_file_location("quet_pii_h14", GOC / "tools" / "quet_pii_repo.py")
    q = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = q
    spec.loader.exec_module(q)
    van = (F / f"{ten}.json").read_text(encoding="utf-8")
    assert q.so_cn(van) == []                                             # ⛔ còn số thật
    ma = sorted(set(__import__("re").findall(r"TK_CA_NHAN_(\d+)", van)), key=int)
    assert len(ma) == SO_TK_CHE[ten] and ma == [str(i) for i in range(1, SO_TK_CHE[ten] + 1)]   # Đ3: tập che ≠ rỗng ở ccr
    assert (SO_TK_CHE[ten] > 0) == ("Che " in a["ghi_chu_khuon"])         # ảnh nói thẳng nó đã che


def test_PII_che_pii_doi_so_that_thanh_ma_giu_nguyen_Decimal_va_dem_so_khac_nhau():
    from decimal import Decimal
    spec = importlib.util.spec_from_file_location("kh_dr_luoi_pii", KH / "_dr_luoi.py")
    G = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = G
    spec.loader.exec_module(G)
    so1, so2 = "7" * 12, "8" * 12                                           # dựng lúc chạy: ⛔ để số/mẫu `…_CN` nằm trong NGUỒN (cổng quét repo ĐỎ)
    ra = {"dong": [[f"R | {so1}_ABC DEF_CN", Decimal("1.50"), None], [f"x {so1} y", 7]], "phu": {"a": [{"v": f"R | {so2}_ABC DEF_CN"}]}}
    n = G.che_pii(ra)
    s = repr(ra)
    assert n == 2 and so1 not in s and so2 not in s
    assert ra["dong"][0][1] == Decimal("1.50") and ra["dong"][1][0] == "x TK_CA_NHAN_1 y"      # cùng số ⇒ cùng mã
    assert G.che_pii({"a": ["sạch"]}) == 0                                # ⛔ che khi không có


# ── `DT11-R2-02` (KQ-272, orchestrator quyết CHE) · 7 nhãn `PO USD` mang số TK + tên viết tắt người ───────────

#: 7 hậu tố tên-viết-tắt người ở nhãn `R | <số>_PO USD_<TÊN>` của A-CCR `5. Daily Report` — ⛔ còn ở ảnh.
HAU_TO_TEN = ("HOATT", "SONNH", "HIEPNV", "LUANDQ", "QUYDX", "TRUNGNT", "LOCNX")


def _chuoi_nhan(a: dict):
    """Mọi chuỗi CHỮ ở cột nhãn `nhan_*` của bảng chính + hàng chỉ-nhãn + tiêu đề phụ *(⛔ ô số dạng chuỗi)*."""
    for d in a["dong"]:
        for c in ("nhan_a", "nhan_b", "nhan_c", "nhan_d", "nhan_e"):
            v = d.get(c) if isinstance(d, dict) else None
            if isinstance(v, dict) and isinstance(v.get("chu"), str):
                yield v["chu"]
    for r in a["phu"]["dong_chi_nhan"]["dong"]:
        if isinstance(r.get("nhan"), dict):
            yield r["nhan"]["chu"]


def test_R2_02_nhan_hang_anh_615_khong_con_chuoi_8_chu_so_va_7_hau_to_ten():
    import re
    a = _doc("ccr_daily_report")
    nhan = list(_chuoi_nhan(a))
    assert len(nhan) > 200                                                # Đ3: mẫu số ≠ 0 *(nhãn đã quét)*
    dai = [s for s in nhan if re.search(r"\d{8,}", s)]
    assert sum(1 for s in dai if "_PO USD" in s) == 0                     # đếm = 0: ⛔ còn số TK ở nhãn `PO USD` (mẫu số: 7 nhãn che ở dưới)
    # nhãn còn lại mang số ≥ 8 chữ số là nhãn TỔ CHỨC `R | <số>_<NH> <TT>_<pháp nhân>` — KQ-272 xếp "tổ chức", GIỮ; ghim đúng
    # SỐ ĐẾM *(Đ4: nhãn hàng, ⛔ số TK khác nhau)* ⇒ che nhầm thêm / sót đều ĐỎ (Đ5 hai chiều). Mở rộng che ⇒ chủ quyết riêng.
    assert len(dai) == 22 and all(s.startswith("R | ") for s in dai), len(dai)
    van = (F / "ccr_daily_report.json").read_text(encoding="utf-8")
    # HẬU TỐ `_<TÊN>` (cả tệp) = 0. ⚠ 7 tên ĐỨNG RIÊNG ở cột `ma`/`nhan_c` + `phu.dong_chi_nhan` ("20 > …") — hàng danh sách PO,
    # ⛔ kèm số TK, ⛔ phải hậu tố — NGOÀI phạm vi lệnh che *(ghi nhận ở BG-270 §R2, chờ chủ)*; ⛔ ghim là 0 ở đây.
    assert [h for h in HAU_TO_TEN if f"_{h}" in van] == []                # ⛔ còn hậu tố tên người
    che = sorted(int(m) for s in nhan for m in re.findall(r"^R \| TK_CA_NHAN_(\d+)_PO USD$", s))
    assert che == list(range(5, 12))                                      # DƯƠNG: 7 nhãn che, nối tiếp 5…11, giữ loại `PO USD`
    assert sum(1 for s in nhan if s.endswith("_CN")) == 4                 # 4 nhãn `_CN` cũ giữ nguyên (`TK_CA_NHAN_1…4`)
    for g in ("MSB", "OCBC", "TPCI", "ASTRONEX"):                         # nhãn TỔ CHỨC ⛔ bị che nhầm
        assert any(g in s for s in nhan), g


def test_R2_02_che_pii_nhan_PO_doi_ca_so_lan_ten_giu_loai_va_nhan_to_chuc():
    spec = importlib.util.spec_from_file_location("kh_dr_luoi_pii2", KH / "_dr_luoi.py")
    G = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = G
    spec.loader.exec_module(G)
    so1, so2, so3 = "5" * 16, "6" * 16, "9" * 12                           # dựng lúc chạy (⛔ số/mẫu nằm trong NGUỒN)
    ra = {"dong": [[f"R | {so1}_PO USD_ABCXY", f"R | {so2}_PO USD_QWERT", f"R | {so3}_OCBC SGD_SGO2"]],
          "phu": {"a": [f"R | {so1}_PO USD_ABCXY"]}}
    n = G.che_pii(ra)
    assert ra["dong"][0] == ["R | TK_CA_NHAN_1_PO USD", "R | TK_CA_NHAN_2_PO USD", f"R | {so3}_OCBC SGD_SGO2"]
    assert ra["phu"]["a"] == ["R | TK_CA_NHAN_1_PO USD"] and n == 2         # cùng số ⇒ cùng mã; tổ chức GIỮ
    s = repr(ra)
    assert "ABCXY" not in s and "QWERT" not in s and so1 not in s
