"""`A1` — NHỊP CHỤP. `QĐ-ITL-114`: mỗi giờ, `8h`–`19h`, mọi ngày.

⛔⛔ **Hai lỗi mà bộ bài này canh, và cả hai đều làm SỐ LƯỢNG ảnh VẪN KHỚP —
   nên ⛔ không cổng đếm nào thấy chúng:**

  ⓐ **Sai MÚI GIỜ.** Một bộ hẹn giờ chạy `UTC` mà đọc `8`–`19` theo `UTC` sẽ
    chụp từ `15h` đến `02h` giờ VN: **12 ảnh/ngày, đúng số lần, sai mọi giờ**.
  ⓑ **Bắn HAI LẦN một giờ** *(máy khởi động lại, một lượt chạy tay chồng lên)*.
    Hai ảnh một giờ ⛔ không sai dữ liệu, nhưng nó làm phép dọn và mọi con số
    *"ảnh/năm"* nói dối — mà chính con số ấy là căn cứ của `QĐ-ITL-115`.
"""
from __future__ import annotations

import uuid
import zoneinfo
from datetime import datetime, timedelta, timezone

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import chup as ch
from fls.repo.nhip_chup import (ACTOR_NHIP, ACTOR_TAY, GIO_CUOI,
                                GIO_DAU, MUI, can_chup,
                                da_chup_gio_nay, gio_viet_nam,
                                trong_gio_lam_viec)

pytestmark = pytest.mark.pg

VN = zoneinfo.ZoneInfo(MUI)


def _hex(n: int = 8) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


# ── ⓐ MÚI GIỜ ───────────────────────────────────────────────────────────
def test_luc_KHONG_mang_mui_gio_thi_NO():
    """⛔⛔ Đoán hộ *"chắc là giờ địa phương"* là **đúng** cách `8h–19h` thành
    `15h–02h` mà ⛔ không cổng nào thấy: số lượng ảnh vẫn khớp."""
    with pytest.raises(ValueError) as e:
        gio_viet_nam(datetime(2026, 9, 9, 10, 0))
    assert "múi giờ" in str(e.value)


@pytest.mark.parametrize("gio_utc,mong", [
    # ⭐ `01:00 UTC` = `08:00` VN ⇒ giờ ĐẦU, có chụp
    (1, True),
    # ⛔ `00:59 UTC` = `07:59` VN ⇒ chưa tới giờ
    (0, False),
    # ⭐ `12:00 UTC` = `19:00` VN ⇒ giờ CUỐI, **vẫn** chụp
    (12, True),
    # ⛔ `13:00 UTC` = `20:00` VN ⇒ hết giờ
    (13, False),
    # ⛔⛔ `08:00 UTC` = `15:00` VN — chụp được. Nhưng nếu ai đọc `8`–`19` theo
    #    `UTC` thì `20:00 UTC` (= `03:00` VN) cũng sẽ *"trong giờ"*: bài dưới.
    (8, True),
    (20, False),
])
def test_gio_lam_viec_doc_theo_gio_VIET_NAM(gio_utc, mong):
    luc = datetime(2026, 9, 9, gio_utc, 0, tzinfo=timezone.utc)
    assert trong_gio_lam_viec(luc) is mong, (
        f"{gio_utc}h UTC = {gio_viet_nam(luc).hour}h VN — "
        f"cửa sổ là {GIO_DAU}h–{GIO_CUOI}h giờ VN")


def test_MOI_NGAY_ke_ca_CUOI_TUAN():
    """⚠ Kể cả cuối tuần là **cố ý**: sao kê bank về vào cuối tuần, và một ảnh
    già `48 giờ` sáng thứ Hai là đúng thứ nhịp này sinh ra để tránh."""
    # 12/09/2026 là **thứ Bảy**, 13/09 là **Chủ nhật**
    for ngay in (12, 13):
        luc = datetime(2026, 9, ngay, 10, 0, tzinfo=VN)
        assert luc.weekday() >= 5
        assert trong_gio_lam_viec(luc) is True


