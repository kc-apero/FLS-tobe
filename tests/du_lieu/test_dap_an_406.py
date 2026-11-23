"""ĐÁP ÁN 406 · `Report I General Ledger` CALC ZONE (BM–BT) — khuôn `gl_406` *(ISP 3.1.2 · DT4)*.

⭐ **Vì sao có tệp này.** Bước **H4** *(AP v3.1.2 §3.3.1 PD 406 · §3.5.4 WP-C2)* so song song
CA.GL ↔ 406 theo DÒNG × KỲ trên 8 cột `BM…BT`. H4 cần một ẢNH đứng yên của 406 — đọc MỘT lần,
đóng băng có checksum, một cổng khẳng định số dòng mỗi kỳ bằng số dòng sổ cùng kỳ, và **bỏ** cột
Diễn giải / Số chứng từ *(PII)*. Khuôn `gl_406` dựng ảnh ấy từ LƯỚI SA *(orchestrator đọc, O7)*.

Ba bài của ISP *(mục 6)* + đối chứng Đ5:

    DT4-B1  đóng băng mọi lát kỳ ⇒ 7883 dòng · Σ dòng/kỳ = phan_bo_ky (hoặc lệch CÓ TÊN 4 kỳ)
    DT4-B2  một lát kỳ RỖNG ⇒ ĐỎ *(Đ3: mẫu số 0 là kết quả)*
    DT4-B3  quét PII ⇒ 0 cột Diễn giải / Số chứng từ / Email; vùng đọc ⛔ phủ B:C

⛔⛔ **Bản đọc thô thật ⛔ nằm trong repo** *(scratchpad orchestrator, ⛔ commit — ISP mục 5)*. ⇒
Bài ở đây TÁI TẠO lưới thô **từ chính ảnh** rồi chạy lại công cụ ⇒ phải ra **đúng từng byte** tệp
đã commit *(cột `A` ⛔ vào ảnh — chỉ `ky`; tái tạo đặt serial ĐẦU THÁNG của `ky`, cho cùng `ky`)*.
Ca phá *(lát rỗng · lỗi BM:BT · khoá hỏng · ô ⛔ số · PII)* dựng lưới TỔNG HỢP, ⛔ số thật.

⭐ **Số đo 17/11 *(khoá SA chỉ-đọc, phiên cloud — mỗi số đếm MỘT vật, Đ4)*:**
  · 7883 hàng dữ liệu = sheet 10…7892 *(liên tục, cột A tăng dần)*.
  · 19 KỲ khớp `phan_bo_ky` CHÍNH XÁC *(2024-10…2026-04 = 19 THÁNG)*; 4 kỳ lệch CÓ TÊN
    *(202605 239/537 · 202606 0/613 · 202607 0/686 · 202608 0/487)* ⇒ Σ406 = 7883.
  · 6 HÀNG *(4962·4963·6073·6507·6949·7631)* thiếu tiền tệ `D` ⇒ `BO` & `BP` rỗng ⇒ **12 ô**.
  · 9843 hàng công thức thừa *(7893…17735, cột A rỗng)* ⇒ ĐẾM + khai, ⛔ vào bảng chính.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

from fls.oracle.anh_chup import AnhChup

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "dong_bang_sheet.py"
ANH = GOC / "tests" / "fixture" / "dap_an" / "gl_406.json"
NGUON_PHAN_BO = GOC / "tests" / "fixture" / "itl_ledge_adjustment.json"
THU_MUC_KHUON = GOC / "tools" / "khuon_dong_bang"

#: Checksum ghim của ảnh đã commit *(đổi ⇒ phải có lượt đóng băng mới + lý do)*.
#: ⚠ Vòng sửa R1 (`KQ-113` · F-1): THÊM bảng phụ `itl_id_lech` ⇒ checksum đổi
#: `e98f3a699e2de469` → `53a243b42101c314`. `nguon` + bảng CHÍNH *(dong)* + `cong_thuc` TRÙNG
#: TỪNG BYTE ảnh cũ *(đọc lại SA 1 lượt batchGet xác nhận 7883×11 = 0 lệch)*; checksum đổi CHỈ do
#: bảng phụ `itl_id_lech` mới *(nguon · dong · cong_thuc đều giữ nguyên ⇒ delta = itl_id_lech)*.
CHECKSUM_ANH = "53a243b42101c314"
MONG = 7883
DONG_DAU_SHEET = 10
EPOCH = datetime.date(1899, 12, 30)
COT_THO = ["dong_sheet", "A", "D", "R", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT"]
BT8 = ("BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT")
COT_ANH = ["ky", "itl_id", "D", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT"]
#: 4 kỳ lệch có tên — số dòng 406 MONG *(khuôn khai đúng số này)*.
LECH_CO_TEN = {202605: 239, 202606: 0, 202607: 0, 202608: 0}

#: ⛔ Đổi 1 byte ảnh cấu hình DT2/DT3 là ĐỎ *(`WO-111` AC-4: giữ ix_fx + 3 ảnh DT3 đúng từng byte)*.
#: sha256[:16] đo trên nền `cf5156e`.
SHA_CAU_HINH = {
    "ix_fx": "e2c9fdd028bd3286",
    "atl_cay": "504fa53d27c44b83",
    "cdt_correct": "8d8cfaed26b6aa5a",
    "mapping_master_cfg": "dc926c1b35b027ef",  # WO-234 19/11: đổi CÓ CHỦ ĐÍCH — che 4 số TK CN → TK_CA_NHAN_<n>
}


# ── trợ thủ ───────────────────────────────────────────────────────────────────

def _chay(*doi_so: str) -> subprocess.CompletedProcess:
    env = dict(os.environ, PYTHONUTF8="1")
    return subprocess.run([sys.executable, str(TOOL), *doi_so], cwd=GOC, env=env,
                          capture_output=True, text=True, timeout=180)


def _doc(p: pathlib.Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


def _chu(v):
    """Ô ảnh → giá trị thô: ô chữ ⇒ chuỗi; ô số ⇒ chuỗi chữ số; rỗng ⇒ None."""
    return None if v is None else (v["chu"] if isinstance(v, dict) else v)


def _checksum_lai(anh: dict) -> str:
    """Tính lại bằng CHÍNH `AnhChup` — dòng chính + mọi dòng bảng phụ *(bọc `{"phu", "dong"}`)*."""
    phu = tuple({"phu": ten, "dong": r} for ten in sorted(anh.get("phu", {}))
                for r in anh["phu"][ten]["dong"])
    return AnhChup(run_id="kiem", ngay=datetime.date.fromisoformat(anh["ngay_dong_bang"]),
                   nguon=anh["nguon"], dong=tuple(anh["dong"]) + phu).checksum()[:16]


def _da_tu_choi(kq: subprocess.CompletedProcess) -> None:
    assert kq.returncode == 2, (kq.returncode, kq.stdout[-800:], kq.stderr[-800:])
    dong = [d for d in kq.stderr.splitlines() if d.startswith("⛔ TỪ CHỐI")]
    assert len(dong) == 1, ("cần đúng MỘT dòng `⛔ TỪ CHỐI …`", kq.stderr[-800:])


def _serial(yyyymm: int) -> int:
    """`yyyymm` → serial ngày ĐẦU THÁNG *(cột A ⛔ vào ảnh — chỉ cần cùng `ky`)*."""
    y, m = divmod(int(yyyymm), 100)
    return (datetime.date(y, m, 1) - EPOCH).days


def _lit(v) -> str:
    """Giá trị thô → literal JSON: số *(chuỗi chữ số)* ⇒ literal SỐ *(⛔ nháy — giữ đủ chữ số)*;
    chuỗi khác ⇒ chuỗi; None ⇒ null."""
    if v is None:
        return "null"
    if isinstance(v, str) and re.fullmatch(r"-?\d+(\.\d+)?([eE][+-]?\d+)?", v):
        return v
    return json.dumps(v, ensure_ascii=False)


def _viet_luoi(p: pathlib.Path, values: list[list], *, cot=None, dong_dau=DONG_DAU_SHEET,
               hang_cong_thuc=None, nguon="TỔNG HỢP · bài DT4 (⛔ số thật)",
               doc_luc="2026-11-17", cach_doc="tổng hợp trong bài thử") -> pathlib.Path:
    """Ghi lưới thô đúng hình orchestrator đưa *(viết TAY phần `values` để ô số ra literal SỐ)*."""
    if cot is None:
        cot = COT_THO
    if hang_cong_thuc is None:
        hang_cong_thuc = {"so_dong": 9843, "dai_hang": "7893..17735", "cot_A_rong": True}
    dong = ",\n  ".join("[" + ", ".join(_lit(x) for x in h) + "]" for h in values)
    p.write_text(
        "{\n"
        f' "nguon": {json.dumps(nguon, ensure_ascii=False)},\n'
        f' "doc_luc": {json.dumps(doc_luc)},\n'
        f' "cach_doc": {json.dumps(cach_doc, ensure_ascii=False)},\n'
        f' "dong_dau_sheet": {dong_dau},\n'
        f' "cot": {json.dumps(cot, ensure_ascii=False)},\n'
        f' "hang_cong_thuc": {json.dumps(hang_cong_thuc, ensure_ascii=False)},\n'
        f' "values": [\n  {dong}\n ]\n'
        "}\n", encoding="utf-8")
    return p


def _luoi_tu_anh(anh: dict) -> list[list]:
    """Lưới thô TÁI TẠO từ ảnh: hàng theo `thu_tu`, ô theo `COT_THO` *(A = serial đầu tháng của
    `ky`; D · R · BM…BT lấy từ ảnh)*. Chạy lại công cụ trên lưới này ⇒ ĐÚNG TỪNG BYTE ảnh."""
    rows = []
    for d in sorted(anh["dong"], key=lambda x: x["thu_tu"]):
        rows.append([int(d["dong_sheet"]), _serial(d["ky"]), _chu(d["D"]), _chu(d["itl_id"])]
                    + [_chu(d[c]) for c in BT8])
    return rows


@pytest.fixture
def luoi(tmp_path) -> list[list]:
    return _luoi_tu_anh(_doc(ANH))


# ══ DT4-B1 · ảnh đã commit (AC-1) ══════════════════════════════════════════════════════════════

def test_DT4_B1_anh_406_7883_dong_khoa_dong_sheet_lien_tuc():
    """Ảnh thật: 7883 dòng, khoá `dong_sheet` 10…7892 LIÊN TỤC, 11 cột mang theo, cổng ĐẠT. Mỗi
    con số đếm một vật *(Đ4)*."""
    anh = _doc(ANH)
    assert anh["bang"] == "PD.406"
    assert anh["khoa"] == "dong_sheet" and anh["kieu_khoa"] == "dong_sheet"
    assert anh["cot"] == COT_ANH
    dong = anh["dong"]
    assert anh["so_dong"] == len(dong) == MONG
    ds = [int(d["dong_sheet"]) for d in dong]
    assert ds == list(range(DONG_DAU_SHEET, DONG_DAU_SHEET + MONG))   # 10…7892 liên tục
    assert [d["thu_tu"] for d in dong] == list(range(1, MONG + 1))    # giữ NGUYÊN thứ tự
    assert anh["cong"] == {"mong": MONG, "so_dong": MONG, "dat": True, "ly_do": []}
    assert (anh["thieu"], anh["khoa_hong"], anh["o_rong"]) == ([], [], [])
    assert anh["lac"] == ["202605", "202606", "202607", "202608"]
    assert anh["ngay_dong_bang"] == "2026-11-17"
    assert anh["checksum_noi_dung"] == _checksum_lai(anh) == CHECKSUM_ANH


def test_DT4_B1_phan_bo_ky_19_khop_4_lech_co_ten():
    """⭐ AC-1 ĐỘC LẬP khuôn: đếm số dòng mỗi kỳ TRÊN CHÍNH ẢNH, so với `phan_bo_ky` của
    `itl_ledge_adjustment.json`. 19 kỳ khớp CHÍNH XÁC; 4 kỳ lệch CÓ TÊN đúng số đo. Lệch nào
    khác ⇒ bài này ĐỎ.

    ⚠ `WO-111`/AC-1 ghi *"21 kỳ"* — MISCOUNT: dải `2024-10…2026-04` có **19** tháng *(Đ4)*.
    """
    anh = _doc(ANH)
    pb = json.loads(NGUON_PHAN_BO.read_text(encoding="utf-8"))["phan_bo_ky"]
    ledger = {int(k[:4]) * 100 + int(k[5:7]): v for k, v in pb.items()}
    thuc: dict[int, int] = {}
    for d in anh["dong"]:
        thuc[int(d["ky"])] = thuc.get(int(d["ky"]), 0) + 1
    assert sum(thuc.values()) == MONG                       # Đ3: mẫu số > 0

    khop = sorted(k for k in ledger if thuc.get(k, 0) == ledger[k])
    lech = {k: (thuc.get(k, 0), ledger[k]) for k in ledger if thuc.get(k, 0) != ledger[k]}
    assert len(khop) == 19, (len(khop), khop)              # ⛔ 21 — WO miscount
    assert lech == {202605: (239, 537), 202606: (0, 613),
                    202607: (0, 686), 202608: (0, 487)}
    # ⛔ kỳ 406 nào ⛔ có trong sổ (kỳ lạ)
    assert set(thuc) <= set(ledger)
    # số học Σ: 7883 = 9967 − (537−239) − 613 − 686 − 487
    assert sum(ledger.values()) - (537 - 239) - 613 - 686 - 487 == MONG


def test_DT4_B1_anh_TAI_TAO_dung_tung_byte_tu_cong_cu(tmp_path):
    """Bản thô thật ⛔ commit ⇒ chứng minh ảnh đã commit LÀ đầu ra công cụ: tái tạo LƯỚI từ ảnh
    *(A = serial đầu tháng của `ky`)* rồi chạy lại ⇒ **đúng từng byte**. Sửa tay ảnh ⇒ ĐỎ."""
    anh = _doc(ANH)
    tho = _viet_luoi(tmp_path / "tho.json", _luoi_tu_anh(anh),
                     nguon=anh["nguon"], doc_luc=anh["ngay_dong_bang"], cach_doc=anh["cach_doc"],
                     hang_cong_thuc={"so_dong": int(anh["phu"]["cong_thuc"]["dong"][0]["so_dong"]),
                                     "dai_hang": anh["phu"]["cong_thuc"]["dong"][0]["dai_hang"]["chu"],
                                     "cot_A_rong": True})
    ra = tmp_path / "gl_406.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    assert kq.returncode == 0, (kq.stdout[-1500:], kq.stderr[-1500:])
    assert ra.read_bytes() == ANH.read_bytes()


def test_DT4_B1_cong_mong_DO_ca_hai_chieu(luoi, tmp_path):
    """Đ5: `--mong` khác số dòng ⇒ ĐỎ cả khi thừa lẫn thiếu; đúng ⇒ đạt."""
    for mong, exit_mong in ((MONG - 1, 1), (MONG, 0), (MONG + 1, 1)):
        tho = _viet_luoi(tmp_path / f"tho_{mong}.json", luoi)
        kq = _chay("gl_406", str(tho), "--mong", str(mong), "--ra", str(tmp_path / "a.json"))
        assert kq.returncode == exit_mong, (mong, kq.stdout[-800:], kq.stderr[-800:])
        assert ("[ĐẠT]" if exit_mong == 0 else "[ĐỎ]") in kq.stdout


# ══ DT4-B1 · cổng KỲ ĐỎ cả hai chiều (AC-1) ════════════════════════════════════════════════════

@pytest.mark.parametrize("sua, phai_thieu, ten", [
    # bỏ 1 dòng kỳ KHỚP (202501: 748→747) ⇒ lệch NGOÀI 4 kỳ có tên ⇒ ĐỎ
    pytest.param("bo_mot_dong_202501", "202501", "thiếu một dòng kỳ khớp", id="thieu_ky_khop"),
    # thêm 1 dòng vào kỳ VẮNG có tên (202606: 0→1) ⇒ ĐỎ (bản sao 406 lẽ ra dừng)
    pytest.param("them_dong_202606", "202606", "thêm dòng kỳ vắng có tên", id="them_ky_vang"),
    # đổi 1 dòng sang kỳ LẠ ⛔ có trong sổ (209901) ⇒ ĐỎ
    pytest.param("ky_la_209901", "209901", "kỳ lạ ⛔ trong sổ", id="ky_la"),
])
def test_DT4_B1_cong_ky_DO_khi_lech_NGOAI_4_ky_co_ten(luoi, tmp_path, sua, phai_thieu, ten):
    """④/Đ5: cổng kỳ phải ĐỎ khi số dòng mỗi kỳ lệch NGOÀI 4 kỳ có tên — thiếu kỳ khớp, thêm kỳ
    vắng, hay kỳ lạ. `thieu` chứa kỳ ấy; `--mong` điều chỉnh cho tách bạch cổng kỳ ⟂ cổng đếm."""
    rows = [list(r) for r in luoi]
    mong = MONG
    if sua == "bo_mot_dong_202501":
        i = next(k for k, r in enumerate(rows) if r[1] == _serial(202501))
        del rows[i]
        mong = MONG - 1
        for k in range(i, len(rows)):        # giữ dong_sheet liên tục
            rows[k][0] = DONG_DAU_SHEET + k
    elif sua == "them_dong_202606":
        mau = rows[-1]
        rows.append([DONG_DAU_SHEET + len(rows), _serial(202606), mau[2], "ITL#X",
                     *mau[4:]])
        mong = MONG + 1
    elif sua == "ky_la_209901":
        rows[-1][1] = _serial(209901)        # đổi ngày dòng cuối sang 2099-01
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(mong), "--ra", str(ra))
    assert kq.returncode == 1, (ten, kq.stdout[-1200:], kq.stderr[-800:])
    anh = _doc(ra)
    assert phai_thieu in anh["thieu"], (ten, anh["thieu"])
    assert f"thiếu {len(anh['thieu'])}" in " · ".join(anh["cong"]["ly_do"]) or anh["thieu"]


def test_DT4_B1_cong_ky_do_duoc_tren_tap_rong_la_DO(luoi, tmp_path, monkeypatch):
    """Đ3: nguồn `phan_bo_ky` thiếu ⇒ cổng kỳ ⛔ ĐO ĐƯỢC ⇒ ảnh ghi `thieu = lac = null`, ĐỎ —
    ⛔ 'xanh trên tập rỗng'. Giả bằng cách trỏ khuôn tới tệp phan_bo không tồn tại."""
    # chạy công cụ với HOME khác? đơn giản hơn: xác minh hành vi qua nạp khuôn trực tiếp
    import importlib.util
    spec = importlib.util.spec_from_file_location("khuon_gl_406_rong", THU_MUC_KHUON / "gl_406.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    monkeypatch.setattr(m, "NGUON_PHAN_BO", GOC / "tests" / "fixture" / "KHONG_CO.json")
    with pytest.raises(ValueError, match="phan_bo_ky"):
        m.thieu_lac([{"ky": "202410"}])


# ══ DT4-B2 · một lát kỳ RỖNG ⇒ ĐỎ (AC-2) ═══════════════════════════════════════════════════════

def test_DT4_B2_mot_lat_ky_RONG_thi_DO(luoi, tmp_path):
    """AC-2/Đ3: một lát kỳ trả RỖNG *(bỏ hết dòng kỳ 202502 — 283 dòng)* ⇒ kỳ ấy đếm 0 ≠
    phan_bo_ky 283 ⇒ `thieu` chứa 202502 ⇒ ĐỎ. Mẫu số 0 LÀ kết quả, ⛔ 'không thấy lệch'."""
    rows = [list(r) for r in luoi if r[1] != _serial(202502)]
    for k in range(len(rows)):
        rows[k][0] = DONG_DAU_SHEET + k
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(len(rows)), "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1200:], kq.stderr[-800:])
    anh = _doc(ra)
    assert "202502" in anh["thieu"]
    assert "thiếu: [" in kq.stdout and "202502" in kq.stdout


def test_DT4_B2_ban_tho_values_RONG_thi_TU_CHOI(tmp_path):
    """AC-2: lưới `values` RỖNG ⇒ TỪ CHỐI exit 2 *(⛔ đóng băng ảnh rỗng — Đ3)*, ⛔ ghi tệp."""
    tho = _viet_luoi(tmp_path / "tho.json", [])
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    _da_tu_choi(kq)
    assert not ra.exists()


# ══ DT4-B3 · PII (AC-3) ════════════════════════════════════════════════════════════════════════

#: Mẫu cột PII — quét TÊN cột ảnh *(ca phá dưới chứng minh nó CẮN)*.
_PII = re.compile(r"di[eễ]n\s*gi[aả]i|s[oố]\s*ch[uứ]ng\s*t[uừ]|email", re.IGNORECASE)


def _quet_pii(ten_cot: list[str]) -> list[str]:
    return [c for c in ten_cot if _PII.search(" ".join(str(c).split()))]


def test_DT4_B3_anh_khong_mang_cot_Dien_giai_So_CT_Email():
    """AC-3: ảnh ⛔ mang cột Diễn giải / Số chứng từ / Email — quét MỌI tên khoá *(đỉnh + cột +
    từng khoá dòng + cột bảng phụ)*; Đ3: mẫu số > 0."""
    anh = _doc(ANH)
    ten = (list(anh) + [anh["khoa"], *anh["cot"]]
           + [k for d in anh["dong"] for k in d]
           + [k for b in anh.get("phu", {}).values() for r in b["dong"] for k in r])
    assert len(ten) > MONG * 3                      # mẫu số: ≥ 3·7883 khoá
    assert _quet_pii(ten) == []
    # vùng đọc ⛔ phủ B:C — lưới thô chỉ A·D·R·BM:BT, ⛔ B/C
    assert "B" not in COT_THO and "C" not in COT_THO
    assert "Diễn giải" not in anh["ghi_chu_khuon"] or "⛔ mang" in anh["ghi_chu_khuon"]


@pytest.mark.parametrize("ten_xau", [
    pytest.param("Diễn giải", id="dien_giai"),
    pytest.param("Diễn  giải", id="dien_giai_khoang_trang"),
    pytest.param("số chứng từ", id="so_chung_tu"),
    pytest.param("Email Address", id="email"),
])
def test_DT4_B3_may_quet_PII_CAN_ca_pha(ten_xau):
    """⭐ Ca phá: máy quét PHẢI cắn tên cột Diễn giải / Số CT / Email *(⛔ cổng mù — Đ5)*."""
    assert _quet_pii(["dong_sheet", "ky", ten_xau, "BM"]) == [ten_xau]


def test_DT4_B3_ban_tho_co_cot_Email_thi_TU_CHOI(luoi, tmp_path):
    """AC-3: lưới thô mang cột `Email Address` ⇒ TỪ CHỐI cả lượt *(`PM_COT_RIENG_TU`)*, ⛔ ghi,
    ⛔ in giá trị."""
    rows = [r + ["nguoi@vi-du.invalid"] for r in luoi]
    tho = _viet_luoi(tmp_path / "tho.json", rows, cot=COT_THO + ["Email Address"])
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    _da_tu_choi(kq)
    assert "PM_COT_RIENG_TU" in kq.stderr
    assert "vi-du.invalid" not in kq.stdout + kq.stderr
    assert not ra.exists()


# ══ DT4 · khuôn là TỆP RIÊNG + giữ ảnh DT2/DT3 từng byte (AC-4) ═════════════════════════════════

def test_DT4_khuon_gl_406_la_tep_rieng_dung_giao_keo():
    """AC-4: khuôn mới = tệp riêng `tools/khuon_dong_bang/gl_406.py`, giao kèo đúng."""
    import importlib.util
    p = THU_MUC_KHUON / "gl_406.py"
    assert p.is_file()
    spec = importlib.util.spec_from_file_location("khuon_gl_406_bai", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    assert m.BANG == "PD.406" and m.KHOA == "dong_sheet" and m.KIEU_KHOA == "dong_sheet"
    assert m.COT == ("ky", "itl_id", "D", "BM", "BN", "BO", "BP", "BQ", "BR", "BS", "BT")
    assert m.KIEU_COT == {"itl_id": "chu", "D": "chu?", "BO": "so?", "BP": "so?"}
    assert m.PHU_MONG == {"cong_thuc": 1, "itl_id_lech": 4}              # F-1: +itl_id_lech
    assert m.LECH_CO_TEN == LECH_CO_TEN
    assert m.LECH_ITL_ID == (6684, 6836, 7500, 7832)                    # F-1: 4 dong_sheet ghim
    assert m.TIEN_TE == ("USD", "SGD", "COP", "VND", "HKD")             # F-3: tập đóng D
    assert m.ITL_ID_RE.fullmatch("ITL#123") and not m.ITL_ID_RE.fullmatch("#N/A ()")
    assert callable(m.chuan_bi) and callable(m.thieu_lac)


def test_DT4_giu_anh_IX_FX_va_ba_anh_DT3_dung_tung_byte():
    """AC-4: sửa công cụ chung *(KIEU_KHOA `dong_sheet` · KIEU_COT `so?`)* ⛔ đổi ảnh cũ — ix_fx
    + 3 ảnh DT3 giữ ĐÚNG TỪNG BYTE *(sha256[:16] ghim)*."""
    for ten, sha in SHA_CAU_HINH.items():
        p = GOC / "tests" / "fixture" / "cau_hinh" / f"{ten}.json"
        got = hashlib.sha256(p.read_bytes()).hexdigest()[:16]
        assert got == sha, (ten, got, sha)


# ══ DT4 · khoá dong_sheet + cột so? (sửa công cụ — chứng minh ĐỎ) ═══════════════════════════════

def test_DT4_khoa_dong_sheet_hop_le():
    """Công cụ: `_khoa_hop_le` kiểu `dong_sheet` = ô SỐ chữ số nguyên ≥ 1; ô chữ / rỗng / âm / 0
    đều HỎNG *(đối xứng yyyymm)*."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("dbs_bai", TOOL)
    m = importlib.util.module_from_spec(spec)
    sys.modules["dbs_bai"] = m
    spec.loader.exec_module(m)
    assert "dong_sheet" in m.KIEU_KHOA_BIET and "so?" in m.KIEU_COT_BIET
    hl = lambda v: m._khoa_hop_le(v, "dong_sheet")
    assert hl("10") and hl("7892") and hl("1")
    assert not hl("0") and not hl("-5") and not hl({"chu": "10"}) and not hl(None) and not hl("10.5")
    # DT4-R1-04: `isdigit()` nhận chữ số NGOÀI ASCII và nổ `int()` — `fullmatch` chặn cả hai
    assert not hl("٣")          # chữ số Ả Rập: isdigit()=True ⇒ xưa nhận nhầm, nay HỎNG
    assert not hl("²")          # mũ 2: isdigit()=True nhưng int("²") NỔ ⇒ nay HỎNG (⛔ traceback)
    assert not hl("７")          # chữ số full-width: cũng ngoài ASCII


