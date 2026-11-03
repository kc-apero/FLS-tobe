# -*- coding: utf-8 -*-
"""Đo **đồng hồ** từng trang danh sách việc *(`NFR-I30` — `BA-08` v1.4)* trên
**sổ THẬT CHỈ ĐỌC**, lật **hết** mọi trang của mọi tiền tệ — `WO-051`.

⛔⛔ **Vì sao công cụ này ra đời** *(`WO-051`, `KQ-050 F-1`)*: trang 2 `VND`
của `/queue` mất **104,33 s** *(`fls-ba` đo 05/10)* trong khi 18 trang khác
**0,07–0,74 s**. Không ai thấy vì mọi phép đo trước đó chỉ đo **trang đầu**.
Gốc *(`EXPLAIN (ANALYZE, BUFFERS)` 06/10 — `BG-064`)*: con trỏ `('VND', 50)`
⇒ bộ lập kế hoạch ước lọc còn **`rows=1`** *(thật **4.192**)* ⇒ `Nested Loop
Left Join` tính lại view `fls_queue_state` *(`GroupAggregate` trên
**110.349** sự kiện)* **4.192 lần** — `182.573.086` lượt đọc bộ đệm, **111,9 s**.
⇒ Một phép đo trang đầu **⛔ bao giờ** bắt được lớp lỗi này; phải lật **hết**.

Ba phép, một lượt:
  ⓐ **ngân sách** — gọi **hàm thật** `doc_hang_cho` *(và `doc_lenh_cho`)*
     lật hết mọi trang `limit=50` cho mỗi tiền tệ **và** `curr=None`; in
     `c · số trang · số hàng · max s · trang chậm nhất`. Mỗi câu có
     `statement_timeout` *(mặc định `10s`)* ⇒ mã hỏng **đỏ trong vài giây**,
     ⛔ chờ 100 s; trang bị cắt in `⛔ HUY` *(⛔ "không thấy lệch" — `Đ5`)*.
  ⓑ **mẫu số** *(`Đ3`)* — số hàng lật được mỗi tiền tệ = `dem_hang_cho`
     **cùng lượt**; `itl_id` ⛔ trùng; `(curr, hang)` tăng nghiêm.
  ⓒ **oracle độc lập con trỏ** *(`AC-4`)* — câu `_SQL_HANG_CHO` **của mã khi
     nhận** *(`9af99c4`, chép **nguyên văn** dưới — ⛔ import từ mã mới, để
     oracle ⛔ trôi theo chính thứ nó canh)*, **⛔ con trỏ**, `LIMIT` ≥ số dòng
     *(câu ⛔ con trỏ đi `Hash Right Join`, `0,1 s`)* ⇒ danh sách đầy đủ; so
     **từng hàng** với các trang nối lại theo
     `(itl_id, hang, luy_ke_pct, reason, defer_until, defer_count)` + mọi cột
     còn lại của hàng.

⛔ Ghi: **0**. Nối qua `noi_chi_doc` *(`default_transaction_read_only = on` —
kho tự chối mọi phép ghi)*; `SET statement_timeout` là của **phiên**, ⛔ lưu.

Chạy::

    PYTHONUTF8=1 .venv/Scripts/python.exe tools/do_trang_hang_cho.py
    … --het-gio 120s          # đo mã cũ tới cùng (trang 2 VND ~100 s)
    … --explain VND:50        # EXPLAIN (ANALYZE, BUFFERS) một trang /queue

Mã thoát: `0` mọi trang ≤ ngân sách **và** mẫu số khớp **và** oracle lệch `0`;
`1` khác — kể cả **⛔ đo được** *(sổ tắt, tập rỗng, trang bị huỷ)*.
"""
from __future__ import annotations

import argparse
import sys
import time
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fls.db.kho import dsn_that, noi_chi_doc  # noqa: E402
from fls.repo import doc_bao_cao as bc  # noqa: E402
from fls.repo.lenh_cho import doc_lenh_cho  # noqa: E402
from fls.repo.pham_vi import chi_nap_that  # noqa: E402

#: `NFR-I30` — một trang danh sách việc ≤ `2 s` *(`BA-08` v1.4)*
NGAN_SACH_S = 2.0
TRANG = 50

