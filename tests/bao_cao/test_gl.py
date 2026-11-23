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

import ast
import copy
import json
import os
import subprocess
import sys
from decimal import Decimal, localcontext
from pathlib import Path

import pytest

import fls.bao_cao.gl as gl_mod
from fls.bao_cao.gl import (
    TIEN_TE_GL,
    DongGL,
    ThieuTyGia,
    TienTeNgoaiGL,
    tinh_gl,
)
from fls.canon.tien_te import ma_tien_te

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


# ═══ Vòng sửa sau R1 (`KQ-072`) ═══════════════════════════════════════════════════════════
# Mỗi bài dưới đây mang mã phát hiện của sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H1.md`
# (`H1-R1-0n` ⇒ tiền tố `test_R1_0n_`). Bài ĐỎ trên mã cũ `5c0a2e2` vì THIẾU hành vi
# (`R1-01` · `R1-02` · `R1-05`); bài XANH sẵn trên mã cũ (`R1-03` · `R1-06` · `R1-07` — mã đúng,
# chỉ thiếu bài ghim) được chứng minh có răng bằng đột biến trên BẢN SAO ngoài worktree.
# Log cả hai: `BG-071` mục "Vòng sửa sau R1 (KQ-072)".


def _gan(ma: Decimal, tay: str) -> bool:
    """`|mã − tay| ≤ 10^-26 × |tay|` — cho ô có phép CHIA *(BN · BT)*.

    Mã chạy 28 chữ số có nghĩa *(`_NGU_CANH`)*; số `tay` ghi ≥ 30 chữ số thập phân, CẮT từ
    phân số đúng tuyệt đối *(`Fraction`)* ⇒ sai số cắt ≤ 10^-34. BT còn cộng dồn các BR/BS đã
    làm tròn ⇒ ⛔ đòi bằng tuyệt đối; độ đúng tuyệt đối của MỘT phép chia được ghim riêng ở
    `test_R1_07_…`. So trong ngữ cảnh 60 chữ số để chính phép trừ ⛔ làm tròn.
    """
    with localcontext() as nc:
        nc.prec = 60
        t = D(tay)
        return abs(ma - t) <= abs(t) * D("1E-26")


# ── H1-R1-01 · MỌI phép so tiền tệ qua `ma_tien_te` (`BA-07` §4g v3.11) ──────────────────
# Bốn biến thể R1 đo (`KQ-072` F-1). Viết bằng ESCAPE — ⛔ chép ký tự vô hình vào nguồn
# (chính `fls/canon/tien_te.py` ghi: 22/30 ký tự trắng VÔ HÌNH trong trình soạn thảo).
BIEN_THE_VND = ["vnd", " VND", "VND\u00a0", "\ufeffVND"]


@pytest.mark.parametrize("ma", BIEN_THE_VND,
                         ids=["chu_thuong", "cach_dau", "NBSP_cuoi", "BOM_dau"])
def test_R1_01_bien_the_ma_tien_te_vao_dung_cot_VND_nhu_moi_cho_khac_cua_FLS(ma):
    """`BA-07` §4g v3.11: *"**mọi** phép so tiền tệ trong `fls/` gọi `ma_tien_te`"*; GL gom
    theo tiền tệ để ra số in = lớp ⓑ *"áp"* (§4g v3.12). Trên `e0bd4a6` cả bốn biến thể ⇒
    `TienTeNgoaiGL` *(R1 đo 4/4)*, trong khi rổ, bậc tiền và cửa ghi của FLS coi là `VND`.

    Mong = y hệt dòng `H1-B1` mã sạch: tiền ở cột VND, tra tỷ giá VND, tồn VND.
    """
    assert ma_tien_te(ma) == "VND"            # Đ3: biến thể THẬT là VND theo luật FLS
    (k,) = tinh_gl([DongGL(thang=202501, tien_te=ma, no=D("2500000000"), co=D("0"))],
                   {202501: {"USD": D("25500"), "VND": D("1")}})
    assert k.no == {**KHONG, "VND": D("2500000000")} and k.co == KHONG
    assert k.ton == {**KHONG, "VND": D("2500000000")}
    assert k.ty_gia == D("1") and k.bvnd_no == D("2.5")       # 1 × 2.500.000.000 / 10^9


