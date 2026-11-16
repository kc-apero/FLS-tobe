"""H1 · `CA.GL` thuần — bài thử đơn vị của `fls/bao_cao/gl.py` *(ISP 3.1.2 Step 1 · `WO-070`)*.

Nguồn sự thật: `IncrementalStepPlan-FLS-Voi_v3.1.2.md` §Step 1 · H1 mục 6 (`H1-B1…B4`) +
AP v3.1.2 §3.3.1 hàng PD `406 · 412` — công thức NOW, chép NGUYÊN VĂN:

    A10 = QUERY(ITL Ledge); tách Nợ/Có theo 5 tiền tệ; tồn = tồn trên + Nợ − Có;
    BO/BP = tỷ giá × E|F / 10^9 (bVND); BR/BS = BO|BP ÷ USD × 10^3 (mUSD);
    CA = VLOOKUP(TK, Mapping Master AB→AD)

và cột conflict cùng hàng: *"tồn luỹ kế theo thứ tự dòng của cả bảng, ⛔ theo TK ⇒ phụ
thuộc sort; tỷ giá theo tháng"*. Hàng PD `405`: *"tra bằng SUMIFS(tháng) … tháng thiếu ⇒
mất số"* — đó là lỗi `H1-B3` canh.

⛔⛔ **Đính chính đơn vị của `H1-B1`** *(orchestrator 16/11 — ghi ở `BG-071` mục "lệch spec
đã xử")*. ISP ghi mong *"bVND 2,5 · mUSD 98,039…"*. Theo CHÍNH công thức AP ở trên:
`BO = 1 × 2.500.000.000 / 10^9 = 2,5` bVND, rồi `BR = 2,5 ÷ 25.500 × 10^3 = 0,098039…`
mUSD *(= 98,039… **nghìn** USD)*. Con số `98,039…` của ISP là cùng giá trị ở đơn vị
**nghìn USD**, ⛔ phải mUSD ⇒ bài thử theo CÔNG THỨC AP, và có một dòng canh riêng cho
đơn vị *(xem `test_H1_B1_…`)* để bản đính chính ⛔ bị lật lại im lặng.

⭐ **Mọi con số mong ở đây TÍNH TAY, ghi nguyên chữ số** — ⛔ gọi lại công thức của mã.
Một bài thử tự tính mong bằng chính công thức đang thử thì xanh cả khi công thức sai.
Phép tính tay ghi ngay cạnh từng hàng.

Tiền và tỷ giá là `Decimal` *(⛔ float — float là "bụi dấu phẩy động" `1.52587890625e-05`
mà `tools/do_trong_tai.py` đã phải lọc khỏi phép đo `DIF`)*.
"""

from __future__ import annotations

import copy
import os
import subprocess
import sys
from decimal import Decimal, localcontext
from pathlib import Path

import pytest

from fls.bao_cao.gl import (
    TIEN_TE_GL,
    DongGL,
    ThieuTyGia,
    TienTeNgoaiGL,
    tinh_gl,
)

D = Decimal
GOC = Path(__file__).resolve().parents[2]

# mUSD của dòng VND 2.500.000.000 là số VÔ HẠN TUẦN HOÀN (2,5 ÷ 25.500 = 1 ÷ 10.200) ⇒
# so tới 12 chữ số thập phân: 10^-12 mUSD = 10^-6 USD (một phần triệu đô).
Q12 = D("1E-12")

# ── Tỷ giá TỔNG HỢP (⛔ số thật) ─────────────────────────────────────────────────────
# Đúng hình `IX.FX` *(AP §3.2.1: "tháng yyyymm × USD · SGD · COP · VND (=1) · HKD")*:
# dict tháng → tiền tệ → số VND cho MỘT đơn vị tiền tệ ấy.
# ⚠ Hai tháng KHÁC NHAU ở mọi tiền tệ trừ VND ⇒ mã tra nhầm tháng là lệch ngay ở hàng 4–6.
FX = {
    202501: {"USD": D("25500"), "SGD": D("20400"), "COP": D("6.4"),
             "VND": D("1"), "HKD": D("3280")},
    202502: {"USD": D("25000"), "SGD": D("19500"), "COP": D("6.25"),
             "VND": D("1"), "HKD": D("3250")},
}

