# -*- coding: utf-8 -*-
"""Bản khai **THỨ HAI** — `Range_*` của danh mục *(`GAP-KHAI-01`)*.

⛔⛔ **Hệ có HAI bản khai cho cùng một phép ánh xạ, và tới 08/09 ⛔ không cổng
   nào so hai cái:**

     ⓐ **dòng 1** của mỗi sheet `R |`      → `fls_khai_cot`  · **FLS đọc**
     ⓑ `Range_Condition/Debit/Credit`       → bảng này       · **script `Run`
        ở `BankAccountList` / `Cash Ledger List`                của trang tính đọc**

⭐ Đo tay 08/09: **192 phép so, `0` lệch** — hai bản khai đang trỏ **cùng một
  cột**. Nhưng đó là **một lần chạy tay**, ⛔ không phải một cổng. Module này
  chở vế ⓑ vào kho để `S10` so được **mỗi lần nạp**.

⛔ **Vì sao lệch ở đây NGUY một cách IM LẶNG.** Sửa dòng 1 mà quên danh mục
   *(hoặc ngược lại)* thì FLS và trang tính **đọc hai cột khác nhau**, và **cả
   hai vẫn chạy bình thường**: ⛔ không câu lệnh nào lỗi · ⛔ không dòng nào rơi
   *(`S1` vẫn cân)* · số tổng vẫn **trông hợp lý**. Cái lệch chỉ lộ ra khi có
   người **đối chiếu từng dòng** với sao kê gốc — tức là **⛔ không bao giờ**.

⛔ **Chỉ-THÊM**, cùng kỷ luật `khai_cot`: danh mục đổi ⇒ **thêm dòng mới**,
   ⛔ không sửa dòng cũ. Một lần nạp tháng trước phải giải thích được bằng
   **cái đã đọc lúc ấy**.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

# ⭐ Danh mục **chỉ khai BA trường**, ⛔ không phủ đủ 6. Khai ở đây để ⛔ không
#   ai gõ lại danh sách này ở `tools/` hay `fls/kiem/`.
BA_TRUONG: tuple[str, ...] = ("Date", "Debit", "Credit")

# `Range_*` của danh mục ↔ tên trường của bản khai dòng 1.
COT_DANH_MUC: dict[str, str] = {"Range_Condition": "Date",
                                "Range_Debit": "Debit",
                                "Range_Credit": "Credit"}

_COT = ("source_id", "truong", "cot", "dai_tho", "danh_muc")
_RE_DAI = re.compile(r"^!?\$?([A-Z]{1,3})\$?\d*\s*:\s*\$?([A-Z]{1,3})?\$?\d*$",
                     re.I)


class LoiDai(Exception):
    """Gốc của mọi lỗi tầng này."""

    ma = "FLS-DAI-HONG"


@dataclass(frozen=True)
class BanDai:
    source_id: int
    cot: dict[str, int | None]      # ⛔ `None` = ⛔ KHÔNG suy được
    tho: dict[str, str]
    danh_muc: str
    doc_luc: datetime


def cot_tu_dai(dai: str) -> int | None:
    """`!L3:L` → `11`. ⛔ **Trả `None` chứ ⛔ không đoán.**

    ⭐⭐ Ba ca trả `None`, và cả ba đều **đo được thật**:

      · **ô RỖNG** — `R | CNC` và `R | Pingpong` có **dòng danh mục đầu tiên**
        bỏ trống cả ba `Range_*` *(đo 08/09: 6 ô)*;
      · **dải nhiều cột** — `!L3:N` ⛔ không suy ra **một** cột;
      · **hình lạ** — ⛔ không khớp mẫu.

    ⛔ Ba ca ấy phải thành *"**⛔ CHƯA ĐO ĐƯỢC**"* ở `S10`, ⛔ **không** thành
      *"khớp"*. Xanh trên tập rỗng là **chưa đo**, ⛔ không phải **đạt** — luật
      nền của cả hai cổng.
    """
    s = str(dai or "").strip()
    if not s:
        return None
    m = _RE_DAI.match(s)
    if not m:
        return None
    a, b = m.group(1), m.group(2)
    if b and b.upper() != a.upper():
        return None                      # dải nhiều cột ⇒ ⛔ không suy được
    n = 0
    for ch in a.upper():
        n = n * 26 + (ord(ch) - 64)
    return n - 1


def _soi(tho: Mapping[str, str]) -> dict[str, str]:
    la = sorted(set(tho) - set(BA_TRUONG))
    if la:
        raise LoiDai("⛔ tên trường lạ %s — danh mục chỉ khai %s"
                     % (la, list(BA_TRUONG)))
    return {t: str(v or "").strip() for t, v in tho.items()}


def ghi_dai(conn, source_id: int, tho: Mapping[str, str], *,
            danh_muc: str) -> BanDai | None:
    """Ghi dải đọc của một nguồn. ⛔ **⛔ Không ghi nếu ⛔ không đổi.**

    ⭐ Trả `None` khi ⛔ không có gì để ghi — chạy lại công cụ thu ⛔ không được
      biến thành một dòng rác mỗi lần, đúng luật đã áp cho `nap_nguon_va_khai`.
    """
    sach = _soi(tho)
    if not str(danh_muc or "").strip():
        raise LoiDai("⛔ thiếu `danh_muc` — phải nói dải này đọc từ BẢNG NÀO, "
                     "vì hai lằn có hai bảng khác đầu cột")

    cu = doc_dai(conn, source_id)
    if cu is not None and cu.tho == sach:
        return None

    hang = [(source_id, t, cot_tu_dai(v), v, danh_muc)
            for t, v in sorted(sach.items())]
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT source_id FROM fls_source WHERE source_id = %s"
                        " FOR UPDATE", (source_id,))
            if cur.fetchone() is None:
                raise LoiDai("⛔ ⛔ không có nguồn `source_id=%s`" % source_id)
            cur.executemany(
                "INSERT INTO fls_nguon_dai (%s) VALUES (%s)"
                % (", ".join(_COT), ", ".join(["%s"] * len(_COT))), hang)
    ra = doc_dai(conn, source_id)
    assert ra is not None
    return ra


def doc_dai(conn, source_id: int) -> BanDai | None:
    """Dải **mới nhất** của một nguồn. `None` nếu ⛔ chưa thu bao giờ.

    ⭐ *"Mới nhất theo từng trường"*, ⛔ không phải *"cả lô mới nhất"*: danh mục
      là bảng của người khác, một trường có thể đổi mà hai trường kia thì ⛔
      không, và ta chỉ ghi thêm những gì thật sự đổi.
    """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT DISTINCT ON (truong) truong, cot, dai_tho, danh_muc, doc_luc"
            "  FROM fls_nguon_dai WHERE source_id = %s"
            " ORDER BY truong, doc_luc DESC, dai_id DESC", (source_id,))
        hang = cur.fetchall()
    if not hang:
        return None
    return BanDai(
        source_id=source_id,
        cot={r[0]: r[1] for r in hang},
        tho={r[0]: r[2] for r in hang},
        danh_muc=hang[0][3],
        doc_luc=max(r[4] for r in hang))
