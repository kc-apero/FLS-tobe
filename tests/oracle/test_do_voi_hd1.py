# -*- coding: utf-8 -*-
"""H2 — HD1 · cổng nhận *"lệch có tên lý do và owner ký"* (`tools/do_voi_so_luong.py` · khối `dat_hd1`).

ISP 3.1.2 · Step 4 · H2 · `WO-090` · AP v3.1.2 §5.3.1 HD1 ★ *("Lệch = 0, hoặc mỗi lệch có tên lý do và
owner ký")* · §5.3.2 AC10.

⭐ Vì sao có bộ bài này. Trên ảnh đóng băng, **122** dòng sổ AS-IS ⛔ ghép 1-1 được *(DT1a · `WO-080`)*,
   rải ở **18/23** kỳ ⇒ chỉ **5/23** kỳ đủ dòng. AP cho HD1 một lối thứ hai: lệch được CHẤP NHẬN khi
   mỗi lệch có **tên lý do** *(nhãn DT1b)* **và owner KÝ** *(sổ `so_ly_do_hd1.json`, O8 = ThuongCT)*.
   Một lối như thế là **miễn trừ** — và repo này đã cấm *"gõ tên vào danh sách miễn trừ để cổng xanh"*
   (`fls-dev` · ⛔ Cấm). Nên miễn trừ phải là **ràng buộc máy cưỡng chế**: nhãn chưa ký vẫn ĐỎ, chữ ký
   lệch số dòng là ĐỎ, tệp nhãn của một tập dòng KHÁC là ĐỎ, và số kỳ đạt có `MONG` khai trước (Đ5).

Phép phán *(một kỳ)*: **đạt HD1** ⇔ *(dòng 1-1 100 %* **hoặc** *mọi dòng thiếu của kỳ có nhãn ĐÃ KÝ)*
   **∧** *(ô Final 7 khối 100 %, mẫu số > 0)*. ⛔ gồm chế độ tự sinh — xem `H15` *(Step 43)*.

⛔⛔ Mỗi bài dưới đây canh một cái bẫy CÓ THẬT ở repo này:
  · `H2-B1` — MONG của bài thử **độc lập** với MONG của công cụ: 5 kỳ lấy từ AP v3.1.2 §5.3.1
    *("5/23 tháng đủ")* + BG-081 *(liệt kê đúng 5 kỳ ⛔ có dòng thiếu)*, và đối chiếu **hai nguồn**
    với phần bù của `phan_bo_ky_thieu` trong MONG của DT1a (Đ2).
  · `H2-B2` — ký GIẢ *(tệp tạm, ⛔ sổ thật)* đi qua **đường thật** `do()` — một bài chỉ gọi hàm phán
    rời thì chứng minh hàm, ⛔ chứng minh nó được gọi (`DT1a-R1-01`).
  · `H2-B3` — nhãn có mà chưa ký vẫn ĐỎ; ký MỘT PHẦN nhãn của kỳ vẫn ĐỎ; chữ ký lệch số dòng ĐỎ; ô
    chưa 100 % thì chữ ký ⛔ cứu được kỳ.
  · `H2-B4` — cổng phải được CHỨNG MINH ĐỎ, **cả hai chiều** (Đ5): MONG thiếu một kỳ ⇒ ĐỎ; MONG thừa
    một kỳ ⇒ ĐỎ; MONG mất khoá ⇒ ĐỎ một dòng *(⛔ traceback — `S0-R1-04`)*; rồi tệp ⛔ đổi byte nào.
  · Mỗi phép kiểm đầu vào mới là một cổng ⇒ mỗi phép có **ca phá riêng** dẫn từ MỘT đầu vào hợp lệ
    *(đối chứng xanh)* bằng đúng MỘT đột biến (`DT1a-R1-03`); hai vân tay mỗi cái một ca (`DT1a-R1-02`).
"""
from __future__ import annotations

import copy
import functools
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "do_voi_so_luong.py"
TOOL_DT1A = GOC / "tools" / "phan_loai_dong_thieu.py"
RA = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
SO_LY_DO = GOC / "docs" / "ITL" / "_tools" / "so_ly_do_hd1.json"
NHAN = GOC / "docs" / "ITL" / "_tools" / "phan_loai_ly_do.json"
DT1A_JSON = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"

