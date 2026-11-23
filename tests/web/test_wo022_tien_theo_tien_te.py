# -*- coding: utf-8 -*-
"""`WO-022` — in tiền theo tiền tệ *(`BA-06` **v4.12** `UI-F10` + §5b ⓐ…ⓗ)*.

⛔⛔ **Vì sao tệp này tồn tại — lỗi ĐÃ ĐO, ⛔ không phải lo xa** *(`KQ-021`
`F-3`, máy `8099` ca **U**)*: `TP.tien` gọi `toLocaleString('vi-VN',
{maximumFractionDigits: 0})` cho **mọi** tiền tệ ⇒ chùm USD `1234.56` +
`765.44` in **`1.235 USD`** · **`765 USD`**. Sổ thật *(đo 02/10, chỉ `SELECT`)*:
**2.413 / 3.980** dòng USD mang phần lẻ — tức **đa số** dòng ngoại tệ in sai, trái
thẳng `QĐ-ITL-62` *("ngoại tệ ⛔ dung sai, dù vài xu")*. Và hai lỗi **tính**:
Σ `0.10 + 0.20` trừ `0.30` ra `5,55·10⁻¹⁷` ⇒ hộp ghép nhiều dòng `F01` **khoá nút
Ghép** trên một chùm khớp đúng từng xu; lệch `−0,40 USD` in thành **`-0`**.

⭐ Mọi bài nạp tệp **THẬT** *(`thanh_phan.js`, `hop_thoai.js`, màn)* — ⛔ định
nghĩa `TP.tien` giả *(bài học `11` §6 + `KQ-019`: khuôn thử tự nhét che chỗ bản
thật hỏng)*. Chiều ĐỎ của từng bài ghi ở docstring và **đã chạy thật** trên
`thanh_phan.js` của `5f8796b` *(trước mã của phiếu — `BG`)*.
"""
from __future__ import annotations

import json
import os
import re

import pytest

from fls.web import phuc_vu as pv
from tests.web.khung_node import _chay, _VE, can_node
from tests.web.test_drawer_f02 import _BAM, _DAT_CUA
from tests.web.test_js_chay_duoc import _chay as _chay_thuan
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01
from tests.web.test_wo008_v2_nam_ca_bo_gan import DEM_HOP
# ⭐ `WO-022` vòng 3 *(`AC-17`)*: bài `AC-6` hộp *Tìm tiền* dựng thân từ CỬA
#   THẬT trên kho TEST — khuôn dựng chung ở tệp vòng 3.
from tests.web.test_wo022_v3_tim_tien_cua_that import (  # noqa: F401
    ca_cua_that, conn, may, mo_hop, tien_usd)

# ═══ AC-1 · hàm thuần — 12 ca, chữ ra ĐÚNG TỪNG BYTE ═══════════════════════
#: ⭐ Nguyên văn bảng `AC-1` của `WO-022` *(⛔ thêm, ⛔ bớt một ca)*.
CA_AC1 = [
    (("1234.56", "USD"), "1.234,56"),
    (("1234", "USD"), "1.234,00"),
    (("765.44", "USD"), "765,44"),
    (("0.01", "USD"), "0,01"),
    (("-0.40", "USD"), "-0,40"),
    (("12.5", "SGD"), "12,50"),
    (("1565307.14", "HKD"), "1.565.307,14"),
    (("39457436", "VND"), "39.457.436"),
    # §5b ⓑ — mặc định `Q-TIEN-1` *(owner chưa trả lời ⇒ in ĐỦ)*
    (("1306103.80", "VND"), "1.306.103,80"),
    # §5b ⓒ — mã lạ: ⛔ đoán là VND/USD. ⭐ Ca thứ 10 ĐỔI theo `AC-13` của
    # `WO-022` vòng 2 *(`BA-06` v4.13 ⓒ viết lại — `TL-026`, yếu #1 của
    # `BG-027`)*: ~~`100,5`~~ *(v4.11–v4.12: cắt số 0 đuôi)* ⇒ `100,50` *(một
    # luật số lẻ cho mọi mã — có lẻ ngoài bảng in đủ thang kho 2)*. Lo gốc
    # của ca giữ nguyên: mã lạ ⛔ bị đoán là VND *(in `101`/`100`)* hay USD.
    (("100.50", "20"), "100,50"),
    (("100", None), "100"),
    (("", "USD"), "—"),
]


