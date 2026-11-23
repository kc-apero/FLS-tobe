"""Ba ảnh nguồn `IX.HD` · `IX.ORG` *(ISP 3.1.2 · Step 10 · DT3 · `WO-106`)* — cây ATL · Mapping
Master · CDT Correct, đóng băng qua CHÍNH đường ống DT2 *(`tools/dong_bang_sheet.py`)*.

⭐ **Vì sao có tệp này.** Bước sau *(C4 cây HD · C8 IX.ORG · C12 dòng PL)* cần ba ẢNH đứng yên
của ba nguồn đang nằm ở sheet NOW, mỗi ảnh có checksum + một cổng khai `mong` *(Đ5)*:

    cây ATL       `'Report I PLA3 Y H Q M | PM + HR | ATL'!A7:F90` ⇒ 74 dòng MÃ · 6 nhóm
    Mapping Master `'Mapping Master'!A1:P120` *(RAW)*            ⇒ 73 mã `hd` *(đầu ra `doc_cot`)*
    CDT Correct   `'Report I H1000 Ledge … | For PL Report'!BR11:BS32` ⇒ 13 dòng

Mỗi con số đếm MỘT vật *(Đ4)*:
  · **74** = dòng MÃ của cây *(nhãn `MÃ | Tên`)* — ⛔ kể 6 dòng tiêu đề nhóm `MÃ|Tên` và 1 dòng
    trống; 81 hàng đọc `A7:F87` = 74 + 6 + 1 *(hàng 88 rỗng, API ⛔ trả)*.
  · **6** = dòng tiêu đề NHÓM `HDO · HDH · HDAP · HDT · HDC · HDCI` *(AP v3.1.2 §3.2.5)*.
  · **73** = mã `hd` mà `fls.adapters.mapping_master.doc_cot` trả *(dữ liệu từ dòng 7, cột H)* —
    ⛔ số hàng của vùng `A1:P120` *(85 hàng có ô)*.
  · **13** = dòng CÓ DỮ LIỆU ở `BR11:BS23` *(quyết định ⑪ của `WO-106`)* — ⛔ "18 dòng
    (BR11:BS28)" của ISP/AP: đó là khoảng Ô, đo lại `BR8:BS32` thì `BR24:BS32` RỖNG.

⛔⛔ **Bản đọc thô thật ⛔ nằm trong repo** *(scratchpad orchestrator — O7)*. ⇒ như DT2: ẢNH đã
commit được kiểm bằng cách **tái tạo bản thô ĐÚNG HÌNH DẠNG orchestrator đưa** từ chính ảnh, chạy
lại công cụ ⇒ phải ra **đúng từng byte**; ca phá *(DT3-B2)* xoá một dòng ở BẢN SAO ấy.

⛔⛔ **Riêng tư** *(AC-3 · `DT3-R1-01`)*. Mapping Master cột `A · B · O` có **7 hàng** mang tên
viết tắt NGƯỜI *(tài khoản PO cá nhân)*. Khuôn `mapping_master_cfg` GIẢ DANH HOÁ chúng — cả `A`
lẫn `B` của hàng ấy thành HẰNG `"an_danh:tk_ca_nhan"` *(⛔ băm: muối công khai trong repo đảo
ngược được — `2a31f76` đảo 7/7)*. ⇒ Ảnh ⛔ mang chuỗi riêng nào, và máy quét đòi: ⛔ chuỗi dạng
`sha256_16:`/hex-16 nào trong ảnh *(R3)*, và hàng `an_danh` có `A = B = ` hằng *(R4)*. Bài tấn
công từ điển *(≥ 200 viết tắt cùng hình dạng, dữ liệu TỔNG HỢP)* đòi **0** chuỗi khôi phục được.

⛔ Bài ở đây ⛔ nối kho, ⛔ đọc mạng: công cụ là hàm thuần trên tệp.
"""
from __future__ import annotations

import ast
import copy
import importlib.util
import json
import os
import pathlib
import random
import re
import string
import subprocess
import sys
from datetime import date

import pytest

from fls.adapters.mapping_master import DongMM, TRUONG, tom_tat
from fls.adapters.pm_join import PM_COT_RIENG_TU
from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
THU_MUC_KHUON = GOC / "tools" / "khuon_dong_bang"
CAU_HINH = GOC / "tests" / "fixture" / "cau_hinh"
ANH_ATL = CAU_HINH / "atl_cay.json"
ANH_MM = CAU_HINH / "mapping_master_cfg.json"
ANH_CDT = CAU_HINH / "cdt_correct.json"

#: `mong` khai ĐỘC LẬP ở bài *(Đ5)* — căn cứ: ISP Step 10 · `WO-106` ⑪ · đo của orchestrator 16/11.
MONG_ATL = 74          # dòng MÃ của cây ATL
MONG_NHOM_ATL = 6      # dòng tiêu đề nhóm
MONG_MM = 73           # mã hd của doc_cot
MONG_CDT = 13          # dòng có dữ liệu (vùng đọc BR11:BS32, biên dư sau dòng 23)

#: ⭐ Cây HD của AP v3.1.2 §3.2.5 — chép từ bảng *"nhóm · cấp L1 → L4"*, THỨ TỰ như AP. Đây là
#: phép so ĐỘC LẬP với khuôn *(khuôn suy nhóm/thứ tự từ sheet; bài đọc từ AP)*.
CAY_AP: dict[str, tuple[str, ...]] = {
    "HDO": ("GI", "OPC", "CAC", "MAC", "OMC", "MC", "OTMC", "COT", "COS", "PS", "API", "SC",
            "LC", "DC", "CSO", "GAC", "OFR", "GAH", "BRC", "HCC", "REC", "BON", "BUT", "OPO",
            "CXA", "OGA", "CDC", "CXP", "CXI", "OSF", "FNS", "CIO", "CXB", "CXO", "ITE", "CFI",
            "LMN", "OMN"),
    "HDH": ("NIS", "INT", "PIT", "COM"),
    "HDAP": ("DEP",),
    "HDT": ("NB",),
    "HDC": ("TAC", "CIT", "AR", "CP1.1 (PL2)", "CP1.2", "CP2", "CP3", "EBITDA", "EBIT", "EBT",
            "NP", "NPC", "NCF", "NCFO", "CRO", "COO", "NCFI", "CRI", "COI", "NCFF", "CRF", "COF",
            "CFO"),
    "HDCI": ("PL2", "PL3", "PL4", "PL5", "PL6", "PL7", "PL8"),
}

#: Đo 28/08 trên nguồn, ghi ở docstring `fls/adapters/mapping_master.py` ⓒ ⓓ ⓔ ⓕ — phép so ĐỘC
#: LẬP với ảnh *(ảnh 16/11 phải ra đúng các số đã đo trước đó gần 3 tháng)*.
TOM_TAT_28_08 = {"ma": 73, "can_phan_bo": 23, "co_phuong_phap": 21, "method_rong": 52,
                 "co_coa1": 0, "co_coa2": 0}

#: Checksum ghim sau lượt đóng băng ĐẦU *(16/11 — ⚠ ⛔ khai trước như DT2: phép so độc lập của
#: DT3 là `CAY_AP` + `TOM_TAT_28_08`)*. Đổi ⇒ phải có lượt đóng băng mới + lý do.
CHECKSUM_ATL = "4c95ef974a3149ba"
CHECKSUM_MM = "4f7605e5cff581ec"
CHECKSUM_CDT = "994571a670e75cec"


# ── trợ thủ chung ─────────────────────────────────────────────────────────────

