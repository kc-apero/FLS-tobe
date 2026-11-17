"""ĐÓNG BĂNG một bản đọc giá trị sheet thành ẢNH có checksum + cổng *(ISP 3.1.2 · DT2)*.

    python tools/dong_bang_sheet.py <khuôn> <bản_thô.json> --mong N [--ra <tệp>]
    python tools/dong_bang_sheet.py ix_fx  <bản_thô.json> --mong 37
        ⇒ tests/fixture/cau_hinh/ix_fx.json

Exit:
  **0** cổng ĐẠT — ảnh ghi ở `--ra`, hoặc đường mặc định của khuôn.
  **1** cổng ĐỎ — ảnh VẪN ghi, đúng như nguồn *(ISP B3)*: ở `--ra` nếu có; ⛔ `--ra` thì ở tệp
        CẠNH `<ra>.DO.json` — ⛔ bao giờ đè ảnh ở đường mặc định *(`DT2-R1-01`)*.
  **2** TỪ CHỐI — ⛔ ghi, ⛔ tạo thư mục, tệp có sẵn ⛔ bị đụng; đúng MỘT dòng `⛔ TỪ CHỐI …`.
  **3** LỖI — ghi đĩa hỏng *(một dòng `⛔ LỖI GHI …`)* hay khuôn nổ *(traceback + một dòng
        `⛔ LỖI …`)*; ⛔ ảnh mới nào được ghi *(ghi nguyên tử)*. ⛔⛔ Mã riêng vì R1 đo
        *(`DT2-R1-05`)*: `--ra <thư mục>` từng ra traceback **exit 1** — trùng mã *"cổng ĐỎ, ảnh
        đã ghi"* trong khi ⛔ tệp nào được ghi.

⭐ **Vì sao có tệp này.** AP v3.1.2 §3.2.4 ghi chỗ AS-IS gõ cứng của bảng tỷ giá
`9.2.Exchange Rate` *(APERO | FS2, nhập tay; CF · P&L · A-CCR đều `IMPORTRANGE` nó)* và hậu quả
đã thấy: *"tháng thiếu ⇒ SUMIFS = 0 ⇒ mất số không báo; tháng nhập hai dòng ⇒ cộng đôi"*. Bước
sau *(C1 kiểm tỷ giá · C5 nạp kho)* cần một ẢNH đứng yên — đọc MỘT lần, đóng băng có checksum,
và một cổng **in ra** tháng thiếu/trùng/lạc thay vì im lặng. Khuôn là *cột chọn + khoá* nên
dùng lại được cho các ảnh DT3…DT11 *(xem "Khuôn" dưới)*, ⛔ viết công cụ thứ hai.

⭐⭐ **Khuôn = MỘT TỆP** ở `tools/khuon_dong_bang/<tên>.py` *(orchestrator 16/11)*. Bản đầu khai
khuôn trong bảng `KHUON` ngay tệp này — các bước DT3…DT12 thêm khuôn SONG SONG thì cùng sửa một
tệp ⇒ phải xếp hàng. Giờ công cụ tìm khuôn theo tên tệp; khuôn lạ ⇒ TỪ CHỐI như cũ. Giao kèo
*(kiểm lúc nạp — `nap_khuon`)*: hằng `BANG · KHOA · KIEU_KHOA · COT · RA` *(KHOA + COT đôi một
khác tên — `DT2-R2-03`)* + hàm `thieu_lac(dong) → {"thieu", "lac", "dai"}` *(`thieu`/`lac` là
`list`/`tuple`; `ValueError` = ⛔ đo được)*. Chia việc:
  · **công cụ** giữ phần CHUNG — đếm `--mong` · khoá hỏng · khoá trùng · ô rỗng · ô ⛔ số · soát
    riêng tư · checksum · ghi;
  · **khuôn** giữ phần RIÊNG của bảng — chọn cột nào, và *thiếu/lạc nghĩa là gì*. Khuôn `ix_fx`
    GỌI `kiem` của C1 *(`DT2-R1-03`: một định nghĩa — xem docstring `ix_fx.py`)*.

⭐⭐ **DT3 — bốn mục TUỲ CHỌN của giao kèo** *(ISP 3.1.2 Step 10 · `WO-106` AC-4: "⛔ sửa công cụ
trừ khi bài đòi — khai lý do")*. **Lý do — bài đòi:** ba nguồn DT3 *(cây ATL · Mapping Master ·
CDT Correct)* đều là bảng **CHỮ** *(mã · tên · ánh xạ)*, mà bản DT2 chỉ biết khoá `yyyymm` và
đòi mọi ô cột chọn là SỐ — ô chữ ⇒ *"ô ⛔ số"* ⇒ ĐỎ, khoá chữ ⇒ TỪ CHỐI *(đo: 20 bài
`test_GIAO_KEO_*` của `tests/du_lieu/test_anh_cau_hinh.py` ĐỎ `KIEU_KHOA='ma' ⛔ thuộc
['yyyymm']`)*. Hai nguồn còn ⛔ ở hình `{cot, dong}`: cây ATL là hàng `{A, cap_cot, o}` phải SUY
cha/cấp/nhóm; Mapping Master là lưới thô A…P phải đi qua `fls.adapters.mapping_master.doc_cot`
*(⛔ khuôn đọc thứ hai)*. Chính chú thích cũ của `KIEU_KHOA_BIET` đã hẹn: *"Kiểu khác ⇒ thêm khi
có bước cần, ⛔ khai trước"* — DT3 là bước cần. Khuôn ⛔ khai mục nào thì công cụ chạy **y như
cũ** — ảnh `ix_fx` giữ từng byte *(bài `test_DT2_B1_anh_IX_FX_TAI_TAO_…` canh)*:
  · `KIEU_KHOA = "ma"` — khoá CHỮ: hợp lệ = ô chữ khác rỗng; trùng so sau khi GỘP khoảng trắng
    *(`"A1 "` trùng `"A1"` — bên tra theo mã sẽ gộp, nên hai dòng ấy là một khoá hai giá trị)*.
  · `KIEU_COT = {cột: "chu" | "chu?"}` — cột CHỮ *(`chu` ⛔ rỗng · `chu?` được rỗng)*; cột ⛔
    khai giữ luật SỐ cũ. Ô số/bool ở cột chữ ⇒ *"ô ⛔ chữ"* ⇒ ĐỎ — đối xứng với *"ô ⛔ số"*.
  · `chuan_bi(tho) -> {cot, dong, phu?, ghi_chu?}` — bản thô HÌNH DẠNG orchestrator → bảng của
    công cụ. `ValueError` ⇒ TỪ CHỐI *(bản thô ⛔ dùng được)*; nổ/trả sai hình ⇒ LỖI exit 3.
    Bảng phụ `phu` *(vd: 6 dòng tiêu đề nhóm của cây ATL)* vào ảnh dưới `phu.<tên>`, ô mã hoá như
    dòng chính, dòng mang `thu_tu`, và **vào checksum** — bảng phụ ⛔ vào checksum thì sửa nó là
    IM LẶNG *(bài `test_GIAO_KEO_checksum_DOI_khi_chi_BANG_PHU_doi`)*. `ghi_chu` *(khuôn tự giải
    thích phép biến đổi — băm gì, bỏ cột nào)* ⇒ `ghi_chu_khuon`.
  · `PHU_MONG = {tên: số dòng}` — Đ5 cho bảng phụ: khác ⇒ ĐỎ. Mỗi bảng phụ PHẢI khai *(bảng phụ
    ⛔ khai ⇒ lỗi khuôn)*; `0` là mong hợp lệ cho bảng phụ *(bảng LỖI — mẫu số là bảng chính,
    vốn đã bị `--mong ≥ 1` chặn rỗng)*.
  Soát riêng tư phủ cả tên cột bảng phụ; bản thô có `cot` thì soát TRƯỚC khi khuôn đọc giá trị.

⛔⛔ **Đọc Drive ⛔ ở đây** *(O7 = A: orchestrator đọc, agent nhận tệp)*. Đầu vào là JSON
`{nguon, doc_luc, cach_doc, cot, dong}` — `cot` là hàng tiêu đề, `dong` là các hàng giá trị theo
**thứ tự của sheet**. Vì thế `fls.oracle.doc.doc_dan` *(đọc dần, retry)* và
`fls.oracle.doc_du` *(đọc lại cột then chốt)* thuộc **lượt đọc** của orchestrator, ⛔ thuộc tệp
này; ở đây chỉ còn phần của `doc_du` áp được lên MỘT bản đọc: **ô rỗng là ĐỎ**, in kèm mẫu số.

Tái dùng *(⛔ viết lại)*:
  · `fls.oracle.anh_chup.AnhChup.checksum()` — sha256 nội dung, độc lập thứ tự, **từ chối ảnh
    rỗng**; `checksum_noi_dung` = 16 hex đầu *(khuôn `tests/fixture/pm_join.json`)*.
  · `fls.adapters.pm_join.PM_COT_RIENG_TU` — bản đen riêng tư khai **một chỗ**.

⭐⭐ **Năm quyết định, mỗi cái chặn một lỗi đã biết:**

  ① **Số đi qua `Decimal`, ⛔ `float`.** Sheets HIỂN THỊ SGD 202507 là `20,692` mà giá trị là
    **`20691.51`** *(orchestrator đo 16/11 — vì thế bản thô đọc bằng `effectiveValue`)*. Một
    `float` giữ ~17 chữ số có nghĩa nên `19744.785000000000001` về `19744.785` im lặng. Mọi ô
    SỐ ghi thành **chuỗi đúng chữ số của JSON thô** — ⛔ làm tròn, ⛔ định dạng lại.
    ⛔⛔ Và ô **CHỮ** ghi thành `{"chu": "…"}` *(`DT2-R1-02`)*: bản đầu giữ chuỗi nguyên ⇒ trong
    ảnh, ô số `20691.51` và ô văn bản `"20691.51"` **giống từng byte** — R1 đo cột `Month` toàn
    chuỗi ra ảnh y hệt ảnh đã commit, và SGD = `"20,692"` qua cổng `[ĐẠT]` trong khi `kiem` của
    C1 từ chối nó. Bọc ô chữ *(⛔ đổi cách ghi ô số)* thì ảnh SẠCH giữ nguyên từng byte, còn
    ảnh có ô chữ thì bên nhận *(C1 `_so`)* thấy chữ là chữ.

  ② **Thứ tự hàng là DỮ LIỆU.** `AnhChup.checksum()` cố ý độc lập thứ tự đọc *(đọc dần/cắt
    lát)*. Nhưng ở sheet này dòng `202306` đứng **sau** `202512` — thứ tự sheet là một phần của
    nguồn ⇒ mỗi dòng mang `thu_tu` *(vị trí 1-based trong bản đọc, ⛔ số hàng sheet — bản thô ⛔
    khai hàng tiêu đề)* ⇒ đổi chỗ hai hàng là đổi checksum. ⚠ Thứ tự vào CHECKSUM, ⛔ vào định
    nghĩa *lạc* *(`DT2-R1-03`)*.

  ③ **`ngay_dong_bang` = `doc_luc` của bản thô**, ⛔ đồng hồ máy. Ảnh là của MỘT ngày đọc;
    lấy ngày từ bản thô thì chạy lại công cụ ra **đúng từng byte** ⇒ ảnh đã commit kiểm được
    bằng cách tái tạo *(bài `test_DT2_B1_anh_IX_FX_TAI_TAO_…`)*. `doc_luc` phải ĐÚNG khuôn
    `YYYY-MM-DD` *(`DT2-R1-06`: `date.fromisoformat` của Python ≥ 3.11 nhận cả `2026-W46-1` lẫn
    `20261116`, và bản đầu ghi nguyên chuỗi ấy vào ảnh)*.

  ④ **Riêng tư từ chối CHẶT hơn nguồn khai.** Bản thô có một cột thuộc `PM_COT_RIENG_TU` ⇒
    TỪ CHỐI cả lượt, **kể cả khi khuôn ⛔ chọn cột ấy**. Tên so sau khi gộp khoảng trắng *(như
    `pm_join.loc_tho`)* **và** ⛔ phân biệt hoa thường. ⛔ In giá trị của cột ấy ở bất cứ đâu.
    Cột tiêu đề RỖNG mà có dữ liệu cũng TỪ CHỐI *(`DT2-R1-08`)*: cột ⛔ tên thì ⛔ soát theo
    tên được, và ô của nó sẽ mất im lặng — cùng lý do từ chối dòng dài hơn tiêu đề.

  ⑤ **Cổng khai `mong` (Đ5) — và đếm dòng thôi là CHƯA ĐỦ.** 37 dòng mà `202409` bị nhập thành
    `202408` lần hai thì đếm dòng vẫn khớp — đúng ca *"cộng đôi"* của AP §3.2.4. ⇒ ĐỎ khi: số
    dòng ≠ `--mong` *(cả thừa lẫn thiếu)* · khoá trùng · tháng thiếu *(định nghĩa của khuôn)* ·
    khoá ⛔ phải `yyyymm` SỐ · ô rỗng ở cột chọn · ô ⛔ số ở cột chọn · thiếu/lạc ⛔ đo được.
    **Lạc thì GHI NHẬN, ⛔ đỏ**: AP §3.2.1 đo bảng thật *"37 dòng 202401 → 202612 (kể cả dòng
    lạc 202306)"* — đó là nguồn, ⛔ phải lỗi đọc.

⛔ **Bia — luật *lạc* theo thứ tự sheet đã BỎ** *(`DT2-R1-03`)*. Bản đầu định nghĩa *lạc* =
*"hàng có khoá nhỏ hơn khoá lớn nhất đứng trước nó"*, *thiếu* = lỗ giữa min/max của hàng ⛔ lạc;
và tự ghi *"⚠ dòng lạc đứng ĐẦU bảng thì ⛔ bị gọi lạc — các tháng ở giữa hiện thành thiếu"*.
R1 đo: chính ca ấy ra 6 tháng thiếu GIẢ, và C1 cùng lúc định nghĩa khác. Giờ thiếu/lạc là việc
của khuôn; công cụ ⛔ còn định nghĩa nào.
"""
from __future__ import annotations