@can_node
def test_AC1_tien_MUOI_HAI_ca_dung_tung_byte():
    """⛔ Chiều ĐỎ *(đã chạy trên `5f8796b`)*: hàm cũ `maximumFractionDigits: 0`
    ⇒ **9/12** ca đỏ *(mọi ca có lẻ + `1234 USD` + mã lạ `100.50` in `101`)*
    — `WO` đòi ≥ 6. Bỏ số lẻ cố
    định ⇒ `1.234,00` đỏ; làm tròn VND ⇒ `1.306.103,80` đỏ; đoán mã lạ là VND ⇒
    `100,50` đỏ *(ca thứ 10 đổi theo `AC-13` vòng 2 — chú thích tại ca)*."""
    ra = _chay_thuan(["thanh_phan.js"], "[" + ",".join(
        "TP.tien(%s, %s)" % (json.dumps(v), json.dumps(c))
        for (v, c), _m in CA_AC1) + "]")
    sai = [(CA_AC1[i][0], CA_AC1[i][1], ra[i]) for i in range(len(CA_AC1))
           if ra[i] != CA_AC1[i][1]]
    assert len(ra) == 12, f"⛔ không đo được: {len(ra)} ca"
    assert sai == [], "⛔ (vào, mong, ra): " + repr(sai)


@can_node
def test_AC1_SO_LE_khai_MOT_cho_dung_nam_ma_va_KHOA():
    """§5b ⓐ: bảng **một chỗ** *(hằng)* — `VND 0` · `USD/SGD/HKD/EUR 2`; ⛔ ai
    sửa được bảng lúc chạy *(sửa ở một màn là hai màn in hai kiểu)*."""
    ra = _chay_thuan(["thanh_phan.js"], """(() => {
      const truoc = JSON.stringify(TP.SO_LE);
      try { TP.SO_LE.VND = 2; } catch (e) {}
      return {bang: TP.SO_LE, dong_bang: Object.isFrozen(TP.SO_LE),
              van: JSON.stringify(TP.SO_LE) === truoc};
    })()""")
    assert ra["bang"] == {"VND": 0, "USD": 2, "SGD": 2, "HKD": 2, "EUR": 2}
    assert ra["dong_bang"] and ra["van"], ra


@can_node
def test_AC1_ma_tien_te_viet_THUONG_hay_CO_KHOANG_van_la_ma_ay():
    """Sao kê `F04` chở chuỗi `Currency` **nguyên văn** nguồn *(`' usd'`)* —
    ⛔ coi là mã lạ thì một USD lại in `1.234,5`."""
    ra = _chay_thuan(["thanh_phan.js"],
                     "[TP.tien('1234.5', ' usd'), TP.tien(66923.25, 'USD'),"
                     " TP.tien(1240000000, 'VND')]")
    assert ra == ["1.234,50", "66.923,25", "1.240.000.000"], ra


@can_node
def test_AC1_chuoi_KHONG_phai_so_tra_NGUYEN_VAN_da_thoat():
    """Hành vi cũ giữ: ô sao kê thô ⛔ là số ⇒ in nguyên văn **đã thoát** —
    ⛔ `NaN`, ⛔ đoán."""
    ra = _chay_thuan(["thanh_phan.js"],
                     "[TP.tien('1,234.56', 'USD'), TP.tien('<b>', 'USD'),"
                     " TP.tien(null, 'USD'), TP.tien(undefined, 'VND')]")
    assert ra == ["1,234.56", "&lt;b&gt;", "—", "—"], ra


# ═══ §5b ⓕ · số nguyên XU — đổi chuỗi bằng TÁCH CHUỖI, ⛔ `Number * 100` ═══
@can_node
def test_xu_TACH_CHUOI_khong_nhan_so_thuc():
    """⛔ `Number('1.005') * 100 = 100,49999…` · `4.35 * 100 = 434,99999…` *(Rủi
    ro ② của `WO`)*. Làm tròn **một lần**, nửa ra xa 0.

    ⛔ Chiều ĐỎ: viết `Math.round(Number(v) * 100)` ⇒ `1.005` ra `100` ⇒ ĐỎ."""
    ra = _chay_thuan(["thanh_phan.js"], """[
      TP.xu('1.005'), TP.xu('4.35'), TP.xu('-0.40'), TP.xu('1234.56'),
      TP.xu('0.10') + TP.xu('0.20') - TP.xu('0.30'),
      TP.xu('11742361787.00'), TP.xu(''), TP.xu('abc'), TP.xu(null),
      TP.xu('617.285', 'san'), TP.xu('-1.005'), TP.xu(66923.25),
      TP.chuoi_xu(-40), TP.chuoi_xu(5), TP.chuoi_xu(123456), TP.chuoi_xu(0)
    ]""")
    assert ra == [101, 435, -40, 123456, 0, 1174236178700, None, None, None,
                  61728, -101, 6692325,
                  "-0.40", "0.05", "1234.56", "0.00"], ra


@can_node
def test_xu_VUOT_thang_an_toan_tra_NULL_khong_tinh_sai():
    """`Number` nguyên an toàn tới `9·10^15` xu. Vượt ⇒ `null` *(⛔ tính được)*,
    ⛔ một số sai lặng lẽ. Thang `numeric(20,2)` cho phép 18 chữ số nguyên."""
    ra = _chay_thuan(["thanh_phan.js"],
                     "[TP.xu('123456789012345678.00'), TP.xu('90000000000000.00')]")
    assert ra == [None, 9000000000000000], ra


