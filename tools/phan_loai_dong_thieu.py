# -*- coding: utf-8 -*-
"""PHÂN LOẠI DÒNG THIẾU — HD1 · kiểm kê dòng sổ AS-IS chưa ghép 1-1, trên ẢNH ĐÓNG BĂNG.

ISP 3.1.2 · Step 3 · DT1a · `WO-080` · AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10 · §2.5.3.

⭐ Vì sao có tệp này. HD1 = *"mapping được 100 %, giống các dữ liệu quá khứ"* (owner 16/11). Trên ảnh
   đóng băng, mã FLS ghép 1-1 được **9.845** trong **9.967** dòng sổ `ITL Ledge` (98,78 %) — phần còn lại
   **122** dòng sổ ⛔ có cặp, và chiều ngược **147** dòng FLS ⛔ có dòng sổ. Trước bước này các TỔNG đã có
   máy canh gián tiếp — `tools/do_voi_so_luong.py:118` · `:129` · `:138` ghim 9.967 · 9.845 · 9.992 — nhưng
   DANH TÍNH tập chỉ sống trong một phép đo TAY của orchestrator (16/11): ⛔ máy nào đỏ khi tập ĐỔI mà
   tổng giữ nguyên, ⛔ ai liệt kê được ĐÚNG 122 dòng nào để DT1b gán lý do. Tệp này liệt kê, ghim, và
   ĐỎ khi khác. *(Đính chính `DT1a-R1-05`ⓒ · `KQ-082`: bản đầu viết "⛔ máy nào đỏ khi chúng đổi" —
   sai `Đ1`, chưa grep `tools/`.)*

Hai tập — mỗi tập nói NÓ ĐẾM GÌ (Đ4), đơn vị là DÒNG:
  THIẾU = `dong_sheet` của sổ (`itl_ledge_adjustment.json`, 9.967 dòng, 23 kỳ)
          ∖ `dong_so` đã ghép (`classifying_vs_canon.json`, 9.845 dòng).
          Mỗi dòng mang thuộc tính ĐO ĐƯỢC trên ảnh: kỳ · hd / pay_type / cdt1 × Classifying / MID / Final,
          và `nhan = null` — LÝ DO là việc của DT1b (cần khoá đọc ở nguồn: ảnh đã bỏ Số CT · TK · tiền).
  NGƯỢC = dòng FLS dựng lại (`pm_join.json` · bank, 9.992 dòng = `so_dong_canon` của ảnh ghép)
          ∖ `dong_canon` đã ghép. ISP: *"chỉ ĐẾM"* — ⛔ ảnh nào mang thuộc tính của dòng canon ⛔ ghép,
          nên mỗi dòng chỉ có số dòng canon + `nhan = null`.

⛔⛔ Mỗi phép trừ chỉ có nghĩa khi hai tập ĐÚNG là tập con của nhau và ⛔ trùng — nên tệp này đếm
   HAI cách và đòi khớp (Đ2 — so HAI NGUỒN): hiệu số đếm `9.967 − 9.845` ↔ cỡ tập liệt kê; dòng ghép
   trỏ dòng sổ ⛔ có ⇒ ĐỎ, `dong_so` trùng ⇒ ĐỎ, `dong_canon` ⛔ thuộc bank ⇒ ĐỎ.

Cổng (Đ5 — khai `MONG`, NO khi khác, cả hai chiều):
  · `MONG` dưới đây: nguồn TỪNG số ghi cạnh nó. Phần do orchestrator đo TAY 16/11 (`WO-080` · ISP `:20`):
    các tổng · 3 kỳ đầu · `hd_classifying` 121/122 · `hd_final` OGA/GI/DEP/ITE. Phần DT1a TỰ ĐO 16/11 ở
    lần chạy đầu của tệp này: 15 kỳ còn lại · "khác 8" của `hd_final` · `pay_type_final` · `cdt1_final`
    — rồi R1 `KQ-082` đo ĐỘC LẬP (kịch bản ⛔ import tệp này) khớp từng số (`KQ-082:48` · `:51` · `:52`).
    `van_tay` ghim ở lần chạy đầu, sau khi mọi số khác đã khớp. *(Đính chính `DT1a-R1-05`ⓐ: bản đầu
    nói cả bộ "lấy từ phép đo TAY ĐỘC LẬP của orchestrator" — nói quá; orchestrator chỉ ghi 3 kỳ.)*
  · ⚠ VÌ SAO CÓ VÂN TAY. Các cổng TỔNG (122 · phân bố kỳ · phân bố thuộc tính) đều MÙ trước một phép
    ĐỔI CHỖ: một dòng ghép trỏ sang một dòng thiếu CÙNG kỳ, CÙNG hd/pay_type/cdt1 ⇒ 122 vẫn 122, mọi
    phân bố y nguyên, mà tập dòng DT1b sẽ gán nhãn đã khác (bài thử `…doi_cho_CUNG_KY…` dựng đúng cặp
    ấy). Đo 16/11, khoá 4 trường (kỳ · hd_classifying · hd_final · pay_type_final): **1.401** dòng ghép
    có ≥ 1 dòng thiếu cùng khoá — tức **3.810** CẶP (dòng ghép × dòng thiếu); khoá thêm `cdt1_final`
    (vòng sửa R1): 764 dòng ghép · 1.742 cặp. *(Đính chính `DT1a-R1-05`ⓑ: bản đầu gọi 1.401 là "cặp" —
    sai nhãn `Đ4`.)* Phía CANON có cùng bẫy: đổi `dong_canon` của một dòng ghép sang một dòng bank chưa
    ghép ⇒ 147 vẫn 147 — chỉ vân tay tập ngược thấy (bài `…doi_cho_phia_CANON…`). Đúng bẫy `Đ4`:
    `52 = 24 + 28` hay `38 + 14` đều ra 52.
  · ⚠ MỖI PHÉP SO CÓ CA PHÁ RIÊNG (`DT1a-R1-03`). R1 đột biến 11 cách, bộ bài đầu bắt 2/11 — chín phép
    so "đã có" mà chưa bài nào thấy chúng cắn. Nay mỗi lời gọi `kiem` trong `do()` + chốt mẫu số 0 +
    chốt riêng tư + chốt ⛔ ghi khi đỏ đều có một bài đòi CHÍNH dòng lệch của nó (bài tham số hoá
    `…moi_cong_co_ca_pha_RIENG` + các bài B2/B3/B4/CLI nêu tên ở docstring của nó). Phá thật thì nhiều
    cổng cùng đỏ (phòng thủ chồng) — nhưng bỏ MỘT cổng thì bài của nó đỏ. Thêm `kiem` mới ⇒ thêm ca.
  · Mẫu số `0` là ĐỎ, ⛔ phải `0 %` (Đ3 · `S0-R1-05`); ⛔ đo được (ảnh thiếu, JSON hỏng) là ĐỎ với
    nguyên nhân trong MỘT dòng, ⛔ traceback (`S0-R1-04`).
  · Ba checksum ảnh so `MONG` của `tools/do_voi_so_luong.py` (ISP mục 5 — tiền điều kiện) — lấy THẲNG
    từ đó, ⛔ chép lại: một bản khai. Ảnh sổ được TÍNH LẠI từ nội dung; hai ảnh kia so trường
    `checksum_noi_dung` đã ghim, ĐÚNG như `do_voi_so_luong.py` (⛔ tệp sinh ra hai ảnh ấy có trong repo
    nên ⛔ tính lại được — giới hạn đã ghi ở BG-081).
  · ⚠ CHECKSUM ẢNH SỔ ⛔ PHỦ `cot` (`DT1a-R1-04`): `_sha` của `do_voi_so_luong.py` băm `dong` +
    `bang_gia_tri`, ⛔ băm tên cột — R1 đổi NHÃN `cdt1_mid` ↔ `cdt1_final` (thân y nguyên) ⇒ công cụ bản
    đầu exit 0, `cdt1_final` in ra có `∅ 1`. ⛔ sửa `_sha` (làn BE-HC, H2 sắp chạm); thay vào đó bộ 23
    tên cột theo thứ tự có `MONG["cot_so"]`, so TRƯỚC khi giải mã.

⛔ Riêng tư (`PM_COT_RIENG_TU`, `CLAUDE.md`): `kiem_rieng_tu` chặn TRƯỚC khi ghi đúng ba thứ — khoá có tên
   chứa một mục `KHOA_CAM` (Diễn giải · Số chứng từ · email) · giá trị dạng email · chuỗi lỗi `#N/A
   (Did not find value '…')` (chuỗi ấy NHÚNG mã giao dịch). Bài `…rieng_tu_NOI_vao_duong_do_that…`
   chứng minh chốt ấy được GỌI trong đường đo (`DT1a-R1-01`). Câu khai `khong_mang_PII` của JSON được
   DỰNG từ chính `KHOA_CAM` — ⛔ khai rộng hơn cổng (`DT1a-R1-09`). Tệp này ⛔ đọc kho, ⛔ đọc
   Drive/mạng: chỉ ba ảnh trong `tests/fixture/`.

Chạy (từ gốc repo):
  python tools/phan_loai_dong_thieu.py                  # in bảng, ⛔ ghi
  python tools/phan_loai_dong_thieu.py --ghi            # + ghi docs/ITL/_tools/phan_loai_dong_thieu.json
  python tools/phan_loai_dong_thieu.py --thu-muc <dir>  # đo trên BẢN SAO ba ảnh (chứng minh ĐỎ); ⛔ cùng --ghi
Mã thoát: 0 = mọi phép so khớp MONG · 1 = ĐỎ (khác MONG, ⛔ đo được, hoặc ghi hiện vật hỏng) · 2 = sai cách gọi.
`--ghi` chỉ ghi khi mọi phép so khớp, và ghi qua TỆP TẠM + `os.replace` (`DT1a-R1-07`).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.ledger.final_rule import KHONG_TRA_LOI  # noqa: E402
# ⭐ MỘT bản khai cho checksum ảnh + cách băm ảnh sổ — ISP mục 5: "khớp MONG của do_voi_so_luong.py".
from tools.do_voi_so_luong import MONG as MONG_VOI  # noqa: E402
from tools.do_voi_so_luong import _sha  # noqa: E402

FX = GOC / "tests" / "fixture"
RA = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
ANH_SO, ANH_GHEP, ANH_PM = "itl_ledge_adjustment.json", "classifying_vs_canon.json", "pm_join.json"

# Thuộc tính đo được của một dòng thiếu (ISP Goal: kỳ · hd Classifying/MID/Final · pay_type · cdt1).
# ⛔ thêm `svc_*` · `id_payee` · `invoice`: ngoài Goal, và `id_payee`/`invoice` là đối tác/số hoá đơn.
THUOC_TINH = ("ky",
              "hd_classifying", "hd_mid", "hd_final",
              "pay_type_classifying", "pay_type_mid", "pay_type_final",
              "cdt1_classifying", "cdt1_mid", "cdt1_final")
# Bảng đếm thuộc-tính × kỳ in ra màn và ghi vào JSON (BG-081 dán bảng này).
THUOC_TINH_THEO_KY = ("hd_classifying", "hd_final", "pay_type_final", "cdt1_final")

# ── MONG — nguồn TỪNG số ghi cạnh nó (`DT1a-R1-05`; xem docstring §Cổng) ──────────────────────────────
MONG = {
    "so_dong_so": 9967,        # dòng sổ AS-IS · = do_voi_so_luong MONG so_dong_so
    "so_ky": 23,               #               · = do_voi_so_luong MONG so_ky
    "so_dong_ghep": 9845,      # dòng sổ ghép 1-1 · = do_voi_so_luong MONG so_dong_ghep_canon
    "so_dong_canon": 9992,     # dòng FLS dựng lại · = do_voi_so_luong MONG so_dong_bank
    "thieu": 122,              # = 9.967 − 9.845 (orchestrator 16/11 · ISP `:20`)
    "nguoc": 147,              # = 9.992 − 9.845 (orchestrator 16/11 · ISP `:20`)
    # Bộ tên cột ảnh sổ THEO THỨ TỰ (`DT1a-R1-04`) — so TRƯỚC khi giải mã, vì checksum ⛔ phủ `cot`.
    # Đ4: 23 = 2 cột khoá + 7 khối × (Classifying · MID · Final); khuôn 7 khối = `do_voi_so_luong.py:54`.
    "cot_so": ["dong_sheet", "ky",
               "hd_classifying", "hd_mid", "hd_final",
               "pay_type_classifying", "pay_type_mid", "pay_type_final",
               "cdt1_classifying", "cdt1_mid", "cdt1_final",
               "svc_start_classifying", "svc_start_mid", "svc_start_final",
               "svc_end_classifying", "svc_end_mid", "svc_end_final",
               "id_payee_classifying", "id_payee_mid", "id_payee_final",
               "invoice_classifying", "invoice_mid", "invoice_final"],
    # orchestrator ghi 3 kỳ đầu (2026-07 · 2025-11 · 2026-08 — ISP `:20` · `:649` · `WO-080:38`) + "…" và
    # "18/23 kỳ"; 15 kỳ còn lại DT1a TỰ ĐO 16/11; R1 `KQ-082:48` đo độc lập khớp 18/18 (tổng 122).
    # ⚠ bản đầu ghi "6 kỳ đầu · 12 kỳ sau" — sai (`DT1a-R1-05`ⓐ: ba kỳ thứ 4–6 ⛔ có ở nguồn nào).
    "phan_bo_ky_thieu": {
        "2026-07": 23, "2025-11": 14, "2026-08": 13, "2026-06": 12, "2025-10": 9, "2026-04": 8,
        "2025-12": 5, "2026-02": 5, "2026-03": 5, "2026-05": 5, "2025-07": 4, "2025-08": 4,
        "2025-09": 4, "2026-01": 4, "2025-06": 3, "2025-02": 2, "2025-01": 1, "2025-05": 1,
    },
    "hd_classifying": {KHONG_TRA_LOI: 121, "GI | Gross Inflow": 1},       # 121/122 máy ⛔ trả lời
    # OGA 74 · GI 25 · DEP 8 · ITE 7 (orchestrator); "khác 8" tách bởi DT1a 16/11.
    "hd_final": {"OGA | GAC - Other": 74, "GI | Gross Inflow": 25, "DEP | Deposit": 8,
                 "ITE | ITE Interest": 7, "NB | Lưu chuyển nội bộ": 2,
                 "OMC | Online Marketing Cost": 2, "LC | License Cost": 2,
                 "LMN | Loan/Borrowing": 1, "BON | Bonus": 1},
    "pay_type_final": {"Thanh toán (Regular)": 71, "Thu tiền": 51},   # DT1a tự đo · R1 `KQ-082:52` khớp
    # DT1a tự đo 16/11 (bảng BG-081 hàng Σ) · R1 `KQ-082:52` đo độc lập khớp (`DT1a-R1-04`: thuộc tính
    # được in làm bằng chứng thì phải có MONG). Hai ô cuối gõ lệch khuôn — GIỮ nguyên chữ ô sổ, nhãn là DT1b.
    "cdt1_final": {"SHQ1 | Headquarters1": 60, "SHQ2 | Headquarters2": 49, "COR | TeraSofts": 9,
                   "CAH | Astronex": 1, "TOR | Project A": 1, "SHQ2 | Headquarters1": 1,
                   "SHQ1| Headquarters1": 1},
    # sha256 (16 ký tự đầu) của danh sách số dòng đã sắp — ghim lần chạy đầu 16/11 (xem docstring).
    "van_tay": {"thieu": "18047e0eb0319ea1", "nguoc": "6ac2463a190ff631"},
}
# Phân bố thuộc tính của dòng thiếu có MONG — vòng `kiem` ở `do()` đi đúng bộ này.
PHAN_BO_CO_MONG = ("hd_classifying", "hd_final", "pay_type_final", "cdt1_final")

# ⛔ Khoá cấm — so trên tên khoá đã bỏ dấu, thường hoá, bỏ ký tự lạ. HAI bản (đây + bài thử) — cố ý, bài
#   ⛔ dùng máy quét của chính đối tượng nó kiểm; bài `…khong_mang_PII_BANG_tap_may_chan` đòi hai bản bằng.
# ⚠ `DT1a-R1-09` — vì sao THU câu khai về đúng tập này, ⛔ thêm `taikhoan` · `tien`:
#   ① `taikhoan` (so CHUỖI CON) cắn cả `Tên tài khoản` — cột owner quyết GIỮ (11/09, `CLAUDE.md` §Riêng
#     tư); chặn nó ở đây là một quyết định chính sách riêng tư, ⛔ phải việc của Dev trong vòng sửa.
#   ② `tien` (chuỗi con) cắn nhầm khoá vô hại DT1b có thể thêm (`tien_te` · `uu_tien`) — cổng ồn sẽ bị
#     nới bằng danh sách miễn trừ, đúng thứ `CLAUDE.md` cấm.
#   ③ Ảnh sổ (23 cột) và ảnh ghép (22 cột) ⛔ có cột Số CT · TK · tiền (đo vòng sửa: trường `cot` của hai
#     ảnh). `pm_join` CÓ `tien` · `ref_tho` ở dòng bank — nhưng công cụ chỉ đọc trường `dong` của nó
#     (`do()` mục ③). Việc JSON ra chỉ mang số dòng · kỳ · 9 ô phân loại là do CẤU TRÚC (`do()` dựng từng
#     dòng từ `THUOC_TINH`; bài B1 đòi đúng tập khoá từng dòng), ⛔ do `KHOA_CAM` — chặn tên khoá mà
#     công cụ ⛔ bao giờ sinh ra là cổng trên tập rỗng (`Đ3`).
KHOA_CAM = ("diengiai", "sochungtu", "email")
MAU_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
MAU_REF_TRONG_LOI = "Did not find value"         # `#N/A (Did not find value 'FT…' …)` nhúng mã giao dịch
# Câu khai của hiện vật — DỰNG từ `KHOA_CAM`, nên BẰNG tập máy chặn (`DT1a-R1-09`). ⛔ chép chuỗi
# `MAU_REF_TRONG_LOI` vào đây: câu khai sẽ tự vấp chính máy quét.
KHAI_RIENG_TU = ("Máy chặn TRƯỚC khi ghi (kiem_rieng_tu) đúng ba thứ: khoá có tên chứa "
                 + " · ".join(KHOA_CAM)
                 + " (so trên tên đã bỏ dấu, thường hoá) · giá trị dạng email · ô lỗi #N/A nhúng mã giao dịch. "
                 "Ngoài phép chặn ấy là CẤU TRÚC: mỗi dòng thiếu chỉ mang dong_sheet · "
                 + " · ".join(THUOC_TINH) + " · nhan; mỗi dòng ngược chỉ dong_canon · nhan.")


def _nap(thu_muc: Path, ten: str) -> dict:
    return json.loads((thu_muc / ten).read_text(encoding="utf-8"))


def _van_tay(so_dong: list[int]) -> str:
    return hashlib.sha256(json.dumps(so_dong, separators=(",", ":")).encode()).hexdigest()[:16]


def _so(n: int) -> str:
    """Số kiểu Việt: 9967 → `9.967`."""
    return f"{n:,}".replace(",", ".")


def _ty_le(tu: int, mau: int) -> str:
    return f"{tu * 100 / mau:.2f}".replace(".", ",") + " %"


def _phan_bo(gia_tri) -> list[list]:
    """Đếm → danh sách `[giá trị, số dòng]` (nhiều trước). ⛔ dict: giá trị `None` ⛔ làm khoá JSON được."""
    return [[v, n] for v, n in sorted(Counter(gia_tri).items(),
                                      key=lambda x: (-x[1], "" if x[0] is None else str(x[0])))]


def _bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def kiem_rieng_tu(d) -> list[str]:
    """Mọi vi phạm riêng tư trong `d`: khoá mang tên cấm · giá trị là email · ô lỗi nhúng mã giao dịch."""
    vi_pham: list[str] = []

    def di(x, duong: str) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if any(c in _bo_dau(str(k)) for c in KHOA_CAM):
                    vi_pham.append(f"riêng tư: khoá cấm {duong}/{k}")
                di(v, f"{duong}/{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                di(v, f"{duong}[{i}]")
        elif isinstance(x, str):
            if MAU_EMAIL.search(x):
                vi_pham.append(f"riêng tư: email ở {duong}")
            if MAU_REF_TRONG_LOI in x:
                vi_pham.append(f"riêng tư: ô lỗi nhúng mã giao dịch ở {duong}")

    di(d, "")
    return vi_pham


def do(thu_muc: Path = FX) -> tuple[dict, list[str]]:
    """Đo trên ba ảnh ở `thu_muc` → (nội dung JSON, danh sách lệch MONG). Ảnh ⛔ đọc được ⇒ ngoại lệ."""
    loi: list[str] = []

    def kiem(ten: str, co, mong) -> None:
        if co != mong:
            loi.append(f"{ten}: đo {co!r} · mong {mong!r}")

    g, c, p = _nap(thu_muc, ANH_SO), _nap(thu_muc, ANH_GHEP), _nap(thu_muc, ANH_PM)
    ck = MONG_VOI["checksum"]
    kiem("checksum itl_ledge_adjustment (tính lại)", _sha(g["dong"], g["bang_gia_tri"]), ck[ANH_SO])
    kiem("checksum classifying_vs_canon (trường đã ghim)", c["checksum_noi_dung"], ck[ANH_GHEP])
    kiem("checksum pm_join (trường đã ghim)", p["checksum_noi_dung"], ck[ANH_PM])
    # Checksum ảnh sổ ⛔ phủ `cot` ⇒ tên cột so RIÊNG, TRƯỚC khi dùng để giải mã (`DT1a-R1-04`)
    kiem("tên cột ảnh sổ (cot, 23 tên theo thứ tự)", list(g["cot"]), MONG["cot_so"])

    # ① sổ AS-IS: dong_sheet → thuộc tính
    idx = {t: i for i, t in enumerate(g["cot"])}
    bang = g["bang_gia_tri"]
    so: dict[int, dict] = {}
    for h in g["dong"]:
        o = {"ky": h[idx["ky"]]}
        for t in THUOC_TINH[1:]:
            i = h[idx[t]]
            o[t] = None if i == -1 else bang[i]
        so[h[idx["dong_sheet"]]] = o
    kiem("dong_sheet ⛔ trùng (số dòng ảnh sổ ↔ số dong_sheet khác nhau)", len(so), len(g["dong"]))

    # ② ghép 1-1 sổ ↔ FLS
    i_so, i_canon = c["cot"].index("dong_so"), c["cot"].index("dong_canon")
    ds_so = [r[i_so] for r in c["dong"]]
    ds_canon = [r[i_canon] for r in c["dong"]]
    ghep, ghep_canon = set(ds_so), set(ds_canon)
    kiem("dong_so ⛔ trùng (dòng ghép ↔ dong_so khác nhau)", len(ghep), len(ds_so))
    kiem("dong_canon ⛔ trùng (dòng ghép ↔ dong_canon khác nhau)", len(ghep_canon), len(ds_canon))
    # Trường KHAI của ảnh ghép ↔ số ĐẾM được (Đ2 — hai nguồn; ⛔ so một nguồn với chính nó)
    kiem("số dòng sổ: trường so_dong_so của ảnh ghép ↔ đếm ảnh sổ", c["so_dong_so"], len(so))
    kiem("số dòng ghép: trường so_dong_ghep của ảnh ↔ đếm", c["so_dong_ghep"], len(ghep))
    kiem("dòng ghép trỏ dòng sổ ⛔ có trong ảnh sổ", len(ghep - set(so)), 0)

    # ③ dòng FLS dựng lại (bank của pm_join) — `so_dong_canon` của ảnh ghép là HAI NGUỒN cho cùng số
    bank = {b["dong"] for b in p["bank"]}
    kiem("số dòng canon: trường so_dong_canon của ảnh ghép ↔ dòng bank pm_join", c["so_dong_canon"], len(bank))
    kiem("dong_canon đã ghép ⛔ thuộc bank pm_join", len(ghep_canon - bank), 0)

    mau_so = {"so_dong_so": len(so), "so_dong_ghep": len(ghep), "so_dong_canon": len(bank)}
    if 0 in mau_so.values():                    # Đ3 — mẫu số rỗng là KẾT QUẢ, ⛔ nền cho tỷ lệ
        loi.append(f"mẫu số = 0 — ⛔ đo được tỷ lệ nào (Đ3): {mau_so}")
        return {"mau_so": mau_so}, loi
    kiem("số dòng sổ", mau_so["so_dong_so"], MONG["so_dong_so"])
    cac_ky = sorted({o["ky"] for o in so.values()})
    kiem("số kỳ", len(cac_ky), MONG["so_ky"])
    kiem("số dòng ghép", mau_so["so_dong_ghep"], MONG["so_dong_ghep"])
    kiem("số dòng canon", mau_so["so_dong_canon"], MONG["so_dong_canon"])

    # ④ hai tập — mỗi tập đếm HAI cách (hiệu số ↔ tập liệt kê)
    thieu = sorted(set(so) - ghep)
    nguoc = sorted(bank - ghep_canon)
    kiem("dòng sổ ⛔ ghép (sổ ∖ ghép)", len(thieu), MONG["thieu"])
    kiem("dòng sổ ⛔ ghép: hiệu trường khai so_dong_so − so_dong_ghep ↔ tập liệt kê",
         c["so_dong_so"] - c["so_dong_ghep"], len(thieu))
    kiem("dòng FLS ⛔ có dòng sổ (canon ∖ ghép)", len(nguoc), MONG["nguoc"])
    kiem("dòng FLS ⛔ có dòng sổ: hiệu trường khai so_dong_canon − so_dong_ghep ↔ tập liệt kê",
         c["so_dong_canon"] - c["so_dong_ghep"], len(nguoc))

    dong_thieu = [{"dong_sheet": d, **so[d], "nhan": None} for d in thieu]
    dong_nguoc = [{"dong_canon": d, "nhan": None} for d in nguoc]
    phan_bo_ky = Counter(o["ky"] for o in dong_thieu)
    kiem("phân bố kỳ của dòng thiếu", dict(phan_bo_ky), MONG["phan_bo_ky_thieu"])
    for t in PHAN_BO_CO_MONG:
        kiem(f"phân bố {t} của dòng thiếu", dict(Counter(o[t] for o in dong_thieu)), MONG[t])
    van_tay = {"thieu": _van_tay(thieu), "nguoc": _van_tay(nguoc)}
    kiem(f"vân tay tập thiếu (sha256 của {len(thieu)} dong_sheet đã sắp)", van_tay["thieu"], MONG["van_tay"]["thieu"])
    kiem(f"vân tay tập ngược (sha256 của {len(nguoc)} dong_canon đã sắp)", van_tay["nguoc"], MONG["van_tay"]["nguoc"])

    kq = {
        "_vi_sao": ("Sinh bởi `python tools/phan_loai_dong_thieu.py --ghi` từ ba ảnh đóng băng tests/fixture/ "
                    "(ISP 3.1.2 Step 3 · DT1a · WO-080). ⛔ sửa tay — bài tests/du_lieu/test_phan_loai_dong_thieu.py "
                    "đòi tệp này BẰNG lần đo hiện tại. `nhan` = null: LÝ DO là việc của DT1b."),
        "khong_mang_PII": KHAI_RIENG_TU,         # = tập máy chặn (DT1a-R1-09), ⛔ khai rộng hơn
        "nguon": {"so": g["nguon"], "so_dong_bang": g["ngay_dong_bang"], "ghep": c["nguon"],
                  "bank": p["nguon"], "checksum": dict(ck)},
        "mau_so": mau_so,
        "dem": {"thieu": len(thieu), "nguoc": len(nguoc), "so_ky": len(cac_ky),
                "so_ky_co_thieu": len(phan_bo_ky)},
        "theo_ky": {k: {"so_dong_so": sum(1 for o in so.values() if o["ky"] == k),
                        "thieu": phan_bo_ky.get(k, 0)} for k in cac_ky},
        "phan_bo_thuoc_tinh": {t: _phan_bo(o[t] for o in dong_thieu) for t in THUOC_TINH[1:]},
        "thuoc_tinh_theo_ky": {t: {k: _phan_bo(o[t] for o in dong_thieu if o["ky"] == k)
                                   for k in cac_ky if phan_bo_ky.get(k)} for t in THUOC_TINH_THEO_KY},
        "van_tay": van_tay,
        "dong_thieu": dong_thieu,
        "dong_nguoc": dong_nguoc,
    }
    loi.extend(kiem_rieng_tu(kq))                # chặn TRƯỚC khi ghi — lệch ⇒ ĐỎ như mọi phép so
    return kq, loi


def in_bao_cao(kq: dict, thu_muc: Path) -> None:
    ms = kq["mau_so"]
    try:
        noi = thu_muc.resolve().relative_to(GOC)
    except ValueError:
        noi = thu_muc
    print(f"PHÂN LOẠI DÒNG THIẾU — HD1 · ba ảnh ở {noi}")
    # Đ3: MẪU SỐ in TRƯỚC mọi tỷ lệ, mỗi số mang nhãn NÓ ĐẾM GÌ (Đ4)
    print(f"① MẪU SỐ: sổ AS-IS {_so(ms['so_dong_so'])} dòng sổ · ghép 1-1 {_so(ms['so_dong_ghep'])} dòng ghép · "
          f"FLS dựng lại {_so(ms['so_dong_canon'])} dòng canon")
    if "dem" not in kq:
        return
    d = kq["dem"]
    print(f"② dòng sổ ⛔ ghép: {_so(d['thieu'])} / {_so(ms['so_dong_so'])} dòng sổ = "
          f"{_ty_le(d['thieu'], ms['so_dong_so'])} · rải {d['so_ky_co_thieu']}/{d['so_ky']} kỳ "
          f"· hiệu {_so(ms['so_dong_so'])} − {_so(ms['so_dong_ghep'])}")
    print(f"③ dòng FLS ⛔ có dòng sổ: {_so(d['nguoc'])} / {_so(ms['so_dong_canon'])} dòng canon = "
          f"{_ty_le(d['nguoc'], ms['so_dong_canon'])} · hiệu {_so(ms['so_dong_canon'])} − {_so(ms['so_dong_ghep'])}")
    print(f"④ thuộc tính của {_so(d['thieu'])} dòng thiếu (đếm DÒNG):")
    for t, pb in kq["phan_bo_thuoc_tinh"].items():
        print(f"   {t:22s} " + " · ".join(f"{'∅' if v is None else v} {n}" for v, n in pb))
    print("⑤ theo kỳ (đếm DÒNG; % = thiếu / dòng sổ của kỳ):")
    print(f"   {'kỳ':8s} {'sổ':>5s} {'thiếu':>6s} {'%':>8s}  hd_final · pay_type_final")
    for k, x in kq["theo_ky"].items():
        hd = kq["thuoc_tinh_theo_ky"]["hd_final"].get(k, [])
        pt = kq["thuoc_tinh_theo_ky"]["pay_type_final"].get(k, [])
        chi_tiet = " · ".join(f"{v} {n}" for v, n in hd)
        if pt:
            chi_tiet += "  ‖  " + " · ".join(f"{v} {n}" for v, n in pt)
        print(f"   {k:8s} {x['so_dong_so']:5d} {x['thieu']:6d} {_ty_le(x['thieu'], x['so_dong_so']):>8s}  {chi_tiet}")
    print(f"   vân tay: thiếu {kq['van_tay']['thieu']} · ngược {kq['van_tay']['nguoc']}")


def _ghi_qua_tep_tam(dich: Path, noi_dung: str) -> None:
    """Ghi hiện vật qua TỆP TẠM cạnh đích → đọc lại kiểm → `os.replace` (nguyên tử trên cùng thư mục).

    `DT1a-R1-07` · `11_BOI_CANH_TU_MEMORY.md` §2: *"mở tệp chế độ ghi là xoá ngay — lỗi ở `.write()` để
    lại tệp 0 byte ⇒ ghi ra tệp tạm → kiểm → chép đè"*. Bản đầu `write_text` thẳng lên đích. Hỏng ở BẤT
    KỲ bước nào ⇒ hiện vật cũ y nguyên, tệp tạm được dọn, `OSError` ném lên cho `main` báo MỘT dòng."""
    tam = dich.with_name(dich.name + ".tam")
    try:
        tam.write_text(noi_dung, encoding="utf-8")
        if tam.read_text(encoding="utf-8") != noi_dung:
            raise OSError(f"đọc lại {tam.name} ⛔ khớp nội dung vừa ghi")
        os.replace(tam, dich)
    finally:
        tam.unlink(missing_ok=True)               # thay xong thì tệp tạm ⛔ còn — no-op


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="HD1 · kiểm kê dòng sổ AS-IS chưa ghép 1-1 (DT1a).")
    ap.add_argument("--ghi", action="store_true", help=f"ghi {RA.relative_to(GOC)} (chỉ từ ảnh thật)")
    ap.add_argument("--thu-muc", type=Path, default=None,
                    help="đo trên bản SAO ba ảnh ở thư mục này (chứng minh ĐỎ) — ⛔ dùng cùng --ghi")
    a = ap.parse_args(argv)
    if a.ghi and a.thu_muc is not None:
        print(f"⛔ TỪ CHỐI: --ghi chỉ ghi từ ảnh thật {FX.relative_to(GOC)}/ — ⛔ ghi hiện vật từ bản sao (--thu-muc)",
              file=sys.stderr)
        return 2
    thu_muc = a.thu_muc if a.thu_muc is not None else FX
    try:
        kq, loi = do(thu_muc)
    except Exception as e:                        # Đ5: ⛔ đo được là ĐỎ — nguyên nhân MỘT dòng (S0-R1-04)
        print(f"LOI {type(e).__name__}: " + " ".join(str(e).split()), file=sys.stderr)
        return 1
    in_bao_cao(kq, thu_muc)
    if loi:
        print(f"⛔ PHÂN LOẠI DÒNG THIẾU ĐỎ — {len(loi)} chỗ khác MONG (⛔ ghi JSON):", file=sys.stderr)
        for x in loi:
            print("  " + x, file=sys.stderr)
        return 1
    print(f"KẾT: ĐẠT — mọi phép so khớp MONG · {_so(kq['dem']['thieu'])} dòng thiếu + "
          f"{_so(kq['dem']['nguoc'])} dòng ngược · nhan = null (DT1b điền)")
    if a.ghi:                                     # chỉ tới đây khi `loi` rỗng — lượt ĐỎ ⛔ chạm hiện vật (M8)
        try:
            _ghi_qua_tep_tam(RA, json.dumps(kq, ensure_ascii=False, indent=1) + "\n")
        except OSError as e:                      # S0-R1-04: nguyên nhân MỘT dòng, ⛔ traceback
            print(f"LOI {type(e).__name__}: " + " ".join(str(e).split()) + " — hiện vật cũ y nguyên",
                  file=sys.stderr)
            return 1
        print(f"✅ đã ghi {RA.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
