# SỔ PHÁT HIỆN REVIEW — ISP 3.1 · phần `C4` *(tệp riêng, chờ gộp vào `SO_PHAT_HIEN_ISP-3.1.md`)*

**Version:** v0.3 · **Ngày:** 2026-11-18 · **Chủ sở hữu:** `fls-test` *(R1 `KQ-124` · R2 `KQ-125` · R3 `KQ-126`)* · **Nguồn:** `IncrementalStepPlan-FLS-Voi_v3.1.2.md` **Step 11 · C4** · `WO-122` · `BG-123`

> **Sổ CHỈ THÊM** *(`10` §4 ③)*: vòng sau *(R2/R3)* chỉ đổi ô **Trạng thái** + thêm hàng, ⛔ viết lại hàng cũ. Vì sao là tệp riêng: cùng lý do `SO_PHAT_HIEN_ISP-3.1_FG.md` — sổ chung sống ở nhánh khác; orchestrator chép nguyên hàng, giữ mã.
>
> **Thang lớp:** **A1** lỗi mã sửa trong bước · **A2** lỗi mã lớp lặp *(kèm luật phòng)* · **B1** lệch spec / thiếu bài · **B2** spec·ISP·đường ống sai → orchestrator. **Mức:** CHẶN · NÊN SỬA · GHI NHẬN *(↔ `CHAN` · `NANG` · `NHE`)*.
>
> ⛔ **Không tính là phát hiện** *(orchestrator đã quyết trước R1)*: câu hỏi của tác giả về *"gốc sai cấp"* ⇒ **A** — gộp vào lỗi `HD_CAP_NHAY` *(một bất biến "cấp = độ sâu")*. R1 chỉ xác nhận gộp **chạy đúng**: gốc ở cấp 2 ⇒ `{HD_CAP_NHAY}`, 1 lỗi.
>
> Mọi số R1 **tự đo** trên `isp/C4` @ `5212f25` *(mã `7478e64`, nền `f1dbd00`)*, cụm PG riêng **5444**; đột biến trên **bản sao** `git archive` ở `/tmp/r1_c4/mut/` *(⛔ chạm worktree: `git status` sạch)*.
>
> **Kết R1: `ĐẠT` — 0 CHẶN.** 5 phát hiện: **2** NÊN SỬA *(`C4-R1-01` lỗi cây còn `ValueError` trơn ở 3 chỗ · `C4-R1-02` ba nhánh lỗi của `doc_mm` ⛔ có bài)* · 3 GHI NHẬN *(`C4-R1-03…05`)*.

## Phát hiện

