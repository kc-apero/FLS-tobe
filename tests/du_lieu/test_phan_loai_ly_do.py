# -*- coding: utf-8 -*-
"""DT1b — gán LÝ DO cho 122 dòng sổ chưa ghép 1-1 bằng khoá đọc ở nguồn (`tools/phan_loai_ly_do.py`).

ISP 3.1.2 · Step 5 · DT1b · dải phiếu `WO-095` / `BG-096` · AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10.

⭐ Vì sao có bộ bài này. DT1a (`BG-081`, R1 `KQ-082` đo độc lập khớp) liệt kê ĐÚNG 122 dòng sổ AS-IS
   ⛔ ghép 1-1 — nhưng ⛔ nói được VÌ SAO: ảnh đóng băng đã bỏ Số CT · TK · tiền (riêng tư). DT1b gán
   mỗi dòng đúng MỘT nhãn trong bảng đóng `KHONG_CO_SAO_KE` · `KHOA_LECH` · `TRUNG_SEQ` · `KHAC`, tính
   từ khoá ghép gốc của fixture (`classifying_vs_canon.json` · `ghep_bang`):
   *"khoá = (Số chứng từ, PS Nợ, PS Có, Tài khoản, Đơn vị tiền tệ) + seq trùng"*.

⛔⛔ Khoá THẬT ⛔ đọc được ở container (`B-DATA-2`, orchestrator đo 16/11: RAW gốc `1md85t…` ⇒
   Permission denied; bản sao ADJUSTED ⇒ `get_values` hết giờ 60 s — `GAP-ORA-08`). ⇒ Mọi bài ở đây
   chạy trên dữ liệu TỔNG HỢP do CHÍNH bài dựng (`_dung`), ⛔ một giá trị thật nào: Số CT tổng hợp
   mang tiền tố `SYN`/`KCS`/`KLN`/`KLS`/`KLX`/`KH`/`NEW` hoặc là số 16 chữ số `(100.000 + dòng) × 10¹⁰`.
   Phần dùng dữ liệu THẬT của repo chỉ là HAI tập SỐ DÒNG: 9.967 `dong_sheet` của ảnh sổ và 122 dòng
   thiếu của DT1a — đúng thứ công cụ sẽ đối chiếu khi owner chạy lượt thật (O10).

⛔⛔ Mỗi bài canh một cái bẫy CÓ THẬT:
  · `DT1b-B1` — MONG của bài là THIẾT KẾ của bộ dựng (60 · 30 · 20 · 12), ⛔ chép từ công cụ; và bài
    so NHÃN TỪNG DÒNG với thiết kế, ⛔ chỉ tổng — đúng bẫy `Đ4` (`52 = 24 + 28` hay `38 + 14` đều ra 52).
  · `DT1b-B2` — fixture ghi: *"PS Nợ/Có trong .xlsx là CHUỖI có dấu phân cách ('2,730,128.00'); Số
    chứng từ dài trong L1 về dạng khoa học ('4.36619E+15'). Không chuẩn hoá hai chỗ này thì tỷ lệ ghép
    từ 98,8% rơi còn 16,6%"*. Bộ dựng viết HAI phía KHÁC DẠNG cho cùng một khoá ở mọi dòng ghép, nên
    bỏ chuẩn hoá thì cổng TÁI LẬP phải ĐỎ (bài chứng minh). Và dòng L1 bị XÁO thứ tự — ghép theo VỊ
    TRÍ là sai (bản sao 13/11 ≠ ảnh 26/08), bài chứng minh hai lần xáo ra CÙNG nhãn.
  · `DT1b-B3` — riêng tư: tệp ra ⛔ mang Số CT thô / đã chuẩn hoá, ⛔ Diễn giải. Chốt chặn của công cụ
    phải được chứng minh NỐI vào đường đo thật bằng một đầu vào BẨN (luật phòng tái phạm `DT1a-R1-01`:
    gọi hàm kiểm rời chỉ chứng minh hàm, ⛔ chứng minh nó được gọi).
  · `DT1b-B4` — chứng minh ĐỎ (Đ5) trên BẢN SAO: gán 2 nhãn cho 1 dòng ⇒ ĐỎ, trả nguyên ⇒ hết đỏ; vân
    tay tập DT1a lệch ⇒ ĐỎ — cho TỪNG tập (`DT1a-R1-02`: chứng minh một vế ⛔ phủ vế kia); thiếu đầu
    vào ⇒ mã RIÊNG `⛔ CHƯA ĐO ĐƯỢC` (3), ⛔ phải "không thấy lệch"; lượt đỏ ⛔ ghi hiện vật
    (`DT1a-R1-03` · M8).

Mã thoát (khai trong công cụ): 0 ĐẠT · 1 ĐỎ · 2 sai cách gọi · 3 ⛔ CHƯA ĐO ĐƯỢC · 4 ĐO ĐƯỢC, MONG phân
bố nhãn CHƯA GHIM (chưa có lượt thật nào — ⛔ được tính là ĐẠT).
"""
from __future__ import annotations

import csv
import functools
import hashlib
import importlib.util
import io
import json
import os
import random
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "phan_loai_ly_do.py"
DT1A = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
ANH_SO = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"
RA_THAT = GOC / "docs" / "ITL" / "_tools" / "phan_loai_ly_do_moc_20261118.json"   # WO-156

