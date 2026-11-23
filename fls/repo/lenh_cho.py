"""`GAP-SCR-14` — HANG CHO PHIA LENH CHI. Cai nguoc lai cua `doc_hang_cho`.

⛔⛔⛔ **Vi sao module nay ton tai, va vi sao no ⛔ khong the la mot bo loc cua
   man hang cho cu.**

Owner chot chieu do ngay 09/09 *(`QĐ-ITL-122`)*:

  > *"`Trans` map vao `PM` (so luong Trans von nhieu hon PM; ⛔ ko can question
  >  cac Trans khong duoc map)"*

Do trong ngay tren bang tuyen: **10** cua khoa theo `itl_id`, **0** cua khoa
theo **dong lenh**. ⇒ Ca he ⛔ **khong co mot duong nao** hoi duoc cau
*"lenh chi nao ⛔ chua tim duoc tien"* — tuc **dung cau hoi cua viec**. Va man
`F01` dang hien **7.682** dong `Trans`, tuc dang hoi **dung cai cau owner vua
noi la ⛔ khong can hoi**.

★ Hai con so cua cung mot ngay, de doc canh nhau:

  · hoi phia TIEN : **5.684** dong chua noi  ⇒ mot danh sach ⛔ khong ai lam het
  · hoi phia LENH : **1.345** dong chua co tien */* **698** phieu ⇒ **viec that**

Chenh **4,2 lan** ve so cu bam, va **cung mot kho du lieu**.

⛔⛔ **Va no ⛔ KHONG mo mot duong GHI thu hai.** Phep ghep van la
`ghi_tay.ghep_lenh(itl_id, [pm_line_id])` — mot chuyen. Man hinh phia lenh chi
chi **doi thu tu hoi**: chon dong lenh truoc, roi chon dong tien. Neu module
nay tu ghi thi he se co **hai duong ghi** vao `fls_pm_link`, va cong quet ma
nguon *(chi-mot-cho-ghi-tay)* se do — dung nhu no phai do.

⭐ Luat xep giu **nguyen tung chu** tu `QĐ-ITL-58`: **`PARTITION BY curr`**.
  Gop hai don vi tien ra mot con so la cai sai da de ra *"310 dong phu 90%"*
  *(that ra **799**)*, va o day no con te hon: dong lenh **USD** nhieu hon
  **VND** *(700 vs 590)* nen gop lai se **dim** ca ve USD xuong duoi.
"""
from __future__ import annotations

from decimal import Decimal
from typing import Any

from fls.adapters.pm_join import canon_ref, dung_sai_ghep_tay
from fls.canon.tien_te import TAP_TRANG_TIEN_TE, ma_tien_te
from fls.repo.anh_pm import anh_pm_hieu_luc
from fls.repo.doc_bao_cao import (TRANG_MAC_DINH, TRANG_TOI_DA,
                                  UNG_VIEN_MAC_DINH, UNG_VIEN_TOI_DA, Trang,
                                  _canh_bao)
from fls.repo.pham_vi import PhamVi

# ⭐ Bon bac ung vien phia TIEN — **soi guong** `BAC_UNG_VIEN` cua chieu thuan.
#
# ⛔⛔ Ten bac giu **y nguyen** *(`ma`/`tien`/`gan_tien`/`cung_tien_te`)*, co y:
#    hai man hinh noi **cung mot tu** cho **cung mot y**. Doi ten o mot phia se
#    lam nguoi doc tuong day la hai thang do khac nhau.
BAC_UNG_VIEN_ITL: tuple[str, ...] = ("ma", "tien", "gan_tien", "cung_tien_te")

# ⛔⛔⛔ **Bac `cung_tien_te` cua chieu NGUOC PHAI co tran, va day la mot bat
#    doi xung THAT — ⛔ khong phai mot su lam tat.**
#
# Chieu thuan hoi *"dong lenh nao cho dong tien nay"*: tap ung vien la
# **3.772** dong lenh. Chieu nguoc hoi *"dong tien nao cho dong lenh nay"*:
# tap ung vien la **10.030** dong tien, va rieng bac *"cung tien te"* co the
# tra ve **hang nghin** dong ⛔ khong noi len dieu gi.
#
# ⇒ Cat, VA **khai ra minh da cat** *(`bi_cat` + `tong_cung_tien_te`)*. Cat ma
#   im la mot **mac dinh im lang** *(`INV-I16`)*: nguoi go se tuong danh sach
#   ay la **day du** va ket luan *"⛔ khong co dong tien nao khop"*.
CAT_CUNG_TIEN_TE = 20

# ⭐ `l.tho` them 11/09 — owner: *"van chua thay du cac cot"*. Ban truoc toi
#   de 28 cot trong NGAN KEO *(phai bam tung dong moi thay)*, nhung cau hoi
#   la ve **BANG**. ⇒ Hang tho di thang ra luoi.
#
# ⚠ Gia: ~894 byte/dong × 50 dong = **~45 KB** mot trang. Do duoc va chap
#   nhan duoc; ⛔ khong doan.
_COT_LENH = ("l.pm_line_id", "l.pm_slip_id", "l.ref_tho", "l.ref_canon",
             "l.amount", "l.curr", "l.status", "l.hd", "l.cdt1",
             "l.source_row", "l.tho")

# ⛔ `fls_moi_noi`, ⛔ KHONG `fls_pm_link`: bang goc con giu ca moi noi DA BO
#   (migration `0013`) ⇒ dem tren bang goc se an mot dong lenh vua duoc go ra
#   khoi hang cho, va ke toan ⛔ khong bao gio thay lai no.
#
# ⭐⭐ `p` them 11/09 (`G5`) — **CA PHIEU co may dong**.
#
# ⛔⛔ Do that truoc khi viet: **1.088/1.553 = 70,1%** dong dang cho nam trong
#    mot phieu co **nhieu hon mot** dong, va phieu to nhat co **44** dong. Tuc
#    cai *"⛔ khong thay duoc cac dong khac cua cung phieu"* ⛔ **khong phai mot
#    ca hiem** — no la **phan lon** danh sach. Nhin mot dong le ma quyet la
#    nhin mot manh cua to giay.
#
# ⚠ Dem tren **CA anh chup**, ⛔ khong tren tap dang cho: ke toan can biet
#   *"phieu nay co 7 dong, 4 da noi roi"* — mot con so chi dem phan con cho se
#   noi *"3 dong"* va **giau mat** 4 dong kia.
_CTE_LENH_CHO = """
WITH p AS (
  SELECT pm_slip_id, count(*)::int AS phieu_tong
  FROM fls_pm_line WHERE run_id = %(run_pm)s GROUP BY 1
), q AS (
  SELECT {cot}, COALESCE(l.amount, 0) AS tien,
         (COALESCE(NULLIF(lower(trim(l.status)), ''), 'x') = 'approve')
           AS duyet,
         p.phieu_tong
  FROM fls_pm_line l
  LEFT JOIN p ON p.pm_slip_id = l.pm_slip_id
  WHERE l.run_id = %(run_pm)s
    AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m
                     WHERE m.pm_line_id = l.pm_line_id)
), x AS (
  SELECT q.*,
         count(*) OVER (PARTITION BY q.pm_slip_id)::int AS phieu_cho,
         row_number() OVER w AS hang,
         round(100.0 * SUM(q.tien) OVER (PARTITION BY q.curr
                                         ORDER BY q.tien DESC, q.pm_line_id
                                         ROWS UNBOUNDED PRECEDING)
               / NULLIF(SUM(q.tien) OVER (PARTITION BY q.curr), 0), 2)
           AS luy_ke_pct
  FROM q
  WINDOW w AS (PARTITION BY q.curr ORDER BY q.tien DESC, q.pm_line_id)
)
"""

