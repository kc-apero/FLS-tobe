"""⛔⛔ CONG QUET MA NGUON: chi MOT file duoc ghi thao tac cua nguoi.

Sau khi `QĐ-ITL-16` bo buoc duyet va `QĐ-ITL-27` khai tu vai nguoi hau kiem,
**nhat ky la lop kiem soat duy nhat con lai**. Mot duong ghi khong sinh nhat ky
⛔ khong phai *"thieu mot tinh nang"* — no la **mot lo trong lop kiem soat cuoi
cung**.

★ Cung ho voi bai da co: *"luat o-loi tung co BON ban sao"*. Cach chua ⛔ khong
phai sua tung ban sao ma la **lam cho ban sao moi khong the ton tai**.

⚠ Quet bang `ast` chu ⛔ khong bang `in`: docstring cua chinh file nay nhac ten
cac bang, va mot cong bao dong vi doc chinh ghi chu cua no la cong sap bi go ra.
"""
from __future__ import annotations

import ast
import re
import pathlib

# ⭐ `fls_pm_unlink` (them 2026-08-28) vao day chu ⛔ KHONG vao
# `PM_LINK_HAI_CHO`: no ⛔ khong co duong ghi tu bo nap — **may ⛔ khong bao gio
# tu bo mot moi noi**. Bo moi noi la mot quyet dinh cua NGUOI (`QĐ-ITL-69`), nen
# dung MOT cho ghi, va mot file thu hai ghi vao no la mot duong go moi noi
# ⛔ khong qua nhat ky.
BANG_CHI_MOT_CHO: frozenset[str] = frozenset({
    "fls_adjustment", "fls_journal", "fls_queue_event", "fls_pm_unlink"})
CHO_DUY_NHAT = "ghi_tay.py"

# ⛔⛔ `fls_pm_link` la mot ca RIENG, va no phai duoc khai rieng chu ⛔ khong nhet
# vao `BANG_CHI_MOT_CHO`. Ly do: bang nay co **HAI** duong ghi hop phap, va chung
# khac ban chat:
#   · `chay_nap.py`  — MAY ghep luc nap (hinh `A`/`B`/`C`, cong Σ tu dong)
#   · `ghi_tay.py`   — NGUOI ghep tay o man `F01` (hinh `T`, `QĐ-ITL-48`)
# Nhet vao danh sach mot-cho thi bai se do o `chay_nap.py`, va cach "chua" de nhat
# la go cong ra. ⇒ khai HAI file, va van chan file thu BA.
PM_LINK_HAI_CHO: frozenset[str] = frozenset({"chay_nap.py", "ghi_tay.py"})
GOC = pathlib.Path(__file__).resolve().parents[2] / "fls"


def _cau_sql(cay: ast.AST) -> list[tuple[int, str]]:
    """Moi HANG CHUOI trong ma nguon, kem so dong. ⛔ Khong doc ghi chu.

    Bat ca chuoi noi bang `+` va f-string, vi mot cau `INSERT` ghep tu hai manh
    la cach de nhat de di qua mot phep quet.
    """
    # ⭐⭐ HẰNG chuỗi mức module — giải TRƯỚC, để câu nối bằng tên còn đọc được.
    #
    # ⛔⛔ **Vì sao thêm (09/09), và nó là bài học của CHÍNH BUỔI SÁNG hôm đó.**
    # Cổng `tools/soi_bang_tuyen.py` ⛔ không đọc được một hằng SQL dựng bằng
    # `.replace()` ⇒ hai bảng **tàng hình** với nó. Ở đây y hệt: `don_chup.py`
    # khai **HÀNG RÀO một lần** rồi nối `" AND " + _HANG_RAO` vào ba câu xoá —
    # cách viết **đúng** *(một bản khai, ⛔ không ba bản sẽ lệch)*, nhưng phép
    # quét cũ chỉ thấy ba mảnh rời và báo *"3 câu ⛔ không có hàng rào"*.
    #
    # ⇒ Chữa ở **CỔNG**, ⛔ không bắt mã nguồn nhân ba hàng rào cho cổng đọc
    #   được. Một cổng buộc mã phải xấu đi là một cổng sẽ bị gỡ.
    hang: dict[str, str] = {}
    for n in cay.body:
        if isinstance(n, ast.Assign) and len(n.targets) == 1 \
                and isinstance(n.targets[0], ast.Name):
            v = _chuoi_cua(n.value, hang)
            if v:
                hang[n.targets[0].id] = v

    ra: list[tuple[int, str]] = []
    for n in ast.walk(cay):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            ra.append((n.lineno, n.value))
        elif isinstance(n, ast.JoinedStr):
            ghep = "".join(v.value for v in n.values
                           if isinstance(v, ast.Constant)
                           and isinstance(v.value, str))
            ra.append((n.lineno, ghep))
        elif isinstance(n, ast.BinOp) and isinstance(n.op, ast.Add):
            # ⚠ Thêm bản ĐÃ NỐI **cạnh** các mảnh rời, ⛔ không thay chúng:
            #   mọi phép đo trong tệp này là `any`/`all` trên danh sách ứng
            #   viên, nên một bản dư ⛔ không làm hỏng phép nào — còn thiếu bản
            #   đã nối thì cổng **mù** với chính cách viết đúng.
            v = _chuoi_cua(n, hang)
            if v:
                ra.append((n.lineno, v))
    return ra


