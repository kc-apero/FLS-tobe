# WO-132 — ISP 3.1.2 · Step 13 · H4: KS.CA · parity CA.GL ↔ đáp án 406 mọi kỳ (cổng HD2 đầu tiên)

| | |
|---|---|
| **Trạng thái** | `DANG_LAM` — giao phiên cloud 18/11 |
| **Phát bởi** | orchestrator (phiên điều phối ISP) · 2026-11-18 |
| **Nhận** | `fls-dev` làn **BE-HC** — **phiên cloud** (Opus 4.8 · medium) · cụm PG **5435** · nhánh `isp/H4` |
| **Nền** | ngọn nhánh làm việc `claude/bold-galileo-zukpaf` (đã gộp H1 · C1 · DT2 · DT4 — đủ phụ thuộc ISP) |
| **Dải phiếu** | `BG-133` · `KQ-134` (R1) · `KQ-135` (R2) · `KQ-136` (R3) |

## Vì sao
- ISP **Step 13 · H4** — nguồn sự thật duy nhất (Goal · Scope · H4-B1…B3 · mục 8). Phụ thuộc H1 · DT4 · DT2 · C1: đã gộp (DT4 18/11, R3 `KQ-115`).

## Spec phải đọc
| Tệp | Mục |
|---|---|
| ISP v3.1.2 | §1 · §2.1 · **Step 13** (· Step 1 H1 · Step 12 DT4) |
| `01_Orchestrator/isp-3.1/CALC_ZONE_406.md` | bản đồ BM…BT · **hai ngữ nghĩa tra tỷ giá** (INDEX/MATCH ⇒ ô rỗng · SUMIFS ⇒ 0/`#DIV/0!` · tháng trùng ⇒ cộng đôi) · ghi chú §H4: dung sai số thực ↔ `Decimal` phải khai trong `mong`; ô AS-IS rỗng/0/`#DIV/0!` do tháng thiếu = **lệch CÓ TÊN** (⛔ đếm là lỗi FLS, ⛔ đếm là khớp) |
| `tests/fixture/dap_an/gl_406.json` (DT4) · `BG-112` · `KQ-113/114/115` | 7.883 dòng (hàng 10…7892) · khoá `dong_sheet` + `ky` + `itl_id` · **4 hàng `itl_id = "#N/A ()"`** (bảng phụ `itl_id_lech`, `dong_sheet` 6684 · 6836 · 7500 · 7832) ⇒ nối theo `dong_sheet` cho 4 hàng này, khai lệch có tên · **4 kỳ lệch có tên** với sổ: 2026-05 (239/537) · 2026-06/07/08 (0) ⇒ chỉ so phần 406 có |
| `fls/bao_cao/gl.py` (H1) · `KQ-074` | `tinh_gl`, `ThieuTyGia`, `TienKhongHuuHan`; R3 H1 khuyên: khai dung sai cột **BT theo độ lớn lũy kế**, ⛔ theo giá trị ô |
| `docs/ITL/04_Test/review/de_xuat/KQ-074_h1_r3_bai_de_xuat.py.txt` | bài đề xuất `H1-R3-01` (pickle lớp lỗi) · `-02` (nhãn Nợ/Có) |
| `fls/cau_hinh/fx.py` (C1) · `tests/fixture/cau_hinh/ix_fx.json` (DT2) | tỷ giá đọc từ ẢNH (⛔ kho — I2) |
| `CLAUDE.md` | Đ1–Đ5 · Riêng tư |

## Quyết định orchestrator
- **Trước tiên (commit riêng, cùng làn BE-HC):** sửa `H1-R3-01` (`ThieuTyGia` · `TienKhongHuuHan` pickle/copy được — `__reduce__`, giữ trường) và `H1-R3-02` (bài ghim `nhan` phía Nợ/Có) — R3 H1 khuyên "nên sửa trước H4"; dùng bài đề xuất ở `de_xuat/` (chép vào `tests/`, ĐỎ trước).
- Dòng sổ cho H1 lấy từ nguồn ISP chỉ định (đọc ISP Step 13 + `fls/oracle/`); ⛔ đọc kho thật ghi; nếu ISP mơ hồ ⇒ dừng, hỏi kèm khuyến nghị A/B.
- `hd2_cong.json` = hợp đồng cho CG2: khai khoá rõ ràng, chỉ THÊM về sau.

## Tiêu chí nghiệm thu
| AC | Mong |
|---|---|
| AC-1 (H4-B1) | `tools/do_hd2.py --goi WP-C2`: số ô so > 0 và = số ô đáp án phần so được; lệch liệt kê theo (kỳ, dòng, cột) + tên lệch (tháng thiếu tỷ giá · `itl_id` `#N/A` · kỳ vắng ở 406) |
| AC-2 (H4-B2) | đáp án rỗng ⇒ ĐỎ `0 ô` (Đ3) |
| AC-3 (H4-B3) | MONG lệch khai trước; khác ⇒ ĐỎ cả hai chiều (Đ5); dung sai khai trong `mong` (BT theo độ lớn lũy kế) |
| AC-4 | `H1-R3-01/02` đã sửa, bài ĐỎ-trước |
| AC-5 (Q8) | sàn `MONG_PYTEST_TOAN_BO` + bài ghim cùng commit |

## Dữ liệu
- Ghi kho THẬT: `KHONG`. ⛔ Drive.
