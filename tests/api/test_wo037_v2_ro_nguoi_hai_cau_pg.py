# -*- coding: utf-8 -*-
"""`WO-037` **vòng 2** *(`TL-038` — `BA-07` **v3.10**)*: rổ `nguoi` nói **hai**
câu theo con số **cửa** trả *(`(i)` · `AC-11`)* · ba câu `VI_SAO` ⛔ ký hiệu cấm
*(`(j)` · `AC-13`)* · SQL `itl-candidates` vế sổ `btrim` *(`(k)` · `AC-14`)* ·
bài quét so tiền tệ phủ `lenh_cho.py` *(`(l)` · `AC-15`)*.

⛔⛔ Lỗi gốc *(`BG-039` yếu #1 — chính vòng 1 gây ra)*: sau khi lệnh khớp mã
**chỉ** ở tiền tệ khác rời rổ `may`, rổ `nguoi` có **hai** loại lệnh *(sổ thật
02/10, ảnh `NAP-2026-10-02-PMA07ED283`, chỉ đọc, hàm thật: `nguoi` **616** = ⛔
số chứng từ **532** ＋ khớp mã khác tiền tệ **84**)*, mà băng `F01L` nói một câu
cho cả rổ *"Chưa có số chứng từ"* — sai **84 / 616**. Màn ⛔ được tự đếm hai
loại *(nó chỉ thấy một trang — lớp lỗi `do_phu` dừng ở 500)* ⇒ cửa `/ro` trả
thêm **một** khoá `nguoi_khac_tien_te`, đếm bằng **chính** hàm quyết
`the.vi_sao` *(`lc.la_khop_ma_chi_khac_tien_te`)*, trong **cùng** vòng lặp của
`dem_theo_ro` *(`WO-037` Rủi ro vòng 2 ③ — ⛔ vòng lặp thứ hai trên sổ thật)*.

⛔ Luật của tệp *(`BA-07` §4h ⓵ — luật bài thử)*: thân đo đi ra từ **cửa HTTP
thật** trên **kho TEST** *(ca `tests/web/ca_wo037.dung_ca_wo037_v2`, assert
`current_database() = 'fls_test'`)*; ca dựng trong **một** lần nạp mới ⇒ ảnh PM
hiệu lực của máy thử là đúng bốn lệnh của ca.

⭐ Mỗi bài ghi **chiều ĐỎ** đã chạy trên mã khi nhận vòng 2 *(`fls/**` =
`4c3b2ae`, HEAD `892a315`)*.
"""
from __future__ import annotations

import ast
import glob
import os
import re

import psycopg
import pytest

from fls.api import xu_ly
from fls.canon.tien_te import ma_tien_te
from fls.db.kho import dsn_test, dsn_that, noi_chi_doc
from fls.repo import lenh_cho as lc
from fls.repo.anh_pm import anh_pm_hieu_luc
from fls.repo.kho_sach import HINH_RUN_THAT
from tests.api.test_wo037_ro_may_theo_cua_ghi_pg import (
    _het_trang, _so_sanh_tien_te_viet_rieng)
from tests.web.ca_wo032 import goi_ca
from tests.web.ca_wo037 import dung_ca_wo037_v2
from tests.web.test_luat_ky_hieu_man_hinh import CAM
from tests.web.test_vong_f02_pg import _may

pytestmark = pytest.mark.pg

GOC = os.path.join(os.path.dirname(__file__), "..", "..", "fls")
RO = "/queue/lenh-cho/ro"
D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"

#: ⭐ Bảng **chữ in** v3.10 *(`BA-07` §4g, đoạn sau bảng ⓐ…ⓓ)* — chép **nguyên
#: văn** từ hợp đồng. Đây là phía **spec** của phép so; phía **mã** là
#: `lc.VI_SAO`. ⛔ Đọc ngược từ `lc.VI_SAO` ra đây — bài sẽ tự so với chính nó.
VI_SAO_V310 = {
    "khong_co_tien_trong_so":
        "có số chứng từ nhưng KHÔNG dòng tiền nào trong sổ mang số ấy — tiền "
        "chưa về, hay nằm trên sheet đã bị xoá khỏi workbook",
    "khong_co_so_chung_tu":
        "chưa có số chứng từ — phải tra bằng TIỀN + NGÀY",
    "ma_khop_khac_tien_te":
        "số chứng từ khớp một dòng tiền bằng {ma} — cửa ghi không ghép hai "
        "tiền tệ, và không ghép theo một số tiền trùng",
}


@pytest.fixture(scope="module")
def ca38():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo037_v2(c)
    with _may() as m:
        yield ca, m


def _ky_hieu_cam(s: str) -> list[str]:
    return sorted({ch for ch in s if ch in CAM})


