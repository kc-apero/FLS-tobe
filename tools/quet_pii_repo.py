"""WO-234 · máy quét số TÀI KHOẢN CÁ NHÂN trong MỌI tệp đã theo dõi (`git ls-files`).

  python tools/quet_pii_repo.py                # bảng ĐẾM theo tệp; thoát 1 nếu còn
  python tools/quet_pii_repo.py --che          # che tại chỗ (TK_CA_NHAN_<n>), rồi quét lại

⛔⛔ KHÔNG BAO GIỜ in giá trị số TK (kể cả vài chữ số đầu): chỉ in ĐẾM · tệp · dòng.

Ba mẫu — mỗi mẫu một dạng đã THẤY ở repo (đo 19/11, `KQ-178` C8-R1-06 · `KQ-195` DT6):
  khoa_R_CN     `R | <số>_<NH> <TT>_CN`        khoá nguồn của hàng nhãn `CN` (ảnh DT3 · tài liệu BA)
  tk_json_CN    `"tk":"<số>" … "le":"CN"`      dữ liệu nhúng trong HTML màn gán lệnh chi
  dien_giai_CK  `<số>-<ddmmyy>-CK …`           diễn giải sao kê có chứa số TK người nhận

Phạm vi = TK CÁ NHÂN (nhãn `CN`). TK pháp nhân (`_VGOH`…) NGOÀI phạm vi WO-234.
Vòng sửa sau R1 (`KQ-239`):
  -01  tệp `.zip` được đọc RUỘT (`zipfile`): tệp ảo `x.zip!ruột`; `che_zip` nén lại cùng cấu trúc.
  -04  Đ3: đếm tệp ĐÃ ĐỌC (`so_doc`), ⛔ tệp liệt kê. Tệp ⛔ đọc được: nhị phân khai theo ĐUÔI
       (`DUOI_NHI_PHAN`, liệt kê có tên) hoặc ĐỎ (`khong_doc_la`).
  -02/-03  mẫu `so_da_biet_CN`: số ĐÃ CHẮC là cá nhân (có khoá `CN`) mà lặp ở bất kỳ dạng nào ⇒ bắt + che.
       Số trong ba dạng chữ tự do (`cho <số>-…` · `<số>-Ref…-CK` · `tài khoản <số>`) mà ⛔ chắc ⇒ GIỮ + ĐẾM.

Che = `TK_CA_NHAN_<n>`: n theo thứ tự gặp đầu tiên; cùng số ⇒ cùng mã; ⛔ đảo được
(bảng số→mã chỉ nằm trong bộ nhớ lúc chạy).

Đ3: tập quét rỗng/quá nhỏ ⇒ ĐỎ.  Đ5: khai `MONG_SO_MAU = 3` và `MONG_TOI_THIEU_TEP`.
"""
from __future__ import annotations

import argparse
import io
import re
import subprocess
import sys
import zipfile
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

