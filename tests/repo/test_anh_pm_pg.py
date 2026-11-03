"""ANH LENH CHI DANG HIEU LUC — `QĐ-ITL-119`, cai mo duong cho moc `A3`.

⛔⛔⛔ **Bo bai nay ghim mot thu ma truoc 09/09 la SAI, va cai sai ay ⛔ khong
   he bao loi — no chi lam moi thu **⛔ khong xay ra**.**

Moc `A3` duoc dat ra de go **6.577 dong** tien co ma chung tu ma ⛔ khong dong
lenh nao mang ma ay. Nhung phep ghep cu loc `l.run_id = <run_id CUA DONG TIEN>`
⇒ nap lenh chi cho moi vao mot `run_id` moi thi 10.030 dong tien **CU** thay
**0** ung vien. `A3` se chay xong, in ra *"nap 3.700 dong lenh"*, va con so
6.577 **dung yen**.

⇒ Bai `test_dong_tien_CU_THAY_DUOC_lenh_chi_MOI` la **cong ra thuc su cua
  `A3`**: no do dung cai *"co dich duoc mot dong nao khong"*, ⛔ khong do
  *"co nap duoc du lieu vao khong"*.

★ Va ba bai con lai canh ba cach de luat moi **hong trong im lang**:
  ⓐ ba noi *(cua doc · phep do · cua ghi)* PHAI nhin **CUNG mot anh**;
  ⓑ anh cu ⛔ khong duoc lam ung vien *(dong lenh da huy phai bien mat)*;
  ⓒ **PHAM VI** phai con hieu luc — day la cho nguy nhat cua ca thay doi nay.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM, canon_ref
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo import do_mau_so as dms
from fls.repo import ghi_tay as gt
from fls.repo.anh_pm import LAN_PM, anh_pm_hieu_luc
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.doc_bao_cao import ung_vien_pm
from fls.repo.pham_vi import chi_nap_that, mot_lan_nap

pytestmark = pytest.mark.pg

ACTOR = "ke.toan@apero.vn"
LY_DO = "bai kiem anh PM hieu luc"


def _hex(n: int = 6) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


def _run(conn, ngay: str = "2000-01-01") -> str:
    r = f"NAP-{ngay}-AP{_hex()}"
    conn.execute("INSERT INTO fls_run (run_id, contract_version,"
                 " canon_version, mapping_version)"
                 " VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_tien(conn, run: str, doc_no: str, tien: str, tt: str) -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_co, work_status)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,'UNMAPPED') RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, doc_no, tt,
         D(tien))).fetchone()[0]


def _lenh(conn, run: str, line: str, ref: str, tien: str, tt: str) -> None:
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"),
                 [DongPM(3, line.split("-")[0], line, D(tien), tt, "Approve",
                         canon_ref(ref), "HD-1", "CDT-1", ref_tho=ref)])


def _ma(goc: str) -> str:
    """Mã dòng lệnh **duy nhất mỗi lần chạy** *(`PMB-1` ⇒ `PMB<hex>-1`)*.

    ⛔⛔ `WO-051` `AC-10` *(`KQ-061` lượt 4 — `test_BA_NOI…` · `test_anh_CU…`
    đỏ, chạy riêng xanh)*: bản trước dùng mã **cố định** *(`PMB-1`,
    `PMC-CU`, …)*. Kho TEST được **giữ** giữa hai lượt *(`FLS_GIU_KHO=1` /
    `--giu-kho` — `KQ-061` ghi Test đặt nó cho mọi lượt riêng)* ⇒ lượt sau gặp
    mối nối / dòng lệnh **cùng mã** của lượt trước ⇒ `ds_tu_chung` trả `{}`,
    `fls_moi_noi` đếm `3` thay vì `1`. Tái hiện có kiểm soát 06/10
    *(`BG-064`)*: `pytest` toàn bộ hai lượt liền, lượt hai `FLS_GIU_KHO=1` ⇒
    **đúng hai** bài này đỏ. Mã ngẫu nhiên ⇒ ⛔ va chạm; lo gốc của từng bài
    ⛔ đổi."""
    a, b = goc.split("-", 1)
    return f"{a}{_hex()}-{b}"


def _anh_cua_ca_hieu_luc(conn, r_pm: str) -> None:
    """⭐ Tiền đề của mọi bài *"ảnh PM hiệu lực của cả phạm vi"*: ảnh **vừa
    dựng** phải là ảnh mới nhất. Một tiến trình khác nạp ảnh PM **mới hơn**
    vào kho TEST *(máy 8099, kịch bản dựng ca…)* làm tiền đề sai ⇒ bài **ĐỎ**
    với câu **nói gốc** *(`Đ5` — ⛔ đo được là ĐỎ)*, ⛔ đỏ mù *"0 ứng viên"* /
    `DongLenhLa` như `KQ-061` lượt 4 *(`WO-051` `AC-10`)*."""
    co = anh_pm_hieu_luc(conn, chi_nap_that())
    if co != r_pm:
        pytest.fail(f"⛔ không đo được: ảnh PM hiệu lực của kho TEST là {co!r}, "
                    f"⛔ phải ảnh của ca {r_pm!r} — có tiến trình khác vừa nạp "
                    "ảnh PM mới hơn vào fls_test (chạy pytest một mình)")


# ── ⭐⭐⭐ CONG RA THUC SU CUA `A3` ──────────────────────────────────────
def test_dong_tien_CU_THAY_DUOC_lenh_chi_MOI(conn):
    """⭐⭐⭐ Dong tien nap **hom qua** phai thay duoc lenh chi nap **hom nay**.

    ⛔⛔ Truoc `QĐ-ITL-119` bai nay **DO**, va no do theo huong te nhat: `0`
    ung vien, ⛔ khong loi, ⛔ khong canh bao — chi la **⛔ khong co gi xay ra**.
    """
    tt = "A" + _hex(5)
    ref = "FT-CU-MOI-" + _hex()
    r_so = _run(conn, "2000-01-01")          # lan nap dong tien — CU
    r_pm = _run(conn, "2000-06-01")          # anh lenh chi — MOI
    i = _dong_tien(conn, r_so, ref, "1000000.00", tt)
    _lenh(conn, r_pm, _ma("PMA-1"), ref, "1000000.00", tt)
    _anh_cua_ca_hieu_luc(conn, r_pm)

    d = ung_vien_pm(conn, chi_nap_that(), i, n=20)
    assert d is not None
    assert [x["bac"] for x in d["ung_vien"]] == ["ma"], \
        "⛔ dong tien CU ⛔ khong thay lenh chi MOI ⇒ moc `A3` vo nghia"
    # ⭐ Va man hinh phai biet no dang nhin anh NAO — hai anh cho hai danh sach
    assert d["anh_chup"]["run_id"] == r_pm
    assert d["anh_chup"]["run_dong_tien"] == r_so
    assert d["anh_chup"]["co_anh"] is True


def test_BA_NOI_deu_nhin_CUNG_mot_anh(conn):
    """⛔⛔ Cua DOC · phep DO · cua GHI — ba noi, **mot** anh.

    Neu cua doc goi y tu anh moi ma cua ghi tra loi tu anh cu thi nguoi go bam
    mot dong lenh **co that tren man** va nhan `⛔ khong co trong anh chup` —
    mot cai bay ⛔ khong ai gia lap ra duoc trong dau.
    """
    tt = "B" + _hex(5)
    ref = "FT-BA-" + _hex()
    r_so, r_pm = _run(conn, "2000-01-01"), _run(conn, "2000-06-01")
    i = _dong_tien(conn, r_so, ref, "2000000.00", tt)
    mb = _ma("PMB-1")
    _lenh(conn, r_pm, mb, ref, "2000000.00", tt)
    _anh_cua_ca_hieu_luc(conn, r_pm)
    pv = chi_nap_that()

    assert anh_pm_hieu_luc(conn, pv) is not None
    d = ung_vien_pm(conn, pv, i, n=20)
    tc = dms.ds_tu_chung(conn, pv, itl_ids=[i])
    ra = gt.ghep_lenh(conn, pv, i, [mb], actor=ACTOR, reason=LY_DO)

    assert d["anh_chup"]["run_id"] == tc["anh_pm"] == ra["run_id"] == r_pm
    assert tc["tu_chung"] == {i: [mb]}


def test_anh_CU_KHONG_con_lam_ung_vien(conn):
    """⭐ Mot dong lenh **da bi huy** thi no ⛔ khong con trong anh moi ⇒ no
    ⛔ khong con la ung vien. Do la hanh vi DUNG, ⛔ khong phai mat du lieu.

    ⚠ Va moi noi CU ⛔ khong he bi anh huong: `fls_moi_noi` noi theo
    `pm_line_id`, ⛔ khong theo `run_id`.
    """
    tt = "C" + _hex(5)
    ref = "FT-HUY-" + _hex()
    r_so = _run(conn, "2000-01-01")
    r_cu = _run(conn, "2000-05-01")
    i1 = _dong_tien(conn, r_so, ref, "500000.00", tt)
    cu = _ma("PMC-CU")
    _lenh(conn, r_cu, cu, ref, "500000.00", tt)
    _anh_cua_ca_hieu_luc(conn, r_cu)
    # ghep bang anh CU (luc do no la anh hieu luc)
    gt.ghep_lenh(conn, chi_nap_that(), i1, [cu], actor=ACTOR,
                 reason=LY_DO)

    # anh MOI ⛔ khong con `PMC-CU` — no da bi huy ben sheet
    r_moi = _run(conn, "2000-07-01")
    _lenh(conn, r_moi, _ma("PMC-KHAC"), "FT-KHAC-" + _hex(), "500000.00", tt)
    _anh_cua_ca_hieu_luc(conn, r_moi)
    i2 = _dong_tien(conn, r_so, ref, "500000.00", tt)

    d = ung_vien_pm(conn, chi_nap_that(), i2, n=20)
    assert cu not in [x["pm_line_id"] for x in d["ung_vien"]]
    # ⭐ moi noi cu VAN CON — no noi theo `pm_line_id`
    assert conn.execute(
        "SELECT count(*) FROM fls_moi_noi WHERE pm_line_id = %s",
        (cu,)).fetchone()[0] == 1


# ── ⛔⛔ PHAM VI — cho nguy nhat cua ca thay doi nay ────────────────────
def test_PHAM_VI_van_LOC__anh_cua_lan_nap_KHAC_khong_lot_vao(conn):
    """⛔⛔⛔ **Cho nguy nhat**, va no ⛔ khong hien nhien.

    Truoc day phep loc dong lenh **ngam** duoc bao ve: no bam theo `i.run_id`,
    ma cau doc dong tien da qua `PhamVi` roi. Nay no **tu chon mot anh** ⇒ cai
    bao ve ngam ay **⛔ khong con**. Mot anh cua lan nap KHAC — nhat la mot lan
    nap co `read_at` moi hon — se thanh *"anh dang hieu luc"* va dong lenh cua
    no **hien ra** o mot pham vi ⛔ khong duoc phep thay no.

    ⇒ Bai nay dat pham vi vao **dung mot lan nap** roi doi anh cua lan nap
      **khac** ⛔ khong duoc lot vao. Day la lop loi da lam 1.204 dong dau test
      len man hinh that mot lan (`pham_vi.py`).
    """
    tt = "D" + _hex(5)
    ref = "FT-PV-" + _hex()
    r_so, r_pm_khac = _run(conn, "2000-01-01"), _run(conn, "2000-09-01")
    i = _dong_tien(conn, r_so, ref, "700000.00", tt)
    md = _ma("PMD-NGOAI")
    _lenh(conn, r_pm_khac, md, ref, "700000.00", tt)

    # ⛔ Pham vi = DUNG lan nap cua dong tien ⇒ anh `r_pm_khac` NGOAI pham vi
    pv = mot_lan_nap(r_so)
    assert anh_pm_hieu_luc(conn, pv) is None
    d = ung_vien_pm(conn, pv, i, n=20)
    assert d["ung_vien"] == []
    assert d["anh_chup"]["co_anh"] is False, \
        "⛔ `co_anh=False` PHAI khac '0 ung vien' — hai cau tra loi khac nhau"
    # ⛔ Va cua GHI cung phai tu choi, ⛔ khong im lang ghep tu mot anh ngoai
    with pytest.raises(gt.DongLenhLa) as e:
        gt.ghep_lenh(conn, pv, i, [md], actor=ACTOR, reason=LY_DO)
    assert "khong co MOT anh chup dong lenh nao" in str(e.value)


def test_KHONG_co_anh_nao_thi_KHAI_RA_chu_khong_bao_0_ung_vien(conn):
    """⛔ *"⛔ Khong co ung vien"* va *"⛔ chua ai nap dong lenh nao"* la **hai
    cau tra loi khac nhau**, va man hinh phai phan biet duoc."""
    tt = "E" + _hex(5)
    r_so = _run(conn, "2000-01-01")
    i = _dong_tien(conn, r_so, "FT-TRONG-" + _hex(), "300000.00", tt)
    pv = mot_lan_nap(r_so)
    d = ung_vien_pm(conn, pv, i, n=20)
    assert d["anh_chup"] == {
        "run_id": None, "co_anh": False, "so_dong": 0,
        "doc_luc_som_nhat": None, "doc_luc_muon_nhat": None,
        "run_dong_tien": r_so}


def test_LAN_PM_la_lan_thu_BA_va_chup_py_nhan_no(conn):
    """`fls_chup.lan` phai nhan `PM` — ⛔ khong thi ⛔ khong co cho de anh
    lenh chi song, va `A3` phai dung mot bang thu hai."""
    from fls.repo import chup as ch
    assert LAN_PM in ch.LAN
    assert ch.LAN == ("Bank", "Cash", LAN_PM)
