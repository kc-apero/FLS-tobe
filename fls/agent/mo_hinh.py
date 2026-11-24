# -*- coding: utf-8 -*-
"""Lớp gọi mô hình — giao diện nhà cung cấp chung, ⛔ cứng một hãng (`WO-329` AC-3).

⭐ Khuôn yêu cầu/đáp CHUNG = khuôn Messages API của Anthropic (dict thuần):
     yêu cầu  {"model", "max_tokens", "system", "tools": [{name, description, input_schema}], "messages"}
     đáp      {"stop_reason": "tool_use" | "end_turn" | "refusal" | "max_tokens", "content": [khối…]}
   khối `tool_use` {id, name, input} · `text` {text}; lượt sau gửi `tool_result` {tool_use_id, content}.
   ⭐ Quyết chủ 23/11 ~12:45 (`WO-355`): giai đoạn này MỘT nhà cung cấp — **Anthropic** (`claude-opus-5-5` cho agent
   LÀM A1–A3 · `claude-sonnet-5-5` cho phần KIỂM/A4 dùng mô hình); **BỎ Gemini**. Giai đoạn sau: OpenAI — họ
   `openai` đã CHỪA chỗ ở `HO_DE_DANH` (chốt chạy trước, rồi `ChuaDung`), ⛔ adapter. Adapter mới phải DỊCH
   sang khuôn này và ghi `NhatKyGoi` như `AnthropicMessages`.

⭐ Ba chế độ — MẶC ĐỊNH là PHÁT LẠI:
   PhatLai  đáp ghi sẵn trong `docs/ITL/06_Agent/phat_lai/<agent>.json`, tra theo VÂN TAY yêu cầu ĐÃ CHE.
            Yêu cầu đổi (prompt · dữ liệu · công cụ) ⇒ ⛔ có lượt ⇒ `KhongCoBanGhi` (ĐỎ, ⛔ đoán).
   GiaLap   mô hình GIẢ tất định: lượt 1 gọi công cụ duy nhất của skill; lượt 2 chép NGUYÊN kết quả
            công cụ làm câu trả lời. Dùng để SINH bản ghi phát lại (`--ghi-phat-lai`) và trong bài thử.
   That     gọi API THẬT — chỉ khi đủ BA chốt: cờ `co_that=True` (CLI `--that`) · `FLS_CHO_GOI_API=1` ·
            khoá trong biến môi trường. Thêm chốt thứ tư: mô hình phải GHIM (`ghim=True`) — ⛔ bí danh.
            Bài `test_mo_hinh.py` chứng minh mỗi chốt thiếu ⇒ `CamGoiThat` (bằng SDK GIẢ, ⛔ mạng).
            ⭐ `WO-355` AC-2: MỖI lời gọi thật ghi một `NhatKyGoi` (mô hình · token vào/ra/cache · giây · USD ước theo
            `BANG_GIA` có NGÀY TRA · vân tay yêu cầu/đáp) — ⛔ nội dung, ⛔ phản hồi thô. Lỗi API ⇒ `LoiApi` CÓ TÊN
            (lớp lỗi SDK · mã HTTP · request-id) — ⛔ bao giờ rơi về GIẢ/phát lại trong im lặng.

⚠ Claude Opus 5.5 (`claude-opus-5-5`, tra skill `claude-api` 23/11): thinking ⛔ tắt được (bỏ tham số) ·
   `tool_choice` ép `any`/`tool` ⇒ 400 (dùng `auto` + lời dặn trong prompt) · effort mặc định `medium` ⇒
   đặt RÕ. Đáp `refusal` ⇒ chuỗi DỪNG có tên — ⛔ bật `fallbacks` sang mô hình khác: phiên bản agent =
   mã mô hình GHIM; rơi sang mô hình khác là đổi phiên bản trong im lặng (câu chủ C1 ở BG-330).

⭐ `WO-359` (lời chủ 24/11): BA ĐƯỜNG tới CÙNG mô hình, chọn bằng cấu hình `FLS_NHA_CUNG_CAP` (⛔ đổi mã gọi, ⛔ đổi
   prompt — khuôn yêu cầu/đáp y hệt). Biên bản quyết: ~03:15 *"dùng claude trực tiếp trong GCP, thông qua vertex AI"* ⇒
   ~03:45 *"đồng ý dùng qua vertex"* ⇒ **~03:50 *"dùng claude.googleapis.com cho nhanh"*** (quyết HIỆN HÀNH):
     `google-cloud` ⭐ đường CHÍNH (MẶC ĐỊNH khi biến vắng) — *Claude Models on Google Cloud (Anthropic managed)*, service
                 `claude.googleapis.com` (đã BẬT trên `fp-a-project`): `anthropic.AnthropicGoogleCloud(project=…,
                 workspace_id=…)` (gói `anthropic[google_cloud]`), project `FLS_GCP_PROJECT` ∈ `DU_AN_CONG_TY` · workspace
                 `FLS_CLAUDE_WORKSPACE_ID` (`wrkspc_…`) · vị trí `global` (skill: *"Leave it there"*) · xác thực ADC/SA của
                 GCP, vai `roles/claude.user` (⛔ khoá: *"There are no API keys here"*) · mã mô hình = mã Claude API
                 (`claude-opus-5-5` / `claude-sonnet-5-5`, ⛔ tiền tố, ⛔ `@`). ⚠ Skill ⛔ có bảng giá cho nền này
                 (*"whether the first-party prices … apply is unknown"*) ⇒ USD = ƯỚC theo giá Claude API để GIỮ trần.
     `vertex`    DỰ PHÒNG — Claude trên Vertex AI (Google managed) của project công ty (`FLS_GCP_PROJECT`) · vùng
                 `FLS_VERTEX_REGION` ∈ `VUNG_VERTEX` (mặc định `global`) · ADC/SA, `roles/aiplatform.user` (`BANG_GIA_VERTEX`).
     `anthropic` DỰ PHÒNG thứ hai (WO-355): Claude API trực tiếp bằng `ANTHROPIC_API_KEY` — chỉ khi đặt RÕ biến.
   Tra 24/11 (skill `claude-api` + trang `claude-models-on-google-cloud/google-managed`): lớp `anthropic.AnthropicVertex(
   project_id=…, region=…)` (gói `anthropic[vertex]`) · mã mô hình Vertex của Opus 5.5 / Sonnet 5.5 = mã TRẦN
   `claude-opus-5-5` / `claude-sonnet-5-5` (⛔ tiền tố, ⛔ `@ngày`) · vùng: `global` (khuyên) · `us`/`eu` (đa vùng, +10%)
   · vùng ĐƠN (vd `asia-southeast1`) **chỉ phục vụ Sonnet 4.6 trở về trước** ⇒ ⛔ nhận · `fallbacks` phía máy chủ ⛔ có
   trên Vertex (ta vốn ⛔ dùng).
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

# ── Chọn ĐƯỜNG (`WO-359` AC-1) ─────────────────────────────────────────────────────────────────
BIEN_NHA_CUNG_CAP = "FLS_NHA_CUNG_CAP"
DUONG_API = "anthropic"          # dự phòng: Claude API trực tiếp, khoá `ANTHROPIC_API_KEY`
DUONG_VERTEX = "vertex"          # dự phòng: Claude trên Vertex AI của project công ty
DUONG_GOOGLE_CLOUD = "google-cloud"   # ⭐ CHÍNH (chủ 24/11 ~03:50): `claude.googleapis.com` (Anthropic managed)
DUONG_HOP_LE = (DUONG_GOOGLE_CLOUD, DUONG_VERTEX, DUONG_API)
DUONG_MAC_DINH = DUONG_GOOGLE_CLOUD
#: Đường của project GCP (đòi `FLS_GCP_PROJECT` ∈ `DU_AN_CONG_TY`, ⛔ khoá).
DUONG_GCP = (DUONG_GOOGLE_CLOUD, DUONG_VERTEX)
BIEN_CLAUDE_WORKSPACE = "FLS_CLAUDE_WORKSPACE_ID"
DAU_WORKSPACE = "wrkspc_"
#: ⭐ AC-2 ở đường `google-cloud` — THAY `FLS_ZDR_DA_BAT`. Tra 24/11 (skill `claude-api` · `google-cloud-anthropic-managed`):
#:    nền do ANTHROPIC vận hành; việc dựng tạo **một tổ chức Anthropic MỚI** — *"A Zero Data Retention arrangement doesn't
#:    carry over"* ⇒ xác nhận ZDR cũ của tài khoản API ⛔ dùng lại được. Người vận hành xác nhận (BG-360 §E C1).
BIEN_GC_DU_LIEU = "FLS_GC_DU_LIEU_XAC_NHAN"
BIEN_GCP_PROJECT = "FLS_GCP_PROJECT"
BIEN_VERTEX_REGION = "FLS_VERTEX_REGION"
#: ⭐ AC-5 (quyết chủ 23/11 + 24/11): agent đọc TOÀN BỘ nội dung + số TK **chỉ trong GCP của công ty** ⇒ đường Vertex chỉ
#:    nhận project trong danh sách này. Thêm project = sửa MÃ (có review), ⛔ một biến môi trường.
DU_AN_CONG_TY = ("fp-a-project",)
VUNG_VERTEX_MAC_DINH = "global"
#: Vùng phục vụ được Opus 5.5 / Sonnet 5.5 (tra 24/11: *"Regional endpoints serve Claude Sonnet 4.6 and earlier models
#:   only. For newer models, use a global or multi-region endpoint."*). Hệ số giá: đa vùng +10% so với global.
VUNG_VERTEX: dict[str, float] = {"global": 1.00, "us": 1.10, "eu": 1.10}
#: ⭐ AC-2 — THAY `FLS_ZDR_DA_BAT` ở đường Vertex. Tra 24/11: trang Anthropic *"Google Cloud governs data handling for Claude
#:    Models on Google Cloud (Google managed)"*; trang Google `data-governance`: ⛔ huấn luyện trên dữ liệu khách khi chưa
#:    cho phép (mọi mô hình managed) · *request-response logging "is disabled by default"* — để ZDR *"do not enable this
#:    feature"* · ZDR cho mô hình ĐỐI TÁC phải XIN qua account team (trang chỉ tả quy trình cho OpenAI, ⛔ một câu riêng về
#:    Claude). ⇒ Người vận hành xác nhận BA điều (BG-360 §câu chủ): ① project = `fp-a-project` của công ty · ② request-
#:    response logging cho mô hình Claude ĐANG TẮT · ③ đã đọc trạng thái ZDR (đã xin / chấp nhận giữ theo điều khoản GCP).
BIEN_VERTEX_DU_LIEU = "FLS_VERTEX_DU_LIEU_XAC_NHAN"


def duong_goi(moi_truong: dict[str, str] | None = None) -> str:
    """Đường gọi thật theo cấu hình. Biến vắng ⇒ `google-cloud` (quyết chủ 24/11 ~03:50). Giá trị lạ trả NGUYÊN để
    `kiem_chot_that` báo ĐỎ có tên (⛔ đoán sang một đường)."""
    mt = os.environ if moi_truong is None else moi_truong
    return (mt.get(BIEN_NHA_CUNG_CAP) or DUONG_MAC_DINH).strip().lower()
#: Bí danh "mới nhất" ⛔ được ghim (Voi phase 1: *"mã mô hình đã ghim, ⛔ bí danh 'mới nhất'"*).
DAU_BI_DANH = ("latest", "moi-nhat", "newest")


@dataclass(frozen=True)
class MoHinh:
    ho: str        # họ nhà cung cấp: hôm nay CHỈ "anthropic" (`WO-355`); "openai" chừa chỗ (`HO_DE_DANH`)
    ma: str        # mã mô hình CHÍNH XÁC
    ghim: bool     # True = mã đã xác nhận; False = tên tạm, CHƯA ghim (gọi thật bị chặn)
    bien_khoa: str  # tên biến môi trường chứa khoá — ⛔ bao giờ đọc giá trị ra log

    def loi_ghim(self) -> str | None:
        if not self.ghim:
            return f"mô hình `{self.ma}` CHƯA ghim (tên tạm) — câu chủ: mã chính xác lúc mở tài khoản"
        if any(d in self.ma.lower() for d in DAU_BI_DANH):
            return f"mô hình `{self.ma}` là bí danh — ⛔ ghim được"
        return None


#: ⭐ Quyết chủ 23/11 ~12:45 (`WO-355`, THAY phương án A của BG-330): MỘT nhà cung cấp Anthropic, mã GHIM đúng bảng
#:    skill `claude-api` (tra 23/11, bảng cache 2026-11-03) — ⛔ hậu tố ngày, ⛔ bí danh.
#:    ⚠ Bia: `GEMINI_FLASH` (`gemini-3.8-flash`, họ `google`, CHƯA ghim) + `GoogleChuaDung` đã XOÁ — chủ: *"không dùng
#:    gemini nữa"*. Bài `test_mo_hinh.py::test_WO355_khong_con_ho_google__chi_anthropic_ghim` canh nó ⛔ quay lại.
OPUS_5_5 = MoHinh(ho="anthropic", ma="claude-opus-5-5", ghim=True, bien_khoa="ANTHROPIC_API_KEY")      # agent LÀM
SONNET_5_5 = MoHinh(ho="anthropic", ma="claude-sonnet-5-5", ghim=True, bien_khoa="ANTHROPIC_API_KEY")  # phần KIỂM
#: Họ ĐÃ có adapter (⇒ `tao_that` dựng được) · họ CHỪA CHỖ cho giai đoạn sau (⇒ chốt rồi `ChuaDung`, ⛔ adapter).
HO_CO_ADAPTER = ("anthropic",)
HO_DE_DANH = ("openai",)

#: Bảng giá USD / 1 triệu token — tra skill `claude-api` NGÀY 2026-11-23 (bảng "Current Models", cache 2026-11-03).
#: ✔ Đối chiếu lại 24/11 với trang `about-claude/pricing`: Opus 5.5 $4 · ghi cache 5 phút $5 · đọc cache $0,20 · ra $20;
#:    Sonnet 5.5 $2 · $2,50 · $0,10 · $10 — khớp 8/8 ô.
#: Ghi cache 5 phút = 1,25 × giá vào (skill: "~1.25x cost"). Giá đổi ⇒ sửa bảng + NGÀY; chi phí in ra luôn là ƯỚC.
NGAY_TRA_GIA = "2026-11-23"
BANG_GIA: dict[str, dict[str, float]] = {
    "claude-opus-5-5": {"vao": 4.00, "ra": 20.00, "cache_doc": 0.20, "cache_ghi": 5.00},
    "claude-sonnet-5-5": {"vao": 2.00, "ra": 10.00, "cache_doc": 0.10, "cache_ghi": 2.50},
}
#: ⭐ Giá Vertex (`WO-359` AC-2) — tra NGÀY 2026-11-24. Trang Anthropic `pricing` §Cloud platform: GCP tự đặt giá + tự lập hoá
#:    đơn; *"Regional and multi-region endpoints include a 10 percent premium over global endpoints"* (Claude 4.5 trở đi).
#:    ⚠ GIẢ ĐỊNH CHƯA KIỂM: trang giá Google (`cloud.google.com/vertex-ai/generative-ai/pricing#claude-models`) ⛔ đọc được từ
#:    phiên này (trang trả rỗng); các bảng tổng hợp bên thứ ba ghi Opus 5.5 global $4/$20 · đa vùng $4,40/$22 — khớp giả định
#:    "global = giá Claude API". ⇒ Bảng dưới = `BANG_GIA` × hệ số vùng; USD in ra là ƯỚC — Billing GCP là số thật (BG-360).
NGAY_TRA_GIA_VERTEX = "2026-11-24"
BANG_GIA_VERTEX: dict[str, dict[str, float]] = {k: dict(v) for k, v in BANG_GIA.items()}
#: ⭐ Đường `google-cloud`: skill (tra 2026-11-24) *"This skill has no per-token prices for this platform, and whether the
#:    first-party prices in SKILL.md apply is unknown"* ⇒ **CHƯA CÓ BẢNG GIÁ chính thức**. Bảng dưới = giá Claude API, dùng
#:    để GIỮ trần USD (chốt WO-355) — ⛔ là giá đã xác minh; số thật = hoá đơn Marketplace GCP (BG-360 §D).
NGAY_TRA_GIA_GOOGLE_CLOUD = "2026-11-24"
BANG_GIA_GOOGLE_CLOUD: dict[str, dict[str, float]] = {k: dict(v) for k, v in BANG_GIA.items()}
NGAY_TRA_GIA_THEO_DUONG = {DUONG_API: NGAY_TRA_GIA, "vertex": NGAY_TRA_GIA_VERTEX,
                           "google-cloud": NGAY_TRA_GIA_GOOGLE_CLOUD}


class CamGoiThat(RuntimeError):
    """Thiếu một chốt của chế độ THẬT."""


class KhongCoBanGhi(RuntimeError):
    """Phát lại: ⛔ có lượt ghi sẵn cho đúng yêu cầu này (bản ghi cũ hoặc yêu cầu đã đổi)."""


class ChuaDung(NotImplementedError):
    """Adapter nhà cung cấp chưa dựng."""


class LoiApi(RuntimeError):
    """Lời gọi API THẬT thất bại — mang TÊN lỗi (lớp SDK · mã HTTP · request-id), ⛔ nội dung yêu cầu, ⛔ khoá.

    Là `RuntimeError` ⇒ `chuoi.chay_skill` bắt và DỪNG chuỗi có tên (`KqChuoi.dung_o`). ⛔ bao giờ đổi sang GIẢ."""


@dataclass(frozen=True)
class NhatKyGoi:
    """MỘT lời gọi thật — chỉ SỐ ĐẾM + VÂN TAY (luật cứng WO-355: ⛔ nội dung/phản hồi thô trong repo)."""
    mo_hinh: str
    token_vao: int
    token_ra: int
    cache_doc: int
    cache_ghi: int
    giay: float
    chi_phi_usd: float          # ƯỚC theo `BANG_GIA` ngày `NGAY_TRA_GIA`
    stop_reason: str
    van_tay_yeu_cau: str
    van_tay_dap: str
    request_id: str = ""
    duong: str = DUONG_API      # `WO-359`: đường đã gọi — `google-cloud` | `vertex` | `anthropic`
    vung: str = ""              # vùng (`global`/`us`/`eu`); "" ở đường API

    def dict(self) -> dict[str, Any]:
        return {"mo_hinh": self.mo_hinh, "token_vao": self.token_vao, "token_ra": self.token_ra,
                "cache_doc": self.cache_doc, "cache_ghi": self.cache_ghi, "giay": round(self.giay, 3),
                "chi_phi_usd": round(self.chi_phi_usd, 6), "stop_reason": self.stop_reason,
                "van_tay_yeu_cau": self.van_tay_yeu_cau, "van_tay_dap": self.van_tay_dap,
                "request_id": self.request_id, "duong": self.duong, "vung": self.vung,
                "ngay_tra_gia": NGAY_TRA_GIA_THEO_DUONG.get(self.duong, NGAY_TRA_GIA)}


def chi_phi(ma: str, vao: int, ra: int, cache_doc: int = 0, cache_ghi: int = 0, duong: str = DUONG_API,
            vung: str = "") -> float:
    """USD ước. Mô hình ⛔ có trong bảng giá của đường ⇒ `KeyError`; vùng Vertex lạ ⇒ `KeyError` (ĐỎ — ⛔ đoán giá 0)."""
    if duong == DUONG_VERTEX:
        g, he_so = BANG_GIA_VERTEX[ma], VUNG_VERTEX[vung]
    elif duong == DUONG_GOOGLE_CLOUD:
        g, he_so = BANG_GIA_GOOGLE_CLOUD[ma], 1.0
    else:
        g, he_so = BANG_GIA[ma], 1.0
    return he_so * (vao * g["vao"] + ra * g["ra"] + cache_doc * g["cache_doc"] + cache_ghi * g["cache_ghi"]) / 1_000_000


def tong_nhat_ky(ds: list[NhatKyGoi]) -> dict[str, Any]:
    """Cộng nhật ký theo mô hình — số lời gọi · token · giây · USD. Rỗng ⇒ mọi số 0 và `so_goi` 0 (Đ3: nói rõ)."""
    duong = sorted({x.duong for x in ds})
    ra: dict[str, Any] = {"so_goi": len(ds), "token_vao": 0, "token_ra": 0, "cache_doc": 0, "cache_ghi": 0,
                          "giay": 0.0, "chi_phi_usd": 0.0, "theo_mo_hinh": {}, "duong": duong,
                          "vung": sorted({x.vung for x in ds if x.vung}),
                          "ngay_tra_gia": (NGAY_TRA_GIA_THEO_DUONG.get(duong[0], NGAY_TRA_GIA) if len(duong) == 1
                                           else NGAY_TRA_GIA)}
    for x in ds:
        for k in ("token_vao", "token_ra", "cache_doc", "cache_ghi", "giay", "chi_phi_usd"):
            ra[k] += getattr(x, k)
        m = ra["theo_mo_hinh"].setdefault(x.mo_hinh, {"so_goi": 0, "chi_phi_usd": 0.0})
        m["so_goi"] += 1
        m["chi_phi_usd"] += x.chi_phi_usd
    ra["giay"] = round(ra["giay"], 3)
    ra["chi_phi_usd"] = round(ra["chi_phi_usd"], 6)
    return ra


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

    `WO-359`: đường `vertex` THAY hai chốt của đường API — khoá `ANTHROPIC_API_KEY` ⇒ project công ty + vùng hỗ trợ
    (xác thực là ADC của GCP, ⛔ kiểm được ở đây mà ⛔ gọi mạng ⇒ lỗi xác thực về sau là `LoiApi` CÓ TÊN);
    `FLS_ZDR_DA_BAT` ⇒ `FLS_VERTEX_DU_LIEU_XAC_NHAN`. Ba chốt chung (`--that` · `FLS_CHO_GOI_API` · ghim) GIỮ NGUYÊN.
    """
    mt = os.environ if moi_truong is None else moi_truong
    thieu = []
    if not co_that:
        thieu.append("cờ `--that` vắng")
    if mt.get(BIEN_CHO_GOI) != "1":
        thieu.append(f"`{BIEN_CHO_GOI}` ≠ 1")
    # Đường chỉ áp cho họ `anthropic`; họ khác (vd `openai` chừa chỗ) giữ chốt khoá của nó.
    duong = duong_goi(mt) if mo_hinh.ho == "anthropic" else DUONG_API
    if duong in DUONG_GCP:
        du_an = mt.get(BIEN_GCP_PROJECT) or ""
        if not du_an:
            thieu.append(f"`{BIEN_GCP_PROJECT}` vắng (đường {duong})")
        elif du_an not in DU_AN_CONG_TY:
            thieu.append(f"project `{du_an}` ⛔ thuộc GCP công ty {list(DU_AN_CONG_TY)} — agent đọc nguyên văn số TK chỉ "
                         "trong GCP công ty (AC-5)")
    if duong == DUONG_GOOGLE_CLOUD:
        ws = mt.get(BIEN_CLAUDE_WORKSPACE) or ""
        if not ws:
            thieu.append(f"`{BIEN_CLAUDE_WORKSPACE}` vắng (đường google-cloud — workspace `{DAU_WORKSPACE}…` của tổ chức "
                         "Anthropic gắn với project)")
        elif not ws.startswith(DAU_WORKSPACE) or not ws.replace("_", "").isalnum():
            thieu.append(f"`{BIEN_CLAUDE_WORKSPACE}` ⛔ đúng dạng `{DAU_WORKSPACE}…`")
    elif duong == DUONG_VERTEX:
        vung = mt.get(BIEN_VERTEX_REGION) or VUNG_VERTEX_MAC_DINH
        if vung not in VUNG_VERTEX:
            thieu.append(f"vùng Vertex `{vung}` ⛔ phục vụ {mo_hinh.ma} (vùng đơn chỉ tới Sonnet 4.6) — dùng "
                         f"{'/'.join(VUNG_VERTEX)}")
    elif duong == DUONG_API:
        if not mt.get(mo_hinh.bien_khoa):
            thieu.append(f"khoá `{mo_hinh.bien_khoa}` vắng trong biến môi trường")
    else:
        thieu.append(f"`{BIEN_NHA_CUNG_CAP}={duong}` lạ — chỉ nhận {'/'.join(DUONG_HOP_LE)}")
    lg = mo_hinh.loi_ghim()
    if lg:
        thieu.append(lg)
    if che_do in CHE_DO_CAN_ZDR:
        if duong == DUONG_GOOGLE_CLOUD and mt.get(BIEN_GC_DU_LIEU) != "1":
            thieu.append(f"chế độ che `{che_do}` gửi nguyên văn tên · số TK ⇒ đòi `{BIEN_GC_DU_LIEU}=1` (người vận hành "
                         "xác nhận: project công ty · chế độ giữ dữ liệu của tổ chức Anthropic MỚI — ZDR cũ ⛔ mang sang; BG-360)")
        elif duong == DUONG_VERTEX and mt.get(BIEN_VERTEX_DU_LIEU) != "1":
            thieu.append(f"chế độ che `{che_do}` gửi nguyên văn tên · số TK ⇒ đòi `{BIEN_VERTEX_DU_LIEU}=1` (người vận "
                         "hành xác nhận: project công ty · request-response logging TẮT · trạng thái ZDR — BG-360)")
        elif duong == DUONG_API and mt.get(BIEN_ZDR) != "1":
            thieu.append(f"chế độ che `{che_do}` gửi nguyên văn tên · số TK ⇒ đòi `{BIEN_ZDR}=1` (ZDR — quyết chủ 23/11)")
    if thieu:
        raise CamGoiThat("⛔ gọi API thật: " + " · ".join(thieu))


