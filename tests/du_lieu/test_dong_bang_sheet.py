"""`tools/dong_bang_sheet.py` — đường ống ĐÓNG BĂNG sheet → ảnh có checksum + cổng *(ISP 3.1.2 · DT2)*.

⭐ **Vì sao có tệp này.** Bảng tỷ giá `9.2.Exchange Rate` *(APERO | FS2, nhập tay)* là nguồn
của `IX.FX`, và AP v3.1.2 §3.2.4 ghi hậu quả đã thấy ở NOW: *"tháng thiếu ⇒ SUMIFS = 0 ⇒ mất
số không báo; tháng nhập hai dòng ⇒ cộng đôi"*. Bước sau *(C1 kiểm · C5 nạp kho)* cần một ẢNH
đứng yên của bảng ấy — đọc MỘT lần từ Drive *(orchestrator, O7)*, đóng băng thành tệp có
`checksum_noi_dung`, và một cổng in ra tháng **thiếu / trùng / lạc** thay vì im lặng.

Ba bài của ISP *(mục 6)* + các đối chứng Đ5:

    DT2-B1  đóng băng từ bản thô  ⇒ 37 dòng · checksum ổn định qua 2 lần chạy (tất định)
    DT2-B2  bản thô có cột `Email Address` ⇒ ĐỎ, ⛔ ghi tệp (`PM_COT_RIENG_TU`)
    DT2-B3  bản thô thiếu 1 tháng ⇒ ảnh vẫn ghi ĐÚNG NGUỒN + cổng in `thiếu: [yyyymm]`, exit ≠ 0

⛔⛔ **Bản đọc thô thật ⛔ nằm trong repo** *(scratchpad orchestrator, ⛔ commit — ISP mục 5)*.
⇒ Bài ở đây tự dựng bản thô **TỔNG HỢP** cùng hình dạng *(37 dòng, dòng lạc `202306` giữa
`202512` và `202601` — đúng chỗ nó nằm ở sheet)*; còn ẢNH đã commit thì được kiểm bằng cách
**tái tạo bản thô từ chính ảnh** rồi chạy lại công cụ ⇒ phải ra **đúng từng byte** tệp đã commit.

⭐ **Số giữ CHÍNH XÁC.** Sheets hiển thị SGD 202507 là `20,692` mà giá trị là **`20691.51`**
*(orchestrator đo — vì thế bản thô đọc bằng `effectiveValue`)*. Công cụ ⛔ được đi qua `float`:
bài B1 cài một ô **20 chữ số có nghĩa** — `float` làm tròn nó, `Decimal` thì giữ nguyên.

⭐ **Checksum ghim (`CHECKSUM_ANH_IX_FX`) được KHAI TRƯỚC khi có công cụ** — tính độc lập bằng
`AnhChup` trên bản thô thật *(dòng = `thu_tu` + 6 cột, mọi ô là chuỗi đúng chữ số)*. Công cụ phải
ra đúng số ấy; sửa một ô của ảnh là ĐỎ *(Đ5)*.

⛔ Bài ở đây ⛔ nối kho, ⛔ đọc mạng: công cụ là hàm thuần trên tệp.
"""
from __future__ import annotations

import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import date

import pytest

from fls.adapters.pm_join import PM_COT_RIENG_TU
from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
ANH_IX_FX = GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json"

#: Khai TRƯỚC khi có công cụ *(xem docstring)*. Đổi ⇒ phải có lượt đóng băng mới + lý do.
CHECKSUM_ANH_IX_FX = "b6d1f9e9074951f1"

KHOA = "Month"
TIEN_TE = ("USD", "SGD", "COP", "VND", "HKD")

#: Một ô 20 chữ số có nghĩa: `float` chỉ giữ ~17 ⇒ `repr(float(x))` = `19744.785`.
O_DAI = "19744.785000000000001"


# ── dựng bản thô TỔNG HỢP ─────────────────────────────────────────────────────

def _thang(nam: int, tu: int, den: int) -> list[int]:
    return [nam * 100 + m for m in range(tu, den + 1)]


