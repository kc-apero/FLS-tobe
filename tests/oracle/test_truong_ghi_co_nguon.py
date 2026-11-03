# -*- coding: utf-8 -*-
"""Cong: MOI truong nguoi go duoc phai co MOT cot nguon — hay khai ra la chua co.

★ Vi sao co cong nay. Owner mo nguyen mau lucoi `F02` (2026-08-28) va hoi mot
cau rat ngan: *"da doc dung cau truc bang chua?"* — ve vung `ALLOCATE`. Do lai
thi ra ba lo, va ⛔ khong lo nao co cong nao bat:

  ⓐ `cdt1_cfa2` la mot trong **10 truong nguoi go duoc** (`BA-07` §3) nhung
    ⛔ **khong co cot nao** trong khuon `ITL Ledge` tro tao — vung ALLOCATE chi
    co BA cot va CFA2 ⛔ khong co cot `Final`. Mot truong cho nguoi go ma khong
    co nguon thi ⛔ **khong ai doi chieu duoc**, va no im lang mai mai.
  ⓑ `alloc_method_classify` khai trong `fls_itl` ma ⛔ khong chu cai nao tro
    tao ⇒ mot cot **mai mai rong**.
  ⓒ `fls/db/schema.py` va `fls/oracle/ledge_spec.py` tung noi KHAC nhau ve
    cung mot chu cai (`AV`): mot ben `cdt1_cfa2`, mot ben `cdt1_cfa2_classify`.

⛔ Cong nay ⛔ KHONG doi phai co nguon — no doi phai **khai ra**. Mot lo duoc
khai kem cau hoi thi no con song; mot lo im lang thi khong.
"""
from __future__ import annotations

from fls.db.schema import TABLES
from fls.oracle.ledge_spec import CHUA_NOI, CHUA_NOI_NGUOC, K, LEDGE_COLS, Q
from fls.repo.ghi_tay import TRUONG_GHI


def _map_truong_chu_cai() -> dict[str, list[str]]:
    m: dict[str, list[str]] = {}
    for c in LEDGE_COLS:
        d = c.di_dau
        if d and not d.startswith(K) and not d.startswith(Q):
            m.setdefault(d, []).append(c.letter)
    return m


def test_MOI_truong_nguoi_go_co_DUNG_MOT_cot_nguon__hay_duoc_KHAI():
    m = _map_truong_chu_cai()
    khong_nguon = {f for f in TRUONG_GHI if not m.get(f)}
    assert khong_nguon == set(CHUA_NOI), (
        "⛔ Truong nguoi go ma khong co cot nguon PHAI duoc khai trong "
        f"`ledge_spec.CHUA_NOI` kem cau hoi.\n"
        f"   chua khai : {sorted(khong_nguon - set(CHUA_NOI))}\n"
        f"   khai thua : {sorted(set(CHUA_NOI) - khong_nguon)}")
    for f in TRUONG_GHI:
        if f in CHUA_NOI:
            continue
        assert len(m[f]) == 1, (
            f"⛔ `{f}` co {len(m[f])} cot nguon {m[f]} — mot truong hai nguon "
            "la hai ban su that")


def test_MOI_muc_CHUA_NOI_phai_kem_MOT_CAU_HOI__khong_chi_mot_ghi_chu():
    """⛔ Khai ra ma khong co cau hoi thi no la mot ghi chu, ⛔ khong phai mot no."""
    for f, ly_do in (CHUA_NOI | CHUA_NOI_NGUOC).items():
        assert "?" in ly_do, f"`{f}`: khai ra ma ⛔ khong co CAU HOI nao"
        assert "GAP-" in ly_do, f"`{f}`: ⛔ khong tro tay den mot GAP nao"
        assert len(ly_do) > 60, f"`{f}`: ly do qua ngan de ai doc cung hieu"


def test_NAM_cot_vung_ALLOCATE_da_BI_BO_khoi_khuon():
    """⛔⛔ `QĐ-ITL-65` (2026-08-28): nam cot vung ALLOCATE **khong con** trong
    `fls_itl` (migration `0012`).

    ★ Vi sao bai nay ton tai thay vi chi... khong co gi. Mot cot bi bo rat de
    quay lai: nguoi sau doc `ledge_spec` thay `AU/AV/AW`, thay `fls_itl` khong
    co cho chua, va "chua" bang cach them cot. Bai nay chan dung viec do, va
    thong bao noi ro phai mo lai quyet dinh nao.

    Ly do bo, gon: ca ba o la CONG THUC — suy lai duoc tu `cdt1` + `hd` +
    `fls_mapping_master` (`ledger/allocate.py`) — va owner chot ke toan ⛔ khong
    sua vung nay (`QĐ-ITL-64`) nen hai cot `*_classify` cung ⛔ het nghia.
    """
    ten = {c.name for c in TABLES["fls_itl"].columns}
    vung = {"cdt1_cfa1", "cdt1_cfa2", "cdt1_cfa2_classify",
            "alloc_method", "alloc_method_classify"}
    con = vung & ten
    assert not con, (
        f"⛔ {sorted(con)} da quay lai `fls_itl`. Nam cot nay BI BO co y "
        "(`QĐ-ITL-65`, migration `0012`): chung SUY LAI DUOC tu `cdt1` + `hd` + "
        "`fls_mapping_master` — xem `fls/ledger/allocate.py`. Them lai = tao "
        "mot cot thu hai canh mot con so suy duoc ⇒ hai ban su that. Muon them "
        "thi phai mo lai `QĐ-ITL-64` va `QĐ-ITL-65` truoc.")
    # ⛔ Va ⛔ khong con cot nao "khai ma khong noi" nua.
    assert CHUA_NOI_NGUOC == {}, (
        f"⛔ con cot khai ma khong co nguon: {sorted(CHUA_NOI_NGUOC)}")


def test_KHONG_chu_cai_nao_tro_tao_HAI_truong():
    """`AV` tung bi hai file khai ve hai truong khac nhau — chan huong do."""
    theo_cot: dict[str, str] = {}
    for c in LEDGE_COLS:
        d = c.di_dau
        if d and not d.startswith(K) and not d.startswith(Q):
            assert c.letter not in theo_cot, (
                f"⛔ cot `{c.letter}` tro tao ca `{theo_cot[c.letter]}` va `{d}`")
            theo_cot[c.letter] = d
