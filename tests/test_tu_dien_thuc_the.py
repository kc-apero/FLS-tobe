"""TỪ ĐIỂN THỰC THỂ — một bảng trong kho mang **ba cách gọi**, và trước
`17/09` ⛔ không chỗ nào nói chúng là MỘT *(owner hỏi: «`fls_itl` đã đúng khái
niệm, tên file excel, ggsheet chưa?»)*.

⛔⛔ **Vì sao phải có cổng chứ ⛔ không chỉ một bảng trong tài liệu.** Câu hỏi
ấy hôm nay phải **đọc tay** mới trả lời được — và một câu phải đọc tay là một
câu **sẽ được trả lời khác nhau mỗi lần**. `TU_DIEN_TEN` đã bắc cầu cho
**khâu**; nó ⛔ **không** bắc cầu cho **thực thể**, nên thêm một bảng vào kho
mà quên khai tên nghiệp vụ của nó thì ⛔ **không gì đỏ**.

⭐ **Luật:** `fls_itl` **giữ nguyên tên** — `ITL` là tên owner đang dùng hằng
ngày, còn `itl_transaction` là một tên **owner chưa từng dùng**. Cái được
chữa là **câu nối**, ⛔ không phải cái tên.
"""
from __future__ import annotations

import importlib.util
import pathlib

GOC = pathlib.Path(__file__).resolve().parents[1]
BA05 = GOC / "docs" / "ITL" / "02_BA" / "05_DATA_DICTIONARY_ERD.md"


def _m():
    sp = importlib.util.spec_from_file_location(
        "_sbd", GOC / "tools" / "sinh_ban_do_tang.py")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _bang_trong_kho() -> set[str]:
    from fls.db import schema
    return set(schema.TABLES)


def test_MOI_bang_trong_kho_deu_duoc_KHAI_TEN_nghiep_vu():
    """⭐⭐ Thêm một bảng mà quên khai tên nghiệp vụ ⇒ **ĐỎ**.

    ⛔ Đây đúng cơ chế của `tang`/`khau`: một trường của bản khai, ⛔ không
      phải một bảng vẽ tay thứ hai. Thiếu nó thì bảng mới **vô hình** với
      người đọc nghiệp vụ, và người ta sẽ tự đặt cho nó một cái tên.
    """
    m = _m()
    khai = {b for b, _, _, _ in m.TU_DIEN_THUC_THE}
    kho = _bang_trong_kho()
    assert kho <= khai, (
        f"⛔ bảng ⛔ CHƯA khai tên nghiệp vụ: {sorted(kho - khai)} — "
        "khai vào `TU_DIEN_THUC_THE` ở `tools/sinh_ban_do_tang.py`")


def test_KHONG_ten_bang_LA_trong_tu_dien():
    """⛔ Một dòng từ điển trỏ vào bảng ⛔ không tồn tại là một sợi dây đứt —
    và nó **sống sót qua mọi lần đổi schema** vì ⛔ không ai đọc lại nó."""
    m = _m()
    khai = {b for b, _, _, _ in m.TU_DIEN_THUC_THE}
    la = sorted(khai - _bang_trong_kho())
    assert not la, f"⛔ từ điển khai bảng ⛔ KHÔNG có trong kho: {la}"


def test_moi_bang_khai_DUNG_MOT_lan():
    """⛔ Hai dòng cho một bảng = hai câu trả lời cho *«nó tên là gì»*."""
    m = _m()
    ds = [b for b, _, _, _ in m.TU_DIEN_THUC_THE]
    trung = sorted({b for b in ds if ds.count(b) > 1})
    assert not trung, f"⛔ khai TRÙNG: {trung}"


def test_o_AS_IS_KHONG_duoc_de_TRONG():
    """⭐⭐ `⛔ FLS dựng mới` là một **LỜI KHAI**, ⛔ không phải một ô trống.

    ⛔⛔ Để trống thì *«AS-IS ⛔ không có thứ này»* trông **y hệt** *«chưa ai
      tra cứu»* — đúng lớp lỗi của `thu_tu IS NULL` *(«chưa khai» ⛔ không
      phải «coi như `dmy`»)* và của `6.843` ô `Input here`.
    """
    m = _m()
    trong = [b for b, _, asis, _ in m.TU_DIEN_THUC_THE if not str(asis).strip()]
    assert not trong, (
        f"⛔ ô `Tên ở AS-IS` để TRỐNG: {trong} — nếu AS-IS ⛔ không có thì "
        f"khai thẳng hằng `FLS_DUNG_MOI`")


def test_fls_itl_khai_DU_ba_truc_owner_hoi():
    """⭐⭐⭐ Ghim đúng câu hỏi của owner `17/09`, ⛔ không hỏi chung chung.

    Ba trục: **khái niệm** *(giao dịch)* · **tên tab ggsheet** *(`ITL Ledge`)*
    · **tên tệp excel** *(`File 1_2` / `File 2_2`)*.

    ⛔ Một bài chỉ hỏi *«`fls_itl` có trong từ điển ⛔ không»* là **XANH GIẢ**:
      nó vẫn xanh khi ai đó bóp ô `Tên ở AS-IS` về một chuỗi rỗng-nghĩa.
    """
    m = _m()
    tra = {b: (kn, asis) for b, kn, asis, _ in m.TU_DIEN_THUC_THE}
    kn, asis = tra["fls_itl"]
    assert "giao dịch" in kn, f"⛔ khái niệm của `fls_itl` phải là *giao dịch* — đang là {kn!r}"
    assert "ITL Ledge" in asis, f"⛔ thiếu tên TAB ggsheet `ITL Ledge` — đang là {asis!r}"
    assert "File 1_2" in asis or "Transaction Mapping L1" in asis, (
        f"⛔ thiếu tên TỆP excel / tab `Transaction Mapping L1` — đang là {asis!r}")


def test_ten_bang_KHONG_be_loi_chinh_ta_cua_nguon_vao_kho():
    """⛔⛔ Tab thật tên `ITL Ledge` — **thiếu chữ `r`**. `R-A2` buộc chép
    nguyên văn lỗi ấy **trong tài liệu**; bê nó vào **tên bảng** thì lỗi sống
    mãi trong mọi câu `SQL`, và ⛔ không ai dám sửa nữa.

    ⇒ Bài này ghim một việc **KHÔNG LÀM**: ⛔ không có bảng nào tên `*ledge*`.
    """
    xau = sorted(b for b in _bang_trong_kho() if "ledge" in b.lower())
    assert not xau, f"⛔ tên bảng bê lỗi chính tả của nguồn: {xau}"


def test_bang_tu_dien_thuc_the_CO_MAT_trong_BA05():
    """⛔ Một bản khai ⛔ không ai đọc được là một bản khai vô hình."""
    vb = BA05.read_text(encoding="utf-8")
    for mau in ("| Bảng trong kho | Khái niệm nghiệp vụ | Tên ở AS-IS |",
                "| `fls_itl` | giao dịch |"):
        assert mau in vb, (
            f"⛔ `BA-05` thiếu {mau!r} — chạy "
            "`python tools/sinh_ban_do_tang.py`")
