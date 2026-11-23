# KQ-349 — R1 vòng 2 `WO-338` / `BG-339` *(ISP 3.1.2 · HELD — bể giữ riêng, sau vòng sửa `KQ-340`)*

| | |
|---|---|
| **Kết quả** | **ĐẠT — 0 CHẶN · 0 NÊN SỬA · 3 GHI NHẬN** ⇒ **sẵn sàng R2 cuối** |
| **Phát phiếu** | `fls-test` · 2026-11-23 · `isp/HELD` ngọn `f015cbf` · cây gộp thử = `origin/claude/bold-galileo-zukpaf` `577044e` *(main `c5ea872` + AG `8a1eca4` + `TIEN_DO`)* + `f015cbf` · cụm PG 16 cổng 5446 |
| **Sổ** | `docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_HELD.md` *(`HELD-R1v2-01…03`; `HELD-R1-01…06` ⇒ đã sửa)* |
| **Gửi** | `ORCHESTRATOR` ⇒ R2 cuối *(đặt sàn 4.997 ở lúc gộp — xem `HELD-R1v2-02`)* |

⚠ Bể dựng lại từ SA chỉ-đọc ở **thư mục NGOÀI repo**, **đã xoá** sau đo; ở đây chỉ số đếm, ⛔ nội dung.

## Bảng kiểm
| # | Kiểm | Đo được *(nhãn · mẫu số)* | Kết |
|---|---|---|---|
| 1 | `HELD-R1-01` gộp AG | `2db1f22` là tổ tiên của `f015cbf` · marker xung đột trong `fls tools tests docs/ITL/_tools` **0** · `git grep cho_noi_dung tools/fleet_eval_voi.py` **0** · `git diff 2db1f22 f015cbf -- fls/agent` **0 dòng** *(⛔ sửa mã AG)* · `tests/agent` + `test_dung_moi_truong_isp` **170 passed** *(không bể)* · `test_be_giu_rieng` **39 passed** *(có bể)* · `che_do` `mo`/`che_noi_dung`/`che_het` đúng API: `chay_skill(…, che_do=)` + `cav.chay("gia", che_do, ncc=)` | ĐẠT |
| 2 | `HELD-R1-02` ca bể mang `tk` | dựng lại từ SA: ca có `tk` khác rỗng **A 65/65 · B 70/70** *(R1: 0/65)*. Chuỗi 4 agent chế độ `mo`: ô khớp / mẫu số **A 631/631 · B 631/631** · lệch 0 · `KHONG_DO_DUOC` 0 · `dung_o` rỗng ⇒ ⛔ `KeyError`; `che_het` cùng số. `fleet_eval_voi --be-giu-rieng` đúng như `BG-339` *(`mo` A nối 2/sai 2 · B nối 2/sai 1; `che_noi_dung` bị `CamGui` 10 / 14 chỗ; exit 1 vì CHẶN — đúng mong)* | ĐẠT |
| 3 | NÊN SỬA `-03…-06` | `-03` tên bài cũ trong `tests/` **0**; bài mới tồn tại, xanh. `-04` `do_duoc_theo_loai` có · `-05` muối dẫn xuất từ bí mật ⇒ `test_BE_van_tay_khop_tep_dem_repo` **xanh trên bể dựng lại** *(R1: đỏ)*. `-06` vòng chính qua `chay_skill`. **Đột biến 3 trên bản sao `git archive` (trả nguyên)**: gỡ `tk` khỏi ca ⇒ **4 đỏ** · `do_duoc_theo_loai` luôn `True` ⇒ **3 đỏ** · muối luôn ngẫu nhiên ⇒ **1 đỏ** · 3/3 cắn | ĐẠT |
| 4 | Riêng tư repo | `git log -p 9840f27..f015cbf` **43 commit · 7.557 dòng thêm**: dãy ≥ 8 số trần **15** = 12 `tk` bịa dạng `1903000000001`/`0071000000002` *(cả bài lẫn fixture, ⛔ TK thật)* + 3 chuỗi vân tay/bịa **đã không còn ở `f015cbf`** *(`git grep` = 0)* · mã `FT`/`IBDN` + ≥ 6 số **0** · email **1 địa chỉ thật** ⇒ `HELD-R1v2-01` *(không do HELD, đã có ở nền)* · muối: `muoi.key` ngoài repo, `git ls-files` khớp `muoi`/`.key` **0** · `quet_pii_repo` **0 chỗ · 0 tệp** *(cả cây HELD lẫn cây gộp)* | ĐẠT + `-01` |
| 5 | Cây gộp thử | gộp: **2 xung đột, chỉ hai dòng sàn** *(`dung_moi_truong_isp.sh:420` · `test_dung_moi_truong_isp.py:423`)*; giải bằng thu thập thật `pytest --collect-only` = **4.997** *(0 lỗi thu thập)*, web **690**. `--duong-nen --cong 5446` MỘT lần, một mình: **`KẾT: ĐẠT`** — toàn bộ **28 = 28** node id *(XFAIL 2 = 2 · thêm 0 · bớt 0)* · chạy **4.997 ≥ 4.997** · skipped 0 · deselected 0 · `12 failed, 4969 passed, 2 xfailed, 14 errors` · web **3 = 3** · chạy **690 ≥ 690** · `test_dung_moi_truong_isp` **60 passed** · `kiem_tai_lieu` **ĐẠT** *(512 tệp · 3.042 bảng)* · `lint-imports` **11 kept, 0 broken** · `quet_pii_repo` **0** | ĐẠT |