def _chuoi_cua(nut: ast.AST, hang: dict[str, str]) -> str:
    """Giá trị chuỗi của một biểu thức, nếu suy được. ⛔ Không suy được ⇒ `''`.

    ⛔ ⛔ Không đoán: một `Name` ⛔ không có trong `hang` trả `''`, ⛔ không trả
      tên biến — trả tên biến là để một cổng khớp `RAO_XOA` với chữ
      `_HANG_RAO`, tức xanh cho một hàng rào **đã bị sửa nội dung**.
    """
    if isinstance(nut, ast.Constant) and isinstance(nut.value, str):
        return nut.value
    if isinstance(nut, ast.Name):
        return hang.get(nut.id, "")
    if isinstance(nut, ast.BinOp) and isinstance(nut.op, ast.Add):
        return (_chuoi_cua(nut.left, hang) + _chuoi_cua(nut.right, hang))
    if isinstance(nut, ast.JoinedStr):
        return "".join(_chuoi_cua(p, hang) for p in nut.values)
    if isinstance(nut, ast.FormattedValue):
        return " "
    return ""


# ⛔⛔ Phep khop phai bat dau bang DONG TU SQL, ⛔ khong phai "co chua".
#
# Ban dau toi viet `"update " in t` — va bai `test_ghi_tay_KHONG_ghi_vao_so`
# **do ngay**, vi chinh docstring cua `dao_but_toan` co cau *"⛔ KHONG `UPDATE
# state` cua dong cu"*. Tuc la cong bao dong vi doc dung cai ghi chu noi rang
# viec do bi cam. Mot cong bao dong nhu the thi nguoi ta go cong chu khong sua ma.
_DONG_TU = ("insert into", "update", "delete from")


def _cau(s: str) -> str:
    return " ".join(s.lower().split())


def _la_ghi(s: str, bang: str) -> bool:
    c = _cau(s)
    return any(c.startswith(f"{tu} {bang}") for tu in _DONG_TU)


def _la_sua_hay_xoa(s: str) -> bool:
    c = _cau(s)
    return c.startswith("update ") or c.startswith("delete from")


def test_chi_ghi_tay_duoc_ghi_vao_ba_bang_mang_vet():
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        if f.name == CHO_DUY_NHAT:
            continue
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            for bang in BANG_CHI_MOT_CHO:
                if _la_ghi(s, bang):
                    xau.append(f"{f.relative_to(GOC)}:{dong} ghi vao {bang}")
    assert xau == [], (
        "chi `fls/repo/ghi_tay.py` duoc ghi vao " + str(sorted(BANG_CHI_MOT_CHO))
        + " — de lop kiem soat cuoi cung khong co lo: " + " · ".join(xau))


