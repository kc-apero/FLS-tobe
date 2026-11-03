"""BANG TUYEN — khai **mot lan**, sinh ra ca bo dinh tuyen ca cong kiem.

★ Cung khuon voi `fls/db/model.py`: mot ban khai duy nhat, hai dau ra. O tang
kho la (DDL + ERD); o day la (may dinh tuyen + cong quet duong).

⛔⛔ **Cong quan trong nhat cua ca `P4`:** `03_Dev/03` §5.8 doi *"test quet
route table: khong ton tai `PUT`/`DELETE` nham `fls_itl`"*. Cong do chi co
nghia khi **co mot bang tuyen de quet**. Neu duong nam rai rac trong cac
`if path == ...` thi cong phai doc ma nguon de doan — va mot cong phai doan la
mot cong se sai.

⇒ Moi duong PHAI khai o day, **kem cac bang no cham** va **co no ghi hay khong**.
`cua.py` ⛔ khong duoc co duong nao khong nam trong bang nay (co bai kiem hai
chieu: khong tuyen nao thieu ham, khong ham nao thieu tuyen).
"""
from __future__ import annotations

import functools
import re
from dataclasses import dataclass

TIEN_TO = "/api/fls/v1"

# Phuong thuc ⛔ KHONG BAO GIO duoc nham vao so. `INV-I03`/`INV-I08`: sua chi
# bang but toan moi. Tang kho da cam bang trigger; bang tuyen cam o tang cua —
# hai lop, vi mot lop la mot lop co the bi go ra ma khong ai thay.
PHUONG_THUC_CAM_LEN_SO: frozenset[str] = frozenset({"PUT", "DELETE", "PATCH"})
SO = "fls_itl"

# ⭐ Bang MANG VET: co `actor` + `at`, tuc la doc lai duoc *ai lam, luc nao*.
# Mot duong ghi ma ⛔ khong cham bang nao trong day la mot duong khong de lai
# vet — va sau khi `QĐ-ITL-27` khai tu vai nguoi hau kiem thi vet la **lop kiem
# soat duy nhat con lai**.
#
# ⚠ `fls_queue_event` **tinh la vet** *(no co `actor`/`at`/`reason`)*, nen duong
# ghi ly do/hoan ⛔ khong bat buoc phai cham `fls_journal`. Ban dau toi doi ca
# bon duong ghi phai cham `fls_journal` — cong do se do GIA, va mot cong do gia
# thi nguoi ta go cong chu khong sua ma.
# ⭐ `fls_khai_cot` (08/09) — no **mang vet that**: `actor` NOT NULL +
# `hieu_luc_tu` NOT NULL, va no la so **CHI-THEM** (sua = `version` moi,
# co cong quet ma nguon cam `UPDATE`/`DELETE`). ⇒ Doc lai duoc *ai khai,
# luc nao, va khai TRUOC do la gi* — dung dinh nghia cua tap nay.
# ⚠ Them vao day vi cong vua bat DUNG: `POST .../khai-cot` bi bao "ghi ma
#   ⛔ khong de lai vet" — cong dung, **tap thi thieu mot ten**.
BANG_CO_VET: frozenset[str] = frozenset({
    "fls_journal", "fls_queue_event", "fls_khai_cot"})

# Bang duoc phep xuat hien trong bang tuyen. ⛔ Ten la = NO, de mot duong doc
# `fps_*` hay P100 khong the lot vao trong im lang (`QĐ-ITL-45`: FLS chi doc
# `fls_*`, moi thu khac di qua adapter).
BANG_CHO_PHEP: frozenset[str] = frozenset({
    "fls_itl", "fls_pm_link", "fls_journal", "fls_adjustment",
    "fls_queue_event",
    "fls_queue_state", "fls_run", "fls_reject", "fls_le",
    "fls_mapping_master", "fls_source", "fls_sua_tay",
    "fls_pm_line",          # anh chup dong lenh chi (migration 0011)
    # ⭐ Duong BO MOI NOI (migration 0013, `GAP-JOIN-05`).
    "fls_pm_unlink",        # so ghi cac lan BO moi noi
    "fls_moi_noi",          # khung xem: moi noi DANG CO HIEU LUC
    # ⭐ NGUOI bam "xong" (migration 0014, `QĐ-ITL-71`).
    "fls_da_xong",          # khung xem: dong da duoc NGUOI bam xong
    # ⭐ Nhom NAP (`CR#11`): ban khai anh xa cot (migration `0016`).
    "fls_khai_cot",
    # ⭐ Ban khai THU HAI: `Range_*` cua danh muc (migration `0017`,
    #   `GAP-KHAI-01`) — thu ma script `Run` cua trang tinh thuc su doc.
    "fls_nguon_dai",
    # ⭐⭐ Lan ANH CHUP (migration `0018`, `QĐ-ITL-110`) — cho o cua vung
    #    CHUAN. ⛔ Truoc no, `xem-truoc`/`nap` doi nguoi goi **dua san `dong`**,
    #    tuc he ⛔ khong co duong vao nao cho du lieu that.
    "fls_chup", "fls_chup_nguon", "fls_chup_dong",
    # ⭐⭐ Khung xem DIEN GIAI (migration `0026`, `QĐ-ITL-145`) — no noi dong so
    #    voi anh chup theo nhip gio, **⛔ khong ghi mot o nao**. Dien giai sao
    #    ke la **bang chung duy nhat** cua `49%` cuon so *(nhanh nuoc ngoai,
    #    `DT-I13 ⓑ`)*, nen cot nay ⛔ **khong bao gio** bi hy sinh khi man hep.
    # ⚠ Them `21/09`: cong da bat DUNG — ban khai thieu mot ten, ⛔ khong phai
    #   cua di sai duong.
    "fls_dien_giai",
    # ⭐⭐ Khung xem GOI Y CUA MAY (migration `0025`, `QĐ-ITL-143`) — co tu
    #    18/09 nhung ⛔ tuyen nao doc no cho toi `WO-003` (01/10): cu ghep TAY
    #    nay ghi `hd`/`cdt1` vao lan may (`QĐ-ITL-149`) va bo ghep dao ca goi y
    #    may ⇒ `match` · `match-lo` · `unmatch` doc no. Kho rieng FLS — dung
    #    tinh than `QĐ-ITL-45`, ⛔ phai mot bang ngoai.
    "fls_may_goi_y",
})


@functools.lru_cache(maxsize=256)
def _mau(duong: str) -> re.Pattern[str]:
    """`/a/{x}` → mau khop MOT doan. ⛔ `{x}` khong an dau `/`.

    Neu `{x}` an ca dau `/` thi `/ledger/{itl_id}` se khop `/ledger/1/nhat-ky`
    va tra ve du lieu cua duong khac — mot loi dinh tuyen **im lang**.
    """
    doan = [f"(?P<{s[1:-1]}>[^/]+)" if s.startswith("{") and s.endswith("}")
            else re.escape(s)
            for s in duong.split("/")]
    return re.compile("^" + "/".join(doan) + "$")


