# CHUYỂN GIAO phiên điều phối ISP 3.1.2 — 2026-11-17 tối (tạm dừng theo lệnh người dùng)

> **Dành cho:** phiên orchestrator kế tiếp (cùng account hoặc khác). **Đọc theo thứ tự:** tệp này → `CLAUDE.md` → `isp-3.1/TIEN_DO.md` (nhật ký 17/11, dòng cuối là trạng thái mới nhất) → `CHUYEN_GIAO_ACCOUNT_2026-11-17.md` (quyết định 1–10, môi trường, giao thức gốc) → ISP v3.1.2.
> **Trạng thái lúc dừng (16:50 UTC 17/11):** người dùng: *"tạm dừng các task. lưu phiên tránh mất container"*. **0 phiên cloud đang chạy · 0 lời nhắc hẹn giờ.** Mọi kết quả đã ở GitHub. ⛔ Có bí mật nào trong tệp này.

## 0. Câu mở đầu cho phiên mới
```
Bạn là orchestrator ISP 3.1.2 dự án FLS (repo kc-apero/FLS-tobe). Đọc
docs/ITL/01_Orchestrator/isp-3.1/CHUYEN_GIAO_2026-11-17_TOI.md trên nhánh
claude/bold-galileo-zukpaf và làm theo §6 "Việc kế". Chạy theo wave, chỉ dừng khi
cần quyết định hoặc bị chặn; mọi câu hỏi kèm khuyến nghị.
```

## 1. Quyết định người dùng thêm trong ngày 17/11 (⛔ hỏi lại)
| # | Quyết định |
|---|---|
| 11 | Tối đa **4–5 phiên song song** (máy 4 CPU; hạn mức 5 giờ của account) |
| 12 | **Mọi việc MỚI chạy ở phiên cloud** (`create_session`), ⛔ agent cục bộ; máy orchestrator chỉ điều phối + gộp |
| 13 | Model: **bước làm/sửa = `claude-opus-4-8` effort medium** · **vòng review = `claude-sonnet-5-5` effort medium** (Sonnet ~1–1,7 USD/vòng ⇔ Opus ~7–15 USD) |
| 14 | Phiên cloud push đúng MỘT nhánh `claude/bold-galileo-zukpaf-isp/<BƯỚC>`; orchestrator fetch rồi gộp vào nhánh làm việc `claude/bold-galileo-zukpaf` |
| 15 | **O7 cho phiên cloud:** phiên cloud làn DATA TỰ đọc Sheets bằng khoá SA chỉ-đọc, đúng vùng brief ghi, bản thô chỉ ở `/tmp`, ⛔ commit, ⛔ đọc cột PII (Số CT · Diễn giải) |
| 16 | **DT3 dựng lại** thành lịch sử mới (bản cũ `2a31f76` băm tên người đảo được) + xoá nhánh GitHub cũ chứa nó |

## 2. Nhánh · sha (đo 16:48 UTC 17/11)
| Nhánh | sha | Ghi chú |
|---|---|---|
| `claude/bold-galileo-zukpaf` (nhánh làm việc) | `eca5e5d` | đã gộp **8/48**: S0 · DT1a · H1 · C1 · DT2 · H2 · CG1 · DT1b. Sàn `MONG_PYTEST_TOAN_BO` = **2980** · `MONG_PYTEST_WEB` = **664** (bài ghim `tests/test_dung_moi_truong_isp.py` cùng số) |
| `…-isp/DT3` | `61c0e20` | DT3 dựng lại (nền DT2 `d46e817`) + R1/R2/R3 phiếu; **R3 TRƯỢT** (`KQ-110`) |
| `…-isp/DT4` | `fdbb024` | DT4 (nền DT3 `cf5156e`) + R1 phiếu; **R1 TRƯỢT nhẹ** (`KQ-113`) |
| `…-isp/FG` | `c037297` | FG (nền CG1 `4dfb7bd`) + sửa R1 + R2 phiếu; **R2 ĐẠT** 1 NÊN SỬA (`KQ-119`) |
| `…-isp/CG1` · `DT1B` · `DT2` · `H2` | `df09484` · `bad486c` · `d9606d9` · `6ce257d` | đã gộp — giữ làm lịch sử |
| ⚠ `claude/laughing-bohr-331pt0-isp/DT3` | `5a96cd9` | **CHỨA `2a31f76` (mã băm tên người đảo được)** — phiên này bị proxy chặn xoá (HTTP 403) ⇒ **chờ người dùng xoá tay** ở GitHub › Branches |

