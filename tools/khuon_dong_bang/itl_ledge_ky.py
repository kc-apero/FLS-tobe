"""Khuôn đóng băng `itl_ledge_ky` — ẢNH MANUAL INPUT của `ITL Ledge`, MỘT kỳ MỘT ảnh *(ISP 3.1.2 · DT12 · `WO-265`)*.

    python tools/dong_bang_sheet.py itl_ledge_ky <bản_thô_kỳ.json> --mong N --ra tests/fixture/dap_an/itl_ledge_<kỳ>.json
    python tools/doc_itl_ledge_ky.py                # đọc sổ + chạy cổng cho MỌI kỳ + ghi `itl_ledge_cac_ky.json`

⭐ **Khuôn CỘT = ảnh 2026-03** *(`tests/fixture/itl_ledge_2026_03.json`, ⛔ đụng)*: `itl_id_sheet · ngay` + 28 cột
của 7 khối × 4 *(Classifying · Manual input · MID · Final)* theo thứ tự sheet `S…AT`; khoá = `dong_sheet` *(hàng sheet)*.
⛔⛔ KHÔNG đọc `Diễn giải` · `Số chứng từ` *(có thể mang tên người)* · `Email Address`: bản thô chỉ gồm cột `A` (ngày),
`R:AT` (ITL ID + 28 cột) và **`tieu_de` — tên 30 cột đúng như hàng 7 + 8 của sổ**; khuôn đòi tên ĐÚNG *(ánh xạ theo TÊN,
⛔ theo vị trí — cột xê dịch thì lệch IM LẶNG)*, và từ chối trước nếu có tên thuộc `CAM`.

⭐ **Khác ảnh 2026-03 — nói thẳng** *(Giả định ở `BG-266`)*: ảnh 2026-03 là JSON thô `{nguon, ky, dong_du_lieu_bat_dau, dong}`
giữ số/chữ nguyên kiểu; ảnh này theo khuôn của `dong_bang_sheet` *(checksum · cổng `--mong` · ô chữ bọc `{"chu": …}`)*.
Nguồn có **cột lẫn số lẫn chữ** *(`svc_*`: số `202603` ở dòng này, chữ `Input here` ở dòng kia — đo 20/11: `svc_start_manual`
10.611 số + 1.396 chữ + 626 rỗng)* mà công cụ đòi MỘT kiểu mỗi cột ⇒ **ô SỐ của 28 cột chọn ghi thành CHỮ số thập phân**
`202603` *(`202603.0` ⇒ `202603`)*; bên đọc `do_voi_so_luong._chuan` chuẩn hoá về chuỗi nên không mất gì. `ngay` = serial → `YYYY-MM-DDT00:00:00`
như ảnh cũ.

⛔ `itl_id_sheet` được mang ĐÚNG `#N/A ()` *(tập `LOI_ITL_ID`)*; mọi lỗi Sheets khác ⇒ TỪ CHỐI.
⛔ Ô RỖNG ở 28 cột chọn là **hợp lệ** *(`chu?` — Manual input rỗng là chính nghĩa "không có tay nhập")*; `itl_id_sheet` · `ngay` ⛔ rỗng.
"""
from __future__ import annotations

import datetime
import pathlib
import re
import sys
from decimal import Decimal
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from fls.canon.o_loi import la_o_loi  # noqa: E402  (một bản khai ô lỗi — `test_CHI_MOT_BAN_KHAI_trong_ca_he`)

BANG = "ITL.Ledge.ManualInput"
KHOA = "dong_sheet"
KIEU_KHOA = "dong_sheet"
KHOI = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
PHAN = ("classifying", "manual", "mid", "final")
COT = ("itl_id_sheet", "ngay", *(f"{k}_{p}" for k in KHOI for p in PHAN))
KIEU_COT = {"itl_id_sheet": "chu", "ngay": "chu", **{c: "chu?" for c in COT[2:]}}
RA = "tests/fixture/dap_an/itl_ledge_mac_dinh.json"      # ⛔ dùng — luôn truyền `--ra` theo kỳ

