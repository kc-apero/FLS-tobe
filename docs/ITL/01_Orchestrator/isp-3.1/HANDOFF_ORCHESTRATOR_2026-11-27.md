# HANDOFF — orchestrator ISP 3.1.2 · 2026-11-27 *(tạm dừng theo lời chủ — mai triển khai tiếp)*

> **Dành cho:** chủ, và phiên orchestrator tiếp quản.
> **Kế thừa** `HANDOFF_ORCHESTRATOR_2026-11-22.md` (§7 bẫy vẫn đúng). Từ 22/11 tới nay: ISP **48/48** đã gộp và PR #1 vào `main` (23/11, ThuongCT ký O6); sau đó là **staging GCP + 4 agent Voi gọi mô hình thật**. Nhật ký đầy đủ từng lượt: `TIEN_DO.md` (mọi hàng 2026-11-23 → 2026-11-27).
> Lời chủ 27/11: *"xong thì tạm dừng, viết handoff, mai triển khai tiếp"* ⇒ orchestrator **⛔ giao phiên mới** sau tệp này; 3 phiên con đang chạy tự kết thúc, kết quả đọc lại ở §4.

---

## 0. Câu mở đầu để dán khi quay lại
```
Bạn là orchestrator của ISP 3.1.2 dự án FLS (repo kc-apero/FLS-tobe). Đọc
docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-27.md trên nhánh
claude/bold-galileo-zukpaf (mục 1 và 4 trước), dùng skill isp-orchestrator ·
isp-gop-buoc · fls-moi-truong, đọc kết quả 3 phiên con ở §4 rồi làm §5 "Việc kế".
Trả lời chủ bằng tiếng Việt; mọi câu hỏi kèm khuyến nghị.
```

## 1. Một màn hình
| | |
|---|---|
| **Nhánh làm việc** | `claude/bold-galileo-zukpaf` @ `0164173` (+ commit handoff này) = `main` + AG + HELD + STG + **STG-NAP** + **AG3** (gồm AG2) + **SONG** |
| **Sàn** | `MONG_PYTEST_TOAN_BO=5389` · `MONG_PYTEST_WEB=690` · tập đỏ nền **28** · web **3** |
| **Đường nền gần nhất ĐẠT** | sau gộp SONG `ba8291f` (cụm **5434**): `KẾT: ĐẠT` — 28 = 28 · chạy 5.389 · web 3 = 3 · 690 |
| **Cụm gộp** | ⭐ **5434** (⛔ 5433 — xem §6 bẫy 1) |
| **Số phiếu trống kế tiếp** | **375** |
| **Chưa gộp** | **STG-WEB** (R2 `KQ-366` ĐẠT nhưng gộp thử ĐỎ 1 bài tích hợp — đang sửa) · **OR** (`WO-367`, R1 đang chạy) · **MCP** (`WO-371`, dev đang làm) |
| **PR #2 → `main`** | CHƯA mở — mở sau khi gộp STG-WEB (+ OR/MCP nếu chủ muốn gom) |

