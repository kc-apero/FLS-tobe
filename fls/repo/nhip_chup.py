"""`A1` — NHỊP CHỤP. `QĐ-ITL-114`: **mỗi giờ, `8h`–`19h`, mọi ngày**.

⛔⛔⛔ **Vì sao nhịp phải là MỘT HÀM CÓ TÊN, ⛔ không phải một dòng trong bộ
   hẹn giờ của hệ điều hành.**

Owner chốt nhịp, và tôi đã khuyên **ngược lại** *(*"cho kế toán một cái nút —
người bấm đúng là người biết mình vừa dán xong; máy ⛔ không biết điều đó"*)*.
Owner chọn cron, và nhịp mỗi giờ xoá gần hết cái bất lợi ấy. ⇒ Quyết định là
của owner, nhưng **hai câu hỏi** vẫn phải trả lời được **bằng máy**:

  ⓐ *"bây giờ có phải giờ chụp ⛔ không"* — và câu trả lời phải kể **múi giờ
    nào**. `8h–19h` là giờ **Việt Nam**; một bộ hẹn giờ chạy theo `UTC` sẽ
    chụp từ `15h` đến `2h sáng` — **đúng số lần**, **sai mọi giờ**, và
    ⛔ không gì báo.
  ⓑ *"giờ này đã chụp chưa"* — bộ hẹn giờ có thể bắn **hai lần** *(máy khởi
    động lại, một lần chạy tay chồng lên)*. Hai ảnh trong một giờ ⛔ không sai
    dữ liệu, nhưng nó làm phép dọn và mọi con số *"ảnh/năm"* nói dối.

★ Nên module này trả **quyết định + LÝ DO**, ⛔ không trả một `bool` trơ. Một
  nhịp bỏ lượt mà ⛔ không nói vì sao là một nhịp ⛔ không ai gỡ lỗi được — và
  nó sẽ được đọc thành *"cron chết"*.

⛔ **Và nó ⛔ KHÔNG tự chụp.** Phép chụp là phép **đọc Google Sheets**, sống ở
  `tools/`. Module này chỉ **quyết định**, nên nó là hàm thuần cộng **một** câu
  đọc — và cả hai đều kiểm được ⛔ không cần mạng.
"""
from __future__ import annotations

import zoneinfo
from datetime import datetime

from fls.repo.danh_muc_actor import ACTOR_NHIP as _NHIP
from fls.repo.danh_muc_actor import ACTOR_NHIP_TAY as _NHIP_TAY

# ⭐ `QĐ-ITL-114` — khai **một** chỗ. `19` là giờ **CUỐI CÒN CHỤP** *(nên `19h`
#   có chụp; `20h` thì ⛔ không)*, ⛔ không phải mốc chặn trên hở.
GIO_DAU, GIO_CUOI = 8, 19

# ⛔⛔ Múi giờ **VIỆT NAM**, khai tường minh. Một bộ hẹn giờ chạy `UTC` mà đọc
#    `8`–`19` theo `UTC` sẽ chụp `15h`–`02h` giờ VN: **đúng số lần, sai mọi
#    giờ**, và ⛔ không cổng nào thấy vì số lượng ảnh vẫn khớp.
MUI = "Asia/Ho_Chi_Minh"

# ⭐ `actor` của nhịp — ⛔ **KHÔNG** phải `tools/<tệp>.py`.
#
# ⛔⛔ Cổng ra của `A1` đòi đúng điều này: *"`actor` ⛔ không phải `tools/…`"*.
#    Hai ảnh hiện có trong kho mang `actor = 'tools/chup_sao_ke.py'` — tức
#    *"một người đã gõ một lệnh"*. Một ảnh do **nhịp** sinh ra phải nói được
#    điều đó, ⛔ không thì ⛔ không ai phân biệt được *"hệ tự chạy"* với *"Dev
#    còn phải gõ tay"* — và đúng chỗ ấy là blocker cứng của *"dùng được thật"*.
# ⭐ `WO-011 T1`: chuỗi sống ở SỔ ACTOR — ⛔ gõ lại ở đây.
ACTOR_NHIP = _NHIP

