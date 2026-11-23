# -*- coding: utf-8 -*-
"""SỔ ACTOR — một chỗ khai **ai ⛔ phải người** và **dòng nào là UAT** (`WO-011`).

⛔⛔⛔ **Vì sao có tệp này — thước mốc `B` đã vỡ BA lần, cùng một kiểu.**

  ⓵ 10/09: máy ghi `reason` *(`dung-lai-so@apero.vn`, **93.666** dòng)* ⇒
     `B2`·`B3`·`B5` lật XANH với **0** cú bấm người ⇒ loại `evt_type='reason'`.
  ⓶ 18/09: máy tự ghép ghi **2.219** sự kiện `match` actor `may@fls`
     *(`QĐ-ITL-143`)* ⇒ lại XANH, ⛔ ai thấy suốt 13 ngày *(`KQ-002 F-2`)* ⇒
     `WO-001` loại **đúng một** actor máy.
  ⓷ 01/10: hai dòng UAT của owner *(`QĐ-ITL-150 ⓐ`)* ⇒ loại `reason` bắt đầu
     `'UAT '` — nhận bằng **chữ**, nên `'uat …'`, `' UAT …'`, `'UAT02/10'` vẫn
     tính là người *(`KQ-010 F-2 ⓒ`)*.

  ⇒ Lần nào cũng **trừ đi cái đã biết là máy** — và cái *đã biết* là **một**
    chuỗi gõ tay trong một câu SQL, trong khi đo 01/10 khuya mã có **8** actor
    ⛔ phải người *(`WO-011` mục Dữ liệu)*. Lần vỡ thứ tư chỉ cần một tiến trình
    máy mới.

⭐ Luật của tệp này *(`09_MILESTONES` **v1.14** §2 ⓐ…ⓔ)*:

  ⓐ **Mọi** actor ⛔ phải người khai ở `ACTOR_MAY` — tiến trình máy **và** tệp
    lệnh / công cụ kiểm. Mọi chỗ khác **lấy từ đây**, ⛔ gõ lại chuỗi. Bài quét
    mã `tests/repo/test_danh_muc_actor.py` đỏ nếu một hằng `…@fls…` /
    `…@apero.vn` trong `fls/` + `tools/` ⛔ thuộc `ACTOR_MAY ∪ ACTOR_DA_THAY`.
  ⓑ **Người thật** ⇔ `actor` ⛔ thuộc `ACTOR_MAY` **và** ⛔ UAT.
  ⓒ Actor trên kho thật ⛔ thuộc **cả hai** sổ ⇒ **vẫn đếm là người** *(ⓑ)*,
    nhưng cổng mốc `B` gọi tên nó một lần *(`⚠ ACTOR MỚI`)* + **NO** cho tới khi
    ai đó khai nó vào một trong hai sổ. ⇒ Hở của danh sách đen *(máy mới quên
    khai ⇒ tính là người)* ⛔ còn **im lặng**.
  ⓓ UAT nhận bằng **một** hàm Python + **một** mẩu SQL sinh cùng một luật.
  ⓔ Áp cho **mọi** cổng *"người đã làm"*: `B2`·`B3`·`B4`·`B5` · `khop_owner C8`
    · `BA-14 G-d`.

⏸ **Đây ⛔ phải danh mục "ai là kế toán"** — cái đó owner **hoãn** 02/10
  *("defer phần tài khoản, làm xong công cụ đã")*. `ACTOR_DA_THAY` chỉ là sổ
  **ghi nhận** những actor ⛔ phải máy đã từng xuất hiện, để cổng ⛔ báo lại.
"""
from __future__ import annotations

# ══ ACTOR_MAY — từng hằng một, có chủ ═══════════════════════════════════════
#
# ⭐ Mỗi hằng một dòng, ghi **ai dùng nó**. Thêm một tiến trình máy ⇒ thêm một
#   dòng ở đây **và** vào `ACTOR_MAY` dưới — ⛔ gõ chuỗi ở tệp của tiến trình.

# `fls/repo/may_ghep.py` — máy tự ghép + gợi ý `hd`/`cdt1` (`QĐ-ITL-143`).
#   Ghi `match` vào `fls_queue_event` *(2.219 dòng trên sổ thật, 18/09)* và
#   **4.424** bút toán `may_goi_y`.
ACTOR_MAY_GHEP = "may@fls"
# `fls/repo/nhip_chup.py` — nhịp chụp do BỘ HẸN GIỜ gọi (`QĐ-ITL-114`).
ACTOR_NHIP = "nhip@fls"
# `fls/repo/nhip_chup.py` — cùng nhịp nhưng **gõ tay** *(⛔ được đếm cho `A1`)*.
ACTOR_NHIP_TAY = "nhip@fls(tay)"
# `tools/dung_lai_so.py` + `tools/don_ly_do_sai.py` — dựng lại sổ 10/09; ghi
#   **108.128** sự kiện `reason` *(`lo_nap` → `ghi_ly_do`)*.
ACTOR_DUNG_LAI_SO = "dung-lai-so@apero.vn"
# `tools/chay_cua.py` — mặc định `--actor` của máy dựng để tự xem *(8088)*.
ACTOR_CHAY_CUA = "thu@apero.vn"
# `tools/verify_cua_ghi.py` — thẻ thử của công cụ kiểm cửa GHI.
ACTOR_VERIFY_CUA_GHI = "cong-ghi@apero.vn"
# `tools/verify_cua_that.py` — thẻ thử của công cụ kiểm cửa ĐỌC trên kho thật.
ACTOR_VERIFY_CUA_THAT = "cong@apero.vn"
# `tools/verify_sua_duoc_gi.py` — công cụ **đóng vai** kế toán trên kho TEST để
#   trả lời *"kế toán sửa được gì"*. ⚠ Trước `WO-011` nó ghi `ke-toan@apero.vn`
#   / `ke-toan-2@apero.vn` — một tên **giống người**, trong khi chính chuỗi ấy là
#   actor **người mẫu** của bài nghiệm thu `KQ-002` *(`HOI-012` câu 1)*. ⇒ Đổi
#   sang tên máy: một công cụ ⛔ được mượn tên một người *(cùng luật
#   `tools/nap_nguon_va_khai.py::MAY`)*.
ACTOR_VERIFY_SUA = "verify-sua-duoc-gi@fls"
ACTOR_VERIFY_SUA_2 = "verify-sua-duoc-gi-2@fls"

