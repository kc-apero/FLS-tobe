"""Cong CAU TRUC cho mui thu luoi `F02` (`GAP-SCR-03`).

⛔⛔ **Doc cai nay truoc khi tin bo bai duoi.** Bo bai nay kiem **CAU TRUC** cua
tep sinh ra, ⛔ **KHONG kiem HANH VI**: no chung minh *"moc cho hanh vi so 3 co
mat trong tep"*, ⛔ khong chung minh *"keo xuong chay dung"*. Muon cai sau thi
phai co mot trinh duyet, va o may nay ⛔ khong co.

★ Vay tai sao van viet? Vi cai no chan duoc la co that va da tung xay ra o cho
khac: **mot tep sinh ra thieu han mot hanh vi ma khong ai thay**. Tam hanh vi
`BA-06` §1 la *"danh sach nghiem thu CUNG"* — thieu mot dong la ke toan ve Sheets.
Neu chi co mot cau *"toi da lam ca 8"* trong bao cao thi lan sau sua tool, mot
hanh vi rung ra va bao cao van noi 8.

⇒ Cong nay noi duoc dung mot cau, va no la cau that: **ca 8 hanh vi deu co moc
mang ten trong tep, va 10 cot sua duoc la 10 cot dung**.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys

import pytest

from fls.repo.ghi_tay import TRUONG_GHI

pytestmark = pytest.mark.pg          # can kho de lay du lieu that

GOC = pathlib.Path(__file__).resolve().parents[2]
TOOL = GOC / "tools" / "mui_thu_luoi.py"


@pytest.fixture(scope="module")
def trang(tmp_path_factory) -> str:
    """Sinh mui thu tu KHO THAT, 40 dong — du de co dong am va o rong."""
    ra = tmp_path_factory.mktemp("mui_thu") / "f02.html"
    r = subprocess.run(
        [sys.executable, str(TOOL), "--dong", "40", "--ra", str(ra)],
        cwd=GOC, capture_output=True, text=True, encoding="utf-8",
        env={**__import__("os").environ, "PYTHONUTF8": "1"})
    assert r.returncode == 0, r.stdout + r.stderr
    return ra.read_text(encoding="utf-8")


# ───────────────────────────────────────── tam hanh vi §1
def test_1_dieu_huong_ban_phim__ca_nam_phim(trang):
    for k in ("ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", "Enter", "Tab"):
        assert k in trang, f"thieu phim {k}"


def test_2_dan_mot_vung__tach_ca_tab_LAN_newline(trang):
    """Dan mot vung nghia la tach **hai** chieu. Tach mot chieu la dan mot cot."""
    assert "'paste'" in trang
    assert r"split('\t')" in trang, "⛔ khong tach theo TAB ⇒ chi dan duoc 1 cot"
    assert r"split('\n')" in trang, "⛔ khong tach theo dong ⇒ chi dan duoc 1 dong"


def test_3_keo_xuong(trang):
    assert "'d'" in trang and "o_tai(r-1, c)" in trang, \
        "⛔ keo xuong phai lay gia tri o NGAY TREN"


def test_4_hoan_tac__co_LICH_SU_chu_khong_chi_mot_buoc(trang):
    assert "state.lich.pop()" in trang, "⛔ hoan tac phai co lich su, khong 1 buoc"
    assert "state.lich.push" in trang


def test_5_filter_view__AN_dong_chu_khong_XOA_dong(trang):
    """★ Filter **VIEW**: doi cach nhin, ⛔ khong doi du lieu.

    `style.display` = an. Neu thay bang `remove()` thi do la **xoa dong** — va
    mot luoi ke toan xoa dong khi loc la mot luoi khong ai dam dung.
    """
    assert "tr.style.display" in trang
    assert ".remove()" not in trang, "⛔ filter ⛔ khong duoc XOA dong"


def test_6_dong_cung_CA_tieu_de_VA_cot_khoa__left_la_TONG_DUNG(trang):
    """★★ Day la cho `BA-06` §6b goi la **yeu nhat** cua bang tran.

    ⛔ `left` ⛔ khong duoc la mot **uoc luong** be rong: uoc sai thi hai cot
    dong cung **de len nhau**. Nen tep phai khai `width` cu the, va `left` cua
    cot thu n phai bang **tong** be rong cua n-1 cot truoc — bai nay cong lai
    va so, ⛔ khong tin con so trong tep.
    """
    assert "position:sticky; top:0" in trang, "⛔ tieu de ⛔ khong dong cung"
    cap = re.findall(r"left:(\d+)px; width:(\d+)px", trang)
    assert len(cap) >= 3, f"phai co >= 3 cot dong cung, thay {len(cap)}"
    x = 0
    for left, rong in cap:
        assert int(left) == x, (
            f"⛔ `left`={left} nhung tong be rong cac cot truoc = {x} ⇒ hai cot "
            f"dong cung SE DE LEN NHAU")
        x += int(rong)


def test_7_so_kieu_ke_toan__tabular_nums_va_am_MAU_DO(trang):
    assert "tabular-nums" in trang, "⛔ so khong thang cot thi khong liec ra duoc"
    assert "td.am" in trang and "--do" in trang, "⛔ so am phai do"
    # phan nhom nghin phai co THAT trong du lieu, ⛔ khong chi co luat CSS
    assert re.search(r">[\d]{1,3}(,\d{3})+\.\d{2}<", trang), \
        "⛔ khong o tien nao duoc phan nhom nghin ⇒ luat dinh dang khong chay"


def test_8_luu_khong_can_bam__gom_lo_va_KHONG_co_nut_Luu(trang):
    assert "setTimeout" in trang and "clearTimeout" in trang, \
        "⛔ khong hen lai dong ho ⇒ ghi tung o mot, dung cai bi cam"
    assert "2500" in trang, "⛔ thieu do tre gom lo (~2–3s)"
    assert not re.search(r"<button[^>]*>\s*L[uư]u", trang, re.I), \
        "⛔ co nut Luu = da thua (Sheets khong co nut Luu)"


# ───────────────────────────────────────── cot sua duoc
def test_dung_7_cot_sua_duoc__khong_5_khong_10(trang):
    """⛔ `BA-06` §6b con ghi *"chi 5 cot sua duoc"*. `QĐ-owner-0824` da mo **10**.

    Bai nay khoa con so vao `TRUONG_GHI` — mot cho khai duy nhat, nen tai lieu
    lech thi tai lieu sai, ⛔ khong phai code sai.
    """
    m = re.search(r"const SUA = new Set\((\[[^\]]*\])\)", trang)
    assert m, "⛔ khong tim thay khai bao cot sua duoc"
    trong_trang = set(__import__("json").loads(m.group(1)))
    assert trong_trang <= TRUONG_GHI, f"cot la: {sorted(trong_trang - TRUONG_GHI)}"
    # ⛔⛔ Ban 27/08 chi cho go **5/10**: nam truong `TRUONG_NGOAI` khong nam
    # trong 14 cot hop dong nen luoi ⛔ khong co cho go chung. Owner bao thieu
    # `Ma doi tac` + `Hoa don` (28/08) — va do ra la thieu **nam**. Bai nay
    # ⛔⛔ 10 -> **7** ngay 2026-08-28 (`QĐ-ITL-64`): owner tra loi ke toan
    # ⛔ KHONG sua vung ALLOCATE. Ba cot ay nay CHI-DOC tren luoi.
    # Bai nay khoa lai: luoi phai go duoc **CA BAY**, khong thi mui thu ⛔
    # khong test duoc chinh nhung truong ma nguoi go nhieu nhat.
    assert trong_trang == TRUONG_GHI, (
        f"thieu cho go: {sorted(TRUONG_GHI - trong_trang)}")


def test_o_CHI_DOC_khong_bao_gio_mang_lop_sua(trang):
    """⛔ 45/55 cot la chi-doc. Mot o chi-doc ma go duoc la mot o sua sai so."""
    for o in re.findall(r'<td class="([^"]*)" data-cot="(canon\.[^"]+)"', trang)[:200]:
        assert "sua" not in o[0], f"o canon {o[1]} mang lop `sua`"


def test_tep_TU_CHUA__khong_mang_khong_thu_vien(trang):
    """★ Mui thu phai mo duoc o may khong co mang — ⛔ khong `http`, ⛔ khong CDN."""
    for xau in ("http://", "https://", "<script src", "<link "):
        assert xau not in trang, f"tep goi ra ngoai: {xau!r}"
