"""Bài thử `tools/staging/02_di_tru_phan_quyen.sh` — `WO-325` AC-1.

⭐ Cách chứng minh (xem `ho_tro.py`): `gcloud` + `cloud-sql-proxy` GIẢ; `psql` · `pg_migrate` ·
`GRANT/REVOKE` **THẬT** trên kho scratch. Ba lớp:

  ⓐ ĐÚNG ⇒ ĐẠT          — chạy "làm" trên kho RỖNG: di trú đủ, `pg_verify: khop`, quyền đúng, exit 0.
  ⓑ HỎNG TỪNG MỤC ⇒ ĐÚNG MỤC ĐỎ — phá MỘT thứ bằng superuser, đo `--kiem`: exit 1 và tập mục ĐỎ
     BẰNG ĐÚNG tập mong (⛔ "có ĐỎ nào đó"); rồi chạy lại "làm" ⇒ lành (chạy-lại-được).
  ⓒ ĐO KHÔNG ĐƯỢC ⇒ ĐỎ  — kho rỗng (mẫu số 0, `Đ3`) · `psql`/`python` hỏng ⇒ 0 mục ĐẠT (`Đ5`).
"""
from __future__ import annotations

import glob
import os
import re
import stat
import subprocess

import psycopg
import pytest

from tests.staging import ho_tro as H

S02 = "02_di_tru_phan_quyen.sh"
SO_TEP = len(glob.glob(str(H.GOC / "fls" / "db" / "migrations" / "*.sql")))


def _chay(mt, *args, **kw):
    return H.chay_script(S02, mt["gia"], mt["kho"], mt["qt"], *args, **kw)


def _dsn(vai: str, kho: str) -> str:
    return f"postgresql://{vai}:{H.MK['fls-staging-pg-' + vai]}@127.0.0.1:{H.cong_pg()}/{kho}"


@pytest.fixture(scope="module")
def da_lam(mt):
    """Chạy "làm" MỘT lần trên kho scratch rỗng ⇒ trạng thái chuẩn mà các bài ⓑ phá rồi trả."""
    r = _chay(mt)
    return r


# ══ ⓐ ĐÚNG ⇒ ĐẠT ═════════════════════════════════════════════════════════════════════════════

def test_lam_tren_kho_rong_ra_DAT_exit_0(da_lam):
    out = da_lam.stdout
    assert da_lam.returncode == 0, out + da_lam.stderr
    assert "KẾT: ĐẠT" in out, out
    assert "pg_verify: khop" in out, "③ di trú phải in `pg_verify: khop` (pg_migrate tự chạy pg_verify)"
    do = H.muc_do(out)
    dat = {k for k, v in H.dong_bao_cao(out).items() if v == "ĐẠT"}
    assert not do, do
    # Đ4: nhãn nói NÓ ĐẾM GÌ; số mục đo ≥ 20 (không phải một báo cáo rỗng ĐẠT trên tập rỗng — Đ3)
    assert len(dat) >= 20, f"chỉ {len(dat)} mục ĐẠT: {sorted(dat)}"
    m = re.search(r"di trú đã áp = số tệp\s+True", out)
    assert m, out
    assert f"tệp di trú trong repo (đếm)" in out and re.search(rf"tệp di trú trong repo \(đếm\)\s+{SO_TEP}\b", out), \
        (SO_TEP, out)


def test_KHONG_ro_mat_khau_ra_stdout_stderr_hay_log_proxy(da_lam, mt):
    gop = da_lam.stdout + da_lam.stderr + mt["gia"]["proxy_log"].read_text()
    ro = [ten for ten, mk in H.MK.items() if mk in gop]
    assert ro == [], f"mật khẩu GIẢ rò ra: {ro}"
    assert not re.search(r"MKGIA-", gop)


