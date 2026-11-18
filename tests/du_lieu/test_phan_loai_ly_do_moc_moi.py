# -*- coding: utf-8 -*-
"""WO-156 — lượt nhãn DT1b trên MỐC MỚI 18/11 (phương án A): mốc THAM SỐ, ảnh mốc gọn, K10/K11 theo mốc KHAI.

⛔ Dữ liệu 100 % TỔNG HỢP do bài dựng (`SYN…`); ⛔ một giá trị thật. Mốc 26/08 vẫn là mặc định — các bài
cũ (`test_phan_loai_ly_do*.py`) canh điều đó; ở đây chỉ canh nhánh mốc mới.
Thiết kế bộ dựng (⛔ chép từ công cụ): SO 12 dòng · khoá A×3 (L1 có 2 ⇒ 1 dòng TRUNG_SEQ) · khoá B×1 (L1 có 1) ·
khoá C×1 (L1 không có; L1 có dòng cùng Số CT khác tiền ⇒ KHOA_LECH) · khoá D×1 (⛔ L1 ⇒ KHONG_CO_SAO_KE) ·
6 dòng khoá E1..E6 ghép 1-1. ⇒ khớp 9 · thiếu 3 (TRUNG_SEQ 1 · KHOA_LECH 1 · KHONG_CO_SAO_KE 1).
"""
from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "phan_loai_ly_do.py"


def _tool():
    s = importlib.util.spec_from_file_location("pl_moc", TOOL)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def _hang(ct, no="100", co="0", tk="111", tt="VND"):
    return [ct, no, co, tk, tt]


SO = ([_hang("SYNA")] * 3 + [_hang("SYNB")] + [_hang("SYNC", no="500")] + [_hang("SYND", no="900")]
      + [_hang(f"SYNE{i}", no=str(10 + i)) for i in range(1, 7)])
L1 = ([_hang("SYNA")] * 2 + [_hang("SYNB")] + [_hang("SYNC", no="501")] + [_hang(f"SYNE{i}", no=str(10 + i)) for i in range(1, 7)])