class VuotTran(RuntimeError):
    """Chi phí cộng dồn đã chạm trần USD của vòng ⇒ ⛔ gọi tiếp (chạy tập nhỏ trước, xem chi phí — WO-355 AC-3)."""


class AnthropicMessages:
    """Adapter Anthropic Messages API — SDK `anthropic` CHÍNH THỨC, nhập MUỘN (chỉ sau khi đủ chốt).

    Tham số theo skill `claude-api` (tra 23/11) cho Opus 5.5 / Sonnet 5.5:
      · `thinking` ⛔ gửi — cả hai mô hình chạy adaptive khi bỏ tham số; `{"type": "disabled"}` / `budget_tokens` ⇒ 400.
      · `output_config={"effort": …}` đặt RÕ (Opus 5.5 mặc định `medium`, Sonnet 5.5 `high` — ⛔ dựa mặc định).
      · `tool_choice` ⛔ gửi (= `auto`); ép `any`/`tool` ⇒ 400. Prompt skill tự dặn gọi đúng công cụ.
      · ⛔ `temperature`/`top_p`/`top_k` (400 từ phiên bản API 2026-10-21) · ⛔ prefill trợ lý (400).
      · ⛔ `fallbacks`: rơi sang mô hình khác = đổi phiên bản agent trong im lặng; `refusal` ⇒ chuỗi DỪNG có tên.
      · Khối `thinking` trả về đi NGUYÊN vào lượt sau (`chuoi.chay_skill` chép `content`) — luật preserved thinking.
    `client` tiêm được cho bài thử (SDK GIẢ) — ⛔ mạng trong pytest.
    """
    ten = "anthropic"
    duong = DUONG_API
    vung = ""
    bang_gia = BANG_GIA

    def __init__(self, mo_hinh: MoHinh, co_that: bool = False, effort: str = "medium", che_do: str = "mo",
                 client: Any = None, tran_usd: float | None = None, max_retries: int = 2,
                 nhat_ky: list[NhatKyGoi] | None = None, moi_truong: dict[str, str] | None = None):
        mt = os.environ if moi_truong is None else moi_truong
        kiem_chot_that(mo_hinh, co_that, mt, che_do=che_do)
        if duong_goi(mt) != self.duong:
            raise CamGoiThat(f"`{BIEN_NHA_CUNG_CAP}={duong_goi(mt)}` ≠ đường của adapter `{self.duong}` — dựng qua `tao_that`")
        if mo_hinh.ma not in self.bang_gia:
            raise CamGoiThat(f"mô hình `{mo_hinh.ma}` ⛔ có trong bảng giá đường `{self.duong}` ⇒ ⛔ ước được chi phí ⇒ "
                             "⛔ gọi thật")
        import anthropic  # noqa: PLC0415 — chỉ tới đây khi đủ chốt
        self._sdk = anthropic
        self.mo_hinh, self.effort, self.tran_usd = mo_hinh, effort, tran_usd
        self.client = client if client is not None else self._dung_client(anthropic, mt, max_retries)
        # `nhat_ky` DÙNG CHUNG giữa các agent của một vòng ⇒ trần `tran_usd` tính trên CẢ vòng, ⛔ từng agent
        self.nhat_ky: list[NhatKyGoi] = nhat_ky if nhat_ky is not None else []

    def _dung_client(self, sdk: Any, mt: Any, max_retries: int) -> Any:
        # khoá đọc từ biến môi trường bên trong SDK — ⛔ truyền tay, ⛔ in
        return sdk.Anthropic(max_retries=max_retries)

    def _loi_xac_thuc(self, e: Exception) -> bool:
        """Lỗi xác thực ngoài lớp lỗi SDK (đường Vertex: `google.auth`) ⇒ True ⇒ `LoiApi` CÓ TÊN. Đường API: ⛔."""
        return False

    def _tham_so(self, yeu_cau: dict) -> dict[str, Any]:
        ts: dict[str, Any] = {"model": self.mo_hinh.ma, "max_tokens": yeu_cau.get("max_tokens", 16000),
                              "messages": yeu_cau["messages"], "output_config": {"effort": self.effort}}
        if yeu_cau.get("system"):
            ts["system"] = yeu_cau["system"]
        if yeu_cau.get("tools"):
            ts["tools"] = yeu_cau["tools"]
        return ts

    def goi(self, yeu_cau: dict) -> dict:
        import time  # noqa: PLC0415
        if yeu_cau.get("model") != self.mo_hinh.ma:
            raise CamGoiThat(f"yêu cầu mang mô hình `{yeu_cau.get('model')}` ≠ ghim `{self.mo_hinh.ma}`")
        da_tieu = sum(x.chi_phi_usd for x in self.nhat_ky)
        if self.tran_usd is not None and da_tieu >= self.tran_usd:
            raise VuotTran(f"đã tiêu ~{da_tieu:.4f} USD ≥ trần {self.tran_usd} USD ({len(self.nhat_ky)} lời gọi) — DỪNG")
        t0 = time.monotonic()
        try:
            tl = self.client.messages.create(**self._tham_so(yeu_cau))
        except self._sdk.APIStatusError as e:      # 4xx/5xx sau khi SDK đã thử lại — CÓ TÊN, ⛔ nội dung
            raise LoiApi(f"{type(e).__name__} HTTP {e.status_code} · request-id {getattr(e, 'request_id', None) or '—'}"
                         f" · mô hình `{self.mo_hinh.ma}`") from None
        except self._sdk.APIConnectionError as e:  # mạng / hết giờ
            raise LoiApi(f"{type(e).__name__} (mạng/hết giờ) · mô hình `{self.mo_hinh.ma}`") from None
        except Exception as e:                     # noqa: BLE001 — chỉ đổi tên lỗi XÁC THỰC; lỗi khác ném nguyên
            if not self._loi_xac_thuc(e):
                raise
            raise LoiApi(f"{type(e).__name__} (xác thực GCP/ADC — `gcloud auth application-default login` hoặc SA gắn máy)"
                         f" · đường `{self.duong}` · mô hình `{self.mo_hinh.ma}`") from None
        giay = time.monotonic() - t0
        d = tl.to_dict()
        u = d.get("usage") or {}
        vao, ra = int(u.get("input_tokens") or 0), int(u.get("output_tokens") or 0)
        cd, cg = int(u.get("cache_read_input_tokens") or 0), int(u.get("cache_creation_input_tokens") or 0)
        self.nhat_ky.append(NhatKyGoi(
            mo_hinh=str(d.get("model") or self.mo_hinh.ma), token_vao=vao, token_ra=ra, cache_doc=cd, cache_ghi=cg,
            giay=giay, chi_phi_usd=chi_phi(self.mo_hinh.ma, vao, ra, cd, cg, self.duong, self.vung),
            stop_reason=str(d.get("stop_reason")), van_tay_yeu_cau=van_tay(yeu_cau), van_tay_dap=van_tay(d),
            request_id=str(getattr(tl, "_request_id", "") or ""), duong=self.duong, vung=self.vung))
        if d.get("model") and d["model"] != self.mo_hinh.ma:
            # API phục vụ bằng mô hình khác mã ghim ⇒ phiên bản agent đã đổi ⇒ ĐỎ có tên (⛔ nhận im lặng)
            raise LoiApi(f"API trả bằng mô hình `{d['model']}` ≠ ghim `{self.mo_hinh.ma}`")
        return {"stop_reason": d.get("stop_reason"), "content": d.get("content") or []}


