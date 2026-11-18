"""Bộ máy CHUNG cho hai khuôn CFA1 — `cfa1_daily` *(PD 409)* · `cfa1_yhqm` *(PD 410)*.

⭐ **Vì sao MỘT tệp dùng chung** *(ISP 3.1.2 · DT5 · `WO-137` AC-4: "⛔ sửa công cụ trừ khi bài
đòi")*. Hai sheet `Report I CFA1 Daily` và `Report I CFA1 Y H Q M` có **cùng** bố cục cây HD
*(5 khối LE × 74 mã, 6 nhóm HDO…HDCI, cột L1…L4 ở B…E)*; chỉ khác TRỤC cột: Daily = NGÀY *(serial
từ G5)*, Y/H/Q/M = KỲ *(Year/Half/Quarter/Month)*. Phần CHUNG — phân loại hàng, dựng cây (cha =
thụt cột trong khối LE), bóc ô giá trị thưa — ở đây; phần RIÊNG *(trục cột, cắt tương lai)* ở hai
khuôn. Tên tệp bắt đầu `_` ⇒ `danh_sach_khuon()` của công cụ BỎ QUA *(⛔ phải một khuôn)*.

⛔⛔ **⛔ sửa `dong_bang_sheet.py`** *(bài ⛔ đòi — khai lý do, `WO-137` AC-4)*. Ảnh CFA1 là LƯỚI
HD × trục rất rộng *(370 × 760 ô ngày)*, ⛔ hợp mô hình "một hàng một thực thể, cột vô hướng" của
công cụ. Nhưng công cụ **đã đủ** nhờ:
  · Ô giá trị **≠ 0** ⇒ một DÒNG CHÍNH thưa `{o_id, le, ma_hd, <trục>, gt}` *(o_id = khoá ghép
    `le#ma#nhãn`, kiểu `ma`)*; ô = 0 ⇒ BỎ *(vắng ⇒ 0 — H5 so "ô so > 0")*.
  · Ô **⛔ số** *(`"-"`, `#REF!`, `#N/A`…)* ⇒ bảng phụ **`o_loi`** *(giữ NGUYÊN chuỗi, ĐẾM, ⛔ hoá
    0 — AC-3)*; ⛔ vào dòng chính, ⛔ hoá đỏ *(ô lỗi là NGUỒN, ⛔ phải lỗi đọc)*.
  · Cây HD đầy đủ *(mọi mã kể cả nút cha, cả 5 LE)* ⇒ bảng phụ **`hd`** *(370 dòng)*.
  · Trục cột *(đã cắt tương lai)* ⇒ bảng phụ **`ngay_truc`**/`ky_truc` *(Đ5: `PHU_MONG` khai số)*.
Nhờ vậy giữ `ix_fx` + 3 ảnh DT3 + `gl_406` ĐÚNG TỪNG BYTE *(công cụ ⛔ đụng)*.

⭐ **Năm bất biến — `ValueError` ⇒ TỪ CHỐI** *(⛔ đóng băng một ảnh sai)*:
  ① **5 khối LE** *(GROUP · SGO2 · SGO1 · HGO6 · BGO2)*, mỗi khối ĐÚNG 74 mã *(= cây ATL)*; khối
     nhận ra bằng hàng nhóm `HDO` có MÃ LE ở cột A.
  ② **Trục cột LIÊN TỤC** *(ngày: serial kề nhau; kỳ: đủ Y/H/Q/M mỗi năm)* — hụt một lát ⇒ TỪ CHỐI
     *(AC-4: "lát rỗng/hỏng ⇒ ĐỎ")*.
  ③ **Cột tương lai** *(ngày > ngày đọc; năm > năm đọc)* phải TOÀN 0 — bằng chứng cắt chúng là an
     toàn *(sheet sinh sẵn cột rỗng tới 2027-01)*; có ô ≠ 0 ⇒ TỪ CHỐI.
  ④ **Dòng `khac`** *(ô canh `CHECK ZONE`…)* chỉ được nằm SAU dữ liệu mỗi khối — giữa bảng ⇒ TỪ
     CHỐI *(rác lọt bảng — như `atl_cay`)*.
  ⑤ Mã HD ∈ cây ATL: ⛔ ở đây — là **cổng** `thieu_lac` *(Đ5, `DT5-B2` chứng minh đỏ)*.
"""
from __future__ import annotations

