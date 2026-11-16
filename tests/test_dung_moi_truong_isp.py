"""Chốt + CLI của `tools/dung_moi_truong_isp.sh` — phần TẤT ĐỊNH, ⛔ cần PostgreSQL.

⛔⛔ **Vì sao có tệp này** *(ISP 3.1.2 S0 · vòng sửa sau R1 · `KQ-067`)*. Bản đầu của
script so `PG_DSN` bằng glob `case` (`postgresql://*@localhost:5433/*`) và R1 đo được
**3** đường lọt — mỗi đường "trông cục bộ mà nối đi chỗ khác":

    ⓐ  …@localhost:5433/<kho>?port=5999        psycopg nối 127.0.0.1:5999      (exit 1, ⛔ 2)
    ⓑ  postgresql://x@10.0.0.9:5432/y@localhost:5433/<kho>
                                              `*` nuốt cả `/` ⇒ khớp glob,
                                              libpq nối 10.0.0.9:5432          (exit 1, ⛔ 2)
    ⓒ  PGHOSTADDR=10.255.255.1                 libpq gộp biến PG* ⇒ nối nơi khác (exit 1, ⛔ 2)

(R1 đo với `<kho>` = kho THẬT `fls`; ở đây viết `<kho>` vì chính cổng
`tests/db/test_khong_ai_tro_lai_kho_that.py` cấm chuỗi DSN tận cùng `/fls` trong
`tests/` — lần đầu tệp này trích nguyên văn và cổng ấy ĐỎ, đúng việc của nó.)

và CLI chỉ soát `$1`: `--chi-kiem --la` ⇒ exit 0 *(`S0-R1-03`)*. Ở chế độ dựng, chuỗi sẽ
chạy `pg_migrate` (DDL) lên đích ấy. Bài ở đây canh đúng các đường đó: mọi chốt phải
ra **exit 2 TRƯỚC mọi bước** *(⛔ in dòng tiêu đề `══ dung_moi_truong_isp`)*.

⭐ **Đối chứng (Đ5 — cả hai chiều).** Một chốt từ chối MỌI THỨ cũng làm các bài exit 2
xanh. ⇒ có bài DSN HỢP LỆ phải **đi qua** chốt *(exit 1 vì môi trường giả vắng, ⛔ 2)*.

⚠ Tên kho trong bài là `fls_thu`, ⛔ `fls`: cổng `tests/db/test_khong_ai_tro_lai_kho_that.py`
cấm mọi chuỗi DSN tận cùng bằng `/fls` trong `tests/` — và chốt ⛔ phân biệt tên kho
(chỉ đòi `[a-z0-9_]+`), nên bài vẫn canh đúng đường lọt. ⛔ Bài nào ở đây nối kho:
đường exit 2 dừng trước mọi kết nối; bài đối chứng trỏ venv + binary PG **vắng**.

Chỉ chạy trên Linux: script viết cho container *(`runuser`, `/usr/lib/postgresql/16`)*.
"""
from __future__ import annotations

import os
import pathlib
import subprocess
import sys

import pytest

GOC = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = GOC / "tools" / "dung_moi_truong_isp.sh"

chi_linux = pytest.mark.skipif(
    sys.platform != "linux",
    reason="⛔ script chỉ viết cho container Linux — cổng này BỎ QUA, ⛔ đạt")

pytestmark = chi_linux

# Biến mà chốt đọc — gỡ khỏi môi trường thừa kế để mỗi bài chỉ mang đúng thứ nó khai.
_BIEN_GO = ("PG_DSN", "PG_DSN_TEST", "FLS_PG_PORT", "FLS_PGDATA", "FLS_PGBIN",
            "FLS_VENV", "FLS_CHO_GHI_THAT", "FLS_DUONG_NEN_DO",
            "PGHOST", "PGHOSTADDR", "PGPORT", "PGSERVICE", "PGSERVICEFILE")

HOP_LE = "postgresql://fls:fls@localhost:5433/fls_thu"


