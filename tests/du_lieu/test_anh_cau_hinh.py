"""Ba ảnh nguồn `IX.HD` · `IX.ORG` *(ISP 3.1.2 · Step 10 · DT3 · `WO-106`)* — cây ATL · Mapping
Master · CDT Correct, đóng băng qua CHÍNH đường ống DT2 *(`tools/dong_bang_sheet.py`)*.

⭐ **Vì sao có tệp này.** Bước sau *(C4 cây HD · C8 IX.ORG · C12 dòng PL)* cần ba ẢNH đứng yên
của ba nguồn đang nằm ở sheet NOW, mỗi ảnh có checksum + một cổng khai `mong` *(Đ5)*:

    cây ATL       `'Report I PLA3 Y H Q M | PM + HR | ATL'!A7:F88` ⇒ 74 dòng MÃ · 6 nhóm
    Mapping Master `'Mapping Master'!A1:P120` *(RAW)*            ⇒ 73 mã `hd` *(đầu ra `doc_cot`)*
    CDT Correct   `'Report I H1000 Ledge … | For PL Report'!BR11:BS23` ⇒ 13 dòng

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

⛔⛔ **Riêng tư** *(AC-3)*. Mapping Master cột `A · B · O` có **7 hàng** mang tên viết tắt NGƯỜI
*(tài khoản PO cá nhân)*. Khuôn `mapping_master_cfg` BĂM chúng *(xem docstring khuôn)* — và ⛔
một tên nào nằm trong repo, kể cả bài này. ⇒ Bài quét tên ⛔ cần biết tên: nó băm MỌI chuỗi/từ
của ảnh *(và của các tệp mã DT3)* rồi so với các mã băm CÓ TRONG ảnh — chuỗi rõ của một giá trị
đã băm mà lọt ra chỗ khác thì băm của nó TRÙNG một mã băm ⇒ ĐỎ.

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
MONG_CDT = 13          # dòng có dữ liệu BR11:BS23

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
CHECKSUM_ATL = "77ca9d6c74f4254a"
CHECKSUM_MM = "e96f6d1a86a03320"
CHECKSUM_CDT = "30aea854bd879f6d"


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
    assert anh["ngay_dong_bang"] == "2026-11-16"
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
    assert (phu["tho"]["so_dong"], phu["bam"]["so_dong"], phu["loai"]["so_dong"]) == (84, 7, 0)
    assert all(phu[k]["mong"] == phu[k]["so_dong"] for k in phu)
    assert anh["cong"] == {"mong": MONG_MM, "so_dong": MONG_MM, "dat": True, "ly_do": []}
    assert anh["ngay_dong_bang"] == "2026-11-16"
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
    assert anh["ngay_dong_bang"] == "2026-11-16"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_CDT


# ── tái tạo bản thô ĐÚNG hình dạng orchestrator đưa, từ chính ảnh ──────────────────────────

def _meta(anh: dict) -> dict:
    return {"nguon": anh["nguon"], "doc_luc": anh["ngay_dong_bang"], "cach_doc": anh["cach_doc"]}


def _tho_atl_tu_anh(anh: dict) -> dict:
    """Hàng `{A, cap_cot, o}` theo dòng sheet: mã ⇒ `MÃ | Tên` ở cột cấp − 1; tiêu đề nhóm ⇒
    `MÃ|Tên` ở cột 0; dòng trống ⇒ `""`. Cột `A` *(số mUSD — ⛔ vào ảnh)* ⇒ `None`."""
    hang: dict[int, dict] = {}
    for d in anh["dong"]:
        hang[int(d["dong_sheet"])] = {"A": None, "cap_cot": int(d["cap"]) - 1,
                                      "o": f'{_chu(d["ma"])} | {_chu(d["ten"])}'}
    for d in anh["phu"]["nhom"]["dong"]:
        hang[int(d["dong_sheet"])] = {"A": None, "cap_cot": 0,
                                      "o": f'{_chu(d["ma"])}|{_chu(d["ten"])}'}
    for d in anh["phu"]["dong_trong"]["dong"]:
        hang[int(d["dong_sheet"])] = {"A": None, "cap_cot": 0, "o": ""}
    dau = min(hang)
    assert sorted(hang) == list(range(dau, dau + len(hang)))
    return {**_meta(anh), "dong": [hang[k] for k in sorted(hang)]}


_COT_HM = dict(zip(TRUONG, "HIJKLM"))      # đúng `fls.adapters.mapping_master.COT`


def _tho_mm_tu_anh(anh: dict) -> dict:
    """Lưới A…P *(16 cột)* theo dòng sheet: A · B · D–G từ bảng phụ `tho` *(ô đã băm giữ nguyên
    mã băm)*; H–M từ dòng chính *(đầu ra doc_cot)*; C · N · O · P ⇒ rỗng."""
    n = max(int(d["dong_sheet"]) for d in anh["dong"] + anh["phu"]["tho"]["dong"])
    luoi: list[list] = [[None] * 16 for _ in range(n)]
    for d in anh["phu"]["tho"]["dong"]:
        for c in "ABDEFG":
            luoi[int(d["dong_sheet"]) - 1][ord(c) - 65] = _chu(d[c])
    for d in anh["dong"]:
        for t, c in _COT_HM.items():
            luoi[int(d["dong_sheet"]) - 1][ord(c) - 65] = _chu(d[t])
    return {**_meta(anh), "dong": luoi}


def _tho_cdt_tu_anh(anh: dict) -> dict:
    cot = [anh["khoa"], *anh["cot"]]
    dong = sorted(anh["dong"], key=lambda d: d["thu_tu"])
    return {**_meta(anh), "cot": cot, "dong": [[_chu(d[c]) for c in cot] for d in dong]}


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
        del pha["dong"][XOA[khuon] - 7]                # hàng 1 của bản thô = dòng sheet 7
        assert pha["dong"][XOA[khuon] - 7]["o"].startswith("COT |")
    elif khuon == "mapping_master_cfg":
        del pha["dong"][XOA[khuon] - 1]                # lưới tính từ dòng sheet 1
    else:
        del pha["dong"][XOA[khuon] - 1]                # thu_tu 1-based
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
    return lambda t: t["dong"].pop(i)


ATL_CHOT = [
    pytest.param(lambda t: t.update(nguon=t["nguon"].replace("!A7:F88", "!B7:F88")), 2, "vùng",
                 id="vung_KHONG_bat_dau_cot_A"),
    pytest.param(lambda t: t.update(nguon=t["nguon"].replace("!A7:F88", "!A7:F80")), 2,
                 "vùng đọc", id="nhieu_hang_hon_vung_doc"),
    pytest.param(lambda t: t["dong"][1].update(F="GI"), 2, "ba khoá", id="hang_co_khoa_la"),
    pytest.param(lambda t: t["dong"][1].update(cap_cot=4), 2, "cap_cot", id="cap_cot_ngoai_0_3"),
    pytest.param(lambda t: t["dong"][0].update(cap_cot=1), 2, "tiêu đề nhóm",
                 id="tieu_de_nhom_KHONG_o_L1"),
    pytest.param(lambda t: t["dong"][1].update(o="GI - Gross Inflow"), 2, "dạng nào",
                 id="nhan_KHONG_thuoc_dang_nao"),
    pytest.param(lambda t: t["dong"][1].update(o="GI | "), 2, "thiếu mã hoặc tên",
                 id="dong_ma_thieu_ten"),
    pytest.param(lambda t: t["dong"].insert(0, {"A": None, "cap_cot": 0, "o": "XX | Gia lap"}), 2,
                 "TRƯỚC tiêu đề nhóm", id="dong_ma_truoc_nhom_dau"),
    pytest.param(lambda t: t["dong"][47].update(o="HDX|HD gia lap"), 1, "⛔ đo được",
                 id="nhom_KHONG_khai_o_NHOM"),
    pytest.param(_xoa(48), 1, "thiếu 1", id="nhom_khai_ma_0_dong_ma"),
    pytest.param(lambda t: t["dong"][28].update(o="HDO|HD Original"), 1,
                 "phụ `nhom` 7 dòng ≠ mong 6", id="them_mot_tieu_de_nhom"),
]


@pytest.mark.parametrize("pha, exit_mong, phai_noi", ATL_CHOT)
def test_KHUON_atl_cay_moi_chot_CAN(tmp_path, pha, exit_mong, phai_noi):
    """Bố cục lạ ⇒ TỪ CHỐI *(exit 2, ⛔ ghi — khuôn ⛔ đoán)*; nhóm lệch khai ⇒ ĐỎ *(exit 1)*."""
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
    ⚠ Dữ liệu thật: mọi nhóm mở bằng dòng L1 ⇒ ⛔ bài này thì đột biến "bỏ xoá ngăn" SỐNG
    *(ảnh tái tạo vẫn đúng từng byte)*. Phá: `NIS` *(dòng đầu `HDH`)* lên cột L2."""
    tho = _tho_atl_tu_anh(_doc(ANH_ATL))
    assert tho["dong"][41]["o"].startswith("NIS |") and tho["dong"][40]["o"].startswith("HDH|")
    tho["dong"][41]["cap_cot"] = 1
    ra = tmp_path / "a.json"
    kq = _chay("atl_cay", str(_ghi(tmp_path / "t.json", tho)), "--mong", str(MONG_ATL),
               "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1200:], kq.stderr[-1200:])
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
        t["dong"][i][j] = v
    return f


MM_CHOT = [
    pytest.param(lambda t: t.update(nguon=t["nguon"].replace("!A1:P120", "!A2:P120")), 2, "!A1:",
                 id="vung_KHONG_bat_dau_A1"),
    pytest.param(_gan(10, 0, 5), 2, "chuỗi/rỗng", id="o_KHONG_phai_chuoi"),
    pytest.param(lambda t: t["dong"][10].append("x"), 2, "≤ 16 ô", id="hang_qua_16_cot_A_P"),
    pytest.param(_gan(2, 0, "Bank"), 2, "tiêu đề", id="tieu_de_A_B_doi"),
    pytest.param(_gan(1, 1, "LE"), 2, "tiêu đề", id="dong_2_A_B_co_o"),
    pytest.param(lambda t: t["dong"][12].__setitem__(7, t["dong"][11][7]), 1,
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


def _ma_bam_trong(anh: dict, km) -> set[str]:
    khoa, chuoi = [], []
    _di(anh, khoa, chuoi)
    return {s for s in chuoi if km.MA_BAM.fullmatch(s)}


def _lo_chuoi_ro(chuoi: list[str], ma_bam: set[str], km) -> list[str]:
    """Chuỗi RÕ của một giá trị đã băm: băm cả chuỗi và từng TỪ *(nguyên · viết hoa)* rồi so
    với tập mã băm. ⛔ cần biết tên — chỉ cần mã băm có trong ảnh."""
    lo = []
    for s in chuoi:
        if km.MA_BAM.fullmatch(s):
            continue
        ung = {s.strip()} | set(_TU.findall(s)) | {t.upper() for t in _TU.findall(s)}
        if any(km.bam(u) in ma_bam for u in ung if u):
            lo.append(f"chuỗi rõ của giá trị đã băm (dài {len(s)})")   # ⛔ in chính chuỗi
    return lo


def quet_pii(anh: dict, ma_bam: set[str], km) -> tuple[list[str], dict[str, int]]:
    """→ (vi phạm, mẫu số). Bốn luật:
      R1 ⛔ khoá/tên cột nào *(mọi tầng + `cot` · `cot_khong_chon` · `khoa`)* thuộc `CAM_COT`;
      R2 ⛔ chuỗi nào dạng email;
      R3 ⛔ chuỗi rõ của giá trị đã băm *(xem `_lo_chuoi_ro`)*;
      R4 *(chỉ Mapping Master)* bảng phụ `tho` từ dòng `DONG_DAU_LE`: cột `B` *(LE)* ∈ pháp nhân
         đã khai hoặc là mã băm; `B` băm thì `A` cũng băm *(tên người nằm ở đuôi tên sheet)*."""
    khoa, chuoi = [], []
    _di(anh, khoa, chuoi)
    ten_cot = khoa + [anh.get("khoa", "")] + list(anh.get("cot", [])) \
        + list(anh.get("cot_khong_chon", []))
    loi = [f"R1 cột cấm `{k}`" for k in ten_cot if _chuan(k) in CAM_COT]
    loi += ["R2 chuỗi dạng email" for s in chuoi + khoa if _EMAIL.search(s)]
    loi += ["R3 " + x for x in _lo_chuoi_ro(chuoi + khoa, ma_bam, km)]
    so_r4 = 0
    if anh.get("khuon") == "mapping_master_cfg":
        for d in anh["phu"]["tho"]["dong"]:
            if int(d["dong_sheet"]) < km.DONG_DAU_LE:
                continue
            a, b = _chu(d["A"]), _chu(d["B"])
            if b is None:
                continue
            so_r4 += 1
            if km.MA_BAM.fullmatch(b):
                if a is not None and not km.MA_BAM.fullmatch(a):
                    loi.append(f"R4 dòng {d['dong_sheet']}: B băm mà A rõ")
            elif b.strip() not in km.LE_PHAP_NHAN:
                loi.append(f"R4 dòng {d['dong_sheet']}: B ⛔ thuộc pháp nhân đã khai, ⛔ băm")
    return loi, {"khoa": len(ten_cot), "chuoi": len(chuoi), "bam": len(ma_bam), "r4": so_r4}


@pytest.fixture(scope="module")
def km():
    return _nap_khuon("mapping_master_cfg")


def test_AC3_ba_anh_quet_PII_bang_0_tren_mau_so_KHAC_0(km):
    """Ba ảnh ⇒ 0 vi phạm. Đ3: mẫu số phải > 0 — và tập mã băm đúng **14** *(7 hàng × A · B)*,
    ⛔ thì R3 xanh trên tập rỗng."""
    anh = [_doc(p) for p in (ANH_ATL, ANH_MM, ANH_CDT)]
    ma_bam = set().union(*(_ma_bam_trong(a, km) for a in anh))
    assert len(ma_bam) == 14
    for a in anh:
        loi, mau = quet_pii(a, ma_bam, km)
        assert loi == [], (a["khuon"], loi)
        assert mau["khoa"] > 0 and mau["chuoi"] > 0, (a["khuon"], mau)
    assert quet_pii(anh[1], ma_bam, km)[1]["r4"] == 76            # dòng 4…79 có LE
    assert _doc(ANH_MM)["phu"]["bam"]["so_dong"] == 7


def _them_hang_gia_lap(km, tmp_path) -> tuple[pathlib.Path, str]:
    """Bản thô Mapping Master tái tạo + MỘT hàng A:B mang LE ⛔ khai *(giá trị TỔNG HỢP, ⛔ tên
    thật)* ở dòng 80 *(đang trống ở A:B)*."""
    tho = _tho_mm_tu_anh(_doc(ANH_MM))
    gia = "GIALAPX"
    assert gia not in km.LE_PHAP_NHAN
    tho["dong"][79][0] = f"R | 99999999_PO USD_{gia}"
    tho["dong"][79][1] = gia
    return _ghi(tmp_path / "tho_gia.json", tho), gia


def test_AC3_khuon_BAM_moi_LE_KHONG_khai_dong_khi_la_va_cong_DO_8_khac_7(km, tmp_path):
    """Khuôn đóng KHI LẠ: LE ⛔ có trong `LE_PHAP_NHAN` ⇒ băm A + B, ⛔ cần ai khai trước tên
    người. Hàng thứ 8 ⇒ bảng phụ `bam` 8 ≠ mong 7 ⇒ cổng ĐỎ *(người phải nhìn)*; và chuỗi rõ
    ⛔ có ở đâu trong ảnh đỏ."""
    tho, gia = _them_hang_gia_lap(km, tmp_path)
    ra = tmp_path / "mm_do.json"
    kq = _chay("mapping_master_cfg", str(tho), "--mong", str(MONG_MM), "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert "phụ `bam` 8 dòng ≠ mong 7" in kq.stdout
    assert gia not in ra.read_text(encoding="utf-8") and gia not in kq.stdout + kq.stderr
    assert km.bam(gia) in _ma_bam_trong(_doc(ra), km)


@pytest.mark.parametrize("pha, luat", [
    pytest.param(lambda a, g: a["dong"][0].update({"Email Address": None}), "R1",
                 id="R1_khoa_Email_Address"),
    pytest.param(lambda a, g: a["cot"].append("  Diễn   giải "), "R1", id="R1_cot_Dien_giai"),
    pytest.param(lambda a, g: a["dong"][0].update({"ten": {"chu": "lien.he@vi-du.invalid"}}),
                 "R2", id="R2_email"),
    pytest.param(lambda a, g: a["dong"][3].update({"ten": {"chu": f"chi phí {g.lower()} tháng"}}),
                 "R3", id="R3_ten_ro_lot_vao_ANH_KHAC"),
])
def test_AC3_ca_pha_may_quet_CAN_tung_luat(km, tmp_path, pha, luat):
    """Mỗi luật của máy quét được chứng minh CẮN *(Đ5)* trên bản sao ảnh cây ATL; ma băm của R3
    lấy từ lượt đóng băng hàng tổng hợp *(chuỗi rõ ấy lọt sang ảnh khác ⇒ bắt được)*."""
    tho, gia = _them_hang_gia_lap(km, tmp_path)
    ra = tmp_path / "mm.json"
    _chay("mapping_master_cfg", str(tho), "--mong", str(MONG_MM), "--ra", str(ra))
    ma_bam = _ma_bam_trong(_doc(ra), km)
    anh = copy.deepcopy(_doc(ANH_ATL))
    assert quet_pii(anh, ma_bam, km)[0] == []
    pha(anh, gia)
    loi = quet_pii(anh, ma_bam, km)[0]
    assert loi and all(x.startswith(luat) for x in loi), loi


def test_AC3_ca_pha_R4_LE_ro_KHONG_khai_trong_anh_Mapping_Master(km):
    """R4 cắn khi một ô B đã băm bị thay bằng chữ RÕ ⛔ thuộc pháp nhân đã khai, hay A của hàng
    băm bị trả về rõ."""
    anh = copy.deepcopy(_doc(ANH_MM))
    hang = next(d for d in anh["phu"]["tho"]["dong"] if km.MA_BAM.fullmatch(_chu(d["B"]) or ""))
    ma_bam = _ma_bam_trong(anh, km)
    hang["B"] = {"chu": "GIALAPX"}
    assert any(x.startswith("R4") and "B ⛔ thuộc" in x for x in quet_pii(anh, ma_bam, km)[0])
    anh = copy.deepcopy(_doc(ANH_MM))
    hang = next(d for d in anh["phu"]["tho"]["dong"] if km.MA_BAM.fullmatch(_chu(d["B"]) or ""))
    hang["A"] = {"chu": "R | 99999999_PO USD_GIALAPX"}
    assert any("B băm mà A rõ" in x for x in quet_pii(anh, ma_bam, km)[0])


#: Mọi tệp DT3 thêm/sửa *(trừ phiếu BG — bài ⛔ phụ thuộc phiếu)*.
TEP_DT3 = [TOOL, THU_MUC_KHUON / "atl_cay.py", THU_MUC_KHUON / "mapping_master_cfg.py",
           THU_MUC_KHUON / "cdt_correct.py", pathlib.Path(__file__),
           GOC / "tests" / "du_lieu" / "test_dong_bang_sheet.py", ANH_ATL, ANH_MM, ANH_CDT]


def test_AC3_tep_ma_va_anh_cua_DT3_KHONG_mang_chuoi_ro_cua_gia_tri_da_bam(km):
    """⛔ một tên người vào repo — kể cả trong bài, chú thích, khuôn: quét MỌI từ của 9 tệp DT3
    bằng R3. Mẫu số: số từ đã băm-so > 0 và 14 mã băm."""
    ma_bam = _ma_bam_trong(_doc(ANH_MM), km)
    assert len(ma_bam) == 14
    so_tu = 0
    for p in TEP_DT3:
        assert p.is_file(), p
        tu = _TU.findall(p.read_text(encoding="utf-8"))
        so_tu += len(tu)
        assert _lo_chuoi_ro(tu, ma_bam, km) == [], p.name
    assert so_tu > 10_000, so_tu


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
