# -*- coding: utf-8 -*-
"""`B1` — luat doc **THE LENH CHI**: `11` truong, va `None` la mot CAU TRA LOI.

⛔⛔ **Vi sao khuon nay phai o tang DOC.** Do `22/09` tren kho that: the lenh
   chi can **6** truong ma **⛔ khong cua nao goi ten** — ca 6 chi nam trong
   tui `tho`, khoa theo **TEN COT CUA GOOGLE SHEETS** (`"Tên tài khoản"`,
   `"Pháp nhân thanh toán"`, …).

⇒ Neu man hinh tu moc `tho["Tên tài khoản"]` thi **JS doc thang ten cot cua
  sheet**. Ten cot ay **da doi mot lan roi**, va khi no doi lan nua thi cho
  hong la **mot o trong im lang** tren man — ⛔ khong bai thu nao do duoc, vi
  bai thu se go **y het ten ay**.
"""
from __future__ import annotations

from fls.repo import man_ghep as mg

#: ⭐ Mot hang tho **dung khuon kho that** — lay tu `/queue/lenh-cho` `22/09`.
#: ⚠ Ten nguoi CO Y la chu cai dau: bai thu nay la **ban se ra ngoai kho**.
HANG = {
    "pm_line_id": "PM01698-1", "pm_slip_id": "PM01698",
    "amount": "40.00", "curr": "EUR", "cdt1": "COR | TeraSofts",
    "ref_tho": None, "status": "Approve",
    "tho": {
        "Timestamp": 46091.42265217593,
        "Loại giao dịch (Payment Type)": "Thanh toán (Regular)",
        "Nội dung giao dịch nhập khi lập lệnh ở bank": "TT Freepik T3",
        "Pháp nhân thanh toán": "VGO2 - TeraSofts",
        "Ngân hàng": "VPBank", "Tên tài khoản": "N. V. A.",
        "Số tài khoản": "134933879",
        "Đơn vị tiền tệ (Currency)": "EUR",
        "Tổng số tiền thanh toán (Transaction Amount)": 40,
        "Reference number": None, "Chủ dự toán (CDT1)": "COR | TeraSofts",
        "Status_Final": "Approve", "Status_Log": "Close",
        "Check trùng ID PMLine": 1,
        "ID PMSlip": "PM01698", "ID PMLine": "PM01698-1",
        "Budget Code (HDCode)": "LC | License Cost",
        "Chủ dự toán *": "COR | Terasofts",
    },
}


def _the(**doi):
    return mg.khuon_the_lenh(dict(HANG, **doi))


# ── ⓐ ⭐ NGAN SACH TRUONG = 11 (`UI-F7`, `QĐ-ITL-147`) ────────────────────

def test_the_co_DUNG_11_truong():
    t = _the()
    co = [k for k in mg.TRUONG_THE if k in t]
    assert len(mg.TRUONG_THE) == 11, "⛔ tran `UI-F7` la **11**"
    assert co == list(mg.TRUONG_THE), f"⛔ thieu truong: {set(mg.TRUONG_THE) - set(t)}"


def test_hai_ban_khai_TRUONG_THE_KHONG_duoc_lech():
    """⭐⭐ Con so `11` song o **hai** cho — Python va JS. Hai ban su that ve
    cung mot tran thi chung se lech, va lech **trong im lang**."""
    import io
    import pathlib
    import re
    js = (pathlib.Path(__file__).resolve().parents[2]
          / "fls" / "web" / "tep" / "man_f01_ghep.js")
    m = re.search(r"TRUONG_THE\s*=\s*\[([\s\S]*?)\]", io.open(js, encoding="utf-8").read())
    assert m, "⛔ ⛔ khong tim thay `TRUONG_THE` ben JS"
    ben_js = tuple(x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip())
    assert ben_js == mg.TRUONG_THE, (
        f"⛔ hai ban khai LECH:\n  py = {mg.TRUONG_THE}\n  js = {ben_js}")


# ── ⓑ ⭐⭐ `None` la mot CAU TRA LOI ──────────────────────────────────────

def test_so_chung_tu_VANG_van_la_mot_KHOA_co_mat():
    """⛔⛔ Bo khoa di la bien *"lenh nay ⛔ khong co so chung tu"* thanh
    *"FLS ⛔ khong biet"*. Do `22/09`: vang **535/3.772** = **14,2%**."""
    t = _the(ref_tho=None)
    assert "so_chung_tu" in t and t["so_chung_tu"] is None


def test_o_VANG_trong_khoi_du_truong_KHONG_bi_bo():
    """⭐ `Chi nhánh` chi **11,7%** hang tho co ⇒ **88,3%** so lan mo khoi nay
    o ay la mot o VANG. No phai **doc duoc**, ⛔ khong duoc bien mat."""
    nh = {n["ten"]: dict(n["o"]) for n in _the()["nhom_du_truong"]}
    assert "Chi nhánh" in nh["Lập lệnh"], "⛔ o VANG bi giau"
    assert nh["Lập lệnh"]["Chi nhánh"] is None


# ── ⓒ ⭐⭐ `UI-F9` — mot su that, MOT cho hien ────────────────────────────