# ── 6 dòng TỔNG HỢP *(ISP H1 §3 "Mock/static: 6 dòng tổng hợp + tỷ giá tổng hợp")* ─────
# Phủ đủ 5 tiền tệ, cả hai phía Nợ/Có, hai tháng; dòng 1 = ca `H1-B1`, dòng 2→4 = ca `H1-B2`
# *(USD Nợ rồi USD Có, có SGD chen giữa ⇒ tồn USD phải bỏ qua dòng khác tiền tệ)*.
SAU_DONG = [
    DongGL(thang=202501, tien_te="VND", no=D("2500000000"), co=D("0")),
    DongGL(thang=202501, tien_te="USD", no=D("100000"), co=D("0")),
    DongGL(thang=202501, tien_te="SGD", no=D("0"), co=D("5000")),
    DongGL(thang=202502, tien_te="USD", no=D("0"), co=D("40000")),
    DongGL(thang=202502, tien_te="COP", no=D("10000000"), co=D("0")),
    DongGL(thang=202502, tien_te="HKD", no=D("0"), co=D("20000")),
]

# Mong TÍNH TAY cho từng dòng:
#   (tỷ giá dòng · bVND Nợ [BO] · bVND Có [BP] · mUSD Nợ [BR] · mUSD Có [BS] ·
#    tồn sau dòng theo thứ tự USD · SGD · COP · VND · HKD — nguyên tệ)
MONG = [
    # 1 · VND 202501: 1 × 2.500.000.000 / 10^9 = 2,5 · 2,5 ÷ 25.500 × 10^3 = 0,0980392156862745…
    ("1", "2.5", "0", "0.098039215686", "0",
     ("0", "0", "0", "2500000000", "0")),
    # 2 · USD 202501: 25.500 × 100.000 / 10^9 = 2,55 · 2,55 ÷ 25.500 × 10^3 = 0,1
    ("25500", "2.55", "0", "0.1", "0",
     ("100000", "0", "0", "2500000000", "0")),
    # 3 · SGD 202501: 20.400 × 5.000 / 10^9 = 0,102 · 0,102 ÷ 25.500 × 10^3 = 0,004
    ("20400", "0", "0.102", "0", "0.004",
     ("100000", "-5000", "0", "2500000000", "0")),
    # 4 · USD 202502: 25.000 × 40.000 / 10^9 = 1 · 1 ÷ 25.000 × 10^3 = 0,04 ·
    #     tồn USD = 100.000 − 40.000 = 60.000 (dòng SGD chen giữa ⛔ chạm tồn USD)
    ("25000", "0", "1", "0", "0.04",
     ("60000", "-5000", "0", "2500000000", "0")),
    # 5 · COP 202502: 6,25 × 10.000.000 / 10^9 = 0,0625 · 0,0625 ÷ 25.000 × 10^3 = 0,0025
    ("6.25", "0.0625", "0", "0.0025", "0",
     ("60000", "-5000", "10000000", "2500000000", "0")),
    # 6 · HKD 202502: 3.250 × 20.000 / 10^9 = 0,065 · 0,065 ÷ 25.000 × 10^3 = 0,0026
    ("3250", "0", "0.065", "0", "0.0026",
     ("60000", "-5000", "10000000", "2500000000", "-20000")),
]

NAM = ("USD", "SGD", "COP", "VND", "HKD")
KHONG = {t: 0 for t in NAM}


def test_nam_tien_te_dung_thu_tu_IX_FX():
    """5 cột tiền tệ của GL = 5 cột của `IX.FX`, đúng thứ tự AP §3.2.1."""
    assert TIEN_TE_GL == NAM


# ── H1-B1 ─────────────────────────────────────────────────────────────────────────────
def test_H1_B1_dong_VND_No_ra_bVND_2_5_va_mUSD_theo_cong_thuc_AP():
    """ISP `H1-B1`: dòng VND Nợ 2.500.000.000, tỷ giá USD 25.500 ⇒ bVND 2,5 · mUSD theo AP.

    ⛔ Đơn vị: mUSD = 0,098039… *(⛔ 98,039… — đó là NGHÌN USD; xem docstring tệp)*.
    """
    (kq,) = tinh_gl(
        [DongGL(thang=202501, tien_te="VND", no=D("2500000000"), co=D("0"))],
        {202501: {"USD": D("25500"), "VND": D("1")}},
    )
    # tách Nợ/Có theo 5 tiền tệ — tiền chỉ nằm ở cột VND phía Nợ
    assert kq.no == {**KHONG, "VND": D("2500000000")}
    assert kq.co == KHONG
    assert kq.ty_gia == D("1") and kq.ty_gia_usd == D("25500")
    # BO = 1 × 2.500.000.000 / 10^9
    assert kq.bvnd_no == D("2.5")
    assert kq.bvnd_co == 0
    # BR = 2,5 ÷ 25.500 × 10^3 = 0,0980392156862745098039… (chu kỳ 16 chữ số)
    assert kq.musd_no.quantize(Q12) == D("0.098039215686")
    assert kq.musd_co == 0
    # ⛔⛔ canh ĐƠN VỊ: 98,039… của ISP là nghìn USD = mUSD × 10^3 — ⛔ phải mUSD
    assert kq.musd_no < 1
    assert (kq.musd_no * 1000).quantize(D("0.001")) == D("98.039")


