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

import ast
import copy
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
from datetime import date

import pytest

from fls.adapters.pm_join import PM_COT_RIENG_TU
from fls.cau_hinh import fx as c1_fx
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


# ══ Vòng sửa sau R1 (`KQ-087`) ═══════════════════════════════════════════════════════════════
#
# Mỗi bài dưới đây mang mã phát hiện của sổ `SO_PHAT_HIEN_ISP-3.1_DT2.md` và nói nó ĐỎ trên
# bản nào *(bản trước vòng sửa = `eb94901`)*. Khuôn là bài đề xuất của R1
# *(`scratchpad/r1_dt2/de_xuat_bai/test_r1_dt2_de_xuat.py`, 17 bài)* — viết lại theo hành vi
# mới đã chốt, ⛔ chép nguyên: R1 đề xuất `test_R1_04c` theo luật *"lạc theo thứ tự sheet"*
# mà orchestrator đã BỎ *(`DT2-R1-03`)*.

#: Tháng đầu dải của `IX.FX` — khai ĐỘC LẬP ở bài *(Đ5: khai mong)*, căn cứ AP v3.1.2 §3.2.1
#: *"37 dòng 202401 → 202612 (kể cả dòng lạc 202306)"*. Khuôn `ix_fx` phải khai đúng số ấy.
THANG_DAU_IX_FX = 202401
THU_MUC_KHUON = GOC / "tools" / "khuon_dong_bang"


