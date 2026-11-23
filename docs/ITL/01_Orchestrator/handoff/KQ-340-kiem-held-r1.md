# KQ-340 — R1 `WO-338` / `BG-339` *(ISP 3.1.2 · HELD — bể giữ riêng A cũ ↔ B hiện tại cho A2.04)*

| | |
|---|---|
| **Kết quả** | **TRƯỢT** — **2 CHẶN · 4 NÊN SỬA · 4 GHI NHẬN** |
| **Phát phiếu** | `fls-test` · 2026-11-23 · `isp/HELD` `4407935` + cây gộp thử `05d7a97` + AG `c4c9d40` + `4407935` · cụm 5444 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_HELD.md` *(`HELD-R1-01…10`)* |
| **Gửi** | `ORCHESTRATOR` → `DEV` làn DATA *(vòng sửa)* |

## Bảng kiểm
| # | Kiểm | Đo được | Kết |
|---|---|---|---|
| 1 | Riêng tư repo | `git log -p 9840f27..4407935` 2.971 dòng thêm: nội dung/tên/số TK/email/mã thật **0**; `quet_pii_repo` **0**; `DEM_BE.json` chỉ đếm + vân tay HMAC muối 128 bit ngoài repo | ĐẠT |
| 2 | Phân tầng thẻ `a3-1-ref` | dựng lại từ SA: A **65/65** · B **70/70**, từng tầng = mong, khớp `DEM_BE.json` toàn bộ. Đáp án = cột N `Mapping L1` *(công thức, ⛔ "người chốt")* — diễn giải; kỳ mở `2026-11`; bank từ `ITL RAW` — câu chủ Q1–Q4 giữ; thiếu 2 ca cài sẵn của thẻ | ĐẠT + `-07` |
| 3 | Độc lập | trùng ca WO-329 **0** · trùng prompt **0** *(65 + 70 ca; 12 ca; 20 tệp)*, cả ở cây gộp; cấy trùng ⇒ **1** *(2/2 cắn)*. A∩B **9** ca | ĐẠT + `-08` |
| 4 | Fleet eval GIẢ | tái lập `2/25` (A) · `1/25` (B) ⇒ CHẶN; `chua_chot` 5, mẫu số chính 65, nối 0/5 | ĐẠT; vòng `KHÔNG CHE` bỏ `chay_skill` (`-06`) |
| 5 | Mục ĐỎ có tên | mẫu số 0 ⇒ ĐỎ đúng, nhãn "phép thay thế khác vật đo" có; lát 800 đọc 15/16 ⇒ gỡ được (`-09`). Nhưng `email`/`Số chứng từ` "0 lọt" là tập rỗng (`-04`) | ĐẠT + `-04` |
| 6 | Cây gộp thử | gộp **xung đột** `fleet_eval_voi.py` + sàn; `--duong-nen`: **`KẾT: ĐỎ`** — 33 vs 28 *(thêm 5: 4 do mã `che_do` + 1 sàn)*, chạy 4.990; web 3 = 3. Bể thiếu `tk` ⇒ `KeyError`. `kiem_tai_lieu` ĐẠT · `lint-imports` 11 kept · `quet_pii_repo` 0 | **TRƯỢT** |

AC-4 "0 lọt": ⛔ chặn theo chủ *(bộ che tuỳ chọn)*; đo lại: sau che còn số TK **1/3** · tên ứng viên **5/2** *(A/B)*.

## Việc cho dev
CHẶN: `-01` gộp nền AG vào HELD, chuyển sang `che_do`, đặt sàn = 4.990 + bài ghim; `-02` thêm `tk` vào ca bể. Sau đó R1 vòng 2 + `--duong-nen` ⇒ mong 28 = 28.
⛔ chưa chạy: `kiem_so_song` · `khop_owner --kiem` *(python hệ thống thiếu `psycopg`; nền đã đỏ theo BG-339)*. Cây thử đã gỡ, bể thật dựng lại đã xoá.
