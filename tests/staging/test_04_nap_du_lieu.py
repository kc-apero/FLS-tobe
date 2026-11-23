"""Bài thử bước 04 — `WO-325` AC-3: `nap_cau_hinh_ix.py` · `04_nap_du_lieu.sh` · `app/chay_chuoi.sh`.

  ⓐ trình nạp config (chạy THẬT trên kho scratch): từ chối khi thiếu cổng ghi · nạp đủ 9 bảng có `mong` hai chiều ·
     chạy lại ⛔ nạp chồng · ⛔ chạm `fls_itl` · kho trắng ⇒ ĐỎ (Đ3).
  ⓑ `04_nap_du_lieu.sh` (gcloud + proxy GIẢ, psql + trình nạp THẬT): đúng ⇒ ĐẠT; đòi `FLS_CHO_GHI_THAT=1`; chỉ đọc bí mật `fls_ghi`;
     cột "Email Address" lọt vào kho ⇒ ĐỎ; `--nguon-that` luôn từ chối.
  ⓒ `chay_chuoi.sh`: kho trắng ⇒ ĐỎ nêu tên gói; sau khi nạp config ⇒ N/N gói ĐẠT (N = `len(tools.do_hd2.GOI_BIET)`, ⛔ số cứng — `STG-R1-02`: H14 thêm `WP-C5c` ⇒ 11 làm hai bài đỏ) (đây là bằng chứng bước 04 ĐỦ để chạy chuỗi).
"""
from __future__ import annotations

import io
import os
import re
import subprocess
import sys
from contextlib import redirect_stdout

import psycopg
import pytest

from tests.staging import ho_tro as H
from tools.do_hd2 import GOI_BIET

DRV = H.STG / "nap_cau_hinh_ix.py"
S04 = "04_nap_du_lieu.sh"


def _kho_rong(ten: str) -> str:
    """Kho scratch RỖNG đã di trú (chủ = `fls` của phiên): trả DSN. ⛔ kho `fls` thật của phiên."""
    from fls.db.kho import dung_lai_kho_test, doi_ten_kho, dsn_that
    dsn = doi_ten_kho(dsn_that(), ten)
    dung_lai_kho_test(dsn)
    return dsn


@pytest.fixture(scope="module")
def dsn_cfg():
    ten = f"fls_stg_cfg_{os.getpid()}"
    dsn = _kho_rong(ten)
    yield dsn
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {ten} WITH (FORCE)")


def _chay_drv(dsn, *args, ghi=True, env_them=None):
    env = dict(os.environ, PG_DSN=dsn, PYTHONUTF8="1")
    env.pop("FLS_CHO_GHI_THAT", None)
    if ghi:
        env["FLS_CHO_GHI_THAT"] = "1"
    if env_them:
        env.update(env_them)
    return subprocess.run([sys.executable, str(DRV), *args], capture_output=True, text=True, env=env, timeout=300)


def _dem(dsn, sql):
    with psycopg.connect(dsn, autocommit=True) as c:
        return c.execute(sql).fetchone()[0]


# ══ ⓐ trình nạp ═════════════════════════════════════════════════════════════════════════════════

def test_kho_TRANG_kiem_ra_DO_vi_mau_so_0__D3(dsn_cfg):
    r = _chay_drv(dsn_cfg, "--kiem", ghi=False)
    assert r.returncode == 1 and "KẾT: ĐỎ" in r.stdout, r.stdout
    assert not re.search(r"\[ĐẠT\] MẪU SỐ", r.stdout), "tổng phiên bản = 0 mà MẪU SỐ vẫn ĐẠT"
    assert "tổng phiên bản config trong kho = 0" in r.stdout
    assert r.stdout.count("[ĐẠT]") == 0, r.stdout            # kho trắng ⇒ 0 mục ĐẠT (kể cả phiên bản "mong 1")


@pytest.mark.parametrize("args,ghi,loi", [
    (("--nguoi-nap", "khanh.thu"), False, "FLS_CHO_GHI_THAT"),
    ((), True, "--nguoi-nap"),
    (("--nguoi-nap", "a@b.com"), True, "--nguoi-nap"),
    (("--nguoi-nap", "   "), True, "--nguoi-nap"),
])
def test_tu_choi_khi_thieu_cong_ghi_hoac_nguoi_nap_xau__khong_ghi_gi(dsn_cfg, args, ghi, loi):
    r = _chay_drv(dsn_cfg, *args, ghi=ghi)
    assert r.returncode == 2 and loi in r.stderr, (r.returncode, r.stderr)
    assert _dem(dsn_cfg, "SELECT count(*) FROM fls_cau_hinh_ban") == 0, "đã ghi dù bị từ chối"