def _chay(doi_so: list[str], bien: dict[str, str] | None = None,
          tmp_path: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    """Gọi script trong môi trường GIẢ VẮNG — ở MỌI bài, kể cả bài mong exit 2.

    ⛔⛔ Đo 16/11 khi chạy tệp này trên bản cũ: ca `--duong-nen --chi-kiem` lọt chốt CLI,
    script vào chế độ dựng + pytest TOÀN BỘ; `timeout` chỉ giết `bash`, còn tiến trình
    pytest con chạy mồ côi trên kho test của cụm. ⇒ Chốt nào hồi quy cũng chỉ được ĐỎ
    NHANH: venv ở `/proc/…` (⛔ tạo nổi — `python3 -m venv` hỏng ngay, ⛔ pip), binary PG
    vắng (`dung_cum` dừng ở dòng đầu), ⛔ venv ⇒ ⛔ pytest, ⛔ lint, ⛔ nối kho.
    """
    env = dict(os.environ)
    for b in _BIEN_GO:
        env.pop(b, None)
    env["FLS_VENV"] = "/proc/fls_khong_co_venv"
    env["FLS_PGBIN"] = str((tmp_path or GOC / "khong_co") / "khong_co_pgbin")
    env["FLS_PGDATA"] = str((tmp_path or GOC / "khong_co") / "cum_rong")
    env.update(bien or {})
    return subprocess.run(["bash", str(SCRIPT), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=120)


def _da_tu_choi_truoc_moi_buoc(kq: subprocess.CompletedProcess) -> None:
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-800:], kq.stderr[-800:])
    assert "══ dung_moi_truong_isp" not in kq.stdout, "chốt phải chạy TRƯỚC dòng tiêu đề"
    assert "⛔" in kq.stderr, "từ chối phải nói vì sao (stderr)"


# ── S0-R1-01 · ba đường R1 đo được — mong exit 2 ───────────────────────────────
@pytest.mark.parametrize("bien", [
    pytest.param({"PG_DSN": "postgresql://fls:fls@localhost:5433/fls_thu?port=5999"},
                 id="a_query_string_port"),
    pytest.param({"PG_DSN": "postgresql://x@10.0.0.9:5432/y@localhost:5433/fls_thu"},
                 id="b_glob_nuot_gach_cheo"),
    pytest.param({"PG_DSN": HOP_LE, "PGHOSTADDR": "10.255.255.1"},
                 id="c_bien_PGHOSTADDR"),
])
def test_S0_R1_01_ba_duong_lot_cua_R1_deu_exit_2(bien):
    _da_tu_choi_truoc_moi_buoc(_chay(["--chi-kiem"], bien))


@pytest.mark.parametrize("ten", ["PGHOST", "PGHOSTADDR", "PGPORT", "PGSERVICE", "PGSERVICEFILE"])
def test_S0_R1_01_moi_bien_PG_doi_dich_noi_deu_exit_2(ten):
    # đặt RỖNG cũng từ chối: chốt hỏi "biến có ĐẶT không", ⛔ hỏi giá trị
    _da_tu_choi_truoc_moi_buoc(_chay(["--chi-kiem"], {"PG_DSN": HOP_LE, ten: ""}))


@pytest.mark.parametrize("dsn", [
    pytest.param("postgres://fls:fls@localhost:5433/fls_thu", id="luoc_do_postgres"),
    pytest.param("postgresql://fls:fls@10.0.0.9:5433/fls_thu", id="host_la"),
    pytest.param("postgresql://fls:fls@localhost:5432/fls_thu", id="cong_ngoai_tap_ISP"),
    pytest.param("postgresql://fls@localhost:5433/fls_thu", id="thieu_mat_khau"),
    pytest.param("postgresql://fls:fls@localhost:5433/fls_thu?sslmode=disable", id="query_bat_ky"),
    pytest.param("postgresql://fls:fls@localhost:5433/Fls-Thu", id="ten_kho_ngoai_a_z0_9_"),
    pytest.param("host=localhost port=5433 dbname=fls_thu", id="dang_tu_khoa"),
    pytest.param("postgresql://fls:fls@localhost:5434/fls_thu", id="cong_DSN_khac_cong_luot"),
])
def test_S0_R1_01_DSN_lech_khuon_nguyen_chuoi_exit_2(dsn):
    _da_tu_choi_truoc_moi_buoc(_chay(["--chi-kiem"], {"PG_DSN": dsn}))


def test_S0_R1_01_PG_DSN_TEST_cung_chot_va_cung_cong():
    # `--duong-nen` chạy pytest ⇒ conftest DROP + CREATE kho của PG_DSN_TEST — cùng lớp rủi ro
    _da_tu_choi_truoc_moi_buoc(_chay(["--chi-kiem"], {
        "PG_DSN": HOP_LE,
        "PG_DSN_TEST": "postgresql://fls:fls@localhost:5434/fls_test"}))
    _da_tu_choi_truoc_moi_buoc(_chay(["--chi-kiem"], {
        "PG_DSN": HOP_LE,
        "PG_DSN_TEST": "postgresql://fls:fls@localhost:5433/fls_test?host=10.0.0.9"}))


