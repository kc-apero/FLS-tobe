# -*- coding: utf-8 -*-
"""`CHECK` trong khuôn khai báo — `QĐ-ITL-113`, cột `fls_khai_cot.thu_tu`.

⛔⛔ **Trước 08/09 `pg_verify` so `FK` · khoá chính · `UNIQUE` — và ⛔ KHÔNG so
   `CHECK`.** Nên một `CHECK` khai trong `schema.py` mà ⛔ chưa ai `ALTER TABLE`
   sẽ đi qua **im lặng**: đúng họ với hai lô đã sinh ra chính cổng ấy.

⚠ **Đo 08/09 trước khi mở cổng:** kho THẬT có **0** ràng buộc `CHECK` ⇒ mở nó
  ⛔ không phải hoà giải nợ cũ, và nó **đỏ được ngay** cột đầu tiên.

⛔⛔ **VÀ MỘT BÀI HỌC ĐÃ TRẢ GIÁ NGAY TRONG LƯỢT NÀY, ghi lại chứ ⛔ không
   giấu.** Phép thử tay đầu tiên của tôi báo *"`DMY` LỌT"* ⇒ tôi tưởng ràng
   buộc ⛔ không chặn. Sai: câu `INSERT … SELECT … FROM fls_source LIMIT 1`
   chèn **0 dòng** *(kho test có `fls_source` **rỗng**)*, nên `CHECK` ⛔ **không
   có gì mà xét** — và tôi đọc *"0 dòng"* thành *"lọt"*. ⇒ Đúng luật nền: **đo
   được 0 thứ ⇒ ⛔ KHÔNG ĐẠT**.

⇒ Nên mọi bài ở đây **đếm `rowcount`** thay vì chỉ bắt/⛔ không bắt ngoại lệ.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.db.model import Column as C
from fls.db.model import Table
from fls.db.pg_verify import so_sanh_voi_db
from fls.db.render import render_ddl
from fls.db.schema import TABLES


# ─────────────────────────────────────────────────────────── ⓐ sinh DDL
def test_check_muc_cot_ra_rang_buoc_muc_bang_CO_TEN():
    """⛔ Có tên, ⛔ không phải `CHECK` nội dòng khuyết danh.

    Postgres tự đặt tên cho `CHECK` khuyết danh *(`thu_check`, `thu_check1`,
    …)*, và lúc ấy cổng ⛔ không còn cách nào nói *"ràng buộc **này** khai mà
    ⛔ chưa áp"* — nó chỉ đếm được số lượng.
    """
    t = Table(name="thu", columns=(C("a", "text", check="a IN ('x', 'y')"),))
    ddl = render_ddl(t)
    assert "CONSTRAINT thu_a_ck CHECK (a IN ('x', 'y'))" in ddl
    # ⛔ ⛔ và ⛔ KHÔNG được dán vào định nghĩa cột
    assert "a text," in ddl or "a text\n" in ddl, ddl


def test_cot_KHONG_khai_check_thi_KHONG_sinh_rang_buoc_nao():
    """⛔ Chống *"xanh vì sinh ra cho mọi cột"* — 0 khai ⇒ 0 ràng buộc."""
    t = Table(name="thu", columns=(C("a", "text"), C("b", "int")))
    assert "_ck CHECK" not in render_ddl(t)


# ─────────────────────────────────────────────── ⓑ cổng `pg_verify` cắn được
@pytest.mark.pg
def test_pg_verify_DO_khi_CHECK_khai_ma_kho_CHUA_AP():
    """⭐⭐ Cổng phải **đỏ được** — ⛔ không thì nó ⛔ chưa đo gì.

    Dựng một bản khai có `CHECK` cho **một bảng đang tồn tại thật** nhưng ràng
    buộc ấy ⛔ chưa bao giờ được áp ⇒ `pg_verify` phải nêu ra.
    """
    goc = TABLES["fls_source"]
    gia = Table(
        name=goc.name, kind=goc.kind, erd_entity=goc.erd_entity,
        island_reason=goc.island_reason, pk_cols=goc.pk_cols,
        unique_keys=goc.unique_keys,
        columns=tuple(
            C(c.name, c.type, null=c.null, default=c.default, fk=c.fk, pk=c.pk,
              unique=c.unique, generated=c.generated, comment=c.comment,
              check="src_type IN ('bank', 'cash')" if c.name == "src_type"
                    else c.check)
            for c in goc.columns))
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        lech = so_sanh_voi_db(c, {goc.name: gia})
    assert any("CHECK khai bao co, DB THIEU" in x and "fls_source_src_type_ck" in x
               for x in lech), lech


@pytest.mark.pg
def test_CHECK_cua_thu_tu_da_AP_that__khai_bao_khop_kho():
    """Bản khai thật ↔ kho thật, ⛔ chỉ trục `CHECK`."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        lech = [x for x in so_sanh_voi_db(c, TABLES) if "CHECK" in x]
    assert lech == [], lech


# ────────────────────────────────────── ⓒ ⭐⭐ ràng buộc CHẶN THẬT, đếm dòng
@pytest.fixture()
def nguon():
    """Một nguồn THẬT — ⛔ vì `CHECK` ⛔ không xét được một câu chèn 0 dòng."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        sid = c.execute(
            "INSERT INTO fls_source (source_key, src_type) VALUES "
            "('R | THU-CHECK-THU-TU', 'bank') RETURNING source_id").fetchone()[0]
        try:
            yield c, sid
        finally:
            c.execute("DELETE FROM fls_khai_cot WHERE source_id = %s", (sid,))
            c.execute("DELETE FROM fls_source WHERE source_id = %s", (sid,))


def _chen(c, sid, truong, thu_tu, ver) -> int | None:
    """Trả số dòng vào được, hay `None` nếu ràng buộc chặn."""
    try:
        return c.execute(
            "INSERT INTO fls_khai_cot (source_id, version, truong, cot, actor,"
            " thu_tu) VALUES (%s, %s, %s, 0, 'bo-test', %s)",
            (sid, ver, truong, thu_tu)).rowcount
    except psycopg.errors.CheckViolation:
        return None


@pytest.mark.pg
@pytest.mark.parametrize("truong,thu_tu", [
    ("Date", "DMY"),        # ⛔ hoa — mot cot text tu do se co ba cach viet
    ("Date", "d/m/y"),      # ⛔ cach viet khac
    ("Date", "dd/mm/yyyy"),
    ("Debit", "mdy"),       # ⛔⛔ `thu_tu` tren truong KHAC `Date` la vo nghia
])
def test_thu_tu_LA_thi_kho_CHAN(nguon, truong, thu_tu):
    c, sid = nguon
    assert _chen(c, sid, truong, thu_tu, 91) is None, (truong, thu_tu)


@pytest.mark.pg
@pytest.mark.parametrize("truong,thu_tu,ver", [
    ("Date", "dmy", 92),
    ("Date", "mdy", 93),
    ("Date", None, 94),     # ⭐ `NULL` = *"nguon CHUA khai"* — phai vao duoc
    ("Debit", None, 95),    # 5/6 truong khong bao gio mang `thu_tu`
])
def test_thu_tu_DUNG_thi_kho_NHAN(nguon, truong, thu_tu, ver):
    """⛔ Chống *"chặn tất cả rồi báo xanh"* — ràng buộc phải **cho lọt** thứ đúng."""
    c, sid = nguon
    assert _chen(c, sid, truong, thu_tu, ver) == 1, (truong, thu_tu)