## Phát hiện mới *(chỉ GHI NHẬN)*
| Mã | Mức | Nội dung |
|---|---|---|
| `HELD-R1v2-01` | GHI NHẬN | Chuỗi email thật của chủ nằm ở `tests/oracle/test_do_hd2_c5c.py` *(ca đột biến email)* + sổ H14 — đi vào `9840f27..f015cbf` **qua gộp nền AG/H14** *(commit gốc `a59f4b9`, đã là tổ tiên của nhánh làm việc; đã ghi ở `H14-R2b2-01`)*. HELD **không thêm**; `quet_pii_repo` chỉ quét số TK ⇒ ⛔ thấy. Việc của chủ nhánh H14/orchestrator, ⛔ chặn HELD |
| `HELD-R1v2-02` | GHI NHẬN | Sàn khi gộp: HELD đặt **4.967** ≠ thu thập thật cây gộp **4.997**; ngọn nhánh làm việc đã nhích `4958` ⇒ gộp thật sẽ xung đột đúng hai dòng sàn. Giải = số thu thập thật **lúc gộp** + bài ghim cùng commit *(Q8)*; **0** xung đột khác |
| `HELD-R1v2-03` | GHI NHẬN | Quyết chủ còn treo, ⛔ lỗi mã: `che_noi_dung` vẫn bị `CamGui` chặn *(A 10 · B 14 chỗ)*, bộ che lọt số TK **17/65 · 24/70** *(A/B, dãy ≥ 8 số, dò `do_ro_ri_che`)*; luật giả `luat_gia_v1` ⇒ `mo` ≡ `che_het` ⇒ bể **chưa đo được** lợi ích đọc nội dung/TK *(cần mô hình thật, ngoài WO-338)*. `-07…-10` R1 giữ backlog, lý do khớp |

## Chưa chạy *(nói thẳng)*
`tools/kiem_so_song.py` · `dong_bo_so_song.py --ghi` *(đường `.venv/Scripts/` Windows cứng)* · `khop_owner.py --kiem` *(nền đã đỏ từ R0)* · `soi_bang_tuyen` · `kiem_thuyet_minh` ⇒ ngoài phạm vi vòng 2 theo prompt. `pip install google-auth requests` vào `.venv` của phiên để đọc SA *(không đổi repo)*.

## Kết luận
**ĐẠT · 0 CHẶN · 0 NÊN SỬA** ⇒ **sẵn sàng R2 cuối**. SHA kiểm: `isp/HELD` `f015cbf`; cây gộp thử `577044e` + `f015cbf` *(không commit)*.