#: Số lần thử đọc mỗi lát/kỳ trước khi `blocked` *(WO-265 AC-2)*.
so_lan_thu = 3

#: Hàng 7 *(nhãn khối)* — nằm ở cột `V W AA AE AI AM AQ`; hàng 8 *(phân khối)* lặp 7 lần.
NHAN_KHOI = ("Budget Code (HDCode)", "Loại giao dịch (Payment Type)", "Chủ dự toán (CDT1)",
             "Thời điểm bắt đầu sử dụng dịch vụ", "Thời điểm kết thúc sử dụng dịch vụ",
             "Mã đối tác (ID Payee)", "File đính kèm: Hóa đơn")
NHAN_PHAN = ("Classifying", "Manual input", "MID", "Final")
#: Tên 30 cột đúng như sổ *(`A7` · `R7` · `<nhãn khối hàng 7> · <phân khối hàng 8>`)*; bản thô phải khai ĐÚNG.
TIEU_DE = ("ITL ID", "Ngày chứng từ", *(f"{n} · {p}" for n in NHAN_KHOI for p in NHAN_PHAN))
#: Mảnh tên cột CẤM — soát trước mọi thứ *(AC-4)*; `tên` bắt cột kiểu "Tên người nhận"…
CAM = ("diễn giải", "số chứng từ", "số ct", "email address", "tên ")
EPOCH = datetime.date(1899, 12, 30)


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def _chu_so(v: Any) -> str:
    """Số → chuỗi thập phân CHÍNH TẮC: `202603` · `202603.0` ⇒ `202603`; `1.5` ⇒ `1.5` *(⛔ float: qua `Decimal(str())`)*."""
    d = Decimal(str(v))
    return str(int(d)) if d == d.to_integral_value() else format(d.normalize(), "f")


#: ⭐ Ô `itl_id` LỖI mà sổ THẬT mang *(đo 20/11: `R` = `#N/A ()` ở hàng chưa gán ITL ID — 2026-03 cũng có, ảnh cũ giữ
#: nguyên)*: một TẬP ĐÓNG, giữ nguyên chữ, ⛔ xoá; số ô đếm riêng ở `BG`/manifest. Lỗi khác ở BẤT KỲ ô nào ⇒ TỪ CHỐI.
LOI_ITL_ID = ("#N/A ()",)


def _o(v: Any, cho_loi: tuple[str, ...] = ()) -> Any:
    if _rong(v):
        return None
    if isinstance(v, bool):
        raise ValueError("ô là bool — ⛔ đo được")
    if isinstance(v, (int, float, Decimal)):
        return _chu_so(v)
    if isinstance(v, str):
        if la_o_loi(v) and v not in cho_loi:       # `##LẢI NHẬP VỐN#` kế toán gõ tay ⇒ KHÔNG phải lỗi, vẫn là chữ
            raise ValueError("ô là lỗi Sheets — ⛔ đóng băng")
        return v
    raise ValueError(f"ô kiểu {type(v).__name__} — ⛔ đo được")


