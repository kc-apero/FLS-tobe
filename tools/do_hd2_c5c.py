"""`do_hd2.py --goi WP-C5c` — **RP.PL · RP.CF · Daily Report 2 · 3** dựng theo khuôn *(`fls.bao_cao.bao_cao`)* ↔ đáp án
605 · 607 · 608 · 609 · 610 · 615 TỪNG Ô — ISP 3.1.2 · Step 46 · H14 · `WO-311`.

⭐ **Đầu vào = ĐẦU RA ENGINE thượng nguồn, ⛔ đáp án** *(AC-4)*:
   · `cfa1_daily` = lưới `so_sanh_c3a(...).luoi` *(H5 — GL CF `gl_cf_dau_vao.json` → `tinh_gl` → `cfa1_daily`)*;
   · `cfa1_yhqm`  = lưới `so_sanh_c3b(...).luoi` *(H6 — `cuon_ky`)*;
   · `pla3_daily` = lưới `so_sanh_c3d(...).luoi['pla3_pm_hr_daily'].o` *(H8 — GL P&L + HR → PLA3 PM + HR)*;
   · `atl`        = `so_sanh_c5a(...).o` *(H12 AL.KEY, cờ IX.ALR 2025 BẬT ký — đọc từ KHO)* đè dòng `PL*` bằng
                    `so_sanh_c5b(...).pl` *(H13 — IX.PL kho)*; ô `PL5` IX.PL ⛔ tính được ⇒ BỎ khỏi lưới *(⛔ ngầm 0)*.
   Đáp án 605–615 + đáp án thượng nguồn *(409 · 410 · 418 · 606)* chỉ ĐỌC ở bước SO.

── LỚP LỆCH *(Đ5 — `mong` khai TRƯỚC ở `do_hd2_c5c_mong.py`, khác ⇒ ĐỎ CẢ HAI CHIỀU)* ────────────────────────────────
⭐ Ô báo cáo lệch **THỪA KẾ** lớp bằng TRUY NGƯỢC THẬT *(luật `H12-R1-01`: ⛔ quy tắc khối × năm)*: mỗi ô báo cáo là phép
   chiếu của 1–2 ô nguồn *(SHQ = SHQ1 + SHQ2)*. So 3 số cùng khoá: `e` engine · `a` đáp án báo cáo · `s` đáp án NGUỒN.
   · `e ≈ a` ⇒ khớp;
   · `e ≈ s`, `a ≠ s` ⇒ `lech_dap_an_nguon` *(hai ảnh AS-IS của CÙNG ô khác nhau — đóng băng khác ngày)*;
   · `e ≠ s` ⇒ lớp của CHÍNH ô nguồn ở cổng thượng nguồn *(C3a/C3b `lech_ite` ⇒ `ite_alias` · C3d `as_is_truoc_CA` /
     `as_is_416_GAC_thieu_CXA` · C5a `lop_o` · C5b `lop`)*, nối `+`; thêm `+lech_dap_an_nguon` nếu cả `a ≠ s`.
     Ô nguồn lệch mà cổng thượng nguồn ⛔ gán lớp ⇒ `lech_FLS` *(mong 0)*.
⭐ **Ô chỉnh tay** *(ISP mục 3)*: ô lệch có lớp chứa `loi_as_is` và `|e − a| = 0,5` *(±1e-9)* ⇒ liệt kê tên
   "chỉnh tay ⛔ actor" *(gốc: ATL `AH12` `='…'!AH12-0.5` — `phu.o_chinh_tay` của ảnh 605)*; ⛔ chép vào config.
⭐ Phần ⛔ có đầu vào *(FS1 luỹ kế · `hr` · cả 605 · đoạn 615 ngoài khuôn CF)* ⇒ DỪNG, đếm ô đáp án bỏ + câu "cần ảnh
   nào" *(tiền lệ DT7b)*, NGOÀI mẫu số. CHECK của báo cáo: chỉ ĐẾM + LIỆT KÊ *(câu chặn đóng sổ chờ chủ)*.
⭐ Vòng sửa R1 `KQ-313`: 615 so bằng khuôn CF *(`-02`)* · đáp án ô so = 0 chưa ký ⇒ cổng `null` *(`-01`)* · chỉnh tay
   theo chuỗi lan `AH12` *(`-04`)* · 609 = `FS1_FS2_gop`, ⛔ FS3 *(`-08`)*.
⭐ Vòng sửa TÍCH HỢP sau R2 `KQ-314` *(gộp nhánh làm việc + DT13)*:
   · `H14-R2-01`: `mong` khối `check` sinh lại bằng lần đo theo phân loại CHECK của H13-R1 *(`dat_0_0` CHỈ khi kỳ-khối rỗng
     thật)* — `do_hd2.py --goi WP-C5c --ghi` + sinh lại `do_hd2_c5c_mong.py` từ cùng lần đo *(⛔ sửa tay)*.
   · 615 khối `CB I Cash Balance by LE` *(1.495 ô số)* DỰNG bằng `fls.bao_cao.so_du_le` từ ảnh ĐẦU VÀO DT13
     `ccr_so_du_ccr` · `ccr_so_du_cash` *(⛔ đáp án)* ⇒ phần `cb` của báo cáo 615; hàng 71 *(công thức đổi theo cột)* NGOÀI
     khuôn CÓ TÊN.
   · ⛔⛔ **Rào DT13** *(`tools/khuon_dong_bang/_rao_dau_vao.py`)*: mọi ảnh `dau_vao` nạp ở đây đi qua
     `kiem_dau_vao_hop_le(ảnh, PD)`; ảnh `ccr_daily_report_2` *(DR2 A-CCR dán giá trị)* CHỈ là đầu vào của 615 và engine
     615 hiện ⛔ đọc nó; ảnh `sign_off_dau_vao` *(= nội dung đáp án 605)* ⛔ dựng 605. `so_sanh_c5c` tự kiểm rào còn chặn
     hai đường ấy — rào mở ⇒ ĐỎ có tên.
   · **`khop_tinh` ≠ `khop_chep`** *(Đ4)*: ô khớp có số đếm TÁCH theo phần báo cáo — phần đánh dấu `chep` *(giá trị engine
     = CHÉP một ô ảnh đầu vào mang giá trị dán của chính sổ báo cáo)* ⇒ `khop_chep`, ⛔ cộng chung "khớp". Hiện mọi phần
     `chep = False` ⇒ `khop_chep = 0` là KẾT QUẢ *(Đ3)*, ⛔ nền.
"""
from __future__ import annotations

import datetime
import hashlib
import re
from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal, InvalidOperation
from typing import Any, Mapping

from fls.bao_cao import bao_cao as bc
from fls.bao_cao import so_du_le as sd
from fls.cau_hinh import dong_pl
from fls.oracle.cong_parity import PhanXu
from tools import do_hd2 as h
from tools import do_hd2_c3d as c3d
from tools import do_hd2_c5a as c5a
from tools import do_hd2_c5b as c5b
from tools.do_hd2 import GOC, nap_anh
from tools.khuon_dong_bang import _rao_dau_vao as rao

DA = GOC / "tests" / "fixture" / "dap_an"
ATOL = Decimal("1e-12")            # rtol 0 — ô báo cáo là CHÍNH ô nguồn (≤ 2 hạng tử) ⇒ cùng ngưỡng C5a/C5b
ATOL_CHINH_TAY = Decimal("1e-9")
CHINH_TAY = Decimal("0.5")
LECH_FLS = "lech_FLS"
LECH_NGUON = "lech_dap_an_nguon"
#: ⭐ `H14-R1-02`: ô 615 *(A-CCR `5. Daily Report 2`, DÁN GIÁ TRỊ — DT13 `BG-320` §1)* lệch mà engine = đáp án CF report
#: 610 cùng khoá ⇒ **bản chính thức ≠ bản CF report** *(đo 22/11: 671/706 ô lệch của 615; 35 còn lại `ite_alias` như 610)*
LECH_CCR_CF = "lech_ban_ccr_vs_cf"

