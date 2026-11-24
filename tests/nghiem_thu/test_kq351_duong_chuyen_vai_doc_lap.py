"""KQ-351 (R2b2) — đường chuyển vai `STG-R2b-02`, đo ĐỘC LẬP với `tests/staging/test_02_chuyen_vai_gcp.py`.

Khác bài Dev: (1) trạng thái đầu vào dựng bằng CHÍNH script bước 02 CŨ `fa2c07e` (không giả lập tay);
(2) có DỮ LIỆU thật trong kho (mẫu số ≠ 0 — Đ3) và so đếm dòng mọi bảng trước = sau; (3) quét `/proc/*/cmdline`
TRONG lúc script chạy tìm mật khẩu giả (argv); (4) lỗi giữa chừng ⇒ đo trạng thái vai + chạy lại phục hồi.
Dùng đồ giả/`dung_vai_cloud_sql` của `tests/staging/ho_tro.py` (chỉ đọc, ⛔ sửa).
"""
from __future__ import annotations

import os
import re
import subprocess
import threading
import time
from pathlib import Path

import pytest

from tests.staging import ho_tro as H

GOC = H.GOC
S02 = "02_di_tru_phan_quyen.sh"
MUC = "fls_ghi/fls_doc: siêu quyền hay CREATEROLE/CREATEDB (đếm vai)"


@pytest.fixture
def cu(tmp_path):
    """Cây script CŨ (`fa2c07e`) để dựng trạng thái 'GCP hiện tại': bước 02 cũ đã chạy, vai còn bẩn."""
    r = subprocess.run(["git", "-C", str(GOC), "cat-file", "-e", "fa2c07e"], capture_output=True)
    if r.returncode:
        pytest.skip("không có commit fa2c07e")
    d = tmp_path / "cu"
    (d / "tools").mkdir(parents=True)
    subprocess.run(f"git -C {GOC} archive fa2c07e tools/staging | tar -x -C {d}", shell=True, check=True)
    os.symlink(GOC / "fls", d / "fls")
    os.symlink(GOC / "requirements.txt", d / "requirements.txt")
    return d


@pytest.fixture(params=["H-A", "H-B"])
def mt(request, tmp_path):
    pid = os.getpid()
    kho, qt = f"fls_kq351_{request.param[-1].lower()}_{pid}", f"kq351_qt_{request.param[-1].lower()}_{pid}"
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")
    don = H.dung_vai_cloud_sql(qt, request.param)
    H.chay_quan_tri(f"CREATE DATABASE {kho} OWNER {qt}")
    yield {"kho": kho, "qt": qt, "kieu": request.param, "gia": H.dung_gia(tmp_path / "gia")}
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")
    don()


def _chay(m, ten=S02, *args, goc=None, env_them=None):
    if goc is None:
        return H.chay_script(ten, m["gia"], m["kho"], m["qt"], *args, env_them=env_them)
    old = H.STG
    H.STG = goc / "tools" / "staging"
    try:
        return H.chay_script(ten, m["gia"], m["kho"], m["qt"], *args, env_them=env_them)
    finally:
        H.STG = old