@can_node
def test_in_tien_so_RAT_LON_van_tach_chuoi_khong_mat_chu_so():
    """In ⛔ đi qua `Number` ⇒ 18 chữ số nguyên vẫn đúng từng chữ."""
    ra = _chay_thuan(["thanh_phan.js"],
                     "TP.tien('123456789012345678.91', 'USD')")
    assert ra == "123.456.789.012.345.678,91", ra


# ═══ AC-2 · MỌI lời gọi `TP.tien(` có ĐÚNG 2 đối số ═══════════════════════
#: ⭐ Danh sách lời gọi mà đối số thứ hai là **`null` tường minh** — `BG` liệt
#: kê đúng danh sách này. Rỗng: cả 6 màn đều **có** mã tiền tệ tại chỗ gọi
#: *(`F04` xem trước truyền chính ô `Currency` của dòng sao kê — ô ấy rỗng thì
#: hàm đi nhánh §5b ⓒ, cùng chỗ với `null`)*.
GOI_NULL_TUONG_MINH: list[str] = []

THU_MUC = pv.THU_MUC


def _bo_chu_thich_va_chuoi(ma: str) -> str:
    """Thay nội dung chuỗi + chú thích bằng khoảng trắng *(giữ độ dài)*.

    ⛔ Regex một dòng ⛔ đủ *(`WO` `AC-2`)*: lời gọi xuống dòng, và một dấu
    `,` / `)` nằm TRONG chuỗi *('Nợ ' + …)* sẽ bị đếm nhầm thành đối số."""
    ra, i, n = [], 0, len(ma)
    while i < n:
        c = ma[i]
        if ma.startswith("//", i):
            j = ma.find("\n", i)
            j = n if j < 0 else j
            ra.append(" " * (j - i)); i = j
        elif ma.startswith("/*", i):
            j = ma.find("*/", i + 2)
            j = n if j < 0 else j + 2
            ra.append(re.sub(r"[^\n]", " ", ma[i:j])); i = j
        elif c in "'\"`":
            j = i + 1
            while j < n and ma[j] != c:
                j += 2 if ma[j] == "\\" else 1
            ra.append(c + " " * (j - i - 1) + c); i = j + 1
        elif c == "/" and ("".join(ra[-40:]).rstrip()[-1:] or "(") in "(,=:!&|?{};":
            # literal regex *(`/\/chum$/`)* — bỏ qua tới dấu `/` đóng
            j = i + 1
            while j < n and ma[j] != "/" and ma[j] != "\n":
                j += 2 if ma[j] == "\\" else 1
            ra.append(" " * (j - i + 1)); i = j + 1
        else:
            ra.append(c); i += 1
    return "".join(ra)


def dem_loi_goi(ma: str, ten: str = "TP.tien(") -> list[tuple[int, list[str]]]:
    """Mọi lời gọi `ten` ⇒ `(dòng, [đối số nguyên văn])`, đếm theo NGOẶC."""
    sach = _bo_chu_thich_va_chuoi(ma)
    ra = []
    for m in re.finditer(re.escape(ten), sach):
        i = m.end()
        sau, doi, dau = 1, [], i
        while sau:
            c = sach[i]
            if c in "([{":
                sau += 1
            elif c in ")]}":
                sau -= 1
            elif c == "," and sau == 1:
                doi.append(ma[dau:i].strip()); dau = i + 1
            i += 1
        cuoi = ma[dau:i - 1].strip()
        if cuoi or doi:
            doi.append(cuoi)
        ra.append((ma.count("\n", 0, m.start()) + 1, doi))
    return ra


def _moi_loi_goi() -> dict[str, list[tuple[int, list[str]]]]:
    ra = {}
    for ten in sorted(os.listdir(THU_MUC)):
        if ten.endswith(".js"):
            with open(os.path.join(THU_MUC, ten), encoding="utf-8") as f:
                ra[ten] = dem_loi_goi(f.read())
    return ra


def test_AC2_MOI_loi_goi_TP_tien_co_DUNG_hai_doi_so():
    """⛔ Chiều ĐỎ *(đã chạy trên `5f8796b`)*: **40/40** lời gọi một đối số ⇒
    ĐỎ. Thêm **một** lời gọi một đối số ⇒ ĐỎ *(bài `…_CAN_dung_ca_ma_xuong_dong`)*;
    xoá hết ⇒ mẫu số 0 ⇒ ĐỎ.

    ⚠ `Đ4`: `WO` ghi **38** — đó là số **DÒNG** có `TP.tien(` *(`grep -c`)*.
    Số **LỜI GỌI** là **40**: `man_f01_lenh.js:654` và `man_f02.js:1127` mỗi
    dòng mang hai lời."""
    goi = _moi_loi_goi()
    tong = sum(len(v) for v in goi.values())
    assert tong >= 38, f"⛔ không đo được: chỉ {tong} lời gọi `TP.tien(`"
    sai = [(t, d, a) for t, v in goi.items() for d, a in v if len(a) != 2]
    assert sai == [], "⛔ (tệp, dòng, đối số) ≠ 2: " + repr(sai)
    tep_man = {t for t, v in goi.items() if v}
    assert tep_man == {"man_f01.js", "man_f01_ghep.js", "man_f01_lenh.js",
                       "man_f02.js", "man_f03.js", "man_f04.js"}, tep_man
    null_ = sorted(f"{t}:{d}" for t, v in goi.items() for d, a in v
                   if a[1] == "null")
    assert null_ == sorted(GOI_NULL_TUONG_MINH), null_