#: nhãn đoạn khối số dư của 615 ⇒ phần `cb` *(vòng sửa tích hợp sau R2: dựng từ ảnh DT13, `fls.bao_cao.so_du_le`)*
NHAN_CB = "CB I Cash Balance by LE I Legal Entity by Currency"
#: ảnh ĐẦU VÀO của phần `cb` *(DT13 `BG-320` §2)* — tên khuôn ↔ tab A-CCR
ANH_SO_DU = {"ccr_so_du_ccr": "2. CCR", "ccr_so_du_cash": "2. CCR Cash"}
DV = GOC / "tests" / "fixture" / "dau_vao"

#: đáp án → (tệp, loại, FS, kỳ) *(kỳ = tháng của trục ngày `From`/`To` — đo ở `BG-270`)*
DAP_AN: dict[str, dict[str, Any]] = {
    "607": {"anh": "daily_report_3_fs2", "loai": "PL", "fs": "FS2", "ky": 202511},
    "608": {"anh": "daily_report_3_fs1", "loai": "PL", "fs": "FS1", "ky": 202511},
    "609": {"anh": "daily_report_3_gop", "loai": "PL", "fs": "FS1_FS2_gop", "ky": 202512},
    "610": {"anh": "daily_report_2", "loai": "CF", "fs": "-", "ky": 202611},
    # ⭐ `H14-R1-02` (KQ-313): 615 = A-CCR `5. Daily Report` = bản CHÍNH THỨC (AP §3.5.3 D5). Đo R1: 22.420/48.021 ô số
    #   (46,7 %) nằm trên ĐÚNG bộ khoá engine sinh cho 610 *(cùng kỳ 11/2026)* ⇒ thiếu KHUÔN, ⛔ thiếu đầu vào. Khuôn =
    #   nhãn đoạn `Unit: mUSD` ↔ `ngay`, `CM Cumulative` ↔ `luy_ke` của CÙNG báo cáo CF engine. Đoạn khác ⇒ NGOÀI mẫu số
    #   CÓ TÊN (`ngoai_khuon_615`). `doi_chieu` = đáp án 610 — chỉ để gán lớp `lech_ban_ccr_vs_cf` ở bước SO.
    "615": {"anh": "ccr_daily_report", "loai": "CF", "fs": "-", "ky": 202611, "doi_chieu": "610",
            "phan_khuon": {"Unit: mUSD": "ngay", "CM Cumulative": "luy_ke", NHAN_CB: "cb"}},
}
#: 615 — đoạn sổ ⛔ thuộc khuôn CF engine ⇒ (loại, tên, cần gì). Loại `chua_co_dau_vao` = cần ảnh ĐẦU VÀO; `ngoai_khuon` =
#: ô ⛔ phải của báo cáo CF *(đã so ở đáp án khác)*. Khoá = (nhãn đoạn, nhóm khối) — nhóm khối: `GROUP` · `FS` *(khối
#: `[FSx][PLA3] …`)* · `*`.
NGOAI_KHUON_615: dict[tuple[str | None, str], tuple[str, str, str]] = {
    (None, "*"): (
        "chua_co_dau_vao", "tien_dau_bao_cao",
        "khối đầu báo cáo `Cash on way` · `Bank` theo LE (hàng 11–55) — chưa đo nguồn (ứng viên: ảnh số dư DT13)"),
    ("Raw Data Management", "*"): (
        "chua_co_dau_vao", "raw_data_management",
        "`Raw Data Management` — 220 công thức nội bộ A-CCR chưa đo (`BG-320` §4)"),
    ("Unit: person", "GROUP"): (
        "chua_co_dau_vao", "hr", "ảnh `Report HR` (số người theo Grade) — FLS ⛔ có engine số người (như 610 `hr`)"),
    ("Unit: person", "FS"): (
        "ngoai_khuon", "ban_sao_DR3_A_CCR",
        "bản sao `5. Daily Report 3` của A-CCR (DT13 đo 35.542/35.542 ô số trùng ảnh 609) — đã so ở 609, ⛔ khuôn CF"),
    ("Unit: person", "*"): ("ngoai_khuon", "person_hang_khong_khoi", "hàng đoạn `Unit: person` ⛔ nhãn khối"),
    ("Daily Transactions", "*"): ("ngoai_khuon", "daily_transactions", "giao dịch ngày (PII) — ⛔ báo cáo"),
}
#: đáp án DỪNG cả bản *(⛔ engine FLS nào sinh được nguồn)* — câu "cần ảnh nào". ⭐ `H14-R1-01`: DỪNG ⇒ ô so = 0 ⇒ cổng
#: ⛔ đo được ⇒ `dat = null` *(⛔ `true`)* trừ khi chủ ký "DỪNG có tên" ở `DUNG_KY`. ⛔ VÒNG TRÒN: ảnh DT13
#: `sign_off_dau_vao` NỘI DUNG Y HỆT đáp án 605 *(`BG-320` §2)* ⇒ ⛔ được dùng để dựng 605 *(đổi tên đáp án thành đầu
#: vào = so đáp án với chính nó)*; được dùng cho 608 *(AS-IS 608 đọc tab Sign off thật)*.
DUNG: dict[str, dict[str, str]] = {
    "605": {"anh": "daily_report_3",
            "can": "nguồn `[MID][FS1][PLA5]` (P&L VND theo 8 thực thể × 24 tháng 2024–2025, bản dán giá trị Sign off): "
                   "ảnh `[FS1][PLA3]`/`[PLA5]` Y/H/Q/M trước khi dán + đường VND; FLS ⛔ có engine FS1, và 2024 "
                   "(trước ITL 10/2024) ⛔ có sổ nguồn; DT13 (`BG-320`): tab gốc `[FS1][PLA5]` ⛔ còn trong sổ — 0 ứng "
                   "viên; ⛔ dùng `sign_off_dau_vao` (= chính đáp án 605 ⇒ vòng tròn)"},
}
#: ⭐ chữ ký chủ "DỪNG có tên" *(mã đáp án → BẢN GHI CÓ CẤU TRÚC, ⛔ chuỗi tự do — đóng `H14-R2-02`: trước đây
#: `{"605": "x"}` mở cổng, đỏ chỉ vì ghim JSON)*. Bốn khoá bắt buộc: `nguoi_ky` *(tên, ⛔ email)* · `ngay` *(ISO
#: `YYYY-MM-DD`, ngày có thật)* · `ly_do` · `nguon_quyet` *(dòng sổ quyết định)*. Hợp lệ ⇔ `kiem_dung_ky(...) == []`;
#: bản ghi hỏng ⇒ cổng ĐỎ có tên *(⛔ coi như không ký)*. 605 ký 23/11 *(`TIEN_DO.md` hàng 2026-11-23)*.
DUNG_KY: dict[str, dict[str, str]] = {
    "605": {
        "nguoi_ky": "KhanhCQ",
        "ngay": "2026-11-23",
        "ly_do": "tab nguồn [FS1][PLA5] đã xoá khỏi sổ P&L — 0 ứng viên (DT13 BG-320); tái lập bằng sign_off_dau_vao "
                 "= vòng tròn (rào DT13)",
        "nguon_quyet": "TIEN_DO 2026-11-23",
    },
}
KHOA_DUNG_KY = ("nguoi_ky", "ngay", "ly_do", "nguon_quyet")


