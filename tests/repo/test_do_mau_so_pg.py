"""`B0` — MAU SO + doi chieu hai cau *"chua ghep"*.

⛔⛔ **Bo bai nay ⛔ KHONG kiem "con so co dung khong" — no kiem ba thu ma mot
   phep dem sai **⛔ khong the** di qua:**

  ⓐ **PHU HET.** `Σ bon nhom == count(*)`, va `Σ bon nhom vi_sao == so dong
    chua noi`. Mot phep phan hoach ⛔ khong tu kiem la mot phep phan hoach se
    lech trong im lang — va no lech xuong, nen ⛔ khong ai thay.
  ⓑ **MOI O CO TEN.** Bon o cua bang cheo deu co ly do dat ten duoc, ⛔ khong
    o nao ten *"khac"*. Ghim ca dieu ⛔ khong o nao co ly do RONG.
  ⓒ ⭐⭐ **TU CHUNG = tap ma `ghep_lenh` CHAC CHAN NHAN.** Day la bai dat nhat
    trong tep: no **goi that `ghep_lenh`** len tung dong `tu_chung` va doi
    ⛔ **khong dong nao bi tu choi**. Chinh cong nay bat duoc con so `584` sai
    *(that ra 68)*: mot tap "tu chung" do bang luat cua **danh sach ung vien**
    thi 88% thanh vien cua no bi cua GHI tu choi.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import canon_ref
from fls.db.kho import dsn_test
from fls.repo import do_mau_so as dms
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import chi_nap_that, mot_lan_nap

pytestmark = pytest.mark.pg


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture(scope="module")
def kho():
    """Mot lan nap that voi **du sau hinh** ma `ds_tu_chung` phai phan biet.

    ⛔ Mot tien te RIENG cho moi lan chay ⇒ ⛔ khong dinh du lieu bai khac va
    ⛔ khong bi du lieu bai khac lam lech.
    """
    tt = "M" + _hex(5)
    run = f"NAP-2000-01-01-MAUSO{_hex()}"
    ma = {}
    with psycopg.connect(dsn_test(), autocommit=True) as c, c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))

        def _so(doc_no, tien, *, ps="co", ws="UNMAPPED", te=None):
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
                " source_row, run_id, contract_version, canon_version,"
                " mapping_version, raw_frozen, canon, curr, ps_no, ps_co,"
                " work_status, doc_date, doc_no) VALUES (%s,'RAW','L1',"
                "%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,%s,%s,%s,%s,"
                "'2026-08-01',%s) RETURNING itl_id",
                (uuid.uuid4().hex, cur.rowcount + abs(hash(doc_no or "")) % 90000,
                 run, te or tt,
                 D(tien) if ps == "no" else None,
                 D(tien) if ps == "co" else None, ws, doc_no))
            return cur.fetchone()[0]

        def _pm(ref, tien, *, status="Approve", te=None):
            pid = "PML" + _hex(10)
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                (run, pid, "SLIP" + _hex(6), ref, canon_ref(ref),
                 D(tien), te or tt,
                 status, abs(hash(pid)) % 900000))
            return pid

        # ⓐ TU CHUNG — mot dong PM, cung tien te, da duyet, dung tien
        ma["tu_chung"] = _so("REF-TC-" + _hex(4), 1_000_000)
        cur.execute("SELECT doc_no FROM fls_itl WHERE itl_id=%s",
                    (ma["tu_chung"],))
        ma["pm_tu_chung"] = _pm(cur.fetchone()[0], 1_000_000)

        # ⓑ TU CHUNG theo CHUM — HAI dong PM cung ma, Σ = tien bank
        r2 = "REF-CHUM-" + _hex(4)
        ma["chum"] = _so(r2, 3_000_000)
        ma["pm_chum"] = [_pm(r2, 1_000_000), _pm(r2, 2_000_000)]

        # ⓒ chum lech tien — hai dong, Σ ⛔ khong bang
        r3 = "REF-LECHCHUM-" + _hex(4)
        ma["chum_lech"] = _so(r3, 3_000_000)
        _pm(r3, 1_000_000)
        _pm(r3, 500_000)

        # ⓓ mot dong lech tien
        r4 = "REF-LECH1-" + _hex(4)
        ma["mot_lech"] = _so(r4, 5_000_000)
        _pm(r4, 77)

        # ⓔ chua duyet
        r5 = "REF-CHUADUYET-" + _hex(4)
        ma["chua_duyet"] = _so(r5, 800_000)
        _pm(r5, 800_000, status="Pending")

        # ⓕ khac tien te — dong PM dung tien, nhung tien te KHAC
        r6 = "REF-KHACTE-" + _hex(4)
        ma["khac_te"] = _so(r6, 900_000)
        _pm(r6, 900_000, te="X" + _hex(5))

        # ⓖ PM ⛔ khong mang ma nay
        ma["khong_co_pm"] = _so("REF-VOCHU-" + _hex(4), 111_000)

        # ⓗ ⛔ khong co so chung tu
        ma["khong_doc_no"] = _so(None, 222_000)

        # ⓘ ve `PS No` — de bai mau so co ca hai ve
        ma["ps_no"] = _so("REF-NO-" + _hex(4), 333_000, ps="no")

        # ⓙ nhan `ok` ma CHUA noi — o thu tu cua bang cheo
        ma["ok_chua_noi"] = _so("REF-OK-" + _hex(4), 444_000, ws="ok")
    # ⛔ Tach hai loai khoa: `pm_*` la ma DONG LENH, ⛔ khong phai dong so.
    #    Dem lan hai loai la mot phep dem ⛔ khong ai kiem duoc — va bai
    #    `test_bon_nhom_VE_phu_het_tong` da do dung vi the.
    so_dong_so = sum(1 for k in ma if not k.startswith("pm_"))
    return {"tt": tt, "run": run, "ma": ma, "so_dong_so": so_dong_so}


@pytest.fixture
def c():
    with psycopg.connect(dsn_test(), autocommit=True) as conn:
        yield conn


def _d(c, kho):
    return dms.do_mau_so(c, mot_lan_nap(kho["run"]))


# ── ⓐ PHU HET ───────────────────────────────────────────────────────────
def test_bon_nhom_VE_phu_het_tong(c, kho):
    d = _d(c, kho)
    assert sum(x["so_dong"] for x in d["ve"]) == d["tong_dong"]
    assert d["tong_dong"] == kho["so_dong_so"]


def test_bon_O_bang_cheo_phu_het_tong(c, kho):
    d = _d(c, kho)
    assert sum(x["so_dong"] for x in d["nhan"]) == d["tong_dong"]


def test_bon_nhom_VI_SAO_phu_het_tap_CHUA_NOI(c, kho):
    """⛔ Σ bon nhom `vi_sao` PHAI bang so dong chua noi — ⛔ khong hut mot dong.

    ⚠ Bai nay la thu bat duoc mot nhom bi bo sot: neu ai them mot nhanh
    `continue` moi trong `ds_tu_chung` ma quen dem no, `Σ` se **nho di** va
    ⛔ khong gi khac bao loi.
    """
    d = _d(c, kho)
    chua_noi = sum(x["chua_noi"] for x in d["ve"])
    assert sum(x["so_dong"] for x in d["vi_sao"]) == chua_noi


def test_khong_o_nao_ten_KHAC_va_khong_ly_do_nao_RONG(c, kho):
    d = _d(c, kho)
    for r in d["nhan"] + d["vi_sao"]:
        assert r["ma"] not in ("khac", "other", ""), r
        assert r["ly_do"].strip(), r
    for k, v in dms.LY_DO_KHONG_TU_CHUNG.items():
        assert v.strip(), k


# ── ⓑ hai nhom NGUOC CHIEU cua "lech 353" ───────────────────────────────
def test_LECH_la_HIEU_cua_hai_nhom_nguoc_chieu(c, kho):
    """⭐⭐ Cau tra loi cua `B0`: `353` la mot **HIEU**, ⛔ khong phai mot nhom.

    Kho bai co **1** dong `ok` ma chua noi, va **0** dong da noi. Nen hieu la
    **-1** trong khi tong dong bi che la **1**: mot con so hieu co the **am**,
    co the **bang 0** trong khi hai nhom deu lon — do la ly do no ⛔ khong dung
    de ai theo doi.
    """
    d = _d(c, kho)
    L = d["lech"]
    assert L["du_phan_loai__chua_noi"] == 1
    assert L["da_noi__nhan_con_UNMAPPED"] == 0
    assert L["hieu_hai_phep_dem"] == -1
    assert L["tong_dong_bi_che"] == 1
    assert "KHONG phai mau thuan" in L["ket_luan"]


def test_MAU_SO_tach_theo_VE_va_khong_gop_hai_ve(c, kho):
    d = _d(c, kho)
    ve = {x["ve"]: x for x in d["ve"]}
    assert ve["ps_no"]["so_dong"] == 1
    assert ve["ps_co"]["so_dong"] == d["tong_dong"] - 1
    # ⛔ Hai ve rong PHAI co mat, va ty le cua chung la `None` ⛔ khong phai `0`
    assert ve["ca_hai"]["so_dong"] == 0
    assert ve["ca_hai"]["ty_le_noi_pct"] is None


# ── ⓒ TU CHUNG = tap `ghep_lenh` CHAC CHAN NHAN ─────────────────────────
def test_TU_CHUNG_bat_dung_hai_hinh_va_loai_dung_bon_hinh(c, kho):
    d = dms.ds_tu_chung(c, mot_lan_nap(kho["run"]))
    m = kho["ma"]
    assert set(d["tu_chung"]) == {m["tu_chung"], m["chum"]}
    assert d["tu_chung"][m["chum"]] == sorted(m["pm_chum"])
    assert d["khong"][m["chum_lech"]] == "chum_lech_tien"
    assert d["khong"][m["mot_lech"]] == "mot_dong_lech_tien"
    assert d["khong"][m["chua_duyet"]] == "co_dong_chua_duyet"
    assert d["khong"][m["khac_te"]] == "khac_tien_te"
    # hai dong nay ⛔ khong co ma / ⛔ khong co PM ⇒ chung o `vi_sao`, ⛔ khong o `khong`
    assert m["khong_co_pm"] not in d["khong"]
    assert m["khong_doc_no"] not in d["khong"]


def test_CHUM_lay_CA_CHUM_chu_KHONG_chon_mot_tap_con(c, kho):
    """⛔⛔ Ba dong cung ma, hai trong ba cong dung tien bank ⇒ **TU CHOI**.

    Neu may chon duoc tap con thi no dang **quyet dinh ho ke toan** dong lenh
    nao da duoc tra — mot quyet dinh nghiep vu, ⛔ khong phai mot phep tinh.
    """
    r = "REF-TAPCON-" + _hex(4)
    with c.cursor() as cur:
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
            " doc_date, doc_no) VALUES (%s,'RAW','L1',991001,%s,'v1.0','v1.0',"
            "'v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED','2026-08-01',%s)"
            " RETURNING itl_id",
            (uuid.uuid4().hex, kho["run"], kho["tt"], D(3_000_000), r))
        i = cur.fetchone()[0]
        for n, tien in enumerate((1_000_000, 2_000_000, 7_000_000)):
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',%s)",
                (kho["run"], "PMS" + _hex(10), "SLIP" + _hex(6), r,
                 canon_ref(r), D(tien), kho["tt"], 991100 + n))
    try:
        d = dms.ds_tu_chung(c, mot_lan_nap(kho["run"]))
        assert i not in d["tu_chung"]
        assert d["khong"][i] == "chum_lech_tien"
    finally:
        with c.cursor() as cur:
            cur.execute("DELETE FROM fls_pm_line WHERE run_id=%s"
                        " AND ref_canon=%s", (kho["run"], r))
            cur.execute("DELETE FROM fls_itl WHERE itl_id=%s", (i,))


def test_GHEP_LENH_that_NHAN_moi_dong_TU_CHUNG(c, kho):
    """⭐⭐⭐ Bai dat nhat: goi **`ghep_lenh` THAT** len tung dong `tu_chung`.

    ⛔⛔ **Vi sao no khong the thay bang mot bai gia lap.** Tap `tu_chung` chi
    co gia tri neu cua ghi **chac chan nhan** no — do la ca ly do cua ghep LO
    duoc phep bo qua buoc *"nguoi chon"*. Mot bai gia lap se kiem lai **luat
    cua toi**, ⛔ khong kiem luat cua **cua ghi** — va do dung la cai da de ra
    con so `584`: 88% thanh vien cua tap ay bi cua ghi tu choi.
    """
    # ⛔⛔ Bai nay dung mot LAN NAP RIENG, ⛔ khong dung kho cua module.
    #
    # ⚠ Vi sao: no **GHEP THAT**, nen sau khi chay thi hai dong tu chung cua
    # kho module ⛔ khong con tu chung nua — va bai
    # `test_TU_CHUNG_bat_dung_hai_hinh...` se do **neu no chay sau**. Da chung
    # minh: chay hai bai theo thu tu do ⇒ `set() == {1, 2}` do. Mot bo test ma
    # ket qua **doi theo thu tu chay** la mot bo test ⛔ khong do gi on dinh.
    tt = "G" + _hex(5)
    run = f"NAP-2000-01-01-GHEP{_hex()}"
    pv = mot_lan_nap(run)
    r1, r2 = "REF-G1-" + _hex(4), "REF-G2-" + _hex(4)
    with c.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        for n, (ref, tien) in enumerate(((r1, 1_000_000), (r2, 3_000_000))):
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
                " source_row, run_id, contract_version, canon_version,"
                " mapping_version, raw_frozen, canon, curr, ps_co,"
                " work_status, doc_date, doc_no) VALUES (%s,'RAW','L1',%s,%s,"
                "'v1.0','v1.0','v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED',"
                "'2026-08-01',%s)", (uuid.uuid4().hex, 700 + n, run, tt,
                                     D(tien), ref))
        # `r1` mot dong · `r2` HAI dong cong lai ⇒ ca hai hinh tu chung
        for n, (ref, tien) in enumerate(
                ((r1, 1_000_000), (r2, 1_000_000), (r2, 2_000_000))):
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row)"
                " VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',%s)",
                (run, "PMG" + _hex(10), "SLIP" + _hex(6), ref, canon_ref(ref),
                 D(tien), tt, 700 + n))

    d = dms.ds_tu_chung(c, pv)
    assert len(d["tu_chung"]) == 2, "⛔ kho bai sai — bai se vo nghia"
    assert sorted(len(v) for v in d["tu_chung"].values()) == [1, 2]
    for i, ds in sorted(d["tu_chung"].items()):
        kq = gt.ghep_lenh(c, pv, i, ds, actor="bai-B0",
                          reason="bai kiem: tap tu chung PHAI duoc nhan")
        assert [x["pm_line_id"] for x in kq["moi_noi"]] == list(ds)
    # sau khi ghep, chung ⛔ khong con trong tap chua noi ⇒ `tu_chung` RONG
    assert dms.ds_tu_chung(c, pv)["tu_chung"] == {}


def test_ds_tu_chung_KHAI_dong_NGOAI_tap_chua_noi(c, kho):
    """Nguoi goi dua `itl_id` ⛔ khong nam trong tap chua noi ⇒ vao `ngoai`.

    ⛔ ⛔ Khong im lang bo qua: cua ghep LO phai **tu choi ca lo** khi thay
    `ngoai`, va no chi lam duoc dieu do neu phep do **khai ra**.
    """
    d = dms.ds_tu_chung(c, mot_lan_nap(kho["run"]), itl_ids=[10**15])
    assert d["ngoai"] == [10**15]
    assert d["tu_chung"] == {}


def test_pham_vi_KHAC_lan_nap_tra_tap_RONG(c, kho):
    """⛔ Pham vi ⛔ khong co mac dinh, va no phai **thuc su loc**."""
    d = dms.ds_tu_chung(c, mot_lan_nap("NAP-1999-12-31-KHONGCO"))
    assert d["tu_chung"] == {} and d["so_dong_xet"] == 0


def test_ban_TRANG_KHONG_thay_dau_test(c, kho):
    """Kho bai dung `run_id` hinh THAT nen no **co** trong ban trang — bai nay
    ghim rang phep do di qua pham vi, ⛔ khong doc ca kho.
    """
    d = dms.do_mau_so(c, chi_nap_that())
    assert d["pham_vi"] == "chi lan nap that"
    assert d["tong_dong"] >= kho["so_dong_so"]


# ── ⭐⭐⭐ TRAN CUNG (`B1`, 09/09) ───────────────────────────────────────
#
# ⛔⛔⛔ **Vi sao khoi bai nay dat: `tran` la con so DUY NHAT lam cau
#    *"do phu 31,1%"* co nghia — va no rat de sai theo huong NOI QUA.**
#
# Mot dong lenh chi da ghep cho dong tien nay thi ⛔ khong ghep lai cho dong
# khac. Nen so dong tien co the noi them bi chan boi so dong lenh **CON RANH**
# trong **mot** anh chup. ⇒ Hai cach lam `tran` **cao gap doi su thuc**:
#   ⓐ ⛔ khong loc anh ⇒ cong ca hai anh *(3.703 + 3.772)*;
#   ⓑ dem ca dong lenh **da bi dung** ⇒ hua lai mot thu da tieu.
def test_tran_do_tren_ANH_HIEU_LUC__khong_cong_ca_hai_anh(c, kho):
    """⭐⭐⭐ **Bai dat nhat cua `B1`.**

    Dung mot anh lenh chi **THU HAI** mang **cung** cac ma tham chieu. Neu
    `_SQL_TRAN` ⛔ khong loc `run_id` thi `dong_lenh_trong_anh` se **cong ca
    hai anh** va tran phong len — mot con so **noi qua** ve viec con lam duoc
    bao nhieu, tuc dung huong nguy hiem. *(Da dien tap: pha phep loc ⇒ bai nay
    do voi dung cau `tran do tren 16 dong trong khi anh hieu luc chi co 8`.)*

    ⛔ Va no ⛔ khong phai mot lo xa: `QĐ-ITL-119` ghi ro phep loc dong lenh
      **truoc kia duoc `PhamVi` bao ve NGAM** *(no bam `i.run_id`)*; tu khi no
      **tu chon** mot anh thi cai bao ve ngam ay **⛔ khong con**.

    ⛔⛔ **VA BAI NAY PHAI TU DON — no da lam DO 19 BAI KHAC mot lan.**
       Ban dau toi dat `read_at = now() + interval '1 hour'`, va vi **kho test
       dung CHUNG**, anh gia ay thanh **anh HIEU LUC cua ca kho** ⇒ moi bai
       `ghep_lenh`/`nap_anh_pm`/`vong_f01` dung pham vi rong hon bong nhien
       ghep vao mot anh ⛔ khong phai cua no. ⇒ Hai luat: `read_at` dat **that
       xa ve QUA KHU** *(⛔ khong the thang cuoc lam anh hieu luc)*, va **xoa
       sach trong `finally`**.
    """
    run2 = f"NAP-2000-01-02-MAUSO2{_hex()}"
    try:
        with psycopg.connect(dsn_test(), autocommit=True) as cc,                 cc.cursor() as cur:
            cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                        " canon_version, mapping_version)"
                        " VALUES (%s,'v1.0','v1.0','v1.0')", (run2,))
            cur.execute(
                "SELECT ref_tho, amount FROM fls_pm_line WHERE run_id=%s",
                (kho["run"],))
            # ⚠ `source_row` phai DUY NHAT trong mot anh, va hai dong cua
            #   nhom "chum" mang **cung** mot `ref` ⇒ bam theo `ref` se trung.
            for i, (ref, tien) in enumerate(cur.fetchall()):
                cur.execute(
                    "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                    " ref_tho, ref_canon, amount, curr, status, source_row,"
                    " read_at) VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',%s,"
                    " '1999-01-01T00:00:00+00'::timestamptz)",
                    (run2, "PML" + _hex(10), "SLIP" + _hex(6), ref,
                     canon_ref(ref), tien, kho["tt"], 700000 + i))
            n1 = cur.execute(
                "SELECT count(*) FROM fls_pm_line WHERE run_id=%s",
                (kho["run"],)).fetchone()[0]
            n2 = cur.execute(
                "SELECT count(*) FROM fls_pm_line WHERE run_id=%s",
                (run2,)).fetchone()[0]
        assert n2 == n1 > 0, "bai nay chi co nghia khi anh thu hai co dong"

        t = _d(c, kho)["tran"]
        assert t["anh_pm"] == kho["run"], (
            "⛔ pham vi `mot_lan_nap` phai giu phep do trong DUNG anh cua no")
        assert t["dong_lenh_trong_anh"] == n1, (
            f"⛔⛔ tran do tren {t['dong_lenh_trong_anh']} dong trong khi anh "
            f"hieu luc chi co {n1} — no dang CONG CA HAI ANH ({n1} + {n2})")
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as cc:
            cc.execute("DELETE FROM fls_pm_line WHERE run_id=%s", (run2,))
            cc.execute("DELETE FROM fls_run WHERE run_id=%s", (run2,))


def test_dong_lenh_DA_DUNG_khong_duoc_tinh_la_CON_RANH(c, kho):
    """⛔ Mot dong lenh da ghep la nguyen lieu **da tieu**. Dem no vao *"con
    ranh"* la hua lai mot thu da dung — va tran se noi QUA."""
    t = _d(c, kho)["tran"]
    assert (t["dong_lenh_con_ranh"]
            == t["dong_lenh_trong_anh"] - t["dong_lenh_da_dung"])
    assert t["dong_lenh_da_dung"] >= 0
    assert t["dong_lenh_con_ranh"] <= t["dong_lenh_trong_anh"]


