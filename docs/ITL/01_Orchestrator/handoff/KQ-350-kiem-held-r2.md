# KQ-350 — R2 CUỐI `WO-338` / `BG-339` *(ISP 3.1.2 · HELD — bể giữ riêng, trên cây gộp thử)*

| | |
|---|---|
| **Kết quả** | **ĐẠT — 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** ⇒ **orchestrator được gộp** *(đặt sàn 4.997 lúc gộp)* |
| **Phát phiếu** | `fls-test` · 2026-11-23 · `isp/HELD` ngọn `7535479` *(= `f015cbf` + `KQ-349`)* · cây gộp thử = `origin/claude/bold-galileo-zukpaf` `06db986` + `7535479` *(⛔ commit)* · cụm PG 16 cổng 5446 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_HELD.md` §R2 *(`HELD-R2-01…03`)* |
| **Gửi** | `ORCHESTRATOR` ⇒ gộp |

⚠ Bể A/B dựng lại từ SA chỉ-đọc ở thư mục **NGOÀI repo**, **đã xoá** sau đo; ở đây chỉ số đếm, ⛔ nội dung. ⚠ Báo cáo `BE_GIU_RIENG` **đo ĐƯỜNG ỐNG + CỔNG, ⛔ chất lượng mô hình** *(agent = luật GIẢ `luat_v0`/`luat_gia_v1`; ⛔ gọi API thật)*.

## Bảng kiểm
| Mã | Kiểm | Đo được *(nhãn · mẫu số)* | Kết |
|---|---|---|---|
| `HELD-R2-01` | Cây gộp thử + sàn | gộp ngọn nhánh làm việc `06db986` ⇒ **2 xung đột, chỉ hai dòng sàn** *(`dung_moi_truong_isp.sh:420` · `test_dung_moi_truong_isp.py:423`)*; giải = thu thập thật `pytest --collect-only` **4.997** *(0 lỗi thu thập)* · `tests/web` **690**. `tests/agent` + `test_dung_moi_truong_isp` + `test_be_giu_rieng` **170 passed** | ĐẠT |
| `HELD-R2-02` | `--duong-nen --cong 5446` MỘT lần, một mình | **`KẾT: ĐẠT`** — toàn bộ **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4.997 ≥ 4.997** · skipped 0 · deselected 0 · `12 failed, 4969 passed, 2 xfailed, 14 errors` *(23′58″)* · web **3 = 3** · chạy **690 ≥ 690** · `3 failed, 687 passed` | ĐẠT |
| `HELD-R2-03` | Cổng giấy/tầng/PII | `kiem_tai_lieu` **ĐẠT** *(513 tệp · 3.046 bảng · 104 mã QĐ)* · `lint-imports` **11 kept, 0 broken** · `soi_bang_tuyen` **KHỚP 49/49** tuyến · `quet_pii_repo` **0 chỗ · 0 tệp** | ĐẠT |
| `HELD-R2-04` | Bể A/B: đếm ca/tầng = `DEM_BE.json` | dựng lại từ SA: **A 65/65 · B 70/70** · `--kiem` **exit 0** · `thuc_theo_tang == mong_theo_tang` cả hai bể *(A: A10 B5 C10 D5 E10 F10 L3_khong_ref5 L3_ma_khac5 chuyen5 · B thêm `chua_chot` 5)* · nhóm A `29·25·11` · B `30·25·10·5` · đối chiếu kỳ A↔B **KHỚP** · trùng ca WO-329 **0** · trùng prompt/ví dụ agent **0** *(20 tệp prompt quét)* · vân tay: `test_BE_van_tay_khop_tep_dem_repo` xanh *(39 passed)* | ĐẠT |
| `HELD-R2-05` | Ca mang `tk` | ca có `tk` khác rỗng **A 65/65 · B 70/70** *(mẫu số 65 · 70 ≠ 0)* | ĐẠT |
| `HELD-R2-06` | Repo ⛔ nội dung thật | `git log -p origin/claude/bold-galileo-zukpaf..HEAD` *(12 commit · 3.138 dòng thêm)*: dãy ≥ 8 số trần = **0** *(chỉ hiện chuỗi vân tay hex 12 ký tự trùng toàn chữ số + số bịa `1903000000001`…/số tiền)*; email **0**; mã `FT`/`IBDN` + ≥ 6 số **0**; `git ls-files` khớp `muoi`/`.key` **0**; bể dựng trong thư mục ngoài repo, `git status` sạch phần chưa-staged | ĐẠT |
| `HELD-R2-07` | Số A ↔ B tái lập | `fleet_eval_voi --be-giu-rieng` *(không `--ghi`)* trên bể dựng lại: `mo` A nối 2/sai 2/recall 0,0/người-bị-nối 2 · B nối 2/sai 1/recall 0,0333/người-bị-nối 1 · `che_het` cùng số · `v0` nối 0 · `che_noi_dung` bị `CamGui` *(A 10 · B 14 chỗ)* ⇒ **khớp từng số** với `BE_GIU_RIENG.md` trong repo *(exit 1 vì CHẶN — đúng mong)*; chuỗi 4 agent ô khớp **631/631** cả hai bể | ĐẠT |
| `HELD-R2-08` | Quyết chủ khớp | `CHE_DO_MAC_DINH = "mo"` *(`fls/agent/che.py:85`)* ⇒ agent đọc toàn bộ; `che_noi_dung` còn bị chặn tới khi chủ quyết *(C4)*; gọi API thật: `co_that=False` mặc định, `kiem_chot_that` đòi `--that` + `FLS_CHO_GOI_API=1`; `ANTHROPIC_API_KEY` trong phiên **0**; ⛔ gọi API | ĐẠT |

## Phát hiện *(chỉ GHI NHẬN — chi tiết ở sổ §R2)*
| Mã | Mức | Nội dung |
|---|---|---|
| `HELD-R2-G1` | GHI NHẬN | **AC-4 chưa chứng minh được "0 lọt sau che"**: bộ che còn lọt số TK **17/65 · 24/70** *(A/B)*, tên ứng viên **5 · 2**; `email` và `so_chung_tu` có `do_duoc_theo_loai = False` ⇒ mẫu số **0** ⇒ "0 lọt" là **KHÔNG ĐO ĐƯỢC** *(Đ3)*, ⛔ coi là sạch. Hậu quả đã khoá: `che_noi_dung` bị `CamGui`, mặc định `mo`. Việc của chủ/BA, ⛔ lỗi mã *(= `HELD-R1v2-03`)* |
| `HELD-R2-G2` | GHI NHẬN | Ngọn nhánh làm việc đã nhích `577044e → 06db986` kể từ `KQ-349`; kết quả gộp **không đổi** *(2 xung đột sàn, 4.997)*. Sàn đặt = thu thập thật **lúc gộp** + bài ghim cùng commit *(Q8)* |
| `HELD-R2-G3` | GHI NHẬN | Giữ mở từ R1: A↔B có **9** ca trùng *(`HELD-R1-08`)* — vòng này **không đo lại** *(ngoài phạm vi R2)*; email thật ở nền `HELD-R1v2-01` — HELD thêm **0** |

## Chưa chạy *(nói thẳng)*
`tools/kiem_so_song.py` · `dong_bo_so_song.py --ghi` *(đường `.venv/Scripts/` Windows)* · `khop_owner.py --kiem` *(nền đỏ từ R0)* · `kiem_thuyet_minh` ⇒ ngoài phạm vi prompt R2. `pip install google-auth requests` vào `.venv` của phiên để đọc SA *(không đổi repo)*.

## Kết luận
**ĐẠT · 0 CHẶN · 0 NÊN SỬA** ⇒ orchestrator **được gộp** `claude/bold-galileo-zukpaf-isp/HELD` vào nhánh làm việc; giải 2 dòng sàn = thu thập thật lúc gộp. SHA kiểm: `isp/HELD` `7535479`; cây gộp thử `06db986` + `7535479` *(không commit)*.
