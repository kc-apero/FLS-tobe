# -*- coding: utf-8 -*-
"""`DD-I10` — khuon bang `fls_khai_cot`. Thuan khai bao, ⛔ khong cham PG.

⭐ Bang nay ⛔ KHONG luu du lieu — no luu **CACH DOC** du lieu. Nen cac bai o
   day ⛔ khong kiem "co dong nao khong", ma kiem **khuon co con giu duoc ba
   luat cua `DD-I10` ⓷ hay khong**.
"""
from fls.adapters.sao_ke import SAU_TRUONG
from fls.db.erd_policy import ERD_ISLANDS
from fls.db.schema import CREATE_ORDER, TABLES

_T = "fls_khai_cot"


def _cot(ten_bang: str) -> dict:
    return {c.name: c for c in TABLES[ten_bang].columns}


def test_du_TAM_cot_cua_DD_I10():
    """⛔ Thua mot cot cung la lech spec — bang nay chi co DUNG 8 cot.

    ⭐ `7 → 8` ngay 2026-09-08 (`QĐ-ITL-113`, migration `0019`): them `thu_tu`.
      `cot` noi *doc COT NAO*, `thu_tu` noi *doc THE NAO* — cung ban chat, nen
      cung mot dong, va duoc `version` + `actor` mien phi.
    """
    assert [c.name for c in TABLES[_T].columns] == [
        "khai_id", "source_id", "version", "truong", "cot", "thu_tu",
        "hieu_luc_tu", "actor"]


def test_kieu_va_NOT_NULL_dung_spec():
    c = _cot(_T)
    assert (c["khai_id"].type, c["khai_id"].pk) == ("bigint", True)
    assert (c["source_id"].type, c["source_id"].null) == ("bigint", False)
    assert (c["version"].type, c["version"].null) == ("int", False)
    assert (c["truong"].type, c["truong"].null) == ("text", False)
    assert (c["cot"].type, c["cot"].null) == ("int", False)
    assert (c["hieu_luc_tu"].type, c["hieu_luc_tu"].null) == ("timestamptz", False)
    assert (c["actor"].type, c["actor"].null) == ("text", False)


def test_cot_NULLABLE_phai_TU_GIOI_HAN_bang_mot_CHECK():
    """⛔ Mot ban khai thieu bat cu manh nao ⛔ khong phai ban khai thieu — no
    la ban khai **HONG**. ⇒ ⛔ khong o nao duoc de trong.

    ⛔⛔ **Bai nay tung la `test_moi_cot_deu_NOT_NULL`, va no DO ngay 08/09 khi
       `thu_tu` xuat hien. ⛔ Toi ⛔ KHONG go ten cot ay vao mot danh sach mien
       tru** — mot danh sach mien tru la thu se dai ra tung dot, va den cai
       thu ba thi ⛔ khong ai con nho tien de goc.

    ⭐ Tien de goc VAN DUNG, chi la no gap truong hop dau tien no ⛔ khong luong:
      moi cot truoc day ap cho **moi dong**, con `thu_tu` ap cho **1 dong tren
      6** *(chi `Date`)* ⇒ `NOT NULL` se **buoc phai bia** mot thu tu ngay cho
      `Debit`, va `Debit` thi ⛔ khong co thu tu ngay nao.
      ⛔ Dung cai bay `R-A1` ma `fls_run.khai_id` da roi vao.

    ⇒ Nen luat moi **chat hon**, ⛔ khong long hon: mot cot cho `NULL` thi
      phai **TU GIOI HAN** bang mot `CHECK` khai bao duoc — tuc mien tru phai
      **doi duoc bang mot rang buoc may cuong che**, ⛔ khong bang mot cai ten
      go trong bai test. Cot thu hai muon `NULL` cung phai tra dung gia ay.
    """
    trong = [c for c in TABLES[_T].columns if c.null]
    khong_rang_buoc = [c.name for c in trong if not c.check]
    assert not khong_rang_buoc, (
        "⛔ cot cho phep NULL trong mot BAN KHAI ma ⛔ KHONG co `CHECK` gioi "
        "han: %s" % khong_rang_buoc)
    # ⛔ Va phai CO cai gi de do — mot danh sach rong lam bai nay xanh vinh vien.
    assert [c.name for c in trong] == ["thu_tu"], [c.name for c in trong]