def test_AC2_may_dem_CAN_dung_ca_ma_xuong_dong_va_dau_phay_trong_chuoi():
    """⭐ Cổng mới phải được **chứng minh ĐỎ** *(`Đ5`)*: máy đếm bắt một lời
    gọi một đối số kể cả khi xuống dòng, ⛔ đếm nhầm `,` trong chuỗi / chú
    thích, ⛔ đếm `TP.tien(` trong chú thích; tập rỗng ⇒ 0 lời."""
    ma = ("a(TP.tien(x));\n"
          "b(TP.tien(\n  r.ps_no,\n  r.curr) + ' Có, ' + TP.tien(y,\n z));\n"
          "c(TP.tien(f(a, b)));  // TP.tien(1, 2, 3)\n"
          "/* TP.tien(q) */ d(TP.tien('a,b)', c));\n"
          "e(TP.tien(v.replace(/[,)]/g, ''), k));\n")
    ra = dem_loi_goi(ma)
    assert [len(a) for _d, a in ra] == [1, 2, 2, 1, 2, 2], ra
    assert [d for d, _a in ra] == [1, 2, 4, 6, 7, 8], ra
    assert dem_loi_goi("const a = 1;") == []


# ═══ AC-4 · Σ và lệch trên số nguyên xu — hộp ghép nhiều dòng `F01` ═══════
TEP_F01_HOP = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
               "man_f01.js"]


def _hop_ghep_nhieu_dong(chon: list[str], bank: str, curr: str = "USD",
                         ds: str = "0") -> dict:
    """Mở hộp `Ghép lệnh` THẬT của `F01` *(`_drawer_ghep`)* rồi **tích** các
    dòng lệnh `chon`.

    ⚠ DOM giả **⛔ phân tích HTML** *(đầu `dom_gia.js`)*: thân hộp đi qua
    `innerHTML` ⇒ ô tích và `#sig` ⛔ thành thẻ. Bài dựng **đúng** ba thứ màn
    đọc *(`#sig` · ô tích con của `#dlg-b` mang `type`/`checked`/`data-a`)*
    bằng `createElement`, rồi phát sự kiện `change` **qua chính người nghe màn
    gắn trên `#dlg-b`**. Nút `Ghép` là nút **thật** `HT.mo` dựng.
    """
    uv = [{"pm_line_id": "PWU-%d" % i, "amount": a, "curr": curr, "bac": "tien",
           "status": "Approve", "da_ghep": 0} for i, a in enumerate(chon)]
    tra = {"/queue/77/pm-candidates": {"data": {
        "dong_so": {"itl_id": 77, "tien": bank, "curr": curr},
        "dung_sai": ds, "ung_vien": uv, "khong_xep_duoc_theo": [],
        "anh_chup": {"so_dong": 2, "doc_luc_muon_nhat": "2026-10-02T10:00"}}}}
    return _chay("".join("_TRA[%s] = %s;\n" % (json.dumps(k), json.dumps(v))
                         for k, v in tra.items()) + """
      const sig = document.createElement('div'); sig.id = 'sig';
      document.body.appendChild(sig);
      await F01._drawer_ghep({itl_id: 77, memo: 'chi USD'});
      const b = document.getElementById('dlg-b');
      const tich = %s;
      tich.forEach((a, i) => {
        const c = document.createElement('input');
        c.type = 'checkbox'; c.checked = true; c.dataset.a = a;
        c.dataset.i = String(i); b.appendChild(c);
      });
      if (typeof b.onchange === 'function') b.onchange({target: b});
      (b._nghe.change || []).forEach(f => f({target: b}));
      const nut = document.getElementById('dlg-f').children
        .filter(x => x.tagName === 'BUTTON');
      return {sig: sig.innerHTML, lop: sig.className,
              ghep_khoa: nut[nut.length - 1].disabled,
              ten_nut: nut.map(x => x.textContent)};
    """ % json.dumps(chon), tep=TEP_F01_HOP, vo=VO_F01)