#: Thứ tự hàng như sheet thật: 202401…202512, rồi dòng lạc 202306, rồi 202601…202612.
THU_TU_SHEET = _thang(2024, 1, 12) + _thang(2025, 1, 12) + [202306] + _thang(2026, 1, 12)


def _so_tho(v: str) -> str:
    """Chuỗi số → literal số JSON *(⛔ nháy kép)*: giữ nguyên chữ số, ⛔ qua `float`."""
    assert re.fullmatch(r"-?\d+(\.\d+)?", v), v
    return v


def _viet_ban_tho(p: pathlib.Path, cot: list[str], hang: list[list[str]],
                  nguon: str = "TỔNG HỢP · bài thử DT2 (⛔ số thật)",
                  doc_luc: str = "2026-03-09",
                  cach_doc: str = "tổng hợp trong bài thử") -> pathlib.Path:
    """Ghi bản thô đúng khuôn orchestrator đưa: `{nguon, doc_luc, cach_doc, cot, dong}`.

    ⚠ Viết TAY phần `dong` để ô số ra **literal số** JSON giữ đủ chữ số *(`json.dumps` của
    `float` sẽ làm tròn `O_DAI`)*. Ô ⛔ phải số *(email giả ở B2)* thì `json.dumps` như chuỗi.
    """
    def o(v: str | None) -> str:
        if v is None:
            return "null"
        return _so_tho(v) if re.fullmatch(r"-?\d+(\.\d+)?", v) else json.dumps(v)

    dong = ",\n  ".join("[" + ", ".join(o(v) for v in h) + "]" for h in hang)
    p.write_text(
        "{\n"
        f' "nguon": {json.dumps(nguon, ensure_ascii=False)},\n'
        f' "doc_luc": {json.dumps(doc_luc)},\n'
        f' "cach_doc": {json.dumps(cach_doc, ensure_ascii=False)},\n'
        f' "cot": {json.dumps(cot, ensure_ascii=False)},\n'
        f' "dong": [\n  {dong}\n ]\n'
        "}\n", encoding="utf-8")
    return p


def _hang_tong_hop(thang: list[int]) -> list[list[str]]:
    """Mỗi tháng một hàng `[Month, USD, SGD, COP, VND, HKD]` — số TỔNG HỢP, ⛔ số thật."""
    ra = []
    for i, t in enumerate(thang):
        ra.append([str(t), str(25000 + i), f"{19000 + i}.51", "6.27", "1", "3300.125"])
    return ra


@pytest.fixture
def ban_tho_37(tmp_path: pathlib.Path) -> pathlib.Path:
    hang = _hang_tong_hop(THU_TU_SHEET)
    hang[0][2] = O_DAI                       # ô 20 chữ số có nghĩa ở SGD 202401
    return _viet_ban_tho(tmp_path / "tho_37.json", [KHOA, *TIEN_TE], hang)


def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=60)


