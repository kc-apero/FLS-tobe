# 11 — BỐI CẢNH DỰ ÁN TỪ MEMORY: thứ ba agent phải biết trước khi làm

**Version:** v1.2 · **Ngày:** 2026-10-07 · **Chủ sở hữu:** owner · **Nguồn:** memory phiên AI *(`~/.claude/projects/…/memory/`, ~40 mục chạm FLS/ITL)*, gom theo yêu cầu owner 01/10

> Ba agent `fls-ba` · `fls-dev` · `fls-test` **⛔ không tự đọc được** memory của phiên chính. Tệp này là **bản chép có chọn lọc** để các agent dùng chung. Mỗi mục ghi **ngày đo** — đó là sự thật **tại ngày ấy**; số sống có thể đã trôi ⇒ **đo lại trước khi trích**.
>
> ⛔ Tệp này **⛔ không thay** spec `02_BA`, quyết định ở `00_MASTER_INDEX`, hay `CLAUDE.md`. Nó trả lời câu *"vì sao mọi thứ lại như thế"* — thứ thường **chỉ sống trong đầu phiên trước**.

---

## 1. Người dùng và cách báo cáo

| Điều | Áp thế nào |
|---|---|
| Owner là người **không chuyên kỹ thuật** | Báo cáo cho owner: **kết luận trước** · câu ngắn · **có hình** *(mermaid luồng/kiến trúc)* · chi tiết kỹ thuật để cuối |
| Owner muốn việc xong thì **đẩy lên git** | Xong việc ⇒ commit + push *(trừ `sao_luu/`, `hien_vat/`)* |
| Hiểu **ý nghĩa** module trước khi chuyển đổi | Đọc spec gốc + nguyên lý **trước**; *"khớp số với bản cũ"* là **cổng**, ⛔ không phải mục tiêu |
| Vận hành thật chỉ **2–3 kế toán** *(`QĐ-ITL-27`, 22/08)* | ⛔ đề xuất duyệt hai cấp / leo thang / hậu kiểm chéo — **kiểm soát phải nằm trong máy**: không bịa · xếp việc theo **tiền** + in **tuổi việc** · nhật ký để **việc sống sót khi người rời đi** *(rủi ro số một: một người rời đi, ⛔ gian lận)* |
| FPA = lớp **xem & quyết**; đối soát + ký chốt là nghiệp vụ kế toán | ⛔ nhét nút ký / bút toán kế toán vào lớp báo cáo |

## 2. Kho và môi trường *(bẫy đã cắn)*

| Sự thật | Hệ quả |
|---|---|
| Kho `fls-pg-1` *(PG 16, cổng `5433`, db/user/pass `fls`)* nằm trên **volume VÔ DANH** *(compose ⛔ khai `volumes:`)* | ⛔⛔ `docker compose down` = kho rỗng. Docker Desktop tắt ⇒ bật Docker rồi **`docker start fls-pg-1`** *(đã chứng minh 17/09)*. Sao lưu: `tools/sao_luu_kho.py` + `pg_dump -Fc` |
| Chạy bằng `.venv/Scripts/python.exe` + **`PYTHONUTF8=1`** | `python` trần ⇒ 31 lỗi thu bài *(thiếu `psycopg`)*; thiếu UTF-8 ⇒ `UnicodeEncodeError` vì đầu ra mang `⛔ ⭐ ⚠` |
| Bộ test **từng ghi thẳng vào kho thật** *(27/08: 1.204 dòng bịa trong sổ)* | Ba tầng chặn: `dsn_test()` **nổ** nếu trỏ kho thật · `noi_chi_doc()` · bài quét mã `test_khong_ai_tro_lai_kho_that.py`. Luật: **bản TRẮNG** *(thật ⇔ `run_id` khớp `NAP-yyyy-mm-dd-NGUỒN`)* |
| Kho test **phình mãi** *(03/09: 24.593 dòng rác `NAP-2000-%`)* | Bài `*_pg` đỏ vì quá `timeout` ⇒ đo `doc_cong` trước; dọn **có mục tiêu**, ⛔ `TRUNCATE`, ⛔ nới timeout |
| `hien_vat/` và `sao_luu/` bị gitignore *(mang tên người + tiền thật)* | **Vô hình với git** ⇒ trước khi dựng gì mới: `ls hien_vat/` + `ls tools/`. `FLS-Design-P6.html` = **hình dạng**, `FLS-Demo-Dong.html` = **hành vi** |
| Mở tệp chế độ ghi là **xoá ngay** | Lỗi ở `.write()` để lại tệp 0 byte ⇒ ghi ra tệp tạm → kiểm → chép đè |
| Sửa tệp qua `python -c` / heredoc đi **hai lớp shell** | `\n`, backtick, `\uXXXX` bị dịch lần nữa ⇒ **viết kịch bản ra tệp** rồi chạy. `str.replace` mẫu ⛔ tồn tại thì **im lặng** ⇒ `assert cu in t` cho mọi phép thay |