@can_node
def test_AC4_F01_khop_DUNG_tung_xu_0_10_cong_0_20_bang_0_30__nut_Ghep_MO():
    """⛔ Chiều ĐỎ *(đã chạy trên `5f8796b`)*: cộng `Number` ⇒ lệch
    `5,55·10⁻¹⁷` > dung sai `0` ⇒ chip `crit`, nút Ghép **khoá** ⇒ ĐỎ."""
    r = _hop_ghep_nhieu_dong(["0.10", "0.20"], "0.30")
    assert r["ten_nut"] == ["Thôi", "Ghép"], r
    assert "khớp — cho ghép" in r["sig"], r["sig"]
    assert "note ok" in r["lop"], r
    assert r["ghep_khoa"] is False, "⛔ nút Ghép KHOÁ trên một chùm khớp đúng xu"
    assert "lệch <b class=\"num\">0,00</b>" in r["sig"], r["sig"]
    assert "Σ dòng lệnh <b class=\"num\">0,30</b>" in r["sig"], r["sig"]


@can_node
def test_AC4_F01_lech_0_40_in_0_40__KHONG_in_0_hay_am_0():
    """⛔ Chiều ĐỎ: in lệch bằng hàm cũ ⇒ `0` *(hay `-0`)* ⇒ ĐỎ."""
    r = _hop_ghep_nhieu_dong(["1234.56"], "1234.16")
    assert "lệch <b class=\"num\">0,40</b>" in r["sig"], r["sig"]
    assert "lệch <b class=\"num\">0</b>" not in r["sig"]
    assert "-0<" not in r["sig"], r["sig"]
    assert "⛔ lệch quá dung sai" in r["sig"] and "crit" in r["lop"], r
    assert r["ghep_khoa"] is True, r
    assert "1.234,56" in r["sig"] and "1.234,16" in r["sig"], r["sig"]


@can_node
def test_AC4_F01_lech_AM_0_40_giu_dau_am():
    """§5b ⓓ: dấu âm **⛔ đổi** — Σ < bank in `-0,40`."""
    r = _hop_ghep_nhieu_dong(["1234.16"], "1234.56")
    assert "lệch <b class=\"num\">-0,40</b>" in r["sig"], r["sig"]
    assert r["ghep_khoa"] is True


@can_node
def test_AC4_F01_dung_sai_VND_so_TOI_DA_la_san_khong_lam_tron_len():
    """⛔ Dung sai tay = `min(1.000 đ, 0,5% × tiền bank)` *(`QĐ-ITL-63`)* có thể
    mang **nhiều** chữ số lẻ *(`617.285`)*. Đổi sang xu bằng **làm tròn** cho
    `61729` ⇒ màn **cho** ghép một lệch `617,29` mà cửa ghi **từ chối**
    *(`617,29 > 617,285`)*. ⇒ Dung sai đổi xu bằng **SÀN**."""
    r = _hop_ghep_nhieu_dong(["123457.29"], "123457.00", curr="VND",
                             ds="617.285")
    ok = _hop_ghep_nhieu_dong(["617.28"], "0.00", curr="VND", ds="617.285")
    vuot = _hop_ghep_nhieu_dong(["617.29"], "0.00", curr="VND", ds="617.285")
    assert "khớp — cho ghép" in r["sig"], r["sig"]          # lệch 0,29 đ
    assert ok["ghep_khoa"] is False, ok["sig"]
    assert vuot["ghep_khoa"] is True, ("⛔ màn cho ghép một lệch cửa ghi từ "
                                       "chối: " + vuot["sig"])


# ── `ve_tong_chum` — tổng chùm trên màn ghép ─────────────────────────────
TEP_GHEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]


def _tong_chum(so_tien: str, ds: list[str], curr: str = "USD") -> str:
    return _chay("""
      const e = F01G.ve_tong_chum(%s, %s);
      return {chu: e.textContent, lop: e.className};
    """ % (json.dumps({"so_tien": so_tien, "curr": curr}),
           json.dumps([{"amount": a, "curr": curr} for a in ds])),
        tep=TEP_GHEP, vo=VO_F01)


@can_node
def test_AC4_tong_chum_0_10_cong_0_20_KHOP_DUNG_lenh_0_30():
    """⛔ Chiều ĐỎ: cộng `Number` rồi in bằng hàm cũ ⇒ `Tổng … 0 USD` ⇒ ĐỎ."""
    r = _tong_chum("0.30", ["0.10", "0.20"])
    assert r["chu"] == ("Tổng 2 giao dịch: 0,30 USD — khớp đúng số tiền lệnh."), r
    assert "khop" in r["lop"].split(), r


@can_node
def test_AC4_tong_chum_lech_0_40_in_0_40_va_KHONG_khop():
    """⛔ Chiều ĐỎ: so `< 0.005` vẫn bắt lệch, nhưng hàm in cũ ra `0 USD` ⇒
    ĐỎ."""
    r = _tong_chum("1234.16", ["1000.00", "234.56"])
    assert r["chu"] == ("Tổng 2 giao dịch: 1.234,56 USD — lệch 0,40 USD so với "
                        "1.234,16 USD của lệnh."), r
    assert "lech" in r["lop"].split(), r


