# FLS — hướng dẫn cho phiên làm việc

**FLS** = sổ cái ITL code hoá, thay sổ Google Sheets kế toán đang chạy tay.
Kho: PostgreSQL trong Docker (`fls-pg-1`, cổng `5433`). Tài liệu: `docs/ITL/`.

> ⭐ **Kế hoạch đang sống:** `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md` §6 *(việc)* · `docs/ITL/03_Dev/03_IMPLEMENTATION_PLAN.md` *(pha)* · `docs/ITL/_AUDIT_ALIGNMENT_ROADMAP.md` *(audit đang chạy)*.
> Sổ quyết định: `docs/ITL/00_MASTER_INDEX.md` *(`QĐ-ITL-…`, `CR#…`)*.
> ⭐ **Ba agent dự án** *(`.claude/agents/`)*: `fls-ba` *(BA · UIUX · PO)* · `fls-dev` · `fls-test` — nói với nhau **chỉ qua phiếu** `WO`/`HOI`·`TL`/`BG`/`KQ` ở `docs/ITL/01_Orchestrator/handoff/`. Luật: `docs/ITL/01_Orchestrator/10_HOP_DONG_AGENT.md`.

---

## ⛔⛔⛔ NĂM LUẬT ĐO — mỗi luật là một lỗi ĐÃ XẢY RA, ⛔ không phải lời khuyên

### `Đ1` · Trước khi viết một câu **PHỦ ĐỊNH**, hãy tìm — ở **CẢ HAI** nơi

> *"⛔ không tệp nào ghi X"* · *"chưa ai đo X"* · *"chưa bao giờ có X"*

⛔ **Cắn BA LẦN trong một buổi (17/09)**, và cả ba lần thứ bị phủ định **đang tồn tại**:

| Tôi viết | Nó nằm ở đâu |
|---|---|
| *"tài liệu chưa bao giờ đọc TÊN TỆP"* | `BA-05:39` + `:130` |
| *"cấu trúc `ITL Ledge` chưa ai nối được về nguồn"* | `BA-05 §DD-I04` — khai **trọn**, từng hàng `1`→`8` |
| *"⛔ không tệp nào ghi bề rộng `PM_Unpivot`"* | `FLS-Process-PM-den-ITL.md:186` **và** `pm_join.py:192` |

⇒ **Grep `docs/` LẪN `fls/` + `tools/` trong chính lượt ấy, rồi dán SỐ ĐẾM cạnh câu.**
⭐ Ở repo này một sự thật đã đo **thường sống trong CHÚ THÍCH MÃ**, ⛔ không phải trong tài liệu.
*(Có còi nhắc: `.claude/hooks/soi_cau_phu_dinh.py`.)*

### `Đ2` · Phép **ĐẾM CHỮ** ⛔ không phân biệt được **KHAI** với **BIÊN BẢN**

⛔ Cắn **hai lần trong một giờ**: viết cổng đếm `"52 cột"` đòi `= 0`; sửa xong lại viết cổng đếm `"38 cột canon"` đòi `= 0` — **lệch mãi**, vì chính **câu đính chính** phải trích lại chuỗi sai.

Đo thật: **`18/19`** chỗ ghi `"52 cột"` là **biên bản** *(sổ `QĐ`/`CR`, changelog, mô tả `GAP`, câu về nguyên mẫu `748 × 52`)*. Ở đó **số cũ là ĐÚNG** — xoá là **viết lại lịch sử**.

⇒ ⭐ **So HAI NGUỒN** *(tài liệu ↔ mã)*, và hỏi ***"câu ĐÚNG có chưa"*** ⛔ **không** hỏi *"chuỗi sai còn không"*.
**Bằng chứng DƯƠNG ⛔ không bị biên bản làm nhiễu; bằng chứng ÂM thì bị.**

### `Đ3` · Một phép đo ra **`0`** phải chứng minh **tập KHÔNG RỖNG** trước khi kết luận

⛔ Nối *"nội dung gõ ở bank"* với `Diễn giải` sao kê ⇒ **`0` khớp**, suýt kết luận *"⛔ không phải khoá ghép"*. Thật ra **`fls_itl.memo` NULL trên `8.387/8.387`** — phép so **xanh trên tập rỗng**.

⇒ Mọi phép so ra `0` hoặc `100%`: **đếm mẫu số trước**, và nếu mẫu số là `0` thì đó là **kết quả**, ⛔ không phải nền.

### `Đ4` · Một con số phải nói **NÓ ĐẾM GÌ**, ngay tại chỗ in

⛔ Tôi báo *"`ITL Ledge` là `69` ⛔ không phải `64`"* — sai: `69` là **bề rộng hàng** *(kể cả đuôi rỗng)*, `64` là **cột CÓ TÊN** *(hàng `7`+`8`)*. Tài liệu đúng.

⛔ Và `BA-06` khai *"52 = 38 canon + 14 hợp đồng"* trong khi thật là **`24` nền + `28` canon** — **cả hai đều ra `52`**, nên mọi cổng canh **tổng** xanh suốt **20 ngày**.

