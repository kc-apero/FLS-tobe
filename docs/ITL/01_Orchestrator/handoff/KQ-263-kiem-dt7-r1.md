# KQ-263 — R1 kiểm `WO-261` · `BG-262` · ISP Step 31 · DT7 *(đáp án PLA, PD 414–419)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 9 GHI NHẬN ⇒ backlog.** Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT7.md` (v0.1). Đo trên `isp/DT7` @ `4aec25f`, cụm `5447`, nguồn sổ P&L `19NNTb…` *(chủ quyết 22/11)*.

## Đo *(nhãn đếm gì — Đ4)*
| Việc | Kết |
|---|---|
| Đọc lại **6 tab** bằng SA, so ảnh↔thô bằng script riêng | **43.811/43.811** ô số khớp; thô→ảnh thiếu **0** / **1.426.794** ô; hàng HD **4.514/4.514**; ô chữ 485 = {`-`}; trôi sổ từ 20/11 = **0** *(tái chạy khuôn: giống từng byte 6/6)* |
| `LOAI_MA` đo từ công thức thật | 40+10+17+7 = 74 **khớp**; ⚠ khối `SHQ2` 40 hàng `la` là công thức **DƯ** (`-01`) |
| `tu_kiem` tính lại độc lập | Daily lệch **4** · KPI **510** *(NPC 408)*; YHQM **0** · KPI **206**; `khong_so_duoc` **46.398** = thật *(thô `417` chỉ 1 khối)* — khớp từng số |
| Tương lai | số ở cột CÓ tiêu đề ⇒ từ chối; cột KHÔNG tiêu đề lọt *(`-02`)*, nhưng đo thật = **0** ô |
| Mốc ngày | sheet 2024-10-20 ≠ AP 21/10; cột 20/10 có **31** ô ≠ 0 *(`-07`)*; `chua_co_du_lieu` HR Daily **88** đúng |
| AC-7 · PII · sàn | 4 tệp chung `0` đổi · ảnh cũ `0` · `quet_pii_repo` **0** · sàn 4.267→4.321 = +48 bài + 6 tham số hoá = **thu thập thật** |
| Ảnh > 2 MB | chấp nhận; tải **0,03 s** ⇒ ⛔ hại H8 *(nén ⇒ backlog)* |

## Đột biến — **13/16 cắn**, 6/6 mục phiếu cắn
Sống 3 biến thể: `LOAI_MA` ở khuôn không ghim *(`-03`)* · số ở cột không tiêu đề *(`-02`)* · đổi giá trị ô thô giữ nguyên đếm *(`-09`, chỉ checksum cắn)*.

## Cổng
`--duong-nen --cong 5447` *(một lần, một mình)*: `12 failed · 4293 passed · 2 xfailed · 14 errors`, tập đỏ **28 = 28** *(thêm 0 · bớt 0, chạy 4321 ≥ 4321)*; `tests/web` **3 = 3**, chạy 681 ≥ 681; **ĐẠT**. `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT.

## Chuyển orchestrator / BA *(GHI NHẬN)*
`-01` `SHQ2` = phần dư ⇒ ghi vào WO H8 · `-07` errata AP mốc 20/10 · `-08` H8 có cần HR Y/H/Q/M 11 khối? · `-02·03·09` cổng/bài ⇒ backlog · `-04·05·06` sửa chữ BG.
