"""Tang GHI cua `P5`. ⛔ Moi bai o day canh mot luat, khong phai mot tinh nang.

★ Bai quan trong nhat: `test_khong_mot_cot_nao_cua_fls_itl_bi_doi` va
`test_but_toan_va_nhat_ky_cung_MOT_giao_dich`.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import ghi_tay as gt
from fls.repo.pham_vi import ca_kho, chi_nap_that, mot_lan_nap

pytestmark = pytest.mark.pg

AI = "ke.toan@apero.vn"


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


def _run(cur, that: bool = True) -> str:
    r = f"NAP-2000-01-01-GHI{_hex()}" if that else f"T-{uuid.uuid4().hex[:8]}"
    cur.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong(cur, run: str, **cot) -> int:
    """Mot dong so. `cot` cho phep dat san `hd`, `hd_thyt`, `period_state`…"""
    co = {"content_key": uuid.uuid4().hex, "source_system": "RAW",
          "source_sheet": "L1", "source_row": 1, "run_id": run,
          "contract_version": "v1.0", "canon_version": "v1.0",
          "mapping_version": "v1.0", "raw_frozen": False, "canon": "{}",
          "curr": "VND", "ps_co": D("1000"), "work_status": "UNMAPPED"}
    co.update(cot)
    ten = ", ".join(co)
    cur.execute(f"INSERT INTO fls_itl ({ten}) VALUES ("
                + ", ".join(["%s"] * len(co)) + ") RETURNING itl_id",
                list(co.values()))
    return cur.fetchone()[0]


@pytest.fixture()
def lat(conn):
    with conn.cursor() as cur:
        r = _run(cur)
        return {
            "run": r,
            "trong": _dong(cur, r),                          # hd NULL = UNMAPPED
            "co_nguon": _dong(cur, r, hd="HD-NGUON"),        # so goc da co hd
            "co_may": _dong(cur, r, hd_thyt="HD-MAY"),       # chi co goi y may
            "chot": _dong(cur, r, period_state="locked"),
            "la": _dong(cur, _run(cur, that=False)),
        }


def _dem(conn, bang: str, itl_id: int) -> int:
    return conn.execute(f"select count(*) from {bang} where itl_id=%s",
                        (itl_id,)).fetchone()[0]


# ── luat 1: ⛔ khong cot nao cua so bi doi ────────────────────────────────
def test_khong_mot_cot_nao_cua_fls_itl_bi_doi(conn, lat):
    """⛔⛔ `INV-I08` + `QĐ-ITL-35`.

    `BA-07` §3 viet *"truong hop-dong cap nhat `*_thyt`"*. Lam the la sai HAI
    luat: ⓐ so la append-only ⓑ `*_thyt` la cot DO PARITY, ghi gia tri nguoi go
    vao do la **bo ban tay vao cai thuoc**. Bai nay khoa ca hai: sau khi nguoi
    go, **khong o nao cua `fls_itl` doi**.
    """
    i = lat["co_nguon"]
    truoc = conn.execute(
        "select hd, hd_thyt, pay_type, cdt1, id_payee, invoice, work_status,"
        " period_state from fls_itl where itl_id=%s", (i,)).fetchone()
    gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), i, "hd", "HD-NGUOI-GO",
                    actor=AI, reason="nguon sai, doi chieu hoa don", force=True)
    sau = conn.execute(
        "select hd, hd_thyt, pay_type, cdt1, id_payee, invoice, work_status,"
        " period_state from fls_itl where itl_id=%s", (i,)).fetchone()
    assert truoc == sau, "co o trong fls_itl bi doi"
    # Nhung gia tri hieu luc DA doi:
    t = gt.truoc_khi_go(conn, mot_lan_nap(lat["run"]), i, "hd")
    assert t["gia_tri"] == "HD-NGUOI-GO" and t["value_source"] == gt.NGUON_TAY
    assert t["nguon"] == "HD-NGUON", "gia tri nguon phai con nguyen de doi chieu"


# ── luat 2: but toan + nhat ky la MOT giao dich ──────────────────────────
def test_but_toan_va_nhat_ky_cung_MOT_giao_dich(conn, lat):
    """⛔⛔ Neu hai cau khong cung giao dich thi se co luc kho co but toan ma
    **khong co vet ai lam** — dung lop kiem soat cuoi cung nay dung ra de chan.

    Bai nay dung mot **trigger tam** lam cau ghi nhat ky NO, roi doi hoi but
    toan cung ⛔ khong duoc con lai.
    """
    i = lat["trong"]
    conn.execute("""
        CREATE OR REPLACE FUNCTION thu_no_nhat_ky() RETURNS trigger AS $$
        BEGIN RAISE EXCEPTION 'thu nghiem: nhat ky no'; END $$ LANGUAGE plpgsql""")
    conn.execute("CREATE TRIGGER thu_no BEFORE INSERT ON fls_journal"
                 " FOR EACH ROW EXECUTE FUNCTION thu_no_nhat_ky()")
    try:
        with pytest.raises(psycopg.errors.RaiseException):
            gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), i, "hd", "X",
                            actor=AI, reason="thu")
        assert _dem(conn, "fls_adjustment", i) == 0, (
            "but toan con lai sau khi nhat ky no ⇒ hai cau KHONG cung giao dich")
    finally:
        conn.execute("DROP TRIGGER IF EXISTS thu_no ON fls_journal")
        conn.execute("DROP FUNCTION IF EXISTS thu_no_nhat_ky()")


def test_nhat_ky_du_BAY_truong(conn, lat):
    i = lat["co_nguon"]
    gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), i, "cdt1", "CDT-X",
                    actor=AI, reason="ke toan xac nhan theo hop dong")
    r = conn.execute(
        "select itl_id, field, value_before, value_after, actor, at,"
        " value_source, reason from fls_journal where itl_id=%s", (i,)).fetchone()
    d = dict(zip(("itl_id", "field", "value_before", "value_after", "actor",
                  "at", "value_source", "reason"), r))
    for k in gt.BAY_TRUONG:
        assert d[k] is not None or k == "value_before", f"thieu truong {k}"
    assert d["actor"] == AI and d["reason"]
    assert d["value_source"] == gt.NGUON_TRONG   # cdt1 rong ca ba nguon


# ── luat 3: he KEU khi go khac nguon (US-025) ────────────────────────────
def test_go_khac_NGUON_thi_bi_chan(conn, lat):
    with pytest.raises(gt.KhacNguon) as e:
        gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["co_nguon"], "hd",
                        "HD-KHAC", actor=AI, reason="thu")
    assert e.value.them["khac"]["nguon"] == "HD-NGUON"
    assert e.value.ma == "FLS-CONFLICT-SOURCE"
    assert _dem(conn, "fls_adjustment", lat["co_nguon"]) == 0


def test_go_khac_GOI_Y_MAY_cung_bi_chan(conn, lat):
    with pytest.raises(gt.KhacNguon) as e:
        gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["co_may"], "hd",
                        "HD-KHAC", actor=AI, reason="thu")
    assert e.value.them["khac"]["may_goi_y"] == "HD-MAY"


def test_force_thi_ghi_duoc_va_nhat_ky_giu_gia_tri_CU(conn, lat):
    i = lat["co_nguon"]
    k = gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), i, "hd", "HD-MOI",
                        actor=AI, reason="hoa don xac nhan khac", force=True)
    assert k.adj_id and k.jrn_id
    assert k.value_before == "HD-NGUON" and k.value_source == gt.NGUON_SO


def test_o_TRONG_thi_khong_KEU_va_nguon_ghi_la_UNMAPPED(conn, lat):
    """⛔ `INV-I16`: may khong suy duoc thi nhat ky noi thang **UNMAPPED**,
    ⛔ khong de trong de sau nay ai doc cung tuong la co nguon."""
    k = gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["trong"], "hd",
                        "HD-NGUOI", actor=AI, reason="tra cuu hop dong")
    assert k.value_source == gt.NGUON_TRONG and k.value_before is None


# ── luat 4: ly do BAT BUOC ───────────────────────────────────────────────
@pytest.mark.parametrize("ly_do", ["", "   ", None])
def test_thieu_LY_DO_thi_bi_chan(conn, lat, ly_do):
    with pytest.raises(gt.ThieuLyDo):
        gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["trong"], "hd", "X",
                        actor=AI, reason=ly_do)
    assert _dem(conn, "fls_adjustment", lat["trong"]) == 0


def test_thieu_ACTOR_thi_bi_chan(conn, lat):
    with pytest.raises(gt.LoiGhi, match="actor"):
        gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["trong"], "hd", "X",
                        actor="", reason="co ly do")


# ── luat 5: ban TRANG 10 truong ──────────────────────────────────────────
def test_truong_ngoai_10_thi_bi_chan(conn, lat):
    """⛔ Ten truong di vao cau SQL nen ban trang la **bat buoc**, ⛔ khong phai
    de cho gon."""
    for la in ("run_id", "itl_id", "ps_no", "canon", "hd; drop table fls_itl"):
        with pytest.raises(gt.TruongLa):
            gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["trong"], la,
                            "X", actor=AI, reason="thu")


def test_dung_7_truong_va_dung_hai_nhom():
    """⛔⛔ 10 -> 7 (`QĐ-ITL-64`, 2026-08-28): owner tra loi *"ho ko sua"*.

    Ba truong vung ALLOCATE ra khoi tap nay. Chung la **cong thuc** tren sheet,
    va quyet dinh phan bo nam o `Mapping Master` cot K/L — ⛔ khong o dong so.
    """
    assert len(gt.TRUONG_GHI) == 7
    assert set(gt.TRUONG_HOP_DONG) == {"hd", "pay_type", "cdt1", "svc_start",
                                       "svc_end"}
    assert set(gt.TRUONG_NGOAI) == {"id_payee", "invoice"}
    assert not set(gt.TRUONG_HOP_DONG) & set(gt.TRUONG_NGOAI)


def test_CUA_GHI_TU_CHOI_ba_truong_vung_ALLOCATE(conn, lat):
    """⛔ `QĐ-ITL-64`: ba truong may-suy ⛔ KHONG duoc phep go de len.

    ★ Vi sao phai co bai nay chu khong chi bo ten khoi danh sach: ba truong ay
    **van la cot that** trong `fls_itl`, nen mot cau SQL viet tay van cham
    duoc. Bai nay khoa **cua** — cho duy nhat duoc ghi.
    """
    for f in ("cdt1_cfa1", "cdt1_cfa2", "alloc_method"):
        with pytest.raises(gt.TruongLa):
            gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["trong"], f,
                            "X", actor=AI, reason="thu")


# ── luat 6: pham vi + ky chot ────────────────────────────────────────────
def test_dong_ngoai_pham_vi_thi_khong_ghi_duoc(conn, lat):
    with pytest.raises(gt.NgoaiPhamVi):
        gt.ghi_but_toan(conn, chi_nap_that(), lat["la"], "hd", "X",
                        actor=AI, reason="thu")
    assert _dem(conn, "fls_adjustment", lat["la"]) == 0


def test_ky_DA_CHOT_thi_khong_ghi_duoc_KE_CA_force(conn, lat):
    """`INV-I13`. ⛔ `force` la de ghi de NGUON, ⛔ khong phai de mo ky da chot."""
    for f in (False, True):
        with pytest.raises(gt.KyDaChot):
            gt.ghi_but_toan(conn, mot_lan_nap(lat["run"]), lat["chot"], "hd",
                            "X", actor=AI, reason="thu", force=f)
    assert _dem(conn, "fls_adjustment", lat["chot"]) == 0


# ── luat 7: bam hai lan ⛔ khong thanh hai but toan ──────────────────────
def test_go_lai_CUNG_gia_tri_thi_khong_chen_dong_thu_hai(conn, lat):
    i = lat["trong"]
    pv = mot_lan_nap(lat["run"])
    a = gt.ghi_but_toan(conn, pv, i, "hd", "HD-1", actor=AI, reason="lan dau")
    b = gt.ghi_but_toan(conn, pv, i, "hd", "HD-1", actor=AI, reason="bam lai")
    assert b.da_co is True and b.adj_id == a.adj_id and b.jrn_id is None
    assert _dem(conn, "fls_adjustment", i) == 1


def test_go_gia_tri_KHAC_thi_chen_dong_moi_va_hieu_luc_theo_dong_moi(conn, lat):
    i = lat["trong"]
    pv = mot_lan_nap(lat["run"])
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-1", actor=AI, reason="lan dau")
    gt.ghi_but_toan(conn, pv, i, "hd", "HD-2", actor=AI, reason="sua lai")
    assert _dem(conn, "fls_adjustment", i) == 2
    assert gt.truoc_khi_go(conn, pv, i, "hd")["gia_tri"] == "HD-2"


# ── luat 8: dao but toan = THEM dong ────────────────────────────────────
def test_dao_but_toan_lui_ve_gia_tri_TRUOC_DO(conn, lat):
    i = lat["trong"]
    pv = mot_lan_nap(lat["run"])
    a1 = gt.ghi_but_toan(conn, pv, i, "hd", "HD-1", actor=AI, reason="lan 1")
    a2 = gt.ghi_but_toan(conn, pv, i, "hd", "HD-2", actor=AI, reason="lan 2")
    gt.dao_but_toan(conn, pv, a2.adj_id, actor=AI, reason="go sai")
    assert gt.truoc_khi_go(conn, pv, i, "hd")["gia_tri"] == "HD-1"
    gt.dao_but_toan(conn, pv, a1.adj_id, actor=AI, reason="go sai ca lan 1")
    t = gt.truoc_khi_go(conn, pv, i, "hd")
    assert t["gia_tri"] is None and t["value_source"] == gt.NGUON_TRONG
    # ⛔ Ba but toan + ba ban dao = SAU dong. Khong dong nao bi xoa hay sua.
    assert _dem(conn, "fls_adjustment", i) == 4
    assert conn.execute(
        "select count(*) from fls_adjustment where itl_id=%s and reversal_of"
        " is not null", (i,)).fetchone()[0] == 2


def test_dao_lui_ve_gia_tri_NGUON_neu_khong_con_but_toan(conn, lat):
    i = lat["co_nguon"]
    pv = mot_lan_nap(lat["run"])
    a = gt.ghi_but_toan(conn, pv, i, "hd", "HD-TAY", actor=AI,
                        reason="doi chieu", force=True)
    gt.dao_but_toan(conn, pv, a.adj_id, actor=AI, reason="dao lai")
    t = gt.truoc_khi_go(conn, pv, i, "hd")
    assert t["gia_tri"] == "HD-NGUON" and t["value_source"] == gt.NGUON_SO


def test_dao_HAI_LAN_cung_but_toan_thi_bi_chan(conn, lat):
    pv = mot_lan_nap(lat["run"])
    a = gt.ghi_but_toan(conn, pv, lat["trong"], "hd", "X", actor=AI, reason="r")
    gt.dao_but_toan(conn, pv, a.adj_id, actor=AI, reason="dao")
    with pytest.raises(gt.LoiGhi, match="da bi dao"):
        gt.dao_but_toan(conn, pv, a.adj_id, actor=AI, reason="dao nua")


def test_khong_dao_mot_BAN_DAO(conn, lat):
    pv = mot_lan_nap(lat["run"])
    a = gt.ghi_but_toan(conn, pv, lat["trong"], "hd", "X", actor=AI, reason="r")
    d = gt.dao_but_toan(conn, pv, a.adj_id, actor=AI, reason="dao")
    with pytest.raises(gt.LoiGhi, match="ban dao"):
        gt.dao_but_toan(conn, pv, d.adj_id, actor=AI, reason="dao ban dao")


def test_dao_ngoai_pham_vi_thi_bi_chan(conn, lat):
    a = gt.ghi_but_toan(conn, ca_kho("bai kiem dao ngoai pham vi"), lat["la"],
                        "hd", "X", actor=AI, reason="r")
    with pytest.raises(gt.NgoaiPhamVi):
        gt.dao_but_toan(conn, chi_nap_that(), a.adj_id, actor=AI, reason="dao")


# ── luat 9: ly do + hoan hang cho ───────────────────────────────────────
def test_ghi_ly_do_vao_hang_cho(conn, lat):
    pv = mot_lan_nap(lat["run"])
    k = gt.ghi_ly_do(conn, pv, lat["trong"], reason="cho ke toan doi tac",
                     actor=AI)
    assert k.evt_id
    r = conn.execute("select s.reason, e.actor, e.evt_type"
                     " from fls_queue_state s"
                     " join fls_queue_event e using (itl_id)"
                     " where s.itl_id=%s", (lat["trong"],)).fetchone()
    assert r == ("cho ke toan doi tac", AI, "reason")


def test_hoan_phai_co_HAN(conn, lat):
    """⛔ Hoan vo han la **bo qua**, ⛔ khong phai hoan."""
    with pytest.raises(gt.TruongLa, match="HAN"):
        gt.ghi_hoan(conn, mot_lan_nap(lat["run"]), lat["trong"], den_ngay="",
                    reason="cho", actor=AI)


def test_hoan_lan_thu_BA_chi_doi_mau_KHONG_leo_cap(conn, lat):
    """⭐ `QĐ-ITL-24`: luong nay ⛔ khong co cap tren. Nen lan thu ba ⛔ khong bi
    chan va ⛔ khong bao cho ai — no chi **doi mau tren man hinh**."""
    pv = mot_lan_nap(lat["run"])
    for n in range(1, 4):
        gt.ghi_hoan(conn, pv, lat["trong"], den_ngay="2026-09-30",
                    reason=f"cho lan {n}", actor=AI)
        assert gt.dem_hoan(conn, lat["trong"]) == n
    # lan thu tu van ghi duoc — ⛔ khong chan
    gt.ghi_hoan(conn, pv, lat["trong"], den_ngay="2026-10-31", reason="cho nua",
                actor=AI)
    assert gt.dem_hoan(conn, lat["trong"]) == 4


def test_ly_do_rong_bi_chan(conn, lat):
    with pytest.raises(gt.ThieuLyDo):
        gt.ghi_ly_do(conn, mot_lan_nap(lat["run"]), lat["trong"], reason="  ",
                     actor=AI)


# ── luat 10: khung xem hieu luc ─────────────────────────────────────────
def test_khung_xem_sua_tay_chi_tra_but_toan_MOI_NHAT_chua_bi_dao(conn, lat):
    i = lat["trong"]
    pv = mot_lan_nap(lat["run"])
    gt.ghi_but_toan(conn, pv, i, "hd", "A", actor=AI, reason="1")
    gt.ghi_but_toan(conn, pv, i, "cdt1", "C", actor=AI, reason="2")
    a = gt.ghi_but_toan(conn, pv, i, "hd", "B", actor=AI, reason="3")
    r = dict(conn.execute("select field, value_after from fls_sua_tay"
                          " where itl_id=%s", (i,)).fetchall())
    assert r == {"hd": "B", "cdt1": "C"}
    gt.dao_but_toan(conn, pv, a.adj_id, actor=AI, reason="dao")
    r = dict(conn.execute("select field, value_after from fls_sua_tay"
                          " where itl_id=%s", (i,)).fetchall())
    assert r == {"hd": "A", "cdt1": "C"}


# ══ ⭐⭐ CUA GHI KIEM GIA TRI (04/09) ══════════════════════════════════════
# ⛔⛔ Truoc hom nay cua ghi **⛔ khong kiem gi ca**: go mot ma hop dong ⛔ khong
# ton tai cung vao so **nhu that**. May da biet du **73 ma** *(bang
# `fls_mapping_master`, va do that thi **0** ma `hd` trong so nam ngoai no ⇒
# danh muc **co tham quyen**)* ma van ⛔ khong chan.
#
# ⚠ Hai o `svc_*` cung the: chung la **KY `YYYYMM`**, ⛔ khong phai NGAY —
# **99,8%** dong dang dung khuon ay, va **11 dong ban** *(gom 2 dong mang so
# serial ngay cua Excel: `45962`)* la thu lot qua vi ⛔ khong ai kiem.


@pytest.fixture(autouse=True)
def danh_muc(conn):
    """Dat danh muc cho MOT bai — va **DON SACH ca TRUOC lan SAU**.

    ⛔⛔ **`autouse` la co y, va day la ly do:** tu 04/09 cua ghi **doc**
    `fls_mapping_master` de kiem ma hop dong. Bang ay dung CHUNG ca kho test,
    va `test_alloc_tren_doc_pg.py` — chay TRUOC tep nay theo thu tu chu cai —
    gieo danh muc roi ⛔ **khong don**. ⇒ Mot thay doi trong SAN PHAM da bien
    mot bang tung vo hai thanh mot **phu thuoc cheo tep**: sau bai `dao_*`
    trong tep nay bong do, ma chay rieng tep thi xanh.

    ⇒ Tep nay **tu lam chu** trang thai ay: moi bai bat dau voi danh muc
    **RONG** *(= may ⛔ khong biet ⇒ ⛔ khong chan)*, va bai nao can ma thi goi
    `danh_muc(...)` tuong minh. ⛔ Mot bo test ma ket qua phu thuoc thu tu chay
    la mot bo test ⛔ khong noi len duoc dieu gi.

    ⛔⛔ Lan dau toi viet cai nay la mot ham thuong: no ghi vao
    `fls_mapping_master` roi **⛔ khong don**. Bang ay dung CHUNG cho ca bo
    test, nen cac bai CU — von go `hd="HD-1"` khi danh muc rong — bong nhien
    **do theo thu tu chay**. ⇒ Mot bo test ma ket qua phu thuoc thu tu la mot
    bo test ⛔ khong noi len duoc dieu gi.

    ⚠ `DELETE` o day hop le: `INV-I08` khai `fls_mapping_master` la **ngoai le
    duy nhat** — no duoc thay **nguyen bang**, ⛔ khong phai so chi-them.
    """
    def dat(*ma: str) -> None:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fls_mapping_master")
            for m in ma:
                cur.execute(
                    "INSERT INTO fls_mapping_master (hd_code) VALUES (%s)",
                    (m,))
    dat()          # ⭐ TRUOC: xoa dau vet cua tep chay truoc
    yield dat
    dat()          # ⭐ SAU: ⛔ khong de lai dau vet cho tep chay sau


def test_ma_hop_dong_NGOAI_danh_muc_thi_cua_TU_CHOI(conn, danh_muc):
    danh_muc("HD-CO-THAT", "NB")
    with conn.cursor() as cur:
        r = _run(cur)
        i = _dong(cur, r)
    pv = mot_lan_nap(r)
    with pytest.raises(gt.MaLa) as e:
        gt.ghi_but_toan(conn, pv, i, "hd", "HD-BIA-RA", actor=AI, reason="x")
    # ⭐ Loi phai noi duoc BUOC TIEP THEO: neu ma vua duoc lap ben so goc thi
    #   ban khai cua FLS dang CU, va ke toan bi chan ma ⛔ khong biet vi sao.
    assert "nap_mapping_master" in str(e.value), str(e.value)
    assert "2 ma" in str(e.value), str(e.value)


def test_force_KHONG_vuot_qua_duoc_phep_kiem_danh_muc(conn, danh_muc):
    """⛔⛔ `force` sinh ra cho *"go khac nguon"* — mot **bat dong** giua hai cau
    tra loi **deu co that**. Mot ma ⛔ khong ton tai thi ⛔ khong phai bat dong,
    no la **mot cai ⛔ khong co**. Cho `force` di qua la bien phep kiem thanh
    mot loi nhac bo qua duoc."""
    danh_muc("HD-CO-THAT")
    with conn.cursor() as cur:
        r = _run(cur)
        i = _dong(cur, r)
    with pytest.raises(gt.MaLa):
        gt.ghi_but_toan(conn, mot_lan_nap(r), i, "hd", "HD-BIA-RA", actor=AI,
                        reason="co y ghi de", force=True)


def test_ma_chi_khac_HOA_THUONG_thi_loi_phai_CHI_RA_ma_that(conn, danh_muc):
    """⭐ Khoa `hd_code` phan biet hoa-thuong, con phep tra cua Sheets thi ⛔
    khong ⇒ nguoi go rat de gap dung cho nay. Mot cau *"⛔ khong co ma nay"* se
    lam ho di tim mot thu **van dang o do**."""
    danh_muc("NB")
    with conn.cursor() as cur:
        r = _run(cur)
        i = _dong(cur, r)
    with pytest.raises(gt.MaLa) as e:
        gt.ghi_but_toan(conn, mot_lan_nap(r), i, "hd", "nb", actor=AI, reason="x")
    assert "'NB'" in str(e.value), str(e.value)


def test_danh_muc_RONG_thi_KHONG_chan(conn):
    """⛔⛔ **Danh muc rong ⇒ may ⛔ KHONG BIET, ⛔ chu ⛔ khong phai "moi ma deu
    sai".** Chan het moi phep ghi vi ban khai chua duoc nap la mot cai may noi
    *"sai"* trong khi y no la *"toi ⛔ khong biet"* — dung cai lan lon ma
    `INV-I16` sinh ra de chan."""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM fls_mapping_master")
        r = _run(cur)
        i = _dong(cur, r)
    kq = gt.ghi_but_toan(conn, mot_lan_nap(r), i, "hd", "HD-BAT-KY", actor=AI,
                         reason="x")
    assert kq.adj_id is not None


def test_BO_GAN_mot_o_thi_luon_di_qua_duoc(conn, danh_muc):
    """⚠ O rong ⛔ khong phai mot gia tri sai — no la phep **BO GAN**. Chan no
    la cat mat duong lui: ke toan gan nham roi thi ⛔ khong xoa lai duoc."""
    danh_muc("HD-CO-THAT")
    with conn.cursor() as cur:
        r = _run(cur)
        i = _dong(cur, r)
    assert gt.ghi_but_toan(conn, mot_lan_nap(r), i, "hd", "", actor=AI,
                           reason="bo gan").adj_id is not None


@pytest.mark.parametrize("v", ["2024-12-01", "45962", "tháng 5", "202413",
                               "2025", "2025.07"])
def test_ky_dich_vu_SAI_KHUON_thi_cua_TU_CHOI(conn, v):
    """⛔ Sau gia tri nay **deu co that trong so** *(11 dong)* — chung lot qua
    vi ⛔ khong ai kiem. `45962` la **so serial ngay cua Excel**."""
    with conn.cursor() as cur:
        r = _run(cur)
        i = _dong(cur, r)
    with pytest.raises(gt.KhuonLa):
        gt.ghi_but_toan(conn, mot_lan_nap(r), i, "svc_start", v, actor=AI,
                        reason="x")


def test_ky_dich_vu_DUNG_KHUON_thi_di_qua(conn):
    with conn.cursor() as cur:
        r = _run(cur)
        i = _dong(cur, r)
    assert gt.ghi_but_toan(conn, mot_lan_nap(r), i, "svc_end", "202412", actor=AI,
                           reason="x").adj_id is not None