def _da_tu_choi(kq: subprocess.CompletedProcess) -> None:
    """exit 2 **của CÔNG CỤ** — ⛔ exit 2 nào cũng được.

    ⛔⛔ Đo khi chạy đỏ: Python thoát **2** với *"can't open file"* khi `tools/dong_bang_sheet.py`
    CHƯA CÓ ⇒ bài chỉ đòi `returncode == 2` sẽ XANH SẴN trên công cụ vắng mặt. ⇒ đòi thêm dòng
    từ chối một dòng của chính công cụ *(`S0-R1-04`: nguyên nhân đọc được trong MỘT dòng)*.
    """
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-800:], kq.stderr[-800:])
    dong = [d for d in kq.stderr.splitlines() if d.startswith("⛔ TỪ CHỐI")]
    assert len(dong) == 1, ("cần đúng MỘT dòng `⛔ TỪ CHỐI …`", kq.stderr[-800:])


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _checksum_lai(anh: dict) -> str:
    """Tính lại bằng CHÍNH `AnhChup` — ảnh phải dùng nó, ⛔ một phép băm riêng."""
    return AnhChup(run_id="kiem", ngay=date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"])).checksum()[:16]


# ── DT2-B1 · tất định ─────────────────────────────────────────────────────────

def test_DT2_B1_dong_bang_37_dong_va_checksum_on_dinh_qua_hai_lan_chay(ban_tho_37, tmp_path):
    """Hai lần chạy trên cùng bản thô ⇒ cùng checksum VÀ cùng từng byte.

    ⭐ `ngay_dong_bang` lấy từ `doc_luc` của bản thô *(ảnh là của MỘT ngày đọc)*, ⛔ đồng hồ
    máy ⇒ tệp tái tạo được nguyên văn: chạy lại công cụ rồi `git diff` phải rỗng.
    """
    a, b = tmp_path / "a.json", tmp_path / "b.json"
    for ra in (a, b):
        kq = _chay("ix_fx", str(ban_tho_37), "--mong", "37", "--ra", str(ra))
        assert kq.returncode == 0, (kq.returncode, kq.stdout[-1500:], kq.stderr[-1500:])
    assert a.read_bytes() == b.read_bytes(), "hai lần chạy ra hai tệp khác nhau ⇒ ⛔ tất định"

    anh = _doc(a)
    assert anh["so_dong"] == len(anh["dong"]) == 37
    assert re.fullmatch(r"[0-9a-f]{16}", anh["checksum_noi_dung"]), anh["checksum_noi_dung"]
    assert anh["checksum_noi_dung"] == _checksum_lai(anh)
    # ⚠ `doc_luc` của bản thô tổng hợp cố ý KHÁC ngày chạy: bản đầu đặt `2026-11-16` — trùng
    #   hôm viết bài — nên một công cụ lấy ĐỒNG HỒ MÁY vẫn xanh hôm ấy. Phá thử M7 (BG-086).
    assert anh["ngay_dong_bang"] == "2026-03-09"
    for k in ("nguon", "ngay_dong_bang", "khong_mang_PII", "checksum_noi_dung"):
        assert anh.get(k), f"thiếu trường `{k}` của khuôn ảnh (`pm_join.json`)"

    # ghi ĐÚNG NGUỒN: thứ tự hàng của sheet, kể cả dòng lạc
    assert [d[KHOA] for d in anh["dong"]] == [str(t) for t in THU_TU_SHEET]
    assert [d["thu_tu"] for d in anh["dong"]] == list(range(1, 38))
    assert (anh["thieu"], anh["trung"], anh["lac"]) == ([], [], ["202306"])
    assert "lạc: [202306]" in kq.stdout

    # số giữ CHÍNH XÁC — ⛔ float
    assert anh["dong"][0]["SGD"] == O_DAI
    assert anh["dong"][0]["COP"] == "6.27" and anh["dong"][0]["VND"] == "1"


def test_DT2_B1_checksum_DOI_khi_mot_o_hoac_thu_tu_doi(ban_tho_37, tmp_path):
    """Đ5: checksum ổn định chỉ có nghĩa khi nó **ĐỔI** lúc nội dung đổi.

    ⭐ `AnhChup.checksum()` cố ý ĐỘC LẬP thứ tự đọc *(đọc dần/cắt lát)*. Nhưng ở đây thứ tự
    hàng của sheet LÀ dữ liệu *(dòng lạc 202306 chỉ "lạc" vì nó đứng sau 202512)* ⇒ mỗi dòng
    mang `thu_tu`, nên đổi chỗ hai hàng cũng đổi checksum.
    """
    goc_ra = tmp_path / "goc.json"
    assert _chay("ix_fx", str(ban_tho_37), "--mong", "37", "--ra", str(goc_ra)).returncode == 0
    goc = _doc(goc_ra)["checksum_noi_dung"]

    hang = _hang_tong_hop(THU_TU_SHEET)
    hang[0][2] = O_DAI
    mot_o = [list(h) for h in hang]
    mot_o[18][2] = "20691.52"                        # một xu ở SGD 202507
    doi_cho = [list(h) for h in hang]
    doi_cho[0], doi_cho[1] = doi_cho[1], doi_cho[0]  # 202402 lên trước 202401
    for ten, h in (("mot_o", mot_o), ("doi_cho", doi_cho)):
        tho = _viet_ban_tho(tmp_path / f"tho_{ten}.json", [KHOA, *TIEN_TE], h)
        ra = tmp_path / f"{ten}.json"
        _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
        assert ra.exists(), ten
        assert _doc(ra)["checksum_noi_dung"] != goc, f"{ten}: checksum ⛔ đổi ⇒ cổng mù"


def test_DT2_B1_anh_IX_FX_da_commit_dung_37_dong_202401_202612_va_dong_lac_202306():
    """⭐ Ảnh thật của `9.2.Exchange Rate` — đúng như AP v3.1.2 §3.2.1 đo: *37 dòng 202401 →
    202612 (kể cả dòng lạc 202306)*. Mỗi con số dưới đây đếm một vật *(Đ4)*.
    """
    anh = _doc(ANH_IX_FX)
    assert anh["bang"] == "IX.FX" and anh["khoa"] == KHOA and anh["cot"] == list(TIEN_TE)
    dong = anh["dong"]
    assert anh["so_dong"] == len(dong) == 37                     # dòng của ảnh

    thang = [d[KHOA] for d in dong]
    du_dai = {str(t) for t in _thang(2024, 1, 12) + _thang(2025, 1, 12) + _thang(2026, 1, 12)}
    assert len(du_dai) == 36                                     # tháng 202401→202612
    assert set(thang) == du_dai | {"202306"} and len(set(thang)) == 37
    assert (anh["thieu"], anh["trung"], anh["lac"]) == ([], [], ["202306"])

    # dòng lạc nằm ĐÚNG chỗ của sheet: giữa 202512 và 202601
    i = thang.index("202306")
    assert (thang[i - 1], thang[i + 1]) == ("202512", "202601")

    # giá trị, ⛔ chuỗi hiển thị: SGD 202507 hiển thị `20,692`
    assert next(d for d in dong if d[KHOA] == "202507")["SGD"] == "20691.51"

    # đủ 5 tiền tệ ở mọi dòng — ô rỗng = 0 trên mẫu số 37 × 5 = 185
    o = [d[c] for d in dong for c in TIEN_TE]
    assert len(o) == 185 and all(v not in (None, "") for v in o)

    assert anh["ngay_dong_bang"] == "2026-11-16"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_ANH_IX_FX


def _ban_tho_tu_anh(anh: dict, p: pathlib.Path) -> pathlib.Path:
    """Tái tạo bản thô từ ẢNH: `cot` = khoá + cột chọn; `dong` theo `thu_tu`."""
    dong = sorted(anh["dong"], key=lambda d: d["thu_tu"])
    cot = [anh["khoa"], *anh["cot"]]
    return _viet_ban_tho(p, cot, [[d[c] for c in cot] for d in dong],
                         nguon=anh["nguon"], doc_luc=anh["ngay_dong_bang"],
                         cach_doc=anh["cach_doc"])


def test_DT2_B1_anh_IX_FX_TAI_TAO_dung_tung_byte_tu_cong_cu(tmp_path):
    """Bản thô thật ⛔ commit ⇒ chứng minh ảnh đã commit LÀ đầu ra của công cụ bằng cách tái
    tạo bản thô từ ảnh rồi chạy lại: phải ra **đúng từng byte**. Ai sửa tay ảnh *(hay sửa công
    cụ đổi hình dạng tệp)* mà ⛔ đóng băng lại là ĐỎ.
    """
    anh = _doc(ANH_IX_FX)
    tho = _ban_tho_tu_anh(anh, tmp_path / "tho_tu_anh.json")
    ra = tmp_path / "ix_fx.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert ra.read_bytes() == ANH_IX_FX.read_bytes()


def _chuan(ten: str) -> str:
    return " ".join(str(ten).split()).casefold()


def test_DT2_B1_anh_IX_FX_khong_mang_khoa_PII_quet_bang_0():
    """Mục 8: *"ảnh ⛔ mang khoá PII (quét = 0)"* — quét MỌI khoá *(đỉnh + từng dòng + tên cột
    khai)*; Đ3: mẫu số phải > 0, ⛔ xanh trên tập rỗng.
    """
    anh = _doc(ANH_IX_FX)
    khoa = list(anh) + [anh["khoa"], *anh["cot"]] + [k for d in anh["dong"] for k in d]
    cam = {_chuan(c) for c in PM_COT_RIENG_TU}
    assert len(cam) >= 1 and len(khoa) > 37 * 7                  # mẫu số: ≥ 259 khoá dòng
    assert [k for k in khoa if _chuan(k) in cam] == []


# ── DT2-B2 · riêng tư ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("ten_cot", [
    pytest.param("Email Address", id="nguyen_van"),
    pytest.param("  Email   Address ", id="khoang_trang"),
    pytest.param("email address", id="chu_thuong"),
])
def test_DT2_B2_ban_tho_co_cot_Email_Address_thi_DO_va_KHONG_ghi_tep(tmp_path, ten_cot):
    """⛔ `PM_COT_RIENG_TU` — cột ấy ⛔ bao giờ vào kho, nên cũng ⛔ vào ảnh *(ảnh là cửa vào kho
    của C5)*. Có trong bản thô là TỪ CHỐI cả lượt, kể cả khi khuôn ⛔ chọn cột ấy.

    ⭐ Khớp tên sau khi gộp khoảng trắng *(như `pm_join.loc_tho`)* và ⛔ phân biệt hoa thường —
    một cổng từ chối chặt hơn nguồn khai là an toàn; lỏng hơn là lọt.
    """
    hang = [h + [f"nguoi.lap.{i}@vi-du.invalid"] for i, h in
            enumerate(_hang_tong_hop(THU_TU_SHEET))]
    tho = _viet_ban_tho(tmp_path / "tho_pii.json", [KHOA, *TIEN_TE, ten_cot], hang)

    moi = tmp_path / "moi" / "ix_fx.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(moi))
    _da_tu_choi(kq)
    assert not moi.exists() and not moi.parent.exists(), "⛔ được tạo tệp/thư mục khi từ chối"
    assert "PM_COT_RIENG_TU" in kq.stderr
    assert "vi-du.invalid" not in kq.stdout + kq.stderr, "⛔ in GIÁ TRỊ của cột riêng tư"

    # tệp có sẵn ⛔ bị đụng
    cu = tmp_path / "cu.json"
    cu.write_bytes(b'{"giu": "nguyen"}\n')
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(cu))
    _da_tu_choi(kq)
    assert cu.read_bytes() == b'{"giu": "nguyen"}\n'