# ── H1-B2 ─────────────────────────────────────────────────────────────────────────────
def test_H1_B2_dong_USD_Co_tach_dung_cot_Co_ton_bang_ton_truoc_tru_Co():
    """ISP `H1-B2`: dòng USD Có ⇒ tách đúng cột Có; tồn = tồn trước − Có."""
    truoc, sau = tinh_gl(
        [
            DongGL(thang=202501, tien_te="USD", no=D("100000"), co=D("0")),
            DongGL(thang=202502, tien_te="USD", no=D("0"), co=D("40000")),
        ],
        FX,
    )
    assert sau.co == {**KHONG, "USD": D("40000")}
    assert sau.no == KHONG
    assert truoc.ton["USD"] == D("100000")
    # tồn = tồn trước − Có  ⇒  100.000 − 40.000
    assert sau.ton["USD"] == truoc.ton["USD"] - D("40000")
    assert sau.ton["USD"] == D("60000")
    # Có quy đổi theo tỷ giá THÁNG CỦA DÒNG: 202502 = 25.000 *(⛔ 25.500 của 202501)*
    assert sau.ty_gia == D("25000")
    assert sau.bvnd_co == D("1") and sau.bvnd_no == 0          # 25.000 × 40.000 / 10^9
    assert sau.musd_co == D("0.04") and sau.musd_no == 0       # 1 ÷ 25.000 × 10^3


# ── Goal của H1: "đúng tay tính trên 6 dòng tổng hợp" ─────────────────────────────────
def test_H1_sau_dong_tong_hop_khop_tay_tinh_tung_o():
    """ISP H1 §2 Goal — mỗi dòng: Nợ/Có tách theo 5 tiền tệ · bVND · mUSD · tồn, đúng tay tính.

    Đếm phủ *(Đ4)*: 6 dòng × (1 tỷ giá + 4 ô quy đổi + 5 ô tồn) = **60** ô so, cộng tách
    Nợ/Có 6 × 2 cột-tập — 5/5 tiền tệ, 2/2 tháng, 3/3 dòng Nợ + 3/3 dòng Có.
    """
    kq = tinh_gl(SAU_DONG, FX)
    assert len(kq) == len(SAU_DONG) == len(MONG) == 6        # Đ3: tập so ⛔ rỗng
    so_o = 0
    for i, (k, dong, mong) in enumerate(zip(kq, SAU_DONG, MONG), start=1):
        ty_gia, bvnd_no, bvnd_co, musd_no, musd_co, ton = mong
        assert k.dong == dong, f"dòng {i}: ⛔ giữ thứ tự / ⛔ trỏ đúng dòng vào"
        # tách theo 5 tiền tệ: ô khác 0 nằm ĐÚNG ở cột tiền tệ của dòng, phía đúng
        assert {t for t, v in k.no.items() if v} == ({dong.tien_te} if dong.no else set())
        assert {t for t, v in k.co.items() if v} == ({dong.tien_te} if dong.co else set())
        assert set(k.no) == set(k.co) == set(k.ton) == set(NAM)
        assert k.ty_gia == D(ty_gia), f"dòng {i}: tỷ giá"
        assert k.bvnd_no == D(bvnd_no), f"dòng {i}: bVND Nợ (BO)"
        assert k.bvnd_co == D(bvnd_co), f"dòng {i}: bVND Có (BP)"
        assert k.musd_no.quantize(Q12) == D(musd_no), f"dòng {i}: mUSD Nợ (BR)"
        assert k.musd_co.quantize(Q12) == D(musd_co), f"dòng {i}: mUSD Có (BS)"
        assert [k.ton[t] for t in NAM] == [D(x) for x in ton], f"dòng {i}: tồn"
        so_o += 1 + 4 + 5
    assert so_o == 60