## 3. Nguồn dữ liệu — cái nào tin được

| Nguồn | Trạng thái |
|---|---|
| ⭐ Bản sao RAW **sống** `1md85t5…` ▸ `Transaction Mapping L1` | Nguồn `ITL-CANON` **chính thức** *(`QĐ-ITL-50`, owner 26/08)*. Dữ liệu bắt đầu **dòng 5** *(header dòng 3, dòng 4 trống)*. Đứt nguồn thì **giữ `#N/A`** ⇒ nói thật |
| Sổ FLS từ **10/09** nạp từ tầng **`R \| <tài khoản>`** *(⛔ tầng `Mapping L1` phái sinh)* | ⛔ nạp lại `Mapping L1` *(cổng `A5a`: một tầng nguồn)*. **1.919 dòng** của 8 sheet đã xoá bị **bỏ có chủ ý** *(owner: "cứ lấy đúng hiện trạng")* — chỉ còn trong `sao_luu/` |
| `ITL Ledge` *(ADJUSTED `1r4Wem…`)* | ⚠ Đứt nguồn ⇒ `iferror` ⇒ cờ `Input here` ⇒ **gán MẶC ĐỊNH im lặng** *(`OGA \| GAC - Other`, `SHQ2 \| Headquarters2`, `VD0`…)*. **6.843** ô `Input here` là **số lần đã dùng mặc định**, ⛔ "việc còn phải làm". `Final` **ưu tiên `Classifying`** — gõ tay bị bỏ qua nếu nguồn có giá trị |
| Bản xuất `.xlsx` của ITL | ⛔⛔ **ĐỪNG dùng cho giá trị**: hoán ngày↔tháng **42%**, ngày thành chuỗi **55%**, chỉ **2,7%** nguyên vẹn; ~84 dòng mới nhất **mất mã** `ITL#`. Đọc được **hình dạng**, ⛔ giá trị |
| `A-CCR_V2_Working` `1axCTQ8…` | Là **bản chụp** *(dừng 19/08)* nhưng **trông như sống** — cột ngày dựng sẵn tới 10/2026 và chuyển tiếp giá trị hôm trước. Hỏi **tuổi bằng sổ giao dịch** *(`tools/do_trong_tai.py`)*, ⛔ bằng bảng tổng hợp |
| Đọc Sheets | SA `claude-code-access@fpa-t-494007` qua `gcloud auth print-access-token`. Tên tab phải **tra từ bảng tính** — tab sai tên trả 400/500/503 lẫn lộn, dễ tưởng Google quá tải |

## 4. Nghiệp vụ ghép PM ↔ tiền *(trục tác vụ ①)*

