# -*- coding: utf-8 -*-
"""⛔⛔ Canh **TỪ VỰNG**, ⛔ không canh dữ liệu — `GAP-PII-01`.

`QĐ-ITL-92` *(07/09)* cấm đọc đúng **một** trường: `Description`. Nó viết
đúng cho **lằn bank**, vì lúc ấy ⛔ **chưa ai đo lằn QUỸ**.

Đo sống cả **68 sheet** ngày 08/09 thì lằn quỹ khác hẳn: **3/8** sheet mang
cột **dữ liệu cá nhân**, và bản khai của kế toán bên ấy đánh số tới **15**
trường — `10` `ID Employee I ID Name` · `11` `Họ và tên (*)` ·
`12` `Số CMND/CCCD/Passport (*)`.

⭐⭐ **Vì sao canh ở TỪ VỰNG chứ ⛔ không ở dữ liệu.** Hôm nay `_soi_khai` là
   một **danh sách TRẮNG** 6 tên, nên ⛔ không số căn cước nào lọt được. Nhưng
   danh sách trắng chỉ bảo vệ **chừng nào ⛔ chưa ai nới nó** — và nới nó là
   việc **hoàn toàn hợp lý** sẽ có người làm: trường `8` = `Legal Entity` và
   `15` = `CDT` là hai thứ **thật sự đáng lấy** *(lằn bank phải chờ ghép PM
   mới có, tỷ lệ ghép gần kịch trần **33,8%**)*.

⇒ Người ấy sẽ mở `SAU_TRUONG` **vì một lý do đúng**, và nếu mở máy móc theo
  số `1`…`15` thì kéo luôn `11` và `12` vào. Bài này đỏ **ngay giây đó**,
  ⛔ không đợi tới lúc dữ liệu cá nhân đã nằm trong kho — lúc ấy thì muộn.
"""
from __future__ import annotations

import pytest

from fls.adapters.sao_ke import SAU_TRUONG, TRUONG_DOC_DUOC, truong_cam_doc

# ⭐ Tên cột **THẬT**, chép nguyên từ dòng 2 của sheet quỹ, đo 08/09.
#    ⛔ Không phải ví dụ tôi bịa — nếu bịa thì phép canh này ⛔ không chứng
#    minh được nó bắt được **thứ đang có thật ngoài kia**.
#
# ⚠⚠ **BA TÊN ĐÃ CHUYỂN VẾ 08/09 — ghi ra chứ ⛔ không sửa lặng lẽ.**
#    Bản đầu của tệp này xếp `ID Employee I ID Number` · `Chức danh` ·
#    `EmpTrack 2 I Ngạch 2` vào nhóm **LÀNH**, theo luật hẹp *(chỉ cấm giấy
#    tờ tuỳ thân + họ tên)*. Owner chốt **`QĐ-ITL-107`: cấm CẢ khối nhân sự
#    `9`…`14`** ⇒ ba tên ấy nay **cố ý bị cấm**, và ba bài đã **đỏ thật**
#    trước khi tôi dời chúng.
#
#    ⛔ Đây ⛔ **KHÔNG** phải nới cổng cho xanh *(`R-A5`)* — nó là **siết**:
#    tập cấm đi từ **3** tên lên **6**. Phép kiểm ⛔ không đổi, chỉ **kỳ vọng**
#    đổi, vì **luật** đổi, vì **người có quyền** đổi nó.
#
#    ⭐ Vì sao owner chọn rộng hơn phép đo, và vì sao nó đúng: hai trường
#    **đáng lấy** là `8` `Legal Entity` và `15` `CDT`, nằm **NGOÀI** khối
#    `9`…`14`. Đo 08/09: `LE` ở cột `H`, khối nhân sự `I`…`N`, `CDT` ở `O`
#    — **liền mạch**. ⇒ Cấm cả khối **⛔ không mất gì**.
COT_THAT_CO_PII = (
    # giấy tờ tuỳ thân + họ tên  (trường 11 · 12)
    "Số CMND/CCCD/Passport (*)",
    "Họ và tên (*)",
    # mã + tên nhân viên  (trường 9 · 10)
    "ID Employee I ID Name",
    "ID Employee I ID Number",
    # chức danh + ngạch  (trường 13 · 14)
    "Chức danh",
    "EmpTrack 2 I Ngạch 2",
)

# ⭐ Hai tên đầu là **hai trường owner chốt LẤY** (`QĐ-ITL-108`). Chúng phải
#    ⛔ **không** bị mẫu cấm chạm tới — nếu chạm thì luật vừa mở đã tự chặn
#    đúng thứ nó cho phép.
COT_THAT_KHONG_PII = (
    "Legal Entity I Pháp nhân ", "CDT",
    "Transaction date", "Description", "Currency", "Debit", "Credit",
    "Reference number", "Reference number_adjust", "Note",
    "Check trùng", "Check trùng_Reference number", "Closing Balance",
)


