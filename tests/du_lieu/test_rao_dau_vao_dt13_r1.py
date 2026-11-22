"""Vòng sửa sau R1 `KQ-321` — RÀO ĐẦU VÀO cho `sign_off_dau_vao` *(DT13-R1-01)* và `ccr_daily_report_2` *(DT13-R1-02)*.

⭐ Đ4 — mỗi số đếm MỘT vật:
  * `sign_off_dau_vao` trùng **13.541/13.541** ô SỐ cột số liệu `cot[7:]` với đáp án 605 *(cùng `checksum_noi_dung`; KQ-321 ghi 14.036 — đếm khác vật, ⛔ tái lập offline)* ⇒ hợp lệ CHỈ cho 608 *(vòng tròn 605)*.
  * `ccr_daily_report_2` ↔ đáp án `daily_report_2` *(PD 610)*: **25.185/26.272 = 95,9 %** ô SỐ trùng ⇒ hợp lệ CHỈ cho 615.
  * Với 615: **23.746/48.021 = 49,4 %** ô là THAM CHIẾU TRỰC TIẾP `='5. Daily Report 2'!…` *(KQ-321, đọc `FORMULA` bằng SA
    22/11 — ⛔ đo lại được offline)* ⇒ "khớp" ở đó là CHÉP giá trị dán, ⛔ chứng minh tính toán.
⭐ Đ5 — cổng khai `mong` rồi bị PHÁ cho đỏ: xem các bài `test_PHA_*`.
"""
from __future__ import annotations

import json
import pathlib

import pytest

from tools.khuon_dong_bang import _rao_dau_vao as R
from tools.khuon_dong_bang import ccr_daily_report_2 as K615
from tools.khuon_dong_bang import sign_off_dau_vao as K608

GOC = pathlib.Path(__file__).resolve().parents[2]
DV = GOC / "tests" / "fixture" / "dau_vao"
DA = GOC / "tests" / "fixture" / "dap_an"


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


# ── khai trong khuôn ────────────────────────────────────────────────────────────────────────────
def test_khuon_khai_DAU_VAO_CHO_va_CAM_CHO():
    assert (K608.DAU_VAO_CHO, K608.CAM_CHO) == (frozenset({"608"}), frozenset({"605"}))
    assert (K615.DAU_VAO_CHO, K615.CAM_CHO) == (frozenset({"615"}), frozenset({"610"}))


def test_bang_khai_gom_dung_hai_anh_Đ5():
    """Mong: ĐÚNG 2 ảnh khai rào *(thêm ảnh có rào ⇒ sửa số Ở ĐÂY)*; tập rỗng ⇒ ĐỎ *(Đ3)*."""
    assert sorted(R.RAO) == ["ccr_daily_report_2", "sign_off_dau_vao"]


# ── hàm kiểm có tên ─────────────────────────────────────────────────────────────────────────────
def test_605_doc_sign_off_dau_vao_NEM_LOI_CO_TEN():
    with pytest.raises(R.DauVaoSaiChoError, match="sign_off_dau_vao.*605"):
        R.kiem_dau_vao_hop_le("sign_off_dau_vao", "605")
    with pytest.raises(R.DauVaoSaiChoError):
        R.kiem_dau_vao_hop_le(_doc(DV / "sign_off_dau_vao.json"), "PD 605")  # nhận cả dict ảnh + nhãn "PD 605"


def test_608_doc_sign_off_dau_vao_HOP_LE():
    R.kiem_dau_vao_hop_le("sign_off_dau_vao", "608")
    R.kiem_dau_vao_hop_le("sign_off_dau_vao", 608)


def test_610_doc_ccr_daily_report_2_NEM_LOI_va_615_HOP_LE():
    with pytest.raises(R.DauVaoSaiChoError, match="ccr_daily_report_2.*610"):
        R.kiem_dau_vao_hop_le("ccr_daily_report_2", "610")
    R.kiem_dau_vao_hop_le("ccr_daily_report_2", "615")


def test_dap_an_la_PD_khac_ngoai_DAU_VAO_CHO_cung_ĐỎ():
    """Không chỉ cấm tên: PD ngoài `DAU_VAO_CHO` *(vd. 609)* cũng ĐỎ — whitelist, ⛔ blacklist."""
    with pytest.raises(R.DauVaoSaiChoError):
        R.kiem_dau_vao_hop_le("sign_off_dau_vao", "609")
    with pytest.raises(R.DauVaoSaiChoError):
        R.kiem_dau_vao_hop_le("ccr_daily_report_2", "608")


def test_anh_khong_khai_rao_khong_bi_chan():
    R.kiem_dau_vao_hop_le("mid3_total", "615")


# ── số đo ghim (Đ4: nhãn mẫu số) ────────────────────────────────────────────────────────────────
def test_605_vong_tron_sign_off_trung_13541_o_voi_dap_an():
    a, b = _doc(DV / "sign_off_dau_vao.json"), _doc(DA / "daily_report_3.json")
    assert a["checksum_noi_dung"] == b["checksum_noi_dung"]
    n, ok = R.dem_o_so_trung(a, b, cot=a["cot"][7:])
    assert n > 0 and (n, ok) == (13541, 13541)  # Đ3: mẫu số TRƯỚC