def test_tran_bang_DA_NOI_cong_CON_RANH__va_hai_ty_le_khop(c, kho):
    """Hai ty le phai **suy ra duoc** tu bon con so — ⛔ khong tinh doc lap.

    ⛔ Neu chung duoc tinh o hai cho thi mot cho doi ma cho kia dung yen, va
      man hinh se in `tran 47,4%` canh `phu tren tran 65,6%` **⛔ khong cong
      duoc lai voi nhau**.
    """
    d = _d(c, kho)
    t, ps = d["tran"], next(x for x in d["ve"] if x["ve"] == "ps_co")
    assert t["toi_da_noi_duoc"] == ps["da_noi"] + t["dong_lenh_con_ranh"]
    assert t["tran_pct"] == dms._pct(t["toi_da_noi_duoc"], ps["so_dong"])
    assert t["phu_tren_tran_pct"] == dms._pct(ps["da_noi"],
                                              t["toi_da_noi_duoc"])
    # ⭐ Tran ⛔ khong the nho hon so da noi — no **chua** so da noi
    assert t["toi_da_noi_duoc"] >= ps["da_noi"]


def test_KHONG_co_anh_lenh_chi_thi_ty_le_la_NONE_chu_khong_0(c):
    """⛔⛔ `0%` la mot cau tra loi **SAI** cho mot cau hoi ⛔ khong do duoc.

    Mot lan nap ⛔ khong co dong lenh nao ⇒ *"da noi bao nhieu phan tram cua
    tran"* ⛔ **khong co nghia**. In `0%` o day noi rang *"chua lam gi"*,
    trong khi su that la *"⛔ khong co nguyen lieu de lam"* — hai cau **khac
    nhau**, va man hinh phai ve chung **khac nhau**.
    """
    run = f"NAP-2000-01-03-KHONGPM{_hex()}"
    with psycopg.connect(dsn_test(), autocommit=True) as cc, cc.cursor() as cur:
        cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                    " canon_version, mapping_version)"
                    " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        cur.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, curr, ps_co, work_status,"
            " doc_date, doc_no) VALUES (%s,'RAW','L1',1,%s,'v1.0','v1.0',"
            "'v1.0',false,'{}'::jsonb,%s,%s,'UNMAPPED','2026-08-01',%s)",
            (uuid.uuid4().hex, run, "Z" + _hex(5), D(500), "REF-" + _hex(4)))

    t = dms.do_mau_so(c, mot_lan_nap(run))["tran"]
    assert t["anh_pm"] is None
    assert t["dong_lenh_trong_anh"] == 0 and t["dong_lenh_con_ranh"] == 0
    assert t["toi_da_noi_duoc"] == 0
    assert t["phu_tren_tran_pct"] is None, (
        "⛔ `0%` noi *'chua lam gi'*; su that la *'⛔ khong co nguyen lieu'*")


