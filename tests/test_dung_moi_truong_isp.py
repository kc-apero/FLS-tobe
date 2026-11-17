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


def test_S0_R2_02_moi_ky_tu_la_hoac_bi_chot_tu_choi_hoac_bi_che_tron(tmp_path):
    """Mỗi ký tự lạ, ở mật khẩu RỒI ở tên user: ⛔ một mảnh mật khẩu nào ra stdout/stderr.

    Mật khẩu là `Kq7<c>Wx9` — hai mảnh hai bên ký tự lạ, để thấy cả lỗi "che nửa đầu, lộ
    đuôi" (`@` thô) lẫn "lộ nửa đầu" (xuống dòng: bản cũ che theo DÒNG). Ca nào QUA chốt
    (exit 1 — môi trường giả vắng) thì dòng tiêu đề + hai dòng `export` phải che; ca nào bị
    từ chối (exit 2) thì câu từ chối phải che.
    """
    def mot(ca: tuple[str, str]) -> tuple[str, str, int, list[str]]:
        noi, c = ca
        dsn = (f"postgresql://fls:Kq7{c}Wx9@localhost:5433/fls_thu" if noi == "mật khẩu"
               else f"postgresql://f{c}u:Kq7Wx9@localhost:5433/fls_thu")
        kq = _chay(["--chi-kiem"], {"PG_DSN": dsn}, tmp_path)
        ra = kq.stdout + kq.stderr
        return noi, c, kq.returncode, [d for d in ra.splitlines() if "Kq7" in d or "Wx9" in d]

    ca = [(noi, c) for noi in ("mật khẩu", "tên user") for c in _KY_TU_LA]
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as tp:
        kq = list(tp.map(mot, ca))
    assert len(kq) == 2 * len(_KY_TU_LA) == 76          # mẫu số (Đ3): 33 + 5 ký tự × 2 nơi
    lo = [(noi, repr(c), ma, dong) for noi, c, ma, dong in kq if dong]
    assert not lo, lo
    la_ma = [(noi, repr(c), ma) for noi, c, ma, _ in kq if ma not in (1, 2)]
    assert not la_ma, la_ma
    # khoảng trắng nằm NGOÀI lớp ký tự (libpq vốn từ chối) ⇒ chốt từ chối, ⛔ cho qua
    qua = [(noi, repr(c)) for noi, c, ma, _ in kq if c in " \t\n\r" and ma != 2]
    assert not qua, qua


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

    ⭐ Q8 = A: bước thêm bài nâng sàn + bài ghim này trong CÙNG commit — +33 CG1 (`WO-101`,
    `tests/api/test_isp_gates_hd1.py`) ⇒ 2.493; +3 FG (`WO-116`, ISP 3.1.2 · Step 9,
    `tests/web/test_isp_f03_hd.py` — FG-F1·F2·F3) ⇒ 2.496 · `tests/web` 664 → 667. Lo gốc giữ
    nguyên: số khai MỘT chỗ, ghim đúng số.
    """
    van = SCRIPT.read_text(encoding="utf-8")
    assert re.findall(r"^MONG_PYTEST_TOAN_BO=(\d+)$", van, re.M) == ["2496"]
    assert re.findall(r"^MONG_PYTEST_WEB=(\d+)$", van, re.M) == ["667"]
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