# ── ⓑ BẮN HAI LẦN một giờ ───────────────────────────────────────────────
def test_da_co_anh_trong_GIO_NAY_thi_BO_LUOT(conn):
    tt = _hex()
    nguon = conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s,'PM') RETURNING source_id", ("PM nhip " + tt,)
    ).fetchone()[0]
    luc = datetime(2026, 9, 9, 10, 5, tzinfo=VN)

    # ⛔ Chưa có ảnh nào ⇒ CHỤP. ⚠ Kho test dùng chung, nên đo trên một lằn
    #   ⛔ chưa ai chụp trong đúng giờ ấy — lùi `doc_luc` bằng tay ở dưới.
    conn.execute("DELETE FROM fls_chup_nguon WHERE chup_id IN"
                 " (SELECT chup_id FROM fls_chup WHERE lan='PM')")
    conn.execute("DELETE FROM fls_chup WHERE lan='PM' AND chup_id NOT IN"
                 " (SELECT chup_id FROM fls_run WHERE chup_id IS NOT NULL)")
    co, ly_do = can_chup(conn, "PM", luc)
    assert co is True and "CHỤP" in ly_do

    a = ch.ghi_chup_pm(conn, spreadsheet_id="SID-" + tt, actor=ACTOR_NHIP,
                       source_id=nguon, khai_version=1)
    conn.execute("UPDATE fls_chup SET doc_luc = %s WHERE chup_id = %s",
                 (luc, a.chup_id))

    assert da_chup_gio_nay(conn, "PM", luc) is True
    co, ly_do = can_chup(conn, "PM", luc)
    assert co is False and "đã có ảnh trong giờ này" in ly_do
    # ⭐ Nhưng **giờ sau** thì lại chụp — nó là một giờ KHÁC
    co, _ = can_chup(conn, "PM", luc + timedelta(hours=1))
    assert co is True


def test_so_theo_GIO_DONG_HO_chu_khong_theo_60_PHUT(conn):
    """⭐⭐ `08:59` rồi `09:01` là **hai giờ khác nhau** ⇒ chụp **cả hai**.

    ⛔ Nếu so theo *"cách đây < 60 phút"* thì lượt `9h` **bị bỏ**, và ⛔ không
      ai thấy: số ảnh/ngày chỉ hụt đi một, trông y như một lượt cron trượt.
    """
    tt = _hex()
    nguon = conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s,'PM') RETURNING source_id", ("PM gio " + tt,)
    ).fetchone()[0]
    conn.execute("DELETE FROM fls_chup_nguon WHERE chup_id IN"
                 " (SELECT chup_id FROM fls_chup WHERE lan='PM')")
    conn.execute("DELETE FROM fls_chup WHERE lan='PM' AND chup_id NOT IN"
                 " (SELECT chup_id FROM fls_run WHERE chup_id IS NOT NULL)")
    a = ch.ghi_chup_pm(conn, spreadsheet_id="SID-" + tt, actor=ACTOR_NHIP,
                       source_id=nguon, khai_version=1)
    conn.execute("UPDATE fls_chup SET doc_luc = %s WHERE chup_id = %s",
                 (datetime(2026, 9, 9, 8, 59, tzinfo=VN), a.chup_id))

    co, _ = can_chup(conn, "PM", datetime(2026, 9, 9, 9, 1, tzinfo=VN))
    assert co is True, "⛔ lượt `9h` bị bỏ vì so theo 60 phút thay vì giờ đồng hồ"


# ── LÝ DO luôn có chữ ───────────────────────────────────────────────────
def test_LY_DO_luon_co_chu__ke_ca_khi_CO_chup(conn):
    """⛔ Một nhịp bỏ lượt trong im lặng sẽ được đọc thành *"cron chết"*, và
    người ta đi khởi động lại một thứ ⛔ không hỏng."""
    for luc in (datetime(2026, 9, 9, 3, 0, tzinfo=VN),      # ngoài giờ
                datetime(2026, 9, 9, 10, 0, tzinfo=VN)):    # trong giờ
        _co, ly_do = can_chup(conn, "Bank", luc)
        assert len(ly_do.strip()) > 20, ly_do
        assert "giờ VN" in ly_do


