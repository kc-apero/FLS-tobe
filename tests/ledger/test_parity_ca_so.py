"""CONG PARITY TREN CA SO — 9.219 dong · 22 ky · 7 khoi.

Mo rong tu `test_parity_2026_03.py` (584 dong, 1 ky). Cong ra cua P2.

⛔ VI SAO CHAY TREN HIEN VAT DONG BANG, KHONG DOC LIVE. Do 2026-08-26: workbook
`ADJUSTED` **khong the tra gia tri tinh ra** qua Sheets API — doc **MOT O** cung
timeout, o **moi** sheet, ca `values.get` lan `spreadsheets.get?includeGridData`.
Chi `valueRenderOption=FORMULA` chay (0,5s). Nguyen nhan trong cong thuc:
`A10 = filter(IMPORTRANGE(...), IMPORTRANGE(...))` — doc o nao cung bat ca
workbook tinh lai. `GAP-ORA-08`.

★ NGUON HIEN VAT DA DOI (owner dan ban moi 2026-08-26 17:55):
`Input_Raw/[Master] ITL_Ledge_raw.xlsx` — **9.967 dong · 23 ky · day den 2026-08**,
thay cho ban cu (9.219 dong, 22 ky, hut ~1,5 ky cuoi). ⇒ Gioi han ① DA DONG.

⚠ Cot ngay cua ban nay hong (5.580 o CHUOI + 4.387 o kieu ngay bi HOAN) nhung
**dung lai duoc**: hai tap BU TRU 100% nen tung o quyet dinh duoc —
`fls/oracle/ngay_xlsx.py`, co cong `kiem_bu_tru` chan neu khong bu tru.
**CHUNG MINH: 21/23 ky khop CHINH XAC voi ban ADJUSTED sach, lech 0**; hai ky
con lai ban moi co NHIEU hon, dung khoang hut da khai truoc do.

⚠ Gioi han con lai: chi lay **21 cot** (`Classifying`/`MID`/`Final` x 7 khoi) +
cot ngay. ⛔ KHONG lay `Dien giai`/`So chung tu` (co the co ten nguoi).
"""
from __future__ import annotations

import json
import pathlib
from collections import Counter

import pytest

from fls.ledger.final_rule import tinh_final
from fls.oracle.cong_parity import danh_gia
from fls.oracle.tu_soi import la_o_loi, soi_mot_dong

F = pathlib.Path(__file__).resolve().parents[1] / "fixture" / "itl_ledge_adjustment.json"
KHOI = ("hd", "pay_type", "cdt1", "svc_start", "svc_end", "id_payee", "invoice")
CHECKSUM = "575c53379074c759"
DONG_MONG_DOI = 9967


@pytest.fixture(scope="module")
def so():
    g = json.loads(F.read_text(encoding="utf-8"))
    idx = {n: i for i, n in enumerate(g["cot"])}
    bang = g["bang_gia_tri"]

    def val(h, ten):
        i = h[idx[ten]]
        return None if i == -1 else bang[i]

    hang = []
    for h in g["dong"]:
        hang.append((h[0], h[1], {k: (val(h, f"{k}_classifying"), None,
                                      val(h, f"{k}_mid"), val(h, f"{k}_final"))
                                  for k in KHOI}))
    return g, hang


