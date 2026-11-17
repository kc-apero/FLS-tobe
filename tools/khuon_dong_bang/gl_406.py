"""Khuôn đóng băng `gl_406` — ĐÁP ÁN 406 · `Report I General Ledger` CALC ZONE (BM–BT).

    python tools/dong_bang_sheet.py gl_406 <bản_thô.json> --mong 7883
        ⇒ tests/fixture/dap_an/gl_406.json

⭐ **Vì sao có khuôn này.** AP v3.1.2 §3.3.1 *(PD 406)* · §3.5.4 *(WP-C2)*: bước **H4** so song
song CA.GL ↔ 406 theo DÒNG × KỲ trên 8 cột `BM…BT` *(`CALC_ZONE_406.md`)*. H4 cần một ẢNH đứng
yên của 406 — đọc MỘT lần, đóng băng có checksum, một cổng khẳng định **số dòng mỗi kỳ** bằng số
dòng sổ cùng kỳ *(nguồn `itl_ledge_adjustment.json`)*, và **bỏ** cột Diễn giải / Số chứng từ.

Hợp đồng bản thô *(orchestrator O7 đọc bằng khoá SA chỉ-đọc, ⛔ commit)* — **LƯỚI đã lắp theo lát
kỳ**, hình `{spreadsheet_id, nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values, hang_cong_thuc}`:
  · `cot` = `("dong_sheet", "A", "D", "R", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT")` —
    cột `A` *(Ngày chứng từ, serial)* · `D` *(Đơn vị tiền tệ)* · `R` *(ITL ID)* · `BM…BT`.
    ⛔⛔ **⛔ cột `B` (Số chứng từ) · `C` (Diễn giải)** — vùng đọc ⛔ phủ `B:C` *(PII, AC-3)*.
  · `values` = các HÀNG DỮ LIỆU *(cột A có ngày)* theo thứ tự sheet, mỗi hàng 12 ô; `dong_sheet`
    = hàng sheet thật *(10…7892)*, dùng để kiểm LIÊN TỤC *(⛔ bỏ sót hàng im lặng — AC-5)*.
  · `hang_cong_thuc` = `{so_dong, dai_hang, cot_A_rong}` — **9.843 hàng công thức thừa** dưới dữ
    liệu *(7893…17735, cột A RỖNG)*: ĐẾM + khai *(bảng phụ `cong_thuc`)*, ⛔ vào bảng chính.

⭐ **Năm quyết định của bước** *(mỗi cái một con số đo 17/11 — Đ4/Đ5)*:

  ① **Khoá = `dong_sheet` (hàng sheet, số nguyên)** *(ISP §3 · `WO-111` ⑯)*. H4 nối dòng 406 ↔
    dòng sổ bằng `dong_sheet` + `itl_id`, ⛔ dựa thứ tự. Giữ NGUYÊN thứ tự dòng *(tồn luỹ kế
    AS-IS phụ thuộc thứ tự — AP §3.3.1)*. Công cụ kiểm khoá trùng/hỏng; khuôn kiểm LIÊN TỤC.

  ② **Mang theo `ky` · `itl_id` · `D`, ⛔ cột nào khác** *(`WO-111` ⑯)*. `ky` = `yyyymm` *(int,
    errata ⑦)* SUY từ cột `A`; `itl_id` = cột `R`; `D` *(tiền tệ)* mang theo để chẩn đoán lệch H4
    *(đo 17/11: 6 hàng THIẾU `D` ⇒ `BO`/`BP` rỗng)*. Cột `A` *(ngày)* ⛔ vào ảnh — chỉ `ky`.

  ③ **`BO` · `BP` = `so?`** *(số HOẶC rỗng)*. `CALC_ZONE_406.md`: `BO`/`BP` = `iferror(INDEX/
    MATCH…)` ⇒ RỖNG khi thiếu (tháng, tiền tệ) ở bảng tỷ giá. Đo 17/11: **6 hàng** *(4962 · 4963
    · 6073 · 6507 · 6949 · 7631)*, mỗi hàng cả `BO` lẫn `BP` rỗng ⇒ **12 ô** *(6 `BO` + 6 `BP`)*.
    `BM·BN·BQ·BR·BS·BT = so` *(strict)* ⇒ ô lỗi `#DIV/0!` *(chuỗi)* trong hàng dữ liệu ⇒ "ô ⛔ số"
    ⇒ ĐỎ *(AC-5: "hàng có ngày mà BM…BT lỗi ⇒ ĐỎ")*. `D = chu?` *(tiền tệ hoặc rỗng)*; `itl_id =
    chu` *(⛔ rỗng — đo 0 rỗng)*.

  ④ **Cổng kỳ = `thieu_lac`** *(Đ5: khai `mong`, NO cả hai chiều)*. So số dòng 406 mỗi kỳ với
    `phan_bo_ky` của `itl_ledge_adjustment.json` *(GỌI nguồn, ⛔ chép số)*. **19 kỳ khớp CHÍNH XÁC**
    *(2024-10…2026-04 = 19 THÁNG)*; **4 kỳ lệch CÓ TÊN** `LECH_CO_TEN` *(bản sao 406 dừng giữa
    2026-05)* ⇒ `lac` *(ghi nhận, ⛔ đỏ)*. Kỳ nào lệch NGOÀI 4 kỳ ấy — thừa, thiếu, hay kỳ lạ —
    ⇒ `thieu` ⇒ ĐỎ. Σ dòng = **7883** = 9967 − (537−239) − 613 − 686 − 487.
    ⚠ `WO-111`/AC-1 ghi *"21 kỳ"* — là MISCOUNT: dải `2024-10…2026-04` có **19** tháng *(Đ4)*;
    bản chất *(4 kỳ lệch tên + số)* ĐÚNG. Khuôn khai **19** *(đo được)*.

  ⑤ **9.843 hàng công thức thừa: ĐẾM + khai, ⛔ vào bảng** *(AC-5)*. Dưới dữ liệu *(cột A rỗng)*
    là hàng chỉ còn công thức *(`BN` = `#DIV/0!`, `BO/BP/BR/BS` rỗng, `BM/BQ/BT` số luỹ kế đông
    cứng)*. `chuan_bi` khai số ấy ở bảng phụ `cong_thuc` *(vào checksum ⇒ sửa tay là ĐỎ)* và đòi
    `cot_A_rong = True` *(cột A của vùng ấy phải RỖNG — bằng chứng chúng ⛔ phải dòng sổ)*.
"""
from __future__ import annotations