# ── MONG ĐỘC LẬP — ⛔ chép từ tool ─────────────────────────────────────────────────────────────────
# AP v3.1.2 §5.3.1 HD1 ★: "dòng ghép 1-1: 9.845/9.967 (98,8%) — 5/23 tháng đủ"; BG-081 §Bảng đếm:
# "5 kỳ ⛔ có dòng thiếu: 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04". Ô Final 7 khối: 23/23 tháng.
KY_DAT_SO_RONG = ("2024-10", "2024-11", "2024-12", "2025-03", "2025-04")
SO_KY = 23                     # AP v3.1.2 §5.3.1 · test_pham_vi_hien_vat_dung_nhu_khai
SO_DONG_SO = 9967              # dòng sổ AS-IS (tests/ledger/test_parity_ca_so.py)
SO_DONG_GHEP = 9845            # dòng sổ ghép 1-1 (tests/ledger/test_classifying.py)
THIEU = 122                    # = 9.967 − 9.845 (DT1a · BG-081)
THIEU_2026_07 = 23             # BG-081 §Bảng đếm, hàng 2026-07
VAN_TAY_DT1A = {"thieu": "18047e0eb0319ea1", "nguoc": "6ac2463a190ff631"}   # BG-081 · MONG DT1a
KY_GIA = "2026-07"             # kỳ ISP H2-B2 ký giả — kỳ nhiều dòng thiếu nhất (23/686 dòng sổ)
NGUOI_KY_GIA = "TONG_HOP_TEST"  # ⛔ tên người thật: chữ ký TỔNG HỢP chỉ sống trong tệp tạm của bài


# ═════════════════════════════════════════════════════════════════════════ trợ thủ
def _nap_tep(duong: Path, ten: str):
    spec = importlib.util.spec_from_file_location(ten, duong)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@functools.lru_cache(maxsize=1)
def _dv():
    """Nạp công cụ TRONG thân bài (⛔ ở fixture) — thiếu hành vi thì bài FAILED, ⛔ ERROR ở khâu dựng."""
    return _nap_tep(TOOL, "_do_voi_so_luong_h2")


def _can(ten: str):
    """Hành vi H2 chưa có ⇒ bài FAILED với câu đọc được (⛔ AttributeError trần)."""
    dv = _dv()
    if not hasattr(dv, ten):
        pytest.fail(f"⛔ tools/do_voi_so_luong.py chưa có `{ten}` — hành vi H2 chưa có")
    return getattr(dv, ten)


@functools.lru_cache(maxsize=1)
def _dt1a_tool():
    """Công cụ DT1a — chỉ để đọc MONG của nó (nguồn thứ hai, Đ2)."""
    return _nap_tep(TOOL_DT1A, "_phan_loai_dong_thieu_h2")


@functools.lru_cache(maxsize=1)
def _kq() -> dict:
    """Một lần đo trên đường thật, tệp mặc định (sổ lý do thật · tệp nhãn ở chỗ mặc định nếu có)."""
    return _dv().do()


def _json(d) -> dict:
    """Khứ hồi JSON — tuple thành list, giống hệt tệp `--ghi` ghi ra."""
    return json.loads(json.dumps(d, ensure_ascii=False))


@functools.lru_cache(maxsize=1)
def _dt1a() -> dict:
    return json.loads(DT1A_JSON.read_text(encoding="utf-8"))


def _thieu() -> list[tuple[int, str]]:
    """122 dòng thiếu `(dong_sheet, kỳ)` — lấy từ hiện vật DT1a, ⛔ từ công cụ đang kiểm."""
    return [(x["dong_sheet"], x["ky"]) for x in _dt1a()["dong_thieu"]]


def _theo_ky_da_ghi() -> dict:
    """Bốn số mỗi kỳ của lần đo ĐÃ GHI (`voi_so_luong.json`) — bài B1 ghim tệp ấy bằng lần đo hiện tại."""
    return json.loads(RA.read_text(encoding="utf-8"))["theo_ky"]


def _gan_mac_dinh() -> dict[int, str]:
    """Nhãn TỔNG HỢP: dòng thiếu của kỳ ký giả mang `TONG_HOP_A`, mọi dòng khác `TONG_HOP_B`."""
    return {d: ("TONG_HOP_A" if k == KY_GIA else "TONG_HOP_B") for d, k in _thieu()}


def _nhan_dict(gan: dict[int, str | None], van_tay: dict | None = None) -> dict:
    """Tệp nhãn theo hợp đồng H2 đọc (khuôn của chính `phan_loai_dong_thieu.json`)."""
    return {"van_tay": dict(van_tay or VAN_TAY_DT1A),
            "dong_thieu": [{"dong_sheet": d, "nhan": n} for d, n in gan.items()]}


def _chu_ky(nhan: str, so_dong: int) -> dict:
    return {"nhan": nhan, "so_dong": so_dong, "nguoi_ky": NGUOI_KY_GIA, "ngay": "2026-11-16"}