def test_ghi_tay_that_su_co_ghi_vao_ba_bang_do():
    """⛔ Cong chung #7: chung minh phep quet DA DO DUOC GI.

    Neu ⓐ cong chi kiem *"khong ai khac ghi"* va ⓑ ban than `ghi_tay.py` cung
    khong ghi, thi cong xanh ma **khong co gi duoc bao ve** — dung cai bay
    *"khong do gi thi tat nhien khong thay loi"*.
    """
    f = GOC / "repo" / CHO_DUY_NHAT
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    thay = {b for _d, s in _cau_sql(cay) for b in BANG_CHI_MOT_CHO
            if _la_ghi(s, b)}
    assert thay == BANG_CHI_MOT_CHO, f"ghi_tay.py chi ghi vao {sorted(thay)}"


def test_fls_pm_link_chi_duoc_ghi_o_HAI_cho_da_khai():
    """⛔ Moi noi lenh chi chi sinh ra o HAI cho: bo nap (may) va cua ghi (nguoi).

    Mot cho thu ba ghi vao bang nay nghia la co moi noi **khong qua cong Σ** —
    va bat bien `Σ moi noi = tien dong bank` la thu duy nhat lam bang noi nay
    dang tin.
    """
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        if f.name in PM_LINK_HAI_CHO:
            continue
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            if _la_ghi(s, "fls_pm_link"):
                xau.append(f"{f.relative_to(GOC)}:{dong}")
    assert xau == [], (
        "chi " + str(sorted(PM_LINK_HAI_CHO)) + " duoc ghi vao `fls_pm_link`: "
        + " · ".join(xau))


def test_CA_HAI_cho_do_that_su_co_ghi_vao_fls_pm_link():
    """⛔ Cong chung #7: neu ca hai file deu KHONG ghi thi bai tren xanh ma
    ⛔ khong bao ve gi. Doi tung file phai THAT SU co cau ghi."""
    thieu = []
    for ten in sorted(PM_LINK_HAI_CHO):
        f = GOC / "repo" / ten
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        if not any(_la_ghi(s, "fls_pm_link") for _d, s in _cau_sql(cay)):
            thieu.append(ten)
    assert thieu == [], f"khai la cho ghi ma ⛔ khong ghi: {thieu}"


def test_ghi_tay_KHONG_ghi_vao_so_va_KHONG_sua_but_toan_cu():
    """⛔ `INV-I08`: ⛔ khong `UPDATE`/`DELETE` o BAT KY dau trong tang ghi —
    ke ca len `fls_adjustment`. Dao la **them mot dong**."""
    f = GOC / "repo" / CHO_DUY_NHAT
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    xau = []
    for dong, s in _cau_sql(cay):
        if _la_sua_hay_xoa(s):
            xau.append(f"{dong}: {s[:70]}")
        if _cau(s).startswith("insert into fls_itl"):
            xau.append(f"{dong}: ghi vao SO — {s[:70]}")
    assert xau == [], "tang ghi co cau sua/xoa: " + " · ".join(xau)


# ⭐⭐ `fls_khai_cot` (thêm 2026-09-07, `CR#11`) — MỘT chỗ ghi, và chỗ ấy ⛔
# KHÔNG phải `ghi_tay.py`.
#
# ⛔⛔ Vì sao ⛔ không nhét vào `BANG_CHI_MOT_CHO`: ba bảng kia là **vết của một
# thao tác NGƯỜI làm trên một DÒNG SỔ** — chúng phải đi cùng nhật ký 7 trường
# neo vào `itl_id`. Một bản khai ánh xạ cột ⛔ không nói về dòng sổ nào cả; nó
# nói *"sheet này đọc thế nào"*. Nhét chung thì `ghi_tay.py` sẽ phải bịa ra một
# `itl_id` cho một việc ⛔ không có dòng sổ — và một `itl_id` bịa trong nhật ký
# còn tệ hơn ⛔ không có nhật ký.
#
# ⭐ Nhưng nó VẪN phải một-chỗ, vì lý do khác: **một file thứ hai ghi vào bảng
# này là một cách khai ánh xạ cột thứ hai** — tức một đường vòng qua luật *"đủ
# 6 trường hoặc ⛔ không ghi gì"* và qua luật *"chỉ-thêm"*.
KHAI_COT_MOT_CHO = "khai_cot.py"