| Mã | Bước | Vòng | Lớp | Mức | Tệp:dòng | Mô tả | Khuyến nghị | Luật phòng tái phạm | Trạng thái |
|---|---|---|---|---|---|---|---|---|---|
| `C4-R1-01` | C4 | R1 | B1 | **NÊN SỬA** | `fls/cau_hinh/hd.py:168-170` *(`_cap`: `v.strip().isdigit()` ⇒ `int(...)`)* · `:220` *(`int(r.get("thu_tu", i))`)* · `:281` và `:321` *(`json.loads` ở `doc_van_ban` · `doc_mm`)* | **WO-122 §Ràng buộc: *"Lỗi cây có TÊN, ⛔ `ValueError` trơn"* — ba đường vẫn nổ trơn.** Đo bằng `LoiHD` đối chiếu *(`/tmp/r1_c4/probe.py`, 1 dòng hợp lệ + 1 ô hỏng)*: `cap='²'` *(`'²'.isdigit()` = True nhưng `int('²')` ném)* ⇒ **`ValueError: invalid literal for int()`**; `thu_tu='abc'` ⇒ `ValueError`; `thu_tu=None` ⇒ **`TypeError`**; `doc_van_ban('{')` ⇒ **`JSONDecodeError`**. Cả 4 ⛔ phải `LoiHD`, ⛔ mang tên. Chiều ngược: `cap='١'` *(chữ số Ả Rập)* **được nhận** là cấp 1 ⇒ `isdigit` rộng hơn `0-9`. Ảnh gói đóng băng nên **⛔ chạm được ở runtime hôm nay** ⇒ NÊN SỬA, ⛔ CHẶN *(`C5` đổi nguồn sang kho thì ảnh hết đóng băng)* | **Dev**: `_cap` dùng `v.isascii() and v.isdigit()`; `thu_tu` đi qua `_cap`-kiểu *(hỏng ⇒ `HD_HONG`)*; bọc `json.loads` ⇒ `LoiHD([(HD_HONG, …)])`. Mỗi đường một bài | **Mọi chỗ đổi chuỗi → số trong tầng `cau_hinh` phải có bài "ô hỏng ⇒ LoiXX có tên"** ; `isdigit()` ⛔ đủ cho `int()` — dùng `isascii()` kèm | **đóng** *(R2 `KQ-125`: 4 lối bản R1 đóng, đột biến R2-M1/M4/M5/M14 giết; còn lối cực đoan → `C4-R2-01`)* |
| `C4-R1-02` | C4 | R1 | B1 | **NÊN SỬA** | `fls/cau_hinh/hd.py:310-344` *(`doc_mm`: `HD_HONG` rỗng · 0 mã `:337` · `HD_MA_TRUNG` `:340`)* · `tests/cau_hinh/test_hd.py:196` *(bài duy nhất của `doc_mm`)* | **`CLAUDE.md` Đ5: *"Cổng mới phải được CHỨNG MINH ĐỎ"* — ba nhánh lỗi của `doc_mm` ⛔ có bài.** Đột biến **M27** *(`n >= 2` ⇒ `n >= 99`, ⛔ bắt mã trùng MM)* ⇒ **`26 passed`**; **M28** *(`if not ma:` ⇒ `if False:`, ⛔ bắt ảnh MM 0 mã)* ⇒ **`26 passed`**. Bài duy nhất `test_doc_mm_73_ma_va_chenh_voi_ATL_la_NCF` chạy **đường xanh** *(73 mã · chênh `NCF`)*. `BG-123` ghi *"mỗi lỗi cây mới chứng minh ĐỎ"* — đúng cho `kiem`, **⛔ cho `doc_mm`**. Hệ quả: gỡ cả hai cổng ⇒ `so_mapping_master`/`chenh_mapping_master` tính trên MM trùng/rỗng mà không ai đỏ *(`Đ3`: ảnh MM rỗng ⇒ `chenh` = cả 74 mã, im lặng)* | **Dev**: 3 bài — ảnh MM mã trùng ⇒ `HD_MA_TRUNG` ; ảnh MM 0 dòng ⇒ `HD_HONG` ; `hd_code` rỗng ⇒ `HD_HONG` *(dùng `tmp_path` + `nguon_tinh` như bài `doc_tep`)* | **Mỗi hàm `doc_*` có nhánh `raise` phải có một bài đỏ cho TỪNG tên lỗi** *(đếm: số hằng `HD_*` ↔ số bài `∈ ten`)* | **đóng** *(R2: R2-M6/M7 giết; 3 nhánh `raise` có bài; lõi `doc_mm_van_ban` cùng chốt với đường tệp)* |
| `C4-R1-03` | C4 | R1 | B1 | GHI NHẬN | `tests/cau_hinh/test_hd.py:177-185` *(`test_vo_o_la_loi_HD_HONG`)* · `fls/cau_hinh/hd.py:164` *(bool)* · `:172` *(`n < 1`)* · `:195` *(`if thua`)* | Ba đột biến **SỐNG** ở nhánh `HD_HONG` của `kiem`: **M22** *(`cap=0` nhận: `n < 1` ⇒ `n < 0`)* · **M23** *(`cap=True` nhận: bỏ nhánh `bool`)* · **M26** *(cột lạ nhận: bỏ `if thua:`)* ⇒ mỗi cái `26 passed`. Đo hành vi **gốc**: `cap=0` ⇒ `{HD_HONG}` · `cap=True` ⇒ `{HD_HONG}` *(đúng)*; chỉ là ⛔ có bài ghim **tên** `HD_HONG` cho chúng. Đo M22: gốc `cap=0` ⇒ `{HD_CAP_NHAY}` *(vẫn bị chặn, chỉ ĐỔI TÊN lỗi — ⛔ lọt cây)* ⇒ nhẹ | Dev *(tuỳ, rẻ)*: một bài tham số `cap ∈ {0, True, -1}` + cột lạ ⇒ `HD_HONG ∈ ten` | — *(cùng luật `C4-R1-02`)* | **đóng** *(R2: M22→R2-M3, M23→R2-M2, M26 `if False`: cả ba giết)* |
| `C4-R1-04` | C4 | R1 | B1 | GHI NHẬN | `fls/cau_hinh/hd.py:245-257` *(`while cur is not None and cur in theo_ma`, `if cur in tham` ở `:249`)* · `tests/cau_hinh/test_hd.py:93` | Đột biến **M1** *(`if cur in tham:` ⇒ `if False and cur in tham:`)* ⇒ vòng `while` **⛔ dừng**, `tham` phình đến khi hệ điều hành `kill -9` *(returncode `-9`, OOM — đo 2 lần)*. Bài `test_C4_B2` **bị giết, ⛔ đỏ có khẳng định** ⇒ một hồi quy ở đúng chỗ này làm **treo/ngốn bộ nhớ cả phiên pytest** thay vì in `HD_CHU_TRINH`. Đột biến yếu hơn **M20** *(⛔ ghi lỗi)* + **M21** *(⛔ khử trùng)* ⇒ đều ĐỎ có khẳng định. Mã gốc đúng | Dev *(tuỳ)*: chặn trên `len(tham) > len(theo_ma)` làm lưới phụ; hoặc đánh dấu bài `@pytest.mark.timeout` nếu gói có | **Vòng lặp theo con trỏ cha ⛔ chỉ dựa MỘT `if` làm điều kiện dừng** | **đóng** *(R2: R2-M8 = M1 cũ + lưới ⇒ ĐỎ sạch `1 failed`, ⛔ OOM; R2-M9/M10 lưới cắt non ⇒ giết; ngưỡng `<=` đúng)* |
| `C4-R1-05` | C4 | R1 | B2 | GHI NHẬN | `fls/cau_hinh/tinh/ix_mapping_master.json` *(`phu.tho`, 84 hàng)* · `tools/kiem_so_song.py:406` | **(a)** Gói `fls/` chép **nguyên** ảnh MM *(sha256 `3c1f61a2…` = ảnh DT3, khớp từng byte)* trong khi `C4` chỉ đọc **`hd_code`** *(`doc_mm`)*. Bảng phụ `tho` mang **84 hàng**, trong đó **51 hàng** có chuỗi ≥ 6 chữ số ở cột A *(dạng `R`, dấu gạch đứng, số tài khoản, `_`, tên ngân hàng, tiền tệ, pháp nhân)* — DT3 đã duyệt ảnh *(`KQ-121` ĐẠT, 7 hàng cá nhân đã ẩn danh)*, nhưng nay **nhân đôi bề mặt** *(fixture + gói)*. Email `@`: **0** ở cả hai tệp. **(b)** `kiem_so_song.py` — thuộc danh sách cổng WO §5 — gọi `.venv/Scripts/lint-imports.exe` *(grep `Scripts/lint-imports` trong `tools/ docs/ITL/_tools/ fls/`: **1** chỗ, dòng 406)* ⇒ ⛔ chạy ở container Linux; Dev khai thật *(BG "CHƯA CHẠY")*. R1 ⛔ có bằng chứng `kiem_so_song` xanh cho `C4` | **Orchestrator**: (a) `C5` gỡ hai tệp *(đã dự kiến)* — hoặc cắt bản gói chỉ giữ `dong` *(bài ghim byte sẽ đổi thành ghim `dong`)*; (b) mở một phiếu nhỏ sửa đường `lint-imports` theo nền tảng *(⛔ việc C4)* | **Tệp trong `fls/cau_hinh/tinh/` chỉ mang cột mà tầng đọc dùng** ; công cụ cổng ⛔ gõ cứng đường nền tảng | **chuyển** *(R3, theo orchestrator 18/11: **(a) → `C5` · `WO-142` AC-6b** — gỡ hai ảnh tĩnh; **(b) → backlog** phiếu riêng; ⛔ chặn gộp `C4`)* |
| `C4-R2-01` | C4 | R2 | B1 | GHI NHẬN | `fls/cau_hinh/hd.py:173-174` *(`_so`: `int(s)`)* · `:306` *(`json.loads` ở `doc_van_ban`)* · `:347` *(`doc_mm_van_ban`)* | **Vòng sửa `C4-R1-01` chưa bịt hết lối `ValueError` trơn.** Đo `kiem`/`doc_van_ban`/`doc_mm_van_ban` *(mã R2, ảnh tổng hợp)*: chuỗi `cap`/`thu_tu` = `'9'*5000` ⇒ `isascii()`+`isdigit()` qua, `int(s)` NÉM **`ValueError: Exceeds the limit (4300 digits)`** ; literal số JSON 5000 chữ số ở `cap` *(`doc_van_ban`)* hay ở ô ảnh MM *(`doc_mm_van_ban`)* ⇒ cùng `ValueError` — **⛔ phải `JSONDecodeError`** nên `except json.JSONDecodeError` ⛔ bắt; `'['*100000` ⇒ **`RecursionError`**. Cả bốn ⛔ mang tên `HD_HONG`. Chạm được cần ô ≥ 4301 chữ số / JSON lồng sâu *(đo ở 100.000 tầng; ⛔ đo ngưỡng thấp nhất)*; ảnh gói đóng băng ⇒ hôm nay 0 đường chạm *(`cap` ảnh DT3 là `'1'…'4'` — `KQ-124` đo)*, hết đóng băng ở `C5` | **Dev** *(tuỳ, rẻ)*: `_so` giới hạn `len(s) <= 18` hoặc bọc `int()` trong `try/except ValueError`; `except (ValueError, RecursionError)` quanh `json.loads` ở hai lõi *(`JSONDecodeError` là con của `ValueError`, một `except ValueError` đủ cho ba lối đầu)*; mỗi lối một bài | **Ở tầng `cau_hinh`, `except` quanh `json.loads`/`int()` phải bắt họ `ValueError` *(+ `RecursionError` cho JSON)*, ⛔ chỉ lớp con hẹp** — lỗi giới hạn chữ số của CPython là `ValueError` thường | **chuyển `C5`** *(R3, orchestrator 18/11: lối ngoại lệ trơn ≥ 4.301 chữ số / `RecursionError` ⇒ ảnh gói đóng băng ⇒ 0 đường chạm hôm nay; mang theo trong `WO-142` — ⛔ có `AC-8`, xem `C4-R3-03`)* |
| `C4-R2-02` | C4 | R2 | B1 | GHI NHẬN | `fls/cau_hinh/hd.py:139-141` *(`_mot_dong`)* · `:170`, `:175`, `:206` *(câu lỗi đưa `repr(v)` vào)* | Câu lỗi `HD_HONG` nhắc **nguyên** giá trị ô, ⛔ cắt độ dài. Đo: ô `cap`/`thu_tu` = `'x'*100000` ⇒ `str(LoiHD)` **100.121** / **100.120** ký tự; `ma=['x'*100000]` ⇒ **100.150**. Một dòng *(đã `" ".join(split())`)* nhưng ⛔ ngắn. Lộ giá trị: với ảnh hiện có là mã/cấp HD *(⛔ PII)*; ⛔ lộ khoá/secret nào *(ảnh ⛔ mang cột đó)*. JSON hỏng ⇒ câu chỉ có `str(JSONDecodeError)` *(`Expecting value: line 1 column 1 (char 0)`, ⛔ trích văn bản)* và `from None` ⇒ ⛔ gắn `__context__` ⇒ ⛔ lộ `doc` | Dev *(tuỳ)*: `_mot_dong` cắt `repr` ở ~80 ký tự + `…` | **Giá trị lạ đưa vào câu lỗi phải cắt độ dài** | **chuyển `C5`** *(R3, orchestrator 18/11: câu lỗi dài ⛔ cắt ⇒ ảnh gói đóng băng ⇒ 0 đường chạm hôm nay; mang theo trong `WO-142` — ⛔ có `AC-8`, xem `C4-R3-03`)* |
| `C4-R2-03` | C4 | R2 | B1 | GHI NHẬN | `fls/cau_hinh/hd.py:173` *(`_so` nhánh chuỗi)* · `tests/cau_hinh/test_hd.py` *(`cap_isdigit_ngoai_ASCII` chỉ `['²','١']`)* | Đột biến **R2-M12** *(`_so` nhận thêm dấu `+`: `.strip().lstrip('+')`)* ⇒ **`31 passed`, SỐNG**. Đo hành vi gốc: `'+3'`·`'-3'`·`'3_0'`·`''`·`'٣'`·`'３'`·`3.0`·`None` ⇒ `(None, lý do)`; `' 3'`·`'03'`·`'3\n'`·`'\t3'` ⇒ `3`; `True` ⇒ bị chặn. Đúng ý, chỉ ⛔ có bài ghim biên chuỗi *(`'+3'`, `'3_0'`, `''`, `'３'` toàn rộng)*. Vô hại *(`+3`=3)* ⇒ nhẹ. *(R2-M13 `hd_code` rỗng `continue`→`pass` cũng sống nhưng là **đột biến tương đương** — `loi.append` đã chạy trước, vẫn `raise`; ⛔ tính)* | Dev *(tuỳ)*: một bài tham số `["+3","3_0","","３"]` ⇒ `HD_HONG` | — *(cùng luật `C4-R1-02`)* | **chuyển `C5`** *(R3, orchestrator 18/11: bài biên `_so` ⇒ ảnh gói đóng băng ⇒ 0 đường chạm hôm nay; mang theo trong `WO-142` — ⛔ có `AC-8`, xem `C4-R3-03`)* |
| `C4-R3-01` | C4 | R3 | B1 | GHI NHẬN | `fls/api/xu_ly.py:1083-1085` *(`cay_hd`: `"ten": n.ten` · `"nhom": n.nhom` · `"dong_sheet": n.dong_sheet`)* · `tests/api/test_isp_config_hd.py:107-138` | **Ba trường của nút trong HTTP ⛔ có bài ghim GIÁ TRỊ** — bài `…200_DUNG_hop_dong` chỉ ghim **tập khoá** `KHOA_NUT` cho 74 nút, còn giá trị chỉ ghim `ma` · `cha` · `cap` · `con_cua` · `la`. Đột biến *(bản sao `git archive`, trả nguyên)*: **R3-M12** `"dong_sheet": n.ten` · **R3-M14** `"ten": n.ma` · **R3-M15** `"nhom": n.ten` ⇒ mỗi cái **`41 passed` — SỐNG** *(đối chiếu: M16 `cap + 1` ⇒ `1 failed, 31 passed` giết; `AC-4` của `WO-122` đòi `con_cua`/`la` — ⛔ đòi ba trường này, nên **nhẹ**)*. `nhom` còn được ghim ở mức **lõi** *(`test_hd.py`, đột biến R3-M8 giết)* — chỉ lớp **tuyến** ⛔ ghim | Dev *(tuỳ, rẻ — gom vào `C5`)*: ghim 1 nút thật `theo_ma["OPC"]["ten"] · ["nhom"] · ["dong_sheet"]` đúng giá trị ảnh | **Bài tuyến phải ghim GIÁ TRỊ mọi trường, ⛔ chỉ tập khoá** *(`Đ3`: khoá có mặt ≠ giá trị đúng)* | mở *(ghi nhận)* |
| `C4-R3-02` | C4 | R3 | B1 | GHI NHẬN | `fls/api/xu_ly.py:1081` *(`sorted(atl_ma - set(mm))`)* | Đột biến **R3-M3** *(`sorted(...)` ⇒ `list(...)`)* ⇒ **`41 passed` — SỐNG**. Lý do: trên ảnh thật chênh chỉ **1 phần tử** `{NCF}` *(đo lại: `ATL−MM = ['NCF']` · `MM−ATL = []` · 74 ∩ 73)* ⇒ `sorted` ⛔ đổi thứ tự — **tương đương trên ảnh thật**; chú thích nói *"`sorted` cho tất định"* nhưng ⛔ có bài ảnh ≥ 2 mã chênh để chứng minh. Vô hại hôm nay *(ảnh đóng băng)*; chỉ cắn khi `C5` đọc ảnh từ kho có ≥ 2 mã chênh | Dev *(tuỳ)*: khi `C5` đổi nguồn, thêm bài hai mã chênh | — *(cùng luật `C4-R3-01`)* | mở *(ghi nhận)* |
| `C4-R3-03` | C4 | R3 | B2 | GHI NHẬN | `docs/ITL/01_Orchestrator/handoff/WO-142-isp-c5-kho-cau-hinh-chi-them.md` *(nhánh làm việc `3cac59f`)* | **Món nợ chuyển sang `C5` ⛔ có chỗ đậu trong `WO-142`.** Chỉ thị orchestrator nói `C4-R2-01/02/03` → *"`WO-142` AC-6b + **AC-8**"*. Đo `WO-142` trên `origin/moi/lam_viec`: bảng AC có `AC-1…AC-7` + `AC-6b` — grep `AC-8` = **0**; grep `ValueError` · `RecursionError` · `4300` · `C4-R2` = **0** *(`AC-6b` nhắc `C4-R1-05(a)` — chỉ về gỡ hai ảnh tĩnh; grep `docs/` nhánh làm việc: `C4-R2-0` = **0**)*. ⇒ nếu `WO-142` giao nguyên văn, ba mục `C4-R2-01…03` **chỉ sống ở sổ này**; `AC-6b` gỡ ảnh nhưng **giữ lõi `hd.py`** *(`_so`/`json.loads`)* — lối `ValueError` trơn vẫn mở khi `C5` nạp JSON từ kho *(lúc đó ảnh hết đóng băng)*. ⛔ chặn gộp `C4` *(mã `C4` đúng; chỉ thiếu chỗ mang nợ)* | **Orchestrator**: thêm `AC-8` vào `WO-142` *("`hd.py`: nạp từ kho ⇒ mọi ô/JSON hỏng ⇒ `LoiHD` có tên — gồm chuỗi ≥ 4.301 chữ số, `RecursionError`; cắt `repr` ≈ 80 ký tự; bài biên `_so` `['+3','3_0','','３']`")* trước khi giao `C5` | **Nợ chuyển bước ⇒ phải có AC mang MÃ nợ trong phiếu bước nhận** | mở *(→ orchestrator)* |

