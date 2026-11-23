# -*- coding: utf-8 -*-
"""`WO-037` — rổ `may` đo theo luật **CỬA GHI** · thứ tự trong bậc `ma` · bậc
`khac_tien_te` ở `gd`/`gd_ds` · **một** phép so tiền tệ *(`BA-07` **v3.9**
§4g ⓹ ⓐ ⓑ · §4h ⓵ dòng `bac` · §4h ⓵')*.

⛔⛔ Lỗi gốc *(`KQ-036 F-6`, `fls-ba` đo lại 02/10 — sổ thật chỉ đọc, hàm thật,
ảnh PM `NAP-2026-10-02-PMA07ED283`; `fls-dev` đo lại ở cổng vào **cùng ảnh**:
khớp từng số)*: `lenh_cho.xep_ro` cho lệnh vào rổ `may` *("máy trả lời được —
người chỉ DUYỆT")* chỉ vì có một dòng tiền **khớp mã**, ⛔ hỏi tiền tệ ⇒ **84 /
268** lệnh rổ `may` có đề xuất đầu *(`the.gd`)* là dòng **khác tiền tệ** — cặp
mà cửa ghi **từ chối** *(`QĐ-ITL-62`, `KhacTienTe`)*; cả **84 / 84** ⛔ có dòng
khớp mã nào cùng tiền tệ. Một rổ hứa nhiều hơn cái bấm được — cùng lớp lỗi
`584` → `68` của `tap_tu_chung`.

⛔ **Vì sao ⛔ vá bằng "đưa ứng viên cùng tiền tệ lên đầu"** *(`BA-07` v3.9
§4g ⓹)*: **45** trong 84 lệnh có ứng viên cùng tiền tệ lệch `0`, nhưng mỗi lệnh
có trung vị **16** dòng cùng số ấy, cách dòng khớp mã trung vị **294 ngày** ⇒
trùng tiền **tình cờ**. Đưa chúng lên đầu là đổi một cú bấm bị **TỪ CHỐI** lấy
một cú ghép **SAI mà cửa ghi NHẬN**. ⇒ Bài `AC-3` canh chiều ấy.

⛔ Luật của tệp *(`BA-07` §4h ⓵ — luật bài thử)*: mọi thân đo đi ra từ **cửa
HTTP thật** trên **kho TEST** *(assert `current_database() = 'fls_test'`)*; ca
dựng trong **một** lần nạp mới, cửa hỏi với `?run_id=<lần nạp>` *(ảnh PM
hiệu lực = ảnh **của ca** — `WO-051` `AC-10`: trước đó bài dựa vào *"ảnh mới
nhất của cả kho TEST là ảnh của ca"*, gãy khi tiến trình khác nạp ảnh)*,
tiền + mã ngẫu nhiên *(kho TEST phình — ⛔ `TRUNCATE`)*.
"""
from __future__ import annotations

import ast
import os
import re

import psycopg
import pytest

from fls.api import xu_ly
from fls.db.kho import dsn_test, dsn_that, noi_chi_doc
from fls.repo import lenh_cho as lc
from fls.repo import man_ghep as mg
from tests.web.ca_wo032 import goi_ca, hang
from tests.web.ca_wo037 import _tien, dung_ca_wo037
from tests.web.test_vong_f02_pg import _may

pytestmark = pytest.mark.pg

GOC = os.path.join(os.path.dirname(__file__), "..", "..", "fls")
D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"
#: ⚠ Rổ `may` = **hai** danh sách *(`tu_chung=0` · `=1`)* — lệnh mà cửa ghi nhận
#: theo lô *(`ds_tu_chung`)* ⛔ nằm trong `tu_chung=0`. Đo rổ thì hỏi **cả hai**.
D_MAY_TC = "/queue/lenh-cho?ro=may&tu_chung=1&limit=500"
D_DA_GAN = "/queue/lenh-da-gan?limit=500"


