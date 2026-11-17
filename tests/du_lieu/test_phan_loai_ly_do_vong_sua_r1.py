# -*- coding: utf-8 -*-
"""DT1b — vòng sửa sau R1 (`KQ-097`): bài cho 5 NÊN SỬA + GHI NHẬN rẻ, đưa vào `tests/du_lieu/`.

ISP 3.1.2 · Step 5 · DT1b · `BG-096` · `KQ-097` §Bài thử đề xuất ①–⑭ · sổ `SO_PHAT_HIEN_ISP-3.1_DT1b.md`.

Hai nhóm (giữ phân biệt của R1):
  · `test_R1_*`         — XANH trên `8a18599` (mã Dev), ĐỎ trên ĐỘT BIẾN BIÊN mà 48 bài gốc ⛔ bắt
    (mỗi bài ghi đột biến nó GIẾT — `DT1b-R1-01` ①–⑥ · `-02` ⑦⑧ · `-03` ⑨–⑫). Chúng ⛔ đổi hành vi mã,
    chỉ KHOÁ hành vi đúng đang có.
  · `test_R1_DE_XUAT_*`  — ĐỎ trên `8a18599` (chính là phát hiện `-04` ⑬ · `-05` ⑭ · `-06`), XANH sau khi
    sửa mã theo khuyến nghị. Chứng minh RED-first ở `KQ-098`/tin nhắn phiên.

⚠ Lệch CÓ Ý so với §Bài thử đề xuất của `KQ-097` (ghi để R2 đối chiếu, ⛔ im):
  · ⑬ case `nguon_ban_doc_sha_la_SoCT`: §KQ-097 cấy Số CT 16 CHỮ SỐ `4366191234567890` — nhưng chuỗi ấy
    KHỚP `MAU_HEX16` (`^[0-9a-f]{16}$`, 16 chữ số đều là hex) ⇒ cổng canh MẪU hex16 ⛔ bắt được nó, bài sẽ
    XANH-GIẢ sau sửa. Dùng mã ngân hàng `FT25123456789` (có `F`·`T` ⇒ ⛔ hex) để bài THẬT đo "mẫu hex16 bị ép".
    Giới hạn còn lại (Số CT 16 chữ số thập phân ở `ban_doc_sha256_16` ⛔ phân biệt được với sha ở chế độ cổng)
    khai ở BG §Vòng sửa sau R1 (KQ-097) và docstring công cụ (R7).
"""
from __future__ import annotations

import json
import subprocess

import pytest

from tests.du_lieu import test_phan_loai_ly_do as g


def _t():
    return g._tool()


MONG = dict(g.MONG_TONG_HOP)


# ═══ DT1b-R1-01 · lõi ghép theo NHÓM KHOÁ — nhánh bộ dựng `_dung` ⛔ chạm ════════════════════════
def test_R1_seq_MOT_PHAN_dong_thieu_dau_KHOP_dong_sau_TRUNG_SEQ():
    """Giết D01 (tất-cả-hoặc-không) · D02 (đảo thứ tự seq). Bộ dựng chỉ có nhóm 1 dòng thiếu."""
    K = ("A1", "100", "0", "1121", "VND")
    nh, tl = _t().phan_loai({1: K, 2: K, 3: K, 4: K}, {101: K, 102: K, 103: K}, [4, 2, 3])
    assert {d: (v["nhan"], v["ghi_chu"]) for d, v in nh.items()} == {
        2: ("KHAC", "KHOP_KHI_GHEP_LAI"), 3: ("KHAC", "KHOP_KHI_GHEP_LAI"), 4: ("TRUNG_SEQ", None)}
    assert tl == 1


def test_R1_dong_L1_do_dong_KHOP_giu_cho_KHONG_la_ung_vien():
    """Giết D04 (dòng L1 'chưa ai ghép' trừ dòng ĐÃ ghép thay vì mọi dòng sổ)."""
    KX, KY = ("B1", "100", "0", "1121", "VND"), ("B1", "200", "0", "1121", "VND")
    nh, _ = _t().phan_loai({11: KX, 12: KY}, {201: KX}, [11, 12])
    assert (nh[11]["nhan"], nh[11]["ghi_chu"]) == ("KHAC", "KHOP_KHI_GHEP_LAI")
    assert (nh[12]["nhan"], nh[12]["lech"]) == ("KHONG_CO_SAO_KE", [])