# ═══ AC-11 *(i · cửa)* — `nguoi_khac_tien_te` ═════════════════════════════════
def test_AC11_ro_tra_NGUOI_KHAC_TIEN_TE_dem_dung_the_vi_sao(ca38):
    """Khoá **luôn có**, kiểu `int`; ca ⇒ `1`; **bằng đúng** số hàng `?ro=nguoi`
    mang `the.vi_sao`; `nguoi − nguoi_khac_tien_te` = số hàng `nguoi` ⛔ mã.

    ⛔ Chiều ĐỎ: ⓐ mã `4c3b2ae` ⇒ khoá vắng ⇒ `KeyError` ⇒ ĐỎ; ⓑ đếm mọi
    `nguoi` có `vi_sao` *(⇒ 3, sổ thật ⇒ 616)* ⇒ ĐỎ."""
    ca, m = ca38
    # ⭐ `WO-051` `AC-10`: phạm vi **của ca** *(`ca_wo032.goi_ca`)*
    d = goi_ca(m, ca, RO)["data"]
    nguoi = goi_ca(m, ca, D_NGUOI)["data"]["rows"]
    co_the = [x["pm_line_id"] for x in nguoi if "vi_sao" in x["the"]]
    rong = [x["pm_line_id"] for x in nguoi if not x.get("ma_canon")]
    print(f"WO-037 AC-11 · kho TEST /ro: {d} · the.vi_sao {len(co_the)} · "
          f"⛔ mã {len(rong)}")
    assert type(d["nguoi_khac_tien_te"]) is int, d
    assert {ca["lenh"][k] for k in "KNT"} <= {x["pm_line_id"] for x in nguoi}
    assert d["nguoi"] == len(nguoi), (d, len(nguoi))
    assert co_the == [ca["lenh"]["K"]], co_the
    assert d["nguoi_khac_tien_te"] == len(co_the) == 1, d
    assert d["nguoi"] - d["nguoi_khac_tien_te"] == len(rong) == 2, d
    assert 0 <= d["nguoi_khac_tien_te"] <= d["nguoi"], d
    # Ba rổ vẫn khép *(⛔ đổi rổ nào)*.
    assert d["may"] + d["nguoi"] + d["khong"] == d["tong"], d


def test_AC11_khoa_CO_MAT_khi_bang_0():
    """`0` ⇒ khoá **vẫn có** *(`BA-07` v3.10: "luôn có mặt, `0` khi ⛔ lệnh
    nào")* — gọi hàm thật trên một phạm vi ⛔ có lệnh nào *(lần nạp ⛔ tồn tại)*.

    ⛔ Chiều ĐỎ: chỉ đặt khoá khi `> 0` ⇒ `KeyError` ⇒ ĐỎ."""
    from fls.repo.pham_vi import mot_lan_nap
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        d = lc.dem_theo_ro(c, mot_lan_nap("NAP-2000-01-01-KHONGCO0000"))
    assert d["tong"] == 0, d
    assert d["nguoi_khac_tien_te"] == 0, d


def test_AC11_SO_THAT_chi_doc_nguoi_khac_tien_te_khop_the_vi_sao():
    """Sổ thật **CHỈ ĐỌC** *(`noi_chi_doc(dsn_that())`, hàm thật, cùng ảnh —
    in `run_id`)*: `nguoi_khac_tien_te` = số thẻ `the.vi_sao` trên `?ro=nguoi`
    *(mọi trang)*; `nguoi − nguoi_khac_tien_te` = số hàng `nguoi` ⛔ mã. Mẫu
    số > 0 *(`Đ3`)*.

    ⛔ Chiều ĐỎ *(mã `4c3b2ae`)*: khoá vắng ⇒ ĐỎ."""
    with noi_chi_doc(dsn_that()) as c:
        assert c.execute("SHOW default_transaction_read_only").fetchone()[0] == "on"
        pv = xu_ly.pham_vi_cua_yeu_cau({})
        run0 = anh_pm_hieu_luc(c, pv)
        d = lc.dem_theo_ro(c, pv)
        nguoi = _het_trang(c, pv, "nguoi")
        run1 = anh_pm_hieu_luc(c, pv)
    co_the = sum(1 for x in nguoi if "vi_sao" in x["the"])
    rong = sum(1 for x in nguoi if not x.get("ma_canon"))
    print(f"WO-037 AC-11 · sổ thật ảnh {run0}: {d} · the.vi_sao {co_the} · "
          f"⛔ mã {rong}")
    assert run0 == run1, f"⛔ ảnh PM trôi giữa phép đo: {run0} → {run1}"
    assert d["nguoi"] > 0 and len(nguoi) == d["nguoi"], (d, len(nguoi))
    assert d["nguoi_khac_tien_te"] == co_the, (d, co_the)
    assert d["nguoi"] - d["nguoi_khac_tien_te"] == rong, (d, rong)


