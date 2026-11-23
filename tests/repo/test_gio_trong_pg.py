# -*- coding: utf-8 -*-
"""`A1` vế THẬT — `do_gio_trong`: đếm GIỜ TRỐNG trong khung chụp.

⛔⛔⛔ **Vì sao phép đo này phải tồn tại.** Sáng `10/09` bộ hẹn giờ **bỏ `3`
   lượt** *(máy ngủ)* và ⛔ **không một cổng nào kêu**. Cổng `A1` đếm *"có ≥2
   ảnh, ≥2 giờ khác nhau"* — và điều đó **vẫn đúng** khi nhịp đã chết ba
   tiếng, vì các ảnh **cũ** vẫn nằm đó. ⇒ `A1` đo *"nhịp TỪNG chạy"*, ⛔ không
   phải *"nhịp ĐANG chạy"*.

⭐⭐ **Cách li bằng lằn `Cash` + dọn HAI ĐẦU.** Kho test là **kho dùng
   chung**, và tôi đã một lần làm **19 bài khác đổ** bằng cách để lại trạng
   thái trong nó. `do_gio_trong` đếm *"từ ảnh nhịp đầu tiên của lằn tới giờ
   trước"* ⇒ **một** ảnh sót của bài khác trong cùng lằn đổi kết quả.

⛔⛔ Ban đầu tôi định dùng một `lan` **ngẫu nhiên** cho cách li tuyệt đối, và
   **cửa kho CHẶN đúng**: `ch.LAN` chỉ nhận `Bank`/`Cash`/`PM`. ⇒ Dùng `Cash`
   *(lằn quỹ — `0` ảnh ở cả hai kho)* và dọn **cả hai đầu**. ⛔ Một cái chặn
   đúng thì ⛔ **không đi đường vòng** bằng `INSERT` tay: làm thế là bỏ luôn
   phép soi `Description`/CMND của chính cửa ấy.

⛔ Cái chúng chặn:
  · đếm từ ảnh đầu tiên **của lằn** thay vì ảnh đầu tiên **của nhịp** ⇒ kêu
    oan những giờ ⛔ chưa ai hứa *(bản đầu của tôi báo `17`, đúng là `3`)*
  · tính **giờ đang diễn ra** là trống ⇒ kêu oan **mỗi giờ một lần**
  · đếm ảnh rồi **TRỪ** thay vì `LEFT JOIN` ⇒ một giờ có hai ảnh **che** một
    giờ trống, và hiệu **nói nhỏ hơn sự thật** *(đúng lỗi `353` đã cắn)*
"""
from __future__ import annotations

import uuid
import zoneinfo
from datetime import datetime, timedelta

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import chup as ch
from fls.repo.nhip_chup import (ACTOR_NHIP, ACTOR_TAY, GIO_CUOI, GIO_DAU,
                                MUI, do_gio_trong)

pytestmark = pytest.mark.pg

VN = zoneinfo.ZoneInfo(MUI)


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


# ⭐ Lằn **`Cash`** — lằn quỹ, và nó `0` ảnh ở **cả** kho thật lẫn kho test
#   *(`§1`: *"quỹ chưa mở"*)*. ⇒ Nó là lằn **duy nhất** cách li được.
#
# ⛔⛔ Ban đầu tôi định dùng một `lan` ngẫu nhiên cho cách li tuyệt đối — và
#    **cửa kho CHẶN đúng**: `ch.LAN` chỉ nhận `Bank`/`Cash`/`PM`, vì *"hai
#    lằn khác khuôn RA (`GAP-CANON-02`) nên ⛔ không được lẫn vào nhau"*. Một
#    cái chặn đúng thì ⛔ **không đi đường vòng qua nó** bằng `INSERT` tay —
#    làm thế là bỏ luôn phép soi `Description`/CMND của chính cửa ấy.
LAN_THU = "Cash"


