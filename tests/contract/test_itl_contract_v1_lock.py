from fls.contract.itl_contract import (CR_DANG_MO, ITL_CONTRACT_V1,
                                       ITL_CONTRACT_V1_1, LECH_HOP_DONG_V1,
                                       LECH_V1_V1_1, VERSION_SONG)
from fls.db.schema import TABLES


def test_dung_14_truong():
    assert len(ITL_CONTRACT_V1) == 14


def test_le_la_cot_P_khong_phai_BL():
    """QD-owner-0820: BL trong 6.379 dong, ruong dan ve 0% thang 8/2026."""
    truong = {t[0]: t[2] for t in ITL_CONTRACT_V1}
    assert truong["le"] == "P"
    assert "BL" not in truong.values()


def test_moi_truong_hop_dong_ton_tai_trong_fls_itl():
    """Kieu phai khop hop dong — TRU nhung lech DA KHAI RA o `LECH_HOP_DONG_V1`.

    ⛔ Con duong bi chan o day la: sua chu `date` thanh `text` trong hop dong da
    dong bang cho test xanh lai. Lech phai co TEN, co CON SO, va co mot CR dang mo.
    """
    cot = {c.name: c for c in TABLES["fls_itl"].columns}
    khai_lech = {t[0]: t for t in LECH_HOP_DONG_V1}
    for ten, kieu, _ in ITL_CONTRACT_V1:
        assert ten in cot, f"hop dong doi {ten} nhung fls_itl khong co"
        if cot[ten].type.startswith(kieu):
            continue
        l = khai_lech.get(ten)
        assert l, (f"{ten}: hop dong {kieu}, schema {cot[ten].type} — lech NAY "
                   f"CHUA KHAI. Them vao LECH_HOP_DONG_V1 kem con so da do, "
                   f"⛔ dung sua hop dong da dong bang")
        assert (l[1], l[2]) == (kieu, cot[ten].type), f"{ten}: khai lech da cu"


def test_moi_LECH_deu_co_con_so():
    """Mot lech khong co con so la mot lech se thanh thoi quen."""
    assert LECH_HOP_DONG_V1, "khong con lech nao thi xoa ca khoi khai di"
    for ten, cu, moi, ly_do in LECH_HOP_DONG_V1:
        assert cu != moi and len(ly_do) >= 60, ten
        assert any(ch.isdigit() for ch in ly_do), f"{ten}: ly do khong co con so nao"


def test_CR2_DA_DONG__ban_song_la_v1_1_va_ban_v1_0_la_LICH_SU():
    """★ Owner chot 2026-08-27, phuong an (a): nang kieu, ⛔ khong them truong rong.

    ⛔ Phuong an (b) bi loai vi truong `svc_start` moi se **khong co nguon du
    lieu nao** — khong cho nao trong nguon mang ngay trong thang. Dung mot cot
    rong lam cho de *"sau nay co thi dien"* la dung cai `P-ITL-05` cam.
    """
    assert VERSION_SONG == "v1.1"
    assert CR_DANG_MO == (), "CR#2 da dong thi danh sach CR mo phai rong"
    kieu = {t[0]: t[1] for t in ITL_CONTRACT_V1_1}
    assert kieu["svc_start"] == kieu["svc_end"] == "text"
    assert {t[0] for t in LECH_V1_V1_1} == {"svc_start", "svc_end"}


def test_v1_1_CHI_doi_dung_hai_truong__khong_gi_khac():
    """Mot ban nang cap "tien the" la ban nang cap khong ai kiem duoc."""
    a = {t[0]: t for t in ITL_CONTRACT_V1}
    b = {t[0]: t for t in ITL_CONTRACT_V1_1}
    assert set(a) == set(b) and len(b) == 14
    doi = {k for k in a if a[k] != b[k]}
    assert doi == {"svc_start", "svc_end"}
    for k in doi:
        assert a[k][2] == b[k][2], f"{k}: ⛔ cot Excel KHONG duoc doi trong v1.1"


def test_ban_SONG_moi_la_ban_di_doi_chieu_voi_schema():
    """Cong nay tro toi `ITL_CONTRACT_V1_1`, khong con lech nao => `LECH` rong dan."""
    cot = {c.name: c for c in TABLES["fls_itl"].columns}
    lech = [(ten, kieu, cot[ten].type) for ten, kieu, _ in ITL_CONTRACT_V1_1
            if ten in cot and not cot[ten].type.startswith(kieu)]
    assert not lech, f"schema lech ban SONG v1.1: {lech}"


def test_hop_dong_v1_KHONG_DOI_MOT_CHU():
    """★ Cong dong bang. QD-ITL-42 dong bang v1.0 ngay 2026-08-24."""
    assert ITL_CONTRACT_V1[12] == ("svc_start", "date", "AH")
    assert ITL_CONTRACT_V1[13] == ("svc_end", "date", "AL")


def test_doc_theo_TEN_khong_theo_vi_tri():
    """QD-ITL-42: doc theo TEN. Cot Excel chi de doi chieu reader that."""
    assert len({t[0] for t in ITL_CONTRACT_V1}) == 14, "ten truong phai duy nhat"