_SQL_LENH_CHO = _CTE_LENH_CHO + """
SELECT x.pm_line_id, x.pm_slip_id, x.ref_tho, x.ref_canon, x.amount, x.curr,
       x.status, x.hd, x.cdt1, x.source_row, x.tho, x.tien, x.duyet,
       x.hang, x.luy_ke_pct, x.phieu_tong, x.phieu_cho
FROM x
WHERE TRUE {them}
ORDER BY x.curr, x.hang
LIMIT %(n)s"""

_SQL_DEM_LENH_CHO = _CTE_LENH_CHO + """
SELECT x.curr, count(*)::int AS so_dong,
       count(DISTINCT x.pm_slip_id)::int AS so_phieu,
       SUM(x.tien) AS tien,
       count(*) FILTER (WHERE x.duyet)::int AS so_dong_duyet,
       count(*) FILTER (WHERE NOT x.duyet)::int AS so_dong_chua_duyet,
       min(x.hang) FILTER (WHERE x.luy_ke_pct >= %(muc)s)::int AS so_dong_phu,
       min(x.luy_ke_pct) FILTER (WHERE x.luy_ke_pct >= %(muc)s) AS pct_that
FROM x
GROUP BY x.curr
ORDER BY 2 DESC"""

# ── ung vien phia TIEN cho MOT dong lenh ────────────────────────────────
#
# ⛔⛔⛔ **Bac `ma` ⛔ KHONG lam duoc trong SQL, va day la mot rang buoc THAT
#    cua kho — ⛔ khong phai mot lua chon.**
#
# `fls_pm_line.ref_canon` **da chuan hoa** *(luu san luc nap)*. Nhung phia ITL
# thi kho **chi co `doc_no` THO** — ⛔ khong mot cot chuan hoa nao. Nen mot cau
# `regexp_replace(i.doc_no, '[^A-Za-z0-9]', '', 'g')` la **ban thu hai** cua
# `canon_ref`, va no ⛔ **khong tuong duong**: `canon_ref` con go **ky hieu khoa
# hoc** *(`4.36619E+15` → `4366190000000000`)*, chuan hoa **`NFKC`**, va loai
# **o loi** *(`#N/A`)*.
#
# ⭐ Va no ⛔ khong phai gia thuyet: toi **da in ra** con so *"560 dong ghep
#   duoc ngay"* do bang dung cau `regexp` ay hom 09/09; luat THAT cho **475**
#   — lech **17,9%**.
#
# ⇒ Bac `ma` tinh o **PYTHON** bang `canon_ref`, con ba bac TIEN thi o SQL.
# ⭐ `11/09` thêm `curr` + `tien` *(`G2`)*: phép chia rổ phải phân biệt được
#   *"khớp mã VÀ khớp tiền"* với *"khớp mã, lệch tiền"* — hai nhóm đi hai
#   đường khác nhau. ⛔ Mở rộng **chính** câu này chứ ⛔ không viết câu thứ
#   hai: hai câu là hai chỗ để chúng lệch nhau, đúng điều đoạn trên cảnh báo.
_SQL_ITL_MA = """
SELECT i.itl_id, i.doc_no, i.curr,
       COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) AS tien
  FROM fls_itl i
 WHERE i.doc_no IS NOT NULL AND {dk}
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)
"""

_COT_ITL = ("i.itl_id", "i.doc_date", "i.doc_no", "i.curr", "i.le", "i.memo",
            "i.work_status",
            # ⭐⭐ `QĐ-ITL-148` — bon thu man GAN LENH CHI can ma truoc day cua
            #    ⛔ khong tra, nen nguoi dung ban dung phai **cat chuoi hien
            #    thi** de lay lai cau truc (`BA-07 §4h ⓵`).
            "i.source_sheet", "i.ps_no", "i.ps_co",
            "dg.dien_giai",
            # ⛔⛔ `dien_giai IS NULL` mang **HAI** nghia, va gop chung la dung
            #    thu `INV-I16` cam: *"giao dich nay ⛔ khong co noi dung"* va
            #    *"FLS ⛔ chua doc duoc"* la hai cau khac nhau.
            #    Do `21/09`: **3** dong noi duoc ma ⛔ khong chu · **26** dong
            #    ⛔ khong noi duoc chut nao.
            # ⭐ `fls_dien_giai` **co chu y** loai dong ⛔ khong co chu
            #   (`QĐ-ITL-145`), nen mot LEFT JOIN vao no ⛔ khong phan biet
            #   duoc hai ca ⇒ hoi **su ton tai cua anh chup** rieng.
            "(EXISTS (SELECT 1 FROM fls_source s2"
            "          JOIN fls_chup_dong d2 ON d2.source_id = s2.source_id"
            "                               AND d2.dong_so = i.source_row"
            "         WHERE s2.source_key = i.source_sheet)) AS noi_duoc")

#: ⭐ Khung xem dien giai — `migration 0026`. ⛔ Khong ghi mot o nao vao so.
_NOI_DIEN_GIAI = " LEFT JOIN fls_dien_giai dg ON dg.itl_id = i.itl_id "

# ⭐ `WO-037` vòng 2 `(k)` *(`BA-07` v3.10 — `BG-039` yếu #3)*: vế SỔ của phép
#   so tiền tệ là `upper(btrim(i.curr, E' \t\r\n'))` — **cùng** luật
#   `ma_tien_te` *(`trim` + chữ hoa)* mà vế LỆNH *(`cur_lenh`)*, rổ *(`xep_ro`)*
#   và bậc `ma` *(Python)* đang dùng. ⛔ Trước: chữ hoa vế sổ ⛔ `trim` — luật
#   so tiền tệ **thứ ba**: một dòng `' vnd '` ⛔ mã khớp thì rổ coi là VND
#   mà ba bậc tiền của `itl-candidates` ⛔ bao giờ hiện nó. Sổ thật 02/10:
#   `curr` có khoảng trắng **0 / 8.387** ⇒ sửa vì **một** luật, ⛔ vì báo
#   động. Tập ký tự = tập `str.strip()` gỡ ở ca thường *(space · tab · CR ·
#   LF)*. Bài ghim: `test_AC15_GHIM_khong_chuoi_upper_i_curr_tran_trong_fls`
#   *(⛔ phép chữ hoa trần nào trên `i.curr` trong `fls/`)*.
# ⛔⛔ `WO-042 (c)` *(`BA-07` v3.11 — `KQ-041 F-2`)*: tập bốn ký tự trên
#   *(space · tab · CR · LF)* ⛔ phải tập `str.strip()` *(29)* — PG thật, 6
#   chuỗi biên *(NBSP · VT · FF · `U+3000` · khoảng trắng hẹp · `U+0085`)*
#   lệch **6 / 6**. Nay tập là **tham số** `%(tap)s` = `TAP_TRANG_TIEN_TE`
#   *(30 ký tự, `fls.canon.tien_te`)* — ⛔ chuỗi gõ lại trong SQL: chuỗi gõ
#   lại là bản thứ hai, và nó đã lệch.
_SQL_ITL_UNG_VIEN = """
WITH s AS (
  SELECT %(cur)s::text AS cur, %(tien)s::numeric AS tien,
         %(ds)s::numeric AS ds
)
SELECT {cot},
       COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) AS tien,
       abs(COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) - s.tien)
         AS lech_tuyet_doi,
       CASE
         WHEN COALESCE(i.ps_no,0) + COALESCE(i.ps_co,0) = s.tien THEN 'tien'
         WHEN abs(COALESCE(i.ps_no,0) + COALESCE(i.ps_co,0) - s.tien) <= s.ds
                                                                 THEN 'gan_tien'
         ELSE 'cung_tien_te' END AS bac
  FROM fls_itl i CROSS JOIN s LEFT JOIN fls_dien_giai dg ON dg.itl_id = i.itl_id
 WHERE {dk} AND upper(btrim(i.curr, %(tap)s)) = s.cur
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)
 ORDER BY abs(COALESCE(i.ps_no,0) + COALESCE(i.ps_co,0) - s.tien), i.itl_id
 LIMIT %(n)s"""

