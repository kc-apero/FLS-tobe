"""BANG TEP — khai **mot lan**, sinh ra ca may phuc vu ca cong kiem.

★ Cung khuon voi `fls/db/model.py` va `fls/api/bang_tuyen.py`: mot ban khai duy
nhat, hai dau ra. O tang kho la (DDL + ERD); o tang cua la (dinh tuyen + cong
quet duong); o day la (may phuc vu + cong quet tep).

⛔⛔ **Vi sao mot BANG chu ⛔ khong phai mot phep ghep duong.** Cach thong thuong
la `os.path.join(THU_MUC, duong_nguoi_goi_gui)` roi kiem xem ket qua co con nam
trong `THU_MUC` khong. Phep kiem ay dung — cho den khi ai do gap mot dang ma hoa
`%2e%2e%2f`, mot lien ket tuong trung, hay mot he tep ⛔ khong phan biet hoa
thuong *(Windows — dung he dang chay)*. ⇒ O day **⛔ khong co phep ghep duong
nao voi chuoi cua nguoi goi**: duong den la mot **khoa tra bang**, khong khop
thi `None`. Loi vuot thu muc khong bi *chan*, no **⛔ khong co cho de ton tai**.

⚠ Va mot cong hai chieu di kem *(`kiem_bang_tep`)*: ⛔ khong tep nao tren dia ma
thieu trong bang, ⛔ khong dong nao trong bang ma thieu tep. Mot tep nam trong
`tep/` ma ⛔ khong ai khai la mot tep se duoc phuc vu **trong im lang** — hay
tuong hon, mot tep **⛔ khong bao gio** duoc phuc vu ma khong ai biet.

★ ⛔ **Tang nay ⛔ khong doc kho, ⛔ khong biet the la gi.** Cai the do
`tools/chay_cua.py` **dua vao** *(`phien`)* — cung khuon "ket noi duoc truyen
vao" cua `P4`. Nho vay `fls.web` ⛔ khong co duong nao tu dong mot the.
"""
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Callable

THU_MUC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tep")

# Ban TRANG. ⛔ Them mot duoi o day la mo them mot loai noi dung ra trinh duyet.
# ⛔ Khong co `.svg` (no chay duoc script), ⛔ khong co `.map` (no lo ma nguon).
KIEU: dict[str, str] = {
    ".html": "text/html; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
}


@dataclass(frozen=True)
class Tep:
    duong: str
    ten: str
    # `True` ⇒ sinh trong bo nho luc chay, ⛔ khong doc tu dia. Dung cho ĐUNG
    # MOT thu: `phien.js` — no cho cai the, va mot cai the ⛔ khong duoc nam
    # tren dia (no se bi commit, bi sao luu, bi gui qua Zalo).
    sinh: bool = False
    mo_ta: str = ""

    @property
    def kieu(self) -> str:
        duoi = os.path.splitext(self.ten)[1]
        return KIEU[duoi]


