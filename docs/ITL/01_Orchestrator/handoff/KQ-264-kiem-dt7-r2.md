# KQ-264 — R2 CUỐI kiểm `WO-261` · `BG-262` · ISP Step 31 · DT7 *(đáp án PLA, PD 414–419)*

**Kết luận: ĐẠT — 0 CHẶN · 0 NÊN SỬA · 10 GHI NHẬN ⇒ backlog** *(9 của `KQ-263` + `DT7-R2-01`)*. Sổ: `04_Test/review/SO_PHAT_HIEN_ISP-3.1_DT7.md` (v0.2). Đo trên **cây gộp thử** `thu/DT7` *(nhánh làm việc `96d6ebf` + `isp/DT7` `5d6881f`, cụm `5447`; ⛔ commit cây này)*. Nguồn = sổ P&L `19NNTb…` *(chủ 22/11)*.

| Việc | Kết |
|---|---|
| Xung đột gộp | **2 tệp**: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(sàn 4278 ↔ 4321)* ⇒ gộp tay, **sàn = thu thập thật cây gộp = 4.332** *(4.278 + 54)*; web 681; 17 tệp còn lại gộp sạch |
| (1) Ảnh PLA ×6 + `_pla.py` + khuôn | C13/H7/F5 chạm **0**; `test_dap_an_pla.py` **48 passed**; `tu_kiem` Daily lệch **4** · YHQM **0** · KPI **510** + **206** *(đúng mong)* |
| (2) Ảnh cũ | đổi byte **0/22** ảnh `dap_an` cũ; khuôn cũ đổi **0** |
| (3) `-02`·`-03`·`-09` | ⛔ nâng: `fls/` + `tools/` ngoài khuôn dùng `LOAI_MA`/ảnh PLA = **0** *(Đ1)* ⇒ chưa đo được hại H8; ảnh đã ghim `loai` + `checksum` ⇒ vẫn GHI NHẬN |
| (4) Đột biến mới *(`git archive` cây gộp thử)* | **7/8 cắn**; sống **N5** *(`SERIAL_MOC` +1 ⇒ 178 xanh)* ⇒ `DT7-R2-01` |
| (5) `--duong-nen --cong 5447` *(một lần, một mình)* | toàn bộ `12 failed · 4304 passed · 2 xfailed · 14 errors`, tập đỏ **28 = 28** *(thêm 0 · bớt 0)*, chạy 4332 ≥ 4332; `tests/web` **3 = 3**, chạy 681 ≥ 681 · `lint-imports` 11/0 · `kiem_tai_lieu` ĐẠT · `soi_bang_tuyen` 48 khớp · `quet_pii_repo` 0 |

**Gộp được:** ĐẠT ⇒ orchestrator gộp `isp/DT7` *(đặt sàn 4.332 như trên)*. **Backlog:** `-01` `SHQ2` phần dư ⇒ WO H8 · `-07` errata AP mốc 20/10 · `-08` H8 cần HR Y/H/Q/M? · `-02·03·09·R2-01` bài ghim hằng khuôn/cột không tiêu đề · `-04·05·06` sửa chữ BG.