_SQL_DEM_CUNG_TE = """
SELECT count(*)::int FROM fls_itl i
 WHERE {dk} AND upper(btrim(i.curr, %(tap)s)) = %(cur)s
   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)
"""

_SQL_MOT_DONG_LENH = """
SELECT l.pm_line_id, l.pm_slip_id, l.ref_tho, l.ref_canon, l.amount, l.curr,
       l.status, l.hd, l.cdt1, l.source_row, l.tho
  FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s AND l.pm_line_id = %(id)s
"""

# ⭐⭐ CA PHIEU — cac dong lenh KHAC cung `pm_slip_id`.
#
# ⛔⛔ **Vi sao phai co.** Do tren 3.703 dong lenh that: **526 phieu mang 2–36
#    `reference` KHAC NHAU** (`CR#6`). Nhin mot dong le ma quyet la nhin mot
#    manh cua mot to giay — va ke toan ⛔ khong co duong nao thay phan con lai.
_SQL_CA_PHIEU = """
SELECT l.pm_line_id, l.ref_tho, l.amount, l.curr, l.status, l.hd,
       (l.pm_line_id = %(id)s) AS dang_xem,
       EXISTS (SELECT 1 FROM fls_moi_noi m
                WHERE m.pm_line_id = l.pm_line_id) AS da_noi
  FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s AND l.pm_slip_id = %(slip)s
 ORDER BY l.source_row
"""

_SQL_ITL_THEO_ID = """
SELECT {cot}, COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) AS tien
  FROM fls_itl i
  LEFT JOIN fls_dien_giai dg ON dg.itl_id = i.itl_id
 WHERE i.itl_id = ANY(%(ids)s::bigint[]) AND {dk}
"""


def _dong(cur) -> list[dict[str, Any]]:
    ten = [x.name for x in cur.description]
    return [dict(zip(ten, r)) for r in cur.fetchall()]


def _trang(limit: int | None) -> int:
    if limit is None:
        return TRANG_MAC_DINH
    n = int(limit)
    if n < 1:
        raise ValueError(f"limit={n} phai >= 1")
    return min(n, TRANG_TOI_DA)


def doc_lenh_cho(conn, pv: PhamVi, *, curr: str | None = None,
                 chi_duyet: bool | None = None,
                 den_pct: Decimal | float | None = None,
                 con_tro: str | None = None,
                 limit: int | None = None) -> Trang:
    """Dong lenh chi **⛔ CHUA tim duoc tien**, xep theo tien GIAM trong tung
    tien te.

    `chi_duyet=True` bo cac dong `status` ⛔ khong phai `Approve`.

    ⛔⛔ **Va mac dinh la `None` — tuc HIEN CA HAI, ⛔ khong loc san.** `275`
       dong ⛔ chua duyet ⛔ **khong phai viec cua ke toan ITL** *(chung doi
       `force` kem ly do)*, nhung an chung di **theo mac dinh** la mot **mac
       dinh im lang** *(`INV-I16`)*: ke toan biet phieu ay ton tai, ⛔ khong
       thay no trong danh sach, va se ket luan **he mat du lieu**. ⇒ Hien, kem
       co `duyet`, va de **nguoi** bat bo loc.

    ⭐ `den_pct` = *"chi lay den khi phu bao nhieu % tien"* — cung phep tra loi
      *"xem toi day la du"* ⛔ **ma ⛔ khong can mot quy dinh nao** ve khoan nao
      can lenh chi *(`QĐ-ITL-56`: ⛔ khong co quy dinh do)*.

    Con tro phan trang la `"<tien te>:<hang>"` — khoa doi, vi thu tu la
    `(tien te, hang)`.
    """
    n = _trang(limit)
    run_pm = anh_pm_hieu_luc(conn, pv)
    ts: dict[str, Any] = {"run_pm": run_pm, "n": n + 1}
    them: list[str] = []
    if curr:
        them.append("AND x.curr = %(curr)s")
        ts["curr"] = curr
    if chi_duyet is True:
        them.append("AND x.duyet")
    elif chi_duyet is False:
        them.append("AND NOT x.duyet")
    if den_pct is not None:
        them.append("AND x.luy_ke_pct <= %(den_pct)s")
        ts["den_pct"] = Decimal(str(den_pct))
    if con_tro:
        c, h = con_tro.split(":", 1)
        them.append("AND (x.curr, x.hang) > (%(ct_c)s, %(ct_h)s)")
        ts["ct_c"], ts["ct_h"] = c, int(h)

    sql = _SQL_LENH_CHO.format(cot=", ".join(_COT_LENH),
                               them=" ".join(them))
    with conn.cursor() as cur:
        cur.execute(sql, ts)
        dong = _dong(cur)
    con = (f"{dong[n - 1]['curr']}:{dong[n - 1]['hang']}"
           if len(dong) > n else None)
    return Trang(dong=dong[:n], con_tro=con, pham_vi=pv.mo_ta())


def dem_lenh_cho(conn, pv: PhamVi,
                 muc_pct: Decimal | float = 90) -> list[dict[str, Any]]:
    """Chan man: **theo TUNG tien te**, ⛔ **khong co dong "tong"**.

    ⛔⛔ Cong hai don vi tien ra mot con so la cai sai da de ra *"310 dong phu
       90%"* *(that ra **799**)*. O day no con te hon: dong lenh **USD** nhieu
       hon **VND** *(700 vs 590)* nen gop lai se **dim ca ve USD** xuong duoi.

    ⭐ Tra ca `so_dong_duyet` va `so_dong_chua_duyet`: hai con so ay la **hai
      loai viec khac nhau**, va mot con so gop lai se lam ke toan tuong ho
      con **1.345** viec trong khi phan lam duoc chi la **1.070**.
    """
    m = Decimal(str(muc_pct))
    if not 0 < m <= 100:
        raise ValueError(f"muc_pct={muc_pct} phai trong (0, 100]")
    run_pm = anh_pm_hieu_luc(conn, pv)
    sql = _SQL_DEM_LENH_CHO.format(cot=", ".join(_COT_LENH))
    with conn.cursor() as cur:
        cur.execute(sql, {"run_pm": run_pm, "muc": m})
        return _dong(cur)


def _dk_ten(pv: PhamVi, cot: str) -> tuple[str, dict[str, Any]]:
    """`pv.dieu_kien` tra tham so **theo VI TRI** (`%s`) -> doi sang **theo
    TEN** (`%(pv0)s`, …).

    ⛔⛔ **Vi sao can phep doi nay:** cac cau o day dung tham so **co ten**
       *(`%(run_pm)s`, `%(cur)s`, …)*, va psycopg ⛔ **khong tron hai kieu
       trong MOT cau** — no NO ngay lan chay dau. Tron duoc thi cung te hon:
       thu tu tham so vi tri se **im lang truot** moi khi ai them mot dieu
       kien vao giua cau.
    """
    sql, ts = pv.dieu_kien(cot)
    ra: dict[str, Any] = {}
    for i, v in enumerate(ts):
        sql = sql.replace("%s", f"%(pv{i})s", 1)
        ra[f"pv{i}"] = v
    return sql, ra