def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=60)


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _ghi(p: pathlib.Path, tho: dict) -> pathlib.Path:
    p.write_text(json.dumps(tho, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return p


def _dong_loi(err: str, dau: str) -> list[str]:
    return [d for d in err.splitlines() if d.startswith(dau)]


def _nap_cong_cu():
    """Nạp công cụ TRONG tiến trình *(để `monkeypatch` được `THU_MUC_KHUON`)* — như DT2."""
    spec = importlib.util.spec_from_file_location("dong_bang_sheet_bai_dt3", TOOL)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["dong_bang_sheet_bai_dt3"] = mod
    spec.loader.exec_module(mod)
    return mod


def _nap_khuon(ten: str):
    spec = importlib.util.spec_from_file_location(f"khuon_bai_dt3_{ten}", THU_MUC_KHUON / f"{ten}.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _chu(v):
    """Ô ảnh → giá trị: ô chữ `{"chu": s}` ⇒ `s`; ô số *(chuỗi chữ số)* ⇒ nguyên; rỗng ⇒ None."""
    return v["chu"] if isinstance(v, dict) else v


def _checksum_lai(anh: dict) -> str:
    """Tính lại bằng CHÍNH `AnhChup` — dòng chính + mọi dòng bảng phụ *(bọc `{"phu", "dong"}`)*."""
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


# ══ Giao kèo khuôn MỞ RỘNG *(DT3 — bài đòi sửa công cụ, `WO-106` AC-4)* ═══════════════════════
#
# Ba nguồn DT3 đều là bảng CHỮ *(mã · tên · ánh xạ)*, mà công cụ DT2 chỉ biết khoá `yyyymm` và đòi
# mọi ô cột chọn là SỐ *(ô chữ ⇒ "ô ⛔ số" ⇒ ĐỎ)*. Hai nguồn còn ⛔ ở hình `{cot, dong}`: cây ATL
# là hàng `{A, cap_cot, o}` phải SUY cha/cấp/nhóm; Mapping Master là lưới thô A…P phải đi qua
# `doc_cot`. ⇒ Bốn mục TUỲ CHỌN của giao kèo *(khuôn cũ ⛔ khai thì chạy y như cũ — ảnh `ix_fx`
# giữ từng byte, bài `test_DT2_B1_anh_IX_FX_TAI_TAO_…` canh)*:
#   KIEU_KHOA = "ma"      khoá CHỮ: ô chữ khác rỗng; trùng so sau khi gộp khoảng trắng
#   KIEU_COT  = {cột: "chu" | "chu?"}   cột CHỮ *(⛔ rỗng · được rỗng)*; cột ⛔ khai = "so" như cũ
#   chuan_bi(tho) -> {cot, dong, phu?, ghi_chu?}   bản thô hình dạng orchestrator → bảng công cụ
#   PHU_MONG  = {tên bảng phụ: số dòng mong}       Đ5 cho bảng phụ — khác ⇒ ĐỎ

KHUON_CHU = '''"""Khuôn GIẢ LẬP bảng CHỮ của bài thử DT3 — ⛔ dữ liệu thật."""
BANG = "GIA.CHU"
KHOA = "Ma"
KIEU_KHOA = "ma"
COT = ("Ten", "Cha", "So")
KIEU_COT = {"Ten": "chu", "Cha": "chu?"}
RA = "khong_bao_gio_ghi/gia_chu.json"


def thieu_lac(dong):
    return {"thieu": [], "lac": [], "dai": "giả lập"}
'''

KHUON_CB = '''"""Khuôn GIẢ LẬP có `chuan_bi` + bảng phụ — ⛔ dữ liệu thật."""
BANG = "GIA.CB"
KHOA = "ma"
KIEU_KHOA = "ma"
COT = ("ten", "dong_sheet")
KIEU_COT = {"ten": "chu"}
RA = "khong_bao_gio_ghi/gia_cb.json"
PHU_MONG = {"tieu_de": 1}


def chuan_bi(tho):
    dong, tieu_de = [], []
    for i, h in enumerate(tho["dong"], 1):
        if h["loai"] == "tieu_de":
            tieu_de.append({"nhan": h["nhan"], "dong_sheet": i})
        elif h["loai"] == "ma":
            ma, ten = h["nhan"].split(" | ", 1)
            dong.append([ma, ten, i])
        else:
            raise ValueError(f"dòng {i}: loại ⛔ biết")
    return {"cot": ["ma", "ten", "dong_sheet"], "dong": dong, "phu": {"tieu_de": tieu_de},
            "ghi_chu": "giả lập: tiêu đề ⇒ bảng phụ"}


def thieu_lac(dong):
    return {"thieu": [], "lac": [], "dai": "giả lập"}
'''


def _goc_khuon(tmp_path: pathlib.Path, **tep: str) -> pathlib.Path:
    thu_muc = tmp_path / "khuon"
    thu_muc.mkdir(exist_ok=True)
    (thu_muc / "__init__.py").write_bytes(b"")
    for ten, noi_dung in tep.items():
        (thu_muc / f"{ten}.py").write_text(noi_dung, encoding="utf-8")
    return thu_muc


def _tho(p: pathlib.Path, dong: list, cot: list | None = None) -> pathlib.Path:
    tho = {"nguon": "TỔNG HỢP · bài thử DT3 (⛔ số thật)", "doc_luc": "2026-03-09",
           "cach_doc": "tổng hợp trong bài thử"}
    if cot is not None:
        tho["cot"] = cot
    tho["dong"] = dong
    return _ghi(p, tho)


COT_CHU = ["Ma", "Ten", "Cha", "So"]
DONG_CHU = [["A1", "Một", None, 1], ["B2", "Hai", "A1", 2], ["C3", "Ba", "", 3]]

DONG_CB = [{"loai": "tieu_de", "nhan": "NHOM|Nhóm"}, {"loai": "ma", "nhan": "A | Một"},
           {"loai": "ma", "nhan": "B | Hai"}]


def test_GIAO_KEO_khoa_MA_va_cot_CHU_dong_bang_duoc_bang_chu(tmp_path, monkeypatch, capsys):
    """Bảng chữ sạch ⇒ exit 0: khoá `ma` là ô chữ, cột `chu` giữ `{"chu": …}`, cột `chu?` nhận ô
    rỗng *(`None` · `""`)*, cột ⛔ khai vẫn là SỐ. ĐỎ trước DT3: `KIEU_KHOA="ma"` ⛔ biết ⇒ exit 2."""
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon(tmp_path, gia_chu=KHUON_CHU))
    ra = tmp_path / "a.json"
    ma = mod.main(["gia_chu", str(_tho(tmp_path / "t.json", DONG_CHU, COT_CHU)), "--mong", "3",
                   "--ra", str(ra)])
    out = capsys.readouterr()
    assert ma == 0, (out.out[-1500:], out.err[-1500:])
    anh = _doc(ra)
    assert anh["kieu_khoa"] == "ma"
    assert [d["Ma"] for d in anh["dong"]] == [{"chu": "A1"}, {"chu": "B2"}, {"chu": "C3"}]
    assert [d["Cha"] for d in anh["dong"]] == [None, {"chu": "A1"}, {"chu": ""}]
    assert [d["So"] for d in anh["dong"]] == ["1", "2", "3"]
    assert (anh["trung"], anh["khoa_hong"], anh["o_rong"]) == ([], [], [])
    # Đ4 — mẫu số của từng phép đếm: ô rỗng trên cột ⛔ được rỗng (Ten + So), ô ⛔ số trên cột
    #   số (So), ô ⛔ chữ trên cột chữ (Ten + Cha)
    assert "ô rỗng: 0/6" in out.out and "ô ⛔ số: 0/3" in out.out and "ô ⛔ chữ: 0/6" in out.out


@pytest.mark.parametrize("sua, phai_noi", [
    pytest.param({(0, 0): ""}, "khoá hỏng 1", id="khoa_rong"),
    pytest.param({(0, 0): 5}, "khoá hỏng 1", id="khoa_so"),
    pytest.param({(1, 0): "A1 "}, "trùng 1", id="khoa_trung_sau_gop_khoang_trang"),
    pytest.param({(0, 1): "  "}, "ô rỗng 1/6", id="cot_chu_rong"),
    pytest.param({(0, 1): 7}, "ô ⛔ chữ 1/6", id="cot_chu_la_so"),
    pytest.param({(1, 2): 9}, "ô ⛔ chữ 1/6", id="cot_chu_duoc_rong_la_so"),
    pytest.param({(2, 3): "ba"}, "ô ⛔ số 1/3", id="cot_so_la_chu"),
])
def test_GIAO_KEO_bang_chu_DO_dung_ly_do(tmp_path, monkeypatch, capsys, sua, phai_noi):
    """Mỗi chốt của bảng chữ CẮN riêng *(bài học `DT2-R1-04`: chốt chạy đúng mà ⛔ bài canh)*:
    exit 1 · ảnh VẪN ghi đúng nguồn · lý do đúng chốt."""
    dong = copy.deepcopy(DONG_CHU)
    for (i, j), v in sua.items():
        dong[i][j] = v
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon(tmp_path, gia_chu=KHUON_CHU))
    ra = tmp_path / "a.json"
    ma = mod.main(["gia_chu", str(_tho(tmp_path / "t.json", dong, COT_CHU)), "--mong", "3",
                   "--ra", str(ra)])
    out = capsys.readouterr()
    assert ma == 1, (out.out[-1500:], out.err[-1500:])
    assert any(phai_noi in x for x in _doc(ra)["cong"]["ly_do"]), _doc(ra)["cong"]["ly_do"]


def _chay_cb(tmp_path, monkeypatch, capsys, dong, khuon=KHUON_CB, ra_ten="cb.json"):
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon(tmp_path, gia_cb=khuon))
    ra = tmp_path / ra_ten
    ma = mod.main(["gia_cb", str(_tho(tmp_path / f"t_{ra_ten}", dong)), "--mong", "2",
                   "--ra", str(ra)])
    return ma, ra, capsys.readouterr()


def test_GIAO_KEO_chuan_bi_dung_bang_tu_ban_tho_KHONG_co_cot_va_ghi_BANG_PHU(tmp_path, monkeypatch,
                                                                           capsys):
    """Bản thô ⛔ có `cot` *(hình dạng orchestrator, như cây ATL)* ⇒ `chuan_bi` dựng bảng; bảng phụ
    vào ảnh dưới `phu.<tên>` với `mong` · `so_dong` · dòng mang `thu_tu` và ô mã hoá như dòng
    chính; `ghi_chu` của khuôn vào `ghi_chu_khuon`; checksum PHỦ cả bảng phụ.
    ĐỎ trước DT3: bản thô thiếu `cot` ⇒ TỪ CHỐI exit 2."""
    ma, ra, out = _chay_cb(tmp_path, monkeypatch, capsys, DONG_CB)
    assert ma == 0, (out.out[-1500:], out.err[-1500:])
    anh = _doc(ra)
    assert [(_chu(d["ma"]), _chu(d["ten"]), d["dong_sheet"]) for d in anh["dong"]] == \
        [("A", "Một", "2"), ("B", "Hai", "3")]
    assert anh["phu"] == {"tieu_de": {"mong": 1, "so_dong": 1, "dong": [
        {"thu_tu": 1, "nhan": {"chu": "NHOM|Nhóm"}, "dong_sheet": "1"}]}}
    assert anh["ghi_chu_khuon"] == "giả lập: tiêu đề ⇒ bảng phụ"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh)
    assert "tieu_de 1/1" in out.out


def test_GIAO_KEO_checksum_DOI_khi_chi_BANG_PHU_doi(tmp_path, monkeypatch, capsys):
    """Đ5: bảng phụ mà ⛔ vào checksum thì sửa nó là IM LẶNG. Đổi MỘT nhãn tiêu đề ⇒ checksum đổi."""
    ma1, ra1, _ = _chay_cb(tmp_path, monkeypatch, capsys, DONG_CB, ra_ten="a.json")
    dong = copy.deepcopy(DONG_CB)
    dong[0]["nhan"] = "NHOM|Nhóm khác"
    ma2, ra2, _ = _chay_cb(tmp_path, monkeypatch, capsys, dong, ra_ten="b.json")
    assert (ma1, ma2) == (0, 0)
    assert _doc(ra1)["dong"] == _doc(ra2)["dong"]
    assert _doc(ra1)["checksum_noi_dung"] != _doc(ra2)["checksum_noi_dung"]


def test_GIAO_KEO_BANG_PHU_lech_mong_thi_DO(tmp_path, monkeypatch, capsys):
    """`PHU_MONG` là cổng Đ5 của bảng phụ — HAI tiêu đề khi mong MỘT ⇒ exit 1, ảnh vẫn ghi."""
    dong = DONG_CB + [{"loai": "tieu_de", "nhan": "NHOM2|Nhóm hai"}]
    ma, ra, out = _chay_cb(tmp_path, monkeypatch, capsys, dong)
    assert ma == 1, (out.out[-1500:], out.err[-1500:])
    assert "phụ `tieu_de` 2 dòng ≠ mong 1" in _doc(ra)["cong"]["ly_do"]


