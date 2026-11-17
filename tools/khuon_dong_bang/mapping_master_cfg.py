"""Khuôn đóng băng `mapping_master_cfg` — tab `Mapping Master` *(RAW)* → `IX.HD` · `IX.ORG`.

    python tools/dong_bang_sheet.py mapping_master_cfg <bản_thô.json> --mong 73
        ⇒ tests/fixture/cau_hinh/mapping_master_cfg.json

Nguồn: bản sao RAW ▸ `'Mapping Master'!A1:P120` — **LƯỚI Ô của SA** *(`DT3-R1-03`)*: hợp đồng
`{spreadsheet_id, nguon, doc_luc, cach_doc, values}`, `values` theo HÀNG *(hàng 1 = dòng sheet 1;
ô rỗng cuối hàng bị API cắt)*. Ảnh có HAI phần:

  ① **Bảng chính = ĐẦU RA của `fls.adapters.mapping_master.doc_cot`** *(ISP Step 10: "⛔ khuôn
    đọc thứ hai")* — khuôn GỌI hàm thật trên sáu cột `H…M` *(từ dòng 7)*, ⛔ chép luật đọc nào. Đo:
    **73** mã `hd`, 0 dòng bị loại *(khớp đo 28/08 ở docstring adapter: 73 · 23 · 21 · 52 · 0 · 0)*.
    Dòng bị loại *(ô lỗi · mã trùng)* ⇒ bảng phụ `loai`, mong **0**.
  ② **Bảng phụ `tho` = cột `A:B · D:G` THÔ** *(quyết định ⑫ của `WO-106`)* — mọi dòng sheet có ô
    ở sáu cột ấy *(đo: **84**)*. `A:B` = *"Mapping LE I Legal Entity"* *(tên sheet bank → LE, phục
    vụ `IX.ORG`)*; `D:G` = cấp `L1…L4` *(dấu `x`)* + dòng tiêu đề nhóm của cây HD. ⛔ `AA:AD`:
    `Q1:AN120` của RAW RỖNG hoàn toàn *(⑫)*. ⛔ `C · N · O · P` *(C rỗng; O:P = "Mapping No via
    LE" — `O` lặp LE, mang tên người ở 7 hàng)*; ⛔ dòng 1…6 của `H…M` *(nhãn phụ)*.

⛔⛔ **Riêng tư — GIẢ DANH HOÁ, ⛔ BĂM** *(`DT3-R1-01` — người dùng duyệt 17/11)*. 7 hàng của
`A:B` là tài khoản PO CÁ NHÂN: `B` là tên viết tắt NGƯỜI, `A` mang số tài khoản + tên ấy ở đuôi
tên sheet. Khuôn **⛔ biết tên nào** — luật ngược: từ dòng `DONG_DAU_LE` *(4)*, hàng nào có `B`
⛔ thuộc `LE_PHAP_NHAN` *(21 mã pháp nhân/nhãn quỹ đo 17/11)* thì **cả `A` lẫn `B`** bị thay bằng
HẰNG `AN_DANH = "an_danh:tk_ca_nhan"` *(⛔ còn chuỗi riêng của hàng — một người mới TỰ bị ẩn danh,
⛔ cần ai khai trước)*. Bảng phụ `an_danh` *(mong **7**)* ĐỎ để người nhìn. Dòng 1…3 của `A:B`
phải ĐÚNG bản đã đo *(`TIEU_DE_AB`)* — khác ⇒ TỪ CHỐI *(⛔ để một tên lọt qua vùng "tiêu đề")*.

  ⚠⚠ **Vì sao hằng, ⛔ băm** *(bia của `DT3-R1-01` — mã băm `2a31f76` đảo được)*: băm với muối
  CÔNG KHAI nằm trong repo thì người có repo băm ứng viên rồi so — từ điển 200 viết tắt đảo 7/7,
  vét cạn mù 26⁵ trong 5 giây đảo 4/7. Dữ liệu vào lịch sử git ⛔ rút lại được ⇒ PII là rủi ro số
  1 ⇒ **LOẠI**, ⛔ băm. Cần KHOÁ NỐI ở C8 *(bên đọc nguồn nối lại)* ⇒ **HMAC-SHA256 với khoá BÍ
  MẬT ngoài repo** *(biến môi trường — owner quyết, ⛔ của khuôn)*, ⛔ bao giờ muối/khoá trong repo.
  Mỗi bước có PII phải có bài **tấn công từ điển** *(≥ 200 ứng viên cùng hình dạng)* đòi 0 khớp.
"""
from __future__ import annotations

