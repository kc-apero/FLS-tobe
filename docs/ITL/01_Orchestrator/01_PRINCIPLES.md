# 01 — PRINCIPLES: Hiến pháp dự án ITL

**Version:** v0.1 | **Chủ sở hữu:** COO-CFO | **Ưu tiên:** cao hơn mọi tài liệu khác trong 4 kit ITL

Khi bất kỳ tài liệu/quyết định nào mâu thuẫn với file này → file này thắng, hoặc phải sửa file này qua Change Control (`07`) trước.

Hai lớp nguyên tắc: **A** kế thừa từ chương trình FIN ERP (chép có ghim version, `QĐ-ITL-04`) · **B** riêng của dự án ITL.

---

## A · Kế thừa từ chương trình — `P-01..P-08`

> Chép từ program `01_Orchestrator/01_PRINCIPLES.md` **v0.1 (2026-07-17)**. Bản chương trình tăng version → mở CR "trôi kế thừa" (`07` §1 loại 4).

| ID | Nguyên tắc | Áp vào ITL thế nào |
|---|---|---|
| **P-01** | Dữ liệu sạch → phân tích → quyền lợi. Không gắn tiền của ai vào số liệu chưa kiểm chứng. | ITL **là** bước "dữ liệu sạch" của cả chương trình. Không có ITL đáng tin thì mọi phân tích phía sau là cát |
| **P-02** | Milestone = sự kiện vận hành thật, không phải "ship xong tính năng". | Với ITL: milestone = một nguồn khớp oracle, một khối nhập tay bị khai tử, một mắt xích Gsheet bị cắt |
| **P-03** | Phương pháp luận cưỡng chế bằng kiến trúc — điều kiện quản trị ánh xạ vào ràng buộc kỹ thuật (FK, immutability, version pin), không nằm trên giấy. | ITL: `RAW` bất biến + journal append-only + Mapping Master versioned = 3 ràng buộc enforce ở tầng DB (`BA-11`) |
| **P-04** | Tiến hoá, không đập xây lại. Đề xuất "viết lại từ đầu" thứ đang chạy phải qua Diễn đàn quản trị. | ITL **không** viết lại engine P&L (L3–L5 đã chạy). Chỉ code hoá L1–L2 |
| **P-05** | Scenario/quy tắc là **dữ liệu**, không phải code — bản ghi có version, người nghiệp vụ tự thao tác. | Luật chuẩn hoá & phân bổ sống trong `Mapping Master` (reference data versioned), không hardcode trong adapter |
| **P-06** | Fail-loud, không bao giờ lặng lẽ tự sửa. Dữ liệu sai bị chặn ở cổng ingest với lý do rõ; máy không tự sửa số. | Adapter đổi schema nguồn → **dừng và báo**, không âm thầm ra 0 dòng (đã từng làm 3 sheet ra 0 dòng) |
| **P-07** | Con người giữ trạng thái, AI làm công việc. Mỗi phiên AI là công nhân không trạng thái, reset context giữa các task. | Trạng thái sống ở `06`; phiên sau đọc `06` + file được trỏ, không đọc lại hội thoại |
| **P-08** | JIT documentation — chỉ viết spec chi tiết cho giai đoạn sắp làm. | BA chỉ chi tiết `IM0–IM2`; `IM3–IM7` giữ khung + `???` |

## B · Riêng dự án ITL — `P-ITL-01..05`

### P-ITL-01 · Contract-first (quan trọng nhất)
Engine P&L sẽ đọc ITL mới, nên **việc số 0 là đóng băng hợp đồng đầu ra của `ITL Ledge`**: đúng tập cột & ngữ nghĩa mà engine đang đọc từ sổ Gsheet hôm nay. Hợp đồng **reverse-engineer từ reader đang chạy thật**, không thiết kế mới, viết thành schema spec có versioning (`02`). Mọi milestone sau phải khớp hợp đồng ⇒ ngày cutover engine không sửa một dòng code.

> Đây là rủi ro #1 của dự án: **lệch hợp đồng ⇒ cutover gãy.** Test hợp đồng chạy ở *mọi* milestone, không chỉ `IM0`.

### P-ITL-02 · Strangler-fig — thay dần, không big-bang
ITL mới chạy **song song** sổ Gsheet. Mỗi milestone thêm **một** nguồn rồi đối chiếu tới khi khớp (hoặc chênh lệch giải thích được — cash-vs-accrual là chênh lệch **hợp lệ**). Chỉ cắt sổ cũ ở `IM7`. Rủi ro luôn giữ ở mức một-nguồn.

### P-ITL-03 · Oracle-first — nghiệm thu bằng sổ thật, không bằng niềm tin
`ITL RAW` và `ITL ADJUSTED` cũ **vẫn tồn tại** ⇒ đó là **test oracle** sẵn có. Mọi nghiệm thu là đối chiếu **từng dòng + tổng** với oracle. Cấm nghiệm thu bằng "chạy không lỗi". Cấm khai tử sổ Gsheet trước khi oracle được dùng cạn.

> Hệ quả bắt buộc: **đo bảo toàn tiền bằng net theo output-sheet**, KHÔNG cộng dồn cả bảng — rollup chồng làm phồng số. Đây là rủi ro #2.

### P-ITL-04 · Điều chỉnh là bút toán append-only
Vùng ADJUSTMENT (~6.843 ô cột `Final` hôm nay — *không phải 6.843 lần người gõ; xem đính chính §3c*) TO-BE là **journal thêm mới**, không ghi đè `RAW`. `RAW` bất biến. `Final` = **kế toán nhập/sửa trực tiếp** *(bỏ tầng `MID`, `QĐ-owner-0820`)*. Mọi dòng ITL giữ khoá nguồn + chuỗi biến đổi ⇒ truy vết được, sửa được mà không hỏng gốc. Chi tiết: [`_BA_UPDATE_ROADMAP §3c`](../02_BA/_BA_UPDATE_ROADMAP.md).

### P-ITL-05 · Không phát minh schema
Khuôn giao dịch chuẩn **đã tồn tại**: 36 cột của sheet `Transaction Mapping L1`. Adapter mỗi nguồn = hàm map *cột nguồn → cột canonical*. Nguồn thiếu trường thì **để trống có kiểm soát**, không bịa. Cấm tạo tập cột mới "cho gọn".

## Changelog
- v0.1 (2026-08-18): Khởi tạo — chép `P-01..P-08` (ghim program v0.1) + 5 nguyên tắc riêng `P-ITL-01..05` dẫn xuất từ `NGUỒN-BUILD §0`, `§X`.