def test_gcloud_chi_goi_lenh_DOC_va_proxy_dung_doi_so_va_duoc_dep(da_lam, mt):
    nk = mt["gia"]["gcloud_log"].read_text().splitlines()
    assert nk, "script ⛔ gọi gcloud nào?"
    cam = re.compile(r"\b(create|delete|add-iam-policy-binding|set-password|enable|update|patch|set-iam)\b")
    assert not [d for d in nk if cam.search(d)], f"lệnh GHI lọt vào bước 02: {nk}"
    # chỉ hai loại lệnh: đọc bí mật (4 vai, ⛔ jwt) + mô tả máy
    kieu = {("secrets" if " secrets " in " " + d else "sql" if " sql instances describe" in " " + d else d) for d in nk}
    assert kieu == {"secrets", "sql"}, kieu
    bi_mat = [d for d in nk if "secrets versions access" in d]
    assert sorted(re.search(r"--secret=(\S+)", d).group(1) for d in bi_mat) == sorted(
        ["fls-staging-pg-postgres", "fls-staging-pg-fls_admin", "fls-staging-pg-fls_ghi", "fls-staging-pg-fls_doc"]
    ), bi_mat      # ⛔ đọc jwt-secret ở bước 02 (không cần)
    pl = mt["gia"]["proxy_log"].read_text()
    assert f"--port {H.cong_pg()}" in pl and "--address 127.0.0.1" in pl
    assert "du-an-gia:asia-southeast1:fls-staging" in pl
    assert "0.0.0.0" not in pl, "proxy ⛔ mở ra ngoài"
    pid = int(mt["gia"]["proxy_pid"].read_text())
    assert not os.path.exists(f"/proc/{pid}") or "sleep" not in open(f"/proc/{pid}/cmdline").read(), \
        "proxy còn sống sau khi script thoát (trap EXIT)"


def test_chay_LAI_duoc_khong_doi_gi_va_van_DAT(da_lam, mt):
    r = _chay(mt)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "khong co gi de ap" in r.stdout, "lần 2 ⛔ áp lại di trú"


def test_kiem_la_CHI_DOC_khong_doi_quyen_hay_vai(da_lam, mt):
    snap_sql = ("SELECT md5(string_agg(relname || coalesce(relacl::text,''), ',' ORDER BY relname)) "
                "FROM pg_class WHERE relnamespace = 'public'::regnamespace AND relkind IN ('r','p','v','S')")
    vai_sql = ("SELECT md5(string_agg(rolname || coalesce(rolconfig::text,'') || rolcreaterole::text, ',' "
               "ORDER BY rolname)) FROM pg_roles WHERE rolname LIKE 'fls\\_%'")
    truoc = (H.chay_quan_tri(snap_sql, mt["kho"]), H.chay_quan_tri(vai_sql))
    r = _chay(mt, "--kiem")
    assert r.returncode == 0, r.stdout
    assert "--kiem (chỉ đọc)" in r.stdout
    assert "② quản trị" not in r.stdout and "④ phân quyền" not in r.stdout
    sau = (H.chay_quan_tri(snap_sql, mt["kho"]), H.chay_quan_tri(vai_sql))
    assert truoc == sau and all(truoc), "`--kiem` đã ĐỔI quyền/vai"


def test_quyen_THAT_do_doc_lap_bang_psycopg_khong_qua_script(da_lam, mt):
    """Chống tautology: BÁO CÁO tự đo bằng psql; bài này dùng psycopg ⇒ hai dụng cụ khác nhau."""
    kho = mt["kho"]
    with psycopg.connect(_dsn("fls_ghi", kho), autocommit=True) as c:
        for sql in ("UPDATE fls_itl SET itl_id = itl_id WHERE false", "DELETE FROM fls_itl WHERE false"):
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                c.execute(sql)
        assert c.execute("SELECT count(*) FROM fls_itl").fetchone()[0] == 0
        c.execute("UPDATE fls_run SET row_count = row_count WHERE false")          # DML bảng khác: được
        c.execute("DELETE FROM fls_run WHERE false")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):                  # sổ di trú: chỉ đọc
            c.execute("DELETE FROM fls_migration WHERE false")
        assert c.execute("SELECT has_table_privilege('fls_ghi','fls_itl','INSERT')").fetchone()[0] is True
        assert c.execute("SELECT nextval('seq_itl_id') > 0").fetchone()[0] is True  # cấp itl_id được
    with psycopg.connect(_dsn("fls_doc", kho), autocommit=True) as c:
        assert c.execute("SHOW default_transaction_read_only").fetchone()[0] == "on"
        assert c.execute("SELECT count(*) FROM fls_itl").fetchone()[0] == 0
        with pytest.raises(psycopg.errors.ReadOnlySqlTransaction):
            c.execute("CREATE TABLE fls_probe_doc_ghi (i int)")
        with pytest.raises(psycopg.errors.InsufficientPrivilege):
            c.execute("SELECT nextval('seq_itl_id')")                              # seq: chỉ SELECT
        with pytest.raises(psycopg.errors.ReadOnlySqlTransaction):                  # lớp 1: mặc định chỉ-đọc
            c.execute("INSERT INTO fls_run (run_id) VALUES ('x')")
        # ⚠ lớp 1 chỉ là MẶC ĐỊNH (phiên tự `SET … = off` được) — tường THẬT là GRANT (lớp 2):
        c.execute("SET default_transaction_read_only = off")
        for sql in ("INSERT INTO fls_run (run_id) VALUES ('x')", "UPDATE fls_run SET row_count = 1 WHERE false",
                    "DELETE FROM fls_run WHERE false", "TRUNCATE fls_run"):
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                c.execute(sql)
    # PUBLIC ⛔ nối được kho
    with pytest.raises(psycopg.OperationalError):
        psycopg.connect(f"postgresql://stg_ngoai:x@127.0.0.1:{H.cong_pg()}/{kho}", connect_timeout=5)


