# -*- coding: utf-8 -*-
"""PHÂN LOẠI LÝ DO — HD1 · gán LÝ DO cho 122 dòng sổ AS-IS chưa ghép 1-1, bằng khoá đọc ở NGUỒN.

ISP 3.1.2 · Step 5 · DT1b · dải phiếu `WO-095` / `BG-096` · AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10 · §4.3.1.

⭐ Vì sao có tệp này. DT1a (`tools/phan_loai_dong_thieu.py`, `BG-081`; R1 `KQ-082` đo độc lập khớp) liệt
   kê ĐÚNG 122 dòng sổ ⛔ ghép 1-1 (vân tay `18047e0eb0319ea1`) — nhưng ⛔ nói được VÌ SAO: ảnh đóng
   băng đã bỏ Số CT · TK · tiền (riêng tư). Tệp này nhận khoá đọc ở nguồn, gán mỗi dòng ĐÚNG MỘT nhãn
   trong bảng đóng, ghi nhãn kèm khoá ĐÃ BĂM, và ĐỎ khi khác MONG.

⭐ Hai quyết định orchestrator — LỆCH CHỮ ISP `:788` · `:798` · `:824` (ghi ở BG-096):
   · Q2 của DT1a = A: nhãn ra TỆP RIÊNG `docs/ITL/_tools/phan_loai_ly_do.json`, khoá `dong_sheet` + hai
     vân tay tập dòng của DT1a; ⛔ sửa `phan_loai_dong_thieu.json`; công cụ là TỆP MỚI này (⛔ thêm chế
     độ `--khoa` vào tool DT1a — tệp ấy đang được phiên khác sửa sau R1).
   · Khoá THẬT ⛔ đọc được ở container (`B-DATA-2`, đo 16/11: RAW gốc `1md85t…` ⇒ Permission denied;
     bản sao ADJUSTED ⇒ `get_values` hết giờ 60 s — `GAP-ORA-08`) ⇒ lượt gán nhãn THẬT do owner chạy
     trên máy có `Input_Raw/[Master] ITL_Ledge_raw.xlsx` (O10). Ở container chỉ có dữ liệu TỔNG HỢP của
     bài thử; ⛔ có đầu vào ⇒ mã RIÊNG 3 `⛔ CHƯA ĐO ĐƯỢC` (Đ5: ⛔ phải "không thấy lệch").

ĐỊNH DẠNG ĐẦU VÀO — một tệp CSV UTF-8 (BOM được), HAI BẢNG xếp chồng, ĐÚNG 7 cột (thứ tự tự do):
  `bang,dong,so_ct,ps_no,ps_co,tk,tien_te`
  · `bang = SO` — sổ `ITL Ledge` của `[Master] ITL_Ledge_raw.xlsx`; `dong` = số hàng Excel, CÙNG hệ với
    `dong_sheet` của ảnh 26/08 (hàng dữ liệu đầu = 10, cuối = 9976). Phải đủ CẢ 9.967 dòng — `TRUNG_SEQ`
    cần biết bao nhiêu dòng sổ cùng một khoá; công cụ đòi tập `dong` = tập `dong_sheet` của ảnh.
  · `bang = L1` — `Transaction Mapping L1` của RAW `1md85t…` (`fls/oracle/nguon.py` `BAN_SAO_RAW`, cột
    B · E · F · G · D); `dong` = số hàng của sheet, CHỈ để định danh trong tệp: ⛔ bao giờ ghép theo nó
    (bản sao 13/11 ≠ ảnh 26/08 — hàng đã xê dịch, có hàng mới).
  · 5 cột khoá = nguyên văn `Số chứng từ` · `PS Nợ` · `PS Có` · `Tài khoản` · `Đơn vị tiền tệ` (`fls/canon/
    spec.py`), xuất thô như ô hiện. Cột NGOÀI 7 cột ⇒ ĐỎ — `Diễn giải` · email ⛔ bao giờ đi cùng được.

KHUÔN TỆP NHÃN — HỢP ĐỒNG với H2 (orchestrator 16/11: `tools/do_voi_so_luong.py` ĐỌC tệp này; khác khuôn ⇒ đỏ
  lúc gộp): `{"van_tay": {"thieu": <16 hex>, "nguoc": <16 hex>}, "dong_thieu": [{"dong_sheet": <int>, "nhan": <chuỗi>
  | null}, …]}` — đúng khuôn `phan_loai_dong_thieu.json` của DT1a; vân tay = vân tay tính lại từ ảnh (qua danh sách
  DT1a); `dong_sheet` số nguyên (⛔ `True`). Khoá thừa được phép với H2 — ở đây mỗi dòng còn `ky` · `khoa_bam` ·
  `lech` · `ghi_chu`, và lược đồ của CHÍNH tệp này ĐÓNG (R1) để ⛔ chuỗi tự do nào lọt vào.

Nhãn (bảng đóng — ISP 3.1.2 `:784`; nghĩa theo ISP 3.1.1 `:685` vì 3.1.2 ⛔ khai lại):
  khoá k = 5 trường ĐÃ chuẩn hoá (fixture `classifying_vs_canon.json` · `ghep_bang`: *"khoá = (Số chứng từ,
  PS Nợ, PS Có, Tài khoản, Đơn vị tiền tệ) + seq trùng"*) ⇒ trong một nhóm khoá, dòng sổ thứ i ghép dòng
  L1 thứ i. Với một dòng thiếu d có khoá k — gọi o(k) = số dòng sổ ĐÃ ghép (theo DT1a) mang khoá k:
   · `KHAC` + `KHOA_HONG:<trường>` — ô tiền là ô lỗi Sheets hoặc ⛔ đọc được số ⇒ khoá ⛔ so được.
   · L1 CÓ dòng khoá k, còn chỗ (số dòng L1 của k > o(k)) ⇒ `KHAC` + `KHOP_KHI_GHEP_LAI`: khoá GHÉP ĐƯỢC
     mà mã gốc ⛔ ghép — lớp lỗi MÃ cho H3, hoặc bản L1 đã đổi sau 26/08.
   · L1 CÓ dòng khoá k, hết chỗ ⇒ `TRUNG_SEQ` — sổ có nhiều dòng cùng khoá hơn L1 (seq vượt).
   · L1 ⛔ có dòng khoá k, nhưng có dòng L1 CHƯA AI GHÉP trùng Số CT (khác rỗng) HOẶC trùng cả bốn trường
     còn lại ⇒ `KHOA_LECH`; `lech` = các trường khác nhau của ứng viên ít trường lệch nhất (hoà ⇒ khoá
     nhỏ nhất theo thứ tự chuỗi — ⛔ theo số hàng, để kết quả ⛔ phụ thuộc vị trí).
   · còn lại ⇒ `KHONG_CO_SAO_KE`.
  ⛔ NGÀY trong khoá (bản xlsx hỏng ngày — đúng phép ghép gốc, ISP mục 3) · ⛔ Diễn giải (riêng tư).

CHUẨN HOÁ — mỗi luật MỘT bản khai, mượn đúng chỗ repo đã khai (⛔ viết bản thứ hai):
  Số CT          → `fls.adapters.pm_join.canon_ref`: gỡ dạng khoa học `4.36619E+15` → `4366190000000000`
                   (y bài `tests/adapters/test_pm_join.py:58`), NFKC, chữ hoa, bỏ `[\\s\\-_.,/\\\\]`; ô lỗi ⇒ rỗng.
  PS Nợ / PS Có  → `fls.canon.validate.parse_so`: chuỗi có dấu phân cách `'2,730,128.00'` → `2730128`;
                   trống ≡ `0`; ô lỗi / rác ⇒ HỎNG (`None`).
  Tiền tệ        → `fls.canon.tien_te.ma_tien_te` (một tập 30 ký tự trắng, chữ hoa); ô lỗi ⇒ rỗng.
  Tài khoản      → NFKC, gỡ trắng hai mép, chữ hoa; ô lỗi ⇒ rỗng.
  ⭐ Vì sao "trống ≡ 0" và "ô lỗi Số CT ⇒ rỗng" (luật NỚI): phép TÁI LẬP = Σₖ min(o(k), số dòng L1 của k),
     mà min cộng dồn ⇒ NỚI chuẩn hoá (gộp nhóm) chỉ làm tái lập TĂNG. ⇒ Chuẩn hoá quá CHẶT (đúng bẫy fixture:
     98,8 % → 16,6 %) bị cổng TÁI LẬP bắt ĐỎ; quá NỚI thì hiện ra thành `KHOP_KHI_GHEP_LAI` / `KHOA_LECH`
     đếm được — ⛔ bao giờ im lặng. Luật chặt hơn chỉ được thêm khi lượt thật chứng minh cần.

Cổng (Đ5 — khai MONG trước, NO khi khác; mỗi phép một ca phá RIÊNG ở `tests/du_lieu/test_phan_loai_ly_do.py`
— luật phòng tái phạm `DT1a-R1-03`; ca nào chỉ là phòng thủ chồng thì ghi rõ):
  K1  vân tay tập THIẾU của DT1a (tính lại) ↔ MONG          · bài `…van_tay_DT1a_lech…` (vế thiếu)
  K2  vân tay tập NGƯỢC của DT1a (tính lại) ↔ MONG          · bài `…van_tay_DT1a_lech…` (vế ngược)
  K3  vân tay ghi trong tệp nhãn ↔ MONG                     · PHA `van_tay_tep`
  K4  mỗi dòng ĐÚNG một nhãn: 2 nhãn (danh sách · dòng lặp) · 0 nhãn (null · vắng) · nhãn lạ · dòng
      ngoài tập 122                                         · bài `…hai_nhan…` · PHA `0_nhan` `vang_mot_dong` `nhan_la` `dong_ngoai_122`
  K5  `dem_nhan` = đếm lại từ dòng (hai nguồn)             · PHA `dem_nhan_lech` (Σ giữ 122)
  K5b Σ `dem_nhan` = 122 — PHÒNG THỦ CHỒNG, ⛔ chứng minh riêng được: K4 đạt (đúng 122 dòng, mỗi dòng một nhãn
      hợp lệ) + K5 đạt ⇒ Σ = 122 tất yếu; đột biến M12 16/11 SỐNG là đúng. Giữ vì ISP Goal `:784` khai nguyên chữ.
  K6  `KHAC` ⇒ ghi chú trong tập đóng · `KHOA_LECH` ⇒ `lech` ⊂ 5 trường, khác rỗng · nhãn khác ⇒ cả hai trống
                                                            · PHA `KHAC_thieu_ghi_chu` `KHOA_LECH_thieu_lech`
  K7  kỳ của dòng = kỳ DT1a · `nhan_theo_ky` = đếm lại     · PHA `ky_lech` `theo_ky_lech`
  K8  mẫu số > 0 (Đ3)                                       · PHA `mau_so_0` · bài `…mau_so_0…`
  K9  mẫu số khai = MONG (122 · 9.967 · 9.845)               · PHA `mau_so_khai_thieu` `mau_so_khai_so` `mau_so_khai_lech`
  K10 TÁI LẬP khoá+seq = 9.845 dòng ghép DT1a               · PHA `tai_lap` · bài `…bo_chuan_hoa…`
  K11 (lúc đo) tập `dong` phía SO = 9.967 `dong_sheet` ảnh  · bài `…tap_dong_sheet_lech…`
  K12 (lúc đo) định dạng đóng: cột · `bang` · `dong` nguyên · ⛔ trùng · bài `…sai_dinh_dang…` `…Dien_giai…`
  R1  lược đồ: khoá gốc / `nguon` / `mau_so` / mỗi dòng đúng tập khoá · PHA `khoa_ngoai_luoc_do`
  R2  `khoa_bam` = 16 ký tự hex                             · PHA `khoa_bam_khong_hex`
  R3  email trong mọi chuỗi (khoá lẫn giá trị)              · PHA `email` · bài `…NOI_vao_duong_do_that` ②
  R4  chuỗi `Did not find value` (ô `#N/A` nhúng mã)        · PHA `o_loi_nhung_ma`
  R6  tên khoá ở MỌI tầng chứa `diengiai` · `sochungtu` · `soct` · `email` (bỏ dấu, thường hoá) — chốt RIÊNG
      của công cụ này, ⛔ mượn `KHOA_CAM` của DT1a (orchestrator 16/11) · PHA `khoa_cam_Dien_giai`
  R7  (vòng sửa R1 — DT1b-R1-04) đóng GIÁ TRỊ, ⛔ chỉ tên khoá: mọi LÁ = hằng (`_vi_sao` · `khong_mang_PII` ·
      `nguon.tep_dt1a`/`anh_so`) · mẫu (`nguon.ban_doc_sha256_16` hex16) · tập đóng + int ≥ 0 (`mau_so.khoa_hong` ·
      `dang_khoa_hoc`) · int (số đếm `mau_so`). Câu lỗi nêu TÊN LÁ, ⛔ in giá trị · bài `…DE_XUAT_la_chuoi_TU_DO…`
  R8  (vòng sửa R1 — DT1b-R1-06) từ chối bản đọc khoá nằm TRONG repo mà ⛔ bị `.gitignore` (mã 2) · bài `…trong_repo…`
  K4b `dong_sheet` là số nguyên, ⛔ bool (hợp đồng H2)    · PHA `dong_sheet_bool`
  R5  (lúc đo) token trùng Số CT ≥ 6 ký tự (thô / chuẩn hoá) hoặc tiền ≥ 6 chữ số của đầu vào
                                                            · bài `…NOI_vao_duong_do_that` ① · `…R5_moi_dang…` ⑦
  M   phân bố nhãn ↔ `MONG["phan_bo_nhan"]` — `None` ⇒ mã 4 · bài `…phan_bo_KHAC…` · `…CHUA_GHIM…`
  K13 (vòng sửa R1 — DT1b-R1-05) vân tay DANH TÍNH nhãn ↔ `MONG["van_tay_nhan"]` — `None` ⇒ mã 4; đổi chỗ nhãn
      hai dòng cùng kỳ giữ nguyên MỌI số đếm nhưng cắn ở đây · bài `…DE_XUAT_doi_nhan_HAI_dong_cung_ky…`
  ⚠ `MONG["phan_bo_nhan"] = None` · `MONG["van_tay_nhan"] = None`: ⛔ phép đo độc lập nào có trước lượt thật của
     owner — ghim CÙNG lượt (orchestrator chốt), kèm nguồn; tới lúc đó công cụ trả 4, ⛔ bao giờ 0.

⛔ Riêng tư: tệp ra ⛔ mang giá trị khoá — chỉ `khoa_bam` = sha256 (16 ký tự đầu) của bộ 5 trường ĐÃ chuẩn
   hoá, ⛔ băm từng trường (một trường tiền / TK đơn lẻ dò ngược được trong tích tắc). Câu `khong_mang_PII`
   trong tệp ra = ĐÚNG tập R1–R5 máy chặn (luật `DT1a-R1-09`). ⛔ đọc kho · ⛔ Drive · ⛔ mạng.

Chạy (từ gốc repo):
  python tools/phan_loai_ly_do.py --khoa <bản_đọc.csv>          # ĐO trên bản đọc khoá, in bảng, ⛔ ghi
  python tools/phan_loai_ly_do.py --khoa <bản_đọc.csv> --ghi    # + ghi docs/ITL/_tools/phan_loai_ly_do.json
  python tools/phan_loai_ly_do.py [--tep <tệp nhãn>]           # CỔNG: kiểm tệp nhãn đã có (mặc định tệp repo)
Mã thoát: 0 ĐẠT · 1 ĐỎ (khác MONG / ⛔ đo được / đầu vào sai định dạng) · 2 sai cách gọi (gồm đường dẫn là
          thư mục · bản đọc khoá nằm trong repo ⛔ bị .gitignore — R8) · 3 ⛔ CHƯA ĐO ĐƯỢC (⛔ có bản đọc
          khoá / ⛔ có tệp nhãn) · 4 ĐO ĐƯỢC nhưng MONG phân bố / vân tay nhãn CHƯA GHIM.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import subprocess
import sys
import unicodedata
from collections import Counter, defaultdict
from decimal import Decimal
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

# ⭐ MỘT bản khai mỗi luật chuẩn hoá — mượn tên CÔNG KHAI (⛔ `_x` xuyên làn — luật `DT1a-R1-06`).
from fls.adapters.pm_join import canon_ref  # noqa: E402
from fls.canon.o_loi import la_o_loi  # noqa: E402
from fls.canon.tien_te import ma_tien_te  # noqa: E402
from fls.canon.validate import parse_so  # noqa: E402

DT1A = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
ANH_SO = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"
RA = GOC / "docs" / "ITL" / "_tools" / "phan_loai_ly_do.json"
# Hằng đường dẫn khai trong `nguon` của tệp ra — R7 (DT1b-R1-04) đóng GIÁ TRỊ hai lá này bằng chính chúng.
NGUON_TEP_DT1A = "docs/ITL/_tools/phan_loai_dong_thieu.json"
NGUON_ANH_SO = "tests/fixture/itl_ledge_adjustment.json"

DAT, DO, SAI_GOI, CHUA_DO_DUOC, CHUA_GHIM = 0, 1, 2, 3, 4

NHAN = ("KHONG_CO_SAO_KE", "KHOA_LECH", "TRUNG_SEQ", "KHAC")       # bảng ĐÓNG — ISP 3.1.2 `:784`
COT_KHOA = ("so_ct", "ps_no", "ps_co", "tk", "tien_te")           # thứ tự khoá ghép gốc (fixture `ghep_bang`)
COT_TIEN = ("ps_no", "ps_co")
COT_VAO = ("bang", "dong") + COT_KHOA
GHI_CHU_KHOP = "KHOP_KHI_GHEP_LAI"
MAU_GHI_CHU_HONG = re.compile(r"^KHOA_HONG:(ps_no|ps_co|ps_no,ps_co)$")

# ── MONG — mỗi số trỏ NƠI GHI (luật `DT1a-R1-05`) ───────────────────────────────────────────────────
MONG = {
    "thieu": 122,              # BG-081 · KQ-082 đo độc lập (dòng sổ ⛔ ghép)
    "so_dong_so": 9967,        # BG-081 · KQ-082 (dòng `dong_sheet` của ảnh sổ 26/08)
    "so_dong_ghep": 9845,      # BG-081 · KQ-082 (dòng sổ ghép 1-1 — mẫu số của TÁI LẬP)
    "van_tay": {"thieu": "18047e0eb0319ea1", "nguoc": "6ac2463a190ff631"},   # BG-081 · KQ-082
    # ⛔ CHƯA GHIM — khoá thật ⛔ đọc được ở container; ghim sau lượt thật của owner (O10), kèm nguồn.
    "phan_bo_nhan": None,
    # ⛔ CHƯA GHIM — K13 (DT1b-R1-05): vân tay DANH TÍNH nhãn từng dòng (sha256-16 của tập
    #   [dong_sheet, nhan, lech, ghi_chu] đã sắp). Ghim CÙNG lượt, CÙNG nguồn với `phan_bo_nhan`.
    #   Phân bố một mình ⛔ giữ được lời hứa "mọi thay đổi nhãn về sau đều ĐỎ" (đổi chỗ nhãn 2 dòng
    #   cùng kỳ giữ nguyên số đếm) — vân tay danh tính mới cắn.
    "van_tay_nhan": None,
}

KHOA_TRAN = ("_vi_sao", "khong_mang_PII", "nguon", "mau_so", "dem_nhan", "nhan_theo_ky", "van_tay", "dong_thieu")
KHOA_NGUON = ("tep_dt1a", "anh_so", "ban_doc_sha256_16")
# R6 — chốt RIÊNG cho tên khoá thô (⛔ mượn `KHOA_CAM` của `tools/phan_loai_dong_thieu.py`: tệp ấy đang được
#   phiên khác sửa, và orchestrator 16/11 đòi chốt riêng). So trên tên đã bỏ dấu, thường hoá, bỏ ký tự lạ.
KHOA_CAM_RIENG = ("diengiai", "sochungtu", "soct", "email")
KHOA_MAU_SO = ("thieu", "so_dong_so", "so_dong_l1", "so_dong_ghep_dt1a", "tai_lap", "khoa_hong", "dang_khoa_hoc")
KHOA_DONG = ("dong_sheet", "ky", "nhan", "khoa_bam", "lech", "ghi_chu")
MAU_HEX16 = re.compile(r"^[0-9a-f]{16}$")
MAU_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
MAU_REF_TRONG_LOI = "Did not find value"         # `#N/A (Did not find value 'FT…' …)` nhúng mã giao dịch
MAU_KHOA_HOC = re.compile(r"^\d(?:\.\d+)?E\+\d+$", re.I)   # chỉ để ĐẾM ô Số CT dạng khoa học (chẩn đoán)
DAI_TOI_THIEU = 6                                # token ≥ 6 ký tự mới so (số dòng · số đếm ≤ 5 chữ số)

VI_SAO = ("Sinh bởi `python tools/phan_loai_ly_do.py --khoa <bản đọc> --ghi` (ISP 3.1.2 Step 5 · DT1b · "
          "BG-096) từ khoá đọc ở nguồn trên máy owner (O10). ⛔ sửa tay — `python tools/phan_loai_ly_do.py` "
          "kiểm lại tệp này. Mỗi dòng sổ thiếu của DT1a mang ĐÚNG một nhãn trong bảng đóng.")
KHONG_MANG_PII = ("Mỗi dòng đúng 6 khoá (dong_sheet · ky · nhan · khoa_bam · lech · ghi_chu); khoá ghép chỉ "
                  "ở dạng sha256 16 ký tự hex của bộ 5 trường ĐÃ chuẩn hoá. Máy chặn trước khi ghi và khi kiểm "
                  "tệp: khoá ngoài lược đồ · tên khoá ở mọi tầng chứa Diễn giải / Số chứng từ / Số CT / email (bỏ dấu) · "
                  "khoa_bam ⛔ phải 16 hex · email trong mọi chuỗi · ô `#N/A` dạng "
                  "dài của VLOOKUP (nhúng mã giao dịch); riêng lúc đo: mọi token trùng Số chứng từ ≥ 6 ký tự "
                  "(thô hoặc đã chuẩn hoá) hay số tiền ≥ 6 chữ số của đầu vào.")
# ⚠ Câu trên ⛔ được chép nguyên chuỗi mà R4 tìm — lần chạy đầu 16/11 chính câu khai đã làm R4 ĐỎ
#   (`riêng tư: ô lỗi nhúng mã giao dịch ở /khong_mang_PII`): cổng cắn cả bản khai của chính nó.


class LoiDauVao(ValueError):
    """Bản đọc khoá sai ĐỊNH DẠNG ĐÓNG. Câu lỗi chỉ mang số hàng CSV / tên cột — ⛔ giá trị ô."""


# ═════════════════════════════════════════════════════════════════════════ chuẩn hoá · băm
def _tien(raw) -> str | None:
    """PS Nợ / PS Có → chuỗi thập phân chuẩn (`'2,730,128.00'` → `'2730128'`); trống ≡ `'0'`; hỏng ⇒ None."""
    if la_o_loi(raw):
        return None
    try:
        v = parse_so(raw)
    except ValueError:
        return None
    return format(Decimal(str(0 if v is None else v)).normalize(), "f")


def _chu(raw) -> str:
    if raw is None or la_o_loi(raw):
        return ""
    return unicodedata.normalize("NFKC", str(raw)).strip().upper()


def chuan_hoa_khoa(so_ct, ps_no, ps_co, tk, tien_te) -> tuple:
    """Bộ 5 trường khoá ĐÃ chuẩn hoá, đúng thứ tự `COT_KHOA`. Trường tiền hỏng ⇒ `None` ở vị trí ấy."""
    return (canon_ref(so_ct) or "", _tien(ps_no), _tien(ps_co), _chu(tk),
            "" if la_o_loi(tien_te) else ma_tien_te(tien_te))


def bam_khoa(khoa: tuple) -> str:
    """sha256 (16 ký tự đầu) của CẢ bộ khoá đã chuẩn hoá — ⛔ băm từng trường (dò ngược được)."""
    return hashlib.sha256(json.dumps(list(khoa), ensure_ascii=False, separators=(",", ":"))
                          .encode("utf-8")).hexdigest()[:16]


def _hong(khoa: tuple) -> list[str]:
    return [COT_KHOA[i] for i, v in enumerate(khoa) if v is None]


def _van_tay(so_dong: list[int]) -> str:
    """Y cách DT1a băm tập dòng (`tools/phan_loai_dong_thieu.py` `_van_tay`) — chép 1 dòng, ⛔ import:
    tệp ấy đang được phiên khác sửa; lệch cách băm thì K1/K2 ĐỎ ngay (ồn, ⛔ im lặng)."""
    return hashlib.sha256(json.dumps(so_dong, separators=(",", ":")).encode()).hexdigest()[:16]


def _van_tay_nhan(dong: list) -> str:
    """K13 (DT1b-R1-05) — vân tay DANH TÍNH nhãn: sha256-16 của tập [dong_sheet, nhan, lech, ghi_chu]
    đã SẮP. Khoá sắp là `dong_sheet` (số nguyên, duy nhất) ⇒ ⛔ so None < str. Đổi chỗ nhãn hai dòng
    cùng kỳ giữ nguyên MỌI số đếm nhưng ĐỔI vân tay này ⇒ cổng cắn thứ phân bố ⛔ thấy."""
    bo = sorted([r.get("dong_sheet"), r.get("nhan"), r.get("lech") or [], r.get("ghi_chu")] for r in dong)
    return hashlib.sha256(json.dumps(bo, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()[:16]


# ═════════════════════════════════════════════════════════════════════════ đọc bản đọc khoá
def doc_khoa(duong: Path) -> dict:
    """CSV định dạng đóng → `{so, l1}` (`dong` → khoá đã chuẩn hoá) + tập token cấm (R5) + chẩn đoán.

    Giá trị THÔ chỉ sống trong hàm này và trong tập token cấm (bộ nhớ) — ⛔ ra tệp, ⛔ ra màn."""
    so: dict[int, tuple] = {}
    l1: dict[int, tuple] = {}
    cam_ct: set[str] = set()
    cam_tien: set[str] = set()
    khoa_hoc = {"SO": 0, "L1": 0}
    with duong.open(encoding="utf-8-sig", newline="") as f:
        r = csv.reader(f)
        tieu_de = next(r, None)
        if tieu_de is None:
            raise LoiDauVao("bản đọc rỗng — ⛔ có hàng tiêu đề")
        td = [x.strip() for x in tieu_de]
        thua = [x for x in td if x not in COT_VAO]
        vang = [x for x in COT_VAO if x not in td]
        if thua or vang or len(td) != len(set(td)):
            raise LoiDauVao(f"cột của bản đọc ⛔ đúng định dạng đóng {','.join(COT_VAO)}: "
                            f"thừa {thua} · thiếu {vang} · lặp {sorted(x for x, n in Counter(td).items() if n > 1)}")
        vt = {t: td.index(t) for t in COT_VAO}
        for so_hang, h in enumerate(r, start=2):
            if not any(x.strip() for x in h):
                continue
            if len(h) != len(td):
                raise LoiDauVao(f"hàng CSV {so_hang}: {len(h)} ô · tiêu đề {len(td)} cột")
            bang = h[vt["bang"]].strip()
            if bang not in ("SO", "L1"):
                raise LoiDauVao(f"hàng CSV {so_hang}: cột bang ⛔ phải SO hoặc L1")
            try:
                dong = int(h[vt["dong"]].strip())
            except ValueError:
                raise LoiDauVao(f"hàng CSV {so_hang}: cột dong ⛔ phải số nguyên") from None
            dich = so if bang == "SO" else l1
            if dong in dich:
                raise LoiDauVao(f"hàng CSV {so_hang}: {bang} dòng {dong} trùng — mỗi dòng một hàng")
            tho = [h[vt[c]] for c in COT_KHOA]
            khoa = chuan_hoa_khoa(*tho)
            dich[dong] = khoa
            for ct in (tho[0].strip(), khoa[0]):
                if ct and len(ct) >= DAI_TOI_THIEU:
                    cam_ct.add(ct)
            for t in khoa[1:3]:
                if t and len(t.replace("-", "").replace(".", "")) >= DAI_TOI_THIEU:
                    cam_tien.add(t)
            if MAU_KHOA_HOC.match(tho[0].strip()):
                khoa_hoc[bang] += 1
    sha = hashlib.sha256(duong.read_bytes()).hexdigest()[:16]
    return {"so": so, "l1": l1, "cam_ct": cam_ct, "cam_tien": cam_tien, "dang_khoa_hoc": khoa_hoc, "sha": sha}


# ═════════════════════════════════════════════════════════════════════════ phân loại
def phan_loai(so: dict[int, tuple], l1: dict[int, tuple], thieu: list[int]) -> tuple[dict[int, dict], int]:
    """Nhãn cho từng dòng thiếu + TÁI LẬP. Làm theo NHÓM KHOÁ — ⛔ theo vị trí hàng, ⛔ theo thứ tự tệp."""
    tap = set(thieu)
    n_l1 = Counter(k for k in l1.values() if not _hong(k))
    n_so = Counter(k for k in so.values() if not _hong(k))
    o = Counter(k for d, k in so.items() if d not in tap and not _hong(k))       # dòng sổ ĐÃ ghép
    u: dict[tuple, list[int]] = defaultdict(list)                                  # dòng sổ thiếu
    for d in sorted(thieu):
        if not _hong(so[d]):
            u[so[d]].append(d)
    # dòng L1 CHƯA AI GHÉP: nhóm khoá có nhiều dòng L1 hơn dòng sổ (mọi dòng sổ, kể cả dòng thiếu)
    mo_coi = [k for k, n in n_l1.items() if n > n_so.get(k, 0)]
    theo_ct: dict[str, list[tuple]] = defaultdict(list)
    theo_bon: dict[tuple, list[tuple]] = defaultdict(list)
    for k in mo_coi:
        if k[0]:
            theo_ct[k[0]].append(k)
        theo_bon[k[1:]].append(k)

    ra: dict[int, dict] = {}
    for d in thieu:
        k = so[d]
        o_dong = {"nhan": None, "khoa_bam": bam_khoa(k), "lech": [], "ghi_chu": None}
        hong = _hong(k)
        if hong:
            o_dong.update(nhan="KHAC", ghi_chu="KHOA_HONG:" + ",".join(hong))
        elif n_l1[k] >= 1:
            cho = min(len(u[k]), max(0, n_l1[k] - o[k]))
            if u[k].index(d) < cho:
                o_dong.update(nhan="KHAC", ghi_chu=GHI_CHU_KHOP)
            else:
                o_dong["nhan"] = "TRUNG_SEQ"
        else:
            ung = set(theo_ct.get(k[0], []) if k[0] else []) | set(theo_bon.get(k[1:], []))
            if ung:
                gan = min(ung, key=lambda c: (sum(a != b for a, b in zip(c, k)), c))
                o_dong.update(nhan="KHOA_LECH", lech=[COT_KHOA[i] for i in range(5) if gan[i] != k[i]])
            else:
                o_dong["nhan"] = "KHONG_CO_SAO_KE"
        ra[d] = o_dong
    tai_lap = sum(min(n, n_l1.get(k, 0)) for k, n in o.items())
    return ra, tai_lap


def _nap(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def do(duong: Path) -> tuple[dict, list[str]]:
    """ĐO trên một bản đọc khoá → (nội dung tệp nhãn, danh sách lệch). Đầu vào sai định dạng ⇒ `LoiDauVao`."""
    dt1a = _nap(DT1A)
    anh = _nap(ANH_SO)
    i = anh["cot"].index("dong_sheet")
    tap_anh = {h[i] for h in anh["dong"]}
    vao = doc_khoa(duong)
    so, l1 = vao["so"], vao["l1"]
    thieu = sorted(x["dong_sheet"] for x in dt1a["dong_thieu"])
    ky = {x["dong_sheet"]: x["ky"] for x in dt1a["dong_thieu"]}
    van_tay = {"thieu": _van_tay(thieu), "nguoc": _van_tay(sorted(x["dong_canon"] for x in dt1a["dong_nguoc"]))}
    mau_so = {"thieu": len(thieu), "so_dong_so": len(so), "so_dong_l1": len(l1),
              "so_dong_ghep_dt1a": dt1a["mau_so"]["so_dong_ghep"]}
    rong = {k: v for k, v in mau_so.items() if not v}
    if rong:                                     # Đ3 — mẫu số rỗng là KẾT QUẢ, ⛔ nền cho tỷ lệ
        return {"mau_so": mau_so}, [f"mẫu số = 0 — ⛔ đo được tỷ lệ nào (Đ3): {rong}"]
    if set(so) != tap_anh:                       # K11 — cùng hệ đánh số `dong_sheet` của ảnh 26/08
        vang, thua = sorted(tap_anh - set(so)), sorted(set(so) - tap_anh)
        return {"mau_so": mau_so}, [
            f"tập dong_sheet phía SO ≠ {len(tap_anh)} dòng của ảnh sổ 26/08: thiếu {len(vang)} · thừa {len(thua)} "
            f"(vd. thiếu {vang[:5]} · thừa {thua[:5]}) — xuất thiếu dòng, hay đánh số ⛔ cùng hệ hàng Excel?"]
    ngoai = sorted(set(thieu) - set(so))
    if ngoai:
        return {"mau_so": mau_so}, [f"{len(ngoai)} dòng thiếu của DT1a ⛔ có phía SO (vd. {ngoai[:5]})"]

    nhan, tai_lap = phan_loai(so, l1, thieu)
    dong = [{"dong_sheet": d, "ky": ky[d], **nhan[d]} for d in thieu]
    theo_ky: dict[str, dict[str, int]] = {}
    for r in dong:
        theo_ky.setdefault(r["ky"], {n: 0 for n in NHAN})[r["nhan"]] += 1
    mau_so.update(tai_lap=tai_lap,
                  khoa_hong={"SO": sum(1 for k in so.values() if _hong(k)),
                             "L1": sum(1 for k in l1.values() if _hong(k))},
                  dang_khoa_hoc=vao["dang_khoa_hoc"])
    kq = {
        "_vi_sao": VI_SAO,
        "khong_mang_PII": KHONG_MANG_PII,
        "nguon": {"tep_dt1a": NGUON_TEP_DT1A,
                  "anh_so": NGUON_ANH_SO,
                  "ban_doc_sha256_16": vao["sha"]},
        "mau_so": mau_so,
        "dem_nhan": {n: sum(1 for r in dong if r["nhan"] == n) for n in NHAN},
        "nhan_theo_ky": {k: theo_ky[k] for k in sorted(theo_ky)},
        "van_tay": van_tay,                      # HỢP ĐỒNG H2: khoá gốc, khuôn của DT1a
        "dong_thieu": dong,                      # HỢP ĐỒNG H2: `dong_sheet` int + `nhan`
    }
    loi = kiem(kq, dt1a)
    loi.extend(quet_token(kq, vao["cam_ct"], vao["cam_tien"]))   # R5 — chặn TRƯỚC khi ghi
    return kq, loi


# ═════════════════════════════════════════════════════════════════════════ kiểm (dùng chung đo ↔ cổng)
def _moi_chuoi(x, duong: str = ""):
    """Mọi chuỗi trong `x` — cả KHOÁ dict (khoá `nhan_theo_ky` là kỳ, đọc từ DT1a) lẫn giá trị."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield f"{duong}/{k}", str(k)
            yield from _moi_chuoi(v, f"{duong}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _moi_chuoi(v, f"{duong}[{i}]")
    elif isinstance(x, (str, int)) and not isinstance(x, bool):
        yield duong, str(x)


def _moi_khoa(x, duong: str = ""):
    """Mọi tên khoá dict ở MỌI tầng (R6)."""
    if isinstance(x, dict):
        for k, v in x.items():
            yield f"{duong}/{k}", str(k)
            yield from _moi_khoa(v, f"{duong}/{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from _moi_khoa(v, f"{duong}[{i}]")


def _bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def _luoc_do(kq) -> tuple[list[str], bool]:
    """R1 · R2 — (lệch, còn đọc tiếp được không)."""
    if not isinstance(kq, dict):
        return ["tệp nhãn ⛔ phải một đối tượng JSON"], False
    loi: list[str] = []

    def tap(ten: str, co, mong) -> None:
        if set(co) != set(mong):
            loi.append(f"riêng tư: khoá ngoài lược đồ ở {ten}: thừa {sorted(set(co) - set(mong))} · "
                       f"thiếu {sorted(set(mong) - set(co))}")

    tap("gốc", kq, KHOA_TRAN)
    if set(KHOA_TRAN) - set(kq) or not all(isinstance(kq[k], dict) for k in ("nguon", "mau_so", "dem_nhan",
                                                                               "nhan_theo_ky", "van_tay")) \
            or not isinstance(kq["dong_thieu"], list) or not all(isinstance(r, dict) for r in kq["dong_thieu"]):
        return loi or ["tệp nhãn sai kiểu ở khoá gốc"], False
    tap("nguon", kq["nguon"], KHOA_NGUON)
    tap("mau_so", kq["mau_so"], KHOA_MAU_SO)
    for r in kq["dong_thieu"]:
        tap(f"dòng {r.get('dong_sheet')}", r, KHOA_DONG)
        if not (isinstance(r.get("khoa_bam"), str) and MAU_HEX16.match(r["khoa_bam"])):
            loi.append(f"riêng tư: dòng {r.get('dong_sheet')}: khoa_bam ⛔ phải 16 ký tự hex (sha256)")
    return loi, True


def kiem(kq: dict, dt1a: dict) -> list[str]:
    """K1–K10 + R1–R4 trên một tệp nhãn (vừa đo, hoặc đọc từ đĩa). Trả danh sách lệch MONG."""
    loi: list[str] = []

    def so(ten: str, co, mong) -> None:
        if co != mong:
            loi.append(f"{ten}: đo {co!r} · mong {mong!r}")

    thieu = sorted(x["dong_sheet"] for x in dt1a["dong_thieu"])
    nguoc = sorted(x["dong_canon"] for x in dt1a["dong_nguoc"])
    so(f"vân tay tập thiếu của DT1a (sha256 của {len(thieu)} dong_sheet đã sắp)", _van_tay(thieu),     # K1
       MONG["van_tay"]["thieu"])
    so(f"vân tay tập ngược của DT1a (sha256 của {len(nguoc)} dong_canon đã sắp)", _van_tay(nguoc),     # K2
       MONG["van_tay"]["nguoc"])
    lo, tiep = _luoc_do(kq)                                                                             # R1 · R2
    loi.extend(lo)
    for duong, k in _moi_khoa(kq):                                                                      # R6
        if any(c in _bo_dau(k) for c in KHOA_CAM_RIENG):
            loi.append(f"riêng tư: khoá cấm {k[:40]!r} ở {duong}")
    for duong, s in _moi_chuoi(kq):                                                                     # R3 · R4
        if MAU_EMAIL.search(s):
            loi.append(f"riêng tư: email ở {duong}")
        if MAU_REF_TRONG_LOI in s:
            loi.append(f"riêng tư: ô lỗi nhúng mã giao dịch ở {duong}")
    if not tiep:
        return loi

    # R7 (DT1b-R1-04) — "lược đồ ĐÓNG" phải đóng cả GIÁ TRỊ, ⛔ chỉ TÊN khoá: mọi LÁ tự do của tệp ra
    #   = hằng · ∈ tập đóng · khớp mẫu. Câu lỗi nêu TÊN LÁ, ⛔ in lại giá trị vừa bắt (⛔ chuyển PII ra màn
    #   owner được dặn gửi về). `ban_doc_sha256_16` chỉ canh được MẪU (hex16 — ⛔ tái tính được ở chế độ cổng):
    #   Số CT 16 chữ số thập phân vẫn khớp hex16 — giới hạn đã khai (BG vòng sửa R1).
    if kq.get("_vi_sao") != VI_SAO:
        loi.append("riêng tư: /_vi_sao ⛔ đúng hằng khai")
    if kq.get("khong_mang_PII") != KHONG_MANG_PII:
        loi.append("riêng tư: /khong_mang_PII ⛔ đúng hằng khai")
    ng = kq["nguon"]
    if ng.get("tep_dt1a") != NGUON_TEP_DT1A:
        loi.append("riêng tư: /nguon/tep_dt1a ⛔ đúng đường dẫn hằng")
    if ng.get("anh_so") != NGUON_ANH_SO:
        loi.append("riêng tư: /nguon/anh_so ⛔ đúng đường dẫn hằng")
    if not (isinstance(ng.get("ban_doc_sha256_16"), str) and MAU_HEX16.match(ng["ban_doc_sha256_16"])):
        loi.append("riêng tư: /nguon/ban_doc_sha256_16 ⛔ phải 16 ký tự hex (sha256)")
    ms0 = kq["mau_so"]
    for ten in ("khoa_hong", "dang_khoa_hoc"):
        d = ms0.get(ten)
        if not (isinstance(d, dict) and set(d) == {"SO", "L1"}
                and all(type(v) is int and v >= 0 for v in d.values())):
            loi.append(f"riêng tư: /mau_so/{ten} ⛔ đúng {{SO, L1}} số nguyên ≥ 0")
    for ten in ("thieu", "so_dong_so", "so_dong_l1", "so_dong_ghep_dt1a", "tai_lap"):
        if ten in ms0 and type(ms0[ten]) is not int:
            loi.append(f"riêng tư: /mau_so/{ten} ⛔ phải số nguyên")

    so("vân tay ghi trong tệp nhãn (van_tay)", kq["van_tay"], MONG["van_tay"])                       # K3

    dong = kq["dong_thieu"]                                                                             # K4
    lap = Counter(r.get("dong_sheet") for r in dong)
    for d, n in lap.items():
        if n >= 2:
            loi.append(f"dòng {d} mang {n} nhãn (dòng lặp {n} lần) — mỗi dòng ĐÚNG một")
    hop_le = []
    for r in dong:
        d, n = r.get("dong_sheet"), r.get("nhan")
        if type(d) is not int:                   # K4b — hợp đồng H2: số nguyên, ⛔ `True` (bool là int của Python)
            loi.append(f"dòng {str(d)[:20]!r}: dong_sheet ⛔ phải số nguyên (kiểu {type(d).__name__})")
            continue
        if isinstance(n, list):
            loi.append(f"dòng {d} mang {len(n)} nhãn {n} — mỗi dòng ĐÚNG một")
        elif n is None:
            loi.append(f"dòng {d} mang 0 nhãn (null)")
        elif n not in NHAN:
            loi.append(f"dòng {d}: nhãn lạ {str(n)[:40]!r} — bảng đóng {NHAN}")
        else:
            hop_le.append(r)
    for d in sorted(set(thieu) - set(lap)):
        loi.append(f"dòng {d} mang 0 nhãn (vắng trong tệp nhãn)")
    for d in sorted(set(lap) - set(thieu), key=str):
        loi.append(f"dòng {d} ngoài tập {MONG['thieu']} dòng thiếu của DT1a")

    dem_lai = {n: sum(1 for r in hop_le if r["nhan"] == n) for n in NHAN}                              # K5
    so("dem_nhan ↔ đếm lại từ dòng (hai nguồn)", kq["dem_nhan"], dem_lai)
    so("Σ dem_nhan (dòng sổ thiếu có nhãn)",
       sum(v for v in kq["dem_nhan"].values() if isinstance(v, int)), MONG["thieu"])

    for r in hop_le:                                                                                    # K6
        d, n, lech, gc = r["dong_sheet"], r["nhan"], r.get("lech"), r.get("ghi_chu")
        if n == "KHAC":
            if not (isinstance(gc, str) and (gc == GHI_CHU_KHOP or MAU_GHI_CHU_HONG.match(gc))):
                loi.append(f"dòng {d}: KHAC ⛔ có ghi chú hợp lệ ({str(gc)[:40]!r}) — tập đóng: "
                           f"{GHI_CHU_KHOP} · KHOA_HONG:<trường tiền>")
            if lech != []:
                loi.append(f"dòng {d}: KHAC ⛔ mang lech")
        elif n == "KHOA_LECH":
            if not (isinstance(lech, list) and lech and len(set(lech)) == len(lech) and set(lech) <= set(COT_KHOA)):
                loi.append(f"dòng {d}: KHOA_LECH ⛔ nêu trường lệch hợp lệ ({str(lech)[:60]}) — ⊂ {COT_KHOA}")
            if gc is not None:
                loi.append(f"dòng {d}: KHOA_LECH ⛔ mang ghi_chu")
        elif lech != [] or gc is not None:
            loi.append(f"dòng {d}: {n} ⛔ mang lech / ghi_chu")

    ky = {x["dong_sheet"]: x["ky"] for x in dt1a["dong_thieu"]}                                        # K7
    for r in dong:
        d = r.get("dong_sheet")
        if d in ky and r.get("ky") != ky[d]:
            loi.append(f"dòng {d}: kỳ {str(r.get('ky'))[:20]!r} ≠ kỳ DT1a {ky[d]!r}")
    theo_ky: dict = {}
    for r in hop_le:
        theo_ky.setdefault(r.get("ky"), {n: 0 for n in NHAN})[r["nhan"]] += 1
    so("nhan_theo_ky ↔ đếm lại từ dòng (hai nguồn)", kq["nhan_theo_ky"], theo_ky)

    ms = kq["mau_so"]                                                                                   # K8 · K9 · K10
    rong = {k: ms.get(k) for k in ("thieu", "so_dong_so", "so_dong_l1", "so_dong_ghep_dt1a")
            if not (isinstance(ms.get(k), int) and ms[k] > 0)}
    if rong:
        loi.append(f"mẫu số = 0 — ⛔ đo được tỷ lệ nào (Đ3): {rong}")
    so("mẫu số khai: dòng sổ thiếu", ms.get("thieu"), MONG["thieu"])
    so("mẫu số khai: dòng sổ của bản đọc", ms.get("so_dong_so"), MONG["so_dong_so"])
    so("mẫu số khai: dòng ghép DT1a", ms.get("so_dong_ghep_dt1a"), MONG["so_dong_ghep"])
    so(f"tái lập khoá+seq (dòng ghép DT1a tìm lại được dòng L1 cùng khoá, trên {MONG['so_dong_ghep']} dòng ghép)",
       ms.get("tai_lap"), MONG["so_dong_ghep"])
    return loi


def quet_token(kq: dict, cam_ct: set[str], cam_tien: set[str]) -> list[str]:
    """R5 (lúc đo) — mọi chuỗi / số trong tệp ra, tách token, so tập Số CT + tiền của CHÍNH bản đọc."""
    loi: list[str] = []
    for duong, s in _moi_chuoi(kq):
        token = {s.strip()} | set(re.findall(r"[0-9A-Za-z.+\-]+", s))
        if token & cam_ct:
            loi.append(f"riêng tư: Số chứng từ của bản đọc lọt vào tệp ra ở {duong}")
        if token & cam_tien:
            loi.append(f"riêng tư: số tiền của bản đọc lọt vào tệp ra ở {duong}")
    return loi


# ═════════════════════════════════════════════════════════════════════════ in · phán · ghi
def _so(n) -> str:
    """Số kiểu Việt: 9967 → `9.967`."""
    return f"{n:,}".replace(",", ".") if isinstance(n, int) else str(n)


def _ty_le(tu: int, mau: int) -> str:
    return f"{tu * 100 / mau:.2f}".replace(".", ",") + " %"


def in_bao_cao(kq: dict, nguon: str) -> None:
    ms = kq["mau_so"]
    print(f"PHÂN LOẠI LÝ DO — HD1 · dòng sổ chưa ghép 1-1 (DT1b) · {nguon}")
    # Đ3: MẪU SỐ in TRƯỚC mọi tỷ lệ, mỗi số mang nhãn NÓ ĐẾM GÌ (Đ4)
    print(f"① MẪU SỐ: bản đọc phía SO {_so(ms.get('so_dong_so'))} dòng sổ · phía L1 {_so(ms.get('so_dong_l1'))} "
          f"dòng L1 · tập DT1a {_so(ms.get('thieu'))} dòng sổ thiếu · {_so(ms.get('so_dong_ghep_dt1a'))} dòng ghép (DT1a)")
    if "dong_thieu" not in kq:
        return
    mau = ms.get("so_dong_ghep_dt1a")
    ty = _ty_le(ms["tai_lap"], mau) if isinstance(mau, int) and mau > 0 and isinstance(ms.get("tai_lap"), int) else "—"
    kh, dk = ms.get("khoa_hong", {}), ms.get("dang_khoa_hoc", {})
    print(f"② tái lập khoá+seq: {_so(ms.get('tai_lap'))} / {_so(mau)} dòng ghép DT1a = {ty} · khoá hỏng: "
          f"sổ {_so(kh.get('SO'))} · L1 {_so(kh.get('L1'))} dòng · Số CT dạng khoa học: sổ {_so(dk.get('SO'))} · "
          f"L1 {_so(dk.get('L1'))} dòng")
    dem = kq["dem_nhan"]
    print(f"③ nhãn của {_so(ms.get('thieu'))} dòng sổ thiếu (đếm DÒNG): " + " · ".join(f"{n} {dem.get(n)}" for n in NHAN))
    gc = Counter(r.get("ghi_chu") for r in kq["dong_thieu"] if r.get("nhan") == "KHAC")
    lc = Counter(",".join(r.get("lech") or []) for r in kq["dong_thieu"] if r.get("nhan") == "KHOA_LECH")
    print("   KHAC theo ghi chú: " + (" · ".join(f"{k} {n}" for k, n in sorted(gc.items(), key=str)) or "—")
          + "  ‖  KHOA_LECH theo trường lệch: " + (" · ".join(f"{k} {n}" for k, n in sorted(lc.items())) or "—"))
    print("④ nhãn × kỳ (đếm DÒNG; chỉ kỳ có dòng thiếu):")
    print(f"   {'kỳ':8s} {'Σ':>4s} " + " ".join(f"{n:>16s}" for n in NHAN))
    for k, x in kq["nhan_theo_ky"].items():
        print(f"   {str(k):8s} {sum(x.values()):4d} " + " ".join(f"{x.get(n, 0):16d}" for n in NHAN))
    print(f"   vân tay DT1a: thiếu {kq['van_tay'].get('thieu')} · ngược {kq['van_tay'].get('nguoc')}")


def phan_xu(kq: dict, loi: list[str]) -> int:
    """Phán cuối: lệch ⇒ 1 · MONG phân bố / vân tay nhãn chưa ghim ⇒ 4 · khớp ⇒ 0 (M · K13)."""
    mong = MONG["phan_bo_nhan"]
    mong_vt = MONG["van_tay_nhan"]
    if mong is not None and isinstance(kq.get("dem_nhan"), dict) and kq["dem_nhan"] != mong:
        loi.append(f"phân bố nhãn của {MONG['thieu']} dòng sổ thiếu: đo {kq['dem_nhan']} · mong {mong}")
    if mong_vt is not None:                       # K13 — DANH TÍNH nhãn, ⛔ chỉ phân bố (DT1b-R1-05)
        try:
            vt = _van_tay_nhan(kq["dong_thieu"])
        except Exception:
            vt = None                             # ⛔ tính được vân tay cũng là ĐỎ (Đ5), ⛔ "không thấy lệch"
        if vt != mong_vt:
            loi.append(f"vân tay danh tính nhãn (K13): đo {vt!r} · mong {mong_vt!r} — "
                       f"tổng có thể y nguyên mà danh tính nhãn từng dòng đã khác")
    if loi:
        print(f"⛔ PHÂN LOẠI LÝ DO ĐỎ — {len(loi)} chỗ khác MONG (⛔ ghi JSON):", file=sys.stderr)
        for x in loi:
            print("  " + x, file=sys.stderr)
        return DO
    if mong is None or mong_vt is None:
        thieu_ghim = [t for t, v in (("phân bố nhãn", mong), ("vân tay danh tính nhãn", mong_vt)) if v is None]
        print(f"KẾT: ĐO ĐƯỢC — ⛔ CHƯA GHIM MONG {' · '.join(thieu_ghim)} (mã {CHUA_GHIM}, ⛔ phải ĐẠT): mọi bất "
              f"biến cấu trúc đạt · {_so(MONG['thieu'])} dòng mỗi dòng đúng một nhãn — gửi tệp nhãn + bảng ③④ "
              f"về orchestrator để ghim")
        return CHUA_GHIM
    print(f"KẾT: ĐẠT — mọi phép so khớp MONG · {_so(MONG['thieu'])} dòng sổ thiếu, mỗi dòng đúng một nhãn")
    return DAT


def _ghi(kq: dict) -> None:
    """Tệp tạm + kiểm đọc lại + `os.replace` — ⛔ `write_text` thẳng lên đích (luật `DT1a-R1-07`).

    Phép "kiểm đọc lại" (so `json.loads(tam)` với `kq`) là PHÒNG THỦ CHỒNG (DT1b-R1-03 · đột biến D27 bỏ
    nó vẫn SỐNG): `json.dumps`→`json.loads` khứ hồi với dữ liệu thuần đã đạt lược đồ thì luôn khớp. Giữ để
    bắt hỏng đĩa / ghi dở lúc thay tệp — ⛔ chứng minh riêng được bằng bài, khai rõ ở đây."""
    tam = RA.with_name(RA.name + ".tam")
    tam.write_text(json.dumps(kq, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if json.loads(tam.read_text(encoding="utf-8")) != kq:
        raise RuntimeError(f"đọc lại {tam.name} ⛔ khớp nội dung vừa ghi")
    os.replace(tam, RA)


def _mot_dong(e: Exception) -> str:
    return f"LOI {type(e).__name__}: " + " ".join(str(e).split())        # S0-R1-04 — ⛔ traceback


def _trong_repo_khong_ignore(duong: Path) -> bool:
    """R8 (DT1b-R1-06) — True nếu `duong` nằm TRONG repo mà ⛔ bị `.gitignore` (⇒ giá trị THÔ có nguy cơ
    lên git). `git check-ignore -q` trả 0 khi BỊ bỏ qua (an toàn), ≠ 0 khi ⛔ bỏ qua (nguy). ⛔ trong repo
    hoặc ⛔ chạy được git ⇒ chốt này ⛔ lo (nhánh khác xử)."""
    try:
        duong.resolve().relative_to(GOC)
    except (ValueError, OSError):
        return False
    try:
        r = subprocess.run(["git", "-C", str(GOC), "check-ignore", "-q", str(duong.resolve())])
    except OSError:
        return False
    return r.returncode != 0


def _che_do_do(duong: Path, ghi: bool) -> int:
    if duong.exists() and not duong.is_file():   # DT1b-R1-11 — thư mục / ⛔ tệp thường là SAI CÁCH GỌI (2), ⛔ "chưa đo"
        print(f"⛔ TỪ CHỐI: {duong.resolve()} CÓ nhưng ⛔ phải TỆP thường (bản đọc khoá CSV)", file=sys.stderr)
        return SAI_GOI
    if not duong.is_file():                      # DT1b-R1-11 — nói thiếu gì, Ở ĐÂU (đường tuyệt đối), ⛔ đoán vì sao
        print(f"⛔ CHƯA ĐO ĐƯỢC — ⛔ thấy bản đọc khoá tại {duong.resolve()}: khoá THẬT chỉ có trên máy owner "
              f"(O10 · B-DATA-2) — xem BG-096 §Hướng dẫn owner chạy lượt thật", file=sys.stderr)
        return CHUA_DO_DUOC
    if _trong_repo_khong_ignore(duong):          # DT1b-R1-06 — chặn ở MÁY, ⛔ ở lời dặn BG-096:155
        print(f"⛔ TỪ CHỐI: bản đọc khoá mang giá trị THÔ nằm trong repo mà ⛔ bị .gitignore "
              f"({duong.resolve()}) — chuyển vào hien_vat/ (một `git add -A` là Số CT + tiền thật lên lịch sử)",
              file=sys.stderr)
        return SAI_GOI
    try:
        kq, loi = do(duong)
    except Exception as e:                       # Đ5: ⛔ đo được / sai định dạng là ĐỎ — nguyên nhân MỘT dòng
        print(_mot_dong(e), file=sys.stderr)
        return DO
    in_bao_cao(kq, f"bản đọc khoá {duong.name}")
    ma = phan_xu(kq, loi)
    if ghi and ma in (DAT, CHUA_GHIM):
        _ghi(kq)
        print(f"✅ đã ghi {RA.name} (mã {ma})")
    return ma


def _che_do_cong(tep: Path) -> int:
    if tep.exists() and not tep.is_file():       # DT1b-R1-11 — thư mục / ⛔ tệp thường là SAI CÁCH GỌI (2)
        print(f"⛔ TỪ CHỐI: {tep.resolve()} CÓ nhưng ⛔ phải TỆP thường (tệp nhãn JSON)", file=sys.stderr)
        return SAI_GOI
    if not tep.is_file():
        print(f"⛔ CHƯA ĐO ĐƯỢC — ⛔ có tệp nhãn {tep.name!r}: lượt gán nhãn THẬT chưa chạy (khoá thật chỉ có trên "
              f"máy owner — O10 · B-DATA-2)", file=sys.stderr)
        return CHUA_DO_DUOC
    try:
        dt1a, kq = _nap(DT1A), _nap(tep)
        loi = kiem(kq, dt1a)
    except Exception as e:
        print(_mot_dong(e), file=sys.stderr)
        return DO
    try:
        in_bao_cao(kq, f"tệp nhãn {tep.name}")
    except Exception as e:                       # bảng chỉ là trình bày — phán quyết nằm ở `loi`
        print(f"(⛔ in được bảng: {_mot_dong(e)})")
    return phan_xu(kq, loi)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="HD1 · gán LÝ DO cho dòng sổ chưa ghép 1-1 (DT1b).")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--khoa", type=Path, default=None, help="ĐO trên bản đọc khoá (CSV định dạng đóng — xem docstring)")
    g.add_argument("--tep", type=Path, default=None, help="CỔNG: kiểm tệp nhãn này (mặc định tệp của repo)")
    ap.add_argument("--ghi", action="store_true", help="ghi tệp nhãn của repo — chỉ cùng --khoa, chỉ khi ⛔ ĐỎ")
    a = ap.parse_args(argv)
    if a.ghi and a.khoa is None:
        print("⛔ TỪ CHỐI: --ghi chỉ đi cùng --khoa (tệp nhãn chỉ sinh từ một lượt ĐO trên bản đọc khoá)",
              file=sys.stderr)
        return SAI_GOI
    if a.khoa is not None:
        return _che_do_do(a.khoa, a.ghi)
    return _che_do_cong(a.tep if a.tep is not None else RA)


if __name__ == "__main__":
    sys.exit(main())