def test_R1_ung_vien_IT_LECH_nhat_va_HOA_theo_khoa_nho_nhat():
    """Giết D07 (max thay min) · D08 (hoà theo thứ tự set — đổi theo PYTHONHASHSEED; 12 dòng ⇒ 2⁻¹² lọt)."""
    so, l1, thieu = {}, {}, []
    for i in range(12):
        ct = f"C{i:02d}"
        so[i] = (ct, "500", "0", "1121", "VND")
        thieu.append(i)
        l1[1000 + 3 * i] = (ct, "501", "0", "1121", "VND")      # lệch ps_no
        l1[1001 + 3 * i] = (ct, "500", "0", "1122", "VND")      # lệch tk — hoà, khoá nhỏ hơn ('500' < '501')
        l1[1002 + 3 * i] = (ct, "999", "7", "9999", "USD")      # lệch 4 trường
    nh, _ = _t().phan_loai(so, l1, thieu)
    assert {d: v["lech"] for d, v in nh.items()} == {i: ["tk"] for i in range(12)}


def test_R1_so_ct_RONG_va_khoa_HONG_khong_la_cau_ung_vien():
    """Giết D05+D06 (cùng lúc — riêng từng cái là đột biến TƯƠNG ĐƯƠNG) · D11 (L1 đếm cả khoá hỏng)."""
    nh, _ = _t().phan_loai({31: ("", "300", "0", "1121", "VND"), 41: ("D1", "600", "0", "1121", "VND")},
                           {401: ("", "999", "0", "1121", "VND"), 501: ("D1", None, "0", "1121", "VND")},
                           [31, 41])
    assert nh[31]["nhan"] == nh[41]["nhan"] == "KHONG_CO_SAO_KE"


def test_R1_o_loi_PS_CO_la_KHOA_HONG_ps_co():
    """Giết D15 (KHOA_HONG chỉ xét PS Nợ) — bộ dựng chỉ có ô lỗi ở PS Nợ."""
    t = _t()
    nh, _ = t.phan_loai({51: t.chuan_hoa_khoa("E1", "", "#N/A", "1121", "VND")}, {}, [51])
    assert (nh[51]["nhan"], nh[51]["ghi_chu"]) == ("KHAC", "KHOA_HONG:ps_co")


def test_R1_TK_go_trang_va_chu_hoa():
    """Giết D13 · D14 — bộ dựng chỉ có TK 4 chữ số, ⛔ trắng, ⛔ chữ."""
    t = _t()
    assert t.chuan_hoa_khoa("X1", "1", "", " 1121a ", "VND") == t.chuan_hoa_khoa("X1", "1", "", "1121A", "VND")


# ═══ DT1b-R1-02 · R5 / R6 / R3 — mỗi vế một ca phá RIÊNG (luật `DT1a-R1-03`) ═════════════════════
def _dt1a_ky(tmp_path, gia_tri):
    d = json.loads(g.DT1A.read_text(encoding="utf-8"))
    dau = g._nen()[1][0]
    vt = [j for j, x in enumerate(d["dong_thieu"]) if x["dong_sheet"] == dau]
    assert len(vt) == 1
    d["dong_thieu"][vt[0]]["ky"] = gia_tri
    p = tmp_path / "dt1a_ban.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return p


@pytest.mark.parametrize("ten", ["tien", "so_ct_khoa_hoc_THO", "so_ct_CHUAN_HOA"])
def test_R1_R5_moi_dang_bi_chan_tren_duong_do_that(tmp_path, monkeypatch, capsys, ten):
    """Giết D17 (bỏ nửa TIỀN) · D19 (bỏ dạng THÔ) · D18 (bỏ dạng CHUẨN HOÁ)."""
    van_ban, _, tin = g._dung(7)
    if ten == "tien":
        ban, cau = sorted(tin["tien"])[0], "riêng tư: số tiền"
    elif ten == "so_ct_khoa_hoc_THO":
        ban, cau = sorted(c for c in tin["so_ct_tho"] if "E+" in c)[0], "riêng tư: Số chứng từ"
    else:   # Số CT thô KHÁC dạng chuẩn hoá (thường + gạch + trắng) ở dòng thiếu đầu; cấy dạng CHUẨN HOÁ
        dau = g._nen()[1][0]
        hang = van_ban.splitlines()
        i = next(j for j, x in enumerate(hang) if x.startswith(f"SO,{dau},"))
        cot = hang[i].split(",")
        cot[2] = "syn-x 12345"
        hang[i] = ",".join(cot)
        van_ban = "\n".join(hang) + "\n"
        ban, cau = "SYNX12345", "riêng tư: Số chứng từ"
    p = g._ghi_csv(tmp_path, van_ban)
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra,
                                 dt1a=_dt1a_ky(tmp_path, ban), mong_nhan=dict(MONG))
    assert ma == 1, (ten, out)
    assert cau in err, err
    assert not ra.exists()


