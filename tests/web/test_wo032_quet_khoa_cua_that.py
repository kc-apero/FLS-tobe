# -*- coding: utf-8 -*-
"""`WO-032` `AC-9` ⭐ — cổng quét khoá **mở rộng** của `WO-022` vòng 3 *(tệp
`test_wo022_v3_tim_tien_cua_that.py` — chỉ `F01L`, 2 hàm)* sang **cả hai** màn
ghép: mọi khoá màn đọc từ thân cửa ⊆ khoá **cửa thật** trả, và mọi **khuôn thử
tự dựng** trong `tests/web/**` cho cùng cửa ⊆ khoá cửa thật.

⛔⛔ **Vì sao phải mở rộng** *(`KQ-031`, 02/10)*: `fls-test` đo bằng tay **28**
cặp *(hàm, biến)* — `F01L` 14 · `F01G` 14 — trên **89** thân cửa 8088, và tìm ra
`F-3`: `ve_dang_gan` đọc `g.khoa_to` mà `the.gd` của **cả hai** cửa danh sách
⛔ bao giờ mang *(sổ thật **0 / 768**)*, trong khi bài màn của khối ấy **tự
nhét** `"khoa_to": ["LUONG"]` — **lần thứ ba** của lớp *"khuôn thử tự nhét"*.
Cổng `WO-022` vòng 3 ⛔ thấy được vì nó chỉ quét **hai** hàm `F01L`.

⭐ Bản đồ dưới đây chép **đúng** 28 cặp `KQ-031` đo *(`kq031/doi_chieu.py`)*,
cộng các cặp hàm mới của `WO-032` *(`F01G.khac_tien_te`)* và cửa thứ hai mà
`ve_ung_vien`/`ve_thanh`/`khop_dung_tien` đọc *(`/so`)*. Khoá **đọc** lấy từ
**mã nguồn**; khoá **trả** lấy từ **cửa thật HTTP** trên kho TEST *(ca
`tests/web/ca_wo032.py` — có đủ ca điều kiện: `loi_nguon` · `dien_giai_vi_sao`
· `gd_ds` · `khac_tien_te`)*. ⛔ Danh sách miễn trừ nào: khoá có điều kiện được
đo bằng cách **dựng ca** cho điều kiện ấy xảy ra, ⛔ bằng cách gõ tên.
"""
from __future__ import annotations

import ast
import glob
import os
import re

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.web import phuc_vu as pv
from tests.web.ca_wo032 import dung_ca, goi_het
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo022_v3_tim_tien_cua_that import _than_ham

pytestmark = pytest.mark.pg

#: Phương thức mảng/chuỗi/DOM — ⛔ là khoá thân cửa *(cùng tập `KQ-031`)*.
DOM = {"length", "map", "filter", "forEach", "join", "slice", "push",
       "concat", "indexOf", "reduce", "some", "find", "every", "includes",
       "trim", "toUpperCase", "split"}

SUMMARY, RO, LUOI = "/queue/lenh-cho/summary", "/queue/lenh-cho/ro", "LUOI_VND"
UV, SO, PM, CHUM = ("UV_A", "UV_X"), ("SO_A", "SO_X"), "PM_A", "CHUM_B"
#: ⭐ `WO-037`: + `GHEP_NGUOI` — chip `Chưa gán` gọi **hai** rổ *(`CHIP_CUA`)*.
GHEP = ("GHEP_NGUOI", "GHEP_MAY", "GHEP_DA_GAN")
THE, GD = ("rows", "the"), ("rows", "the", "gd|gd_ds")

