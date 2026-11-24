"""Bài thử kịch bản UAT `docs/ITL/04_Test/UAT_STAGING_E2E.md` — `WO-325` AC-4.

Luật `Đ2`: một con số trong tài liệu phải so với NGUỒN của nó. Mỗi con số HD2 trong UAT mang thẻ `<!--hd2:GÓI.TRƯỜNG-->`;
bài này tính lại từ `docs/ITL/_tools/hd2_cong.json` và đòi KHỚP — đổi một con số ở một bên (tài liệu hay tệp cổng) ⇒ ĐỎ.
Và `Đ3`: số thẻ > 0 (báo cáo "khớp" trên tập rỗng là vô nghĩa).
"""
from __future__ import annotations

import json
import re

import pytest

from tests.staging import ho_tro as H

DOC = H.GOC / "docs" / "ITL" / "04_Test" / "UAT_STAGING_E2E.md"
JSON = H.GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json"

# ⭐ `STG-R1-05`: ⛔ đóng cứng `CHA = {"WP-C5": [C5a, C5b]}` — bài từng tự tính lại bằng CHÍNH giả định sai của tài liệu (Đ2: hai nguồn ⛔ độc lập)
#   nên xanh khi H14 thêm `WP-C5c`. Nay gói con suy từ KHOÁ có trong `hd2_cong.json`; gói cha = tiền tố có ≥ 2 con.
def _cha(d: dict) -> dict[str, list[str]]:
    nhom: dict[str, list[str]] = {}
    for k in d:
        m = re.fullmatch(r"(WP-C\d)[a-z]", k)
        if m:
            nhom.setdefault(m.group(1), []).append(k)
    return {c: sorted(v) for c, v in nhom.items() if len(v) >= 2}


CHA = _cha(json.loads(JSON.read_text(encoding="utf-8")))