def _nap_cong_cu():
    """Nạp công cụ TRONG tiến trình *(để `monkeypatch` được `GOC` · `THU_MUC_KHUON`)*.

    ⚠ Đăng ký vào `sys.modules` TRƯỚC khi chạy: `@dataclass` cùng `from __future__ import
    annotations` tra module của lớp qua `sys.modules` — thiếu là nổ lúc nạp.
    """
    spec = importlib.util.spec_from_file_location("dong_bang_sheet_bai", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["dong_bang_sheet_bai"] = mod
    spec.loader.exec_module(mod)
    return mod


def _tho_json(p: pathlib.Path, dong_json: list[str], cot: list[str] | None = None,
              doc_luc: str = "2026-03-09", nguon: str = "TỔNG HỢP · vòng sửa R1 (⛔ số thật)",
              cach_doc: str = "tổng hợp trong bài thử") -> pathlib.Path:
    """Bản thô với từng hàng viết sẵn bằng JSON — để cài được ô CHỮ `"20691.51"` *(`_viet_ban_tho`
    biến mọi chuỗi trông như số thành literal số, nên ⛔ dựng được ca ấy)*."""
    p.write_text(
        '{"nguon": %s, "doc_luc": %s, "cach_doc": %s, "cot": %s, "dong": [\n  %s\n]}\n'
        % (json.dumps(nguon, ensure_ascii=False), json.dumps(doc_luc),
           json.dumps(cach_doc, ensure_ascii=False),
           json.dumps(cot if cot is not None else [KHOA, *TIEN_TE], ensure_ascii=False),
           ",\n  ".join(dong_json)), encoding="utf-8")
    return p


def _hang_json(thang: list[int] | None = None,
               sua: dict[tuple[int, int], str] | None = None) -> list[str]:
    """Hàng JSON của `_hang_tong_hop` *(số TỔNG HỢP)*; `sua[(i, j)]` = literal JSON thay ô."""
    ra = []
    for i, h in enumerate(_hang_tong_hop(THU_TU_SHEET if thang is None else thang)):
        o = list(h)
        for (si, sj), lit in (sua or {}).items():
            if si == i:
                o[sj] = lit
        ra.append("[" + ", ".join(o) + "]")
    return ra


def _sha(p: pathlib.Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _kiem_C1(anh: dict) -> c1_fx.BangFX:
    """Chạy `kiem` của C1 TRÊN CHÍNH ẢNH — ánh xạ `Month → yyyymm` *(Q3: C5 ánh xạ)*, bỏ
    `thu_tu`. Bài tự ánh xạ, ⛔ mượn hàm của khuôn: đây là phép so ĐỘC LẬP."""
    return c1_fx.kiem([{"yyyymm": d[KHOA], **{c: d[c] for c in TIEN_TE}} for d in anh["dong"]],
                      thang_dau=THANG_DAU_IX_FX, nguon="bai-thu")


def _dong_loi(kq_err: str, dau: str) -> list[str]:
    return [d for d in kq_err.splitlines() if d.startswith(dau)]


# ── DT2-R1-01 · cổng ĐỎ ⛔ đè ảnh ở đường MẶC ĐỊNH ──────────────────────────────────────────

def test_R1_01_cong_DO_khong_ra_thi_KHONG_de_anh_da_commit_ma_ghi_tep_DO(tmp_path, monkeypatch,
                                                                        capsys):
    """⛔ BG-086 yếu ⑤ · `DT2-R1-01`: lượt ĐỎ ⛔ `--ra` từng **ghi đè ảnh đã commit** — R1 đo
    `--mong 36` ⇒ ` M tests/fixture/cau_hinh/ix_fx.json`, chỉ 1/20 bài bắt.

    Chạy trong tiến trình, `GOC` trỏ một gốc TẠM mang **đúng từng byte** ảnh đã commit ⇒ bài
    ⛔ bao giờ chạm ảnh thật kể cả khi công cụ hồi quy. Bản thô = tái tạo từ chính ảnh;
    `--mong 36` ⛔ `--ra` ⇒ exit 1, sha256 ảnh **trước = sau**, ảnh đỏ nằm ở `ix_fx.DO.json`.
    ĐỎ trên `eb94901` *(ảnh bị đè)*.
    """
    mod = _nap_cong_cu()
    goc_gia = tmp_path / "goc"
    anh_gia = goc_gia / ANH_IX_FX.relative_to(GOC)
    anh_gia.parent.mkdir(parents=True)
    anh_gia.write_bytes(ANH_IX_FX.read_bytes())
    truoc = _sha(anh_gia)
    monkeypatch.setattr(mod, "GOC", goc_gia)

    tho = _ban_tho_tu_anh(_doc(ANH_IX_FX), tmp_path / "tho_tu_anh.json")
    assert mod.main(["ix_fx", str(tho), "--mong", "36"]) == 1
    assert _sha(anh_gia) == truoc, "lượt ĐỎ ⛔ --ra đã ĐÈ ảnh ở đường mặc định"

    do = anh_gia.with_name("ix_fx.DO.json")
    assert do.is_file(), "ISP B3: cổng đỏ thì ảnh VẪN ghi — ở tệp cạnh, ⛔ đè"
    anh_do = _doc(do)
    assert anh_do["cong"]["dat"] is False and anh_do["cong"]["mong"] == 36
    out = capsys.readouterr().out
    assert "ix_fx.DO.json" in out and "[ĐỎ] cổng --mong 36" in out


def test_R1_01_cong_DAT_khong_ra_thi_ghi_DUNG_duong_mac_dinh_va_KHONG_tep_DO(tmp_path, monkeypatch):
    """Đối chứng của bài trên *(Đ5 hai chiều)*: lượt ĐẠT ⛔ `--ra` vẫn ghi ĐÚNG đường mặc định
    *(lệnh ISP `… ix_fx <bản thô> --mong 37`)* — ⛔ được "an toàn" bằng cách ⛔ bao giờ ghi."""
    mod = _nap_cong_cu()
    goc_gia = tmp_path / "goc"
    monkeypatch.setattr(mod, "GOC", goc_gia)
    tho = _ban_tho_tu_anh(_doc(ANH_IX_FX), tmp_path / "tho_tu_anh.json")
    assert mod.main(["ix_fx", str(tho), "--mong", "37"]) == 0
    ra = goc_gia / ANH_IX_FX.relative_to(GOC)
    assert ra.read_bytes() == ANH_IX_FX.read_bytes()
    assert not ra.with_name("ix_fx.DO.json").exists()


def test_R1_01b_anh_da_commit_mang_cong_DAT():
    """`DT2-R1-01`: bài nội dung từng ⛔ đòi `cong.dat` — một ảnh mang `"dat": false` qua cả bài
    nội dung lẫn checksum *(checksum `AnhChup` ⛔ phủ khối `cong`)*. Xanh trên `eb94901`; ĐỎ khi
    một lượt đỏ ghi vào đường của ảnh *(R1 đo: bản thô thật `--mong 36` ⛔ `--ra` ⇒ bài này đỏ)*."""
    anh = _doc(ANH_IX_FX)
    assert anh["cong"] == {"mong": 37, "so_dong": 37, "dat": True, "ly_do": []}


# ── DT2-R1-02 · ô CHỮ ⛔ được qua cổng · ảnh phân biệt SỐ với CHỮ ───────────────────────────

@pytest.mark.parametrize("lit, mong_anh", [
    pytest.param('"20,692"', {"chu": "20,692"}, id="hien_thi_formattedValue"),
    pytest.param('"20691.51"', {"chu": "20691.51"}, id="so_go_thanh_chu"),
    pytest.param('" 20691.51"', {"chu": " 20691.51"}, id="khoang_trang_dau"),
    pytest.param("true", True, id="bool"),
])
def test_R1_02_o_KHONG_SO_o_cot_tien_te_thi_DO_va_anh_ghi_ro_la_chu(tmp_path, lit, mong_anh):
    """`DT2-R1-02`: R1 đo SGD `202507` = chuỗi `"20,692"` *(đúng giá trị HIỂN THỊ mà docstring
    công cụ nêu làm lý do đọc `effectiveValue`)* ⇒ `[ĐẠT]` exit 0 — trong khi `kiem` của C1
    từ chối nó, và AS-IS `SUMIFS` bỏ qua ô chữ ⇒ ra 0 IM LẶNG *(AP §3.2.4)*.

    Mong: exit 1 · `ô ⛔ số: 1/185` *(mẫu số — `S0-R1-05`)* · trong ảnh ô ấy là `{"chu": …}`
    *(⛔ lẫn được với ô số `"20691.51"`)*, ô số bên cạnh vẫn là chuỗi đúng chữ số.
    ĐỎ trên `eb94901` *(exit 0)*.
    """
    tho = _tho_json(tmp_path / "tho.json", _hang_json(sua={(18, 2): lit}))
    ra = tmp_path / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 1, (kq.returncode, kq.stdout[-1500:], kq.stderr[-800:])
    assert "ô ⛔ số: 1/185" in kq.stdout, kq.stdout[-1500:]
    anh = _doc(ra)
    d19 = anh["dong"][18]
    assert (d19[KHOA], d19["SGD"]) == ("202507", mong_anh)
    assert d19["USD"] == "25018" and anh["dong"][17]["SGD"] == "19017.51"
    assert anh["cong"]["dat"] is False


def test_R1_02_khoa_Month_CHU_thi_KHOA_HONG_va_anh_KHAC_anh_so(tmp_path):
    """`DT2-R1-02` · R1 ⑨: cột `Month` toàn CHUỖI `"202401"` ⇒ ảnh ra **giống từng byte** ảnh
    đã commit — ảnh ⛔ còn nói được nguồn là số hay chữ. Mong: khoá chữ = khoá hỏng *(37/37)*,
    exit 1, ảnh KHÁC ảnh commit. ĐỎ trên `eb94901` *(exit 0, byte-identical)*."""
    anh_goc = _doc(ANH_IX_FX)
    dong = sorted(anh_goc["dong"], key=lambda d: d["thu_tu"])
    hang = ["[" + ", ".join([json.dumps(d[KHOA])] + [d[c] for c in TIEN_TE]) + "]" for d in dong]
    tho = _tho_json(tmp_path / "tho_month_chu.json", hang, nguon=anh_goc["nguon"],
                    doc_luc=anh_goc["ngay_dong_bang"], cach_doc=anh_goc["cach_doc"])
    ra = tmp_path / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-800:])
    assert ra.read_bytes() != ANH_IX_FX.read_bytes()
    anh = _doc(ra)
    assert len(anh["khoa_hong"]) == 37
    assert anh["khoa_hong"][0] == {"chu": "202401"}
    assert "(37/37 dòng · chữ 37)" in kq.stdout, kq.stdout[-1500:]