# ── S0-R1-03 · CLI từ chối MỌI đối số ⛔ khai ──────────────────────────────────
@pytest.mark.parametrize("doi_so", [
    pytest.param(["--chi-kiem", "--la"], id="doi_so_thua_sau_che_do"),
    pytest.param(["--duong-nen", "--chi-kiem"], id="hai_che_do"),
    pytest.param(["--la"], id="doi_so_la"),
    pytest.param(["--cong"], id="cong_thieu_gia_tri"),
    pytest.param(["--cong", "5999"], id="cong_ngoai_tap_ISP"),
    pytest.param(["--cong", "5434", "--cong", "5435"], id="cong_hai_lan"),
    pytest.param(["--help", "--la"], id="help_kem_doi_so_khac"),
])
def test_S0_R1_03_doi_so_khong_khai_exit_2(doi_so):
    _da_tu_choi_truoc_moi_buoc(_chay(doi_so))


def test_Q1_cong_doi_so_va_bien_FLS_PG_PORT_mau_thuan_exit_2():
    _da_tu_choi_truoc_moi_buoc(_chay(["--cong", "5435", "--chi-kiem"], {"FLS_PG_PORT": "5434"}))


def test_Q1_FLS_PG_PORT_ngoai_tap_ISP_exit_2():
    _da_tu_choi_truoc_moi_buoc(_chay(["--chi-kiem"], {"FLS_PG_PORT": "5432"}))


# ── S0-R1-06 · ⛔ in mật khẩu — kể cả ở đường từ chối ──────────────────────────
def test_S0_R1_06_dong_tu_choi_che_mat_khau():
    kq = _chay(["--chi-kiem"], {"PG_DSN": "postgresql://fls:bimat123@10.0.0.9:5433/fls_thu"})
    _da_tu_choi_truoc_moi_buoc(kq)
    assert "bimat123" not in kq.stdout + kq.stderr
    assert "fls:***@" in kq.stderr


# ── Đối chứng (Đ5): DSN HỢP LỆ phải ĐI QUA chốt ────────────────────────────────
@pytest.mark.parametrize("doi_so,bien,cong", [
    pytest.param(["--chi-kiem"], {"PG_DSN": HOP_LE}, "5433", id="mac_dinh_5433"),
    pytest.param(["--cong", "5434", "--chi-kiem"],
                 {"PG_DSN": "postgresql://fls:fls@127.0.0.1:5434/fls_thu"}, "5434",
                 id="doi_so_cong_5434"),
    pytest.param(["--chi-kiem"], {"FLS_PG_PORT": "5447"}, "5447",
                 id="bien_FLS_PG_PORT_5447_DSN_mac_dinh"),
])
def test_doi_chung_DSN_hop_le_DI_QUA_chot(doi_so, bien, cong, tmp_path):
    kq = _chay(doi_so, bien, tmp_path)
    # exit 1 = qua chốt, rồi ĐỎ vì môi trường giả vắng (Đ5: ⛔ đo được là ĐỎ) — ⛔ phải 2
    assert kq.returncode == 1, (kq.returncode, kq.stdout[-1500:], kq.stderr[-800:])
    assert "══ dung_moi_truong_isp" in kq.stdout
    assert "══ KIỂM" in kq.stdout and "══ KẾT: ĐỎ" in kq.stdout
    assert f"(cổng {cong})" in kq.stdout
    # S0-R1-06: dòng tiêu đề che mật khẩu
    dong_dsn = [d for d in kq.stdout.splitlines() if d.strip().startswith("PG_DSN ")]
    assert len(dong_dsn) == 1 and ":***@" in dong_dsn[0], dong_dsn
    # Q1: cuối lượt in sẵn hai dòng export đúng cổng, kho `fls` / `fls_test` (tên kho test GIỮ)
    xuat = [d.strip() for d in kq.stdout.splitlines() if d.strip().startswith("export PG_DSN")]
    assert len(xuat) == 2, xuat
    assert xuat[0].startswith("export PG_DSN='postgresql://") and f":{cong}/" in xuat[0]
    assert xuat[1].startswith("export PG_DSN_TEST='postgresql://") and xuat[1].endswith(f":{cong}/fls_test'")
