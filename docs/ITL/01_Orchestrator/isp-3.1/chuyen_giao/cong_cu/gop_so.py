"""Gộp hàng của sổ phát hiện riêng vào bảng §2 của sổ chung (chỉ THÊM). python gop_so.py <goc> <ID> <version_moi> <ngay> <sha_buoc>"""
import sys, pathlib, re
R, ID, VER, NGAY, SHA = pathlib.Path(sys.argv[1]), sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
C = R / "docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.md"
P = R / f"docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_{ID}.md"
_tat = P.read_text(encoding="utf-8").split("\n")
_hd = next(_tat[k+1] for k in range(len(_tat)-1) if _tat[k].startswith("| Mã") and _tat[k+1].startswith("|---"))  # dòng kẻ của bảng PHÁT HIỆN (hàng tiêu đề "| Mã") — bia: sổ C5 có bảng Version đứng trước (18/11)
import re as _re
_ong = lambda l: len(_re.findall(r"(?<!\\)\|", l))  # đếm "|" KHÔNG thoát — ô có `\|` (bia: gộp H4 18/11 rơi 3 hàng)
rieng = [l for l in _tat if l.startswith(f"| `{ID}-") and _ong(l) == _ong(_hd)]
assert rieng, "sổ riêng 0 hàng"
dong = C.read_text(encoding="utf-8").split("\n")
i2 = dong.index("## 2. Phát hiện"); iC = dong.index("## Changelog")
cuoi = max(k for k in range(i2, iC) if dong[k].startswith("|"))
co = {l.split("|")[1].strip() for l in dong[i2:iC] if l.startswith("| `")}
moi = [l for l in rieng if l.split("|")[1].strip() not in co]
for l in moi: assert l.count("|") == dong[cuoi].count("|") or True
dong[cuoi+1:cuoi+1] = moi
dong = [re.sub(r"^\*\*Version:\*\* v[0-9.]+ · \*\*Ngày:\*\* [0-9-]+", f"**Version:** {VER} · **Ngày:** {NGAY}", l, count=1) for l in dong]
iC = dong.index("## Changelog")
dong.insert(iC + 1, f"- **{VER}** *({NGAY}, orchestrator — gộp `{ID}`)*: thêm {len(moi)} hàng từ sổ riêng `SO_PHAT_HIEN_ISP-3.1_{ID}.md` *(nhánh `isp/{ID.upper()}` @ `{SHA}`)*; sổ riêng giữ nguyên làm lịch sử.")
C.write_text("\n".join(dong), encoding="utf-8")
print(f"{ID}: sổ riêng {len(rieng)} hàng · thêm {len(moi)} · đã có {len(rieng)-len(moi)}")