# ── MONG ĐỘC LẬP — mỗi số trỏ NƠI GHI (luật `DT1a-R1-05`), ⛔ chép từ công cụ ──────────────────────
THIEU = 122                # BG-081 `:49` · R1 KQ-082 đo độc lập `:41` (122 dòng sổ ⛔ ghép)
SO_DONG_SO = 9967          # BG-081 · KQ-082 `:35` (dòng sổ `dong_sheet` của ảnh 26/08)
SO_DONG_GHEP = 9845        # BG-081 · KQ-082 `:36` (dòng sổ ghép 1-1 — mẫu số của phép TÁI LẬP)
VAN_TAY = {"thieu": "18047e0eb0319ea1", "nguoc": "6ac2463a190ff631"}   # BG-081 `:53` · KQ-082 `:41-42`
NHAN = ("KHONG_CO_SAO_KE", "KHOA_LECH", "TRUNG_SEQ", "KHAC")           # ISP 3.1.2 `:784` (bảng đóng)
COT_VAO = ("bang", "dong", "so_ct", "ps_no", "ps_co", "tk", "tien_te")  # định dạng đầu vào (BG-096)
# Thiết kế bộ dựng `_dung` (đếm DÒNG trong 122): 60 ⛔ có sao kê · 15 lệch PS Nợ + 15 lệch Số CT ·
# 20 trùng khoá với một dòng đã ghép · 10 khớp khi ghép lại + 2 ô PS Nợ là ô lỗi.
MONG_TONG_HOP = {"KHONG_CO_SAO_KE": 60, "KHOA_LECH": 30, "TRUNG_SEQ": 20, "KHAC": 12}
# K13 (DT1b-R1-05) — vân tay DANH TÍNH nhãn của bản đọc TỔNG HỢP: sha256-16 của sorted([dong_sheet, nhan,
# lech, ghi_chu]) theo THIẾT KẾ `_dung` (⛔ chép từ công cụ — bài `…van_tay_nhan_TONG_HOP_dung_thiet_ke`
# tự tính lại từ `mong` của `_dung` và đối chiếu). Đổi chỗ nhãn 2 dòng cùng kỳ giữ nguyên số đếm nhưng ĐỔI số này.
VT_NHAN_TONG_HOP = "c5c55c272e02b414"
SO_L1_MOI = 300            # dòng L1 "mới sau 26/08" — bản sao 13/11 DÀI hơn ảnh (⛔ ghép với ai)
KHOA_DONG = {"dong_sheet", "ky", "nhan", "khoa_bam", "lech", "ghi_chu"}   # lược đồ một dòng ra
GHI_CHU_KHOP = "KHOP_KHI_GHEP_LAI"                                       # ghi chú của `KHAC` (bảng đóng)
MAU_HEX16 = re.compile(r"^[0-9a-f]{16}$")


# ═════════════════════════════════════════════════════════════════════════ trợ thủ
def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(TOOL), *doi_so], cwd=GOC, capture_output=True, text=True,
        encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})