@pytest.fixture(scope="module")
def ca37():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo037(c)
    with _may() as m:
        yield ca, m


def _ma_trong(than: dict) -> set[str]:
    return {x.get("pm_line_id") for x in than.get("rows") or []}


def _ro_may(m, ca) -> dict:
    """Thân rổ `may` **đủ** — hợp hai danh sách `tu_chung=0` ＋ `=1`.
    ⭐ `WO-051` `AC-10`: mọi cửa trong tệp hỏi với phạm vi **của ca**
    *(`ca_wo032.goi_ca` — ảnh PM hiệu lực = ảnh **của ca**, ⛔ ảnh mới nhất
    của cả kho TEST)*."""
    return {"rows": goi_ca(m, ca, D_MAY)["data"]["rows"]
            + goi_ca(m, ca, D_MAY_TC)["data"]["rows"]}


# ═══ AC-1 *(a)* — rổ `may` ⇔ khớp mã **CÙNG** tiền tệ ════════════════════════
def test_AC1_khop_ma_CHI_khac_tien_te_vao_ro_NGUOI_kem_vi_sao_ma_tien_te(ca37):
    """⛔ Chiều ĐỎ *(mã `8d7bea2`)*: `xep_ro` ⛔ so tiền tệ ⇒ `K` ở rổ `may`,
    `the.gd.curr = 'USD'` *(đề xuất một cặp cửa ghi từ chối)* ⇒ ĐỎ."""
    ca, m = ca37
    k = ca["lenh"]["K"]
    nguoi, may = goi_ca(m, ca, D_NGUOI)["data"], _ro_may(m, ca)
    assert k not in _ma_trong(may), "⛔ lệnh chỉ khớp mã ở USD vẫn ở rổ `may`"
    x = hang(nguoi, k)
    assert x["ro"] == "nguoi", x["ro"]
    assert "USD" in x["vi_sao"] and "tiền tệ" in x["vi_sao"], x["vi_sao"]
    assert x["vi_sao"] == lc.cau_ma_khop_khac_tien_te(["USD"]), x["vi_sao"]
    assert x["ung_vien_itl"] == [], x["ung_vien_itl"]
    assert x["tu_chung"] is False
    assert x["the"]["gd"] is None, x["the"]["gd"]


def test_AC1_them_dong_VND_cung_ma_thi_lenh_VE_ro_MAY_de_xuat_VND(ca37):
    """Cùng lệnh, thêm **một** dòng VND mang mã ấy ⇒ lệnh về `may`,
    `the.gd.curr == 'VND'` *(đề xuất ⛔ bao giờ là dòng USD — `§4h ⓵'`)*.

    ⛔ Chiều ĐỎ: `ung_vien_itl` mang cả dòng USD *(xếp `itl_id`)* ⇒ `gd` USD ⇒ ĐỎ."""
    ca, m = ca37
    w = ca["lenh"]["W"]
    assert w in _ma_trong(goi_ca(m, ca, D_NGUOI)["data"]), "⛔ nền: W phải ở `nguoi`"
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        assert c.execute("SELECT current_database()").fetchone()[0] == "fls_test"
        i_vnd = _tien(c, ca["run"], ca["nguon_vnd"], 8,
                      f"{ca['tien']['W'] + 7}.00", "VND", ca["doc"]["W"])
    may = _ro_may(m, ca)
    x = hang(may, w)
    assert x["ro"] == "may" and x["vi_sao"] == "", (x["ro"], x["vi_sao"])
    assert x["ung_vien_itl"] == [i_vnd], x["ung_vien_itl"]
    assert x["the"]["gd"]["curr"] == "VND", x["the"]["gd"]
    assert w not in _ma_trong(goi_ca(m, ca, D_NGUOI)["data"])


