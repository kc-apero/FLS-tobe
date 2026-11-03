"""`B0` — DO LAI MAU SO cua tac vu ①, va doi chieu hai cau *"chua ghep"*.

⛔⛔ **Vi sao module nay ra doi, va no ⛔ KHONG phai mot bang thong ke cho dep.**

Lo trinh `13_LO_TRINH_HAI_TAC_VU` §0 ⓸ ghi mot con so va goi no la *"mot mau
thuan noi bo"*: `work_status='UNMAPPED'` dem **7.682** dong, con *"⛔ khong co
moi noi"* dem **7.329** — **lech 353**. Phep do o day tra loi cau do, va no
tra loi **khac** cai ma tep lo trinh doan:

  ⓐ `353` la **HIEU** cua hai nhom nguoc chieu, ⛔ khong phai mot nhom.
    `778` dong DA NOI ma nhan con `UNMAPPED`, va `425` dong nhan `ok` ma
    ⛔ CHUA NOI. `778 - 425 = 353`. ⇒ Con so `353` **che di 1.203 dong** —
    no noi nho hon su that **3,4 lan**.
  ⓑ Va do ⛔ **khong phai mot mau thuan**: hai cot tra loi **hai cau hoi khac
    nhau**. `work_status` tra loi *"may co suy du 5 truong phan loai khong"*
    (`fls/ledger/build.py`, `INV-I16`, dong bang luc nap). `fls_moi_noi` tra
    loi *"dong tien nay da noi voi mot dong lenh chi chua"*. Mot dong co the
    du phan loai ma chua noi lenh chi — **425 dong dung la the**, va ca 425
    dong deu co `hd`+`pay_type`+`cdt1`+`doc_no` (do 09/09).

⇒ Ket luan cua `B0` **⛔ khong phai** *"va cho khop"*: hai con so **dung PHAI
  khac nhau**, va cai sai la **cau van** dem chung ra so sanh. Bai hoc lap lai:
  mot con so **HIEU** giua hai phep dem la mot con so **⛔ khong ai kiem duoc**
  — no nho di khi ca hai ve cung tang.

★★ **Va thu hai `B0` chua:** MAU SO. Moi ty le do phu tu 27/08 den nay deu
chia cho **10.030** *(ca so)*. Do 09/09: dong ghep duoc **don han ve ve
`PS Co`** — `31,1%` so voi `7,8%` ⇒ ve `PS Co` la **ve cua lenh chi**, va
mau so that cua tac vu ① la **8.246**, ⛔ khong phai 10.030.

★★★ **Va thu ba `B0` chua, va no la thu dat nhat: con so `584`.**

Lo trinh §0 ⓵ ghi *"**584** dong TU CHUNG (8,0%) ⇒ cua ghep LO nhan duoc ngay"*.
Phep do o day noi con so ay la **68 (0,9%)** — nho hon **8,6 lan**. Vi sao:

  ⓐ Ban do cu dinh nghia tu chung la *"dung MOT ung vien bac `ma` chua bi
    ghep"* — no do bang luat cua **danh sach ung vien** *(`ung_vien_pm`, mot
    cau DOC de nguoi CHON)*, ⛔ **khong** bang luat cua **cua GHI**
    (`ghep_lenh`). Cua ghi con bon cong nua: ⓔ cung tien te · ⓒ chua bi ghep ·
    ⓖ da duyet · ⓕ **Σ = tien bank trong dung sai `QĐ-ITL-63`**.
  ⓑ Do 09/09 tren dung tap **584** dong ay: **301** dong bi cong ⓕ tu choi
    *(mot ma tham chieu ung voi mot so tien khac — do hinh cai lech: chi
    **16/491** nam trong khoang phi bank, con lai lech **hang chuc lan**)*,
    **202** dong bi cong ⓔ *(khac tien te)*, **30** dong bi cong ⓖ.
  ⓒ Va mot lan sua **nguoc chieu**: luat cu *"dung MOT dong"* con **chat hon**
    cua ghi, vi `ghep_lenh` nhan **N dong** va chi doi `Σ`. Nen o day tu chung
    lay **CA CHUM** cung ma. *(Do tren kho that: moi chum tu chung hom nay co
    kich thuoc **1** — nen luat rong hon ⛔ khong thay doi con so, nhung no
    ⛔ khong con la mot luat SAI.)*

⇒ Bai hoc, va no la **lan thu hai** trong hai ngay: *"do QUAN HE thi goi ham
  that"* ⛔ **khong du** — phai goi **dung ham cua CAU HOI**. Cau hoi la *"cu
  bam LO se ghep duoc bao nhieu dong"*, nen luat phai la luat cua **cua GHI**.
  Toi da goi mot ham that, va no la ham **tra loi cau khac**.

★ Va ⓓ: phep do o day tra ket qua bang **BA cau** *(so + PM + moi noi)* ⇒ ~1
  giay, thay vi `ung_vien_pm` **7.329 lan** (~40 giay). Dung viec ma `B0` duoc
  dat ra de lam: *"bien mot anh chup thanh mot phep do chay duoc moi luc"* —
  va cung nho no chay duoc moi luc ma con so `584` moi bi bat.

⛔⛔ **Va no ⛔ KHONG go lai luat `bac 'ma'` bang tay.** Menh de nhan ung vien
   bac `ma` khai **mot lan** o `doc_bao_cao.DK_BAC_MA` va **ca hai** cau dung
   chung no.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

from fls.adapters.pm_join import canon_ref, dung_sai_ghep_tay
from fls.canon.tien_te import ma_tien_te
from fls.repo.anh_pm import anh_pm_hieu_luc
from fls.repo.doc_bao_cao import DK_BAC_MA
from fls.repo.pham_vi import PhamVi

# ── ⓐ VE cua so: `PS Co` hay `PS No` ────────────────────────────────────
#
# ⛔⛔ Bon nhom, ⛔ **khong ba**. Do 09/09 tren kho that: `CA HAI` = 0 va
# `KHONG VE NAO` = 0. Nhung mot phep phan hoach **bo mat** hai nhom rong ay se
# lam `Σ != tong` ngay dong dau tien co ca hai ve — va no se **im lang**, vi
# tong lay tu `count(*)` chu ⛔ khong tu Σ cac nhom. ⇒ Giu du bon, va co bai
# ghim `Σ bon nhom == count(*)`.
_SQL_VE = """
SELECT CASE WHEN COALESCE(i.ps_co,0) <> 0 AND COALESCE(i.ps_no,0) <> 0
              THEN 'ca_hai'
            WHEN COALESCE(i.ps_co,0) <> 0 THEN 'ps_co'
            WHEN COALESCE(i.ps_no,0) <> 0 THEN 'ps_no'
            ELSE 'khong_ve_nao' END                       AS ve,
       count(*)::int                                      AS so_dong,
       count(*) FILTER (WHERE m.itl_id IS NOT NULL)::int   AS da_noi,
       count(*) FILTER (WHERE m.itl_id IS NULL)::int       AS chua_noi
  FROM fls_itl i
  LEFT JOIN (SELECT DISTINCT itl_id FROM fls_moi_noi) m ON m.itl_id = i.itl_id
 WHERE {dk}
 GROUP BY 1
