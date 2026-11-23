# -*- coding: utf-8 -*-
"""WO-338 — bể GIỮ RIÊNG cho A2.04: dựng · độc lập · riêng tư · A ↔ B. Nguồn GIẢ (⛔ sheet, ⛔ API).

Mỗi bài khai `mong` TRƯỚC (Đ5) và có phép chứng minh tập KHÔNG RỖNG (Đ3). Bài trên bể THẬT chỉ chạy khi
`FLS_HELDOUT_NOI_DUNG` trỏ tới thư mục có `a/` + `b/` (⛔ in mẫu — chỉ SỐ ĐẾM); thiếu ⇒ SKIP có lý do.
"""
from __future__ import annotations

import datetime as dt
import json
import os
import stat
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))

import dung_be_giu_rieng as dbg  # noqa: E402
import do_ro_ri_che as rr  # noqa: E402
import fleet_eval_voi as fe  # noqa: E402

EPOCH = dt.date(1899, 12, 30)
CHOT_GIA = {f"2025-{m:02d}" for m in range(1, 13)} | {"2026-01", "2026-02", "2026-03"}     # kỳ chốt ảnh (giả)
KY_MO = {"2026-11"}
TENS = ["NGUYEN VAN AN", "TRAN THI BICH", "LE MINH TUAN", "PHAM QUOC HUY"]


def _serial(ky: str, ngay: int = 10) -> int:
    y, m = int(ky[:4]), int(ky[5:])
    return (dt.date(y, m, ngay) - EPOCH).days