@pytest.fixture()
def lan(conn) -> str:
    """Lằn `Cash` **sạch** trước và sau mỗi bài.

    ⚠⚠ Kho test là kho **dùng chung**, và tôi đã một lần làm **19 bài khác
      đổ** bằng cách để lại trạng thái trong nó. `do_gio_trong` đếm *"từ ảnh
      nhịp đầu tiên của lằn"* ⇒ **một** ảnh sót lại của bài trước đổi kết quả
      của mọi bài sau. ⇒ Dọn **cả hai đầu**, ⛔ không chỉ đầu ra.
    """
    def _don():
        conn.execute(
            "DELETE FROM fls_chup_dong WHERE chup_id IN"
            " (SELECT chup_id FROM fls_chup WHERE lan = %s)", (LAN_THU,))
        conn.execute(
            "DELETE FROM fls_chup_nguon WHERE chup_id IN"
            " (SELECT chup_id FROM fls_chup WHERE lan = %s)", (LAN_THU,))
        conn.execute("DELETE FROM fls_chup WHERE lan = %s", (LAN_THU,))

    _don()
    try:
        yield LAN_THU
    finally:
        _don()


@pytest.fixture()
def nguon(conn):
    k = "GIOTRONG-" + uuid.uuid4().hex[:8].upper()
    r = conn.execute(
        "INSERT INTO fls_source (source_key, src_type) VALUES (%s, 'Cash')"
        " RETURNING source_id", (k,)).fetchone()
    return int(r[0])


def _anh(conn, lan: str, nguon: int, luc: datetime,
         actor: str = ACTOR_NHIP) -> int:
    """Một ảnh của lằn `lan` **đúng vào giờ** `luc`.

    ⛔ `ghi_chup` NỔ nếu `nguon` rỗng, nên phải đưa nguồn thật vào; `doc_luc`
      thì ⛔ không nhận được từ ngoài *(sổ chỉ-thêm ghi *"bây giờ"*)* ⇒ đặt
      lại bằng một cú `UPDATE`, đúng khuôn các bài `nhip_chup` sẵn có.
    """
    a = ch.ghi_chup(conn, spreadsheet_id="SID-" + lan, lan=lan, actor=actor,
                    nguon={nguon: 1}, dong=[])
    conn.execute("UPDATE fls_chup SET doc_luc = %s WHERE chup_id = %s",
                 (luc, a.chup_id))
    return int(a.chup_id)


# ⭐ Một mốc CỐ ĐỊNH trong khung, đủ xa quá khứ để ⛔ không phụ thuộc *"hôm
#   nay là ngày nào"*. `10:00` giờ VN — nằm giữa `GIO_DAU` và `GIO_CUOI`.
T0 = datetime(2026, 6, 1, 10, 0, tzinfo=VN)


def test_LANG_CHUA_CO_ANH_NHIP_thi_KHONG_KEU_OAN(conn, lan, nguon):
    """⛔⛔ Lằn ⛔ chưa có ảnh nhịp nào ⇒ **`0`** giờ trống, ⛔ không phải vô số.

    ⛔ Nếu mốc bắt đầu là `1970` thì con số sẽ là **hàng trăm nghìn**, và một
      cổng như thế bị tắt trong một ngày.
    """
    d = do_gio_trong(conn, lan, T0 + timedelta(hours=5))
    assert d["gio_trong"] == 0
    assert d["gio_phai_co"] == 0
    assert d["anh_dau_tien"] is None


def test_chi_dem_tu_ANH_DAU_TIEN_CUA_NHIP_khong_cua_LAN(conn, lan, nguon):
    """⛔⛔⛔ **Đây là lỗi bản đầu của tôi.**

    Lằn `Bank` có ảnh từ `08/09 15:00` do `tools/chup_sao_ke.py` **gõ tay**,
    còn nhịp chỉ được đăng ký chiều `09/09`. Đếm từ ảnh đầu **của lằn** ra
    **`17`** giờ trống; đúng là **`3`**. Những giờ trước khi nhịp tồn tại là
    những giờ **⛔ chưa ai hứa** sẽ có ảnh.
    """
    # ⓐ ba giờ gõ tay TRƯỚC khi nhịp tồn tại
    for h in (0, 1, 2):
        _anh(conn, lan, nguon, T0 + timedelta(hours=h), actor=ACTOR_TAY)
    # ⓑ nhịp bắt đầu ở `+3`, rồi TRỐNG `+4`, `+5`
    _anh(conn, lan, nguon, T0 + timedelta(hours=3))

    d = do_gio_trong(conn, lan, T0 + timedelta(hours=6))
    assert d["gio_phai_co"] == 3, d          # +3 · +4 · +5
    assert d["gio_co_anh"] == 1, d           # chỉ +3
    assert d["gio_trong"] == 2, d            # +4 · +5