def test_ton_luy_ke_theo_THU_TU_dong_dua_vao__giu_hanh_vi_AS_IS():
    """AP §3.3.1 conflict của 406: *"tồn luỹ kế theo thứ tự dòng của cả bảng, ⛔ theo TK ⇒
    phụ thuộc sort"*. H1 **GIỮ** hành vi ấy *(ISP H1 §3: "giữ hành vi AS-IS, ghi rõ")* để
    H4 so parity được với đáp án 406; tồn theo (TK, ngày) là đích TO-BE, ⛔ việc của H1.

    Mong: cùng tập dòng ⇒ tồn CUỐI như nhau; nhưng tồn GIỮA bảng đổi theo thứ tự đưa vào.
    """
    xuoi = tinh_gl(SAU_DONG, FX)
    nguoc = tinh_gl(list(reversed(SAU_DONG)), FX)
    assert xuoi[-1].ton == nguoc[-1].ton
    # đảo thứ tự: dòng USD Có 40.000 (dòng 4) đứng ở vị trí 3, TRƯỚC dòng USD Nợ 100.000
    assert nguoc[2].dong == SAU_DONG[3]
    assert nguoc[2].ton["USD"] == D("-40000")          # 0 − 40.000
    assert xuoi[3].ton["USD"] == D("60000")            # 100.000 − 40.000


# ── H1-B3 ─────────────────────────────────────────────────────────────────────────────
def test_H1_B3_thang_khong_co_ty_gia_nem_ThieuTyGia__khong_tra_0():
    """ISP `H1-B3`: tháng ⛔ có tỷ giá ⇒ lỗi CÓ TÊN, ⛔ trả 0.

    AS-IS tra tỷ giá bằng `SUMIFS(tháng)` *(AP PD 405)*: tháng vắng ⇒ SUMIFS = 0 ⇒ bVND/mUSD
    = 0 **im lặng** — *"tháng thiếu ⇒ mất số"*. Ở đây: ném lỗi, ⛔ trả nửa bảng.
    """
    dong = [SAU_DONG[0], DongGL(thang=202503, tien_te="VND", no=D("1000000"), co=D("0"))]
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl(dong, FX)
    assert (e.value.thang, e.value.tien_te, e.value.vi_tri) == (202503, "VND", 2)
    thong_diep = str(e.value)
    # luật phòng tái phạm `S0-R1-04`: nguyên nhân đọc được trong MỘT dòng
    assert "202503" in thong_diep and "VND" in thong_diep and "\n" not in thong_diep


def test_H1_B3_thang_co_nhung_thieu_tien_te_cua_dong():
    fx = {202501: {"USD": D("25500"), "VND": D("1")}}
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl([DongGL(thang=202501, tien_te="SGD", no=D("0"), co=D("5000"))], fx)
    assert (e.value.thang, e.value.tien_te, e.value.vi_tri) == (202501, "SGD", 1)


def test_H1_B3_thieu_ty_gia_USD_thi_khong_quy_ra_mUSD_duoc():
    """mUSD = bVND ÷ **USD** × 10^3 ⇒ dòng VND cũng cần tỷ giá USD của tháng ấy."""
    fx = {202501: {"VND": D("1")}}
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl([SAU_DONG[0]], fx)
    assert (e.value.thang, e.value.tien_te) == (202501, "USD")


@pytest.mark.parametrize("ty_gia", [D("0"), D("-20400")], ids=["bang_0", "am"])
def test_H1_B3_ty_gia_khong_duong_tinh_la_thieu__0_la_dau_vet_SUMIFS_rong(ty_gia):
    """Tỷ giá `0` chính là thứ `SUMIFS` trả cho tháng vắng ⇒ coi như THIẾU, ⛔ quy đổi ra 0.

    Dòng SGD với tỷ giá SGD = 0 mà ⛔ chặn thì bVND = 0 và mUSD = 0 **im lặng** — đúng
    lỗi AS-IS. Tỷ giá âm ⛔ có nghĩa ⇒ cùng lỗi.
    """
    fx = {202501: {"USD": D("25500"), "SGD": ty_gia}}
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl([SAU_DONG[2]], fx)
    assert (e.value.thang, e.value.tien_te) == (202501, "SGD")


# ── Đầu vào ⛔ vào được 5 cột / ⛔ phải Decimal ⇒ lỗi, ⛔ đoán (`INV-I16`) ─────────────────
def test_tien_te_ngoai_nam_cot_GL_nem_TienTeNgoaiGL__khong_roi_im_lang():
    """GL có đúng 5 cột tiền tệ ⇒ dòng EUR ⛔ có cột để vào — kể cả khi có tỷ giá EUR.
    ⛔ Bỏ qua im lặng *(mất tiền khỏi GL)*, ⛔ quy về cột nào khác *(bịa)*."""
    fx = {202501: {**FX[202501], "EUR": D("27000")}}
    with pytest.raises(TienTeNgoaiGL) as e:
        tinh_gl([DongGL(thang=202501, tien_te="EUR", no=D("10"), co=D("0"))], fx)
    assert "EUR" in str(e.value) and "\n" not in str(e.value)