Khôi phục nhánh bước ở máy mới (ví dụ): `git fetch origin 'refs/heads/claude/bold-galileo-zukpaf-isp/*:refs/remotes/origin/isp-moi/*'` rồi `git branch -f isp/<BƯỚC> origin/isp-moi/<BƯỚC>` + `git worktree add .claude/worktrees/isp-<bước> isp/<BƯỚC>` (khi cần gộp).

## 3. Trạng thái từng bước còn dở
| Step · ID | Trạng thái | Việc kế (quyết định đã chốt) |
|---|---|---|
| 10 · DT3 | R3 `KQ-110` TRƯỢT 0 CHẶN · 2 NÊN SỬA (lỗ BÀI, mã đúng): `DT3-R3-01` hàng chỉ-`B` của luật ẩn danh ⛔ bài · `-02` danh sách cho phép `D:G` chỉ có bài cột `D`. Đối chiếu nguồn 3 ảnh: byte trùng, 0 ô lệch; PII 0 | **A: vòng sửa nhỏ** (Opus) — phiên `session_01EC3zCW6P5uoyfv4C7yUrDm` hỏng 429 lúc 10:23, ⛔ push gì ⇒ **giao lại phiên mới** (lời giao mẫu §5) ⇒ **R3b** (Sonnet, chạy lại đột biến M2/M3/M4 + cổng; số KQ mới **121**) ⇒ gộp DT3 (giữ bài `danh_sach_khuon` bản DT2) |
| 12 · DT4 | R1 `KQ-113` TRƯỢT nhẹ 0 CHẶN · 1 NÊN SỬA — đối chiếu độc lập 157.648 ô / 0 lệch. `F-1`: 4 hàng (`dong_sheet` 6684 · 6836 · 7500 · 7832) `itl_id = "#N/A ()"` lọt cổng | **A: vòng sửa** (Opus): `itl_id` phải khớp `^ITL#\d+$`, 4 hàng ⇒ lệch CÓ TÊN mong = 4; F-2/F-3/F-4 làm luôn; F-6 sửa số BG (+26) — phiên `session_01EC3zCVhSCfSrYXHfu8XNVw` hỏng 429 ⇒ **giao lại** ⇒ R2 `KQ-114` ⇒ R3 `KQ-115` ⇒ gộp SAU DT3 |
| 9 · FG | R2 `KQ-119` ĐẠT 0 CHẶN · 1 NÊN SỬA `FG-R2-01` (F3 xanh cả khi thẻ HD1 mất `ly_do` — Goal ISP đòi "danh sách kỳ đỏ trong lý do") + `FG-R2-02` GHI NHẬN (số "đạt" dòng tóm ⛔ bài) | Khuyến nghị **A cho cả hai** (chưa chốt — orchestrator chốt): vòng sửa nhỏ (Opus) thêm khẳng định `ly_do` của `GET /gates` nằm trong thẻ HD1 + một dòng F1 ⇒ R3 `KQ-120` ⇒ gộp (xung đột script/bài ghim ⇒ giữ bản nhánh làm việc; sàn = thu thập cây gộp) |
| 5 · DT1b | **đã gộp** với MONG nhãn chưa ghim (mã 4) | **WO mới: lượt nhãn THẬT** (`B-DATA-2` đã gỡ — SA đọc được RAW gốc `1md85t5too5drScNYlqsLALqFkWjwYZm7tE8H1p91_4E`; `Transaction Mapping L1` hết giờ 120 s cả `A1:AZ6` ⇒ thử theo lát / dùng `Transaction Original` (A Ngày · B Số CT · D tiền tệ · E Nợ · F Có · G TK; ⛔ C Diễn giải) và khai lệch so ISP; khoá ra tệp chỉ dạng băm ⛔ đảo được; kèm cổng **K14** (Số CT dạng khoa học)) ⇒ gỡ chặn **H3** |
| 11 · C4 | `planned` | Mở khi DT3 sạch ⇒ soạn WO theo ISP Step 11 |
| 6 · H3 | `blocked` | chờ nhãn THẬT DT1b |
| 13+ · H4 · DT5… | `planned` | H4 chờ DT4 gộp; xem bảng 48 bước ở `TIEN_DO.md` |

