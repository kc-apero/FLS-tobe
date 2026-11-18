"""Bộ máy CHUNG cho ba khuôn GL HR — `gl_hr_407` · `gl_hr_408` · `gl_hr_413`.

⭐ **Vì sao MỘT tệp dùng chung** *(ISP 3.1.2 · Step 23 · DT6 · `WO-192` AC-5: "khuôn mới = tệp
riêng, ⛔ sửa công cụ chung")*. Ba sheet `Report I H1000 Ledge (HR Allocate HD) Y2025` *(PD 407)*,
`… | For PL Report` ở sổ CF *(PD 408)* và ở sổ P&L *(PD 413)* có **cùng** bố cục cột `A…BO`
*(`A` Ngày chứng từ · `D` tiền tệ · `E`/`F` PS Nợ/Có · `G` Tài khoản · `H` Payment Type · `I`
HDCode · `J` CDT1 · `P` LE · `R` ITL ID · `V`/`Z`/`AD` cột Final · `AX…BC` CALC ZONE)*; chỉ khác
SỐ DÒNG và VÙNG A-RỖNG. Phần CHUNG — soát tiêu đề, bóc hàng, che số tài khoản, cổng — ở đây;
phần RIÊNG *(kỳ mong, lỗi mong, đoạn trống mong)* ở ba khuôn. Tên tệp bắt đầu `_` ⇒ `danh_sach_
khuon()` BỎ QUA *(⛔ phải một khuôn)*. ⛔ sửa `dong_bang_sheet.py`: bài ⛔ đòi — khuôn dùng đủ
`KIEU_KHOA="dong_sheet"` + `KIEU_COT` `so?`/`chu?` + `PHU_MONG` sẵn có.

⛔⛔ **Riêng tư** *(`WO-192` AC-2 · HR có tên người)*. Lưới thô đọc bằng khoá SA chỉ-đọc, **bản đồ cột
bằng hàng tiêu đề TRƯỚC**, rồi chỉ đọc các cột ⛔ mang tên người:
  · **BỎ** `B` *(Số chứng từ)* · `C` *(Diễn giải)* · `M` *(Mã đối tác — ID Payee)* · `N`·`O` *(file
    đính kèm)* — ⛔ có trong lưới. Cột `AP` = bản FINAL của `ID Payee` *(`M`)* cũng BỎ *(mã nhân sự
    ⇒ **BỎ**, ⛔ băm: băm một mã nhân sự rồi giữ lại vẫn là định danh ổn định xuyên kỳ)*.
  · **CHE số tài khoản ngân hàng** ở `H`/`Z` *(Payment Type)*: đo 18/11 — 5 giá trị dạng
    `R | <số tài khoản>_<NGÂN HÀNG VND>_<TÊN ĐƠN VỊ>`; ảnh giữ tiền tố `R` *(loại giao dịch)* và
    ⛔ giữ số. Giá trị còn lại *(`Thanh toán (Regular)`)* giữ nguyên.
  · MỌI cột chữ còn lại có **TẬP ĐÓNG** khai ở khuôn *(vài chục mã đo được)*: một giá trị lạ — kể cả
    một tên người rơi lạc cột — ⇒ cổng ĐỎ, ⛔ in giá trị *(chỉ `dong_sheet`, bia `DT5-R1-02`)*.

⭐ **Đ5**: cổng khai `mong` TRƯỚC *(số dòng mỗi kỳ · số ô lỗi theo cột · các đoạn A-rỗng)*, ĐỎ khi
lệch **cả hai chiều**; kỳ ngoài 2025 ⇒ `lac` *(ghi nhận CÓ TÊN, ⛔ im lặng)* và dòng `dai` IN rõ
*"kỳ ⊂ 2025: KHÔNG"* khi đúng như vậy.
"""
from __future__ import annotations

import datetime
import pathlib
import re
import sys
from collections import Counter
from typing import Any

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2]))
from fls.adapters.pm_join import PM_COT_RIENG_TU  # noqa: E402
from fls.canon.o_loi import la_o_loi              # noqa: E402

EPOCH = datetime.date(1899, 12, 30)

#: Cột của lưới thô *(chữ cột sheet, theo thứ tự đọc)* — `values[0]` = hàng sheet `DONG_DAU_SHEET`.
COT_THO = ("A", "D", "E", "F", "G", "H", "I", "J", "P", "Q", "R", "V", "Z", "AD", "AH", "AP",
           "AU", "AV", "AX", "AY", "AZ", "BA", "BB", "BC")