@can_node
def test_AC3_tong_chum_ca_U_2000_00_USD_khop():
    """Ca **U** đảo chiều *(một lệnh `2000.00` trả bằng hai giao dịch `1234.56`
    + `765.44`)* — `AC-3` ⭐ *"tổng chùm in `2.000,00 USD` + khớp"*."""
    r = _tong_chum("2000.00", ["1234.56", "765.44"])
    assert r["chu"] == "Tổng 2 giao dịch: 2.000,00 USD — khớp đúng số tiền lệnh.", r


@can_node
def test_khop_dung_tien_so_tren_XU_va_null_KHONG_bang_null():
    """`khop_dung_tien` *(phím `Enter` gán ngay)* — so trên xu. ⛔ Hai số tiền
    **thiếu** ⛔ được coi là "khớp đúng tiền" *(`Number(null) === Number(null)`
    ⇒ `true` ở mã cũ)*."""
    ra = _chay("""return [
      F01G.khop_dung_tien({so_tien: '1000.00', curr: 'USD'},
                          {amount: '1000', curr: 'USD'}),
      F01G.khop_dung_tien({so_tien: '1000.00', curr: 'USD'},
                          {amount: '1000.01', curr: 'USD'}),
      F01G.khop_dung_tien({so_tien: null, curr: 'USD'},
                          {amount: null, curr: 'USD'}),
      F01G.khop_dung_tien({so_tien: '5.00', curr: 'USD'},
                          {amount: '5.00', curr: 'SGD'})];""",
               tep=TEP_GHEP, vo=VO_F01)
    assert ra == [True, False, False, False], ra


# ═══ AC-6 · sáu màn — mỗi tệp ≥ 1 bài DOM in USD có lẻ đúng khuôn ⓐ ═══════
#: ⚠ DOM giả: thẻ đã có con thì `textContent` chỉ ghép chữ của **con** —
#: `innerHTML` của chính thẻ *(thẻ `card` của `F01` chân màn)* bị bỏ. Gom cả
#: cây: HTML của thẻ + HTML/chữ mọi con.
CAY = """
  const _cay = e => (e._html || (e.children.length ? '' : e._txt || ''))
                    + e.children.map(_cay).join('');
"""
DONG_USD = [{"ma_lenh": "PWU-1", "noi_dung": "chi USD", "so_tien": "1234.56",
             "curr": "USD", "trang_thai": "chua", "trang_thai_nhan": "chưa gán",
             "trang_thai_mau": "", "loai_phieu": "PM", "ngay": "2026-09-30",
             "cdt": "CVL", "nhom_du_truong": [], "itl_da_gan": [], "gd_ds": []}]


@can_node
def test_AC6_man_f01_ghep_THE_va_RAIL_in_1_234_56_USD():
    """⛔ Chiều ĐỎ: hàm cũ ⇒ `1.235 USD` trên thẻ + rail ⇒ ĐỎ."""
    r = _chay("""
      _TRA['/queue/lenh/PWU-1/itl-candidates'] = {data: {ung_vien: []}};
      F01G.ST.dong = %s;
      await F01G.mo_lenh('PWU-1');
      const goc = document.getElementById('ghep-goc');
      return {the: goc.querySelectorAll('.tien').map(x => x.textContent),
              rail: goc.querySelectorAll('.amt').map(x => x.textContent),
              man: goc.textContent};
    """ % json.dumps(DONG_USD, ensure_ascii=False), tep=TEP_F01, vo=VO_F01)
    assert r["the"] == ["1.234,56 USD"], r["the"]
    assert "1.234,56 USD" in r["rail"], r["rail"]
    assert "1.235 USD" not in r["man"]


@can_node
def test_AC6_man_f01_HANG_CHO_the_tien_te_in_USD_co_le():
    """`F01` chân màn theo từng tiền tệ — Σ USD có lẻ."""
    r = _chay(CAY + """
      _TRA['/queue/summary'] = {data: {theo_tien_te: [
        {curr: 'USD', so_dong: 2, tien: '2000.40'},
        {curr: 'VND', so_dong: 1, tien: '39457436.00'}]}};
      const o = document.createElement('div'); document.body.appendChild(o);
      await F01.ve_tom(o);
      return _cay(o);
    """, tep=TEP_F01_HOP, vo=VO_F01)
    assert "Σ 2.000,40" in r and "Σ 39.457.436<" in r, r