@functools.lru_cache(maxsize=1)
def _tool():
    """Nạp công cụ TRONG thân bài (⛔ ở fixture) — công cụ chưa có thì bài FAILED vì thiếu hành vi,
    ⛔ ERROR ở khâu dựng."""
    assert TOOL.exists(), f"⛔ chưa có {TOOL.relative_to(GOC)} — hành vi DT1b chưa có"
    spec = importlib.util.spec_from_file_location("_phan_loai_ly_do", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@functools.lru_cache(maxsize=1)
def _nen() -> tuple[list[int], list[int], dict[int, str]]:
    """Hai tập SỐ DÒNG thật (⛔ giá trị nào khác): 9.967 `dong_sheet` của ảnh sổ · 122 dòng thiếu DT1a."""
    g = json.loads(ANH_SO.read_text(encoding="utf-8"))
    i = g["cot"].index("dong_sheet")
    so = sorted(h[i] for h in g["dong"])
    d = json.loads(DT1A.read_text(encoding="utf-8"))
    thieu = sorted(x["dong_sheet"] for x in d["dong_thieu"])
    ky = {x["dong_sheet"]: x["ky"] for x in d["dong_thieu"]}
    # Đ3 — mẫu số trước: hai tập phải ĐÚNG cỡ đã đo, ⛔ rỗng
    assert (len(so), len(set(so)), len(thieu), len(set(thieu))) == (SO_DONG_SO, SO_DONG_SO, THIEU, THIEU)
    assert set(thieu) <= set(so)
    return so, thieu, ky


def _tien_pc(n: int) -> str:
    """Tiền dạng CHUỖI có dấu phân cách — đúng hình `.xlsx` của fixture: 2730128 → '2,730,128.00'."""
    return f"{n:,}.00"


@functools.lru_cache(maxsize=4)
def _dung(hat_xao: int = 7) -> tuple[str, dict, dict]:
    """Dựng một bản đọc TỔNG HỢP đủ cỡ thật (9.967 dòng sổ + 10.185 dòng L1).

    Trả `(văn bản CSV, mong từng dòng {dong_sheet: (nhan, lech, ghi_chu)}, thông tin để quét riêng tư)`.
    ⛔ mượn mã công cụ: khoá, nhãn mong đợi và mọi con số đều do bài tự định.
    """
    so, thieu, _ = _nen()
    tap = set(thieu)
    ghep = [d for d in so if d not in tap]              # 9.845 dòng sổ ĐÃ ghép (theo DT1a)
    assert len(ghep) == SO_DONG_GHEP
    so_tho: dict[int, tuple] = {}
    l1_tho: list[tuple] = []
    tien_ghep: dict[int, int] = {}
    mong: dict[int, tuple] = {}
    khoa_hoc_l1 = 0

    # ① 9.845 dòng ghép: mỗi dòng một khoá riêng + đúng MỘT dòng L1 cùng khoá — viết KHÁC DẠNG ở
    #    MỌI dòng (phân cách ↔ trơn · trống ↔ "0" · hoa ↔ thường + khoảng trắng · 1/7 Số CT khoa học).
    for j, d in enumerate(ghep):
        tien = 1_000_000 + d * 1_000 + 7
        tien_ghep[d] = tien
        if j % 7 == 0:                                   # Số CT dài: sổ chữ số thường, L1 dạng khoa học
            n = (100_000 + d) * 10**10
            ct_so, ct_l1 = str(n), f"{n:.5E}"
            khoa_hoc_l1 += 1
        else:
            ct_so = ct_l1 = f"SYN{d:06d}"
        if j % 2 == 0:
            so_tho[d] = (ct_so, _tien_pc(tien), "", "1121", "VND")
            l1_tho.append((ct_l1, str(tien), "0", "1121", " vnd"))
        else:
            so_tho[d] = (ct_so, "", str(tien), "3311", "USD")
            l1_tho.append((ct_l1, "0", _tien_pc(tien), "3311", "usd "))

    # ② 122 dòng thiếu — năm kịch bản theo thứ tự dong_sheet (rải đủ 18 kỳ)
    for i, d in enumerate(thieu):
        if i < 5:      # chung Số CT với một dòng L1 ĐÃ BỊ dòng ghép khác lấy (j = 100…104) ⇒ ⛔ ứng viên:
            #            dòng L1 ấy đã có chủ — `KHOA_LECH` chỉ xét dòng L1 CHƯA AI GHÉP
            so_tho[d] = (so_tho[ghep[100 + i]][0], str(500_000_000 + d), "", "1121", "VND")
            mong[d] = ("KHONG_CO_SAO_KE", [], None)
        elif i < 60:   # ⛔ dòng L1 nào chung Số CT, ⛔ dòng L1 nào chung bốn trường còn lại
            so_tho[d] = (f"KCS{d:06d}", str(500_000_000 + d), "", "1121", "VND")
            mong[d] = ("KHONG_CO_SAO_KE", [], None)
        elif i < 75:   # L1 có dòng cùng Số CT, PS Nợ khác 1.000 ⇒ lệch đúng PS Nợ
            so_tho[d] = (f"KLN{d:06d}", _tien_pc(600_000_000 + d), "", "1121", "VND")
            l1_tho.append((f"KLN{d:06d}", str(600_001_000 + d), "", "1121", "VND"))
            mong[d] = ("KHOA_LECH", ["ps_no"], None)
        elif i < 90:   # L1 có dòng cùng PS Nợ/Có/TK/tiền tệ, Số CT khác ⇒ lệch đúng Số CT
            so_tho[d] = (f"KLS{d:06d}", "", str(700_000_000 + d), "3311", "USD")
            l1_tho.append((f"KLX{d:06d}", "0", _tien_pc(700_000_000 + d), "3311", "USD"))
            mong[d] = ("KHOA_LECH", ["so_ct"], None)
        elif i < 110:  # chung khoá với MỘT dòng đã ghép (viết khác dạng); L1 chỉ có MỘT dòng khoá ấy
            m = ghep[(i - 90) * 400]                     # j = 0, 400 … 7600 ⇒ có cả Số CT khoa học
            ct, _no, _co, tk, te = so_tho[m]
            so_tho[d] = (ct, str(tien_ghep[m]), "0", tk, te.lower())
            mong[d] = ("TRUNG_SEQ", [], None)
        elif i < 120:  # L1 CÓ dòng cùng khoá — sổ '2,730,128.00' + Số CT trơn, L1 khoa học + tiền trơn
            n = (200_000 + d) * 10**10
            so_tho[d] = (str(n), "2,730,128.00", "", "1121", "VND")
            l1_tho.append((f"{n:.5E}", "2730128", "0", "1121", "VND"))
            khoa_hoc_l1 += 1
            mong[d] = ("KHAC", [], "KHOP_KHI_GHEP_LAI")
        else:          # ô PS Nợ là ô lỗi của Sheets ⇒ khoá ⛔ so được
            so_tho[d] = (f"KH{d:06d}", "#N/A", "", "1121", "VND")
            mong[d] = ("KHAC", [], "KHOA_HONG:ps_no")

    # ③ dòng L1 "mới" (bản sao 13/11 dài hơn ảnh 26/08) — khoá riêng, tiền ≥ 9e8 ⛔ trùng ai
    for k in range(SO_L1_MOI):
        l1_tho.append((f"NEW{k:06d}", str(900_000_000 + k), "", "1121", "VND"))

    # ④ XÁO: L1 đánh số theo thứ tự sau khi xáo (dòng dữ liệu đầu = 5, như RAW); dòng CSV cũng xáo
    rnd = random.Random(hat_xao)
    rnd.shuffle(l1_tho)
    hang = [("SO", d, *so_tho[d]) for d in so] + [("L1", 5 + i, *k) for i, k in enumerate(l1_tho)]
    rnd.shuffle(hang)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(COT_VAO)
    w.writerows(hang)

    tho_ct = ({k[0] for k in so_tho.values()} | {k[0] for k in l1_tho}) - {""}
    tron = {x.replace(",", "").removesuffix(".00") for k in list(so_tho.values()) + l1_tho
            for x in (k[1], k[2])}
    tin = {"so_ct_tho": tho_ct, "tien": {x for x in tron if x.isdigit() and len(x) >= 6},
           "khoa_hoc_l1": khoa_hoc_l1, "so_dong_l1": len(l1_tho), "ct_dau": so_tho[thieu[0]][0]}
    return buf.getvalue(), mong, tin


def _ghi_csv(thu_muc: Path, van_ban: str, ten: str = "khoa.csv") -> Path:
    p = thu_muc / ten
    p.write_text(van_ban, encoding="utf-8")
    return p


def _chay_trong(monkeypatch, capsys, *argv: str, ra: Path, dt1a: Path = DT1A,
                mong_nhan="giu") -> tuple[int, str, str]:
    """Chạy `main()` TRONG tiến trình, trỏ hiện vật ra `ra` (tmp) — ⛔ bao giờ chạm tệp thật của repo."""
    tool = _tool()
    monkeypatch.setattr(tool, "DT1A", dt1a)
    monkeypatch.setattr(tool, "RA", ra)
    if mong_nhan != "giu":
        monkeypatch.setitem(tool.MONG, "phan_bo_nhan", mong_nhan)
        # K13 (DT1b-R1-05) — ghim vân tay danh tính CÙNG lượt với phân bố; chưa ghim thì cổng trả 4
        monkeypatch.setitem(tool.MONG, "van_tay_nhan", VT_NHAN_TONG_HOP)
    ma = tool.main(list(argv))
    o = capsys.readouterr()
    return ma, o.out, o.err


def _do_tong_hop(tmp_path: Path, monkeypatch, capsys, hat_xao: int = 7,
                 mong_nhan="giu") -> tuple[int, str, str, Path]:
    van_ban, _, _ = _dung(hat_xao)
    p = _ghi_csv(tmp_path, van_ban)
    ra = tmp_path / "phan_loai_ly_do.json"
    ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, mong_nhan=mong_nhan)
    return ma, out, err, ra


_HOP_LE: dict[str, str] = {}