def test_GIAO_KEO_chuan_bi_ValueError_thi_TU_CHOI_exit_2_mot_dong_KHONG_ghi(tmp_path, monkeypatch,
                                                                          capsys):
    """Khuôn ⛔ hiểu bản thô *(`ValueError`)* = đầu vào ⛔ dùng được ⇒ exit 2, MỘT dòng nói tên
    khuôn + lời khuôn, ⛔ ghi gì."""
    dong = DONG_CB + [{"loai": "la", "nhan": "?"}]
    ma, ra, out = _chay_cb(tmp_path, monkeypatch, capsys, dong)
    assert ma == 2
    dong_loi = _dong_loi(out.err, "⛔ TỪ CHỐI")
    assert len(dong_loi) == 1 and "gia_cb" in dong_loi[0] and "dòng 4" in dong_loi[0], dong_loi
    assert not ra.exists()


@pytest.mark.parametrize("sua", [
    pytest.param(('"phu": {"tieu_de": tieu_de}', '"phu": {"tieu_de": tieu_de, "la": []}'),
                 id="bang_phu_KHONG_khai_o_PHU_MONG"),
    pytest.param(('return {"cot"', 'return len(None) or {"cot"'), id="no_TypeError"),
    pytest.param(('"dong": dong,', '"dong": 5,'), id="dong_KHONG_phai_danh_sach"),
])
def test_GIAO_KEO_chuan_bi_NO_hay_tra_SAI_HINH_thi_exit_3_KHONG_ghi(tmp_path, monkeypatch, capsys,
                                                                   sua):
    """Khuôn nổ / trả sai hình = lỗi LẬP TRÌNH của khuôn ⇒ exit 3 *(⛔ 1 = "ảnh đỏ đã ghi",
    ⛔ 2 = "đầu vào hỏng")*, đúng MỘT dòng `⛔ LỖI`, ⛔ ghi."""
    cu, moi = sua
    assert cu in KHUON_CB
    ma, ra, out = _chay_cb(tmp_path, monkeypatch, capsys, DONG_CB, khuon=KHUON_CB.replace(cu, moi))
    assert ma == 3, (out.out[-800:], out.err[-800:])
    assert len(_dong_loi(out.err, "⛔ LỖI")) == 1 and "gia_cb" in out.err
    assert not ra.exists()


def test_GIAO_KEO_BANG_PHU_mang_cot_RIENG_TU_thi_TU_CHOI(tmp_path, monkeypatch, capsys):
    """Soát `PM_COT_RIENG_TU` phủ cả tên cột của bảng phụ — ⛔ chỉ `cot` của bảng chính."""
    khuon = KHUON_CB.replace('{"nhan": h["nhan"], "dong_sheet": i}',
                             '{"nhan": h["nhan"], "Email  address": "x", "dong_sheet": i}')
    assert khuon != KHUON_CB
    ma, ra, out = _chay_cb(tmp_path, monkeypatch, capsys, DONG_CB, khuon=khuon)
    assert ma == 2
    assert "PM_COT_RIENG_TU" in _dong_loi(out.err, "⛔ TỪ CHỐI")[0]
    assert not ra.exists()


@pytest.mark.parametrize("cu, moi, phai_noi", [
    pytest.param('KIEU_COT = {"Ten": "chu", "Cha": "chu?"}', 'KIEU_COT = {"Ten": "van_ban"}',
                 "KIEU_COT", id="KIEU_COT_kieu_la"),
    pytest.param('KIEU_COT = {"Ten": "chu", "Cha": "chu?"}', 'KIEU_COT = {"Khong_co": "chu"}',
                 "KIEU_COT", id="KIEU_COT_cot_ngoai_COT"),
    pytest.param('RA = "khong_bao_gio_ghi/gia_chu.json"',
                 'RA = "khong_bao_gio_ghi/gia_chu.json"\nPHU_MONG = {"x": 1}', "PHU_MONG",
                 id="PHU_MONG_ma_KHONG_chuan_bi"),
    pytest.param('RA = "khong_bao_gio_ghi/gia_chu.json"',
                 'RA = "khong_bao_gio_ghi/gia_chu.json"\nchuan_bi = 5', "chuan_bi",
                 id="chuan_bi_KHONG_goi_duoc"),
])
def test_GIAO_KEO_muc_tuy_chon_SAI_thi_TU_CHOI_exit_2_luc_nap(tmp_path, monkeypatch, capsys, cu, moi,
                                                             phai_noi):
    """Mục tuỳ chọn khai sai ⇒ TỪ CHỐI LÚC NẠP *(một dòng nói tên khuôn + mục hỏng)* — ⛔ để nó
    rơi im lặng về mặc định."""
    assert cu in KHUON_CHU
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON",
                        _goc_khuon(tmp_path, gia_chu=KHUON_CHU.replace(cu, moi)))
    ra = tmp_path / "moi" / "a.json"
    assert mod.main(["gia_chu", str(_tho(tmp_path / "t.json", DONG_CHU, COT_CHU)), "--mong", "3",
                     "--ra", str(ra)]) == 2
    dong = _dong_loi(capsys.readouterr().err, "⛔ TỪ CHỐI")
    assert len(dong) == 1 and "gia_chu" in dong[0] and phai_noi in dong[0], dong
    assert not ra.parent.exists()


# ══ DT3-B1 · ba ảnh đã commit *(AC-1)* ═════════════════════════════════════════════════════════

def test_DT3_B1_anh_cay_ATL_74_dong_MA_6_NHOM_dung_cay_AP_3_2_5():
    """Cây ATL: **74** dòng mã · **6** nhóm · 1 dòng trống *(81 hàng đọc = 74 + 6 + 1, Đ4)* — và
    từng nhóm mang ĐÚNG các mã của AP v3.1.2 §3.2.5, ĐÚNG thứ tự *(phép so độc lập: khuôn suy nhóm
    từ dòng tiêu đề của sheet, bài đọc từ AP)*."""
    anh = _doc(ANH_ATL)
    assert (anh["bang"], anh["khuon"], anh["khoa"], anh["kieu_khoa"]) == \
        ("IX.HD", "atl_cay", "ma", "ma")
    dong = anh["dong"]
    assert anh["so_dong"] == len(dong) == MONG_ATL                       # dòng MÃ
    nhom = anh["phu"]["nhom"]
    assert nhom["mong"] == nhom["so_dong"] == len(nhom["dong"]) == MONG_NHOM_ATL  # tiêu đề nhóm
    assert [_chu(n["ma"]) for n in nhom["dong"]] == list(CAY_AP)
    trong = anh["phu"]["dong_trong"]["dong"]
    assert [d["dong_sheet"] for d in trong] == ["35"]                    # 1 dòng trống
    so_hang = len(dong) + len(nhom["dong"]) + len(trong)
    assert so_hang == 81 == 87 - 7 + 1                                   # hàng đọc A7:F87

    theo_nhom: dict[str, list[str]] = {}
    for d in dong:
        theo_nhom.setdefault(_chu(d["nhom"]), []).append(_chu(d["ma"]))
    assert {k: tuple(v) for k, v in theo_nhom.items()} == CAY_AP
    assert sum(len(v) for v in CAY_AP.values()) == MONG_ATL

    # dòng sheet tăng dần, ⛔ trùng giữa ba loại dòng — ảnh giữ ĐÚNG vị trí của sheet
    vi_tri = [int(d["dong_sheet"]) for d in dong + nhom["dong"] + trong]
    assert sorted(vi_tri) == list(range(7, 88))
    assert anh["cong"] == {"mong": MONG_ATL, "so_dong": MONG_ATL, "dat": True, "ly_do": []}
    assert (anh["trung"], anh["thieu"], anh["khoa_hong"], anh["o_rong"]) == ([], [], [], [])
    assert anh["ngay_dong_bang"] == "2026-11-17"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_ATL


def test_DT3_B1_cay_ATL_cha_va_cap_suy_tu_THUT_COT_dung_nhom():
    """`cha` suy từ thụt cột *(`cap_cot`)* TRONG nhóm: cấp 1 ⇒ ⛔ cha; cấp k > 1 ⇒ cha là dòng mã
    gần nhất PHÍA TRÊN có cấp k − 1, cùng nhóm. Đo trên nguồn 16/11: ⛔ dòng nào nhảy cấp ⇒ mọi
    `cap(cha) = cap − 1`. ⚠ Kiểm cha–con/chu trình là việc của C4 — bài này chỉ chứng minh ảnh
    ghi ĐÚNG quan hệ thụt cột của sheet."""
    anh = _doc(ANH_ATL)
    theo_ma = {_chu(d["ma"]): d for d in anh["dong"]}
    dem_cap = {k: 0 for k in "1234"}
    for d in anh["dong"]:
        dem_cap[d["cap"]] += 1
        cha = _chu(d["cha"])
        if d["cap"] == "1":
            assert cha is None, d
            continue
        c = theo_ma[cha]
        assert int(c["cap"]) == int(d["cap"]) - 1, d
        assert _chu(c["nhom"]) == _chu(d["nhom"]), d
        assert int(c["dong_sheet"]) < int(d["dong_sheet"]), d
    assert sum(dem_cap.values()) == MONG_ATL and all(dem_cap.values())  # đủ L1–L4
    # vài quan hệ đọc thẳng ở AP §3.2.5 (thụt lề)
    assert [_chu(theo_ma[m]["cha"]) for m in ("OMC", "COT", "OSF", "CXP", "CRO", "CFO")] == \
        ["MAC", "CAC", "CXI", "CDC", "NCFO", "NCFF"]
    assert _chu(theo_ma["CXA"]["cha"]) == "GAC"          # CXA ở GAC (sheet), ⛔ ở CDC