#: `(tệp, hàm, biến, thân cửa (khoá goi_het), đường vào thân)`.
BAN_DO = [
    ("man_f01_lenh.js", "_ve_tom", "data", SUMMARY, ()),
    ("man_f01_lenh.js", "_ve_tom", "r", SUMMARY, ("theo_tien_te",)),
    ("man_f01_lenh.js", "_ve_viec", "data", RO, ()),
    ("man_f01_lenh.js", "_ve_ro", "data", RO, ()),
    ("man_f01_lenh.js", "_ve_luoi", "data", LUOI, ()),
    ("man_f01_lenh.js", "_the_dong", "r", LUOI, ("rows",)),
    ("man_f01_lenh.js", "_viec_cua_dong", "r", LUOI, ("rows",)),
    ("man_f01_lenh.js", "_cot_them", "r", LUOI, ("rows",)),
    ("man_f01_lenh.js", "_drawer_tim_tien", "d", UV, ()),
    ("man_f01_lenh.js", "_drawer_tim_tien", "u", UV, ("ung_vien",)),
    ("man_f01_lenh.js", "_drawer_tim_tien", "r", LUOI, ("rows",)),
    ("man_f01_lenh.js", "_tinh", "u", UV, ("ung_vien",)),
    ("man_f01_lenh.js", "_panel_pm", "d", PM, ()),
    ("man_f01_lenh.js", "_panel_pm", "x", PM, ("ca_phieu",)),
    ("man_f01_ghep.js", "tai_danh_sach", "than", GHEP, ()),
    ("man_f01_ghep.js", "the_lenh", "r", GHEP, ("rows",)),
    ("man_f01_ghep.js", "ve_the", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "ve_du_truong", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "ve_du_truong", "nh", GHEP, THE + ("nhom_du_truong",)),
    ("man_f01_ghep.js", "khop_dung_tien", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "khop_dung_tien", "uv", UV + SO, ("ung_vien",)),
    ("man_f01_ghep.js", "khac_tien_te", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "khac_tien_te", "uv", UV + SO, ("ung_vien",)),
    ("man_f01_ghep.js", "ve_ung_vien", "uv", UV, ("ung_vien",)),
    ("man_f01_ghep.js", "ve_ung_vien", "uv", SO, ("ung_vien",)),
    ("man_f01_ghep.js", "ve_thanh", "uv", UV, ("ung_vien",)),
    ("man_f01_ghep.js", "ve_thanh", "uv", SO, ("ung_vien",)),
    ("man_f01_ghep.js", "ve_thanh", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "gan", "uv", UV + SO, ("ung_vien",)),
    ("man_f01_ghep.js", "ve_nguon", "n", UV + SO, ("ung_vien", "nguon")),
    ("man_f01_ghep.js", "ve_dang_gan", "g", GHEP, GD),
    ("man_f01_ghep.js", "ve_tong_chum", "g", ("GHEP_DA_GAN",), THE + ("gd_ds",)),
    ("man_f01_ghep.js", "ve_tong_chum", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "ve_o_gd", "d", GHEP, THE),
    ("man_f01_ghep.js", "ve_o_gd", "g", GHEP, GD),
    ("man_f01_ghep.js", "ve_bang", "d", GHEP, THE),
    ("man_f01_ghep.js", "ve_rail", "d", GHEP, THE),
    ("man_f01_ghep.js", "bo_gan", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "bo_gan", "chum", (CHUM,), ()),
    ("man_f01_ghep.js", "bo_gan", "d", (CHUM,), ("dong_lenh",)),
    ("man_f01_ghep.js", "lenh_ke_tiep", "d", GHEP, THE),
    ("man_f01_ghep.js", "ve", "lenh", GHEP, THE),
    ("man_f01_ghep.js", "_sau_bo_gan", "d", GHEP, THE),
]


@pytest.fixture(scope="module")
def than():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca(c)
    with _may() as m:
        t = goi_het(m, ca)
    t[SUMMARY], t[RO] = t["/queue/lenh-cho/summary"], t["/queue/lenh-cho/ro"]
    return t


def phan_tu(t: dict, cua, duong: tuple) -> list[dict]:
    """Mọi phần tử dict ở `duong` trong các thân `cua`. `a|b` = hợp hai khoá."""
    xs = [t[k] for k in ((cua,) if isinstance(cua, str) else cua)]
    for p in duong:
        nx = []
        for x in xs:
            if not isinstance(x, dict):
                continue
            for k in p.split("|"):
                v = x.get(k)
                if isinstance(v, list):
                    nx += v
                elif v is not None:
                    nx.append(v)
        xs = nx
    return [x for x in xs if isinstance(x, dict)]


def khoa_doc(than_ham: str, bien: str) -> set[str]:
    """Mọi khoá `bien.<k>` / `bien['k']` — ⛔ chú thích, ⛔ phương thức DOM."""
    s = re.sub(r"/\*.*?\*/", "", than_ham, flags=re.S)
    s = re.sub(r"(?m)//.*$", "", s)
    k = (set(re.findall(r"(?<![\w.$])" + re.escape(bien) + r"\.(\w+)", s))
         | set(re.findall(r"(?<![\w.$])" + re.escape(bien)
                          + r"\[['\"](\w+)['\"]\]", s)))
    return k - DOM


