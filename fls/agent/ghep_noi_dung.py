# -*- coding: utf-8 -*-
"""Ghép theo NỘI DUNG giao dịch — bước "thông minh" của A2 (chủ 23/11) + phép chấm fleet eval `a3-1-ref`.

⭐ Vì sao: mã tất định (`pm_join`, v0) chỉ ghép theo Reference No + Σ tiền; dòng ⛔ có Ref, Ref gõ sai, hoặc
   hình D · E · F đều đẩy người. Thẻ eval `a3-1-ref` đo bể ấy: L3 mã rỗng **60** · diễn giải ghi mã khác **136** ·
   D 5 mã/27 dòng · E 119 mã/199 dòng · F 325 mã/452 dòng *(số của thẻ, đo trên ảnh 26/08)*.
   Phần dư ấy cần SUY LUẬN trên nội dung giao dịch + ứng viên — chỗ mô hình lớn có ích (Voi F0b ④).

⭐ Ba thứ ở tệp này, tách bạch:
   `luat_gia_v1`  luật GIẢ tất định đứng thay mô hình ở chế độ giả/phát lại (⛔ phải mô hình thật):
                  mã PM xuất hiện trong nội dung (đã che) + cùng tiền tệ + tiền trong dung sai ⇒ chọn;
                  ⛔ nội dung ⇒ chỉ chọn khi đúng MỘT ứng viên khớp tiền+tiền tệ+ngày; khác ⇒ `DE_NGUOI`.
   `cham`         bộ chấm MÙ theo rubric thẻ `a3-1-ref` (0 = nối sai / nối ca phải-để-người · 1 = đúng lớp,
                  sai line hoặc thiếu lý do · 2 = đúng lớp, đúng line, lý do nêu khoá đã so).
   `tong_hop`     chỉ số vòng: tỉ lệ nối sai · recall nhóm phải-nối · số ca cài sẵn "phải để người" bị nối.
⛔ Đáp án ⛔ bao giờ vào đầu vào agent: `cham` nhận đáp án từ tệp RIÊNG (ngoài repo khi là dữ liệu thật).
"""
from __future__ import annotations

from typing import Any

DE_NGUOI = "DE_NGUOI"


def _ca(cells: dict[str, Any]) -> list[str]:
    return sorted({m.split(":")[1].split(".")[0] for m in cells if m.startswith("noi:")})


def ung_vien(cells: dict[str, Any], ca: str) -> list[dict[str, Any]]:
    ra, i = [], 0
    while f"noi:{ca}.uv.{i}.pm" in cells:
        ra.append({k: cells.get(f"noi:{ca}.uv.{i}.{k}") for k in ("pm", "tien", "cur", "ngay")})
        i += 1
    return ra


def _khop_tien(uv: dict, tien: Any, cur: Any) -> bool:
    ds = 1000 if cur == "VND" else 0
    return (uv["cur"] == cur and isinstance(uv["tien"], (int, float)) and isinstance(tien, (int, float))
            and abs(uv["tien"] - tien) <= ds)


def luat_gia_v1(cells: dict[str, Any]) -> dict[str, Any]:
    """Đứng thay mô hình (GIẢ). Đọc ĐÚNG những gì mô hình thật sẽ thấy — yêu cầu ĐÃ CHE."""
    ra: dict[str, Any] = {}
    for c in _ca(cells):
        tien, cur, nd = cells.get(f"noi:{c}.tien"), cells.get(f"noi:{c}.cur"), cells.get(f"noi:{c}.noi_dung")
        ds = ung_vien(cells, c)
        hop = [u for u in ds if _khop_tien(u, tien, cur)]
        chon, ly = DE_NGUOI, "không đủ chắc"
        if isinstance(nd, str):
            co_ma = [u for u in hop if isinstance(u["pm"], str) and u["pm"] in nd]
            if len(co_ma) == 1:
                chon, ly = co_ma[0]["pm"], "mã PM trong nội dung + tiền + tiền tệ"
        if chon == DE_NGUOI:
            cung_ngay = [u for u in hop if u.get("ngay") == cells.get(f"noi:{c}.ngay")]
            if len(cung_ngay) == 1 and len(hop) == 1:
                chon, ly = cung_ngay[0]["pm"], "ứng viên DUY NHẤT khớp tiền + tiền tệ + ngày"
        ra[f"noi:{c}.chon"] = chon
        ra[f"noi:{c}.ly_do"] = ly
    return ra


def luat_v0(cells: dict[str, Any]) -> dict[str, Any]:
    """Mã tất định hôm nay trên bể này: mọi ca đã là "mã bó tay" ⇒ `DE_NGUOI` (mốc "không tệ hơn")."""
    return {f"noi:{c}.chon": DE_NGUOI for c in _ca(cells)}


def cham(chon: dict[str, Any], dap_an: dict[str, Any]) -> list[dict[str, Any]]:
    """Chấm MÙ từng ca. `dap_an` = `{"noi:<ca>.chon": pm | DE_NGUOI, "noi:<ca>.nhom": "phai_noi" | "phai_nguoi"}`."""
    ra = []
    for c in sorted({m.split(":")[1].split(".")[0] for m in dap_an}):
        dung = dap_an.get(f"noi:{c}.chon")
        nhom = dap_an.get(f"noi:{c}.nhom")
        a = chon.get(f"noi:{c}.chon")
        ly = chon.get(f"noi:{c}.ly_do") or ""
        if a is None:
            d, vi = 0, "rỗng"
        elif a == DE_NGUOI:
            d, vi = (2, "để người đúng") if dung == DE_NGUOI else (1, "để người — an toàn, bỏ lỡ nối")
        elif dung == DE_NGUOI:
            d, vi = 0, "NỐI ca phải để người"
        elif a != dung:
            d, vi = 0, "nối SAI PM line"
        else:
            d, vi = (2, "đúng line, có lý do") if ly else (1, "đúng line, thiếu lý do")
        ra.append({"ca": c, "nhom": nhom, "diem": d, "vi_sao": vi, "noi": a not in (None, DE_NGUOI),
                   "dung_line": a == dung and a != DE_NGUOI})
    return ra


def tong_hop(ds: list[dict[str, Any]]) -> dict[str, Any]:
    noi = [x for x in ds if x["noi"]]
    sai = [x for x in noi if not x["dung_line"]]
    phai_noi = [x for x in ds if x["nhom"] == "phai_noi"]
    phai_nguoi_bi_noi = [x for x in ds if x["nhom"] == "phai_nguoi" and x["noi"]]
    return {
        "so_ca": len(ds),
        "so_noi": len(noi),
        "noi_sai": len(sai),
        "ti_le_noi_sai": (round(len(sai) / len(noi), 4) if noi else None),   # None = 0/0, ⛔ là 0 %
        "recall_phai_noi": (round(sum(1 for x in phai_noi if x["dung_line"]) / len(phai_noi), 4)
                            if phai_noi else None),
        "phai_nguoi_bi_noi": len(phai_nguoi_bi_noi),
        "diem_tb": (round(sum(x["diem"] for x in ds) / len(ds), 4) if ds else None),
    }
