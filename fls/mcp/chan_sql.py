"""Lớp chặn ỨNG DỤNG cho `truy_van_doc` — thuần, ⛔ kho, ⛔ `psycopg`.

⛔⛔ Đây là lớp THỨ NHẤT trong HAI. Lớp thứ hai ở kho *(`cong_cu.chay_doc`)*: vai `fls_doc` chỉ
SELECT *(`tools/staging/sql/02b_phan_quyen.sql`)* · giao dịch `BEGIN READ ONLY` · `statement_timeout`
· giao thức MỞ RỘNG *(`prepare=True` — PG từ chối nhiều câu trong một lệnh)*. Bài
`tests/mcp/test_chan_sql_dot_bien.py` chạy từng câu đột biến QUA CẢ HAI lớp RIÊNG RẼ ⇒ một lớp bị gỡ
thì lớp kia vẫn chặn, và gỡ một lớp thì bài của lớp ấy ĐỎ.

⭐ Vì sao lớp ứng dụng vẫn cần khi kho đã chặn ghi: kho chặn GHI, ⛔ chặn được hết TÁC DỤNG PHỤ của một
câu đọc — `pg_sleep` *(giữ kết nối)*, `pg_advisory_lock` *(khoá phiên)*, `set_config` *(đổi tham số
phiên)*, `lo_*`/`pg_read_file` *(đọc tệp máy chủ — vai `fls_doc` ⛔ có quyền, nhưng một vai cấu hình
sai thì có)*. Đo 27/11 trên PG 16 cục bộ: `select pg_advisory_lock(1)` trong giao dịch READ ONLY ⇒ **chạy
được** — chỉ lớp này chặn nó.

Cách làm: TÁCH câu thành từ vựng *(chuỗi '…' · E'…' · $thẻ$…$thẻ$ · "định danh" · chú thích -- và
/* */ lồng nhau)* rồi xét PHẦN MÃ. Từ khoá nằm trong chuỗi ⛔ bị bắt nhầm *(`WHERE memo LIKE
'%delete%'` đi qua)*; định danh trong ngoặc kép bị xét như MÃ *(`"set_config"(…)` ⛔ lách được)* —
đổi lại một cột tên `"update"` bị từ chối: bảo thủ, chấp nhận.
"""
from __future__ import annotations

import re
from dataclasses import dataclass

DAI_TOI_DA = 20_000  # ký tự — một câu đọc của người hỏi ⛔ cần hơn; dài hơn là dấu hiệu lạ

# Từ khoá ⛔ được xuất hiện ở BẤT KỲ đâu trong phần mã. `INTO` bắt `SELECT … INTO bảng` (tạo bảng).
TU_CAM: frozenset[str] = frozenset("""
INSERT UPDATE DELETE MERGE UPSERT DROP CREATE ALTER TRUNCATE COPY GRANT REVOKE SET RESET CALL DO
LOCK VACUUM ANALYZE CLUSTER REINDEX COMMENT SECURITY REFRESH DISCARD LISTEN NOTIFY UNLISTEN PREPARE
EXECUTE DEALLOCATE IMPORT LOAD CHECKPOINT BEGIN START COMMIT ROLLBACK SAVEPOINT RELEASE INTO
""".split())

# Hàm có TÁC DỤNG PHỤ (đọc tệp máy chủ · khoá · ngủ · đổi tham số · đẩy sequence · ra mạng).
_HAM_CAM = re.compile(
    r"\b(set_config|pg_sleep\w*|pg_read_\w+|pg_ls_\w+|pg_stat_file|pg_file_\w+|lo_\w+|dblink\w*"
    r"|pg_terminate_backend|pg_cancel_backend|pg_reload_conf|pg_rotate_logfile|pg_\w*advisory\w*"
    r"|nextval|setval|pg_notify|txid_current\w*|pg_current_xact_id\w*|pg_switch_wal|pg_create_\w+"
    r"|pg_drop_\w+|pg_logical_\w+|pg_replication_\w+|query_to_xml\w*|table_to_xml\w*|cursor_to_xml\w*"
    r"|pg_import_system_collations|pg_promote|pg_log_backend_memory_contexts)\s*\(",
    re.IGNORECASE)
_KHOA_DONG = re.compile(r"\bFOR\s+(UPDATE|SHARE|NO\s+KEY|KEY)\b", re.IGNORECASE)
_TU = re.compile(r"[A-Za-z_][A-Za-z0-9_$]*")
_DOLLAR = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)?\$")


class SqlBiChan(ValueError):
    """Câu bị lớp ỨNG DỤNG từ chối. `ma` là mã CÓ TÊN để nhật ký + bài đếm được."""

    def __init__(self, ma: str, chi_tiet: str):
        super().__init__(f"{ma}: {chi_tiet}")
        self.ma = ma
        self.chi_tiet = chi_tiet


@dataclass(frozen=True)
class CauDaKiem:
    sql: str            # câu gốc (đã bỏ `;` cuối nếu có) — đưa nguyên cho kho
    tu_dau: str         # SELECT | WITH


