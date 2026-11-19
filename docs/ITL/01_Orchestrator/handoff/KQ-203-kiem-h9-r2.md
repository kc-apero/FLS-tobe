# KQ-203 — R2 CUỐI · `H9` + `DT8b` (Step 24 · soát vòng sửa sau R1 `KQ-202` + cây gộp thử)

| | |
|---|---|
| **Thuộc** | `WO-200` · `BG-201` *(mục «Vòng sửa sau R1»)* · `isp/H9` @ `c536809` · cụm `5444` |
| **Phát bởi** | `fls-test` R2 · 2026-11-19 |
| **Kết luận** | **ĐẠT** — 0 CHẶN · **0 NÊN SỬA** · 2 GHI NHẬN mới *(`H9-R2-01..02`)* |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_H9.md` v0.2 |

## Số đo *(Đ4 — mỗi số một nhãn)*
| Nhãn | R2 đo |
|---|---|
| `H9-R1-01` đóng | đổi `gi_mid3` `cvl_pm` VD336·202506 *(Vendor-tháng P-chữ)* ⇒ `KHONG DAT: o_khong_so_khac_0: đo 1 ≠ mong 0` *(R1: XANH ở `5762d39`)*; baseline `0/196`; `mong` ô ⛔ so được **196** khai trước *(`MongC4a.o_khong_so`)*; `mong 0→1` ⇒ ĐỎ chiều ngược |
| `-02` · `DT8B-R1-01` đóng | `ks = 44` hằng ⇒ 1 bài ĐỎ; `pe` chữ ⇒ exit 1, nhãn `pe_la@`, ⛔ `TypeError`, ⛔ lộ giá trị |
| đột biến mã sửa *(5)* | cắn **4**: ks hằng · bỏ nhánh `except` ⇒ coi 0 · `mong` 0→1 · bỏ phép đo đáp án; sống **1**: bỏ `isinstance(dict,bool)` ⇒ 33/33 xanh *(`H9-R2-01`: ⛔ ca `pe=True`)* |
| cây gộp thử *(`thu/H9` = nhánh làm việc `c5d7c66` + `isp/H9`)* | WP-C4a `DAT` *(420 ô so · 196 ⛔ so được · lệch 0 · KS.AL 44)* · WP-C3a `DAT` *(205.175/205.175 ô)* · WP-C3b `DAT` *(11.585/11.585 ô, ≠ 0 2.636 = mong)* — IX.PER = 21/10, IX.VEN nạp vào kho **test** |
| đường nền `--duong-nen --cong 5444` *(chạy một mình)* | **28 = 28** *(thêm 0 · bớt 0)* · chạy **3.665** · web **3 = 3** *(675)* · `KẾT: ĐẠT` |
| `lint-imports` · `kiem_tai_lieu` · `soi_bang_tuyen` | 11 kept 0 broken · ĐẠT *(335 tệp)* · 45/45 tuyến |

## Gộp thử
- **Xung đột 2 tệp**: `tools/dung_moi_truong_isp.sh` + `tests/test_dung_moi_truong_isp.py` *(chỉ hằng sàn)* ⇒ lấy bản nhánh làm việc *(3616)*, rồi đặt sàn = **thu thập cây gộp = 3.665** *(`pytest --collect-only`; = 3616 + 49 bài H9)*; `tests/web` giữ 675. `tools/do_hd2.py` ⛔ xung đột *(tự gộp giữ cả C3 lẫn C4a)*.
- Sàn **3.665** là con số cho orchestrator khi gộp thật *(⛔ commit cây gộp thử)*.

## Phát hiện mới *(GHI NHẬN)*
- `H9-R2-01` — nhánh `bool` của `pe_la@` ⛔ bài.
- `H9-R2-02` — `do_hd2 --dsn` chỉ chảy vào C4a; C3a/C3b đọc IX.PER từ `PG_DSN`, và đường ĐỎ C3a nổ `KeyError: 'dong_so'` *(có từ H5/H6)*. Nạp IX.PER cho cổng C3: `PG_DSN=$PG_DSN_TEST`.

⛔ Kiểm không sửa mã. Kho thật `KHONG_CHAM`.
