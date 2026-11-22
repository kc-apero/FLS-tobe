# KQ-286 — R2b NHẸ `WO-269` / `BG-270` vòng sửa `KQ-272` *(ISP 3.1.2 · Step 41 · DT11)*

| | |
|---|---|
| **Kết quả** | **ĐẠT** — **0 CHẶN · 0 NÊN SỬA** *(1 GHI NHẬN giữ từ `KQ-272`)* |
| **Phát bởi** | `fls-test` *(R2b nhẹ, vai KIỂM — ⛔ sửa mã)* · 2026-11-22 · `isp/DT11` `d4850ad` + cây gộp thử `thu/DT11` *(nhánh làm việc `dbac86e` + `isp/DT11`)* |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT11.md` *(v0.4, mục "Số đo R2b")* |

## Soát *(phần đã ĐẠT ở R1/R2 ⛔ soát lại)*
- **Gộp thử**: **0 xung đột**.
- **`-01` đóng**: bài AC6 `⊇` xanh trên cây gộp thử *(60 ảnh `dap_an/`)*; đột biến xoá `atl.json` ⇒ **ĐỎ**, thêm 1 byte `atl.json` ⇒ **ĐỎ**; trả nguyên ⇒ xanh, cây sạch.
- **`-02` đóng** *(script đếm riêng, ⛔ hàm khuôn; nhãn đếm gì: 6.427 chuỗi nhãn hàng / 66.504 chuỗi ảnh 615)*: nhãn `≥ 8` chữ số gắn hậu tố tên người **0** *(ảnh cũ 7)*; đủ **11** mã `TK_CA_NHAN_1…11`, mỗi mã 1 lần; 7 số cũ → 7 mã mới **1–1** hai chiều *(cùng số ⇒ cùng mã)*; chỉ **9** chuỗi đổi *(7 nhãn + `ghi_chu_khuon` + checksum)*. Còn 23 chuỗi `≥ 8` chữ số = 22 nhãn tổ chức *(giữ, đúng orchestrator)* + 1 số thực `46086.…` *(⛔ TK)*.
- **Checksum 615** tính lại sha256 riêng = **`14f965a9b8f7a4e8`** = khai = ghim *(cũ `2fd16287aa3648e0`)*. **54/54** ảnh có ở nhánh làm việc y nguyên byte; 5/5 ảnh DT11 còn lại y nguyên so `34a119c` — chỉ 615 đổi.
- **PII**: `quet_pii_repo` **0 chỗ · 0 tệp**. 7 tên viết tắt đứng riêng *(⛔ kèm số TK)* **giữ** theo quyết chủ 11/09 — ⛔ phát hiện.

## Cổng
- `--duong-nen --cong 5446` *(một mình)*: **ĐẠT** — tập đỏ **28 = 28** *(thêm 0 · bớt 0; XFAIL 2)*, chạy **4450** *(mong ≥ 4450 = sàn cây gộp)*; `12 failed · 4422 passed · 2 xfailed · 14 errors`; web **3 = 3**, 681.
- `lint-imports` 11 kept 0 broken · `kiem_tai_lieu` ĐẠT.

## GHI NHẬN ⇒ backlog
`DT11-R2-03`: mở rộng máy quét `khoa_R_CN` + tài liệu BA cũ — chờ chủ quyết, ⛔ chặn.

Việc kế: `isp-gop-buoc` gộp `isp/DT11` vào nhánh làm việc *(0 CHẶN · 0 NÊN SỬA)*; đặt sàn **4450**.