def test_R1_01_bien_the_cung_mot_ma_cong_don_vao_CUNG_mot_cot_ton():
    """Khoá tồn cũng là một phép so tiền tệ: `'USD'` rồi `'usd'+U+3000` phải cộng dồn vào
    CÙNG cột tồn USD *(100 − 30 = 70)*, ⛔ mở cột thứ sáu, ⛔ ném."""
    a, b = tinh_gl([DongGL(thang=202501, tien_te="USD", no=D("100"), co=D("0")),
                    DongGL(thang=202501, tien_te="usd\u3000", no=D("0"), co=D("30"))], FX)
    assert a.ton["USD"] == D("100")
    assert b.co == {**KHONG, "USD": D("30")}
    assert b.ton == {**KHONG, "USD": D("70")}


def test_R1_01_khoa_tien_te_cua_bang_ty_gia_cung_qua_ma_tien_te():
    """Tra `fx` là phép so tiền tệ thứ ba *(khoá của bảng ↔ mã của dòng)*. Bảng mang khoá
    `'usd'` · `' VND'` mà ⛔ chuẩn hoá thì dòng VND sạch rơi vào `ThieuTyGia` — ồn, nhưng là
    lỗi SAI tên *("thiếu tỷ giá" trong khi tỷ giá CÓ)*."""
    (k,) = tinh_gl([SAU_DONG[0]], {202501: {"usd": D("25500"), " VND": D("1")}})
    assert (k.ty_gia, k.ty_gia_usd) == (D("1"), D("25500"))
    assert k.bvnd_no == D("2.5")


def test_R1_01_hai_khoa_cung_chuan_hoa_ve_mot_ma__ThieuTyGia_mo_ho__khong_chon_bua():
    """Chuẩn hoá khoá đẻ ra một ca MỚI: `{'USD': 25.500, 'usd': 26.000}` = HAI tỷ giá cho MỘT
    tiền tệ. Chọn một là đoán — AS-IS chọn theo hai cách khác nhau *(`CALC_ZONE_406.md`
    "tháng TRÙNG": INDEX/MATCH lấy dòng ĐẦU, SUMIFS CỘNG ĐÔI)*. Đ5: mẫu khớp **≥ 2** lần là
    ⛔ đo được ⇒ lỗi có tên, ⛔ chọn bừa."""
    fx = {202501: {"USD": D("25500"), "usd": D("26000"), "VND": D("1")}}
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl([SAU_DONG[0]], fx)
    assert (e.value.thang, e.value.tien_te, e.value.vi_tri) == (202501, "USD", 1)
    assert "mơ hồ" in str(e.value) and "\n" not in str(e.value)


# ── H1-R1-02 · tiền / tỷ giá ⛔ HỮU HẠN ⇒ lỗi có tên ─────────────────────────────────────
@pytest.mark.parametrize("phia", ["no", "co"])
@pytest.mark.parametrize("so", ["NaN", "sNaN", "Infinity", "-Infinity"])
def test_R1_02_tien_khong_huu_han_bi_tu_choi_co_ten(so, phia):
    """`Decimal` NaN/±Infinity ⛔ là tiền. Trên `e0bd4a6` *(R1 đo)*: NaN ở Nợ ⇒ ⛔ ném, tồn =
    bVND = mUSD = NaN, và vì tồn LUỸ KẾ ⇒ **mọi dòng sau** cùng tiền tệ cũng NaN; Infinity ở
    Có ⇒ tồn `-Infinity`; sNaN ⇒ `decimal.InvalidOperation` *(⛔ có tên)*. Đường vào có thật:
    `fls_itl.ps_no`/`ps_co` là `numeric(20,2)` ⛔ CHECK *(`0001_baseline.sql:45-46`)*, PG
    nhận `'NaN'`, psycopg trả `Decimal('NaN')`.

    Mong: `TienKhongHuuHan` *(một `ValueError`)* mang `vi_tri` của dòng hỏng — ở đây dòng 2,
    sau một dòng lành ⇒ ⛔ trả nửa bảng.
    """
    no, co = (D(so), D("0")) if phia == "no" else (D("0"), D(so))
    with pytest.raises(ValueError) as e:
        tinh_gl([SAU_DONG[1], DongGL(thang=202501, tien_te="VND", no=no, co=co)], FX)
    assert isinstance(e.value, gl_mod.TienKhongHuuHan), repr(e.value)
    assert e.value.vi_tri == 2 and "\n" not in str(e.value)


