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
import os
import pathlib
import re
import subprocess
import sys
import zoneinfo

GOC = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

# ⭐ `WO-011 T1` — SO ACTOR: moi chuoi actor lay tu day, ⛔ go lai.
from fls.repo.danh_muc_actor import ACTOR_NHIP as _ACTOR_NHIP  # noqa: E402

# ⛔⛔⛔ Cong nay tung **DO-BLIND**: tren mot shell dung trang ma he thong,
#   dong `print` cua no vo o dung chu `⛔` — nghia la no in duoc moi dong
#   `OK` *(ASCII)* va **no vo dung luc no can noi mot cai cong DO**. Ket qua
#   la mot cong *"chay xong khong thay loi"* trong khi no ⛔ chua bao gio in
#   ra noi cai loi. ⇒ Dat lai dong ra ngay tai day, TRUOC moi phep do.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
# 2026-09-03: bo tai lieu ITL da CHUYEN VAO repo nay (`docs/ITL/`). Truoc do no
# song o repo FIN-ERP canh ben, nen cong phai voi qua mot duong dan tuong doi
# `../FIN-ERP/...` — chi dung khi hai repo tinh co nam canh nhau tren cung mot
# may. Nay tai lieu va cong o CUNG repo ⇒ duong dan chac chan, CI doc duoc.
TAI_LIEU_MAC_DINH = GOC / "docs" / "ITL"

DASH = "01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md"
ROADMAP = "01_Orchestrator/08_MIGRATION_ROADMAP.md"
BANVE = "02_BA/Artifacts/Ban-ve-Kien-truc-TOBE.html"

MASTER = "00_MASTER_INDEX.md"
# ⭐⭐ 09/09: tep MOC theo HAI TAC VU. Gia tri cua no la CON SO, va dung
#    nhung con so ay la thu bon moc `A`-`D` duoc thiet ke de LAM DOI.
MOC = "01_Orchestrator/09_MILESTONES_HAI_TAC_VU.md"
# ⭐ 09/09: `BA-06` bat dau mang so SONG (so nguon `fls_source`) ⇒ no phai
#    vao cong. Truoc do no chi mang so trong changelog (luat ⓒ: so cu la dung).
BA06 = "02_BA/06_SCREEN_SPEC.md"

# ⭐⭐ BA cho ghi con so cua **chinh cong nay** (`N/N`). Khai o day thanh MOT
#    danh sach de phep dem `tong` do duoc `len(...)` — thay cho mot `+ 3` go
#    tay tung lam cong tu khai **88** trong khi no co **98** phep so.
_TU_DEM = (
    # ⛔ Neo dau `**` (01/10, `WO-001`): so `QĐ-ITL-150` ghi *"cong so song
    #   01/10"* — mot NGAY, ⛔ mot phep dem — va mau tran khop 2 lan.
    ("master · số phép so của cổng", MASTER,
     r"\*\*cổng số sống (\d+)/(\d+)\*\*"),
    ("dashboard · số phép so của cổng", DASH,
     r"`tools/kiem_so_song\.py` \*\*ĐẠT (\d+)/(\d+)\*\*"),
    ("bản vẽ · số phép so của cổng", BANVE, r"cổng số sống (\d+)/(\d+)"),
)


@dataclasses.dataclass(frozen=True)
class Muc:
    """Mot phep so: `mau` khop dung mot lan trong `file`, cac nhom = `gia`."""

    ten: str
    file: str
    mau: str
    gia: tuple[str, ...]


def _phan_tram(a: int, b: int) -> str:
    """`a/b` -> `26,9` — dau PHAY, dung loi tai lieu viet."""
    if not b:
        raise SystemExit("⛔ khong do duoc ty le: mau so = 0")
    return f"{a * 100 / b:.1f}".replace(".", ",")


def vn(n: int) -> str:
    """Dinh dang so kieu tai lieu: dau cham ngan hang nghin."""
    return f"{n:,}".replace(",", ".")


def _dem_tuyen() -> dict[str, str]:
    """Dem cua theo KHOA cua chung: `itl_id` ↔ dong lenh chi.

    ⛔⛔⛔ **Day la phep do cua mot cai THIEU, va do la ly do no phai o trong
       cong.** `QĐ-ITL-122`: owner chot chieu do la *"`Trans` map vao `PM`"*,
       nen cau hoi cua viec la *"lenh chi nao ⛔ chua tim duoc tien"*. Do
       09/09: **10** cua khoa `itl_id`, **0** cua khoa dong lenh ⇒ ⛔ **khong
       mot duong nao** hoi duoc cau ay.

    ⭐ Ghim `0` vao cong nghia la: khi ai do **mo** cua ay thi `0 → 1`, cong
      **DO**, va nguoi sua phai vao sua **CAU** trong tai lieu. Neu ⛔ khong
      ghim, cau *"⛔ khong co cua nao"* se song sot **qua ca luc no thanh
      sai** — dung hinh benh `GAP-DOC-07` va `GAP-DOC-08`.
    """
    from fls.api.bang_tuyen import BANG_TUYEN                # noqa: PLC0415

    itl = sum(1 for t in BANG_TUYEN if "{itl_id}" in t.duong)
    # ⛔⛔ Dem cua **PHIA LENH CHI**, ⛔ khong chi cua co `{pm_line_id}`
    #    trong duong. Ban dau toi dem theo tham so duong va duoc **1** —
    #    trong khi co **3** cua phia lenh chi *(hai cua danh sach ⛔ khong
    #    co tham so duong nao)*. Mot phep dem hep hon cau van no dang canh
    #    la mot phep dem **noi nho hon su that**.
    pm = sum(1 for t in BANG_TUYEN
             if "/lenh-cho" in t.duong or "/queue/lenh/" in t.duong)
    return {"tuyen_khoa_itl": str(itl), "tuyen_phia_pm": str(pm)}


def _cong_moc_a(k: dict[str, int]) -> dict[str, str]:
    """SAU cong cua MOC `A` -> `(so DAT, so MOT NUA, so CHUA)`.

    ⛔⛔⛔ **Vi sao phep dem nay o trong MA, ⛔ khong trong mot cau tai lieu.**

    Ban ve 13 mo dau bang mot the *"moc 1 dong duoc may cong"*. Lan dau toi
    **go tay `2/4`** — va no **sai theo dung cai bang nam ngay duoi the ay**:
    bang ghi `A4` la cong duy nhat `✔`, con `A2`/`A3` la `◐`. Mot con so tong
    go tay canh mot bang chi tiet la cho **de mau thuan nhat** cua ca trang,
    va no ⛔ khong bao gio tu bao.

    ⇒ Luat dem khai ngay day, doc lai duoc, va **⛔ khong noi long**:

      ⓐ `A1` DAT khi co **>=2** anh do NHIP sinh *(`actor` ⛔ khong mang
        `tools/`)* va chung roi vao **>=2 gio dong ho khac nhau**. Chi dem
        so anh la ⛔ khong du: hai anh trong cung mot gio la dung cai loi ma
        `da_chup_gio_nay` duoc viet ra de chan.
      ⓑ `A2` co hai ve. Ve *"vet nap ⛔ khong dut"* do duoc **ngay**. Ve
        *"xoa anh qua 30 ngay ⛔ chua nap"* thi **chi do duoc khi kho co mot
        anh nhu the** — hom nay anh gia nhat ⛔ chua du tuoi ⇒ ve ay dang
        xanh tren mot **tap RONG**, va *"xanh tren tap rong la CHUA DO"*.
        ⇒ `A2` = **MOT NUA**, ⛔ khong phai DAT.
      ⓒ `A3` co hai ve: *"co duong vao"* **da chay that**, con *"dong moi vao
        ⛔ khong qua mot dong lenh go tay"* thi phu thuoc `A1` ⇒ khi `A1`
        ⛔ chua dat thi `A3` cung chi la **MOT NUA**.
      ⓓ `A4` DAT khi **ca hai** be mat ⛔ khong co dong trung: trong mot anh
        lenh chi, va trong bang moi noi.
    """
    a1 = k["anh_nhip"] >= 2 and k["anh_nhip_gio"] >= 2
    a2_nua = k["anh_dut"] == 0
    a2 = a2_nua and k["anh_gia_nhat_ngay"] > 30
    a3_nua = k["run_pm"] >= 2
    a3 = a3_nua and a1
    a4 = k["pm_trung"] == 0 and k["noi_trung"] == 0
    # ⭐⭐⭐ Hai cong THEM 10/09 — xem khoi chu thich o `tang_nguon` /
    #   `gio_anh_bank_chua_nap`. Ca hai hoi cau ma `A1`-`A4` ⛔ KHONG hoi.
    a5a = k["tang_nguon"] == 1
    a5b = 0 <= k["gio_anh_bank_chua_nap"] <= 48
    dat = sum((a1, a2, a3, a4, a5a, a5b))
    nua = sum((a2_nua and not a2, a3_nua and not a3))
    return {"moc_a_dat": str(dat), "moc_a_nua": str(nua),
            "moc_a_chua": str(6 - dat - nua)}


