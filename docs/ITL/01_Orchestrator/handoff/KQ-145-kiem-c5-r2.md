# KQ-145 — biên bản kiểm `BG-143` *(R2 CUỐI · ISP 3.1.2 · Step 14 · C5)*

| | |
|---|---|
| **Thuộc** | `BG-143` · `WO-142` *(sau vòng sửa `KQ-144`)* |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2 độc lập)* · 2026-11-18 · nhánh `isp/C5` @ `c2725b5` *(nền C4 `31509bd`)* · cây gộp thử trên `origin/moi/lam_viec` @ `1b768f2` |
| **Phán quyết** | **`ĐẠT`** — `0 CHẶN · 0 NÊN SỬA · 2 GHI NHẬN mới` *(sổ: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C5.md` v0.2)*. **ĐỦ điều kiện GỘP** |

## 4 NÊN SỬA R1 — tái đột biến trên bản sao `git archive isp/C5` *(gói 200 bài: `tests/cau_hinh` · `test_isp_config_fx/hd` · `test_cau_hinh_chi_them_pg`; gốc: `200 passed`)*
| F | Đột biến R1 *(nhãn)* | Kết quả | Đóng |
|---|---|---|:-:|
| `C5-R1-01` | `"ten": n.ma` *(M13)* · `"nhom": n.ten` *(M14)* · `"dong_sheet": n.ma` · bỏ `sorted` *(M15)* | cả 4 **ĐỎ** *(`test_C4_R3_01_…` ×3 · `test_C4_R3_02_…`)* | ✅ |
| `C5-R1-02` | ghi `tho` vào `gia_tri` MM *(M8′)* | **ĐỎ** hai lối: `_kiem_mm` + bài AC-6b cũ; gỡ `_kiem_mm` ⇒ vẫn ĐỎ bởi `test_C5R1_02_…` *(tập khoá = `{hd_code, thu_tu}`, 73 hàng)* | ✅ |
| `C5-R1-03` | `with conn.transaction()` → `if True:` *(M7)* | **ĐỎ** `test_C5R1_03_…` *(đếm `(ban, dong)` trước/sau)* | ✅ |
| `C5-R1-04` | bỏ `_kiem_noi_dung` · bỏ `except BanHong` ở `cay_hd` · ở `ty_gia` · `doc_hd` bắt sai lớp | cả 4 **ĐỎ** *(5 bài `C5R1_04`)*; **riêng** `doc_mm` bắt sai lớp ⇒ SỐNG ⇒ `C5-R2-01` | ✅ |

Đột biến thêm: M4 *(`khong_doi` so bản đầu)* **ĐỎ** · `pg_verify` bỏ kiểm trigger tắt **ĐỎ** *(`C5-R1-05/06` đóng phần được hứa)* · M1 *(bỏ khoá advisory)* **SỐNG** ⇒ `C5-R2-02`.

## Lối mới có mở lỗ không
- **Lộ giá trị ô?** Không ở tuyến: `LoiCua` `FLS-CAUHINH-BAN-HONG` mang câu **cố định** *(⛔ `str(e)`)*; `BanHong` chỉ chứa `phien_ban`. Lỗi `nap` *(đường người nạp, ⛔ tuyến)* chỉ nêu tên khoá + kiểu; một chỗ lặp lại `thu_tu` sai của chính tệp người nạp — ⛔ PII *(MM chỉ `{hd_code, thu_tu}`)*.
- **`nap()` từ chối nhầm ảnh THẬT?** Không: `ix_fx.json` *(37 dòng, `lac=[202306]`)* · ATL · MM *(73)* nạp được; 9 mẫu bẩn *(đối tượng/chuỗi/list/`None`/khoá lạ/`cap` chuỗi/`thu_tu` chuỗi)* ⇒ `LoiFX`/`LoiHD`/`LoiCauHinh` CÓ TÊN, 0 `KeyError`.
- Bảng khác *(`IX.DRV`…)* chỉ bị kiểm HÌNH chung *(rỗng · khoá rỗng · khoá trùng)* — đúng thiết kế.

## Cây gộp thử `/tmp/r2_c5/gop` *(`merge --no-ff --no-commit`, ⛔ commit/push)*
| Tệp | Xung đột? | Cách giải |
|---|:-:|---|
| `tools/dung_moi_truong_isp.sh` | ✅ | `--ours` ⇒ `MONG_PYTEST_TOAN_BO=3253` *(= tổng `pytest --collect-only -q`: **3253** bài ở 231 tệp; web **667**)* |
| `tests/test_dung_moi_truong_isp.py` | ✅ | `--ours` ⇒ bài ghim đòi `"3253"`; **chú thích docstring cần thêm đoạn C5** *(orchestrator, ⛔ tôi viết lịch sử)* |
| ERD/golden/`05_DATA_DICTIONARY_ERD.md` · `07_API_CONTRACT.md` · `fls/cau_hinh/*` · di trú | ⛔ *(tự gộp)* | `0027` nối `0026` *(không trùng số)* |

Cổng một lần trên cây gộp: `--duong-nen --cong 5434` **KẾT: ĐẠT** *(đỏ + XFAIL = nền **28 = 28**, thêm 0 · bớt 0; chạy **3253** ≥ 3253; web **3 = 3**, 667)* · `lint-imports` 11 kept, 0 broken · `soi_bang_tuyen` khớp SQL ở **42** tuyến · `kiem_tai_lieu` K1–K6 OK *(270 file · 2.441 bảng)* · `pg_migrate` `fls_test`: "không có gì để áp", `pg_verify: khớp`. *(12 failed + 14 errors = bài `SO_THAT` đòi kho thật; `fls_itl=0` ⇒ môi trường, khớp nền.)*

## Phát hiện mới *(chỉ ghi sổ — vòng CUỐI)*
| F | Mức | Nơi | Gửi |
|---|---|---|---|
| `C5-R2-01` | GHI NHẬN | `doc_mm` nhánh `BanHong` ⛔ bài | `DEV` *(tuỳ)* |
| `C5-R2-02` | GHI NHẬN | `nap` khoá advisory: M1 SỐNG | `DEV` *(tuỳ)* |

## Câu hỏi cho orchestrator
Gộp `isp/C5` vào nhánh làm việc? **Khuyến nghị: GỘP** — giải hai tệp xung đột bằng `--ours` + `3253`, thêm đoạn C5 vào docstring bài ghim; đưa `C5-R1-07`, `C5-R2-01/02` vào backlog.