def test_GIO_DANG_DIEN_RA_khong_tinh_la_TRONG(conn, lan, nguon):
    """⚠ Nhịp có thể **chưa tới lượt** trong giờ này ⇒ tính nó là trống là
    **kêu oan mỗi giờ một lần**."""
    _anh(conn, lan, nguon, T0)
    # Bây giờ là `T0 + 1h`, và giờ ấy ⛔ chưa có ảnh — nhưng nó **đang diễn ra**
    d = do_gio_trong(conn, lan, T0 + timedelta(hours=1, minutes=5))
    assert d["gio_trong"] == 0, d
    assert d["gio_phai_co"] == 1, d


def test_MOT_GIO_HAI_ANH_khong_CHE_mot_gio_trong(conn, lan, nguon):
    """⛔⛔⛔ Đếm ảnh rồi **TRỪ** là phép sai, và nó sai theo chiều **nói nhỏ
    hơn sự thật** — đúng lỗi `353`.

    Ở đây: `3` giờ phải có · `4` ảnh · `1` giờ trống. Phép *"số giờ − số
    ảnh"* sẽ ra **−1** rồi bị kẹp thành `0` ⇒ **che** giờ trống.
    """
    _anh(conn, lan, nguon, T0)
    _anh(conn, lan, nguon, T0 + timedelta(minutes=30))       # ⭐ cùng giờ T0
    _anh(conn, lan, nguon, T0 + timedelta(hours=1))
    # `T0+2h` TRỐNG
    d = do_gio_trong(conn, lan, T0 + timedelta(hours=3))
    assert d["gio_phai_co"] == 3, d
    assert d["gio_co_anh"] == 2, d
    assert d["gio_trong"] == 1, d


def test_GIO_NGOAI_KHUNG_khong_tinh_la_TRONG(conn, lan, nguon):
    """Đêm ⛔ không phải giờ trống — `QĐ-ITL-114` khai khung `8h`–`19h`."""
    _anh(conn, lan, nguon, T0)
    # `T0` là `10:00`; nhảy tới `10:00` **hôm sau** ⇒ đi qua cả một đêm.
    d = do_gio_trong(conn, lan, T0 + timedelta(days=1))
    # Trong khung của ngày đầu: `11h`…`19h` = 9 giờ; ngày sau `8h`·`9h` = 2
    # ⇒ 11 giờ trống. ⛔ Đêm (`20h`–`07h`) ⛔ không có mặt.
    assert d["gio_trong"] == 11, d
    assert d["gio_phai_co"] == 12, d         # + chính giờ `T0`


def test_GOI_TEN_gio_trong_chu_khong_chi_DEM(conn, lan, nguon):
    """⭐ Một con số đếm nói *"có chuyện"*; một danh sách nói *"đi xem cái
    này"*. Báo cáo nhịp in `nguon_ra_0_dong: 14` — và ⛔ không ai hành động
    được trên con số ấy."""
    _anh(conn, lan, nguon, T0)
    d = do_gio_trong(conn, lan, T0 + timedelta(hours=3))
    assert d["gio_trong"] == 2
    assert len(d["trong_gan_nhat"]) == 2
    # ⭐ Gần nhất TRƯỚC, để người đọc thấy ngay giờ vừa hụt.
    assert d["trong_gan_nhat"][0].endswith("12:00")
    assert d["trong_gan_nhat"][1].endswith("11:00")


