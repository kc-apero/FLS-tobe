"""Do tien do 9 module — sinh so cho BAN VE 12 (`Ban-ve-Kien-truc-TOBE.html`).

★ Vi sao co file nay. Bang tien do go tay se gia di trong im lang — dung benh ma
ca du an nay dang chua. Nen so trong bang phai SINH RA duoc, va lech thi thay ngay.

Chay:  python tools/tien_do.py            (bang doc cho nguoi)
       python tools/tien_do.py --json     (de dan vao cong cu khac)

`xong` la % TU KHAI theo DoD (`03_IMPLEMENTATION_PLAN` §5) — day la phan xet
doan cua nguoi, ⛔ khong phai so do duoc. Con `test` va `dong` thi do that.
`trong_so` = phan cong viec uoc luong cua module trong ca he, cong lai = 100.
"""

from __future__ import annotations

import ast
import json
import re
import subprocess
import sys

# 2026-09-03: console Windows mac dinh cp1252 KHONG ma hoa noi tieng Viet co dau.
# Khong ep UTF-8 thi `tien_do.py --json` chet o dong in => `kiem_so_song.py` bao
# "khong do duoc" va CONG SO SONG BI MU. Do la lan thu BA cung mot loi trong ba
# repo (`check_plan_docs.py` @FPA-T4, `_tools/kiem_tai_lieu.py` @FIN-ERP, day) =>
# no la mot LOP loi, khong phai ba su co roi rac: bat ky cong nao IN ra tieng Viet
# tren Windows deu can dong nay. Cong bao sai / cong bi mu deu te hon khong co cong.
try:                                    # py>=3.7
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:                        # pragma: no cover
    pass
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]