def test_thieu_PG_DSN_exit_2():
    env = {k: v for k, v in os.environ.items() if k != "PG_DSN"}
    r = subprocess.run([sys.executable, str(DRV), "--kiem"], capture_output=True, text=True, env=env)
    assert r.returncode == 2 and "PG_DSN" in r.stderr


def test_nap_du_9_bang_DAT_actor_dung_khong_cham_so_va_chay_lai_khong_nap_chong(dsn_cfg):
    so_truoc = _dem(dsn_cfg, "SELECT count(*) FROM fls_itl")
    run_truoc = _dem(dsn_cfg, "SELECT count(*) FROM fls_run")
    r = _chay_drv(dsn_cfg, "--nguoi-nap", "khanh.thu")
    assert r.returncode == 0 and "KẾT: ĐẠT" in r.stdout, r.stdout + r.stderr
    assert "[ĐỎ]" not in r.stdout
    assert r.stdout.count("[ĐẠT]") == 9 * 2 + 1, r.stdout          # 9 bảng × (phiên bản + dòng) + MẪU SỐ
    ban = psycopg.connect(dsn_cfg, autocommit=True).execute(
        "SELECT bang, phien_ban, actor FROM fls_cau_hinh_ban ORDER BY bang, phien_ban").fetchall()
    assert len(ban) == 10 and len({b for b, _, _ in ban}) == 9, ban
    actor = {(b, v): a for b, v, a in ban}
    assert actor[("IX.ALR", 1)] == "khanh.thu" and actor[("IX.ALR", 2)] == "KhanhCQ", "bản KÝ mang tên NGƯỜI KÝ trong tệp"
    assert all(a == "khanh.thu" for (b, v), a in actor.items() if (b, v) != ("IX.ALR", 2))
    assert not [a for a in actor.values() if "@" in a]
    # ⛔ chạm sổ / lô nạp
    assert _dem(dsn_cfg, "SELECT count(*) FROM fls_itl") == so_truoc == 0
    assert _dem(dsn_cfg, "SELECT count(*) FROM fls_run") == run_truoc
    # chạy lại: ⛔ nạp chồng
    r2 = _chay_drv(dsn_cfg, "--nguoi-nap", "nguoi.khac")
    assert r2.returncode == 0 and r2.stdout.count("có rồi v") == 9, r2.stdout          # cả 9 bảng ⇒ "có rồi", ⛔ "nạp"
    assert _dem(dsn_cfg, "SELECT count(*) FROM fls_cau_hinh_ban") == 10, "chạy lại đẻ thêm phiên bản"
    # đúng các bảng + số dòng khớp `mong` đã ghim
    with psycopg.connect(dsn_cfg, autocommit=True) as c:
        sl = dict(c.execute("SELECT b.bang, count(*) FROM fls_cau_hinh_dong d JOIN fls_cau_hinh_ban b USING (ban_id) "
                            "WHERE (b.bang, b.phien_ban) IN (SELECT bang, max(phien_ban) FROM fls_cau_hinh_ban GROUP BY bang) "
                            "GROUP BY 1").fetchall())
    sys.path.insert(0, str(H.GOC))
    from tools.staging import nap_cau_hinh_ix as N
    assert sl == N.MONG_DONG, (sl, N.MONG_DONG)