def nguon_gia() -> dict:
    """Nguồn GIẢ có đủ MỌI tầng ở cả kỳ chốt lẫn kỳ mở. Mỗi mã một `REFxxxxx` (≥ 8 ký tự ⇒ khớp mẫu token)."""
    l1, pm = [], []
    kys = sorted(CHOT_GIA) + ["2026-10"]                 # kỳ chuyển = 2026-10 ⛔ thuộc ảnh ⇒ B chốt, A ⛔ có

    def bank(ky, ref, nd, cur, tien, line=None, co=True):
        r = [_serial(ky), ref, nd, cur, None if co else tien, tien if co else None, "TK"] + [None] * 6 + [line or "#N/A"]
        l1.append(r)

    def lenh(ky, ref, line, cur, tien):
        r = [None] * 26
        r[0], r[8], r[9], r[15], r[16], r[24], r[25] = _serial(ky), cur, tien, "S" + line, line, "Done", ref
        pm.append(r)

    n = 0

    def moi():
        nonlocal n
        n += 1
        return n
    for ky in kys + sorted(KY_MO):
        for i in range(3):
            # A
            k = moi(); ref, line = f"REFA{k:05d}", f"PMA{k:05d}-1"
            nd = f"CHUYEN TIEN {TENS[k % 4]} email a{k}@mail.vn so TK 0123456{k:03d}"
            bank(ky, ref, nd, "VND", 1_000_000 + k * 1000, line); lenh(ky, ref, line, "VND", 1_000_000 + k * 1000)
        for i in range(2):                               # B: 1 bank × 2 PM
            k = moi(); ref = f"REFB{k:05d}"
            bank(ky, ref, "TRA 2 LENH", "VND", 3_000_000 + k, f"PMB{k:05d}-1")
            lenh(ky, ref, f"PMB{k:05d}-1", "VND", 1_000_000); lenh(ky, ref, f"PMB{k:05d}-2", "VND", 2_000_000 + k)
        for i in range(2):                               # C: 2 bank × 1 PM
            k = moi(); ref = f"REFC{k:05d}"
            bank(ky, ref, "TRA LAN 1", "VND", 500_000, f"PMC{k:05d}-1"); bank(ky, ref, "TRA LAN 2", "VND", 500_000 + k * 0, f"PMC{k:05d}-1")
            lenh(ky, ref, f"PMC{k:05d}-1", "VND", 1_000_000)
        k = moi(); ref = f"REFD{k:05d}"                  # D: 2 × 2
        for j in range(2):
            bank(ky, ref, "N x M", "VND", 1_000_000, f"PMD{k:05d}-{j}"); lenh(ky, ref, f"PMD{k:05d}-{j}", "VND", 1_000_000)
        for i in range(2):                               # E: khác tiền tệ
            k = moi(); ref = f"REFE{k:05d}"
            bank(ky, ref, "USD vs VND", "USD", 100 + k, f"PME{k:05d}-1"); lenh(ky, ref, f"PME{k:05d}-1", "VND", 2_500_000 + k)
        for i in range(2):                               # F: Σ lệch
            k = moi(); ref = f"REFF{k:05d}"
            bank(ky, ref, "LECH", "VND", 2_000_000 + 5000, f"PMF{k:05d}-1"); lenh(ky, ref, f"PMF{k:05d}-1", "VND", 2_000_000)
        for i in range(2):                               # L3 không Ref
            k = moi(); bank(ky, "", f"{TENS[k % 4]} chuyen khoan", "VND", 777_000 + k)
        for i in range(2):                               # L3 nội dung ghi mã PM khác
            k = moi(); ref_pm = f"REFL{k:05d}"
            lenh(ky, ref_pm, f"PML{k:05d}-1", "VND", 888_000 + k)
            bank(ky, f"BANKX{k:05d}", f"THANH TOAN {ref_pm} CHO NCC", "VND", 888_000 + k)
    pt = ["Timestamp", "Email Address", "Loại giao dịch (Payment Type)", "ID PELine - Nội dung PE (Advance)",
          "ID PELine - Nội dung PE (Urgent)", "ID PILine - Nội dung PI", "Pháp nhân thanh toán",
          "Nội dung giao dịch nhập khi ", "Đơn vị tiền tệ (Currency)", "Tổng số tiền thanh toán (Transaction Amount)",
          "Ngân hàng", "Chi nhánh", "Số tài khoản", "Tên tài khoản", "Ghi chú (nếu có)", "ID PMSlip", "ID PMLine", "ID PESlip",
          "ID PELine", "ID PISlip", "ID PILine", "Budget Code (HDCode)", "Chủ dự toán (CDT1)", "Chủ dự toán *", "Status_Final",
          "Reference number"]
    ld = ["Ngày chứng từ", "Số chứng từ", "Diễn giải", "Đơn vị tiền tệ", "PS Nợ", "PS Có", "Tài khoản", "", "", "", "", "", "", "ID PMLine"]
    return {"ngay_doc": "2026-11-23", "l1": l1, "pm": pm, "pm_tieu_de": pt, "l1_tieu_de": ld,
            "ledge_ngay": [_serial(k) for k in sorted(CHOT_GIA | KY_MO | {"2026-10"})]}


@pytest.fixture(scope="module")
def nguon():
    return nguon_gia()


@pytest.fixture(scope="module")
def be_a(nguon):
    return dbg.dung_be(nguon, ten="a", ky_chot_dong_bang=CHOT_GIA, ky_mo_ngay_chay=KY_MO)


@pytest.fixture(scope="module")
def be_b(nguon):
    return dbg.dung_be(nguon, ten="b", ky_chot_dong_bang=CHOT_GIA, ky_mo_ngay_chay=KY_MO)


# ───────────── AC-1 · dựng bể, `mong` từng tầng ─────────────
def test_tieu_de_nguon_gia_dung(nguon):
    assert dbg.kiem_tieu_de(nguon) == []


def test_MONG_tung_tang_A(be_a):
    assert be_a["thieu"] == {}, be_a["thieu"]
    assert be_a["dem"] == dbg.MONG_TANG                       # D5 E10 F10 C10 B5 A10 L3 5+5 chuyển 5
    assert len(be_a["ca"]["ca"]) == sum(dbg.MONG_TANG.values()) == 65


