# BG-189 — bàn giao `WO-188`

| | |
|---|---|
| **Thuộc** | `WO-188` (ISP 3.1.2 · Step 20 · H6 — SO Y/H/Q/M theo IX.PER, cổng WP-C3b) |
| **Phát bởi** | `fls-dev` làn BE-HC · 2026-11-18 |
| **Nhận** | `fls-test` (R1 → `KQ-190`) |
| **Commit** | `claude/bold-galileo-zukpaf-isp/H6` @ `3418203` *(mã + bài + `hd2_cong.json`)* + commit BG này |

## Cách sheet 410 cuộn *(SA chỉ-đọc, `FORMULA`, 18/11 — ⛔ đoán)*
- `Report I CFA1 Y H Q M` ô lá = `SUMIFS('Report I CFA1 Daily'!$G8:8, Daily!$G$1:$1, năm[, Daily!$G$2:$2 | $3:$3 | $4:$4, H|Q|M])`; ô cha = `=sum(con)`; AR/CP1.1/CP1.2/CP2/CP3 = `"-"`.
- Tiêu đề Daily: `Year=YEAR(G5)` · `Half=if(G4<7,"H1","H2")` · `Quarter=if(G4<4,"Q1",…)` · `Month=MONTH(G5)`; `G5 = 45585` *(20/10/2024)*, `H5 = G5+1` ⇒ năm của **chính ngày** = `ky.ky_cua`.

## Đã đổi
| Tệp | Vì sao |
|---|---|
| `fls/bao_cao/cfa.py` | `truc_ngay(lich IX.PER, den)` · `cuon_ky(daily, cay, ngay, khoi)` *(Σ Daily theo `ky_cua`; năm = năm của trục; ô thiếu ⇒ `KeyError`, ⛔ hoá 0)* · `ky_khong_ngay` *(kỳ 0 ngày trên trục — errata ㉑)*; docstring `cfa1_daily` bỏ "ngày đầu tạm" |
| `tools/do_hd2.py` | `--goi WP-C3b`: GL CF → `tinh_gl` → `cfa1_daily` *(trục `truc_ngay(IX.PER KHO, ngay_dong_bang ảnh vào)`)* → `cuon_ky` → so từng ô 410. Kho tắt/chưa khai IX.PER ⇒ **ĐỎ có lý do** *(⛔ rơi về ngày tạm)* |
| `docs/ITL/_tools/hd2_cong.json` | + khoá `WP-C3b` *(C2 gốc · C3a giữ nguyên — 120 dòng thêm, 0 dòng xoá)* |
| `tests/bao_cao/test_cuon_ky.py` *(7)* · `tests/oracle/test_do_hd2_c3b.py` *(15)* | AC-1…AC-3 |
| `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` | Q8: `MONG_PYTEST_TOAN_BO` 3493 → **3515** *(= thu thập; +22)*, cùng commit |

## Số đo cổng WP-C3b *(Đ4 — mỗi số một nhãn)*
| Nhãn | Thực | Mong |
|---|---|---|
| ô lưới 410 | 21.090 = 370 hàng × 57 kỳ | — |
| **ô so** | **11.585** = 5 × 54 mã × 43 kỳ có ngày − 25 ô `-` | 11.585 |
| **ô so mà đáp án ≠ 0** *(bằng chứng dương, Đ3)* | **2.636** | 2.636 |
| **khớp** | **11.585 / 11.585** · lệch ngoài tên **0** | — |
| ô KPI loại *(20 mã = `MA_KPI` của H5, cùng đối tượng)* | 5.700 = 5 × 20 × 57 | 5.700 |
| ô `-` loại | 25 | 25 |
| ô kỳ 0 ngày loại *(14 kỳ: 2024 H1·Q1–Q3·M01–M09 + 2026M12)* | 3.780; đáp án ≠ 0 ở đó: **0** | 3.780 · 0 |
| hàng đáp án *(ô ≠ 0, cả KPI)* | 5.655 | 5.655 |
| trục | IX.PER **2024-10-21** → 2026-11-18 · 759 ngày · năm 2024–2026 · 57 kỳ | — |

**Lệch có tên = MONG** *(cùng feed WP-C3a)*: `thieu_tien_te_D` 12 dòng · `hd_ngoai_cay` 162 *(ITE Interest 152+1 · Server Cost 7 · GAC - Other 1 · rỗng 1)* · `hd_khac_hoa_thuong` 5 · `dong_nhan_cha` 0 · `dong_ngoai_truc` 0 · `o_khac_0_ky_khong_ngay` 0.