def _ghi(duong: Path, d) -> Path:
    duong.write_text(d if isinstance(d, str) else json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return duong


def _do_do(**kw) -> str:
    """Gọi `do()` trên đường thật và ĐÒI nó ĐỎ — trả thông điệp ĐỎ."""
    with pytest.raises(SystemExit) as e:
        _dv().do(**kw)
    assert isinstance(e.value.code, str), f"ĐỎ phải mang câu đọc được, ⛔ mã trần: {e.value.code!r}"
    return e.value.code


def _dong_mong_hd1(thong_diep: str) -> tuple[list[str], list[str]]:
    """Tách vế `đo` / `mong` của dòng lệch `dat_hd1_theo_ky` — mẫu khớp ĐÚNG một dòng (Đ5)."""
    dong = [x for x in thong_diep.splitlines() if "dat_hd1_theo_ky" in x]
    assert len(dong) == 1, f"mẫu `dat_hd1_theo_ky` phải khớp đúng 1 dòng — khớp {len(dong)}: {thong_diep}"
    m = re.search(r"đo (\(.*?\)) · mong (\(.*?\))", dong[0])
    assert m, dong[0]
    return re.findall(r"'([0-9]{4}-[0-9]{2})'", m.group(1)), re.findall(r"'([0-9]{4}-[0-9]{2})'", m.group(2))


def _chay_cli(*doi_so: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, capture_output=True, text=True,
                          encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})


def _chay_pha(ma_pha: str, *doi_so: str) -> subprocess.CompletedProcess:
    """Chạy `main()` của công cụ sau khi PHÁ `MONG` TRONG BỘ NHỚ — tệp nguồn ⛔ chạm."""
    ma = ("import sys; sys.path.insert(0, %r); import tools.do_voi_so_luong as t; %s; t.main()"
          % (str(GOC), ma_pha))
    return subprocess.run([sys.executable, "-c", ma, *doi_so], cwd=GOC, capture_output=True, text=True,
                          encoding="utf-8", env={**os.environ, "PYTHONUTF8": "1"})