class AnthropicVertexMessages(AnthropicMessages):
    """Claude trên **Vertex AI** (Google managed) — `WO-359` AC-1. CÙNG khuôn yêu cầu/đáp, CÙNG tham số mô hình, CÙNG
    nhật ký + trần USD như `AnthropicMessages`; chỉ khác client và bảng giá.

    · client = `anthropic.AnthropicVertex(project_id=FLS_GCP_PROJECT, region=FLS_VERTEX_REGION)` — SDK chuyển `model` vào
      URL `…/publishers/anthropic/models/<mã>:rawPredict` và tự đặt `anthropic_version`; xác thực = ADC của GCP (SA gắn
      VM `fls-staging-app` / `gcloud auth application-default login` ở Cloud Shell) — ⛔ khoá nào đi qua mã này.
    · Lỗi xác thực của `google.auth` (⛔ ADC, token hết hạn) ⇒ `LoiApi` CÓ TÊN (⛔ rơi về GIẢ).
    · USD ước = `BANG_GIA_VERTEX` × hệ số vùng (`global` 1,0 · `us`/`eu` 1,1) — giá tra `NGAY_TRA_GIA_VERTEX`.
    """
    ten = "anthropic-vertex"
    duong = DUONG_VERTEX
    bang_gia = BANG_GIA_VERTEX

    def _dung_client(self, sdk: Any, mt: Any, max_retries: int) -> Any:
        return sdk.AnthropicVertex(project_id=mt[BIEN_GCP_PROJECT], region=self.vung, max_retries=max_retries)

    def __init__(self, mo_hinh: MoHinh, co_that: bool = False, effort: str = "medium", che_do: str = "mo",
                 client: Any = None, tran_usd: float | None = None, max_retries: int = 2,
                 nhat_ky: list[NhatKyGoi] | None = None, moi_truong: dict[str, str] | None = None):
        mt = os.environ if moi_truong is None else moi_truong
        self.vung = mt.get(BIEN_VERTEX_REGION) or VUNG_VERTEX_MAC_DINH
        self.du_an = mt.get(BIEN_GCP_PROJECT) or ""
        super().__init__(mo_hinh, co_that, effort=effort, che_do=che_do, client=client, tran_usd=tran_usd,
                         max_retries=max_retries, nhat_ky=nhat_ky, moi_truong=mt)

    def _loi_xac_thuc(self, e: Exception) -> bool:
        return any(k.__module__.startswith("google.auth") for k in type(e).__mro__)