def test_DT4_dong_sheet_KHONG_lien_tuc_thi_TU_CHOI(luoi, tmp_path):
    """①: khuôn kiểm `dong_sheet` LIÊN TỤC — một hàng bị bỏ sót *(đổi dong_sheet hàng 5)* ⇒
    `chuan_bi` ValueError ⇒ TỪ CHỐI exit 2 *(⛔ bỏ sót hàng im lặng — AC-5)*."""
    rows = [list(r) for r in luoi]
    rows[5][0] = 99999                       # dong_sheet ⛔ liên tục
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    _da_tu_choi(kq)
    assert "liên tục" in kq.stderr and not ra.exists()


def test_DT4_cot_so_opt_BO_RONG_cho_phep_nhung_LOI_thi_DO(luoi, tmp_path):
    """③: `BO`/`BP` = `so?` — RỖNG cho phép *(ảnh thật 6 hàng, cổng ĐẠT)*; nhưng ô CÓ giá trị mà
    ⛔ số *(chuỗi lỗi `#DIV/0!`)* ⇒ "ô ⛔ số" ⇒ ĐỎ *(đối xứng `so`)*."""
    rows = [list(r) for r in luoi]
    rows[0][6] = "#DIV/0!"                    # BO (idx 6 trong COT_THO) của hàng dữ liệu = lỗi
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1200:], kq.stderr[-800:])
    assert "ô ⛔ số: 1/" in kq.stdout
    # ô ấy ghi là CHỮ trong ảnh (⛔ lẫn số)
    assert _doc(ra)["dong"][0]["BO"] == {"chu": "#DIV/0!"}


