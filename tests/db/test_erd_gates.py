import json
import pathlib

from fls.db.render import render_erd_json, render_erd_mermaid
from fls.db.schema import TABLES

_ROOT = pathlib.Path(__file__).resolve().parents[2]
JSON_PATH = _ROOT / "ERD-CONTRACT.json"
MMD_PATH = _ROOT / "ERD-CONTRACT.mmd"


def test_g_erd_1_json_khop_code():
    """G-ERD-1: doi schema ma quen sinh lai ERD => do."""
    assert json.loads(JSON_PATH.read_text(encoding="utf-8")) == render_erd_json(TABLES), (
        "ERD-CONTRACT.json lech schema. Chay: python -m fls.db.erd_export --write")


def test_g_erd_1_mermaid_khop_code():
    assert MMD_PATH.read_text(encoding="utf-8") == render_erd_mermaid(TABLES), (
        "ERD-CONTRACT.mmd lech schema. Chay: python -m fls.db.erd_export --write")


def test_erd_json_co_quan_he_fk():
    erd = render_erd_json(TABLES)
    cap = {(r["from"], r["to"]) for r in erd["relations"]}
    assert ("fls_journal", "fls_itl") in cap
    assert ("fls_itl", "fls_le") in cap


import re

from fls.db.erd_policy import BA_ERD_DOC, ERD_ISLANDS, bang_mo_coi


def _entity_trong_doc_BA() -> set[str]:
    """Doc khoi ```mermaid erDiagram trong 05_DATA_DICTIONARY_ERD.md."""
    txt = BA_ERD_DOC.read_text(encoding="utf-8")
    khoi = re.search(r"```mermaid\s*\nerDiagram\n(.*?)```", txt, re.S)
    assert khoi, "khong tim thay khoi erDiagram trong doc BA"
    return set(re.findall(r"^\s{4}(\w+)\s*\{", khoi.group(1), re.M))


def test_g_erd_2_moi_bang_trong_code_deu_co_tren_ERD_BA():
    """Chieu 1: them bang ma quen ve len ERD => do."""
    thieu = set(TABLES) - _entity_trong_doc_BA()
    assert not thieu, f"bang co trong code nhung VANG tren ERD cua BA: {sorted(thieu)}"


def test_g_erd_2_moi_entity_tren_ERD_BA_deu_ton_tai_trong_code():
    """Chieu 2: ERD ve entity khong co thuc => do."""
    du = _entity_trong_doc_BA() - set(TABLES)
    assert not du, f"entity tren ERD cua BA nhung KHONG co trong code: {sorted(du)}"


def test_g_erd_3_moi_bang_toi_duoc_fls_itl_hoac_khai_island():
    """G-ERD-3: khong co bang mo coi lang le.

    ⚠ 2026-09-07: phep tinh kha-nang-toi chuyen sang `erd_policy.bang_mo_coi()`.
    Cau khang dinh KHONG doi mot chu — no doi cho o vi tu nay co cong CHIEU
    NGUOC doc cung mot phep tinh, va hai ban ma se troi khoi nhau.
    """
    mo_coi = bang_mo_coi(TABLES)
    assert mo_coi <= ERD_ISLANDS, (
        f"bang khong noi voi fls_itl va chua khai island: {sorted(mo_coi - ERD_ISLANDS)}")


def test_g_erd_3_moi_island_phai_co_ly_do_bang_chu():
    for n in ERD_ISLANDS:
        assert TABLES[n].island_reason.strip(), f"{n} khai island nhung khong co ly do"


def test_g_erd_3_khai_island_ma_THUC_TE_noi_duoc_thi_DO():
    """⭐⭐ CHIEU NGUOC — moi 2026-09-07 (`CR#11`).

    ⛔⛔ Cong `G-ERD-3` cu chi hoi MOT chieu: *"co bang nao mo coi ma CHUA khai
    khong?"*. No ⛔ khong bao gio hoi chieu con lai: *"co ten nao DA khai la dao
    ma thuc te da noi duoc roi khong?"* ⇒ mot ngoai le co the **song sot qua ca
    cai ly do sinh ra no**, va ⛔ khong cong nao do.

    Chuyen do vua xay ra that: `fls_source` khai dao voi ly do *"manifest
    pipeline, khong gan dong nao"*. Dung — cho toi khi `fls_khai_cot` ra doi va
    mo duong `fls_itl → fls_run → fls_khai_cot → fls_source`. Neu ⛔ khong co
    cong nay, loi khai **da thoi dung** ay se nam lai trong `ERD_ISLANDS`, va
    ERD sinh ra se ke mot cau sai ve chinh no.

    ⭐ Day la **that chat** mot cong, ⛔ khong phai noi long (`R-A5`): tap hop
      duoc mien tru chi co the NHO di, ⛔ khong to ra.
    """
    mo_coi = bang_mo_coi(TABLES)
    assert mo_coi, "⛔ do duoc 0 thu — cong nay dang xanh vi CHUA DO"
    thua = ERD_ISLANDS - mo_coi
    assert not thua, (
        f"⛔ khai island ma THUC TE noi duoc toi fls_itl: {sorted(thua)}. "
        f"Go ten do khoi ERD_ISLANDS va xoa `island_reason` — mot ngoai le het "
        f"ly do la mot cau da thoi dung.")


