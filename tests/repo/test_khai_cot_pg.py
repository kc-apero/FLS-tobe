# -*- coding: utf-8 -*-
"""`fls/repo/khai_cot.py` trên PG THẬT — bốn luật của tầng khai có sống không.

⭐ Cổng của task `2` *(`DEV-03` §2b)*: **sửa khai ⇒ 2 bản ghi, ⛔ bản cũ ⛔ không
   đổi một ô** — bài `test_LUAT_A_sua_khai_la_THEM_ban_cu_KHONG_doi_MOT_O`.
"""
import os
from datetime import timedelta

import psycopg
import pytest

from fls.adapters.sao_ke import SAU_TRUONG
from fls.db.kho import dsn_test
from fls.repo.khai_cot import (KhongCoKhai, LoiKhai, NguonLa, doc_khai,
                               ghi_khai)

pytestmark = pytest.mark.pg

# ⛔ Kho TEST, ⛔ KHÔNG phải kho thật.
DSN = dsn_test()


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _nguon(conn) -> int:
    """Một `fls_source` RIÊNG cho mỗi bài — ⛔ không dùng chung."""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_source (source_key, src_type) "
                    "VALUES (%s,'Bank') RETURNING source_id",
                    ("R | Thu" + os.urandom(5).hex(),))
        return cur.fetchone()[0]


def _du(**doi: int) -> dict[str, int]:
    khai = {t: i for i, t in enumerate(SAU_TRUONG)}
    khai.update(doi)
    return khai


def _dem(conn, sid: int) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_khai_cot WHERE source_id = %s",
                    (sid,))
        return int(cur.fetchone()[0])


def _anh_chup(conn, sid: int, ver: int) -> list[tuple]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT khai_id, truong, cot, hieu_luc_tu, actor FROM fls_khai_cot"
            " WHERE source_id = %s AND version = %s ORDER BY truong",
            (sid, ver))
        return cur.fetchall()


# ────────────────────────────────────────────────── đường đi được, trước hết
def test_ghi_roi_doc_lai_ra_DUNG_ban_khai(conn):
    sid = _nguon(conn)
    ghi_khai(conn, sid, _du(Debit=3, Credit=4), actor="thanh")
    b = doc_khai(conn, sid)
    assert b.version == 1 and b.actor == "thanh"
    assert b.cot == _du(Debit=3, Credit=4)


def test_khuon_tra_ve_DUNG_khuon_cua_sao_ke(conn):
    """⭐ `cot` phải là `{tên trường: chỉ số cột}` — **y hệt**
    `sao_ke.doc_ban_khai()`, để task `3` đổi nguồn bản khai mà ⛔ không phải
    dịch khuôn. Mọi phép dịch giữa hai khuôn là một chỗ để lệch len vào."""
    sid = _nguon(conn)
    ghi_khai(conn, sid, _du(), actor="thanh")
    cot = doc_khai(conn, sid).cot
    assert set(cot) == set(SAU_TRUONG)
    assert all(isinstance(v, int) for v in cot.values())


# ─────────────────────────────────────────────────────────── ⓐ luật CHỈ-THÊM
def test_LUAT_A_sua_khai_la_THEM_ban_cu_KHONG_doi_MOT_O(conn):
    """⭐⭐ **CỔNG CỦA TASK 2.**

    Ngân hàng chèn thêm một cột ⇒ khai MỚI. Bản khai cũ phải còn **nguyên từng
    ô** — vì một dòng nạp tháng trước chỉ giải thích được bằng bản khai **hiệu
    lực lúc ấy**. Sửa đè là **viết lại lịch sử** *(`INV-I08`)*.
    """
    sid = _nguon(conn)
    ghi_khai(conn, sid, _du(Debit=3), actor="thanh")
    truoc = _anh_chup(conn, sid, 1)

    b2 = ghi_khai(conn, sid, _du(Debit=7), actor="huong")

    assert b2.version == 2
    assert _dem(conn, sid) == 12, "⛔ 2 bản khai = 12 dòng, ⛔ không phải 6"
    assert _anh_chup(conn, sid, 1) == truoc, (
        "⛔ bản khai v1 ĐÃ ĐỔI — kể cả `khai_id`/`hieu_luc_tu`/`actor`. "
        "Sửa đè một bản khai là viết lại lịch sử của mọi dòng đã nạp bằng nó")
    assert doc_khai(conn, sid).cot["Debit"] == 7, "đọc mặc định = bản MỚI NHẤT"