def test_chi_khai_cot_py_duoc_ghi_vao_fls_khai_cot():
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        if f.name == KHAI_COT_MOT_CHO:
            continue
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            if _la_ghi(s, "fls_khai_cot"):
                xau.append(f"{f.relative_to(GOC)}:{dong}")
    assert xau == [], (
        "chi `fls/repo/khai_cot.py` duoc ghi vao `fls_khai_cot` — mot file thu "
        "hai la mot duong vong qua luat 'du 6 truong hoac khong ghi gi': "
        + " · ".join(xau))


def test_khai_cot_py_THAT_SU_co_ghi_vao_bang_do():
    """⛔ Cổng chung #7: nếu ⓐ ⛔ không ai khác ghi và ⓑ chính nó cũng ⛔ không
    ghi, thì cổng trên xanh mà ⛔ **không bảo vệ gì**."""
    f = GOC / "repo" / KHAI_COT_MOT_CHO
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    assert any(_la_ghi(s, "fls_khai_cot") for _d, s in _cau_sql(cay)), (
        f"{KHAI_COT_MOT_CHO} khai la cho ghi ma ⛔ khong he ghi")


# ⭐⭐ `fls_chup*` (thêm 2026-09-08, `QĐ-ITL-110`) — MỘT chỗ ghi cho **ba** bảng.
#
# ⛔⛔ Vì sao ba bảng chung một cổng: chúng **phải được ghi CÙNG NHAU trong một
# giao dịch**, và ba luật của tầng ấy *(⛔ không ảnh chụp rỗng · ⛔ không dòng
# thuộc nguồn chưa khai đọc · ⛔ không ô mang dữ liệu cá nhân)* chỉ có nghĩa
# khi cả ba bảng đi qua **một** hàm. Một file thứ hai ghi vào **bất kỳ** bảng
# nào trong ba là một đường vòng qua **cả ba** luật — nặng nhất là luật cuối:
# một `INSERT` lạ vào `fls_chup_dong` có thể chở **số CMND** vào kho.
CHUP_MOT_CHO = "chup.py"
CHUP_BANG = ("fls_chup", "fls_chup_nguon", "fls_chup_dong")


# ⭐⭐⭐ Tệp thứ HAI được chạm ba bảng ấy — và **CHỈ bằng `DELETE`**
#    *(thêm 09/09, `QĐ-ITL-115` mốc `A2`)*.
#
# ⛔⛔ **Vì sao đây ⛔ KHÔNG phải một chỗ nới cổng.** `QĐ-ITL-114` chốt nhịp
# chụp **mỗi giờ** ⇒ **3.000 ảnh/năm**, mà ảnh **thật sự được nạp** chỉ ~250
# ⇒ **11/12 ảnh mỗi ngày ⛔ không bút toán nào trỏ tới**. Owner chốt nhịp ấy
# **cùng lúc** với phép dọn, và hai quyết định ấy ⛔ không tách rời được. Tiền
# lệ thật: `fls-test-store-grows-unbounded` — kho phình làm **4 cổng ĐỎ giả**.
#
# ⇒ Nên hai phép đo mới ở dưới **CHẶT HƠN** phép đo cũ, ⛔ không lỏng hơn:
#   ⓐ tệp dọn **⛔ KHÔNG** được có một câu `INSERT`/`UPDATE` nào;
#   ⓑ **MỌI** câu `DELETE` của nó phải mang **HÀNG RÀO** `NOT EXISTS … fls_run`
#     — tức *"⛔ không bút toán nào trỏ tới ảnh này"*. Chính hàng rào ấy giữ
#     nguyên ý nghĩa của cổng cũ: một ảnh **đã được nạp** thì ⛔ **không bao
#     giờ** bị xoá, nên ⛔ không lô nào **đã nạp** bị mất căn cứ.
CHUP_CHO_XOA = "don_chup.py"
# ⛔ Chuỗi hàng rào — so bằng **NỘI DUNG**, ⛔ không bằng một cái tên biến: một
#   cổng đọc tên biến sẽ xanh cho một hàng rào **đã bị sửa nội dung**.
RAO_XOA = "not exists (select 1 from fls_run r where r.chup_id = c.chup_id)"