# ══ DT4 · 9843 hàng công thức thừa (AC-5) ══════════════════════════════════════════════════════

def test_DT4_B1_anh_khai_9843_hang_cong_thuc():
    """AC-5: ảnh khai 9843 hàng công thức thừa ở bảng phụ `cong_thuc` *(1 dòng, vào checksum)* +
    `ghi_chu_khuon`; ⛔ vào bảng chính."""
    anh = _doc(ANH)
    cf = anh["phu"]["cong_thuc"]
    assert cf["mong"] == cf["so_dong"] == 1
    assert cf["dong"][0]["so_dong"] == "9843"
    assert cf["dong"][0]["dai_hang"] == {"chu": "7893..17735"}
    assert "9843" in anh["ghi_chu_khuon"] and "⛔ vào bảng chính" in anh["ghi_chu_khuon"]


def test_DT4_hang_du_lieu_co_loi_BM_thi_DO(luoi, tmp_path):
    """AC-5: hàng có ngày *(dữ liệu)* mà `BM` LỖI *(chuỗi `#DIV/0!`)* ⇒ "ô ⛔ số" ⇒ ĐỎ — ⛔ lọt
    vào ảnh như số."""
    rows = [list(r) for r in luoi]
    rows[3][4] = "#DIV/0! (Function DIVIDE parameter 2 cannot be zero.)"   # BM idx 4
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1200:], kq.stderr[-800:])
    assert "ô ⛔ số: 1/" in kq.stdout


