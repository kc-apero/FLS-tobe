# -*- coding: utf-8 -*-
"""Đo RÒ RỈ của bộ che `NFR-I13` (`fls.agent.che.che_noi_dung`) trên MỘT bể giữ riêng — `WO-338 AC-4`.

    FLS_HELDOUT_NOI_DUNG=/ngoai/repo python tools/do_ro_ri_che.py a      # in SỐ ĐẾM, ⛔ in mẫu

⭐ Bốn loại thứ phải ĐẾM = 0 sau che *(WO-329 AC-3: tên người · số TK · email · Số chứng từ)* — bằng bộ dò ĐỘC LẬP
   với bộ che *(⛔ dùng lại `MAU_TEN` của bộ che: phép so ấy tự khớp mình — Đ2)*:
   `email`        mẫu email
   `so_tk`        dãy ≥ 8 chữ số, KỂ CẢ khi xen dấu cách / `.` / `-` *(`0123 4567 89`)* — bộ che chỉ thay `\\d{6,}` liền
   `so_chung_tu`  chuỗi `Số chứng từ` của CHÍNH dòng bank (từ `meta.json`) còn nằm nguyên trong nội dung đã che
   `ten_ung_vien` họ Việt (bỏ dấu, KHÔNG phân biệt hoa/thường ở họ nhưng phải VIẾT HOA CHỮ ĐẦU) + 1–3 từ chữ
                  ⇒ ĐẾM ỨNG VIÊN, ⛔ khẳng định là tên thật *(có thể dương giả: từ thường trùng họ)*.
⭐ Đ3 — một phép đo ra 0 phải chứng minh tập KHÔNG RỖNG: in kèm `mau_so` (số nội dung đã quét) và `truoc_che`
   (CÙNG bộ dò chạy trên chữ CHƯA che): nếu `truoc_che` = 0 thì phép đo ⛔ có nghĩa ⇒ `hop_le = False`.
⭐ Thêm lớp 2 của chính bộ che: `che.kiem_den` trên nội dung đã che — đếm số ca bị `CamGui` *(lời gọi sẽ bị từ chối)*.
"""
from __future__ import annotations

import json
import os
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.agent import che  # noqa: E402

MAU_EMAIL = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
MAU_SO_TK = re.compile(r"(?<![\d.\-])\d(?:[ .\-]?\d){7,}(?![\d])")
HO = {"NGUYEN", "TRAN", "LE", "PHAM", "HOANG", "HUYNH", "PHAN", "VU", "VO", "DANG", "BUI", "DO", "HO", "NGO", "DUONG",
      "LY", "HA", "TRINH", "DINH", "LAM", "MAI", "TRUONG", "CAO", "LUONG", "TA", "TO", "VUONG", "KIEU", "THAI", "QUACH",
      "DAO", "DOAN", "LUU", "CHU", "TANG", "TRIEU", "PHUNG", "LA", "TONG", "BACH", "DIEP", "THACH", "MAC"}
MAU_TU = re.compile(r"[^\W\d_]{2,}", re.UNICODE)


def _bo_dau(s: str) -> str:
    s = s.replace("Đ", "D").replace("đ", "d")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def dem_ten(van: str) -> int:
    """Ứng viên tên: họ Việt VIẾT HOA chữ đầu + 1–3 từ cũng viết hoa chữ đầu (hoặc toàn HOA)."""
    tu = [(m.group(0), m.start(), m.end()) for m in MAU_TU.finditer(van)]
    n = i = 0
    while i < len(tu):
        t = tu[i][0]
        if _bo_dau(t).upper() in HO and t[0].isupper():
            j = i + 1
            while j < len(tu) and j - i <= 3 and tu[j][0][0].isupper() and van[tu[j - 1][2]:tu[j][1]].strip() == "":
                j += 1
            if j - i >= 2:
                n += 1
                i = j
                continue
        i += 1
    return n


def dem_mot(van: str, so_ct: str | None) -> dict[str, int]:
    return {"email": len(MAU_EMAIL.findall(van)), "so_tk": len(MAU_SO_TK.findall(van)),
            "so_chung_tu": int(bool(so_ct) and len(str(so_ct)) >= 6 and str(so_ct) in van.replace(" ", "")),
            "ten_ung_vien": dem_ten(van)}


def do(ca: dict, meta: dict | None = None) -> dict[str, Any]:
    """`ca` = `{"ca": {id: {noi_dung, ...}}}`; `meta[id]["so_ct"]` (tuỳ chọn) = Số chứng từ thật của dòng."""
    meta = meta or {}
    tru = {k: 0 for k in ("email", "so_tk", "so_chung_tu", "ten_ung_vien")}
    sau = dict(tru)
    mau_so = cam_gui = the = 0
    for cid, c in ca["ca"].items():
        nd = c.get("noi_dung")
        if not isinstance(nd, str) or not nd.strip():
            continue
        mau_so += 1
        so_ct = (meta.get(cid) or {}).get("so_ct")
        for k, v in dem_mot(nd, so_ct).items():
            tru[k] += v
        da_che, n = che.che_noi_dung(nd)
        the += n
        for k, v in dem_mot(da_che, so_ct).items():
            sau[k] += v
        if che.kiem_den({"messages": [{"role": "user", "content": da_che}]}):
            cam_gui += 1
    return {"mau_so_noi_dung": mau_so, "the_da_thay": the, "truoc_che": tru, "sau_che": sau,
            "tong_lot_sau_che": sum(sau.values()), "ca_bi_lop2_chan": cam_gui,
            "hop_le": mau_so > 0 and sum(tru.values()) > 0,      # Đ3: bộ dò phải THẤY gì đó trên chữ chưa che (TỔNG)
            # ⭐ `HELD-R1-04`: bản R0 chỉ kiểm TỔNG ⇒ loại có `truoc_che = 0` (đo 23/11: `email` · `so_chung_tu`) vẫn in
            # "0 lọt sau che" như số đo — tập RỖNG. Nay từng loại khai riêng: `False` ⇒ "0 lọt" của loại ấy ⛔ có nghĩa.
            "do_duoc_theo_loai": {k: tru[k] > 0 for k in tru}}


def main(argv: list[str] | None = None) -> int:
    a = (argv if argv is not None else sys.argv[1:]) or ["a"]
    tm = os.environ.get("FLS_HELDOUT_NOI_DUNG")
    if not tm:
        print("⛔ ĐỎ: thiếu FLS_HELDOUT_NOI_DUNG (⛔ đo được)")
        return 2
    d = Path(tm) / a[0]
    ca = json.loads((d / "ca.json").read_text(encoding="utf-8"))
    mp = d / "meta.json"
    r = do(ca, json.loads(mp.read_text(encoding="utf-8")) if mp.exists() else {})
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0 if r["hop_le"] and r["tong_lot_sau_che"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
