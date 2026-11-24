"""Bước 02 — `STG-R2b-02` (`KQ-344`): lỗi THẬT GCP 23/11 — `fls_ghi`/`fls_doc` còn CREATEROLE/CREATEDB.

⭐ Lỗi đã xảy ra (chủ chạy bước 02 ở Cloud Shell, ngọn `c4a0f39`): BÁO CÁO 23/24 ĐẠT, ĐỎ đúng mục
`fls_ghi/fls_doc: siêu quyền hay CREATEROLE/CREATEDB (đếm vai) = 2`; script in `⚠ không hạ được thuộc tính`.
Bài cũ XANH vì vai quản trị của bài là SUPERUSER — `ALTER ROLE … NOSUPERUSER …` chạy được ở bài, ⛔ ở GCP.

Mô phỏng (`H.dung_vai_cloud_sql`) theo HAI giả thuyết, CẢ HAI ⛔ đo được ở GCP (lỗi gốc bị nuốt):
  `H-B` (fixture `mt` của mọi bài staging) — khớp MỌI sự thật đã đo; mã cũ ⇒ tái hiện ĐÚNG báo cáo GCP.
  `H-A` (tệp này) — vai quản trị ⛔ ADMIN OPTION trên vai app ⇒ `DROP ROLE` SQL bị từ chối ⇒ đường chuyển
        phải rơi sang `gcloud sql users delete`.
Ba trạng thái đầu vào: ⓐ như sau bước 01 cũ (vai gcloud tạo, kho rỗng) · ⓑ như GCP HIỆN TẠI (bước 02 cũ ĐÃ chạy
xong: kho di trú đủ, quyền đã cấp, vai vẫn bẩn) · ⓒ bước 01 mới (vai app CHƯA có).
"""
from __future__ import annotations

import os
import re

import psycopg
import pytest

from tests.staging import ho_tro as H

S02 = "02_di_tru_phan_quyen.sh"
MUC = "fls_ghi/fls_doc: siêu quyền hay CREATEROLE/CREATEDB (đếm vai)"


@pytest.fixture
def mt_a(tmp_path):
    """Kho scratch RỖNG + vai kiểu `H-A`. Mỗi bài một bộ (bài đổi vai)."""
    pid = os.getpid()
    kho, qt = f"fls_stg_a_{pid}", f"stg_qt_a_{pid}"
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")
    don = H.dung_vai_cloud_sql(qt, "H-A")
    H.chay_quan_tri(f"CREATE DATABASE {kho} OWNER {qt}")
    yield {"kho": kho, "qt": qt, "gia": H.dung_gia(tmp_path / "gia")}
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")
    don()


def _chay(m, *args):
    return H.chay_script(S02, m["gia"], m["kho"], m["qt"], *args)


def _ghi_gcloud(m):
    nk = m["gia"]["gcloud_log"].read_text().splitlines()
    return [d for d in nk if re.search(r"\b(create|delete|add-iam-policy-binding|set-password|enable|update|patch)\b", d)]


def _vai_sach_va_dang_nhap_duoc(kho):
    """Đo ĐỘC LẬP script (psycopg + peer postgres): thuộc tính, nhóm, đăng nhập bằng mật khẩu của "Secret Manager"."""
    assert H.chay_quan_tri("SELECT count(*) FROM pg_roles WHERE rolname IN ('fls_ghi','fls_doc') AND (rolsuper OR "
                           "rolcreaterole OR rolcreatedb OR rolreplication OR rolbypassrls)") == "0"
    assert H.chay_quan_tri("SELECT count(*) FROM pg_auth_members m JOIN pg_roles g ON g.oid = m.roleid JOIN pg_roles u "
                           "ON u.oid = m.member WHERE g.rolname = 'cloudsqlsuperuser' AND u.rolname IN ('fls_ghi','fls_doc')") == "0"
    for vai in ("fls_ghi", "fls_doc"):
        dsn = f"postgresql://{vai}:{H.MK['fls-staging-pg-' + vai]}@127.0.0.1:{H.cong_pg()}/{kho}"
        with psycopg.connect(dsn, autocommit=True) as c:
            ro = c.execute("SHOW default_transaction_read_only").fetchone()[0]
            assert ro == ("on" if vai == "fls_doc" else "off"), (vai, ro)
            assert c.execute("SELECT count(*) FROM fls_itl").fetchone()[0] == 0