"""

# ── ⓑ bon O cua bang cheo `work_status` × `co moi noi` ──────────────────
_SQL_NHAN = """
SELECT (i.work_status = 'UNMAPPED')                AS nhan_unmapped,
       (m.itl_id IS NOT NULL)                      AS co_moi_noi,
       count(*)::int                               AS so_dong
  FROM fls_itl i
  LEFT JOIN (SELECT DISTINCT itl_id FROM fls_moi_noi) m ON m.itl_id = i.itl_id
 WHERE {dk}
 GROUP BY 1, 2
"""

# ⭐ **Ten ly do cho tung o**, ⛔ khong mot o nao ten *"khac"*. Cong ra cua `B0`
#   doi dung dieu nay: mot o ⛔ khong co ten la mot o ⛔ khong ai giai thich
#   duoc, va no se duoc doc thanh *"loi"* trong lan doc lai dau tien.
LY_DO_NHAN: dict[tuple[bool, bool], tuple[str, str]] = {
    (True, False): (
        "chua_phan_loai__chua_noi",
        "may ⛔ khong suy du 5 truong phan loai VA ⛔ chua noi lenh chi — "
        "day la DICH THAT cua tac vu ①"),
    (False, True): (
        "da_phan_loai__da_noi",
        "du phan loai VA da noi lenh chi — trang thai HOAN CHINH"),
    (True, True): (
        "da_noi__nhan_con_UNMAPPED",
        "DA noi lenh chi ma nhan van la `UNMAPPED`: `work_status` bi DONG BANG "
        "luc nap (`fls/ledger/build.py`) va phep ghep ⛔ khong ghi vao "
        "`fls_itl` (`INV-I08`) ⇒ nhan ⛔ khong bao gio duoc tinh lai. "
        "⛔ Day ⛔ KHONG phai loi du lieu — no la HE QUA cua so chi-them"),
    (False, False): (
        "du_phan_loai__chua_noi",
        "du 5 truong phan loai nen ⛔ khong vao hang cho, nhung ⛔ CHUA noi "
        "lenh chi. Hai cau hoi KHAC NHAU: `work_status` do PHAN LOAI, "
        "`fls_moi_noi` do MOI NOI ⇒ mot dong du phan loai van co the chua noi"),
}

# ── ⓒ vi sao mot dong ⛔ chua noi duoc: bon nhom, bon viec KHAC NHAU ────
LY_DO_VI_SAO: dict[str, str] = {
    "khong_co_so_chung_tu":
        "⛔ khong co `doc_no` ⇒ ⛔ khong khoa nao de ghep theo ma",
    "ma_khong_chuan_hoa_duoc":
        "co `doc_no` ma `canon_ref` tra `None` (ma loi / rong sau khi bo ky "
        "tu) ⇒ viec la o BO CHUAN HOA",
    "PM_khong_mang_ma_nay":
        "ma chuan hoa duoc ma ⛔ KHONG mot dong PM nao trong cung lan nap mang "
        "ma ay ⇒ viec la NAP PM (moc `A3`), ⛔ khong phai ma va ⛔ khong phai "
        "giao dien",
    "PM_co_ma_nay":
        "PM CO mang ma ay ⇒ dong nay ghep duoc ngay; xem `tu_chung` de biet "
        "bao nhieu dong ghep duoc **⛔ khong can nguoi chon**",
}

# ── ⓓ vi sao mot dong `PM_co_ma_nay` van ⛔ KHONG tu chung ──────────────
#
# ⛔⛔ **Bon ten nay soi guong BON CONG cua `ghep_lenh`**, theo **dung thu tu**
# ma no kiem: ⓔ khac tien te · ⓒ da ghep · ⓖ chua duyet · ⓕ lech tong. Doi thu
# tu la doi TEN cua ly do — mot dong khac tien te se bi bao la *"lech tien"*, va
# nguoi doc se di sua dung sai thay vi di sua tien te. Toi da mac dung loi do
# trong ban dau cua ham nay: **202 dong** bi dan nhan `lech_tien` trong khi
# chung khac TIEN TE.
LY_DO_KHONG_TU_CHUNG: dict[str, str] = {
    "khac_tien_te":
        "co dong PM mang ma ay nhung ⛔ khong dong nao CUNG TIEN TE voi dong "
        "tien ⇒ `ghep_lenh` ⓔ tu choi: ⛔ khong cong hai don vi khac nhau",
    "ung_vien_da_bi_ghep":
        "moi dong PM cung ma + cung tien te DA bi ghep cho dong tien khac ⇒ "
        "hoac ma tham chieu trung, hoac mot moi noi truoc do sai",
    "co_dong_chua_duyet":
        "chum co it nhat mot dong `status` ⛔ khong phai `Approve` ⇒ "
        "`ghep_lenh` ⓖ doi `force` kem ly do, va mot cu bam LO ⛔ khong bao "
        "gio duoc mang `force`",
    "mot_dong_lech_tien":
        "dung MOT dong PM mang ma ay ma so tien lech khoi tien bank qua dung "
        "sai `QĐ-ITL-63` ⇒ mot ma tham chieu dang ung voi mot so tien KHAC "
        "(phi bank rieng dong, hay tra tung phan) — viec cua NGUOI, ⛔ khong "
        "phai cua may",
    "chum_lech_tien":
        "≥2 dong PM cung ma, va Σ CA CHUM van lech tien bank ⇒ may se phai "
        "**chon mot tap con**, va no ⛔ khong duoc chon ho ai",
}

# ⚠ Bon nhom `vi_sao` PHAI phu het, nen thu tu xet la mot phan cua luat:
# `khong_co_so_chung_tu` TRUOC `ma_khong_chuan_hoa_duoc` (khong co gi thi
# ⛔ khong chuan hoa duoc gi), roi moi den hai nhom PM. ⛔ Dung doi thu tu.
_THU_TU_VI_SAO = ("khong_co_so_chung_tu", "ma_khong_chuan_hoa_duoc",
                  "PM_khong_mang_ma_nay", "PM_co_ma_nay")

_SQL_SO_CHUA_NOI = """
SELECT i.itl_id, i.run_id, i.doc_no, i.curr,
       COALESCE(i.ps_no,0) + COALESCE(i.ps_co,0) AS tien,
       (COALESCE(i.ps_co,0) <> 0 AND COALESCE(i.ps_no,0) = 0) AS la_ps_co
  FROM fls_itl i
 WHERE {dk}
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)
 ORDER BY i.itl_id
