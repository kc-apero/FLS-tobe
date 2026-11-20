"""Gộp một nhánh bước ISP 3.1.2 vào nhánh làm việc — phần MÁY của thủ tục gộp 11 bước.

Nguồn thủ tục: `docs/ITL/01_Orchestrator/isp-3.1/HANDOFF_ORCHESTRATOR_2026-11-19.md` §5.3.
Công cụ này làm bước **1–2 · 4–7 · 9**; bước **3** (gỡ xung đột MÃ) · **8** (lật `07_API_CONTRACT` §4i)
· **10** (commit + `--duong-nen` ~25 phút) · **11** (hàng `TIEN_DO`) cần mắt người — công cụ IN ra
danh sách việc còn lại, ⛔ tự làm.

    python tools/gop_buoc_isp.py bat-dau <ID> [--nhanh-lam-viec claude/bold-galileo-zukpaf]
        bước 1–2: fetch nhánh bước, `git merge --no-ff --no-commit`. Còn xung đột NGOÀI hai tệp
        sàn ⇒ in danh sách, exit 2 — gỡ tay (bước 3) rồi chạy `tiep`.
    python tools/gop_buoc_isp.py tiep <ID> <ngày YYYY-MM-DD> [--cong 5433]
        bước 4–7 + 9: giữ bản `--ours` hai tệp sàn · đếm thu thập THẬT của cây gộp · đặt sàn +
        bài ghim + chú thích · gộp sổ phát hiện riêng (bump version) · chạy cổng giấy/tầng/tuyến/PII.

Luật đo (CLAUDE.md):
- Đ5: mỗi cổng khai `mong`; ⛔ đo được (pytest thu thập 0 bài, mẫu khớp 0 hoặc ≥ 2 lần) ⇒ ĐỎ.
- Đ4: sàn đếm **số bài thu thập** (`pytest --collect-only`, tổng các dòng `tests/…: n`) của CÂY GỘP
  sau khi đã hết dấu xung đột — ⛔ cộng tay số bài của nhánh bước (bia: 2–9 bài lệch, 19/11).
- Sửa tệp bằng Python đọc/ghi UTF-8 — ⛔ sed/heredoc qua hai lớp shell (bẫy `CLAUDE.md`).
"""
from __future__ import annotations

import argparse
import os
import pathlib
import re
import subprocess
import sys

GOC = pathlib.Path(__file__).resolve().parent.parent
SCRIPT = GOC / "tools/dung_moi_truong_isp.sh"
BAI_GHIM = GOC / "tests/test_dung_moi_truong_isp.py"
SO_CHUNG = GOC / "docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1.md"
GOP_SO = GOC / "docs/ITL/01_Orchestrator/isp-3.1/chuyen_giao/cong_cu/gop_so.py"
TIEN_TO_BUOC = "-isp/"
HAI_TEP_SAN = ("tools/dung_moi_truong_isp.sh", "tests/test_dung_moi_truong_isp.py")
PY = str(GOC / ".venv/bin/python") if (GOC / ".venv/bin/python").exists() else sys.executable


def chay(lenh: list[str], *, kiem: bool = True, **kw) -> subprocess.CompletedProcess:
    print("  $", " ".join(lenh), flush=True)
    kq = subprocess.run(lenh, cwd=GOC, text=True, capture_output=True, **kw)
    if kiem and kq.returncode != 0:
        sys.stderr.write(kq.stdout[-3000:] + kq.stderr[-3000:])
        raise SystemExit(f"ĐỎ: lệnh trả {kq.returncode}")
    return kq


def xung_dot() -> list[str]:
    kq = chay(["git", "diff", "--name-only", "--diff-filter=U"], kiem=False)
    return [d for d in kq.stdout.splitlines() if d.strip()]