- Logic AS-IS: `Transaction Mapping L1` là **`VLOOKUP` một tầng** khoá `Số chứng từ` ↔ `PM_Unpivot!Z` *(`Reference number`)*. **`HDCode` và `CDT1` — hai trường quyết định P&L — đến TỪ PM**, ⛔ từ `Mapping Master`.
- `33,8%` ghép được **gần kịch trần**, ⛔ "phép ghép hỏng": phần lớn tiền ra không có lệnh là **vốn ⛔ cần lệnh** *(lãi/phí bank, điều chuyển nội bộ, nền tảng — 92% tiền nhóm này)*. **50 dòng lớn nhất gánh 89,3% tiền** ⇒ việc thật ~50 dòng, ⛔ 6.843.
- `fls_pm_line` là **ẢNH CHỤP một lần nạp** *(`run_id` trong khoá chính)*: nạp lại = **thêm ảnh**, ⛔ `DO UPDATE`; cửa đọc **trả tuổi ảnh**; `amount` trong ảnh ⛔ là căn cứ — lúc ghép Σ so với tiền bank **thật**.
- Ứng viên xếp **4 bậc có tên** *(`ma` › `tien` › `gan_tien` › `cung_tien_te`)*, ⛔ điểm mờ. Thân `/match` là **`{pm_line_ids}`** *(`CR#6`: 526 phiếu mang 2–36 reference ⇒ ghép theo phiếu là máy quyết thay người)*.
- Ghép = **THÊM** `fls_pm_link` + `fls_queue_event` + bút toán `hd`/`cdt1` *(một giao dịch)*. `hd`/`cdt1` chỉ suy khi **cả N dòng đồng ý**; lệch ⇒ `khong_suy_duoc`. ⚠ **UAT 01/10 xác nhận:** một cú Ghép **tự điền 2 ô** `cdt1` + `hd` nhân danh người bấm; Bỏ ghép **đảo** cả hai *(`itl_id 27728`, `reason` "UAT 01/10…")* — kế toán phải được báo trước. ⭐ **Owner 01/10 *(`QĐ-ITL-149`)*: hai ô ấy là "Máy gợi ý"**, ⛔ người chốt ⇒ sau `WO-003` chúng vào `fls_may_goi_y` *(`nguon='may_goi_y'`)*, **Final ⛔ đổi**, cổng `C8` ⛔ đếm. Và cú Ghép/Bỏ ghép **⛔ còn bắt buộc lý do** *(owner: "bỏ yêu cầu lý do cho cú Ghép")* — thiếu thì máy điền lý do mặc định có nhãn `(may dien)`.
- ✅ ~~`GAP-CR1-04`: dung sai `1.000 VND` tuyệt đối quá rộng cho ghép tay~~ — **ĐÓNG 28/08** *(`QĐ-ITL-63`)*: ghép **tay** đòi **≤ 1.000 đ VÀ ≤ 0,5%** tiền bank, lấy cái nhỏ hơn *(mã `pm_join.py` `TY_LE_GHEP_TAY = Decimal("0.005")`; ghi v1.0 chép từ trí nhớ đã cũ — `R-13`)*.
- **Hai con số đừng gọi lẫn:** *dòng sổ đã ghép* ≠ *số mối nối* *(hình `B`: một dòng bank trả N dòng lệnh)*.

## 5. Ngày tháng *(lớp lỗi đắt nhất của ITL)*

- Hoán ngày↔tháng **~181 tỷ sai kỳ** là **chặn dưới đã lạc hậu**; xảy ra khi import qua locale, ô vẫn là ngày **hợp lệ nhưng sai** ⇒ không có lỗi nào để bắt.
- Ở FLS: **29/60 nguồn** chuỗi ngày là **`mdy`** *(OCBC Singapore, TCB USD — sao kê nước ngoài)*, **0** nguồn `dmy` *(`QĐ-ITL-113/117`)*. ⛔ Mặc định `dmy` "vì Việt Nam" = hoán 1.894 dòng.
- Khoá nối mang **ngày** ⇒ kế toán sửa ngày là mất dòng **im lặng** *(FPA: 748 dòng / 16.789 mVND)*. ⛔ Đưa ngày vào khoá định danh.
- `itl_id` AS-IS = **số thứ tự sau `SORT` theo ngày** ⇒ chèn một giao dịch lùi ngày là **đánh số lại cả phía sau**. FLS cấp `itl_id` **khi vào sổ rồi đóng băng** *(`QĐ-ITL-30`)*. ⛔ Có cầu khoá AS-IS ↔ FLS ⇒ đối soát di trú đi **theo nội dung** *(`GAP-DITRU-01`)*.
- Ngày **cuối** của một bản trích là **số TẠM** *(trích lại phình +7,7% vì tiền về muộn)*.

## 6. Luật đo — các lỗi phương pháp đã xảy ra *(bổ sung `Đ1`–`Đ5` của `CLAUDE.md`)*

