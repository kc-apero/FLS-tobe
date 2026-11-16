# -*- coding: utf-8 -*-
"""DT1a — kiểm kê dòng sổ AS-IS chưa ghép 1-1 (`tools/phan_loai_dong_thieu.py`).

ISP 3.1.2 · Step 3 · DT1a · `WO-080` · AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10.

⭐ Vì sao có bộ bài này. HD1 = *"mapping được 100 %, giống các dữ liệu quá khứ"* (owner 16/11).
   Trên ảnh đóng băng, sổ AS-IS `ITL Ledge` có **9.967** dòng, mã FLS ghép 1-1 được **9.845**
   (`classifying_vs_canon.json`) — **122** dòng sổ ⛔ có cặp, và chiều ngược **9.992 − 9.845 = 147**
   dòng FLS ⛔ có dòng sổ. Trước bước này con số ấy chỉ sống trong một phép đo tay của orchestrator
   (16/11) — ⛔ máy nào đỏ khi nó đổi, và ⛔ ai liệt kê được ĐÚNG 122 dòng nào để DT1b gán lý do.

⛔⛔ Mỗi bài dưới đây canh một cái bẫy CÓ THẬT ở repo này:
  · `DT1a-B1` — MONG của bài thử **độc lập** với MONG của công cụ: lấy từ phép đo tay của
    orchestrator (16/11), ⛔ chép từ tool. Một MONG chép từ chính công cụ thì sửa công cụ cho khớp
    dữ liệu hỏng là cả hai cùng xanh. Tập 122 dòng còn được bài thử **tự tính lại** từ ba ảnh.
  · `DT1a-B2` — cổng phải được CHỨNG MINH ĐỎ (Đ5): phá một bản SAO TẠM *(⛔ chạm ảnh thật)*, chạy,
    xem cổng cắn, trả nguyên, chạy lại xanh. ⚠ Bài này đòi exit **= 1** (mã ĐỎ của công cụ), ⛔
    *"≠ 0"*: công cụ chưa có thì python thoát **2** (*can't open file*) — một bài *"≠ 0"* sẽ XANH
    trên một công cụ ⛔ tồn tại. Và bài **đổi chỗ cùng kỳ** chứng minh cổng TỔNG mù: 122 vẫn là 122,
    phân bố kỳ y nguyên, mà tập dòng đã khác — đúng bẫy `Đ4` *(`52 = 24 + 28` hay `38 + 14` đều ra
    52, mọi cổng canh tổng xanh suốt 20 ngày)*.
  · `DT1a-B3` — Đ3: mẫu số in TRƯỚC tỷ lệ, và mẫu số `0` là ĐỎ, ⛔ phải `0 %`
    (`SO_PHAT_HIEN_ISP-3.1.md` · `S0-R1-05`).
  · `DT1a-B4` — riêng tư: JSON ra ⛔ mang `Diễn giải` · `Số chứng từ` · email. Máy quét của bài thử
    cũng phải được chứng minh CẮN trên một mẫu bẩn, ⛔ chỉ chạy xanh trên đầu ra sạch (Đ3).
  · CLI từ chối đối số ⛔ khai (`S0-R1-03`); ⛔ đo được ⇒ ĐỎ với nguyên nhân trong MỘT dòng
    (`S0-R1-04`).
"""
from __future__ import annotations

import functools
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "phan_loai_dong_thieu.py"
FX = GOC / "tests" / "fixture"
RA = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
BA_ANH = ("itl_ledge_adjustment.json", "classifying_vs_canon.json", "pm_join.json")