PHA_R1 = [
    ("nguon_thua", lambda d: d["nguon"].update(them="x"), "khoá ngoài lược đồ ở nguon"),          # giết D30
    ("mau_so_thua", lambda d: d["mau_so"].update(them=1), "khoá ngoài lược đồ ở mau_so"),         # giết D31
    ("khoa_cam_So_chung_tu", lambda d: d["mau_so"]["khoa_hong"].update({"Số chứng từ": 1}), "riêng tư: khoá cấm"),  # D20
    ("khoa_cam_Email", lambda d: d["mau_so"]["khoa_hong"].update({"Email": 1}), "riêng tư: khoá cấm"),             # D21
    ("email_o_TEN_khoa", lambda d: d["mau_so"]["khoa_hong"].update({"ke-toan@vi-du.vn": 1}), "riêng tư: email"),   # D22
]


@pytest.mark.parametrize("ten, pha, cau", PHA_R1, ids=[p[0] for p in PHA_R1])
def test_R1_bat_bien_tep_nhan_CAN_tren_ban_sao(tmp_path, monkeypatch, capsys, ten, pha, cau):
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(goc, encoding="utf-8")
    assert g._kiem_tep(monkeypatch, capsys, sao, tmp_path)[0] == 0
    d = json.loads(goc)
    pha(d)
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)
    assert cau in err, err


# ═══ DT1b-R1-03 · đọc bản đọc · ghi hiện vật ════════════════════════════════════════════════════
def test_R1_hang_TRANG_kieu_Excel_duoc_bo_qua(tmp_path, monkeypatch, capsys):
    """Giết D23. Excel hay xuất hàng chỉ có dấu phẩy ở cuối vùng đã chạm."""
    van_ban, _, _ = g._dung(7)
    p = g._ghi_csv(tmp_path, van_ban + ",,,,,,\n,,,,,,\n")
    ma, _, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), ra=tmp_path / "ra.json", mong_nhan=dict(MONG))
    assert ma == 0, err


def test_R1_cot_LAP_la_DO(tmp_path, monkeypatch, capsys):
    """Giết D24 — cột `tk` lặp: bản đầu dùng ÂM THẦM cột đầu."""
    van_ban, _, _ = g._dung(7)
    h = van_ban.splitlines()
    p = g._ghi_csv(tmp_path, "\n".join([h[0] + ",tk"] + [x + ",9999" for x in h[1:]]) + "\n")
    ra = tmp_path / "ra.json"
    ma, _, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, mong_nhan=dict(MONG))
    assert ma == 1 and "lặp ['tk']" in err, err
    assert not ra.exists()


def test_R1_ghi_qua_TEP_TAM_hong_luc_thay_thi_dich_NGUYEN(tmp_path, monkeypatch, capsys):
    """Giết D28 (ghi thẳng lên đích) — luật `DT1a-R1-07` có bài canh."""
    t = _t()
    van_ban, _, _ = g._dung(7)
    p = g._ghi_csv(tmp_path, van_ban)
    ra = tmp_path / "phan_loai_ly_do.json"
    ra.write_text("BAN CU", encoding="utf-8")

    def hong(*a, **k):
        raise OSError("mô phỏng hỏng lúc thay tệp")

    monkeypatch.setattr(t.os, "replace", hong)
    with pytest.raises(OSError):
        g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, mong_nhan=dict(MONG))
    assert ra.read_text(encoding="utf-8") == "BAN CU"


# ═══ PHÁT HIỆN — ĐỎ trên 8a18599 (bài mong hành vi SAU khi sửa) ══════════════════════════════════
SO_CT = "4366191234567890"                 # Số CT 16 CHỮ SỐ (khớp hex16 — chỉ dùng cho lá ⛔ canh hex)
SO_CT_REF = "FT25123456789"                # mã ngân hàng có chữ ⇒ ⛔ hex16 (dùng cho lá canh MẪU hex16)
DG = "Chuyen tien cho Nguyen Van A theo HD 123"
TU_DO = [
    ("nguon_ban_doc_sha_la_SoCT", lambda d: d["nguon"].update(ban_doc_sha256_16=SO_CT_REF)),
    ("nguon_anh_so_la_DienGiai", lambda d: d["nguon"].update(anh_so=DG)),
    ("vi_sao_mang_DienGiai", lambda d: d.update(_vi_sao=d["_vi_sao"] + " " + DG)),
    ("khong_mang_PII_la_SoCT", lambda d: d.update(khong_mang_PII=SO_CT)),
    ("khoa_hong_gia_tri_SoCT", lambda d: d["mau_so"]["khoa_hong"].update(SO=SO_CT)),
    ("dang_khoa_hoc_gia_tri_DienGiai", lambda d: d["mau_so"]["dang_khoa_hoc"].update(L1=DG)),
    ("dang_khoa_hoc_khoa_la", lambda d: d["mau_so"]["dang_khoa_hoc"].update({"FT25123456789": 1})),
]