"""

# ⭐⭐ Cau UNG VIEN theo LO. Menh de bac `ma` lay tu `DK_BAC_MA` — **cung mot
# chuoi** ma `ung_vien_pm` dung. ⛔ Dung go lai `l.ref_canon = s.ma` o day.
_BAC_MA_LO = DK_BAC_MA.format(s="s", l="l")

# ⛔⛔ **Vi sao NOI CHUOI (`+`) chu ⛔ khong `.replace()`.** Cong
# `tools/soi_bang_tuyen.py` doi chieu **ban khai bang tuyen** voi **SQL that**
# bang cach doc TINH cay ma nguon: no suy duoc gia tri cua mot hang chuoi khi no
# la chuoi thuong, f-string, hay mot phep **cong**. Mot hang dung
# `"""...""".replace(...)` la mot `Call` ⇒ cong suy ⛔ **khong ra chuoi nao** ⇒
# hai bang `fls_pm_line`/`fls_moi_noi` trong cau nay **tang hinh** voi cong.
#
# ⭐ Va cong da bat dung dieu do ngay lan chay dau: *"`bang` khai
#   ['fls_pm_line'] ma SQL ⛔ khong cham"*. Cong bao theo chieu **AN TOAN**
#   *(khai thua thi bao)*, nen no ⛔ khong im lang — nhung neu ai them mot cau
#   `INSERT` vao mot hang kieu `.replace()` thi cong se **⛔ khong thay**.
#   ⇒ Chua o **ma nguon**, ⛔ khong noi cong.
_SQL_UNG_VIEN_LO = """
WITH s AS (
  SELECT * FROM unnest(%(ids)s::bigint[], %(mas)s::text[])
              AS t(itl_id, ma)
)
SELECT s.itl_id, l.pm_line_id, l.amount, l.curr, l.status,
       (SELECT count(*)::int FROM fls_moi_noi k
         WHERE k.pm_line_id = l.pm_line_id) AS da_ghep
  FROM s JOIN fls_pm_line l ON l.run_id = %(run_pm)s
 WHERE """ + _BAC_MA_LO


# ⭐⭐⭐ TRAN CUNG cua tac vu ① — them 2026-09-09 (`B1`).
#
# ⛔⛔⛔ **Vi sao phep do nay o DAY, va vi sao no tung o SAI CHO.**
#
# Sang 09/09 toi do tran nay **trong `tools/kiem_so_song.py`** — tuc trong
# **CONG**, ⛔ khong trong lang nghiep vu. Nghia la kho co **HAI ban su that**
# ve mot con so ma ca mot moc phu thuoc vao: mot ban cho cong doc, va ⛔ khong
# ban nao cho **man hinh** hay **cua API** doc. Dung lop loi da lam
# *"584 vs 68"*: hai phep dem cho **hai tap khac nhau** cua cung mot cau hoi.
#
# ⇒ Dat o day, canh `_SQL_VE`, va cong doc **qua `do_mau_so`**.
#
# ⭐ Y nghia: mot dong lenh chi da ghep cho dong tien nay thi ⛔ **khong ghep
#   lai** cho dong khac. Nen so dong tien co the noi them **⛔ khong bao gio
#   vuot** so dong lenh chi CON RANH trong anh hieu luc.
#
# ⛔ `run_id = %(run_pm)s` — **anh HIEU LUC**, cung anh ma cua ghep dung. Do
#   tren `fls_pm_line` ⛔ khong loc anh se cong ca **hai** anh lai
#   *(3.703 + 3.772)* va cho mot tran **cao gap doi su thuc**.
_SQL_TRAN = """
SELECT count(*)::int AS anh_tong,
       count(*) FILTER (
         WHERE EXISTS (SELECT 1 FROM fls_moi_noi m
                        WHERE m.pm_line_id = l.pm_line_id))::int AS da_dung
  FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s