def _ban_hop_le(tmp_path: Path, monkeypatch, capsys) -> str:
    """Văn bản JSON nhãn HỢP LỆ của bản đọc tổng hợp (đo một lần, dùng lại cho mọi bài phá bản sao)."""
    if "v" not in _HOP_LE:
        thu_muc = tmp_path / "hop_le"
        thu_muc.mkdir()
        ma, _, err, ra = _do_tong_hop(thu_muc, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
        assert ma == 0, err
        _HOP_LE["v"] = ra.read_text(encoding="utf-8")
    return _HOP_LE["v"]


def _kiem_tep(monkeypatch, capsys, tep: Path, tmp_path: Path) -> tuple[int, str, str]:
    """Chế độ CỔNG (⛔ `--khoa`): kiểm một tệp nhãn có sẵn. `RA` trỏ tmp — ⛔ bao giờ ghi ở chế độ này."""
    return _chay_trong(monkeypatch, capsys, "--tep", str(tep), ra=tmp_path / "khong_duoc_ghi.json",
                       mong_nhan=dict(MONG_TONG_HOP))


# ═════════════════════════════════════════ DT1b-B1 — Σ = 122 · mỗi dòng ĐÚNG một nhãn · bảng có MONG
def test_DT1b_B1_moi_dong_DUNG_mot_nhan_va_DUNG_thiet_ke_TUNG_dong(tmp_path, monkeypatch, capsys):
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 0, err
    assert "KẾT: ĐẠT" in out
    kq = json.loads(ra.read_text(encoding="utf-8"))
    _, mong, _ = _dung(7)
    dong = kq["dong_thieu"]
    ds = [r["dong_sheet"] for r in dong]
    assert (len(dong), len(set(ds))) == (THIEU, THIEU)
    assert set(ds) == set(_nen()[1])
    for r in dong:
        assert isinstance(r["nhan"], str) and r["nhan"] in NHAN, r
        # từng dòng = THIẾT KẾ của bộ dựng (⛔ chỉ tổng — Đ4)
        assert (r["nhan"], r["lech"], r["ghi_chu"]) == mong[r["dong_sheet"]], r["dong_sheet"]
    assert kq["dem_nhan"] == MONG_TONG_HOP
    assert sum(kq["dem_nhan"].values()) == THIEU


def test_DT1b_B1_MONG_khai_TRONG_tool_va_phan_bo_CHUA_GHIM_la_ma_4(tmp_path, monkeypatch, capsys):
    tool = _tool()
    assert tool.NHAN == NHAN
    assert (tool.MONG["thieu"], tool.MONG["so_dong_so"], tool.MONG["so_dong_ghep"]) == \
        (THIEU, SO_DONG_SO, SO_DONG_GHEP)
    assert tool.MONG["van_tay"] == VAN_TAY
    # Chưa có lượt THẬT nào (khoá thật ⛔ đọc được ở container) ⇒ phân bố nhãn CHƯA GHIM. Khi owner chạy
    # lượt thật (O10) và orchestrator chốt ghim, bài này đổi theo kèm nguồn của số — Đ5: một bản khai.
    assert tool.MONG["phan_bo_nhan"] is None
    assert tool.MONG["van_tay_nhan"] is None    # K13 ghim CÙNG lượt với phân bố (DT1b-R1-05)
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys)
    assert ma == 4, err
    assert "CHƯA GHIM" in out and "KẾT: ĐẠT" not in out
    assert ra.exists()          # đo trọn, bất biến cấu trúc đạt ⇒ được ghi để owner gửi về


def test_DT1b_B1_MONG_phan_bo_KHAC_thi_DO_va_KHONG_ghi(tmp_path, monkeypatch, capsys):
    sai = dict(MONG_TONG_HOP, KHONG_CO_SAO_KE=59, KHAC=13)       # tổng VẪN 122 — chỉ phân bố khác
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=sai)
    assert ma == 1
    assert "phân bố nhãn" in err
    assert not ra.exists()


def test_DT1b_B1_bang_nhan_theo_ky_va_MAU_SO_in_TRUOC_ty_le(tmp_path, monkeypatch, capsys):
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 0, err
    kq = json.loads(ra.read_text(encoding="utf-8"))
    _, _, ky = _nen()
    tu_dem: dict[str, Counter] = {}
    for r in kq["dong_thieu"]:
        assert r["ky"] == ky[r["dong_sheet"]]                      # kỳ lấy từ DT1a, ⛔ tự chế
        tu_dem.setdefault(r["ky"], Counter())[r["nhan"]] += 1
    assert kq["nhan_theo_ky"] == {k: {n: c[n] for n in NHAN} for k, c in tu_dem.items()}
    assert len(kq["nhan_theo_ky"]) == 18                           # BG-081: 18/23 kỳ có dòng thiếu
    # Đ3 — MẪU SỐ in TRƯỚC ký tự `%` đầu tiên, mỗi số mang nhãn NÓ ĐẾM GÌ (Đ4)
    truoc = out[:out.index("%")]
    so_l1 = f"{_dung(7)[2]['so_dong_l1']:,}".replace(",", ".")
    for cum in ("9.967 dòng sổ", "122 dòng sổ thiếu", "9.845 dòng ghép", f"{so_l1} dòng L1"):
        assert cum in truoc, cum
    for n in NHAN:
        assert n in out[out.index("%"):]


def test_DT1b_B1_tep_ra_DUNG_KHUON_hop_dong_ma_H2_doc(tmp_path, monkeypatch, capsys):
    """HỢP ĐỒNG tệp nhãn (orchestrator 16/11 — H2 đã bàn giao, `tools/do_voi_so_luong.py` sẽ ĐỌC tệp này; khác
    khuôn ⇒ đỏ lúc gộp): `{"van_tay": {"thieu": <16 hex>, "nguoc": <16 hex>}, "dong_thieu": [{"dong_sheet": <int>,
    "nhan": <chuỗi> | null}, …]}` — đúng khuôn `phan_loai_dong_thieu.json` của DT1a; vân tay = vân tay tính lại từ
    ảnh; `dong_sheet` số nguyên (⛔ `True`); khoá thừa được phép, ⛔ thay khoá bắt buộc. Bài đọc tệp RA bằng máy
    đọc của CHÍNH bài, chỉ theo khuôn ấy."""
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 0, err
    tep = json.loads(ra.read_text(encoding="utf-8"))
    assert isinstance(tep, dict)
    vt = tep["van_tay"]
    assert isinstance(vt, dict) and set(vt) >= {"thieu", "nguoc"}
    assert all(isinstance(vt[k], str) and MAU_HEX16.match(vt[k]) for k in ("thieu", "nguoc"))
    assert {k: vt[k] for k in ("thieu", "nguoc")} == VAN_TAY
    # vân tay = tính lại từ ẢNH (bài tự tính trên tập 122 dòng của ảnh qua DT1a — cùng cách băm của DT1a)
    _, thieu, _ = _nen()
    assert hashlib.sha256(json.dumps(thieu, separators=(",", ":")).encode()).hexdigest()[:16] == vt["thieu"]
    dong = tep["dong_thieu"]
    assert isinstance(dong, list) and len(dong) == THIEU
    for r in dong:
        assert isinstance(r, dict) and {"dong_sheet", "nhan"} <= set(r), r
        assert type(r["dong_sheet"]) is int, r                      # ⛔ bool (`True` là int của Python)
        assert r["nhan"] is None or (isinstance(r["nhan"], str) and r["nhan"] in NHAN), r
    assert sorted(r["dong_sheet"] for r in dong) == thieu