def test_AC1_tien_te_co_KHOANG_TRANG_la_CUNG_tien_te(ca37):
    """`' vnd '` ≡ `VND` *(`trim` + chữ hoa — **cùng** `mg.ma_tien_te` của
    `lech_ung_vien`)* ⇒ rổ `may`.

    ⛔ Chiều ĐỎ: so ⛔ `trim` *(`str(curr).upper()`)* ⇒ `S` sang `nguoi` ⇒ ĐỎ."""
    ca, m = ca37
    x = hang(_ro_may(m, ca), ca["lenh"]["S"])
    assert x["ro"] == "may", x
    assert x["ung_vien_itl"] == [ca["i"]["S"]], x["ung_vien_itl"]
    assert mg.ma_tien_te(x["the"]["gd"]["curr"]) == "VND", x["the"]["gd"]


def test_AC1_dem_theo_ro_KHEP_va_khop_danh_sach(ca37):
    """`/lenh-cho/ro` đếm **cùng** luật với danh sách *(một `xep_ro`)*: ba rổ
    khép về `tong`, và `may`/`nguoi` = số hàng hai cửa danh sách trả."""
    ca, m = ca37
    d = goi_ca(m, ca, "/queue/lenh-cho/ro")["data"]
    assert d["may"] + d["nguoi"] + d["khong"] == d["tong"], d
    assert d["may"] == len(_ro_may(m, ca)["rows"]), d
    assert d["nguoi"] == len(goi_ca(m, ca, D_NGUOI)["data"]["rows"]), d


# ═══ AC-3 *(b)* — trong bậc `ma`: cùng tiền tệ › khác tiền tệ › bậc tiền ═══════
def test_AC3_bac_MA_cung_tien_te_TRUOC_khac_tien_te_TRUOC_bac_tien(ca37):
    """⛔ Chiều ĐỎ: ⓐ xếp theo `itl_id` *(mã `8d7bea2`)* ⇒ USD *(id nhỏ)* đứng
    đầu ⇒ ĐỎ; ⓑ hạ dòng mã khác tiền tệ xuống dưới bậc tiền ⇒ `[1]` là dòng
    bậc `tien` ⇒ ĐỎ."""
    ca, m = ca37
    i = ca["i"]
    assert i["Y_usd"] < i["Y_vnd"], "⛔ nền: dòng USD phải có `itl_id` nhỏ hơn"
    uv = goi_ca(m, ca, f"/queue/lenh/{ca['lenh']['Y']}/itl-candidates?limit=50"
                )["data"]["ung_vien"]
    ids = [u["itl_id"] for u in uv]
    print(f"WO-037 AC-3 · itl-candidates Y: {[(u['bac'], u['curr']) for u in uv[:4]]}")
    assert ids[:3] == [i["Y_vnd"], i["Y_usd"], i["Y_tien"]], ids[:3]
    assert [(u["bac"], u["curr"]) for u in uv[:3]] == [
        ("ma", "VND"), ("ma", "USD"), ("tien", "VND")], uv[:3]


# ═══ AC-4 *(c · `F-2`)* — `gd_ds` khác tiền tệ ⛔ khớp mã ⇒ `khac_tien_te` ═════
def test_AC4_gd_ds_KHAC_tien_te_khong_khop_ma_la_bac_KHAC_TIEN_TE(ca37):
    """⛔ Chiều ĐỎ *(mã `8d7bea2`)*: nhánh cuối `_bac` `return 'cung_tien_te'`
    ⇒ dòng USD dưới lệnh VND mang *"cùng đơn vị tiền"* ⇒ ĐỎ."""
    ca, m = ca37
    x = hang(goi_ca(m, ca, D_DA_GAN)["data"], ca["lenh"]["G"])
    ds = [u for u in x["the"]["gd_ds"] if u.get("itl_id") == ca["i"]["G"]]
    assert ds, f"⛔ không đo được: gd_ds ⛔ có {ca['i']['G']}"
    assert ds[0]["curr"] == "USD" and ds[0]["lech"] is None, ds[0]
    assert ds[0]["bac"] == "khac_tien_te", ds[0]
    assert x["the"]["gd"]["bac"] == "khac_tien_te", x["the"]["gd"]


