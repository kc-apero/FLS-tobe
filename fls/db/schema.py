"""Khai bao 18 bang + 7 view cua FLS. Chi khai bao, khong ham.

⛔⛔ Hai con so tren co CONG canh (`tests/test_ban_do_tang.py`): dong dau tep
   nay tung ghi **"10 bang + 2 view"** va no sai suot nhieu thang — mot CAU
   gia nam ngay tren SSOT cua ca kho, va ⛔ khong cong nao doc no.

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
    name="fls_le", erd_entity="LEGAL_ENTITY", tang="3-so", khau="S-so",
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
    name="fls_itl", erd_entity="ITL_ROW", tang="3-so", khau="S-so",
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
    name="fls_adjustment", erd_entity="ADJUSTMENT_ENTRY", tang="6-sua", khau="C-sua",
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
        # ⭐⭐⭐ Them 2026-09-18 (migration `0025`, `QĐ-ITL-143`, owner chot B).
        #
        # ⛔⛔ Truoc do bang GIA TRI nay ⛔ KHONG noi duoc *"ai noi con so"*:
        # `value_source` chi song o `fls_journal` (so NHAT KY), ma khung xem
        # tra loi *"o nay dang la gi"* (`fls_sua_tay`) doc **bang nay**.
        # ⇒ Mot goi y cua MAY ghi vao day se hien y het quyet dinh cua NGUOI,
        #   va `_hieu_luc()` lay no lam `value_before` cho lan go sau.
        #   Do dung la `INV-I16`.
        C("nguon", "text", null=False, default="'sua_tay'",
          check="nguon IN ('sua_tay', 'may_goi_y')",
          comment="sua_tay = NGUOI chot · may_goi_y = MAY suy tu dong lenh. "
                  "⛔ fls_sua_tay CHI lay `sua_tay` (INV-I16)"),
    ))

_FLS_JOURNAL = Table(
    name="fls_journal", erd_entity="JOURNAL", tang="6-sua", khau="C-sua",
    columns=(
        C("jrn_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("itl_id", "bigint", null=False, fk="fls_itl.itl_id"),
        C("field", "text", null=False),
        C("value_before", "text"),
        C("value_after", "text"),
        C("actor", "text", null=False),
        C("at", "timestamptz", null=False, default="now()"),
        # ⭐⭐ `WO-018` (`BA-05` v0.34 `DD-I15 ⓓe`, `TL-016`): **lop cua CHINH
        #   dong** (ai noi `value_after`) = `fls_adjustment.nguon` cua but toan
        #   ghi cung giao dich trong `ghi_tay._them` (cua ghi cuong che).
        # ⛔⛔ Chu thich cu *"nguon goi y luc go"* la dau vet nghia THU HAI
        #   (`HOI-016` ⓑ): cu `/adjust` tung ghi nguon TRUOC khi go (`UNMAPPED`
        #   · `nguon` · `may_goi_y` · `sua_tay`). So that 02/10: 0 dong nhu the;
        #   kho TEST cu thi co ⇒ ⛔ `CHECK` o day (phieu rieng neu can).
        C("value_source", "text", null=False,
          comment="lop cua chinh dong: sua_tay = NGUOI · may_goi_y = MAY; "
                  "= fls_adjustment.nguon cung giao dich (DD-I15 ⓓe)"),
        C("reason", "text"),
    ))

_FLS_RUN = Table(
    name="fls_run", erd_entity="RUN", tang="2-nap", khau="A-nap",
    columns=(
        C("run_id", "text", null=False, pk=True),
        C("contract_version", "text", null=False),
        C("canon_version", "text", null=False),
        C("mapping_version", "text", null=False),
        C("started_at", "timestamptz", null=False, default="now()"),
        C("row_count", "int"),
        C("state", "text", null=False, default="'queued'", comment="SM-I04"),
        # ⭐⭐ `CR#11` / `DD-I10` — lo nap nay doc bang BAN KHAI nao.
        # ⛔ NULLABLE co chu dich, ⛔ khong phai de long tay: lan nap
        # `NAP-2026-08-27-RAW` (10.030 dong dang nam trong kho) CO TRUOC bang
        # `fls_khai_cot`, va bia mot `khai_id` cho qua khu la trai `R-A1`.
        # ⇒ NULL o day doc la *"lo nay co truoc khi ban khai co cho o"*, mot
        #   cau THAT — con mot so bia ra thi doc nhu mot cau tra loi, va do la
        #   dung benh ma ca `INV-I16` chua (NULL trung thuc hon ma bia).
        C("khai_id", "bigint", fk="fls_khai_cot.khai_id",
          comment="DD-I10: ban khai anh xa cot dung cho lo nay. NULL = lo co "
                  "TRUOC khi bang khai ton tai (⛔ khong bia — R-A1)"),
        # ⭐⭐ `QĐ-ITL-110` — lo nay doc tu ANH CHUP nao.
        # ⛔ NULLABLE co chu dich, cung ly do `khai_id` ngay tren: mot lo vao
        # bang duong `dong` (test / phep do doi chung) **PHAI HIEN RA** la
        # `chup_id = NULL`, tuc *"⛔ khong co anh chup nao dung sau no"*.
        # Khai `NOT NULL` la buoc phai **bia** mot anh chup cho moi lo test —
        # tuc lam ban dung cai cot dung ra de noi that.
        C("chup_id", "bigint", fk="fls_chup.chup_id",
          comment="QĐ-ITL-110: anh chup vung CHUAN ma lo nay doc. NULL = lo "
                  "vao bang duong `dong` (test/doi chung), ⛔ KHONG co anh "
                  "chup dung sau — ⛔ khong bia (R-A1)"),
    ))

# ⭐⭐⭐ `DD-I10` — BAN KHAI ANH XA COT (`CR#11`, migration `0016`).
#
# ⛔⛔ **Bang nay ⛔ KHONG luu du lieu — no luu CACH DOC du lieu.**
#
# Vi sao phai ton tai: ke toan DA tu giai bai "60+ dinh dang sao ke", va giai
# rat tot — **dong 1 cua moi sheet `R |` la mot ban khai anh xa** (`1`=Date …
# `6`=Reference number), ho tu duy tri bang tay, do duoc **68/68 sheet khai du**
# tren **19 bo cot khac nhau** (do tren kho 08/09; **16** neu chi dem 5
# truong FLS thuc doc). ⚠ Con so **9** cua ban truoc DUNG nhung chi nhin
# **3/6 truong** — mot con so dung trong mot cau sai.
# `QĐ-ITL-105` bo Google Sheets khoi duong nap
# ⇒ ⛔ khong dung cho o moi thi **ban khai ay bi vut theo**, va FLS phai **doan
# vi tri cot** — thu `fls/adapters/sao_ke.py` cam thang: *"doan ⛔ khong phai la
# kem chinh xac — no la SAI TIEN."*
#
# ★ Ba luat (`DD-I10` ⓷), va moi luat chong mot hong CU THE:
#   ⓐ ⛔ CHI-THEM — sua khai = them `version` moi. Mot dong nap thang truoc
#      phai giai thich duoc bang ban khai HIEU LUC LUC AY; sua de la viet lai
#      lich su (`INV-I08`).
#   ⓑ ⛔ Du 6 truong moi cho nap — thieu mot truong la NO TO (`BanKhaiHong`),
#      ⛔ khong nap mot phan: mat cot trong im lang, ma cot mat co the la cot tien.
#   ⓒ ⛔ `cot` la SO, `truong` la TEN. `ITL-CANON` co 4 cot trung ten ⇒ ⛔ khong
#      tham chieu theo ten duoc; con tep nguon thi doi thu tu cot ⇒ ⛔ khong neo
#      theo so duoc. Hai dau **phai nguoc nhau**.
#
# ⚠ Luat ⓑ va mien gia tri (`truong` ∈ `SAU_TRUONG` · `cot >= 0`) ⛔ KHONG
#   cuong che o tang kho — ca repo nay ⛔ khong co mot `CHECK` nao, enum deu la
#   **loi van + chan o tang ghi** (`work_status` · `period_state` · `src_type` ·
#   `evt_type`). Giu dung tien le do; cho chan la `fls/repo/khai_cot.py` (task
#   `2`), va no phai chan luc **GHI** — chan luc doc thi ban khai hong da nam
#   trong kho roi.
_FLS_KHAI_COT = Table(
    name="fls_khai_cot", erd_entity="KHAI_COT", tang="1-anh", khau="A-nap",
    columns=(
        C("khai_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("source_id", "bigint", null=False, fk="fls_source.source_id",
          comment="khai nay cua NGUON nao"),
        C("version", "int", null=False,
          comment="ngan hang doi mau sao ke ⇒ khai MOI, ⛔ khong sua khai cu"),
        C("truong", "text", null=False,
          comment="mot trong 6 ten cua `sao_ke.SAU_TRUONG` — doc theo TEN"),
        C("cot", "int", null=False, comment="chi so cot 0-based trong tep nguon"),
        # ⭐⭐ `QĐ-ITL-113` — THU TU NGAY do nguon khai (migration `0019`).
        #
        # `cot` noi *"doc cot nao"*; `thu_tu` noi *"doc THE NAO"* — cung ban
        # chat ⇒ cung mot dong, va duoc `version` + `actor` mien phi.
        #
        # ⛔⛔ `NULL` = *"nguon ⛔ CHUA khai"*, ⛔ **khong** = *"coi nhu
        #    `dmy`"*. Do 08/09 tren anh chup that: **1.894/8.368 dong (22,6%)**
        #    co ngay mo ho, trai **29/60 nguon**, va **29/29** nguon ay la
        #    **`mdy`** — ⛔ **0** nguon `dmy`. Mot mac dinh *"vi day la Viet
        #    Nam"* se **hoan ngay<->thang tren 1.894 dong** (`QĐ-ITL-17`).
        C("thu_tu", "text",
          check="thu_tu IS NULL OR (truong = 'Date' AND thu_tu IN ('dmy', 'mdy'))",
          comment="QĐ-ITL-113: `dmy`|`mdy`, CHI tren dong `Date`. NULL = "
                  "nguon chua khai ⇒ ngay mo ho van BI LOAI kem ly do"),
        C("hieu_luc_tu", "timestamptz", null=False, default="now()"),
        C("actor", "text", null=False,
          comment="ban khai la HANH VI CUA NGUOI, phai co ten"),
    ),
    unique_keys=(("source_id", "version", "truong"),))

# ⭐⭐⭐ `QĐ-ITL-110` — LAN ANH CHUP (`BA-07` §4c, migration `0018`).
#
# ⛔⛔ **Ba bang nay sinh ra vi mot phep do, ⛔ khong vi mot y tuong.** Soi man
# `F04` xuong bang tuyen ngay 08/09 (**20** tuyen that): man can **5 cua**, va
# **3 cua ⛔ KHONG TON TAI**. Nang hon: **hai cua CO van ⛔ khong chay duoc**,
# vi ca `POST /nap/xem-truoc` lan `POST /nap` doi nguoi goi **dua san `dong`**
# vao than yeu cau — tien de *"man hinh da cam tep trong tay nguoi dung"* cua
# `QĐ-ITL-105` ⓷, thu ma `QĐ-ITL-109` **da lat** (`F04` ⛔ khong co mot o nhap
# nao; cu chi dan **o lai Google Sheets**).
# ⇒ Trinh duyet ⛔ khong doc duoc Sheets, cua thi ⛔ khong tu doc
#   ⇒ **⛔ KHONG CO duong nao dua du lieu vao.**
#
# ── Vi sao ANH CHUP, va ⛔ KHONG phai vi toc do ────────────────────────────
#
# ⚠⚠ Lap luan dau tien la SAI, giu lai lam bia: toi dan `GAP-API-04` (*"nguon
#    chap chon, timeout 3/3"*) de chong duong doc song. Phep do ay chay tren
#    workbook **`ADJUSTED`** (day `IMPORTRANGE`), ⛔ **khong** tren `R |`. Do
#    chinh `R |` 08/09: **1,8s** liet ke + **2,7s** doc & chuyen = **4,4 giay
#    / 60 sheet / 8.365 dong** — thua suc trong han cho 10s cua client.
#
# ⭐⭐ Ly do THAT nam o `BA-07` §4b ⓶: no hua *"xem truoc cho ra DUNG THU nap
#    se ghi"*. Neu moi cua tu doc Sheets **song** thi hai cua doc sheet o **hai
#    thoi diem khac nhau** ⇒ loi hua **vo trong im lang**, ma nguoi dung tin
#    **cai ho vua nhin thay**. Cung mot `chup_id` thi no dung **bang CAU TRUC**,
#    ⛔ khong bang ky luat nguoi viet.
#
# ⚠ Cong mot rang buoc da do: han muc doc Sheets la **tai nguyen dung CHUNG
#   voi owner dang mo chinh file do** — da an `429` THAT khi goi 60 lot thay
#   vi gop. Mot man doc song moi lan bam la mot man **tieu han muc cua nguoi
#   khac**.
#
# ── Ba bang, va ⛔ KHONG mot con so nao luu HAI lan ────────────────────────
#
#   `fls_chup`        — mot LAN DOC. Trang thai ② cua `F04` can *"doc luc
#                       nao"* ma ⛔ khong phai cham 8.365 dong.
#   `fls_chup_nguon`  — mot NGUON trong mot lan doc + `khai_version` DA DUNG.
#                       ⭐⭐ Nho bang nay ma nguon doc ra **0 dong** van **CO
#                       MAT** — dung diem mu `S8` tung tu lo: *"sheet ra 0
#                       dong bien mat khoi chinh phep kiem sinh ra de tim no"*.
#   `fls_chup_dong`   — mot dong vung CHUAN, o de `jsonb` theo TEN TRUONG.
#
# ⛔⛔ **⛔ KHONG co `so_dong`/`so_nguon` o bang dau.** Ca hai **suy duoc** tu
#    hai bang duoi, va mot cai dau ghi `so_dong = 8365` canh mot bang dong
#    **RONG** la **mot loi noi doi ma ⛔ khong cong nao thay** — dung luat nen
#    *"do duoc 0 thu ⇒ ⛔ KHONG DAT"*. `giay` thi GIU, vi no ⛔ khong suy duoc
#    tu dau.
#
# ⛔⛔ **`o` la `jsonb`, ⛔ KHONG `text` — va day la lan thu BA cung cai bay.**
#    Ep moi o ve chuoi lam se-ri ngay thanh `"45586"` (`QĐ-ITL-102` ⓶) va lam
#    `L6` cua cong #17 do duoc **0 dong** ⇒ do. Anh chup phai giu **KIEU** cua
#    o dung nhu sheet tra ve: so la so, chuoi la chuoi.
#
# ⛔ `Description` ⛔ **KHONG co mat trong anh chup** (`QĐ-ITL-92`/`107`) —
#   5/6 truong, cuong che o `sao_ke.TRUONG_DOC_DUOC`.
#
# ⭐ Ban khai dung luc nap ⛔ **khong can mot co che moi**:
#   `repo.khai_cot.doc_khai(conn, source_id, tai=doc_luc)` **da** tra ban khai
#   *hieu luc tai mot moc* — dung viec tham so `tai=` duoc dung ra de lam
#   (task `2`). `fls_chup_nguon.khai_version` **ghim** ket qua ay de doi chieu
#   duoc, ⛔ **khong** de thay no.
_FLS_CHUP = Table(
    name="fls_chup", erd_entity="CHUP", tang="1-anh", khau="A-nap",
    island_reason="dau anh chup — `fls_run.chup_id` tro NGUOC ve day; "
                  "⛔ khong dong so nao tro toi no truc tiep",
    columns=(
        C("chup_id", "bigint", null=False, pk=True,
          default="nextval('seq_itl_id')"),
        C("doc_luc", "timestamptz", null=False, default="now()",
          comment="★ DAU THOI DIEM — trang thai ② hien con so nay. ⛔ KHONG "
                  "phai 'tuoi': tuoi la mot phep tru, dau thoi diem la mot su that"),
        C("spreadsheet_id", "text", null=False,
          comment="doc workbook NAO — hai lan chup tu hai file la hai thu khac nhau"),
        C("lan", "text", null=False,
          comment="Bank | Cash — hai lan khac khuon RA (GAP-CANON-02: bank 10 "
                  "cot, quy 11) nen ⛔ khong duoc lan vao nhau"),
        C("giay", "numeric(8,2)",
          comment="phep doc mat bao lau. ⛔ KHONG suy duoc tu dau nen phai luu; "
                  "do that 08/09: 4,4s cho 60 sheet"),
        C("actor", "text", null=False,
          comment="chup la HANH VI, phai co ten — cung luat `fls_khai_cot.actor`"),
    ))

_FLS_CHUP_NGUON = Table(
    name="fls_chup_nguon", erd_entity="CHUP_NGUON", tang="1-anh", khau="A-nap",
    columns=(
        C("chup_id", "bigint", null=False, fk="fls_chup.chup_id"),
        C("source_id", "bigint", null=False, fk="fls_source.source_id"),
        C("khai_version", "int", null=False,
          comment="ban khai DA DUNG de doc nguon nay trong lan chup nay — "
                  "ghim ket qua `doc_khai(tai=doc_luc)` de doi chieu duoc"),
    ),
    # Mot lan chup doc mot nguon nhieu nhat MOT lan.
    pk_cols=("chup_id", "source_id"))

_FLS_CHUP_DONG = Table(
    name="fls_chup_dong", erd_entity="CHUP_DONG", tang="1-anh", khau="A-nap",
    columns=(
        C("chup_id", "bigint", null=False, fk="fls_chup.chup_id"),
        C("source_id", "bigint", null=False, fk="fls_source.source_id"),
        C("dong_so", "int", null=False,
          comment="thu tu dong TRONG VUNG DOC (0-based) — de truy nguoc ve sheet"),
        C("o", "jsonb", null=False,
          comment="{ten truong: gia tri NGUYEN VAN}, 5/6 truong (⛔ khong "
                  "Description). ⛔ KHONG `text`: ep ve chuoi la dung lai cai "
                  "bay lam se-ri ngay thanh \"45586\""),
    ),
    pk_cols=("chup_id", "source_id", "dong_so"))

_FLS_NGUON_DAI = Table(
    name="fls_nguon_dai", erd_entity="NGUON_DAI", tang="1-anh", khau="A-nap",
    columns=(
        C("dai_id", "bigint", null=False, pk=True, default="nextval('seq_itl_id')"),
        C("source_id", "bigint", null=False, fk="fls_source.source_id",
          comment="dai nay cua NGUON nao"),
        C("truong", "text", null=False,
          comment="Date | Debit | Credit — danh muc chi khai BA truong"),
        C("cot", "int",
          comment="0-based, suy tu `dai_tho`. NULL = ⛔ KHONG suy duoc ⇒ S10 bao CHUA DO"),
        C("dai_tho", "text", null=False,
          comment="nguyen van o danh muc, vd `!L3:L` — giu de mat nguoi doi chieu duoc"),
        C("danh_muc", "text", null=False,
          comment="BankAccountList | Cash Ledger List"),
        C("doc_luc", "timestamptz", null=False, default="now()"),
    ))

_FLS_REJECT = Table(
    name="fls_reject", erd_entity="REJECT", tang="2-nap", khau="A-nap",
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
    #
    # ⛔⛔⛔ **SUA 10/09 (migration `0020`) — them `source_sheet`.** Khoa cu
    # `(run_id, source_row)` dung khi **mot lan nap = MOT nguon**. `QĐ-ITL-111`
    # dung cua nap CA LO — *mot* `run_id` cho **59 nguon** — va `source_row` chi
    # la chi so dong TRONG MOT SHEET ⇒ dong 0 cua 59 sheet dung chung mot gia
    # tri, chi nguon den truoc duoc ghi. Do that tren anh `24033`: **646 dong bi
    # loai ma ⛔ KHONG co ban ghi nao**, trai tren **23 nguon** (chi 11 nguon co
    # ban ghi). Dau van tay: 1.143 ban ghi tren **1.143 `source_row` khac nhau
    # tuyet doi**. `run_id` giu trong khoa nen tinh *chay lai ⛔ khong nhan ban*
    # (ly do `0007` ra doi) ⛔ khong mat.
    unique_keys=(("run_id", "source_sheet", "source_row"),))

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
    name="fls_pm_link", erd_entity="PM_LINK", tang="4-ghep", khau="B-ghep",
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
        # ⭐⭐⭐ Them 2026-09-18 (migration `0024`, `CR#12` · `GAP-ERD-P0-02`).
        #
        # ⛔⛔ **Vi sao mot cot RIENG chu ⛔ khong dung `run_id` san co.**
        # `run_id` mang **HAI nghia** tuy duong ghi: `chay_nap.chen_moi_noi`
        # ghi lan **NAP**, con `ghi_tay` ghi anh **LENH CHI**. Do 18/09 tren
        # kho that: ca **2.262** dong deu la lan NAP — vi ⛔ chua ai ghep tay
        # lan nao (`hinh='T'` = 0). Mot cot hai nghia thi moi cau hoi dat len
        # no deu co hai cau tra loi dung.
        #
        # ⛔ **Cai gia cua viec thieu no, do duoc:** `fls_pm_line` khoa chinh
        # **ghep doi** `(run_id, pm_line_id)` — 22 anh PM giu 22 ban cua cung
        # mot dong lenh. Noi hai bang bang `pm_line_id` DON thi moi phep dem
        # **phong dung bang SO ANH PM**: 2.262 moi noi -> **49.764**. Cau SQL
        # van chay trot lot, con so van **trong hop ly**, va ⛔ khong co canh
        # bao nao. Bay nay can HAI lan trong MOT ngay (18/09).
        #
        # ⚠ **`NULL` duoc, va no co nghia THAT:** *"moi noi sinh truoc khi cot
        # nay ra doi"*. 2.262 dong cu ⛔ khong suy nguoc chac chan duoc anh PM
        # nao dang hieu luc ngay 10/09 — mot `DEFAULT` o day se bien
        # *"⛔ khong biet"* thanh mot lo **doan** (`INV-I16`).
        #
        # ⚠ ⛔ **Chua dat `FOREIGN KEY`**: rang buoc cung tren du lieu lich su
        # doi mot phep **suy**, va phep suy ⛔ khong duoc hoa thanh rang buoc.
        # Bai `test_moi_noi_neo_anh_pm` do bang mot **cau dem**, ⛔ khong bang
        # mot `FK` — do duoc ma ⛔ khong chan lan nap nao.
        C("run_pm", "text", null=True, fk="fls_run.run_id",
          comment="ANH LENH CHI da dung luc ghep. NULL = moi noi sinh truoc "
                  "2026-09-18. ⛔ KHONG lay `run_id` thay: cot do mang hai nghia"),
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
    name="fls_pm_unlink", erd_entity="PM_UNLINK", tang="4-ghep", khau="B-ghep",
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
    name="fls_pm_line", erd_entity="PM_LINE_SNAP", tang="4-ghep", khau="B-ghep",
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
        # ⭐⭐⭐ BAY KHOA `PE`/`PI` LEN KIEU — 2026-09-17, migration `0023`.
        #
        # ⛔⛔ Owner chot: *"PE/PI cot CO KIEU trong `fls_pm_line`, chua can
        #   lam bang rieng"*. ⇒ **Duong VAO ≠ THUC THE**: ca ba di nho mot
        #   duong nap (`PM_Unpivot`), nhung chung la **ba thuc the khac nhau**.
        #
        # ⛔ Truoc hom nay bay khoa nay chi song trong `tho` (JSON) — tuc kho
        #   **CO du lieu ma ⛔ KHONG co kieu**: ⛔ khong tra duoc, ⛔ khong noi
        #   duoc, ⛔ khong canh duoc.
        C("pe_slip", "text", comment="'ID PESlip'. Do: 3.500/26.404 dong"),
        C("pe_line", "text",
          comment="'ID PELine'. ⛔ Di CAP voi `pe_slip` — do 26.404 dong: 0 lech"),
        C("pe_loai", "text",
          check="pe_loai IS NULL OR (pe_line IS NOT NULL "
                "AND pe_loai IN ('Advance', 'Urgent'))",
          comment="⭐ MA SINH RA, ⛔ khong doc thang: nguon de o HAI cot rieng "
                  "('(Advance)' 3.381 · '(Urgent)' 119 = 3.500, trung 0). "
                  "⛔ Day la `CHECK` DUY NHAT trong nhom nay — xem `pm_join`"),
        C("pi_slip", "text", comment="'ID PISlip'. Do: 22.904/26.404 dong"),
        C("pi_line", "text",
          comment="'ID PILine'. ⛔ Di CAP voi `pi_slip` — do 26.404 dong: 0 lech. "
                  "⭐ Mot dong co DUNG MOT cha: chi PI 22.904 · chi PE 3.500 · "
                  "ca hai 0 · khong cha 0. ⛔ ⛔ Bat bien ay CO Y ⛔ KHONG thanh "
                  "`CHECK`: phep chen chay trong MOT giao dich cho ca lan nap, "
                  "nen mot dong la se DO CA LUOT thay vi thanh tin tuc"),
        # ⭐⭐ Them 2026-09-11 (migration `0021`) — owner chot **CO LUU dong tho**.
        #
        # ⛔⛔ Truoc no, lan `PM` giu **8 truong da phan tich** va **20 cot con
        #    lai cua `PM_Unpivot` bien mat ngay luc doc** ⇒ them mot truong ve
        #    sau thi ⛔ khong bu nguoc duoc, phai doi cu chup ke tiep. Lan
        #    `Bank` thi ⛔ khong co van de ay: no giu 7.454.400 dong tho.
        #
        # ⛔ Khoa theo **TEN COT**, ⛔ khong theo vi tri — cot xe dich thi ban
        #   khai vi tri lech, con ten thi ⛔ khong.
        # ⛔⛔ `json`, ⛔ KHONG `jsonb` (migration `0022`). `jsonb` **sap lai
        #    khoa** nen thu tu cot cua to giay **chet ngay luc ghi** — ma owner
        #    doi dung thu tu ay (11/09). Gia: ⛔ khong co toan tu `?`/`@>`,
        #    ⛔ khong GIN. Quet ma nguon: **0** cau dung chung tren cot nay.
        C("tho", "json",
          comment="ca hang tho cua PM_Unpivot, khoa theo TEN COT, GIU DUNG "
                  "THU TU COT cua to giay. NULL = anh chup TRUOC 11/09 "
                  "(⛔ khong phai 'doc duoc 0 cot'). "
                  "⛔ KHONG chua `Email Address` — xem PM_COT_RIENG_TU"),
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
    name="fls_mapping_master", erd_entity="MAPPING_MASTER", tang="3-so", khau="S-so",
    island_reason="danh muc HD — tra theo gia tri hd, khong FK vi hd co the UNMAPPED",
    columns=(
        C("hd_code", "text", null=False, pk=True),
        C("need_cfa2", "text"),
        C("method_cfa2", "text"),
        C("code_hr", "text"),
        C("coa1", "text"),
        C("coa2", "text"),
    ))

# ⭐⭐ 2026-09-07 (`CR#11`) — bang nay **THOI LA DAO**.
#
# Truoc do no khai `island_reason="manifest pipeline — pipeline ghi, F06 doc"`:
# dung, vi ⛔ khong dong so nao tro toi duoc no. Tu khi co `fls_khai_cot` thi
# co mot **duong di THAT**, di bo duoc:
#
#     fls_itl.run_id → fls_run.khai_id → fls_khai_cot.source_id → fls_source
#
# doc ra tieng Viet: *"dong so nay den tu NGUON nay, doc bang BAN KHAI nay"*.
# ⇒ Giu lai loi khai dao la giu mot cau **da thoi dung**, nen no bi go — cung
#   luc mot cong moi ra doi de chuyen nay ⛔ khong lap lai trong im lang:
#   `test_g_erd_3_khai_island_ma_THUC_TE_noi_duoc_thi_DO`.
_FLS_SOURCE = Table(
    name="fls_source", erd_entity="SOURCE", tang="1-anh", khau="A-nap",
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
    name="fls_queue_event", erd_entity="QUEUE_EVENT", tang="5-viec", khau="V-viec",
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
    name="fls_queue_state", kind="view", erd_entity="QUEUE_STATE", tang="5-viec", khau="V-viec",
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
    name="fls_queue_reason_weekly", kind="view", erd_entity="QUEUE_REASON_WEEKLY", tang="5-viec", khau="V-viec",
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
    name="fls_sua_tay", kind="view", erd_entity="MANUAL_EFFECTIVE", tang="6-sua", khau="C-sua",
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
        AND a.nguon = 'sua_tay'
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1""".strip())