def test_cua_API_chap_nhan_ket_noi_fls_doc_vi_la_chi_doc(da_lam, mt):
    """Móc với cổng thật của cửa: `kiem_truoc_khi_mo` ⇒ `la_chi_doc` đọc `SHOW default_transaction_read_only`.
    Cửa ⛔ gọi `noi_chi_doc` ở đây — vai `fls_doc` tự thân đã chỉ-đọc nhờ `ALTER ROLE` của bước 02."""
    from fls.api.cua import kiem_truoc_khi_mo, kiem_duong_ghi
    with psycopg.connect(_dsn("fls_doc", mt["kho"]), autocommit=True) as c:
        kiem_truoc_khi_mo(c)                       # ⛔ nổ nếu còn ghi được
        with pytest.raises(RuntimeError):
            kiem_duong_ghi(c)                      # và nó ⛔ dùng làm đường GHI được
    with psycopg.connect(_dsn("fls_ghi", mt["kho"]), autocommit=True) as c:
        kiem_duong_ghi(c)                          # đường ghi: fls_ghi ghi được
        with pytest.raises(RuntimeError):
            kiem_truoc_khi_mo(c)                   # ⇒ cửa dùng nó làm đường ĐỌC phải qua `noi_chi_doc`


# ══ ⓑ HỎNG TỪNG MỤC ⇒ ĐÚNG MỤC ĐỎ ══════════════════════════════════════════════════════════════
# (tên bài, SQL phá, SQL trả-lại ("" = chạy lại script là đủ), tập mục ĐỎ mong — nguyên văn nhãn)
PHA = [
    ("ghi_duoc_UPDATE_so", "GRANT UPDATE ON fls_itl TO fls_ghi", "",
     {"fls_ghi · quyền trên fls_itl", "fls_ghi · UPDATE fls_itl bị chặn"}),
    ("ghi_duoc_DELETE_so", "GRANT DELETE ON fls_itl TO fls_ghi", "",
     {"fls_ghi · quyền trên fls_itl", "fls_ghi · DELETE fls_itl bị chặn"}),
    ("ghi_het_INSERT_so", "REVOKE INSERT ON fls_itl FROM fls_ghi", "",
     {"fls_ghi · quyền trên fls_itl"}),
    ("ghi_mat_DML_mot_bang", "REVOKE DELETE ON fls_run FROM fls_ghi", "",
     {"fls_ghi · bảng thiếu DML (trừ fls_itl, fls_migration)"}),
    ("ghi_sua_duoc_so_di_tru", "GRANT UPDATE ON fls_migration TO fls_ghi", "",
     {"fls_ghi · quyền trên fls_migration"}),
    ("doc_co_quyen_ghi", "GRANT INSERT ON fls_run TO fls_doc", "",
     {"fls_doc · bảng có quyền GHI"}),
    ("doc_mat_SELECT", "REVOKE SELECT ON fls_run FROM fls_doc", "",
     {"fls_doc · bảng/view thiếu SELECT"}),
    ("doc_het_chi_doc_mac_dinh", "ALTER ROLE fls_doc RESET default_transaction_read_only", "",
     {"fls_doc · default_transaction_read_only (phiên mới)", "fls_doc · ALTER ROLE đã đặt",
      "fls_doc · CREATE TABLE bị PG từ chối vì chỉ-đọc"}),
    ("public_co_quyen", "GRANT SELECT ON fls_run TO PUBLIC", "",
     {"bảng/view còn quyền cho PUBLIC"}),
    ("bang_khong_thuoc_admin", "ALTER TABLE fls_run OWNER TO fls_ghi", "ALTER TABLE fls_run OWNER TO fls_admin",
     # ⭐ hai mục, ⛔ một: bảng của người lạ thì `pg_verify` (chạy bằng fls_admin) cũng ⛔ soi hết được
     {"bảng/view/seq KHÔNG thuộc fls_admin", "pg_verify (4 ký tự đầu)"}),
    ("vai_ghi_co_CREATEROLE", "ALTER ROLE fls_ghi CREATEROLE", "",
     {"fls_ghi/fls_doc: siêu quyền hay CREATEROLE/CREATEDB (đếm vai)"}),
    ("vai_doc_vao_cloudsqlsuperuser", "GRANT cloudsqlsuperuser TO fls_doc", "",
     {"fls_ghi/fls_doc là thành viên cloudsqlsuperuser (đếm)"}),
    ("kho_lech_khai_bao", "ALTER TABLE fls_run ADD COLUMN stg_cot_la int", "ALTER TABLE fls_run DROP COLUMN stg_cot_la",
     {"pg_verify (4 ký tự đầu)"}),
    ("thieu_mot_di_tru",
     # bản sao để TRẢ nằm ở schema riêng ⇒ ⛔ làm lệch phép đếm bảng của schema `public`
     "CREATE SCHEMA stg_tmp; CREATE TABLE stg_tmp.sao AS SELECT * FROM fls_migration WHERE version = "
     "(SELECT max(version) FROM fls_migration); DELETE FROM fls_migration WHERE version = "
     "(SELECT max(version) FROM fls_migration)",
     "INSERT INTO fls_migration SELECT * FROM stg_tmp.sao; DROP SCHEMA stg_tmp CASCADE",
     {"di trú đã áp = số tệp"}),
]


