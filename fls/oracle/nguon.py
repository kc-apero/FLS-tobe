"""Khai bao NGUON doc — DU LIEU thuan, khong logic.

Khai o mot cho de doi nguon la doi mot dong, va de co test khoa dia chi.

★ QD-ITL-50 (owner, 2026-08-26, nguyen van "ban sao nay la y chang ban goc, song"):
  dau vao ITL-CANON lay tu BAN SAO RAW `1md85t...`, ⛔ khong phai file goc
  (file goc tra HTTP 403). Day KHONG phai "ban sao thi dung duoc" — xem
  `11_ORACLE_READ_SPEC` v1.2 §"vi sao ban sao RAW duoc ma ban sao ADJUSTED khong":
  `ITL Ledge` khi phu thuoc dut thi `iferror` bat co `Input here` roi `MID` nhan
  MOT HANG MAC DINH (0 o loi, sai ~5.000 dong im lang); `Transaction Mapping L1`
  thi GIU NGUYEN `#N/A` — do 26/08: 6.648 o `#N/A` duoc bao toan, ty le ghep
  33,5% trung khit 33,8% da do doc lap.

⚠ `dong_dau` cua RAW la **5**, ⛔ khong phai 4. Header o dong 3, **dong 4 TRONG**.
  Spec v1.0 tung ghi 4 — off-by-one nay lam roi 1 dong trong im lang.
"""

from __future__ import annotations

from dataclasses import dataclass

from fls.canon.spec import CANON_COLS, pos_of


@dataclass(frozen=True)
class Nguon:
    ma: str
    spreadsheet_id: str
    sheet: str
    dong_dau: int
    can_cu: str


BAN_SAO_RAW = Nguon(
    ma="RAW",
    spreadsheet_id="1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E",
    sheet="Transaction Mapping L1",
    dong_dau=5,
    can_cu="QD-ITL-50 — owner chot ban sao song; giu nguyen #N/A nen khong bia",
)

SO_GOC_ADJUSTED = Nguon(
    ma="ADJUSTED",
    spreadsheet_id="1r4WemIbazqYQLtin6FbUn3VghIi3WiskjhAtMGk1yXA",
    sheet="ITL Ledge",
    dong_dau=10,
    can_cu="QD-ITL-49 — nguon `Manual input` 7 khoi, doc tu FILE GOC",
)

# ⛔ Bon thu tuyet doi khong mo. Moi cai da sap mot lan — ly do la BANG CHUNG,
# khong phai canh bao chung chung.
CAM_MO: dict[str, str] = {
    "[Master] ITL_Ledge_raw.xlsx":
        "~84 dong MAT MA (ITL# tro) lam boc hoi 19,9 ty ma tong VAN tu khop",
    "1Pqg_G81xQKKP-tyR8IFFcnaimT2oZ22e-Tq_mewxbN0":
        "ban sao ADJUSTED ngoai kiem soat (dungtt1@); TU SAN XUAT gia tri mac dinh "
        "voi 0 o loi => nguy hon #REF!: ai kiem theo AUD-5 se ket luan 'sach'",
    "ITL_altered":
        "sai 680 HD + 1.048 CDT; QD-ITL-36 loai khoi vai tham chieu",
    "*.xlsx xuat offline":
        "chi 2,7% o ngay con nguyen kieu (4.117 hoan · 5.369 mat kieu · 38 roi)",
}

# ---------------------------------------------------------------------------
# Ba tap cot — PHU KIN 38 vi tri, KHONG chong nhau (co test khoa ca hai dieu).
# Chia theo dung mot cau hoi: "o loi o day nghia la gi?"
# ---------------------------------------------------------------------------

# Cot goc tu `Transaction Original` + `Master Mapping`: o loi = LOI THAT
# => vao fls_reject voi ly do CO TEN (ACC-4). Do 26/08: A/G 100% · B 98,9%
# · C 99,9% (7 o loi that) · D 99,9% · AG 99,9% · AL 99,9%.
COT_LOI_LA_LOI_THAT: frozenset[int] = frozenset(
    {pos_of(c) for c in ("A", "B", "C", "D", "E", "F", "G", "AG", "AL")})

# R-ORA-07c: Z/AA rong, khong tieu de, khong cong thuc => KHONG doc.
# Van giu du 38 vi tri: cho trong CUNG LA mot vi tri (khuyet tat #3 cua khuon).
COT_RONG_CO_Y: frozenset[int] = frozenset(
    c.pos for c in CANON_COLS if not c.name)

# R-ORA-07a: nua mapping — `#N/A` la CAU TRA LOI ("chua ghep"), ⛔ khong phai loi
# => trong CO KIEM SOAT (NULL), ⛔ khong fls_reject, ⛔ khong tinh "sai kieu".
COT_DUOC_PHEP_NA: frozenset[int] = frozenset(
    c.pos for c in CANON_COLS
    if c.pos not in COT_LOI_LA_LOI_THAT and c.pos not in COT_RONG_CO_Y)

# ---------------------------------------------------------------------------
# QD-ITL-51 — bai hoc dat nhat cua ngay 26/08.
# W/X va AB/AC khac nhau o KHOA, ⛔ KHONG o bang tra. Ca bon deu tra PI_Unpivot.
# May do tung lay "nhan dong 2 khai PE nhung cong thuc tra PI" lam bang chung
# loi, roi bao GAP-ORA-07. Owner: day la CHU Y THIET KE. Nhan dong 2 chi la
# nhan NHOM cot, ⛔ khong phai khai bao nguon cua tung cot.
# ---------------------------------------------------------------------------
BANG_TRA_SVC: dict[int, str] = {
    pos_of("W"): "[Importrange]PI_Unpivot",
    pos_of("X"): "[Importrange]PI_Unpivot",
    pos_of("AB"): "[Importrange]PI_Unpivot",
    pos_of("AC"): "[Importrange]PI_Unpivot",
}

# Khoa ghep: W/X theo duong LENH CHI (ID PELine, cot P) — do duoc 0%, la trang
# thai DUNG ("dong nay chua co hoa don xac nhan thoi gian dich vu").
# AB/AC theo duong HOA DON (ID PILine, cot R) — do duoc 23,7%.
KHOA_SVC: dict[int, int] = {
    pos_of("W"): pos_of("P"),
    pos_of("X"): pos_of("P"),
    pos_of("AB"): pos_of("R"),
    pos_of("AC"): pos_of("R"),
}

# R-ORA-07d: ⛔ khong dat nguong cong tren W/X — 0% khong phai bat thuong.
CAM_DAT_NGUONG: frozenset[int] = frozenset({pos_of("W"), pos_of("X")})
