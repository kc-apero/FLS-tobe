"""Đường **NGUỒN TĨNH** — luật **MỘT chỗ** *(ISP 3.1.2 · Step 2 · `C1` · vòng sửa sau R1,
`C1-R1-02` · `KQ-077`)*.

⛔⛔ **Vì sao tệp này tồn tại — bia của một ngoại lệ đã NỚI cổng.** `C1` thêm
   `Tuyen.nguon_tinh` *(tuyến đọc một TỆP đi cùng gói, ⛔ đọc kho)* và dạy hai cổng
   chấp nhận nó. Phép canh duy nhất lúc ấy là *"tệp có TỒN TẠI"* — một câu về
   **hình**. R1 dựng 4 tuyến cố ý khai sai rồi hỏi hai cổng *(bản sao, ⛔ kho)*:
     · **A** hàm `so` *(đọc sổ)* · `bang=()` · `nguon_tinh=('pyproject.toml',)` ⇒
       `kiem_bang_tuyen` **XANH** *(trước C1 cổng ⓓ đỏ)*;
     · **B** `nguon_tinh=('CLAUDE.md',)` ⇒ **cả hai cổng XANH**;
     · **D** `nguon_tinh=('../../../../../../../../etc/hostname',)` *(ra NGOÀI repo)*
       ⇒ **cả hai cổng XANH**;
     · **C** `nguon_tinh` là CHUỖI *(quên dấu phẩy tuple)* ⇒ `kiem_bang_tuyen` XANH,
       `soi` đỏ bằng **32** câu rác *(nó lặp trên từng KÝ TỰ)*.
   Và `fx.doc_tep` cũ đọc `_GOC_REPO / duong` — trong `pathlib`, `Path('/repo') /
   '/etc/hostname'` **là** `/etc/hostname`: đường tuyệt đối THẮNG gốc, im lặng.
   ⇒ Ngoại lệ *"⛔ khai bảng nào — vì đọc tệp tĩnh"* đã thành *"⛔ khai bảng nào —
   miễn chỉ vào một tệp có thật bất kỳ trên máy"*.

⇒ **Thư mục nguồn tĩnh khai ở đây, một lần** (`THU_MUC`), và **một** luật đường dùng
  chung cho ba chỗ: `fls.api.bang_tuyen.kiem_bang_tuyen` *(lúc dựng máy)* ·
  `tools/soi_bang_tuyen.py` *(cổng — thêm phép canh SỰ THẬT: hàm có mang chuỗi đường,
  có chạm kho)* · `fls.cau_hinh.fx.doc_tep` *(lúc đọc)*. `C4` *(`GET /config/hd`
  "tĩnh từ ảnh")* là người dùng thứ hai — dùng lại, ⛔ chép luật.

Luật *(mọi lý do đều MỘT dòng — luật `S0-R1-04`)*:
  ⓐ kiểu `str` *(⛔ `Path`, ⛔ `bytes`)*; ⓑ ⛔ rỗng, ⛔ khoảng trắng đầu/cuối;
  ⓒ dạng POSIX *(⛔ `\\`)*; ⓓ TƯƠNG ĐỐI gốc repo *(⛔ `/…`, ⛔ ổ đĩa `C:`)*;
  ⓔ ⛔ khúc rỗng/`.`/`..`; ⓕ nằm **NGAY dưới** `THU_MUC/` *(⛔ thư mục con)*;
  ⓖ tên tệp `[a-z0-9_]+.json`; ⓗ **giải đường THẬT** *(liên kết mềm)* vẫn nằm ngay
  dưới `THU_MUC` thật, và `THU_MUC` thật **chính là** `<gốc>/THU_MUC` *(chính thư mục
  ⛔ được là liên kết ra ngoài)*.
  `kiem_duong` xét ⓐ…ⓗ *(HÌNH + đường thật)*; sự CÓ MẶT của tệp là việc của `giai`
  *(lúc đọc)* và của `soi` *(cổng)* — `kiem_bang_tuyen` chạy lúc dựng máy và ⛔ nên
  phụ thuộc vào việc một tệp dữ liệu đã được chép tới hay chưa.

⛔ Tầng này ⛔ biết kho *(`.importlinter` hợp đồng 10)* — chỉ `re` + `pathlib`.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Iterable

# ⭐ Khai MỘT chỗ *(tương đối gốc repo, dạng POSIX)*. `fx.NGUON_TINH` nằm dưới nó.
THU_MUC = "fls/cau_hinh/tinh"
_KHUC_THU_MUC = tuple(THU_MUC.split("/"))
GOC_REPO = Path(__file__).resolve().parents[2]

_TEN_TEP = re.compile(r"[a-z0-9_]+\.json", re.ASCII)
_O_DIA = re.compile(r"[A-Za-z]:")


def _mot_dong(s: object) -> str:
    """Giá trị lạ đưa vào câu lỗi — ⛔ để nó phá luật *"một dòng"*."""
    return " ".join(repr(s).split())


class LoiNguonTinh(ValueError):
    """Đường nguồn tĩnh ⛔ hợp lệ. Câu lỗi **một dòng**, nói ra đường + mọi lý do."""

    def __init__(self, duong: object, ly_do: Iterable[str]) -> None:
        self.duong = duong
        self.ly_do = tuple(ly_do)
        super().__init__(f"⛔ nguồn tĩnh {_mot_dong(duong)}: " + " · ".join(self.ly_do))


def kiem_duong(duong: object, *, goc: Path | None = None) -> list[str]:
    """Lý do một đường nguồn tĩnh **⛔ hợp lệ** *(rỗng = hợp lệ)*. ⛔ Đòi tệp có mặt.

    `goc` — gốc repo *(mặc định `GOC_REPO`)*; bài thử truyền một repo giả để dựng
    liên kết mềm mà ⛔ ghi vào repo thật.
    """
    if not isinstance(duong, str):
        return [f"kiểu {type(duong).__name__} — ⛔ phải str (đường POSIX tương đối "
                f"gốc repo)"]
    ly_do: list[str] = []
    if not duong or duong != duong.strip():
        ly_do.append("rỗng hay có khoảng trắng đầu/cuối")
    if "\\" in duong:
        ly_do.append("có `\\` — ⛔ dạng POSIX")
    if duong.startswith("/") or _O_DIA.match(duong):
        ly_do.append("đường TUYỆT ĐỐI — ⛔ tương đối gốc repo")
    khuc = duong.split("/")
    if any(k in ("", ".", "..") for k in khuc):
        ly_do.append("có khúc rỗng / `.` / `..`")
    if tuple(khuc[:-1]) != _KHUC_THU_MUC:
        ly_do.append(f"⛔ nằm NGAY dưới {THU_MUC}/")
    if not _TEN_TEP.fullmatch(khuc[-1]):
        ly_do.append("tên tệp ⛔ khớp [a-z0-9_]+.json")
    if ly_do:
        return ly_do      # hình đã sai ⇒ ⛔ giải đường *(⛔ chạm hệ tệp vì một đường lạ)*

    # ⓗ Giải đường THẬT: hình đúng mà một liên kết mềm trỏ ra ngoài vẫn là ra ngoài.
    g = goc if goc is not None else GOC_REPO
    thu_muc_khai = g.resolve().joinpath(*_KHUC_THU_MUC)
    thu_muc_that = g.joinpath(*_KHUC_THU_MUC).resolve()
    that = g.joinpath(*khuc).resolve()
    if that.parent != thu_muc_that or thu_muc_that != thu_muc_khai:
        ly_do.append(f"đường thật {that} ra ngoài {THU_MUC}/ (liên kết mềm?)")
    return ly_do


def giai(duong: object, *, goc: Path | None = None) -> Path:
    """Đường **thật** *(tuyệt đối, đã giải)* của một nguồn tĩnh hợp lệ VÀ có mặt.

    ⛔ Hỏng ⇒ `LoiNguonTinh` *(⛔ trả `None`, ⛔ đọc thử)*.
    """
    ly_do = kiem_duong(duong, goc=goc)
    if ly_do:
        raise LoiNguonTinh(duong, ly_do)
    g = goc if goc is not None else GOC_REPO
    p = g.joinpath(*str(duong).split("/")).resolve()
    if not p.is_file():
        raise LoiNguonTinh(duong, ["tệp ⛔ có thật"])
    return p


def kiem_khai(khai: object, *, goc: Path | None = None) -> list[str]:
    """Lý do giá trị **`Tuyen.nguon_tinh`** ⛔ hợp lệ *(rỗng = hợp lệ; `()` = tuyến ⛔
    có nguồn tĩnh)*.

    ⛔ Sai KIỂU ⇒ **MỘT** lý do, ⛔ lặp vào bên trong: một chuỗi là một dãy ký tự, và
      `soi` cũ đã in **32** câu rác cho đúng một chỗ quên dấu phẩy *(R1 · C)*.
    """
    if not isinstance(khai, tuple):
        return [f"kiểu {type(khai).__name__} — ⛔ phải tuple[str, ...] "
                f"(quên dấu phẩy: `(x,)`?)"]
    ly_do: list[str] = []
    hop_le: list[str] = []
    for d in khai:
        r = kiem_duong(d, goc=goc)
        if r:
            ly_do.append(f"{_mot_dong(d)}: " + " · ".join(r))
        else:
            hop_le.append(d)
    if len(set(hop_le)) != len(hop_le):
        ly_do.append(f"trùng đường: {sorted({d for d in hop_le if hop_le.count(d) > 1})}")
    return ly_do
