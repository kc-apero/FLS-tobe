# KQ-362 — biên bản kiểm R2 cuối `BG-360` §I *(`WO-355` + `WO-359` · vòng sửa sau R1 `KQ-361`)*

| | |
|---|---|
| **Thuộc** | `BG-360` §I · `KQ-361` · `WO-355` · `WO-359` |
| **Kiểm bởi** | `fls-test` · 2026-11-24 · `isp/AG3` ngọn `13b0264` *(chứa `dbd4a90`)* gộp thử vào `claude/bold-galileo-zukpaf` · cụm PG 16 cổng 5436 |
| **Phán quyết** | **ĐẠT** — **0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(`AG3-R2-01…03`, vào backlog)* |

> Vai KIỂM: ⛔ sửa mã · ⛔ gọi API thật · ⛔ GCP. Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_AG2.md` v0.3 *(10 cột sổ chung)*.

## Gộp thử *(cây thử `thu/AG3`, ⛔ commit lên nhánh nào)*
`--no-ff` `isp/AG3` vào nhánh làm việc: **2** xung đột — `tools/dung_moi_truong_isp.sh` *(sàn)* · `tests/test_dung_moi_truong_isp.py` *(bài ghim sàn + changelog)*. Giải: nhánh làm việc đã có `isp/STG` ⇒ **5126**; AG3 báo **5178** trên cây KHÔNG có STG ⇒ ⛔ cộng tay, lấy **thu thập thật cây gộp = 5307** `pytest --collect-only`; changelog giữ CẢ HAI chuỗi, thêm đoạn `isp/AG3`.

## Cổng *(trên cây gộp thử)*
| Lệnh | Mong | Đo | |
|---|---|---|:-:|
| `--duong-nen --cong 5436` *(một mình, 1 lần)* | 28 = 28 · web 3 = 3 | **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **5307** *(mong ≥ 5307)* · `12 failed, 5279 passed, 2 xfailed, 14 errors` · web **3 = 3** · chạy **690** · skipped 0 · deselected 0 · `KẾT: ĐẠT` | ✅ |
| `kiem_tai_lieu` | ĐẠT | 532 file · 3121 bảng · 995 ô ngày · 104 mã QĐ | ✅ |
| `lint-imports` | 11 kept | `11 kept, 0 broken` | ✅ |
| `quet_pii_repo` | 0 | `0 chỗ số TK cá nhân · 0 tệp` | ✅ |
| `git status --porcelain` sau đường nền *(`AG3-R1-02`)* | 0 | **0** dòng · thư mục `06_Agent/nhat_ky/` ⛔ tồn tại | ✅ |
| `git grep 'wrkspc_[A-Za-z0-9]'` ngoài `tests/` | 0 | **0** trong `fls/` + `tools/` + `docs/` mã; **2** dòng ở **biên bản** `KQ-361` + sổ *(mẫu bịa `wrkspc_é`, `wrkspc_a-b` — Đ2)*; trong `tests/`: 7, đều bịa | ✅ *(ghi nhãn)* |

## `AG3-R1-01…06` đóng **6/6**
`01` ✅ · `02` ✅ · `03` ✅ có bảo lưu ⇒ `AG3-R2-01` · `04` ✅ · `05` ✅ · `06` ✅ có hàng đi kèm `AG3-R2-02`. Cách đo: bài của vòng sửa *(`test_vong_sua_kq357` · `test_06_vertex_agent` · `test_mo_hinh_google_cloud` · `conftest`)* chạy **xanh trong đường nền** + đọc mã từng lối thoát + đột biến; ⛔ dựng lại kịch bản SDK giả riêng. `02` đo trực tiếp: **0** dòng `git status`, **0** tệp nhật ký trong repo sau 5307 bài.
`01` đọc mã: `LoiApi` thoát `chay` ⇒ ĐỎ có tên + nhật ký; chuỗi tự bắt `dung_o` ⇒ dòng `loi`; `main` bắt `BaseException` ⇒ ghi `loi` = TÊN lỗi rồi `raise`. `06`: `--workspace-id` ⇒ exit 2 *(dòng 61)* · curl `-K` *(170, 190)* · ssh `--command='bash -s'` + stdin *(207)*.

## G11 *(`gcloud compute ssh --command='bash -s'` chuyển stdin)*: **CHƯA KIỂM**
`gcloud compute ssh --help` *(bản cài hiện hành)* chỉ ví dụ `--command="ps -ejH"` · `--command="bash -i -c env" -- -t`; trang tham chiếu cloud.google.com **không** nêu stdin. ⛔ có bằng chứng tài liệu. Việc cần: 1 lượt thật trên VM *(lệnh `echo ok | gcloud compute ssh VM --command='bash -s'` phải in `ok`)*. Nếu sai ⇒ 4 mục TRONG VM ĐỎ *(HTTP `None`)* — ⛔ xanh giả. Ghi nhận làm điều kiện **chạy thật 06**, ⛔ điều kiện gộp.

## Đột biến ngoài vòng sửa *(bản sao `git archive`, chạy tuần tự, trả nguyên)*: **2/8** cắn đỏ
| | Đột biến | |
|---|---|---|
| MA | bỏ `chmod 600` tệp `-K` (Cloud Shell) | **sống** |
| MB | `WS_CHE` in đủ workspace | ĐỎ |
| MC | trần `>=` → `>` | **sống** |
| MD | bỏ `rm -f` token + cfg | **sống** |
| ME | bỏ `chmod 600` tệp `-K` (trong VM) | **sống** |
| MF | mất chữ “CHƯA có bảng giá” ở nguồn giá `google-cloud` | **sống** |
| MG | lính canh nhật ký bỏ `assert` | **sống** *(⛔ bài đòi nó cắn)* |
| MH | bỏ nhãn `ƯỚC` dòng vertex | ĐỎ |

6 sống ⇒ `AG3-R2-03` *(GHI NHẬN: quyền tệp bí mật + dọn tệp + biên trần chưa có bài)*. ⛔ chặn: bài vòng sửa cắn đúng điều đã hứa *(nhãn ƯỚC · workspace che)*.

## Phát hiện mới
| F | Mức | Nơi |
|---|---|---|
| `AG3-R2-01` | GHI NHẬN | `mo_hinh.py:443` — lời `VuotTran` có USD ⛔ nhãn ƯỚC |
| `AG3-R2-02` | GHI NHẬN | `06_vertex_agent.sh:80` — `bash -c … "$WS"` đưa workspace vào argv con |
| `AG3-R2-03` | GHI NHẬN | 6/8 đột biến sống *(bảng trên)* |

⇒ Điều kiện gộp `isp/AG3`: **đạt** *(0 CHẶN · 0 NÊN SỬA)*; đặt sàn **5307 / 690** theo thu thập cây gộp.