@pytest.mark.parametrize("ten, pha", TU_DO, ids=[x[0] for x in TU_DO])
def test_R1_DE_XUAT_la_chuoi_TU_DO_bi_chan(tmp_path, monkeypatch, capsys, ten, pha):
    """DT1b-R1-04 — mọi lá của tệp nhãn phải = hằng / ∈ tập đóng / khớp mẫu (hex16 · số nguyên)."""
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    d = json.loads(goc)
    pha(d)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)
    # câu lỗi của cổng riêng tư ⛔ bao giờ in LẠI giá trị nó vừa bắt (DT1b-R1-04)
    for ro_ri in (SO_CT, SO_CT_REF, DG):
        assert ro_ri not in err, (ten, err)


def test_R1_DE_XUAT_doi_nhan_HAI_dong_cung_ky_la_DO(tmp_path, monkeypatch, capsys):
    """DT1b-R1-05 — tổng y nguyên, bảng kỳ y nguyên, DANH TÍNH nhãn đã khác (Đ4). Đổi chỗ CẢ bộ
    (nhan, lech, ghi_chu) ⇒ mỗi dòng vẫn hợp lệ với nhãn mới (K6 ⛔ cắn) · số đếm + bảng kỳ y nguyên ⇒
    chỉ K13 (vân tay danh tính) cắn."""
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    d = json.loads(goc)
    a = next(r for r in d["dong_thieu"] if r["ky"] == "2026-07" and r["nhan"] == "KHOA_LECH")
    b = next(r for r in d["dong_thieu"] if r["ky"] == "2026-07" and r["nhan"] == "TRUNG_SEQ")
    for k in ("nhan", "lech", "ghi_chu"):
        a[k], b[k] = b[k], a[k]
    sao = tmp_path / "ban_sao.json"
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, out
    assert "vân tay danh tính nhãn" in err, err


# ═══ DT1b-R1-06 · bản đọc khoá THÔ nằm trong repo mà ⛔ bị .gitignore ⇒ TỪ CHỐI (mã 2) ════════════
def test_R1_DE_XUAT_ban_doc_khoa_trong_repo_khong_gitignore_bi_tu_choi(tmp_path, monkeypatch, capsys):
    """DT1b-R1-06 — chặn ở MÁY, ⛔ ở lời dặn. `git init` ở tmp_path; CSV ở gốc repo ⇒ 2 (⛔ đọc),
    CSV ở `hien_vat/` (bị bỏ qua) ⇒ đo bình thường."""
    tool = _t()
    repo = tmp_path / "repo_gia"
    (repo / "hien_vat").mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    (repo / ".gitignore").write_text("hien_vat/\n", encoding="utf-8")
    van_ban, _, _ = g._dung(7)
    monkeypatch.setattr(tool, "GOC", repo)
    # ① trong repo gốc, ⛔ bị gitignore ⇒ TỪ CHỐI mã 2, ⛔ ghi
    p_in = repo / "dt1b_khoa.csv"
    p_in.write_text(van_ban, encoding="utf-8")
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p_in), "--ghi", ra=ra,
                                 mong_nhan=dict(MONG))
    assert ma == 2, (out, err)
    assert "bị .gitignore" in err and not ra.exists()
    # ② trong hien_vat/ (bị bỏ qua) ⇒ chốt R8 ⛔ chặn (đo bình thường — ở đây ma 0 vì đã ghim)
    p_safe = repo / "hien_vat" / "dt1b_khoa.csv"
    p_safe.write_text(van_ban, encoding="utf-8")
    ra2 = tmp_path / "ra2.json"
    ma2, out2, err2 = g._chay_trong(monkeypatch, capsys, "--khoa", str(p_safe), "--ghi", ra=ra2,
                                    mong_nhan=dict(MONG))
    assert ma2 == 0, err2
    assert ra2.exists()
