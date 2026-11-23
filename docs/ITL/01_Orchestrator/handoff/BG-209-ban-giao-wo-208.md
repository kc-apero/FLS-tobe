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

## Vòng sửa sau R1 (`KQ-210`) — orchestrator chốt · 2026-11-19
R1: 0 CHẶN · 2 NÊN SỬA · 3 GHI NHẬN. Hợp đồng `GET /gates` chỉ THÊM 1 trường (`lat_bo_nguon`); `do_hd2.py` ⛔ sửa.
- **`CG2-R1-01`** *(`lat_bo` vắng)*: `do_hd2.py` ⛔ cắt lát ⇒ khoá có **0** lần ở tệp thật (3/3 khối đo đều vắng — mẫu số ⛔ rỗng, Đ3). ⛔ đổi cổng sang `null`. Cổng NÓI THẲNG: `da_do` kèm `lat_bo vắng ⇒ coi 0 (phép đo HD2 ⛔ cắt lát)` + `Cong.lat_bo_nguon` ∈ `"vang"` · `"khai"` · `"sai_kieu"` · `""` *(cổng ⛔ đọc khoá: gói chưa đo)*; ra ở `/gates` cạnh `ly_do`. Cha: có phần `vang` ⇒ `vang`. Khoá có mà ⛔ phải số nguyên ≥ 0 *(`None` · `-1` · `True` · `"0"` · `0.0`)* ⇒ `dat=null` + `` `lat_bo` `` trong `ly_do` + `sai_kieu`. Ba ca vắng · 0 · 2 + ca hỏng có bài. *(Xuất `lat_bo` thật từ `do_hd2.py` = WO riêng — orchestrator.)*
- **`CG2-R1-02`** *(khối gói hỏng kiểu)*: `WP-C3a: [1]` trước bị bỏ im ⇒ `C3` `true` nhờ mỗi `C3b`. Nay khối kiểu ⛔ dict ⇒ cổng con ĐÓ hiện `dat=null` + `khối WP-C3a kiểu list ⛔ phải đối tượng JSON`, cha `null`. Chứng ĐỎ-trước: bài mới (5 kiểu + gói con mới `WP-C4a`) ĐỎ trên mã cũ (`KeyError: HD2_WP_C3A`), XANH sau.
- **`-04`** *(M8 `goi ≠ khoá` sống)*: bài ghim ở GÓI CON; chứng cắn: đổi `if b.get("goi") != goi:` → `if False:` ⇒ ĐỎ, trả nguyên ⇒ XANH. **`-05`** *(M13 dây `chay_cua`)*: bài ghim `main()` truyền `tep_hd2` đúng cho `dung_may` *(mặc định · `--tep-hd2 X` · `''`⇒`None`)*; chứng cắn: `tep_hd2=None` cứng ⇒ ĐỎ 2 ca. **`-03`** ⇒ backlog.
- **Q8**: `MONG_PYTEST_TOAN_BO` 3647 → **3667** (= thu thập cây này `--collect-only` ⇒ +20: R1-01 ×10 · R1-02 ×6 · `-04` ×1 · `-05` ×3) cùng commit bài ghim `test_S0_R3_02_…`.

## Sửa tích hợp với H9 (`WP-C4a`) — orchestrator chốt · 2026-11-19 (`CG2-R2-03`)
Gộp `isp/CG2` + nhánh làm việc (đã có H9) ⇒ `--duong-nen` ĐỎ +5 ở `test_isp_gates_hd2.py`. Nguyên nhân: khối `WP-C4a` ⛔ có `tong_o`/`khop` (chỉ `o_so`/`lech`) ⇒ cổng thứ 7 `HD2_WP_C4A` = `null` (đúng luật ⛔ tin mù), và bài CG2 ghim cứng tập 6 cổng.
- **Hợp đồng khối gói (H4)**: mọi gói khai `tong_o` + `khop`. `tools/do_hd2.py`: `WP-C4a` xuất thêm `tong_o` = ô SO ĐƯỢC (**420**, ⛔ tính 196 ô P chữ) · `khop` = `o_so − lech` (**420**); mọi khoá cũ giữ nghĩa. Khối sinh lại bằng `do_hd2.py --goi WP-C4a --dsn $PG_DSN_TEST --ghi` (⛔ sửa tay): chỉ khối `WP-C4a` đổi, thêm `tong_o`·`khop`·`o_khong_so_khac_0` (khoá H9-R1-01 mà bản cũ chưa ghi); khoá gốc + 3 khối kia nguyên.
- **Bài tệp thật**: 7 cổng — `C2·C3·C3a·C3b·C4·C4a` true, `C5` null *(`mong` khai, Đ5)*; `lat_bo_nguon` = `vang` ở 6 cổng đo. Hai bài mới quét `hd2_cong.json`: mọi khối có `tong_o`/`khop` kiểu int (Đ3: ≥ 4 khối) · tập cổng đọc TỪ TỆP (4 cha + mỗi con). Chứng ĐỎ: đặt tệp cũ lại ⇒ cả hai ĐỎ; tệp mới ⇒ XANH. Hai bài oracle `WP-C4a`: `tong_o = o_so = 420`; đột biến 1 ô ⇒ `khop = 419`. Bài tệp tổng hợp (`_tep`) giữ nguyên; `…CHI_co_C2…` thêm `pop("WP-C4a")`.
- **Q8**: xung đột gộp chỉ ở sàn ⇒ lấy bản nhánh làm việc; `MONG_PYTEST_TOAN_BO` **3754** = thu thập thật (3750 + 4 bài mới) · web **675** — cùng commit bài ghim `test_S0_R3_02_…`.
- **Cổng**: `--duong-nen --cong 5446` MỘT lần ⇒ ĐẠT (tập đỏ **28 = 28**, chạy 3754; web 3 = 3, chạy 675) · `lint-imports` 11 kept · `soi_bang_tuyen` 45/45 khớp.
