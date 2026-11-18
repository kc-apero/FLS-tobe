"""Khuôn đóng băng `gl_406_dau_vao` — ĐẦU VÀO THÔ của 406 · `Report I General Ledger`.

    python tools/dong_bang_sheet.py gl_406_dau_vao <bản_thô.json> --mong 7883
        ⇒ tests/fixture/dap_an/gl_406_dau_vao.json

⭐ **Vì sao có khuôn này** *(ISP 3.1.2 · Step 13 · H4 — quyết định orchestrator B′, 18/11)*.
Bước **H4** *(AP v3.1.2 §3.5.4 WP-C2)* so CA.GL ↔ đáp án 406 trên 8 cột `BM…BT`. Để *"chạy H1
trên dòng sổ"* cần **tiền NGUYÊN TỆ** `E` *(PS Nợ)* · `F` *(PS Có)* — ĐẦU VÀO thô mà công thức
`AX…BT` của sheet dùng *(`CALC_ZONE_406.md`)*. Ảnh đáp án `gl_406.json` *(DT4)* CHỈ giữ `BM…BT`
*(đầu RA)* + `BO`/`BP` *(Nợ/Có ĐÃ quy bVND)* — ⛔ mang `E`/`F`. Đo 18/11 *(Đ1, grep `ps_no|ps_co`
ở `fls/` + `tools/` + `tests/fixture/`)*: repo ⛔ có ẢNH nào mang `E`/`F` nguyên tệ — O10 của ISP
*(§2)* ghi cột PS Nợ/Có · TK · tiền tệ ĐÃ bị bỏ khỏi ảnh. ⇒ Tái dựng Nợ/Có từ `BO`/`BP` của chính
đáp án là **VÒNG TRÒN** *(orchestrator bác phương án A)*; nguồn ĐỘC LẬP = đọc thẳng cột đầu vào
`E`/`F` của sheet bằng khoá SA chỉ-đọc, đóng băng ở đây. Nhờ vậy `BO`/`BP` ở H4 là **phép kiểm
THẬT**, ⛔ tự khớp.

⭐ **Kiểm chéo với `gl_406.json`** *(H4 làm, ⛔ ở khuôn này)*: `dong_sheet` · `itl_id` · `D` của
ảnh đầu vào phải TRÙNG đáp án *(0 lệch)* — hai ảnh đọc hai lượt, hai vùng cột khác nhau, cùng khoá
hàng; lệch ⇒ một trong hai sai.

Hợp đồng bản thô *(orchestrator đọc bằng khoá SA chỉ-đọc — `sa_lay.py`, 3 lượt `A10:A` · `D10:F`
· `R10:R`; ⛔ commit bản thô — chỉ ở /tmp)* — **LƯỚI** hình `{spreadsheet_id, nguon, doc_luc,
cach_doc, dong_dau_sheet, cot, values}`:
  · `cot` = `("dong_sheet", "A", "D", "E", "F", "R")` — cột `A` *(Ngày chứng từ, serial)* · `D`
    *(Đơn vị tiền tệ)* · `E` *(PS Nợ, nguyên tệ)* · `F` *(PS Có, nguyên tệ)* · `R` *(ITL ID)*.
    ⛔⛔ **⛔ cột `B` (Số chứng từ) · `C` (Diễn giải)** — vùng đọc ⛔ phủ `B:C` *(PII, AC-3)*.
  · `values` = các HÀNG DỮ LIỆU *(cột A có ngày)* theo thứ tự sheet, mỗi hàng 6 ô; `dong_sheet`
    = hàng sheet thật *(10…7892)*, dùng để kiểm LIÊN TỤC *(⛔ bỏ sót hàng im lặng)*.

⭐ **Khác `gl_406` ở ĐÚNG một chỗ:** khuôn này ⛔ có `hang_cong_thuc`. Vùng dưới dữ liệu
*(7893+)* ở các cột đầu vào `A·D·E·F·R` là **RỖNG** *(đo 18/11: `A7893:A7896` trả 0 hàng)* —
⛔ có *"công thức thừa"* như cột `BM…BT`; bước này chỉ đọc đúng 7883 hàng dữ liệu, cổng `--mong
7883` canh số hàng.

⭐ **Năm quyết định** *(mỗi cái một con số đo 18/11 — Đ4/Đ5)*:

  ① **Khoá = `dong_sheet` (hàng sheet, số nguyên)**. H4 nối ảnh đầu vào ↔ đáp án bằng `dong_sheet`
    *(+ `itl_id` kiểm chéo)*. Giữ NGUYÊN thứ tự dòng *(tồn luỹ kế AS-IS phụ thuộc thứ tự — AP
    §3.3.1)*. Khuôn kiểm LIÊN TỤC `10…7892`.

  ② **Mang theo `ky` · `itl_id` · `D` · `E` · `F`, ⛔ cột nào khác.** `ky` = `yyyymm` *(int)* SUY từ
    cột `A`; `itl_id` = cột `R`; `D` *(tiền tệ)* để kiểm chéo + chẩn đoán; `E`/`F` = tiền NGUYÊN TỆ
    cho H1. Cột `A` *(ngày)* ⛔ vào ảnh — chỉ `ky`.

  ③ **`E` · `F` = `so?`** *(số HOẶC rỗng)*. Một dòng sổ ghi Nợ HOẶC Có ⇒ cột kia rỗng *(đo 18/11:
    2983 hàng có cả hai; còn lại một bên)*; ô ⛔ rỗng mà ⛔ số *(chuỗi lỗi)* ⇒ "ô ⛔ số" ⇒ ĐỎ *(đo
    18/11: 0 ô E/F là chuỗi khác rỗng)*. `D = chu?` *(tiền tệ hoặc rỗng — đo 18/11: 6 hàng thiếu
    `D`: `dong_sheet` 4962·4963·6073·6507·6949·7631)*; `itl_id = chu` *(⛔ rỗng — đo 0 rỗng)*.

  ④ **Cổng kỳ = `thieu_lac`** *(Đ5: khai `mong`, NO cả hai chiều)* — Y HỆT `gl_406`: so số hàng mỗi
    kỳ với `phan_bo_ky` của `itl_ledge_adjustment.json` *(GỌI nguồn, ⛔ chép số)*. **19 kỳ khớp
    CHÍNH XÁC** *(2024-10…2026-04)*; **4 kỳ lệch CÓ TÊN** `LECH_CO_TEN` *(bản sao 406 dừng giữa
    2026-05: 2026-05 chỉ 239/537, 2026-06·07·08 vắng)* ⇒ `lac`. Kỳ khác ⇒ `thieu` ⇒ ĐỎ.
    `D` CÓ chữ mà ⛔ thuộc 5 tiền tệ ⇒ `thieu` *(quét PII GIÁ TRỊ — Diễn giải/Số CT lạc sang `D`)*.

  ⑤ **Bảng phụ `itl_id_lech`** *(mong 4)*: `itl_id` *(cột R)* CÓ chữ mà ⛔ khớp `^ITL#\\d+$` ⇒ LỆCH
    CÓ TÊN *(đo 18/11: 4 hàng `#N/A ()` — `dong_sheet` 6684·6836·7500·7832; H4 ⛔ nối được bằng
    `itl_id`, nối bằng `dong_sheet`)*. Khác 4 ⇒ cổng bảng phụ ĐỎ. ⛔ sửa giá trị nguồn — khai y
    nguyên để H4 thấy 4 dòng ấy.
"""
from __future__ import annotations

