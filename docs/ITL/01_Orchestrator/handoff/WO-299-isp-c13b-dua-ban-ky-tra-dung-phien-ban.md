# WO-299 — ISP 3.1.2 · bổ sung C13 (C13b): `dua_ban_ky` trả ĐÚNG phiên bản vừa chèn khi chạy song song

| | |
|---|---|
| **Trạng thái** | `MO` — viết 22/11 ~10:30 UTC; giao khi có ô trống (luật D ≤ 3) |
| **Phát bởi** | orchestrator · 2026-11-22 |
| **Nhận** | `fls-dev` làn **BE-CF** — phiên cloud Sonnet 5.5 · medium · nhánh `isp/C13B` |
| **Nền** | ngọn nhánh làm việc (C13 đã gộp 20/11 `0543792`) |
| **Dải phiếu** | `BG-300` · `KQ-301` (R1) · `KQ-302` (R2 cuối). Số trống kế tiếp sau dải: **303** |

## Vì sao — đo được
- `--duong-nen` của lượt gộp H8 (22/11) ĐỎ **thêm 1**: `tests/cau_hinh/test_ban_ky_pg.py::test_C13_R1_02_dua_ban_SONG_SONG_cung_noi_dung_dung_1_phien_ban_va_khac_noi_dung_ra_phien_ban_lien_tuc` — `assert sorted(kq) == [1..8]` ⇒ `[1, 3, 3, 4, 5, 6, …]`.
- Đo chập chờn (orchestrator): chạy riêng khi máy đang tải (cổng chạy song song) **1/8** đỏ; máy rảnh **0/30** trên ngọn remote (chưa H8) và **0/30** trên HEAD có H8. Diff `origin..HEAD` trên `fls/repo` · `fls/cau_hinh` · `tests/cau_hinh` = **rỗng** ⇒ lỗi CÓ SẴN từ C13, ⛔ do H8.
- Gốc (đọc mã `fls/repo/cau_hinh_repo.py:790-811`): `dua_ban_ky` cấp `n = len(cu) + 1` và chèn **trong** `conn.transaction()` có `pg_advisory_xact_lock`, nhưng **trả** `_sk_ban_ky(conn, k)[-1]` **SAU** khi khối giao dịch kết thúc ⇒ khoá đã nhả, luồng khác có thể chèn bản `n+1` trước lần đọc ấy ⇒ hàm trả phiên bản CỦA LUỒNG KHÁC. Kho có thể vẫn đúng (bài còn khẳng định `doc_ban_ky` = 1…8 — đo lại), nhưng **giá trị trả về sai** ⇒ engine H14 (bên gọi) có thể báo/ký nhầm phiên bản. `ky_ban` (dòng 814+) cùng mẫu đọc-sau-giao-dịch — kiểm luôn.
- R1/R2 C13 (`C13-R1-02` đóng) chỉ chạy 5/5 khi máy rảnh ⇒ ⛔ bắt được (Đ3: phép đo xanh trên mẫu quá nhỏ).

## Tiêu chí nghiệm thu
| AC | Mong *(đo được)* | Cách đo |
|---|---|---|
| AC-1 | `dua_ban_ky` trả ĐÚNG bản nó vừa chèn (hoặc bản trùng checksum khi `khong_doi`) — đọc TRONG giao dịch đang giữ khoá, hoặc dựng từ `n`/`ck` đã ghi; `ky_ban` tương tự | pytest |
| AC-2 | bài ép đua TẤT ĐỊNH (⛔ dựa may rủi tải máy): vd. chèn bản `n+1` từ kết nối khác ngay sau khi khối giao dịch của luồng A kết thúc và trước lần đọc trả về (móc/patch điểm giữa) ⇒ ĐỎ trước sửa, xanh sau | pytest |
| AC-3 | bài song song cũ chạy **≥ 50 lần dưới tải** (vd. 4 tiến trình pytest đồng thời) ⇒ 0 đỏ; ghi lệnh + số vào BG | pytest lặp |
| AC-4 | ⛔ đổi hợp đồng tuyến `report/snapshot` (C13 · F7); bài F7/C13 cũ xanh | pytest |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit; `--duong-nen` ĐẠT | `--duong-nen` |

## Ràng buộc
- ⛔ di trú · ⛔ đổi khoá advisory (đúng) · ⛔ đổi tuyến. Ghi kho THẬT: `KHONG`.
