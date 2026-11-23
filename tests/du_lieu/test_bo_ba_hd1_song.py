"""`WO-353` — khuôn bộ ba HD1 *(C1 = ⓐ)* + chụp lại 615 · DR2 · số dư CÙNG lượt *(C3 = ⓐ)*, chủ 23/11.

Ghim *(Đ5 — mong khai, ĐỎ cả hai chiều; mỗi cổng mới có ca PHÁ ngay dưới nó)*:
  · 3 ảnh bộ ba sống `tests/fixture/{itl_ledge_adjustment,l1_canon,pm_join}_song_20261123.json` — checksum TÍNH LẠI từ nội dung
    *(`AnhChup` — ⛔ chỉ so chữ ghi sẵn)* = trường ghi sẵn = `do_voi_so_luong.MONG_SONG`; số dòng = mong của khuôn; PII.
  · `khoa_ghep` *(một hàm cho cả sổ và L1)* — chuẩn hoá đúng hai chỗ `ban_xuat_lam_hong` của ảnh tháng 8.
  · `ghep_theo_khoa` *(thay ảnh `classifying_vs_canon`)* — seq trùng theo thứ tự hàng sheet.
  · HD1 trên bộ ba sống *(`do(bo_ba="song")`)*: 16/23 kỳ đạt · 10.187/10.199 dòng ghép · ô parity — và tệp
    `voi_so_luong_song.json` = lần đo *(⛔ sửa tay)*. Cổng mặc định GIỮ bộ ba cũ *(5/23 — số đã ký)*.
  · 615 + DR2 chụp lại: khuôn `_song` ĐẠT trên ảnh; khuôn CŨ ĐỎ trên ảnh mới *(chứng vì sao cần khuôn mới)*.
"""
from __future__ import annotations

import copy
import datetime
import importlib.util
import json
import pathlib
import sys

import pytest

GOC = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC))
sys.path.insert(0, str(GOC / "tools"))

from fls.oracle.anh_chup import AnhChup  # noqa: E402

FX = GOC / "tests" / "fixture"
KH = GOC / "tools" / "khuon_dong_bang"
ANH = {"itl_ledge_adjustment": "itl_ledge_adjustment_song_20261123.json", "l1_canon": "l1_canon_song_20261123.json",
       "pm_join": "pm_join_song_20261123.json"}
#: (số dòng ảnh, checksum TÍNH LẠI) — đo lượt WO-353 23/11 12:11:50–12:17:22Z rồi khai.
MONG = {"itl_ledge_adjustment": (12722, "469daa90d9255072"), "l1_canon": (12601, "bb2386bf3696b0ac"),
        "pm_join": (3909, "51c6454d3d6e0d82")}


def _khuon(ten: str):
    import dong_bang_sheet as t
    return t, t.nap_khuon(ten)


def _anh(ten: str) -> dict:
    return json.loads((FX / ANH[ten]).read_text(encoding="utf-8"))


