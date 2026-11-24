"""Fixture của bài thử staging: một kho scratch + ba vai ứng dụng + đồ GIẢ. Xem `ho_tro.py`."""
from __future__ import annotations

import os

import pytest

from tests.staging import ho_tro as H


@pytest.fixture(scope="module")
def mt(tmp_path_factory):
    """Môi trường bước 02: kho scratch RỖNG do vai quản trị `stg_qt_*` sở hữu (như `gcloud sql databases
    create` — chủ kho là `postgres`, KHÔNG phải `fls_admin`), ba vai có mật khẩu của "Secret Manager"
    GIẢ, dựng theo đúng hình Cloud SQL PG16 đã ĐO (`H.dung_vai_cloud_sql`, kiểu `H-B`):
    vai quản trị ⛔ siêu người dùng, có ADMIN OPTION (qua `cloudsqlsuperuser`) trên vai gcloud tạo;
    `fls_ghi`/`fls_doc` mang CREATEROLE + CREATEDB. Dọn sạch khi xong.

    ⭐ `STG-R2b-02`: trước đây vai quản trị là SUPERUSER ⇒ `ALTER ROLE … NOSUPERUSER …` của bản cũ chạy được ở
    đây và bài XANH, trong khi ở GCP nó bị từ chối ⇒ lỗi thật lọt cổng giả."""
    pid = os.getpid()
    kho, qt = f"fls_stg_{pid}", f"stg_qt_{pid}"
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho}")
    don = H.dung_vai_cloud_sql(qt, "H-B")
    H.chay_quan_tri(f"CREATE DATABASE {kho} OWNER {qt}")
    gia = H.dung_gia(tmp_path_factory.mktemp("gia"))
    yield {"kho": kho, "qt": qt, "gia": gia}
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")
    don()


@pytest.fixture(scope="module")
def kho_san(mt):
    """Kho scratch đã qua bước 02 (di trú + phân quyền) — nền để chạy `vao.sh`/`04` bằng vai `fls_doc`/`fls_ghi` THẬT."""
    r = H.chay_script("02_di_tru_phan_quyen.sh", mt["gia"], mt["kho"], mt["qt"])
    assert r.returncode == 0, r.stdout + r.stderr
    return mt