## R2 *(`KQ-125`, ngày 2026-11-18)* — đối tượng `isp/C4` @ `31509bd` *(mã `d6dea99` + `BG-123`)*, cụm PG **5444**
**Kết R2: `ĐẠT` — 0 CHẶN.** `C4-R1-01…04` **đóng** *(tự đột biến lại đúng chỗ — bài cắn)*; `C4-R1-05` → orchestrator đã chốt. 3 phát hiện mới `C4-R2-01…03` *(đều GHI NHẬN)*.

| Mã đột biến *(bản sao `git archive`, `/tmp/…/mut`)* | Phá | Kết | |
|---|---|---|:-:|
| R2-M1 | `_so` bỏ `isascii()` | `1 failed, 16 passed` *(`…cap_isdigit…[²]`)* | giết |
| R2-M2 | `_so` bỏ nhánh `bool` | `1 failed, 28 passed` *(`cap_sai[True]`)* | giết |
| R2-M3 | `_cap` `n < 1` ⇒ `n < 0` | `1 failed, 27 passed` *(`cap_sai[0]`)* | giết |
| R2-M4 | `thu_tu` ⛔ kiểm *(`tt, ly = i, ''`)* | `1 failed, 18 passed` | giết |
| R2-M5 | `doc_van_ban` gỡ `try` JSON | `1 failed, 21 passed` | giết |
| R2-M6 | `doc_mm_van_ban` `n >= 2` ⇒ `99` | `1 failed, 23 passed` | giết |
| R2-M7 | `doc_mm_van_ban` 0 mã `if False` | `1 failed, 24 passed` | giết |
| R2-M8 | **M1 cũ** *(`if False and cur in tham`)* **+ lưới** | `1 failed, 6 passed` — **ĐỎ có khẳng định, ⛔ OOM** | giết |
| R2-M9 / M10 | lưới cắt non `< len-1` / `< len` | `1 failed, 6 passed` mỗi cái | giết |
| R2-M11 | gỡ lưới *(không đổi `if cur in tham`)* | `31 passed` — **tương đương** *(lưới là belt; ⛔ tính)* | — |
| R2-M12 | `_so` nhận dấu `+` | `31 passed` | **SỐNG** → `C4-R2-03` |
| R2-M13 | `hd_code` rỗng `continue`→`pass` | `31 passed` | tương đương |
| R2-M14 | `doc_mm_van_ban` gỡ `raise` JSON | `1 failed, 22 passed` | giết |
| M26 *(`if thua:` ⇒ `if False`)* | cột lạ nhận | `1 failed, 30 passed` | giết |

