"""Bài thử kịch bản UAT `docs/ITL/04_Test/UAT_STAGING_E2E.md` — `WO-325` AC-4.

Luật `Đ2`: một con số trong tài liệu phải so với NGUỒN của nó. Mỗi con số HD2 trong UAT mang thẻ `<!--hd2:GÓI.TRƯỜNG-->`;
bài này tính lại từ `docs/ITL/_tools/hd2_cong.json` và đòi KHỚP — đổi một con số ở một bên (tài liệu hay tệp cổng) ⇒ ĐỎ.
Và `Đ3`: số thẻ > 0 (báo cáo "khớp" trên tập rỗng là vô nghĩa).
"""
from __future__ import annotations

import json
import re

import pytest

from tests.staging import ho_tro as H

DOC = H.GOC / "docs" / "ITL" / "04_Test" / "UAT_STAGING_E2E.md"
JSON = H.GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"
CHA = {"WP-C3": ["WP-C3a", "WP-C3b", "WP-C3c", "WP-C3d"], "WP-C4": ["WP-C4a", "WP-C4b", "WP-C4c"], "WP-C5": ["WP-C5a", "WP-C5b"]}


def _vn(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _khoi(d: dict, g: str) -> dict:
    return d if g == "WP-C2" else d[g]


def _mong(d: dict, g: str, k: str) -> int:
    kids = CHA.get(g, [g])
    if k == "lech":
        return sum(_khoi(d, x)["tong_o"] - _khoi(d, x)["khop"] for x in kids)
    return sum(_khoi(d, x)[k] for x in kids)


def _the() -> list[tuple[str, str, str]]:
    return re.findall(r"<!--hd2:([A-Za-z0-9-]+)\.(\w+)-->([0-9.]+)", DOC.read_text(encoding="utf-8"))


def test_moi_con_so_HD2_trong_UAT_khop_hd2_cong_json():
    d = json.loads(JSON.read_text(encoding="utf-8"))
    the = _the()
    # 13 hàng: C2 (2 số: lệch có tên = 0 ⛔ thẻ) · C3a/b/c/d (3) · C3 (3) · C4a/C4b (2 — lệch 0) · C4c (3) · C4 (3) · C5a/b (3+3) · C5 (3)
    assert len(the) == 36, f"{len(the)} thẻ ≠ 36 — thêm/bớt số trong bảng U3 phải đổi bài này (Đ5: khai mong)"
    sai = [(g, k, doc, _vn(_mong(d, g, k))) for g, k, doc in the if doc != _vn(_mong(d, g, k))]
    assert sai == [], sai
    # đủ gói: 10 gói con + 3 gói cha
    assert {g for g, _, _ in the} == {"WP-C2", "WP-C3a", "WP-C3b", "WP-C3c", "WP-C3d", "WP-C3", "WP-C4a", "WP-C4b", "WP-C4c",
                                      "WP-C4", "WP-C5a", "WP-C5b", "WP-C5"}


def test_UAT_doi_mot_con_so_thi_bai_DO__D5():
    """Cổng phải ĐỎ cả hai chiều: sửa một số trong tài liệu (±1) ⇒ phát hiện; sửa trong tệp cổng ⇒ cũng phát hiện."""
    d = json.loads(JSON.read_text(encoding="utf-8"))
    van = DOC.read_text(encoding="utf-8")
    sua = van.replace("<!--hd2:WP-C2.tong_o-->63.016", "<!--hd2:WP-C2.tong_o-->63.017")
    assert sua != van
    sai = [(g, k) for g, k, doc in re.findall(r"<!--hd2:([A-Za-z0-9-]+)\.(\w+)-->([0-9.]+)", sua) if doc != _vn(_mong(d, g, k))]
    assert sai == [("WP-C2", "tong_o")]
    d2 = json.loads(JSON.read_text(encoding="utf-8"))
    d2["WP-C3d"]["khop"] += 1
    sai2 = {(g, k) for g, k, doc in _the() if doc != _vn(_mong(d2, g, k))}
    assert sai2 == {("WP-C3d", "khop"), ("WP-C3d", "lech"), ("WP-C3", "khop"), ("WP-C3", "lech")}


def test_UAT_co_du_muc_AC4_va_gioi_han_O6():
    van = DOC.read_text(encoding="utf-8")
    for can in ("đăng nhập", "Ký tháng", "chạy chuỗi", "4 thẻ", "Ký bản", "605", "615", "D3", "CHECK IX.PL", "O6", "Người test", "ĐẠT / ĐỎ", "Ghi chú"):
        assert can.lower() in van.lower() or can in van, can
    # bảng bước: mỗi hàng có đủ 7 ô và ô "Mong" ⛔ rỗng
    hang = [l for l in van.splitlines() if re.match(r"\| \*\*U\d+\*\*", l)]
    assert len(hang) >= 12, len(hang)
    for l in hang:
        o = [c.strip() for c in l.strip().strip("|").split("|")]
        assert len(o) == 7 and o[2], (l[:80], len(o))
        assert o[3] == o[4] == o[5] == o[6] == "", l[:60]      # ô người test/ngày/ĐẠT-ĐỎ/ghi chú để TRỐNG — người test điền


def test_UAT_khong_chua_thu_cam_va_nhan_dem_gi():
    van = DOC.read_text(encoding="utf-8")
    assert not re.search(r"postgresql://\S+:\S+@", van) and "MKGIA" not in van
    assert "thu@apero.vn" in van and "⛔" in van          # nêu tên mặc định để CẤM, ⛔ dùng
    # Đ4: bảng U3 nói "ô" đếm gì
    assert "ô đáp án so được" in van
    # bảng markdown: không `|` trần trong ô (CLAUDE.md · Bẫy) — số ô mỗi hàng bảng U3 cố định 4
    u3 = [l for l in van.split("### Bảng U3")[1].splitlines() if l.startswith("| ") and "---" not in l][1:]
    assert u3 and all(len(l.strip().strip("|").split("|")) == 4 for l in u3)