# (ma, ten, trong_so, xong_pct, pha)
#
# ⚠ `xong_pct` la XET DOAN CUA NGUOI. Nen moi lan doi no phai co LY DO viet ra
# ngay day — khong thi no thanh mot num nhich len theo cam giac, va bang tien do
# lai gia di theo mot kieu khac.
#
# Nhat ky doi `xong_pct`:
#   2026-08-27  repo 78 -> 85   +`kho_sach.py` (cong kho sach) +`chen_moi_noi`
#                               +cong Σ chan truoc khi ghi. CON LAI: duong ghi
#                               cho P5 (adjust/reason/defer/match).
#   2026-08-27  adapters 40 -> 45  hinh `B` DAU DUOC (bang noi `fls_pm_link`) =>
#                               ca 3 hinh ghep duoc deu dau. CON LAI: 4 bo nap
#                               C·D·E·F + 3 tang T0/T3/T4 (⛔ CHAN NGOAI: cho ke
#                               toan tra loi va cho P4·P6).
#   2026-08-27  api 0 -> 40     `P4` cua DOC xong: bang tuyen + the (fail-closed)
#                               + vo boc + 6 duong `/ledger` `/ledger/{id}`
#                               `/queue` `/queue/summary` `/journal` `/gates`,
#                               **chay that tren kho that qua HTTP**
#                               (`tools/verify_cua_that.py`).
#                               ⛔ CON LAI, va khai ro chu khong lam tron:
#                               ⓐ **6 duong doc cua `BA-07` §2 chua co**
#                                 (`/queue/coverage` `/weekly` `/sources`
#                                  `/mapping-master` `/le` `/queue/state`) —
#                                 phan lon cho bang nguon co du lieu;
#                               ⓑ nhom `/runs*` (§4);
#                               ⓒ **toan bo `P5`** (duong ghi).
#                               ⇒ 40 la "P4 theo dung pham vi plan da xong",
#                                 ⛔ khong phai "cua da xong".
#   2026-08-27  repo 85 -> 90   +`pham_vi.py` (pham vi doc, ⛔ khong mac dinh)
#                               +`doc_bao_cao.py` (5 cau doc + cong) + phep xep
#                               hang cho **co tham so** (chuyen tu khung xem).
#                               CON LAI: duong ghi cho `P5`.
#   2026-08-27  api 40 -> 75    `P5` cua GHI: 4 duong ghi + `/fields/{f}` (hoi
#                               nguon truoc khi go). `actor` den TU THE; but
#                               toan + nhat ky trong MOT giao dich; 409 khi khac
#                               nguon; dao but toan = them dong; ⛔ khong duong
#                               nao ghi vao `fls_itl`. Chay that ca vong ghi qua
#                               HTTP (`tools/verify_cua_ghi.py`).
#                               ⛔ CON LAI, khai ro: ⓐ `/match` + `/pm-candidates`
#                                 **CHAN** — `fps_pm_line` khong nam trong kho
#                                 `fls_*` (`GAP-API-04`) ⓑ 6 duong doc cua
#                                 `BA-07` §2 + nhom `/runs*` ⓒ chot ky/ky
#                                 (`GAP-PLAN-04`, chua co dac ta).
#   2026-08-27  repo 90 -> 95   +`ghi_tay.py` (CHO DUY NHAT ghi thao tac nguoi).
#                               CON LAI: duong ghi cho `/match`.
#   2026-08-27  api 75 -> 85    GHEP LENH mo duoc: `GET .../pm-candidates` +
#                               `POST .../match`. Day la doi duong tung bi
#                               **CHAN** (`GAP-API-04`) chu ⛔ khong phai chua
#                               lam — owner chot duong (a): luu ANH CHUP dong
#                               lenh vao kho (`fls_pm_line`, migration `0011`).
#                               Ghep tay = THEM `fls_pm_link` (hinh `T`) +
#                               `fls_queue_event` + but toan `hd`/`cdt1` suy tu
#                               dong lenh; so `fls_itl` ⛔ khong doi mot o.
#                               ⛔ CON LAI, khai ro chu khong lam tron len 90:
#                               ⓐ **6 duong doc** cua `BA-07` §2
#                                 (`/queue/coverage` `/weekly` `/sources`
#                                  `/mapping-master` `/le` `/queue/state`)
#                               ⓑ nhom `/runs*` (§4)
#                               ⓒ **chot ky / ky** — co may trang thai ma ⛔
#                                 khong co cua, va ⛔ chua co dac ta
#                                 (`GAP-PLAN-04`)
#                               ⓓ ⛔ **bo moi noi** de ghep lai (`GAP-JOIN-05`):
#                                 nay ghep sai thi ⛔ khong co duong nao sua.
#   2026-08-27  repo 95 -> 95   +`ghep_lenh` + `chen_dong_pm` + `ung_vien_pm`.
#                               ⛔ GIU 95, ⛔ khong tang: phan con thieu cua
#                               `repo` la **bo moi noi** (`GAP-JOIN-05`), va no
#                               VAN thieu sau dot nay.
#   ⛔ `db` GIU 100 du vua them khoa nhieu cot + `kho.py`: DoD cua no da dat tu
#      truoc, viec moi la mo rong — ⛔ khong co cho de "tang" nua.
#   2026-08-28  repo 95 -> 100  ⭐ **DUONG BO MOI NOI xong** (`GAP-JOIN-05`,
#                               `QĐ-ITL-69`, migration `0013`). Day la thu DUY
#                               NHAT con thieu cua `repo` tu 27/08 — hai dot
#                               truoc CO Y giu 95 vi no van thieu.
#                               Bo = THEM dong `fls_pm_unlink` + khung xem
#                               `fls_moi_noi`; ⛔ khong `DELETE`, ⛔ khong
#                               `UPDATE`. Bo CA CHUM (⛔ khong bo le, vi bo le
#                               lam `Σ moi noi != tien bank`), dao dung nhung
#                               but toan do CHINH phep ghep suy ra va CON hieu
#                               luc, va KHAI RA thu ⛔ khong dao.
#   2026-08-28  adapters 45->55 ⭐ **Bo nap `Mapping Master`** — bang QUYET DINH
#                               PHAN BO, da nap vao kho THAT: **73 ma `hd`**,
#                               0 ma trung, 23 ma can phan bo CFA2.
#                               ⇒ Tra xong loi hua cua `QĐ-ITL-65`: vung
#                               ALLOCATE gio la mot **phep tinh** co du lieu
#                               that (do tren 10.030 dong so: **3.339 dong
#                               (33,3%)** tra duoc `hd`, **2.922 dong** can
#                               phan bo, **547 dong** ra `Method = 0` — con so
#                               dong `GAP-ALLOC-01`).
#                               ⛔ CON LAI (⛔ khong lam tron len): bon bo nap
#                               nguon C/D/E/F cua `BA-07` van chua co.
#   2026-08-28  api 85 -> 90    ⭐ **Hai cua LUI da co**: `POST .../unmatch`
#                               (`QĐ-ITL-69`) va `POST .../done` + `.../reopen`
#                               (`QĐ-ITL-71`, owner chot NGUOI bam xong).
#                               ⇒ Muc ⓓ cua ghi chu 27/08 (*"bo moi noi"*) DA
#                               giai, va cung do dong luon `GAP-JOIN-06`
#                               (hang cho ⛔ khong tu nha mot dong da chua xong).
#                               ⛔ CON LAI, khai ro chu khong lam tron len 95:
#                               ⓐ **6 duong doc** cua `BA-07` §2
#                                 (`/queue/coverage` `/weekly` `/sources`
#                                  `/mapping-master` `/le` `/queue/state`)
#                               ⓑ nhom `/runs*` (§4)
#                               ⓒ **chot ky / ky** — `GAP-PLAN-04`, chua co dac ta
#   2026-09-03  web 0 -> 15     `B2` BO XUONG xong (`DEV-12` §3): vo man hinh +
#                               `tokens.css` (⭐ MOT ban su that ve mau — truoc
#                               do khoi `:root` nam o BA cho: A-CCR handoff,
#                               ban ve `FLS-Design-P6`, `tools/demo_dong.py`)
#                               + `goi_cua.js` (mot cho duy nhat goi cua, dich
#                               **het** ma trong `bao.MA_LOI` sang cau tieng
#                               Viet, co cong bat hai chieu) + khuon **4 trang
#                               thai** dung chung + luat `import-linter` thu 8
#                               + `BANG_TEP` (loi vuot thu muc ⛔ khong co CHO
#                               de ton tai) + cua TU CHOI phuc vu man hinh khi
#                               nghe ra ngoai loopback (`GAP-WEB-01`).
#                               **Chay that**: `GET /gates` qua HTTP tren cung
#                               cong ⇒ 3 dat · 0 khong dat · 5 chua do duoc.
#                               ⛔ CON LAI, va day la PHAN LON viec:
#                                 ⓐ `B3` F03 day du · ⓑ `B4` F01 hang cho
#                                 ⓒ `B5` F02 **luoi go duoc** — dat nhat
#                                 ⓓ `B6` F06 + hai cua doc con thieu
#                                 ⓔ `B7` UAT — ⛔ MAY KHONG DONG DUOC cong nay
#                               ⇒ 15 la *"vo + duong day da co"*, ⛔ khong phai
#                                 *"man hinh dung duoc"*.
#   2026-09-03  web 15 -> 25    ⭐ `B3` — man **F03 Cong hom nay** DAY DU: bon
#                               cong + ⭐ **the DO PHU hang cho theo tien te**
#                               (cua moi `GET /queue/coverage`) + nut bao cao
#                               tuan **de MO va NOI RA vi sao** (`GET /weekly`
#                               chua co). Hai khoi goi cua DOC LAP: mot cua hong
#                               ⛔ khong keo ca man xuong.
#                               ⛔ CON LAI: `B4` F01 · `B5` F02 (luoi — dat
#                               nhat) · `B6` F06 + 2 cua doc · `B7` UAT.
#   2026-09-03  api 90 -> 92    ⭐ `GET /queue/coverage` — mot trong **6 duong
#                               doc** cua `BA-07` §2 con thieu, nay con **5**.
#                               ⛔ Khong lam tron len 95: nam duong kia
#                               (`/weekly` `/sources` `/mapping-master` `/le`
#                               `/queue/state`) van thieu, va `/queue/state` thi
#                               nen **DONG chu ⛔ khong nen lam** (ba truong cua
#                               no `/queue` da tra roi — agent do 03/09).
#   2026-09-03  web 25 -> 45    ⭐ `B4` — man **F01 Hang cho** noi day du: chan man
#                               theo TUNG tien te · luoi + phan trang khoa ·
#                               **nam hanh dong** (ly do · hoan · ghep · bo ghep
#                               · xong) + **mo lai**. Drawer ghep co Σ ba con
#                               so, dung sai, **TUOI anh chup**, va nut **MO kem
#                               cau giai thich hien san** khi lech.
#                               ⭐⭐ **Cong ra da chay THAT qua HTTP**
#                               (`tests/web/test_vong_f01_pg.py`, 8 bai):
#                               ghep -> bo ghep -> **ghep lai dung dong lenh vua
#                               go (lan 2)**; bam Xong ⇒ **roi hang cho**, Mo
#                               lai ⇒ **quay ve**; dong da xong bien khoi CA
#                               `/queue/summary` LAN `/queue/coverage`.
#                               ⚠ Bo test bat **hai loi that** cua man vua viet:
#                               dung `xong_boi`/`xong_luc` (`BA-06` §8) trong
#                               khi cua tra `boi`/`luc`; va **quen gui `reason`**
#                               — cua DOI ly do o 5/6 thao tac ma §8 ⛔ khong noi
#                               (`GAP-SPEC-02`).
#                               ⛔ CON LAI: `B5` F02 luoi (dat nhat) · `B6` F06 +
#                               2 cua doc *(dang bi `GAP-SPEC-01` chan)* · `B7` UAT.
#   2026-09-03  web 45 -> 70    ⭐⭐ `B5` — man **F02 So ITL**, man DAT NHAT cua
#                               ca chang. Luoi **23 cot** *(⛔ khong 52 — cua
#                               `GET /ledger` CO Y ⛔ khong mang `canon`; xem
#                               `GAP-SPEC-03`)*, tieu de **sinh tu**
#                               `oracle/ledge_spec` + `canon/spec` nen ⛔ khong
#                               mot ten cot tieng Viet nao go tay.
#                               ⭐⭐ **Tam hanh vi §1 chay THAT** duoi `node`
#                               tren mot DOM toi thieu — bam phim, dan vung,
#                               keo xuong, hoan tac *(15 bai)*.
#                               ⭐ **`GAP-SCR-07` DONG**: luu theo lo, ba ca loi
#                               deu co bai *(go tiep khi lo dang bay · mang dut
#                               giua chung · hai nguoi sua mot o)* + cong ra
#                               *"go 20 dong lien tuc ⛔ khong mat mot o nao"*.
#                               ⚠ Bo test bat mot loi that: o bi NGUOI KHAC go
#                               lai hien cau *"khac voi NGUON"* — sai nguoi.
#                               ⛔ **⛔ Chua tang qua 70**: `B6` con bi
#                               `GAP-SPEC-01` chan, va `B7` UAT thi may
#                               ⛔ **khong dong duoc** (cong so 8 khai thang).
#                               ⛔ Vung PHAN BO cua drawer ⛔ khong ve duoc —
#                               `GET /mapping-master` chua co.
MODULE = (
    ("db", "Khuôn dữ liệu · schema SSOT", 8, 100, "P0"),
    ("contract", "Hợp đồng 14 trường", 2, 100, "P0"),
    ("canon", "Khuôn 36 cột (ITL-CANON)", 6, 100, "P1"),
    ("ledger", "Lớp ghi sổ mỏng", 8, 100, "P1"),
    ("repo", "Cửa duy nhất vào kho", 8, 100, "P1→P5"),
    ("oracle", "Thước chuẩn", 9, 95, "P2"),
    ("adapters", "Sáu bộ nạp nguồn", 22, 55, "P2→P3"),
    ("api", "Cửa vào ra", 17, 92, "P4·P5"),
    ("web", "Bốn màn hình", 20, 70, "P6"),
)