import argparse
import copy
import importlib.util
import json
import os
import re
import sys
import tempfile
import traceback
from dataclasses import dataclass, field
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.adapters.pm_join import PM_COT_RIENG_TU  # noqa: E402
from fls.oracle.anh_chup import AnhChup           # noqa: E402

#: Thư mục khuôn — mỗi tệp `<tên>.py` là MỘT khuôn *(tên tệp = tên khuôn ở dòng lệnh)*.
THU_MUC_KHUON = Path(__file__).resolve().parent / "khuon_dong_bang"
#: Tên khuôn hợp lệ — loại `__init__` và tệp `_…` *(⛔ phải khuôn)*.
_TEN_KHUON = re.compile(r"[a-z][a-z0-9_]*")
#: Kiểu khoá công cụ biết kiểm *(khoá hỏng)*. Kiểu khác ⇒ thêm khi có bước cần, ⛔ khai trước.
#: `ma` thêm ở DT3 *(khoá CHỮ của cây ATL · Mapping Master · CDT Correct — xem docstring)*.
KIEU_KHOA_BIET = ("yyyymm", "ma")
#: Kiểu cột chọn *(DT3)*: `so` = luật DT2 *(ô SỐ, ⛔ rỗng)* · `chu` = ô CHỮ ⛔ rỗng · `chu?` = ô
#: chữ hoặc rỗng. Cột ⛔ khai ở `KIEU_COT` của khuôn = `so` ⇒ khuôn DT2 chạy y như cũ.
KIEU_COT_BIET = ("so", "chu", "chu?")