#: ⭐ Oracle: `_CTE_HANG_CHO` + `_SQL_HANG_CHO` **của mã khi nhận** `9af99c4`
#: *(`fls/repo/doc_bao_cao.py:494-531`)*, bỏ vế con trỏ — **chép nguyên văn**,
#: ⛔ import. Câu ⛔ con trỏ của mã cũ đo nhanh *(trang đầu `0,09 s` — ước
#: hàng đúng ⇒ `Hash Right Join`, view tính **một** lần)* nên nó là thước
#: đúng cho câu **có** con trỏ.
_ORACLE = """
WITH q AS (
  SELECT i.itl_id, i.doc_date, i.doc_no, i.curr, i.le, i.memo,
         COALESCE(i.ps_no, 0) + COALESCE(i.ps_co, 0) AS tien
  FROM fls_itl i
  WHERE i.work_status = 'UNMAPPED' AND {dk}
    AND NOT EXISTS (SELECT 1 FROM fls_da_xong x WHERE x.itl_id = i.itl_id)
), x AS (
  SELECT q.*,
         row_number() OVER w AS hang,
         round(100.0 * SUM(q.tien) OVER (PARTITION BY q.curr
                                         ORDER BY q.tien DESC, q.itl_id
                                         ROWS UNBOUNDED PRECEDING)
               / NULLIF(SUM(q.tien) OVER (PARTITION BY q.curr), 0), 2)
           AS luy_ke_pct
  FROM q
  WINDOW w AS (PARTITION BY q.curr ORDER BY q.tien DESC, q.itl_id)
)
SELECT x.itl_id, x.doc_date, x.doc_no, x.curr, x.le, x.memo, x.tien,
       x.hang, x.luy_ke_pct,
       s.reason, s.defer_until, s.defer_count
FROM x LEFT JOIN fls_queue_state s ON s.itl_id = x.itl_id
WHERE TRUE {them}
ORDER BY x.curr, x.hang
"""


def oracle_hang_cho(conn, pv, curr: str | None) -> list[dict]:
    """Danh sách **đầy đủ** theo câu mã khi nhận, ⛔ con trỏ, ⛔ `LIMIT`."""
    dk, ts = pv.dieu_kien("i.run_id")
    them = ""
    if curr:
        them = "AND x.curr = %s"
        ts.append(curr)
    with conn.cursor() as cur:
        cur.execute(_ORACLE.format(dk=dk, them=them), ts)
        ten = [d.name for d in cur.description]
        return [dict(zip(ten, r)) for r in cur.fetchall()]


def ket_noi_moi(het_gio: str):
    """Một kết nối **MỚI**, chỉ đọc, `statement_timeout` của phiên.

    ⛔⛔ **Vì sao mỗi trang một kết nối mới — bẫy đã cắn ngay lượt đo đầu
    (06/10).** Bản đầu công cụ này dùng **một** kết nối cho mọi trang và báo
    trang 2 `VND` **0,088 s** — *XANH* — trong khi cùng giờ, cùng câu, hàm thật
    trên kết nối mới mất **97,98 s**. Gốc: `psycopg` 3 tự **chuẩn bị**
    *(`prepare`)* một câu sau **5** lần chạy cùng chữ *(`prepare_threshold=5`)*;
    80 trang `USD` chạy trước đã chạy câu có con trỏ **cùng chữ** ⇒ tới `VND`
    PostgreSQL dùng **kế hoạch chung** *(generic plan — ⛔ biết giá trị con
    trỏ ⇒ ⛔ ước `rows=1`)* ⇒ `Hash Right Join` ⇒ nhanh. Cửa thật **⛔ bao
    giờ** được như thế: `tools/chay_cua.py::_mo_ket_noi` mở **một kết nối mới
    mỗi lượt gọi** ⇒ luôn kế hoạch riêng ⇒ luôn `Nested Loop`.
    ⇒ Đo như cửa: kết nối mới mỗi trang. Đồng hồ **chỉ** quanh hàm *(⛔ tính
    giờ mở kết nối — cửa cũng mở nó, nhưng ngoài câu đang bị đo)*."""
    c = noi_chi_doc(dsn_that())
    c.execute("SELECT set_config('statement_timeout', %s, false)", (het_gio,))
    return c


def lat_het(goi, nhan: str, het_gio: str) -> dict:
    """Lật hết mọi trang qua `goi(conn, con_tro) -> Trang`; đồng hồ quanh
    **mỗi** lượt; **mỗi** lượt một kết nối mới *(xem `ket_noi_moi`)*.

    Trang bị `statement_timeout` huỷ ⇒ ghi `huy` và **dừng** *(⛔ đoán phần
    còn lại)*."""
    dong: list[dict] = []
    gio: list[float] = []
    tro = None
    huy = None
    while True:
        c = ket_noi_moi(het_gio)
        t0 = time.perf_counter()
        try:
            tr = goi(c, tro)
        except Exception as e:                      # noqa: BLE001
            gio.append(time.perf_counter() - t0)
            huy = f"trang {len(gio)} ({tro}): {type(e).__name__}"
            c.close()
            break
        gio.append(time.perf_counter() - t0)
        c.close()
        dong += tr.dong
        tro = tr.con_tro
        if not tro:
            break
    cham = max(range(len(gio)), key=lambda k: gio[k])
    return {"nhan": nhan, "dong": dong, "gio": gio, "max": gio[cham],
            "trang_cham": cham + 1, "huy": huy}


