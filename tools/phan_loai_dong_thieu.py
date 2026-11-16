# -*- coding: utf-8 -*-
"""PHÂN LOẠI DÒNG THIẾU — HD1 · kiểm kê dòng sổ AS-IS chưa ghép 1-1, trên ẢNH ĐÓNG BĂNG.

ISP 3.1.2 · Step 3 · DT1a · `WO-080` · AP v3.1.2 §5.3.1 HD1 ★ · §5.3.2 AC10 · §2.5.3.

⭐ Vì sao có tệp này. HD1 = *"mapping được 100 %, giống các dữ liệu quá khứ"* (owner 16/11). Trên ảnh
   đóng băng, mã FLS ghép 1-1 được **9.845** trong **9.967** dòng sổ `ITL Ledge` (98,78 %) — phần còn lại
   **122** dòng sổ ⛔ có cặp, và chiều ngược **147** dòng FLS ⛔ có dòng sổ. Trước bước này hai con số ấy
   chỉ sống trong một phép đo TAY của orchestrator (16/11): ⛔ máy nào đỏ khi chúng đổi, ⛔ ai liệt kê
   được ĐÚNG 122 dòng nào để DT1b gán lý do. Tệp này liệt kê, ghim, và ĐỎ khi khác.

Hai tập — mỗi tập nói NÓ ĐẾM GÌ (Đ4), đơn vị là DÒNG:
  THIẾU = `dong_sheet` của sổ (`itl_ledge_adjustment.json`, 9.967 dòng, 23 kỳ)
          ∖ `dong_so` đã ghép (`classifying_vs_canon.json`, 9.845 dòng).
          Mỗi dòng mang thuộc tính ĐO ĐƯỢC trên ảnh: kỳ · hd / pay_type / cdt1 × Classifying / MID / Final,
          và `nhan = null` — LÝ DO là việc của DT1b (cần khoá đọc ở nguồn: ảnh đã bỏ Số CT · TK · tiền).
  NGƯỢC = dòng FLS dựng lại (`pm_join.json` · bank, 9.992 dòng = `so_dong_canon` của ảnh ghép)
          ∖ `dong_canon` đã ghép. ISP: *"chỉ ĐẾM"* — ⛔ ảnh nào mang thuộc tính của dòng canon ⛔ ghép,
          nên mỗi dòng chỉ có số dòng canon + `nhan = null`.

⛔⛔ Mỗi phép trừ chỉ có nghĩa khi hai tập ĐÚNG là tập con của nhau và ⛔ trùng — nên tệp này đếm
   HAI cách và đòi khớp (Đ2 — so HAI NGUỒN): hiệu số đếm `9.967 − 9.845` ↔ cỡ tập liệt kê; dòng ghép
   trỏ dòng sổ ⛔ có ⇒ ĐỎ, `dong_so` trùng ⇒ ĐỎ, `dong_canon` ⛔ thuộc bank ⇒ ĐỎ.

Cổng (Đ5 — khai `MONG`, NO khi khác, cả hai chiều):
  · `MONG` dưới đây lấy từ phép đo TAY ĐỘC LẬP của orchestrator 16/11 (`WO-080`), ⛔ từ lần chạy đầu của
    chính tệp này — trừ `van_tay` (ghim ở lần chạy đầu, sau khi mọi số khác đã khớp phép đo độc lập).
  · ⚠ VÌ SAO CÓ VÂN TAY. Các cổng TỔNG (122 · phân bố kỳ · phân bố thuộc tính) đều MÙ trước một phép
    ĐỔI CHỖ: một dòng ghép trỏ sang một dòng thiếu CÙNG kỳ, CÙNG hd/pay_type ⇒ 122 vẫn 122, mọi phân
    bố y nguyên, mà tập dòng DT1b sẽ gán nhãn đã khác (bài thử `…doi_cho_CUNG_KY…` dựng đúng cặp ấy —
    đo 16/11: 1.401 cặp như vậy). Đúng bẫy `Đ4`: `52 = 24 + 28` hay `38 + 14` đều ra 52.
  · Mẫu số `0` là ĐỎ, ⛔ phải `0 %` (Đ3 · `S0-R1-05`); ⛔ đo được (ảnh thiếu, JSON hỏng) là ĐỎ với
    nguyên nhân trong MỘT dòng, ⛔ traceback (`S0-R1-04`).
  · Ba checksum ảnh so `MONG` của `tools/do_voi_so_luong.py` (ISP mục 5 — tiền điều kiện) — lấy THẲNG
    từ đó, ⛔ chép lại: một bản khai. Ảnh sổ được TÍNH LẠI từ nội dung; hai ảnh kia so trường
    `checksum_noi_dung` đã ghim, ĐÚNG như `do_voi_so_luong.py` (⛔ tệp sinh ra hai ảnh ấy có trong repo
    nên ⛔ tính lại được — giới hạn đã ghi ở BG-081).

⛔ Riêng tư (`PM_COT_RIENG_TU`, `CLAUDE.md`): JSON ra ⛔ mang `Diễn giải` · `Số chứng từ` · email; ⛔ mang
   chuỗi lỗi `#N/A (Did not find value '…')` — chuỗi ấy NHÚNG mã giao dịch. `kiem_rieng_tu` chặn TRƯỚC
   khi ghi. Tệp này ⛔ đọc kho, ⛔ đọc Drive/mạng: chỉ ba ảnh trong `tests/fixture/`.

Chạy (từ gốc repo):
  python tools/phan_loai_dong_thieu.py                  # in bảng, ⛔ ghi
  python tools/phan_loai_dong_thieu.py --ghi            # + ghi docs/ITL/_tools/phan_loai_dong_thieu.json
  python tools/phan_loai_dong_thieu.py --thu-muc <dir>  # đo trên BẢN SAO ba ảnh (chứng minh ĐỎ); ⛔ cùng --ghi
Mã thoát: 0 = mọi phép so khớp MONG · 1 = ĐỎ (khác MONG, hoặc ⛔ đo được) · 2 = sai cách gọi.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.ledger.final_rule import KHONG_TRA_LOI  # noqa: E402
# ⭐ MỘT bản khai cho checksum ảnh + cách băm ảnh sổ — ISP mục 5: "khớp MONG của do_voi_so_luong.py".
from tools.do_voi_so_luong import MONG as MONG_VOI  # noqa: E402
from tools.do_voi_so_luong import _sha  # noqa: E402

FX = GOC / "tests" / "fixture"
RA = GOC / "docs" / "ITL" / "_tools" / "phan_loai_dong_thieu.json"
ANH_SO, ANH_GHEP, ANH_PM = "itl_ledge_adjustment.json", "classifying_vs_canon.json", "pm_join.json"

# Thuộc tính đo được của một dòng thiếu (ISP Goal: kỳ · hd Classifying/MID/Final · pay_type · cdt1).
# ⛔ thêm `svc_*` · `id_payee` · `invoice`: ngoài Goal, và `id_payee`/`invoice` là đối tác/số hoá đơn.
THUOC_TINH = ("ky",
              "hd_classifying", "hd_mid", "hd_final",
              "pay_type_classifying", "pay_type_mid", "pay_type_final",
              "cdt1_classifying", "cdt1_mid", "cdt1_final")
# Bảng đếm thuộc-tính × kỳ in ra màn và ghi vào JSON (BG-081 dán bảng này).
THUOC_TINH_THEO_KY = ("hd_classifying", "hd_final", "pay_type_final", "cdt1_final")

# ── MONG — phép đo TAY độc lập của orchestrator 16/11 (`WO-080` · ISP Step 3 · Estimate) ──────────────
MONG = {
    "so_dong_so": 9967,        # dòng sổ AS-IS · = do_voi_so_luong MONG so_dong_so
    "so_ky": 23,               #               · = do_voi_so_luong MONG so_ky
    "so_dong_ghep": 9845,      # dòng sổ ghép 1-1 · = do_voi_so_luong MONG so_dong_ghep_canon
    "so_dong_canon": 9992,     # dòng FLS dựng lại · = do_voi_so_luong MONG so_dong_bank
    "thieu": 122,              # = 9.967 − 9.845
    "nguoc": 147,              # = 9.992 − 9.845
    # orchestrator ghi 6 kỳ đầu + "…" và "18/23 kỳ"; 12 kỳ sau DT1a đo 16/11 (tổng 122, đúng 18 kỳ).
    "phan_bo_ky_thieu": {
        "2026-07": 23, "2025-11": 14, "2026-08": 13, "2026-06": 12, "2025-10": 9, "2026-04": 8,
        "2025-12": 5, "2026-02": 5, "2026-03": 5, "2026-05": 5, "2025-07": 4, "2025-08": 4,
        "2025-09": 4, "2026-01": 4, "2025-06": 3, "2025-02": 2, "2025-01": 1, "2025-05": 1,
    },
    "hd_classifying": {KHONG_TRA_LOI: 121, "GI | Gross Inflow": 1},       # 121/122 máy ⛔ trả lời
    # OGA 74 · GI 25 · DEP 8 · ITE 7 (orchestrator); "khác 8" tách bởi DT1a 16/11.
    "hd_final": {"OGA | GAC - Other": 74, "GI | Gross Inflow": 25, "DEP | Deposit": 8,
                 "ITE | ITE Interest": 7, "NB | Lưu chuyển nội bộ": 2,
                 "OMC | Online Marketing Cost": 2, "LC | License Cost": 2,
                 "LMN | Loan/Borrowing": 1, "BON | Bonus": 1},
    "pay_type_final": {"Thanh toán (Regular)": 71, "Thu tiền": 51},
    # sha256 (16 ký tự đầu) của danh sách số dòng đã sắp — ghim lần chạy đầu 16/11 (xem docstring).
    "van_tay": {"thieu": "18047e0eb0319ea1", "nguoc": "6ac2463a190ff631"},
}

KHOA_CAM = ("diengiai", "sochungtu", "email")   # so trên tên khoá đã bỏ dấu, thường hoá, bỏ ký tự lạ
MAU_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
MAU_REF_TRONG_LOI = "Did not find value"         # `#N/A (Did not find value 'FT…' …)` nhúng mã giao dịch


def _nap(thu_muc: Path, ten: str) -> dict:
    return json.loads((thu_muc / ten).read_text(encoding="utf-8"))


def _van_tay(so_dong: list[int]) -> str:
    return hashlib.sha256(json.dumps(so_dong, separators=(",", ":")).encode()).hexdigest()[:16]


def _so(n: int) -> str:
    """Số kiểu Việt: 9967 → `9.967`."""
    return f"{n:,}".replace(",", ".")


def _ty_le(tu: int, mau: int) -> str:
    return f"{tu * 100 / mau:.2f}".replace(".", ",") + " %"


def _phan_bo(gia_tri) -> list[list]:
    """Đếm → danh sách `[giá trị, số dòng]` (nhiều trước). ⛔ dict: giá trị `None` ⛔ làm khoá JSON được."""
    return [[v, n] for v, n in sorted(Counter(gia_tri).items(),
                                      key=lambda x: (-x[1], "" if x[0] is None else str(x[0])))]


def _bo_dau(s: str) -> str:
    s = unicodedata.normalize("NFD", s.replace("đ", "d").replace("Đ", "D"))
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if not unicodedata.combining(c)).lower())


def kiem_rieng_tu(d) -> list[str]:
    """Mọi vi phạm riêng tư trong `d`: khoá mang tên cấm · giá trị là email · ô lỗi nhúng mã giao dịch."""
    vi_pham: list[str] = []

    def di(x, duong: str) -> None:
        if isinstance(x, dict):
            for k, v in x.items():
                if any(c in _bo_dau(str(k)) for c in KHOA_CAM):
                    vi_pham.append(f"riêng tư: khoá cấm {duong}/{k}")
                di(v, f"{duong}/{k}")
        elif isinstance(x, list):
            for i, v in enumerate(x):
                di(v, f"{duong}[{i}]")
        elif isinstance(x, str):
            if MAU_EMAIL.search(x):
                vi_pham.append(f"riêng tư: email ở {duong}")
            if MAU_REF_TRONG_LOI in x:
                vi_pham.append(f"riêng tư: ô lỗi nhúng mã giao dịch ở {duong}")

    di(d, "")
    return vi_pham


def do(thu_muc: Path = FX) -> tuple[dict, list[str]]:
    """Đo trên ba ảnh ở `thu_muc` → (nội dung JSON, danh sách lệch MONG). Ảnh ⛔ đọc được ⇒ ngoại lệ."""
    loi: list[str] = []

    def kiem(ten: str, co, mong) -> None:
        if co != mong:
            loi.append(f"{ten}: đo {co!r} · mong {mong!r}")

    g, c, p = _nap(thu_muc, ANH_SO), _nap(thu_muc, ANH_GHEP), _nap(thu_muc, ANH_PM)
    ck = MONG_VOI["checksum"]
    kiem("checksum itl_ledge_adjustment (tính lại)", _sha(g["dong"], g["bang_gia_tri"]), ck[ANH_SO])
    kiem("checksum classifying_vs_canon (trường đã ghim)", c["checksum_noi_dung"], ck[ANH_GHEP])
    kiem("checksum pm_join (trường đã ghim)", p["checksum_noi_dung"], ck[ANH_PM])

    # ① sổ AS-IS: dong_sheet → thuộc tính
    idx = {t: i for i, t in enumerate(g["cot"])}
    bang = g["bang_gia_tri"]
    so: dict[int, dict] = {}
    for h in g["dong"]:
        o = {"ky": h[idx["ky"]]}
        for t in THUOC_TINH[1:]:
            i = h[idx[t]]
            o[t] = None if i == -1 else bang[i]
        so[h[idx["dong_sheet"]]] = o
    kiem("dong_sheet ⛔ trùng (số dòng ảnh sổ ↔ số dong_sheet khác nhau)", len(so), len(g["dong"]))

    # ② ghép 1-1 sổ ↔ FLS
    i_so, i_canon = c["cot"].index("dong_so"), c["cot"].index("dong_canon")
    ds_so = [r[i_so] for r in c["dong"]]
    ds_canon = [r[i_canon] for r in c["dong"]]
    ghep, ghep_canon = set(ds_so), set(ds_canon)
    kiem("dong_so ⛔ trùng (dòng ghép ↔ dong_so khác nhau)", len(ghep), len(ds_so))
    kiem("dong_canon ⛔ trùng (dòng ghép ↔ dong_canon khác nhau)", len(ghep_canon), len(ds_canon))
    # Trường KHAI của ảnh ghép ↔ số ĐẾM được (Đ2 — hai nguồn; ⛔ so một nguồn với chính nó)
    kiem("số dòng sổ: trường so_dong_so của ảnh ghép ↔ đếm ảnh sổ", c["so_dong_so"], len(so))
    kiem("số dòng ghép: trường so_dong_ghep của ảnh ↔ đếm", c["so_dong_ghep"], len(ghep))
    kiem("dòng ghép trỏ dòng sổ ⛔ có trong ảnh sổ", len(ghep - set(so)), 0)

    # ③ dòng FLS dựng lại (bank của pm_join) — `so_dong_canon` của ảnh ghép là HAI NGUỒN cho cùng số
    bank = {b["dong"] for b in p["bank"]}
    kiem("số dòng canon: trường so_dong_canon của ảnh ghép ↔ dòng bank pm_join", c["so_dong_canon"], len(bank))
    kiem("dong_canon đã ghép ⛔ thuộc bank pm_join", len(ghep_canon - bank), 0)

    mau_so = {"so_dong_so": len(so), "so_dong_ghep": len(ghep), "so_dong_canon": len(bank)}
    if 0 in mau_so.values():                    # Đ3 — mẫu số rỗng là KẾT QUẢ, ⛔ nền cho tỷ lệ
        loi.append(f"mẫu số = 0 — ⛔ đo được tỷ lệ nào (Đ3): {mau_so}")
        return {"mau_so": mau_so}, loi
    kiem("số dòng sổ", mau_so["so_dong_so"], MONG["so_dong_so"])
    cac_ky = sorted({o["ky"] for o in so.values()})
    kiem("số kỳ", len(cac_ky), MONG["so_ky"])
    kiem("số dòng ghép", mau_so["so_dong_ghep"], MONG["so_dong_ghep"])
    kiem("số dòng canon", mau_so["so_dong_canon"], MONG["so_dong_canon"])

    # ④ hai tập — mỗi tập đếm HAI cách (hiệu số ↔ tập liệt kê)
    thieu = sorted(set(so) - ghep)
    nguoc = sorted(bank - ghep_canon)
    kiem("dòng sổ ⛔ ghép (sổ ∖ ghép)", len(thieu), MONG["thieu"])
    kiem("dòng sổ ⛔ ghép: hiệu trường khai so_dong_so − so_dong_ghep ↔ tập liệt kê",
         c["so_dong_so"] - c["so_dong_ghep"], len(thieu))
    kiem("dòng FLS ⛔ có dòng sổ (canon ∖ ghép)", len(nguoc), MONG["nguoc"])
    kiem("dòng FLS ⛔ có dòng sổ: hiệu trường khai so_dong_canon − so_dong_ghep ↔ tập liệt kê",
         c["so_dong_canon"] - c["so_dong_ghep"], len(nguoc))

    dong_thieu = [{"dong_sheet": d, **so[d], "nhan": None} for d in thieu]
    dong_nguoc = [{"dong_canon": d, "nhan": None} for d in nguoc]
    phan_bo_ky = Counter(o["ky"] for o in dong_thieu)
    kiem("phân bố kỳ của dòng thiếu", dict(phan_bo_ky), MONG["phan_bo_ky_thieu"])
    for t in ("hd_classifying", "hd_final", "pay_type_final"):
        kiem(f"phân bố {t} của dòng thiếu", dict(Counter(o[t] for o in dong_thieu)), MONG[t])
    van_tay = {"thieu": _van_tay(thieu), "nguoc": _van_tay(nguoc)}
    kiem(f"vân tay tập thiếu (sha256 của {len(thieu)} dong_sheet đã sắp)", van_tay["thieu"], MONG["van_tay"]["thieu"])
    kiem(f"vân tay tập ngược (sha256 của {len(nguoc)} dong_canon đã sắp)", van_tay["nguoc"], MONG["van_tay"]["nguoc"])

    kq = {
        "_vi_sao": ("Sinh bởi `python tools/phan_loai_dong_thieu.py --ghi` từ ba ảnh đóng băng tests/fixture/ "
                    "(ISP 3.1.2 Step 3 · DT1a · WO-080). ⛔ sửa tay — bài tests/du_lieu/test_phan_loai_dong_thieu.py "
                    "đòi tệp này BẰNG lần đo hiện tại. `nhan` = null: LÝ DO là việc của DT1b."),
        "khong_mang_PII": "⛔ Diễn giải · Số chứng từ · Tài khoản · tiền · email — chỉ số dòng, kỳ và 9 ô phân loại.",
        "nguon": {"so": g["nguon"], "so_dong_bang": g["ngay_dong_bang"], "ghep": c["nguon"],
                  "bank": p["nguon"], "checksum": dict(ck)},
        "mau_so": mau_so,
        "dem": {"thieu": len(thieu), "nguoc": len(nguoc), "so_ky": len(cac_ky),
                "so_ky_co_thieu": len(phan_bo_ky)},
        "theo_ky": {k: {"so_dong_so": sum(1 for o in so.values() if o["ky"] == k),
                        "thieu": phan_bo_ky.get(k, 0)} for k in cac_ky},
        "phan_bo_thuoc_tinh": {t: _phan_bo(o[t] for o in dong_thieu) for t in THUOC_TINH[1:]},
        "thuoc_tinh_theo_ky": {t: {k: _phan_bo(o[t] for o in dong_thieu if o["ky"] == k)
                                   for k in cac_ky if phan_bo_ky.get(k)} for t in THUOC_TINH_THEO_KY},
        "van_tay": van_tay,
        "dong_thieu": dong_thieu,
        "dong_nguoc": dong_nguoc,
    }
    loi.extend(kiem_rieng_tu(kq))                # chặn TRƯỚC khi ghi — lệch ⇒ ĐỎ như mọi phép so
    return kq, loi


def in_bao_cao(kq: dict, thu_muc: Path) -> None:
    ms = kq["mau_so"]
    try:
        noi = thu_muc.resolve().relative_to(GOC)
    except ValueError:
        noi = thu_muc
    print(f"PHÂN LOẠI DÒNG THIẾU — HD1 · ba ảnh ở {noi}")
    # Đ3: MẪU SỐ in TRƯỚC mọi tỷ lệ, mỗi số mang nhãn NÓ ĐẾM GÌ (Đ4)
    print(f"① MẪU SỐ: sổ AS-IS {_so(ms['so_dong_so'])} dòng sổ · ghép 1-1 {_so(ms['so_dong_ghep'])} dòng ghép · "
          f"FLS dựng lại {_so(ms['so_dong_canon'])} dòng canon")
    if "dem" not in kq:
        return
    d = kq["dem"]
    print(f"② dòng sổ ⛔ ghép: {_so(d['thieu'])} / {_so(ms['so_dong_so'])} dòng sổ = "
          f"{_ty_le(d['thieu'], ms['so_dong_so'])} · rải {d['so_ky_co_thieu']}/{d['so_ky']} kỳ "
          f"· hiệu {_so(ms['so_dong_so'])} − {_so(ms['so_dong_ghep'])}")
    print(f"③ dòng FLS ⛔ có dòng sổ: {_so(d['nguoc'])} / {_so(ms['so_dong_canon'])} dòng canon = "
          f"{_ty_le(d['nguoc'], ms['so_dong_canon'])} · hiệu {_so(ms['so_dong_canon'])} − {_so(ms['so_dong_ghep'])}")
    print(f"④ thuộc tính của {_so(d['thieu'])} dòng thiếu (đếm DÒNG):")
    for t, pb in kq["phan_bo_thuoc_tinh"].items():
        print(f"   {t:22s} " + " · ".join(f"{'∅' if v is None else v} {n}" for v, n in pb))
    print("⑤ theo kỳ (đếm DÒNG; % = thiếu / dòng sổ của kỳ):")
    print(f"   {'kỳ':8s} {'sổ':>5s} {'thiếu':>6s} {'%':>8s}  hd_final · pay_type_final")
    for k, x in kq["theo_ky"].items():
        hd = kq["thuoc_tinh_theo_ky"]["hd_final"].get(k, [])
        pt = kq["thuoc_tinh_theo_ky"]["pay_type_final"].get(k, [])
        chi_tiet = " · ".join(f"{v} {n}" for v, n in hd)
        if pt:
            chi_tiet += "  ‖  " + " · ".join(f"{v} {n}" for v, n in pt)
        print(f"   {k:8s} {x['so_dong_so']:5d} {x['thieu']:6d} {_ty_le(x['thieu'], x['so_dong_so']):>8s}  {chi_tiet}")
    print(f"   vân tay: thiếu {kq['van_tay']['thieu']} · ngược {kq['van_tay']['nguoc']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="HD1 · kiểm kê dòng sổ AS-IS chưa ghép 1-1 (DT1a).")
    ap.add_argument("--ghi", action="store_true", help=f"ghi {RA.relative_to(GOC)} (chỉ từ ảnh thật)")
    ap.add_argument("--thu-muc", type=Path, default=None,
                    help="đo trên bản SAO ba ảnh ở thư mục này (chứng minh ĐỎ) — ⛔ dùng cùng --ghi")
    a = ap.parse_args(argv)
    if a.ghi and a.thu_muc is not None:
        print(f"⛔ TỪ CHỐI: --ghi chỉ ghi từ ảnh thật {FX.relative_to(GOC)}/ — ⛔ ghi hiện vật từ bản sao (--thu-muc)",
              file=sys.stderr)
        return 2
    thu_muc = a.thu_muc if a.thu_muc is not None else FX
    try:
        kq, loi = do(thu_muc)
    except Exception as e:                        # Đ5: ⛔ đo được là ĐỎ — nguyên nhân MỘT dòng (S0-R1-04)
        print(f"LOI {type(e).__name__}: " + " ".join(str(e).split()), file=sys.stderr)
        return 1
    in_bao_cao(kq, thu_muc)
    if loi:
        print(f"⛔ PHÂN LOẠI DÒNG THIẾU ĐỎ — {len(loi)} chỗ khác MONG (⛔ ghi JSON):", file=sys.stderr)
        for x in loi:
            print("  " + x, file=sys.stderr)
        return 1
    print(f"KẾT: ĐẠT — mọi phép so khớp MONG · {_so(kq['dem']['thieu'])} dòng thiếu + "
          f"{_so(kq['dem']['nguoc'])} dòng ngược · nhan = null (DT1b điền)")
    if a.ghi:
        RA.write_text(json.dumps(kq, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"✅ đã ghi {RA.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