def ung_vien_itl(conn, pv: PhamVi, pm_line_id: str,
                 n: int = UNG_VIEN_MAC_DINH) -> dict[str, Any] | None:
    """Dong TIEN ung vien cho MOT dong lenh. `None` neu dong lenh ⛔ khong co
    trong anh chup HIEU LUC.

    Bon bac **soi guong** chieu thuan: `ma` › `tien` › `gan_tien` ›
    `cung_tien_te`.

    ⛔⛔ Bac `ma` tinh o **PYTHON** bang `canon_ref` — xem khoi chu thich cua
       `_SQL_ITL_MA`. Mot cau `regexp_replace` trong SQL la **ban thu hai** cua
       `canon_ref` va no ⛔ khong tuong duong *(da do: `560` vs **`475`**, lech
       **17,9%**)*.

    ⭐ Tra ve ca `bi_cat` va `tong_cung_tien_te`: bac `cung_tien_te` cua chieu
      nguoc co **hang nghin** dong, nen no bi cat — va mot phep cat **im lang**
      se lam nguoi go ket luan *"⛔ khong co dong tien nao khop"* *(`INV-I16`)*.
    """
    n = min(max(int(n), 1), UNG_VIEN_TOI_DA)
    run_pm = anh_pm_hieu_luc(conn, pv)
    dk, ts_dk = _dk_ten(pv, "i.run_id")

    with conn.cursor() as cur:
        cur.execute(_SQL_MOT_DONG_LENH, {"run_pm": run_pm, "id": pm_line_id})
        d = _dong(cur)
        if not d:
            return None
        lenh = d[0]

        # ── bac `ma`: doc (id, doc_no) THO roi chuan hoa o PYTHON
        cur.execute(_SQL_ITL_MA.format(dk=dk), ts_dk)
        ma_lenh = lenh["ref_canon"]
        # ⚠ `_SQL_ITL_MA` trả **bốn** cột từ 11/09 (`curr`+`tien` cho `G2`);
        #   bậc `ma` ở đây ⛔ không cần hai cột ấy.
        id_ma = ([i for i, doc, _c, _t in cur.fetchall()
                  if canon_ref(doc) == ma_lenh] if ma_lenh else [])
        ds_ma = []
        if id_ma:
            cur.execute(
                _SQL_ITL_THEO_ID.format(cot=", ".join(_COT_ITL), dk=dk),
                {"ids": id_ma, **ts_dk})
            ds_ma = _dong(cur)

        # ── ba bac TIEN: o SQL
        # ⭐ `WO-037`: **cùng** `ma_tien_te`; trước: bản `strip().upper()`
        #   viết tay ở đây. `WO-042 (c)`: nhập từ `fls.canon.tien_te` ở đầu
        #   tệp *(hết vòng nhập với `man_ghep`)*.
        cur_lenh = ma_tien_te(lenh["curr"])
        tien = Decimal(str(lenh["amount"] or 0))
        # ⚠ `dung_sai_ghep_tay` — **cung phep dung sai ma cua GHI dung**. Mot
        #   ban rieng o day se ve mot ung vien vao bac `gan_tien` roi cua ghi
        #   **tu choi** no: mot cai bay.
        ds = dung_sai_ghep_tay({cur_lenh}, tien) if cur_lenh else Decimal(0)
        ds_tien, tong_cung_te = [], 0
        if cur_lenh:
            cur.execute(
                _SQL_ITL_UNG_VIEN.format(cot=", ".join(_COT_ITL), dk=dk),
                {"cur": cur_lenh, "tien": tien, "ds": ds,
                 "tap": TAP_TRANG_TIEN_TE,
                 "n": CAT_CUNG_TIEN_TE + n, **ts_dk})
            ds_tien = _dong(cur)
            cur.execute(_SQL_DEM_CUNG_TE.format(dk=dk),
                        {"cur": cur_lenh, "tap": TAP_TRANG_TIEN_TE,
                         **ts_dk})
            tong_cung_te = int(cur.fetchone()[0])

    # ⛔ Bac `ma` THANG moi bac tien: mot dong tien mang **dung** ma tham chieu
    #   thi no la ung vien manh nhat, du so tien co lech.
    goi: dict[int, dict[str, Any]] = {}
    for r in ds_ma:
        # ⚠ `lech_tuyet_doi=None` ở đây **chỉ** để giữ THỨ TỰ xếp bậc `ma`
        #   như cũ *(theo `itl_id`)* — `WO-032` ⛔ đổi thứ tự. ⛔ Nó KHÔNG còn
        #   là `lech` cửa trả: khuôn `⓵` tính lại bằng `man_ghep.lech_ung_vien`
        #   ở **mọi** bậc *(`BA-07` v3.7 — trước: bậc `ma` luôn `null`, sổ thật
        #   **338 / 448** ứng viên lệch thật in `—`, `KQ-031 F-2`)*.
        goi[r["itl_id"]] = dict(r, bac="ma", lech_tuyet_doi=None)
    for r in ds_tien:
        goi.setdefault(r["itl_id"], r)
    # ⭐⭐ `WO-037` *(`BA-07` v3.9 — đoạn sau *"Bốn bậc soi gương"*)*: **trong
    #   bậc `ma`, CÙNG tiền tệ đứng trước KHÁC tiền tệ**, rồi `itl_id` như cũ.
    #   Thứ tự đủ: `ma` cùng tệ › `ma` khác tệ › `tien` › `gan_tien` ›
    #   `cung_tien_te`. ⛔⛔ **⛔ hạ** dòng mã khác tệ xuống dưới ba bậc tiền:
    #   với lệnh có nó, nó là **bằng chứng duy nhất** *(sổ thật 84 / 84)*, còn
    #   bậc tiền bên dưới là trùng tiền tình cờ — hạ nó là đặt một cặp **cửa
    #   ghi nhận mà sai** lên dòng đầu. An toàn nằm ở chỗ khác: màn ⛔ chọn sẵn
    #   *(`INV-I16`)* và nói *"cửa ghi sẽ TỪ CHỐI"* *(`WO-032`)*; thứ máy **đề
    #   xuất** là `the.gd`, và nó đi theo rổ *(`xep_ro`)*. Ba bậc tiền ở SQL đã
    #   lọc cùng tiền tệ ⇒ khoá thứ hai chỉ phân biệt được **trong** bậc `ma`.
    ra = sorted(goi.values(),
                key=lambda r: (BAC_UNG_VIEN_ITL.index(r["bac"]),
                               ma_tien_te(r.get("curr")) != cur_lenh,
                               r.get("lech_tuyet_doi") or 0, r["itl_id"]))
    return {
        "dong_lenh": lenh,
        "dung_sai": ds,
        "ung_vien": ra[:n],
        # ⛔ KHAI RA da cat — cat ma im la mot mac dinh im lang (`INV-I16`)
        "bi_cat": len(ra) > n,
        "tong_cung_tien_te": tong_cung_te,
        # ⛔ `status` RONG la KHONG BIET, ⛔ khong phai "da duyet"
        "canh_bao": _canh_bao(lenh["status"]),
        "anh_pm": run_pm,
        "pham_vi": pv.mo_ta(),
    }


