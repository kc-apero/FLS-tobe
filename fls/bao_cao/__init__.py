"""`fls.bao_cao` — tầng **ENGINE BÁO CÁO / PHÂN BỔ THUẦN** *(AP Voi FLS v3.1.2 · WP-C2…C5)*.

Vai: hàm thuần từ dòng sổ + config đã ký ra số báo cáo — `CA.GL` *(Nợ/Có × tiền tệ → bVND ·
mUSD)* · `SO.CFA1/3` · `SO.PLA1/3` · `AL.PLT` · `AL.KEY` · `SO.PLA3-ATL` · `RP.CF/PL`; mỗi
engine có cổng parity với đáp án NOW *(HD2)*. Chủ làn: **BE-HC** *(ISP 3.1.2 §2.1)*.

⛔⛔ **Vì sao tầng này ⛔ được biết kho** *(`.importlinter` hợp đồng 11 — cấm `psycopg`,
`fls.repo`, `fls.db`)*. Một engine báo cáo mà tự đọc được kho thì nó tự **đi lấy số** — và
khi ấy cổng parity ⛔ còn chứng minh được *"cùng đầu vào ⇒ cùng con số"*: hai lần chạy có thể
nhìn hai tập dữ liệu khác nhau mà ⛔ ai thấy. ⇒ Dòng sổ và config được **TRUYỀN VÀO**, giống
hệt `fls.ledger` *(hàm thuần — hợp đồng 4)* và `fls.xuat` *(số phải được truyền vào — hợp
đồng 9)*.

⭐ Gói ra đời **rỗng** ở bước `S0` *(WO-065)*, cùng hợp đồng tầng của nó, để hai làn BE
⛔ phải cùng sửa `.importlinter` về sau *(tệp dùng chung, tuần tự hoá về `S0`)*.
"""