# ═══ AC-13 *(j)* — chữ in v3.10, 0 ký hiệu cấm ════════════════════════════════
def test_AC13_VI_SAO_DUNG_chu_in_v3_10():
    """⛔ Chiều ĐỎ *(mã `4c3b2ae` — chữ v3.9)*: **3 / 3** khoá lệch ⇒ ĐỎ."""
    assert lc.VI_SAO == VI_SAO_V310


def test_AC13_VI_SAO_va_cau_ghep_KHONG_ky_hieu_cam():
    """Mọi giá trị `VI_SAO` ＋ đầu ra `cau_ma_khop_khac_tien_te` *(cả ca mã
    rỗng `(trống)`)* có **0** ký tự trong `CAM` của
    `test_luat_ky_hieu_man_hinh.py` *(dùng lại hằng — ⛔ chép)*.

    ⛔ Chiều ĐỎ *(mã `4c3b2ae`)*: `⛔` ×1 · ×1 · ×2 ⇒ ĐỎ."""
    cau = dict(lc.VI_SAO)
    cau["ghep(USD)"] = lc.cau_ma_khop_khac_tien_te(["USD"])
    cau["ghep(VND, '', USD)"] = lc.cau_ma_khop_khac_tien_te(["VND", "", "USD"])
    xau = {k: _ky_hieu_cam(v) for k, v in cau.items() if _ky_hieu_cam(v)}
    assert not xau, f"⛔ câu cửa mang ký hiệu cấm: {xau}"


def test_AC13_cong_ky_hieu_BAT_DUOC_mot_cau_xau():
    """⭐ Bài cổng tự chứng *(`Đ5`)*: chèn `⛔` vào **bản sao** một giá trị ⇒
    bắt đúng **1**."""
    sao = dict(lc.VI_SAO)
    sao["khong_co_so_chung_tu"] = "⛔ " + sao["khong_co_so_chung_tu"]
    assert sum(1 for v in sao.values() if _ky_hieu_cam(v)) == 1
    assert CAM and "⛔" in CAM, "⛔ hằng CAM rỗng — cổng mù"


# ═══ AC-14 *(k)* — SQL vế sổ `btrim` ═══════════════════════════════════════════
def test_AC14_dong_tien_te_KHOANG_TRANG_vao_BAC_TIEN_va_dem_cung_te(ca38):
    """Lệnh `T` *(VND, ⛔ mã, số tiền `X`)* ↔ dòng chưa nối `curr = ' vnd '` ⛔
    mã khớp, đúng `X` ⇒ `itl-candidates` có dòng ấy bậc `tien`; và
    `tong_cung_tien_te` = số dòng chưa nối trong phạm vi mà
    `upper(btrim(curr)) = 'VND'` *(đếm cả nó)*.

    ⛔ Chiều ĐỎ *(mã `4c3b2ae` — `upper(i.curr)` ⛔ `trim`)*: dòng ⛔ có trong
    `ung_vien` ⇒ ĐỎ; `tong` thiếu mọi dòng `' vnd '` ⇒ ĐỎ."""
    ca, m = ca38
    uv = goi_ca(m, ca, f"/queue/lenh/{ca['lenh']['T']}/itl-candidates?limit=50")["data"]
    x = [u for u in uv["ung_vien"] if u["itl_id"] == ca["i"]["T"]]
    print(f"WO-037 AC-14 · T: {[(u['bac'], u['curr']) for u in uv['ung_vien'][:4]]}"
          f" · tong_cung_tien_te {uv['tong_cung_tien_te']}")
    assert x, "⛔ dòng `' vnd '` đúng số tiền ⛔ ở danh sách ứng viên"
    assert x[0]["bac"] == "tien", x[0]
    # ⚠ *(`WO-042 (c)`, `BA-07` v3.11)*: phía **mong** trước là **một bản SQL**
    #   `upper(btrim(i.curr, E' \t\r\n'))` — `BG-040` yếu #4: mã và bài cùng
    #   trôi một chiều thì xanh; và sau v3.11 tập là **30** ký tự ⇒ bản SQL bốn
    #   ký tự đếm **thiếu** mọi dòng biên khác *(ca `WO-042` để lại dòng NBSP +
    #   VND trong kho TEST)*. Nay phía mong đếm bằng **Python** `ma_tien_te`
    #   *(oracle khác ngôn ngữ với vế đo)*; lo gốc giữ: dòng `' vnd '` vào bậc
    #   `tien` và được đếm, `mong > tho` chứng tập ⛔ rỗng.
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        # ⭐ `WO-051` `AC-10`: cửa hỏi với phạm vi **của ca** ⇒ phía mong đếm
        #   **cùng** phạm vi *(bản trắng ∧ `run_id` của ca — đúng
        #   `PhamVi.mot_lan_nap`)*; lo gốc giữ *(dòng `' vnd '` được đếm,
        #   `mong > tho`)*.
        te = [r[0] for r in c.execute(
            "SELECT i.curr FROM fls_itl i WHERE i.run_id ~ %s AND i.run_id = %s"
            "   AND NOT EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.itl_id = i.itl_id)",
            (HINH_RUN_THAT.pattern, ca["run"])).fetchall()]
    mong = sum(1 for t in te if ma_tien_te(t) == "VND")
    tho = sum(1 for t in te if (t or "").upper() == "VND")
    assert mong > tho, f"⛔ không đo được: kho TEST ⛔ có dòng `' vnd '` ({mong}, {tho})"
    assert uv["tong_cung_tien_te"] == mong, (uv["tong_cung_tien_te"], mong, tho)