@pytest.mark.parametrize("ten,pha,tra,mong_do", PHA, ids=[p[0] for p in PHA])
def test_pha_mot_muc_thi_DUNG_muc_do_roi_chay_lai_thi_lanh(da_lam, mt, ten, pha, tra, mong_do):
    assert da_lam.returncode == 0, "nền chưa ĐẠT — bài ⓑ vô nghĩa"
    kho = mt["kho"]
    H.chay_quan_tri(pha, kho)
    try:
        r = _chay(mt, "--kiem")
    finally:
        if tra:
            H.chay_quan_tri(tra, kho)
        lanh = _chay(mt)                   # "làm" lại LUÔN chạy (⛔ để một bài đỏ kéo đổ các bài sau)
    assert r.returncode == 1, f"phá `{ten}` mà báo cáo VẪN exit {r.returncode}:\n{r.stdout}"
    assert "KẾT: ĐỎ" in r.stdout
    assert H.muc_do(r.stdout) == mong_do, (ten, H.muc_do(r.stdout) ^ mong_do, r.stdout)
    assert lanh.returncode == 0 and "KẾT: ĐẠT" in lanh.stdout, (ten, lanh.stdout, lanh.stderr)   # chạy-lại ⇒ lành


def test_chu_kho_sai_thi_DO_roi_lam_lai_tra_chu(da_lam, mt):
    H.chay_quan_tri(f"ALTER DATABASE {mt['kho']} OWNER TO {mt['qt']}")
    try:
        r = _chay(mt, "--kiem")
    finally:
        lanh = _chay(mt)
    # ⭐ đổi chủ kho ⇒ ACL kho bị viết lại theo chủ mới ⇒ `fls_admin` MẤT quyền nối ⇒ KHÔNG đo được gì
    #   ⇒ cả báo cáo ĐỎ (Đ5: "không đo được" là ĐỎ), ⛔ chỉ mục "chủ kho".
    assert r.returncode == 1 and "chủ kho" in H.muc_do(r.stdout) and len(H.muc_do(r.stdout)) >= 10, r.stdout
    assert H.dong_bao_cao(r.stdout) and not [k for k, v in H.dong_bao_cao(r.stdout).items() if v == "ĐẠT"
                                              and k.startswith(("fls_ghi · quyền", "fls_doc · bảng"))]
    assert lanh.returncode == 0, lanh.stdout + lanh.stderr


