"""KHUNG NODE dung chung — nap tep man hinh THAT vao mot DOM toi thieu.

⛔⛔ **Vi sao tach ra thay vi chep sang tep thu hai.** Khung nay quyet dinh
*"man hinh dang chay trong hoan canh nao"* — bang cot nao, phien nao, cua gia
tra gi. Hai ban chep se **lech**, va luc do hai bo bai kiem se noi ve hai man
hinh khac nhau ma ca hai deu xanh.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess

import pytest

from fls.api.cot_so import than_js
from fls.web import phuc_vu as pv

NODE = shutil.which("node")
can_node = pytest.mark.skipif(
    NODE is None,
    reason="⛔ may ⛔ khong co `node` — cong nay BO QUA, ⛔ khong dat")

O_DAY = os.path.dirname(os.path.abspath(__file__))

# 3 dong: hai dong ky MO, mot dong ky DA CHOT.
DONG = [
    {"itl_id": 101, "doc_date": "2026-08-01", "doc_no": "FT-A", "memo": "chi A",
     "curr": "VND", "ps_no": None, "ps_co": "1000000.00", "acct": "R | x",
     "le": "VVOT", "le_payer": None, "hd": None, "pay_type": None,
     "cdt1": None, "svc_start": None, "svc_end": None,
     "work_status": "UNMAPPED", "pm_hinh": None, "is_flash": True,
     "period_state": "open", "run_id": "NAP-1", "source_system": "RAW",
     "source_sheet": "L1", "source_row": 1,
     # ⭐ Nam truong vung PHAN BO — cua THAT tra chung *(suy o may
     # chu)*, nen dong mau ⛔ khong duoc thieu: thieu la bo test
     # dang thu mot cua KHAC cua that.
     "alloc_cfa1": "", "alloc_cfa2": "#N/A", "alloc_method": "#N/A",
     "alloc_can_phan_bo": False, "alloc_na": True},
    {"itl_id": 102, "doc_date": "2026-08-02", "doc_no": "FT-B", "memo": "chi B",
     "curr": "VND", "ps_no": None, "ps_co": "2000000.00", "acct": "R | x",
     "le": "VVOT", "le_payer": None, "hd": None, "pay_type": None,
     "cdt1": None, "svc_start": None, "svc_end": None,
     "work_status": "UNMAPPED", "pm_hinh": None, "is_flash": True,
     "period_state": "open", "run_id": "NAP-1", "source_system": "RAW",
     "source_sheet": "L1", "source_row": 2,
     # ⭐ Nam truong vung PHAN BO — cua THAT tra chung *(suy o may
     # chu)*, nen dong mau ⛔ khong duoc thieu: thieu la bo test
     # dang thu mot cua KHAC cua that.
     "alloc_cfa1": "", "alloc_cfa2": "#N/A", "alloc_method": "#N/A",
     "alloc_can_phan_bo": False, "alloc_na": True},
    {"itl_id": 103, "doc_date": "2026-07-31", "doc_no": "FT-C", "memo": "chi C",
     "curr": "VND", "ps_no": None, "ps_co": "3000000.00", "acct": "R | x",
     "le": "VVOT", "le_payer": None, "hd": None, "pay_type": None,
     "cdt1": None, "svc_start": None, "svc_end": None,
     "work_status": "UNMAPPED", "pm_hinh": None, "is_flash": True,
     # ⭐ Ky DA CHOT — moi o cua dong nay phai la chi-doc (`INV-I13`).
     "period_state": "locked", "run_id": "NAP-1", "source_system": "RAW",
     "source_sheet": "L1", "source_row": 3,
     # ⭐ Nam truong vung PHAN BO — cua THAT tra chung *(suy o may
     # chu)*, nen dong mau ⛔ khong duoc thieu: thieu la bo test
     # dang thu mot cua KHAC cua that.
     "alloc_cfa1": "", "alloc_cfa2": "#N/A", "alloc_method": "#N/A",
     "alloc_can_phan_bo": False, "alloc_na": True},
]

TEP = ["thanh_phan.js", "goi_cua.js", "trang_thai.js", "hop_thoai.js",
       "man_f02.js"]

_KHUNG = r"""
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {lam_dom} from %(dom)s;

const d = lam_dom();
const window = {
  FLS_PHIEN: %(phien)s,
  location: {origin: 'http://x', search: ''},
  scrollTo() {}
};
const hop = {
  console, URL, URLSearchParams, setTimeout, clearTimeout, Promise, JSON,
  Math, Number, String, Object, Array, Boolean, Map, Set, Error, isFinite,
  window, document: d.document, fetch: () => { throw new Error('⛔ cua that'); }
};
hop.globalThis = hop;
vm.createContext(hop);
// ⭐ Duong BAN su kien — bo test dong vai nguoi go phim / dan.
hop._ban = d.ban;