| Lỗi | Luật |
|---|---|
| Cổng lọc `IS NOT NULL` **trên chính cột nó canh** — xanh 2 tháng trên 28 vi phạm | Cổng ⛔ được lọc bỏ đúng thứ nó phải bắt |
| Báo động chạm **76,6%** sổ | **Đếm** số dòng bị chạm trước khi bật báo; báo động chỉ đáng giá bằng **độ hiếm** |
| Khai cái mới theo suy luận, sai **3 lần/1 ngày** | **Đo cái đang chạy** trước khi khai cái thay nó |
| Dựng lại SQL bằng tay ra **2/35** thay vì **18/35** | Đo một **quan hệ** thì **gọi chính hàm thật** |
| *"Một cú bấm dọn được bao nhiêu"* ra **584** thay vì **68** | Đo theo luật **cửa GHI**, ⛔ cửa ĐỌC |
| Trường có trong **kiểu**, rỗng trong **dữ liệu** *(20/20 = 0)* — qua `tsc` xanh | Kiểm **giá trị thật**, ⛔ chỉ kiểu |
| Khuôn thử **tự nhét state** ⇒ che chỗ bản thật **⛔ bao giờ gọi cửa** *(màn `B3`)* — ⭐ **lặp lại 3 lần trong đợt ba agent** *(`KQ-019` · `KQ-029` · `KQ-031`, 01→02/10: màn đọc khoá mà cửa ⛔ trả, bài thử vẫn xanh vì tự đút sẵn thân)* | Bài thử màn phải chứng minh màn **tự đi lấy** dữ liệu. ⭐ Từ `WO-032` *(02/10)* mọi `WO` có màn **bắt buộc** AC *"thân từ **cửa thật** *(kho TEST)* + **Chrome chuột thật**"* — `KQ-041` · `KQ-046` · `KQ-050` · `KQ-061` đều đo theo luật ấy |
| Agent soạn **một khối văn bản dài một lần** ⇒ watchdog **600 s** giết lượt *(**2** lượt treo trong đợt `01→07/10`)* | Viết tệp **từng phần nhỏ** *(tạo khung rồi điền từng mục; sửa bằng kịch bản ra tệp — §2)*; một lượt ⛔ ôm cả tài liệu dài |
| Ngân sách *"≤ N lượt hỏi kho"* xanh ở 3 lượt khi thật **126 lượt / 67,7s** | Đo **đồng hồ**, ⛔ số lượt |
| Lọc **một vế** của phép so *(thực tế bị cắt, kế hoạch ⛔)* | Lọc thì lọc **cả hai vế**; dấu hiệu: nửa biểu đồ bẹp sát đáy |
| Suy chỉ số từ **một dòng**; trung bình trên **hai nhóm trộn** | Kiểm phân bố trước khi báo "bất thường" |
| Bộ tài liệu **già trong im lặng** *(20 số lệch sau 19 giờ; 8 lớp lệch)* | Số sống **một chỗ ghi**, chỗ khác **trỏ tới**; cổng `kiem_so_song` canh **số**, ⛔ canh **câu** ⇒ số đúng cạnh câu sai vẫn xanh. Phân biệt **khai** với **biên bản** *(số cũ trong changelog là ĐÚNG)* |

## 7. Trạng thái tại 07/10 *(`fls-ba` đo trong lượt — đo lại trước khi dùng)*