def test_R1_02_kiem_C1_chay_TREN_CHINH_ANH_va_thay_chu_la_chu(tmp_path):
    """`DT2-R1-02`: *"ghi kiểu/giá trị sao cho bên nhận C1 `kiem` chạy được trên chính ảnh"*.

    ① ảnh đã commit ⇒ `kiem` của C1 nhận, `lac = (202306,)` · `thieu = trung = ()`.
    ② ảnh có ô CHỮ `"20691.51"` ⇒ `kiem` của C1 **từ chối** *(`LoiFX` nói `SGD`)*. Trên
       `eb94901` ảnh ghi ô ấy thành `"20691.51"` — y hệt ô số — nên C1 NHẬN ⇒ ĐỎ.
    """
    b = _kiem_C1(_doc(ANH_IX_FX))
    assert (b.lac, b.thieu, b.trung, len(b.ky)) == ((202306,), (), (), 37)

    tho = _tho_json(tmp_path / "tho.json", _hang_json(sua={(18, 2): '"20691.51"'}))
    ra = tmp_path / "a.json"
    _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    with pytest.raises(c1_fx.LoiFX, match="SGD"):
        _kiem_C1(_doc(ra))


# ── DT2-R1-03 · MỘT định nghĩa thiếu/lạc — của C1 *(theo `thang_dau`)* ─────────────────────

@pytest.mark.parametrize("thu_tu", [
    pytest.param([THU_TU_SHEET[1], THU_TU_SHEET[0], *THU_TU_SHEET[2:]], id="doi_cho_202401_202402"),
    pytest.param([202306, *[t for t in THU_TU_SHEET if t != 202306]], id="dong_lac_dung_DAU"),
    pytest.param([*[t for t in THU_TU_SHEET if t != 202405], 202405], id="202405_xuong_CUOI"),
])
def test_R1_03_thieu_lac_theo_thang_dau_cua_C1_KHONG_theo_thu_tu_sheet(tmp_path, thu_tu):
    """`DT2-R1-03`: hai định nghĩa máy cho cùng bảng — R1 đo trên bản cũ: đổi chỗ `202401`/
    `202402` ⇒ `lac=['202401','202306']` ↔ C1 `[202306]`; dòng lạc đứng ĐẦU ⇒ cũ báo
    `thieu` 6 tháng GIẢ *(202307…202312, cổng ĐỎ)* ↔ C1 `thieu=[]`.

    Orchestrator chốt MỘT định nghĩa — của C1 *(`fls/cau_hinh/fx.py`, `thang_dau`)*. Mong ở cả
    ba thứ tự: exit 0 · `lac = ['202306']` · `thieu = []` · và **bằng** `kiem` của C1 chạy trên
    chính ảnh. ĐỎ trên `eb94901` cả ba ca.
    """
    tho = _viet_ban_tho(tmp_path / "tho.json", [KHOA, *TIEN_TE], _hang_tong_hop(thu_tu))
    ra = tmp_path / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-800:])
    anh = _doc(ra)
    assert (anh["thieu"], anh["lac"]) == ([], ["202306"])
    b = _kiem_C1(anh)
    assert (anh["thieu"], anh["lac"]) == ([str(m) for m in b.thieu], [str(m) for m in b.lac])
    assert "thiếu: []" in kq.stdout and "lạc: [202306]" in kq.stdout