def test_ban_khai_moi_KHONG_can_giong_ban_cu(conn):
    """⛔ `version` mới là một bản khai ĐỘC LẬP, ⛔ không phải một *bản vá*."""
    sid = _nguon(conn)
    ghi_khai(conn, sid, _du(), actor="thanh")
    b2 = ghi_khai(conn, sid, {t: 10 + i for i, t in enumerate(SAU_TRUONG)},
                  actor="thanh")
    assert min(b2.cot.values()) == 10


# ────────────────────────────────────────────── ⓑ đủ 6 hoặc ⛔ không ghi gì
def test_LUAT_B_thieu_mot_truong_thi_NO_va_KHONG_ghi_DONG_NAO(conn):
    """⛔⛔ *"⛔ Không ghi một phần"* ⛔ không phải một lời hứa — nó phải **đo
    được**: đếm dòng trước và sau."""
    sid = _nguon(conn)
    thieu = _du()
    del thieu["Credit"]
    with pytest.raises(LoiKhai, match="thiếu"):
        ghi_khai(conn, sid, thieu, actor="thanh")
    assert _dem(conn, sid) == 0, "⛔ đã ghi một phần — mất cột trong im lặng"


def test_ten_LA_cung_KHONG_ghi_dong_nao(conn):
    sid = _nguon(conn)
    with pytest.raises(LoiKhai):
        ghi_khai(conn, sid, dict(_du(), Creditt=9), actor="thanh")
    assert _dem(conn, sid) == 0


def test_actor_RONG_thi_NO(conn):
    """⛔ Bản khai là **hành vi của người** — ⛔ không ai đứng tên thì ⛔ không
    ai giải thích được vì sao cột tiền lại nằm ở đó."""
    sid = _nguon(conn)
    for xau in ("", "   ", None):
        with pytest.raises(LoiKhai, match="actor"):
            ghi_khai(conn, sid, _du(), actor=xau)
    assert _dem(conn, sid) == 0


def test_doc_VAN_kiem_du_6_truong_du_ai_do_chen_TAY_vao_kho(conn):
    """⛔⛔ Một phép kiểm chỉ tin vào **chính người ghi của nó** là phép kiểm
    ⛔ không đo gì. Bản khai có thể vào kho bằng đường khác *(nạp tay, khôi
    phục dở dang)*, và cái nó thiếu có thể là **cột tiền**."""
    sid = _nguon(conn)
    with conn.cursor() as cur:                    # ⛔ chèn TAY, 5/6 trường
        cur.executemany(
            "INSERT INTO fls_khai_cot (source_id, version, truong, cot, actor)"
            " VALUES (%s,1,%s,%s,'tay')",
            [(sid, t, i) for i, t in enumerate(SAU_TRUONG) if t != "Credit"])
    with pytest.raises(LoiKhai, match="thiếu"):
        doc_khai(conn, sid)


# ───────────────────────────────────────── ⓒ hiệu lực tại một mốc / MỘT mốc
def test_SAU_dong_cua_mot_ban_khai_dung_chung_MOT_moc(conn):
    """⛔⛔ `now()` của PostgreSQL là mốc **đầu giao dịch** ⇒ cả 6 dòng chung
    một mốc. Nếu ⛔ không, một phép đọc rơi vào **giữa** 6 dòng sẽ trả về bản
    khai **5 trường** — tức `BanKhaiHong` trên một cái kho hoàn toàn **lành**."""
    sid = _nguon(conn)
    ghi_khai(conn, sid, _du(), actor="thanh")
    with conn.cursor() as cur:
        cur.execute("SELECT count(DISTINCT hieu_luc_tu) FROM fls_khai_cot"
                    " WHERE source_id = %s", (sid,))
        assert int(cur.fetchone()[0]) == 1