import datetime
import json
import re
from pathlib import Path
from typing import Any

BANG = "PD.406.DauVao"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
#: Thứ tự cột ảnh = khoá + 5 cột mang theo *(②)*. ⛔ thêm cột.
COT = ("ky", "itl_id", "D", "E", "F")
#: `itl_id` = mã CHỮ *(⛔ rỗng)* · `D` = tiền tệ *(được rỗng)* · `E`/`F` = SỐ hoặc rỗng *(③)*.
#: Cột ⛔ khai *(ky)* = `so` *(strict)*.
KIEU_COT = {"itl_id": "chu", "D": "chu?", "E": "so?", "F": "so?"}
RA = "tests/fixture/dap_an/gl_406_dau_vao.json"
#: Bảng phụ: `itl_id_lech` *(⑤)* + `so_du_dau` *(⑥)* — cả hai vào checksum.
#: `itl_id_lech` mong = **4**; `so_du_dau` mong = **5** *(đo 18/11)*; khác ⇒ cổng phụ ĐỎ.
PHU_MONG = {"itl_id_lech": 4, "so_du_dau": 5}

#: ⑥ SỐ DƯ ĐẦU KỲ GÕ TAY — 5 ô ở HÀNG 24 *(ds24)* lệch khuôn CALC_ZONE *(R-chẩn orchestrator
#: 18/11: quét công thức `AX10:BT7892` = 181.263 ô, ĐÚNG 5 ô lệch, cả 5 ở hàng 24)*. Đây là lý do
#: cột LŨY KẾ `BM·BN·BQ·BT` của đáp án chênh ~56.84e9 bVND · ~2.2677 mUSD so với H1 thuần từ ds24
#: *(đo độc lập 18/11 trước khi biết công thức)*. FLS CHƯA có khái niệm số dư đầu kỳ — nguồn chính
#: thức là câu hỏi cho BA/owner *(errata ⑳)*. H4 GIEO 5 hằng này vào engine qua `so_du_dau` TƯỜNG
#: MINH *(⛔ sửa `tinh_gl` ngầm)*. Khuôn CHỈ đóng băng công thức verbatim + hằng trích; ⛔ đọc công
#: thức ô NÀO KHÁC vào ảnh. `vao` ∈ {`ton` (+ `tien_te`), `bvnd_ton`, `musd_ton`}.
SO_DU_DAU_MAU_SO = 181263       # mẫu số R-chẩn (orchestrator) — 5 ô lệch / 181.263 ô quét
VAO_BIET = ("ton", "bvnd_ton", "musd_ton")