def test_DT4_cot_A_rong_False_thi_TU_CHOI(luoi, tmp_path):
    """AC-5/⑤: `hang_cong_thuc.cot_A_rong = False` ⇒ TỪ CHỐI — vùng công thức thừa PHẢI có cột A
    RỖNG *(bằng chứng ⛔ phải dòng sổ)*; False ⇒ ⛔ dám bỏ im lặng."""
    tho = _viet_luoi(tmp_path / "tho.json", luoi,
                     hang_cong_thuc={"so_dong": 9843, "dai_hang": "7893..17735", "cot_A_rong": False})
    ra = tmp_path / "moi" / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    _da_tu_choi(kq)
    assert "cot_A_rong" in kq.stderr and not ra.exists()


def test_DT4_sau_hang_thieu_tien_te_D_BO_BP_rong():
    """③ đo 17/11: ĐÚNG 6 hàng *(4962·4963·6073·6507·6949·7631)* thiếu tiền tệ `D`, mỗi hàng cả
    `BO` lẫn `BP` rỗng ⇒ 12 ô. itl_id 0 rỗng. Mẫu số 7883 *(Đ3/Đ4)*."""
    anh = _doc(ANH)
    mong_ds = {"4962", "4963", "6073", "6507", "6949", "7631"}
    rong_d = {d["dong_sheet"] for d in anh["dong"] if d["D"] is None}
    rong_bo = {d["dong_sheet"] for d in anh["dong"] if d["BO"] is None}
    rong_bp = {d["dong_sheet"] for d in anh["dong"] if d["BP"] is None}
    assert rong_d == rong_bo == rong_bp == mong_ds
    o_rong_bo_bp = sum(1 for d in anh["dong"] for c in ("BO", "BP") if d[c] is None)
    assert o_rong_bo_bp == 12                               # 6 hàng × 2 ô
    assert all(d["itl_id"] is not None for d in anh["dong"])
    assert len(anh["dong"]) == MONG