def test_ket_luan_cua_tran_NOI_RO_no_la_GIOI_HAN_chu_khong_MUC_TIEU(c, kho):
    """⛔⛔ Mot con so tran ⛔ khong kem cau giai thich se bi doc thanh **muc
    tieu** — va roi ai do se di *"toi uu"* cho no len 100%, tuc di ghep bua.

    ⇒ Ghim rang loi khai co **ca hai** y: no do **so dong lenh TON TAI** dat
      ra, va `toi_da` gia dinh `1:1` nen thuc te **con thap hon**.
    """
    k = _d(c, kho)["tran"]["ket_luan"]
    assert "TON TAI" in k
    assert "1:1" in k and "THAP HON" in k


# ── ⭐⭐⭐ DO PHU PHIA PM (`QĐ-ITL-122`, 09/09) ──────────────────────────
#
# ⛔⛔⛔ **Owner doi CHIEU do:** *"Trans map vao PM (so luong Trans von nhieu
#    hon PM; ⛔ ko can question cac Trans khong duoc map)"*. ⇒ Mau so la so
#    **DONG LENH CHI**, ⛔ khong phai so dong tien — va moi con so do phu tu
#    27/08 den 09/09 do **SAI PHIA**.
def test_mau_so_la_so_DONG_LENH__khong_phai_so_dong_TIEN(c, kho):
    """⭐ Bai neo lai chinh cai chieu do: mau so la so DONG LENH.

    ⛔⛔ **Va so ay phai ĐO, ⛔ khong go tay.** Ban dau toi go `8` — dem tay
       so lan goi `_pm` trong `kho`. Thuc te la **11**: mot bai KHAC trong
       chinh tep nay *(`REF-TAPCON`)* cung them dong lenh vao `kho["run"]`,
       nen mot con so go tay o day **phu thuoc THU TU chay bai**. Do lai bang
       mot cau doc lap thi no dung du ai them bao nhieu.
    """
    d = dms.do_phu_pm(c, mot_lan_nap(kho["run"]))
    that = c.execute("SELECT count(*) FROM fls_pm_line WHERE run_id = %s",
                     (kho["run"],)).fetchone()[0]
    assert d["dong_lenh"] == that, (
        f"⛔ mau so phai la so DONG LENH ({that}) — do duoc {d['dong_lenh']}")
    assert d["dong_lenh"] != kho["so_dong_so"], (
        f"⛔⛔ mau so dang bang so DONG TIEN ({kho['so_dong_so']}) — do la "
        f"phia SAI (`QĐ-ITL-122`)")
    assert d["chua_co_tien"] == d["dong_lenh"] - d["da_co_tien"]
    assert d["ty_le_pct"] == dms._pct(d["da_co_tien"], d["dong_lenh"])


