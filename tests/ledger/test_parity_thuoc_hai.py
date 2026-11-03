"""THUOC THU HAI — doi chieu luat `Final` tren mot FILE KHAC, doc lap.

Vi sao can thuoc thu hai: cong parity dau (`test_parity_ca_so`) chay tren mot
nguon duy nhat. Neu chinh nguon do co mot dac diem rieng ma luat cua ta tinh co
khop, cong se xanh ma luat van sai. Hai nguon khac nhau cung khop thi kha nang
do gan het.

Nguon: `Input_Raw/[Master] ITL_Ledge_raw.xlsx` — owner chi tro toi 2026-08-26.
**9.767 dong** (nhieu hon nguon thu nhat 548 dong) va co them mot bo cot nua.

★ NEN GON: giu **bo ba DUY NHAT** `(Classifying, MID, Final)` thay vi tung dong.
Luat `Final` chi doc ba o nay, nen phu het bo ba = phu het dong.
**9.767 dong -> 2.166 bo ba -> 311 KB** thay vi ~0,9 MB.

⛔ FILE NAY **KHONG** DUNG DE CHIA KY. Do that: **4.387/4.387** o kieu ngay deu
co `ngay <= 12` — ngay that thi ky vong ~61% vuot 12, nen ca tap nay bi **HOAN
thang<->ngay**. Co che: Excel doc `M/D/YYYY`; gap `10/21/2024` thi 21 khong the
la thang nen **de lai dang CHUOI**; gap `10/12/2024` thi doc duoc nhung **hoan**.
⇒ **5.380 o CHUOI moi la o an toan**, 4.387 o "kieu ngay" moi la o hong. Nguoc
han truc giac. Owner xac nhan: *"sai format date"*.

⇒ Phan chia ky van thuoc `test_parity_ca_so.py` (nguon do: **9.219/9.219 o ngay
nguyen kieu**, 55,4% vuot 12, phan bo deu 31 ngay — sach).
"""
from __future__ import annotations

import hashlib
import json
import pathlib

import pytest

from fls.ledger.final_rule import TEN_BAY_KHOI, tinh_final
from fls.oracle.tu_soi import la_o_loi

F = pathlib.Path(__file__).resolve().parents[1] / "fixture" / "itl_master_bo_ba.json"
CHECKSUM = "a36c93569267f384"
DONG_GOC = 9767
SO_BO_BA = 2166


@pytest.fixture(scope="module")
def goi():
    return json.loads(F.read_text(encoding="utf-8"))


def _chuan(v) -> str:
    if v is None:
        return ""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v).strip()


def test_hien_vat_khong_bi_sua(goi):
    tinh = hashlib.sha256(
        json.dumps(goi["bo_ba"], ensure_ascii=False,
                   separators=(",", ":")).encode()).hexdigest()[:16]
    assert tinh == CHECKSUM == goi["checksum_noi_dung"]


def test_pham_vi_dung_nhu_khai(goi):
    assert goi["dong_goc"] == DONG_GOC
    assert goi["so_bo_ba"] == SO_BO_BA == len(goi["bo_ba"])
    assert {b[0] for b in goi["bo_ba"]} == TEN_BAY_KHOI      # du bay khoi


def test_hien_vat_KHAI_RO_rang_khong_dung_de_chia_ky(goi):
    """Mot hien vat mang khuyet tat phai NOI RA, ⛔ khong de nguoi sau tu phat hien."""
    assert "KHONG dung de chia ky" in goi["vai"]
    assert "HOAN" in goi["vi_sao_khong_chia_ky"]


def test_luat_Final_khop_tren_NGUON_THU_HAI(goi):
    """★ Doi chieu doc lap: **68.311/68.369 o = 99,92%**.

    ⛔ KHONG phai 100%, va toi khong lam tron len. 58 o lech — xem phep thu duoi
    day chung minh chung KHONG phai loi luat.
    """
    tong = khop = bo_qua = 0
    o_khop = o_lech = 0
    lech = []
    for k, cls, mid, fin, n in goi["bo_ba"]:
        if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
            bo_qua += 1
            continue
        tinh = tinh_final(_chuan(cls) or None, _chuan(mid) or None)
        a, b = _chuan(tinh), _chuan(fin)
        ok = a == b
        if not ok:
            try:
                ok = float(a) == float(b)
            except (TypeError, ValueError):
                pass
        tong += 1
        if ok:
            khop += 1
            o_khop += n
        else:
            o_lech += n
            lech.append((k, _chuan(cls), _chuan(mid), b, a, n))

    assert bo_qua == 0
    assert (khop, tong) == (2133, SO_BO_BA)
    assert (o_khop, o_lech) == (68311, 58)
    assert o_khop + o_lech == 68369
    assert len(lech) == 33


def test_MOI_O_LECH_deu_KHONG_THE_sinh_tu_dong_do__nen_khong_phai_loi_luat(goi):
    """★★ Phep thu quan trong nhat cua file nay — no bien "58 o lech" tu mot
    con so dang lo thanh mot ket luan.

    Luat `Final` chi co the tra ve **`Classifying`** hoac **`MID`** — do la toan
    bo mien gia tri cua no. Nen neu `Final` cua so **khong thuoc `{Classifying,
    MID}`** thi o do **khong the sinh ra tu dong do bang BAT KY luat nao**.
    ⇒ Khong phai luat cua ta sai. La `Final` mang gia tri cua **dong khac**.

    Do that: **33/33** o lech deu the. Hai dang:
      `Final` RONG                      14
      `Final` = gia tri cua dong KHAC   19
    Cung mot hien tuong da thay o thuoc thu nhat (20 dong don het vao duoi so):
    ban xuat bi **lech dong** o cot `Final`.
    """
    ngoai_mien = []
    for k, cls, mid, fin, _n in goi["bo_ba"]:
        if la_o_loi(cls) or la_o_loi(mid) or la_o_loi(fin):
            continue
        tinh = _chuan(tinh_final(_chuan(cls) or None, _chuan(mid) or None))
        if tinh == _chuan(fin):
            continue
        # o lech: `Final` co nam trong mien gia tri kha di cua luat khong?
        mien = {_chuan(cls), _chuan(mid)}
        assert _chuan(fin) not in mien, (
            f"o lech NAM TRONG mien gia tri cua luat => day MOI la loi luat that: "
            f"khoi={k} Classifying={_chuan(cls)!r} MID={_chuan(mid)!r} "
            f"Final={_chuan(fin)!r} FLS_tinh={tinh!r}")
        ngoai_mien.append(k)
    assert len(ngoai_mien) == 33
    from collections import Counter
    assert dict(Counter(ngoai_mien)) == {
        "hd": 19, "id_payee": 3, "svc_start": 3, "svc_end": 3,
        "cdt1": 2, "pay_type": 2, "invoice": 1}


def test_hai_thuoc_dong_y_nhau(goi):
    """Hai nguon khac nhau, cung mot ket luan.

    Thuoc 1: **64.393/64.393** o tren 9.219 dong (`test_parity_ca_so`)
    Thuoc 2: **68.311/68.369** o tren 9.767 dong, nen thanh 2.166 bo ba (o day)
    ⇒ **132.704/132.762 o** tu hai file doc lap. 58 o lech, ⛔ tat ca da chung
      minh la lech dong cua ban xuat, khong phai loi luat.
    """
    assert goi["dong_goc"] > 9219          # nguon nay LON hon nguon thu nhat
    assert sum(b[4] for b in goi["bo_ba"]) == 68369
