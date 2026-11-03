# -*- coding: utf-8 -*-
"""`WO-022` vòng 2 · `AC-11` — chuỗi ô tiền dài nhất trên **sổ THẬT** ≤ ngân
sách §5b ⓘ *(chỉ `SELECT`, `noi_chi_doc`)*.

⛔⛔ **Vì sao bài này đo dữ liệu, ⛔ đo CSS.** `AC-10` canh *"ô đủ rộng cho 18
ký tự"*; nó **⛔ biết** 18 có còn là chuỗi dài nhất ⛔. `HOI-026` sinh ra đúng
từ chỗ ấy: con số *"18 ký tự đã vừa"* được **tin**, ⛔ đo lại trên tập mà ô thật
in. Bài này đo **chuỗi ô in** *(`TP.tien` **thật** qua `node`, đúng biểu thức
của `ve_bang`)* trên:
  · **tập lệnh mà bảng danh sách lệnh đọc** — gọi **hàm repo của cửa**
    `lenh_cho.doc_lenh_cho` + `doc_lenh_da_gan` *(hai rổ khép về tổng — chip
    `Tất cả`)* trên phạm vi mặc định của cửa `chi_nap_that()`; ⛔ tự viết SQL
    chọn run *(chọn run sai là đo một tập ô ⛔ in)*;
  · mọi `ps_no`/`ps_co ≠ 0` của `fls_itl` *(cột `Số tiền GD`)*.

⭐ Đỏ **thật** về sau = dữ liệu vượt ngân sách ⇒ **việc của `fls-ba`** *(tính lại
§5b ⓘ)*, ⛔ nới số trong bài *(`WO-022` `AC-11`)*.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

import pytest

from fls.api.bao import _thuong
from fls.db.kho import dsn_that, noi_chi_doc
from fls.repo import lenh_cho as lc
from fls.repo.doc_bao_cao import TRANG_TOI_DA
from fls.repo.pham_vi import chi_nap_that
from fls.web import phuc_vu as pv
from tests.web.khung_node import NODE, can_node
from tests.web.test_wo022_v2_o_tien_va_mot_luat_so_le import NGAN_SACH_KY_TU

pytestmark = pytest.mark.pg

#: Đúng hai biểu thức ô của `ve_bang` *(`man_f01_ghep.js`)*: cột `Số tiền`
#: `TP.tien(d.so_tien, d.curr) + ' ' + d.curr` · cột `Số tiền GD`
#: `TP.tien(d.gd.amount, d.gd.curr) + ' ' + (d.gd.curr || '')`.
_KICH_BAN = r"""
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const hop = {console, window: {}, document: undefined};
hop.globalThis = hop;
vm.createContext(hop);
vm.runInContext(readFileSync('thanh_phan.js', 'utf8'), hop,
                {filename: 'thanh_phan.js'});
hop._VAO = JSON.parse(readFileSync(process.argv[2], 'utf8'));
const ra = vm.runInContext(
  "({lenh: _VAO.lenh.map(x => TP.tien(x[0], x[1]) + ' ' + x[1]),"
  + " so: _VAO.so.map(x => TP.tien(x[0], x[1]) + ' ' + (x[1] || ''))})", hop);