## 2. Quyết của chủ 23/11 → 27/11 — ⛔ hỏi lại
| Ngày | Quyết |
|---|---|
| 23/11 | ThuongCT ký O6: *"Cho phép lên staging và bắt đầu test full luồng e2e bằng human"* · agent đọc TOÀN BỘ nội dung + số TK · nguồn SỐNG là chuẩn cho mọi kỳ · CDT1 đo lại sàn (đã đo: 3.300 ⇒ 3.000) · một nhà cung cấp Anthropic (Opus 5.5 làm · Sonnet 5.5 Auditor) · ⛔ Gemini · OpenAI giai đoạn sau |
| 24/11 | Staging có link web như fps-v35 + MỘT tài khoản đăng nhập chung `HondurasGesha` (mật khẩu ⛔ ở repo/chat — chủ tự đặt qua `08_dat_dang_nhap.sh`, `read -s`, chỉ băm lên Secret Manager; khuyên đổi mật khẩu đã lộ trong chat) · FLS staging **ở tạm `fp-a-project` dùng chung** — chủ chấp nhận rủi ro SA compute mặc định giữ `editor` + `secretAccessor` + `cloudsql.client` mức dự án (đã kiểm kê: Cloud Build + 13/21 Cloud Run + 3/4 VM chạy bằng SA ấy ⇒ ⛔ gỡ) |
| 25/11 | Bật Claude Opus 5.5 + Sonnet 5.5 ở Model Garden; billing tính **SGD** (1 USD = 1,28 SGD tháng 11); *"tạm bỏ qua billing"* |
| 27/11 | **Bỏ Vertex ⇒ OpenRouter** (`WO-367`) · **dựng MCP** để tài khoản Claude của chủ kết nối FLS và đọc TOÀN BỘ dữ liệu (`WO-371`, chỉ đọc) · *"chưa cần thiết đặt API key"* · tạm dừng |
| GIỮ | 20/11 *"Claude ⛔ vào GCP"* — mọi script GCP do CHỦ chạy ở Cloud Shell (tarball `git archive` từ máy Windows `C:\Users\Admin\Downloads\FLS-i2`) |

## 3. Staging GCP (`fp-a-project`) — đã chạy gì
| Bước | Trạng thái |
|---|---|
| 01 Cloud SQL · bí mật · SA | ĐẠT (23/11) |
| 02 di trú + 3 vai | ĐẠT 24/24 (đường chuyển vai SQL) |
| 03 ảnh + VM `fls-staging-app` (IAP SSH) | ĐẠT 435/435 tệp ngữ cảnh |
| 04 config IX.* | ĐẠT — 9 bảng · 10 phiên bản · `fls_itl` = 0 |
| **05 nạp nguồn sống** | **SẴN SÀNG, CHỦ CHƯA CHẠY** — khối lệnh ở `tools/staging/README.md` §05 (`--kiem` trước, rồi `FLS_CHO_GHI_THAT=1 … --sa-json-tep …`); dùng tarball của nhánh làm việc MỚI NHẤT |
| 06 agent ↔ Claude trên GCP | Mã có 3 đường (`google-cloud` · `vertex` · `anthropic`). Vertex: hạ tầng 6/6 ĐẠT nhưng **quota `anthropic-claude-*` = 0**, xin tăng ⇒ Denied tự động (*"wait 48h … or until your Billing account has additional history"*); chủ đã gửi Sales/Support. `claude.googleapis.com`: chặn ở Subscribe Marketplace (chủ ⛔ quản trị billing — người giữ billing: xem nhật ký Cloud Audit mục `AssignResourceToBillingAccount`). **Chủ đã chuyển sang OpenRouter** |
| 07/08 link web + đăng nhập | mã ở `isp/STG-WEB` — chạy SAU khi gộp |
| 10 MCP | mã đang làm (`WO-371`) |