# ── MONG ĐỘC LẬP — orchestrator đo tay 16/11 (`WO-080` · ISP Step 3 · Estimate), ⛔ chép từ tool ──
SO_DONG_SO = 9967          # dòng sổ AS-IS `ITL Ledge` trên ảnh (tests/ledger/test_parity_ca_so.py)
SO_DONG_GHEP = 9845        # dòng sổ ghép 1-1 được với dòng FLS (tests/ledger/test_classifying.py)
SO_DONG_CANON = 9992       # dòng FLS dựng lại từ `Transaction Mapping L1` (tests/adapters/test_pm_join.py)
THIEU = 122                # dòng sổ ∖ dòng đã ghép
NGUOC = 147                # dòng FLS ∖ dòng đã ghép = 9.992 − 9.845
# Orchestrator ghi 6 kỳ đầu + "…" và "18/23 kỳ"; 12 kỳ còn lại DT1a đo 16/11 — tổng phải 122, đúng 18 kỳ.
PHAN_BO_KY = {
    "2026-07": 23, "2025-11": 14, "2026-08": 13, "2026-06": 12, "2025-10": 9, "2026-04": 8,
    "2025-12": 5, "2026-02": 5, "2026-03": 5, "2026-05": 5, "2025-07": 4, "2025-08": 4,
    "2025-09": 4, "2026-01": 4, "2025-06": 3, "2025-02": 2, "2025-01": 1, "2025-05": 1,
}
HD_CLASSIFYING = {"Need to manual input": 121, "GI | Gross Inflow": 1}          # 121/122 (orchestrator)
# OGA 74 · GI 25 · DEP 8 · ITE 7 do orchestrator đo; "khác 8" tách bởi DT1a 16/11 (2 + 2 + 2 + 1 + 1 = 8).
HD_FINAL = {"OGA | GAC - Other": 74, "GI | Gross Inflow": 25, "DEP | Deposit": 8,
            "ITE | ITE Interest": 7, "NB | Lưu chuyển nội bộ": 2,
            "OMC | Online Marketing Cost": 2, "LC | License Cost": 2,
            "LMN | Loan/Borrowing": 1, "BON | Bonus": 1}
PAY_TYPE_FINAL = {"Thanh toán (Regular)": 71, "Thu tiền": 51}

# Thuộc tính đo được của một dòng thiếu (ISP Goal: kỳ · hd Classifying/MID/Final · pay_type · cdt1).
THUOC_TINH = ("ky",
              "hd_classifying", "hd_mid", "hd_final",
              "pay_type_classifying", "pay_type_mid", "pay_type_final",
              "cdt1_classifying", "cdt1_mid", "cdt1_final")


# ═════════════════════════════════════════════════════════════════════════ trợ thủ
def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *doi_so], cwd=GOC, capture_output=True, text=True,
        encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})


@functools.lru_cache(maxsize=1)
def _tool():
    """Nạp công cụ TRONG thân bài (⛔ ở fixture) — công cụ chưa có thì bài FAILED vì thiếu hành vi,
    ⛔ ERROR ở khâu dựng."""
    assert TOOL.exists(), f"⛔ chưa có {TOOL.relative_to(GOC)} — hành vi DT1a chưa có"
    spec = importlib.util.spec_from_file_location("_phan_loai_dong_thieu", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@functools.lru_cache(maxsize=1)
def _kq() -> dict:
    ra, loi = _tool().do(FX)
    assert loi == [], loi
    return ra


def _nap(thu_muc: Path, ten: str) -> dict:
    return json.loads((thu_muc / ten).read_text(encoding="utf-8"))


def _ghi(thu_muc: Path, ten: str, d: dict) -> None:
    (thu_muc / ten).write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")


def _sao_ba_anh(thu_muc: Path) -> Path:
    thu_muc.mkdir(parents=True, exist_ok=True)
    for ten in BA_ANH:
        shutil.copyfile(FX / ten, thu_muc / ten)
    return thu_muc


@functools.lru_cache(maxsize=1)
def _doc_anh_doc_lap():
    """Bài thử TỰ giải mã ba ảnh — ⛔ mượn mã của công cụ (một lỗi giải mã chung thì cả hai cùng sai
    mà vẫn khớp nhau)."""
    g = _nap(FX, BA_ANH[0])
    c = _nap(FX, BA_ANH[1])
    p = _nap(FX, BA_ANH[2])
    idx = {t: i for i, t in enumerate(g["cot"])}
    bang = g["bang_gia_tri"]
    so = {}
    for h in g["dong"]:
        o = {"ky": h[idx["ky"]]}
        for t in THUOC_TINH[1:]:
            i = h[idx[t]]
            o[t] = None if i == -1 else bang[i]
        so[h[idx["dong_sheet"]]] = o
    i_so, i_canon = c["cot"].index("dong_so"), c["cot"].index("dong_canon")
    ghep = {r[i_so] for r in c["dong"]}
    canon = {r[i_canon] for r in c["dong"]}
    bank = {b["dong"] for b in p["bank"]}
    return so, ghep, canon, bank


def _bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]", "", "".join(ch for ch in s if not unicodedata.combining(ch)).lower())


KHOA_CAM = ("diengiai", "sochungtu", "email")
MAU_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
MAU_REF_TRONG_LOI = "Did not find value"     # ô `#N/A (Did not find value 'FT…')` mang mã giao dịch