def test_DT3_B1_anh_Mapping_Master_73_ma_hd_la_DAU_RA_doc_cot():
    """Mapping Master: **73** mã `hd` = đầu ra `doc_cot` *(⛔ khuôn đọc thứ hai)* — kiểm bằng CHÍNH
    `tom_tat` của adapter trên dòng ảnh, so với số đã đo 28/08 *(docstring adapter)*."""
    anh = _doc(ANH_MM)
    assert (anh["bang"], anh["khuon"], anh["khoa"]) == ("IX.HD · IX.ORG", "mapping_master_cfg",
                                                        "hd_code")
    assert [anh["khoa"], *anh["cot"]] == [*TRUONG, "dong_sheet"]
    dong = anh["dong"]
    assert anh["so_dong"] == len(dong) == MONG_MM                        # mã hd của doc_cot
    mm = [DongMM(dong_sheet=int(d["dong_sheet"]), **{t: _chu(d[t]) for t in TRUONG})
          for d in dong]
    assert {k: v for k, v in tom_tat(mm).items() if k in TOM_TAT_28_08} == TOM_TAT_28_08
    assert len({m.hd_code for m in mm}) == MONG_MM and min(m.dong_sheet for m in mm) >= 7
    # hai định nghĩa (ATL ↔ MM) đóng băng NGUYÊN, ⛔ hoà giải (C12): MM ⛔ có NCF
    ma_mm = [m.hd_code.split(" | ")[0] for m in mm]
    ma_atl = [_chu(d["ma"]) for d in _doc(ANH_ATL)["dong"]]
    assert set(ma_atl) - set(ma_mm) == {"NCF"} and set(ma_mm) <= set(ma_atl)

    phu = anh["phu"]
    assert (phu["tho"]["so_dong"], phu["an_danh"]["so_dong"], phu["loai"]["so_dong"]) == (84, 7, 0)
    assert all(phu[k]["mong"] == phu[k]["so_dong"] for k in phu)
    assert anh["cong"] == {"mong": MONG_MM, "so_dong": MONG_MM, "dat": True, "ly_do": []}
    assert anh["ngay_dong_bang"] == "2026-11-17"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_MM


def test_DT3_B1_anh_CDT_Correct_13_dong_co_du_lieu():
    """CDT Correct: **13** = dòng CÓ DỮ LIỆU ở `BR11:BS23` *(⑪ — ⛔ 18: khoảng Ô của ISP/AP)*;
    khoá `cdt_nguon` ⛔ trùng; mọi `cdt1_chuan` là ô chữ ⛔ rỗng."""
    anh = _doc(ANH_CDT)
    assert (anh["bang"], anh["khuon"], anh["khoa"], anh["cot"]) == \
        ("IX.ORG", "cdt_correct", "cdt_nguon", ["cdt1_chuan"])
    dong = anh["dong"]
    assert anh["so_dong"] == len(dong) == MONG_CDT                      # dòng có dữ liệu
    nguon = [_chu(d["cdt_nguon"]) for d in dong]
    assert len(set(nguon)) == MONG_CDT
    chuan = {_chu(d["cdt1_chuan"]) for d in dong}
    assert all(isinstance(d["cdt1_chuan"], dict) and d["cdt1_chuan"]["chu"].strip() for d in dong)
    assert {c.split(" | ")[0] for c in chuan} == {"SHQ2", "SHQ1", "CSM", "ASA", "CVL", "COR", "CAH"}
    assert anh["cong"] == {"mong": MONG_CDT, "so_dong": MONG_CDT, "dat": True, "ly_do": []}
    assert anh["ngay_dong_bang"] == "2026-11-17"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_CDT


# ── tái tạo bản thô ĐÚNG hình dạng orchestrator đưa, từ chính ảnh ──────────────────────────

def _meta(anh: dict) -> dict:
    return {"nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"], "cach_doc": anh["cach_doc"]}


def _tho_atl_tu_anh(anh: dict) -> dict:
    """LƯỚI Ô của SA *(`values`, `DT3-R1-03`)* theo dòng sheet: dòng mã ⇒ `MÃ | Tên` ở cột `cap`
    *(B=1…E=4)* và lặp ở `F`=5; tiêu đề nhóm ⇒ HAI ô `B`=mã · `C`=tên; dòng trống ⇒ `[0]`. Cột
    `A` *(số mUSD — ⛔ vào ảnh)* ⇒ `0`. ⛔ cần biên dư: vùng `nguon` *(A7:F90)* đã dư quá dòng cuối."""
    hang: dict[int, list] = {}
    for d in anh["dong"]:
        row = [0, "", "", "", "", ""]
        lab = f'{_chu(d["ma"])} | {_chu(d["ten"])}'
        row[int(d["cap"])] = lab          # B=1 … E=4
        row[5] = lab                      # F lặp nhãn
        hang[int(d["dong_sheet"])] = row
    for d in anh["phu"]["nhom"]["dong"]:
        hang[int(d["dong_sheet"])] = [0, _chu(d["ma"]), _chu(d["ten"])]
    for d in anh["phu"]["dong_trong"]["dong"]:
        hang[int(d["dong_sheet"])] = [0]
    dau = min(hang)
    assert sorted(hang) == list(range(dau, dau + len(hang)))
    return {**_meta(anh), "values": [hang[k] for k in sorted(hang)]}


_COT_HM = dict(zip(TRUONG, "HIJKLM"))      # đúng `fls.adapters.mapping_master.COT`


def _tho_mm_tu_anh(anh: dict) -> dict:
    """LƯỚI A…P *(16 cột, `values`)* theo dòng sheet: A · B · D–G từ bảng phụ `tho` *(ô ẩn danh giữ
    HẰNG `an_danh:tk_ca_nhan`)*; H–M từ dòng chính *(đầu ra doc_cot)*; C · N · O · P ⇒ rỗng. Hằng
    ẩn danh TỰ-ẩn-danh lại ⇒ tái tạo ra đúng từng byte."""
    n = max(int(d["dong_sheet"]) for d in anh["dong"] + anh["phu"]["tho"]["dong"])
    luoi: list[list] = [[None] * 16 for _ in range(n)]
    for d in anh["phu"]["tho"]["dong"]:
        for c in "ABDEFG":
            luoi[int(d["dong_sheet"]) - 1][ord(c) - 65] = _chu(d[c])
    for d in anh["dong"]:
        for t, c in _COT_HM.items():
            luoi[int(d["dong_sheet"]) - 1][ord(c) - 65] = _chu(d[t])
    return {**_meta(anh), "values": luoi}


def _tho_cdt_tu_anh(anh: dict) -> dict:
    """LƯỚI Ô `BR:BS` *(`values`)* theo thứ tự; biên dư nằm trong `nguon` *(BR11:BS32)*."""
    dong = sorted(anh["dong"], key=lambda d: d["thu_tu"])
    return {**_meta(anh),
            "values": [[_chu(d["cdt_nguon"]), _chu(d["cdt1_chuan"])] for d in dong]}


BA_ANH = [
    pytest.param("atl_cay", ANH_ATL, _tho_atl_tu_anh, MONG_ATL, id="atl_cay"),
    pytest.param("mapping_master_cfg", ANH_MM, _tho_mm_tu_anh, MONG_MM, id="mapping_master_cfg"),
    pytest.param("cdt_correct", ANH_CDT, _tho_cdt_tu_anh, MONG_CDT, id="cdt_correct"),
]


