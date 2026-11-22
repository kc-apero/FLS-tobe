"""`MONG` của WP-C3d *(H8 · `WO-277`)* — khai TRƯỚC, sinh tay từ phép đo 22/11 *(Đ5: khác ⇒ ĐỎ cả hai chiều)*.

Đ4 — mỗi số đếm gì:
  · `lop.gl`: hàng ảnh `gl_pl_dau_vao` *(7.883)* · `thieu_D` 6 *(D rỗng ⇒ ⛔ vào `tinh_gl`)* · `AH_RONG` 309 *(AS-IS
    `DE = #NUM!`)* · `AH_LA` = 8 hàng sheet *(`DT7B-R1-01`: serial 45962 ×2 · tháng 27/14 · `yymmdd` ×4)* ·
    `de_lech` = hàng mà ngày C6 ≠ cột `DE` của sổ *(0 = D4 A tái lập đúng)* · `br_lech` = hàng `tinh_gl` ≠ BR/BS sổ ·
    `dong_ngoai_cay` 51 *(V rỗng ×2 + nhãn ⛔ là nút cây ×49 — gồm 2 biến thể `ITE`)* · `dong_ngoai_truc` = dòng
    có ngày ghi nhận ngoài trục `2024-10-21 … 2026-02-27` *(AS-IS SUMIFS cũng bỏ)*.
  · `lop.hr`: hàng `hr_pl_dau_vao` 13.356 · `ba_bb_rong` 2.571 *(A rỗng ⇒ BA/BB rỗng ⇒ góp 0)* · `bm_lech` = ngày
    C6 ≠ `BM` sổ.
  · `lop.tab.<t>`: `o_so` = ô la+tong × khối đo được × cột trên trục · `o_so_kpi` = ô 17 KPI *(tách)* · `o_0_0` ·
    `chua_co_dau_vao` = ô đáp án ≠ 0 ở khối CHƯA có khoá đầu vào · `cot_ngoai_truc` = ô ≠ 0 ở cột 2024-10-20 *(NPC)* ·
    `trong_khac_0` = ô `trong` ≠ 0.
  · `khong_so_duoc` = 46.398 = 11 khối × 74 mã × 57 kỳ *(417 chỉ GROUP)*.
  · `tu_kiem_*` *(GROUP — ô mà PM+HR ≠ PM + HR theo khoá)*: ĐÁP ÁN Daily thường **4** *(AS-IS — 416 `GAC` thiếu
    `CXA`)* · KPI Daily 505 · Y/H/Q/M thường 0 · KPI 206; ENGINE thường 0 · KPI 505/206 *(KPI cấu trúc — dấu HR
    ngược, NPC — ⛔ lỗi)*.
  · `o_lech`: 8 ô `pla3_hr_daily` GROUP — engine theo cây IX.HD *(GAC = Σ 10 con, có `CXA`)*, đáp án 416
    `=sum(G24,…,G31,G33)` THIẾU `G32` *(CXA)* ⇒ GAC · NCFO · COO · NCF lệch ở 2024-11-01 · 2024-12-01.
"""
MONG = {
    "den": "2026-02-27",          # ngày cuối trục = cột cuối của lưới AS-IS 414/416/418 (496 cột, DT7) — NPC hậu tố cần
    "tong_o": 258888,             # Σ ô so 6 tab = thường 192.400 + KPI 66.488 (đo 22/11 — xem lop.tab)
    "atol_lech": "1e-9",
    "o_lech": {
        "pla3_hr_daily|GROUP#GAC#45597": ("-0.10621767589801757602467", "-0.08978994140086179"),
        "pla3_hr_daily|GROUP#GAC#45627": ("-0.14043221151168833934897", "-0.10779161576274277"),
        "pla3_hr_daily|GROUP#NCFO#45597": ("0.00567299978484214516083", "0.022100734281998005"),
        "pla3_hr_daily|GROUP#NCFO#45627": ("0.01603053400645960244633", "0.048671129755405294"),
        "pla3_hr_daily|GROUP#NCF#45597": ("0.00486991482838516706683", "0.021297649325541027"),
        "pla3_hr_daily|GROUP#NCF#45627": ("0.01456395112446540941633", "0.0472045468734111"),
        "pla3_hr_daily|GROUP#COO#45597": ("0.00567299978484214516083", "0.022100734281998005"),
        "pla3_hr_daily|GROUP#COO#45627": ("0.01603053400645960244633", "0.048671129755405294"),
    },
    "lop": {
        "gl": {"vao": 7883, "thieu_D": 6, "AH_RONG": 309,
               "AH_LA": [669, 5487, 5556, 5557, 5634, 5712, 6230, 7098],
               "de_lech": 0, "br_lech": 0, "vao_engine": 7560, "dong_ngoai_cay": 51, "dong_nhan_cha": 0,
               "dong_ngoai_truc": 922, "dong_khac_hoa": 0},
        "hr": {"vao": 13356, "BK_RONG": 0, "AH_LA": 0, "bm_lech": 0, "ba_bb_rong": 2571, "vao_engine": 13356,
               "dong_ngoai_cay": 0, "dong_nhan_cha": 0, "dong_ngoai_truc": 0, "dong_khac_hoa": 0},
        "truc": ["2024-10-21", "2026-02-27", 495],
        "tab": {
            "pla1_daily": {"o_so": 123750, "o_so_kpi": 42075, "o_0_0": 161553, "chua_co_dau_vao": 5417,
                           "cot_ngoai_truc": 5, "trong_khac_0": 0},
            "pla3_hr_daily": {"o_so": 24750, "o_so_kpi": 8415, "o_0_0": 32892, "chua_co_dau_vao": 4457,
                              "cot_ngoai_truc": 0, "trong_khac_0": 0},
            "pla3_pm_hr_daily": {"o_so": 24750, "o_so_kpi": 8415, "o_0_0": 31868, "chua_co_dau_vao": 9056,
                                 "cot_ngoai_truc": 1, "trong_khac_0": 0},
            "pla1_yhqm": {"o_so": 14250, "o_so_kpi": 4845, "o_0_0": 15113, "chua_co_dau_vao": 4862,
                          "cot_ngoai_truc": 0, "trong_khac_0": 0},
            "pla3_hr_yhqm": {"o_so": 2850, "o_so_kpi": 969, "o_0_0": 3333, "chua_co_dau_vao": 0,
                             "cot_ngoai_truc": 0, "trong_khac_0": 0},
            "pla3_pm_hr_yhqm": {"o_so": 2850, "o_so_kpi": 969, "o_0_0": 2240, "chua_co_dau_vao": 8146,
                                "cot_ngoai_truc": 0, "trong_khac_0": 0},
        },
        "khong_so_duoc": 46398,
        "tu_kiem_dap_an": {"daily": {"thuong": 4, "kpi": 510}, "yhqm": {"thuong": 0, "kpi": 206}},
        "tu_kiem_engine": {"daily": {"thuong": 0, "kpi": 505}, "yhqm": {"thuong": 0, "kpi": 206}},
    },
}