# ══ VÒNG SỬA SAU R1 (KQ-113) ═══════════════════════════════════════════════════════════════════
# F-1 (DT4-R1-01 · NÊN SỬA) · F-3 (DT4-R1-03) · F-2 (DT4-R1-02) · F-4 (DT4-R1-04 ở test khoá trên).

def test_DT4_R1_itl_id_lech_co_ten_4_hang():
    """F-1 (DT4-R1-01): 4 hàng itl_id = chuỗi LỖI Sheets `#N/A ()` khai thành LỆCH CÓ TÊN ở bảng
    phụ `itl_id_lech` *(mong 4, liệt kê dong_sheet)* — ⛔ lọt cổng `chu` im lặng. Đọc lại nguồn SA
    *(vòng sửa R1)* xác nhận ĐÚNG 4 hàng ấy *(6684·6836·7500·7832)*; bảng chính TRÙNG byte ảnh cũ."""
    anh = _doc(ANH)
    il = anh["phu"]["itl_id_lech"]
    assert il["mong"] == il["so_dong"] == 4
    assert [int(r["dong_sheet"]) for r in il["dong"]] == [6684, 6836, 7500, 7832]
    pat = re.compile(r"ITL#\d+")
    assert all(not pat.fullmatch(_chu(r["itl_id_tho"])) for r in il["dong"])
    # bảng CHÍNH: đúng 7879 hàng khớp ^ITL#\d+$; 4 hàng lệch = đúng tập itl_id_lech (Đ3 mẫu số>0)
    khop = [d for d in anh["dong"] if pat.fullmatch(_chu(d["itl_id"]) or "")]
    assert len(khop) == MONG - 4 == 7879
    lech_ds = sorted(int(d["dong_sheet"]) for d in anh["dong"]
                     if not pat.fullmatch(_chu(d["itl_id"]) or ""))
    assert lech_ds == [6684, 6836, 7500, 7832]
    assert "itl_id_lech" in anh["ghi_chu_khuon"] and "^ITL#" in anh["ghi_chu_khuon"]