def kiem_dung_ky(dung_ky: Any) -> list[str]:
    """Kiểm hợp lệ `DUNG_KY`: mỗi mã phải là đáp án DỪNG *(`DUNG`)* · bản ghi đủ `KHOA_DUNG_KY` *(⛔ thừa)* · mọi trường là
    chuỗi không rỗng · ngày đúng khuôn ISO và có thật · người ký ⛔ email. Trả danh sách lỗi CÓ TÊN *(rỗng = hợp lệ)*."""
    if not isinstance(dung_ky, dict):
        return [f"DUNG_KY kiểu {type(dung_ky).__name__} ⛔ phải đối tượng {{mã: bản ghi}}"]
    loi: list[str] = []
    for ma, ky in dung_ky.items():
        if ma not in DUNG:
            loi.append(f"{ma}: ⛔ phải mã đáp án DỪNG {sorted(DUNG)}")
            continue
        if not isinstance(ky, dict):
            loi.append(f"{ma}: chữ ký ⛔ phải bản ghi 4 khoá {list(KHOA_DUNG_KY)} (chuỗi tự do ⛔ mở cổng)")
            continue
        thieu = [k for k in KHOA_DUNG_KY if k not in ky]
        thua = [k for k in ky if k not in KHOA_DUNG_KY]
        if thieu or thua:
            loi.append(f"{ma}: thiếu trường {thieu} · thừa trường {thua}")
            continue
        for k in KHOA_DUNG_KY:
            if not isinstance(ky[k], str) or not ky[k].strip():
                loi.append(f"{ma}: {'người ký' if k == 'nguoi_ky' else 'lý do' if k == 'ly_do' else k} rỗng "
                           f"hoặc ⛔ chuỗi ({k} = {ky[k]!r})")
        if isinstance(ky["nguoi_ky"], str) and "@" in ky["nguoi_ky"]:
            loi.append(f"{ma}: người ký là email ⛔ (ghi tên, riêng tư)")
        ng = ky["ngay"]
        if isinstance(ng, str) and ng.strip():
            try:
                ok = datetime.date.fromisoformat(ng).isoformat() == ng
            except ValueError:
                ok = False
            if not ok:
                loi.append(f"{ma}: ngày {ng!r} ⛔ đúng khuôn YYYY-MM-DD / ngày có thật")
    return loi


def _dung_ky_hop_le() -> dict[str, dict[str, str]]:
    """Chỉ các chữ ký HỢP LỆ *(từng mã — một mã hỏng ⛔ kéo mã khác)*; hỏng ⇒ coi như chưa ký + cổng ĐỎ ở `so_sanh_c5c`."""
    return {m: k for m, k in DUNG_KY.items() if not kiem_dung_ky({m: k})} if isinstance(DUNG_KY, dict) else {}

#: ⭐ `H14-R1-04` — gốc ô chỉnh tay ⛔ actor: ATL `AH12` = `GROUP·OMC·2025M02` `='…'!AH12-0.5` *(ghi ở ảnh 605
#: `phu.o_chinh_tay`: `dong_sheet_atl` 12 · `cot_anh_atl` `y2025_m02` — bài đối chiếu hai nguồn)*. Chuỗi lan = mọi mã của
#: khối gốc mang ĐỦ `±0,5` ở kỳ gốc VÀ MỌI kỳ cộng dồn chứa nó *(M02 ⇒ Q1 ⇒ H1 ⇒ Y)*: hàng nhận `OMC` qua công thức lan
#: đủ 4 kỳ; ô `±0,5` ở mã ⛔ lan đủ *(đo: `NPC` M01 · M02, `PL5` M02)* = TRÙNG ngẫu nhiên, liệt kê riêng, ⛔ gọi chỉnh tay.
GOC_CHINH_TAY = ("GROUP", "OMC", "2025M02")


def _so(v: Any) -> Decimal | None:
    if v is None or isinstance(v, (bool, dict)):
        return None
    try:
        return Decimal(str(v))
    except InvalidOperation:
        return None


def _chu(v: Any) -> str | None:
    return v.get("chu") if isinstance(v, dict) else None


# ── đọc khuôn của đáp án *(nhãn hàng + tiêu đề cột — ⛔ giá trị vào engine)* ─────────────────────────────────────────

_TIEN_TO = re.compile(r"^\[(FS\d)\]\[PLA3\] ")


def _tieu_de(anh: Mapping[str, Any]) -> dict[int, dict[str, Any]]:
    by: dict[int, dict[str, Any]] = {}
    for t in anh["phu"]["tieu_de"]["dong"]:
        g = t["gia_tri"]
        by.setdefault(int(t["dong_sheet"]), {})[t["cot"]["chu"].lower()] = _chu(g) if isinstance(g, dict) else g
    return by


def _cot_ky(hd: Mapping[str, Any]) -> dict[str, str]:
    """Hàng tiêu đề luỹ kế *(`2025` · `H1` … `Q4` · `1` … `12` · `2026` …)* ⇒ cột → kỳ `2025H1`/`2025M01`."""
    ra: dict[str, str] = {}
    nam = None
    for c in sorted(hd, key=lambda x: (len(x), x)):
        v = str(hd[c])
        if re.fullmatch(r"20\d\d", v):
            nam = v
            ra[c] = v
        elif nam and v in ("H1", "H2", "Q1", "Q2", "Q3", "Q4"):
            ra[c] = nam + v
        elif nam and v.isdigit() and 1 <= int(v) <= 12:
            ra[c] = f"{nam}M{int(v):02d}"
    return ra


def nhan_cb_615(anh: Mapping[str, Any]) -> dict[int, tuple[str, str]]:
    """Khối CB của ảnh 615 ⇒ {hàng sheet → (LE, đơn vị)}. LE = `LE<nn>` theo số thứ tự nhãn `"<nn> > <tên>"` của hàng chỉ
    nhãn đứng TRƯỚC *(⛔ mang tên — 7 nhãn là tên người)*; đơn vị = nhãn `ma` *(`mUSD` · `mSGD` · `mHKD` · `bVND`)*."""
    hang: list[tuple[int, str, Any]] = []
    for x in anh["phu"]["dong_chi_nhan"]["dong"]:
        if _chu(x.get("phan")) == NHAN_CB:
            m = re.match(r"^(\d+) > ", _chu(x.get("nhan")) or "")
            if m:
                hang.append((int(x["dong_sheet"]), "le", f"LE{int(m.group(1)):02d}"))
    for r in anh["dong"]:
        if _chu(r.get("phan")) == NHAN_CB:
            hang.append((int(r["dong_sheet"]), "o", _chu(r.get("ma"))))
    ra: dict[int, tuple[str, str]] = {}
    le = None
    for ds, loai, v in sorted(hang):
        if loai == "le":
            le = v
        elif le is not None and v:
            ra[ds] = (le, v)
    return ra