def _sha_tep(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


# ═════════════════════════════════════════════════════════════════════════ H2-B1 · cổng · sổ rỗng
def test_H2_B1_so_ly_do_khoi_tao_RONG_0_chu_ky():
    """ISP mục 3 + 7: sổ lý do khởi tạo RỖNG — 0 chữ ký; O8 (ThuongCT) ký thật về sau, ⛔ agent."""
    assert SO_LY_DO.exists(), f"⛔ chưa có {SO_LY_DO.relative_to(GOC)} — hiện vật H2 chưa có"
    so = json.loads(SO_LY_DO.read_text(encoding="utf-8"))
    assert so.get("chu_ky") == [], f"sổ lý do phải RỖNG lúc khởi tạo — có {so.get('chu_ky')!r}"
    assert "O8" in so.get("_vi_sao", ""), "sổ phải tự nói ai ký (O8) — người đọc tệp ⛔ phải đi tìm ISP"


def test_H2_B1_hai_nguon_cho_5_ky_dat_khop_nhau():
    """Đ2 — MONG độc lập (AP + BG-081) ↔ phần bù kỳ có dòng thiếu trong MONG của DT1a (23 − 18 = 5)."""
    dt1a = _dt1a_tool()
    tat_ca = sorted(_theo_ky_da_ghi())
    assert len(tat_ca) == SO_KY
    phan_bu = tuple(k for k in tat_ca if k not in dt1a.MONG["phan_bo_ky_thieu"])
    assert phan_bu == KY_DAT_SO_RONG, phan_bu


def test_H2_B1_so_rong_ky_dat_DUNG_5_tren_23():
    """Sổ rỗng ⇒ kỳ đạt = 5 (= AP v3.1.2). Mẫu số in trong khối, mọi kỳ đỏ mang số dòng thiếu của DT1a."""
    kq = _kq()
    assert "dat_hd1" in kq, "⛔ voi_so_luong chưa có khối `dat_hd1` — trường mới chưa có"
    h = kq["dat_hd1"]
    # Đ3 — mẫu số TRƯỚC: 23 kỳ · 9.967 dòng sổ · 122 dòng thiếu (⛔ tập rỗng)
    assert h["mau_so"] == {"so_ky": SO_KY, "dong_so": SO_DONG_SO, "dong_thieu": THIEU}, h["mau_so"]
    assert h["so_chu_ky"] == 0
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG
    assert h["so_ky_dat"] == len(KY_DAT_SO_RONG) == 5
    assert h["dem"]["da_ky"] == 0
    phan_bo = _dt1a_tool().MONG["phan_bo_ky_thieu"]
    assert sorted(h["theo_ky"]) == sorted(_theo_ky_da_ghi())
    for k, x in h["theo_ky"].items():
        assert x["thieu"] == phan_bo.get(k, 0), (k, x)
        assert x["dat"] is (k in KY_DAT_SO_RONG), (k, x)
        assert x["o_100"] is True, (k, x)                      # ô 23/23 kỳ (AP §5.3.1)
    # tệp nhãn DT1b: vắng ⇒ 0 dòng có nhãn; có ⇒ đếm của tệp (⛔ đổi số kỳ đạt khi sổ rỗng)
    assert h["tep_nhan"]["co"] is NHAN.exists()
    if not NHAN.exists():
        assert h["dem"]["co_nhan"] == 0


def test_H2_B1_MONG_dat_hd1_theo_ky_khai_TRUOC_va_giu_khoa_DT1a_dung():
    """MONG mới khai trước (Đ5); `_sha` + khoá MONG cũ mà DT1a import giữ nguyên tên + nghĩa (`DT1a-R1-06`)."""
    dv = _dv()
    assert "dat_hd1_theo_ky" in dv.MONG, "⛔ MONG chưa khai `dat_hd1_theo_ky`"
    assert tuple(dv.MONG["dat_hd1_theo_ky"]) == KY_DAT_SO_RONG
    # hai nguồn cho checksum: MONG của công cụ ↔ checksum DT1a đã ghi vào hiện vật của nó
    assert dv.MONG["checksum"] == _dt1a()["nguon"]["checksum"]
    for khoa, gia_tri in (("so_dong_so", SO_DONG_SO), ("so_ky", SO_KY), ("so_dong_ghep_canon", SO_DONG_GHEP),
                          ("so_dong_bank", 9992)):
        assert dv.MONG[khoa] == gia_tri, khoa
    assert dv._sha([1], [2]) == hashlib.sha256(b"[[1],[2]]").hexdigest()[:16]


def test_H2_B1_van_tay_tap_dong_TRUNG_DT1a():
    """Khoá ghép của tệp nhãn = hai vân tay của DT1a. H2 tính lại từ ảnh — phải BẰNG cả hiện vật DT1a lẫn BG-081."""
    h = _kq()["dat_hd1"]
    assert h["van_tay"] == _dt1a()["van_tay"] == VAN_TAY_DT1A


def test_H2_B1_json_DA_GHI_khop_lan_do_hien_tai():
    """`voi_so_luong.json` đã commit = lần đo hiện tại (⛔ sửa tay; quên `--ghi` là ĐỎ)."""
    da_ghi = json.loads(RA.read_text(encoding="utf-8"))
    assert "dat_hd1" in da_ghi, "⛔ voi_so_luong.json chưa có `dat_hd1` — chưa `--ghi`"
    assert da_ghi == _json(_kq())


def test_H2_B1_CLI_in_MAU_SO_truoc_ty_le_va_hang_Sigma_y_nguyen():
    """Đ3: mẫu số in TRƯỚC `5/23`; hàng Σ (K6 của dung_moi_truong_isp.sh đọc) vẫn `9967 9845`."""
    r = _chay_cli()
    assert r.returncode == 0, r.stderr
    assert re.search(r"^Σ\s+9967\s+9845\s", r.stdout, re.M), r.stdout[-600:]
    dong = r.stdout.splitlines()
    i_mau = [i for i, x in enumerate(dong) if x.startswith("HD1") and "MẪU SỐ" in x]
    i_dat = [i for i, x in enumerate(dong) if x.startswith("HD1") and "kỳ đạt" in x]
    assert len(i_mau) == 1 and len(i_dat) == 1, f"⛔ CLI chưa in đúng một dòng HD1 mẫu số + một dòng kỳ đạt: {dong[-8:]}"
    assert i_mau[0] < i_dat[0] and "5/23" in dong[i_dat[0]], dong[-8:]
    dong_mau = dong[i_mau[0]]
    assert "23 kỳ" in dong_mau and f"{THIEU} dòng thiếu" in dong_mau and f"{SO_DONG_SO} dòng sổ" in dong_mau, dong_mau


def test_H2_B1_tep_DT1a_dung_lam_tep_nhan_hop_le_0_nhan():
    """Hợp đồng tệp nhãn = khuôn của chính `phan_loai_dong_thieu.json` (`van_tay` + `dong_thieu[].nhan`).
    Hiện vật DT1a (mọi `nhan = null`) phải là một tệp nhãn HỢP LỆ, 0 nhãn ⇒ 5 kỳ — DT1b ghi đúng khuôn ấy
    thì H2 đọc được ngay."""
    phan_hd1 = _can("phan_hd1")
    h, loi = phan_hd1(_theo_ky_da_ghi(), _thieu(), dict(VAN_TAY_DT1A), DT1A_JSON, SO_LY_DO)
    assert loi == [], loi
    assert h["tep_nhan"]["co"] is True and h["dem"]["co_nhan"] == 0
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG


# ═════════════════════════════════════════════════════════════════════════ H2-B2 · ký giả 2026-07
def test_H2_B2_ky_gia_moi_dong_2026_07_thi_2026_07_DAT_tong_6(tmp_path):
    """Ký giả nhãn của MỌI dòng thiếu 2026-07 (23 dòng) ⇒ 2026-07 đạt; tổng 6 = 5 + 1."""
    phan_hd1 = _can("phan_hd1")
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(_gan_mac_dinh()))
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", THIEU_2026_07)]})
    h, loi = phan_hd1(_theo_ky_da_ghi(), _thieu(), dict(VAN_TAY_DT1A), nhan, so)
    assert loi == [], loi
    assert tuple(h["ky_dat"]) == tuple(sorted(KY_DAT_SO_RONG + (KY_GIA,)))
    assert h["so_ky_dat"] == 6
    x = h["theo_ky"][KY_GIA]
    assert (x["thieu"], x["co_nhan"], x["da_ky"], x["dong_100"], x["o_100"], x["dat"]) == \
        (THIEU_2026_07, THIEU_2026_07, THIEU_2026_07, False, True, True), x
    assert h["dem"] == {"thieu": THIEU, "co_nhan": THIEU, "da_ky": THIEU_2026_07}
    # ⛔ chữ ký của 2026-07 ⛔ lan sang kỳ khác: mọi kỳ còn lại giữ nguyên phán của sổ rỗng
    for k, y in h["theo_ky"].items():
        if k != KY_GIA:
            assert y["dat"] is (k in KY_DAT_SO_RONG), (k, y)


