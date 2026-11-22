"""`mong` của cổng `WP-C5b` *(ISP 3.1.2 · Step 44 · H13 · `WO-307`)* — khai TRƯỚC, khác ⇒ ĐỎ CẢ HAI CHIỀU *(Đ5)*.

Nhãn Đ4 *(mỗi số nói nó đếm gì)*:
  · `tong_o` 4.102 = ô DÒNG PL so được: hàng `PL2…PL8` có nhãn của ATL *(80 hàng = 12 khối × 6 dòng + 8 hàng PL5)* × 57
    kỳ, ô là số, IX.PL tính được. = `o_0_0` 2.295 + ô có số 1.807. `khop` 3.179 = khớp THẬT 884 + `o_0_0` 2.295.
  · ngoài mẫu số *(có tên)*: `PL5|PL_THIEU_GIA_TRI` 252 *(ô PL5 có số ở ATL ngoài GROUP × 12 tháng 2025 — ảnh
    `COM_GAG` chỉ có GROUP 2025)* · `o_trong_dap_an` 192 *(ô ATL rỗng — PL5 2024/2026 tháng)* · `khong_so_duoc` 14
    *(`#N/A`/`#VALUE!` của `y2024_y`/`q*`)*.
  · `lop_thua_ke` — 923 ô dòng PL lệch, MỌI ô thừa kế lớp từ lá *(tập lớp NHỎ NHẤT hồi phục ô — phép đo)*; lệch FLS 0.
  · `nhan_c5a` — lớp C5a của CHÍNH ô KPI `PL*` ∈ nhãn thừa kế: 922 trùng · 0 khác · 1 ⛔ có *(GROUP PL5 2025M02 — PL5
    là ô `trong` của `pla`, C5a ⛔ so)*.
  · `hai_dinh_nghia` — IX.PL ↔ KPI `PL*` của `pla.CONG_THUC_PM` *(H8)*: 4.104 ô = 6 dòng × 12 khối × 57 kỳ, chênh 0.
  · `check` — kỳ-KHỐI *(684 = 12 × 57 mỗi phép)*: `dat_co_so` 0 ở CẢ HAI phép *(Đ3: mọi "đạt" là 0 = 0 — trùng DT11
    trên Daily Report)*; 29 kỳ có ≥ 1 khối đỏ; đối chiếu CHECK của ATL: 1.326 khớp + 42 lệch thừa kế `loi_as_is`.
"""
from typing import Any

MONG: dict[str, Any] = {'tong_o': 4102,
 'lop': {'dem': {'hang_pl': 80,
                 'o_so': 4102,
                 'khop_co_so': 884,
                 'o_0_0': 2295,
                 'o_trong_dap_an': 192,
                 'khong_so_duoc': 14,
                 'khop': 3179},
         'khong_tinh': {'PL5|PL_THIEU_GIA_TRI': 252},
         'nhan_c5a': {'trung': 922, 'khac': 0, 'khong_co': 1},
         'hai_dinh_nghia': {'o_so': 4104, 'chenh': 0},
         'check': {'fls': {'NB = 0': {'dat_co_so': 0, 'dat_0_0': 537, 'do': 147, 'khong_do_duoc': 0},
                           'NIS+INT+PIT+COM = CXA+GAH+DC+MC': {'dat_co_so': 0,
                                                               'dat_0_0': 470,
                                                               'do': 214,
                                                               'khong_do_duoc': 0}},
                   'dap_an': {'NB = 0': {'dat_co_so': 0, 'dat_0_0': 537, 'do': 147, 'khong_do_duoc': 0},
                              'NIS+INT+PIT+COM = CXA+GAH+DC+MC': {'dat_co_so': 0,
                                                                  'dat_0_0': 473,
                                                                  'do': 211,
                                                                  'khong_do_duoc': 0}},
                   'so_ky_do': 29,
                   'do_sha256': '8aff172ae42ef1de08b63885b0ed4fbde04e4d9b90de1558aa9a3ff1fabfb012',
                   'doi_chieu_dap_an': {'khop': 1326,
                                        'dap_an_khong_do_duoc': 0,
                                        'lop_thua_ke': {'loi_as_is': 42},
                                        'lech_FLS': 0}}},
 'lop_thua_ke': {'chua_co_dau_vao': {'so_o': 167,
                                     'theo_khoi': {'ASA': 27,
                                                   'CAH': 19,
                                                   'COR': 19,
                                                   'CSM': 19,
                                                   'CVL': 19,
                                                   'SHQ1': 19,
                                                   'SHQ2': 45},
                                     'sha256': '2b6dcc764d7709db35077144d8ccb90537eb8caa0398948ba51d5ff59c41e533'},
                 'chua_co_dau_vao+lech_D3': {'so_o': 600,
                                             'theo_khoi': {'ASA': 80,
                                                           'CAH': 95,
                                                           'COR': 95,
                                                           'CSM': 95,
                                                           'CVL': 95,
                                                           'SHQ1': 95,
                                                           'SHQ2': 45},
                                             'sha256': '1bbae5017cd456d49773fe8352b2767e50175ae394d26ecf2fb66b4e0d0605cf'},
                 'chua_co_dau_vao+lech_D3+loi_as_is': {'so_o': 15,
                                                       'theo_khoi': {'SHQ2': 15},
                                                       'sha256': 'd3e8287678fbc512bb288661782d619c4425b30ebe58af040af936ad365f0212'},
                 'chua_co_dau_vao+loi_as_is': {'so_o': 9,
                                               'theo_khoi': {'SHQ2': 9},
                                               'sha256': '8231cf8c6ad5e4123fca86ded2194549b2fe3179e75384495975304635acc2a3'},
                 'loi_as_is': {'so_o': 132,
                               'theo_khoi': {'ASA': 8,
                                             'CAH': 13,
                                             'COR': 13,
                                             'CSM': 13,
                                             'CVL': 13,
                                             'GROUP': 25,
                                             'SGO1': 21,
                                             'SHQ1': 13,
                                             'SHQ2': 13},
                               'sha256': '34bcbc74738002476ad4995799154c789af0b1dc26aba1392769a5ff5eeb80a2'}}}