BANG_TEP: tuple[Tep, ...] = (
    Tep("/", "index.html", mo_ta="vo man hinh (shell) — top bar + control bar"),
    Tep("/index.html", "index.html", mo_ta="cung tep, duong day du"),
    Tep("/tokens.css", "tokens.css",
        mo_ta="⭐ TOKEN lay tu A-CCR. ⛔ Day la cho DUY NHAT co ma mau"),
    Tep("/hinh.css", "hinh.css",
        mo_ta="hinh dang: shell · the · chip · nut · luoi · 4 trang thai"),
    Tep("/goi_cua.js", "goi_cua.js",
        mo_ta="⭐ CHO DUY NHAT goi cua API. ⛔ Khong `fetch` rai rac"),
    Tep("/thanh_phan.js", "thanh_phan.js",
        mo_ta="chip niem tin · chip trang thai · so ke toan"),
    Tep("/trang_thai.js", "trang_thai.js",
        mo_ta="⭐ KHUON 4 trang thai dung chung (mac dinh·rong·dang tai·loi)"),
    Tep("/man_f03.js", "man_f03.js",
        mo_ta="man F03 — goi MOT cua that (`GET /gates`), cong ra cua B2"),
    Tep("/hop_thoai.js", "hop_thoai.js",
        mo_ta="hop xac nhan + drawer — dung chung F01/F02"),
    Tep("/man_f01.js", "man_f01.js",
        mo_ta="man F01 hang cho — 5 hanh dong moi dong (B4)"),
    # ⭐⭐⭐ `GAP-SCR-14` — lan LENH CHI cua man hang cho. ⛔ Phai KHAI
    #    o day: ban khai la ban TRANG hai chieu, nen mot tep tren dia
    #    ⛔ chua khai se **⛔ khong duoc phuc vu**, va man hinh se
    #    ⛔ khong bao loi — no chi **thieu mot lan**.
    Tep("/man_f01_lenh.js", "man_f01_lenh.js",
        mo_ta="man F01 · lan LENH CHI: dong lenh ⛔ chua tim duoc tien (QĐ-ITL-122)"),
    # ⭐⭐⭐ `QĐ-ITL-148` · chang `B3` — man GAN LENH CHI theo HOP DONG THIET KE
    #    (`Artifacts/Thiet-ke-Man-Gan-Lenh-Chi.md` + `BA-06 §4.5`/`§4.6`).
    # ⛔ Co cong RIENG canh do bam sat: `tests/web/test_b3_fe_bam_thiet_ke.py`
    #   — vi mot loi nhac ⛔ khong giu duoc gi (do: `339 → 735` dong qua 7 lan
    #   sua, ⛔ khong lan nao tong di xuong).
    Tep("/man_f01_ghep.js", "man_f01_ghep.js",
        mo_ta="man F01 · GAN LENH CHI ↔ GIAO DICH — 4 chip (dich cuoi TACH "
              "rieng, INV-I20) · 4 bac ①②③④ · Enter KHOA o ca lech tien · "
              "dien giai la cot ⛔ KHONG BAO GIO bi hy sinh"),
    Tep("/man_f02.js", "man_f02.js",
        mo_ta="man F02 so ITL — luoi 8 hanh vi + drawer doi soat (B5)"),
    # ⭐⭐⭐ `P7` task `6` — man NAP SAO KE.
    #
    # ⛔⛔ Man nay ⛔ **KHONG PHAI MAN DAN** (`QĐ-ITL-109`): FLS doc **vung
    # CHUAN** cua sheet `R |`, cu chi `Ctrl+V` **o lai Google Sheets**, va man
    # ⛔ khong co mot o nhap nao cho du lieu giao dich. Ly do duoc ky thanh
    # quyet dinh: **23/60** nguon **DOI DAU** khi chuan hoa, cho 60 phep bien
    # doi ay sang FLS la mo mot cho de **SAI DAU TIEN**.
    Tep("/man_f04.js", "man_f04.js",
        mo_ta="man F04 nap sao ke — 5 trang thai, bien ban 9 luat, "
              "`CHAN` thi nut Nhan TAT (task `6`)"),
    Tep("/ung_dung.js", "ung_dung.js", mo_ta="khoi dong vo + chon man"),
    Tep("/danh_muc.js", "danh_muc.js", sinh=True,
        mo_ta="⛔ SINH LUC KHOI DONG tu `fls_mapping_master`: danh muc "
              "ma hop dong cho o go `hd`. ⚠ ANH CHUP — Master doi thi "
              "phai khoi dong lai cua"),
    Tep("/phien.js", "phien.js", sinh=True,
        mo_ta="⛔ SINH TRONG BO NHO: cho the + ten nguoi dang lam. "
              "⛔ Khong bao gio nam tren dia"),
    # ⭐ `B5` — bang cot cua luoi, SINH tu `fls/api/cot_so.py`.
    #
    # ⛔⛔ **Vi sao no la tep SINH chu ⛔ khong phai tep tren dia.** Tieu de cot
    # phai den tu `oracle/ledge_spec` + `canon/spec` — **mot nguon duy nhat**
    # (`DEV-12 · B5`). Mot ban chep tren dia la **ban chep thu hai**: mot ngay
    # so doi ten cot ma ban chep ⛔ khong doi, man hinh hien ten cu, ke toan
    # doi chieu voi so mang ten moi — va lech ay ⛔ khong bao gio no ra. Sinh
    # luc chay ⇒ ⛔ khong co cho de lech.
    Tep("/cot.js", "cot.js", sinh=True,
        mo_ta="⭐ SINH: 23 tieu de luoi + 38 vi tri canon cho drawer. "
              "⛔ Khong mot ten cot nao go tay"),
)