# ⭐⭐⭐ Khung xem GOI Y CUA MAY (migration `0025`, `QĐ-ITL-143`, owner chot B).
#
# ⛔⛔ **Vi sao no la mot khung xem RIENG, ⛔ khong phai mot cot cua `fls_sua_tay`.**
# `fls_sua_tay` dang tra loi **MOT** cau — *"NGUOI da chot gi"* — va `bang_tuyen.py`
# co **8 tuyen** doc no voi dung nghia ay. Nhet goi y cua may vao rong roi bat moi
# cho tu loc la doi nghia mot khung xem **dang chay**; cho nao quen loc thi ⛔ khong
# bao loi, chi tra sai — dung hinh benh `gate-filtering-own-column-is-blind`.
#
# ⇒ Hai cau hoi khac nhau, hai khung xem khac nhau. Man hinh hoi **ca hai** roi ve
#   *"may doan X — anh gat ⛔ khong?"*; phep do parity hoi **mot** (`fls_sua_tay`).
_V_MAY_GOI_Y = Table(
    name="fls_may_goi_y", kind="view", erd_entity="MACHINE_SUGGESTION",
    tang="6-sua", khau="C-sua",
    island_reason="khung xem doc tu fls_adjustment — goi y cua may dang co hieu "
                  "luc, khong luu gi",
    columns=(
        C("itl_id", "bigint"),
        C("field", "text"),
        C("value_after", "text"),
        C("adj_id", "bigint"),
        C("at", "timestamptz"),
    ),
    view_sql="""
SELECT z.itl_id, z.field, z.value_after, z.adj_id, z.at
FROM (SELECT a.itl_id, a.field, a.value_after, a.adj_id, a.at,
             row_number() OVER (PARTITION BY a.itl_id, a.field
                                ORDER BY a.adj_id DESC) AS rn
      FROM fls_adjustment a
      WHERE a.reversal_of IS NULL
        AND a.nguon = 'may_goi_y'
        AND NOT EXISTS (SELECT 1 FROM fls_adjustment d
                        WHERE d.reversal_of = a.adj_id)) z
WHERE z.rn = 1""".strip())