def o_dap_an(ma_da: str, anh: Mapping[str, Any]) -> tuple[dict[str, Decimal], Counter]:
    """Đáp án ⇒ {khoá ô báo cáo → số}; cột ⛔ thuộc trục *(`F` ngày trước · `AK` ⛔ ngày)* đếm riêng có tên."""
    cfg = DAP_AN[ma_da]
    td = _tieu_de(anh)
    nam, thang = divmod(cfg["ky"], 100)
    hd5 = td.get(5, {})
    cot_ngay: dict[str, str] = {}
    for c, v in hd5.items():
        s = _so(v)
        if s is not None and 40000 < s < 50000:
            d = datetime.date(1899, 12, 30) + datetime.timedelta(days=int(s))
            if (d.year, d.month) == (nam, thang):
                cot_ngay[c] = d.isoformat()
    hd_ky = sorted((r, _cot_ky(m)) for r, m in td.items() if str(m.get("g")) in ("2024", "2025", "2026"))
    ra: dict[str, Decimal] = {}
    ngoai = Counter()
    pk = cfg.get("phan_khuon")
    cb = nhan_cb_615(anh) if pk and "cb" in pk.values() else {}
    for r in anh["dong"]:
        ds = int(r["dong_sheet"])
        ph = _chu(r.get("phan")) or _chu(r.get("che_do"))
        kh, ma = _chu(r.get("khoi")), _chu(r.get("ma"))
        if pk is not None:                                   # 615: nhãn đoạn sổ ⇒ phần của khuôn CF; đoạn khác ⇒ có tên
            nhan = _chu(r.get("phan"))
            if nhan not in pk:
                nhom = "GROUP" if kh == "GROUP" else "FS" if kh and kh.startswith("[FS") else "*"
                loai, ten, _can = NGOAI_KHUON_615.get((nhan, nhom)) or NGOAI_KHUON_615[(nhan, "*")]
                ngoai[f"{loai}:{ten}"] += sum(1 for c, v in r.items() if len(c) <= 2 and c.isalpha()
                                              and _so(v) is not None)
                continue
            ph = pk[nhan]
            if ph == "cb":                                   # khối số dư: khoá (LE, đơn vị) — hàng ngoài khuôn CÓ TÊN
                kh, ma = cb.get(ds, (None, None))
                if (kh, ma) in sd.NGOAI_KHUON_CB:
                    ngoai[f"ngoai_khuon:{sd.NGOAI_KHUON_CB[(kh, ma)][0]}"] += sum(
                        1 for c, v in r.items() if len(c) <= 2 and c.isalpha() and _so(v) is not None)
                    continue
        if kh is None or ma is None:
            ngoai["hang_khong_nhan"] += 1
            ngoai["o_hang_khong_nhan"] += sum(1 for c, v in r.items() if len(c) <= 2 and c.isalpha()
                                              and _so(v) is not None)
            continue
        if ph == "cb":
            phan, cot = "cb", cot_ngay
        elif ph in (None, "ngay"):
            phan, cot = "ngay", cot_ngay
        else:
            m = _TIEN_TO.match(kh)
            if cfg["loai"] == "CF":
                phan = ph
            else:
                phan = "luy_ke:" + (m.group(1) if m else ("FS1" if cfg["fs"] == "FS1" else "FS2"))
            kh = _TIEN_TO.sub("", kh)
            tr = [x for x in hd_ky if x[0] < ds]
            cot = tr[-1][1] if tr else {}
        for c, v in r.items():
            if len(c) > 2 or not c.isalpha():
                continue
            s = _so(v)
            if s is None:
                continue
            if c not in cot:
                ngoai[f"{phan}:{c}"] += 1
                continue
            ra[bc.khoa_o(phan, kh, ma, cot[c])] = s
    return ra, ngoai


# ── nguồn engine + lớp của ô nguồn ở cổng thượng nguồn ─────────────────────────────────────────────────────────────

@dataclass
class NguonEngine:
    luoi: dict[str, dict[tuple, Decimal]]
    lop: dict[str, dict[tuple, str]]                     # nguồn → (khối, mã, cột) → lớp ở cổng thượng nguồn
    dap_an: dict[str, dict[tuple, Decimal]]              # nguồn → giá trị đáp án THƯỢNG NGUỒN *(chỉ bước so)*
    cong: dict[str, bool]                                # cổng thượng nguồn ĐẠT?
    pl5_bo: int = 0
    so_du: dict[str, dict[int, dict[str, Decimal | None]]] | None = None   # phần `cb` của 615 *(ảnh DT13)*
    tom: dict[str, tuple[set[str], int]] = field(default_factory=dict)   # bộ nhớ đệm (mã có · cột ngày lớn nhất)


def _dap_an_thua(anh: Mapping[str, Any], cot: str) -> dict[tuple, Decimal]:
    """Ảnh thưa *(409 · 410 · 418: ô 0/vắng ⇒ 0)* ⇒ {(khối, mã, cột) → số}."""
    ra: dict[tuple, Decimal] = {}
    for r in anh["dong"]:
        k = r[cot]
        k = int(k) if cot == "ngay" else _chu(k)
        s = _so(r["gt"])
        if s is not None:
            ra[(_chu(r["le"]), _chu(r["ma_hd"]), k)] = s
    return ra


def nap_so_du(pd: str = "615") -> dict[str, dict[int, dict[str, Decimal | None]]]:
    """Ảnh ĐẦU VÀO DT13 `ccr_so_du_ccr` · `ccr_so_du_cash` ⇒ `{tab: {hàng sheet: {ngày ISO: số|None}}}` cho `so_du_le`.
    ⭐ Qua rào DT13 TRƯỚC khi đọc *(`kiem_dau_vao_hop_le(ảnh, PD)` — ảnh dùng sai PD ⇒ `DauVaoSaiChoError` có tên)*."""
    ra: dict[str, dict[int, dict[str, Decimal | None]]] = {}
    for ten, tab in ANH_SO_DU.items():
        rao.kiem_dau_vao_hop_le(ten, pd)
        anh = nap_anh(DV / f"{ten}.json")
        cot = {c: datetime.date(int(c[1:5]), int(c[5:7]), int(c[7:9])).isoformat()
               for c in anh["cot"] if re.fullmatch(r"d\d{8}", c)}
        ra[tab] = {int(r["dong_sheet"]): {iso: _so(r.get(c)) for c, iso in cot.items()} for r in anh["dong"]}
    return ra


def nguon_engine(lich, alr, dinh_nghia: Mapping[str, str]) -> NguonEngine:
    fx, cay = h.nap_fx(), h.nap_cay()
    gl_cf = nap_anh(h.ANH_CFA1.parent / "gl_cf_dau_vao.json")
    a = h.so_sanh_c3a(gl_cf, nap_anh(h.ANH_CFA1), fx, cay, lich, h.mong_c3a_mac_dinh())
    b = h.so_sanh_c3b(gl_cf, nap_anh(DA / "cfa1_yhqm.json"), fx, cay, lich, h.mong_c3b_mac_dinh())
    gl, hr, tabs, _fx, _cay = c3d.nap_nguon()
    den = datetime.date.fromisoformat(c3d.mong_c3d_mac_dinh().so["den"])
    d = c3d.so_sanh_c3d(gl, hr, tabs, fx, cay, lich, den, c3d.mong_c3d_mac_dinh())
    atl, drv = nap_anh(c5a.ANH_ATL), nap_anh(c5a.ANH_DRV)
    t5a = c5a.so_sanh_c5a(d.luoi["pla3_pm_hr_yhqm"], atl, drv, alr, cay, c5a.mong_c5a_mac_dinh())
    t5b = c5b.so_sanh_c5b(t5a, atl, dinh_nghia, c5b.com_gag_ngoai(fx=fx), c5b.mong_c5b_mac_dinh())
    # ── ATL của FLS = lưới C5a, dòng PL* đè bằng IX.PL (C5b); PL5 IX.PL ⛔ tính được ⇒ BỎ ──
    luoi_atl = dict(t5a.o)
    pl_ma = set(dinh_nghia)
    bo = [k for k in luoi_atl if k[1] in pl_ma and k not in t5b.pl]
    for k in bo:
        del luoi_atl[k]
    luoi_atl.update(t5b.pl)
    lop_atl = {tuple(k.split("#")): v for k, v in t5a.lop_o.items()}
    lop_atl.update({tuple(x["o"].split("#")): x["lop"] for x in t5b.lech})
    lop_cfa1 = {(x["le"], x["ma"], int(x["ngay"])): "ite_alias" for x in a.lech_ite}
    lop_yhqm = {(x["le"], x["ma"], x["ky"]): "ite_alias" for x in b.lech_ite}
    lop_pla3: dict[tuple, str] = {}
    for x in d.lech:
        if x["tab"] != "pla3_pm_hr_daily":
            continue
        kh, ma, t = x["o"].split("#")
        lop_pla3[(kh, ma, int(t))] = "as_is_truoc_CA" if c3d.la_truoc_ca(x) else "as_is_416_GAC_thieu_CXA"
    pla3 = d.luoi["pla3_pm_hr_daily"].o
    # ── KPI của CFA1 *(`MA_KPI`)*: engine H5/H6 ⛔ tính *(ô 0 giữ chỗ — C3a/C3b LOẠI có tên `o_kpi`)* ⇒ BỎ khỏi lưới,
    #    ⛔ để báo cáo in 0 ngầm *(đo 22/11: 2.948 ô luỹ kế 610 "lệch FLS" chính là ô KPI giữ chỗ này)* ──
    kpi = set(h.MA_KPI)
    cfa1 = {k: v for k, v in a.luoi.items() if k[1] not in kpi}
    yhqm = {k: v for k, v in b.luoi.items() if k[1] not in kpi}
    return NguonEngine(
        luoi={"cfa1_daily": cfa1, "cfa1_yhqm": yhqm, "pla3_daily": dict(pla3), "atl": luoi_atl},
        lop={"cfa1_daily": lop_cfa1, "cfa1_yhqm": lop_yhqm, "pla3_daily": lop_pla3, "atl": lop_atl},
        dap_an={"cfa1_daily": _dap_an_thua(nap_anh(h.ANH_CFA1), "ngay"),
                "cfa1_yhqm": _dap_an_thua(nap_anh(DA / "cfa1_yhqm.json"), "ky"),
                "pla3_daily": _dap_an_thua(nap_anh(DA / "pla3_pm_hr_daily.json"), "ngay"),
                "atl": c5a.gia_tri_atl(atl)},
        cong={"WP-C3a": a.phan_xu.dat, "WP-C3b": b.phan_xu.dat, "WP-C3d": d.phan_xu.dat,
              "WP-C5a": t5a.phan_xu.dat, "WP-C5b": t5b.phan_xu.dat},
        pl5_bo=len(bo), so_du=nap_so_du("615"))