def _dem_moi_bang(kho):
    """{bảng: số dòng} cho MỌI bảng public (đếm thật)."""
    ds = H.chay_quan_tri("SELECT relname FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                         "WHERE nspname='public' AND relkind IN ('r','p') ORDER BY 1", kho).split()
    return {t: int(H.chay_quan_tri(f"SELECT count(*) FROM public.{t}", kho)) for t in ds}


def _thuoc_tinh(vai):
    return H.chay_quan_tri(f"SELECT rolcreaterole::text||rolcreatedb::text||rolsuper::text||rolreplication::text||rolbypassrls::text "
                           f"FROM pg_roles WHERE rolname='{vai}'")


def _dung_trang_thai_cu(m, cu):
    """Chạy 02 CŨ — dựng đúng trạng thái GCP hiện tại — rồi nạp dữ liệu thật."""
    if m["kieu"] == "H-B":
        r = _chay(m, goc=cu)
        # 02 cũ: ĐỎ đúng mục siêu quyền (tái hiện báo cáo của chủ) — nếu không đỏ thì mô phỏng không còn bẩn
        assert H.dong_bao_cao(r.stdout).get(MUC) == "ĐỎ", r.stdout[-1500:] + r.stderr[-500:]
    else:   # H-A mâu thuẫn với sự thật đã đo (02a cũ nổ) ⇒ dựng bằng 02 mới rồi trả vai về hình gcloud-tạo
        assert _chay(m).returncode == 0
        for v in ("fls_ghi", "fls_doc"):
            H.chay_quan_tri(f"ALTER ROLE {v} CREATEROLE CREATEDB; REVOKE {v} FROM {m['qt']}")
        H.chay_quan_tri("GRANT cloudsqlsuperuser TO fls_doc")
    kho = m["kho"]
    H.chay_quan_tri("INSERT INTO fls_mapping_master (hd_code) VALUES ('KQ351-A'),('KQ351-B')", kho)
    H.chay_quan_tri("INSERT INTO fls_sua_tay DEFAULT VALUES", kho) if False else None
    dem = _dem_moi_bang(kho)
    assert sum(dem.values()) > 0 and len(dem) >= 20, dem      # Đ3: mẫu số
    assert dem["fls_mapping_master"] >= 2
    return dem


class _SoiArgv(threading.Thread):
    """Quét /proc/*/cmdline mỗi 20ms tìm 'MKGIA-' trong lúc script chạy."""
    def __init__(self):
        super().__init__(daemon=True)
        self.dung, self.thay, self.lan_quet, self.tien_trinh = False, set(), 0, set()

    def run(self):
        me = os.getpid()
        while not self.dung:
            for p in Path("/proc").iterdir():
                if not p.name.isdigit() or int(p.name) == me:
                    continue
                try:
                    c = (p / "cmdline").read_bytes()
                except OSError:
                    continue
                self.tien_trinh.add(c.split(b"\0")[0][-20:])
                if b"MKGIA-" in c:
                    self.thay.add(c[:120])
            self.lan_quet += 1
            time.sleep(0.02)


def test_duong_chuyen_giu_du_lieu_chay_lai_idempotent_va_khong_ro_mat_khau(mt, cu):
    kho = mt["kho"]
    dem0 = _dung_trang_thai_cu(mt, cu)
    chu0 = H.chay_quan_tri("SELECT string_agg(DISTINCT pg_get_userbyid(relowner),',') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                           "WHERE nspname='public' AND relkind IN ('r','p','v','S')", kho)
    assert chu0 == "fls_admin"
    assert _thuoc_tinh("fls_ghi").startswith("truetrue"), "trạng thái đầu KHÔNG bẩn"
    # ── chạy mới, soi argv
    soi = _SoiArgv(); soi.start()
    r = _chay(mt)
    soi.dung = True; soi.join()
    out = r.stdout + r.stderr
    assert r.returncode == 0 and "KẾT: ĐẠT" in r.stdout, out[-3000:]
    assert out.count("ĐƯỜNG CHUYỂN") == 2 and out.count("ⓐ thu mọi quyền") == 2 and out.count("ⓒ CREATE ROLE") == 2, out
    # thuộc tính + nhóm
    for v in ("fls_ghi", "fls_doc"):
        assert _thuoc_tinh(v) == "falsefalsefalsefalsefalse", (v, _thuoc_tinh(v))
    assert H.chay_quan_tri("SELECT count(*) FROM pg_roles WHERE rolname IN ('fls_ghi','fls_doc')") == "2"          # mẫu số
    # quyền 02b
    q = lambda vai, b: H.chay_quan_tri("SELECT coalesce(string_agg(p, ',' ORDER BY p), '') FROM unnest(ARRAY['SELECT','INSERT','UPDATE','DELETE','TRUNCATE','REFERENCES','TRIGGER']) p "
                                       f"WHERE has_table_privilege('{vai}', 'public.{b}', p)", kho)
    assert q("fls_ghi", "fls_itl") == "INSERT,SELECT"
    assert q("fls_ghi", "fls_migration") == "SELECT"
    assert q("fls_ghi", "fls_mapping_master") == "DELETE,INSERT,SELECT,UPDATE"
    assert q("fls_doc", "fls_itl") == "SELECT" and q("fls_doc", "fls_mapping_master") == "SELECT"
    assert H.chay_quan_tri("SELECT rolconfig::text FROM pg_roles WHERE rolname='fls_doc'") == "{default_transaction_read_only=on}"
    # DỮ LIỆU: đếm dòng từng bảng trước = sau; chủ bảng không đổi
    dem1 = _dem_moi_bang(kho)
    assert dem1 == dem0, {k: (dem0[k], dem1.get(k)) for k in dem0 if dem0[k] != dem1.get(k)}
    assert H.chay_quan_tri("SELECT string_agg(DISTINCT pg_get_userbyid(relowner),',') FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace "
                           "WHERE nspname='public' AND relkind IN ('r','p','v','S')", kho) == chu0
    # rò mật khẩu: màn, nhật ký proxy/gcloud, argv sống
    gop = out + mt["gia"]["proxy_log"].read_text() + mt["gia"]["gcloud_log"].read_text()
    assert "MKGIA-" not in gop
    assert soi.lan_quet >= 20 and b"psql" in b" ".join(soi.tien_trinh), (soi.lan_quet, "bộ quét không thấy psql — phép đo rỗng")
    assert not soi.thay, soi.thay
    # ── chạy lại lần 2
    r2 = _chay(mt)
    assert r2.returncode == 0 and r2.stdout.count("SẠCH ⇒ đồng bộ mật khẩu") == 2 and "ĐƯỜNG CHUYỂN" not in r2.stdout, r2.stdout[-1500:]
    assert _dem_moi_bang(kho) == dem0
    assert q("fls_ghi", "fls_itl") == "INSERT,SELECT"


def test_loi_giua_chung_DUNG_co_ten_bao_trang_thai_va_chay_lai_phuc_hoi(mt, cu):
    kho = mt["kho"]
    dem0 = _dung_trang_thai_cu(mt, cu)
    ghi = mt["gia"]["dir"] / "secret_fls-staging-pg-fls_ghi"
    tot = ghi.read_text()
    ghi.write_text("MKGIA-ghi-hong'; --")         # sai khuôn ⇒ CREATE không làm được SAU khi DROP đã chạy
    r = _chay(mt)
    assert r.returncode == 1 and "VAI_KHONG_TAO_DUOC: fls_ghi" in r.stderr, r.stdout + r.stderr
    assert "đã xoá" in r.stderr and "chạy lại 02" in r.stderr           # BÁO CÁO nói rõ vai đã xoá chưa
    assert "BÁO CÁO (KHÔNG" not in r.stdout                               # ⛔ đi tiếp
    # đo THẬT: fls_ghi đã mất, fls_doc ⛔ bị chạm
    assert H.chay_quan_tri("SELECT count(*) FROM pg_roles WHERE rolname='fls_ghi'") == "0"
    assert H.chay_quan_tri("SELECT count(*) FROM pg_roles WHERE rolname='fls_doc'") == "1"
    assert _dem_moi_bang(kho) == dem0, "dữ liệu mất khi dừng giữa chừng"
    assert "MKGIA-" not in r.stdout + r.stderr
    # phục hồi: sửa bí mật, chạy lại ⇒ ĐẠT, dữ liệu nguyên
    ghi.write_text(tot)
    r2 = _chay(mt)
    assert r2.returncode == 0 and "KẾT: ĐẠT" in r2.stdout, r2.stdout[-2000:] + r2.stderr[-500:]
    assert _dem_moi_bang(kho) == dem0
    assert _thuoc_tinh("fls_ghi") == "falsefalsefalsefalsefalse"


def test_tinh_khong_co_set_x_echo_mat_khau_hay_argv_mang_mat_khau():
    code = "\n".join(l for l in (H.STG / S02).read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#"))
    assert not re.search(r"set\s+-[a-z]*x", code)
    assert not re.search(r"echo[^\n]*\$\{?MK_", code), "echo mật khẩu"
    assert not re.search(r"-c\s+\"[^\"]*\$\{?MK_", code)
    assert code.count("PGPASSWORD=") >= 2     # mật khẩu đi bằng biến môi trường