@pytest.mark.parametrize("cot", ["VND", "USD"])
@pytest.mark.parametrize("so", ["NaN", "sNaN", "Infinity"])
def test_R1_02_ty_gia_khong_huu_han_la_THIEU__ThieuTyGia(so, cot):
    """Tỷ giá ⛔ hữu hạn = ⛔ có tỷ giá dùng được ⇒ cùng lớp với tỷ giá ≤ 0 *(`H1-B3`)*.
    Trên `e0bd4a6` *(đo ở pha đỏ của vòng sửa)*: NaN/sNaN ⇒ `InvalidOperation` từ phép so
    `<= 0` *(⛔ có tên)*; Infinity ở cột VND ⇒ `InvalidOperation` từ `Infinity × 0` ở BP *(dòng
    chỉ có Nợ — dòng mang cả hai vế thì LỌT, bVND = Infinity)*; Infinity ở cột USD ⇒ LỌT, mUSD
    = 0 IM LẶNG. `-Infinity` đã bị `≤ 0` chặn."""
    fx = {202501: {"USD": D("25500"), "VND": D("1"), cot: D(so)}}
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl([SAU_DONG[0]], fx)
    assert (e.value.thang, e.value.tien_te, e.value.vi_tri) == (202501, cot, 1)


# ── H1-R1-03 · dòng mang CẢ Nợ lẫn Có ───────────────────────────────────────────────────
def test_R1_03_dong_mang_CA_No_lan_Co__ton_va_quy_doi_dung_ca_hai_phia():
    """Công thức ô xử CẢ HAI vế trên MỘT hàng *(`CALC_ZONE_406.md`: `AX = if($D=AX$9,$E,"")` ·
    `AY = if($D=AY$9,$F,"")` · `AZ11 = AZ10+AX11-AY11`)*. 6 dòng tổng hợp ⛔ có dòng nào như
    thế ⇒ R1 đột biến *"bỏ/ghi đè một vế"* (`R1-M1` · `M2` · `M6`) SỐNG 18/18. Sổ thật hôm nay
    **0 / 10.030** dòng cả hai vế *(`07_API_CONTRACT.md:446`)* — bài canh nhánh công thức,
    ⛔ canh tần suất. Số của R1 *(`KQ-072` đề xuất `test_R1_01_…`)*: USD E = 100 · F = 30 @ 25.500.
    """
    (k,) = tinh_gl([DongGL(thang=202501, tien_te="USD", no=D("100"), co=D("30"))], FX)
    assert k.no == {**KHONG, "USD": D("100")} and k.co == {**KHONG, "USD": D("30")}
    assert k.ton["USD"] == D("70")                                   # 0 + 100 − 30
    assert (k.bvnd_no, k.bvnd_co) == (D("0.00255"), D("0.000765"))  # 25.500 × 100 | 30 / 10^9
    assert (k.musd_no, k.musd_co) == (D("0.0001"), D("0.00003"))    # BO | BP ÷ 25.500 × 10^3


