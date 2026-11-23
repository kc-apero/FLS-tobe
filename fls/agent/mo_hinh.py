# -*- coding: utf-8 -*-
"""Lớp gọi mô hình — giao diện nhà cung cấp chung, ⛔ cứng một hãng (`WO-329` AC-3).

⭐ Khuôn yêu cầu/đáp CHUNG = khuôn Messages API của Anthropic (dict thuần):
     yêu cầu  {"model", "max_tokens", "system", "tools": [{name, description, input_schema}], "messages"}
     đáp      {"stop_reason": "tool_use" | "end_turn" | "refusal" | "max_tokens", "content": [khối…]}
   khối `tool_use` {id, name, input} · `text` {text}; lượt sau gửi `tool_result` {tool_use_id, content}.
   Nhà cung cấp họ khác (Google cho A4 ở phương án A) phải DỊCH sang khuôn này ở adapter của nó.

⭐ Ba chế độ — MẶC ĐỊNH là PHÁT LẠI:
   PhatLai  đáp ghi sẵn trong `docs/ITL/06_Agent/phat_lai/<agent>.json`, tra theo VÂN TAY yêu cầu ĐÃ CHE.
            Yêu cầu đổi (prompt · dữ liệu · công cụ) ⇒ ⛔ có lượt ⇒ `KhongCoBanGhi` (ĐỎ, ⛔ đoán).
   GiaLap   mô hình GIẢ tất định: lượt 1 gọi công cụ duy nhất của skill; lượt 2 chép NGUYÊN kết quả
            công cụ làm câu trả lời. Dùng để SINH bản ghi phát lại (`--ghi-phat-lai`) và trong bài thử.
   That     gọi API THẬT — chỉ khi đủ BA chốt: cờ `co_that=True` (CLI `--that`) · `FLS_CHO_GOI_API=1` ·
            khoá trong biến môi trường. Thêm chốt thứ tư: mô hình phải GHIM (`ghim=True`) — ⛔ bí danh.
            ⛔ WO-329 ⛔ gọi thật: bài `test_mo_hinh.py` chứng minh mỗi chốt thiếu ⇒ `CamGoiThat`.

⚠ Claude Opus 5.5 (`claude-opus-5-5`, tra skill `claude-api` 23/11): thinking ⛔ tắt được (bỏ tham số) ·
   `tool_choice` ép `any`/`tool` ⇒ 400 (dùng `auto` + lời dặn trong prompt) · effort mặc định `medium` ⇒
   đặt RÕ. Đáp `refusal` ⇒ chuỗi DỪNG có tên — ⛔ bật `fallbacks` sang mô hình khác: phiên bản agent =
   mã mô hình GHIM; rơi sang mô hình khác là đổi phiên bản trong im lặng (câu chủ C1 ở BG-330).
"""
from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

BIEN_CHO_GOI = "FLS_CHO_GOI_API"
#: ⭐ Quyết chủ 23/11: chế độ che `mo` (mặc định) gửi NGUYÊN VĂN nội dung · số TK · tên ra API — đi KÈM điều kiện
#:    ZDR (zero data retention: nhà cung cấp ⛔ lưu dữ liệu). Bia `AG-R1-11` (KQ-331): điều kiện ấy chỉ nằm ở thẻ/BG,
#:    **0** chỗ trong mã ⇒ nay là CHỐT THỨ NĂM của chế độ THẬT: `mo` ⇒ đòi `FLS_ZDR_DA_BAT=1` (người vận hành
#:    xác nhận tài khoản API đã bật ZDR). Chế độ `che_noi_dung` · `che_het` ⛔ đòi (dữ liệu đã che).
BIEN_ZDR = "FLS_ZDR_DA_BAT"
CHE_DO_CAN_ZDR = ("mo",)
#: Bí danh "mới nhất" ⛔ được ghim (Voi phase 1: *"mã mô hình đã ghim, ⛔ bí danh 'mới nhất'"*).
DAU_BI_DANH = ("latest", "moi-nhat", "newest")


@dataclass(frozen=True)
class MoHinh:
    ho: str        # họ nhà cung cấp: "anthropic" · "google" · …  (luật hai họ: A4 ≠ A1–A3)
    ma: str        # mã mô hình CHÍNH XÁC
    ghim: bool     # True = mã đã xác nhận; False = tên tạm, CHƯA ghim (gọi thật bị chặn)
    bien_khoa: str  # tên biến môi trường chứa khoá — ⛔ bao giờ đọc giá trị ra log

    def loi_ghim(self) -> str | None:
        if not self.ghim:
            return f"mô hình `{self.ma}` CHƯA ghim (tên tạm) — câu chủ: mã chính xác lúc mở tài khoản"
        if any(d in self.ma.lower() for d in DAU_BI_DANH):
            return f"mô hình `{self.ma}` là bí danh — ⛔ ghim được"
        return None