def chuan_bi(tho: dict[str, Any]) -> dict[str, Any]:
    """Bản thô `{ky, tieu_de, hang:[[dong_sheet, A, R, S…AT(28)]…]}` → bảng công cụ. `ValueError` ⇒ TỪ CHỐI.

    ⛔⛔ Lời lỗi KHÔNG mang giá trị ô."""
    ky, td, hang = tho.get("ky"), tho.get("tieu_de"), tho.get("hang")
    cam = sorted({str(t) for t in (td or []) if any(x in str(t).casefold() + " " for x in CAM)})
    if cam:
        raise ValueError(f"bản thô có cột CẤM {cam} — ⛔ vào ảnh (`Diễn giải` · `Số chứng từ` · `Email Address` · tên người)")
    if tuple(td or ()) != TIEU_DE:
        raise ValueError("`tieu_de` ≠ 30 tên cột của khuôn *(hàng 7 + 8 của sổ)* — cột xê dịch hay sổ đổi bố cục; "
                         "ánh xạ theo TÊN nên ⛔ đóng băng")
    if not (isinstance(ky, str) and len(ky) == 7 and ky[4] == "-" and (ky[:4] + ky[5:]).isdigit()):
        raise ValueError("`ky` phải `YYYY-MM`")
    if not isinstance(hang, list) or not hang or any(not isinstance(h, list) or len(h) != 31 for h in hang):
        raise ValueError("`hang` phải lưới ≥ 1 hàng × 31 ô [dong_sheet, A ngày, R ITL ID, S…AT ×28]")
    dong = []
    for h in hang:
        khoa, a, itl, *cac = h
        if not isinstance(khoa, int) or isinstance(khoa, bool) or khoa < 1:
            raise ValueError("`dong_sheet` phải số nguyên ≥ 1")
        if isinstance(a, bool) or not isinstance(a, (int, float, Decimal)) or a != int(a) or a < 1:
            raise ValueError(f"hàng sheet {khoa}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        ngay = (EPOCH + datetime.timedelta(days=int(a))).isoformat() + "T00:00:00"
        if ngay[:7] != ky:
            raise ValueError(f"hàng sheet {khoa}: ngày thuộc kỳ khác `{ngay[:7]}` ≠ `{ky}` — bản thô lẫn kỳ")
        dong.append([khoa, _o(itl, LOI_ITL_ID), ngay, *(_o(x) for x in cac)])
    return {"cot": [KHOA, *COT], "dong": dong,
            "ghi_chu": (f"ITL Ledge · kỳ {ky}: {len(dong)} hàng theo cột A *(ngày)*; chỉ `A` · `R:AT` = itl_id + 28 cột của "
                        "7 khối. ⛔⛔ BỎ `Diễn giải` · `Số chứng từ` *(có thể chứa tên người)* · `Email Address`. Ô SỐ ghi "
                        "thành CHỮ số thập phân *(cột lẫn số/chữ — xem docstring khuôn)*; `ngay` = serial → ISO như ảnh 2026-03.")}


def _u(v: Any) -> Any:
    return v.get("chu") if isinstance(v, dict) else v


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Thiếu = hàng sheet vắng GIỮA min…max · Lạc = hàng có ngày khác kỳ của đa số. Cả hai phải rỗng ở sổ này
    *(đo 20/11: mỗi kỳ là MỘT khối hàng liên tục — sổ xếp theo ngày)*; ⛔ ghi nhận như lạc của `ix_fx`: lạc ⇒ cổng ĐỎ vì
    một ảnh một kỳ mà lẫn kỳ là ảnh hỏng."""
    if not dong:
        raise ValueError("ảnh rỗng — ⛔ đo được (Đ3)")
    hang = sorted(int(str(_u(r["dong_sheet"]))) for r in dong)
    co = set(hang)
    thieu = [n for n in range(hang[0], hang[-1] + 1) if n not in co]
    ky = [str(_u(r["ngay"]))[:7] for r in dong]
    chinh = max(set(ky), key=ky.count)
    lac = [str(_u(r["dong_sheet"])) for r, k in zip(dong, ky) if k != chinh]
    return {"thieu": thieu, "lac": lac, "dai": f"hàng sheet {hang[0]}…{hang[-1]} · kỳ {chinh}"}


def phan_loai_ky(doc: dict[str, int | None], mong: int) -> dict[str, Any]:
    """Cổng kỳ: `doc[kỳ]` = số dòng đọc được, `None` = hỏng sau `so_lan_thu` lần ⇒ `blocked` CÓ TÊN.
    ĐẠT ⇔ ≥ 1 kỳ · đọc được + hỏng = `mong` · hỏng = 0. Tập rỗng ⇒ ĐỎ *(Đ3)*."""
    doc_duoc = {k: n for k, n in doc.items() if n is not None}
    hong = {k: "blocked" for k, n in doc.items() if n is None}
    ly_do = []
    if not doc:
        ly_do.append("tập kỳ rỗng — ⛔ đo được (Đ3)")
    if len(doc) != mong:
        ly_do.append(f"đọc được {len(doc_duoc)} + hỏng {len(hong)} = {len(doc)} ≠ mong {mong}")
    if hong:
        ly_do.append(f"{len(hong)} kỳ blocked: {sorted(hong)}")
    return {"doc_duoc": doc_duoc, "hong": hong, "dat": not ly_do, "ly_do": ly_do}


def tho_mau() -> dict[str, Any]:
    """Bản thô NHỎ, dữ liệu GIẢ *(⛔ từ sổ)* — cho bài chiều ĐỎ: 2 hàng · kỳ 2026-04."""
    serial = (datetime.date(2026, 4, 1) - EPOCH).days
    ma = [["Need to manual input", "x", "x", "x"]] * 3 + [[202604, 202604.0, 202604, "Input here"]] * 4
    c28 = [v for b in ma for v in b]
    return {"nguon": "mau-gia", "doc_luc": "2026-11-20", "cach_doc": "mẫu giả", "ky": "2026-04",
            "tieu_de": list(TIEU_DE),
            "hang": [[10 + i, serial + i, f"ITL#{i}", *c28] for i in range(2)]}


# ══════════════════════════════════════════════════════════════════════════════════════════════
# ⭐ CHUẨN HOÁ ẢNH về ĐÚNG HÌNH ảnh 2026-03 *(`KQ-267` · `DT12-R1-01` · orchestrator quyết phương án (a))*
# Lý do: ảnh `dong_bang_sheet` mang `{bang, khuon, cot, cong, checksum…, dong:[{thu_tu, dong_sheet:"7049", ô:{"chu": …}}]}`;
# bước đọc H15 *(`do_voi_so_luong._nap` + `_chuan`)* viết cho ảnh 2026-03 `{nguon, ky, dong_du_lieu_bat_dau, so_dong, ghi_chu,
# dong:[{dong_sheet:int, ô phẳng}]}` ⇒ trên ảnh `{"chu"}` thì `d["ky"]` KeyError và `_chuan({"chu": …})` ra CHUỖI DICT
# `"{'chu': …}"` — hai lỗi mà AC-5 cũ *(chỉ `json.loads`)* KHÔNG thấy. Ảnh ghi ra = hình 2026-03; cổng · checksum · cột
# sống ở `itl_ledge_cac_ky.json` *(manifest)*; `ve_dang_cong` là phép NGƯỢC để tính lại checksum *(khứ hồi)*.
KHOA_ANH = ("nguon", "ky", "dong_du_lieu_bat_dau", "so_dong", "ghi_chu", "dong")      # thứ tự khoá cấp trên của ảnh 2026-03
#: Hàng dữ liệu đầu của SỔ *(ảnh 2026-03: `10` — hàng 7·8 tiêu đề, 9 trống)*, ⛔ hàng đầu của kỳ.
HANG_DAU_SO = 10
#: Cột mà nguồn LẪN số lẫn chữ *(`svc_*`)* — chỉ ở đây ô chữ-số **trả lại SỐ** *(ảnh 2026-03: `svc_start_manual` 149 số + 435 chữ)*.
#: ⛔ cột khác: `id_payee_*` có vài ô toàn chữ số mà là MÃ *(chữ)*.
COT_SO = tuple(c for c in COT if c.startswith(("svc_start_", "svc_end_")))
_RE_SO = re.compile(r"^-?\d+(\.\d+)?$", re.ASCII)


def _tra_so(v: str) -> int | float:
    return int(v) if "." not in v else float(v)


def chuan_hoa_anh(cong: dict[str, Any], hang_dau_so: int = HANG_DAU_SO) -> dict[str, Any]:
    """Ảnh của `dong_bang_sheet` *(`{"chu"}`, `thu_tu`)* → ảnh HÌNH 2026-03. Chỉ ĐỔI HÌNH: ô chữ gỡ `{"chu"}`; ô chữ-số của
    `COT_SO` trả lại số; `dong_sheet` → số nguyên; ô rỗng giữ `None`. ⛔ bỏ/thêm dòng·ô *(`ValueError` nếu ảnh vào hỏng hình)*."""
    dong = cong.get("dong")
    if not dong or cong.get("so_dong") != len(dong):
        raise ValueError("ảnh cổng rỗng hoặc `so_dong` ≠ số dòng — ⛔ chuẩn hoá (Đ3)")
    ra = []
    for r in dong:
        o: dict[str, Any] = {"dong_sheet": int(_u(r["dong_sheet"]))}
        for c in COT:
            v = _u(r[c])
            if v is not None and not isinstance(v, str):
                raise ValueError(f"cột `{c}`: ô kiểu {type(v).__name__} — ảnh cổng chỉ có chữ/rỗng")
            o[c] = _tra_so(v) if (c in COT_SO and v is not None and _RE_SO.match(v)) else v
        ra.append(o)
    ky = str(ra[0]["ngay"])[:7]
    return {"nguon": cong["nguon"], "ky": ky, "dong_du_lieu_bat_dau": hang_dau_so, "so_dong": len(ra),
            "ghi_chu": cong.get("ghi_chu_khuon", ""), "dong": ra}


def ve_dang_cong(anh: dict[str, Any]) -> list[dict[str, Any]]:
    """Phép NGƯỢC của `chuan_hoa_anh`: ảnh hình 2026-03 → dòng dạng cổng *(`thu_tu` · `dong_sheet` chữ · ô `{"chu"}`)* để
    `AnhChup.checksum()` tính lại ⇒ so với checksum ghim = bằng chứng khứ hồi 100 % ô."""
    ra = []
    for i, r in enumerate(anh["dong"], 1):
        o: dict[str, Any] = {"thu_tu": i, "dong_sheet": str(r["dong_sheet"])}
        for c in COT:
            v = r[c]
            o[c] = None if v is None else {"chu": _chu_so(v) if isinstance(v, (int, float)) else v}
        ra.append(o)
    return ra


def _kieu(v: Any) -> str:
    return "rỗng" if v is None else "số" if isinstance(v, (int, float)) and not isinstance(v, bool) else type(v).__name__


def loi_hinh(anh: dict[str, Any], mau: dict[str, Any]) -> list[str]:
    """So HÌNH `anh` với `mau` *(ảnh 2026-03)*: khoá cấp trên *(tập + thứ tự)* · khoá dòng · KIỂU ô từng cột ⊆ kiểu của mẫu *(chữ/số; rỗng ở đâu cũng được)* ·
    `dong_sheet` số · ⛔ ô `dict` ở đâu cả. `[]` = đúng hình; mỗi lỗi một câu, ⛔ mang giá trị ô."""
    loi = []
    if list(anh) != list(mau):
        loi.append(f"khoá cấp trên {list(anh)} ≠ {list(mau)}")
    if not isinstance(anh.get("dong"), list) or not anh.get("dong"):
        return [*loi, "`dong` rỗng/không phải danh sách — ⛔ đo được (Đ3)"]
    khoa_dong = list(mau["dong"][0])
    kieu_mau: dict[str, set[str]] = {c: set() for c in khoa_dong}
    for r in mau["dong"]:
        for c in khoa_dong:
            kieu_mau[c].add(_kieu(r[c]))
    sai_khoa = sai_kieu = 0
    ghi: dict[str, set[str]] = {}
    for r in anh["dong"]:
        if list(r) != khoa_dong:
            sai_khoa += 1
            continue
        for c in khoa_dong:
            k = _kieu(r[c])
            if k != "rỗng" and k not in kieu_mau[c]:       # ô RỖNG hợp lệ ở mọi cột *(khuôn `chu?` — sổ thật có ô trống ở cột mà 2026-03 đầy)*
                sai_kieu += 1
                ghi.setdefault(c, set()).add(k)
    if sai_khoa:
        loi.append(f"{sai_khoa} dòng có khoá ≠ ảnh 2026-03")
    if sai_kieu:
        loi.append(f"{sai_kieu} ô sai KIỂU so với ảnh 2026-03 ở cột {sorted(ghi)} (kiểu lạ: {sorted(set().union(*ghi.values()))})")
    return loi