# ── so ─────────────────────────────────────────────────────────────────────────────────────────────────────────────

def _nguon_cua(bao: Mapping[str, Any]) -> dict[str, Mapping[str, Any]]:
    return {p["id"]: p for p in bao["phan"]}


def _khoi_engine(phan: str, nhan: str) -> tuple[str, ...]:
    for n, k in bc.KHOI_LE + bc.KHOI_CDT:
        if n == nhan:
            return k
    return (nhan,)


def _cot_nguon(truc: str, c: str) -> Any:
    if truc == "ngay":
        return (datetime.date.fromisoformat(c) - datetime.date(1899, 12, 30)).days
    return c


def _lop_lech(ne: NguonEngine, nguon: str, truc: str, khoi: str, ma: str, c: str, e: Decimal, a: Decimal) -> str:
    """TRUY NGƯỢC THẬT về ô nguồn *(xem đầu tệp)*."""
    cn = _cot_nguon(truc, c)
    kh_e = _khoi_engine("", khoi)
    da = ne.dap_an[nguon]
    thua = nguon != "atl"
    s = Decimal(0)
    for k in kh_e:
        v = da.get((k, ma, cn))
        if v is None and not thua:
            return LECH_FLS                                  # ô nguồn ⛔ có ở đáp án nguồn ⇒ ⛔ truy được
        s += v or Decimal(0)
    a_khac_s = abs(a - s) > ATOL
    if abs(e - s) <= ATOL:
        return LECH_NGUON if a_khac_s else LECH_FLS
    lop: set[str] = set()
    for k in kh_e:
        ev = ne.luoi[nguon].get((k, ma, cn))
        sv = da.get((k, ma, cn), Decimal(0))
        if ev is not None and abs(ev - sv) <= ATOL:
            continue
        l = ne.lop[nguon].get((k, ma, cn))
        if l is None:
            return LECH_FLS
        lop.update(l.split("+"))
    if a_khac_s:
        lop.add(LECH_NGUON)
    return "+".join(sorted(lop)) if lop else LECH_FLS


def ly_do_vang(ne: NguonEngine, p: Mapping[str, Any], ma: str, c: str) -> str:
    """Ô đáp án mà báo cáo engine ⛔ có ⇒ lý do CÓ TÊN *(⛔ một rổ "vắng")*."""
    if p["nguon"] not in ne.luoi:
        return f"ngoai_luoi:{p['nguon']}"                 # phần ⛔ lấy từ lưới engine thượng nguồn (vd `cb`)
    luoi = ne.luoi[p["nguon"]]
    if p["nguon"] not in ne.tom:
        ne.tom[p["nguon"]] = ({k[1] for k in luoi}, max((k[2] for k in luoi if isinstance(k[2], int)), default=0))
    ma_co, cot_max = ne.tom[p["nguon"]]
    if p["nguon"].startswith("cfa1") and ma in h.MA_KPI:
        return "kpi_cfa1_engine_chua_tinh"                 # C3a/C3b loại KPI (o_kpi)
    if p["nguon"] == "atl" and ma in dong_pl.DINH_NGHIA:
        return f"{ma}_ix_pl_khong_tinh_duoc"              # C5b `pl5_khong_tinh_duoc`
    if ma not in ma_co:
        return f"ma_ngoai_luoi:{ma}"                      # mã có ở sổ, ⛔ ở cây IX.HD của engine
    if p["truc"] == "ngay":
        cn = _cot_nguon("ngay", c)
        if cn > cot_max:
            return "ngay_sau_ngay_doc_dau_vao"
    return "khac"


def _sha(ds: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(ds)).encode("utf-8")).hexdigest()


def chuoi_chinh_tay(ung_vien: list[str], goc: tuple[str, str, str] = GOC_CHINH_TAY) -> tuple[list[str], list[str]]:
    """`H14-R1-04`: ô `loi_as_is` có |e − a| = 0,5 ⇒ (chuỗi lan từ gốc `AH12`, trùng ngẫu nhiên). Chuỗi = mã của khối gốc
    mang 0,5 ở kỳ gốc VÀ mọi kỳ cộng dồn chứa nó *(M ⇒ Q ⇒ H ⇒ Y)*; ⛔ có ô gốc ⇒ chuỗi rỗng *(⛔ đoán)*."""
    kh0, ma0, ky0 = goc
    nam, th = int(ky0[:4]), int(ky0[5:])
    ky_chuoi = {ky0, f"{nam}Q{(th - 1) // 3 + 1}", f"{nam}H{1 if th <= 6 else 2}", f"{nam}"}
    co: dict[tuple[str, str, str], set[str]] = {}
    for k in ung_vien:
        ph, kh, ma, c = k.split("|")
        co.setdefault((ph, kh, ma), set()).add(c)
    goc_co = any(kh == kh0 and ma == ma0 and ky_chuoi <= cs for (ph, kh, ma), cs in co.items())
    chuoi = sorted(k for k in ung_vien if goc_co and k.split("|")[1] == kh0 and k.split("|")[3] in ky_chuoi
                   and ky_chuoi <= co[tuple(k.split("|")[:3])])
    return chuoi, sorted(set(ung_vien) - set(chuoi))