# ⭐⭐⭐ Khung xem DIEN GIAI SAO KE (migration `0026`, `QĐ-ITL-145`).
#
# ⛔⛔⛔ **Vi sao dien giai KHONG nam trong `fls_itl`.** `QĐ-ITL-128` (17/09) da
# cho doc `Description`, nhung `fls_itl.memo` van `0/8.387`: **quyet dinh doi,
# duong ghi o lai**. Va nay ⛔ **khong sua duoc bang cach nap lai** —
# `content_key` ⛔ khong chua dien giai nen luot nap lai bi **bo qua vi trung**;
# cung ⛔ **khong duoc `UPDATE`** — `INV-I08`, so la sach chi-them.
#
# ⭐ Nhung nhip chup moi gio DA giu no. Do `18/09`: noi duoc **8.361/8.387**,
#   co chu **8.358**, va **tien te KHOP 8.358** — phep kiem thu ba ay chung
#   minh noi **dung dong**, vi mot phep noi **lech mot hang** van se tra ve
#   `99,7%` va van trong hoan toan hop ly.
#
# ⚠ Dong ⛔ khong co dien giai thi **VANG** khoi khung xem — mot o rong noi
#   *"giao dich nay khong co noi dung"*, su that la *"chua doc duoc"*.
_V_DIEN_GIAI = Table(
    name="fls_dien_giai", kind="view", erd_entity="STATEMENT_MEMO",
    tang="1-anh", khau="A-nap",
    island_reason="khung xem noi fls_itl voi anh chup moi nhat — khong luu gi",
    columns=(
        C("itl_id", "bigint"),
        C("dien_giai", "text"),
        C("chup_id", "bigint", comment="TUOI cua cau chu — doc luc nao"),
    ),
    view_sql="""
SELECT i.itl_id,
       btrim(d.o ->> 'Description') AS dien_giai,
       d.chup_id
FROM fls_itl i
JOIN fls_source s ON s.source_key = i.source_sheet
JOIN LATERAL (
  SELECT dd.o, dd.chup_id
    FROM fls_chup_dong dd
   WHERE dd.source_id = s.source_id
     AND dd.dong_so   = i.source_row
   ORDER BY dd.chup_id DESC
   LIMIT 1
) d ON true
WHERE btrim(coalesce(d.o ->> 'Description', '')) <> ''""".strip())

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
    name="fls_moi_noi", kind="view", erd_entity="PM_LINK_EFFECTIVE", tang="4-ghep", khau="B-ghep",
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
    name="fls_da_xong", kind="view", erd_entity="QUEUE_DONE", tang="5-viec", khau="V-viec",
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
    name="fls_migration", erd_entity="MIGRATION", tang="7-ha-tang", khau="H-ha-tang",
    island_reason="so ghi cac lan di tru — ha tang, khong gan dong so nao",
    columns=(
        C("version", "int", null=False, pk=True),
        C("name", "text", null=False),
        C("checksum", "text", null=False, comment="sha256 file .sql — sua sau khi ap la NO"),
        C("applied_at", "timestamptz", null=False, default="now()"),
    ))