def test_DT1b_B1_TAI_LAP_khoa_seq_DUNG_9845_dong_ghep(tmp_path, monkeypatch, capsys):
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 0, err
    ms = json.loads(ra.read_text(encoding="utf-8"))["mau_so"]
    _, _, tin = _dung(7)
    assert ms["tai_lap"] == SO_DONG_GHEP                 # mọi dòng ghép của DT1a có dòng L1 cùng khoá
    assert (ms["thieu"], ms["so_dong_so"], ms["so_dong_ghep_dt1a"]) == (THIEU, SO_DONG_SO, SO_DONG_GHEP)
    assert ms["so_dong_l1"] == tin["so_dong_l1"]
    assert ms["dang_khoa_hoc"] == {"SO": 0, "L1": tin["khoa_hoc_l1"]}


# ═════════════════════════════════════════ DT1b-B2 — chuẩn hoá TRƯỚC khi băm · ghép theo KHOÁ
def test_DT1b_B2_so_ct_khoa_hoc_va_tien_phan_cach_bam_BANG_ban_so_thuong():
    t = _tool()
    a = t.chuan_hoa_khoa("4.36619E+15", "2,730,128.00", "", "1121", "VND")
    b = t.chuan_hoa_khoa("4366190000000000", "2730128", "0", "1121", " vnd ")
    assert a == b == ("4366190000000000", "2730128", "0", "1121", "VND")
    assert t.bam_khoa(a) == t.bam_khoa(b)
    assert MAU_HEX16.match(t.bam_khoa(a))
    # đối chứng: bài tự băm bản THÔ ⇒ khác nhau — chính chuẩn hoá làm hai bản khớp
    tho = [hashlib.sha256(json.dumps(x).encode()).hexdigest()[:16] for x in
           (["4.36619E+15", "2,730,128.00", "", "1121", "VND"], ["4366190000000000", "2730128", "0", "1121", " vnd "])]
    assert tho[0] != tho[1]
    # ô lỗi ở cột tiền ⇒ None (khoá HỎNG) — ⛔ bị coi là 0
    assert t.chuan_hoa_khoa("X1", "#N/A", "", "1121", "VND")[1] is None
    # băm phủ CẢ năm trường: đổi MỘT trường bất kỳ ⇒ băm khác (đột biến M43 16/11 — băm một trường — SỐNG
    # trước khi có vế này: mọi bài khác chỉ so hai khoá CÙNG Số CT, hoặc 122 khoá khác Số CT)
    for i, khac in enumerate(("4366190000000001", "2730129", "1", "1122", "USD")):
        b2 = list(b)
        b2[i] = khac
        assert t.bam_khoa(tuple(b2)) != t.bam_khoa(b), i


def test_DT1b_B2_bo_chuan_hoa_thi_TAI_LAP_roi_va_cong_DO(tmp_path, monkeypatch, capsys):
    """Đúng bẫy fixture ghi (98,8% → 16,6%): khoá THÔ ⇒ dòng ghép ⛔ tìm lại được dòng L1 ⇒ ĐỎ."""
    monkeypatch.setattr(_tool(), "chuan_hoa_khoa", lambda *x: tuple("" if v is None else str(v) for v in x))
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 1
    m = re.search(r"tái lập[^\n]*đo (\d+) · mong 9845", err)
    assert m, err
    assert int(m.group(1)) < SO_DONG_GHEP
    assert not ra.exists()


def test_DT1b_B2_ghep_theo_KHOA_khong_theo_VI_TRI(tmp_path, monkeypatch, capsys):
    """Bản sao 13/11 ≠ ảnh 26/08: hai bản đọc cùng khoá, KHÁC thứ tự + số dòng L1 ⇒ CÙNG nhãn, cùng băm."""
    assert _dung(7)[0] != _dung(11)[0]
    kq = []
    for hat in (7, 11):
        thu_muc = tmp_path / f"xao_{hat}"
        thu_muc.mkdir()
        ma, _, err, ra = _do_tong_hop(thu_muc, monkeypatch, capsys, hat_xao=hat, mong_nhan=dict(MONG_TONG_HOP))
        assert ma == 0, err
        kq.append(json.loads(ra.read_text(encoding="utf-8")))
    for t in ("dong_thieu", "dem_nhan", "nhan_theo_ky", "mau_so", "van_tay"):
        assert kq[0][t] == kq[1][t], t