import datetime
import json
import pathlib
import re
import sys
from decimal import Decimal
from typing import Any, Callable

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from fls.adapters.pm_join import PM_COT_RIENG_TU  # noqa: E402

EPOCH = datetime.date(1899, 12, 30)
#: 5 khối Legal Entity của CFA1 *(CF THEO LE — AP v3.1.2 §3.5.1)*, thứ tự như sheet. Khai MỘT chỗ.
LE = ("GROUP", "SGO2", "SGO1", "HGO6", "BGO2")
#: 6 nhóm HD *(= `atl_cay.NHOM`)* — mỗi khối LE lặp đủ 6 nhóm.
NHOM = ("HDO", "HDH", "HDAP", "HDT", "HDC", "HDCI")
_TACH = " | "
_MA_NHOM = re.compile(r"[A-Z][A-Z0-9]*")


def ngay_tu_serial(serial: int) -> datetime.date:
    """Serial Google Sheets *(1899-12-30 = 0)* → ngày."""
    return EPOCH + datetime.timedelta(days=int(serial))


def _o(row: list, i: int) -> Any:
    """Ô thô cột `i` *(hay None nếu thiếu/rỗng-chuỗi)* — giữ kiểu gốc *(số · chuỗi · bool)*."""
    v = row[i] if i < len(row) else None
    if v is None:
        return None
    if isinstance(v, str) and not v.strip():
        return None
    return v


def _chuoi(row: list, i: int) -> str | None:
    v = _o(row, i)
    return v if isinstance(v, str) and v.strip() else None


def _la_so(v: Any) -> bool:
    #: Công cụ đọc bản thô với `parse_float=Decimal` ⇒ số thực là `Decimal` *(⛔ `float`)*; số
    #: nguyên vẫn `int`. Cả hai là SỐ; `bool` thì ⛔.
    return isinstance(v, (int, Decimal)) and not isinstance(v, bool)


#: Ô CẤU TRÚC an toàn để hiện trong lời lỗi: mã/nhãn/token lỗi ngắn — chữ, số và vài dấu của mã
#: `#REF!`, `#DIV/0!`, `-`. ⛔ khớp email *(có `@`)* hay tên *(có khoảng trắng)*.
_O_AN_TOAN = re.compile(r"[#A-Za-z0-9/.!?\-]{1,16}")


def _an_toan(v: Any) -> str:
    """Hiện ô trong lời lỗi mà ⛔ rò GIÁ TRỊ bản thô có thể mang PII *(bia `DT5-R1-02`)*.

    Số ⛔ bao giờ là PII *(PII là tên · email = CHUỖI)* ⇒ hiện nguyên. Chuỗi: chỉ hiện khi là
    MÃ/NHÃN ngắn `[#A-Za-z0-9/.!?\\-]{1,16}` *(mã LE · nhóm · token lỗi)*; còn lại *(email có `@`,
    tên có khoảng trắng, chuỗi dài)* ⇒ CHE, chỉ nói loại + độ dài.
    """
    if v is None:
        return "∅"
    if isinstance(v, bool):
        return str(v)
    if _la_so(v):
        return str(v)
    if isinstance(v, str) and _O_AN_TOAN.fullmatch(v):
        return v
    n = len(v) if isinstance(v, str) else len(str(v))
    return f"⟨{type(v).__name__}·{n} ký tự ⛔ hiện⟩"


