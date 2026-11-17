"""Khuôn đóng băng `ix_fx` — bảng tỷ giá `9.2.Exchange Rate` *(APERO | FS2, nhập tay)* → `IX.FX`.

    python tools/dong_bang_sheet.py ix_fx <bản_thô.json> --mong 37
        ⇒ tests/fixture/cau_hinh/ix_fx.json

AP v3.1.2 §3.2.1 hàng `IX.FX`: *"tháng yyyymm × USD · SGD · COP · VND (=1) · HKD"*, đo bảng thật
*"37 dòng 202401 → 202612 (kể cả dòng lạc 202306)"*.

⭐ **Vì sao khuôn là MỘT TỆP riêng** *(orchestrator 16/11, vòng sửa sau R1 `KQ-087`)*: các bước
`DT3` · `DT4` · … · `DT12` thêm khuôn **song song**. Khuôn khai trong chính
`tools/dong_bang_sheet.py` *(bảng `KHUON` cũ)* thì mọi bước cùng sửa một tệp ⇒ phải xếp hàng,
và mỗi lần sửa là một lần chạm vào cổng chung. ⇒ bước sau chỉ **THÊM** một tệp ở thư mục này;
công cụ tìm khuôn theo tên tệp *(`ix_fx` → `ix_fx.py`)*, ⛔ sửa công cụ.

Giao kèo một khuôn *(công cụ kiểm lúc nạp — thiếu/sai ⇒ TỪ CHỐI, exit 2)*:
    BANG · KHOA · KIEU_KHOA · COT · RA     — hằng
    thieu_lac(dong) -> {"thieu", "lac", "dai"}
        `dong` = BẢN SAO các dòng ảnh *(ô số là chuỗi đúng chữ số; ô chữ là `{"chu": …}`)*.
        ⛔ đo được ⇒ `raise ValueError(<lý do một dòng>)` ⇒ cổng ĐỎ, ảnh ghi `thieu = lac = null`.

⛔⛔ **thiếu/lạc: MỘT định nghĩa — của C1** *(`DT2-R1-03`, quyết định orchestrator)*. Bản đầu của
DT2 tự suy *lạc* theo **thứ tự hàng sheet** *("khoá nhỏ hơn khoá lớn nhất đứng trước nó")* trong
khi C1 *(`fls/cau_hinh/fx.py`, làn BE-CF chạy song song)* định nghĩa theo **`thang_dau`**. R1 đo
hai định nghĩa trên cùng một ảnh: đổi chỗ `202401`/`202402` ⇒ DT2 `lac=['202401','202306']` ↔
C1 `[202306]`; dòng lạc đứng ĐẦU ⇒ DT2 báo `thieu` **6 tháng giả** *(202307…202312, cổng ĐỎ)* ↔
C1 `thieu=[]`. Docstring C1 đã bác đúng định nghĩa theo thứ tự: *"phụ thuộc thứ tự dòng, mà ảnh
đóng băng ⛔ hứa giữ"*. ⇒ khuôn này **GỌI** `kiem` của C1 *(import, ⛔ chép)* — đổi định nghĩa ở
C1 thì khuôn đổi theo, ⛔ lệch lại.

⛔ Hệ quả đã chọn *(ghi rõ để ⛔ ai bất ngờ)*: `kiem` của C1 từ chối **cả bảng** khi một dòng
hỏng — kể cả luật nghiệp vụ như `VND ≠ 1`. Khi ấy thiếu/lạc **⛔ đo được** ⇒ cổng ĐỎ *(Đ5:
"phép ⛔ đo được là ĐỎ")*. Cũng chính là luật phòng tái phạm của `DT2-R1-02`: *"cổng đóng băng
phải chặn ít nhất mọi thứ bên tiêu thụ đầu tiên sẽ từ chối"*. Khuôn ⛔ viết lại luật nào của C1.
"""
from __future__ import annotations

import copy
from typing import Any

from fls.cau_hinh.fx import LoiFX, kiem

BANG = "IX.FX"
#: Tên cột khoá ĐÚNG như nguồn *(Q3 của `BG-086`: ảnh giữ `Month`, C5 ánh xạ `Month → yyyymm`)*.
KHOA = "Month"
KIEU_KHOA = "yyyymm"
#: AP v3.1.2 §3.2.1 — thứ tự = thứ tự cột của `9.2.Exchange Rate`.
COT = ("USD", "SGD", "COP", "VND", "HKD")
RA = "tests/fixture/cau_hinh/ix_fx.json"

#: ⭐ Tháng đầu của dải — khai **MỘT chỗ, ở đây**. Căn cứ: AP v3.1.2 §3.2.1 hàng `IX.FX`,
#: *"37 dòng 202401 → 202612 (kể cả dòng lạc 202306)"* ⇒ dải bắt đầu `202401`, và `202306`
#: *(trước `thang_dau`)* là **lạc** theo định nghĩa của C1. ⛔ suy từ dữ liệu: C1 đã nêu vì sao
#: mọi cách suy *(chuỗi liền dài nhất · tháng lẻ · thứ tự sheet)* đều giấu một tháng THIẾU.
THANG_DAU = 202401

#: Cột khoá của C1 *(`fls/cau_hinh/fx.py` — `kiem` đọc `r.get("yyyymm")`)*.
_KHOA_C1 = "yyyymm"


def thieu_lac(dong: list[dict[str, Any]]) -> dict[str, Any]:
    """Các dòng ảnh → `{"thieu", "lac", "dai"}` theo `kiem` của C1 *(`thang_dau = THANG_DAU`)*.

    Ánh xạ `Month → yyyymm` và bỏ `thu_tu` *(C1 từ chối cột lạ)* — đúng ánh xạ C5 sẽ làm. Tháng
    trả về dạng CHUỖI 6 chữ số, cùng biểu diễn với `Month` trong ảnh *(tra ngược được)*.
    """
    c1 = [{_KHOA_C1: copy.deepcopy(d.get(KHOA)), **{c: copy.deepcopy(d.get(c)) for c in COT}}
          for d in dong]
    try:
        b = kiem(c1, thang_dau=THANG_DAU, nguon=f"dong_bang_sheet:{BANG}")
    except LoiFX as e:
        dau = " · ".join(" ".join(x.split()) for x in e.ly_do[:3])
        raise ValueError(f"kiem của C1 (fls/cau_hinh/fx.py) từ chối bảng — {len(e.ly_do)} lỗi: "
                         f"{dau}{' · …' if len(e.ly_do) > 3 else ''}") from None
    cuoi = max(d.yyyymm for d in b.ky)
    return {"thieu": [str(m) for m in b.thieu], "lac": [str(m) for m in b.lac],
            "dai": f"{THANG_DAU}→{cuoi} · thang_dau {THANG_DAU} của khuôn · kiem của C1"}