# ═════════════════════════════════════════ DT1b-B3 — riêng tư: 0 Số CT thô · 0 Diễn giải
def _bo_dau(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def _moi_khoa(x, ra: list) -> list:
    if isinstance(x, dict):
        for k, v in x.items():
            ra.append(k)
            _moi_khoa(v, ra)
    elif isinstance(x, list):
        for v in x:
            _moi_khoa(v, ra)
    return ra


def test_DT1b_B3_tep_ra_0_so_ct_tho_0_tien_0_dien_giai(tmp_path, monkeypatch, capsys):
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 0, err
    van_ban = ra.read_text(encoding="utf-8")
    kq = json.loads(van_ban)
    _, _, tin = _dung(7)
    # máy quét RIÊNG của bài (⛔ mượn công cụ): Số CT thô · dạng trơn của số khoa học · tiền ≥ 6 chữ số
    tho = tin["so_ct_tho"]
    tron = {str(int(float(c))) for c in tho if "E+" in c}
    cam = tho | tron | tin["tien"]
    assert len(tho) >= SO_DONG_SO and len(tin["tien"]) >= SO_DONG_SO and len(tron) > 0   # Đ3: tập quét ⛔ rỗng
    token = set(re.findall(r"[0-9A-Za-z.+]+", van_ban))
    assert len(token) > 0
    assert token & cam == set()
    khoa = _moi_khoa(kq, [])
    assert len(khoa) >= 6 * THIEU                                   # Đ3: đã quét ≥ 732 khoá
    assert [k for k in khoa if any(c in _bo_dau(k) for c in ("diengiai", "sochungtu", "soct", "email"))] == []
    for r in kq["dong_thieu"]:
        assert set(r) == KHOA_DONG, r
        assert MAU_HEX16.match(r["khoa_bam"]), r
    assert len({r["khoa_bam"] for r in kq["dong_thieu"]}) == THIEU         # 122 khoá khác nhau theo thiết kế


def test_DT1b_B3_dau_vao_mang_cot_Dien_giai_bi_TU_CHOI_va_KHONG_ghi(tmp_path, monkeypatch, capsys):
    van_ban, _, _ = _dung(7)
    hang = van_ban.splitlines()
    p = _ghi_csv(tmp_path, "\n".join([hang[0] + ",Diễn giải"] + [x + ",noi dung gia" for x in hang[1:]]) + "\n")
    ra = tmp_path / "ra.json"
    ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra,
                               mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 1
    assert not ra.exists()
    assert len(err.strip().splitlines()) == 1, err                 # nguyên nhân MỘT dòng (S0-R1-04)
    assert "Diễn giải" in err and "cột" in err


def test_DT1b_B3_chot_rieng_tu_NOI_vao_duong_do_that(tmp_path, monkeypatch, capsys):
    """`DT1a-R1-01`: đầu vào BẨN đi qua đường đo thật. Kỳ của dòng thiếu đầu tiên (đọc từ JSON DT1a — vân
    tay chỉ phủ SỐ DÒNG nên vẫn khớp) bị thay bằng ① chính Số CT thô của dòng ấy trong bản đọc · ② một
    email. Chốt ⛔ nối ⇒ giá trị ấy đi thẳng vào tệp ra."""
    van_ban, _, tin = _dung(7)
    p = _ghi_csv(tmp_path, van_ban)
    dau = _nen()[1][0]
    for i, (ban, cau) in enumerate(((tin["ct_dau"], "riêng tư: Số chứng từ"), ("ke-toan@vi-du.vn", "riêng tư: email"))):
        d = json.loads(DT1A.read_text(encoding="utf-8"))
        vt = [j for j, x in enumerate(d["dong_thieu"]) if x["dong_sheet"] == dau]
        assert len(vt) == 1
        d["dong_thieu"][vt[0]]["ky"] = ban
        bs = tmp_path / f"dt1a_ban_{i}.json"
        bs.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        ra = tmp_path / f"ra_{i}.json"
        ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, dt1a=bs,
                                   mong_nhan=dict(MONG_TONG_HOP))
        assert ma == 1, (i, out)
        assert not ra.exists()
        assert cau in err, err


# ═════════════════════════════════════════ DT1b-B4 — chứng minh ĐỎ trên BẢN SAO, rồi trả nguyên
def test_DT1b_B4_hai_nhan_cho_MOT_dong_tren_BAN_SAO_thi_DO_roi_tra_nguyen(tmp_path, monkeypatch, capsys):
    goc = _ban_hop_le(tmp_path, monkeypatch, capsys)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(goc, encoding="utf-8")
    ma0, _, err0 = _kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma0 == 0, err0                                           # đối chứng
    # ① một dòng mang HAI nhãn
    d = json.loads(goc)
    ds = d["dong_thieu"][0]["dong_sheet"]
    d["dong_thieu"][0]["nhan"] = ["KHONG_CO_SAO_KE", "KHAC"]
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma1, _, err1 = _kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma1 == 1 and f"dòng {ds} mang 2 nhãn" in err1, err1
    # ② cùng dòng xuất hiện HAI lần, hai nhãn khác nhau
    d = json.loads(goc)
    r2 = dict(d["dong_thieu"][0], nhan="TRUNG_SEQ")
    assert d["dong_thieu"][0]["nhan"] != "TRUNG_SEQ"
    d["dong_thieu"].append(r2)
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma2, _, err2 = _kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma2 == 1 and f"dòng {ds} mang 2 nhãn" in err2, err2
    # ③ trả nguyên ⇒ hết đỏ
    sao.write_text(goc, encoding="utf-8")
    ma3, _, err3 = _kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma3 == 0, err3


def _dong_co(d: dict, nhan: str) -> dict:
    return next(r for r in d["dong_thieu"] if r["nhan"] == nhan)


