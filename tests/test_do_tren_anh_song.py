# -*- coding: utf-8 -*-
"""WO-345 — `tools/do_tren_anh_song.chuyen_huong`: đo HD2 trên ảnh MỚI = chuyển MỌI lần mở `tests/fixture/**/X.json`
sang `X<hậu tố>.json` NẾU có. Bẫy canh: (1) chuyển im lặng ảnh ⛔ có bản mới ⇒ `FileNotFoundError` giả; (2) hậu tố
rỗng (đo ảnh CŨ) mà vẫn chuyển ⇒ "CŨ" thật ra là MỚI; (3) tệp ngoài `tests/fixture` bị chuyển; (4) chuyển mà ⛔ ghi
lại ⇒ BG ⛔ nói được gói đã đọc ảnh nào (Đ4)."""
from __future__ import annotations

import json
from pathlib import Path

from tools import do_tren_anh_song as t

GOC = Path(__file__).resolve().parents[1]
CO_MOI = GOC / "tests" / "fixture" / "dau_vao" / "ccr_so_du_ccr.json"        # có `_20261123` (WO-345)
KHONG_MOI = GOC / "tests" / "fixture" / "dap_an" / "gl_406.json"              # ≡ ⇒ ⛔ có tệp mới


def _ck(p) -> str:
    with open(p, encoding="utf-8") as f:
        return json.load(f)["checksum_noi_dung"]


def test_chuyen_khi_co_anh_moi_va_ghi_lai():
    da: dict[str, str] = {}
    with t.chuyen_huong("_20261123", da):
        moi = _ck(CO_MOI)
        moi_path = _ck(Path(CO_MOI))
        cu_khac = _ck(KHONG_MOI)
    assert moi == moi_path == "89b8fafe" + moi[8:] and moi != _ck(CO_MOI)
    assert da == {"dau_vao/ccr_so_du_ccr.json": "dau_vao/ccr_so_du_ccr_20261123.json"}
    assert cu_khac == _ck(KHONG_MOI)                                           # ⛔ bản mới ⇒ đọc ảnh cũ


def test_hau_to_rong_khong_chuyen():
    da: dict[str, str] = {}
    with t.chuyen_huong("", da):
        assert _ck(CO_MOI).startswith("9693d0a5")                             # ảnh CŨ (DT13)
    assert da == {}


def test_tra_nguyen_open_sau_khoi(tmp_path):
    da: dict[str, str] = {}
    with t.chuyen_huong("_20261123", da):
        pass
    assert _ck(CO_MOI).startswith("9693d0a5")
    ngoai = tmp_path / "x.json"
    ngoai.write_text('{"checksum_noi_dung": "ngoai"}', encoding="utf-8")
    (tmp_path / "x_20261123.json").write_text('{"checksum_noi_dung": "sai"}', encoding="utf-8")
    with t.chuyen_huong("_20261123", da):
        assert _ck(ngoai) == "ngoai"                                          # ngoài tests/fixture ⇒ ⛔ chuyển
