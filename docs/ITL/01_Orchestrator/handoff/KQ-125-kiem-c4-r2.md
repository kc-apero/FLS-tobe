# KQ-125 — biên bản kiểm `BG-123` *(ISP 3.1.2 · Step 11 · C4 · R2)*

| | |
|---|---|
| **Thuộc** | `BG-123` *(mục "Vòng sửa sau R1 (KQ-124)")* · `WO-122` *(dải: WO-122 · BG-123 · KQ-124 R1 · KQ-125 R2 · KQ-126 R3)* |
| **Kiểm bởi** | `fls-test` — **R2** *(phiên cloud CON độc lập)* · 2026-11-18 |
| **Đối tượng** | nhánh `isp/C4` @ `31509bd` *(mã `d6dea99` + `BG-123`; R1 là `533504e`)* · phạm vi `git diff 533504e isp/C4` = 5 tệp *(`hd.py` · `test_hd.py` · `test_dung_moi_truong_isp.py` · `dung_moi_truong_isp.sh` · `BG-123`)* · cụm PG riêng **5444** |
| **Phán quyết** | **`ĐẠT`** — **0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** *(chi tiết: `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_C4.md` v0.2)* |

> **Điều kiện PUSH** *(ISP mục 8)*: R1 `ĐẠT` · R2 `ĐẠT` · còn **R3** *(KQ-126)* ⇒ **chưa đủ PUSH**.
> Mọi số R2 tự chạy lại; `PG_DSN=…:5444/fls PG_DSN_TEST=…:5444/fls_test PYTHONUTF8=1`. Đột biến trên **bản sao** `git archive isp/C4` *(⛔ chạm worktree; ⛔ sửa mã hệ thống)*. Container Linux — bỏ qua đường Windows/PowerShell.
> Orchestrator đã chốt trước R2: **Q1 = A** *(giữ `doc_mm_van_ban` public)* · `C4-R1-05(a)` → `C5` *(`WO-142` AC-6b)* · `C4-R1-05(b)` → backlog phiếu riêng, ⛔ chặn C4 — R2 ⛔ đổi.

