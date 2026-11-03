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
BANG_CO_VET: frozenset[str] = frozenset({"fls_journal", "fls_queue_event"})

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
    ghi: bool = False
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
          ("fls_journal", "fls_itl"),
          mo_ta="nhat ky 7 truong cua mot dong (?itl_id=)"),
    Tuyen("GET", f"{TIEN_TO}/gates", "cong",
          # ⚠⚠ Ban khai cu vua THIEU vua THUA: no ghi `fls_pm_link` +
          # `fls_reject` *(SQL ⛔ khong cham)* va bo sot `fls_moi_noi` *(SQL CO
          # cham — phep do Σ moi noi phai chay tren khung xem HIEU LUC, ⛔ khong
          # tren bang goc)*. Ca hai chieu deu la ban do ve sai.
          ("fls_itl", "fls_moi_noi", "fls_run"),
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
           "fls_queue_event", "fls_adjustment", "fls_journal", "fls_sua_tay"),
          bang_ghi=("fls_pm_link", "fls_queue_event", "fls_adjustment",
                    "fls_journal"),
          ghi=True, ghi_nhat_ky=True,
          mo_ta="ghep tay: Σ dong lenh PHAI bang tien bank (dung sai theo tien "
                "te) ⇒ lech thi 422 va GIU UNMAPPED, ⛔ khong chia bua"),

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
           "fls_sua_tay"),
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
        if SO in t.bang_ghi:
            loi.append(f"{t.phuong_thuc} {t.duong} khai GHI vao {SO} — "
                       f"`INV-I08`: so la append-only, sua chi bang but toan "
                       f"moi trong `fls_adjustment`")
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
