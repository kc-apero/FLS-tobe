# -*- coding: utf-8 -*-
"""§1 EntityRelationshipDescription — FLS kho 7 tầng."""
from apgen import *
import os

SCRATCH = os.path.dirname(os.path.abspath(__file__))

def svg7():
    return open(os.path.join(SCRATCH, "erd7tang_static.svg"), encoding="utf-8").read()

def sections():
    out = []
    out.append(S("s1", "§1 EntityRelationshipDescription — kho 7 tầng, 18 bảng + 5 view", st="draft", part="PART A · KIẾN TRÚC CHUẨN — ERD · PROCESS · USERFLOWS", body=
        P("Kho là <b>một</b> PostgreSQL 16 (Docker <code>fls-pg-1</code>, cổng 5433), schema khai <b>một lần</b> bằng <code>Table/Column</code> trong <code>fls/db/schema.py</code> (814 dòng), sinh ra DDL, ERD JSON/Mermaid và bản đồ 7 tầng; migration là <i>đường đi</i> (22 tệp forward-only, checksum), schema là <i>trạng thái mong đợi</i>, <code>pg_verify</code> nối hai bên. Ba cổng <code>G-ERD-1/2/3</code> giữ cho ERD trong tài liệu BA không lệch mã. Mọi con số mục này là [CODE 17/09].")
    ))

    out.append(S("s1-1", "§1.1 Mô hình 7 tầng &amp; bản đồ thực thể", body=
        P("<code>tang</code> là <b>cách đọc</b>, không đổi một dòng DDL: mỗi bảng khai mình thuộc tầng nào, công cụ <code>tools/sinh_ban_do_tang.py</code> sinh ba hiện vật từ cùng bản khai (Mermaid <code>ERD-TANG.mmd</code>, khối mermaid trong BA-05, SVG dưới đây) và 16 bài test canh chúng khớp. Mũi tên = khoá ngoại thật (23); <b>đỏ</b> = trỏ xuống tầng lớn hơn hoặc tự tham chiếu — hai chỗ đáng nhìn nhất.")
        + '<div class="erd-wrap">' + svg7() + '</div>'
        + '<p class="fig-cap"><strong>Hình 1.1</strong> — Bản đồ kiến trúc kho FLS theo 7 tầng (SVG sinh từ <code>schema.py</code>, commit <code>bfeb1a7</code>; tái dùng nguyên hình, chỉ đổi biến màu sang bảng màu tài liệu). Nét đứt = khung xem (view).</p>'
        + T([("#", 4), ("Tầng", 16), ("Câu tầng trả lời", 24), ("Luật của tầng", 24), ("Bảng thật", 22), ("View", 10)], [
            ["①", "<code>1-anh</code> ẢNH CHỤP", "tờ giấy lúc ấy ghi gì", "chỉ-THÊM, không ai sửa một tấm ảnh", "<code>fls_source</code> · <code>fls_khai_cot</code> · <code>fls_nguon_dai</code> · <code>fls_chup</code> · <code>fls_chup_nguon</code> · <code>fls_chup_dong</code>", "—"],
            ["②", "<code>2-nap</code> NẠP", "dòng nào vào sổ, dòng nào BỊ LOẠI và vì sao", "phần bị loại phải lưu lại kèm lý do có tên (<code>ACC-4</code>)", "<code>fls_run</code> · <code>fls_reject</code>", "—"],
            ["③", "<code>3-so</code> SỔ KẾ TOÁN", "sổ", "append-only (<code>INV-I08</code>); hai danh mục nó tra tới", "<code>fls_itl</code> · <code>fls_le</code> · <code>fls_mapping_master</code>", "—"],
            ["④", "<code>4-ghep</code> GHÉP LỆNH CHI", "dòng tiền này chi theo lệnh nào", "bỏ ghép là THÊM một dòng", "<code>fls_pm_line</code> · <code>fls_pm_link</code> · <code>fls_pm_unlink</code>", "<code>fls_moi_noi</code>"],
            ["⑤", "<code>5-viec</code> VIỆC CỦA NGƯỜI", "người còn phải làm gì", "tầng duy nhất mô tả NGƯỜI; chỉ treo vào <code>itl_id</code>", "<code>fls_queue_event</code>", "<code>fls_queue_state</code> · <code>fls_queue_reason_weekly</code> · <code>fls_da_xong</code>"],
            ["⑥", "<code>6-sua</code> SỬA &amp; VẾT", "ai đã gõ gì, lúc nào, vì sao", "nhật ký 7 trường, chỉ-THÊM", "<code>fls_adjustment</code> · <code>fls_journal</code>", "<code>fls_sua_tay</code>"],
            ["⑦", "<code>7-ha-tang</code> HẠ TẦNG", "sổ di trú", "bootstrap trước migration 0001", "<code>fls_migration</code>", "—"],
        ])
        + P("<b>Hai đảo có tên</b> (<code>ERD_ISLANDS</code>): <code>fls_mapping_master</code> (tra theo giá trị <code>hd</code>, không FK vì <code>hd</code> có thể UNMAPPED) và <code>fls_migration</code> (hạ tầng). Mọi bảng khác tới được <code>fls_itl</code> qua FK vô hướng; <code>fls_source</code> tới bằng <b>đúng hai</b> đường (qua <code>fls_run.khai_id</code> và qua ảnh chụp) — cổng <code>G-ERD-3</code> kiểm cả chiều ngược: khai đảo mà nối được ⇒ đỏ.")
    ))

    out.append(S("s1-2", f"§1.2 Tầng ① ② — Ảnh chụp · Bản khai · Nạp {BUILT}", body=
        T([("Bảng", 16), ("Khoá", 22), ("Cột đáng nhớ", 36), ("Vì sao có / luật", 26)], [
            ["<code>fls_source</code>", "PK <code>source_id</code> (seq) · UQ <code>source_key</code>", "<code>source_key</code> <code>'R | HoangACB'</code> / <code>'file>sheet'</code> · <code>src_type</code> Bank|Cash|CCR|Platform|Mapping · <code>last_seen_at, lag_days, cutoff_date, txn_count</code>", "một nguồn = một <b>dòng chảy</b> có một bố cục cột (7 quỹ đổ vào 2 dòng chảy); thôi là đảo từ CR#11"],
            ["<code>fls_khai_cot</code>", "PK <code>khai_id</code> · FK <code>source_id</code> · UQ <code>(source_id, version, truong)</code> · CHECK <code>thu_tu IS NULL OR (truong='Date' AND thu_tu IN ('dmy','mdy'))</code>", "<code>truong</code> (1/6 tên <code>SAU_TRUONG</code>) · <code>cot</code> 0-based · <code>version</code> · <code>thu_tu</code> · <code>hieu_luc_tu</code> do kho đặt · <code>actor</code>", "DD-I10: lưu <b>cách đọc</b>, không lưu dữ liệu; chỉ-thêm (đổi mẫu = version mới); CHECK đầu tiên của cả kho (mig 0019)"],
            ["<code>fls_nguon_dai</code>", "PK <code>dai_id</code> · FK <code>source_id</code>", "<code>truong</code> Date|Debit|Credit · <code>dai_tho</code> <code>'!L3:L'</code> · <code>cot</code> suy ra (NULL = S10 chưa đo) · <code>danh_muc</code>", "bản khai <b>thứ hai</b> (script <code>Run</code> của trang tính đọc) để S10 so với dòng 1 (<code>GAP-KHAI-01</code>; 192 phép so 0 lệch)"],
            ["<code>fls_chup</code>", "PK <code>chup_id</code>", "<code>doc_luc</code> (dấu thời điểm) · <code>spreadsheet_id</code> · <code>lan</code> Bank|Cash|PM · <code>giay</code> · <code>actor</code> (<code>nhip@fls</code> / <code>nhip@fls(tay)</code>)", "một LẦN ĐỌC vùng chuẩn; cố ý không có <code>so_dong</code> (suy từ hai bảng dưới); chọn ảnh chụp vì «xem trước = nạp» chỉ đúng bằng cấu trúc khi cùng <code>chup_id</code>"],
            ["<code>fls_chup_nguon</code>", "PK <code>(chup_id, source_id)</code> · 2 FK", "<code>khai_version</code> đã dùng để đọc nguồn này", "nguồn ra 0 dòng vẫn có mặt — để «gọi tên» nguồn rỗng"],
            ["<code>fls_chup_dong</code>", "PK <code>(chup_id, source_id, dong_so)</code> · 2 FK", "<code>o</code> jsonb {tên trường: giá trị nguyên văn}, 5/6 trường (không <code>Description</code>)", "jsonb, không text — ép chuỗi làm sê-ri ngày thành <code>45586</code> (<code>QĐ-ITL-102</code>); lằn Bank 7.454.400 ô thô, lằn PM 0 (<code>GAP-CHUP-01</code>)"],
            ["<code>fls_run</code>", "PK <code>run_id</code> text · FK <code>khai_id</code> NULLABLE · FK <code>chup_id</code> NULLABLE", "3 <code>*_version</code> NN (<code>INV-I12</code>) · <code>row_count</code> đếm từ bảng · <code>state</code> mặc định <code>queued</code>", "NULL <b>có chủ đích</b>: lô <code>NAP-2026-08-27-RAW</code> có trước bảng khai/ảnh — không bịa (<code>R-A1</code>); hình <code>NAP-yyyy-mm-dd-NGUON</code>"],
            ["<code>fls_reject</code>", "PK <code>rej_id</code> · FK <code>run_id</code> · UQ <code>(run_id, source_sheet, source_row)</code>", "<code>reason</code> NN có tên", "khoá thêm <code>source_sheet</code> ở mig 0020 sau khi 646 dòng loại của 23 nguồn mất bản ghi (một <code>run_id</code> cho 59 nguồn)"],
        ])
        + P("Lineage thật từ một dòng sổ về tờ giấy: <code>fls_itl.run_id → fls_run.chup_id → fls_chup_nguon(source_id, khai_version) → fls_khai_cot</code>. Không có <code>khai_id</code> trên <code>fls_itl</code> vì <code>fls_khai_cot</code> giữ một dòng/trường nên <code>khai_id</code> không định danh được một bản khai (<code>GAP-CHUP-04</code>).")
    ))

    out.append(S("s1-3", f"§1.3 Tầng ③ ④ — Sổ kế toán · Ghép lệnh chi {BUILT}", body=
        P("<code>fls_itl</code> là bảng trung tâm: 43 cột, chia lớp theo cách đọc của DEV-04.")
        + T([("Lớp", 14), ("Cột", 50), ("Luật", 36)], [
            ["C · danh tính", "<code>itl_id</code> PK seq · <code>content_key</code> UQ = sha256(source_system, source_sheet, doc_date, ps_no, ps_co, doc_no, seq_trung) · <code>itl_id_sheet</code> (ITL# sổ cũ, chỉ đối soát)", "<code>INV-I04a</code> danh tính đóng băng (trigger chặn đổi) · <code>INV-I04b</code> khoá đối sánh, không phải danh tính; 357 dòng (3,7 %) trùng khoá nội dung là lý do giữ <code>itl_id_sheet</code>"],
            ["C · lineage · run", "<code>source_system|sheet|row</code> NN · <code>run_id</code> FK NN · <code>contract_version, canon_version, mapping_version</code> NN", "<code>INV-I05</code>, <code>INV-I12</code>; FK để gõ sai <code>run_id</code> bị chặn (<code>GAP-ERD-P0-01</code>)"],
            ["C · trạng thái", "<code>raw_frozen</code> · <code>is_flash</code> · <code>period_state</code> open|locked · <code>work_status</code> ok|UNMAPPED|rejected · <code>created_at</code>", "<code>INV-I03/I14/I13/I16</code>; enum bằng lời văn, chặn ở tầng ghi"],
            ["A · 14 trường hợp đồng", "<code>doc_date</code> date · <code>doc_no</code> · <code>memo</code> · <code>curr</code> · <code>ps_no/ps_co</code> numeric(20,2) · <code>acct</code> · <code>le</code> FK · <code>hd</code> · <code>pay_type</code> · <code>cdt1</code> · <code>svc_start/svc_end</code> <b>text</b>", "ITL-CONTRACT v1.1 đọc theo TÊN (<code>QĐ-ITL-42</code>); <code>svc_*</code> là kỳ <code>YYYYMM</code> người gõ, không phải date (mig 0005); <code>le</code> = cột P không phải BL"],
            ["A′ · song song &amp; ngoài P&amp;L", "7 cột <code>*_thyt</code> (5 P&amp;L + <code>id_payee_thyt</code>, <code>invoice_thyt</code>) · <code>id_payee</code> · <code>invoice</code> · <code>le_payer</code> FK · <code>is_intercompany</code> GENERATED · <code>pic</code> · <code>audit_status</code> · <code>pm_hinh</code>", "<code>QĐ-ITL-35</code>: <code>thyt</code> NULL chỗ máy bịa, không vào parity; 5 cột ALLOCATE <b>đã bỏ</b> (mig 0012), <code>pm_line_id</code> <b>đã bỏ</b> (mig 0007 → <code>fls_pm_link</code>)"],
            ["B · canon", "<code>canon</code> jsonb NN — 38 ô nguyên văn theo vị trí", "4 cột AH–AK trùng tên nên lưu theo vị trí, không theo key"],
        ])
        + T([("Bảng", 16), ("Khoá", 26), ("Cột đáng nhớ", 32), ("Luật", 26)], [
            ["<code>fls_le</code>", "PK <code>le_code</code>", "<code>le_name</code> NULL cho 24/29 mã (<code>GAP-LE-01</code>) · <code>is_entity</code>", "không lấy mã làm tên — NULL trung thực hơn (<code>INV-I16</code>); <code>INV-I10</code>"],
            ["<code>fls_mapping_master</code>", "PK <code>hd_code</code> (đảo có tên)", "<code>need_cfa2</code> · <code>method_cfa2</code> (52/73 rỗng ⇒ Sheets hiện <code>0</code>) · <code>code_hr</code> · <code>coa1/coa2</code>", "danh mục soi gương: nạp = thay toàn bộ trong một giao dịch; 73 mã; phép suy ALLOCATE đọc từ đây"],
            ["<code>fls_pm_line</code>", "PK <code>(run_id, pm_line_id)</code> · UQ <code>(run_id, source_row)</code> · FK <code>run_id</code>", "<code>pm_slip_id</code> · <code>ref_tho</code> / <code>ref_canon</code> (hai trạng thái của một trường) · <code>amount</code> · <code>curr</code> · <code>status</code> Approve|RỖNG|Reject · <code>tho</code> <b>json</b> (giữ thứ tự 28 cột, mig 0022) · <code>hd</code> · <code>cdt1</code> · <code>read_at</code>", "ảnh chụp dòng lệnh chi tại một lần nạp; <code>pm_line_id</code> không FK (<code>fps_*</code> là hệ khác, <code>QĐ-ITL-45</code>); không PII (<code>Email Address</code> không bao giờ vào kho); ảnh hiệu lực = <code>max(read_at)</code>"],
            ["<code>fls_pm_link</code>", "PK <code>link_id</code> · UQ <code>(itl_id, pm_line_id, lan)</code> · FK <code>itl_id</code>, <code>run_id</code>", "<code>amount</code> phần tiền quy cho dòng lệnh (Σ theo <code>itl_id</code> = tiền bank — cổng <code>SIGMA_MOI_NOI</code>) · <code>hinh</code> A|B|C|T · <code>lan</code>", "là LỊCH SỬ; hiệu lực tra ở view; khoá đổi 28/08 (<code>QĐ-ITL-69</code>) để bỏ được mối nối mà không xoá dòng"],
            ["<code>fls_pm_unlink</code>", "PK <code>unlink_id</code> · UQ <code>link_id</code> · FK <code>link_id, itl_id, evt_id</code>", "<code>at</code>", "bỏ đúng một lần; <b>không</b> có <code>actor/reason</code> — chúng sống ở <code>fls_queue_event</code> (một chỗ, mũi tên đỏ duy nhất đi xuống tầng ⑤)"],
            ["view <code>fls_moi_noi</code>", "—", "<code>fls_pm_link</code> trừ <code>fls_pm_unlink</code> (<code>NOT EXISTS</code>)", "«hiện tại» là một phép tính; view cũ <code>fls_queue_xep_tien</code> bị bỏ sau 1h48 vì view không mang phạm vi"],
        ])
    ))

    out.append(S("s1-4", f"§1.4 Tầng ⑤ ⑥ ⑦ — Việc của người · Sửa &amp; vết · Hạ tầng {BUILT}", body=
        T([("Bảng / view", 18), ("Khoá", 22), ("Cột · phép tính", 36), ("Luật", 24)], [
            ["<code>fls_queue_event</code>", "PK <code>evt_id</code> · FK <code>itl_id</code>", "<code>evt_type</code> reason|defer|match|unmatch|done|reopen · <code>reason</code> · <code>defer_until</code> · <code>actor</code> NN · <code>at</code>", "bảng THẬT duy nhất của tầng ⑤; máy cũng ghi <code>reason</code> lúc nạp CỜ ⇒ phép đếm mốc hỏi <code>evt_type</code> không hỏi <code>count(*)</code>"],
            ["view <code>fls_queue_state</code>", "—", "GROUP BY <code>itl_id</code>: lý do mới nhất, <code>MAX(defer_until)</code>, <code>COUNT(defer)</code>", "lần hoãn ≥3 ⇒ màn đổi màu, không leo cấp (<code>QĐ-ITL-24</code>)"],
            ["view <code>fls_queue_reason_weekly</code>", "—", "<code>DATE_TRUNC('week', at)</code>, <code>COUNT(*) WHERE evt_type='reason'</code>", "thước <code>US-KT-045</code> «4 tuần không ai gõ = cổng chết»; <b>không tuyến nào đọc</b> hôm nay"],
            ["view <code>fls_da_xong</code>", "—", "sự kiện mới nhất trong {done, reopen} là <code>done</code>", "hàng chờ = UNMAPPED trừ view này; người bấm xong mới rời (<code>QĐ-ITL-71</code>)"],
            ["<code>fls_adjustment</code>", "PK <code>adj_id</code> · FK <code>itl_id</code> · FK <code>reversal_of</code> → chính nó · FK <code>evt_id</code> NULLABLE", "<code>field</code> · <code>value_after</code> · <code>state</code> posted|reversed · <code>actor</code> · <code>at</code>", "<code>SM-I03</code> không có deleted; <code>evt_id</code> = thao tác sinh bút toán (vd phép ghép suy <code>hd/cdt1</code>) để bỏ mối nối đảo đúng bút toán"],
            ["<code>fls_journal</code>", "PK <code>jrn_id</code> · FK <code>itl_id</code>", "<code>field</code> · <code>value_before/after</code> · <code>actor</code> · <code>at</code> · <code>value_source</code> NN · <code>reason</code>", "<code>AUD-1</code> 7 trường; insert-only; <b>0 dòng</b> trên kho thật [DOC 10/09]"],
            ["view <code>fls_sua_tay</code>", "—", "<code>row_number</code> theo (itl_id, field) DESC, loại bút toán có <code>reversal_of</code> và bút toán đã bị đảo; rn = 1", "giá trị người gõ ĐANG hiệu lực; sửa lỗi BA-07 §3 («cập nhật <code>*_thyt</code>»)"],
            ["<code>fls_migration</code>", "PK <code>version</code>", "<code>name</code> · <code>checksum</code> sha256 · <code>applied_at</code>", "BOOTSTRAP: runner tự tạo trước 0001; sửa tệp đã áp ⇒ NỔ"],
        ])
    ))

    out.append(S("s1-5", "§1.5 Cổng cạnh, trigger, hai hệ toạ độ và thuật ngữ", body=
        P("<b>Cổng cạnh</b> — 23 FK phân theo chiều tầng (đo trên <code>schema.py</code>): 11 trỏ lên tầng nhỏ hơn · 10 cùng tầng · <b>1 đi xuống</b> (<code>fls_pm_unlink.evt_id → fls_queue_event</code>: «ai bỏ ghép và vì sao» sống ở tầng VIỆC, không nhân bản) · <b>1 tự tham chiếu</b> (<code>fls_adjustment.reversal_of</code>: cơ chế thay DELETE). Tầng ⑦ không có cạnh; tầng ① chỉ nhận cạnh. Chiều là <b>quy ước đọc</b> (vẽ đỏ), không có test cấm — ghi thẳng để không ai tưởng là ràng buộc.")
        + T([("Trigger", 26), ("Sự kiện", 22), ("Cưỡng chế", 34), ("Nguồn", 18)], [
            ["<code>trg_fls_itl_inv_i03</code>", "BEFORE UPDATE OR DELETE / ROW", "<code>OLD.raw_frozen</code> ⇒ RAISE «sửa chỉ bằng bút toán mới»", "<code>triggers.py</code>, mig 0001"],
            ["<code>trg_fls_itl_inv_i04a</code>", "BEFORE UPDATE / ROW", "<code>NEW.itl_id &lt;&gt; OLD.itl_id</code> ⇒ RAISE", "<code>triggers.py</code>, mig 0001"],
            ["<code>trg_fls_itl_chan_truncate</code>", "BEFORE TRUNCATE / STATEMENT", "RAISE — bịt lỗ: trigger DELETE mức dòng không bắn khi TRUNCATE (đo 07/09, <code>QĐ-ITL-91</code>)", "<b>chỉ</b> mig 0015; <code>triggers.py</code> chưa liệt kê; <code>pg_verify</code> không so trigger ⇒ lệch này không có cổng (<a href='#s9-1'>§9.1</a>)"],
        ])
        + P("<b>Hai hệ toạ độ, đừng lẫn.</b> <i>Canon</i> 38 vị trí A..AL / 36 trường là khuôn <code>Transaction Mapping L1</code>; <i>ITL Ledge</i> 64 cột A..BL (BASE+IMPORT A–Q · ADJUSTMENT R–AT · ALLOCATE AU–AW · AUDIT AX–BL) là khuôn output. FLS lưu 18/64 cột Ledge (7 BASE + <code>le</code> + <code>itl_id_sheet</code> + 7 Final + <code>pic</code> + <code>work_status</code>); 46 cột còn lại mỗi cột có <b>lý do không lưu có tên</b> trong <code>oracle/ledge_spec.py</code> (Classifying/MID suy lại được · Manual input → <code>*_thyt</code> · ALLOCATE suy từ Mapping Master · 6×2 cột AUDIT là kết quả so với GL trước sửa). Cột <code>svc_start</code> đọc từ AB không W (W/X là khoá <code>ID PELine</code>, <code>#N/A</code> 100 % là câu trả lời — <code>QĐ-ITL-51</code>).")
        + T([("Thuật ngữ", 18), ("Nghĩa trong FLS", 52), ("Bẫy đồng âm", 30)], [
            ["<b>lằn</b>", "ba nghĩa: dòng dữ liệu (Bank · Cash · PM); hai lằn màn F01 (LỆNH CHI · TIỀN); thứ tự cắt (Ô · Cổng · Máng)", "ghi rõ nghĩa mỗi lần dùng"],
            ["<b>nguồn</b>", "một <i>dòng chảy</i> sao kê có một bố cục cột — không phải một tài khoản", "7 quỹ đổ vào 2 dòng chảy"],
            ["<b>lô · lần nạp · <code>run_id</code></b>", "một lần nạp <code>NAP-yyyy-mm-dd-NGUON</code>, có thể gồm 59 nguồn", "mọi cửa đọc mặc định lọc theo <i>lần nạp thật</i> (bản trắng), không có <code>ca_kho</code>"],
            ["<b>mối nối</b>", "một lần ghép dòng tiền ↔ dòng lệnh (<code>fls_pm_link</code>); hiệu lực = view", "AS-IS ghép theo <i>phiếu</i>; FLS ghép theo <i>dòng</i> (CR#1)"],
            ["<b>Số chứng từ</b>", "tên hiển thị duy nhất cho <code>Reference number</code> (GGSheet) = <code>ref_tho/ref_canon</code> (kho) = <code>doc_no</code> (sổ)", "từng có 5 tên; G1 quét <code>fls/web/tep</code> 0 lần «Mã tham chiếu»"],
            ["<b>thyt</b>", "cột «thật» song song với cột parity; NULL = máy không bịa", "không phải «thật» theo nghĩa kế toán đã duyệt"],
            ["<b>tự chứng</b>", "hai nghĩa: nguồn mà dữ liệu chứng minh <code>dmy/mdy</code>; dòng mà cửa GHI chắc chắn nhận (ứng viên bậc mã duy nhất, khớp cả mã lẫn tiền)", "danh sách ứng viên nói 584, cửa ghi nói 68"],
            ["<b>hoá thạch</b>", "dòng tài liệu giữ con số đúng bên trong câu đã sai (<code>QĐ-ITL-130</code>)", "cổng số sống canh số, không canh câu"],
        ])
    ))
    return out