def test_actor_cua_NHIP_khong_phai_mot_TEP_trong_tools():
    """⭐⭐ Cổng ra của `A1` đòi đúng điều này.

    Hai ảnh hiện có trong kho mang `actor = 'tools/chup_sao_ke.py'` — tức *"một
    người đã gõ một lệnh"*. Một ảnh do **nhịp** sinh ra phải nói được điều đó,
    ⛔ không thì ⛔ không ai phân biệt *"hệ tự chạy"* với *"Dev còn phải gõ
    tay"* — và đúng chỗ ấy là blocker cứng của *"dùng được thật"*.
    """
    assert not ACTOR_NHIP.startswith("tools/")
    assert not ACTOR_NHIP.endswith(".py")
    assert "@" in ACTOR_NHIP


# ── ⭐⭐⭐ HAI ACTOR: bit mot lo cua CHINH cong `A1` ─────────────────────
def test_actor_GO_TAY_khac_actor_cua_BO_HEN_GIO():
    """⭐⭐⭐ **Bai nay sinh ra tu mot lo cua chinh cong `A1` toi viet.**

    Cong `A1` dat: *">=2 anh mang `actor` ⛔ khong phai `tools/…`, o >=2 gio
    dong ho khac nhau"*. Nhung `tools/nhip_chup.py --that` ghi
    `actor = nhip@fls` **du ai goi no** ⇒ toi co the **go tay hai lan** cach
    nhau mot gio va cong `A1` **XANH**, trong khi bo hen gio ⛔ **chua he
    duoc dang ky**.

    ⇒ Do la mot cong **TU BAM DUOC**, va no vo dung **dung vao luc no can
      dung**: cau hoi cua `A1` la *"he TU CHAY chua"*, ⛔ khong phai *"co hai
      anh chua"*.

    ⭐ Chua: chi cu goi tu **bo hen gio** *(co `--tu-bo-hen-gio`)* mang
      `ACTOR_NHIP`; mot luot go tay mang `ACTOR_TAY`. Cong dem **DUNG BANG**
      `ACTOR_NHIP`.
    """
    assert ACTOR_TAY != ACTOR_NHIP
    # ⛔ Va `ACTOR_TAY` phai NOI RA no la go tay — mot ten mo ho o day se
    #   duoc doc thanh mot lang khac cua nhip.
    assert "tay" in ACTOR_TAY.lower()
    # ⛔ `ACTOR_NHIP` ⛔ khong duoc la TIEN TO cua `ACTOR_TAY` theo cach lam
    #   mot phep so `LIKE 'nhip@fls%'` dem ca hai — cung hinh benh voi
    #   `delete from fls_chup` la tien to cua `fls_chup_dong` (`A2`).
    assert not ACTOR_TAY.startswith(ACTOR_NHIP + " ")


def test_cong_A1_dem_DUNG_BANG_actor_nhip__khong_dem_go_tay(conn):
    """⛔⛔ Phep dem cua cong PHAI la `actor = 'nhip@fls'` **dung bang**.

    Neu no la *"⛔ khong chua `tools/`"* thi `nhip@fls(tay)` **cung duoc
    dem** — va cai lo vua bit lai mo ra.
    """
    tt = _hex()
    nguon = conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s,'PM') RETURNING source_id", ("PM actor " + tt,)
    ).fetchone()[0]
    a = ch.ghi_chup_pm(conn, spreadsheet_id="SID-" + tt, actor=ACTOR_TAY,
                       source_id=nguon, khai_version=1)
    n = conn.execute("SELECT count(*) FROM fls_chup WHERE chup_id = %s"
                     " AND actor = %s", (a.chup_id, ACTOR_NHIP)).fetchone()[0]
    assert n == 0, (
        "⛔⛔ mot anh GO TAY dang duoc dem la anh cua NHIP — cong `A1` "
        "vua thanh mot cong TU BAM DUOC")