@dataclass(frozen=True)
class Tuyen:
    phuong_thuc: str
    duong: str
    ham: str
    bang: tuple[str, ...]
    # ⛔⛔ `bang_ghi` them o `P5`, va no chua mot lo THAT cua ban `P4`.
    #
    # Cong cu chi kiem *"khong `PUT`/`DELETE`/`PATCH` nao nham `fls_itl`"* — mot
    # phep kiem theo PHUONG THUC. Nhung duong ghi cua `P5` la `POST`, nen mot
    # `POST /ledger/{id}/adjust` **ghi thang vao `fls_itl`** se **di qua cong do
    # trong im lang**. Va do dung la duong de nhat: dac ta `BA-07` §3 con noi
    # *"truong hop-dong cap nhat `*_thyt`"* — tuc la moi nguoi da mo cua san.
    #
    # ⇒ Khai TUONG MINH bang nao mot duong duoc GHI, va cong chan `fls_itl` o
    #   moi phuong thuc, ⛔ khong chi ba phuong thuc kia.
    bang_ghi: tuple[str, ...] = ()
    # ⭐⭐⭐ `CR#11` task `4` — **THEM vao so ⛔ KHONG phai SUA so**.
    #
    # ⛔⛔ Cho toi 08/09, luat cua bang nay la *"⛔ khong tuyen nao duoc ghi vao
    # `fls_itl`"* — va no DUNG, vi luc ay **⛔ khong tuyen nao NAP**: duong duy
    # nhat dua du lieu vao kho la mot lenh dong lenh. Moi `POST` deu SUA mot
    # dong DA CO, nen "ghi vao so" chi co the nghia la **sua so**.
    #
    # `POST /nap` la tuyen **DAU TIEN** THEM dong vao so, va `INV-I08` doc
    # nguyen van la *"chi THEM, ⛔ khong SUA"* — tuc phep THEM **chinh la thu
    # bat bien ay cho phep**. Mot cong khong phan biet duoc hai viec ay se
    # **cam ca cai no sinh ra de bao ve**.
    #
    # ⛔ Va vi day la mot **ngoai le co ten**, no phai **hep va CHUNG MINH
    #   DUOC** — cong doi ba dieu kien cung luc:
    #     ⓐ phai la `POST` *(`PUT`/`DELETE`/`PATCH` van cam tuyet doi)*;
    #     ⓑ phai ghi ca `fls_run` — mot dong so ⛔ khong co lan nap la mot dong
    #        **mat lineage** (`INV-I05`/`I12`), va do la thu `GAP-ERD-P0-01` da
    #        dong bang mot FK;
    #     ⓒ ca `fls/` ⛔ **khong duoc chua** mot cau `UPDATE`/`DELETE` nao nham
    #        `fls_itl` — quet ma nguon, o `tests/api/test_them_vao_so.py`.
    them_vao_so: bool = False
    ghi: bool = False
    # ⭐⭐ `CR#11` task `4` — **DOC THAN ⛔ KHONG dong nghia voi GHI**.
    #
    # ⛔⛔ Cho toi 08/09 `cua.py` viet `than = _doc_than() if tuyen.ghi else {}`
    # — tuc no **gan chat** hai khai niem khac nhau. Dung, cho toi khi co
    # `POST /nap/xem-truoc`: mot tuyen **doc ca mot lo du lieu** trong than yeu
    # cau va **⛔ khong ghi mot dong nao**.
    #
    # ⛔ Cach chua SAI la khai no `ghi=True` cho "de": lam the thi no duoc cap
    #   **ket noi GHI**, va ca dac diem cua tuyen ay — *"go nham duong ⛔ khong
    #   mat gi"* — bien mat.
    #
    # ⇒ Tach thanh mot truong RIENG. Mac dinh `None` = *"theo `ghi`"*, nen
    #   **17 tuyen cu ⛔ khong doi mot chu**.
    #
    # ⭐⭐ Va nho tach ma co mot bao dam manh hon moi loi hua trong ma:
    #   `xem-truoc` chay tren **ket noi bi PostgreSQL CHAN GHI**. *"Xem truoc
    #   ⛔ khong ghi"* vi the ⛔ khong phai mot cau hua — no la mot thu **cai
    #   kho tu choi**.
    doc_than: bool | None = None

    @property
    def can_than(self) -> bool:
        return self.ghi if self.doc_than is None else self.doc_than
    ghi_nhat_ky: bool = False
    mo_ta: str = ""

    def khop(self, duong: str) -> dict[str, str] | None:
        m = _mau(self.duong).match(duong)
        return None if m is None else m.groupdict()