# ── H1-R1-05 · bốn cột còn lại của CALC ZONE: BM · BN · BQ · BT ─────────────────────────
# Công thức ô NOW (`CALC_ZONE_406.md`, orchestrator đọc 16/11 — chỉ công thức):
#   BM = AZ×USD + BC×SGD + BF×COP + BI + BL×HKD        (VND; tỷ giá = THÁNG CỦA DÒNG đang xét)
#   BN = (AZ + BC×SGD/USD + BF×COP/USD + BI/USD + BL×HKD/USD) / 10^6              (mUSD)
#   BQ = BQ trên + BO − BP      (bVND, luỹ kế)  ·  BT = BT trên + BR − BS      (mUSD, luỹ kế)
# Mong TÍNH TAY bằng `Fraction` ngoài repo, ⛔ gọi `gl.py` — phép tính ghi cạnh từng hàng.
# Thứ tự mỗi hàng: (BM, BN, BQ, BT).
MONG_BM_BT = [
    # 1 · 202501 · tồn VND 2.500.000.000 ⇒ BM = BI = 2.500.000.000
    #     BN = 2.500.000.000 / 25.500 / 10^6 · BQ = BO = 2,5 · BT = BR = 0,0980392156…
    ("2500000000", "0.0980392156862745098039215686274509",
     "2.5", "0.0980392156862745098039215686274509"),
    # 2 · + tồn USD 100.000 ⇒ BM = 100.000 × 25.500 + 2.500.000.000 = 5.050.000.000
    #     BN = (100.000 + 98.039,2156…) / 10^6 · BQ = 2,5 + 2,55 = 5,05 · BT = 0,098039… + 0,1
    ("5050000000", "0.1980392156862745098039215686274509",
     "5.05", "0.1980392156862745098039215686274509"),
    # 3 · + tồn SGD −5.000 ⇒ BM = 5.050.000.000 − 5.000 × 20.400 = 4.948.000.000
    #     BN = (100.000 − 5.000 × 20.400 / 25.500 + 98.039,2156…) / 10^6
    #        = (100.000 − 4.000 + 98.039,2156…) / 10^6
    #     BQ = 5,05 − 0,102 = 4,948 · BT = 0,198039… − 0,004
    #     ⭐ cùng MỘT tháng từ dòng 1 ⇒ BM = BQ × 10^9 (4.948.000.000) và BN = BT
    ("4948000000", "0.1940392156862745098039215686274509",
     "4.948", "0.1940392156862745098039215686274509"),
    # 4 · 202502 — ĐÁNH GIÁ LẠI tồn cũ theo tỷ giá tháng MỚI (dòng này chỉ là USD Có 40.000):
    #     tồn USD 60.000 · SGD −5.000 · VND 2.500.000.000
    #     BM = 60.000 × 25.000 − 5.000 × 19.500 + 2.500.000.000 = 3.902.500.000
    #     BN = (60.000 − 5.000 × 19.500 / 25.000 + 2.500.000.000 / 25.000) / 10^6
    #        = (60.000 − 3.900 + 100.000) / 10^6 = 0,1561
    #     BQ = 4,948 − 1 = 3,948  ⚠ ≠ BM / 10^9 = 3,9025: BQ cộng theo tỷ giá LỊCH SỬ từng dòng
    #     BT = 0,194039… − 0,04
    ("3902500000", "0.1561", "3.948", "0.1540392156862745098039215686274509"),
    # 5 · + tồn COP 10.000.000 ⇒ BM = 3.902.500.000 + 10.000.000 × 6,25 = 3.965.000.000
    #     BN = (156.100 + 10.000.000 × 6,25 / 25.000) / 10^6 = (156.100 + 2.500) / 10^6 = 0,1586
    #     BQ = 3,948 + 0,0625 = 4,0105 · BT = 0,154039… + 0,0025
    ("3965000000", "0.1586", "4.0105", "0.1565392156862745098039215686274509"),
    # 6 · + tồn HKD −20.000 ⇒ BM = 3.965.000.000 − 20.000 × 3.250 = 3.900.000.000
    #     BN = (158.600 − 20.000 × 3.250 / 25.000) / 10^6 = (158.600 − 2.600) / 10^6 = 0,156
    #     BQ = 4,0105 − 0,065 = 3,9455 · BT = 0,156539… − 0,0026
    ("3900000000", "0.156", "3.9455", "0.1539392156862745098039215686274509"),
]


def test_R1_05_bon_cot_BM_BN_BQ_BT__sau_dong_tong_hop_khop_tay_tinh():
    """Quyết định orchestrator 16/11 sau R1 *(`H1-R1-05`)*: engine CA.GL trả đủ **8** cột
    BM–BT. Ca này phủ: 5/5 tiền tệ có tồn ≠ 0 *(BM/BN cộng tới 5 số hạng)*, 3 dòng CÙNG tháng
    rồi ĐỔI tháng *(dòng 4 — đánh giá lại: BM đổi dù dòng ⛔ chạm tồn SGD/VND)*.

    BM · BQ: ⛔ có phép chia ⇒ so BẰNG tuyệt đối. BN · BT: so `_gan` *(10^-26 tương đối)*.
    Đếm phủ *(Đ4)*: 6 dòng × 4 cột = **24** ô so.
    """
    kq = tinh_gl(SAU_DONG, FX)
    assert len(kq) == len(MONG_BM_BT) == 6                   # Đ3: tập so ⛔ rỗng
    so_o = 0
    for i, (k, (bm, bn, bq, bt)) in enumerate(zip(kq, MONG_BM_BT), start=1):
        assert k.vnd_ton_all == D(bm), f"dòng {i}: BM = {k.vnd_ton_all}"
        assert _gan(k.musd_ton_all, bn), f"dòng {i}: BN = {k.musd_ton_all}"
        assert k.bvnd_ton == D(bq), f"dòng {i}: BQ = {k.bvnd_ton}"
        assert _gan(k.musd_ton, bt), f"dòng {i}: BT = {k.musd_ton}"
        so_o += 4
    assert so_o == 24


