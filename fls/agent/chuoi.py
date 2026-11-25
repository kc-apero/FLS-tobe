# -*- coding: utf-8 -*-
"""Chuỗi 4 agent: A1 → A2 → A3 → A4 — TUẦN TỰ, có cửa (`WO-329` AC-2).

⭐ Hai tầng cửa:
   ① trong một agent: skill `n+1` chỉ chạy khi cổng ra của skill `n` ĐẠT (`cong_skill.py`);
   ② giữa hai agent: agent `k+1` chỉ chạy khi A4 (phép so `doi_chieu.py`, MÃ) cho agent `k` ĐẠT —
      mọi ô của các skill `lam` khớp máy (lệch 0 · ⛔ đo được 0 · thiếu 0 · thừa 0).
   Dừng ở đâu ⇒ `KqChuoi.dung_o` mang TÊN chỗ dừng (agent/skill + cổng + lý do) — ⛔ "lỗi chung".
⭐ Skill `bong` (G0 bóng) chịu cổng ① (luật cứng) nhưng ⛔ vào cửa ② — nó so với ĐÁP ÁN giữ riêng, ở khối riêng.
⭐ Skill `ma` ⛔ gọi mô hình: `01_soat_lop` = chính cửa ②; `04_report` = sinh trang (tools/chay_agent_voi.py).
   Skill `ma` CÓ công cụ được tiêm (A4.02 `cong_hd1` · A4.03 `cong_hd2`) ⇒ MÃ chạy công cụ, đầu ra = kết quả
   công cụ, vẫn qua cổng ① và cửa ② — ⛔ nhà cung cấp nào được dựng cho nó.
   ⚠ Bia `AG-R1-06` (KQ-331): bản đầu để A4.02/03 `loai: lam` ⇒ gọi `gemini-3.8-flash` CHƯA ghim, ngược quyết chủ
   C2 *"A4 MÃ THUẦN tới G1"* — và `--that` phải dựng nhà cung cấp Google ⇒ chạy thật A1–A3 cũng ⛔ được.
⭐ `WO-355` (chủ 23/11 ~12:45): MỘT nhà cung cấp Anthropic — A1–A3 (agent LÀM) = `claude-opus-5-5`; A4 (phần KIỂM
   dùng mô hình, mở ở G1) = `claude-sonnet-5-5`; phán cuối của A4 vẫn là MÃ `doi_chieu`. "Luật hai HỌ" (Voi phase 1)
   ⛔ còn thoả được với một hãng ⇒ thay bằng luật HAI MÔ HÌNH (`kiem_a4_khac_mo_hinh`): mô hình A4 ≠ mô hình agent làm.
   Mô hình theo TỪNG skill: `mo_hinh_skill` — `lam`/`bong` ⇒ mô hình agent; `ma` ⇒ `None` (⛔ lượt API).

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
from fls.agent.mo_hinh import OPUS_5_5, SONNET_5_5, MoHinh, NhaCungCap
from fls.agent.skill import Skill, checksum_prompt, he_thong, nap_bo

SO_LUOT_TOI_DA = 4
MAX_TOKENS = 16000


@dataclass(frozen=True)
class DinhNghiaAgent:
    ma: str
    ten: str
    mo_hinh: MoHinh


#: Thứ tự chuỗi. ⭐ `WO-355` (THAY phương án A): A1–A3 `claude-opus-5-5` · A4 `claude-sonnet-5-5` (cùng hãng, KHÁC mô hình).
#: ⭐ Quyết chủ C2 (23/11): A4 là MÃ THUẦN tới G1 — `mo_hinh` của A4 chỉ là mô hình DỰ KIẾN cho phần KIỂM ở G1 (giữ để
#:    canh luật hai mô hình); hôm nay A4 ⛔ có skill `lam`/`bong` nên ⛔ được dựng nhà cung cấp (`can_mo_hinh`).
AGENT = (
    DinhNghiaAgent("A1_RI", "A1 · Collect_raw_data (4 nguồn raw)", OPUS_5_5),
    DinhNghiaAgent("A2_PR_MAP", "A2 · Generate Group Ledger + Mapping", OPUS_5_5),
    DinhNghiaAgent("A3_SI_ITL", "A3 · SI.ITL — Adjust + Allocate", OPUS_5_5),
    DinhNghiaAgent("A4_AUDITOR", "A4 · Auditor", SONNET_5_5),
)


class LoiChuoi(RuntimeError):
    pass


LOAI_GOI_MO_HINH = ("lam", "bong")


def can_mo_hinh(ma_agent: str) -> bool:
    """Agent có ít nhất một skill gọi mô hình (`lam`/`bong`)? ⛔ ⇒ ⛔ dựng nhà cung cấp cho nó (C2)."""
    return any(s.loai in LOAI_GOI_MO_HINH for s in nap_bo(ma_agent))


def kiem_a4_khac_mo_hinh(agent: tuple[DinhNghiaAgent, ...] = AGENT) -> None:
    """Luật HAI MÔ HÌNH (`WO-355`, thay luật hai họ): mã mô hình A4 ≠ mã mô hình MỌI agent làm. Vi phạm ⇒ ⛔ chạy.

    ⚠ Một hãng ⇒ A4 ⛔ còn độc lập về HỌ với A1–A3; độc lập còn lại = mô hình khác + phán cuối là MÃ."""
    ma_lam = {a.mo_hinh.ma for a in agent if a.ma != "A4_AUDITOR"}
    a4 = [a for a in agent if a.ma == "A4_AUDITOR"]
    if not a4 or a4[0].mo_hinh.ma in ma_lam:
        raise LoiChuoi(f"luật hai mô hình: A4 `{a4[0].mo_hinh.ma if a4 else '—'}` trùng mô hình agent làm {sorted(ma_lam)}")


def mo_hinh_skill(dn: DinhNghiaAgent, s: Skill) -> MoHinh | None:
    """Mô hình MỘT skill thật sự gọi: `lam`/`bong` ⇒ mô hình agent; `ma` ⇒ `None` (MÃ, ⛔ lượt API)."""
    return dn.mo_hinh if s.loai in LOAI_GOI_MO_HINH else None


def doc_json_tra_loi(van: str) -> Any:
    """Câu trả lời cuối của mô hình ⇒ JSON. Chịu MỘT rào ```json … ``` bao ngoài (mô hình thật hay bọc);
    ⛔ cắt chữ thừa khác — chữ ngoài JSON ⇒ `JSONDecodeError` ⇒ skill ĐỎ có tên (⛔ đoán)."""
    t = van.strip()
    if t.startswith("```") and t.endswith("```") and t.count("```") == 2:
        t = t[3:-3]
        dau, _, than = t.partition("\n")
        t = than if dau.strip().lower() in ("", "json") else t
    return json.loads(t)


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
                ra = doc_json_tra_loi(van)
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


def chay_skill_ma(s: Skill, cong_cu: dict[str, Callable[[], dict]]) -> KqSkill:
    """Skill `ma` có công cụ: MÃ gọi công cụ, đầu ra = kết quả công cụ (⛔ mô hình, ⛔ lượt API)."""
    kq = KqSkill(skill=s)
    try:
        kq.may_cong_cu = cong_cu[s.cong_cu]()
    except Exception as e:  # noqa: BLE001 — mọi lỗi công cụ ⇒ chuỗi DỪNG có tên
        kq.loi = f"{type(e).__name__}: {e}"
        return kq
    kq.ra = dict(kq.may_cong_cu)
    kq.dat_cong, kq.ly_do = chay_cong(s.cong, kq.ra, {"cong_cu": kq.may_cong_cu})
    return kq


def chay_chuoi(ncc_theo_agent: dict[str, NhaCungCap], cong_cu: dict[str, Callable[[], dict]],
               may: dict[str, Any], dap_an: dict[str, Any] | None = None, che_do: str | None = None,
               agent: tuple[DinhNghiaAgent, ...] = AGENT) -> KqChuoi:
    """Chạy chuỗi. `may` = số máy đã đo theo nguồn ô (`voi` · `hd2` · `nguon` · `cong`); `dap_an` = `{"noi": …}`."""
    kiem_a4_khac_mo_hinh(agent)
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
                if s.cong_cu in cong_cu and s.mau_o:
                    ks = chay_skill_ma(s, cong_cu)
                    ka.skills.append(ks)
                    if ks.loi or not ks.dat_cong:
                        kc.dung_o = f"DỪNG ở {s.nhan} — " + (ks.loi or f"cổng `{s.cong}` ĐỎ: {ks.ly_do}")
                else:
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
            if s.loai == "lam" or (s.loai == "ma" and s.mau_o):
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