def _loai_hang(row: list) -> tuple[str, int | None]:
    """Phân loại hàng lưới từ CHÍNH ô `B…E` *(⛔ nhãn dựng sẵn — như `atl_cay`)* →
    (`ma`|`nhom`|`trong`|`khac`, cột nhãn `B=1…E=4`)."""
    nhan = [j for j in range(1, 5) if isinstance(_chuoi(row, j), str) and _TACH in _chuoi(row, j)]
    if len(nhan) == 1:
        return "ma", nhan[0]
    b, c, d, e = (_chuoi(row, j) for j in range(1, 5))
    if not nhan and b and _MA_NHOM.fullmatch(b) and c and not d and not e:
        return "nhom", None
    if not any(_chuoi(row, j) for j in range(1, 5)):
        return "trong", None
    return "khac", None


def soat_pii_luoi(values: list[list]) -> None:
    """⛔ TỪ CHỐI khi lưới mang tên cột PII *(`PM_COT_RIENG_TU` — vd `Email Address`)*.

    ⚠ Bản thô CFA1 là **LƯỚI** *(⛔ trường `cot`)* ⇒ phép soát của công cụ *(`_soat_rieng_tu`)*
    ⛔ thấy tiêu đề nguồn; khuôn soát lấy: quét MỌI ô của 7 hàng tiêu đề *(nơi một cột PII sẽ có
    đầu đề)* + 6 cột nhãn `A…F` của mọi hàng. So sau khi gộp khoảng trắng, ⛔ phân biệt hoa thường.
    ⛔ in giá trị ô.
    """
    cam = {" ".join(str(c).split()).casefold() for c in PM_COT_RIENG_TU}

    def trung(v: Any) -> bool:
        return isinstance(v, str) and " ".join(v.split()).casefold() in cam

    for i, r in enumerate(values):
        for j, v in enumerate(r):
            if (i < 7 or j < 6) and trung(v):
                raise ValueError(f"lưới có đầu đề thuộc PM_COT_RIENG_TU {sorted(PM_COT_RIENG_TU)} "
                                 f"ở hàng {i + 1} cột {j + 1} — cột ấy ⛔ vào kho nên ⛔ vào ảnh; "
                                 "bỏ cột khỏi lượt đọc rồi đóng băng lại")


def dung_cay(values: list[list]) -> list[dict[str, Any]]:
    """Lưới → danh sách hàng HD `{le, ma, ten, cha, cap, nhom, dong_sheet}` theo thứ tự sheet.

    Bất biến ① ④ ⑤ *(`ValueError` ⇒ TỪ CHỐI)*. `cha` = thụt cột TRONG khối LE *(ngăn xếp, nhóm
    xoá ngăn, dòng trống ⛔ đụng — hệt `atl_cay`)*. ⛔ kiểm cha–con/chu trình *(C4)*; chỉ GHI quan
    hệ thụt cột.
    """
    hdo = [i for i, r in enumerate(values)
           if _loai_hang(r)[0] == "nhom" and _chuoi(r, 1) == "HDO"]
    if len(hdo) != len(LE):
        raise ValueError(f"thấy {len(hdo)} hàng nhóm HDO ≠ {len(LE)} khối LE "
                         f"*(mỗi khối LE mở bằng một hàng HDO có mã LE ở cột A)*")
    ra: list[dict[str, Any]] = []
    for bi, start in enumerate(hdo):
        end = hdo[bi + 1] if bi + 1 < len(hdo) else len(values)
        le = _chuoi(values[start], 0)
        if le != LE[bi]:
            # ⛔ `{le!r}` — ô cột A có thể mang PII *(bia `DT5-R1-02`)*; hiện qua `_an_toan`.
            raise ValueError(f"khối {bi} *(hàng sheet {start + 1}, cột A)*: mã LE = "
                             f"{_an_toan(le)} ≠ mong {LE[bi]!r} *(thứ tự khối LE là {list(LE)})*")
        ngan: list[tuple[int, str]] = []
        nhom_hien: str | None = None
        du_lieu_xong = False
        n_ma = 0
        for i in range(start, end):
            r = values[i]
            lo, col = _loai_hang(r)
            dong_sheet = i + 1
            if lo == "trong":
                continue
            if lo == "khac":
                # ④ ô canh *(CHECK ZONE…)* chỉ SAU dữ liệu của khối
                du_lieu_xong = True
                continue
            if du_lieu_xong:
                raise ValueError(f"dòng sheet {dong_sheet} *(khối {le})*: dữ liệu `{lo}` nằm SAU "
                                 "vùng canh/CHECK ZONE — rác lọt giữa bảng")
            if lo == "nhom":
                nhom_hien = _chuoi(r, 1)
                if nhom_hien not in NHOM:
                    # ⛔ `{nhom_hien!r}` — ô cột B có thể mang PII *(bia `DT5-R1-02`)*.
                    raise ValueError(f"dòng sheet {dong_sheet}: nhóm {_an_toan(nhom_hien)} ⛔ thuộc "
                                     f"{list(NHOM)} *(AP v3.1.2 §3.2.5)*")
                ngan = []
                continue
            # ⚠ Cột F ở sheet này ⛔ LẶP nhãn tất định *(đo: dòng NCF 69 có F RỖNG)* ⇒ ⛔ canh F;
            #   phân loại chỉ dựa B…E *(`_loai_hang`)*.
            nhan = _chuoi(r, col)                      # lo == "ma"
            ma, ten = (x.strip() for x in nhan.split(_TACH, 1))
            if not ma or not ten:
                raise ValueError(f"dòng sheet {dong_sheet}: `MÃ | Tên` thiếu mã hoặc tên")
            if nhom_hien is None:
                raise ValueError(f"dòng sheet {dong_sheet}: dòng mã trước tiêu đề nhóm đầu")
            cap = col
            while ngan and ngan[-1][0] >= cap:
                ngan.pop()
            ra.append({"le": le, "ma": ma, "ten": ten,
                       "cha": ngan[-1][1] if ngan else None,
                       "cap": cap, "nhom": nhom_hien, "dong_sheet": dong_sheet})
            ngan.append((cap, ma))
            n_ma += 1
        if n_ma != 74:
            raise ValueError(f"khối {le}: {n_ma} mã HD ≠ 74 *(cây ATL)*")
    return ra


