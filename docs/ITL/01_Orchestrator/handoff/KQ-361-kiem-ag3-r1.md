# KQ-361 — biên bản kiểm `BG-360` *(R1 · `WO-359` + vòng sửa sau R1 `KQ-357`)*

| | |
|---|---|
| **Thuộc** | `BG-360` · `WO-359` · `BG-356` §vòng sửa · `KQ-357` |
| **Kiểm bởi** | `fls-test` · 2026-11-24 · mã đo `4140a5f` *(`isp/AG3`)* · cụm PG 16 cổng 5447 · SDK `anthropic` 2.13.0 |
| **Phán quyết** | **ĐẠT CÓ ĐIỀU KIỆN** *(R1: 0 CHẶN · 3 NÊN SỬA · 3 GHI NHẬN)* — vòng sửa nên gom 3 NÊN SỬA vào MỘT lượt trước R2; ⛔ ảnh hưởng gọi thật hôm nay *(cả hai đường GCP chưa gọi được)* |

> Vai KIỂM: ⛔ sửa mã · ⛔ gọi API thật · ⛔ GCP · ⛔ ghi kho. **0** lời gọi ra ngoài: SDK giả *(chữ ký `bind` vào SDK 2.13.0 thật)*, `socket.connect` chặn ⇒ **0** kết nối; gcloud + curl GIẢ có trạng thái. Sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_AG2.md` v0.2 *(`AG3-R1-01…06`; trạng thái `AG2-R1-*` đã cập nhật)*.

## Cổng
| Lệnh | `BG` nói | Đo | Khớp |
|---|---|---|:-:|
| `--duong-nen --cong 5447` *(một mình)* | 28 = 28 · web 3 = 3 · sàn 5158 | `KẾT: ĐẠT` · **28 = 28** *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **5158** · `12 failed, 5130 passed, 2 xfailed, 14 errors` · web **3 = 3** · chạy **690** | ✅ |
| `kiem_tai_lieu` · `lint-imports` · `quet_pii_repo` | ĐẠT | 523 file / 3081 bảng · `11 kept, 0 broken` · **0** chỗ · 0 tệp | ✅ |

## AG2-R1 đóng **6/8** *(04 đóng một phần · 05 vẫn mở — của BA)*
`01` ✅ venv MỚI chỉ từ `requirements.txt`: `google.auth` · `google.oauth2` · `requests` import được; python hệ thống *(0 gói)* vẫn `ModuleNotFoundError: google.auth` — đối chứng; bài canh cắn **3/3** *(bỏ `google-auth` · bỏ extra `google_cloud` · thêm `import yaml` nhập muộn)*. `02` ✅ phẳng · `a/b/` ⇒ B · rỗng ⇒ `FileNotFoundError` có tên. `03` ✅ khai ở `--help`. `04` ⚠ **đóng một phần** ⇒ `AG3-R1-01`. `06` ✅ *(kèm `AG3-R1-05`)*. `07` ✅ khai. `08` ✅ 16/17 đột biến. `05` ⏳ zip còn **3** dòng Gemini *(A2 2 · A4 1)*.

## 06 với gcloud giả *(mục `mong` ĐỎ đúng 12/12 kịch bản)*
Dựng từ trống + cả 8 lời gọi thử `403` ⇒ **8** ĐỎ đúng 8 mục *(HTTP ×4 · mô hình trả về ×4)*, mỗi lỗi in tên *“CHƯA Subscribe/Activate … thiếu roles/claude.user”*, ⛔ “chờ”/xanh. Đủ ⇒ **16/16** ĐẠT *(vertex **14/14**)*. Bỏ **một** trong **2** dịch vụ ⇒ **1** ĐỎ đúng mục *(cả hai chiều: thiếu `claude.googleapis.com` · thiếu Marketplace)*. SA thiếu vai · vai CÓ điều kiện · vai sai `aiplatform.user` ⇒ **1** ĐỎ mỗi ca. Biến `FLS_NHA_CUNG_CAP` vắng · `vertex` · `anthropic` ⇒ ĐỎ mục biến. Project lạ ⇒ ĐỎ. Mô hình trả về ≠ ghim ⇒ ĐỎ ×2. `--condition=None`: **2/2** lệnh cấp vai; **0** lệnh gỡ vai; `services enable` mang **cả 2** dịch vụ. Workspace: vắng · `abc` · `wrkspc_a-b` · `wrkspc_é`* · có cách · `WRKSPC_x` ⇒ exit 2; **`wrkspc_` lọt** ⇒ `AG3-R1-04`. *(\* ở 06; ở `mo_hinh` `wrkspc_é` lọt.)*

## Bộ chọn nhà cung cấp *(SDK giả, 0 socket)*
`google-cloud` ⇒ `AnthropicGoogleCloud(project, workspace_id, max_retries)`; `vertex` ⇒ `AnthropicVertex(project_id, region, max_retries)`; `anthropic` *(và biến vắng)* ⇒ `Anthropic(max_retries)` + đòi khoá — chữ ký **bind được** vào SDK thật. Thiếu chốt `FLS_CHO_GOI_API` · xác nhận dữ liệu · project công ty · vùng · khoá ⇒ `CamGoiThat` với **0** SDK dựng *(12/12 ca)*; `ZDR` cũ ⛔ thay được xác nhận GCP; dựng thẳng lớp khoá khi cấu hình nói GCP ⇒ `CamGoiThat`.

## Bí mật · giá
`git grep 'wrkspc_[A-Za-z0-9]'` ngoài `tests/` = **0** *(trong `tests/`: 5, đều bịa)*; báo cáo 06 **0** lần lộ token · workspace · nội dung trả lời; workspace nằm trong argv `curl` ×2 + `ssh --command` ×1 ⇒ `AG3-R1-06`. Giá: `BANG_GIA_GOOGLE_CLOUD` = Claude API, report `vong_that_voi` gắn *“USD là ƯỚC”*; dòng `API THẬT` **không** ⇒ `AG3-R1-03`.

## Đột biến *(bản sao `git archive`, `diff` về cây sạch)*: **16/17** cắn đỏ
M1 bỏ `workspace_id` · M2 bỏ chốt xác nhận · M3 vertex dựng `Anthropic` · M4 mặc định ⇒ google-cloud · M5 bỏ `--condition=None` · M6 bật 1 dịch vụ · M7 thêm lệnh gỡ vai · M8 gọi thử khớp mọi mã · M9 mục biến luôn khớp · M10–M12 requirements/import · M14 bỏ chốt `FLS_CHO_GOI_API` · M15 bỏ chốt project · M16 bỏ kiểm tiền tố · M17 giá = 0. **M13 sống** *(`import anthropic` sớm)* = tương đương: chốt đếm **dựng** SDK.

## Phát hiện
| F | Mức | Nơi | Gửi |
|---|---|---|---|
| `AG3-R1-01` | `NANG` | `vong_that_voi.py:153` — `LoiApi` giữa chừng ⇒ mất nhật ký | `DEV` |
| `AG3-R1-02` | `NANG` | bài gc/vertex ghi nhật ký giả vào repo *(4 tệp đã commit)* | `DEV` |
| `AG3-R1-03` | `NANG` | `chay_agent_voi.py:369` USD ⛔ nhãn ƯỚC | `DEV` |
| `AG3-R1-04` | `NHE` | workspace `wrkspc_` · Unicode lọt | `DEV` |
| `AG3-R1-05` | `NHE` | `chmod 700` thư mục có sẵn | `DEV` |
| `AG3-R1-06` | `NHE` | workspace ID trong argv | orchestrator |

Bài thử mới: ⛔ thêm vào `tests/` *(vai KIỂM chỉ báo; bằng chứng là kịch bản ở scratchpad phiên, ⛔ commit)*.
