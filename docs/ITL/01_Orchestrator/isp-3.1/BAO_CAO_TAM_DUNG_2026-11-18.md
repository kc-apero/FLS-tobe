# Báo cáo tạm dừng ISP 3.1.2 — 2026-11-18 ~07:10 UTC

> Người dùng 18/11: *"sau khi xong, tạm dừng toàn bộ, cập nhật tiến độ + log + token các agents đang tiêu tốn — đốt quá nhanh; tiến độ không đẩy nhanh được nhiều"*. ⇒ ⛔ giao phiên mới; 4 phiên đang chạy được để chạy xong (dừng giữa chừng = bỏ phí phần đã tiêu); lượt kiểm 07:28 chỉ THU kết quả.

## 1. Tiến độ so với ISP (48 bước)
| Trạng thái | Số | Bước |
|---|---|---|
| ✅ Đã gộp (R1–R3) | **12** | S0 · H1 · C1 · DT1a · H2 · CG1 · DT1b *(công cụ)* · DT2 · FG · DT3 · DT4 · C4 |
| 🟢 Đủ 3 vòng, chờ gộp | 1 | DT1b-xuất khoá (`WO-127`, R3 `KQ-131` ĐẠT @ `2108027`) — gộp xong ⇒ owner chạy nhãn thật |
| 🔄 Đang chạy (để xong) | 4 | R3 DT5 · sửa H4 sau R2 · sửa C5 sau R1 · DT8 (làm) |
| ⏸ Chặn | 1 | H3 — cần nhãn THẬT DT1b (owner chạy) |
| ⬜ Chưa bắt đầu | 30 | C6 · F4 (đã mở khoá) · DT6 · H5 → I2 |

Đường găng (13): xong S0 · DT2 · DT3 · C4; C5 đang sửa R1.

## 2. Chi phí (giá niêm yết API, đo bằng `get_session` 18/11 ~07:05; 4 phiên đang chạy còn tăng)
| Model · vai | Phiên | USD | Output tokens | Cache-read tokens |
|---|---|---|---|---|
| Opus 4.8 · dev | 24 | **294,66** | 2,18 tr | 371 tr |
| Opus 4.8 · review *(trước khi đổi Sonnet 17/11)* | 6 | 49,56 | 0,36 tr | 58 tr |
| Sonnet 5.5 · review | 26 | **30,69** | 0,88 tr | 101 tr |
| Orchestrator (phiên này) | 1 | **96,04** | 0,85 tr | 214 tr |
| **Tổng** | **57** | **≈ 471** | 4,27 tr | 744 tr |

- Theo bước (gồm làm + mọi vòng sửa + review): C5 62 · DT3 60 · DT1b 46 · H4 42 · DT4 35 · FG 26 · DT1b-xuất 24 · C4 23 · H2 19 · CG1 14 · DT5 13 · DT2 11 USD.
- Phiên đắt nhất: C5 dev **60,7** (ngữ cảnh ~600 nghìn token) · H4 dev 28,3 · DT3 dựng lại 28,3 · sửa DT1b R1 17,4.
- 5 phiên hỏng vì hạn mức (429) — tiêu ít nhưng mất thời gian chờ.
- Bình quân ≈ **35 USD / bước đã gộp**; một vòng review Sonnet ≈ 1–1,7 USD, một phiên dev Opus ≈ 8–60 USD.

## 3. Vì sao tốn mà không nhanh
1. **Mỗi bước = 5–8 phiên** (làm · R1 · sửa · R2 · sửa · R3 · đôi khi R3b). Review mỗi vòng đều tìm thêm GHI NHẬN/NÊN SỬA nhỏ ⇒ thêm vòng sửa Opus.
2. **Phiên dev Opus đọc lại repo lớn + chạy cổng hồi quy đầy đủ** (~3.100 bài, nhiều lần mỗi phiên) ⇒ cache-read 371 triệu token. C5 một mình 60 USD.
3. **Hạn mức 5 giờ** chặn 2 lần ⇒ 5 phiên chạy song song không tăng tốc tương ứng; chờ hạn mức xoá phần lợi.
4. **Orchestrator** đọc báo cáo dài của từng phiên + làm gộp tại chỗ ⇒ 96 USD.

## 4. Đề xuất giảm chi phí (chờ người dùng chọn)
| | Đề xuất | Ước giảm |
|---|---|---|
| A | Dev chuyển **Sonnet 5.5** (giữ Opus chỉ cho bước engine khó H5/H6/H9…) | ~70–80 % chi phí dev |
| B | **2 vòng review** thay 3: R1 đầy đủ + R2 cuối (gộp R2/R3, kèm cây gộp thử); GHI NHẬN ⇒ backlog, ⛔ mở vòng sửa | ~30–40 % số phiên/bước |
| C | Cổng hồi quy đầy đủ **chỉ chạy 1 lần** ở cuối phiên dev và ở vòng review cuối; giữa chừng chạy bài liên quan | giảm thời gian + cache-read |
| D | Song song **2–3 phiên** thay 5 (tránh chạm hạn mức) | ổn định, ít phiên hỏng |
| E | Orchestrator tóm báo cáo ngắn hơn (yêu cầu phiên con báo ≤ 15 dòng) | ~30–50 % chi phí orchestrator |

Ước: A + B + C ⇒ ~8–12 USD/bước (từ ~35).
