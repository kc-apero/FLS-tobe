# -*- coding: utf-8 -*-
"""`fls/repo/chup.py` trên PG THẬT — lằn ẢNH CHỤP *(`QĐ-ITL-110`, task `9b`)*.

⭐ **Cổng của task `9b`** *(`DEV-03` §2b)*: **chụp hai lần ⇒ hai `chup_id`, và
   ảnh cũ ⛔ không đổi một ô.**

⛔⛔ **Và bài đắt nhất ở đây ⛔ KHÔNG phải bài ghi-rồi-đọc.** Nó là
   `test_KIEU_O_giu_duoc_...`: ảnh chụp mà ép ô về chuỗi thì nó **dựng lại đúng
   cái bẫy đã cắn HAI lần** — `doc_cot` ép sê-ri ngày thành `"45586"`
   *(`QĐ-ITL-102` ⓶)* và làm `L6` của cổng #17 đo được **0 dòng** ⇒ đỏ. Một
   bài ghi-rồi-đọc bằng chuỗi sẽ **XANH** trên chính cái bẫy ấy.
"""
import os

import psycopg
import pytest

from fls.adapters.sao_ke import KHAI_ANH_CHUP, chuyen, hang_tu_o
from fls.db.kho import dsn_test
from fls.repo import chup as ch

pytestmark = pytest.mark.pg

# ⛔ Kho TEST, ⛔ KHÔNG phải kho thật.
DSN = dsn_test()


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _nguon(conn, lan: str = "Bank") -> int:
    """Một `fls_source` RIÊNG cho mỗi bài — ⛔ không dùng chung."""
    with conn.cursor() as cur:
        cur.execute("INSERT INTO fls_source (source_key, src_type) "
                    "VALUES (%s, %s) RETURNING source_id",
                    ("R | Chup" + os.urandom(5).hex(), lan))
        return cur.fetchone()[0]


def _o(**doi):
    o = {"Date": 45586, "Currency": "VND", "Debit": 1000, "Credit": "",
         "Reference number": "FT-A"}
    o.update(doi)
    return o


def _ghi(conn, nguon, dong, **kw):
    kw.setdefault("spreadsheet_id", "SID-TEST")
    kw.setdefault("lan", "Bank")
    kw.setdefault("actor", "test")
    return ch.ghi_chup(conn, nguon=nguon, dong=dong, **kw)


# ── cổng của task `9b` ────────────────────────────────────────────────────
def test_CONG_chup_hai_lan_ra_HAI_anh_va_anh_cu_KHONG_doi_MOT_O(conn):
    """⛔⛔ Luật **CHỈ-THÊM**, và nó được đo bằng **ảnh chụp của ảnh chụp**.

    ⛔ Đo bằng *"số dòng có tăng ⛔ không"* thì một phép ghi-đè vẫn qua được:
      xoá 2 thêm 2 là **±0**. ⇒ Chụp lại toàn bộ nội dung ảnh cũ **trước**,
      rồi đòi nó **y nguyên từng ô** sau khi chụp lần hai.
    """
    s = _nguon(conn)
    a = _ghi(conn, {s: 1}, [(s, 0, _o()), (s, 1, _o(Reference_number="x")
                             if False else _o(**{"Reference number": "FT-B"}))])
    truoc = (a.doc_luc, a.spreadsheet_id, a.lan, a.giay, a.actor,
             ch.doc_dong(conn, a.chup_id))

    b = _ghi(conn, {s: 2}, [(s, 0, _o(Debit=9999))])

    assert b.chup_id != a.chup_id, "⛔ chụp lại phải ra `chup_id` MỚI"

    lai = ch.doc_chup(conn, a.chup_id)
    sau = (lai.doc_luc, lai.spreadsheet_id, lai.lan, lai.giay, lai.actor,
           ch.doc_dong(conn, a.chup_id))
    assert sau == truoc, "⛔ ảnh chụp CŨ đã bị đổi — luật chỉ-THÊM vỡ"
    # ⭐ Và bản khai đã dùng của hai ảnh KHÁC nhau ⇒ lineage đọc được.
    assert [n.khai_version for n in lai.nguon] == [1]
    assert [n.khai_version for n in ch.doc_chup(conn, b.chup_id).nguon] == [2]