def test_doc_TAI_MOT_MOC_tra_ve_ban_khai_hieu_luc_LUC_AY(conn):
    """⭐⭐ Đây là thứ làm câu *"dòng nạp 27/08 đọc bằng bản khai nào"* **có câu
    trả lời** sau khi ngân hàng đổi mẫu. ⛔ Không có nó thì mọi dòng cũ lặng lẽ
    được giải thích bằng bản khai của **hôm nay**."""
    sid = _nguon(conn)
    b1 = ghi_khai(conn, sid, _du(Debit=3), actor="thanh")
    b2 = ghi_khai(conn, sid, _du(Debit=7), actor="thanh")

    assert doc_khai(conn, sid, tai=b1.hieu_luc_tu).cot["Debit"] == 3
    assert doc_khai(conn, sid, tai=b2.hieu_luc_tu).cot["Debit"] == 7
    assert doc_khai(conn, sid).cot["Debit"] == 7


def test_doc_TRUOC_khi_co_ban_khai_nao_thi_NO_chu_KHONG_doan(conn):
    """⛔ ⛔ Không có bản khai **mặc định**. Một mặc định im lặng chính là cơ chế
    đẻ ra **6.843 ô *"Input here"*** của AS-IS — sai mà ⛔ không ai thấy."""
    sid = _nguon(conn)
    b1 = ghi_khai(conn, sid, _du(), actor="thanh")
    with pytest.raises(KhongCoKhai):
        doc_khai(conn, sid, tai=b1.hieu_luc_tu - timedelta(microseconds=1))


def test_version_va_thoi_gian_KHONG_BAO_GIO_cai_nhau(conn):
    """⭐ Luật ⓒ: `hieu_luc_tu` do MÁY đặt, người gọi ⛔ không truyền vào được.

    ⇒ `version` tăng **thì** mốc cũng tăng. Nếu mở cửa cho người gọi đặt mốc
    thì *"bản khai nào đang hiệu lực"* sẽ có **hai** câu trả lời khác nhau tuỳ
    ta sắp theo `version` hay theo thời gian.
    """
    sid = _nguon(conn)
    moc = [ghi_khai(conn, sid, _du(), actor="thanh").hieu_luc_tu
           for _ in range(3)]
    assert moc == sorted(moc) and len(set(moc)) == 3


def test_ghi_khai_KHONG_nhan_tham_so_hieu_luc_tu(conn):
    """⛔ Khoá cánh cửa ấy lại bằng một bài — thêm một tham số `hieu_luc_tu`
    trông rất vô hại, và nó phá đúng bất biến ở bài trên."""
    import inspect
    assert "hieu_luc_tu" not in inspect.signature(ghi_khai).parameters


# ──────────────────────────────────── ⓓ hai câu trả lời KHÁC nhau cho 2 lỗi
def test_nguon_KHONG_CO_THAT_thi_NguonLa_ca_khi_GHI_lan_khi_DOC(conn):
    la = 10 ** 15
    with pytest.raises(NguonLa):
        ghi_khai(conn, la, _du(), actor="thanh")
    with pytest.raises(NguonLa):
        doc_khai(conn, la)


def test_nguon_CO_nhung_CHUA_KHAI_thi_KhongCoKhai_chu_KHONG_phai_NguonLa(conn):
    """⚠ `BA-07` §4b ⓺: **409 ⛔ không phải 404**. *"⛔ Không có nguồn ấy"* và
    *"có nguồn, nhưng ⛔ chưa ai khai cách đọc nó"* là **hai** câu, và chúng dẫn
    người dùng đi **hai đường sửa khác nhau**."""
    sid = _nguon(conn)
    with pytest.raises(KhongCoKhai):
        doc_khai(conn, sid)
    assert not isinstance(KhongCoKhai("x"), NguonLa)