**Dung sai** *(theo khối, `rtol 0`)*: đo không dung sai trên 11.585 ô — max|lệch| lá **1,10e-14** · cha **1,17e-14** *(Σ ≤ 366 ô Daily; max|exp| 59,6)* ⇒ `atol 2e-13` *(biên ×17–18)*. +1e-12 một ô đáp án ⇒ ĐỎ đúng ô ấy; +1 nguyên tệ một dòng ⇒ ĐỎ đúng lá + tổ tiên × {GROUP, LE} × 4 kỳ.

## Quyết định khai *(lưu ý orchestrator)*
- **20/10/2024**: engine theo **KHO** *(21/10, C6)*. Đo 18/11: dòng sổ ngày 20/10 = **0** *(ngày sổ nhỏ nhất 45586 = 21/10)*; ô ≠ 0 cột 20/10 của 409 = **5**, cả 5 là `NPC` *(KPI luỹ kế — loại)* ⇒ 21/10 ⛔ làm rơi số nào; `dong_ngoai_truc` MONG 0 canh nếu sổ có dòng 20/10. IX.PER = 20/10 ⇒ cổng ĐỎ *(bài `…khac_ngay_dau_khai_thi_DO`)*.
- **411** ⛔ so: DT5 loại khỏi đóng băng *(ISP Step 15)* ⇒ khai `loai_tru` trong `hd2_cong.json`. ISP Step 20 §2 ghi "410 · 411" ⇒ **cần errata**.
- **Kỳ chưa tới / trước ngày đầu** *(errata ㉑)*: ⛔ đếm là khớp 0; loại có tên, đáp án ≠ 0 ở đó ⇒ ĐỎ.
- **WP-C3a giữ nguyên** *(trục từ đáp án 409 — cổng H5 đã R2 ĐẠT)*; AC-3 phủ bằng WP-C3b + `truc_ngay`.
- **Cụm 5435** *(⛔ kho thật)*: nạp `IX.PER` 21/10 *(phiên bản 1, actor `isp-h6-cum5435`)* để `--ghi` chạy được.

## Bằng chứng từng AC
| AC | Đỏ trước | Bằng chứng |
|---|---|---|
| AC-1 · H6-B1 | `pytest tests/bao_cao/test_cuon_ky.py` ⇒ exit 2 `ImportError: cannot import name 'cuon_ky'` | 2 ngày T11/2024 ⇒ `2024`·`2024H2`·`2024Q4`·`2024M11` đúng, cha = Σ con, 0 ô `2025*`. Phá: ép `replace(year=2025)` ⇒ `10 failed, 12 passed`; trả nguyên ⇒ `22 passed` |
| AC-2 · H6-B2 | `pytest tests/oracle/test_do_hd2_c3b.py` ⇒ exit 1 `4 failed, 11 errors` *(thiếu `ANH_YHQM`/`so_sanh_c3b`)* | `do_hd2.py --goi WP-C3b --ghi` ⇒ `KẾT: DAT`, exit 0; Đ3 đáp án rỗng ĐỎ; Đ5 bốn MONG đổi ĐỎ; ô kỳ chưa tới có số ĐỎ; ⛔ vòng tròn *(xoá giá trị đáp án ⇒ lưới y nguyên)* |
| AC-3 | cùng lượt đỏ | IX.PER nạp + `doc_per` từ kho test ⇒ ĐẠT; kho chưa khai ⇒ ĐỎ *(CLI thật trước khi nạp: `KHONG DAT: IX.PER ⛔ đọc được từ kho: ChuaKhai`)*; `MA_KPI_C3B is MA_KPI` |
| AC-4 · Q8 | — | `--duong-nen --cong 5435` (một lần, một mình): `KẾT: ĐẠT` · toàn bộ `12 failed, 3487 passed, 2 xfailed, 14 errors` = **28 = 28** node id · chạy 3515 *(mong ≥ 3515)* · web `3 failed, 672 passed` = 3 = 3, chạy 675 |

## Cổng
| Lệnh | Kết quả |
|---|---|
| `lint-imports` | `11 kept, 0 broken` |
| `kiem_tai_lieu.py` | ĐẠT *(314 file, 2578 bảng)* |
| `kiem_so_song` · `khop_owner` · `soi_bang_tuyen` | ⛔ CHƯA CHẠY — ⛔ chạm tuyến/schema/số sống |

## Kho thật
`KHONG_CHAM`. ⛔ Drive. SA chỉ đọc công thức `Report I CFA1 Y H Q M` + `Report I CFA1 Daily` *(vài hàng đầu)*.