# ── cái bẫy đã cắn HAI lần ────────────────────────────────────────────────
def test_KIEU_O_giu_duoc_se_ri_ngay_va_ma_16_SO_khong_thanh_chuoi(conn):
    """⛔⛔ **Lần thứ BA cùng cái bẫy — nên nó có một bài riêng.**

    ⓐ Sê-ri ngày `45586` phải về là **`int`**, ⛔ không phải `"45586"`.
    ⓑ Mã kiểu số **16 chữ số** phải về **nguyên vẹn**, ⛔ không thành
       `1.23e+15` — đo 07/09: **45%** mã của sổ thật lưu kiểu **SỐ**, và mọi
       đường đi qua bản hiển thị đều làm hỏng chúng *(`QĐ-ITL-93`)*.
    ⓒ Số thập phân giữ **`float`**, ⛔ không bị làm tròn.
    """
    s = _nguon(conn)
    ma = 1234567890123456
    a = _ghi(conn, {s: 1}, [(s, 0, _o(**{"Date": 45586,
                                         "Reference number": ma,
                                         "Credit": 66923.25}))])
    (_s, _d, o), = ch.doc_dong(conn, a.chup_id)

    assert o["Date"] == 45586 and isinstance(o["Date"], int), (
        "⛔ sê-ri ngày ⛔ không còn là số — đúng cái bẫy `QĐ-ITL-102` ⓶")
    assert o["Reference number"] == ma, (
        "⛔ mã 16 số bị đổi: %r ⇒ ảnh chụp ⛔ không truy được về sao kê"
        % (o["Reference number"],))
    assert isinstance(o["Reference number"], int)
    assert o["Credit"] == 66923.25 and isinstance(o["Credit"], float)


# ── điểm mù `S8`: nguồn ra 0 dòng ────────────────────────────────────────
def test_nguon_doc_ra_0_DONG_van_CO_MAT_trong_anh_chup(conn):
    """⭐⭐ Toàn bộ lý do `fls_chup_nguon` tồn tại.

    Suy tập nguồn từ **dữ liệu** thì một sheet ra `0` dòng **biến mất khỏi
    chính phép kiểm sinh ra để tìm nó** — `S8` đã tự lộ đúng điểm mù ấy.
    """
    a, b = _nguon(conn), _nguon(conn)
    kq = _ghi(conn, {a: 1, b: 1}, [(a, 0, _o())])

    theo = {n.source_id: n.so_dong for n in kq.nguon}
    assert theo == {a: 1, b: 0}, (
        "⛔ nguồn đọc ra 0 dòng ⛔ KHÔNG có mặt ⇒ ⛔ không ai phân biệt được "
        "*sheet rỗng thật* với *sheet ⛔ chưa đọc*")
    assert kq.so_nguon == 2 and kq.so_dong == 1


# ── ⛔ ba thứ phải NỔ ────────────────────────────────────────────────────
def test_anh_chup_KHONG_doc_nguon_nao_thi_NO(conn):
    """⛔ *Đo được 0 thứ ⇒ ⛔ KHÔNG ĐẠT* — ở đây nó là một phép chặn lúc GHI.

    Một ảnh chụp rỗng vẫn có `doc_luc` thật, và `F04` sẽ hiện nó ra như
    *"đã đọc lúc 15:02"*. Đó là một **dấu thời điểm nói dối**.
    """
    with pytest.raises(ch.LoiChup, match="⛔ không đọc nguồn nào"):
        _ghi(conn, {}, [])