@pytest.mark.parametrize("khuon, anh_p, tai_tao, mong", BA_ANH)
def test_DT3_B1_anh_TAI_TAO_dung_tung_byte_tu_cong_cu(tmp_path, khuon, anh_p, tai_tao, mong):
    """Bản thô thật ⛔ commit ⇒ chứng minh ảnh đã commit LÀ đầu ra của công cụ: tái tạo bản thô
    *(hình dạng orchestrator)* từ ảnh, chạy lại ⇒ **đúng từng byte**. Ai sửa tay ảnh *(hay đổi
    khuôn làm đổi hình dạng ảnh)* mà ⛔ đóng băng lại là ĐỎ."""
    tho = _ghi(tmp_path / "tho.json", tai_tao(_doc(anh_p)))
    ra = tmp_path / anh_p.name
    kq = _chay(khuon, str(tho), "--mong", str(mong), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert ra.read_bytes() == anh_p.read_bytes()


# ══ DT3-B2 · ca phá: xoá MỘT dòng ở BẢN SAO ⇒ ĐỎ `N−1 ≠ N`, trả nguyên ⇒ xanh *(AC-2)* ═════════

#: Dòng sheet bị xoá ở bản sao — một LÁ của mỗi bảng *(⛔ đụng cấu trúc khác)*.
XOA = {"atl_cay": 14, "mapping_master_cfg": 13, "cdt_correct": 5}


@pytest.mark.parametrize("khuon, anh_p, tai_tao, mong", BA_ANH)
def test_DT3_B2_xoa_mot_dong_o_BAN_SAO_thi_DO_N_tru_1_khac_N_tra_nguyen_thi_XANH(
        tmp_path, khuon, anh_p, tai_tao, mong):
    """Mỗi ảnh MỘT ca phá riêng. Phá: bỏ một hàng của bản thô *(bản sao)* ⇒ exit 1, dòng `[ĐỎ]`
    nói `N−1 dòng ≠ mong N`, ảnh đỏ ghi ở `--ra` *(⛔ đè ảnh đã commit)*. Trả nguyên ⇒ exit 0,
    ảnh = ảnh đã commit từng byte."""
    goc = tai_tao(_doc(anh_p))
    pha = copy.deepcopy(goc)
    if khuon == "atl_cay":
        del pha["values"][XOA[khuon] - 7]              # hàng lưới = dòng sheet − 7
        assert pha["values"][XOA[khuon] - 7][5].startswith("COT |")   # hàng kế = COT (lá L3)
    else:
        del pha["values"][XOA[khuon] - 1]              # lưới / thứ tự tính từ dòng sheet 1
    truoc = anh_p.read_bytes()

    ra_do = tmp_path / "do.json"
    kq = _chay(khuon, str(_ghi(tmp_path / "pha.json", pha)), "--mong", str(mong),
               "--ra", str(ra_do))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert f"{mong - 1} dòng ≠ mong {mong}" in kq.stdout
    assert _doc(ra_do)["so_dong"] == mong - 1
    assert anh_p.read_bytes() == truoc, "ca phá đã đè ảnh đã commit"

    ra = tmp_path / "tra.json"
    kq = _chay(khuon, str(_ghi(tmp_path / "goc.json", goc)), "--mong", str(mong), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert "[ĐẠT]" in kq.stdout and ra.read_bytes() == truoc


# ── mọi CHỐT của hai khuôn có `chuan_bi` phải CẮN *(bài học `DT2-R1-04`)* ──────────────────────
#
# Bản thô tái tạo từ ảnh ⇒ phá MỘT chỗ ⇒ đòi đúng mã thoát + đúng lý do. Chỉ số hàng của cây ATL:
# hàng i của bản thô = dòng sheet i + 7 *(0 = tiêu đề `HDO` · 1 = `GI` · 28 = dòng trống ·
# 47 = tiêu đề `HDT` · 48 = `NB`)*.

def _xoa(i):
    return lambda t: t["values"].pop(i)


# Chỉ số hàng lưới của cây ATL: hàng i = dòng sheet i + 7 *(0 = tiêu đề `HDO` · 1 = `GI` ·
# 28 = dòng trống · 47 = tiêu đề `HDT` · 48 = `NB`)*. Ô: A=0 · B=1 … E=4 · F=5.
ATL_CHOT = [
    pytest.param(lambda t: t.update(nguon=t["nguon"].replace("!A7:F90", "!B7:F90")), 2, "vùng",
                 id="vung_KHONG_bat_dau_cot_A"),
    pytest.param(lambda t: t.update(nguon=t["nguon"].replace("!A7:F90", "!A7:F87")), 2,
                 "dư hàng", id="bien_du_vua_khit_du_lieu"),
    pytest.param(lambda t: t["values"][10].append("x"), 2, "≤ 6 ô", id="hang_qua_6_cot_A_F"),
    pytest.param(lambda t: t["values"][1].__setitem__(2, t["values"][1][1]), 2, "dạng nào",
                 id="dong_ma_hai_nhan"),
    pytest.param(lambda t: t["values"][1].__setitem__(5, "KHAC"), 2, "ô F",
                 id="F_KHONG_lap_nhan"),
    pytest.param(lambda t: (t["values"][1].__setitem__(1, "GI | "),
                            t["values"][1].__setitem__(5, "GI | ")), 2, "thiếu mã hoặc tên",
                 id="dong_ma_thieu_ten"),
    pytest.param(lambda t: t["values"].insert(0, [0, "XX | Gia lap", "", "", "", "XX | Gia lap"]),
                 2, "TRƯỚC tiêu đề nhóm", id="dong_ma_truoc_nhom_dau"),
    pytest.param(lambda t: t["values"].__setitem__(47, [0, "HDX", "HD gia lap"]), 1, "⛔ đo được",
                 id="nhom_KHONG_khai_o_NHOM"),
    pytest.param(_xoa(48), 1, "thiếu 2", id="nhom_khai_ma_0_dong_ma"),
    pytest.param(lambda t: t["values"].__setitem__(28, [0, "HDO", "HD Original"]), 1,
                 "phụ `nhom` 7 dòng ≠ mong 6", id="them_mot_tieu_de_nhom"),
    # `DT3-R2-03`ⓑ: tiêu đề nhóm đòi ô `C` *(tên)*. Xoá `C` ⇒ hàng B-only ⇒ "khác" (rác). ĐỎ trên
    # M18 *(bỏ đòi ô C)*: hàng B-only bị coi là tiêu đề nhóm ten=None ⇒ nhận, exit 0.
    pytest.param(lambda t: t["values"][0].__setitem__(2, ""), 2, "dạng nào",
                 id="tieu_de_nhom_thieu_o_C_ten"),
]


@pytest.mark.parametrize("pha, exit_mong, phai_noi", ATL_CHOT)
def test_KHUON_atl_cay_moi_chot_CAN(tmp_path, pha, exit_mong, phai_noi):
    """Bố cục lạ ⇒ TỪ CHỐI *(exit 2, ⛔ ghi — khuôn ⛔ đoán)*; nhóm/cấp lệch khai ⇒ ĐỎ *(exit 1)*."""
    tho = _tho_atl_tu_anh(_doc(ANH_ATL))
    pha(tho)
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("atl_cay", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_ATL),
               "--ra", str(ra))
    assert kq.returncode == exit_mong, (kq.stdout[-1200:], kq.stderr[-1200:])
    if exit_mong == 2:
        dong = _dong_loi(kq.stderr, "⛔ TỪ CHỐI")
        assert len(dong) == 1 and "atl_cay" in dong[0] and phai_noi in dong[0], dong
        assert not ra.parent.exists()
    else:
        assert any(phai_noi in x for x in _doc(ra)["cong"]["ly_do"]), _doc(ra)["cong"]["ly_do"]


def test_KHUON_atl_cay_tieu_de_nhom_XOA_ngan_cha_KHONG_vuot_sang_nhom_truoc(tmp_path):
    """Dòng mã đầu nhóm ở cấp > 1 ⇒ `cha = null` *(gốc mới)*, ⛔ là dòng L1 cuối của nhóm TRƯỚC.
    ⚠ Dữ liệu thật: mọi nhóm mở bằng dòng L1 ⇒ ⛔ bài này thì đột biến "bỏ xoá ngăn" SỐNG. Phá:
    `NIS` *(dòng đầu `HDH`)* lên cột L2 — đổi bố cục cấp ⇒ cổng ĐỎ *(`DT3-R1-06`)*, nhưng ảnh vẫn
    ghi ở `--ra` và GHI ĐÚNG `cha = null`."""
    tho = _tho_atl_tu_anh(_doc(ANH_ATL))
    assert tho["values"][41][5].startswith("NIS |") and tho["values"][40][1] == "HDH"
    tho["values"][41][2] = tho["values"][41][1]        # nhãn NIS: cột B (L1) → C (L2)
    tho["values"][41][1] = ""
    ra = tmp_path / "a.json"
    kq = _chay("atl_cay", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_ATL),
               "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1200:], kq.stderr[-1200:])   # cấp L1/L2 lệch mong
    nis = next(d for d in _doc(ra)["dong"] if _chu(d["ma"]) == "NIS")
    assert (nis["cap"], nis["cha"], _chu(nis["nhom"])) == ("2", None, "HDH")


def test_GIAO_KEO_ban_tho_CO_cot_RIENG_TU_thi_TU_CHOI_TRUOC_chuan_bi(tmp_path, monkeypatch, capsys):
    """Quyết định ④ của DT2 giữ cho khuôn có `chuan_bi`: bản thô mang `cot` có cột riêng tư ⇒
    TỪ CHỐI **trước** khi khuôn đọc giá trị — kể cả khi `chuan_bi` ⛔ chọn cột ấy *(khuôn giả lập
    ⛔ đọc `cot`)*."""
    mod = _nap_cong_cu()
    monkeypatch.setattr(mod, "THU_MUC_KHUON", _goc_khuon(tmp_path, gia_cb=KHUON_CB))
    ra = tmp_path / "a.json"
    tho = _tho(tmp_path / "t.json", DONG_CB, cot=["loai", "nhan", "Email Address"])
    assert mod.main(["gia_cb", str(tho), "--mong", "2", "--ra", str(ra)]) == 2
    assert "PM_COT_RIENG_TU" in _dong_loi(capsys.readouterr().err, "⛔ TỪ CHỐI")[0]
    assert not ra.exists()


def _gan(i: int, j: int, v):
    def f(t):
        t["values"][i][j] = v
    return f


MM_CHOT = [
    pytest.param(lambda t: t.update(nguon=t["nguon"].replace("!A1:P120", "!A2:P120")), 2, "!A1:",
                 id="vung_KHONG_bat_dau_A1"),
    pytest.param(_gan(10, 0, 5), 2, "chuỗi/rỗng", id="o_KHONG_phai_chuoi"),
    pytest.param(lambda t: t["values"][10].append("x"), 2, "≤ 16 ô", id="hang_qua_16_cot_A_P"),
    pytest.param(_gan(2, 0, "Bank"), 2, "tiêu đề", id="tieu_de_A_B_doi"),
    pytest.param(_gan(1, 1, "LE"), 2, "tiêu đề", id="dong_2_A_B_co_o"),
    pytest.param(lambda t: t["values"][12].__setitem__(7, t["values"][11][7]), 1,
                 "phụ `loai` 1 dòng ≠ mong 0", id="ma_hd_TRUNG_doc_cot_loai"),
]


@pytest.mark.parametrize("pha, exit_mong, phai_noi", MM_CHOT)
def test_KHUON_mapping_master_cfg_moi_chot_CAN(tmp_path, pha, exit_mong, phai_noi):
    """Bố cục lạ *(vùng ⛔ từ A1 · ô ⛔ chuỗi · hàng quá A…P · ô tiêu đề A:B đổi)* ⇒ TỪ CHỐI —
    ⛔ để một tên lọt qua vùng "tiêu đề"; mã `hd` trùng ⇒ `doc_cot` loại ⇒ ĐỎ."""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    pha(tho)
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("mapping_master_cfg", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_MM),
               "--ra", str(ra))
    assert kq.returncode == exit_mong, (kq.stdout[-1200:], kq.stderr[-1200:])
    if exit_mong == 2:
        dong = _dong_loi(kq.stderr, "⛔ TỪ CHỐI")
        assert len(dong) == 1 and "mapping_master_cfg" in dong[0] and phai_noi in dong[0], dong
        assert not ra.parent.exists()
    else:
        assert any(phai_noi in x for x in _doc(ra)["cong"]["ly_do"]), _doc(ra)["cong"]["ly_do"]


CDT_CHOT = [
    pytest.param(_gan(4, 1, ""), "ô rỗng 1/13", id="cdt1_chuan_RONG_la_duong_roi_ve_SHQ2"),
    pytest.param(_gan(4, 1, 7), "ô ⛔ chữ 1/13", id="cdt1_chuan_la_SO"),
    pytest.param(_gan(4, 0, "SHQ2 |  Headquarters2 "), "trùng 1", id="cdt_nguon_TRUNG_sau_gop"),
    pytest.param(_gan(4, 0, "  "), "khoá hỏng 1", id="cdt_nguon_RONG"),
]