def test_mong_hai_chieu_doi_mot_con_so_mong_thi_DO_dung_bang__D5(dsn_cfg):
    """Cổng chỉ xanh khi `mong` khớp: sửa `mong` lên/xuống 1 ⇒ ĐỎ ĐÚNG bảng ấy, ⛔ bảng khác."""
    sys.path.insert(0, str(H.GOC))
    from tools.staging import nap_cau_hinh_ix as N
    if _dem(dsn_cfg, "SELECT count(*) FROM fls_cau_hinh_ban") != 10:
        assert _chay_drv(dsn_cfg, "--nguoi-nap", "khanh.thu").returncode == 0
    with psycopg.connect(dsn_cfg, autocommit=True) as c:
        for d in (+1, -1):
            goc = N.MONG_DONG["IX.FX"]
            N.MONG_DONG["IX.FX"] = goc + d
            try:
                buf = io.StringIO()
                with redirect_stdout(buf):
                    rc = N.bao_cao(N.do_kho(c), {}, "thu")
            finally:
                N.MONG_DONG["IX.FX"] = goc
            do = [l for l in buf.getvalue().splitlines() if "[ĐỎ]" in l]
            assert rc == 1 and len(do) == 1 and do[0].lstrip().startswith("[ĐẠT] IX.FX"), (d, do)
            assert "dòng bản mới nhất = 38" in do[0] and f"(mong {goc + d})" in do[0]
        N.MONG_PHIEN_BAN["IX.ALR"] = 3
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = N.bao_cao(N.do_kho(c), {}, "thu")
        finally:
            N.MONG_PHIEN_BAN["IX.ALR"] = 2
        assert rc == 1 and "[ĐỎ] IX.ALR" in buf.getvalue()


def test_nap_thieu_mot_bang_thi_bang_do_con_lai_xanh__khong_xanh_suong(tmp_path):
    ten = f"fls_stg_cfg2_{os.getpid()}"
    dsn = _kho_rong(ten)
    try:
        sys.path.insert(0, str(H.GOC))
        from tools.staging import nap_cau_hinh_ix as N
        thu_tu = N.BANG_THU_TU
        N.BANG_THU_TU = tuple(b for b in thu_tu if b != "IX.DRV")
        try:
            with psycopg.connect(dsn, autocommit=True) as c:
                N._nap_het(c, "khanh.thu")
        finally:
            N.BANG_THU_TU = thu_tu
        r = _chay_drv(dsn, "--kiem", ghi=False)
        assert r.returncode == 1, r.stdout
        do = [l.strip() for l in r.stdout.splitlines() if "[ĐỎ]" in l]
        assert len(do) == 1 and "IX.DRV" in do[0], do          # hai chiều của DRV nằm trên MỘT dòng
        assert "phiên bản = 0" in do[0] and "dòng bản mới nhất = 0" in do[0]
        assert "MẪU SỐ" in r.stdout and re.search(r"\[ĐẠT\] MẪU SỐ", r.stdout)       # 9 phiên bản ≥ 9
    finally:
        H.chay_quan_tri(f"DROP DATABASE IF EXISTS {ten} WITH (FORCE)")


def test_trinh_nap_chi_goi_ham_san_co_khong_chua_ban_chep_luat_nap():
    van = DRV.read_text(encoding="utf-8")
    code = "\n".join(l for l in van.splitlines() if not l.lstrip().startswith("#"))
    assert "cau_hinh_repo" in code
    for ham in ("nap_ix_fx", "nap_ix_hd", "nap_ix_pl", "nap_mapping_master", "nap_ix_per", "nap_ix_ven", "nap_ix_org",
                "nap_ix_alr", "ky_bat_ix_alr", "nap_ix_drv"):
        assert f"chc.{ham}(" in code, ham
    code_khong_doc = re.sub(r'"""[\s\S]*?"""', "", code)                   # bỏ docstring (nó NÊU các tên cấm)
    assert not re.search(r"INSERT\s+INTO|UPDATE\s|DELETE\s+FROM", code_khong_doc, re.I), "trình nạp ⛔ tự viết SQL ghi"
    assert "fls_itl" not in code_khong_doc, "trình nạp ⛔ chạm sổ"
    assert not re.search(r"sao_luu|hien_vat|Input_Raw|Email Address", code_khong_doc), "⛔ đường tới dữ liệu thật/riêng tư"
    anh = [m for m in re.findall(r'ANH / "([^"]+)"', code)]
    assert anh and all((H.GOC / "tests" / "fixture" / "cau_hinh" / a).is_file() for a in anh), anh


# ══ ⓑ 04_nap_du_lieu.sh ═════════════════════════════════════════════════════════════════════════

def _chay04(mt, *args, ghi=True, env_them=None):
    env = {"FLS_CHO_GHI_THAT": "1"} if ghi else {}
    if env_them:
        env.update(env_them)
    r = H.chay_script(S04, mt["gia"], mt["kho"], mt["qt"], *args, env_them=env)
    return r


