"""Khuôn đóng băng `cfa1_dau_vao` — ĐẦU VÀO thô của H5: dòng sổ `ITL Ledge` → LE · HD Final · ngày · tiền.

    python tools/dong_bang_sheet.py cfa1_dau_vao <bản_thô.json> --mong 12590
        ⇒ tests/fixture/dap_an/cfa1_dau_vao.json

⭐ **Vì sao** *(WO-168 · errata ㉓)*: H5 *(`WO-164`)* so CFA1 Daily ↔ đáp án 409 `cfa1_daily.json` *(5 LE ×
74 mã × 760 ngày)*, mà repo ⛔ có ảnh đầu vào mang **LE + ngày + HD Final + tiền** theo dòng sổ
*(đáp án ⛔ dùng làm đầu vào — vòng tròn)*. Khuôn đọc thẳng cột đầu vào của CSV `ITL Ledge` 18/11.

Hợp đồng bản thô *(LƯỚI — `{nguon, doc_luc, cach_doc, dong_dau_sheet, cot, values}`; ⛔ commit bản thô)*:
  · `cot` = `("dong_sheet","A","D","E","F","G","R","V")`: `A` Ngày chứng từ *(CSV hiển thị `MM/DD/YYYY`)* ·
    `D` tiền tệ · `E` PS Nợ · `F` PS Có *(hiển thị `1,234.56`)* · `G` Tài khoản · `R` ITL ID · `V` Budget
    Code *(HDCode)* khối **Final**. ⛔⛔ KHÔNG có `B` Số chứng từ · `C` Diễn giải — `chuan_bi` TỪ CHỐI
    lưới mang cột ngoài danh sách.
  · `G` chỉ dùng để TÁCH LE bằng `fls.repo.man_ghep.tach_nguon` rồi **BỎ** — ⛔ ảnh mang tk/bank.
    `tach_nguon` lỗi khuôn ⇒ `le = null` + ĐẾM theo nhóm ở bảng phụ `le_loi_khuon` *(⛔ đoán LE)*.
  · HD Final hiển thị `MÃ | Tên` ⇒ lấy MÃ *(trước ` | `)*; mã ∉ cây ATL 74 *(GỌI `cfa1_daily.json`)* hoặc
    rỗng ⇒ bảng phụ `hd_ngoai_atl` *(đếm; ⛔ ép về mã gần nhất)*.
  · Ngày ⇒ ISO `YYYY-MM-DD`; ô ⛔ đọc được ⇒ `ngay = null` + `thieu_lac` báo ⇒ ĐỎ. Tiền ⇒ 2 số lẻ
    *(`DT1BM-R1-01`)*; ô tiền ⛔ đọc được ⇒ giữ CHUỖI ⇒ cột `so?` bắt ⇒ ĐỎ.
  · ⛔ In giá trị ô trong lời lỗi — chỉ `dong_sheet` + số đếm *(`DT5-R1-02`)*.
"""
from __future__ import annotations

import datetime
import json
import re
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

GOC = Path(__file__).resolve().parents[2]
if str(GOC) not in sys.path:
    sys.path.insert(0, str(GOC))
from fls.repo.man_ghep import TIEN_TO_TANG, tach_nguon  # noqa: E402

BANG = "PD.409.DauVao"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
COT = ("itl_id", "ngay", "le", "hd_final", "tien_te", "ps_no", "ps_co")
KIEU_COT = {"itl_id": "chu", "ngay": "chu?", "le": "chu?", "hd_final": "chu?",
            "tien_te": "chu?", "ps_no": "so?", "ps_co": "so?"}
RA = "tests/fixture/dap_an/cfa1_dau_vao.json"
#: Bảng phụ: `le_loi_khuon` *(2 nhóm — đo 18/11)* · `hd_ngoai_atl` *(5 nhóm: 4 mã lạ + rỗng — đo 18/11)*.
PHU_MONG = {"le_loi_khuon": 2, "hd_ngoai_atl": 5}

COT_THO = ("dong_sheet", "A", "D", "E", "F", "G", "R", "V")
DONG_DAU_SHEET = 10
TIEN_TE = ("USD", "SGD", "VND", "HKD", "COP")
NGUON_ATL = GOC / "tests" / "fixture" / "dap_an" / "cfa1_daily.json"
_NGAY = re.compile(r"(\d{2})/(\d{2})/(\d{4})")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _ngay_iso(v: Any) -> str | None:
    m = _NGAY.fullmatch(v.strip()) if isinstance(v, str) else None
    if not m:
        return None
    try:
        return datetime.date(int(m.group(3)), int(m.group(1)), int(m.group(2))).isoformat()
    except ValueError:
        return None


