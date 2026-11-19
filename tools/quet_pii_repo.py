"""WO-234 · máy quét số TÀI KHOẢN CÁ NHÂN trong MỌI tệp đã theo dõi (`git ls-files`).

  python tools/quet_pii_repo.py                # bảng ĐẾM theo tệp; thoát 1 nếu còn
  python tools/quet_pii_repo.py --che          # che tại chỗ (TK_CA_NHAN_<n>), rồi quét lại

⛔⛔ KHÔNG BAO GIỜ in giá trị số TK (kể cả vài chữ số đầu): chỉ in ĐẾM · tệp · dòng.

Ba mẫu — mỗi mẫu một dạng đã THẤY ở repo (đo 19/11, `KQ-178` C8-R1-06 · `KQ-195` DT6):
  khoa_R_CN     `R | <số>_<NH> <TT>_CN`        khoá nguồn của hàng nhãn `CN` (ảnh DT3 · tài liệu BA)
  tk_json_CN    `"tk":"<số>" … "le":"CN"`      dữ liệu nhúng trong HTML màn gán lệnh chi
  dien_giai_CK  `<số>-<ddmmyy>-CK …`           diễn giải sao kê có chứa số TK người nhận

Phạm vi = TK CÁ NHÂN (nhãn `CN`). TK pháp nhân (`_VGOH`…) NGOÀI phạm vi WO-234.
Che = `TK_CA_NHAN_<n>`: n theo thứ tự gặp đầu tiên; cùng số ⇒ cùng mã; ⛔ đảo được
(bảng số→mã chỉ nằm trong bộ nhớ lúc chạy).

Đ3: tập quét rỗng/quá nhỏ ⇒ ĐỎ.  Đ5: khai `MONG_SO_MAU = 3` và `MONG_TOI_THIEU_TEP`.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

MAU = {
    "khoa_R_CN": re.compile(r"(?<!\d)(\d{6,})(?=_[A-Za-z]+ [A-Z]{3}_CN\b)"),
    "tk_json_CN": re.compile(r'(?<="tk":")(\d{6,})(?="[^}\n]*"le":"CN")'),
    "dien_giai_CK": re.compile(r"(?<!\d)(\d{10,16})(?=-\d{6}-CK)"),
}
MONG_SO_MAU = 3
MONG_TOI_THIEU_TEP = 1000          # mẫu số tối thiểu khi quét repo thật (Đ3)


@dataclass
class Khop:
    mau: str
    dong: int
    bd: int
    kt: int


@dataclass
class KetQua:
    so_tep: int
    so_mau: int
    theo_tep: dict


def quet_van_ban(van: str) -> list[Khop]:
    ra = []
    for dong, d in enumerate(van.split("\n"), 1):
        for ten, mau in MAU.items():
            ra += [Khop(ten, dong, m.start(), m.end()) for m in mau.finditer(d)]
    return ra


def che_van_ban(van: str, ma: dict) -> str:
    """Thay mọi số TK cá nhân bằng `TK_CA_NHAN_<n>`; `ma` (số→n) dùng chung để cùng số ⇒ cùng mã.
    Đã biết số ⇒ thay MỌI chỗ xuất hiện nguyên số ấy (kể cả ngoài ba mẫu), có biên chữ số."""
    for mau in MAU.values():
        for m in mau.finditer(van):
            ma.setdefault(m.group(1), len(ma) + 1)
    for so, n in sorted(ma.items(), key=lambda kv: -len(kv[0])):
        van = re.sub(rf"(?<!\d){so}(?!\d)", f"TK_CA_NHAN_{n}", van)
    return van


def _tep_theo_doi(goc: Path) -> list[str]:
    kq = subprocess.run(["git", "ls-files", "-z"], cwd=goc, capture_output=True, check=True)
    return [t for t in kq.stdout.decode("utf-8").split("\0") if t]


def _doc(goc: Path, tep: str):
    try:
        return (goc / tep).read_bytes().decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return None                                  # nhị phân / đã xoá: ⛔ có chữ để quét


def quet_repo(goc: Path) -> KetQua:
    theo = defaultdict(list)
    tep = _tep_theo_doi(goc)
    for t in tep:
        van = _doc(goc, t)
        if van is not None and (kh := quet_van_ban(van)):
            theo[t] = kh
    return KetQua(len(tep), len(MAU), dict(theo))


def che_repo(goc: Path) -> dict:
    """Che tại chỗ. Trả {tệp: số chỗ che}. Số→mã gom MỘT lượt: tệp quét theo thứ tự `git ls-files`."""
    ma, dem = {}, {}
    for t in _tep_theo_doi(goc):
        van = _doc(goc, t)
        if van is None or not quet_van_ban(van):
            continue
        moi = che_van_ban(van, ma)
        dem[t] = moi.count("TK_CA_NHAN_") - van.count("TK_CA_NHAN_")
        (goc / t).write_bytes(moi.encode("utf-8"))
    return dem


def _in(kq: KetQua) -> int:
    n = sum(len(v) for v in kq.theo_tep.values())
    print(f"quét {kq.so_tep} tệp · {kq.so_mau} mẫu (mong {MONG_SO_MAU})")
    for t, kh in sorted(kq.theo_tep.items()):
        ct = defaultdict(int)
        for k in kh:
            ct[k.mau] += 1
        print(f"  {len(kh):>3}  {t}  " + " ".join(f"{m}={c}" for m, c in sorted(ct.items())))
    do = kq.so_tep < MONG_TOI_THIEU_TEP or kq.so_mau != MONG_SO_MAU
    if do:
        print(f"[ĐỎ] mẫu số {kq.so_tep} tệp < {MONG_TOI_THIEU_TEP} hoặc số mẫu ≠ {MONG_SO_MAU} — phép đo ⛔ đáng tin")
    print(f"[{'ĐẠT' if n == 0 and not do else 'ĐỎ'}] {n} chỗ số TK cá nhân · {len(kq.theo_tep)} tệp")
    return 1 if (n or do) else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--goc", default=str(Path(__file__).resolve().parents[1]))
    ap.add_argument("--che", action="store_true")
    a = ap.parse_args(argv)
    goc = Path(a.goc)
    if a.che:
        dem = che_repo(goc)
        for t, n in sorted(dem.items()):
            print(f"  che {n:>3}  {t}")
        print(f"che {sum(dem.values())} chỗ · {len(dem)} tệp")
    return _in(quet_repo(goc))


if __name__ == "__main__":
    sys.exit(main())
