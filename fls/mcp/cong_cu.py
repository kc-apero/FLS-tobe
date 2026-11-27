"""Lõi công cụ MCP — CHỈ ĐỌC. Kết nối được TRUYỀN VÀO (⛔ `fls.db`, ⛔ `psycopg` — hợp đồng tầng 1).

Sáu công cụ *(tên là API công khai — đổi tên là vỡ connector của chủ)*:

| công cụ | đọc gì |
|---|---|
| `liet_ke_bang` | mọi bảng/view/khung xem của schema `public` + số dòng ĐẾM THẬT (`count(*)`, ⛔ ước `reltuples`) |
| `mo_ta_bang` | cột · kiểu · NULL được · chú thích cột + chú thích bảng |
| `truy_van_doc` | MỘT câu SELECT/WITH…SELECT — hai lớp chặn *(`chan_sql` ⇒ `chay_doc`)*, trần dòng + trần byte |
| `liet_ke_tuyen` | các tuyến ĐỌC (`GET`, `ghi=False`) của cửa `fls.api` — tên · đường · tham số · mô tả |
| `goi_tuyen` | gọi MỘT tuyến đọc bằng ĐÚNG hàm của cửa (`fls.api.xu_ly.HAM`) — ⛔ viết lại logic |
| `cong` | = `goi_tuyen("cong")` — cổng HD1/HD2 + cổng kế toán (`GET /gates`) |

⛔⛔ **Lớp chặn KHO** (`chay_doc`) — chạy được kể cả khi lớp ứng dụng bị gỡ, và bài đột biến
`tests/mcp/test_chan_sql_dot_bien.py` chạy nó RIÊNG để chứng minh:
  ⓐ kết nối do người gọi mở bằng vai `fls_doc` *(staging: chỉ `SELECT`, `default_transaction_read_only=on`)*;
  ⓑ mỗi lời gọi một giao dịch `BEGIN READ ONLY` … `ROLLBACK` — kể cả `set_config(…, false)` cũng bị
     hoàn tác *(đo 27/11: `SHOW default_transaction_read_only` sau ROLLBACK = `on`)*;
  ⓒ `SET LOCAL statement_timeout` — `pg_sleep` quá hạn bị PG huỷ `57014` *(đo: đặt lại
     `statement_timeout` = 0 BÊN TRONG câu ⛔ gỡ được hạn của chính câu ấy)*;
  ⓓ `prepare=True` ⇒ giao thức MỞ RỘNG ⇒ PG từ chối `42601` *"cannot insert multiple commands into a
     prepared statement"* *(đo: thiếu nó, `psycopg` gửi giao thức ĐƠN và `select 1; delete …` chạy CẢ HAI)*.

⭐ Nhật ký (AC-5): MỖI lời gọi ⇒ một bản ghi `{ai, cong_cu, sql_bam, so_dong, ms, ket_qua}` — băm
SHA-256 (16 hex) của câu, ⛔ câu, ⛔ nội dung trả về. Trần tốc độ theo người (cửa sổ trượt 60 giây).
"""
from __future__ import annotations

import base64
import collections
import datetime as _dt
import decimal
import hashlib
import json
import threading
import time
import uuid
from dataclasses import dataclass
from typing import Any, Callable, ContextManager

from fls.api import bang_tuyen, bao
from fls.api.xu_ly import HAM, LoiCua, YeuCau, pham_vi_cua_yeu_cau
from fls.mcp import chan_sql

MoKetNoi = Callable[[], ContextManager[Any]]
GhiNhatKy = Callable[[dict], None]

SCHEMA = "public"
# Khoá ⛔ BAO GIỜ được có trong kho (`PM_COT_RIENG_TU`, `fls/adapters`) — đo lại ở bài + BÁO CÁO 10.
COT_RIENG_TU = "Email Address"


@dataclass(frozen=True)
class CauHinh:
    han_ms: int = 5_000            # statement_timeout của MỘT câu
    tran_dong: int = 1_000         # trần cứng số dòng một lời gọi
    mac_dinh_dong: int = 200       # khi người gọi ⛔ nói
    tran_byte: int = 1_000_000     # trần byte JSON của phần `dong` — quá ⇒ cắt + `bi_cat`
    toc_do_phut: int = 60          # số lời gọi / người / 60 giây
    tep_do: Any = None             # `voi_so_luong.json` — truyền cho tuyến `cong` (như `chay_cua.py`)
    tep_hd2: Any = None            # `hd2_cong.json`


class LoiCongCu(Exception):
    """Lỗi CÓ TÊN trả cho Claude. `ma` đi vào nhật ký; ⛔ mang nội dung kho."""

    def __init__(self, ma: str, chi_tiet: str = ""):
        super().__init__(f"{ma}: {chi_tiet}" if chi_tiet else ma)
        self.ma = ma
        self.chi_tiet = chi_tiet