# ══ `G2` · CHIA BA RỔ theo *"AI trả lời được câu này"* (`BA-12 §2`) ═══════
#
# ⛔⛔⛔ **Vì sao phép chia này tồn tại.** Màn lằn LỆNH CHI đang trộn **ba câu
#    hỏi khác nhau** vào **một** danh sách, và kế toán ⛔ không có cách nào biết
#    mình đang ở câu nào:
#
#      ⓐ *"ghép cái này với cái nào?"*      — việc THẬT
#      ⓑ *"máy biết rồi, bấm duyệt thôi"*   — ⛔ không đáng một giây suy nghĩ
#      ⓒ *"cái này ⛔ không bao giờ ghép được"* — ngồi nghĩ về nó là phí công
#
#    Đo `11/09` trên `1.553` dòng lệnh chưa nối: **250** thuộc ⓑ và **768**
#    thuộc ⓒ ⇒ **1.018 / 1.553 = 65,6%** danh sách ⛔ **không phải việc ghép**.
#
# ⛔⛔⛔ **VÀ ĐÂY LÀ CHỖ PHẢI ĐỌC KỸ — vì sao bậc `mã` KHÔNG ở trong SQL.**
#    Xem chú thích của `_SQL_ITL_MA` phía trên: `fls_pm_line.ref_canon` **đã
#    chuẩn hoá**, còn kho chỉ có `fls_itl.doc_no` **THÔ**. Một câu
#    `i.doc_no = l.ref_canon` là **bản sao thứ hai** của `canon_ref`, và nó
#    ⛔ **không tương đương**.
#
#    ⚠ Tôi đã tự chứng minh điều đó **một lần nữa** ngày `11/09`: đo bằng SQL
#      ra `121` dòng rổ `may`; gọi `canon_ref` thật ra **`250`** — **sai
#      107%**, và sai **cùng chiều** ở rổ `khong` *(`514` → `768`)*. Đúng lớp
#      lỗi mà chú thích `_SQL_ITL_MA` đã cảnh báo bằng một con số khác
#      *(`560` vs `475`, `09/09`)*.
#
#    ⇒ Phép chia rổ chạy **trong Python**, trên `canon_ref` của **CẢ HAI VẾ**.
RO_MAY = "may"          # máy trả lời được — người chỉ DUYỆT
RO_NGUOI = "nguoi"      # cần người tra — việc thật
RO_KHONG = "khong"      # ⛔ không ai trả lời được ở FLS

# ⛔ Câu **vì sao** cho rổ `khong`. Một rổ *"⛔ không bao giờ"* mà ⛔ không nói
#   vì sao thì kế toán sẽ **tìm mãi mãi** — đúng điều màn hình hôm nay đang làm.
#
# ⛔⛔ `WO-037` vòng 2 `(j)` *(`BA-07` v3.10 — bảng **chữ in**, `BG-039` yếu
#    #4)*: đây là chữ **cửa trả cho màn IN** *(`F01L` `hint` · ô *Giao dịch*
#    `F01G`)* ⇒ nó theo **luật ký hiệu màn hình**: **0** ký tự trong `⛔ ⚠ ⭐ 🔒`
#    *(bộ `CAM` của `tests/web/test_luat_ky_hieu_man_hinh.py`)*. Đo 02/10 trên
#    mã `4c3b2ae`: **3 / 3** câu mang `⛔` *(×1 · ×1 · ×2)* — Chrome 8099 vẽ nó
#    thành **biểu tượng tròn đỏ giữa câu** ở `F01L`; cổng ký hiệu chỉ quét
#    `man_f02.js`/`man_f04.js` và ⛔ quét chuỗi Python ⇒ ⛔ cổng nào canh. Nay
#    có cổng: `test_AC13_VI_SAO_va_cau_ghep_KHONG_ky_hieu_cam` *(dùng lại hằng
#    `CAM`)*. ⚠ Chỉ đổi **chữ**: khoá + tập lệnh mang câu nào ⛔ đổi. Khoá mới
#    thêm vào đây cũng phải qua cổng ấy. ⛔ Viết lại "cho gọn" bằng `⛔`/`⇒`.
VI_SAO = {
    "khong_co_tien_trong_so":
        "có số chứng từ nhưng KHÔNG dòng tiền nào trong sổ mang số ấy — "
        "tiền chưa về, hay nằm trên sheet đã bị xoá khỏi workbook",
    "khong_co_so_chung_tu":
        "chưa có số chứng từ — phải tra bằng TIỀN + NGÀY",
    # ⭐⭐ `WO-037` *(`BA-07` v3.9 §4g ⓹ ⓐ)* — câu **có chỗ trống** `{ma}`: mã
    #   tiền tệ **thật** của (các) dòng khớp mã. ⛔ Một câu chung *"khác tiền
    #   tệ"*: kế toán cần biết tiền đã đi bằng **đồng nào** để tra *(sổ thật
    #   02/10: USD 63 · VND 15 · SGD 5 · HKD 1 lệnh — `Q-FX-1`)*. Gắn chữ bằng
    #   `cau_ma_khop_khac_tien_te` — ⛔ `.format` rải rác.
    "ma_khop_khac_tien_te":
        "số chứng từ khớp một dòng tiền bằng {ma} — cửa ghi không ghép hai "
        "tiền tệ, và không ghép theo một số tiền trùng",
}


def cau_ma_khop_khac_tien_te(ma: list[str]) -> str:
    """Câu `vi_sao` của lệnh **chỉ** khớp mã ở tiền tệ khác — `ma` là mã tiền
    tệ *(đã qua `ma_tien_te`)* của các dòng khớp; trùng gộp, xếp chữ cái.

    ⚠ Mã rỗng *(dòng tiền ⛔ có `curr`)* in `(trống)` — ⛔ bỏ: một câu *"bằng
      — "* là câu **nói thiếu**, và bỏ hẳn mã ấy đi thì câu nói sai.
    """
    ds = sorted({m or "(trống)" for m in ma})
    return VI_SAO["ma_khop_khac_tien_te"].format(ma=", ".join(ds))


def la_khop_ma_chi_khac_tien_te(d: dict[str, Any]) -> bool:
    """Lệnh đã qua `xep_ro` có ở **đúng** nhánh *"khớp mã chỉ ở tiền tệ khác"*.

    ⭐ Nhánh ấy là nhánh **duy nhất** của `xep_ro` cho `ro = nguoi` **khi lệnh
      có mã** *(nhánh kia — ⛔ mã — là `khong_co_so_chung_tu`)*; hỏi hàm này
      chứ ⛔ so chuỗi `vi_sao` *(câu có chỗ trống)* hay chép lại điều kiện.
      `xu_ly._gd_vao_the` dùng nó để quyết `the.vi_sao` *(`HOI-038` phương
      án B — câu thay ô *"đề xuất"* ở bảng `F01G`)*.
    """
    return d.get("ro") == RO_NGUOI and bool(d.get("ma_canon"))


def chi_muc_ma(conn, pv: PhamVi) -> dict[str, list[tuple]]:
    """`canon_ref(doc_no)` → `[(itl_id, curr, tien)]` của các dòng **chưa nối**.

    ⛔ Dùng lại **đúng** `_SQL_ITL_MA` mà bậc `ma` đang dùng — ⛔ không viết
      câu thứ hai, vì hai câu là hai chỗ để chúng lệch nhau.
    """
    dk, ts = pv.dieu_kien("i.run_id")
    thom: dict[str, list[tuple]] = {}
    with conn.cursor() as cur:
        cur.execute(_SQL_ITL_MA.format(dk=dk), ts)
        for itl_id, doc_no, curr, tien in cur.fetchall():
            k = canon_ref(doc_no)
            if k:
                thom.setdefault(k, []).append((itl_id, curr, tien))
    return thom


def tap_tu_chung(conn, pv: PhamVi) -> set[str]:
    """Cac `pm_line_id` ma **cua GHI chac chan nhan** trong mot cu bam LO.

    ⛔⛔⛔ **Vi sao ham nay ton tai, va no sua mot con so TOI DA HIEN SAI.**

    Ban dau `xep_ro` tu tinh `tu_chung` = *"dung mot ung vien khop ca tien va
    don vi tien te"*. Do 11/09:

        dinh nghia CUA TOI : 90 dong lenh -> 127 `itl_id`
        cua GHI (`ds_tu_chung`) :             47 `itl_id`
        giao                                  47  ⇒ **bank ⊂ cua toi**

    ⇒ **80** `itl_id` ma man hinh goi la *"may tra loi duoc, bam duyet thoi"*
      se bi cua ghi **TU CHOI CA LO** (`FLS-GHEP-KHONG-TU-CHUNG`). Mot con so
      hua nhieu hon cai bam duoc la mot con so **noi doi**.

    ⛔ `ds_tu_chung` khai thang no la gi: *"tap ma `ghep_lenh` **chac chan
      nhan**"* — no da kiem ca bon cong (`da ghep` · `khac tien te` ·
      `lech tong` · `chua duyet`). ⇒ Man hinh **hoi no**, ⛔ khong dung mot
      luat thu hai. Dung bai hoc *"do QUAN HE thi goi ham that"*.
    """
    from fls.repo.do_mau_so import ds_tu_chung      # repo → repo, hop le
    d = ds_tu_chung(conn, pv)
    return {p for ds in d["tu_chung"].values() for p in ds}


