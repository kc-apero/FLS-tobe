"""`D3` — CO CHE GHI AN TOAN len mot trang tinh **dang song**.

⛔⛔ **Bon dieu module nay lam, va moi dieu deu la mot lo da co that:**

  ⓐ ⛔ **KHONG dia chi tuyet doi.** Mot o dich duoc khai bang
    `(tab, cot khoa, gia tri khoa, ten cot)` — ⛔ **khong** bang `'H1310'`.
    ⚠ Lo: chu so dang **cung mo tep** va mot cu chen dong lam moi dia chi
    duoi no **dich mot dong**. Ghi theo `A1` cung thi cu ghi roi **dung o
    khac** — va no ⛔ khong bao loi, no chi **ghi sai cho**. Bai hoc nay da
    duoc ghi mot lan roi *(`live-sheet-absolute-range-hazard`)*, va day la
    lan dau no thanh **mot cau truc** chu ⛔ khong con la mot loi nhac.

  ⓑ ⭐⭐ **Ghi hai lan ⇒ ⛔ KHONG nhan doi.** Phep so sanh la voi **gia tri
    dang co tren ban SONG**, ⛔ khong voi mot cai the "da ghi" nao. Nen neu
    o dich **da dung roi** thi quyet dinh la `DA_DUNG_ROI` va ⛔ khong cu ghi
    nao duoc gui. ⇒ Chay lai lan hai: **0 o duoc ghi**.
    ⛔ Mot cai the trong kho **⛔ khong lam duoc viec nay**: the noi *"toi da
    ghi"*, con cau hoi that la *"o kia dang la gi"*.

  ⓒ **Bien ban chay kho neu O DICH THAT.** Moi dong bien ban mang dia chi
    `A1` **da giai ra tu ban song**, gia tri dang co, gia tri moi, va mot
    **quyet dinh co ten**. ⛔ Mot bien ban noi *"se ghi 12 o"* ma ⛔ khong noi
    **o nao** la mot bien ban ⛔ khong ai duyet duoc.

  ⓓ ⛔⛔ **Cu ghi ⛔ KHONG CHAY khi co duyet tat.** `ap_dung` doi
    `duyet=True` **tuong minh**; thieu la **NO**, ⛔ khong am tham bo qua.
    Va bo van chuyen (`ghi`) duoc **TIEM VAO** — nen ban than module nay
    ⛔ **khong co duong nao** goi ra mang.

★ Va mot luat thu nam, cung khuon voi moi cua LO khac cua he: **co mot dong
  bi TU CHOI ⇒ TU CHOI CA LO**, ⛔ 0 o duoc ghi. Ghi nua vo len so cua nguoi
  khac la trang thai ⛔ khong ai doc duoc.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Sequence

# ── quyet dinh, va CHI ba ────────────────────────────────────────────────
SE_GHI = "se_ghi"
DA_DUNG_ROI = "da_dung_roi"
TU_CHOI = "tu_choi"

# ⭐ Ten ly do TU CHOI — ⛔ khong ly do nao ten "khac". Moi ten dan tay nguoi
#   doc di mot duong sua khac nhau, nen gop chung lai la bo di dung phan tin
#   nguoi ay can.
LY_DO_TU_CHOI: dict[str, str] = {
    "tab_khong_co":
        "ban song ⛔ khong co tab ay ⇒ hoac ai da doi ten tab, hoac ta dang "
        "nham tep",
    "cot_khoa_khong_co":
        "hang tieu de ⛔ khong co cot khoa ⇒ ⛔ khong neo vao dau duoc",
    "cot_dich_khong_co":
        "hang tieu de ⛔ khong co cot dich ⇒ ai da doi ten cot, hay ta dang "
        "khai mot ten cu",
    "khoa_khong_co":
        "⛔ khong dong nao mang khoa ay ⇒ dong da bi xoa, hay khoa sai",
    "khoa_TRUNG":
        "≥2 dong mang cung khoa ay ⇒ may phai **chon mot dong**, va no "
        "⛔ khong duoc chon ho ai",
    "hai_but_toan_mot_O":
        "hai o dich khac nhau giai ra CUNG mot dia chi ⇒ cu ghi sau se dap "
        "len cu truoc trong im lang",
}


@dataclass(frozen=True)
class KhungTab:
    """Hinh cua mot tab: hang TIEU DE o dau, va du lieu bat dau tu dau.

    ⚠ Ca hai la so **1-based** *(nhu Sheets hien)*, ⛔ khong 0-based: mot bien
    ban nham he dem la mot bien ban chi sai o **mot dong**, va do la sai lam
    **de nhat de khong ai thay** trong ca thiet ke nay.
    """

    tab: str
    dong_tieu_de: int = 1
    dong_dau: int = 2

    def __post_init__(self) -> None:
        if self.dong_tieu_de < 1 or self.dong_dau < 1:
            raise ValueError("hang tieu de / dong dau la 1-based, phai >= 1")
        if self.dong_dau <= self.dong_tieu_de:
            raise ValueError(
                f"dong dau ({self.dong_dau}) phai SAU hang tieu de "
                f"({self.dong_tieu_de}) — ⛔ khong doc tieu de thanh du lieu")


@dataclass(frozen=True)
class Neo:
    """Mot o dich, neo theo **KHOA DONG + TEN COT**. ⛔ Khong dia chi `A1`."""

    tab: str
    cot_khoa: str
    khoa: str
    cot: str

    def __post_init__(self) -> None:
        for ten, v in (("tab", self.tab), ("cot_khoa", self.cot_khoa),
                       ("khoa", self.khoa), ("cot", self.cot)):
            if not str(v).strip():
                raise ValueError(f"neo thieu `{ten}` — mot neo rong ⛔ khong "
                                 f"giai ra o nao")


@dataclass(frozen=True)
class MotO:
    neo: Neo
    gia_tri_moi: str


@dataclass(frozen=True)
class DongBienBan:
    neo: Neo
    gia_tri_moi: str
    quyet_dinh: str
    o_a1: str | None = None            # `None` = ⛔ chua giai ra duoc
    gia_tri_dang_co: str | None = None
    ly_do: str = ""


@dataclass(frozen=True)
class BienBan:
    dong: tuple[DongBienBan, ...]

    @property
    def se_ghi(self) -> tuple[DongBienBan, ...]:
        return tuple(d for d in self.dong if d.quyet_dinh == SE_GHI)

    @property
    def tu_choi(self) -> tuple[DongBienBan, ...]:
        return tuple(d for d in self.dong if d.quyet_dinh == TU_CHOI)

    @property
    def da_dung_roi(self) -> tuple[DongBienBan, ...]:
        return tuple(d for d in self.dong if d.quyet_dinh == DA_DUNG_ROI)

    def tom(self) -> dict[str, int]:
        return {"tong": len(self.dong), "se_ghi": len(self.se_ghi),
                "da_dung_roi": len(self.da_dung_roi),
                "tu_choi": len(self.tu_choi)}


class ChuaDuyet(Exception):
    """Cu ghi bi chan vi ⛔ chua duyet. ⛔ Khong phai mot canh bao."""


class CoDongTuChoi(Exception):
    """Bien ban co dong TU CHOI ⇒ ⛔ khong ghi mot o nao."""


def chu_cot(so_0: int) -> str:
    """`0 → 'A'` · `25 → 'Z'` · `26 → 'AA'` · `63 → 'BL'`.

    ⚠ Nhan chi so **0-based** *(vi tri trong danh sach Python)* va tra chu cai
    cua Sheets. Hai he dem gap nhau **dung o day va chi o day** — nen phep
    doi nam trong mot ham co ten, ⛔ khong rai trong bon cho.
    """
    if so_0 < 0:
        raise ValueError(f"chi so cot phai >= 0, nhan {so_0}")
    s = ""
    n = so_0 + 1
    while n:
        n, du = divmod(n - 1, 26)
        s = chr(ord("A") + du) + s
    return s


def _chuoi(v: Any) -> str:
    """Mot o cua Sheets → chuoi de **so sanh**. ⛔ Khong doan kieu.

    ⚠ `None` va `''` la **cung mot thu** o day *(o trong)*, va mot con so
    ⛔ khong duoc so bang `float`: `1000` va `1000.0` la hai chuoi khac nhau
    tren mot o van ban, va doan kieu o day se lam phep so sanh **im lang sai**
    theo ca hai chieu.
    """
    return "" if v is None else str(v).strip()


def lap_bien_ban(luoi: dict[str, Sequence[Sequence[Any]]],
                 khung: dict[str, KhungTab],
                 ds: Sequence[MotO]) -> BienBan:
    """Giai tung neo tren **BAN SONG** roi lap bien ban. ⛔ Khong ghi gi.

    `luoi` = `{tab: cac hang}` **vua doc**, tinh tu **hang 1** cua tab.
    `khung` = `{tab: KhungTab}`.

    ⛔⛔ **Phai doc ban song TRUOC khi lap bien ban** — day la ca diem cua `D3`.
    Mot bien ban lap tu mot anh chup cu se noi dung o `H1310` trong khi ban
    song da dich xuong `H1311`.
    """
    ra: list[DongBienBan] = []
    # `a1 -> chi so dong bien ban` — de bat hai but toan cung mot o
    da_nham: dict[str, int] = {}
    xung_dot: set[str] = set()

    for m in ds:
        n = m.neo
        k = khung.get(n.tab)
        hang = luoi.get(n.tab)
        if k is None or hang is None:
            ra.append(DongBienBan(n, m.gia_tri_moi, TU_CHOI,
                                  ly_do="tab_khong_co"))
            continue
        i_td = k.dong_tieu_de - 1
        if i_td >= len(hang):
            ra.append(DongBienBan(n, m.gia_tri_moi, TU_CHOI,
                                  ly_do="tab_khong_co"))
            continue
        tieu_de = [_chuoi(x) for x in hang[i_td]]
        if n.cot_khoa not in tieu_de:
            ra.append(DongBienBan(n, m.gia_tri_moi, TU_CHOI,
                                  ly_do="cot_khoa_khong_co"))
            continue
        if n.cot not in tieu_de:
            ra.append(DongBienBan(n, m.gia_tri_moi, TU_CHOI,
                                  ly_do="cot_dich_khong_co"))
            continue
        i_khoa = tieu_de.index(n.cot_khoa)
        i_cot = tieu_de.index(n.cot)

        # ⚠ Quet **moi** dong du lieu roi dem — ⛔ khong dung lai o dong dau
        #   khop. Dung lai som thi khoa TRUNG se **im lang** di qua, va cu ghi
        #   se roi vao dong dau tien tinh co xep truoc.
        khop = [d for d in range(k.dong_dau - 1, len(hang))
                if i_khoa < len(hang[d])
                and _chuoi(hang[d][i_khoa]) == n.khoa]
        if not khop:
            ra.append(DongBienBan(n, m.gia_tri_moi, TU_CHOI,
                                  ly_do="khoa_khong_co"))
            continue
        if len(khop) > 1:
            ra.append(DongBienBan(n, m.gia_tri_moi, TU_CHOI,
                                  ly_do="khoa_TRUNG"))
            continue

        d = khop[0]
        a1 = f"{chu_cot(i_cot)}{d + 1}"
        dang_co = _chuoi(hang[d][i_cot]) if i_cot < len(hang[d]) else ""
        moi = _chuoi(m.gia_tri_moi)

        if a1 in da_nham:
            xung_dot.add(a1)
        da_nham[a1] = len(ra)

        ra.append(DongBienBan(
            n, m.gia_tri_moi,
            DA_DUNG_ROI if dang_co == moi else SE_GHI,
            o_a1=a1, gia_tri_dang_co=dang_co))

    # ⛔⛔ Hai but toan cung mot O: **CA HAI** bi tu choi, ⛔ khong phai *"lay
    # cai sau"*. Lay cai sau la mot phep chon ma ⛔ khong ai khai, va no dap
    # len ket luan cua nguoi kia trong im lang.
    if xung_dot:
        ra = [DongBienBan(x.neo, x.gia_tri_moi, TU_CHOI, o_a1=x.o_a1,
                          gia_tri_dang_co=x.gia_tri_dang_co,
                          ly_do="hai_but_toan_mot_O")
              if x.o_a1 in xung_dot else x
              for x in ra]
    return BienBan(tuple(ra))


def ap_dung(bb: BienBan, ghi: Callable[[str, str, str], Any], *,
            duyet: bool = False) -> dict[str, Any]:
    """Gui **chi** cac o `SE_GHI`. ⛔ Thieu `duyet=True` la **NO**.

    `ghi(tab, o_a1, gia_tri)` la bo van chuyen **duoc tiem vao** — module nay
    ⛔ **khong co duong nao** tu goi ra mang.

    ⛔⛔ Hai cong, theo dung thu tu nay:
      ⓐ `duyet` tat  ⇒ `ChuaDuyet`  *(⛔ 0 o duoc ghi)*
      ⓑ co dong `TU_CHOI` ⇒ `CoDongTuChoi` *(⛔ 0 o duoc ghi — CA LO)*

    ⚠ Thu tu ay **co y**: kiem `duyet` **TRUOC**. Neu kiem bien ban truoc thi
      mot lan chay thu voi co tat se bao *"co 3 dong tu choi"* va nguoi ta di
      sua ba dong do, roi bam lai — trong khi cai chan that su la **co duyet**.
    """
    if duyet is not True:
        raise ChuaDuyet(
            "⛔ cu ghi BI CHAN: `duyet` ⛔ chua bat. Bien ban chay kho van doc "
            f"duoc ({bb.tom()}), nhung ⛔ khong o nao duoc ghi. Bat `duyet` la "
            "quyet dinh cua CHU SO, ⛔ khong phai cua may")
    if bb.tu_choi:
        raise CoDongTuChoi(
            f"⛔ TU CHOI CA LO: {len(bb.tu_choi)} trong {len(bb.dong)} dong "
            f"⛔ khong giai ra o dich chac chan "
            f"({sorted({d.ly_do for d in bb.tu_choi})}) ⇒ ⛔ 0 o duoc ghi")

    da: list[dict[str, str]] = []
    for d in bb.se_ghi:
        ghi(d.neo.tab, d.o_a1 or "", _chuoi(d.gia_tri_moi))
        da.append({"tab": d.neo.tab, "o": d.o_a1 or "",
                   "truoc": d.gia_tri_dang_co or "",
                   "sau": _chuoi(d.gia_tri_moi)})
    return {"so_o_da_ghi": len(da), "o": da,
            # ⭐ Hai con so nay ra cung cho: mot bao cao noi *"da ghi 3 o"* ma
            #   ⛔ khong noi *"2 o da dung roi"* se lam nguoi doc tuong lo cua
            #   ho co 3 o.
            "so_o_da_dung_roi": len(bb.da_dung_roi),
            "tom": bb.tom()}


# ⭐⭐ Luat HAI KHOA — song o day, ⛔ khong trong cong cu.
#
# ⛔⛔ Vi sao: bo van chuyen that (`tools/ghi_o_that.py`) chi chay duoc khi co
# mang va co the Google, nen mot luat nam trong do la mot luat **⛔ khong bai
# nao do duoc**. Tach ra thanh ham thuan thi cai co quan trong nhat cua ca `D3`
# co bai kiem — ke ca truong hop `duyet=1` *(truthy ma ⛔ khong phai `True`)*.
BIEN_CHO_GHI = "FLS_CHO_GHI_SHEET"


def hai_khoa_mo(duyet: Any, bien: str | None) -> bool:
    """`True` chi khi **CA HAI** khoa mo: `duyet is True` va `bien == "1"`.

    ⚠ Mot co dong lenh la thu **go duoc trong ba giay**, va cai nay ghi vao
    **trang tinh cua ke toan dang mo** — ⛔ khong co "kho test" nao o day. Nen
    khoa thu hai nam **ngoai dong lenh**: mot cu dan lenh cu ⛔ khong mo duoc no.
    """
    return duyet is True and (bien or "").strip() == "1"


def van_bien_ban(bb: BienBan) -> list[str]:
    """Bien ban thanh **cac dong chu** — de dan vao mot bao cao cho NGUOI duyet.

    ⛔ Moi dong neu **O DICH THAT**; dong ⛔ khong giai ra duoc thi neu
    `⛔ khong giai ra o` kem **ten ly do**, ⛔ khong de trong.
    """
    v: list[str] = []
    for d in bb.dong:
        dau = {SE_GHI: "→ SE GHI ", DA_DUNG_ROI: "= DA DUNG ",
               TU_CHOI: "⛔ TU CHOI "}[d.quyet_dinh]
        cho = (f"{d.neo.tab}!{d.o_a1}" if d.o_a1
               else f"{d.neo.tab} ⛔ khong giai ra o")
        n = d.neo
        neo = f"[{n.cot_khoa}={n.khoa} · cot {n.cot!r}]"
        if d.quyet_dinh == TU_CHOI:
            v.append(f"{dau}{cho} {neo} — {d.ly_do}: "
                     f"{LY_DO_TU_CHOI.get(d.ly_do, '⛔ ly do ⛔ khong co ten')}")
        else:
            v.append(f"{dau}{cho} {neo} "
                     f"{d.gia_tri_dang_co!r} → {_chuoi(d.gia_tri_moi)!r}")
    t = bb.tom()
    v.append(f"── Σ {t['tong']} dong: {t['se_ghi']} se ghi · "
             f"{t['da_dung_roi']} da dung roi · {t['tu_choi']} TU CHOI")
    return v