def _cong_moc_b(k: dict[str, int]) -> dict[str, str]:
    """Nam cong cua MOC `B` -> `(so DAT, so MOT NUA, so CHUA)`.

    ⛔⛔⛔ **Vi sao phep dem nay phai o trong MA, va vi sao no phai do tren
      KHO THAT.**

    Ngay 10/09 toi vua viet **ba bai** chung minh duong LUI cua mot LO chay
    duoc *(`test_cua_ghep_lo_pg.py`)*, va phan xa dau tien cua toi la ghi
    *"`B4` DAT"* vao tai lieu. ⛔ **Sai.** Bai thu chay tren **kho TEST**;
    con cong `B4` hoi *"duong LUI con nguyen"* tren **so THAT**, va tren so
    that `fls_pm_unlink` = **0** — ⛔ **chua mot cu bo ghep nao tung xay ra**.

    ⇒ Luat: *"bo test xanh"* ⛔ **KHONG** dong duoc mot cong cua moc. No
      chung minh **ma chay dung**; cong hoi **viec da xay ra**. Hai cau khac
      nhau, va gop chung lai la cach de mot lan `422 FLS-SOAT-CHAN` no vao
      mat lan dau co mot lo that.

    Luat dem, khai ra va doc lai duoc:

      ⓐ `B1` DAT khi do duoc **mau so phia PM** *(so dong lenh chi)* — no
        da do that va da vao cong *(`QĐ-ITL-121`/`122`)*.
      ⓑ `B2` doi cua ghep LO **da chay tren so THAT**: ⛔ khong phai *"cua co
        ton tai"*. Cua co tu 09/09 va ⛔ chua ai bam.
      ⓒ `B3` doi **hau qua do duoc** — mot lo that lam do phu DOI. Cung dieu
        kien voi `B2`, nen no ⛔ khong the dat truoc `B2`.
      ⓓ `B4` doi **>=1 dong `fls_pm_unlink`** tren so that. Ma da co bai thu
        *(10/09)* ⇒ **MOT NUA**, ⛔ khong phai DAT.
      ⓔ `B5` doi **>=1 `fls_queue_event`** do **nguoi that**.

    ⚠ `B2`/`B3`/`B5` la **CHUA**, ⛔ khong phai *"mot nua"*: ⛔ khong mot ve
      nao cua chung da xay ra tren so that. Chi `B4` co mot ve *(ma da chung
      minh)* nen no la mot nua.
    ⛔⛔ **VA LUAT NAY CO NGAY HET HAN, khai ngay day:** hom nay
      `su_kien_cho = 0`, nen *"da co ai bam cua hang cho chua"* la **mot** cau
      hoi va no tra loi duoc cho **ca ba** cong `B2`/`B3`/`B5`. Giay phut con
      so ay len `1`, phep dem nay **thanh qua tho** — no se ⛔ khong phan biet
      duoc *lo da chay* voi *mot cu bam le*. ⇒ Luc do **phai siet lai**, va
      dong nay la loi nhac. ⛔ Dung de no song sot qua cai moc ay.
    """
    # ⭐ `B1` = *"mau so duoc dinh nghia bang SU KIEN"* (`QĐ-ITL-121`), va no
    #   do duoc khi va chi khi kho **co dong lenh chi** de ma do. `anh_chup`
    #   la so dong `fls_pm_line`.
    # ⛔⛔ Ban dau toi viet `k.get("dong_lenh", 0)` — mot khoa ⛔ **KHONG TON
    #    TAI** trong `kho` *(no chi co trong `khai()`, da qua `vn()` thanh
    #    chuoi)*. `.get(..., 0)` tra `0` **im lang** ⇒ `B1` bao **CHUA** trong
    #    khi no da dat. Mot `.get` co gia tri mac dinh la mot cho **xanh/do
    #    sai ma ⛔ khong ai thay** — dung lop loi `INV-I16`.
    b1 = k.get("anh_chup", 0) > 0
    # ⛔⛔⛔ **SUA 10/09 — TIEN DE CUA BA CONG NAY DA VO, va no vo AM THAM.**
    #
    # Ban cu do `su_kien_cho` = `count(*) fls_queue_event`, voi tien de *"chi
    # cua hang cho ghi vao day"*. Nhung `lo_nap` goi `ghi_tay.ghi_ly_do()` cho
    # moi dong bi CO ⇒ **MAY cung ghi vao bang ay**. Cu dung lai so 10/09 ghi
    # **93.666** su kien `reason` mang `actor = dung-lai-so@apero.vn`, va ba
    # cong `B2`/`B3`/`B5` **lat sang XANH** trong khi ⛔ **0 cu bam cua nguoi**.
    #
    # ⭐ Cho phan biet duy nhat SACH la `evt_type`: `reason` la loai **DUY
    #   NHAT** ma may cung ghi; `match`/`unmatch`/`done`/`reopen`/`defer` chi
    #   sinh tu mot cu bam co y trong `F01`.
    #
    # ⚠ Phep dem nay **thieu di** mot `reason` do NGUOI that go — va do la
    #   chieu **an toan**: mot cong bao it hon su that con sua duoc, mot cong
    #   bao XANH khi ⛔ chua ai chung minh gi thi ⛔ khong.
    #
    # ⛔⛔ **Tien de tren VO LAN NUA 18/09** *(`QĐ-ITL-143`: may tu ghep ghi
    #    `match` actor `may@fls`)* va ⛔ khong ai thay suot 13 ngay — `KQ-002
    #    F-2`. Sua 01/10 *(`WO-001 T1a`+`T1b`)* o **cau SQL** trong `do_may()`
    #    *(loai them actor `MAY` + dong UAT)*, ⛔ o day: luat dem khong doi.
    # ⚠ "Ngay het han" trong docstring **van chua den**: so that hom nay
    #   `su_kien_cho_nguoi` = **0** sau khi loai may + UAT. No den khi ke toan
    #   bam cu dau tien — luc ay `B2`·`B3`·`B5` cung nhay, va phai siet.
    bam = k.get("su_kien_cho_nguoi", 0) > 0
    b2 = bam
    b3 = bam
    b5 = bam
    b4 = k.get("moi_noi_da_bo", 0) > 0
    dat = sum((b1, b2, b3, b4, b5))
    # ⭐ `B4` co MOT ve da xong: ma duong LUI cua mot LO da co bai thu (10/09,
    #   3 bai, da chung minh DO). Ve con lai — *"da xay ra tren so THAT"* —
    #   thi `fls_pm_unlink = 0`.
    nua = 0 if b4 else 1
    return {"moc_b_dat": str(dat), "moc_b_nua": str(nua),
            "moc_b_chua": str(5 - dat - nua)}


# ─────────────────────────────────────────────────────────── do tu MAY
def _chay(*lenh: str) -> str:
    # ⛔⛔ `PYTHONUTF8=1` — ⛔ khong phai cho dep, va ⛔ khong the bo.
    #   `lint-imports` doc ma nguon `fls/` bang trang ma HE THONG khi thieu
    #   bien nay, va ma nguon o day day tieng Viet ⇒ tren mot shell chua dat
    #   bien, no do voi *"'charmap' codec can't decode byte 0x90"* va tra ma
    #   `1`. Cong se noi *"⛔ khong do duoc"* — dung, nhung no **do vi mot ly
    #   do ⛔ khong lien quan den thu no canh**, va mot cai cong do nhu the
    #   la mot cai cong **se bi tat**. ⇒ Dat moi truong ngay tai day, mot
    #   lan, cho **moi** tien trinh con cong goi.
    moi = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    r = subprocess.run(lenh, cwd=GOC, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=moi)
    if r.returncode != 0:
        raise SystemExit(f"⛔ khong do duoc: `{' '.join(lenh)}` "
                         f"tra ma {r.returncode}\n{r.stderr[-400:]}")
    return r.stdout


# Dem so BO TRI COT khac nhau tren cac ban khai **dang hieu luc**.
# `%s` = cho cam `Description` khi dem theo **5 truong FLS thuc doc**.
_Q_BO_TRI = """
select count(distinct h) from (
  select string_agg(k.truong || ':' || k.cot, ',' order by k.truong) as h
  from fls_khai_cot k
  join (select source_id, max(version) as v from fls_khai_cot
        group by source_id) m
    on m.source_id = k.source_id and m.v = k.version
  %s
  group by k.source_id
) t"""


# ⭐⭐⭐ Hai DAU THOI DIEM: `(dau_so, dau_anh)`.
#
# ⛔⛔ **Sua 01/10 (`WO-001 T2`, `Ra-soat` `R-2`).** Ban cu lay `started_at` cua
#    luot `fls_run` **moi nhat bat ky**. Tu khi nhip chup nap anh PM moi gio
#    *(`NAP-2026-10-01-PM…`, **0** dong `fls_itl`)*, luot moi nhat **luon** la
#    mot anh PM ⇒ cau *"`8.387` dong so (ban sao nap `01/10 18:20`)"* noi rang
#    so vua nap chieu nay — trong khi so nap lan cuoi **10/09** *(hai luot
#    `NAP-2026-09-10-RTANG24037` 6.617 + `NAP-2026-09-10-BU1` 1.770)*. Con so
#    dung, cau sai, cong xanh: dung benh `GAP-DOC-08`.
# ⭐ Dau SO = luot nap **co dong trong `fls_itl`** moi nhat. Dau ANH PM giu
#   nguyen *(`max(read_at)` cua `fls_pm_line`)*.
# ⚠ Dat o day *(⛔ trong `do_may`)* de bai thu chay DUNG cau nay tren khuon CTE.
_Q_GIO = ("select (select r.started_at from fls_run r"
          " where exists (select 1 from fls_itl i where i.run_id = r.run_id)"
          " order by r.started_at desc limit 1),"
          " (select max(read_at) from fls_pm_line)")


def _kiem_hang_may(sql: str, tien_to: str = "",
                   may: frozenset[str] | None = None) -> None:
    """⛔ No ⇒ `SystemExit` neu cau dem *"nguoi"* ⛔ mang DUNG ban sinh tu SO.

    ⭐ Rui ro 2 cua `WO-001`: *"loc theo actor la luat moi de vo lan thu ba —
    khai hang actor may MOT cho, co bai ghim"*. Cau SQL cua cong phai la mot
    **chuoi THUAN** *(hai bai nghiem thu `KQ-002`, `KQ-010` doc no bang `ast`
    roi CHAY no)* nen no ⛔ noi duoc bien. ⇒ Ham nay la soi day noi hai cho.

    ⛔⛔ **Sua 02/10 (`WO-011 T2`/`T4`, `HOI-012` cau 2).** Ban `WO-001` chi soi
       MOT hang (`'may@fls'`) — dung cai danh sach den mot phan tu ma
       `KQ-010 F-2 ⓐ` chi ra: ma co **8** actor ⛔ phai nguoi. Nay cau phai
       chua **trung byte** hai mau SINH tu so `fls/repo/danh_muc_actor.py`:
         · `sql_ngoai_may(<tien_to>actor)` — CA danh sach `ACTOR_MAY`;
         · `sql_khong_uat(<tien_to>reason)` — MOT luat UAT *(`09` v1.13 ⓓ)*.
       Ai them mot actor may vao so ma quen cau ⇒ cong **DO ngay lan chay**
       *(⛔ lang le dem may thanh nguoi lan thu tu)*.
    ⚠ `may` chi de bai thu dat mot so KHAC vao — cong ⛔ truyen.
    """
    from fls.repo import danh_muc_actor as dm              # noqa: PLC0415

    ngoai = dm.sql_ngoai_may(tien_to + "actor",
                             dm.ACTOR_MAY if may is None else may)
    if ngoai not in sql:
        raise SystemExit(
            "⛔ khong do duoc: cau dem su kien NGUOI ⛔ mang DUNG danh sach MAY "
            "cua so `fls/repo/danh_muc_actor.py::ACTOR_MAY` — them/doi actor "
            "may ma quen cau ⇒ may lai duoc dem la nguoi (`KQ-002 F-2`, "
            f"`WO-011 T2`). Mong chuoi: {ngoai}")
    if dm.sql_khong_uat(tien_to + "reason") not in sql:
        raise SystemExit(
            "⛔ khong do duoc: cau dem su kien NGUOI ⛔ mang DUNG mau UAT cua so "
            "(`danh_muc_actor.sql_khong_uat`) — `WO-011 T4`: UAT nhan MOT luat")


# ⭐⭐⭐ `WO-011 T3` — ACTOR MOI ⇒ goi ten, NO MOT lan *(`09` v1.14 ⓒ)*.
#
# ⛔⛔ **Vi sao.** Luat *"nguoi that"* hom nay la *"⛔ thuoc `ACTOR_MAY` ∧ ⛔ UAT"*
#    — tuc van la **tru cai da biet la may** *(danh muc ke toan hoan, owner
#    02/10)*. Cho ho cua no: mot tien trinh may MOI quen khai ⇒ duoc dem la
#    NGUOI ⇒ moc `B` nhich **sai**. ⇒ Moi actor tren kho that ⛔ thuoc ca hai
#    so *(`ACTOR_MAY ∪ ACTOR_DA_THAY`)* van duoc dem la nguoi *(⛔ loai — mot
#    ke toan that bam lan dau ⛔ duoc phep bien mat)*, nhung cong **goi ten**
#    no va **NO** cho toi khi ai do khai no vao mot trong hai so.
# ⭐ Bao **hiem** *(`11 §6`)*: moi actor mot dong, moi lan mot cu khai la het.
#
# ⭐ Ba bang **goc** *(`fls_queue_event` · `fls_adjustment` · `fls_journal`)*.
#   `fls_da_xong` la khung xem tren `fls_queue_event`, `fls_pm_unlink` noi ve
#   `fls_queue_event` qua `evt_id` ⇒ chung **nam trong** bang dau, ⛔ cong lai.
# ⭐ So in ra = so **THAO TAC**: moi su kien hang cho + moi but toan go THANG
#   *(`evt_id IS NULL` — `ghi_but_toan` o luoi `F02`)*. But toan theo su kien
#   *(goi y `hd`/`cdt1` cua mot cu ghep)* va dong nhat ky *(ban sao 1:1 cua but
#   toan, `ghi_tay._them`)* ⛔ cong them: mot cu `Gan` la **1**, ⛔ phai 5.
#   Cot thu ba = tong so dong o ca ba bang — de nguoi doc thay ca hai con so.
def _q_actor_moi(so: frozenset[str] | None = None) -> str:
    from fls.repo import danh_muc_actor as dm              # noqa: PLC0415

    so = (dm.ACTOR_MAY | dm.ACTOR_DA_THAY) if so is None else so
    # ⚠ Bang con trong `from (…)`, ⛔ `with x as`: bai thu che bang that bang
    #   mot CTE cung ten dat **truoc** cau — hai chu `with` thi vo cu phap.
    return ("select actor, sum(thao_tac)::int, count(*)::int from ("
            " select actor, 1 as thao_tac from fls_queue_event"
            " union all select actor, case when evt_id is null then 1 else 0"
            " end from fls_adjustment"
            " union all select actor, 0 from fls_journal) x"
            f" where {dm.sql_ngoai_may('actor', so)}"
            " group by actor order by actor")