**Phiếu:** đã cấp tới `KQ-120` (`WO-111` · `BG-112` · `KQ-113/114/115` cho DT4; `WO-116` · `BG-117` · `KQ-118/119/120` cho FG). **Số trống kế tiếp: 121.**

## 4. Việc chờ NGƯỜI DÙNG
1. **Xoá nhánh GitHub `claude/laughing-bohr-331pt0-isp/DT3`** (mã băm tên người đảo được; phiên này 403).
2. **`docs/ITL/02_BA/Artifacts/Ket-qua-Phan-loai-4-loai-o.md:83/91/92`** chứa 3 số tài khoản cá nhân kèm mã người (có từ trước ISP; `DT3-R3-04`). Khuyến nghị: giao BA che ở nhánh riêng — nhưng cần người dùng xác nhận có thuộc quyết định "Tên tài khoản GIỮ" (11/09) không.
3. **Hạ quyền SA về Người xem** ở RAW gốc (đang "Người chỉnh sửa"; mã luôn dùng scope chỉ-đọc).
4. Câu treo cũ: Q2 (owner) — nếu C8 cần nối Mapping Master theo tài khoản cá nhân thì dùng HMAC với khoá NGOÀI repo.

## 5. Quy trình vận hành đã chuẩn hoá (đọc kỹ — mỗi dòng là một bài học trong ngày)
- **Lời giao phiên cloud:** mẫu đầy đủ ở `chuyen_giao/cong_cu/vi_du_loi_giao_phien_cloud_review.txt`. Khung: (1) vai + đọc ISP/`CLAUDE.md`/tệp vai; (2) Bước 0 dựng: `git fetch` nhánh `claude/laughing-bohr-331pt0-isp/S0` (script dựng môi trường) + nhánh bước `claude/bold-galileo-zukpaf-isp/<BƯỚC>`, `worktree add`, `mkdir /var/run/postgresql`, `env -C …isp-s0 bash …/dung_moi_truong_isp.sh --cong N` đòi `KẾT: ĐẠT`; (3) sha mong; (4) phạm vi diff + phát hiện vòng trước + quyết định đã chốt (⛔ tính là phát hiện); (5) việc + `export PG_DSN/PG_DSN_TEST/PYTHONUTF8` + phiếu `KQ-…` theo `_mau/KQ.md`; (6) push đúng một nhánh, ⛔ force/PR/comment; (7) báo cáo cuối = TIN NHẮN CUỐI. `create_session(source_revision='claude/bold-galileo-zukpaf', model=…, effort='medium')`.
- ⚠ **`tools/dung_moi_truong_isp.sh` lấy GOC theo thư mục CHỨA script** ⇒ cổng hồi quy của một nhánh phải chạy bằng script CỦA nhánh đó (log in `GOC = …`).
- ⚠ **⛔ chạy đột biến chồng lên `--duong-nen` trên cùng cụm** (dùng chung `fls_test` ⇒ ĐỎ giả) — chạy cổng MỘT MÌNH.
- **Phiên cloud xong sạch ⛔ tự báo** ⇒ sau khi giao luôn `send_later` 35–40 phút để tự kiểm (`list_events kinds [result]` + `git ls-remote`).
- **Hạn mức 5 giờ:** ~5 phiên Opus song song tiêu hết trong ~70–90 phút (chạm 3 lần ngày 17/11: 04:45 · ~10:20). Phiên hỏng 429 ⇒ đọc `rate_limit_event` để biết giờ đặt lại; review chưa push thì tạo phiên MỚI (rẻ hơn nối lại), dev thì gửi "tiếp tục".
- **Container orchestrator khởi động lại nhiều lần** ⇒ 9 cụm PG tắt: `mkdir -p /var/run/postgresql && chown postgres:postgres /var/run/postgresql` rồi vòng `runuser -u postgres -- /usr/lib/postgresql/16/bin/pg_ctl -D <dir> -l <dir>/pg_ctl.log -w -t 60 start` cho `/home/user/fls-pg16` + `/home/user/fls-pg16-54{34,35,36,37,44,45,46,47}`. venv `/home/user/FLS-tobe/.venv` (cần `pip install google-auth requests` nếu mất).
- **Danh sách kiểm MỖI lần gộp** (orchestrator): `git fetch` + `merge --ff-only` nhánh bước cục bộ (⛔ `FETCH_HEAD` trong worktree — dùng `origin/…`) → `git merge --no-ff --no-commit isp/<BƯỚC>` → xung đột `tools/dung_moi_truong_isp.sh` / `tests/test_dung_moi_truong_isp.py` ⇒ `checkout --ours` (bản S0 mới) → `python3 -I chuyen_giao/cong_cu/gop_so.py <gốc> <ID> v0.N <ngày> <sha>` (gộp sổ phát hiện riêng vào sổ chung, lọc theo mã + số cột) → sàn = tổng `pytest --collect-only -q` (cộng các dòng `tests/…: N`) + sửa bài ghim cùng số → `pytest tests/test_dung_moi_truong_isp.py` + bài của bước → `python docs/ITL/_tools/kiem_tai_lieu.py` (⛔ nằm trong `--duong-nen`!) → `lint-imports` → commit → `--duong-nen --cong 5433` đòi `KẾT: ĐẠT` → push → dòng `TIEN_DO.md`. Việc kèm theo riêng từng bước: xem `CHUYEN_GIAO_ACCOUNT_2026-11-17.md` §6.2.
- **Đọc Sheets bằng SA:** `chuyen_giao/cong_cu/sa_lay.py <id> "<vùng>" <ra.json>` (khoá ở biến `FLS_GSHEETS_SA_JSON_B64`; `REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt`; chạy `python -I`). `sa_ds.py` liệt kê bảng tính SA thấy; `sa_meta.py <id>` liệt kê sheet + kích thước. ⛔ in giá trị; bản thô ⛔ commit.