def gan_ma_canon(dong: list[dict[str, Any]]) -> None:
    """Gắn `ma_canon = canon_ref(ref_tho)` — **mã số chứng từ của CHÍNH dòng
    lệnh** — vào từng dòng. Sửa **tại chỗ**.

    ⭐⭐ **MỘT** chỗ gắn cho **cả hai** cửa danh sách *(`BA-07` v3.8 §4h ⓵',
      `WO-032` vòng 2 `(i)`)*: `xep_ro` *(cửa `lenh-cho`)* gọi nó, và
      `xu_ly.lenh_da_gan` gọi nó **trước** `_gan_gd`. `xu_ly._bac` đọc
      `ma_canon` để chia bậc `ma` cho `gd` / `gd_ds`.

    ⛔⛔ **Bia `HOI-033`.** Trước 02/10 phép gắn này nằm **trong thân `xep_ro`**,
       mà `xep_ro` **chỉ** chạy ở cửa `lenh-cho` ⇒ cửa `lenh-da-gan` gọi
       `_gan_gd` với dòng **⛔ có** `ma_canon` ⇒ `_bac` ⛔ BAO GIỜ ra `ma` ở
       cửa ấy. Sổ thật 02/10 *(chỉ đọc, gọi hàm thật mọi trang)*: mối nối
       `gd_ds` khớp số chứng từ **2.262 / 2.262**, cửa trả `ma` **0**
       *(`tien` 2.128 · `cung_tien_te` 134)*; khối *"✓ Đang gán"* chip `①`
       **0 / 2.219** lệnh *(`②` 2.121 · `④` 98)* — **100%** chip nói một bậc
       **yếu hơn** sự thật, và ⛔ bài nào đỏ: khuôn có trường `bac`, chỉ là
       giá trị sai.
    ⛔ Một bản thứ hai *(vd. `regexp` trong SQL, hay gọi `canon_ref` lần nữa ở
      tầng cửa)* là đúng lớp lỗi khối chú thích trên `chi_muc_ma` đã đo:
      `regexp` lệch `canon_ref` **17,9%**. Bài quét
      `tests/api/test_wo032_v2_bac_da_gan_pg.py` đòi **một** chỗ đặt khoá
      `ma_canon` trong `fls/`.
    """
    for d in dong:
        d["ma_canon"] = canon_ref(d.get("ref_tho"))


def xep_ro(dong: list[dict[str, Any]],
           chi_muc: dict[str, list[tuple]],
           tu_chung: set[str] | None = None) -> None:
    """Gắn `ro` · `vi_sao` · `tu_chung` · `ung_vien_itl` vào **từng** dòng.

    Sửa **tại chỗ**. ⛔ Không trả bản sao: người gọi đang cầm đúng trang mà
    màn hình sẽ vẽ, và hai bản là hai chỗ để chúng lệch nhau.

    ⚠ `tu_chung` chỉ `True` khi **đúng một** ứng viên và ứng viên ấy khớp
      **cả tiền lẫn đơn vị tiền tệ**. Nhóm *"khớp mã nhưng lệch tiền"*
      *(`160` dòng, `11/09`)* ⛔ **KHÔNG** được gộp vào đây: ở đó máy **phải**
      hỏi *"lệnh này ăn bao nhiêu của giao dịch kia"*, và trả lời hộ là để
      **máy quyết thay người** *(`INV-I16`)*.
    """
    # ⭐ `ma_canon` gắn ở **một** chỗ dùng chung với `lenh-da-gan` — xem
    #   `gan_ma_canon` *(`WO-032` vòng 2 `(i)`)*.
    gan_ma_canon(dong)
    # ⚠ ⛔ Viết một bản `strip().upper()` ở đây cho gọn — đó là bản so thứ
    #   ba mà `WO-032` Rủi ro 2 / `KQ-036 F-1` cấm. *(Trước `WO-042`: nhập
    #   TRONG hàm từ `man_ghep` vì vòng nhập; nay từ `fls.canon.tien_te`
    #   ở đầu tệp.)*
    for d in dong:
        k = d["ma_canon"]
        if not k:
            d["ro"], d["vi_sao"] = RO_NGUOI, VI_SAO["khong_co_so_chung_tu"]
            d["tu_chung"], d["ung_vien_itl"] = False, []
            continue
        ung = chi_muc.get(k)
        if not ung:
            d["ro"], d["vi_sao"] = RO_KHONG, VI_SAO["khong_co_tien_trong_so"]
            d["tu_chung"], d["ung_vien_itl"] = False, []
            continue
        # ⭐⭐⭐ `WO-037` *(`BA-07` v3.9 §4g ⓹ ⓐ ⓑ)* — rổ `may` đo theo luật
        #   **CỬA GHI**: chỉ dòng khớp mã **CÙNG** tiền tệ mới là câu trả lời
        #   của máy. ⛔ Trước 02/10 nhánh này ⛔ hỏi tiền tệ ⇒ sổ thật *(ảnh
        #   `NAP-2026-10-02-PMA07ED283`, chỉ đọc, hàm thật)* **84 / 268** lệnh
        #   rổ `may` có đề xuất đầu *(`the.gd`)* là dòng **khác tiền tệ** —
        #   cặp cửa ghi **TỪ CHỐI** *(`QĐ-ITL-62`)*; cả **84 / 84** ⛔ có dòng
        #   khớp mã nào cùng tiền tệ. Người đầu tiên bấm theo máy sẽ gặp ngõ
        #   cụt ở gần **một phần ba** rổ dễ nhất.
        #   ⛔⛔ ⛔ vá bằng *"lấy ứng viên cùng tiền tệ ở bậc tiền"*: **45** lệnh
        #   có ứng viên cùng tiền tệ lệch `0`, nhưng trung vị **16** dòng cùng
        #   số ấy, cách dòng khớp mã trung vị **294 ngày** ⇒ trùng tiền **tình
        #   cờ** — đổi cú bấm bị từ chối *(0 ghi sai)* lấy cú ghép **SAI mà cửa
        #   ghi NHẬN**. Đề xuất phải vừa **ghi được** vừa có **bằng chứng mã**.
        #   ⚠ Lệnh ⛔ có `curr` ⇒ ⛔ dòng nào "cùng" *(như `lech_ung_vien`)*.
        cl = ma_tien_te(d.get("curr"))
        cung = [u for u in ung if cl and ma_tien_te(u[1]) == cl]
        if not cung:
            d["ro"] = RO_NGUOI
            d["vi_sao"] = cau_ma_khop_khac_tien_te(
                [ma_tien_te(u[1]) for u in ung])
            # ⛔ `tu_chung` chỉ có nghĩa trong rổ `may` *(`BA-07` §4g ⓹ ⓒ —
            #   sổ thật **0 / 84** lệnh nhóm này mang nó)*.
            d["tu_chung"], d["ung_vien_itl"] = False, []
            continue
        d["ro"], d["vi_sao"] = RO_MAY, ""
        d["ung_vien_itl"] = [u[0] for u in cung]
        # ⛔ `tu_chung` = **cua GHI noi the**, ⛔ khong phai phep do cua man
        #   hinh (xem `tap_tu_chung`). `None` ⇒ ⛔ chua hoi ⇒ **False**, chu
        #   ⛔ khong doan bang mot luat thu hai.
        d["tu_chung"] = bool(tu_chung and d["pm_line_id"] in tu_chung)