def _csv(p: Path, so=SO, l1=L1) -> Path:
    with p.open("w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["bang", "dong", "so_ct", "ps_no", "ps_co", "tk", "tien_te"])
        for i, h in enumerate(so):
            w.writerow(["SO", 10 + i, *h])
        for i, h in enumerate(l1):
            w.writerow(["L1", 4 + 3 * i, *h])
    return p


@pytest.fixture
def m(tmp_path, monkeypatch):
    t = _tool()
    monkeypatch.setattr(t, "RA", tmp_path / "ra.json")
    monkeypatch.setattr(t, "ANH_MOC", tmp_path / "moc.json")
    monkeypatch.setattr(t, "MONG_MOC", {k: None for k in t.MONG_MOC})        # bộ dựng bắt đầu CHƯA ghim
    return t


def test_AC2_do_moc_moi_dem_khop_thieu_nhan_theo_thiet_ke(m, tmp_path):
    kq, loi, anh = m.do_moc_moi(_csv(tmp_path / "k.csv"))
    assert (anh["so_dong"], anh["so_khop"], anh["so_thieu"]) == (12, 9, 3)
    thieu = {r["dong_sheet"]: r["nhan"] for r in kq["dong_thieu"]}
    # dòng SO 12 = 10+2 (A thứ 3), 14 (C), 15 (D) theo thiết kế
    assert thieu == {12: "TRUNG_SEQ", 14: "KHOA_LECH", 15: "KHONG_CO_SAO_KE"}
    assert [d["dong_sheet"] for d in anh["dong"] if not d["khop"]] == [12, 14, 15]
    assert kq["mau_so"]["tai_lap"] == 9 and kq["mau_so"]["so_dong_ghep_dt1a"] == 9
    assert not [x for x in loi if "mẫu số" in x or "tái lập" in x]


def test_AC2_K11_tap_dong_khai_trong_anh_khac_so_thi_DO(m, tmp_path):
    csvp = _csv(tmp_path / "k.csv")
    _, _, anh = m.do_moc_moi(csvp)
    anh["dong"].pop()                                  # bớt 1 dòng ở ảnh KHAI
    anh["so_dong"] -= 1
    _, loi, _ = m.do_moc_moi(csvp, anh)
    assert any("K11" in x for x in loi)


def test_AC2_K10_so_khop_khai_khac_tai_lap_thi_DO(m, tmp_path):
    csvp = _csv(tmp_path / "k.csv")
    _, _, anh = m.do_moc_moi(csvp)
    anh["so_khop"] += 1
    anh["so_thieu"] -= 1
    _, loi, _ = m.do_moc_moi(csvp, anh)
    assert any("K10" in x for x in loi)


def test_AC2_anh_khai_khop_thi_khong_loi(m, tmp_path):
    csvp = _csv(tmp_path / "k.csv")
    _, _, anh = m.do_moc_moi(csvp)
    _, loi, _ = m.do_moc_moi(csvp, anh)
    assert loi == []


def test_AC2_anh_moc_gon_khong_PII_dung_luoc_do(m, tmp_path):
    _, _, anh = m.do_moc_moi(_csv(tmp_path / "k.csv"))
    assert set(anh) == {"nguon", "so_dong", "so_khop", "so_thieu", "dong"}
    assert set(anh["dong"][0]) == {"dong_sheet", "khoa_bam", "khop"}
    txt = json.dumps(anh)
    assert "SYN" not in txt and "500" not in txt
    assert m.kiem_anh_moc(anh) == []
    bad = json.loads(txt)
    bad["dong"].append({"dong_sheet": 99, "khoa_bam": "0" * 16, "khop": True})
    assert any("so_dong" in x for x in m.kiem_anh_moc(bad))


def _ghim(m, kq, anh):
    mong = {"so_dong": anh["so_dong"], "so_khop": anh["so_khop"], "so_thieu": anh["so_thieu"],
            "van_tay_anh": m._van_tay_anh(anh), "phan_bo_nhan": dict(kq["dem_nhan"]),
            "van_tay_nhan": m._van_tay_nhan(kq["dong_thieu"])}
    m.MONG_MOC.update(mong)


def test_AC3_ghi_roi_cong_DAT_khi_da_ghim_va_ma4_khi_chua(m, tmp_path):
    csvp = _csv(tmp_path / "k.csv")
    assert m.main(["--khoa", str(csvp), "--moc", str(m.ANH_MOC), "--ghi"]) == m.CHUA_GHIM   # chưa ghim ⇒ 4
    assert m.RA.is_file() and m.ANH_MOC.is_file()
    assert m.main([]) == m.CHUA_GHIM                                                        # cổng, chưa ghim
    kq, anh = json.loads(m.RA.read_text("utf-8")), json.loads(m.ANH_MOC.read_text("utf-8"))
    assert kq["nguon"]["anh_so"] == m.NGUON_ANH_MOC and kq["nguon"]["tep_dt1a"] is None
    _ghim(m, kq, anh)
    assert m.main([]) == m.DAT
    assert m.main(["--khoa", str(csvp), "--moc", str(m.ANH_MOC)]) == m.DAT


def test_AC2_pha_anh_moc_them_bot_1_dong_thi_cong_DO(m, tmp_path):
    csvp = _csv(tmp_path / "k.csv")
    m.main(["--khoa", str(csvp), "--moc", str(m.ANH_MOC), "--ghi"])
    kq, anh = json.loads(m.RA.read_text("utf-8")), json.loads(m.ANH_MOC.read_text("utf-8"))
    _ghim(m, kq, anh)
    assert m.main([]) == m.DAT
    for pha in ("bot", "them"):
        a2 = json.loads(json.dumps(anh))
        if pha == "bot":
            a2["dong"].pop(0); a2["so_dong"] -= 1; a2["so_khop"] -= 1          # khai LẠI cho nhất quán
        else:
            a2["dong"].append({"dong_sheet": 999, "khoa_bam": "a" * 16, "khop": True})
            a2["so_dong"] += 1; a2["so_khop"] += 1
        m.ANH_MOC.write_text(json.dumps(a2), "utf-8")
        assert m.main([]) == m.DO, pha                                          # nhất quán nội bộ vẫn ĐỎ vì ghim
    m.ANH_MOC.write_text(json.dumps(anh), "utf-8")                              # trả nguyên
    assert m.main([]) == m.DAT


def test_AC4_doi_1_nhan_thi_cong_DO(m, tmp_path):
    csvp = _csv(tmp_path / "k.csv")
    m.main(["--khoa", str(csvp), "--moc", str(m.ANH_MOC), "--ghi"])
    kq, anh = json.loads(m.RA.read_text("utf-8")), json.loads(m.ANH_MOC.read_text("utf-8"))
    _ghim(m, kq, anh)
    for r in kq["dong_thieu"]:
        if r["nhan"] == "KHONG_CO_SAO_KE":
            r["nhan"] = "TRUNG_SEQ"
    kq["dem_nhan"] = {n: sum(1 for r in kq["dong_thieu"] if r["nhan"] == n) for n in m.NHAN}
    kq["nhan_theo_ky"] = {"-": dict(kq["dem_nhan"])}
    m.RA.write_text(json.dumps(kq), "utf-8")
    assert m.main([]) == m.DO


def test_AC4_ghim_THAT_cong_DAT_tren_tep_repo_va_doi_1_nhan_thi_DO(tmp_path):
    t = _tool()
    assert all(v is not None for v in t.MONG_MOC.values())                      # đã ghim, ⛔ None
    assert t.main([]) == t.DAT                                                  # tệp nhãn + ảnh mốc THẬT của repo
    kq = json.loads(t.RA.read_text("utf-8"))
    dem = kq["dem_nhan"]
    assert (sum(dem.values()), t.MONG_MOC["so_dong"] - t.MONG_MOC["so_khop"]) == (19, 19)
    r0 = next(r for r in kq["dong_thieu"] if r["nhan"] == "KHONG_CO_SAO_KE")
    r0["nhan"] = "TRUNG_SEQ"                                                    # đổi ĐÚNG 1 nhãn (giữ Σ)
    kq["dem_nhan"] = {n: sum(1 for r in kq["dong_thieu"] if r["nhan"] == n) for n in t.NHAN}
    kq["nhan_theo_ky"] = {"-": dict(kq["dem_nhan"])}
    p = tmp_path / "x.json"
    p.write_text(json.dumps(kq), "utf-8")
    assert t.main(["--tep", str(p)]) == t.DO


def test_AC1_mac_dinh_van_la_moc_26_08(m):
    assert m.MONG["so_dong_so"] == 9967 and m.MONG["so_dong_ghep"] == 9845 and m.MONG["thieu"] == 122
    assert m.main(["--tep", str(GOC / "docs" / "ITL" / "_tools" / "KHONG_CO_TEP.json")]) == m.CHUA_DO_DUOC


def test_WO156_xuat_so_csv_doc_theo_ten_tieu_de_hang7_dong_la_ban_ghi_va_bo_Dien_giai(tmp_path):
    spec = importlib.util.spec_from_file_location("xk_moc", GOC / "tools" / "xuat_khoa_dt1b.py")
    x = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(x)
    hang = [[""] * 7 for _ in range(6)]
    hang.append(["Ngày chứng từ", "Số chứng từ", "Diễn giải", "Đơn vị tiền tệ", "PS Nợ", "PS Có", "Tài khoản"])
    hang += [["", "", "", "", "", "", ""]] * 2
    hang.append(["2026-01-01", "SYNX1", "KHONG_DUOC_RA", "VND", "1,000.00", "", "111"])
    hang.append(["", "", "CHI_CO_CONG_THUC", "", "", "", ""])         # hàng 0 ô khoá ⇒ ⛔ phải là dòng sổ
    p = tmp_path / "so.csv"
    with p.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(hang)
    ra = x.doc_so_csv(p)
    assert [r["dong"] for r in ra] == [10]
    assert ra == [{"dong": 10, "so_ct": "SYNX1", "ps_no": "1,000.00", "ps_co": "", "tk": "111", "tien_te": "VND"}]
    out = tmp_path / "ra.csv"
    l1 = tmp_path / "l1.csv"
    l1.write_text("a\nb\nSố chứng từ,Đơn vị tiền tệ,PS Nợ,PS Có,Tài khoản\nSYNX1,VND,1000,,111\n", "utf-8")
    assert x.main(["--so-csv", str(p), "--l1", str(l1), "--ra", str(out)]) == 0
    assert "KHONG_DUOC_RA" not in out.read_text("utf-8")
    with pytest.raises(SystemExit) as e:                                                           # loại trừ lẫn nhau
        x.main(["--so-csv", str(p), "--xlsx", str(p), "--l1", str(l1), "--ra", str(out)])
    assert e.value.code == 2
