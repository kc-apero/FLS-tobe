"""CONG: schema kho du lieu co DU nhu sheet chua? — cau hoi cua owner 26/08.

Truoc cong nay, cau tra loi phai so bang mat giua 64 cot sheet va 44 cot bang.
So bang mat thi truot — va da truot thật: bon gia tri lop so tinh ra bi tang ghi
BO ROI IM LANG (`id_payee`, `invoice`, `id_payee_thyt`, `invoice_thyt`), trong
do HAI cot dau DB co san ma khong ai ghi vao.
"""
from __future__ import annotations

from fls.db.schema import TABLES
from fls.oracle.ledge_spec import (COT_CHUA_QUYET, COT_KHONG_LUU, COT_LUU,
                                   LEDGE_COLS, SO_CHUA_QUYET, SO_COT,
                                   dich_cua)
from fls.repo.itl_repo import _COT

_ITL = TABLES["fls_itl"]
_COT_DB = {c.name for c in _ITL.columns}


def test_khuon_du_64_cot_khong_trung_chu_cai():
    assert SO_COT == 64
    letters = [c.letter for c in LEDGE_COLS]
    assert len(set(letters)) == 64
    assert letters[0] == "A" and letters[-1] == "BL"


def test_moi_cot_khai_KHONG_LUU_deu_co_ly_do_bang_chu():
    """⛔ Khong duoc phep 'khong luu' ma khong noi vi sao (ACC-4)."""
    for c in COT_KHONG_LUU:
        ly_do = c.di_dau.removeprefix("KHONG LUU: ").strip()
        assert len(ly_do) >= 20, f"{c.letter} ({c.name}): ly do qua mong: {ly_do!r}"


def test_moi_dich_deu_la_cot_CO_THAT_trong_fls_itl():
    """★ Cong chinh. Doi ten cot DB ma quen sua khai bao => DO."""
    thieu = [(c.letter, c.name, c.di_dau) for c in COT_LUU
             if c.di_dau not in _COT_DB]
    assert not thieu, ("cot sheet tro tới cot DB KHONG TON TAI:\n  "
                       + "\n  ".join(f"{a} {b!r} -> {d}" for a, b, d in thieu))


def test_bay_khoi_deu_co_DU_cap_Final_va_thyt():
    """★★ Cong bat dung lo da tim ra: khoi 6-7 thieu cot noi that.

    Bay khoi cua sheet, moi khoi mot cot `Final` -> mot cot DB, va cot DB do
    PHAI co ban `_thyt` di kem (co che 'cho noi that', QD-ITL-35).
    """
    final_cua_khoi = ("V", "Z", "AD", "AH", "AL", "AP", "AT")
    thieu = []
    for lt in final_cua_khoi:
        cot = dich_cua(lt)
        assert cot in _COT_DB, f"{lt} -> {cot} khong co trong fls_itl"
        if f"{cot}_thyt" not in _COT_DB:
            thieu.append(f"{lt} -> {cot} thieu {cot}_thyt")
    assert not thieu, "khoi thieu cot noi that:\n  " + "\n  ".join(thieu)


def test_tang_ghi_KHONG_BO_ROI_gia_tri_nao_cua_lop_so():
    """★★ Lo da tim ra 26/08: `_gia_tri` kiem khoa THIEU nhung khong kiem khoa
    THUA, nen 4 gia tri lop so tinh ra roi ra ngoai trong im lang.
    """
    from fls.canon.row import CanonRow
    from fls.ledger.build import NgucCanh, dung_dong

    o = [None] * 38
    o[0], o[1], o[3], o[5], o[6], o[32] = "2026-03-01", "FT1", "VND", 100, "R|a", "VVOT"
    p = dung_dong(CanonRow.from_list(o), 5,
                  NgucCanh("R1", "v1", "v1", "v1", "RAW", "Transaction Mapping L1"),
                  khoi={k: ("A", "", "A") for k in
                        ("hd", "pay_type", "cdt1", "svc_start", "svc_end",
                         "id_payee", "invoice")})
    roi = sorted(k for k in p if k not in _COT)
    assert not roi, f"lop so tinh ra ma tang ghi KHONG ghi: {roi}"