@pytest.fixture(scope="module")
def kho_04(kho_san):
    """Kho đã qua 02 — bước 04 chạy trên nó (vai `fls_ghi` THẬT). Kèm một BẢN SAO "trắng" (di trú + phân quyền, ⛔ config)
    chụp TRƯỚC khi bước 04 chạy — để bài chuỗi đo trên kho thiếu config mà ⛔ phải xoá gì (config là chỉ-thêm)."""
    trang = kho_san["kho"] + "_trang"
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {trang} WITH (FORCE)")
    H.chay_quan_tri(f"CREATE DATABASE {trang} TEMPLATE {kho_san['kho']}")
    yield dict(kho_san, trang=trang)
    H.chay_quan_tri(f"DROP DATABASE IF EXISTS {trang} WITH (FORCE)")


def test_04_dung_ra_DAT_chi_doc_bi_mat_fls_ghi_va_khong_lo_mat_khau(kho_04):
    mt = kho_04
    mt["gia"]["gcloud_log"].write_text("")
    r = _chay04(mt, "--nguoi-nap", "khanh.thu")
    assert r.returncode == 0, r.stdout + r.stderr
    assert "KẾT: ĐẠT" in r.stdout and not H.muc_do(r.stdout), r.stdout
    gop = r.stdout + r.stderr + mt["gia"]["proxy_log"].read_text()
    assert [t for t, mk in H.MK.items() if mk in gop] == [], "mật khẩu GIẢ rò ra"
    nk = mt["gia"]["gcloud_log"].read_text().splitlines()
    bi_mat = sorted(re.search(r"--secret=(\S+)", d).group(1) for d in nk if "secrets versions access" in d)
    assert bi_mat == ["fls-staging-pg-fls_ghi"], bi_mat        # ⛔ postgres, ⛔ admin, ⛔ jwt
    assert not [d for d in nk if re.search(r"\b(create|delete|add-iam|set-password|update)\b", d)]
    # kết quả THẬT trong kho scratch
    with psycopg.connect(f"postgresql://fls_ghi:{H.MK['fls-staging-pg-fls_ghi']}@127.0.0.1:{H.cong_pg()}/{mt['kho']}",
                         autocommit=True) as c:
        assert c.execute("SELECT count(*) FROM fls_cau_hinh_ban").fetchone()[0] == 10
        assert c.execute("SELECT count(*) FROM fls_itl").fetchone()[0] == 0
    # 9 bảng (mỗi bảng 1 dòng, hai chiều) + MẪU SỐ config + 6 mục riêng tư/phạm vi có `mong` = 16 dòng `[ĐẠT]`
    bc = H.dong_bao_cao(r.stdout)
    assert len(bc) == 16 and "cột tên có 'email' (đếm, ⛔ vào kho)" in bc and "fls_itl số dòng (chỉ-config ⇒ 0; ⛔ sổ ở bước này)" in bc, bc


def test_04_chay_lai_van_DAT_va_khong_nap_chong(kho_04):
    mt = kho_04
    r = _chay04(mt, "--nguoi-nap", "khanh.thu")
    assert r.returncode == 0 and "có rồi" in r.stdout, r.stdout
    with psycopg.connect(f"postgresql://fls_ghi:{H.MK['fls-staging-pg-fls_ghi']}@127.0.0.1:{H.cong_pg()}/{mt['kho']}",
                         autocommit=True) as c:
        assert c.execute("SELECT count(*) FROM fls_cau_hinh_ban").fetchone()[0] == 10


def test_04_kiem_chi_doc_khong_can_cong_ghi(kho_04):
    mt = kho_04
    r = _chay04(mt, "--kiem", ghi=False)
    assert r.returncode == 0 and "--kiem (chỉ đọc)" in r.stdout and "KẾT: ĐẠT" in r.stdout, r.stdout


def test_04_cot_Email_Address_lot_vao_kho_thi_DO(kho_04):
    mt = kho_04
    H.chay_quan_tri('ALTER TABLE fls_run ADD COLUMN "Email Address" text', mt["kho"])
    try:
        r = _chay04(mt, "--kiem", ghi=False)
    finally:
        H.chay_quan_tri('ALTER TABLE fls_run DROP COLUMN "Email Address"', mt["kho"])
    assert r.returncode == 1 and H.muc_do(r.stdout) == {"cột tên có 'email' (đếm, ⛔ vào kho)"}, r.stdout


