import os

import pytest

from fls.db.kho import dung_lai_kho_test, tao_kho_test


def pytest_addoption(parser):
    parser.addoption("--update-golden", action="store_true",
                     help="ghi lai anh chup DDL/ERD")
    parser.addoption("--giu-kho", action="store_true",
                     help="⛔ KHONG dung lai kho test dau phien (soi hien truong)")


@pytest.fixture(scope="session", autouse=True)
def kho_test_san_sang(request):
    """Dung lai kho TEST TU DAU roi ap het di tru, TRUOC moi test PG.

    ⛔ Neu buoc nay im lang that bai thi test PG se do voi loi "khong co bang"
    — do la dieu MONG DOI: tha do to hon la lang le quay ve kho that.

    ★★ **Vi sao DUNG LAI, ⛔ khong chi "tao neu chua co"** (`GAP-KHO-02`).
    Ban cu chi goi `tao_kho_test()` nen kho **⛔ khong bao gio duoc don**. Do
    2026-09-07: `fls_itl` **56.323** dong, **43.573 (77,4%)** la rac cua chinh
    bo test — **+22.831 dong trong 4 ngay**. Hau qua ⛔ khong phai ton dia:
    `GET /gates` cham toi **16,1s** > timeout **10s** cua client ⇒ **5 bai DO
    ma ⛔ khong phai loi code**. Va mot bo test co 5 bai do thuong truc thi
    ⛔ khong con ai doc mau do nua — bai do THAT se di qua trong im lang.

    ⚠ **Don o DAU phien, ⛔ khong phai cuoi.** Cuoi phien thi test vua hong se
    mat luon hien truong. Dau phien vua chan phinh (rac song toi da MOT luot)
    vua giu duoc dau vet de soi. Muon giu han thi `pytest --giu-kho`.

    ⛔ Duong dung lai la `DROP DATABASE` — ⛔ khong phai DELETE (bi `INV-I03`
    chan) va ⛔ khong phai TRUNCATE (bi di tru `0015` chan). Xem `kho.py`.
    """
    giu = request.config.getoption("--giu-kho") or os.environ.get("FLS_GIU_KHO")
    try:
        if giu:
            tao_kho_test()
        else:
            dung_lai_kho_test()
    except Exception as e:                      # noqa: BLE001
        # ⛔ khong nuot: in ra roi de test PG do
        print(f"⛔ khong dung duoc kho TEST: {e}")