def dem_theo_ro(conn, pv: PhamVi) -> dict[str, int]:
    """Đếm **toàn bộ** dòng lệnh chưa nối theo rổ. ⛔ Không phân trang.

    ⛔⛔ **Vì sao phải có, chứ ⛔ không để màn hình đếm trang đang xem.** Một
       trang là `50`–`500` dòng; đếm trên trang rồi in ra như một tổng là
       **đúng lớp lỗi** `do_phu` đã dính *(đếm số dòng trả về của một cửa có
       trần `500`, nên con số **im lặng dừng ở 500**)*. Ở đây còn tệ hơn: thứ
       tự là `(tiền tệ, hạng)` nên một trang ⛔ **không phải** một mẫu ngẫu
       nhiên — nó nghiêng hẳn về đồng tiền đứng đầu bảng chữ cái.

    ⚠ Trả **cả** `tong` để người đọc cộng lại được và thấy ba rổ **khép**.
      Một bảng phân loại ⛔ không cộng về tổng là một bảng ⛔ không kiểm được.

    ⭐⭐ `nguoi_khac_tien_te` *(`WO-037` vòng 2 `(i)` — `BA-07` v3.10 §4g,
      `BG-039` yếu #1)*: số lệnh rổ `nguoi` ở **đúng** nhánh *"khớp mã chỉ ở
      tiền tệ khác"*. Sau vòng 1 rổ `nguoi` có **hai** loại lệnh, mà băng
      `F01L` nói *"Chưa có số chứng từ"* cho cả rổ — sổ thật 02/10 *(ảnh
      `NAP-2026-10-02-PMA07ED283`)* sai **84 / 616**. Đếm bằng **chính**
      `la_khop_ma_chi_khac_tien_te` *(hàm quyết `the.vi_sao`)* — ⛔ so chuỗi
      `vi_sao` *(câu có chỗ trống)*, ⛔ chép điều kiện — trong **cùng** vòng
      lặp *(⛔ vòng thứ hai: hàm này đã kéo mọi trang)*. **Luôn có mặt**, `0`
      khi ⛔ lệnh nào: một khoá vắng khi `0` buộc màn đoán *"vắng là 0 hay là
      cửa cũ"*.
    """
    chi_muc = chi_muc_ma(conn, pv)
    tc = tap_tu_chung(conn, pv)
    t = doc_lenh_cho(conn, pv, limit=TRANG_TOI_DA)
    dem = {RO_MAY: 0, RO_NGUOI: 0, RO_KHONG: 0, "tu_chung": 0, "tong": 0,
           "nguoi_khac_tien_te": 0}
    con_tro = t.con_tro
    while True:
        xep_ro(t.dong, chi_muc, tc)
        for d in t.dong:
            dem[d["ro"]] += 1
            dem["tong"] += 1
            if d["tu_chung"]:
                dem["tu_chung"] += 1
            if la_khop_ma_chi_khac_tien_te(d):
                dem["nguoi_khac_tien_te"] += 1
        if not con_tro:
            break
        t = doc_lenh_cho(conn, pv, con_tro=con_tro, limit=TRANG_TOI_DA)
        con_tro = t.con_tro
    return dem


def doc_lenh_cho_theo_ro(conn, pv: PhamVi, ro: str, *,
                         tu_chung: bool | None = None,
                         con_tro: str | None = None,
                         limit: int | None = None) -> Trang:
    """Dòng lệnh chờ **của MỘT rổ** (`BA-12 §2`, `G2`).

    ⛔⛔⛔ **Vì sao hàm này TỐN hơn `doc_lenh_cho`, và vì sao khai ra chứ ⛔
       không giấu.** Rổ tính ở **Python** *(`canon_ref` trên cả hai vế — xem
       `chi_muc_ma`)*, nên nó ⛔ **không lọc được trong `WHERE`**. ⇒ Hàm này
       **kéo hết** dòng lệnh chưa nối, xếp rổ, lọc, **rồi mới** cắt trang.

       Cái giá ấy **đo được và có trần**: `1.553` dòng *(11/09)*, và trần thật
       là số dòng lệnh của **một** ảnh PM — `3.772`. ⛔ Nó ⛔ không lớn theo
       kích thước sổ *(`8.387` dòng tiền ⛔ không ảnh hưởng)*.

    ⚠ ⛔ **Đừng "tối ưu" bằng cách viết phép chuẩn hoá vào SQL.** Đó đúng là
      cái đã cho ra `121` thay vì `250` ngày `11/09` *(sai 107%)*, và `560`
      thay vì `475` ngày `09/09`. Chậm mà đúng ⛔ không đổi được lấy nhanh mà
      sai.

    `tu_chung=True` thu hẹp rổ `may` về nhóm **tự chứng** *(khớp cả tiền)*.
    """
    if ro not in (RO_MAY, RO_NGUOI, RO_KHONG):
        raise ValueError(
            f"ro={ro!r} phai la mot trong {RO_MAY!r}/{RO_NGUOI!r}/{RO_KHONG!r}")
    n = _trang(limit)
    chi_muc = chi_muc_ma(conn, pv)
    tc = tap_tu_chung(conn, pv)
    het: list[dict[str, Any]] = []
    t = doc_lenh_cho(conn, pv, limit=TRANG_TOI_DA)
    while True:
        xep_ro(t.dong, chi_muc, tc)
        het += [d for d in t.dong
                if d["ro"] == ro
                and (tu_chung is None or bool(d["tu_chung"]) is tu_chung)]
        if not t.con_tro:
            break
        t = doc_lenh_cho(conn, pv, con_tro=t.con_tro, limit=TRANG_TOI_DA)

    # ⛔ Con tro giu **cùng hình dạng** `"<tien te>:<hang>"` cua `doc_lenh_cho`
    #   — man hinh ⛔ khong duoc biet o day phan trang bang mot co che khac.
    if con_tro:
        c, h = con_tro.split(":", 1)
        het = [d for d in het
               if (d["curr"], d["hang"]) > (c, int(h))]
    con = (f"{het[n - 1]['curr']}:{het[n - 1]['hang']}"
           if len(het) > n else None)
    return Trang(dong=het[:n], con_tro=con, pham_vi=pv.mo_ta())


def doc_mot_dong_lenh(conn, pv: PhamVi, pm_line_id: str) -> dict[str, Any] | None:
    """**Toàn bộ** một dòng lệnh chi — 8 trường đã phân tích + **cả hàng thô**
    + **các dòng khác cùng phiếu**. `None` nếu ⛔ không có.

    ⛔⛔⛔ **Vì sao cửa này ra đời.** Owner `11/09`: *"bảng PM vẫn chưa đủ các
       trường như trong GGSheet"*. Đo thật: `PM_Unpivot` có **28 cột**, FLS
       đọc **8** — và `20` cột bỏ qua kia điền **100%**, trong đó có đúng hai
       thứ một người dùng để nhận ra khoản tiền:

         cột `7`  *Nội dung giao dịch nhập khi lập lệnh ở bank*  — 100%
         cột `13` *Tên tài khoản* — tức **trả cho AI**            — 100%

       ⇒ `535` dòng ⛔ không có số chứng từ **chỉ tra được bằng hai cột ấy**,
         mà màn hình ⛔ không hề hiện chúng. Hàm này mở cả `28` cột ra.

    ⚠ `tho = None` có nghĩa **THẬT**: *"dòng này thuộc ảnh chụp TRƯỚC `11/09`"*
      — ⛔ không phải *"đọc được 0 cột"*. Màn hình phải nói đúng câu ấy
      *(`INV-I16`)*.
    """
    run_pm = anh_pm_hieu_luc(conn, pv)
    with conn.cursor() as cur:
        cur.execute(_SQL_MOT_DONG_LENH, {"run_pm": run_pm, "id": pm_line_id})
        d = _dong(cur)
        if not d:
            return None
        mot = d[0]
        cur.execute(_SQL_CA_PHIEU, {"run_pm": run_pm, "id": pm_line_id,
                                    "slip": mot["pm_slip_id"]})
        mot["ca_phieu"] = _dong(cur)
    mot["anh_pm"] = run_pm
    return mot