# ══ ⓒ ĐO KHÔNG ĐƯỢC ⇒ ĐỎ ═══════════════════════════════════════════════════════════════════════

def test_kho_RONG_la_DO_khong_phai_xanh_tren_tap_rong__D3(mt):
    """Kho scratch thứ hai, CHƯA di trú: mẫu số = 0 ⇒ phải ĐỎ (mọi phép "= 0" ở đó đều ĐẠT trên tập rỗng)."""
    kho = mt["kho"] + "_rong"
    H.chay_quan_tri(f"CREATE DATABASE {kho} OWNER {mt['qt']}")
    try:
        r = H.chay_script(S02, mt["gia"], kho, mt["qt"], "--kiem")
        assert r.returncode == 1, r.stdout
        do = H.muc_do(r.stdout)
        assert "mẫu số ≠ 0" in do, do
        # các phép đếm "= 0" ĐẠT vì tập rỗng — bằng chứng cho luật: chúng ĐẠT mà mẫu số 0
        dat = {k for k, v in H.dong_bao_cao(r.stdout).items() if v == "ĐẠT"}
        assert "bảng/view còn quyền cho PUBLIC" in dat or "fls_doc · bảng có quyền GHI" in dat, \
            "bài này chứng minh phép `= 0` xanh trên tập rỗng — nếu không còn xanh thì cập nhật bài"
    finally:
        H.chay_quan_tri(f"DROP DATABASE IF EXISTS {kho} WITH (FORCE)")


def _gia_hong(gia, ten: str, noi_dung: str):
    p = gia["dir"] / "hong" / ten
    p.parent.mkdir(exist_ok=True)
    p.write_text(noi_dung, encoding="utf-8")
    p.chmod(p.stat().st_mode | stat.S_IXUSR)
    return p.parent


def test_psql_va_python_GIA_hong_thi_KHONG_muc_nao_ĐẠT__D5(da_lam, mt):
    """Mọi dụng cụ đo hỏng ⇒ exit 1 và 0 mục ĐẠT: "không đo được" là ĐỎ, ⛔ "không thấy lệch"."""
    gia = mt["gia"]
    thu_muc = _gia_hong(gia, "psql", "#!/usr/bin/env bash\nexit 2\n")
    py = _gia_hong(gia, "python", "#!/usr/bin/env bash\nexit 1\n") / "python"
    env = {"PATH": f"{thu_muc}{os.pathsep}{gia['dir']}{os.pathsep}{os.environ['PATH']}", "FLS_STG_PYTHON": str(py)}
    r = _chay(mt, "--kiem", env_them=env)
    # `psql` giả đứng đầu PATH ⇒ nhưng `command -v psql` OK; mọi phép đo ra rỗng
    assert r.returncode == 1, r.stdout + r.stderr
    dat = {k for k, v in H.dong_bao_cao(r.stdout).items() if v == "ĐẠT"}
    assert dat == set(), f"đo hỏng mà vẫn ĐẠT: {sorted(dat)}"
    assert len(H.muc_do(r.stdout)) >= 20


# ══ tham số xấu · thiếu đồ · thiếu bí mật ═════════════════════════════════════════════════════

def test_tham_so_xau_exit_2_va_khong_goi_proxy(mt):
    gia = mt["gia"]
    for args, loi in ((("--kho", "x;DROP DATABASE y"), "--kho chỉ gồm"), (("--cong-proxy", "abc"), "--cong-proxy phải là số"),
                      (("--la",), "tham số lạ")):
        env = dict(os.environ, PATH=f"{gia['dir']}{os.pathsep}{os.environ['PATH']}")
        r = subprocess.run(["bash", str(H.STG / S02), "--project", "p", *args], capture_output=True, text=True, env=env)
        assert r.returncode == 2 and loi in r.stderr, (args, r.returncode, r.stderr)
    r = subprocess.run(["bash", str(H.STG / S02)], capture_output=True, text=True)
    assert r.returncode == 2 and "thiếu --project" in r.stderr