# Ca 2 của R1 *(`KQ-072` §Tính tay — 3 dòng SGD ở 3 tháng khác nhau, 1 dòng USD chen giữa
# CÙNG tháng với dòng SGD trước nó, 1 dòng mang CẢ Nợ lẫn Có)*. Tỷ giá SGD 202507 =
# `20.691,51` = số lẻ thật của thăm dò O7 *(`TIEN_DO.md`)*; các tỷ giá khác tổng hợp.
FX_R1 = {
    202506: {"USD": D("26000"), "SGD": D("19876.5"), "VND": D("1")},
    202507: {"USD": D("25500"), "SGD": D("20691.51"), "VND": D("1")},
    202508: {"USD": D("25500"), "SGD": D("20500"), "VND": D("1")},
}
DONG_R1 = [
    DongGL(thang=202506, tien_te="SGD", no=D("12345.67"), co=D("0")),
    DongGL(thang=202507, tien_te="SGD", no=D("0"), co=D("2000.5")),
    DongGL(thang=202507, tien_te="USD", no=D("1000"), co=D("0")),
    DongGL(thang=202508, tien_te="SGD", no=D("500"), co=D("100")),
]
# Thứ tự mỗi hàng: (tồn SGD, tồn USD, BM, BN, BQ, BT)
MONG_R1 = [
    # ① 202506 SGD Nợ 12.345,67 ⇒ tồn SGD 12.345,67
    #    BM = 12.345,67 × 19.876,5 = 245.388.709,755 · BN = 245.388.709,755 / 26.000 / 10^6
    #    BQ = BO = 19.876,5 × 12.345,67 / 10^9 = 0,245388709755
    #    BT = BR = 0,245388709755 / 26.000 × 10^3 = 0,00943802729826923076923…
    ("12345.67", "0", "245388709.755", "0.0094380272982692307692307692307692",
     "0.245388709755", "0.0094380272982692307692307692307692"),
    # ② 202507 SGD Có 2.000,5 ⇒ tồn SGD = 12.345,67 − 2.000,5 = 10.345,17
    #    BM = 10.345,17 × 20.691,51 = 214.057.188,5067   (đánh giá lại theo tỷ giá 202507)
    #    BN = 214.057.188,5067 / 25.500 / 10^6
    #    BQ = 0,245388709755 − 20.691,51 × 2.000,5 / 10^9 = 0,245388709755 − 0,041393365755
    #       = 0,203995344
    #    BT = 0,00943802729826923… − 0,041393365755 / 25.500 × 10^3 (= 0,00162326924529411…)
    ("10345.17", "0", "214057188.5067", "0.0083943995492823529411764705882352",
     "0.203995344", "0.0078147580529751131221719457013574"),
    # ③ 202507 USD Nợ 1.000 — CÙNG tháng ⇒ BM có HAI tiền tệ
    #    BM = 1.000 × 25.500 + 10.345,17 × 20.691,51 = 25.500.000 + 214.057.188,5067
    #       = 239.557.188,5067
    #    BN = (1.000 + 214.057.188,5067 / 25.500) / 10^6
    #    BQ = 0,203995344 + 25.500 × 1.000 / 10^9 = 0,203995344 + 0,0255 = 0,229495344
    #    BT = 0,00781475805297511… + 0,0255 / 25.500 × 10^3 (= 0,001)
    ("10345.17", "1000", "239557188.5067", "0.0093943995492823529411764705882352",
     "0.229495344", "0.0088147580529751131221719457013574"),
    # ④ 202508 SGD Nợ 500 · Có 100 (CẢ HAI vế) ⇒ tồn SGD = 10.345,17 + 500 − 100 = 10.745,17
    #    BM = 1.000 × 25.500 + 10.745,17 × 20.500 = 25.500.000 + 220.275.985 = 245.775.985
    #    BN = 245.775.985 / 25.500 / 10^6
    #    BQ = 0,229495344 + 0,01025 − 0,00205 = 0,237695344   ← mong của R1 (`KQ-072`)
    #    BT = 0,00881475805297511… + 0,000401960784313725… − 0,0000803921568627450…
    #       = 0,009136326680426093…                          ← mong của R1 (`KQ-072`)
    ("10745.17", "1000", "245775985", "0.0096382739215686274509803921568627",
     "0.237695344", "0.0091363266804260935143288084464555"),
]


