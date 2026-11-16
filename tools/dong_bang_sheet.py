"""ĐÓNG BĂNG một bản đọc giá trị sheet thành ẢNH có checksum + cổng *(ISP 3.1.2 · DT2)*.

    python tools/dong_bang_sheet.py <khuôn> <bản_thô.json> --mong N [--ra <tệp>]
    python tools/dong_bang_sheet.py ix_fx  <bản_thô.json> --mong 37
        ⇒ tests/fixture/cau_hinh/ix_fx.json

Exit: **0** cổng ĐẠT · **1** cổng ĐỎ *(ảnh VẪN ghi — đúng như nguồn)* · **2** TỪ CHỐI *(⛔ ghi,
⛔ tạo thư mục, tệp có sẵn ⛔ bị đụng; đúng MỘT dòng `⛔ TỪ CHỐI …` ở stderr)*.

⭐ **Vì sao có tệp này.** AP v3.1.2 §3.2.4 ghi chỗ AS-IS gõ cứng của bảng tỷ giá
`9.2.Exchange Rate` *(APERO | FS2, nhập tay; CF · P&L · A-CCR đều `IMPORTRANGE` nó)* và hậu quả
đã thấy: *"tháng thiếu ⇒ SUMIFS = 0 ⇒ mất số không báo; tháng nhập hai dòng ⇒ cộng đôi"*. Bước
sau *(C1 kiểm tỷ giá · C5 nạp kho)* cần một ẢNH đứng yên — đọc MỘT lần, đóng băng có checksum,
và một cổng **in ra** tháng thiếu/trùng/lạc thay vì im lặng. Khuôn là *cột chọn + khoá* nên
dùng lại được cho các ảnh DT3…DT11: thêm một dòng vào `KHUON`, ⛔ viết công cụ thứ hai.

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
    ghi thành **chuỗi đúng chữ số của JSON thô** — ⛔ làm tròn, ⛔ định dạng lại.

  ② **Thứ tự hàng là DỮ LIỆU.** `AnhChup.checksum()` cố ý độc lập thứ tự đọc *(đọc dần/cắt
    lát)*. Nhưng ở sheet này dòng `202306` chỉ "lạc" vì nó đứng **sau** `202512` ⇒ mỗi dòng
    mang `thu_tu` *(vị trí 1-based trong bản đọc, ⛔ số hàng sheet — bản thô ⛔ khai hàng tiêu
    đề)* ⇒ đổi chỗ hai hàng là đổi checksum.

  ③ **`ngay_dong_bang` = `doc_luc` của bản thô**, ⛔ đồng hồ máy. Ảnh là của MỘT ngày đọc;
    lấy ngày từ bản thô thì chạy lại công cụ ra **đúng từng byte** ⇒ ảnh đã commit kiểm được
    bằng cách tái tạo *(bài `test_DT2_B1_anh_IX_FX_TAI_TAO_…`)*.

  ④ **Riêng tư từ chối CHẶT hơn nguồn khai.** Bản thô có một cột thuộc `PM_COT_RIENG_TU` ⇒
    TỪ CHỐI cả lượt, **kể cả khi khuôn ⛔ chọn cột ấy**. Tên so sau khi gộp khoảng trắng *(như
    `pm_join.loc_tho`)* **và** ⛔ phân biệt hoa thường. ⛔ In giá trị của cột ấy ở bất cứ đâu.

  ⑤ **Cổng khai `mong` (Đ5) — và đếm dòng thôi là CHƯA ĐỦ.** 37 dòng mà `202409` bị nhập thành
    `202408` lần hai thì đếm dòng vẫn khớp — đúng ca *"cộng đôi"* của AP §3.2.4. ⇒ ĐỎ khi: số
    dòng ≠ `--mong` *(cả thừa lẫn thiếu)* · khoá trùng · tháng thiếu trong dải · khoá ⛔ phải
    `yyyymm` · ô rỗng ở cột chọn. **Lạc thì GHI NHẬN, ⛔ đỏ**: AP §3.2.1 đo bảng thật *"37 dòng
    202401 → 202612 (kể cả dòng lạc 202306)"* — đó là nguồn, ⛔ phải lỗi đọc; kiểm nghiệp vụ
    tỷ giá *(VND = 1, tháng hiệu lực)* là việc của C1.

Luật của lạc/thiếu *(khoá `yyyymm`)*, ghi ra để bước sau đừng đoán:
  · **lạc**  = hàng có khoá **nhỏ hơn** khoá lớn nhất đứng trước nó *(theo thứ tự sheet)*.
  · **thiếu** = tháng nằm giữa khoá nhỏ nhất và lớn nhất của các hàng **⛔ lạc** mà ⛔ hàng nào
    *(kể cả hàng lạc)* mang. ⚠ Dòng lạc đứng ĐẦU bảng thì ⛔ bị gọi lạc — dải chính kéo về nó và
    các tháng ở giữa hiện thành **thiếu** ⇒ vẫn ĐỎ, ⛔ im lặng.
  · **trùng** = khoá xuất hiện ≥ 2 lần *(liệt kê một lần, tăng dần)*.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Any

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.adapters.pm_join import PM_COT_RIENG_TU  # noqa: E402
from fls.oracle.anh_chup import AnhChup           # noqa: E402


@dataclass(frozen=True)
class Khuon:
    """Một khuôn đóng băng: chọn cột nào, khoá nào, ghi ra đâu.

    ⛔ Ánh xạ cột theo **TÊN**, ⛔ theo vị trí *(bài học `pm_join.loc_tho`: cột xê dịch thì bản
    khai vị trí lệch IM LẶNG, còn tên thì ⛔)*.
    """
    ten: str
    bang: str
    khoa: str
    kieu_khoa: str          # chỉ `yyyymm` — kiểu khác ⇒ thêm khi có bước cần, ⛔ khai trước
    cot: tuple[str, ...]
    ra: str                 # tương đối với gốc repo


KHUON: dict[str, Khuon] = {
    # AP v3.1.2 §3.2.1 IX.FX: tháng yyyymm × USD · SGD · COP · VND (=1) · HKD
    "ix_fx": Khuon(ten="ix_fx", bang="IX.FX", khoa="Month", kieu_khoa="yyyymm",
                   cot=("USD", "SGD", "COP", "VND", "HKD"),
                   ra="tests/fixture/cau_hinh/ix_fx.json"),
}

_YYYYMM = re.compile(r"\d{6}")


class TuChoi(Exception):
    """Đầu vào ⛔ dùng được ⇒ exit 2, ⛔ ghi gì."""


# ── đọc ───────────────────────────────────────────────────────────────────────

def _ten(c: Any) -> str:
    """Tên cột gộp khoảng trắng — đúng phép của `pm_join.loc_tho`."""
    return " ".join(str("" if c is None else c).split())


def _o(v: Any) -> Any:
    """Ô thô → giá trị ảnh. Số ⇒ **chuỗi đúng chữ số** của JSON thô *(quyết định ①)*."""
    if v is None or isinstance(v, (bool, str)):
        return v
    if isinstance(v, (int, Decimal)):
        return str(v)
    raise TuChoi(f"ô kiểu {type(v).__name__} ⛔ phải số/chuỗi/rỗng")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and not v.strip())


def _khong_hang_so(c: str) -> Any:
    raise TuChoi(f"bản thô có hằng `{c}` ⛔ phải số JSON")


def doc_ban_tho(p: Path) -> dict:
    if not p.is_file():
        raise TuChoi(f"⛔ thấy bản thô `{p}`")
    try:
        tho = json.loads(p.read_text(encoding="utf-8"), parse_float=Decimal,
                         parse_constant=_khong_hang_so)
    except json.JSONDecodeError as e:
        raise TuChoi(f"bản thô ⛔ phải JSON: {e}") from None
    if not isinstance(tho, dict):
        raise TuChoi("bản thô phải là một đối tượng `{nguon, doc_luc, cach_doc, cot, dong}`")
    for k in ("nguon", "doc_luc", "cach_doc"):
        if not isinstance(tho.get(k), str) or not tho[k].strip():
            raise TuChoi(f"bản thô thiếu `{k}` *(chuỗi)* — ảnh ⛔ có xuất xứ thì ⛔ đóng băng")
    try:
        date.fromisoformat(tho["doc_luc"])
    except ValueError:
        raise TuChoi(f"`doc_luc` ⛔ phải ngày ISO: {tho['doc_luc']!r}") from None
    if not isinstance(tho.get("cot"), list) or not isinstance(tho.get("dong"), list):
        raise TuChoi("bản thô thiếu `cot` *(danh sách)* hoặc `dong` *(danh sách hàng)*")
    return tho


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


def _thang_ke(t: str) -> str:
    n, m = int(t[:4]), int(t[4:])
    return f"{n + 1}01" if m == 12 else f"{n}{m + 1:02d}"


def _khoa_hop_le(v: Any) -> bool:
    return isinstance(v, str) and bool(_YYYYMM.fullmatch(v)) and 1 <= int(v[4:]) <= 12


def phan_tich_khoa(khoa: list[Any]) -> dict[str, Any]:
    """Khoá theo THỨ TỰ SHEET → hỏng · trùng · lạc · thiếu *(luật ở docstring tệp)*."""
    hong = [k for k in khoa if not _khoa_hop_le(k)]
    tot = [k for k in khoa if _khoa_hop_le(k)]

    dem: dict[str, int] = {}
    for k in tot:
        dem[k] = dem.get(k, 0) + 1
    trung = sorted(k for k, n in dem.items() if n >= 2)

    lac: list[str] = []
    chinh: list[str] = []
    lon_nhat = ""
    for k in tot:
        if lon_nhat and k < lon_nhat:
            lac.append(k)
        else:
            chinh.append(k)
            lon_nhat = k

    thieu: list[str] = []
    if chinh:
        co = set(tot)
        t, het = min(chinh), max(chinh)
        while t <= het:
            if t not in co:
                thieu.append(t)
            t = _thang_ke(t)
    dai = f"{min(chinh)}→{max(chinh)}" if chinh else "∅"
    return {"khoa_hong": hong, "trung": trung, "lac": lac, "thieu": thieu, "dai": dai}


def dong_bang(kh: Khuon, tho: dict, mong: int) -> tuple[dict, list[str]]:
    """Bản thô đã đọc → (ảnh, các dòng báo). ⛔ Ghi gì — `main` ghi.

    ⛔ Mọi `TuChoi` phải nổ ở ĐÂY, trước khi chạm đĩa.
    """
    cot = [_ten(c) for c in tho["cot"]]
    _soat_rieng_tu(tho["cot"])                       # ⛔ trước mọi thứ đọc giá trị

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

    dong: list[dict[str, Any]] = []
    for i, h in enumerate(tho["dong"], 1):
        if not isinstance(h, list):
            raise TuChoi(f"dòng {i} ⛔ phải danh sách ô")
        if len(h) > len(cot):
            raise TuChoi(f"dòng {i} có {len(h)} ô > {len(cot)} cột tiêu đề — ô ngoài tiêu đề "
                         "sẽ mất im lặng")
        d: dict[str, Any] = {"thu_tu": i}
        for c in can:
            j = vi_tri[c]
            d[c] = _o(h[j]) if j < len(h) else None
        dong.append(d)

    pt = phan_tich_khoa([d[kh.khoa] for d in dong])
    o_rong = [{"thu_tu": d["thu_tu"], "cot": c}
              for d in dong for c in kh.cot if _rong(d[c])]
    mau_o = len(dong) * len(kh.cot)

    ly_do: list[str] = []
    if len(dong) != mong:
        ly_do.append(f"{len(dong)} dòng ≠ mong {mong}")
    for ten, nhan_ in (("trung", "trùng"), ("thieu", "thiếu"), ("khoa_hong", "khoá hỏng")):
        if pt[ten]:
            ly_do.append(f"{nhan_} {len(pt[ten])}")
    if o_rong:
        ly_do.append(f"ô rỗng {len(o_rong)}/{mau_o}")

    ngay = tho["doc_luc"]
    checksum = AnhChup(run_id=f"dong_bang_sheet:{kh.ten}", ngay=date.fromisoformat(ngay),
                       nguon=tho["nguon"], dong=tuple(dong)).checksum()[:16]
    khong_chon = [c for c in cot if c and c not in can]
    rieng_tu = sorted(PM_COT_RIENG_TU)

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
            f"{len(khong_chon)} cột bản thô ⛔ chọn (tên ở `cot_khong_chon`)."),
        "khoa": kh.khoa,
        "kieu_khoa": kh.kieu_khoa,
        "cot": list(kh.cot),
        "cot_khong_chon": khong_chon,
        "so_dong": len(dong),
        "trung": pt["trung"],
        "thieu": pt["thieu"],
        "lac": pt["lac"],
        "khoa_hong": pt["khoa_hong"],
        "o_rong": o_rong,
        "cong": {"mong": mong, "so_dong": len(dong), "dat": not ly_do, "ly_do": ly_do},
        "checksum_noi_dung": checksum,
        "dong": dong,
    }

    def ds(xs: list) -> str:
        return "[" + ", ".join("∅" if x is None else str(x) for x in xs) + "]"

    o_in = " ".join(f"[dòng {o['thu_tu']} · {o['cot']}]" for o in o_rong[:10])
    bao = [
        f"══ dong_bang_sheet · {kh.ten} ({kh.bang})",
        f"  nguồn      : {tho['nguon']}",
        f"  cách đọc   : {tho['cach_doc']}",
        f"  ngày đọc   : {ngay}  (= ngay_dong_bang)",
        f"  bản thô    : {len(cot)} cột · {len(dong)} dòng",
        f"  soát PII   : {len(cot)}/{len(cot)} tên cột · 0 thuộc PM_COT_RIENG_TU {rieng_tu}",
        f"  cột chọn   : khoá {kh.khoa} + {len(kh.cot)} {list(kh.cot)} · "
        f"⛔ chọn {len(khong_chon)} {khong_chon}",
        f"  khoá hỏng: {ds(pt['khoa_hong'])}  ({len(pt['khoa_hong'])}/{len(dong)} dòng)",
        f"  ô rỗng: {len(o_rong)}/{mau_o}  ({len(dong)} dòng × {len(kh.cot)} cột) {o_in}".rstrip(),
        f"  trùng: {ds(pt['trung'])}",
        f"  thiếu: {ds(pt['thieu'])}  (dải chính {pt['dai']})",
        f"  lạc: {ds(pt['lac'])}  (khoá nhỏ hơn khoá lớn nhất đứng trước — ghi nhận, ⛔ đỏ)",
        f"  checksum_noi_dung: {checksum}",
    ]
    return anh, bao


# ── ghi ───────────────────────────────────────────────────────────────────────

def _ghi(p: Path, noi_dung: str) -> None:
    """Ghi NGUYÊN TỬ: tệp tạm cùng thư mục rồi `os.replace` — ⛔ để lại ảnh ghi dở."""
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


class _Lenh(argparse.ArgumentParser):
    """argparse nhưng lỗi đối số ⇒ `TuChoi` *(một dòng, exit 2)* — `S0-R1-03`: mọi đối số ⛔
    khai đều bị từ chối, ⛔ chỉ đối số đầu."""

    def error(self, message: str):        # type: ignore[override]
        raise TuChoi(f"đối số: {message}")


def _lenh() -> _Lenh:
    p = _Lenh(prog="dong_bang_sheet.py",
              description="Đóng băng bản đọc giá trị sheet thành ảnh có checksum + cổng.")
    p.add_argument("khuon", choices=sorted(KHUON), help="khuôn đóng băng")
    p.add_argument("ban_tho", type=Path, help="JSON {nguon, doc_luc, cach_doc, cot, dong}")
    p.add_argument("--mong", type=int, required=True,
                   help="số dòng MONG — khác ⇒ exit 1 (Đ5: cổng phải khai mong)")
    p.add_argument("--ra", type=Path, default=None,
                   help="tệp ảnh ra (mặc định: đường của khuôn, tương đối gốc repo)")
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        a = _lenh().parse_args(argv)
        if a.mong < 1:
            raise TuChoi(f"--mong {a.mong} — cổng mong 0 dòng là cổng xanh trên tập rỗng (Đ3)")
        kh = KHUON[a.khuon]
        anh, bao = dong_bang(kh, doc_ban_tho(a.ban_tho), a.mong)
    except TuChoi as e:
        print("⛔ TỪ CHỐI: " + " ".join(str(e).split()) + " — ⛔ ghi tệp nào", file=sys.stderr)
        return 2

    ra = a.ra if a.ra is not None else GOC / kh.ra
    _ghi(ra, json.dumps(anh, ensure_ascii=False, indent=1) + "\n")
    try:
        hien = ra.resolve().relative_to(GOC)
    except ValueError:
        hien = ra
    print("\n".join(bao))
    print(f"  ghi        : {hien}")
    c = anh["cong"]
    if c["dat"]:
        print(f"[ĐẠT] cổng --mong {c['mong']}: {c['so_dong']} dòng = mong · trùng 0 · thiếu 0 · "
              f"khoá hỏng 0 · ô rỗng 0/{c['so_dong'] * len(kh.cot)}")
        return 0
    print(f"[ĐỎ] cổng --mong {c['mong']}: " + " · ".join(c["ly_do"])
          + " — ảnh đã ghi ĐÚNG NGUỒN, ⛔ sửa; ⛔ dùng ảnh này khi cổng chưa đạt")
    return 1


if __name__ == "__main__":
    sys.exit(main())