def test_R1_03_khuon_ix_fx_KHAI_thang_dau_202401_va_GOI_kiem_cua_C1():
    """Một chỗ khai `thang_dau` *(khuôn `ix_fx`)*, và khuôn gọi CHÍNH hàm `kiem` của C1 — ⛔ một
    bản chép *(đổi định nghĩa ở C1 ⇒ khuôn đổi theo, ⛔ lệch lại như `DT2-R1-03`)*."""
    spec = importlib.util.spec_from_file_location("khuon_ix_fx_bai", THU_MUC_KHUON / "ix_fx.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert m.THANG_DAU == THANG_DAU_IX_FX
    assert m.kiem is c1_fx.kiem


def test_R1_03_C1_tu_choi_bang_thi_thieu_lac_KHONG_DO_DUOC_la_DO(tmp_path):
    """Khuôn gọi `kiem` của C1; C1 từ chối CẢ bảng khi một dòng hỏng *(ở đây `VND = 2` — luật
    nghiệp vụ của C1, ⛔ viết lại ở công cụ)* ⇒ thiếu/lạc **⛔ đo được**.

    ⛔ Đ5: *"phép ⛔ đo được là ĐỎ, ⛔ phải 'không thấy lệch'"*. ⇒ ảnh ghi `thieu = lac = null`
    *(⛔ `[]` — `[]` là "đã đo, 0")*, cổng ĐỎ, dòng báo nói lý do của C1. Cũng là luật phòng
    tái phạm của `DT2-R1-02`: *"cổng đóng băng chặn ít nhất mọi thứ bên tiêu thụ đầu tiên từ
    chối"*. ĐỎ trên `eb94901` *(exit 0 — R1 ⑭)*.
    """
    tho = _tho_json(tmp_path / "tho.json", _hang_json(sua={(5, 4): "2"}))
    ra = tmp_path / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-800:])
    anh = _doc(ra)
    assert anh["thieu"] is None and anh["lac"] is None
    assert any("thiếu/lạc ⛔ đo được" in x and "VND" in x for x in anh["cong"]["ly_do"])
    assert "thiếu: ⛔ ĐO ĐƯỢC" in kq.stdout


# ── DT2-R1-04 · mọi chốt phụ phải được chứng minh CẮN *(đột biến D1–D8 · D10–D12)* ──────────

@pytest.mark.parametrize("cot, dong, doi_so, sua_tho, phai_noi", [
    pytest.param(None, _hang_json()[:36] + ["[202612, 1, 1, 1, 1, 1, 9]"], ["--mong", "37"], {},
                 "ô > 6 cột", id="D1_dong_dai_hon_tieu_de"),
    pytest.param([KHOA, *TIEN_TE, "USD "], [h[:-1] + ", 0]" for h in _hang_json()],
                 ["--mong", "37"], {}, "tên trùng", id="D2_ten_cot_trung"),
    pytest.param(None, [], ["--mong", "37"], {}, "0 dòng", id="D3_ban_tho_0_dong"),
    pytest.param(None, _hang_json(), ["--mong", "0"], {}, "--mong 0", id="D4_mong_0"),
    pytest.param(None, _hang_json(), ["--mong=-1"], {}, "--mong -1", id="D4_mong_am"),
    pytest.param(None, _hang_json(), ["--mong", "37"], {"doc_luc": "16/11/2026"}, "doc_luc",
                 id="D5_doc_luc_hong"),
    pytest.param(None, _hang_json(), ["--mong", "37"], {"nguon": ""}, "nguon",
                 id="D6_thieu_nguon"),
    pytest.param(None, _hang_json(), ["--mong", "37"], {"cach_doc": "  "}, "cach_doc",
                 id="D6_thieu_cach_doc"),
    pytest.param(None, ['[202401, {"a": 1}, 1, 1, 1, 1]'] + _hang_json()[1:], ["--mong", "37"],
                 {}, "kiểu dict", id="D8_o_dict"),
    pytest.param(None, ["[202401, [1], 1, 1, 1, 1]"] + _hang_json()[1:], ["--mong", "37"],
                 {}, "kiểu list", id="D8_o_list"),
    pytest.param(None, ["[202401, NaN, 1, 1, 1, 1]"] + _hang_json()[1:], ["--mong", "37"], {},
                 "hằng `NaN`", id="D11_NaN"),
    pytest.param(None, ["[202401, -Infinity, 1, 1, 1, 1]"] + _hang_json()[1:], ["--mong", "37"],
                 {}, "hằng `-Infinity`", id="D11_am_vo_cuc"),
])
def test_R1_04_moi_duong_TU_CHOI_exit_2_mot_dong_dung_ly_do_KHONG_ghi(tmp_path, cot, dong, doi_so,
                                                                     sua_tho, phai_noi):
    """`DT2-R1-04`: R1 đột biến 14 chốt, bộ 20 bài bắt 3 — mọi chốt CHẠY đúng nhưng ⛔ bài nào
    canh. Mỗi ca ở đây là MỘT chốt; đòi exit 2 + **đúng một dòng** `⛔ TỪ CHỐI` + dòng ấy nói
    **đúng lý do** *(`phai_noi`)*.

    ⭐ Vì sao đòi lý do: D11 *(bỏ `parse_constant`)* SỐNG trước bài của R1 vì `NaN` khi ấy thành
    `float` rồi bị `_o` từ chối — vẫn exit 2, nhưng vì lý do KHÁC. Đòi chữ `hằng \\`NaN\\``
    thì hai chốt chồng nhau được canh RIÊNG.
    """
    tho = _tho_json(tmp_path / "tho.json", dong, cot=cot, **sua_tho)
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("ix_fx", str(tho), *doi_so, "--ra", str(ra))
    _da_tu_choi(kq)
    assert phai_noi in _dong_loi(kq.stderr, "⛔ TỪ CHỐI")[0], kq.stderr[-800:]
    assert not ra.exists() and not ra.parent.exists()


