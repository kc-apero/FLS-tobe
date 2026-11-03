# -*- coding: utf-8 -*-
"""§5 Complex Logic — FLS."""
from apgen import *

def sections():
    out = []
    out.append(S("s5", "§5 Complex Logic — năm khối thuật toán và bất biến", st="draft", body=
        P("Năm chỗ trong FLS có luật đủ dày để cần một mục riêng: hợp đồng và khuôn canon (§5.1), phép suy 7 khối Final (§5.2), phép ghép lệnh chi và trần cứng (§5.3), thước chuẩn và các bộ luật soát (§5.4). §5.5 gom mọi bất biến, cổng và mã lỗi vào một chỗ để không phải đọc rải.")
    ))

    out.append(S("s5-1", f"§5.1 Hợp đồng 14 trường · canon 38 vị trí · <code>validate</code> {BUILT}", body=
        T([("Lớp", 16), ("Định nghĩa", 46), ("Luật then chốt", 38)], [
            ["<b>ITL-CONTRACT</b> v1.1 (<code>fls/contract/itl_contract.py</code>)", "14 trường <code>fls_itl</code> phải có, đọc <b>theo tên</b>: <code>doc_date A · doc_no B · memo C · curr D · ps_no E · ps_co F · acct G · le P · itl_id R · hd V · pay_type Z · cdt1 AD · svc_start AH · svc_end AL</code>", "v1.0 đóng băng 2026-08-24 (<code>QĐ-ITL-42</code>), không đổi một chữ (test khoá); v1.1 (CR#2) chỉ đổi <code>svc_start/svc_end</code> <code>date → text</code> vì đó là <b>kỳ</b> <code>YYYYMM</code> người gõ (39/57 giá trị không phải YYYYMM trên 9.967 dòng). Phương án «thêm <code>svc_ky</code> riêng» bị loại vì trường mới không có nguồn (<code>P-ITL-05</code>)"],
            ["<b>ITL-CANON</b> (<code>fls/canon/spec.py</code>)", "38 vị trí A..AL / 36 trường, chép nguyên văn header dòng 3 của <code>Transaction Mapping L1</code>; truy cập <b>theo vị trí</b>, <code>CanonRow</code> cố ý không có <code>as_dict</code>", "4 cột AH–AK trùng tên; W/X và AB/AC trùng tên nhưng <b>khác khoá ghép</b> (<code>ID PELine</code> vs <code>ID PILine</code>, <code>QĐ-ITL-51</code>) — W/X <code>#N/A</code> 100 % là <i>câu trả lời</i>; Z/AA trống ⇒ 38 vị trí/36 trường. Hai hệ toạ độ canon ↔ <code>ITL Ledge</code> 64 cột, đừng lẫn"],
            ["<b>validate</b> (<code>fls/canon/validate.py</code>)", "<code>validate(row, thu_tu) → KetQua(loai, cho)</code>; <code>parse_so</code> chấp định dạng kế toán, rác thì NỔ; <code>parse_ngay</code> seri Sheets chặn dải [20.000, 63.800]", "<b>THIẾU ≠ SAI KIỂU</b>: ① ngày không đọc được → LOẠI · ② cả <code>PS Nợ</code> và <code>PS Có</code> rỗng/0 → LOẠI · ③ số không đọc được → LOẠI · ④ thiếu Tài khoản / Tiền tệ → CHỜ (<code>UNMAPPED</code>). Chuỗi <code>d/m/y</code> cả hai ≤12 ⇒ NỔ, buộc <code>thu_tu</code> từ bản khai; đo 29/29 nguồn mơ hồ là <code>mdy</code>, 0 <code>dmy</code> (<code>QĐ-ITL-113</code>)"],
            ["<b>Ô lỗi</b> (<code>o_loi.py</code>) · <b>LE</b> (<code>le.py</code>)", "9 mã lỗi Sheets, so bằng prefix (<code>#N/A (Did not find value…)</code>); <code>ma_le</code> = phần trước <code>' - '</code>", "<code>##LAI NHAP VON#</code> là kế toán gõ tay, không phải ô lỗi (7 giao dịch thật từng bị loại oan); <code>Cash Treasury</code> đi qua nguyên vẹn (<code>GAP-LE-01</code>)"],
        ])
    ))

    out.append(S("s5-2", f"§5.2 Final 7 khối · cột <code>_thyt</code> · ALLOCATE suy lại {BUILT}", body=
        P("Sheet <code>ITL Ledge</code> AS-IS lặp bốn cột <code>Classifying | Manual input | MID | Final</code> cho 7 khối. FLS đọc được công thức thật và tái hiện <b>từng ô</b>; TO-BE bỏ tầng <code>MID</code> và để <code>Final</code> là ô kế toán nhập/sửa (<code>QĐ-owner-0824</code>).")
        + MER("""flowchart LR
  classDef src fill:#f4f4f5,stroke:#71717a,color:#1f2937;
  classDef act fill:#f0fdf4,stroke:#16a34a,color:#1f2937;
  classDef store fill:#eff6ff,stroke:#1d4ed8,color:#1f2937;
  classDef gate fill:#fef2f2,stroke:#991b1b,color:#1f2937;
  canon["canon 38 ô<br/>S · H · T · AB · AC · Y · AD"]:::src
  cls["classifying(v)<br/>iferror(ô, 'Need to manual input')<br/>luật B: rỗng giữ rỗng"]:::act
  mid["tinh_mid(cls, manual, mặc định KHỐI)<br/>bước 1 · DD-I06"]:::act
  fin["tinh_final(cls, mid)<br/>= if(or(S='NTMI', len(S)=0), U, S)"]:::act
  par[("parity<br/>= sổ, kể cả chỗ mặc định")]:::store
  thyt[("*_thyt<br/>NULL khi máy tự bịa")]:::store
  ws["work_status = UNMAPPED<br/>1 trong 5 khối P&L trống"]:::gate
  canon --> cls --> mid --> fin
  fin --> par
  fin --> thyt
  thyt --> ws
""", "<strong>Hình 5.2</strong> — Hai bước tách rời: gộp lại thì 6/7 khối khớp nhưng khối 7 lệch 521/584 ô; tách ra khớp 4.088/4.088.")
        + T([("Khối", 14), ("Vị trí Classifying", 14), ("Mặc định máy (đo 9.219 dòng)", 24), ("Hợp đồng P&L", 12), ("Vào hàng chờ", 36)], [
            ["① <code>hd</code> Budget Code", "18 (S)", "<code>OGA | GAC - Other</code>", "có", "thiếu ⇒ UNMAPPED; <code>hd</code> ngoài <code>Mapping Master</code> 73 mã ⇒ <code>FLS-UNKNOWN-CODE</code>"],
            ["② <code>pay_type</code>", "7 (H)", "<code>Thanh toán (Regular)</code>", "có", "thiếu ⇒ UNMAPPED"],
            ["③ <code>cdt1</code> Chủ dự toán", "19 (T)", "<code>SHQ2 | Headquarters2</code>", "có", "thiếu ⇒ UNMAPPED"],
            ["④ <code>svc_start</code>", "27 (AB, không W)", "<code>None</code> (<code>GAP-ORA-06</code>)", "có", "khuôn <code>YYYYMM</code> ⇒ <code>FLS-BAD-FORMAT</code> khi gõ"],
            ["⑤ <code>svc_end</code>", "28 (AC, không X)", "<code>None</code>", "có", "như ④"],
            ["⑥ <code>id_payee</code>", "24 (Y)", "<code>VD0</code>", "không", "không đẩy hàng chờ (thiếu >95,7 % dòng)"],
            ["⑦ <code>invoice</code>", "29 (AD)", "<code>Nợ hoá đơn</code>", "không", "như ⑥"],
        ])
        + P("<b>Cột <code>_thyt</code> («thật»)</b> song song với parity (<code>QĐ-ITL-35</code>, áp cả 7 khối): <code>parity</code> = giá trị y như sổ kể cả chỗ máy gán mặc định (để so từng ô 100 %); <code>thyt</code> = <code>NULL</code> đúng chỗ máy tự bịa (<code>Manual input == 'Input here'</code> và Classifying không trả lời) — NULL trung thực hơn một câu bịa (<code>INV-I16</code>), và <code>thyt</code> không bao giờ chạm giá trị người gõ (<code>AUD-12</code>). Chọn W/X thay AB/AC chỉ khớp 70,4 %; luật A (rỗng → NTMI) sai 1.490 ô ở khối invoice.")
        + P("<b>ALLOCATE là phép tính, không phải cột.</b> Ba công thức owner đưa 28/08: <code>AU = AD</code> (CFA1 là bản sao <code>cdt1</code>) · <code>AV = VLOOKUP(V, MM!H:K) = 'Need to Allocate to CFA2' ? cờ : AU</code> · <code>AW = VLOOKUP(V, MM!H:L) &lt;&gt; '' ? L : 'No need'</code>. Hai bẫy Sheets được giữ nguyên có chủ ý: so chuỗi không phân biệt hoa/thường, và ô L rỗng thật ⇒ VLOOKUP trả <code>0</code> ⇒ <code>Method = '0'</code> (52/73 mã, <code>GAP-ALLOC-01</code>). Năm cột ALLOCATE bị bỏ khỏi <code>fls_itl</code> (<code>QĐ-ITL-65</code>, migration 0012) vì suy lại được 100 % từ <code>cdt1 + hd + fls_mapping_master</code>; muốn thêm lại phải mở lại hai quyết định.")
    ))

    out.append(S("s5-3", f"§5.3 Ghép PM: <code>canon_ref</code>, dung sai, ứng viên, tự chứng, TRẦN CỨNG {BUILT}", body=
        T([("Thành phần", 18), ("Luật", 52), ("Nguồn · đo", 30)], [
            ["<code>canon_ref(raw)</code>", "NFKC → upper → bỏ <code>[\\s\\-_.,/\\\\]</code> → gỡ ký hiệu khoa học <code>4.36619E+15</code> → ô lỗi ⇒ <code>None</code>. <b>Chưa</b> cắt tiền tố ngân hàng (<code>GAP-JOIN-01</code>)", "<code>pm_join.py:144-171</code>; 0/7.329 dòng chưa ghép trả <code>None</code> ⇒ bộ chuẩn hoá không phải nút thắt"],
            ["Dung sai", "<code>DUNG_SAI = {VND: 1.000}</code> (<code>QĐ-ITL-57</code>) · ngoại tệ <b>0</b> (<code>QĐ-ITL-62</code>) · ghép tay <code>min(1.000, 0,5 % tiền bank)</code> (<code>QĐ-ITL-63</code>)", "301 dòng lệch tiền: chỉ 16/491 trong khoảng phí bank ⇒ cửa ghi từ chối <b>đúng</b>"],
            ["Xếp hình lúc nạp", "<code>xep_ca_lat</code>: gom theo mã; đúng 1×1 & Σ khớp ⇒ A; 1×N & Σ khớp ⇒ B + <code>chia_tien</code>; N×1 & Σ khớp ⇒ C; còn lại D/E/F ⇒ người. Kết quả cố ý <b>nhỏ hơn</b> AS-IS: 26,79 % không đoán vs 33,2 % VLOOKUP (968/3.312 khớp mã nhưng không khớp tiền)", "<code>tests/adapters/test_pm_join.py</code> T-JOIN-01…09 · fixture 3.703 PM × 9.992 bank"],
            ["Cửa ghép tay <code>ghep_lenh</code>", "7 phép kiểm ⓐ–ⓖ: dòng tiền thật · dòng PM thuộc ảnh hiệu lực · chưa bị ghép cho dòng khác · phạm vi · cùng tiền tệ (ⓔ) · Σ trong dung sai (ⓕ) · <code>status = Approve</code> (ⓖ); ghi <code>hinh='T'</code>, <code>lan</code> tăng theo cặp", "<code>ghi_tay.py:522-707</code>; 409 kèm giá trị đang có"],
            ["Cửa ghép LÔ <code>match-lo</code> (B2)", "thân <b>chỉ</b> <code>itl_ids[]</code>, máy đo lại phía máy chủ; ghép chỉ tập <b>tự chứng</b> = ứng viên bậc <code>ma</code> duy nhất, cả chùm cùng mã, khớp cả mã lẫn tiền; một dòng không tự chứng ⇒ <b>422 cả lô, 0 mối nối</b>", "68 dòng (0,9 %) — <code>QĐ-ITL-118</code>; 61 dòng lệch tiền <b>không</b> vào nút lô (máy không quyết thay người)"],
            ["TRẦN CỨNG (<code>do_mau_so._tran</code>)", "mỗi dòng lệnh chỉ ghép cho một dòng tiền ⇒ <code>toi_da = da_noi + ranh</code>; <code>tran = toi_da / 8.246</code>; <code>phu_tren_tran = da_noi / toi_da</code>", "47,4 % · 65,6 % (2.562/3.907); <code>QĐ-ITL-122</code> đo phía PM: 2.427/3.772 = 64,3 % đã có tiền; việc thật 1.345 dòng / 698 phiếu (188 phiếu nối một phần)"],
            ["«Lệch 353» không phải mâu thuẫn", "<code>work_status</code> trả lời «máy suy đủ 5 trường chưa» (đóng băng lúc nạp); <code>fls_moi_noi</code> trả lời «đã nối lệnh chưa». 778 đã nối mà nhãn còn UNMAPPED − 425 đủ phân loại chưa nối = 353 — một <b>hiệu</b> che 1.203 dòng", "<code>do_mau_so.do_mau_so</code> bốn ô có tên; đích thật 6.904 dòng"],
        ])
    ))

    out.append(S("s5-4", f"§5.4 Thước chuẩn, parity và ba bộ luật soát <code>L1–L9</code> · <code>S1–S10</code> · <code>G-ORA-LIVE</code> {BUILT}", body=
        T([("Bộ luật", 16), ("Ở đâu", 18), ("Từng luật", 66)], [
            ["<code>L1–L9</code> nguồn sống (cổng #17, Đ6)", "<code>fls/kiem/nguon_song.py</code>", "L1 mỗi sheet <code>R |</code> khai đủ 6 trường dòng 1 · L2 tầng NHẬP = tầng GỘP từng tài khoản · L3 mỗi dòng gộp có xuất xứ một sheet <code>R |</code> · L4 không dòng nào mất vì kiểu ô · L5 |lệch| &lt; 1.000 VND từng tài khoản (<code>QĐ-ITL-101</code>) · L6 <code>Num</code> = thứ tự xuất hiện · L7 <code>_Filter</code> = số dòng gốc · L8 cờ đối soát kế toán TRUE · L9 mỗi tài khoản Active có sheet thật. Mọi luật: <code>da_do == 0 ⇒ KHÔNG ĐẠT</code>"],
            ["<code>S1–S10</code> soát lô (F04)", "<code>fls/kiem/soat_nap.py</code>", "<b>CHẶN</b>: S1 ba đường cân · S10 hai bản khai trỏ cùng cột. <b>CỜ</b> (ghi + hàng chờ đúng dòng): S2 có tiền phải có mã · S3 mỗi dòng có tiền · S4 có tiền tệ · S7 dòng trùng hoàn toàn không tính <code>Num</code> · S8 xuất xứ trong danh mục. <b>CANH</b>: S5 mã không bị hạ kiểu float · S6 một sheet một kiểu ngày. <code>R-A5</code>: không hạ hạng để xanh"],
            ["<code>G-ORA-LIVE-1/2/3</code>", "<code>fls/oracle/song.py</code>", "① kỳ mới nhất >45 ngày ⇒ nghi IMPORTRANGE chết · ② tab 0 dòng / toàn ô lỗi · ③ tỷ lệ ghép ngoài [25 %, 45 %] (đo 33,5 %); không đặt ngưỡng trên W/X (<code>R-ORA-07d</code>)"],
            ["Đọc đủ · tự soi · phán xử", "<code>doc_du.py</code> · <code>tu_soi.py</code> · <code>cong_parity.py</code>", "ngưỡng sàn S/H/T 3.300 · AB/AC 2.300 · Y 400 ô sau vụ 257 ô <code>svc_start</code> biến mất im lặng; dòng có <code>Final ≠ f(Classifying, MID)</code> bị loại kèm lý do (bị gõ giữa hai lần đọc); parity chỉ ĐẠT khi ≥1.000 ô · 0 lát trượt · số dòng ±2 % · 0 ô lệch — sinh ra sau khi một script đọc 0 dòng mà in PASS"],
            ["Thứ tự ngày (<code>QĐ-ITL-113/117</code>)", "<code>fls/kiem/thu_tu_ngay.py</code>", "<code>BangChung(so_dong, o_so, o_chuoi, chac_dmy, chac_mdy, mo_ho)</code>; máy <b>đề xuất</b> kèm bằng chứng, mâu thuẫn ⇒ im; người bấm khai; cửa lô chỉ nhận nguồn tự chứng và <b>không nhận</b> <code>thu_tu</code> từ màn. Đo ảnh 23719: 4.175 ô số · 4.193 chuỗi · 1.894 mơ hồ (22,6 %) trải 29/60 nguồn"],
            ["Bảo hộ phép đo", "<code>fls/kiem/do_luong.py</code>", "<code>ty_le(tu, mau, thap, cao)</code> NỔ khi ngoài khoảng khai (bắt 105,7 % của Đ4-a)"],
        ])
    ))

    out.append(S("s5-5", "§5.5 Bất biến, cổng và mã lỗi — một chỗ", body=
        P("<b>Bất biến kho <code>INV-I*</code> đang được cưỡng chế trong mã</b> (đối chiếu BA-11):")
        + T([("Mã", 10), ("Phát biểu", 44), ("Cưỡng chế", 30), ("Build", 16)], [
            ["<code>INV-I03</code>", "<code>ITL RAW</code> bất biến: <code>raw_frozen</code> ⇒ cấm UPDATE/DELETE/TRUNCATE", "trigger <code>trg_fls_itl_inv_i03</code>, migration 0015", BUILT],
            ["<code>INV-I04a/b</code>", "<code>itl_id</code> do SEQUENCE cấp, không đổi; <code>content_key</code> = hash 7 thành phần là khoá <b>đối sánh</b>, không phải danh tính", "<code>build.py</code>, <code>ON CONFLICT (content_key)</code>", BUILT],
            ["<code>INV-I05</code> · <code>I12</code>", "lineage <code>source_system/sheet/row</code>, <code>run_id</code> NOT NULL; run ghim 3 version hợp đồng", "DDL <code>fls_itl</code>, FK <code>fls_run</code>", BUILT],
            ["<code>INV-I08</code>", "sổ chỉ-THÊM: sửa = bút toán mới, đảo = dòng <code>reversal_of</code>", "<code>itl_repo</code> chỉ INSERT · <code>ghi_tay</code> · <code>test_chi_mot_cho_ghi_tay</code>", BUILT],
            ["<code>INV-I10</code> · <code>I11</code>", "LE hợp lệ (FK <code>fls_le</code>, <code>is_entity</code>); ngày là <code>date</code> không phải chuỗi", "schema", BUILT],
            ["<code>INV-I13</code>", "kỳ <code>locked</code> bất động kể cả <code>force</code>", "<code>ghi_tay.truoc_khi_go</code> → <code>FLS-LOCKED-PERIOD</code>", f"{PARTIAL} — không đường đưa kỳ sang locked"],
            ["<code>INV-I14</code>", "cờ số nhanh <code>is_flash</code>", "cột, đọc ở <code>bao.py</code>", PARTIAL],
            ["<code>INV-I16</code>", "máy không suy được ⇒ <code>UNMAPPED</code> + có mặt hàng chờ; không mặc định im lặng; mọi ghi có lý do", "<code>build.py</code>, <code>ghi_tay</code> → <code>FLS-UNMAPPED-HIDDEN</code>", BUILT],
            ["<code>INV-I17</code> · <code>I18</code>", "AK (LE = mảnh đầu Pháp nhân thanh toán) TRUE; không dùng dữ liệu để <b>cưỡng chế</b> giá trị (vòng tròn)", "<code>kiem_so_song</code>; khai là <i>không</i> ép", "đo, không ép"],
        ])
        + P("<b>Cổng đang chạy</b> (ngày đo trong ngoặc; kho không chạy lúc viết 2026-09-17 nên các con số kho là [DOC]):")
        + T([("Cổng", 26), ("Chạy ở đâu", 14), ("Chấm gì", 40), ("Trạng thái", 20)], [
            ["Bộ test <code>pytest</code>", "local (CI: <code>06_CICD_PIPELINE</code>)", "1.652 bài / 123 tệp thu thập được [CODE 2026-09-17]; 634 bài <code>pg</code> cần PostgreSQL thật, fixture dựng lại kho TEST từ <code>DROP DATABASE</code>", "chạy được offline 1.018 bài; <code>pg</code> chờ kho"],
            ["<code>lint-imports</code> 9 hợp đồng", "local/CI", "tầng nào được import tầng nào (<a href='#s6-1'>§6.1</a>)", "xanh"],
            ["Cổng chung #3/#4/#7/#8", "mã + tools", "0 dòng rơi im lặng · chạy lại y hệt (bốn đường trước/sau) · cổng phải chứng minh đã đo gì · chạy thật qua HTTP (<code>verify_cua_that/ghi</code>)", "chạy"],
            ["Cổng #13 số sống", "<code>tools/kiem_so_song.py</code>", "mỗi con số một nguồn; máy đếm mốc A (4·1·1) và B (1·1·3)", "109/109 [DOC 2026-09-08]"],
            ["Cổng #17 nguồn sống", "<code>tools/kiem_nguon_song.py</code>", "L1–L9 trên workbook P100 sống", "chạy; cần token"],
            ["Cổng ERD <code>G-ERD-1/2/3</code>", "<code>tests/db/test_erd_gates.py</code>", "ERD sinh từ <code>schema.py</code> khớp; mỗi bảng có trên ERD BA; mọi bảng tới được <code>fls_itl</code> hoặc khai <code>island_reason</code>", "xanh"],
            ["Cổng tài liệu", "<code>docs/ITL/_tools/kiem_tai_lieu.py</code> · <code>tests/test_kiem_thuyet_minh.py</code> · <code>kiem_ten_truong.py</code>", "liên kết, số sống; mọi nút có thuyết minh BA-13; một tên một trường (G1)", "chạy"],
            ["Cổng kho sạch", "<code>fls/repo/kho_sach.py</code>", "kho thật chỉ có <code>run_id</code> khớp <code>^NAP-\\d{4}-\\d{2}-\\d{2}-[A-Z0-9]+$</code>; &lt;1.000 dòng ⇒ KHÔNG ĐẠT (sau vụ 1.204 dòng test lọt kho thật 27/08)", "chạy"],
            ["<code>docs/ap-status-check.py</code>", "tay", "AP này: unmarked · stale-approval · index · fan-out · § treo", "0 failure (xem Phụ lục D)"],
        ])
        + P("<b>Mã lỗi cửa</b> (tập đóng, màn hình phải phủ hết — <code>tests/web/test_goi_cua_phu_het_ma_loi.py</code>): <code>FLS-SOAT-CHAN</code> 422 · <code>FLS-NGUON-LA</code> 404 · <code>FLS-KHAI-KHONG-CO</code> 409 · <code>FLS-CONFLICT-SOURCE</code> 409 · <code>FLS-LOCKED-PERIOD</code> 409 · <code>FLS-UNKNOWN-CODE</code> · <code>FLS-BAD-FORMAT</code> · <code>FLS-UNMAPPED-HIDDEN</code> · <code>FLS-CHUP-HONG</code> · <code>FLS-CHUP-KHONG-CO</code> · <code>FLS-DAI-HONG</code> · <code>FLS-GHEP-KHONG-TU-CHUNG</code> 422.")
    ))
    return out