def test_dong_thuoc_nguon_KHONG_khai_da_doc_thi_NO(conn):
    a, b = _nguon(conn), _nguon(conn)
    with pytest.raises(ch.LoiChup, match="HAI câu chuyện"):
        _ghi(conn, {a: 1}, [(a, 0, _o()), (b, 0, _o())])


def test_o_mang_Description_thi_VAO_KHO_NGUYEN_VEN(conn):
    """⭐⭐⭐ `QĐ-ITL-128` *(17/09)* — owner **mở lại `QĐ-ITL-92`**.

    ⛔⛔ **Bài này TỪNG ghim điều NGƯỢC LẠI** *(ô mang `Description` ⇒ NỔ)*, và
    nó ⛔ **không bị xoá** — nó bị **đảo chiều**, vì **nỗi lo gốc vẫn y nguyên**:
    *một giá trị bị ném lặng lẽ thì ⛔ không ai biết*. Trước kia nỗi lo ấy bảo
    *"đừng để nó VÀO"*; nay nó bảo *"đừng để nó RƠI"*.

    ⛔ Căn cứ owner cân nhắc, đo trên 58/60 sheet `R |` *(7.712 ô có chữ)*:
       tên NGƯỜI **4,8%** *(sàn dưới)* · mã ghép `PI…/PE…` **23,0%**.
    """
    s = _nguon(conn)
    kq = _ghi(conn, {s: 1}, [(s, 0, dict(_o(), Description="NGUYEN VAN A"))])
    o = conn.execute("SELECT o FROM fls_chup_dong WHERE chup_id=%s",
                     (kq.chup_id,)).fetchone()[0]
    assert o.get("Description") == "NGUYEN VAN A", (
        "⛔ `Description` bị RƠI trên đường vào kho — và rơi lặng lẽ thì "
        "⛔ không ai biết (đúng nỗi lo cũ, chiều ngược lại)")


def test_khoi_NHAN_SU_VAN_bi_chan_du_Description_da_duoc_mo(conn):
    """⛔⛔ `QĐ-ITL-128` mở **đúng một** trường. `QĐ-ITL-107` là quyết định
    **KHÁC** và ⛔ **không** bị mở theo — bài này chặn đúng cái suy luận
    *"đã nới một chỗ thì nới cả lô"*."""
    s = _nguon(conn, "Cash")
    with pytest.raises(ch.LoiChup, match="DỮ LIỆU CÁ NHÂN"):
        _ghi(conn, {s: 1},
             [(s, 0, dict(_o(), Description="ok",
                          **{"Họ và tên (*)": "NGUYEN VAN A"}))])


def test_o_mang_truong_HO_VA_TEN_thi_NO(conn):
    """⛔ Khối nhân sự `9`…`14` của lằn quỹ *(`QĐ-ITL-107`)* — cấm cả khối."""
    s = _nguon(conn, "Cash")
    with pytest.raises(ch.LoiChup, match="DỮ LIỆU CÁ NHÂN"):
        _ghi(conn, {s: 1},
             [(s, 0, dict(_o(), **{"Số CMND/CCCD/Passport (*)": "001"}))],
             lan="Cash")


def test_lan_LA_thi_NO(conn):
    s = _nguon(conn)
    with pytest.raises(ch.LoiChup, match="`lan="):
        _ghi(conn, {s: 1}, [(s, 0, _o())], lan="Quy")


def test_thieu_actor_thi_NO(conn):
    s = _nguon(conn)
    with pytest.raises(ch.LoiChup, match="actor"):
        _ghi(conn, {s: 1}, [(s, 0, _o())], actor="")