def test_R1_04_o_CHI_KHOANG_TRANG_la_RONG_khong_phai_CHU(tmp_path):
    """D7: ô `"   "` *(Sheets: ô văn bản chỉ có dấu cách)* là ô RỖNG — ⛔ qua cổng, và ⛔ đếm
    hai lần *(rỗng ∩ chữ = ∅: mỗi ô cột số rơi vào ĐÚNG một trong số · rỗng · ⛔ số)*."""
    tho = _tho_json(tmp_path / "tho.json", _hang_json(sua={(18, 2): '"   "'}))
    ra = tmp_path / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 1, kq.stdout[-1500:]
    assert "ô rỗng: 1/185" in kq.stdout and "ô ⛔ số: 0/185" in kq.stdout
    assert _doc(ra)["o_rong"] == [{"thu_tu": 19, "cot": "SGD"}]


# ── DT2-R1-05 · lỗi GHI ⛔ trùng mã 1 *("cổng ĐỎ, ảnh đã ghi")* ─────────────────────────────

def test_R1_05_ra_la_THU_MUC_thi_exit_3_mot_dong_KHONG_traceback(ban_tho_37, tmp_path):
    """R1 đo: `--ra <thư mục>` ⇒ `IsADirectoryError` traceback, exit **1** = mã *"cổng ĐỎ, ảnh
    VẪN ghi"* — trong khi ⛔ tệp nào được ghi. Mong: exit **3**, đúng MỘT dòng `⛔ LỖI GHI`,
    ⛔ traceback *(`S0-R1-04`)*. ĐỎ trên `eb94901`."""
    d = tmp_path / "la_thu_muc"
    d.mkdir()
    kq = _chay("ix_fx", str(ban_tho_37), "--mong", "37", "--ra", str(d))
    assert kq.returncode == 3, (kq.returncode, kq.stderr[-800:])
    assert "Traceback" not in kq.stderr
    assert len(_dong_loi(kq.stderr, "⛔ LỖI GHI")) == 1, kq.stderr[-800:]
    assert list(d.iterdir()) == [] and sorted(x.name for x in tmp_path.iterdir()) == [
        "la_thu_muc", "tho_37.json"], "⛔ được sót tệp tạm"