PHA = [  # (tên, phá bản sao, cụm chữ phải có trong stderr)
    ("0_nhan", lambda d: d["dong_thieu"][0].update(nhan=None), "mang 0 nhãn"),
    ("vang_mot_dong", lambda d: d["dong_thieu"].pop(0), "mang 0 nhãn"),
    ("dong_ngoai_122", lambda d: d["dong_thieu"][0].update(dong_sheet=10), "ngoài tập 122"),
    ("nhan_la", lambda d: d["dong_thieu"][0].update(nhan="LY_DO_KHAC"), "nhãn lạ"),
    ("KHAC_thieu_ghi_chu", lambda d: _dong_co(d, "KHAC").update(ghi_chu=None), "KHAC ⛔ có ghi chú hợp lệ"),
    ("KHOA_LECH_thieu_lech", lambda d: _dong_co(d, "KHOA_LECH").update(lech=[]), "KHOA_LECH ⛔ nêu trường lệch"),
    # ba ca dưới thêm sau lượt đột biến 16/11 (M15 · M16 · M17 SỐNG): nhãn mang trường ⛔ thuộc về nó
    ("KCSK_mang_lech", lambda d: _dong_co(d, "KHONG_CO_SAO_KE").update(lech=["ps_no"]), "⛔ mang lech / ghi_chu"),
    ("KHAC_mang_lech", lambda d: _dong_co(d, "KHAC").update(lech=["so_ct"]), "KHAC ⛔ mang lech"),
    ("KHOA_LECH_mang_ghi_chu", lambda d: _dong_co(d, "KHOA_LECH").update(ghi_chu=GHI_CHU_KHOP),
     "KHOA_LECH ⛔ mang ghi_chu"),
    # Σ GIỮ 122 (KHAC +1 · KHONG_CO_SAO_KE −1): đột biến M11 16/11 SỐNG khi ca này đổi cả tổng — phép Σ cắn trước
    ("dem_nhan_lech", lambda d: d["dem_nhan"].update(KHAC=d["dem_nhan"]["KHAC"] + 1,
                                                      KHONG_CO_SAO_KE=d["dem_nhan"]["KHONG_CO_SAO_KE"] - 1),
     "dem_nhan ↔ đếm lại"),
    ("ky_lech", lambda d: d["dong_thieu"][0].update(ky="2099-01"), "kỳ"),
    ("theo_ky_lech", lambda d: next(iter(d["nhan_theo_ky"].values())).update(KHAC=99), "nhan_theo_ky"),
    ("tai_lap", lambda d: d["mau_so"].update(tai_lap=9844), "tái lập"),
    ("van_tay_tep", lambda d: d["van_tay"].update(thieu="0" * 16), "vân tay"),
    # hai ca dưới thêm theo HỢP ĐỒNG tệp nhãn của orchestrator (H2 đọc tệp này — `dong_sheet` là số nguyên,
    # ⛔ `True`; chốt riêng tư RIÊNG cho khoá thô, ⛔ dựa `KHOA_CAM` của DT1a)
    ("dong_sheet_bool", lambda d: d["dong_thieu"][0].update(dong_sheet=True), "dong_sheet ⛔ phải số nguyên"),
    ("khoa_cam_Dien_giai", lambda d: d["mau_so"]["khoa_hong"].update({"Diễn giải": "x"}), "riêng tư: khoá cấm"),
    ("khoa_ngoai_luoc_do", lambda d: d["dong_thieu"][0].update(so_chung_tu="X"), "khoá ngoài lược đồ"),
    ("email", lambda d: d.update(_vi_sao=d["_vi_sao"] + " ke-toan@vi-du.vn"), "riêng tư: email"),
    ("o_loi_nhung_ma", lambda d: d.update(_vi_sao=d["_vi_sao"] + " #N/A (Did not find value 'X1' in VLOOKUP)"),
     "riêng tư: ô lỗi"),
    ("mau_so_khai_lech", lambda d: d["mau_so"].update(so_dong_ghep_dt1a=9846), "mẫu số khai"),
    # hai ca dưới thêm sau đột biến M22 · M23 16/11 SỐNG: mỗi trường mẫu số khai một ca riêng
    ("mau_so_khai_thieu", lambda d: d["mau_so"].update(thieu=121), "mẫu số khai: dòng sổ thiếu"),
    ("mau_so_khai_so", lambda d: d["mau_so"].update(so_dong_so=9966), "mẫu số khai: dòng sổ của bản đọc"),
    ("khoa_bam_khong_hex", lambda d: d["dong_thieu"][0].update(khoa_bam="4.36619E+15"), "khoa_bam"),
    ("mau_so_0", lambda d: d["mau_so"].update(so_dong_l1=0), "mẫu số = 0"),
]


@pytest.mark.parametrize("ten, pha, cau", PHA, ids=[p[0] for p in PHA])
def test_DT1b_B4_moi_bat_bien_cua_tep_nhan_CAN_tren_ban_sao(tmp_path, monkeypatch, capsys, ten, pha, cau):
    goc = _ban_hop_le(tmp_path, monkeypatch, capsys)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(goc, encoding="utf-8")
    assert _kiem_tep(monkeypatch, capsys, sao, tmp_path)[0] == 0    # đối chứng trên chính bản sao
    d = json.loads(goc)
    pha(d)
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = _kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)
    assert cau in err, err
    assert not (tmp_path / "khong_duoc_ghi.json").exists()


def test_DT1b_B4_van_tay_DT1a_lech_thi_DO_cho_TUNG_tap(tmp_path, monkeypatch, capsys):
    """`DT1a-R1-02`: mỗi tập chứng minh RIÊNG. Đổi chỗ một số dòng ⇒ tổng y nguyên (122 · 147), tập khác."""
    van_ban, _, _ = _dung(7)
    p = _ghi_csv(tmp_path, van_ban)
    so, thieu, _ = _nen()
    ngoai = next(x for x in so if x not in set(thieu))
    for tap, khac in (("thiếu", "ngược"), ("ngược", "thiếu")):
        d = json.loads(DT1A.read_text(encoding="utf-8"))
        if tap == "thiếu":
            d["dong_thieu"][0]["dong_sheet"] = ngoai
        else:
            d["dong_nguoc"][0]["dong_canon"] = max(x["dong_canon"] for x in d["dong_nguoc"]) + 1
        bs = tmp_path / f"dt1a_{tap}.json"
        bs.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        ra = tmp_path / f"ra_{tap}.json"
        ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, dt1a=bs,
                                   mong_nhan=dict(MONG_TONG_HOP))
        assert ma == 1, out
        assert f"vân tay tập {tap}" in err and f"vân tay tập {khac}" not in err, err
        assert not ra.exists()


def test_DT1b_B4_dong_thieu_DT1a_vang_phia_SO_la_DO_co_ten(tmp_path, monkeypatch, capsys):
    """Đột biến M27 16/11 SỐNG trước bài này: thiếu chốt thì công cụ vẫn ĐỎ — nhưng vì `KeyError` (một
    dòng `LOI KeyError: 99999`), ⛔ nói được nguyên nhân. Bài đòi CÂU có tên."""
    van_ban, _, _ = _dung(7)
    p = _ghi_csv(tmp_path, van_ban)
    d = json.loads(DT1A.read_text(encoding="utf-8"))
    d["dong_thieu"].append(dict(d["dong_thieu"][0], dong_sheet=99999))
    bs = tmp_path / "dt1a_ngoai.json"
    bs.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ra = tmp_path / "ra.json"
    ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, dt1a=bs,
                               mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 1 and not ra.exists()
    assert "dòng thiếu của DT1a ⛔ có phía SO" in err, err


def test_DT1b_B4_thieu_dau_vao_la_CHUA_DO_DUOC_ma_3(tmp_path):
    for doi_so in (("--khoa", str(tmp_path / "khong_co.csv")), ("--tep", str(tmp_path / "khong_co.json"))):
        r = _chay(*doi_so)
        assert r.returncode == 3, (doi_so, r.stdout, r.stderr)
        assert "CHƯA ĐO ĐƯỢC" in r.stdout + r.stderr
        assert "KẾT: ĐẠT" not in r.stdout                           # ⛔ bao giờ "không thấy lệch"