def so_mot(ma_da: str, anh: Mapping[str, Any], bao: Mapping[str, Any], ne: NguonEngine,
           doi_chieu: Mapping[str, Decimal] | None = None) -> dict[str, Any]:
    """So TỪNG Ô một đáp án với báo cáo engine. Trả số đếm *(Đ4 — mỗi khoá nói nó đếm gì)*.

    `doi_chieu` *(chỉ 615)* = ô đáp án 610 cùng khoá: ô lệch mà engine = 610 ⇒ lớp `lech_ban_ccr_vs_cf`."""
    da, ngoai = o_dap_an(ma_da, anh)
    phan = _nguon_cua(bao)
    dem = Counter({"khop_tinh": 0, "khop_chep": 0})
    theo_phan: dict[str, Counter] = {}
    chua = Counter()
    nk = Counter()
    for k in [k for k in ngoai if k.startswith(("chua_co_dau_vao:", "ngoai_khuon:"))]:
        (chua if k.startswith("chua") else nk)[k.split(":", 1)[1]] += ngoai.pop(k)
    vang = Counter()
    lech: list[dict[str, str]] = []
    mx = Decimal(0)
    for k, a in sorted(da.items()):
        ph, kh, ma, c = k.split("|")
        p = phan.get(ph)
        if p is None or p.get("dung"):
            chua[ph] += 1
            continue
        e = bao["o"].get(k)
        if e is None:
            vang[ly_do_vang(ne, p, ma, c)] += 1
            continue
        e = Decimal(e)
        dem["tong_o"] += 1
        tp = theo_phan.setdefault(ph, Counter({"tong_o": 0, "o_0_0": 0, "khop_co_so": 0, "lech": 0}))
        tp["tong_o"] += 1
        if e == 0 and a == 0:
            dem["o_0_0"] += 1
            tp["o_0_0"] += 1
        elif abs(e - a) <= ATOL:
            dem["khop_co_so"] += 1
            tp["khop_co_so"] += 1
            dem["khop_chep" if p.get("chep") else "khop_tinh"] += 1
            mx = max(mx, abs(e - a))
        else:
            tp["lech"] += 1
            # phần `cb` ⛔ có cổng thượng nguồn để truy *(đầu vào = ảnh số dư)* ⇒ lệch = `lech_FLS` *(mong 0)*
            lop = (LECH_FLS if p["nguon"] not in ne.dap_an
                   else _lop_lech(ne, p["nguon"], p["truc"], kh, ma, c, e, a))
            b = doi_chieu.get(k) if doi_chieu is not None else None
            if b is not None and abs(a - b) > ATOL:          # bản chính thức (615) ≠ bản CF report (610) ở ô này
                lop = LECH_CCR_CF if abs(e - b) <= ATOL else "+".join(sorted(set(lop.split("+")) | {LECH_CCR_CF}))
            lech.append({"o": k, "engine": str(e), "dap_an": str(a), "lop": lop})
    dem["khop"] = dem["khop_co_so"] + dem["o_0_0"]
    dem["o_co_so"] = dem["tong_o"] - dem["o_0_0"]
    q = Decimal("1e-12")
    theo_lop: dict[str, list[dict[str, str]]] = {}
    for x in lech:
        theo_lop.setdefault(x["lop"], []).append(x)
    lop = {l: {"so_o": len(v), "sha256": _sha([f"{x['o']}={Decimal(x['engine']).quantize(q)}|"
                                                f"{Decimal(x['dap_an']).quantize(q)}" for x in v])}
           for l, v in sorted(theo_lop.items())}
    ung_vien = [x["o"] for x in lech if "loi_as_is" in x["lop"].split("+")
                and abs(abs(Decimal(x["engine"]) - Decimal(x["dap_an"])) - CHINH_TAY) <= ATOL_CHINH_TAY]
    chinh_tay, trung = chuoi_chinh_tay(ung_vien)
    vang_ma = Counter()
    for k, n in vang.items():
        vang_ma[k] += n
    tp_ra = {ph: {**dict(v), "khop": v["khop_co_so"] + v["o_0_0"]} for ph, v in sorted(theo_phan.items())}
    return {"dem": dict(dem), "theo_phan": tp_ra, "lop": lop, "chua_co_dau_vao": dict(sorted(chua.items())),
            "engine_vang": dict(sorted(vang_ma.items())), "ngoai_truc": dict(sorted(ngoai.items())),
            "chinh_tay": chinh_tay, "chinh_tay_trung_0_5": trung, "ngoai_khuon": dict(sorted(nk.items())),
            "max_lech_khop": str(mx),
            "lech_FLS": sorted(x["o"] for x in lech if x["lop"] == LECH_FLS),
            "_lech": lech}


def dem_dap_an_dung(anh: Mapping[str, Any]) -> int:
    """Số ô SỐ của đáp án DỪNG *(mẫu số bị bỏ — Đ3: phải > 0 để câu "dừng" có nghĩa)*."""
    n = 0
    for r in anh["dong"]:
        for c, v in r.items():
            if c not in ("thu_tu", "dong_sheet", "cap") and _so(v) is not None and not isinstance(v, dict):
                n += 1
    return n


@dataclass(frozen=True)
class MongC5c:
    so: Mapping[str, Any] | None = None


def mong_c5c_mac_dinh() -> MongC5c:
    from tools.do_hd2_c5c_mong import MONG
    return MongC5c(so=MONG)


@dataclass
class ThanhQuaC5c:
    """`phan_xu` = phép so khớp `mong` hai chiều; `dat` = phán CỔNG *(`H14-R1-01`: `None` khi còn đáp án ô so = 0 chưa
    có chữ ký chủ "DỪNG có tên" — ⛔ đo được ⛔ phải đạt)*."""
    phan_xu: PhanXu
    hd2_cong: dict[str, Any]
    dat: bool | None = None
    theo_dap_an: dict[str, Any] = field(default_factory=dict)
    bao: dict[str, dict[str, Any]] = field(default_factory=dict)


def _khac(thuc: Any, mong: Any, duong: str, ly: list[str]) -> None:
    c3d._khac(thuc, mong, duong, ly)


def them_phan_cb(b: dict[str, Any], so_du: Mapping[str, Any] | None) -> dict[str, Any]:
    """Báo cáo CF + phần `cb` *(khối số dư theo LE — `fls.bao_cao.so_du_le`)*. CHECK IX.PL ⛔ áp cho `cb` *(tính TRƯỚC)*.
    Ảnh số dư vắng ⇒ phần DỪNG `chua_co_dau_vao` có tên *(⛔ ngầm 0)*. `chep = False`: engine TÍNH từ số dư."""
    nam, thang = divmod(int(b["ky"]), 100)
    mo_ta: dict[str, Any] = {"id": "cb", "nguon": "ccr_so_du", "truc": "ngay", "chep": False,
                             "khoi": sorted({le for le, _dv in sd.KHUON_CB_615}),
                             "cot": [d.isoformat() for d in sd.ngay_cua_thang(nam, thang)]}
    try:
        o = sd.bang_so_du_le(nam, thang, so_du)
    except sd.LoiSoDu as l:
        mo_ta["dung"] = "chua_co_dau_vao"
        b["chua_co_dau_vao"].append({"phan": "cb", "nguon": "ccr_so_du", "khoi": mo_ta["khoi"], "can": str(l)})
        b["phan"].append(mo_ta)
        return b
    for (le, dv, c), v in o.items():
        b["o"][bc.khoa_o("cb", le, dv, c)] = str(v)
    mo_ta["so_o"] = len(o)
    b["phan"].append(mo_ta)
    return b


def dung_bao(ne: NguonEngine) -> dict[str, dict[str, Any]]:
    """Dựng 5 báo cáo bằng CÙNG engine *(FS là tham số)* — đầu vào = lưới engine; 615 + phần `cb` từ ảnh số dư."""
    ra = {m: bc.daily_report(cfg["ky"], cfg["fs"], ne.luoi, loai=cfg["loai"]) for m, cfg in DAP_AN.items()}
    for m, cfg in DAP_AN.items():
        if "cb" in (cfg.get("phan_khuon") or {}).values():
            them_phan_cb(ra[m], ne.so_du)
    return ra