def test_thieu_proxy_exit_2_chi_cach_tai(mt, tmp_path):
    env = dict(os.environ, PATH=f"{mt['gia']['dir']}{os.pathsep}{os.environ['PATH']}")
    r = subprocess.run(["bash", str(H.STG / S02), "--project", "p", "--proxy", str(tmp_path / "khong-co")],
                       capture_output=True, text=True, env=env)
    assert r.returncode == 2 and "cloud-sql-proxy" in r.stderr and "sql-proxy#install" in r.stderr, r.stderr


def test_thieu_bi_mat_thi_dung_TRUOC_khi_bat_proxy(mt, tmp_path):
    gia = H.dung_gia(tmp_path / "g", thieu_bi_mat="fls-staging-pg-fls_ghi")
    r = H.chay_script(S02, gia, mt["kho"], mt["qt"], "--kiem")
    assert r.returncode != 0 and "không đọc được bí mật fls-staging-pg-fls_ghi" in r.stderr, r.stderr
    assert not gia["proxy_log"].exists(), "proxy đã được bật dù thiếu bí mật"


# ══ tĩnh: những thứ ⛔ được có trong script ═════════════════════════════════════════════════════

def test_tinh_script_va_sql_khong_co_thu_cam():
    van = (H.STG / S02).read_text(encoding="utf-8")
    sql = "\n".join(l for f in ("02a_quan_tri.sql", "02b_phan_quyen.sql")
                    for l in (H.STG / "sql" / f).read_text(encoding="utf-8").splitlines()
                    if not l.lstrip().startswith("--"))          # bỏ chú thích: lời khuyên ⛔ phải bị cổng bắt
    code = "\n".join(l for l in van.splitlines() if not l.lstrip().startswith("#"))
    assert subprocess.run(["bash", "-n", str(H.STG / S02)]).returncode == 0
    assert not re.search(r"^\s*set\s+-[a-z]*x", code, re.M), "⛔ `set -x` lộ mật khẩu"
    assert not re.search(r"postgresql://[^@/\s\"']+:[^@\s\"']+@", van), "⛔ DSN mang mật khẩu"
    assert "echo \"$MK_" not in code and "echo $MK_" not in code
    assert "ALTER DEFAULT PRIVILEGES" not in sql, "bảng mới ⛔ được tự cấp quyền (xem 02b)"
    assert "GRANT ALL" not in sql.upper().replace("REVOKE ALL", "")
    assert "0.0.0.0" not in code and "--private-ip" not in code


def test_kiem_KHONG_de_lai_vat_ke_ca_khi_fls_doc_con_CREATE_va_het_chi_doc__STG_R1_08(da_lam, mt):
    """`STG-R1-08`: `--kiem` (chỉ ĐỌC) từng chạy `CREATE TABLE fls_probe_doc_ghi` bằng `fls_doc`; nếu vai ấy còn `CREATE` trên
    `public` và hết chỉ-đọc thì bảng THẬT được tạo (chủ = fls_doc) ⇒ lần "làm" kế chết ở `02b`. Bài trước đo **quyền/vai** ⛔ đổi,
    ⛔ đo "⛔ để lại VẬT" (Đ3: "không đổi quyền" ≠ "không đổi gì"). Ở đây dựng ĐÚNG hoàn cảnh ấy."""
    assert da_lam.returncode == 0
    kho = mt["kho"]
    H.chay_quan_tri("GRANT CREATE ON SCHEMA public TO fls_doc; ALTER ROLE fls_doc RESET default_transaction_read_only", kho)
    try:
        r = _chay(mt, "--kiem")
        vat = H.chay_quan_tri("SELECT count(*) FROM pg_class WHERE relname = 'fls_probe_doc_ghi'", kho)
    finally:
        H.chay_quan_tri("REVOKE CREATE ON SCHEMA public FROM fls_doc", kho)
        H.chay_quan_tri("DROP TABLE IF EXISTS public.fls_probe_doc_ghi", kho)
        lanh = _chay(mt)
    assert r.returncode == 1 and "fls_doc · CREATE TABLE bị PG từ chối vì chỉ-đọc" in H.muc_do(r.stdout), r.stdout   # vẫn ĐỎ — nhưng
    assert str(vat) == "0", f"`--kiem` để lại {vat} bảng `fls_probe_doc_ghi`"                                          # ⛔ có vật
    assert lanh.returncode == 0 and "KẾT: ĐẠT" in lanh.stdout, lanh.stdout