def test_MONG_tung_tang_B_them_chua_chot(be_b):
    assert be_b["thieu"] == {}, be_b["thieu"]
    assert be_b["dem"] == dbg.MONG_TANG | {"chua_chot": 5}
    assert len(be_b["ca"]["ca"]) == 70


def test_tang_ra_DO_khi_thieu_hai_chieu(nguon):
    """Đ5: thiếu D (hết mã hình D) ⇒ ĐỎ có tên tầng — ⛔ lặng lẽ ít hơn mong."""
    n2 = dict(nguon)
    n2["l1"] = [r for r in nguon["l1"] if not str(r[1]).startswith("REFD")]
    n2["pm"] = [r for r in nguon["pm"] if not str(r[25]).startswith("REFD")]
    b = dbg.dung_be(n2, ten="a", ky_chot_dong_bang=CHOT_GIA, ky_mo_ngay_chay=KY_MO)
    assert "D" in b["thieu"] and b["dem"]["D"] == 0


def test_ca_A_chi_tu_ky_da_chot_va_chuyen_la_ky_moi_nhat(be_a):
    ky = {m["ky"] for m in be_a["meta"].values()}
    assert ky <= CHOT_GIA                                      # ⛔ kỳ ngoài ảnh đóng băng, ⛔ kỳ mở
    assert {m["ky"] for m in be_a["meta"].values() if m["tang"] == "chuyen"} == {max(CHOT_GIA)}
    assert not any(m["tang"] != "chuyen" and m["ky"] == max(CHOT_GIA) for m in be_a["meta"].values())


def test_B_ky_mo_gan_nhan_chua_chot_va_tach_khoi_recall(be_b):
    ck = {c for c, d in be_b["dap_an"]["noi"].items() if d["nhom"] == "chua_chot"}
    assert len(ck) == 5 and all(be_b["meta"][c]["ky"] in KY_MO for c in ck)
    assert not any(m["ky"] in KY_MO for c, m in be_b["meta"].items() if c not in ck)
    assert "chua_chot" not in {d["nhom"] for c, d in be_b["dap_an"]["noi"].items() if c not in ck}


def test_dap_an_phai_noi_nam_trong_ung_vien_va_la_bi_danh(be_a, nguon):
    ca, dap = be_a["ca"]["ca"], be_a["dap_an"]["noi"]
    pn = [c for c, d in dap.items() if d["nhom"] == "phai_noi"]
    assert len(pn) == 25 + 5 - 5 + 0 or len(pn) > 0                # có mẫu (⛔ rỗng)
    for c in pn:
        assert dap[c]["chon"].startswith("PM-") and dap[c]["chon"] in {u["pm"] for u in ca[c]["ung_vien"]}
    pc = [c for c, d in dap.items() if d["nhom"] in ("phai_nguoi", "l3")]
    assert pc and all(dap[c]["chon"] == dbg.DE_NGUOI for c in pc)
    txt = json.dumps(ca, ensure_ascii=False)
    assert "PMA0" not in txt and "PMB0" not in txt             # mã dòng lệnh chi THẬT ⛔ vào ca (chỉ bí danh)


def test_bi_danh_khong_co_chu_so_vi_lop2_che_nham_la_so_TK():
    """Ghim lỗi đo 23/11: bí danh hex toàn chữ số bị `che.kiem_den` chặn cả lời gọi."""
    import re as _re
    from fls.agent import che
    bd = [dbg.alias_pm(bytes([i % 251]) * 16, f"L{i}") for i in range(3000)]
    assert len(set(bd)) > 2990 and all(_re.fullmatch(r"PM-[A-Z]{10}", x) for x in bd)
    assert che.kiem_den({"messages": [{"role": "user", "content": " ".join(bd)}]}) == []
    assert dbg.alias_pm(b"k" * 16, "L1") != dbg.alias_pm(b"j" * 16, "L1")           # phụ thuộc muối