# ── DT2-B3 · cổng ─────────────────────────────────────────────────────────────

def test_DT2_B3_ban_tho_thieu_mot_thang_ghi_DUNG_NGUON_va_cong_DO(tmp_path):
    """Thiếu 202408 ⇒ ảnh ghi 36 dòng như nguồn *(⛔ điền, ⛔ nội suy)* + cổng in
    `thiếu: [202408]` và exit ≠ 0 vì `--mong 37` lệch.
    """
    thang = [t for t in THU_TU_SHEET if t != 202408]
    tho = _viet_ban_tho(tmp_path / "tho_36.json", [KHOA, *TIEN_TE], _hang_tong_hop(thang))
    ra = tmp_path / "ix_fx.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))

    assert kq.returncode == 1, (kq.returncode, kq.stdout[-1500:], kq.stderr[-1500:])
    assert "thiếu: [202408]" in kq.stdout
    assert "36 dòng ≠ mong 37" in kq.stdout
    anh = _doc(ra)
    assert [d[KHOA] for d in anh["dong"]] == [str(t) for t in thang]
    assert anh["so_dong"] == 36 and anh["thieu"] == ["202408"]
    assert anh["cong"] == {"mong": 37, "so_dong": 36, "dat": False,
                           "ly_do": anh["cong"]["ly_do"]} and anh["cong"]["ly_do"]