**15 đột biến: 13 có nghĩa = 12 giết · 1 sống; 2 tương đương** *(R2-M11, M13 ⛔ tính)*. Trả nguyên ⇒ `31 passed`; `git status` worktree sạch. Lưới `while`: cây chuỗi 150 nút hợp lệ ⇒ 150 nút, ⛔ cắt; vòng đủ 150 nút ⇒ `{HD_CAP_NHAY, HD_CHU_TRINH}` ⇒ ngưỡng `len(tham) <= len(theo_ma)` **đúng**.

## R3 *(`KQ-126`, ngày 2026-11-18)* — đối tượng `isp/C4` @ `5837455` *(mã `d6dea99`)*, cụm PG **5446**
**Kết R3: `ĐẠT` — 0 CHẶN · 0 NÊN SỬA.** `C4-R2-01…03` + `C4-R1-05` ⇒ trạng thái **`chuyển`** *(⛔ còn "mở" mơ hồ)*. 3 phát hiện mới `C4-R3-01…03` *(đều GHI NHẬN)*. **Cây gộp thử**: 2 tệp xung đột *(`tools/dung_moi_truong_isp.sh` · `tests/test_dung_moi_truong_isp.py`)* ⇒ giữ bản nhánh làm việc; sàn `3100 → 3141` *(= thu thập cây gộp; web `667`)*; `--duong-nen` ⇒ **`KẾT: ĐẠT`** *(`28 = 28` · chạy `3141` · web `3 = 3`)*.