def test_R1_05_D12_dia_DAY_giua_chung_thi_exit_3_anh_cu_NGUYEN_va_0_tep_tam(ban_tho_37, tmp_path):
    """D12 *(ghi ⛔ nguyên tử)* + R1-05 trên một lỗi I/O THẬT: giới hạn cỡ tệp
    *(`RLIMIT_FSIZE`)* nhỏ hơn ảnh ⇒ lệnh `write` hỏng GIỮA CHỪNG *(`EFBIG` — CPython bỏ qua
    `SIGXFSZ`)*. Ghi nguyên tử ⇒ tệp cũ **giữ nguyên byte**, 0 tệp `.tam` sót, exit 3. Ghi
    thẳng vào tệp đích ⇒ tệp cũ thành **nửa ảnh** ⇒ ĐỎ.

    Đ3: giới hạn phải THẬT nhỏ hơn ảnh — đo ảnh đối chứng trước, ⛔ tin con số.
    ⚠ Chỉ chạy được ở hệ có `resource` *(Linux/macOS)*; Windows bỏ qua.
    """
    resource = pytest.importorskip("resource")
    gioi_han = 2048
    doi_chung = tmp_path / "doi_chung" / "a.json"
    assert _chay("ix_fx", str(ban_tho_37), "--mong", "37", "--ra", str(doi_chung)).returncode == 0
    assert doi_chung.stat().st_size > gioi_han, "giới hạn ⛔ nhỏ hơn ảnh ⇒ phép thử rỗng (Đ3)"

    noi = tmp_path / "noi"
    noi.mkdir()
    cu = noi / "ix_fx.json"
    cu.write_bytes(b'{"giu": "nguyen"}\n')

    def _han() -> None:
        resource.setrlimit(resource.RLIMIT_FSIZE, (gioi_han, gioi_han))

    env = dict(os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1")
    kq = subprocess.run([sys.executable, str(TOOL), "ix_fx", str(ban_tho_37), "--mong", "37",
                         "--ra", str(cu)], cwd=GOC, env=env, capture_output=True, text=True,
                        timeout=60, preexec_fn=_han)
    assert kq.returncode == 3, (kq.returncode, kq.stdout[-800:], kq.stderr[-800:])
    assert cu.read_bytes() == b'{"giu": "nguyen"}\n', "ghi ⛔ nguyên tử: ảnh cũ bị thay bằng nửa ảnh"
    assert [x.name for x in noi.iterdir()] == ["ix_fx.json"], "⛔ được sót tệp tạm"
    assert len(_dong_loi(kq.stderr, "⛔ LỖI GHI")) == 1 and "Traceback" not in kq.stderr


# ── DT2-R1-06 · `doc_luc` phải là NGÀY ISO `YYYY-MM-DD` ─────────────────────────────────────

@pytest.mark.parametrize("doc_luc", [
    pytest.param("2026-W46-1", id="tuan_ISO"),
    pytest.param("20261116", id="ISO_gon"),
    pytest.param("2026-11-16T00:00:00", id="co_gio"),
    pytest.param("2026-02-30", id="ngay_khong_co"),
    pytest.param("16/11/2026", id="kieu_VN"),
])
def test_R1_06_doc_luc_KHONG_phai_YYYY_MM_DD_thi_TU_CHOI(tmp_path, doc_luc):
    """`DT2-R1-06`: `date.fromisoformat` *(Python ≥ 3.11)* nhận cả `2026-W46-1` lẫn `20261116`,
    và công cụ cũ ghi NGUYÊN chuỗi ấy vào `ngay_dong_bang` — quyết định ③ hứa một NGÀY. Mong:
    chỉ `YYYY-MM-DD` có thật. ĐỎ trên `eb94901` ở `tuan_ISO` · `ISO_gon` *(exit 0)*; ba ca còn
    lại là chốt đã có, giữ để canh."""
    tho = _tho_json(tmp_path / "tho.json", _hang_json(), doc_luc=doc_luc)
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    _da_tu_choi(kq)
    assert "doc_luc" in _dong_loi(kq.stderr, "⛔ TỪ CHỐI")[0]
    assert not ra.exists()


# ── DT2-R1-08 · cột tiêu đề RỖNG mà có dữ liệu ──────────────────────────────────────────────

def test_R1_08_cot_tieu_de_RONG_CO_du_lieu_thi_TU_CHOI(tmp_path):
    """`DT2-R1-08`: cột tiêu đề `""` mang chữ ở mọi dòng ⇒ bản cũ exit 0, bỏ cột IM LẶNG, báo
    *"7 cột"* mà *"khoá 1 + 5 + ⛔ chọn 0"* = 6 *(Đ4)*. Cùng lúc công cụ TỪ CHỐI dòng dài hơn
    tiêu đề vì *"ô ngoài tiêu đề sẽ mất im lặng"* — hai luật lệch nhau. Thêm một lý do: cột
    ⛔ tên thì ⛔ soát riêng tư THEO TÊN được *(`PM_COT_RIENG_TU`)*. Mong: exit 2, ⛔ ghi.
    ĐỎ trên `eb94901`."""
    hang = [h[:-1] + f', "ghi chu {i}"]' for i, h in enumerate(_hang_json())]
    tho = _tho_json(tmp_path / "tho.json", hang, cot=[KHOA, *TIEN_TE, ""])
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    _da_tu_choi(kq)
    assert "tiêu đề rỗng" in _dong_loi(kq.stderr, "⛔ TỪ CHỐI")[0]
    assert "ghi chu" not in kq.stdout + kq.stderr, "⛔ in giá trị của cột ⛔ soát được"
    assert not ra.exists()


def test_R1_08_cot_tieu_de_RONG_MOI_O_RONG_thi_nhan_va_dong_bao_CONG_DUNG(tmp_path):
    """Cột tiêu đề rỗng mà MỌI ô rỗng *(Sheets trả thêm cột trống)* ⇒ nhận; dòng báo
    `bản thô` phải **cộng lại** đúng *(Đ4: N cột = khoá + chọn + ⛔ chọn + tiêu đề rỗng)* và
    `khong_mang_PII` kể cột ấy. ĐỎ trên `eb94901` *(dòng báo `7 cột` ⛔ nhãn)*."""
    hang = [h[:-1] + ", null]" for h in _hang_json()]
    tho = _tho_json(tmp_path / "tho.json", hang, cot=[KHOA, *TIEN_TE, "", "Ghi chú"])
    ra = tmp_path / "a.json"
    kq = _chay("ix_fx", str(tho), "--mong", "37", "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-800:])
    m = re.search(r"bản thô\s*: (\d+) cột tiêu đề = khoá (\d+) \+ chọn (\d+) \+ ⛔ chọn (\d+) "
                  r"\+ tiêu đề rỗng (\d+) · 37 dòng", kq.stdout)
    assert m, kq.stdout[-1500:]
    n, *phan = (int(x) for x in m.groups())
    assert (n, phan) == (8, [1, 5, 1, 1]) and n == sum(phan)
    anh = _doc(ra)
    assert anh["cot_khong_chon"] == ["Ghi chú"]
    assert "1 cột tiêu đề rỗng" in anh["khong_mang_PII"]


# ── Khuôn = MỘT TỆP *(orchestrator 16/11: DT3…DT12 thêm khuôn SONG SONG)* ───────────────────

def _chuoi_trong_ma(p: pathlib.Path) -> set[str]:
    """Mọi hằng chuỗi của tệp `.py` TRỪ docstring *(docstring là bia, được nhắc tên khuôn)*."""
    cay = ast.parse(p.read_text(encoding="utf-8"))
    doc = set()
    for n in ast.walk(cay):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) \
                and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(n.body[0].value, ast.Constant):
            doc.add(id(n.body[0].value))
    return {n.value for n in ast.walk(cay)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in doc}


def test_KHUON_ix_fx_la_mot_tep_va_cong_cu_KHONG_mang_du_lieu_khuon():
    """Khuôn `ix_fx` nằm ở `tools/khuon_dong_bang/ix_fx.py`; gói có `__init__.py` **0 byte**;
    công cụ tìm thấy `ix_fx` *(và ĐÚNG mọi tệp khuôn của thư mục)*; và MÃ công cụ ⛔ còn mang dữ
    liệu khuôn nào *(tên bảng, khoá, tiền tệ, đường ảnh)* — còn là còn phải sửa công cụ khi thêm
    khuôn. ĐỎ trên `eb94901`.

    ⚠ DT3 *(`WO-106`)*: bản đầu ghim `danh_sach_khuon() == ['ix_fx']` — đúng khi `ix_fx` là khuôn
    DUY NHẤT. DT3 thêm ba tệp khuôn *(`atl_cay` · `mapping_master_cfg` · `cdt_correct` — đúng điều
    bài này canh: thêm khuôn = thêm TỆP)* ⇒ bài ĐỎ `['atl_cay', …] == ['ix_fx']`, tiền đề "một
    khuôn" hết đúng. Lo gốc GIỮ: `ix_fx` được tìm thấy, và công cụ thấy ĐÚNG tập tệp khuôn —
    ⛔ bỏ sót tệp nào, ⛔ thấy tệp ⛔ có."""
    assert (THU_MUC_KHUON / "__init__.py").read_bytes() == b""
    assert (THU_MUC_KHUON / "ix_fx.py").is_file()
    co = _nap_cong_cu().danh_sach_khuon()
    assert "ix_fx" in co
    assert co == sorted(p.stem for p in THU_MUC_KHUON.glob("*.py") if not p.stem.startswith("_"))
    lot = _chuoi_trong_ma(TOOL) & {"IX.FX", "Month", "USD", "VND", "tests/fixture/cau_hinh/ix_fx.json"}
    assert lot == set(), f"công cụ còn mang dữ liệu khuôn: {sorted(lot)}"


KHUON_GIA = '''"""Khuôn GIẢ LẬP của bài thử — ⛔ dữ liệu thật."""
BANG = "GIA.LAP"
KHOA = "Thang"
KIEU_KHOA = "yyyymm"
COT = ("A", "B")
RA = "khong_bao_gio_ghi/gia.json"


def thieu_lac(dong):
    return {"thieu": [], "lac": [], "dai": "giả lập"}
'''


def _goc_khuon_gia(tmp_path: pathlib.Path, noi_dung: str, ten: str = "gia") -> pathlib.Path:
    thu_muc = tmp_path / "khuon"
    thu_muc.mkdir(exist_ok=True)
    (thu_muc / "__init__.py").write_bytes(b"")
    (thu_muc / f"{ten}.py").write_text(noi_dung, encoding="utf-8")
    return thu_muc


def _tho_gia(p: pathlib.Path) -> pathlib.Path:
    return _tho_json(p, ["[202401, 1, 2]", "[202402, 3, 4.5]", "[202403, 5, 6]"],
                     cot=["Thang", "A", "B"])


def test_KHUON_moi_la_THEM_MOT_TEP_KHONG_sua_cong_cu(tmp_path, monkeypatch, capsys):
    """⭐ Thêm khuôn = THÊM một tệp vào thư mục khuôn — công cụ ⛔ đổi một byte: thư mục tạm có
    `gia.py` ⇒ `danh_sach_khuon()` thấy nó, lệnh `gia …` chạy và ghi ảnh theo khuôn ấy.
    ĐỎ trên `eb94901` *(⛔ có `THU_MUC_KHUON` — khuôn khai cứng trong `KHUON`)*."""
    sha_cong_cu = _sha(TOOL)
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon_gia(tmp_path, KHUON_GIA))
    assert mod.danh_sach_khuon() == ["gia"]

    ra = tmp_path / "gia.json"
    assert mod.main(["gia", str(_tho_gia(tmp_path / "tho.json")), "--mong", "3",
                     "--ra", str(ra)]) == 0, capsys.readouterr()
    anh = _doc(ra)
    assert (anh["bang"], anh["khuon"], anh["khoa"], anh["cot"]) == ("GIA.LAP", "gia", "Thang",
                                                                     ["A", "B"])
    assert [d["B"] for d in anh["dong"]] == ["2", "4.5", "6"]
    assert mod.main(["ix_fx", str(_tho_gia(tmp_path / "tho2.json")), "--mong", "3"]) == 2, \
        "khuôn ⛔ có trong thư mục ⇒ TỪ CHỐI"
    assert _sha(TOOL) == sha_cong_cu