def test_tu_vung_doc_duoc_KHONG_duoc_chua_truong_CAM():
    """⛔⛔ Cổng chính. Đỏ ngay giây ai thêm một tên PII vào `SAU_TRUONG`."""
    xau = [t for t in SAU_TRUONG if truong_cam_doc(t)]
    assert xau == [], (
        "⛔ `SAU_TRUONG` dang chua truong mang DU LIEU CA NHAN: %s. "
        "Neu ban vua mo tu vung de lay `Legal Entity`/`CDT` — do la viec "
        "DUNG, nhung ⛔ dung keo ca `11`/`12` theo." % xau)
    xau2 = [t for t in TRUONG_DOC_DUOC if truong_cam_doc(t)]
    assert xau2 == [], "⛔ `TRUONG_DOC_DUOC` chua truong CAM: %s" % xau2


@pytest.mark.parametrize("ten", COT_THAT_CO_PII)
def test_phep_canh_BAT_DUOC_ten_cot_that(ten):
    """⛔ Cổng chung #7: một phép canh ⛔ không bắt được gì là phép canh CHẾT.

    Ba tên dưới đây là **tên cột thật** đang sống trong sổ quỹ.
    """
    assert truong_cam_doc(ten), (
        "⛔ mau `RE_TRUONG_CAM` ⛔ KHONG bat duoc %r — day la ten cot THAT "
        "trong `P100 | Cash Ledger`, do 2026-09-08" % ten)


@pytest.mark.parametrize("ten", COT_THAT_KHONG_PII)
def test_phep_canh_KHONG_bat_NHAM_cot_lanh(ten):
    """⛔ Chặn quá tay cũng là hỏng: một luật cấm cả `Debit` sẽ bị gỡ ngay."""
    assert not truong_cam_doc(ten), (
        "⛔ mau bat NHAM %r — cot nay ⛔ KHONG mang du lieu ca nhan. Mot luat "
        "cam qua rong se bi go bo, va khi do no ⛔ khong bao ve gi nua" % ten)


def test_ghi_khai_TU_CHOI_truong_cam_va_noi_dung_ly_do():
    """⛔ Chặn ở **chỗ ghi**, ⛔ không chỉ ở từ vựng.

    ⭐ Và thông báo phải nói **cấm**, ⛔ không nói **lạ**: *"tên lạ"* dẫn
      người ta đi **thêm tên vào `SAU_TRUONG`** — đúng việc phải ⛔ không bao
      giờ làm với số căn cước.
    """
    from fls.repo.khai_cot import LoiKhai, _soi_khai

    with pytest.raises(LoiKhai) as e:
        _soi_khai({"Date": 0, "Số CMND/CCCD/Passport (*)": 11})
    s = str(e.value)
    assert "CÁ NHÂN" in s or "CA NHAN" in s, \
        "⛔ thong bao ⛔ khong noi day la du lieu ca nhan: %s" % s
    assert "lạ" not in s, \
        "⛔ thong bao goi day la 'ten la' — no se dan nguoi ta di THEM ten"


def test_ban_khai_6_truong_HOM_NAY_van_di_qua_binh_thuong():
    """⛔ Phép siết ⛔ không được làm hỏng đường đang chạy."""
    from fls.repo.khai_cot import _soi_khai

    khai = {t: i for i, t in enumerate(SAU_TRUONG)}
    assert _soi_khai(khai) == khai


def test_hai_truong_THEM_cua_lan_quy_di_qua_duoc():
    """⭐ `QĐ-ITL-108` — `Legal Entity` và `CDT` phải **nhận được**.

    Lằn quỹ gõ sẵn hai thứ này **tại nguồn**; lằn bank phải **chờ ghép PM**
    mới có, tỷ lệ gần kịch trần **33,8%**. Bỏ chúng là **vứt một phân loại
    đã có sẵn**.
    """
    from fls.adapters.sao_ke import TRUONG_THEM_QUY
    from fls.repo.khai_cot import _soi_khai

    khai = {t: i for i, t in enumerate(SAU_TRUONG)}
    khai.update({"Legal Entity": 7, "CDT": 14})
    assert _soi_khai(khai) == khai
    for t in TRUONG_THEM_QUY:
        assert not truong_cam_doc(t), \
            "⛔ %r vua duoc phep LAY ma lai bi mau CAM chan" % t


def test_so_dong_1_nhan_DUNG_8_va_15_chu_KHONG_nhan_9_toi_14():
    """⛔⛔ Lằn quỹ đánh số tới `15`. Nhận **đúng hai** số có giá trị.

    ⭐ Bài này khoá **chỗ nguy nhất** của `QĐ-ITL-108`: mở từ `6` lên `15`
      *(hoặc thêm bất kỳ số nào trong `9`…`14`)* là kéo khối nhân sự vào.
    """
    from fls.adapters.sao_ke import SO_TRUONG

    assert SO_TRUONG.get("8") == "Legal Entity"
    assert SO_TRUONG.get("15") == "CDT"
    lot = [s for s in ("7", "9", "10", "11", "12", "13", "14")
           if s in SO_TRUONG]
    assert lot == [], (
        "⛔ `SO_TRUONG` dang nhan so %s — `9`…`14` la khoi NHAN SU bi cam "
        "(QD-ITL-107), `7` la `Note` ⛔ khong ai xin" % lot)
