"""`CA.GL` thuần — dòng sổ cái → Nợ/Có tách theo 5 tiền tệ · tồn luỹ kế · bVND · mUSD.

ISP 3.1.2 **Step 1 · H1** *(`WO-070`)* · AP v3.1.2 §3.3.1 hàng PD `406 · 412` · §3.5.4 `WP-C2`.

── Công thức NOW, chép NGUYÊN VĂN *(AP §3.3.1, cột "PD NOW · script · công thức")* ──────────

    A10 = QUERY(ITL Ledge); tách Nợ/Có theo 5 tiền tệ; tồn = tồn trên + Nợ − Có;
    BO/BP = tỷ giá × E|F / 10^9 (bVND); BR/BS = BO|BP ÷ USD × 10^3 (mUSD);
    CA = VLOOKUP(TK, Mapping Master AB→AD)

    cột conflict cùng hàng: "tồn luỹ kế theo thứ tự dòng của cả bảng, ⛔ theo TK ⇒ phụ thuộc
    sort; tỷ giá theo tháng"
    hàng PD 405: "9.2.Exchange Rate = IMPORTRANGE APERO | FS2; tra bằng SUMIFS(tháng) và
    INDEX(MATCH tháng; MATCH tiền tệ)" — conflict: "bảng đứng yên từ 07/2025; tháng thiếu ⇒
    mất số"

Ánh xạ cột AS-IS → trường của `KetQuaDongGL` *(E|F = Nợ|Có nguyên tệ của dòng)*:

    BO = tỷ giá × E / 10^9   → bvnd_no        BR = BO ÷ USD × 10^3 → musd_no
    BP = tỷ giá × F / 10^9   → bvnd_co        BS = BP ÷ USD × 10^3 → musd_co

⭐ **Đơn vị** *(Đ4 — mỗi số nói nó đếm gì)*: `tỷ giá` = số VND cho MỘT đơn vị tiền tệ của dòng
*(`IX.FX`: VND = 1)* · **bVND** = tỷ VND *(÷ 10^9)* · **mUSD** = triệu USD *(tỷ VND ÷ VND/USD
= tỷ USD; × 10^3 = triệu USD)*. ⛔⛔ ISP `H1-B1` ghi mong *"mUSD 98,039…"* cho dòng VND
2.500.000.000 @ 25.500 — **sai đơn vị**: chính công thức trên cho `2,5 ÷ 25.500 × 10^3 =
0,098039…` mUSD; `98,039…` là cùng giá trị đo bằng **nghìn** USD *(orchestrator đính chính
16/11, `BG-071`)*. Mã theo CÔNG THỨC AP; bài `test_H1_B1_…` canh riêng đơn vị.

── Ba hành vi AS-IS được GIỮ có chủ ý *(parity trước — D2; H4 so với đáp án 406)* ───────────

① **Tồn luỹ kế theo THỨ TỰ dòng đưa vào, ⛔ theo TK.** *"tồn = tồn trên + Nợ − Có"* cộng dồn
  từ trên xuống cả bảng ⇒ đổi thứ tự dòng là đổi tồn giữa bảng *(tồn cuối thì ⛔ đổi)*. Đó là
  conflict AP đã ghi *("phụ thuộc sort")*; đích TO-BE *"tồn theo (TK, ngày)"* là việc SAU
  parity, ⛔ của H1. `DongGL` ⛔ mang TK ⇒ hàm này **⛔ thể** gộp theo TK, bằng cấu trúc.
  ⚠ Đọc công thức: tồn tính **theo từng tiền tệ, bằng nguyên tệ** — vì *"tồn = …"* đứng
  SAU *"tách Nợ/Có theo 5 tiền tệ"* và TRƯỚC bước quy đổi BO/BP, mà cộng 1 USD với 1 VND
  thành "2" thì vô nghĩa. Repo ⛔ chép ô nào của CALC ZONE `BM–BT` *(đáp án 406 đóng băng ở
  `DT4`)* ⇒ cách đọc này **chưa đối chiếu được với số thật** — H4 là phép đo quyết định
  *(câu hỏi đã nêu ở `BG-071`)*.
② **Tỷ giá theo THÁNG của dòng** *(`SUMIFS(tháng)`)* — `fx[thang][tien_te]`; mUSD chia cho
  tỷ giá USD **cùng tháng** ⇒ dòng VND cũng cần tỷ giá USD của tháng ấy.
③ **5 cột tiền tệ** `USD · SGD · COP · VND · HKD` — đúng thứ tự `IX.FX` *(AP §3.2.1: "tháng
  yyyymm × USD · SGD · COP · VND (=1) · HKD", 37 dòng 202401 → 202612 kể cả dòng lạc
  202306)*. `TIEN_TE_GL` là **khuôn cột của GL**, ⛔ phải luật số: ⛔ một tỷ giá nào gõ
  trong mã — kể cả VND = 1 — mọi tỷ giá đến từ tham số `fx` *(AP AC9: engine đọc config,
  ⛔ gõ lại)*.

── Hai chỗ **⛔ giữ** lỗi AS-IS — đây là lý do engine tồn tại ─────────────────────────────

ⓐ **Tháng thiếu tỷ giá ⇒ `ThieuTyGia`, ⛔ ra 0.** `SUMIFS` trên tháng vắng trả **0** ⇒
  bVND = mUSD = 0 **im lặng** — *"tháng thiếu ⇒ mất số"*, và bảng tỷ giá *"đứng yên từ
  07/2025"*. Tỷ giá `0` chính là dấu vết ấy ⇒ tỷ giá ≤ 0 cũng là THIẾU. Lỗi ném cho CẢ lượt
  *(⛔ trả nửa bảng)*: một GL có lỗ thủng mà vẫn in được thì ⛔ ai thấy lỗ *(`INV-I16`)*.
ⓑ **Tiền tệ ngoài 5 cột ⇒ `TienTeNgoaiGL`.** Dòng EUR ⛔ có cột để vào: bỏ qua là mất tiền
  khỏi GL, dồn vào cột khác là bịa — cả hai đều im lặng.

── Hàm THUẦN *(`.importlinter` hợp đồng 11 — cấm `psycopg` · `fls.repo` · `fls.db`)* ─────────

Dòng và tỷ giá được **TRUYỀN VÀO**; ⛔ đọc kho, ⛔ đọc biến môi trường. Cùng đầu vào ⇒ cùng
con số — kể cả khi người gọi đổi độ chính xác `Decimal` toàn cục: phép tính chạy trong ngữ
cảnh CỐ ĐỊNH `_NGU_CANH` *(28 chữ số có nghĩa, làm tròn nửa-về-chẵn = mặc định Python)*.
⛔ float cho tiền/tỷ giá *(`TypeError`)* — bên nạp JSON phải `parse_float=Decimal`
*(tỷ giá thật có lẻ: SGD 202507 = `20691.51` — `TIEN_DO.md` thăm dò O7)*.

⚠ Sheets tính bằng số thực IEEE-754 *(~15–17 chữ số có nghĩa)*, mã này 28 ⇒ ô mUSD vô hạn
tuần hoàn *(vd. 2,5 ÷ 25.500)* lệch nhau ở chữ số thứ ~16 — H4 phải khai dung sai khi so
với đáp án 406, ⛔ đòi bằng tuyệt đối.

Trước H1, grep `musd|bvnd|ty_gia` ở `fls/` + `tools/` = **2 dòng, cả hai là docstring**
`fls/bao_cao/__init__.py` ⇒ **0 dòng mã** quy đổi tỷ giá *(khớp ISP §1.3 đo 16/11)*.

⛔ Ngoài H1: dữ liệu thật + parity 406 *(H4)* · dòng HR 407/408 *(H7)* · cột `CA` Cash/Bank
qua `IX.ORG` *(C8)* · đọc `IX.FX` từ kho *(C5 — đến đây vẫn qua tham số)*.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_EVEN, Context, Decimal, localcontext
from typing import Iterable, Mapping

# Khuôn cột tiền tệ của GL — đúng thứ tự `IX.FX` (AP §3.2.1). ⛔ chứa tỷ giá.
TIEN_TE_GL: tuple[str, ...] = ("USD", "SGD", "COP", "VND", "HKD")

_MOT_TY = Decimal(10) ** 9        # 10^9 : VND → bVND        (BO/BP "… / 10^9")
_MOT_NGHIN = Decimal(10) ** 3     # 10^3 : tỷ USD → mUSD      (BR/BS "… × 10^3")
_KHONG = Decimal(0)

# Ngữ cảnh CỐ ĐỊNH ⇒ kết quả ⛔ phụ thuộc `getcontext()` của người gọi
# (bài `test_ket_qua_khong_phu_thuoc_ngu_canh_Decimal_cua_nguoi_goi`: prec = 5 ⇒ y nguyên).
_NGU_CANH = Context(prec=28, rounding=ROUND_HALF_EVEN)


class ThieuTyGia(LookupError):
    """Tháng/tiền tệ của dòng ⛔ có tỷ giá DƯƠNG dùng được. ⛔ Quy đổi ra 0 — `INV-I16`.

    Mang `thang` · `tien_te` · `vi_tri` *(vị trí dòng trong dãy đưa vào, đếm từ 1 — ⛔ phải
    số hàng sheet)* để bên gọi gom được *"tháng nào thiếu gì"* mà ⛔ phải đọc chữ.
    """

    def __init__(self, thang: object, tien_te: str, vi_tri: int, ly_do: str) -> None:
        self.thang = thang
        self.tien_te = tien_te
        self.vi_tri = vi_tri
        # MỘT dòng, đọc được ngay (luật phòng tái phạm `S0-R1-04`)
        super().__init__(
            f"⛔ thiếu tỷ giá {tien_te} tháng {thang!r} (dòng thứ {vi_tri}): {ly_do} — "
            f"⛔ quy đổi ra 0 (đó là lỗi SUMIFS = 0 của AS-IS, AP PD 405)"
        )


class TienTeNgoaiGL(ValueError):
    """Dòng mang tiền tệ ⛔ thuộc 5 cột của GL ⇒ ⛔ có cột để vào. ⛔ Bỏ qua, ⛔ dồn cột khác."""


@dataclass(frozen=True)
class DongGL:
    """Một dòng sổ đưa vào GL *(phần AS-IS dùng để quy đổi: tháng · tiền tệ · E · F)*.

    `thang` là `yyyymm` *(khoá của `IX.FX` — AP §3.2.1)*; `no`/`co` là **nguyên tệ**
    *(cột E/F)*, `Decimal` hoặc `int`.
    """

    thang: int
    tien_te: str
    no: Decimal
    co: Decimal


@dataclass(frozen=True)
class KetQuaDongGL:
    """Kết quả MỘT dòng, cùng thứ tự với dòng vào.

    `no`/`co`/`ton`: dict đủ 5 khoá `TIEN_TE_GL`, **nguyên tệ** — tiền nằm đúng ở cột tiền tệ
    của dòng, 4 cột kia = 0; `ton` là tồn luỹ kế SAU dòng này *(hành vi ① ở docstring tệp)*.
    `ty_gia`/`ty_gia_usd`: tỷ giá đã dùng *(tháng của dòng)* — để soi lại được từng ô.
    """

    dong: DongGL
    no: dict[str, Decimal]
    co: dict[str, Decimal]
    ton: dict[str, Decimal]
    ty_gia: Decimal
    ty_gia_usd: Decimal
    bvnd_no: Decimal      # BO
    bvnd_co: Decimal      # BP
    musd_no: Decimal      # BR
    musd_co: Decimal      # BS


def tinh_gl(
    dong: Iterable[DongGL],
    fx: Mapping[int, Mapping[str, Decimal]],
) -> list[KetQuaDongGL]:
    """Quy đổi từng dòng theo công thức NOW 406 *(docstring tệp)*; trả MỘT kết quả mỗi dòng.

    `fx`: tháng `yyyymm` → tiền tệ → số VND cho 1 đơn vị *(hình `IX.FX`)*. Thiếu tỷ giá ở
    BẤT KỲ dòng nào ⇒ `ThieuTyGia` cho cả lượt; tiền tệ ngoài 5 cột ⇒ `TienTeNgoaiGL`;
    float ⇒ `TypeError`.
    """
    ton = {t: _KHONG for t in TIEN_TE_GL}
    ra: list[KetQuaDongGL] = []
    with localcontext(_NGU_CANH):
        for vi_tri, d in enumerate(dong, start=1):
            no = _so_dung(d.no, "Nợ", vi_tri)
            co = _so_dung(d.co, "Có", vi_tri)
            if d.tien_te not in TIEN_TE_GL:
                raise TienTeNgoaiGL(
                    f"⛔ dòng thứ {vi_tri} mang tiền tệ {d.tien_te!r} — GL chỉ có 5 cột "
                    f"{' · '.join(TIEN_TE_GL)}; ⛔ bỏ qua, ⛔ dồn sang cột khác"
                )
            ty_gia = _tra_ty_gia(fx, d.thang, d.tien_te, vi_tri)
            ty_gia_usd = _tra_ty_gia(fx, d.thang, "USD", vi_tri)

            # ① tồn = tồn trên + Nợ − Có — cộng dồn theo THỨ TỰ đưa vào, theo tiền tệ
            ton[d.tien_te] = ton[d.tien_te] + no - co

            bvnd_no = ty_gia * no / _MOT_TY            # BO = tỷ giá × E / 10^9
            bvnd_co = ty_gia * co / _MOT_TY            # BP = tỷ giá × F / 10^9
            ra.append(KetQuaDongGL(
                dong=d,
                no={t: (no if t == d.tien_te else _KHONG) for t in TIEN_TE_GL},
                co={t: (co if t == d.tien_te else _KHONG) for t in TIEN_TE_GL},
                ton=dict(ton),
                ty_gia=ty_gia,
                ty_gia_usd=ty_gia_usd,
                bvnd_no=bvnd_no,
                bvnd_co=bvnd_co,
                musd_no=bvnd_no / ty_gia_usd * _MOT_NGHIN,   # BR = BO ÷ USD × 10^3
                musd_co=bvnd_co / ty_gia_usd * _MOT_NGHIN,   # BS = BP ÷ USD × 10^3
            ))
    return ra


def _so_dung(v: object, nhan: str, vi_tri: int) -> Decimal:
    """`Decimal`/`int` → `Decimal`; ⛔ float *(bụi dấu phẩy động — ⛔ được vào tiền)*.

    ⛔ In GIÁ TRỊ vào thông điệp: chỉ kiểu — thông điệp lỗi hay đi vào log/phiếu.
    """
    if not isinstance(v, (Decimal, int)):
        raise TypeError(
            f"⛔ {nhan} ở dòng thứ {vi_tri} là {type(v).__name__} — chỉ nhận Decimal/int, "
            f"⛔ float (JSON thì đọc bằng parse_float=Decimal)"
        )
    return Decimal(v)


def _tra_ty_gia(
    fx: Mapping[int, Mapping[str, Decimal]], thang: int, tien_te: str, vi_tri: int,
) -> Decimal:
    """`fx[thang][tien_te]` — vắng tháng, vắng cột, hay ≤ 0 đều là `ThieuTyGia`."""
    bang_thang = fx.get(thang)
    if bang_thang is None:
        raise ThieuTyGia(thang, tien_te, vi_tri, "tháng ⛔ có trong bảng tỷ giá")
    gia = bang_thang.get(tien_te)
    if gia is None:
        raise ThieuTyGia(thang, tien_te, vi_tri,
                         f"tháng có trong bảng nhưng ⛔ có cột {tien_te}")
    gia = _so_dung(gia, f"tỷ giá {tien_te} tháng {thang!r}", vi_tri)
    if gia <= 0:
        raise ThieuTyGia(thang, tien_te, vi_tri,
                         f"tỷ giá = {gia} ⛔ dương (0 là dấu vết SUMIFS trên tháng rỗng)")
    return gia