# ═══ AC-5 *(d · `F-1`)* — MỘT phép so tiền tệ ═════════════════════════════════
@pytest.mark.parametrize("cu, cl, mong", [
    (" vnd ", "VND", "tien"), ("VND", " vnd", "tien"), ("usd", "VND", "khac_tien_te"),
    ("VND", "VND", "tien")])
def test_AC5_bac_so_tien_te_CUNG_LUAT_voi_lech_ung_vien(cu, cl, mong):
    """`_bac` và `lech_ung_vien` nói **cùng** một câu về *"cùng tiền tệ"*.

    ⛔ Chiều ĐỎ *(mã `8d7bea2`)*: `' vnd '` ↔ `VND` ⇒ `_bac` `cung_tien_te`
    trong khi `lech_ung_vien` ⇒ `0` ⇒ ĐỎ."""
    d = {"ma_canon": None, "curr": cl, "amount": "100.00"}
    r = {"doc_no": "WO37-KHAC-MA", "curr": cu, "tien": "100.00"}
    assert xu_ly._bac(d, r) == mong, xu_ly._bac(d, r)
    assert (mg.lech_ung_vien("100.00", cu, "100.00", cl) is None) == (
        mong == "khac_tien_te")


def _so_sanh_tien_te_viet_rieng(duong: str) -> list[str]:
    """Mọi phép so `==`/`!=` mà một vế là lời gọi `.upper()`/`.lower()`/
    `.casefold()` *(bản riêng của `ma_tien_te`)* ⇒ `[tệp:dòng · đoạn mã]`."""
    src = open(duong, encoding="utf-8").read()
    ra = []
    for n in ast.walk(ast.parse(src)):
        if not isinstance(n, ast.Compare):
            continue
        if not any(isinstance(o, (ast.Eq, ast.NotEq)) for o in n.ops):
            continue
        for v in [n.left, *n.comparators]:
            if (isinstance(v, ast.Call) and isinstance(v.func, ast.Attribute)
                    and v.func.attr in {"upper", "lower", "casefold"}):
                ra.append(f"{os.path.basename(duong)}:{n.lineno} · "
                          f"{ast.get_source_segment(src, n)}")
                break                   # ⛔ đếm đôi khi CẢ HAI vế đều gọi `.upper()`
    return ra


def test_AC5_QUET_xu_ly_KHONG_co_phep_so_tien_te_viet_rieng():
    """⛔ Chiều ĐỎ: thêm lại `str(r.get('curr') or '').upper() == …` vào
    `xu_ly.py` ⇒ ĐỎ *(đã chạy trên mã `8d7bea2`: 1 chỗ, `xu_ly.py:764`)*. ⭐ Bài
    tự chứng nó bắt được: chạy trên một tệp dựng sẵn mang đúng mẫu ấy."""
    p = os.path.join(GOC, "api", "xu_ly.py")
    xau = _so_sanh_tien_te_viet_rieng(p)
    assert not xau, "⛔ so tiền tệ bằng bản riêng — gọi `mg.ma_tien_te`:\n" + \
        "\n".join(xau)
    src = open(p, encoding="utf-8").read()
    assert "mg.ma_tien_te(" in src, "⛔ `_bac` ⛔ gọi `mg.ma_tien_te`"


def test_AC5_QUET_bat_duoc_mau_cu(tmp_path):
    """⭐ Bài quét phải **ĐỎ được** *(`Đ5`)* — mẫu nguyên văn `KQ-036 F-1`."""
    t = tmp_path / "x.py"
    t.write_text("def f(r, d):\n    return str(r.get('curr') or '').upper() =="
                 " str(d.get('curr') or '').upper()\n", encoding="utf-8")
    assert len(_so_sanh_tien_te_viet_rieng(str(t))) == 1