def test_DT1b_B4_tep_nhan_THAT_cua_repo_vang_la_3_co_thi_khong_DO():
    """Hai nhánh, cả hai đều đòi một điều: ở container (⛔ khoá thật) tệp vắng ⇒ 3; owner đã nộp ⇒ ⛔ ĐỎ.

    DT1b-R1-10: khi tệp thật ĐÃ có mà MONG chưa ghim, mã công cụ trả 4 (`⛔ phải ĐẠT`). ⛔ chấp nhận 4 như
    ĐẠT (`xfail` bị đếm là "chạy" — `S0-R3-01`): còn chưa ghim ⇒ `pytest.fail` (ĐỎ thật, đường nền ghi tên)."""
    r = _chay()
    if RA_THAT.exists():
        tool = _tool()
        # WO-156: tệp nhãn THẬT khai MỐC MỚI 18/11 ⇒ phải ghim `MONG_MOC` (MONG 26/08 vẫn chưa ghim ở nhánh ấy)
        moi = json.loads(RA_THAT.read_text(encoding="utf-8")).get("nguon", {}).get("anh_so") == tool.NGUON_ANH_MOC
        mong = tool.MONG_MOC if moi else tool.MONG
        if mong["phan_bo_nhan"] is not None and mong["van_tay_nhan"] is not None:
            assert r.returncode == 0, r.stderr
        else:
            pytest.fail("tệp nhãn thật ĐÃ có mà MONG[phan_bo_nhan]/[van_tay_nhan] chưa ghim — mở WO ghim "
                        "(DT1b-R1-10); ⛔ để pytest XANH ở trạng thái 'đo được nhưng ⛔ ĐẠT'")
    else:
        assert r.returncode == 3, (r.stdout, r.stderr)
        assert "CHƯA ĐO ĐƯỢC" in r.stdout + r.stderr


def test_DT1b_R1_05_van_tay_nhan_TONG_HOP_dung_thiet_ke(tmp_path, monkeypatch, capsys):
    """DT1b-R1-05 — hằng `VT_NHAN_TONG_HOP` của bài tự tính lại từ THIẾT KẾ `_dung` (⛔ chép công cụ) và
    đối chiếu với vân tay của tệp ra thật. Hai nguồn — như MONG số dòng/vân tay DT1a."""
    _, mong, _ = _dung(7)
    bo = sorted([d, n, l, gc] for d, (n, l, gc) in mong.items())
    tu_thiet_ke = hashlib.sha256(json.dumps(bo, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
    assert tu_thiet_ke == VT_NHAN_TONG_HOP, tu_thiet_ke
    ma, out, err, ra = _do_tong_hop(tmp_path, monkeypatch, capsys, mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 0, err
    dong = json.loads(ra.read_text(encoding="utf-8"))["dong_thieu"]
    bo2 = sorted([r["dong_sheet"], r["nhan"], r["lech"], r["ghi_chu"]] for r in dong)
    vt_tep = hashlib.sha256(json.dumps(bo2, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]
    assert vt_tep == VT_NHAN_TONG_HOP, vt_tep


def test_DT1b_R1_11_duong_dan_la_thu_muc_la_2_khong_phai_3(tmp_path):
    """DT1b-R1-11 — đường dẫn CÓ mà ⛔ phải tệp thường (thư mục) là SAI CÁCH GỌI (2), ⛔ 'chưa đo' (3)."""
    d = tmp_path / "thu_muc"
    d.mkdir()
    for doi_so in (("--khoa", str(d)), ("--tep", str(d))):
        r = _chay(*doi_so)
        assert r.returncode == 2, (doi_so, r.stdout, r.stderr)
        assert "phải TỆP thường" in r.stderr, r.stderr


def test_DT1b_B4_luot_DO_KHONG_ghi_va_tap_dong_sheet_lech_la_DO(tmp_path, monkeypatch, capsys):
    """`DT1a-R1-03` M8: lượt đỏ ⛔ ghi hiện vật. Phá: bản đọc thiếu dòng sổ 10 (đánh số lệch / xuất thiếu)."""
    van_ban, _, _ = _dung(7)
    hang = van_ban.splitlines()
    assert sum(x.startswith("SO,10,") for x in hang) == 1
    p = _ghi_csv(tmp_path, "\n".join(x for x in hang if not x.startswith("SO,10,")) + "\n")
    ra = tmp_path / "ra.json"
    ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra,
                               mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 1
    assert not ra.exists()
    assert "tập dong_sheet" in err and "thiếu 1" in err, err


def test_DT1b_B4_mau_so_0_la_DO_khong_phai_0_phan_tram(tmp_path, monkeypatch, capsys):
    van_ban, _, _ = _dung(7)
    p = _ghi_csv(tmp_path, "\n".join(x for x in van_ban.splitlines() if not x.startswith("L1,")) + "\n")
    ra = tmp_path / "ra.json"
    ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra,
                               mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 1
    assert "mẫu số = 0" in err, err
    assert "%" not in out
    assert not ra.exists()


SAI_DINH_DANG = [
    ("thieu_cot_tk", lambda h: [h[0].replace(",tk,", ",")] + h[1:], "cột"),
    ("bang_la", lambda h: h + ["XX,5,A1,1,0,1121,VND"], "bang"),
    ("dong_so_trung", lambda h: h + [next(x for x in h if x.startswith("SO,"))], "trùng"),
    ("dong_khong_phai_so", lambda h: h + ["L1,abc,A1,1,0,1121,VND"], "dong"),
]


@pytest.mark.parametrize("ten, sua, cau", SAI_DINH_DANG, ids=[s[0] for s in SAI_DINH_DANG])
def test_DT1b_B4_dau_vao_sai_dinh_dang_la_DO_mot_dong(tmp_path, monkeypatch, capsys, ten, sua, cau):
    van_ban, _, _ = _dung(7)
    p = _ghi_csv(tmp_path, "\n".join(sua(van_ban.splitlines())) + "\n")
    ra = tmp_path / "ra.json"
    ma, out, err = _chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra,
                               mong_nhan=dict(MONG_TONG_HOP))
    assert ma == 1
    assert not ra.exists()
    assert len(err.strip().splitlines()) == 1 and err.startswith("LOI"), err
    assert cau in err, err


def test_CLI_sai_cach_goi_la_2():
    for doi_so, cau in ((["--ghi"], "--ghi chỉ đi cùng --khoa"),
                        (["--khoa", "a.csv", "--tep", "b.json"], "not allowed with"),
                        (["--la"], "unrecognized arguments: --la")):
        r = _chay(*doi_so)
        assert r.returncode == 2 and cau in r.stderr, (doi_so, r.stderr)
