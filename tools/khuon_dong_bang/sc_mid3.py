"""Khuôn đóng băng `sc_mid3` — ĐÁP ÁN MID3 Platform Data (`O,P,S…AF,H,F`) + cổng Σ chia = O/P của SC *(ISP 3.1.2 · DT9 · `WO-220`)*.

    python tools/dong_bang_sheet.py sc_mid3 <bản_thô.json> --mong <số dòng ảnh>
        ⇒ tests/fixture/dap_an/sc_mid3.json

Thân + số MONG ở `_nen_tang.py` *(bảng `DO[("sc", 3)]`)* — xem docstring ở đó.
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

globals().update(_nt.tao("sc", 3))
