# -*- coding: utf-8 -*-
"""VOI SỐ LƯỢNG DỮ LIỆU — ma trận THÁNG × LOẠI DỮ LIỆU, mỗi ô bốn số: CÓ · CHẠY · MAPPING · SỬA.

⭐ Owner 13/11 (AP Voi FLS v2): *"Cột là tháng, dòng là các loại dữ liệu. Mỗi ô cần có dữ liệu
   đối chiếu → Voi số lượng dữ liệu. Số có, số chạy, mapping và số đã sửa sai."*

⛔⛔ Công cụ này CHỈ đọc ẢNH ĐÓNG BĂNG đã có trong repo (`tests/fixture/`), và chạy CHÍNH MÃ FLS lên
   ảnh ấy (`pm_join.xep_ca_lat`, `final_rule.tinh_final`, `tu_soi.soi_mot_dong`). Nó ⛔ đọc kho:
   kho `fls-pg-1` ⛔ chạy trong phiên dựng AP (cổng 5433 từ chối). Số của kho (fls_itl · fls_adjustment
   theo tháng) là việc của agent ở máy có kho — AP ghi rõ ô nào đo trên ảnh, ô nào ⛔ đo.

Bốn số — mỗi số nói NÓ ĐẾM GÌ (Đ4), đơn vị là DÒNG trừ khi ghi "ô":
  CÓ      = dòng sổ AS-IS `ITL Ledge` của kỳ (ảnh `[Master] ITL_Ledge_raw.xlsx`, đóng băng 26/08).
  CHẠY    = dòng FLS dựng lại được từ `Transaction Mapping L1` (đọc live 26/08) VÀ ghép 1-1 được với
            dòng sổ theo khoá (Số CT, PS Nợ, PS Có, TK, tiền tệ) — `classifying_vs_canon.json`.
  MAPPING = hai số, ⛔ gộp: NOW = dòng mà VLOOKUP của Gsheet trả được mã HD (Classifying khối 1 có giá
            trị, ⛔ `#N/A`, ⛔ "Need to manual input"); FLS = dòng bank thuộc nhóm ghép được hình A · B · C
            của `pm_join` (Ref No + Σ tiền trong dung sai).
  SỬA     = Ô (⛔ dòng) kế toán phải điền ở vùng chỉnh tay R–AT, 7 khối: máy KHÔNG trả lời (Classifying
            rỗng hoặc "Need to manual input") mà Final có giá trị. Tách: GÕ = giá trị thật người gõ ·
            MĐ = nhận mặc định cứng của khối (`MAC_DINH_THEO_KHOI`). Thêm hai số để soát: TRỐNG = máy không
            trả lời và Final vẫn rỗng · ĐÈ = Final ≠ Classifying dù máy CÓ trả lời (trái công thức
            `Final = f(S, U)` — lỗi bản xuất, test_parity_ca_so ghim 63 ô lệch kiểu này trên cả sổ).
  ⚠ Đã thử đếm SỬA theo DÒNG ("≥1 khối người điền"): ra 9.964/9.967 — vô nghĩa, vì khối 4–7 (kỳ DV ·
            đối tác · hoá đơn) gần như dòng nào máy cũng không trả lời. Nên đếm ô và tách theo khối.

Cổng (Đ5 — khai `mong`, NO khi khác, cả hai chiều): tổng dòng · số ghép · hình ghép · parity phải
   bằng đúng số đã ghim trong bài test của chính các ảnh; lệch ⇒ exit 1, ⛔ ghi JSON.

HD1 THEO KỲ — khối `dat_hd1` (ISP 3.1.2 · Step 4 · H2 · `WO-090` · AP v3.1.2 §5.3.1 HD1 ★: *"Lệch = 0,
   hoặc mỗi lệch có tên lý do và owner ký"*):
  Một kỳ ĐẠT ⇔ [dòng] (dòng 1-1 100 % — `chạy = có` — HOẶC mọi dòng thiếu của kỳ có nhãn lý do ĐÃ KÝ)
              ∧ [ô]   (mẫu số ô trên MỌI dòng sổ của kỳ > 0 (Đ3) ∧ (ô Final = f(Classifying, MID) khớp
                       trên MỌI dòng sổ của kỳ HOẶC mọi dòng tự-soi loại của kỳ có nhãn ĐÃ KÝ)).
  ⭐⛔ VÌ SAO vế [ô] đọc MỌI dòng (vòng sửa sau R1 · `KQ-092` · `H2-R1-01` = ⓐ, errata ⑩ của bản vá ISP).
     Bản đầu tính vế ô bằng `o_parity` — mà `o_parity` BỎ các dòng `soi_mot_dong` loại, và `soi_mot_dong`
     loại ĐÚNG mọi dòng có một ô `Final ≠ f(Classifying, MID)` ⇒ `o_parity_khop == o_parity` THEO CẤU
     TRÚC: vế ô chỉ đỏ được khi `0/0`, tức nó lọc bỏ đúng thứ nó phải bắt. Đo (R1 độc lập + 16/11 lại):
     trên MỌI dòng, ô khớp 69.706/69.769 — 63 ô lệch, cả 63 ở 37 dòng tự-soi loại của 2026-07 (tập dòng
     loại = tập dòng có ô lệch, 37 = 37; `tests/ledger/test_parity_ca_so.py` ghim 63 = 60 + 3). Ký giả 23
     dòng thiếu 2026-07 làm kỳ ấy "đạt" trong khi 63 ô FLS ≠ Final sổ ⛔ tên lý do, ⛔ ai ký. Nay:
       · `o_100` (giữ tên — CG1 đọc) = vế [ô] ở trên, ⛔ còn là "ô 100 % trên dòng tự nhất quán".
       · vế "mọi dòng loại đã ký" đi KÈM "ô của các dòng còn lại khớp hết" (`o_parity_khop = o_parity`):
         đúng sẵn theo cấu trúc `soi_mot_dong` (ô lệch ⇒ dòng bị loại), nhưng chặn sự thật RỖNG — kỳ ⛔
         có dòng loại nào thì "mọi dòng loại đã ký" đúng suông (0/0) và ⛔ được miễn ô lệch nào.
       · ô chỉ đếm khi ⛔ ô nào trong ba (Cls · MID · Final) là mã lỗi Sheets — CÙNG luật với `o_parity`.
  ⛔ gồm chế độ tự sinh: nó chỉ đo được 2026-03 (một ảnh Manual input) — theo kỳ là việc của `H15`
     (Step 43). Vì thế số ở đây (5/23 khi sổ rỗng) ≠ "tháng đạt HD1" của Figure 5.3.3 (0/23, đòi CẢ
     tự sinh) — hai phép, hai nhãn (Đ4).
  ⛔ gồm CHIỀU NGƯỢC (`H2-R1-05`): phán theo kỳ chỉ đi một chiều — dòng SỔ → dòng FLS. 147 dòng FLS ⛔ có
     dòng sổ (DT1a `dong_nguoc`) ⛔ vào phán kỳ nào: ảnh `pm_join.json` ⛔ có ngày (khoá `dong · ref_tho ·
     cur · tien`) ⇒ ⛔ gán được kỳ. Số ấy in ở `dat_hd1.ngoai_phan` + dòng `①` — "5/23 kỳ đạt" ⛔ có nghĩa
     "FLS = sổ ở 5 kỳ". BA chốt chiều ngược khi DT2 (Step 8) đóng băng được ngày.
  · NHÃN lý do: tệp `docs/ITL/_tools/phan_loai_ly_do.json` của DT1b (Step 5, làm song song) — H2 chỉ ĐỌC.
    Hợp đồng đọc = khuôn của chính `phan_loai_dong_thieu.json` (DT1a): `{"van_tay": {"thieu", "nguoc"},
    "dong_thieu": [{"dong_sheet": int, "nhan": str | null}, …]}` (khoá thừa bỏ qua). Hai vân tay phải
    BẰNG vân tay tập dòng H2 tính lại từ ảnh (cùng công thức DT1a) — ⛔ thì đó là nhãn của một tập dòng
    KHÁC ⇒ ĐỎ. Tệp VẮNG ⇒ mọi dòng thiếu = "chưa có nhãn" (đỏ) — ⛔ lỗi: DT1b chưa về.
    · tập `dong_sheet` HỢP LỆ = dòng thiếu ∪ dòng tự-soi loại (`H2-R1-01` ⓐ — nhãn cho 37 dòng loại đi CÙNG
      danh sách `dong_thieu`, cùng khuôn; tập 37 dòng ấy CÔNG BỐ ở `dat_hd1.dong_tu_soi_loai`).
    · dòng VẮNG trong tệp nhãn = "chưa có nhãn" (đỏ) — tệp liệt kê một phần tập vẫn HỢP LỆ (`H2-R1-07`,
      chiều an toàn; ISP DT1b đòi "Σ = 122" là việc của bên GHI — đổi sang "đòi đủ" khi DT1b về).
  · CHỮ KÝ: sổ `docs/ITL/_tools/so_ly_do_hd1.json` — `{"chu_ky": [{"nhan", "so_dong", "van_tay_dong",
    "nguoi_ky", "ngay"}]}`, khởi tạo RỖNG; O8 = ThuongCT ký thật (⛔ agent). Một chữ ký phủ MỌI dòng (thiếu
    ∪ loại) mang nhãn ấy, và PHẢI buộc vào ĐÚNG TẬP dòng ấy lúc đo:
      · `so_dong` = số dòng mang nhãn — lệch ⇒ ĐỎ (owner ký N dòng, ⛔ được lặng lẽ phủ dòng thứ N+1);
      · `van_tay_dong` = `_van_tay_dong(các dong_sheet mang nhãn)` — lệch ⇒ ĐỎ (`H2-R1-02` ⓑ, errata ⑬:
        chỉ buộc SỐ dòng thì đổi chỗ một dòng giữa hai nhãn đã ký — tổng mỗi nhãn y nguyên — là VÔ HÌNH,
        K5b của R1 exit 0; số đếm đúng mà tập khác là bẫy Đ4). Công cụ IN SẴN hai số ấy mỗi nhãn ở
        `dat_hd1.theo_nhan` + dòng `⑤` — owner CHÉP, ⛔ tự tính.
      · ⛔ ký nhãn `KHAC` (`H2-R1-06`, quyết định orchestrator thay BA): HD1 = lệch CÓ TÊN lý do; `KHAC` =
        "lý do khác" ⛔ phải tên. So sau khi bỏ dấu + cách + hoa/thường (`Khác`, ` khac ` cũng cấm).
      · `ngay` YYYY-MM-DD có thật VÀ ≤ hôm nay — ngày tương lai ⇒ ĐỎ; "hôm nay" truyền vào được
        (`do(hom_nay=…)`) để bài thử tất định.
    Sổ VẮNG ⇒ ĐỎ (mất sổ ⛔ được trông như "chưa ai ký").
  · ⛔⛔ Đây là MIỄN TRỪ trong cổng — repo cấm "gõ tên vào danh sách miễn trừ để cổng xanh". Nên mọi
    đầu vào hỏng (JSON · cấu trúc · kiểu · trùng · ngoài tập · vân tay · số dòng · nhãn cấm · ngày) là ĐỎ
    với nguyên nhân MỘT dòng (`S0-R1-04`), ⛔ rơi về "chưa có nhãn" cho êm; và TẬP kỳ đạt có `MONG` khai
    trước — một chữ ký thật làm đổi tập ⇒ ĐỎ ⇒ người sửa phải khai lại `MONG["dat_hd1_theo_ky"]` (Đ5).
  · ⚠ `_sha` và `MONG` (các khoá cũ) được `tools/phan_loai_dong_thieu.py` (DT1a) import — GIỮ NGUYÊN
    tên + nghĩa (`DT1a-R1-06`); H2 chỉ THÊM khoá `dat_hd1_theo_ky` · `o_moi_dong`.
  · ⚠ CG1 (Step 7, làn BE-CF) đọc `dat_hd1.so_ky_dat` · `.mau_so.so_ky` · `.ky_dat` · `.theo_ky[k].dat` ·
    `.theo_ky[k].thieu` — ⛔ đổi tên / xoá; chỉ THÊM khoá.

Chạy:  python tools/do_voi_so_luong.py            # in bảng, ⛔ ghi
       python tools/do_voi_so_luong.py --ghi      # ghi docs/ITL/_tools/voi_so_luong.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from decimal import Decimal as D
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.adapters.pm_join import (DAY_NGUOI, GHEP_DUOC, DongBank, DongPM,  # noqa: E402
                                  canon_ref, moi_noi, xep_ca_lat)
from fls.ledger.final_rule import (MAC_DINH_THEO_KHOI, may_khong_tra_loi,  # noqa: E402
                                   tinh_final)
from fls.oracle.tu_soi import la_o_loi, soi_mot_dong  # noqa: E402

FX = GOC / "tests" / "fixture"
RA = GOC / "docs" / "ITL" / "_tools" / "voi_so_luong.json"
NHAN = GOC / "docs" / "ITL" / "_tools" / "phan_loai_ly_do.json"     # DT1b ghi — H2 chỉ ĐỌC (vắng = chưa có nhãn)
SO_LY_DO = GOC / "docs" / "ITL" / "_tools" / "so_ly_do_hd1.json"    # O8 ký — H2 khởi tạo RỖNG (vắng = ĐỎ)
# ISP Step 4 §3: nhãn · số dòng · người ký · ngày — + `van_tay_dong` (H2-R1-02 ⓑ · errata ⑬: buộc chữ ký vào TẬP dòng)
KHOA_CHU_KY = ("nhan", "so_dong", "van_tay_dong", "nguoi_ky", "ngay")
# H2-R1-06 (quyết định orchestrator thay BA): HD1 = lệch CÓ TÊN lý do ⇒ nhãn gom "lý do khác" của DT1b
# (ISP Step 5: KHONG_CO_SAO_KE · KHOA_LECH · TRUNG_SEQ · KHAC) ⛔ ký được. So sau `_goc_nhan` (bỏ dấu/cách/hoa).
NHAN_CAM_KY = ("KHAC",)
KHOI =("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")

# ── `mong` — mỗi số lấy từ bài test đã ghim của chính ảnh ấy (⛔ đặt tay ở đây cho đẹp) ──
MONG = {
    "so_dong_so": 9967,              # tests/ledger/test_parity_ca_so.py · DONG_MONG_DOI
    "so_ky": 23,                     # test_pham_vi_hien_vat_dung_nhu_khai
    "so_dong_ghep_canon": 9845,      # tests/ledger/test_classifying.py · DONG_MONG_DOI
    "so_dong_bank": 9992,            # tests/adapters/test_pm_join.py
    "so_dong_pm": 3703,
    "khong_co_ma": 105,
    "khong_thay_ma_PM": 6532,
    "dong_theo_hinh": {"A": 2272, "B": 29, "C": 400, "D": 27, "E": 199, "F": 428},
    "parity_o": (69510, 69510),      # test_parity_100_phan_tram_tung_o_tren_CA_SO
    "dong_loai_tu_soi": 37,
    # ⭐ 16/11 (owner: "How done quan trọng nhất là mapping được 100%, giống các dữ liệu quá khứ"):
    "hd_parity": (9930, 9930),       # khối 1 HD, chế độ oracle (đọc MID của sổ) — đo 16/11 rồi ghim
    "tu_sinh_o": (4088, 4088),       # chế độ TỰ SINH 2026-03: FLS tự tính MID từ Manual input (tinh_mid) → Final
    "tu_sinh_hd": (584, 584),
    "tu_sinh_mid": (4020, 4088),     # MID tự tính = MID của sổ ở 4.020 ô (Final vẫn khớp đủ vì Classifying có trả lời)
    # ⭐ H15 (ISP 3.1.2 · Step 43 · WO-287) — HD1 TỰ SINH theo kỳ, khai SAU lần đo đầu (22/11, 26 kỳ có ảnh DT12). Mỗi kỳ:
    #    ô Final (khớp, tổng ô 7 khối) · khối HD · MID tự tính = MID sổ · lệch Final / lệch MID THEO KHỐI · ô bỏ vì mã lỗi.
    #    ⛔ sửa lệch MID (ISP loại trừ). Sửa được 1 kỳ ⇒ ĐỎ ⇒ khai lại ở đây (Đ5). 2026-03 = ảnh sổ CŨ; 25 kỳ còn lại = mốc 20/11.
    "tu_sinh_so_ky": 26,
    "tu_sinh_chua_do": (),
    "tu_sinh_theo_ky": {
        "2024-10": {"o": (42, 42), "hd": (6, 6), "mid": (42, 42),
                    "lech_final": {}, "lech_mid": {}, "o_loi": 0},
        "2024-11": {"o": (21, 21), "hd": (3, 3), "mid": (21, 21),
                    "lech_final": {}, "lech_mid": {}, "o_loi": 0},
        "2024-12": {"o": (42, 42), "hd": (6, 6), "mid": (42, 42),
                    "lech_final": {}, "lech_mid": {}, "o_loi": 0},
        "2025-01": {"o": (5236, 5236), "hd": (748, 748), "mid": (4758, 5236),
                    "lech_final": {}, "lech_mid": {'cdt1': 144, 'hd': 128, 'id_payee': 15, 'invoice': 18, 'pay_type': 145, 'svc_end': 13, 'svc_start': 15}, "o_loi": 0},
        "2025-02": {"o": (1979, 1981), "hd": (283, 283), "mid": (1464, 1981),
                    "lech_final": {'svc_end': 1, 'svc_start': 1}, "lech_mid": {'cdt1': 104, 'hd': 94, 'id_payee': 14, 'invoice': 63, 'pay_type': 90, 'svc_end': 76, 'svc_start': 76}, "o_loi": 0},
        "2025-03": {"o": (2077, 2079), "hd": (297, 297), "mid": (1274, 2079),
                    "lech_final": {'svc_end': 1, 'svc_start': 1}, "lech_mid": {'cdt1': 154, 'hd': 156, 'id_payee': 8, 'invoice': 84, 'pay_type': 139, 'svc_end': 132, 'svc_start': 132}, "o_loi": 0},
        "2025-04": {"o": (2324, 2324), "hd": (332, 332), "mid": (1507, 2324),
                    "lech_final": {}, "lech_mid": {'cdt1': 140, 'hd': 152, 'id_payee': 5, 'invoice': 109, 'pay_type': 142, 'svc_end': 134, 'svc_start': 135}, "o_loi": 0},
        "2025-05": {"o": (2852, 2856), "hd": (408, 408), "mid": (1611, 2856),
                    "lech_final": {'svc_end': 2, 'svc_start': 2}, "lech_mid": {'cdt1': 225, 'hd': 236, 'id_payee': 9, 'invoice': 135, 'pay_type': 221, 'svc_end': 210, 'svc_start': 209}, "o_loi": 0},
        "2025-06": {"o": (2436, 2436), "hd": (348, 348), "mid": (1956, 2436),
                    "lech_final": {}, "lech_mid": {'cdt1': 62, 'hd': 65, 'id_payee': 18, 'invoice': 83, 'pay_type': 132, 'svc_end': 60, 'svc_start': 60}, "o_loi": 0},
        "2025-07": {"o": (3822, 3822), "hd": (546, 546), "mid": (3541, 3822),
                    "lech_final": {}, "lech_mid": {'id_payee': 9, 'invoice': 98, 'pay_type': 174}, "o_loi": 0},
        "2025-08": {"o": (3759, 3759), "hd": (537, 537), "mid": (3488, 3759),
                    "lech_final": {}, "lech_mid": {'id_payee': 12, 'invoice': 104, 'pay_type': 155}, "o_loi": 0},
        "2025-09": {"o": (3507, 3507), "hd": (501, 501), "mid": (3356, 3507),
                    "lech_final": {}, "lech_mid": {'id_payee': 8, 'invoice': 74, 'pay_type': 69}, "o_loi": 0},
        "2025-10": {"o": (3401, 3409), "hd": (487, 487), "mid": (3264, 3409),
                    "lech_final": {'svc_end': 8}, "lech_mid": {'id_payee': 12, 'invoice': 81, 'pay_type': 31, 'svc_end': 21}, "o_loi": 0},
        "2025-11": {"o": (3321, 3339), "hd": (477, 477), "mid": (3208, 3339),
                    "lech_final": {'svc_end': 18}, "lech_mid": {'id_payee': 5, 'invoice': 61, 'pay_type': 31, 'svc_end': 34}, "o_loi": 0},
        "2025-12": {"o": (3943, 3962), "hd": (566, 566), "mid": (3764, 3962),
                    "lech_final": {'svc_end': 19}, "lech_mid": {'id_payee': 18, 'invoice': 59, 'pay_type': 78, 'svc_end': 43}, "o_loi": 0},
        "2026-01": {"o": (3290, 3297), "hd": (471, 471), "mid": (3184, 3297),
                    "lech_final": {'svc_end': 7}, "lech_mid": {'id_payee': 4, 'invoice': 62, 'pay_type': 26, 'svc_end': 21}, "o_loi": 0},
        "2026-02": {"o": (3073, 3073), "hd": (439, 439), "mid": (3020, 3073),
                    "lech_final": {}, "lech_mid": {'invoice': 53}, "o_loi": 0},
        "2026-03": {"o": (4088, 4088), "hd": (584, 584), "mid": (4020, 4088),
                    "lech_final": {}, "lech_mid": {'cdt1': 2, 'id_payee': 2, 'invoice': 62, 'pay_type': 2}, "o_loi": 0},
        "2026-04": {"o": (4200, 4200), "hd": (600, 600), "mid": (4126, 4200),
                    "lech_final": {}, "lech_mid": {'invoice': 66, 'pay_type': 8}, "o_loi": 0},
        "2026-05": {"o": (3759, 3759), "hd": (537, 537), "mid": (3682, 3759),
                    "lech_final": {}, "lech_mid": {'id_payee': 4, 'invoice': 72, 'svc_end': 1}, "o_loi": 0},
        "2026-06": {"o": (4291, 4291), "hd": (613, 613), "mid": (4251, 4291),
                    "lech_final": {}, "lech_mid": {'invoice': 40}, "o_loi": 0},
        "2026-07": {"o": (4770, 4802), "hd": (686, 686), "mid": (4762, 4802),
                    "lech_final": {'cdt1': 7, 'id_payee': 6, 'invoice': 9, 'svc_end': 5, 'svc_start': 5}, "lech_mid": {'invoice': 40}, "o_loi": 0},
        "2026-08": {"o": (5068, 5068), "hd": (724, 724), "mid": (5043, 5068),
                    "lech_final": {}, "lech_mid": {'invoice': 25}, "o_loi": 0},
        "2026-09": {"o": (5159, 5159), "hd": (737, 737), "mid": (5119, 5159),
                    "lech_final": {}, "lech_mid": {'invoice': 40}, "o_loi": 0},
        "2026-10": {"o": (7266, 7266), "hd": (1038, 1038), "mid": (7249, 7266),
                    "lech_final": {}, "lech_mid": {'invoice': 17}, "o_loi": 0},
        "2026-11": {"o": (4613, 4613), "hd": (659, 659), "mid": (4610, 4613),
                    "lech_final": {}, "lech_mid": {'invoice': 3}, "o_loi": 0},
    },
    "checksum": {"itl_ledge_adjustment.json": "575c53379074c759",
                 "classifying_vs_canon.json": "7226ef112dbd00f7",
                 "pm_join.json": "6ec10945e6c1636a"},
    # ⭐ H2 (ISP 3.1.2 · Step 4 · WO-090) — TẬP kỳ ĐẠT HD1 (mọi kỳ khác là ĐỎ), khai TRƯỚC lần đo đầu:
    #    AP v3.1.2 §5.3.1 "dòng ghép 1-1: 9.845/9.967 — 5/23 tháng đủ" + BG-081 §Bảng đếm (đúng 5 kỳ ⛔ có
    #    dòng thiếu) · ô Final 23/23 tháng. Sổ lý do RỖNG ⇒ chỉ kỳ đủ dòng mới đạt. Một chữ ký THẬT (O8)
    #    làm đổi tập này ⇒ ĐỎ ⇒ khai lại ở đây cùng commit chữ ký (Đ5 — cố ý, ⛔ lỗi).
    #    ⭐ Vòng sửa sau R1 (H2-R1-01 ⓐ): vế ô nay đọc MỌI dòng ⇒ 2026-07 đỏ thêm vì ô — tập ⛔ đổi (5 = 5):
    #    5 kỳ trên ⛔ có dòng tự-soi loại nào (37/37 ở 2026-07), và 2026-07 vốn đỏ vì 23 dòng thiếu.
    "dat_hd1_theo_ky": ("2024-10", "2024-11", "2024-12", "2025-03", "2025-04"),
    # ⭐ H2-R1-01 — ô Final = f(Cls, MID) trên MỌI dòng sổ (gồm 37 dòng tự-soi loại), mẫu số vế [ô] của HD1.
    #    Khai TRƯỚC lần đo của công cụ, từ HAI nguồn: KQ-092 phép (b) — R1 đo ĐỘC LẬP (⛔ import tool):
    #    69.706/69.769; và tests/ledger/test_parity_ca_so.py — 63 ô lệch (60 ngoài miền + 3 trong miền)
    #    ⇒ 69.769 − 63 = 69.706. Khác `parity_o` (69.510 = 9.930 dòng tự nhất quán × 7) — hai phép, hai nhãn.
    "o_moi_dong": (69706, 69769),
}
_HONG = object()                     # dấu "tệp ⛔ đọc được" của _doc_json (⛔ nhầm với JSON `null`)


def _chuan(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def _nap(ten: str) -> dict:
    return json.loads((FX / ten).read_text(encoding="utf-8"))


def _sha(*phan) -> str:
    return hashlib.sha256(json.dumps(list(phan), ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()[:16]


# ══════════════════════════════════════════════════════════════════ HD1 theo kỳ (H2 · WO-090)
def _van_tay_dong(so_dong) -> str:
    """Vân tay một TẬP dòng = sha256 (16 ký tự) của danh sách số dòng ĐÃ SẮP — ĐÚNG công thức `_van_tay`
    của `tools/phan_loai_dong_thieu.py` (DT1a). ⛔ import ngược từ đó: DT1a đã import tệp này (vòng).
    Bài `test_H2_B1_van_tay_tap_dong_TRUNG_DT1a` canh hai bản bằng nhau (Đ2 — hai nguồn)."""
    return hashlib.sha256(json.dumps(sorted(so_dong), separators=(",", ":")).encode()).hexdigest()[:16]


def _duong(p: Path) -> str:
    try:
        return str(p.resolve().relative_to(GOC))
    except ValueError:
        return str(p)


def _doc_json(p: Path, ten: str, loi: list[str]):
    """Đọc một tệp JSON; ⛔ đọc được ⇒ MỘT dòng lỗi (`S0-R1-04`, ⛔ traceback) và trả `_HONG`."""
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:        # vắng/quyền ⊂ OSError · JSON/UTF-8 hỏng ⊂ ValueError
        loi.append(f"{ten} {_duong(p)}: ⛔ đọc được — {type(e).__name__}: " + " ".join(str(e).split()))
        return _HONG


def _co_chu(v) -> bool:
    return isinstance(v, str) and v.strip() != ""


def _so_nguyen(v) -> bool:
    return isinstance(v, int) and not isinstance(v, bool)   # ⛔ True/False: bool là con của int


def _ngay_that(v) -> bool:
    # ⛔ regex là chốt DUY NHẤT của khuôn: `date.fromisoformat` của Python ≥ 3.11 nhận cả `20261116` lẫn
    #    `2026-W47-1` (R1 đo: cả hai ra 2026-11-16 — `H2-R1-04`, đột biến R1-M19); bài thử có ca phá riêng.
    if not (isinstance(v, str) and re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", v)):
        return False
    try:
        date.fromisoformat(v)
    except ValueError:                         # 2026-02-30 đúng khuôn mà ⛔ có thật
        return False
    return True


def _goc_nhan(n: str) -> str:
    """Dạng gốc của tên nhãn để so với `NHAN_CAM_KY`: bỏ dấu (NFKD + bỏ dấu kết hợp, `Đ`→`D`), bỏ cách hai
    đầu, viết hoa — `KHAC` · `Khác` · ` khac ` cùng một gốc (⛔ lách luật bằng cách gõ khác đi)."""
    bo_dau = "".join(c for c in unicodedata.normalize("NFKD", n) if not unicodedata.combining(c))
    return bo_dau.replace("Đ", "D").replace("đ", "d").strip().upper()


def _doc_nhan(tep: Path, van_tay: dict, tap_hop_le: set[int], loi: list[str]) -> dict[int, str] | None:
    """Tệp nhãn DT1b → `{dong_sheet: nhãn}` (chỉ dòng CÓ nhãn). Vắng ⇒ `{}` (DT1b chưa về — mọi dòng thiếu
    là "chưa có nhãn", ⛔ lỗi). Có mà hỏng ⇒ `None` + lỗi (mỗi luật một dòng; bài thử có ca phá riêng).
    `tap_hop_le` = dòng thiếu ∪ dòng tự-soi loại (H2-R1-01 ⓐ). Dòng VẮNG trong tệp = chưa có nhãn (H2-R1-07)."""
    if not tep.exists():
        return {}
    d = _doc_json(tep, "tệp nhãn", loi)
    if d is _HONG:
        return None
    if not (isinstance(d, dict) and isinstance(d.get("van_tay"), dict) and isinstance(d.get("dong_thieu"), list)):
        loi.append(f"tệp nhãn {_duong(tep)}: cấu trúc sai — cần "
                   "{'van_tay': {'thieu', 'nguoc'}, 'dong_thieu': [{'dong_sheet', 'nhan'}]}")
        return None
    truoc = len(loi)
    for tap, ten in (("thieu", "thiếu"), ("nguoc", "ngược")):
        if d["van_tay"].get(tap) != van_tay[tap]:
            loi.append(f"tệp nhãn: vân tay tập {ten} — tệp ghi {d['van_tay'].get(tap)!r} · ảnh hôm nay "
                       f"{van_tay[tap]!r} — nhãn của một tập dòng KHÁC")
    nhan: dict[int, str] = {}
    da_thay: set[int] = set()
    for i, x in enumerate(d["dong_thieu"]):
        ds = x.get("dong_sheet") if isinstance(x, dict) else None
        if not _so_nguyen(ds):
            loi.append(f"tệp nhãn: dong_thieu[{i}] cần dong_sheet là số nguyên — có {ds!r}")
            continue
        if ds not in tap_hop_le:
            loi.append(f"tệp nhãn: dong_sheet {ds} ngoài tập {len(tap_hop_le)} dòng (thiếu ∪ tự-soi loại)")
            continue
        if ds in da_thay:
            loi.append(f"tệp nhãn: dong_sheet {ds} trùng — một dòng chỉ một nhãn")
            continue
        da_thay.add(ds)
        n = x.get("nhan")
        if n is None:
            continue                           # null = chưa có nhãn (đỏ), ⛔ lỗi
        if not _co_chu(n):
            loi.append(f"tệp nhãn: dong_sheet {ds} — nhãn phải là chuỗi có chữ hoặc null, có {n!r}")
            continue
        nhan[ds] = n
    return None if len(loi) > truoc else nhan


def _doc_so(tep: Path, loi: list[str], hom_nay: date) -> list[dict] | None:
    """Sổ lý do → danh sách chữ ký đã kiểm. Vắng/hỏng ⇒ `None` + lỗi (mỗi luật một dòng). Kiểm NGHĨA của
    thứ được ký, ⛔ chỉ kiểu (`H2-R1-06`): nhãn ⛔ được là `KHAC`; ngày ⛔ được sau `hom_nay`."""
    d = _doc_json(tep, "sổ lý do", loi)
    if d is _HONG:
        return None
    if not (isinstance(d, dict) and isinstance(d.get("chu_ky"), list)):
        loi.append(f"sổ lý do {_duong(tep)}: cấu trúc sai — cần {{'chu_ky': [{{{', '.join(KHOA_CHU_KY)}}}]}}")
        return None
    truoc = len(loi)
    for i, c in enumerate(d["chu_ky"]):
        if not (isinstance(c, dict) and set(c) == set(KHOA_CHU_KY)):
            loi.append(f"sổ lý do: chu_ky[{i}] khoá phải đúng {KHOA_CHU_KY} — có "
                       f"{tuple(sorted(c)) if isinstance(c, dict) else type(c).__name__}")
            continue
        if not _co_chu(c["nhan"]):
            loi.append(f"sổ lý do: chu_ky[{i}] nhãn phải là chuỗi có chữ — có {c['nhan']!r}")
        elif _goc_nhan(c["nhan"]) in NHAN_CAM_KY:
            loi.append(f"sổ lý do: chu_ky[{i}] nhãn {c['nhan']!r} ⛔ ký được — {'/'.join(NHAN_CAM_KY)} = 'lý do "
                       "khác', ⛔ tên; HD1 đòi lệch CÓ TÊN lý do (H2-R1-06) — gán nhãn có tên rồi ký")
        if not (_so_nguyen(c["so_dong"]) and c["so_dong"] > 0):
            loi.append(f"sổ lý do: chu_ky[{i}] so_dong phải là số nguyên > 0 — có {c['so_dong']!r}")
        if not (isinstance(c["van_tay_dong"], str) and re.fullmatch(r"[0-9a-f]{16}", c["van_tay_dong"])):
            loi.append(f"sổ lý do: chu_ky[{i}] van_tay_dong phải là 16 ký tự hex thường (chép từ "
                       f"dat_hd1.theo_nhan) — có {c['van_tay_dong']!r}")
        if not _co_chu(c["nguoi_ky"]):
            loi.append(f"sổ lý do: chu_ky[{i}] người ký phải là chuỗi có chữ — có {c['nguoi_ky']!r}")
        if not _ngay_that(c["ngay"]):
            loi.append(f"sổ lý do: chu_ky[{i}] ngày phải là YYYY-MM-DD có thật — có {c['ngay']!r}")
        elif date.fromisoformat(c["ngay"]) > hom_nay:
            loi.append(f"sổ lý do: chu_ky[{i}] ngày {c['ngay']} sau hôm nay {hom_nay.isoformat()} — ⛔ ký trước "
                       "(H2-R1-06)")
    dem = Counter(c["nhan"] for c in d["chu_ky"] if isinstance(c, dict) and isinstance(c.get("nhan"), str))
    for n, k in sorted(dem.items()):
        if k > 1:
            loi.append(f"sổ lý do: nhãn {n!r} ký trùng {k} lần — một nhãn một chữ ký")
    return None if len(loi) > truoc else d["chu_ky"]


def phan_hd1(theo_ky: dict, thieu: list[tuple[int, str]], van_tay: dict,
             tep_nhan: Path = NHAN, tep_so: Path = SO_LY_DO, *,
             loai: list[tuple[int, str]], hom_nay: date | None = None) -> tuple[dict | None, list[str]]:
    """Phán HD1 theo kỳ → (khối `dat_hd1`, lỗi). Đầu vào hỏng ⇒ (None, lỗi): ⛔ phán kỳ nào (Đ5).

    `theo_ky` — `{kỳ: {"co", "chay", "o_parity", "o_parity_khop", "o_moi_dong", "o_moi_dong_khop",
                "loai_tu_soi", …}}` (bốn số của `do()` + ô trên MỌI dòng);
    `thieu`   — `[(dong_sheet, kỳ)]` dòng sổ ⛔ ghép 1-1; `van_tay` — `{"thieu", "nguoc"}` tính từ ảnh;
    `loai`    — `[(dong_sheet, kỳ)]` dòng `soi_mot_dong` loại (H2-R1-01 ⓐ). BẮT BUỘC, ⛔ mặc định: quên
                truyền mà mặc định "rỗng" thì vế ô lặng lẽ thành "mọi dòng loại đã ký" (0/0) — đúng bẫy cũ;
    `hom_nay` — ngày so với `ngay` của chữ ký (H2-R1-06); `None` ⇒ `date.today()`."""
    loi: list[str] = []
    cac_ky = sorted(theo_ky)
    thieu_ky: dict[str, list[int]] = defaultdict(list)
    for d, k in thieu:
        thieu_ky[k].append(d)
    loai_ky: dict[str, list[int]] = defaultdict(list)
    for d, k in loai:
        loai_ky[k].append(d)
    # Phòng thủ chồng (Đ2 — hai nguồn cho cùng một số): `có − chạy` của kỳ ↔ dòng thiếu liệt kê;
    # `loai_tu_soi` của kỳ ↔ dòng tự-soi loại liệt kê.
    for k in cac_ky:
        a = theo_ky[k].get("co", 0) - theo_ky[k].get("chay", 0)
        if a != len(thieu_ky.get(k, ())):
            loi.append(f"phòng thủ: kỳ {k} có − chạy = {a} · dòng thiếu liệt kê {len(thieu_ky.get(k, ()))}")
        b = theo_ky[k].get("loai_tu_soi", 0)
        if b != len(loai_ky.get(k, ())):
            loi.append(f"phòng thủ: kỳ {k} loai_tu_soi = {b} · dòng tự-soi loại liệt kê {len(loai_ky.get(k, ()))}")
    ngoai = sorted((set(thieu_ky) | set(loai_ky)) - set(cac_ky))
    if ngoai:
        loi.append(f"phòng thủ: dòng thiếu / tự-soi loại thuộc kỳ ngoài bảng {ngoai}")
    nhan = _doc_nhan(tep_nhan, van_tay, {d for d, _ in thieu} | {d for d, _ in loai}, loi)
    chu_ky = _doc_so(tep_so, loi, hom_nay or date.today())
    if nhan is not None and chu_ky is not None:
        dong_cua: dict[str, list[int]] = defaultdict(list)
        for d, n in nhan.items():
            dong_cua[n].append(d)
        for c in chu_ky:
            ds = dong_cua.get(c["nhan"], [])
            vt = _van_tay_dong(ds)
            # ⛔ chỉ so SỐ dòng: đổi chỗ một dòng giữa hai nhãn đã ký giữ nguyên tổng mỗi nhãn (K5b · H2-R1-02)
            if len(ds) != c["so_dong"] or vt != c["van_tay_dong"]:
                loi.append(f"sổ lý do: chữ ký {c['nhan']!r} ({c['nguoi_ky']} · {c['ngay']}) ghi số dòng {c['so_dong']} "
                           f"· vân tay dòng {c['van_tay_dong']} — tệp nhãn có {len(ds)} dòng (thiếu ∪ tự-soi loại) "
                           f"mang nhãn ấy · vân tay dòng {vt} — chữ ký cũ, ký lại")
    if loi:
        return None, loi

    da_ky = {c["nhan"] for c in chu_ky}
    ket: dict[str, dict] = {}
    for k in cac_ky:
        x, ds, ls = theo_ky[k], thieu_ky.get(k, []), loai_ky.get(k, [])
        ky = sum(1 for d in ds if nhan.get(d) in da_ky)
        lk = sum(1 for d in ls if nhan.get(d) in da_ky)
        dong_100 = not ds
        om, omk = x.get("o_moi_dong", 0), x.get("o_moi_dong_khop", 0)
        # [ô] — Đ3: 0/0 ⛔ 100 %. Vế phải "dòng loại đã ký" đi kèm "ô của dòng tự nhất quán khớp hết": mọi ô
        #       lệch phải nằm trong dòng ĐÃ KÝ; ⛔ thế thì kỳ ⛔ có dòng loại được miễn suông (0 = 0).
        o_100 = om > 0 and (omk == om or (lk == len(ls)
                                           and x.get("o_parity_khop", 0) == x.get("o_parity", 0)))
        ket[k] = {"dat": (dong_100 or ky == len(ds)) and o_100, "thieu": len(ds),
                  "co_nhan": sum(1 for d in ds if d in nhan), "da_ky": ky,
                  "dong_100": dong_100, "o_100": o_100,
                  "loai_tu_soi": len(ls), "loai_co_nhan": sum(1 for d in ls if d in nhan), "loai_da_ky": lk,
                  "o_moi_dong": om, "o_moi_dong_khop": omk}
    ky_dat = [k for k in cac_ky if ket[k]["dat"]]
    dong_cua = defaultdict(list)
    for d, n in nhan.items():
        dong_cua[n].append(d)
    return {
        "_luat": ("kỳ ĐẠT HD1 ⇔ [dòng] (dòng 1-1 100 % hoặc mọi dòng thiếu của kỳ có nhãn ĐÃ KÝ trong sổ lý do) "
                  "∧ [ô] (mẫu số ô trên MỌI dòng sổ của kỳ > 0 ∧ (ô Final = f(Classifying, MID) khớp trên MỌI dòng "
                  "— gồm dòng tự-soi loại, ⛔ chỉ dòng đã ghép — hoặc mọi dòng tự-soi loại của kỳ có nhãn ĐÃ KÝ và "
                  "ô của các dòng còn lại khớp hết)). `o_100` = vế [ô] ấy (H2-R1-01 ⓐ, errata ⑩). Nhãn: tệp DT1b, "
                  "tập hợp lệ = dòng thiếu ∪ dòng tự-soi loại; dòng VẮNG trong tệp nhãn = chưa có nhãn (đỏ, ⛔ lỗi). "
                  "Chữ ký: so_dong + van_tay_dong phải bằng TẬP dòng mang nhãn lúc đo (chép từ theo_nhan — "
                  "errata ⑬); ⛔ ký KHAC; ngày ≤ hôm nay. ⛔ xét: chế độ tự sinh (H15); chiều ngược — dòng FLS ⛔ "
                  "có dòng sổ (số ở ngoai_phan; ảnh pm_join ⛔ có ngày ⇒ ⛔ gán được kỳ; BA chốt khi DT2). "
                  "AP v3.1.2 §5.3.1 HD1."),
        "mau_so": {"so_ky": len(cac_ky), "dong_so": sum(theo_ky[k].get("co", 0) for k in cac_ky),
                   "dong_thieu": len(thieu), "dong_tu_soi_loai": len(loai),
                   "o_moi_dong": sum(theo_ky[k].get("o_moi_dong", 0) for k in cac_ky)},
        "tep_nhan": {"duong": _duong(tep_nhan), "co": tep_nhan.exists()},
        "so_ly_do": _duong(tep_so),
        "so_chu_ky": len(chu_ky),
        "van_tay": dict(van_tay),
        "dem": {"thieu": len(thieu), "co_nhan": sum(1 for d, _ in thieu if d in nhan),
                "da_ky": sum(1 for d, _ in thieu if nhan.get(d) in da_ky),
                "loai_tu_soi": len(loai), "loai_co_nhan": sum(1 for d, _ in loai if d in nhan),
                "loai_da_ky": sum(1 for d, _ in loai if nhan.get(d) in da_ky)},
        "so_ky_dat": len(ky_dat),
        "ky_dat": ky_dat,
        "theo_ky": ket,
        # H2-R1-02 ⓑ — owner CHÉP hai số này vào chữ ký (⛔ tự tính); `cam_ky` = nhãn ⛔ ký được (H2-R1-06)
        "theo_nhan": {n: {"so_dong": len(ds), "van_tay_dong": _van_tay_dong(ds), "da_ky": n in da_ky,
                          "cam_ky": _goc_nhan(n) in NHAN_CAM_KY} for n, ds in sorted(dong_cua.items())},
        # H2-R1-01 ⓐ — TẬP dòng tự-soi loại (danh tính, ⛔ chỉ số đếm): nơi gán nhãn cho chúng cần biết dòng nào
        "dong_tu_soi_loai": {k: sorted(ls) for k, ls in sorted(loai_ky.items())},
    }, []


def do(nhan: Path = NHAN, so_ly_do: Path = SO_LY_DO, hom_nay: date | None = None) -> dict:
    """Đo cả bảng + khối `dat_hd1`. `hom_nay` (H2-R1-06) — ngày so với `ngay` của chữ ký; `None` ⇒ hôm nay
    của máy (CLI); bài thử truyền vào để tất định."""
    loi: list[str] = []

    def kiem(ten, co, mong):
        if co != mong:
            loi.append(f"{ten}: đo {co!r} · mong {mong!r}")

    # ① sổ AS-IS · ITL Ledge (Classifying / MID / Final × 7 khối, kỳ đã dựng lại)
    g = _nap("itl_ledge_adjustment.json")
    kiem("checksum itl_ledge_adjustment", _sha(g["dong"], g["bang_gia_tri"]),
         MONG["checksum"]["itl_ledge_adjustment.json"])
    idx = {n: i for i, n in enumerate(g["cot"])}
    bang = g["bang_gia_tri"]

    def val(h, ten):
        i = h[idx[ten]]
        return None if i == -1 else bang[i]

    so = []                                   # (dong_sheet, ky, {khoi: (cls, None, mid, fin)})
    for h in g["dong"]:
        so.append((h[0], h[1], {k: (val(h, f"{k}_classifying"), None, val(h, f"{k}_mid"),
                                    val(h, f"{k}_final")) for k in KHOI}))
    kiem("số dòng sổ", len(so), MONG["so_dong_so"])
    ky_cua_dong = {d: k for d, k, _ in so}
    cac_ky = sorted({k for _, k, _ in so})
    kiem("số kỳ", len(cac_ky), MONG["so_ky"])

    # ② dòng FLS dựng lại ↔ dòng sổ (khoá Số CT · PS Nợ · PS Có · TK · tiền tệ)
    c = _nap("classifying_vs_canon.json")
    kiem("checksum classifying_vs_canon", c["checksum_noi_dung"], MONG["checksum"]["classifying_vs_canon.json"])
    ci = {n: i for i, n in enumerate(c["cot"])}
    canon_ve_so = {r[ci["dong_canon"]]: r[ci["dong_so"]] for r in c["dong"]}
    so_co_canon = set(canon_ve_so.values())
    kiem("số dòng ghép canon", len(so_co_canon), MONG["so_dong_ghep_canon"])

    # ③ ghép bank ↔ PM bằng CHÍNH mã FLS
    p = _nap("pm_join.json")
    kiem("checksum pm_join", p["checksum_noi_dung"], MONG["checksum"]["pm_join.json"])
    bank = [DongBank(x["dong"], canon_ref(x["ref_tho"]), D(x["tien"]), x["cur"]) for x in p["bank"]]
    pm = [DongPM(x["dong"], x["slip"], x["line"], D(x["tien"]) if x["tien"] else None, x["cur"],
                 x["status"], canon_ref(x["ref_tho"]), x["hd"] or None, x["cdt1"] or None) for x in p["pm"]]
    nhom, tk = xep_ca_lat(bank, pm)
    kiem("số dòng bank", tk.dong_bank, MONG["so_dong_bank"])
    kiem("số dòng PM", len(pm), MONG["so_dong_pm"])
    kiem("bank không có mã", tk.khong_co_ma, MONG["khong_co_ma"])
    kiem("bank không thấy mã PM", tk.khong_thay_ma_PM, MONG["khong_thay_ma_PM"])
    kiem("dòng theo hình", dict(tk.dong_theo_hinh), MONG["dong_theo_hinh"])
    hinh_cua_bank: dict[int, str] = {}
    line_cua_bank: dict[int, set] = defaultdict(set)
    for n in nhom:
        for b in n.bank:
            hinh_cua_bank[b.dong_sheet] = n.hinh
        if n.ghep_duoc:
            for dong_b, line, _t in moi_noi(n):
                line_cua_bank[dong_b].add(line)

    # ④ từng kỳ
    o = {k: Counter() for k in cac_ky}
    khoi_ky = {k: Counter() for k in cac_ky}           # ô người điền theo khối: '<khối>:go' · '<khối>:md'
    line_ky: dict[str, set] = {k: set() for k in cac_ky}
    tong_o = khop_o = 0
    loai = 0
    # H2-R1-01 ⓐ — ô trên MỌI dòng (⛔ bỏ dòng tự-soi loại) cho vế [ô] của HD1. Counter RIÊNG, ⛔ trộn vào `o`:
    # `theo_ky`/`tong` cũ của voi_so_luong.json giữ y nguyên (AP sinh từ đó); số mới chỉ sống trong `dat_hd1`.
    o_moi = {k: Counter() for k in cac_ky}
    dong_loai: list[tuple[int, str]] = []
    for dong, ky, bon in so:
        x = o[ky]
        for kh, (cls, _m, mid, fin) in bon.items():
            if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):      # CÙNG luật bỏ ô lỗi với parity bên dưới
                continue
            o_moi[ky]["o_moi_dong"] += 1
            o_moi[ky]["o_moi_dong_khop"] += _chuan(tinh_final(_chuan(cls) or None, _chuan(mid) or None)) == _chuan(fin)
        x["co"] += 1
        if dong in so_co_canon:
            x["chay"] += 1
        cls_hd = _chuan(bon["hd"][0])
        if cls_hd and not la_o_loi(cls_hd) and not may_khong_tra_loi(cls_hd):
            x["map_now"] += 1
        for kh, (cls, _m, mid, fin) in bon.items():
            sc, sf = _chuan(cls), _chuan(fin)
            if la_o_loi(sc) or la_o_loi(sf):
                continue
            if may_khong_tra_loi(sc):
                if not sf:
                    x["o_trong"] += 1
                elif MAC_DINH_THEO_KHOI.get(kh) is not None and sf == MAC_DINH_THEO_KHOI[kh]:
                    x["o_mac_dinh"] += 1
                    khoi_ky[ky][f"{kh}:md"] += 1
                else:
                    x["o_go_that"] += 1
                    khoi_ky[ky][f"{kh}:go"] += 1
            elif sf and sf != sc:
                x["o_de"] += 1
        # parity: FLS tính lại Final (bỏ dòng tu_soi loại, ô lỗi là câu trả lời)
        if not soi_mot_dong(bon).giu:
            loai += 1
            x["loai_tu_soi"] += 1
            dong_loai.append((dong, ky))
            continue
        for kh, (cls, _m, mid, fin) in bon.items():
            if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
                continue
            tinh = tinh_final(_chuan(cls) or None, _chuan(mid) or None)
            tong_o += 1
            x["o_parity"] += 1
            trung = _chuan(tinh) == _chuan(fin)
            if trung:
                khop_o += 1
                x["o_parity_khop"] += 1
            if kh == "hd":
                x["hd_parity"] += 1
                x["hd_parity_khop"] += trung
    kiem("parity ô", (khop_o, tong_o), MONG["parity_o"])
    kiem("dòng tu_soi loại", loai, MONG["dong_loai_tu_soi"])
    # MONG.get: mất khoá ⇒ ĐỎ một dòng, ⛔ KeyError (S0-R1-04)
    kiem("ô Final trên MỌI dòng (o_moi_dong)", (sum(o_moi[k]["o_moi_dong_khop"] for k in cac_ky),
                                                 sum(o_moi[k]["o_moi_dong"] for k in cac_ky)),
         tuple(MONG.get("o_moi_dong") or ()))
    kiem("parity khối HD", (sum(o[k]["hd_parity_khop"] for k in cac_ky), sum(o[k]["hd_parity"] for k in cac_ky)), MONG["hd_parity"])
    tsk = do_tu_sinh_theo_ky()
    loi.extend(tsk["loi"])
    tu_sinh = dict(tsk["theo_ky"].get("2026-03") or {"ky": "2026-03", "o": (0, 0), "hd": (0, 0), "mid": (0, 0)})
    kiem("tự sinh ô Final 2026-03", tu_sinh["o"], MONG["tu_sinh_o"])
    kiem("tự sinh khối HD 2026-03", tu_sinh["hd"], MONG["tu_sinh_hd"])
    kiem("tự sinh MID 2026-03", tu_sinh["mid"], MONG["tu_sinh_mid"])
    # H15 — MONG theo kỳ (Đ5 hai chiều): so TỪNG kỳ với bản khai; kỳ ⛔ đo được ⇒ ĐỎ có tên (⛔ "không thấy lệch")
    kiem("số kỳ tự sinh có ảnh", tsk["so_ky_co_anh"], MONG.get("tu_sinh_so_ky"))
    kiem("kỳ chua_do", tuple(sorted(tsk["chua_do"])), tuple(MONG.get("tu_sinh_chua_do") or ()))
    for ky, mo in (MONG.get("tu_sinh_theo_ky") or {}).items():
        x = tsk["theo_ky"].get(ky)
        if x is not None:
            kiem(f"tự sinh {ky} (ô Final · HD · MID · lệch Final theo khối · lệch MID theo khối · ô lỗi)",
                 (tuple(x["o"]), tuple(x["hd"]), tuple(x["mid"]), x["lech_final"], x["lech_mid"], x["o_loi"]),
                 (tuple(mo["o"]), tuple(mo["hd"]), tuple(mo["mid"]), mo["lech_final"], mo["lech_mid"], mo["o_loi"]))
    for ky in sorted(set(tsk["theo_ky"]) - set(MONG.get("tu_sinh_theo_ky") or {})):
        loi.append(f"tự sinh {ky}: đo được nhưng MONG ⛔ khai kỳ này (Đ5)")
    tu_sinh["theo_ky"] = tsk["theo_ky"]
    tu_sinh.update({"so_ky_co_anh": tsk["so_ky_co_anh"], "chua_do": tsk["chua_do"], "tong": tsk["tong"],
                    "moc_so": tsk["moc_so"]})

    # mapping FLS + PM line theo kỳ (bank → dòng canon → dòng sổ → kỳ)
    bank_khong_ky = 0
    for b in bank:
        dso = canon_ve_so.get(b.dong_sheet)
        ky = ky_cua_dong.get(dso) if dso is not None else None
        if ky is None:
            bank_khong_ky += 1
            continue
        h = hinh_cua_bank.get(b.dong_sheet)
        if h in GHEP_DUOC:
            o[ky]["map_fls"] += 1
            line_ky[ky] |= line_cua_bank.get(b.dong_sheet, set())
        elif h in DAY_NGUOI:
            o[ky]["day_nguoi"] += 1
    for k in cac_ky:
        o[k]["pm_noi"] = len(line_ky[k])

    # ⑤ HD1 theo kỳ (H2): dòng thiếu = dòng sổ ⛔ ghép 1-1 — cùng phép trừ với DT1a, tập khoá bằng vân tay
    thieu = [(dong, ky) for dong, ky, _ in so if dong not in so_co_canon]
    nguoc = {b.dong_sheet for b in bank} - set(canon_ve_so)
    van_tay = {"thieu": _van_tay_dong(d for d, _ in thieu), "nguoc": _van_tay_dong(nguoc)}
    hd1, loi_hd1 = phan_hd1({k: {**o[k], **o_moi[k]} for k in cac_ky}, thieu, van_tay, nhan, so_ly_do,
                            loai=dong_loai, hom_nay=hom_nay)
    loi.extend(loi_hd1)
    if hd1 is not None:                        # đầu vào hỏng ⇒ loi_hd1 đã ĐỎ, ⛔ so MONG trên phán rỗng
        kiem("kỳ đạt HD1 (dat_hd1_theo_ky)", tuple(hd1["ky_dat"]), tuple(MONG.get("dat_hd1_theo_ky") or ()))
        # H2-R1-05 (Đ4) — chiều ngược KHAI bằng số, ⛔ chỉ bằng lời: tập này ⛔ vào phán kỳ nào ở bước này
        hd1["ngoai_phan"] = {
            "dong_fls_khong_co_dong_so": len(nguoc),
            "_vi_sao": ("dòng FLS dựng lại (bank) ⛔ có dòng sổ AS-IS — chiều ngược của HD1, = DT1a dong_nguoc. "
                        "⛔ vào phán kỳ: ảnh pm_join.json ⛔ có ngày ⇒ ⛔ gán được kỳ. BA chốt khi DT2 (Step 8) "
                        "đóng băng được ngày."),
        }

    if any(o[k]["co"] == 0 for k in cac_ky):   # Đ3 — mẫu số rỗng là KẾT QUẢ, ⛔ nền
        loi.append("có kỳ 0 dòng")
    if loi:
        raise SystemExit("⛔ VOI SỐ LƯỢNG ĐỎ — số đo khác số đã ghim, hoặc ⛔ đo được:\n  " + "\n  ".join(loi))

    tong = Counter()
    for k in cac_ky:
        tong.update(o[k])
    return {
        "_vi_sao": "Sinh bởi tools/do_voi_so_luong.py — chạy mã FLS lên ảnh đóng băng tests/fixture/. ⛔ sửa tay.",
        "nguon": {"so": g["nguon"], "so_dong_bang": g["ngay_dong_bang"], "canon": c["nguon"], "pm": p["nguon"],
                  "checksum": MONG["checksum"]},
        "ky": cac_ky,
        "theo_ky": {k: dict(o[k]) for k in cac_ky},
        "khoi_theo_ky": {k: {kh: [khoi_ky[k][f"{kh}:go"], khoi_ky[k][f"{kh}:md"]] for kh in KHOI} for k in cac_ky},
        "tong": dict(tong),
        "pm_tong": {"so_dong_pm": len(pm), "pm_noi_tong": len(set().union(*line_ky.values())),
                    "pm_co_ref": sum(1 for x in pm if x.ref)},
        "tu_sinh": tu_sinh,
        "bank_tong": {"dong_bank": tk.dong_bank, "khong_co_ma": tk.khong_co_ma,
                      "khong_thay_ma_PM": tk.khong_thay_ma_PM, "dong_theo_hinh": dict(tk.dong_theo_hinh),
                      "bank_khong_ky": bank_khong_ky},
        "dat_hd1": hd1,
    }


ANH_DAP_AN = FX / "dap_an"
# ⭐ WO-345 (chủ 23/11: NGUỒN SỐNG là chuẩn) — đóng băng LẠI 26 kỳ từ sổ sống (`doc_itl_ledge_ky.py --hau-to _20261123
#    --ca-2026-03 --hang-cuoi 12824`). Ảnh CŨ GIỮ làm biên bản (Đ2): manifest 20/11 `itl_ledge_cac_ky.json` + 25 ảnh
#    `itl_ledge_<kỳ>.json` + ảnh sổ xlsx `tests/fixture/itl_ledge_2026_03.json`. Kỳ nào đóng băng lại ra checksum BẰNG ảnh
#    20/11 thì ⛔ có tệp `_20261123` (≡ — ⛔ nhân đôi repo; manifest mới ghi checksum ấy) ⇒ đọc ảnh 20/11.
HAU_TO_SONG = "_20261123"
MANIFEST_KY = ANH_DAP_AN / f"itl_ledge_cac_ky{HAU_TO_SONG}.json"   # 26 kỳ · 12.722 dòng cột A (đo 23/11; 20/11: 12.633)


def _duong_anh_ky(ky: str) -> Path:
    """Ảnh của kỳ: ảnh nguồn sống `_20261123` nếu có; ⛔ thì ảnh 20/11 (checksum ≡ — xem manifest). 2026-03 nay CÓ ảnh
    sống ở `dap_an/` *(chủ 23/11 quyết — trước: ảnh CŨ chụp sổ xlsx ở `tests/fixture/`, `DT12-R1-05`, giữ làm biên bản)*."""
    moi = ANH_DAP_AN / f"itl_ledge_{ky}{HAU_TO_SONG}.json"
    if moi.exists():
        return moi
    return FX / "itl_ledge_2026_03.json" if ky == "2026-03" else ANH_DAP_AN / f"itl_ledge_{ky}.json"


def do_tu_sinh_ky(d: dict, ky: str) -> dict:
    """Đo chế độ TỰ SINH trên MỘT ảnh kỳ (`d` đã nạp). Mọi phép so ô qua `_chuan` (⛔ so KIỂU — `DT12-R2-02`).
    Ra: `o` · `hd` · `mid` = (khớp, tổng) — tổng đếm Ô (⛔ dòng) 7 khối ⛔ có mã lỗi Sheets ở Cls/MID/Final;
    `lech_final` · `lech_mid` = lệch theo KHỐI (lớp có tên); `o_loi` = ô bỏ vì mã lỗi (`#N/A ()`… giữ nguyên chuỗi)."""
    from fls.ledger.final_rule import tinh_mid
    if d.get("ky") != ky or len(d["dong"]) != d["so_dong"]:
        raise ValueError(f"ảnh khai ky={d.get('ky')} so_dong={d.get('so_dong')} ≠ {ky}/{len(d['dong'])} dòng thật")
    tong = khop = hd_t = hd_k = mid_k = o_loi = 0
    lech_final: Counter = Counter()
    lech_mid: Counter = Counter()
    for r in d["dong"]:
        for k in KHOI:
            cls, man, mid, fin = (r[f"{k}_{c}"] for c in ("classifying", "manual", "mid", "final"))
            if any(la_o_loi(_chuan(v)) for v in (cls, mid, fin) if v is not None):
                o_loi += 1
                continue
            m2 = tinh_mid(_chuan(cls) or None, _chuan(man) or None, MAC_DINH_THEO_KHOI[k])
            f2 = tinh_final(_chuan(cls) or None, m2)
            tong += 1
            ok = _chuan(f2) == _chuan(fin)
            khop += ok
            if not ok:
                lech_final[k] += 1
            if _chuan(m2) == _chuan(mid):
                mid_k += 1
            else:
                lech_mid[k] += 1
            if k == "hd":
                hd_t, hd_k = hd_t + 1, hd_k + ok
    return {"ky": ky, "so_dong": len(d["dong"]), "o": (khop, tong), "hd": (hd_k, hd_t), "mid": (mid_k, tong),
            "lech_final": dict(lech_final), "lech_mid": dict(lech_mid), "o_loi": o_loi}


def do_tu_sinh_theo_ky(manifest: Path | None = None, duong_anh=None) -> dict:
    """H15 · Step 43: lặp chế độ TỰ SINH theo MỌI kỳ có ảnh (26). Kỳ ⛔ có ảnh / ảnh hỏng ⇒ `chua_do` CÓ TÊN
    (⛔ "đạt"). `ky_kham` rỗng (manifest hỏng/0 kỳ) ⇒ `loi` — Đ3, ⛔ xanh trên tập rỗng."""
    manifest = manifest or MANIFEST_KY
    duong_anh = duong_anh or _duong_anh_ky
    loi: list[str] = []
    try:
        cac_ky = sorted(json.loads(manifest.read_text(encoding="utf-8"))["dong_theo_ky_o_cot_A"])
    except (OSError, ValueError, KeyError) as e:
        cac_ky = []
        loi.append(f"manifest DT12 {_duong(manifest)}: ⛔ đọc được — {type(e).__name__}")
    theo_ky: dict = {}
    chua_do: dict = {}
    for ky in cac_ky:
        p = duong_anh(ky)
        try:
            theo_ky[ky] = do_tu_sinh_ky(json.loads(p.read_text(encoding="utf-8")), ky)
        except FileNotFoundError:
            chua_do[ky] = f"⛔ có ảnh {_duong(p)}"
        except (OSError, ValueError, KeyError, TypeError) as e:
            chua_do[ky] = f"ảnh hỏng {_duong(p)}: {type(e).__name__}: " + " ".join(str(e).split())[:120]
    if not cac_ky:
        loi.append("DT12 cho 0 kỳ (⛔ đo trên tập rỗng)")
    tong = {c: [sum(x[c][i] for x in theo_ky.values()) for i in (0, 1)] for c in ("o", "hd", "mid")}
    return {"so_ky_co_anh": len(cac_ky), "theo_ky": theo_ky, "chua_do": chua_do, "tong": tong,
            "loi": loi,
            "moc_so": {k: _moc_so(k) for k in theo_ky}}


def _moc_so(ky: str) -> str:
    """Nhãn mốc của số (Đ4): ảnh nguồn sống 23/11, hay ảnh 20/11 mà đóng băng lại 23/11 ra checksum ≡."""
    p = _duong_anh_ky(ky)
    if p.name.endswith(f"{HAU_TO_SONG}.json"):
        return "23/11 (nguồn sống — ảnh _20261123; chủ quyết nguồn sống là chuẩn)"
    if p.parent == FX:
        return "mốc CŨ (ảnh chụp sổ xlsx — ⛔ có ảnh sống)"
    return "23/11 ≡ 20/11 (đóng băng lại ra checksum BẰNG ảnh 20/11 — đọc ảnh 20/11)"


def do_tu_sinh() -> dict:
    """Tương thích ngược (2026-03 — HD 584/584): lát cắt kỳ 2026-03 của `do_tu_sinh_theo_ky`.
    MID_fls = tinh_mid(Classifying, Manual, mặc định khối) → Final_fls = tinh_final(Classifying, MID_fls), so Final sổ.
    ⛔ đọc MID của sổ — đây mới là phép đo "FLS tự mapping ra đúng quá khứ"."""
    x = do_tu_sinh_ky(json.loads(_duong_anh_ky("2026-03").read_text(encoding="utf-8")), "2026-03")
    return {k: x[k] for k in ("ky", "o", "hd", "mid")}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ghi", action="store_true")
    a = ap.parse_args()
    kq = do()
    print(f"{'kỳ':8s} {'có':>6s} {'chạy':>6s} {'mapNOW':>7s} {'mapFLS':>7s} {'ô gõ':>6s} {'ô mđ':>6s} {'trống':>6s} {'đè':>4s} {'parity':>13s}")
    for k in kq["ky"]:
        x = kq["theo_ky"][k]
        print(f"{k:8s} {x.get('co',0):6d} {x.get('chay',0):6d} {x.get('map_now',0):7d} {x.get('map_fls',0):7d} "
              f"{x.get('o_go_that',0):6d} {x.get('o_mac_dinh',0):6d} {x.get('o_trong',0):6d} {x.get('o_de',0):4d} "
              f"{x.get('o_parity_khop',0):6d}/{x.get('o_parity',0):<6d}")
    t = kq["tong"]
    print(f"{'Σ':8s} {t['co']:6d} {t['chay']:6d} {t['map_now']:7d} {t['map_fls']:7d} "
          f"{t['o_go_that']:6d} {t['o_mac_dinh']:6d} {t['o_trong']:6d} {t['o_de']:4d} {t['o_parity_khop']:6d}/{t['o_parity']}")
    print("PM:", kq["pm_tong"], "· bank:", kq["bank_tong"])
    # HD1 theo kỳ — Đ3: MẪU SỐ in TRƯỚC mọi tỷ lệ; Đ4: mỗi số mang nhãn NÓ ĐẾM GÌ. Năm dòng ①…⑤ — bài CLI
    # đòi ĐỦ cả năm, mỗi dòng một lần (H2-R1-04: R1-M17/M18 bỏ `②`/`④` mà bộ R1 vẫn xanh).
    h, ms, d = kq["dat_hd1"], kq["dat_hd1"]["mau_so"], kq["dat_hd1"]["dem"]
    print(f"HD1 · ① MẪU SỐ: {ms['so_ky']} kỳ · {ms['dong_so']} dòng sổ · {ms['dong_thieu']} dòng thiếu (sổ ⛔ ghép 1-1) "
          f"· {ms['dong_tu_soi_loai']} dòng tự-soi loại · {ms['o_moi_dong']} ô Final trên MỌI dòng "
          f"· tệp nhãn DT1b {h['tep_nhan']['duong']}: {'có' if h['tep_nhan']['co'] else 'VẮNG'} "
          f"· sổ lý do {h['so_ly_do']}: {h['so_chu_ky']} chữ ký "
          f"· ⛔ xét {h['ngoai_phan']['dong_fls_khong_co_dong_so']} dòng FLS ⛔ có dòng sổ (chiều ngược — ảnh ⛔ có ngày)")
    print(f"HD1 · ② dòng thiếu có nhãn {d['co_nhan']}/{d['thieu']} · có nhãn ĐÃ KÝ {d['da_ky']}/{d['thieu']} "
          f"· dòng tự-soi loại có nhãn {d['loai_co_nhan']}/{d['loai_tu_soi']} · có nhãn ĐÃ KÝ "
          f"{d['loai_da_ky']}/{d['loai_tu_soi']}")
    print(f"HD1 · ③ kỳ đạt ([dòng] 1-1 100 % hoặc mọi dòng thiếu có nhãn ĐÃ KÝ — ∧ [ô] Final 7 khối khớp trên MỌI dòng "
          f"hoặc mọi dòng tự-soi loại có nhãn ĐÃ KÝ): {h['so_ky_dat']}/{ms['so_ky']} · " + (" · ".join(h["ky_dat"]) or "—"))
    do_ = [k for k in kq["ky"] if not h["theo_ky"][k]["dat"]]

    def _ky_do(k: str) -> str:
        y = h["theo_ky"][k]
        s = f"{k} {y['thieu']}·{y['co_nhan']}·{y['da_ky']}"
        if y["loai_tu_soi"]:                   # H2-R1-01 ⓑ — người ký phải THẤY dòng tự-soi loại của kỳ
            s += f" loại {y['loai_tu_soi']}·{y['loai_co_nhan']}·{y['loai_da_ky']}"
        if not y["o_100"]:
            s += f" ô {y['o_moi_dong_khop']}/{y['o_moi_dong']}"
        return s

    print(f"HD1 · ④ kỳ đỏ {len(do_)}/{ms['so_ky']} (dòng thiếu·có nhãn·đã ký [· loại: dòng tự-soi loại·có nhãn·đã ký]"
          f" [· ô khớp/ô trên MỌI dòng khi vế ô đỏ]): " + (" · ".join(_ky_do(k) for k in do_) or "—"))
    print("HD1 · ⑤ nhãn để ký (nhãn · so_dong · van_tay_dong — CHÉP NGUYÊN vào chữ ký; ⛔ ký KHAC): "
          + (" · ".join(f"{n} {x['so_dong']} {x['van_tay_dong']}"
                        + (" ĐÃ KÝ" if x["da_ky"] else "") + (" ⛔ ký được" if x["cam_ky"] else "")
                        for n, x in h["theo_nhan"].items()) or "— (0 nhãn)"))
    if a.ghi:
        # tệp tạm + os.replace (`DT1a-R1-07`): đứt giữa chừng ⛔ để lại voi_so_luong.json cụt — và ⛔ để lại
        # rác `.tam` hiện ở `git status` (H2-R1-03: bài mô phỏng đứt giữa lúc ghi canh cả hai)
        tam = RA.with_name(RA.name + ".tam")
        try:
            tam.write_text(json.dumps(kq, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tam, RA)
        except BaseException:
            tam.unlink(missing_ok=True)
            raise
        print("✅ đã ghi", _duong(RA))


if __name__ == "__main__":
    main()