def test_vi_tri_ung_vien_dung_khong_lo(be_a):
    vt = [next(i for i, u in enumerate(be_a["ca"]["ca"][c]["ung_vien"]) if u["pm"] == d["chon"])
          for c, d in be_a["dap_an"]["noi"].items() if d["nhom"] == "phai_noi"]
    assert len(set(vt)) > 1                                     # xáo: ⛔ luôn đứng đầu


def test_id_ca_khong_lo_tang(be_a):
    thu_tu = [be_a["meta"][c]["tang"] for c in sorted(be_a["meta"])]
    assert thu_tu != sorted(thu_tu)


def test_dap_an_mau_thuan_bi_loai_va_dem(nguon):
    """Mapping L1 ghi một dòng KHÁC pm_join ⇒ ca bị loại, đếm `dap_an_mau_thuan` (⛔ im lặng)."""
    n2 = dict(nguon)
    n2["l1"] = [list(r) for r in nguon["l1"]]
    for r in n2["l1"]:
        if str(r[1]).startswith("REFA"):
            r[13] = "PM-KHAC-1"
    ung, th = dbg.phan_tang(*(dbg.doc_bank(n2)[0], dbg.doc_pm(n2)[0]))
    assert th["loai"].get("A:dap_an_mau_thuan", 0) > 0 and not [u for u in ung if u.tang == "A"]


# ───────────── AC-2 · độc lập ─────────────
def test_doc_lap_ca_dung_va_prompt_bang_0_va_phep_do_khong_rong(be_a, be_b):
    assert dbg.so_tep_prompt() > 0                             # Đ3: tập prompt quét KHÔNG rỗng
    for b in (be_a, be_b):
        assert dbg.trung_voi_ca_dung(b["ca"]) == 0
        assert dbg.trung_voi_prompt(b["ca"]) == 0


def test_phep_trung_CAN_duoc_khi_cay_ca_trung(be_a):
    """Chứng minh ĐỎ: cấy MỘT ca có nội dung của ca dựng WO-329 ⇒ đếm = 1."""
    dung = json.loads(dbg.TEP_CA_DUNG.read_text(encoding="utf-8"))["ca"]
    nd = next(c["noi_dung"] for c in dung.values() if c.get("noi_dung"))
    ca = json.loads(json.dumps(be_a["ca"]))
    ca["ca"]["c001"]["noi_dung"] = nd
    assert dbg.trung_voi_ca_dung(ca) == 1


def test_phep_trung_prompt_CAN_duoc_khi_cay_noi_dung_prompt(be_a, tmp_path):
    (tmp_path / "p.md").write_text("vi du: THANH TOAN CHO NHA CUNG CAP ABC", encoding="utf-8")
    ca = {"ca": {"x": {"tien": 1, "cur": "VND", "ngay": "2026-01-01", "noi_dung": "thanh toan cho nha cung cap abc"}}}
    assert dbg.trung_voi_prompt(ca, tmp_path) == 1


# ───────────── AC-1/AC-4 · ghi NGOÀI repo, chmod 600, repo chỉ đếm ─────────────
def test_ghi_be_chmod_600_va_cam_trong_repo(be_a, tmp_path):
    d = dbg.ghi_be(tmp_path, be_a)
    assert stat.S_IMODE(d.stat().st_mode) == 0o700
    tep = sorted(d.iterdir())
    assert {p.name for p in tep} == {"ca.json", "dap_an.json", "meta.json", "muoi.key"}
    assert all(stat.S_IMODE(p.stat().st_mode) == 0o600 for p in tep)
    assert dbg.main(["--tu-tep", str(tmp_path / "x.json"), "--ra", str(GOC / "docs" / "be_cam")]) == 2   # trong repo ⇒ ⛔


def test_tep_dem_chi_dem_khong_noi_dung(be_a):
    dem = dbg.dem_cua(be_a, None)
    txt = json.dumps(dem, ensure_ascii=False)
    for ten in TENS:
        assert ten not in txt
    assert "@mail.vn" not in txt and "0123456" not in txt
    assert "noi_dung" not in txt and "REFA" not in txt
    assert dem["tong_ca"] == 65 and len(dem["van_tay_ca"]) == 65 and len(dem["van_tay_be"]) == 16