def test_cong_CHIEU_NGUOC_that_su_CAN_duoc_fls_source():
    """⛔⛔ Chung minh cong tren **can that**, ⛔ khong xanh vi khong do gi.

    Mot cong moi viet bao gio cung xanh — cau hoi la no xanh vi **DUNG** hay
    xanh vi **CHUA DO**. Bai nay dung lai dung hien truong cua sang 07/09: coi
    nhu `fls_source` van con trong `ERD_ISLANDS`, va doi hoi cong PHAI do.
    """
    islands_cu = ERD_ISLANDS | {"fls_source"}          # ban khai TRUOC `CR#11`
    thua = islands_cu - bang_mo_coi(TABLES)
    assert thua == {"fls_source"}, (
        "⛔ cong chieu nguoc ⛔ KHONG bat duoc `fls_source` — no dang xanh gia. "
        f"do duoc: {sorted(thua)}")


def _bo_bang(bo: set[str]) -> dict:
    """`TABLES` bo mot so bang, **va bo luon canh FK tro toi chung**.

    ⛔ Bo bang ma de canh lai thi phep do noi mot dieu khac: canh tro toi mot
    bang ⛔ khong con van bi `bang_mo_coi` dem nhu mot duong di duoc.
    """
    from fls.db.model import Table

    con = {n: t for n, t in TABLES.items() if n not in bo}
    for n, t in list(con.items()):
        moi = tuple(c for c in t.columns
                    if not (c.fk and c.fk.split(".")[0] in bo))
        if moi != t.columns:
            con[n] = Table(
                name=t.name, kind=t.kind, erd_entity=t.erd_entity,
                island_reason=t.island_reason, view_sql=t.view_sql,
                pk_cols=t.pk_cols, unique_keys=t.unique_keys, columns=moi)
    return con


# ⭐⭐ **Sua 2026-09-08 (`QĐ-ITL-110`) — va no la mot SU THAT DOI, ⛔ khong phai
#    mot cong bi noi long.**
#
# Ban truoc cua bai nay ten la `..._qua_DUNG_duong_khai_cot` va doi hoi: bo
# `fls_khai_cot` thi `fls_source` **phai tro lai la dao**. Cau ay dung cho tan
# 08/09 sang — luc `fls_khai_cot` la duong DUY NHAT.
#
# Migration `0018` mo **duong THU HAI**, va no la mot duong THAT, di bo duoc:
#
#     fls_itl.run_id → fls_run.chup_id → fls_chup ← fls_chup_dong → fls_source
#
# doc ra tieng Viet: *"dong so nay den tu lo nay, lo doc ANH CHUP nay, anh chup
# nay doc NGUON nay"*. ⇒ Cai sai ⛔ khong phai duong moi, ma la **cau khang
# dinh "DUNG mot duong"** trong ten bai cu.
#
# ⛔⛔ **Nen bai nay ⛔ KHONG duoc chi doi thanh "toi duoc la du".** Nhu thi no
#    thanh mot ban sao cua `test_g_erd_3_khai_island_ma_THUC_TE_noi_duoc_thi_DO`
#    va ⛔ khong con canh **LY DO** nua. ⇒ Do **ba** dieu, va dieu thu ba moi
#    la cai can:
#      ⓐ bo `khai_cot` ⇒ **VAN toi duoc** (con lan anh chup);
#      ⓑ bo lan anh chup ⇒ **VAN toi duoc** (con `khai_cot`);
#      ⓒ bo **CA HAI** ⇒ **PHAI tro lai la dao**.
#    Thieu ⓒ thi mot ngay nao do ca hai duong bi go ma cong van xanh.
_LAN_CHUP = {"fls_chup", "fls_chup_nguon", "fls_chup_dong"}