@dataclass(frozen=True)
class Khuon:
    """Một khuôn đóng băng: chọn cột nào, khoá nào, ghi ra đâu, thiếu/lạc nghĩa là gì.

    ⛔ Ánh xạ cột theo **TÊN**, ⛔ theo vị trí *(bài học `pm_join.loc_tho`: cột xê dịch thì bản
    khai vị trí lệch IM LẶNG, còn tên thì ⛔)*.
    """
    ten: str
    bang: str
    khoa: str
    kieu_khoa: str
    cot: tuple[str, ...]
    ra: str                 # tương đối với gốc repo
    thieu_lac: Callable[[list[dict[str, Any]]], dict[str, Any]]
    # ── tuỳ chọn *(DT3)* — khuôn ⛔ khai ⇒ y như DT2 ──
    kieu_cot: dict[str, str] = field(default_factory=dict, compare=False)
    chuan_bi: Callable[[dict], dict] | None = field(default=None, compare=False)
    phu_mong: dict[str, int] = field(default_factory=dict, compare=False)

    def cot_theo_kieu(self) -> tuple[list[str], list[str], list[str]]:
        """→ (cột ⛔ được rỗng, cột SỐ, cột CHỮ) — theo thứ tự `cot`, mỗi cột ở đúng chỗ của nó."""
        k = {c: self.kieu_cot.get(c, "so") for c in self.cot}
        return ([c for c in self.cot if k[c] != "chu?"], [c for c in self.cot if k[c] == "so"],
                [c for c in self.cot if k[c] != "so"])


_YYYYMM = re.compile(r"\d{6}")
_NGAY_ISO = re.compile(r"\d{4}-\d{2}-\d{2}")
#: Dấu thời gian ISO-8601 của lưới SA *(DT3-R1-03)* — chặt như `_NGAY_ISO` *(⛔ nhận `2026-W46-1`
#: lẫn `20261116`, bia `DT2-R1-06`)*; `ngay_dong_bang` lấy phần NGÀY.
_NGAY_GIO = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2}|Z)?")


class TuChoi(Exception):
    """Đầu vào ⛔ dùng được ⇒ exit 2, ⛔ ghi gì."""


class LoiKhuon(Exception):
    """Khuôn nổ khi chạy *(lỗi lập trình, ⛔ `ValueError`)* ⇒ exit 3, ⛔ ghi gì."""


# ── khuôn ─────────────────────────────────────────────────────────────────────

def danh_sach_khuon() -> list[str]:
    """Tên mọi khuôn có ở `THU_MUC_KHUON` — chính là các lựa chọn của dòng lệnh."""
    if not THU_MUC_KHUON.is_dir():
        return []
    return sorted(p.stem for p in THU_MUC_KHUON.glob("*.py") if _TEN_KHUON.fullmatch(p.stem))


