# -*- coding: utf-8 -*-
"""`KQ-036` *(kiểm gộp `BG-034` + `BG-035` — `WO-032` vòng 1 + 2)* · ba lỗ còn
lại quanh **bậc** của `gd` / `gd_ds` và chip khối *"✓ Đang gán"* sau khi
`WO-032` sửa bậc `ma` + `lech` + `khoa_to`.

⭐ Cách tìm *(`fls-test`, 02/10)*: đọc diff `a718142..932d8a4` đối chiếu
`BA-07` v3.8 §4h ⓵ / ⓵' — phiếu đòi **một** phép so tiền tệ *(`WO-032` Rủi ro 2:
*"so tiền tệ có `trim`/chữ hoa ở chỗ này mà ⛔ ở chỗ kia"*)* và *"phép chia bậc
của `gd`/`gd_ds` **giống hệt** khuôn `⓵`"*. `fls/api/xu_ly.py::_bac` — hàm chia
bậc của **cả hai** cửa danh sách — vẫn so tiền tệ bằng **bản riêng**
`str(curr).upper()` *(⛔ `trim`)*, ⛔ gọi `mg.ma_tien_te` mà `lech_ung_vien` gọi;
và nhánh cuối của nó trả `cung_tien_te` cho **mọi** dòng còn lại — kể cả dòng
**khác tiền tệ** lệnh. Đó đúng là lỗi `(d)` của `WO-032` *(`/so` dán *"cùng
tiền tệ"* lên dòng USD cạnh lệnh VND)*, sống sót ở cửa **thứ hai**.

ⓐ **`F-1` *(`NHE` → `DEV`)*** — `_bac` so tiền tệ ⛔ `trim` ⇒ cùng một cặp, hàm
   `lech_ung_vien` nói *"cùng tiền tệ, lệch 0"* còn `_bac` nói *"⛔ đúng tiền"*.
   Sổ thật 02/10: `fls_itl.curr` + `fls_pm_line.curr` **0** giá trị mang khoảng
   trắng *(`SELECT curr, count(*) … GROUP BY curr` — 4 + 6 giá trị sạch)* ⇒ hôm
   nay ⛔ ca nào; đây là **hai luật** đúng chỗ phiếu cấm.
ⓑ **`F-2` *(`NHE` → `BA`)*** — mối nối **khác tiền tệ** ⛔ khớp số chứng từ ⇒
   `gd_ds.bac = 'cung_tien_te'` *(chip *"④ cùng đơn vị tiền"*)* trong khi chính
   phần tử ấy `lech = null` *(⛔ so được vì khác tiền tệ)*. `BA-07` v3.7 §4h ⓵
   cho `khac_tien_te` **chỉ ở cửa `/so`** ⇒ spec ⛔ nói `gd`/`gd_ds` khác tiền tệ
   mang bậc gì. Sổ thật 02/10 *(cửa 8088, mọi trang)*: mối nối khác tiền tệ
   **0 / 2.262** — ca biên, nhưng bộ nạp `chay_nap.chen_moi_noi` ⛔ chặn tiền tệ
   *(ca `Y` của `tests/web/ca_wo032.py` chèn đúng đường ấy)*.
ⓒ **`F-3` *(`NHE` → `DEV`)*** — `F01G.ve_dang_gan` gặp bậc **lạ** ⇒ **bỏ** chip
   *(`const b = BAC[g.bac]; if (b) …`)*; `BA-07 §4h ⓵` dòng `bac`: *"Màn gặp bậc
   lạ ⇒ in nguyên tên"* — `ve_ung_vien` đã sửa ở `WO-032 (d)`, khối *"Đang gán"*
   thì chưa. Im lặng thay vì nói dối — nhẹ hơn, nhưng vẫn **mất** nhãn.

Dữ liệu: kho **TEST** *(assert `current_database() = 'fls_test'`)*, run
`NAP-2000-01-01-T…`, tiền ngẫu nhiên; thân màn lấy từ **cửa HTTP thật**.
"""
from __future__ import annotations

import json
import os
import random
import uuid
from decimal import Decimal as D

import pytest

from fls.adapters.pm_join import DongPM, canon_ref
from fls.api import xu_ly
from fls.ledger.build import NgucCanh
from fls.repo import man_ghep as mg
from fls.repo.chay_nap import chen_dong_pm
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import conn  # noqa: F401
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01
from tests.web.test_wo032_man_cua_that import D_DA_GAN, _f01g, ca_tra  # noqa: F401