import re
from typing import Any

from fls.adapters.mapping_master import COT as COT_MM
from fls.adapters.mapping_master import TRUONG, doc_cot

BANG = "IX.HD · IX.ORG"
#: Trường của `doc_cot` — lấy từ adapter *(import, ⛔ chép)*: đổi adapter là ảnh đổi theo.
KHOA = TRUONG[0]
KIEU_KHOA = "ma"
COT = (*TRUONG[1:], "dong_sheet")
#: Mọi trường ngoài khoá đều được RỖNG *(đo 28/08: COA1/COA2 rỗng hết · 52/73 `method` rỗng)*.
KIEU_COT = {t: "chu?" for t in TRUONG[1:]}
RA = "tests/fixture/cau_hinh/mapping_master_cfg.json"
#: Đo 17/11 *(Đ5 — khác ⇒ ĐỎ)*: 84 dòng có ô ở A:B·D:G · 7 hàng ẩn danh · 0 dòng doc_cot loại.
PHU_MONG = {"tho": 84, "an_danh": 7, "loai": 0}

#: Cột THÔ mang vào bảng phụ `tho` *(⑫)*.
COT_THO = ("A", "B", "D", "E", "F", "G")
#: Dòng đầu của DỮ LIỆU `A:B` — dòng 1 tiêu đề vùng, dòng 2 trống, dòng 3 nhãn cột.
DONG_DAU_LE = 4
#: Ba ô tiêu đề của `A:B` đo 17/11 — mọi ô khác ở dòng 1…3 của `A:B` phải RỖNG.
TIEU_DE_AB = {(1, "A"): "Mapping LE I Legal Entity", (3, "A"): "Bank Sheet", (3, "B"): "LE"}
#: ⭐ Pháp nhân / nhãn quỹ được GIỮ RÕ ở cột `B` — 21 giá trị đo 17/11 *(⛔ tên người)*. `Cash
#: Treasury` là nhãn ⛔ phải pháp nhân *(`fls/canon/le.py` · `INV-I10`)* nhưng ⛔ phải người.
LE_PHAP_NHAN = frozenset({
    "BGO1", "BGO2", "CN", "Cash Treasury", "HGO1", "HGO2", "HGO6", "MGO1", "SGO1", "SGO2",
    "UGO1", "VGC1", "VGO1", "VGOH", "VOOA", "VOOL", "VOON", "VVOH", "VVOS", "VVOT", "VVOV"})

#: ⭐ HẰNG giả danh hoá — thay CẢ `A` lẫn `B` của hàng tài khoản cá nhân *(⛔ chuỗi riêng nào)*.
AN_DANH = "an_danh:tk_ca_nhan"

_VUNG = re.compile(r"!([A-Z]+)(\d+):([A-Z]+)(\d+)")


