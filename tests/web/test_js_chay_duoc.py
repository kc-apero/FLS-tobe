"""⛔ Cong: ma man hinh phai CHAY DUOC, ⛔ khong chi "trong dung".

⛔⛔ **Vi sao cong nay ton tai.** Moi bai kiem khac o `tests/web/` doc ma man
hinh nhu **van ban**. Mot dau ngoac thieu se qua het chung — roi ke toan mo man
va thay **mot trang trang tron**, ⛔ khong mot cau bao loi nao. Do la lop hong
te nhat: no ⛔ khong keu.

★ Dung `node` de ⓐ kiem cu phap moi tep, va ⓑ **chay that** cac ham thuan
*(⛔ khong cham DOM)* roi soi ket qua. ⛔ Bo qua neu may ⛔ khong co `node` —
nhung ⛔ khong am tham: bai se bao **skip**, chu ⛔ khong xanh gia.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess

import pytest

from fls.web import phuc_vu as pv

NODE = shutil.which("node")
can_node = pytest.mark.skipif(
    NODE is None, reason="⛔ may ⛔ khong co `node` — cong nay BO QUA, ⛔ khong dat")

TEP_JS = sorted(t.ten for t in pv.BANG_TEP
                if t.ten.endswith(".js") and not t.sinh)


def _node(ma: str) -> str:
    r = subprocess.run([NODE, "--input-type=module", "-e", ma],
                       capture_output=True, text=True, encoding="utf-8",
                       cwd=pv.THU_MUC, timeout=60)
    assert r.returncode == 0, f"⛔ node NO:\n{r.stderr}"
    return r.stdout


# ── ⓐ cu phap ─────────────────────────────────────────────────────────────
@can_node
@pytest.mark.parametrize("ten", TEP_JS)
def test_cu_phap_khong_hong(ten):
    r = subprocess.run([NODE, "--check", os.path.join(pv.THU_MUC, ten)],
                       capture_output=True, text=True, encoding="utf-8",
                       timeout=60)
    assert r.returncode == 0, f"⛔ {ten} loi cu phap:\n{r.stderr}"


@can_node
def test_cong_DO_khi_ma_hong(tmp_path):
    """⛔ Cong chua tung thay do la cong chua biet co song."""
    t = tmp_path / "hong.js"
    t.write_text("function a( { return 1", encoding="utf-8")
    r = subprocess.run([NODE, "--check", str(t)],
                       capture_output=True, text=True, timeout=60)
    assert r.returncode != 0


# ── ⓑ chay THAT cac ham thuan ─────────────────────────────────────────────
_NAP = """
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const hop = {console, URL, URLSearchParams, window:{}, document:undefined};
hop.globalThis = hop;
vm.createContext(hop);
for (const t of %s) vm.runInContext(readFileSync(t,'utf8'), hop, {filename:t});
const ra = vm.runInContext(%s, hop);
console.log(JSON.stringify(ra));
"""


def _chay(tep: list[str], bieu_thuc: str):
    return json.loads(_node(_NAP % (json.dumps(tep), json.dumps(bieu_thuc))))


@can_node
def test_chu_an_toan_that_su_thoat_dau_ngoac():
    """⛔ Cot `memo` cua so THAT di thang len man — mot `<` ⛔ khong duoc nuot
    mat mot doan chu ma ke toan ⛔ khong biet."""
    ra = _chay(["thanh_phan.js"],
               "TP.chu('a <b> & \"c\" </script>')")
    assert ra == "a &lt;b&gt; &amp; &quot;c&quot; &lt;/script&gt;"


@can_node
def test_so_tien_dinh_dang_kieu_viet():
    ra = _chay(["thanh_phan.js"],
               "[TP.tien('11555276662.00'), TP.tien(''), TP.tien(null)]")
    assert ra[0].replace(" ", ".").replace(",", ".") \
        .endswith("555.276.662")
    assert ra[1] == "—" and ra[2] == "—"


@can_node
def test_co_niem_tin_LA_thi_KEU_chu_khong_am_tham_thanh_flash():
    """⛔⛔ Mot co la ⛔ khong duoc am tham thanh `flash`: mot con so chua doi
    soat khoac nhan da doi soat la loai sai te nhat cua ca lop bao cao."""
    ra = _chay(["thanh_phan.js"], "TP.chip_niem_tin('da_ky_roi_nhe')")
    assert "cờ lạ" in ra and "chip crit" in ra


@can_node
def test_ba_co_niem_tin_that_deu_ve_duoc():
    ra = _chay(["thanh_phan.js"],
               "['flash','reconciled','signed'].map(TP.chip_niem_tin)")
    assert len(ra) == 3 and all("cờ lạ" not in x for x in ra)


@can_node
def test_dat_null_KHONG_duoc_ve_giong_DAT():
    """⭐⭐ Luat so mot cua du an, dat vao mot lop CSS."""
    ra = _chay(["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f03.js"],
               "[F03._muc(true), F03._muc(false), F03._muc(null)]")
    dat, khong, chua = ra
    assert dat["lop"] == "pass" and khong["lop"] == "fail"
    assert chua["lop"] == "unk"
    assert chua["lop"] not in (dat["lop"], khong["lop"])
    assert "KHÔNG ĐO ĐƯỢC" in chua["chu"]


@can_node
def test_moi_ma_loi_deu_co_du_hai_phan_khi_CHAY():
    """Bai `test_goi_cua_phu_het_ma_loi` doc bang **van ban**; bai nay doc bang
    **gia tri that** sau khi JS chay — hai duong doc doc lap."""
    ra = _chay(["goi_cua.js"],
               "Object.entries(FLS.CAU).filter(([k,v]) => !v.cau || !v.lam_gi)"
               ".map(([k]) => k)")
    assert ra == []


@can_node
def test_loi_cua_mang_du_cau_va_viec_lam_tiep():
    ra = _chay(["goi_cua.js"], """
      (() => { const e = new FLS.LoiCua('FLS-LOCKED-PERIOD', 409, 'chi tiet',
                                        null, 'rq1');
               return {ma:e.ma, cau:e.cau, lam_gi:e.lam_gi, rq:e.request_id}; })()
    """)
    assert ra["ma"] == "FLS-LOCKED-PERIOD"
    assert "đã chốt" in ra["cau"] and ra["lam_gi"]
    assert ra["rq"] == "rq1"


# ── ⭐ `B3` · o "⛔ khong do duoc" cua bang do phu ─────────────────────────
@can_node
def test_o_do_phu_NULL_khong_duoc_ve_thanh_0():
    """⭐⭐ Cung luat voi cong `dat = null`, dat vao mot o cua bang.

    Σ tien = 0 ⇒ *"xem bao nhieu dong thi qua 90 phan tram tien"* ⛔ khong co
    nghia. Ve `0` la noi *"xem 0 dong la du"* — sai, va **nghe nhu tin tot**.
    """
    ra = _chay(["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f03.js"],
               "F03._o_phu({so_dong_phu:null, pct_that:null,"
               " so_dong_trong_danh_sach:null}, '90')")
    assert "không đo được" in ra
    assert ">0<" not in ra and ">0 dòng" not in ra


@can_node
def test_o_do_phu_hien_PHAN_TRAM_THAT_de_nhan_khong_noi_qua():
    ra = _chay(["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f03.js"],
               "F03._o_phu({so_dong_phu:444, pct_that:'90.00',"
               " so_dong_trong_danh_sach:444}, '90')")
    assert "444" in ra and "90.00%" in ra
    assert "danh sách hiện" not in ra          # ⛔ hai so bang nhau ⇒ khong on ao


@can_node
def test_o_do_phu_NOI_RA_khi_hai_cau_hoi_lech_nhau():
    """⚠ *"Luy ke <= muc"* va *"du cham muc"* lech dung mot dong ⇒ PHAI noi ra,
    ⛔ khong de nguoi doc thay hai con so khac nhau o hai cho ma tu doan."""
    ra = _chay(["thanh_phan.js", "goi_cua.js", "trang_thai.js", "man_f03.js"],
               "F03._o_phu({so_dong_phu:9, pct_that:'100.00',"
               " so_dong_trong_danh_sach:8}, '90')")
    assert "danh sách hiện" in ra and "8" in ra


# ── ⭐ `B4` · man F01 ──────────────────────────────────────────────────────
_F01 = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
        "man_f01.js"]


@can_node
def test_hoan_lan_thu_BA_doi_mau_va_KHONG_bao_cho_ai():
    """⚠ `QĐ-ITL-24`: lan thu ba **doi mau**, ⛔ khong leo cap — leo cap la mot
    co che can NGUOI NHAN, ma `QĐ-ITL-27` da khai tu vai do."""
    ra = _chay(_F01, """[
      F01._o_hoan({defer_until:'2026-09-20', defer_count:1}),
      F01._o_hoan({defer_until:'2026-09-20', defer_count:3}),
      F01._o_hoan({defer_until:null, defer_count:0})
    ]""")
    mot, ba, khong = ra
    assert "chip lock" in mot and "chip crit" not in mot
    assert "chip crit" in ba, "⛔ lan thu ba phai DOI MAU"
    assert khong == "", "⛔ dong chua hoan thi ⛔ khong ve gi"


@can_node
def test_o_hoan_hien_ca_NGAY_va_SO_LAN():
    """⛔ Mot dong da hoan den 20/09 ⛔ khong duoc trong y het dong chua ai dung
    vao — hai ke toan se lam trung."""
    ra = _chay(_F01, "F01._o_hoan({defer_until:'2026-09-20', defer_count:2})")
    assert "2026-09-20" in ra and "lần 2" in ra


@can_node
def test_man_F01_khong_go_cung_ten_cua_nao_ngoai_bang_tuyen():
    """⛔ Moi duong man hinh goi phai co that trong `BANG_TUYEN` — `DEV-12` §5
    muc 5 doi dung phep quet nay."""
    import re as _re

    from fls.api import bang_tuyen as bt

    with open(os.path.join(pv.THU_MUC, "man_f01.js"), encoding="utf-8") as f:
        ma = f.read()
    goi = set(_re.findall(r"FLS\.(?:doc|ghi)\('([^']+)'", ma))
    assert goi, "⛔ ⛔ khong doc duoc duong nao — phep quet nay vo dung"
    mau = [t.duong[len(bt.TIEN_TO):] for t in bt.BANG_TUYEN]
    for g in goi:
        # `'/queue/' + r.itl_id + '/match'` ⇒ chuoi bat duoc la `/queue/`
        assert any(m.startswith(g.rstrip("/")) or g.startswith(
            m.split("{")[0].rstrip("/")) for m in mau), \
            f"⛔ man hinh goi {g!r} ma ⛔ khong tuyen nao khop"
