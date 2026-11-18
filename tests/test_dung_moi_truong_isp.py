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

⛔⛔ **Vòng sửa sau R2** *(`KQ-068` — 1 NÊN SỬA + 4 GHI NHẬN)*. R2 đo thêm **năm** lỗ, mỗi
nhóm bài dưới canh một lỗ và đã chứng minh ĐỎ trên bản `fec4dd0` trước khi sửa:

    S0-R2-01  `--cong ''` lặng lẽ rơi về FLS_PG_PORT/5433 (cụm gốc S0)       exit 1, ⛔ 2
    S0-R2-02  khuôn chốt NHẬN khoảng trắng mà hàm che DỪNG ở khoảng trắng      in mật khẩu
    S0-R2-03  `PYTEST_ADDOPTS=--lf` ⇒ 26/2.460 bài chạy mà vẫn `KẾT: ĐẠT`      ⛔ mẫu số
    S0-R2-04  K2 đã ĐỎ mà pytest vẫn chạy ⇒ conftest DROP + CREATE kho test    ghi trước, đỏ sau

Bài của `S0-R2-03` gọi hàm `chay_pytest` **NGUYÊN VĂN** của script *(trích bằng `_trich`, ⛔
chép lại)* với một `python` GIẢ in log dựng sẵn — vì sau `S0-R2-04` pytest chỉ chạy khi K2
đạt, tức cần một cụm thật; phần đầu-cuối của đường nền đo ở `DUONG_NEN.md` §4.3.

⛔⛔ **Vòng sửa sau R3** *(`KQ-069` — 1 NÊN SỬA + 4 GHI NHẬN)*. R3 đo thêm ba lỗ ở mã, mỗi nhóm
bài dưới canh một lỗ và đã chứng minh ĐỎ trên bản `fb79f7e` trước khi sửa:

    S0-R3-01  `xfailed` đếm là "đã chạy" mà ⛔ có `mong` theo TÊN: làm hỏng một bài
              xanh rồi gắn `xfail(strict=True)` ⇒ `[ĐẠT] 26 = 26` · `KẾT: ĐẠT`         ⛔ mong xfail
    S0-R3-02  sàn `MONG_PYTEST_TOAN_BO = 2460` < 2.481 bài thu thập ⇒ bỏ im lặng 20
              bài vẫn ĐẠT                                                              sàn lỏng
    S0-R3-03  DSN gõ SAI lược đồ (`fls:<mk>@…` · `postgresql:/…` · `postgresql:…`)
              bị từ chối nhưng câu từ chối in NGUYÊN mật khẩu                          in mật khẩu