def _tach_ma(sql: str) -> str:
    """Trả PHẦN MÃ: chuỗi ⇒ `''`, chú thích ⇒ dấu cách, "định danh" ⇒ chữ trần (để bị xét).

    ⛔ Chuỗi/chú thích/ngoặc kép chưa đóng ⇒ `SqlBiChan` (⛔ đoán ý).
    """
    ra: list[str] = []
    i, n = 0, len(sql)
    while i < n:
        c = sql[i]
        if c == "-" and sql.startswith("--", i):
            j = sql.find("\n", i)
            i = n if j < 0 else j
            ra.append(" ")
        elif c == "/" and sql.startswith("/*", i):
            sau, i = 1, i + 2
            while i < n and sau:
                if sql.startswith("/*", i):
                    sau, i = sau + 1, i + 2
                elif sql.startswith("*/", i):
                    sau, i = sau - 1, i + 2
                else:
                    i += 1
            if sau:
                raise SqlBiChan("CHU_THICH_HO", "chú thích /* chưa đóng")
            ra.append(" ")
        elif c in "uU" and sql.startswith("&", i + 1):
            # U&'…' / U&"…" mã hoá thoát Unicode ⇒ định danh `"\0073et_config"` lách được phép soi.
            raise SqlBiChan("UNICODE_ESCAPE", "⛔ nhận U&'…' / U&\"…\"")
        elif c == "'" or (c in "eEbBxXnN" and i + 1 < n and sql[i + 1] == "'"
                          and (i == 0 or not (sql[i - 1].isalnum() or sql[i - 1] == "_"))):
            thoat = c in "eE"
            i = i + 1 if c == "'" else i + 2
            while True:
                if i >= n:
                    raise SqlBiChan("CHUOI_HO", "chuỗi '…' chưa đóng")
                if thoat and sql[i] == "\\":
                    i += 2
                    continue
                if sql[i] == "'":
                    if sql.startswith("''", i):
                        i += 2
                        continue
                    i += 1
                    break
                i += 1
            ra.append("''")
        elif c == '"':
            j = i + 1
            ten: list[str] = []
            while True:
                if j >= n:
                    raise SqlBiChan("DINH_DANH_HO", 'định danh "…" chưa đóng')
                if sql[j] == '"':
                    if sql.startswith('""', j):
                        ten.append('"')
                        j += 2
                        continue
                    break
                ten.append(sql[j])
                j += 1
            i = j + 1
            # Xét định danh NHƯ MÃ: ký tự lạ ⇒ `_` để `\b…\b` vẫn khớp từ bên trong.
            ra.append(" " + re.sub(r"\W", "_", "".join(ten)) + " ")
        elif c == "$" and (m := _DOLLAR.match(sql, i)) and (i == 0 or not (sql[i - 1].isalnum() or sql[i - 1] == "_")):
            the = m.group(0)
            j = sql.find(the, m.end())
            if j < 0:
                raise SqlBiChan("CHUOI_HO", f"chuỗi {the}…{the} chưa đóng")
            i = j + len(the)
            ra.append("''")
        else:
            ra.append(c)
            i += 1
    return "".join(ra)


def kiem(sql: str) -> CauDaKiem:
    """⛔ NÉM `SqlBiChan` nếu `sql` ⛔ phải MỘT câu SELECT/WITH…SELECT vô hại. Trả câu đã kiểm.

    Mặc định là TỪ CHỐI: câu rỗng · quá dài · nhiều câu · từ đầu khác SELECT/WITH · từ khoá cấm ·
    hàm có tác dụng phụ · khoá dòng (`FOR UPDATE/SHARE`).
    """
    if not isinstance(sql, str) or not sql.strip():
        raise SqlBiChan("RONG", "câu rỗng")
    if len(sql) > DAI_TOI_DA:
        raise SqlBiChan("QUA_DAI", f"{len(sql)} ký tự > {DAI_TOI_DA}")
    if "\x00" in sql:
        raise SqlBiChan("KY_TU_LA", "ký tự NUL")
    ma = _tach_ma(sql)
    than = ma.rstrip()
    goc = sql.rstrip()
    if than.endswith(";"):          # MỘT `;` cuối được bỏ — nhiều hơn là nhiều câu
        than = than[:-1].rstrip()
        goc = goc[:-1].rstrip()
    if ";" in than:
        raise SqlBiChan("NHIEU_CAU", "⛔ nhận nhiều câu (`;` giữa câu)")
    tu = [t.upper() for t in _TU.findall(than)]
    if not tu or tu[0] not in ("SELECT", "WITH"):
        raise SqlBiChan("KHONG_PHAI_SELECT", f"câu phải bắt đầu bằng SELECT/WITH (nhận {tu[0] if tu else '∅'})")
    cam = sorted(set(tu) & TU_CAM)
    if cam:
        raise SqlBiChan("TU_KHOA_CAM", "từ khoá cấm: " + ", ".join(cam))
    if (m := _HAM_CAM.search(than)):
        raise SqlBiChan("HAM_CAM", f"hàm có tác dụng phụ: {m.group(1)}")
    if _KHOA_DONG.search(than):
        raise SqlBiChan("KHOA_DONG", "⛔ khoá dòng (FOR UPDATE/SHARE)")
    return CauDaKiem(sql=goc, tu_dau=tu[0])
