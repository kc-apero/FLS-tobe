"""Khai bao 10 bang + 2 view cua FLS. Chi khai bao, khong ham.

Nguon: 03_Dev/04_DB_IMPLEMENTATION v1.0 §2-§6b.
LECH CO CHU DICH: bo fls_id_counter, dung SEQUENCE (xem plan P0 Task 3).
"""

from __future__ import annotations

from fls.db.model import Column as C
from fls.db.model import Table

SEQUENCES: dict[str, str] = {
    "seq_itl_id": "CREATE SEQUENCE IF NOT EXISTS seq_itl_id START 1",
}

_FLS_LE = Table(
    name="fls_le", erd_entity="LEGAL_ENTITY",
    island_reason="danh muc phap nhan — fls_itl tro TOI no, khong nguoc lai",
    columns=(
        C("le_code", "text", null=False, pk=True, comment="ma phap nhan"),
        C("le_name", "text",
          comment="GAP-LE-01: nguon khong co ten cho 24/29 ma. ⛔ KHONG lay ma lam "
                  "ten — NULL trung thuc hon (INV-I16)"),
        C("is_entity", "boolean", null=False, default="true",
          comment="INV-I10: nhan khong-phai-phap-nhan (USD, HotBonus) => false"),
    ))

_FLS_ITL = Table(
    name="fls_itl", erd_entity="ITL_ROW",
    columns=(
        # -- lop C · danh tinh (INV-I04a/b) --
        C("itl_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')",
          comment="cap luc staged roi DONG BANG; KHONG theo vi tri dong"),
        C("content_key", "text", null=False, unique=True,
          comment="INV-I04b: hash(source_system,source_sheet,doc_date,ps_no,ps_co,doc_no,seq_trung)"),
        # -- lop C · lineage (INV-I05) --
        C("source_system", "text", null=False, comment="P100|Cash|A-CCR|HR|Platform"),
        C("source_sheet", "text", null=False),
        C("source_row", "int", null=False),
        # -- lop C · run (INV-I12) --
        C("run_id", "text", null=False, fk="fls_run.run_id",
          comment="GAP-ERD-P0-01 (owner chot 26/08): FK de go sai run_id bi CHAN, "
                  "khong de dong so mat lineage trong im lang (INV-I05)"),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        # -- lop C · trang thai --
        C("raw_frozen", "boolean", null=False, default="false",
          comment="INV-I03: true => trigger cam UPDATE/DELETE"),
        C("is_flash", "boolean", null=False, default="true", comment="INV-I14"),
        C("period_state", "text", null=False, default="'open'", comment="INV-I13: open|locked"),
        C("created_at", "timestamptz", null=False, default="now()"),
        # -- lop A · 14 truong ITL-CONTRACT v1.0, doc THEO TEN (QD-ITL-42) --
        C("doc_date", "date", comment="A(0) Ngay chung tu. INV-I11: date khong phai chuoi"),
        C("doc_no", "text", comment="B(1) So chung tu. AUD-12: KHONG mang nghia thoi gian"),
        C("memo", "text", comment="C(2) Dien giai"),
        C("curr", "text", comment="D(3) Don vi tien te"),
        C("ps_no", "numeric(20,2)", comment="E(4) PS No"),
        C("ps_co", "numeric(20,2)", comment="F(5) PS Co"),
        C("acct", "text", comment="G(6) Tai khoan"),
        C("le", "text", fk="fls_le.le_code", comment="P(15) SSOT phap nhan — KHONG dung BL"),
        C("hd", "text", comment="V(21) Final khoi 1 — Budget Code"),
        C("pay_type", "text", comment="Z(25) Final khoi 2 — Loai giao dich"),
        C("cdt1", "text", comment="AD(29) Final khoi 3 — Chu du toan"),
        C("svc_start", "text",
          comment="AH(33) Final khoi 4 — KY do nguoi go. ⛔ KHONG phai date: do "
                  "tren 9.967 dong co 'thang 5' '2025.07' 'TPCI' '252512'… "
                  "va khong he co ngay trong thang (migration 0005)"),
        C("svc_end", "text", comment="AL(37) Final khoi 5 — xem svc_start"),
        # -- lop A' · cot song song (QD-ITL-35) --
        C("hd_thyt", "text", comment="NULL o cho may tu bia. KHONG vao parity"),
        C("pay_type_thyt", "text"),
        C("cdt1_thyt", "text"),
        C("svc_start_thyt", "text"),
        C("svc_end_thyt", "text"),
        C("work_status", "text", null=False, default="'ok'",
          comment="INV-I16: ok|UNMAPPED|rejected"),
        # -- lop A' · khoi 6-7 ngoai hop dong P&L (QD-owner-0824) --
        C("id_payee", "text", comment="AP Final khoi 6 — goi y doc tu canon[Y]"),
        C("invoice", "text", comment="AT Final khoi 7 — link hoa don"),
        # LO 2026-08-26: khoi 6-7 co Final nhung THIEU ban noi that, trong khi
        # final_rule.BAY_KHOI da tinh ra id_payee_thyt/invoice_thyt tu P1.
        # => 4 gia tri roi im lang o tang ghi. QD-ITL-35 ap cho CA BAY khoi.
        C("id_payee_thyt", "text",
          comment="NULL o cho may tu bia (mac dinh VD0). KHONG vao parity"),
        C("invoice_thyt", "text",
          comment="NULL o cho may tu bia (mac dinh 'No hoa don'). KHONG vao parity"),
        # -- lop A' · ALLOCATE: may goi y, nguoi override thang --
        # ⛔⛔ NAM cot vung ALLOCATE (`cdt1_cfa1` `cdt1_cfa2`
        # `cdt1_cfa2_classify` `alloc_method` `alloc_method_classify`) DA BI BO
        # 2026-08-28 — owner chot (`QĐ-ITL-65`, migration `0012`).
        #
        # ⛔ Dung them lai. Ly do, gon:
        #   · ca ba o tren sheet la CONG THUC, suy lai duoc 100% tu `cdt1` +
        #     `hd` + `fls_mapping_master` (K/L) — phep suy o `ledger/allocate.py`
        #   · `AU` con chi la BAN SAO cua `cdt1` ⇒ luu no la HAI BAN SU THAT
        #   · owner chot ke toan ⛔ KHONG sua vung nay (`QĐ-ITL-64`) ⇒ hai cot
        #     `*_classify` (anh chup goi y luc NGUOI ghi de) ⛔ khong con nghia
        # ⇒ Con so ay se hien lai o man hinh nhu mot **phep tinh**, ⛔ khong
        #   phai mot cot. Muon them lai thi phai mo lai hai quyet dinh tren.
        # -- lop A' · phap nhan tra (QD-ITL-10) --
        C("le_payer", "text", fk="fls_le.le_code", comment="ai THUC tra; NULL neu nguon thieu"),
        C("is_intercompany", "boolean",
          generated="(le IS NOT NULL AND le_payer IS NOT NULL AND le <> le_payer)",
          comment="cam nhap tay — may suy"),
        # -- lop A' · audit/workflow --
        C("pic", "text", comment="BJ giu cot, CHUA len UI"),
        C("audit_status", "text", comment="BK khac work_status"),
        # -- lop B · canonical 36 cot --
        # Owner chot 2026-08-26: LUU lam THAM CHIEU, ⛔ KHONG lam khoa.
        # Can vi 357 dong (3,7%) TRUNG khoa noi dung + 105 dong khong co so
        # chung tu => khong co cot nay thi 3,7% so khong chung minh duoc la
        # chuyen dung khi cat sang FLS. ⛔ Ma nay KHONG BEN (="ITL#"&No, No=
        # ROW() tren bang da SORT) nen co test chan dung no lam danh tinh.
        # -- moi noi voi lenh chi PM --
        # ⛔ Cot `pm_line_id` DA BO (migration 0007). No chi giu duoc MOT moi noi
        # cho mot dong so, nen hinh `B` (1 dong bank tra N dong lenh) khong the
        # dau. Moi noi nay chuyen sang `fls_pm_link` — va do la MOT cho duy nhat:
        # giu ca hai la hai ban su that, dung cai benh khuon nay chua.
        C("pm_hinh", "text",
          comment="ghep BANG CACH NAO: A 1x1 · B 1 bank x N PM (chia tien) · "
                  "C N bank x 1 PM (tra nhieu lan). Khong luu thi ve sau khong ai "
                  "tra loi duoc 'dong nay ghep kieu gi'"),
        C("itl_id_sheet", "text",
          comment="ITL# cua so cu — CHI de doi soat, ⛔ KHONG phai danh tinh"),
        C("canon", "jsonb", null=False,
          comment="36 cot nguyen van theo VI TRI — 4 cot AH-AK trung ten, luu theo key la mat cot"),
    ))