# ── P4: CHI DOC. `P5` se them nhom ghi vao dung bang nay. ─────────────────
BANG_TUYEN: tuple[Tuyen, ...] = (
    # ⚠ `fls_mapping_master` them 03/09: cua nay nay mang ca vung PHAN BO 🔒,
    # suy tu `cdt1` + `hd` + danh muc *(`fls/ledger/allocate.py`)*.
    # ⭐ Cong #14 `soi_bang_tuyen` **do ngay** khi toi them phep doc do ma quen
    # ban khai — dung viec no sinh ra de lam (`GAP-API-05`).
    Tuyen("GET", f"{TIEN_TO}/ledger", "so", ("fls_itl", "fls_mapping_master"),
          mo_ta="dong so + vung PHAN BO 🔒, loc period/le/status, phan trang khoa"),
    Tuyen("GET", f"{TIEN_TO}/ledger/{{itl_id}}", "mot_dong",
          # ⚠ Tam bang. Ban khai cu chi co 2 (`fls_itl`, `fls_pm_link`) —
          # `GAP-API-05` do duoc 03/09: mot dong so keo theo but toan tay,
          # trang thai xong, moi noi con hieu luc + cac lan da bo, va nhat ky
          # hang cho. Nay `tools/soi_bang_tuyen.py` canh cho nay.
          ("fls_itl", "fls_pm_link", "fls_moi_noi", "fls_pm_unlink",
           "fls_sua_tay", "fls_adjustment", "fls_da_xong", "fls_queue_event",
           "fls_mapping_master"),
          mo_ta="mot dong + 36 cot canon + moi noi lenh chi + cac lan da BO "
                "+ vung PHAN BO 🔒"),
    Tuyen("GET", f"{TIEN_TO}/queue", "hang_cho",
          # ⚠ `fls_da_xong` them 03/09 (`GAP-API-05`): dieu kien "da bam xong"
          # nam TRONG cau con `q` tu `QĐ-ITL-71` ma ban khai ⛔ khong theo kip.
          ("fls_itl", "fls_queue_state", "fls_da_xong"),
          mo_ta="hang cho xep theo TIEN trong tung tien te (QĐ-ITL-58)"),
    Tuyen("GET", f"{TIEN_TO}/queue/summary", "hang_cho_tom",
          ("fls_itl", "fls_da_xong"),
          mo_ta="so dong + Σ tien hang cho THEO TUNG tien te, ⛔ khong dong tong"),
    Tuyen("GET", f"{TIEN_TO}/journal", "nhat_ky",
          # ⭐ `WO-023` `(f)` *(`BA-07` v3.6)*: `la_ban_dao` noi `fls_adjustment`
          #   theo `(itl_id, field, at, actor)` ⇒ tuyen **doc them** bang ay.
          ("fls_journal", "fls_itl", "fls_adjustment"),
          mo_ta="nhat ky 7 truong cua mot dong (?itl_id=)"),
    Tuyen("GET", f"{TIEN_TO}/gates", "cong",
          # ⚠⚠ Ban khai cu vua THIEU vua THUA: no ghi `fls_pm_link` +
          # `fls_reject` *(SQL ⛔ khong cham)* va bo sot `fls_moi_noi` *(SQL CO
          # cham — phep do Σ moi noi phai chay tren khung xem HIEU LUC, ⛔ khong
          # tren bang goc)*. Ca hai chieu deu la ban do ve sai.
          # ⭐ Them 11/09: `fls_chup` + `fls_pm_line` — cong `RUN_DEM_KHOP` nay
          # do **dung BANG ma lan nap ay ghi vao** *(`Bank`→`fls_itl`,
          # `PM`→`fls_pm_line`)*, va no phan biet bang `fls_chup.lan`. ⭐ Chinh
          # cong `soi_bang_tuyen` da bat thieu sot nay ngay trong buoi sua —
          # dung viec no sinh ra de lam (`GAP-API-05`).
          ("fls_chup", "fls_itl", "fls_moi_noi", "fls_pm_line", "fls_run"),
          mo_ta="cong do duoc + 4 cong ke toan khai la CHUA DO DUOC"),

    # ── ⭐ `P6·B3` — DO PHU hang cho. Mot trong **6 duong doc** cua `BA-07` §2
    # con thieu; man `F03` can dung no *(ban ve `FLS-Design-P6`, the "Do phu
    # hang cho theo tien te")*.
    #
    # ⛔⛔ Truoc duong nay, cach duy nhat lay so *"N dong phu 90 phan tram tien"*
    # la keo `/queue?den_pct=90&limit=500` roi **dem o phia man hinh** — va chan
    # tren mot trang la **500** (`TRANG_TOI_DA`), nen con so ay **im lang dung o
    # 500** khi hang cho dai ra. Hom nay USD can **444**: con **56 dong** nua la
    # no sai ma ⛔ khong ai biet. ⇒ Dem bang `count(*)` trong kho.
    Tuyen("GET", f"{TIEN_TO}/queue/coverage", "do_phu",
          ("fls_itl", "fls_da_xong"),
          mo_ta="do phu hang cho THEO TUNG tien te: so dong cho · Σ tien · so "
                "dong du phu ?muc_pct (mac dinh 90) · phan tram dong. "
                "⛔ khong co dong 'tong'"),

    # ── P5 · nhom GHI. ⛔ Ca bon deu la `POST` va ⛔ khong duong nao ghi vao
    # `fls_itl` — sua chi bang but toan moi (`INV-I08`).
    Tuyen("GET", f"{TIEN_TO}/ledger/{{itl_id}}/fields/{{field}}", "truoc_khi_go",
          ("fls_itl", "fls_sua_tay"),
          mo_ta="gia tri dang co + no den TU DAU (nguon/may/tay) — de man hinh "
                "noi duoc 'nguon noi X' TRUOC khi nguoi go"),
    Tuyen("POST", f"{TIEN_TO}/ledger/{{itl_id}}/adjust", "sua",
          # ⭐ `fls_mapping_master` them 04/09: duong ghi nay nay **doc**
          #   danh muc de kiem ma hop dong (`QĐ-ITL-86`). Chi DOC —
          #   ⛔ khong bao gio ghi vao do.
          ("fls_itl", "fls_sua_tay", "fls_adjustment", "fls_journal",
           "fls_mapping_master"),
          bang_ghi=("fls_adjustment", "fls_journal"),
          ghi=True, ghi_nhat_ky=True,
          mo_ta="nguoi go mot trong 7 truong; 409 neu khac nguon "
                "(US-025); 4xx neu ma hop dong ngoai danh muc hay ky "
                "sai khuon YYYYMM (QĐ-ITL-86)"),
    Tuyen("POST", f"{TIEN_TO}/adjustments/{{adj_id}}/reverse", "dao",
          ("fls_itl", "fls_adjustment", "fls_journal"),
          bang_ghi=("fls_adjustment", "fls_journal"),
          ghi=True, ghi_nhat_ky=True,
          mo_ta="dao but toan = THEM mot dong tro toi no (SM-I03)"),
    Tuyen("POST", f"{TIEN_TO}/queue/{{itl_id}}/reason", "ly_do",
          ("fls_itl", "fls_queue_event"), bang_ghi=("fls_queue_event",),
          ghi=True,
          mo_ta="cot ly do cua hang cho (US-039) — cot US-045 dem"),
    Tuyen("POST", f"{TIEN_TO}/queue/{{itl_id}}/defer",  "hoan",
          ("fls_itl", "fls_queue_event", "fls_queue_state"),
          bang_ghi=("fls_queue_event",), ghi=True,
          mo_ta="hoan CO HAN (US-040); lan thu ba doi mau, ⛔ khong leo cap"),

    # ── GHEP LENH · duong DOC. Mo duoc nho anh chup `fls_pm_line`
    # (migration `0011`, owner chot duong (a) — dong `GAP-API-04`).
    #
    # ⛔ Truoc do duong nay **BI CHAN, ⛔ khong phai chua lam**: danh sach dong
    # lenh chi nam o he khac va bo nap doc no **luc chay roi khong luu**.
    Tuyen("GET", f"{TIEN_TO}/queue/{{itl_id}}/pm-candidates", "ung_vien",
          ("fls_itl", "fls_pm_line", "fls_moi_noi"),
          mo_ta="ung vien ghep lenh, 4 BAC CO TEN (ma/tien/gan_tien/cung_tien_te) "
                "+ TUOI cua anh chup. ⛔ khong xep duoc theo ngay/payee "
                "(anh chup khong mang PII — GAP-JOIN-04)"),
    # ⛔⛔ Than yeu cau la `{pm_line_ids: [...]}` — danh sach ma DONG, ⛔ KHONG
    # `{pm_id}` (mot PHIEU) nhu `BA-07` §2 viet. So lieu lat cau do: 526 phieu
    # mang 2–36 reference KHAC NHAU, nen ghep vao phieu thi MAY phai tu chon dong
    # nao — tuc may quyet thay nguoi (`INV-I16`). Sua dac ta: `CR#6`.
    Tuyen("POST", f"{TIEN_TO}/queue/{{itl_id}}/match", "ghep",
          ("fls_itl", "fls_pm_line", "fls_pm_link", "fls_moi_noi",
           "fls_queue_event", "fls_adjustment", "fls_journal", "fls_sua_tay",
           # ⭐ `WO-003` (`QĐ-ITL-149`): `hd`/`cdt1` suy luc ghep la GOI Y
           #   CUA MAY ⇒ doc `fls_may_goi_y` (goi y trung ⇒ ⛔ them dong;
           #   `value_before`) qua `ghi_tay.loc_goi_y`.
           "fls_may_goi_y"),
          bang_ghi=("fls_pm_link", "fls_queue_event", "fls_adjustment",
                    "fls_journal"),
          ghi=True, ghi_nhat_ky=True,
          mo_ta="ghep tay: Σ dong lenh PHAI bang tien bank (dung sai theo tien "
                "te) ⇒ lech thi 422 va GIU UNMAPPED, ⛔ khong chia bua"),

    # ── ⭐⭐⭐ `B0` + `B2` (09/09, `QĐ-ITL-118`) — MAU SO va cua ghep LO.
    #
    # ⛔⛔ **Vi sao ba duong nay ra doi cung mot lan.** Lo trinh `13` §1 chang ①
    # dat `B0` *(do lai mau so)* **truoc** `B2` *(cua ghep lo)*, va do la mot
    # thu tu **co ly do do duoc**: `B2` chi co nghia neu con so *"bao nhieu dong
    # ghep duoc ngay"* la con so cua **cua GHI**, ⛔ khong phai cua **danh sach
    # ung vien**. Va dung `B0` bat duoc rang hai con so ay lech **8,6 lan**
    # (`584` so voi `68`).
    # ══ ⭐⭐⭐ `GAP-SCR-14` — HANG CHO PHIA LENH CHI (09/09) ══
    #
    # ⛔⛔ Truoc hom nay: **10** tuyen khoa `itl_id`, ⛔ **0** tuyen khoa dong
    #    lenh ⇒ ⛔ khong duong nao hoi *"lenh chi nao ⛔ chua tim duoc tien"*,
    #    trong khi `QĐ-ITL-122` noi do **la** cau hoi cua viec.
    #
    # ⛔⛔⛔ **Ca ba deu la `GET`.** Phep ghep van di qua
    #    `POST /queue/{itl_id}/match` — ⛔ KHONG co duong ghi thu hai.
    # ⭐ `11/09` (`G2`): tuyen nay nay cham them `fls_itl` — phep chia RO doc
    #   `doc_no` de biet dong lenh co tim duoc tien khong (`BA-12 §2`).
    Tuyen("GET", f"{TIEN_TO}/queue/lenh-cho", "lenh_cho",
          # ⭐ `fls_dien_giai` them `22/09`: moi hang nay mang `gd` — giao dich
          #   **de xuat dau** — de BANG SO ve duoc ba cot cuoi. ⛔ Khong khai
          #   thi cong `soi_bang_tuyen` DO ngay, va no da do dung nhu the.
          ("fls_pm_line", "fls_moi_noi", "fls_itl", "fls_dien_giai"),
          mo_ta="dong lenh chi ⛔ CHUA tim duoc tien, xep theo tien GIAM trong "
                "TUNG tien te (`PARTITION BY curr` — `QĐ-ITL-58`). `?duyet=0|1` "
                "loc theo `status`; mac dinh HIEN CA HAI (⛔ khong mac dinh im "
                "lang — `INV-I16`). Moi dong mang `ro` (`may`/`nguoi`/`khong`) "
                "+ `vi_sao` + `tu_chung` (`BA-12 §2`)"),
    Tuyen("GET", f"{TIEN_TO}/queue/lenh-cho/ro", "lenh_cho_ro",
          ("fls_pm_line", "fls_moi_noi", "fls_itl"),
          mo_ta="dem dong lenh cho theo RO — `may` (may tra loi duoc) · "
                "`nguoi` (viec that) · `khong` (⛔ khong ai tra loi duoc o FLS) "
                "+ `tu_chung` + `tong`. Ba ro phai KHEP ve `tong`"),
    Tuyen("GET", f"{TIEN_TO}/queue/lenh-cho/summary", "lenh_cho_tom",
          ("fls_pm_line", "fls_moi_noi"),
          mo_ta="chan man phia lenh chi theo TUNG tien te: so dong · so phieu · "
                "tien · so dong DUYET va CHUA DUYET (hai loai viec khac nhau) · "
                "so dong de phu `muc_pct` tien. ⛔ khong co dong 'tong'"),
    # ⭐⭐⭐ `GAP-API-08` — tuyen **40**. Truoc no, **2/4** chip cua man ghep
    #    ⛔ khong goi duoc: `/queue/lenh-cho` loc cung `NOT EXISTS
    #    (fls_moi_noi)` nen ⛔ khong duong nao hoi *"lenh nao DA co tien"*, va
    #    ca nua *"da gan"* cua man chet theo day chuyen — nut `Bo gan` ⛔ khong
    #    bao gio bat, `.mrow.da_gan` la CSS chet.
    #
    # ⛔⛔ **Mot tuyen RIENG chu ⛔ khong mot co tren `lenh-cho`:** ten
    #    `lenh-cho` nghia la *"dang cho"*; cho no tra dong da noi la de mot cai
    #    ten **noi doi**, va moi nguoi doc ma sau nay se tin cai ten ay.
    Tuyen("GET", f"{TIEN_TO}/queue/lenh-da-gan", "lenh_da_gan",
          ("fls_pm_line", "fls_moi_noi", "fls_itl", "fls_dien_giai"),
          mo_ta="dong lenh chi **DA** tim duoc tien, kem `itl_da_gan[]` — "
                "⭐ mot DANH SACH chu ⛔ khong mot so: do 22/09 tren kho that, "
                "**23/2.219 = 1,0%** lenh gan NHIEU HON MOT dong tien, va mot "
                "khoa so it se im lang bo mat phan con lai dung o cho nguoi ta "
                "bam `Bo gan`. Bu cua `/queue/lenh-cho`; hai ro KHEP ve tong "
                "2.219 + 1.553 = 3.772"),
    # ⭐⭐ `11/09` — owner: *"bang PM van chua du cac truong nhu trong GGSheet"*.
    #   Do that: `PM_Unpivot` co **28 cot**, FLS doc **8**, va 20 cot bo qua
    #   dien **100%** — trong do co `Noi dung nhap o bank` va `Ten tai khoan`,
    #   dung hai thu de nhan ra mot khoan tien. Cua nay mo ca 28 cot.
    Tuyen("GET", f"{TIEN_TO}/queue/lenh/{{pm_line_id}}", "mot_dong_lenh",
          ("fls_pm_line", "fls_moi_noi"),
          mo_ta="MOT dong lenh: 8 truong da phan tich + `tho` (ca hang tho, "
                "khoa theo TEN COT) + `ca_phieu` (cac dong khac cung phieu — "
                "526 phieu mang 2-36 reference khac nhau)"),
    Tuyen("GET", f"{TIEN_TO}/queue/lenh/{{pm_line_id}}/itl-candidates",
          "ung_vien_tien",
          # ⭐ `fls_dien_giai` them `21/09` (`QĐ-ITL-148`): dien giai sao ke la
          #   **bang chung duy nhat** cua `49%` cuon so — cot ⛔ khong bao gio
          #   bi hy sinh khi man hep.
          ("fls_pm_line", "fls_itl", "fls_moi_noi", "fls_dien_giai"),
          mo_ta="dong TIEN ung vien cho MOT dong lenh — chieu NGUOC cua "
                "`pm-candidates`. 4 bac CO TEN, ten giu y nguyen. Bac `ma` "
                "tinh o PYTHON bang `canon_ref` (kho ⛔ khong co ban chuan hoa "
                "cua `doc_no`). Bac `cung_tien_te` BI CAT, va cua KHAI RA da "
                "cat (`bi_cat` + `tong_cung_tien_te`)"),
    # ⭐⭐ Tuyen 36 — TRA CUU TOAN SO. `QĐ-ITL-148` · `BA-07 §4h ⓹`.
    #
    # ⛔ Vi sao ⛔ KHONG dung `GET /ledger`: no loc `?period=&le=&status=` —
    #   ⛔ khong tim chu, va ⛔ khong biet lenh nao dang mo nen ⛔ khong tinh
    #   lai bac duoc.
    # ⭐ Va day ⛔ khong phai tinh nang phu: che do nay **bat san** voi lenh may
    #   ⛔ khong tim duoc ung vien nao ⇒ no la **loi thoat ngo cut** cua **768**
    #   dong. ⛔ Khong co no thi man **LA** ngo cut.
    Tuyen("GET", f"{TIEN_TO}/queue/lenh/{{pm_line_id}}/so", "so_theo_lenh",
          ("fls_pm_line", "fls_itl", "fls_moi_noi", "fls_chup_dong",
           "fls_source", "fls_dien_giai"),
          mo_ta="TOAN SO cho MOT dong lenh — cung khuon `ung_vien[]`, nhung "
                "bac duoc TINH LAI theo lenh dang mo (khop `canon_ref` ⇒ `ma`, "
                "dung tien ⇒ `tien`, con lai ⇒ `cung_tien_te`). ⛔ Bac `ma` "
                "tinh o PYTHON: `regexp` trong SQL lech 17,9% (560 vs 475). "
                "`?q=` tim trong dien giai + so chung tu"),
    # ⭐⭐ Tuyen 37 — CHUM moi noi. `QĐ-ITL-148 ③`.
    #
    # ⛔ Cua `unmatch` bo TOAN BO moi noi cua dong tien va ⛔ khong nhan
    #   `pm_line_ids` (`QĐ-ITL-69`: bo le lam `Σ moi noi ≠ tien bank`). Owner
    #   chot **giu cua, MAN noi ra thiet hai** ⇒ man phai hoi duoc *"cu bam nay
    #   se go NHUNG DONG NAO"*.
    # ⭐ Do `21/09`: chi **25/2.222 = 1,1%** dong tien mang chum, lon nhat **10**.
    Tuyen("GET", f"{TIEN_TO}/queue/{{itl_id}}/chum", "chum_moi_noi",
          ("fls_moi_noi", "fls_pm_line"),
          mo_ta="cac dong lenh mot cu `Bo gan` se go — KEM TEN, ⛔ khong mot "
                "con so. Mot con so 'se go 3 moi noi' ⛔ khong du: nguoi dung "
                "chi dinh dong toi MOT trong so do"),
    Tuyen("GET", f"{TIEN_TO}/queue/mau-so", "mau_so",
          ("fls_itl", "fls_moi_noi", "fls_pm_line"),
          mo_ta="MAU SO tac vu ①: 4 nhom VE (`PS Co`/`PS No`/ca hai/khong ve) "
                "· 4 o `work_status` x `co moi noi` MOI O MOT TEN LY DO · 4 "
                "nhom vi sao chua noi (PHU HET) · so dong TU CHUNG · TRAN "
                "CUNG + do phu TREN TRAN · ⭐ `phia_pm`: mau so THAT la so "
                "DONG LENH CHI (`QĐ-ITL-122` — `Trans` map vao `PM`)"),
    Tuyen("GET", f"{TIEN_TO}/queue/tu-chung", "tu_chung_ds",
          ("fls_itl", "fls_moi_noi", "fls_pm_line"),
          mo_ta="danh sach dong TU CHUNG (ghep duoc ⛔ khong can nguoi chon) + "
                "ly do TU CHOI cho tung dong co ma ma ⛔ khong tu chung"),
    # ⛔⛔ Than yeu cau la `{itl_ids: [...]}` va **CHI** the — ⛔ KHONG
    # `pm_line_ids`, ⛔ KHONG `force`. May do lai phia may chu roi ghep dung cai
    # no do ra; cung luat voi cua khai thu tu LO (`QĐ-ITL-117`).
    Tuyen("POST", f"{TIEN_TO}/queue/match-lo", "ghep_lo",
          ("fls_itl", "fls_pm_line", "fls_pm_link", "fls_moi_noi",
           "fls_queue_event", "fls_adjustment", "fls_journal", "fls_sua_tay",
           # ⭐ `WO-003` (`QĐ-ITL-149`): `hd`/`cdt1` suy luc ghep la GOI Y
           #   CUA MAY ⇒ doc `fls_may_goi_y` (goi y trung ⇒ ⛔ them dong;
           #   `value_before`) qua `ghi_tay.loc_goi_y`.
           "fls_may_goi_y"),
          bang_ghi=("fls_pm_link", "fls_queue_event", "fls_adjustment",
                    "fls_journal"),
          ghi=True, ghi_nhat_ky=True, doc_than=True,
          mo_ta="ghep CA LO, CHI dong TU CHUNG: mot dong ⛔ khong tu chung ⇒ "
                "422 CA LO va ⛔ 0 moi noi moi. ⛔ Khong nhan `pm_line_ids` va "
                "⛔ khong bao gio nhan `force`"),

    # ── ⭐⭐ DUONG LUI cua phep ghep (`GAP-JOIN-05`, `QĐ-ITL-69`).
    #
    # ⛔⛔ **Vi sao duong nay phai co TRUOC khi mo man hang cho.** Tu 27/08 ke
    # toan ghep duoc, nhung mot moi noi ghep sai thi ⛔ khong go duoc — chinh
    # `ghep_lenh` phai NO ra cau *"chua co duong nao lam viec do"*. Giao man
    # hang cho ma thieu day la giao mot cai nut ⛔ khong co duong lui.
    #
    # ⚠ `POST` chu ⛔ khong `DELETE`: bo mot moi noi la **THEM mot dong**
    # (`INV-I08`) — `DELETE` mo tu dung hanh vi ma ca tang nay cam.
    Tuyen("POST", f"{TIEN_TO}/queue/{{itl_id}}/unmatch", "bo_ghep",
          # ⚠ ⛔ KHONG co `fls_pm_link`: phep bo DOC khung xem `fls_moi_noi`
          # va GHI vao `fls_pm_unlink`; bang goc ⛔ khong bi cham — no la LICH
          # SU (`QĐ-ITL-69`). Ban khai cu ghi no ⇒ ban do ve mot duong ⛔ khong
          # co (`GAP-API-05`).
          ("fls_itl", "fls_moi_noi", "fls_pm_unlink",
           "fls_queue_event", "fls_adjustment", "fls_journal",
           # ⭐ `fls_sua_tay` CHI con de dung `bo_qua` (gia tri NGUOI —
           #   `DT-I14` v0.7 dinh nghia `bo_qua`).
           "fls_sua_tay"),
          # ⛔⛔ `WO-003` vong 2 (`KQ-005 F-1`, `DT-I14` v0.7 nhanh 6–8): BO
          #   `fls_may_goi_y` khoi ban khai. Vong 1 doc tap "con hieu luc" =
          #   `fls_sua_tay` ∪ `fls_may_goi_y` — hai khung xem tra **lop tren
          #   cung** ⇒ lop goi y bi `goi_y_lai` de NOI LEN LAI thanh mo coi sau
          #   bo ghep (2/2 kich ban kho TEST). Nay tap can dao doc thang BANG GOC
          #   `fls_adjustment` + `reversal_of` (`NOT EXISTS` ban dao).
          bang_ghi=("fls_pm_unlink", "fls_queue_event", "fls_adjustment",
                    "fls_journal"),
          ghi=True, ghi_nhat_ky=True,
          mo_ta="bo TOAN BO moi noi cua mot dong (⛔ khong bo le — Σ se lech), "
                "dao cac but toan hd/cdt1 do CHINH phep ghep suy ra ma CON hieu "
                "luc, va KHAI RA thu ⛔ khong dao (nguoi da go tay len)"),

    # ── ⭐⭐ NGUOI BAM "XONG" (`QĐ-ITL-71`, dong `GAP-JOIN-06`).
    #
    # ⛔⛔ **Vi sao hai duong nay phai co.** `fls_itl.work_status` bi **dong bang
    # luc nap** va moi cua ghi deu ⛔ khong dung vao `fls_itl` (`INV-I08`) ⇒
    # truoc quyet dinh nay, mot dong da chua xong **nam trong hang cho MAI MAI**.
    # Owner chot: **NGUOI bam xong**, ⛔ khong phai may tu nha khi thay du truong.
    #
    # ⚠ `reason` **tuy y** khi dong da du 5 truong hop dong; **BAT BUOC** khi con
    #   thieu truong HAY ky da chot — luc do nguoi dang **ghi de ket luan cua
    #   may** (`INV-I16`), va so dong nhu the duoc **dem rieng**.
    Tuyen("POST", f"{TIEN_TO}/queue/{{itl_id}}/done", "xong",
          ("fls_itl", "fls_da_xong", "fls_sua_tay", "fls_queue_event"),
          bang_ghi=("fls_queue_event",), ghi=True,
          mo_ta="NGUOI bam xong ⇒ dong roi hang cho (⛔ khong o nao cua so doi). "
                "Bam hai lan ⛔ khong thanh hai su kien — tra ve ai da bam va luc nao"),
    Tuyen("POST", f"{TIEN_TO}/queue/{{itl_id}}/reopen", "mo_lai",
          ("fls_itl", "fls_da_xong", "fls_queue_event"),
          bang_ghi=("fls_queue_event",), ghi=True,
          mo_ta="mo lai mot dong da bam xong = THEM su kien `reopen` (⛔ khong "
                "xoa). `reason` BAT BUOC: keo lai la lat ket luan cua NGUOI khac"),

    # ── ⭐⭐⭐ NHOM NAP (`CR#11` task `4`, `BA-07` §4b) ────────────────────
    #
    # ⛔⛔ **Truoc hom nay nhom nay ⛔ KHONG TON TAI.** Do duoc: **0/17** tuyen
    # la cua nap — 8 `GET` + 9 `POST`, va **moi `POST` deu SUA mot dong DA CO**.
    # Duong duy nhat dua du lieu vao kho la mot **lenh dong lenh doc Google
    # Sheets**. ⇒ Bo Google Sheets ma ⛔ khong dung nhom nay thi **⛔ khong con
    # duong nao vao**.
    #
    # ⛔ Van **⛔ KHONG co `PUT`/`DELETE`**: so chi-THEM (`INV-I08`). Nap nham
    #   thi **nap ban dung roi dao**, ⛔ khong xoa.
    # ── ⭐⭐⭐ NHOM ANH CHUP (`QĐ-ITL-110`, task `9d`, `BA-07` §4c) ────────
    #
    # ⛔⛔ **Bon tuyen nay sinh ra vi mot PHEP DO, ⛔ khong vi mot y tuong.**
    # Soi man `F04` xuong CHINH bang nay ngay 08/09: man can **5 cua**, va
    # **3 cua ⛔ KHONG TON TAI** (① danh sach nguon · ② duong doc vung CHUAN ·
    # ③ `GET .../khai-cot` — chi co `POST`). Nang hon: **hai cua CO van ⛔
    # khong chay duoc**, vi ca `xem-truoc` lan `nap` doi nguoi goi **dua san
    # `dong`** — tien de *"man hinh da cam tep"* cua `QĐ-ITL-105` ⓷ ma
    # `QĐ-ITL-109` **da lat**.
    #
    # ⚠ Va no noi mot dieu ve chinh cong `soi_bang_tuyen`: cong ay kiem *"ban
    #   khai co KHOP SQL that khong"* — mot cau rat manh — nhung no ⛔ **khong
    #   bao gio hoi** *"co du cua cho cai man hinh dang cho khong"*. Mot bang
    #   do **dung tuyet doi** va **thieu ba duong** thi van xanh.
    #
    # ⛔ Ca bon deu `GET`, `bang_ghi` RONG — chung chay tren ket noi bi
    #   PostgreSQL **chan ghi**.
    Tuyen("GET", f"{TIEN_TO}/sources", "nguon_ds",
          ("fls_source", "fls_khai_cot", "fls_chup", "fls_chup_nguon"),
          mo_ta="68 NGUON + `khai_version` hien hieu luc (`null` = ⛔ chua ai "
                "khai) + `chup_cuoi`. ⛔ KHONG co trang thai InActive/Closed — "
                "kho ⛔ khong co cot ay (`GAP-CHUP-02`), va cua KHAI THANG "
                "bang `trang_thai_nguon: null` chu ⛔ khong im lang bo truong"),
    Tuyen("GET", f"{TIEN_TO}/sources/{{source_id}}/khai-cot", "khai_cua_nguon",
          ("fls_source", "fls_khai_cot"),
          mo_ta="ban khai hien hieu luc + CA DAY `version` (ai khai · luc nao) "
                "— trang thai ③, **de XEM** (`BA-06` §7 ⓶b). ⛔ Chua khai ⇒ "
                "409 FLS-KHAI-KHONG-CO, ⛔ khong 404"),
    Tuyen("GET", f"{TIEN_TO}/chup", "chup_ds",
          ("fls_chup", "fls_chup_nguon", "fls_chup_dong", "fls_source",
           "fls_pm_line", "fls_run"),
          mo_ta="danh sach ANH CHUP, moi nhat truoc. `?lan=Bank|Cash` `?limit=`"),
    Tuyen("GET", f"{TIEN_TO}/chup/{{chup_id}}", "chup_mot",
          ("fls_chup", "fls_chup_nguon", "fls_chup_dong", "fls_source",
           "fls_pm_line", "fls_run"),
          mo_ta="mot ANH CHUP: dau + tung nguon (⭐ ke ca nguon ra **0 dong**) "
                "+ `?limit` dong dau de xem truoc — trang thai ②. ⛔ `limit` "
                "mac dinh **50**, ⛔ khong phai 'tat ca': mot anh co 8.365 dong"),
    # ⭐⭐ `QĐ-ITL-113` — BANG CHUNG thu tu ngay, ⛔ KHONG phai mot ket luan.
    #    Tuyen rieng chu ⛔ khong nhet vao `chup_mot`: `chup_mot` tra **50 dong
    #    dau**, con phep do nay phai soi **MOI dong** (bang chung quyet dinh co
    #    the o dong cuoi) ⇒ hai cau hoi khac nhau, hai cua.
    Tuyen("GET", f"{TIEN_TO}/chup/{{chup_id}}/thu-tu", "thu_tu_ds",
          ("fls_chup", "fls_chup_nguon", "fls_chup_dong", "fls_source",
           "fls_khai_cot", "fls_pm_line", "fls_run"),
          mo_ta="BANG CHUNG thu tu ngay tung nguon trong mot anh chup: da khai "
                "gi + de xuat cua may + SO DONG lam chung. ⛔ May ⛔ KHONG "
                "quyet — ke toan bam khai (QĐ-ITL-113)"),

    # ⭐⭐ `QĐ-ITL-113` — khai CHI thu tu ngay. Cua RIENG chu ⛔ khong dung
    #    `khai-cot`: ban khai la chi-THEM nen mot `version` moi phai cho DU 6
    #    truong ⇒ qua cua kia, man phai **doc `cot` roi gui lai** = mot chu
    #    trinh doc-sua-ghi, va ai khai `cot` moi trong khe do se bi de lai
    #    bang `cot` CU ma ⛔ khong cong nao thay. Cua nay doc+ghi mot giao dich.
    Tuyen("POST", f"{TIEN_TO}/sources/{{source_id}}/thu-tu", "ghi_thu_tu",
          ("fls_source", "fls_khai_cot"), bang_ghi=("fls_khai_cot",),
          ghi=True, doc_than=True,
          mo_ta="khai THU TU NGAY (`dmy`|`mdy`) — sinh `version` MOI, GIU "
                "nguyen `cot`. ⛔ Chua khai `cot` ⇒ 409, ⛔ KHONG tu dung mot "
                "ban khai rong de co cho dau (QĐ-ITL-113)"),
    # ⭐⭐⭐ `QĐ-ITL-117` — khai thu tu CA LO, **CHI** nguon TU CHUNG.
    #    ⛔⛔ Tuyen nay `doc_than=True` nhung than **⛔ KHONG mang `thu_tu`** —
    #    no do lai bang chung phia may chu roi ghi dung cai no do ra. ⇒ Man
    #    hinh ⛔ khong co duong nao khai `dmy` cho 27 nguon bang mot cu bam.
    #    Nguon ⛔ khong tu chung ⇒ NO ca lo, va nguon ay phai qua cua mot-nguon.
    Tuyen("POST", f"{TIEN_TO}/chup/{{chup_id}}/thu-tu", "khai_thu_tu_lo",
          ("fls_chup", "fls_chup_nguon", "fls_chup_dong", "fls_source",
           "fls_khai_cot", "fls_pm_line", "fls_run"), bang_ghi=("fls_khai_cot",),
          ghi=True, doc_than=True,
          mo_ta="khai THU TU NGAY cho NHIEU nguon — moi nguon theo bang chung "
                "CUA NO. ⛔ Than ⛔ KHONG duoc mang `thu_tu`. Nguon ⛔ khong tu "
                "chung / BAT DONG voi ban khai cua nguoi ⇒ 422 va ⛔ 0 ban "
                "khai moi (QĐ-ITL-117)"),
    Tuyen("POST", f"{TIEN_TO}/sources/{{source_id}}/khai-cot", "ghi_khai",
          ("fls_source", "fls_khai_cot"), bang_ghi=("fls_khai_cot",),
          ghi=True,
          mo_ta="ghi BAN KHAI ANH XA COT — sinh `version` MOI, ⛔ khong sua "
                "khai cu (DD-I10). Thieu truong trong 6 ⇒ 422 FLS-KHAI-THIEU"),

    # ⭐⭐ **Tuyen RIENG, ⛔ khong phai mot co.** Hai viec khac nhau ve **HAU
    # QUA** thi ⛔ khong duoc khac nhau bang **mot chu trong than yeu cau**:
    # mot co `?that=true` go thieu la **ghi that khi dinh thu**. Hai duong
    # rieng thi go nham duong **⛔ khong mat gi** — no chi soat.
    #
    # ⛔ `bang_ghi` RONG, va do la ca dac diem cua tuyen nay.
    # ⭐⭐⭐ `QĐ-ITL-111` + `112` — NAP CA LO. Tuyen RIENG chu ⛔ khong them
    #    mot khoa vao hai tuyen mot-nguon: khuon TRA VE khac han (bien ban GOP
    #    mang `so_nguon_vao`/`so_nguon_chua`, moi luat mang danh sach nguon ⛔
    #    khong dat). Mot tuyen tra HAI khuon la mot tuyen ma nguoi goi ⛔ khong
    #    biet minh dang doc khuon nao.
    Tuyen("POST", f"{TIEN_TO}/nap/lo/xem-truoc", "lo_xem_truoc",
          ("fls_source", "fls_khai_cot", "fls_nguon_dai",
           "fls_chup", "fls_chup_nguon", "fls_chup_dong",
           # ⭐⭐ Hai bang them 09/09 (`QĐ-ITL-119`): `chup.py::_dung` nay **DO**
           #    `so_dong` cua lan `PM` tu `fls_pm_line`, di qua
           #    `fls_run.chup_id` — vi lan ay ⛔ khong ghi vao `fls_chup_dong`
           #    *(`fls_pm_line` CHINH LA bang dong cua no)*.
           # ⚠ Cong `soi_bang_tuyen` bat dung **6 tuyen** khai thieu hai bang
           #   nay ngay lan chay dau. Ban khai la mot **ban do**, va mot ban do
           #   ve thieu duong thi nguy hon mot ban do ve thua.
           "fls_pm_line", "fls_run"), doc_than=True,
          mo_ta="SOAT CA LO ma ⛔ KHONG GHI — bien ban GOP 9 dong + tung "
                "nguon. `{chup_id, source_ids}`; ⛔ KHONG co mac dinh "
                "lay-het (QĐ-ITL-112)"),
    Tuyen("POST", f"{TIEN_TO}/nap/lo", "lo_nap",
          # ⛔ Bo bang nay do CONG `soi_bang_tuyen` bat, ⛔ khong do toi
          #    doan: ban dau toi khai thieu `fls_pm_line` va khai THUA
          #    `fls_journal`/`fls_mapping_master`. Mot ban do ve mot duong ⛔
          #    khong co cung sai bang mot ban do thieu duong.
          ("fls_itl", "fls_run", "fls_reject", "fls_le", "fls_pm_link",
           "fls_pm_line", "fls_queue_event", "fls_source", "fls_khai_cot",
           "fls_nguon_dai", "fls_chup", "fls_chup_nguon", "fls_chup_dong"),
          bang_ghi=("fls_itl", "fls_run", "fls_reject", "fls_le",
                    "fls_pm_link", "fls_pm_line", "fls_queue_event"),
          # ⛔ `ghi_nhat_ky=False` — Y HET tuyen `POST /nap` (no goi
          #    CUNG `nap_lo`). Ban dau toi khai `True`, va HAI cong noi
          #    hai dieu: `soi_bang_tuyen` bao SQL ⛔ khong cham
          #    `fls_journal`, `kiem_bang_tuyen` bao `ghi_nhat_ky=True`
          #    PHAI khai no ⇒ co sai, ⛔ khong phai ban khai bang sai.
          ghi=True, them_vao_so=True, doc_than=True,
          mo_ta="NAP CA LO: nguon sach VAO SO, nguon CHAN BI CHUA (QĐ-ITL-111) "
                "— MOT `run_id`, MOT giao dich cho ca lo"),
    Tuyen("POST", f"{TIEN_TO}/nap/xem-truoc", "xem_truoc",
          ("fls_source", "fls_khai_cot", "fls_nguon_dai",
           "fls_chup", "fls_chup_nguon", "fls_chup_dong",
           # ⭐⭐ Hai bang them 09/09 (`QĐ-ITL-119`): `chup.py::_dung` nay **DO**
           #    `so_dong` cua lan `PM` tu `fls_pm_line`, di qua
           #    `fls_run.chup_id` — vi lan ay ⛔ khong ghi vao `fls_chup_dong`
           #    *(`fls_pm_line` CHINH LA bang dong cua no)*.
           # ⚠ Cong `soi_bang_tuyen` bat dung **6 tuyen** khai thieu hai bang
           #   nay ngay lan chay dau. Ban khai la mot **ban do**, va mot ban do
           #   ve thieu duong thi nguy hon mot ban do ve thua.
           "fls_pm_line", "fls_run"), doc_than=True,
          mo_ta="SOAT ma ⛔ KHONG GHI — tra bien ban 9 luat, moi luat kem "
                "`da_do` (do duoc 0 thu ⇒ ⛔ KHONG DAT)"),
    # ⚠ `fls_pm_line`/`fls_pm_link` khai o day vi phep NAP dung lai
    #   `repo/chay_nap.chay()` — cho DUY NHAT giu chong trung + cong bon duong
    #   + mot giao dich. Ham do co **mot nhanh GHEP LENH** ma tuyen nay ⛔ khong
    #   bao gio di qua (`pm=None`), nhung phep do cua `soi_bang_tuyen` la **do
    #   TINH** va **VUOT co chu dich**: no gom ca bang chi cham o nhanh khac.
    #
    #   ⛔ Cach chua ⛔ KHONG phai noi cong ra — ban khai la mot **BAN DO**, va
    #   *"khai du hon la khai thieu"* (loi van cua chinh cong do). Khai thieu
    #   thi cong dang canh mot ban do CU; khai du thi ban do rong hon su that,
    #   nhung ⛔ khong che giau duong nao.
    Tuyen("POST", f"{TIEN_TO}/nap", "nap",
          ("fls_source", "fls_khai_cot", "fls_nguon_dai",
           "fls_chup", "fls_chup_nguon", "fls_chup_dong",
           "fls_run", "fls_itl", "fls_reject",
           "fls_le", "fls_queue_event", "fls_pm_line", "fls_pm_link"),
          bang_ghi=("fls_run", "fls_itl", "fls_reject", "fls_le",
                    "fls_queue_event", "fls_pm_line", "fls_pm_link"),
          them_vao_so=True, ghi=True,
          mo_ta="nap that ⇒ `run_id` + CUNG mot bien ban voi xem-truoc. Hang "
                "CHAN do ⇒ 422 va ⛔ 0 dong vao so; hang CO do ⇒ 201 va dong "
                "bi co vao HANG CHO CO LY DO (chung la tien that)"),
)


