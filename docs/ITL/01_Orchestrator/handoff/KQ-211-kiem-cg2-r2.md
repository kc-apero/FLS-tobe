# KQ-211 — biên bản kiểm vòng sửa sau R1 *(R2 CUỐI · Step 30 · CG2)*

| | |
|---|---|
| **Thuộc** | `KQ-210` · `BG-209` *(mục "Vòng sửa sau R1")* · `WO-208` · nhánh `isp/CG2` @ `64acb86` |
| **Kiểm bởi** | `fls-test` · 2026-11-19 *(⛔ sửa mã; cây gộp thử `thu/CG2` ⛔ commit)* |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(sổ `SO_PHAT_HIEN_ISP-3.1_CG2.md` v0.2: `R2-01` xác nhận đóng · `R2-02` · `R2-03` mở)* |

## Cây gộp thử *(`origin/claude/bold-galileo-zukpaf` @ `4a13162` + `--no-ff isp/CG2`)*
- **Xung đột 2 tệp** *(đúng loại dự báo)*: `tools/dung_moi_truong_isp.sh` *(hằng `MONG_PYTEST_TOAN_BO`)* · `tests/test_dung_moi_truong_isp.py` *(bài ghim hằng)*. Giải: lấy bản nhánh làm việc, rồi đặt sàn = số bài THU THẬP thật.
- **Sàn:** `pytest --collect-only` = **3.701** bài ở 256 tệp *(web 675 ở 58 tệp)* — nhánh làm việc 3650 + 51 bài của CG2 *(⛔ cộng tay: đo)*. Đặt 3650 → **3701** ở script + bài ghim; 111 bài (`test_isp_gates_hd2` + `test_dung_moi_truong_isp`) xanh.
- **Cổng `GET /gates` trên tệp thật** *(tên · `dat` · `lat_bo_nguon`)*: `HD2_WP_C2` true·vang · `HD2_WP_C3` true·vang · `HD2_WP_C3A` true·vang · `HD2_WP_C3B` true·vang · `HD2_WP_C4` null·"" · `HD2_WP_C5` null·"".
- **H9 / `WP-C4a`:** ⛔ có trong cây *(H9 chưa gộp vào nhánh làm việc; `hd2_cong.json` chỉ có `C3a`·`C3b`)* ⇒ `HD2_WP_C4A` ⛔ hiện, `C4` null *(đúng: chưa đo)*. Giả lập tay khối `WP-C4a` hợp lệ ⇒ `C4A` true · `C4` true, tự hiện không sửa mã → `CG2-R2-03`.

## Soát
1. **`R1-01` · `-02` đóng thật.** Đột biến R1 `WP-C3a: [1]` ⇒ `C3A null` *(lý do có tên)* · `C3 null` ⛔ `true`. `lat_bo` trên C3a: vắng ⇒ `true`·`vang` · `0` ⇒ `true`·`khai` · `2` ⇒ `C3A` + `C3` `false` · hỏng `"x"`/`-1`/`True`/`None` ⇒ `null`·`sai_kieu`. 4 ca đủ; mẫu số mỗi ca ≥ 1 lá *(Đ3)*.
2. **Bài ghim `-04` · `-05` cắn:** bỏ chốt `goi` ⇒ ĐỎ; `chay_cua` `tep_hd2=None` ⇒ ĐỎ.
3. **Hợp đồng cũ chỉ THÊM:** `tests/api -k gate|cong|hd2|cg1` xanh *(bài CG1)*; `soi_bang_tuyen` 45/45.
4. Xem trên.
5. **Đột biến 6/6 CHẾT** *(bản sao tại cây thử, trả nguyên bằng `git checkout`)*: bỏ kiểm kiểu khối · `nguon` luôn `khai` · bỏ chốt `goi` · bỏ `lat>0⇒false` · bỏ `lat<0` · `chay_cua` `tep_hd2=None`. *(Chạy `-x`: mỗi ca ĐỎ ở 1 bài đầu, ⛔ đối chiếu tên bài.)*
6. **Cổng:** `--duong-nen --cong 5446` *(1 lần, một mình)* **ĐẠT** — 12F·14E·2X = 28 = 28 node id *(thêm 0 · bớt 0)*, chạy **3701** *(mong ≥ 3701)*; web 3 = 3, chạy 675 · `lint-imports` 11 kept · 0 broken · `kiem_tai_lieu` K1–K6 ĐẠT *(339 file)* · `soi_bang_tuyen` 45/45.

## Ghi nhận *(⇒ backlog)*
`R2-02` cha lấy nguồn `vang` nếu bất kỳ con `vang` *(lệch nhẹ khi cha `false`)* · `R2-03` kiểm lại `HD2_WP_C4A` khi H9 gộp · `R1-03` *(danh sách gói con mong đợi)* vẫn mở. Việc `do_hd2.py` xuất `lat_bo` thật = WO riêng *(orchestrator)*.