def test_R1_05_BM_BN_BQ_BT__ca_SGD_luy_ke_cua_R1_khop_tay_tinh():
    """Ca 2 của R1, dòng ①→④: tồn SGD luỹ kế qua 3 tháng, BM/BN đánh giá lại theo tỷ giá
    THÁNG CỦA DÒNG *(② và ③ cùng 202507; ④ sang 202508)*, BQ/BT cộng theo tỷ giá LỊCH SỬ.
    Đếm phủ: 4 dòng × 6 ô = **24** ô so."""
    kq = tinh_gl(DONG_R1, FX_R1)
    assert len(kq) == len(MONG_R1) == 4
    so_o = 0
    for i, (k, (sgd, usd, bm, bn, bq, bt)) in enumerate(zip(kq, MONG_R1), start=1):
        assert (k.ton["SGD"], k.ton["USD"]) == (D(sgd), D(usd)), f"dòng {i}: tồn"
        assert k.vnd_ton_all == D(bm), f"dòng {i}: BM = {k.vnd_ton_all}"
        assert _gan(k.musd_ton_all, bn), f"dòng {i}: BN = {k.musd_ton_all}"
        assert k.bvnd_ton == D(bq), f"dòng {i}: BQ = {k.bvnd_ton}"
        assert _gan(k.musd_ton, bt), f"dòng {i}: BT = {k.musd_ton}"
        so_o += 6
    assert so_o == 24
    assert kq[-1].bvnd_ton == D("0.237695344")                # mong tham chiếu của orchestrator


def test_R1_05_BM_ton_khac_0_ma_thang_cua_dong_thieu_ty_gia_tien_te_ay__ThieuTyGia():
    """BM đánh giá lại tồn của MỌI tiền tệ theo tỷ giá tháng của dòng ĐANG XÉT ⇒ dòng USD
    tháng 202502 cũng cần tỷ giá **SGD** 202502 khi tồn SGD ≠ 0. AS-IS: `SUMIFS` = 0 ⇒ BM nhân
    0 ⇒ **mất số SGD IM LẶNG** *(`CALC_ZONE_406.md` "Hai NGỮ NGHĨA")*. FLS *(D1)*: lỗi có tên,
    mang tiền tệ THIẾU *(SGD)* — ⛔ tiền tệ của dòng *(USD)*."""
    fx = {202501: {"USD": D("25500"), "SGD": D("20400")}, 202502: {"USD": D("25000")}}
    dong = [DongGL(thang=202501, tien_te="SGD", no=D("100"), co=D("0")),
            DongGL(thang=202502, tien_te="USD", no=D("10"), co=D("0"))]
    with pytest.raises(ThieuTyGia) as e:
        tinh_gl(dong, fx)
    assert (e.value.thang, e.value.tien_te, e.value.vi_tri) == (202502, "SGD", 2)
    assert "BM" in str(e.value) and "\n" not in str(e.value)