# ═══ `the.vi_sao` — câu thay đề xuất, CHỈ khi khớp mã chỉ ở tiền tệ khác ══════
def test_THE_vi_sao_CHI_CO_khi_khop_ma_chi_khac_tien_te(ca37):
    """`the.vi_sao` = **đúng** `vi_sao` của hàng ⇔ `ro = nguoi` vì khớp mã chỉ ở
    tiền tệ khác *(`HOI-038` phương án B)*; mọi hàng khác ⛔ có khoá ấy
    *(vắng ⇒ ô `Giao dịch` giữ năm câu cũ — `BA-06` v4.16 §4.5)*."""
    ca, m = ca37
    k = hang(goi_ca(m, ca, D_NGUOI)["data"], ca["lenh"]["K"])
    assert k["the"]["vi_sao"] == k["vi_sao"], k["the"]
    for than in (_ro_may(m, ca), goi_ca(m, ca, D_DA_GAN)["data"]):
        for x in than["rows"]:
            assert "vi_sao" not in x["the"], (x["pm_line_id"], x["the"].get("vi_sao"))


# ═══ AC-2 *(a · sổ THẬT, CHỈ ĐỌC)* ════════════════════════════════════════════
def _het_trang(c, pv, ro):
    rows, cur = [], None
    while True:
        q = {"limit": "500", "ro": ro, **({"cursor": cur} if cur else {})}
        out, _ = xu_ly.lenh_cho(xu_ly.YeuCau(conn=c, pv=pv, q=q, tham={}))
        rows += out["rows"]
        cur = out["next_cursor"]
        if not cur:
            return rows


def test_AC2_SO_THAT_chi_doc_ro_MAY_KHONG_de_xuat_dong_khac_tien_te():
    """Sổ thật **chỉ đọc** *(`noi_chi_doc(dsn_that())`, gọi `xu_ly.lenh_cho` —
    chính hàm của cửa — mọi trang)*: **0** lệnh rổ `may` có `the.gd` khác tiền
    tệ; mọi lệnh `nguoi` mang câu `ma_khop_khac_tien_te` có `gd = null`. Mẫu số
    in ra > 0 *(`Đ3`)*.

    ⛔ Chiều ĐỎ *(mã `8d7bea2`, ảnh `NAP-2026-10-02-PMA07ED283`)*: **84 / 268**
    ⇒ ĐỎ."""
    with noi_chi_doc(dsn_that()) as c:
        assert c.execute("SHOW default_transaction_read_only").fetchone()[0] == "on"
        pv = xu_ly.pham_vi_cua_yeu_cau({})
        may, nguoi = _het_trang(c, pv, "may"), _het_trang(c, pv, "nguoi")
    khac = [x["pm_line_id"] for x in may
            if x["the"].get("gd") and mg.ma_tien_te(x["the"]["gd"].get("curr"))
            != mg.ma_tien_te(x["curr"])]
    print(f"WO-037 AC-2 · sổ thật: may {len(may)} · gd khác tiền tệ {len(khac)}"
          f" · nguoi {len(nguoi)}")
    assert may, "⛔ không đo được: rổ `may` rỗng"
    assert not khac, f"⛔ {len(khac)} lệnh rổ `may` đề xuất dòng khác tiền tệ: {khac[:5]}"
    mau = re.escape(lc.VI_SAO["ma_khop_khac_tien_te"]).replace(r"\{ma\}", ".+")
    nk = [x for x in nguoi if re.fullmatch(mau, x["vi_sao"] or "")]
    print(f"WO-037 AC-2 · nguoi mang vi_sao ma_khop_khac_tien_te {len(nk)}")
    assert nk, "⛔ không đo được: 0 lệnh `nguoi` mang câu `ma_khop_khac_tien_te`"
    assert all(x["the"]["gd"] is None and x["ung_vien_itl"] == [] for x in nk)