#: Hàng sheet đầu của lưới thô = hàng 7 *(tiêu đề 7·8·9, dữ liệu từ 10)*.
DONG_DAU_SHEET = 7
DONG_DAU_DU_LIEU = 10
#: Cột MANG vào ảnh *(ngoài khoá `dong_sheet`)* — `ky` suy từ `A` *(⛔ mang cột A)*.
COT = ("ky", "D", "E", "F", "G", "H", "I", "J", "P", "R", "V", "Z", "AD",
       "AX", "AY", "AZ", "BA", "BB", "BC")
KHOA = "dong_sheet"
#: Cột CHỮ *(`chu?` — được rỗng)*; `E`·`F`·`AX`·`AY` = số HOẶC rỗng *(`so?`)*; còn lại số *(`so`)*.
CHU = ("D", "G", "H", "I", "J", "P", "R", "V", "Z", "AD")
KIEU_COT = {**{c: "chu?" for c in CHU}, **{c: "so?" for c in ("E", "F", "AX", "AY")}}
#: Cột bị BỎ khỏi ảnh nhưng có trong lưới thô *(khai ở `ghi_chu`)*.
COT_BO = tuple(c for c in COT_THO if c not in COT and c != "A")

#: Tiêu đề kỳ vọng *(ánh xạ theo TÊN, ⛔ theo vị trí)*: cột → (hàng 7, hàng 8, hàng 9). Đo 18/11 ở
#: cả ba sheet; `V`·`Z`·`AD` = bản `Final` của HDCode · Payment Type · CDT1.
TIEU_DE = {
    "A": ("Ngày chứng từ", "", ""), "D": ("Đơn vị tiền tệ", "", ""), "E": ("PS Nợ", "", ""),
    "F": ("PS Có", "", ""), "G": ("Tài khoản", "", ""),
    "H": ("Loại giao dịch (Payment Type)", "", ""), "I": ("Budget Code (HDCode)", "", ""),
    "J": ("Chủ dự toán (CDT1)", "", ""), "P": ("LE", "", ""), "R": ("ITL ID", "", ""),
    "V": ("", "Final", ""), "Z": ("", "Final", ""), "AD": ("", "Final", ""),
    "AX": ("Phát sinh", "PS Nợ", "bVND"), "AY": ("", "PS Có", "bVND"),
    "AZ": ("Tồn", "", "bVND"), "BA": ("Phát sinh", "PS Nợ", "mUSD"),
    "BB": ("", "PS Có", "mUSD"), "BC": ("Tồn", "", "mUSD"),
}

#: TẬP ĐÓNG của các cột chữ *(đo 18/11, hợp 3 sheet)* — ⛔ mang giá trị lạ vào ảnh.
TIEN_TE = ("VND",)
TAI_KHOAN = tuple(f"No {i}" for i in range(1, 26))
PAYMENT_TYPE = ("R", "Thanh toán (Regular)")                       # sau khi CHE số tài khoản
HD_CODE = ("COM | COM Total", "CXA", "CXB", "DC", "GAH", "INT | Insurance Total", "MC",
           "NIS | Net Income Staff", "PI00001-1", "PI00024-4", "PI00371-2", "PI00961-7",
           "PI00961-8", "PI01174-2", "PI01372-2", "PI01372-4", "PIT", "PIT | PIT Total")
CDT1 = ("ASA_Super App (IOs)", "CAH | Astronex", "CAH_Astronex", "CMN_Management",
        "COM | COM Total", "COR | TeraSofts", "COR_TeraSofts", "COR_Terasofts",
        "CSM | SuperMinds", "CSM_SuperMinds", "CVL | VisionLab", "CVL_VisionLab",
        "INT | Insurance Total", "NIS | Net Income Staff", "SHQ1_Headquarters1",
        "SHQ2 | Headquarters2", "SHQ2_Headquarters2")
HD_FINAL = ("COM | COM Total", "CXA | Product Cost In-House Development App",
            "CXB | Biz Development", "DC | Dev Cost (Maintain App)", "GAH | GA HR Cost",
            "INT | Insurance Total", "MC | Maketer Cost", "NIS | Net Income Staff",
            "OGA | GAC - Other", "PIT | PIT Total")
LE = ("VGOH", "VVOH", "VVOS", "VVOT", "VVOV")
TAP_DONG: dict[str, tuple[str, ...]] = {
    "D": TIEN_TE, "G": TAI_KHOAN, "H": PAYMENT_TYPE, "I": HD_CODE, "J": CDT1, "P": LE,
    "V": HD_FINAL, "Z": PAYMENT_TYPE, "AD": CDT1,
}
ITL_ID_RE = re.compile(r"ITL#\d+")
#: Số tài khoản ngân hàng ở Payment Type: `R | <chữ số>_…` ⇒ CHE về tiền tố `R`.
_TK_NGAN_HANG = re.compile(r"(R) \| \d+_.+")

