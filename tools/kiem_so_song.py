# -*- coding: utf-8 -*-
"""Cong chung #13 — MOT con so do duoc chi duoc phep co MOT nguon.

    python tools/kiem_so_song.py [--tai-lieu <duong/dan/den/ITL>]

★ Vi sao co file nay, va vi sao no o repo `FLS` chu khong o bo tai lieu.
Cong tai lieu (`_tools/kiem_tai_lieu.py`) chi doc **giay**: no khong chay duoc
`pytest`, khong mo duoc kho, khong biet `git` dang o commit nao. Nen no khong
the biet con so trong tai lieu con dung hay khong. Con o day thi biet — day la
noi DO duoc. ⇒ phep so noi tai lieu voi may phai dat o day.

⛔ **Lo da xay ra HAI lan, va lan thu hai chi cach lan dau MOT NGAY.**
  · 27/08: `08_MIGRATION_ROADMAP` buoc 4 lac hau **9 con so cung luc**; ban ve
    kien truc lac hau 4 con so. ⇒ dat ra **cong chung #13** tren giay:
    *"mot con so do duoc chep sang >=2 file thi phai co MOT phep so noi chung"*.
  · 28/08: do lai — **10 con so lech tren 3 file**, gom ca hai cho vua sua hom
    truoc. Bang tien do trong `06_DASHBOARD` con **tu mau thuan voi chinh no**:
    cong 9 dong module ra `6.255` trong khi dong TONG cua no ghi `6.328`.
  ⇒ Cong chung #13 co **loi van** tu 27/08 nhung ⛔ **khong co may** (`GAP-DOC-04`).
    Mot cong chi ton tai bang loi van la mot cong chua ton tai. Day la may.

⛔ Luat cua cong nay (cong chung #7 — cong phai chung minh no DO gi):
  ⓐ moi mau phai khop **DUNG MOT LAN** trong file. Khop **0** lan la DO
    *(mau vo, hoac cau van doi — ⛔ khong duoc phep xanh vi "khong thay loi")*;
    khop **>=2** lan cung la DO *(khong biet dang so voi cho nao)*.
  ⓑ do khong duoc thi DO, ⛔ khong bo qua: thieu kho, thieu `git`, thieu file
    tai lieu deu la khong dat.
  ⓒ cong nay CHI canh **so SONG** *(trang thai hom nay)*. ⛔ No khong canh so
    trong **changelog / dong duong-dan-chung** — o do so cu la **dung**, vi do
    la bien ban. Phan biet duoc hai thu ay la viec cua nguoi khai mau o duoi.
"""
from __future__ import annotations

import argparse
import dataclasses
import json
import pathlib
import re
import subprocess
import sys
import zoneinfo

GOC = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))
# 2026-09-03: bo tai lieu ITL da CHUYEN VAO repo nay (`docs/ITL/`). Truoc do no
# song o repo FIN-ERP canh ben, nen cong phai voi qua mot duong dan tuong doi
# `../FIN-ERP/...` — chi dung khi hai repo tinh co nam canh nhau tren cung mot
# may. Nay tai lieu va cong o CUNG repo ⇒ duong dan chac chan, CI doc duoc.
TAI_LIEU_MAC_DINH = GOC / "docs" / "ITL"

DASH = "01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md"
ROADMAP = "01_Orchestrator/08_MIGRATION_ROADMAP.md"
BANVE = "02_BA/Artifacts/Ban-ve-Kien-truc-TOBE.html"
MASTER = "00_MASTER_INDEX.md"


@dataclasses.dataclass(frozen=True)
class Muc:
    """Mot phep so: `mau` khop dung mot lan trong `file`, cac nhom = `gia`."""

    ten: str
    file: str
    mau: str
    gia: tuple[str, ...]


def vn(n: int) -> str:
    """Dinh dang so kieu tai lieu: dau cham ngan hang nghin."""
    return f"{n:,}".replace(",", ".")