@pytest.mark.parametrize("pha, phai_noi", CDT_CHOT)
def test_KHUON_cdt_correct_moi_chot_CAN(tmp_path, pha, phai_noi):
    """`cdt1_chuan` rỗng là ĐÚNG đường AP §3.2.4 gọi tên *("CDT lạ rơi im lặng về SHQ2")* ⇒ cổng
    ĐỎ, ⛔ ghi nhận. ⚠ Thiếu bài này thì đột biến `KIEU_COT = {"cdt1_chuan": "chu?"}` SỐNG
    *(đo: 124/124 xanh)*."""
    tho = _tho_cdt_tu_anh(_doc(ANH_CDT))
    pha(tho)
    ra = tmp_path / "a.json"
    kq = _chay("cdt_correct", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_CDT),
               "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1200:], kq.stderr[-1200:])
    assert any(phai_noi in x for x in _doc(ra)["cong"]["ly_do"]), _doc(ra)["cong"]["ly_do"]


# ══ AC-3 · ⛔ PII — máy quét, có ca phá ═══════════════════════════════════════════════════════

def _chuan(ten: str) -> str:
    return " ".join(str(ten).split()).casefold()


#: Tên cột CẤM mang vào ảnh: bản đen của kho *(`PM_COT_RIENG_TU`)* + hai cột PII của sổ mà
#: lời giao DT3 nêu *(`Diễn giải` · `Số chứng từ`)*.
CAM_COT = {_chuan(c) for c in PM_COT_RIENG_TU} | {_chuan("Diễn giải"), _chuan("Số chứng từ")}
_EMAIL = re.compile(r"[^\s@]+@[^\s@]+\.[A-Za-z]{2,}")
_TU = re.compile(r"[0-9A-Za-zÀ-ỹ]+")


def _di(x, khoa: list[str], chuoi: list[str]) -> None:
    if isinstance(x, dict):
        for k, v in x.items():
            khoa.append(k)
            _di(v, khoa, chuoi)
    elif isinstance(x, list):
        for v in x:
            _di(v, khoa, chuoi)
    elif isinstance(x, str):
        chuoi.append(x)


#: Mã băm cũ *(`DT3-R1-01`)* — dạng CÓ TIỀN TỐ `sha256_16:`; ảnh/mã MỚI ⛔ được chứa nữa. ⚠ ⛔
#: quét hex-16 TRẦN toàn ảnh: `checksum_noi_dung` là hex-16 hợp lệ *(Đ4 — đếm nhầm vật)*.
_MA_BAM = re.compile(r"sha256_16:[0-9a-f]{16}")
#: Hex-16 TRẦN — chỉ soát trong ô `A·B` của `phu.tho` *(chỗ từng băm; chặn hồi quy băm ⛔ tiền tố)*.
_HEX16 = re.compile(r"(?<![0-9a-fA-Z]):?[0-9a-f]{16}$")


def _bam_con_sot(anh: dict) -> set[str]:
    """Mọi chuỗi còn giống MÃ BĂM cũ *(có tiền tố `sha256_16:`)* trong ảnh *(mong rỗng)*."""
    khoa, chuoi = [], []
    _di(anh, khoa, chuoi)
    return {s for s in chuoi if _MA_BAM.search(s)}


def quet_pii(anh: dict, km) -> tuple[list[str], dict[str, int]]:
    """→ (vi phạm, mẫu số). Bốn luật *(`DT3-R1-01` sửa R3 · R4)*:
      R1 ⛔ khoá/tên cột nào *(mọi tầng + `cot` · `cot_khong_chon` · `khoa`)* thuộc `CAM_COT`;
      R2 ⛔ chuỗi nào dạng email;
      R3 ⛔ chuỗi nào dạng `sha256_16:`/hex-16 *(ảnh giả danh hoá ⇒ ⛔ còn mã băm — muối công khai
         băm được là đảo được)*;
      R4 *(chỉ Mapping Master)* bảng phụ `tho` từ dòng `DONG_DAU_LE`: cột `B` *(LE)* ∈ pháp nhân
         đã khai HOẶC = hằng `AN_DANH`; `B` = hằng thì `A` cũng = hằng *(tên người ở đuôi tên
         sheet của `A`)*."""
    khoa, chuoi = [], []
    _di(anh, khoa, chuoi)
    ten_cot = khoa + [anh.get("khoa", "")] + list(anh.get("cot", [])) \
        + list(anh.get("cot_khong_chon", []))
    loi = [f"R1 cột cấm `{k}`" for k in ten_cot if _chuan(k) in CAM_COT]
    loi += ["R2 chuỗi dạng email" for s in chuoi + khoa if _EMAIL.search(s)]
    loi += [f"R3 chuỗi dạng mã băm (dài {len(s)})" for s in chuoi + khoa if _MA_BAM.search(s)]
    so_r4 = 0
    if anh.get("khuon") == "mapping_master_cfg":
        for d in anh["phu"]["tho"]["dong"]:
            if int(d["dong_sheet"]) < km.DONG_DAU_LE:
                continue
            a, b = _chu(d["A"]), _chu(d["B"])
            if b is None:
                continue
            so_r4 += 1
            # R3 phạm vi phu.tho: ô A·B hex-16 trần (băm ⛔ tiền tố) cũng là mã băm
            loi += [f"R3 ô {c} dòng {d['dong_sheet']} dạng hex-16" for c, x in (("A", a), ("B", b))
                    if isinstance(x, str) and _HEX16.search(x)]
            if b == km.AN_DANH:
                if a != km.AN_DANH:
                    loi.append(f"R4 dòng {d['dong_sheet']}: B ẩn danh mà A ⛔ ẩn danh")
            elif b.strip() not in km.LE_PHAP_NHAN:
                loi.append(f"R4 dòng {d['dong_sheet']}: B ⛔ thuộc pháp nhân đã khai, ⛔ ẩn danh")
    return loi, {"khoa": len(ten_cot), "chuoi": len(chuoi), "r4": so_r4}


@pytest.fixture(scope="module")
def km():
    return _nap_khuon("mapping_master_cfg")


def test_AC3_ba_anh_quet_PII_bang_0_tren_mau_so_KHAC_0(km):
    """Ba ảnh ⇒ 0 vi phạm. Đ3: mẫu số phải > 0 *(chuỗi quét · hàng LE của MM)* — và ⛔ CÒN mã
    băm nào *(`DT3-R1-01`: ảnh cũ có 14, mới 0)*."""
    anh = [_doc(p) for p in (ANH_ATL, ANH_MM, ANH_CDT)]
    assert set().union(*(_bam_con_sot(a) for a in anh)) == set()      # ⛔ còn mã băm
    for a in anh:
        loi, mau = quet_pii(a, km)
        assert loi == [], (a["khuon"], loi)
        assert mau["khoa"] > 0 and mau["chuoi"] > 0, (a["khuon"], mau)
    assert quet_pii(anh[1], km)[1]["r4"] == 76                        # dòng 4…79 có LE
    assert _doc(ANH_MM)["phu"]["an_danh"]["so_dong"] == 7


def _them_hang_gia_lap(km, tmp_path) -> tuple[pathlib.Path, str]:
    """Lưới Mapping Master tái tạo + MỘT hàng A:B mang LE ⛔ khai *(giá trị TỔNG HỢP, ⛔ tên
    thật)* ở dòng 80 *(đang trống ở A:B)*."""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    gia = "GIALAPX"
    assert gia not in km.LE_PHAP_NHAN
    tho["values"][79][0] = f"R | 99999999_PO USD_{gia}"
    tho["values"][79][1] = gia
    return _ghi(tmp_path / "tho_gia.json", tho), gia


def test_R1_01_hang_ca_nhan_KHONG_dao_nguoc_duoc_bang_tu_dien_200_ten(km, tmp_path):
    """`DT3-R1-01` *(CHẶN — bia của `2a31f76`)*: hàng TK cá nhân TỔNG HỢP `GIALAPX` ⇒ đóng băng ⇒
    kẻ có repo + từ điển 200 viết tắt ⛔ khôi phục được chuỗi rõ từ ảnh *(muối công khai ⇒ đảo
    được — ĐỎ trên `5a96cd9`)*. Sau sửa: khuôn ⛔ có `bam`/`MUOI`, ảnh dùng HẰNG ⇒ 0 khôi phục,
    và ô A·B của hàng ấy = hằng, `GIALAPX` ⛔ ở đâu trong ảnh."""
    tho, gia = _them_hang_gia_lap(km, tmp_path)
    ra = tmp_path / "mm.json"
    _chay("mapping_master_cfg", str(tho), "--mong", str(MONG_MM), "--ra", str(ra))
    random.seed(108)
    tu_dien = {gia} | {"".join(random.choices(string.ascii_uppercase, k=random.choice((5, 6, 7))))
                       for _ in range(199)}
    ma_trong_anh = _bam_con_sot(_doc(ra))                 # mong rỗng (⛔ còn mã băm)
    bam = getattr(km, "bam", lambda v: None)              # sau sửa: khuôn ⛔ có `bam`
    dao_duoc = sorted(t for t in tu_dien if bam(t) is not None and bam(t) in ma_trong_anh)
    assert dao_duoc == [], f"{len(dao_duoc)} chuỗi rõ khôi phục được từ ảnh"
    assert not hasattr(km, "bam") and not hasattr(km, "MUOI") and not hasattr(km, "MA_BAM")
    assert gia not in ra.read_text(encoding="utf-8")
    hang = next(d for d in _doc(ra)["phu"]["tho"]["dong"] if d["dong_sheet"] == "80")
    assert _chu(hang["A"]) == _chu(hang["B"]) == km.AN_DANH