@pytest.mark.parametrize("mong, exit_mong", [("36", 1), ("37", 0), ("38", 1)])
def test_DT2_B3_cong_mong_DO_ca_hai_chieu(ban_tho_37, tmp_path, mong, exit_mong):
    """Đ5: `--mong` khác số dòng ⇒ ĐỎ **cả khi thừa lẫn khi thiếu**; đúng ⇒ đạt."""
    kq = _chay("ix_fx", str(ban_tho_37), "--mong", mong, "--ra", str(tmp_path / "a.json"))
    assert kq.returncode == exit_mong, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert ("[ĐẠT]" if exit_mong == 0 else "[ĐỎ]") in kq.stdout


def test_DT2_B3_thang_TRUNG_bu_cho_thang_THIEU_van_DO(tmp_path):
    """37 dòng mà 202409 bị nhập thành 202408 lần hai ⇒ đếm dòng VẪN khớp `--mong 37`.

    ⛔ Cổng chỉ đếm dòng sẽ XANH ở đây — đúng ca AP §3.2.4 *"tháng nhập hai dòng ⇒ cộng đôi"*.
    ⇒ khoá `yyyymm` phải duy nhất và liền tháng: trùng/thiếu đều đỏ.
    """
    thang = [202408 if t == 202409 else t for t in THU_TU_SHEET]
    tho = _viet_ban_tho(tmp_path / "tho_trung.json", [KHOA, *TIEN_TE], _hang_tong_hop(thang))
    ra = tmp_path / "ix_fx.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert "trùng: [202408]" in kq.stdout and "thiếu: [202409]" in kq.stdout
    assert _doc(ra)["so_dong"] == 37


