# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ CONG CANH: **FE co bam THIET KE DA CO ⛔ khong**.

⭐ Owner `22/09`: *"luu y dam bao FE bam sat thiet ke da co"*.

⛔⛔ **Mot loi nhac ⛔ khong giu duoc gi.** Do duoc, tren chinh du an nay:
   `man_f01_lenh.js` di **`339 → 735`** dong qua **7** lan sua trong **2** ngay
   va ⛔ **khong** lan nao tong di xuong. Moi lan sua deu co ly do rieng va deu
   dung; cai mat di la **hinh dang tong the**, va no mat **trong im lang**.

⇒ Tep nay bien **hop dong thiet ke** (`Artifacts/Thiet-ke-Man-Gan-Lenh-Chi.md`
  + `BA-06 §4.5`/`§4.6`) thanh **phep do tren ma FE**.

⛔ Cong nay ⛔ **khong** do *"trong co dep ⛔ khong"* — no do nhung dieu hop
  dong khai la **⛔ KHONG DUOC VI PHAM**, va moi dieu deu dem duoc.
"""
from __future__ import annotations

import io
import pathlib
import re

GOC = pathlib.Path(__file__).resolve().parents[2]
MAN = GOC / "fls" / "web" / "tep" / "man_f01_ghep.js"


def _nguon() -> str:
    assert MAN.exists(), f"⛔ ⛔ chua co man ghep: {MAN}"
    return io.open(MAN, encoding="utf-8").read()


def _ma_chay(s: str) -> str:
    """Bo chu thich — ⭐ cung bai hoc cua `test_chieu_KHONG_duoc_suy_tu_pay_type`.

    ⛔ Mot phep do quet ca van xuoi se bat ca **loi canh bao ve loi**, va khi
       ay no ⛔ khong do cai no tuong.
    """
    s = re.sub(r"/\*.*?\*/", "", s, flags=re.S)
    return re.sub(r"(?m)^\s*//.*$", "", s)


# ── ⓐ BON chip loc, ⛔ khong ba ─────────────────────────────────────────

def test_co_DU_BON_chip_loc():
    """⛔ Ban dung co **ba** ⇒ `768` dong DICH CUOI bi tron vao viec hang ngay
    ⇒ danh sach mac dinh `1.553` thay vi **738** (`G-a` truot, `INV-I20`)."""
    s = _ma_chay(_nguon())
    for chip in ("chua_gan", "da_gan", "khong_gan_duoc", "tat_ca"):
        assert chip in s, f"⛔ thieu chip `{chip}`"


def test_chip_mac_dinh_la_CHUA_GAN():
    assert re.search(r"chip\s*:\s*['\"]chua_gan['\"]", _ma_chay(_nguon())), (
        "⛔ chip mac dinh phai la `chua_gan` (738 dong viec that)")


# ── ⓑ BON bac, moi nghia noi MOT lan ───────────────────────────────────

def test_co_DU_BON_ky_hieu_bac():
    """⭐ `①②③④` — phan bang **thu tu ＋ mot ky hieu to mau**, ⛔ khong bon chip
    cung co: bac ④ chiem **149/226** ung vien se **nhuom het man**."""
    s = _nguon()
    for k in "①②③④":
        assert k in s, f"⛔ thieu ky hieu bac `{k}`"


def test_ten_bac_GIU_Y_NGUYEN_bon_bac_cua_cua():
    """⛔ Doi ten o mot phia lam nguoi doc tuong day la **hai thang do**."""
    s = _ma_chay(_nguon())
    for b in ("ma", "tien", "gan_tien", "cung_tien_te"):
        assert f"'{b}'" in s or f'"{b}"' in s, f"⛔ thieu bac `{b}`"


# ── ⓒ ⭐⭐⭐ THU TU HY SINH COT ──────────────────────────────────────────

def test_dien_giai_KHONG_BAO_GIO_nam_trong_danh_sach_cot_bo_duoc():
    """⭐⭐⭐ Luat cung nhat cua ca thiet ke.

    Dien giai sao ke la **bang chung duy nhat** cua **`4.145/8.387` = 49%**
    cuon so *(nhanh nuoc ngoai, `DT-I13 ⓑ`)*. Cot nao cung bo duoc **TRU NO**.
    """
    s = _ma_chay(_nguon())
    m = re.search(r"COT_BO_DUOC\s*=\s*\[([^\]]*)\]", s)
    assert m, "⛔ ⛔ chua khai `COT_BO_DUOC` ⇒ thu tu hy sinh cot ⛔ khong do duoc"
    ds = [x.strip().strip("'\"") for x in m.group(1).split(",") if x.strip()]
    assert ds == ["nguon", "doc_no"], (
        f"⛔ thu tu hy sinh phai la `Nguon` → `So CT`, do duoc: {ds}")
    assert "dien_giai" not in ds, (
        "⛔⛔ `dien_giai` nam trong danh sach cot BO DUOC — no la bang chung "
        "duy nhat cua 49% cuon so")


# ── ⓓ ⭐⭐ CHONG GAT PHAN XA ────────────────────────────────────────────

def test_ENTER_bi_KHOA_khi_lech_tien():
    """⛔ **`45%`** ca ⛔ khong co ung vien khop dung tien. Mot phim `Enter` de
    dai o day **day nguoi ta gat bua** (`NFR-I25`, `INV-I16`)."""
    s = _ma_chay(_nguon())
    assert re.search(r"khop_tuyet_doi|khop_dung_tien", s), (
        "⛔ ⛔ khong thay phep kiem *khop dung tien* — `Enter` dang gan vo dieu kien")
    m = re.search(r"Enter[\s\S]{0,400}?khop_(?:tuyet_doi|dung_tien)", s)
    assert m, "⛔ nhanh `Enter` ⛔ khong hoi *khop dung tien*"


def test_lech_tien_phai_bam_HAI_lan():
    s = _ma_chay(_nguon())
    assert "xac_nhan" in s, "⛔ ⛔ khong co trang thai xac nhan hai buoc"


def test_MAY_KHONG_chon_san_ung_vien():
    """⭐ `INV-I16` o tang ngon tay: may **de xuat**, nguoi **quyet**.

    ⚠ Viet lai `WO-023` `(i)` *(05/10, `fls-dev`)* — **giu nguyen lo goc**
    *("khoi tao `null` — ⛔ chon san")*: danh tinh lua chon doi tu chi so
    `ung_vien_chon` sang `chon_itl` *(`BA-06` v4.22 `§4.5 ⓦ` ⑥)*;
    `ung_vien_chon` nay la **phai sinh** *(getter)* nen ⛔ con dong khai
    `ung_vien_chon: null` de do. Phep do chuyen sang **cho khai that**."""
    s = _ma_chay(_nguon())
    assert re.search(r"chon_itl\s*:\s*null", s), (
        "⛔ `chon_itl` phai khoi tao `null` — ⛔ khong chon san ca nao, "
        "ke ca ca may de xuat")


# ── ⓔ ⭐ BAN PHIM — `NFR-I24`, du 9 phim ───────────────────────────────

def test_du_CHIN_phim():
    s = _ma_chay(_nguon())
    thieu = [p for p in ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight",
                         "Enter", "Escape", "'/'", "'k'", "'j'")
             if p.strip("'") not in s]
    assert not thieu, f"⛔ thieu phim: {thieu}"


def test_gan_xong_TU_NHAY_sang_lenh_ke_tiep():
    """⭐ Nhip la **tung giao dich mot** — dua nguoi ve danh sach sau moi lan
    gan la **bat ho tim lai cho cu**."""
    assert re.search(r"lenh_ke_tiep|ke_tiep_chua_gan", _ma_chay(_nguon())), (
        "⛔ ⛔ khong thay phep nhay sang lenh chua gan ke tiep")


# ── ⓕ ⭐⭐ TRUONG VANG phai HIEN ────────────────────────────────────────

def test_khoi_bung_HIEN_truong_vang_chu_KHONG_giau():
    """⛔⛔ Ban dung **bo qua** hang khi gia tri rong ⇒ truong vang bien mat
    ⛔ khong mot chu nao — o dung khoi sinh ra de ke toan **yen tam ve data**.

    ⭐ Do `21/09`: `tho` co **`41` hinh dang**; `Chi nhanh` **11,7%** ·
      `PE (Urgent)` **0,45%**.
    """
    s = _ma_chay(_nguon())
    assert re.search(r"KHONG_CO|khong_co_gia_tri", s), (
        "⛔ ⛔ khong thay nhan cho truong VANG ⇒ khoi bung dang giau im lang")
    assert not re.search(r"if\s*\(\s*!v\s*\)\s*return", s), (
        "⛔⛔ con nhanh *bo qua hang khi rong* — dung loi cua ban dung")


# ── ⓖ ⭐ BO GAN chi hoi khi co CHUM ─────────────────────────────────────

def test_bo_gan_CHI_hoi_khi_dong_tien_mang_chum():
    """⛔⛔ Hoi ca **2.222** lan de dung **25** lan la cach nhanh nhat **day
    nguoi ta bam `OK` ⛔ khong doc** — va khi ay no ⛔ khong con can duoc gi."""
    s = _ma_chay(_nguon())
    assert "can_hoi" in s, "⛔ ⛔ khong doc co `can_hoi` cua cua `chum`"
    assert "/chum" in s, "⛔ ⛔ khong goi cua `chum` truoc khi bo gan"


# ── ⓗ ⭐ NGAN SACH TRUONG = 11 (`UI-F7`, owner noi 21/09) ───────────────

def test_the_lenh_chi_DUNG_11_truong():
    s = _nguon()
    m = re.search(r"TRUONG_THE\s*=\s*\[([\s\S]*?)\]", s)
    assert m, "⛔ ⛔ chua khai `TRUONG_THE` ⇒ ngan sach truong ⛔ khong do duoc"
    n = len([x for x in m.group(1).split(",") if x.strip()])
    assert n == 11, (
        f"⛔ the lenh chi co **{n}** truong, tran `UI-F7` la **11** "
        "(owner noi 9 → 11 ngay 21/09, `QĐ-ITL-147`). Them mot ⇒ **bo mot**, "
        "hoac xin mot quyet dinh nua — mot tran doi duoc ⛔ khong can ai ky "
        "thi no ⛔ khong phai tran.")


# ── ⓘ ⛔ KHONG ma mau go tay ────────────────────────────────────────────

def test_man_NAM_TRONG_tam_quet_cua_cong_ma_mau():
    """⭐ `NFR-I19` — **⛔ KHONG viet lai phep quet o day**.

    ⛔⛔ **Ban dau toi viet mot phep quet RIENG, va no DO ngay** — vi `#f01-ghep`
       *(mot `id` CSS)* co `f01` la hex hop le. ⭐ Va cai dang noi: cong da co
       *(`test_khong_ma_mau_go_tay.py`)* **da xu dung bay ay tu lau** — no co
       han mot khoi *"MA PHAN TU ⛔ KHONG DUOC DOC NHAM THANH MAU"*.

    ⇒ Viet ban thu hai la tao **hai ban su that** ve *"the nao la mot ma mau"*,
      va ban moi hon thi **dot hon**. Bai nay chi canh mot dieu: tep man
      **nam trong tam quet** cua cong ay.
    """
    from tests.web import test_khong_ma_mau_go_tay as cong
    assert MAN.name not in cong.DUOC_CO_MAU, (
        f"⛔ `{MAN.name}` bi mien tru khoi cong ma mau")
    assert MAN.exists() and MAN.parent.name == "tep", (
        "⛔ man phai nam trong `fls/web/tep/` — do la thu muc cong ay quet")