def canh_actor_moi(ds: list) -> list[str]:
    """`[(actor, thao_tac, so_dong)]` → dong bao, ⛔ rong ⇒ cong mot moc `B` NO."""
    return [f"⚠ ACTOR MỚI: {a} · {n} dòng *(thao tác; {tong} dòng ở "
            "`fls_queue_event`+`fls_adjustment`+`fls_journal`)* — xem tên rồi "
            "khai vào `fls/repo/danh_muc_actor.py`: `ACTOR_MAY` nếu là máy, "
            "`ACTOR_DA_THAY` nếu ⛔ phải máy"
            for a, n, tong in ds]


def do_may() -> dict[str, str]:
    """Do TAT CA con so song. Do khong duoc thi nem loi — ⛔ khong doan."""
    from fls.db.kho import dsn_that                       # noqa: PLC0415
    from fls.db.schema import TABLES                      # noqa: PLC0415

    import psycopg                                        # noqa: PLC0415

    from fls.oracle import ledge_spec as _ls                 # noqa: PLC0415

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
        gio = c.execute(_Q_GIO).fetchone()
        def dem(sql: str) -> int:
            return int(c.execute(sql).fetchone()[0])

        def dem_nguoi(sql: str, tien_to: str = "") -> int:
            _kiem_hang_may(sql, tien_to)
            return dem(sql)

        # ⭐ `WO-011 T3` — doc TRUOC: danh sach actor ngoai so *(⛔ con so)*.
        actor_moi = [list(r) for r in c.execute(_q_actor_moi()).fetchall()]

        kho = {
            "so_dong": dem("select count(*) from fls_itl"),
            # ⚠ `fls_moi_noi` — moi noi CON HIEU LUC. Dem tren `fls_pm_link`
            # thi tu 2026-08-28 con so se cong ca cac moi noi DA BO
            # (`QĐ-ITL-69`), va tai lieu se noi mot con so ⛔ khong ai dung.
            "moi_noi": dem("select count(*) from fls_moi_noi"),
            "dong_lenh_noi": dem("select count(distinct pm_line_id) "
                                 "from fls_moi_noi"),
            # ⛔⛔ **Sua 01/10 (`WO-001 T1b`, `QĐ-ITL-150 ⓐ`).** Cu bo ghep
            #    DAU TIEN tren so that la cu **UAT** cua owner *(`unlink 163568`
            #    → `evt 163567`, `itl_id 27728`, reason `UAT 01/10 - hoan lai…`)*
            #    ⇒ dem tran `fls_pm_unlink` lat `B4` DAT bang mot cu **thu duong
            #    ghi**, ⛔ viec that. Owner chot: UAT ⛔ BAO GIO tinh la nguoi.
            # ⭐ Loc theo **ly do** cua su kien `unmatch` *(`evt_id` — "AI bo va
            #   VI SAO song o do, MOT cho")*, ⛔ theo actor: xem khoi chu thich
            #   o `su_kien_cho_nguoi` ben duoi.
            # ⚠ (01/10) `left(…, 4)` chu ⛔ `LIKE 'UAT %'`: `dem()` goi
            #   `execute(sql)` ⛔ kem tham so — xem chu thich `anh_tong`.
            # ⛔⛔ **Sua 02/10 (`WO-011 T5`, `KQ-010 F-2 ⓑ`) — `B4` DOI XUNG.**
            #    Ban 01/10 loc UAT nhung ⛔ loc MAY: mot tien trinh may bo ghep
            #    *(hom nay chi `fls/api/xu_ly.py:470` goi `bo_moi_noi` ⇒ 0 cham)*
            #    se dong `B4` voi 0 cu bam nguoi — dung lo `B2`/`B3`/`B5` da vo
            #    18/09. Nay cung hai vach nhu `su_kien_cho_nguoi`, cung sinh tu
            #    so *(`_kiem_hang_may(…, "e.")` doi chieu)*. Luat UAT cu
            #    `left(…, 4) <> 'UAT '` ⛔ con — xem `T4` ben duoi.
            "moi_noi_da_bo": dem_nguoi(
                "select count(*) from fls_pm_unlink u join fls_queue_event e on "
                "e.evt_id = u.evt_id where coalesce(e.actor, '') <> all "
                "(array['cong-ghi@apero.vn', 'cong@apero.vn', "
                "'dung-lai-so@apero.vn', 'may@fls', 'nhip@fls', 'nhip@fls(tay)', "
                "'thu@apero.vn', 'verify-sua-duoc-gi-2@fls', "
                "'verify-sua-duoc-gi@fls']) and coalesce(e.reason, '') !~* '^[ "
                "\\t\\n\\r\\f\\v\\u00a0\\u3000\\ufeff]*uat([^[:alpha:]]|$)'", "e."),
            "anh_chup": dem("select count(*) from fls_pm_line"),
            "phieu": dem("select count(distinct pm_slip_id) from fls_pm_line"),
            "loai": dem("select count(*) from fls_reject"),
            # ⭐⭐⭐ Bon con so cua TAC VU ① — do phu MAPPING PM<->tien.
            #    ⛔ Dem `distinct itl_id` tren `fls_moi_noi` (moi noi CON
            #    HIEU LUC), ⛔ khong tren `fls_pm_link` — tu 28/08
            #    (`QĐ-ITL-69`) bang do con giu ca moi noi DA BO.
            "itl_ghep": dem("select count(distinct itl_id) from fls_moi_noi"),
            "itl_chua_ghep": dem(
                "select count(*) from fls_itl i where not exists ("
                " select 1 from fls_moi_noi m where m.itl_id = i.itl_id)"),
            # ⭐⭐⭐ Hai con so cua TAC VU ② — va ca hai dang la **0**.
            #    ⛔ `0` o day ⛔ KHONG phai "thieu so do": no la phep do
            #    noi rang lan adjust **chua mot lan** chay tren kho that.
            #    Khi no nhay `0 -> 1` thi cong DO, va cong do **vi tien
            #    do di len** la cong dang lam dung viec.
            "but_toan_sua": dem("select count(*) from fls_journal"),
            "su_kien_cho": dem("select count(*) from fls_queue_event"),
            # ══ ⭐⭐⭐ BON CONG cua MOC `A` — them 2026-09-09 ══
            #
            # ⛔⛔ **Vi sao chung phai vao cong, ⛔ khong viet vao mot cau.**
            #    Bang *"Buoc tiep"* cua ban ve dung nguyen **16 ngay** voi ba
            #    viec cua 24/08 — hai trong ba **da xong** va mot **da bi doi
            #    dich**. No gia trong im lang vi ⛔ khong mot con so nao cua no
            #    duoc do lai. ⇒ Trang thai cua bon cong nay la thu **de gia
            #    nhat** trong ca trang, nen no phai la thu **duoc do**.
            #
            # ⭐ `anh_nhip` la cong `A1` do bang mot cau **ai sinh ra anh**:
            #   `actor` mang `tools/` nghia la *"mot NGUOI da go mot lenh"*.
            #   Cong `A1` DAT khi con so nay >= 2 va hai anh cach nhau ~1 gio
            #   ⇒ hom nay no la **1**, va do la con so noi rang bo hen gio
            #   **⛔ chua duoc dang ky** — mot cu bam cua owner, ⛔ khong phai
            #   mot dong ma.
            #
            # ⛔ `position('tools/' in actor) = 0` chu ⛔ khong `LIKE 'tools/%'`:
            #   `dem()` goi `execute(sql)` ⛔ khong kem tham so, va mot dau `%`
            #   trong cau se lam psycopg hieu sai. Cung lop voi loi vua cắn o
            #   phep do nhap: `only '%s' allowed as placeholders`.
            "anh_tong": dem("select count(*) from fls_chup"),
            # ⛔⛔⛔ **`actor = 'nhip@fls'` DUNG BANG, ⛔ khong phai
            #    *"⛔ khong chua tools/"*.** Phep do cu dem CA mot luot go
            #    tay: `tools/nhip_chup.py --that` truoc 09/09 ghi
            #    `nhip@fls` **du ai goi no**, nen toi co the go tay hai lan
            #    cach nhau mot gio va cong `A1` **XANH** trong khi bo hen gio
            #    ⛔ CHUA duoc dang ky. ⇒ Mot cong **TU BAM DUOC**, va no vo
            #    dung dung vao luc no can dung: cau hoi cua `A1` la *"he TU
            #    CHAY chua"*, ⛔ khong phai *"co hai anh chua"*.
            #    ⭐ Nay mot luot go tay mang `nhip@fls(tay)` va ⛔ KHONG duoc
            #      dem — xem `fls/repo/nhip_chup.py::ACTOR_TAY`.
            #
            # ⚠ **Mot cho ⛔ khong chinh xac, va toi khai ra chu ⛔ khong lam
            #   nhu ⛔ khong co:** mot anh `lan='PM'` co truoc co nay
            #   *(09/09 sang)* mang `nhip@fls` **ma no la mot luot GO TAY**.
            #   So chi-them (`INV-I08`) nen toi ⛔ **khong sua** dong ay.
            #   ⇒ `anh_nhip` dang **cong 1 anh go tay**, va he qua la cong
            #     `A1` co the xanh sau **MOT** cu ban that cua bo hen gio thay
            #     vi hai. Chap nhan: mot cu ban that **cung da chung minh** bo
            #     hen gio song. ⛔ Nhung ⛔ khong duoc quen dieu nay.
            # ⭐ (`WO-011 T1`) chuoi actor LAY TU SO *(`danh_muc_actor`)*, ⛔ go
            #   lai: hai cau nay ⛔ bi bai nghiem thu doc bang `ast` nen duoc
            #   phep la f-string.
            "anh_nhip": dem("select count(*) from fls_chup"
                            f" where actor = '{_ACTOR_NHIP}'"),
            # ⭐ `A1` doi hai anh **cach nhau ~1 gio**, ⛔ khong chi hai anh.
            #   Dem so GIO DONG HO khac nhau — cung luat ma `da_chup_gio_nay`
            #   dung, nen hai cho ⛔ khong the lech nhau.
            "anh_nhip_gio": dem(
                "select count(distinct date_trunc('hour', doc_luc))"
                f" from fls_chup where actor = '{_ACTOR_NHIP}'"),
            # ⭐⭐ Tuoi cua anh GIA NHAT — de biet cong `A2` co **cai gi de
            #    do** hay ⛔ khong. Kho chua du 30 ngay tuoi thi ve *"xoa anh
            #    qua han"* dang xanh tren mot tap RONG, va *"xanh tren tap
            #    rong la chua do"*.
            "anh_gia_nhat_ngay": dem(
                "select coalesce(max(extract(day from now() - doc_luc)), 0)"
                "::int from fls_chup"),
            "anh_lan_pm": dem("select count(*) from fls_chup"
                              " where lan = 'PM'"),
            # ⭐ `A3` — so ANH LENH CHI khac nhau. `1` nghia la nua PM cua tac
            #   vu ① **dong bang**; `>=2` nghia la duong nap da chay that.
            "run_pm": dem("select count(distinct run_id) from fls_pm_line"),
            # ⭐ `A2` — mot lan nap tro vao mot anh ⛔ KHONG con. Phai la `0`,
            #   va `0` o day la mot phep do CO NGHIA: neu phep don xoa nham
            #   mot anh **da nap** thi lo ay mat can cu ma ⛔ khong gi bao.
            # ⭐⭐⭐ `B2`/`B3`/`B5` — su kien hang cho do NGUOI bam.
            #   ⛔ Loai `reason`: xem khoi chu thich trong `_cong_moc_b`.
            #
            # ⛔⛔⛔ **Sua 01/10 (`WO-001 T1a`+`T1b`, `KQ-002 F-2`) — LAN THU BA
            #    tien de "chi nguoi ghi loai nay" vo.** ⓵ 10/09: may ghi
            #    `reason` ⇒ loai `reason`. ⓶ 18/09: `QĐ-ITL-143` cho may tu
            #    ghep ghi **2.219** su kien `match` actor `may@fls` ⇒ `B2`·`B3`·
            #    `B5` DAT voi **0** ke toan bam — va cong ⛔ thay vi tien de
            #    *"`match` chi sinh tu mot cu bam trong `F01`"* nam trong chu
            #    thich, ⛔ trong may. ⓷ 01/10: hai su kien UAT cua owner.
            # ⭐ Ba vach, moi vach mot ly do:
            #   · `evt_type <> 'reason'` — nhu cu.
            #   · `actor <> 'may@fls'` — **CHINH hang** `may_ghep.MAY`; chuoi
            #     phai thuan *(bai `KQ-002` doc bang `ast`)* nen `dem_nguoi`
            #     goi `_kiem_hang_may` de soi hai cho con khop nhau.
            #   · `left(reason, 4) <> 'UAT '` — `QĐ-ITL-150 ⓐ` + `10 §6`: moi
            #     dong ghi UAT mang `reason` bat dau `UAT <ngay>`. ⛔ Loc theo
            #     ACTOR *(owner la nguoi that, se lam viec that)*; ⛔ loc
            #     `'(%'` *(ly do mac dinh `(may dien) …` cua `WO-003` la cu
            #     bam NGUOI that ⇒ phai dem)*; ⛔ `'%UAT%'` *(mot ly do NHAC
            #     toi UAT ⛔ phai UAT)*. Ca ba chieu co bai ghim DO.
            # ⚠ Tien trinh may MOI mang actor khac thi lai lot — `WO-001` Rui
            #   ro 2. Luat ma: moi actor may phai la mot hang trong `fls/`, va
            #   cong nay phai biet no. ⛔ Chua co cong canh "actor la ai".
            #
            # ⛔⛔⛔ **Sua 02/10 (`WO-011 T2`·`T4`, `KQ-010 F-2 ⓐⓒ`) — dong tren
            #    la loi bao truoc, va no DUNG.** Do 01/10 khuya: ma co **8** actor
            #    ⛔ phai nguoi *(nay **9** — `HOI-012` cau 1)*, vach tren biet **1**;
            #    UAT nhan bang CHU nen `'uat …'`, `' UAT …'`, `'UAT02/10'` tinh la
            #    nguoi. ⇒ Hai vach nay nay la hai mau **SINH tu so**
            #    `fls/repo/danh_muc_actor.py` *(`sql_ngoai_may` · `sql_khong_uat`)*,
            #    CHEP vao chuoi thuan *(bai `KQ-002`/`KQ-010` doc bang `ast` roi
            #    CHAY no — `HOI-012` cau 2)*; `dem_nguoi` → `_kiem_hang_may` doi
            #    chieu **trung byte** voi so moi lan chay. Them actor may ma quen
            #    cau ⇒ cong ⛔ khong do duoc *(DO)*, ⛔ lang le dem may la nguoi.
            # ⭐ Va cho ho con lai — mot may moi quen khai VAO SO — thi `T3` canh:
            #   `_q_actor_moi` goi ten moi actor ngoai so, cong NO.
            # ⛔ Giu `coalesce(reason, '')`: cu `Xong` cua nguoi ghi `reason NULL`
            #   *(`KQ-010 F-1`, dot bien `M5`)*. ⛔ Giu loc theo LY DO, ⛔ theo
            #   actor owner *(`M4`)*.
            "su_kien_cho_nguoi": dem_nguoi(
                "select count(*) from fls_queue_event where evt_type <> 'reason' "
                "and coalesce(actor, '') <> all (array['cong-ghi@apero.vn', "
                "'cong@apero.vn', 'dung-lai-so@apero.vn', 'may@fls', 'nhip@fls', "
                "'nhip@fls(tay)', 'thu@apero.vn', 'verify-sua-duoc-gi-2@fls', "
                "'verify-sua-duoc-gi@fls']) and coalesce(reason, '') !~* '^[ "
                "\\t\\n\\r\\f\\v\\u00a0\\u3000\\ufeff]*uat([^[:alpha:]]|$)'"),
            "anh_dut": dem(
                "select count(*) from fls_run r where r.chup_id is not null"
                " and not exists (select 1 from fls_chup c"
                " where c.chup_id = r.chup_id)"),
            # ⭐⭐⭐ `A5a` — **so chi duoc co MOT TANG NGUON SONG.**
            #
            # ⛔⛔ Cong nay sinh ra tu mot loi da xay ra that (10/09): so duoc
            #    nap tu `Transaction Mapping L1` *(tang PHAI SINH)* trong khi
            #    duong thiet ke la 60 sheet `R |` *(tang ke toan GO VAO)*. Hai
            #    tang dung hai `source_system`, va `content_key` chua no ⇒
            #    chong trung **MU giua chung**: do duoc **3.694 dong** khop ca
            #    bon khoa nghiep vu ma nam **hai lan** neu nap ca hai.
            #
            # ⛔ Va ⛔ khong cong nao trong `A1`-`A4` hoi cau nay, nen moc `A`
            #   **dong duoc** trong khi so co hai tang.
            "tang_nguon": dem(
                "select count(distinct source_system) from fls_itl"),
            # ⭐⭐⭐ `A5b` — **anh moi nhat moi lan phai CO DUONG VAO SO.**
            #
            # ⛔⛔ Do 10/09: lan `Bank` co **12 anh** trong kho va **0 anh**
            #    duoc nap vao so; so dung yen tu **27/08**. Nhip chay dep moi
            #    gio, va **⛔ khong cong nao noi rang so dang dong bang** —
            #    dung hinh benh *"xanh tren mot cau hoi KHAC"*.
            #
            # ⭐ Dem so GIO tu anh Bank moi nhat den lan nap gan nhat CUA NO.
            #   `-1` = ⛔ chua bao gio nap *(⛔ khong phai `0` — `0` doc nhu
            #   "vua nap xong", va do la mot cau tra loi NGUOC)*.
            "gio_anh_bank_chua_nap": dem(
                "select coalesce((select extract(epoch from"
                " (now() - c.doc_luc))/3600 from fls_chup c"
                " where c.lan = 'Bank'"
                "   and exists (select 1 from fls_run r"
                "               where r.chup_id = c.chup_id)"
                " order by c.doc_luc desc limit 1), -1)::int"),
            # ⭐ `A4` — nap lai ⛔ khong nhan doi, do o **ca hai** be mat.
            "pm_trung": dem(
                "select count(*) from (select run_id, source_row"
                " from fls_pm_line group by run_id, source_row"
                " having count(*) > 1) x"),
            "noi_trung": dem(
                "select count(*) from (select itl_id, pm_line_id"
                " from fls_pm_link group by itl_id, pm_line_id"
                " having count(*) > 1) x"),
            # ⭐⭐ 09/09 — `BA-06 §7 ⓶ ①` ghi *"danh sach N nguon"*. Con so ay
            # go tay thanh **68** tu 08/09 va do lai ngay 09/09 la **69**: mot
            # cau ve **hien trang man hinh** lac hau sau MOT ngay, va ⛔ khong
            # cong nao thay vi `BA-06` chua he co mot phep so nao.
            # ⛔ Dem CA hai: tong va rieng `Bank` — man liet ke TAT CA nguon
            #   (`Mapping Master` cung o trong danh sach), con lan sao ke thi
            #   chi cham `Bank`. Mot con so mot minh se lam nguoi doc tuong
            #   hai thu ay la mot.
            "so_nguon": dem("select count(*) from fls_source"),
            "so_nguon_bank": dem(
                "select count(*) from fls_source where src_type = 'Bank'"),
            # ── ⭐⭐ `CR#11` task `7` (08/09) — ba con so cua BAN KHAI ANH XA.
            #
            # ⛔⛔ **Vi sao them.** Cau *"do song co **9 bo tri cot** khac nhau"*
            # duoc trich o **7 cho** trong ma va tai lieu nhu mot bang chung
            # rang *"doan la sai tien"*. Do lai tren kho 08/09: con so `9` la
            # DUNG, nhung no chi nhin **3/6 truong** (`Date`,`Debit`,`Credit`
            # — xem `tools/do_hinh_dang.py`), con cau chu thi noi *"bo tri
            # COT"*. ⇒ Mot con so DUNG nam trong mot cau SAI, va no di qua
            # **66 phep so** ma ⛔ khong cai nao thay — vi cong canh **CON SO**,
            # ⛔ khong canh **NGHIA cua con so**.
            #
            # ⭐ Cach chua ⛔ khong phai *"can than hon"*: la **dua chinh con so
            #   ay vao cong**, do tu kho, kem **so truong dem tren** — de cau
            #   chu ⛔ khong the tach khoi phep do nua.
            "nguon_khai": dem("select count(distinct source_id) "
                              "from fls_khai_cot"),
            # ⛔ Chi dem ban khai **DANG HIEU LUC** (`version` cao nhat cua
            #    tung nguon). Dem ca ban cu thi mot lan ngan hang doi mau se
            #    lam con so phong len, va no se ke ve **lich su** trong khi cau
            #    van noi ve **hien tai**.
            "bo_tri_6": dem(_Q_BO_TRI % ""),
            "bo_tri_5": dem(_Q_BO_TRI % "where k.truong <> 'Description'"),
        }

    # ⛔ Ghi DAU THOI DIEM, ⛔ KHONG ghi "tuoi". Tuoi la con so ĐỘNG (nhich
    # tung phut) nen chep vao tai lieu la sai ngay hom sau; dau thoi diem la
    # mot SU KIEN, no ⛔ khong gia di. Nguoi doc tu tru ra tuoi.
    if not gio or not gio[0] or not gio[1]:
        raise SystemExit("⛔ khong do duoc: kho ⛔ khong co dau thoi diem cua "
                         "lan nap / anh chup — cong ⛔ khong duoc phep xanh")
    vn_tz = zoneinfo.ZoneInfo("Asia/Ho_Chi_Minh")

    # ── ⭐⭐⭐ `B0` (09/09, `QĐ-ITL-118`) — NAM con so cua chang ①.
    #
    # ⛔⛔ **Vi sao chung o day chu ⛔ khong o mot cong rieng, va vi sao dieu
    # do la ca diem cua `B0`.** Lo trinh `13` §0 ⓵ **co y ⛔ khong ghim** hai
    # con so `584`/`6.577` voi ly do viet ra: *"mot cong chay 40 giay la mot
    # cong SE BI TAT, va mot cong bi tat te hon mot con so ⛔ khong ghim vi no
    # con lam nguoi ta TUONG co canh"*. Ban do cu goi `ung_vien_pm` **7.329
    # lan**. `ds_tu_chung` tra **cung cau tra loi** bang **ba cau** ⇒ ~1 giay
    # ⇒ ghim duoc.
    #
    # ⭐⭐⭐ Va chinh viec no chay duoc moi luc da **bat con so `584` sai**:
    #   luat cua cua GHI cho **68**, ⛔ khong 584. Mot phep do dat trong mot
    #   anh chup se ⛔ khong bao gio tu lat duoc chinh no.
    #
    # ⛔ Goi **CHINH HAM ma cua ghep LO goi** — ⛔ khong dung lai mot cau SQL
    #   thu hai o day: hai ban se lech, va cong se canh mot tap KHAC cai tap
    #   ma mot cu bam thuc su ghep.
    from fls.repo.do_mau_so import do_mau_so, do_phu_pm      # noqa: PLC0415
    from fls.repo.doc_bao_cao import do_phu_hang_cho     # noqa: PLC0415
    from fls.repo.lenh_cho import dem_lenh_cho           # noqa: PLC0415
    from fls.repo.pham_vi import chi_nap_that                # noqa: PLC0415

    with psycopg.connect(dsn_that(), connect_timeout=5) as _c:
        _ms = do_mau_so(_c, chi_nap_that())
        # ⭐⭐ VIEC NGUOI XEM — `799` dong phu 90% TIEN trong TUNG tien te.
        #
        # ⛔⛔ Goi `do_phu_hang_cho` — **chinh phep xep ma man `F01` dung**.
        #    Dung lai mot cau SQL thu hai o day thi cong se canh mot con so
        #    KHAC con so tren man, va ⛔ khong ai thay: hai ban deu *"dung"*.
        #
        # ⛔ Cong `so_dong_phu` cua **tung** tien te, ⛔ khong gop tien lai:
        #   gop hai don vi ra mot con so la dung cai sai da de ra *"310 dong
        #   phu 90%"* (that ra **799**).
        _phu = do_phu_hang_cho(_c, chi_nap_that(), 90)
        # ⭐⭐⭐ PHIA PM — mau so THAT (`QĐ-ITL-122`). ⛔ Goi ham that.
        _pm = do_phu_pm(_c, chi_nap_that())
        # ⛔ Goi HAM THAT — cung phep xep ma lan LENH CHI cua `F01` dung.
        _lc = dem_lenh_cho(_c, chi_nap_that(), 90)
    _ve = {x["ve"]: x for x in _ms["ve"]}
    _vs = {x["ma"]: x for x in _ms["vi_sao"]}
    _tr = _ms["tran"]

    ra = {
        # mau so THAT cua tac vu ①: ve `PS Co`, ⛔ khong ca so
        "ve_ps_co": vn(_ve["ps_co"]["so_dong"]),
        "ve_ps_co_noi": vn(_ve["ps_co"]["da_noi"]),
        "ve_ps_co_chua": vn(_ve["ps_co"]["chua_noi"]),
        "phu_ps_co": _ve["ps_co"]["ty_le_noi_pct"],
        "phu_ps_no": _ve["ps_no"]["ty_le_noi_pct"],
        # ⭐ so dong cua ghep LO nhan duoc NGAY — luat cua cua GHI
        "tu_chung": vn(_ms["tu_chung"]),
        # ⭐⭐⭐ TRAN CUNG — doc tu `do_mau_so`, ⛔ KHONG do lai o day.
        #
        # ⛔⛔ Ban dau (sang 09/09) toi dat phep do nay **ngay trong cong**:
        #    hai cau SQL rieng. Nghia la kho co **HAI ban su that** ve mot con
        #    so ma ca mot moc phu thuoc — mot ban cho cong, va ⛔ khong ban nao
        #    cho man hinh hay cua API. Dung lop loi da lam *"584 vs 68"*.
        #    ⇒ Da don ve `fls/repo/do_mau_so.py::_tran`, va cong **doc** no.
        "pm_anh_tong": vn(_tr["dong_lenh_trong_anh"]),
        "pm_da_dung": vn(_tr["dong_lenh_da_dung"]),
        "pm_ranh": vn(_tr["dong_lenh_con_ranh"]),
        "tran_dong": vn(_tr["toi_da_noi_duoc"]),
        "tran_pct": _tr["tran_pct"],
        # ⭐⭐ Con so noi DUNG phan viec da lam: `da_noi / tran`
        "phu_tren_tran": _tr["phu_tren_tran_pct"],
        # ⭐⭐ VIEC NGUOI XEM — Σ `so_dong_phu` cua TUNG tien te
        "viec_nguoi_xem": vn(sum(r["so_dong_phu"] or 0 for r in _phu)),
        # ══ ⭐⭐⭐ PHIA PM (`QĐ-ITL-122`) — mau so THAT cua viec ghep ══
        #
        # ⛔⛔ Owner chot *"Trans map vao PM; ⛔ ko can question cac Trans
        #    khong duoc map"* ⇒ moi con so do phu tu 27/08 den 09/09 do **SAI
        #    PHIA**. Chung ghim o day de con so cu ⛔ khong lang le song lai.
        "pm_ty_le": _pm["ty_le_pct"],
        "pm_phieu": vn(_pm["phieu"]),
        "pm_phieu_da": vn(_pm["phieu_da_co"]),
        "pm_ghep_ngay": vn(_pm["ghep_duoc_ngay"]),
        "pm_chua_duyet": vn(_pm["chua_co_va_chua_duyet"]),
        # ⭐⭐⭐ BA con so PHIEU — va toi da viet SAI mot trong ba vao BON
        #    tep tai lieu truoc khi kip bat: `510` la *"phieu ⛔ chua noi gi
        #    ca"*, con *"viec con lai"* la **698**. Chenh **188** phieu **da
        #    noi mot phan** — loai **de bo sot nhat**. ⇒ Ghim CA BA.
        "pm_phieu_chua_noi_gi": vn(_pm["phieu_chua_noi_gi"]),
        "pm_phieu_con_dong_chua": vn(_pm["phieu_con_dong_chua"]),
        "pm_phieu_mot_nua": vn(_pm["phieu_mot_nua"]),
        # ⭐⭐ `69` dong lenh phu 90% TIEN — con so *"viec nguoi xem"* cua
        #    dung phia. ⛔ Do bang `dem_lenh_cho` (ham man `F01` dung).
        "pm_phu_90": vn(sum(r["so_dong_phu"] or 0 for r in _lc)),
        # ⭐⭐⭐ KHUYET TAT GIAO DIEN, do bang cach DEM BANG TUYEN.
        #
        # ⛔⛔ `GAP-SCR-14`: **⛔ khong co mot cua nao** hoi *"lenh chi nao
        #    ⛔ chua tim duoc tien"* — tuc dung cau hoi cua viec. Con so `0`
        #    nay la **phep do cua mot cai THIEU**, va no phai o trong cong:
        #    khi ai do mo cua ay thi `0 -> 1` va cong DO ⇒ ai do phai vao
        #    sua CAU trong tai lieu. ⛔ Mot cai thieu ⛔ khong duoc phep im.
        **_dem_tuyen(),
        # ⭐ nut that THAT: co ma ma ⛔ KHONG dong PM nao mang
        "thieu_pm": vn(_vs["PM_khong_mang_ma_nay"]["so_dong"]),
        # hai nhom NGUOC CHIEU lam nen con so "lech 353"
        "noi_nhan_cu": vn(_ms["lech"]["da_noi__nhan_con_UNMAPPED"]),
        "du_chua_noi": vn(_ms["lech"]["du_phan_loai__chua_noi"]),
        "bi_che": vn(_ms["lech"]["tong_dong_bi_che"]),
        "dau_so": gio[0].astimezone(vn_tz).strftime("%d/%m %H:%M"),
        "dau_anh": gio[1].astimezone(vn_tz).strftime("%d/%m %H:%M"),
        "bang_view": str(len(TABLES)),
        "test_tong": str(td["tong_test"]),
        "test_module": str(sum(h["test"] for h in td["module"])),
        "test_ngoai": str(td["tong_test"] - sum(h["test"] for h in td["module"])),
        "dong_tong": vn(sum(h["dong"] for h in td["module"])),
        "tien_do": f"{td['tien_do_pct']:.0f}",
        # ⭐⭐ Khuon OUTPUT cua moc `D`: 64 cot sheet `ITL Ledge`, FLS luu
        #    18. Do tu `oracle/ledge_spec` — **ban khai duy nhat**, ⛔
        #    khong go tay mot con so nao vao tai lieu.
        "ledge_cot": str(len(_ls.LEDGE_COLS)),
        "ledge_luu": str(len(_ls.COT_LUU)),
        "ledge_khong_luu": str(len(_ls.COT_KHONG_LUU)),
        # ⭐ Hai TY LE cua moc `B`. ⛔ Tinh o DAY chu ⛔ khong go tay: mot
        #    phan tram go tay canh hai con so duoc ghim la dung cho ma
        #    `GAP-DOC-08` song — so dung, cau sai, cong xanh.
        "ty_le_ghep": _phan_tram(kho["itl_ghep"], kho["so_dong"]),
        "ty_le_chua_ghep": _phan_tram(
            kho["itl_chua_ghep"], kho["so_dong"]),
        "tong_trong_so": str(td["tong_trong_so"]),
        # ⛔⛔ **`Σ gop` va **tien do %** la HAI DAI LUONG — va cong nay tung
        #    lan chung.** Ban truoc gan `gop_tong = tien_do_pct`, va no **dung
        #    tinh co** suot 12 ngay vi `Σ trong so` **dung bang 100** nen
        #    `Σ gop` = `Σ gop / 100 × 100`. Ngay 09/09 `Σ trong so` len **106**
        #    va hai con so tach doi: `Σ gop = 87,00` con tien do = `82,1%`.
        #
        # ⇒ Do RIENG. ⚠ Va no la mot loi cua CONG, ⛔ khong phai cua tai lieu:
        #   con so trong tai lieu **dung**, cong so no voi mot con so KHAC.
        "gop_tong": f"{sum(h['gop_pct'] for h in td['module']):.2f}"
                    .replace(".", ","),
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
        # ⭐⭐ NGAY cua **dung commit ay**, ⛔ khong phai hom nay.
        #
        # ⛔⛔ Vi sao ⛔ khong lay `date.today()`: cau tai lieu la *"so trong ban
        # ve nay DO ngay X tren commit Y"* — hai ve cua mot cau khai. Ghim theo
        # **hom nay** thi cong DO **moi ngay** ke ca khi ⛔ khong ai sua gi, va
        # mot cong do moi ngay la mot cong **se bi tat** *(bai hoc `doc_cong`
        # 15,6s)*. Ghim theo ngay cua commit thi no chi doi khi `fls/` doi —
        # dung luc con so that su duoc do lai.
        "ngay_commit_vn": _chay("git", "log", "-1", "--date=format:%d/%m/%Y",
                                "--format=%ad", "--", "fls/").strip(),
        # ⭐ So module — DEM tu `tien_do.py`, ⛔ khong go `9` vao mau regex.
        "so_module": str(len(td["module"])),
        # ⭐⭐ Hai con so cua SO DO ban ve 12. ⛔⛔ So do ay ghi *"XONG HAN · 5
        #    khoi"* + *"DANG LAM · 4 khoi"* tu 24/08 va **⛔ chua he duoc do**:
        #    ngay 09/09 module thu muoi ra doi thi ve *"dang lam"* thanh **5**
        #    va so do noi sai — trong khi bang thanh ngay duoi no thi dung, vi
        #    bang ay CO cong canh. Cung hinh benh `GAP-DOC-08`, o mot be mat
        #    ⛔ khong ai nghi la mot be mat: mot **so do**.
        "module_xong": str(sum(1 for h in td["module"]
                               if h["xong_pct"] == 100)),
        "module_dang": str(sum(1 for h in td["module"]
                               if h["xong_pct"] < 100)),
        # ⛔⛔ Ty le nay tinh o DAY, ⛔ khong trong `khai()`. Ban dau toi
        #    tinh no ngay trong ban khai phep so — va bai
        #    `test_MOI_MAU_DICH_DUOC` **DO NGAY**: bai ay dung mot `may` GIA
        #    de kiem *"moi mau dich duoc va so nhom khop so gia tri"*, nen
        #    `so_module` la `0` va phep chia NO. ⇒ Ban khai phep so phai la
        #    **du lieu tro**, ⛔ khong duoc TINH gi — ⛔ khong thi no ⛔ khong
        #    kiem duoc ma ⛔ khong co kho that.
        "ty_le_module_xong": str(round(
            100 * sum(1 for h in td["module"] if h["xong_pct"] == 100)
            / len(td["module"]))),
        **_cong_moc_a(kho),
        **_cong_moc_b(kho),
        **{k: vn(v) for k, v in kho.items()},
        # ⭐ `WO-011 T3` — ⛔ mot con so: danh sach `[actor, thao_tac, dong]`
        #   ngoai so, chep ra chuoi de `do_may` giu kieu `dict[str, str]`.
        "actor_moi": json.dumps(actor_moi, ensure_ascii=False),
    }
    for h in td["module"]:
        ra[f"dong_{h['ma']}"] = vn(h["dong"])
        ra[f"test_{h['ma']}"] = str(h["test"])
        # ⭐⭐ 09/09 — them cot `xong`. ⛔⛔ **Vi sao no phai vao cong:** hai
        # con so `dong`/`test` duoc ghim tu 28/08, con cot `xong` thi ⛔
        # KHONG — nen no lac hau **trong im lang** tu 03/09 *(`api` 92 ·
        # `web` 70)* qua ca dot dung `F04` + 9 tuyen moi, va cong van XANH
        # vi hai con so canh no thi dung. Do 09/09: `api` 95 · `web` 85.
        # ⚠ Day dung la hinh benh `GAP-DOC-08` *(cong canh SO, ⛔ khong canh
        #   NGHIA)* nhung o mot dang xau hon: **cong canh MOT PHAN cua mot
        #   dong**, va phan ⛔ khong canh thi nam ngay canh phan co canh.
        ra[f"xong_{h['ma']}"] = str(h["xong_pct"])
        ra[f"file_{h['ma']}"] = str(h["file"])
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
        # ── ⭐ BA-06 §7 ⓶ ① — so nguon man `F04` liet ke
        Muc("BA-06 · so nguon F04", BA06,
            r"danh sách \*\*(\d+) nguồn\*\* \*\(`fls_source`, đo [0-9/]+ "
            r"— trong đó \*\*(\d+)\*\*",
            (may["so_nguon"], may["so_nguon_bank"])),
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
        # ⛔⛔ **So MODULE nay do, ⛔ khong go tay** — them 09/09.
        #    Ban truoc mau ghim cung chu `trong 9 module`, va khi module thu
        #    muoi (`xuat`) ra doi thi cong bao **khop 0 lan** ⇒ DO. Cong DO
        #    dung *(cau van da doi)*, nhung ly do no do la mot con so **go tay
        #    NAM TRONG CHINH CONG** — tuc cong nay cung mac benh no canh.
        Muc("test · tong va trong module", DASH,
            r"\*\*(\d+) test\*\* \*\((\d+) trong (\d+) module \+ (\d+) ngoài\)\* "
            r"trên \*\*([\d.]+) dòng\*\*",
            (may["test_tong"], may["test_module"], may["so_module"],
             may["test_ngoai"], may["dong_tong"])),
        # ── ⭐⭐ 08/09 — BAN KHAI ANH XA. Xem ly do dai o `do_may()`.
        #    ⛔ Ba con so trong MOT phep so, CO Y: chung phai di cung nhau.
        #    Tach ra thi mot cai doi ma hai cai kia dung yen, va cau van se
        #    lai noi mot dieu ⛔ khong con dung — dung benh vua chua.
        Muc("kho · ban khai anh xa", DASH,
            r"\*\*(\d+) dòng chảy\*\* có bản khai trong kho[^|]*?"
            r"\*\*(\d+) bố cục cột\*\* khác nhau[^|]*?"
            r"\*\*(\d+)\*\* nếu chỉ đếm \*\*5 trường",
            (may["nguon_khai"], may["bo_tri_6"], may["bo_tri_5"])),
        Muc("nhanh · commit", DASH,
            r"`feat/p2-oracle-parity` — `([0-9a-f]{7})`", (may["commit"],)),
        # ── ban ve kien truc: khoi "Dau thoi diem"
        # ⛔⛔ **NAM con so trong MOT phep so, va do la co y** — them 09/09 sau
        #    khi ba trong nam vua **gia trong im lang** ma cong ⛔ KHONG bat
        #    duoc: ngay `07/09` dung canh mot commit cua `09/09` · `8 luat ranh
        #    gioi` khi luat thu chin da co · `85/66` khi cong co 85 phep so.
        #
        # ⭐ Vi sao ghim CA NAM trong mot phep: chung la **mot cau khai** —
        #   *"so nay do luc nao, tren ban nao, va bang may cong nao"*. Tach ra
        #   thi mot cai doi ma bon cai kia dung yen, va cau van se noi mot dieu
        #   ⛔ khong con dung. Dung benh `GAP-DOC-08` vua chua.
        Muc("ban ve · chan trang", BANVE,
            r"đo ngày <strong>(\d{2}/\d{2}/\d{4})</strong>[^<]*"
            r"<code>feat/p2-oracle-parity</code>, commit "
            r"<code>([0-9a-f]{7})</code>\. <strong>(\d+) phép thử xanh · "
            r"(\d+) luật ranh giới, 0 vi phạm",
            (may["ngay_commit_vn"], may["commit"], may["test_tong"],
             may["lint_kept"])),
        # ── 08_MIGRATION_ROADMAP buoc 4: version cua 3 file DEV
        Muc("roadmap · DEV-03 version", ROADMAP,
            # ⛔ Neo cu ghim ca **so pha** ("roadmap 7 pha") ⇒ them pha `P7`
            #    la mat neo, du con so version van dung. Phep do nay do
            #    **VERSION**; so pha la mot su that KHAC, ⛔ khong gop vao day.
            r"`DEV-03` roadmap[^|]*?\*\*v([0-9.]+)\*\*",
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
        # ══ ⭐⭐⭐ `B0` — MAU SO tac vu ① (them 09/09, `QĐ-ITL-118`) ══
        #
        # ⛔⛔ **Muoi con so trong MOT phep so, va do la co y.** Chung la mot
        # cau khai duy nhat: *"mau so la ve `PS Co`, no bang bao nhieu, phu bao
        # nhieu, cua ghep LO don duoc bao nhieu, va nut that o dau"*. Tach ra
        # thi mot cai doi ma chin cai kia dung yen, va cau van se noi mot dieu
        # ⛔ khong con dung — dung benh `GAP-DOC-08`.
        #
        # ⭐ Va day la cho hai con so `13_LO_TRINH` §0 ⓵ **co y ⛔ khong ghim**
        #   *(vi ban do cu chay 40 giay)* cuoi cung **duoc ghim**: phep do moi
        #   chay ~1 giay bang ba cau. Dung viec `B0` duoc dat ra de lam.
        Muc("§1 · mẫu số tác vụ ①", DASH,
            r"Vế \*\*`PS Có`\*\*: \*\*([\d.]+)\*\* dòng · "
            r"\*\*([\d.]+)\*\* đã nối lệnh chi · ⛔ \*\*([\d.]+)\*\* chưa nối "
            r"⇒ độ phủ \*\*([\d,]+)%\*\*\. Vế `PS Nợ` chỉ \*\*([\d,]+)%\*\*[^|]*?"
            r"nhận ngay \*\*([\d.]+)\*\* dòng[^|]*?"
            r"⛔ \*\*([\d.]+)\*\* dòng \*\*có mã chuẩn hoá được[^|]*?"
            r"HIỆU\*\* của \*\*([\d.]+)\*\* dòng[^|]*?"
            r"trừ \*\*([\d.]+)\*\* dòng[^|]*?"
            r"che đi ([\d.]+) dòng",
            (may["ve_ps_co"], may["ve_ps_co_noi"], may["ve_ps_co_chua"],
             may["phu_ps_co"], may["phu_ps_no"], may["tu_chung"],
             may["thieu_pm"], may["noi_nhan_cu"], may["du_chua_noi"],
             may["bi_che"])),
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
            r"`03` \*\*v([0-9.]+)\*\*[^|]*? · `04`",
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
        # ⛔⛔ **LAN THU BA cung mot lop loi — 08/09.** Neo cu la
        #   `` `06` **vX** *(+§3c `` : no bam vao **CHU GHI CHU**, nen no tuot
        #   ngay khi `06` duoc ghi chu ve cai MOI (`+§7 ⓶b`). Va no tuot theo
        #   kieu **⛔ khong do duoc** — dung hang nguy hon mot phep so lech.
        #
        # ⚠ Hai lan truoc da chua dung cach nay roi (`BA-05` neo vao o dau
        #   hang; `BA-07` neo vao ma tep) va **⛔ khong ai go luat ra**: ghi
        #   chu la thu ⛔ KHONG BAO GIO duoc lam mot phan cua neo — no doi moi
        #   dot, con `ma tep` thi ⛔ khong.
        #
        # ⛔ Va day ⛔ KHONG phai noi long cong (`R-A5`): phep so van hoi dung
        #   cau cu — *"§8 co dang ghi version THAT cua tep ⛔ khong"* — va van
        #   DO neu §8 quen theo. Chi cai NEO doi.
        Muc("master · §8 version BA-06", MASTER,
            r"`06` \*\*v([0-9.]+)\*\*",
            (v("02_BA/06_SCREEN_SPEC.md"),)),
        Muc("master · §8 version BA-07", MASTER,
            # ⚠ Neo cu bam vao *"... · `09` v0.4 ·"* — mot cho ⛔ khong
            #   noi len no dang do CAI GI, va no vo ngay khi `07` duoc
            #   ghi chu them. Neo lai vao **chinh ma tep** nhu cac phep
            #   so khac.
            # ⛔ 08/09 — neo *"`+2 mã lỗi`"* cung la CHU GHI CHU, va nay no
            #   cung tuot. `07` xuat hien **HAI lan** trong §8 (`ORCH-07`
            #   v1.5 · `BA-07`) nen ⛔ khong neo bang ma tep mot minh duoc.
            #   ⇒ Neo bang **CHUOI**: cai `07` nam sau `06` **trong cung mot
            #   o** thi la `07` cua kit `02_BA/`. Hai thu do la **ma tep**,
            #   ⛔ khong phai ghi chu ⇒ chung ⛔ khong doi theo dot.
            r"`06` \*\*v[0-9.]+\*\*[^|]*?`07` \*\*v([0-9.]+)\*\*",
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
        # ⛔ `adapters` neo bang mot **so** (`6 bộ nạp`) — va so ay doi khi
        # them mot bo nap (`sao_ke` = `F04`, 07/09) ⇒ cong **mat neo** va bao
        # *"mau khop 0 lan"*. ⭐ Neo dung mot chu **⛔ khong doi**, con so thi
        # de phep so canh. Cung lop voi hai lan re-anchor truoc do.
        "adapters": "bộ nạp", "api": "cửa vào ra", "web": "4 màn hình",
        # ⭐ module thu 10 (09/09) — neo bang mot CHU ⛔ khong doi.
        "xuat": "đưa số ra ngoài",
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
            rf"\| `{ma}`[^|]*{re.escape(nhan)}[^|]*\| [^|]+ \| ([\d.]+) \|"
            rf" (\d+) \| (?:◐ )?(?:\*\*)?(\d+)%",
            (may[f"dong_{ma}"], may[f"test_{ma}"], may[f"xong_{ma}"])))

    # ⭐⭐⭐ CHIN CAPTION cua BAN VE 12 — them 2026-09-09.
    #
    # ⛔⛔ **Day la be mat GIA NHAT cua ca bo tai lieu, va no chua he duoc do.**
    #    Do 09/09: caption khoi `repo` ghi **1.454 dong · 124 phep thu** trong
    #    khi may do **3.706 · 321** — lech **2,5 lan**. Khoi `api` ghi
    #    **1.036 · 108 · 75%** trong khi may do **3.159 · 261 · 95%**.
    #
    # ⭐ Chung song sot vi ban ve **CO** 5 cho ghim *(commit · test tong · thanh
    #   api)* nen trang trong y het mot trang duoc canh — con phan than thi
    #   ⛔ khong. Mot cong canh MOT PHAN cua mot trang la mot cong **noi lon**
    #   ve ca trang.
    # ⭐ 09/09: MUOI caption. Ban ve ve 9 khoi tren 10 module ⇒ khoi thu muoi
    #    (`xuat`) **⛔ khong co mat tren trang ma nguoi quyet doc** — mot be mat
    #    ⛔ khong ai canh, dung lop loi vua chua o day.
    for ma, so, ten in ((("db", 1, "Khuôn dữ liệu"), ("contract", 2, "Hợp đồng 14 trường"),
                         ("canon", 3, "Khuôn 36 cột"), ("ledger", 4, "Lớp ghi sổ"),
                         ("oracle", 5, "Thước chuẩn"), ("repo", 6, "Cửa duy nhất vào kho"),
                         ("adapters", 7, "Bảy bộ nạp nguồn"), ("api", 8, "Cửa vào ra"),
                         ("web", 9, "Bốn màn hình"),
                         ("xuat", 10, "Đưa số ra ngoài"))):
        m.append(Muc(
            f"bản vẽ · caption khối {so} ({ma})", BANVE,
            rf"Khối {so} · {re.escape(ten)} — <strong>(\d+)%</strong>"
            rf" · (\d+) tệp · ([\d.]+) dòng · (\d+) phép thử",
            (may[f"xong_{ma}"], may[f"file_{ma}"], may[f"dong_{ma}"],
             may[f"test_{ma}"])))

    # ══ ⭐⭐⭐ TEP MOC (`09_MILESTONES_HAI_TAC_VU`) — them 2026-09-09 ══
    m += [
        # `§2 ⓶` — bang do phu mapping cua TAC VU ①
        Muc("mốc · độ phủ mapping", MOC,
            r"\| Dòng tiền trong sổ \| \*\*([\d.]+)\*\*",
            (may["so_dong"],)),
        Muc("mốc · dòng ĐÃ ghép", MOC,
            r"ghép được về lệnh chi\*\* \| \*\*([\d.]+)\*\* · \*\*([\d,]+)%\*\*",
            (may["itl_ghep"], may["ty_le_ghep"])),
        Muc("mốc · dòng CHƯA ghép", MOC,
            r"CHƯA ghép\*\* \| ⛔ \*\*([\d.]+)\*\* · \*\*([\d,]+)%\*\*",
            (may["itl_chua_ghep"], may["ty_le_chua_ghep"])),
        # `§3 ⓶` — hai con so DANG LA 0 cua TAC VU ②
        # ⭐⭐⭐ `2026-09-18` — MAU NAY VUA HONG DUNG NHU CHU THICH DUOI
        #    DAY DA CANH BAO, va no hong vao **dung ngay con so bat dau
        #    co nghia**: `QĐ-ITL-143` ghi **4.424** but toan goi y dau
        #    tien, `dem()` `vn()` no thanh `"4.424"`, va `(\d+)` ⛔ khong
        #    nhan dau cham ⇒ **khop 0 lan**. Cong bao *"⛔ khong do
        #    duoc"* — dung, va ly do nam o **CHINH CONG**.
        # ⇒ Noi rong thanh `[\d.]+`, y het `su_kien_cho` ngay duoi.
        Muc("mốc · bút toán sửa THẬT", MOC,
            r"`fls_journal`\)\* \| ⛔ \*\*([\d.]+)\*\*",
            (may["but_toan_sua"],)),
        # ⛔⛔ Mau nay tung la `(\d+)`, va no **im lang hong** ngay 11/09:
        #    con so vuot `1.000` nen tai lieu viet `108.128` *(dau cham kieu
        #    VN, dung loi ca bo)*, con mau thi ⛔ khong nhan dau cham ⇒ **khop
        #    0 lan**. Cong bao *"⛔ khong do duoc"* — dung, nhung ly do nam o
        #    **CHINH CONG**, ⛔ khong o tai lieu.
        #
        # ⇒ Mot mau viet cho luc con so con la `0` se hong vao dung ngay no
        #   thoi la `0` — tuc dung ngay no bat dau co nghia.
        #
        # ⚠ Va `dem()` DA `vn()` san *(tra `'108.128'`)*, nen chi phai noi
        #   rong MAU — ⛔ khong dinh dang lai gia tri. Toi vua suyt boc them
        #   mot `vn(int(...))` va no NO ngay: `int('108.128')`.
        Muc("mốc · sự kiện hàng chờ THẬT", MOC,
            r"`fls_queue_event`\)\* \| ⛔ \*\*([\d.]+)\*\*",
            (may["su_kien_cho"],)),
        # `§4 ⓵` — khuon OUTPUT cua moc `D`
        Muc("mốc · khuôn 64 cột ITL Ledge", MOC,
            r"`oracle/ledge_spec`\)\* \| \*\*(\d+)\*\*",
            (may["ledge_cot"],)),
        Muc("mốc · số cột FLS LƯU", MOC,
            r"FLS \*\*LƯU\*\* \| \*\*(\d+)\*\*",
            (may["ledge_luu"],)),
        Muc("mốc · số cột FLS KHÔNG lưu", MOC,
            r"FLS ⛔ \*\*không lưu\*\* \| \*\*(\d+)\*\*",
            (may["ledge_khong_luu"],)),
        # ⭐⭐ `WO-011 T7` (02/10) — cong chung #13: ba so cua §7 dong `B`.
        #
        # ⛔⛔ `fls-ba` chep `58,1%` · `1.601` · `826` vao bang moc §7 ngay
        #    01/10 khuya *(`KQ-010 F-4`)* — cung ba so ma ban ve 13 ghim o
        #    *"Lenh chi da tim duoc tien"* + *"bang viec con lai"*. Mot so song
        #    chep o >=2 tep ma ⛔ co phep so la dung cai `09` cu da lam: chep
        #    `64,3%` · `1.345`/`698` ngay 09/09 roi gia **22 ngay**.
        # ⭐ Neo vao **dau hang** *(`| **`B`** Mapping | ① |`)* + chu bao quanh
        #   tung so — ⛔ vao ngay/gio trong ngoac *(gio anh hieu luc doi moi gio)*.
        Muc("mốc · §7 dòng B · phía PM", MOC,
            r"\| \*\*`B`\*\* Mapping \| ① \| ⭐ \*\*([\d,]+)%\*\* dòng lệnh "
            r"đã có tiền[^|]*?việc thật ⛔ \*\*([\d.]+)\*\* dòng \*/\* "
            r"\*\*([\d.]+)\*\* phiếu",
            (may["pm_ty_le"], may["pm_ranh"], may["pm_phieu_con_dong_chua"])),
    ]

    m += [
        # ══ ⭐⭐⭐ BAN VE 13 — "Bon moc · cong nao da dong" (them 09/09) ══
        #
        # ⛔⛔⛔ **Day la trang ma owner doc de RA QUYET DINH, nen no la trang
        #    ⛔ khong duoc phep gia.** Tien le ngay canh no: bang *"Buoc tiep"*
        #    o chan trang dung nguyen **16 ngay** voi ba viec cua 24/08 — hai
        #    da xong, mot da mat dich — trong khi chin con so tien do ngay tren
        #    thi tuoi, vi chung CO cong do. ⇒ Moi con so cua ban ve 13 phai co
        #    mot phep so, ngay tu luc no duoc viet.
        # ⭐ Chan trang ban ve: *"N anh chup · M dong lenh"*. ⛔ Cau nay tung
        #   ghi `3.703` — con so cua MOT anh duy nhat ngay 27/08 — va no gia
        #   trong im lang khi kho co anh thu hai, trong khi cung con so ay o
        #   `00_MASTER_INDEX` thi tuoi vi cho do **co** mot phep so.
        Muc("bản vẽ · ảnh chụp lệnh chi", BANVE,
            r"<strong>(\d+) ảnh chụp · ([\d.]+) dòng lệnh</strong>",
            # ⚠ `run_pm`, ⛔ KHONG `anh_lan_pm`: luot nap 27/08 co truoc khi
            #   lan anh chup ra doi nen no ⛔ khong co dong `fls_chup`, nhung
            #   no **la** mot lan doc lenh chi. Dem theo `run_id` thi ca hai
            #   duoc tinh — va do la dieu cau van dang noi.
            (may["run_pm"], may["anh_chup"])),
        # ⭐ Cung ba con so ay o `06_DASHBOARD` §1 — *"trang thai duy nhat"*.
        #   ⛔ Ghim ca ba cho no xuat hien: mot con so tong dung mot cho ma
        #   sai cho khac la dung cach bo tai lieu **noi nguoc nhau**, va bai
        #   hoc `doc_set_silent_drift` noi ro no ⛔ khong tu bao.
        Muc("dashboard · cổng mốc A", DASH,
            r"MÁY ĐẾM: `(\d+)` đạt · `(\d+)` một nửa · `(\d+)` chưa\*\*"
            r" \*\(`tools/kiem_so_song\.py::_cong_moc_a`",
            (may["moc_a_dat"], may["moc_a_nua"], may["moc_a_chua"])),
        Muc("dashboard · ảnh nhịp trên tổng ảnh", DASH,
            r"\*\*`(\d+)`\*\* ảnh do nhịp sinh trên \*\*`(\d+)`\*\* "
            r"ảnh trong kho",
            (may["anh_nhip"], may["anh_tong"])),
        # ⭐⭐⭐ MOC `B` — ghim de con so `1 · 1 · 3` ⛔ khong the gia.
        #   ⛔ ⛔ Khong dat ngay thang vao mau: mot ngay trong mau se lam
        #     cong DO moi khi tai lieu duoc doc lai vao ngay khac, va luc ay
        #     nguoi ta se **noi long mau** chu ⛔ khong sua tai lieu.
        Muc("dashboard · cổng mốc B", DASH,
            r"MÁY ĐẾM: `(\d+)` đạt · `(\d+)` một nửa · `(\d+)` chưa\*\*"
            r" \*\(`_cong_moc_b`",
            (may["moc_b_dat"], may["moc_b_nua"], may["moc_b_chua"])),
        Muc("mốc · cổng mốc B", MOC,
            r"MỐC `B` ĐÃ ĐẠT CHƯA — máy đếm trên kho THẬT: "
            r"\*\*`(\d+)` đạt · `(\d+)` một nửa · `(\d+)` chưa\*\*",
            (may["moc_b_dat"], may["moc_b_nua"], may["moc_b_chua"])),
        # ⛔⛔ NGAY ⛔ KHONG duoc ghim cung trong mau neo. Ban dau mau nay viet
        #   `đo 09/09 trên kho THẬT` — va ngay 14/09, khi mot cong that su
        #   TUT va toi sua lai ngay do cho dung, **mau khop 0 lan** ⇒ cong
        #   noi *"⛔ khong do duoc"*. Do la hanh vi DUNG cua cong, nhung no
        #   chan dung cai luc no can do nhat.
        # ⇒ Cung mot lop loi voi `(\d+)` viet hoi con so con la `0`: mot mau
        #   viet cho MOT THOI DIEM se hong vao dung ngay thoi diem ay qua di.
        Muc("mốc · cổng mốc A", MOC,
            r"đo \d\d/\d\d trên kho THẬT: \*\*(\d+) đạt · (\d+) một nửa · "
            r"(\d+) chưa\*\*",
            (may["moc_a_dat"], may["moc_a_nua"], may["moc_a_chua"])),
        Muc("bản vẽ 13 · tổng kết cổng mốc A", BANVE,
            r'<span class="k">Mốc 1 · sáu cổng: đạt · một nửa · chưa</span>\s*'
            r'<p class="v num">(\d+) · (\d+) · (\d+)</p>',
            (may["moc_a_dat"], may["moc_a_nua"], may["moc_a_chua"])),
        # ⭐ The MOC 2 cua ban ve — ghim NGAY khi them, ⛔ khong de sau.
        #   ⛔⛔ Toi vua go tay `1 · 1 · 3` vao ban ve, va do **dung cai
        #     benh** toi vua go bo o hai cho khac trong cung mot luot: mot
        #     con so go tay canh mot ket luan la mot cho **gia trong im
        #     lang**. ⇒ Ghim truoc khi ket thuc luot, ⛔ khong ghi vao mot
        #     danh sach viec.
        Muc("bản vẽ 13 · tổng kết cổng mốc B", BANVE,
            r'<span class="k">Mốc 2 · năm cổng: đạt · một nửa · chưa</span>\s*'
            r'<p class="v num">(\d+) · (\d+) · (\d+)</p>',
            (may["moc_b_dat"], may["moc_b_nua"], may["moc_b_chua"])),
        Muc("bản vẽ 13 · ảnh nhịp · tổng ảnh", BANVE,
            r'<span class="k">Ảnh do NHỊP sinh · tổng ảnh</span>\s*'
            r'<p class="v num">(\d+) · (\d+)</p>',
            (may["anh_nhip"], may["anh_tong"])),
        Muc("bản vẽ 13 · ảnh lệnh chi khác nhau", BANVE,
            r'<span class="k">Ảnh lệnh chi khác nhau trong kho</span>\s*'
            r'<p class="v num">(\d+)</p>', (may["run_pm"],)),
        # ⭐⭐⭐ Con so quan trong nhat cua ca ban ve — ghim CA HAI cho no
        #    xuat hien *(the o dau, va dong TRAN o cuoi bang)*.
        Muc("bản vẽ 13 · trần độ phủ", BANVE,
            r'<span class="k">Trần của cách đo CŨ — nay chỉ còn là biên bản</span>\s*'
            r'<p class="v num">([\d,]+)%</p>', (may["tran_pct"],)),
        # ⛔⛔ **Bay con so trong MOT phep so, va do la co y.** Chung la mot
        #    cau khai duy nhat: *"mau so bang bao nhieu, da noi bao nhieu,
        #    nguyen lieu con bao nhieu, nen TRAN o dau"*. Tach ra thi mot cai
        #    doi ma sau cai kia dung yen — va cau van se noi mot dieu ⛔ khong
        #    con dung, dung benh `GAP-DOC-08`.
        Muc("bản vẽ 13 · bảng trần cứng", BANVE,
            r"<td class=\"n\"><strong>([\d.]+)</strong></td><td>Mẫu số thật"
            r"[\s\S]*?<td class=\"n\"><strong>([\d.]+)</strong></td><td>Độ phủ hôm "
            r"nay: <strong>([\d,]+)%</strong>"
            r"[\s\S]*?<td class=\"n\"><strong>([\d.]+)</strong></td><td>Toàn bộ "
            r"nguyên liệu"
            r"[\s\S]*?<td class=\"n\"><strong>([\d.]+)</strong></td><td>Một dòng "
            r"lệnh đã ghép"
            r"[\s\S]*?<td class=\"n\"><strong>([\d.]+)</strong></td><td>Số dòng "
            r"tiền tối đa"
            r"[\s\S]*?<td class=\"n\">⛔ <strong>([\d.]+)</strong></td><td>⛔ "
            r"<strong>([\d,]+)%</strong>",
            (may["ve_ps_co"], may["ve_ps_co_noi"], may["phu_ps_co"],
             may["pm_anh_tong"], may["pm_da_dung"], may["pm_ranh"],
             may["tran_dong"], may["tran_pct"])),
        # ⭐ `3.772` con xuat hien mot lan nua trong o cong `A3`
        Muc("bản vẽ 13 · cổng A3 số dòng lệnh", BANVE,
            r"<strong>([\d.]+)</strong> dòng lệnh trong ảnh mới",
            (may["pm_anh_tong"],)),
        # ══ ⭐⭐⭐ BAN VE 13 · PHIA PM — con so DAN DAT tu 09/09 ══
        #
        # ⛔⛔ Hai pin truoc do o day ghim `65,6%` *(do phu TREN TRAN)*. Con so
        #    ay **van dung**, nhung owner da chot rang do tren dong TIEN la
        #    **do sai phia** ⇒ the dan dau cua trang doi sang `64,3%` phia PM.
        #    ⇒ Doi pin theo, ⛔ khong giu mot pin tro vao mot the da bi thay.
        Muc("bản vẽ 13 · phía PM · tỷ lệ", BANVE,
            r'<span class="k">Lệnh chi đã tìm được tiền của nó</span>\s*'
            r'<p class="v num">([\d,]+)%</p>', (may["pm_ty_le"],)),
        Muc("bản vẽ 13 · phía PM · dòng và phiếu trong thẻ", BANVE,
            r"<strong>([\d.]+)</strong> trong <strong>([\d.]+)</strong> dòng "
            r"lệnh đã nối được vào tiền thật; tính theo phiếu là "
            r"<strong>([\d.]+) / ([\d.]+)</strong>[\s\S]*?"
            r"<strong>([\d.]+) dòng lệnh</strong>, nằm trên "
            r"<strong>([\d.]+) phiếu</strong>",
            (may["pm_da_dung"], may["pm_anh_tong"], may["pm_phieu_da"],
             may["pm_phieu"], may["pm_ranh"],
             may["pm_phieu_con_dong_chua"])),
        Muc("bản vẽ 13 · phía PM · bảng việc còn lại", BANVE,
            r"<td class=\"n\"><strong>([\d.]+)</strong></td><td><strong>"
            r"([\d,]+)%</strong> — con số của việc ghép"
            r"[\s\S]*?<td class=\"n\">⛔ <strong>([\d.]+)</strong></td>"
            r"<td><strong>Đây là danh sách việc.</strong> Theo phiếu: "
            r"<strong>([\d.]+)</strong> trong <strong>([\d.]+)</strong> — trong đó "
            r"<strong>([\d.]+)</strong> phiếu"
            r"[\s\S]*?<td class=\"n\"><strong>([\d.]+)</strong></td><td>Có "
            r"một dòng tiền chưa nối"
            r"[\s\S]*?<td class=\"n\"><strong>([\d.]+)</strong></td><td>Việc "
            r"của người khác",
            (may["pm_da_dung"], may["pm_ty_le"], may["pm_ranh"],
             may["pm_phieu_con_dong_chua"], may["pm_phieu"],
             may["pm_phieu_mot_nua"], may["pm_ghep_ngay"],
             may["pm_chua_duyet"])),
        Muc("bản vẽ 13 · phía PM · cửa khoá theo dòng lệnh", BANVE,
            r"bảng tuyến: (\d+) cửa khoá theo dòng tiền, và trước hôm nay là (\d+) cửa "
            r"khoá theo dòng lệnh — nay là (\d+)",
            (may["tuyen_khoa_itl"], "0", may["tuyen_phia_pm"])),
        # ⭐⭐ `799` — VIEC NGUOI XEM. ⛔ Do bang `do_phu_hang_cho` — chinh
        #    phep xep man `F01` dung, nen con so tren trang va con so tren
        #    man **⛔ khong the lech**.
        Muc("bản vẽ 13 · việc người xem", BANVE,
            r"việc người phải xem là <strong>([\d.]+) dòng</strong>, "
            r"không phải ([\d.]+)</td>",
            (may["viec_nguoi_xem"], may["ve_ps_co_chua"])),
        # ⭐ Khuon OUTPUT: `64` cot. Do tu `oracle/ledge_spec`, ⛔ khong go tay
        Muc("bản vẽ 13 · khuôn output", BANVE,
            r"bộ xuất ra khuôn <strong>(\d+)</strong> cột",
            (may["ledge_cot"],)),
        # ── ban ve 12: SO DO va cau "dem theo khoi"
        # ⛔ So do ghi *"XONG HAN · N khoi"* tu 24/08 va ⛔ CHUA HE duoc do —
        #   ngay 09/09 module thu muoi ra doi thi ve *"dang lam"* thanh sai.
        Muc("bản vẽ 12 · sơ đồ số khối", BANVE,
            r'subgraph X\["XONG HẲN · (\d+) khối"\][\s\S]*?'
            r'subgraph D\["ĐANG LÀM · (\d+) khối"\]',
            (may["module_xong"], may["module_dang"])),
        Muc("bản vẽ 12 · đếm theo khối", BANVE,
            r"Đếm theo khối thì được <strong>(\d+)%</strong> \((\d+) trong "
            r"(\d+) khối xong hẳn\), đếm theo chặng thì 5,5/7 ≈ "
            r"<strong>79%</strong>, đếm theo khối lượng việc thì "
            r"<strong>(\d+)%</strong>",
            (may["ty_le_module_xong"], may["module_xong"],
             may["so_module"], may["tien_do"])),
    ]

    # ⭐⭐ CONG TU DEM CHINH NO — them 2026-08-28.
    #
    # ⛔⛔ Con so "cong so song N/N" da MUC HAI LAN trong mot ngay: 43 -> 48 ->
    # 57, va moi lan phai sua tay o **ba** cho (`00_MASTER_INDEX` §10 ·
    # `06_DASHBOARD` §1 · ban ve kien truc). Mot con so noi ve **chinh cai cong**
    # thi cong phai tu canh duoc — khong thi no la cho DUY NHAT trong ca bo tai
    # lieu duoc mien khoi luat cua chinh no.
    #
    # ⛔⛔⛔ **`len(m) + 3` la mot GIA DINH VE VI TRI, va no vua cắn — 09/09.**
    #
    # `+ 3` chi dung khi ba muc tu-dem la ba muc **CUOI CUNG** cua danh sach.
    # Toi them **muoi** phep so cua ban ve 13 vao *sau* chung ⇒ cong co **98**
    # phep so ma **tu khai `88`**, va no van **XANH**: ba tai lieu deu ghi 88,
    # nen `88 == 88` khop ca ba cho. ⇒ **Cong nay vua noi doi ve chinh no, va
    # chinh no la cong duoc viet ra de chan dung loai loi ay.**
    #
    # ⭐ Nen `+ 3` bi thay bang `len(_TU_DEM)`: so muc tu-dem **do tu chinh
    #   danh sach muc tu-dem**. Them mot cho ghim thu tu thi con so tu dung,
    #   ⛔ khong con mot con so nao trong phep dem phai go tay.
    tong = str(len(m) + len(_TU_DEM))
    # ⛔⛔ **Ghim CA HAI so cua `N/N`** — sua 09/09.
    #
    # Ban truoc chi ghim so DAU (`(\d+)/\d+`). Nen ve sau **gia trong im lang**
    # o **ca ba** cho, va lech ngay cang xa: ban ve `86/85` · master `86/66` ·
    # dashboard `86/85`. Mot cai `86/66` doc ra la *"20 phep so KHONG DAT"* —
    # tuc cong nay tu bao cao rang no dang do, trong khi no xanh.
    #
    # ⇒ Ca hai ve deu la `tong`: cau *"DAT N/N"* chi dung khi hai so **bang
    #   nhau**. Neu mai co phep so khong dat thi cau van phai doi, ⛔ khong
    #   phai con so.
    m += [Muc(ten, tep, mau, (tong, tong)) for ten, tep, mau in _TU_DEM]
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

    # ⭐⭐ `WO-011 T3` — cong moc `B` · ACTOR MOI. ⛔ Mot `Muc` *(⛔ so tai lieu
    #   voi may)*: no hoi kho *"co ai la ghi vao so khong"*. Co ⇒ goi ten, NO.
    moi = canh_actor_moi(json.loads(may["actor_moi"]))
    print(f"{'OK ' if not moi else '⛔ '}cổng mốc B · actor ngoài sổ "
          f"(`ACTOR_MAY ∪ ACTOR_DA_THAY`): {len(moi)}")
    for x in moi:
        print(f"     - {x}")
    tong += moi

    print()
    if tong:
        print(f"⛔ CONG SO SONG KHONG DAT — {len(tong)} lech/khong-do-duoc")
        return 1
    print(f"✅ cong so song DAT — {len(muc)} phep so, moi phep khop DUNG mot "
          f"lan va khop dung con so MAY do (commit `{may['commit']}`)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