@can_node
@pytest.mark.pg
def test_AC6_man_f01_lenh_CHAN_MAN_va_hop_TIM_TIEN_lech_0_40(ca_cua_that):
    """`F01` lằn **lệnh**: chân màn + hộp *"Tìm tiền"* *(`:653`–`:654` — tiền
    lệnh ↔ tiền bank · lệch)*.

    ⭐⭐ **Viết lại ở `WO-022` vòng 3** *(`AC-17`, `KQ-029` `F-1`)* — **giữ
    nguyên lo gốc**: chân màn in USD **có lẻ**, và lệch `0,40 USD` in `0,40`
    cạnh *"VƯỢT dung sai"*, ⛔ `0`. ⛔ Bản cũ **tự nhét** thân cửa
    `{tien: '1234.16', lech_tuyet_doi: '0.40', memo}` — khuôn cửa ⛔ trả từ
    `23/09` *(cửa trả khuôn `⓵` `BA-07 §4h`: `amount` · `lech` · `dien_giai`)*
    ⇒ bài xanh trong khi trên máy thật hộp in `—` và *"VƯỢT"* cho **mọi** ứng
    viên. Bản này lấy **mọi** thân *(tóm tắt · danh sách lệnh · ứng viên · nhìn
    đủ PM)* từ **cửa thật qua HTTP trên kho TEST** *(`ca_cua_that`)*; ⛔ một
    khoá nào do bài đặt. Tiền ngẫu nhiên mỗi lần *(`<N>.56`/`<N>.16`)* — lý do
    ở docstring tệp `test_wo022_v3_tim_tien_cua_that.py`.

    ⛔ Chiều ĐỎ: ⓐ `Math.abs(Number - Number)` rồi in hàm cũ ⇒ lệch `0` ⇒ ĐỎ
    *(lo gốc vòng 1)*; ⓑ ⭐ màn đọc `u.tien`/`u.lech_tuyet_doi` *(`a69ee92`)* ⇒
    cột Tiền `—`, lệch *"⛔ không tính được"* ⇒ ĐỎ *(đã chạy)*."""
    ca, tra = ca_cua_that
    r = mo_hop(ca, tra, ca["lech"], kich_truoc=CAY + """
      _TRA['/queue/lenh-cho/summary'] = {data: %s};
      const o = document.createElement('div'); document.body.appendChild(o);
      await F01L.ve_tom(o);
      globalThis._tom = _cay(o);
    """ % json.dumps(tra["/queue/lenh-cho/summary"], ensure_ascii=False))
    # Σ USD của ảnh PM hiệu lực = hai dòng lệnh của bài `<N>.56` + `10.00`
    assert tien_usd(ca["n"] + 10, "56") in r["tom"], r["tom"]
    assert "0,40" in r["hop"] and tien_usd(ca["n"], "16") in r["hop"], r["hop"]
    assert "lệch <b>0,40</b>" in r["sig"], r["sig"]
    assert ("tiền lệnh <b>" + tien_usd(ca["n"], "56") + "</b>") in r["sig"], r["sig"]
    assert "VƯỢT dung sai" in r["sig"], r["sig"]