# ⛔⛔⛔ **VA MOT LO CUA CHINH CONG `A1`, bit truoc khi dang ky bo hen gio.**
#
# Cong `A1` dat: *">=2 anh mang `actor` ⛔ khong phai `tools/…`, o >=2 gio dong
# ho khac nhau"*. Nhung `tools/nhip_chup.py --that` ghi `actor = nhip@fls`
# **du ai goi no** — nen toi co the go tay hai lan cach nhau mot gio va cong
# `A1` **XANH**, trong khi bo hen gio ⛔ **chua he duoc dang ky**.
#
# ⇒ Do la mot cong **tu bam duoc**, va no vo dung dung vao luc no can dung:
#   cau hoi cua `A1` la *"he TU CHAY chua"*, ⛔ khong phai *"co hai anh chua"*.
#
# ⭐ Chua: **chi cu goi tu BO HEN GIO** duoc mang `ACTOR_NHIP`; mot luot go tay
#   mang `ACTOR_TAY`. Bo hen gio duoc dang ky **kem co** `--tu-bo-hen-gio`, va
#   cong dem **dung** `ACTOR_NHIP`. ⇒ ⛔ Khong the lam cong xanh bang tay nua.
ACTOR_TAY = _NHIP_TAY


def gio_viet_nam(luc: datetime | None = None) -> datetime:
    """`luc` → giờ **Việt Nam**. `None` = bây giờ.

    ⛔ `luc` ⛔ không mang múi giờ ⇒ **NỔ**. Đoán *"chắc là giờ địa phương"* là
      đúng cái sai làm `8h–19h` thành `15h–02h`.
    """
    if luc is None:
        return datetime.now(zoneinfo.ZoneInfo(MUI))
    if luc.tzinfo is None:
        raise ValueError(
            "⛔ `luc` ⛔ không mang múi giờ. Đoán hộ là cách `8h–19h` thành "
            "`15h–02h` mà ⛔ không cổng nào thấy — số lượng ảnh vẫn khớp")
    return luc.astimezone(zoneinfo.ZoneInfo(MUI))


def trong_gio_lam_viec(luc: datetime | None = None) -> bool:
    """`8h` ≤ giờ VN ≤ `19h`. **Mọi ngày** — kể cả cuối tuần *(`QĐ-ITL-114`)*.

    ⚠ Kể cả cuối tuần là **cố ý**: sao kê bank về vào cuối tuần, và một ảnh
      già `48 giờ` sáng thứ Hai là đúng thứ nhịp này sinh ra để tránh.
    """
    return GIO_DAU <= gio_viet_nam(luc).hour <= GIO_CUOI


def da_chup_gio_nay(conn, lan: str, luc: datetime | None = None) -> bool:
    """Lằn `lan` đã có ảnh nào trong **giờ đồng hồ hiện tại** *(giờ VN)* chưa.

    ⚠ So theo **giờ đồng hồ**, ⛔ không theo *"cách đây < 60 phút"*. Hai cách
      khác nhau ở một chỗ quan trọng: bộ hẹn giờ bắn ở `08:59` rồi `09:01` thì
      cách-60-phút sẽ **bỏ lượt `9h`**, còn giờ-đồng-hồ thì chụp cả hai —
      đúng, vì đó là **hai giờ khác nhau**.
    """
    g = gio_viet_nam(luc)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM fls_chup"
            " WHERE lan = %s"
            "   AND date_trunc('hour', doc_luc AT TIME ZONE %s)"
            "     = date_trunc('hour', %s::timestamptz AT TIME ZONE %s)",
            (lan, MUI, g, MUI))
        return int(cur.fetchone()[0]) > 0


