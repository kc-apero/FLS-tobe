"""ĐÁP ÁN CFA1 · `Report I CFA1 Daily` *(409)* + `… Y H Q M` *(410)* — khuôn `cfa1_daily` ·
`cfa1_yhqm` *(ISP 3.1.2 · Step 15 · DT5)*.

⭐ **Vì sao có tệp này.** Bước **H5/H6** *(SO.CFA1 Daily · Y/H/Q/M — AP v3.1.2 §3.3.1 PD 409–410 ·
§3.5.1)* so Σ theo (HD, ngày|kỳ) trên cây IX.HD với đáp án 409/410 TỪNG Ô. H5/H6 cần ẢNH đứng yên
— đọc MỘT lần, đóng băng có checksum, cổng khẳng định **mọi mã HD ∈ cây ATL 74** *(DT5-B1)* và
**số cột ngày = số ngày từ 21/10/2024 tới ngày đọc**. Khuôn dựng ảnh từ LƯỚI SA.

Bài của ISP *(mục 6)* + đối chứng Đ5/AC:

    DT5-B1  đóng băng ⇒ mọi mã HD ∈ cây ATL; số cột ngày = số ngày 2024-10-20…ngày đọc *(khai)*
    DT5-B2  phá: đổi 1 mã HD LẠ ở BẢN SAO ⇒ ĐỎ; trả nguyên ⇒ đúng từng byte
    AC-3    ô ⛔ số nguồn *(`-`, `#REF!`…)* ⇒ bảng phụ `o_loi`: giữ chuỗi, ĐẾM, ⛔ hoá 0, ⛔ đỏ
    AC-4    lát hỏng *(trục ⛔ liên tục · mốc sai · cột tương lai ≠ 0 · PII · thiếu khối LE)* ⇒ ĐỎ

⛔⛔ **Bản đọc thô thật ⛔ nằm trong repo** *(scratchpad orchestrator)*. ⇒ Ảnh thật kiểm bằng
**checksum ghim + khẳng định trường** *(⛔ tái tạo lưới: ảnh THƯA ⛔ dựng lại lưới 458×818)*. Ca
phá dựng **lưới TỔNG HỢP** từ CHÍNH cây ATL *(5 LE × 74)*, ⛔ số thật — đổi/phá rồi chạy lại.

⭐ **Số đo 18/11 *(mỗi số đếm MỘT vật, Đ4)*:** Daily 760 cột ngày *(2024-10-20 … 2026-11-18 LIÊN
TỤC)* · 370 hàng HD *(5 LE × 74)* · 33.355 ô ≠ 0 · 25 ô `"-"`. Y/H/Q/M 57 cột kỳ *(2024–2026 ×
19)* · 5.655 ô ≠ 0 · 25 ô `"-"`. ⚠ Cột ngày đầu 2024-10-20 (CN) sớm 1 ngày so với spec 21/10.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
THU_MUC_KHUON = GOC / "tools" / "khuon_dong_bang"
ANH_D = GOC / "tests" / "fixture" / "dap_an" / "cfa1_daily.json"
ANH_Y = GOC / "tests" / "fixture" / "dap_an" / "cfa1_yhqm.json"
ATL = GOC / "tests" / "fixture" / "cau_hinh" / "atl_cay.json"

#: Checksum ghim ảnh đã commit *(đổi ⇒ phải có lượt đóng băng mới + lý do)* — nền `a8367ed`.
CHECKSUM_D = "6e01ee2b0f2207a3"
CHECKSUM_Y = "ff9e76976cda1401"
EPOCH = datetime.date(1899, 12, 30)
SERIAL_MOC = 45585                        # 2024-10-20 (CN) — cột ngày đầu THẬT của sheet
NGAY_DOC = datetime.date(2026, 11, 18)    # = doc_luc của bản thô SA (ngày đọc)
LE5 = ("GROUP", "SGO2", "SGO1", "HGO6", "BGO2")
MONG_D, OLOI_D, HD_N, NGAY_N = 33355, 25, 370, 760
MONG_Y, OLOI_Y, KY_N = 5655, 25, 57
COT_DAU = 6                               # cột dữ liệu đầu *(sau A…F)* trong lưới tổng hợp

#: ⛔ Đổi 1 byte ảnh cấu hình DT2/DT3 hay đáp án 406 là ĐỎ *(công cụ chung ⛔ đụng ⇒ giữ từng byte)*.
SHA_GIU = {
    "cau_hinh/ix_fx": "e2c9fdd028bd3286",
    "cau_hinh/atl_cay": "504fa53d27c44b83",
    "cau_hinh/cdt_correct": "8d8cfaed26b6aa5a",
    "cau_hinh/mapping_master_cfg": "dc926c1b35b027ef",  # WO-234 19/11: đổi CÓ CHỦ ĐÍCH — che 4 số TK CN → TK_CA_NHAN_<n>
    "dap_an/gl_406": "91987833e9bb15ec",
}


# ── trợ thủ ───────────────────────────────────────────────────────────────────

def _chay(khuon: str, tho: pathlib.Path, mong, ra: pathlib.Path) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), khuon, str(tho), "--mong", str(mong),
                           "--ra", str(ra)], cwd=GOC, env=env, capture_output=True, text=True,
                          timeout=300)


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _chu(v):
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _checksum_lai(anh: dict) -> str:
    """Tính lại bằng CHÍNH `AnhChup` — dòng chính + mọi dòng bảng phụ *(bọc `{"phu","dong"}`)*."""
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _da_tu_choi(kq: subprocess.CompletedProcess, ra: pathlib.Path, dau_moi: str) -> None:
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-800:], kq.stderr[-800:])
    dong = [d for d in kq.stderr.splitlines() if d.startswith("⛔ TỪ CHỐI")]
    assert len(dong) == 1 and dau_moi in kq.stderr, (dau_moi, kq.stderr[-800:])
    assert not ra.exists()


def _ma_cay() -> set[str]:
    return {_chu(d["ma"]) for d in _doc(ATL)["dong"]}


#: Mẫu cột/giá trị PII — quét *(ca phá chứng minh CẮN)*.
_PII = re.compile(r"di[eễ]n\s*gi[aả]i|s[oố]\s*ch[uứ]ng\s*t[uừ]|email", re.IGNORECASE)


def _quet_pii(xs: list[str]) -> list[str]:
    return [c for c in xs if _PII.search(" ".join(str(c).split()))]


# ── lưới TỔNG HỢP từ cây ATL *(5 LE × 74)* — ca phá, ⛔ số thật ─────────────────

_TEN_NHOM = {"HDO": "HD Original", "HDH": "HD HR", "HDAP": "HD Account Payable",
            "HDT": "HD Tempo", "HDC": "HD Calculated", "HDCI": "HD Calculated Internal"}


def _cay_nodes() -> list[dict]:
    """74 nút cây ATL theo thứ tự sheet → [{ma, ten, cap, nhom}]."""
    return [{"ma": _chu(d["ma"]), "ten": _chu(d["ten"]), "cap": int(_chu(d["cap"])),
             "nhom": _chu(d["nhom"])}
            for d in sorted(_doc(ATL)["dong"], key=lambda x: int(_chu(x["dong_sheet"])))]


def _serials(n, start=SERIAL_MOC):
    return [start + i for i in range(n)]


def _wd(s):
    """Nhãn thứ ngày khớp phép `(serial + 6) % 7` của khuôn *(C locale: Sun…Sat)*."""
    return (EPOCH + datetime.timedelta(days=int(s))).strftime("%a")


def _luoi_daily(serials=None, *, gia=None, oloi=None, break_code=None, break_le=None,
                future=(), future_gia=None, extra_col=None, extra_val=None):
    """Lưới CFA1 Daily tổng hợp. `serials=None` ⇒ trục đầy đủ 760 ngày + TỰ 25 ô `"-"` *(khớp
    PHU_MONG cho ca XANH)*; `serials` nhỏ ⇒ lưới gọn *(ca TỪ CHỐI, hỏng trước cổng PHU_MONG)*.
    `gia`/`oloi` = {(le, ma_GỐC, serial): số|chuỗi}; `break_code=(khối, ma_cũ, ma_mới)` đổi NHÃN mã
    *(giữ GIÁ TRỊ gốc ⇒ mã mới vào dòng chính)*; `break_le=(khối, le_mới)`; `extra_col` = cột PII."""
    day_du = serials is None
    serials = _serials(NGAY_N) if day_du else list(serials)
    nodes = _cay_nodes()
    gia = dict(gia or {})
    oloi = dict(oloi or {})
    if day_du and not oloi:                                  # tự 25 ô "-" trên 25 nút CUỐI của GROUP
        for nd in nodes[-OLOI_D:]:
            oloi[("GROUP", nd["ma"], serials[0])] = "-"
    all_ser = serials + list(future)
    nd_cols = len(all_ser)
    px = [extra_col] if extra_col else []                    # đuôi cột PII (nếu có)

    def drow(le, ma):
        row = [0.0] * nd_cols
        for k, s in enumerate(all_ser):
            if (le, ma, s) in gia:
                row[k] = gia[(le, ma, s)]
            elif (le, ma, s) in oloi:
                row[k] = oloi[(le, ma, s)]
            elif s in future and future_gia and (le, ma) in future_gia:
                row[k] = future_gia[(le, ma)]
        return row

    values = [[None] * 5 + [lab] + [0] * nd_cols + ([None] if px else [])
              for lab in ("Year", "Half", "Quarter", "Month")]
    values.append([None] * 5 + ["Day"] + all_ser + px)                       # hàng 5 = Day
    values.append([None, "L1", "L2", "L3", "L4", "Days of the week"]
                  + [_wd(s) for s in all_ser] + px)              # thứ ngày KHỚP serial (DT5-R1-03)
    for bi, le in enumerate(LE5):
        le_hien = break_le[1] if (break_le and break_le[0] == bi) else le
        prev, first = None, True
        for nd in nodes:
            ma, ten, cap, nhom = nd["ma"], nd["ten"], nd["cap"], nd["nhom"]
            if nhom != prev:
                values.append([(le_hien if first else 0), nhom, _TEN_NHOM[nhom], None, None, None]
                              + [0] * nd_cols + ([None] if px else []))
                first, prev = False, nhom
            ma_hien = (break_code[2] if break_code and break_code[0] == bi
                       and ma == break_code[1] else ma)
            row = [1.0, None, None, None, None, None]        # A = mUSD (⛔ vào ảnh)
            row[cap] = f"{ma_hien} | {ten}"
            ev = [extra_val if (le == "GROUP" and ma == "GI" and extra_val is not None) else None] \
                if px else []
            values.append(row + drow(le, ma) + ev)           # GIÁ TRỊ theo ma GỐC
    return {"nguon": "'Report I CFA1 Daily'!A1:TONG_HOP", "doc_luc": NGAY_DOC.isoformat(),
            "cach_doc": "TỔNG HỢP · bài DT5 (⛔ số thật)", "values": values}


def _viet(tmp, raw) -> pathlib.Path:
    p = tmp / "tho.json"
    p.write_text(json.dumps(raw, ensure_ascii=False), encoding="utf-8")
    return p


def _freeze(tmp, raw, mong, ra="a.json"):
    out = tmp / ra
    return _chay("cfa1_daily", _viet(tmp, raw), mong, out), out


# ══ DT5-B1 · ảnh thật (AC-1) ═══════════════════════════════════════════════════

def test_DT5_B1_daily_cau_truc_va_checksum():
    """Ảnh 409 thật: PD.409, khoá ghép `o_id`, 33.355 ô ≠ 0, cổng ĐẠT, checksum ghim. Đ4."""
    a = _doc(ANH_D)
    assert a["bang"] == "PD.409" and a["khoa"] == "o_id" and a["kieu_khoa"] == "ma"
    assert a["cot"] == ["le", "ma_hd", "ngay", "gt"]
    assert a["so_dong"] == len(a["dong"]) == MONG_D
    assert a["cong"] == {"mong": MONG_D, "so_dong": MONG_D, "dat": True, "ly_do": []}
    assert (a["thieu"], a["lac"], a["khoa_hong"], a["o_rong"]) == ([], [], [], [])
    assert a["phu"]["hd"]["so_dong"] == a["phu"]["hd"]["mong"] == HD_N
    assert a["phu"]["ngay_truc"]["so_dong"] == a["phu"]["ngay_truc"]["mong"] == NGAY_N
    assert a["phu"]["o_loi"]["so_dong"] == a["phu"]["o_loi"]["mong"] == OLOI_D
    assert a["ngay_dong_bang"] == NGAY_DOC.isoformat()
    assert a["checksum_noi_dung"] == _checksum_lai(a) == CHECKSUM_D


def test_DT5_B1_daily_moi_ma_HD_trong_cay_ATL():
    """DT5-B1: mọi mã HD của ảnh ∈ cây ATL 74; 5 LE; cây phụ `hd` = 5 × 74 = 370. Đ3: mẫu số > 0."""
    a = _doc(ANH_D)
    cay = _ma_cay()
    assert len(cay) == 74
    ma_dong = {_chu(d["ma_hd"]) for d in a["dong"]}
    assert ma_dong and ma_dong <= cay                     # ⊆ cây (mẫu số > 0)
    assert {_chu(d["le"]) for d in a["dong"]} == set(LE5)
    hd = a["phu"]["hd"]["dong"]
    assert len(hd) == HD_N and {_chu(r["ma"]) for r in hd} == cay      # đủ 74 mã
    from collections import Counter
    assert Counter(_chu(r["le"]) for r in hd) == {le: 74 for le in LE5}


def test_DT5_B1_daily_so_cot_ngay_tu_moc_toi_ngay_doc():
    """DT5-B1: số cột ngày = số ngày từ MỐC tới ngày đọc, LIÊN TỤC; khai ngày đọc. ⚠ mốc THẬT của
    sheet = 2024-10-20 (serial 45585), sớm 1 ngày so với spec 21/10/2024 — ghi rõ, giữ mốc thật."""
    a = _doc(ANH_D)
    sers = [int(_chu(r["ngay"])) for r in a["phu"]["ngay_truc"]["dong"]]
    assert sers[0] == SERIAL_MOC                           # 2024-10-20
    assert sers == list(range(SERIAL_MOC, SERIAL_MOC + len(sers)))   # LIÊN TỤC
    d_dau = EPOCH + datetime.timedelta(days=sers[0])
    d_cuoi = EPOCH + datetime.timedelta(days=sers[-1])
    assert d_dau == datetime.date(2024, 10, 20) and d_cuoi == NGAY_DOC
    assert len(sers) == (NGAY_DOC - d_dau).days + 1 == NGAY_N
    assert (datetime.date(2024, 10, 21) - EPOCH).days in sers        # spec 21/10 PHẢI có mặt
    assert "2024-10-20" in a["ghi_chu_khuon"] and "21/10/2024" in a["ghi_chu_khuon"]


def test_DT5_B1_yhqm_cau_truc_va_checksum():
    """Ảnh 410 thật: PD.410, 5.655 ô ≠ 0, 57 cột kỳ Y/H/Q/M (2024–2026), checksum ghim."""
    a = _doc(ANH_Y)
    assert a["bang"] == "PD.410" and a["cot"] == ["le", "ma_hd", "ky", "gt"]
    assert a["so_dong"] == MONG_Y and a["cong"]["dat"] is True
    assert a["phu"]["hd"]["so_dong"] == HD_N
    assert a["phu"]["ky_truc"]["so_dong"] == a["phu"]["ky_truc"]["mong"] == KY_N
    assert a["phu"]["o_loi"]["so_dong"] == OLOI_Y
    assert {_chu(d["ma_hd"]) for d in a["dong"]} <= _ma_cay()
    assert a["checksum_noi_dung"] == _checksum_lai(a) == CHECKSUM_Y
    loai = {_chu(r["loai"]) for r in a["phu"]["ky_truc"]["dong"]}
    nam = {int(_chu(r["nam"])) for r in a["phu"]["ky_truc"]["dong"]}
    assert loai == {"Y", "H", "Q", "M"} and nam == {2024, 2025, 2026}


# ══ AC-3 · ô ⛔ số nguồn ⇒ bảng phụ o_loi (giữ chuỗi, đếm, ⛔ hoá 0) ════════════

def test_AC3_o_loi_giu_chuoi_dem_khong_hoa_0():
    """AC-3: 25 ô `"-"` ⇒ bảng phụ `o_loi` giữ NGUYÊN chuỗi, ĐẾM, ⛔ hoá 0, ⛔ vào dòng chính, ⛔
    đỏ. Daily + Y/H/Q/M đều 25; ô `gia` ⛔ hiện trong dòng chính *(cột chỉ `le·ma_hd·trục·gt`)*."""
    for anh, oloi_n in ((_doc(ANH_D), OLOI_D), (_doc(ANH_Y), OLOI_Y)):
        ol = anh["phu"]["o_loi"]["dong"]
        assert len(ol) == oloi_n
        assert all(isinstance(r["gia"], dict) and r["gia"]["chu"].strip() for r in ol)
        assert all(r["gia"] != {"chu": "0"} for r in ol)
        assert anh["cong"]["dat"] is True
        assert "gia" not in anh["cot"]                    # ô lỗi ⛔ vào dòng chính


# ══ PII (AC-4) ═════════════════════════════════════════════════════════════════

def test_PII_anh_khong_mang_gia_tri_dinh_danh():
    """AC-4: ảnh ⛔ mang Diễn giải/Số CT/Email — quét MỌI tên khoá + giá trị chữ; Đ3 mẫu số > 0."""
    for anh in (_doc(ANH_D), _doc(ANH_Y)):
        ten = (list(anh) + [anh["khoa"], *anh["cot"]]
               + [k for d in anh["dong"] for k in d]
               + [k for b in anh["phu"].values() for r in b["dong"] for k in r])
        gtri = [_chu(d[c]) for d in anh["dong"] for c in anh["cot"] if isinstance(d.get(c), dict)]
        gtri += [_chu(r.get("ten")) for r in anh["phu"]["hd"]["dong"]]
        assert len(ten) > anh["so_dong"] * 3
        assert _quet_pii(ten) == [] and _quet_pii([g for g in gtri if g]) == []


@pytest.mark.parametrize("xau", ["Diễn giải", "Diễn  giải", "số chứng từ", "Email Address"])
def test_PII_may_quet_CAN_ca_pha(xau):
    """⭐ Ca phá: máy quét PHẢI cắn Diễn giải/Số CT/Email *(⛔ cổng mù — Đ5)*."""
    assert _quet_pii(["le", "ma_hd", xau, "gt"]) == [xau]


def test_PII_ban_tho_co_cot_Email_thi_TU_CHOI(tmp_path):
    """AC-4: lưới thô mang đầu đề `Email Address` ⇒ TỪ CHỐI *(`PM_COT_RIENG_TU`)*, ⛔ ghi, ⛔ in giá
    trị. Lưới gọn 3 ngày — soát PII nổ TRƯỚC mọi thứ."""
    raw = _luoi_daily(_serials(3), extra_col="Email Address", extra_val="nguoi@vi-du.invalid")
    kq, ra = _freeze(tmp_path, raw, 1)
    _da_tu_choi(kq, ra, "PM_COT_RIENG_TU")
    assert "vi-du.invalid" not in kq.stdout + kq.stderr


# ══ DT5-B2 · phá đổi 1 mã HD lạ ⇒ ĐỎ; trả nguyên ⇒ đúng từng byte ══════════════

def test_DT5_B2_doi_ma_HD_la_thi_DO_tra_nguyen_dung_tung_byte(tmp_path):
    """DT5-B2: lưới tổng hợp ĐẦY ĐỦ *(5 LE × 74, 760 ngày, 25 ô `-`)* với 2 ô ≠ 0 ⇒ ĐẠT; đổi 1 mã
    HD khối GROUP `GI → ZZZ` *(giữ giá trị)* ⇒ cổng ĐỎ *(thieu=['ZZZ'])*; trả nguyên ⇒ ĐÚNG TỪNG
    BYTE baseline. ⭐ Cổng được CHỨNG MINH ĐỎ *(phá, chạy, xem cắn, trả nguyên)*."""
    ser = _serials(NGAY_N)
    gia = {("GROUP", "GI", ser[1]): 1.5, ("SGO2", "OPC", ser[2]): -2.25}
    kq0, ra0 = _freeze(tmp_path, _luoi_daily(gia=gia), 2, "base.json")
    assert kq0.returncode == 0, (kq0.stdout[-1500:], kq0.stderr[-1500:])
    goc = ra0.read_bytes()
    b = _doc(ra0)
    assert b["phu"]["o_loi"]["so_dong"] == OLOI_D and b["phu"]["ngay_truc"]["so_dong"] == NGAY_N

    kq1, ra1 = _freeze(tmp_path, _luoi_daily(gia=gia, break_code=(0, "GI", "ZZZ")), 2, "pha.json")
    assert kq1.returncode == 1, (kq1.stdout[-1500:], kq1.stderr[-1500:])
    assert "ZZZ" in _doc(ra1)["thieu"] and "[ĐỎ]" in kq1.stdout

    kq2, ra2 = _freeze(tmp_path, _luoi_daily(gia=gia), 2, "lai.json")     # trả nguyên
    assert kq2.returncode == 0 and ra2.read_bytes() == goc               # đúng từng byte


def test_DT5_B2_doi_LE_la_thi_TU_CHOI(tmp_path):
    """DT5-B2 *(chiều LE)*: đổi mã LE khối 1 sang `XXX` ⇒ cây sai cấu trúc ⇒ TỪ CHỐI."""
    kq, ra = _freeze(tmp_path, _luoi_daily(_serials(3), break_le=(1, "XXX")), 1)
    _da_tu_choi(kq, ra, "mã LE")


# ══ AC-4 · lát hỏng ⇒ TỪ CHỐI (mỗi cổng chứng minh ĐỎ) ═════════════════════════

def test_AC4_truc_ngay_khong_lien_tuc_thi_TU_CHOI(tmp_path):
    """AC-4 ②: trục ngày ⛔ liên tục *(bỏ một serial giữa)* ⇒ TỪ CHỐI *(lát ngày hụt — ⛔ im lặng)*."""
    kq, ra = _freeze(tmp_path, _luoi_daily([SERIAL_MOC, SERIAL_MOC + 1, SERIAL_MOC + 3]), 1)
    _da_tu_choi(kq, ra, "liên tục")


def test_AC4_moc_ngay_dau_sai_thi_TU_CHOI(tmp_path):
    """AC-4: cột ngày đầu ≠ mốc 45585 *(2024-10-20)* ⇒ TỪ CHỐI *(⛔ neo nhầm trục ngày)*."""
    kq, ra = _freeze(tmp_path, _luoi_daily([SERIAL_MOC + 1, SERIAL_MOC + 2]), 1)
    _da_tu_choi(kq, ra, str(SERIAL_MOC))


def test_AC4_cot_tuong_lai_khac_0_thi_TU_CHOI(tmp_path):
    """AC-4 ③: cột ngày tương lai *(> ngày đọc)* có ô ≠ 0 ⇒ TỪ CHỐI *(⛔ dám cắt)*."""
    raw = _luoi_daily(_serials(3), future=(SERIAL_MOC + 5000,),
                      future_gia={("GROUP", "GI"): 9.9})
    kq, ra = _freeze(tmp_path, raw, 1)
    _da_tu_choi(kq, ra, "tương lai")


def test_AC4_cot_tuong_lai_toan_0_thi_CAT_dung(tmp_path):
    """AC-4 ③ *(chiều xanh — Đ5 NO cả hai chiều)*: cột tương lai TOÀN 0 ⇒ CẮT; ảnh chỉ còn trục
    ≤ ngày đọc. Lưới đầy đủ 760 ngày + 1 cột tương lai 0 ⇒ `ngay_truc` = 760, vẫn ĐẠT."""
    gia = {("GROUP", "GI", SERIAL_MOC + 1): 1.0}
    kq, ra = _freeze(tmp_path, _luoi_daily(gia=gia, future=(SERIAL_MOC + 5000,)), 1)
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-800:])
    assert _doc(ra)["phu"]["ngay_truc"]["so_dong"] == NGAY_N


def test_AC4_ban_tho_values_RONG_thi_TU_CHOI(tmp_path):
    """AC-4/Đ3: lưới `values` RỖNG ⇒ TỪ CHỐI *(⛔ đóng băng ảnh rỗng)*, ⛔ ghi tệp."""
    raw = {"nguon": "'Report I CFA1 Daily'!A1:X", "doc_luc": NGAY_DOC.isoformat(),
           "cach_doc": "rỗng", "values": []}
    kq, ra = _freeze(tmp_path, raw, 1)
    _da_tu_choi(kq, ra, "values")


def test_AC4_thieu_khoi_LE_thi_TU_CHOI(tmp_path):
    """AC-4: lưới thiếu một khối LE *(chỉ 4 HDO)* ⇒ TỪ CHỐI *(⛔ đủ 5 khối CF THEO LE)*."""
    raw = _luoi_daily(_serials(2))
    vals = raw["values"]
    idx = [i for i, r in enumerate(vals)
           if len(r) > 1 and r[1] == "HDO" and isinstance(r[0], str) and r[0] in LE5]
    raw["values"] = vals[:idx[4]]
    kq, ra = _freeze(tmp_path, raw, 1)
    _da_tu_choi(kq, ra, "khối LE")


# ══ lưới TỔNG HỢP Y/H/Q/M từ cây ATL — ca phá vòng sửa R1 ══════════════════════

def _ky_cot_nam(nam):
    """19 kỳ CHUẨN của một năm → [(ô Period, token)]: Năm · H1 H2 · Q1…Q4 · tháng 1…12."""
    out = [(nam, "Y"), ("H1", "H1"), ("H2", "H2")]
    out += [(f"Q{q}", f"Q{q}") for q in range(1, 5)]
    out += [(m, f"M{m:02d}") for m in range(1, 13)]
    return out


def _luoi_yhqm(nams=(2024, 2025, 2026), *, gia=None, swap_thang=None, period_override=None,
               break_code=None):
    """Lưới CFA1 Y/H/Q/M tổng hợp *(5 LE × 74, ⛔ số thật)*. `gia`={(le, ma, chỉ_số_cột): số};
    `swap_thang`=(năm, m1, m2) hoán ô Period hai cột tháng *(⇒ thứ tự khoá lệch)*; `period_override`
    =(chỉ_số_cột, ô_mới); `break_code`=(khối, ma_cũ, ma_mới). Tự 25 ô `"-"` cho ca XANH."""
    gia = dict(gia or {})
    nodes = _cay_nodes()
    cols = []                                                   # (nam, ô Period, token)
    for nam in nams:
        kc = _ky_cot_nam(nam)
        if swap_thang and swap_thang[0] == nam:
            idx = {tok: i for i, (pc, tok) in enumerate(kc)}
            i1, i2 = idx[f"M{swap_thang[1]:02d}"], idx[f"M{swap_thang[2]:02d}"]
            kc[i1], kc[i2] = (kc[i2][0], kc[i1][1]), (kc[i1][0], kc[i2][1])   # hoán ô Period
        cols += [(nam, pc, tok) for pc, tok in kc]
    if period_override:
        ci, ncell = period_override
        cols[ci] = (cols[ci][0], ncell, cols[ci][2])
    ncol = len(cols)
    oloi = {("GROUP", nd["ma"], 0): "-" for nd in nodes[-OLOI_Y:]}           # 25 ô "-" ở cột 0

    def drow(le, ma):
        row = [0.0] * ncol
        for k in range(ncol):
            if (le, ma, k) in gia:
                row[k] = gia[(le, ma, k)]
            elif (le, ma, k) in oloi:
                row[k] = oloi[(le, ma, k)]
        return row

    values = [[None] * 6 + [0] * ncol for _ in range(4)]
    values.append([None] * 5 + ["Year"] + [nam for nam, pc, tok in cols])   # hàng 5 = Year
    values.append([None] * 5 + ["Period"] + [pc for nam, pc, tok in cols])  # hàng 6 = Period
    for bi, le in enumerate(LE5):
        prev, first = None, True
        for nd in nodes:
            ma, ten, cap, nhom = nd["ma"], nd["ten"], nd["cap"], nd["nhom"]
            if nhom != prev:
                values.append([(le if first else 0), nhom, _TEN_NHOM[nhom], None, None, None]
                              + [0] * ncol)
                first, prev = False, nhom
            ma_hien = (break_code[2] if break_code and break_code[0] == bi
                       and ma == break_code[1] else ma)
            row = [1.0, None, None, None, None, None]
            row[cap] = f"{ma_hien} | {ten}"
            values.append(row + drow(le, ma))
    return {"nguon": "'Report I CFA1 Y H Q M'!A1:TONG_HOP", "doc_luc": NGAY_DOC.isoformat(),
            "cach_doc": "TỔNG HỢP yhqm · bài DT5 (⛔ số thật)", "values": values}


def _freeze_y(tmp, raw, mong, ra="y.json"):
    out = tmp / ra
    return _chay("cfa1_yhqm", _viet(tmp, raw), mong, out), out


# ══ DT5-R1-01 · cổng đo trên CÂY ĐẦY ĐỦ (hàng toàn-0, ⛔ chỉ hàng có số) ════════

def test_DT5_R1_01_ma_hang_toan_0_la_thi_DO(tmp_path):
    """`DT5-R1-01`: mã LẠ ở hàng HD **TOÀN-0** *(⛔ ô ≠ 0 nào)* phải ĐỎ — cổng cũ MÙ 164/370 hàng
    toàn-0. Lưới đầy đủ + 1 ô ≠ 0 ở mã KHÁC ⇒ XANH; đổi một mã GROUP toàn-0 → `ZZZ` ⇒ cổng ĐỎ
    *(`thieu` có `GROUP:lạ@ZZZ` + `GROUP:vắng@<mã cũ>`)*; trả nguyên ⇒ XANH. ⭐ ĐỎ hai chiều Đ5."""
    codes = [n["ma"] for n in _cay_nodes()]
    ma0 = codes[0]                                             # mã GROUP đầu — toàn-0 (⛔ trong 25 ô "-")
    gia = {("SGO2", "OPC", _serials(NGAY_N)[1]): 1.5}         # 1 ô ≠ 0 ở mã KHÁC
    kq0, ra0 = _freeze(tmp_path, _luoi_daily(gia=gia), 1, "base.json")
    assert kq0.returncode == 0, (kq0.stdout[-1200:], kq0.stderr[-1200:])

    kq1, ra1 = _freeze(tmp_path, _luoi_daily(gia=gia, break_code=(0, ma0, "ZZZ")), 1, "pha.json")
    assert kq1.returncode == 1, (kq1.stdout[-1500:], kq1.stderr[-1500:])
    th = _doc(ra1)["thieu"]
    assert f"GROUP:lạ@ZZZ" in th and f"GROUP:vắng@{ma0}" in th, th
    assert "ZZZ" not in {_chu(d["ma_hd"]) for d in _doc(ra1)["dong"]}        # ⛔ vào dòng chính (toàn-0)

    kq2, ra2 = _freeze(tmp_path, _luoi_daily(gia=gia), 1, "lai.json")
    assert kq2.returncode == 0, (kq2.stdout[-1200:], kq2.stderr[-800:])


def test_DT5_R1_01_hai_hang_cung_ma_thi_DO(tmp_path):
    """`DT5-R1-01`: hai hàng cùng mã ở khối *(ATL vắng 1 + trùng 1, vẫn 74 hàng/khối)* phải ĐỎ.
    Đổi mã GROUP `codes[0]` → `codes[1]` ⇒ `codes[1]` TRÙNG, `codes[0]` VẮNG ⇒ cổng ĐỎ."""
    codes = [n["ma"] for n in _cay_nodes()]
    gia = {("SGO2", "OPC", _serials(NGAY_N)[1]): 1.5}
    kq, ra = _freeze(tmp_path, _luoi_daily(gia=gia, break_code=(0, codes[0], codes[1])), 1)
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-1500:])
    th = _doc(ra)["thieu"]
    assert f"GROUP:trùng@{codes[1]}" in th and f"GROUP:vắng@{codes[0]}" in th, th


def test_DT5_R1_01_cong_neu_cây_toan_0_dem_mau_so(tmp_path):
    """`DT5-R1-01` *(Đ3)*: cổng NÊU mẫu số hàng toàn-0 ở dòng `dải` — lưới baseline *(chỉ 1 ô ≠ 0)*
    có 369 hàng toàn-0 *(370 − 1)*. Chứng minh phép đo trên tập KHÔNG rỗng."""
    gia = {("SGO2", "OPC", _serials(NGAY_N)[1]): 1.5}
    kq, ra = _freeze(tmp_path, _luoi_daily(gia=gia), 1)
    assert kq.returncode == 0, (kq.stdout[-1200:], kq.stderr[-800:])
    assert "hàng toàn-0 369" in kq.stdout, kq.stdout


# ══ DT5-R1-02 · lời lỗi ⛔ in GIÁ TRỊ ô bản thô (có thể PII) ════════════════════

def test_DT5_R1_02_loi_ma_LE_khong_in_o_ban_tho(tmp_path):
    """`DT5-R1-02`: ô cột A *(mã LE)* mang chuỗi giả-PII ⇒ TỪ CHỐI nhưng lời lỗi ⛔ in lại chuỗi
    *(`_cfa1.py:132` dùng `_an_toan`, ⛔ `!r`)*."""
    pii = "ketoan@vi-du.invalid"
    kq, ra = _freeze(tmp_path, _luoi_daily(_serials(3), break_le=(0, pii)), 1)
    _da_tu_choi(kq, ra, "mã LE")
    assert pii not in kq.stdout + kq.stderr and "vi-du.invalid" not in kq.stdout + kq.stderr


def test_DT5_R1_02_loi_Period_khong_in_o_ban_tho(tmp_path):
    """`DT5-R1-02`: ô Period mang chuỗi giả-PII ⇒ TỪ CHỐI nhưng lời lỗi ⛔ in lại chuỗi
    *(`cfa1_yhqm.py:81` dùng `_an_toan`, ⛔ `!r`)*."""
    pii = "nguoi@vi-du.invalid"
    kq, ra = _freeze_y(tmp_path, _luoi_yhqm(period_override=(10, pii)), 1)
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-800:], kq.stderr[-800:])
    assert "Period" in kq.stderr and pii not in kq.stdout + kq.stderr
    assert "vi-du.invalid" not in kq.stdout + kq.stderr and not ra.exists()


# ══ DT5-R1-03 · nhãn trục ĐỐI CHIẾU chéo (serial · thứ · kỳ) ═══════════════════

def test_DT5_R1_03_serial_khong_nguyen_thi_TU_CHOI(tmp_path):
    """`DT5-R1-03`: serial ngày LẺ *(`.5`)* ⇒ TỪ CHỐI *(⛔ `int()` cắt im lặng)*."""
    raw = _luoi_daily(_serials(3))
    raw["values"][4][COT_DAU + 1] = SERIAL_MOC + 1.5          # hàng Day, cột thứ 2
    kq, ra = _freeze(tmp_path, raw, 1)
    _da_tu_choi(kq, ra, "nguyên")


def test_DT5_R1_03_dow_sai_thi_TU_CHOI(tmp_path):
    """`DT5-R1-03`: nhãn thứ ngày SAI *(đổi một ô 'Days of the week')* ⇒ TỪ CHỐI *(⛔ khớp
    `(serial+6)%7`)*."""
    raw = _luoi_daily(_serials(3))
    j = COT_DAU                                               # cột ngày đầu (2024-10-20 = Sun)
    raw["values"][5][j] = "Fri"                               # Sun → Fri
    kq, ra = _freeze(tmp_path, raw, 1)
    _da_tu_choi(kq, ra, "thứ ngày")


def test_DT5_R1_03_period_ngoai_1_12_thi_TU_CHOI(tmp_path):
    """`DT5-R1-03`: Period SỐ ∉ 1…12 và ≠ năm *(vd `2023` ở cột `Year=2024`)* ⇒ TỪ CHỐI *(⛔ khoá
    rác `2024M2023`)*."""
    kq, ra = _freeze_y(tmp_path, _luoi_yhqm(period_override=(10, 2023)), 1)   # cột tháng của 2024
    assert kq.returncode == 2, (kq.returncode, kq.stderr[-800:])
    assert "tháng 1…12" in kq.stderr and not ra.exists()


def test_DT5_R1_03_hoan_nhan_thang_thi_TU_CHOI(tmp_path):
    """`DT5-R1-03`: hoán nhãn tháng 3↔4 của một năm ⇒ thứ tự kỳ lệch ⇒ TỪ CHỐI."""
    kq, ra = _freeze_y(tmp_path, _luoi_yhqm(swap_thang=(2024, 3, 4)), 1)
    assert kq.returncode == 2, (kq.returncode, kq.stderr[-800:])
    assert "thứ tự kỳ" in kq.stderr and not ra.exists()


# ══ DT5-R1-04 · cổng o_loi ghim PHÂN BỐ giá trị lỗi (⛔ chỉ đếm) ════════════════

def test_DT5_R1_04_REF_thay_dash_thi_DO(tmp_path):
    """`DT5-R1-04`: đổi một ô `"-"` → `#REF!` *(vẫn đếm 25)* phải ĐỎ — `o_loi_gia` ghim phân bố
    `{"-": 25}`, Đ5 buộc ghi lại bản khai. Baseline 25 `"-"` ⇒ XANH."""
    codes = [n["ma"] for n in _cay_nodes()]
    gia = {("SGO2", "OPC", _serials(NGAY_N)[1]): 1.5}
    kq0, _ = _freeze(tmp_path, _luoi_daily(gia=gia), 1, "base.json")
    assert kq0.returncode == 0, (kq0.stdout[-1200:], kq0.stderr[-800:])

    # một ô "-" (trên 25 nút CUỐI của GROUP) → "#REF!"
    oloi = {("GROUP", nd["ma"], SERIAL_MOC): "-" for nd in _cay_nodes()[-OLOI_D:]}
    ma_ref = _cay_nodes()[-1]["ma"]
    oloi[("GROUP", ma_ref, SERIAL_MOC)] = "#REF!"
    kq1, ra1 = _freeze(tmp_path, _luoi_daily(gia=gia, oloi=oloi), 1, "ref.json")
    assert kq1.returncode == 1, (kq1.stdout[-1500:], kq1.stderr[-1500:])
    assert any("o_loi_gia@khác" in t for t in _doc(ra1)["thieu"]), _doc(ra1)["thieu"]
    assert "#REF!" in kq1.stdout                               # token lỗi an toàn ⇒ hiện


# ══ Khuôn là TỆP RIÊNG + giữ ảnh cũ từng byte (AC-4) ═══════════════════════════

def test_khuon_cfa1_la_tep_rieng_dung_giao_keo():
    """Khuôn mới = hai tệp riêng, giao kèo đúng; dùng chung `_cfa1`; `_cfa1` ⛔ phải một khuôn."""
    import importlib.util
    for ten, bang, cot in (("cfa1_daily", "PD.409", ("le", "ma_hd", "ngay", "gt")),
                           ("cfa1_yhqm", "PD.410", ("le", "ma_hd", "ky", "gt"))):
        p = THU_MUC_KHUON / f"{ten}.py"
        assert p.is_file()
        spec = importlib.util.spec_from_file_location(f"khuon_{ten}_bai", p)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        assert m.BANG == bang and m.KHOA == "o_id" and m.KIEU_KHOA == "ma"
        assert m.COT == cot and callable(m.chuan_bi) and callable(m.thieu_lac)
        assert m.PHU_MONG["hd"] == 370 and "o_loi" in m.PHU_MONG
    assert "_cfa1" not in [p.stem for p in THU_MUC_KHUON.glob("*.py")
                           if not p.stem.startswith("_")]


def test_giu_anh_DT2_DT3_DT4_dung_tung_byte():
    """Thêm khuôn CFA1 *(công cụ chung ⛔ đụng)* ⇒ ix_fx + 3 ảnh DT3 + đáp án 406 giữ ĐÚNG TỪNG
    BYTE *(sha256[:16] ghim)*."""
    for f, sha in SHA_GIU.items():
        got = hashlib.sha256((GOC / "tests" / "fixture" / f"{f}.json").read_bytes()).hexdigest()[:16]
        assert got == sha, (f, got, sha)