def test_H2_B2_qua_DUONG_THAT_do_6_ky_va_cong_DO_vi_khac_MONG_5(tmp_path):
    """Cùng ký giả, đi qua `do()` thật: cổng ĐỎ vì đo 6 kỳ ≠ MONG 5 — chính là Đ5 làm việc (một chữ ký
    thật về sau BUỘC khai lại MONG), và chứng minh `do()` ĐỌC cả tệp nhãn lẫn sổ lý do được truyền vào."""
    _can("phan_hd1")
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(_gan_mac_dinh()))
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", THIEU_2026_07)]})
    do_, mong = _dong_mong_hd1(_do_do(nhan=nhan, so_ly_do=so))
    assert do_ == sorted(KY_DAT_SO_RONG + (KY_GIA,)) and len(do_) == 6, do_
    assert mong == list(KY_DAT_SO_RONG), mong


# ═════════════════════════════════════════════════════════════════════════ H2-B3 · nhãn chưa ký vẫn đỏ
def test_H2_B3_co_nhan_ma_CHUA_KY_van_do_qua_duong_that(tmp_path):
    """Mọi 122 dòng có nhãn, sổ RỖNG (sổ thật) ⇒ ⛔ kỳ nào thêm: vẫn 5; 2026-07 đỏ dù 23/23 dòng có nhãn."""
    _can("phan_hd1")
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(_gan_mac_dinh()))
    kq = _dv().do(nhan=nhan, so_ly_do=SO_LY_DO)               # ⛔ SystemExit: 5 = MONG
    h = kq["dat_hd1"]
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG
    assert h["dem"] == {"thieu": THIEU, "co_nhan": THIEU, "da_ky": 0}
    x = h["theo_ky"][KY_GIA]
    assert (x["co_nhan"], x["da_ky"], x["dat"]) == (THIEU_2026_07, 0, False), x


def test_H2_B3_ky_MOT_PHAN_nhan_cua_ky_thi_ky_VAN_do(tmp_path):
    """2026-07 mang hai nhãn (22 + 1), chỉ ký một ⇒ 22/23 dòng đã ký ⇒ kỳ VẪN đỏ ('mọi dòng')."""
    phan_hd1 = _can("phan_hd1")
    gan = _gan_mac_dinh()
    dong_ky = sorted(d for d, k in _thieu() if k == KY_GIA)
    assert len(dong_ky) == THIEU_2026_07                       # Đ3 — tập ⛔ rỗng, đúng 23
    gan[dong_ky[-1]] = "TONG_HOP_C"
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(gan))
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", THIEU_2026_07 - 1)]})
    h, loi = phan_hd1(_theo_ky_da_ghi(), _thieu(), dict(VAN_TAY_DT1A), nhan, so)
    assert loi == [], loi
    x = h["theo_ky"][KY_GIA]
    assert (x["co_nhan"], x["da_ky"], x["dat"]) == (THIEU_2026_07, THIEU_2026_07 - 1, False), x
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG


def test_H2_B3_chu_ky_LECH_so_dong_la_DO_qua_duong_that(tmp_path):
    """Owner ký 'TONG_HOP_A · 22 dòng' mà tệp nhãn có 23 dòng mang nhãn ấy ⇒ chữ ký CŨ ⇒ ĐỎ, ⛔ lặng lẽ
    phủ thêm dòng thứ 23 mà owner chưa thấy."""
    _can("phan_hd1")
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(_gan_mac_dinh()))
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", THIEU_2026_07 - 1)]})
    tb = _do_do(nhan=nhan, so_ly_do=so)
    assert "số dòng" in tb and "TONG_HOP_A" in tb, tb


def test_H2_B3_chu_ky_khi_tep_nhan_VANG_la_DO_qua_duong_that(tmp_path):
    """Sổ có chữ ký mà tệp nhãn vắng ⇒ chữ ký trỏ 0 dòng ⇒ ĐỎ (⛔ đo được, ⛔ 'không thấy lệch')."""
    _can("phan_hd1")
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", 1)]})
    tb = _do_do(nhan=tmp_path / "vang.json", so_ly_do=so)
    assert "số dòng" in tb and "TONG_HOP_A" in tb, tb


def test_H2_B3_o_chua_100_thi_chu_ky_KHONG_cuu_duoc_ky(tmp_path):
    """Vế 'ô 100 %' ⛔ miễn trừ được: 2026-07 đã ký đủ mà một ô lệch ⇒ đỏ; kỳ đủ dòng (2024-10) mà một ô
    lệch ⇒ đỏ; mẫu số ô = 0 ⇒ đỏ (Đ3 — ⛔ '0/0 = 100 %')."""
    phan_hd1 = _can("phan_hd1")
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(_gan_mac_dinh()))
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", THIEU_2026_07)]})
    tk = copy.deepcopy(_theo_ky_da_ghi())
    tk[KY_GIA]["o_parity_khop"] -= 1
    tk["2024-10"]["o_parity_khop"] -= 1
    tk["2024-11"]["o_parity"] = tk["2024-11"]["o_parity_khop"] = 0
    h, loi = phan_hd1(tk, _thieu(), dict(VAN_TAY_DT1A), nhan, so)
    assert loi == [], loi
    for k in (KY_GIA, "2024-10", "2024-11"):
        assert (h["theo_ky"][k]["o_100"], h["theo_ky"][k]["dat"]) == (False, False), (k, h["theo_ky"][k])
    assert tuple(h["ky_dat"]) == ("2024-12", "2025-03", "2025-04")


# ═════════════════════════════════════════════════════════════════════════ H2-B4 · phá MONG
def test_H2_B4_pha_MONG_ca_hai_chieu_cong_DO_roi_tra_nguyen():
    """Phá MONG trong bộ nhớ (⛔ chạm tệp): thiếu một kỳ ⇒ exit 1; thừa một kỳ ⇒ exit 1; mất khoá ⇒ exit 1
    một dòng; phá + `--ghi` ⇒ exit 1 và `voi_so_luong.json` ⛔ đổi byte nào; trả nguyên ⇒ exit 0."""
    _can("phan_hd1")
    sha_tool, sha_ra = _sha_tep(TOOL), _sha_tep(RA)
    ca = {
        "thiếu một kỳ": "t.MONG['dat_hd1_theo_ky'] = %r" % (KY_DAT_SO_RONG[:-1],),
        "thừa một kỳ": "t.MONG['dat_hd1_theo_ky'] = %r" % (tuple(sorted(KY_DAT_SO_RONG + (KY_GIA,))),),
        "mất khoá": "del t.MONG['dat_hd1_theo_ky']",
    }
    for ten, ma in ca.items():
        r = _chay_pha(ma)
        assert r.returncode == 1, (ten, r.returncode, r.stderr[-800:])
        assert "dat_hd1_theo_ky" in r.stderr, (ten, r.stderr[-800:])
        assert "Traceback" not in r.stderr, (ten, r.stderr[-800:])        # S0-R1-04
    r = _chay_pha(ca["thừa một kỳ"], "--ghi")
    assert r.returncode == 1 and "đã ghi" not in r.stdout, r.stdout[-400:]
    assert _sha_tep(RA) == sha_ra, "⛔ cổng ĐỎ mà vẫn ghi voi_so_luong.json"
    r = _chay_cli()                                                  # trả nguyên = MONG thật
    assert r.returncode == 0, r.stderr[-800:]
    assert _sha_tep(TOOL) == sha_tool