def test_phieu_dem_DISTINCT__mot_phieu_nhieu_dong_van_la_MOT(c, kho):
    """⛔ *"526 phieu mang 2–36 reference khac nhau"* (`CR#6`) ⇒ dem DONG va
    dem PHIEU la **hai con so**, va man hinh phai noi duoc ca hai."""
    d = dms.do_phu_pm(c, mot_lan_nap(kho["run"]))
    assert d["phieu"] <= d["dong_lenh"]
    assert d["phieu_chua_noi_gi"] == d["phieu"] - d["phieu_da_co"]


def test_BA_con_so_PHIEU_tra_loi_BA_cau_HOI_khac_nhau(c, kho):
    """⭐⭐⭐ **Bai nay sinh ra tu mot loi cua toi, va loi ay da vao BON tep
    tai lieu truoc khi bi bat.**

    Toi viet **`510`** voi nhan *"viec con lai theo phieu"*. Nhung `510` la
    *"phieu ⛔ CHUA NOI GI CA"*; *"viec con lai"* phai la **`698`** — phieu
    **con it nhat mot dong chua noi**. Chenh **`188`** phieu **da noi mot
    phan**, va do dung la loai phieu **de bo sot nhat**: no ⛔ khong con nam
    trong nhom *"chua lam gi"* ma cung ⛔ chua xong.

    ⇒ Bai nay ghim **bat dang thuc** giua ba con so, nen mot ngay nao do ai
      gan lai chung cho nhau thi no DO.
    """
    d = dms.do_phu_pm(c, mot_lan_nap(kho["run"]))
    assert d["phieu_da_co"] + d["phieu_chua_noi_gi"] == d["phieu"]
    assert (d["phieu_mot_nua"]
            == d["phieu_da_co"] + d["phieu_con_dong_chua"] - d["phieu"])
    assert d["phieu_mot_nua"] >= 0
    # ⛔ *"con dong chua noi"* PHAI >= *"chua noi gi ca"* — no CHUA nhom kia
    assert d["phieu_con_dong_chua"] >= d["phieu_chua_noi_gi"]