| Mã đột biến *(bản sao `git archive isp/C4`, `/tmp/r3_c4/mut`; vùng tuyến `/config/hd`)* | Phá | Kết | |
|---|---|---|:-:|
| R3-M1 | `cay_hd` gỡ cổng `?run_id=` ⇒ 400 | `1 failed, 32 passed` *(`…run_id_o_tuyen_TINH…400`)* | giết |
| R3-M2 | `chenh_mapping_master` đảo chiều `MM − ATL` | `1 failed, 31 passed` *(`…200_DUNG_hop_dong`)* | giết |
| R3-M3 | `chenh_mapping_master` bỏ `sorted` | `41 passed` — tương đương trên ảnh thật *(1 mã chênh)* | **SỐNG** → `C4-R3-02` |
| R3-M4 | `so_mapping_master = len(cay.nut)` *(74 thay 73)* | `1 failed, 31 passed` | giết |
| R3-M5 | `la` luôn `True` | `1 failed, 31 passed` | giết |
| R3-M6 | `data_status` `flash` ⇒ `reconciled` *(`INV-I14`)* | `1 failed, 31 passed` | giết |
| R3-M7 | `_ma_mm` bỏ `.strip()` *(73 mã dính khoảng trắng ⇒ chênh sai)* | `1 failed, 15 passed` *(`test_doc_mm_73…NCF`)* | giết |
| R3-M8 | `CayHD.nhom` sắp xếp *(đổi thứ tự 6 nhóm)* | `1 failed` *(`test_C4_B1_nap_anh_ATL_74…`, `-x`)* | giết |
| R3-M9 | `so_atl = len(mm)` *(73 thay 74)* | `1 failed, 31 passed` | giết |
| R3-M10 | `goc` = mọi nút *(74 thay 37)* | `1 failed, 31 passed` | giết |
| R3-M11 | `con_cua` đảo thứ tự | `1 failed, 31 passed` | giết |
| R3-M12 | nút `dong_sheet = ten` | `41 passed` | **SỐNG** → `C4-R3-01` |
| R3-M13 | `nguon_mm = ""` | `1 failed, 31 passed` | giết |
| R3-M14 | nút `ten = ma` | `41 passed` | **SỐNG** → `C4-R3-01` |
| R3-M15 | nút `nhom = ten` | `41 passed` | **SỐNG** → `C4-R3-01` |
| R3-M16 | nút `cap + 1` | `1 failed, 31 passed` | giết |

