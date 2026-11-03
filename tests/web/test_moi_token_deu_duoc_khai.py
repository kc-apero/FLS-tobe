# -*- coding: utf-8 -*-
"""⛔ Cong: moi `var(--x)` duoc DUNG thi phai co ai do KHAI `--x`.

⛔⛔ **Bai nay sinh ra vi mot loi CO SAN, tim thay `22/09`.** `--accent-soft`
   duoc dung o **ba** cho trong `hinh.css` va **⛔ CHUA BAO GIO duoc khai**:

     · `@keyframes soi`                  — hieu ung soi mot dong chay tu
                                           *trong suot* sang *trong suot*
                                           ⇒ **⛔ khong thay gi**
     · `@media (prefers-reduced-motion)` — nguoi TAT chuyen dong dang le nhan
                                           mot **nen tinh** thay animation;
                                           ho nhan **⛔ khong gi ca**
     · `.gapfold:hover`                  — hover ⛔ khong doi nen

⭐⭐ **Vi sao ⛔ khong cong nao bat duoc.** `test_khong_ma_mau_go_tay` canh
   *"co hex NGOAI `tokens.css` ⛔ khong"* — mot cau hoi **dung**, nhung no chi
   canh **mot chieu**. Chieu con lai — *"mot ten token co that ⛔ khong"* — thi
   ⛔ khong ai hoi. Va CSS **⛔ khong bao gio bao loi**: mot `var(--khong-co)`
   chi lang le ⛔ khong ap gi, y het nhu ⛔ chua ai viet dong ay.

⇒ Cung mot ho voi bai hoc `tailwind-class-typo-passes-tsc`: **canh cai CHAY
  ra, ⛔ dung canh cai GO vao**.
"""
from __future__ import annotations

import os
import re

from fls.web import phuc_vu as pv

# ⭐⭐ Dung **lai** phep bo ghi chu cua cong mau, ⛔ KHONG viet ban thu hai.
#
# ⛔⛔ Lan chay dau, bai nay **DO** — va bao dong la mot **dong ghi chu tôi vua
#    go trong `tokens.css`**, cau van ta chinh cai cong nay *(`"moi var(--x)
#    co ai khai khong"`)*. Do la lan thu **BA** cung mot bai hoc trong hai
#    ngay: `test_chieu_KHONG_duoc_suy_tu_pay_type` quet `getsource()` va bat
#    khoi chu thich canh bao ve loi; phep quet mau rieng cua toi bat `#f01-ghep`.
#
# ⭐ Va cong mau **da co san** `_bo_ghi_chu` — giu so dong y nguyen de toa do
#   bao loi con dung. Viet mot ban thu hai la tao **hai dinh nghia** ve *"the
#   nao la mot ghi chu"*, va ban moi hon thi **dot hon**.
from tests.web.test_khong_ma_mau_go_tay import _bo_ghi_chu

DUNG = re.compile(r"var\(\s*(--[A-Za-z0-9_-]+)")
KHAI = re.compile(r"(--[A-Za-z0-9_-]+)\s*:")

#: ⭐ Token dat **inline theo dong** *(hop dong thiet ke §3)* — no ⛔ khong
#: song o `tokens.css` vi moi dong mot gia tri. Ban TRANG: them mot ten vao
#: day la khai rang *"cho nay CO Y ⛔ khong co gia tri mac dinh"*.
DAT_INLINE: frozenset[str] = frozenset()


def _doc(ten: str) -> str:
    with open(os.path.join(pv.THU_MUC, ten), encoding="utf-8") as f:
        return _bo_ghi_chu(f.read())


def _khai_o_tokens() -> set[str]:
    return set(KHAI.findall(_doc("tokens.css")))


def test_moi_token_duoc_dung_deu_co_noi_khai():
    khai = _khai_o_tokens() | DAT_INLINE
    thieu: list[str] = []
    for ten in sorted(os.listdir(pv.THU_MUC)):
        if not ten.endswith((".css", ".js", ".html")):
            continue
        chu = _doc(ten)
        # ⭐ Token khai NGAY TRONG tep ay *(nhu `table.g.lenh{--khoa-1:88px}`)*
        #   la hop le: bien CSS ke thua theo cay the, va `G5` co y dat lai
        #   `--khoa-1` tren chinh cai bang do.
        cho_nay = khai | set(KHAI.findall(chu))
        for m in DUNG.finditer(chu):
            if m.group(1) not in cho_nay:
                dong = chu[:m.start()].count("\n") + 1
                thieu.append(f"{ten}:{dong}  var({m.group(1)})")
    assert thieu == [], (
        "⛔ Ten token ⛔ KHONG duoc khai o dau — CSS se lang le ⛔ khong ap gi, "
        "va ⛔ khong mot loi nao hien ra:\n  " + "\n  ".join(thieu))


# ── ⛔⛔ PHA CO CHU DICH: cong phai DO ─────────────────────────────────────

def test_cong_DO_khi_co_token_ma(tmp_path):
    """⭐ Mot cong ⛔ chua bao gio thay mau do la mot cong ⛔ chua ai do."""
    khai = _khai_o_tokens()
    assert "--accent-soft" in khai, (
        "⛔ `--accent-soft` phai duoc khai — day dung la loi bai nay sinh ra "
        "de chan, va no da song **ba** cho trong `hinh.css`")
    gia = ".x{background:var(--chua-ai-khai-bao-gio)}"
    assert [m.group(1) for m in DUNG.finditer(gia)] == ["--chua-ai-khai-bao-gio"]
    assert "--chua-ai-khai-bao-gio" not in khai


def test_bon_token_MOI_cua_man_ghep_co_mat():
    """⭐ Delta that su cua ban giao thiet ke (`§3`) — ⛔ khong hon ⛔ khong kem.

    ⚠ Ban giao con doi ten mot loat token cu (`--font-sans`, `--radius-md`…).
      ⛔ **⛔ KHONG nhan** — kho da co `--sans`/`--mono`/`--bo-*` va **12** tep
      dung chung; doi ten la sua **toan he** ma ⛔ khong mua duoc mot pixel.
    """
    khai = _khai_o_tokens()
    for t in ("--hair", "--evi-bg", "--rail-w", "--shadow-card", "--row-ghep"):
        assert t in khai, f"⛔ thieu token `{t}` cua man ghep"
    for cu in ("--sans", "--mono", "--bo", "--bo-the"):
        assert cu in khai, f"⛔ ten CU `{cu}` bi doi — do la sua toan he"
    for doi_ten in ("--font-sans", "--radius-md", "--radius-pill"):
        assert doi_ten not in khai, (
            f"⛔ `{doi_ten}` la ten cua BAN GIAO — nhan no vao la co **hai** "
            f"ten cho cung mot thu, va chung se lech")