def _vn(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def _khoi(d: dict, g: str) -> dict:
    return d if g == "WP-C2" else d[g]


def _mong(d: dict, g: str, k: str) -> int:
    kids = CHA.get(g, [g])
    if k == "lech":
        return sum(_khoi(d, x)["tong_o"] - _khoi(d, x)["khop"] for x in kids)
    return sum(_khoi(d, x)[k] for x in kids)


def _the() -> list[tuple[str, str, str]]:
    return re.findall(r"<!--hd2:([A-Za-z0-9-]+)\.(\w+)-->([0-9.]+)", DOC.read_text(encoding="utf-8"))


def test_moi_con_so_HD2_trong_UAT_khop_hd2_cong_json():
    d = json.loads(JSON.read_text(encoding="utf-8"))
    the = _the()
    # 14 hàng: C2 (2 số: lệch có tên = 0 ⛔ thẻ) · C3a/b/c/d (3) · C3 (3) · C4a/C4b (2 — lệch 0) · C4c (3) · C4 (3) · C5a/b/c (3+3+3) · C5 (3)
    assert len(the) == 39, f"{len(the)} thẻ ≠ 39 — thêm/bớt số trong bảng U3 phải đổi bài này (Đ5: khai mong)"
    sai = [(g, k, doc, _vn(_mong(d, g, k))) for g, k, doc in the if doc != _vn(_mong(d, g, k))]
    assert sai == [], sai
    # đủ gói: mọi gói của NGUỒN (`tools.do_hd2.GOI_BIET` — ⛔ chép tay) + các gói cha suy từ tệp cổng
    from tools.do_hd2 import GOI_BIET
    assert GOI_BIET and {g for g, _, _ in the} == set(GOI_BIET) | set(CHA), (sorted(set(GOI_BIET) | set(CHA)), sorted({g for g, _, _ in the}))
    assert CHA["WP-C5"] == ["WP-C5a", "WP-C5b", "WP-C5c"], CHA        # mẫu số ≠ rỗng: H14 đã gộp
    assert d["WP-C5c"]["dat"] is True and d["WP-C5c"]["dat_mong"] is True and d.get("dat") is not False


def _so_615(d: dict, k: str) -> int:
    """Số §1·615 từ tệp cổng: `o_so` / `o_dap_an_so` của đáp án 615 + Σ `chua_co_dau_vao:*` trong `ngoai_mau_so_co_ten`."""
    p = d["WP-C5c"]["do_phu"]["615"]
    if k == "chua_co_dau_vao":
        return sum(v for kk, v in p["ngoai_mau_so_co_ten"].items() if kk.startswith("chua_co_dau_vao:"))
    return p[k]


def test_so_615_o_muc_1_khop_hd2_cong_json_va_so_dong_chuoi_U7_khop_GOI_BIET():
    d = json.loads(JSON.read_text(encoding="utf-8"))
    van = DOC.read_text(encoding="utf-8")
    the = re.findall(r"<!--hd2x:615\.(\w+)-->([0-9.]+)", van)
    assert {k for k, _ in the} == {"o_so", "o_dap_an_so", "chua_co_dau_vao"}, the      # mẫu số: đủ 3 thẻ
    assert [(k, v) for k, v in the if v != _vn(_so_615(d, k))] == []
    # U7: số dòng + số gói trong chuỗi in = ĐÚNG số gói của nguồn, ⛔ số cứng (`STG-R1-02` cùng gốc)
    from tools.do_hd2 import GOI_BIET
    n = len(GOI_BIET)
    m = re.search(r"<!--goi:dong-->(\d+) dòng\*\* `(WP-C\w+) … (WP-C\w+)`.*<!--goi:chuoi-->(\d+) gói", van)
    assert m and (int(m.group(1)), m.group(2), m.group(3), int(m.group(4))) == (n, GOI_BIET[0], GOI_BIET[-1], n), (m and m.groups(), n)
    assert "[CHỜ H14]" not in van, "H14 đã gộp — nhãn chờ phải bỏ"
    # `STG-R2-02`: U9 = chuỗi SAU ký; U7 = chuỗi TRƯỚC ký — hai chiều D1, số gói đều từ NGUỒN (⛔ số cứng)
    t = re.search(r"<!--goi:truoc_dong-->(\d+) dòng.*<!--goi:truoc_chuoi-->(\d+) gói · ĐỎ (\d+)", van)
    assert t and (int(t.group(1)), int(t.group(2))) == (n, n), (t and t.groups(), n)
    # MONG đo 23/11 (`test_04`: tập ĐỎ trước ký = tập gói đọc tỷ giá, đo từ nguồn): MỌI gói đọc tỷ giá ⇒ ĐỎ n/n.
    # Gói nào sau này thôi đọc tỷ giá ⇒ bài `test_04` đổi mong ⇒ bài này đỏ ⇒ sửa UAT cùng commit.
    assert int(t.group(3)) == n, t.groups()
    assert re.search(r"<!--goi:truoc_n-->(\d+) gói ĐỎ", van).group(1) == str(n)


def test_UAT_I2_da_gop_khong_con_nhan_CHO_I2_va_so_thang_ky_khop_nguon():
    """`STG-R2-02`: nhãn `[CHỜ I2]` lỗi thời ở cây gộp (I2 có `FxKho`) — canh để nó TỰ ĐỎ khi I2 vào mà UAT còn nhãn;
    số tháng cần ký ở U8 = (số dòng ảnh `ix_fx.json` − số tháng LẠC) tính lại từ NGUỒN `fls.cau_hinh.fx.kiem`."""
    van = DOC.read_text(encoding="utf-8")
    from tools import do_hd2 as h
    i2 = "class FxKho" in (H.GOC / "tools" / "do_hd2.py").read_text(encoding="utf-8")
    assert i2, "cây này ⛔ có I2 (FxKho) — bài canh vô nghĩa (Đ3)"
    than = van.split("## Changelog")[0]                       # Đ2: changelog là BIÊN BẢN (nó trích lại nhãn cũ) ⇒ chỉ đo phần KHAI
    assert "[CHỜ I2]" not in than and "CHƯA có I2" not in than, "I2 đã có FxKho — UAT còn nhãn chờ"
    j = json.loads((H.GOC / "tests" / "fixture" / "cau_hinh" / "ix_fx.json").read_text(encoding="utf-8"), parse_float=h.Decimal)
    dong = [{"yyyymm": int(r["Month"]), **{c: r[c] for c in h.cfx.TIEN_TE}} for r in j["dong"]]
    bang = h.cfx.kiem(dong, thang_dau=h.THANG_DAU_FX, nguon="ix_fx.json")
    can_ky = len(bang.ky) - len(bang.lac)
    assert bang.lac and can_ky > 0, (len(bang.ky), bang.lac)            # Đ3: có tháng lạc, có tháng cần ký
    m = re.search(r"<!--ky:so_thang-->(\d+) tháng cần ký", van)
    assert m and int(m.group(1)) == can_ky, (m and m.group(1), can_ky)
    assert f"{can_ky}/{can_ky} tháng đã ký" in van
    hang = [l for l in van.splitlines() if re.match(r"\| \*\*U\d+\*\*", l)]
    assert [re.match(r"\| \*\*(U\d+)\*\*", l).group(1) for l in hang] == [f"U{k}" for k in range(1, len(hang) + 1)]   # đánh số liền


def test_UAT_doi_mot_con_so_thi_bai_DO__D5():
    """Cổng phải ĐỎ cả hai chiều: sửa một số trong tài liệu (±1) ⇒ phát hiện; sửa trong tệp cổng ⇒ cũng phát hiện."""
    d = json.loads(JSON.read_text(encoding="utf-8"))
    van = DOC.read_text(encoding="utf-8")
    sua = van.replace("<!--hd2:WP-C2.tong_o-->63.016", "<!--hd2:WP-C2.tong_o-->63.017")
    assert sua != van
    sai = [(g, k) for g, k, doc in re.findall(r"<!--hd2:([A-Za-z0-9-]+)\.(\w+)-->([0-9.]+)", sua) if doc != _vn(_mong(d, g, k))]
    assert sai == [("WP-C2", "tong_o")]
    d2 = json.loads(JSON.read_text(encoding="utf-8"))
    d2["WP-C3d"]["khop"] += 1
    sai2 = {(g, k) for g, k, doc in _the() if doc != _vn(_mong(d2, g, k))}
    assert sai2 == {("WP-C3d", "khop"), ("WP-C3d", "lech"), ("WP-C3", "khop"), ("WP-C3", "lech")}


def test_UAT_co_du_muc_AC4_va_gioi_han_O6():
    van = DOC.read_text(encoding="utf-8")
    for can in ("đăng nhập", "Ký tháng", "chạy chuỗi", "4 thẻ", "Ký bản", "605", "615", "D3", "CHECK IX.PL", "O6", "Người test", "ĐẠT / ĐỎ", "Ghi chú"):
        assert can.lower() in van.lower() or can in van, can
    # bảng bước: mỗi hàng có đủ 7 ô và ô "Mong" ⛔ rỗng
    hang = [l for l in van.splitlines() if re.match(r"\| \*\*U\d+\*\*", l)]
    assert len(hang) >= 14, len(hang)
    for l in hang:
        o = [c.strip() for c in l.strip().strip("|").split("|")]
        assert len(o) == 7 and o[2], (l[:80], len(o))
        assert o[3] == o[4] == o[5] == o[6] == "", l[:60]      # ô người test/ngày/ĐẠT-ĐỎ/ghi chú để TRỐNG — người test điền


def test_UAT_khong_chua_thu_cam_va_nhan_dem_gi():
    van = DOC.read_text(encoding="utf-8")
    assert not re.search(r"postgresql://\S+:\S+@", van) and "MKGIA" not in van
    assert "thu@apero.vn" in van and "⛔" in van          # nêu tên mặc định để CẤM, ⛔ dùng
    # Đ4: bảng U3 nói "ô" đếm gì
    assert "ô đáp án so được" in van
    # bảng markdown: không `|` trần trong ô (CLAUDE.md · Bẫy) — số ô mỗi hàng bảng U3 cố định 4
    u3 = [l for l in van.split("### Bảng U3")[1].splitlines() if l.startswith("| ") and "---" not in l][1:]
    assert u3 and all(len(l.strip().strip("|").split("|")) == 4 for l in u3)