**16 đột biến: 12 giết · 4 sống** *(M3 · M12 · M14 · M15 — tất cả GHI NHẬN, ⛔ chặn)*. Bản sao `git archive` ⛔ phải kho git ⇒ đo *"trả nguyên"* bằng `md5sum` `xu_ly.py` gốc = bản sao; chạy lại ⇒ `41 passed`; worktree `isp/C4` `git status` sạch.

**Đo lại độc lập trên mã cuối** *(`python -I`, `hd.doc_tep()`/`hd.doc_mm()`)*: nút ATL **74** · mã duy nhất **74** · mã MM **73** · duy nhất **73** · `ATL−MM = ['NCF']` · `MM−ATL = []` *(`Đ3`: cả hai chiều)* · gốc **37** · nhóm `HDO·HDH·HDAP·HDT·HDC·HDCI` · cấp `(1,37)(2,23)(3,11)(4,3)` Σ**74** · nút lá **64** *(`Đ4`: **lá của cây IX.HD**, ⛔ cùng nhãn "64 cột có tên" `ITL Ledge`)*.

## Cổng R1 tự chạy *(so với `BG-123`)*
| Lệnh | `BG-123` nói | R1 đo *(cụm 5444)* | Khớp |
|---|---|---|:-:|
| `pytest tests/cau_hinh/test_hd.py tests/api/test_isp_config_hd.py` | `26 passed` | `26 passed in 0.94s` | ✅ |
| `pytest tests/api tests/cau_hinh` | *(BG ⛔ ghi)* | `3 failed, 530 passed, 11 errors` — 14 nút đỏ: 11 `tests/api/test_mui_thu_luoi.py` *(ERROR)* + 3 `…_pg.py` *(`wo032_v2` · `wo037` · `wo037_v2`)* ⇒ **⛔ có tệp C4 nào** *(đều thuộc đường nền — xem dòng kế)* | ✅ |
| `--duong-nen --cong 5444` *(GOC = `…/isp-c4`, một mình)* | `KẾT: ĐẠT` · `28 = 28` · chạy 3093 · web `3 = 3` · 667 | `KẾT: ĐẠT` · `12 failed, 3065 passed, 2 xfailed, 14 errors in 382s` ⇒ `28 = 28 (XFAIL 2 = 2 · thêm 0 · bớt 0) · chạy 3093 (mong ≥ 3093) · skipped 0 · deselected 0`; web `3 failed, 664 passed` ⇒ `3 = 3 · chạy 667 (mong ≥ 667) · skipped 0` | ✅ |
| `lint-imports` | `11 kept, 0 broken` | `Contracts: 11 kept, 0 broken.` | ✅ |
| `soi_bang_tuyen.py` | ĐẠT · 42 tuyến | `✅ ban khai KHOP SQL that o ca 42 tuyen` · `TINH […ix_hd_cay.json, …ix_mapping_master.json] · vet 11 ham` | ✅ |
| `kiem_tai_lieu.py` | ĐẠT · 240 file · 2270 bảng | ĐẠT · **241** file · **2273** bảng · 776 ô ngày · 104 mã QĐ *(lệch +1 file/+3 bảng = chính `BG-123` ở commit sau mã)* | ✅ |
| `pytest --collect-only` *(Q8)* | 3093 · web 667 | tổng **3093** *(227 tệp)* · `tests/web` **667** *(đếm `awk` trên `--collect-only -q`)* ⇒ hằng `MONG_PYTEST_TOAN_BO=3093`/`MONG_PYTEST_WEB=667` **= thu thập** | ✅ |
| `kiem_so_song.py` | ⛔ CHƯA CHẠY | ⛔ chạy được — đường Windows `tools/kiem_so_song.py:406` | — *(→ `C4-R1-05`)* |

