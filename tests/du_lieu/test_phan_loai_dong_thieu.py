# -*- coding: utf-8 -*-
"""DT1a — kiểm kê dòng sổ AS-IS chưa ghép 1-1 (`tools/phan_loai_dong_thieu.py`).

ISP 3.1.2 · Step 3 · DT1a · `WO-080` · AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10.

⭐ Vì sao có bộ bài này. HD1 = *"mapping được 100 %, giống các dữ liệu quá khứ"* (owner 16/11).
   Trên ảnh đóng băng, sổ AS-IS `ITL Ledge` có **9.967** dòng, mã FLS ghép 1-1 được **9.845**
   (`classifying_vs_canon.json`) — **122** dòng sổ ⛔ có cặp, và chiều ngược **9.992 − 9.845 = 147**
   dòng FLS ⛔ có dòng sổ. Trước bước này các TỔNG đã có máy canh gián tiếp —
   `tools/do_voi_so_luong.py:118` · `:129` · `:138` ghim 9.967 · 9.845 · 9.992 — nhưng DANH TÍNH tập
   chỉ sống trong một phép đo tay của orchestrator (16/11): ⛔ máy nào đỏ khi tập ĐỔI mà tổng giữ
   nguyên, và ⛔ ai liệt kê được ĐÚNG 122 dòng nào để DT1b gán lý do.
   *(Đính chính `DT1a-R1-05`ⓒ · `KQ-082`: bản đầu viết "⛔ máy nào đỏ khi nó đổi" — sai `Đ1`, chưa grep
   `tools/`.)*

⛔⛔ Mỗi bài dưới đây canh một cái bẫy CÓ THẬT ở repo này:
  · `DT1a-B1` — MONG của bài thử được VIẾT RIÊNG, ⛔ import từ tool: một MONG chép từ chính công cụ
    thì sửa công cụ cho khớp dữ liệu hỏng là cả hai cùng xanh. Tập 122 dòng còn được bài thử **tự
    tính lại** từ ba ảnh. ⚠ "Viết riêng" ⛔ phải "mọi số do orchestrator đo": nguồn TỪNG số ghi cạnh
    nó — orchestrator đo tay 16/11 phần tổng · 3 kỳ đầu · `hd` (ISP `:20`); DT1a TỰ ĐO 16/11 phần 15
    kỳ còn lại · "khác 8" · `pay_type_final` · `cdt1_final`, rồi R1 `KQ-082` đo ĐỘC LẬP khớp (`:48` ·
    `:51` · `:52`). *(Đính chính `DT1a-R1-05`ⓐ: bản đầu nói cả bộ "lấy từ phép đo tay của
    orchestrator" — nói quá.)*
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

⛔⛔ Vòng sửa sau R1 (`KQ-082`) — R1 đột biến công cụ 11 cách, bộ 16 bài cũ chỉ bắt **2/11**. Bài thêm:
  · `DT1a-R1-01` — chốt riêng tư phải được chứng minh NỐI vào đường đo thật (cấy email vào một ô
    của dòng thiếu trên bản sao), ⛔ chỉ gọi hàm `kiem_rieng_tu` rời: đột biến bỏ lời gọi ⇒ 16 bài
    cũ vẫn xanh.
  · `DT1a-R1-02` — vân tay tập NGƯỢC phải được chứng minh cắn MỘT MÌNH: phía canon có đúng bẫy `Đ4`
    mà bài đổi chỗ cùng kỳ dựng cho phía sổ.
  · `DT1a-R1-03` — mỗi phép so của `do()` có một ca phá RIÊNG đòi CHÍNH dòng của nó xuất hiện; và
    cổng ĐỎ ⛔ được ghi đè hiện vật (chốt DUY NHẤT giữ JSON khỏi một lượt đỏ).
  · `DT1a-R1-04` — checksum ảnh sổ ⛔ phủ `cot`: đổi NHÃN hai cột ⇒ công cụ cũ exit 0. Nay bộ 23 tên
    cột + phân bố `cdt1_final` có MONG.
  · `DT1a-R1-07` — ghi hiện vật qua tệp tạm + `os.replace`. `DT1a-R1-09` — câu khai `khong_mang_PII`
    phải BẰNG tập máy chặn.
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

# ── MONG VIẾT RIÊNG — ⛔ import từ tool; nguồn TỪNG số ghi cạnh nó (`DT1a-R1-05`) ───────────────────
SO_DONG_SO = 9967          # dòng sổ AS-IS `ITL Ledge` trên ảnh (tests/ledger/test_parity_ca_so.py)
SO_DONG_GHEP = 9845        # dòng sổ ghép 1-1 được với dòng FLS (tests/ledger/test_classifying.py)
SO_DONG_CANON = 9992       # dòng FLS dựng lại từ `Transaction Mapping L1` (tests/adapters/test_pm_join.py)
THIEU = 122                # dòng sổ ∖ dòng đã ghép (orchestrator 16/11 · ISP `:20`)
NGUOC = 147                # dòng FLS ∖ dòng đã ghép = 9.992 − 9.845 (orchestrator 16/11 · ISP `:20`)
# Orchestrator ghi 3 kỳ đầu (2026-07 · 2025-11 · 2026-08 — ISP `:20` · `:649` · `WO-080:38`) + "…" và
# "18/23 kỳ"; 15 kỳ còn lại DT1a TỰ ĐO 16/11; R1 `KQ-082:48` đo độc lập khớp 18/18 — tổng 122, đúng 18 kỳ.
# ⚠ Bản đầu ghi "6 kỳ đầu · 12 kỳ còn lại" — sai (`DT1a-R1-05`ⓐ). Đo lại vòng sửa: grep `2026-06: 12` ·
#   `2025-10: 9` · `2026-04: 8` trên docs/+fls/+tools/+tests/ ⇒ 1 dòng/mẫu, đều ở sổ phát hiện R1 (biên bản
#   TRÍCH LẠI mẫu grep, ⛔ nguồn); dạng `"2026-06": 12` chỉ ở MONG của chính DT1a (tool + bài này).
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
PAY_TYPE_FINAL = {"Thanh toán (Regular)": 71, "Thu tiền": 51}   # DT1a tự đo 16/11 · R1 `KQ-082:52` khớp
# `cdt1_final` của 122 dòng thiếu — DT1a tự đo 16/11 (bảng `BG-081` hàng Σ) · R1 `KQ-082:52` đo độc lập khớp.
# ⚠ Hai ô cuối gõ lệch khuôn (`SHQ2 | Headquarters1` mã ↔ tên chéo · `SHQ1| Headquarters1` thiếu dấu cách) —
#   GIỮ nguyên chữ: MONG ghim ĐÚNG ô sổ, sửa nhãn là việc DT1b (`DT1a-R1-04`).
CDT1_FINAL = {"SHQ1 | Headquarters1": 60, "SHQ2 | Headquarters2": 49, "COR | TeraSofts": 9,
              "CAH | Astronex": 1, "TOR | Project A": 1, "SHQ2 | Headquarters1": 1,
              "SHQ1| Headquarters1": 1}
# Bộ tên cột của ảnh sổ, THEO THỨ TỰ (`DT1a-R1-04`) — DỰNG từ khuôn, ⛔ chép danh sách của tool:
# 2 cột khoá + 7 khối × (Classifying · MID · Final). Hai nguồn cho khuôn: `tools/do_voi_so_luong.py:54`
# (`KHOI`, 7 khối) · `tests/ledger/test_parity_ca_so.py:22` ("21 cột Classifying/MID/Final × 7 khối").
# Đ4: 23 = 2 + 3 × 7 — đếm TÊN CỘT của trường `cot`, ⛔ bề rộng hàng của sổ gốc.
KHOI_SO = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
COT_SO = ("dong_sheet", "ky", *(f"{k}_{t}" for k in KHOI_SO for t in ("classifying", "mid", "final")))

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


def _sua(thu_muc: Path, ten: str, phep) -> None:
    """Đọc ảnh `ten` của BẢN SAO, áp `phep(d)` tại chỗ, ghi lại. ⛔ bao giờ trỏ `FX`."""
    assert thu_muc.resolve() != FX.resolve(), "⛔ sửa ảnh THẬT"
    d = _nap(thu_muc, ten)
    phep(d)
    _ghi(thu_muc, ten, d)


def _loi(r: subprocess.CompletedProcess) -> list[str]:
    """Các dòng lệch công cụ in ra stderr (thụt hai dấu cách) — đã bỏ thụt."""
    return [d.strip() for d in r.stderr.splitlines() if d.startswith("  ")]


def _co_cong(loi: list[str], nhan: str) -> bool:
    """Có dòng lệch của ĐÚNG cổng `nhan` — khớp nguyên nhãn + `: đo ` (dạng `kiem` in), nên nhãn
    `số dòng sổ` ⛔ ăn nhầm dòng của cổng `số dòng sổ: trường so_dong_so …`."""
    return any(d.startswith(nhan + ": đo ") for d in loi)


def _tool_moi():
    """Một bản nạp MỚI của công cụ cho bài gọi `main()` trong tiến trình và monkeypatch `GOC`/`FX`/`RA`
    — ⛔ dùng bản `_tool()` đã cache chung, để một lần vá ⛔ rò sang bài khác."""
    assert TOOL.exists(), f"⛔ chưa có {TOOL.relative_to(GOC)}"
    spec = importlib.util.spec_from_file_location("_phan_loai_dong_thieu_moi", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tro_ve_ban_sao(monkeypatch, mod, tmp_path: Path) -> tuple[Path, Path]:
    """Trỏ `FX` của công cụ vào bản sao ba ảnh, `RA` vào `tmp_path` — `main(["--ghi"])` ⛔ chạm hiện vật
    thật. `GOC` cũng trỏ `tmp_path`: công cụ in `RA.relative_to(GOC)` ở `--help` lẫn dòng `✅ đã ghi`."""
    anh = _sao_ba_anh(tmp_path / "anh")
    ra = tmp_path / "ra" / RA.name
    ra.parent.mkdir()
    monkeypatch.setattr(mod, "GOC", tmp_path)
    monkeypatch.setattr(mod, "FX", anh)
    monkeypatch.setattr(mod, "RA", ra)
    return anh, ra


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
    assert dict(Counter(d["cdt1_final"] for d in dong)) == CDT1_FINAL                # DT1a-R1-04
    assert sum(CDT1_FINAL.values()) == THIEU


def test_DT1a_B1_MONG_khai_TRONG_tool_va_cong_exit_0_tren_ba_anh():
    """Exit criteria mục 8: *"MONG khai trong tool (Đ5)"* — và MONG ấy bằng MONG viết riêng ở đây."""
    m = _tool().MONG
    assert (m["thieu"], m["nguoc"]) == (THIEU, NGUOC)
    assert m["phan_bo_ky_thieu"] == PHAN_BO_KY
    assert (m["so_dong_so"], m["so_dong_ghep"], m["so_dong_canon"]) == (
        SO_DONG_SO, SO_DONG_GHEP, SO_DONG_CANON)
    assert (m["hd_classifying"], m["hd_final"], m["pay_type_final"]) == (
        HD_CLASSIFYING, HD_FINAL, PAY_TYPE_FINAL)
    # DT1a-R1-04 — bộ 23 tên cột ảnh sổ + phân bố `cdt1_final` có MONG; và ảnh THẬT đúng bộ ấy (hai nguồn:
    # khuôn dựng ở bài ↔ trường `cot` của ảnh ↔ danh sách khai trong tool).
    assert len(COT_SO) == 23
    assert tuple(m["cot_so"]) == COT_SO
    assert tuple(_nap(FX, BA_ANH[0])["cot"]) == COT_SO
    assert m["cdt1_final"] == CDT1_FINAL
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
    """★ Bẫy `Đ4`: một dòng ghép trỏ sang một dòng thiếu CÙNG kỳ, CÙNG hd/pay_type/cdt1 ⇒ 122 vẫn 122,
    phân bố kỳ và phân bố thuộc tính y nguyên — chỉ VÂN TAY tập dòng thấy tập đã khác.

    ⚠ Vòng sửa R1 (`DT1a-R1-04`) thêm MONG phân bố `cdt1_final` vào công cụ ⇒ khoá chọn cặp thêm
    `cdt1_final`, để GIỮ tiền đề *"mọi phân bố có MONG đều y nguyên"*. Lo gốc ⛔ đổi: chỉ vân tay cắn.
    Đo vòng sửa: khoá 4 trường có 1.401 dòng ghép ứng viên, khoá 5 trường còn 764 — cặp bài chọn ⛔ đổi
    (dòng ghép `#646` · `dong_so 656 → 744`, cả hai `cdt1_final = SHQ2 | Headquarters2`): trước đây bài
    xanh nhờ TÌNH CỜ trùng `cdt1_final`, nay nhờ khoá."""
    so, ghep, _canon, _bank = _doc_anh_doc_lap()
    thieu = sorted(set(so) - ghep)

    def khoa(d):
        o = so[d]
        return (o["ky"], o["hd_classifying"], o["hd_final"], o["pay_type_final"], o["cdt1_final"])

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


def test_DT1a_B2_doi_cho_phia_CANON_tong_van_147_nhung_VAN_TAY_NGUOC_do(tmp_path):
    """★ `DT1a-R1-02` — bẫy `Đ4` phía CANON, đối xứng bài trên: một dòng ghép đổi `dong_canon` sang một
    dòng bank CHƯA ghép ⇒ 147 vẫn 147, mọi số tổng y nguyên, mà tập 147 dòng DT1b khoá nhãn (Q2 = ⓐ)
    đã khác — chỉ vân tay tập NGƯỢC thấy.

    ⛔⛔ Vì sao có bài này: bài đổi chỗ phía sổ chỉ chứng minh vân tay THIẾU; R1 bỏ hẳn phép so vân tay
    ngược (đột biến M2) ⇒ 16 bài cũ vẫn xanh. Chứng minh một vế ⛔ phủ vế kia."""
    _so, _ghep, canon, bank = _doc_anh_doc_lap()
    tu_do = sorted(bank - canon)
    assert len(tu_do) == NGUOC, "⛔ ⛔ có dòng bank chưa ghép để đổi chỗ — bài ⛔ đo được gì (Đ3)"
    tm = _sao_ba_anh(tmp_path / "anh")

    def phep(c):
        c["dong"][0][c["cot"].index("dong_canon")] = tu_do[0]
    _sua(tm, BA_ANH[1], phep)

    r = _chay("--thu-muc", str(tm))
    assert r.returncode == 1, r.stdout + r.stderr
    assert f"{NGUOC} / 9.992 dòng canon" in r.stdout, r.stdout  # tổng vẫn 147 — cổng TỔNG mù
    loi = _loi(r)
    assert loi and all(d.startswith("vân tay tập ngược") for d in loi), r.stderr


# ── DT1a-R1-03 · -04 — mỗi phép so của `do()` có ca phá RIÊNG ─────────────────────────────────────────
def _dong_thieu_dau() -> int:
    so, ghep, _c, _b = _doc_anh_doc_lap()
    return min(set(so) - ghep)


def _p_doi_nhan_cot(a: str, b: str):
    def phep(g):
        i, j = g["cot"].index(a), g["cot"].index(b)
        g["cot"][i], g["cot"][j] = b, a                        # đổi NHÃN, thân `dong` y nguyên
    return phep


def _p_o_dong_thieu(t: str):
    """Ô `t` của dòng thiếu ĐẦU sang một giá trị KHÁC đã có ở cột ấy (⛔ đổi tập dòng)."""
    def phep(g):
        d0, i_ds, i_t = _dong_thieu_dau(), g["cot"].index("dong_sheet"), g["cot"].index(t)
        h = next(h for h in g["dong"] if h[i_ds] == d0)
        if t == "ky":                                          # `ky` là GIÁ TRỊ, ⛔ chỉ số vào bảng
            h[i_t] = next(x[i_t] for x in g["dong"] if x[i_t] != h[i_t])
            return
        cu = None if h[i_t] == -1 else g["bang_gia_tri"][h[i_t]]
        h[i_t] = next(x[i_t] for x in g["dong"] if x[i_t] != -1 and g["bang_gia_tri"][x[i_t]] != cu)
    return phep


def _p_gop_ky_khong_thieu(g):
    """Gộp một kỳ ⛔ có dòng thiếu vào kỳ kề ⇒ 22 kỳ, phân bố kỳ của dòng thiếu y nguyên."""
    so, ghep, _c, _b = _doc_anh_doc_lap()
    i_ky = g["cot"].index("ky")
    cac_ky = sorted({o["ky"] for o in so.values()})
    ky_thieu = {so[d]["ky"] for d in set(so) - ghep}
    k = next(k for k in cac_ky if k not in ky_thieu)
    sang = cac_ky[cac_ky.index(k) + 1]
    for h in g["dong"]:
        if h[i_ky] == k:
            h[i_ky] = sang


def _p_bo_dong_so_thieu(g):
    i_ds, d0 = g["cot"].index("dong_sheet"), _dong_thieu_dau()
    g["dong"] = [h for h in g["dong"] if h[i_ds] != d0]


def _p_trung(cot: str):
    def phep(d):
        i = d["cot"].index(cot)
        d["dong"][1][i] = d["dong"][0][i]
    return phep


def _p_truong(ten: str):
    def phep(c):
        c[ten] += 1
    return phep


def _p_tro_ra_ngoai(cot: str):
    def phep(c):
        so, _g, _cn, bank = _doc_anh_doc_lap()
        c["dong"][0][c["cot"].index(cot)] = max(set(so) | bank) + 1000
    return phep


def _p_bo_dong_ghep(c):
    c["dong"].pop(0)


def _p_bo_dong_bank_chua_ghep(p):
    _so, _g, canon, bank = _doc_anh_doc_lap()
    bo = min(bank - canon)
    p["bank"] = [b for b in p["bank"] if b["dong"] != bo]


N_SO, N_GHEP, N_PM = BA_ANH
# (ảnh phá, phép phá, nhãn cổng PHẢI có dòng lệch, chỉ-những-cổng-ấy?) — nhãn = chữ `kiem` của công cụ.
CA_PHA = {
    "cot_doi_nhan_cdt1_mid_final": (N_SO, _p_doi_nhan_cot("cdt1_mid", "cdt1_final"),
                                    ("tên cột ảnh sổ (cot, 23 tên theo thứ tự)",
                                     "phân bố cdt1_final của dòng thiếu"), False),
    "cot_doi_nhan_pay_cls_cdt1_cls": (N_SO, _p_doi_nhan_cot("pay_type_classifying", "cdt1_classifying"),
                                      ("tên cột ảnh sổ (cot, 23 tên theo thứ tự)",), True),
    "dong_sheet_trung": (N_SO, _p_trung("dong_sheet"),
                         ("dong_sheet ⛔ trùng (số dòng ảnh sổ ↔ số dong_sheet khác nhau)",), False),
    "M6_dong_so_trung": (N_GHEP, _p_trung("dong_so"),
                         ("dong_so ⛔ trùng (dòng ghép ↔ dong_so khác nhau)",), False),
    "dong_canon_trung": (N_GHEP, _p_trung("dong_canon"),
                         ("dong_canon ⛔ trùng (dòng ghép ↔ dong_canon khác nhau)",), False),
    "M3_truong_so_dong_so": (N_GHEP, _p_truong("so_dong_so"),
                             ("số dòng sổ: trường so_dong_so của ảnh ghép ↔ đếm ảnh sổ",
                              "dòng sổ ⛔ ghép: hiệu trường khai so_dong_so − so_dong_ghep ↔ tập liệt kê"), True),
    "truong_so_dong_ghep": (N_GHEP, _p_truong("so_dong_ghep"),
                            ("số dòng ghép: trường so_dong_ghep của ảnh ↔ đếm",), False),
    "M4_ghep_tro_dong_so_khong_co": (N_GHEP, _p_tro_ra_ngoai("dong_so"),
                                     ("dòng ghép trỏ dòng sổ ⛔ có trong ảnh sổ",
                                      "dòng sổ ⛔ ghép (sổ ∖ ghép)"), False),
    "truong_so_dong_canon": (N_GHEP, _p_truong("so_dong_canon"),
                             ("số dòng canon: trường so_dong_canon của ảnh ghép ↔ dòng bank pm_join",
                              "dòng FLS ⛔ có dòng sổ: hiệu trường khai so_dong_canon − so_dong_ghep ↔ tập liệt kê"),
                             True),
    "M5_canon_ngoai_bank": (N_GHEP, _p_tro_ra_ngoai("dong_canon"),
                            ("dong_canon đã ghép ⛔ thuộc bank pm_join",
                             "dòng FLS ⛔ có dòng sổ (canon ∖ ghép)"), False),
    "MONG_so_dong_so": (N_SO, _p_bo_dong_so_thieu, ("số dòng sổ", "dòng sổ ⛔ ghép (sổ ∖ ghép)"), False),
    "M11_so_ky": (N_SO, _p_gop_ky_khong_thieu, ("số kỳ",), False),
    "MONG_so_dong_ghep": (N_GHEP, _p_bo_dong_ghep, ("số dòng ghép", "dòng FLS ⛔ có dòng sổ (canon ∖ ghép)"),
                          False),
    "MONG_so_dong_canon": (N_PM, _p_bo_dong_bank_chua_ghep,
                           ("số dòng canon", "dòng FLS ⛔ có dòng sổ (canon ∖ ghép)"), False),
    "phan_bo_ky": (N_SO, _p_o_dong_thieu("ky"), ("phân bố kỳ của dòng thiếu",), False),
    **{f"M7_phan_bo_{t}": (N_SO, _p_o_dong_thieu(t), (f"phân bố {t} của dòng thiếu",), False)
       for t in ("hd_classifying", "hd_final", "pay_type_final", "cdt1_final")},
}


@pytest.mark.parametrize("ca", list(CA_PHA))
def test_DT1a_R1_03_moi_cong_co_ca_pha_RIENG(tmp_path, ca):
    """`DT1a-R1-03` · `-04` — mỗi phép so của `do()` phải được chứng minh CẮN bằng một ca phá của
    CHÍNH nó: bài đòi dòng lệch mang ĐÚNG nhãn cổng ấy. Bỏ phép so (đột biến) ⇒ dòng biến mất ⇒ bài
    ĐỎ — dù các cổng khác (phòng thủ chồng) vẫn đỏ theo và exit vẫn 1.

    ⛔⛔ Vì sao: R1 đột biến 11 cách, 16 bài cũ bắt 2/11 — chín phép so "đã có" mà chưa bài nào thấy
    chúng cắn MỘT LẦN. Ca `chi = True` còn đòi KHÔNG cổng nào khác đỏ — cổng ấy là cổng DUY NHẤT thấy
    phép phá (vd. đổi nhãn `pay_type_classifying` ↔ `cdt1_classifying`: công cụ trước vòng sửa exit 0).
    Cổng có bài riêng ở chỗ khác: ba checksum (`…checksum_BA_anh_la_cong`) · hai vân tay (hai bài đổi
    chỗ) · `dòng sổ ⛔ ghép (sổ ∖ ghép)` = 123 (`…bo_MOT_dong…`) · mẫu số 0 (`…mau_so_0…`) · riêng tư
    (`…rieng_tu_NOI_vao_duong_do_that…`)."""
    anh, phep, nhan_phai_co, chi = CA_PHA[ca]
    tm = _sao_ba_anh(tmp_path / "anh")
    _sua(tm, anh, phep)
    r = _chay("--thu-muc", str(tm))
    assert r.returncode == 1, r.stdout + r.stderr
    loi = _loi(r)
    for nhan in nhan_phai_co:
        assert _co_cong(loi, nhan), f"⛔ cổng '{nhan}' ⛔ cắn ca {ca}:\n" + r.stderr
    if chi:
        thua = [d for d in loi if not any(d.startswith(n + ": đo ") for n in nhan_phai_co)]
        assert thua == [], f"ca {ca} phải CHỈ đỏ ở {nhan_phai_co}:\n" + r.stderr


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
    """Hàm chặn của công cụ cắn trên mẫu tay. ⚠ Bài này CHỈ chứng minh HÀM — việc hàm được NỐI vào
    đường đo thì bài kế tiếp chứng minh (`DT1a-R1-01`)."""
    kiem = _tool().kiem_rieng_tu
    assert kiem(_kq()) == []
    assert kiem({"dong_thieu": [{"dien_giai": "x"}]})
    assert kiem({"dong_thieu": [{"hd_final": "ai@vi-du.vn"}]})


def test_DT1a_B4_rieng_tu_NOI_vao_duong_do_that_email_o_hd_mid_dong_thieu(tmp_path):
    """★ `DT1a-R1-01` — cấy một email vào ô `hd_mid` của dòng THIẾU đầu tiên trên bản sao ảnh sổ ⇒
    công cụ (chạy thật, qua `main`) phải in dòng `riêng tư: email ở /dong_thieu[0]/hd_mid` và exit 1.

    ⛔⛔ Vì sao: bài trên gọi `kiem_rieng_tu` RỜI trên mẫu tay; R1 thay lời gọi trong `do()` bằng `pass`
    (đột biến M1) ⇒ 16 bài cũ vẫn xanh — chốt mà DT1b sẽ dựa vào khi thêm khoá băm Số CT ⛔ có bài
    canh. Gọi hàm kiểm rời chỉ chứng minh hàm, ⛔ chứng minh nó được gọi.
    ⚠ Checksum ảnh sổ cũng đỏ (sửa `bang_gia_tri`) — nên bài đòi ĐÚNG dòng riêng tư, ⛔ chỉ exit 1;
    và đòi đúng ĐƯỜNG `/dong_thieu[0]/hd_mid`: email lọt qua tập 122 dòng, ⛔ chỉ qua bảng phân bố."""
    so, ghep, _c, _b = _doc_anh_doc_lap()
    d0 = min(set(so) - ghep)                                   # dòng thiếu đầu ⇒ phần tử [0] của dong_thieu
    tm = _sao_ba_anh(tmp_path / "anh")

    def phep(g):
        i_ds, i_mid = g["cot"].index("dong_sheet"), g["cot"].index("hd_mid")
        h = next(h for h in g["dong"] if h[i_ds] == d0)
        g["bang_gia_tri"].append("ke-toan@vi-du.vn")
        h[i_mid] = len(g["bang_gia_tri"]) - 1
    _sua(tm, BA_ANH[0], phep)

    r = _chay("--thu-muc", str(tm))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "riêng tư: email ở /dong_thieu[0]/hd_mid" in _loi(r), r.stderr
    assert "KẾT: ĐẠT" not in r.stdout


def test_DT1a_B4_cau_khai_khong_mang_PII_BANG_tap_may_chan():
    """★ `DT1a-R1-09` — câu `khong_mang_PII` trong hiện vật phải BẰNG tập máy chặn: bản đầu khai 5 thứ
    (*"Diễn giải · Số chứng từ · Tài khoản · tiền · email"*) mà `KHOA_CAM` chỉ canh 3 tên khoá — khai
    rộng hơn cổng là khai, ⛔ phải bằng chứng.

    Vòng sửa chọn THU câu khai (⛔ mở `KHOA_CAM`) — lý do ở docstring `KHOA_CAM` của công cụ. Bài canh
    ba điều: ① hai bản `KHOA_CAM` (tool ↔ bài — `BG-081` yếu #4) bằng nhau, sửa một bên ⇒ đỏ; ② câu khai
    nêu ĐỦ từng khoá cấm (công cụ DỰNG câu từ chính `KHOA_CAM`); ③ câu khai ⛔ còn nêu thứ máy ⛔ chặn."""
    assert tuple(_tool().KHOA_CAM) == KHOA_CAM
    khai = _kq()["khong_mang_PII"]
    for k in KHOA_CAM:
        assert k in khai, f"câu khai thiếu khoá cấm '{k}': {khai!r}"
    for x in ("Tài khoản", "tiền"):
        assert x not in khai, f"câu khai nêu '{x}' mà máy ⛔ chặn: {khai!r}"
    assert _quet_rieng_tu({"khong_mang_PII": khai})[0] == []   # chính câu khai ⛔ tự vấp máy quét


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


def test_CLI_cong_DO_thi_KHONG_ghi_de_hien_vat(tmp_path, monkeypatch):
    """★ `DT1a-R1-03` (đột biến M8) — `--ghi` trên một lượt ĐỎ ⛔ được chạm hiện vật: đây là chốt DUY
    NHẤT giữ `phan_loai_dong_thieu.json` khỏi bị ghi từ dữ liệu hỏng. R1 đảo thứ tự (ghi TRƯỚC khi xét
    lệch) ⇒ 16 bài cũ vẫn xanh.

    Gọi `main(["--ghi"])` TRONG tiến trình, `FX` → bản sao, `RA` → `tmp_path` (⛔ chạm hiện vật thật).
    Đối chứng TRƯỚC (Đ3): ảnh nguyên ⇒ exit 0 và tệp ghi ĐÚNG lần đo — chứng minh bài QUAN SÁT được một
    lần ghi; thiếu nó, *"hiện vật ⛔ đổi"* xanh cả khi đường ghi hỏng hẳn."""
    mod = _tool_moi()
    anh, ra = _tro_ve_ban_sao(monkeypatch, mod, tmp_path)
    assert mod.main(["--ghi"]) == 0
    assert json.loads(ra.read_text(encoding="utf-8")) == _kq()
    truoc = ra.read_bytes()

    _sua(anh, BA_ANH[1], _p_bo_dong_ghep)                      # phá: 123 ≠ 122
    assert mod.main(["--ghi"]) == 1
    assert ra.read_bytes() == truoc, "⛔ lượt ĐỎ đã ghi đè hiện vật"
    assert sorted(x.name for x in ra.parent.iterdir()) == [ra.name], "tệp tạm sót lại"


def test_CLI_ghi_qua_TEP_TAM_loi_luc_thay_thi_hien_vat_cu_Y_NGUYEN(tmp_path, monkeypatch, capsys):
    """★ `DT1a-R1-07` — hiện vật ghi qua tệp tạm + `os.replace`, ⛔ `write_text` thẳng lên đích
    (`11_BOI_CANH_TU_MEMORY.md` §2: *"mở tệp chế độ ghi là xoá ngay … ghi ra tệp tạm → kiểm → chép đè"*).

    Giả lập hỏng ở bước thay (`os.replace` ném `OSError`) ⇒ hiện vật CŨ y nguyên byte, tệp tạm được
    dọn, exit 1 với nguyên nhân MỘT dòng (`S0-R1-04`). Công cụ trước vòng sửa ghi thẳng ⇒ hiện vật cũ
    bị thay, exit 0 ⇒ bài ĐỎ đúng lý do."""
    mod = _tool_moi()
    _anh, ra = _tro_ve_ban_sao(monkeypatch, mod, tmp_path)
    cu = b'{"hien_vat": "cu"}\n'
    ra.write_bytes(cu)

    def hong(*_a, **_k):
        raise OSError("đĩa đầy (giả lập)")
    monkeypatch.setattr(os, "replace", hong)

    assert mod.main(["--ghi"]) == 1
    assert ra.read_bytes() == cu, "⛔ hiện vật cũ bị chạm trước khi thay xong"
    assert sorted(x.name for x in ra.parent.iterdir()) == [ra.name], "tệp tạm sót lại"
    err = capsys.readouterr().err
    assert "Traceback" not in err
    assert any(d.startswith("LOI OSError:") and "đĩa đầy" in d for d in err.splitlines()), err


def test_thieu_tep_anh_la_DO_voi_nguyen_nhan_MOT_dong(tmp_path):
    """Đ5: ⛔ đo được là ĐỎ. `S0-R1-04`: nguyên nhân đọc được trong MỘT dòng, ⛔ traceback."""
    (tmp_path / "rong").mkdir()
    r = _chay("--thu-muc", str(tmp_path / "rong"))
    assert r.returncode == 1, r.stdout + r.stderr
    assert "Traceback" not in r.stderr
    assert any(d.startswith("LOI FileNotFoundError:") for d in r.stderr.splitlines()), r.stderr