// ⭐ Bang cot THAT — sinh tu `fls/api/cot_so.py`, ⛔ khong go tay o day.
vm.runInContext(readFileSync(%(cot)s, 'utf8'), hop, {filename: 'cot.js'});

// Vo man: hai o ma `man_f02.js` tim.
const than = d.document.createElement('div'); than.id = 'than-f02';
const man = d.document.createElement('section'); man.id = 'man-f02';
man.className = 'screen on';
d.body.appendChild(man); d.body.appendChild(than);

for (const t of %(tep)s)
  vm.runInContext(readFileSync(t, 'utf8'), hop, {filename: t});

// ⭐ Thay cua bang mot cua GIA — cung khuon `?gia_lap=` cua `ung_dung.js`,
// tuc la mot duong da co that trong san pham, ⛔ khong phai mot cua hau cho
// rieng bo test.
const goi = [];
vm.runInContext(`
  globalThis._GOI = [];
  globalThis._TRA = {};
  FLS.doc = function (duong, q) {
    _GOI.push(['doc', duong, q || null]);
    const t = _TRA[duong];
    if (t && t.no) return Promise.reject(t.no);
    return Promise.resolve({data: t ? t.data : null, meta: {data_status:'flash'}});
  };
  FLS.ghi = function (duong, than) {
    _GOI.push(['ghi', duong, than]);
    const t = _TRA[duong];
    if (t && t.no) return Promise.reject(t.no);
    return Promise.resolve({data: t ? t.data : {}, meta: {}});
  };
  _TRA['/ledger'] = {data: {rows: %(dong)s, next_cursor: null, count: 3}};
`, hop);

// ⛔⛔ Kich ban di vao bang mot CHUOI da `json.dumps`, ⛔ KHONG nhet vao mot
// template literal. Ban dau toi nhet vao `` ` ` `` cho gon — va mot dau
// backtick trong **chu thich** cua kich ban da dong template literal lai giua
// chung, roi node bao mot loi ⛔ khong lien quan gi (`input is not defined`).
// ⇒ Cung cach nghi voi bang tep: bo cai cho de loi ton tai, ⛔ khong hoc cach
//   ne no.
const ra = await vm.runInContext(%(kich_ban)s, hop);
console.log(JSON.stringify(ra === undefined ? null : ra));
"""


def _chay(kich_ban: str, *, phien: dict | None = None, dong=None):
    import tempfile

    cot = os.path.join(tempfile.mkdtemp(), "cot.js")
    with open(cot, "wb") as f:
        f.write(than_js())
    ma = _KHUNG % {
        "dom": json.dumps(
            "file:///" + os.path.join(O_DAY, "dom_gia.js").replace("\\", "/")),
        "cot": json.dumps(cot),
        "tep": json.dumps(TEP),
        "phien": json.dumps(phien if phien is not None
                            else {"actor": "lan@apero.vn", "cho_ghi": True}),
        "dong": json.dumps(DONG if dong is None else dong, ensure_ascii=False),
        "kich_ban": json.dumps("(async () => {" + kich_ban + "})()"),
    }
    r = subprocess.run([NODE, "--input-type=module", "-e", ma],
                       capture_output=True, text=True, encoding="utf-8",
                       cwd=pv.THU_MUC, timeout=90)
    assert r.returncode == 0, f"⛔ node NO:\n{r.stdout}\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


_VE = """
  await F02.ve();
  const luoi = document.querySelector('#so-luoi');
  const than = luoi.tBodies[0];
"""

# ⭐⭐ CHE DO GO — luoi du 25 cot, go THANG tren o.
#
# ⛔⛔ **Vi sao phai noi ro che do trong bo test.** Tu 03/09 man `F02` co HAI
# che do *(owner chot sau khi doi chieu `FLS-Wireframe.html`)*: `quet` — luoi
# 9 cot **chi doc**, sua trong panel ben phai — va `go` — luoi du cot, go tren
# o. Mac dinh la `quet`, vi do la layout owner chi ra.
#
# ⇒ Tam hanh vi Sheets *(§1)* chi ton tai o che do `go`, nen bo test cua chung
#   phai **noi ra minh dang o che do nao**. ⛔ Mot bai test ⛔ khong noi che do
#   la mot bai test se **doi nghia** vao lan ai do doi mac dinh — va no se doi
#   nghia **trong im lang**, van xanh, van trong nhu dang do dieu cu.
_VE_GO = """
  F02.ST.che_do = 'go';
""" + _VE


def _o(r, c):
    return f"than.rows[{r}].cells[{c}]"