#: Hai tab Y2024 mà `407`/`408` gom bằng `QUERY({…Y2025; …Y2024})` — đi bằng IMPORTRANGE.
TAB_Y2024 = ("H1000 Ledge NIS/INT/COM (HR Allocate HD) Y2024",
             "H1000 Ledge PIT (HR Allocate HD) Y2024")


def _rong(v: Any) -> bool:
    return v is None or (isinstance(v, str) and v == "")


def _la_so(v: Any) -> bool:
    return not isinstance(v, bool) and hasattr(v, "__float__") and not isinstance(v, str)


def che_tai_khoan(v: Any) -> Any:
    """`R | 355…_VPB VND_TÊN` → `R`; giá trị khác giữ nguyên. Trả cả cờ *(đã che?)*."""
    if isinstance(v, str):
        m = _TK_NGAN_HANG.fullmatch(v)
        if m:
            return m.group(1), True
    return v, False


def _soat_pii_tieu_de(values: list[list]) -> None:
    """⛔ TỪ CHỐI khi tiêu đề *(3 hàng đầu, MỌI cột lưới)* trùng `PM_COT_RIENG_TU`. ⛔ in ô."""
    cam = {" ".join(str(c).split()).casefold() for c in PM_COT_RIENG_TU}
    for i, r in enumerate(values[:3]):
        for j, v in enumerate(r):
            if isinstance(v, str) and " ".join(v.split()).casefold() in cam:
                raise ValueError(f"lưới có đầu đề thuộc PM_COT_RIENG_TU {sorted(PM_COT_RIENG_TU)} "
                                 f"ở hàng {i + 1} cột {j + 1} — cột ấy ⛔ vào ảnh; bỏ khỏi "
                                 "lượt đọc rồi đóng băng lại")


# Ngữ cảnh lượt `chuan_bi` gần nhất *(cổng `thieu_lac` có hợp đồng cứng `(dong)` ⇒ ⛔ thấy đoạn
# A-rỗng · số ô che — như `_cfa1._NGU_CANH`)*. Khoá = tên PD ⇒ ba khuôn ⛔ nhiễm chéo.
_NGU_CANH: dict[str, dict[str, Any]] = {}