#: Phương án A (Voi phase 1 §F0b — PROPOSED, chờ chủ chốt sau vòng chọn mô hình N8).
OPUS_5_5 = MoHinh(ho="anthropic", ma="claude-opus-5-5", ghim=True, bien_khoa="ANTHROPIC_API_KEY")
GEMINI_FLASH = MoHinh(ho="google", ma="gemini-3.8-flash", ghim=False, bien_khoa="GEMINI_API_KEY")


class CamGoiThat(RuntimeError):
    """Thiếu một chốt của chế độ THẬT."""


class KhongCoBanGhi(RuntimeError):
    """Phát lại: ⛔ có lượt ghi sẵn cho đúng yêu cầu này (bản ghi cũ hoặc yêu cầu đã đổi)."""


class ChuaDung(NotImplementedError):
    """Adapter nhà cung cấp chưa dựng."""


class NhaCungCap(Protocol):
    ten: str

    def goi(self, yeu_cau: dict) -> dict: ...


def van_tay(yeu_cau: dict) -> str:
    """Vân tay yêu cầu ĐÃ CHE — JSON chuẩn (khoá xếp) ⇒ sha256 16 hex."""
    return hashlib.sha256(json.dumps(yeu_cau, ensure_ascii=False, sort_keys=True)
                          .encode("utf-8")).hexdigest()[:16]


# ── PHÁT LẠI (mặc định) ────────────────────────────────────────────────────────────────────────
class PhatLai:
    ten = "phat-lai"

    def __init__(self, tep: Path):
        self.tep = Path(tep)
        try:
            d = json.loads(self.tep.read_text(encoding="utf-8"))
        except FileNotFoundError:
            raise KhongCoBanGhi(f"bản ghi phát lại vắng: `{self.tep.name}`") from None
        self.dau = d
        self.luot = {x["van_tay_yeu_cau"]: x["tra_loi"] for x in d.get("luot", [])}

    def goi(self, yeu_cau: dict) -> dict:
        vt = van_tay(yeu_cau)
        if vt not in self.luot:
            raise KhongCoBanGhi(f"`{self.tep.name}` ⛔ có lượt cho yêu cầu {vt} — prompt, công cụ hoặc dữ "
                                "liệu đã đổi so với lúc ghi ⇒ ghi lại bằng `--ghi-phat-lai` (⛔ đoán)")
        return json.loads(json.dumps(self.luot[vt]))


# ── GIẢ tất định ──────────────────────────────────────────────────────────────────────────────
class GiaLap:
    """Lượt 1: gọi công cụ đầu tiên với input `{}`. Lượt có `tool_result`: chép nguyên làm câu trả lời —
    trừ công cụ có `luat` riêng (vd. `ung_vien_ghep` ⇒ `ghep_noi_dung.luat_gia_v1`): khi ấy câu trả lời =
    `luat(kết quả công cụ ĐÃ CHE)`, đúng những gì mô hình thật sẽ thấy."""
    ten = "gia-lap"

    def __init__(self, luat: dict[str, Any] | None = None):
        self.luat = luat or {}

    def goi(self, yeu_cau: dict) -> dict:
        cuoi = yeu_cau["messages"][-1]
        noi = cuoi.get("content")
        if isinstance(noi, list):
            for k in noi:
                if isinstance(k, dict) and k.get("type") == "tool_result":
                    ten_cc = (yeu_cau.get("tools") or [{}])[0].get("name")
                    van = k["content"]
                    if ten_cc in self.luat:
                        van = json.dumps(self.luat[ten_cc](json.loads(van)), ensure_ascii=False, sort_keys=True)
                    return {"stop_reason": "end_turn", "content": [{"type": "text", "text": van}]}
        cc = yeu_cau.get("tools") or []
        if not cc:
            return {"stop_reason": "end_turn", "content": [{"type": "text", "text": "{}"}]}
        so = sum(1 for m in yeu_cau["messages"] if m["role"] == "assistant")
        return {"stop_reason": "tool_use",
                "content": [{"type": "tool_use", "id": f"toolu_gia_{so:02d}", "name": cc[0]["name"], "input": {}}]}