def test_MA_LOI_dung_nhu_BA_07_khai(conn):
    """⛔ Mã lỗi là thứ tầng cửa dịch ra HTTP — sai một chữ là sai mã trạng thái."""
    assert NguonLa.ma == "FLS-NGUON-LA"
    assert KhongCoKhai.ma == "FLS-KHAI-KHONG-CO"
    assert LoiKhai.ma == "FLS-KHAI-THIEU"


def test_khai_cua_nguon_NAY_khong_ro_sang_nguon_KHAC(conn):
    """⛔ Khoá phải mang `source_id`. 60 sao kê đều có trường `Debit`; một phép
    đọc quên lọc nguồn sẽ trả bản khai của **tài khoản khác** — sai tiền, và
    ⛔ không lỗi nào nổ."""
    a, b = _nguon(conn), _nguon(conn)
    ghi_khai(conn, a, _du(Debit=3), actor="thanh")
    ghi_khai(conn, b, _du(Debit=9), actor="thanh")
    assert doc_khai(conn, a).cot["Debit"] == 3
    assert doc_khai(conn, b).cot["Debit"] == 9


def test_version_dem_RIENG_cho_tung_nguon(conn):
    a, b = _nguon(conn), _nguon(conn)
    ghi_khai(conn, a, _du(), actor="thanh")
    ghi_khai(conn, a, _du(), actor="thanh")
    assert ghi_khai(conn, b, _du(), actor="thanh").version == 1, (
        "⛔ `version` đếm chung cả kho thì nguồn mới sẽ bắt đầu từ một số lạ")


def test_GIAO_DICH_that_su_bao_ve_khi_kho_TU_CHOI_o_dong_thu_tu(conn):
    """⛔⛔ Bài `test_LUAT_B…` chứng minh **phép kiểm trước cửa** chạy — nó ⛔
    KHÔNG chứng minh **giao dịch** chạy. Hai cơ chế khác nhau, và cái thứ hai
    mới là cái đỡ những hỏng ⛔ không đoán trước được.

    Ở đây bản khai **qua được** mọi phép kiểm của ta *(6 trường, số nguyên,
    ⛔ không âm)* rồi bị **chính kho** từ chối ở một dòng giữa chừng: cột `cot`
    là `int` 4 byte. ⇒ Nếu thiếu giao dịch, kho sẽ giữ lại **một bản khai cụt**
    — và một bản khai cụt là thứ `doc_khai()` sẽ NỔ vào mặt người dùng vào một
    ngày khác, ở một chỗ khác, ⛔ không ai lần ra được vì sao.
    """
    sid = _nguon(conn)
    qua_to = _du(Credit=2 ** 40)          # ⛔ vượt `int` 4 byte của PostgreSQL
    with pytest.raises(psycopg.Error):
        ghi_khai(conn, sid, qua_to, actor="thanh")
    assert _dem(conn, sid) == 0, (
        "⛔ kho còn lại một BẢN KHAI CỤT sau khi phép ghi hỏng giữa chừng")


def test_sau_khi_ghi_HONG_van_ghi_lai_duoc_va_version_KHONG_nhay_so(conn):
    """⛔ Một lần ghi hỏng ⛔ không được **tiêu mất** một số `version`.

    Nhảy số thì dãy `version` có lỗ, và một cái lỗ trong dãy đọc y hệt *"có một
    bản khai đã bị xoá"* — mà tầng này ⛔ không hề có đường xoá nào.
    """
    sid = _nguon(conn)
    ghi_khai(conn, sid, _du(), actor="thanh")
    with pytest.raises(psycopg.Error):
        ghi_khai(conn, sid, _du(Credit=2 ** 40), actor="thanh")
    assert ghi_khai(conn, sid, _du(), actor="thanh").version == 2


