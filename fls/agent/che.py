# -*- coding: utf-8 -*-
"""Bộ che `NFR-I13` — chạy TRƯỚC MỌI lời gọi mô hình (phát lại, giả, thật: CÙNG một đường).

⭐ `NFR-I13 ③` *(owner 17/09)*: chặn bằng DANH SÁCH TRẮNG ở TỪ VỰNG, ⛔ danh sách ĐEN ở dữ liệu —
   *"danh sách ĐEN luôn thua khi nguồn thêm cột, và vòng ① là bằng chứng nó đã thua"*. Nên:
   LỚP 1 (TRẮNG) — dữ liệu (kết quả công cụ) chỉ rời máy nếu
     · KHOÁ là mã ô `voi:` · `hd2:` · `nguon:` · `cong:` · `noi:` (khuôn `MAU_KHOA_O`), và
     · GIÁ TRỊ là số · bool · null · hoặc chuỗi thuộc một khuôn an toàn `MAU_CHUOI_AN_TOAN`.
     Khác ⇒ khoá BỎ / giá trị thành `null` (đếm, có tên khoá, ⛔ giá trị).
   NGOẠI LỆ DUY NHẤT — ô `noi:<ca>.noi_dung` (nội dung giao dịch cho skill ghép theo nội dung, chủ 23/11):
     · cờ `cho_noi_dung=False` (MẶC ĐỊNH, đúng WO-329 AC-3 *"Diễn giải ⛔ rời máy"*) ⇒ ô thành `null`;
     · cờ bật ⇒ chữ đi qua `che_noi_dung` (thay số dài · email · điện thoại · tên người bằng thẻ) —
       bật hay không là QUYẾT ĐỊNH CỦA CHỦ (câu chủ C4 ở BG-330), ⛔ của mã.
   LỚP 2 (ĐEN, chốt cuối) trên TOÀN yêu cầu đã che, đi vào cả JSON lồng trong `tool_result`:
     email · dãy ≥ 9 chữ số trong CHUỖI (số tiền đi dạng SỐ JSON nên ⛔ vướng) · tên trường cấm làm khoá.
     Bắt được ⇒ `CamGui` — lời gọi BỊ TỪ CHỐI, ⛔ gửi.

⛔ Năm thứ ⛔ rời máy *(WO-329 AC-3)*: `Diễn giải` · `Số chứng từ` · tên người · email · số TK cá nhân.
   Bài chứng minh: `tests/agent/test_che.py` — nhà cung cấp gián điệp ghi ĐÚNG byte nó nhận.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

MAU_KHOA_O = re.compile(r"(voi|hd2|nguon|cong|noi):[A-Za-z0-9_\-]+(\.[A-Za-z0-9_\-]+)*")
MAU_CHUOI_AN_TOAN = (
    re.compile(r"[0-9a-f]{16}"),                 # vân tay ảnh (16 hex)
    re.compile(r"\d{4}-\d{2}(-\d{2})?"),         # kỳ `2025-01` · ngày `2026-08-26`
    re.compile(r"WP-C\d+[a-z]?"),                # mã gói HD2
    re.compile(r"[A-Z]{3}"),                     # mã tiền tệ
    re.compile(r"PM-[0-9A-Z\-]{1,24}"),          # mã PM line (ca ghép)
    re.compile(r"DE_NGUOI|A|B|C|D|E|F|L3"),      # nhãn quyết định ghép · hình ghép
)
TRUONG_CAM = ("diễn giải", "dien_giai", "description", "số chứng từ", "so_chung_tu", "reference number",
              "tên tài khoản", "ten_tai_khoan", "số tài khoản", "so_tai_khoan", "email address", "email",
              "memo", "tho", "ghi chú", "ghi_chu", "nguoi_nhan", "payee name")
MAU_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
MAU_SO_DAI = re.compile(r"(?<![0-9a-fA-F])\d{9,}(?![0-9a-fA-F])")
MAU_DIEN_THOAI = re.compile(r"(?<![0-9a-fA-F])(\+84|0)\d{9,10}(?![0-9a-fA-F])")   # ⛔ bắt trong vân tay hex
# Tên người trong nội dung sao kê: chữ HOA không dấu, bắt đầu bằng một HỌ Việt phổ biến, 2–4 từ.
# ⚠ Đây là lớp ĐEN bên trong ngoại lệ — nó SẼ lọt tên lạ; vì thế cờ `cho_noi_dung` mặc định TẮT
#   và việc bật là quyết định có đo của chủ (`NFR-I13 ②`: đo trước, cả hai vế).
HO_VIET = ("NGUYEN", "TRAN", "LE", "PHAM", "HOANG", "HUYNH", "PHAN", "VU", "VO", "DANG", "BUI", "DO",
           "HO", "NGO", "DUONG", "LY", "HA", "TRINH", "DINH", "LAM", "MAI", "TRUONG", "CAO", "LUONG",
           "TA", "TO", "VUONG", "KIEU", "THAI", "QUACH", "DAO", "DOAN", "LUU", "CHU", "TANG")
# ⚠ từ ngay sau tên mà dính `-`/số (mã `PM-1201-01`) ⛔ thuộc tên — đo 23/11: bản đầu nuốt `PM` của
#   "TRAN THI B PM-1201-01" ⇒ mã PM mất ⇒ ca dựng c12 trượt ghép (fleet eval vòng 3 bắt được).
MAU_TEN = re.compile(r"\b(?:" + "|".join(HO_VIET) + r")(?:\s+[A-Z]{1,8}\b(?![\-\d])){1,3}")
KHOA_NOI_DUNG = re.compile(r"noi:[A-Za-z0-9_\-]+\.noi_dung")


# ⭐⭐ QUYẾT ĐỊNH CHỦ 23/11 (sau BG-330): *"Không cần che nội dung hay stk, cho phép agents access toàn bộ, vì
#   agents có thể học mapping, sẽ có 1 vài stk ngân hàng sẽ chỉ chi một loại giao dịch nhất định."*
#   ⇒ chế độ MẶC ĐỊNH = `mo`: dữ liệu công cụ đi NGUYÊN VĂN (nội dung giao dịch · số TK · tên). Chỉ còn bỏ cột
#   `PM_COT_RIENG_TU = {"Email Address"}` (CLAUDE.md — cột ấy ⛔ bao giờ vào kho nên ⛔ có lý do rời máy).
#   Hai chế độ cũ GIỮ làm tuỳ chọn (`--che`), có bài: `che_noi_dung` (thay số/tên/email/ĐT bằng thẻ) ·
#   `che_het` (danh sách trắng mã ô, nội dung thành null — đúng WO-329 AC-3 bản gốc).
CHE_DO = ("mo", "che_noi_dung", "che_het")
CHE_DO_MAC_DINH = "mo"
COT_RIENG_TU = ("Email Address",)


class CamGui(RuntimeError):
    """Lớp 2 bắt được dữ liệu cấm SAU khi che ⇒ lời gọi bị từ chối (⛔ gửi)."""


@dataclass
class BaoCaoChe:
    bo_khoa: list[str] = field(default_factory=list)     # khoá bị bỏ (cắt 40 ký tự — ⛔ giá trị)
    bo_gia_tri: list[str] = field(default_factory=list)  # mã ô bị thay giá trị bằng null
    the_noi_dung: int = 0                                # số thẻ <SO>/<TEN>/… đã thay trong nội dung

    @property
    def so_bo(self) -> int:
        return len(self.bo_khoa) + len(self.bo_gia_tri)


def che_noi_dung(van: str) -> tuple[str, int]:
    """Che MỘT chuỗi nội dung giao dịch. Trả (chữ đã che, số thẻ đã thay)."""
    n = 0

    def thay(mau: re.Pattern, the: str, s: str) -> str:
        nonlocal n
        s2, k = mau.subn(the, s)
        n += k
        return s2
    s = thay(MAU_EMAIL, "<EMAIL>", van)
    s = thay(MAU_DIEN_THOAI, "<DT>", s)
    s = thay(re.compile(r"\d{6,}"), "<SO>", s)
    s = thay(MAU_TEN, "<TEN>", s)
    return s, n


def _an_toan(v: Any) -> bool:
    if v is None or isinstance(v, (bool, int, float)):
        return True
    if isinstance(v, str):
        return any(m.fullmatch(v) for m in MAU_CHUOI_AN_TOAN)
    if isinstance(v, list):
        return all(_an_toan(x) and not isinstance(x, list) for x in v)
    return False


def che_du_lieu(du_lieu: Any, bc: BaoCaoChe | None = None, cho_noi_dung: bool = False) -> tuple[dict, BaoCaoChe]:
    """Lớp 1 (TRẮNG) cho KẾT QUẢ CÔNG CỤ: chỉ còn `{mã ô: giá trị an toàn}`."""
    bc = bc or BaoCaoChe()
    if not isinstance(du_lieu, dict):
        bc.bo_khoa.append(f"<{type(du_lieu).__name__}>")
        return {}, bc
    ra: dict[str, Any] = {}
    for k, v in du_lieu.items():
        if not isinstance(k, str) or not MAU_KHOA_O.fullmatch(k):
            bc.bo_khoa.append(str(k)[:40])
            continue
        if KHOA_NOI_DUNG.fullmatch(k):
            if cho_noi_dung and isinstance(v, str):
                ra[k], n = che_noi_dung(v)
                bc.the_noi_dung += n
            else:
                ra[k] = None
                bc.bo_gia_tri.append(k)
            continue
        if _an_toan(v):
            ra[k] = v
        else:
            ra[k] = None
            bc.bo_gia_tri.append(k)
    return ra, bc


def kiem_den(yeu_cau: dict) -> list[str]:
    """Lớp 2 (ĐEN) — đi MỌI chuỗi và MỌI khoá (kể cả JSON lồng trong chuỗi). ⛔ in giá trị."""
    dem = {"email": 0, "so_dai": 0, "dt": 0}
    khoa_cam: set[str] = set()

    def di(x: Any) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if isinstance(k, str) and k.strip().lower() in TRUONG_CAM:
                    khoa_cam.add(k.strip().lower())
                di(v)
        elif isinstance(x, list):
            for v in x:
                di(v)
        elif isinstance(x, str):
            s = x.strip()
            if s[:1] in "{[":
                try:
                    di(json.loads(s))
                    return
                except json.JSONDecodeError:
                    pass
            dem["email"] += len(MAU_EMAIL.findall(x))
            dem["so_dai"] += len(MAU_SO_DAI.findall(x))
            dem["dt"] += len(MAU_DIEN_THOAI.findall(x))
    # Khoá của KHUÔN API (`tools[].description` · `input_schema`) ⛔ là dữ liệu: soát khoá chỉ ở `messages`/`system`;
    # chuỗi thì soát MỌI nơi (kể cả mô tả công cụ).
    for k, v in yeu_cau.items():
        if k == "tools":
            for t in v or []:
                for x in (t.get("description"), t.get("name")):
                    di(x)
        else:
            di({k: v} if k in ("messages", "system") else v)
    ly = [f"{t}: {n} chỗ" for t, n in (("email", dem["email"]), ("dãy ≥ 9 chữ số trong chuỗi (số TK?)",
          dem["so_dai"]), ("số điện thoại", dem["dt"])) if n]
    if khoa_cam:
        ly.append(f"trường cấm làm khoá: {sorted(khoa_cam)}")
    return ly


def _bo_rieng_tu(x: Any, bc: BaoCaoChe) -> Any:
    if isinstance(x, dict):
        ra = {}
        for k, v in x.items():
            if k in COT_RIENG_TU or (isinstance(k, str) and k.rsplit(".", 1)[-1] in COT_RIENG_TU):
                bc.bo_khoa.append(str(k)[:40])
                continue
            ra[k] = _bo_rieng_tu(v, bc)
        return ra
    if isinstance(x, list):
        return [_bo_rieng_tu(v, bc) for v in x]
    return x


def che_yeu_cau(yeu_cau: dict, che_do: str = CHE_DO_MAC_DINH) -> tuple[dict, BaoCaoChe]:
    """Che MỘT yêu cầu Messages trước khi giao cho nhà cung cấp.

    · `mo` (MẶC ĐỊNH, chủ 23/11): chỉ bỏ `COT_RIENG_TU`; ⛔ lớp 2.
    · `che_noi_dung` · `che_het`: như dưới.

    · `tool_result.content` (JSON) ⇒ lớp 1. Nội dung ⛔ phải JSON dict ⇒ bỏ hết (`{}`).
    · `system` + chữ `user` là PROMPT trong repo (đã ghim checksum) ⇒ ⛔ che, nhưng VẪN qua lớp 2.
    · Lớp 2 bắt được gì ⇒ `CamGui`.
    """
    if che_do not in CHE_DO:
        raise ValueError(f"chế độ che `{che_do}` ⛔ thuộc {CHE_DO}")
    bc = BaoCaoChe()
    ra = json.loads(json.dumps(yeu_cau, ensure_ascii=False))
    if che_do == "mo":
        for tn in ra.get("messages", []):
            for khoi in (tn.get("content") if isinstance(tn.get("content"), list) else []):
                if isinstance(khoi, dict) and khoi.get("type") == "tool_result":
                    try:
                        du = json.loads(khoi.get("content") or "")
                    except (TypeError, json.JSONDecodeError):
                        continue
                    khoi["content"] = json.dumps(_bo_rieng_tu(du, bc), ensure_ascii=False, sort_keys=True)
        return ra, bc
    cho_noi_dung = che_do == "che_noi_dung"
    for tn in ra.get("messages", []):
        noi = tn.get("content")
        if not isinstance(noi, list):
            continue
        for khoi in noi:
            if isinstance(khoi, dict) and khoi.get("type") == "tool_result":
                try:
                    du = json.loads(khoi.get("content") or "")
                except (TypeError, json.JSONDecodeError):
                    du = None
                sach, bc = che_du_lieu(du, bc, cho_noi_dung)
                khoi["content"] = json.dumps(sach, ensure_ascii=False, sort_keys=True)
    ly = kiem_den(ra)
    if ly:
        raise CamGui("⛔ dữ liệu cấm còn trong yêu cầu SAU khi che — từ chối gửi: " + " · ".join(ly))
    return ra, bc
