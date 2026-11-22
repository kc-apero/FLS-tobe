"""Thân chung của 4 khuôn ảnh đáp án H14 *(ISP 3.1.2 · Step 41 · DT11 · vòng sửa `KQ-271` `DT11-R1-02`)*:
`daily_report_3_fs2` · `daily_report_3_fs1` · `daily_report_3_gop` *(PD 607 · 608 · 609 — sổ `[COPY] … P&L Report`)* và
`ccr_daily_report` *(PD 615 — sổ A-CCR)*. **Khuôn mới, tệp riêng** — ⛔ sửa `daily_report_2/3` · `_daily_report` · ảnh cũ.

⭐ **Lưới chung** *(bố cục họ `5. Daily Report*` — 4 tab cùng khung `A1:AL…`: nhãn `A…E`, cột `F…AL`)*:
  · ảnh khoá theo **hàng sheet** `dong_sheet`; cột nhãn `nhan_a…nhan_e` *(chữ; số ở cột `A` của A-CCR ghi thành chữ)* +
    `phan` *(vết "đoạn": chữ của hàng-đầu-đoạn gần nhất ≥ 8 ký tự, vd `CM Cumulative` · `CHECK ZONE`)* + `khoi` *(mã trước `|`
    ở hàng tiêu đề khối gần nhất, vd `GROUP` · `CVL`)* + `ma` *(mã trước `|` ở nhãn `B…E`)*;
  · cột giá trị `f…al` = **đúng chữ cột Sheets `F…AL`** *(33 cột, kiểu `so!`: số HOẶC ô lỗi Sheets, ghi nguyên chuỗi + đếm
    theo cột + ghim phân bố)*; nghĩa của cột = bảng phụ `tieu_de` *(Đ4: cột chỉ có CHỮ CỘT, nghĩa nằm ở hàng tiêu đề)*;
  · **ô CHỮ / bool** ở vùng giá trị ⇒ bảng phụ `o_khong_so` *(nguyên văn, có hàng + cột; ⛔ ép số, ⛔ vứt)*;
  · hàng **tiêu đề** *(`dong_sheet ≤ N_DAU`, hoặc có CHỮ/bool ở `G…AL`)* ⇒ phụ `tieu_de` *(mọi ô ≠ rỗng, nguyên văn)*;
  · hàng chỉ có nhãn ⇒ phụ `dong_chi_nhan`; hàng rỗng hẳn ⛔ mang.
Mỗi khuôn khai `MONG_COT` *(số ô số ≠ rỗng THEO CỘT)* · `MONG_DONG` *(hàng·ô theo `phan:khoi`)* · `CHUA_CO_DU_LIEU` *(cột 0 ô số — có tên)* · `LOI_MONG` *(ô lỗi theo cột)* · `PHU_MONG` — **Đ5**: khác ⇒ ĐỎ cả hai chiều; tập rỗng ⇒ `ValueError`
*(Đ3: mẫu số 0 ⛔ nền xanh)*.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys
from dataclasses import dataclass
from typing import Any

from fls.canon.o_loi import la_o_loi

W = 38                                                       # A…AL
COT_NHAN = ("nhan_a", "nhan_b", "nhan_c", "nhan_d", "nhan_e")
COT_GT = tuple(c.lower() for c in "F G H I J K L M N O P Q R S T U V W X Y Z AA AB AC AD AE AF AG AH AI AJ AK AL".split())
COT = ("phan", "khoi", "ma", *COT_NHAN, *COT_GT)
KIEU_COT = {"phan": "chu?", "khoi": "chu?", "ma": "chu?", **{c: "chu?" for c in COT_NHAN}, **{c: "so!" for c in COT_GT}}
assert len(COT_GT) == 33


def _quet():
    """`tools/quet_pii_repo.py` — MỘT bản khai mẫu số TK cá nhân *(⛔ viết lại)*; nạp theo đường dẫn *(`tools/` ⛔ là gói)*."""
    p = pathlib.Path(__file__).resolve().parents[1] / "quet_pii_repo.py"
    s = importlib.util.spec_from_file_location("khuon_dong_bang__quet_pii", p)
    m = sys.modules.get(s.name) or importlib.util.module_from_spec(s)
    if s.name not in sys.modules:
        sys.modules[s.name] = m
        s.loader.exec_module(m)
    return m


def che_pii(ra: dict[str, Any]) -> int:
    """⭐ Che số TK CÁ NHÂN *(nhãn `R | <số>_<NH> <TT>_CN` — gặp ở sổ A-CCR, tab `5. Daily Report`)* → `TK_CA_NHAN_<n>`
    NGAY ở khuôn, TRƯỚC khi ghi ảnh: ảnh commit ⛔ mang số thật *(`CLAUDE.md` · "Riêng tư & tiền thật"; bài
    `tests/kiem/test_quet_pii_repo.py` ĐỎ khi còn)*. `n` theo thứ tự gặp đầu tiên trong chính ảnh, cùng số ⇒ cùng mã,
    ⛔ đảo được. Che NGAY trong `ra` *(tại chỗ)*; trả số chuỗi bị đổi *(Đ4: ô chữ, ⛔ số TK)*. 0 ⇒ ảnh sạch sẵn."""
    q = _quet()
    ma: dict[str, int] = {}

    def duyet(o: Any):
        if isinstance(o, dict):
            for v in o.values():
                yield from duyet(v)
        elif isinstance(o, list):
            for v in o:
                yield from duyet(v)
        elif isinstance(o, str):
            yield o

    for s in duyet(ra):                                      # lượt 1: gom SỐ theo thứ tự gặp đầu tiên
        for so in q.so_cn(s):
            ma.setdefault(so, len(ma) + 1)
    if not ma:
        return 0

    def thay(o: Any) -> Any:                                 # lượt 2: thay tại chỗ, ⛔ đụng kiểu khác `str` (Decimal giữ nguyên)
        if isinstance(o, dict):
            return {k: thay(v) for k, v in o.items()}
        if isinstance(o, list):
            return [thay(v) for v in o]
        return q.che_van_ban(o, ma) if isinstance(o, str) else o

    moi = thay(ra)
    ra.clear()
    ra.update(moi)
    return len(ma)


@dataclass(frozen=True)
class CauHinh:
    n_hang: int            # số hàng `values` đọc về *(API cắt hàng cuối rỗng)*
    n_dau: int             # hàng sheet ≤ n_dau luôn là tiêu đề
    vung: str              # vùng đọc, vd `A1:AN1424`


def chu_cot(n: int) -> str:
    s, n = "", n + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v.strip() == "")


def _la_so(x: Any) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _chu(x: Any) -> bool:
    """Ô CHỮ thật *(⛔ lỗi `#…`, ⛔ `-`, ⛔ rỗng)* hoặc bool."""
    if isinstance(x, bool):
        return True
    return isinstance(x, str) and x.strip() not in ("", "-") and not la_o_loi(x)


def chuan_bi(tho: dict[str, Any], ch: CauHinh, mo_ta: str) -> dict[str, Any]:
    V = tho.get("values")
    if not isinstance(V, list) or len(V) != ch.n_hang or any(not isinstance(h, list) for h in V):
        raise ValueError(f"`values` phải {ch.n_hang} hàng *(vùng {ch.vung}, API cắt hàng cuối rỗng)*")
    if any(len(h) > W for h in V):
        raise ValueError(f"`values` rộng quá {W} cột *(A…AL)*")
    V = [list(h) + [""] * (W - len(h)) for h in V]
    phan, khoi = "", ""
    dong, chi_nhan, tieu_de, o_chu = [], [], [], []
    n_trong = 0
    for i, h in enumerate(V):
        ds = i + 1
        a = h[0]
        gt = h[5:W]
        nhan_ngoai_a = [None if _rong(h[j]) else str(h[j]) for j in range(1, 5)]
        co_chu_gt = any(_chu(x) for x in h[6:W])             # `G…AL` — ⛔ `F` *(cột F có chữ ở hàng dữ liệu)*
        tieu = ds <= ch.n_dau or co_chu_gt
        if tieu:
            for j in range(W):
                if not _rong(h[j]):
                    tieu_de.append({"dong_sheet": ds, "cot": chu_cot(j), "gia_tri": h[j]})
            ten = str(a).split("|")[0].strip() if not _rong(a) else (nhan_ngoai_a[0] or "").split("|")[0].strip()
            if ds > ch.n_dau and ten and ten != ".":
                khoi = ten
            continue
        sa = "" if _rong(a) else str(a).strip()
        n_gt = sum(1 for x in gt if not _rong(x) and x != "-")
        if n_gt == 0:                                        # hàng không giá trị: đầu đoạn / chỉ nhãn / rỗng
            if sa and sa != "." and not any(nhan_ngoai_a):
                if len(sa) >= 8:
                    phan, khoi = sa[:60], ""
                elif sa in ("GROUP", "SGO2", "SGO1", "HGO2", "BGO2"):
                    khoi = sa
            if sa not in ("", ".") or any(nhan_ngoai_a):
                chi_nhan.append({"dong_sheet": ds, "phan": phan or None, "khoi": khoi or None,
                                 "nhan": " > ".join(x for x in [sa if sa != "." else None, *nhan_ngoai_a] if x)})
            else:
                n_trong += 1
            continue
        cells: list[Any] = []
        for j, x in enumerate(gt):
            c = chu_cot(5 + j)
            if _rong(x) or x == "-":
                cells.append(None)
            elif isinstance(x, bool) or (isinstance(x, str) and not la_o_loi(x)):
                o_chu.append({"dong_sheet": ds, "cot": c, "gia_tri": x})      # CHỮ/bool: nguyên văn ở phụ, ⛔ ép số
                cells.append(None)
            else:
                cells.append(x)                              # số · hoặc chuỗi lỗi `#…` ghi nguyên
        lab = [None if _rong(h[j]) else str(h[j]) for j in range(0, 5)]
        ma = next((x.split("|")[0].strip() for x in [*lab[1:], lab[0]] if x and x != "."), None)
        if all(x is None for x in cells):                    # chỉ có ô chữ ⇒ giữ ở `o_chu`, hàng ⛔ vào bảng chính
            chi_nhan.append({"dong_sheet": ds, "phan": phan or None, "khoi": khoi or None,
                             "nhan": " > ".join(x for x in lab if x and x != ".")})
            continue
        dong.append([ds, phan or None, khoi or None, ma, *lab, *cells])
    if not dong:
        raise ValueError("0 hàng dữ liệu — mẫu số 0 (Đ3)")
    ra = {
        "cot": ["dong_sheet", *COT],
        "dong": dong,
        "phu": {"tieu_de": tieu_de, "dong_chi_nhan": chi_nhan, "o_khong_so": o_chu},
        "ghi_chu": (
            f"{mo_ta}: vùng {ch.vung} · {len(dong)} hàng sheet có ô số/lỗi × 33 cột F…AL; `phan`/`khoi` = vết đoạn/khối; "
            f"tiêu đề nguyên văn ở `tieu_de` ({len(tieu_de)} ô); ô chữ/bool ở `o_khong_so` ({len(o_chu)} ô, ⛔ ép số); "
            f"{len(chi_nhan)} hàng chỉ nhãn ở `dong_chi_nhan`; {n_trong} hàng rỗng hẳn ⛔ mang."),
    }
    n_che = che_pii(ra)                                       # số TK cá nhân ⇒ `TK_CA_NHAN_<n>` ngay ở khuôn
    if n_che:
        ra["ghi_chu"] += f" ⭐ Che {n_che} số TK cá nhân → `TK_CA_NHAN_<n>` ngay ở khuôn (⛔ ảnh mang số thật)."
    return ra


# ── đo + cổng ───────────────────────────────────────────────────────────────

def _la_loi_o(v: Any) -> bool:
    return isinstance(v, dict) and la_o_loi(v["chu"])


def dem_cot(dong: list[dict[str, Any]]) -> dict[str, int]:
    """Số ô SỐ *(⛔ ô lỗi)* ≠ rỗng THEO CỘT `f…al`."""
    return {c: sum(1 for d in dong if d[c] is not None and not _la_loi_o(d[c])) for c in COT_GT}


def dem_dong(dong: list[dict[str, Any]]) -> dict[str, tuple[int, int]]:
    out: dict[str, tuple[int, int]] = {}
    for d in dong:
        ph = d["phan"]["chu"] if isinstance(d["phan"], dict) else "-"
        kh = d["khoi"]["chu"] if isinstance(d["khoi"], dict) else "-"
        k = f"{ph}:{kh}"
        n, o = out.get(k, (0, 0))
        out[k] = (n + 1, o + sum(1 for c in COT_GT if d[c] is not None))
    return out


def cot_chua_co(dong: list[dict[str, Any]]) -> tuple[str, ...]:
    """Cột `f…al` có **0** ô số/lỗi ở bảng chính ⇒ có tên *(Đ5)*. Cột ấy có TIÊU ĐỀ hay không ⇒ bài đối chiếu `tieu_de`."""
    return tuple(c.upper() for c in COT_GT if all(d[c] is None for d in dong))


def thieu_lac(dong: list[dict[str, Any]], mong_cot: dict[str, int], mong_dong: dict[str, tuple[int, int]],
              chua_mong: tuple[str, ...], nhan: str) -> dict[str, Any]:
    """Cổng *(Đ5)*: ô số theo cột ↔ `MONG_COT` · hàng/ô theo `phan:khoi` ↔ `MONG_DONG` · cột 0 ô ↔ `CHUA_CO_DU_LIEU`.
    Tập rỗng / mong ⛔ khai ⇒ `ValueError` *(Đ3)*."""
    if not dong:
        raise ValueError("0 hàng — mẫu số 0, ⛔ nền xanh (Đ3)")
    if not mong_cot or not mong_dong or sum(mong_cot.values()) <= 0:
        raise ValueError("MONG_COT / MONG_DONG ⛔ khai hoặc 0 ô — cổng ⛔ đo được")
    thieu: list[str] = []
    oc = dem_cot(dong)
    thieu += [f"cột {c.upper()}: {oc.get(c)}≠{mong_cot.get(c)}" for c in COT_GT if oc.get(c) != mong_cot.get(c)]
    dd = dem_dong(dong)
    if dd != mong_dong:
        thieu += [f"{k}: {dd.get(k)}≠{mong_dong.get(k)}" for k in sorted(set(dd) | set(mong_dong)) if dd.get(k) != mong_dong.get(k)]
    chua = cot_chua_co(dong)
    if chua != chua_mong:
        thieu.append(f"chua_co_du_lieu {chua}≠{chua_mong}")
    return {"thieu": thieu, "lac": [],
            "dai": f"{nhan}: {len(dong)} hàng × 33 cột F…AL · {sum(oc.values())} ô số · {len(dd)} đoạn:khối · cột 0 ô: {len(chua)}"}
