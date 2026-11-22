# -*- coding: utf-8 -*-
"""H15 · Step 43 · `WO-287` — HD1 TỰ SINH theo từng kỳ (AC10 · AC11): `tools/do_voi_so_luong.py` · `tu_sinh`.

Mỗi bài canh một cái bẫy CÓ THẬT:
  · `H15-B1` 26 kỳ có ảnh (⛔ "22 còn lại"), 0 `chua_do`; tổng dòng = Σ manifest DT12; HD 12.633/12.633.
  · `H15-B2` hồi quy 2026-03: HD 584/584, ô 4.088/4.088, MID 4.020/4.088 *(đo trước bước)*.
  · `H15-B3` Đ3: manifest 0 kỳ / hỏng ⇒ ĐỎ có tên; ảnh vắng / hỏng ⇒ `chua_do` CÓ TÊN, ⛔ "đạt".
  · `H15-B4` AC-4 `_chuan`: đổi 1 ô `svc_*` của 1 ảnh mới số↔chuỗi CÙNG giá trị ⇒ kết quả KHÔNG đổi;
            đổi giá trị ⇒ đúng kỳ ấy ĐỎ (qua đường thật `do()`).
  · `H15-B5` Đ5 hai chiều: MONG sai / thiếu / thừa một kỳ ⇒ ĐỎ; kỳ ⛔ ghim ⇒ ĐỎ.
  · `H15-B6` tệp sinh `voi_so_luong.json` khớp phép đo (⛔ sửa tay).
"""
from __future__ import annotations

import copy
import importlib.util
import json
import re
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "do_voi_so_luong.py"
F = GOC / "tests" / "fixture"
MANIFEST = F / "dap_an" / "itl_ledge_cac_ky.json"
RA = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"


def _tool():
    spec = importlib.util.spec_from_file_location("dvsl_h15", TOOL)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


@pytest.fixture(scope="module")
def m():
    return _tool()


@pytest.fixture(scope="module")
def tsk(m):
    return m.do_tu_sinh_theo_ky()