def tim(phuong_thuc: str, duong: str) -> tuple[Tuyen, dict[str, str]] | None:
    """Tuyen khop, hay `None`. Duong khop ma phuong thuc khong ⇒ tra 405."""
    for t in BANG_TUYEN:
        p = t.khop(duong)
        if p is not None and t.phuong_thuc == phuong_thuc:
            return t, p
    return None


def duong_ton_tai(duong: str) -> bool:
    return any(t.khop(duong) is not None for t in BANG_TUYEN)


def kiem_bang_tuyen(bang: tuple[Tuyen, ...] = BANG_TUYEN) -> list[str]:
    """⛔ Cong. Rong = dat. ⛔ Khong bao gio tra "OK" — tra danh sach vi pham."""
    loi: list[str] = []

    thay: set[tuple[str, str]] = set()
    for t in bang:
        # ⓐ ⛔ khong duong nao PUT/DELETE/PATCH nham vao so
        if t.phuong_thuc in PHUONG_THUC_CAM_LEN_SO and SO in t.bang:
            loi.append(f"{t.phuong_thuc} {t.duong} nham vao {SO} — "
                       f"`INV-I08` cam: sua chi bang but toan moi")
        # ⓐ' ⛔⛔ VA khong duong nao — DU PHUONG THUC GI — duoc GHI vao so.
        #     Phep kiem ⓐ theo phuong thuc ⛔ khong bat duoc `POST .../adjust`
        #     ghi thang vao `fls_itl`, va do dung la duong de nhat.
        if SO in t.bang_ghi and not t.them_vao_so:
            loi.append(f"{t.phuong_thuc} {t.duong} khai GHI vao {SO} — "
                       f"`INV-I08`: so la append-only, sua chi bang but toan "
                       f"moi trong `fls_adjustment`")
        # ⓐ''' Ngoai le `them_vao_so` phai HEP: xem loi van o `Tuyen`.
        if t.them_vao_so:
            if SO not in t.bang_ghi:
                loi.append(f"{t.phuong_thuc} {t.duong} khai `them_vao_so` ma "
                           f"⛔ khong he ghi {SO} — mot ngoai le ⛔ khong dung "
                           f"den la mot ngoai le phai GO")
            if t.phuong_thuc != "POST":
                loi.append(f"{t.phuong_thuc} {t.duong}: `them_vao_so` chi cho "
                           f"`POST`. `PUT`/`DELETE`/`PATCH` len so van CAM tuyet doi")
            if "fls_run" not in t.bang_ghi:
                loi.append(f"{t.phuong_thuc} {t.duong}: them dong vao so ma "
                           f"⛔ khong ghi `fls_run` — dong so ⛔ khong co lan nap "
                           f"la dong MAT LINEAGE (`INV-I05`/`I12`)")
        # ⓐ'' bang_ghi phai la con cua bang, va `ghi` phai khop bang_ghi
        la_ghi = [b for b in t.bang_ghi if b not in t.bang]
        if la_ghi:
            loi.append(f"{t.duong} khai ghi bang khong co trong `bang`: {la_ghi}")
        if bool(t.bang_ghi) != bool(t.ghi):
            loi.append(f"{t.duong} tu mau thuan: ghi={t.ghi} ma "
                       f"bang_ghi={t.bang_ghi} — mot duong noi minh khong ghi "
                       f"ma co bang ghi la mot duong khong ai canh")
        # ⓑ moi duong ghi phai DE LAI VET (cho kiem soat duy nhat con lai
        #    sau khi `QĐ-ITL-27` khai tu nguoi hau kiem)
        if t.ghi and not (set(t.bang_ghi) & BANG_CO_VET):
            loi.append(f"{t.phuong_thuc} {t.duong} ghi ma ⛔ khong de lai VET "
                       f"— `AUD-1`. Phai ghi vao mot trong "
                       f"{sorted(BANG_CO_VET)}")
        # `ghi_nhat_ky` la mot khai bao, nen no phai KHOP thuc te.
        if t.ghi_nhat_ky != ("fls_journal" in t.bang_ghi):
            loi.append(f"{t.duong} tu mau thuan: ghi_nhat_ky={t.ghi_nhat_ky} "
                       f"ma bang_ghi={t.bang_ghi}")
        # ⓒ tien to
        if not t.duong.startswith(TIEN_TO + "/"):
            loi.append(f"{t.duong} khong bat dau bang {TIEN_TO}/ "
                       f"(⛔ khong dung /api/voi/ hay /api/fps/)")
        # ⓓ ⛔ khong bang la nao
        la = [b for b in t.bang if b not in BANG_CHO_PHEP]
        if la:
            loi.append(f"{t.duong} cham bang ngoai `fls_*`: {la} — "
                       f"`QĐ-ITL-45` FLS chi doc kho rieng")
        if not t.bang:
            loi.append(f"{t.duong} khong khai bang nao — mot duong khong noi no "
                       f"cham gi la mot duong cong khong quet duoc")
        # ⓔ trung
        khoa = (t.phuong_thuc, t.duong)
        if khoa in thay:
            loi.append(f"trung tuyen: {t.phuong_thuc} {t.duong}")
        thay.add(khoa)
        # ⓕ phuong thuc biet
        if t.phuong_thuc not in {"GET", "POST", "PUT", "DELETE", "PATCH"}:
            loi.append(f"phuong thuc la: {t.phuong_thuc!r}")
    return loi