def test_nguon_LA_thi_NO_va_KHONG_de_lai_anh_nua_vo(conn):
    """⭐ Phép kiểm trước cửa và **giao dịch** là hai thứ khác nhau.

    Nguồn ⛔ không có ⇒ NỔ; và ⛔ **không được để lại** một dòng `fls_chup`
    mồ côi *(một đầu ảnh chụp ⛔ không có nguồn nào)* — nó sẽ hiện trên `F04`.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_chup")
        truoc = cur.fetchone()[0]
    with pytest.raises(ch.LoiChup, match="⛔ không có nguồn"):
        _ghi(conn, {2 ** 40: 1}, [])
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_chup")
        assert cur.fetchone()[0] == truoc, "⛔ để lại một đầu ảnh chụp mồ côi"


def test_doc_anh_chup_KHONG_co_thi_NO_chu_KHONG_tra_vo_rong(conn):
    """⛔ *"⛔ không có ảnh `7`"* ≠ *"ảnh `7` đọc được 0 dòng"*.

    Hai câu dẫn người dùng đi **hai đường sửa khác nhau**; trả `None`/`[]` cho
    cả hai là gộp chúng lại — cùng lý do `FLS-NGUON-LA` **404** và
    `FLS-KHAI-KHONG-CO` **409** phải là hai mã *(`BA-07` §4b ⓺)*.
    """
    with pytest.raises(ch.KhongCoChup):
        ch.doc_chup(conn, 2 ** 40)
    with pytest.raises(ch.KhongCoChup):
        ch.doc_dong(conn, 2 ** 40)


# ── nối vào phép `chuyen()` đang chạy ────────────────────────────────────
def test_anh_chup_doc_lai_duoc_qua_CHINH_phep_chuyen_dang_chay(conn):
    """⭐⭐ Ảnh chụp phải đi vào **đúng** `chuyen()` mà chặng 1 đã chứng minh.

    ⛔ Nếu lằn ảnh chụp có một phép chuyển **riêng** thì `8.338/8.338` của
      chặng 1 ⛔ **không còn nói gì** về đường mà `F04` thật sự đi.
    """
    s = _nguon(conn)
    a = _ghi(conn, {s: 1}, [
        (s, 0, _o(**{"Reference number": "FT-1"})),
        (s, 1, _o(**{"Reference number": "FT-1"})),      # cùng mã ⇒ `Num` 1,2
        (s, 2, _o(**{"Date": "", "Reference number": "FT-9"})),   # rỗng
    ])
    hang = [hang_tu_o(o) for _s, _d, o in ch.doc_dong(conn, a.chup_id)]
    ra, tk = chuyen("R | X", KHAI_ANH_CHUP, hang)

    assert (tk.vao, tk.ra, tk.rong, tk.loi) == (3, 2, 1, 0)
    from fls.adapters.sao_ke import I_MOTA, I_NUM
    assert [r[I_NUM] for r in ra] == [1, 2], "⛔ luật `Num` của AS-IS bị đổi"
    # ⛔ `Description` ra RỖNG — 5/6 trường, `QĐ-ITL-92`.
    assert {r[I_MOTA] for r in ra} == {""}


def test_thu_tu_doc_lai_DUNG_thu_tu_da_doc(conn):
    """⛔ Luật `Num` = **thứ tự lần xuất hiện** *(đo 8.331/8.331 = 100,0%)*.

    ⇒ Đọc lại theo thứ tự khác là **đổi `Num`**, tức làm sai một cột mà FLS
      đã chứng minh là dựng đúng. Bài này ghim thứ tự `(source_id, dong_so)`.
    """
    s = _nguon(conn)
    a = _ghi(conn, {s: 1}, [(s, i, _o(**{"Reference number": "FT-%d" % i}))
                            for i in (2, 0, 1)])
    assert [d for _s, d, _o in ch.doc_dong(conn, a.chup_id)] == [0, 1, 2]


def test_gioi_han_va_moi_nhat(conn):
    s = _nguon(conn)
    a = _ghi(conn, {s: 1}, [(s, i, _o()) for i in range(5)])
    assert len(ch.doc_dong(conn, a.chup_id, gioi_han=2)) == 2
    assert ch.moi_nhat(conn, "Bank").chup_id == a.chup_id
    assert a.chup_id in [x.chup_id for x in ch.liet_ke(conn, lan="Bank")]
