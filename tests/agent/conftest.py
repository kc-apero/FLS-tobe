# -*- coding: utf-8 -*-
"""`AG3-R1-02` (KQ-361): bài agent ⛔ được để nhật ký GIẢ trong `docs/ITL/06_Agent/nhat_ky/` — nơi nhật ký THẬT nằm
(bản cũ: 4 tệp giả bị commit ở `0e44c81` · `4140a5f`; người đọc thấy nhật ký `google-cloud` có số mà ⛔ lời gọi thật — Đ3).

Hai lớp, tự động cho MỌI bài dưới `tests/agent/`:
  ① đổi hướng `chay_agent_voi.TM_NHAT_KY` → `tmp_path` (hàm `ghi_nhat_ky` đọc biến LÚC GỌI).
  ② lính canh: tập tệp của thư mục nhật ký THẬT trước ≡ sau bài; khác ⇒ bài ĐỎ có tên tệp lạ (bắt cả đường ghi né ①).
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

GOC = Path(__file__).resolve().parents[2]
TM_THAT = GOC / "docs" / "ITL" / "06_Agent" / "nhat_ky"
sys.path.insert(0, str(GOC / "tools"))


def _tep() -> set[str]:
    return {p.name for p in TM_THAT.glob("*")} if TM_THAT.exists() else set()


@pytest.fixture(autouse=True)
def _nhat_ky_ra_tmp(monkeypatch, tmp_path):
    import chay_agent_voi as cav
    truoc = _tep()
    monkeypatch.setattr(cav, "TM_NHAT_KY", tmp_path / "nhat_ky")
    yield
    la = _tep() - truoc
    assert not la, f"bài để lại nhật ký GIẢ trong repo {TM_THAT.relative_to(GOC)}: {sorted(la)}"