| | |
|---|---|
| Nhánh | `feat/p2-oracle-parity` @ `6b4aa2d` *(commit 06/10 11:25)* = `origin/feat/p2-oracle-parity`; **266** commit chưa vào `origin/main` *(`git rev-list --count origin/main..HEAD` 07/10)*, chưa có PR |
| Đợt ba agent `01→07/10` | **99** commit *(01/10 **15** · 02/10 **42** · 05/10 **35** · 06/10 **7**)* · **64** phiếu *(WO **16** · BG **23** · KQ **15** · HOI **10**)* · **11** `WO` đóng qua `KQ` ĐẠT + nghiệm thu PO: `WO-001` · `003` · `008` · `011` · `018` · `022` · `023` · `032` · `037` · `042` · `045` |
| ⭐ Hai đường ghi sai | **Chứng minh** trên kho TEST *(mã cũ, cửa ghi trả `200`)* rồi **chặn** ở mã mới: `KQ-050` *(đổi lệnh khi ứng viên đang tải — `WO-045`)* · `KQ-061` *(chọn hàng khi lượt tìm đang bay — `WO-023 (i)`)*. ⇒ **Cặp sai trong dung sai lọt cửa ghi; màn là chốt chặn duy nhất** |
| Sổ | ⛔ **0** dòng ghi suốt đợt: `fls_itl` **8.387** · `fls_pm_link` **2.263** *(2.262 từ 10/09 + 1 UAT 01/10)* · `fls_pm_unlink` **1** · `fls_adjustment` / `fls_journal` **4.428** · `fls_queue_event` **110.349**; thời điểm ghi mới nhất cả năm bảng = `2026-10-01 09:06 UTC` *(cú UAT)* |
| Người thật | **0** ⇒ mốc `B` máy đếm **`1 · 1 · 3`** *(thước sửa ở `WO-001`/`WO-011`)* · actor ngoài sổ **0** |
| Nhịp chụp | `fls_chup` **182** ảnh; mới nhất **07/10 11:02** *(giờ VN)*; ảnh lệnh **322.143** dòng — vẫn chỉ khi máy bật |
| Cổng 07/10 | `pytest` **2.428 passed, 2 xfailed** *(`BG-064` ×2; máy thu **2.430** bài)* · `kiem_tai_lieu` ĐẠT · `khop_owner --kiem` **17/20** khớp ĐẠT · ⛔ `kiem_so_song` **79** lệch *(số trôi + phiếu — `dong_bo --ghi` là việc `fls-dev`)* |
| Máy xem | `8088` **chỉ đọc** trên `6b4aa2d` *(trang 2 `VND` **0,3 s** — phiên chính đo)* |
| Phiếu | `WO-051` `CHO_TEST` *(`BG-064`)* · `HOI-063` `MO` chờ `fls-ba` · hàng chờ `WO-062` **CAO** *(trước buổi `C1`)* → `WO-060` → `WO-047` → `WO-015` — bảng sống ở `handoff/README.md`, thứ tự ở dashboard §6 `6.-20` |
| Chờ owner | `Q-FX-1` · `Q-TIEN-1` · xoá ô `F02` ⇒ Final trống hay sổ gốc · hẹn buổi `C1` · **52** dòng số TK đầy đủ trong git *(che từ nay hay viết lại lịch sử; repo riêng tư hay công khai)* · `GAP-SCR-33` · `GAP-SCR-26` · ⏸ danh mục tài khoản + người dùng *(hoãn 02/10)* |

## 7a. Trạng thái tại 01/10 *(biên bản — đo trong phiên chính 01/10; ⛔ dùng làm hiện trạng)*

