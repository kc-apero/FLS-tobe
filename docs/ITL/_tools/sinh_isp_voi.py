#!/usr/bin/env python3
"""Sinh `IncrementalStepPlan-FLS-Voi_v3.1.2.md` — ISP của AP Voi FLS v3.1.2 (build-isp).

⚠ Bản ISP v3.1.1 đóng băng (§A.16) — bộ sinh của nó là chính tệp này ở commit `0980f84`.
v3.1.2 = so sánh mã ↔ ISP (người dùng chọn A) + luật *"agent FE nhận bước BE"*.

⭐ Vì sao SINH, ⛔ viết tay: 51 bước × 8 trường × 2 substep. Viết tay thì một bước thiếu
trường, một cạnh phụ thuộc trỏ vào bước không có, hay hai làn cùng ghi một tệp — đều
⛔ ai thấy. Bộ sinh này KIỂM trước khi ghi (cổng ở `kiem()`), và ĐỎ khi:
  · bước thiếu trường bắt buộc, hoặc thiếu test BE lẫn FE (FE N/A phải có lý do);
  · phụ thuộc trỏ tới bước không có, hoặc DAG có chu trình;
  · ước lượng trên vượt nửa ngày (4 giờ);
  · một tệp/thư mục thuộc hai làn (trừ chỗ khai tuần tự hoá);
  · AP ghim không đúng sha256 đã khai (`AP_SHA`).
Lịch wave tính bằng máy (list scheduling, mỗi làn một việc một lúc, một ô = nửa ngày).

⛔ Tệp này ⛔ viết mã sản phẩm. Nó chỉ sinh tài liệu kế hoạch.
"""
from __future__ import annotations

import fnmatch
import hashlib
import re
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[3]
AP = GOC / "docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html"
RA = GOC / "docs/ITL/02_BA/Artifacts/IncrementalStepPlan-FLS-Voi_v3.1.2.md"
AP_SHA = "5cf6e576ff46f0886eb4a6b6cbefbcbd4f905a7835f843a2bfdb94d8a90982ba"
NGAY = "2026-11-16"

# ───────────────────────── làn, chủ sở hữu tệp ─────────────────────────
LAN = {
    "BE-CF": dict(ten="Backend · config", agent="fls-dev #CF",
                  so_huu=["fls/cau_hinh/**", "fls/repo/cau_hinh_repo.py", "fls/api/bang_tuyen.py", "fls/api/xu_ly.py",
                          "fls/repo/doc_bao_cao.py (chỉ `doc_cong` · `_CHUA_DO_DUOC`)", "fls/db/migrations/0027_*.sql", "fls/db/schema.py (chỉ phần 0027)",
                          "tests/cau_hinh/**", "tests/api/test_isp_*.py", "tools/soi_bang_tuyen.py"]),
    "BE-HC": dict(ten="Backend · hard code (engine)", agent="fls-dev #HC",
                  so_huu=["fls/bao_cao/**", "fls/ledger/**", "fls/oracle/**", "fls/adapters/**",
                          "tools/do_voi_so_luong.py", "tools/do_hd2.py", "docs/ITL/_tools/voi_so_luong.json",
                          "docs/ITL/_tools/hd2_cong.json", "tests/bao_cao/**", "tests/ledger/**", "tests/oracle/**", "tests/tich_hop/test_hd2_*.py"]),
    "FE": dict(ten="Frontend", agent="fls-dev #FE",
               so_huu=["fls/web/tep/**", "fls/web/phuc_vu.py", "tests/web/test_isp_*.py"]),
    "DATA": dict(ten="Data", agent="fls-dev #DATA",
                 so_huu=["tests/fixture/cau_hinh/**", "tests/fixture/dap_an/**", "tests/du_lieu/**",
                         "tools/dong_bang_sheet.py", "tools/phan_loai_dong_thieu.py",
                         "docs/ITL/_tools/phan_loai_dong_thieu.json", "tests/tich_hop/test_hd1_*.py"]),
}
# Tệp dùng chung — chỉ MỘT bước được chạm, đã khai ở bước ấy (tuần tự hoá, skill build-isp §3).
DUNG_CHUNG = {".importlinter": "S0", "pyproject.toml": "S0", "requirements.txt": "S0",
              "tools/dung_moi_truong_isp.sh": "S0", "fls/bao_cao/__init__.py": "S0",
              "docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md": "S0",
              "docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md §5": "mọi bước — chỉ THÊM một dòng (hợp đồng agent §1)"}

# ───────────────────────── lệnh chạy (Step 0 xác minh) ─────────────────────────
ENV = "export PG_DSN='postgresql://fls:fls@localhost:5433/fls' PYTHONUTF8=1"
LENH_CHUNG = [".venv/bin/lint-imports", "python -m fls.db.pg_migrate", "python tools/kiem_so_song.py"]


def be(*ids: str) -> str:
    return f"`.venv/bin/python -m pytest {' '.join(ids)}`"


# ───────────────────────── 51 bước ─────────────────────────
# Mỗi bước: id · lan · ten · goal · ap · est(lo, hi, tin) · deps
#   gom · loai · moi (khái niệm mới duy nhất) · mock · gioi_han
#   tp {FE, BE, DB, TH}  · tien_de · tb [(id, làm gì, mong, loại, vì sao đỏ trước)] · tf (list hoặc "N/A — lý do")
#   hv (hiện vật) · ex (exit) · lam (implementation dự kiến) · tep (tệp chạm) · chay (lệnh)
B: list[dict] = []


def step(**k):
    B.append(k)


NA_FE_TOOL = "N/A — lát cắt là lệnh/cổng (đường vào = CLI, đầu ra = JSON + exit code); ⛔ dựng UI giả (skill build-isp §2)."
NA_FE_DATA = "N/A — bước dữ liệu: đầu ra là ảnh đóng băng + cổng kiểm; người dùng thấy qua cổng (exit code) và bước BE/FE tiêu thụ."
NA_FE_API = "N/A — bước mở tuyến API; màn tiêu thụ tuyến này ở bước FE riêng (nêu ở Phụ thuộc kế tiếp)."

# ═════════════ Step 0 ═════════════
step(id="S0", lan="BE-CF", ten="Môi trường test + đường nền cổng + khung hai gói mới",
     goal="Một lệnh dựng được môi trường và in đường nền: số bài pytest đỏ/xanh, 26 di trú áp đủ, lint-imports 11 hợp đồng giữ, cổng HD1 in 9.845/9.967.",
     ap="AP v3.1.2 §1.3.3 (luật agent lấy từ CLAUDE.md) · §5.3.1 HD5 (lặp lại được) · CLAUDE.md §Cổng",
     est=(2, 3, "trung bình — đo 16/11: container có PostgreSQL 16 (`/usr/lib/postgresql/16/bin`), node 22, PyPI vào được; ⛔ Docker, ⛔ pytest"),
     deps=[],
     gom=["⭐ tái dùng: `fls/db/kho.py` tự tạo/dựng lại kho test (`tao_kho_test` · `dung_lai_kho_test`, biến `PG_DSN_TEST`) qua fixture autouse ở `tests/conftest.py` ⇒ S0 chỉ dựng cụm + role `fls` có quyền tạo kho", "venv `.venv` + `requirements.txt` (psycopg · pytest · import-linter)",
          "cụm PostgreSQL 16 cục bộ cổng 5433, user/kho `fls` (⛔ `docker compose down` — ở container ⛔ có Docker; trên máy owner vẫn `docker start fls-pg-1`)",
          "chạy đường nền mọi cổng ở CLAUDE.md, GHI kết quả THẬT (kể cả bài đỏ có sẵn) vào `docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md`",
          "tạo hai gói rỗng có hợp đồng tầng: `fls/cau_hinh` (config thuần, ⛔ DB) · `fls/bao_cao` (engine báo cáo/phân bổ thuần, ⛔ DB) — để hai làn BE ⛔ cùng sửa `.importlinter` về sau"],
     loai=["sửa bất kỳ bài đỏ có sẵn nào (ghi vào DUONG_NEN, chuyển orchestrator)", "dữ liệu thật vào kho (`FLS_CHO_GHI_THAT` ⛔ đặt)"],
     moi="môi trường test của ISP (hạ tầng chạy)", mock="không",
     gioi_han=["kho test là cụm cục bộ, ⛔ phải `fls-pg-1` của owner — bước tích hợp cuối chạy lại trên máy owner (O4)"],
     tp=dict(FE="N/A — chưa có màn mới; chỉ chạy bộ test web sẵn có để lấy đường nền.",
             BE="`fls/cau_hinh/__init__.py`, `fls/bao_cao/__init__.py` (rỗng, có docstring vai)",
             DB="cụm PG16 cục bộ :5433 · `python -m fls.db.pg_migrate` → 0001…0026",
             TH="`.importlinter` +2 hợp đồng (cau_hinh, bao_cao ⛔ psycopg/fls.repo/fls.db)"),
     tien_de=["người dùng duyệt ISP 3.1.2", "O4 chốt nơi chạy (khuyến nghị: container này)"],
     tb=[("S0-B1", "chạy `python -m pytest` lần đầu", "có dòng tổng kết `N passed` (mẫu số: grep đếm 2.044 hàm `def test_`, ⛔ phải số pytest thu thập); mọi bài đỏ được liệt kê tên trong DUONG_NEN (⛔ con số trần)", "toàn bộ", "chưa có pytest ⇒ hôm nay ⛔ chạy được"),
         ("S0-B2", "`python -m fls.db.pg_migrate`", "26/26 di trú áp; `pg_verify` exit 0", "tích hợp DB", "chưa có cụm PG"),
         ("S0-B3", "`lint-imports`", "11 hợp đồng giữ (9 cũ + 2 mới); phá thử: `import psycopg` trong `fls/bao_cao` ⇒ ĐỎ, gỡ ⇒ xanh (Đ5)", "kiến trúc", "hai hợp đồng mới chưa có"),
         ("S0-B4", "`python tools/do_voi_so_luong.py`", "exit 0; in `chay 9845 / co 9967` (đúng `MONG`)", "cổng dữ liệu", "chưa chạy ở môi trường mới")],
     tf=[("S0-F1", "chạy `python -m pytest tests/web` (node headless qua `khung_node.py`)", "dòng tổng kết có; bài đỏ ghi tên", "web headless", "node chưa được bộ test gọi ở container")],
     hv=["`docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md` (số đo + lệnh + exit code)", "2 gói rỗng + 2 hợp đồng tầng", "script dựng `tools/dung_moi_truong_isp.sh`"],
     ex=["S0-B1…B4, S0-F1 chạy được và kết quả THẬT được ghi (bài đỏ có sẵn ≠ lỗi bước này)", "phép phá thử S0-B3 đã thấy ĐỎ rồi trả nguyên", "3 vòng review xong"],
     lam="script dựng môi trường + 2 `__init__.py` + 2 khối hợp đồng `.importlinter`; ⛔ đụng mã nghiệp vụ.",
     tep=["tools/dung_moi_truong_isp.sh", ".importlinter", "fls/cau_hinh/__init__.py", "fls/bao_cao/__init__.py", "docs/ITL/03_Dev/isp-3.1/DUONG_NEN.md"],
     chay=["bash tools/dung_moi_truong_isp.sh", ENV, be(""), ".venv/bin/lint-imports", "python -m fls.db.pg_migrate", "python tools/do_voi_so_luong.py"])

# ═════════════ DATA ═════════════
step(id="DT1a", lan="DATA", ten="HD1 · kiểm kê 122 dòng sổ chưa 1-1 (offline, trên ảnh đóng băng)",
     goal="Một lệnh liệt kê đúng 122 dòng sổ AS-IS chưa ghép 1-1 và 147 dòng FLS chưa có dòng sổ, kèm thuộc tính đo được (kỳ · hd Classifying/MID/Final · pay_type · cdt1), và cổng đỏ khi tổng khác 122 / 147.",
     ap="AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10 · §2.5.3 · Figure 2.2 hàng BANK",
     est=(2, 3, "cao — chính phép này đã chạy tay 16/11: 122 dòng · 18/23 kỳ · 121/122 `hd_classifying = Need to manual input` · hd Final OGA 74 · GI 25 · DEP 8 · ITE 7 · khác 8"),
     deps=["S0"],
     gom=["tool `tools/phan_loai_dong_thieu.py`: tập thiếu = `dong_sheet` của `itl_ledge_adjustment.json` ∖ `dong_so` của `classifying_vs_canon.json`",
          "chiều ngược: 9.992 dòng canon − 9.845 dòng ghép = 147 dòng FLS ⛔ có dòng sổ (chỉ ĐẾM)",
          "ghi `docs/ITL/_tools/phan_loai_dong_thieu.json` theo `dong_sheet`, trường `nhan = null` (DT1b điền)"],
     loai=["nhãn LÝ DO (cần khoá — DT1b)", "sửa mã ghép (H3)", "ký lý do (O8)"],
     moi="kiểm kê tập lệch có cổng", mock="không — ảnh đóng băng thật đã có trong repo",
     gioi_han=["⛔ gán được LÝ DO: ảnh đã bỏ Số CT · TK · tiền (riêng tư), và mã ghép đã tạo ra 9.845 ⛔ có trong repo (fixture ghi 'đọc LIVE 2026-08-26') — DT1b"],
     tp=dict(FE=NA_FE_DATA, BE="`tools/phan_loai_dong_thieu.py` (đọc fixture, ⛔ ghi kho)", DB="không", TH="không"),
     tien_de=["S0 xong (pytest chạy được)", "ba checksum fixture khớp `MONG` của `do_voi_so_luong.py`"],
     tb=[("DT1a-B1", "chạy tool trên 3 fixture", "122 dòng; 147 chiều ngược; phân bố kỳ có MONG (2026-07: 23 · 2025-11: 14 · 2026-08: 13 …)", "đơn vị + cổng", "tool chưa có"),
         ("DT1a-B2", "phá nguồn: bỏ 1 dòng khỏi tập ghép (bản sao tạm)", "cổng ĐỎ (123 ≠ 122) rồi trả nguyên (Đ5)", "chứng minh đỏ", "—"),
         ("DT1a-B3", "mẫu số (Đ3)", "in 9.967 dòng sổ và 9.845 dòng ghép trước khi in tỷ lệ", "đơn vị", "—"),
         ("DT1a-B4", "quét PII trên JSON ra", "0 khoá `dien_giai` / `so_chung_tu` / `email`", "riêng tư", "—")],
     tf=NA_FE_DATA,
     hv=["`phan_loai_dong_thieu.json` (122 + 147 dòng, thuộc tính, `nhan = null`)"],
     ex=["DT1a-B1…B4 đúng; DT1a-B2 đã thấy đỏ", "MONG khai trong tool (Đ5)", "3 vòng review xong"],
     lam="một module tool + bài test.",
     tep=["tools/phan_loai_dong_thieu.py", "tests/du_lieu/test_phan_loai_dong_thieu.py", "docs/ITL/_tools/phan_loai_dong_thieu.json"],
     chay=[be("tests/du_lieu/test_phan_loai_dong_thieu.py"), "python tools/phan_loai_dong_thieu.py --ghi"])

step(id="DT1b", lan="DATA", ten="HD1 · gán lý do cho 122 dòng bằng khoá đọc ở nguồn (khoá băm, ⛔ commit giá trị)",
     goal="Mỗi dòng trong 122 dòng mang đúng một nhãn `KHONG_CO_SAO_KE` · `KHOA_LECH` · `TRUNG_SEQ` · `KHAC` tính từ khoá (Số CT, PS Nợ, PS Có, TK, tiền tệ) đọc ở nguồn, và cổng đỏ khi một dòng có 0/≥2 nhãn hoặc Σ ≠ 122.",
     ap="AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10 · §4.3.1 SI.MAP",
     est=(3, 4, "thấp — phụ thuộc chỗ đọc được cột khoá (O10)"),
     deps=["DT1a"],
     gom=["chế độ `--khoa <bản đọc>` của tool DT1a: nhận cột khoá của sổ AS-IS + `Transaction Mapping L1` (RAW `1md85t…`, khai ở `fls/oracle/nguon.py`)",
          "chuẩn hoá đúng như ghi chú của fixture: PS Nợ/Có là CHUỖI có dấu phân cách, Số CT dài bị về dạng khoa học (`4.36619E+15`) — thiếu bước này tỷ lệ ghép rơi từ 98,8% còn 16,6%",
          "khoá ra tệp chỉ dưới dạng băm sha256 16 ký tự; ⛔ Số CT, ⛔ Diễn giải trong repo",
          "điền `nhan` trong `phan_loai_dong_thieu.json` + bảng đếm nhãn × kỳ"],
     loai=["sửa mã ghép (H3)", "ghi kho"], moi="ghép lại theo khoá để phân loại lý do", mock="không",
     gioi_han=["⛔ dùng NGÀY làm khoá (ngày của bản xlsx hỏng — đúng như phép ghép gốc)", "nếu cột khoá chỉ có ở `Input_Raw/[Master] ITL_Ledge_raw.xlsx` trên máy owner thì bước chạy ở đó (O10)"],
     tp=dict(FE=NA_FE_DATA, BE="`tools/phan_loai_dong_thieu.py` (+ chế độ `--khoa`)", DB="không", TH="Google Sheets RAW qua orchestrator, hoặc tệp xlsx trên máy owner (O10)"),
     tien_de=["DT1a", "O10 (nơi đọc cột khoá)", "O7"],
     tb=[("DT1b-B1", "chạy `--khoa` trên bản đọc", "Σ nhãn = 122; mỗi dòng đúng 1 nhãn; bảng đếm nhãn có MONG", "cổng", "chế độ chưa có"),
         ("DT1b-B2", "Số CT dạng `4.36619E+15` và tiền '2,730,128.00' (tổng hợp)", "chuẩn hoá trước khi băm; khớp bản số thường", "đơn vị", "—"),
         ("DT1b-B3", "quét tệp ra", "0 Số CT thô · 0 Diễn giải", "riêng tư", "—"),
         ("DT1b-B4", "phá: gán 2 nhãn cho 1 dòng (bản sao)", "ĐỎ rồi trả nguyên", "chứng minh đỏ", "—")],
     tf=NA_FE_DATA,
     hv=["`phan_loai_dong_thieu.json` có `nhan`", "bảng nhãn × kỳ dán vào BG"],
     ex=["DT1b-B1…B4 đúng", "3 vòng review xong"],
     lam="thêm chế độ `--khoa` vào tool DT1a.",
     tep=["tools/phan_loai_dong_thieu.py", "tests/du_lieu/test_phan_loai_ly_do.py", "docs/ITL/_tools/phan_loai_dong_thieu.json"],
     chay=[be("tests/du_lieu/test_phan_loai_ly_do.py"), "python tools/phan_loai_dong_thieu.py --khoa <bản_đọc> --ghi"])

step(id="DT2", lan="DATA", ten="Đường ống đóng băng sheet + ảnh IX.FX (9.2 Exchange Rate)",
     goal="Một lệnh biến bản đọc giá trị sheet thành ảnh đóng băng có checksum và cổng; ảnh IX.FX ra đúng 37 dòng 202401→202612 kể cả dòng lạc 202306.",
     ap="AP v3.1.2 §3.2.1 IX.FX · §3.2.4 (bảng tỷ giá gõ cứng) · §3.5.3 D1",
     est=(2, 3, "cao — ⭐ lõi đã có: `fls/oracle/anh_chup.AnhChup` · `doc.doc_dan` · `doc_du` · `tools/do_kha_nang_doc.py`; khuôn tệp theo `pm_join.json`"),
     deps=["S0"],
     gom=["⭐ tái dùng, ⛔ viết lại: `AnhChup` (checksum nội dung, độc lập thứ tự, từ chối ảnh rỗng) · `doc.doc_dan` (đọc dần, retry, một khối lỗi ⛔ phá cả lượt) · `doc_du` (đọc lại cột then chốt — chặn IMPORTRANGE trả ô rỗng im lặng) · `PM_COT_RIENG_TU`", "thử đọc trước từng workbook bằng `tools/do_kha_nang_doc.py` — `GAP-ORA-08`: sổ ADJUSTED ⛔ trả giá trị qua API, chỉ `FORMULA`", "`tools/dong_bang_sheet.py`: vào = JSON giá trị đọc từ Drive (orchestrator lấy, O7), ra = `tests/fixture/cau_hinh/ix_fx.json` có `nguon`, `ngay_dong_bang`, `khong_mang_PII`, `checksum_noi_dung`",
          "cổng: 37 dòng · khoá `yyyymm` · 5 tiền tệ (USD · SGD · COP · VND = 1 · HKD) · liệt kê tháng trùng/thiếu/lạc (⛔ sửa — ghi đúng như nguồn)"],
     loai=["kiểm nghiệp vụ tỷ giá (BE-CF · C1)", "đọc Drive trực tiếp từ agent (O7)"],
     moi="đường ống đóng băng sheet → fixture có checksum", mock="không",
     gioi_han=["ảnh là của MỘT ngày đọc; tháng mới cần lượt đóng băng mới (HD5 ngoài bước này)"],
     tp=dict(FE=NA_FE_DATA, BE="`tools/dong_bang_sheet.py`", DB="không", TH="Google Sheets (đọc, qua orchestrator — O7)"),
     tien_de=["S0", "O7 chốt cách lấy dữ liệu Drive", "bản đọc thô nằm ở scratchpad orchestrator, ⛔ commit"],
     tb=[("DT2-B1", "đóng băng từ bản đọc thô", "37 dòng; checksum ổn định qua 2 lần chạy (tất định)", "đơn vị", "tool chưa có"),
         ("DT2-B2", "bản thô có cột `Email Address` giả lập", "tool ĐỎ, ⛔ ghi tệp (PM_COT_RIENG_TU)", "riêng tư", "—"),
         ("DT2-B3", "bản thô thiếu 1 tháng", "ảnh vẫn ghi đúng nguồn + cổng in `thiếu: [yyyymm]` và exit ≠ 0 khi `--mong 37` lệch", "cổng", "—")],
     tf=NA_FE_DATA,
     hv=["`tests/fixture/cau_hinh/ix_fx.json`", "`tools/dong_bang_sheet.py`"],
     ex=["DT2-B1…B3 xanh; cổng đã thấy đỏ", "ảnh ⛔ mang khoá PII (quét = 0)", "3 vòng review xong"],
     lam="tool đóng băng tổng quát (cột chọn + khoá + checksum) dùng lại ở DT3…DT11.",
     tep=["tools/dong_bang_sheet.py", "tests/du_lieu/test_dong_bang_sheet.py", "tests/fixture/cau_hinh/ix_fx.json"],
     chay=[be("tests/du_lieu/test_dong_bang_sheet.py"), "python tools/dong_bang_sheet.py ix_fx <bản_thô.json> --mong 37"])