def _manifest():
    return json.loads(MANIFEST.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"]


# ── H15-B1 ──────────────────────────────────────────────────────────────────
def test_B1_26_ky_co_anh_khong_chua_do(tsk):
    mf = _manifest()
    assert tsk["so_ky_co_anh"] == 26 == len(mf) and len(tsk["theo_ky"]) == 26      # Đ3: mẫu số 26 ≠ 0
    assert tsk["chua_do"] == {} and tsk["loi"] == []
    assert {k: x["so_dong"] for k, x in tsk["theo_ky"].items()} == mf               # số dòng đo = số dòng manifest
    assert tsk["tong"]["hd"] == [sum(mf.values())] * 2 == [12633, 12633]


def test_B1_lech_theo_lop_co_ten(tsk):
    for ky, x in tsk["theo_ky"].items():
        assert sum(x["lech_final"].values()) == x["o"][1] - x["o"][0], ky           # lệch theo khối cộng đủ
        assert sum(x["lech_mid"].values()) == x["mid"][1] - x["mid"][0], ky
        assert x["o"][1] > 0 and x["o_loi"] == 0, ky                               # Đ3 + ô lỗi đếm riêng (⛔ ẩn)
    # kỳ lệch Final THẬT (⛔ sửa: ISP loại trừ) — 8 kỳ, 2026-07 nặng nhất
    lech = {k: sum(x["lech_final"].values()) for k, x in tsk["theo_ky"].items() if x["lech_final"]}
    assert lech == {"2025-02": 2, "2025-03": 2, "2025-05": 4, "2025-10": 8, "2025-11": 18, "2025-12": 19,
                    "2026-01": 7, "2026-07": 32}


# ── H15-B2 ──────────────────────────────────────────────────────────────────
def test_B2_hoi_quy_2026_03(m, tsk):
    x = tsk["theo_ky"]["2026-03"]
    assert tuple(x["hd"]) == (584, 584) and tuple(x["o"]) == (4088, 4088) and tuple(x["mid"]) == (4020, 4088)
    assert (m.do_tu_sinh()["hd"], m.do_tu_sinh()["o"]) == ((584, 584), (4088, 4088))
    assert "CŨ" in tsk["moc_so"]["2026-03"] and "20/11" in tsk["moc_so"]["2026-10"]      # hai mốc có nhãn (Đ4)


# ── H15-B3 ──────────────────────────────────────────────────────────────────
def test_B3_manifest_0_ky_do(m, tmp_path):
    p = tmp_path / "mf.json"
    p.write_text(json.dumps({"dong_theo_ky_o_cot_A": {}}), encoding="utf-8")
    r = m.do_tu_sinh_theo_ky(manifest=p)
    assert r["so_ky_co_anh"] == 0 and any("0 kỳ" in e for e in r["loi"])
    p.write_text("{hỏng", encoding="utf-8")
    assert any("đọc được" in e for e in m.do_tu_sinh_theo_ky(manifest=p)["loi"])


def test_B3_anh_vang_va_hong_la_chua_do_co_ten(m, tmp_path):
    hong = tmp_path / "hong.json"
    hong.write_text("{không phải json", encoding="utf-8")
    kham = {"2025-01": tmp_path / "khong_co.json", "2025-02": hong}
    r = m.do_tu_sinh_theo_ky(duong_anh=lambda ky: kham.get(ky) or m._duong_anh_ky(ky))
    assert set(r["chua_do"]) == {"2025-01", "2025-02"} and len(r["theo_ky"]) == 24
    assert "⛔ có ảnh" in r["chua_do"]["2025-01"] and "ảnh hỏng" in r["chua_do"]["2025-02"]
    assert "2025-01" not in r["theo_ky"]                                            # ⛔ "đạt" cho kỳ ⛔ đo


def test_B3_anh_khai_sai_ky_la_chua_do(m, tmp_path):
    d = json.loads(m._duong_anh_ky("2025-04").read_text(encoding="utf-8"))
    d["ky"] = "2025-05"
    p = tmp_path / "x.json"
    p.write_text(json.dumps(d), encoding="utf-8")
    r = m.do_tu_sinh_theo_ky(duong_anh=lambda ky: p if ky == "2025-04" else m._duong_anh_ky(ky))
    assert "2025-04" in r["chua_do"] and "2025-04" not in r["theo_ky"]


# ── H15-B4 (AC-4) ───────────────────────────────────────────────────────────
def _o_svc(d):
    """Ô `svc_*_final` đầu tiên là SỐ NGUYÊN (ảnh mới 100 % số — `DT12-R2-02`): đổi sang chuỗi cùng giá trị."""
    for i, r in enumerate(d["dong"]):
        for c in ("svc_start_final", "svc_end_final"):
            v = r.get(c)
            if isinstance(v, int) and not isinstance(v, bool) and v > 0:
                return i, c, v
    raise AssertionError("ảnh không có ô svc_* chữ-số")


def _do_voi_anh(m, ky, d, tmp_path, monkeypatch):
    p = tmp_path / f"{ky}.json"
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setattr(m, "_duong_anh_ky", lambda k: p if k == ky else F / "dap_an" / f"itl_ledge_{k}.json"
                        if k != "2026-03" else F / "itl_ledge_2026_03.json")
    return m


def test_B4_chuan_doi_kieu_cung_gia_tri_khong_doi(m, tsk, tmp_path, monkeypatch):
    ky = "2025-06"
    d = json.loads((F / "dap_an" / f"itl_ledge_{ky}.json").read_text(encoding="utf-8"))
    i, c, v = _o_svc(d)
    d2 = copy.deepcopy(d)
    d2["dong"][i][c] = str(v)                                                        # số → chuỗi, CÙNG giá trị
    _do_voi_anh(m, ky, d2, tmp_path, monkeypatch)
    assert m.do_tu_sinh_theo_ky()["theo_ky"][ky] == tsk["theo_ky"][ky]


def test_B4_doi_gia_tri_dung_ky_do_qua_do(m, tmp_path, monkeypatch):
    ky = "2025-06"
    d = json.loads((F / "dap_an" / f"itl_ledge_{ky}.json").read_text(encoding="utf-8"))
    i, c, v = _o_svc(d)
    d["dong"][i][c] = v + 7                                                # đổi GIÁ TRỊ Final
    _do_voi_anh(m, ky, d, tmp_path, monkeypatch)
    with pytest.raises(SystemExit) as e:
        m.do()
    loi = str(e.value)
    assert f"tự sinh {ky}" in loi and all(f"tự sinh {k}" not in loi for k in ("2025-05", "2025-07", "2026-03"))


def test_B4_do_xanh_khi_doi_kieu_cung_gia_tri_qua_do(m, tmp_path, monkeypatch):
    ky = "2025-06"
    d = json.loads((F / "dap_an" / f"itl_ledge_{ky}.json").read_text(encoding="utf-8"))
    i, c, v = _o_svc(d)
    d["dong"][i][c] = str(v)
    _do_voi_anh(m, ky, d, tmp_path, monkeypatch)
    m.do()                                                                           # ⛔ SystemExit: số↔chuỗi cùng giá trị ⛔ đổi kết quả


# ── H15-B5 (Đ5 hai chiều) ───────────────────────────────────────────────────
def _do_do(m, monkeypatch, sua):
    mong = copy.deepcopy(m.MONG)
    sua(mong)
    monkeypatch.setattr(m, "MONG", mong)
    with pytest.raises(SystemExit) as e:
        m.do()
    return str(e.value)


def test_B5_mong_duong_chuan_xanh(m):
    assert m.do()["tu_sinh"]["so_ky_co_anh"] == 26


def test_B5_sua_duoc_mot_ky_cung_do(m, monkeypatch):                                  # chiều "tốt hơn mong"
    def sua(mg):
        mg["tu_sinh_theo_ky"]["2025-02"]["o"] = (1981, 1981)
        mg["tu_sinh_theo_ky"]["2025-02"]["lech_final"] = {}
    assert "tự sinh 2025-02" in _do_do(m, monkeypatch, sua)


def test_B5_xau_di_mot_ky_do(m, monkeypatch):                                         # chiều "xấu hơn mong"
    def sua(mg):
        mg["tu_sinh_theo_ky"]["2026-10"]["o"] = (7267, 7267)
    assert "tự sinh 2026-10" in _do_do(m, monkeypatch, sua)


def test_B5_mong_thieu_ky_do(m, monkeypatch):
    assert "tự sinh 2026-11: đo được nhưng MONG ⛔ khai" in _do_do(m, monkeypatch, lambda mg: mg["tu_sinh_theo_ky"].pop("2026-11"))


def test_B5_mong_mat_khoa_do_mot_dong(m, monkeypatch):
    def sua(mg):
        for k in ("tu_sinh_theo_ky", "tu_sinh_so_ky", "tu_sinh_chua_do"):
            mg.pop(k)
    assert "Traceback" not in _do_do(m, monkeypatch, sua)


def test_B5_ky_khai_chua_do_ma_do_duoc_do(m, monkeypatch):
    assert "chua_do" in _do_do(m, monkeypatch, lambda mg: mg.__setitem__("tu_sinh_chua_do", ("2025-01",)))


# ── H15-B6 ──────────────────────────────────────────────────────────────────
def test_B6_tep_sinh_khop_phep_do(m, tsk):
    ts = json.loads(RA.read_text(encoding="utf-8"))["tu_sinh"]
    assert ts["so_ky_co_anh"] == 26 and ts["chua_do"] == {}
    for ky, x in tsk["theo_ky"].items():
        y = ts["theo_ky"][ky]
        assert (y["o"], y["hd"], y["mid"], y["lech_final"], y["lech_mid"], y["o_loi"]) == (
            list(x["o"]), list(x["hd"]), list(x["mid"]), x["lech_final"], x["lech_mid"], x["o_loi"]), ky