# ═════════════════════════════════════════════════════════════════════════ kiểm đầu vào — mỗi luật một ca
def _dau_vao_hop_le() -> tuple[dict, dict]:
    """Đầu vào HỢP LỆ dùng chung: 122 nhãn + một chữ ký đúng số dòng — mỗi ca phá đổi đúng MỘT chỗ."""
    return _nhan_dict(_gan_mac_dinh()), {"chu_ky": [_chu_ky("TONG_HOP_A", THIEU_2026_07)]}


def _ngoai_tap() -> int:
    tap = {d for d, _ in _thieu()}
    return next(i for i in range(1, 10 ** 6) if i not in tap)


def _pha_nhan(f):
    def ap(nhan, so):
        f(nhan)
        return nhan, so
    return ap


def _pha_so(f):
    def ap(nhan, so):
        f(so)
        return nhan, so
    return ap


def _dat(d: dict, khoa, gia_tri):
    d[khoa] = gia_tri


CA_PHA = {
    # ── tệp nhãn (DT1b) ──
    "nhan_json_hong": (lambda n, s: ("{hỏng", s), "tệp nhãn"),
    "nhan_khong_phai_dict": (lambda n, s: ([], s), "cấu trúc"),
    "nhan_thieu_van_tay": (_pha_nhan(lambda n: n.pop("van_tay")), "cấu trúc"),
    "nhan_thieu_dong_thieu": (_pha_nhan(lambda n: n.pop("dong_thieu")), "cấu trúc"),
    "nhan_van_tay_THIEU_sai": (_pha_nhan(lambda n: _dat(n["van_tay"], "thieu", "0" * 16)), "vân tay tập thiếu"),
    "nhan_van_tay_NGUOC_sai": (_pha_nhan(lambda n: _dat(n["van_tay"], "nguoc", "0" * 16)), "vân tay tập ngược"),
    "nhan_dong_sheet_chuoi": (_pha_nhan(lambda n: _dat(n["dong_thieu"][0], "dong_sheet", "744")), "dong_sheet"),
    "nhan_dong_sheet_bool": (_pha_nhan(lambda n: _dat(n["dong_thieu"][0], "dong_sheet", True)), "dong_sheet"),
    "nhan_dong_ngoai_tap": (_pha_nhan(lambda n: n["dong_thieu"].append({"dong_sheet": _ngoai_tap(), "nhan": "TONG_HOP_B"})),
                            "ngoài tập"),
    "nhan_dong_trung": (_pha_nhan(lambda n: n["dong_thieu"].append(dict(n["dong_thieu"][0]))), "trùng"),
    "nhan_rong": (_pha_nhan(lambda n: _dat(n["dong_thieu"][0], "nhan", "  ")), "nhãn"),
    "nhan_kieu_la": (_pha_nhan(lambda n: _dat(n["dong_thieu"][0], "nhan", 5)), "nhãn"),
    # ── sổ lý do ──
    "so_json_hong": (lambda n, s: (n, "{"), "sổ lý do"),
    "so_cau_truc": (lambda n, s: (n, {}), "cấu trúc"),
    "so_thieu_khoa": (_pha_so(lambda s: s["chu_ky"][0].pop("ngay")), "khoá"),
    "so_thua_khoa": (_pha_so(lambda s: _dat(s["chu_ky"][0], "ky", KY_GIA)), "khoá"),
    "so_nhan_rong": (_pha_so(lambda s: _dat(s["chu_ky"][0], "nhan", " ")), "nhãn"),
    "so_so_dong_0": (_pha_so(lambda s: _dat(s["chu_ky"][0], "so_dong", 0)), "so_dong"),
    "so_so_dong_bool": (_pha_so(lambda s: _dat(s["chu_ky"][0], "so_dong", True)), "so_dong"),
    "so_so_dong_chuoi": (_pha_so(lambda s: _dat(s["chu_ky"][0], "so_dong", "23")), "so_dong"),
    "so_nguoi_ky_rong": (_pha_so(lambda s: _dat(s["chu_ky"][0], "nguoi_ky", "")), "người ký"),
    "so_ngay_sai_khuon": (_pha_so(lambda s: _dat(s["chu_ky"][0], "ngay", "16/11/2026")), "ngày"),
    "so_ngay_khong_co_that": (_pha_so(lambda s: _dat(s["chu_ky"][0], "ngay", "2026-02-30")), "ngày"),
    "so_nhan_ky_trung": (_pha_so(lambda s: s["chu_ky"].append(dict(s["chu_ky"][0]))), "trùng"),
    "so_lech_so_dong": (_pha_so(lambda s: _dat(s["chu_ky"][0], "so_dong", THIEU_2026_07 + 1)), "số dòng"),
    "so_nhan_khong_ai_gan": (_pha_so(lambda s: s["chu_ky"].append(_chu_ky("KHONG_AI_GAN", 1))), "số dòng"),
}