@pytest.mark.parametrize("sua, mong_so, ten", [
    pytest.param("them_na_5", 5, "thêm hàng #N/A thứ 5", id="them_NA_thu_5"),
    pytest.param("bo_na_1", 3, "bỏ 1 hàng #N/A", id="bo_1_NA"),
])
def test_DT4_R1_itl_id_lech_khac_4_thi_DO(luoi, tmp_path, sua, mong_so, ten):
    """F-1/Đ5 ĐỎ-TRƯỚC: số hàng itl_id ⛔ khớp `^ITL#\\d+$` KHÁC 4 ⇒ cổng bảng phụ ĐỎ *(thừa HAY
    thiếu)*. *(Đo 17/11: công cụ TRƯỚC sửa cho cả hai ca qua `[ĐẠT]` exit 0 — cổng `chu` mù.)*"""
    rows = [list(r) for r in luoi]
    iR = COT_THO.index("R")
    if sua == "them_na_5":
        for r in rows:
            if isinstance(r[iR], str) and r[iR].startswith("ITL#"):
                r[iR] = "#N/A ()"; break
    else:
        for r in rows:
            if r[iR] == "#N/A ()":
                r[iR] = "ITL#999999"; break
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    assert kq.returncode == 1, (ten, kq.stdout[-1200:], kq.stderr[-800:])
    assert ("`itl_id_lech` %d dòng ≠ mong 4" % mong_so) in kq.stdout
    assert _doc(ra)["phu"]["itl_id_lech"]["so_dong"] == mong_so