# ⭐ Tep SINH ma than do **nguoi goi dua vao** — ⛔ khong phai `phien.js` *(cai
# the do `_than_phien` dung tai cho, va no ⛔ khong duoc di qua tay ai)*.
#
# ⚠ Ban TRANG hai chieu: mot tep sinh nam ngoai tap nay ma cung ⛔ khong phai
# `phien.js` se lam `lam_nguoi_phuc_vu` NO — vi no se duoc phuc vu **RONG**, va
# mot luoi ⛔ khong co tieu de trong nhu mot luoi **chua tai xong**.
SINH_TU_NGOAI: frozenset[str] = frozenset({"cot.js", "danh_muc.js"})

# Nhung tep tren dia ma bang KHONG phai khai (khong phuc vu ra ngoai).
# ⛔ Ban TRANG, va hom nay no RONG — moi tep trong `tep/` deu duoc phuc vu.
KHONG_PHUC_VU: frozenset[str] = frozenset()


def kiem_bang_tep(bang: tuple[Tep, ...] | None = None,
                  thu_muc: str = THU_MUC) -> list[str]:
    """⛔ Cong. Rong = dat. ⛔ Khong bao gio tra "OK" — tra danh sach vi pham.

    ⚠⚠ `bang=None` ⇒ doc `BANG_TEP` **luc goi**, ⛔ khong phai luc dinh nghia.
    Ban dau toi viet `bang: tuple = BANG_TEP` cho gon — va bai
    `test_lam_nguoi_phuc_vu_NO_khi_bang_hong` **do**: Python gan mac dinh MOT
    LAN luc nap module, nen cong van soi cai bang **cu** trong khi may phuc vu
    da doi sang bang moi. ⇒ Mot cai cong soi **ban chup cu** la mot cai cong
    xanh trong khi thuc te da hong — dung lop loi ca du an nay dung ra de chan.
    """
    if bang is None:
        bang = BANG_TEP
    loi: list[str] = []

    thay: set[str] = set()
    for t in bang:
        if t.duong in thay:
            loi.append(f"trung duong: {t.duong}")
        thay.add(t.duong)
        if not t.duong.startswith("/"):
            loi.append(f"{t.duong!r} khong bat dau bang `/`")
        # ⛔ Duong tep ⛔ KHONG duoc dam vao vung cua. Neu mot ngay nao do ai do
        # khai `/api/fls/v1/gates` o day thi man hinh se doc mot tep tinh thay
        # vi hoi kho — va no se **trong nhu that**.
        if t.duong.startswith("/api/"):
            loi.append(f"{t.duong} dam vao vung cua API — mot tep tinh nam duoi "
                       f"`/api/` se gia lam mot cau tra loi that")
        duoi = os.path.splitext(t.ten)[1]
        if duoi not in KIEU:
            loi.append(f"{t.ten} duoi {duoi!r} chua khai trong KIEU")
        if not t.mo_ta:
            loi.append(f"{t.duong} khong co mo ta — mot tep khong noi no la gi "
                       f"la mot tep khong ai biet co bo di duoc khong")
        if not t.sinh:
            d = os.path.join(thu_muc, t.ten)
            if not os.path.isfile(d):
                loi.append(f"{t.duong} tro toi {t.ten} — ⛔ khong co tep do")

    # ⛔⛔ Chieu nguoc: tep nam tren dia ma ⛔ khong ai khai.
    khai = {t.ten for t in bang if not t.sinh} | KHONG_PHUC_VU
    if os.path.isdir(thu_muc):
        for ten in sorted(os.listdir(thu_muc)):
            if not os.path.isfile(os.path.join(thu_muc, ten)):
                loi.append(f"`tep/` chua thu muc con {ten!r} — bang tep phang, "
                           f"⛔ khong di sau")
                continue
            if ten not in khai:
                loi.append(f"tep {ten!r} nam trong `tep/` ma ⛔ khong ai khai "
                           f"trong BANG_TEP — no se ⛔ khong bao gio duoc phuc "
                           f"vu, va ⛔ khong ai biet dieu do")
    else:
        loi.append(f"⛔ khong co thu muc {thu_muc}")
    return loi