## Đo độc lập *(mã CỦA R1, ⛔ gọi lại `hd.py`)* — `/tmp/r1_c4/do.py` · `http_probe.py`
| Phép đo | Nhãn | Kết quả |
|---|---|---|
| Đếm nút ảnh `atl_cay.json` | dòng mã · duy nhất | **74** · **74** |
| Nhóm theo thứ tự xuất hiện | nhóm | **6**: `HDO · HDH · HDAP · HDT · HDC · HDCI` |
| Cấp *(cột `cap` — ⛔ là chuỗi trong ảnh `'1'`…`'4'`)* | nút/cấp | `L1 37 · L2 23 · L3 11 · L4 3` *(Σ 74 — khớp `MONG_CAP`)* |
| Tính lại `cha` = *"mã gần nhất phía trên có cấp nhỏ hơn, TRONG nhóm"* | nút lệch | **0 / 74** |
| `MM` *(`mapping_master_cfg.json`)* | mã `hd_code` · duy nhất · có ` \| ` | **73** · **73** · **73/73** |
| `ATL − MM` · `MM − ATL` | mã | `{NCF}` · **`∅`** *(Đ3: cả hai chiều, ⛔ chỉ chiều dự kiến)* |
| Ảnh gói ↔ ảnh DT3 | sha256 | cả hai cặp **khớp từng byte** *(`504fa53d…` · `3c1f61a2…`)* |
| `GET /api/fls/v1/config/hd` *(máy thật, thẻ HS256, PG 5444)* | HTTP | **200** · `so_atl=74` · `so_mapping_master=73` · `chenh_mapping_master=['NCF']` · `len(nut)=74` · `len(goc)=37` · `nhom` đúng thứ tự · `meta.data_status='flash'` |
| `con_cua`/`la` của 74 nút so với tính lại của R1 | nút lệch | **0 / 74** · `la=True` ở **64** nút *(= 74 − 10 cha; `Đ4`: 64 là **nút lá**, ⛔ cùng nhãn "64 cột có tên" của `ITL Ledge`)* · thứ tự ảnh giữ · `cap` mỗi nút khớp |
| `?run_id=NAP-2026-01-01-X` | HTTP | **400** `FLS-BAD-REQUEST` *(`data=None`)* |
| không thẻ · `POST` | HTTP | **401** · **405** |
| Trả lời chứa `@` | số | **0** *(⛔ PII)* |
| Cây TỔNG HỢP do R1 dựng *(`/tmp/r1_c4/syn.py`)* | tên lỗi | `A→B→A` ⇒ `{HD_CAP_NHAY, HD_CHU_TRINH}` *(3 lỗi)* · vòng 3 nút ⇒ cùng hai tên · cha vắng ⇒ `{HD_CHA_VANG}` · con cấp 3 dưới cấp 1 ⇒ `{HD_CAP_NHAY}` · gốc cấp 2 ⇒ `{HD_CAP_NHAY}` · cây hợp lệ 4 nút ⇒ **sạch** *(Đ5 chiều kia)* · `[]` ⇒ `{HD_HONG}` *(Đ3)* |

