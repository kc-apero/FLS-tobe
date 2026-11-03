"""Chinh sach cong ERD: doc BA nao la doi chieu, bang nao duoc phep khong noi FK."""

from __future__ import annotations

import pathlib

# 2026-09-03: TRO VAO BAN GOC. Bo tai lieu ITL da chuyen vao repo nay
# (`docs/ITL/`), nen doc BA THAT gio nam TRONG repo — khong con phai voi sang
# repo canh ben.
BA_ERD_DOC = (pathlib.Path(__file__).resolve().parents[2]
              / "docs" / "ITL" / "02_BA" / "05_DATA_DICTIONARY_ERD.md")

# ⚠ DA GO 2026-09-03 — `BA_ERD_DOC_NGOAI` + `cac_doc_can_dong_bo()`.
#
# Lich su: 26/08 phat hien cong `G-ERD-2` chi canh mot BAN SAO trong repo FLS,
# con doc BA THAT song o repo `FIN-ERP` ngoai working-dir ⇒ sua doc that thi
# KHONG cong nao do. Vi hai repo khong noi voi nhau trong CI, cach vua suc luc
# do la khai them mot duong dan TUY CHON: thay thi kiem, khong thay thi BO QUA.
#
# ⛔ Do la mot duong FAIL-OPEN, va no chi dung duoc vi khong co lua chon khac:
# tren CI (hoac may khac) cong luon bo qua ban that, tuc no xanh ma KHONG do
# thu can do. Cong that su chi song tren dung mot may co hai repo canh nhau.
#
# Nay tai lieu va cong o CUNG repo ⇒ duong dan la CHAC CHAN. Mot doc BAT BUOC,
# khong nhanh bo qua, khong ban sao thu hai. Ban sao `docs/05_DATA_DICTIONARY_ERD.md`
# da xoa: giu hai file cung noi mot chuyen trong cung mot repo la tu tao hai ban
# su that — dung cai benh ma ca bo tai lieu nay chua o tang so.

# Bang KHONG noi FK voi fls_itl. Moi ten o day PHAI co island_reason trong schema.
#
# GAP-ERD-P0-01 DA DONG 2026-08-26 (owner chot): them FK fls_itl.run_id -> fls_run.run_id.
# fls_run va fls_reject NOI LIEN fls_itl tu day, da bo khoi danh sach nay (4 -> 2).
# Truoc do go sai run_id thi dong so mat lineage trong im lang, trai INV-I05.
ERD_ISLANDS: frozenset[str] = frozenset({
    "fls_mapping_master",   # tra theo gia tri hd; hd co the UNMAPPED nen khong FK duoc
    "fls_source",           # manifest pipeline, khong gan dong nao
    "fls_migration",        # so ghi di tru — ha tang, khong gan dong so nao (GAP-DB-P0-02)
})