def test_van_tay_phu_thuoc_muoi(be_a):
    c = next(iter(be_a["ca"]["ca"].values()))
    assert dbg.van_tay_ca(c, b"a" * 16) != dbg.van_tay_ca(c, b"b" * 16)


# ───────────── AC-4 · bộ che ─────────────
def test_che_0_lot_tren_mau_gia_va_bo_do_ko_rong(be_a, be_b):
    for b in (be_a, be_b):
        r = rr.do(b["ca"], b["meta"])
        assert r["mau_so_noi_dung"] > 0 and r["hop_le"], r              # Đ3: dò THẤY gì đó trên chữ chưa che
        assert sum(r["truoc_che"].values()) > 0
        assert r["sau_che"] == {"email": 0, "so_tk": 0, "so_chung_tu": 0, "ten_ung_vien": 0}, r
        assert r["ca_bi_lop2_chan"] == 0


def test_bo_do_ten_bat_duoc_ten_co_dau_va_chu_thuong_ten():
    """Chứng minh bộ dò ĐỎ trên thứ nó phải bắt (và `che_noi_dung` hiện ⛔ bắt tên CÓ DẤU — khai ở BG-339)."""
    assert rr.dem_ten("Chuyen tien Nguyễn Văn An thanh toan") == 1
    assert rr.dem_ten("CK NGUYEN VAN A") == 1
    assert rr.dem_ten("thanh toan hoa don thang 5") == 0


def test_bo_do_so_tk_bat_day_xen_cach_ma_che_6_chu_so_lien_bo_sot():
    assert rr.dem_mot("TK 0123 4567 89", None)["so_tk"] == 1
    assert rr.dem_mot("so 12345", None)["so_tk"] == 0


def test_bo_do_so_chung_tu_bat_khi_con_nguyen():
    assert rr.dem_mot("FT26123ABC456", "FT26123ABC456")["so_chung_tu"] == 1
    assert rr.dem_mot("<SO>", "FT26123ABC456")["so_chung_tu"] == 0


# ───────────── AC-3 · fleet eval trên bể (GIẢ) ─────────────
@pytest.fixture(scope="module")
def pool_gia(be_a, be_b, tmp_path_factory):
    g = tmp_path_factory.mktemp("heldout")
    dbg.ghi_be(g, be_a)
    dbg.ghi_be(g, be_b)
    return g


def test_chay_be_chi_so_va_chua_chot_khong_vao_recall(pool_gia):
    kq = fe.chay_be(pool_gia / "b")
    n_pn = sum(1 for d in json.loads((pool_gia / "b" / "dap_an.json").read_text())["noi"].values() if d["nhom"] == "phai_noi")
    assert "loi" not in kq and [v["phien_ban"] for v in kq["vong"]] == [m for m, _, _ in fe.VONG]
    for v in kq["vong"]:
        t = v["be"]
        assert t["mau_so_chinh"] == 65 and t["chua_chot"]["so_ca"] == 5       # 70 ca − 5 chưa chốt
        assert t["so_phai_noi"] == n_pn >= 25          # A10 + B5 + C10 (+ ca chuyển hình A·B·C — nhóm theo ĐÁP ÁN)
    v0, v2, v3 = (v["be"] for v in kq["vong"])
    assert v0["so_noi"] == 0 and v0["phai_nguoi_bi_noi"] == 0
    assert v3["so_noi"] >= v2["so_noi"]


def test_chay_chuoi_be_dung_duong_o_ca_hai_co_noi_dung(pool_gia):
    for c in ("a", "b"):
        for cho in (False, True):
            r = fe.chay_chuoi_be(pool_gia / c, cho)
            assert "loi" not in r, r
            assert r["mau_so"] > 0 and r["khop"] + r["lech"] <= r["mau_so"]
            assert r["g0"]["so_ca"] == len(json.loads((pool_gia / c / "ca.json").read_text())["ca"])