# ═════════════════════════════════════════════════════════════════════════
# `QĐ-ITL-108` — hai trường THÊM của lằn quỹ. Ba bài dưới đây khoá đúng
# **cái bẫy đã cắn thật** ngày 08/09, ⛔ không phải một ca giả định.
# ═════════════════════════════════════════════════════════════════════════

def test_ghi_khai_GIU_DU_hai_truong_them_cua_lan_quy(conn):
    """⛔ Ghi 8 trường thì kho phải có **8 dòng**, ⛔ không phải 6.

    ⛔⛔ Bản trước lặp `for t in SAU_TRUONG` khi `INSERT` ⇒ hai trường thêm
       **rơi mất trong im lặng**, trong khi hàm **vẫn trả về đủ 8**.
    """
    sid = _nguon(conn)
    khai = _du()
    khai.update({"Legal Entity": 7, "CDT": 14})

    b = ghi_khai(conn, sid, khai, actor="test")
    assert b.cot == khai, "⛔ ham tra ve THIEU truong"

    with conn.cursor() as cur:
        cur.execute("SELECT truong, cot FROM fls_khai_cot"
                    " WHERE source_id = %s AND version = %s", (sid, b.version))
        trong_kho = dict(cur.fetchall())
    assert trong_kho == khai, (
        "⛔ KHO chi co %d truong trong khi ham nhan %d — hai truong THEM roi "
        "mat trong im lang" % (len(trong_kho), len(khai)))

    assert doc_khai(conn, sid).cot == khai, "⛔ doc lai ⛔ khong ra du"


def test_chay_LAI_cung_ban_khai_8_truong_KHONG_de_them_version(conn):
    """⛔⛔ Đây mới là **cái hỏng thật** của lỗi trên, và nó ⛔ không ồn ào.

    Người gọi *(`tools/nap_nguon_va_khai.py`)* so `doc_khai()` với bản khai
    vừa trích, khác thì ghi `version` mới. Nếu phép ghi **rụng** hai trường
    thì phép so **luôn luôn khác** ⇒ **mỗi lần chạy đẻ một `version` rác,
    mãi mãi** — và ⛔ không cổng nào báo, vì từng dòng riêng lẻ đều hợp lệ.

    ⭐ Bài này ⛔ không kiểm phép ghi; nó kiểm **vòng đọc-so-ghi** khép kín.
    """
    sid = _nguon(conn)
    khai = _du()
    khai.update({"Legal Entity": 7, "CDT": 14})
    ghi_khai(conn, sid, khai, actor="test")

    for _ in range(3):
        cu = doc_khai(conn, sid)
        assert cu.cot == khai, (
            "⛔ doc lai ⛔ KHONG bang thu da ghi ⇒ nguoi goi se ghi version "
            "moi, va lan sau lai the — VONG LAP VO HAN")

    with conn.cursor() as cur:
        cur.execute("SELECT count(DISTINCT version) FROM fls_khai_cot"
                    " WHERE source_id = %s", (sid,))
        assert cur.fetchone()[0] == 1


def test_moi_dong_cua_ban_khai_8_truong_dung_CHUNG_mot_moc(conn):
    """⛔ Luật cũ nói *"cả 6 dòng"*; nay có bản khai **8 dòng**.

    Một phép đọc rơi vào **giữa** sẽ thấy bản khai thiếu trường — tức
    `BanKhaiHong` trên một cái kho hoàn toàn lành.
    """
    sid = _nguon(conn)
    khai = _du()
    khai.update({"Legal Entity": 7, "CDT": 14})
    b = ghi_khai(conn, sid, khai, actor="test")

    with conn.cursor() as cur:
        cur.execute("SELECT count(*), count(DISTINCT hieu_luc_tu)"
                    " FROM fls_khai_cot WHERE source_id = %s AND version = %s",
                    (sid, b.version))
        so_dong, so_moc = cur.fetchone()
    assert so_dong == 8, "⛔ mong 8 dong, co %d" % so_dong
    assert so_moc == 1, "⛔ 8 dong mang %d moc khac nhau" % so_moc
