# -*- coding: utf-8 -*-
"""`WO-022` — hai bài cần KHO: `AC-3` *(cửa thật trên kho TEST)* + `AC-5` *(sổ
THẬT, chỉ `SELECT`)*.

⛔⛔ **Vì sao `AC-3` phải đi qua cửa thật.** Bài DOM ở tệp bên cạnh đút sẵn
thân `/chum`. `11` §6 đã ghi lớp lỗi *"khuôn thử tự nhét che chỗ bản thật"*:
ở đây cái có thể lệch là **khuôn tiền cửa trả** *(`"1234.56"` hay `"1234.5600"`
hay số?)* và **tên trường tiền tệ** *(`curr` ở từng dòng lệnh?)* — khuôn tự nhét
trả đúng cái người viết **tưởng**, cửa thật trả cái nó trả. Ca **U** của
`KQ-021` *(máy `8099`)*: một dòng tiền USD `2000.00` ghép hai dòng lệnh
`1234.56` + `765.44` ⇒ hộp ② in **`1.235 USD`** · **`765 USD`**.

⛔⛔ **Vì sao `AC-5` đo QUAN HỆ trên toàn sổ thật, ⛔ ghim hằng.** Khứ hồi
*"in rồi đọc lại = giá trị kho"* trên **mọi** `ps_no`/`ps_co` ≠ 0 bắt cả lớp lỗi
`Number * 100` *(Rủi ro ② của `WO`)* lẫn mọi chỗ cắt / làm tròn — mà ⛔ cần biết
trước sổ có bao nhiêu dòng. Mẫu số theo tiền tệ in ra và phải > 0 *(`Đ3`)*.
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile
from decimal import Decimal

import pytest

from fls.db.kho import dsn_that, noi_chi_doc
from fls.web import phuc_vu as pv
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import (_dong_bank, _lenh, _ma,  # noqa: F401
                                                        _run, conn)
from tests.web.khung_node import NODE, _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01
from tests.web.test_wo008_v2_nam_ca_bo_gan import DEM_HOP

pytestmark = pytest.mark.pg


# ═══ AC-3 · ca U của `KQ-021` dựng từ CỬA THẬT trên kho TEST ═══════════════
@pytest.fixture()
def ca_U(conn, may):  # noqa: F811
    """Dòng tiền USD `2000.00` ⇐ ghép **qua HTTP thật** hai dòng lệnh `1234.56`
    + `765.44` *(Σ khớp đúng xu — dung sai USD = 0, `QĐ-ITL-62`)*; trả
    `(itl_id, [mã lệnh], thân /chum)`."""
    run = _run(conn)
    i = _dong_bank(conn, run, "2000.00", "USD")
    a, b = _ma(), _ma()
    _lenh(conn, run, (a, "1234.56", "USD", "Approve", "HD-U", "C-U"),
          (b, "765.44", "USD", "Approve", "HD-U", "C-U"))
    ok, r = _goi(may, f"{V}/queue/{i}/match", pt="POST",
                 than={"pm_line_ids": [a, b]})
    assert ok == 200, r
    ok, ch = _goi(may, f"{V}/queue/{i}/chum")
    assert ok == 200, ch
    return i, [a, b], ch["data"]


def _lenh_man(ma: str, tien: str, i: int) -> dict:
    """Dòng lệnh **đang gắn** dòng tiền `i` — khuôn `F01G.ST.dong`."""
    return {"ma_lenh": ma, "noi_dung": "chi " + ma, "so_tien": tien,
            "curr": "USD", "loai_phieu": "PM", "itl_da_gan": [i],
            "trang_thai": "da_gan", "trang_thai_nhan": "đã gán",
            "trang_thai_mau": "ok", "ngay": "2026-09-30", "cdt": "CVL",
            "nhom_du_truong": [],
            "gd_ds": [{"itl_id": i, "bac": "tien", "doc_no": "FT-W",
                       "amount": "2000.00", "curr": "USD",
                       "doc_date": "2026-09-30", "da_gan": True}]}


@can_node
def test_AC3_ca_U_than_CHUM_THAT__hop_2_in_1_234_56_va_765_44_USD(ca_U):
    """⭐⭐ Hộp ② *(`HT.mo` thật)* chứa `1.234,56 USD` **và** `765,44 USD`; thẻ
    lệnh + rail in `1.234,56 USD`; ⛔ chuỗi `1.235 USD` ở đâu trên màn ghép.

    ⛔ Chiều ĐỎ *(đã chạy trên `5f8796b`)*: hàm cũ ⇒ hộp `1.235 USD` · `765
    USD` ⇒ ĐỎ."""
    i, (a, b), chum = ca_U
    # hình dạng cửa thật — thứ màn đọc (`dong_lenh[].pm_line_id/amount/curr`)
    assert chum["so_dong"] == 2 and chum["can_hoi"] is True, chum
    assert sorted((x["pm_line_id"], x["amount"], x["curr"])
                  for x in chum["dong_lenh"]) == sorted(
        [(a, "1234.56", "USD"), (b, "765.44", "USD")]), chum
    dong = [_lenh_man(a, "1234.56", i), _lenh_man(b, "765.44", i)]
    r = _chay(DEM_HOP + """
      _TRA[%s] = {data: %s};
      _TRA['/queue/lenh/%s/itl-candidates'] = {data: {ung_vien: []}};
      F01G.ST.dong = %s;
      await F01G.mo_lenh(%s);
      const goc = document.getElementById('ghep-goc');
      const the = goc.querySelectorAll('.tien').map(x => x.textContent);
      const rail = goc.querySelectorAll('.amt').map(x => x.textContent);
      const man = goc.textContent;
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _ngu(30);
      return {the, rail, man, hop: _hop(), so_hop: _HOP.length,
              chum: _dem(/\\/chum$/)};
    """ % (json.dumps(f"/queue/{i}/chum"), json.dumps(chum, ensure_ascii=False),
           a, json.dumps(dong, ensure_ascii=False), json.dumps(a)),
        tep=TEP_F01, vo=VO_F01)
    assert r["chum"] == 1, "⛔ không đo được: màn ⛔ hỏi cửa /chum"
    assert r["so_hop"] == 1 and r["hop"]["mo"] is True, r
    hop = r["hop"]["b"]
    assert f"{a} — 1.234,56 USD" in hop and f"{b} — 765,44 USD" in hop, hop
    assert r["the"] == ["1.234,56 USD"], r["the"]
    assert "1.234,56 USD" in r["rail"] and "765,44 USD" in r["rail"], r["rail"]
    for chu in (r["man"], hop):
        assert "1.235 USD" not in chu and "765 USD" not in chu, chu


# ═══ AC-5 · KHỨ HỒI trên sổ THẬT — chỉ `SELECT` ═══════════════════════════
_KICH_BAN = r"""
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
const hop = {console, window: {}, document: undefined};
hop.globalThis = hop;
vm.createContext(hop);
vm.runInContext(readFileSync('thanh_phan.js', 'utf8'), hop,
                {filename: 'thanh_phan.js'});