def nap_khuon(ten: str) -> Khuon:
    """`<tên>` → `Khuon`, kiểm ĐỦ giao kèo. Hỏng gì cũng TỪ CHỐI một dòng nói tên khuôn.

    ⚠ Nạp bằng ĐƯỜNG TỆP *(⛔ `import khuon_dong_bang.x`)*: ⛔ phụ thuộc `sys.path` lúc chạy —
    chạy như script *(`sys.path[0]` = `tools/`)* hay nạp từ bài thử đều ra cùng một khuôn.

    ⛔⛔ Module khuôn được ĐĂNG KÝ `sys.modules` TRƯỚC khi chạy *(`DT2-R2-01`)*: bản đầu ⛔ đăng
    ký ⇒ khuôn có `@dataclass` + `from __future__ import annotations` *(lối viết của 41/41 tệp
    `fls/`+`tools/` có `@dataclass` — R2 đếm)* bị TỪ CHỐI `AttributeError: 'NoneType' object has
    no attribute '__dict__'`, vì `dataclasses` tra `sys.modules[cls.__module__]`. Nạp lỗi
    **hay sai giao kèo** ⇒ GỠ ra, ⛔ để lại module dở / bị khước từ cho lần nạp sau.
    """
    p = THU_MUC_KHUON / f"{ten}.py"
    if not _TEN_KHUON.fullmatch(ten) or not p.is_file():
        raise TuChoi(f"khuôn `{ten}` ⛔ có ở {THU_MUC_KHUON.name}/ (có: {danh_sach_khuon()})")
    spec = importlib.util.spec_from_file_location(f"khuon_dong_bang_{ten}", p)
    m = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = m
    try:
        spec.loader.exec_module(m)
    except Exception as e:                 # SyntaxError · ImportError · … — khuôn ⛔ dùng được
        sys.modules.pop(spec.name, None)
        raise TuChoi(f"khuôn `{ten}` ({p.name}) nạp lỗi: {type(e).__name__}: {e}") from None

    sai: list[str] = []
    for k in ("BANG", "KHOA", "RA"):
        if not isinstance(getattr(m, k, None), str) or not getattr(m, k).strip():
            sai.append(f"{k} ⛔ phải chuỗi khác rỗng")
    if getattr(m, "KIEU_KHOA", None) not in KIEU_KHOA_BIET:
        sai.append(f"KIEU_KHOA={getattr(m, 'KIEU_KHOA', None)!r} ⛔ thuộc {list(KIEU_KHOA_BIET)}")
    cot = getattr(m, "COT", None)
    if not isinstance(cot, tuple) or not cot \
            or not all(isinstance(c, str) and c.strip() for c in cot):
        sai.append("COT ⛔ phải tuple tên cột khác rỗng")
    elif isinstance(getattr(m, "KHOA", None), str) and len({m.KHOA, *cot}) != 1 + len(cot):
        # DT2-R2-03: R2 đo khuôn có KHOA ∈ COT ⇒ dòng báo `3 cột tiêu đề = khoá 1 + chọn 2 +
        #   ⛔ chọn 1 + tiêu đề rỗng 0` (4 ≠ 3 — Đ4); COT trùng ⇒ mẫu số ô `0/6` trên 3 ô thật.
        ten_cot = [m.KHOA, *cot]
        trung = sorted({c for c in ten_cot if ten_cot.count(c) > 1})
        sai.append(f"KHOA + COT ⛔ được trùng tên: {trung}")
    if not callable(getattr(m, "thieu_lac", None)):
        sai.append("thieu_lac ⛔ phải hàm")
    # ── mục tuỳ chọn *(DT3)*: khai SAI ⇒ từ chối, ⛔ rơi im lặng về mặc định ──
    kieu_cot = getattr(m, "KIEU_COT", {})
    if not isinstance(kieu_cot, dict) or not all(
            isinstance(cot, tuple) and c in cot and k in KIEU_COT_BIET
            for c, k in kieu_cot.items()):
        sai.append(f"KIEU_COT ⛔ phải {{cột thuộc COT: kiểu thuộc {list(KIEU_COT_BIET)}}}")
    chuan_bi = getattr(m, "chuan_bi", None)
    if chuan_bi is not None and not callable(chuan_bi):
        sai.append("chuan_bi ⛔ phải hàm")
    phu_mong = getattr(m, "PHU_MONG", {})
    if not isinstance(phu_mong, dict) or not all(
            isinstance(k, str) and k.strip() and type(v) is int and v >= 0
            for k, v in phu_mong.items()):
        sai.append("PHU_MONG ⛔ phải {tên bảng phụ: số dòng ≥ 0}")
    elif phu_mong and chuan_bi is None:
        sai.append("PHU_MONG ⛔ có chuan_bi — bảng phụ chỉ đến từ chuan_bi")
    if sai:
        sys.modules.pop(spec.name, None)   # khuôn bị khước từ cũng ⛔ nằm lại (bài …SAI_GIAO_KEO…)
        raise TuChoi(f"khuôn `{ten}` ({p.name}) sai giao kèo: " + " · ".join(sai))
    return Khuon(ten=ten, bang=m.BANG, khoa=m.KHOA, kieu_khoa=m.KIEU_KHOA, cot=tuple(cot),
                 ra=m.RA, thieu_lac=m.thieu_lac, kieu_cot=dict(kieu_cot), chuan_bi=chuan_bi,
                 phu_mong=dict(phu_mong))


# ── đọc ───────────────────────────────────────────────────────────────────────

def _ten(c: Any) -> str:
    """Tên cột gộp khoảng trắng — đúng phép của `pm_join.loc_tho`."""
    return " ".join(str("" if c is None else c).split())


def _o(v: Any) -> Any:
    """Ô thô → giá trị ảnh *(quyết định ①)*: số ⇒ **chuỗi đúng chữ số** của JSON thô; chuỗi ⇒
    `{"chu": …}` *(⛔ lẫn với số — `DT2-R1-02`)*; `bool` · rỗng ⇒ giữ nguyên."""
    if v is None or isinstance(v, bool):
        return v
    if isinstance(v, str):
        return {"chu": v}
    if isinstance(v, (int, Decimal)):
        return str(v)
    raise TuChoi(f"ô kiểu {type(v).__name__} ⛔ phải số/chuỗi/rỗng")


def _rong_tho(v: Any) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def _rong(v: Any) -> bool:
    """Ô ảnh RỖNG: `null` hay ô chữ chỉ có khoảng trắng *(Sheets: ô văn bản `"   "`)*."""
    return v is None or (isinstance(v, dict) and not v["chu"].strip())


def _khong_so(v: Any) -> bool:
    """Ô ảnh ⛔ SỐ mà ⛔ rỗng: ô chữ có nội dung, hay `bool`. Rỗng ∩ ⛔ số = ∅ ⇒ mỗi ô cột chọn
    rơi vào ĐÚNG một trong *số · rỗng · ⛔ số* — ⛔ ô nào bị đếm hai lần."""
    return isinstance(v, bool) or (isinstance(v, dict) and bool(v["chu"].strip()))


def _khong_chu(v: Any) -> bool:
    """Ô ảnh ⛔ CHỮ mà ⛔ rỗng: ô số *(chuỗi chữ số)* hay `bool` *(DT3 — đối xứng `_khong_so`:
    rỗng ∩ ⛔ chữ = ∅ ⇒ mỗi ô cột chữ rơi vào ĐÚNG một trong chữ · rỗng · ⛔ chữ)*."""
    return isinstance(v, (str, bool))


def _khong_hang_so(c: str) -> Any:
    raise TuChoi(f"bản thô có hằng `{c}` ⛔ phải số JSON")


def doc_ban_tho(p: Path) -> dict:
    if not p.is_file():
        raise TuChoi(f"⛔ thấy bản thô `{p}`")
    try:
        van = p.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        raise TuChoi(f"⛔ đọc được bản thô `{p}`: {type(e).__name__}: {e}") from None
    try:
        tho = json.loads(van, parse_float=Decimal, parse_constant=_khong_hang_so)
    except json.JSONDecodeError as e:
        raise TuChoi(f"bản thô ⛔ phải JSON: {e}") from None
    if not isinstance(tho, dict):
        raise TuChoi("bản thô phải là một đối tượng `{nguon, doc_luc, cach_doc, cot, dong}`")
    for k in ("nguon", "doc_luc", "cach_doc"):
        if not isinstance(tho.get(k), str) or not tho[k].strip():
            raise TuChoi(f"bản thô thiếu `{k}` *(chuỗi)* — ảnh ⛔ có xuất xứ thì ⛔ đóng băng")
    dl = tho["doc_luc"]
    try:
        if _NGAY_ISO.fullmatch(dl):
            ngay = date.fromisoformat(dl)
        elif _NGAY_GIO.fullmatch(dl):
            # lưới SA ghi doc_luc = dấu thời gian (vd 2026-11-17T04:08:29+00:00) ⇒ lấy NGÀY
            ngay = datetime.fromisoformat(dl.replace("Z", "+00:00")).date()
        else:
            raise ValueError
    except ValueError:
        raise TuChoi(f"`doc_luc` ⛔ phải ngày YYYY-MM-DD hay dấu thời gian ISO-8601 có thật: "
                     f"{dl!r}") from None
    tho["doc_luc"] = ngay.isoformat()        # chuẩn hoá về NGÀY — `ngay_dong_bang` suy từ đây
    return tho