#: ⑤ `itl_id` *(cột R)* PHẢI khớp `^ITL#\d+$`. 4 hàng mang chuỗi LỖI Sheets `#N/A ()`.
ITL_ID_RE = re.compile(r"ITL#\d+")
#: ⑤ *(H4-R1-04)* Cột R MỞ *(công thức trả `ITL#n` HOẶC chuỗi lỗi Sheets)*; giá trị ⛔ khớp
#: `ITL#\d+` phải là lỗi Sheets `#…` *(TẬP ĐÓNG)*, ⛔ chuỗi tự do — nếu không, PII *(Diễn giải/tên)*
#: lạc sang R lọt vào ảnh mà vẫn đủ 4 hàng *(đo 18/11: 4 giá trị hiện tại đều `#N/A ()`)*.
ITL_LOI_RE = re.compile(r"#[A-Z/0-9!?]+( \(\))?")
#: 4 `dong_sheet` itl_id lệch CÓ TÊN *(đo 18/11; để bài ghim — khác tập ⇒ checksum đổi)*.
LECH_ITL_ID = (6684, 6836, 7500, 7832)
#: ③/④ `D` *(Đơn vị tiền tệ)* có TẬP ĐÓNG = 5 tiền tệ của AP *(đo 18/11: VND·USD·SGD·HKD + 6 rỗng;
#: ⛔ COP trong lát 406 này)*. Giá trị KHÁC *(⛔ rỗng)* ⇒ `thieu_lac` báo ⇒ ĐỎ *(quét PII giá trị)*.
TIEN_TE = ("USD", "SGD", "COP", "VND", "HKD")

