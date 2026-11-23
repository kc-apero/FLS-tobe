"""`A2` — DON ANH CHUP. `QĐ-ITL-115`: giu **VINH VIEN** anh DA DUNG de nap,
don anh ⛔ khong ai dung sau **30 ngay**.

⛔⛔⛔ **Vi sao module nay ton tai — va vi sao no phai la mot TEP RIENG.**

`fls/repo/chup.py` la **cho ghi duy nhat** cua ba bang anh chup, va no bi mot
cong quet ma nguon cam **moi** cau `UPDATE`/`DELETE`. Cong ay **dung**, va ly le
cua no ⛔ khong he yeu: *"sua mot anh chup tai cho la doi cai ma mot lo da nap
dua vao — bien ban 9 luat cua lo ay bong noi ve du lieu ⛔ khong con ton tai, va
⛔ khong ai thay gi doi"*.

⇒ Nhung `QĐ-ITL-114` chot **nhip moi gio, 8h–19h** ⇒ **3.000 anh/nam = 6,6 GB**,
  ma anh **that su duoc nap** chi ~1/ngay = **250 anh = 0,55 GB** ⇒ **11/12 anh
  moi ngay ⛔ khong but toan nao tro toi**. Owner chot nhip ay **cung luc** voi
  phep don, va hai quyet dinh ay ⛔ **khong tach roi duoc**.

⚠ Va tien le that: `fls-test-store-grows-unbounded` — kho phinh lam **4 cong DO
  gia** *(`doc_cong` mat 15,6s > timeout 10s)*. Mot kho phinh ⛔ khong chi ton
  dia: no **lam cong noi doi**.

★★ **Cho nay ⛔ KHONG noi long cong tren — no LAM SAC HON.** Ba luat:

  ⓐ Tep nay **CHI** duoc `DELETE`. ⛔ Khong `INSERT`, ⛔ khong `UPDATE`.
  ⓑ **Moi** cau `DELETE` phai mang **HANG RAO** `NOT EXISTS … fls_run` — tuc
    *"⛔ khong but toan nao tro toi anh nay"*. Chinh hang rao ay giu nguyen y
    nghia cua cong cu: mot anh **da duoc nap** thi ⛔ **khong bao gio** bi xoa,
    nen ⛔ khong lo nao **da nap** bi mat can cu.
  ⓒ Co **cong quet ma nguon** doi ca ⓐ va ⓑ — `tests/repo/test_chi_mot_cho_
    ghi_tay.py`. ⛔ Mot loi hua trong docstring ⛔ khong phai mot hang rao.

⛔⛔ **Va vi sao xoa theo `chup_id` CU THE chu ⛔ khong mot cau `DELETE` quet
   ca bang.** Ba bang, ba cau xoa, va chung phai xoa **dung cung mot tap**.
   Mot cau quet ca bang cho tung bang la ba phep quet **doc lap** — chung se
   lech neu mot but toan xuat hien **giua** hai cau, va luc do `fls_chup_dong`
   mat dong trong khi `fls_chup` con dau. ⇒ **Chon tap MOT lan**, roi xoa ba
   bang theo dung tap ay, trong **mot giao dich**.
"""
from __future__ import annotations

from typing import Any

# ⭐ `QĐ-ITL-115` — owner chot **30 ngay**. Khai o day, mot cho.
GIU_NGAY = 30

# ⛔⛔ HANG RAO — khai **mot lan**, dung o **ca hai** cau *(phep do va phep
#    xoa)*. Hai ban se lech, va luc do phep do se noi *"se xoa 40 anh"* trong
#    khi phep xoa xoa mot tap khac.
#
# ⚠ `NOT EXISTS … fls_run` la ve *"⛔ khong but toan nao tro toi"*. `QĐ-ITL-115`
#   dat no bang mot cau **do duoc**: *"ly do giu dong tho la de chung minh mot
#   but toan den TU DAU ⇒ anh ⛔ khong but toan nao tro toi thi no ⛔ khong
#   chung minh gi"*.
_HANG_RAO = (
    "c.doc_luc < now() - make_interval(days => %(giu)s)"
    " AND NOT EXISTS (SELECT 1 FROM fls_run r WHERE r.chup_id = c.chup_id)")

_SQL_CHON = """
SELECT c.chup_id, c.doc_luc, c.lan
  FROM fls_chup c
 WHERE """ + _HANG_RAO + """
 ORDER BY c.doc_luc
"""