"""


# ══ ⭐⭐⭐ PHIA PM — mau so THAT cua viec ghep (them 2026-09-09) ══
#
# ⛔⛔⛔ **Owner doi CHIEU do, 09/09:** *"Trans map vao PM (so luong Trans von
#    nhieu hon PM; ⛔ ko can question cac Trans khong duoc map)"*.
#
# ⇒ Moi con so do phu tu 27/08 den 09/09 do **SAI PHIA**. Chung chia cho
#   `PS Co` = `8.246` dong TIEN, va tra ve `31,1%` — mot con so doc ra la
#   *"that bai"*. Nhung `10.030` dong tien vs `3.772` dong lenh la **dung nhu
#   thiet ke**: mot dong lenh chi ⛔ khong tuong ung mot giao dich bank.
#   ⇒ Cau *"con bao nhieu viec"* phai chia cho **so DONG LENH**, va viec that
#   la nhung dong lenh **⛔ chua tim duoc tien cua no**.
#
# ⭐ Va no lam **tan** ca khai niem *"tran cung 47,4%"*: `tran` ⛔ khong phai
#   mot gioi han cua thanh cong, no chi la **ty le kich thuoc hai tap**. Giu
#   `tran` lai vi no van tra loi mot cau THAT *(*"⛔ dung hua do phu `PS Co`
#   len 100%"*)*, nhung no **thoi la con so de ra quyet dinh**.
_SQL_PM_PHU = """
SELECT count(*)::int AS dong_lenh,
       count(*) FILTER (WHERE k.co)::int              AS da_co_tien,
       count(DISTINCT l.pm_slip_id)::int              AS phieu,
       count(DISTINCT l.pm_slip_id) FILTER (WHERE k.co)::int AS phieu_da_co,
       -- ⭐⭐⭐ BA con so PHIEU, va chung tra loi BA cau hoi khac nhau. Do
       --    09/09: **1.500** phieu · **990** co >=1 dong da noi · **698** con
       --    dong CHUA noi · **510** ⛔ chua noi gi ca · **188** NUA NO NUA KIA.
       --
       -- ⛔⛔ Toi da viet **510** vao bon tep tai lieu voi nhan *"viec con
       --    lai"* — va do la con so SAI cho cau ay: `510` la *"phieu ⛔ chua
       --    noi GI CA"*, con *"viec con lai"* phai la **698**. Chenh **188**
       --    phieu **da noi mot phan** — dung loai phieu **de bo sot nhat**,
       --    vi no ⛔ khong con nam trong nhom *"chua lam gi"*.
       count(DISTINCT l.pm_slip_id) FILTER (WHERE NOT k.co)::int
                                                      AS phieu_con_dong_chua,
       count(*) FILTER (WHERE NOT k.co
                          AND l.status IS DISTINCT FROM 'Approve')::int
                                                      AS chua_co_va_chua_duyet
  FROM fls_pm_line l
  CROSS JOIN LATERAL (
    SELECT EXISTS (SELECT 1 FROM fls_moi_noi m
                    WHERE m.pm_line_id = l.pm_line_id) AS co) k
 WHERE l.run_id = %(run_pm)s
"""

# ⛔ Tien te cua nhung dong lenh CHUA co tien — **⛔ khong co dong "tong"**.
#   Cong hai don vi ra mot con so la dung cai sai da de ra *"310 dong phu
#   90%"* (that ra **799**).
_SQL_PM_CHUA_THEO_TE = """
SELECT upper(COALESCE(l.curr, '?')) AS te, count(*)::int AS so_dong,
       COALESCE(SUM(l.amount), 0) AS tien
  FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m
                    WHERE m.pm_line_id = l.pm_line_id)
 GROUP BY 1 ORDER BY 2 DESC
