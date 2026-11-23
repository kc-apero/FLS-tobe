# -*- coding: utf-8 -*-
"""Chuỗi 4 agent: A1 → A2 → A3 → A4 — TUẦN TỰ, có cửa (`WO-329` AC-2).

⭐ Hai tầng cửa:
   ① trong một agent: skill `n+1` chỉ chạy khi cổng ra của skill `n` ĐẠT (`cong_skill.py`);
   ② giữa hai agent: agent `k+1` chỉ chạy khi A4 (phép so `doi_chieu.py`, MÃ) cho agent `k` ĐẠT —
      mọi ô của các skill `lam` khớp máy (lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0).
   Dừng ở đâu ⇒ `KqChuoi.dung_o` mang TÊN chỗ dừng (agent/skill + cổng + lý do) — ⛔ "lỗi chung".
⭐ Skill `bong` (G0 bóng) chịu cổng ① (luật cứng) nhưng ⛔ vào cửa ② — nó so với ĐÁP ÁN giữ riêng, ở khối riêng.
⭐ Skill `ma` ⛔ gọi mô hình: `01_soat_lop` = chính cửa ②; `04_report` = sinh trang (tools/chay_agent_voi.py).

Vòng một skill `lam`/`bong` (khuôn Messages, xem `mo_hinh.py`): user = prompt skill · mô hình gọi ĐÚNG công cụ
của skill (tên khác ⇒ dừng) · kết quả công cụ (phía máy) đi vào `tool_result` · MỌI yêu cầu qua `che.che_yeu_cau` (chế độ mặc định `mo` — chủ 23/11)
TRƯỚC khi tới nhà cung cấp · mô hình trả chữ JSON `{mã ô: giá trị}`. Tối đa `SO_LUOT_TOI_DA` lượt.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Callable

from fls.agent import che as che_mod
from fls.agent import doi_chieu as dc
from fls.agent.cong_skill import chay_cong
from fls.agent.mo_hinh import GEMINI_FLASH, OPUS_5_5, MoHinh, NhaCungCap
from fls.agent.skill import Skill, checksum_prompt, he_thong, nap_bo

SO_LUOT_TOI_DA = 4
MAX_TOKENS = 16000


@dataclass(frozen=True)
class DinhNghiaAgent:
    ma: str
    ten: str
    mo_hinh: MoHinh


#: Thứ tự chuỗi. Phương án A (Voi phase 1 §F0b — PROPOSED): A1–A3 Claude Opus 5.5 · A4 họ khác (Gemini 3.8 Flash).
AGENT = (
    DinhNghiaAgent("A1_RI", "A1 · Collect_raw_data (4 nguồn raw)", OPUS_5_5),
    DinhNghiaAgent("A2_PR_MAP", "A2 · Generate Group Ledger + Mapping", OPUS_5_5),
    DinhNghiaAgent("A3_SI_ITL", "A3 · SI.ITL — Adjust + Allocate", OPUS_5_5),
    DinhNghiaAgent("A4_AUDITOR", "A4 · Auditor", GEMINI_FLASH),
)


class LoiChuoi(RuntimeError):
    pass


def kiem_hai_ho(agent: tuple[DinhNghiaAgent, ...] = AGENT) -> None:
    """Luật hai họ (Voi phase 1): họ A4 ≠ họ mọi agent làm. Vi phạm ⇒ ⛔ chạy."""
    ho_lam = {a.mo_hinh.ho for a in agent if a.ma != "A4_AUDITOR"}
    a4 = [a for a in agent if a.ma == "A4_AUDITOR"]
    if not a4 or a4[0].mo_hinh.ho in ho_lam:
        raise LoiChuoi(f"luật hai họ: A4 họ `{a4[0].mo_hinh.ho if a4 else '—'}` trùng họ agent làm {sorted(ho_lam)}")


@dataclass
class KqSkill:
    skill: Skill
    ra: dict[str, Any] | None = None           # đầu ra AGENT (mã ô → giá trị)
    may_cong_cu: dict[str, Any] | None = None  # kết quả công cụ phía máy (chưa che) — cho cổng luật cứng
    dat_cong: bool | None = None
    ly_do: str = ""
    loi: str = ""
    so_luot: int = 0
    so_bo_che: int = 0
    the_noi_dung: int = 0


@dataclass
class KqAgent:
    dn: DinhNghiaAgent
    checksum: str
    skills: list[KqSkill] = field(default_factory=list)
    o: list[dc.O] = field(default_factory=list)      # phán của A4 (cửa ②) trên các skill `lam`
    o_bong: list[dc.O] = field(default_factory=list)  # skill `bong` ↔ đáp án giữ riêng
    dat_a4: bool | None = None


@dataclass
class KqChuoi:
    agents: list[KqAgent] = field(default_factory=list)
    dung_o: str | None = None

    @property
    def dat(self) -> bool:
        return self.dung_o is None and all(a.dat_a4 for a in self.agents)


def _cong_cu_def(s: Skill) -> dict:
    return {"name": s.cong_cu, "description": f"Công cụ FLS của skill {s.ma} (tất định, chỉ đọc).",
            "input_schema": {"type": "object", "properties": {}, "additionalProperties": False}}


def chay_skill(dn: DinhNghiaAgent, he: str, s: Skill, ncc: NhaCungCap,
               cong_cu: dict[str, Callable[[], dict]], che_do: str | None = None) -> KqSkill:
    kq = KqSkill(skill=s)
    if s.cong_cu not in cong_cu:
        kq.loi = f"công cụ `{s.cong_cu}` ⛔ được tiêm"
        return kq
    messages: list[dict] = [{"role": "user", "content": s.prompt}]
    try:
        for _ in range(SO_LUOT_TOI_DA):
            yc = {"model": dn.mo_hinh.ma, "max_tokens": MAX_TOKENS, "system": he,
                  "tools": [_cong_cu_def(s)], "messages": messages}
            yc_che, bc = che_mod.che_yeu_cau(yc, che_do or che_mod.CHE_DO_MAC_DINH)
            kq.so_bo_che, kq.the_noi_dung = bc.so_bo, bc.the_noi_dung
            tl = ncc.goi(yc_che)
            kq.so_luot += 1
            dung = tl.get("stop_reason")
            if dung == "tool_use":
                ket = []
                for k in tl.get("content", []):
                    if k.get("type") != "tool_use":
                        continue
                    if k.get("name") != s.cong_cu:
                        raise LoiChuoi(f"mô hình gọi công cụ `{k.get('name')}` ⛔ của skill (chỉ `{s.cong_cu}`)")
                    kq.may_cong_cu = cong_cu[s.cong_cu]()
                    ket.append({"type": "tool_result", "tool_use_id": k["id"],
                                "content": json.dumps(kq.may_cong_cu, ensure_ascii=False, sort_keys=True)})
                if not ket:
                    raise LoiChuoi("stop_reason tool_use mà 0 khối tool_use")
                messages = messages + [{"role": "assistant", "content": tl["content"]},
                                       {"role": "user", "content": ket}]
                continue
            if dung == "end_turn":
                van = "".join(k.get("text", "") for k in tl.get("content", []) if k.get("type") == "text")
                ra = json.loads(van)
                if not isinstance(ra, dict):
                    raise LoiChuoi("câu trả lời ⛔ phải một đối tượng JSON")
                kq.ra = ra
                break
            raise LoiChuoi(f"mô hình dừng `{dung}` (refusal · max_tokens · …) ⇒ ⛔ đầu ra")
        else:
            raise LoiChuoi(f"quá {SO_LUOT_TOI_DA} lượt mà chưa có câu trả lời")
    except (LoiChuoi, che_mod.CamGui, json.JSONDecodeError, RuntimeError) as e:
        kq.loi = f"{type(e).__name__}: {e}"
        return kq
    kq.dat_cong, kq.ly_do = chay_cong(s.cong, kq.ra, {"cong_cu": kq.may_cong_cu or {}})
    return kq


def chay_chuoi(ncc_theo_agent: dict[str, NhaCungCap], cong_cu: dict[str, Callable[[], dict]],
               may: dict[str, Any], dap_an: dict[str, Any] | None = None, che_do: str | None = None,
               agent: tuple[DinhNghiaAgent, ...] = AGENT) -> KqChuoi:
    """Chạy chuỗi. `may` = số máy đã đo theo nguồn ô (`voi` · `hd2` · `nguon` · `cong`); `dap_an` = `{"noi": …}`."""
    kiem_hai_ho(agent)
    kc = KqChuoi()
    for dn in agent:
        bo = nap_bo(dn.ma)
        ka = KqAgent(dn=dn, checksum=checksum_prompt(dn.ma))
        kc.agents.append(ka)
        he = he_thong(dn.ma)
        for s in bo:
            if kc.dung_o is not None:
                ka.skills.append(KqSkill(skill=s))
                continue
            if s.loai == "ma":
                ka.skills.append(KqSkill(skill=s, dat_cong=True, ly_do="skill mã — chạy ở cửa ② / sinh trang"))
                continue
            ncc = ncc_theo_agent.get(dn.ma)
            if ncc is None:
                ks = KqSkill(skill=s, loi=f"⛔ có nhà cung cấp cho {dn.ma}")
            else:
                ks = chay_skill(dn, he, s, ncc, cong_cu, che_do)
            ka.skills.append(ks)
            if ks.loi or not ks.dat_cong:
                kc.dung_o = f"DỪNG ở {s.nhan} — " + (ks.loi or f"cổng `{s.cong}` ĐỎ: {ks.ly_do}")
        # cửa ② — A4 (mã) soát agent này
        for ks in ka.skills:
            s = ks.skill
            if s.loai == "lam":
                ka.o += dc.doi_chieu_skill(s.nhan, s.mau_o, ks.ra, may)
            elif s.loai == "bong":
                ka.o_bong += dc.doi_chieu_skill(s.nhan, s.mau_o, ks.ra, dap_an or {})
        do_ = [o for o in ka.o if o.do]
        ka.dat_a4 = not do_ and kc.dung_o is None
        if kc.dung_o is None and do_:
            dem = dc.tom_tat(ka.o)
            kc.dung_o = (f"A4 TRƯỢT {dn.ma}: " + " · ".join(f"{k} {v}" for k, v in dem.items()
                                                             if k in dc.TRANG_THAI_DO and v)
                         + f" — ô đầu: {do_[0].ma} ({do_[0].trang_thai})")
    return kc