def test_khoi_du_truong_KHONG_lap_lai_thu_da_len_the():
    t = _the()
    tat_ca = [k for n in t["nhom_du_truong"] for k, _ in n["o"]]
    for lap in mg.THO_DA_LEN_THE:
        assert lap not in tat_ca, (
            f"⛔ `{lap}` hien **hai lan** (tren the ＋ trong khoi du truong) — "
            "mot con so hien hai cho la mot con so se lech")


# ── ⓓ ⭐⭐⭐ SO SE RI ⛔ KHONG duoc len man mot NGUOI ─────────────────────

def test_timestamp_KHONG_con_la_so_se_ri():
    """⛔⛔ `BA-06 §4.5 ⓕ` tung khai *"da het timestamp se ri"* — va khai ay
    **SAI**: no do tren BAN DUNG *(nguoi thiet ke go tay `18/09/2026 09:14`)*,
    ⛔ khong do tren kho. Do lai `22/09` **tren cua that**: `Timestamp` ra dung
    **3.772/3.772** dong duoi dang so se ri.
    """
    nh = {n["ten"]: dict(n["o"]) for n in _the()["nhom_du_truong"]}
    gt = nh["Lập lệnh"]["Timestamp"]
    assert isinstance(gt, str) and "/" in gt, (
        f"⛔⛔ `Timestamp` len man duoi dang **{gt!r}** — mot ke toan ⛔ khong "
        "doc duoc `46091.42265217593`")
    assert gt == "10/03/2026 10:08", gt


def test_se_ri_HONG_thi_GIU_NGUYEN_chu_KHONG_xoa():
    """⭐ *"⛔ khong doi duoc"* ⛔ khac *"⛔ khong co"*. Mot gia tri la phai
    **hien nguyen**, de nguoi ta thay chinh cai la ay."""
    t = _the(tho=dict(HANG["tho"], Timestamp="hom qua"))
    nh = {n["ten"]: dict(n["o"]) for n in t["nhom_du_truong"]}
    assert nh["Lập lệnh"]["Timestamp"] == "hom qua"


# ── ⓔ ⭐ CHE tai khoan — CUNG MOT LUAT voi `nguon.tk` ────────────────────

def test_tai_khoan_di_qua_DUNG_phep_che_cua_ung_vien():
    assert _the()["tai_khoan"] == mg.che_tai_khoan("134933879") == "••3879"


def test_the_KHONG_phai_so_thi_KHONG_bi_cat_mu_quang():
    t = _the(tho=dict(HANG["tho"], **{"Số tài khoản": "PO2"}))
    assert t["tai_khoan"] == "PO2", "⛔ `••PO2` vua vo nghia vua ⛔ che duoc gi"


# ── ⓕ ⭐ NHAN loai phieu — bang tra, ⛔ KHONG regex ──────────────────────

def test_loai_phieu_rut_ngan_theo_BANG_TRA():
    assert _the()["loai_phieu"] == "Regular"


def test_loai_phieu_LA_thi_hien_NGUYEN_VAN():
    """⛔⛔ Cat bang regex se **im lang** bop mot gia tri moi thanh mot nhan
    sai. Gia tri la NGHIA, va mot nghia la thi phai **doc thay**."""
    t = _the(tho=dict(HANG["tho"],
                      **{"Loại giao dịch (Payment Type)": "Hoàn ứng (Refund)"}))
    assert t["loai_phieu"] == "Hoàn ứng (Refund)"


# ── ⓖ ⭐⭐ COT MOI cua sheet ⛔ KHONG duoc bien mat ──────────────────────

def test_khoa_LA_roi_vao_nhom_Khac_chu_KHONG_bi_nuot():
    t = _the(tho=dict(HANG["tho"], **{"Cột mới ai đó vừa thêm": "x"}))
    nh = {n["ten"]: dict(n["o"]) for n in t["nhom_du_truong"]}
    assert nh.get("Khác", {}).get("Cột mới ai đó vừa thêm") == "x", (
        "⛔ mot cot MOI cua sheet bien mat — bang khai la **ban trang co loi "
        "thoat**, ⛔ khong phai mot bo loc")


def test_nhom_KHONG_ap_dung_thi_KHONG_hien():
    """⛔ Mot nhom **trong ruot** ⛔ khong phai mot o vang: `PE` chi co o
    **8,2%** dong. Hien mot tieu de rong la **them nhieu**, ⛔ khong them tin."""
    tho = {k: v for k, v in HANG["tho"].items()
           if not k.startswith(("ID PE", "Budget", "Chủ dự toán *"))}
    ten = [n["ten"] for n in mg.du_truong(tho)]
    assert "Ngân sách" not in ten


# ── ⓗ ⭐ ten NGUOI NHAN hien NGUYEN tren man (`QĐ-ITL-148 ②`) ────────────

def test_nguoi_nhan_KHONG_bi_che_tren_man():
    """⭐ Owner chot `21/09`: ten nguoi nhan la **noi dung cua khoan chi**,
    ⛔ khong phai ho so nhan su. Luat che chi ap cho **ban xuat ra ngoai kho**
    — nhu chinh tep nay, nen o day ten la chu cai dau."""
    assert _the()["nguoi_nhan"] == "N. V. A."