def can_chup(conn, lan: str, luc: datetime | None = None
             ) -> tuple[bool, str]:
    """`(có chụp ⛔ không, LÝ DO)`. ⛔ Lý do **luôn** có chữ — cả khi `True`.

    ⛔⛔ Vì sao trả cả lý do: một nhịp bỏ lượt trong im lặng sẽ được đọc thành
       *"cron chết"*, và người ta sẽ đi khởi động lại một thứ ⛔ không hỏng.
       Còn một nhịp **chạy** mà ⛔ không nói vì sao thì ⛔ không ai đối chiếu
       được số ảnh/ngày với nhịp đã chốt.
    """
    g = gio_viet_nam(luc)
    dau = g.strftime("%d/%m %H:%M") + " (giờ VN)"
    if not trong_gio_lam_viec(g):
        return False, (
            f"{dau} ⛔ ngoài giờ chụp `{GIO_DAU}h`–`{GIO_CUOI}h` "
            f"(`QĐ-ITL-114`) ⇒ bỏ lượt. ⛔ Đây ⛔ KHÔNG phải lỗi")
    if da_chup_gio_nay(conn, lan, g):
        return False, (
            f"{dau} lằn `{lan}` **đã có ảnh trong giờ này** ⇒ bỏ lượt. "
            f"⛔ Hai ảnh một giờ ⛔ không sai dữ liệu, nhưng nó làm phép dọn "
            f"và mọi con số *ảnh/năm* nói dối")
    return True, f"{dau} lằn `{lan}` ⛔ chưa có ảnh trong giờ này ⇒ CHỤP"


