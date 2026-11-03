# -*- coding: utf-8 -*-
"""`P7` task `7` — bước ĐO. **⛔ Công cụ này ⛔ KHÔNG GHI gì cả.**

⭐⭐ **Vì sao phải đo TRƯỚC KHI nạp.** Bảng `fls_source` là **gốc** của mọi bản
   khai ánh xạ cột: mỗi bản khai treo vào một `source_id`. Nạp một danh sách
   nguồn **chưa ai kiểm** là đóng đinh sai số ấy vào **đúng cái bảng làm gốc**,
   rồi mọi thứ dựng lên trên đều lệch theo mà ⛔ không ai lần ra được.

⛔⛔ **Và ta ĐÃ BIẾT danh mục có khuyết tật thật** *(`GAP-KT-01..04`, đo 07/09)*:
   **2/52** tài khoản `Active` khai một tên sheet ⛔ **không tồn tại** *(và hoá
   ra là **lỗi gõ THỪA MỘT KÝ TỰ** — `1` và `7`)*, **5** dòng đánh `Active` mà
   ⛔ **không có tên tài khoản**. ⇒ Chép thẳng danh mục vào kho là chép cả
   khuyết tật, và từ đó chúng **thành sự thật của hệ mới**.

★ **Ba câu hỏi, và ⛔ KHÔNG câu nào trả lời được từ MỘT phía:**

  ⓵ Danh mục khai sheet nào? *(danh mục → sheet)*
  ⓶ Thực tế có sheet nào? *(sheet → danh mục)*
  ⓷ Sheet nào **khai đủ 6 trường** ở dòng 1? *(cái ta thật sự chép được)*

  ⭐ Bài học 07/09, ghi thẳng vào đây để ⛔ không lặp: **một chiều đủ để BÁO,
    ⛔ không đủ để KẾT LUẬN**. Cổng `L9` hỏi chiều ⓵ và kết luận *"2 tài khoản
    ⛔ không có sheet"*; hỏi thêm chiều ⓶ mới lòi ra *"2 sheet **có thật** mà
    danh mục ⛔ không biết"* — và ghép cặp gần-giống thì thấy **⛔ KHÔNG thiếu
    sheet nào**, chỉ là hai lỗi gõ.

⛔ **`QĐ-ITL-92`:** chỉ đọc **tên sheet · dòng 1 · cột trạng thái**. ⛔ Không
  đọc `Description`, ⛔ không in nội dung ô dữ liệu nào.

Chạy:  PYTHONUTF8=1 ./.venv/Scripts/python.exe tools/do_danh_muc_nguon.py
"""
from __future__ import annotations

import difflib
import sys

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

from fls.adapters.sao_ke import SAU_TRUONG, doc_ban_khai  # noqa: E402
from tools.do_bat_bien_ngam import BANK, QUY, cot  # noqa: E402
from tools.do_hinh_dang import dong_dau, meta, token  # noqa: E402

# Hai danh mục, đọc theo **đúng bản khai cột của cổng #17** — ⛔ không gõ lại
# một bộ chỉ số thứ hai (`tools/kiem_nguon_song.py` §nguồn 3).
DANH_MUC = (
    ("BNK", BANK, "BankAccountList", 3, 18),
    ("CSH", QUY, "Cash Ledger List", 1, 18),
)
GIONG = 0.90            # ngưỡng ghép cặp gần-giống


def _o(c, k):
    return c[k] if k < len(c) else ""


def doc_danh_muc(sid: str, sheet: str, i_ten: int, i_tt: int, tok: str):
    """→ `{nhãn: (tên sheet khai, trạng thái)}`.

    ⛔⛔ Nhãn mang **SỐ DÒNG**, ⛔ không phải tên. Tên thì **có trùng và có
    rỗng** ⇒ khoá bằng tên là để dict **âm thầm nuốt dòng** — đã hỏng thật:
    `L8-CSH` báo **9** tài khoản `Active` trong khi đo thẳng ra **19**.
    """
    v = cot(sid, "'%s'!A3:V" % sheet, tok, "UNFORMATTED_VALUE")
    ten_c = v[i_ten] if i_ten < len(v) else []
    tt_c = v[i_tt] if i_tt < len(v) else []
    n = len([x for x in ten_c if str(x).strip()])
    return {"#%d" % (k + 3): (str(_o(ten_c, k)).strip(),
                              str(_o(tt_c, k)).strip())
            for k in range(n)}


