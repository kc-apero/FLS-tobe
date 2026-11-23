"""RÀO ĐẦU VÀO — ảnh `dau_vao` nào được dựng PD nào *(ISP 3.1.2 · DT13 · vòng sửa R1 `KQ-321`: `DT13-R1-01` · `DT13-R1-02`)*.

⭐ Vì sao. Hai ảnh của DT13 **trùng đáp án** của một PD khác ⇒ nạp nhầm là đọc đáp án đổi tên, engine xanh vô nghĩa:
  * `sign_off_dau_vao` trùng **13.541/13.541** ô SỐ cột số liệu *(KQ-321 ghi 14.036 — đếm khác vật)* với đáp án 605 *(`daily_report_3`, cùng `checksum_noi_dung`)* ⇒ hợp lệ CHỈ cho **608**.
  * `ccr_daily_report_2` trùng **25.185/26.272 = 95,9 %** ô SỐ với đáp án `daily_report_2` *(PD 610)* ⇒ hợp lệ CHỈ cho **615**.
Khai `DAU_VAO_CHO` *(whitelist)* + `CAM_CHO` *(blacklist, để thông báo lỗi có tên)* nằm Ở KHUÔN của từng ảnh; module này gom lại,
nạp bằng đường tệp *(như `ccr_daily_report_2` nạp `daily_report_2`)*. Engine H14 GỌI `kiem_dau_vao_hop_le(anh, dap_an)` trước khi đọc ảnh;
`quet_tham_chieu` bắt tệp mã nào nhắc ảnh mà ⛔ gọi hàm kiểm. Bài: `tests/du_lieu/test_rao_dau_vao_dt13_r1.py`.
"""
from __future__ import annotations

import importlib.util
import pathlib
import re
import sys
from typing import Any

_KH = pathlib.Path(__file__).resolve().parent
TEN_HAM = "kiem_dau_vao_hop_le"


class DauVaoSaiChoError(ValueError):
    """Ảnh đầu vào được dùng cho PD ngoài `DAU_VAO_CHO` của nó *(vòng tròn / trùng đáp án)*."""


def _nap(ten: str):
    ten_mod = f"khuon_dong_bang_rao_{ten}"
    if ten_mod in sys.modules:
        return sys.modules[ten_mod]
    spec = importlib.util.spec_from_file_location(ten_mod, _KH / f"{ten}.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules[ten_mod] = mod
    spec.loader.exec_module(mod)
    return mod


#: `ccr_daily_report_2_song` *(WO-353)* = khuôn chụp lại DR2 từ nguồn sống — CÙNG rào với khuôn cũ *(đọc thẳng `DAU_VAO_CHO`/`CAM_CHO`
#: của khuôn cũ)*; ảnh của nó mang `khuon: ccr_daily_report_2_song` ⇒ phải có mục ở đây, ⛔ thì rào cho qua im lặng.
ANH_CO_RAO = ("sign_off_dau_vao", "ccr_daily_report_2", "ccr_daily_report_2_song")
#: {tên ảnh: (DAU_VAO_CHO, CAM_CHO)} — đọc TỪ KHUÔN *(⛔ khai hai chỗ)*.
RAO: dict[str, tuple[frozenset, frozenset]] = {t: (_nap(t).DAU_VAO_CHO, _nap(t).CAM_CHO) for t in ANH_CO_RAO}


def _pd(dap_an: Any) -> str:
    so = re.findall(r"\d+", str(dap_an))
    return so[0] if so else str(dap_an)


def kiem_dau_vao_hop_le(anh: Any, dap_an: Any) -> None:
    """Ném `DauVaoSaiChoError` nếu ảnh `anh` *(tên, hoặc dict ảnh có `khuon`)* KHÔNG được dựng PD `dap_an` *(`605` · `"PD 605"` · `605`)*.
    Ảnh không khai rào ⇒ qua."""
    ten = anh["khuon"] if isinstance(anh, dict) else str(anh)
    if ten not in RAO:
        return
    cho, cam = RAO[ten]
    pd = _pd(dap_an)
    if pd in cam or pd not in cho:
        raise DauVaoSaiChoError(
            f"ảnh `{ten}` CHỈ là đầu vào cho PD {sorted(cho)} — ⛔ dùng cho PD {pd} "
            f"(CAM_CHO={sorted(cam)}; trùng đáp án ⇒ đọc đáp án đổi tên)")


def dem_o_so_trung(a: dict, b: dict, *, cot: list[str]) -> tuple[int, int]:
    """(ô SỐ ở `a` theo `cot`, số ô trong đó TRÙNG ô cùng `dong_sheet` + cột của `b` — dung sai tương đối 1e-9). Mẫu số = ô số của `a`."""
    def so(x: Any):
        try:
            return float(x)
        except (TypeError, ValueError):
            return None
    bb = {int(d["dong_sheet"]): d for d in b["dong"]}
    n = ok = 0
    for d in a["dong"]:
        e = bb.get(int(d["dong_sheet"]))
        for c in cot:
            v = so(d.get(c))
            if v is None:
                continue
            n += 1
            w = so(e.get(c)) if e else None
            if w is not None and abs(v - w) <= 1e-9 * max(1.0, abs(w)):
                ok += 1
    return n, ok


def quet_tham_chieu(goc: pathlib.Path, ten_anh: str) -> list[pathlib.Path]:
    """Tệp `.py` dưới `fls/` + `tools/` NHẮC `ten_anh` mà ⛔ gọi `kiem_dau_vao_hop_le` — trừ khuôn của chính ảnh và module rào này."""
    # khuôn của chính ảnh + khuôn ANH EM có rào *(`<ảnh>_song` — WO-353: nạp thân khuôn cũ nên nhắc tên ảnh, và chính nó
    # khai rào ở `ANH_CO_RAO`)* — ⛔ phải "engine đọc ảnh".
    bo_qua = {(_KH / f"{ten_anh}.py").resolve(), pathlib.Path(__file__).resolve(),
              *((_KH / f"{t}.py").resolve() for t in ANH_CO_RAO if t.startswith(f"{ten_anh}_"))}
    bat = []
    for thu_muc in ("fls", "tools"):
        for p in sorted((goc / thu_muc).rglob("*.py")):
            if "__pycache__" in p.parts or p.resolve() in bo_qua:
                continue
            van = p.read_text(encoding="utf-8", errors="replace")
            # theo TOKEN *(WO-353)*: `ccr_daily_report_2` là CHUỖI CON của `ccr_daily_report_20261123` *(ảnh 615)* — so chuỗi con
            # thì tệp nhắc ảnh 615 bị gọi là "đọc DR2". Sau tên ⛔ được là chữ/số; `_`/`.`/hết dòng thì đúng là nhắc ảnh.
            if re.search(rf"{re.escape(ten_anh)}(?![0-9A-Za-z])", van) and TEN_HAM not in van:
                bat.append(p)
    return bat
