# -*- coding: utf-8 -*-
"""Bộ skill có THỨ TỰ — mỗi skill MỘT tệp `fls/agent/skill/<agent>/NN_<tên>.md`.

⭐ Thứ tự = số `NN` ở đầu tên tệp (01, 02, …) — ⛔ thứ tự liệt kê, ⛔ thứ tự hệ tệp.
   Số trùng · số nhảy (01, 03) · tệp ⛔ có số ⇒ `LoiBoSkill` (ĐỎ khi NẠP, ⛔ khi chạy giữa chừng).

Tệp skill = đầu khai (giữa hai dòng `---`, mỗi dòng `khoá: giá trị`) + PROMPT (phần còn lại, gửi mô hình).
   ten        tên skill (người đọc)
   cong_cu    tên công cụ FLS DUY NHẤT skill được gọi (tiêm từ `tools/chay_agent_voi.py`)
   o          mẫu mã ô đầu ra, phân cách `,` (xem `o.py`) — mở rộng trên dữ liệu MÁY
   cong       tên cổng ra (`cong_skill.CONG`) + tham số sau `:`
   loai       `lam` (mô hình làm, đầu ra so 100 % với máy) · `bong` (G0 bóng — so với đáp án giữ riêng,
              ⛔ ghi, ⛔ cộng vào lệch agent ↔ máy) · `ma` (mã tất định, ⛔ gọi mô hình — A4)

Checksum prompt của agent = sha256 các tệp skill + `00_he_thong.md`, theo thứ tự tên — một phiên bản
agent = mã mô hình ghim + checksum prompt + checksum tham chiếu (Voi phase 1 §F0b ⑤).
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

THU_MUC = Path(__file__).resolve().parent / "skill"
MAU_TEN = re.compile(r"(\d{2})_([a-z0-9_]+)\.md")
KHOA_BAT_BUOC = ("ten", "cong_cu", "o", "cong", "loai")
LOAI = ("lam", "bong", "ma")


class LoiBoSkill(ValueError):
    pass


@dataclass(frozen=True)
class Skill:
    agent: str
    so: int
    ma: str                      # `NN_tên`
    ten: str
    cong_cu: str
    mau_o: tuple[str, ...]
    cong: str
    loai: str
    prompt: str
    tep: Path = field(compare=False)

    @property
    def nhan(self) -> str:
        return f"{self.agent}/{self.ma}"


def doc_tep(agent: str, tep: Path) -> Skill:
    m = MAU_TEN.fullmatch(tep.name)
    if not m:
        raise LoiBoSkill(f"{agent}: tệp `{tep.name}` ⛔ theo khuôn `NN_ten.md`")
    van = tep.read_text(encoding="utf-8")
    dong = van.split("\n")
    if not dong or dong[0].strip() != "---" or "---" not in [x.strip() for x in dong[1:]]:
        raise LoiBoSkill(f"{agent}/{tep.name}: ⛔ có đầu khai `---`")
    het = 1 + [x.strip() for x in dong[1:]].index("---")
    khai: dict[str, str] = {}
    for x in dong[1:het]:
        if ":" in x:
            k, _, v = x.partition(":")
            khai[k.strip()] = v.strip()
    thieu = [k for k in KHOA_BAT_BUOC if not khai.get(k)]
    if thieu:
        raise LoiBoSkill(f"{agent}/{tep.name}: đầu khai thiếu {thieu}")
    if khai["loai"] not in LOAI:
        raise LoiBoSkill(f"{agent}/{tep.name}: loai `{khai['loai']}` ⛔ thuộc {LOAI}")
    return Skill(agent=agent, so=int(m.group(1)), ma=tep.stem, ten=khai["ten"], cong_cu=khai["cong_cu"],
                 mau_o=tuple(x.strip() for x in khai["o"].split(",") if x.strip() not in ("", "-")), cong=khai["cong"],
                 loai=khai["loai"], prompt="\n".join(dong[het + 1:]).strip(), tep=tep)


def nap_bo(agent: str, goc: Path = THU_MUC) -> list[Skill]:
    """Bộ skill của `agent`, đã xếp theo số; kiểm số liền 01…n, ⛔ trùng."""
    tm = goc / agent
    if not tm.is_dir():
        raise LoiBoSkill(f"{agent}: ⛔ có thư mục skill `{tm.name}`")
    tep = [p for p in sorted(tm.iterdir()) if p.suffix == ".md" and p.name != "00_he_thong.md"]
    bo = [doc_tep(agent, p) for p in tep]
    so = [s.so for s in bo]
    if not bo:
        raise LoiBoSkill(f"{agent}: 0 skill (Đ3)")
    if so != list(range(1, len(bo) + 1)):
        raise LoiBoSkill(f"{agent}: số thứ tự {so} ≠ 01…{len(bo):02d} (trùng hoặc nhảy)")
    return bo


def he_thong(agent: str, goc: Path = THU_MUC) -> str:
    p = goc / agent / "00_he_thong.md"
    if not p.is_file():
        raise LoiBoSkill(f"{agent}: thiếu `00_he_thong.md`")
    return p.read_text(encoding="utf-8").strip()


def checksum_prompt(agent: str, goc: Path = THU_MUC) -> str:
    """sha256 (16 hex) của `00_he_thong.md` + mọi tệp skill, theo thứ tự tên — byte nguyên văn."""
    h = hashlib.sha256()
    for p in sorted((goc / agent).iterdir()):
        if p.suffix == ".md":
            h.update(p.name.encode("utf-8") + b"\0" + p.read_bytes() + b"\0")
    return h.hexdigest()[:16]