class AnthropicGoogleCloudMessages(AnthropicMessages):
    """⭐ ĐƯỜNG CHÍNH (chủ 24/11 ~03:50) — *Claude Models on Google Cloud (Anthropic managed)*, `claude.googleapis.com`.

    Tra 24/11 (skill `claude-api` · `shared/google-cloud-anthropic-managed.md`; chữ ký đối chiếu SDK THẬT `anthropic` 2.13.0:
    `AnthropicGoogleCloud(*, project, location, workspace_id, token_provider, credentials, …, max_retries, …)`):
    · client = `anthropic.AnthropicGoogleCloud(project=FLS_GCP_PROJECT, workspace_id=FLS_CLAUDE_WORKSPACE_ID)` — ⛔ tự viết
      endpoint (*"Never write the endpoint by hand in SDK code"*); vị trí để mặc định `global`.
    · Gọi như Claude API (`messages.create`), mã mô hình như Claude API ⇒ CÙNG tham số, CÙNG nhật ký + trần như cha.
    · Xác thực = ADC (SA gắn VM / `gcloud auth application-default login`), vai `roles/claude.user`; lỗi `google.auth` ⇒
      `LoiApi` CÓ TÊN. SDK ⛔ đọc `ANTHROPIC_API_KEY` ở nền này.
    · USD ƯỚC theo `BANG_GIA_GOOGLE_CLOUD` (= giá Claude API; CHƯA có bảng giá chính thức cho nền này).
    """
    ten = "anthropic-google-cloud"
    duong = DUONG_GOOGLE_CLOUD
    vung = "global"
    bang_gia = BANG_GIA_GOOGLE_CLOUD

    def _dung_client(self, sdk: Any, mt: Any, max_retries: int) -> Any:
        return sdk.AnthropicGoogleCloud(project=mt[BIEN_GCP_PROJECT], workspace_id=mt[BIEN_CLAUDE_WORKSPACE],
                                        max_retries=max_retries)

    def _loi_xac_thuc(self, e: Exception) -> bool:
        return any(k.__module__.startswith("google.auth") for k in type(e).__mro__)