def _cot_so(d: dict) -> tuple:
    return tuple((k, d[k]) for k in sorted(d))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--het-gio", default="10s",
                    help="statement_timeout mỗi câu (mặc định 10s)")
    ap.add_argument("--explain", metavar="CURR:HANG",
                    help="chỉ in EXPLAIN (ANALYZE, BUFFERS) một trang /queue")
    ap.add_argument("--bo-lenh-cho", action="store_true",
                    help="bỏ phép /lenh-cho (AC-3)")
    a = ap.parse_args()

    conn = noi_chi_doc(dsn_that())
    ro = conn.execute("SHOW transaction_read_only").fetchone()[0]
    if ro != "on":
        print(f"⛔ phiên ⛔ chỉ đọc (transaction_read_only={ro}) — dừng")
        return 1
    conn.execute("SELECT set_config('statement_timeout', %s, false)",
                 (a.het_gio,))
    pv = chi_nap_that()
    print(f"sổ THẬT chỉ đọc · transaction_read_only={ro} · "
          f"statement_timeout={a.het_gio} · ngân sách {NGAN_SACH_S} s/trang")

    if a.explain:
        return _explain(conn, pv, a.explain)

    dem = {d["curr"]: d["so_dong"] for d in bc.dem_hang_cho(conn, pv)}
    tong = sum(dem.values())
    print(f"dem_hang_cho: {dem} · Σ {tong} dòng")
    if not tong:
        print("⛔ KHÔNG ĐO ĐƯỢC: hàng chờ rỗng (Đ3)")
        return 1
    xau: list[str] = []

    # ── ⓐ ⓑ ⓒ `/queue` ────────────────────────────────────────────────────
    print("\n/queue · doc_hang_cho(chi_nap_that(), curr=c, limit=50)")
    print(f"{'c':<6}{'trang':>6}{'hàng':>7}{'dem':>7}{'max s':>9}"
          f"{'trang chậm':>12}{'Σ s':>9}  oracle")
    gop: list[dict] = []
    for c in sorted(dem) + [None]:
        r = lat_het(lambda k, tro, c=c: bc.doc_hang_cho(
            k, pv, curr=c, con_tro=tro, limit=TRANG), c or "None", a.het_gio)
        ds = r["dong"]
        mong_n = dem[c] if c else tong
        ghi = []
        if r["huy"]:
            ghi.append(f"⛔ HUY {r['huy']}")
        if len(ds) != mong_n:
            ghi.append(f"⛔ hàng {len(ds)} ≠ dem {mong_n}")
        ids = [d["itl_id"] for d in ds]
        if len(ids) != len(set(ids)):
            ghi.append(f"⛔ itl_id trùng {len(ids) - len(set(ids))}")
        khoa = [(d["curr"], d["hang"]) for d in ds]
        if any(khoa[k] >= khoa[k + 1] for k in range(len(khoa) - 1)):
            ghi.append("⛔ (curr, hang) ⛔ tăng nghiêm")
        if r["max"] > NGAN_SACH_S:
            ghi.append(f"⛔ trang {r['trang_cham']} {r['max']:.2f} s > "
                       f"{NGAN_SACH_S}")
        orc = oracle_hang_cho(conn, pv, c)
        lech = sum(1 for k in range(max(len(orc), len(ds)))
                   if k >= len(orc) or k >= len(ds)
                   or _cot_so(orc[k]) != _cot_so(ds[k]))
        if not orc:
            ghi.append("⛔ oracle rỗng (Đ3)")
        if lech:
            ghi.append(f"⛔ oracle lệch {lech}/{len(orc)}")
        if c:
            gop += ds
        print(f"{r['nhan']:<6}{len(r['gio']):>6}{len(ds):>7}{mong_n:>7}"
              f"{r['max']:>9.3f}{r['trang_cham']:>12}{sum(r['gio']):>9.2f}"
              f"  lệch {lech}/{len(orc)}"
              + ("" if not ghi else "  " + " · ".join(ghi)))
        xau += [f"/queue {r['nhan']}: {g}" for g in ghi]
    print(f"Σ bốn tiền tệ lật được: {len(gop)} / dem {tong}")

    # ── do_phu_hang_cho(90) — CTE chung ⛔ đổi ⇒ phải ra cùng số ──────────
    dp = {d["curr"]: (d["so_dong_cho"], d["so_dong_phu"], d["pct_that"])
          for d in bc.do_phu_hang_cho(conn, pv, Decimal(90))}
    print(f"\ndo_phu_hang_cho(90): {dp}")

    # ── `/lenh-cho` — cùng khuôn con trỏ (`AC-3`) ──────────────────────────
    if not a.bo_lenh_cho:
        print("\n/lenh-cho · doc_lenh_cho(chi_nap_that(), curr=c, limit=50)")
        print(f"{'c':<6}{'trang':>6}{'hàng':>7}{'max s':>9}{'trang chậm':>12}"
              f"{'Σ s':>9}")
        # ⚠ tập tiền tệ lấy từ **chính** danh sách ⛔ lọc *(lật hết bên dưới)*
        r0 = lat_het(lambda k, tro: doc_lenh_cho(k, pv, con_tro=tro,
                                                 limit=TRANG), "None",
                     a.het_gio)
        tien_te = sorted({d["curr"] for d in r0["dong"]})
        for c in tien_te + [None]:
            r = r0 if c is None else lat_het(
                lambda k, tro, c=c: doc_lenh_cho(k, pv, curr=c, con_tro=tro,
                                                 limit=TRANG), c, a.het_gio)
            ghi = []
            if r["huy"]:
                ghi.append(f"⛔ HUY {r['huy']}")
            if not r["dong"]:
                ghi.append("⛔ rỗng (Đ3)")
            if r["max"] > NGAN_SACH_S:
                ghi.append(f"⛔ trang {r['trang_cham']} {r['max']:.2f} s")
            print(f"{r['nhan']:<6}{len(r['gio']):>6}{len(r['dong']):>7}"
                  f"{r['max']:>9.3f}{r['trang_cham']:>12}{sum(r['gio']):>9.2f}"
                  + ("" if not ghi else "  " + " · ".join(ghi)))
            xau += [f"/lenh-cho {r['nhan']}: {g}" for g in ghi]

    print()
    if xau:
        print(f"⛔ ĐỎ — {len(xau)} điều:")
        for g in xau:
            print("  " + g)
        return 1
    print("✅ XANH — mọi trang ≤ ngân sách · mẫu số khớp · oracle lệch 0")
    return 0