def test_main_be_DO_khi_khong_co_be(monkeypatch):
    monkeypatch.delenv(fe.BIEN_BE, raising=False)
    assert fe.main_be(False) == 2                                              # Đ5: ⛔ đo được ⇒ ĐỎ, ⛔ xanh


def test_doi_chieu_ky_lech_co_ten():
    """Ledge sống thiếu/thừa dòng ở một kỳ so với ảnh đóng băng ⇒ kỳ ĐƯỢC KÊ TÊN (⛔ 'không thấy lệch')."""
    dong_bang = json.loads(dbg.TEP_KY_DONG_BANG.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"]
    song = [_serial(k) for k, n in dong_bang.items() for _ in range(n)]
    assert dbg.doi_chieu_ky(song)["ky_lech_so_dong"] == {}                     # mẫu số = tổng ảnh ⇒ KHỚP
    song2 = song + [_serial("2025-05")]
    dc = dbg.doi_chieu_ky(song2)
    assert set(dc["ky_lech_so_dong"]) == {"2025-05"} and dc["mau_so_o_ngay_song"] == sum(dong_bang.values()) + 1


def test_ky_chot_dong_bang_bo_ky_moi_nhat():
    ks = sorted(json.loads(dbg.TEP_KY_DONG_BANG.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"])
    assert dbg.ky_chot_dong_bang() == set(ks[:-1]) and ks[-1] not in dbg.ky_chot_dong_bang()


# ───────────── bể THẬT (chỉ khi có `FLS_HELDOUT_NOI_DUNG`) — ⛔ in mẫu ─────────────
_TM = os.environ.get(dbg.BIEN)
_CO_BE = bool(_TM) and (Path(_TM) / "a" / "ca.json").exists() and (Path(_TM) / "b" / "ca.json").exists()
THAT = pytest.mark.skipif(not _CO_BE, reason=f"không có bể giữ riêng (${dbg.BIEN}) — bể thật nằm NGOÀI repo")


@THAT
@pytest.mark.parametrize("c", ["a", "b"])
def test_BE_THAT_che_0_lot(c):
    d = Path(_TM) / c
    r = rr.do(json.loads((d / "ca.json").read_text(encoding="utf-8")), json.loads((d / "meta.json").read_text(encoding="utf-8")))
    assert r["hop_le"], f"bộ dò ⛔ thấy gì trên chữ chưa che (mẫu số {r['mau_so_noi_dung']}) — phép đo vô nghĩa"
    assert r["sau_che"] == {"email": 0, "so_tk": 0, "so_chung_tu": 0, "ten_ung_vien": 0}, {"sau": r["sau_che"], "truoc": r["truoc_che"]}
    assert r["ca_bi_lop2_chan"] == 0


@THAT
@pytest.mark.parametrize("c", ["a", "b"])
def test_BE_THAT_mong_va_doc_lap(c):
    d = Path(_TM) / c
    ca = json.loads((d / "ca.json").read_text(encoding="utf-8"))
    mong = sum(dbg.MONG_TANG.values()) + (dbg.MONG_CHUA_CHOT if c == "b" else 0)
    assert len(ca["ca"]) == mong
    assert dbg.trung_voi_ca_dung(ca) == 0 and dbg.trung_voi_prompt(ca) == 0


@THAT
def test_BE_THAT_van_tay_khop_tep_dem_repo():
    dem = json.loads(dbg.TEP_DEM.read_text(encoding="utf-8"))
    for c in ("a", "b"):
        d = Path(_TM) / c
        ca = json.loads((d / "ca.json").read_text(encoding="utf-8"))
        muoi = (d / "muoi.key").read_bytes()
        vt = sorted(dbg.van_tay_ca(x, muoi) for x in ca["ca"].values())
        assert vt == dem["be"][c]["van_tay_ca"]
