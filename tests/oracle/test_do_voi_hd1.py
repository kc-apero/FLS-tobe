# -*- coding: utf-8 -*-
"""H2 — HD1 · cổng nhận *"lệch có tên lý do và owner ký"* (`tools/do_voi_so_luong.py` · khối `dat_hd1`).

ISP 3.1.2 · Step 4 · H2 · `WO-090` · AP v3.1.2 §5.3.1 HD1 ★ *("Lệch = 0, hoặc mỗi lệch có tên lý do và
owner ký")* · §5.3.2 AC10.

⭐ Vì sao có bộ bài này. Trên ảnh đóng băng, **122** dòng sổ AS-IS ⛔ ghép 1-1 được *(DT1a · `WO-080`)*,
   rải ở **18/23** kỳ ⇒ chỉ **5/23** kỳ đủ dòng. AP cho HD1 một lối thứ hai: lệch được CHẤP NHẬN khi
   mỗi lệch có **tên lý do** *(nhãn DT1b)* **và owner KÝ** *(sổ `so_ly_do_hd1.json`, O8 = ThuongCT)*.
   Một lối như thế là **miễn trừ** — và repo này đã cấm *"gõ tên vào danh sách miễn trừ để cổng xanh"*
   (`fls-dev` · ⛔ Cấm). Nên miễn trừ phải là **ràng buộc máy cưỡng chế**: nhãn chưa ký vẫn ĐỎ, chữ ký
   lệch TẬP dòng là ĐỎ, tệp nhãn của một tập dòng KHÁC là ĐỎ, và số kỳ đạt có `MONG` khai trước (Đ5).

Phép phán *(một kỳ)* — ⭐ ĐỔI ở vòng sửa sau R1 *(`KQ-092` · `H2-R1-01` = ⓐ, errata ⑩ của bản vá ISP)*:
   **đạt HD1** ⇔ **[dòng]** *(dòng 1-1 100 %* **hoặc** *mọi dòng thiếu của kỳ có nhãn ĐÃ KÝ)*
   **∧ [ô]** *(mẫu số ô trên MỌI dòng sổ của kỳ > 0* **∧** *(ô `Final = f(Classifying, MID)` khớp trên MỌI
   dòng* **hoặc** *mọi dòng tự-soi loại của kỳ có nhãn ĐÃ KÝ))*. ⛔ gồm chế độ tự sinh — xem `H15`.
   ⛔⛔ Bản R1 tính vế ô trên tập ĐÃ LỌC bỏ 37 dòng tự-soi loại — tức lọc bỏ ĐÚNG thứ vế ấy phải bắt
   *(63 ô `Final ≠ f(Cls, MID)`, cả 63 ở 37 dòng ấy của 2026-07)* ⇒ vế ô ⛔ đỏ được trên đường thật, và
   ký giả 23 dòng thiếu 2026-07 làm kỳ ấy "đạt" dù 63 ô lệch ⛔ tên lý do, ⛔ ai ký.

⛔⛔ Mỗi bài dưới đây canh một cái bẫy CÓ THẬT ở repo này:
  · `H2-B1` — MONG của bài thử **độc lập** với MONG của công cụ: 5 kỳ lấy từ AP v3.1.2 §5.3.1
    *("5/23 tháng đủ")* + BG-081 *(liệt kê đúng 5 kỳ ⛔ có dòng thiếu)*, và đối chiếu **hai nguồn**
    với phần bù của `phan_bo_ky_thieu` trong MONG của DT1a (Đ2). Tập 37 dòng tự-soi loại + ô trên MỌI
    dòng đo LẠI ở bài bằng phép độc lập *(⛔ import công cụ — cách R1 đo ở `KQ-092`)*.
  · `H2-B2` — ký GIẢ *(tệp tạm, ⛔ sổ thật)* đi qua **đường thật** `do()` — một bài chỉ gọi hàm phán
    rời thì chứng minh hàm, ⛔ chứng minh nó được gọi (`DT1a-R1-01`). **Mong MỚI (errata ⑩):** ký 23 dòng
    thiếu 2026-07 ⇒ 2026-07 **vẫn ĐỎ** *(37 dòng tự-soi loại chưa nhãn)*; ký thêm 37 dòng ấy ⇒ đạt, tổng 6.
  · `H2-B3` — nhãn có mà chưa ký vẫn ĐỎ; ký MỘT PHẦN nhãn của kỳ vẫn ĐỎ; chữ ký lệch số dòng / lệch TẬP
    dòng *(đổi chỗ giữa hai nhãn đã ký — K5b, `H2-R1-02`)* ĐỎ; ô lệch ngoài dòng đã ký ⛔ cứu được kỳ.
  · `H2-B4` — cổng phải được CHỨNG MINH ĐỎ, **cả hai chiều** (Đ5): MONG thiếu một kỳ ⇒ ĐỎ; MONG thừa
    một kỳ ⇒ ĐỎ; MONG mất khoá ⇒ ĐỎ một dòng *(⛔ traceback — `S0-R1-04`)*; rồi tệp ⛔ đổi byte nào.
  · `--ghi` — chốt tệp tạm + `os.replace` phải có bài **mô phỏng đúng sự cố nó chống** *(đứt giữa lúc ghi —
    `H2-R1-03`: đột biến M15 "ghi thẳng" sống qua bộ R1 vì mọi bài `--ghi` đều chạy khi cổng ĐỎ)*.
  · Mỗi phép kiểm đầu vào mới là một cổng ⇒ mỗi phép có **ca phá riêng** dẫn từ MỘT đầu vào hợp lệ
    *(đối chứng xanh)* bằng đúng MỘT đột biến (`DT1a-R1-03`); hai vân tay mỗi cái một ca (`DT1a-R1-02`) —
    kể cả phần **regex đứng trước** một hàm thư viện dễ dãi *(`date.fromisoformat` của Python 3.13 nhận cả
    `20261116` lẫn `2026-W47-1` — `H2-R1-04`)*, ký nhãn `KHAC` và ngày sau hôm nay *(`H2-R1-06`)*.
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
from collections import Counter
from datetime import date
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "do_voi_so_luong.py"
TOOL_DT1A = GOC / "tools" / "phan_loai_dong_thieu.py"
RA = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
SO_LY_DO = GOC / "docs" / "ITL" / "_tools" / "so_ly_do_hd1.json"
NHAN = GOC / "docs" / "ITL" / "_tools" / "phan_loai_ly_do.json"
DT1A_JSON = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
ANH_SO = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"

# ── MONG ĐỘC LẬP — ⛔ chép từ tool ─────────────────────────────────────────────────────────────────
# AP v3.1.2 §5.3.1 HD1 ★: "dòng ghép 1-1: 9.845/9.967 (98,8%) — 5/23 tháng đủ"; BG-081 §Bảng đếm:
# "5 kỳ ⛔ có dòng thiếu: 2024-10 · 2024-11 · 2024-12 · 2025-03 · 2025-04". Năm kỳ ấy ⛔ có dòng tự-soi
# loại nào (37/37 dòng loại ở 2026-07 — tests/ledger/test_parity_ca_so.py) ⇒ vế ô mới ⛔ đổi tập (5 = 5).
KY_DAT_SO_RONG = ("2024-10", "2024-11", "2024-12", "2025-03", "2025-04")
SO_KY = 23                     # AP v3.1.2 §5.3.1 · test_pham_vi_hien_vat_dung_nhu_khai
SO_DONG_SO = 9967              # dòng sổ AS-IS (tests/ledger/test_parity_ca_so.py)
SO_DONG_GHEP = 9845            # dòng sổ ghép 1-1 (tests/ledger/test_classifying.py)
THIEU = 122                    # = 9.967 − 9.845 (DT1a · BG-081)
THIEU_2026_07 = 23             # BG-081 §Bảng đếm, hàng 2026-07
VAN_TAY_DT1A = {"thieu": "18047e0eb0319ea1", "nguoc": "6ac2463a190ff631"}   # BG-081 · MONG DT1a
KY_GIA = "2026-07"             # kỳ ISP H2-B2 ký giả — kỳ nhiều dòng thiếu nhất (23/686 dòng sổ)
KY_C = "2025-11"               # kỳ thứ hai của K5b (KQ-092): 14 dòng thiếu, ⛔ dòng tự-soi loại nào
NGUOI_KY_GIA = "TONG_HOP_TEST"  # ⛔ tên người thật: chữ ký TỔNG HỢP chỉ sống trong tệp tạm của bài
# ── vòng sửa sau R1 (`KQ-092`) ──
HOM_NAY = date(2026, 11, 16)   # 'hôm nay' TRUYỀN VÀO công cụ (H2-R1-06) — bài tất định, ⛔ theo đồng hồ máy
NGAY_KY = "2026-11-16"         # = HOM_NAY: ký ĐÚNG hôm nay là HỢP LỆ (biên của luật "ngày ≤ hôm nay")
LOAI_2026_07 = 37              # test_parity_ca_so: 37 dòng bị loại, TẤT CẢ ở 2026-07, dải 8872–9125
LOAI_GIAO_THIEU = 1            # KQ-092: 37 dòng loại ∩ 23 dòng thiếu 2026-07 = 1
O_MOI_DONG = (69706, 69769)    # ô khớp / ô trên MỌI dòng — KQ-092 phép (b) đo độc lập · 63 ô lệch = 60 + 3
#                                (test_parity_ca_so: `(ngoai_mien, trong_mien) == (60, 3)`)
O_MOI_DONG_2026_07 = (4739, 4802)   # KQ-092: ô 2026-07 trên MỌI dòng (63 lệch)
SO_DONG_NGUOC = 147            # DT1a · BG-081: dòng FLS ⛔ có dòng sổ (chiều ngược — ⛔ vào phán HD1)


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


def _da_ghi() -> dict:
    return json.loads(RA.read_text(encoding="utf-8"))


def _theo_ky_da_ghi() -> dict:
    """Bốn số mỗi kỳ của lần đo ĐÃ GHI (`voi_so_luong.json`) — bài B1 ghim tệp ấy bằng lần đo hiện tại."""
    return _da_ghi()["theo_ky"]


def _vao() -> dict:
    """Đầu vào theo kỳ của `phan_hd1` = bốn số (`theo_ky`) + ô trên MỌI dòng (`dat_hd1.theo_ky[k].o_moi_dong*`)
    của lần đo ĐÃ GHI (H2-R1-01 — vế ô đọc MỌI dòng, ⛔ chỉ dòng tự nhất quán)."""
    d = _da_ghi()
    hk = (d.get("dat_hd1") or {}).get("theo_ky", {})
    ra = {}
    for k, x in d["theo_ky"].items():
        assert "o_moi_dong" in hk.get(k, {}), \
            f"⛔ voi_so_luong.json chưa có `dat_hd1.theo_ky[{k}].o_moi_dong` — vế ô trên MỌI dòng (H2-R1-01) chưa có"
        ra[k] = {**x, "o_moi_dong": hk[k]["o_moi_dong"], "o_moi_dong_khop": hk[k]["o_moi_dong_khop"]}
    return ra


def _loai() -> list[tuple[int, str]]:
    """Dòng tự-soi loại `(dong_sheet, kỳ)` — đọc từ lần đo ĐÃ GHI (`dat_hd1.dong_tu_soi_loai`). Bài
    `…tap_dong_tu_soi_loai_HAI_NGUON…` ghim tập ấy bằng phép đo ĐỘC LẬP trên ảnh (Đ2)."""
    h = _da_ghi().get("dat_hd1") or {}
    assert "dong_tu_soi_loai" in h, \
        "⛔ voi_so_luong.json chưa có `dat_hd1.dong_tu_soi_loai` — tập dòng tự-soi loại (H2-R1-01) chưa công bố"
    return [(d, k) for k, ds in sorted(h["dong_tu_soi_loai"].items()) for d in ds]


def _van_tay(ds) -> str:
    """Vân tay một TẬP dòng — viết LẠI ở bài (⛔ import công cụ): sha256 (16 hex) của danh sách ĐÃ SẮP, đúng
    công thức DT1a/BG-081. `test_H2_B1_van_tay_tap_dong_TRUNG_DT1a` chứng minh nó = hiện vật DT1a (Đ2)."""
    return hashlib.sha256(json.dumps(sorted(ds), separators=(",", ":")).encode()).hexdigest()[:16]


def _gan_mac_dinh() -> dict[int, str]:
    """Nhãn TỔNG HỢP: dòng thiếu của kỳ ký giả mang `TONG_HOP_A`, mọi dòng thiếu khác `TONG_HOP_B`
    (dòng tự-soi loại: ⛔ nhãn — trừ 1 dòng vừa thiếu vừa loại, nó mang nhãn dòng thiếu của nó)."""
    return {d: ("TONG_HOP_A" if k == KY_GIA else "TONG_HOP_B") for d, k in _thieu()}


def _gan_ca_loai() -> dict[int, str]:
    """`_gan_mac_dinh` + mọi dòng tự-soi loại CHƯA có nhãn mang `TONG_HOP_L` (36 = 37 − 1 dòng đã là A)."""
    gan = _gan_mac_dinh()
    for d, _k in _loai():
        gan.setdefault(d, "TONG_HOP_L")
    return gan


def _nhan_dict(gan: dict[int, str | None], van_tay: dict | None = None) -> dict:
    """Tệp nhãn theo hợp đồng H2 đọc (khuôn của chính `phan_loai_dong_thieu.json`; danh sách `dong_thieu`
    nay mang được cả dòng tự-soi loại — tập hợp lệ = thiếu ∪ loại)."""
    return {"van_tay": dict(van_tay or VAN_TAY_DT1A),
            "dong_thieu": [{"dong_sheet": d, "nhan": n} for d, n in gan.items()]}


def _chu_ky(nhan: str, gan: dict[int, str | None]) -> dict:
    """Chữ ký TỔNG HỢP đúng TẬP dòng đang mang nhãn ấy — năm khoá (H2-R1-02 thêm `van_tay_dong`)."""
    ds = [d for d, n in gan.items() if n == nhan]
    return {"nhan": nhan, "so_dong": len(ds), "van_tay_dong": _van_tay(ds),
            "nguoi_ky": NGUOI_KY_GIA, "ngay": NGAY_KY}


def _ghi(duong: Path, d) -> Path:
    duong.write_text(d if isinstance(d, str) else json.dumps(d, ensure_ascii=False), encoding="utf-8")
    return duong


def _phan(tmp_path: Path | None = None, *, gan=None, chu_ky=None, theo_ky=None, nhan: Path | None = None,
          so: Path | None = None, thieu=None, loai=None):
    """Gọi `phan_hd1` với đầu vào mặc định = lần đo ĐÃ GHI; `gan`/`chu_ky` ⇒ ghi tệp tạm ở `tmp_path`."""
    phan_hd1 = _can("phan_hd1")
    if gan is not None:
        nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(gan))
    if chu_ky is not None:
        so = _ghi(tmp_path / "so.json", {"chu_ky": chu_ky})
    return phan_hd1(theo_ky if theo_ky is not None else _vao(), thieu if thieu is not None else _thieu(),
                    dict(VAN_TAY_DT1A), nhan, so,
                    loai=loai if loai is not None else _loai(), hom_nay=HOM_NAY)


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


@functools.lru_cache(maxsize=1)
def _do_doc_lap_o() -> dict:
    """Ô `Final = f(Classifying, MID)` trên MỌI dòng sổ, đo ĐỘC LẬP với công cụ — ⛔ import tool, ⛔ gọi
    `tu_soi`/`final_rule`; chỉ dùng hằng `MA_LOI` (danh sách mã lỗi Sheets). Luật viết lại nguyên văn sổ:
    `=if(or(S="Need to manual input", len(S)=0), U, S)` — đúng cách R1 đo phép (b) ở `KQ-092`."""
    from fls.canon.o_loi import MA_LOI

    def loi(v) -> bool:
        if not isinstance(v, str):
            return False
        s = v.strip()
        return any(s == m or s.startswith(m + " ") or s.startswith(m + "(") for m in MA_LOI)

    def chuan(v) -> str:
        if v is None:
            return ""
        if isinstance(v, float) and v.is_integer():
            return str(int(v))
        return str(v).strip()

    g = json.loads(ANH_SO.read_text(encoding="utf-8"))
    cot, bang = {n: i for i, n in enumerate(g["cot"])}, g["bang_gia_tri"]
    o, khop, dong_lech = Counter(), Counter(), {}
    for h in g["dong"]:
        for kh in ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice"):
            cls, mid, fin = ((None if h[cot[f"{kh}_{c}"]] == -1 else bang[h[cot[f"{kh}_{c}"]]])
                             for c in ("classifying", "mid", "final"))
            if loi(cls) or loi(mid) or loi(fin):
                continue
            f = chuan(mid) if chuan(cls) in ("", "Need to manual input") else chuan(cls)
            o[h[1]] += 1
            if f == chuan(fin):
                khop[h[1]] += 1
            else:
                dong_lech.setdefault(h[1], set()).add(h[0])
    return {"o": o, "khop": khop, "dong_lech": dong_lech}


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
    """Sổ rỗng ⇒ kỳ đạt = 5 (= AP v3.1.2). Mẫu số in trong khối, mọi kỳ đỏ mang số dòng thiếu của DT1a.

    ⭐ Viết lại ở vòng sửa sau R1 (`H2-R1-01` ⓐ, errata ⑩) — lo gốc GIỮ (sổ rỗng ⇒ đúng 5 kỳ; mẫu số
    ⛔ rỗng; dòng thiếu mỗi kỳ = DT1a). Đổi đúng một tiền đề: bản R1 đòi `o_100 is True` ở 23/23 kỳ vì vế ô
    tính trên tập ĐÃ LỌC (tautology — R1-M3). Nay `o_100` = vế [ô] trên MỌI dòng ⇒ 2026-07 ĐỎ ô *(63 ô
    lệch ở 37 dòng tự-soi loại chưa nhãn)*, 22 kỳ còn lại đúng; và 5 = 5 (năm kỳ đạt ⛔ có dòng loại nào)."""
    kq = _kq()
    assert "dat_hd1" in kq, "⛔ voi_so_luong chưa có khối `dat_hd1` — trường mới chưa có"
    h = kq["dat_hd1"]
    # Đ3 — mẫu số TRƯỚC: 23 kỳ · 9.967 dòng sổ · 122 dòng thiếu · 37 dòng tự-soi loại · 69.769 ô (⛔ tập rỗng)
    assert {k: h["mau_so"].get(k) for k in ("so_ky", "dong_so", "dong_thieu", "dong_tu_soi_loai", "o_moi_dong")} \
        == {"so_ky": SO_KY, "dong_so": SO_DONG_SO, "dong_thieu": THIEU, "dong_tu_soi_loai": LOAI_2026_07,
            "o_moi_dong": O_MOI_DONG[1]}, h["mau_so"]
    assert h["so_chu_ky"] == 0
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG
    assert h["so_ky_dat"] == len(KY_DAT_SO_RONG) == 5
    assert h["dem"]["da_ky"] == 0 and h["dem"]["loai_da_ky"] == 0
    phan_bo = _dt1a_tool().MONG["phan_bo_ky_thieu"]
    assert sorted(h["theo_ky"]) == sorted(_theo_ky_da_ghi())
    for k, x in h["theo_ky"].items():
        assert x["thieu"] == phan_bo.get(k, 0), (k, x)
        assert x["dat"] is (k in KY_DAT_SO_RONG), (k, x)
        assert x["loai_tu_soi"] == (LOAI_2026_07 if k == KY_GIA else 0), (k, x)
        assert x["o_100"] is (k != KY_GIA), (k, x)                 # vế [ô] trên MỌI dòng — 2026-07 đỏ
    x = h["theo_ky"][KY_GIA]
    assert (x["o_moi_dong_khop"], x["o_moi_dong"]) == O_MOI_DONG_2026_07, x
    # tệp nhãn DT1b: vắng ⇒ 0 dòng có nhãn; có ⇒ đếm của tệp (⛔ đổi số kỳ đạt khi sổ rỗng)
    assert h["tep_nhan"]["co"] is NHAN.exists()
    if not NHAN.exists():
        assert h["dem"]["co_nhan"] == 0 and h["dem"]["loai_co_nhan"] == 0 and h["theo_nhan"] == {}


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
    # H2-R1-01: ô trên MỌI dòng có MONG khai trước (Đ5) — bằng phép đo độc lập của R1 + test_parity_ca_so
    assert tuple(dv.MONG.get("o_moi_dong") or ()) == O_MOI_DONG, "⛔ MONG chưa khai `o_moi_dong`"


def test_H2_B1_van_tay_tap_dong_TRUNG_DT1a():
    """Khoá ghép của tệp nhãn = hai vân tay của DT1a. H2 tính lại từ ảnh — phải BẰNG cả hiện vật DT1a lẫn BG-081;
    và công thức viết lại ở bài (`_van_tay`, dùng cho mọi chữ ký tổng hợp) cho đúng vân tay tập thiếu (Đ2)."""
    h = _kq()["dat_hd1"]
    assert h["van_tay"] == _dt1a()["van_tay"] == VAN_TAY_DT1A
    assert _van_tay(d for d, _ in _thieu()) == VAN_TAY_DT1A["thieu"]


def test_H2_B1_json_DA_GHI_khop_lan_do_hien_tai():
    """`voi_so_luong.json` đã commit = lần đo hiện tại (⛔ sửa tay; quên `--ghi` là ĐỎ)."""
    da_ghi = _da_ghi()
    assert "dat_hd1" in da_ghi, "⛔ voi_so_luong.json chưa có `dat_hd1` — chưa `--ghi`"
    assert da_ghi == _json(_kq())


def test_H2_B1_CLI_in_MAU_SO_truoc_ty_le_va_hang_Sigma_y_nguyen():
    """Đ3: mẫu số in TRƯỚC `5/23`; hàng Σ (K6 của dung_moi_truong_isp.sh đọc) vẫn `9967 9845`.

    ⭐ Siết ở vòng sửa sau R1 (`H2-R1-04`): đột biến R1-M17 / R1-M18 *(bỏ dòng in `②` / `④`)* SỐNG qua bản
    R1 vì bài chỉ đòi `①` + `③` — mà BG-091 dẫn `②` `④` làm bằng chứng. Nay đòi ĐỦ năm dòng `①…⑤`, đúng
    thứ tự, mỗi dòng một lần, kèm số của chúng (`H2-R1-01`: `④` phải cho người ký THẤY 37 dòng loại)."""
    r = _chay_cli()
    assert r.returncode == 0, r.stderr
    assert re.search(r"^Σ\s+9967\s+9845\s", r.stdout, re.M), r.stdout[-600:]
    dong = r.stdout.splitlines()
    vi_tri = {}
    for so in "①②③④⑤":
        i = [j for j, x in enumerate(dong) if x.startswith(f"HD1 · {so} ")]
        assert len(i) == 1, f"⛔ CLI phải in ĐÚNG một dòng `HD1 · {so}` — có {len(i)}: {dong[-8:]}"
        vi_tri[so] = i[0]
    assert list(vi_tri.values()) == sorted(vi_tri.values()), vi_tri
    mau, hai, ba, bon = (dong[vi_tri[s]] for s in "①②③④")
    assert "MẪU SỐ" in mau and "23 kỳ" in mau and f"{THIEU} dòng thiếu" in mau and f"{SO_DONG_SO} dòng sổ" in mau, mau
    assert f"{LOAI_2026_07} dòng tự-soi loại" in mau and f"{O_MOI_DONG[1]} ô" in mau, mau
    assert f"{SO_DONG_NGUOC} dòng FLS" in mau, mau                                   # H2-R1-05 — chiều ngược khai
    assert "kỳ đạt" in ba and "5/23" in ba and " · ".join(KY_DAT_SO_RONG) in ba, ba
    assert re.search(rf"dòng thiếu có nhãn \d+/{THIEU} · có nhãn ĐÃ KÝ \d+/{THIEU}", hai), hai
    assert re.search(rf"dòng tự-soi loại có nhãn \d+/{LOAI_2026_07} · có nhãn ĐÃ KÝ \d+/{LOAI_2026_07}", hai), hai
    assert "kỳ đỏ 18/23" in bon, bon
    if not NHAN.exists():
        assert f"có nhãn 0/{THIEU} · có nhãn ĐÃ KÝ 0/{THIEU}" in hai, hai
        assert f"{KY_GIA} {THIEU_2026_07}·0·0 loại {LOAI_2026_07}·0·0 ô {O_MOI_DONG_2026_07[0]}/{O_MOI_DONG_2026_07[1]}" \
            in bon, bon
        assert "2026-08 13·0·0" in bon, bon


def test_H2_B1_tep_DT1a_dung_lam_tep_nhan_hop_le_0_nhan():
    """Hợp đồng tệp nhãn = khuôn của chính `phan_loai_dong_thieu.json` (`van_tay` + `dong_thieu[].nhan`).
    Hiện vật DT1a (mọi `nhan = null`) phải là một tệp nhãn HỢP LỆ, 0 nhãn ⇒ 5 kỳ — DT1b ghi đúng khuôn ấy
    thì H2 đọc được ngay."""
    h, loi = _phan(nhan=DT1A_JSON, so=SO_LY_DO)
    assert loi == [], loi
    assert h["tep_nhan"]["co"] is True and h["dem"]["co_nhan"] == 0
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG


def test_H2_B1_tap_dong_tu_soi_loai_HAI_NGUON_va_o_moi_dong_khop_MONG():
    """Đ2 — tập dòng tự-soi loại công cụ CÔNG BỐ (`dat_hd1.dong_tu_soi_loai`) = tập dòng có ô `Final ≠ f(Cls,
    MID)` đo ĐỘC LẬP trên ảnh; ô trên MỌI dòng theo kỳ = phép đo độc lập; Σ = MONG độc lập (KQ-092 (b)).
    ⛔ Vế ô mà tính trên tập đã lọc bỏ đúng 37 dòng này là tautology (`H2-R1-01`)."""
    dl = _do_doc_lap_o()
    loai = _loai()
    assert len(loai) == LOAI_2026_07 and {k for _, k in loai} == {KY_GIA}, loai          # Đ3 — ⛔ tập rỗng
    assert {d for d, _ in loai} == dl["dong_lech"].get(KY_GIA) and set(dl["dong_lech"]) == {KY_GIA}
    assert (min(d for d, _ in loai), max(d for d, _ in loai)) == (8872, 9125)       # test_parity_ca_so
    assert len({d for d, _ in loai} & {d for d, _ in _thieu()}) == LOAI_GIAO_THIEU
    assert (sum(dl["khop"].values()), sum(dl["o"].values())) == O_MOI_DONG
    hk = _kq()["dat_hd1"]["theo_ky"]
    assert {k: (x["o_moi_dong_khop"], x["o_moi_dong"]) for k, x in hk.items()} == \
        {k: (dl["khop"][k], dl["o"][k]) for k in dl["o"]}


def test_H2_B1_luat_KHAI_chieu_nguoc_ngoai_phan_va_dong_VANG_la_chua_co_nhan():
    """`H2-R1-05` · `-07` (Đ4 — một phán "đạt" phải tự khai tập nào nó ⛔ xét): 147 dòng FLS ⛔ có dòng sổ
    ⛔ vào phán HD1 ở bước này (ảnh `pm_join` ⛔ có ngày ⇒ ⛔ gán được kỳ) — số ấy CÓ trong khối, bằng DT1a;
    và "dòng vắng trong tệp nhãn = chưa có nhãn" nằm trong `_luat`."""
    h = _kq()["dat_hd1"]
    assert h["ngoai_phan"]["dong_fls_khong_co_dong_so"] == SO_DONG_NGUOC == len(_dt1a()["dong_nguoc"])
    luat = h["_luat"]
    for cum in ("chiều ngược", "ngoai_phan", "VẮNG", "chưa có nhãn", "tự-soi loại", "MỌI dòng", "KHAC",
                "van_tay_dong", "hôm nay", "o_100"):
        assert cum in luat, (cum, luat)


def test_H2_B1_tep_nhan_THIEU_dong_la_HOP_LE_dong_vang_la_CHUA_co_nhan(tmp_path):
    """`H2-R1-07` (K4e) — hợp đồng đã KHAI: tệp nhãn liệt kê MỘT PHẦN tập (23/122 dòng) vẫn hợp lệ; 99 dòng
    vắng = "chưa có nhãn" ⇒ kỳ của chúng đỏ (chiều an toàn). Bài ghim hành vi ấy cho tới khi DT1b về và
    orchestrator chọn "đòi đủ 122" (khi ấy bài này phải ĐỎ — đổi hợp đồng có chủ đích)."""
    gan = {d: "TONG_HOP_A" for d, k in _thieu() if k == KY_GIA}
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[])
    assert loi == [], loi
    assert h["dem"]["co_nhan"] == THIEU_2026_07 and tuple(h["ky_dat"]) == KY_DAT_SO_RONG


# ═════════════════════════════════════════════════════════════════════════ H2-B2 · ký giả 2026-07
def test_H2_B2_ky_gia_23_dong_thieu_2026_07_thi_2026_07_VAN_DO_vi_dong_tu_soi_loai(tmp_path):
    """Mong MỚI (errata ⑩, `H2-R1-01` ⓐ): ký giả nhãn của MỌI dòng thiếu 2026-07 (23 dòng) ⇒ vế [dòng] đạt
    nhưng 2026-07 VẪN ĐỎ — 37 dòng tự-soi loại mang 63 ô lệch, chỉ 1 dòng có nhãn (dòng vừa thiếu vừa loại);
    tổng vẫn 5. Bản R1 ra "đạt, tổng 6" (K1′ của KQ-092)."""
    gan = _gan_mac_dinh()
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[_chu_ky("TONG_HOP_A", gan)])
    assert loi == [], loi
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG and h["so_ky_dat"] == 5
    x = h["theo_ky"][KY_GIA]
    assert (x["thieu"], x["co_nhan"], x["da_ky"], x["dong_100"]) == \
        (THIEU_2026_07, THIEU_2026_07, THIEU_2026_07, False), x
    assert (x["loai_tu_soi"], x["loai_co_nhan"], x["loai_da_ky"]) == \
        (LOAI_2026_07, LOAI_GIAO_THIEU, LOAI_GIAO_THIEU), x
    assert (x["o_moi_dong_khop"], x["o_moi_dong"]) == O_MOI_DONG_2026_07, x
    assert (x["o_100"], x["dat"]) == (False, False), x


def test_H2_B2_ky_them_37_dong_tu_soi_loai_thi_2026_07_DAT_tong_6(tmp_path):
    """Ký thêm nhãn cho 37 dòng tự-soi loại (36 dòng `TONG_HOP_L` + 1 dòng đã là A) ⇒ 2026-07 đạt; tổng 6
    = 5 + 1; chữ ký của 2026-07 ⛔ lan sang kỳ khác."""
    gan = _gan_ca_loai()
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[_chu_ky("TONG_HOP_A", gan), _chu_ky("TONG_HOP_L", gan)])
    assert loi == [], loi
    assert tuple(h["ky_dat"]) == tuple(sorted(KY_DAT_SO_RONG + (KY_GIA,))) and h["so_ky_dat"] == 6
    x = h["theo_ky"][KY_GIA]
    assert (x["da_ky"], x["loai_tu_soi"], x["loai_da_ky"], x["o_100"], x["dat"]) == \
        (THIEU_2026_07, LOAI_2026_07, LOAI_2026_07, True, True), x
    assert {k: h["dem"][k] for k in ("thieu", "co_nhan", "da_ky", "loai_tu_soi", "loai_co_nhan", "loai_da_ky")} == \
        {"thieu": THIEU, "co_nhan": THIEU, "da_ky": THIEU_2026_07, "loai_tu_soi": LOAI_2026_07,
         "loai_co_nhan": LOAI_2026_07, "loai_da_ky": LOAI_2026_07}, h["dem"]
    for k, y in h["theo_ky"].items():
        if k != KY_GIA:
            assert y["dat"] is (k in KY_DAT_SO_RONG), (k, y)


def test_H2_B2_qua_DUONG_THAT_ky_23_dong_van_5_ky_ky_them_37_dong_thi_DO_vi_khac_MONG_5(tmp_path):
    """Đường thật `do()` — hai bước của errata ⑩: ① chỉ ký 23 dòng thiếu ⇒ `do()` XANH (5 = MONG) và 2026-07
    đỏ VÌ VẾ Ô (vế ô nay ĐỎ được trên đường thật — R1-M3 *(bỏ `and o_100`)* chết ở đây, ⛔ chỉ trên `theo_ky`
    tổng hợp); ② ký thêm 37 dòng loại ⇒ cổng ĐỎ vì đo 6 ≠ MONG 5 — Đ5 làm việc: chữ ký thật BUỘC khai lại
    MONG; và `do()` ĐỌC cả tệp nhãn lẫn sổ lý do được truyền vào."""
    _can("phan_hd1")
    gan = _gan_mac_dinh()
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(gan))
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", gan)]})
    h = _dv().do(nhan=nhan, so_ly_do=so, hom_nay=HOM_NAY)["dat_hd1"]          # ⛔ SystemExit: 5 = MONG
    x = h["theo_ky"][KY_GIA]
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG and h["so_chu_ky"] == 1
    assert (x["da_ky"], x["o_100"], x["dat"]) == (THIEU_2026_07, False, False), x
    gan = _gan_ca_loai()
    nhan = _ghi(tmp_path / "nhan2.json", _nhan_dict(gan))
    so = _ghi(tmp_path / "so2.json", {"chu_ky": [_chu_ky("TONG_HOP_A", gan), _chu_ky("TONG_HOP_L", gan)]})
    do_, mong = _dong_mong_hd1(_do_do(nhan=nhan, so_ly_do=so, hom_nay=HOM_NAY))
    assert do_ == sorted(KY_DAT_SO_RONG + (KY_GIA,)) and len(do_) == 6, do_
    assert mong == list(KY_DAT_SO_RONG), mong


# ═════════════════════════════════════════════════════════════════════════ H2-B3 · nhãn chưa ký vẫn đỏ
def test_H2_B3_co_nhan_ma_CHUA_KY_van_do_qua_duong_that(tmp_path):
    """Mọi 122 dòng thiếu + 37 dòng loại có nhãn, sổ RỖNG (sổ thật) ⇒ ⛔ kỳ nào thêm: vẫn 5; 2026-07 đỏ dù
    23/23 dòng thiếu + 37/37 dòng loại có nhãn."""
    _can("phan_hd1")
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(_gan_ca_loai()))
    kq = _dv().do(nhan=nhan, so_ly_do=SO_LY_DO, hom_nay=HOM_NAY)    # ⛔ SystemExit: 5 = MONG
    h = kq["dat_hd1"]
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG
    assert {k: h["dem"][k] for k in ("thieu", "co_nhan", "da_ky", "loai_co_nhan", "loai_da_ky")} == \
        {"thieu": THIEU, "co_nhan": THIEU, "da_ky": 0, "loai_co_nhan": LOAI_2026_07, "loai_da_ky": 0}, h["dem"]
    x = h["theo_ky"][KY_GIA]
    assert (x["co_nhan"], x["da_ky"], x["loai_co_nhan"], x["loai_da_ky"], x["dat"]) == \
        (THIEU_2026_07, 0, LOAI_2026_07, 0, False), x


def test_H2_B3_ky_MOT_PHAN_nhan_cua_ky_thi_ky_VAN_do(tmp_path):
    """2026-07 mang hai nhãn dòng thiếu (22 + 1), chỉ ký một ⇒ 22/23 dòng đã ký ⇒ kỳ VẪN đỏ ('mọi dòng') —
    kể cả khi 37 dòng loại đã ký (vế ô đạt, vế dòng thì ⛔)."""
    gan = _gan_ca_loai()
    dong_ky = sorted(d for d, k in _thieu() if k == KY_GIA and d not in {x for x, _ in _loai()})
    assert len(dong_ky) == THIEU_2026_07 - LOAI_GIAO_THIEU                    # Đ3 — tập ⛔ rỗng, đúng 22
    gan[dong_ky[-1]] = "TONG_HOP_C"
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[_chu_ky("TONG_HOP_A", gan), _chu_ky("TONG_HOP_L", gan)])
    assert loi == [], loi
    x = h["theo_ky"][KY_GIA]
    assert (x["co_nhan"], x["da_ky"], x["o_100"], x["dat"]) == (THIEU_2026_07, THIEU_2026_07 - 1, True, False), x
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG


def test_H2_B3_ky_dong_tu_soi_loai_ma_CHUA_ky_dong_thieu_VAN_do(tmp_path):
    """Hai vế độc lập: ký đủ 37 dòng loại (vế ô đạt) mà ⛔ ký 23 dòng thiếu ⇒ 2026-07 VẪN đỏ (vế dòng)."""
    gan = _gan_ca_loai()
    gan = {d: ("TONG_HOP_L" if n == "TONG_HOP_A" and d in {x for x, _ in _loai()} else n) for d, n in gan.items()}
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[_chu_ky("TONG_HOP_L", gan)])
    assert loi == [], loi
    x = h["theo_ky"][KY_GIA]
    assert (x["loai_da_ky"], x["o_100"], x["da_ky"], x["dat"]) == \
        (LOAI_2026_07, True, LOAI_GIAO_THIEU, False), x
    assert tuple(h["ky_dat"]) == KY_DAT_SO_RONG


def test_H2_B3_chu_ky_LECH_so_dong_la_DO_qua_duong_that(tmp_path):
    """Owner ký 'TONG_HOP_A · 22 dòng' mà tệp nhãn có 23 dòng mang nhãn ấy ⇒ chữ ký CŨ ⇒ ĐỎ, ⛔ lặng lẽ
    phủ thêm dòng thứ 23 mà owner chưa thấy."""
    _can("phan_hd1")
    gan = _gan_mac_dinh()
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(gan))
    ck = _chu_ky("TONG_HOP_A", gan)
    ck["so_dong"] -= 1
    so = _ghi(tmp_path / "so.json", {"chu_ky": [ck]})
    tb = _do_do(nhan=nhan, so_ly_do=so, hom_nay=HOM_NAY)
    assert "số dòng" in tb and "TONG_HOP_A" in tb and "chữ ký cũ" in tb, tb


def test_H2_B3_chu_ky_khi_tep_nhan_VANG_la_DO_qua_duong_that(tmp_path):
    """Sổ có chữ ký mà tệp nhãn vắng ⇒ chữ ký trỏ 0 dòng ⇒ ĐỎ (⛔ đo được, ⛔ 'không thấy lệch')."""
    _can("phan_hd1")
    so = _ghi(tmp_path / "so.json", {"chu_ky": [_chu_ky("TONG_HOP_A", {_thieu()[0][0]: "TONG_HOP_A"})]})
    tb = _do_do(nhan=tmp_path / "vang.json", so_ly_do=so, hom_nay=HOM_NAY)
    assert "số dòng" in tb and "TONG_HOP_A" in tb, tb


def test_H2_B3_o_chua_100_thi_chu_ky_KHONG_cuu_duoc_ky(tmp_path):
    """Vế [ô] chỉ miễn trừ được ô của dòng TỰ-SOI LOẠI có nhãn ĐÃ KÝ — ⛔ ô nào khác: 2026-07 đã ký đủ (23
    dòng thiếu + 37 dòng loại) mà MỘT ô của dòng tự nhất quán lệch ⇒ đỏ; kỳ đủ dòng (2024-10) mà một ô lệch
    ⇒ đỏ; mẫu số ô = 0 ⇒ đỏ (Đ3 — ⛔ '0/0 = 100 %').

    ⭐ Viết lại ở vòng sửa sau R1 (`H2-R1-01` ⓐ) — lo gốc GIỮ ("ô chưa 100 % thì chữ ký ⛔ cứu được kỳ").
    Đổi tiền đề: vế ô nay đọc `o_moi_dong*` (MỌI dòng) + `o_parity*` (dòng tự nhất quán); ca 2026-07 nay
    ký CẢ 37 dòng loại — nếu ⛔ thì kỳ đỏ sẵn vì dòng loại, bài ⛔ còn chứng minh gì."""
    gan = _gan_ca_loai()
    tk = copy.deepcopy(_vao())
    for k in (KY_GIA, "2024-10"):
        tk[k]["o_parity_khop"] -= 1
        tk[k]["o_moi_dong_khop"] -= 1
    for khoa in ("o_parity", "o_parity_khop", "o_moi_dong", "o_moi_dong_khop"):
        tk["2024-11"][khoa] = 0
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[_chu_ky("TONG_HOP_A", gan), _chu_ky("TONG_HOP_L", gan)], theo_ky=tk)
    assert loi == [], loi
    assert h["theo_ky"][KY_GIA]["loai_da_ky"] == LOAI_2026_07                  # dòng loại ĐÃ ký đủ
    for k in (KY_GIA, "2024-10", "2024-11"):
        assert (h["theo_ky"][k]["o_100"], h["theo_ky"][k]["dat"]) == (False, False), (k, h["theo_ky"][k])
    assert tuple(h["ky_dat"]) == ("2024-12", "2025-03", "2025-04")


def test_H2_B3_o_khop_tren_MOI_dong_thi_dong_loai_KHONG_can_ky(tmp_path):
    """Vế [ô] = "khớp trên MỌI dòng **hoặc** mọi dòng loại đã ký" — vế trái đứng một mình: nếu ô của MỌI dòng
    khớp (đầu vào tổng hợp: 63 ô lệch của 2026-07 coi như đã sửa) thì 37 dòng loại ⛔ cần chữ ký; ký 23 dòng
    thiếu là đủ ⇒ 2026-07 đạt. Canh đúng chữ errata ⑩, ⛔ để vế "đã ký" nuốt vế "khớp"."""
    gan = _gan_mac_dinh()
    tk = copy.deepcopy(_vao())
    tk[KY_GIA]["o_moi_dong_khop"] = tk[KY_GIA]["o_moi_dong"]
    h, loi = _phan(tmp_path, gan=gan, chu_ky=[_chu_ky("TONG_HOP_A", gan)], theo_ky=tk)
    assert loi == [], loi
    x = h["theo_ky"][KY_GIA]
    assert (x["loai_da_ky"], x["o_100"], x["dat"]) == (LOAI_GIAO_THIEU, True, True), x


def test_H2_B3_doi_cho_MOT_dong_giua_HAI_nhan_DA_KY_la_DO_qua_duong_that(tmp_path):
    """K5b (`KQ-092` · `H2-R1-02` ⓑ, errata ⑬): hai nhãn ĐÃ KÝ — `A · 23` (dòng thiếu 2026-07) và `C · 14`
    (dòng thiếu 2025-11); đổi chỗ nhãn của MỘT dòng mỗi bên ⇒ số dòng mỗi nhãn Y NGUYÊN (23 · 14) mà tập
    đã khác — bản R1 exit 0, `ky_dat` 7 = 7, dòng đổi lý do vô hình (bẫy Đ4). Nay mỗi chữ ký mang
    `van_tay_dong` ⇒ ĐỎ "chữ ký cũ, ký lại" ở CẢ HAI chữ ký, ⛔ phán kỳ nào."""
    gan = _gan_mac_dinh()
    for d, k in _thieu():
        if k == KY_C:
            gan[d] = "TONG_HOP_C"
    so = {"chu_ky": [_chu_ky("TONG_HOP_A", gan), _chu_ky("TONG_HOP_C", gan)]}
    assert (so["chu_ky"][0]["so_dong"], so["chu_ky"][1]["so_dong"]) == (THIEU_2026_07, 14)   # Đ3 — ⛔ rỗng
    h, loi = _phan(tmp_path, gan=gan, chu_ky=so["chu_ky"])                                   # đối chứng
    assert loi == [] and KY_C in h["ky_dat"], loi
    a = min(d for d, k in _thieu() if k == KY_GIA)
    c = min(d for d, k in _thieu() if k == KY_C)
    dem_truoc = Counter(gan.values())
    gan[a], gan[c] = "TONG_HOP_C", "TONG_HOP_A"
    assert Counter(gan.values()) == dem_truoc                                  # tổng mỗi nhãn y nguyên
    nhan = _ghi(tmp_path / "nhan_doi_cho.json", _nhan_dict(gan))
    tb = _do_do(nhan=nhan, so_ly_do=_ghi(tmp_path / "so_cu.json", so), hom_nay=HOM_NAY)
    dong = [x for x in tb.splitlines() if "chữ ký cũ" in x]
    assert len(dong) == 2 and all("vân tay dòng" in x for x in dong), tb
    assert {n for n in ("TONG_HOP_A", "TONG_HOP_C") if any(n in x for x in dong)} == {"TONG_HOP_A", "TONG_HOP_C"}
    assert "dat_hd1_theo_ky" not in tb, tb                                     # ⛔ phán trên đầu vào hỏng


def test_H2_B3_theo_nhan_IN_SAN_van_tay_cho_owner_chep_va_chu_ky_chep_dung_thi_NHAN(tmp_path):
    """`H2-R1-02` ⓑ: công cụ IN SẴN `so_dong` + `van_tay_dong` mỗi nhãn (`dat_hd1.theo_nhan` · CLI `⑤`) để owner
    CHÉP vào chữ ký — ⛔ tự tính tay. Vòng tròn: đo khi sổ rỗng → chép đúng hai số ấy → chữ ký được NHẬN và
    phủ đúng 23 dòng. Vân tay công cụ in = công thức viết lại ở bài (Đ2)."""
    gan = _gan_mac_dinh()
    nhan = _ghi(tmp_path / "nhan.json", _nhan_dict(gan))
    h, loi = _phan(nhan=nhan, so=_ghi(tmp_path / "so_rong.json", {"chu_ky": []}))
    assert loi == [], loi
    tn = h["theo_nhan"]
    assert sorted(tn) == ["TONG_HOP_A", "TONG_HOP_B"], tn
    a = tn["TONG_HOP_A"]
    assert (a["so_dong"], a["van_tay_dong"], a["da_ky"]) == \
        (THIEU_2026_07, _van_tay(d for d, n in gan.items() if n == "TONG_HOP_A"), False), a
    ck = {"nhan": "TONG_HOP_A", "so_dong": a["so_dong"], "van_tay_dong": a["van_tay_dong"],
          "nguoi_ky": NGUOI_KY_GIA, "ngay": NGAY_KY}
    h, loi = _phan(nhan=nhan, so=_ghi(tmp_path / "so.json", {"chu_ky": [ck]}))
    assert loi == [], loi
    assert h["theo_nhan"]["TONG_HOP_A"]["da_ky"] is True and h["theo_ky"][KY_GIA]["da_ky"] == THIEU_2026_07


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


def test_H2_B4_pha_MONG_o_moi_dong_la_DO_mot_dong():
    """MONG mới của vòng sửa (`o_moi_dong`) cũng phải CHỨNG MINH ĐỎ (Đ5): lệch một ô ⇒ exit 1, đúng một dòng
    nguyên nhân mang tên phép, ⛔ traceback; mất khoá ⇒ exit 1 (⛔ KeyError)."""
    _can("phan_hd1")
    for ma in ("t.MONG['o_moi_dong'] = (%d, %d)" % (O_MOI_DONG[0] + 1, O_MOI_DONG[1]),
               "del t.MONG['o_moi_dong']"):
        r = _chay_pha(ma)
        assert r.returncode == 1, (ma, r.returncode, r.stderr[-800:])
        assert len([x for x in r.stderr.splitlines() if "MỌI dòng" in x]) == 1, (ma, r.stderr[-800:])
        assert "Traceback" not in r.stderr, (ma, r.stderr[-800:])


# ═════════════════════════════════════════════════════════════════════════ `--ghi` XANH (H2-R1-03)
def test_H2_ghi_XANH_dut_giua_chung_KHONG_lam_cut_hien_vat(tmp_path, monkeypatch, capsys):
    """M15 (`H2-R1-03`): `--ghi` khi cổng XANH mà ĐỨT giữa lúc ghi ⇒ hiện vật đích ⛔ đổi byte nào và ⛔ sót
    tệp `.tam` (đứt giữa chừng ⛔ được để rác hiện ở `git status`). Bài R1 đề xuất (`KQ-092`), ⛔ đổi lo."""
    dv = _dv()
    ra = tmp_path / "voi_so_luong.json"
    ra.write_bytes(RA.read_bytes())
    goc = ra.read_bytes()
    monkeypatch.setattr(dv, "RA", ra)
    that = Path.write_text

    def dut(self, s, *a, **k):
        that(self, s[: len(s) // 2], *a, **k)
        raise OSError("bài thử: đứt giữa chừng")

    monkeypatch.setattr(Path, "write_text", dut)
    monkeypatch.setattr(sys, "argv", ["do_voi_so_luong.py", "--ghi"])
    with pytest.raises(OSError, match="đứt giữa chừng"):
        dv.main()
    monkeypatch.setattr(Path, "write_text", that)
    assert ra.read_bytes() == goc, "⛔ hiện vật bị ghi CỤT — `--ghi` ghi thẳng lên đích"
    assert sorted(p.name for p in tmp_path.iterdir()) == ["voi_so_luong.json"], list(tmp_path.iterdir())


def test_H2_ghi_XANH_ra_DUNG_byte_tep_da_commit(tmp_path, monkeypatch, capsys):
    """`--ghi` XANH trên đích tạm ⇒ byte = `voi_so_luong.json` đã commit, ⛔ sót `.tam`, in `đã ghi`."""
    dv = _dv()
    ra = tmp_path / "voi_so_luong.json"
    monkeypatch.setattr(dv, "RA", ra)
    monkeypatch.setattr(sys, "argv", ["do_voi_so_luong.py", "--ghi"])
    dv.main()
    assert "đã ghi" in capsys.readouterr().out
    assert ra.read_bytes() == RA.read_bytes()
    assert sorted(p.name for p in tmp_path.iterdir()) == ["voi_so_luong.json"]


# ═════════════════════════════════════════════════════════════════════════ kiểm đầu vào — mỗi luật một ca
def _dau_vao_hop_le() -> tuple[dict, dict]:
    """Đầu vào HỢP LỆ dùng chung: 122 dòng thiếu + 37 dòng loại có nhãn, hai chữ ký đúng tập (A · L) ⇒ 6 kỳ.
    Mỗi ca phá đổi đúng MỘT chỗ — phần lớn ở chữ ký ĐẦU (`TONG_HOP_A`)."""
    gan = _gan_ca_loai()
    return _nhan_dict(gan), {"chu_ky": [_chu_ky("TONG_HOP_A", gan), _chu_ky("TONG_HOP_L", gan)]}


def _ngoai_tap() -> int:
    tap = {d for d, _ in _thieu()} | {d for d, _ in _loai()}
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


def _dat_nhan_ca_hai(n: dict, s: dict, nhan_moi: str):
    """Đổi tên nhãn A ở CẢ tệp nhãn lẫn chữ ký (số dòng + vân tay y nguyên) — đúng một đột biến: TÊN nhãn ký."""
    for x in n["dong_thieu"]:
        if x["nhan"] == "TONG_HOP_A":
            x["nhan"] = nhan_moi
    s["chu_ky"][0]["nhan"] = nhan_moi
    return n, s


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
    "so_nhan_khong_ai_gan": (_pha_so(lambda s: s["chu_ky"].append(
        {"nhan": "KHONG_AI_GAN", "so_dong": 1, "van_tay_dong": _van_tay([1]), "nguoi_ky": NGUOI_KY_GIA,
         "ngay": NGAY_KY})), "số dòng"),
    # ── vòng sửa sau R1 (KQ-092) ──
    # H2-R1-02 — khoá thứ năm `van_tay_dong`: thiếu khoá · sai khuôn · đúng khuôn mà lệch tập (K5b một chữ ký)
    "so_thieu_van_tay_dong": (_pha_so(lambda s: s["chu_ky"][0].pop("van_tay_dong")), "khoá"),
    "so_van_tay_dong_sai_khuon": (_pha_so(lambda s: _dat(s["chu_ky"][0], "van_tay_dong", "XYZ")), "van_tay_dong"),
    "so_van_tay_dong_lech_tap": (_pha_so(lambda s: _dat(s["chu_ky"][0], "van_tay_dong", "0" * 16)), "vân tay dòng"),
    # H2-R1-06 — ⛔ ký `KHAC` (HD1 = lệch CÓ TÊN lý do); tên nhãn đổi ở CẢ tệp nhãn lẫn chữ ký (⛔ lệch số dòng)
    "so_nhan_KHAC": (lambda n, s: _dat_nhan_ca_hai(n, s, "KHAC"), "KHAC"),
    "so_nhan_Khac_co_dau": (lambda n, s: _dat_nhan_ca_hai(n, s, " Khác "), "KHAC"),
    # H2-R1-06 — ngày ký sau hôm nay (hôm nay TRUYỀN VÀO: HOM_NAY)
    "so_ngay_tuong_lai": (_pha_so(lambda s: _dat(s["chu_ky"][0], "ngay", "2026-11-17")), "sau hôm nay"),
    # H2-R1-04 — regex đứng trước `date.fromisoformat` (Python 3.13 nhận cả hai khuôn này) — R1-M19
    "so_ngay_khuon_co_ban": (_pha_so(lambda s: _dat(s["chu_ky"][0], "ngay", "20261116")), "ngày"),
    "so_ngay_khuon_tuan": (_pha_so(lambda s: _dat(s["chu_ky"][0], "ngay", "2026-W47-1")), "ngày"),
}


def test_H2_kiem_dau_vao_DOI_CHUNG_hop_le_0_loi(tmp_path):
    """Đối chứng: đầu vào gốc của mọi ca phá là HỢP LỆ — mỗi ĐỎ dưới đây do đúng một đột biến. Ký ĐÚNG hôm nay
    (biên) là hợp lệ; tên nhãn có dấu khác `KHAC` (đối chứng của ca `Khác`) cũng hợp lệ."""
    n, s = _dau_vao_hop_le()
    h, loi = _phan(nhan=_ghi(tmp_path / "n.json", n), so=_ghi(tmp_path / "s.json", s))
    assert loi == [] and h is not None and h["so_ky_dat"] == 6, loi
    assert s["chu_ky"][0]["ngay"] == HOM_NAY.isoformat()
    n, s = _dat_nhan_ca_hai(*_dau_vao_hop_le(), "Lý do có tên")
    h, loi = _phan(nhan=_ghi(tmp_path / "n2.json", n), so=_ghi(tmp_path / "s2.json", s))
    assert loi == [] and h["so_ky_dat"] == 6, loi


@pytest.mark.parametrize("ten", sorted(CA_PHA))
def test_H2_kiem_dau_vao_moi_luat_CAN(ten, tmp_path):
    """Mỗi phép kiểm đầu vào là một cổng ⇒ có ca phá riêng (`DT1a-R1-03`). Đầu vào lỗi ⇒ ⛔ phán kỳ nào
    (khối = None) — ⛔ đo được là ĐỎ (Đ5), ⛔ rơi về 'chưa có nhãn' cho êm."""
    pha, mau = CA_PHA[ten]
    n, s = pha(*_dau_vao_hop_le())
    h, loi = _phan(nhan=_ghi(tmp_path / "n.json", n), so=_ghi(tmp_path / "s.json", s))
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
    """Phòng thủ chồng (Đ2 — hai nguồn): `có − chạy` của kỳ ↔ số dòng thiếu liệt kê; `loai_tu_soi` của kỳ ↔ số
    dòng tự-soi loại liệt kê (vòng sửa R1); và dòng thiếu/loại ⛔ được thuộc kỳ ngoài bảng bốn số. Mỗi phép
    một ca phá (`DT1a-R1-03`), đúng MỘT lỗi."""
    vang = tmp_path / "vang.json"
    tk = copy.deepcopy(_vao())
    tk[KY_GIA]["chay"] += 1
    h, loi = _phan(theo_ky=tk, nhan=vang, so=SO_LY_DO)
    assert h is None and len(loi) == 1 and KY_GIA in loi[0] and "dòng thiếu liệt kê" in loi[0], loi
    tk = copy.deepcopy(_vao())
    tk[KY_GIA]["loai_tu_soi"] += 1
    h, loi = _phan(theo_ky=tk, nhan=vang, so=SO_LY_DO)
    assert h is None and len(loi) == 1 and KY_GIA in loi[0] and "tự-soi loại liệt kê" in loi[0], loi
    tk = copy.deepcopy(_vao())
    del tk[KY_GIA]
    h, loi = _phan(theo_ky=tk, nhan=vang, so=SO_LY_DO)
    assert h is None and len(loi) == 1 and KY_GIA in loi[0] and "ngoài bảng" in loi[0], loi
    h, loi = _phan(nhan=vang, so=SO_LY_DO, thieu=[x for x in _thieu() if x[1] != KY_GIA])
    assert h is None and len(loi) == 1 and KY_GIA in loi[0] and "dòng thiếu liệt kê" in loi[0], loi