console.log(JSON.stringify(ra));
"""


def _o_in(lenh: list[list], so: list[list]) -> dict:
    with tempfile.TemporaryDirectory() as d:
        js, du = os.path.join(d, "k.mjs"), os.path.join(d, "vao.json")
        with open(js, "w", encoding="utf-8") as f:
            f.write(_KICH_BAN)
        with open(du, "w", encoding="utf-8") as f:
            # ⭐ `Decimal` → chuỗi bằng **chính** hàm cửa dùng *(`bao._thuong`)*
            #   — chuỗi ô đo được là chuỗi màn nhận, ⛔ một bản dựng lại.
            json.dump({"lenh": lenh, "so": so}, f, default=_thuong)
        r = subprocess.run([NODE, js, du], capture_output=True, text=True,
                           encoding="utf-8", cwd=pv.THU_MUC, timeout=120)
    assert r.returncode == 0, f"⛔ node NO:\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


def _het_trang(doc, conn, p) -> list[dict]:
    """Đọc **hết** các trang của một hàm repo có con trỏ."""
    t = doc(conn, p, limit=TRANG_TOI_DA)
    dong = list(t.dong)
    while t.con_tro:
        t = doc(conn, p, con_tro=t.con_tro, limit=TRANG_TOI_DA)
        dong += t.dong
    return dong


def _dai_nhat_theo_tien_te(cap: list[tuple[str, str]]) -> dict:
    """`{tiền tệ: (số ô, chuỗi dài nhất, độ dài)}` — mẫu số in ra *(`Đ4`)*."""
    ra: dict = {}
    for cur, chu in cap:
        n, best, dai = ra.get(cur, (0, "", -1))
        ra[cur] = (n + 1, chu, len(chu)) if len(chu) > dai \
            else (n + 1, best, dai)
    return ra


@can_node
def test_AC11_chuoi_o_tien_DAI_NHAT_tren_so_THAT_vua_ngan_sach():
    """⛔ Chiều ĐỎ *(đã chạy)*: ngân sách tạm `17` ⇒ ĐỎ *(sổ hôm nay có 18 —
    `11.742.361.787 VND` · lệnh `103.950.000,00 USD`)*; tập rỗng ⇒ ĐỎ
    *(`Đ3`)*."""
    p = chi_nap_that()
    with noi_chi_doc(dsn_that()) as c:
        lenh = (_het_trang(lc.doc_lenh_cho, c, p)
                + _het_trang(lc.doc_lenh_da_gan, c, p))
        so = c.execute(
            "SELECT curr, v::text FROM ("
            " SELECT curr, ps_no AS v FROM fls_itl"
            " UNION ALL SELECT curr, ps_co FROM fls_itl) x"
            " WHERE v IS NOT NULL AND v <> 0").fetchall()
    vao_lenh = [[d.get("amount"), d.get("curr")] for d in lenh
                if d.get("amount") not in (None, "")]
    vao_so = [[v, cur] for cur, v in so]
    assert vao_lenh, "⛔ không đo được: cửa bảng lệnh trả 0 lệnh có tiền"
    assert vao_so, "⛔ không đo được: sổ thật 0 giá trị tiền ≠ 0"
    ra = _o_in(vao_lenh, vao_so)
    assert len(ra["lenh"]) == len(vao_lenh) and len(ra["so"]) == len(vao_so)
    bang_lenh = _dai_nhat_theo_tien_te(
        [(x[1], s) for x, s in zip(vao_lenh, ra["lenh"])])
    bang_so = _dai_nhat_theo_tien_te(
        [(x[1], s) for x, s in zip(vao_so, ra["so"])])
    # ⭐ Mẫu số + chuỗi dài nhất THEO TIỀN TỆ in ra *(đo 02/10: lệnh **3.820**
    #   — `103.950.000,00 USD`; sổ **8.387** — `11.742.361.787 VND`)* — ⛔ ghim.
    print("WO-022 AC-11 · lenh =", len(vao_lenh), bang_lenh)
    print("WO-022 AC-11 · so =", len(vao_so), bang_so)
    vuot = [("lệnh", s) for s in ra["lenh"] if len(s) > NGAN_SACH_KY_TU] \
        + [("sổ", s) for s in ra["so"] if len(s) > NGAN_SACH_KY_TU]
    assert vuot == [], (
        f"⛔ {len(vuot)} chuỗi ô vượt ngân sách {NGAN_SACH_KY_TU} ký tự — việc "
        f"của `fls-ba` tính lại `BA-06` §5b ⓘ, ⛔ nới số ở đây: {vuot[:10]}")