def test_fls_source_toi_fls_itl_qua_HAI_duong_va_CHI_hai_duong_do():
    # ⓐ ⛔ khong con `khai_cot` — lan anh chup con giu duoc lineage.
    assert "fls_source" not in bang_mo_coi(_bo_bang({"fls_khai_cot"})), (
        "⛔ bo `fls_khai_cot` ma `fls_source` thanh dao — vay lan ANH CHUP "
        "⛔ khong noi toi `fls_itl`, tuc `fls_run.chup_id` dut o dau do")

    # ⓑ ⛔ khong con lan anh chup — `khai_cot` con giu duoc lineage.
    assert "fls_source" not in bang_mo_coi(_bo_bang(set(_LAN_CHUP))), (
        "⛔ bo lan anh chup ma `fls_source` thanh dao — duong `khai_cot` da dut")

    # ⓒ ⛔⛔ CAI CAN: bo CA HAI thi no PHAI tro lai la dao.
    assert "fls_source" in bang_mo_coi(_bo_bang(_LAN_CHUP | {"fls_khai_cot"})), (
        "⛔ bo CA `fls_khai_cot` LAN lan anh chup ma `fls_source` VAN toi duoc "
        "fls_itl — vay con mot duong THU BA ma ⛔ khong ai khai, va ca doan ly "
        "do o `erd_policy` sai cho.")


def test_G_ERD_2_doc_BA_THAT_nam_TRONG_repo_va_KHONG_co_nhanh_bo_qua():
    """2026-09-03: bo tai lieu ITL da chuyen vao `docs/ITL/` cua repo nay.

    Truoc do doc BA THAT o repo `FIN-ERP` ngoai working-dir, nen cong phai co
    mot nhanh TUY CHON "khong thay thi bo qua" — mot duong FAIL-OPEN: tren CI
    no luon bo qua, tuc xanh ma khong do thu can do.

    Nay doc o trong repo ⇒ duong dan CHAC CHAN. Test nay khoa hai thu:
      1. `BA_ERD_DOC` phai tro vao `docs/ITL/...` (ban goc), khong phai ban sao;
      2. ⛔ KHONG con nhanh bo qua — file phai TON TAI, khong `skip`.
    """
    import re

    from fls.db import erd_policy
    from fls.db.erd_policy import BA_ERD_DOC

    assert BA_ERD_DOC.parts[-3:] == (
        "ITL", "02_BA", "05_DATA_DICTIONARY_ERD.md")
    assert BA_ERD_DOC.is_file(), (
        f"⛔ {BA_ERD_DOC} khong ton tai. Doc BA phai o TRONG repo tu 03/09; "
        f"neu no bien mat thi cong nay phai DO, khong duoc bo qua.")

    # Duong fail-open cu da go — no khong duoc quay lai trong im lang.
    assert not hasattr(erd_policy, "BA_ERD_DOC_NGOAI"), (
        "⛔ `BA_ERD_DOC_NGOAI` da quay lai. Do la duong bo-qua-neu-khong-thay; "
        "tai lieu nay o TRONG repo nen khong con ly do nao can no.")
    assert not hasattr(erd_policy, "cac_doc_can_dong_bo")

    # Va ERD trong ban goc phai khop hien vat sinh ra.
    khoi = re.compile(r"```mermaid\s*\nerDiagram\n(.*?)```", re.S)
    mmd = (pathlib.Path(__file__).resolve().parents[2]
           / "ERD-CONTRACT.mmd").read_text(encoding="utf-8")
    than = mmd.split("erDiagram\n", 1)[1].strip()
    m = khoi.search(BA_ERD_DOC.read_text(encoding="utf-8"))
    assert m, f"{BA_ERD_DOC} khong co khoi 'mermaid + erDiagram'"
    assert m.group(1).strip() == than, (
        f"ERD trong {BA_ERD_DOC.name} LECH voi ERD sinh ra — "
        f"chay: python tools/sync_erd_doc.py {BA_ERD_DOC}")


def test_ban_sao_ERD_cu_da_bien_mat():
    """`docs/05_DATA_DICTIONARY_ERD.md` ton tai CHI vi ban goc o repo khac.

    Cung mot repo ma giu hai file noi cung mot chuyen la tu tao hai ban su that.
    Neu ai chep no ve, cong nay do.
    """
    cu = pathlib.Path(__file__).resolve().parents[2] / "docs" / "05_DATA_DICTIONARY_ERD.md"
    assert not cu.exists(), (
        f"⛔ {cu} quay lai. Ban goc la `docs/ITL/02_BA/05_DATA_DICTIONARY_ERD.md`; "
        f"ban sao thu hai chi de tao drift.")