#: Họ → lớp adapter. Thêm họ (vd. `openai` giai đoạn sau) = thêm MỘT dòng + bỏ họ ấy khỏi `HO_DE_DANH`.
ADAPTER: dict[str, Any] = {"anthropic": AnthropicMessages}
#: `WO-359`: họ `anthropic` có BA đường — chọn theo `FLS_NHA_CUNG_CAP` (`duong_goi`, mặc định `google-cloud`).
ADAPTER_DUONG: dict[tuple[str, str], Any] = {("anthropic", DUONG_GOOGLE_CLOUD): AnthropicGoogleCloudMessages,
                                             ("anthropic", DUONG_VERTEX): AnthropicVertexMessages,
                                             ("anthropic", DUONG_API): AnthropicMessages}


def tao_that(mo_hinh: MoHinh, co_that: bool, che_do: str = "mo", **kw: Any) -> Any:
    """Nhà cung cấp THẬT theo HỌ của mô hình — ⛔ cứng một hãng trong giao diện.

    Họ chừa chỗ (`HO_DE_DANH`, hôm nay `openai`): chốt chạy TRƯỚC (thiếu chốt ⇒ `CamGoiThat`), rồi `ChuaDung`.
    Họ lạ ⇒ `ChuaDung` ngay. `WO-359`: họ `anthropic` ⇒ adapter theo ĐƯỜNG (`FLS_NHA_CUNG_CAP`); đường lạ ⇒ chốt báo ĐỎ."""
    if mo_hinh.ho in ADAPTER:
        mt = kw.get("moi_truong")
        lop = ADAPTER_DUONG.get((mo_hinh.ho, duong_goi(mt)))
        if lop is None:                       # đường lạ: chốt chạy để báo ĐỎ CÓ TÊN (kèm mọi chốt thiếu khác)
            kiem_chot_that(mo_hinh, co_that, mt, che_do=che_do)
            raise CamGoiThat(f"đường `{duong_goi(mt)}` ⛔ có adapter")
        return lop(mo_hinh, co_that, che_do=che_do, **kw)
    if mo_hinh.ho in HO_DE_DANH:
        kiem_chot_that(mo_hinh, co_that, che_do=che_do)
        raise ChuaDung(f"họ `{mo_hinh.ho}` CHỪA CHỖ cho giai đoạn sau (quyết chủ 23/11) — ⛔ adapter hôm nay")
    raise ChuaDung(f"họ `{mo_hinh.ho}` chưa có adapter")