# ⚠ Va mot cau DO nua — **anh duoc GIU**, tach theo LY DO. ⛔ Mot bao cao chi
#   noi *"xoa 40"* ma ⛔ khong noi *"giu 250 vi da nap · giu 12 vi con moi"* la
#   mot bao cao ⛔ khong ai duyet duoc: nguoi doc ⛔ khong biet phep don co
#   dung dau vao khong.
_SQL_GIU = """
SELECT count(*) FILTER (WHERE EXISTS (
         SELECT 1 FROM fls_run r WHERE r.chup_id = c.chup_id))       AS da_nap,
       count(*) FILTER (WHERE NOT EXISTS (
         SELECT 1 FROM fls_run r WHERE r.chup_id = c.chup_id)
         AND c.doc_luc >= now() - make_interval(days => %(giu)s))    AS con_moi,
       count(*)                                                      AS tong
  FROM fls_chup c
"""


def do_don(conn, *, giu_ngay: int = GIU_NGAY) -> dict[str, Any]:
    """⛔ **CHI DO** — tra ve *"neu don thi xoa gi"*. ⛔ Khong xoa mot dong nao.

    ⇒ `se_xoa[]` mang **`chup_id` · `doc_luc` · `lan`** cua tung anh, ⛔ khong
      chi mot con so: mot bao cao noi *"se xoa 40 anh"* ma ⛔ khong noi **anh
      nao** la mot bao cao ⛔ khong ai duyet duoc.
    """
    if int(giu_ngay) < 1:
        raise ValueError(
            f"⛔ `giu_ngay={giu_ngay}` — `0` nghia la *xoa moi anh chua duoc "
            f"nap NGAY HOM NAY*, ke ca anh vua chup xong va dang cho nguoi bam "
            f"nhan. Owner chot **{GIU_NGAY}** (`QĐ-ITL-115`)")
    with conn.cursor() as cur:
        cur.execute(_SQL_CHON, {"giu": int(giu_ngay)})
        ds = [{"chup_id": r[0], "doc_luc": r[1], "lan": r[2]}
              for r in cur.fetchall()]
        cur.execute(_SQL_GIU, {"giu": int(giu_ngay)})
        g = cur.fetchone()
    return {
        "giu_ngay": int(giu_ngay),
        "se_xoa": ds,
        "so_se_xoa": len(ds),
        # ⭐ Ba con so cua ve GIU — ⛔ khong bao gio chi bao ve XOA.
        "giu_vi_da_nap": int(g[0]),
        "giu_vi_con_moi": int(g[1]),
        "tong_anh": int(g[2]),
    }


def don_anh_chup(conn, *, actor: str,
                 giu_ngay: int = GIU_NGAY) -> dict[str, Any]:
    """XOA cac anh ⛔ khong but toan nao tro toi va da qua `giu_ngay`.

    ⛔ `actor` **bat buoc** — don la mot HANH VI, va no xoa du lieu. ⚠ Va no
    ⛔ khong vao mot so nhat ky nao *(⛔ khong co bang cho viec do)*, nen `actor`
    o day di vao **bao cao** cua nguoi goi. Khai thang cho thieu ay thay vi de
    no trong nhu da co vet.
    """
    if not str(actor or "").strip():
        raise ValueError("⛔ thieu `actor` — don la mot HANH VI, phai co ten")
    d = do_don(conn, giu_ngay=giu_ngay)
    ids = [x["chup_id"] for x in d["se_xoa"]]
    if not ids:
        return dict(d, so_da_xoa=0, so_dong_da_xoa=0, so_nguon_da_xoa=0,
                    actor=actor)

    # ⛔⛔ MOT giao dich cho ba bang, va tap duoc **chon MOT lan** o tren.
    with conn.transaction(), conn.cursor() as cur:
        cur.execute(
            "DELETE FROM fls_chup_dong d USING fls_chup c"
            " WHERE d.chup_id = c.chup_id AND c.chup_id = ANY(%(ids)s)"
            " AND " + _HANG_RAO, {"ids": ids, "giu": int(giu_ngay)})
        n_dong = cur.rowcount
        cur.execute(
            "DELETE FROM fls_chup_nguon n USING fls_chup c"
            " WHERE n.chup_id = c.chup_id AND c.chup_id = ANY(%(ids)s)"
            " AND " + _HANG_RAO, {"ids": ids, "giu": int(giu_ngay)})
        n_nguon = cur.rowcount
        cur.execute(
            "DELETE FROM fls_chup c WHERE c.chup_id = ANY(%(ids)s)"
            " AND " + _HANG_RAO, {"ids": ids, "giu": int(giu_ngay)})
        n_anh = cur.rowcount
    return dict(d, so_da_xoa=n_anh, so_dong_da_xoa=n_dong,
                so_nguon_da_xoa=n_nguon, actor=actor)