def test_dong_CHUA_DUYET_duoc_TACH_RA_khoi_viec_con_lai(c, kho):
    """⛔⛔ `status` ⛔ khong phai `Approve` ⇒ `ghep_lenh` doi `force` kem ly do
    ⇒ **⛔ khong phai viec cua ke toan ITL**. Gop no vao *"viec con lai"* la
    dua cho ke toan mot danh sach ho ⛔ khong lam duoc gi voi no."""
    d = dms.do_phu_pm(c, mot_lan_nap(kho["run"]))
    assert d["chua_co_va_chua_duyet"] >= 1
    assert d["chua_co_va_chua_duyet"] <= d["chua_co_tien"]


def test_ghep_duoc_ngay_dung_CANON_REF__khong_dung_regexp_SQL(c):
    """⭐⭐⭐ **Bai dat nhat cua `QĐ-ITL-122`.**

    Ma ITL ⛔ **khong** co ban chuan hoa trong kho — chi co `doc_no` **tho**.
    Nen mot cau `regexp_replace(doc_no,'[^A-Za-z0-9]','','g')` trong SQL la
    **ban thu hai** cua `canon_ref`, va no ⛔ **khong tuong duong**:
    `canon_ref` con go **ky hieu khoa hoc** *(`4.36619E+15`)*, chuan hoa
    `NFKC`, va loai **o loi** *(`#N/A`)*.

    ⛔⛔ Bai nay dung dung mot so chung tu dang khoa hoc:
      · `canon_ref('4.36619E+15')` -> `4366190000000000` ⇒ **KHOP**
      · mot `regexp` tu dung      -> `436619E15`        ⇒ **TRUOT**
    ⇒ Neu ai doi phep giao sang SQL, bai nay DO.

    ⭐ Va no ⛔ khong phai gia thuyet: toi **da in ra** con so `560` do bang
      mot cau SQL tu dung hom 09/09; luat THAT cho **475** — lech **17,9%**.
    """
    import re as _re

    tt = "K" + _hex(5)
    run = f"NAP-2000-01-04-CANON{_hex()}"
    tho_itl = "4.36619E+15"
    ma = canon_ref(tho_itl)
    assert ma == "4366190000000000", ma
    assert _re.sub(r"[^A-Za-z0-9]", "", tho_itl).upper() != ma, (
        "bai nay chi co nghia khi hai luat cho KET QUA KHAC nhau")
    try:
        with psycopg.connect(dsn_test(), autocommit=True) as cc, \
                cc.cursor() as cur:
            cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                        " canon_version, mapping_version)"
                        " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
            cur.execute(
                "INSERT INTO fls_itl (content_key, source_system,"
                " source_sheet, source_row, run_id, contract_version,"
                " canon_version, mapping_version, raw_frozen, canon, curr,"
                " ps_co, work_status, doc_date, doc_no) VALUES (%s,'RAW','L1',"
                "1,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,%s,%s,"
                "'UNMAPPED','2026-08-01',%s)",
                (uuid.uuid4().hex, run, tt, D(700), tho_itl))
            cur.execute(
                "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                " ref_tho, ref_canon, amount, curr, status, source_row,"
                " read_at) VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',1,"
                " '1999-01-01T00:00:00+00'::timestamptz)",
                (run, "PML" + _hex(10), "SLIP" + _hex(6),
                 "4366190000000000", ma, D(700), tt))

        d = dms.do_phu_pm(c, mot_lan_nap(run))
        assert d["dong_lenh"] == 1 and d["chua_co_tien"] == 1
        assert d["ghep_duoc_ngay"] == 1, (
            "⛔⛔ phep giao dang dung mot luat KHAC `canon_ref` — mot so chung "
            "tu dang khoa hoc vua bi truot")
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as cc:
            cc.execute("DELETE FROM fls_pm_line WHERE run_id=%s", (run,))
            cc.execute("DELETE FROM fls_itl WHERE run_id=%s", (run,))
            cc.execute("DELETE FROM fls_run WHERE run_id=%s", (run,))