def do_gio_trong(conn, lan: str, luc: datetime | None = None,
                 cua_so: int | None = None) -> dict:
    """⭐⭐⭐ `A1` vế THẬT — **bao nhiêu giờ trong khung chụp ⛔ KHÔNG có ảnh**.

    ⛔⛔⛔ **Vì sao phép đo này phải tồn tại.** Sáng `10/09` bộ hẹn giờ **bỏ
      `3` lượt** *(máy ngủ)* và ⛔ **không một cổng nào kêu**. Cổng `A1` đếm
      *"có ≥2 ảnh, ≥2 giờ khác nhau"* — và điều đó **vẫn đúng** khi nhịp đã
      chết ba tiếng, vì các ảnh **cũ** vẫn nằm đó. ⇒ `A1` đang đo *"nhịp TỪNG
      chạy"*, ⛔ không phải *"nhịp ĐANG chạy"*.

    ⚠ `tools/soi_nhip.py` **đọc được** con số ấy từ bộ hẹn giờ, nhưng nó
      **Windows-only** ⇒ ⛔ **không** vào được `kiem_so_song` *(một cổng đổ vì
      thiếu `schtasks` là một cổng **sẽ bị tắt**)*.

    ⭐⭐ **Nhưng câu hỏi đo được HOÀN TOÀN TỪ KHO:** khung là `GIO_DAU`–
      `GIO_CUOI` giờ VN, và mỗi giờ trong khung phải có **đúng một** ảnh mỗi
      lằn. ⇒ *"đếm giờ trong khung mà ⛔ không có ảnh"* là một câu `SQL`, và
      nó **chạy trên mọi máy**.

    ⛔⛔⛔ **Mốc BẮT ĐẦU là chỗ dễ làm cổng kêu OAN nhất — và bản đầu tiên
      của chính hàm này ĐÃ kêu oan.** Tôi đếm từ **ảnh đầu tiên của lằn**, và
      lằn `Bank` có ảnh từ `08/09 15:00` do `tools/chup_sao_ke.py` **gõ tay**
      — trong khi nhịp chỉ được **đăng ký** chiều `09/09`. ⇒ Máy báo **`17`**
      giờ trống, mà `14` trong số đó là những giờ **⛔ chưa ai hứa** sẽ có
      ảnh. Một cổng kêu oan `14`/`17` là một cổng **sẽ bị tắt trong một
      ngày**.

    ⇒ Mốc bắt đầu là **ảnh đầu tiên do NHỊP sinh** *(`actor = ACTOR_NHIP`)*,
      ⛔ không phải ảnh đầu tiên của lằn. Trước lúc nhịp tồn tại thì ⛔ **không
      có lời hứa nào** để mà thất hứa.

    ⚠ Và mốc **KẾT THÚC** loại **giờ đang diễn ra**: nhịp có thể chưa tới
      lượt trong giờ này, nên tính nó là trống là **kêu oan mỗi giờ một lần**.

    ⭐⭐⭐ **`cua_so` — và ⛔ KHÔNG có nó thì con số này ⛔ KHÔNG dùng được làm
      CỔNG.** Không cửa sổ, phép đếm phủ **từ ảnh nhịp đầu tiên tới nay**, nên
      một giờ trống của hôm nay **ở lại mãi mãi**: cổng đỏ một lần rồi ⛔ không
      bao giờ xanh lại được, kể cả sau khi lỗi đã chữa. **Một cổng ⛔ không hồi
      phục được là một cổng sẽ bị tắt.**

    ⇒ `cua_so = N` ⇒ chỉ đếm trong **`N` giờ KHUNG gần nhất** *(⛔ không phải
      `N` giờ đồng hồ — đêm ⛔ không nằm trong khung, nên `12` giờ khung là hơn
      một ngày)*. Cổng nên hỏi cửa sổ; **báo cáo** nên hỏi toàn phần.

    Trả: `gio_trong` · `gio_phai_co` · `gio_co_anh` · `trong_gan_nhat[]`
    *(tối đa `12` giờ trống gần nhất, để người đọc **đi xem** chứ ⛔ không chỉ
    biết là có)* · `anh_dau_tien` · `cua_so`.
    """
    g = gio_viet_nam(luc)
    with conn.cursor() as cur:
        # ⭐ `generate_series` dựng **mọi giờ** từ ảnh đầu tiên tới mốc kết
        #   thúc, rồi lọc theo khung; `LEFT JOIN` chỉ ra giờ ⛔ không có ảnh.
        #   ⛔ Đừng làm bằng cách đếm ảnh rồi trừ: một giờ có **hai** ảnh sẽ
        #   che một giờ trống, và hai lỗi ngược chiều thì hiệu **nói nhỏ hơn
        #   sự thật** — đúng lỗi `353` đã cắn.
        cur.execute(
            """
            WITH d AS (
              SELECT min(date_trunc('hour', doc_luc AT TIME ZONE %(mui)s))
                       AS dau
                FROM fls_chup
               WHERE lan = %(lan)s AND actor = %(nhip)s
            ), khung AS (
              SELECT generate_series(d.dau,
                       date_trunc('hour', %(nay)s::timestamptz
                                          AT TIME ZONE %(mui)s)
                         - interval '1 hour',
                       interval '1 hour') AS h
                FROM d WHERE d.dau IS NOT NULL
            ), trong_khung AS (
              SELECT h FROM khung
               WHERE extract(hour FROM h) BETWEEN %(dau)s AND %(cuoi)s
            ), can AS (
              -- ⭐ Cua so dem theo **gio KHUNG**, ⛔ khong theo gio dong ho:
              --   dem theo gio dong ho thi mot cua so `12` roi vao ban dem se
              --   phu `0` gio khung, va cong se XANH tren tap RONG.
              SELECT h FROM (
                SELECT h, row_number() OVER (ORDER BY h DESC) AS r
                  FROM trong_khung) z
               WHERE %(cua_so)s::int IS NULL OR z.r <= %(cua_so)s::int
            )
            SELECT (SELECT dau FROM d),
                   (SELECT count(*) FROM can),
                   (SELECT count(*) FROM can c
                     WHERE EXISTS (SELECT 1 FROM fls_chup p
                                    WHERE p.lan = %(lan)s
                                      AND date_trunc('hour',
                                            p.doc_luc AT TIME ZONE %(mui)s)
                                          = c.h)),
                   (SELECT array_agg(to_char(c.h, 'DD/MM HH24:MI')
                                     ORDER BY c.h DESC)
                      FROM (SELECT h FROM can c2
                             WHERE NOT EXISTS
                               (SELECT 1 FROM fls_chup p
                                 WHERE p.lan = %(lan)s
                                   AND date_trunc('hour',
                                         p.doc_luc AT TIME ZONE %(mui)s)
                                       = c2.h)
                             ORDER BY h DESC LIMIT 12) c)
            """,
            {"lan": lan, "mui": MUI, "nay": g, "nhip": ACTOR_NHIP,
             "dau": GIO_DAU, "cuoi": GIO_CUOI, "cua_so": cua_so})
        dau, phai, co, gan = cur.fetchone()
    return {"lan": lan, "anh_dau_tien": dau, "cua_so": cua_so,
            "gio_phai_co": int(phai or 0), "gio_co_anh": int(co or 0),
            "gio_trong": int(phai or 0) - int(co or 0),
            "trong_gan_nhat": list(gan or [])}