def test_moi_cot_repo_ghi_deu_co_that_trong_DB():
    """Chieu nguoc lai: repo khong ghi vao cot khong ton tai."""
    assert not [c for c in _COT if c not in _COT_DB]


def test_sau_phep_AUDIT_KHONG_thanh_cot__vi_lech_la_dieu_MONG_DOI():
    """★ Ly do doi han sau khi owner chot huong cua su that (`QD-ITL-52`).

    Ban dau toi ghi: "ket qua doi soat lien he thong, thuoc bang rieng".
    Owner chot: `Report I General Ledger` la ban THUONG NGUON (gia tri TRUOC khi
    ke toan sua); ban FINAL la chinh `ITL Ledge`.

    ⇒ Lech o sau cot do la **DIEU MONG DOI**. No do KHOI LUONG DA SUA, ⛔ khong
      do cai gi sai. Luu vao `fls_itl` la bien mot con so binh thuong thanh mot
      **bao dong thuong truc** — va bao dong thuong truc thi khong ai doc nua.
    ⇒ Va FLS thay CA HAI so bang MOT kho, nen cho do trot khong con ton tai.

    ⚠ Bang chung so: `tests/oracle/test_doi_soat_gl.py`.
    """
    audit = [c for c in COT_KHONG_LUU
             if c.letter in ("AX", "AZ", "BB", "BD", "BF", "BH")]
    assert len(audit) == 6
    for c in audit:
        assert "QD-ITL-52" in c.di_dau
        assert "DIEU MONG DOI" in c.di_dau


def test_ba_trang_thai_phu_kin_64_cot_khong_chong_nhau():
    tong = len(COT_LUU) + len(COT_KHONG_LUU) + len(COT_CHUA_QUYET)
    assert tong == SO_COT == 64
    # ⛔ 21 -> 18 va 43 -> 46 ngay 2026-08-28: owner dua NGUYEN VAN ba cong
    # thuc cua vung ALLOCATE (`AU`/`AV`/`AW`) va ca ba SUY LAI DUOC tu
    # `cdt1` + `hd` + `Mapping Master` cot K/L ⇒ chuyen sang KHONG LUU.
    # `AU` con la BAN SAO cua `AD` (=`cdt1`) — luu no la hai ban su that.
    assert len(COT_LUU) == 18          # 21 - 3 (vung ALLOCATE suy lai duoc)
    assert len(COT_KHONG_LUU) == 46    # 43 + 3


def test_itl_id_sheet_CHI_de_doi_soat__KHONG_duoc_lam_khoa():
    """Owner chot luu `ITL#` cua so cu lam THAM CHIEU. Phep thu nay chan viec
    no bi dung lam danh tinh — dung loi ma so cu da mac.

    ⛔ Khong duoc: PRIMARY KEY · UNIQUE · nam trong content_key.
    """
    from fls.ledger.build import content_key

    cot = next(c for c in _ITL.columns if c.name == "itl_id_sheet")
    assert not cot.pk and not cot.unique, "itl_id_sheet KHONG duoc lam khoa"
    assert cot.null, "phai cho NULL — so cu co 16 dong mat ma"

    # va no KHONG duoc lot vao khoa doi sanh
    a = content_key("RAW", "ITL Ledge", None, 1, None, "FT1", 0)
    b = content_key("RAW", "ITL Ledge", None, 1, None, "FT1", 0)
    assert a == b                                # khoa khong phu thuoc gi khac
    assert "ITL#" not in a


def test_khong_con_cau_hoi_nao_treo():
    """★ 8 cau hoi ngay 26/08 da giai quyet het: 6 -> GAP-REC-01, R -> luu tham
    chieu, O -> tra ra la khong mat (da co trong canon).

    Neu ai them cot moi vao sheet ma chua quyet luu hay khong => con so lech => DO.
    """
    assert len(COT_CHUA_QUYET) == SO_CHUA_QUYET == 0