def _khong_ro(r, m):
    gop = r.stdout + r.stderr + m["gia"]["proxy_log"].read_text()
    assert not re.search(r"MKGIA-", gop), "mật khẩu GIẢ rò ra màn"


# ══ ⓐ trạng thái sau bước 01 CŨ: vai gcloud tạo, kho rỗng ═══════════════════════════════════════

def test_HA_vai_gcloud_tao_thi_xoa_qua_gcloud_roi_tao_lai_bang_SQL_va_DAT(mt_a):
    r = _chay(mt_a)
    out = r.stdout
    assert r.returncode == 0 and "KẾT: ĐẠT" in out, out + r.stderr
    assert H.dong_bao_cao(out)[MUC] == "ĐẠT"
    # đường chuyển: ĐO trước (giả thuyết in ra) → DROP SQL bị từ chối (lỗi PG THẬT in ra, ⛔ nuốt) → gcloud → CREATE SQL
    assert out.count("ĐƯỜNG CHUYỂN") == 2, out
    assert len(re.findall(r"có ADMIN OPTION=false", out)) == 2, out
    assert len(re.findall(r"DROP ROLE fls_(ghi|doc) bằng SQL bị từ chối — PG nói: .*ADMIN option", out)) == 2, out
    assert _ghi_gcloud(mt_a) == [f"--project=du-an-gia --quiet sql users delete {v} --instance=fls-staging"
                                 for v in ("fls_ghi", "fls_doc")], _ghi_gcloud(mt_a)
    assert re.search(r"vai quản trị có ADMIN OPTION trên fls_ghi/fls_doc \(đếm vai\)\s+2\b", out), out
    _vai_sach_va_dang_nhap_duoc(mt_a["kho"])
    _khong_ro(r, mt_a)
    # chạy lại: vai SẠCH ⇒ chỉ đồng bộ mật khẩu, ⛔ gọi gcloud ghi nữa
    mt_a["gia"]["gcloud_log"].write_text("")
    r2 = _chay(mt_a)
    assert r2.returncode == 0 and r2.stdout.count("SẠCH ⇒ đồng bộ mật khẩu") == 2 and "ĐƯỜNG CHUYỂN" not in r2.stdout
    assert _ghi_gcloud(mt_a) == []


# ══ ⓑ trạng thái GCP HIỆN TẠI: bước 02 cũ đã chạy xong (quyền đã cấp), vai vẫn bẩn ═════════════════

@pytest.mark.parametrize("kieu", ["H-A", "H-B"])
def test_GCP_hien_tai_da_chay_02_cu_thi_duong_chuyen_THU_quyen_roi_xoa_tao_lai_va_DAT(mt_a, kieu):
    """Dựng đúng trạng thái chủ đang có: chạy 02 (được kho di trú + quyền 02b), rồi trả vai về hình gcloud-tạo
    (CREATEROLE/CREATEDB · thành viên `cloudsqlsuperuser` · `H-A`: thu ADMIN OPTION của vai quản trị). Vai còn được
    cấp quyền ⇒ `DROP ROLE` (SQL lẫn gcloud) ĐỎ nếu đường chuyển ⛔ THU quyền trước."""
    assert _chay(mt_a).returncode == 0
    qt = mt_a["qt"]
    for v in ("fls_ghi", "fls_doc"):
        H.chay_quan_tri(f"ALTER ROLE {v} CREATEROLE CREATEDB; REVOKE {v} FROM {qt}")
        if kieu == "H-B":
            H.chay_quan_tri(f"GRANT {v} TO cloudsqlsuperuser WITH ADMIN OPTION, INHERIT FALSE, SET FALSE")
    H.chay_quan_tri("GRANT cloudsqlsuperuser TO fls_doc") if kieu == "H-A" else None
    truoc = _chay(mt_a, "--kiem")
    assert truoc.returncode == 1 and H.dong_bao_cao(truoc.stdout)[MUC] == "ĐỎ", truoc.stdout   # tái hiện GCP: ĐỎ
    mt_a["gia"]["gcloud_log"].write_text("")
    r = _chay(mt_a)
    assert r.returncode == 0 and "KẾT: ĐẠT" in r.stdout, r.stdout + r.stderr
    assert r.stdout.count("ⓐ thu mọi quyền") == 2 and r.stdout.count("ⓒ CREATE ROLE") == 2, r.stdout
    assert len(_ghi_gcloud(mt_a)) == (2 if kieu == "H-A" else 0), _ghi_gcloud(mt_a)
    _vai_sach_va_dang_nhap_duoc(mt_a["kho"])
    _khong_ro(r, mt_a)


