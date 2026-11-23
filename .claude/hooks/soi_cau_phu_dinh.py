# -*- coding: utf-8 -*-
"""Coi cho MOT lop loi da can BA LAN trong mot buoi (2026-09-17).

Doc JSON cua `PreToolUse` tren `Write|Edit`. Neu noi dung sap ghi mang mot
**cau PHU DINH DINH LUONG** ve tep/cho/noi, chen mot doan nhac vao ngu canh.

⛔⛔ **Vi sao chi bat DUNG mot ho mau hep — va con so di kem.**
Do 17/09 tren ca repo truoc khi bat coi *(bai `alarm-worth-equals-rarity`:
DEM so dong bi cham TRUOC khi bat bao)*:

    "chưa ai"                        142 lan  ⇒ ⛔ QUA DAY, coi se bi tat
    "chưa bao giờ"                    37 lan  ⇒ ⛔ qua day
    (không|chưa) (một )?(tệp|chỗ|nơi) nào
                          docs 9 · code 0     ⇒ ⭐ DU HIEM
                          va 6/9 nam trong DUNG tep toi viet sai

⇒ Mot coi kem chinh xac se bi bo qua, va luc do no te hon la ⛔ khong co.

⛔ **No ⛔ KHONG chan.** Cua van chay; no chi **nhac**, vi mot cau phu dinh
   co the DUNG — chi la no phai co phep do di kem.
"""
from __future__ import annotations

import json
import re
import sys

MAU = re.compile(r"(không|chưa)\s+(một\s+)?(tệp|chỗ|nơi)\s+nào", re.I)

NHAC = (
    "⛔ Bạn sắp ghi một CÂU PHỦ ĐỊNH ĐỊNH LƯỢNG ({n} chỗ): {vd}\n"
    "Lớp lỗi này đã cắn BA LẦN ngày 17/09 — mỗi lần thứ bị phủ định đều "
    "ĐANG TỒN TẠI:\n"
    "  · «tài liệu chưa bao giờ đọc TÊN TỆP» → BA-05:39 + :130 đã khai đủ\n"
    "  · «cấu trúc ITL Ledge chưa ai nối được» → BA-05 §DD-I04 khai trọn\n"
    "  · «không tệp nào ghi bề rộng PM_Unpivot» → FLS-Process-PM-den-ITL.md"
    ":186 và pm_join.py:192 đều ghi 28 cột\n"
    "⇒ TRƯỚC KHI GHI: grep CẢ `docs/` LẪN `fls/`+`tools/` trong chính lượt "
    "này, rồi dán SỐ ĐẾM cạnh câu. Ở repo này một sự thật đã đo THƯỜNG SỐNG "
    "TRONG CHÚ THÍCH MÃ, ⛔ không phải trong tài liệu."
)


def main() -> int:
    try:
        d = json.load(sys.stdin)
    except Exception:
        return 0                       # ⛔ coi hong ⛔ khong duoc chan cua
    ti = d.get("tool_input") or {}
    noi_dung = " \n".join(
        str(ti.get(k) or "") for k in ("content", "new_string"))
    hit = MAU.findall(noi_dung)
    if not hit:
        return 0
    vd = " · ".join(
        sorted({" ".join(x for x in m if x).strip() for m in hit})[:3])
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "additionalContext": NHAC.format(n=len(hit), vd=vd)}},
        ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