@pytest.mark.parametrize("noi_dung, phai_noi", [
    pytest.param(KHUON_GIA.replace('COT = ("A", "B")\n', ""), "COT", id="thieu_COT"),
    pytest.param(KHUON_GIA.replace('KIEU_KHOA = "yyyymm"', 'KIEU_KHOA = "chu"'), "KIEU_KHOA",
                 id="kieu_khoa_chua_co"),
    pytest.param(KHUON_GIA + "\nday la loi cu phap\n", "SyntaxError", id="cu_phap"),
])
def test_KHUON_hong_thi_TU_CHOI_exit_2_mot_dong(tmp_path, monkeypatch, capsys, noi_dung, phai_noi):
    """Khuôn do làn khác viết *(DT3…)* — khuôn thiếu tên bắt buộc / kiểu khoá chưa có / sai cú
    pháp ⇒ exit 2, MỘT dòng nói tên khuôn + chỗ hỏng, ⛔ ghi."""
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon_gia(tmp_path, noi_dung))
    ra = tmp_path / "moi" / "gia.json"
    assert mod.main(["gia", str(_tho_gia(tmp_path / "tho.json")), "--mong", "3",
                     "--ra", str(ra)]) == 2
    dong = _dong_loi(capsys.readouterr().err, "⛔ TỪ CHỐI")
    assert len(dong) == 1 and "gia" in dong[0] and phai_noi in dong[0], dong
    assert not ra.parent.exists()