def test_DT4_R1_D_ngoai_tap_tien_te_thi_DO(luoi, tmp_path):
    """F-3 (DT4-R1-03) ĐỎ-TRƯỚC: `D` CÓ chữ mà ⛔ thuộc {USD,SGD,COP,VND,HKD} ⇒ ĐỎ *(Diễn giải/Số
    CT lạc sang cột D là đường rò PII mà quét TÊN cột ⛔ thấy)*. Rỗng vẫn cho phép. ⛔ in giá trị."""
    rows = [list(r) for r in luoi]
    iD = COT_THO.index("D")
    rows[0][iD] = "Diễn giải lạc cột D"            # giá trị PII giả lạc vào D (dong_sheet 10)
    tho = _viet_luoi(tmp_path / "tho.json", rows)
    ra = tmp_path / "a.json"
    kq = _chay("gl_406", str(tho), "--mong", str(MONG), "--ra", str(ra))
    assert kq.returncode == 1, (kq.stdout[-1200:], kq.stderr[-800:])
    assert "D_la@10" in _doc(ra)["thieu"]
    assert "Diễn giải lạc" not in kq.stdout        # cổng ⛔ in GIÁ TRỊ lạ (chỉ dong_sheet)


def test_DT4_R1_quet_PII_GIA_TRI_o_itl_id_va_D():
    """F-3 (DT4-R1-03): quét GIÁ TRỊ ô cột chữ tự do `itl_id` + `D` *(bia -03: xưa chỉ quét TÊN
    cột)*. Ảnh thật: 0 giá trị khớp mẫu Diễn giải/Số CT/Email. Mẫu số = 2·7883 ô *(Đ3)*."""
    anh = _doc(ANH)
    gia_tri = [v for d in anh["dong"] for c in ("itl_id", "D")
               if (v := _chu(d[c])) is not None]
    assert len(gia_tri) > MONG                      # mẫu số > 0 (Đ3)
    assert _quet_pii(gia_tri) == []
    for r in anh["phu"]["itl_id_lech"]["dong"]:     # cả bảng phụ
        assert _quet_pii([_chu(r["itl_id_tho"])]) == []