def test_04_actor_email_trong_config_thi_DO(kho_04):
    """Bản config mang `actor` là email ⇒ ĐỎ. (Kho chỉ-thêm ⇒ dùng một kho scratch riêng, ⛔ bẩn kho dùng chung.)"""
    mt = kho_04
    ten = f"fls_stg_mail_{os.getpid()}"
    H.chay_quan_tri(f"CREATE DATABASE {ten} TEMPLATE {mt['kho']}")        # nhân bản kho đã di trú+phân quyền+config
    try:
        H.chay_quan_tri("INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor) "
                        "VALUES ('IX.PER', 99, 'x', 'y', 'ai.do@x.com')", ten)
        r = H.chay_script(S04, mt["gia"], ten, mt["qt"], "--kiem")
        assert r.returncode == 1, r.stdout
        assert "bản config có actor chứa '@' (đếm)" in H.muc_do(r.stdout), r.stdout
    finally:
        H.chay_quan_tri(f"DROP DATABASE IF EXISTS {ten} WITH (FORCE)")


def test_04_tu_choi_thieu_cong_ghi_nguoi_nap_xau_va_nguon_that_KHONG_goi_gcloud(kho_04):
    mt = kho_04
    mt["gia"]["gcloud_log"].write_text("")
    cases = [(("--nguoi-nap", "khanh.thu"), False, "FLS_CHO_GHI_THAT"),
             ((), True, "--nguoi-nap"), (("--nguoi-nap", "a@b.com"), True, "--nguoi-nap"),
             (("--nguoi-nap", "x;rm"), True, "--nguoi-nap"), (("--nguon-that",), True, "CÂU CHỦ".lower())]
    for args, ghi, loi in cases:
        r = _chay04(mt, *args, ghi=ghi)
        assert r.returncode == 2, (args, r.returncode, r.stderr)
        assert loi.lower() in r.stderr.lower(), (args, r.stderr)
    assert mt["gia"]["gcloud_log"].read_text() == "", "đã gọi gcloud trước khi kiểm tham số"
    r = _chay04(mt, "--nguon-that", ghi=True, env_them={"FLS_STG_DU_LIEU": "that"})
    assert r.returncode == 2, "biến môi trường ⛔ mở khoá `--nguon-that` (câu chủ chưa trả lời)"
    assert "nap_that.py" in r.stderr and "⛔" in r.stderr


# ══ ⓒ chay_chuoi.sh ═════════════════════════════════════════════════════════════════════════════

def _chay_chuoi(mt, *args, kho=None, thoi_gian=600):
    sv = None
    from tests.staging.test_03_dung_app import _may_chu, JWT_GIA   # máy chủ metadata + Secret Manager GIẢ
    sv = _may_chu({"fls-staging-jwt-secret": JWT_GIA, "fls-staging-pg-fls_doc": H.MK["fls-staging-pg-fls_doc"],
                   "fls-staging-pg-fls_ghi": H.MK["fls-staging-pg-fls_ghi"]})
    env = dict(os.environ, FLS_STG_PROJECT="du-an-gia", FLS_STG_CONG_PROXY=str(H.cong_pg()), FLS_STG_KHO=kho or mt["kho"],
               FLS_STG_PYTHON=sys.executable, PYTHONUTF8="1",
               FLS_STG_URL_METADATA=f"http://127.0.0.1:{sv.server_port}", FLS_STG_URL_SM=f"http://127.0.0.1:{sv.server_port}")
    for k in ("PG_DSN", "PG_DSN_TEST", "PGPASSWORD"):
        env.pop(k, None)
    try:
        return subprocess.run(["bash", str(H.STG / "app" / "chay_chuoi.sh"), *args], capture_output=True, text=True,
                              env=env, timeout=thoi_gian)
    finally:
        sv.shutdown()