# ── ⭐⭐ RO **DA GAN** — bu cua `_CTE_LENH_CHO` (`GAP-API-08`) ───────────
#
# ⛔⛔ **Vi sao mot cau SQL RIENG chu ⛔ khong mot co tren `_SQL_LENH_CHO`.**
#    `_CTE_LENH_CHO` co ca mot bo may **xep hang theo tien** *(`row_number`
#    ＋ `luy_ke_pct` ＋ `PARTITION BY curr`)*, va bo may ay tra loi cau
#    *"xem toi dau thi du"* — mot cau **chi co nghia voi viec dang cho**.
#    Mot dong **da gan** ⛔ khong con la viec, nen mot thu hang cho no la mot
#    con so vo nghia ma man se hien nhu that.
#
# ⛔ `fls_moi_noi`, ⛔ KHONG `fls_pm_link` — cung ly do da ghi o `_COT_LENH`:
#   bang goc con giu ca moi noi **DA BO**.
#
# ⭐⭐ `array_agg` chu ⛔ KHONG `min(itl_id)`: do `22/09` tren kho that,
#   **23/2.219 = 1,0%** lenh chi gan **nhieu hon mot** dong tien. Mot con so
#   se **im lang bo mat** phan con lai — dung o cho nguoi ta bam `Bo gan`.
# ⛔⛔⛔ **`fls_moi_noi` PHAI duoc loc theo PHAM VI — va loc qua phia ITL.**
#
# `pm_line_id` la mot **khoa nghiep vu**: no **lap lai o moi lan nap**. Con
# `itl_id` la khoa cua **mot dong trong mot anh chup**. ⇒ Mot cau con chi hoi
# `WHERE m.pm_line_id = l.pm_line_id` se vo ca moi noi cua **moi lan nap khac**
# — bai thu bat duoc ngay: `[2, 3, 23, 24]` thay vi `[23, 24]`.
#
# ⚠ Va phai loc o **phia ITL** *(`i.run_id`)*, ⛔ khong phai phia PM: anh chup
#   ngan hang va anh chup PM la **HAI lan nap khac nhau**, nen lay `run_pm` ap
#   cho ve tien se ra rong tren kho that.
_SQL_LENH_DA_GAN = """
SELECT {cot}, COALESCE(l.amount, 0) AS tien,
       (SELECT array_agg(DISTINCT m.itl_id)
          FROM fls_moi_noi m
          JOIN fls_itl i ON i.itl_id = m.itl_id
         WHERE m.pm_line_id = l.pm_line_id AND {dk}) AS itl_da_gan
  FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s
   AND EXISTS (SELECT 1 FROM fls_moi_noi m
                 JOIN fls_itl i ON i.itl_id = m.itl_id
                WHERE m.pm_line_id = l.pm_line_id AND {dk})
   {them}
 ORDER BY l.pm_line_id
 LIMIT %(n)s"""


def doc_lenh_da_gan(conn, pv: PhamVi, *, con_tro: str | None = None,
                    limit: int | None = None) -> Trang:
    """Dong lenh chi **DA tim duoc tien** — `GAP-API-08`.

    ⛔⛔ **Vi sao mot tuyen RIENG chu ⛔ khong mot co tren `/queue/lenh-cho`.**
       Ten `lenh-cho` co nghia *"dang cho"*; cho no tra dong **da noi** la de
       mot cai ten **noi doi**, va moi nguoi doc ma sau nay se tin cai ten.

    ⭐ Hai ro phai **KHEP ve tong**: do `22/09` tren kho that, `2.219` da gan
      ＋ `1.553` chua gan = **`3.772`** = toan bo anh PM hieu luc. Hai ro
      chong nhau thi mot dong hien **hai lan** o chip `Tat ca`, va ⛔ khong ai
      cong duoc.

    ⭐ Con tro la `pm_line_id` — khoa **DON**, vi thu tu o day la
      `(pm_line_id)`. ⚠ ⛔ Khong dung `(curr, hang)` nhu `doc_lenh_cho`: ro
      nay ⛔ khong co thu hang theo tien.
    """
    n = _trang(limit)
    dk, ts_dk = _dk_ten(pv, "i.run_id")
    ts: dict[str, Any] = {"run_pm": anh_pm_hieu_luc(conn, pv), "n": n + 1,
                          **ts_dk}
    them: list[str] = []
    if con_tro:
        them.append("AND l.pm_line_id > %(ct)s")
        ts["ct"] = con_tro
    sql = _SQL_LENH_DA_GAN.format(cot=", ".join(_COT_LENH), dk=dk,
                                  them=" ".join(them))
    with conn.cursor() as cur:
        cur.execute(sql, ts)
        dong = _dong(cur)
    # ⭐ `array_agg` tra thu tu **⛔ khong bao dam** ⇒ xep o Python, de hai lan
    #   goi cung mot cua ra cung mot danh sach. Mot thu tu doi giua hai lan
    #   doc lam moi phep so sanh phia tren **lech ma ⛔ khong ai biet vi sao**.
    for d in dong:
        d["itl_da_gan"] = sorted(d.get("itl_da_gan") or [])
    con = dong[n - 1]["pm_line_id"] if len(dong) > n else None
    return Trang(dong=dong[:n], con_tro=con, pham_vi=pv.mo_ta())


# ── ⭐⭐ GIAO DICH cua tung dong lenh — cot `Giao dich da gan` cua BANG ────

def gd_theo_itl(conn, pv: PhamVi,
                ids: list[int] | set[int]) -> dict[int, dict[str, Any]]:
    """`itl_id` → hang THO cua dong tien. ⭐ **MOT** truy van cho **ca trang**.

    ⛔⛔ **Vi sao can ham nay.** Ban dung co bang so **12 cot**, ba cot cuoi la
       `Giao dich da gan` · `So tien GD` · `Bac`. Nhung ca hai cua danh sach
       chi tra **ID**: `ung_vien_itl = [47298]`, `itl_da_gan = [28338]`. ⇒ Man
       ⛔ khong co gi de ve ba cot ay, va tra tung dong mot la **738 luot goi
       cua** cho mot lan mo man.

    ⭐ Dung lai **dung** `_SQL_ITL_THEO_ID` ma bac `ma` dang dung — no da cho
      `dien_giai` · `doc_date` · `source_sheet` · `ps_no`/`ps_co`. ⛔ Viet mot
      cau thu hai o day la tao mot **ban su that thu hai** ve *"mot dong tien
      trong nhu the nao"*, va hai ban se lech.

    ⛔ `ids` rong ⇒ tra `{}` **⛔ khong goi kho**: mot truy van `IN ()` vua vo
      nghia vua la mot luot di kho ⛔ khong ai can.
    """
    ds = sorted({int(i) for i in (ids or [])})
    if not ds:
        return {}
    dk, ts = _dk_ten(pv, "i.run_id")
    with conn.cursor() as cur:
        cur.execute(_SQL_ITL_THEO_ID.format(cot=", ".join(_COT_ITL), dk=dk),
                    {"ids": ds, **ts})
        return {d["itl_id"]: d for d in _dong(cur)}