TABLES: dict[str, Table] = {t.name: t for t in (
    _FLS_LE, _FLS_KHAI_COT, _FLS_NGUON_DAI,
    _FLS_CHUP, _FLS_CHUP_NGUON, _FLS_CHUP_DONG,
    _FLS_RUN, _FLS_ITL, _FLS_PM_LINK, _FLS_PM_LINE,
    _FLS_ADJUSTMENT,
    _FLS_JOURNAL,
    _FLS_REJECT, _FLS_MAPPING_MASTER, _FLS_SOURCE, _FLS_QUEUE_EVENT,
    _FLS_PM_UNLINK,
    _V_QUEUE_STATE, _V_QUEUE_REASON_WEEKLY, _V_SUA_TAY, _V_MAY_GOI_Y, _V_DIEN_GIAI,
    _V_MOI_NOI,
    _V_DA_XONG,
    _FLS_MIGRATION,
)}

# ⚠ `fls_queue_event` PHAI dung TRUOC `fls_adjustment`: tu 2026-08-28 but toan
# co FK `evt_id` tro ve thao tac sinh ra no (migration `0013`). Dat sai thu tu
# thi cau `CREATE` do o kho trong.
#
# ⭐ 2026-09-07 (`CR#11`): `fls_source` NHAY LEN dau — no thoi la mot manifest
#   dung cuoi hang, no nay la **cha FK** cua `fls_khai_cot`, ma `fls_khai_cot`
#   lai la cha cua `fls_run`. Chuoi cha→con moi: `fls_source` → `fls_khai_cot`
#   → `fls_run` → `fls_itl`. (`test_create_order_cha_truoc_con` canh cho nay.)
CREATE_ORDER: tuple[str, ...] = (
    "fls_le", "fls_source", "fls_khai_cot", "fls_nguon_dai",
    # ⭐ `fls_chup*` PHAI truoc `fls_run` — `fls_run.chup_id` tro vao `fls_chup`
    #    (`QĐ-ITL-110`), va `fls_chup_nguon`/`fls_chup_dong` tro vao ca
    #    `fls_chup` lan `fls_source` ⇒ ca hai da dung phia tren.
    "fls_chup", "fls_chup_nguon", "fls_chup_dong",
    "fls_run", "fls_itl", "fls_pm_link", "fls_pm_line",
    "fls_queue_event", "fls_pm_unlink",
    "fls_adjustment", "fls_journal",
    "fls_reject", "fls_mapping_master",
    "fls_queue_state", "fls_queue_reason_weekly", "fls_sua_tay",
    "fls_may_goi_y", "fls_dien_giai", "fls_moi_noi",
    "fls_da_xong",
)

# Bang do RUNNER di tru tu tao truoc khi ap migration dau tien, nen CO Y khong
# nam trong CREATE_ORDER. Moi ten o day phai co ly do — giong luat ERD_ISLANDS.
BOOTSTRAP: frozenset[str] = frozenset({
    "fls_migration",   # phai ton tai TRUOC migration 0001 nen khong the la 0001
})