def _checksum_lai(anh: dict) -> str:
    phu = tuple({"phu": ten, "dong": r} for ten, b in anh.get("phu", {}).items() for r in b["dong"])
    return AnhChup(run_id=f"dong_bang_sheet:{anh['khuon']}", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _b():
    spec = importlib.util.spec_from_file_location("khuon_dong_bang__bo_ba_hd1", KH / "_bo_ba_hd1.py")
    m = sys.modules.get(spec.name)
    if m is None:
        m = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def dv():
    import tools.do_voi_so_luong as v
    return v


# ── AC-1 · ảnh bộ ba: số dòng · checksum TÍNH LẠI · khuôn ─────────────────────────────────────────────────────────
@pytest.mark.parametrize("ten", list(ANH))
def test_AC1_anh_bo_ba_so_dong_va_checksum_TINH_LAI(ten, dv):
    a = _anh(ten)
    n, cs = MONG[ten]
    assert a["khuon"] == ten and a["so_dong"] == len(a["dong"]) == n
    assert _checksum_lai(a) == a["checksum_noi_dung"] == cs == dv.MONG_SONG["checksum"][ANH[ten]]


@pytest.mark.parametrize("ten", list(ANH))
def test_AC1_PHA_doi_mot_o_thi_checksum_tinh_lai_DO(ten):
    a = _anh(ten)
    a["dong"][0] = {**a["dong"][0], a["cot"][2]: {"chu": "PHA"}}
    assert _checksum_lai(a) != MONG[ten][1]


def test_AC1_khuon_so_phan_bo_ky_DAT_va_PHA_mot_ky_thi_DO():
    t, k = _khuon("itl_ledge_adjustment")
    a = _anh("itl_ledge_adjustment")
    assert k.thieu_lac(a["dong"])["thieu"] == []
    m = sys.modules["khuon_dong_bang_itl_ledge_adjustment"]
    assert sum(m.MONG_KY.values()) == 12722 and len(m.MONG_KY) == 26          # = Σ cột A DT12 23/11 (Đ2)
    d = copy.deepcopy(a["dong"])
    d[0]["ky"] = {"chu": "2026-12"}                                            # PHÁ: một dòng đổi kỳ
    th = k.thieu_lac(d)["thieu"]
    assert any("2026-12" in x for x in th) and any(x.startswith("kỳ 2024-10") for x in th)


def test_AC1_khuon_khai_mong_rong_thi_DO_do_duoc():
    _t, k = _khuon("itl_ledge_adjustment")
    m = sys.modules["khuon_dong_bang_itl_ledge_adjustment"]
    goc = dict(m.MONG_KY)
    m.MONG_KY.clear()
    try:
        with pytest.raises(ValueError, match="MONG_KY"):
            k.thieu_lac(_anh("itl_ledge_adjustment")["dong"])
    finally:
        m.MONG_KY.update(goc)


# ── PII ─────────────────────────────────────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("ten", list(ANH))
def test_PII_anh_bo_ba_khong_mang_cot_rieng_tu_so_ct_dien_giai(ten):
    a = _anh(ten)
    cot = {c.casefold() for c in a["cot"]}
    assert not cot & {"email address", "số chứng từ", "diễn giải", "tên tài khoản", "số tài khoản", "ghi chú", "ps nợ", "ps có"}
    van = json.dumps(a["dong"], ensure_ascii=False)                 # GIÁ TRỊ ô *(câu khai `khong_mang_PII` nêu tên cột cấm — đúng)*
    assert "Email Address" not in van and "@" not in van


def test_PII_khuon_pm_TU_CHOI_ban_tho_mang_Email_hay_o_ngoai_14_vi_tri():
    _b()
    spec = importlib.util.spec_from_file_location("khuon_dong_bang_pm_join", KH / "pm_join.py")
    m = sys.modules.get(spec.name) or importlib.util.module_from_spec(spec)
    if spec.name not in sys.modules:
        sys.modules[spec.name] = m
        spec.loader.exec_module(m)
    from fls.adapters.pm_join import PM_TIEU_DE_MONG_DOI
    td = [PM_TIEU_DE_MONG_DOI.get(j, "") for j in range(29)]
    hang = [[None] * 29]
    hang[0][15], hang[0][16], hang[0][9], hang[0][8] = "PM1", "PM1-1", 10, "VND"
    assert len(m.chuan_bi({"tieu_de": td, "dong_dau": 3, "values": hang})["dong"]) == 1     # nền XANH
    td_e = list(td)
    td_e[1] = "Email Address"
    with pytest.raises(ValueError, match="riêng tư"):
        m.chuan_bi({"tieu_de": td_e, "dong_dau": 3, "values": hang})
    h2 = [list(hang[0])]
    h2[0][2] = "x"                                                     # ô ngoài 14 vị trí ⇒ bản thô ⛔ chiếu
    with pytest.raises(ValueError, match="chiếu"):
        m.chuan_bi({"tieu_de": td, "dong_dau": 3, "values": h2})


# ── khoa_ghep · ghép ────────────────────────────────────────────────────────────────────────────────────────────
def test_khoa_ghep_chuan_hoa_hai_cho_ban_xuat_lam_hong():
    b = _b()
    goc = [None, 4366190000000000, None, "VND", 2730128, None, 1121]
    assert b.khoa_ghep(goc) == b.khoa_ghep([None, "4.36619E+15", "x", " vnd ", "2,730,128.00", "", "1121"])
    assert b.khoa_ghep(goc) != b.khoa_ghep([None, 4366190000000000, None, "VND", 2730129, None, 1121])     # PHÁ: tiền
    assert b.khoa_ghep(goc) != b.khoa_ghep([None, 4366190000000000, None, "VND", None, 2730128, 1121])     # Nợ ≠ Có


def test_ghep_theo_khoa_seq_trung_theo_thu_tu_hang(dv):
    so = [(10, "k"), (11, "k"), (12, "z")]
    cn = [(7, "k"), (5, "k"), (9, "q")]
    assert dv.ghep_theo_khoa(so, cn) == {5: 10, 7: 11}                 # hàng nhỏ ↔ hàng nhỏ; z/q ⛔ cặp
    assert dv.ghep_theo_khoa(so, []) == {}


# ── HD1 trên bộ ba SỐNG — định nghĩa GIỮ, mẫu số GIỮ 23 kỳ ──────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def kq_song(dv):
    return dv.do(bo_ba="song")


def test_AC2_HD1_song_16_tren_23_ky_dat_va_10187_tren_10199_dong_ghep(kq_song, dv):
    h = kq_song["dat_hd1"]
    assert h["mau_so"]["so_ky"] == 23 and h["so_ky_dat"] == 16 and tuple(h["ky_dat"]) == dv.MONG_SONG["dat_hd1_theo_ky"]
    t = kq_song["tong"]
    assert (t["chay"], t["co"]) == (10187, 10199) and (t["o_parity_khop"], t["o_parity"]) == (71302, 71302)
    assert h["mau_so"]["dong_thieu"] == 12 and h["mau_so"]["dong_tu_soi_loai"] == 13
    assert kq_song["nguon"]["ngoai_mau_so"]["dong_so"] == {"2026-09": 737, "2026-10": 1038, "2026-11": 748}


def test_AC2_mau_so_GIU_23_ky_da_ky_va_cong_mac_dinh_GIU_bo_ba_cu(dv):
    old = json.loads((FX / "itl_ledge_adjustment.json").read_text(encoding="utf-8"))
    assert tuple(sorted(old["phan_bo_ky"])) == dv.KY_HD1                # 23 kỳ = phân bố kỳ của ảnh tháng 8
    assert dv.BO_BA_MAC_DINH == "cu"                                     # chuyển cổng = câu chủ, ⛔ Dev tự chuyển


def test_AC2_PHA_mong_song_thi_DO(dv, monkeypatch):
    monkeypatch.setitem(dv.MONG_SONG, "so_dong_ghep_canon", 10186)
    with pytest.raises(SystemExit, match="số dòng ghép canon: đo 10187 · mong 10186"):
        dv.do(bo_ba="song")


def test_AC2_tep_voi_so_luong_song_bang_lan_do(kq_song):
    tep = json.loads((GOC / "docs" / "ITL" / "_tools" / "voi_so_luong_song.json").read_text(encoding="utf-8"))
    assert tep == json.loads(json.dumps(kq_song, ensure_ascii=False))


def test_AC2_121_dong_so_khong_ghep_DUNG_la_121_hang_L1_bi_loai():
    """Dòng sổ ⛔ ghép *(cả 26 kỳ)* = 12.722 − 12.601 = **121** = số hàng `bank.nap` LOẠI *(khuôn `l1_canon` MONG `loai`)* —
    hai nguồn đếm cùng một số (Đ2). Danh tính *(khoá ghép = khoá hàng loại)* đo ở lượt đọc *(BG-346 §WO-353)*: bản thô ⛔ repo."""
    import tools.do_voi_so_luong as v
    so, cn = _anh("itl_ledge_adjustment"), _anh("l1_canon")
    u = v._o_song
    cap = v.ghep_theo_khoa([(int(u(r["dong_sheet"])), u(r["khoa_ghep"])) for r in so["dong"]],
                           [(int(u(r["dong_sheet"])), u(r["khoa_ghep"])) for r in cn["dong"]])
    _khuon("l1_canon")
    assert len(so["dong"]) - len(cap) == 121 == sys.modules["khuon_dong_bang_l1_canon"].MONG_BA_DUONG["loai"]
    assert len(cap) == len(cn["dong"]) == 12601                         # chiều ngược 0


# ── C3 · 615 + DR2 chụp lại CÙNG lượt ───────────────────────────────────────────────────────────────────────────
@pytest.mark.parametrize("khuon,tep,n", [("ccr_daily_report_song", "dap_an/ccr_daily_report_20261123.json", 2056),
                                        ("ccr_daily_report_2_song", "dau_vao/ccr_daily_report_2_20261123.json", 846)])
def test_AC3_anh_luot2_qua_khuon_song_DAT_va_khuon_CU_DO(khuon, tep, n):
    a = json.loads((FX / tep).read_text(encoding="utf-8"))
    assert a["khuon"] == khuon and a["so_dong"] == len(a["dong"]) == n and a["ngay_dong_bang"] == "2026-11-23"
    assert _checksum_lai(a) == a["checksum_noi_dung"]
    _t, k = _khuon(khuon)
    assert k.thieu_lac(a["dong"])["thieu"] == []
    _t, cu = _khuon(khuon.removesuffix("_song"))
    assert cu.thieu_lac(a["dong"])["thieu"]                             # khuôn 22/11 ĐỎ trên ảnh sống ⇒ vì sao cần khuôn mới


def test_AC3_cong_C5c_doc_bo_anh_cung_luot():
    import tools.do_hd2_c5c as c5c
    assert c5c._tep("ccr_daily_report") == "ccr_daily_report_20261123"
    assert {c5c._tep(t) for t in c5c.ANH_SO_DU} == {"ccr_so_du_ccr_20261123", "ccr_so_du_cash_20261123"}
    for t in ("ccr_daily_report_20261123", "ccr_so_du_ccr_20261123", "ccr_so_du_cash_20261123"):
        p = FX / ("dap_an" if t.startswith("ccr_daily") else "dau_vao") / f"{t}.json"
        assert json.loads(p.read_text(encoding="utf-8"))["ngay_dong_bang"] == "2026-11-23"


def test_dung_pm_tach_thuan_giu_luat_doc():
    from tools.nap_that import dung_pm
    hang = [[None] * 29, [None] * 29]
    hang[1][15], hang[1][16], hang[1][9], hang[1][8], hang[1][25] = "PM9", "PM9-1", "1,000.50", "USD", 4.36619e15
    ra = dung_pm([], hang)
    assert [x.dong_sheet for x in ra] == [3, 4]                          # hàng rỗng giữ chỗ — số hàng ⛔ trôi
    assert str(ra[1].tien) == "1000.50" and ra[1].ref == "4366190000000000" and ra[0].tien is None


def _cls_khop(sua=None) -> tuple[int, int]:
    """Phép của ảnh tháng 8 `classifying_vs_canon` *(`tests/ledger/test_classifying.py`: Classifying sổ = `iferror(<ô canon>, NTMI)`,
    68.915 ô · 100 %)* — chạy lại trên CẶP GHÉP sống. `sua` = hàm phá một ô canon *(ca ĐỎ)*."""
    import tools.do_voi_so_luong as v
    from fls.ledger.classifying import VI_TRI_CLASSIFYING, classifying
    u = v._o_song
    so = {int(u(r["dong_sheet"])): {k: u(x) for k, x in r.items()} for r in _anh("itl_ledge_adjustment")["dong"]}
    cn = {int(u(r["dong_sheet"])): {k: u(x) for k, x in r.items()} for r in _anh("l1_canon")["dong"]}
    if sua:
        sua(cn)
    cap = v.ghep_theo_khoa([(d, r["khoa_ghep"]) for d, r in so.items()], [(d, r["khoa_ghep"]) for d, r in cn.items()])
    tong = khop = 0
    for dc, ds in cap.items():
        for k, p in VI_TRI_CLASSIFYING.items():
            tong += 1
            khop += v._chuan(classifying(cn[dc][f"canon_pos_{p}"])) == v._chuan(so[ds][f"{k}_classifying"])
    return khop, tong


def test_AC2_classifying_so_BANG_iferror_canon_tren_cap_ghep_song():
    assert _cls_khop() == (88207, 88207)                       # 12.601 cặp × 7 khối; mẫu số > 0 (Đ3)


def test_AC2_PHA_doi_mot_o_canon_thi_classifying_LECH():
    def pha(cn):
        d = min(cn)
        cn[d]["canon_pos_18"] = "PHA | Pha"                      # khối hd *(S)*
    assert _cls_khop(pha) == (88206, 88207)