def so_sanh_c5c(ne: NguonEngine, dap_an: Mapping[str, Mapping[str, Any]], mong: MongC5c,
                bao: Mapping[str, Mapping[str, Any]] | None = None) -> ThanhQuaC5c:
    ly: list[str] = []
    for g, ok in ne.cong.items():
        if not ok:
            ly.append(f"nền {g} ĐỎ ⇒ lưới engine ⛔ tin được")
    for anh, pd in (("sign_off_dau_vao", "605"), ("ccr_daily_report_2", "610")):
        try:
            rao.kiem_dau_vao_hop_le(anh, pd)
            ly.append(f"rào DT13 ⛔ chặn `{anh}` → PD {pd} ⇒ vòng tròn đáp án mở (DT13-R1-01/02)")
        except rao.DauVaoSaiChoError:
            pass
    bao = dict(bao) if bao is not None else dung_bao(ne)
    m = mong.so
    if m is None:
        ly.append("`mong` chưa khai ⇒ ⛔ tin (Đ5)")
        m = {}
    theo: dict[str, Any] = {}
    tong = Counter()
    lop_tong = Counter()
    for ma_da, cfg in DAP_AN.items():
        dc = o_dap_an(cfg["doi_chieu"], dap_an[cfg["doi_chieu"]])[0] if cfg.get("doi_chieu") else None
        r = so_mot(ma_da, dap_an[ma_da], bao[ma_da], ne, doi_chieu=dc)
        lech = r.pop("_lech")
        theo[ma_da] = r
        for k in ("tong_o", "khop", "khop_co_so", "o_0_0", "o_co_so", "khop_tinh", "khop_chep"):
            tong[k] += r["dem"].get(k, 0)
        for l, v in r["lop"].items():
            lop_tong[l] += v["so_o"]
        if r["dem"].get("tong_o", 0) == 0:
            ly.append(f"{ma_da}: 0 ô được so ⇒ ⛔ đo được gì (Đ3)")
        for x in [x for x in lech if x["lop"] == LECH_FLS][:10]:
            ly.append(f"{ma_da}: ô lệch FLS `{x['o']}`: engine {x['engine']} · đáp án {x['dap_an']}")
        mg = (m.get("dap_an") or {}).get(ma_da)
        thuc = {k: v for k, v in r.items() if k not in ("max_lech_khop",)}
        _khac(thuc, mg, f"dap_an.{ma_da}", ly)
    dung: dict[str, Any] = {}
    for ma_da, cfg in DUNG.items():
        n = dem_dap_an_dung(dap_an[ma_da])
        dung[ma_da] = {"o_dap_an_so": n, "can": cfg["can"], "trang_thai": "chua_co_dau_vao"}
        if n == 0:
            ly.append(f"{ma_da}: đáp án DỪNG mà 0 ô số ⇒ câu 'dừng' ⛔ nghĩa (Đ3)")
    _khac({k: v["o_dap_an_so"] for k, v in dung.items()}, m.get("dung"), "dung", ly)
    check = {ma_da: {"theo_phan": b["check"]["theo_phan"], "so_do": b["check"]["so_do"],
                     "do_sha256": _sha(b["check"]["do"])} for ma_da, b in bao.items()}
    _khac(check, m.get("check"), "check", ly)
    fs = {ma_da: {"fs": b["fs"], "phan": [p["id"] for p in b["phan"]]} for ma_da, b in bao.items()}
    lech_co_chu_dich = sum(v for l, v in lop_tong.items() if l != LECH_FLS)
    ly += [f"DUNG_KY {x}" for x in kiem_dung_ky(DUNG_KY)]      # chữ ký hỏng ⇒ ĐỎ có tên (H14-R2-02)
    px = PhanXu(not ly, tuple(ly))
    # ── ⭐ `H14-R1-01` (Đ3 · Đ5): ô so > 0 cho TỪNG đáp án. Đáp án ô so = 0 ⇒ ⛔ đo được ⇒ cổng `null` CÓ TÊN *(⛔ `true`)*,
    #    trừ khi chủ ký "DỪNG có tên" (`DUNG_KY`). Độ phủ mỗi đáp án = ô so / ô SỐ của ảnh — in cạnh nhau *(Đ4)*. ──
    do_phu: dict[str, dict[str, Any]] = {}
    ky_hop_le = _dung_ky_hop_le()
    for ma_da in list(DAP_AN) + list(DUNG):
        n = dem_dap_an_dung(dap_an[ma_da])
        o = theo[ma_da]["dem"].get("tong_o", 0) if ma_da in theo else 0
        ngoai: dict[str, int] = {}
        if ma_da in theo:
            ngoai = {**{f"chua_co_dau_vao:{k}": v for k, v in theo[ma_da]["chua_co_dau_vao"].items()},
                     **{f"ngoai_khuon:{k}": v for k, v in theo[ma_da].get("ngoai_khuon", {}).items()}}
        do_phu[ma_da] = {"o_dap_an_so": n, "o_so": o, "o_so_chua_so": n - o, "ngoai_mau_so_co_ten": ngoai,
                         "dung_ky": ky_hop_le.get(ma_da)}
    khong_do: list[str] = []
    for ma_da, v in do_phu.items():
        if v["o_so"] > 0:
            continue
        if v["dung_ky"]:
            continue                                         # chủ đã ký DỪNG có tên ⇒ ngoại lệ DUY NHẤT
        can = DUNG[ma_da]["can"].split(";")[0] if ma_da in DUNG else "đáp án so được mà 0 ô so"
        khong_do.append(f"{ma_da}: ô so 0/{v['o_dap_an_so']} ô số — DỪNG `chua_co_dau_vao` CHƯA có chữ ký chủ "
                        f"'DỪNG có tên' (cần: {can})")
    phu_mot_phan = [f"{m}: ô so {v['o_so']}/{v['o_dap_an_so']} ô số · {v['o_so_chua_so']} ô số chưa so"
                    + (" (" + " · ".join(f"{k} {n}" for k, n in v["ngoai_mau_so_co_ten"].items()) + ")"
                       if v["ngoai_mau_so_co_ten"] else "")
                    for m, v in do_phu.items() if m == "615"]
    dat_cong: bool | None = (None if khong_do else True) if px.dat else False
    hd2 = {
        "bang": "HD2.WP-C5c", "goi": "WP-C5c",
        "mo_ta": "RP.PL · RP.CF: Daily Report 2 · 3 dựng theo khuôn (fls.bao_cao.bao_cao.daily_report, FS tham số) từ "
                 "lưới engine (CFA1 H5/H6 · PLA3 PM+HR H8 · ATL H12+H13) ↔ đáp án 607 · 608 · 609 · 610 · 615 (A-CCR, khuôn "
                 "CF: Unit: mUSD ↔ ngay · CM Cumulative ↔ luy_ke · CB Cash Balance by LE ↔ cb: số dư fls.bao_cao.so_du_le "
                 "từ ảnh DT13 ccr_so_du_ccr · ccr_so_du_cash) từng ô; 605 DỪNG (chua_co_dau_vao, chưa ký ⇒ cổng "
                 "null); lệch THỪA KẾ lớp bằng truy ngược ô nguồn",
        "nguon_dau_vao": ["WP-C3a lưới cfa1_daily (tests/fixture/dap_an/gl_cf_dau_vao.json)", "WP-C3b lưới cfa1_yhqm",
                          "WP-C3d lưới pla3_pm_hr_daily (gl_pl_dau_vao.json + hr_pl_dau_vao.json)",
                          "WP-C5a + WP-C5b lưới ATL của FLS (IX.ALR kho cờ 2025 BẬT ký · IX.PL kho)",
                          "DT13 ảnh đầu vào số dư 615: tests/fixture/dau_vao/ccr_so_du_ccr.json + ccr_so_du_cash.json "
                          "(qua rào kiem_dau_vao_hop_le)"],
        "dap_an": [f"tests/fixture/dap_an/{c['anh']}.json" for c in DAP_AN.values()],
        "dap_an_dung": dung,
        "khoa": "đáp án × phần (ngay · luy_ke[:FS]) × khối × mã × cột (ngày ISO | kỳ); ô đáp án là số, cột thuộc trục, "
                "phần có đầu vào, engine có ô",
        "dung_sai": {"atol": str(ATOL), "rtol": "0", "chinh_tay": f"|e−a| = {CHINH_TAY} ± {ATOL_CHINH_TAY}"},
        "tong_o": tong["tong_o"], "mong_tong_o": sum(((m.get("dap_an") or {}).get(x) or {}).get("dem", {})
                                                     .get("tong_o", 0) for x in DAP_AN) or None,
        "o_co_so": tong["o_co_so"], "khop_co_so": tong["khop_co_so"], "o_0_0": tong["o_0_0"],
        "khop": tong["khop"], "khop_tinh": tong["khop_tinh"], "khop_chep": tong["khop_chep"],
        "lech_co_chu_dich": lech_co_chu_dich,
        "mong_lech_co_chu_dich": sum(v.get("so_o", 0) for x in DAP_AN
                                     for l, v in (((m.get("dap_an") or {}).get(x) or {}).get("lop") or {}).items()
                                     if l != LECH_FLS),
        "lech_ngoai_ten": lop_tong.get(LECH_FLS, 0),
        "khop_ghi_chu": "tong_o = Σ 5 đáp án ô so = o_co_so + o_0_0; khop = ô khớp THẬT (khop_co_so) + o_0_0; "
                        "khop + lech_co_chu_dich = tong_o; khop_co_so = khop_tinh (engine TÍNH từ đầu vào) + khop_chep "
                        "(engine CHÉP ô ảnh đầu vào mang giá trị dán của chính sổ báo cáo — vd DR2 A-CCR; đếm RIÊNG, ⛔ "
                        "gộp); ô chua_co_dau_vao / engine_vang / ngoai_truc / ngoai_khuon NGOÀI mẫu số",
        "lech_co_ten": {"lop_thua_ke": dict(sorted(lop_tong.items())),
                        "chinh_tay_actor": {x: theo[x]["chinh_tay"] for x in DAP_AN if theo[x]["chinh_tay"]},
                        "chinh_tay_trung_0_5": {x: theo[x]["chinh_tay_trung_0_5"] for x in DAP_AN
                                                if theo[x]["chinh_tay_trung_0_5"]},
                        "chinh_tay_goc": "ATL AH12 `='Report I PLA3 Y H Q M | PM + HR'!AH12-0.5` (GROUP·OMC·2025M02) — "
                                         "chuỗi lan = mã khối GROUP mang 0,5 ở M02 VÀ Q1 · H1 · Y; ô 0,5 ngoài chuỗi = "
                                         "trùng ngẫu nhiên (chinh_tay_trung_0_5) — chỉnh tay ⛔ actor; ⛔ chép vào config"},
        "fs_tham_so": fs,
        "check": check,
        "theo_dap_an": theo,
        "pl5_bo_khoi_luoi": ne.pl5_bo,
        "do_phu": do_phu,
        "khong_do_duoc": khong_do, "phu_mot_phan": phu_mot_phan,
        "dung_co_ky": [f"{m}: DỪNG có chữ ký {k['nguoi_ky']} {k['ngay']}" for m, k in ky_hop_le.items()],
        "dat_mong": px.dat,
        "dat": dat_cong, "ly_do": list(px.ly_do),
    }
    return ThanhQuaC5c(phan_xu=px, hd2_cong=hd2, theo_dap_an=theo, bao=bao, dat=dat_cong)