class GhiLai:
    """Bọc một nhà cung cấp, ghi (vân tay → đáp) để tạo bản ghi phát lại."""

    def __init__(self, goc: NhaCungCap):
        self.goc = goc
        self.ten = f"ghi:{goc.ten}"
        self.luot: list[dict] = []

    def goi(self, yeu_cau: dict) -> dict:
        tl = self.goc.goi(yeu_cau)
        self.luot.append({"van_tay_yeu_cau": van_tay(yeu_cau), "tra_loi": tl})
        return tl


# ── THẬT — chốt ba lớp + ghim ─────────────────────────────────────────────────────────────────
def kiem_chot_that(mo_hinh: MoHinh, co_that: bool, moi_truong: dict[str, str] | None = None,
                   che_do: str = "mo") -> None:
    """⛔ trả về = được gọi thật. Thiếu bất kỳ chốt nào ⇒ `CamGoiThat` kèm TÊN chốt (⛔ giá trị khoá).

    `che_do` mặc định `mo` (= mặc định của bộ che) ⇒ ⛔ quên truyền thì bị đòi ZDR, ⛔ lọt.
    """
    mt = os.environ if moi_truong is None else moi_truong
    thieu = []
    if not co_that:
        thieu.append("cờ `--that` vắng")
    if mt.get(BIEN_CHO_GOI) != "1":
        thieu.append(f"`{BIEN_CHO_GOI}` ≠ 1")
    if not mt.get(mo_hinh.bien_khoa):
        thieu.append(f"khoá `{mo_hinh.bien_khoa}` vắng trong biến môi trường")
    lg = mo_hinh.loi_ghim()
    if lg:
        thieu.append(lg)
    if che_do in CHE_DO_CAN_ZDR and mt.get(BIEN_ZDR) != "1":
        thieu.append(f"chế độ che `{che_do}` gửi nguyên văn tên · số TK ⇒ đòi `{BIEN_ZDR}=1` (ZDR — quyết chủ 23/11)")
    if thieu:
        raise CamGoiThat("⛔ gọi API thật: " + " · ".join(thieu))


class AnthropicMessages:
    """Adapter Anthropic Messages API (SDK `anthropic`, nhập MUỘN — ⛔ có trong `requirements.txt`)."""
    ten = "anthropic"

    def __init__(self, mo_hinh: MoHinh, co_that: bool = False, effort: str = "medium", che_do: str = "mo"):
        kiem_chot_that(mo_hinh, co_that, che_do=che_do)
        import anthropic  # noqa: PLC0415 — chỉ tới đây khi đủ chốt
        self.mo_hinh, self.effort = mo_hinh, effort
        self.client = anthropic.Anthropic()          # khoá đọc từ biến môi trường, ⛔ truyền tay

    def goi(self, yeu_cau: dict) -> dict:
        if yeu_cau.get("model") != self.mo_hinh.ma:
            raise CamGoiThat(f"yêu cầu mang mô hình `{yeu_cau.get('model')}` ≠ ghim `{self.mo_hinh.ma}`")
        tl = self.client.messages.create(
            model=self.mo_hinh.ma, max_tokens=yeu_cau.get("max_tokens", 16000),
            system=yeu_cau.get("system", ""), tools=yeu_cau.get("tools", []),
            messages=yeu_cau["messages"], output_config={"effort": self.effort})
        return tl.to_dict()


class GoogleChuaDung:
    """Chỗ cắm adapter họ Google (A4 · phương án A). Chốt chạy TRƯỚC — rồi mới báo chưa dựng."""
    ten = "google"

    def __init__(self, mo_hinh: MoHinh, co_that: bool = False, che_do: str = "mo"):
        kiem_chot_that(mo_hinh, co_that, che_do=che_do)
        raise ChuaDung("adapter Gemini chưa dựng — chờ chủ chốt phương án A/B (câu chủ C1, C2 ở BG-330)")

    def goi(self, yeu_cau: dict) -> dict:  # pragma: no cover
        raise ChuaDung


def tao_that(mo_hinh: MoHinh, co_that: bool, che_do: str = "mo") -> Any:
    """Nhà cung cấp THẬT theo HỌ của mô hình — ⛔ cứng một hãng."""
    if mo_hinh.ho == "anthropic":
        return AnthropicMessages(mo_hinh, co_that, che_do=che_do)
    if mo_hinh.ho == "google":
        return GoogleChuaDung(mo_hinh, co_that, che_do=che_do)
    raise ChuaDung(f"họ `{mo_hinh.ho}` chưa có adapter")