⇒ `38`/`36` khuôn canon · `52` lưới `F02` · `64` cột có tên `ITL Ledge` · `23` lưới **ngày 03/09**: **mỗi số đếm một vật khác**. Thiếu **nhãn**, ⛔ không thiếu con số.

### `Đ5` · Cổng phải khai **`mong`**, và **NO khi khác — cả hai chiều**

Một cổng chỉ báo *"có lệch"* thì nó **xanh mãi mãi**. Khai trước kết quả mong đợi ⇒ **sửa được một chỗ cũng ĐỎ**, buộc ghi lại bản khai.
⛔ **Phép ⛔ không đo được là ĐỎ**, ⛔ không phải *"không thấy lệch"* — kho tắt, mẫu khớp `0` hoặc `≥2` lần, tập rỗng.
⭐ **Cổng mới phải được CHỨNG MINH ĐỎ** *(phá nguồn, chạy, xem nó cắn, trả nguyên)* trước khi được tin.

---

## Cổng — chạy trước khi báo xong

```bash
export PG_DSN='postgresql://fls:fls@localhost:5433/fls'   # trùng mặc định ở fls/db/kho.py

python -m pytest                                 # ~1.677 bài · ~4 phút
python tools/kiem_so_song.py                     # 109 phép so SỐ SỐNG ↔ máy
python tools/dong_bo_so_song.py --ghi            #   …lệch thì soạn lại
python docs/ITL/_tools/kiem_tai_lieu.py          # K1–K5 (giấy)
python docs/ITL/_tools/khop_owner.py --kiem      # C1 · bảng đối chiếu audit
python tools/soi_bang_tuyen.py                   # 37 tuyến ↔ SQL thật
python tools/kiem_thuyet_minh.py                 # 31 nút
.venv/Scripts/lint-imports.exe                   # 9 hợp đồng tầng
python -m fls.db.pg_migrate                      # di trú → tự chạy pg_verify
```

⚠ Sinh lại **hiện vật** sau khi đổi `schema.py`:
`python -m fls.db.erd_export --write` · `python tools/sync_erd_doc.py docs/ITL/02_BA/05_DATA_DICTIONARY_ERD.md` · `python tools/sinh_ban_do_tang.py` · `pytest tests/db/test_schema_fls_itl.py --update-golden`

---

## ⛔ Bẫy đã cắn — ⛔ đừng cắn lại

| | |
|---|---|
| ⛔⛔ **⛔ KHÔNG BAO GIỜ `docker compose down`** | `docker-compose.yml` ⛔ không khai `volumes:` ⇒ kho nằm trên **volume vô danh**; một lệnh `down` là kho rỗng. Khởi động lại bằng **`docker start fls-pg-1`** |
| `PYTHONUTF8=1` | thiếu nó thì `lint-imports` giải mã nguồn tiếng Việt bằng codepage hệ thống và **im lặng in 0 byte** *(đã đặt sẵn trong `.claude/settings.json`)* |
| `pytest` thêm `-q` | `pyproject.toml` đã có `-q`; thêm nữa thành `-qq` và **mất dòng tổng kết** |
| Bản `.xlsx` xuất offline | đọc được **HÌNH DẠNG**, ⛔ **không** đọc **GIÁ TRỊ** — đã chứng minh nó **phá huỷ ngày** *(chỉ còn `2,7%` đúng)* |
| Dấu `\|` trần trong ô bảng markdown | **vỡ cả bảng** mà mắt ⛔ không thấy; máy sinh bảng phải **thoát ở chỗ sinh** |
| Sửa tệp bằng `python -c` / heredoc qua **hai lớp shell** | `\n` biến dạng — dùng tệp script, ⛔ đừng nhét chuỗi dài qua shell |

## ⛔ Riêng tư & tiền thật

- `PM_COT_RIENG_TU = {"Email Address"}` — **CẤM** vào kho. `Tên tài khoản` thì **GIỮ** *(owner quyết 11/09)*.
- `sao_luu/` và `hien_vat/` bị `gitignore` **đúng vì chúng mang tên người và tiền thật** — ⛔ đừng gỡ.
- `AS-IS system/Accounting_Files/RAW/` *(repo `FIN-ERP`)* cũng vậy — `.gitignore:13`.
- Công cụ ghi sổ đòi `FLS_CHO_GHI_THAT=1`. `fls_itl` là **chỉ-THÊM** (`INV-I08`).
- ⛔ `Client secret` ⛔ không bao giờ đi qua chat, ⛔ không vào bất kỳ tệp nào của repo.

## Cách viết

Tài liệu và mã ở đây **tiếng Việt**, chú thích dày, và **mỗi câu khẳng định đi kèm một con số đo được**. Giữ đúng giọng ấy — ⛔ đừng viết lại cho "gọn": phần lớn chú thích dài là **bia của một lỗi đã xảy ra**.