Bài `S0-R3-01` chạy `chay_pytest` + khối `KẾT` NGUYÊN VĂN của script: một lần với `python` giả
in short summary dựng từ tệp đường nền THẬT, một lần với pytest THẬT trên một cây bài nhỏ ở
`tmp_path` và một plugin `PYTEST_PLUGINS` đổi bài xanh thành xfail *(đường R3 đã dùng)*.
"""
from __future__ import annotations

import concurrent.futures
import os
import pathlib
import re
import shlex
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
    # `errors="replace"`: bài S0-R2-02 đưa byte UTF-8 LẺ vào DSN — nếu script để lọt nó ra thì
    # bài phải FAIL vì thấy mảnh mật khẩu, ⛔ ERROR vì giải mã stdout hỏng.
    return subprocess.run(["bash", str(SCRIPT), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, errors="replace", timeout=120)


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


# ═════════════════════════════════════════════════ vòng sửa sau R2 (`KQ-068`)

# ── S0-R2-01 · giá trị RỖNG là lỗi đầu vào, ⛔ phải "không đưa" ─────────────────
#    R2 đo: `--cong '' --chi-kiem` ⇒ tiêu đề `(cổng 5433)` · exit 1; `--cong '' --cong 5435`
#    ⇒ chạy 5435 — chốt "hai lần" hỏi `-n "$CONG_DOI_SO"` nên ⛔ thấy lần đầu. Đường thật:
#    `--cong "$BIEN"` với biến rỗng ⇒ dựng / `--duong-nen` đi vào cụm 5433 của người khác.
@pytest.mark.parametrize("doi_so,bien", [
    pytest.param(["--cong", "", "--chi-kiem"], {}, id="cong_rong"),
    pytest.param(["--cong", "", "--cong", "5435", "--chi-kiem"], {}, id="cong_rong_roi_cong_that"),
    pytest.param(["--cong", "5435", "--cong", "", "--chi-kiem"], {}, id="cong_that_roi_cong_rong"),
    # cùng lớp, nguồn thứ hai của cổng (sổ `S0-R2-01` · Khuyến nghị: "FLS_PG_PORT đặt-mà-rỗng")
    pytest.param(["--chi-kiem"], {"FLS_PG_PORT": ""}, id="bien_FLS_PG_PORT_dat_rong"),
])
def test_S0_R2_01_cong_rong_exit_2(doi_so, bien, tmp_path):
    _da_tu_choi_truoc_moi_buoc(_chay(doi_so, bien, tmp_path))


# ── S0-R2-02 · khuôn CHẤP NHẬN và hàm CHE dùng MỘT lớp ký tự ────────────────────
#    R2 đo: `fls:bi mat@…` QUA chốt và in mật khẩu nguyên văn 4 dòng; `fls:ab@cdXYZ@…` bị từ
#    chối nhưng câu từ chối in `fls:***@cdXYZ@…`; `password='a b'` ⇒ `password=*** b'`.
#    Luật sổ: thử hàm che bằng CẢ tập chốt cho qua LẪN tập chốt từ chối mà vẫn in ra.
@pytest.mark.parametrize("dsn,manh", [
    pytest.param("postgresql://fls:bi mat9@localhost:5433/fls_thu", ("mat9",),
                 id="mat_khau_co_khoang_trang"),
    pytest.param("postgresql://fls:ab@cdXYZ@localhost:5433/fls_thu", ("cdXYZ",),
                 id="mat_khau_co_a_cong_tho"),
    pytest.param("host=localhost port=5433 dbname=fls_thu password='a b9Q'", ("b9Q",),
                 id="dang_tu_khoa_mat_khau_trong_nhay"),
    pytest.param("postgresql://f s:bimat7@localhost:5433/fls_thu", ("bimat7",),
                 id="user_co_khoang_trang"),
    pytest.param("postgresql://fls:zz8ab\ncd7Q@localhost:5433/fls_thu", ("zz8ab", "cd7Q"),
                 id="mat_khau_co_xuong_dong"),
])
def test_S0_R2_02_khong_lo_manh_mat_khau(dsn, manh, tmp_path):
    kq = _chay(["--chi-kiem"], {"PG_DSN": dsn}, tmp_path)
    ra = kq.stdout + kq.stderr
    lo = [m for m in manh if m in ra]
    assert not lo, (lo, [d for d in ra.splitlines() if any(m in d for m in manh)])
    # cả năm đều NGOÀI lớp ký tự của khuôn ⇒ bị chốt TỪ CHỐI, ⛔ đi qua rồi mới trông vào hàm che
    _da_tu_choi_truoc_moi_buoc(kq)


# Ký tự ⛔ phải chữ/số trong ASCII in được + khoảng trắng điều khiển + NBSP + một byte UTF-8 LẺ
# (`\udca0` ⇒ byte 0xA0 qua surrogateescape). Đo khi viết bài: `sed` ở locale UTF-8 ⛔ khớp `.`
# qua byte lẻ ⇒ lọt; Python đặt `LC_CTYPE=C.UTF-8` cho tiến trình con (PEP 538) còn shell
# container là POSIX — tức cùng một script chạy ở HAI locale, nên lớp ký tự phải đọc theo BYTE.
_KY_TU_LA = ([c for c in map(chr, range(0x20, 0x7F)) if not c.isalnum()]
             + ["\t", "\n", "\r", "\u00a0", "\udca0"])


# S0-R3-03 · ca biến CẤU TRÚC, ⛔ chỉ biến ký tự. R3 (`KQ-069` F-3) đo: hàm che chỉ nhận ra mật
# khẩu khi chuỗi có `://` ⇒ DSN gõ SAI lược đồ bị chốt từ chối (đúng) nhưng câu từ chối in NGUYÊN
# mật khẩu — `⛔ PG_DSN=fls:<mk>@localhost:5433/fls_thu ⛔ khớp NGUYÊN CHUỖI …`; có từ bản
# `fec4dd0` ⇒ ⛔ hồi quy, chỉ là khe của phép quét ký tự. Ba ca đầu là ba dạng R3 đo; ca thứ tư
# (`thiếu @` — gõ `/` thay `@`) là hạng "thiếu @" mà luật phòng tái phạm của sổ nêu tên.
_CAU_TRUC_SAI = (
    ("thiếu lược đồ", "fls:Kq7Wx9@localhost:5433/fls_thu"),
    ("lược đồ một gạch", "postgresql:/fls:Kq7Wx9@localhost:5433/fls_thu"),
    ("lược đồ ⛔ gạch", "postgresql:fls:Kq7Wx9@localhost:5433/fls_thu"),
    ("thiếu @", "postgresql://fls:Kq7Wx9/localhost:5433/fls_thu"),
)


def test_S0_R2_02_moi_ky_tu_la_hoac_bi_chot_tu_choi_hoac_bi_che_tron(tmp_path):
    """Mỗi ký tự lạ, ở mật khẩu RỒI ở tên user: ⛔ một mảnh mật khẩu nào ra stdout/stderr.

    Mật khẩu là `Kq7<c>Wx9` — hai mảnh hai bên ký tự lạ, để thấy cả lỗi "che nửa đầu, lộ
    đuôi" (`@` thô) lẫn "lộ nửa đầu" (xuống dòng: bản cũ che theo DÒNG). Ca nào QUA chốt
    (exit 1 — môi trường giả vắng) thì dòng tiêu đề + hai dòng `export` phải che; ca nào bị
    từ chối (exit 2) thì câu từ chối phải che.

    ⛔⛔ Vòng sửa sau R3 (`S0-R3-03`): thêm các ca `_CAU_TRUC_SAI` — mật khẩu `Kq7Wx9` trong một
    DSN SAI CẤU TRÚC; mỗi ca phải bị chốt TỪ CHỐI (exit 2) và ⛔ lộ mảnh nào.
    """
    def mot(ca: tuple[str, str, str]) -> tuple[str, str, int, list[str]]:
        noi, c, dsn = ca
        kq = _chay(["--chi-kiem"], {"PG_DSN": dsn}, tmp_path)
        ra = kq.stdout + kq.stderr
        return noi, c, kq.returncode, [d for d in ra.splitlines() if "Kq7" in d or "Wx9" in d]

    ca = [(noi, c, f"postgresql://fls:Kq7{c}Wx9@localhost:5433/fls_thu" if noi == "mật khẩu"
           else f"postgresql://f{c}u:Kq7Wx9@localhost:5433/fls_thu")
          for noi in ("mật khẩu", "tên user") for c in _KY_TU_LA]
    ca += [("cấu trúc", nhan, dsn) for nhan, dsn in _CAU_TRUC_SAI]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as tp:
        kq = list(tp.map(mot, ca))
    # mẫu số (Đ3): 33 + 5 ký tự × 2 nơi = 76 · cộng 4 ca cấu trúc (S0-R3-03)
    assert len(kq) == 2 * len(_KY_TU_LA) + len(_CAU_TRUC_SAI) == 76 + 4
    lo = [(noi, repr(c), ma, dong) for noi, c, ma, dong in kq if dong]
    assert not lo, lo
    la_ma = [(noi, repr(c), ma) for noi, c, ma, _ in kq if ma not in (1, 2)]
    assert not la_ma, la_ma
    # khoảng trắng nằm NGOÀI lớp ký tự (libpq vốn từ chối) ⇒ chốt từ chối, ⛔ cho qua
    qua = [(noi, repr(c)) for noi, c, ma, _ in kq
           if noi != "cấu trúc" and c in " \t\n\r" and ma != 2]
    assert not qua, qua
    # tiền đề của ca cấu trúc: chốt TỪ CHỐI — ⛔ xanh vì chuỗi đi qua rồi chết ở bước sau
    qua_cau_truc = [(c, ma) for noi, c, ma, _ in kq if noi == "cấu trúc" and ma != 2]
    assert not qua_cau_truc, qua_cau_truc


# ── S0-R2-03 · cổng so TẬP phải canh cả MẪU SỐ ─────────────────────────────────
#    R2 đo: `PYTEST_ADDOPTS=--lf … --duong-nen` ⇒ toàn bộ `12 failed, 14 errors in 0.94s`
#    (26 / 2.460 bài) ⇒ `[ĐẠT] … 26 = 26` · `KẾT: ĐẠT` exit 0; log tổng hợp cùng 26 id với
#    `2000 skipped` / `2434 deselected` ⇒ `[ĐẠT]`. Bài dưới chạy `chay_pytest` NGUYÊN VĂN.
def _trich(*ten: str) -> str:
    """Trích NGUYÊN VĂN từ script định nghĩa hàm `ten() {…}` / phép gán `ten=…` ở đầu dòng.

    Hàm một dòng (`dat() { …; }`) lấy một dòng; hàm nhiều dòng lấy tới dòng `}` đầu tiên ở cột
    0. Tên ⛔ có trong script ⇒ bỏ qua (bản cũ ⛔ có hằng mới — bài phải ĐỎ vì HÀNH VI, ⛔ vì
    trích hỏng); hàm nào thiếu thật thì `bash` báo `command not found` ⇒ bài vẫn ĐỎ.
    """
    dong = SCRIPT.read_text(encoding="utf-8").splitlines()
    ra: list[str] = []
    for t in ten:
        vt = [k for k, d in enumerate(dong) if d.startswith((f"{t}() {{", f"{t}="))]
        if not vt:
            continue
        i = vt[0]
        if dong[i].startswith(f"{t}=") or dong[i].rstrip().endswith("}"):
            ra.append(dong[i])
        else:
            j = next(k for k in range(i + 1, len(dong)) if dong[k] == "}")
            ra.extend(dong[i:j + 1])
    return "\n".join(ra)


_ID_A = "tests/a/test_gia.py::test_mot"
_ID_B = "tests/web/test_gia.py::test_hai"


def _chay_pytest_gia(tmp_path: pathlib.Path, tong: str, mong: int,
                     bien: dict[str, str] | None = None) -> tuple[subprocess.CompletedProcess, str]:
    """`chay_pytest "toàn bộ" "" <mong>` của script với `python` GIẢ: in một log `-rfE` dựng sẵn
    (khối `short test summary info` có đúng 2 node = tệp đường nền giả, rồi dòng tổng kết `tong`),
    ghi lại đối số + `PYTEST_ADDOPTS` nó thấy, exit 1 (= có bài đỏ, như đường nền thật)."""
    nen = tmp_path / "duong_nen_gia.txt"
    nen.write_text(f"{_ID_A}\n{_ID_B}\n", encoding="utf-8")
    log = tmp_path / "log_gia.txt"
    log.write_text("....F.E\n"
                   "=========================== short test summary info ============================\n"
                   f"FAILED {_ID_A} - AssertionError: gia\n"
                   f"ERROR {_ID_B} - LookupError: gia\n"
                   f"{tong}\n", encoding="utf-8")
    ghi = tmp_path / "py_gia.ghi"
    py = tmp_path / "python_gia"
    py.write_text('#!/usr/bin/env bash\n'
                  'printf "ARGS %s\\n" "$*" >> "$PY_GIA_GHI"\n'
                  'printf "ADDOPTS %s\\n" "${PYTEST_ADDOPTS-<vang>}" >> "$PY_GIA_GHI"\n'
                  'cat "$PY_GIA_LOG"; exit 1\n', encoding="utf-8")
    py.chmod(0o755)
    ma = "\n".join([
        "set -uo pipefail",
        _trich("DO", "dat", "do_", "so_tap_do", "chay_pytest"),
        f"PY={shlex.quote(str(py))}; DUONG_NEN_DO={shlex.quote(str(nen))}",
        f'chay_pytest "toàn bộ" "" {mong}',
        'echo "DO=$DO"',
    ])
    env = {k: v for k, v in os.environ.items() if k != "PYTEST_ADDOPTS"}
    env.update({"PY_GIA_GHI": str(ghi), "PY_GIA_LOG": str(log), "TMPDIR": str(tmp_path)})
    env.update(bien or {})
    kq = subprocess.run(["bash", "-c", ma], env=env, capture_output=True, text=True, timeout=60)
    return kq, (ghi.read_text(encoding="utf-8") if ghi.exists() else "")


@pytest.mark.parametrize("tong,mong_dat", [
    # đối chứng (Đ5 — chiều XANH): đúng mẫu số đường nền ⇒ ĐẠT; bước sau THÊM bài ⇒ vẫn ĐẠT (≥)
    pytest.param("1 failed, 2458 passed, 1 error in 3.00s", True, id="du_2460_DAT"),
    pytest.param("1 failed, 2488 passed, 1 error in 3.00s", True, id="them_bai_2490_DAT"),
    pytest.param("1 failed, 2455 passed, 2 xfailed, 1 xpassed, 1 error in 3.00s", True,
                 id="xfailed_xpassed_tinh_la_da_chay_DAT"),
    pytest.param("===== 1 failed, 2458 passed, 1 error in 3.00s =====", True,
                 id="dong_tong_ket_co_vien_DAT"),
    # R2: cùng tập đỏ trên một bộ bài TEO ⇒ phải ĐỎ
    pytest.param("1 failed, 458 passed, 2000 skipped, 1 error in 1.00s", False, id="skipped_DO"),
    pytest.param("1 failed, 1 error, 2458 deselected in 0.50s", False, id="deselected_DO"),
    pytest.param("1 failed, 1 error in 0.94s", False, id="lf_chi_2_bai_DO"),
    pytest.param("1 failed, 2457 passed, 1 error in 3.00s", False, id="thieu_1_bai_2459_DO"),
])
def test_S0_R2_03_mau_so_duong_nen(tong, mong_dat, tmp_path):
    kq, _ = _chay_pytest_gia(tmp_path, tong, 2460)
    dong = [d for d in kq.stdout.splitlines() if "đường nền toàn bộ" in d]
    assert len(dong) == 1, (kq.stdout, kq.stderr)
    if mong_dat:
        assert dong[0].startswith("  [ĐẠT]") and "DO=0" in kq.stdout, kq.stdout
        # số bài CHẠY in cạnh `2 = 2` — ⛔ để người đọc tự cộng dòng tổng kết
        assert "2 = 2 node id" in dong[0] and re.search(r"chạy 2\d{3} bài", dong[0]), dong[0]
    else:
        assert dong[0].startswith("  [ĐỎ]") and "DO=1" in kq.stdout, kq.stdout
        assert "skipped" in dong[0] and "deselected" in dong[0], dong[0]


def test_S0_R2_03_PYTEST_ADDOPTS_cua_nguoi_goi_bi_go(tmp_path):
    kq, ghi = _chay_pytest_gia(tmp_path, "1 failed, 2458 passed, 1 error in 3.00s", 2460,
                               {"PYTEST_ADDOPTS": "--lf"})
    assert "ARGS -m pytest -rfE" in ghi, (ghi, kq.stdout, kq.stderr)     # python giả ĐÃ được gọi
    assert "ADDOPTS <vang>" in ghi and "--lf" not in ghi, ghi


def test_S0_R2_03_hang_mau_so_khai_MOT_cho():
    """2.460 = 12 + 2432 + 2 + 14 (lượt toàn bộ chính thức R2); 664 = 3 + 661 (`tests/web`).

    ⛔⛔ S0-R3-02 (Q8 = A): ghim nâng 2460 → **2490** = số bài THU THẬP của nhánh sau vòng sửa R3
    (`pytest --collect-only`: 2.481 của R3 + 9 bài mới · 211 tệp) — số 2460 là của vòng R1 bị để
    lại ở R2 (+21 bài) ⇒ khoảng dư 21 mà R3 lách bằng 20 bài bỏ im lặng. Bài ghim GIỮ việc gốc:
    hằng khai MỘT chỗ, đúng giá trị, hai dòng gọi dùng hằng; `test_S0_R3_02_…` đòi hằng = thu thập.
    Gộp (orchestrator, luật 17/11: sàn = số thu thập CÂY GỘP, ⛔ cộng tay): + `isp/DT1A` ⇒ **2530** · + `isp/H1` ⇒ **2579** · + `isp/C1` ⇒ **2704** · + `isp/DT2` ⇒ **2792** · + `isp/H2` ⇒ **2857** · + `isp/CG1` ⇒ **2890** (xung đột script + bài ghim ⇒ giữ bản nhánh làm việc — `CG1-R2-01`) · + `isp/DT1B` ⇒ **2980** · + `isp/DT3` ⇒ **3064** · + `isp/FG` ⇒ **3067** (web 664 ⇒ **667**: FG thêm bài `tests/web`) · + `isp/DT4` ⇒ **3100** · + `isp/C4` ⇒ **3141** · + `isp/DT1BT` ⇒ **3186** · + `isp/DT5` ⇒ **3219** · + `isp/H4` ⇒ **3262** · + `isp/C5` ⇒ **3296** · + `isp/DT8` ⇒ **3343** · + `isp/C6` ⇒ **3377** · + `isp/DT1BM` ⇒ **3399** · + `isp/F4` ⇒ **3407** (web 667 ⇒ **675**: F4 thêm bài `tests/web`) · + `isp/C9` ⇒ **3447** (+40 bài đo thu thập: `test_vendor.py` + `test_vendor_pg.py` + `test_isp_config_ven.py`; web giữ 675) · + `isp/C9` ⇒ **3447** · + `isp/C8` ⇒ **3466** (xung đột `fls/repo/cau_hinh_repo.py` C9 ↔ C8 ⇒ giữ CẢ HAI nhánh) · + `isp/H5` ⇒ **3493** · + `isp/C11` ⇒ **3557** · + `isp/DT10` ⇒ **3588** (+29 bài `tests/du_lieu/test_dap_an_atl.py`; web giữ 675). ⚠ Đo nền `fba4849` = 3559 bài thu thập, ⛔ 3557 như hằng cũ — lệch 2 có từ trước; nâng hằng về số THU THẬP của cây.
    """
    van = SCRIPT.read_text(encoding="utf-8")
    assert re.findall(r"^MONG_PYTEST_TOAN_BO=(\d+)$", van, re.M) == ["3588"]
    assert re.findall(r"^MONG_PYTEST_WEB=(\d+)$", van, re.M) == ["675"]
    goi = [d.strip() for d in van.splitlines() if d.strip().startswith("chay_pytest ")]
    assert len(goi) == 2 and '"$MONG_PYTEST_TOAN_BO"' in goi[0] and '"$MONG_PYTEST_WEB"' in goi[1], goi


# ── S0-R2-04 · phép kiểm định danh đã ĐỎ ⇒ ⛔ bước GHI nào sau nó ──────────────
#    R2 đo: `FLS_PGDATA=<thư mục ⛔ phải cụm>` + `--duong-nen` ⇒ `[ĐỎ] dựng · cụm` + K2 `[ĐỎ]` mà
#    hai lượt pytest vẫn chạy; OID `fls_test` đổi (conftest DROP + CREATE) — đỏ đúng, nhưng SAU
#    khi đã ghi. Ở đây: venv GIẢ có `python` ghi lại mọi lần bị gọi, binary PG vắng ⇒ dựng ĐỎ +
#    K2 ĐỎ; `--duong-nen` ⇒ ⛔ một lần gọi `python -m pytest` nào.
def test_S0_R2_04_dung_hoac_K2_DO_thi_KHONG_chay_pytest(tmp_path):
    venv = tmp_path / "venv_gia"
    (venv / "bin").mkdir(parents=True)
    ghi = tmp_path / "py_gia.ghi"
    py = venv / "bin" / "python"
    py.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$PY_GIA_GHI"\nexit 1\n',
                  encoding="utf-8")
    py.chmod(0o755)
    kq = _chay(["--duong-nen"], {"PG_DSN": HOP_LE, "FLS_VENV": str(venv), "PY_GIA_GHI": str(ghi)},
               tmp_path)
    goi = ghi.read_text(encoding="utf-8").splitlines() if ghi.exists() else []
    assert kq.returncode == 1, (kq.returncode, kq.stdout[-1500:], kq.stderr[-800:])
    # tiền đề của bài: dựng ĐỎ + K2 ĐỎ thật, và python giả ĐÃ được gọi (⛔ xanh vì ⛔ ai gọi nó)
    assert "[ĐỎ]  dựng · cụm" in kq.stdout and "[ĐỎ]  cụm PG localhost:5433" in kq.stdout, kq.stdout
    assert goi, "python giả phải được gọi ở bước dựng/kiểm"
    assert not [g for g in goi if g.startswith("-m pytest")], goi
    assert re.search(r"\[ĐỎ\]\s+pytest.*bỏ qua", kq.stdout), kq.stdout[-1500:]


# ═════════════════════════════════════════════════ vòng sửa sau R3 (`KQ-069`)

# ── S0-R3-01 · `xfailed` có `mong` theo TÊN — và theo LOẠI ────────────────────
#    R3 đo đầu-cuối (cụm 5433, plugin qua `PYTEST_PLUGINS`): làm HỎNG `tests/web/test_wo022_…`
#    (đang xanh) rồi gắn `xfail(strict=True)` ⇒ toàn bộ `12 failed, 2432 passed, 3 xfailed,
#    14 errors` ⇒ `[ĐẠT] 26 = 26 · chạy 2461` · web `[ĐẠT] 3 = 3 · chạy 664 (mong ≥ 664)` ·
#    `KẾT: ĐẠT` exit 0. Gốc: `-rfE` ⛔ liệt kê `XFAIL`, và `xfailed` cộng vào "chạy" mà ⛔ có
#    `mong` về SỐ hay TÊN — `xfail(strict)` lại là CHÍNH thành ngữ "bài đỏ đã biết" của repo.
#    ⇒ `-rfEx`; tệp đường nền khai từng node xfail bằng dòng `XFAIL <id>` (cùng chữ pytest in ở
#    short summary); tập đo = `<id>` của FAILED/ERROR + `XFAIL <id>` — so theo TÊN và LOẠI.
_NEN_THAT = GOC / "docs" / "ITL" / "03_Dev" / "isp-3.1" / "duong_nen_bai_do.txt"
# hai dấu `xfail(strict=True)` đang sống — `2 xfailed` ở mọi lượt toàn bộ từ 16/11 (DUONG_NEN §4)
_XF_NEN = (
    "tests/nghiem_thu/test_kq046_chieu_nguoc_ung_vien_pm_mot_tap.py"
    "::test_F1_chieu_nguoc_ung_vien_pm_BANG_ma_tien_te",
    "tests/nghiem_thu/test_kq061_f02_het_gio_lo_luu.py"
    "::test_F1_HET_GIO_lo_luu_F02_KHONG_noi_o_CHUA_vao_so",
)
# bài XANH mà R3 làm hỏng rồi gắn xfail ở lượt đầu-cuối
_XF_MOI = "tests/web/test_wo022_tien_theo_tien_te.py::test_AC1_tien_MUOI_HAI_ca_dung_tung_byte"


def _ket() -> str:
    """Khối KẾT cuối script NGUYÊN VĂN (từ `if [ "$DO" = 0 ]; then` tới hết tệp): exit 0 +
    `KẾT: ĐẠT` khi DO = 0, exit 1 + `KẾT: ĐỎ` khi khác — bài đòi đúng dòng agent đọc, ⛔ chỉ `DO`."""
    dong = SCRIPT.read_text(encoding="utf-8").splitlines()
    vt = [k for k, d in enumerate(dong) if d == 'if [ "$DO" = 0 ]; then']
    assert len(vt) == 1, vt
    return "\n".join(dong[vt[0]:])


def _chay_duong_nen(tmp_path: pathlib.Path, py: str, nen: pathlib.Path, goi: str,
                    bien: dict[str, str] | None = None,
                    cwd: pathlib.Path | None = None) -> subprocess.CompletedProcess:
    """Hằng `MONG_…` + `dat` · `do_` · `so_tap_do` · `chay_pytest` + dòng gọi `goi` + khối KẾT —
    tất cả NGUYÊN VĂN của script (`_trich` · `_ket`), với `PY` = `py`, tệp đường nền = `nen`."""
    ma = "\n".join([
        "set -uo pipefail",
        _trich("DO", "MONG_PYTEST_TOAN_BO", "MONG_PYTEST_WEB", "dat", "do_", "so_tap_do", "chay_pytest"),
        f"PY={shlex.quote(py)}; DUONG_NEN_DO={shlex.quote(str(nen))}",
        goi,
        _ket(),
    ])
    env = {k: v for k, v in os.environ.items() if k not in ("PYTEST_ADDOPTS", "PYTEST_PLUGINS")}
    env["TMPDIR"] = str(tmp_path)
    env.update(bien or {})
    return subprocess.run(["bash", "-c", ma], cwd=cwd or tmp_path, env=env,
                          capture_output=True, text=True, timeout=120)


def _dong_duong_nen(kq: subprocess.CompletedProcess, nhan: str = "toàn bộ") -> str:
    dong = [d for d in kq.stdout.splitlines() if f"đường nền {nhan}" in d]
    assert len(dong) == 1, (kq.returncode, kq.stdout, kq.stderr)
    return dong[0]


def test_S0_R3_01_tep_duong_nen_khai_hai_xfail_theo_TEN():
    """Tệp đường nền khai ĐÚNG hai node xfail đang sống — theo TÊN (⛔ chỉ số), và lời khai ấy
    THẬT: mỗi tên mang dấu `@pytest.mark.xfail(strict=True …)` ngay trên `def` trong nguồn."""
    dong = [d for d in _NEN_THAT.read_text(encoding="utf-8").splitlines() if d.strip()]
    xf = [d.removeprefix("XFAIL ") for d in dong if d.startswith("XFAIL ")]
    assert sorted(xf) == sorted(_XF_NEN), xf
    for nid in _XF_NEN:
        tep, ten = nid.split("::")
        van = (GOC / tep).read_text(encoding="utf-8")
        assert re.search(rf"@pytest\.mark\.xfail\(strict=True(?:(?!\ndef ).)*\ndef {ten}\(",
                         van, re.S), nid


@pytest.mark.parametrize("ca,them,bot", [
    # đối chứng (Đ5 — chiều XANH): đúng đường nền THẬT — 26 đỏ + 2 xfail, chạy = mong (sàn KHÍT)
    pytest.param("doi_chung", 0, 0, id="duong_nen_that_DAT"),
    # R3: bước sau làm HỎNG một bài xanh rồi gắn xfail(strict) — số bài chạy ⛔ đổi
    pytest.param("them_xfail", 1, 0, id="bai_xanh_hong_roi_gan_xfail_DO"),
    # chiều ngược: một xfail tự xanh (xpass ⛔ strict) hay bị gỡ khỏi bộ — đường nền ⛔ ghi lại
    pytest.param("bot_xfail", 0, 1, id="mot_xfail_bien_mat_DO"),
    # đổi LOẠI: xfail(strict) tự qua ⇒ pytest in `FAILED … [XPASS(strict)]` — cùng TÊN, khác loại
    pytest.param("xfail_thanh_do", 1, 1, id="xfail_strict_tu_qua_thanh_FAILED_DO"),
    # đổi LOẠI chiều kia: một bài đỏ có sẵn bị gắn xfail — "chấp nhận" mà ⛔ sửa tệp đường nền
    pytest.param("do_thanh_xfail", 1, 1, id="bai_do_co_san_bi_gan_xfail_DO"),
])
def test_S0_R3_01_tap_xfail_co_mong_theo_TEN_va_LOAI(ca, them, bot, tmp_path):
    """`chay_pytest "toàn bộ" …` đúng DÒNG GỌI của script, với hằng `MONG_PYTEST_TOAN_BO` và tệp
    đường nền THẬT; `python` giả in short summary dựng từ tệp ấy. Tổng chạy giữ = mong ở MỌI ca
    — chỉ TÊN/LOẠI đổi — để thấy cổng tập bắt được, ⛔ nhờ cổng mẫu số."""
    van = SCRIPT.read_text(encoding="utf-8")
    mong = int(re.search(r"^MONG_PYTEST_TOAN_BO=(\d+)$", van, re.M).group(1))
    goi = [d.strip() for d in van.splitlines() if d.strip().startswith('chay_pytest "toàn bộ"')]
    assert len(goi) == 1, goi
    do = [d for d in _NEN_THAT.read_text(encoding="utf-8").splitlines()
          if d.strip() and not d.startswith("XFAIL ")]
    assert len(do) >= 26, len(do)                                   # mẫu số (Đ3)
    xf = list(_XF_NEN)
    mong_dong: list[str] = []
    if ca == "them_xfail":
        xf.append(_XF_MOI)
        mong_dong = [f"+ THÊM  XFAIL {_XF_MOI}"]
    elif ca == "bot_xfail":
        mong_dong = [f"− BỚT   XFAIL {xf.pop()}"]
    elif ca == "xfail_thanh_do":
        do.append(xf.pop())
        mong_dong = [f"+ THÊM  {do[-1]}", f"− BỚT   XFAIL {do[-1]}"]
    elif ca == "do_thanh_xfail":
        xf.append(do.pop(0))
        mong_dong = [f"+ THÊM  XFAIL {xf[-1]}", f"− BỚT   {xf[-1]}"]
    log = tmp_path / "log_gia.txt"
    log.write_text(
        "=========================== short test summary info ============================\n"
        + "".join(f"FAILED {i} - AssertionError: nen\n" for i in do)
        + "".join(f"XFAIL {i} - ly do\n" for i in xf)
        + f"{len(do)} failed, {mong - len(do) - len(xf)} passed, {len(xf)} xfailed in 300.00s\n",
        encoding="utf-8")
    py = tmp_path / "python_gia"
    py.write_text('#!/usr/bin/env bash\nprintf "%s\\n" "$*" >> "$PY_GIA_GHI"\ncat "$PY_GIA_LOG"; exit 1\n',
                  encoding="utf-8")
    py.chmod(0o755)
    ghi = tmp_path / "py_gia.ghi"
    kq = _chay_duong_nen(tmp_path, str(py), _NEN_THAT, goi[0],
                         {"PY_GIA_LOG": str(log), "PY_GIA_GHI": str(ghi)})
    dong = _dong_duong_nen(kq)
    assert f"chạy {mong} bài" in dong or f"chạy {mong} ·" in dong, dong
    if ca == "doi_chung":
        assert kq.returncode == 0 and "══ KẾT: ĐẠT" in kq.stdout, kq.stdout
        assert dong.startswith("  [ĐẠT]") and "XFAIL 2 = 2" in dong, dong
    else:
        assert kq.returncode == 1 and "══ KẾT: ĐỎ" in kq.stdout, kq.stdout
        assert dong.startswith("  [ĐỎ]") and f"thêm {them} · bớt {bot}" in dong, dong
        thieu = [m for m in mong_dong if m not in kq.stdout]
        assert not thieu, (thieu, kq.stdout)
    # `-rfEx`: ⛔ `x` thì pytest THẬT ⛔ in dòng XFAIL nào — log giả ở đây vẫn in, nên khẳng định
    # cờ (sau hành vi: bản cũ phải ĐỎ vì HÀNH VI trước, ⛔ vì cờ)
    assert ghi.read_text(encoding="utf-8").split()[:3] == ["-m", "pytest", "-rfEx"], ghi.read_text()


# Cây bài NHỎ cho pytest THẬT: một bài xanh · một bài đỏ có sẵn · một xfail(strict) có sẵn.
_MINI = '''import pytest


def test_xanh():
    assert 1 + 1 == 2


def test_do_co_san():
    assert 0, "đỏ có sẵn"


@pytest.mark.xfail(strict=True, reason="lỗi đã biết - có gạch giữa")
def test_xf_co_san():
    assert 0
'''

# Đúng đường R3 dùng: plugin nạp qua `PYTEST_PLUGINS` (`env -u PYTEST_ADDOPTS` ⛔ chặn) làm HỎNG
# bài xanh rồi gắn `xfail(strict=True)` lên nó.
_PLUGIN_LACH = '''import pytest


def pytest_collection_modifyitems(session, config, items):
    for i in items:
        if i.name == "test_xanh":
            i.add_marker(pytest.mark.xfail(strict=True, reason="giả lập: hồi quy được che bằng xfail"))


@pytest.hookimpl(tryfirst=True)
def pytest_pyfunc_call(pyfuncitem):
    if pyfuncitem.name == "test_xanh":
        raise AssertionError("giả lập: hồi quy")
'''


@pytest.mark.parametrize("lach", [
    pytest.param(False, id="doi_chung_DAT"),
    pytest.param(True, id="plugin_doi_bai_xanh_thanh_xfail_KET_DO"),
])
def test_S0_R3_01_pytest_THAT_plugin_doi_bai_xanh_thanh_xfail(lach, tmp_path):
    """pytest THẬT (venv) chạy qua `chay_pytest` NGUYÊN VĂN — chứng minh cờ `-r` của script làm
    pytest IN dòng `XFAIL <id>` và cổng đọc được nó, ⛔ chỉ tin log dựng tay."""
    mini = tmp_path / "mini"
    mini.mkdir()
    (mini / "pytest.ini").write_text("[pytest]\naddopts = -q -p no:cacheprovider\n", encoding="utf-8")
    (mini / "test_mini.py").write_text(_MINI, encoding="utf-8")
    plug = tmp_path / "plug"
    plug.mkdir()
    (plug / "r3_lach_mini.py").write_text(_PLUGIN_LACH, encoding="utf-8")
    nen = tmp_path / "duong_nen_mini.txt"
    nen.write_text("XFAIL test_mini.py::test_xf_co_san\ntest_mini.py::test_do_co_san\n", encoding="utf-8")
    bien = {"PYTHONPATH": str(plug)}
    if lach:
        bien["PYTEST_PLUGINS"] = "r3_lach_mini"
    kq = _chay_duong_nen(tmp_path, sys.executable, nen, 'chay_pytest "toàn bộ" "" 3', bien, cwd=mini)
    dong = _dong_duong_nen(kq)
    assert "chạy 3" in dong, dong                 # số bài chạy ⛔ đổi — lỗ ⛔ nhờ cổng mẫu số
    if not lach:
        assert kq.returncode == 0 and "══ KẾT: ĐẠT" in kq.stdout, kq.stdout
        assert dong.startswith("  [ĐẠT]") and "2 = 2 node id" in dong, dong
    else:
        assert kq.returncode == 1 and "══ KẾT: ĐỎ" in kq.stdout, kq.stdout
        assert dong.startswith("  [ĐỎ]") and "thêm 1 · bớt 0" in dong, dong
        assert "+ THÊM  XFAIL test_mini.py::test_xanh" in kq.stdout, kq.stdout


# ── S0-R3-02 · hằng mẫu số = số bài THU THẬP của nhánh (Q8 = A) ─────────────────
#    R3 đo: vòng sửa R2 thêm 21 bài, nhánh thu thập 2.481 bài (211 tệp) mà sàn vẫn 2460 ⇒ bỏ
#    IM LẶNG cả `tests/adapters/test_bank.py` (20 bài, ⛔ dòng `deselected`) ⇒ `chạy 2461 bài
#    (mong ≥ 2460)` ⇒ `[ĐẠT]`. Q8 = A: bước nào thêm bài thì nâng hằng TRONG CÙNG commit — bài này
#    làm luật ấy thành máy: thêm/bớt một bài mà ⛔ sửa hằng ⇒ ĐỎ.
def test_S0_R3_02_hang_mau_so_bang_so_bai_THU_THAP():
    van = SCRIPT.read_text(encoding="utf-8")
    mong_tb = int(re.search(r"^MONG_PYTEST_TOAN_BO=(\d+)$", van, re.M).group(1))
    mong_web = int(re.search(r"^MONG_PYTEST_WEB=(\d+)$", van, re.M).group(1))
    # đo CÂY bài, ⛔ đo cấu hình phiên của người gọi (`--lf` · plugin bỏ chọn)
    env = {k: v for k, v in os.environ.items() if k not in ("PYTEST_ADDOPTS", "PYTEST_PLUGINS")}
    kq = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-p", "no:cacheprovider"],
                        cwd=GOC, env=env, capture_output=True, text=True, timeout=300)
    assert kq.returncode == 0, kq.stdout[-1500:]
    nid = [d for d in kq.stdout.splitlines() if d.startswith("tests/") and "::" in d]
    tong = re.findall(r"^(\d+) tests? collected", kq.stdout, re.M)
    assert tong == [str(len(nid))], (tong, len(nid))                # hai cách đếm khớp nhau
    tep = {d.split("::")[0] for d in nid}
    assert len(tep) > 100, len(tep)                                 # mẫu số (Đ3)
    web = [d for d in nid if d.startswith("tests/web/")]
    assert (mong_tb, mong_web) == (len(nid), len(web)), (
        f"MONG_PYTEST_TOAN_BO = {mong_tb} · MONG_PYTEST_WEB = {mong_web} ≠ thu thập "
        f"{len(nid)} ({len(tep)} tệp) · tests/web {len(web)}")