## 6. Việc kế (theo thứ tự, ≤ 5 phiên)
1. Kiểm/bật 9 cụm PG; `git -C /home/user/FLS-tobe status` sạch; đọc dòng cuối `TIEN_DO.md`.
2. Giao lại **sửa DT3 sau R3** (Opus) và **sửa DT4 sau R1** (Opus) — brief như mô tả §3; nhánh nền `61c0e20` / `fdbb024`.
3. Chốt FG-R2-01/02 (khuyến nghị A) ⇒ giao **sửa FG sau R2** (Opus) ⇒ R3 FG.
4. Soạn **WO-121 nhãn THẬT DT1b** (+ K14) ⇒ giao (Opus, làn DATA) ⇒ R1–R3 ⇒ gỡ H3.
5. DT3 sạch ⇒ R3b ⇒ gộp DT3 ⇒ soạn WO C4. DT4 sạch ⇒ gộp DT4 ⇒ H4.
6. Errata gom thêm cho bản vá ISP/AP v3.1.3 (ngoài ①–⑬): ⑭ DT2 Q5 (cổng DT2 ĐỎ khi C1 từ chối bảng) · ⑮ hợp đồng bản thô = lưới SA `{spreadsheet_id, nguon, doc_luc, cach_doc, values}` · ⑯ DT4 khoá `dong_sheet` + `ky` + `itl_id` (cột R) · ⑰ ISP `:1355` DT4 còn ghi "5 tiền tệ" (F-5) · ⑱ `CALC_ZONE`/WO-111 đếm: 19 kỳ khớp (⛔ 21), 6 hàng = 12 ô rỗng BO/BP.
