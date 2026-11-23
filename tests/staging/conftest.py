"""Fixture của bài thử staging: một kho scratch + ba vai ứng dụng + đồ GIẢ. Xem `ho_tro.py`."""
from __future__ import annotations

import os

import pytest

from tests.staging import ho_tro as H


@pytest.fixture(scope="module")
def mt(tmp_path_factory):
    """Môi trường bước 02: kho scratch RỖNG do vai quản trị `stg_qt_*` sở hữu (như `gcloud sql databases
    create` — chủ kho là `postgres`, KHÔNG phải `fls_admin`), ba vai có mật khẩu của "Secret Manager"
    GIẢ, và `fls_ghi`/`fls_doc` mang đúng hai tật Cloud SQL gắn (CREATEROLE/CREATEDB + thành viên
    `cloudsqlsuperuser`). Dọn sạch khi xong."""
    pid = os.getpid()
    kho, qt = f"fls_stg_{pid}", f"stg_qt_{pid}"
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho}")
    tao_csu = H.chay_quan_tri("SELECT count(*) = 0 FROM pg_roles WHERE rolname = 'cloudsqlsuperuser'") == "t"
    if tao_csu:
        H.chay_quan_tri("CREATE ROLE cloudsqlsuperuser NOLOGIN CREATEROLE CREATEDB")
    for v in ("fls_admin", "fls_ghi", "fls_doc", qt):
        H.chay_quan_tri(f"DROP ROLE IF EXISTS {v}")
    H.chay_quan_tri(f"CREATE ROLE {qt} LOGIN SUPERUSER PASSWORD '{H.MK['fls-staging-pg-postgres']}'")
    H.chay_quan_tri(f"CREATE ROLE fls_admin LOGIN PASSWORD '{H.MK['fls-staging-pg-fls_admin']}' CREATEROLE CREATEDB")
    H.chay_quan_tri(f"CREATE ROLE fls_ghi LOGIN PASSWORD '{H.MK['fls-staging-pg-fls_ghi']}' CREATEROLE CREATEDB")
    H.chay_quan_tri(f"CREATE ROLE fls_doc LOGIN PASSWORD '{H.MK['fls-staging-pg-fls_doc']}' CREATEROLE CREATEDB")
    H.chay_quan_tri("GRANT cloudsqlsuperuser TO fls_ghi, fls_doc")
    H.chay_quan_tri(f"CREATE DATABASE {kho} OWNER {qt}")
    gia = H.dung_gia(tmp_path_factory.mktemp("gia"))
    yield {"kho": kho, "qt": qt, "gia": gia}
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")
    for v in ("fls_admin", "fls_ghi", "fls_doc", qt):
        H.chay_quan_tri(f"DROP ROLE IF EXISTS {v}")
    if tao_csu:
        H.chay_quan_tri("DROP ROLE IF EXISTS cloudsqlsuperuser")