def test_R1_05_BM_chi_doi_ty_gia_cua_tien_te_co_ton_khac_0__VND_cong_thang():
    """Hai ranh giới của bài trên, khai `mong` cả hai chiều *(Đ5)*:

    ⓐ tồn = 0 ⇒ số hạng = 0 bất kể tỷ giá ⇒ ⛔ đòi tỷ giá *(AS-IS `0 × 0 = 0` cũng ⛔ mất số)*
       — dòng `H1-B1` với bảng chỉ có USD · VND vẫn ra BM/BN;
    ⓑ VND: ô `… + BI + …` và `BI/USD` — ⛔ tra tỷ giá VND. VND là ĐƠN VỊ của chính BM ⇒ hệ số
       1 là định nghĩa đơn vị, ⛔ tỷ giá gõ cứng. Đây là ngữ nghĩa thứ ba *(`KQ-072` F-5)*, khác
       BO/BP *(đọc cột VND của 9.2 qua INDEX/MATCH — vẫn đòi `fx[tháng]["VND"]` cho dòng VND)*:
       tháng 202502 ⛔ có cột VND mà tồn VND ≠ 0 ⇒ BM vẫn tính.
    """
    (b1,) = tinh_gl([SAU_DONG[0]], {202501: {"USD": D("25500"), "VND": D("1")}})
    assert b1.vnd_ton_all == D("2500000000")                 # BM = BI
    assert _gan(b1.musd_ton_all, "0.0980392156862745098039215686274509")  # BI / 25.500 / 10^6
    fx = {202501: {"USD": D("25500"), "VND": D("1")}, 202502: {"USD": D("25000")}}
    _, k = tinh_gl([SAU_DONG[0], DongGL(thang=202502, tien_te="USD", no=D("1000"), co=D("0"))],
                   fx)
    assert k.vnd_ton_all == D("2525000000")      # 1.000 × 25.000 + 2.500.000.000
    assert k.musd_ton_all == D("0.101")          # (1.000 + 2.500.000.000 / 25.000) / 10^6


# ── H1-R1-06 · `fls/bao_cao` ⛔ chạm kho — cả đường import ĐỘNG ─────────────────────────
# `lint-imports` *(H1-B4)* chỉ thấy import TĨNH: R1 thêm `importlib.import_module("fls.db.kho")`
# vào `gl.py` ⇒ `11 kept` + `18 passed` *(`KQ-072` F-6)*. Hai phép đo bổ nhau:
#   ⓐ HÀNH VI — tiến trình con sạch nạp MỌI mô-đun của `fls.bao_cao`, CHẠY `tinh_gl`, rồi đọc
#     `sys.modules`: bắt cả import động lúc nạp lẫn lúc chạy, kể cả đi vòng qua mô-đun khác;
#   ⓑ NGUỒN — cây cú pháp của `fls/bao_cao/**/*.py` ⛔ có `importlib` / `__import__`: bắt cả
#     đường ⓐ ⛔ chạy tới *(hàm chưa được gọi)*.
_DO_SYS_MODULES = """
import importlib, json, pkgutil, sys
from decimal import Decimal as D
import fls.bao_cao
ten = [m.name for m in pkgutil.walk_packages(fls.bao_cao.__path__, "fls.bao_cao.")]
for t in ten:
    importlib.import_module(t)
import fls.bao_cao.gl as gl
kq = gl.tinh_gl([gl.DongGL(thang=202501, tien_te="VND", no=D("2500000000"), co=D("0"))],
                {202501: {"USD": D("25500"), "VND": D("1")}})
def cam(m):
    return (m.split(".")[0].startswith("psycopg") or m in ("fls.db", "fls.repo")
            or m.startswith(("fls.db.", "fls.repo.")))
print(json.dumps({"cam": sorted(m for m in sys.modules if cam(m)), "mo_dun": ten,
                  "so_kq": len(kq)}))
"""


