# -*- coding: utf-8 -*-
"""Phép so Ô agent ↔ MÁY ĐÃ ĐO — lõi TẤT ĐỊNH của A4 Auditor (`WO-329` AC-4 · AC-5).

⭐ Chủ 23/11: *"khớp 100 %"* = đầu ra agent BẰNG số máy đã đo, lệch **0** từng ô.
   · Tập ô MONG = mẫu của skill mở rộng trên DỮ LIỆU MÁY (⛔ trên đầu ra agent) — agent bỏ ô ⇒
     `AGENT_THIEU` (đỏ); agent thêm ô ngoài tập ⇒ `AGENT_THUA` (đỏ).
   · Nguồn máy VẮNG (xoá đầu vào một lớp) hoặc mẫu mở ra 0 ô ⇒ `KHONG_DO_DUOC` (đỏ — Đ3 · Đ5:
     phép ⛔ đo được là ĐỎ, ⛔ "không thấy lệch").
   · So bằng GIÁ TRỊ JSON, phân biệt bool với số (`True == 1` của Python ⛔ được tính là khớp).
⭐ Skill `loai: bong` (G0 bóng — ghép theo nội dung) so với ĐÁP ÁN GIỮ RIÊNG, ⛔ với máy; kết quả ở khối
   riêng của report và ⛔ cộng vào lệch agent ↔ máy (AP Voi: G0 = chạy song song, ⛔ ghi, so với người).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fls.agent.o import VANG, gia_tri, mo_rong

KHOP, LECH, KHONG_DO_DUOC, AGENT_THIEU, AGENT_THUA, CHUA_CHAY = (
    "KHOP", "LECH", "KHONG_DO_DUOC", "AGENT_THIEU", "AGENT_THUA", "CHUA_CHAY")
TRANG_THAI_DO = (LECH, KHONG_DO_DUOC, AGENT_THIEU, AGENT_THUA, CHUA_CHAY)


@dataclass(frozen=True)
class O:
    ma: str
    skill: str          # `A1_RI/01_…`
    agent: Any
    may: Any
    trang_thai: str
    ly_do: str = ""

    @property
    def do(self) -> bool:
        return self.trang_thai in TRANG_THAI_DO


def bang(a: Any, b: Any) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(bang(x, y) for x, y in zip(a, b))
    return a == b and type(a) in (int, float, str, type(None)) and type(b) in (int, float, str, type(None))


def mong_cua(mau_o: tuple[str, ...], may: dict[str, Any]) -> tuple[list[str], list[tuple[str, str]]]:
    """(tập ô mong, [(mẫu, lý do ⛔ đo được)]). Danh sách sau khác rỗng ⇒ phép này ĐỎ."""
    ma: list[str] = []
    ly: list[tuple[str, str]] = []
    for m in mau_o:
        nguon = m.split(":", 1)[0]
        if nguon not in may or may[nguon] is None:
            ly.append((m, f"nguồn máy `{nguon}` VẮNG ⇒ ⛔ đo được"))
            continue
        x = mo_rong(m, may)
        if not x:
            ly.append((m, "mẫu mở ra 0 ô trên máy (Đ3)"))
        ma += [y for y in x if y not in ma]
    return ma, ly


def doi_chieu_skill(nhan_skill: str, mau_o: tuple[str, ...], ra_agent: dict[str, Any] | None,
                    may: dict[str, Any], bo_qua_hau_to: tuple[str, ...] = (".ly_do",)) -> list[O]:
    """So mọi ô của MỘT skill. `ra_agent=None` ⇒ skill chưa chạy (mọi ô `CHUA_CHAY`)."""
    mong, ly = mong_cua(mau_o, may)
    ra: list[O] = [O(ma=m, skill=nhan_skill, agent=VANG, may=VANG, trang_thai=KHONG_DO_DUOC, ly_do=x)
                   for m, x in ly]
    for m in mong:
        if m.endswith(bo_qua_hau_to):
            continue
        mv = gia_tri(m, may)
        if ra_agent is None:
            ra.append(O(m, nhan_skill, VANG, mv, CHUA_CHAY, "skill chưa chạy (chuỗi dừng trước)"))
            continue
        av = ra_agent.get(m, VANG)
        if av is VANG:
            ra.append(O(m, nhan_skill, av, mv, AGENT_THIEU, "agent ⛔ trả ô này"))
        elif bang(av, mv):
            ra.append(O(m, nhan_skill, av, mv, KHOP))
        else:
            ra.append(O(m, nhan_skill, av, mv, LECH, "agent ≠ máy"))
    if ra_agent is not None:
        tap = set(mong)
        for m in ra_agent:
            if m not in tap and not m.endswith(bo_qua_hau_to):
                ra.append(O(m, nhan_skill, ra_agent[m], VANG, AGENT_THUA, "ô ngoài tập mong (agent tự thêm)"))
    return ra


def tom_tat(ds: list[O]) -> dict[str, int]:
    dem = {k: 0 for k in (KHOP,) + TRANG_THAI_DO}
    for o in ds:
        dem[o.trang_thai] += 1
    dem["mau_so"] = len(ds)
    return dem
