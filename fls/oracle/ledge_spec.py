"""Khuon `ITL Ledge` — 64 cot A..BL, va TUNG cot DI DAU trong kho du lieu.

★ Vi sao file nay ton tai. Cau hoi cua owner 2026-08-26: *"cac entity/table nay
da co du schema nhu ggsheet chua?"* — truoc file nay khong ai tra loi duoc bang
may. Phai mo hai thu ra so bang mat, va so bang mat thi truot.

Nay moi cot cua sheet phai khai **di dau**: hoac ten cot trong `fls_itl`, hoac
mot LY DO BANG CHU tai sao khong luu. `tests/oracle/test_ledge_schema.py` cham:
  ⓐ du 64 cot, khong trung chu cai
  ⓑ moi dich la cot CO THAT trong `fls_itl` (doi chieu `fls.db.schema`)
  ⓒ khong cot nao "khong luu" ma thieu ly do
⇒ Them cot vao sheet ma quen khai => cong DO. Doi ten cot DB => cong DO.

⚠ HAI HE TOA DO: chu cai o day la cua `ITL Ledge` (dau ra, 64 cot). `ITL-CANON`
(dau vao, 38 vi tri) cung dung A..AL nhung Y NGHIA KHAC. Xem `canon/spec.py`.
"""

from __future__ import annotations

from dataclasses import dataclass

K = "KHONG LUU: "     # DA QUYET khong luu — bat buoc kem ly do
Q = "CHUA QUYET: "    # CHUA co quyet dinh — bat buoc kem CAU HOI cho owner

# Cau dan dung cho ba cot vung ALLOCATE — mot cho khai duy nhat.
CT = ("Owner dua NGUYEN VAN cong thuc 2026-08-28 ⇒ suy lai duoc 100%: "
      "xem `fls/ledger/allocate.py` (SSOT cua phep suy). ")

# ★ Vi sao co HAI tien to. Neu chi co `K` thi moi cot chua quyet phai bi nhet
# vao "khong luu" — va mot cau hoi chua tra loi se bien thanh mot quyet dinh
# ngam. Do dung la cach tai lieu du an nay tung gia di trong im lang. Tach ra
# thi cong dem duoc: co bao nhieu cau hoi dang treo, va co cai nao MOI len ma
# khong ai thay.


@dataclass(frozen=True)
class LedgeCol:
    letter: str
    name: str
    di_dau: str        # ten cot fls_itl, HOAC bat dau bang K + ly do

    @property
    def luu(self) -> bool:
        return not (self.di_dau.startswith(K) or self.di_dau.startswith(Q))


