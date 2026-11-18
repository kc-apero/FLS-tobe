"""Khuôn đóng băng `gi_mid3` — ĐÁP ÁN MID3 của GI *(`CFA2 | MID 3 | GI Platform Data Ledger`,
PD 507)* + cổng `Σ chia = O / P` *(ISP 3.1.2 · DT8 · `WO-147` AC-2 · DT8-B2)*.

    python tools/dong_bang_sheet.py gi_mid3 <bản_thô.json> --mong 253
        ⇒ tests/fixture/dap_an/gi_mid3.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.4.1 PD 505–507 · §3.5.4 WP-C4. MID3 là ĐÁP ÁN phân bổ
nền tảng GI: mỗi **Vendor-tháng** *(ở GI gộp về TỔNG tháng)* chia `PE Amount (O)` và `PM Amount
(P)` xuống **6 CDT1** theo `RATE = PE_cdt / Σ PE 6 CDT1` ⇒ `PE_cdt = RATE × O`, `PM_cdt = RATE ×
P`. Cổng của sheet *(cột `CHECK ALLOCATE` AE/AF = True)* khẳng định **`Σ chia = O / P`**; H9/H10
*(AL.PLT · KS.AL)* phải khớp TỪNG Ô MID3. Ảnh đóng băng **253 hàng số** *(11 tổng-tháng + 242
chi tiết — vòng sửa `DT8-R1-03`)*, và cổng `thieu_lac` TÁI dựng `Σ chia = O / P` ĐỘC LẬP trên
đủ 253 *(⛔ tin cột AE/AF của nguồn)*.

Hợp đồng bản thô *(phiên cloud DATA đọc bằng khoá SA chỉ-đọc, ⛔ commit)* — **LƯỚI SA vùng
`O:AF`** *(⛔ phủ `A:N` = Số chứng từ · Diễn giải · Tài khoản · … PII)*, hình `{spreadsheet_id,
nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("O","P","S","T","U","V","W","X","Y","Z","AA","AB","AC","AD","AE","AF")` — `O` PE
    Amount · `P` PM Amount · 6 cặp CDT1 *(`S/T` CVL · `U/V` COR · `W/X` SHQ1 · `Y/Z` CSM · `AA/AB`
    CAH · `AC/AD` ASA — mỗi cặp PE/PM)* · `AE/AF` = `CHECK ALLOCATE` PE/PM *(True trên hàng đáp án)*.
  · `values` = hàng dữ liệu sheet *(10…)*; `dong_dau_sheet` = **10**.

⭐ **Hai quyết định của bước** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **Chọn hàng SỐ: `O` là số** *(⛔ theo `AE ∧ AF = True`, ⛔ theo nhãn cột A — cột A là 'Số chứng
    từ', ⛔ đọc)* — `DT8-R1-03`. Đo 18/11 vùng `O10:AF273` *(264 hàng)*: **253** hàng `O` là số =
    **11** tổng-tháng *(sheet 10–20, mang `CHECK ALLOCATE` AE=AF=True)* + **242** chi tiết *(22
    hàng/tháng × 11, sheet 22+; AE/AF ⛔ có)*; **11** hàng NGĂN *(sheet 21, 44, …, 251 — `O` ⛔ số)*
    ⛔ vào ảnh. Mọi ô 14 cột số của 253 hàng đều là số *(0 rỗng)*. Khoá = `dong_sheet` *(⛔ cần
    tháng ⇒ ⛔ chạm cột PII)*. 253 hàng ⇒ `--mong 253`. *(Bản đầu chọn 11/253 = 4,3 % hàng số.)*

  ② **Cổng `Σ chia = O / P` = `thieu_lac`** *(Đ5 · Đ3)*. Mỗi hàng: `|O − Σ 6 PE_cdt| ≤ TOL` ∧
    `|P − Σ 6 PM_cdt| ≤ TOL`, `TOL = 1e-6` *(đo 18/11 trên 253 hàng: dư lớn nhất Decimal `5,085e-9`
    PE · `0` PM — làm tròn của sheet)*. **MONG lệch = 0**; một hàng lệch *(engine/nguồn chia sai)* ⇒ `thieu` ⇒
    ĐỎ. Tập rỗng *(0 hàng chọn)* ⇒ `ValueError` ⇒ ĐỎ *(Đ3: mẫu số 0 là kết quả, ⛔ nền xanh)*.

  ③ **Cổng KHAI mẫu số từng vế** *(`DT8-R1-02` · Đ3)*. Đo 18/11: vế **PE** `O` + 6 `PE_cdt` có
    **1.275/1.771** ô ≠ 0 *(253 × 7)*; vế **PM** `P` + 6 `PM_cdt` có **0/1.771** ô ≠ 0 ⇒ `lệch 0`
    ở vế PM là `0 = 0` trên tập rỗng. `thieu_lac` in `PE: n/N ô ≠ 0` · `PM: n/N ô ≠ 0` cạnh kết
    quả, và khi n = 0 nói thẳng *"vế này chưa đo được trên dữ liệu thật"*. Vế PM được chứng minh
    ĐỎ bằng bài TỔNG HỢP có PM ≠ 0 *(`test_DT8_R1_02_*`: bỏ vế PM khỏi cổng ⇒ bài ĐỎ)*.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from typing import Any

BANG = "PD.507"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
#: Thứ tự cột ảnh = khoá `dong_sheet` + `pe` `pm` + 6 cặp CDT1 PE/PM *(①)*. Mọi cột = `so` strict
#: *(11 hàng đáp án: đo 0 ô rỗng, 0 ô ⛔ số)* — ô lỗi ở hàng đáp án ⇒ ĐỎ.
COT = ("pe", "pm",
       "cvl_pe", "cvl_pm", "cor_pe", "cor_pm", "shq1_pe", "shq1_pm",
       "csm_pe", "csm_pm", "cah_pe", "cah_pm", "asa_pe", "asa_pm")
RA = "tests/fixture/dap_an/gi_mid3.json"

#: Cột LƯỚI bản thô *(vùng O:AF)* — vị trí cố định.
COT_THO = ("O", "P", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF")
DONG_DAU_SHEET = 10
#: Chỉ số *(trong COT_THO)* của 6 PE_cdt và 6 PM_cdt — cặp `S/T U/V W/X Y/Z AA/AB AC/AD`.
I_PE = (2, 4, 6, 8, 10, 12)
I_PM = (3, 5, 7, 9, 11, 13)
I_O, I_P, I_AE, I_AF = 0, 1, 14, 15
#: Dung sai cổng `Σ chia = O / P` *(②)*.
TOL = Decimal("0.000001")


def _la_so(v: Any) -> bool:
    """Ô thô là SỐ JSON *(int/Decimal — ⛔ bool, ⛔ chuỗi, ⛔ rỗng)*."""
    return isinstance(v, (int, Decimal)) and not isinstance(v, bool)


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI `O:AF` → bảng 253 hàng số `{dong_sheet, pe, pm, <6×(pe,pm)>}` *(①)*.
    Chọn hàng có `O` là SỐ *(⛔ `AE/AF`)*. ⛔ lời lỗi mang giá trị ô; `ValueError` ⇒ TỪ CHỐI."""
    cot_tho = tho.get("cot")
    if cot_tho != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(vùng O:AF, ⛔ phủ A:N = PII)*")
    dau = tho.get("dong_dau_sheet")
    if dau != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng MID3 ⛔ rỗng")

    dong: list[list[Any]] = []
    so_check = 0                                         # hàng số có CHECK ALLOCATE True ∧ True
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ O:AF)*")
        if _la_so(h[I_O]):                               # hàng SỐ (⛔ hàng ngăn, ⛔ theo AE/AF)
            if h[I_AE] is True and h[I_AF] is True:
                so_check += 1
            ds = DONG_DAU_SHEET + i
            cols = [ds, h[I_O], h[I_P]]
            for j in range(2, 14):                       # S..AD theo thứ tự COT_THO
                cols.append(h[j])
            dong.append(cols)

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "ghi_chu": (
            f"{len(dong)} hàng số MID3 *(chọn theo `O` là số — ⛔ theo AE/AF, ⛔ đọc cột A 'Số chứng "
            f"từ'; {so_check}/{len(dong)} hàng mang CHECK ALLOCATE True = tổng-tháng, còn lại chi "
            f"tiết; {len(values) - len(dong)} hàng ngăn ⛔ chọn)*, khoá dong_sheet. Mỗi hàng = PE Amount (O) · PM Amount (P) · "
            f"6 cặp CDT1 PE/PM *(CVL·COR·SHQ1·CSM·CAH·ASA)*. Cổng Σ chia = O/P *(TOL {TOL})* ở "
            f"`thieu_lac`. ⛔ mang cột A:N *(Số CT · Diễn giải · Tài khoản · … PII)*."),
    }