def test_H2_kiem_dau_vao_DOI_CHUNG_hop_le_0_loi(tmp_path):
    """Đối chứng: đầu vào gốc của mọi ca phá là HỢP LỆ — mỗi ĐỎ dưới đây do đúng một đột biến."""
    phan_hd1 = _can("phan_hd1")
    n, s = _dau_vao_hop_le()
    h, loi = phan_hd1(_theo_ky_da_ghi(), _thieu(), dict(VAN_TAY_DT1A),
                      _ghi(tmp_path / "n.json", n), _ghi(tmp_path / "s.json", s))
    assert loi == [] and h is not None and h["so_ky_dat"] == 6, loi


@pytest.mark.parametrize("ten", sorted(CA_PHA))
def test_H2_kiem_dau_vao_moi_luat_CAN(ten, tmp_path):
    """Mỗi phép kiểm đầu vào là một cổng ⇒ có ca phá riêng (`DT1a-R1-03`). Đầu vào lỗi ⇒ ⛔ phán kỳ nào
    (khối = None) — ⛔ đo được là ĐỎ (Đ5), ⛔ rơi về 'chưa có nhãn' cho êm."""
    phan_hd1 = _can("phan_hd1")
    pha, mau = CA_PHA[ten]
    n, s = pha(*_dau_vao_hop_le())
    h, loi = phan_hd1(_theo_ky_da_ghi(), _thieu(), dict(VAN_TAY_DT1A),
                      _ghi(tmp_path / "n.json", n), _ghi(tmp_path / "s.json", s))
    assert h is None, f"{ten}: đầu vào lỗi mà vẫn phán kỳ"
    # ĐÚNG một lỗi, của ĐÚNG nguồn bị phá, mang ĐÚNG luật — ⛔ "có lỗi nào đó" (một đột biến, một luật cắn)
    assert len(loi) == 1, (ten, loi)
    assert loi[0].startswith("tệp nhãn" if ten.startswith("nhan_") else "sổ lý do"), (ten, loi)
    assert mau in loi[0], (ten, mau, loi)
    assert all("\n" not in x for x in loi), loi                          # S0-R1-04 — mỗi nguyên nhân MỘT dòng


def test_H2_kiem_so_ly_do_VANG_la_DO_qua_duong_that(tmp_path):
    """Sổ lý do là hiện vật của H2 — vắng ⇒ ĐỎ (⛔ coi như 'sổ rỗng': mất sổ ⛔ được trông như chưa ai ký)."""
    _can("phan_hd1")
    tb = _do_do(so_ly_do=tmp_path / "vang.json")
    assert "sổ lý do" in tb and "Traceback" not in tb, tb


def test_H2_kiem_tep_nhan_HONG_la_DO_qua_duong_that(tmp_path):
    """Tệp nhãn có mà hỏng ⇒ ĐỎ trên đường thật, nguyên nhân MỘT dòng (`S0-R1-04`)."""
    _can("phan_hd1")
    tb = _do_do(nhan=_ghi(tmp_path / "n.json", "{hỏng"), so_ly_do=SO_LY_DO)
    dong = [x for x in tb.splitlines() if "tệp nhãn" in x]
    assert len(dong) == 1 and "Traceback" not in tb, tb


def test_H2_phong_thu_chong_co_tru_chay_KHAC_dong_thieu_liet_ke_la_DO(tmp_path):
    """Phòng thủ chồng (Đ2 — hai nguồn): `có − chạy` của kỳ ↔ số dòng thiếu liệt kê phải bằng nhau; và
    dòng thiếu ⛔ được thuộc kỳ ngoài bảng bốn số. Mỗi phép một ca phá (`DT1a-R1-03`), đúng MỘT lỗi."""
    phan_hd1 = _can("phan_hd1")
    tk = copy.deepcopy(_theo_ky_da_ghi())
    tk[KY_GIA]["chay"] += 1
    h, loi = phan_hd1(tk, _thieu(), dict(VAN_TAY_DT1A), tmp_path / "vang.json", SO_LY_DO)
    assert h is None and len(loi) == 1 and KY_GIA in loi[0] and "dòng thiếu liệt kê" in loi[0], loi
    tk = copy.deepcopy(_theo_ky_da_ghi())
    del tk[KY_GIA]
    h, loi = phan_hd1(tk, _thieu(), dict(VAN_TAY_DT1A), tmp_path / "vang.json", SO_LY_DO)
    assert h is None and len(loi) == 1 and KY_GIA in loi[0] and "ngoài bảng" in loi[0], loi