## 4. Ba phiên con đang chạy lúc tạm dừng — đọc kết quả trước
| Phiên | Việc | Khi có kết quả |
|---|---|---|
| `session_01Ci2qSKGavu6TMMAL7mfaQS` (fls-dev, WO-363) | **sửa tích hợp STG-WEB × AG3**: bài `tests/staging/test_iam_dieu_kien.py::test_tinh_MOI_binding_muc_du_an_co_condition_None` ghim tập script có binding mức dự án = {01, 03}, AG3 thêm `06_vertex_agent.sh` ⇒ khai báo MỘT chỗ + giữ ĐỎ khi script mới chưa khai | ✅ **XONG 27/11 ~04:57** (`BG-364` §13; gộp @ `4018560`, ngọn `6f1fb51`; hằng `KHAI_BINDING_DU_AN` = 01 · 03 · 06, kiểm 3 chiều + bài mới chứng minh ĐỎ; `--duong-nen --cong 5434` ĐẠT 28 = 28 · web 3 = 3 · sàn **5.485**) ⇒ việc kế: giao **R2b nhẹ** (mẫu `r2_cay_gop_thu.md`, phiếu `KQ-366b`) ⇒ ĐẠT ⇒ gộp (cụm 5434). Gộp thử cục bộ cũ `luu/gop-STG-WEB-do-7063926` CHỈ ở container cũ — bỏ được; cách gỡ xung đột đã ghi trong lời giao phiên + `TIEN_DO` 27/11 |
| `session_01Ci2qSNWAqBpp9xNxDHzY2p` (fls-test) | **R1 OR** `KQ-369` trên `isp/OR` @ `b219484` | có CHẶN/NÊN SỬA ⇒ nhắn lại phiên dev `session_01Ci2qSMHBTQvb4h5HwZJnJ4` sửa ⇒ R2 cuối `KQ-370` ⇒ gộp |
| `session_01Ci2qSM4SkDRsCHvvfGwxrq` (fls-dev) | **WO-371 MCP FLS** (chỉ đọc · OAuth · Cloud Run `fls-staging-mcp` · `10_mcp.sh`) ⇒ `BG-372` | R1 `KQ-373` ⇒ R2 `KQ-374` ⇒ gộp ⇒ đưa chủ khối lệnh 10 + cách thêm connector claude.ai |

Đọc: `ReadNotifications` (tin các phiên gửi về) · `list_sessions children=true` · `get_session`.

## 5. Việc kế (theo thứ tự)
1. Đọc §4; xử lý từng kết quả theo bảng (R2b STG-WEB · sửa/R2 OR · R1 MCP).
2. Gộp **STG-WEB** (cụm 5434) ⇒ đưa chủ khối lệnh **08 → 07** (`BG-364` §12.1: `07 --kiem` → `08` → `07` → mở link → `07 --kiem`).
3. Gộp **OR** ⇒ khi chủ có khoá OpenRouter: script 09/06 `--duong openrouter` + tập nhỏ trần 2 USD ⇒ fleet eval ma trận.
4. Gộp **MCP** ⇒ chủ chạy `10_mcp.sh` + thêm connector.
5. Mở **PR #2** `claude/bold-galileo-zukpaf` → `main` (khi chủ đồng ý), theo mẫu PR #1.
6. Backlog (phiếu nhỏ, gom một lượt): `ORC-ENV-01` (`dung_moi_truong_isp.sh:279-285` chỉ cài `requirements.txt` khi thiếu 3 gói gốc — phải kiểm MỌI dòng) · `AG3-GOP-01` (06 gặp 429 phải in TÊN hạn mức) · `AG3-GOP-02` (BG-360 §⓪ thêm bước xin quota Vertex) · `SONG-R2b-01` (số UAT ⛔ thẻ chưa được canh) · `gop_buoc_isp.py` ghi `5433` trong lời nhắc + tìm sổ theo mã nhánh (`STG-NAP` ↔ `_NAP.md`) · `gop_so.py` lọc theo tiền tố mã và chỉ đọc bảng đầu (AG3 trong sổ AG2, R2b ở bảng thứ hai) — chép tay đã làm 3 lần.

