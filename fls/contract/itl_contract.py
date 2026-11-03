"""ITL-CONTRACT — ban SONG la **v1.1** (2026-08-27, CR#2). v1.0 dong bang 2026-08-24.

14 truong, doc THEO TEN. Cot Excel chi de doi chieu reader dang chay.
le = cot P (QD-owner-0820), KHONG phai BL.
Doi file nay la CR loai 3, kem test tuong thich (02_REPO_CONVENTIONS §4.5).
"""

from __future__ import annotations

ITL_CONTRACT_V1: tuple[tuple[str, str, str], ...] = (
    ("doc_date", "date", "A"),
    ("doc_no", "text", "B"),
    ("memo", "text", "C"),
    ("curr", "text", "D"),
    ("ps_no", "numeric", "E"),
    ("ps_co", "numeric", "F"),
    ("acct", "text", "G"),
    ("le", "text", "P"),
    ("itl_id", "bigint", "R"),
    ("hd", "text", "V"),
    ("pay_type", "text", "Z"),
    ("cdt1", "text", "AD"),
    ("svc_start", "date", "AH"),
    ("svc_end", "date", "AL"),
)


# ---------------------------------------------------------------------------
# LECH giua hop dong DA DONG BANG va so THAT. ⛔ Khong sua ITL_CONTRACT_V1.
#
# Hop dong v1.0 dong bang 2026-08-24 (QD-ITL-42) va doi file nay la CR loai 3.
# Nen khi lan nap THAT dau tien (2026-08-26) chung minh hop dong khai SAI kieu,
# duong dung KHONG phai la lang le sua chu 'date' thanh 'text' — ma la ghi cai
# lech ra day, dem duoc, va de owner quyet.
#
# Neu che di thi cai gia phai tra la: hoac `fls_itl` giu kieu `date` va lan nap
# NO tren 9-10 loai gia tri ke toan that su da go, hoac ta am tham "sua lai cho
# dung kieu" nhung chi so va khong con duong quay ve.
LECH_HOP_DONG_V1: tuple[tuple[str, str, str, str], ...] = (
    ("svc_start", "date", "text",
     "do tren 9.967 dong: 39 gia tri, 9 loai KHONG phai YYYYMM — 'thang 5', "
     "'2025.07', 'TPCI', '252512', '2027', '45962'. Va don vi la KY (thang), "
     "nen kieu `date` buoc phai bia mot ngay trong thang ma nguon khong co"),
    ("svc_end", "date", "text",
     "y nhu svc_start: 57 gia tri, 10 loai KHONG phai YYYYMM ('Thang 4', "
     "'20509', '2025.07'…)"),
)

# CR#2 da DONG 2026-08-27 — xem khoi v1.1 o cuoi file.


# ---------------------------------------------------------------------------
# ITL-CONTRACT v1.1 — owner chot 2026-08-27, dong CR#2 phuong an (a).
#
# ⛔ `ITL_CONTRACT_V1` o tren KHONG DOI MOT CHU. Day la ban SONG; ban tren la
# LICH SU. Giu ca hai vi ba ly do:
#   ① cong khoa v1.0 van chay => khong ai lang le sua lich su cho test xanh lai;
#   ② `LECH_V1_V1_1` noi ro DOI CAI GI, kem con so da do — mot ban nang cap
#      khong noi duoc no doi gi la mot ban nang cap khong ai dam tin;
#   ③ du lieu da nap theo v1.0 van truy lai duoc kieu cua no.
#
# Doi: `svc_start`/`svc_end` `date` -> `text`. Ly do do duoc tren 9.967 dong:
# hai cot do la KY (thang) do NGUOI GO, khong phai ngay. 39/57 gia tri khac
# nhau, trong do 9-10 loai KHONG phai `YYYYMM`: 'thang 5' · 'Thang 4' · 'TPCI'
# · '2025.07' · '20509' · '252512' · '2027' · '45962'. Kieu `date` buoc phai bia
# mot ngay trong thang ma nguon khong he co (`INV-I16`).
VERSION_SONG = "v1.1"

ITL_CONTRACT_V1_1: tuple[tuple[str, str, str], ...] = tuple(
    (ten, "text" if ten in ("svc_start", "svc_end") else kieu, cot)
    for ten, kieu, cot in ITL_CONTRACT_V1
)

LECH_V1_V1_1: tuple[tuple[str, str, str, str], ...] = (
    ("svc_start", "date", "text",
     "KY do nguoi go, khong phai ngay: 39 gia tri, 9 loai khong phai YYYYMM"),
    ("svc_end", "date", "text",
     "y nhu svc_start: 57 gia tri, 10 loai khong phai YYYYMM"),
)

# CR#2 DA DONG (2026-08-27, owner chon phuong an (a)).
# ⛔ Phuong an (b) — them mot truong `svc_ky` rieng va giu `svc_start` cho mot
# NGAY that — bi loai vi truong `svc_start` moi do se **khong co nguon du lieu
# nao**: khong cho nao trong nguon mang ngay trong thang. Dung mot cot rong lam
# cho de "sau nay co thi dien" la dung cai luat nay cam (P-ITL-05).
CR_DANG_MO: tuple[str, ...] = ()