def test_chuoi_tren_kho_TRANG_DO_nen_ten_goi_thieu_config(kho_04):
    mt = kho_04
    assert _dem(f"postgresql://fls_ghi:{H.MK['fls-staging-pg-fls_ghi']}@127.0.0.1:{H.cong_pg()}/{mt['trang']}",
                "SELECT count(*) FROM fls_cau_hinh_ban") == 0, "bản sao 'trắng' đã có config — bài vô nghĩa"
    r = _chay_chuoi(mt, kho=mt["trang"])
    assert r.returncode == 1 and "KẾT: ĐỎ" in r.stdout, r.stdout + r.stderr
    assert "ChuaKhai" in r.stdout and "WP-C3c" in r.stdout, r.stdout
    assert re.search(r"WP-C2\s+0\s", r.stdout), "WP-C2 không cần kho ⇒ vẫn ĐẠT"
    dong = [l for l in r.stdout.splitlines() if re.match(r"WP-C\d", l)]
    assert GOI_BIET and len(dong) == len(GOI_BIET) and [l.split()[0] for l in dong] == list(GOI_BIET), (dong, GOI_BIET)   # `STG-R1-02`: đếm từ NGUỒN
    assert sum(l.split()[1] != "0" for l in dong) >= 7, dong        # đo 23/11: 7+ gói cần kho


def test_chuoi_sau_khi_nap_config_ra_DAT_moi_goi_cua_GOI_BIET(kho_04):
    mt = kho_04
    r = _chay_chuoi(mt)
    assert r.returncode == 0, r.stdout + r.stderr
    dong = [l for l in r.stdout.splitlines() if re.match(r"WP-C\d", l)]
    assert GOI_BIET and len(dong) == len(GOI_BIET) and all(l.split()[1] == "0" for l in dong), dong
    assert "KẾT: ĐẠT" in r.stdout and f"{len(GOI_BIET)} gói · ĐỎ 0" in r.stdout
    assert "đã ghi" not in r.stdout, "⛔ --ghi ⇒ không ghi tệp"


def test_chuoi_tham_so_la_exit_2(kho_04):
    r = _chay_chuoi(kho_04, "--la")
    assert r.returncode == 2


# ══ `STG-R1-07` — chết GIỮA hai việc của IX.ALR (nền v1 → KÝ v2) ⇒ chạy lại PHẢI tự lành (kho chỉ-THÊM, ⛔ xoá được) ══
def test_chet_giua_IX_ALR_chay_lai_tu_lanh_DAT_va_khong_nap_chong(tmp_path):
    ten = f"fls_stg_cfg_ngat_{os.getpid()}"
    dsn = _kho_rong(ten)
    try:
        boom = tmp_path / "ngat.py"
        boom.write_text(
            "import sys\n"
            f"sys.path.insert(0, {str(H.STG.parents[1])!r})\n"
            "from fls.repo import cau_hinh_repo as chc\n"
            "def _no(*a, **k):\n"
            "    raise RuntimeError('ép nổ giữa IX.ALR: sau nap_ix_alr, trước ky_bat_ix_alr')\n"
            "chc.ky_bat_ix_alr = _no\n"
            "import tools.staging.nap_cau_hinh_ix as m\n"
            "raise SystemExit(m.main())\n", encoding="utf-8")
        env = dict(os.environ, PG_DSN=dsn, PYTHONUTF8="1", FLS_CHO_GHI_THAT="1")
        r0 = subprocess.run([sys.executable, str(boom), "--nguoi-nap", "khanh.thu"], capture_output=True, text=True, env=env, timeout=300)
        assert r0.returncode != 0, "ép nổ mà vẫn thoát 0 — bài vô nghĩa"
        # MẪU SỐ (Đ3): đúng trạng thái hỏng của R1 — IX.ALR có v1 · 17 dòng, và ⛔ có v2
        assert _dem(dsn, "SELECT max(phien_ban) FROM fls_cau_hinh_ban WHERE bang = 'IX.ALR'") == 1
        for lan in (1, 2):                                   # hai lần liên tiếp: lần 1 TỰ LÀNH, lần 2 ⛔ nạp chồng
            r = _chay_drv(dsn, "--nguoi-nap", "khanh.thu")
            assert r.returncode == 0 and "KẾT: ĐẠT" in r.stdout, (lan, r.stdout, r.stderr)
        assert _dem(dsn, "SELECT count(*) FROM fls_cau_hinh_ban WHERE bang = 'IX.ALR'") == 2
        assert _dem(dsn, "SELECT count(*) FROM fls_cau_hinh_ban") == 10
    finally:
        H.chay_quan_tri(f"DROP DATABASE IF EXISTS {ten} WITH (FORCE)")
