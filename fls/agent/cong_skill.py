# -*- coding: utf-8 -*-
"""Cổng RA của từng skill — skill `n+1` chỉ chạy khi cổng của skill `n` ĐẠT (`WO-329` AC-2).

Mỗi cổng là hàm thuần `(ra, tham, ngu_canh) → (dat, ly_do)`:
  ra        đầu ra AGENT của skill `{mã ô: giá trị}` (sau khi đọc câu trả lời mô hình)
  tham      chuỗi sau dấu `:` trong khai `cong:` của tệp skill
  ngu_canh  `{"cong_cu": <kết quả công cụ phía MÁY, chưa che>}` — để soát luật cứng (ghép theo nội dung)
⭐ Mọi cổng ĐỎ khi mẫu số 0 (Đ3) và khi một ô cần số mà ⛔ phải số (phép ⛔ đo được = ĐỎ, Đ5).
⛔ Cổng ⛔ so với số máy đã đo — đó là việc của A4 (`doi_chieu.py`), chạy SAU cả agent. Cổng skill chỉ
   soát TỰ NHẤT QUÁN của đầu ra (Σ kỳ = tổng · khớp ≤ mẫu · luật cứng) — bắt lỗi sớm, có TÊN chỗ dừng.
"""
from __future__ import annotations

from typing import Any, Callable

Cong = Callable[[dict[str, Any], str, dict[str, Any]], tuple[bool, str]]


def _so(v: Any) -> bool:
    return isinstance(v, (int, float)) and not isinstance(v, bool)


def _rong(ra: dict) -> tuple[bool, str] | None:
    if not ra:
        return False, "0 ô đầu ra ⇒ ⛔ đo được gì (Đ3)"
    return None


def _so_het(ra: dict, ma_list: list[str]) -> str | None:
    hong = [m for m in ma_list if not _so(ra.get(m))]
    return f"{len(hong)} ô cần SỐ mà ⛔ phải số: {hong[:3]}" if hong else None


def cong_khop_khai(ra, tham, nc):
    """A1 · KS.RI: mỗi nguồn `nguon:<x>.dem_dong` (máy đếm dòng ảnh) = `nguon:<x>.so_dong` (ảnh tự khai)."""
    r = _rong(ra)
    if r:
        return r
    nguon = sorted({m.split(":")[1].split(".")[0] for m in ra if m.startswith("nguon:")})
    ly = []
    for n in nguon:
        a, b = ra.get(f"nguon:{n}.dem_dong"), ra.get(f"nguon:{n}.so_dong")
        if not (_so(a) and _so(b)):
            ly.append(f"{n}: thiếu dem_dong/so_dong")
        elif a != b or a <= 0:
            ly.append(f"{n}: Σ dòng ảnh {a} ≠ khai {b}" if a != b else f"{n}: 0 dòng (Đ3)")
    mong = [x for x in tham.split("+") if x]
    if mong and sorted(mong) != nguon:
        ly.append(f"nguồn {nguon} ≠ mong {sorted(mong)}")
    return (not ly), " · ".join(ly) or f"{len(nguon)} nguồn: Σ dòng ảnh = khai"


def cong_tong_ky(ra, tham, nc):
    """Σ `voi:theo_ky.*.<f>` = `voi:tong.<f>` cho từng trường `f` trong `tham` (phân cách `+`)."""
    r = _rong(ra)
    if r:
        return r
    ly = []
    for f in [x for x in tham.split("+") if x]:
        tong = ra.get(f"voi:tong.{f}")
        ky = [v for m, v in ra.items() if m.startswith("voi:theo_ky.") and m.endswith(f".{f}")]
        if not _so(tong) or not ky:
            ly.append(f"{f}: ⛔ đo được (tổng {tong!r} · {len(ky)} kỳ)")
        elif any(not _so(v) for v in ky) or sum(ky) != tong:
            ly.append(f"{f}: Σ {len(ky)} kỳ = {sum(v for v in ky if _so(v))} ≠ tổng {tong}")
    return (not ly), " · ".join(ly) or f"Σ kỳ = tổng ({tham})"


def cong_khop_le_mau(ra, tham, nc):
    """Mỗi cặp `<a>_khop ≤ <a>` (cùng tiền tố) và mọi ô là số; `tham` = các `a` (phân cách `+`)."""
    r = _rong(ra)
    if r:
        return r
    ly = []
    for a in [x for x in tham.split("+") if x]:
        cap = [(m, m.replace(f".{a}", f".{a}_khop")) for m in ra if m.endswith(f".{a}")]
        if not cap:
            ly.append(f"{a}: 0 cặp (Đ3)")
        for m, mk in cap:
            v, vk = ra.get(m), ra.get(mk)
            if not (_so(v) and _so(vk)):
                ly.append(f"{m}: ⛔ số")
            elif vk > v:
                ly.append(f"{mk} {vk} > mẫu {v}")
    return (not ly), " · ".join(ly[:5]) or f"khớp ≤ mẫu ({tham})"


def cong_so_khong_am(ra, tham, nc):
    """Mọi ô là số ≥ 0 (danh sách số cũng được), mẫu số > 0."""
    r = _rong(ra)
    if r:
        return r
    hong = []
    for m, v in ra.items():
        vs = v if isinstance(v, list) else [v]
        if not vs or any(not _so(x) or x < 0 for x in vs):
            hong.append(m)
    return (not hong), (f"{len(hong)} ô ⛔ phải số ≥ 0: {hong[:3]}" if hong else f"{len(ra)} ô số ≥ 0")