#: Cột của LƯỚI bản thô *(hình orchestrator đưa qua `sa_lay.py`)* — vị trí cố định.
COT_THO = ("dong_sheet", "A", "D", "E", "F", "R")
#: Hàng sheet đầu của DỮ LIỆU *(bản đồ cột ở `CALC_ZONE_406.md`: tiêu đề 7–9, dữ liệu từ 10)*.
DONG_DAU_SHEET = 10
#: Epoch serial của Google Sheets *(1899-12-30)* — suy `ky` từ cột `A`.
EPOCH = datetime.date(1899, 12, 30)

#: ④ 4 kỳ LỆCH CÓ TÊN — số hàng MONG *(đo 18/11; Đ5)*: bản sao 406 dừng giữa `2026-05`
#: ⇒ `2026-05` chỉ 239/537, `2026-06`·`2026-07`·`2026-08` VẮNG *(0)*. Lệch nào khác ⇒ ĐỎ.
LECH_CO_TEN: dict[int, int] = {202605: 239, 202606: 0, 202607: 0, 202608: 0}

GOC = Path(__file__).resolve().parents[2]
#: Nguồn `phan_bo_ky` — GỌI *(đọc)*, ⛔ chép số.
NGUON_PHAN_BO = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"


def _ky_tu_serial(serial: int) -> int:
    """Serial ngày *(cột A)* → `yyyymm` *(int)*."""
    d = EPOCH + datetime.timedelta(days=int(serial))
    return d.year * 100 + d.month


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def _doc_so_du_dau(raw: Any) -> list[dict[str, Any]]:
    """Kiểm + dựng bảng phụ `so_du_dau` *(⑥)* từ `tho["so_du_dau"]`. `ValueError` ⇒ TỪ CHỐI.

    Mỗi ô: `{o, ds, cong_thuc, vao, tien_te, hang_so}`. `cong_thuc` = verbatim SA FORMULA;
    `hang_so` = HẰNG đã trích *(bài DT ghim lại cả hai)*. ⛔ IN giá trị lạ vào lời lỗi dài.
    """
    if not isinstance(raw, list) or not raw:
        raise ValueError("`so_du_dau` phải danh sách ô số dư đầu kỳ ⛔ rỗng "
                         "*(5 ô gõ tay hàng 24 — đọc FORMULA)*")
    ra: list[dict[str, Any]] = []
    for i, o in enumerate(raw, 1):
        if not isinstance(o, dict):
            raise ValueError(f"so_du_dau[{i}] ⛔ phải một đối tượng")
        thieu = [k for k in ("o", "ds", "cong_thuc", "vao", "tien_te", "hang_so") if k not in o]
        if thieu:
            raise ValueError(f"so_du_dau[{i}] thiếu khoá {thieu}")
        if o["ds"] != DONG_DAU_SHEET + 14:        # cả 5 ô ở HÀNG 24 (ds24)
            raise ValueError(f"so_du_dau[{i}] ds={o['ds']} ⛔ phải 24 *(số dư đầu kỳ gõ ở hàng 24)*")
        if o["vao"] not in VAO_BIET:
            raise ValueError(f"so_du_dau[{i}] vao={o['vao']!r} ⛔ thuộc {list(VAO_BIET)}")
        if o["vao"] == "ton" and o["tien_te"] not in TIEN_TE:
            raise ValueError(f"so_du_dau[{i}] vao=ton cần tien_te thuộc {list(TIEN_TE)}")
        # giữ NGUYÊN thứ tự nguồn; framework thêm `thu_tu` + bọc kiểu ô.
        ra.append({"o": o["o"], "ds": o["ds"], "cong_thuc": o["cong_thuc"],
                   "vao": o["vao"], "tien_te": o["tien_te"], "hang_so": o["hang_so"]})
    return ra


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """LƯỚI đầu vào 406 → bảng `{dong_sheet, ky, itl_id, D, E, F}` + bảng phụ `itl_id_lech`.
    ⛔ lời lỗi mang giá trị ô *(nguồn có thể còn ô lạ)*; `ValueError` ⇒ TỪ CHỐI."""
    cot_tho = tho.get("cot")
    if cot_tho != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(lưới A·D·E·F·R, ⛔ phủ B:C)*")
    dau = tho.get("dong_dau_sheet")
    if dau != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET} *(dữ liệu từ hàng 10)*")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng dữ liệu ⛔ rỗng")

    dong: list[list[Any]] = []
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô *(đủ dong_sheet·A·D·E·F·R)*")
        ds, a, d_tt, e, f, r = h
        if ds != DONG_DAU_SHEET + i:
            raise ValueError(f"hàng {i + 1}: dong_sheet {ds} ⛔ liên tục *(mong "
                             f"{DONG_DAU_SHEET + i}) — hàng bị bỏ sót hay xáo thứ tự*")
        if not isinstance(a, int) or isinstance(a, bool) or a < 1:
            raise ValueError(f"hàng {i + 1}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        ky = _ky_tu_serial(a)
        # ô rỗng ("" | null) chuẩn hoá về null; ô khác giữ nguyên *(ô lỗi là CHUỖI ⇒ cột `so?`
        #   sẽ bắt)*. Thứ tự trả = [KHOA, *COT] = [dong_sheet, ky, itl_id, D, E, F].
        d_tt = None if _rong(d_tt) else d_tt
        # ③/④ D = TẬP ĐÓNG tiền tệ *(H4-R1-04)*: đuôi/đầu trắng *(`"USD "`)* ⇒ TỪ CHỐI — ⛔ chuẩn
        #   hoá ngầm để `thieu_lac` strip() thấy khớp mà ảnh giữ chuỗi bẩn. ⛔ IN giá trị *(PII)*.
        if isinstance(d_tt, str) and d_tt != d_tt.strip():
            raise ValueError(f"hàng {i + 1}: cột D có khoảng trắng đuôi/đầu ⇒ ⛔ thuộc tập đóng "
                             f"tiền tệ *(chuẩn hoá nguồn; H4-R1-04)*")
        r = None if _rong(r) else r
        e = None if _rong(e) else e
        f = None if _rong(f) else f
        dong.append([ds, ky, r, d_tt, e, f])

    # ⑤ hàng itl_id CÓ chữ mà ⛔ khớp `^ITL#\d+$` ⇒ LỆCH CÓ TÊN *(bảng phụ)*. itl_id RỖNG ⇒ cột
    #   `chu` bắt *(⛔ vào đây)*. ⛔ sửa giá trị nguồn — khai y nguyên để H4 thấy 4 dòng ấy.
    itl_lech = sorted(
        ({"dong_sheet": d[0], "itl_id_tho": d[2]}
         for d in dong if isinstance(d[2], str) and not ITL_ID_RE.fullmatch(d[2])),
        key=lambda x: x["dong_sheet"])
    # ⑤ *(H4-R1-04)* TẬP ĐÓNG: mỗi itl_id lệch phải là LỖI Sheets `#…`, ⛔ chuỗi tự do *(PII lọt)*.
    #   ⛔ IN giá trị vào lời lỗi — chỉ `dong_sheet`.
    for x in itl_lech:
        if not ITL_LOI_RE.fullmatch(x["itl_id_tho"]):
            raise ValueError(f"itl_id_lech ds={x['dong_sheet']}: cột R ⛔ phải lỗi Sheets `#…` "
                             f"*(chuỗi tự do ⇒ PII lọt — H4-R1-04)*")

    so_du_dau = _doc_so_du_dau(tho.get("so_du_dau"))

    thieu_tt = sum(1 for r in dong if r[3] is None)       # hàng thiếu tiền tệ D
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"itl_id_lech": itl_lech, "so_du_dau": so_du_dau},
        "ghi_chu": (
            f"ĐẦU VÀO thô 406 = {len(dong)} hàng dữ liệu *(cột A có ngày)*, khoá dong_sheet "
            f"{DONG_DAU_SHEET}…{DONG_DAU_SHEET + len(dong) - 1} liên tục; ky suy từ cột A "
            f"*(⛔ mang cột A)*, itl_id = cột R *(khớp ^ITL#\\d+$)*, D = tiền tệ {list(TIEN_TE)}, "
            f"E = PS Nợ · F = PS Có *(nguyên tệ, cho H1)*. ⛔ mang cột B (Số chứng từ) · C "
            f"(Diễn giải) — vùng đọc ⛔ phủ B:C (AC-3). {thieu_tt} hàng thiếu tiền tệ D. "
            f"{len(itl_lech)} hàng itl_id ⛔ khớp ^ITL#\\d+$ *(chuỗi lỗi Sheets)* ⇒ LỆCH CÓ TÊN ở "
            f"bảng phụ `itl_id_lech` (mong 4; khác ⇒ ĐỎ) — H4 nối 4 dòng ấy bằng dong_sheet. "
            f"⛔ vùng công thức thừa: cột đầu vào dưới hàng 7892 RỖNG (đo 18/11). "
            f"Bảng phụ `so_du_dau` = {len(so_du_dau)} ô số dư đầu kỳ GÕ TAY ở hàng 24 lệch khuôn "
            f"CALC_ZONE (R-chẩn orchestrator: 5/{SO_DU_DAU_MAU_SO} ô lệch khuôn ở AX10:BT7892) — "
            f"công thức verbatim + hằng trích; H4 gieo vào engine qua `so_du_dau` (errata ⑳: FLS "
            f"chưa có khái niệm số dư đầu kỳ — nguồn chính thức là câu hỏi cho BA/owner)."),
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
    """Cổng KỲ *(④)* — y hệt `gl_406`: số hàng mỗi kỳ ↔ `phan_bo_ky` *(có `LECH_CO_TEN`)*.

    `thieu` = kỳ lệch NGOÀI 4 kỳ có tên *(thừa · thiếu · kỳ lạ — ĐỎ)* + `D` ngoài 5 tiền tệ *(quét
    PII giá trị)*; `lac` = 4 kỳ lệch có tên *(ghi nhận, ⛔ đỏ)*. Nguồn hỏng ⇒ `ValueError`.
    """
    ledger = _phan_bo_ledger()                            # ValueError ⇒ ⛔ đo được
    thuc: dict[int, int] = {}
    for d in dong:
        k = int(d["ky"])                                  # ky là ô số (chuỗi chữ số)
        thuc[k] = thuc.get(k, 0) + 1
    mong_406 = {k: LECH_CO_TEN.get(k, v) for k, v in ledger.items()}
    thieu = sorted(set(thuc) | set(mong_406))
    thieu = [str(k) for k in thieu if thuc.get(k, 0) != mong_406.get(k)]
    # D CÓ chữ mà ⛔ thuộc TẬP ĐÓNG tiền tệ ⇒ LỆCH *(Diễn giải/Số CT lạc cột D)* ⇒ ĐỎ. Ô rỗng cho
    #   phép *(chu?)*. ⛔ IN GIÁ TRỊ — marker chỉ mang `dong_sheet`.
    d_la = sorted(
        (d["dong_sheet"] for d in dong
         if isinstance(d.get("D"), dict) and d["D"]["chu"].strip()
         and d["D"]["chu"].strip() not in TIEN_TE),
        key=int)
    thieu = thieu + [f"D_la@{ds}" for ds in d_la]
    lac = [str(k) for k in sorted(LECH_CO_TEN)]
    khop = sum(1 for k, v in mong_406.items() if thuc.get(k, 0) == v and k not in LECH_CO_TEN)
    return {
        "thieu": thieu,
        "lac": lac,
        "dai": (f"{khop} kỳ khớp phan_bo_ky CHÍNH XÁC · {len(LECH_CO_TEN)} kỳ lệch có tên "
                f"(bản sao 406 dừng giữa 2026-05) · D ngoài {list(TIEN_TE)}: {len(d_la)} · "
                f"nguồn {NGUON_PHAN_BO.name}"),
    }