| | |
|---|---|
| Nhánh | `feat/p2-oracle-parity` — **169 commit** chưa vào `origin/main` *(đo 01/10 tối tại `1bdcff8`; ⚠ `main` cục bộ già hơn)*, chưa có PR. PR #1, #2 đã gộp |
| Hoạt động mã/tài liệu cuối | 23/09 *(màn ghép `SCR-F01`: 4 vòng góp ý owner, 13 điều, 6 GAP đóng)*; 01/10: ba agent + hợp đồng (`10`) + tệp này · `WO-001` + `KQ-002` · ⭐ owner trả 4 câu ⇒ `QĐ-ITL-149`/`150`, phát `WO-003` |
| Nhịp chụp | Chạy **chỉ khi máy bật** — ngày có ảnh `actor='nhip@fls'`: **09, 10, 15, 18, 19, 23, 25, 28/09 và 01/10** *(⚠ v1.0 ghi "chỉ 23, 25, 28/09 và 01/10" — đúng **từ 20/09**, `KQ-002 F-8`)*. Ảnh **mới nhất** *(đo 01/10 tối)*: Bank **17:20**, PM **16:21** — nhịp vẫn chạy nên con số này **trôi theo giờ**. Ảnh 15:20: Bank 8.923 dòng / 64 nguồn *(12 nguồn 0 dòng)*, PM 3.820 dòng |
| Sổ | `fls_itl` **8.387** · `fls_pm_link` **2.263** *(2.262 từ lần dựng 10/09 + 1 cú UAT 01/10)* · `fls_pm_unlink` **1** *(UAT)* |
| Người thật | **0** thao tác của kế toán thật. Hai thao tác duy nhất ngoài máy là cú UAT ghép/bỏ ghép `27728` của owner 01/10 ⇒ ⭐ **owner chốt *(`QĐ-ITL-150 ⓐ`)*: UAT ⛔ tính là người thật** cho mốc `B` hay bất kỳ cổng *"người đã làm"* nào *(`09:339`/`:347` "kế toán (hoặc owner)" — nay thua câu này; `R-12`)* |
| Cổng 01/10 | `pytest` **1.903** xanh *(trước bài nghiệm thu; sau `KQ-002`: **1.905 passed, 6 xfailed**)* · `kiem_tai_lieu` ĐẠT — **92 tệp** *(đo 01/10 tối; v1.0 ghi "87" — trôi theo số tệp mới, `F-8`)* · ⛔ `kiem_so_song` **47 → 55** nhóm lệch trong cùng ngày *(38 số trôi theo ảnh · 8 UAT · còn lại số tệp/phép thử mới — `Ra-soat` §1.1)* · `khop_owner --kiem` **15/19 khớp — ĐÚNG MONG**: bốn mục `A2`·`B5`·`B6`·`C5` khai `mong=False` *(lệch **có chủ ý**)*; cổng đỏ **chỉ vì** khối sinh máy `SINH-KHOP` trong lộ trình audit lệch **3** dòng *(⚠ v1.0 đọc như "bốn lỗi" — `R-4`)* |
| Chờ owner | chip `Tất cả` *(`GAP-SCR-26`)* · khôi phục hai bản dựng `_9`/`v2` bị xoá ở `fe403ce` · đổi kho sang volume có tên · ⭐ mới: mở lằn **GIÁ TRỊ** *(màn hiện gợi ý `hd`/`cdt1` + nút gật — `GAP-SCR-33`)*. ✅ ~~`QĐ-ITL-116` giữ đích `A-CCR` hay chĩa sang ITL adjust~~ — **đã trả 09/09**: `QĐ-ITL-120` *(đích BigQuery)* + `QĐ-ITL-123` *(hoãn BQ)* — `R-14` |
| Phiếu | `WO-003` *(sẵn sàng, làm TRƯỚC)* → `WO-001` *(sẵn sàng, `T5` `dong_bo --ghi` sau cùng)* · `KQ-002` mở *(chờ `BG`)* — bảng sống ở `handoff/README.md` |

## Changelog
- v1.2 (2026-10-07, `fls-ba` — owner: *"cập nhật tài liệu dự án về tiến độ và hiện trạng"*): §7 **trạng thái 07/10** đo lại trong lượt *(git `6b4aa2d` · kho thật chỉ `SELECT` · cổng 07/10)*; bảng 01/10 giữ nguyên thành **§7a** biên bản. §6: hàng *"khuôn thử tự nhét state"* ghi lặp **3** lần trong đợt *(`KQ-019` · `KQ-029` · `KQ-031`)* + luật AC *"cửa thật + Chrome chuột thật"*; thêm hàng **watchdog 600 s** *(2 lượt treo ⇒ viết từng phần nhỏ)*.
- v1.1 (2026-10-01, `fls-ba`): §4 ghi lời owner *(`QĐ-ITL-149`: `hd`/`cdt1` khi ghép = **máy gợi ý**; cú Ghép ⛔ bắt buộc lý do)* + đính chính `GAP-CR1-04` **đã đóng 28/08** *(`R-13`)*; §7 sửa nhịp chụp, ảnh mới nhất, số tệp *(`KQ-002 F-8`)*, đọc lại `khop_owner` 15/19 là **đúng mong** *(`R-4`)*, UAT ⛔ tính người *(`QĐ-ITL-150 ⓐ`, `R-12`)*, bỏ câu chờ owner `QĐ-ITL-116` đã có trả lời *(`R-14`)*, thêm dòng *Phiếu*. Số đo §7 lấy **01/10 tối** — đo lại trước khi trích.
- v1.0 (2026-10-01): Khởi tạo — chép có chọn lọc ~40 mục memory chạm FLS/ITL cho ba agent `fls-ba`/`fls-dev`/`fls-test`.