def test_danh_sach_bi_CAT_thi_so_dem_van_DUNG(conn, lan, nguon):
    """⚠ Danh sách cắt ở `12`; ⛔ con số đếm **⛔ không** được cắt theo.

    ⛔ Trả một danh sách `12` phần tử rồi để người đọc `len()` nó là cách
      biến `40` giờ trống thành `12` — và ⛔ không gì báo.
    """
    _anh(conn, lan, nguon, T0)
    d = do_gio_trong(conn, lan, T0 + timedelta(days=2))
    assert d["gio_trong"] > 12, d
    assert len(d["trong_gan_nhat"]) == 12, d


def test_KHUNG_lay_tu_HANG_SO_khong_go_tay():
    """⛔ `8`/`19` ⛔ không được gõ lại trong bài — `QĐ-ITL-114` khai **một**
    chỗ, và một bản sao trong bài thử là một nguồn sự thật thứ hai."""
    assert (GIO_DAU, GIO_CUOI) == (8, 19)


# ── `cua_so` — dieu kien de con so nay dung duoc lam CONG ────────────────
def test_KHONG_CUA_SO_thi_cong_KHONG_HOI_PHUC_duoc(conn, lan, nguon):
    """⛔⛔⛔ **Day la ly do `cua_so` phai ton tai.**

    Khong cua so, phep dem phu *"tu anh nhip dau tien toi nay"* ⇒ mot gio
    trong cua hom nay **o lai MAI MAI**. Cong do mot lan roi ⛔ khong bao gio
    xanh lai duoc, ke ca sau khi loi da chua. **Mot cong ⛔ khong hoi phuc
    duoc la mot cong se bi TAT.**
    """
    _anh(conn, lan, nguon, T0)
    # `T0+1h` TRONG — mot lan hong
    _anh(conn, lan, nguon, T0 + timedelta(hours=2))
    _anh(conn, lan, nguon, T0 + timedelta(hours=3))
    _anh(conn, lan, nguon, T0 + timedelta(hours=4))

    # ⛔ Toan phan: gio trong ay **con nguyen** du nhip da chay dung 3 gio lien
    assert do_gio_trong(conn, lan, T0 + timedelta(hours=5))["gio_trong"] == 1
    # ⭐ Cua so 3 gio khung gan nhat (`+2`·`+3`·`+4`): SACH ⇒ cong xanh lai
    d = do_gio_trong(conn, lan, T0 + timedelta(hours=5), cua_so=3)
    assert d["gio_phai_co"] == 3, d
    assert d["gio_trong"] == 0, d
    assert d["cua_so"] == 3


def test_CUA_SO_dem_theo_gio_KHUNG_khong_theo_gio_DONG_HO(conn, lan, nguon):
    """⛔⛔ Dem theo gio dong ho thi mot cua so `12` roi vao **ban dem** se phu
    `0` gio khung, va cong se **XANH tren tap RONG**.

    O day: nhip chay `T0` roi chet; do vao `10:00` **hom sau**. Cua so `3`
    phai lay `3` gio KHUNG gan nhat *(`19h` hom truoc · `8h`·`9h` hom sau)* —
    ca ba deu TRONG.
    """
    _anh(conn, lan, nguon, T0)
    d = do_gio_trong(conn, lan, T0 + timedelta(days=1), cua_so=3)
    assert d["gio_phai_co"] == 3, d
    assert d["gio_trong"] == 3, d


def test_CUA_SO_lon_hon_lich_su_thi_bang_TOAN_PHAN(conn, lan, nguon):
    _anh(conn, lan, nguon, T0)
    a = do_gio_trong(conn, lan, T0 + timedelta(hours=3))
    b = do_gio_trong(conn, lan, T0 + timedelta(hours=3), cua_so=999)
    assert a["gio_phai_co"] == b["gio_phai_co"] == 3
    assert a["gio_trong"] == b["gio_trong"] == 2


def test_CUA_SO_khong_lam_LANG_RONG_keu_oan(conn, lan, nguon):
    d = do_gio_trong(conn, lan, T0, cua_so=12)
    assert d["gio_trong"] == 0 and d["anh_dau_tien"] is None