def bam_sql(sql: str | None) -> str | None:
    return None if sql is None else hashlib.sha256(sql.encode("utf-8")).hexdigest()[:16]


def _json_an(v: Any) -> Any:
    """Giá trị kho ⇒ JSON. ⛔ `float` cho tiền: `Decimal` ⇒ CHUỖI (giữ đủ chữ số)."""
    if v is None or isinstance(v, (bool, int, str)):
        return v
    if isinstance(v, float):
        return v if v == v and v not in (float("inf"), float("-inf")) else str(v)
    if isinstance(v, decimal.Decimal):
        return str(v)
    if isinstance(v, (_dt.datetime, _dt.date, _dt.time)):
        return v.isoformat()
    if isinstance(v, _dt.timedelta):
        return str(v)
    if isinstance(v, uuid.UUID):
        return str(v)
    if isinstance(v, (bytes, bytearray, memoryview)):
        return "base64:" + base64.b64encode(bytes(v)).decode()
    if isinstance(v, dict):
        return {str(k): _json_an(x) for k, x in v.items()}
    if isinstance(v, (list, tuple)):
        return [_json_an(x) for x in v]
    return str(v)


def _ngoac(ten: str) -> str:
    return '"' + ten.replace('"', '""') + '"'


def chay_doc(conn: Any, sql: str, gioi_han: int, han_ms: int) -> dict:
    """Lớp chặn KHO: chạy `sql` trong MỘT giao dịch READ ONLY có hạn giờ, giao thức mở rộng, ROLLBACK.

    ⛔ ⛔ KHÔNG kiểm câu — đó là việc của `chan_sql.kiem`. Hàm này phải TỰ đứng vững khi lớp kia vắng.
    Lỗi kho ⇒ `LoiCongCu("KHO_TU_CHOI", "<sqlstate>: <dòng đầu lời PG>")`.
    """
    if not (1 <= gioi_han) or not (1 <= han_ms):
        raise LoiCongCu("THAM_SO", "gioi_han/han_ms phải ≥ 1")
    conn.execute("BEGIN TRANSACTION READ ONLY")
    try:
        conn.execute(f"SET LOCAL statement_timeout = {int(han_ms)}")
        conn.execute(f"SET LOCAL lock_timeout = {int(min(han_ms, 2_000))}")
        conn.execute(f"SET LOCAL idle_in_transaction_session_timeout = {int(han_ms) * 2}")
        cur = conn.cursor()
        try:
            cur.execute(sql, prepare=True)
        except Exception as e:                                   # noqa: BLE001 — lỗi kho bất kỳ ⇒ có tên
            ma = getattr(e, "sqlstate", None) or type(e).__name__
            dong1 = (str(e).strip().splitlines() or [""])[0][:200]
            raise LoiCongCu("KHO_TU_CHOI", f"{ma}: {dong1}") from None
        cot = [d.name for d in (cur.description or [])]
        dong = cur.fetchmany(gioi_han + 1) if cur.description else []
        return {"cot": cot, "dong": [list(d) for d in dong[:gioi_han]], "bi_cat": len(dong) > gioi_han}
    finally:
        try:
            conn.execute("ROLLBACK")
        except Exception:                                        # noqa: BLE001 — kết nối hỏng: người gọi đóng
            pass


class TranTocDo:
    """Cửa sổ trượt 60 giây theo người. ⛔ Vượt ⇒ `LoiCongCu("QUA_NHANH")`."""

    def __init__(self, moi_phut: int, dong_ho: Callable[[], float] = time.monotonic):
        self.moi_phut = moi_phut
        self.dong_ho = dong_ho
        self._vet: dict[str, collections.deque] = collections.defaultdict(collections.deque)
        self._khoa = threading.Lock()

    def lay(self, ai: str) -> None:
        bay_gio = self.dong_ho()
        with self._khoa:
            q = self._vet[ai]
            while q and bay_gio - q[0] >= 60:
                q.popleft()
            if len(q) >= self.moi_phut:
                raise LoiCongCu("QUA_NHANH", f"> {self.moi_phut} lời gọi / 60 giây — chờ rồi gọi lại")
            q.append(bay_gio)


def ghi_nhat_ky_stderr(ban_ghi: dict) -> None:
    """Một dòng JSON ra **stderr** — Cloud Run đưa vào Cloud Logging (khoá `severity` + `message`).

    ⛔ stdout: ở transport stdio, stdout LÀ kênh giao thức — ghi vào đó là làm hỏng phiên MCP.
    """
    import sys
    sys.stderr.write(json.dumps({"severity": "INFO", "message": "FLS_MCP_GOI", **ban_ghi},
                                ensure_ascii=False) + "\n")
    sys.stderr.flush()