⛔ **Ràng buộc (e)** — `hd.py` import đúng `json · collections · dataclasses · typing · fls.cau_hinh.nguon_tinh` *(⛔ `psycopg`, ⛔ `fls.db`/`fls.repo`)*; `lint-imports` hợp đồng cho `fls.cau_hinh` giữ *(11 kept)*; tuyến ⛔ có phép cộng trên cột số *(⛔ `sum(`)*; `chenh_mapping_master` chỉ liệt kê *(⛔ ghi lại hay sửa ATL/MM)*. `soi_bang_tuyen`: SQL của tuyến mới **0 bảng**.

## Đột biến *(bản sao `git archive isp/C4`, 29 chỗ; mỗi chỗ trả nguyên; chạy `test_hd.py` + `test_isp_config_hd.py -x`)*
| Mã | Phá | Bài đỏ / kết | |
|---|---|---|:-:|
| M1 | `HD_CHU_TRINH` ⛔ dừng vòng *(`if False and cur in tham`)* | `-9` OOM *(vòng vô hạn)* ⇒ **→ `C4-R1-04`** | giết* |
| M2 | `HD_CHA_VANG` ⛔ bắt *(`if False`)* | `1 failed, 8 passed` | giết |
| M3 | `HD_CAP_NHAY` chỉ bắt `<` *(⛔ n+2)* | `1 failed, 9 passed` | giết |
| M4 | gốc cấp ≠ 1 ⛔ bắt | `1 failed, 10 passed` | giết |
| M5 | `chenh_mapping_master=[]` | `1 failed, 16 passed` | giết |
| M6 | `la()` đảo | `1 failed, 2 passed` | giết |
| M7 | `con_cua` ⇒ `()` | `1 failed, 2 passed` | giết |
| M8 | `?run_id=` ⛔ 400 | `1 failed, 17 passed` | giết |
| M9 | `_ma_mm` ⛔ tách `\|` | `1 failed, 15 passed` | giết |
| M10 | 0 nút ⛔ nổ *(Đ3)* | `1 failed, 14 passed` | giết |
| M11 | `HD_MA_TRUNG` ⛔ bắt *(`kiem`)* | `1 failed, 12 passed` | giết |
| M12 | `data_status="signed"` | `1 failed, 16 passed` | giết |
| M13 | `so_atl` − 1 | `1 failed, 16 passed` | giết |
| M14 | `nhom` rớt nhóm thứ 6 | `1 failed` | giết |
| M15 | tuyến khai `nguon_tinh` thiếu MM | `1 failed, 20 passed` | giết |
| M16 | vỏ ô lạ ⇒ nhận | `1 failed, 13 passed` | giết |
| M17 | bỏ sắp theo `thu_tu` | `1 failed` | giết |
| M18 | `goc` tính sai | `1 failed` | giết |
| M19 | sửa 1 cấp trong ảnh gói `ix_hd_cay.json` | `1 failed, 4 passed` *(bài ghim byte)* | giết |
| M20 | `HD_CHU_TRINH` ⛔ ghi lỗi | `1 failed, 6 passed` | giết |
| M21 | `HD_CHU_TRINH` ⛔ khử trùng *(báo lặp)* | `1 failed, 6 passed` | giết |
| M22 | `cap=0` nhận | `26 passed` | **SỐNG** |
| M23 | `cap=True` nhận | `26 passed` | **SỐNG** |
| M24 | `HD_CAP_NHAY` bỏ nhánh có cha | `1 failed, 9 passed` | giết |
| M25 | vỏ nhiều khoá nhận | `1 failed, 13 passed` | giết |
| M26 | cột lạ nhận | `26 passed` | **SỐNG** |
| M27 | `doc_mm` mã trùng ⛔ bắt | `26 passed` | **SỐNG** → `C4-R1-02` |
| M28 | `doc_mm` 0 mã ⛔ bắt | `26 passed` | **SỐNG** → `C4-R1-02` |
| M29 | `chenh` đổi chiều `MM − ATL` | `1 failed, 16 passed` | giết |

**24/29 giết · 5 SỐNG** *(M22 M23 M26 → `C4-R1-03`; M27 M28 → `C4-R1-02`)*. *\* M1 "giết" bằng OOM, ⛔ bằng khẳng định.* Bản gốc trả nguyên ⇒ `26 passed`; `git status` worktree sạch.

## Changelog
- **v0.1** *(2026-11-18, `fls-test` R1 của `C4`, `KQ-124`)*: khởi tạo — 5 phát hiện `C4-R1-01…05` *(**0 CHẶN** · 2 NÊN SỬA · 3 GHI NHẬN)*.
- **v0.2** *(2026-11-18, `fls-test` R2 của `C4`, `KQ-125`)*: R2 — 3 phát hiện `C4-R2-01…03` *(**0 CHẶN** · 0 NÊN SỬA · 3 GHI NHẬN)*; đổi **Trạng thái** `C4-R1-01…05`; thêm bảng đột biến R2.
- **v0.3** *(2026-11-18, `fls-test` R3 của `C4`, `KQ-126`)*: R3 — 3 phát hiện `C4-R3-01…03` *(**0 CHẶN** · 0 NÊN SỬA · 3 GHI NHẬN)*; đổi **Trạng thái** `C4-R1-05` + `C4-R2-01…03` ⇒ **`chuyển`** *(⛔ "mở")*; thêm mục R3 + 16 đột biến vùng `/config/hd` + kết cây gộp thử.