_FLS_ADJUSTMENT = Table(
    name="fls_adjustment", erd_entity="ADJUSTMENT_ENTRY",
    columns=(
        C("adj_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_after", "text"),
        C("state", "text", null=False, default="'posted'",
          comment="SM-I03: posted|reversed. KHONG co deleted"),
        C("reversal_of", "bigint", fk="fls_adjustment.adj_id",
          comment="dao chi bang but toan moi (INV-I08)"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
        # ⭐⭐ Them 2026-08-28 (migration `0013`) — phep BO MOI NOI buoc phai co.
        #
        # Phep ghep TU SUY `hd`/`cdt1` tu dong lenh. Bo moi noi thi **can cu cua
        # phep suy ay mat**, nen phai dao dung nhung but toan do — ⛔ khong phai
        # moi but toan cua dong. Khong co cot nay thi cach duy nhat nhan ra
        # chung la **doi chuoi `reason`**, mot phep nhan dang vo tay lam vo.
        # ⚠ Chi ghi luc `INSERT`. ⛔ KHONG bao gio `UPDATE` (INV-I08).
        C("evt_id", "bigint", fk="fls_queue_event.evt_id",
          comment="thao tac sinh ra but toan nay (vd phep ghep suy hd/cdt1)"),
    ))

_FLS_JOURNAL = Table(
    name="fls_journal", erd_entity="JOURNAL",
    columns=(
        C("jrn_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_before", "text"),
        C("value_after", "text"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
        C("value_source", "text", null=False, comment="nguon goi y luc go"),
        C("reason", "text"),
    ))

_FLS_RUN = Table(
    name="fls_run", erd_entity="RUN",
    columns=(
        C("run_id", "text", null=False, pk=True),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        C("started_at", "timestamptz", null=False, default="now()"),
        C("row_count", "int"),
        C("state", "text", null=False, default="'queued'", comment="SM-I04"),
    ))

_FLS_REJECT = Table(
    name="fls_reject", erd_entity="REJECT",
    columns=(
        C("rej_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("run_id", "text", null=False, fk="fls_run.run_id"),
        C("source_system", "text", null=False),
        C("source_sheet", "text", null=False),
        C("source_row", "int", null=False),
        C("reason", "text", null=False, comment="ACC-4: ly do CO TEN, khong duoc rong"),
    ),
    # ⭐ Dong `GAP-DB-P0-03` (27/08). Truoc day khuon chi khai duoc khoa MOT cot
    # nen rang buoc nay ⛔ khong ton tai o tang kho: lop chan trung duy nhat la
    # dieu kien `WHERE NOT EXISTS` trong cau INSERT. Da tung hong THAT — mot lan
    # chay lai nhan ban `fls_reject` thanh 76 dong cho 19 dong loai that.
    unique_keys=(("run_id", "source_row"),))

# ⭐⭐ Bang noi mot dong so ↔ N dong lenh chi (`GAP-JOIN-03`, migration 0007).
#
# Vi sao phai co: phep ghep do duoc 6 hinh dang. Hinh `A` (1 bank × 1 PM) va `C`
# (N bank × 1 PM) moi dong chi tro toi MOT dong lenh nen mot cot du. Hinh `B`
# (1 lan chuyen tra N dong lenh) thi KHONG — va truoc 27/08, 27 dong hinh `B`
# phai vao hang cho **kem ly do co ten** thay vi dau duoc.
#
# ⛔ Cai KHONG lam: tach mot dong bank thanh N dong so (`T-JOIN-03` cua spec
# v0.1). Tach nhu the vo the 1–1 giua so va nguon ma ca bon duong doi soat dua
# vao. Bang noi giai dung van de do ma ⛔ khong dong den thang 1–1.
#
# ⚠ `pm_line_id` ⛔ KHONG FK: `fps_*` la he KHAC va FLS chi DOC (`QĐ-ITL-45`).
_FLS_PM_LINK = Table(
    name="fls_pm_link", erd_entity="PM_LINK",
    columns=(
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id",
          comment="dong so. ⛔ KHONG cascade — so la append-only (INV-I08)"),
        C("pm_line_id", "text", null=False,
          comment="fps_pm_line.line_id — dinh danh muc DONG. ⛔ KHONG cot "
                  "'ID PMLine' go tay (day #N/A). ⛔ KHONG FK (QĐ-ITL-45)"),
        C("amount", "numeric(20,2)", null=False,
          comment="PHAN tien cua dong so nay quy cho dong lenh nay. Σ theo itl_id "
                  "PHAI bang tien cua dong bank — cong `kiem_tong_moi_noi`"),
        C("hinh", "text", null=False,
          comment="A|B|C — ghep BANG CACH NAO. Khong luu thi ve sau khong ai tra "
                  "loi duoc 'dong nay ghep kieu gi'"),
        C("run_id", "text", null=False, fk="fls_run.run_id",
          comment="lan nap sinh ra moi noi nay (INV-I05 lineage)"),
        C("created_at", "timestamptz", null=False, default="now()"),
        # ⭐⭐ Them 2026-08-28 (migration `0013`, `GAP-JOIN-05`).
        C("link_id", "bigint", null=False, default="nextval('seq_itl_id')",
          comment="danh tinh cua MOT LAN ghep — co no thi BO duoc mot moi noi "
                  "ma ⛔ khong xoa dong nao (INV-I08)"),
        C("lan", "smallint", null=False, default="1",
          comment="lan ghep thu may cua cap (dong so, dong lenh). Bo roi ghep "
                  "lai dung dong lenh ay => lan+1"),
    ),
    # ⛔⛔ Khoa DA DOI 2026-08-28 (`QĐ-ITL-69`, migration `0013`).
    #
    # Khoa cu la `(itl_id, pm_line_id)` — doc ra la *"mot dong so noi voi mot
    # dong lenh nhieu nhat MOT lan trong DOI"*. Voi khoa do thi **bo roi ghep
    # lai dung dong lenh ay** — chinh ly do pho bien nhat de bo — bi kho chan
    # bang mot loi trung khoa, va ke toan ⛔ khong hieu tai sao.
    #
    # ⇒ Khoa chinh la `link_id` (mot LAN ghep), con khoa duy nhat mang them
    #   `lan`: **mot lan ghep** la duy nhat, ghep lai la `lan = 2`.
    pk_cols=("link_id",),
    unique_keys=(("itl_id", "pm_line_id", "lan"),))

# ⭐⭐ SO GHI CAC LAN BO MOI NOI — them 2026-08-28, dong `GAP-JOIN-05`.
#
# ⛔⛔ **Vi sao mot BANG chu khong mot cot `da_bo`.** Mot cot `da_bo` chi doi
# duoc bang mot cau `UPDATE` len `fls_pm_link` — va do la dung dieu luat ⓐ cua
# `fls/repo/ghi_tay.py` cam: *"THEM, khong SUA"*. Bo mot moi noi la **them mot
# dong**, y nhu dao mot but toan.
#
# ★ Bang nay CO Y ⛔ khong chua `actor`/`reason`: *ai bo* va *vi sao bo* song o
#   `fls_queue_event` (`evt_type='unmatch'`). Chep chung sang day la tao **hai
#   ban su that** — dung cai benh ca khuon nay dung ra de chua.
_FLS_PM_UNLINK = Table(
    name="fls_pm_unlink", erd_entity="PM_UNLINK",
    columns=(
        C("unlink_id", "bigint", null=False, pk=True,
          default="nextval('seq_itl_id')"),
        C("link_id", "bigint", null=False, unique=True, fk="fls_pm_link.link_id",
          comment="moi noi bi bo. UNIQUE: bo duoc DUNG MOT lan — bo hai lan la "
                  "mot lo dem, ⛔ khong phai mot thao tac"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id",
          comment="dong so — de tra 'dong nay tung bo bao nhieu lan' ma khong join"),
        C("evt_id", "bigint", null=False, fk="fls_queue_event.evt_id",
          comment="thao tac bo (evt_type=unmatch) — AI bo va VI SAO song o do, MOT cho"),
        C("at", "timestamptz", null=False, default="now()"),
    ))

# ★★ ANH CHUP dong lenh chi — them 2026-08-27, dong `GAP-API-04` bang duong (a).
#
# ⛔⛔ **Vi sao phai co, va vi sao no la mot QUYET DINH kho.** Bo nap ghep PM doc
# dong lenh tu Google Sheets **luc chay roi khong luu lai gi**. Nghia la sau khi
# nap xong, kho biet *"dong so nay noi voi dong lenh `PM00030-2`"* nhung ⛔ khong
# biet **dong lenh do la gi** — nen thao tac **ghep tay** o man `F01`
# (`QĐ-ITL-48`, viec chinh cua man do) ⛔ khong the co danh sach ung vien.
#
# Owner chot duong **(a)**: luu anh chup vao kho. Duong (b) — doc Sheets SONG
# trong mot duong HTTP — bi loai: nguon da do duoc la **chap chon** (timeout 3/3
# lan o tab `IMPORTRANGE`), va mot cua treo vi mang la cua ke toan se bo.
#
# ⛔⛔ **Va day la cho de sinh ra HAI BAN SU THAT** — dung cai benh khuon nay
# chua. Ba luat chong lai, khai ngay o day chu ⛔ khong de trong dau ai:
#   ⓐ Bang nay la **ANH CHUP CUA MOT LAN NAP** (`run_id` trong khoa chinh), ⛔
#     khong phai "danh muc lenh chi". No ⛔ khong bao gio duoc sua tai cho: nap
#     lai la **them mot anh chup moi**, anh cu con nguyen de truy.
#   ⓑ Cua doc PHAI tra **tuoi cua anh chup** (`read_at`) cung moi danh sach ung
#     vien. Cau tra loi cho "ban luu gia di thi sao" ⛔ khong phai "no khong gia"
#     ma la **noi ra no gia bao nhieu**, de nguoi go tu quyet.
#   ⓒ Tien trong anh chup ⛔ KHONG phai can cu ghi so. Luc ghep, Σ duoc cong lai
#     va so voi tien dong bank THAT trong `fls_itl` — lech thi **422**, ⛔ khong
#     chia bua (`INV-I16`).
#
# ⚠ `pm_line_id` / `pm_slip_id` ⛔ KHONG FK: `fps_*` la he KHAC va FLS chi DOC
# (`QĐ-ITL-45`). Bang nay noi voi `fls_itl` qua `fls_run` (G-ERD-3 di duoc).
#
# ⚠ Giu **CA HAI** dang ma tham chieu: `ref_tho` (nguyen van) va `ref_canon` (da
# chuan hoa). Chi giu ban chuan hoa thi be `canon_ref` di ma cong van XANH —
# dung cai bay da mac mot lan voi hien vat `Classifying`.
#
# ⛔ KHONG mang PII: ⛔ khong Timestamp · Email · Ten tai khoan · So tai khoan ·
# Ghi chu · Dien giai. Hau qua do duoc, khai thang: ⇒ xep ung vien CHI xep duoc
# theo **ma tham chieu + tien + tien te**, ⛔ **KHONG theo ngay va payee** nhu
# `BA-07` §2 mong. Muon co hai truc do thi phai mo pham vi doc — quyet dinh cua
# chu so, ⛔ khong phai cua code (`GAP-JOIN-04`).
_FLS_PM_LINE = Table(
    name="fls_pm_line", erd_entity="PM_LINE_SNAP",
    columns=(
        C("run_id", "text", null=False, fk="fls_run.run_id",
          comment="lan nap da DOC anh chup nay (INV-I05 lineage)"),
        C("pm_line_id", "text", null=False,
          comment="'ID PMLine' — dinh danh muc DONG. Do tren 3.703 dong: DUY NHAT "
                  "toan lat. ⛔ KHONG FK (QĐ-ITL-45)"),
        C("pm_slip_id", "text", null=False,
          comment="'ID PMSlip' — 1.468 phieu / 3.703 dong. Chi de GOM khi hien, "
                  "⛔ khong phai truc ghep: do ra `reference` song o DONG"),
        C("ref_tho", "text",
          comment="ma tham chieu NGUYEN VAN. 530/3.703 dong RONG"),
        C("ref_canon", "text",
          comment="ma da chuan hoa qua `canon_ref` — cot de TRA. NULL neu ma rong "
                  "hay la o loi: ⛔ o loi khong bao gio thanh khoa"),
        C("amount", "numeric(20,2)",
          comment="'Tong so tien thanh toan' cua DONG nay. ⛔ KHONG phai can cu "
                  "ghi so — luc ghep phai cong Σ va so voi tien bank THAT"),
        C("curr", "text", null=False),
        C("status", "text",
          comment="Status_Final. Do: Approve 3.347 · RONG 251 · Reject 105. "
                  "⛔ RONG la KHONG BIET, ⛔ khong phai 'da duyet' (INV-I16)"),
        C("hd", "text", comment="Budget Code (HDCode) — RONG 7/3.703"),
        C("cdt1", "text", comment="Chu du toan (CDT1) — RONG 12/3.703"),
        C("source_row", "integer", null=False,
          comment="so dong tren sheet nguon — de truy nguoc (tieu de dong 2, "
                  "du lieu tu dong 3)"),
        C("read_at", "timestamptz", null=False, default="now()",
          comment="★ TUOI cua anh chup. Cua doc PHAI tra con so nay cung moi "
                  "danh sach ung vien — xem luat ⓑ o tren"),
    ),
    # Mot lan nap chup mot dong lenh nhieu nhat MOT lan.
    pk_cols=("run_id", "pm_line_id"),
    unique_keys=(("run_id", "source_row"),))

_FLS_MAPPING_MASTER = Table(
    name="fls_mapping_master", erd_entity="MAPPING_MASTER",
    island_reason="danh muc HD — tra theo gia tri hd, khong FK vi hd co the UNMAPPED",
    columns=(
        C("hd_code", "text", null=False, pk=True),
        C("need_cfa2", "text"),
        C("method_cfa2", "text"),
        C("code_hr", "text"),
        C("coa1", "text"),
        C("coa2", "text"),
    ))

_FLS_SOURCE = Table(
    name="fls_source", erd_entity="SOURCE",
    island_reason="manifest pipeline — pipeline ghi, F06 doc (DD-I07)",
    columns=(
        C("source_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("source_key", "text", null=False, unique=True, comment="'R | HoangACB' | 'file>sheet'"),
        C("src_type", "text", null=False, comment="Bank|Cash|CCR|Platform|Mapping"),
        C("last_seen_at", "timestamptz"),
        C("lag_days", "int"),
        C("cutoff_date", "date"),
        C("txn_count", "int"),
    ))

_FLS_QUEUE_EVENT = Table(
    name="fls_queue_event", erd_entity="QUEUE_EVENT",
    columns=(
        C("evt_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("evt_type", "text", null=False,
          comment="reason|defer|match|unmatch|done|reopen — `match`/`unmatch` la vet cua phep GHEP va phep BO ghep (QĐ-ITL-48, QĐ-ITL-69); `done`/`reopen` la NGUOI bam xong / mo lai (QĐ-ITL-71)"),
        C("reason", "text"),
        C("defer_until", "date"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
    ))

_V_QUEUE_STATE = Table(
    name="fls_queue_state", kind="view", erd_entity="QUEUE_STATE",
    columns=(C("itl_id", "bigint"), C("reason", "text"),
             C("defer_until", "date"), C("defer_count", "int")),
    view_sql="""
SELECT itl_id,
       (ARRAY_AGG(reason ORDER BY at DESC)
          FILTER (WHERE evt_type = 'reason'))[1]            AS reason,
       MAX(defer_until) FILTER (WHERE evt_type = 'defer')   AS defer_until,
       COUNT(*) FILTER (WHERE evt_type = 'defer')::int      AS defer_count
FROM fls_queue_event
GROUP BY itl_id""".strip())

_V_QUEUE_REASON_WEEKLY = Table(
    name="fls_queue_reason_weekly", kind="view", erd_entity="QUEUE_REASON_WEEKLY",
    columns=(C("tuan", "date"), C("so_lan", "int")),
    view_sql="""
SELECT DATE_TRUNC('week', at)::date AS tuan,
       COUNT(*)::int                AS so_lan
FROM fls_queue_event
WHERE evt_type = 'reason'
GROUP BY 1
ORDER BY 1 DESC""".strip())

# ⛔⛔ `fls_queue_xep_tien` DA BO (migration 0009), dung 27/08 — song mot ngay.
#
# Bia mo de day, khong phai de tiec: **khung xem SQL khong nhan tham so**, nen
# no khong the mang PHAM VI. Ma phep xep hang cho bat buoc phai co pham vi —
# neu khong thi 194 dong dau test (1.285.475.949 tien bia) day % luy ke cua moi
# dong that lech di, ma ban than chung khong con trong danh sach ⇒ con so sai
# ma khong con dau vet giai thich vi sao. Loc o DAU RA ⛔ khong sua duoc mot
# thu tu da xep sai.
#
# ⇒ Phep xep chuyen sang `fls/repo/doc_bao_cao.doc_hang_cho` — mot cau CO THAM
#   SO, pham vi nam TRONG cau con (truoc khi xep). Luat `PARTITION BY curr`
#   cua `QĐ-ITL-58` giu nguyen tung chu.

# ⭐⭐ Khung xem GIA TRI NGUOI GO dang co hieu luc (`P5`, migration 0010).
#
# ⛔⛔ **Vi sao phai co khung xem nay, va vi sao `BA-07` §3 SAI mot cho.**
# `BA-07` §3 viet: *"truong hop-dong cap nhat `*_thyt`"*. Lam the la sai HAI luat
# cung luc:
#   ⓐ `INV-I08` — `fls_itl` la **append-only**. Mot cau `UPDATE` len no la mot
#     duong xoa lich su, va co trigger `INV-I03` chan san.
#   ⓑ `QĐ-ITL-35` — cot `*_thyt` la **cho MAY tu bia**, va no la cot **do
#     parity**. Ghi gia tri NGUOI GO vao do la **bo ban tay vao cai thuoc**:
#     tu do tro di khong ai phan biet duoc *"may suy dung"* voi *"nguoi da sua"*.
#
# ⇒ Gia tri nguoi go song trong `fls_adjustment` (**them dong**, khong sua dong),
#   va *"gia tri hien tai"* la mot **phep tinh**: but toan moi nhat cua tung
#   (dong, truong), tru cac but toan da bi dao.
#
# ★ Dao but toan cung la **them dong**: mot dong co `reversal_of` tro toi but
#   toan bi huy. ⛔ KHONG `UPDATE state` cua dong cu — neu doi trang thai tai cho
#   thi so nhat ky khong con la so nhat ky.
_V_SUA_TAY = Table(
    name="fls_sua_tay", kind="view", erd_entity="MANUAL_EFFECTIVE",
    island_reason="khung xem doc tu fls_adjustment — tinh gia tri nguoi go dang "
                  "co hieu luc, khong luu gi",
    columns=(
        C("itl_id", "bigint"),
        C("field", "text"),
        C("value_after", "text"),
        C("adj_id", "bigint", comment="de man hinh dao dung but toan nao"),
        C("actor", "text"),
        C("at", "timestamptz"),
    ),
    view_sql="""
SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.actor, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.actor, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1""".strip())

# ⭐⭐ Khung xem MOI NOI DANG CO HIEU LUC (migration 0013, `GAP-JOIN-05`).
#
# Cung mot thuoc thang voi `fls_sua_tay`: **so giu ca lich su, con "hien tai" la
# mot PHEP TINH**. `fls_pm_link` tu day la **lich su moi lan ghep**; cau hoi
# *"dong nay dang noi voi dong lenh nao"* tra loi o day.
#
# ⛔⛔ **Va day la cho cua mot cai bay.** Moi cho DOC con tro vao `fls_pm_link`
# sau 2026-08-28 se doc **ca nhung moi noi da bo** — va no ⛔ khong bao loi, chi
# tra sai. Co cong `tests/repo/test_moi_noi_hieu_luc.py` quet ma nguon chan
# huong do: moi cau DOC phai tro vao khung xem nay.
_V_MOI_NOI = Table(
    name="fls_moi_noi", kind="view", erd_entity="PM_LINK_EFFECTIVE",
    island_reason="khung xem doc tu fls_pm_link tru fls_pm_unlink — moi noi dang "
                  "co hieu luc, khong luu gi",
    columns=(
        C("link_id", "bigint"), C("itl_id", "bigint"),
        C("pm_line_id", "text"), C("amount", "numeric(20,2)"),
        C("hinh", "text"), C("lan", "smallint"), C("run_id", "text"),
        C("created_at", "timestamptz"),
    ),
    view_sql="""
SELECT l.link_id, l.itl_id, l.pm_line_id, l.amount, l.hinh, l.lan, l.run_id,
       l.created_at
FROM fls_pm_link l
WHERE NOT EXISTS (SELECT 1 FROM fls_pm_unlink u WHERE u.link_id = l.link_id)""".strip())

# ⭐⭐ Khung xem DONG DA XONG (migration 0014, `QĐ-ITL-71`, dong `GAP-JOIN-06`).
#
# ⛔⛔ **Lo no dong.** `fls_itl.work_status` bi **dong bang luc nap** va ⛔ khong
# co gi tinh lai — moi cua ghi deu ⛔ khong dung vao `fls_itl` (dung `INV-I08`).
# ⇒ Ke toan chua xong mot dong thi dong ay **VAN nam trong hang cho, mai mai**.
#
# ★★ **Owner chot (28/08): NGUOI BAM "XONG"**, ⛔ khong phai may tu nha khi thay
# du 5 truong. Can cu la nghiep vu: may tu nha thi ke toan **mat cho danh dau
# viec dang lam do**; nguoi bam thi hang cho dai hon nhung **dung y nguoi**.
#
# ⇒ *"Dong nay da xong chua"* la mot **PHEP TINH**: su kien MOI NHAT trong hai
#   loai `done`/`reopen`. Bam nham thi `reopen` — cung la THEM mot su kien,
#   ⛔ khong xoa. Cung thang thuoc voi `fls_sua_tay` va `fls_moi_noi`.
_V_DA_XONG = Table(
    name="fls_da_xong", kind="view", erd_entity="QUEUE_DONE",
    island_reason="khung xem doc tu fls_queue_event — dong da duoc NGUOI bam "
                  "xong, khong luu gi",
    columns=(
        C("itl_id", "bigint"),
        C("evt_id", "bigint", comment="su kien `done` dang co hieu luc"),
        C("actor", "text"), C("at", "timestamptz"), C("reason", "text"),
    ),
    view_sql="""
SELECT z.itl_id, z.evt_id, z.actor, z.at, z.reason
FROM (SELECT e.itl_id, e.evt_id, e.actor, e.at, e.reason, e.evt_type,
             row_number() OVER (PARTITION BY e.itl_id
                                ORDER BY e.evt_id DESC) AS rn
      FROM fls_queue_event e
      WHERE e.evt_type IN ('done', 'reopen')) z
WHERE z.rn = 1 AND z.evt_type = 'done'""".strip())

_FLS_MIGRATION = Table(
    name="fls_migration", erd_entity="MIGRATION",
    island_reason="so ghi cac lan di tru — ha tang, khong gan dong so nao",
    columns=(
        C("version", "int", null=False, pk=True),
        C("name", "text", null=False),
        C("checksum", "text", null=False, comment="sha256 file .sql — sua sau khi ap la NO"),
        C("applied_at", "timestamptz", null=False, default="now()"),
    ))

TABLES: dict[str, Table] = {t.name: t for t in (
    _FLS_LE, _FLS_RUN, _FLS_ITL, _FLS_PM_LINK, _FLS_PM_LINE, _FLS_ADJUSTMENT,
    _FLS_JOURNAL,
    _FLS_REJECT, _FLS_MAPPING_MASTER, _FLS_SOURCE, _FLS_QUEUE_EVENT,
    _FLS_PM_UNLINK,
    _V_QUEUE_STATE, _V_QUEUE_REASON_WEEKLY, _V_SUA_TAY, _V_MOI_NOI,
    _V_DA_XONG,
    _FLS_MIGRATION,
)}

# ⚠ `fls_queue_event` PHAI dung TRUOC `fls_adjustment`: tu 2026-08-28 but toan
# co FK `evt_id` tro ve thao tac sinh ra no (migration `0013`). Dat sai thu tu
# thi cau `CREATE` do o kho trong.
CREATE_ORDER: tuple[str, ...] = (
    "fls_le", "fls_run", "fls_itl", "fls_pm_link", "fls_pm_line",
    "fls_queue_event", "fls_pm_unlink",
    "fls_adjustment", "fls_journal",
    "fls_reject", "fls_mapping_master", "fls_source",
    "fls_queue_state", "fls_queue_reason_weekly", "fls_sua_tay", "fls_moi_noi",
    "fls_da_xong",
)

# Bang do RUNNER di tru tu tao truoc khi ap migration dau tien, nen CO Y khong
# nam trong CREATE_ORDER. Moi ten o day phai co ly do — giong luat ERD_ISLANDS.
BOOTSTRAP: frozenset[str] = frozenset({
    "fls_migration",   # phai ton tai TRUOC migration 0001 nen khong the la 0001
})