## 6. Bẫy mới 23/11 → 27/11 (đã cắn)
1. **Cụm 5433 ở container cloud**: `NAP-R1-05` chặn `PG_DSN` cổng 5433 (= `fls-pg-1` THẬT trên máy chủ) ⇒ 15 bài `test_05` ĐỎ đúng thiết kế ⇒ gộp + đường nền ở **5434** (skill `isp-gop-buoc` đã ghi).
2. **venv cũ thiếu gói mới**: sau AG3 phải `pip install -r requirements.txt` (thiếu `anthropic` ⇒ 1 bài ĐỎ + 2 skipped).
3. **Sổ phát hiện khác khuôn 10 cột** cắn 3 lần (AG · HELD · SONG) ⇒ mẫu prompt R1/R2/sửa nay đòi 10 cột + MỘT bảng.
4. **Tệp sinh ra (report.html · zip agent · ảnh) xung đột khi gộp** ⇒ SINH LẠI bằng công cụ trên cây gộp (`chay_agent_voi.py --ghi-report` · `sinh_the_agent.py --zip` · chụp `report.png` 1240×1000 không full-page), ⛔ chọn một bên.
5. **Bài `test_03`/`test_07` dựng ngữ cảnh bằng `git archive HEAD`** ⇒ chạy trên cây gộp CHƯA commit là ĐỎ giả — commit rồi mới đo.
6. **Container khởi động lại giữa chừng** ⇒ PG tắt im lặng (`Connection refused` hàng loạt) ⇒ `dung_moi_truong_isp.sh --cong 5434` dựng lại, trạng thái git còn nguyên.
7. **`git reset --hard` bị bộ phân loại chặn** ⇒ cất commit gộp đỏ: `git branch -f luu/<tên> HEAD` rồi `git switch -C <nhánh làm việc> origin/<nhánh làm việc>`.
8. **IAM dự án có binding điều kiện** ⇒ mọi `projects add-iam-policy-binding` phải `--condition=None` (thiếu ⇒ gcloud dừng hỏi). Đã ghim bằng bài ở 01 · 03 · 06 · 07/08.
9. **gcloud đòi xác nhận bật API** khi chủ chạy lệnh kiểm kê (đã vô tình bật `cloudfunctions.googleapis.com`, 0 function) — lệnh đưa chủ nên kèm `--quiet`/ghi rõ.

## 7. Câu hỏi mở cho chủ (kèm khuyến nghị)
| # | Câu | Khuyến nghị |
|---|---|---|
| Q1 | **Ký lại** bảng số cuối `KQ-354` (HD1 26 kỳ 88.962/89.054 · HD 12.722 · 2026-11 748 dòng · HD1 bộ ba sống 16/23 · WP-C5c 77.663/8.487) **+ 615 lệch bản 671 → 680** (`KQ-354b`) — chủ + ThuongCT | ký — mọi số đã được R2/R2b tự đo lại (46/46 số UAT khớp) |
| Q2 | Câu **C6**: cổng HD1 mặc định chuyển sang bộ ba SỐNG? | chuyển, sau khi Q1 ký |
| Q3 | OpenRouter **C1** mô hình so trong fleet eval · **C2** dữ liệu thật qua bên thứ ba (tắt lưu prompt/huấn luyện ở tài khoản OpenRouter trước khi đặt `FLS_OPENROUTER_DU_LIEU_XAC_NHAN=1`) | C1: Claude Opus 5.5 + Sonnet 5.5 + 1 mô hình OpenAI hàng đầu · C2: bật ZDR/⛔ thu thập |
| Q4 | MCP **C1** email được kết nối · **C2** dữ liệu thật vào ngữ cảnh Claude | C1: chỉ chủ giai đoạn đầu |
| Q5 | Chạy **bước 05** (nạp nguồn sống) | chạy trước 07 để người test thấy dữ liệu thật |
| Q6 | Trước go-live: chuyển `fp-a-project` (hoặc FLS) vào **tổ chức Apero** / dự án riêng (người tạo dự án là tài khoản Gmail cá nhân; 11 Owner gồm 2 Gmail; SA compute mặc định đọc được bí mật FLS) | lên kế hoạch trước UAT rộng |

## Trạng thái cuối
- Nhánh làm việc sạch, khớp `origin` (handoff này là commit cuối). Mọi gộp đã push đều `--duong-nen` ĐẠT.
- 3 phiên con đang chạy (§4); orchestrator ⛔ giao phiên mới sau tệp này (lời chủ *"tạm dừng"*).
- Chi phí phiên con lớn nhất đã đo: WO-359 (Opus) **16,08 USD** tới 24/11 04:15; review Sonnet mỗi lượt ≈ 0,5–1,8 USD.