ACTOR_MAY: frozenset[str] = frozenset({
    ACTOR_MAY_GHEP, ACTOR_NHIP, ACTOR_NHIP_TAY, ACTOR_DUNG_LAI_SO,
    ACTOR_CHAY_CUA, ACTOR_VERIFY_CUA_GHI, ACTOR_VERIFY_CUA_THAT,
    ACTOR_VERIFY_SUA, ACTOR_VERIFY_SUA_2,
})

# ══ ACTOR_DA_THAY — actor ⛔ phải máy đã từng xuất hiện trên kho THẬT ═══════
#
# ⛔ **⛔ phải** danh mục kế toán *(hoãn — `WO-011 Q1`)*. Một tên ở đây nghĩa là
#   *"đã có người nhìn thấy nó và xác nhận nó ⛔ phải máy"*; cổng mốc `B` thôi
#   gọi tên nó. Nó **vẫn** chỉ được tính là người khi dòng ⛔ UAT.
# `khanhcq@apero.vn` — owner; xuất hiện 01/10 *(UAT ghép/bỏ ghép `itl_id 27728`
#   — `QĐ-ITL-150` gọi tên)*.
ACTOR_DA_THAY: frozenset[str] = frozenset({"khanhcq@apero.vn"})


# ══ UAT — MỘT luật, hai mặt (Python + SQL) ══════════════════════════════════
#
# ⭐ `09` v1.13 ⓓ: `reason` **bỏ khoảng trắng đầu**, ⛔ phân biệt hoa thường,
#   bắt đầu `UAT` và ký tự kế tiếp **⛔ phải chữ cái** *(hoặc hết chuỗi)*.
#   `NULL` ⇒ ⛔ UAT *(cú `Xong` của người ghi `reason = NULL` — `KQ-010 F-1`
#   đột biến `M5`)*.
#
# ⚠ "Khoảng trắng" khai **TƯỜNG MINH**, ⛔ dùng `str.isspace` / `[[:space:]]`:
#   đo 02/10 trên kho *(`en_US.utf8`)* — `[[:space:]]` **⛔ nhận** `U+00A0`
#   *(NBSP)* trong khi `'\u00a0'.isspace()` là `True` ⇒ hai mặt **lệch** đúng ở
#   một ký tự hay dính vào khi dán từ trình duyệt. Một tập khai tay thì hai mặt
#   đọc **cùng một danh sách**.
# ⚠ "Chữ cái" thì dùng `[[:alpha:]]` ↔ `str.isalpha()` — bài thử bảng mẫu ghim
#   hai mặt trùng nhau *(gồm `é`, `đ`, `Ư`, `中`, chữ số, dấu câu)*.
KHOANG_TRANG_DAU = " \t\n\r\f\v\u00a0\u3000\ufeff"
_KT_SQL = "[ \\t\\n\\r\\f\\v\\u00a0\\u3000\\ufeff]"


def la_uat(reason: str | None) -> bool:
    """`True` ⇔ dòng này là UAT *(thử đường ghi — ⛔ BAO GIỜ là người thật)*."""
    if reason is None:
        return False
    s = reason.lstrip(KHOANG_TRANG_DAU)
    if s[:3].lower() != "uat":
        return False
    return len(s) == 3 or not s[3].isalpha()


def _mau_uat() -> str:
    return f"'^{_KT_SQL}*uat([^[:alpha:]]|$)'"


def sql_la_uat(cot: str) -> str:
    """Mẩu SQL **cùng luật** `la_uat` — `TRUE` ⇔ UAT. ⛔ Mang dấu `%`."""
    return f"coalesce({cot}, '') ~* {_mau_uat()}"


def sql_khong_uat(cot: str) -> str:
    """Phủ định của `sql_la_uat` — ⚠ `NULL` ⇒ ⛔ UAT ⇒ `TRUE` *(giữ `coalesce`)*."""
    return f"coalesce({cot}, '') !~* {_mau_uat()}"


def _chuoi_sql(x: str) -> str:
    return "'" + x.replace("'", "''") + "'"


def sql_ngoai_may(cot: str, may: frozenset[str] = ACTOR_MAY) -> str:
    """Mẩu SQL `TRUE` ⇔ `cot` ⛔ thuộc `ACTOR_MAY`. Thứ tự **sắp xếp** ⇒ chuỗi
    sinh ra ổn định *(cổng so nó với bản chép trong câu SQL thuần — xem
    `tools/kiem_so_song.py::_kiem_hang_may`)*.

    ⚠ `coalesce(…, '')`: `actor` `NULL` *(⛔ có trên kho — cột `NOT NULL`)* thì
      tính là **người** — chiều cổng **nhích** để có người nhìn, ⛔ chiều im.
    """
    ds = ", ".join(_chuoi_sql(a) for a in sorted(may))
    return f"coalesce({cot}, '') <> all (array[{ds}])"
