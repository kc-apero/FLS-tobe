# KQ-155 — biên bản kiểm `BG-153` *(R2 CUỐI · ISP 3.1.2 · Step 17 · C6)*

| | |
|---|---|
| **Thuộc** | `BG-153` *(mục vòng sửa)* · `WO-152` · `KQ-154` |
| **Kiểm bởi** | `fls-test` *(phiên cloud con, R2)* · 2026-11-18 · `isp/C6` @ `dcb4f57` |
| **Phán quyết** | **`ĐẠT` — đủ điều kiện GỘP** · `0 CHẶN · 0 NÊN SỬA mới · 1 GHI NHẬN mới` *(`C6-R2-01`, sổ `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C6.md`)* |

## Thay đổi từ R1 *(`git diff b525b9b isp/C6`: 5 tệp — 3 bài/script/ghim + `BG-153`; `fls/` ⛔ đổi)*
| Lỗi R1 | Tái đột biến *(bản sao `git archive`; gói `tests/cau_hinh` + `test_isp_config_per` = **175 bài**, nền xanh 175/175)* | Đóng? |
|---|---|---|
| `C6-R1-01` | **M3** *(`quy` tháng 9 ⇒ 4)* ⇒ ĐỎ `test_ky…[ngay6]` · **M4** *(29/02 lùi năm)* ⇒ ĐỎ `[ngay8]` — trước đó SỐNG | **ĐÓNG** |
| `C6-R1-02` | **M7** *(handler gõ cứng ngày 2024-10-21)* ⇒ **2 đỏ** · **M8** *(gõ cứng `"A"`)* ⇒ **1 đỏ** *(bài handler luật `Z`)* — trước đó SỐNG | **ĐÓNG** |
Trả nguyên sau mỗi đột biến; chạy lại sau trả: 175/175 xanh. `C6-R1-03/04` giữ *ghi nhận* *(backlog · H5)*.

## Cây gộp thử `/tmp/r2_c6/gop` *(`origin/moi/lam_viec` @ `aea5d82` + `merge --no-ff --no-commit isp/C6`; ⛔ commit/push)*
| | |
|---|---|
| Xung đột | **2 tệp, đúng như dự báo**: `tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py` *(script + bài ghim)* ⇒ `checkout --ours`; ⛔ xung đột khác |
| Thu thập | `pytest --collect-only` cây gộp = **3377** *(lam_viec 3343 + 34 bài C6)* ⇒ `MONG_PYTEST_TOAN_BO` = 3377; `tests/web` = **667** |
| `--duong-nen --cong 5446` *(một lần)* | **`KẾT: ĐẠT`** · toàn bộ tập đỏ = đường nền **28 = 28** *(thêm 0 · bớt 0 · XFAIL 2 = 2)* · chạy **3377** ≥ 3377 · web **3 = 3** · 667 |
| `lint-imports` | `11 kept, 0 broken` |
| `soi_bang_tuyen.py` | khớp SQL ở **43** tuyến · `OK /config/per` |
| `kiem_tai_lieu.py` | **ĐẠT** K1–K6 *(286 tệp · 2513 bảng · 817 ô ngày · 104 mã QĐ)* — K3 đỏ `TIEN_DO.md:155` của R1 **đã hết** trên cây gộp |

## Việc cho orchestrator khi gộp thật
- Sàn = thu thập cây gộp **lúc gộp** *(3377 ở thời điểm đo)*, ⛔ `3330` của nhánh; thêm `+ isp/C6` vào changelog bài ghim.
- `07_API_CONTRACT.md` dòng `/config/per` + mã `FLS-CAUHINH-LUAT-CHUA-KY` *(theo WO)*; H5 chốt ngày đầu 20/21.