def test_AC9_MOI_khoa_F01L_F01G_doc_tu_than_cua_DEU_CO_trong_CUA_THAT(than):
    """⭐ Mỗi cặp *(hàm, biến)*: khoá màn đọc ⊆ hợp khoá **mọi** phần tử cửa
    thật trả ở đường ấy. In mẫu số *(cặp · khoá · phần tử)*.

    ⛔ Chiều ĐỎ *(mã `a718142`)*: `ve_dang_gan`/`ve_o_gd` đọc `g.khoa_to` mà
    `gd`/`gd_ds` ⛔ trả ⇒ ĐỎ. Phá thử: thêm `uv.so_tien` vào `ve_ung_vien` ⇒
    ĐỎ; bỏ một hàng trong bản đồ mà hàm ⛔ còn ⇒ tổng < 28 ⇒ ĐỎ."""
    nguon = {f: open(os.path.join(pv.THU_MUC, f), encoding="utf-8").read()
             for f in {x[0] for x in BAN_DO}}
    thieu, cap, khoa, dong = [], 0, 0, 0
    for tep, ham, bien, cua, duong in BAN_DO:
        doc = khoa_doc(_than_ham(nguon[tep], ham), bien)
        assert doc, f"⛔ không đo được: `{ham}` ⛔ đọc khoá nào qua `{bien}.`"
        pt = phan_tu(than, cua, duong)
        assert pt, f"⛔ không đo được: {ham}.{bien} — 0 phần tử ở {cua} {duong}"
        co = set().union(*(set(x) for x in pt))
        cap += 1
        khoa += len(doc)
        dong += len(pt)
        print(f"WO-032 AC-9 · {tep}:{ham}.{bien} đọc {len(doc)} khoá · "
              f"N={len(pt)} · {sorted(doc)}")
        thieu += [f"{ham}: {bien}.{k} ({cua} {'.'.join(duong)})"
                  for k in sorted(doc - co)]
    print(f"WO-032 AC-9 · TỔNG {cap} cặp (hàm × biến) · {khoa} khoá đọc · "
          f"{dong} phần tử cửa thật")
    assert cap >= 28, f"⛔ mẫu số {cap} < 28 cặp `KQ-031` đã đo"
    assert not thieu, ("⛔ màn đọc khoá cửa THẬT ⛔ trả:\n  " + "\n  ".join(thieu))


# ═══ khuôn thử TỰ DỰNG trong tests/web/** ⊆ khoá cửa thật ═══════════════════
def _dict_khoa(nut: ast.AST) -> set[str] | None:
    """Khoá chuỗi của một `{...}` hoặc `dict(X, k=...)` — `None` nếu ⛔ phải."""
    if isinstance(nut, ast.Dict):
        k = [x.value for x in nut.keys
             if isinstance(x, ast.Constant) and isinstance(x.value, str)]
        return set(k) if k else None
    if (isinstance(nut, ast.Call) and isinstance(nut.func, ast.Name)
            and nut.func.id == "dict"):
        return {kw.arg for kw in nut.keywords if kw.arg}
    return None


_JS_OBJ = re.compile(r"\{\s*itl_id\s*:[^{}]*\}")


def khuon_tu_dung() -> list[tuple[str, str, set[str]]]:
    """`(tệp:dòng, loại, khoá)` của mọi khuôn tự dựng cho cửa khuôn `⓵`
    *(dict có `itl_id` + `bac`, hoặc `dict(<khuôn ⓵>, k=…)`)* và cửa thẻ lệnh
    *(dict có `ma_lenh`)*, trong `tests/web/**` — Python **lẫn** đối tượng JS
    viết trong chuỗi kịch bản."""
    ra = []
    for p in sorted(glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))):
        if os.path.basename(p) in {os.path.basename(__file__)}:
            continue
        src = open(p, encoding="utf-8").read()
        cay = ast.parse(src)
        ten = os.path.basename(p)
        for nut in ast.walk(cay):
            k = _dict_khoa(nut)
            if k is None:
                continue
            if isinstance(nut, ast.Dict) and {"itl_id", "bac"} <= k:
                ra.append((f"{ten}:{nut.lineno}", "uv", k))
            elif isinstance(nut, ast.Dict) and "ma_lenh" in k:
                ra.append((f"{ten}:{nut.lineno}", "the", k))
            elif isinstance(nut, ast.Call) and k and nut.args:
                ra.append((f"{ten}:{nut.lineno}", "uv?", k))
            if isinstance(nut, ast.Constant) and isinstance(nut.value, str):
                pass
        for nut in ast.walk(cay):
            if isinstance(nut, ast.Constant) and isinstance(nut.value, str):
                for m in _JS_OBJ.finditer(nut.value):
                    k = set(re.findall(r"(\w+)\s*:", m.group(0)))
                    if "bac" in k:
                        ra.append((f"{ten}:{nut.lineno}", "uv", k))
    return ra