def chuan_bi(tho: dict[str, Any], pd: str) -> dict[str, Any]:
    """LƯỚI SA → bảng `{dong_sheet, ky, D…BC}` + bảng phụ `doan_trong` · `thieu_nguon`.

    `ValueError` ⇒ TỪ CHỐI. ⛔⛔ lời lỗi KHÔNG mang giá trị ô *(chỉ vị trí/số/loại)*.
    """
    if tho.get("cot_sheet") != list(COT_THO):
        raise ValueError(f"`cot_sheet` phải đúng {list(COT_THO)} *(lưới ⛔ phủ B·C·M·N·O)*")
    if tho.get("dong_dau_sheet") != DONG_DAU_SHEET:
        raise ValueError(f"`dong_dau_sheet` phải {DONG_DAU_SHEET} *(tiêu đề từ hàng 7)*")
    values = tho.get("values")
    if not isinstance(values, list) or len(values) <= 3:
        raise ValueError("`values` phải lưới ≥ 3 hàng tiêu đề + dữ liệu")
    if any(not isinstance(h, list) or len(h) != len(COT_THO) for h in values):
        raise ValueError(f"mọi hàng của `values` phải {len(COT_THO)} ô")
    _soat_pii_tieu_de(values)
    ix = {c: i for i, c in enumerate(COT_THO)}
    for c, mong in TIEU_DE.items():
        thuc = tuple("" if v is None else v for v in (values[0][ix[c]], values[1][ix[c]],
                                                      values[2][ix[c]]))
        if thuc != mong:
            raise ValueError(f"tiêu đề cột {c} (hàng 7·8·9) ≠ bản khai của khuôn — cột xê dịch hay "
                             "sheet đổi bố cục; ánh xạ theo TÊN nên ⛔ đóng băng")
    # ── Y2024: bằng chứng đọc ⛔ được *(AC-3)* ──
    y24 = tho.get("y2024")
    if not isinstance(y24, list) or [x.get("tab") for x in y24 if isinstance(x, dict)] \
            != list(TAB_Y2024):
        raise ValueError(f"`y2024` phải liệt kê đủ 2 tab {list(TAB_Y2024)} *(bằng chứng đọc)*")
    thieu_nguon = []
    for x in y24:
        loai = x.get("loai_o_loi")
        n_doc, n_loi, n_rong, n_gt = (x.get(k) for k in ("so_hang_doc", "so_o_loi", "so_hang_rong",
                                                          "so_hang_co_gia_tri"))
        if not (la_o_loi(loai)) or not all(
                type(n) is int and n >= 0 for n in (n_doc, n_loi, n_rong, n_gt)):
            raise ValueError("`y2024[*]` phải {tab, loai_o_loi:'#…', so_hang_doc, so_o_loi, "
                             "so_hang_rong, so_hang_co_gia_tri} số nguyên ≥ 0")
        if n_gt != 0 or n_loi + n_rong != n_doc:
            raise ValueError("nguồn Y2024 đọc ĐƯỢC *(có hàng giá trị hoặc đếm ⛔ khớp)* ⇒ ⛔ ghi "
                             "`thiếu Y2024` — đóng băng cả phần Y2024 rồi khai lại")
        thieu_nguon.append({"tab": x["tab"], "nguyen_nhan": f"IMPORTRANGE ⇒ {loai}",
                            "so_hang_doc": n_doc, "so_o_loi": n_loi, "so_hang_rong": n_rong,
                            "ghi_chu": "thiếu Y2024 — ⛔ suy, ⛔ hoá 0"})

    dong: list[list[Any]] = []
    doan: list[dict[str, Any]] = []
    cur: dict[str, Any] | None = None
    so_che = 0
    dem_che: Counter = Counter()
    data = values[3:]
    for i, h in enumerate(data):
        ds = DONG_DAU_DU_LIEU + i
        a = h[ix["A"]]
        if _rong(a):
            if cur is None:
                cur = {"tu": ds, "so_hang": 0, "so_hang_co_o_khac": 0, "vi_tri": "giua"}
            cur["so_hang"] += 1
            if any(not _rong(x) for x in h):
                cur["so_hang_co_o_khac"] += 1
            continue
        if cur is not None:
            doan.append(cur)
            cur = None
        if not isinstance(a, int) or isinstance(a, bool) or a < 1:
            raise ValueError(f"hàng sheet {ds}: cột A *(ngày)* phải serial số nguyên ≥ 1")
        d = EPOCH + datetime.timedelta(days=int(a))
        o: dict[str, Any] = {}
        for c in COT[1:]:
            v = h[ix[c]]
            v = None if _rong(v) else v
            if c in ("H", "Z"):
                v, che = che_tai_khoan(v)
                if che:
                    so_che += 1
                    dem_che[c] += 1
            o[c] = v
        dong.append([ds, d.year * 100 + d.month, *(o[c] for c in COT[1:])])
    if cur is not None:
        cur["vi_tri"] = "duoi"
        doan.append(cur)
    if not dong:
        raise ValueError("lưới ⛔ có hàng nào cột A có ngày — ⛔ đóng băng ảnh rỗng (Đ3)")
    _NGU_CANH[pd] = {"doan": [(x["tu"], x["so_hang"], x["so_hang_co_o_khac"], x["vi_tri"])
                              for x in doan]}
    return {
        "cot": [KHOA, *COT],
        "dong": dong,
        "phu": {"doan_trong": doan, "thieu_nguon": thieu_nguon},
        "ghi_chu": (
            f"{pd} *(lưới SA)*: {len(dong)} hàng cột A có ngày, khoá dong_sheet = hàng sheet; "
            f"{len(doan)} đoạn A-RỖNG *(bảng phụ `doan_trong`: "
            f"{sum(1 for x in doan if x['vi_tri'] == 'giua')} giữa dữ liệu · "
            f"{sum(1 for x in doan if x['vi_tri'] == 'duoi')} đuôi)* chứa "
            f"{sum(x['so_hang'] for x in doan)} hàng, "
            f"{sum(x['so_hang_co_o_khac'] for x in doan)} hàng còn ô khác — ĐẾM + khai, ⛔ vào bảng "
            f"chính. ⛔⛔ BỎ cột B Số chứng từ · C Diễn giải · M Mã đối tác · N·O file đính kèm "
            f"(⛔ có trong lưới) và các cột {list(COT_BO)} của lưới: AP = bản Final của ID Payee "
            f"*(mã nhân sự ⇒ BỎ, ⛔ băm)*; Q ⛔ có dữ liệu; AH·AU·AV ⛔ cần cho đáp án. CHE số tài "
            f"khoản ngân hàng ở H·Z: `R | <số>_…` ⇒ `R` *(số ô che khai ở BG, ⛔ vào ảnh)*. ⛔ mang cột "
            f"A — chỉ `ky`. Hai tab Y2024 đi bằng IMPORTRANGE ⇒ thiếu: bảng phụ `thieu_nguon`."),
    }