def test_chi_chup_py_duoc_ghi_vao_ba_bang_anh_chup():
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        if f.name in (CHUP_MOT_CHO, CHUP_CHO_XOA):
            continue
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            for b in CHUP_BANG:
                if _la_ghi(s, b):
                    xau.append(f"{f.relative_to(GOC)}:{dong} → {b}")
    assert xau == [], (
        "chi `fls/repo/chup.py` duoc ghi vao ba bang anh chup — mot file thu "
        "hai la mot duong vong qua ca ba luat cua tang ay, nang nhat la luat "
        "cam o mang du lieu ca nhan (QD-ITL-92/107): " + " · ".join(xau))


def test_chup_py_THAT_SU_co_ghi_vao_CA_BA_bang():
    """⛔ Cổng chung #7 — và ở đây nó phải hỏi **cả ba**.

    Nếu `chup.py` chỉ ghi hai bảng thì cổng trên vẫn xanh cho bảng thứ ba, và
    bảng thứ ba ấy thành **một bảng ⛔ không ai canh**. Đúng lớp lỗi *"cổng lọc
    trên chính cột nó canh"*: xanh vì ⛔ chưa từng có khả năng đỏ.
    """
    f = GOC / "repo" / CHUP_MOT_CHO
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    cau = [s for _d, s in _cau_sql(cay)]
    thieu = [b for b in CHUP_BANG if not any(_la_ghi(s, b) for s in cau)]
    assert thieu == [], (
        f"{CHUP_MOT_CHO} khai la cho ghi ma ⛔ khong he ghi vao: {thieu}")


def test_chup_py_KHONG_co_cau_SUA_hay_XOA():
    """⛔⛔ **CHỈ-THÊM**, cưỡng chế ở tầng mã nguồn.

    Sửa một ảnh chụp tại chỗ là **đổi cái mà một lô đã nạp dựa vào** — biên bản
    9 luật của lô ấy bỗng nói về dữ liệu ⛔ không còn tồn tại, và ⛔ không ai
    thấy gì đổi. ⇒ Chụp lại chỉ có MỘT đường: `chup_id` mới.
    """
    f = GOC / "repo" / CHUP_MOT_CHO
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    xau = [f"{d}: {s[:70]}" for d, s in _cau_sql(cay) if _la_sua_hay_xoa(s)]
    assert xau == [], "tang anh chup co cau sua/xoa: " + " · ".join(xau)


def test_don_chup_py_CHI_co_cau_XOA__khong_INSERT_khong_UPDATE():
    """⛔ Tệp dọn là tệp **chỉ xoá**. Một câu `INSERT` ở đây là một đường vòng
    qua **cả ba** luật của tầng ảnh chụp *(⛔ không ảnh rỗng · ⛔ không dòng
    thuộc nguồn chưa khai · ⛔ không ô mang dữ liệu cá nhân)* — nặng nhất là
    luật cuối."""
    f = GOC / "repo" / CHUP_CHO_XOA
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    xau = [f"{d}: {s[:70]}" for d, s in _cau_sql(cay)
           if _cau(s).startswith("insert into") or _cau(s).startswith("update ")]
    assert xau == [], (
        f"`{CHUP_CHO_XOA}` chi duoc XOA — mot cau ghi o day la mot duong vong "
        "qua ca ba luat cua tang anh chup: " + " · ".join(xau))