def test_R1_06_nap_va_chay_fls_bao_cao_khong_keo_tang_kho_vao_sys_modules():
    r = subprocess.run(
        [sys.executable, "-c", _DO_SYS_MODULES],
        cwd=GOC, env={**os.environ, "PYTHONUTF8": "1"},
        capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    assert r.returncode == 0, r.stdout + r.stderr
    do = json.loads(r.stdout.strip().splitlines()[-1])
    # Đ3: phép đo CÓ nhìn thấy engine — đã nạp `gl` và đã CHẠY nó — ⛔ xanh trên tập rỗng
    assert "fls.bao_cao.gl" in do["mo_dun"] and do["so_kq"] == 1, do
    assert do["cam"] == [], do


def test_R1_06_nguon_fls_bao_cao_khong_co_import_dong():
    goc_bc = GOC / "fls" / "bao_cao"
    tep = sorted(goc_bc.rglob("*.py"))
    assert goc_bc / "gl.py" in tep and len(tep) >= 2         # Đ3: `__init__.py` + `gl.py`
    vi_pham: list[str] = []
    so_nut = 0
    for p in tep:
        for n in ast.walk(ast.parse(p.read_text(encoding="utf-8"), filename=str(p))):
            so_nut += 1
            if isinstance(n, ast.Import):
                vi_pham += [f"{p.name}:{n.lineno} import {a.name}" for a in n.names
                            if a.name.split(".")[0] == "importlib"]
            elif isinstance(n, ast.ImportFrom) and (n.module or "").split(".")[0] == "importlib":
                vi_pham.append(f"{p.name}:{n.lineno} from {n.module} import …")
            elif ((isinstance(n, ast.Name) and n.id == "__import__")
                  or (isinstance(n, ast.Attribute) and n.attr == "__import__")):
                vi_pham.append(f"{p.name}:{n.lineno} __import__")
    assert so_nut > 100, so_nut                               # Đ3: cây ⛔ rỗng
    assert vi_pham == [], vi_pham


# ── H1-R1-07 · ghim ngữ cảnh số học: 28 chữ số có nghĩa, nửa-về-chẵn ───────────────────
def test_R1_07_BR_dung_tuyet_doi_o_chu_so_28__prec_28_lam_tron_len():
    """`H1-B1` so mUSD tới 12 chữ số *(`Q12`)* ⇒ đột biến prec 12 · `ROUND_DOWN` SỐNG
    *(`KQ-072` F-7)*. Tính tay: 2,5 ÷ 25.500 × 10^3 = 0,0980392156862745098039215686|27…
    ⇒ chữ số có nghĩa thứ 28 là `2`, thứ 29 là `7` ⇒ làm tròn LÊN ⇒ `…6863`.
    prec 12 ⇒ `0.0980392156863` · `ROUND_DOWN` ⇒ `…6862`. BN *(= BI ÷ USD ÷ 10^6)* và BT
    *(= BR ở dòng đầu)* cùng giá trị ⇒ cùng ghim."""
    (k,) = tinh_gl([SAU_DONG[0]], FX)
    assert str(k.musd_no) == "0.09803921568627450980392156863", k.musd_no          # BR
    assert str(k.musd_ton_all) == "0.09803921568627450980392156863", k.musd_ton_all  # BN
    assert str(k.musd_ton) == "0.09803921568627450980392156863", k.musd_ton          # BT


@pytest.mark.parametrize("no, mong", [
    # N / 10^9 / 2 × 10^3 = N / (2 × 10^6) — 29 chữ số có nghĩa, chữ số cuối = 5 (HOÀ):
    ("2000000000000000000000000001", "1000000000000000000000.000000"),   # …0|5 ⇒ về chẵn 0
    ("2000000000000000000000000003", "1000000000000000000000.000002"),   # …1|5 ⇒ về chẵn 2
], ids=["chu_so_28_chan__xuong", "chu_so_28_le__len"])
def test_R1_07_hoa_o_chu_so_29__lam_tron_nua_ve_chan(no, mong):
    """Phân biệt NỬA-VỀ-CHẴN với nửa-lên *(`ROUND_HALF_UP` hỏng ca 1)* và nửa-xuống
    *(`ROUND_HALF_DOWN` hỏng ca 2)* — bài trên chỉ phân biệt được với `ROUND_DOWN`.
    ⚠ Số TỔNG HỢP, ⛔ thực tế *(2·10^27 VND; tỷ giá USD = 2)*: chỉ để chữ số thứ 29 rơi đúng
    vào `5`. BO = N / 10^9 có 28 chữ số ⇒ đúng tuyệt đối; phép làm tròn duy nhất là ÷ USD."""
    (k,) = tinh_gl([DongGL(thang=202501, tien_te="VND", no=D(no), co=D("0"))],
                   {202501: {"USD": D("2"), "VND": D("1")}})
    assert k.bvnd_no == D(no).scaleb(-9)                     # BO = N / 10^9 đúng tuyệt đối
    assert k.musd_no == D(mong), k.musd_no                   # BR = BO ÷ USD × 10^3
    assert k.musd_ton_all == D(mong), k.musd_ton_all         # BN = BI ÷ USD ÷ 10^6
    assert k.musd_ton == D(mong), k.musd_ton                 # BT = BR (dòng đầu)