def nap_nen_kho(conn, *, actor: str = "bai-h14") -> None:
    """Nạp nền cấu hình cổng vào kho *(bài: giao dịch ROLLBACK; `--ghi`: kho TEST — `PG_DSN_TEST`)*: IX.PER *(21/10,
    luật A)* · IX.ALR *(17 luật MM `@202501` rồi KÝ BẬT 2025 = `ix_alr_2025_bat.json` — quyết chủ 22/11)* · IX.PL.
    ⛔ kho THẬT *(nơi gọi chọn `conn`)*; ⛔ IX.TMP *(bản ký là ĐẦU RA, đưa riêng bằng `dua_ban_ky`)*."""
    from fls.cau_hinh import luat_pb
    from fls.repo import cau_hinh_repo as chc
    chc.nap_ix_per(conn, actor=actor, ngay_dau="2024-10-21", luat="A",
                   nguon=f"{actor}:ISP-3.1.2-Step46 (IX.PER = 21/10, C6)")
    nen = c5a.alr_tu_anh_mm()
    chc.nap(conn, luat_pb.BANG, [(luat_pb.khoa_cua(x.hd, x.tu_ky),
                                  {"hd": x.hd, "tu_ky": x.tu_ky, "nhan_mm": x.nhan_mm, "bat": x.bat,
                                   "ngoai_le": list(x.ngoai_le_cdt1)}) for x in nen.luat],
            nguon=f"{actor}:{c5a.ANH_MM.name}", actor=actor)
    import json
    nguoi_ky = json.loads(c5a.TEP_KY.read_text(encoding="utf-8"))["ky"]["nguoi_ky"]   # chữ ký CỦA người trong tệp
    chc.ky_bat_ix_alr(conn, str(c5a.TEP_KY), actor=nguoi_ky)
    chc.nap_ix_pl(conn, actor=actor)


def nap_dap_an() -> dict[str, dict[str, Any]]:
    ra = {m: nap_anh(DA / f"{c['anh']}.json") for m, c in DAP_AN.items()}
    ra.update({m: nap_anh(DA / f"{c['anh']}.json") for m, c in DUNG.items()})
    return ra


def _do(ly: tuple[str, ...]) -> ThanhQuaC5c:
    return ThanhQuaC5c(phan_xu=PhanXu(False, ly), hd2_cong={"bang": "HD2.WP-C5c", "goi": "WP-C5c", "dat": False,
                                                             "ly_do": list(ly)}, dat=False)


def chay_wp_c5c(dsn: str | None = None, conn=None) -> ThanhQuaC5c:
    """IX.PER + IX.ALR + IX.PL ĐỌC TỪ KHO *(`conn` tuỳ chọn — bài chạy trong giao dịch rollback)*."""
    lich, l1 = c5a._lich_tu_conn(conn) if conn is not None else c3d._lich_tu_kho(dsn)
    alr, l2 = c5a._alr_tu_kho(dsn, conn)
    dn, l3 = c5b._pl_tu_kho(dsn, conn)
    if lich is None or alr is None or dn is None:
        return _do(tuple(x for x in (l1, l2, l3) if x))
    return so_sanh_c5c(nguon_engine(lich, alr, dn), nap_dap_an(), mong_c5c_mac_dinh())


def in_bao(tq: ThanhQuaC5c) -> None:
    hh = tq.hd2_cong
    print("══ WP-C5c · RP.PL · RP.CF Daily Report 2 · 3 (khuôn, FS tham số) ↔ 605 · 607–610 · 615 từng ô")
    for ma_da, r in hh.get("theo_dap_an", {}).items():
        d = r["dem"]
        print(f"  {ma_da} ({DAP_AN[ma_da]['fs']}): ô so {d.get('tong_o', 0)} = có số {d.get('o_co_so', 0)} + 0=0 "
              f"{d.get('o_0_0', 0)} · khớp {d.get('khop', 0)} (thật {d.get('khop_co_so', 0)}) · lệch theo lớp "
              + (" · ".join(f"{k} {v['so_o']}" for k, v in r["lop"].items()) or "0")
              + f" · chua_co_dau_vao {sum(r['chua_co_dau_vao'].values())} · ngoài khuôn "
              f"{sum(r.get('ngoai_khuon', {}).values())} · engine vắng "
              f"{sum(r['engine_vang'].values())} · ngoài trục {sum(r['ngoai_truc'].values())} · chỉnh tay "
              f"{len(r['chinh_tay'])} (+ {len(r.get('chinh_tay_trung_0_5', []))} trùng 0,5 ngoài chuỗi)")
    for ma_da, v in hh.get("dap_an_dung", {}).items():
        print(f"  {ma_da}: DỪNG — {v['o_dap_an_so']} ô số ⛔ so · cần: {v['can']}")
    if "tong_o" in hh:
        print(f"  Σ ô so {hh['tong_o']} · khớp {hh['khop']} (thật {hh['khop_co_so']}/{hh['o_co_so']}) · lệch có chủ "
              f"đích {hh['lech_co_chu_dich']} · lệch FLS {hh['lech_ngoai_ten']}")
        for ma_da, c in hh["check"].items():
            print(f"  CHECK {ma_da}: đỏ {c['so_do']} · " + " · ".join(
                f"{p}: " + ", ".join(f"{ph} {dict((k, v) for k, v in d.items() if v)}" for ph, d in x.items())
                for p, x in c["theo_phan"].items()))
    for x in hh.get("phu_mot_phan", []):
        print(f"  độ phủ {x}")
    for x in hh.get("ly_do", []):
        print(f"  ⛔ {x}")
    for x in hh.get("khong_do_duoc", []):
        print(f"  ⛔ đo được: {x}")
    kq = {True: "ĐẠT", False: "ĐỎ", None: "⛔ ĐO ĐƯỢC (cổng null)"}[tq.dat]
    print(f"  KẾT: {kq} · so mong: {tq.phan_xu.mot_dong}")