def _chu(v: Any) -> str | None:
    return None if v is None else (v["chu"] if isinstance(v, dict) else str(v))


def thieu_lac(dong: list[dict[str, Any]], *, pd: str, ky_mong: dict[int, int],
              loi_mong: dict[str, dict[str, int]],
              doan_mong: list[tuple[int, int, int, str]]) -> dict[str, Any]:
    """Cổng GL HR *(Đ5 — khai `mong`, NO cả hai chiều)*. ĐỎ *(`thieu` ⛔ rỗng)* khi:

      ⒜ số dòng mỗi kỳ ≠ `ky_mong` *(thừa · thiếu · kỳ lạ)*;
      ⒝ ô chữ ngoài TẬP ĐÓNG của cột *(PII lạc cột)* / `R` ⛔ khớp `ITL#\\d+` / chứa số tài khoản
         *(≥ 6 chữ số liền ở cột ⛔ phải mã)* — marker chỉ mang `dong_sheet` + cột;
      ⒞ phân bố ô LỖI Sheets theo cột ≠ `loi_mong` *(thêm `#REF!`/đổi tập ⇒ ĐỎ, `DT5-R1-04`)*;
      ⒟ đoạn A-rỗng ≠ `doan_mong` *(thiếu ngữ cảnh ⇒ ĐỎ, Đ3/Đ5)*.

    `lac` = kỳ NGOÀI 2025 *(ghi nhận CÓ TÊN)*. `dai` IN rõ *kỳ ⊂ 2025?* — mỗi số kèm nhãn (Đ4).
    """
    thieu: list[str] = []
    thuc: Counter = Counter(int(d["ky"]) for d in dong)
    for k in sorted(set(thuc) | set(ky_mong)):
        if thuc.get(k, 0) != ky_mong.get(k, 0):
            thieu.append(f"ky@{k}:{thuc.get(k, 0)}/{ky_mong.get(k, 0)}")
    loi: Counter = Counter()
    for d in dong:
        ds = d["dong_sheet"]
        for c in CHU:
            s = _chu(d[c])
            if s is None:
                continue
            if la_o_loi(s):
                loi[(c, s)] += 1
                continue
            if c == "R":
                if not ITL_ID_RE.fullmatch(s):
                    thieu.append(f"R_la@{ds}")
            elif c in TAP_DONG and s not in TAP_DONG[c]:
                thieu.append(f"{c}_la@{ds}")
            elif re.search(r"\d{6,}", s) and c not in ("I",):
                thieu.append(f"{c}_so_dai@{ds}")
    mong_loi = {(c, s): n for c, m in loi_mong.items() for s, n in m.items()}
    if dict(loi) != mong_loi:
        tong = lambda m: sum(m.values())                                   # noqa: E731
        thieu.append(f"o_loi@khác: khai {tong(mong_loi)} ô ≠ thực {tong(loi)} ô "
                     f"({len(mong_loi)} nhóm cột×chuỗi khai ↔ {len(loi)} thực)")
    nc = _NGU_CANH.get(pd)
    if nc is None:
        thieu.append("NGU_CANH@thiếu")                                      # Đ5: ⛔ đo được = ĐỎ
    elif nc["doan"] != list(doan_mong):
        thieu.append(f"doan_trong@khác: khai {len(doan_mong)} đoạn ≠ thực {len(nc['doan'])} đoạn "
                     "(hoặc đổi vị trí/số hàng)")
    ngoai = {k: n for k, n in thuc.items() if k // 100 != 2025}
    lac = [str(k) for k in sorted(ngoai)]
    trong = sum(n for k, n in thuc.items() if k // 100 == 2025)
    dai = (f"kỳ ⊂ 2025: {'CÓ' if not ngoai else 'KHÔNG'} — {len(thuc)} kỳ có dòng "
           f"({sum(1 for k in thuc if k // 100 == 2025)} kỳ ∈ 2025 = {trong} dòng"
           + (f" · {len(ngoai)} kỳ ngoài 2025 {sorted(ngoai)} = {sum(ngoai.values())} dòng" if ngoai
              else "")
           + f") · ô lỗi theo cột {dict(sorted((f'{c}:{s}', n) for (c, s), n in loi.items()))}"
           f" · {0 if nc is None else len(nc['doan'])} đoạn A-rỗng")
    return {"thieu": thieu, "lac": lac, "dai": dai}