def test_gcloud_xoa_vai_hong_thi_loi_CO_TEN_exit_1_va_vai_van_con(mt_a):
    (mt_a["gia"]["dir"] / "xoa_vai_hong").touch()
    r = _chay(mt_a)
    assert r.returncode == 1 and "VAI_KHONG_XOA_DUOC: fls_ghi" in r.stderr, r.stdout + r.stderr
    assert "BÁO CÁO" not in r.stdout, "đi tiếp sau khi ⛔ xoá được vai"
    assert H.chay_quan_tri("SELECT count(*) FROM pg_roles WHERE rolname IN ('fls_ghi','fls_doc')") == "2"


# ══ ⓒ bước 01 MỚI: vai app CHƯA có ⇒ tạo bằng SQL ══════════════════════════════════════════════

def test_vai_app_chua_co_thi_tao_bang_SQL_khong_goi_gcloud_ghi(mt_a):
    H.chay_quan_tri("DROP ROLE fls_ghi; DROP ROLE fls_doc")
    r = _chay(mt_a)
    assert r.returncode == 0 and r.stdout.count("tạo bằng SQL (LOGIN NOCREATEDB NOCREATEROLE)") == 2, r.stdout + r.stderr
    assert _ghi_gcloud(mt_a) == []
    _vai_sach_va_dang_nhap_duoc(mt_a["kho"])
    _khong_ro(r, mt_a)


def test_tao_vai_bi_PG_tu_choi_thi_DUNG_va_loi_PG_KHONG_mang_mat_khau(mt_a):
    H.chay_quan_tri("DROP ROLE fls_ghi; DROP ROLE fls_doc")
    H.chay_quan_tri(f"ALTER ROLE {mt_a['qt']} NOCREATEROLE")
    r = _chay(mt_a)
    assert r.returncode == 1 and "VAI_KHONG_TAO_DUOC: fls_ghi" in r.stderr, r.stdout + r.stderr
    assert re.search(r"PG nói: .*permission denied to create role", r.stdout), r.stdout
    _khong_ro(r, mt_a)


def test_bi_mat_ky_tu_la_thi_DUNG_truoc_khi_cham_vai(mt_a):
    H.chay_quan_tri("DROP ROLE fls_ghi; DROP ROLE fls_doc")
    (mt_a["gia"]["dir"] / "secret_fls-staging-pg-fls_ghi").write_text("MKGIA-ghi-x'; DROP ROLE fls_admin; --")
    r = _chay(mt_a)
    assert r.returncode == 1 and "ký tự ngoài [A-Za-z0-9_-]" in r.stderr, r.stdout + r.stderr
    assert H.chay_quan_tri("SELECT count(*) FROM pg_roles WHERE rolname = 'fls_admin'") == "1"
    _khong_ro(r, mt_a)


def test_tinh_buoc_02_KHONG_con_ALTER_NOSUPERUSER_va_KHONG_nuot_loi_vai():
    code = "\n".join(l for l in (H.STG / S02).read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))
    assert "NOSUPERUSER" not in code, "mệnh đề này bị PG16 từ chối cho vai ⛔ siêu người dùng (`STG-R2b-02`)"
    assert "không hạ được thuộc tính" not in code
    assert "CREATE ROLE %s LOGIN NOCREATEDB NOCREATEROLE" in code
