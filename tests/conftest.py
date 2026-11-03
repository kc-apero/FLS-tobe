import pytest

from fls.db.kho import tao_kho_test


def pytest_addoption(parser):
    parser.addoption("--update-golden", action="store_true",
                     help="ghi lai anh chup DDL/ERD")


@pytest.fixture(scope="session", autouse=True)
def kho_test_san_sang():
    """Dam bao kho TEST ton tai + da ap het di tru, TRUOC moi test PG.

    ⛔ Neu buoc nay im lang that bai thi test PG se do voi loi "khong co bang"
    — do la dieu MONG DOI: tha do to hon la lang le quay ve kho that.
    """
    try:
        tao_kho_test()
    except Exception as e:                      # noqa: BLE001
        # ⛔ khong nuot: in ra roi de test PG do
        print(f"⛔ khong dung duoc kho TEST: {e}")