step(id="DT3", lan="DATA", ten="Ảnh nguồn IX.HD · IX.ORG: cây ATL 74 dòng + Mapping Master + CDT Correct",
     goal="Ba ảnh đóng băng mới nạp được và cổng khẳng định: cây ATL 74 dòng · 6 nhóm, Mapping Master 73 mã hd, CDT Correct 18 dòng.",
     ap="AP v3.1.2 §3.2.1 IX.HD · IX.ORG · §3.2.5 cây HD · §3.5.4 WP-C1",
     est=(2, 3, "cao — phần Mapping Master đọc bằng `fls/adapters/mapping_master.py` sẵn có (header dòng 3, dữ liệu từ dòng 7, 73 mã — đo 28/08)"),
     deps=["DT2"],
     gom=["`tests/fixture/cau_hinh/atl_cay.json` (mã · tên · cha · cấp · nhóm)", "`mapping_master_cfg.json` (A:B · AA:AD · D:L) — đóng băng ĐẦU RA của `mapping_master.doc_cot` (⛔ khuôn đọc thứ hai)", "`cdt_correct.json` (BR11:BS28)"],
     loai=["kiểm cha–con, chu trình (BE-CF · C4)"], moi="không (dùng lại đường ống DT2)", mock="không",
     gioi_han=["hai định nghĩa dòng PL (ATL ↔ Mapping Master) được đóng băng NGUYÊN, ⛔ hoà giải — C12 xử"],
     tp=dict(FE=NA_FE_DATA, BE="`tools/dong_bang_sheet.py` (khuôn mới)", DB="không", TH="Google Sheets qua orchestrator"),
     tien_de=["DT2 xong"],
     tb=[("DT3-B1", "đóng băng 3 nguồn", "74 · 73 · 18 dòng đúng MONG; 6 nhóm", "cổng", "ảnh chưa có"),
         ("DT3-B2", "phá: xoá 1 dòng cây ở bản sao", "ĐỎ 73 ≠ 74, trả nguyên", "chứng minh đỏ", "—")],
     tf=NA_FE_DATA, hv=["3 ảnh trong `tests/fixture/cau_hinh/`"],
     ex=["DT3-B1, DT3-B2 xanh/đỏ đúng", "3 vòng review xong"],
     lam="3 khuôn cột cho tool + 1 bài test.", tep=["tests/fixture/cau_hinh/*.json", "tests/du_lieu/test_anh_cau_hinh.py"],
     chay=[be("tests/du_lieu/test_anh_cau_hinh.py")])

