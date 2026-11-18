# WO-168 — ISP 3.1.2 · bước DATA phụ cho H5: ảnh `cfa1_dau_vao` (dòng sổ ITL Ledge 18/11 → LE · HD Final · ngày · tiền)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 (Sonnet · 2 vòng review) |
| **Phát bởi** | orchestrator · 2026-11-18 (errata ㉓ cho ISP: Step 16 · H5 cần ảnh đầu vào theo dòng — ⛔ ghi ở Step 15) |
| **Nhận** | `fls-dev` làn **DATA** — phiên cloud **Sonnet 5.5** medium · cụm PG **5437** · nhánh `isp/DTCF` |
| **Nền** | ngọn nhánh làm việc (đã gộp DT5 — đáp án `cfa1_daily.json` 5 LE × 74 mã × 760 ngày; công cụ chung `tools/dong_bang_sheet.py`) |
| **Dải phiếu** | `BG-169` · `KQ-170` (R1) · `KQ-171` (R2 cuối). Số trống kế tiếp: **172** |

## Vì sao
H5 (`WO-164`, Opus 5.5) DỪNG đúng luật: repo ⛔ có nguồn mang **LE + ngày + HD Final + tiền** theo từng dòng sổ mà ⛔ đọc đáp án (quét 17 ảnh `tests/fixture/`: chỉ 2 ảnh có LE — đều là đáp án). Orchestrator chốt **A**: bước DATA riêng đóng băng ảnh đầu vào.

## Nguồn (khoá SA chỉ-đọc; env `FLS_GSHEETS_SA_JSON_B64`/`FLS_GSHEETS_SA_JSON`; `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`; python `-I`)
- Tệp CSV `ITL Ledge` 18/11 trên Drive `1U-IQVOXBbGE6X6n0i0mi3IG9VWc9J_Ap` (người dùng tải 09:29 UTC; `files.get?alt=media`, scope `drive.readonly`): tiêu đề hàng **7**, dữ liệu từ hàng **10**; loại 22 hàng đuôi 0 ô khoá (12600–12621) như WO-156.
- Cột lấy: `A` Ngày chứng từ · `D` Đơn vị tiền tệ · `E` PS Nợ · `F` PS Có · `G` Tài khoản (**⇒ tách LE bằng `fls/repo/man_ghep.py::tach_nguon` rồi BỎ tk/bank — ⛔ lưu số tài khoản**) · `ITL ID` · `Budget Code (HDCode)` khối **Final**. ⛔⛔ `B` Số chứng từ · `C` Diễn giải · cột ngoài danh sách.
- CSV là giá trị HIỂN THỊ: ngày ⇒ chuẩn hoá về ISO (khai định dạng gặp được, ĐẾM ô ⛔ đọc được); tiền 2 số lẻ (bài học `DT1BM-R1-01`).

## Tiêu chí nghiệm thu
| AC | Mong | Cách đo |
|---|---|---|
| AC-1 | `tests/fixture/dap_an/cfa1_dau_vao.json` (hoặc `tests/fixture/cfa1_dau_vao.json`): mỗi dòng `{dong_sheet, itl_id, ngay, le, hd_final, tien_te, ps_no, ps_co}`; số dòng = 12.590 (mốc WO-156) — khác ⇒ dừng, báo | cổng `dong_bang_sheet.py … --mong` + pytest — ĐỎ trước |
| AC-2 | `tach_nguon` lỗi khuôn ⇒ ĐẾM + khai theo nhóm (⛔ đoán LE); tập LE đo được khai trong ảnh; HD Final ∉ cây ATL 74 ⇒ đếm + khai | pytest |
| AC-3 | **GROUP:** đáp án 409 có 5 khối LE (`GROUP` · `SGO2` · `SGO1` · `BGO2` · `HGO6`). ĐO (⛔ khai bừa) GROUP = Σ LE nào khớp đáp án nhất trên dữ liệu đầu vào (thử: Σ mọi LE; Σ 4 LE kia; Σ theo pháp nhân Việt Nam…) — báo bảng ứng viên × số ô khớp; ⛔ chốt — orchestrator/BA chốt | báo cáo |
| AC-4 | PII: 0 cột Số CT/Diễn giải/Email/số TK; máy quét có ca phá; lời lỗi ⛔ in ô (luật `DT5-R1-02`) | pytest |
| AC-5 (Q8) | nâng `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit | `--duong-nen` MỘT lần cuối |

## Dữ liệu
Ghi kho THẬT: `KHONG`. Bản thô chỉ `/tmp` phiên (chmod 700), XOÁ khi xong; ⛔ commit; ⛔ in giá trị ô.
