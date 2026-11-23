# -*- coding: utf-8 -*-
"""`WO-003` — cú Ghép TAY: `reason` tuỳ ý · `hd`/`cdt1` là MÁY GỢI Ý · bỏ ghép
đảo mọi gợi ý của dòng.

⭐⭐⭐ Căn cứ: `QĐ-ITL-149` *(owner 01/10, nguyên văn)*:
  · *"Khi bấm Ghép, máy tự điền cdt1/hd. Hai ô này nên được ghi là người chốt
    hay máy gợi ý?"* ⇒ **"Máy gợi ý"**.
  · *"bỏ yêu cầu lý do cho cú Ghép"*.
Spec: `BA-07` v3.4 `§4h ⓼` · `BA-05` v0.32 `DD-I15 ⓓd` · `BA-10` v0.6 `DT-I14`
· `BA-09` v0.5 `SM-I06` *(chuyển cấm `F-7`, `F-9`)* · `BA-11` v0.14 `INV-I16`
*(phạm vi lý do)* + `INV-I21` *(lằn máy gồm ghép tay)*.

⛔⛔ **Vì sao tệp này tồn tại — lỗ ĐÃ ĐO, ⛔ không phải lo xa.**

  ⓐ `KQ-002 F-1` *(`CHAN`)*: màn ghép ⛔ có ô lý do *(`QĐ-ITL-137` hoãn)*, cửa
    đòi `reason` ⇒ nút `Gán` / `Bỏ gán` trên máy thật trả **`400`** cả hai.
  ⓑ UAT 01/10 *(`itl_id 27728`)*: một cú Ghép ghi **4** dòng `nguon='sua_tay'`
    ⇒ hai ô `hd`/`cdt1` vào **Final** nhân danh người bấm, trong khi người bấm
    `Gán` là chọn **dòng lệnh**, ⛔ gõ ô nào *(`INV-I21` v0.14)*.
  ⓒ Bỏ ghép một dòng **máy** ghép ⛔ đảo gợi ý máy *(chỉ giữ dòng ở
    `fls_sua_tay`)* ⇒ gợi ý **mồ côi**: căn cứ đã mất mà màn vẫn có thể hiện.

⭐ Mọi phép đếm ở đây đếm trên **CÙNG một `itl_id`** vừa dựng, và mỗi bài
chứng minh mẫu số ≠ 0 trước khi kết luận *(`Đ3`)*.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo import ghi_tay as gt
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg

DSN = dsn_test()
ACTOR = "ke-toan@apero.vn"
LY_DO = "ghep tay tu man F01"


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _run(conn) -> str:
    """Lần nạp HÌNH DẠNG THẬT nhưng năm **2000** — bản TRẮNG của kho test."""
    r = "NAP-2000-01-01-W" + uuid.uuid4().hex[:6].upper()
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (r,))
    return r


def _dong_bank(conn, run: str, tien: str, curr: str = "VND") -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW','L1',%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-W',%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, uuid.uuid4().int % 100000, run, curr,
         D(tien))).fetchone()[0]


def _lenh(conn, run: str, *ds: tuple) -> None:
    """`ds` = (line, tien, curr, status, hd, cdt1) — đặt vào ảnh chụp."""
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + i, x[0].split("-")[0], x[0], D(x[1]), x[2], x[3], None,
               x[4], x[5], ref_tho=None) for i, x in enumerate(ds)])


def _ma() -> str:
    """Mã dòng lệnh RIÊNG mỗi bài — tránh đếm lẫn với các lần chạy trước."""
    return "PW" + uuid.uuid4().hex[:6].upper() + "-1"


def _dem(conn, sql: str, i: int) -> int:
    return conn.execute(sql, (i,)).fetchone()[0]


def _final(conn, i: int) -> dict[str, str | None]:
    """Final của ô = `COALESCE(fls_sua_tay, fls_itl.<field>)` — `DD-I15 ⓓd`."""
    r = conn.execute(
        "SELECT COALESCE((SELECT value_after FROM fls_sua_tay"
        "                  WHERE itl_id=i.itl_id AND field='hd'), i.hd),"
        "       COALESCE((SELECT value_after FROM fls_sua_tay"
        "                  WHERE itl_id=i.itl_id AND field='cdt1'), i.cdt1)"
        "  FROM fls_itl i WHERE i.itl_id=%s", (i,)).fetchone()
    return {"hd": r[0], "cdt1": r[1]}


def _mot_dong(conn, hd: str = "HD-W", cdt1: str = "CDT-W") -> tuple[str, int, str]:
    run = _run(conn)
    i = _dong_bank(conn, run, "5000000.00")
    ma = _ma()
    _lenh(conn, run, (ma, "5000000.00", "VND", "Approve", hd, cdt1))
    return run, i, ma


# ═════════════════════════════ (a) `reason` TUỲ Ý — `BA-07 §4h ⓼` · AC-2
def test_hai_hang_ly_do_mac_dinh_DUNG_chuoi_hop_dong():
    """`BA-07 §4h ⓼`: *"chuỗi là HỢP ĐỒNG, khai một chỗ trong mã"*."""
    assert gt.LY_DO_MAC_DINH_GHEP == \
        "(may dien) ghep tren man - nguoi bam khong ghi ly do"
    assert gt.LY_DO_MAC_DINH_BO_GHEP == \
        "(may dien) bo ghep tren man - nguoi bam khong ghi ly do"


def test_ghep_va_bo_ghep_THIEU_ly_do__vet_mang_ly_do_MAC_DINH_va_actor_NGUOI(conn):
    """⭐⭐ AC-2. Hai vế của một bài:

      ⓐ thiếu lý do ⇒ **được** *(owner: "bỏ yêu cầu lý do cho cú Ghép")*;
      ⓑ ⛔ nhưng vết **⛔ BAO GIỜ rỗng** — lỗ 27/08 *(`ghi_tay.py` chú thích
        `ghep_lenh`)*: một phép ghép đi qua với `reason` rỗng ⇒ sổ vết có dòng
        ⛔ trả lời được *"vì sao"*. Lý do mặc định có nhãn `(may dien)` ⇒ người
        đọc vết phân biệt được *"người ⛔ ghi lý do"* với *"lý do bị mất"*.

    ⚠ Nhãn nói *"chữ do máy điền"*, ⛔ nói *"máy bấm"* ⇒ `actor` VẪN là người
      *(`§4h ⓼ ⓓ`)* — cổng mốc `B` đếm cú bấm này theo `actor`.
    """
    _run_id, i, ma = _mot_dong(conn)
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason="")
    rb = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="   ")

    vet = conn.execute(
        "SELECT evt_id, evt_type, reason, actor FROM fls_queue_event"
        " WHERE itl_id=%s AND evt_type IN ('match','unmatch') ORDER BY evt_id",
        (i,)).fetchall()
    assert [v[0] for v in vet] == [ra["evt_id"], rb["evt_id"]], \
        f"⛔ không đo được: mong 2 sự kiện của chính hai cú bấm, thấy {vet}"
    for _e, loai, ly_do, ai in vet:
        assert ly_do and ly_do.startswith("(may dien) "), (
            f"⛔ sự kiện `{loai}` thiếu lý do mà vết mang {ly_do!r} — phải bắt "
            "đầu bằng lý do mặc định `(may dien) …` (`BA-07 §4h ⓼`)")
        assert ai == ACTOR, (
            f"⛔ `actor` của `{loai}` = {ai!r}: lý do do máy ĐIỀN, ⛔ máy BẤM — "
            "đổi `actor` là giấu người đã bấm (`AUD-1`)")
    assert vet[0][2].startswith(gt.LY_DO_MAC_DINH_GHEP)
    assert vet[1][2].startswith(gt.LY_DO_MAC_DINH_BO_GHEP)
    # ⛔ Và **0** dòng rỗng — đếm trên chính dòng này, mẫu số = 2 (đã chứng ở trên).
    assert _dem(conn, "SELECT count(*) FROM fls_queue_event WHERE itl_id=%s"
                      " AND COALESCE(btrim(reason),'')=''", i) == 0


@pytest.mark.parametrize("xau", [None, "", "   "])
def test_ly_do_RONG_moi_kieu_deu_thanh_ly_do_mac_dinh(conn, xau):
    """Ba hình của *"thiếu"*: `None` · rỗng · toàn khoảng trắng."""
    _run_id, i, ma = _mot_dong(conn)
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=xau)
    ly_do, = conn.execute("SELECT reason FROM fls_queue_event WHERE evt_id=%s",
                          (ra["evt_id"],)).fetchone()
    assert ly_do.startswith(gt.LY_DO_MAC_DINH_GHEP), ly_do


def test_ly_do_CO_thi_ghi_DUNG_chu_nguoi_gui(conn):
    """Chiều ngược (`Đ5`): có lý do thì ⛔ máy điền gì."""
    _run_id, i, ma = _mot_dong(conn)
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    ly_do, = conn.execute("SELECT reason FROM fls_queue_event WHERE evt_id=%s",
                          (ra["evt_id"],)).fetchone()
    assert ly_do.startswith(LY_DO) and "(may dien)" not in ly_do, ly_do


# ═════════════════════════════ (b) `hd`/`cdt1` = MÁY GỢI Ý — AC-5 · AC-8
def test_ghep_TAY_hd_cdt1_vao_fls_may_goi_y__Final_KHONG_doi(conn):
    """⭐⭐⭐ AC-5 — `DD-I15 ⓓd`, `DT-I14` nhánh 3, chuyển cấm `SM-I06 F-7`.

    ⛔ Người bấm `Gán` chọn **dòng lệnh**, ⛔ gõ `hd`/`cdt1`. Hai ô suy ra là
      lời **máy** nói: vào `fls_may_goi_y`, ⛔ vào `fls_sua_tay`, ⛔ đổi Final.
    """
    _run_id, i, ma = _mot_dong(conn)
    truoc = {"may": _dem(conn, "SELECT count(*) FROM fls_may_goi_y WHERE itl_id=%s", i),
             "tay": _dem(conn, "SELECT count(*) FROM fls_sua_tay WHERE itl_id=%s", i),
             "final": _final(conn, i)}

    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)

    # ⭐ Mẫu số ≠ 0: cú ghép THẬT có suy ra hai ô (`Đ3`).
    assert {x["field"] for x in ra["but_toan"]} == {"hd", "cdt1"}, ra
    assert _dem(conn, "SELECT count(*) FROM fls_may_goi_y WHERE itl_id=%s", i) \
        == truoc["may"] + 2
    assert _dem(conn, "SELECT count(*) FROM fls_sua_tay WHERE itl_id=%s", i) \
        == truoc["tay"], "⛔⛔ cú ghép lọt vào `fls_sua_tay` = máy chốt thay người"
    adj = conn.execute(
        "SELECT a.field, a.nguon, a.actor, a.evt_id FROM fls_adjustment a"
        " WHERE a.itl_id=%s ORDER BY a.field", (i,)).fetchall()
    assert adj == [("cdt1", "may_goi_y", ACTOR, ra["evt_id"]),
                   ("hd", "may_goi_y", ACTOR, ra["evt_id"])], adj
    jrn = conn.execute(
        "SELECT field, value_source, actor, value_before FROM fls_journal"
        " WHERE itl_id=%s ORDER BY field", (i,)).fetchall()
    assert jrn == [("cdt1", "may_goi_y", ACTOR, None),
                   ("hd", "may_goi_y", ACTOR, None)], jrn
    assert _final(conn, i) == truoc["final"], (
        "⛔⛔ Final ĐỔI sau cú ghép — owner: *\"Máy gợi ý\"* (`QĐ-ITL-149`)")
    assert ra["nguoi_da_chot"] == []


def test_cong_C8_KHONG_lat_khi_chi_co_cu_ghep(conn):
    """AC-8 — `khop_owner C8` đếm `fls_sua_tay` *(người đã chốt ô nào)*; một cú
    ghép thật đầu tiên ⛔ được lật nó. Đếm **cả bảng**, như cổng đếm."""
    _run_id, i, ma = _mot_dong(conn)
    truoc = conn.execute("SELECT count(*) FROM fls_sua_tay").fetchone()[0]
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    assert ra["but_toan"], "⛔ không đo được: cú ghép ⛔ suy ra ô nào"
    assert conn.execute("SELECT count(*) FROM fls_sua_tay").fetchone()[0] == truoc


def test_NGUOI_da_chot_hd_roi_moi_ghep__may_IM_o_hd_van_goi_y_cdt1(conn):
    """⭐⭐ AC-6 — `DT-I14` nhánh 1: người đã chốt ô ⇒ máy **im**, khai
    `nguoi_da_chot`. Cùng luật `may_ghep.ghi_goi_y_may` — ⛔ bản thứ hai."""
    _run_id, i, ma = _mot_dong(conn, hd="HD-LENH", cdt1="CDT-LENH")
    gt.ghi_but_toan(conn, chi_nap_that(), i, "hd", "HD-NGUOI", actor=ACTOR,
                    reason="nguoi chot truoc khi ghep")

    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)

    assert ra["nguoi_da_chot"] == ["hd"], ra
    assert [x["field"] for x in ra["but_toan"]] == ["cdt1"], ra
    may = dict(conn.execute("SELECT field, value_after FROM fls_may_goi_y"
                            " WHERE itl_id=%s", (i,)).fetchall())
    assert may == {"cdt1": "CDT-LENH"}, f"⛔ máy gợi ý đè ô người đã chốt: {may}"
    assert _final(conn, i)["hd"] == "HD-NGUOI"


def test_goi_y_TRUNG_gia_tri_dang_co__KHONG_them_dong(conn):
    """`DT-I14` nhánh 2: gợi ý đang có = `v` ⇒ ⛔ thêm dòng rỗng."""
    from fls.repo.may_ghep import ghi_goi_y_may

    _run_id, i, ma = _mot_dong(conn, hd="HD-T", cdt1="CDT-T")
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-T",
                                         "cdt1": "CDT-KHAC"}])
    n = _dem(conn, "SELECT count(*) FROM fls_adjustment WHERE itl_id=%s", i)
    assert n == 2, "⛔ không đo được: máy ⛔ gợi ý trước"

    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    assert [x["field"] for x in ra["but_toan"]] == ["cdt1"], ra
    assert _dem(conn, "SELECT count(*) FROM fls_adjustment WHERE itl_id=%s", i) == 3
    # ⭐ `value_before` = gợi ý máy ĐANG hiệu lực, ⛔ lấy lằn người.
    vb, = conn.execute(
        "SELECT value_before FROM fls_journal WHERE itl_id=%s AND field='cdt1'"
        " ORDER BY jrn_id DESC LIMIT 1", (i,)).fetchone()
    assert vb == "CDT-KHAC"


def test_N_dong_lenh_noi_KHAC_nhau__khong_suy_va_KHONG_goi_y(conn):
    """`DT-I14` nhánh 4 — `INV-I16`: ⛔ lấy dòng đầu tiên."""
    run = _run(conn)
    i = _dong_bank(conn, run, "100.00")
    a, b = _ma(), _ma()
    _lenh(conn, run, (a, "60.00", "VND", "Approve", "HD-A", "CDT-X"),
          (b, "40.00", "VND", "Approve", "HD-B", "CDT-X"))
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [a, b], actor=ACTOR, reason=LY_DO)
    assert ra["khong_suy_duoc"] == ["hd"]
    assert dict(conn.execute("SELECT field, value_after FROM fls_may_goi_y"
                             " WHERE itl_id=%s", (i,)).fetchall()) == \
        {"cdt1": "CDT-X"}


# ═════════════════════════════ (b) BỎ GHÉP đảo mọi gợi ý — AC-7
def test_bo_ghep_dong_ghep_TAY__dao_goi_y__fls_may_goi_y_ve_0(conn):
    """AC-7 ⓐ — `DT-I14` nhánh 6: gợi ý còn hiệu lực ⇒ ĐẢO, bản đảo mang
    `nguon` **bằng** `nguon` của dòng bị đảo."""
    _run_id, i, ma = _mot_dong(conn)
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    assert _dem(conn, "SELECT count(*) FROM fls_may_goi_y WHERE itl_id=%s", i) == 2

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="ghep sai")

    assert {x["field"] for x in ra["but_toan_dao"]} == {"hd", "cdt1"}, ra
    assert _dem(conn, "SELECT count(*) FROM fls_may_goi_y WHERE itl_id=%s", i) == 0
    dao = conn.execute(
        "SELECT d.nguon, d.state, d.value_after, g.nguon FROM fls_adjustment d"
        " JOIN fls_adjustment g ON g.adj_id = d.reversal_of"
        " WHERE d.itl_id=%s", (i,)).fetchall()
    assert len(dao) == 2 and all(
        x == ("may_goi_y", "reversed", None, "may_goi_y") for x in dao), dao
    vs = {r[0] for r in conn.execute(
        "SELECT value_source FROM fls_journal WHERE itl_id=%s AND value_after"
        " IS NULL", (i,)).fetchall()}
    assert vs == {"may_goi_y"}, vs


def test_bo_ghep_dong_MAY_ghep__dao_ca_goi_y_cua_may_fls(conn):
    """⭐⭐ AC-7 ⓑ — **đổi hành vi**: trước `WO-003` bỏ ghép một dòng **máy**
    ghép giữ phép lọc `con_hieu_luc &= dang_dung` *(chỉ `fls_sua_tay`)* ⇒ gợi ý
    `may@fls` **mồ côi**: căn cứ của nó *(chùm mối nối)* đã bị bỏ mà nó vẫn
    nằm trong `fls_may_goi_y`."""
    from fls.repo.may_ghep import MAY, ghi_goi_y_may

    run, i, ma = _mot_dong(conn)
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)",
                 (i, ma, D("5000000.00"), run))
    g = ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-W",
                                             "cdt1": "CDT-W"}], run_pm=run)
    assert len(g["but_toan"]) == 2, "⛔ không đo được: máy ⛔ gợi ý"
    assert {r[0] for r in conn.execute(
        "SELECT actor FROM fls_adjustment WHERE itl_id=%s", (i,))} == {MAY}

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="ghep sai")

    assert {x["field"] for x in ra["but_toan_dao"]} == {"hd", "cdt1"}, ra
    con = _dem(conn, "SELECT count(*) FROM fls_may_goi_y WHERE itl_id=%s", i)
    assert con == 0, f"⛔⛔ {con} gợi ý MỒ CÔI sau khi bỏ cả chùm mối nối"


def test_bo_ghep_KHONG_dao_gia_tri_NGUOI__va_KHAI_trong_bo_qua(conn):
    """AC-7 — `DT-I14` dòng cuối, chuyển cấm `SM-I06 F-8`: giá trị **người** gõ
    sau cú ghép ⛔ gắn sự kiện `match` ⇒ ⛔ chạm; khai `bo_qua` vì nó đè lên ô
    có gợi ý."""
    _run_id, i, ma = _mot_dong(conn)
    gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    gt.ghi_but_toan(conn, chi_nap_that(), i, "hd", "HD-NGUOI",
                    actor="ke-toan-2@apero.vn", reason="go lai")

    ra = gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="ghep sai")

    assert dict(conn.execute("SELECT field, value_after FROM fls_sua_tay"
                             " WHERE itl_id=%s", (i,)).fetchall()) == \
        {"hd": "HD-NGUOI"}, "⛔⛔ bỏ ghép đã đảo giá trị NGƯỜI"
    nguoi = [x for x in ra["bo_qua"] if x["field"] == "hd"]
    assert nguoi and "NGUOI" in nguoi[0]["vi_sao"], ra["bo_qua"]
    assert _dem(conn, "SELECT count(*) FROM fls_may_goi_y WHERE itl_id=%s", i) == 0


def test_goi_y_lai_KHONG_goi_y_lai_dong_da_bo_ghep(conn):
    """`WO-003` Rủi ro 2: `tools/goi_y_lai.py` đọc khung xem `fls_moi_noi`
    *(`:37`, `:51`)* nên dòng đã bỏ ghép ⛔ được gợi ý lại — ghim bằng **chính
    câu SQL** của công cụ, ⛔ chỉ tin chú thích."""
    from fls.repo.may_ghep import ghi_goi_y_may
    from tools import goi_y_lai

    run, i, ma = _mot_dong(conn)
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)",
                 (i, ma, D("5000000.00"), run))
    ghi_goi_y_may(conn, itl_id=i, lenh=[{"pm_line_id": ma, "hd": "HD-W",
                                         "cdt1": "CDT-W"}], run_pm=run)
    dk, ts = chi_nap_that().dieu_kien("p.run_id")
    goc = goi_y_lai._SQL.format(dk=dk)
    assert goc.count("ORDER BY n.itl_id") == 1, "⛔ khuôn SQL của công cụ đã đổi"
    sql = goc.replace("ORDER BY n.itl_id", "WHERE n.itl_id = %s ORDER BY n.itl_id")
    assert conn.execute(sql, [*ts, i]).fetchall(), \
        "⛔ không đo được: trước khi bỏ, công cụ phải THẤY dòng này"

    gt.bo_moi_noi(conn, chi_nap_that(), i, actor=ACTOR, reason="ghep sai")
    assert conn.execute(sql, [*ts, i]).fetchall() == [], \
        "⛔ `goi_y_lai` sẽ gợi ý lại một dòng vừa bị bỏ ghép"


# ═════════════════════════════ (d) `run_pm` — AC-4 (bài repo của Dev)
def test_ghep_TAY_ghi_run_pm_bang_anh_PM_da_dung(conn):
    """`KQ-002 F-4`: `run_pm` **0/2.263** trên kho thật. Cột `run_id` giữ
    nghĩa đang có ở đường tay *(= ảnh PM, bài `test_ghep_lenh_pg::
    test_TU_CHOI_dong_lenh_cua_ANH_CU…` ghim)*."""
    _run_id, i, ma = _mot_dong(conn)
    ra = gt.ghep_lenh(conn, chi_nap_that(), i, [ma], actor=ACTOR, reason=LY_DO)
    r = conn.execute("SELECT run_pm, run_id FROM fls_pm_link WHERE itl_id=%s",
                     (i,)).fetchall()
    assert r == [(ra["run_id"], ra["run_id"])], r