class CongCu:
    def __init__(self, mo_doc: MoKetNoi, cau_hinh: CauHinh | None = None,
                 ghi_nhat_ky: GhiNhatKy = ghi_nhat_ky_stderr):
        self.mo_doc = mo_doc
        self.ch = cau_hinh or CauHinh()
        self.ghi_nhat_ky = ghi_nhat_ky
        self.toc_do = TranTocDo(self.ch.toc_do_phut)

    # ── khung chung: trần tốc độ · đo giờ · nhật ký (⛔ nội dung) ─────────────────────────────
    def _chay(self, ai: str, cong_cu: str, viec: Callable[[], dict], sql: str | None = None) -> dict:
        bd = time.monotonic()
        ket, so_dong = "ok", None
        try:
            self.toc_do.lay(ai)
            ra = viec()
            so_dong = ra.get("so_dong")
            return ra
        except LoiCongCu as e:
            ket = e.ma
            raise
        except chan_sql.SqlBiChan as e:
            ket = "CHAN_SQL_" + e.ma
            raise LoiCongCu("CHAN_SQL", str(e)) from None
        except Exception as e:                                   # noqa: BLE001
            ket = "LOI_" + type(e).__name__
            raise LoiCongCu("LOI_NOI_BO", type(e).__name__) from None
        finally:
            self.ghi_nhat_ky({"ai": ai, "cong_cu": cong_cu, "sql_bam": bam_sql(sql), "so_dong": so_dong,
                              "ms": round((time.monotonic() - bd) * 1000, 1), "ket_qua": ket})

    def _gioi_han(self, gioi_han: int | None) -> int:
        g = self.ch.mac_dinh_dong if gioi_han is None else int(gioi_han)
        if g < 1:
            raise LoiCongCu("THAM_SO", "gioi_han phải ≥ 1")
        return min(g, self.ch.tran_dong)

    def _cat_byte(self, dong: list) -> tuple[list, bool]:
        tong, ra = 0, []
        for d in dong:
            tong += len(json.dumps(d, ensure_ascii=False))
            if tong > self.ch.tran_byte:
                return ra, True
            ra.append(d)
        return ra, False

    # ── 1 · liet_ke_bang ─────────────────────────────────────────────────────────────────────
    def _danh_sach(self, conn) -> list[tuple[str, str, str | None]]:
        r = chay_doc(conn, (
            "SELECT c.relname, CASE c.relkind WHEN 'r' THEN 'bang' WHEN 'p' THEN 'bang' WHEN 'v' THEN 'view' "
            "WHEN 'm' THEN 'view_vat_the' END, obj_description(c.oid, 'pg_class') "
            "FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace "
            f"WHERE n.nspname = '{SCHEMA}' AND c.relkind IN ('r','p','v','m') ORDER BY c.relname"),
            10_000, self.ch.han_ms)
        return [tuple(d) for d in r["dong"]]

    def liet_ke_bang(self, ai: str) -> dict:
        def viec():
            with self.mo_doc() as conn:
                ds = self._danh_sach(conn)
                if not ds:
                    return {"bang": [], "so_dong": 0}
                dem = " UNION ALL ".join(
                    f"SELECT {i}, count(*) FROM {SCHEMA}.{_ngoac(t)}" for i, (t, _, _) in enumerate(ds))
                so = {i: n for i, n in chay_doc(conn, dem, len(ds) + 1, self.ch.han_ms * 4)["dong"]}
            bang = [{"ten": t, "loai": k, "so_dong": so.get(i), "chu_thich": c}
                    for i, (t, k, c) in enumerate(ds)]
            return {"bang": bang, "so_dong": len(bang)}
        return self._chay(ai, "liet_ke_bang", viec)

    # ── 2 · mo_ta_bang ───────────────────────────────────────────────────────────────────────
    def mo_ta_bang(self, ai: str, ten: str) -> dict:
        def viec():
            with self.mo_doc() as conn:
                ds = {t: (k, c) for t, k, c in self._danh_sach(conn)}
                if ten not in ds:
                    raise LoiCongCu("KHONG_CO_BANG", f"{ten!r} ⛔ có trong schema {SCHEMA} — xem liet_ke_bang")
                lit = "'" + ten.replace("'", "''") + "'"
                r = chay_doc(conn, (
                    "SELECT a.attname, format_type(a.atttypid, a.atttypmod), NOT a.attnotnull, "
                    "col_description(a.attrelid, a.attnum) FROM pg_attribute a "
                    f"WHERE a.attrelid = ('{SCHEMA}.' || quote_ident({lit}))::regclass "
                    "AND a.attnum > 0 AND NOT a.attisdropped ORDER BY a.attnum"), 2_000, self.ch.han_ms)
            cot = [{"ten": a, "kieu": k, "null_duoc": n, "chu_thich": c} for a, k, n, c in r["dong"]]
            return {"ten": ten, "loai": ds[ten][0], "chu_thich": ds[ten][1], "cot": cot, "so_dong": len(cot)}
        return self._chay(ai, "mo_ta_bang", viec)

    # ── 3 · truy_van_doc ─────────────────────────────────────────────────────────────────────
    def truy_van_doc(self, ai: str, sql: str, gioi_han: int | None = None) -> dict:
        def viec():
            g = self._gioi_han(gioi_han)
            cau = chan_sql.kiem(sql)                 # LỚP 1 — ứng dụng
            with self.mo_doc() as conn:              # LỚP 2 — kho (vai fls_doc · READ ONLY · hạn giờ)
                r = chay_doc(conn, cau.sql, g, self.ch.han_ms)
            dong, cat_byte = self._cat_byte([_json_an(d) for d in r["dong"]])
            return {"cot": r["cot"], "dong": dong, "so_dong": len(dong), "gioi_han": g,
                    "bi_cat": r["bi_cat"] or cat_byte,
                    "ly_do_cat": "tran_dong" if r["bi_cat"] else ("tran_byte" if cat_byte else None)}
        return self._chay(ai, "truy_van_doc", viec, sql=sql if isinstance(sql, str) else None)

    # ── 4 · liet_ke_tuyen / 5 · goi_tuyen / 6 · cong ─────────────────────────────────────────
    @staticmethod
    def tuyen_doc() -> dict[str, bang_tuyen.Tuyen]:
        """Tuyến ĐỌC của cửa: `GET` và `ghi=False`. Khoá = tên hàm (`Tuyen.ham`) — duy nhất (bài canh)."""
        return {t.ham: t for t in bang_tuyen.BANG_TUYEN if t.phuong_thuc == "GET" and not t.ghi}

    def liet_ke_tuyen(self, ai: str) -> dict:
        def viec():
            ds = [{"ten": t.ham, "duong": t.duong.removeprefix(bang_tuyen.TIEN_TO),
                   "tham_so_duong": [s[1:-1] for s in t.duong.split("/") if s.startswith("{")],
                   "bang": list(t.bang), "mo_ta": t.mo_ta} for t in self.tuyen_doc().values()]
            return {"tuyen": ds, "so_dong": len(ds),
                    "ghi_chu": "tham_so ngoài tham_so_duong đi vào chuỗi truy vấn (?k=v) y như cửa HTTP"}
        return self._chay(ai, "liet_ke_tuyen", viec)

    def goi_tuyen(self, ai: str, ten: str, tham_so: dict | None = None, *, _cong_cu: str = "goi_tuyen") -> dict:
        def viec():
            t = self.tuyen_doc().get(ten)
            if t is None:
                raise LoiCongCu("KHONG_CO_TUYEN", f"{ten!r} ⛔ phải tuyến ĐỌC — xem liet_ke_tuyen")
            ts = {str(k): "" if v is None else str(v) for k, v in (tham_so or {}).items()}
            ten_duong = [s[1:-1] for s in t.duong.split("/") if s.startswith("{")]
            thieu = [x for x in ten_duong if not ts.get(x)]
            if thieu:
                raise LoiCongCu("THAM_SO", "thiếu tham số đường: " + ", ".join(thieu))
            tham = {x: ts.pop(x) for x in ten_duong}
            if any("/" in v for v in tham.values()):
                raise LoiCongCu("THAM_SO", "tham số đường ⛔ chứa '/'")
            try:
                pv = pham_vi_cua_yeu_cau(ts)
            except ValueError as e:
                raise LoiCongCu("THAM_SO", str(e)) from None
            try:
                with self.mo_doc() as conn:
                    data, trang_thai = HAM[t.ham](YeuCau(
                        conn=conn, pv=pv, q=ts, tham=tham, actor=ai, than={},
                        tep_do=self.ch.tep_do, tep_hd2=self.ch.tep_hd2))
            except LoiCua as e:
                raise LoiCongCu(e.ma, e.chi_tiet) from None
            goi = json.loads(bao.dong_goi(data, bao.meta(pv.mo_ta(), data_status=trang_thai, run_id=pv.run_id)))
            d = goi["data"]
            goi["so_dong"] = len(d) if isinstance(d, list) else (len(d.get("items", [])) if isinstance(d, dict)
                                                                   and isinstance(d.get("items"), list) else None)
            return goi
        return self._chay(ai, _cong_cu, viec)

    def cong(self, ai: str) -> dict:
        return self.goi_tuyen(ai, "cong", {}, _cong_cu="cong")
