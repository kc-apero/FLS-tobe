# WO-329 — Voi · dựng 4 agent VẬN HÀNH gọi API (A1 RI · A2 PR · A3 SI.ITL · A4 Auditor) — bộ skill tuần tự + report MỘT TRANG khớp 100 %

| | |
|---|---|
| **Trạng thái** | `CHO_TEST` — giao 23/11 ~04:20 UTC · `fls-dev` bàn giao [`BG-330`](BG-330-ban-giao-wo-329.md) 23/11 |
| **Phát bởi** | orchestrator · 2026-11-23 |
| **Nhận** | `fls-dev` — phiên cloud **Opus 5.5 · medium** · nhánh `claude/bold-galileo-zukpaf-isp/AG` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` |
| **Dải phiếu** | `BG-330` · `KQ-331` (R1) · `KQ-332` (R2 cuối). Số trống kế tiếp sau dải: **333** |

## Vì sao — lời chủ 23/11
> *"giao 1 agents dựng 4 agents … Tôi muốn kiểm tra 4 agents đó trước, trong agents phải có bộ skill được chạy tuần tự, với mục tiêu ra được report tất cả các dữ liệu trên cùng 1 trang và khớp 100%, không được lệch"* — *"ý tôi đây là các agents vận hành như trong voi … agents gọi qua API"*.
- Chủ chốt nghĩa **"khớp 100 %"** = **đầu ra agent = số máy đã đo** (đầu ra engine tất định FLS + `voi_so_luong.json` + `hd2_cong.json`), lệch **0** từng ô. Lệch AS-IS CÓ TÊN (đã ký) hiện trên report với nhãn riêng, ⛔ tính là lệch.
- Chủ chọn chia theo **lớp dữ liệu** ⇒ khớp đúng 4 agent của AP Voi: **A1 RI** (nguồn → ảnh) · **A2 PR + SI.MAP** (dòng chuẩn + ghép) · **A3 SI.ITL** (sổ ITL hiệu lực, 7 khối R–AT) · **A4 Auditor** (cổng mỗi bước + report).

## Đã đo — đọc TRƯỚC khi viết dòng mã nào
| Nguồn | Nói gì |
|---|---|
| `docs/ITL/02_BA/Artifacts/AP_FLS-Voi_v3.1.2_ISP-Correction_2026-11-16.html` §4.1–§4.4 · §5.3.1 | hộp RI/PR/SI/KS, mã đã có (BUILT/PARTIAL), "còn lại cho agent"; **agent chỉ BẬT sau HD1 + HD2** |
| `docs/ITL/02_BA/Artifacts/Voi-FLS-tobe-phase1.html` (dòng ~701 · ~2342–2383 · ~2649 · ~2808–2832 · ~2869–2898 khi bóc chữ) | agent gọi API; phương án **A** (agent làm Claude Opus 5.5 · agent kiểm A4 **khác họ**) / **B**; phiên bản = mã mô hình ghim + checksum prompt + checksum tham chiếu; cửa G0→G3; scrubber `NFR-I13` trước khi gửi API |
| `docs/ITL/05_FleetEval/AP_FLS_FleetEval_v1.3.0_2026-11-09.html` + `eval-cards/` (`_chung` · `a3-1-ref` · `a3-2-luong` · `a3-3-nen-tang` · `a4-soat`) | thẻ đánh giá từng agent, rubric A4 0–2 — trạng thái **review**, CHƯA ký |
| `docs/ITL/_tools/voi_so_luong.json` | HD1 hôm nay: **5/23** kỳ đạt · sổ lý do **0** chữ ký · dòng ghép 9.845/9.967 · ô parity 69.510/69.510 |
| `docs/ITL/_tools/hd2_cong.json` (ngọn H14) | HD2: 11 gói · lệch FLS 0 |

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 · thẻ agent | 4 thẻ agent **để chủ đọc** (`docs/ITL/06_Agent/A1_RI.md` … `A4_AUDITOR.md`): vai · đầu vào/đầu ra (bảng kho/tệp) · công cụ được gọi (CHỈ hàm/tuyến FLS có sẵn — liệt kê) · mô hình ghim (phương án A, ⛔ bí danh) · checksum prompt · việc ⛔ được làm · cổng ra · trỏ hộp AP §4.x + thẻ fleet eval | BG + `kiem_tai_lieu.py` |
| AC-2 · skill tuần tự | mỗi agent một **bộ skill có thứ tự** (mỗi skill một tệp, số thứ tự trong tên); skill `n+1` chỉ chạy khi cổng của skill `n` ĐẠT; agent `k+1` chỉ chạy khi A4 cho agent `k` ĐẠT (A1 → A2 → A3 → A4). Bài: phá cổng skill giữa ⇒ chuỗi DỪNG đúng chỗ, có tên | pytest |
| AC-3 · gọi API | lớp gọi mô hình có giao diện chung (Anthropic Messages API cho agent làm; A4 khác họ theo AP — giao diện nhà cung cấp, ⛔ cứng một hãng); **mặc định chế độ PHÁT LẠI** (câu trả lời ghi sẵn / giả) — gọi API THẬT chỉ khi có cờ rõ + khoá trong biến môi trường + `FLS_CHO_GOI_API=1`; **⛔ gọi API thật trong WO này**. Scrubber `NFR-I13` chạy TRƯỚC mọi lời gọi: `Diễn giải` · `Số chứng từ` · tên người · email · số TK cá nhân ⛔ rời máy (bài chứng minh) | pytest |
| AC-4 · report MỘT trang | một tệp HTML tĩnh (`docs/ITL/06_Agent/report.html`, sinh bằng lệnh): MỌI dữ liệu của 4 lớp trên một trang — mỗi lớp/kỳ/khối: **mẫu số** (Đ3) · khớp · lệch · nhãn số (Đ4); cột so **agent ↔ máy đã đo**; mong **lệch 0 mọi ô** (Đ5 — khai `mong`, ĐỎ hai chiều; phép ⛔ đo được = ĐỎ); lệch AS-IS có tên ở khối riêng, ⛔ cộng vào lệch | lệnh sinh + pytest |
| AC-5 · chứng minh | chạy chuỗi 4 agent ở chế độ phát lại trên kho test ⇒ report **KẾT: ĐẠT, lệch 0**; đột biến 1 ô đầu ra agent ⇒ report ĐỎ đúng ô; xoá đầu vào một lớp ⇒ ĐỎ "⛔ đo được" | pytest |
| AC-6 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT (28 = 28 · web 3 = 3); `lint-imports` (thêm hợp đồng tầng cho gói agent mới nếu có) · `kiem_tai_lieu` · `quet_pii_repo` = 0 | `--duong-nen` |

## Ràng buộc
- **⛔ BẬT agent chạy thật** (AP §5.3.1: sau HD1 + HD2; HD1 đang 5/23) · **⛔ gọi API thật** · ⛔ khoá API trong repo/chat. Ghi kho THẬT: `KHONG`.
- ⛔ sửa engine tất định / tuyến (agent GỌI chúng). ⛔ đổi quyết định AP (mô hình, cửa G0–G3) — chỗ AP còn PROPOSED/chưa ký ⇒ ghi **câu chủ** kèm khuyến nghị trong BG.
- Riêng tư `CLAUDE.md` · `PM_COT_RIENG_TU` · `sao_luu/` `hien_vat/` ⛔ commit.
- Sản phẩm để CHỦ KIỂM trước: BG-330 mở đầu bằng mục "Đọc 4 agent trong 10 phút" — trỏ 4 thẻ + danh sách skill theo thứ tự + ảnh chụp report.

## §5 · Nhật ký
| Ngày | Ai | Việc |
|---|---|---|
| 2026-11-23 | `fls-dev` | `DANG_LAM` → `CHO_TEST`: [`BG-330`](BG-330-ban-giao-wo-329.md). Hai lời chủ giữa lượt (4 nguồn raw · ghép theo nội dung · fleet eval nhiều vòng · 4 zip) đã gộp vào phạm vi — xem BG |