def _quet_rieng_tu(d) -> tuple[list[str], int]:
    """(vi phạm, số khoá đã quét) — máy quét RIÊNG của bài thử, ⛔ dùng `kiem_rieng_tu` của tool."""
    vi_pham: list[str] = []
    so_khoa = 0

    def di(x, duong):
        nonlocal so_khoa
        if isinstance(x, dict):
            for k, v in x.items():
                so_khoa += 1
                if any(c in _bo_dau(str(k)) for c in KHOA_CAM):
                    vi_pham.append(f"khoá {duong}/{k}")
                di(v, f"{duong}/{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                di(v, f"{duong}[{i}]")
        elif isinstance(x, str):
            if MAU_EMAIL.search(x):
                vi_pham.append(f"email ở {duong}")
            if MAU_REF_TRONG_LOI in x:
                vi_pham.append(f"mã tham chiếu trong ô lỗi ở {duong}")

    di(d, "")
    return vi_pham, so_khoa


# ═════════════════════════════════════════════════════════════════════ DT1a-B1
def test_DT1a_B1_tap_thieu_DUNG_122_dong_va_chieu_nguoc_147():
    """Tập thiếu = `dong_sheet` của sổ ∖ `dong_so` đã ghép — bài thử tự tính lại, so TỪNG dòng."""
    kq = _kq()
    so, ghep, canon, bank = _doc_anh_doc_lap()
    assert (len(so), len(ghep), len(bank)) == (SO_DONG_SO, SO_DONG_GHEP, SO_DONG_CANON)  # Đ3 trước
    assert kq["mau_so"]["so_dong_so"] == SO_DONG_SO
    assert kq["mau_so"]["so_dong_ghep"] == SO_DONG_GHEP
    assert kq["mau_so"]["so_dong_canon"] == SO_DONG_CANON

    mong_thieu = sorted(set(so) - ghep)
    assert len(mong_thieu) == THIEU
    assert kq["dem"]["thieu"] == THIEU
    assert [d["dong_sheet"] for d in kq["dong_thieu"]] == mong_thieu      # theo `dong_sheet`, tăng dần
    for d in kq["dong_thieu"]:
        assert set(d) == {"dong_sheet", *THUOC_TINH, "nhan"}, d           # ⛔ khoá thừa, ⛔ khoá thiếu
        assert d["nhan"] is None                                           # DT1b điền
        assert {t: d[t] for t in THUOC_TINH} == so[d["dong_sheet"]], d["dong_sheet"]

    mong_nguoc = sorted(bank - canon)
    assert len(mong_nguoc) == NGUOC == SO_DONG_CANON - SO_DONG_GHEP
    assert kq["dem"]["nguoc"] == NGUOC
    assert [d["dong_canon"] for d in kq["dong_nguoc"]] == mong_nguoc
    assert all(set(d) == {"dong_canon", "nhan"} and d["nhan"] is None for d in kq["dong_nguoc"])


def test_DT1a_B1_phan_bo_ky_va_thuoc_tinh_DUNG_MONG():
    dong = _kq()["dong_thieu"]
    assert len(dong) == THIEU                                              # Đ3: tập ⛔ rỗng
    assert dict(Counter(d["ky"] for d in dong)) == PHAN_BO_KY
    assert len(PHAN_BO_KY) == 18 and sum(PHAN_BO_KY.values()) == THIEU
    assert dict(Counter(d["hd_classifying"] for d in dong)) == HD_CLASSIFYING
    assert dict(Counter(d["hd_final"] for d in dong)) == HD_FINAL
    assert dict(Counter(d["pay_type_final"] for d in dong)) == PAY_TYPE_FINAL


def test_DT1a_B1_MONG_khai_TRONG_tool_va_cong_exit_0_tren_ba_anh():
    """Exit criteria mục 8: *"MONG khai trong tool (Đ5)"* — và MONG ấy bằng MONG độc lập ở đây."""
    m = _tool().MONG
    assert (m["thieu"], m["nguoc"]) == (THIEU, NGUOC)
    assert m["phan_bo_ky_thieu"] == PHAN_BO_KY
    assert (m["so_dong_so"], m["so_dong_ghep"], m["so_dong_canon"]) == (
        SO_DONG_SO, SO_DONG_GHEP, SO_DONG_CANON)
    r = _chay()
    assert r.returncode == 0, r.stdout + r.stderr
    assert "KẾT: ĐẠT" in r.stdout


def test_DT1a_B1_json_DA_GHI_khop_lan_do_hien_tai():
    """Hiện vật sinh máy ⛔ sửa tay: tệp đã commit phải BẰNG lần đo bây giờ (lệch ⇒ chạy `--ghi`)."""
    assert RA.exists(), f"⛔ chưa ghi {RA.relative_to(GOC)} — chạy `python {TOOL.relative_to(GOC)} --ghi`"
    assert json.loads(RA.read_text(encoding="utf-8")) == _kq()


# ═════════════════════════════════════════════════════════════════════ DT1a-B2
def test_DT1a_B2_bo_MOT_dong_khoi_tap_ghep_thi_DO_123_khac_122_roi_tra_nguyen(tmp_path):
    """Phá nguồn (bản SAO TẠM) → chạy → cắn → trả nguyên → xanh lại. ⛔ chạm `tests/fixture/`."""
    tm = _sao_ba_anh(tmp_path / "anh")
    r0 = _chay("--thu-muc", str(tm))
    assert r0.returncode == 0, "đối chứng: bản sao NGUYÊN phải xanh\n" + r0.stdout + r0.stderr

    c = _nap(tm, BA_ANH[1])
    bo = c["dong"].pop(0)                                    # bỏ một dòng khỏi tập ghép
    _ghi(tm, BA_ANH[1], c)
    r1 = _chay("--thu-muc", str(tm))
    assert r1.returncode == 1, r1.stdout + r1.stderr         # ⛔ "≠ 0": thiếu tool là exit 2
    assert any("123" in d and "122" in d for d in r1.stderr.splitlines()), r1.stderr
    assert "KẾT: ĐẠT" not in r1.stdout

    shutil.copyfile(FX / BA_ANH[1], tm / BA_ANH[1])          # trả nguyên
    r2 = _chay("--thu-muc", str(tm))
    assert r2.returncode == 0, r2.stdout + r2.stderr
    assert bo[0] not in {d["dong_sheet"] for d in _kq()["dong_thieu"]}   # dòng bỏ vốn đã ghép


def test_DT1a_B2_doi_cho_CUNG_KY_tong_van_122_nhung_VAN_TAY_do(tmp_path):
    """★ Bẫy `Đ4`: một dòng ghép trỏ sang một dòng thiếu CÙNG kỳ, CÙNG hd/pay_type ⇒ 122 vẫn 122,
    phân bố kỳ và phân bố thuộc tính y nguyên — chỉ VÂN TAY tập dòng thấy tập đã khác."""
    so, ghep, _canon, _bank = _doc_anh_doc_lap()
    thieu = sorted(set(so) - ghep)

    def khoa(d):
        o = so[d]
        return (o["ky"], o["hd_classifying"], o["hd_final"], o["pay_type_final"])

    cho = {khoa(m): m for m in thieu}
    tm = _sao_ba_anh(tmp_path / "anh")
    c = _nap(tm, BA_ANH[1])
    i_so = c["cot"].index("dong_so")
    cap = next(((i, cho[khoa(r[i_so])]) for i, r in enumerate(c["dong"]) if khoa(r[i_so]) in cho),
               None)
    assert cap is not None, "⛔ ⛔ tìm được cặp đổi chỗ — bài ⛔ đo được gì (Đ3)"
    i, m = cap
    c["dong"][i][i_so] = m
    _ghi(tm, BA_ANH[1], c)

    r = _chay("--thu-muc", str(tm))
    assert r.returncode == 1, r.stdout + r.stderr
    loi = [d for d in r.stderr.splitlines() if d.startswith("  ")]
    assert loi and all("vân tay" in d for d in loi), r.stderr  # mọi cổng TỔNG đều xanh — chỉ vân tay cắn


@pytest.mark.parametrize("ten", BA_ANH)
def test_DT1a_B2_checksum_BA_anh_la_cong(tmp_path, ten):
    """Tiền điều kiện ISP mục 5: ba checksum khớp MONG như `do_voi_so_luong.py`. Ảnh sổ được TÍNH LẠI
    từ nội dung; hai ảnh kia so trường `checksum_noi_dung` đã ghim (giống `do_voi_so_luong.py`)."""
    tm = _sao_ba_anh(tmp_path / "anh")
    d = _nap(tm, ten)
    if ten == "itl_ledge_adjustment.json":
        d["dong"][0][2] = d["dong"][1][6]                    # đổi MỘT ô, ⛔ đổi số dòng
    else:
        d["checksum_noi_dung"] = "0" * 16
    _ghi(tm, ten, d)
    r = _chay("--thu-muc", str(tm))
    assert r.returncode == 1, r.stdout + r.stderr
    assert any("checksum" in x and ten.split(".")[0] in x for x in r.stderr.splitlines()), r.stderr


# ═════════════════════════════════════════════════════════════════════ DT1a-B3
def test_DT1a_B3_in_MAU_SO_truoc_ty_le():
    r = _chay()
    assert r.returncode == 0, r.stdout + r.stderr
    out = r.stdout
    assert "%" in out, "⛔ ⛔ in tỷ lệ nào — bài ⛔ đo được thứ tự (Đ3)"
    dau_ty_le = out.index("%")
    for so, nhan in (("9.967", "dòng sổ"), ("9.845", "ghép")):
        assert so in out[:dau_ty_le], f"⛔ mẫu số {so} ⛔ in trước tỷ lệ đầu tiên"
        dong = next(d for d in out[:dau_ty_le].splitlines() if so in d)
        assert nhan in dong, f"Đ4: số {so} phải mang nhãn '{nhan}' ngay tại chỗ in: {dong!r}"


def test_DT1a_B3_mau_so_0_la_DO_khong_phai_0_phan_tram(tmp_path):
    tm = _sao_ba_anh(tmp_path / "anh")
    g = _nap(tm, BA_ANH[0])
    g["dong"] = []
    _ghi(tm, BA_ANH[0], g)
    r = _chay("--thu-muc", str(tm))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "mẫu số" in r.stderr, r.stderr
    assert "%" not in r.stdout, "⛔ in tỷ lệ trên mẫu số 0"


# ═════════════════════════════════════════════════════════════════════ DT1a-B4
def test_DT1a_B4_may_quet_cua_bai_CAN_tren_mau_ban():
    """Máy quét phải được chứng minh CẮN trước khi tin nó xanh (Đ3 · Đ5)."""
    for ban in ({"dong": [{"Diễn giải": "x"}]}, {"so_chung_tu": 1}, {"Email Address": "x"},
                {"a": [{"b": "ai@vi-du.vn"}]}, {"hd": "#N/A (Did not find value 'FT1' in VLOOKUP)"}):
        assert _quet_rieng_tu(ban)[0], ban
    assert _quet_rieng_tu({"dong_sheet": 1, "hd_final": "OGA | GAC - Other"})[0] == []


def test_DT1a_B4_json_ra_0_khoa_dien_giai_so_chung_tu_email():
    kq = _kq()
    vi_pham, so_khoa = _quet_rieng_tu(kq)
    assert so_khoa >= (THIEU + NGUOC) * 2, f"⛔ chỉ quét {so_khoa} khoá — ⛔ đo được (Đ3)"
    assert vi_pham == []
    if RA.exists():
        assert _quet_rieng_tu(json.loads(RA.read_text(encoding="utf-8")))[0] == []


def test_DT1a_B4_tool_TU_CHAN_truoc_khi_ghi():
    kiem = _tool().kiem_rieng_tu
    assert kiem(_kq()) == []
    assert kiem({"dong_thieu": [{"dien_giai": "x"}]})
    assert kiem({"dong_thieu": [{"hd_final": "ai@vi-du.vn"}]})


# ═════════════════════════════════════════════════════════════════════ CLI · Đ5
def test_CLI_doi_so_LA_va_ghi_tu_thu_muc_LA_bi_tu_choi(tmp_path):
    """`S0-R1-03`: từ chối MỌI đối số ⛔ khai. Và `--ghi` chỉ từ ảnh thật — ⛔ ghi hiện vật từ bản sao.

    ⛔⛔ Bản đầu của bài này chỉ đòi `returncode == 2` — và nó XANH khi công cụ CHƯA TỒN TẠI (lượt đỏ
    16/11): python thoát **2** với *"can't open file"*, trùng mã `2` của argparse. Nên mỗi lần
    từ chối phải mang CÂU của chính công cụ, ⛔ chỉ mã thoát.
    """
    r = _chay("--la")
    assert r.returncode == 2 and "unrecognized arguments: --la" in r.stderr, r.stderr
    truoc = RA.read_bytes() if RA.exists() else None
    tm = _sao_ba_anh(tmp_path / "anh")
    r = _chay("--ghi", "--thu-muc", str(tm))
    assert r.returncode == 2, r.stdout + r.stderr
    assert "TỪ CHỐI" in r.stderr and "--thu-muc" in r.stderr, r.stderr
    assert (RA.read_bytes() if RA.exists() else None) == truoc


def test_thieu_tep_anh_la_DO_voi_nguyen_nhan_MOT_dong(tmp_path):
    """Đ5: ⛔ đo được là ĐỎ. `S0-R1-04`: nguyên nhân đọc được trong MỘT dòng, ⛔ traceback."""
    (tmp_path / "rong").mkdir()
    r = _chay("--thu-muc", str(tmp_path / "rong"))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "Traceback" not in r.stderr
    assert any(d.startswith("LOI FileNotFoundError:") for d in r.stderr.splitlines()), r.stderr
