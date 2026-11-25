# -*- coding: utf-8 -*-
"""WO-345 — `tools/do_tren_anh_song.chuyen_huong`: đo HD2 trên ảnh MỚI = chuyển MỌI lần mở `tests/fixture/**/X.json`
sang `X<hậu tố>.json` NẾU có. Bẫy canh: (1) chuyển im lặng ảnh ⛔ có bản mới ⇒ `FileNotFoundError` giả; (2) hậu tố
rỗng (đo ảnh CŨ) mà vẫn chuyển ⇒ "CŨ" thật ra là MỚI; (3) tệp ngoài `tests/fixture` bị chuyển; (4) chuyển mà ⛔ ghi
lại ⇒ BG ⛔ nói được gói đã đọc ảnh nào (Đ4)."""
from __future__ import annotations

import json
from pathlib import Path

from tools import do_tren_anh_song as t

GOC = Path(__file__).resolve().parents[1]
CO_MOI = GOC / "tests" / "fixture" / "dau_vao" / "ccr_so_du_ccr.json"        # có `_20261123` (WO-345)
KHONG_MOI = GOC / "tests" / "fixture" / "dap_an" / "gl_406.json"              # ≡ ⇒ ⛔ có tệp mới


def _ck(p) -> str:
    with open(p, encoding="utf-8") as f:
        return json.load(f)["checksum_noi_dung"]


def test_chuyen_khi_co_anh_moi_va_ghi_lai():
    da: dict[str, str] = {}
    with t.chuyen_huong("_20261123", da):
        moi = _ck(CO_MOI)
        moi_path = _ck(Path(CO_MOI))
        cu_khac = _ck(KHONG_MOI)
    assert moi == moi_path == "89b8fafe" + moi[8:] and moi != _ck(CO_MOI)
    assert da == {"dau_vao/ccr_so_du_ccr.json": "dau_vao/ccr_so_du_ccr_20261123.json"}
    assert cu_khac == _ck(KHONG_MOI)                                           # ⛔ bản mới ⇒ đọc ảnh cũ


def test_hau_to_rong_khong_chuyen():
    da: dict[str, str] = {}
    with t.chuyen_huong("", da):
        assert _ck(CO_MOI).startswith("9693d0a5")                             # ảnh CŨ (DT13)
    assert da == {}


def test_tra_nguyen_open_sau_khoi(tmp_path):
    da: dict[str, str] = {}
    with t.chuyen_huong("_20261123", da):
        pass
    assert _ck(CO_MOI).startswith("9693d0a5")
    ngoai = tmp_path / "x.json"
    ngoai.write_text('{"checksum_noi_dung": "ngoai"}', encoding="utf-8")
    (tmp_path / "x_20261123.json").write_text('{"checksum_noi_dung": "sai"}', encoding="utf-8")
    with t.chuyen_huong("_20261123", da):
        assert _ck(ngoai) == "ngoai"                                          # ngoài tests/fixture ⇒ ⛔ chuyển


#: ⭐ `SONG-R1-03` (KQ-347): R1 đọc trường `goi` ở GỐC tệp *(= `WP-C2`)* rồi kết luận *"chỉ có MỘT gói"* — sai cấu
#: trúc: `do_hd2._ghi_cong` giữ WP-C2 ở GỐC *(hợp đồng H4)*, 10 gói kia ở khoá `<gói>`. Vòng sửa sinh lại CẢ 11 bằng
#: `do_hd2.py --goi <g> --dsn <kho TEST đã nạp nền> --ghi` *(bẫy `H14-R2-04`)*: 11/11 `KẾT: ĐẠT`, số **lệch 0** —
#: khác duy nhất 2 chuỗi `truc.nguon_ngay_dau` *(actor nạp IX.PER của kho TEST)* ⇒ giữ tệp. Bài này ghim số khối
#: + `tong_o`/`khop` từng gói *(Đ4: ô so · ô khớp)* để câu "11 gói = `hd2_cong.json`" kiểm được bằng máy.
MONG_HD2_11 = {"WP-C2": (63016, 63016), "WP-C3a": (205175, 205140), "WP-C3b": (11585, 11543),
               "WP-C3c": (888, 835), "WP-C3d": (1289415, 1287624), "WP-C4a": (420, 420), "WP-C4b": (1981, 1981),
               "WP-C4c": (19894, 19591), "WP-C5a": (45674, 40556), "WP-C5b": (4102, 3179), "WP-C5c": (86150, 77663)}   # WO-353 — 22/11: 77672


def test_SONG_R1_03_hd2_cong_du_11_khoi_dat_va_so_ghim():
    d = json.loads((t.GOC / "docs" / "ITL" / "_tools" / "hd2_cong.json").read_text(encoding="utf-8"))
    khoi = {"WP-C2": d, **{k: v for k, v in d.items() if k.startswith("WP-")}}
    assert d["goi"] == "WP-C2" and tuple(sorted(khoi)) == tuple(sorted(t.GOI)) and len(khoi) == 11
    for g, (tong, khop) in MONG_HD2_11.items():
        b = khoi[g]
        assert b["goi"] == g and b["dat"] is True and (b["tong_o"], b["khop"]) == (tong, khop), g
        assert tong > 0                                                      # Đ3: mẫu số ≠ 0