def test_CHECK_cua_thu_tu_neo_vao_CA_HAI_cot__khong_chi_mien_gia_tri():
    """⭐⭐ Ly do that de `thu_tu` xung dang mot `CHECK`, ⛔ khong chi loi van.

    ⛔⛔ Quy uoc cua bo nay *(ghi ngay trong bai
       `test_mien_gia_tri_cua_truong_van_la_SAU_TRUONG…` ben duoi)* la: mien
       gia tri thi **loi van + chan o tang ghi**, ⛔ **khong** `CHECK`. Do
       08/09: ca kho THAT co **0** rang buoc `CHECK` ⇒ quy uoc ay duoc giu
       that, ⛔ khong phai chi noi.

    ⇒ Nen `thu_tu` phai giai thich duoc **vi sao no khac**. Va no khac o mot
      cho do duoc: rang buoc cua no **neo vao GIA TRI CUA MOT COT KHAC**
      (`truong = 'Date'`) — thu ma `work_status`/`src_type` ⛔ khong he can.
      Mot tang ghi co the cuong che dieu do, nhung mot **script sua tay** —
      thu luon xay ra voi kho ke toan — thi ⛔ khong di qua tang ghi.
    """
    c = _cot(_T)["thu_tu"]
    assert c.check, "⛔ `thu_tu` phai co `CHECK`"
    assert "truong" in c.check, (
        "⛔ `CHECK` cua `thu_tu` phai neo vao cot `truong` — neu no chi gioi "
        "han MIEN GIA TRI thi no ⛔ khong khac gi `work_status`, va luc ay quy "
        "uoc *loi van + chan o tang ghi* moi la cai dung")
    for x in ("dmy", "mdy"):
        assert x in c.check, x


def test_source_id_FK_ve_fls_source():
    assert _cot(_T)["source_id"].fk == "fls_source.source_id"


def test_khoa_duy_nhat_CO_version_va_KHONG_co_hieu_luc_tu():
    """⭐⭐ Khoa nay la cho luat ⓐ (CHI-THEM) song, ⛔ khong phai chong go trung.

    ⛔ Bo `version` khoi khoa ⇒ mot nguon chi con giu duoc MOT ban khai trong
       doi ⇒ *"ngan hang doi mau sao ke"* thanh **sua de**, tuc viet lai lich su
       (`INV-I08`). Mot dong nap thang truoc se duoc giai thich bang ban khai
       cua THANG NAY — sai ma ⛔ khong ai thay.
    ⛔ Them `hieu_luc_tu` vao khoa ⇒ khoa **luon duy nhat** (moc thoi gian khong
       lap), tuc rang buoc bien thanh mot cau **luon dung** — mot cong xanh vi
       ⛔ khong do gi, dung hinh dang cong mu ma bo nay chua.
    """
    assert TABLES[_T].unique_keys == (("source_id", "version", "truong"),)


def test_truong_la_TEN_va_cot_la_SO():
    """Luat ⓒ: hai dau **phai nguoc nhau** — neo cung mot kieu la hong mot dau."""
    c = _cot(_T)
    assert c["truong"].type == "text"
    assert c["cot"].type == "int"


def test_mien_gia_tri_cua_truong_van_la_SAU_TRUONG_va_chi_khai_MOT_cho():
    """⛔ Bang nay ⛔ KHONG chep lai 6 ten — no tro ve `sao_ke.SAU_TRUONG`.

    ⚠ **Cau nay da duoc SUA 2026-09-08 — ban cu noi *"ca repo ⛔ khong co lay
      mot `CHECK` nao"*.** Do hom ay: dung, kho THAT co **0** rang buoc
      `CHECK`, va bon cot mien-gia-tri (`work_status` · `period_state` ·
      `src_type` · `evt_type`) van la **loi van + chan o tang ghi**.

    ⭐ Nhung `QĐ-ITL-113` da them **mot** `CHECK`: `fls_khai_cot_thu_tu_ck`.
      Quy uoc ⛔ khong bi bo — no duoc **thu hep**: `CHECK` danh cho rang buoc
      neo vao **gia tri cua mot cot khac**, thu ma loi van ⛔ khong noi duoc voi
      kho. Mien gia tri thuan thi **van** la loi van + tang ghi.
      *(Xem `test_CHECK_cua_thu_tu_neo_vao_CA_HAI_cot…`.)*

    ⇒ Bai nay khoa hai thu: `SAU_TRUONG` van du 6, va loi van cua cot `truong`
      van **tro ve day** — ⛔ khong tu liet ke mot ban sao thu hai.
    """
    assert len(SAU_TRUONG) == 6
    assert "SAU_TRUONG" in _cot(_T)["truong"].comment


def test_fls_run_them_dung_MOT_cot_va_no_NULLABLE():
    """⭐ `R-A1`: lo `NAP-2026-08-27-RAW` co TRUOC bang nay ⇒ ⛔ khong bia
    `khai_id` cho qua khu. NOT NULL o day se **buoc phai bia**."""
    c = _cot("fls_run")["khai_id"]
    assert c.fk == "fls_khai_cot.khai_id"
    assert c.null is True, (
        "⛔ khai_id NOT NULL se buoc phai BIA mot ban khai cho 10.030 dong da "
        "nam trong kho — trai R-A1")


def test_fls_source_THOI_la_dao():
    """⭐⭐ Duong di THAT, di bo duoc:
        fls_itl.run_id → fls_run.khai_id → fls_khai_cot.source_id → fls_source
    ⇒ loi khai dao cu (*"manifest pipeline, khong gan dong nao"*) da thoi dung.
    """
    assert "fls_source" not in ERD_ISLANDS
    assert not TABLES["fls_source"].island_reason, (
        "⛔ fls_source het la dao ma van con `island_reason` — mot cau da thoi dung")


def test_CREATE_ORDER_cha_truoc_con_cho_chuoi_moi():
    i = CREATE_ORDER.index
    assert i("fls_source") < i(_T) < i("fls_run") < i("fls_itl")