def _kiem_bang(tho: dict) -> None:
    """`{cot, dong}` của BẢNG công cụ — kiểm SAU `chuan_bi` *(DT3: bản thô cây ATL · Mapping
    Master ⛔ có `cot`; khuôn dựng nó)*. Khuôn ⛔ có `chuan_bi` ⇒ đúng phép kiểm cũ của
    `doc_ban_tho`, cùng lời, cùng chỗ trong chuỗi *(trước mọi thứ đọc giá trị)*."""
    if not isinstance(tho.get("cot"), list) or not isinstance(tho.get("dong"), list):
        raise TuChoi("bản thô thiếu `cot` *(danh sách)* hoặc `dong` *(danh sách hàng)*")


# ── đóng băng ─────────────────────────────────────────────────────────────────

def _soat_rieng_tu(cot: list[str]) -> None:
    """⛔ Từ chối khi BẤT KỲ cột nào của bản thô thuộc `PM_COT_RIENG_TU` *(quyết định ④)*.

    ⚠ Thông điệp in TÊN chuẩn trong bản đen, ⛔ in giá trị ô.
    """
    cam = {_ten(c).casefold(): c for c in PM_COT_RIENG_TU}
    lot = sorted({cam[_ten(c).casefold()] for c in cot if _ten(c).casefold() in cam})
    if lot:
        raise TuChoi(f"bản thô có cột thuộc PM_COT_RIENG_TU: {lot} — cột ấy ⛔ bao giờ vào "
                     "kho nên cũng ⛔ vào ảnh; bỏ cột khỏi lượt đọc rồi đóng băng lại")


def _khoa_hop_le(v: Any, kieu: str = "yyyymm") -> bool:
    """Khoá `yyyymm` hợp lệ = ô SỐ *(chuỗi đúng chữ số)* 6 chữ số, tháng 01–12. Ô chữ
    `{"chu": "202401"}` là khoá HỎNG *(`DT2-R1-02`)*. Khoá `ma` *(DT3)* hợp lệ = ô CHỮ có nội
    dung — ô số, `bool`, rỗng, chỉ-khoảng-trắng đều HỎNG."""
    if kieu == "ma":
        return isinstance(v, dict) and bool(v["chu"].strip())
    return isinstance(v, str) and bool(_YYYYMM.fullmatch(v)) and 1 <= int(v[4:]) <= 12


def _gia_tri_khoa(v: Any, kieu: str) -> str:
    """Giá trị đem ĐẾM TRÙNG: `yyyymm` ⇒ nguyên chuỗi; `ma` ⇒ chữ đã GỘP khoảng trắng."""
    return " ".join(v["chu"].split()) if kieu == "ma" else v


def phan_tich_khoa(khoa: list[Any], kieu: str = "yyyymm") -> dict[str, Any]:
    """Phần CHUNG của khoá → hỏng · trùng. *(Thiếu/lạc: của khuôn — `Khuon.thieu_lac`.)*"""
    hong = [k for k in khoa if not _khoa_hop_le(k, kieu)]
    dem: dict[str, int] = {}
    for k in khoa:
        if _khoa_hop_le(k, kieu):
            g = _gia_tri_khoa(k, kieu)
            dem[g] = dem.get(g, 0) + 1
    return {"khoa_hong": hong, "trung": sorted(k for k, n in dem.items() if n >= 2)}


_META = ("nguon", "doc_luc", "cach_doc")


def _chuan_bi(kh: Khuon, tho: dict) -> tuple[dict, dict[str, list[dict]], str | None]:
    """Gọi `chuan_bi` của khuôn trên BẢN SAO bản thô → (bảng công cụ, bảng phụ, ghi chú) *(DT3)*.

    `ValueError` ⇒ `TuChoi` *(bản thô ⛔ dùng được — in LỜI khuôn; khuôn ⛔ được đưa giá trị ô
    vào lời ấy)*; lỗi khác hay trả sai hình ⇒ `LoiKhuon` *(exit 3)*. `nguon · doc_luc · cach_doc`
    lấy từ BẢN THÔ — khuôn ⛔ đổi được xuất xứ của ảnh; khoá khác của bản thô *(vd
    `canh_bao_rieng_tu`, `ghi_chu` của orchestrator)* ⛔ bao giờ vào ảnh.
    """
    try:
        ra = kh.chuan_bi(copy.deepcopy(tho))
    except ValueError as e:
        raise TuChoi(f"khuôn `{kh.ten}` ⛔ dựng được bảng từ bản thô: {e}") from None
    except Exception as e:
        raise LoiKhuon(f"khuôn `{kh.ten}` nổ khi chuẩn bị bản thô: {type(e).__name__}: {e}") from e
    sai: list[str] = []
    if not isinstance(ra, dict):
        sai.append(f"trả {type(ra).__name__} ⛔ phải dict")
        ra = {}
    if not isinstance(ra.get("cot"), list) or not isinstance(ra.get("dong"), list):
        sai.append("`cot` · `dong` ⛔ phải danh sách")
    phu = ra.get("phu", {})
    if not isinstance(phu, dict) or not all(
            isinstance(h, list) and all(isinstance(r, dict) and "thu_tu" not in r for r in h)
            for h in phu.values()):
        sai.append("`phu` ⛔ phải {tên: [dòng dict ⛔ khoá thu_tu]}")
        phu = {}
    elif set(phu) != set(kh.phu_mong):
        sai.append(f"bảng phụ {sorted(phu)} ≠ PHU_MONG {sorted(kh.phu_mong)}")
    ghi_chu = ra.get("ghi_chu")
    if ghi_chu is not None and not (isinstance(ghi_chu, str) and ghi_chu.strip()):
        sai.append("`ghi_chu` ⛔ phải chuỗi khác rỗng")
    if sai:
        raise LoiKhuon(f"khuôn `{kh.ten}`: chuan_bi phải trả {{cot, dong, phu?, ghi_chu?}} — "
                       + " · ".join(sai))
    return {**{k: tho[k] for k in _META}, "cot": ra["cot"], "dong": ra["dong"]}, phu, ghi_chu


