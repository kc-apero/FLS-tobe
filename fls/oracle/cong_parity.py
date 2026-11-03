"""Phan xu mot luot parity — va cai chan "khong do gi ma bao XANH".

★ Vi sao module nay ton tai. Ban dau logic phan xu nam ngay trong script
`tools/verify_parity_all.py`. Lan chay dau tien: ca 3 lat doc deu truot (503/500),
doc duoc **0 dong**, so sanh **0 o** — va script in *"0 o lech, luat Final tai
hien DUNG 100% tung o"* roi tra ve **PASS**.

Do dung la loi im lang ma ca he nay dung de chan: `row_counts` tu khop, tong tu
khop, khong ai thay gi. Nen phan xu duoc doi ra day, thanh ham thuan CO TEST —
trong do co test "0 o thi phai FAIL".

Ba dieu kien, ⛔ thieu MOT la khong duoc noi "parity 100%":
  ① co so lieu thuc su          (do it nhat `toi_thieu_o` o)
  ② khong lat nao bi bo lai      (lo trong so = khong the noi "ca so")
  ③ khong o nao lech
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PhanXu:
    dat: bool
    ly_do: tuple[str, ...] = field(default_factory=tuple)

    @property
    def mot_dong(self) -> str:
        return "DAT" if self.dat else "KHONG DAT: " + " · ".join(self.ly_do)


def danh_gia(tong_o: int, khop: int, lat_truot: int, dong_doc: int,
             dong_mong_doi: int, toi_thieu_o: int = 1000,
             sai_so_dong: float = 0.02) -> PhanXu:
    """⛔ Mac dinh la KHONG DAT. Chi "dat" khi chung minh duoc ca ba dieu.

    `dong_mong_doi` la so dong da do doc lap truoc do — khai bao ra de mot luot
    doc hut mot nua so khong the di qua trong im lang.
    """
    ly: list[str] = []
    if lat_truot:
        ly.append(f"{lat_truot} lat doc bi bo lai => co lo trong, "
                  f"khong the ket luan cho CA SO")
    if tong_o < toi_thieu_o:
        ly.append(f"chi so duoc {tong_o} o (nguong {toi_thieu_o}) => "
                  f"khong do duoc gi thi khong duoc bao XANH")
    if dong_mong_doi > 0:
        lech = abs(dong_doc - dong_mong_doi) / dong_mong_doi
        if lech > sai_so_dong:
            ly.append(f"doc {dong_doc} dong nhung mong doi ~{dong_mong_doi} "
                      f"(lech {lech:.1%} > {sai_so_dong:.0%})")
    if tong_o and khop != tong_o:
        ly.append(f"{tong_o - khop}/{tong_o} o LECH")
    return PhanXu(not ly, tuple(ly))
