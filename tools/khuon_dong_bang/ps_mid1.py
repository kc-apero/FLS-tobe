"""Khuôn đóng băng `ps_mid1` — ĐÁP ÁN MID1 phân bổ 7 CDT1 (`D,J,K,Q,M,R,T,U,V,F,S`) của PS *(ISP 3.1.2 · DT9 · `WO-220`)*.

    python tools/dong_bang_sheet.py ps_mid1 <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dap_an/ps_mid1.json

Thân + số MONG ở `_nen_tang.py` *(bảng `DO[("ps", 1)]`)* — xem docstring ở đó.
"""
from __future__ import annotations

import importlib.util
import pathlib
import sys

_P = pathlib.Path(__file__).resolve().parent / "_nen_tang.py"
_spec = importlib.util.spec_from_file_location("khuon_dong_bang__nen_tang", _P)
_nt = sys.modules.get(_spec.name) or importlib.util.module_from_spec(_spec)
if _spec.name not in sys.modules:
    sys.modules[_spec.name] = _nt
    _spec.loader.exec_module(_nt)

globals().update(_nt.tao("ps", 1))