def test_do_phu_pm_do_tren_ANH_HIEU_LUC__khong_cong_ca_hai_anh(c, kho):
    """⛔ Cung hiem hoa nhu `tran`: mot anh thu hai lam mau so **gap doi**, va
    con so se noi rang con **nhieu viec hon** su thuc."""
    run2 = f"NAP-2000-01-05-PMPHU{_hex()}"
    n1 = c.execute("SELECT count(*) FROM fls_pm_line WHERE run_id = %s",
                   (kho["run"],)).fetchone()[0]
    try:
        with psycopg.connect(dsn_test(), autocommit=True) as cc, \
                cc.cursor() as cur:
            cur.execute("INSERT INTO fls_run (run_id, contract_version,"
                        " canon_version, mapping_version)"
                        " VALUES (%s,'v1.0','v1.0','v1.0')", (run2,))
            cur.execute("SELECT ref_tho, amount FROM fls_pm_line"
                        " WHERE run_id=%s", (kho["run"],))
            for i, (ref, tien) in enumerate(cur.fetchall()):
                cur.execute(
                    "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id,"
                    " ref_tho, ref_canon, amount, curr, status, source_row,"
                    " read_at) VALUES (%s,%s,%s,%s,%s,%s,%s,'Approve',%s,"
                    " '1999-01-01T00:00:00+00'::timestamptz)",
                    (run2, "PML" + _hex(10), "SLIP" + _hex(6), ref,
                     canon_ref(ref), tien, kho["tt"], 800000 + i))
        d = dms.do_phu_pm(c, mot_lan_nap(kho["run"]))
        assert d["anh_pm"] == kho["run"]
        assert d["dong_lenh"] == n1, (
            f"⛔⛔ mau so {d['dong_lenh']} trong khi anh hieu luc chi co {n1}"
            f" — dang CONG CA HAI ANH")
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as cc:
            cc.execute("DELETE FROM fls_pm_line WHERE run_id=%s", (run2,))
            cc.execute("DELETE FROM fls_run WHERE run_id=%s", (run2,))