def test_610_ccr_dr2_trung_95_9_phan_tram_voi_dap_an_610():
    a, b = _doc(DV / "ccr_daily_report_2.json"), _doc(DA / "daily_report_2.json")
    n, ok = R.dem_o_so_trung(a, b, cot=a["cot"][7:])
    assert n > 0 and (n, ok) == (26272, 25185)
    assert round(100 * ok / n, 1) == 95.9


def test_615_tach_dem_chep_vs_tinh_Đ4():
    """Khai trong khuôn: 23.746 ô tham chiếu trực tiếp *(CHÉP)* / 48.021 ô công thức; phần còn lại = 24.275 *(có phép tính)*."""
    chep, tong = K615.O_THAM_CHIEU_TRUC_TIEP_615, K615.O_CONG_THUC_615
    assert (chep, tong) == (23746, 48021)
    assert round(100 * chep / tong, 1) == 49.4 and tong - chep == 24275


# ── quét mã: ⛔ đường dựng 605/610 đọc ảnh cấm ──────────────────────────────────────────────────
def test_quet_ma_thuc_khong_co_tham_chieu_ngoai_khuon_va_rao():
    """Hôm nay MỌI tham chiếu `sign_off_dau_vao`/`ccr_daily_report_2` ngoài khuôn+rào+bài = 0 *(mong 0; engine H14 thêm ⇒ sửa ở đây
    VÀ phải gọi `kiem_dau_vao_hop_le`)*."""
    assert R.quet_tham_chieu(GOC, "sign_off_dau_vao") == []
    assert R.quet_tham_chieu(GOC, "ccr_daily_report_2") == []


@pytest.mark.parametrize("ten,cam", [("sign_off_dau_vao", "605"), ("ccr_daily_report_2", "610")])
def test_PHA_nhet_tham_chieu_vao_engine_cam_thi_quet_DO(tmp_path, ten, cam):
    """⭐ Đ5 — cổng cấm CHỨNG MINH ĐỎ: dựng cây giả có engine đọc ảnh mà ⛔ gọi hàm kiểm ⇒ phải bị bắt."""
    (tmp_path / "fls").mkdir()
    (tmp_path / "tools").mkdir()
    (tmp_path / "fls" / f"engine_{cam}.py").write_text(
        f'ANH = "tests/fixture/dau_vao/{ten}.json"\nTINH = "dung o {cam}"\n', encoding="utf-8")
    bat = R.quet_tham_chieu(tmp_path, ten)
    assert [p.name for p in bat] == [f"engine_{cam}.py"]


def test_engine_co_goi_ham_kiem_van_bi_liet_ke_de_nguoi_duyet_nhung_khong_bi_cam_im(tmp_path):
    """Engine 608 đọc `sign_off_dau_vao` + GỌI `kiem_dau_vao_hop_le` ⇒ KHÔNG bị bắt; thiếu lời gọi ⇒ bị bắt."""
    (tmp_path / "fls").mkdir()
    (tmp_path / "fls" / "e608.py").write_text(
        'ANH="sign_off_dau_vao"\nkiem_dau_vao_hop_le(ANH, "608")\n', encoding="utf-8")
    assert R.quet_tham_chieu(tmp_path, "sign_off_dau_vao") == []
    (tmp_path / "fls" / "e605.py").write_text('ANH="sign_off_dau_vao"\n', encoding="utf-8")
    assert [p.name for p in R.quet_tham_chieu(tmp_path, "sign_off_dau_vao")] == ["e605.py"]


def test_PHA_dem_o_so_trung_doi_mot_o_thi_DO():
    a, b = _doc(DV / "ccr_daily_report_2.json"), _doc(DA / "daily_report_2.json")
    a["dong"][0]["h"] = str(float(a["dong"][0]["h"]) + 1e9)
    n, ok = R.dem_o_so_trung(a, b, cot=a["cot"][7:])
    assert (n, ok) == (26272, 25184)


def test_docstring_khong_vien_dan_bai_ma():
    """DT13-R1-01: docstring từng viện dẫn `test_AC4_engine_khong_doc_dap_an` — tên bài ⛔ tồn tại."""
    src = (GOC / "tools" / "khuon_dong_bang" / "sign_off_dau_vao.py").read_text(encoding="utf-8")
    assert "test_AC4_engine_khong_doc_dap_an" not in src
    ten_bai = {"test_605_doc_sign_off_dau_vao_NEM_LOI_CO_TEN", "test_quet_ma_thuc_khong_co_tham_chieu_ngoai_khuon_va_rao"}
    assert all(t in src for t in ten_bai)
    me = pathlib.Path(__file__).read_text(encoding="utf-8")
    assert all(f"def {t}(" in me for t in ten_bai)  # bài viện dẫn TỒN TẠI