def _so_cot(chu: str) -> int:
    n = 0
    for c in chu:
        n = n * 26 + ord(c) - 64
    return n


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Lưới ô SA → bảng `doc_cot` + bảng phụ `tho` *(đã giả danh hoá)* · `an_danh` · `loai`.
    ⛔ Lời lỗi mang giá trị ô *(công cụ in lời khuôn — nguồn này CÓ tên người)*."""
    v = _VUNG.findall(tho["nguon"])
    if len(v) != 1 or (v[0][0], v[0][1]) != ("A", "1"):
        raise ValueError("`nguon` phải khai ĐÚNG một vùng bắt đầu `!A1:` — `doc_cot` đếm dòng từ "
                         "dòng sheet 1, cột theo chữ cái từ A")
    rong, cuoi = _so_cot(v[0][2]), int(v[0][3])
    hang = tho.get("values")
    if not isinstance(hang, list) or not hang or len(hang) > cuoi:
        raise ValueError(f"`values` phải lưới 1…{cuoi} hàng")
    for r, h in enumerate(hang, 1):
        if not isinstance(h, list) or len(h) > rong \
                or not all(x is None or isinstance(x, str) for x in h):
            raise ValueError(f"dòng sheet {r}: hàng phải danh sách ≤ {rong} ô chuỗi/rỗng")

    def o(r: int, c: str) -> str | None:
        h, j = hang[r - 1], ord(c) - 65
        x = h[j] if j < len(h) else None
        return None if x is None or x == "" else x

    for r in range(1, DONG_DAU_LE):
        for c in "AB":
            if r <= len(hang) and o(r, c) != TIEU_DE_AB.get((r, c)):
                raise ValueError(f"ô {c}{r}: tiêu đề `A:B` ⛔ đúng bản đo 17/11 — bố cục đã đổi")

    ra, loai = doc_cot({c: [h[ord(c) - 65] if ord(c) - 65 < len(h) else None for h in hang]
                        for c in COT_MM})
    dong = [[getattr(d, t) for t in TRUONG] + [d.dong_sheet] for d in ra]

    tho_ra: list[dict[str, Any]] = []
    an_danh_ra: list[dict[str, Any]] = []
    for r in range(1, len(hang) + 1):
        d = {c: o(r, c) for c in COT_THO}
        if r >= DONG_DAU_LE and (d["A"] is not None or d["B"] is not None) \
                and not (d["B"] is not None and d["B"].strip() in LE_PHAP_NHAN):
            cot_an = [c for c in "AB" if d[c] is not None]
            for c in cot_an:
                d[c] = AN_DANH
            an_danh_ra.append({"dong_sheet": r, "cot": "·".join(cot_an)})
        if any(x is not None for x in d.values()):
            tho_ra.append({"dong_sheet": r, **d})

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"tho": tho_ra, "an_danh": an_danh_ra,
                "loai": [{"dong_sheet": x.dong_sheet, "hd_code": x.hd_code, "ly_do": x.ly_do}
                         for x in loai]},
        "ghi_chu": (
            f"Bảng chính = đầu ra fls.adapters.mapping_master.doc_cot trên cột H…M (từ dòng 7): "
            f"{len(dong)} mã, {len(loai)} dòng loại (bảng phụ `loai`). Bảng phụ `tho` = cột "
            f"A:B · D:G THÔ, {len(tho_ra)} dòng sheet có ô. ⛔ mang: cột C · N · O · P; dòng 1…6 "
            "của H…M; vùng AA:AD (⑫: RỖNG ở RAW). Riêng tư (DT3-R1-01): từ dòng "
            f"{DONG_DAU_LE}, hàng có B ⛔ thuộc {len(LE_PHAP_NHAN)} pháp nhân/nhãn quỹ đã khai ⇒ "
            f"A và B thay bằng HẰNG '{AN_DANH}' (giả danh hoá — ⛔ băm, ⛔ muối, ⛔ chuỗi riêng "
            f"nào; nối ở C8 ⇒ HMAC khoá ngoài repo, owner quyết); {len(an_danh_ra)} hàng ẩn danh "
            "(bảng phụ `an_danh`)."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """⛔ áp dụng — bảng mã ⛔ có dải. Cổng của bảng = `--mong` + khoá ⛔ trùng/hỏng *(công cụ)*
    + bảng phụ `loai` mong 0 *(trùng/ô lỗi mà `doc_cot` đã gạt)*."""
    return {"thieu": [], "lac": [],
            "dai": "⛔ áp dụng — bảng mã; trùng/ô lỗi của doc_cot ở bảng phụ `loai` (mong 0)"}