def bat_dau(a: argparse.Namespace) -> int:
    id_ = a.id
    nhanh = f"{a.nhanh_lam_viec}{TIEN_TO_BUOC}{id_}"
    if chay(["git", "status", "--porcelain", "--untracked-files=no"]).stdout.strip():
        raise SystemExit("ĐỎ: cây làm việc bẩn — commit/stash trước khi gộp")
    if chay(["git", "rev-parse", "--abbrev-ref", "HEAD"]).stdout.strip() != a.nhanh_lam_viec:
        raise SystemExit(f"ĐỎ: HEAD không ở {a.nhanh_lam_viec}")
    chay(["git", "fetch", "origin", f"refs/heads/{nhanh}"])                       # bước 1
    chay(["git", "branch", "-f", f"isp/{id_}", "FETCH_HEAD"])
    sha = chay(["git", "rev-parse", "--short", f"isp/{id_}"]).stdout.strip()
    print(f"── isp/{id_} @ {sha}")
    kq = chay(["git", "merge", "--no-ff", "--no-commit", f"isp/{id_}"], kiem=False)  # bước 2
    print(kq.stdout[-1500:])
    con = [t for t in xung_dot() if t not in HAI_TEP_SAN]
    if con:
        print("── BƯỚC 3 (tay): gỡ xung đột MÃ — giữ CẢ HAI khi hai bước thêm khối song song "
              "(`hd2_cong.json` · `do_hd2.py` · `cau_hinh_repo.py` · changelog `07_API_CONTRACT`):")
        for t in con:
            print("   ·", t)
        print(f"   rồi `git add` từng tệp và chạy: python tools/gop_buoc_isp.py tiep {id_} <ngày>")
        return 2
    print(f"── không còn xung đột MÃ ⇒ chạy: python tools/gop_buoc_isp.py tiep {id_} <ngày>")
    return 0


def dem_thu_thap(*duong: str) -> int:
    """Tổng các dòng `tests/…: n` — `pyproject` đã có `-q`, thêm `-q` ⇒ dạng một dòng mỗi tệp."""
    env = dict(os.environ, PYTEST_ADDOPTS="")
    kq = chay([PY, "-m", "pytest", "--collect-only", "-q", *duong], kiem=False, env=env)
    so = [int(m) for m in re.findall(r"^tests/\S+: (\d+)$", kq.stdout, re.M)]
    if not so or kq.returncode not in (0,):
        sys.stderr.write(kq.stdout[-3000:] + kq.stderr[-2000:])
        raise SystemExit(f"ĐỎ (Đ5): thu thập {duong or 'toàn bộ'} ⛔ đo được — exit {kq.returncode}, {len(so)} dòng tệp")
    return sum(so)


def thay_mot(van: str, mau: str, moi: str, ten: str) -> str:
    """Thay ĐÚNG một chỗ khớp — 0 hoặc ≥ 2 chỗ ⇒ ĐỎ (Đ5)."""
    kq, n = re.subn(mau, moi, van, flags=re.M)
    if n != 1:
        raise SystemExit(f"ĐỎ (Đ5): mẫu `{ten}` khớp {n} lần, mong 1")
    return kq


def dat_san(id_: str, n: int, web: int) -> tuple[int, int]:
    s = SCRIPT.read_text(encoding="utf-8")
    cu = int(re.search(r"^MONG_PYTEST_TOAN_BO=(\d+)$", s, re.M).group(1))
    cu_web = int(re.search(r"^MONG_PYTEST_WEB=(\d+)$", s, re.M).group(1))
    s = thay_mot(s, r"^MONG_PYTEST_TOAN_BO=\d+$", f"MONG_PYTEST_TOAN_BO={n}", "MONG_PYTEST_TOAN_BO")
    s = thay_mot(s, r"^MONG_PYTEST_WEB=\d+$", f"MONG_PYTEST_WEB={web}", "MONG_PYTEST_WEB")

    b = BAI_GHIM.read_text(encoding="utf-8")
    b = thay_mot(b, r'(MONG_PYTEST_TOAN_BO=\(\\d\+\)\$", van, re\.M\) == \[")\d+("\])', rf"\g<1>{n}\g<2>", "ghim TOAN_BO")
    b = thay_mot(b, r'(MONG_PYTEST_WEB=\(\\d\+\)\$", van, re\.M\) == \[")\d+("\])', rf"\g<1>{web}\g<2>", "ghim WEB")
    them = f" · + `isp/{id_}` ⇒ **{n}**" + (f" (web {cu_web} ⇒ **{web}**)" if web != cu_web else "") + "."
    if n != cu or web != cu_web:   # sàn không đổi ⇒ nhánh bước đã tự ghi chuỗi gộp (bia: gộp H7 20/11 ghi lặp)
        b = thay_mot(b, rf"(⇒ \*\*{cu}\*\*(?: \([^)\n]*\))?)\.$", rf"\g<1>{them}", "chú thích chuỗi gộp")
    SCRIPT.write_text(s, encoding="utf-8")   # ghi CẢ HAI chỉ khi mọi mẫu đã khớp đúng 1 lần
    BAI_GHIM.write_text(b, encoding="utf-8")
    return cu, cu_web