def ten_r(sid: str, tok: str) -> set[str]:
    return {s["properties"]["title"] for s in meta(sid, tok)["sheets"]
            if s["properties"]["title"].startswith("R |")}


def ghep_gan_giong(thieu: set[str], thua: set[str]):
    """Ghép các cặp **gần giống** giữa hai phía → `[(khai, thật, độ giống)]`.

    ⭐ Đây là bước biến *"2 tài khoản mất sheet"* + *"2 sheet vô chủ"* thành
      *"**2 lỗi gõ**"* — một câu **khác hẳn**, và dẫn tới một việc sửa **khác
      hẳn** *(sửa một ký tự trong danh mục, ⛔ không phải dựng 2 sheet mới)*.
    """
    cap = []
    for a in sorted(thieu):
        b = difflib.get_close_matches(a, sorted(thua), n=1, cutoff=GIONG)
        if b:
            cap.append((a, b[0],
                        difflib.SequenceMatcher(None, a, b[0]).ratio()))
    return cap


def main() -> int:
    tok = token()
    print("=" * 78)
    print("ĐO DANH MỤC NGUỒN — `P7` task 7 · ⛔ KHÔNG GHI GÌ")
    print("=" * 78)

    tong = {"tk": 0, "active": 0, "khong_ten": 0, "co_sheet": 0,
            "khai_du": 0, "sheet_vo_chu": 0, "loi_go": 0,
            "dong": 0, "vo_chu_that": 0, "chung_sheet": 0}

    for ma, sid, sheet, i_ten, i_tt in DANH_MUC:
        dm = doc_danh_muc(sid, sheet, i_ten, i_tt, tok)
        that = ten_r(sid, tok)

        active = {k: v for k, v in dm.items() if v[1].lower() == "active"}
        khong_ten = [k for k, v in active.items() if not v[0]]
        khai = {k: v[0] for k, v in active.items() if v[0]}

        # ⓵ danh mục → sheet   ·   ⓶ sheet → danh mục
        thieu = {t for t in khai.values() if t not in that}
        thua = that - set(khai.values())
        cap = ghep_gan_giong(thieu, thua)

        # ⓷ sheet nào khai ĐỦ 6 trường ở dòng 1 — cái ta THẬT SỰ chép được
        hdr = dong_dau(sid, sorted(that), tok, n=1)
        du, thieu_khai = {}, {}
        for s in sorted(that):
            k = doc_ban_khai(hdr.get(s, [[]])[0] if hdr.get(s) else [])
            (du if len(k) == len(SAU_TRUONG) else thieu_khai)[s] = k

        print("\n── %s · `%s` ──────────────────────────────" % (ma, sheet))
        print("  dòng có tên tài khoản      : %3d" % len(dm))
        print("  trong đó `Active`          : %3d" % len(active))
        print("  ⛔ `Active` mà KHÔNG có tên : %3d %s"
              % (len(khong_ten), sorted(khong_ten) if khong_ten else ""))
        print("  sheet `R |` CÓ THẬT        : %3d" % len(that))
        print("  ⛔ danh mục khai mà ko có   : %3d %s"
              % (len(thieu), sorted(thieu) if thieu else ""))
        print("  ⛔ sheet có mà danh mục ko  : %3d %s"
              % (len(thua), sorted(thua) if thua else ""))
        if cap:
            print("  ⭐ GHÉP CẶP gần giống — tức LỖI GÕ, ⛔ không phải thiếu sheet:")
            for a, b, r in cap:
                print("       khai `%s`\n       thật `%s`   (giống %.1f%%)"
                      % (a, b, r * 100))
        print("  ⭐ sheet khai ĐỦ 6 trường   : %3d/%d" % (len(du), len(that)))
        if thieu_khai:
            for s, k in sorted(thieu_khai.items()):
                print("     ⛔ %s — thiếu %s"
                      % (s, sorted(set(SAU_TRUONG) - set(k))))

        # ── ⓸ ⭐⭐ HAI câu hỏi mà ba phép trên ⛔ KHÔNG trả lời được ─────────
        #
        # ⛔⛔ Chúng quyết định **`fls_source` một dòng là CÁI GÌ**, nên ⛔ không
        # được đoán:
        #
        #   ⓐ *"Sheet có mà danh mục ⛔ không biết"* ở trên chỉ so với dòng
        #      **`Active`**. Một sheet của **tài khoản ĐÃ ĐÓNG** sẽ rơi vào đó
        #      và trông y như một sheet **vô chủ** — hai thứ hoàn toàn khác
        #      nhau: một cái là **lịch sử hợp lệ**, một cái là **lỗ hổng**.
        #   ⓑ **Hai tài khoản có cùng trỏ vào MỘT sheet ⛔ không?** Nếu có thì
        #      *"nguồn"* ⛔ **không** một-đối-một với *"tài khoản"*, và cả khuôn
        #      `fls_source` ↔ `fls_khai_cot` phải hiểu khác đi.
        theo_sheet: dict[str, list[str]] = {}
        for k, (t, tt) in dm.items():
            if t:
                theo_sheet.setdefault(t, []).append("%s%s" % (
                    k, "" if tt.lower() == "active" else "(%s)" % (tt or "∅")))

        chung = {s: r for s, r in theo_sheet.items() if len(r) > 1}
        chi_dong = sorted(s for s in that
                          if s in theo_sheet
                          and not any("(" not in r for r in theo_sheet[s]))
        vo_chu = sorted(s for s in that if s not in theo_sheet)

        print("  ⓐ sheet của tài khoản ĐÃ ĐÓNG (lịch sử hợp lệ) : %3d %s"
              % (len(chi_dong), chi_dong if chi_dong else ""))
        print("  ⛔ⓐ sheet ⛔ KHÔNG dòng danh mục nào trỏ tới     : %3d %s"
              % (len(vo_chu), vo_chu if vo_chu else ""))
        print("  ⓑ sheet bị NHIỀU dòng danh mục cùng trỏ tới    : %3d"
              % len(chung))
        for s, r in sorted(chung.items()):
            print("       %s  ←  %s" % (s, ", ".join(sorted(r))))
        tong["dong"] += len(chi_dong)
        tong["vo_chu_that"] += len(vo_chu)
        tong["chung_sheet"] += len(chung)

        tong["tk"] += len(dm)
        tong["active"] += len(active)
        tong["khong_ten"] += len(khong_ten)
        tong["co_sheet"] += len(khai) - len(thieu)
        tong["khai_du"] += len(du)
        tong["sheet_vo_chu"] += len(thua)
        tong["loi_go"] += len(cap)

    print("\n" + "=" * 78)
    print("TỔNG — và đây là những con số quyết định `fls_source` chứa GÌ")
    print("=" * 78)
    for k, nhan in (("tk", "dòng danh mục có tên"),
                    ("active", "`Active`"),
                    ("khong_ten", "⛔ `Active` mà KHÔNG có tên tài khoản"),
                    ("co_sheet", "`Active` + có sheet thật"),
                    ("khai_du", "sheet khai ĐỦ 6 trường (chép được ngay)"),
                    ("sheet_vo_chu", "⛔ sheet có thật mà danh mục không biết"),
                    ("loi_go", "⭐ trong đó ghép được thành LỖI GÕ"),
                    ("dong", "sheet của tài khoản ĐÃ ĐÓNG (hợp lệ)"),
                    ("vo_chu_that", "⛔ sheet KHÔNG dòng danh mục nào trỏ tới"),
                    ("chung_sheet", "⛔ sheet bị NHIỀU dòng cùng trỏ tới")):
        print("  %-45s : %3d" % (nhan, tong[k]))

    print("\n⛔ ⛔ KHÔNG nạp gì cả — đây là bước ĐO. Quyết định `fls_source`")
    print("   chứa gì là việc của owner, ⛔ không phải của công cụ này.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
