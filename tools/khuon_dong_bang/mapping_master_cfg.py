"""Khuôn đóng băng `mapping_master_cfg` — tab `Mapping Master` *(RAW)* → `IX.HD` · `IX.ORG`.

    python tools/dong_bang_sheet.py mapping_master_cfg <bản_thô.json> --mong 73
        ⇒ tests/fixture/cau_hinh/mapping_master_cfg.json

Nguồn: bản sao RAW `ITL I Input Transaction Ledger File 1/2` ▸ `'Mapping Master'!A1:P120` — lưới
thô theo HÀNG *(hàng 1 = dòng sheet 1; ô rỗng cuối hàng bị API cắt)*. Ảnh có HAI phần:

  ① **Bảng chính = ĐẦU RA của `fls.adapters.mapping_master.doc_cot`** *(ISP Step 10: "⛔ khuôn
    đọc thứ hai")* — khuôn GỌI hàm thật trên sáu cột `H…M`, ⛔ chép luật đọc nào. Đo 16/11:
    **73** mã `hd`, 0 dòng bị loại *(khớp đo 28/08 ở docstring adapter: 73 · 23 · 21 · 52 · 0 · 0)*.
    Dòng bị loại *(ô lỗi · mã trùng)* ⇒ bảng phụ `loai`, mong **0**.
  ② **Bảng phụ `tho` = cột `A:B · D:G` THÔ** *(quyết định ⑫ của `WO-106`)* — mọi dòng sheet có ô
    ở sáu cột ấy *(đo: **84**/85 — trừ dòng 2)*. `A:B` = *"Mapping LE I Legal Entity"* *(tên sheet
    bank → LE, phục vụ `IX.ORG`)*; `D:G` = cấp `L1…L4` *(dấu `x`)* + dòng tiêu đề nhóm của cây HD.
    ⛔ `AA:AD`: `Q1:AN120` của RAW RỖNG hoàn toàn *(⑫ — đó là Mapping Master của FS2, ảnh riêng
    trước C8)*. ⛔ `C · N · O · P` *(C rỗng; O:P = "Mapping No via LE" — `O` lặp LE, mang tên
    người ở 7 hàng)*; ⛔ dòng 1…6 của `H…M` *(nhãn phụ — `doc_cot` đọc từ dòng 7)*.

⛔⛔ **Riêng tư — BĂM, đóng KHI LẠ.** 7 hàng của `A:B` *(dòng 70…76)* là tài khoản PO CÁ NHÂN:
`B` là tên viết tắt NGƯỜI, `A` mang số tài khoản + tên ấy ở đuôi tên sheet. ⛔ Khuôn **⛔ biết
tên nào** — luật ngược lại: từ dòng `DONG_DAU_LE` *(4 — dòng 1 tiêu đề, dòng 3 nhãn cột)*, hàng
nào có `B` ⛔ thuộc `LE_PHAP_NHAN` *(21 mã pháp nhân/nhãn quỹ đo 16/11)* thì **cả `A` lẫn `B`**
bị thay bằng mã băm. Một người mới ⛔ cần ai khai trước — nó TỰ bị băm, và bảng phụ `bam`
*(mong **7**)* ĐỎ để người nhìn. Dòng 1…3 của `A:B` phải ĐÚNG bản đã đo *(`TIEU_DE_AB`)* —
khác ⇒ TỪ CHỐI *(⛔ để một tên lọt qua vùng "tiêu đề")*.

  Cách băm *(khai muối/cách — lời giao DT3)*:
      bam(v) = "sha256_16:" + sha256( MUOI + "\\x1f" + v.strip() ).hexdigest()[:16]
  `MUOI` là hằng CÔNG KHAI dưới đây *(tách miền: cùng giá trị ở bảng khác ⇒ mã khác)*. Ô đã là
  mã băm thì giữ nguyên *(chạy lại trên ảnh tái tạo ra đúng từng byte)*. ⚠ Muối công khai ⇒ một
  tên viết tắt 5–7 chữ cái DÒ NGƯỢC được bằng vét cạn — mã băm ở đây để **⛔ chép tên vào repo**
  và để NỐI được *(bên đọc nguồn băm cùng cách)*, ⛔ phải để giấu với người có mã nguồn. Muốn
  giấu thật ⇒ muối BÍ MẬT ngoài repo — quyết định của owner, ⛔ của khuôn.
"""
from __future__ import annotations

import hashlib
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
#: Đo 16/11 *(Đ5 — khác ⇒ ĐỎ)*: 84 dòng có ô ở A:B·D:G · 7 hàng băm · 0 dòng doc_cot loại.
PHU_MONG = {"tho": 84, "bam": 7, "loai": 0}