def kiem_tuong_lai_rong(values: list[list], hd: list[dict], cot_tuong_lai: list[int]) -> int:
    """③ Mọi cột tương lai *(chỉ số ở `cot_tuong_lai`)* phải TOÀN 0/rỗng trên mọi hàng HD; ô ≠ 0
    ⇒ `ValueError` *(⛔ dám cắt)*. Trả số cột tương lai đã kiểm."""
    for d in hd:
        r = values[d["dong_sheet"] - 1]
        for j in cot_tuong_lai:
            v = _o(r, j)
            if v is not None and not (_la_so(v) and v == 0):
                raise ValueError(f"cột tương lai {j} *(dòng sheet {d['dong_sheet']})* có ô ≠ 0 "
                                 "⇒ ⛔ cắt được — trục cột phải dừng ở ngày/năm đọc")
    return len(cot_tuong_lai)


GOC = pathlib.Path(__file__).resolve().parents[2]
#: Nguồn cây ATL — GỌI *(đọc)*, ⛔ chép: đổi cây thì cổng đổi theo *(như `gl_406` gọi `phan_bo`)*.
NGUON_CAY = GOC / "tests" / "fixture" / "cau_hinh" / "atl_cay.json"


def ma_cay_atl() -> set[str]:
    """Tập mã HD của `atl_cay.json` *(74)*. Thiếu/hỏng ⇒ `ValueError` ⇒ cổng ĐỎ *(Đ3)*."""
    try:
        j = json.loads(NGUON_CAY.read_text(encoding="utf-8"))
        ma = {(d["ma"]["chu"] if isinstance(d["ma"], dict) else d["ma"]) for d in j["dong"]}
        if not ma:
            raise ValueError("rỗng")
        return ma
    except (OSError, ValueError, KeyError, TypeError) as e:
        raise ValueError(f"⛔ đọc được cây ATL từ {NGUON_CAY.name}: "
                         f"{type(e).__name__}: {e}") from None


def _chu_cua(v: Any) -> str:
    return v["chu"].strip() if isinstance(v, dict) else str(v)


