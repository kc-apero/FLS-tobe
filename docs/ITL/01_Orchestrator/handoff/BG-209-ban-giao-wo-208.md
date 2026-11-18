# BG-209 — Bàn giao WO-208 · ISP Step 30 · CG2 · cổng HD2 theo gói vào `GET /gates`

| | |
|---|---|
| Phát bởi | fls-dev #FE (phiên cloud) · 2026-11-18 · nhánh `isp/CG2` (nền `e2ee232`) |
| Gửi | fls-test (R1) |

## Đã làm
`fls/repo/doc_bao_cao.py`: `doc_cong_hd2(tep_hd2)` (hàm thuần) + `doc_cong(…, tep_hd2=)` thêm cổng cuối nhóm HD1. Đường dẫn tệp **TRUYỀN VÀO** (khuôn CG1): `chay_cua.py --tep-hd2` (mặc định `hd2_cong.json` ở rìa) → `dung_may(tep_hd2=)` → `YeuCau.tep_hd2`. Chạm thêm `fls/api/cua.py` · `fls/api/xu_ly.py` · `tools/chay_cua.py` (đường truyền, ngoài danh sách tệp của WO — bắt buộc để truyền tệp). ⛔ sửa `tools/do_hd2.py` · ⛔ di trú · ghi kho thật: KHÔNG. Bài: `tests/api/test_isp_gates_hd2.py` (31 bài).

## AC-4 · cách gộp cha/con (Đ4 — số đếm gì)
- **Cổng = HỢP** của 4 cha khai sẵn (`HD2_WP_C2/C3/C4/C5`, luôn có mặt) và mọi khối trong tệp khớp `WP-C<số>[chữ]` (`WP-C2` ở cấp cao nhất; `WP-C3a` … là khoá lồng). Gói con mới (`WP-C3c`, `WP-C4a`) **tự hiện**, ⛔ sửa mã (có bài).
- **Cha gộp phần** (con, + khối riêng nếu có): một phần `false` ⇒ `false` (thắng `null`); còn phần `null` ⇒ `null`; còn lại `true`; không phần nào ⇒ `null`.
- **Cổng lá đếm Ô đáp án** (`khop/tong_o`); **cổng cha có con đếm GÓI CON đạt** (+ Σ ô). Cha chỉ có khối riêng (`WP-C2`) = chính cổng lá. Số cổng của tuyến = 4 cha + số gói con có trong tệp (hiện 6).
- Lá: `lat_bo > 0` ⇒ `false` (tệp ghi `dat=true` cũng bị ghi đè); sai kiểu `lat_bo`/`dat`/`goi`, `tong_o=0` (Đ3), `khop≠tong_o`, thiếu `khop`/`tong_o` mà `dat=true` ⇒ `null` kèm lý do. Tệp vắng/hỏng/không truyền ⇒ 4 cha `null`, lý do chỉ có TÊN tệp.
- Ghi chú: tệp thật **chưa có khoá `lat_bo`** (`do_hd2.py` chưa xuất) ⇒ cổng coi vắng = 0; khoá có mặt thì được tin. Cần H-làn ghi `lat_bo` nếu muốn đo lát thật.

## Kết quả trên tệp thật (`hd2_cong.json`)
`HD2_WP_C2` true 63016/63016 ô · `HD2_WP_C3` true (2/2 gói con · Σ 216760 ô) · `HD2_WP_C3A` true 205175/205175 · `HD2_WP_C3B` true 11585/11585 · `HD2_WP_C4` null · `HD2_WP_C5` null.
Hợp đồng cũ: chỉ THÊM phần tử (bài đòi các cổng cũ giữ nguyên thứ tự); `soi_bang_tuyen.py` ĐẠT 45/45 tuyến.

## Chứng ĐỎ
Trước mã: 30/31 bài hỏng (chưa có `doc_cong_hd2` · `tep_hd2`). Chiều ĐỎ có bài: tệp phá (7 ca tự mâu thuẫn), `lat_bo` (4 kiểu sai), cha false/null/true.

## Q8
`MONG_PYTEST_TOAN_BO` 3616 → **3647** (= thu thập cây này; +31) · `MONG_PYTEST_WEB` giữ **675** (⛔ thêm bài web) · bài ghim `test_S0_R3_02_…` cùng commit.

## Cổng đã chạy
`--duong-nen --cong 5446` (một lần): **ĐẠT** — toàn bộ `12 failed · 3619 passed · 2 xfailed · 14 errors` = tập đỏ 28 = 28 node id đường nền (thêm 0 · bớt 0), chạy 3647 (≥ 3647) · web `3 failed · 672 passed`, 3 = 3 node id, chạy 675 (≥ 675). `lint-imports` 11 kept · 0 broken · `soi_bang_tuyen` 45/45.