def bat_cau(conn, pv, *, curr: str | None, con_tro: str | None,
            limit: int = TRANG) -> tuple[str, list, float]:
    """Chạy **hàm thật** `doc_hang_cho` và bắt **đúng câu** nó gửi
    *(`sql`, tham số, giây)* — bằng một con trỏ bọc `execute`.

    ⛔ Dựng lại SQL tay để `EXPLAIN` là đo một câu **khác** *(`11` §6: *"đo
    quan hệ thì gọi hàm thật"* — dựng tay ra **2/35** thay vì **18/35**)*."""
    bat: dict = {}

    class _Cur:
        def __init__(self, cur):
            self.cur = cur

        def __enter__(self):
            return self

        def __exit__(self, *_):
            self.cur.close()

        def execute(self, sql, ts=None):
            bat["sql"], bat["ts"] = sql, ts
            return self.cur.execute(sql, ts)

        def __getattr__(self, k):
            return getattr(self.cur, k)

    class _Conn:
        def cursor(self):
            return _Cur(conn.cursor())

    t0 = time.perf_counter()
    bc.doc_hang_cho(_Conn(), pv, curr=curr, con_tro=con_tro, limit=limit)
    return bat["sql"], bat["ts"], time.perf_counter() - t0


def _explain(conn, pv, ct: str) -> int:
    """`EXPLAIN (ANALYZE, BUFFERS)` **đúng câu** hàm thật gửi."""
    c, _h = ct.split(":", 1)
    sql, ts, s = bat_cau(conn, pv, curr=c, con_tro=ct)
    print(f"hàm thật doc_hang_cho(curr={c!r}, con_tro={ct!r}): {s:.3f} s")
    t0 = time.perf_counter()
    for (dong,) in conn.execute("EXPLAIN (ANALYZE, BUFFERS) " + sql,
                                ts).fetchall():
        print(dong)
    print(f"(EXPLAIN ANALYZE {time.perf_counter() - t0:.3f} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
