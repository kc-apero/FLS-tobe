"""`fls.cau_hinh` — tầng **CONFIG THUẦN** của lõi config chung *(AP Voi FLS v3.1.2 · WP-C1)*.

Vai: nạp + kiểm các bảng config `IX.*` *(`IX.FX` tỷ giá · `IX.HD` cây HD · `IX.ORG` ·
`IX.PER` lịch kỳ · `IX.VEN` · `IX.DRV` · `IX.ALR` · `IX.PL` · `IX.TMP`)* thành giá trị
Python có kiểu, kèm lý do CÓ TÊN khi một dòng config sai. Chủ làn: **BE-CF** *(ISP 3.1.2 §2.1)*.

⛔⛔ **Vì sao tầng này ⛔ được biết kho** *(`.importlinter` hợp đồng 10 — cấm `psycopg`,
`fls.repo`, `fls.db`)*. Config là thứ **mọi** engine đọc *(`fls.bao_cao` phân bổ theo nó, cửa
`GET /config/*` trả nó ra)*. Một bộ kiểm config mà tự mở được kết nối thì nó tự chọn được
**đọc bản nào** — và lúc đó ⛔ còn chỗ nào bảo đảm *"engine và màn hình nhìn CÙNG một bản
config đã ký"*. ⇒ Bản config được **TRUYỀN VÀO**; đọc/ghi kho config chỉ-thêm là việc của
`fls/repo/cau_hinh_repo.py` *(đúng khuôn `fls.api`: kết nối truyền vào — hợp đồng 7)*.

⭐ Gói ra đời **rỗng** ở bước `S0` *(WO-065)*, cùng hợp đồng tầng của nó, để hai làn BE
⛔ phải cùng sửa `.importlinter` về sau *(tệp dùng chung, tuần tự hoá về `S0`)*.
"""