def cong_van_tay(ra, tham, nc):
    """A1 · vân tay: mỗi `nguon:<x>.van_tay` là 16 hex; `voi:nguon.checksum.*` cũng vậy."""
    r = _rong(ra)
    if r:
        return r
    hong = [m for m, v in ra.items() if (m.endswith(".van_tay") or ".checksum." in m)
            and not (isinstance(v, str) and len(v) == 16 and all(c in "0123456789abcdef" for c in v))]
    return (not hong), (f"vân tay hỏng: {hong}" if hong else "vân tay 16 hex đủ")


def cong_cong_doc(ra, tham, nc):
    """Ô `cong:<mã>.dat` phải bool hoặc null (null = chưa đo — hiện, ⛔ coi xanh); ô số phải số."""
    r = _rong(ra)
    if r:
        return r
    hong = [m for m, v in ra.items() if m.endswith(".dat") and v is not None and not isinstance(v, bool)]
    hong += [m for m, v in ra.items() if not m.endswith(".dat") and not (_so(v) or isinstance(v, list))]
    return (not hong), (f"ô cổng hỏng kiểu: {hong[:3]}" if hong else f"{len(ra)} ô cổng đọc được")


def cong_hd2_dem(ra, tham, nc):
    """HD2 mỗi gói: `khop ≤ tong_o`, `tong_o > 0` (Đ3)."""
    r = _rong(ra)
    if r:
        return r
    goi = sorted({m.split(":")[1].split(".")[0] for m in ra if m.endswith(".tong_o")})
    ly = []
    for g in goi:
        o, k = ra.get(f"hd2:{g}.tong_o"), ra.get(f"hd2:{g}.khop")
        if not (_so(o) and _so(k)) or o <= 0 or k > o:
            ly.append(f"{g}: khớp {k} / ô {o}")
    if not goi:
        ly.append("0 gói (Đ3)")
    return (not ly), " · ".join(ly) or f"{len(goi)} gói: khớp ≤ ô so, ô so > 0"


def cong_luat_ghep(ra, tham, nc):
    """A2 · ghép theo NỘI DUNG — LUẬT CỨNG (`INV-I16`: ⛔ đoán) trên MỖI ca agent chọn một PM line:
       · PM line phải là ỨNG VIÊN công cụ đưa ra cho đúng ca ấy;
       · cùng tiền tệ, |tiền bank − tiền line| ≤ dung sai (1.000 VND · 0 tiền tệ khác — AP §4.3.1);
       · một PM line ⛔ được chọn cho hai ca.
       Ca chọn `DE_NGUOI` luôn hợp lệ (để người là lựa chọn an toàn). Mẫu số = số ca (Đ3)."""
    cc = nc.get("cong_cu") or {}
    ca = sorted({m.split(":")[1].split(".")[0] for m in cc if m.startswith("noi:")})
    if not ca:
        return False, "0 ca trong công cụ ⇒ ⛔ đo được (Đ3)"
    ly, dung = [], {}
    for c in ca:
        chon = ra.get(f"noi:{c}.chon")
        if chon is None:
            ly.append(f"{c}: agent ⛔ trả `chon`")
            continue
        if chon == "DE_NGUOI":
            continue
        uv = {}
        i = 0
        while f"noi:{c}.uv.{i}.pm" in cc:
            uv[cc[f"noi:{c}.uv.{i}.pm"]] = (cc.get(f"noi:{c}.uv.{i}.tien"), cc.get(f"noi:{c}.uv.{i}.cur"))
            i += 1
        if chon not in uv:
            ly.append(f"{c}: `{chon}` ⛔ là ứng viên")
            continue
        tien, cur = uv[chon]
        bt, bc = cc.get(f"noi:{c}.tien"), cc.get(f"noi:{c}.cur")
        ds = 1000 if bc == "VND" else 0
        if cur != bc or not (_so(tien) and _so(bt)) or abs(tien - bt) > ds:
            ly.append(f"{c}: `{chon}` lệch tiền/tiền tệ (luật cứng)")
        if chon in dung:
            ly.append(f"{c}: `{chon}` đã chọn cho {dung[chon]}")
        dung[chon] = c
    return (not ly), " · ".join(ly[:5]) or f"{len(ca)} ca: 0 vi phạm luật cứng"


CONG: dict[str, Cong] = {
    "khop_khai": cong_khop_khai, "tong_ky": cong_tong_ky, "khop_le_mau": cong_khop_le_mau,
    "so_khong_am": cong_so_khong_am, "van_tay": cong_van_tay, "cong_doc": cong_cong_doc,
    "hd2_dem": cong_hd2_dem, "luat_ghep": cong_luat_ghep,
}


def chay_cong(khai: str, ra: dict[str, Any], ngu_canh: dict[str, Any]) -> tuple[bool, str]:
    ten, _, tham = khai.partition(":")
    if ten not in CONG:
        return False, f"cổng `{ten}` ⛔ có trong sổ cổng"
    return CONG[ten](ra, tham, ngu_canh)