MAU = {
    "khoa_R_CN": re.compile(r"(?<!\d)(\d{6,})(?=_[A-Za-z]+ [A-Z]{3}_CN\b)"),
    "tk_json_CN": re.compile(r'(?<="tk":")(\d{6,})(?="[^}\n]*"le":"CN")'),
    "dien_giai_CK": re.compile(r"(?<!\d)(\d{10,16})(?=-\d{6}-CK)"),
}
MONG_SO_MAU = 3
MONG_TOI_THIEU_TEP = 1000          # tệp THEO DÕI tối thiểu khi quét repo thật (Đ3)
MONG_TOI_THIEU_DOC = 1000          # tệp ĐÃ ĐỌC tối thiểu (Đ3 · PII-R1-04)
MONG_TY_LE_DOC = 0.95              # ≥ 95 % mục quét phải đọc được
# Nhị phân KHAI CÓ CHỦ ĐÍCH theo đuôi (không có chữ để quét) — liệt kê có tên; đuôi khác mà ⛔ đọc được ⇒ ĐỎ.
DUOI_NHI_PHAN = {".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".pdf", ".xlsx", ".woff", ".woff2", ".ttf", ".gz"}
# Ba dạng chữ tự do (PII-R1-03): số ở đây GIỮ + ĐẾM nếu ⛔ chắc là cá nhân.
DANG_TU_DO = {
    "cho": re.compile(r"\bcho (\d{8,16})-"),
    "ref": re.compile(r"(?<!\d)(\d{8,16})-Ref[^\n]{0,80}?-CK"),
    "tk": re.compile(r"[Tt]ài khoản (\d{8,16})"),
}


@dataclass
class Khop:
    mau: str
    dong: int
    bd: int
    kt: int


@dataclass
class KetQua:
    so_tep: int                    # tệp THEO DÕI (git ls-files)
    so_mau: int
    theo_tep: dict
    so_doc: int = 0                # mục ĐÃ ĐỌC (tệp văn bản + ruột zip)
    khong_doc_co_y: list = field(default_factory=list)   # nhị phân khai theo đuôi
    khong_doc_la: list = field(default_factory=list)     # ⛔ đọc được, đuôi ⛔ khai ⇒ ĐỎ
    giu_tu_do: dict = field(default_factory=dict)        # dạng chữ tự do ⛔ chắc ⇒ GIỮ + đếm
    so_da_biet: int = 0
    xung_dot: int = 0              # chỗ của số vừa `CN` vừa pháp nhân ⇒ GIỮ + đếm

    @property
    def khong_doc(self):
        return self.khong_doc_co_y + self.khong_doc_la


def quet_van_ban(van: str, da_biet=frozenset()) -> list[Khop]:
    ra = []
    ds = [(so, re.compile(rf"(?<!\d){so}(?!\d)")) for so in da_biet]
    for dong, d in enumerate(van.split("\n"), 1):
        for ten, mau in MAU.items():
            ra += [Khop(ten, dong, m.start(), m.end()) for m in mau.finditer(d)]
        for _, mau in ds:
            ra += [Khop("so_da_biet_CN", dong, m.start(), m.end()) for m in mau.finditer(d)]
    return ra


def so_cn(van: str) -> list:
    """Số CHẮC là cá nhân: đứng ở một trong ba mẫu có khoá `CN`. Trả DANH SÁCH theo thứ tự gặp
    (mẫu rồi vị trí) — ⛔ `set`: thứ tự băm ngẫu nhiên ⇒ nhãn `TK_CA_NHAN_<n>` đánh số lệch giữa các lần chạy."""
    return list(dict.fromkeys(m.group(1) for mau in MAU.values() for m in mau.finditer(van)))


PHAP_NHAN = re.compile(r"(?<!\d)(\d{6,})(?=_[A-Za-z]+ [A-Z]{3}_(?!CN\b)[A-Z0-9]+)")


def so_phap_nhan(van: str) -> set:
    """Số mang khoá KHÁC `CN` (`_VGOH`…) — pháp nhân."""
    return {m.group(1) for m in PHAP_NHAN.finditer(van)}


def che_van_ban(van: str, ma: dict) -> str:
    """Thay mọi số TK cá nhân bằng `TK_CA_NHAN_<n>`; `ma` (số→n) dùng chung để cùng số ⇒ cùng mã.
    Đã biết số ⇒ thay MỌI chỗ xuất hiện nguyên số ấy (kể cả ngoài ba mẫu), có biên chữ số."""
    for so in so_cn(van):
        ma.setdefault(so, len(ma) + 1)
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


def _doc_zip(goc: Path, tep: str):
    """Ruột zip ⇒ [(tên ảo, văn bản|None)]; zip hỏng ⇒ None."""
    try:
        with zipfile.ZipFile(goc / tep) as z:
            ra = []
            for i in z.infolist():
                if i.is_dir():
                    continue
                try:
                    ra.append((f"{tep}!{i.filename}", z.read(i).decode("utf-8")))
                except UnicodeDecodeError:
                    ra.append((f"{tep}!{i.filename}", None))
            return ra
    except (OSError, zipfile.BadZipFile):
        return None


def _muc(goc: Path, tep: str):
    """Các mục quét của MỘT tệp theo dõi: [(tên, văn bản|None)]."""
    if tep.lower().endswith(".zip"):
        ruot = _doc_zip(goc, tep)
        return ruot if ruot is not None else [(tep, None)]
    return [(tep, _doc(goc, tep))]


def _doc_tat_ca(goc: Path):
    muc = []
    for t in _tep_theo_doi(goc):
        muc += _muc(goc, t)
    return muc


def quet_repo(goc: Path) -> KetQua:
    muc = _doc_tat_ca(goc)
    kq = KetQua(len(_tep_theo_doi(goc)), len(MAU), {})
    da_biet: set = set()
    phap_nhan: set = set()
    for ten, van in muc:
        if van is None:
            (kq.khong_doc_co_y if Path(ten).suffix.lower() in DUOI_NHI_PHAN else kq.khong_doc_la).append(ten)
            continue
        kq.so_doc += 1
        da_biet.update(so_cn(van))
        phap_nhan |= so_phap_nhan(van)
        for d, mau in DANG_TU_DO.items():
            kq.giu_tu_do[d] = kq.giu_tu_do.get(d, 0) + sum(1 for _ in mau.finditer(van))
    # -02: số vừa gắn `CN` vừa gắn khoá pháp nhân ⇒ ⛔ CHẮC ⇒ GIỮ (chủ 19/11 08:30) + đếm chỗ
    xung = da_biet & phap_nhan
    da_biet -= xung
    kq.xung_dot = sum(1 for _, van in muc if van is not None for so in xung for _ in re.finditer(rf"(?<!\d){so}(?!\d)", van))
    kq.so_da_biet = len(da_biet)
    kq.giu_tu_do = {d: kq.giu_tu_do.get(d, 0) for d in DANG_TU_DO}
    for ten, van in muc:
        if van is not None and (kh := quet_van_ban(van, da_biet)):
            kq.theo_tep[ten] = kh
    # Chữ tự do GIỮ = hit dạng tự do TRỪ chỗ đã bị bắt (số đã biết ⇒ sẽ che, ⛔ giữ)
    for d, mau in DANG_TU_DO.items():
        bi_bat = sum(1 for _, van in muc if van is not None for m in mau.finditer(van) if m.group(1) in da_biet)
        kq.giu_tu_do[d] -= bi_bat
    return kq


def che_zip(du: bytes, ma: dict):
    """Che BÊN TRONG zip, nén lại CÙNG cấu trúc (tên · thứ tự · ngày · kiểu nén · thuộc tính).
    Trả (zip mới, {tên ruột: số chỗ che}). `ma` có sẵn nhãn ⇒ dùng lại (nhất quán với cây)."""
    ra, dem = io.BytesIO(), {}
    with zipfile.ZipFile(io.BytesIO(du)) as zi, zipfile.ZipFile(ra, "w") as zo:
        muc = []
        for i in zi.infolist():
            nd = zi.read(i)
            try:
                van = nd.decode("utf-8")
            except UnicodeDecodeError:
                van = None
            muc.append((i, nd, van))
        for _, _, van in muc:
            if van is not None:
                for so in so_cn(van):
                    ma.setdefault(so, len(ma) + 1)
        for i, nd, van in muc:
            if van is not None and not i.is_dir() and (quet_van_ban(van) or quet_van_ban(van, set(ma))):
                moi = che_van_ban(van, ma)
                dem[i.filename] = moi.count("TK_CA_NHAN_") - van.count("TK_CA_NHAN_")
                nd = moi.encode("utf-8")
            zo.writestr(i, nd, compress_type=i.compress_type)
    return ra.getvalue(), dem


def che_repo(goc: Path) -> dict:
    """Che tại chỗ. Trả {tệp: số chỗ che}. Số→mã gom MỘT lượt: tệp quét theo thứ tự `git ls-files`;
    tệp chỉ mang SỐ ĐÃ BIẾT (không có mẫu) cũng được xử (PII-R1-02)."""
    ma, dem = {}, {}
    tep = _tep_theo_doi(goc)
    van_cua = {t: _doc(goc, t) for t in tep if not t.lower().endswith(".zip")}
    pn: set = set()
    for t in tep:
        if van_cua.get(t) is not None:
            pn |= so_phap_nhan(van_cua[t])
            for so in so_cn(van_cua[t]):
                ma.setdefault(so, len(ma) + 1)
    xung = set(ma) & pn                              # vừa `CN` vừa pháp nhân ⇒ GIỮ (-02)
    for t in tep:
        if t.lower().endswith(".zip"):
            moi, d = che_zip((goc / t).read_bytes(), ma)
            if d:
                (goc / t).write_bytes(moi)
                dem[t] = sum(d.values())
            continue
        van = van_cua[t]
        if van is None or not (quet_van_ban(van) or quet_van_ban(van, set(ma) - xung)):
            continue
        moi = che_van_ban(van, ma)
        dem[t] = moi.count("TK_CA_NHAN_") - van.count("TK_CA_NHAN_")
        (goc / t).write_bytes(moi.encode("utf-8"))
    return dem


def danh_gia(kq: KetQua, toi_thieu=None):
    """(đỏ?, [lý do]) — Đ3/Đ5: phép ⛔ đo được là ĐỎ, ⛔ phải 'không thấy lệch'."""
    toi_thieu = MONG_TOI_THIEU_DOC if toi_thieu is None else toi_thieu
    ly = []
    if kq.so_doc < toi_thieu:
        ly.append(f"đã đọc {kq.so_doc} < {toi_thieu}")
    tong = kq.so_doc + len(kq.khong_doc)
    if tong and kq.so_doc / tong < MONG_TY_LE_DOC:
        ly.append(f"đọc được {kq.so_doc}/{tong} < {MONG_TY_LE_DOC:.0%}")
    if kq.khong_doc_la:
        ly.append(f"{len(kq.khong_doc_la)} tệp ⛔ đọc được, đuôi ⛔ khai")
    return bool(ly), ly


def _in(kq: KetQua) -> int:
    n = sum(len(v) for v in kq.theo_tep.values())
    print(f"quét {kq.so_tep} tệp theo dõi · ĐÃ ĐỌC {kq.so_doc} mục (kể cả ruột zip) · {kq.so_mau} mẫu (mong {MONG_SO_MAU}) · {kq.so_da_biet} số đã biết")
    for t, kh in sorted(kq.theo_tep.items()):
        ct = defaultdict(int)
        for k in kh:
            ct[k.mau] += 1
        print(f"  {len(kh):>3}  {t}  " + " ".join(f"{m}={c}" for m, c in sorted(ct.items())))
    for t in kq.khong_doc_co_y:
        print(f"  [không đọc · khai theo đuôi] {t}")
    for t in kq.khong_doc_la:
        print(f"  [KHÔNG ĐỌC ĐƯỢC · ⛔ khai] {t}")
    print("  giữ (⛔ chắc cá nhân; chỉ đếm): " + " ".join(f"{k}={v}" for k, v in sorted(kq.giu_tu_do.items())) + f" · số_vừa_CN_vừa_pháp_nhân={kq.xung_dot}")
    do_doc, ly = danh_gia(kq)
    do = do_doc or kq.so_tep < MONG_TOI_THIEU_TEP or kq.so_mau != MONG_SO_MAU
    if do:
        print(f"[ĐỎ] phép đo ⛔ đáng tin: {'; '.join(ly) or 'mẫu số/mẫu sai mong'}")
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