def test_AC3_khuon_AN_DANH_moi_LE_KHONG_khai_dong_khi_la_va_cong_DO_8_khac_7(km, tmp_path):
    """Khuôn đóng KHI LẠ: LE ⛔ có trong `LE_PHAP_NHAN` ⇒ ẩn danh A + B, ⛔ cần ai khai trước tên
    người. Hàng thứ 8 ⇒ bảng phụ `an_danh` 8 ≠ mong 7 ⇒ cổng ĐỎ *(người phải nhìn)*; chuỗi rõ
    ⛔ có + ⛔ mã băm nào trong ảnh đỏ."""
    tho, gia = _them_hang_gia_lap(km, tmp_path)
    ra = tmp_path / "mm_do.json"
    kq = _chay("mapping_master_cfg", str(tho), "--mong", str(MONG_MM), "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert "phụ `an_danh` 8 dòng ≠ mong 7" in kq.stdout
    assert gia not in ra.read_text(encoding="utf-8") and gia not in kq.stdout + kq.stderr
    assert _bam_con_sot(_doc(ra)) == set()


@pytest.mark.parametrize("pha, luat", [
    pytest.param(lambda a: a["dong"][0].update({"Email Address": None}), "R1",
                 id="R1_khoa_Email_Address"),
    pytest.param(lambda a: a["cot"].append("  Diễn   giải "), "R1", id="R1_cot_Dien_giai"),
    pytest.param(lambda a: a["dong"][0].update({"ten": {"chu": "lien.he@vi-du.invalid"}}),
                 "R2", id="R2_email"),
    pytest.param(lambda a: a["dong"][3].update({"ten": {"chu": "sha256_16:0123456789abcdef"}}),
                 "R3", id="R3_ma_bam_lot_vao_anh"),
])
def test_AC3_ca_pha_may_quet_CAN_tung_luat(km, pha, luat):
    """Mỗi luật của máy quét được chứng minh CẮN *(Đ5)* trên bản sao ảnh cây ATL."""
    anh = copy.deepcopy(_doc(ANH_ATL))
    assert quet_pii(anh, km)[0] == []
    pha(anh)
    loi = quet_pii(anh, km)[0]
    assert loi and all(x.startswith(luat) for x in loi), loi


def test_AC3_ca_pha_R4_LE_ro_KHONG_khai_trong_anh_Mapping_Master(km):
    """R4 cắn khi một ô B đã ẩn danh bị thay bằng chữ RÕ ⛔ thuộc pháp nhân đã khai, hay A của
    hàng ẩn danh bị trả về rõ."""
    anh = copy.deepcopy(_doc(ANH_MM))
    hang = next(d for d in anh["phu"]["tho"]["dong"] if _chu(d["B"]) == km.AN_DANH)
    hang["B"] = {"chu": "GIALAPX"}
    assert any(x.startswith("R4") and "B ⛔ thuộc" in x for x in quet_pii(anh, km)[0])
    anh = copy.deepcopy(_doc(ANH_MM))
    hang = next(d for d in anh["phu"]["tho"]["dong"] if _chu(d["B"]) == km.AN_DANH)
    hang["A"] = {"chu": "R | 99999999_PO USD_GIALAPX"}
    assert any("A ⛔ ẩn danh" in x for x in quet_pii(anh, km)[0])


def test_R1_02_cdt_correct_vung_doc_KHONG_du_hang_sau_du_lieu_thi_TU_CHOI(tmp_path):
    """`DT3-R1-02`: vùng đọc khít dữ liệu *(`BR11:BS23` cho 13 hàng về)* ⇒ dòng CDT thêm ở `BR24`
    ⛔ bao giờ tới công cụ. Đòi: `cuoi` của vùng > dòng dữ liệu cuối ⇒ TỪ CHỐI exit 2
    *(ĐỎ trên `5a96cd9`: exit 0 `[ĐẠT]`)*."""
    tho = _tho_cdt_tu_anh(_doc(ANH_CDT))
    tho["nguon"] = tho["nguon"].replace("!BR11:BS32", "!BR11:BS23")
    assert "!BR11:BS23" in tho["nguon"] and len(tho["values"]) == 13
    ra = tmp_path / "moi" / "c.json"
    kq = _chay("cdt_correct", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_CDT),
               "--ra", str(ra))
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-400:], kq.stderr[-400:])
    assert "dư hàng" in _dong_loi(kq.stderr, "⛔ TỪ CHỐI")[0]
    assert not ra.parent.exists()


def test_R1_03_atl_cay_nhan_LUOI_o_cua_sheet_ra_cung_74_dong(tmp_path):
    """`DT3-R1-03`: hợp đồng bản thô = LƯỚI Ô của SA. Tiêu đề nhóm ở sheet là HAI ô `B`=mã · `C`
    =tên — ⛔ chuỗi `MÃ|Tên`. Lưới ô ⇒ công cụ ra đúng 74 dòng, cùng `ma · cha · cap · nhom`
    *(ĐỎ trên `5a96cd9`: exit 2 `ba khoá A · cap_cot · o`)*."""
    anh = _doc(ANH_ATL)
    tho = _tho_atl_tu_anh(anh)                             # đã là lưới `values`
    assert "values" in tho and "dong" not in tho
    for row in tho["values"]:                             # ⛔ ô nào mang chuỗi `MÃ|Tên`
        for cell in row:
            assert not (isinstance(cell, str) and re.fullmatch(r"[A-Z][A-Z0-9]*\|\S.*", cell)), cell
    ra = tmp_path / "a.json"
    kq = _chay("atl_cay", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_ATL),
               "--ra", str(ra))
    assert kq.returncode == 0, kq.stderr[-400:]
    moi = _doc(ra)
    khoa = lambda a: [(_chu(d["ma"]), _chu(d["cha"]), d["cap"], _chu(d["nhom"])) for d in a["dong"]]
    assert khoa(moi) == khoa(anh) and len(moi["dong"]) == MONG_ATL


# ══ Vòng sửa sau R2 (KQ-109) ═════════════════════════════════════════════════════════════════

def test_R2_01_hang_chi_co_A_B_rong_VAN_duoc_an_danh(km):
    """`DT3-R2-01` *(NÊN SỬA)*: nhánh *"hàng chỉ có `A`, `B` rỗng"* của luật ẩn danh. Tài khoản PO
    cá nhân có thể chỉ điền `A` *(B rỗng)* — đuôi tên sheet của `A` mang tên NGƯỜI. Đột biến M22
    `(A≠∅ hoặc B≠∅)` → `(B≠∅)` bỏ qua hàng A-only ⇒ chuỗi rõ lọt vào ảnh. Dữ liệu TỔNG HỢP: lưới
    MM + hàng chỉ `A` ở dòng 80 *(A:B đang trống)* ⇒ `an_danh` +1 `cot=A`, `A` = hằng, chuỗi tổng
    hợp ⛔ ở đâu trong kết quả `chuan_bi`. *(ĐỎ trên đột biến M22 — R2 chứng minh phá lại.)*"""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    gia = "GIALAPONLYA"
    assert gia not in km.LE_PHAP_NHAN
    tho["values"][79][0] = f"R | 99999999_PO USD_{gia}"    # chỉ `A` (dòng sheet 80)
    assert not tho["values"][79][1]                        # `B` để RỖNG ⇒ nhánh A-only
    kq = km.chuan_bi(tho)
    moi = [d for d in kq["phu"]["an_danh"] if d["dong_sheet"] == 80]
    assert len(kq["phu"]["an_danh"]) == 8 and len(moi) == 1 and moi[0]["cot"] == "A", \
        kq["phu"]["an_danh"]
    hang = next(d for d in kq["phu"]["tho"] if d["dong_sheet"] == 80)
    assert hang["A"] == km.AN_DANH and hang["B"] is None
    khoa, chuoi = [], []
    _di(kq, khoa, chuoi)
    assert gia not in "\n".join(chuoi), "chuỗi rõ của hàng A-only lọt vào kết quả chuan_bi"


#: Ô dấu cấp `x` sẵn có ở MỖI cột `D·E·F·G` *(đo 17/11 từ ảnh)* — `(cột, dòng sheet, hàng lưới,
#: chỉ số cột 0-based)*. Tham số hoá để CẢ BỐN cột cùng được canh *(`DT3-R3-02`: chỉ canh `D` thì
#: đột biến `"DEFG"`→`"D"`/`"DEF"` sống — một chuỗi lạ ở `E·F·G` vẫn lọt vào ảnh thô)*.
_O_X_DG = [
    pytest.param("D", 7, 6, 3, id="cot_D"),
    pytest.param("E", 9, 8, 4, id="cot_E"),
    pytest.param("F", 10, 9, 5, id="cot_F"),
    pytest.param("G", 11, 10, 6, id="cot_G"),
]


@pytest.mark.parametrize("cot, dong_sheet, hang_i, cot_j", _O_X_DG)
def test_R2_02_cot_DG_chuoi_LA_ngoai_danh_sach_cho_phep_thi_TU_CHOI(
        tmp_path, cot, dong_sheet, hang_i, cot_j):
    """`DT3-R2-02` *(NÊN SỬA)* + `DT3-R3-02`: cột `D:G` của `phu.tho` chép THÔ. Thay MỘT ô `x` sẵn
    có ở TỪNG cột `D·E·F·G` bằng chuỗi LẠ *(số dòng ⛔ đổi — cổng `--mong`/`phu` ⛔ thấy, như thăm
    dò P4b của R2)* ⇒ khuôn đòi mỗi ô `D:G` ∈ danh sách giá trị đã đo 17/11 ⇒ TỪ CHỐI exit 2
    *(⛔ ghi ảnh)*. ĐỎ-trước *(⛔ danh sách)*: exit 0 `[ĐẠT]`, chuỗi lạ vào ảnh. Lời lỗi ⛔ mang giá
    trị ô *(nguồn CÓ tên người)*. Tham số `E·F·G` giết đột biến `"DEFG"`→`"D"` *(M3, chỉ canh `D`)*
    và `"DEFG"`→`"DEF"` *(M4, bỏ `G` — chỉ `cot_G` cắn)*."""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    assert tho["values"][hang_i][cot_j] == "x", (cot, dong_sheet)   # dấu cấp `x` của cột ấy
    gia = "CHUOILA_COTHE_TEN_NGUOI"
    tho["values"][hang_i][cot_j] = gia
    ra = tmp_path / "moi" / "mm.json"
    kq = _chay("mapping_master_cfg", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_MM),
               "--ra", str(ra))
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-600:], kq.stderr[-600:])
    dong = _dong_loi(kq.stderr, "⛔ TỪ CHỐI")
    assert len(dong) == 1 and "mapping_master_cfg" in dong[0] and "danh sách" in dong[0], dong
    assert not ra.parent.exists()
    assert gia not in kq.stdout + kq.stderr                # lời lỗi ⛔ in giá trị ô


