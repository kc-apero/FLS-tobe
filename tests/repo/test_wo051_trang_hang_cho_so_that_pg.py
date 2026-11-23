# -*- coding: utf-8 -*-
"""`WO-051` `AC-5` — bài **hồi quy hiệu năng** đọc **sổ THẬT CHỈ ĐỌC**:
trang 2 hàng chờ của tiền tệ **nhiều dòng nhất** phải về trong `2 s`
*(`BA-08` v1.4 `NFR-I30` — một trang danh sách việc ≤ `2 s`)*.

⛔⛔ Lỗi gốc *(`KQ-050 F-1`, `EXPLAIN (ANALYZE, BUFFERS)` 06/10 — `BG-064`)*:
con trỏ `('VND', 50)` ⇒ bộ lập kế hoạch ước **`rows=1`** *(thật **4.192**)* ⇒
`Nested Loop Left Join` tính lại view `fls_queue_state` **4.192 lần** ⇒
**89–112 s** một trang. Mã khi nhận *(`9af99c4`)* ⇒ `QueryCanceled` sau `2 s`
⇒ bài **ĐỎ trong vài giây**, ⛔ chờ 100 s *(`WO-051` `(d)`)*.

⭐ Luật của tệp:
  · ⛔ ghi cứng `VND` — tiền tệ nhiều dòng nhất tra `dem_hang_cho` **lúc
    chạy** *(phân bố đổi thì bài đi theo)*;
  · ⛔ `skip`: sổ thật tắt / tiền tệ ⛔ có trang 2 ⇒ **ĐỎ** *"⛔ không đo
    được"* *(`Đ5` — phép ⛔ đo được là ĐỎ, ⛔ phải "không thấy lệch")*;
  · ⛔ nới `statement_timeout` *(`NFR-I09`)* — `2s` **là** ngân sách;
  · ⭐ **mỗi trang một kết nối MỚI** — như cửa thật
    *(`tools/chay_cua.py::_mo_ket_noi`)*. Đo trên một kết nối dùng lại là đo
    **sai**: `psycopg` tự `prepare` câu sau 5 lần cùng chữ ⇒ kế hoạch chung ⇒
    mã cũ báo trang 2 `VND` **0,088 s** *(xanh giả — đã cắn 06/10, xem
    `tools/do_trang_hang_cho.py::ket_noi_moi`)*.
"""
from __future__ import annotations

import time

import pytest

from fls.db.kho import dsn_that, noi_chi_doc
from fls.repo import doc_bao_cao as bc
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg

#: `NFR-I30` *(`BA-08` v1.4)* — ⛔ nới để xanh *(`NFR-I09`)*
NGAN_SACH = "2s"
TRANG = 50


def _ket_noi():
    """Kết nối **mới**, chỉ đọc ở tầng PG, hạn chờ `NGAN_SACH`. Sổ tắt ⇒ ĐỎ."""
    try:
        c = noi_chi_doc(dsn_that())
    except Exception as e:                          # noqa: BLE001
        pytest.fail(f"⛔ không đo được: ⛔ nối được sổ thật ({e})")
    assert c.execute("SHOW transaction_read_only").fetchone()[0] == "on", \
        "⛔ kết nối sổ thật PHẢI chỉ đọc"
    c.execute("SELECT set_config('statement_timeout', %s, false)",
              (NGAN_SACH,))
    return c


def _trang_2(curr: str) -> tuple[str, float, int]:
    """Trang 1 rồi trang 2 *(con trỏ do **hàm** cấp)* — mỗi trang một kết nối."""
    pv = chi_nap_that()
    with _ket_noi() as c:
        t1 = bc.doc_hang_cho(c, pv, curr=curr, limit=TRANG)
    assert t1.con_tro, f"⛔ không đo được: {curr} ⛔ có trang 2"
    with _ket_noi() as c:
        t0 = time.perf_counter()
        t2 = bc.doc_hang_cho(c, pv, curr=curr, con_tro=t1.con_tro, limit=TRANG)
        s = time.perf_counter() - t0
    return t1.con_tro, s, len(t2.dong)