def tiep(a: argparse.Namespace) -> int:
    id_ = a.id
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ["PG_DSN"] = f"postgresql://fls:fls@localhost:{a.cong}/fls"
    os.environ["PG_DSN_TEST"] = f"postgresql://fls:fls@localhost:{a.cong}/fls_test"
    if not (GOC / ".git/MERGE_HEAD").exists():
        raise SystemExit("ĐỎ: không có phép gộp đang dở — chạy `bat-dau` trước")
    con = [t for t in xung_dot() if t not in HAI_TEP_SAN]
    if con:
        raise SystemExit(f"ĐỎ: còn xung đột MÃ chưa gỡ: {con}")
    chay(["git", "checkout", "--ours", *HAI_TEP_SAN])                             # bước 4
    chay(["git", "add", *HAI_TEP_SAN])
    dau = chay(["git", "grep", "-lE", "^(<<<<<<<|>>>>>>>) ", "--", "."], kiem=False).stdout.split()
    if dau:
        raise SystemExit(f"ĐỎ: còn dấu xung đột trong {dau}")

    n = dem_thu_thap()                                                            # bước 5
    web = dem_thu_thap("tests/web")
    cu, cu_web = dat_san(id_, n, web)                                             # bước 6
    print(f"── sàn toàn bộ {cu} ⇒ {n} · web {cu_web} ⇒ {web}  (thu thập thật của cây gộp)")

    van = SO_CHUNG.read_text(encoding="utf-8")                                    # bước 7
    m = re.search(r"\*\*Version:\*\* v0\.(\d+)", van)
    ver = f"v0.{int(m.group(1)) + 1}"
    rieng = GOC / f"docs/ITL/04_Test/review/SO_PHAT_HIEN_ISP-3.1_{id_}.md"
    if rieng.exists():
        sha = chay(["git", "rev-parse", "--short", f"isp/{id_}"]).stdout.strip()
        print(chay([PY, "-I", str(GOP_SO), str(GOC), id_, ver, a.ngay, sha]).stdout)
    else:
        print(f"── ⚠ không có sổ riêng {rieng.name} — bỏ bước 7 (ghi lý do vào commit)")

    print("── bước 9: cổng (mong: giấy ĐẠT · 11 kept · tuyến khớp · PII 0)")    # bước 9
    ket = []
    for ten, lenh, mong in [
        ("kiem_tai_lieu", [PY, "docs/ITL/_tools/kiem_tai_lieu.py"], r"cong tai lieu DAT"),
        ("lint-imports", [str(GOC / ".venv/bin/lint-imports")], r"11 kept, 0 broken"),
        ("soi_bang_tuyen", [PY, "tools/soi_bang_tuyen.py"], None),
        ("quet_pii_repo", [PY, "tools/quet_pii_repo.py"], r"\[ĐẠT\] 0 chỗ"),
    ]:
        kq = chay(lenh, kiem=False)
        dat = kq.returncode == 0 and (mong is None or re.search(mong, kq.stdout + kq.stderr))
        dong = (kq.stdout + kq.stderr).strip().splitlines()[-1:] or [""]
        ket.append(dat)
        print(f"  [{'ĐẠT' if dat else 'ĐỎ'}] {ten}: {dong[0][:160]}")

    print(f"""
── VIỆC CÒN LẠI (tay):
   8.  bước mở tuyến/đổi hợp đồng ⇒ `07_API_CONTRACT.md` §4i ⬜ → ✅ + bump version + changelog
   ·   chạy bài liên quan của bước
   10. git commit -m "Gộp isp/{id_} (…): R2 cuối KQ-… ĐẠT 0 · 0" + trailer
       bash tools/dung_moi_truong_isp.sh --duong-nen --cong {a.cong}   (nền ~25 phút; chỉ push khi KẾT: ĐẠT)
   11. hàng TIEN_DO → commit → push""")
    return 0 if all(ket) else 1


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="lenh", required=True)
    b = sp.add_parser("bat-dau")
    b.add_argument("id")
    b.add_argument("--nhanh-lam-viec", default="claude/bold-galileo-zukpaf")
    t = sp.add_parser("tiep")
    t.add_argument("id")
    t.add_argument("ngay")
    t.add_argument("--cong", default="5433")
    a = p.parse_args()
    return bat_dau(a) if a.lenh == "bat-dau" else tiep(a)


if __name__ == "__main__":
    sys.exit(main())