step(id="DT4", lan="DATA", ten="Ảnh đáp án 406 · Report I General Ledger CALC ZONE (BM–BT)",
     goal="Đáp án 406 đóng băng theo dòng × kỳ cho cột BM–BT, bỏ Diễn giải/Số CT, cổng khẳng định số dòng mỗi kỳ bằng số dòng sổ cùng kỳ.",
     ap="AP v3.1.2 §3.3.1 PD 406 · §3.5.4 WP-C2 · HD2",
     est=(3, 4, "thấp–trung bình — bảng lớn (cỡ 10⁴ dòng); rủi ro hết giờ đọc (GAP-ORA-08) ⇒ đọc theo lát kỳ"),
     deps=["DT2"],
     gom=["`tests/fixture/dap_an/gl_406.json`: khoá dòng (`dong_sheet`), kỳ, BM–BT (tiền theo 5 tiền tệ, bVND, mUSD)", "đọc theo lát kỳ; lát hỏng = ĐỎ (⛔ 'không thấy lệch')"],
     loai=["tính lại GL (BE-HC · H1/H4)"], moi="không", mock="không",
     gioi_han=["tồn luỹ kế AS-IS phụ thuộc thứ tự dòng (AP §3.3.1) — ảnh giữ NGUYÊN thứ tự dòng để H4 tái hiện"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"),
     tien_de=["DT2", "O7"],
     tb=[("DT4-B1", "đóng băng mọi lát kỳ", "Σ dòng theo kỳ = phân bố kỳ của `itl_ledge_adjustment.json` (hoặc lệch có tên)", "cổng", "ảnh chưa có"),
         ("DT4-B2", "một lát trả rỗng", "ĐỎ (Đ3: mẫu số 0 là kết quả)", "chứng minh đỏ", "—"),
         ("DT4-B3", "quét PII", "0 cột Diễn giải/Số CT", "riêng tư", "—")],
     tf=NA_FE_DATA, hv=["`gl_406.json`"], ex=["DT4-B1…B3 đúng", "3 vòng review xong"],
     lam="khuôn cột 406 + đọc theo lát.", tep=["tests/fixture/dap_an/gl_406.json", "tests/du_lieu/test_dap_an_406.py"],
     chay=[be("tests/du_lieu/test_dap_an_406.py")])

step(id="DT5", lan="DATA", ten="Ảnh đáp án 409–411 · CFA1 Daily + Y/H/Q/M",
     goal="Đáp án CFA1 theo (HD, ngày) và theo Y/H/Q/M đóng băng; cổng khẳng định mọi hàng có mã HD nằm trong cây ATL 74 dòng.",
     ap="AP v3.1.2 §3.3.1 PD 409–411 · §3.5.4 WP-C3", est=(3, 4, "trung bình"), deps=["DT3"],
     gom=["`dap_an/cfa1_daily.json` (HD × ngày)", "`dap_an/cfa1_yhqm.json` (HD × kỳ Y/H/Q/M)"],
     loai=["CFA3/PLA (D6a, D6b)"], moi="không", mock="không",
     gioi_han=["ô công thức lỗi ở nguồn (#REF!, #N/A) được ghi nguyên dạng chuỗi, ⛔ đổi thành 0"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT3 (cây để kiểm mã HD)"],
     tb=[("DT5-B1", "đóng băng", "mọi mã HD ∈ cây ATL; số cột ngày = số ngày từ 21/10/2024 tới ngày đọc", "cổng", "ảnh chưa có"),
         ("DT5-B2", "phá: đổi 1 mã HD lạ", "ĐỎ, trả nguyên", "chứng minh đỏ", "—")],
     tf=NA_FE_DATA, hv=["2 ảnh đáp án"], ex=["DT5-B1, B2 đúng", "3 vòng review xong"],
     lam="2 khuôn cột + test.", tep=["tests/fixture/dap_an/cfa1_*.json", "tests/du_lieu/test_dap_an_cfa1.py"],
     chay=[be("tests/du_lieu/test_dap_an_cfa1.py")])

step(id="DT6", lan="DATA", ten="Ảnh đáp án GL HR + CFA3 (407 · 408 · 412 · 413)",
     goal="Đáp án GL HR và CFA3 đóng băng; cổng khẳng định chỉ có kỳ của Y2025 (AS-IS chỉ có sheet Y2025) và in rõ điều đó.",
     ap="AP v3.1.2 §3.3.1 PD 401–404 · 407 · 408 · 412 · 413 · Q3 (HR ⛔ qua ALLOCATE)", est=(3, 4, "trung bình"), deps=["DT2"],
     gom=["`dap_an/gl_hr.json`", "`dap_an/cfa3.json`"], loai=["PLA1/PLA3 (DT7)"], moi="không", mock="không",
     gioi_han=["H1000 Y2024 đi bằng IMPORTRANGE — nếu đọc ⛔ được, ghi `thiếu Y2024` (⛔ suy)"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT2"],
     tb=[("DT6-B1", "đóng băng", "kỳ ⊂ 2025; số dòng theo kỳ có MONG", "cổng", "ảnh chưa có"),
         ("DT6-B2", "quét PII (HR có tên người)", "0 cột tên/email; chỉ mã nhân sự băm hoặc bỏ", "riêng tư", "—")],
     tf=NA_FE_DATA, hv=["2 ảnh"], ex=["DT6-B1, B2 đúng", "3 vòng review xong"],
     lam="2 khuôn cột + test.", tep=["tests/fixture/dap_an/gl_hr.json", "tests/fixture/dap_an/cfa3.json", "tests/du_lieu/test_dap_an_hr.py"],
     chay=[be("tests/du_lieu/test_dap_an_hr.py")])

step(id="DT7", lan="DATA", ten="Ảnh đáp án PLA1 · PLA3 HR · PLA3 PM+HR (414–419)",
     goal="Đáp án PLA đóng băng; cổng khẳng định PLA3 PM+HR = PLA1 + PLA3 HR từng ô ngay trên đáp án (nếu AS-IS lệch chính nó, liệt kê ô lệch).",
     ap="AP v3.1.2 §3.3.1 PD 414–419 · §3.5.3 D4", est=(3, 4, "trung bình"), deps=["DT2"],
     gom=["`dap_an/pla1.json`", "`dap_an/pla3_hr.json`", "`dap_an/pla3_pm_hr.json`"], loai=["engine PLA (H8)"], moi="không", mock="không",
     gioi_han=["phép tự kiểm cộng theo VỊ TRÍ ô (đúng như AS-IS) — lệch nào là của AS-IS, ⛔ của FLS"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT2"],
     tb=[("DT7-B1", "đóng băng + tự kiểm cộng", "số ô lệch của chính AS-IS có MONG (đo lần đầu rồi khai)", "cổng", "ảnh chưa có")],
     tf=NA_FE_DATA, hv=["3 ảnh"], ex=["DT7-B1 đúng + đã chứng minh đỏ", "3 vòng review xong"],
     lam="3 khuôn cột + test.", tep=["tests/fixture/dap_an/pla*.json", "tests/du_lieu/test_dap_an_pla.py"],
     chay=[be("tests/du_lieu/test_dap_an_pla.py")])

step(id="DT8", lan="DATA", ten="Ảnh IX.VEN Block 1 + đáp án MID1–MID3 của sổ GI",
     goal="Ảnh Vendor & Network Block 1 (36 dòng × 7 CDT1) và MID1–MID3 của GI đóng băng; cổng khẳng định Σ chia của MID3 = O / P trên chính đáp án.",
     ap="AP v3.1.2 §3.2.2 IX.VEN · §3.4.1 PD 503–507 · §3.5.4 WP-C4", est=(3, 4, "trung bình"), deps=["DT2"],
     gom=["`cau_hinh/ix_ven.json` (36 dòng, cột 'cách tính' cho VD341 · VD444 · VD428 · 'Max' · VD62)", "`dap_an/gi_mid1.json` · `gi_mid2.json` · `gi_mid3.json`"],
     loai=["OMC · SC · PS (DT9)"], moi="không", mock="không",
     gioi_han=["U3 #REF! ở nguồn được ghi nguyên"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT2"],
     tb=[("DT8-B1", "đóng băng", "36 dòng Block 1; 5 vendor có 'cách tính' ≠ thường", "cổng", "ảnh chưa có"),
         ("DT8-B2", "tự kiểm Σ chia MID3 = O/P", "số Vendor-tháng lệch có MONG", "cổng", "—")],
     tf=NA_FE_DATA, hv=["4 ảnh"], ex=["DT8-B1, B2 đúng + chứng minh đỏ", "3 vòng review xong"],
     lam="4 khuôn cột + test.", tep=["tests/fixture/cau_hinh/ix_ven.json", "tests/fixture/dap_an/gi_mid*.json", "tests/du_lieu/test_dap_an_gi.py"],
     chay=[be("tests/du_lieu/test_dap_an_gi.py")])

step(id="DT9", lan="DATA", ten="Ảnh đáp án MID1–MID3 của OMC · SC · PS",
     goal="Ba bộ MID của OMC · SC · PS đóng băng; cổng in rõ PS thiếu 03–09/2026 như AP đã đo (⛔ lấp).",
     ap="AP v3.1.2 §3.4.1 PD 508–510 · 600–603", est=(3, 4, "trung bình"), deps=["DT8"],
     gom=["`dap_an/{omc,sc,ps}_mid{1,2,3}.json`"], loai=["engine (H11)"], moi="không", mock="không",
     gioi_han=["lỗi row[45] của script OMC (AP §3.4.1) làm đáp án có thể sai — ghi cờ `nguon_nghi_loi`"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT8"],
     tb=[("DT9-B1", "đóng băng", "PS thiếu đúng 7 tháng 03–09/2026; còn lại có MONG số dòng", "cổng", "ảnh chưa có")],
     tf=NA_FE_DATA, hv=["9 ảnh"], ex=["DT9-B1 đúng + chứng minh đỏ", "3 vòng review xong"],
     lam="khuôn cột dùng chung 3 sổ + test.", tep=["tests/fixture/dap_an/{omc,sc,ps}_mid*.json", "tests/du_lieu/test_dap_an_nen_tang.py"],
     chay=[be("tests/du_lieu/test_dap_an_nen_tang.py")])

step(id="DT10", lan="DATA", ten="Ảnh IX.DRV (Allocation Table) + đáp án ATL (604 · 606)",
     goal="Driver theo (driver, CDT1, tháng) và ATL đóng băng; cổng khẳng định driver chỉ có 2025 (AP đo) và NOEM trỏ ô cứng của H1000 được ghi nguồn.",
     ap="AP v3.1.2 §3.2.2 IX.DRV · §3.4.2 PD 500 · 511–513 · 604", est=(3, 4, "trung bình"), deps=["DT2"],
     gom=["`cau_hinh/ix_drv.json` (NOEM · GI theo PE · GI theo PM · NB theo LE)", "`dap_an/atl.json` (604 · 606)"],
     loai=["engine AL.KEY (H12)"], moi="không", mock="không", gioi_han=["driver 2026 ⛔ có ở nguồn ⇒ ATL 2026 chỉ đối chiếu được khi cờ tắt (D2)"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT2"],
     tb=[("DT10-B1", "đóng băng", "driver: 4 loại × 8 CDT1 × 12 tháng 2025 (hoặc lệch có tên)", "cổng", "ảnh chưa có")],
     tf=NA_FE_DATA, hv=["2 ảnh"], ex=["DT10-B1 đúng + chứng minh đỏ", "3 vòng review xong"],
     lam="2 khuôn cột + test.", tep=["tests/fixture/cau_hinh/ix_drv.json", "tests/fixture/dap_an/atl.json", "tests/du_lieu/test_dap_an_atl.py"],
     chay=[be("tests/du_lieu/test_dap_an_atl.py")])

step(id="DT11", lan="DATA", ten="Ảnh đáp án Daily Report 2 · 3 (607–616)",
     goal="Daily Report 2 · 3 của bản A-CCR (D5) đóng băng theo (dòng PL, ngày/kỳ); cổng khẳng định hai phép CHECK của IX.PL trên chính đáp án.",
     ap="AP v3.1.2 §3.3.2 PD 605–617 · §3.5.3 D5 · IX.PL CHECK", est=(3, 4, "trung bình"), deps=["DT2"],
     gom=["`dap_an/daily_report_2.json`", "`dap_an/daily_report_3.json` (bản [MID][FS1][PLA5] Sign off)"],
     loai=["engine RP (H14)", "PDF"], moi="không", mock="không", gioi_han=["ATL AH12 '− 0.5' chỉnh tay được ghi là ô chỉnh tay (⛔ config)"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT2"],
     tb=[("DT11-B1", "đóng băng + CHECK", "NB = 0 và NIS+INT+PIT+COM = CXA+GAH+DC+MC: số kỳ đạt có MONG", "cổng", "ảnh chưa có")],
     tf=NA_FE_DATA, hv=["2 ảnh"], ex=["DT11-B1 đúng + chứng minh đỏ", "3 vòng review xong"],
     lam="2 khuôn cột + test.", tep=["tests/fixture/dap_an/daily_report_*.json", "tests/du_lieu/test_dap_an_report.py"],
     chay=[be("tests/du_lieu/test_dap_an_report.py")])

step(id="DT12", lan="DATA", ten="Ảnh Manual input của 22 kỳ còn lại (chế độ tự sinh AC10)",
     goal="Ảnh ô Manual input của ITL Ledge cho 22 kỳ ngoài 2026-03 đóng băng theo khuôn `itl_ledge_2026_03.json`; cổng liệt kê kỳ đọc được / hỏng.",
     ap="AP v3.1.2 §5.3.2 AC10 · AC11 (tự sinh) · §5.3.1 HD1", est=(3, 4, "thấp — rủi ro hết giờ đọc sổ ADJUSTED (GAP-ORA-08)"), deps=["DT2"],
     gom=["22 tệp `dap_an/itl_ledge_<ky>.json` (28 cột của 7 khối + ngày + itl_id; ⛔ Diễn giải, ⛔ Số CT — như ảnh 2026-03)"],
     loai=["chạy tự sinh (H15)"], moi="không", mock="không",
     gioi_han=["kỳ đọc hỏng sau 3 lần thử = `blocked` có tên, báo orchestrator (⛔ bỏ im)"],
     tp=dict(FE=NA_FE_DATA, BE="tool DT2", DB="không", TH="Google Sheets qua orchestrator"), tien_de=["DT2", "O7"],
     tb=[("DT12-B1", "đóng băng 22 kỳ", "số kỳ đọc được + số kỳ hỏng = 22; mỗi kỳ số dòng = phân bố kỳ của sổ", "cổng", "ảnh chưa có")],
     tf=NA_FE_DATA, hv=["≤ 22 ảnh"], ex=["DT12-B1 đúng + chứng minh đỏ", "3 vòng review xong"],
     lam="khuôn dùng lại + vòng đọc theo kỳ.", tep=["tests/fixture/dap_an/itl_ledge_*.json", "tests/du_lieu/test_anh_manual_input.py"],
     chay=[be("tests/du_lieu/test_anh_manual_input.py")])

# ═════════════ BE-CF ═════════════
HOP_FX = "`GET /api/fls/v1/config/fx` → `{bang:'IX.FX', nguon, ky:[{yyyymm, USD, SGD, COP, VND, HKD, trang_thai}], thieu:[yyyymm], trung:[yyyymm], lac:[yyyymm]}`"
step(id="C1", lan="BE-CF", ten="IX.FX đọc tĩnh: kiểm tỷ giá + GET /config/fx",
     goal=f"Gọi {HOP_FX} trả bảng tỷ giá từ nguồn tĩnh, và tháng thiếu/trùng/lạc hiện ra trong trường riêng thay vì im lặng thành 0.",
     ap="AP v3.1.2 §3.2.1 IX.FX · §3.2.4 dòng 'bảng tỷ giá' · §3.5.3 D1 · AC9",
     est=(3, 4, "trung bình — tuyến GET theo khuôn `bang_tuyen.py` (40 dòng `Tuyen(`)"), deps=["S0"],
     gom=["`fls/cau_hinh/fx.py`: nạp + kiểm (một dòng/tháng, VND = 1, 5 tiền tệ, thiếu/trùng/lạc)", "tuyến GET đọc nguồn tĩnh `fls/cau_hinh/tinh/ix_fx_mau.json` (4 tháng TỔNG HỢP, ⛔ số thật)", "khai tuyến + bảng ở `soi_bang_tuyen`"],
     loai=["kho (C5)", "ký tháng (C7)", "ảnh thật (DT2 — C5 nối)"], moi="miền config `fls/cau_hinh` (nạp + kiểm thuần)", mock="nguồn tĩnh 4 tháng tổng hợp",
     gioi_han=["số trả về là tổng hợp cho tới C5 — FE vẫn dựng được trên hợp đồng"],
     tp=dict(FE=NA_FE_API + " (F4)", BE="`fls/cau_hinh/fx.py` · `fls/api/xu_ly.py` (+1 hàm) · `fls/api/bang_tuyen.py` (+1 `Tuyen`)", DB="không (tĩnh)", TH="không"),
     tien_de=["S0 (gói `fls/cau_hinh` + hợp đồng tầng)"],
     tb=[("C1-B1", "nạp 4 tháng hợp lệ", "4 dòng, VND = 1, `thieu = trung = lac = []`", "đơn vị", "module chưa có"),
         ("C1-B2", "tháng 202407 có hai dòng", "`trung = ['202407']`; ⛔ cộng đôi", "đơn vị", "—"),
         ("C1-B3", "thiếu 202408 giữa dải", "`thieu = ['202408']`", "đơn vị", "—"),
         ("C1-B4", "GET qua máy chủ thử", "200, đúng hợp đồng; `soi_bang_tuyen` xanh với tuyến mới", "API", "tuyến chưa có"),
         ("C1-B5", "lint-imports", "`fls/cau_hinh` ⛔ import psycopg/repo/db", "kiến trúc", "—")],
     tf=NA_FE_API + " (F4)",
     hv=[HOP_FX, "`fls/cau_hinh/fx.py`", "nguồn tĩnh 4 tháng"],
     ex=["C1-B1…B5 xanh, đỏ trước khi có mã", "regression `tests/api` xanh", "3 vòng review xong"],
     lam="hàm thuần nạp/kiểm + 1 handler + 1 dòng `Tuyen`.",
     tep=["fls/cau_hinh/fx.py", "fls/cau_hinh/tinh/ix_fx_mau.json", "fls/api/xu_ly.py", "fls/api/bang_tuyen.py", "tests/cau_hinh/test_fx.py", "tests/api/test_isp_config_fx.py"],
     chay=[be("tests/cau_hinh/test_fx.py", "tests/api/test_isp_config_fx.py"), "python tools/soi_bang_tuyen.py", ".venv/bin/lint-imports"])

step(id="C4", lan="BE-CF", ten="IX.HD cây: nạp + kiểm cha–con + GET /config/hd (tĩnh từ ảnh)",
     goal="Gọi `GET /api/fls/v1/config/hd` trả cây 74 dòng · 6 nhóm từ ảnh ATL, và cây hỏng (cha vắng, chu trình, cấp nhảy) bị từ chối có tên lỗi.",
     ap="AP v3.1.2 §3.2.1 IX.HD · §3.2.5 · §3.2.4 dòng 'cây HD theo vị trí dòng' · WP-C1", est=(3, 4, "trung bình"), deps=["DT3"],
     gom=["`fls/cau_hinh/hd.py`: cây + `con_cua()` + `la()`; cha = Σ con là việc của engine (H5), ⛔ ở đây", "GET đọc ảnh `atl_cay.json` qua đường dẫn truyền vào"],
     loai=["kho (C5)", "đối chiếu 73 mã Mapping Master (ghi chênh, ⛔ hoà giải)"], moi="cây phân cấp có kiểm", mock="ảnh đóng băng thật (tĩnh)",
     gioi_han=["74 (ATL) ≠ 73 (Mapping Master): trả cả hai số + danh sách chênh"],
     tp=dict(FE="N/A — ⛔ có màn cây trong AP v3.1.2; cây được dùng bởi engine H5.", BE="`fls/cau_hinh/hd.py` · tuyến", DB="không", TH="không"),
     tien_de=["DT3"],
     tb=[("C4-B1", "nạp ảnh ATL", "74 nút, 6 nhóm, gốc đúng, ⛔ chu trình", "đơn vị", "module chưa có"),
         ("C4-B2", "cây có chu trình A→B→A (tổng hợp)", "lỗi `HD_CHU_TRINH`", "đơn vị", "—"),
         ("C4-B3", "cha vắng", "lỗi `HD_CHA_VANG`", "đơn vị", "—"),
         ("C4-B4", "GET", "200 · 74 · `chenh_mapping_master` liệt kê", "API", "tuyến chưa có")],
     tf="N/A — ⛔ có màn cây trong AP v3.1.2; cây được dùng bởi engine H5.",
     hv=["`GET /api/fls/v1/config/hd`", "`fls/cau_hinh/hd.py`"], ex=["C4-B1…B4 xanh", "3 vòng review xong"],
     lam="module cây + 1 tuyến.", tep=["fls/cau_hinh/hd.py", "fls/api/xu_ly.py", "fls/api/bang_tuyen.py", "tests/cau_hinh/test_hd.py", "tests/api/test_isp_config_hd.py"],
     chay=[be("tests/cau_hinh/test_hd.py", "tests/api/test_isp_config_hd.py")])

step(id="C5", lan="BE-CF", ten="Kho config chỉ-thêm có phiên bản (di trú 0027) — IX.FX + IX.HD đọc từ kho",
     goal="Hai tuyến /config/fx và /config/hd trả số từ kho; mọi UPDATE/DELETE trên bảng config bị trigger chặn, và một lần nạp lại tạo phiên bản mới thay vì ghi đè.",
     ap="AP v3.1.2 §3.2.3 IX.TMP ('snapshot có version') · §3.5.3 D1 · AP Q4 (PostgreSQL trước) · INV-I08 (chỉ-thêm)",
     est=(2, 3, "cao — chép khuôn `fls_khai_cot` (di trú 0016) + `fls/repo/khai_cot.py`"), deps=["C4", "DT2"],
     gom=["⭐ chép khuôn `fls_khai_cot`: chỉ-thêm · `version` · `hieu_luc_tu` do MÁY đặt · đủ-hoặc-không trong một giao dịch · ⛔ bản mặc định · lỗi 'nguồn lạ' ≠ 'chưa khai'", "0027: `fls_cau_hinh_ban` (bang · phien_ban · nguon · checksum · actor · luc) + `fls_cau_hinh_dong` (ban_id · khoa · gia_tri jsonb) — chỉ-thêm (O5)",
          "`fls/repo/cau_hinh_repo.py`: nạp ảnh → phiên bản mới; đọc phiên bản mới nhất", "C1/C4 đổi nguồn từ tĩnh sang kho; GỠ `fls/cau_hinh/tinh/ix_fx_mau.json`", "sinh lại hiện vật ERD/golden (CLAUDE.md §Cổng)"],
     loai=["ký (C7)", "bảng config khác (C6, C8…)"], moi="lưu kho (persistence) config", mock="không — kho test PG",
     gioi_han=["kho test cục bộ (O4)"],
     tp=dict(FE="N/A — hợp đồng tuyến ⛔ đổi; F4 dùng lại nguyên.", BE="`fls/repo/cau_hinh_repo.py` · handler C1/C4", DB="`0027_cau_hinh_chi_them.sql` · trigger chặn UPDATE/DELETE", TH="không"),
     tien_de=["C4", "DT2 (ảnh FX thật)", "S0 (kho test)"],
     tb=[("C5-B1", "nạp `ix_fx.json` thật", "phiên bản 1; GET trả 37 dòng; `lac = ['202306']`", "tích hợp DB (pg)", "bảng chưa có"),
         ("C5-B2", "nạp lại cùng ảnh", "phiên bản 2, checksum trùng ⇒ ghi `khong_doi = true`, ⛔ ghi đè", "pg", "—"),
         ("C5-B3", "UPDATE một dòng", "trigger ĐỎ có tên", "pg", "—"),
         ("C5-B4", "golden DDL + `pg_verify`", "xanh sau `--update-golden` có chủ đích", "pg", "—")],
     tf="N/A — hợp đồng tuyến ⛔ đổi; F4 dùng lại nguyên.",
     hv=["di trú 0027", "`cau_hinh_repo.py`", "ERD/golden sinh lại"], ex=["C5-B1…B4 xanh", "bộ `tests/db` xanh", "3 vòng review xong"],
     lam="1 di trú + 1 repo + đổi nguồn 2 handler.", tep=["fls/db/migrations/0027_cau_hinh_chi_them.sql", "fls/db/schema.py", "fls/repo/cau_hinh_repo.py", "fls/api/xu_ly.py", "tests/cau_hinh/test_kho_cau_hinh_pg.py"],
     chay=[ENV, "python -m fls.db.pg_migrate", be("tests/cau_hinh/test_kho_cau_hinh_pg.py", "tests/db"), "python -m fls.db.erd_export --write"])

step(id="C6", lan="BE-CF", ten="IX.PER: lịch kỳ từ dữ liệu + ngày đầu + luật ghi nhận kỳ (D4)",
     goal="`kỳ_của(ngày)` trả Y/H/Q/M đúng năm của chính dữ liệu (⛔ ép 2025), ngày đầu cột đọc từ config (21/10/2024), luật ghi nhận = 'dồn ngày 1 tháng PL start' (D4 A).",
     ap="AP v3.1.2 §3.2.1 IX.PER · §3.2.4 dòng 'ngày đầu cột… năm ép 2025' · D4", est=(2, 4, "cao"), deps=["C5"],
     gom=["`fls/cau_hinh/ky.py` + dòng config IX.PER trong kho (phiên bản)", "GET /config/per"], loai=["chia đều PL start→end (D4 B — sau khi owner ký)"], moi="lịch kỳ có cấu hình", mock="không",
     gioi_han=["chỉ luật A hoạt động; luật B bị từ chối có tên `LUAT_CHUA_KY`"],
     tp=dict(FE="N/A — ⛔ có màn kỳ trong AP; engine H6 tiêu thụ.", BE="`fls/cau_hinh/ky.py` · tuyến", DB="dòng config qua 0027 (⛔ di trú mới)", TH="không"), tien_de=["C5"],
     tb=[("C6-B1", "ngày 2026-11-05", "Y2026 · H2 · Q4 · M11 (⛔ 2025)", "đơn vị", "module chưa có"),
         ("C6-B2", "ngày 2024-12-31", "Y2024 (bản AS-IS ép T11/T12 → 2024 — giữ đúng dữ liệu)", "đơn vị", "—"),
         ("C6-B3", "chọn luật B", "lỗi `LUAT_CHUA_KY`", "đơn vị", "—"), ("C6-B4", "GET /config/per", "200 · ngày đầu 2024-10-21 · luật A", "API", "—")],
     tf="N/A — ⛔ có màn kỳ trong AP; engine H6 tiêu thụ.", hv=["`fls/cau_hinh/ky.py`", "`GET /api/fls/v1/config/per`"], ex=["C6-B1…B4 xanh", "3 vòng review xong"],
     lam="module lịch + nạp dòng config + 1 tuyến.", tep=["fls/cau_hinh/ky.py", "fls/api/xu_ly.py", "fls/api/bang_tuyen.py", "tests/cau_hinh/test_ky.py"],
     chay=[be("tests/cau_hinh/test_ky.py")])

step(id="C7", lan="BE-CF", ten="IX.FX ký tháng + CHẶN tháng chưa ký/thiếu (D1)",
     goal="`POST /api/fls/v1/config/fx/{yyyymm}/sign` niêm phong tháng với người ký lấy TỪ TOKEN (`fls/api/the.py`); `fx_cua(yyyymm)` cho engine trả tỷ giá chỉ khi tháng đã ký, còn lại ném `FX_CHAN` có tên tháng.",
     ap="AP v3.1.2 §3.5.3 D1 (DECIDED · A: owner ký mỗi tháng; thiếu tháng = CHẶN) · §3.2.4 · BA-07 §1 (actor từ token)",
     est=(2, 3, "cao — ⭐ cửa token đã có: mọi yêu cầu qua `the.kiem` → `Nguoi` (JWT HS256, fail-closed); khuôn ghi chỉ-thêm của C5"),
     deps=["C5"],
     gom=["bản ký = phiên bản mới có `actor` = người trong token (⛔ từ thân yêu cầu), `ky_luc`; ký lại cùng tháng ⇒ 409",
          "`fx_cua()` thuần cho engine H4 … I2 (CHẶN)", "khai tuyến với `bang_ghi=('fls_cau_hinh_ban', 'fls_cau_hinh_dong')`"],
     loai=["UI ký (F5)", "huỷ ký", "đăng nhập mới — đã có `the.py`", "phân quyền theo vai (O11)"],
     moi="ký niêm phong (sign-off)", mock="token thử ký bằng khoá bí mật của bộ test",
     gioi_han=["mọi token hợp lệ đều ký được (O11 — máy chỉ mở `127.0.0.1`, `GAP-WEB-01`)"],
     tp=dict(FE=NA_FE_API + " (F5)", BE="`fls/cau_hinh/fx.py` (+`fx_cua`) · `fls/repo/cau_hinh_repo.py` (+ký) · tuyến POST", DB="dòng mới qua 0027", TH="không"),
     tien_de=["C5"],
     tb=[("C7-B1", "ký 202510 với token hợp lệ", "201; GET thấy `trang_thai = 'da_ky'`, `actor` = người trong token", "pg", "tuyến chưa có"),
         ("C7-B2", "ký lại 202510", "409", "pg", "—"),
         ("C7-B3", "`fx_cua('202511')` chưa ký", "`FX_CHAN 202511`", "đơn vị", "—"),
         ("C7-B4", "thân yêu cầu tự khai `actor` khác token", "bị bỏ qua; `actor` = người trong token", "an toàn", "—"),
         ("C7-B5", "không token", "401 từ cửa sẵn có (hồi quy — ⛔ mã lỗi mới)", "hồi quy", "—"),
         ("C7-B6", "`soi_bang_tuyen`: POST khai `bang_ghi`, ⛔ chạm `fls_itl`", "xanh", "kiến trúc", "—")],
     tf=NA_FE_API + " (F5)",
     hv=["`POST /api/fls/v1/config/fx/{yyyymm}/sign`", "`fx_cua()`"],
     ex=["C7-B1…B6 đúng", "3 vòng review xong"],
     lam="+1 tuyến ghi +1 hàm CHẶN; người ký đọc từ `Nguoi` của yêu cầu.",
     tep=["fls/cau_hinh/fx.py", "fls/repo/cau_hinh_repo.py", "fls/api/xu_ly.py", "fls/api/bang_tuyen.py", "tests/cau_hinh/test_ky_fx_pg.py"],
     chay=[be("tests/cau_hinh/test_ky_fx_pg.py"), "python tools/soi_bang_tuyen.py"])

step(id="C8", lan="BE-CF", ten="IX.ORG: LE · TK → CDT1 + CDT lạ vào hàng chờ (⛔ rơi về SHQ2)",
     goal="`cdt_cua(tk)` trả CDT1 từ IX.ORG; CDT ⛔ có trong CDT Correct sinh một sự kiện hàng chờ thấy được qua `GET /api/fls/v1/queue` hiện có, thay vì mặc định SHQ2 im lặng.",
     ap="AP v3.1.2 §3.2.1 IX.ORG · §3.2.4 dòng 'CDT Correct… mặc định SHQ2'", est=(2, 3, "cao — pháp nhân dùng lại `fls_le` + `fls/canon/le.py`"), deps=["C5", "DT3"],
     gom=["⭐ pháp nhân: bảng `fls_le` (`le_code` · `le_name` · `is_entity`) + `fls/canon/le.py` (hai hình dạng mã LE) — ⛔ bảng LE mới", "`fls/cau_hinh/to_chuc.py` + nạp ảnh `mapping_master_cfg.json`, `cdt_correct.json` vào kho (0027)", "CDT lạ → `fls_queue_event` (bảng có sẵn) loại `CDT_LA`"],
     loai=["màn mới (hàng chờ hiện có hiển thị)"], moi="hàng chờ cho giá trị config lạ", mock="không",
     gioi_han=["8 CDT1 · 18 dòng CDT Correct là của ảnh đóng băng"],
     tp=dict(FE="N/A — màn hàng chờ hiện có đọc `GET /queue`; ⛔ màn mới.", BE="`fls/cau_hinh/to_chuc.py` · repo", DB="`fls_queue_event` (có sẵn) + dòng config 0027", TH="không"), tien_de=["C5", "DT3"],
     tb=[("C8-B1", "TK có trong Mapping Master", "CDT1 đúng; 0 sự kiện", "đơn vị", "module chưa có"),
         ("C8-B2", "CDT 'XYZ' lạ", "1 sự kiện `CDT_LA` thấy ở `GET /queue`; ⛔ trả SHQ2", "pg", "—")],
     tf="N/A — màn hàng chờ hiện có đọc `GET /queue`; ⛔ màn mới.", hv=["`fls/cau_hinh/to_chuc.py`"], ex=["C8-B1, B2 xanh", "regression `tests/api/test_cua_lenh_cho_pg.py` xanh", "3 vòng review xong"],
     lam="module tổ chức + ghi hàng chờ.", tep=["fls/cau_hinh/to_chuc.py", "fls/repo/cau_hinh_repo.py", "tests/cau_hinh/test_to_chuc_pg.py"],
     chay=[be("tests/cau_hinh/test_to_chuc_pg.py", "tests/api/test_cua_lenh_cho_pg.py")])

step(id="C9", lan="BE-CF", ten="IX.VEN: vendor · network · CDT1 + cột 'cách tính'",
     goal="`GET /api/fls/v1/config/ven` trả 36 dòng Block 1 từ kho, và 5 vendor VD341 · VD444 · VD428 · 'Max' · VD62 mang mã 'cách tính' riêng thay vì nằm trong công thức.",
     ap="AP v3.1.2 §3.2.2 IX.VEN · §3.2.4 dòng 'VD341 · VD444…'", est=(2, 4, "cao"), deps=["C5", "DT8"],
     gom=["`fls/cau_hinh/vendor.py` + nạp ảnh `ix_ven.json`", "tuyến GET"], loai=["phép tính riêng (H10)"], moi="không (bảng config theo khuôn C5)", mock="không",
     gioi_han=["mã 'cách tính' chỉ là NHÃN; phép tính ở H10"],
     tp=dict(FE="N/A — ⛔ màn trong AP; engine H9/H10 tiêu thụ.", BE="`fls/cau_hinh/vendor.py` · tuyến", DB="dòng config 0027", TH="không"), tien_de=["C5", "DT8"],
     tb=[("C9-B1", "nạp", "36 dòng; 5 mã đặc biệt; product_id → CDT1 đủ 7 CDT1", "pg", "chưa có"), ("C9-B2", "vendor trùng khoá", "lỗi có tên", "đơn vị", "—")],
     tf="N/A — ⛔ màn trong AP; engine H9/H10 tiêu thụ.", hv=["`GET /api/fls/v1/config/ven`"], ex=["C9-B1, B2 xanh", "3 vòng review xong"],
     lam="module + tuyến.", tep=["fls/cau_hinh/vendor.py", "fls/api/xu_ly.py", "fls/api/bang_tuyen.py", "tests/cau_hinh/test_vendor_pg.py"],
     chay=[be("tests/cau_hinh/test_vendor_pg.py")])

step(id="C10", lan="BE-CF", ten="IX.DRV: driver theo (driver, CDT1, tháng)",
     goal="`driver_cua(loai, cdt1, thang)` trả giá trị từ kho; tháng ⛔ có driver ném `DRV_THIEU` có tên (⛔ trỏ ô cứng của H1000).",
     ap="AP v3.1.2 §3.2.2 IX.DRV · §3.2.4 dòng 'headcount NOEM lấy ô cứng'", est=(2, 4, "cao"), deps=["C5", "DT10"],
     gom=["`fls/cau_hinh/driver.py` + nạp `ix_drv.json` + GET /config/drv"], loai=["driver 2026 (nguồn ⛔ có)"], moi="không", mock="không",
     gioi_han=["chỉ 2025 (AP đo)"],
     tp=dict(FE="N/A — engine H12 tiêu thụ.", BE="`fls/cau_hinh/driver.py`", DB="dòng config 0027", TH="không"), tien_de=["C5", "DT10"],
     tb=[("C10-B1", "NOEM · SHQ1 · 202503", "giá trị = ảnh", "pg", "chưa có"), ("C10-B2", "202603", "`DRV_THIEU`", "đơn vị", "—")],
     tf="N/A — engine H12 tiêu thụ.", hv=["`fls/cau_hinh/driver.py`", "`GET /api/fls/v1/config/drv`"], ex=["C10-B1, B2 xanh", "3 vòng review xong"],
     lam="module + tuyến.", tep=["fls/cau_hinh/driver.py", "fls/api/bang_tuyen.py", "fls/api/xu_ly.py", "tests/cau_hinh/test_driver_pg.py"],
     chay=[be("tests/cau_hinh/test_driver_pg.py")])

step(id="C11", lan="BE-CF", ten="IX.ALR: luật phân bổ có hiệu lực theo kỳ + cờ mặc định TẮT (D2)",
     goal="`luat_cua(hd, ky)` trả phương pháp và cờ; mọi luật nạp vào đều `bat = false` (D2 A), theo PM 4 · by GI 8 · by NOEM 5 · by LE 0 HD như AP đo.",
     ap="AP v3.1.2 §3.2.2 IX.ALR · §3.2.5 · §3.5.3 D2 · D3 (driver by GI = PE)", est=(2, 3, "cao — nguồn là `fls_mapping_master` đã nạp"), deps=["C5", "DT3"],
     gom=["⭐ nguồn = bảng `fls_mapping_master` đã nạp (`need_cfa2` · `method_cfa2`; đo 28/08: 21 mã có phương pháp — By GI 8 · By NOEM 5 · H1000 Ledger 4 · GI/OMC/PS/SC Ledger mỗi loại 1). Bảng ấy bị XOÁ-NẠP LẠI toàn bộ (⛔ phiên bản) — chính lỗ IX.ALR lấp: thêm hiệu lực theo kỳ + cờ vào kho config", "giữ bẫy VLOOKUP của `fls/ledger/allocate.py` (ô `Method` rỗng hiện `0`, ⛔ 'No need')", "`fls/cau_hinh/luat_pb.py` + ghi chú ATL B2:C4", "GET /config/alr"], loai=["bật cờ (owner ký — ngoài ISP)"], moi="luật có hiệu lực theo kỳ + cờ", mock="không",
     gioi_han=["bật cờ ⛔ có tuyến trong ISP này (D2: parity trước)"],
     tp=dict(FE="N/A — ⛔ màn cờ trong AP v3.1.2; engine H12 tiêu thụ.", BE="`fls/cau_hinh/luat_pb.py`", DB="dòng config 0027", TH="không"), tien_de=["C5", "DT3"],
     tb=[("C11-B1", "nạp", "17 HD có luật (4 + 8 + 5); 4 mã H1000 Ledger mang `khong_qua_allocate` (Q3); 100% `bat = false`", "pg", "chưa có"), ("C11-B2", "HD OFR của CAH", "⛔ by NOEM (ngoại lệ AP §3.2.5)", "đơn vị", "—"),
         ("C11-B3", "by GI", "driver = PE (D3)", "đơn vị", "—")],
     tf="N/A — ⛔ màn cờ trong AP v3.1.2; engine H12 tiêu thụ.", hv=["`fls/cau_hinh/luat_pb.py`", "`GET /api/fls/v1/config/alr`"], ex=["C11-B1…B3 xanh", "3 vòng review xong"],
     lam="module + tuyến.", tep=["fls/cau_hinh/luat_pb.py", "fls/api/bang_tuyen.py", "fls/api/xu_ly.py", "tests/cau_hinh/test_luat_pb_pg.py"],
     chay=[be("tests/cau_hinh/test_luat_pb_pg.py")])

step(id="C12", lan="BE-CF", ten="IX.PL: dòng PL là biểu thức trên cây HD + 2 phép CHECK",
     goal="`tinh_pl(gia_tri_hd)` trả PL2…PL8 từ MỘT định nghĩa biểu thức (⛔ eval), và `check_pl()` trả kết quả hai phép NB = 0 · NIS+INT+PIT+COM = CXA+GAH+DC+MC.",
     ap="AP v3.1.2 §3.2.3 IX.PL · §3.2.4 dòng 'dòng PL viết trong ô ATL… hai định nghĩa'", est=(3, 4, "trung bình — bộ phân tích biểu thức cộng/trừ trên mã HD"), deps=["C4", "C5"],
     gom=["ngữ pháp tối thiểu: mã HD, `+`, `−`, ngoặc — ⛔ `eval`", "nguồn định nghĩa = ATL (bản DECIDED theo đề xuất A của §3.2.3); chênh với Mapping Master ghi thành danh sách"],
     loai=["hàm khác ngoài + −"], moi="biểu thức cấu hình (bộ phân tích an toàn)", mock="giá trị HD tổng hợp ở test",
     gioi_han=["chênh định nghĩa (vd LC ở PL3) được LIỆT KÊ cho owner, ⛔ tự hoà giải"],
     tp=dict(FE="N/A — engine H13 tiêu thụ.", BE="`fls/cau_hinh/dong_pl.py`", DB="dòng config 0027", TH="không"), tien_de=["C4 (cây)", "C5"],
     tb=[("C12-B1", "PL2 với giá trị HD tổng hợp", "đúng tay tính", "đơn vị", "chưa có"), ("C12-B2", "biểu thức `__import__`", "từ chối", "an toàn", "—"),
         ("C12-B3", "CHECK trên số cân", "cả hai đúng; lệch 1 ⇒ báo dòng nào", "đơn vị", "—")],
     tf="N/A — engine H13 tiêu thụ.", hv=["`fls/cau_hinh/dong_pl.py`"], ex=["C12-B1…B3 xanh", "3 vòng review xong"],
     lam="bộ phân tích nhỏ + nạp định nghĩa.", tep=["fls/cau_hinh/dong_pl.py", "tests/cau_hinh/test_dong_pl.py"],
     chay=[be("tests/cau_hinh/test_dong_pl.py")])

step(id="C13", lan="BE-CF", ten="IX.TMP: bản báo cáo ký có phiên bản (snapshot sign-off)",
     goal="`POST /api/fls/v1/report/snapshot/{ky}/sign` lưu bản Daily Report 3 kèm checksum và người ký lấy từ token; bản đã ký ⛔ đổi khi số nguồn đổi — số mới thành phiên bản mới chưa ký.",
     ap="AP v3.1.2 §3.2.3 IX.TMP · §3.2.4 dòng 'sign-off dán value ở sheet [PLA5]'", est=(2, 3, "cao — khuôn ký + người ký từ token của C7"), deps=["C7"],
     gom=["lưu bản (JSON ô) do engine H14 đưa vào; GET danh sách phiên bản + trạng thái"], loai=["khuôn Templ 1–5 dạng trình bày", "PDF"], moi="không (dùng lại ký C7 + kho C5)", mock="bản báo cáo tổng hợp cho tới khi H14 xong",
     gioi_han=["nội dung bản lấy từ tham số; nối engine thật ở I2"],
     tp=dict(FE=NA_FE_API + " (F7)", BE="`fls/cau_hinh/ban_ky.py` · tuyến GET + POST", DB="dòng 0027", TH="không"), tien_de=["C7 (khuôn ký)"],
     tb=[("C13-B1", "ký bản kỳ 2025-12", "201; GET thấy phiên bản 1 đã ký + checksum", "pg", "chưa có"),
         ("C13-B2", "đưa bản mới khác 1 ô", "phiên bản 2 `chua_ky`; phiên bản 1 giữ nguyên", "pg", "—")],
     tf=NA_FE_API + " (F7 — màn F08)", hv=["`GET/POST /api/fls/v1/report/snapshot/{ky}…`"], ex=["C13-B1, B2 xanh", "3 vòng review xong"],
     lam="module + 2 tuyến.", tep=["fls/cau_hinh/ban_ky.py", "fls/api/bang_tuyen.py", "fls/api/xu_ly.py", "tests/cau_hinh/test_ban_ky_pg.py"],
     chay=[be("tests/cau_hinh/test_ban_ky_pg.py"), "python tools/soi_bang_tuyen.py"])

step(id="CG1", lan="BE-CF", ten="Cổng HD1 vào `GET /gates`: ô chờ `FINAL` thành số đo + cổng `HD1_THANG`",
     goal="`GET /api/fls/v1/gates` trả cổng `FINAL` = 69.510/69.510 ô (ĐẠT) và cổng `HD1_THANG` = '5/23 kỳ đạt' (KHÔNG ĐẠT, `ly_do` liệt kê kỳ đỏ + số dòng thiếu), đọc từ `voi_so_luong.json`; tệp đo vắng thì cả hai `dat = null`.",
     ap="AP v3.1.2 §5.3.1 HD1 ★ · HD5 · §5.3.2 AC10 · Figure 5.3.3",
     est=(2, 3, "cao — ⭐ tuyến `/gates`, `doc_cong` (`fls/repo/doc_bao_cao.py:871`), vỏ `{data,error,meta}` và ba trạng thái đã có; ô chờ `FINAL` đã ghi sẵn 'chạy ngoài kho bằng `cong_parity.py`'"),
     deps=["H2", "DT1a"],
     gom=["thay ô chờ `FINAL` của `_CHUA_DO_DUOC` (`doc_bao_cao.py:850`) bằng số đo từ tệp; thêm cổng `HD1_THANG`",
          "đường dẫn tệp đo truyền vào (⛔ gõ cứng) — như kết nối kho được truyền vào (hợp đồng tầng 7)",
          "giữ luật của `doc_cong`: ⛔ bao giờ trả danh sách toàn xanh; `chua_do_duoc` đếm đúng"],
     loai=["cổng HD2 (CG2)", "thẻ trên màn (FG)", "đọc kho sống (HD5 sau)"],
     moi="cổng đọc từ tệp đo (ngoài kho) trong `/gates`", mock="tệp đo tĩnh `voi_so_luong.json`",
     gioi_han=["số là của ảnh 26/08 — `ly_do` ghi ngày ảnh"],
     tp=dict(FE="N/A — F03 hiện cổng mới ở FG; bước này ⛔ sửa màn.", BE="`fls/repo/doc_bao_cao.py` (`doc_cong` · `_CHUA_DO_DUOC`)", DB="không — tệp đo", TH="không"),
     tien_de=["H2 (trường `dat_hd1` trong `voi_so_luong.json`)", "DT1a (danh sách kỳ đỏ)"],
     tb=[("CG1-B1", "GET /gates với tệp đo thật", "`FINAL`: dat true · da_do '69.510/69.510 ô'; `HD1_THANG`: dat false · da_do '5/23 kỳ đạt'", "API", "ô chờ còn `dat = null`"),
         ("CG1-B2", "tệp đo vắng", "cả hai `dat = null`, `chua_do_duoc` tăng đúng 2 — ⛔ 200 toàn xanh (Đ5)", "API lỗi", "—"),
         ("CG1-B3", "bài sẵn có của `/gates` + `tests/api`", "xanh", "hồi quy", "—"),
         ("CG1-B4", "phá MONG trong bài", "ĐỎ rồi trả nguyên", "chứng minh đỏ", "—")],
     tf="N/A — F03 hiện cổng mới ở FG; bước này ⛔ sửa màn.",
     hv=["2 cổng trong `GET /api/fls/v1/gates`"],
     ex=["CG1-B1…B4 đúng", "3 vòng review xong"],
     lam="đổi một ô chờ thành cổng đo + thêm một cổng.",
     tep=["fls/repo/doc_bao_cao.py", "tests/api/test_isp_gates_hd1.py"],
     chay=[be("tests/api/test_isp_gates_hd1.py", "tests/api")])

step(id="CG2", lan="BE-CF", ten="Cổng HD2 theo gói WP-C2…C5 vào `GET /gates`",
     goal="`GET /gates` có một cổng mỗi gói `HD2_WP_C2` … `HD2_WP_C5` đọc `hd2_cong.json`; gói chưa có cổng là `dat = null` ('chưa đo'), gói có lát bỏ là `dat = false` — ⛔ bao giờ '0 lệch' khi chưa đo.",
     ap="AP v3.1.2 §5.3.1 HD2 · §3.5.4",
     est=(2, 3, "cao — cùng khuôn CG1; phán quyết `cong_parity.PhanXu` đã nằm trong tệp"),
     deps=["CG1", "H4"],
     gom=["4 cổng theo hợp đồng `hd2_cong.json` do H4 khai", "gói mới tự hiện khi H5…H14 ghi thêm vào tệp — ⛔ bước mới cho mỗi gói"],
     loai=["khoan xuống từng ô lệch"], moi="không (dùng lại khuôn CG1)", mock="tệp cổng tĩnh",
     gioi_han=["chỉ gói đã có cổng tại lúc chạy"],
     tp=dict(FE="N/A — F03 vẽ cổng mới không cần sửa (ba trạng thái đã có); FG đã có bài kiểm thẻ.", BE="`fls/repo/doc_bao_cao.py`", DB="không", TH="không"),
     tien_de=["CG1 (khuôn cổng tệp đo)", "H4 (hợp đồng `hd2_cong.json`)"],
     tb=[("CG2-B1", "tệp chỉ có WP-C2", "WP-C2 theo `PhanXu`; WP-C3…C5 `dat = null`", "API", "cổng chưa có"),
         ("CG2-B2", "WP-C2 có `lat_bo > 0`", "`dat = false` (thiếu lát ⛔ được nói 100%)", "API", "—"),
         ("CG2-B3", "tệp vắng", "4 cổng `dat = null`", "API lỗi", "—")],
     tf="N/A — F03 vẽ cổng mới không cần sửa (ba trạng thái đã có); FG đã có bài kiểm thẻ.",
     hv=["4 cổng HD2 trong `GET /api/fls/v1/gates`"],
     ex=["CG2-B1…B3 đúng", "3 vòng review xong"],
     lam="+4 cổng đọc tệp.",
     tep=["fls/repo/doc_bao_cao.py", "tests/api/test_isp_gates_hd2.py"],
     chay=[be("tests/api/test_isp_gates_hd2.py")])

# ═════════════ BE-HC ═════════════
step(id="H1", lan="BE-HC", ten="CA.GL thuần trên dòng tổng hợp (Nợ/Có × 5 tiền tệ → bVND · mUSD)",
     goal="`tinh_gl(dong, fx)` trả, cho mỗi dòng, Nợ/Có tách theo 5 tiền tệ, bVND = tỷ giá × tiền / 10⁹ và mUSD = bVND ÷ USD × 10³ — đúng tay tính trên 6 dòng tổng hợp.",
     ap="AP v3.1.2 §3.3.1 PD 406 · 412 · §3.5.4 WP-C2 · AC9 (engine đọc config, ⛔ gõ lại)", est=(3, 4, "trung bình"), deps=["S0"],
     gom=["`fls/bao_cao/gl.py` thuần; tỷ giá vào bằng THAM SỐ (dict tháng → tiền tệ) — ⛔ đọc kho", "tồn luỹ kế theo thứ tự dòng đưa vào (giữ hành vi AS-IS, ghi rõ)"],
     loai=["dữ liệu thật (H4)", "dòng HR (H7)"], moi="engine quy đổi GL", mock="6 dòng tổng hợp + tỷ giá tổng hợp",
     gioi_han=["chưa so với đáp án 406 — H4"],
     tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/gl.py`", DB="không", TH="không"), tien_de=["S0 (gói `fls/bao_cao`)"],
     tb=[("H1-B1", "dòng VND Nợ 2.500.000.000, tỷ giá USD 25.500", "bVND 2,5 · mUSD 98,039…", "đơn vị", "module chưa có"),
         ("H1-B2", "dòng USD Có", "tách đúng cột Có; tồn = tồn trước − Có", "đơn vị", "—"),
         ("H1-B3", "tháng ⛔ có tỷ giá", "ném lỗi có tên (⛔ trả 0 — chính lỗi SUMIFS = 0 của AS-IS)", "đơn vị", "—"),
         ("H1-B4", "lint-imports", "`fls/bao_cao` ⛔ chạm DB", "kiến trúc", "—")],
     tf=NA_FE_TOOL, hv=["`fls/bao_cao/gl.py`"], ex=["H1-B1…B4 xanh, đỏ trước khi có mã", "3 vòng review xong"],
     lam="một hàm thuần + dataclass dòng GL.", tep=["fls/bao_cao/gl.py", "tests/bao_cao/test_gl.py"],
     chay=[be("tests/bao_cao/test_gl.py"), ".venv/bin/lint-imports"])

step(id="H2", lan="BE-HC", ten="HD1 · cổng nhận 'lệch có tên lý do và owner ký'",
     goal="`do_voi_so_luong.py` tính kỳ 'đạt HD1' khi mọi dòng chưa 1-1 của kỳ đều có nhãn lý do (DT1b) ĐÃ KÝ trong sổ lý do, và nhãn chưa ký vẫn tính là đỏ.",
     ap="AP v3.1.2 §5.3.1 HD1 ('Lệch = 0, hoặc mỗi lệch có tên lý do và owner ký') · AC10", est=(2, 4, "cao"), deps=["DT1a"],
     gom=["sổ lý do `docs/ITL/_tools/so_ly_do_hd1.json` (nhãn · số dòng · người ký · ngày) — khởi tạo RỖNG (0 chữ ký)", "MONG mới: `dat_hd1_theo_ky` khai trước (Đ5)"],
     loai=["ký thật (owner — O8)", "sửa mã ghép (H3)"], moi="miễn trừ có chữ ký trong cổng", mock="chữ ký tổng hợp chỉ trong test",
     gioi_han=["khi chưa có chữ ký thật, số kỳ đạt giữ 5/23"],
     tp=dict(FE=NA_FE_TOOL, BE="`tools/do_voi_so_luong.py`", DB="không", TH="không"), tien_de=["DT1a (danh sách dòng)"],
     tb=[("H2-B1", "sổ rỗng", "kỳ đạt = 5 (= AP v3.1.2)", "cổng", "trường mới chưa có"),
         ("H2-B2", "test ký giả nhãn của mọi dòng 2026-07", "2026-07 thành đạt; tổng 6", "đơn vị", "—"),
         ("H2-B3", "nhãn có nhưng chưa ký", "vẫn đỏ", "đơn vị", "—"), ("H2-B4", "phá MONG", "cổng ĐỎ rồi trả nguyên", "chứng minh đỏ", "—")],
     tf=NA_FE_TOOL, hv=["`so_ly_do_hd1.json` (rỗng)", "trường `dat_hd1` trong `voi_so_luong.json`"], ex=["H2-B1…B4 đúng", "3 vòng review xong"],
     lam="đọc sổ lý do + phán theo kỳ.", tep=["tools/do_voi_so_luong.py", "docs/ITL/_tools/voi_so_luong.json", "tests/oracle/test_do_voi_hd1.py"],
     chay=[be("tests/oracle/test_do_voi_hd1.py"), "python tools/do_voi_so_luong.py --ghi"])

step(id="H3", lan="BE-HC", ten="HD1 · sửa lớp lỗi mã lớn nhất mà DT1b chỉ ra",
     goal="Số dòng ghép 1-1 tăng đúng bằng số dòng của lớp được sửa (mong khai trước từ DT1b), ⛔ dòng đang ghép nào bị mất.",
     ap="AP v3.1.2 §5.3.1 HD1 · AC10 · §4.3.1 SI.MAP", est=(3, 4, "thấp — lớp chỉ biết sau DT1b"), deps=["H2", "DT1b"],
     gom=["lớp nhãn `KHOA_LECH` hoặc `TRUNG_SEQ` lớn nhất (theo DT1b) — sửa ở chỗ DT1b trỏ (chuẩn hoá khoá / seq)", "bài hồi quy dùng đúng các `dong_sheet` của lớp"],
     loai=["lớp `KHONG_CO_SAO_KE` (đi đường ký lý do — H2/O8)", "lớp thứ hai (ISP sửa đổi nếu cần)"], moi="không (sửa lỗi)", mock="không",
     gioi_han=["⚠ DT1b cho 0 dòng 'lỗi mã' ⇒ bước này bị HUỶ bằng bản ISP sửa có lý do (⛔ chạy rỗng)"],
     tp=dict(FE=NA_FE_TOOL, BE="`fls/ledger/classifying.py` hoặc `fls/adapters/sao_ke_canon.py` (DT1b trỏ chỗ nào sửa chỗ ấy)", DB="không", TH="không"), tien_de=["DT1b có lớp lỗi mã ≥ 1 dòng", "H2"],
     tb=[("H3-B1", "bài hồi quy theo `dong_sheet` của lớp", "đỏ trước sửa; xanh sau", "hồi quy", "lỗi đang có"),
         ("H3-B2", "toàn bộ ghép", "chay = 9.845 + n (n khai từ DT1b); 0 dòng cũ mất", "cổng", "—"),
         ("H3-B3", "bộ parity cũ", "`tests/ledger/test_parity_*` xanh", "hồi quy", "—")],
     tf=NA_FE_TOOL, hv=["sửa tối thiểu", "MONG `so_dong_ghep_canon` mới"], ex=["H3-B1…B3 xanh", "3 vòng review xong"],
     lam="sửa nhỏ nhất tại điểm DT1b chỉ.", tep=["fls/ledger/classifying.py | fls/adapters/sao_ke_canon.py", "tools/do_voi_so_luong.py", "tests/ledger/test_hd1_lop1.py"],
     chay=[be("tests/ledger"), "python tools/do_voi_so_luong.py"])

step(id="H4", lan="BE-HC", ten="KS.CA · parity CA.GL ↔ đáp án 406 mọi kỳ (cổng HD2 đầu tiên)",
     goal="`tools/do_hd2.py --goi WP-C2` so từng ô BM–BT của CA.GL với đáp án 406 ở mọi kỳ có dữ liệu, ghi `hd2_cong.json`, và ĐỎ khi 0 ô hoặc có lát bị bỏ.",
     ap="AP v3.1.2 §3.5.4 WP-C2 (cổng 'từng ô BM–BT khớp, mọi tháng') · §5.3.1 HD2", est=(3, 4, "trung bình — dùng lại `fls/oracle/cong_parity.py`"), deps=["H1", "DT4", "DT2", "C1"],
     gom=["tool chạy H1 trên dòng sổ + `ix_fx.json` (qua `fls/cau_hinh/fx.py`)", "phân xử bằng `cong_parity.PhanXu` (≥ 1 ô, ⛔ lát bỏ, 0 lệch)", "khai hợp đồng `hd2_cong.json` cho CG2"],
     loai=["đọc tỷ giá từ kho (I2)"], moi="đối chiếu với đáp án thật (oracle) cho engine", mock="không",
     gioi_han=["tỷ giá đọc từ ảnh, ⛔ từ kho ký — I2 nối"],
     tp=dict(FE=NA_FE_TOOL, BE="`tools/do_hd2.py` · `fls/bao_cao/gl.py`", DB="không", TH="không"), tien_de=["H1", "DT4", "DT2", "C1 (`fls/cau_hinh/fx.py`)"],
     tb=[("H4-B1", "chạy WP-C2", "số ô so > 0 và = số ô của đáp án; lệch được liệt kê theo (kỳ, dòng, cột)", "cổng", "tool chưa có"),
         ("H4-B2", "đáp án rỗng", "ĐỎ `0 ô` (Đ3)", "chứng minh đỏ", "—"), ("H4-B3", "MONG lệch khai trước", "khác ⇒ ĐỎ cả hai chiều (Đ5)", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["`tools/do_hd2.py`", "`docs/ITL/_tools/hd2_cong.json` (WP-C2)"], ex=["H4-B1…B3 đúng", "lệch còn lại (nếu có) mỗi cái có tên lý do trong JSON", "3 vòng review xong"],
     lam="tool cổng + nối engine.", tep=["tools/do_hd2.py", "docs/ITL/_tools/hd2_cong.json", "tests/oracle/test_do_hd2_ca.py"],
     chay=[be("tests/oracle/test_do_hd2_ca.py"), "python tools/do_hd2.py --goi WP-C2 --ghi"])

step(id="H5", lan="BE-HC", ten="SO.CFA1 Daily: Σ theo (HD, ngày) trên cây IX.HD",
     goal="`cfa1_daily(gl, cay)` trả ô lá = Σ mUSD Nợ − Σ mUSD Có theo (HD Final, ngày) và ô cha = Σ con theo cây; cổng WP-C3a khớp đáp án 409 từng ô.",
     ap="AP v3.1.2 §3.3.1 PD 409 · §3.2.4 dòng 'cây HD theo vị trí dòng, cha = SUM con' · WP-C3", est=(3, 4, "trung bình"), deps=["H4", "C4", "DT5"],
     gom=["`fls/bao_cao/cfa.py`", "`do_hd2.py --goi WP-C3a`"], loai=["Y/H/Q/M (H6)", "HR (H7)"], moi="tổng hợp theo cây (cha = Σ con do engine)", mock="không",
     gioi_han=["cột ngày bắt đầu 21/10/2024 lấy tạm từ tham số tới khi H6 đọc IX.PER"],
     tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/cfa.py` · `tools/do_hd2.py`", DB="không", TH="không"), tien_de=["H4", "C4 (`fls/cau_hinh/hd.py`)", "DT5"],
     tb=[("H5-B1", "cây 3 nút tổng hợp", "cha = Σ hai con", "đơn vị", "chưa có"), ("H5-B2", "WP-C3a trên đáp án 409", "ô so > 0; lệch có MONG", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["`fls/bao_cao/cfa.py`", "`hd2_cong.json` + WP-C3a"], ex=["H5-B1, B2 đúng + chứng minh đỏ", "3 vòng review xong"],
     lam="hàm tổng hợp + nối cổng.", tep=["fls/bao_cao/cfa.py", "tools/do_hd2.py", "tests/bao_cao/test_cfa1.py"],
     chay=[be("tests/bao_cao/test_cfa1.py"), "python tools/do_hd2.py --goi WP-C3a"])

step(id="H6", lan="BE-HC", ten="SO Y/H/Q/M theo IX.PER",
     goal="`cuon_ky(daily, per)` cuộn Daily thành Y/H/Q/M dùng lịch IX.PER (năm từ dữ liệu); cổng WP-C3b khớp đáp án 410 · 411.",
     ap="AP v3.1.2 §3.3.1 PD 410 · 411 · IX.PER", est=(2, 4, "cao"), deps=["H5", "C6"],
     gom=["`fls/bao_cao/cfa.py` (+cuộn)", "bỏ tham số ngày đầu tạm của H5 — đọc IX.PER"], loai=["PLA"], moi="cuộn kỳ", mock="không",
     gioi_han=["—"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/cfa.py`", DB="không", TH="không"), tien_de=["H5", "C6"],
     tb=[("H6-B1", "Daily 2 ngày T11/2024 tổng hợp", "Y2024 (⛔ 2025)", "đơn vị", "chưa có"), ("H6-B2", "WP-C3b", "lệch có MONG", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["WP-C3b trong `hd2_cong.json`"], ex=["H6-B1, B2 đúng", "3 vòng review xong"],
     lam="+1 hàm cuộn.", tep=["fls/bao_cao/cfa.py", "tools/do_hd2.py", "tests/bao_cao/test_cuon_ky.py"], chay=[be("tests/bao_cao/test_cuon_ky.py")])

step(id="H7", lan="BE-HC", ten="CA.GL dòng HR + SO.CFA3",
     goal="CA.GL chạy trên dòng họ HR và CFA3 dựng theo khuôn CFA1; cổng WP-C3c khớp đáp án GL HR · CFA3 (chỉ Y2025 như AS-IS).",
     ap="AP v3.1.2 §3.3.1 PD 401–404 · 407 · 408 · 412 · 413 · Q3", est=(3, 4, "trung bình"), deps=["H6", "DT6", "C8"],
     gom=["CDT chuẩn hoá qua IX.ORG (`cdt_cua`) — ⛔ CDT Correct mặc định"], loai=["HR qua ALLOCATE (Q3 DECIDED: ⛔)"], moi="không (dùng lại H1/H5 cho họ HR)", mock="không",
     gioi_han=["chỉ 2025"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/gl.py` · `cfa.py`", DB="không", TH="không"), tien_de=["H6", "DT6", "C8 (`cdt_cua`)"],
     tb=[("H7-B1", "WP-C3c", "ô so > 0; lệch có MONG", "cổng", "chưa có"), ("H7-B2", "CDT lạ trong dòng HR", "ném lỗi có tên (⛔ SHQ2)", "đơn vị", "—")],
     tf=NA_FE_TOOL, hv=["WP-C3c"], ex=["H7-B1, B2 đúng", "3 vòng review xong"], lam="nối họ HR.",
     tep=["fls/bao_cao/gl.py", "fls/bao_cao/cfa.py", "tools/do_hd2.py", "tests/bao_cao/test_cfa3.py"], chay=[be("tests/bao_cao/test_cfa3.py")])

step(id="H8", lan="BE-HC", ten="SO.PLA1 (dồn ngày 1 tháng PL start — D4) + SO.PLA3 cộng theo khoá",
     goal="PLA1 ghi mọi số vào ngày 1 tháng PL start (D4 A) và PLA3 PM+HR = PLA1 + PLA3 HR cộng theo (HD, ngày) — ⛔ theo vị trí ô; cổng WP-C3d khớp đáp án 414–419.",
     ap="AP v3.1.2 §3.3.1 PD 414–419 · §3.5.3 D4 · §3.2.4 dòng 'PLA3 PM + HR = cộng theo VỊ TRÍ'", est=(3, 4, "trung bình"), deps=["H7", "DT7", "C6"],
     gom=["`fls/bao_cao/pla.py`"], loai=["chia đều (D4 B)"], moi="ghi nhận kỳ P&L", mock="không",
     gioi_han=["ô AS-IS tự lệch (DT7) được tách khỏi lệch FLS"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/pla.py`", DB="không", TH="không"), tien_de=["H7", "DT7", "C6 (luật A)"],
     tb=[("H8-B1", "dịch vụ PL start 2025-03-15 → end 2025-08", "toàn bộ vào 2025-03-01", "đơn vị", "chưa có"), ("H8-B2", "WP-C3d", "lệch FLS có MONG; lệch của AS-IS tách riêng", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["`fls/bao_cao/pla.py`", "WP-C3d"], ex=["H8-B1, B2 đúng", "3 vòng review xong"], lam="module PLA.",
     tep=["fls/bao_cao/pla.py", "tools/do_hd2.py", "tests/bao_cao/test_pla.py"], chay=[be("tests/bao_cao/test_pla.py")])

step(id="H9", lan="BE-HC", ten="AL.PLT · GI vendor thường + KS.AL (Σ chia = O / P)",
     goal="`chia_nen_tang(pe, o, p, ven)` chia theo RATE = PE của CDT1 ÷ Σ PE 6 CDT1 theo Vendor-tháng (O = 0 ∧ P > 0 ⇒ theo tổng tháng), Σ chia = O/P từng Vendor-tháng; cổng WP-C4a khớp MID3 GI cho vendor thường.",
     ap="AP v3.1.2 §3.4.1 PD 501–507 · §3.5.4 WP-C4", est=(3, 4, "trung bình"), deps=["H4", "C9", "DT8"],
     gom=["`fls/bao_cao/phan_bo.py`", "KS.AL: Σ chia ≠ tiền ⇒ lỗi có tên"], loai=["5 vendor đặc biệt (H10)"], moi="phân bổ nền tảng theo tỷ lệ", mock="không",
     gioi_han=["vendor đặc biệt bị bỏ qua có ĐẾM (⛔ im)"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/phan_bo.py`", DB="không", TH="không"), tien_de=["H4", "C9", "DT8"],
     tb=[("H9-B1", "Vendor-tháng 6 CDT1 tổng hợp", "Σ chia = O; RATE đúng", "đơn vị", "chưa có"), ("H9-B2", "O = 0, P > 0", "chia theo tổng tháng", "đơn vị", "—"),
         ("H9-B3", "WP-C4a", "lệch có MONG; số vendor bỏ qua = 5 mã", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["`fls/bao_cao/phan_bo.py`", "WP-C4a"], ex=["H9-B1…B3 đúng", "3 vòng review xong"], lam="module phân bổ.",
     tep=["fls/bao_cao/phan_bo.py", "tools/do_hd2.py", "tests/bao_cao/test_phan_bo.py"], chay=[be("tests/bao_cao/test_phan_bo.py")])

step(id="H10", lan="BE-HC", ten="AL.PLT · 5 vendor đặc biệt theo cột 'cách tính'",
     goal="VD341 · VD444 · VD428 · 'Max' · VD62 được tính bằng hàm chọn theo mã 'cách tính' của IX.VEN (⛔ if theo tên vendor); cổng WP-C4b khớp MID3 GI đủ mọi vendor.",
     ap="AP v3.1.2 §3.2.2 IX.VEN · §3.2.4 dòng 'VD341 · VD444 · VD428 · Max · VD62 tính riêng'", est=(3, 4, "thấp — công thức riêng cần đọc nguyên văn"), deps=["H9"],
     gom=["bảng hàm theo mã 'cách tính' (5 mã)", "mã lạ ⇒ lỗi có tên"], loai=["vendor mới"], moi="tính theo mã cấu hình", mock="không",
     gioi_han=["công thức riêng chép từ công thức AS-IS nguyên văn vào chú thích (giọng repo)"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/phan_bo.py`", DB="không", TH="không"), tien_de=["H9"],
     tb=[("H10-B1", "mỗi mã một ca tổng hợp", "đúng tay tính", "đơn vị", "chưa có"), ("H10-B2", "grep tên vendor trong `fls/bao_cao`", "0 lần (Đ1: đếm cả `fls/` lẫn `tools/`)", "kiến trúc", "—"),
         ("H10-B3", "WP-C4b", "lệch có MONG; vendor bỏ qua = 0", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["WP-C4b"], ex=["H10-B1…B3 đúng", "3 vòng review xong"], lam="bảng hàm theo mã.",
     tep=["fls/bao_cao/phan_bo.py", "tools/do_hd2.py", "tests/bao_cao/test_vendor_dac_biet.py"], chay=[be("tests/bao_cao/test_vendor_dac_biet.py")])

step(id="H11", lan="BE-HC", ten="AL.PLT · OMC · SC · PS",
     goal="Cùng engine H9/H10 chạy cho OMC · SC · PS; cổng WP-C4c khớp MID3 ba sổ, kỳ PS thiếu 03–09/2026 hiện là `chua_co_dap_an` thay vì đạt.",
     ap="AP v3.1.2 §3.4.1 PD 508–510 · 600–603", est=(2, 4, "cao"), deps=["H10", "DT9"],
     gom=["tham số hoá theo sổ (⛔ chép code)"], loai=["sửa lỗi row[45] của AS-IS"], moi="không", mock="không",
     gioi_han=["đáp án nghi lỗi (cờ DT9) tách khỏi lệch FLS"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/phan_bo.py`", DB="không", TH="không"), tien_de=["H10", "DT9"],
     tb=[("H11-B1", "WP-C4c", "3 sổ; lệch có MONG; PS 7 kỳ `chua_co_dap_an`", "cổng", "chưa có")],
     tf=NA_FE_TOOL, hv=["WP-C4c"], ex=["H11-B1 đúng + chứng minh đỏ", "3 vòng review xong"], lam="tham số hoá sổ.",
     tep=["fls/bao_cao/phan_bo.py", "tools/do_hd2.py", "tests/bao_cao/test_nen_tang_ba_so.py"], chay=[be("tests/bao_cao/test_nen_tang_ba_so.py")])

step(id="H12", lan="BE-HC", ten="AL.KEY · cờ tắt = đồng nhất; ATL khớp AS-IS (D2)",
     goal="Khi mọi cờ IX.ALR tắt, `phan_bo_khoa()` trả đúng PLA3 PM + HR (đồng nhất) và cổng WP-C5a khớp ATL 604 · 606; khi bật cờ trên dữ liệu tổng hợp, Σ chia theo driver = tiền.",
     ap="AP v3.1.2 §3.4.2 PD 500 · 511–513 · 604 · §3.5.3 D2 · D3", est=(3, 4, "trung bình"), deps=["H8", "H11", "C10", "C11", "DT10"],
     gom=["`fls/bao_cao/phan_bo_khoa.py`", "nhánh bật cờ chỉ chạy trong test tổng hợp"], loai=["bật cờ trên dữ liệu thật (owner ký)"], moi="phân bổ theo khoá driver có cờ", mock="dữ liệu tổng hợp cho nhánh bật cờ",
     gioi_han=["kỳ 2026 ⛔ có driver ⇒ chỉ đối chiếu ở cờ tắt"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/phan_bo_khoa.py`", DB="không", TH="không"), tien_de=["H8", "H11", "C10", "C11", "DT10"],
     tb=[("H12-B1", "cờ tắt", "đầu ra = đầu vào từng ô", "đơn vị", "chưa có"), ("H12-B2", "bật by NOEM tổng hợp", "Σ chia = tiền; theo driver", "đơn vị", "—"),
         ("H12-B3", "WP-C5a", "ATL khớp; lệch có MONG", "cổng", "—")],
     tf=NA_FE_TOOL, hv=["`fls/bao_cao/phan_bo_khoa.py`", "WP-C5a"], ex=["H12-B1…B3 đúng", "3 vòng review xong"], lam="module khoá.",
     tep=["fls/bao_cao/phan_bo_khoa.py", "tools/do_hd2.py", "tests/bao_cao/test_phan_bo_khoa.py"], chay=[be("tests/bao_cao/test_phan_bo_khoa.py")])

step(id="H13", lan="BE-HC", ten="SO.PLA3-ATL + IX.PL CHECK",
     goal="Dòng PL2…PL8 tính từ IX.PL trên ATL của FLS và hai phép CHECK chạy mỗi kỳ; cổng WP-C5b khớp dòng PL của đáp án và in kỳ nào CHECK đỏ.",
     ap="AP v3.1.2 §3.2.3 IX.PL · §3.4.2 PD 606", est=(2, 4, "cao"), deps=["H12", "C12"],
     gom=["dùng `fls/cau_hinh/dong_pl.py` (C12)"], loai=["báo cáo trình bày (H14)"], moi="không", mock="không",
     gioi_han=["chênh định nghĩa PL ATL ↔ Mapping Master hiện ở báo cáo cổng"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/pla.py`", DB="không", TH="không"), tien_de=["H12", "C12"],
     tb=[("H13-B1", "WP-C5b", "dòng PL khớp; CHECK đỏ kỳ nào có tên", "cổng", "chưa có")],
     tf=NA_FE_TOOL, hv=["WP-C5b"], ex=["H13-B1 đúng + chứng minh đỏ", "3 vòng review xong"], lam="nối IX.PL.",
     tep=["fls/bao_cao/pla.py", "tools/do_hd2.py", "tests/bao_cao/test_pla_atl.py"], chay=[be("tests/bao_cao/test_pla_atl.py")])

step(id="H14", lan="BE-HC", ten="RP.CF · RP.PL · Daily Report 2 · 3 theo bản A-CCR (D5)",
     goal="`daily_report(ky, fs)` dựng Daily Report 2 · 3 với FS là tham số (D5 A) và cổng WP-C5c khớp đáp án 607–616 từng ô; đầu ra là JSON ô đưa được vào C13.",
     ap="AP v3.1.2 §3.3.2 PD 605–617 · §3.5.3 D5 · §5.3.1 HD2", est=(3, 4, "trung bình"), deps=["H13", "DT11", "C13"],
     gom=["`fls/bao_cao/bao_cao.py`", "JSON ô theo hợp đồng của C13"], loai=["ghi CCR / PDF (HD4 — ngoài ISP)"], moi="dựng báo cáo theo khuôn", mock="không",
     gioi_han=["ô chỉnh tay AS-IS (ATL AH12 '− 0.5') tính là lệch có tên 'chỉnh tay ⛔ actor', ⛔ chép vào config"], tp=dict(FE=NA_FE_TOOL, BE="`fls/bao_cao/bao_cao.py`", DB="không", TH="không"), tien_de=["H13", "DT11", "C13 (hợp đồng JSON ô của bản ký)"],
     tb=[("H14-B1", "WP-C5c", "ô so > 0; lệch có MONG; ô chỉnh tay liệt kê", "cổng", "chưa có"), ("H14-B2", "FS = FS1/FS2/FS3", "cùng engine, khác tham số", "đơn vị", "—")],
     tf=NA_FE_TOOL, hv=["`fls/bao_cao/bao_cao.py`", "WP-C5c"], ex=["H14-B1, B2 đúng", "3 vòng review xong"], lam="module báo cáo.",
     tep=["fls/bao_cao/bao_cao.py", "tools/do_hd2.py", "tests/bao_cao/test_daily_report.py"], chay=[be("tests/bao_cao/test_daily_report.py")])

step(id="H15", lan="BE-HC", ten="HD1 · tự sinh theo từng kỳ (AC10 · AC11 cho 22 kỳ còn lại)",
     goal="`do_voi_so_luong.py` chạy chế độ tự sinh (FLS tự tính MID) trên mọi kỳ có ảnh Manual input và ghi `tu_sinh` theo kỳ; kỳ ⛔ có ảnh hiện `chua_do` thay vì đạt.",
     ap="AP v3.1.2 §5.3.2 AC10 · AC11 · §5.3.1 HD1", est=(3, 4, "trung bình — đường tự sinh đã chạy trên 2026-03 (584/584 HD)"), deps=["H3", "DT12"],
     gom=["lặp `do_tu_sinh()` theo kỳ; MONG theo kỳ khai sau lần đo đầu"], loai=["sửa lệch MID tự sinh (4.020/4.088 ở 2026-03) — mỗi lớp là một bước riêng nếu cần"], moi="không (mở rộng đường tự sinh có sẵn)", mock="không",
     gioi_han=["kỳ DT12 đọc hỏng = `chua_do`"], tp=dict(FE=NA_FE_TOOL, BE="`tools/do_voi_so_luong.py` · `fls/oracle/tu_soi.py` (đọc)", DB="không", TH="không"), tien_de=["H3", "DT12"],
     tb=[("H15-B1", "chạy mọi kỳ", "`tu_sinh` có ở ≥ 1 kỳ ngoài 2026-03 hoặc DT12 cho 0 kỳ ⇒ ĐỎ có tên", "cổng", "chưa có"), ("H15-B2", "kỳ 2026-03", "HD 584/584 giữ nguyên (hồi quy)", "hồi quy", "—")],
     tf=NA_FE_TOOL, hv=["`voi_so_luong.json` + `tu_sinh` theo kỳ"], ex=["H15-B1, B2 đúng", "3 vòng review xong"], lam="vòng theo kỳ.",
     tep=["tools/do_voi_so_luong.py", "docs/ITL/_tools/voi_so_luong.json", "tests/oracle/test_tu_sinh_theo_ky.py"], chay=[be("tests/oracle/test_tu_sinh_theo_ky.py"), "python tools/do_voi_so_luong.py --ghi"])

# ═════════════ FE ═════════════
FE_RUN = "`.venv/bin/python -m pytest tests/web/{t}` (node headless qua `tests/web/khung_node.py` + `dom_gia.js`)"
step(id="FG", lan="FE", ten="F03 'Cổng hôm nay' hiện cổng HD1 (đọc tuyến thật)",
     goal="Mở F03 thấy thẻ `FINAL` ĐẠT, thẻ `HD1_THANG` KHÔNG ĐẠT kèm '5/23 kỳ đạt' và danh sách kỳ đỏ trong lý do — đúng như `GET /gates` trả; tệp đo vắng thì hai thẻ 'KHÔNG ĐO ĐƯỢC', ⛔ xanh.",
     ap="AP v3.1.2 §5.2 UF-2 · §5.3.1 HD1 · Figure 5.3.3",
     est=(2, 3, "cao — ⭐ F03 đã vẽ ba trạng thái (`_muc`, lớp `.gate.unk`) cho mọi cổng của `/gates`; có thể chỉ cần bài kiểm + gấp lý do dài"),
     deps=["CG1"],
     gom=["bài DOM + bài qua máy chủ thử cho hai thẻ mới", "nếu `ly_do` dài (≤ 23 kỳ) vỡ thẻ: gấp/mở trong thẻ — sửa tối thiểu ở `man_f03.js`"],
     loai=["màn mới (phương án A bỏ F09)", "khoan xuống từng dòng"],
     moi="không — màn F03 sẵn có hiển thị cổng mới", mock="không (tuyến thật, tệp đo tĩnh)",
     gioi_han=["thẻ HD2 'KHÔNG ĐO ĐƯỢC' tới khi CG2 + H4 xong — đúng nghĩa"],
     tp=dict(FE="`fls/web/tep/man_f03.js` (chỉ nếu lý do dài vỡ thẻ) · bài `tests/web`", BE="tuyến `/gates` + CG1 (dùng, ⛔ sửa)", DB="không", TH="máy chủ thử `fls/web/phuc_vu.py`"),
     tien_de=["CG1", "S0 (bộ test web)"],
     tb=[("FG-B1", "N/A — tuyến có bài ở CG1", "—", "—", "—")],
     tf=[("FG-F1", "mở F03 qua máy chủ thử với tệp đo thật", "thẻ `FINAL` ĐẠT; `HD1_THANG` KHÔNG ĐẠT · '5/23'; số 'chưa đo được' khớp tuyến", "tích hợp headless", "thẻ chưa có"),
         ("FG-F2", "tệp đo vắng", "hai thẻ lớp `.gate.unk` 'KHÔNG ĐO ĐƯỢC'", "tích hợp", "—"),
         ("FG-F3", "lý do 23 kỳ ở bề rộng 390 px", "⛔ tràn ngang", "DOM", "—"),
         ("FG-F4", "bộ `tests/web` sẵn có (token màu, một bản mẫu, phím)", "xanh", "hồi quy web", "—")],
     hv=["2 thẻ cổng mới trên F03"],
     ex=["FG-F1…F4 đúng", "3 vòng review xong"],
     lam="bài kiểm + (nếu cần) gấp lý do trong thẻ.",
     tep=["fls/web/tep/man_f03.js", "tests/web/test_isp_f03_hd.py"],
     chay=[FE_RUN.format(t="test_isp_f03_hd.py"), "`.venv/bin/python -m pytest tests/web`"])

step(id="F4", lan="FE", ten="SCR-F08 Cấu hình · bảng IX.FX chỉ đọc trên tuyến thật",
     goal="Mở màn Cấu hình thấy bảng tỷ giá theo tháng từ `GET /config/fx`, tháng thiếu/trùng/lạc mang nhãn riêng (CHẶN · TRÙNG · LẠC).",
     ap="AP v3.1.2 §3.2.1 IX.FX · §3.2.4 · §3.5.3 D1",
     est=(3, 4, "trung bình — ⭐ ghép từ `goi_cua.js` · `trang_thai.js` · `thanh_phan.js` · `tokens.css`; khai tệp ở bảng `fls/web/phuc_vu.py`"),
     deps=["C5"],
     gom=["`man_f08.js` + khai ở BẢNG TỆP `fls/web/phuc_vu.py` (cổng `kiem_bang_tep`) + mục ở `ung_dung.js` / `index.html`",
          "bốn trạng thái qua `trang_thai.js`; màu chỉ từ token (bài `test_khong_ma_mau_go_tay.py`)"],
     loai=["ký (F5)"], moi="màn mới SCR-F08", mock="không",
     gioi_han=["mã F08 cần BA đăng ký (O9)"],
     tp=dict(FE="`fls/web/tep/man_f08.js` · `ung_dung.js` · `index.html` · `fls/web/phuc_vu.py`", BE="tuyến C1/C5 (dùng)", DB="kho test (C5)", TH="máy chủ thử"),
     tien_de=["C5", "O9 (fls-ba đăng ký mã SCR-F08)", "S0 (bộ test web)"],
     tb=[("F4-B1", "N/A — tuyến có bài ở C1/C5", "—", "—", "—")],
     tf=[("F4-F1", "mở màn trên kho có ảnh FX", "37 dòng; 202306 nhãn LẠC", "tích hợp headless (pg)", "chưa có"),
         ("F4-F2", "kho thiếu 202408 (dữ liệu test)", "nhãn CHẶN ở 202408", "tích hợp", "—"),
         ("F4-F3", "`kiem_bang_tep` + token màu + bản mẫu", "xanh", "hồi quy", "—")],
     hv=["SCR-F08"], ex=["F4-F1…F3 đúng", "3 vòng review xong"], lam="một màn + một dòng bảng tệp.",
     tep=["fls/web/tep/man_f08.js", "fls/web/tep/ung_dung.js", "fls/web/tep/index.html", "fls/web/phuc_vu.py", "tests/web/test_isp_f08_fx_pg.py"],
     chay=[FE_RUN.format(t="test_isp_f08_fx_pg.py")])

step(id="F5", lan="FE", ten="SCR-F08 ký tháng tỷ giá (D1) có hộp xác nhận",
     goal="Bấm 'Ký tháng' ở một tháng chưa ký, xác nhận trong hộp thoại, thấy tháng chuyển 'đã ký · người ký (từ token) · ngày' và nút khoá; ký lại báo 409 bằng chữ.",
     ap="AP v3.1.2 §3.5.3 D1 · §3.2.4", est=(3, 4, "trung bình — hộp thoại theo `hop_thoai.js`"), deps=["F4", "C7"],
     gom=["nút + hộp xác nhận + khoá sau ký", "mã lỗi 403/409 có chữ (bài `test_goi_cua_phu_het_ma_loi.py`)"], loai=["huỷ ký"], moi="hành động ghi từ màn cấu hình", mock="không",
     gioi_han=["người ký lấy từ token của phiên (`phien.js` ↔ `the.py`); ⛔ phân quyền theo vai (O11)"], tp=dict(FE="`man_f08.js`", BE="tuyến C7 (dùng)", DB="kho test", TH="máy chủ thử"), tien_de=["F4", "C7"],
     tb=[("F5-B1", "N/A — tuyến có bài ở C7", "—", "—", "—")],
     tf=[("F5-F1", "ký 202510", "hộp xác nhận → 'đã ký'; nút khoá", "tích hợp headless (pg)", "chưa có"), ("F5-F2", "ký lại", "chữ lỗi 409", "tích hợp", "—"),
         ("F5-F3", "huỷ ở hộp xác nhận", "⛔ gọi POST", "DOM", "—")],
     hv=["nút ký SCR-F08"], ex=["F5-F1…F3 xanh", "3 vòng review xong"], lam="nút + hộp + gọi POST.",
     tep=["fls/web/tep/man_f08.js", "tests/web/test_isp_f08_ky_pg.py"], chay=[FE_RUN.format(t="test_isp_f08_ky_pg.py")])

step(id="F7", lan="FE", ten="SCR-F08 ký bản Daily Report 3 (IX.TMP snapshot)",
     goal="Ở SCR-F08, kỳ có bản báo cáo hiện danh sách phiên bản (checksum · trạng thái · người ký); bấm 'Ký bản' ký phiên bản mới nhất, phiên bản cũ đã ký giữ nguyên.",
     ap="AP v3.1.2 §3.2.3 IX.TMP · §3.2.4 dòng 'sign-off dán value'",
     est=(2, 3, "cao — dùng lại hộp ký của F5 trên cùng màn"),
     deps=["F5", "C13"],
     gom=["danh sách phiên bản + nút ký (hộp xác nhận của F5)"], loai=["xem nội dung báo cáo từng ô", "PDF"], moi="hiển thị phiên bản có ký", mock="không",
     gioi_han=["nội dung bản là của engine H14 khi I2 chạy; trước đó là bản tổng hợp của C13"],
     tp=dict(FE="`fls/web/tep/man_f08.js`", BE="tuyến C13 (dùng)", DB="kho test", TH="máy chủ thử"),
     tien_de=["C13", "F5 (hộp ký)"],
     tb=[("F7-B1", "N/A — tuyến có bài ở C13", "—", "—", "—")],
     tf=[("F7-F1", "kỳ có 2 phiên bản (1 đã ký)", "ký bản 2 → cả hai 'đã ký', checksum khác nhau", "tích hợp headless (pg)", "chưa có")],
     hv=["danh sách phiên bản + ký trên SCR-F08"], ex=["F7-F1 đúng", "3 vòng review xong"], lam="danh sách + nút.",
     tep=["fls/web/tep/man_f08.js", "tests/web/test_isp_f08_ky_ban_pg.py"], chay=[FE_RUN.format(t="test_isp_f08_ky_ban_pg.py")])

# ═════════════ tích hợp cuối ═════════════
step(id="I1", lan="DATA", ten="Tích hợp HD1 xuyên suốt: ảnh → ghép → cổng theo kỳ → `GET /gates` → F03",
     goal="Một bài tích hợp chạy từ ba ảnh đóng băng qua ghép FLS, nhãn lý do, cổng HD1 theo kỳ (kể cả tự sinh), `GET /gates` và màn F03, và kết luận AC10 · AC11 khớp nhau ở mọi tầng.",
     ap="AP v3.1.2 §5.3.1 HD1 · §5.3.2 AC10 · AC11 · HD5", est=(3, 4, "trung bình"), deps=["H15", "H3", "CG1", "FG"],
     gom=["bài `tests/tich_hop/test_hd1_xuyen_suot.py`: tầng cổng ↔ JSON ↔ `/gates` ↔ thẻ F03 cùng một số", "đường lỗi: tệp đo vắng ⇒ API 503 ⇒ màn khối lỗi; sổ lý do có chữ ký giả ⇒ kỳ đổi xanh ở cả 3 tầng"],
     loai=["chữ ký thật (O8)"], moi="không (tích hợp)", mock="chữ ký lý do giả trong bài (biên ghi rõ)",
     gioi_han=["số là của ảnh 26/08; đọc kho sống (HD5) ngoài ISP"], tp=dict(FE="F03 qua máy chủ thử", BE="cổng `do_voi_so_luong.py` + `/gates` (CG1)", DB="không", TH="máy chủ thử"), tien_de=["H15", "H3", "CG1", "FG"],
     tb=[("I1-B1", "cổng → JSON → `/gates`", "số kỳ đạt và danh sách kỳ đỏ giống nhau ở 3 tầng; nhãn DT1b có trong `ly_do`", "tích hợp", "chưa có"), ("I1-B2", "tệp đo vắng", "`/gates`: `FINAL` + `HD1_THANG` `dat = null`", "tích hợp lỗi", "—")],
     tf=[("I1-F1", "F03", "thẻ `HD1_THANG` ghi đúng x/23 như cổng", "tích hợp headless", "—"), ("I1-F2", "đường lỗi", "thẻ KHÔNG ĐO ĐƯỢC", "tích hợp", "—")],
     hv=["`tests/tich_hop/test_hd1_xuyen_suot.py`", "bảng AC10/AC11 theo kỳ dán vào BG"], ex=["I1-B1, B2, F1, F2 xanh", "toàn bộ cổng CLAUDE.md chạy, kết quả thật dán vào BG", "3 vòng review xong"],
     lam="một bài tích hợp.", tep=["tests/tich_hop/test_hd1_xuyen_suot.py"], chay=[be("tests/tich_hop/test_hd1_xuyen_suot.py")])

step(id="I2", lan="BE-HC", ten="Tích hợp HD2 xuyên suốt: config ký trong kho → GL → CFA/PLA → phân bổ → báo cáo → ký bản",
     goal="Một bài tích hợp nạp config vào kho, ký tỷ giá các tháng, chạy chuỗi engine CA→SO→AL→RP với `fx_cua()` thật, so mọi gói WP-C2…C5 với đáp án và ký bản Daily Report 3 — và tháng chưa ký tỷ giá CHẶN cả chuỗi có tên.",
     ap="AP v3.1.2 §5.3.1 HD2 · §5.3.2 AC9 · §3.5.4 WP-C1…C5 · D1 · D2 · D5", est=(3, 4, "trung bình"), deps=["H14", "C13", "CG2", "F7", "I1"],
     gom=["`tests/tich_hop/test_hd2_xuyen_suot.py` (pg)", "đường lỗi: bỏ ký 1 tháng ⇒ `FX_CHAN` ở GL ⇒ cổng `HD2_WP_C2` `dat = false` ⇒ thẻ F03 đỏ", "chạy lại trên máy owner (`fls-pg-1`, chỉ đọc) trước merge — O4"],
     loai=["bật cờ luật", "ghi CCR/PDF", "agent"], moi="không (tích hợp)", mock="actor ký là actor test",
     gioi_han=["kho test; bản owner chạy lại là điều kiện MERGE, ⛔ điều kiện xong bước"], tp=dict(FE="F03 thẻ HD2 + SCR-F08 ký bản", BE="toàn chuỗi engine + tuyến", DB="kho test (0027)", TH="máy chủ thử"), tien_de=["H14", "C13", "CG2", "F7", "I1"],
     tb=[("I2-B1", "chuỗi đủ", "mỗi gói: số ô so = số ô đáp án; lệch = MONG đã khai ở từng bước", "tích hợp (pg)", "chưa có"),
         ("I2-B2", "bỏ ký 202510", "`FX_CHAN 202510` xuyên chuỗi; ⛔ số nào ra cho tháng ấy", "tích hợp lỗi", "—"),
         ("I2-B3", "ký bản 2025-12 từ đầu ra H14", "phiên bản có checksum = checksum JSON ô", "tích hợp", "—")],
     tf=[("I2-F1", "F03 sau chuỗi đủ", "4 thẻ HD2 có số; ⛔ 'KHÔNG ĐO ĐƯỢC'", "tích hợp headless", "—"), ("I2-F2", "sau bỏ ký", "thẻ `HD2_WP_C2` đỏ có chữ", "tích hợp", "—")],
     hv=["`tests/tich_hop/test_hd2_xuyen_suot.py`", "báo cáo HD2 theo gói dán vào BG"], ex=["I2-B1…B3, F1, F2 xanh", "toàn bộ cổng CLAUDE.md xanh hoặc đỏ-có-sẵn đã ghi ở S0", "3 vòng review xong", "điều kiện MERGE (khác điều kiện xong): chạy lại trên máy owner + ThuongCT ký (O6)"],
     lam="một bài tích hợp.", tep=["tests/tich_hop/test_hd2_xuyen_suot.py"], chay=[ENV, be("tests/tich_hop/test_hd2_xuyen_suot.py"), be("")])

# ───────────────────────── quyết định mở ─────────────────────────
QD = [
    ("O1", "✅ ĐÃ GỠ 16/11 — push từng bị chặn 403; đo lúc nộp ISP: push `5b35284..0ce05f8` thành công",
     "—", "—", "— (giữ luật: chỉ push nhánh làm việc, chỉ sau R3)", "không còn chặn"),
    ("O2", "Nhánh làm việc",
     "A · mỗi agent một worktree cục bộ, nhánh cục bộ `isp/<bước>` (⛔ push); sau R3 orchestrator gộp vào `claude/laughing-bohr-331pt0` rồi push; PR vào main chỉ khi bạn duyệt",
     "B · push từng nhánh `claude/laughing-bohr-331pt0-<bước>` lên remote — được: thấy trên GitHub · mất: cần bạn cho phép push nhánh khác",
     "A", "B cần quyền rõ ràng (luật phiên: chỉ push nhánh đã giao)"),
    ("O3", "`/process-issues` cần bảng ReportIssue + gấp vào AP; dự án ⛔ có bảng ấy",
     "A · R1 chạy triage A1/A2/B1/B2 của process-issues trên phát hiện review, ghi `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.md` + một dòng 'luật phòng tái phạm' cho bước sau đọc; chỉ phát hiện làm đổi AP mới gấp vào bản AP vá (gom theo wave, ISP cùng số §A.30)",
     "B · mỗi phát hiện một bản AP mới — được: đúng nguyên skill · mất: ~50 bản AP, nhiễu",
     "A", "Sổ phát hiện là bằng chứng 'đã chạy process-issues' của R1"),
    ("O4", "Nơi chạy test",
     "A · container cloud này: PG16 cục bộ :5433 (đo: có binary, PyPI vào được) — được: cô lập, lặp lại được · mất: ⛔ phải `fls-pg-1` thật",
     "B · máy Windows của owner với `fls-pg-1` — được: kho thật · mất: agent cloud ⛔ chạm được",
     "A cho mọi bước + chạy lại I2 trên máy owner trước merge", "Ảnh hưởng S0 và điều kiện merge"),
    ("O5", "Lưu config: một cặp bảng chỉ-thêm có phiên bản dùng chung, hay một bảng gõ kiểu cho mỗi IX.*",
     "A · dùng chung (`fls_cau_hinh_ban` + `fls_cau_hinh_dong` jsonb) — được: một khái niệm, một di trú, ít sửa ERD · mất: kiểu dữ liệu kiểm ở tầng `fls/cau_hinh` thay vì DDL",
     "B · 10 bảng gõ kiểu — được: DDL chặt · mất: 10 di trú + 10 lần sinh lại ERD/golden",
     "A", "Đổi C5…C13; B thêm ~1 bước mỗi bảng"),
    ("O6", "AP v3.1.2 ghi duyệt theo lời bạn trong phiên; AP ghi Owner là ThuongCT",
     "A · chạy Wave 0–n trên nhánh (đảo ngược được), ThuongCT ký trước MERGE vào main",
     "B · chờ ThuongCT ký trước Wave 0", "A", "Chỉ chặn merge"),
    ("O7", "Agent con có thể ⛔ có công cụ Google Drive/Sheets",
     "A · orchestrator (phiên này) đọc giá trị sheet chỉ-đọc vào scratchpad; DATA đóng băng từ bản ấy; bản thô ⛔ commit; cổng PII chặn cột cấm",
     "B · cấp công cụ Drive cho agent DATA — được: tự chủ · mất: chưa chắc khả dụng; rộng quyền", "A", "Chặn DT1b · DT2…DT12"),
    ("O8", "Ai ký 'lệch có tên lý do' của HD1",
     "A · ThuongCT ký sổ `so_ly_do_hd1.json`; chưa ký = đỏ", "B · operator ký thay", "A", "Quyết định số kỳ đạt HD1 thật"),
    ("O9", "AP v3.1.2 ⛔ có wireframe cho SCR-F08; F05–F07 đã dùng/khai tử ở `06_SCREEN_SPEC`",
     "A · SCR-F08 theo khuôn F04; fls-ba đăng ký mã F08 trước F4 (F09 đã bỏ theo phương án A)",
     "B · BA vẽ wireframe đầy đủ trước — được: chặt · mất: FE chờ ≥ 1 wave", "A", "Chặn F4"),
    ("O10", "DT1b cần cột khoá (Số CT · PS Nợ/Có · TK · tiền tệ) của sổ AS-IS — ảnh trong repo đã bỏ chúng; mã ghép gốc ⛔ có trong repo",
     "A · orchestrator đọc qua connector nếu tài khoản vào được RAW `1md85t…` + cột khoá; nếu ⛔, owner chạy `tools/phan_loai_dong_thieu.py --khoa` trên máy có `Input_Raw/[Master] ITL_Ledge_raw.xlsx`, chỉ gửi về JSON khoá đã băm",
     "B · dựng lại mã ghép đọc sống trong repo — được: lặp lại được · mất: +1–2 bước, cần khoá Sheets ở container", "A", "Chặn DT1b → H3 → I1"),
    ("O11", "Ai được ký tháng tỷ giá / bản báo cáo — AP D1 ghi 'owner ký', repo ⛔ có phân quyền theo vai",
     "A · mọi token hợp lệ ký được, người ký ghi lại từ token — đủ khi máy chỉ mở `127.0.0.1` (`GAP-WEB-01`)",
     "B · thêm danh sách người được ký (config) — được: đúng chữ D1 · mất: +1 bước", "A", "C7 · C13 · F5 · F7"),
]

BUOC_BAT_BUOC = ["id", "lan", "ten", "goal", "ap", "est", "deps", "gom", "loai", "moi", "mock", "gioi_han", "tp", "tien_de", "tb", "tf", "hv", "ex", "lam", "tep", "chay"]


def kiem() -> list[str]:
    loi = []
    ids = [b["id"] for b in B]
    if len(set(ids)) != len(ids):
        loi.append("id trùng")
    for b in B:
        for k in BUOC_BAT_BUOC:
            if k not in b or (k != "deps" and b[k] in (None, "", [])):   # deps rỗng hợp lệ (Step 0)
                loi.append(f"{b.get('id')}: thiếu {k}")
        for d in b.get("deps", []):
            if d not in ids:
                loi.append(f"{b['id']}: phụ thuộc {d} ⛔ có")
            # Preconditions phải nhắc MỌI phụ thuộc — hai nơi khai một sự thật thì máy giữ chúng khớp
            if not any(d in t for t in b.get("tien_de", [])):
                loi.append(f"{b['id']}: phụ thuộc {d} ⛔ có trong Preconditions")
        if b["est"][1] > 4:
            loi.append(f"{b['id']}: ước lượng {b['est'][1]}h > 4h")
        if b["lan"] not in LAN:
            loi.append(f"{b['id']}: làn lạ")
        for k in ("FE", "BE", "DB", "TH"):
            if not b["tp"].get(k):
                loi.append(f"{b['id']}: Components thiếu {k}")
        if isinstance(b["tf"], str) and not b["tf"].startswith("N/A"):
            loi.append(f"{b['id']}: FE chuỗi mà ⛔ N/A")
        # ⛔ Đã cắn 16/11: H10 thêm gói WP-C4b vào `tools/do_hd2.py` mà ⛔ khai tệp ⇒ lịch xếp nó
        # chạy cùng ô với H7 (cũng sửa tệp ấy). Bước engine nào thêm cổng WP phải khai tệp cổng.
        if b["id"].startswith("H") and re.search(r"WP-C\d", b["goal"]) and "tools/do_hd2.py" not in tep_cua(b):   # I2 chỉ ĐỌC cổng
            loi.append(f"{b['id']}: thêm cổng WP mà ⛔ khai `tools/do_hd2.py`")
    # chu trình
    thu_tu, tham = [], {}

    def dfs(x, duong):
        if tham.get(x) == 1:
            loi.append(f"chu trình qua {x}")
            return
        if tham.get(x) == 2:
            return
        tham[x] = 1
        for d in next(b for b in B if b["id"] == x)["deps"]:
            if d in ids:
                dfs(d, duong + [x])
        tham[x] = 2
        thu_tu.append(x)

    for i in ids:
        dfs(i, [])
    # Quyền ghi: mọi tệp một bước chạm phải thuộc LÀN GỐC của bước (hoặc tệp dùng chung đã khai cho
    # đúng bước ấy). Agent FE nhận bước BE thì mượn quyền của làn gốc — ⛔ quyền riêng.
    for b in B:
        mau = [re.sub(r"\s*\(.*$", "", m).replace("**", "*") for m in LAN[b["lan"]]["so_huu"]]
        for t in tep_cua(b):
            if DUNG_CHUNG.get(t) == b["id"]:
                continue
            if not any(fnmatch.fnmatch(t, m) for m in mau):
                loi.append(f"{b['id']}: tệp `{t}` ⛔ thuộc làn {b['lan']}")
    # Lịch: mỗi agent ≤ 1 bước/ô và ⛔ hai bước cùng ô chạm chung một tệp
    if not loi:
        W, AG = lich()
        by = {b["id"]: b for b in B}
        for o in set(W.values()):
            cung = [i for i in W if W[i] == o]
            if len({AG[i] for i in cung}) != len(cung):
                loi.append(f"W{o}: một agent hai bước")
            for x in range(len(cung)):
                for y in range(x + 1, len(cung)):
                    chung = tep_cua(by[cung[x]]) & tep_cua(by[cung[y]])
                    if chung:
                        loi.append(f"W{o}: {cung[x]} và {cung[y]} cùng chạm {sorted(chung)}")
            for i in cung:
                if AG[i] != by[i]["lan"] and not (AG[i] == "FE" and by[i]["lan"] in FE_NHAN):
                    loi.append(f"{i}: agent {AG[i]} ⛔ được nhận bước làn {by[i]['lan']}")
    sha = hashlib.sha256(AP.read_bytes()).hexdigest()
    if sha != AP_SHA:
        loi.append(f"AP sha256 {sha[:12]}… ≠ khai {AP_SHA[:12]}…")
    return loi


# ★ HD1 đi trước đường găng: owner 16/11 đặt "mapping 100% giống quá khứ" lên đầu (AP §5.3.1 HD1 ★).
UU_TIEN = {"DT1a", "DT1b", "H2", "H3", "CG1", "FG"}


# ★ Người dùng 16/11: *"Sau khi chạy xong thì agent FE sẽ nhận job từ agents BE"*.
#   Đọc thành luật: agent FE làm bước FE khi có bước FE SẴN SÀNG; ⛔ có thì nhận một bước BE sẵn sàng
#   (làn BE-CF hoặc BE-HC) mà ⛔ đụng tệp của bước đang chạy cùng ô. Bước vẫn MỘT owner (giao lại,
#   ⛔ giao trùng); quyền ghi tệp của bước đi theo LÀN GỐC trong thời gian bước chạy.
FE_NHAN = ("BE-CF", "BE-HC")


def tep_cua(b: dict) -> set[str]:
    return {t.strip() for x in b["tep"] for t in x.split("|")}


def lich() -> tuple[dict[str, int], dict[str, str]]:
    """List scheduling theo AGENT: mỗi agent một bước/ô; ưu tiên HD1 (UU_TIEN), rồi đường dài nhất còn lại."""
    by = {b["id"]: b for b in B}
    con = {i: [b["id"] for b in B if i in b["deps"]] for i in by}
    dai: dict[str, int] = {}

    def L(i):
        if i not in dai:
            dai[i] = 1 + max((L(c) for c in con[i]), default=0)
        return dai[i]

    for i in by:
        L(i)
    xong: dict[str, int] = {}
    ag: dict[str, str] = {}
    o = 0
    while len(xong) < len(by):
        san = sorted((i for i in by if i not in xong and all(d in xong and xong[d] < o for d in by[i]["deps"])),
                     key=lambda i: (i not in UU_TIEN, -dai[i], i))
        ban: dict[str, str] = {}
        dang: list[str] = []
        dung = lambda i: any(tep_cua(by[i]) & tep_cua(by[j]) for j in dang)
        for i in san:                                   # ① agent của làn nhận bước làn mình
            lan = by[i]["lan"]
            if lan not in ban and not dung(i):
                ban[lan] = i
                dang.append(i)
        if "FE" not in ban:                             # ② FE ⛔ có bước FE sẵn sàng ⇒ nhận bước BE
            for i in san:
                if i not in dang and by[i]["lan"] in FE_NHAN and not dung(i):
                    ban["FE"] = i
                    dang.append(i)
                    break
        for a_, i in ban.items():
            xong[i], ag[i] = o, a_
        o += 1
        if o > 200:
            raise SystemExit("⛔ lịch ⛔ hội tụ")
    return xong, ag


def md_bang(cot, hang) -> str:
    esc = lambda s: str(s).replace("|", "\\|").replace("\n", " ")
    out = ["| " + " | ".join(cot) + " |", "|" + "---|" * len(cot)]
    out += ["| " + " | ".join(esc(x) for x in h) + " |" for h in hang]
    return "\n".join(out)


def sinh() -> str:
    W, AG = lich()
    THU_AG = ["BE-HC", "BE-CF", "FE", "DATA"]
    so = {b["id"]: n for n, b in enumerate(sorted(B, key=lambda b: (W[b["id"]], THU_AG.index(AG[b["id"]]) if b["id"] != "S0" else -1, b["id"])))}
    ag_ten = lambda i: LAN[AG[i]]["agent"]
    muon = lambda i: AG[i] != by_id[i]["lan"]          # agent FE đang làm bước của làn BE
    by_id = {b["id"]: b for b in B}
    ten_buoc = lambda i: f"Step {so[i]} · {i}"
    B_sap = sorted(B, key=lambda b: so[b["id"]])
    tong_lo = sum(b["est"][0] for b in B)
    tong_hi = sum(b["est"][1] for b in B)
    so_wave = max(W.values()) + 1
    theo_lan = {l: sum(1 for b in B if b["lan"] == l) for l in LAN}
    theo_ag = {l: sum(1 for b in B if AG[b["id"]] == l) for l in LAN}
    fe_muon = [b["id"] for b in B if AG[b["id"]] == "FE" and b["lan"] != "FE"]
    # đường găng
    by = {b["id"]: b for b in B}
    con = {i: [b["id"] for b in B if i in b["deps"]] for i in by}
    memo = {}

    def dai(i):
        if i not in memo:
            memo[i] = 1 + max((dai(c) for c in con[i]), default=0)
        return memo[i]

    goc = max(by, key=dai)
    gang = [goc]
    while con[gang[-1]]:
        gang.append(max(con[gang[-1]], key=dai))
    out = []
    A = out.append
    A(f"# IncrementalStepPlan-FLS-Voi v3.1.2")
    A("")
    A(f"> **ISP v3.1.2** — cùng số với AP nó thực thi (apr-build-ap §A.30). Sinh bởi `docs/ITL/_tools/sinh_isp_voi.py` ({NGAY}); "
      "bộ sinh ĐỎ khi bước thiếu trường, phụ thuộc trỏ vào bước không có, DAG có chu trình, ước lượng > 4h, hoặc AP ghim sai sha256.")
    A("> ⛔ **Chưa triển khai.** Đây là bản chia bước để bạn duyệt. Không bước nào được chạy trước khi bạn xác nhận breakdown này.")
    A("")
    A("## 1. Phần đầu kế hoạch")
    A("")
    A(md_bang(["Mục", "Giá trị"], [
        ("Project", "FLS — sổ cái ITL code hoá · lõi config chung (báo cáo + phân bổ) và HD1 'mapping 100% giống quá khứ'"),
        ("Ngày lập", NGAY),
        ("AP baseline", f"`docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` · v3.1.2 · sha256 `{AP_SHA}` · bản vá chỉ trỏ: 0 đơn vị đổi thân, 64/64 `approved · {NGAY}` (duyệt ở v3.1.1) · 0 lỗi ở 4 bộ kiểm"),
        ("Phiên bản ISP", "3.1.2 (= AP). v3.1.1 đóng băng; v3.1.2 = so sánh mã ↔ ISP 16/11 + hai lựa chọn của người dùng"),
        ("Thay đổi so với ISP 3.1.1", "người dùng: *\"Chọn A. Sau khi chạy xong thì agent FE sẽ nhận job từ agents BE\"* → bỏ màn F09 + tuyến C2 · C3 · C14 + khối F6, thay bằng cổng HD1/HD2 trong `GET /gates` sẵn có (CG1 · CG2) và thẻ trên màn F03 sẵn có (FG); F7 chuyển sang SCR-F08; DT1 tách DT1a (offline) / DT1b (khoá); 8 bước hạ ước lượng nhờ mã có sẵn; sửa 8 lỗi đọc ra từ mã (§1.3); agent FE nhận bước BE khi ⛔ có bước FE sẵn sàng (§2.1)"),
        ("Duyệt AP", "người dùng phiên 16/11: *\"Duyệt AP, đồng ý với các recommendation\"* → 15 nhãn RECOMMENDED thành DECIDED (§2.1.1 · §2.1.2 · D1–D5 · Q1–Q6) ở v3.1.1; ThuongCT ký trước merge (O6)"),
        ("Project instructions", "`CLAUDE.md` (Đ1–Đ5, cổng, bẫy, riêng tư) · `docs/ITL/01_Orchestrator/10_HOP_DONG_AGENT.md` (vai, phiếu WO/HOI·TL/BG/KQ)"),
        ("Repo / nhánh", "`kc-apero/FLS-tobe` · nhánh làm việc `claude/laughing-bohr-331pt0` (đồng bộ remote — đo 16/11: push `5b35284..0ce05f8` thành công, lỗi 403 cũ đã hết) · main ⛔ commit thẳng"),
        ("Trạng thái hệ thống", "**đang có, có lỗi đã đo**: 40 dòng `Tuyen(` ở `fls/api/bang_tuyen.py` · di trú 0001–0026 · 18 bảng (17 qua di trú + `fls_migration`) · 7 view (8 tạo, 0009 bỏ `fls_queue_xep_tien`) · màn F01 (3 tệp) · F02 · F03 *Cổng hôm nay* · F04 · 6 ảnh đóng băng ở `tests/fixture/` · 2.044 hàm `def test_` (đếm grep 16/11; số bài pytest thu thập sẽ đo ở S0) · `.github/` ⛔ có (⛔ CI)"),
        ("HD1 hôm nay (đo)", "dòng ghép 1-1 **9.845/9.967** (5/23 kỳ đủ) · ô Final 7 khối 69.510/69.510 (23/23) · khối HD 9.930/9.930 · tự sinh 2026-03: HD 584/584, MID 4.020/4.088 — `voi_so_luong.json`"),
        ("122 dòng thiếu (đo 16/11, chỉ đọc ảnh)", "rải 18/23 kỳ (2026-07: 23 · 2025-11: 14 · 2026-08: 13 …) · 121/122 có `hd_classifying = Need to manual input` · hd Final: OGA 74 · GI 25 · DEP 8 · ITE 7 · khác 8 · chiều ngược: 9.992 − 9.845 = **147** dòng FLS ⛔ có dòng sổ"),
        ("HD2 hôm nay", "0 ô — engine báo cáo/phân bổ chưa có (AC9: 0/10 bảng config có mã engine)"),
        ("Môi trường container (đo 16/11)", "PostgreSQL 16 có binary · node 22 · PyPI vào được · ⛔ Docker daemon · ⛔ pytest ở python hệ thống · ⛔ `.venv`"),
        ("Nguồn đã đọc", "AP v3.1.2 §1.3 · §2.1–§2.5 · §3.1–§3.5 · §4.3–§4.5 · §5.1–§5.5 · `CLAUDE.md` · `10_HOP_DONG_AGENT.md` §1–§4 · `.importlinter` (9 hợp đồng) · `fls/api/bang_tuyen.py` · `fls/api/xu_ly.py` · `fls/ledger/allocate.py` · `fls/oracle/cong_parity.py` · `tests/conftest.py` · danh sách `tests/**` · 3 ảnh fixture HD1 · `06_SCREEN_SPEC.md` (mã màn) · lượt so sánh mã 16/11: docstring + tên hàm của mọi module `fls/**` và 56 tệp `tools/` · `fls/oracle/{anh_chup,doc,doc_du,nguon}.py` · `fls/adapters/mapping_master.py` · `fls/repo/{khai_cot,nap_mapping,doc_bao_cao,ghi_tay}.py` · `fls/api/{the,cua}.py` · `fls/web/{phuc_vu.py,tep/man_f03.js,tep/thanh_phan.js}` · di trú 0001 · 0009 · 0016 · `tests/ledger/test_parity_{ca_so,thuoc_hai}.py` · `tests/oracle/test_doi_soat_gl.py` · phiếu handoff (dãy số + trạng thái WO-051 · WO-062)"),
        ("Nguồn nhắc tới, chưa đọc lại ở lượt này", "sheet Drive AS-IS (đã đọc ở phiên dựng AP v3.0.0 — giá trị sẽ đóng băng ở DT2…DT12) · `docs/ITL/03_Dev/01_TECH_DESIGN.md`"),
        ("agent_count", "**4** — BE-HC (hard code) · BE-CF (config) · FE · DATA; mỗi agent một bước đang chạy; **agent FE nhận bước BE** khi ⛔ có bước FE sẵn sàng (người dùng 16/11)"),
        ("review_rounds", "**3** — R1 quét toàn diff + process-issues (O3) · R2 chỉ phần đổi sau R1 · R3 chỉ phần đổi sau R2 · rồi push tự động lên nhánh làm việc"),
        ("Đơn vị ước lượng", "giờ làm việc của agent; **nửa ngày = 4 giờ** (giả định lập kế hoạch — dự án chưa khai quy ước); một ô wave = nửa ngày"),
        ("Tổng", f"{len(B)} bước · {tong_lo}–{tong_hi} giờ-agent · {so_wave} wave (máy xếp) · theo làn: " + " · ".join(f"{l} {n}" for l, n in theo_lan.items())),
    ]))
    A("")
    A("### 1.1 Phạm vi")
    A("")
    A(md_bang(["", "Gồm", "Ngoài (lý do)"], [
        ("HD1", "122 dòng chưa 1-1: phân loại → sửa lớp lỗi mã → miễn trừ có chữ ký; tự sinh theo kỳ (AC10 · AC11)", "đọc kho sống theo tháng (HD5 — sau khi O4 có kho thật)"),
        ("Lõi config (WP-C1)", "IX.FX · IX.HD · IX.ORG · IX.PER · IX.VEN · IX.DRV · IX.ALR · IX.PL · IX.TMP — nạp, kiểm, kho chỉ-thêm, ký", "bật cờ luật (D2: parity trước) · chia đều kỳ PL (D4 B)"),
        ("Engine (WP-C2…C5)", "CA.GL · SO.CFA1/3 · SO.PLA1/3 · AL.PLT · AL.KEY · SO.PLA3-ATL · RP.CF/PL — mỗi cái có cổng parity với đáp án NOW", "ghi CCR / PDF (HD4 — cắt Gsheet) · BigQuery (Q4 DECIDED: PostgreSQL trước)"),
        ("Màn", "F03 *Cổng hôm nay* (sẵn có) hiện cổng HD1 · HD2 · SCR-F08 Cấu hình (IX.FX · ký tháng · ký bản báo cáo)", "màn bảng tháng × loại dữ liệu trong app (F09 — bỏ theo phương án A: nhân đôi Figure 2.2 mà một lệnh đã sinh) · màn cây HD, màn cờ luật (⛔ có trong AP v3.1.2)"),
        ("Ngoài hẳn", "—", "agent RI/PR/SI (AP §5.3.1: agent chỉ vào sau HD1 + HD2) · họ HR/PLT ở Agent 1·2 (§4.5 PROPOSED) · AP/AR (Q5 DECIDED: GĐ2)"),
    ]))
    A("")
    A("### 1.2 Quyết định còn mở — mỗi câu đã có khuyến nghị")
    A("")
    A(md_bang(["Mã", "Câu", "A", "B", "Khuyến nghị", "Chặn gì"], [(q[0], q[1], q[2], q[3], q[4], q[5]) for q in QD]))
    A("")
    A("### 1.3 Tái dùng từ mã đã có và lỗi của ISP 3.1.1 (so sánh mã 16/11)")
    A("")
    A(md_bang(["Mã đã có (đo 16/11)", "Bước dùng", "Tác động"], [
        ("`fls/oracle/anh_chup.py` · `doc.py` · `doc_du.py` · `nguon.py` · `ngay_xlsx.py` · `tools/do_kha_nang_doc.py`", "DT2…DT12", "đường ống đóng băng chỉ còn bộ chuyển lưới → AnhChup; cổng đọc đủ có sẵn"),
        ("bảng `fls_mapping_master` + `fls/adapters/mapping_master.py` + `tools/nap_mapping_master.py` (73 mã · 21 có phương pháp)", "DT3 · C11", "IX.ALR chỉ thêm hiệu lực theo kỳ + cờ"),
        ("bảng `fls_le` + `fls/canon/le.py`", "C8", "phần pháp nhân của IX.ORG có sẵn"),
        ("`fls_khai_cot` (0016) + `fls/repo/khai_cot.py` — chỉ-thêm, version, hiệu lực máy đặt", "C5", "khuôn kho config có tiền lệ (ủng hộ O5 = A)"),
        ("`fls/api/the.py` (JWT fail-closed, actor từ token) · `period_state = locked` / `FLS-LOCKED-PERIOD`", "C7 · C13 · F5 · F7", "người ký lấy từ token, ⛔ tự viết kiểm"),
        ("`GET /gates` + `doc_cong` + ô chờ `FINAL` + màn F03 ba trạng thái", "CG1 · CG2 · FG", "thay 7 bước F09/tuyến bằng 3 bước"),
        ("`fls/oracle/cong_parity.py` · `fls/kiem/do_luong.py` · `tu_soi.py` · `tools/do_voi_so_luong.py`", "H2 · H4…H15", "khung cổng dùng chung"),
        ("`fls/db/kho.py` (tạo/dựng lại kho test qua `conftest`)", "S0", "S0 chỉ dựng cụm + venv"),
        ("`goi_cua.js` · `trang_thai.js` · `hop_thoai.js` · `thanh_phan.js` · bộ test web node headless", "FG · F4 · F5 · F7", "màn mới ghép từ mảnh có sẵn"),
    ]))
    A("")
    A("**Phải viết mới, ⛔ giảm được** — grep 16/11 cả `fls/` + `tools/`: `musd|bvnd|ty_gia|exchange|fx` = **0 dòng mã** (chỉ chú thích ở `pm_join.py`, `lenh_cho.py`, `do_trong_tai.py`); `CALC ZONE` · `MID3` = **0** ở mã lẫn tài liệu `.md`. ⇒ engine H1 · H4…H14 và 6 bảng IX.FX · IX.PER · IX.VEN · IX.DRV · IX.PL · IX.TMP giữ nguyên — và chúng nằm trên đường găng, nên tái dùng giảm CÔNG, ⛔ giảm LỊCH.")
    A("")
    A(md_bang(["#", "Lỗi của ISP 3.1.1", "Sửa ở 3.1.2"], [
        ("1", "AC7 truy vết sai: AC7 là *'một cú bấm mục lục'* của chính AP, ⛔ màn khoan xuống", "bỏ F3/F09; AC7 thuộc phần đã đo ở AP"),
        ("2", "C7 ghi *'⛔ có đăng nhập'* — sai: `fls/api/the.py` có JWT", "C7/C13/F5: người ký từ token; bỏ bài '403 actor lạ'"),
        ("3", "làn FE thiếu `fls/web/phuc_vu.py` (màn mới phải khai ở BẢNG TỆP)", "thêm vào quyền làn FE; cổng sở hữu tệp của bộ sinh"),
        ("4", "số phiếu `WO-063+` sai: WO/HOI/TL/BG/KQ chung MỘT dãy, cuối là BG-064", "phiếu kế tiếp **065**"),
        ("5", "'17 bảng' · '~1.677 bài'", "18 bảng + 7 view · 2.044 hàm `def test_`"),
        ("6", "DT1 ⛔ chạy trọn được ở container: mã ghép ra 9.845 ⛔ có trong repo, ảnh đã bỏ trường khoá", "tách DT1a / DT1b + O10"),
        ("7", "rủi ro `GAP-ORA-08` (sổ ADJUSTED ⛔ trả giá trị qua API) ⛔ được khai ở bước DATA", "DT2 thử đọc trước bằng `do_kha_nang_doc.py`"),
        ("8", "⛔ nhắc hai phiếu đang dở: WO-062 `MO` · WO-051 `CHO_TEST` (ngoài ISP)", "§2.4: ⛔ chạy song song trên tệp chung (`doc_bao_cao.py`, tệp màn)"),
    ]))
    A("")
    A("Quyết định đã chốt (AP v3.1.2, DECIDED 16/11) được dùng thẳng: §2.1 định nghĩa A · Q1 giữ ngữ pháp · Q2 SI.MAP → Agent 2 · Q3 HR ⛔ qua ALLOCATE · Q4 PostgreSQL trước · Q5 AP/AR ở GĐ2 · Q6 A · D1 IX.FX ký tháng, thiếu = CHẶN · D2 parity trước, cờ tắt · D3 driver by GI = PE · D4 dồn ngày 1 PL start · D5 bản A-CCR chính thức, FS là tham số.")
    A("")
    A("## 2. Dependency và lịch thực hiện")
    A("")
    A("### 2.1 Làn và tệp sở hữu (⛔ giao trùng)")
    A("")
    A(md_bang(["Làn", "Agent", "Bước thuộc làn", "Bước agent làm (lịch)", "Tệp/thư mục chỉ làn này ghi"], [(l, f"{v['ten']} · `{v['agent']}`", theo_lan[l], theo_ag[l], " · ".join(f"`{t}`" for t in v["so_huu"])) for l, v in LAN.items()]))
    A("")
    A("**Agent FE nhận bước BE** (người dùng 16/11: *\"Sau khi chạy xong thì agent FE sẽ nhận job từ agents BE\"*):")
    A("")
    A("- Ở mỗi lần giao, agent FE làm bước FE nếu có bước FE **sẵn sàng**; nếu ⛔ có, orchestrator giao cho nó một bước BE-CF hoặc BE-HC sẵn sàng — bước ưu tiên cao nhất mà ⛔ chạm tệp của bước đang chạy cùng lúc.")
    A("- Bước ấy vẫn **một owner** (giao lại, ⛔ giao trùng); quyền ghi tệp đi theo **làn gốc** trong lúc bước chạy; review 3 vòng như mọi bước.")
    A("- Bước FE trở nên sẵn sàng khi agent FE đang dở bước BE thì chờ tới khi bước BE xong (⛔ cắt ngang).")
    A(f"- Theo lịch máy xếp: agent FE làm {theo_ag['FE']} bước, trong đó {len(fe_muon)} bước của làn BE: " + (", ".join(fe_muon) or "—") + ".")
    A("")
    A("Mã bước: `S0` · `C*` BE-CF · `H*` BE-HC · `F*` FE · `DT*` DATA · `I*` tích hợp cuối. ⚠ `D1`–`D5` trong tài liệu này luôn là **quyết định** của AP §3.5.3, ⛔ bước — bước DATA mang tiền tố `DT` chính vì vậy.")
    A("")
    A("Tệp dùng chung, tuần tự hoá: " + " · ".join(f"`{k}` → {v}" for k, v in DUNG_CHUNG.items()) + ". "
      "Mọi tuyến API mới đi qua làn BE-CF (chỉ một làn chạm `bang_tuyen.py`/`xu_ly.py`); engine của BE-HC lộ ra bằng lệnh cổng + JSON, BE-CF đưa JSON ấy vào `GET /gates` sẵn có (CG1 · CG2). "
      "Phiếu WO/HOI/TL/BG/KQ dùng **chung một dãy số** — đo 16/11 phiếu cuối là BG-064 ⇒ phiếu đầu của ISP là **065**.")
    A("")
    A("### 2.2 Wave (máy xếp theo AGENT — mỗi agent một bước một lúc; một wave ≈ nửa ngày)")
    A("")
    hang = []
    for w in range(so_wave):
        o = {l: "" for l in LAN}
        for b in B:
            if W[b["id"]] == w:
                o[AG[b["id"]]] = f"{ten_buoc(b['id'])} · {b['ten']}" + (f" *(làn {b['lan']})*" if muon(b["id"]) else "")
        hang.append((f"W{w}", o["BE-HC"], o["BE-CF"], o["FE"], o["DATA"]))
    A(md_bang(["Wave", "agent BE-HC", "agent BE-CF", "agent FE", "agent DATA"], hang))
    A("")
    A(f"Đường găng ({len(gang)} bước): " + " → ".join(gang) + ". Ô trống = agent chờ phụ thuộc — dùng để sửa phát hiện review của bước trước (review 3 vòng tốn thời gian thật).")
    A("")
    A("### 2.3 Bảng phân công")
    A("")
    A(md_bang(["Bước", "Phụ thuộc", "Wave", "Owner (agent làm)", "Làn gốc", "Tệp chạm", "Ước lượng", "Trạng thái", "Review"],
              [(ten_buoc(b["id"]), ", ".join(b["deps"]) or "—", f"W{W[b['id']]}", f"`{ag_ten(b['id'])}`" + (" ↩ nhận từ BE" if muon(b["id"]) else ""), b["lan"],
                " · ".join(f"`{t}`" for t in b["tep"]), f"{b['est'][0]}–{b['est'][1]}h", "planned",
                "R1 · R2 · R3 (fls-test, mỗi vòng một phiên mới)") for b in B_sap]))
    A("")
    A("<details><summary>Sơ đồ phụ thuộc (mermaid)</summary>")
    A("")
    A("```mermaid")
    A("flowchart LR")
    for l in LAN:
        A(f"  subgraph {l.replace('-', '_')}[\"{l}\"]")
        for b in B_sap:
            if b["lan"] == l:
                A(f"    {b['id']}[\"{b['id']}\"]")
        A("  end")
    for b in B_sap:
        for d in b["deps"]:
            A(f"  {d} --> {b['id']}")
    A("```")
    A("")
    A("</details>")
    A("")
    A("### 2.4 Vòng một bước — orchestrator, phiếu, review, push")
    A("")
    A(md_bang(["#", "Ai", "Làm gì", "Ra"], [
        ("1", "orchestrator (phiên này)", "kiểm phụ thuộc done · ước lượng còn lại · rủi ro · tệp ⛔ chồng → đổi `planned → ready`; cấp phiếu WO tối thiểu (số kế tiếp của dãy chung, bắt đầu **065**) trỏ về bước ISP (ISP là spec — hợp đồng agent §2 luật thứ tự); agent FE rảnh ⇒ giao bước BE theo luật §2.1", "WO"),
        ("2", "agent được giao (worktree riêng, nhánh cục bộ `isp/<bước>`)", "Substep 1 → báo; Substep 2 TDD: test đỏ → lưu log đỏ → mã tối thiểu → xanh → chạy lại bộ liên quan", "BG kèm log đỏ/xanh thật"),
        ("3", "R1 · fls-test phiên mới", "quét TOÀN diff của bước: lỗi, lệch spec, lệch AP, Đ1–Đ5; chạy triage process-issues (A1/A2/B1/B2) vào sổ phát hiện + luật phòng tái phạm (O3)", "KQ-R1 + sổ phát hiện"),
        ("4", "agent", "sửa theo khuyến nghị R1; chạy lại test bị ảnh hưởng", "commit sửa"),
        ("5", "R2 · fls-test phiên mới", "chỉ quét phần đổi SAU R1", "KQ-R2"),
        ("6", "R3 · fls-test phiên mới", "chỉ quét phần đổi SAU R2; còn phát hiện chặn ⇒ sửa rồi R3 lại (⛔ push khi còn chặn)", "KQ-R3"),
        ("7", "orchestrator", "gộp `isp/<bước>` vào `claude/laughing-bohr-331pt0`, chạy lại cổng CLAUDE.md, push; ghi §5 dashboard; `review → done`", "commit trên nhánh làm việc"),
        ("8", "người dùng", "merge vào main chỉ qua PR bạn duyệt + ThuongCT ký (O6)", "PR"),
    ]))
    A("")
    A("Hai phiếu ngoài ISP đang dở — WO-062 `MO` (lưới F02) · WO-051 `CHO_TEST` (trang hàng chờ): ⛔ chạy song song với bước ISP chạm cùng tệp (`fls/repo/doc_bao_cao.py`, tệp màn `fls/web/tep/**`); orchestrator xếp chúng trước hoặc sau, ⛔ xen.")
    A("")
    A("Theo dõi: `docs/ITL/01_Orchestrator/isp-3.1/TIEN_DO.md` — trạng thái `planned → ready → in_progress → review(R1/R2/R3) → done` hoặc `blocked` kèm nguyên nhân; tiến độ theo bằng chứng (exit criteria), ⛔ gán phần trăm.")
    A("")
    A("## 3. Các bước")
    A("")
    for b in B_sap:
        i = b["id"]
        A(f"## {ten_buoc(i)} — {b['ten']}")
        A("")
        A(f"**Traceability:** {b['ap']}.  ")
        A(f"**Estimate:** {b['est'][0]}–{b['est'][1]} giờ · độ tin: {b['est'][2]}; **Dependency:** {', '.join(ten_buoc(d) for d in b['deps']) or 'không có'}.  ")
        A(f"**Ownership:** task `{i}` · owner `{ag_ten(i)}`" + (f" (nhận từ làn {b['lan']} — luật §2.1, quyền tệp của làn {b['lan']})" if muon(i) else f" ({b['lan']})")
          + f" · wave W{W[i]} · reviewer R1/R2/R3 = `fls-test` (ba phiên riêng).")
        A("")
        A(f"### 1. Step name\n\n{b['ten']}\n")
        A(f"### 2. Goal\n\n{b['goal']}\n")
        A("### 3. Scope\n")
        A("- **Gồm:** " + "; ".join(b["gom"]))
        A("- **Loại trừ:** " + "; ".join(b["loai"]))
        A(f"- **Khái niệm mới duy nhất:** {b['moi']}")
        A(f"- **Mock/static:** {b['mock']}")
        A("- **Giới hạn còn lại sau bước:** " + "; ".join(b["gioi_han"]))
        A("")
        A("### 4. Components touched\n")
        for k, ten in (("FE", "Frontend"), ("BE", "Backend"), ("DB", "DB"), ("TH", "Integrations")):
            A(f"- **{ten}:** {b['tp'][k]}")
        A("")
        A("### 5. Preconditions\n")
        for t in b["tien_de"]:
            A(f"- {t}")
        A("")
        A("### 6. Test cases\n")
        A("**Backend/API**\n")
        A(md_bang(["ID", "Setup · input · action", "Mong (assertion)", "Loại", "Vì sao đỏ trước thay đổi"], b["tb"]))
        A("")
        A("**Frontend/UI**\n")
        if isinstance(b["tf"], str):
            A(b["tf"])
        else:
            A(md_bang(["ID", "Setup · input · action", "Mong (assertion)", "Loại", "Vì sao đỏ trước thay đổi"], b["tf"]))
        A("")
        A("### 7. Expected artifacts\n")
        for t in b["hv"]:
            A(f"- {t}")
        A("")
        A("### 8. Exit criteria\n")
        for t in b["ex"]:
            A(f"- [ ] {t}")
        A("- [ ] điều kiện PUSH (khác điều kiện xong code): đủ R1 · R2 · R3, phát hiện chặn = 0")
        A("")
        ids_t = [t[0] for t in b["tb"] if not t[0].endswith("B1") or not t[1].startswith("N/A")] + ([t[0] for t in b["tf"]] if not isinstance(b["tf"], str) else [])
        A("### Substep 1 — Test cases và handoff cho một thay đổi nhỏ\n")
        A(f"1. **Test cases:** {', '.join(ids_t)} — phủ mọi dòng ở mục 8.")
        A(f"2. **Implementation (kế hoạch, chưa viết mã):** {b['lam']} Tệp: " + " · ".join(f"`{t}`" for t in b["tep"]) + ".")
        A("3. **How to run tests** (dự kiến — Step 0 xác minh; chạy từ gốc repo, `" + ENV + "`):")
        for c in b["chay"]:
            A(f"   - {c}" if c.startswith("`") else f"   - `{c}`")
        A("4. **Known limitations:** " + "; ".join(b["gioi_han"]) + ".")
        qd = [q[0] for q in QD if any(q[0] in s for s in b["tien_de"]) or (b["lan"] == "DATA" and q[0] == "O7" and i not in ("DT1a", "I1"))]
        A(f"5. **Approval boundary:** chỉ chạy khi bạn duyệt ISP 3.1.2 và orchestrator đổi `{i}` sang `ready` (phụ thuộc done: {', '.join(b['deps']) or '—'})"
          + (f"; cần chốt trước: {', '.join(sorted(set(qd)))}" if qd else "") + ". Hết bước: báo và hỏi có sang bước kế không.")
        A("")
        A("### Substep 2 — Hợp đồng strict TDD của bước này\n")
        A(f"Nguồn sự thật duy nhất: **{ten_buoc(i)}** ở trên. Một bước; ⛔ làm việc của bước sau; ⛔ mở rộng, ⛔ refactor cho gọn.")
        A("")
        A(f"1. **Test design** — dẫn từ mục 6 + 8: {', '.join(ids_t)}; tách BE/API ↔ FE/UI" + (" (FE: N/A có lý do)" if isinstance(b["tf"], str) else "") + "; chỗ mơ hồ → `HOI` về orchestrator kèm khuyến nghị, ⛔ đoán.")
        A("2. **Write failing tests** — viết test thật bằng pytest (FE qua node headless của `tests/web`), tất định; chưa viết mã.")
        A("3. **Run red** — chạy, lưu lệnh + exit code + failure vào BG; xác nhận đỏ vì THIẾU hành vi (⛔ vì lỗi cú pháp/setup). Test đã xanh sẵn ⇒ ghi bằng chứng + đánh giá phủ, ⛔ phá mã để có đỏ.")
        A("4. **Implement minimum** — chỉ mã cho test đỏ; ⛔ thêm tuyến/màn/config ngoài mục 7.")
        A("5. **Fix-on-failure** — nêu nguyên nhân gốc, sửa nhỏ nhất, chạy lại test hỏng; bị chặn (quyền, kho, quyết định) ⇒ báo blocker, ⛔ tự nới phạm vi.")
        A("6. **Final verification** — chạy lại bộ ở mục Substep 1.3 + hồi quy của thư mục chạm tới + " + ", ".join(f"`{c}`" for c in LENH_CHUNG) + "; ghi bộ nào ⛔ chạy và vì sao.")
        A("7. **Stop and report** — đối chiếu từng dòng mục 8 với bằng chứng; liệt kê thay đổi, giới hạn; chuyển R1 → R2 → R3; hỏi rõ có sang bước kế không.")
        A("")
    A("## 4. Phần cuối kế hoạch")
    A("")
    A("### 4.1 Tích hợp cuối và acceptance được phủ")
    A("")
    phu = {}
    for b in B:
        for ac in ("HD1", "HD2", "HD5", "AC9", "AC10", "AC11", "D1", "D2", "D3", "D4", "D5", "WP-C1", "WP-C2", "WP-C3", "WP-C4", "WP-C5"):
            # (?!\d): `WP-C3b` vẫn là WP-C3; lookbehind: `D1` ⛔ khớp trong `HD1`
            if re.search(rf"(?<![\w-]){re.escape(ac)}(?!\d)", b["ap"] + " " + b["goal"]):
                phu.setdefault(ac, []).append(b["id"])
    A(md_bang(["Acceptance / quyết định", "Bước phủ", "Tích hợp cuối"], [(k, ", ".join(v), "I1" if k in ("HD1", "AC10", "AC11", "HD5") else "I2") for k, v in sorted(phu.items())]))
    A("")
    A("- **I1** (HD1) và **I2** (HD2) chạy trên thành phần đã tích hợp thật (ảnh đóng băng, kho test PG, máy chủ thử, màn headless).")
    A("- **Biên còn mô phỏng:** chữ ký lý do HD1 trong I1 là chữ ký test (O8 cho chữ ký thật) · người ký là token test · kho test cục bộ (O4: chạy lại I2 trên `fls-pg-1` trước merge) · số NOW là ảnh đóng băng một ngày (đọc kho sống = HD5, ngoài ISP).")
    A("- **Chưa phủ (có tên):** HD3 (đủ bốn họ dữ liệu — cần RI/PR) · HD4 (kế toán làm trên FLS, cắt Gsheet) · AC1–AC8 (đo ở chính AP — AC7 là một cú bấm mục lục của AP, ⛔ màn ứng dụng).")
    A("")
    A("### 4.2 Việc cần bạn chốt trước Wave 0")
    A("")
    A(f"1. **Xác nhận breakdown này** ({len(B)} bước, 4 agent — agent FE nhận bước BE —, 3 vòng review).")
    A("2. **O2 · O3 · O4 · O5 · O7 · O9 · O10 · O11** — khuyến nghị A cho cả tám; **O6 · O8** — xác nhận ThuongCT là người ký (merge và sổ lý do HD1). O1 (push) đã tự gỡ.")
    A("")
    A(f"<sub>Kiểm bởi bộ sinh: {len(B)} bước · đủ 8 trường + 2 substep · DAG ⛔ chu trình · ước lượng ≤ 4h · mọi tệp thuộc làn gốc · ⛔ hai bước cùng wave chạm chung tệp · AP sha256 khớp.</sub>")
    return "\n".join(out) + "\n"


def main() -> int:
    loi = kiem()
    if loi:
        print("⛔ ĐỎ:\n  " + "\n  ".join(loi))
        return 1
    s = sinh()
    if "--kho" in sys.argv:
        print(f"✅ kiểm xanh · {len(B)} bước · {len(s):,} ký tự (⛔ ghi)")
        return 0
    RA.write_text(s, encoding="utf-8")
    print(f"✅ đã ghi {RA.relative_to(GOC)} · {len(B)} bước · {len(s):,} ký tự")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