def _thieu_lac(kh: Khuon, dong: list[dict[str, Any]]) -> tuple[list | None, list | None, str,
                                                                    str | None]:
    """Gọi khuôn trên BẢN SAO dòng ảnh *(khuôn ⛔ sửa được ảnh)*.

    `ValueError` ⇒ ⛔ đo được *(trả `None, None`, lý do)*; lỗi khác ⇒ `LoiKhuon` *(exit 3)*.
    """
    try:
        r = kh.thieu_lac(copy.deepcopy(dong))
    except ValueError as e:
        return None, None, "∅", " ".join(str(e).split())
    except Exception as e:
        raise LoiKhuon(f"khuôn `{kh.ten}` nổ khi tính thiếu/lạc: {type(e).__name__}: {e}") from e
    try:
        # ⛔⛔ DT2-R2-03: chuỗi và set cũng LẶP được — `"thieu": "202402"` thành `thiếu: [2, 0, 2,
        #   4, 0, 2]`, `"lac": "202306"` qua `[ĐẠT]` (lạc chỉ ghi nhận), set lặp theo băm ⇒ ảnh
        #   ⛔ tất định. ⇒ thieu/lac phải DANH SÁCH; sai ⇒ TypeError ⇒ LoiKhuon (exit 3) như
        #   mọi sai hình khác của kết quả khuôn.
        for k in ("thieu", "lac"):
            if not isinstance(r[k], (list, tuple)):
                raise TypeError(f"`{k}` là {type(r[k]).__name__} ⛔ phải list/tuple")
        return [str(x) for x in r["thieu"]], [str(x) for x in r["lac"]], str(r["dai"]), None
    except Exception as e:
        raise LoiKhuon(f"khuôn `{kh.ten}`: thieu_lac phải trả {{thieu, lac, dai}} — "
                       f"{type(e).__name__}: {e}") from e


