# KQ-342 — R1 vòng 2 `WO-329` / `BG-330` *(ISP 3.1.2 · AG — 4 agent vận hành Voi gọi API)*

| | |
|---|---|
| **Kết quả** | **ĐẠT** — **0 CHẶN · 0 NÊN SỬA** · 4 GHI NHẬN ⇒ **sẵn sàng R2 cuối** |
| **Phát phiếu** | `fls-test` *(vai KIỂM — ⛔ sửa mã · ⛔ gọi API thật · ⛔ ghi kho thật)* · 2026-11-23 · `isp/AG` `b1e08a4` + cây gộp thử với `origin/claude/bold-galileo-zukpaf` `8f727ac` *(ISP 48/48, đã gộp I2)* · cụm 5447 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_AG.md` *(mục "R1 vòng 2", mã `AG-R1v2-01…04`)* |
| **Gửi** | `ORCHESTRATOR` — mở R2 cuối trên cây gộp thử |
| **Điều kiện ĐẠT** | `KQ-331` v0.2 mục "Điều kiện ĐẠT ở R1 vòng sau" — 4/4 đạt |

## Quyết chủ đã đối chiếu
C1 = A *(Opus 5.5 · G0 bóng · ⛔ `fallbacks`)* ✓ · C2 = A4 MÃ THUẦN tới G1 ✓ *(A4.01–04 `loai: ma` **4/4**)* · C3 = ngưỡng đề xuất, A2.04 siết — thuộc G1, ⛔ chặn hôm nay *(`AG-R1-10` giữ GHI NHẬN)* · **C4 thay**: chủ xác nhận 23/11 ~06:00 *"cho agents đọc toàn bộ"* — mặc định `mo` ✓ *(đo: nội dung + số TK đi nguyên văn, chỉ bỏ `Email Address`)*, bộ che là **tuỳ chọn** · C5 bể giữ riêng = `WO-338` ✓.

## Bảng kiểm *(mỗi mục một số đo · nhãn đếm gì)*

| # | Kiểm | Đo được | Kết |
|---|---|---|---|
| 1 | `AG-R1-01` report nói rõ chứng minh gì | `report.html` *(cây gộp, sinh bằng `chay_agent_voi.py`)*: khối §0 *"chứng minh gì / ⛔ chứng minh gì"* **2** lần chữ · "mô hình GIẢ" **5** · `gia-lap` **4** · `claude-opus-5-5 ✅` **0** · ghim ⇒ *"CHƯA gọi thật"* **3**. KẾT tách hai mẫu số: **ĐỘC LẬP `voi` 557/557** · **VÒNG TRÒN `hd2·cong·nguon` 74/74** · tổng **631** *(= dev báo)*. **Đột biến tự chứng minh** *(bản sao `git archive`, trả nguyên, `diff` = 0)*: **M1** `hd2_cong.json WP-C3a.dong_so`+1 ⇒ KẾT vẫn ĐẠT, độc lập **557/557** y nguyên, vòng tròn **74/74** *(⛔ bị đếm là khớp độc lập)* · **M2** `voi_so_luong.json tong.map_fls`+7 ⇒ ĐỎ `lệch 1` ở nhóm độc lập · **M3** ảnh `pm_join.json` bỏ 1 dòng ⇒ ĐỎ · **M4** engine `do_voi_so_luong.py:620` `+=1`→`+=2` ⇒ ĐỎ *(M3/M4 ĐỎ qua `KhongCoBanGhi`, xem `AG-R1v2-03`)* | **ĐẠT** |
| 2 | `AG-R1-02` cây gộp | `git merge b1e08a4` lên `8f727ac`: xung đột **2 tệp** — chỉ sàn `MONG_PYTEST_TOAN_BO` *(4887 ↔ 4928)*; giải = thu thập thật **4.958** ⇒ **0** dấu xung đột còn lại *(`AG-R1v2-02`)*. `tests/agent` **71 passed** *(71 = 52 + 19)*. `test_dung_moi_truong_isp.py` **60 passed** | **ĐẠT** |
| 3 | `AG-R1-03`/`11` bộ che tuỳ chọn + ZDR | **14 ca khó BỊA** của KIỂM *(⛔ trùng ca dev: TK cách 3 nhóm · trộn `.`/`-` · gạch+cách · slash · liền 13 số · hai cách · ĐT ngoặc · tên Hoa-thường giữa câu · tên HOA · tên Hoa-thường 4 từ · email HOA · email+tên · ĐT chấm · tên có dấu)*: `che_het` lọt **0/14** · `che_noi_dung` lọt **3/14** *(slash · hai cách · tên có dấu — ngoài phạm vi KQ-331, `AG-R1v2-01` GHI NHẬN, ⛔ mặc định)* · ca KQ-331 *(`.`/`-`/cách đơn, Hoa-thường, email hoa)* **0 lọt** · che nhầm ngày/kỳ/mã PM **0**. Mặc định = `mo`, nguyên văn giữ ✓. 13 tổ hợp chốt: MỞ đúng **1** *(đủ 5 chốt)* + **2** *(`che_*` ⛔ đòi ZDR)*; CHẶN **9**; `anthropic` nhập: **không**. Đột biến: M6 `CHE_DO_CAN_ZDR=()` ⇒ **1 ĐỎ** · M7 ngưỡng che 6→60 ⇒ **7 ĐỎ** · M8 lớp 2 9→90 ⇒ **5 ĐỎ** | **ĐẠT** |
| 4 | `AG-R1-05`/`06` | §6 Độ phủ: `voi` **557/1.045** lá *(số **318/660**)* · `hd2` **30/1.312** *(số **30/915**)* — khớp KQ-331. A4.01–04 `loai: ma`; `can_mo_hinh(A4)` = False; `ncc_cho("that")` dựng **3** nhà cung cấp *(A1–A3, `anthropic` · `claude-opus-5-5`)*, **0** Gemini *(`tao_that` bị thay bằng bản ghi — ⛔ API)*. Đột biến M5 A4.02 về `loai: lam` ⇒ **3 failed + 7 errors** · M9 `NGUON_DOC_LAP += hd2` ⇒ **3 ĐỎ** · M10 `NGUON_THAT += gia-lap` ⇒ **2 ĐỎ** | **ĐẠT** |
| 5 | Thẻ + 4 zip | sinh lại `sinh_the_agent.py --zip` trên bản sao: thẻ + `report` + `phat_lai` **0** tệp khác; 4 zip cùng danh sách **38** tệp *(7·14·9·8)*, nội dung khác **0/38**, skill `.md` = nguồn **20/20** byte; bài checksum thẻ **10 passed**. Byte zip khác vì mtime *(`AG-R1v2-04`)* | **ĐẠT** |
| 6 | Cây gộp thử — cổng cuối | `bash tools/dung_moi_truong_isp.sh --duong-nen --cong 5447` **MỘT lần, một mình**: **`KẾT: ĐẠT`** — toàn bộ `12 failed · 4930 passed · 2 xfailed · 14 errors` ⇒ **28 = 28** *(thêm 0 · bớt 0 · chạy 4958 ≥ sàn 4958 · skipped 0 · deselected 0)* · web `3 failed · 687 passed` ⇒ **3 = 3** *(chạy 690)* · lint **11 kept** · di trú **27/27**. `kiem_tai_lieu` ĐẠT *(505 file · 3.016 bảng)* · `lint-imports` **11 kept, 0 broken** · `quet_pii_repo` **0 chỗ · 0 tệp** | **ĐẠT** |

Mẫu số các phép *(Đ3/Đ4)*: 14 ca che *(13 có chuỗi nhạy trong đầu vào gốc; ca 14 "tên có dấu" bị JSON thoát — đo bằng chuỗi giải mã)* · 13 tổ hợp chốt · 10 đột biến M1–M10 *(trả nguyên: `diff` bản sao ↔ cây gộp = 0)* · 4 zip/38 tệp · 631 ô.

## Phát hiện
| Mức | Số | Mã |
|---|---|---|
| CHẶN | **0** | — |
| NÊN SỬA | **0** | — |
| GHI NHẬN | **4** | `AG-R1v2-01` bộ che tuỳ chọn lọt 3/14 ca ngoài phạm vi *(slash · hai cách · tên có dấu)* · `-02` gộp lại luôn xung đột sàn *(nhắc lúc gộp)* · `-03` đột biến engine/ảnh ĐỎ qua vân tay, ⛔ qua "lệch" · `-04` zip ⛔ tái lập byte |

Mọi hàng cũ `AG-R1-01 · 02 · 03 · 05 · 06 · 11` → **đóng** *(bảng ở sổ)*; `04 · 07 · 08 · 09 · 10` giữ GHI NHẬN.

## Ghi chú vai KIỂM
Cây thử `thu/AG` đã gỡ, **⛔ commit**; mọi đột biến ở bản sao. Chỉ **2 tệp** thêm vào nhánh bước: phiếu này + sổ. ⛔ chưa chạy *(ngoài phạm vi, như KQ-331)*: `kiem_so_song.py` · `khop_owner.py --kiem`. Lỗi của chính KIỂM: lần dựng worktree đầu sai thứ tự đối số *(không ảnh hưởng đo)*.

**Kết luận: ĐẠT, 0 CHẶN ⇒ sẵn sàng R2 cuối** *(cây gộp thử: gộp `b1e08a4` lên ngọn nhánh làm việc; nhớ đặt sàn = thu thập thật cây gộp — `AG-R1v2-02`)*.
