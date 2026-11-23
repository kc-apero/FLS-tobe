# WO-234 — làm sạch số tài khoản cá nhân ở BẢN HIỆN HÀNH (chủ duyệt 19/11)

| | |
|---|---|
| **Trạng thái** | `MO` |
| **Phát bởi** | orchestrator · 2026-11-19 · theo quyết của chủ 19/11 02:30 ("đồng ý các đề xuất": làm sạch bản hiện hành, ⛔ viết lại lịch sử) |
| **Nhận** | `fls-dev` — phiên cloud Sonnet 5.5 · medium · nhánh `isp/PII` |
| **Dải phiếu** | `BG-238` · `KQ-239` (R1) · `KQ-240` (R2) |

## Phạm vi (đã đo trước — `KQ-178` `C8-R1-06` · `KQ-195` R2 DT6)
- `tests/fixture/cau_hinh/mapping_master_cfg.json` (ảnh DT3): 4 hàng `CN` mang số TK cá nhân thô (+ chữ số đầu số TK thật).
- 3 tệp HTML BA trong `docs/ITL/02_BA/Artifacts/` mang chữ số đầu số TK thật (R2 DT6 liệt kê — đo lại bằng máy quét, ⛔ đoán tệp).
- Quét MỌI tệp đã theo dõi (`git ls-files`) tìm số TK cá nhân: mẫu chuỗi số dài gắn với ngữ cảnh tài khoản (`R | <số>_`, `STK`, `Số TK`, `Bank Account`…) — ⛔ in giá trị (chỉ đếm, tệp, dòng).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | số TK cá nhân ⇒ thay bằng mã che KHÔNG đảo được (`R` hoặc nhãn `TK_CA_NHAN_<n>` thứ tự), giữ được mọi phép đo đang dùng ảnh (bài DT3 · C8 · H4… xanh; checksum ghim cập nhật CÓ CHỦ ĐÍCH, khai từng tệp) | pytest |
| AC-2 | máy quét PII mới `tools/quet_pii_repo.py` (+ bài có ca phá) chạy trên `git ls-files`; ĐẠT = 0 số TK cá nhân; nối vào cổng (khai ở đâu) để tái phạm ĐỎ | pytest + chạy máy quét |
| AC-3 | ⛔ viết lại lịch sử git (chủ chọn bản hiện hành); BG ghi rõ: lịch sử cũ VẪN còn giá trị — rủi ro khai | BG |
| AC-4 | HTML BA: sửa tối thiểu đúng ô/chuỗi (⛔ dàn lại tệp); diff chỉ ở chỗ che | diff |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` |

## Ràng buộc
- ⛔ in số TK ra log/BG/commit message. ⛔ đụng `sao_luu/` · `hien_vat/` (gitignored). Ghi kho THẬT: `KHONG`.
