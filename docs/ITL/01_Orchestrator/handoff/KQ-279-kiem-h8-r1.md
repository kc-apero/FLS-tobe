# KQ-279 — R1 kiểm `H8` · ISP Step 39 *(SO.PLA1 dồn ngày 1 tháng PL start — D4 + SO.PLA3 cộng theo khoá, cổng WP-C3d)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(⇒ backlog)*. Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_H8.md` v0.1 *(`H8-R1-01…03`)*. Đo trên `isp/H8` @ `8980abd`, cụm PG `5445`, IX.PER nạp vào `fls_test` *(21/10, luật A)*. Phiếu thuộc `WO-277` · `BG-278`.

## Soát
| # | Việc | Mẫu số | Kết |
|---|---|---|---|
| 1 | ⛔ vòng tròn: đường tính ⛔ đọc đáp án | grep `pla.py` + `fls/` | **0** khớp `dap_an`·`fixture`·`tools`·`json`; `tinh_luoi` chỉ nhận `gl · hr · fx · cay · lich`; đáp án chỉ vào `so_tab` / `_tu_kiem` |
| 1b | Đột biến 1 dòng đầu vào | GL +1000 `GI` · HR +1000 `BA` | GL ⇒ ĐỎ 414·418·415·419, 416·417 y nguyên; HR ⇒ ĐỎ 416·418·417·419, 414·415 y nguyên; ô `GROUP#<mã>#<ngày\|kỳ>` ĐỎ đúng — Daily lẫn Y/H/Q/M |
| 2 | D4 qua `ngay_ghi_nhan` C6, luật B bị từ chối | `pla.py` | ⛔ chép: `ngay_pl` chỉ gọi `ky.ngay_ghi_nhan`; M7 *(luật B)* ⇒ bài `test_H8_B1…` ĐỎ, **cổng XANH** ⇒ `H8-R1-01` |
| 3 | Cộng theo KHOÁ · KPI theo tab | đột biến | M1 *(khoá → vị trí)* ĐỎ · M2 *(cộng KPI)* ĐỎ · M3 `SHQ2 = 0` ĐỎ · M4 dấu HR ĐỎ · M5 `PL8` dùng `CIT` ĐỎ · M6 `NPC` tiền tố ĐỎ |
| 4 | Lệch AS-IS **1.791** có thật là của AS-IS | **96** ô lá tính tay *(⛔ qua engine)* + **8** ô `GAC` + đối chứng **20** ô ≥ `CA` | **96/96** · **8/8** *(chênh = `CXA` tay)* · **20/20** — xem sổ; **0** lệch FLS bị nhét vào lớp AS-IS *(giới hạn: 1.687 ô suy ra chưa tính tay riêng ⇒ `H8-R1-02`)* |
| 4b | `mong_lech_co_chu_dich` + sha ĐỎ hai chiều | đột biến | `mong` +1e-6 ĐỎ · đổi 1 ô đáp án vùng AS-IS ĐỎ *(sha)* · đổi 1 chữ số sha ĐỎ · đổi 1 ô ngoài vùng ĐỎ · nới `ATOL` ĐỎ · `mong` +1e-15 XANH *(trong 1e-9)* |
| 5 | Mẫu số Đ4 đếm lại | `hd2_cong.json` | Daily **1.193.940** · Y/H/Q/M **95.475** · `khong_so_duoc` **46.398** · `tong_o` **1.289.415** · khớp **1.287.624** · lệch có chủ đích **1.791** · ngoài tên **0** |
| 6 | `WP-C3d` ↔ CG2 · `/gates` | tệp thật | `--ghi` chạy lại ⇒ **0 byte** đổi; `/gates` `HD2_WP_C3D` = `true` *(1.287.624/1.289.415 + 1.791)*; cha `HD2_WP_C3` = `true`, **4/4** gói con *(1.505.142/1.507.063 + 1.921)*; bài `test_pla` + `test_do_hd2_c3d` + `test_isp_gates_hd2` + `test_dung_moi_truong_isp` **183 passed** |
| 7 | Sàn Q8 4.426 | `--collect-only` | thu thập **4.426** = sàn = chạy thật |

## Đột biến
**15/15 chết** *(14 ở cổng, M7 chỉ ở bài đơn vị)* — engine/cổng M1…M10 trên bản sao `git archive` *(trả nguyên, cổng lại `KẾT: DAT`)* + dữ liệu GL · HR · `mong` · ô đáp án vùng AS-IS · ô đáp án ngoài vùng.

## Cổng *(`--duong-nen --cong 5445` MỘT lần, một mình, trên `8980abd`)*
`KẾT: ĐẠT` — toàn bộ: tập đỏ + XFAIL **28 = 28** node id *(thêm 0 · bớt 0)* · chạy **4426 ≥ 4426**; `tests/web` **3 = 3** · chạy **681**. `lint-imports`: **11 kept, 0 broken**. `kiem_tai_lieu.py`: ĐẠT *(432 file · 2.838 bảng · 926 ô ngày · 104 mã QĐ, đo SAU khi thêm 2 tệp này)*; `soi_bang_tuyen.py`: **48/48** tuyến khớp SQL thật.

## Gửi orchestrator
**Gộp được sang R2 cuối** *(0 CHẶN · 0 NÊN SỬA)*. Backlog: `H8-R1-01` *(D4 chỉ chứng bằng bài đơn vị)* · `-02` *(thêm bài tay độc lập cho lớp `as_is_truoc_CA`)* · `-03` *(`atol ≥ ×30` sai, thật ×18,9)*. Hai câu hỏi sổ 416 *(72 cột 2024 dán cũ · `GAC` thiếu `CXA`)* vẫn chờ chủ sổ — kiểm xác nhận cả hai là lệch AS-IS thật.