## Cổng chạy lại
| Lệnh | `BG-123` nói | R2 đo | Khớp |
|---|---|---|:-:|
| Dựng môi trường *(S0, `--cong 5444`)* | `KẾT: ĐẠT` | `KẾT: ĐẠT` · 26/26 di trú · pg_verify 25 bảng 0 lệch · `lint-imports 11 kept` · HD1 `9845/9967` · kho `fls_itl = 0` | ✅ |
| `pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py` | `41 passed` | `41 passed in 0.93s` *(`test_hd.py` riêng: `31 passed`)* | ✅ |
| `pytest tests/cau_hinh tests/api/test_isp_config_hd.py` | *(BG ⛔ ghi)* | `131 passed in 1.20s` *(bằng `.venv/bin/python`; lần đầu chạy nhầm Python hệ thống ⇒ `psycopg` vắng, ⛔ tính)* | ✅ |
| `--duong-nen --cong 5444` *(chạy MỘT MÌNH, sau đột biến)* | `KẾT: ĐẠT` · `28 = 28` · chạy 3108 · web `3 = 3` · 667 | `KẾT: ĐẠT` · `28 = 28 node id (XFAIL 2 = 2 · thêm 0 · bớt 0)` · **chạy 3108** *(mong ≥ 3108)* · skipped 0 · deselected 0; web `3 failed, 664 passed` ⇒ `3 = 3 · chạy 667` | ✅ |
| `.venv/bin/lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `soi_bang_tuyen.py` | ĐẠT · 42 tuyến · vết 13 hàm | `✅ ban khai KHOP SQL that o ca 42 tuyen` · `TINH […ix_hd_cay.json, …ix_mapping_master.json] · vet 13 ham` | ✅ |
| `kiem_tai_lieu.py` | ĐẠT | `✅ cong tai lieu DAT` · 243 file · 2285 bảng · 778 ô ngày · 104 mã QĐ *(trước khi thêm KQ-125)* | ✅ |
| Q8 *(sàn)* | `3093 → 3108` cùng commit | `MONG_PYTEST_TOAN_BO=3108` = chạy 3108 *(S0 `--duong-nen` kiểm `≥`)*; bài ghim `tests/test_dung_moi_truong_isp.py` đổi cùng commit `d6dea99` | ✅ |
| `kiem_so_song.py` | ⛔ CHƯA CHẠY | ⛔ chạy *(đường Windows `:406` — backlog, orchestrator đã chốt)* | — |

## Đóng lỗi R1 *(tự đột biến lại đúng chỗ)*
| Lỗi R1 | Cách R2 thử | Kết |
|---|---|---|
| `C4-R1-01` *(4 lối `ValueError` trơn)* | R2-M1 bỏ `isascii` · R2-M4 `thu_tu` ⛔ kiểm · R2-M5 gỡ `try` JSON ATL · R2-M14 gỡ `raise` JSON MM | cả 4 **giết**. Đo trực tiếp `_so`: `'٣'` `'²'` `'+3'` `'-3'` `'3_0'` `''` `'３'` `3.0` `None` ⇒ lý do; `True` ⇒ chặn; `' 3'` `'03'` `'3\n'` `'\t3'` ⇒ `3`. **Còn lối cực đoan ⇒ `C4-R2-01`** |
| `C4-R1-02` *(3 nhánh `doc_mm`)* | R2-M6 `n>=99` · R2-M7 `if False` 0 mã | **giết**. R2-M13 *(`hd_code` rỗng `continue`→`pass`)* sống nhưng **tương đương** *(`loi.append` đã chạy trước)* |
| `C4-R1-03` | R2-M3 `cap=0` · R2-M2 `bool` · M26 cột lạ | cả 3 **giết** |
| `C4-R1-04` | R2-M8 *(= M1 cũ `if False and cur in tham` **+ lưới**)* · R2-M9/M10 lưới cắt non | M8 ⇒ `1 failed, 6 passed` **đỏ có khẳng định** *(R1: `kill -9` OOM)*; M9/M10 giết. Cây chuỗi 150 nút hợp lệ ⇒ 150 nút ⛔ cắt; vòng đủ 150 nút ⇒ `{HD_CAP_NHAY, HD_CHU_TRINH}` ⇒ ngưỡng `<=` **đúng** |
| `C4-R1-05` | — | orchestrator đã chốt; R2 ⛔ đổi |

## Thử phá — vòng sửa có mở lỗ mới?
| Hỏi *(brief)* | Đo | Kết |
|---|---|---|
| Thông báo `HD_HONG` lộ giá trị ô dài? | ô `'x'*100000` ⇒ câu lỗi **100.121** ký tự *(`cap`)* · **100.120** *(`thu_tu`)* · **100.150** *(`ma`)* — ⛔ cắt | GHI NHẬN `C4-R2-02` *(giá trị là mã/cấp HD, ⛔ PII)* |
| Exception gốc còn `raise … from`? | cả hai lõi `raise LoiHD(…) from None`; câu lỗi giữ `str(JSONDecodeError)` *(vị trí, ⛔ trích văn bản)* | chủ ý *(⛔ lộ `doc`)*; ⛔ lỗi |
| `_so` với `'٣'`, `'²'`, `' 3'`, `'+3'`, `'03'`, `True` | `None` · `None` · `3` · `None` · `3` · chặn | đúng; ghim biên chuỗi thiếu ⇒ `C4-R2-03` |
| `_so('9'*5000)` · số JSON 5000 chữ số · `'['*100000` | **`ValueError`** *(giới hạn 4300 chữ số)* · **`ValueError`** *(⛔ `JSONDecodeError`)* · **`RecursionError`** | **`C4-R2-01`** — lối ⛔ bịt hết |
| `doc_mm_van_ban` cùng chốt kiểm như đường tệp? | `doc_mm(duong)` = `giai` + `read_text` ⇒ **gọi** `doc_mm_van_ban`; ⛔ còn thân kiểm thứ hai ⇒ một đường kiểm duy nhất. Lõi chỉ đọc `hd_code` *(⛔ cột PII)* | ✅ |
| Lưới `while` cắt nhầm cây hợp lệ sâu? | xem hàng `C4-R1-04` | ⛔ cắt |

## Bảng AC *(chỉ phần bị chạm bởi vòng sửa)*
| AC | Mong | R2 đo được | Phán quyết |
|---|---|---|---|
| AC-2 `C4-B2` *(chu trình)* | `HD_CHU_TRINH`, ⛔ treo | vòng 2 nút và vòng 150 nút ⇒ `HD_CHU_TRINH ∈ ten`; M8 ⇒ đỏ sạch | **ĐẠT** |
| AC-3 `C4-B3` *(lỗi có TÊN, ⛔ `ValueError` trơn)* | mọi ô hỏng ⇒ `LoiHD` có tên | 4 lối R1 đóng; lối cực đoan *(≥ 4301 chữ số, lồng sâu)* còn ⇒ `C4-R2-01` GHI NHẬN | **ĐẠT** *(kèm `C4-R2-01`)* |
| AC-4 `C4-B4` | 74 nút · 73 MM · `chenh = {NCF}` | `test_isp_config_hd.py` xanh *(`41 passed` gộp)*; `--duong-nen` xác nhận 74 nút không đổi sau siết `_so` | **ĐẠT** |
| AC-6 *(Q8)* | nâng sàn cùng commit | `3093 → 3108` · chạy 3108 | **ĐẠT** |
| AC-1 · AC-5 | ⛔ đổi kể từ R1 | `git diff 533504e isp/C4 -- fls` chỉ `hd.py` | giữ **ĐẠT** |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** | **ĐẠT** | 12/13 đột biến có nghĩa giết · 1 sống *(R2-M12, nhẹ)* · 2 tương đương *(M11 lưới, M13)*; lưới ngưỡng đúng cả hai phía |
| **Dữ liệu** *(kho thật, chỉ đọc)* | **ĐẠT** | vòng sửa ⛔ chạm ảnh/kho; kho `fls_itl = 0`; SQL tuyến `0` bảng *(`soi` ĐẠT)* |
| **Màn hình** | **N/A** | C4 ⛔ có màn *(như R1)* |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| `C4-R2-01` | GHI NHẬN | `hd.py:173-174` · `:306` · `:347` | `cap='9'*5000` ⇒ `ValueError` · số JSON 5000 chữ số ⇒ `ValueError` *(⛔ `JSONDecodeError`)* · `'['*100000` ⇒ `RecursionError`. Hôm nay ⛔ chạm được *(ảnh đóng băng)*; hết đóng băng ở `C5` | **DEV** *(tuỳ, rẻ)* |
| `C4-R2-02` | GHI NHẬN | `hd.py:139-141` | câu lỗi nhắc giá trị ô nguyên độ dài *(100.121 ký tự cho ô 100.000)* | DEV *(tuỳ)* |
| `C4-R2-03` | GHI NHẬN | `hd.py:173` · `test_hd.py` | R2-M12 *(nhận `+`)* ⇒ `31 passed`; ⛔ bài ghim `'+3'`/`'3_0'`/`''`/`'３'` | DEV *(tuỳ)* |

*Ghi chú ngoài phạm vi vòng sửa *(⛔ phát hiện)*: phép dò chu trình dùng `cur in tham` trên `list` ⇒ tốn ~ `n·độ_sâu²`; chuỗi cha–con 5000 nút ⛔ xong trong 120 giây, 150 nút tức thì. Ảnh thật 74 nút sâu 4 ⇒ vô hại; mã này ⛔ đổi bởi vòng sửa.*

## Câu hỏi *(kèm khuyến nghị)*
- **Q-C4-R2-1** — `C4-R2-01` *(lối `ValueError`/`RecursionError` cực đoan)*: vá ở vòng R2→R3 hay để `C5` *(kho config chỉ-thêm — lúc đó ảnh hết đóng băng)*? **Khuyến nghị B: để `C5`**, đưa thành AC của `WO-142` *("nguồn nạp mới ⇒ ô hỏng, kể cả ≥ 4301 chữ số, ⇒ `LoiHD` có tên")* — ⛔ chặn PUSH C4, hôm nay 0 đường chạm. A *(chấp nhận được)*: Dev vá ngay *(`except ValueError` + giới hạn độ dài, 3 bài nhỏ, nâng sàn Q8 cùng commit)* nếu muốn R3 sạch hoàn toàn.
- **Q-C4-R2-2** — `C4-R2-02/03` *(nhẹ)*: bỏ qua hay gộp cùng `C4-R2-01`? **Khuyến nghị: gộp vào cùng quyết định Q-C4-R2-1**.

## Bài thử mới `tests/nghiem_thu/`
*(không)* — 15 bài của Dev phủ 12/13 đột biến có nghĩa; bản thử R2 ở scratchpad *(⛔ commit)*.

## Môi trường R2
`tools/dung_moi_truong_isp.sh --cong 5444` ⇒ `KẾT: ĐẠT`; worktree `…/.claude/worktrees/isp-c4`; sha `isp/C4` = `31509bd` *(khớp brief)*. Nhánh đẩy: `claude/bold-galileo-zukpaf-isp/C4`. Đột biến chạy **trước** `--duong-nen`, chạy tuần tự *(⛔ chồng `fls_test`)*.