@pytest.mark.parametrize("cho", ["no", "co", "ty_gia"])
def test_float_cho_tien_hoac_ty_gia_bi_tu_choi(cho):
    """⛔ float cho tiền/tỷ giá: `0.1 + 0.2 != 0.3`. JSON đọc thường cho float
    *(`20691.51`)* ⇒ bên nạp phải `json.load(..., parse_float=Decimal)`."""
    no, co, fx = D("100000"), D("0"), {202501: {"USD": D("25500")}}
    if cho == "no":
        no = 100000.0
    elif cho == "co":
        co = 0.5
    else:
        fx = {202501: {"USD": 25500.0}}
    with pytest.raises(TypeError):
        tinh_gl([DongGL(thang=202501, tien_te="USD", no=no, co=co)], fx)


def test_so_nguyen_int_duoc_nhan_dung_nhu_Decimal():
    """`int` đúng tuyệt đối *(⛔ như float)* ⇒ nhận, kết quả y như Decimal."""
    (k,) = tinh_gl([DongGL(thang=202501, tien_te="USD", no=100000, co=0)],
                   {202501: {"USD": 25500}})
    assert k.bvnd_no == D("2.55") and k.musd_no == D("0.1")      # như dòng 2 của MONG


# ── Hàm THUẦN: cùng đầu vào ⇒ cùng con số (điều kiện để parity HD2 có nghĩa) ─────────────
def test_ket_qua_khong_phu_thuoc_ngu_canh_Decimal_cua_nguoi_goi():
    """Độ chính xác `Decimal` là trạng thái TOÀN CỤC của luồng. Người gọi hạ `prec` = 5 mà
    kết quả đổi theo thì *"cùng đầu vào ⇒ cùng con số"* ⛔ còn đúng — cổng parity H4 có
    thể xanh/đỏ tuỳ ai gọi trước."""
    chuan = tinh_gl(SAU_DONG, FX)
    with localcontext() as nc:
        nc.prec = 5
        thu = tinh_gl(SAU_DONG, FX)
    assert thu == chuan


def test_ham_thuan__khong_sua_dau_vao():
    fx = copy.deepcopy(FX)
    dong = list(SAU_DONG)
    tinh_gl(dong, fx)
    assert fx == FX and dong == SAU_DONG


# ── H1-B4 ─────────────────────────────────────────────────────────────────────────────
# Chạy ĐÚNG hợp đồng 11 của `.importlinter` trong một tiến trình con *(⛔ trong tiến trình
# pytest: `importlinter.cli.lint_imports` chèn `sys.path` và cấu hình lại `logging`)*.
_LINT_HOP_DONG_11 = (
    "import sys; from importlinter.cli import lint_imports; "
    "sys.exit(lint_imports(config_filename='.importlinter', limit_to_contracts=('11',), "
    "no_cache=True, no_logo=True))"
)


def test_H1_B4_fls_bao_cao_khong_cham_kho__lint_imports_hop_dong_11():
    """ISP `H1-B4`: `fls/bao_cao` ⛔ chạm DB — đo bằng `lint-imports` *(hợp đồng 11: cấm
    `psycopg` · `fls.repo` · `fls.db`, kể cả gián tiếp)*.

    Đ3: trước H1 gói `fls/bao_cao` RỖNG ⇒ hợp đồng xanh **trên tập rỗng**. Bài này đòi
    `gl.py` CÓ MÃ trước, rồi mới tin chữ `KEPT`. Đ5: chạy hỏng *(⛔ có `importlinter`,
    ⛔ thấy dòng tổng kết)* là ĐỎ, ⛔ bỏ qua.
    """
    gl = GOC / "fls" / "bao_cao" / "gl.py"
    assert gl.is_file() and "def tinh_gl" in gl.read_text(encoding="utf-8")
    r = subprocess.run(
        [sys.executable, "-c", _LINT_HOP_DONG_11],
        cwd=GOC, env={**os.environ, "PYTHONUTF8": "1"},   # CLAUDE.md: thiếu ⇒ in 0 byte
        capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    ra = r.stdout + r.stderr
    assert r.returncode == 0, ra
    assert any(d.startswith("fls.bao_cao ") and d.rstrip().endswith("KEPT")
               for d in r.stdout.splitlines()), ra
    assert "Contracts: 1 kept, 0 broken." in r.stdout, ra