def test_MOI_cau_XOA_cua_don_chup_deu_CO_HANG_RAO():
    """⭐⭐⭐ **Phép đo đắt nhất của mốc `A2`.**

    `QĐ-ITL-115` đặt điều kiện bằng một câu **đo được**: *"lý do giữ dòng thô
    là để chứng minh một bút toán đến TỪ ĐÂU ⇒ ảnh ⛔ không bút toán nào trỏ
    tới thì nó ⛔ không chứng minh gì"*. Nên phép xoá **chỉ** được chạm những
    ảnh ⛔ không ai trỏ tới, và điều đó phải nằm **trong chính câu SQL**,
    ⛔ không nằm trong một biến Python ở trên nó.

    ⛔⛔ **Vì sao ⛔ không đủ nếu chỉ có bài `pg` chứng minh "ảnh đã nạp sống
      sót".** Bài ấy đo **một lần chạy** với **một hình dữ liệu**. Còn cổng này
      đọc **mọi** câu `DELETE` trong tệp — nên một câu xoá **thứ tư** thêm vào
      ngày mai mà quên hàng rào sẽ ĐỎ **ngay**, kể cả khi ⛔ không bài `pg` nào
      đi qua nhánh ấy. *"Một nhánh ⛔ chưa ai đi qua là một nhánh CHƯA BIẾT CÓ
      CHẠY"* — bài học đã ghi ngày 08/09.
    """
    f = GOC / "repo" / CHUP_CHO_XOA
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    # ⚠ Soi **TỪNG** ứng viên chuỗi, ⛔ không nối cả tệp lại: `_cau_sql` trả về
    #   **cả** các mảnh rời **và** bản đã nối, nên nối lần nữa sẽ trộn chúng
    #   vào nhau và mọi phép chia sẽ vô nghĩa.
    ung_vien = [_cau(s) for _d, s in _cau_sql(cay)]
    # ⛔ Luật đo: với **mỗi bảng** bị xoá, phải TỒN TẠI một chuỗi mang **cả**
    #   câu `DELETE` của bảng ấy **và** hàng rào. Mảnh rời ⛔ không có hàng rào
    #   là bình thường *(nó được nối lúc chạy)*; cái ⛔ không được phép là
    #   ⛔ **không tồn tại** bản nào đủ hai thứ.
    bang = sorted({c.split("delete from", 1)[1].strip().split()[0]
                   for c in ung_vien if "delete from" in c})
    assert bang == sorted(CHUP_BANG), (
        f"⛔ `{CHUP_CHO_XOA}` phai xoa DU ba bang anh chup (⛔ khong thi mot "
        f"bang thanh mot bang ⛔ khong ai don) — thay: {bang}")
    # ⛔⛔⛔ **Khớp theo BIÊN TỪ, ⛔ không theo "có chứa" — và đây là một cổng
    #    XANH GIẢ mà tôi đã tự dựng ra rồi tự bắt được bằng cách **phá có chủ
    #    ý**.**
    #
    # Bản đầu viết `f"delete from {b}" in c`. Nhưng `delete from fls_chup` là
    # **TIỀN TỐ** của `delete from fls_chup_dong` ⇒ câu xoá bảng gốc được tính
    # là *"có hàng rào"* nhờ câu xoá của **một bảng khác**. Tôi gỡ hàng rào
    # khỏi câu `DELETE FROM fls_chup` và cổng vẫn **XANH**.
    #
    # ⇒ Bài học lặp lại, và lần này trên chính cổng tôi vừa viết: *một cổng
    #   chưa từng thấy đỏ là một cổng chưa biết có sống*. ⛔ Khớp tên bảng thì
    #   luôn phải có biên từ — ba bảng ở đây có tên **lồng tiền tố nhau**.
    thieu = [b for b in bang
             if not any(re.search(r"delete from " + b + r"\b", c)
                        and RAO_XOA in c for c in ung_vien)]
    assert thieu == [], (
        f"⛔⛔ cau `DELETE` cua {thieu} ⛔ KHONG mang hang rao `{RAO_XOA}` ⇒ no "
        "co the xoa mot anh **DA DUOC NAP**, va lo nap ay mat can cu trong im "
        "lang")


def test_khai_cot_py_KHONG_co_cau_SUA_hay_XOA():
    """⛔⛔ Luật ⓐ **CHỈ-THÊM**, cưỡng chế ở tầng mã nguồn.

    Sửa một bản khai tại chỗ là **viết lại lịch sử của mọi dòng đã nạp bằng
    nó** — một dòng nạp tháng trước bỗng được giải thích bằng cách đọc của hôm
    nay, và ⛔ không ai thấy gì đổi. ⇒ Sửa khai chỉ có MỘT đường: `version` mới.
    """
    f = GOC / "repo" / KHAI_COT_MOT_CHO
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    xau = [f"{d}: {s[:70]}" for d, s in _cau_sql(cay) if _la_sua_hay_xoa(s)]
    assert xau == [], "tang khai co cau sua/xoa: " + " · ".join(xau)
