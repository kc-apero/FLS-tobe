# -*- coding: utf-8 -*-
"""Mã Ô — đơn vị so của report (Đ4: mỗi ô nói NÓ ĐẾM GÌ qua tiền tố + đường dẫn).

Một mã ô = `<nguồn>:<đường>` · đường là các khoá JSON nối bằng `.` (chỉ số danh sách là số).
  voi:theo_ky.2025-01.co      ← `docs/ITL/_tools/voi_so_luong.json` (HD1 · engine tất định trên ảnh đóng băng)
  hd2:WP-C3a.khop             ← `docs/ITL/_tools/hd2_cong.json` (HD2 · gói gốc `WP-C2` đọc ở `hd2:WP-C2.…`)
  nguon:bank.so_dong          ← ảnh đóng băng 4 nguồn raw (`tests/fixture/…`), máy đếm lại trực tiếp
  cong:HD1_THANG.dat          ← cổng FLS `fls.repo.doc_bao_cao.doc_cong_tep_do/_hd2` (gọi trực tiếp)
  noi:<mã ca>.chon            ← ghép theo NỘI DUNG (A2 · skill 04) — so với đáp án GIỮ RIÊNG, ⛔ với máy

Mẫu có `*` mở rộng trên MỘT tầng khoá — mở rộng trên dữ liệu MÁY, ⛔ trên đầu ra agent
(agent xoá ô ⇒ ô vẫn có trong tập mong ⇒ ĐỎ "agent thiếu ô").
"""
from __future__ import annotations

from typing import Any

VANG = object()          # ⛔ có giá trị ở đường này (khác `None` — `None` là giá trị JSON `null` hợp lệ)


def tach(ma: str) -> tuple[str, list[str]]:
    nguon, _, duong = ma.partition(":")
    return nguon, [p for p in duong.split(".") if p != ""]


def lay(d: Any, phan: list[str]) -> Any:
    x = d
    for p in phan:
        if isinstance(x, dict):
            if p not in x:
                return VANG
            x = x[p]
        elif isinstance(x, list):
            try:
                x = x[int(p)]
            except (ValueError, IndexError):
                return VANG
        else:
            return VANG
    return x


def mo_rong(mau: str, du_lieu: dict[str, Any]) -> list[str]:
    """Mẫu → danh sách mã ô có thật trong `du_lieu[nguồn]` (giữ thứ tự khoá nguồn).

    Lá phải là giá trị VÔ HƯỚNG (số · chuỗi · bool · null) hoặc danh sách vô hướng — mẫu chạm một khối
    dict ⇒ ⛔ ô (khối ⛔ so được một lần; viết mẫu sâu hơn).
    """
    nguon, phan = tach(mau)
    goc = du_lieu.get(nguon, VANG)
    if goc is VANG:
        return []
    ra: list[str] = []

    def di(x: Any, i: int, duong: list[str]) -> None:
        if i == len(phan):
            if isinstance(x, dict):
                return
            if isinstance(x, list) and any(isinstance(y, (dict, list)) for y in x):
                return
            ra.append(f"{nguon}:{'.'.join(duong)}")
            return
        p = phan[i]
        if p == "*":
            if isinstance(x, dict):
                for k in x:
                    di(x[k], i + 1, duong + [str(k)])
            elif isinstance(x, list):
                for j, y in enumerate(x):
                    di(y, i + 1, duong + [str(j)])
            return
        y = lay(x, [p])
        if y is not VANG:
            di(y, i + 1, duong + [p])

    di(goc, 0, [])
    return ra


def gia_tri(ma: str, du_lieu: dict[str, Any]) -> Any:
    nguon, phan = tach(ma)
    goc = du_lieu.get(nguon, VANG)
    return VANG if goc is VANG else lay(goc, phan)