def test_KHUON_no_khi_tinh_thieu_lac_thi_exit_3_KHONG_trung_ma_cong_DO(tmp_path, monkeypatch,
                                                                       capsys):
    """`DT2-R1-05` áp cho chỗ cắm khuôn: khuôn nổ *(lỗi lập trình, ⛔ `ValueError`)* ⇒ exit 3
    *(⛔ 1 = "ảnh đỏ đã ghi")*, ⛔ ghi; traceback GIỮ để sửa khuôn, dòng cuối `⛔ LỖI`."""
    mod = _nap_cong_cu()
    no = KHUON_GIA.replace('return {"thieu": [], "lac": [], "dai": "giả lập"}',
                           'return len(None)')
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon_gia(tmp_path, no))
    ra = tmp_path / "gia.json"
    assert mod.main(["gia", str(_tho_gia(tmp_path / "tho.json")), "--mong", "3",
                     "--ra", str(ra)]) == 3
    err = capsys.readouterr().err
    assert len(_dong_loi(err, "⛔ LỖI")) == 1 and "TypeError" in err
    assert not ra.exists()


def test_KHUON_ix_fx_nhan_BAN_SAO_anh_KHONG_sua_duoc_anh(tmp_path, monkeypatch):
    """Khuôn nhận BẢN SAO các dòng ảnh — một khuôn lỡ tay sửa dòng ⛔ được đổi ảnh đã đóng băng
    *(ảnh phải = nguồn)*."""
    mod = _nap_cong_cu()
    sua = KHUON_GIA.replace('return {"thieu": [], "lac": [], "dai": "giả lập"}',
                            'dong[0]["A"] = "999"\n'
                            '    dong[1]["B"]["chu"] = "da sua"\n'
                            '    return {"thieu": [], "lac": [], "dai": "giả lập"}')
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon_gia(tmp_path, sua))
    ra = tmp_path / "gia.json"
    tho = _tho_json(tmp_path / "tho.json", ['[202401, 1, 2]', '[202402, 3, "chu"]',
                                             '[202403, 5, 6]'], cot=["Thang", "A", "B"])
    assert mod.main(["gia", str(tho), "--mong", "3", "--ra", str(ra)]) == 1   # ô chữ ⇒ ĐỎ
    anh = _doc(ra)
    goc = copy.deepcopy(anh["dong"])
    assert (goc[0]["A"], goc[1]["B"]) == ("1", {"chu": "chu"}), "khuôn đã sửa được ẢNH"