def test_DT4_R1_quet_PII_GIA_TRI_CAN_ca_pha():
    """⭐ Ca phá: quét GIÁ TRỊ phải CẮN chuỗi Diễn giải/Số CT/Email lạc vào ô *(⛔ cổng mù — Đ5)*."""
    assert _quet_pii(["ITL#12", "Diễn giải abc", "USD", "số chứng từ X"]) == \
        ["Diễn giải abc", "số chứng từ X"]


def test_DT4_R1_ky_tu_serial_ghim_ranh_gioi_thang():
    """F-2 (DT4-R1-02): `_ky_tu_serial` ghim ở HAI phía ranh giới tháng bằng serial VIẾT TAY
    *(⛔ dùng chung EPOCH với mã)*. Đột biến `EPOCH`±1 ngày ⇒ đẩy ngày cuối/đầu tháng sang kỳ kế ⇒
    bài này ĐỎ *(bia: bài tái tạo lưới cũ suy serial bằng cùng EPOCH ⇒ đối xứng sai, M7 xanh)*."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("gl406_f2", THU_MUC_KHUON / "gl_406.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # serial Google Sheets VIẾT TAY (1899-12-30 = 0) — tra bảng, ⛔ tính từ EPOCH của mã:
    assert m._ky_tu_serial(45688) == 202501     # 2025-01-31 ngày CUỐI tháng (bắt EPOCH+1)
    assert m._ky_tu_serial(45689) == 202502     # 2025-02-01 ngày ĐẦU tháng (bắt EPOCH-1)
    assert m._ky_tu_serial(45657) == 202412     # 2024-12-31 cuối NĂM
    assert m._ky_tu_serial(45717) == 202503     # 2025-03-01 đầu tháng 3