def dem_test() -> Counter:
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"],
                       cwd=GOC, capture_output=True, text=True)
    c: Counter = Counter()
    for line in r.stdout.splitlines():
        m = re.match(r"tests[/\\]([\w.]+)[/\\]?.*: (\d+)$", line.strip())
        if m:
            c[m.group(1) if not m.group(1).endswith(".py") else "smoke"] += int(m.group(2))
    return c


def dem_dong(ma: str) -> tuple[int, int, int]:
    """(dong code, so file, so ham) cua `fls/<ma>/`."""
    d = GOC / "fls" / ma
    if not d.is_dir():
        return 0, 0, 0
    dong = ham = 0
    files = [p for p in sorted(d.glob("*.py")) if p.stat().st_size]
    for p in files:
        src = p.read_text(encoding="utf-8")
        dong += len(src.splitlines())
        ham += sum(1 for n in ast.walk(ast.parse(src))
                   if isinstance(n, ast.FunctionDef))
    return dong, len(files), ham


def main() -> int:
    test = dem_test()
    hang = []
    for ma, ten, tsl, xong, pha in MODULE:
        dong, nfile, nham = dem_dong(ma)
        hang.append({"ma": ma, "ten": ten, "pha": pha, "trong_so": tsl,
                     "xong_pct": xong, "test": test.get(ma, 0),
                     "dong": dong, "file": nfile, "ham": nham,
                     "gop_pct": round(tsl * xong / 100, 2)})

    tong_ts = sum(h["trong_so"] for h in hang)
    tien_do = sum(h["gop_pct"] for h in hang)
    tong_test = sum(test.values())
    xong_han = sum(1 for h in hang if h["xong_pct"] == 100)
    dang = sum(1 for h in hang if 0 < h["xong_pct"] < 100)

    if "--json" in sys.argv:
        print(json.dumps({"module": hang, "tien_do_pct": round(tien_do, 1),
                          "tong_test": tong_test, "tong_trong_so": tong_ts},
                         ensure_ascii=False, indent=1))
        return 0

    print(f"{'module':<10}{'pha':<8}{'file':>5}{'dòng':>6}{'hàm':>5}"
          f"{'test':>6}{'xong':>7}{'trọng số':>10}{'góp':>7}")
    print("-" * 66)
    for h in hang:
        print(f"{h['ma']:<10}{h['pha']:<8}{h['file']:>5}{h['dong']:>6}"
              f"{h['ham']:>5}{h['test']:>6}{h['xong_pct']:>6}%"
              f"{h['trong_so']:>9}{h['gop_pct']:>7.2f}")
    print("-" * 66)
    print(f"{'TỔNG':<10}{'':<8}"
          f"{sum(h['file'] for h in hang):>5}{sum(h['dong'] for h in hang):>6}"
          f"{sum(h['ham'] for h in hang):>5}{sum(h['test'] for h in hang):>6}"
          f"{'':>7}{tong_ts:>9}{tien_do:>7.2f}")
    if tong_ts != 100:
        print(f"\n[X] trọng số cộng lại {tong_ts}, phải bằng 100")
    print(f"\ntest thu được ở mọi nơi: {tong_test} "
          f"(ngoài 9 module: {tong_test - sum(h['test'] for h in hang)})")
    print(f"module xong hẳn: {xong_han}/9 · đang làm: {dang}/9")
    print(f"TIẾN ĐỘ THEO KHỐI LƯỢNG VIỆC: {tien_do:.0f}%")
    return 0 if tong_ts == 100 else 1


if __name__ == "__main__":
    raise SystemExit(main())