const vao = JSON.parse(readFileSync(process.argv[2], 'utf8'));
hop._VAO = vao;
const ra = vm.runInContext('_VAO.map(x => TP.tien(x[0], x[1]))', hop);
console.log(JSON.stringify(ra));
"""


def _in_ca_so(vao: list[list]) -> list[str]:
    """Chạy `TP.tien` THẬT trên mọi cặp `(giá trị, tiền tệ)` — một lượt `node`.

    ⚠ Dữ liệu đi qua **tệp**, ⛔ dòng lệnh: ~8 nghìn giá trị vượt trần 32.767
    ký tự của dòng lệnh Windows."""
    with tempfile.TemporaryDirectory() as d:
        js, du = os.path.join(d, "k.mjs"), os.path.join(d, "vao.json")
        with open(js, "w", encoding="utf-8") as f:
            f.write(_KICH_BAN)
        with open(du, "w", encoding="utf-8") as f:
            json.dump(vao, f)
        r = subprocess.run([NODE, js, du], capture_output=True, text=True,
                           encoding="utf-8", cwd=pv.THU_MUC, timeout=120)
    assert r.returncode == 0, f"⛔ node NO:\n{r.stderr}"
    return json.loads(r.stdout.strip().splitlines()[-1])


def _doc_lai(chu: str) -> Decimal:
    """Ngược luật §5b ⓓ: bỏ `.` nghìn, `,` ⇒ `.` thập phân."""
    return Decimal(chu.replace(".", "").replace(",", "."))


@can_node
def test_AC5_KHU_HOI_moi_ps_no_ps_co_cua_SO_THAT_bang_gia_tri_kho():
    """⛔ Chiều ĐỎ *(đã chạy trên `5f8796b`)*: hàm cũ ⇒ **2.518** giá trị lệch
    *(≥ 2.500 như `WO`)* ⇒ ĐỎ; tập rỗng ⇒ ĐỎ *(`Đ3`)*."""
    with noi_chi_doc(dsn_that()) as c:
        dong = c.execute(
            "SELECT curr, v::text FROM ("
            " SELECT curr, ps_no AS v FROM fls_itl"
            " UNION ALL SELECT curr, ps_co FROM fls_itl) x"
            " WHERE v IS NOT NULL AND v <> 0").fetchall()
        le = dict(c.execute(
            "SELECT curr, count(*) FROM fls_itl"
            " WHERE ps_no <> trunc(ps_no) OR ps_co <> trunc(ps_co)"
            " GROUP BY curr").fetchall())
    assert len(dong) > 0, "⛔ không đo được: sổ thật 0 giá trị tiền ≠ 0"
    # ⭐ Mẫu số in ra theo tiền tệ *(đo 02/10: USD 2.413 · SGD 74 · HKD 20 ·
    #   VND 11)* — ⛔ ghim hằng, chỉ đòi > 0 ở cả bốn.
    print("WO-022 AC-5 · gia tri ≠ 0 =", len(dong),
          "· dong so co phan le theo tien te =", le)
    for t in ("USD", "SGD", "HKD", "VND"):
        assert le.get(t, 0) > 0, f"⛔ không đo được: {t} 0 dòng có phần lẻ — {le}"
    ra = _in_ca_so([[v, cur] for cur, v in dong])
    assert len(ra) == len(dong)
    lech = [(cur, v, chu) for (cur, v), chu in zip(dong, ra)
            if _doc_lai(chu) != Decimal(v)]
    assert lech == [], (f"⛔ {len(lech)}/{len(dong)} giá trị in ra ≠ kho — "
                        f"10 đầu: {lech[:10]}")