#: Cột THÔ mang vào bảng phụ `tho` *(⑫)*.
COT_THO = ("A", "B", "D", "E", "F", "G")
#: Dòng đầu của DỮ LIỆU `A:B` — dòng 1 tiêu đề vùng, dòng 2 trống, dòng 3 nhãn cột.
DONG_DAU_LE = 4
#: Ba ô tiêu đề của `A:B` đo 16/11 — mọi ô khác ở dòng 1…3 của `A:B` phải RỖNG.
TIEU_DE_AB = {(1, "A"): "Mapping LE I Legal Entity", (3, "A"): "Bank Sheet", (3, "B"): "LE"}
#: ⭐ Pháp nhân / nhãn quỹ được GIỮ RÕ ở cột `B` — 21 giá trị đo 16/11 *(⛔ tên người)*. `Cash
#: Treasury` là nhãn ⛔ phải pháp nhân *(`fls/canon/le.py` · `INV-I10`)* nhưng ⛔ phải người.
LE_PHAP_NHAN = frozenset({
    "BGO1", "BGO2", "CN", "Cash Treasury", "HGO1", "HGO2", "HGO6", "MGO1", "SGO1", "SGO2",
    "UGO1", "VGC1", "VGO1", "VGOH", "VOOA", "VOOL", "VOON", "VVOH", "VVOS", "VVOT", "VVOV"})

MUOI = "fls-dt3-mapping_master_cfg-v1"
MA_BAM = re.compile(r"sha256_16:[0-9a-f]{16}")

_VUNG = re.compile(r"!([A-Z]+)(\d+):([A-Z]+)(\d+)")


def bam(v: str) -> str:
    """Giá trị → mã băm *(xem docstring)*. Ô đã là mã băm ⇒ giữ nguyên."""
    if MA_BAM.fullmatch(v):
        return v
    return "sha256_16:" + hashlib.sha256(f"{MUOI}\x1f{v.strip()}".encode()).hexdigest()[:16]


def _so_cot(chu: str) -> int:
    n = 0
    for c in chu:
        n = n * 26 + ord(c) - 64
    return n


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Lưới thô → bảng `doc_cot` + bảng phụ `tho` *(đã băm)* · `bam` · `loai`. ⛔ Lời lỗi mang
    giá trị ô *(công cụ in lời khuôn — nguồn này CÓ tên người)*."""
    v = _VUNG.findall(tho["nguon"])
    if len(v) != 1 or (v[0][0], v[0][1]) != ("A", "1"):
        raise ValueError("`nguon` phải khai ĐÚNG một vùng bắt đầu `!A1:` — `doc_cot` đếm dòng từ "
                         "dòng sheet 1, cột theo chữ cái từ A")
    rong, cuoi = _so_cot(v[0][2]), int(v[0][3])
    hang = tho.get("dong")
    if not isinstance(hang, list) or not hang or len(hang) > cuoi:
        raise ValueError(f"`dong` phải danh sách 1…{cuoi} hàng")
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
                raise ValueError(f"ô {c}{r}: tiêu đề `A:B` ⛔ đúng bản đo 16/11 — bố cục đã đổi")

    ra, loai = doc_cot({c: [h[ord(c) - 65] if ord(c) - 65 < len(h) else None for h in hang]
                        for c in COT_MM})
    dong = [[getattr(d, t) for t in TRUONG] + [d.dong_sheet] for d in ra]

    tho_ra: list[dict[str, Any]] = []
    bam_ra: list[dict[str, Any]] = []
    for r in range(1, len(hang) + 1):
        d = {c: o(r, c) for c in COT_THO}
        if r >= DONG_DAU_LE and (d["A"] is not None or d["B"] is not None) \
                and not (d["B"] is not None and d["B"].strip() in LE_PHAP_NHAN):
            cot_bam = [c for c in "AB" if d[c] is not None]
            for c in cot_bam:
                d[c] = bam(d[c])
            bam_ra.append({"dong_sheet": r, "cot": "·".join(cot_bam)})
        if any(x is not None for x in d.values()):
            tho_ra.append({"dong_sheet": r, **d})

    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"tho": tho_ra, "bam": bam_ra,
                "loai": [{"dong_sheet": x.dong_sheet, "hd_code": x.hd_code, "ly_do": x.ly_do}
                         for x in loai]},
        "ghi_chu": (
            f"Bảng chính = đầu ra fls.adapters.mapping_master.doc_cot trên cột H…M (từ dòng 7): "
            f"{len(dong)} mã, {len(loai)} dòng loại (bảng phụ `loai`). Bảng phụ `tho` = cột "
            f"A:B · D:G THÔ, {len(tho_ra)} dòng sheet có ô. ⛔ mang: cột C · N · O · P; dòng 1…6 "
            "của H…M; vùng AA:AD (⑫: RỖNG ở RAW). Riêng tư: từ dòng "
            f"{DONG_DAU_LE}, hàng có B ⛔ thuộc {len(LE_PHAP_NHAN)} pháp nhân/nhãn quỹ đã khai ⇒ "
            "A và B thay bằng bam(v) = 'sha256_16:' + sha256(MUOI + '\\x1f' + v.strip())[:16], "
            f"MUOI = '{MUOI}' (công khai — dò ngược được bằng vét cạn; mã băm để ⛔ chép tên và "
            f"để nối, ⛔ để giấu); {len(bam_ra)} hàng băm (bảng phụ `bam`)."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """⛔ áp dụng — bảng mã ⛔ có dải. Cổng của bảng = `--mong` + khoá ⛔ trùng/hỏng *(công cụ)*
    + bảng phụ `loai` mong 0 *(trùng/ô lỗi mà `doc_cot` đã gạt)*."""
    return {"thieu": [], "lac": [],
            "dai": "⛔ áp dụng — bảng mã; trùng/ô lỗi của doc_cot ở bảng phụ `loai` (mong 0)"}