# ─────────────────────────────────────────────────────────── do tu MAY
def _chay(*lenh: str) -> str:
    r = subprocess.run(lenh, cwd=GOC, capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    if r.returncode != 0:
        raise SystemExit(f"⛔ khong do duoc: `{' '.join(lenh)}` "
                         f"tra ma {r.returncode}\n{r.stderr[-400:]}")
    return r.stdout


def do_may() -> dict[str, str]:
    """Do TAT CA con so song. Do khong duoc thi nem loi — ⛔ khong doan."""
    from fls.db.kho import dsn_that                       # noqa: PLC0415
    from fls.db.schema import TABLES                      # noqa: PLC0415

    import psycopg                                        # noqa: PLC0415

    td = json.loads(_chay(sys.executable, "tools/tien_do.py", "--json"))
    lint = _chay(str(GOC / ".venv" / "Scripts" / "lint-imports.exe"))
    m_lint = re.search(r"Contracts:\s*(\d+)\s+kept,\s*(\d+)\s+broken", lint)
    if not m_lint:
        raise SystemExit("⛔ khong doc duoc ket qua `lint-imports`")

    # ⛔ Kho khong mo duoc thi DO ro rang, ⛔ khong de mot vet do ky thuat
    # tho — mot cong noi khong ai hieu la mot cong se bi go.
    try:
        noi = psycopg.connect(dsn_that(), connect_timeout=5)
    except psycopg.Error as e:
        raise SystemExit(
            f"⛔ khong do duoc: khong mo duoc kho THAT ({type(e).__name__}). "
            "Cong nay ⛔ khong duoc phep xanh khi thieu so do.") from None
    with noi as c:
        gio = c.execute(
            "select (select started_at from fls_run order by started_at desc"
            " limit 1), (select max(read_at) from fls_pm_line)").fetchone()
        def dem(sql: str) -> int:
            return int(c.execute(sql).fetchone()[0])

        kho = {
            "so_dong": dem("select count(*) from fls_itl"),
            # ⚠ `fls_moi_noi` — moi noi CON HIEU LUC. Dem tren `fls_pm_link`
            # thi tu 2026-08-28 con so se cong ca cac moi noi DA BO
            # (`QĐ-ITL-69`), va tai lieu se noi mot con so ⛔ khong ai dung.
            "moi_noi": dem("select count(*) from fls_moi_noi"),
            "dong_lenh_noi": dem("select count(distinct pm_line_id) "
                                 "from fls_moi_noi"),
            "moi_noi_da_bo": dem("select count(*) from fls_pm_unlink"),
            "anh_chup": dem("select count(*) from fls_pm_line"),
            "phieu": dem("select count(distinct pm_slip_id) from fls_pm_line"),
            "loai": dem("select count(*) from fls_reject"),
        }

    # ⛔ Ghi DAU THOI DIEM, ⛔ KHONG ghi "tuoi". Tuoi la con so ĐỘNG (nhich
    # tung phut) nen chep vao tai lieu la sai ngay hom sau; dau thoi diem la
    # mot SU KIEN, no ⛔ khong gia di. Nguoi doc tu tru ra tuoi.
    if not gio or not gio[0] or not gio[1]:
        raise SystemExit("⛔ khong do duoc: kho ⛔ khong co dau thoi diem cua "
                         "lan nap / anh chup — cong ⛔ khong duoc phep xanh")
    vn_tz = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")

    ra = {
        "dau_so": gio[0].astimezone(vn_tz).strftime("%d/%m %H:%M"),
        "dau_anh": gio[1].astimezone(vn_tz).strftime("%d/%m %H:%M"),
        "bang_view": str(len(TABLES)),
        "test_tong": str(td["tong_test"]),
        "test_module": str(sum(h["test"] for h in td["module"])),
        "test_ngoai": str(td["tong_test"] - sum(h["test"] for h in td["module"])),
        "dong_tong": vn(sum(h["dong"] for h in td["module"])),
        "tien_do": f"{td['tien_do_pct']:.0f}",
        "tong_trong_so": str(td["tong_trong_so"]),
        "gop_tong": f"{td['tien_do_pct']:.2f}".replace(".", ","),
        "lint_kept": m_lint.group(1),
        "lint_broken": m_lint.group(2),
        # ⛔⛔ Commit cua LAN SUA `fls/` GAN NHAT, ⛔ KHONG phai `HEAD`.
        #
        # Truoc 03/09 bo tai lieu song o kho FIN-ERP, nen `HEAD` cua kho nay
        # dung yen trong luc toi sua tai lieu ⇒ ghi `HEAD` vao tai lieu la mot
        # viec lam duoc. Sau khi CHUYEN tai lieu vao chinh kho nay, cach do
        # thanh mot DIEM BAT DONG ⛔ KHONG BAO GIO CHAM TOI: moi commit sua con
        # so lai lam con so do sai.
        #
        # ⇒ Doi phep do cho khop dung dieu tai lieu NOI: *"so trong ban ve nay
        #   DO tren commit X"*. Cac con so deu la ve `fls/`, nen moc dung la
        #   lan `fls/` doi gan nhat — va mot commit chi-sua-tai-lieu ⛔ khong
        #   lam no doi. ⛔ Khong noi long phep kiem, ma sua cho no do DUNG THU
        #   no dang khai.
        "commit": _chay("git", "log", "-1", "--format=%h",
                        "--abbrev=7", "--", "fls/").strip(),
        **{k: vn(v) for k, v in kho.items()},
    }
    for h in td["module"]:
        ra[f"dong_{h['ma']}"] = vn(h["dong"])
        ra[f"test_{h['ma']}"] = str(h["test"])
    return ra


def dem_bo_tai_lieu(tai_lieu: pathlib.Path) -> dict[str, str]:
    """Dem chinh BO TAI LIEU: bao nhieu file `.md`, bao nhieu hien vat.

    ⛔⛔ **Vi sao con so nay phai do, ⛔ khong chep tay.** Ngay 28/08 khoi §8 cua
    `00_MASTER_INDEX` bi bat ghi *"38 file .md + 21 hien vat"* trong khi that
    la **61** va **22** — va no lac hau **im lang** vi khoi ay ⛔ khong nam
    trong 48 cho cong da khai (`GAP-DOC-05`). Mot con so **dem duoc** ma de
    nguoi chep tay thi no se lech, chi la som hay muon.
    """
    if not tai_lieu.is_dir():
        raise SystemExit(f"⛔ khong do duoc: ⛔ khong thay kho tai lieu {tai_lieu}")
    md = sum(1 for _ in tai_lieu.rglob("*.md"))
    hv = tai_lieu / "02_BA" / "Artifacts"
    return {"so_md": str(md),
            "so_hien_vat": str(sum(1 for _ in hv.iterdir()) if hv.is_dir() else 0)}


def doc_version(tai_lieu: pathlib.Path, duong: str) -> str:
    """Version o HEADER cua chinh file do — nguon duy nhat cua con so ay."""
    f = tai_lieu / duong
    if not f.exists():
        raise SystemExit(f"⛔ thieu file tai lieu: {f}")
    m = re.search(r"\*\*Version:\*\*\s*v?([0-9]+\.[0-9]+)",
                  f.read_text(encoding="utf-8", errors="replace"))
    if not m:
        raise SystemExit(f"⛔ khong tim thay version o header: {duong}")
    return m.group(1)


# ─────────────────────────────────────────────────────────── khai cac phep so
def khai(may: dict[str, str], tai_lieu: pathlib.Path) -> list[Muc]:
    v = lambda d: doc_version(tai_lieu, d)                             # noqa: E731
    bo = dem_bo_tai_lieu(tai_lieu)
    m: list[Muc] = [
        # ── 06_DASHBOARD §1 — dong "Cong"
        # ⛔ Mau dau tien toi viet la ``lint-imports` **N kept**`, va no khop
        # **4 lan** trong file — cong tra ve "⛔ khong do duoc" chu ⛔ khong
        # xanh, dung luat ⓐ. Nay neo vao dau dong "Cong" cua §1.
        Muc("cong · lint-imports", DASH,
            r"\| Cổng \| `lint-imports` \*\*(\d+) kept (\d+) broken\*\*",
            (may["lint_kept"], may["lint_broken"])),
        # ⛔ Mau cu (khong neo) khop **3 lan** sau khi hai dong su kien 28/08
        # cung nhac "khop 15 bang/view" — chung la BIEN BAN, so o do la dung
        # (luat ⓒ). Neo vao dong "Cong" cua §1, la cho duy nhat mang so SONG.
        Muc("cong · pg_verify bang/view", DASH,
            r"\| Cổng \|[^|]*?`pg_verify` \*\*khớp (\d+) bảng/view\*\*",
            (may["bang_view"],)),
        # ── 06_DASHBOARD §1 — dong "Kho that"
        Muc("kho · dong so", DASH,
            r"\*\*([\d.]+) dòng sổ\*\* \*\(bản sao nạp [0-9/: ]+\)\*"
            r" · \*\*[\d.]+ mối nối PM\*\*",
            (may["so_dong"],)),
        Muc("kho · moi noi PM", DASH,
            r"\*\*([\d.]+) mối nối PM\*\* \*\(([\d.]+) dòng lệnh\)\*",
            (may["moi_noi"], may["dong_lenh_noi"])),
        Muc("kho · anh chup dong lenh", DASH,
            r"ảnh chụp \*\*([\d.]+) dòng lệnh · ([\d.]+) phiếu\*\*",
            (may["anh_chup"], may["phieu"])),
        Muc("kho · DẤU THỜI ĐIỂM bản sao sổ", DASH,
            r"\*\*[\d.]+ dòng sổ\*\* \*\(bản sao nạp ([0-9/: ]+)\)\*",
            (may["dau_so"],)),
        Muc("kho · DẤU THỜI ĐIỂM ảnh chụp", DASH,
            r"ảnh chụp \*\*[\d.]+ dòng lệnh · [\d.]+ phiếu\*\* "
            r"\*\(`fls_pm_line`, đọc ([0-9/: ]+)\)\*",
            (may["dau_anh"],)),
        Muc("master · DẤU THỜI ĐIỂM", MASTER,
            r"bản sao nạp ([0-9/: ]+) · ảnh chụp đọc ([0-9/: ]+)\)\*",
            (may["dau_so"], may["dau_anh"])),
        Muc("bản vẽ · DẤU THỜI ĐIỂM", BANVE,
            r"bản sao nạp <strong>([0-9/: ]+)</strong>", (may["dau_so"],)),
        Muc("kho · dong loai", DASH,
            r"([\d.]+) dòng `fls_reject`", (may["loai"],)),
        # ── 06_DASHBOARD §1 — dong "Test · code" + "Nhanh"
        Muc("test · tong va trong module", DASH,
            r"\*\*(\d+) test\*\* \*\((\d+) trong 9 module \+ (\d+) ngoài\)\* "
            r"trên \*\*([\d.]+) dòng\*\*",
            (may["test_tong"], may["test_module"], may["test_ngoai"],
             may["dong_tong"])),
        Muc("nhanh · commit", DASH,
            r"`feat/p2-oracle-parity` — `([0-9a-f]{7})`", (may["commit"],)),
        # ── ban ve kien truc: khoi "Dau thoi diem"
        Muc("ban ve · commit + phep thu", BANVE,
            r"commit <code>([0-9a-f]{7})</code>\. <strong>(\d+) phép thử xanh",
            (may["commit"], may["test_tong"])),
        # ── 08_MIGRATION_ROADMAP buoc 4: version cua 3 file DEV
        Muc("roadmap · DEV-03 version", ROADMAP,
            r"`DEV-03` roadmap 7 pha \*\*v([0-9.]+)\*\*",
            (v("03_Dev/03_IMPLEMENTATION_PLAN.md"),)),
        Muc("roadmap · DEV-04 version", ROADMAP,
            r"`DEV-04` schema \*\*v([0-9.]+)\*\*",
            (v("03_Dev/04_DB_IMPLEMENTATION.md"),)),
        Muc("roadmap · DEV-10 version", ROADMAP,
            r"`DEV-10` spec adapter ghép \*\*v([0-9.]+)\*\*",
            (v("03_Dev/10_PM_JOIN_ADAPTER_SPEC.md"),)),
        Muc("roadmap · DEV-11 version", ROADMAP,
            r"`DEV-11` spec đọc thước chuẩn \*\*v([0-9.]+)\*\*",
            (v("03_Dev/11_ORACLE_READ_SPEC.md"),)),
        # ── 08_MIGRATION_ROADMAP buoc 4: con so song (cung con so voi §1
        # cua dashboard — dung cho cong #13 sinh ra de canh)
        Muc("roadmap · phép thử + dòng", ROADMAP,
            r"\*\*(\d+) phép thử\*\*, \*\*([\d.]+) dòng\*\* `fls/`",
            (may["test_tong"], may["dong_tong"])),
        Muc("roadmap · lint-imports", ROADMAP,
            r"`lint-imports` \*\*(\d+) kept (\d+) broken\*\*",
            (may["lint_kept"], may["lint_broken"])),
        Muc("roadmap · dòng sổ", ROADMAP,
            r"Kho PostgreSQL có \*\*([\d.]+) dòng sổ thật\*\*",
            (may["so_dong"],)),
        Muc("roadmap · mối nối", ROADMAP,
            r"\*\*([\d.]+) mối nối lệnh chi\*\*", (may["moi_noi"],)),
        # ⛔ Khong neo `fls_pm_line` thi mau nay khop **2 lan** — lan thu hai
        # nam trong muc changelog `v0.7`, noi con so cu la DUNG (luat ⓒ).
        Muc("roadmap · DẤU THỜI ĐIỂM", ROADMAP,
            r"bản sao nạp ([0-9/: ]+) · ảnh chụp đọc ([0-9/: ]+)\)\*",
            (may["dau_so"], may["dau_anh"])),
        Muc("roadmap · ảnh chụp", ROADMAP,
            r"\*\*ảnh chụp ([\d.]+) dòng lệnh\*\* trong `fls_pm_line`",
            (may["anh_chup"],)),
        # ── dong TONG cua bang tien do: 4 o nay ⛔ khong duoc suy tu 9 dong
        # tren no bang mat. Bang tung TU MAU THUAN — 9 dong cong ra 6.255
        # trong khi dong TONG ghi 6.328 — va no im lang suot mot ngay.
        Muc("bảng tiến độ · dòng TỔNG", DASH,
            r"\| \*\*TỔNG\*\* \| \| \*\*([\d.]+)\*\* \| \*\*(\d+)\*\* \| \|"
            r" \*\*(\d+)\*\* \| \*\*([\d,]+)\*\* \|",
            (may["dong_tong"], may["test_module"], may["tong_trong_so"],
             may["gop_tong"])),
        Muc("§1 · tiến độ %", DASH,
            r"\*\*Tiến độ theo khối lượng việc\*\* \| \*\*(\d+)%\*\*",
            (may["tien_do"],)),
        # ── 00_MASTER_INDEX §10: khoi "da sang CODE THAT". ⛔ Day la file
        # ma dot 27/08 vua viet lai §10 vi no "noi nguoc su that" — va 28/08
        # do lai thi chinh khoi vua viet ay lac hau 4 con so.
        Muc("master · phép thử + dòng", MASTER,
            r"\*\*(\d+) phép thử\*\*, \*\*([\d.]+) dòng\*\* `fls/`",
            (may["test_tong"], may["dong_tong"])),
        Muc("master · kho", MASTER,
            r"\*\*([\d.]+) dòng sổ thật\*\* \+ \*\*([\d.]+) mối nối lệnh chi\*\*"
            r" \+ \*\*ảnh chụp ([\d.]+) dòng lệnh\*\*",
            (may["so_dong"], may["moi_noi"], may["anh_chup"])),
        Muc("master · tiến độ %", MASTER,
            r"Tiến độ theo khối lượng việc \*\*(\d+)%\*\*", (may["tien_do"],)),
        # ── ban ve kien truc: 2 the so + 8 thanh module
        Muc("bản vẽ · tiến độ %", BANVE,
            r'<span class="k">Tiến độ theo khối lượng việc</span>\s*'
            r'<p class="v num">(\d+)%</p>', (may["tien_do"],)),
        Muc("bản vẽ · phép thử + dòng", BANVE,
            r'<span class="k">Phép thử tự động</span>\s*<p class="v num">(\d+)'
            r'</p>\s*<p>Trên <strong>([\d.]+) dòng</strong>',
            (may["test_tong"], may["dong_tong"])),
        # ── ⭐ 00_MASTER_INDEX §8: chinh BO TAI LIEU tu dem no
        #
        # ⛔⛔ Them 2026-08-28 sau khi §8 bi bat ghi "38 file .md + 21 hien vat"
        # trong khi that la 61 va 22 — mot con so DEM DUOC ma de nguoi chep tay.
        Muc("master · §8 số file + hiện vật", MASTER,
            r"## 8\. Cấu trúc bộ \(\*\*(\d+) file `\.md`\*\* \+ "
            r"\*\*(\d+) hiện vật\*\*\)",
            (bo["so_md"], bo["so_hien_vat"])),
        Muc("master · §8 test của repo FLS", MASTER,
            r"phép thử sống trong repo `FLS` \*\(\*\*(\d+) test\*\*\)",
            (may["test_tong"],)),
        # ⭐ Version cua tung file MA §8 CHEP LAI. Doc tu header cua chinh file
        #   do, nen mot lan bump version se lam cong nay DO neu §8 quen theo.
        Muc("master · §8 version DEV-03", MASTER,
            r"`03` \*\*v([0-9.]+)\*\* · `04`",
            (v("03_Dev/03_IMPLEMENTATION_PLAN.md"),)),
        Muc("master · §8 version DEV-04", MASTER,
            r"`04` \*\*v([0-9.]+)\*\* · `09` v1\.0",
            (v("03_Dev/04_DB_IMPLEMENTATION.md"),)),
        Muc("master · §8 version DEV-12", MASTER,
            r"`12` \*\*v([0-9.]+)\*\* \*\(kế hoạch chi tiết 4 màn",
            (v("03_Dev/12_P6_WEB_PLAN.md"),)),
        # ⭐⭐ Them 2026-09-04: **ba tep BA truoc day ⛔ KHONG ai canh.**
        #   Cong nay von chi soi `BA-03/06/07/09`. Ngay 04/09 toi bump
        #   `05`/`10`/`11` va **⛔ khong cai gi keu** — mot phien ban chep tay
        #   ma ⛔ khong co phep so thi no gia di **trong im lang**, dung cai
        #   benh ma ca bo tai lieu nay dung ra de chua.
        Muc("master · §8 version BA-04", MASTER,
            r"`04` \*\*v([0-9.]+)\*\* \*\(3 vai người",
            (v("02_BA/04_ROLE_PERMISSION_MATRIX.md"),)),
        Muc("master · §8 version BA-08", MASTER,
            r"`08` \*\*v([0-9.]+)\*\* \*\(23 NFR",
            (v("02_BA/08_NFR.md"),)),
        Muc("master · §8 version BA-02", MASTER,
            r"`02` \*\*v([0-9.]+)\*\* \*\(bỏ",
            (v("02_BA/02_PROCESS_FLOW.md"),)),
        # ⭐ Neo lai 2026-09-07 (lan thu HAI cung mot lop loi — sau ORCH-08):
        # neo cu bam vao GHI CHU cua ban khai (`*(khuôn KỲ …)*`), mot chuoi
        # doi moi lan `BA-05` duoc ghi chu them ⇒ no VO khi v0.18 doi ghi chu.
        # ⇒ Bam vao O DAU HANG (`02_BA/`) — thu noi ro dang do version cua KIT
        # nao, va la thu ⛔ khong doi theo noi dung ghi chu.
        Muc("master · §8 version BA-05", MASTER,
            r"\| `02_BA/`.*?`05` \*\*v([0-9.]+)\*\*",
            (v("02_BA/05_DATA_DICTIONARY_ERD.md"),)),
        # ⚠⚠ Neo hai phep nay **⛔ khong** duoc bam vao ma bat-dau *(`DT-I09`,
        #    `INV-I17`)*: moi lan bo tai lieu them mot bat bien hay mot bang
        #    quyet dinh thi chu trong ngoac doi, va phep do **mat neo** ⇒ cong
        #    bao *"khop 0 lan"*. Da xay ra dung the 04/09. ⇒ Neo vao `` `10` ``
        #    / `` `11` `` cong mot dau `(` — thu ⛔ khong doi theo noi dung.
        Muc("master · §8 version BA-10", MASTER,
            r"`10` \*\*v([0-9.]+)\*\* \*\(",
            (v("02_BA/10_DECISION_TABLE.md"),)),
        Muc("master · §8 version BA-11", MASTER,
            r"`11` \*\*v([0-9.]+)\*\* \*\(",
            (v("02_BA/11_INVARIANTS.md"),)),
        Muc("master · §8 version BA-06", MASTER,
            r"`06` \*\*v([0-9.]+)\*\* \*\(\+§3c",
            (v("02_BA/06_SCREEN_SPEC.md"),)),
        Muc("master · §8 version BA-07", MASTER,
            # ⚠ Neo cu bam vao *"... · `09` v0.4 ·"* — mot cho ⛔ khong
            #   noi len no dang do CAI GI, va no vo ngay khi `07` duoc
            #   ghi chu them. Neo lai vao **chinh ma tep** nhu cac phep
            #   so khac.
            r"`07` \*\*v([0-9.]+)\*\* \*\(\+2 mã lỗi",
            (v("02_BA/07_API_CONTRACT.md"),)),
        Muc("master · §8 version ORCH-07", MASTER,
            r"`07` \*\*v([0-9.]+)\*\* \*\(6 luật chống sổ già",
            (v("01_Orchestrator/07_CHANGE_CONTROL.md"),)),
        # ⭐ Neo lai 2026-09-07: neo cu bam vao duoi cau ghi chu cua `07`
        # ("da thanh lenh chay duoc)*") — mot cho ⛔ KHONG noi len no dang do
        # CAI GI, nen no VO ngay khi `07` duoc ghi chu them `CR#10`. Day la
        # DUNG cai loi da ghi trong commit 93b7b0f cho phep so `BA-07`, va no
        # lap lai. ⇒ Neo vao O DAU HANG (`01_Orchestrator/`) — thu noi ro
        # phep so nay dang doc version cua kit NAO.
        Muc("master · §8 version ORCH-08", MASTER,
            r"\| `01_Orchestrator/`.*?`08` \*\*v([0-9.]+)\*\*",
            (v("01_Orchestrator/08_MIGRATION_ROADMAP.md"),)),
        # ── ban ve kien truc: the "Dong so · moi noi lenh chi"
        Muc("bản vẽ · dòng sổ + mối nối", BANVE,
            r'<span class="k">Dòng sổ · mối nối lệnh chi</span>\s*'
            r'<p class="v num">([\d.]+) · ([\d.]+)</p>',
            (may["so_dong"], may["moi_noi"])),
    ]
    # ── bang tien do 9 dong: `dong` va `test` cua tung module.
    # ⛔ Day la cho da lech that: dong `db` con in `1.127` trong khi may do
    # `1.200`, va bang khi ay **tu mau thuan** — 9 dong cong ra 6.255 nhung
    # dong TONG cua no ghi 6.328.
    ten_bang = {
        "db": "khuôn dữ liệu", "contract": "hợp đồng 14 trường",
        "canon": "khuôn 36 cột", "ledger": "lớp ghi sổ",
        "repo": "cửa vào kho", "oracle": "thước chuẩn",
        "adapters": "6 bộ nạp", "api": "cửa vào ra", "web": "4 màn hình",
    }
    # ⛔ 8 thanh trong BAN VE cung chep so test cua tung module — va thanh
    # `api` da lac hau (`122` trong khi may do `133`). `web` ⛔ khong co so
    # (`chua mo`) nen ⛔ khong co gi de so.
    for ma in ("db", "contract", "canon", "ledger", "oracle", "repo",
               "adapters", "api"):
        m.append(Muc(f"bản vẽ · thanh {ma}", BANVE,
                     rf"<small>{ma} · (\d+)", (may[f"test_{ma}"],)))
    for ma, nhan in ten_bang.items():
        m.append(Muc(
            f"bảng tiến độ · {ma}", DASH,
            rf"\| `{ma}` {re.escape(nhan)} \| [^|]+ \| ([\d.]+) \| (\d+) \|",
            (may[f"dong_{ma}"], may[f"test_{ma}"])))

    # ⭐⭐ CONG TU DEM CHINH NO — them 2026-08-28.
    #
    # ⛔⛔ Con so "cong so song N/N" da MUC HAI LAN trong mot ngay: 43 -> 48 ->
    # 57, va moi lan phai sua tay o **ba** cho (`00_MASTER_INDEX` §10 ·
    # `06_DASHBOARD` §1 · ban ve kien truc). Mot con so noi ve **chinh cai cong**
    # thi cong phai tu canh duoc — khong thi no la cho DUY NHAT trong ca bo tai
    # lieu duoc mien khoi luat cua chinh no.
    #
    # ⚠ `len(m) + 3` vi ba muc nay duoc them ngay sau day va chung cung TINH.
    tong = str(len(m) + 3)
    m += [
        Muc("master · số phép so của cổng", MASTER,
            r"cổng số sống (\d+)/\d+", (tong,)),
        Muc("dashboard · số phép so của cổng", DASH,
            r"`tools/kiem_so_song\.py` \*\*ĐẠT (\d+)/\d+\*\*", (tong,)),
        Muc("bản vẽ · số phép so của cổng", BANVE,
            r"cổng số sống (\d+)/\d+", (tong,)),
    ]
    return m


# ─────────────────────────────────────────────────────────── phep so (thuan)
def kiem_mot(noi_dung: str, m: Muc) -> list[str]:
    """So MOT muc. Tra ve danh sach loi — rong la dat.

    ⛔ Khop 0 lan hay >=2 lan deu la DO: mot cong khong biet no dang so voi
    cho nao thi no ⛔ khong do duoc gi (cong chung #7).
    """
    khop = list(re.finditer(m.mau, noi_dung))
    if len(khop) != 1:
        return [f"{m.ten}: mau khop {len(khop)} lan (phai DUNG 1) — "
                f"⛔ khong do duoc, ⛔ khong phai 'khong thay loi'"]
    g = khop[0].groups()
    if len(g) != len(m.gia):
        return [f"{m.ten}: mau co {len(g)} nhom nhung khai {len(m.gia)} gia tri"]
    loi = []
    for i, (tai_lieu, may) in enumerate(zip(g, m.gia), 1):
        if tai_lieu != may:
            loi.append(f"{m.ten} (nhom {i}): tài liệu ghi `{tai_lieu}` · "
                       f"MÁY đo `{may}` ⛔ LỆCH")
    return loi


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(add_help=True)
    p.add_argument("--tai-lieu", default=str(TAI_LIEU_MAC_DINH))
    ns = p.parse_args(argv)
    tai_lieu = pathlib.Path(ns.tai_lieu)
    if not tai_lieu.is_dir():
        raise SystemExit(f"⛔ khong thay bo tai lieu: {tai_lieu}")

    may = do_may()
    muc = khai(may, tai_lieu)

    print(f"kho tai lieu : {tai_lieu}")
    print(f"may do       : {len(may)} con so · "
          f"{len(muc)} phep so tren {len({m.file for m in muc})} file\n")

    cache: dict[str, str] = {}
    tong: list[str] = []
    for m in muc:
        if m.file not in cache:
            f = tai_lieu / m.file
            if not f.exists():
                tong.append(f"{m.ten}: ⛔ thieu file {m.file}")
                cache[m.file] = ""
                continue
            cache[m.file] = f.read_text(encoding="utf-8", errors="replace")
        loi = kiem_mot(cache[m.file], m)
        print(f"{'OK ' if not loi else '⛔ '}{m.ten}")
        for x in loi:
            print(f"     - {x}")
        tong += loi

    print()
    if tong:
        print(f"⛔ CONG SO SONG KHONG DAT — {len(tong)} lech/khong-do-duoc")
        return 1
    print(f"✅ cong so song DAT — {len(muc)} phep so, moi phep khop DUNG mot "
          f"lan va khop dung con so MAY do (commit `{may['commit']}`)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