# ═══ ⓐ F-1 — `_bac` so tiền tệ bằng bản riêng (⛔ trim) ══════════════════════
def test_CANH_lech_ung_vien_coi_vnd_co_khoang_trang_la_CUNG_tien_te():
    """⭐ Xanh — **mỏ neo**: hàm `lech` của khuôn `⓵` *(một hàm cho bốn cửa)*
    coi `' vnd '` ≡ `VND` ⇒ lệch `0`. Bài dưới đòi `_bac` nói **cùng** câu."""
    assert mg.lech_ung_vien("100.00", " vnd ", "100.00", "VND") == D("0")


# ✅ `KQ-041` *(05/10)*: gỡ `xfail(strict)` — `WO-037 (d)` `_bac` gọi
#   `mg.ma_tien_te` cho cả hai vế *(`4c3b2ae`)*; XPASS đúng lý do *(bậc `tien`)*.
def test_F1_bac_gd_so_tien_te_CUNG_LUAT_voi_lech_ung_vien():
    d = {"ma_canon": None, "curr": "VND", "amount": "100.00"}
    r = {"doc_no": "KQ36-KHAC-MA", "curr": " vnd ", "tien": "100.00"}
    assert xu_ly._bac(d, r) == "tien", xu_ly._bac(d, r)


# ═══ ⓑ F-2 — `gd_ds` khác tiền tệ, ⛔ khớp mã ⇒ nhãn "cùng đơn vị tiền" ══════
@pytest.fixture()
def ca_khac_te(conn, may):  # noqa: F811
    """Lệnh VND `<y>` ↔ mối nối tới dòng tiền **USD** `<y>.00` mang số CT
    **KHÁC** *(⛔ bậc `ma`)* — chèn như `chay_nap.chen_moi_noi` *(cửa ghi tay
    ném `KhacTienTe` nên ⛔ đi đường ấy được — cùng cách ca `Y` của Dev)*."""
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ bài này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T36" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    y = random.randint(1_000, 8_999) * 100
    i = conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW',%s,1,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,'USD',%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, "R | 987654321_OCBC USD_K36" + h, run,
         "FTZ" + h, D(f"{y}.00"))).fetchone()[0]
    lenh = "PQ" + h[:6] + "-1"
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3, lenh.split("-")[0], lenh, D(f"{y}.00"), "VND", "Approve",
               canon_ref("FTQ" + h), "HD-K36", "C-K36", ref_tho="FTQ" + h)])
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)", (i, lenh, D(f"{y}.00"), run))
    return {"lenh": lenh, "itl": i, "y": y}


def _hang_da_gan(may, ma):  # noqa: F811
    con_tro = None
    for _ in range(20):
        ok, r = _goi(may, V + D_DA_GAN + ("&cursor=" + con_tro if con_tro else ""))
        assert ok == 200, r
        for x in r["data"].get("rows") or []:
            if x.get("pm_line_id") == ma:
                return x
        con_tro = r["data"].get("next_cursor")
        if not con_tro:
            break
    raise AssertionError(f"⛔ không đo được: cửa lenh-da-gan ⛔ trả {ma}")


# ✅ `KQ-041` *(05/10)*: gỡ `xfail(strict)` — `WO-037 (c)` `_bac` trả
#   `khac_tien_te` *(`BA-07` v3.9 §4h ⓵)*; XPASS đúng lý do *(`bac` =
#   `khac_tien_te`, mỏ neo `lech is None` vẫn giữ)*.
def test_F2_gd_ds_KHAC_tien_te_khong_khop_ma_KHONG_mang_nhan_CUNG_tien_te(
        ca_khac_te, may):  # noqa: F811
    the = _hang_da_gan(may, ca_khac_te["lenh"])["the"]
    ds = [u for u in the.get("gd_ds") or [] if u.get("itl_id") == ca_khac_te["itl"]]
    assert ds, f"⛔ không đo được: gd_ds ⛔ có dòng tiền {ca_khac_te['itl']}: {the}"
    u = ds[0]
    assert u["curr"] == "USD" and u["lech"] is None, u          # mỏ neo: cửa biết khác tiền tệ
    assert u["bac"] != "cung_tien_te", u