#: NGỮ CẢNH của lượt `chuan_bi` gần nhất — `chuan_bi` GHI *(cuối hàm)*, cổng `cong_hd` ĐỌC.
#:
#: ⭐ **Vì sao một global** *(bia `DT5-R1-01` · `-04`)*. Cổng của công cụ CHUNG có hợp đồng cứng
#: `thieu_lac(dong)` *(⛔ đổi — DT2/DT3/DT4 dùng chung)*; `dong` chỉ là DÒNG CHÍNH *(ô ≠ 0)* ⇒
#: cổng MÙ trên **164/370 hàng HD toàn-0** *(lạ/vắng/trùng ở hàng toàn-0 lọt qua ĐẠT — `F-1`)*,
#: và cũng ⛔ thấy `o_loi`. Cây ĐẦY ĐỦ `phu.hd` + phân bố `o_loi` nằm ở đây, do `chuan_bi` dựng
#: NGAY TRƯỚC khi cổng chạy *(cùng tiến trình: `_chuan_bi` → `_thieu_lac` trong `dong_bang`)*.
#: Mỗi lần đóng băng là MỘT tiến trình con *(bài gọi `subprocess`)* ⇒ ⛔ nhiễm chéo. `chuan_bi`
#: nổ trước khi ghi ⇒ cổng ⛔ chạy *(⛔ dùng ngữ cảnh cũ)*.
_NGU_CANH: dict[str, Any] | None = None


def ghi_ngu_canh(hd: list[dict[str, Any]], o_loi: list[dict[str, Any]],
                 o_loi_gia_mong: dict[str, int]) -> None:
    """`chuan_bi` GHI cây đầy đủ + ô lỗi + bản khai phân bố lỗi cho cổng `cong_hd` đọc."""
    global _NGU_CANH
    _NGU_CANH = {"hd": hd, "o_loi": o_loi, "o_loi_gia_mong": dict(o_loi_gia_mong)}


