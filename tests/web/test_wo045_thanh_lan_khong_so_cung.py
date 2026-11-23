# -*- coding: utf-8 -*-
"""`WO-045` ⑤ · `AC-13` · `BA-06` **v4.20** `§4.5 ⓦ` ③ — `title` nút thanh lằn
`F01` ⛔ mang **số đo cứng** *(`KQ-046 F-3`)*.

⛔ Lỗi gốc: `man_f01.js:766` `_thanh_lan` — `title` nút `Theo LỆNH CHI` =
*"1.345 dòng lệnh đang chờ tiền — …"*: **1.345** là số đo **09/09** gõ vào
mã; sổ thật 05/10 `/lenh-cho/ro` `tong` **1.601** *(và ⛔ cùng định nghĩa)*.

⭐ Oracle **đọc thẳng** `06_SCREEN_SPEC.md` *(⛔ chép tay — `WO-045` `AC-13`)*:
dòng phương án ⓐ của `ⓦ` ③ là chỗ **duy nhất** spec viết chuỗi ấy trong
backtick ngay sau `` `title` = `` — bài đòi khớp **đúng một** lần *(`Đ5`: mẫu
khớp `0` hoặc `≥ 2` lần là **⛔ đo được**)*.

⚠ Vế *"chữ số"*: `AC-13` viết `/[0-9]/` **0** lần — nhưng chính chuỗi spec
mang mã quyết định `QĐ-ITL-122` *(ba chữ số)*. Hai câu ⛔ cùng đúng nguyên văn
⇒ `HOI` của phiếu *(`KHONG_CHAN`)*; bài làm theo **ý** `ⓦ` ③ *("⛔ mang số đo
cứng")*: bỏ **mã quyết định** `QĐ-ITL-<n>` rồi mới đếm chữ số.
"""
from __future__ import annotations

import os
import re

from tests.web.khung_node import _chay, can_node
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = can_node

SPEC = os.path.join(os.path.dirname(__file__), "..", "..", "docs", "ITL",
                    "02_BA", "06_SCREEN_SPEC.md")
MAU = re.compile(r"ⓐ \*\*Bỏ số\*\* — `title` = `([^`]+)`")


def _chuoi_spec() -> str:
    t = open(SPEC, encoding="utf-8").read()
    assert "**Version:** v4.20" in t or re.search(r"\*\*Version:\*\* v4\.(2[0-9]|[3-9]\d)", t), \
        "⛔ spec cũ hơn v4.20 — ⓦ ③ chưa có"
    ra = MAU.findall(t)
    assert len(ra) == 1, f"⛔ không đo được: mẫu khớp {len(ra)} lần ở spec"
    return ra[0]


def _bo_ma_qd(s: str) -> str:
    return re.sub(r"QĐ-ITL-\d+", "", s)


_VE = """
  F01.ve_man(); await new Promise(r => setTimeout(r, 0));
  return document.querySelectorAll('.tabs button')
    .map(b => ({chu: b.textContent, title: b.title}));
"""


def test_AC13_title_THEO_LENH_CHI_DUNG_chuoi_spec_v4_20():
    """⛔ Chiều ĐỎ: trả lại `1.345` ⇒ ĐỎ; đổi một ký tự chuỗi ⇒ ĐỎ."""
    mong = _chuoi_spec()
    nut = _chay(_VE, tep=TEP_F01, vo=VO_F01)
    theo = {n["chu"]: n["title"] for n in nut}
    assert set(theo) == {"Theo LỆNH CHI", "Theo dòng tiền"}, theo
    assert theo["Theo LỆNH CHI"] == mong, (theo["Theo LỆNH CHI"], mong)


def test_AC13_title_HAI_nut_KHONG_chu_so_ngoai_ma_quyet_dinh():
    nut = _chay(_VE, tep=TEP_F01, vo=VO_F01)
    assert len(nut) == 2, nut
    so = {n["chu"]: re.findall(r"[0-9]", _bo_ma_qd(n["title"])) for n in nut}
    assert not any(so.values()), f"⛔ số cứng trong title: {so}"
    # tự chứng phép đếm *(`Đ5`)*: chuỗi cũ PHẢI bị bắt, mã QĐ ⛔ bị bắt
    assert re.findall(r"[0-9]", _bo_ma_qd("1.345 dòng lệnh (QĐ-ITL-122)")) == list("1345")
    assert not re.findall(r"[0-9]", _bo_ma_qd(_chuoi_spec()))