def dong_bang(kh: Khuon, tho: dict, mong: int) -> tuple[dict, list[str]]:
    """Bản thô đã đọc → (ảnh, các dòng báo). ⛔ Ghi gì — `main` ghi.

    ⛔ Mọi `TuChoi` phải nổ ở ĐÂY, trước khi chạm đĩa.
    """
    phu_tho: dict[str, list[dict]] = {}
    ghi_chu: str | None = None
    # Đ4: số HÀNG của bản thô ⛔ phải số dòng bảng khi khuôn có `chuan_bi` (cây ATL: 83 ≠ 74).
    #   Lưới SA ở `values` (DT3-R1-03); bản thô cũ / ix_fx ở `dong`.
    if isinstance(tho.get("values"), list):
        hang_tho = len(tho["values"])
    elif isinstance(tho.get("dong"), list):
        hang_tho = len(tho["dong"])
    else:
        hang_tho = None
    if kh.chuan_bi is not None:
        if isinstance(tho.get("cot"), list):
            _soat_rieng_tu(tho["cot"])               # bản thô có tiêu đề ⇒ soát TRƯỚC khi khuôn đọc
        tho, phu_tho, ghi_chu = _chuan_bi(kh, tho)
    _kiem_bang(tho)
    cot = [_ten(c) for c in tho["cot"]]
    _soat_rieng_tu(tho["cot"])                       # ⛔ trước mọi thứ đọc giá trị
    for hang in phu_tho.values():                    # … và tên cột của mọi bảng phụ (DT3)
        _soat_rieng_tu(sorted({_ten(k) for h in hang for k in h}))

    nhan = [c for c in cot if c]
    trung_ten = sorted({c for c in nhan if nhan.count(c) > 1})
    if trung_ten:
        raise TuChoi(f"tiêu đề có tên trùng {trung_ten} — ánh xạ theo tên sẽ mơ hồ")
    can = [kh.khoa, *kh.cot]
    thieu_cot = [c for c in can if c not in cot]
    if thieu_cot:
        raise TuChoi(f"bản thô thiếu cột khuôn `{kh.ten}` chọn: {thieu_cot} "
                     f"*(tiêu đề đọc được: {cot})*")
    if not tho["dong"]:
        raise TuChoi("bản thô 0 dòng — ⛔ đóng băng một ảnh rỗng (Đ3)")
    vi_tri = {c: cot.index(c) for c in can}
    cot_rong = [j for j, c in enumerate(cot) if not c]

    dong: list[dict[str, Any]] = []
    for i, h in enumerate(tho["dong"], 1):
        if not isinstance(h, list):
            raise TuChoi(f"dòng {i} ⛔ phải danh sách ô")
        if len(h) > len(cot):
            raise TuChoi(f"dòng {i} có {len(h)} ô > {len(cot)} cột tiêu đề — ô ngoài tiêu đề "
                         "sẽ mất im lặng")
        co = [j + 1 for j in cot_rong if j < len(h) and not _rong_tho(h[j])]
        if co:
            # ⛔ in GIÁ TRỊ: cột ⛔ tên là cột ⛔ soát riêng tư được (quyết định ④)
            raise TuChoi(f"dòng {i}: cột tiêu đề rỗng ở vị trí {co} mà ô có giá trị — ô ấy sẽ "
                         "mất im lặng và ⛔ soát riêng tư theo tên được; đặt tên cột hoặc bỏ "
                         "cột khỏi lượt đọc")
        d: dict[str, Any] = {"thu_tu": i}
        for c in can:
            j = vi_tri[c]
            d[c] = _o(h[j]) if j < len(h) else None
        dong.append(d)

    pt = phan_tich_khoa([d[kh.khoa] for d in dong], kh.kieu_khoa)
    thieu, lac, dai, khong_do = _thieu_lac(kh, dong)
    # ⚠ DT3: mỗi phép đếm ô có MẪU SỐ của riêng nó *(Đ4)* — khuôn ⛔ khai `KIEU_COT` thì ba tập
    #   cột trùng `kh.cot` / rỗng như DT2 ⇒ thứ tự, số và lời in giữ từng byte.
    cot_day, cot_so, cot_chu = kh.cot_theo_kieu()
    o_rong = [{"thu_tu": d["thu_tu"], "cot": c}
              for d in dong for c in kh.cot if c in cot_day and _rong(d[c])]
    o_khong_so = [{"thu_tu": d["thu_tu"], "cot": c}
                  for d in dong for c in kh.cot if c in cot_so and _khong_so(d[c])]
    o_khong_chu = [{"thu_tu": d["thu_tu"], "cot": c}
                   for d in dong for c in kh.cot if c in cot_chu and _khong_chu(d[c])]
    mau_rong, mau_so, mau_chu = (len(dong) * len(x) for x in (cot_day, cot_so, cot_chu))
    phu: dict[str, dict[str, Any]] = {}
    for ten in sorted(phu_tho):
        hang = [{"thu_tu": i, **{k: _o(v) for k, v in r.items()}}
                for i, r in enumerate(phu_tho[ten], 1)]
        phu[ten] = {"mong": kh.phu_mong[ten], "so_dong": len(hang), "dong": hang}

    ly_do: list[str] = []
    if len(dong) != mong:
        ly_do.append(f"{len(dong)} dòng ≠ mong {mong}")
    if pt["trung"]:
        ly_do.append(f"trùng {len(pt['trung'])}")
    if thieu:
        ly_do.append(f"thiếu {len(thieu)}")
    if pt["khoa_hong"]:
        ly_do.append(f"khoá hỏng {len(pt['khoa_hong'])}")
    if o_rong:
        ly_do.append(f"ô rỗng {len(o_rong)}/{mau_rong}")
    if o_khong_so:
        ly_do.append(f"ô ⛔ số {len(o_khong_so)}/{mau_so}")
    if o_khong_chu:
        ly_do.append(f"ô ⛔ chữ {len(o_khong_chu)}/{mau_chu}")
    for ten, b in phu.items():
        if b["so_dong"] != b["mong"]:
            ly_do.append(f"phụ `{ten}` {b['so_dong']} dòng ≠ mong {b['mong']}")
    if khong_do is not None:                 # lý do DÀI (lời của khuôn) — đứng cuối
        ly_do.append(f"thiếu/lạc ⛔ đo được — {khong_do}")

    ngay = date.fromisoformat(tho["doc_luc"]).isoformat()
    # ⭐ DT3: dòng bảng phụ VÀO checksum, bọc `{"phu", "dong"}` ⇒ ⛔ lẫn với dòng chính. Khuôn ⛔
    #   có bảng phụ ⇒ `them = ()` ⇒ checksum đúng phép của DT2 *(ảnh `ix_fx` giữ số ghim)*.
    them = tuple({"phu": ten, "dong": r} for ten, b in phu.items() for r in b["dong"])
    checksum = AnhChup(run_id=f"dong_bang_sheet:{kh.ten}", ngay=date.fromisoformat(ngay),
                       nguon=tho["nguon"], dong=tuple(dong) + them).checksum()[:16]
    khong_chon = [c for c in cot if c and c not in can]
    rieng_tu = sorted(PM_COT_RIENG_TU)
    # ⚠ Câu này nằm TRONG ảnh: khi ⛔ có cột tiêu đề rỗng, nó phải giữ ĐÚNG từng chữ của bản
    #   đầu ⇒ ảnh đã commit ⛔ đổi byte nào. Cột tiêu đề rỗng chỉ THÊM một mệnh đề (DT2-R1-08).
    them_rong = (f" {len(cot_rong)} cột tiêu đề rỗng (mọi ô rỗng — đã soát, ⛔ vào ảnh)."
                 if cot_rong else "")
    # ⚠ Như trên: khuôn ⛔ `chuan_bi` ⇒ câu ⛔ đổi chữ nào. Có ⇒ nói THẬT `cot` là của ai (DT3).
    so_ten_phu = sum(len({k for r in b["dong"] for k in r if k != "thu_tu"}) for b in phu.values())
    if kh.chuan_bi is not None:
        them_rong += (f" Bản thô qua `chuan_bi` của khuôn: {len(cot)} tên cột trên là của BẢNG "
                      f"khuôn dựng; soát thêm {so_ten_phu} tên cột của {len(phu)} bảng phụ — 0 "
                      "trùng. Ô bản thô mà khuôn ⛔ mang/băm: xem `ghi_chu_khuon`.")

    anh = {
        "bang": kh.bang,
        "khuon": kh.ten,
        "nguon": tho["nguon"],
        "cach_doc": tho["cach_doc"],
        "ngay_dong_bang": ngay,
        "khong_mang_PII": (
            f"⛔ KHÔNG mang cột riêng tư: máy soát {len(cot)} tên cột của bản thô với "
            f"PM_COT_RIENG_TU {rieng_tu} — 0 trùng (gộp khoảng trắng, ⛔ phân biệt hoa "
            f"thường). Ảnh chỉ giữ khoá `{kh.khoa}` + {len(kh.cot)} cột chọn; "
            f"{len(khong_chon)} cột bản thô ⛔ chọn (tên ở `cot_khong_chon`).{them_rong}"),
        **({"ghi_chu_khuon": ghi_chu} if ghi_chu is not None else {}),
        "khoa": kh.khoa,
        "kieu_khoa": kh.kieu_khoa,
        "cot": list(kh.cot),
        "cot_khong_chon": khong_chon,
        "so_dong": len(dong),
        "trung": pt["trung"],
        "thieu": thieu,
        "lac": lac,
        "khoa_hong": pt["khoa_hong"],
        "o_rong": o_rong,
        "cong": {"mong": mong, "so_dong": len(dong), "dat": not ly_do, "ly_do": ly_do},
        "checksum_noi_dung": checksum,
        "dong": dong,
        **({"phu": phu} if kh.phu_mong else {}),
    }

    def hien(x: Any) -> str:
        return "∅" if x is None else x["chu"] if isinstance(x, dict) else str(x)

    def ds(xs: list) -> str:
        return "[" + ", ".join(hien(x) for x in xs) + "]"

    def vi(os_: list[dict]) -> str:
        return " ".join(f"[dòng {o['thu_tu']} · {o['cot']}]" for o in os_[:10])

    chu_khoa = sum(isinstance(k, dict) for k in pt["khoa_hong"])
    dem_chu = f" · chữ {chu_khoa})" if kh.kieu_khoa == "yyyymm" else ")"
    bao = [
        f"══ dong_bang_sheet · {kh.ten} ({kh.bang})",
        f"  nguồn      : {tho['nguon']}",
        f"  cách đọc   : {tho['cach_doc']}",
        f"  ngày đọc   : {ngay}  (= ngay_dong_bang)",
        # Đ4 — con số phải CỘNG LẠI: N cột tiêu đề = khoá + chọn + ⛔ chọn + tiêu đề rỗng
        (f"  bản thô    : {len(cot)} cột tiêu đề = khoá 1 + chọn {len(kh.cot)} + ⛔ chọn "
         f"{len(khong_chon)} + tiêu đề rỗng {len(cot_rong)} · {len(dong)} dòng"
         if kh.chuan_bi is None else
         f"  bản thô    : {hang_tho} hàng ⇒ chuan_bi dựng bảng {len(cot)} cột = khoá 1 + chọn "
         f"{len(kh.cot)} + ⛔ chọn {len(khong_chon)} · {len(dong)} dòng + bảng phụ "
         f"{sum(b['so_dong'] for b in phu.values())} dòng"),
        f"  soát PII   : {len(cot)}/{len(cot)} tên cột"
        f"{f' + {so_ten_phu} tên cột bảng phụ' if phu else ''} · 0 thuộc PM_COT_RIENG_TU "
        f"{rieng_tu}",
        f"  cột chọn   : khoá {kh.khoa} + {len(kh.cot)} {list(kh.cot)} · "
        f"⛔ chọn {len(khong_chon)} {khong_chon}",
        f"  khoá hỏng: {ds(pt['khoa_hong'])}  ({len(pt['khoa_hong'])}/{len(dong)} dòng"
        f"{dem_chu}",
        f"  ô rỗng: {len(o_rong)}/{mau_rong}  ({len(dong)} dòng × {len(cot_day)} cột"
        f"{' ⛔ được rỗng' if cot_chu else ''}) {vi(o_rong)}".rstrip(),
        f"  ô ⛔ số: {len(o_khong_so)}/{mau_so}  (chữ/bool ở cột {'số' if cot_chu else 'chọn'}) "
        f"{vi(o_khong_so)}".rstrip(),
    ]
    if cot_chu:
        bao.append(f"  ô ⛔ chữ: {len(o_khong_chu)}/{mau_chu}  (số/bool ở cột chữ) "
                   f"{vi(o_khong_chu)}".rstrip())
    bao.append(f"  trùng: {ds(pt['trung'])}")
    if phu:
        bao.append("  bảng phụ: " + " · ".join(f"{ten} {b['so_dong']}/{b['mong']}"
                                               for ten, b in phu.items()))
    if khong_do is None:
        bao += [f"  thiếu: {ds(thieu)}  (dải {dai})",
                f"  lạc: {ds(lac)}  (định nghĩa của khuôn `{kh.ten}` — ghi nhận, ⛔ đỏ)"]
    else:
        bao += [f"  thiếu: ⛔ ĐO ĐƯỢC — {khong_do}",
                "  lạc: ⛔ ĐO ĐƯỢC  (ảnh ghi thieu = lac = null, ⛔ [])"]
    bao.append(f"  checksum_noi_dung: {checksum}")
    return anh, bao