def _dec(v: Any) -> Decimal:
    """Ô ảnh *(chuỗi chữ số)* → Decimal. Ô ⛔ số ⇒ `ValueError` *(⛔ đo được ⇒ ĐỎ)*."""
    if isinstance(v, str):
        try:
            return Decimal(v)
        except InvalidOperation:
            pass
    raise ValueError(f"ô cột đáp án ⛔ phải số")


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng `Σ chia = O / P` *(②)*: mỗi hàng, Σ 6 PE_cdt = `pe` ∧ Σ 6 PM_cdt = `pm` *(±TOL)*.

    `thieu` = `dong_sheet` của hàng LỆCH *(MONG lệch = 0 — Đ5)*; khớp hết ⇒ `thieu = []`. Tập
    rỗng ⇒ `ValueError` *(Đ3: 0 hàng là kết quả, ⛔ nền xanh)*. `lac` = [] *(⛔ lệch có tên)*.
    `dai` KHAI mẫu số từng vế *(③ — `DT8-R1-02`)*: số ô ≠ 0 của vế PE và vế PM.
    """
    if not dong:
        raise ValueError("0 hàng đáp án *(AE/AF ⛔ True ở hàng nào)* — mẫu số 0, ⛔ nền xanh (Đ3)")
    cot_pe = ("cvl_pe", "cor_pe", "shq1_pe", "csm_pe", "cah_pe", "asa_pe")
    cot_pm = ("cvl_pm", "cor_pm", "shq1_pm", "csm_pm", "cah_pm", "asa_pm")
    lech: list[str] = []
    du_max = Decimal(0)
    # Đ3 *(③)*: đếm ô ≠ 0 của TỪNG vế — `lệch 0` ở vế 0 ô ≠ 0 là `0 = 0` trên tập rỗng.
    cot_ve_pe = ("pe", *cot_pe)
    cot_ve_pm = ("pm", *cot_pm)
    khac0_pe = sum(1 for d in dong for c in cot_ve_pe if _dec(d[c]) != 0)
    khac0_pm = sum(1 for d in dong for c in cot_ve_pm if _dec(d[c]) != 0)
    mau_ve = len(dong) * len(cot_ve_pe)
    for d in dong:
        o = _dec(d["pe"]); p = _dec(d["pm"])
        spe = sum((_dec(d[c]) for c in cot_pe), Decimal(0))
        spm = sum((_dec(d[c]) for c in cot_pm), Decimal(0))
        du = max(abs(o - spe), abs(p - spm))
        du_max = max(du_max, du)
        if abs(o - spe) > TOL or abs(p - spm) > TOL:
            ds = d["dong_sheet"]
            lech.append(f"dong_sheet@{ds}")
    return {
        "thieu": lech,
        "lac": [],
        "dai": (f"Σ chia = O/P trên {len(dong)} hàng số · lệch {len(lech)} *(mong 0)* · "
                f"dư lớn nhất {du_max} *(TOL {TOL})* · mẫu số từng vế — "
                f"PE: {khac0_pe}/{mau_ve} ô ≠ 0"
                + (" — vế này chưa đo được trên dữ liệu thật" if khac0_pe == 0 else "")
                + f" · PM: {khac0_pm}/{mau_ve} ô ≠ 0"
                + (" — vế này chưa đo được trên dữ liệu thật" if khac0_pm == 0 else "")),
    }