@can_node
def test_AC6_man_f02_LUOI_va_PANEL_No_Co_in_USD_co_le():
    """`F02`: ô lưới tiền + dải số tiền panel *(`Nợ/Có` — ca cả hai vế)*.

    ⛔ Chiều ĐỎ: hàm cũ ⇒ `1.235` ⇒ ĐỎ."""
    from tests.web.khung_node import DONG
    g = dict(DONG[0], curr="USD", ps_no=None, ps_co="1234.56")
    hai = dict(DONG[0], curr="USD", ps_no="100.50", ps_co="0.25")
    luoi = _chay("F02.ST.che_do = 'go';" + _VE + """
      return than.rows[0].cells.map(c => c.textContent);
    """, dong=[g])
    assert "1.234,56" in luoi, luoi
    panel = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('#so-dai-tien').textContent;
    """, dong=[g])
    assert "−1.234,56" in panel and "USD" in panel, panel
    doi = _chay(_DAT_CUA + _VE + _BAM + """
      return document.querySelector('#so-dai-tien').textContent;
    """, dong=[hai])
    assert "Nợ 100,50 Có 0,25" in doi, doi


@can_node
def test_AC6_man_f03_BANG_THEO_TIEN_TE_in_USD_co_le():
    """`F03` bảng độ phủ theo từng tiền tệ — `Σ tiền chờ`."""
    r = _chay(CAY + """
      _TRA['/queue/coverage'] = {data: {muc_pct: '90', theo_tien_te: [
        {curr: 'USD', so_dong_cho: 3, pct_dong: '1.0', tien_cho: '765.44',
         so_dong_phu: 2, pct_that: '90.1', so_dong_trong_danh_sach: 2}]}};
      const o = document.createElement('div'); document.body.appendChild(o);
      await F03.ve_phu(o);
      return _cay(o);
    """, tep=["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f03.js"])
    assert '<td class="r">765,44</td>' in r, r


@can_node
def test_AC6_man_f04_XEM_TRUOC_in_theo_o_Currency_cua_chinh_dong():
    """`F04` xem trước sao kê: ô `Debit`/`Credit` in theo ô `Currency` **của
    chính dòng ấy** *(`66923.25` USD ⇒ `66.923,25`)*.

    ⛔ Chiều ĐỎ: hàm cũ ⇒ `66.923` ⇒ ĐỎ."""
    from tests.web.test_man_f04_dom import _f04
    ra = _f04("""
      await F04.ve();
      document.querySelector('[data-chup]').cells[4].children[0].onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      const t = document.querySelector('#nap-xem table');
      const th = t.children.filter(c => c.tagName === 'THEAD')[0];
      const b = t.tBodies[0];
      return {cot: th.rows[0].cells.map(c => c.textContent),
              d: b.rows.map(r => r.cells.map(c => c.textContent))};
    """)
    no = [i for i, c in enumerate(ra["cot"]) if c.startswith("Debit")][0]
    co = [i for i, c in enumerate(ra["cot"]) if c.startswith("Credit")][0]
    assert ra["d"][0][no] == "1.240.000.000", ra["d"][0]
    assert ra["d"][1][co] == "66.923,25", ra["d"][1]


# ═══ §5b ⓖ · con số GỬI LÊN CỬA vẫn là chuỗi cửa trả ═══════════════════════
@can_node
def test_hop_F01_gan_data_a_la_CHUOI_CUA_khong_phai_chu_in():
    """⓪ `TP.tien` ⛔ dùng để TÍNH: hộp `F01` gắn `data-a` = **chuỗi cửa**,
    ⛔ chuỗi đã in *(`"1.234,56"` lên cửa là hỏng tiền)*."""
    r = _chay("""
      _TRA['/queue/77/pm-candidates'] = {data: {
        dong_so: {itl_id: 77, tien: '1234.56', curr: 'USD'}, dung_sai: '0',
        ung_vien: [{pm_line_id: 'P-1', amount: '1234.56', curr: 'USD',
                    bac: 'tien'}], khong_xep_duoc_theo: [], anh_chup: null}};
      const sig = document.createElement('div'); sig.id = 'sig';
      document.body.appendChild(sig);
      await F01._drawer_ghep({itl_id: 77, memo: ''});
      return document.getElementById('dlg-b').innerHTML;
    """, tep=TEP_F01_HOP, vo=VO_F01)
    assert 'data-a="1234.56"' in r, r
    assert '<td class="r">1.234,56</td>' in r, r


# ═══ bổ sung sau đột biến — ca mà `Number × 100` LỆCH THẬT ═════════════════
#: ⚠ Đột biến `M8` *(tổng chùm cộng `Number(x) * 100`)* **sống sót** qua ca
#: `0.10 + 0.20`: trong IEEE `0.1 * 100 === 10` và `0.2 * 100 === 20` — tình
#: cờ đúng. Ca dưới thì ⛔: `4.35 * 100 = 434,99999999999994` *(Rủi ro ② của
#: `WO`)* ⇒ Σ `499,99…` ≠ `500` ⇒ "lệch" một chùm khớp đúng xu.
@can_node
def test_bo_sung_tong_chum_4_35_cong_0_65_KHOP_5_00():
    r = _tong_chum("5.00", ["4.35", "0.65"])
    assert r["chu"] == "Tổng 2 giao dịch: 5,00 USD — khớp đúng số tiền lệnh.", r


@can_node
def test_bo_sung_F01_4_35_cong_0_65_bang_5_00__nut_Ghep_MO():
    r = _hop_ghep_nhieu_dong(["4.35", "0.65"], "5.00")
    assert "khớp — cho ghép" in r["sig"] and r["ghep_khoa"] is False, r["sig"]
    assert "lệch <b class=\"num\">0,00</b>" in r["sig"], r["sig"]


@can_node
def test_bo_sung_F04_USD_SO_NGUYEN_in_00_va_ma_viet_thuong():
    """⚠ Đột biến `M12` *(`F04` truyền `null` thay ô `Currency`)* chỉ bị `AC-2`
    bắt: dòng mẫu `66923.25` USD in như nhau ở nhánh mã lạ. Ca phân biệt: USD
    **số nguyên** `5000` ⇒ `5.000,00` *(mã lạ ⇒ `5.000`)*; ô `Currency` viết
    thường có khoảng *(`' usd '`)* vẫn là USD."""
    from tests.web.test_man_f04_dom import _CHUP_MOT, _f04
    chup = json.loads(json.dumps(_CHUP_MOT))
    chup["dong"][1]["o"].update({"Currency": " usd ", "Credit": 5000})
    ra = _f04("""
      await F04.ve();
      document.querySelector('[data-chup]').cells[4].children[0].onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      const t = document.querySelector('#nap-xem table');
      const th = t.children.filter(c => c.tagName === 'THEAD')[0];
      return {cot: th.rows[0].cells.map(c => c.textContent),
              d: t.tBodies[0].rows.map(r => r.cells.map(c => c.textContent))};
    """, **{"/chup/23719?limit=50": chup})
    co = [i for i, c in enumerate(ra["cot"]) if c.startswith("Credit")][0]
    assert ra["d"][1][co] == "5.000,00", ra["d"][1]
