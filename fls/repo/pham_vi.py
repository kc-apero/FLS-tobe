"""PHAM VI doc: dong nao cua kho duoc phep ra man hinh.

⛔⛔ **Vi sao cai nay ra doi TRUOC cua doc, khong phai sau.** Ngay 27/08 dem ra
`fls_itl` co **1.204 dong dau test** lan vao so that, trong do **194 dong ngay
trong hang cho** — tuc la danh sach viec phai lam cua ke toan. Kho da dung lai
sach, nhung cho hong that su la: **khong gi bat buoc phai loc**. Neu cua doc
(`P4`) mo ra ma khong mang pham vi, thi lan sau co dau test la no len man hinh.

⇒ Luat o day: **moi cau doc PHAI nhan mot `PhamVi`**, va `PhamVi` ⛔ **khong co
mac dinh**. Khong ai "quen truyen" duoc — thieu doi so la NO ngay luc goi.

★ Ba pham vi, va CHI ba:

    chi_nap_that()      — ban TRANG: chi `run_id` khop `NAP-yyyy-mm-dd-NGUON`
    mot_lan_nap(run)    — mot lan nap CU THE, **van phai qua ban trang**
    ca_kho(ly_do=...)   — ⛔ ca kho, KE CA dau test. Bat buoc viet LY DO,
                          va co test quet ma nguon: `fls/api/**` ⛔ khong duoc
                          nhac ten ham nay o bat ky dau

⚠ `mot_lan_nap` **giao** voi ban trang chu khong thay the no: neu ai truyen vao
mot `run_id` cua test thi cau doc tra **rong**, ⛔ khong tra dong test ra.

★ Mot nguon su that cho hai bo may. Hinh dang `run_id` khai o
`fls.repo.kho_sach.HINH_RUN_THAT` (Python) va cau SQL o day dung **cung chuoi
mau do** cho toan tu `~` cua PostgreSQL. Hai bo may regex khac nhau ⇒ co the
lech ⇒ co bai `test_hai_bo_may_regex_hieu_GIONG_nhau` doi chieu tung mau.
"""
from __future__ import annotations

from dataclasses import dataclass

from fls.repo.kho_sach import HINH_RUN_THAT

# Ba kieu, va chi ba. Them kieu thu tu phai sua o day roi `__post_init__` no.
KIEU: frozenset[str] = frozenset({"nap_that", "mot_lan_nap", "ca_kho"})


@dataclass(frozen=True)
class PhamVi:
    """⛔ Dung `PhamVi(...)` truc tiep cung duoc, nhung khong co mac dinh nao."""

    kieu: str
    run_id: str | None = None
    ly_do: str = ""

    def __post_init__(self) -> None:
        if self.kieu not in KIEU:
            raise ValueError(f"pham vi khong biet: {self.kieu!r} — chi co {sorted(KIEU)}")
        if self.kieu == "mot_lan_nap" and not self.run_id:
            raise ValueError("pham vi 'mot_lan_nap' phai co run_id")
        if self.kieu != "mot_lan_nap" and self.run_id:
            raise ValueError(f"pham vi {self.kieu!r} ⛔ khong nhan run_id")
        if self.kieu == "ca_kho" and not self.ly_do.strip():
            raise ValueError(
                "⛔ pham vi 'ca_kho' doc CA dau test ra — phai viet LY DO. "
                "Neu dang lam cua doc/man hinh thi day la pham vi SAI: dung "
                "chi_nap_that()")

    def dieu_kien(self, cot: str = "run_id") -> tuple[str, list[object]]:
        """Tra (menh de SQL, tham so). ⛔ Khong noi chuoi gia tri vao SQL.

        `cot` la ten cot `run_id` da co bi danh, vd `i.run_id`.
        """
        if self.kieu == "ca_kho":
            return "TRUE", []
        ban_trang = f"{cot} ~ %s"
        if self.kieu == "nap_that":
            return ban_trang, [HINH_RUN_THAT.pattern]
        # mot_lan_nap: giao voi ban trang, ⛔ khong thay the no
        return f"({ban_trang} AND {cot} = %s)", [HINH_RUN_THAT.pattern, self.run_id]

    def mo_ta(self) -> str:
        if self.kieu == "nap_that":
            return "chi lan nap that"
        if self.kieu == "mot_lan_nap":
            return f"lan nap {self.run_id}"
        return f"ca kho (ly do: {self.ly_do})"


def chi_nap_that() -> PhamVi:
    """Ban TRANG — pham vi cua moi man hinh va moi cua doc."""
    return PhamVi(kieu="nap_that")


def mot_lan_nap(run_id: str) -> PhamVi:
    return PhamVi(kieu="mot_lan_nap", run_id=run_id)


def ca_kho(ly_do: str) -> PhamVi:
    """⛔⛔ Doc CA dau test. Chi cho cong cu soi kho va bo test.

    Co bai quet ma nguon chan ten ham nay xuat hien trong `fls/api/**`.
    """
    return PhamVi(kieu="ca_kho", ly_do=ly_do)