# ── ghi ───────────────────────────────────────────────────────────────────────

def _ghi(p: Path, noi_dung: str) -> None:
    """Ghi NGUYÊN TỬ: tệp tạm cùng thư mục rồi `os.replace` — ⛔ để lại ảnh ghi dở.

    ⭐ Có bài canh trên lỗi I/O THẬT *(`RLIMIT_FSIZE` nhỏ hơn ảnh ⇒ `write` hỏng giữa chừng)*:
    ghi thẳng vào tệp đích sẽ để lại NỬA ảnh thay cho ảnh cũ.
    """
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tam = tempfile.mkstemp(dir=p.parent, prefix=f".{p.name}.", suffix=".tam")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(noi_dung)
        os.chmod(tam, 0o644)
        os.replace(tam, p)
    except BaseException:
        Path(tam).unlink(missing_ok=True)
        raise


def _hien_duong(p: Path) -> Path:
    try:
        return p.resolve().relative_to(GOC.resolve())
    except ValueError:
        return p


class _Lenh(argparse.ArgumentParser):
    """argparse nhưng lỗi đối số ⇒ `TuChoi` *(một dòng, exit 2)* — `S0-R1-03`: mọi đối số ⛔
    khai đều bị từ chối, ⛔ chỉ đối số đầu."""

    def error(self, message: str):        # type: ignore[override]
        raise TuChoi(f"đối số: {message}")


def _lenh() -> _Lenh:
    p = _Lenh(prog="dong_bang_sheet.py",
              description="Đóng băng bản đọc giá trị sheet thành ảnh có checksum + cổng.")
    p.add_argument("khuon", choices=danh_sach_khuon(),
                   help=f"khuôn đóng băng — một tệp ở {THU_MUC_KHUON.name}/")
    p.add_argument("ban_tho", type=Path, help="JSON {nguon, doc_luc, cach_doc, cot, dong}")
    p.add_argument("--mong", type=int, required=True,
                   help="số dòng MONG — khác ⇒ exit 1 (Đ5: cổng phải khai mong)")
    p.add_argument("--ra", type=Path, default=None,
                   help="tệp ảnh ra (mặc định: đường của khuôn, tương đối gốc repo; cổng ĐỎ "
                        "⛔ --ra ⇒ tệp cạnh <ra>.DO.json, ⛔ đè ảnh)")
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        a = _lenh().parse_args(argv)
        if a.mong < 1:
            raise TuChoi(f"--mong {a.mong} — cổng mong 0 dòng là cổng xanh trên tập rỗng (Đ3)")
        kh = nap_khuon(a.khuon)
        anh, bao = dong_bang(kh, doc_ban_tho(a.ban_tho), a.mong)
    except TuChoi as e:
        print("⛔ TỪ CHỐI: " + " ".join(str(e).split()) + " — ⛔ ghi tệp nào", file=sys.stderr)
        return 2
    except LoiKhuon as e:
        if e.__cause__ is not None:        # LỖI do kiểm hình dạng (DT3) ⛔ có traceback
            traceback.print_exception(e.__cause__, file=sys.stderr)
        print("⛔ LỖI: " + " ".join(str(e).split()) + " — ⛔ ghi tệp nào; sửa khuôn",
              file=sys.stderr)
        return 3

    c = anh["cong"]
    mac_dinh = GOC / kh.ra
    ra = a.ra if a.ra is not None else mac_dinh
    ghi_chu = ""
    if a.ra is None and not c["dat"]:
        # ⛔⛔ DT2-R1-01: đường mặc định LÀ ảnh đã commit. Lượt ĐỎ ghi vào đó thì `git status`
        #   thành ` M …/ix_fx.json` và chỉ 1/20 bài bắt (R1 đo). ⇒ ảnh đỏ ra tệp CẠNH.
        ra = mac_dinh.with_name(mac_dinh.stem + ".DO" + mac_dinh.suffix)
        ghi_chu = (f"  (cổng ĐỎ ⛔ --ra ⇒ ⛔ đè {_hien_duong(mac_dinh)}; "
                   "tệp .DO ⛔ commit)")
    try:
        _ghi(ra, json.dumps(anh, ensure_ascii=False, indent=1) + "\n")
    except OSError as e:
        print(f"⛔ LỖI GHI: {type(e).__name__}: " + " ".join(str(e).split())
              + " — ⛔ ảnh mới nào được ghi (ghi nguyên tử; tệp cũ, nếu có, giữ nguyên)",
              file=sys.stderr)
        return 3
    print("\n".join(bao))
    print(f"  ghi        : {_hien_duong(ra)}{ghi_chu}")
    m_rong, m_so, m_chu = (c["so_dong"] * len(x) for x in kh.cot_theo_kieu())
    if c["dat"]:
        # ⚠ khuôn ⛔ cột chữ · ⛔ bảng phụ ⇒ đúng từng chữ dòng ĐẠT của DT2
        them = (f" · ô ⛔ chữ 0/{m_chu}" if kh.cot_theo_kieu()[2] else "") + "".join(
            f" · phụ {ten} {b['so_dong']} = mong" for ten, b in anh.get("phu", {}).items())
        print(f"[ĐẠT] cổng --mong {c['mong']}: {c['so_dong']} dòng = mong · trùng 0 · thiếu 0 · "
              f"khoá hỏng 0 · ô rỗng 0/{m_rong} · ô ⛔ số 0/{m_so}{them}")
        return 0
    print(f"[ĐỎ] cổng --mong {c['mong']}: " + " · ".join(c["ly_do"])
          + " — ảnh đã ghi ĐÚNG NGUỒN, ⛔ sửa; ⛔ dùng ảnh này khi cổng chưa đạt")
    return 1


if __name__ == "__main__":
    sys.exit(main())
