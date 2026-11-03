"""Do tien do 10 module — sinh so cho BAN VE 12 (`Ban-ve-Kien-truc-TOBE.html`).

★ Vi sao co file nay. Bang tien do go tay se gia di trong im lang — dung benh ma
ca du an nay dang chua. Nen so trong bang phai SINH RA duoc, va lech thi thay ngay.

Chay:  python tools/tien_do.py            (bang doc cho nguoi)
       python tools/tien_do.py --json     (de dan vao cong cu khac)

`xong` la % TU KHAI theo DoD (`03_IMPLEMENTATION_PLAN` §5) — day la phan xet
doan cua nguoi, ⛔ khong phai so do duoc. Con `test` va `dong` thi do that.
`trong_so` = phan cong viec uoc luong cua module trong ca he.

⛔⛔ **Tong trong so ⛔ KHONG con bi ghim o 100 — va do la mot sua co chu y
(09/09).** Ban truoc cong `gop_pct` lai roi goi ket qua la phan tram, tuc **ngam
dinh** Σ trong so = 100. Khi `fls/xuat` ra doi *(module thu 10, `D3` cua chang
④)* thi hoac ⓐ phai **cat bot trong so cua mot module khac** — mot cau noi rang
phan viec cua no **nho di**, ma no ⛔ khong nho di — hoac ⓑ chap nhan Σ > 100 va
**chia cho dung Σ ay**. Chon ⓑ: pham vi lon ra thi mau so lon ra, va mot module
moi **chua xong** thi keo con so **XUONG**. Do la hanh vi dung; an module moi di
de giu con so cu la dung cai benh ca bo tai lieu nay dang chua.
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
#   2026-09-09  api 92 -> 95    ⭐⭐ **CHIN tuyen moi tu 03/09: 20 -> 29.** Lan
#                               ANH CHUP 4 (`QĐ-ITL-110`) + THU TU NGAY 2
#                               (`113`) + NAP CA LO 2 (`111`/`112`) + KHAI THU
#                               TU CA LO 1 (`117`). ⭐ Ca chin da **chay that**
#                               qua HTTP tren kho THAT: lo 60 nguon ra
#                               **58 vao so · 2 bi chua · 8.356 dong**.
#                               ⛔ **⛔ Chua len 100**: `GET /catalog`
#                               (`GAP-SPEC-01` — chan `B6`) va
#                               `GET /mapping-master` (chan vung PHAN BO cua
#                               drawer `F02`) van ⛔ KHONG ton tai.
#                               ⚠ Va mot lo do 09/09: hai tuyen `/nap/lo*`
#                               song **tron mot ngay ngoai `BA-07`** — cong
#                               `test_ba07_phu_het_tuyen` sinh ra tu do.
#   2026-09-09  web 70 -> 85    ⭐⭐⭐ **`F04` XONG — man thu tu, va la man DUY
#                               NHAT GHI vao so.** Nam trang thai + khoi `②b`
#                               chay that; man **LUON** di duong lo. ⛔ Luu y
#                               `F04` ⛔ **khong nam trong ke hoach `B1`–`B7`**
#                               cua `DEV-12` — no den sau, tu `CR#11` +
#                               `QĐ-ITL-105`/`109`/`110`. ⇒ Bon man cua module
#                               (`F01`·`F02`·`F03`·`F04`) nay **du**.
#                               ⛔ **⛔ Chua len qua 85**: `B6` (`F06` Danh muc)
#                               con bi `GAP-SPEC-01` chan, va `B7` UAT thi may
#                               ⛔ **khong dong duoc** (Lan/Thuong go that).
#   2026-09-09  xuat 0 -> 20    MODULE MOI (thu 10). `D3` co che ghi an toan
#                               xong that: neo theo `(tab, cot khoa, khoa, ten
#                               cot)` ⛔ khong dia chi `A1` · ghi hai lan ⇒ ⛔ 0
#                               o · HAI KHOA (`--duyet` + bien moi truong) · 27
#                               bai. ⛔ CON LAI: `D1` bo xuat 64 cot · `D2` doi
#                               chieu tung dong voi sheet that · `D5` vong khep
#                               kin — va `D4` cho owner chot dich (`QĐ-ITL-116`).
MODULE = (
    ("db", "Khuôn dữ liệu · schema SSOT", 8, 100, "P0"),
    ("contract", "Hợp đồng 14 trường", 2, 100, "P0"),
    ("canon", "Khuôn 36 cột (ITL-CANON)", 6, 100, "P1"),
    ("ledger", "Lớp ghi sổ mỏng", 8, 100, "P1"),
    ("repo", "Cửa duy nhất vào kho", 8, 100, "P1→P5"),
    ("oracle", "Thước chuẩn", 9, 95, "P2"),
    ("adapters", "Sáu bộ nạp nguồn", 22, 55, "P2→P3"),
    ("api", "Cửa vào ra", 17, 95, "P4·P5"),
    ("web", "Bốn màn hình", 20, 85, "P6"),
    # ⭐⭐ Module thu 10 — ra doi 09/09 cung `D3` (`QĐ-ITL-118`).
    #
    # ⚠ `trong_so = 6`: no giu **ca chang ④** cua lo trinh — `D3` co che ghi
    #   an toan *(xong)* + `D1` bo xuat khuon 64 cot + `D2` doi chieu tung dong
    #   + `D5` vong khep kin *(ca ba ⛔ chua co)*. Dat ngang `canon` (6) vi khoi
    #   luong tuong duong: mot khuon co dinh + mot phep doi chieu.
    #   ⛔ Con so nay la **xet doan cua toi**, owner sua duoc.
    #
    # ⚠ `xong_pct = 20`: `D3` xong that *(27 bai, ke ca bai "chen mot dong ⇒ o
    #   dich tu dich theo")*. ⛔ Nhung `D1`/`D2`/`D5` **⛔ khong ton tai**, va
    #   `D4` con cho mot quyet dinh cua owner (`QĐ-ITL-116`: dich `A-CCR` hay
    #   ITL adjust). ⇒ 1/4 viec + phan ha tang ⇒ 20, ⛔ khong 25.
    ("xuat", "Đưa số ra ngoài", 6, 20, "P8·chặng ④"),
)

# ⛔⛔ **Cổng chặn DRIFT trọng số — và vì sao nó ⛔ KHÔNG còn là `== 100`.**
#
# Bản trước đòi `Σ trọng số == 100`. Cổng ấy canh đúng một thứ: **trọng số bị
# sửa lẻ trong im lặng**. Nhưng nó làm điều đó bằng cách ghim một con số mà
# **phạm vi dự án ⛔ không thể lớn ra được** — nên khi `fls/xuat` ra đời, đường
# duy nhất cho cổng xanh là **cắt trọng số của một module khác**, tức nói rằng
# phần việc của module ấy **nhỏ đi** khi nó ⛔ không nhỏ đi.
#
# ⇒ Cổng này nay canh **một con số ĐƯỢC KHAI**: đổi `Σ` thì phải đổi hằng số
#   này **VÀ viết lý do vào nhật ký trên**. Drift vẫn bị bắt *(sửa lẻ một trọng
#   số ⇒ `Σ` lệch ⇒ ĐỎ)*, nhưng phạm vi lớn ra ⛔ không còn buộc phải nói dối.
TONG_TRONG_SO = 106      # 09/09: 100 → 106, +6 cho module `xuat` (chặng ④)


def dem_test() -> Counter:
    r = subprocess.run([sys.executable, "-m", "pytest", "--collect-only", "-q"],
                       cwd=GOC, capture_output=True, text=True)
    c: Counter = Counter()
    for line in r.stdout.splitlines():
        m = re.match(r"tests[/\\]([\w.]+)[/\\]?.*: (\d+)$", line.strip())
        if m:
            c[m.group(1) if not m.group(1).endswith(".py") else "smoke"] += int(m.group(2))
    return c


# ⭐ Duoi tep duoc coi la MA. ⛔ `.json`/`.md` ⛔ khong vao — chung la du lieu
#   va van ban, va dem chung vao *"dong ma"* se lam con so phong len vo nghia.
DUOI_MA = frozenset({".py", ".js", ".css", ".html"})


def dem_dong(ma: str) -> tuple[int, int, int]:
    """(dong code, so file, so ham) cua module `fls/<ma>/` — **DE QUY**.

    ⛔⛔⛔ **Ban truoc chi `glob("*.py")` o DUNG mot tang, va no lam module
      `web` noi doi 22 lan.**

    `fls/web/` co `phuc_vu.py` *(265 dong)* va `fls/web/tep/` *(**5.961**
    dong `.js`/`.css`/`.html` — tuc TOAN BO man hinh)*. Phep dem cu bao
    **265**. Nen bang tien do in ra `web  265 dong  ·  333 test` — **nhieu
    bai thu hon dong ma**, mot dieu vo ly nam trong tai lieu **da duoc cong
    so song GHIM**, va ⛔ khong ai thay trong 7 ngay.

    ⚠ Do la mot cai cong **canh dung mot con so SAI**: `va_so_song.py` giu
      cho `265` luon khop, nen no **bao ve** con so sai thay vi bat no.

    ★ Bai hoc chep lai o day vi no la luat cho moi phep dem sau: **mot phep
      dem phai phu HET vat lieu cua thu no dem**. `fls.web` ⛔ khong phai
      *"mot tep Python"* — no la **bon man hinh**, va bon man hinh ay viet
      bang `.js`. Dem theo duoi tep quen thuoc thay vi theo **thu module ay
      thuc su lam bang gi** la cung mot lop loi voi *"do o cua DOC roi khai
      la ket qua cua cua GHI"*.

    ⛔ `ham` van chi dem cho `.py` *(can `ast`)* — khai ra chu ⛔ khong de
      nguoi doc tuong no gom ca ham JS.
    """
    d = GOC / "fls" / ma
    if not d.is_dir():
        return 0, 0, 0
    dong = ham = 0
    files = [p for p in sorted(d.rglob("*"))
             if p.is_file() and p.suffix in DUOI_MA and p.stat().st_size
             and "__pycache__" not in p.parts]
    for p in files:
        src = p.read_text(encoding="utf-8")
        dong += len(src.splitlines())
        if p.suffix == ".py":
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
    if not tong_ts:
        raise SystemExit("⛔ Σ trong so = 0 ⇒ ⛔ khong chia duoc")
    # ⛔ Chia cho **dung Σ trong so**, ⛔ khong ngam dinh 100. Xem dau tep.
    tien_do = 100 * sum(h["gop_pct"] for h in hang) / tong_ts
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
    if tong_ts != TONG_TRONG_SO:
        print(f"\n[X] trọng số cộng lại {tong_ts}, bản khai nói "
              f"{TONG_TRONG_SO} — sửa `TONG_TRONG_SO` VÀ viết lý do vào nhật ký")
    print(f"\ntest thu được ở mọi nơi: {tong_test} "
          f"(ngoài {len(MODULE)} module: "
          f"{tong_test - sum(h['test'] for h in hang)})")
    # ⛔ Đếm `len(MODULE)`, ⛔ không gõ `9`: một con số gõ tay cạnh một bảng
    #   sinh ra được là đúng chỗ mà `GAP-DOC-08` sống.
    print(f"module xong hẳn: {xong_han}/{len(MODULE)} · "
          f"đang làm: {dang}/{len(MODULE)}")
    print(f"TIẾN ĐỘ THEO KHỐI LƯỢNG VIỆC: {tien_do:.0f}%")
    return 0 if tong_ts == TONG_TRONG_SO else 1


if __name__ == "__main__":
    raise SystemExit(main())