def _tien(v: Any) -> Any:
    """`1,234.5` → `Decimal("1234.50")` *(công cụ ghi đúng chữ số)*; rỗng → None; ⛔ đọc được → giữ chuỗi *(cột `so?` bắt ⇒ ĐỎ)*."""
    if _rong(v):
        return None
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        v = str(v)
    try:
        return Decimal(str(v).replace(",", "").strip()).quantize(Decimal("0.01"))
    except (InvalidOperation, ValueError):
        return v


def _ma_atl() -> frozenset[str]:
    try:
        j = json.loads(NGUON_ATL.read_text(encoding="utf-8"))
        ma = frozenset(r["ma"]["chu"] for r in j["phu"]["hd"]["dong"])
        if not ma:
            raise ValueError("rỗng")
        return ma
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise ValueError(f"⛔ đọc được cây ATL từ {NGUON_ATL.name}: {type(e).__name__}") from None


def _nhom_loi_le(g: str) -> str:
    co = "co" if g.startswith(TIEN_TO_TANG) else "khong"
    return f"{g.count('_')}_gach_{co}_tien_to"


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    if tho.get("cot") != list(COT_THO):
        raise ValueError(f"`cot` phải đúng {list(COT_THO)} *(⛔ cột B Số chứng từ · C Diễn giải)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET}")
    values = tho.get("values")
    if not isinstance(values, list) or not values:
        raise ValueError("`values` phải lưới hàng dữ liệu ⛔ rỗng")
    atl = _ma_atl()
    dong: list[list[Any]] = []
    loi_le: dict[str, int] = {}
    hd_ngoai: dict[str, int] = {}
    for i, h in enumerate(values):
        if not isinstance(h, list) or len(h) != len(COT_THO):
            raise ValueError(f"hàng {i + 1} phải {len(COT_THO)} ô")
        ds, a, d_tt, e, f, g, r, v = h
        if ds != DONG_DAU_SHEET + i:
            raise ValueError(f"hàng {i + 1}: dong_sheet ⛔ liên tục *(mong {DONG_DAU_SHEET + i})*")
        gs = "" if g is None else str(g)
        try:
            le = tach_nguon(gs)["le"]
        except ValueError:
            le = None
            k = _nhom_loi_le(gs)
            loi_le[k] = loi_le.get(k, 0) + 1
        # `g` (tk/bank) dừng ở đây — ⛔ vào `dong`.
        hd = None if _rong(v) else str(v).split(" | ")[0].strip() or None
        if hd is None or hd not in atl:
            k = hd if hd is not None else ""
            hd_ngoai[k] = hd_ngoai.get(k, 0) + 1
        dong.append([ds, None if _rong(r) else r, _ngay_iso(a), le, hd,
                     None if _rong(d_tt) else str(d_tt).strip(), _tien(e), _tien(f)])
    phu = {
        "le_loi_khuon": [{"nhom": k, "so_dong": n} for k, n in sorted(loi_le.items())],
        "hd_ngoai_atl": [{"nhom": "rong" if k == "" else "ngoai_atl", "hd": k or None, "so_dong": n}
                         for k, n in sorted(hd_ngoai.items())],
    }
    les = sorted({d[3] for d in dong if d[3]})
    return {
        "cot": [KHOA, *COT], "dong": dong, "phu": phu,
        "ghi_chu": (
            f"ĐẦU VÀO H5 = {len(dong)} dòng sổ ITL Ledge, dong_sheet {DONG_DAU_SHEET}…"
            f"{DONG_DAU_SHEET + len(dong) - 1} liên tục. LE tách bằng man_ghep.tach_nguon từ cột G "
            f"rồi BỎ G *(⛔ tk/bank)*: {len(les)} LE đo được {les}; {sum(loi_le.values())} dòng lỗi "
            f"khuôn ⇒ le null, theo nhóm {loi_le} *(⛔ đoán LE)*. HD Final lấy MÃ trước ' | '; "
            f"{sum(hd_ngoai.values())} dòng mã ∉ cây ATL {len(atl)} hoặc rỗng ⇒ `hd_ngoai_atl` "
            f"{len(phu['hd_ngoai_atl'])} nhóm. Ngày MM/DD/YYYY → ISO; tiền 2 số lẻ. ⛔ mang cột B "
            f"Số chứng từ · C Diễn giải · tài khoản · bank."),
    }


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """`thieu` = ngày ⛔ đọc được · tiền tệ ngoài 5 tiền tệ *(⛔ in giá trị — chỉ `dong_sheet`)*."""
    thieu: list[str] = []
    for d in dong:
        if d.get("ngay") is None:
            thieu.append(f"ngay_khong_doc@{d['dong_sheet']}")
        t = d.get("tien_te")
        if isinstance(t, dict) and t["chu"] not in TIEN_TE:
            thieu.append(f"tien_te_la@{d['dong_sheet']}")
    return {"thieu": thieu, "lac": [],
            "dai": f"{len(dong)} dòng · ngày ⛔ đọc được/tiền tệ lạ: {len(thieu)}"}
