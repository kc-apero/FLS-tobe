from fls.contract.itl_contract import ITL_CONTRACT_V1
from fls.db.schema import TABLES


def test_dung_14_truong():
    assert len(ITL_CONTRACT_V1) == 14


def test_le_la_cot_P_khong_phai_BL():
    """QD-owner-0820: BL trong 6.379 dong, ruong dan ve 0% thang 8/2026."""
    truong = {t[0]: t[2] for t in ITL_CONTRACT_V1}
    assert truong["le"] == "P"
    assert "BL" not in truong.values()


def test_moi_truong_hop_dong_ton_tai_trong_fls_itl():
    cot = {c.name: c for c in TABLES["fls_itl"].columns}
    for ten, kieu, _ in ITL_CONTRACT_V1:
        assert ten in cot, f"hop dong doi {ten} nhung fls_itl khong co"
        assert cot[ten].type.startswith(kieu), f"{ten}: hop dong {kieu}, schema {cot[ten].type}"


def test_doc_theo_TEN_khong_theo_vi_tri():
    """QD-ITL-42: doc theo TEN. Cot Excel chi de doi chieu reader that."""
    assert len({t[0] for t in ITL_CONTRACT_V1}) == 14, "ten truong phai duy nhat"