import datetime
import json
from pathlib import Path
from typing import Any

BANG = "PD.406"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
#: Thứ tự cột ảnh = khoá + 10 cột mang theo *(② · ③)*. ⛔ thêm cột — `WO-111` ⑯.
COT = ("ky", "itl_id", "D", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT")
#: `itl_id` = mã CHỮ *(⛔ rỗng)* · `D` = tiền tệ *(được rỗng)* · `BO`/`BP` = SỐ hoặc rỗng *(③)*.
#: Cột ⛔ khai *(ky · BM · BN · BQ · BR · BS · BT)* = `so` *(strict)*.
KIEU_COT = {"itl_id": "chu", "D": "chu?", "BO": "so?", "BP": "so?"}
RA = "tests/fixture/dap_an/gl_406.json"
#: Bảng phụ `cong_thuc` giữ TÓM TẮT vùng công thức thừa *(⑤)* — đúng 1 dòng, vào checksum.
PHU_MONG = {"cong_thuc": 1}

#: Cột của LƯỚI bản thô *(hình orchestrator đưa)* — vị trí cố định.
COT_THO = ("dong_sheet", "A", "D", "R", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT")
#: Hàng sheet đầu của DỮ LIỆU *(bản đồ cột ở `CALC_ZONE_406.md`: tiêu đề 7–9, dữ liệu từ 10)*.
DONG_DAU_SHEET = 10
#: Epoch serial của Google Sheets *(1899-12-30)* — suy `ky` từ cột `A`.
EPOCH = datetime.date(1899, 12, 30)

#: ⭐ 4 kỳ LỆCH CÓ TÊN — số dòng 406 MONG *(đo 17/11; Đ5)*: bản sao 406 dừng giữa `2026-05`
#: ⇒ `2026-05` chỉ 239/537, `2026-06`·`2026-07`·`2026-08` VẮNG *(0)*. Lệch nào khác ⇒ ĐỎ.
LECH_CO_TEN: dict[int, int] = {202605: 239, 202606: 0, 202607: 0, 202608: 0}

GOC = Path(__file__).resolve().parents[2]
#: Nguồn `phan_bo_ky` — GỌI *(đọc)*, ⛔ chép số: đổi ảnh sổ thì cổng kỳ đổi theo *(như `ix_fx`
#: gọi `kiem` của C1)*.
NGUON_PHAN_BO = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"


def _ky_tu_serial(serial: int) -> int:
    """Serial ngày *(cột A)* → `yyyymm` *(int)*."""
    d = EPOCH + datetime.timedelta(days=int(serial))
    return d.year * 100 + d.month


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI 406 *(đã lắp theo lát kỳ)* → bảng `{dong_sheet, ky, itl_id, D, BM…BT}` + bảng phụ
    `cong_thuc`. ⛔ lời lỗi mang giá trị ô *(nguồn có thể còn ô lạ)*; `ValueError` ⇒ TỪ CHỐI."""
    cot_tho = tho.get("cot")
    if cot_tho != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(lưới A·D·R·BM:BT, ⛔ phủ B:C)*")
    dau = tho.get("dong_dau_sheet")
    if dau != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET} *(dữ liệu từ hàng 10)*")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng dữ liệu ⛔ rỗng")

    dong: list[list[Any]] = []
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ dong_sheet·A·D·R·BM:BT)*")
        ds, a, d_tt, r = h[0], h[1], h[2], h[3]
        if ds != DONG_DAU_SHEET + i:
            raise ValueError(f"hàng {i + 1}: dong_sheet {ds} ⛔ liên tục *(mong "
                             f"{DONG_DAU_SHEET + i}) — hàng bị bỏ sót hay xáo thứ tự*")
        if not isinstance(a, int) or isinstance(a, bool) or a < 1:
            raise ValueError(f"hàng {i + 1}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        ky = _ky_tu_serial(a)
        # ô rỗng ("" | null) chuẩn hoá về null *(ảnh tất định)*; ô khác giữ nguyên *(ô lỗi là
        #   CHUỖI ⇒ cột `so` sẽ bắt)*. BM…BT = h[4:12].
        o = [None if _rong(x) else x for x in h[4:12]]
        d_tt = None if _rong(d_tt) else d_tt
        r = None if _rong(r) else r
        dong.append([ds, ky, r, d_tt, *o])        # thứ tự = [KHOA, *COT]

    hc = tho.get("hang_cong_thuc")
    if not isinstance(hc, dict) or not (isinstance(hc.get("so_dong"), int)
                                        and not isinstance(hc["so_dong"], bool)
                                        and hc["so_dong"] >= 0) \
            or not (isinstance(hc.get("dai_hang"), str) and hc["dai_hang"].strip()):
        raise ValueError("`hang_cong_thuc` phải {so_dong:int≥0, dai_hang:str, cot_A_rong:bool}")
    if hc.get("cot_A_rong") is not True:
        raise ValueError("`hang_cong_thuc.cot_A_rong` phải True *(vùng công thức thừa có cột A "
                         "RỖNG — bằng chứng ⛔ phải dòng sổ; False ⇒ ⛔ dám bỏ)*")

    thieu_tt = sum(1 for r in dong if r[3] is None)       # hàng thiếu tiền tệ D
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"cong_thuc": [{"so_dong": hc["so_dong"], "dai_hang": hc["dai_hang"]}]},
        "ghi_chu": (
            f"Bảng chính = {len(dong)} hàng dữ liệu 406 *(cột A có ngày)*, khoá dong_sheet "
            f"{DONG_DAU_SHEET}…{DONG_DAU_SHEET + len(dong) - 1} liên tục; ky suy từ cột A "
            f"*(⛔ mang cột A)*, itl_id = cột R, D = tiền tệ. ⛔ mang cột B (Số chứng từ) · C "
            f"(Diễn giải) — vùng đọc ⛔ phủ B:C (AC-3). {thieu_tt} hàng thiếu tiền tệ D ⇒ BO/BP "
            f"rỗng (so?). Vùng công thức thừa: {hc['so_dong']} hàng {hc['dai_hang']} (cột A RỖNG) "
            f"ĐẾM + khai ở bảng phụ `cong_thuc`, ⛔ vào bảng chính (AC-5)."),
    }


def _phan_bo_ledger() -> dict[int, int]:
    """`phan_bo_ky` của `itl_ledge_adjustment.json` → `{yyyymm int: số dòng}`. Thiếu/hỏng ⇒
    `ValueError` ⇒ cổng ĐỎ *(Đ3: ⛔ đo được là ĐỎ)*."""
    try:
        j = json.loads(NGUON_PHAN_BO.read_text(encoding="utf-8"))
        pb = j["phan_bo_ky"]
        if not isinstance(pb, dict) or not pb:
            raise ValueError("rỗng")
        ra: dict[int, int] = {}
        for k, v in pb.items():
            nam, thang = k.split("-")
            ra[int(nam) * 100 + int(thang)] = int(v)
        return ra
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise ValueError(f"⛔ đọc được phan_bo_ky từ {NGUON_PHAN_BO.name}: "
                         f"{type(e).__name__}: {e}") from None


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng KỲ *(④)*: số dòng 406 mỗi kỳ ↔ `phan_bo_ky` *(có `LECH_CO_TEN`)*.

    `thieu` = kỳ lệch NGOÀI 4 kỳ có tên *(thừa · thiếu · kỳ lạ — ĐỎ)*; `lac` = 4 kỳ lệch có tên
    *(ghi nhận, ⛔ đỏ)*. Khớp hết ⇒ `thieu = []`. Nguồn hỏng ⇒ `ValueError` *(⛔ đo được = ĐỎ)*.
    """
    ledger = _phan_bo_ledger()                            # ValueError ⇒ ⛔ đo được
    thuc: dict[int, int] = {}
    for d in dong:
        k = int(d["ky"])                                  # ky là ô số (chuỗi chữ số)
        thuc[k] = thuc.get(k, 0) + 1
    mong_406 = {k: LECH_CO_TEN.get(k, v) for k, v in ledger.items()}
    thieu = sorted(set(thuc) | set(mong_406))
    thieu = [str(k) for k in thieu if thuc.get(k, 0) != mong_406.get(k)]
    lac = [str(k) for k in sorted(LECH_CO_TEN)]
    khop = sum(1 for k, v in mong_406.items() if thuc.get(k, 0) == v and k not in LECH_CO_TEN)
    return {
        "thieu": thieu,
        "lac": lac,
        "dai": (f"{khop} kỳ khớp phan_bo_ky CHÍNH XÁC · {len(LECH_CO_TEN)} kỳ lệch có tên "
                f"(bản sao 406 dừng giữa 2026-05) · nguồn {NGUON_PHAN_BO.name}"),
    }