@pytest.mark.parametrize("ten, sua, mau_in", [
    pytest.param("khoa_hong", lambda h: h[3].__setitem__(0, "2024-04"),
                 "khoá hỏng: [2024-04]", id="khoa_hong"),
    pytest.param("thang_13", lambda h: h[3].__setitem__(0, "202413"),
                 "khoá hỏng: [202413]", id="thang_13"),
    pytest.param("o_rong", lambda h: h[5].__setitem__(4, None),
                 "ô rỗng: 1/185", id="o_rong"),
])
def test_DT2_B3_khoa_hong_va_o_rong_thi_DO(tmp_path, ten, sua, mau_in):
    """Một ô rỗng *(IMPORTRANGE đang nạp trả ô rỗng IM LẶNG — `doc_du.py`)* hay một khoá ⛔ phải
    `yyyymm` ⇒ ghi đúng nguồn, cổng ĐỎ, và in MẪU SỐ cạnh số đếm *(Đ3)*.
    """
    hang = _hang_tong_hop(THU_TU_SHEET)
    sua(hang)
    tho = _viet_ban_tho(tmp_path / f"tho_{ten}.json", [KHOA, *TIEN_TE], hang)
    ra = tmp_path / "ix_fx.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert mau_in in kq.stdout
    assert _doc(ra)["so_dong"] == 37


@pytest.mark.parametrize("ten, doi_so_them, cot", [
    pytest.param("thieu_mong", [], [KHOA, *TIEN_TE], id="thieu_mong"),
    pytest.param("khuon_la", None, [KHOA, *TIEN_TE], id="khuon_la"),
    pytest.param("doi_so_la", ["--mong", "37", "--la"], [KHOA, *TIEN_TE], id="doi_so_la"),
    pytest.param("thieu_cot_HKD", ["--mong", "37"], [KHOA, "USD", "SGD", "COP", "VND"],
                 id="thieu_cot_HKD"),
])
def test_DT2_tu_choi_dau_vao_sai_exit_2_va_KHONG_ghi_tep(tmp_path, ten, doi_so_them, cot):
    """Từ chối *(exit 2, ⛔ ghi tệp)*: ⛔ khai `--mong` *(Đ5: cổng phải khai mong)* · khuôn ⛔ có
    · đối số ⛔ khai *(`S0-R1-03`)* · bản thô thiếu cột khuôn chọn *(ánh xạ theo TÊN)*.
    """
    hang = [h[:len(cot)] for h in _hang_tong_hop(THU_TU_SHEET)]
    tho = _viet_ban_tho(tmp_path / "tho.json", cot, hang)
    ra = tmp_path / "ra.json"
    if doi_so_them is None:
        kq = _chay("khong_co_khuon", str(tho), "--mong", "37", "--ra", str(ra))
    else:
        kq = _chay("ix_fx", str(tho), *doi_so_them, "--ra", str(ra))
    _da_tu_choi(kq)
    assert not ra.exists(), ten
