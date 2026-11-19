# KQ-239 — R1 kiểm `WO-234` · làm sạch số TK cá nhân *(`isp/PII` @ `cf9ae8a`)*

**Kết luận: TRƯỢT *(gửi `DEV`)* — 1 CHẶN · 3 NÊN SỬA · 2 GHI NHẬN.** Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_PII.md`. ⛔ Phiếu không chứa giá trị số TK.

| Mã | Mức | Tóm |
|---|---|---|
| `PII-R1-01` | **CHẶN** | zip theo dõi `docs/ap-src/Man g#U00e1n…zip` còn **37 chỗ** số TK cá nhân *(4 tệp trong zip, đủ 5 số)*; máy quét bỏ qua tệp ⛔ UTF-8 |
| `PII-R1-02` | NÊN SỬA | số `P2` có cả nhãn `CN` *(11 tệp, che)* lẫn `_VGO1` *(3 chỗ / 2 tệp, chưa che)* — chủ quyết |
| `PII-R1-03` | NÊN SỬA | độ phủ: `cho <số>-` **45/10 tệp** · `<số>-Ref…-CK` **19/3** · `tài khoản <số>` **5/3** lọt mẫu |
| `PII-R1-04` | NÊN SỬA | đột biến `_doc`→`None` ⇒ 6/6 xanh *(Đ3: đếm tệp liệt kê, ⛔ tệp đã đọc)* |
| `PII-R1-05·06` | GHI NHẬN | biên chữ số ở che không bài cắn *(`M9`)* · log phiên lỡ in 1 số TK pháp nhân *(đóng)* |

**Đã ĐẠT:** diff HTML/tài liệu tối thiểu *(0 dòng ngoài chỗ che)* · mỗi số 1 nhãn *(5 số/5 nhãn)* · nhãn theo thứ tự gặp, ⛔ theo thứ tự số *(`1·4·5·2·3`)* · thông điệp + dòng `+` của `471f0ce`/`cf9ae8a`: 0 số TK · ảnh đổi duy nhất `mapping_master_cfg.json`, ghim 3 chỗ cùng commit · đột biến 7/9 bị cắn · `--duong-nen --cong 5436` ĐẠT *(28 = 28, chạy 4040; web 3 = 3, 675)* · `lint-imports` 11 kept · `kiem_tai_lieu` ĐẠT.
**Quét độc lập:** 148.671 chuỗi 8–16 chữ số / 1.041 tệp *(kể cả ruột zip)* ⇒ số cá nhân sót **40 chỗ** *(zip 37 · `P2` 3)*.
Việc kế: Dev sửa `01·04` *(+`02` sau quyết chủ)* ⇒ R2.