def cong_hd(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Cổng DT5-B1/B2 *(Đ5)* DÙNG CHUNG hai khuôn. ĐỎ *(`thieu` ⛔ rỗng)* khi một trong:

      ⒜ mã HD ở DÒNG CHÍNH *(ô ≠ 0)* ⛔ ∈ cây ATL, hoặc LE ⛔ ∈ 5 khối *(giữ hành vi cũ —
         mã lạ ở hàng CÓ số ĐỎ ngay, kể cả khi thiếu ngữ cảnh)*;
      ⒝ CÂY ĐẦY ĐỦ `phu.hd`: MỖI khối LE ⇒ tập mã == cây ATL 74 **CHÍNH XÁC** *(lạ · vắng · trùng
         đều ĐỎ)* — ⒜ một mình MÙ trên **164/370** hàng toàn-0 *(bia `DT5-R1-01`)*; nêu mẫu số
         hàng toàn-0 *(Đ3)*;
      ⒞ phân bố ô lỗi `o_loi` == **bản khai** `o_loi_gia` *(thêm `#REF!` hay đổi tập ⇒ ĐỎ — bia
         `DT5-R1-04`, Đ5: sửa một chỗ cũng ĐỎ, buộc ghi lại bản khai)*.

    ⛔ `lac` *(thứ tự là dữ liệu)*. Nguồn cây hỏng, hay THIẾU ngữ cảnh ⇒ ĐỎ *(Đ3/Đ5: ⛔ đo được
    = ĐỎ)*."""
    from collections import Counter
    cay = ma_cay_atl()                                        # ValueError ⇒ ⛔ đo được
    thieu: list[str] = []
    # ⒜ dòng chính thưa — mẫu số hàng CÓ số là tập (LE, mã) xuất hiện ở `dong`.
    co_so: set[tuple[str, str]] = set()
    ma_co: list[str] = []
    le_co: list[str] = []
    for d in dong:
        m, l = _chu_cua(d["ma_hd"]), _chu_cua(d["le"])
        co_so.add((l, m))
        if m not in ma_co:
            ma_co.append(m)
        if l not in le_co:
            le_co.append(l)
    thieu += sorted(m for m in ma_co if m not in cay)
    thieu += [f"LE_la@{l}" for l in sorted(l for l in le_co if l not in LE)]
    # ⒝⒞ cây ĐẦY ĐỦ + phân bố o_loi — ngữ cảnh `chuan_bi` dựng (cùng tiến trình)
    nc = _NGU_CANH
    toan_0: int | None = None
    n_khai: int | None = None
    if nc is None:
        thieu.append("NGU_CANH@thiếu")                        # Đ5: ⛔ đo được = ĐỎ
    else:
        hd = nc["hd"]
        for le in LE:
            ma_khoi = [_chu_cua(r["ma"]) for r in hd if _chu_cua(r["le"]) == le]
            c = Counter(ma_khoi)
            thieu += [f"{le}:lạ@{m}" for m in sorted(m for m in c if m not in cay)]
            thieu += [f"{le}:trùng@{m}" for m in sorted(m for m, n in c.items() if n > 1)]
            thieu += [f"{le}:vắng@{m}" for m in sorted(cay - set(ma_khoi))]
        rows = {(_chu_cua(r["le"]), _chu_cua(r["ma"])) for r in hd}
        toan_0 = sum(1 for r in rows if r not in co_so)       # Đ3: mẫu số hàng toàn-0
        thuc = Counter(_chu_cua(x["gia"]) for x in nc["o_loi"])
        mong = nc["o_loi_gia_mong"]
        n_khai = sum(mong.values())
        if dict(thuc) != dict(mong):
            def _d(m: dict) -> str:
                return "{" + ", ".join(f"{_an_toan(k)}:{v}" for k, v in sorted(m.items())) + "}"
            thieu.append(f"o_loi_gia@khác: khai {_d(mong)} ≠ thực {_d(dict(thuc))}")
    dai = (f"{len(ma_co)} mã HD *(trên dòng chính ≠ 0)* · cây đầy đủ "
           f"{'?' if nc is None else len(nc['hd'])} hàng, mỗi khối == ATL {len(cay)} · hàng "
           f"toàn-0 {'?' if toan_0 is None else toan_0} *(Đ3 mẫu số)* · o_loi khai "
           f"{'?' if n_khai is None else n_khai} · {len(le_co)} LE ∈ {list(LE)} · nguồn "
           f"{NGUON_CAY.name}")
    return {"thieu": thieu, "lac": [], "dai": dai}


def boc_o(values: list[list], hd: list[dict], cot_giu: list[tuple[int, str, Any]],
          ten_truc: str) -> tuple[list[list], list[dict]]:
    """Bóc ô giá trị THƯA từ các cột giữ `[(chỉ_số_cột, nhãn_o_id, giá_trị_trục)]`.

    → (dong_chinh, o_loi). `nhãn_o_id` *(chuỗi)* đi vào khoá ghép `o_id`; `giá_trị_trục` là Ô của
    cột trục trong ảnh *(Daily: serial INT ⇒ cột `so`; Y/H/Q/M: khoá kỳ CHUỖI ⇒ cột `chu`)*.
    Ô số ≠ 0 ⇒ `[o_id, le, ma, giá_trị_trục, gt]` *(thứ tự `[KHOA, *COT]`)*; ô ⛔ số *(chuỗi ·
    bool)* ⇒ `{le, ma_hd, <ten_truc>, gia}` vào `o_loi` *(AC-3)*; ô 0/rỗng ⇒ BỎ *(vắng ⇒ 0)*.
    """
    dong: list[list] = []
    o_loi: list[dict] = []
    for d in hd:
        le, ma = d["le"], d["ma"]
        r = values[d["dong_sheet"] - 1]
        for j, nhan, truc in cot_giu:
            v = _o(r, j)
            if v is None:
                continue
            o_id = f"{le}#{ma}#{nhan}"
            if _la_so(v):
                if v != 0:
                    dong.append([o_id, le, ma, truc, v])
            else:                                      # chuỗi *(`"-"`, `#REF!`…)* hay bool
                o_loi.append({"le": le, "ma_hd": ma, ten_truc: truc, "gia": v})
    return dong, o_loi