def test_AC9_KHUON_THU_tu_dung_trong_tests_web_CUNG_la_khuon_cua_that(than):
    """⛔⛔ Lỗi trốn ở **khuôn thử**, ⛔ ở màn. Mọi khuôn ứng viên / `gd` tự
    dựng trong `tests/web/**` *(khoá ⊇ {`itl_id`, `bac`})* phải ⊆ hợp khoá
    khuôn `⓵` cửa thật *(ứng viên `itl-candidates` + `/so` + `gd`/`gd_ds`)*;
    mọi thẻ lệnh tự dựng *(có `ma_lenh`)* ⊆ khoá `the` cửa thật.

    ⛔ Chiều ĐỎ: thêm `"tien": "1.00"` hay `"memo": "x"` vào một khuôn ứng viên
    *(khoá hàng thô `KQ-029 F-1`)* ⇒ ĐỎ; thêm `"khoa_to"` vào một khuôn `gd`
    khi cửa ⛔ trả *(`a718142`)* ⇒ ĐỎ."""
    gd = phan_tu(than, GHEP, GD)
    uv = phan_tu(than, UV + SO, ("ung_vien",)) + gd
    co_uv = set().union(*(set(x) for x in uv))
    # ⭐ Khuôn `gd` *(có `da_gan`)* so với **riêng** `gd`/`gd_ds` cửa thật: hai
    #   cửa ứng viên **đã** trả `khoa_to` từ `23/09`, nên so với hợp chung thì
    #   khuôn `gd` tự nhét `khoa_to` *(`KQ-031 F-3`)* lọt qua — đúng chỗ lỗi trốn.
    co_gd = set().union(*(set(x) for x in gd))
    co_the = set().union(*(set(x) for x in phan_tu(than, GHEP, THE)))
    ds = khuon_tu_dung()
    n_uv = sum(1 for _t, l, _k in ds if l == "uv")
    n_the = sum(1 for _t, l, _k in ds if l == "the")
    print(f"WO-032 AC-9 · khuôn tự dựng: {n_uv} ứng viên/gd · {n_the} thẻ · "
          f"khoá cửa thật: ứng viên {len(co_uv)} · thẻ {len(co_the)}")
    assert n_uv >= 5 and n_the >= 3, f"⛔ không đo được: {n_uv} / {n_the}"
    sai = []
    for tai, loai, k in ds:
        if loai == "uv" and "da_gan" in k:
            thua = k - co_gd
        elif loai == "uv":
            thua = k - co_uv
        elif loai == "the":
            thua = k - co_the
        else:   # `dict(GD, k=…)` — đè khoá lên một khuôn ⓵ ⇒ cùng luật ứng viên
            thua = k - co_uv if k & {"itl_id", "bac", "doc_no", "amount",
                                     "dien_giai"} else set()
        if thua:
            sai.append(f"{tai} [{loai}] {sorted(thua)}")
    assert not sai, ("⛔ khuôn thử tự dựng mang khoá cửa thật ⛔ trả:\n  "
                     + "\n  ".join(sai))


# ═══ `WO-037` — `ve_o_gd` đọc `d.vi_sao` *(câu thứ sáu, `BA-06` v4.16)* ═══════
def test_WO037_ve_o_gd_doc_VI_SAO_va_CUA_THAT_tra_no_o_the(than):
    """⭐ Mở rộng cổng quét *(`WO-037` `(h)`)*: `ve_o_gd` đọc `d.vi_sao`, và
    **cửa thật** trả `vi_sao` **trong `the`** *(⛔ hàng thô — màn đọc `the`)* với
    ≥ 1 câu ⛔ rỗng *(ca `X` của `ca_wo032.py`: lệnh VND khớp mã **chỉ** dòng
    USD ⇒ rổ `nguoi` — `Đ3`: mẫu số > 0)*.

    ⛔ Chiều ĐỎ *(đã chạy)*: ⓐ cửa chở câu ấy dưới một tên khác *(`the.ly_do`)*
    ⇒ khoá màn đọc ⛔ có ở cửa ⇒ bài `AC9` trên **và** bài này ĐỎ; ⓑ cửa ⛔ chở
    *(`xu_ly._gd_vao_the` bỏ dòng `the["vi_sao"]`)* ⇒ ĐỎ."""
    nguon = open(os.path.join(pv.THU_MUC, "man_f01_ghep.js"), encoding="utf-8").read()
    assert "vi_sao" in khoa_doc(_than_ham(nguon, "ve_o_gd"), "d"), \
        "⛔ `ve_o_gd` ⛔ còn đọc `d.vi_sao` — bản đồ trên phải đổi theo"
    co = [x["vi_sao"] for x in phan_tu(than, GHEP, THE) if x.get("vi_sao")]
    print(f"WO-037 · the.vi_sao ⛔ rỗng ở {len(co)} thẻ cửa thật")
    assert co, "⛔ không đo được: cửa thật ⛔ trả `the.vi_sao` ở thẻ nào"