# ═══ ⓒ F-3 — khối "Đang gán" gặp bậc lạ ⇒ bỏ chip im lặng ════════════════════
_CHIP_DANG_GAN = """
  await F01G.doi_chip('da_gan');
  await F01G.mo_lenh(%s);
  // ⚠ DOM giả chỉ hiểu bộ chọn HAI tầng (`dom_gia.js::khop`)
  const c = document.querySelector('.mh .chip');
  return {co: !!document.querySelector('.mblock'), chip: c ? c.textContent : null};
"""


@can_node
def test_CANH_khoi_DANG_GAN_bac_MA_than_cua_that_co_chip_1(ca_tra):  # noqa: F811
    """⭐ Xanh — mỏ neo: thân cửa thật, lệnh `B` *(đã gán, khớp số CT)* ⇒ chip
    `① khớp số chứng từ` *(`WO-032` vòng 2 `(i)`)*."""
    ca, tra = ca_tra
    r = _chay(_f01g(tra, _CHIP_DANG_GAN % json.dumps(ca["lenh"]["B"])),
              tep=TEP_F01, vo=VO_F01)
    assert r["co"] and r["chip"] == "① khớp số chứng từ", r


# ✅ `KQ-041` *(05/10)*: gỡ `xfail(strict)` — `WO-037 (e)` `ve_dang_gan` in
#   nguyên tên bậc lạ *(`4c3b2ae`)*; XPASS đúng lý do *(chip chứa `xyz`)*.
@can_node
def test_F3_khoi_DANG_GAN_bac_LA_in_NGUYEN_TEN(ca_tra):  # noqa: F811
    """Cùng thân cửa thật, đổi **giá trị** `gd.bac` của lệnh `B` thành `'xyz'`
    *(⛔ thêm khoá — như bài `AC-5` của Dev)* ⇒ chip phải in `xyz`."""
    ca, tra = ca_tra
    la = json.loads(json.dumps(tra, default=str))
    doi = 0
    for x in la[D_DA_GAN]["rows"]:
        if x.get("pm_line_id") == ca["lenh"]["B"]:
            # khối vẽ từ `gd_ds` *(`man_f01_ghep.js` `ds_gan = lenh.gd_ds || …`)*
            for g in [x["the"]["gd"]] + list(x["the"].get("gd_ds") or []):
                g["bac"] = "xyz"
            doi += 1
    assert doi == 1, f"⛔ không đo được: thân lenh-da-gan ⛔ có {ca['lenh']['B']}"
    r = _chay(_f01g(la, _CHIP_DANG_GAN % json.dumps(ca["lenh"]["B"])),
              tep=TEP_F01, vo=VO_F01)
    assert r["co"], r
    assert r["chip"] and "xyz" in r["chip"], r

# ═══ ⓓ canh — `WO-032 AC-4` chiều ĐỎ *"bài b3 nhét lại `khoa_to`"* ═══════════
#: Bài màn khối "Đang gán" của Dev — trước `WO-032` nó **tự nhét** `khoa_to`
#: *(`KQ-031 F-3`, lần thứ ba của lớp "khuôn thử tự nhét")*.
TEP_B3 = os.path.join(os.path.dirname(__file__), "..", "web",
                      "test_b3_cuon_va_khoi_dang_gan.py")


def test_CANH_bai_b3_KHONG_tu_nhet_khoa_to():
    """⭐ Xanh hôm nay *(`grep -c khoa_to` = **0**)*. ⛔⛔ Vì sao bài này phải có:
    `WO-032 AC-4` khai chiều ĐỎ *"bài `b3` nhét lại `khoa_to` ⇒ cổng quét (h)
    ĐỎ"* — Test đo 02/10 *(đột biến `GD = {"khoa_to": ["LUONG"], …}`)*: cổng
    quét `AC-9` **XANH** *(nó hỏi khoá khuôn ⊆ khoá cửa thật, mà cửa **nay**
    trả `khoa_to`)*, và ⛔ bài nào khác đỏ ⇒ chiều ĐỎ ấy chỉ là một lần `grep`
    tay trong `BG-034`. Bài này biến lần `grep` ấy thành cổng."""
    t = open(TEP_B3, encoding="utf-8").read()
    assert len(t) > 1000, "⛔ không đo được: tệp b3 rỗng / dời chỗ"
    assert "khoa_to" not in t, "bài b3 lại tự đặt khoa_to — thân phải lấy từ cửa thật"