_T: tuple[tuple[str, str, str], ...] = (
    # ---- vung GOC (chep tu ITL-CANON) ----
    ("A", "Ngày chứng từ", "doc_date"),
    ("B", "Số chứng từ", "doc_no"),
    ("C", "Diễn giải", "memo"),
    ("D", "Đơn vị tiền tệ", "curr"),
    ("E", "PS Nợ", "ps_no"),
    ("F", "PS Có", "ps_co"),
    ("G", "Tài khoản", "acct"),
    ("H", "Loại giao dịch (Payment Type)", K + "gia tri THO tu canon; ban chot "
     "nam o Final khoi 2 (cot Z). Con nguyen trong `canon` jsonb"),
    ("I", "Budget Code (HDCode)", K + "gia tri THO; ban chot o Final khoi 1 (V)"),
    ("J", "Chủ dự toán (CDT1)", K + "gia tri THO; ban chot o Final khoi 3 (AD)"),
    ("K", "Thời điểm bắt đầu sử dụng dịch vụ", K + "gia tri THO; chot o AH"),
    ("L", "Thời điểm kết thúc sử dụng dịch vụ", K + "gia tri THO; chot o AL"),
    ("M", "Mã đối tác (ID Payee)", K + "gia tri THO; chot o AP"),
    ("N", "File đính kèm: Hóa đơn", K + "gia tri THO; chot o AT"),
    ("O", "File đính kèm: Khác", K + "KHONG MAT: gia tri tho da nam nguyen "
     "trong `canon` jsonb vi tri 30 (canon `AE`). Va khong man hinh nao dung "
     "no — `06_SCREEN_SPEC` chi noi 'Dinh kem hoa don'. Can den thi lay tu "
     "canon, khong phai them cot"),
    ("P", "LE", "le"),
    ("Q", "No", K + "so thu tu dong tren bang da SORT — KHONG ben (INV-I04a). "
     "Danh tinh la itl_id do SEQUENCE cap"),
    ("R", "ITL ID", "itl_id_sheet"),
    # ---- vung ADJUSTMENT · 7 khoi x 4 cot ----
    ("S", "Budget Code · Classifying", K + "suy lai duoc: Classifying = iferror(canon S, \'Need to manual input\'). "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("T", "Budget Code · Manual input", K + "o NGUOI GO. Thong tin cua no da nam "
     "trong `hd_thyt` (NULL khi may tu bia) — QD-ITL-35"),
    ("U", "Budget Code · MID", K + "buoc TRUNG GIAN cua luat hai buoc; Final = f(Classifying, MID) nen suy lai duoc tu Classifying + o nguoi go"),
    ("V", "Budget Code · Final", "hd"),
    ("W", "Loại giao dịch · Classifying", K + "suy lai duoc: Classifying = iferror(canon H, \'Need to manual input\'). "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("X", "Loại giao dịch · Manual input", K + "o NGUOI GO — xem `pay_type_thyt`"),
    ("Y", "Loại giao dịch · MID", K + "buoc TRUNG GIAN, suy lai duoc — xem cot MID khoi 1 (U)"),
    ("Z", "Loại giao dịch · Final", "pay_type"),
    ("AA", "Chủ dự toán · Classifying", K + "suy lai duoc: Classifying = iferror(canon T, \'Need to manual input\'). "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("AB", "Chủ dự toán · Manual input", K + "o NGUOI GO — xem `cdt1_thyt`"),
    ("AC", "Chủ dự toán · MID", K + "buoc TRUNG GIAN, suy lai duoc — xem cot MID khoi 1 (U)"),
    ("AD", "Chủ dự toán · Final", "cdt1"),
    ("AE", "Bắt đầu DV · Classifying", K + "suy lai duoc: Classifying = iferror(canon AB, \'Need to manual input\') — ⚠ ⛔ KHONG phai canon W: hai cot TRUNG TEN y het, va W la cap 100% #N/A CO CHU Y (QD-ITL-51); lay sai thi ca so thanh \'Need to manual input\' ma khong cong nao do, do duoc 70,4114%. "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("AF", "Bắt đầu DV · Manual input", K + "o NGUOI GO — xem `svc_start_thyt`"),
    ("AG", "Bắt đầu DV · MID", K + "buoc TRUNG GIAN, suy lai duoc — xem cot MID khoi 1 (U)"),
    ("AH", "Bắt đầu DV · Final", "svc_start"),
    ("AI", "Kết thúc DV · Classifying", K + "suy lai duoc: Classifying = iferror(canon AC, \'Need to manual input\') — ⚠ ⛔ KHONG phai canon X (xem cot AE). "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("AJ", "Kết thúc DV · Manual input", K + "o NGUOI GO — xem `svc_end_thyt`"),
    ("AK", "Kết thúc DV · MID", K + "buoc TRUNG GIAN, suy lai duoc — xem cot MID khoi 1 (U)"),
    ("AL", "Kết thúc DV · Final", "svc_end"),
    ("AM", "Mã đối tác · Classifying", K + "suy lai duoc: Classifying = iferror(canon Y, \'Need to manual input\'). "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("AN", "Mã đối tác · Manual input", K + "CONG THUC sinh co 'Input here', "
     "khong phai nguoi go — xem `id_payee_thyt`"),
    ("AO", "Mã đối tác · MID", K + "buoc TRUNG GIAN, suy lai duoc — xem cot MID khoi 1 (U)"),
    ("AP", "Mã đối tác · Final", "id_payee"),
    ("AQ", "Hoá đơn · Classifying", K + "suy lai duoc: Classifying = iferror(canon AD, \'Need to manual input\'). "
     "DA DO tren du lieu that: 9.845 dong x 7 khoi = 68.915 o KHOP 100,0000% — fls/ledger/classifying.py. "
     "⚠ o RONG giu RONG, ⛔ khong thanh 'Need to manual input' (bien the do sai 1.490 o o khoi invoice)"),
    ("AR", "Hoá đơn · Manual input", K + "CONG THUC sinh co 'Input here' — "
     "xem `invoice_thyt`"),
    ("AS", "Hoá đơn · MID", K + "buoc TRUNG GIAN, suy lai duoc — xem cot MID khoi 1 (U)"),
    ("AT", "Hoá đơn · Final", "invoice"),
    # ---- vung ALLOCATE ----
    #
    # ⛔⛔ Vung nay la NGOAI LE cua khuon, va owner da chi ra 2026-08-28.
    # Bay khoi ADJUSTMENT deu co **bon** cot mot khoi:
    #       Classifying · Manual input · MID · Final
    # (vd Ma doi tac AM/AN/AO/AP · Hoa don AQ/AR/AS/AT — `Final` la cho luu).
    # Vung ALLOCATE chi co **BA** cot, va chung ⛔ KHONG theo khuon do:
    #       AU = "Chu du toan (CDT1) CFA1"   (⛔ khong co nhan phu)
    #       AV = "Chu du toan (CDT1) CFA2"  ->  nhan phu "Classifying"
    #       AW = (⛔ khong co nhan tren)     ->  nhan phu "Method"
    #
    # ⇒ **CFA2 ⛔ KHONG co cot `Final`.** Nen cau hoi that la: gia tri NGUOI SUA
    # cat o dau? Hai kha nang, va chung khac nhau ve ke toan:
    #   ⓐ ke toan **ghi de len chinh AV** ⇒ mot o vua la goi y vua la gia tri
    #     chot ⇒ tu do ⛔ khong phan biet duoc "may suy dung" voi "nguoi da sua"
    #   ⓑ co mot cho khac ma toi chua thay
    # ⛔ Toi ⛔ KHONG chon giup: do la cach lam viec that cua ke toan
    # (`GAP-ALLOC-01`).
    #
    # ⚠ Va ba dong duoi day ⛔ CHUA duoc xac nhan tu NGUON SONG: doc so
    # ADJUSTED 2026-08-28 that bai (185s roi loi, 3 lan). Chung dua tren anh
    # chup cua owner + ban khai nay, ⛔ khong phai mot phep do.
    # ⭐⭐ 2026-08-28: owner dua NGUYEN VAN ba cong thuc, va chung lat mo hinh:
    #   AU = ArrayFormula(AD7:AD)                       <- BAN SAO cua `AD`=cdt1
    #   AV = if(VLOOKUP(V, MM!H:K, 2, FALSE) = "Need to Allocate to CFA2",
    #           "Need to Allocate to CFA2", AU)
    #   AW = if(VLOOKUP(V, MM!H:L, 2, FALSE) <> "", VLOOKUP(...), "No need")
    # ⇒ Ca ba SUY LAI DUOC tu `cdt1` + `hd` (=V) + `Mapping Master` cot K/L.
    #   Quyet dinh phan bo ⛔ KHONG nam o so nay — no nam o **Mapping Master**.
    ("AU", "Chủ dự toán CFA1", K + CT
     + "AU la BAN SAO cua `AD` (=`cdt1`) ⇒ luu them mot cot la HAI BAN SU THAT "
       "cho cung mot gia tri (dung benh `=L130` cua so P100)."),
    ("AV", "Chủ dự toán CFA2 · Classifying", K + CT
     + "AV = co `Need to Allocate to CFA2` (tu `Mapping Master!K` theo `hd`) "
       "hoac roi ve AU. ⛔ No TRON CO voi GIA TRI trong mot o."),
    ("AW", "Method", K + CT
     + "AW = `Mapping Master!L` theo `hd`, hoac `No need`. ⛔ Cung tron CO voi "
       "GIA TRI. ⚠ Bay: o RONG that thi VLOOKUP cua Sheets tra `0` nen o nay "
       "hien `0`, ⛔ khong phai `No need`."),
    # ---- vung AUDIT · 6 phep kiem, moi phep 2 cot (VALUE + FALSE=n) ----
    ("AX", "AUDIT · ITL ID", K + "KET QUA cua mot phep so voi `Report I General Ledger`. Owner chot 2026-08-26 (QD-ITL-52): so do la ban THUONG NGUON, mang gia tri TRUOC khi ke toan sua; ban FINAL la chinh `ITL Ledge` nay. ⇒ Lech o sau cot do la DIEU MONG DOI, khong phai loi — no do KHOI LUONG DA SUA, khong do cai gi sai. ⛔ Luu vao `fls_itl` la bien mot con so binh thuong thanh mot bao dong thuong truc. Va FLS thay CA HAI so bang MOT kho nen cho do trot khong con ton tai"),
    ("AY", "AUDIT · ITL ID · FALSE", K + "o dem tong cua sheet, khong phai du "
     "lieu dong. Dem lai duoc tu `audit_*`"),
    ("AZ", "AUDIT · HD CODE", K + "KET QUA cua mot phep so voi `Report I General Ledger`. Owner chot 2026-08-26 (QD-ITL-52): so do la ban THUONG NGUON, mang gia tri TRUOC khi ke toan sua; ban FINAL la chinh `ITL Ledge` nay. ⇒ Lech o sau cot do la DIEU MONG DOI, khong phai loi — no do KHOI LUONG DA SUA, khong do cai gi sai. ⛔ Luu vao `fls_itl` la bien mot con so binh thuong thanh mot bao dong thuong truc. Va FLS thay CA HAI so bang MOT kho nen cho do trot khong con ton tai"),
    ("BA", "AUDIT · HD CODE · FALSE", K + "o DEM TONG cua sheet, khong phai du lieu cua dong nao. Dem lai duoc sau khi co cac cot audit"),
    ("BB", "AUDIT · Loại Giao dịch", K + "KET QUA cua mot phep so voi `Report I General Ledger`. Owner chot 2026-08-26 (QD-ITL-52): so do la ban THUONG NGUON, mang gia tri TRUOC khi ke toan sua; ban FINAL la chinh `ITL Ledge` nay. ⇒ Lech o sau cot do la DIEU MONG DOI, khong phai loi — no do KHOI LUONG DA SUA, khong do cai gi sai. ⛔ Luu vao `fls_itl` la bien mot con so binh thuong thanh mot bao dong thuong truc. Va FLS thay CA HAI so bang MOT kho nen cho do trot khong con ton tai"),
    ("BC", "AUDIT · Loại Giao dịch · FALSE", K + "o DEM TONG cua sheet, khong phai du lieu cua dong nao. Dem lai duoc sau khi co cac cot audit"),
    ("BD", "AUDIT · PL Time start", K + "KET QUA cua mot phep so voi `Report I General Ledger`. Owner chot 2026-08-26 (QD-ITL-52): so do la ban THUONG NGUON, mang gia tri TRUOC khi ke toan sua; ban FINAL la chinh `ITL Ledge` nay. ⇒ Lech o sau cot do la DIEU MONG DOI, khong phai loi — no do KHOI LUONG DA SUA, khong do cai gi sai. ⛔ Luu vao `fls_itl` la bien mot con so binh thuong thanh mot bao dong thuong truc. Va FLS thay CA HAI so bang MOT kho nen cho do trot khong con ton tai"),
    ("BE", "AUDIT · PL Time start · FALSE", K + "o DEM TONG cua sheet, khong phai du lieu cua dong nao. Dem lai duoc sau khi co cac cot audit"),
    ("BF", "AUDIT · PL Time end", K + "KET QUA cua mot phep so voi `Report I General Ledger`. Owner chot 2026-08-26 (QD-ITL-52): so do la ban THUONG NGUON, mang gia tri TRUOC khi ke toan sua; ban FINAL la chinh `ITL Ledge` nay. ⇒ Lech o sau cot do la DIEU MONG DOI, khong phai loi — no do KHOI LUONG DA SUA, khong do cai gi sai. ⛔ Luu vao `fls_itl` la bien mot con so binh thuong thanh mot bao dong thuong truc. Va FLS thay CA HAI so bang MOT kho nen cho do trot khong con ton tai"),
    ("BG", "AUDIT · PL Time end · FALSE", K + "o DEM TONG cua sheet, khong phai du lieu cua dong nao. Dem lai duoc sau khi co cac cot audit"),
    ("BH", "AUDIT · ID Vendor", K + "KET QUA cua mot phep so voi `Report I General Ledger`. Owner chot 2026-08-26 (QD-ITL-52): so do la ban THUONG NGUON, mang gia tri TRUOC khi ke toan sua; ban FINAL la chinh `ITL Ledge` nay. ⇒ Lech o sau cot do la DIEU MONG DOI, khong phai loi — no do KHOI LUONG DA SUA, khong do cai gi sai. ⛔ Luu vao `fls_itl` la bien mot con so binh thuong thanh mot bao dong thuong truc. Va FLS thay CA HAI so bang MOT kho nen cho do trot khong con ton tai"),
    ("BI", "AUDIT · ID Vendor · FALSE", K + "o DEM TONG cua sheet, khong phai du lieu cua dong nao. Dem lai duoc sau khi co cac cot audit"),
    # ---- duoi so ----
    ("BJ", "PIC", "pic"),
    ("BK", "Trạng thái", "work_status"),
    ("BL", "ENITY", K + "cot KHONG tieu de, VLOOKUP suy ra, TRONG 60% dong. "
     "Owner chot dung cot P lam SSOT (QD-owner-0820)"),
)

LEDGE_COLS: tuple[LedgeCol, ...] = tuple(LedgeCol(*x) for x in _T)
SO_COT = len(LEDGE_COLS)                                     # 64

COT_LUU: tuple[LedgeCol, ...] = tuple(c for c in LEDGE_COLS if c.luu)
COT_KHONG_LUU: tuple[LedgeCol, ...] = tuple(
    c for c in LEDGE_COLS if c.di_dau.startswith(K))
COT_CHUA_QUYET: tuple[LedgeCol, ...] = tuple(
    c for c in LEDGE_COLS if c.di_dau.startswith(Q))

# So cau hoi dang treo. Khai ra de mot cau hoi MOI khong len duoc trong im lang.
SO_CHUA_QUYET = 0

# ⛔⛔ Truong NGUOI GO DUOC ma ⛔ KHONG co cot nao trong khuon `ITL Ledge` tro
# tao. Khai ra de no ⛔ khong nam im: mot truong cho nguoi go ma khong co nguon
# la mot truong ⛔ khong ai doi chieu duoc. Moi muc PHAI kem CAU HOI.
# Co cong khoa: `tests/oracle/test_truong_ghi_co_nguon.py`.
CHUA_NOI: dict[str, str] = {
    # ⭐ RONG tu 2026-08-28 (`QĐ-ITL-64`): ba truong vung ALLOCATE da ra khoi
    # `TRUONG_GHI` vi owner tra loi *"ho ko sua"*. Con lai bay truong, va ca
    # bay deu co DUNG MOT cot nguon.
    # ⛔ Giu cai `dict` nay chu ⛔ khong xoa: mot truong ghi MOI ma khong co
    # nguon thi cong `tests/oracle/test_truong_ghi_co_nguon.py` se doi khai o
    # day — do la cho de khai.
}

# ⛔ Cot khai trong `fls_itl` ma ⛔ khong chu cai nao tro tao (nguoc chieu voi
# `CHUA_NOI`): mot cot khai ma khong noi thi no se mai mai rong.
CHUA_NOI_NGUOC: dict[str, str] = {
    # ⭐ RONG tu 2026-08-28 (`QĐ-ITL-65`): nam cot vung ALLOCATE da BI BO khoi
    # `fls_itl` (migration `0012`) — chung suy lai duoc va ⛔ khong ai go.
    # ⛔ Giu `dict` nay: mot cot MOI khai ma khong co chu cai nao tro tao thi
    # cong `tests/oracle/test_truong_ghi_co_nguon.py` se doi khai o day.
}


def dich_cua(letter: str) -> str:
    for c in LEDGE_COLS:
        if c.letter == letter.upper():
            return c.di_dau
    raise ValueError(f"cot {letter!r} khong thuoc khuon ITL Ledge")