def test_AC5_SO_THAT_trang_2_tien_te_NHIEU_DONG_NHAT_trong_2s():
    """Mong: trang 2 về **trong** `statement_timeout = 2s`, có hàng.

    ⛔ Chiều ĐỎ *(mã khi nhận `9af99c4` — `BG-064` dán)*:
    `psycopg.errors.QueryCanceled: canceling statement due to statement
    timeout` ở trang 2 `VND`."""
    with _ket_noi() as c:
        dem = bc.dem_hang_cho(c, chi_nap_that())
    assert dem, "⛔ không đo được: hàng chờ sổ thật rỗng (Đ3)"
    lon = max(dem, key=lambda d: d["so_dong"])
    assert lon["so_dong"] > TRANG, (
        f"⛔ không đo được: tiền tệ nhiều nhất {lon['curr']} chỉ "
        f"{lon['so_dong']} dòng — ⛔ có trang 2")
    tro, s, n = _trang_2(lon["curr"])
    print(f"WO-051 AC-5 · sổ thật · {lon['curr']} ({lon['so_dong']} dòng) "
          f"trang 2 cursor={tro}: {s:.3f} s, {n} hàng")
    assert n == min(TRANG, lon["so_dong"] - TRANG), (n, lon)


def test_AC5_SO_THAT_trang_2_MOI_tien_te_co_trang_2_trong_2s():
    """Cùng phép cho **mọi** tiền tệ có trang 2 *(lớp lỗi là "con trỏ ước ra
    nhỏ", ⛔ riêng `VND` — `WO-051` Căn cứ ⓐ)*. Mẫu số: ≥ 1 tiền tệ có trang 2."""
    with _ket_noi() as c:
        dem = [d for d in bc.dem_hang_cho(c, chi_nap_that())
               if d["so_dong"] > TRANG]
    assert dem, "⛔ không đo được: ⛔ tiền tệ nào có trang 2"
    for d in dem:
        tro, s, n = _trang_2(d["curr"])
        print(f"WO-051 AC-5 · {d['curr']} trang 2 ({tro}): {s:.3f} s")
        assert n == min(TRANG, d["so_dong"] - TRANG), (d, n)


def test_AC5_SO_THAT_view_GOM_DUNG_MOT_LAN_moi_trang():
    """⭐ Cổng **hình dạng** kế hoạch *(⛔ chỉ đồng hồ)* — `EXPLAIN (ANALYZE)`
    trên sổ thật *(chạy câu đọc — `ANALYZE` của `EXPLAIN` ⛔ phải lệnh
    `ANALYZE` thống kê; ⛔ ghi)*.

    Vì sao đồng hồ ⛔ đủ: nó có một vùng mù **đã đo được** — bản thử
    `LATERAL` ⛔ `OFFSET 0` *(bị kéo phẳng)* chạy trang 2 `VND` **1,05–1,31 s**,
    **dưới** `2 s` ⇒ hai bài trên **XANH** — trong khi view vẫn gom **cả**
    `fls_queue_event` cho **mỗi** hàng *(`loops=51` × 25 ms)* và chậm thêm theo
    mỗi sự kiện mới.

    Mong: **mọi** nút `GroupAggregate` *(chỉ view `fls_queue_state` có nó trong
    câu này)* chạy **`loops=1`** — view gom **đúng một lần** mỗi trang, bất
    kể bộ lập kế hoạch ước bao nhiêu hàng. Mẫu số: ≥ 1 nút như thế.

    ⛔ Chiều ĐỎ *(chứng ở `BG-064`)*: mã khi nhận *(`loops=4192` — chạy tới
    hạn `2s` ⇒ `QueryCanceled`, cũng ĐỎ)* · bản `LATERAL` ⛔ `OFFSET 0`
    *(`loops=51`)*."""
    import re

    from tools.do_trang_hang_cho import bat_cau
    pv = chi_nap_that()
    with _ket_noi() as c:
        dem = bc.dem_hang_cho(c, pv)
        assert dem, "⛔ không đo được: hàng chờ rỗng"
        lon = max(dem, key=lambda d: d["so_dong"])["curr"]
        t1 = bc.doc_hang_cho(c, pv, curr=lon, limit=TRANG)
        assert t1.con_tro, "⛔ không đo được: ⛔ có trang 2"
        sql, ts, _ = bat_cau(c, pv, curr=lon, con_tro=t1.con_tro)
    with _ket_noi() as c:
        ke = [r[0] for r in c.execute("EXPLAIN (ANALYZE) " + sql, ts)]
    gom = [d for d in ke if "GroupAggregate" in d]
    print("\n".join(gom))
    assert gom, "⛔ không đo được: ⛔ có nút GroupAggregate:\n" + "\n".join(ke)
    vong = [int(m.group(1)) for d in gom
            for m in [re.search(r"loops=(\d+)\)", d)] if m]
    assert len(vong) == len(gom) and set(vong) == {1}, (vong, "\n".join(ke))