def _than_phien(phien: dict) -> bytes:
    """`phien.js` — ⭐ **cho** cua cai the, ⛔ khong phai noi phat the.

    Nap bang `<script src>` nen ⛔ khong co chuyen `</script>` cat ngang; van
    di qua `json.dumps` de mot dau nhay trong ten nguoi ⛔ khong lam vo tep.
    """
    return ("// ⛔ SINH TRONG BO NHO luc chay — ⛔ khong co tep nay tren dia.\n"
            "window.FLS_PHIEN = "
            + json.dumps(phien, ensure_ascii=False) + ";\n").encode("utf-8")


def lam_nguoi_phuc_vu(
    phien: dict | None = None,
    than_sinh: dict[str, bytes] | None = None,
) -> Callable[[str], tuple[str, bytes] | None]:
    """Tra ve mot ham: `duong` → `(kieu_noi_dung, than)`, hay `None` = ⛔ khong co.

    ⛔ NO ngay luc dung neu bang tep vi pham — cung khuon `dung_may` cua `P4`:
    mot cai cong chi kiem luc cai dat la mot cai cong chay duoc voi bang hong.

    ★ `than_sinh` = `{ten_tep: than}` cho cac tep trong `SINH_TU_NGOAI`. ⭐ Do
    la cach `fls.web` co duoc bang cot **ma van ⛔ khong import mot dong nao
    cua `fls`** — cung khuon "ket noi duoc truyen vao" cua `P4`. Neu tang nay
    tu `import fls.api.cot_so` thi no da biet tang duoi, va luat thu tam cua
    `import-linter` mat nua y nghia.
    """
    loi = kiem_bang_tep()
    if loi:
        raise RuntimeError("⛔ bang tep vi pham:\n  - " + "\n  - ".join(loi))

    # ⛔⛔ Doi chieu HAI CHIEU, va no truoc khi may chay.
    #
    # ⚠ Chieu *thieu* la chieu nguy hiem: mot tep sinh khong co than se duoc
    # phuc vu **RONG** — trinh duyet nhan `200 OK`, `Content-Type` dung, than
    # `0` byte. Man hinh khi do ⛔ khong bao loi, no chi ⛔ khong co tieu de cot;
    # va mot luoi khong tieu de trong y het mot luoi **chua tai xong**.
    ngoai = dict(than_sinh or {})
    can = SINH_TU_NGOAI
    thieu = sorted(can - set(ngoai))
    if thieu:
        raise RuntimeError(
            f"⛔ tep SINH thieu than: {thieu} — chung se duoc phuc vu RONG, va "
            f"mot tep rong tra `200 OK` trong y het mot tep chua tai xong")
    thua = sorted(set(ngoai) - can)
    if thua:
        raise RuntimeError(
            f"⛔ dua than cho tep ⛔ khong khai trong `SINH_TU_NGOAI`: {thua} — "
            f"than nay se ⛔ khong bao gio den duoc trinh duyet")

    p = dict(phien or {})
    tra: dict[str, Tep] = {t.duong: t for t in BANG_TEP}

    def phuc_vu(duong: str) -> tuple[str, bytes] | None:
        # ⭐⭐ Duong den la mot KHOA TRA BANG. ⛔ Khong mot phep ghep duong nao
        #    voi chuoi cua nguoi goi ⇒ `../` ⛔ khong co cho de ton tai.
        t = tra.get(duong)
        if t is None:
            return None
        if t.sinh:
            # `phien.js` dung tai cho (cai the ⛔ khong di qua tay ai); cac tep
            # sinh khac lay than tu `than_sinh`.
            if t.ten in ngoai:
                return t.kieu, ngoai[t.ten]
            return t.kieu, _than_phien(p)
        # `t.ten` den TU BANG, ⛔ khong tu nguoi goi.
        with open(os.path.join(THU_MUC, t.ten), "rb") as f:
            return t.kieu, f.read()

    return phuc_vu