# ═══ AC-15 *(l)* — quét so tiền tệ phủ `lenh_cho.py` + ghim `upper(i.curr)` ═══
QUET = (os.path.join(GOC, "api", "xu_ly.py"), os.path.join(GOC, "repo", "lenh_cho.py"))
_UPPER_TRAN = re.compile(r"upper\(\s*i\.curr\s*\)")


@pytest.mark.parametrize("duong", QUET, ids=["xu_ly.py", "lenh_cho.py"])
def test_AC15_QUET_khong_phep_so_tien_te_viet_rieng(duong):
    """⛔ Chiều ĐỎ: thêm `str(x).strip().upper() == …` vào tệp ⇒ ĐỎ."""
    xau = _so_sanh_tien_te_viet_rieng(duong)
    assert not xau, "⛔ so tiền tệ bằng bản riêng — gọi `ma_tien_te`:\n" + "\n".join(xau)


def test_AC15_QUET_bat_duoc_mau_trong_BAN_SAO_lenh_cho(tmp_path):
    """⭐ Tự chứng *(`Đ5`)*: chèn mẫu `str(x).strip().upper() == …` vào **bản
    sao** nguồn `lenh_cho.py` ⇒ bắt **1**. ⛔ Chiều ĐỎ: bài quét chỉ chạy
    `xu_ly.py` *(vòng 1)* ⇒ tệp này ⛔ bao giờ được quét."""
    src = open(QUET[1], encoding="utf-8").read()
    t = tmp_path / "lenh_cho_sao.py"
    t.write_text(src + "\n\ndef _xau(x, y):\n    return str(x).strip().upper() =="
                 " str(y).strip().upper()\n", encoding="utf-8")
    assert len(_so_sanh_tien_te_viet_rieng(str(t))) == 1


def test_AC15_GHIM_khong_chuoi_upper_i_curr_tran_trong_fls():
    """Trong `fls/` **0** chuỗi `upper(i.curr)` trần — vế sổ SQL qua `btrim`.

    ⛔ Chiều ĐỎ *(mã `4c3b2ae`)*: `lenh_cho.py` `_SQL_ITL_UNG_VIEN` +
    `_SQL_DEM_CUNG_TE` ⇒ **2** ⇒ ĐỎ."""
    tep = glob.glob(os.path.join(GOC, "**", "*.py"), recursive=True)
    assert len(tep) > 50, f"⛔ không đo được: chỉ thấy {len(tep)} tệp"
    xau = []
    for p in tep:
        for n, dong in enumerate(open(p, encoding="utf-8"), 1):
            if _UPPER_TRAN.search(dong):
                xau.append(f"{os.path.relpath(p, GOC)}:{n} · {dong.strip()}")
    assert not xau, "⛔ `upper(i.curr)` ⛔ qua `btrim`:\n" + "\n".join(xau)
    assert _UPPER_TRAN.search(" WHERE x AND upper(i.curr) = s.cur")
    assert not _UPPER_TRAN.search("upper(btrim(i.curr, E' \\t\\r\\n')) = s.cur")
    sql = lc._SQL_ITL_UNG_VIEN + lc._SQL_DEM_CUNG_TE
    # ⚠ *(`WO-042 (c)`, `BA-07` v3.11)*: tập là tham số `%(tap)s` từ hằng
    #   `TAP_TRANG_TIEN_TE` *(30)* — ⛔ chuỗi `E' \t\r\n'` *(4)* gõ trong SQL.
    #   Lo gốc giữ: **hai** câu, cả hai qua `btrim`, ⛔ `upper(i.curr)` trần.
    assert sql.count("upper(btrim(i.curr, %(tap)s))") == 2, sql


def test_AC15_ast_dung_duoc_tren_ca_hai_tep():
    """`Đ3`: hai tệp quét **có** phép so `==` *(tập ⛔ rỗng)*."""
    for p in QUET:
        cay = ast.parse(open(p, encoding="utf-8").read())
        assert any(isinstance(n, ast.Compare) for n in ast.walk(cay)), p