def test_KHONG_co_dong_lenh_nao_thi_ty_le_la_NONE_chu_khong_0(c):
    """⛔ `0%` noi *"chua ghep duoc gi"*; su that la *"⛔ khong co lenh chi nao
    trong anh"* — hai cau khac nhau, va man hinh phai ve chung khac nhau."""
    run = f"NAP-2000-01-06-RONG{_hex()}"
    try:
        with psycopg.connect(dsn_test(), autocommit=True) as cc:
            cc.execute("INSERT INTO fls_run (run_id, contract_version,"
                       " canon_version, mapping_version)"
                       " VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
        d = dms.do_phu_pm(c, mot_lan_nap(run))
        assert d["anh_pm"] is None and d["dong_lenh"] == 0
        assert d["ty_le_pct"] is None and d["ty_le_phieu_pct"] is None
    finally:
        with psycopg.connect(dsn_test(), autocommit=True) as cc:
            cc.execute("DELETE FROM fls_run WHERE run_id=%s", (run,))


def test_tien_te_KHONG_gop_thanh_mot_dong_TONG(c, kho):
    """⛔ Cong hai don vi tien ra mot con so la cai sai da de ra *"310 dong phu
    90%"* (that ra **799**). ⇒ ⛔ khong dong `tong` nao, va Σ phai khop."""
    d = dms.do_phu_pm(c, mot_lan_nap(kho["run"]))
    te = [r["te"] for r in d["chua_co_tien_theo_te"]]
    assert te and all(t.lower() not in ("tong", "total", "all") for t in te)
    assert (sum(r["so_dong"] for r in d["chua_co_tien_theo_te"])
            == d["chua_co_tien"])
