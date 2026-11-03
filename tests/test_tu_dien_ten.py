"""TỪ ĐIỂN TÊN — một khâu đang mang **ba bộ tên**, và ⛔ không chỗ nào nói
chúng là MỘT *(`T3` của cuộc audit, owner chốt 2026-09-17)*.

⛔⛔ **Cái thiếu ⛔ KHÔNG phải *"tài liệu chưa đọc tên tệp AS-IS"*** — nó **có**
đọc *(`BA-05:39` + `:130`, và `pm_join.py:192`)*. Cái thiếu là **CÂU NỐI**:
⛔ không một dòng nào nói `File 1_2` **là** cái mà `09_MILESTONES` gọi là
*«mốc `A`»*. Thiếu câu nối thì mỗi người tự nối lấy, mỗi người một kiểu — và
đó là chỗ drift sinh ra.

⭐ **Tên CHUẨN là tên TÁC VỤ** *(owner chốt)*; hai bộ kia là **bí danh**.
⇒ ⛔ **Không đổi tên tệp** `09_MILESTONES_HAI_TAC_VU.md` — nó đang **đúng**.
*(Phép đo cũ của tôi đòi tên ấy biến mất; nó **đo sai thứ**.)*
"""
from __future__ import annotations

import importlib.util
import pathlib

import pytest

GOC = pathlib.Path(__file__).resolve().parents[1]
BA05 = GOC / "docs" / "ITL" / "02_BA" / "05_DATA_DICTIONARY_ERD.md"


def _m():
    sp = importlib.util.spec_from_file_location(
        "_sbd", GOC / "tools" / "sinh_ban_do_tang.py")
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m


def _chuoi(m) -> set[str]:
    return {k for k, _, loai, _ in m.KHAU if loai == "chuoi"}


def test_MOI_khau_chuoi_co_ten_o_CA_BA_xuat_xu():
    """⭐⭐ Thiếu một xuất xứ = một bộ tên ⛔ không nói được về khâu nào."""
    m = _m()
    chuoi = _chuoi(m)
    for xx in m.XUAT_XU_BAT_BUOC:
        phu = {k for _, x, ks, _ in m.TU_DIEN_TEN if x == xx for k in ks}
        assert chuoi <= phu, (
            f"⛔ xuất xứ {xx!r} ⛔ không phủ khâu {sorted(chuoi - phu)} — "
            "một khâu ⛔ không có tên ở một bộ là một chỗ người đọc phải "
            "TỰ NỐI, và đó là chỗ drift sinh ra")


def test_MOI_khau_trong_tu_dien_deu_LA_khau_CO_THAT():
    """⛔ Một bí danh trỏ vào một khâu ⛔ không tồn tại là một sợi dây đứt."""
    m = _m()
    hop_le = {k for k, _, _, _ in m.KHAU}
    for ten, _xx, ks, _ in m.TU_DIEN_TEN:
        la = sorted(set(ks) - hop_le)
        assert not la, f"⛔ {ten!r} trỏ tới khâu ⛔ KHÔNG có: {la}"


def test_ten_CHUAN_la_ten_TAC_VU_va_phu_DU_ba_khau():
    """⭐ Owner chốt 17/09. Ba tên chuẩn: mốc `A` · tác vụ ① · tác vụ ②."""
    m = _m()
    chuan = {k for ten, xx, ks, _ in m.TU_DIEN_TEN
             if "CHUẨN" in xx for k in ks}
    assert chuan == _chuoi(m), f"⛔ tên chuẩn ⛔ không phủ đủ ba khâu: {chuan}"


def test_ITL_1_tren_2_trai_DUNG_HAI_khau_A_va_B():
    """⚠ «ITL (1/2)» là một **TỆP**, ⛔ không phải một bước — trong nó có cả
    `Transaction Original` *(Ⓐ)* lẫn `Transaction Mapping L1` *(Ⓑ)*.

    ⛔ Làm tròn chuyện ấy thành *"một tên ↔ một khâu"* là **bóp méo nguồn**,
    và chính nó là lý do owner trả lời `Q1` rằng «ITL (1/2)» là một **BƯỚC**.

    ⛔⛔ **Bản đầu của bài này chỉ hỏi *"có tên nào trỏ >1 khâu ⛔ không"* — và
    nó **XANH GIẢ**: dòng `mã nguồn` liệt kê cả ba khâu nên câu hỏi ấy luôn
    được thoả, kể cả khi ai đó đã bóp «ITL (1/2)» về một khâu. Phép chứng
    minh ĐỎ đã lộ ra điều đó sau **ba** lần thử phá.
    ⇒ Nay nó ghim **đúng cặp khâu của đúng cái tên**, ⛔ không hỏi một câu
      chung chung mà một dòng khác trả lời hộ.
    """
    m = _m()
    tra = {t: set(ks) for t, _, ks, _ in m.TU_DIEN_TEN}
    assert tra.get("ITL (1/2)") == {"A-nap", "B-ghep"}, (
        "⛔ «ITL (1/2)» phải trỏ ĐÚNG hai khâu `A-nap` + `B-ghep` — "
        f"đang là {sorted(tra.get('ITL (1/2)', []))}")


def test_tep_09_MILESTONES_VAN_mang_ten_cu__no_DANG_DUNG():
    """⛔⛔ GHIM MỘT VIỆC **KHÔNG LÀM**.

    Phép đo cũ của tôi đòi `HAI_TAC_VU` biến khỏi tên tệp. Owner chốt tên
    CHUẨN là **tên tác vụ** ⇒ tên tệp ấy **đang đúng**, và đổi nó là **đổi
    một danh tính đã đi vào ~10 tệp + sổ commit** để chiều một phép đo sai.
    """
    assert (GOC / "docs" / "ITL" / "01_Orchestrator"
            / "09_MILESTONES_HAI_TAC_VU.md").exists(), (
        "⛔ tệp bị đổi tên — xem `QĐ` 17/09: tên tác vụ LÀ tên chuẩn")


@pytest.mark.parametrize("mau", [
    "| Tên đang lưu hành | Xuất xứ | Khâu |",
    "ITL (1/2)",
])
def test_bang_tu_dien_CO_MAT_trong_BA05(mau):
    """⛔ Một bản khai ⛔ không ai đọc được là một bản khai vô hình."""
    assert mau in BA05.read_text(encoding="utf-8"), (
        f"⛔ ⛔ `BA-05` thiếu {mau!r} — chạy `python tools/sinh_ban_do_tang.py`")