def test_R2_03a_cdt_correct_vung_SAI_COT_khong_phai_BR_BS_thi_TU_CHOI(tmp_path):
    """`DT3-R2-03`ⓐ *(GHI NHẬN)*: khuôn CDT đòi vùng ĐÚNG cột `BR:BS`. Đột biến M17 *(bỏ kiểm
    cột)* ⇒ vùng cột KHÁC *(vd `BX:BY`)* lọt qua *(biên dư vẫn khớp)*. Đổi `nguon` sang
    `!BX11:BY32` ⇒ TỪ CHỐI exit 2 *(ĐỎ trên M17: exit 0)*."""
    tho = _tho_cdt_tu_anh(_doc(ANH_CDT))
    tho["nguon"] = tho["nguon"].replace("!BR11:BS32", "!BX11:BY32")
    ra = tmp_path / "moi" / "c.json"
    kq = _chay("cdt_correct", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_CDT),
               "--ra", str(ra))
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-400:], kq.stderr[-400:])
    assert "BR:BS" in _dong_loi(kq.stderr, "⛔ TỪ CHỐI")[0]
    assert not ra.parent.exists()


# ══ Vòng sửa sau R3 (KQ-110) ═════════════════════════════════════════════════════════════════

def test_R3_01_hang_chi_co_B_A_rong_VAN_duoc_an_danh(km):
    """`DT3-R3-01` *(NÊN SỬA)*: nhánh *"hàng chỉ có `B`, `A` rỗng"* của luật ẩn danh — đối xứng với
    `test_R2_01` *(hàng chỉ có `A`)*. Một LE ⛔ khai có thể chỉ điền `B` *(tên viết tắt NGƯỜI)* mà
    `A` *(số TK + tên)* còn trống. Đột biến M2 `(A≠∅ hoặc B≠∅)` → `(A≠∅)` bỏ nhánh `B` ⇒ hàng
    B-only ⛔ được ẩn danh ⇒ chuỗi rõ lọt vào ảnh. Dữ liệu TỔNG HỢP: lưới MM + hàng chỉ `B` ở dòng
    80 *(A:B đang trống)* ⇒ `an_danh` +1 `cot=B`, `B` = hằng, `A` vẫn None, chuỗi tổng hợp ⛔ ở đâu
    trong kết quả `chuan_bi`. *(ĐỎ trên M2 — R3 chứng minh phá lại.)*"""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    gia = "GIALAPONLYB"
    assert gia not in km.LE_PHAP_NHAN
    tho["values"][79][1] = gia                             # chỉ `B` (dòng sheet 80)
    assert not tho["values"][79][0]                        # `A` để RỖNG ⇒ nhánh B-only
    kq = km.chuan_bi(tho)
    moi = [d for d in kq["phu"]["an_danh"] if d["dong_sheet"] == 80]
    assert len(kq["phu"]["an_danh"]) == 8 and len(moi) == 1 and moi[0]["cot"] == "B", \
        kq["phu"]["an_danh"]
    hang = next(d for d in kq["phu"]["tho"] if d["dong_sheet"] == 80)
    assert hang["B"] == km.AN_DANH and hang["A"] is None
    khoa, chuoi = [], []
    _di(kq, khoa, chuoi)
    assert gia not in "\n".join(chuoi), "chuỗi rõ của hàng B-only lọt vào kết quả chuan_bi"


def test_R3_03_bien_duoi_DONG_DAU_LE_hang_dau_tien_duoc_an_danh(km):
    """`DT3-R3-03` *(GHI NHẬN)*: biên DƯỚI của luật ẩn danh = `DONG_DAU_LE` *(4)* — dòng dữ liệu
    `A:B` đầu tiên *(1…3 là tiêu đề)*. Đột biến M7 `r >= DONG_DAU_LE` → `r >= DONG_DAU_LE + 1` bỏ
    ĐÚNG dòng 4; trên dữ liệu thật dòng 4 là pháp nhân *(⛔ ẩn danh dù sao)* nên M7 sống. Dữ liệu
    TỔNG HỢP: thay `A:B` dòng 4 bằng LE ⛔ khai ⇒ dòng 4 PHẢI ẩn danh *(biên bao gồm chính nó)*.
    Trên M7 dòng 4 lọt ⇒ `B` còn chuỗi rõ ⇒ bài ĐỎ."""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    assert km.DONG_DAU_LE == 4
    gia = "GIALAPBIEN4"
    assert gia not in km.LE_PHAP_NHAN
    tho["values"][3][0] = f"R | 99999999_PO USD_{gia}"     # `A` dòng 4 (tổng hợp — ⛔ TK thật)
    tho["values"][3][1] = gia                              # `B` dòng 4 = LE ⛔ khai
    kq = km.chuan_bi(tho)
    moi = [d for d in kq["phu"]["an_danh"] if d["dong_sheet"] == 4]
    assert len(moi) == 1 and moi[0]["cot"] == "A·B", kq["phu"]["an_danh"]
    hang = next(d for d in kq["phu"]["tho"] if d["dong_sheet"] == 4)
    assert hang["A"] == km.AN_DANH and hang["B"] == km.AN_DANH, hang
    khoa, chuoi = [], []
    _di(kq, khoa, chuoi)
    assert gia not in "\n".join(chuoi), "chuỗi rõ của hàng biên (dòng 4) lọt vào kết quả chuan_bi"


#: Tệp MÃ SẢN XUẤT của DT3 — công cụ + ba khuôn *(bài THẢO LUẬN `MUOI`/băm trong chú thích ⇒
#: ⛔ quét token ở bài; ảnh quét bằng `_bam_con_sot`)*.
TEP_MA_DT3 = [TOOL, THU_MUC_KHUON / "atl_cay.py", THU_MUC_KHUON / "mapping_master_cfg.py",
              THU_MUC_KHUON / "cdt_correct.py"]


def test_AC3_tep_ma_va_anh_cua_DT3_KHONG_mang_ma_bam_muoi_hay_ham_bam():
    """`DT3-R1-01`: ⛔ muối / hàm băm / mã băm vào repo. Ảnh: `_bam_con_sot` = rỗng *(⛔ chuỗi
    `sha256_16:`)*. Mã sản xuất *(công cụ + 3 khuôn)*: 0 `MUOI`, 0 `def bam`, 0 `hashlib`. Mẫu
    số: tổng từ > 2.000. ⚠ `sha256` *(checksum qua `AnhChup`)* ĐƯỢC — ⛔ phải băm tên."""
    for p in (ANH_ATL, ANH_MM, ANH_CDT):
        assert _bam_con_sot(_doc(p)) == set(), p.name
    so_tu = 0
    for p in TEP_MA_DT3:
        assert p.is_file(), p
        van = p.read_text(encoding="utf-8")
        so_tu += len(_TU.findall(van))
        for cam in ("MUOI", "def bam", "hashlib"):
            assert cam not in van, (p.name, cam)
    assert so_tu > 2_000, so_tu


# ══ AC-4 · khuôn mới = tệp RIÊNG; công cụ ⛔ mang dữ liệu khuôn ════════════════════════════════

def _chuoi_trong_ma(p: pathlib.Path) -> set[str]:
    """Mọi hằng chuỗi của tệp `.py` TRỪ docstring *(như bài DT2 cùng tên)*."""
    cay = ast.parse(p.read_text(encoding="utf-8"))
    doc = set()
    for n in ast.walk(cay):
        if isinstance(n, (ast.Module, ast.FunctionDef, ast.ClassDef, ast.AsyncFunctionDef)) \
                and n.body and isinstance(n.body[0], ast.Expr) \
                and isinstance(n.body[0].value, ast.Constant):
            doc.add(id(n.body[0].value))
    return {n.value for n in ast.walk(cay)
            if isinstance(n, ast.Constant) and isinstance(n.value, str) and id(n) not in doc}


def test_AC4_ba_khuon_DT3_la_ba_TEP_RIENG_va_cong_cu_KHONG_mang_du_lieu_cua_chung():
    """Mỗi nguồn MỘT tệp `tools/khuon_dong_bang/<tên>.py`; công cụ tìm thấy cả ba *(cạnh `ix_fx`)*;
    và MÃ công cụ ⛔ mang tên bảng · khoá · đường ảnh · nhóm của khuôn nào."""
    co = _nap_cong_cu().danh_sach_khuon()
    for ten in ("atl_cay", "mapping_master_cfg", "cdt_correct", "ix_fx"):
        assert ten in co, (ten, co)
        assert (THU_MUC_KHUON / f"{ten}.py").is_file()
    lot = _chuoi_trong_ma(TOOL) & {
        "IX.HD", "IX.ORG", "IX.HD · IX.ORG", "hd_code", "cdt_nguon", "cdt1_chuan", "HDO",
        "tests/fixture/cau_hinh/atl_cay.json", "tests/fixture/cau_hinh/mapping_master_cfg.json",
        "tests/fixture/cau_hinh/cdt_correct.json", "Mapping Master", "sha256_16:"}
    assert lot == set(), f"công cụ mang dữ liệu khuôn DT3: {sorted(lot)}"


@pytest.mark.parametrize("ten, ra", [
    ("atl_cay", "tests/fixture/cau_hinh/atl_cay.json"),
    ("mapping_master_cfg", "tests/fixture/cau_hinh/mapping_master_cfg.json"),
    ("cdt_correct", "tests/fixture/cau_hinh/cdt_correct.json"),
])
def test_AC4_khuon_KHAI_duong_anh_va_qua_giao_keo_luc_nap(ten, ra):
    """Khuôn qua `nap_khuon` *(giao kèo — kể cả các mục tuỳ chọn)* và khai đúng đường ảnh."""
    kh = _nap_cong_cu().nap_khuon(ten)
    assert kh.ra == ra and kh.kieu_khoa == "ma"
    assert (GOC / ra).is_file()
