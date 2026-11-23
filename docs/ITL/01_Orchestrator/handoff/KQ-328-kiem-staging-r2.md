# KQ-328 — biên bản kiểm `BG-326` *(R2 cuối · `WO-325` — staging bước 02 · 03 · 04 + `Dockerfile` + UAT + README)*

| | |
|---|---|
| **Thuộc** | `BG-326` §9 · `WO-325` · `KQ-327` |
| **Kiểm bởi** | `fls-test` *(phiên cloud · cụm PG **5446**)* · 2026-11-23 |
| **Phán quyết** | **`TRƯỢT`** — **1 CHẶN · 1 NÊN SỬA · 2 GHI NHẬN** *(`STG-R2-01…04`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_STG.md` v0.2)*. Mọi CHẶN/NÊN SỬA của R1 đã sửa **đúng** *(đo lại độc lập)*; cái chặn là **mới**, lộ ra chỉ ở cây gộp I2 |
| **Kiểm ở** | `isp/STG` @ `7fbb987` · cây gộp thử = `origin/claude/bold-galileo-zukpaf` @ `8f727ac` ⊕ `7fbb987` *(⛔ commit cây thử)* |
| **Kho thật** | `KHONG_CHAM` — ⛔ GCP · ⛔ `gcloud` thật · ⛔ ghi kho thật *(chỉ kho scratch của cụm phiên)* |

## Kết luận một dòng
Vòng sửa R1 **đúng**: SA chỉ đọc 3 bí mật app · gỡ thừa idempotent · số gói từ `GOI_BIET` · UAT 42/42 thẻ số khớp. Nhưng **cây gộp thử ĐỎ**: sau khi gộp I2, **2 bài `tests/staging` đỏ** *(chuỗi: kho trắng `WP-C2` không còn ĐẠT; sau nạp 04 ra ĐỎ 6/11 gói)* ⇒ `--duong-nen` tập đỏ **30 ≠ 28** *(`STG-R2-01`)*.

## Cổng chạy lại
| Lệnh | Mong | Test đo | Khớp |
|---|---|---|:-:|
| `pytest tests/staging` *(cây STG riêng)* | 104 | **104 passed** · 168 s | ✅ |
| `pytest --collect-only` *(cây gộp)* | sàn | **4991** *(= 4887 + 104)* · web **690** | ✅ *(xung đột sàn, đặt ở cây thử — `-R2-03`)* |
| `dung_moi_truong_isp.sh --duong-nen --cong 5446` *(cây gộp, MỘT lần, một mình)* | `KẾT: ĐẠT` 28 = 28 · web 3 = 3 | **`KẾT: ĐỎ`** — `14 failed · 4961 passed · 2 xfailed · 14 errors` = 4991 chạy · tập đỏ+XFAIL **30** *(thêm 2, bớt 0)* · web **3 = 3** ✔ | ⛔ `STG-R2-01` |
| `kiem_tai_lieu.py` *(cây gộp)* | 0 | **K1–K6 OK** *(501 tệp · 3.012 bảng · 984 ô ngày)* | ✅ |
| `lint-imports` | 11 kept | **11 kept · 0 broken** | ✅ |
| `quet_pii_repo.py` | 0 | **0 chỗ · 0 tệp** | ✅ |

## Đo lại từng phát hiện R1 *(độc lập, ⛔ tin BG)*
| R1 | Kết quả đo | Phán quyết |
|---|---|---|
| `-01` CHẶN | gcloud giả riêng của Test; trạng thái thật 23/11 *(`postgres 0 · fls_admin 0 · fls_ghi 1 · fls_doc 1 · jwt 1`)* ⇒ `add` 3 · `remove` 0 · add quản trị 0 · BÁO CÁO `'3/3'` `'0/2'` `True`. Còn thừa cả 5 ⇒ gỡ **2**, lần 2 gỡ **0**. **3 đột biến cắn** *(add 5 + bỏ gỡ ⇒ `'2/2'` ĐỎ · gỡ hỏng ⇒ `GO_QUYEN_THUA_LOI` · `get-iam-policy` hỏng ⇒ `'0/3'`/`'2/2'`/`False` ĐỎ)* | **ĐÓNG** |
| `-02` CHẶN | số gói từ `GOI_BIET` *(= 11)*; đột biến bớt 1 gói ⇒ **3 bài đỏ**; còn `10` trong bài = 10 bản config *(không phải số gói)*. ⚠ Nhưng gộp I2 lộ lỗi khác `-R2-01` | **ĐÓNG** *(riêng `-02`)* |
| `-04` | `PERMISSION_DENIED` ⇒ 3 dòng `IAM_KHONG_LAN_TRUYEN` + chữ gcloud + `KẾT: ĐỎ` | **ĐÓNG** |
| `-05` | **39/39** thẻ `hd2` + **3/3** `hd2x` khớp `hd2_cong.json` @ `8f727ac` *(bộ so riêng; tệp ⛔ đổi từ `6e68811`)*. Nhưng nhãn `[CHỜ I2]` lỗi thời ở cây gộp ⇒ `-R2-02` | **ĐÓNG** *(số)* · mở `-R2-02` |
| `-06` | U7/U8 `[chỉ CHỦ chạy — cần sudo]`; `osAdminLogin` = 0 | **ĐÓNG** *(phương án A)* |
| `-07` · `-08` | bài của Dev xanh trên PG thật; chết giữa `IX.ALR` tự lành, probe `--kiem` ⛔ để lại bảng | **ĐÓNG** |
| `-03` · `-13` | đóng ở `d04557a` | đóng |
| `-10` · `-11` · `-12` | backlog Dev khai | còn mở *(GHI NHẬN)* |

**Vòng sửa ⛔ đẻ lỗi mới** ở an toàn bí mật · loopback · `INV-I08` · `fls_doc` chỉ-đọc *(ĐO trên quyền PG THẬT — `test_02` 29 bài xanh trong 104)*.

## Phát hiện mới
| F | Mức | Nơi | Gửi |
|---|---|---|---|
| `STG-R2-01` | `CHAN` | `test_04_nap_du_lieu.py` *(2 bài chuỗi)* · `nap_cau_hinh_ix.py` · `chay_chuoi.sh` | `DEV` *(+ `HOI` BA: 04 có cần nạp/ký `IX.FX`)* |
| `STG-R2-02` | `NANG` | `UAT_STAGING_E2E.md:7,44,46,47` | `BA`/`DEV` |
| `STG-R2-03` | `NHE` | `dung_moi_truong_isp.sh:420-428` · bài ghim | orchestrator |
| `STG-R2-04` | `NHE` | `01_dung_staging_gcp.sh` `sa_doc_duoc` *(căn cứ mã, ⛔ đo GCP)* | `DEV` backlog |

## Bài thử mới
⛔ Không thêm bài vào `tests/nghiem_thu/` — các phát hiện là bài thiếu/lệch ở phía Dev. Chứng ĐỎ bằng đột biến trên bản sao ở scratchpad *(3 đột biến `-01` + 1 đột biến `GOI_BIET`, trả nguyên: `git status` sạch)*.

## Truy vết
`03_TRACEABILITY_GAP_REPORT.md`: ⛔ cập nhật.