def _chuan(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def khop_o(tinh, cua_so) -> tuple[bool, bool]:
    """(khop, da_phai_chuan_hoa_so). Chi khop-qua-so khi HAI BEN ra CUNG mot so."""
    a, b = _chuan(tinh), _chuan(cua_so)
    if a == b:
        return True, False
    try:
        if float(a) == float(b):
            return True, True
    except (TypeError, ValueError):
        pass
    return False, False


def test_hien_vat_khong_bi_sua(so):
    """Doi mot o trong fixture thi test nay do — hien vat phai dong bang."""
    import hashlib
    g, _ = so
    tinh = hashlib.sha256(
        json.dumps([g["dong"], g["bang_gia_tri"]], ensure_ascii=False,
                   separators=(",", ":")).encode()).hexdigest()[:16]
    assert tinh == CHECKSUM == g["checksum_noi_dung"]


def test_pham_vi_hien_vat_dung_nhu_khai(so):
    g, hang = so
    assert len(hang) == g["so_dong"] == DONG_MONG_DOI
    assert len(g["phan_bo_ky"]) == 23
    assert g["ngay_mo_ho"] == 0   # moi o ngay dung lai duoc, khong o nao doan


def test_hien_vat_KHONG_chua_cot_co_the_co_ten_nguoi(so):
    """AUD-12 + luat PII: khong doc/khong luu Dien giai · So chung tu."""
    g, _ = so
    xau = ("dien_giai", "so_chung_tu", "memo", "doc_no")
    assert not [c for c in g["cot"] if any(x in c.lower() for x in xau)]


def test_parity_100_phan_tram_tung_o_tren_CA_SO(so):
    """★ Cong ra cua P2. ⛔ Cam dung sai."""
    _g, hang = so
    tong_o = khop = can_chuan = 0
    loai: list[str] = []
    lech: list[dict] = []

    for dong_sheet, ky, bon in hang:
        kq = soi_mot_dong(bon)
        if not kq.giu:                       # ① tu soi: loai, co ly do CO TEN
            loai.append(f"dong {dong_sheet} ({ky}): {kq.ly_do}")
            continue
        for k, (cls, _man, mid, fin) in bon.items():     # ② so tung o
            if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
                continue
            tinh = tinh_final(_chuan(cls) or None, _chuan(mid) or None)
            ok, ch = khop_o(tinh, fin)
            tong_o += 1
            can_chuan += ch
            khop += ok
            if not ok and len(lech) < 8:
                lech.append({"dong": dong_sheet, "ky": ky, "khoi": k,
                             "Classifying": _chuan(cls), "MID": _chuan(mid),
                             "Final_so": _chuan(fin), "FLS_tinh": _chuan(tinh)})

    assert not lech, json.dumps(lech, ensure_ascii=False, indent=1)
    assert (khop, tong_o) == (69510, 69510)
    # CONG BO, de "100%" khong bi doc thanh "sach tuyet doi":
    assert can_chuan == 0        # ⛔ khong o nao phai chuan hoa so moi khop
    assert len(loai) == 37       # 37 dong bi loai, TAT CA o ky 2026-07


def test_ba_muoi_bay_dong_bi_loai_don_vao_MOT_KY__khong_phai_duoi_so(so):
    """⛔ TOI DA GIAI THICH SAI, va du lieu moi lat lai.

    Voi ban cu (9.219 dong) toi ghi: *"20 dong bi loai don het vao KY CUOI => file
    duoc luu khi may dong cuoi con dang settle"*. Ban moi co them 748 dong va ky
    moi (2026-08) **sach hoan toan**, con 37 dong bi loai van nam o **2026-07**,
    dai dong **8872-9125**, **cach cuoi so 851 dong**.

    => Khong phai hien tuong "duoi so dang settle". La **mot dai dong cu the**,
      on dinh qua hai lan chup khac nhau. ⛔ Toi khong biet vi sao, va khong bia
      mot loi giai thich thu hai.

    Phep thu nay khoa dung cai HINH: don vao mot ky, mot dai dong, khong o duoi.
    """
    _g, hang = so
    ky_loai: set[str] = set()
    dong_loai: list[int] = []
    khoi_loai: Counter = Counter()
    for dong_sheet, ky, bon in hang:
        kq = soi_mot_dong(bon)
        if not kq.giu:
            ky_loai.add(ky)
            dong_loai.append(dong_sheet)
            for k in KHOI:
                if f"khoi {k} " in kq.ly_do:
                    khoi_loai[k] += 1
    assert ky_loai == {"2026-07"}
    assert len(dong_loai) == 37
    assert (min(dong_loai), max(dong_loai)) == (8872, 9125)
    assert hang[-1][0] - max(dong_loai) == 851        # ⛔ KHONG phai duoi so
    assert dict(khoi_loai) == {"hd": 25, "cdt1": 7, "invoice": 5}


def test_BA_O_ma_luat_KHONG_giai_thich_duoc__ghi_ra_chu_khong_lam_tron(so):
    """★★ Phep thu that tha nhat cua ca bo.

    60/63 o lech co `Final` NGOAI mien gia tri cua luat => khong the sinh tu dong
    do bang bat ky luat nao => lech dong cua ban xuat.

    Nhung **3 o thi NAM TRONG mien** — va do la 3 o luat cua ta KHONG giai thich
    duoc:

        Classifying  = 'API | API'          MID = 'SC | Server Cost'
        Final cua so = 'SC | Server Cost'   FLS tinh = 'API | API'

    So tra ve `MID` du `Classifying` CO gia tri — trai voi cong thuc da doc
    nguyen van o ba dong khac nhau. Gia thuyet kha nhat: ban `[Master]` la mot
    lan DAN GIA TRI, va cot `Classifying` duoc dan o thoi diem KHAC cot `Final`,
    nen `Final` con giu gia tri cua lan truoc. ⛔ CHUA CHUNG MINH.

    Ca 3 o deu thuoc 37 dong ma `tu_soi` **da loai** khoi thuoc chuan — nen
    parity khong bi anh huong. Do dung la viec `tu_soi` sinh ra de lam. Nhung
    ⛔ khong duoc lam tron con so 3 nay thanh 0.
    """
    _g, hang = so
    ngoai_mien = trong_mien = 0
    ky_la: list[tuple] = []
    for dong_sheet, _ky, bon in hang:
        for k, (cls, _man, mid, fin) in bon.items():
            if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
                continue
            tinh = _chuan(tinh_final(_chuan(cls) or None, _chuan(mid) or None))
            if tinh == _chuan(fin):
                continue
            if _chuan(fin) in {_chuan(cls), _chuan(mid)}:
                trong_mien += 1
                ky_la.append((dong_sheet, k, _chuan(cls), _chuan(mid), _chuan(fin)))
            else:
                ngoai_mien += 1
    assert (ngoai_mien, trong_mien) == (60, 3)
    assert [x[0] for x in ky_la] == [8877, 8938, 8940]
    assert all(x[1] == "hd" for x in ky_la)
    assert all(8872 <= x[0] <= 9125 for x in ky_la)


def test_cong_phan_xu_DAT_tren_ca_so(so):
    """Noi cong parity vao cai chan — ⛔ khong tu ket luan bang mat."""
    _g, hang = so
    px = danh_gia(tong_o=69510, khop=69510, lat_truot=0,
                  dong_doc=len(hang), dong_mong_doi=DONG_MONG_DOI)
    assert px.dat, px.ly_do