"""

# ⛔⛔ Ma tham chieu cua dong lenh CHUA co tien, va so chung tu cua dong tien
#    ⛔ CHUA noi. Phep giao lam o **PYTHON** — xem `_pm_ghep_duoc_ngay`.
_SQL_PM_REF_CHUA = """
SELECT l.ref_canon FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s AND l.ref_canon IS NOT NULL
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m
                    WHERE m.pm_line_id = l.pm_line_id)
"""

_SQL_ITL_DOC_NO_CHUA_NOI = """
SELECT i.doc_no FROM fls_itl i
 WHERE i.doc_no IS NOT NULL AND {dk}
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)
"""


def _dong(cur) -> list[dict[str, Any]]:
    ten = [x.name for x in cur.description]
    return [dict(zip(ten, r)) for r in cur.fetchall()]


def _pct(a: int, b: int) -> str | None:
    """`a/b` theo phan tram, mot chu so thap phan. `None` neu `b == 0`.

    ⛔ Tra `None` chu ⛔ **khong tra `0`**: *"0% cua 0 dong"* la mot cau tra loi
    SAI cho mot cau hoi ⛔ khong co nghia — va man hinh se in `0%` ma
    ⛔ khong ai biet mau so rong.
    """
    return None if not b else f"{a * 100 / b:.1f}".replace(".", ",")


def ds_tu_chung(conn, pv: PhamVi, itl_ids: list[int] | None = None,
                ) -> dict[str, Any]:
    """Cac dong **TU CHUNG**: dung MOT dong PM mang cung ma, chua bi ghep, da
    duyet, va tien nam trong dung sai.

    ⛔⛔ **Vi sao dinh nghia phai chat den the.** Cua ghep LO (`B2`) nhan tap
    nay **⛔ khong hoi nguoi mot cau nao**. Nen moi dieu kien ma `ghep_lenh` se
    kiem (`ⓒ` da ghep · `ⓔ` khac tien te · `ⓕ` lech tong · `ⓖ` chua duyet) ma
    o day ⛔ **khong** kiem truoc, se thanh mot cu **422 CA LO**: mot dong xau
    chan 583 dong tot. ⇒ Tap `tu_chung` la tap ma `ghep_lenh` **chac chan nhan**.

    ⛔ Va no van **⛔ khong tu ghep**: `ghep_lenh` van la noi duy nhat kiem lai.
    Ham nay chi **thu hep dau vao**, ⛔ khong thay the cong nao.

    `itl_ids=None` ⇒ **moi** dong chua noi trong pham vi *(dung cho phep do)*.
    Co danh sach ⇒ chi nhung dong ay *(dung cho cua ghep lo)*.

    Tra:
      `tu_chung`  — `{itl_id: [pm_line_id, ...]}` — CA CHUM cung ma, da sap
      `khong`     — `{itl_id: ma_ly_do}` cho dong CO ma ma ⛔ khong tu chung
      `ngoai`     — `itl_id` nguoi goi dua ma ⛔ khong nam trong tap chua noi
      `vi_sao`    — dem theo bon nhom `LY_DO_VI_SAO`
    """
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(_SQL_SO_CHUA_NOI.format(dk=dk), ts)
        so = _dong(cur)

    xin = None if itl_ids is None else {int(x) for x in itl_ids}
    if xin is not None:
        co = {r["itl_id"] for r in so}
        ngoai = sorted(xin - co)
        so = [r for r in so if r["itl_id"] in xin]
    else:
        ngoai = []

    # ⚠ `canon_ref` chay BEN PYTHON — day la ban chuan hoa DUY NHAT.
    ma_cua: dict[int, str] = {}
    vi_sao: dict[str, list[int]] = {k: [] for k in _THU_TU_VI_SAO}
    for r in so:
        if r["doc_no"] is None or not str(r["doc_no"]).strip():
            vi_sao["khong_co_so_chung_tu"].append(r["itl_id"])
            continue
        ma = canon_ref(r["doc_no"])
        if not ma:
            vi_sao["ma_khong_chuan_hoa_duoc"].append(r["itl_id"])
            continue
        ma_cua[r["itl_id"]] = ma

    # ⛔⛔ **MOT anh PM cho ca lo — anh DANG HIEU LUC**, ⛔ khong con mot anh
    #    rieng cho tung dong theo `run_id` cua no (`QĐ-ITL-119`, xem
    #    `fls/repo/anh_pm.py`). Bam theo `run_id` cua dong tien nghia la du
    #    lieu lenh chi MOI ⛔ khong bao gio giup duoc dong tien CU.
    #
    # ⚠ Va no PHAI la **cung mot anh** ma `ung_vien_pm` va `ghep_lenh` nhin:
    #   ba noi nhin ba anh khac nhau thi man hinh, phep do, va cu ghi thuc su
    #   se noi ve ba tap khac nhau — va ca ba deu "dung".
    uv: dict[int, list[dict[str, Any]]] = {}
    run_pm = anh_pm_hieu_luc(conn, pv)
    if ma_cua and run_pm is not None:
        ids = sorted(ma_cua)
        with conn.cursor() as cur:
            cur.execute(_SQL_UNG_VIEN_LO,
                        {"ids": ids, "mas": [ma_cua[i] for i in ids],
                         "run_pm": run_pm})
            for x in _dong(cur):
                uv.setdefault(x["itl_id"], []).append(x)

    tien_cua = {r["itl_id"]: (r["tien"], r["curr"]) for r in so}
    ps_co_cua = {r["itl_id"]: bool(r["la_ps_co"]) for r in so}
    tu_chung: dict[int, list[str]] = {}
    khong: dict[int, str] = {}
    for i in sorted(ma_cua):
        ds = uv.get(i, [])
        if not ds:
            vi_sao["PM_khong_mang_ma_nay"].append(i)
            continue
        vi_sao["PM_co_ma_nay"].append(i)
        tien, cur_so = tien_cua[i]
        # ⭐ `WO-042 (c)` *(`BA-07` v3.11)*: **cùng** `ma_tien_te` *(tập 30 ký tự
        #   `TAP_TRANG_TIEN_TE`)* — trước: `strip().upper()` viết tay *(29, thiếu
        #   `U+FEFF`)*: cửa ghi coi ``U+FEFF`+`VND`` là một mã **khác** VND.
        te = ma_tien_te(cur_so)
        # ⓔ cung tien te — `ghep_lenh` kiem dieu nay **truoc** moi phep cong
        cung_te = [x for x in ds if ma_tien_te(x["curr"]) == te]
        if not cung_te:
            khong[i] = "khac_tien_te"
            continue
        # ⓒ chua bi ghep cho dong khac
        ranh = [x for x in cung_te if not x["da_ghep"]]
        if not ranh:
            khong[i] = "ung_vien_da_bi_ghep"
            continue
        # ⓖ ca chum phai DA DUYET — mot cu bam LO ⛔ khong mang `force`
        if any((x["status"] or "").strip().lower() != "approve" for x in ranh):
            khong[i] = "co_dong_chua_duyet"
            continue
        # ⓕ Σ CA CHUM = tien bank.
        #
        # ⛔⛔ **Vi sao la CA CHUM chu ⛔ khong phai "dung mot dong".** Ban dau
        # toi dinh nghia tu chung la *"dung MOT ung vien bac `ma`"* — mot luat
        # **chat hon cua that**: `ghep_lenh` nhan **N dong** va chi doi
        # `Σ amount = tien bank`. Mot cu chuyen tien tra hai dong lenh cung ma
        # tham chieu la chuyen thuong, va luat cu bo mat no.
        #
        # ⚠ Va no lay **CA chum**, ⛔ khong bao gio mot **tap con**: neu ba dong
        # mang cung ma ma chi hai trong ba cong dung tien bank, thi chon hai
        # dong nao la mot **quyet dinh nghiep vu** ⇒ may tu choi (`chum_lech_tien`).
        t = Decimal(str(tien or 0))
        tong = sum((x["amount"] or Decimal(0) for x in ranh), Decimal(0))
        if abs(tong - t) > dung_sai_ghep_tay({te}, t):
            khong[i] = ("mot_dong_lech_tien" if len(ranh) == 1
                        else "chum_lech_tien")
            continue
        tu_chung[i] = sorted(x["pm_line_id"] for x in ranh)

    return {
        "tu_chung": tu_chung,
        "khong": khong,
        "ngoai": ngoai,
        "so_dong_xet": len(so),
        "vi_sao": {k: len(v) for k, v in vi_sao.items()},
        # ⭐ Anh PM da dung — man hinh phai noi ra: hai anh khac nhau cho
        #   **hai tap tu chung khac nhau**.
        "anh_pm": run_pm,
        "vi_sao_ps_co": {
            k: sum(1 for i in v if ps_co_cua.get(i)) for k, v in vi_sao.items()},
        "pham_vi": pv.mo_ta(),
    }


def _tran(ps_co: dict[str, Any] | None, tho: dict[str, Any],
          run_pm: str | None) -> dict[str, Any]:
    """TRAN CUNG cua do phu ve `PS Co`, va do phu **tren tran** ay.

    ⭐⭐⭐ **Con so quan trong nhat cua tac vu ①, va no ⛔ khong phai mot muc
    tieu — no la mot GIOI HAN VAT LIEU.**

    `31,1%` doc mot minh nghe nhu **that bai**: *"con 69% chua lam"*. Nhung
    `1.345` dong lenh chi con ranh la **toan bo nguyen lieu** con lai ⇒ du moi
    cu ghep deu hoan hao, do phu chi tay **`47,4%`**. Nen con so **noi dung
    viec da lam** la `da_noi / tran` = **`65,6%`**, ⛔ khong phai `31,1%`.

    ⛔ Va `tran` **⛔ khong phai** *"se dat duoc"*: no gia dinh ghep **1:1**,
      con thuc te mot dong tien co the an **nhieu** dong lenh ⇒ tran thuc
      **thap hon**. ⇒ Ten truong la `toi_da`, ⛔ khong phai `du_bao`.

    ⛔ `None` cho moi ty le khi ⛔ khong co anh lenh chi nao: *"0%"* la mot cau
      tra loi SAI cho mot cau hoi ⛔ khong do duoc.
    """
    ranh = tho["anh_tong"] - tho["da_dung"]
    da_noi = (ps_co or {}).get("da_noi", 0)
    mau = (ps_co or {}).get("so_dong", 0)
    toi_da = da_noi + ranh
    return {
        "anh_pm": run_pm,
        "dong_lenh_trong_anh": tho["anh_tong"],
        "dong_lenh_da_dung": tho["da_dung"],
        "dong_lenh_con_ranh": ranh,
        "toi_da_noi_duoc": toi_da,
        # ⭐ tran tinh theo % cua mau so `PS Co`
        "tran_pct": _pct(toi_da, mau),
        # ⭐⭐ do phu **TREN TRAN** — con so noi dung phan viec da lam
        "phu_tren_tran_pct": _pct(da_noi, toi_da),
        "ket_luan":
            "⛔ Tran nay do SO DONG LENH CHI TON TAI dat ra — ⛔ khong do giao "
            "dien, ⛔ khong do ma, ⛔ khong do do tuoi cua du lieu. ⇒ Cau *'dua "
            "do phu mapping len 100%'* la mot cau ⛔ KHONG THE DUNG, va moi ty "
            "le do tren mau so `PS Co` se mai mai trong nhu that bai. ⚠ Va "
            "`toi_da` gia dinh ghep 1:1 nen thuc te con THAP HON",
    }


def do_phu_pm(conn, pv: PhamVi) -> dict[str, Any]:
    """⭐⭐⭐ DO PHU **PHIA PM** — mau so THAT cua viec ghep.

    `QĐ-ITL-122`: owner chot chieu do la **`Trans` map vao `PM`**, va
    *"⛔ ko can question cac Trans khong duoc map"*. ⇒ Viec that la nhung
    **dong lenh chi ⛔ chua tim duoc tien cua no**, ⛔ khong phai nhung dong
    tien ⛔ chua co lenh.

    ⛔⛔ **Vi sao dieu nay doi CA con so lan CA danh sach viec:**
      · con so: `2.427/3.772` = do phu **phia PM**, thay `2.562/8.246`;
      · danh sach: `1.345` dong lenh */* `510` phieu, thay `5.684` dong tien.
    Hai cach dem chenh nhau **4,2 lan** ve so cu bam.

    ⭐ `ghep_duoc_ngay` — dong lenh chua co tien MA co mot dong tien chua noi
      mang **dung** ma tham chieu ay. ⛔ Phep giao lam o **PYTHON bang
      `canon_ref`** — ⛔ **khong** bang mot cau `regexp_replace` trong SQL:
      ma ITL ⛔ **khong** co ban chuan hoa trong kho *(chi co `doc_no` tho)*,
      nen mot cau SQL tu dung se la **ban thu hai** cua `canon_ref` va no
      ⛔ khong tuong duong *(`canon_ref` con go ky hieu khoa hoc `4.36E+15`,
      chuan hoa `NFKC`, va loai o loi `#N/A`)*. Toi da in ra mot con so do
      bang cau SQL tu dung mot lan hom 09/09 truoc khi kip bat.
    """
    run_pm = anh_pm_hieu_luc(conn, pv)
    dk, ts = pv.dieu_kien("i.run_id")
    with conn.cursor() as cur:
        cur.execute(_SQL_PM_PHU, {"run_pm": run_pm})
        d = _dong(cur)[0]
        cur.execute(_SQL_PM_CHUA_THEO_TE, {"run_pm": run_pm})
        theo_te = _dong(cur)
        cur.execute(_SQL_PM_REF_CHUA, {"run_pm": run_pm})
        ref_pm = {r[0] for r in cur.fetchall()}
        cur.execute(_SQL_ITL_DOC_NO_CHUA_NOI.format(dk=dk), ts)
        ma_itl = {m for (x,) in cur.fetchall() if (m := canon_ref(x))}

    chua = d["dong_lenh"] - d["da_co_tien"]
    return {
        "anh_pm": run_pm,
        "dong_lenh": d["dong_lenh"],
        "da_co_tien": d["da_co_tien"],
        "chua_co_tien": chua,
        "ty_le_pct": _pct(d["da_co_tien"], d["dong_lenh"]),
        "phieu": d["phieu"],
        "phieu_da_co": d["phieu_da_co"],
        # ⛔ `phieu` − `phieu_da_co` = phieu ⛔ CHUA NOI GI CA. ⛔ Day
        #   **⛔ KHONG** phai *"viec con lai"* — xem `phieu_con_dong_chua`.
        "phieu_chua_noi_gi": d["phieu"] - d["phieu_da_co"],
        # ⭐⭐ VIEC CON LAI theo phieu: phieu con it nhat mot dong chua noi
        "phieu_con_dong_chua": d["phieu_con_dong_chua"],
        # ⭐⭐⭐ Phieu NUA NO NUA KIA — de bo sot nhat, vi no ⛔ khong con nam
        #    trong nhom *"chua lam gi"* ma cung ⛔ chua xong
        "phieu_mot_nua": (d["phieu_da_co"] + d["phieu_con_dong_chua"]
                          - d["phieu"]),
        "ty_le_phieu_pct": _pct(d["phieu_da_co"], d["phieu"]),
        # ⛔ `status` ⛔ khong phai `Approve` ⇒ `ghep_lenh` doi `force` kem ly
        #   do ⇒ **⛔ khong phai viec cua ke toan ITL**, tach ra de ⛔ khong ai
        #   dem no vao *"viec con lai"*.
        "chua_co_va_chua_duyet": d["chua_co_va_chua_duyet"],
        "ghep_duoc_ngay": len(ref_pm & ma_itl),
        "chua_co_tien_theo_te": theo_te,
        "ket_luan":
            "⭐ Mau so la so DONG LENH CHI, ⛔ khong phai so dong tien: "
            "`Trans` nhieu hon `PM` la DUNG THIET KE, va cac `Trans` "
            "⛔ khong map thi ⛔ KHONG PHAI mot cau hoi (`QĐ-ITL-122`). ⇒ Viec "
            "that la cac dong lenh ⛔ chua tim duoc tien",
    }


def do_mau_so(conn, pv: PhamVi) -> dict[str, Any]:
    """MAU SO cua tac vu ① + doi chieu hai cau *"chua ghep"*. ⛔ Chi doc.

    Tra:
      `ve[]`      — bon nhom ve, moi nhom co `so_dong`/`da_noi`/`chua_noi`/`pct`
      `nhan[]`    — bon o `work_status` × `co moi noi`, **moi o mot TEN LY DO**
      `lech`      — `353` va **hai nhom nguoc chieu** lam nen no
      `vi_sao[]`  — bon nhom cua tap chua noi, va Σ = so dong chua noi
      `tu_chung`  — so dong cua ghep LO nhan duoc **ngay**
      `tran`      — ⭐⭐⭐ TRAN CUNG + do phu **tren tran** (xem `_tran`)
    """
    dk, ts = pv.dieu_kien("i.run_id")
    run_pm = anh_pm_hieu_luc(conn, pv)
    with conn.cursor() as cur:
        cur.execute(_SQL_VE.format(dk=dk), ts)
        ve = {r["ve"]: r for r in _dong(cur)}
        cur.execute(_SQL_NHAN.format(dk=dk), ts)
        nhan_tho = _dong(cur)
        cur.execute(_SQL_TRAN, {"run_pm": run_pm})
        tran_tho = _dong(cur)[0]

    ds_ve = []
    for k in ("ps_co", "ps_no", "ca_hai", "khong_ve_nao"):
        r = ve.get(k) or {"so_dong": 0, "da_noi": 0, "chua_noi": 0}
        ds_ve.append({
            "ve": k, "so_dong": r["so_dong"], "da_noi": r["da_noi"],
            "chua_noi": r["chua_noi"],
            "ty_le_noi_pct": _pct(r["da_noi"], r["so_dong"])})

    ds_nhan = []
    for r in nhan_tho:
        ma, ly_do = LY_DO_NHAN[(bool(r["nhan_unmapped"]), bool(r["co_moi_noi"]))]
        ds_nhan.append({"ma": ma, "so_dong": r["so_dong"], "ly_do": ly_do})
    ds_nhan.sort(key=lambda x: -x["so_dong"])

    def _o(ma: str) -> int:
        return next((x["so_dong"] for x in ds_nhan if x["ma"] == ma), 0)

    da_noi_nhan_cu = _o("da_noi__nhan_con_UNMAPPED")
    du_ma_chua_noi = _o("du_phan_loai__chua_noi")

    tc = ds_tu_chung(conn, pv)
    tong = sum(x["so_dong"] for x in ds_ve)
    ra = {
        "tong_dong": tong,
        "ve": ds_ve,
        "nhan": ds_nhan,
        "lech": {
            # ⭐⭐ Day la cau tra loi cua `B0` cho §0 ⓸ cua lo trinh.
            "hieu_hai_phep_dem": da_noi_nhan_cu - du_ma_chua_noi,
            "da_noi__nhan_con_UNMAPPED": da_noi_nhan_cu,
            "du_phan_loai__chua_noi": du_ma_chua_noi,
            "tong_dong_bi_che": da_noi_nhan_cu + du_ma_chua_noi,
            "ket_luan":
                "⛔ KHONG phai mau thuan: `work_status` do PHAN LOAI (dong bang "
                "luc nap), `fls_moi_noi` do MOI NOI. Hai cau hoi khac nhau ⇒ "
                "hai con so dung PHAI khac. ⛔ Cai sai la phep TRU chung: "
                "mot HIEU che hai nhom nguoc chieu va noi NHO hon su that",
        },
        "vi_sao": [{"ma": k, "so_dong": tc["vi_sao"][k],
                    "so_dong_ps_co": tc["vi_sao_ps_co"][k],
                    "ly_do": LY_DO_VI_SAO[k]} for k in _THU_TU_VI_SAO],
        "tu_chung": len(tc["tu_chung"]),
        "khong_tu_chung": {
            k: sum(1 for v in tc["khong"].values() if v == k)
            for k in LY_DO_KHONG_TU_CHUNG},
        "tran": _tran(ve.get("ps_co"), tran_tho, run_pm),
        "pham_vi": pv.mo_ta(),
    }
    # ⛔⛔ Hai bat bien tu kiem — mot phep phan hoach ⛔ khong tu kiem la mot
    # phep phan hoach **se lech trong im lang** (dung lop loi `GAP-DOC-08`).
    if sum(x["so_dong"] for x in ds_nhan) != tong:
        raise AssertionError(
            f"⛔ bang cheo nhan lech tong: {sum(x['so_dong'] for x in ds_nhan)}"
            f" != {tong}")
    if sum(x["so_dong"] for x in ra["vi_sao"]) != tc["so_dong_xet"]:
        raise AssertionError(
            f"⛔ bon nhom `vi_sao` ⛔ khong phu het tap chua noi: "
            f"{sum(x['so_dong'] for x in ra['vi_sao'])} != {tc['so_dong_xet']}")
    return ra
