# KQ-280 — R2 CUỐI kiểm `H8` · ISP Step 39 *(SO.PLA1 dồn ngày 1 tháng PL start — D4 + SO.PLA3 cộng theo khoá, cổng WP-C3d)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới** *(+ 3 GHI NHẬN R1 xét lại, giữ nguyên mức)* ⇒ backlog. Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_H8.md` v0.2 *(`H8-R2-01…02`)*. Đo trên cây gộp thử `thu/H8` = nhánh làm việc `291993f` + `isp/H8` @ `518ea28`, cụm `5445`; IX.PER + IX.ORG nạp vào `fls_test`. Phiếu thuộc `WO-277` · `BG-278` · `KQ-279`.

| # | Việc | Mẫu số | Kết |
|---|---|---|---|
| 0 | Xung đột gộp | tệp | **2**, đều sàn pytest *(`dung_moi_truong_isp.sh` + bài ghim; nhánh làm việc 4481 ↔ H8 4426)*; `hd2_cong.json` · `do_hd2.py` · bài gates · sổ · changelog gộp sạch *(C3c · C4c · C3d cùng có mặt)* |
| 1 | `do_hd2.py --goi` trước/sau gộp | `tong_o · khop · lech_co_chu_dich` | C3a **205.175 · 205.140 · 35** · C3b **11.585 · 11.543 · 42** · C3c **888 · 835 · 53** · C3d **1.289.415 · 1.287.624 · 1.791** — **không đổi** so với `isp/H8` |
| 1b | `--ghi` · ảnh `dau_vao` | `hd2_cong.json` · **6** ảnh | **0 byte** đổi *(nạp IX.PER đúng chuỗi `nguon` — `H8-R2-01`)*; ảnh **TRÙNG byte** cả với `isp/H8` lẫn nhánh làm việc *(DT7b `d5fdea2` không đụng ảnh H8 dùng)* |
| 1c | Bài xanh | CG2 + `test_isp_gates_hd2` + `test_pla` + `test_do_hd2_c3a/b/c/d` + `test_dung_moi_truong_isp` | **183 passed** + **73 passed**; `/gates` `HD2_WP_C3D` + cha C3 **4/4** do bài quét tệp thật xanh |
| 2 | `H8-R1-02` đo bù | lớp `as_is_truoc_CA` **1.783** ô *(− 133 `NPC` Y/H/Q/M ⛔ tính được)* | tính tay độc lập từ cột thô *(⛔ qua engine)*: engine = tay **1.650/1.650**; đáp án = tay dựng bằng nguyên nhân khai *(CDT = 0 · dư = GROUP trước `CA`)* **1.650/1.650** ⇒ **0** ô là lệch FLS. Mẫu ngẫu nhiên *(seed `20261122`)* **60** ô trên **1.554** ô chưa tính tay riêng *(KPI 41 · tong 12 · lá Y/H/Q/M 7)*: **60/60** · **60/60**. `-01` *(D4)*: GL **0** hàng `AH` có ngày ≠ 1 ⇒ cổng ⛔ phân biệt được, bài đơn vị là chốt — rủi ro dữ liệu hiện tại **0**. `-03`: nhãn, cổng ⛔ ảnh hưởng *(max\|lệch\| 5,3e-14 ≪ atol 1e-12)* ⇒ cả ba **giữ GHI NHẬN** |
| 3 | Đột biến mới *(bản sao `git archive` cây gộp thử)* | **10** | **9/10** ĐỎ: `SERIAL_CA`+1 · đổi nhãn CDT `CAH↔ASA` · năm `BM` luôn 2025 · bỏ `yhqm` khỏi lớp · dấu `EBIT−CDC` · 1 ô HR `BA` +1e-9 · `GAC` đáp án 1e-6 · `hd2_cong.json` C3d 1791→1790 *(bài gates)* · sàn 4525→4524 *(bài ghim)*. **Sống 1**: `GAC` đáp án lệch 2,8e-15 < `atol_lech` 1e-9 — đúng thiết kế |
| 4 | Cổng `--duong-nen --cong 5445` *(một lần, một mình)* | pytest toàn bộ + web | tập đỏ + XFAIL **28 = 28** *(thêm 0 · bớt 0)*, chạy **4525 ≥ 4525**; web **3 = 3**, chạy **681**; `lint-imports` **11 kept, 0 broken**; `kiem_tai_lieu.py` ĐẠT *(440 tệp · 2.859 bảng · 935 ô ngày · 104 mã QĐ, đo SAU khi thêm 2 tệp này)*; `soi_bang_tuyen.py` **48/48** tuyến khớp SQL thật |

**Sàn cây gộp thử = 4.525** *(thu thập thật; ⛔ 4.426 của H8 · ⛔ 4.481 của nhánh làm việc)* — gộp tay: đặt `MONG_PYTEST_TOAN_BO` + bài ghim = thu thập thật cây gộp ở commit gộp; nhánh làm việc có thể đã tăng thêm ⇒ đo lại.

## GHI NHẬN mới ⇒ backlog *(⛔ chặn gộp)*
- `H8-R2-01` `--ghi` mang chuỗi `nguon` do người nạp IX.PER đặt vào `nguon_ngay_dau` *(C3a ≠ C3b)* ⇒ tái lập cần đúng chuỗi.
- `H8-R2-02` **133** ô `NPC` Y/H/Q/M của lớp `as_is_truoc_CA` chưa tính tay *(quy ước hậu tố kỳ chưa khai)*.

## Gửi orchestrator
**Gộp `isp/H8` được** *(0 CHẶN · 0 NÊN SỬA)*; xung đột chỉ ở sàn pytest — đặt = thu thập thật. Hai câu hỏi sổ 416 *(72 cột 2024 dán cũ · `GAC` thiếu `CXA`)* vẫn chờ chủ sổ.
