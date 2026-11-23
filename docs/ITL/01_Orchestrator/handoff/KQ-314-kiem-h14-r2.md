# KQ-314 — R2 cuối `WO-311` / `BG-312` *(ISP 3.1.2 · Step 46 · H14 — WP-C5c)*

| | |
|---|---|
| **Kết quả** | **TRƯỢT** — **1 CHẶN** *(tích hợp gộp)* · **0 NÊN SỬA** · 3 GHI NHẬN |
| **Phát phiếu** | `fls-test` *(R2, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/H14` `f8768c2` + cây gộp thử `origin/work` `e437f4b` · cụm 5445 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H14.md` *(v0.2)* |

## Kết luận
Vòng sửa R1 **đúng** *(5/5 mục đo lại)*. TRƯỢT chỉ vì **tích hợp**: nhánh làm việc đã có H13-R1 `31a6bb3` *(`pla.py`)* mà `isp/H14` chưa — `mong` check `NB = 0` của `WP-C5c` lệch ⇒ **`H14-R2-01`**.

1. **`-01` cổng `None` trung thực — ĐÚNG.** `HD2_WP_C5C` + cha `HD2_WP_C5` = `None`; `ly_do` nêu *"605: ô so 0/13706 ô số — DỪNG … CHƯA có chữ ký chủ"* + *"độ phủ 615: ô so 12380/48021 · 35641 ô số chưa so (…)"*. `DUNG_KY = {}`. Đột biến `DUNG_KY={"605":"x"}` ⇒ ĐỎ 3 bài *(nhờ ghim JSON; chữ ký = mọi chuỗi ⇒ `R2-02`)*. F03: `_muc(null)` ⇒ *"— ⛔ KHÔNG ĐO ĐƯỢC"* *(đo tầng `doc_cong_hd2` + đọc mã; ⛔ dựng trình duyệt)*.
2. **`-02` khuôn 615**: ô so **12.380** · khớp **11.674** *(thật 2.023/2.729)* · lệch `lech_ban_ccr_vs_cf` **671** + `ite_alias` **35**. **Mẫu 24/24** ô `ngày` lệch truy độc lập từ HAI ảnh thô *(615 `Unit: mUSD` vs 610 `ngay`, cột tra theo hàng ngày 5)*: engine = 610 ≠ 615. Rổ **48.021 = 12.380 + 10.040 + 800 + 6.753 + 18.048** *(`engine_vang` · ngoài trục · `chua_co_dau_vao` · `ngoai_khuon`)* ✓. `ngoai_khuon` 18.046 = bản sao DR3: **18.046/18.046** trùng ảnh 609 cùng *(khối, mã, cột)* ✓ *(609 có 35.542; ảnh 615 trong repo chứa nửa — `R2-03`)*. ⛔ ô 615 nào khớp nhờ ảnh dán: `ccr_daily_report_2` **0** tệp ở `tests/fixture` · `tools` · `fls`; 615 đọc `ccr_daily_report.json` *(DT13 chưa gộp)* ✓.
3. **`-03` vòng tròn**: bài `test_AC4_…` ĐỎ được — đột biến mới *(engine CFA1 đọc 1 ô đáp án 409)* ⇒ đúng bài đó đỏ; trả nguyên xanh.
4. **`-04`**: đo độc lập 607 và 609: ô `|e−a|=0,5` = **71** *(`loi_as_is` 71 · khối GROUP · e>a 71)* = **68** chuỗi *(17 mã × M02/Q1/H1/Y)* + **3** *(NPC M01 · NPC M02 · PL5 M02)*; `SHQ` 0 ✓.
5. **`-08`**: `FS1_FS2_gop` dựng được; `FS3` DỪNG có tên *(đột biến `fs3_tin_cay` đổi nguồn ⇒ `test_R1_08_FS3…` ĐỎ)*; câu FS3 ở ảnh 609 · 615 = 1 · 1.
6. **Cây gộp thử** *(xung đột `dung_moi_truong_isp.sh` + bài ghim ⇒ lấy bản nhánh `isp/H14`, đặt sàn = thu thập **4.767**; `hd2_cong.json` tự gộp)*: `--goi WP-C5a` ĐẠT 45.674 · `WP-C5b` ĐẠT 4.102 · `--ghi` C5a+C5b **0 byte đổi**; **`WP-C5c` ĐỎ** + `--ghi` đổi 40+/21− dòng *(khối `check NB`)* = `R2-01`. Đối chứng: `isp/H14` riêng 136/136 xanh.
7. **Đột biến** **9/9 cắn**, baseline xanh: DUNG_KY không chữ ký · bỏ nhãn `lech_ban_ccr_vs_cf` · hoán đổi khuôn 615 · chuỗi chỉnh tay bỏ `Y` · FS3 đổi nguồn · `_goi_la` bỏ chặn `dat=true+kdd` · bỏ chặn `dat=null` không kdd · vòng tròn CFA1 · `do_phu` đếm ô so = ô số đáp án. *(Lần đầu vòng tròn CFA1 "sống" vì khoá không khớp ⇒ đột biến vô hiệu, làm lại đúng khoá ⇒ cắn.)*
8. **Cổng cây gộp**: `--duong-nen --cong 5445` *(một mình)* **ĐỎ**: `17 failed · 4734 passed · 2 xfailed · 14 errors`, chạy **4.767**; tập đỏ **33 = 28 + 5** *(thêm đúng 5 bài C5c ở `R2-01` · bớt 0)*; web **3 = 3**/690. `lint-imports` 11 kept 0 broken · `kiem_tai_lieu` ĐẠT *(480 file · 2.941 bảng)* · `soi_bang_tuyen` KHỚP 49 tuyến.

## Điều kiện gộp *(orchestrator quyết)*
Dev sửa `R2-01` trong commit gộp *(sinh lại `mong` `NB = 0` + `hd2_cong.json` `WP-C5c` trên cây gộp, ĐỎ→xanh, sàn 4.767; tập đỏ về 28)* ⇒ R2 lại ngắn. Trạng thái cổng đúng khi gộp: `HD2_WP_C5C = None` có tên — **605** chờ chủ ký *"DỪNG có tên"* · **615 `Cash Balance` 1.495 ô** chờ gộp DT13. Gộp H14 **không** làm cổng C5 xanh; H14 ĐẠT ≠ cổng `true`.
