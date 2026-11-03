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
# ⭐⭐ `CR#11` 2026-09-07: `fls_source` RA KHOI danh sach nay (3 → 2).
# Tu khi co `fls_khai_cot`, no toi duoc `fls_itl` bang mot duong THAT:
#   `fls_itl.run_id` → `fls_run.khai_id` → `fls_khai_cot.source_id` → `fls_source`
# tuc *"dong so nay den tu NGUON nay, doc bang BAN KHAI nay"*.
#
# ⛔ Danh sach nay la **mot ngoai le co ten**, nen mot ten o lai sau khi het ly
#    do ⛔ khong phai chuyen nho: no la mot cau **da thoi dung** ma ⛔ khong cong
#    nao do, dung hinh dang cua `GAP-DOC-07`. ⇒ Tu nay co cong canh chieu nguoc:
#    `test_g_erd_3_khai_island_ma_THUC_TE_noi_duoc_thi_DO`.
ERD_ISLANDS: frozenset[str] = frozenset({
    "fls_mapping_master",   # tra theo gia tri hd; hd co the UNMAPPED nen khong FK duoc
    "fls_migration",        # so ghi di tru — ha tang, khong gan dong so nao (GAP-DB-P0-02)
})


def bang_mo_coi(tables) -> set[str]:
    """Cac BANG ⛔ khong toi duoc `fls_itl` qua duong FK (bo qua view).

    Canh FK coi la **VO HUONG**: `fls_source` ⛔ khong tro di dau ca, nhung
    `fls_khai_cot` tro TOI no, va `fls_run` tro toi `fls_khai_cot` ⇒ tu mot dong
    so di bo ve toi `fls_source` duoc. Do la lineage that, ⛔ khong phai meo do.

    ⭐ Ham nay o day — ⛔ khong nam trong file test — vi **hai** cong doc no
      (`G-ERD-3` chieu "co dao nao chua khai khong", va chieu nguoc lai "co ten
      nao khai dao ma thuc te da noi duoc khong"). Hai cong tinh kha-nang-toi
      bang hai doan ma rieng thi chinh chung se troi khoi nhau.
    """
    canh: dict[str, set[str]] = {}
    for n, t in tables.items():
        if t.kind == "view":
            continue
        canh[n] = {c.fk.split(".")[0] for c in t.columns if c.fk} | {n}
    ke: dict[str, set[str]] = {n: set() for n in canh}
    for n, ds in canh.items():
        for d in ds:
            if d in ke:
                ke[n].add(d)
                ke[d].add(n)
    toi_duoc: set[str] = set()
    hang_doi = ["fls_itl"]
    while hang_doi:
        cur = hang_doi.pop()
        if cur in toi_duoc:
            continue
        toi_duoc.add(cur)
        hang_doi.extend(ke.get(cur, ()))
    return set(canh) - toi_duoc
