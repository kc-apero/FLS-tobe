# -*- coding: utf-8 -*-
"""`KQ-050` *(kiểm `BG-048` — `WO-045` ①)* · cú `Gán` sai cặp **CÙNG tiền tệ,
TRONG dung sai** — ca `WO-045` *"Câu còn treo"* ghi **chưa đo**.

⭐ Vì sao cần ca riêng *(`fls-test` 05/10)*: ca của Dev *(`ca_wo045`: `A` USD ↔
`B` VND)* chứng minh màn **gửi** cặp sai, nhưng cửa ghi trả `422` *(khác tệ)* ⇒
⛔ biết cặp sai mà cửa **nhận** có lọt ⛔. Ca này: hai lệnh **VND** `X`, `Y`;
dòng tiền mã của mỗi lệnh lệch **1.500 đ** với chính nó *(ngoài dung sai tay
`min(1.000 đ; 0,5%)` ⇒ ⛔ tự chứng ⇒ chip `Chưa gán`)* và lệch **500 đ** với
lệnh **kia** *(trong dung sai)*.

Đo Chrome *(8099 kho TEST, chuột thật + phím `j`, CDP giữ `itl-candidates` của
lệnh trước ~2 s — `KQ-050` `AC-11`)*:
  · mã khi nhận *(`db0adae`, worktree `14a4b72`)*: `POST /queue/<itl mã của
    lệnh TRƯỚC>/match {pm_line_ids: [lệnh ĐANG MỞ]}` ⇒ **`200`**, một mối nối
    sai ghi vào kho TEST *(hình `T`, kèm bút toán `cdt1`/`hd`)*;
  · mã mới *(`2b804e3`)*: `POST /queue/<itl mã của lệnh đang mở>/match` ⇒ `422`
    *(lệch 1.500 — đúng cặp, đúng bị chặn)*.

Hai bài: ⓐ màn *(DOM, thân cửa thật)* — lượt lệnh trước về **sau** ⇒ `Gán`
⛔ mang `itl_id` mã của lệnh trước; ⓑ **sự thật** của cửa ghi *(`Đ5` — `mong`
khai trước)*: cặp sai trong dung sai **được nhận** ⇒ màn là chốt chặn **duy
nhất** của ①. Cửa đổi luật ⇒ ⓑ ĐỎ, phải khai lại.

⛔ Ghi **kho TEST** *(`assert current_database()`)*.
"""
from __future__ import annotations

import random
import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import DongPM, canon_ref
from fls.db.kho import dsn_test
from fls.ledger.build import NgucCanh
from fls.repo.chay_nap import chen_dong_pm
from tests.web.ca_wo032 import goi_ok
from tests.web.ca_wo037 import _tien
from tests.web.khung_giu import CUA_GIU, nap
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = [pytest.mark.pg, can_node]


def dung_ca_cung_te(conn) -> dict:
    assert conn.execute("SELECT current_database()").fetchone()[0] == "fls_test"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T50" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    a = random.randint(300, 800) * 1000       # ≥ 300.000 ⇒ 0,5% ≥ 1.500 ⇒ dung sai 1.000
    tien = {"X": a, "Y": a + 2000}
    itl_tien = {"X": a + 1500, "Y": a + 500}  # |iX−X|=1500 · |iX−Y|=500 · |iY−Y|=1500 · |iY−X|=500
    doc = {k: f"FT50{k}{h}" for k in "XY"}
    nguon = "R | 123456789_VPB VND_K50" + h
    i = {k: _tien(conn, run, nguon, n + 1, f"{itl_tien[k]}.00", "VND", doc[k])
         for n, k in enumerate("XY")}
    lenh = {k: f"P{k}0{h[:5]}-1" for k in "XY"}
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"),
                 [DongPM(3 + n, lenh[k].split("-")[0], lenh[k],
                         D(f"{tien[k]}.00"), "VND", "Approve", canon_ref(doc[k]),
                         "HD-K50", "C-K50", ref_tho=doc[k])
                  for n, k in enumerate("XY")])
    return {"run": run, "lenh": lenh, "doc": doc, "i": i, "tien": tien,
            "itl_tien": itl_tien}


@pytest.fixture(scope="module")
def ca_tra():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_cung_te(c)
    L = ca["lenh"]
    Dg = {"g_nguoi": "/queue/lenh-cho?ro=nguoi&limit=500",
          "g_may": "/queue/lenh-cho?ro=may&tu_chung=0&limit=500",
          "uv_X": f"/queue/lenh/{L['X']}/itl-candidates",
          "uv_Y": f"/queue/lenh/{L['Y']}/itl-candidates"}
    with _may() as m:
        TRA = {d: goi_ok(m, d) for d in Dg.values()}
    return ca, Dg, TRA


def _uv(env: dict) -> list:
    return [(u["itl_id"], u["bac"]) for u in (env["data"] or {}).get("ung_vien") or []]


def test_kq050_GAN_sau_khi_luot_lenh_TRUOC_ve_muon_KHONG_mang_itl_ma_cua_lenh_truoc(ca_tra):
    """`mo_lenh(X)` *(giữ)* → `mo_lenh(Y)` *(như phím `j`)* → thả `Y` → thả `X`
    *(muộn)* → bấm hàng ứng viên **đầu** + `Gán` *(hai lần nếu xác nhận lệch)*.

    Mong: danh sách = thân cửa của `Y`; cú ghi duy nhất = `/queue/<itl mã của
    Y>/match {pm_line_ids: [Y]}`. ⛔ Chiều ĐỎ *(mã `db0adae`)*: danh sách của
    `X` đè lên ⇒ `/queue/<itl mã của X>/match {pm_line_ids: [Y]}` — cặp mà
    bài ⓑ chứng minh cửa ghi **nhận**."""
    ca, Dg, TRA = ca_tra
    X, Y = ca["lenh"]["X"], ca["lenh"]["Y"]
    iX, iY = ca["i"]["X"], ca["i"]["Y"]
    uX, uY = _uv(TRA[Dg["uv_X"]]), _uv(TRA[Dg["uv_Y"]])
    # ⭐ tự chứng ca *(Đ3)*: hàng đầu của mỗi lệnh = dòng tiền MÃ của chính nó
    assert uX and uX[0] == (iX, "ma"), ("⛔ không đo được: ca X lệch", uX[:3])
    assert uY and uY[0] == (iY, "ma"), ("⛔ không đo được: ca Y lệch", uY[:3])
    r = _chay(CUA_GIU + nap(TRA) + f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates');
      const px = F01G.mo_lenh({X!r}).catch(e => 'ném: ' + e.message); await _cho();
      const py = F01G.mo_lenh({Y!r}).catch(e => 'ném: ' + e.message); await _cho();
      await _tha('/lenh/{Y}/itl-candidates');
      await _tha('/lenh/{X}/itl-candidates');
      const ra = [await px, await py];
      const uv = F01G.ST.ung_vien.map(u => u.itl_id);
      const mo = F01G.ST.mo;   /* ⚠ đọc TRƯỚC Gán — Gán xong màn tự sang lệnh kế */
      const hang = document.querySelectorAll('.cands .cand');
      _bam(hang[0]); await _cho();
      for (let k = 0; k < 2 && !_ghi().length; k++) {{
        _bam(document.querySelectorAll('.act button')[0]); await _cho();
      }}
      return {{ra, mo, uv, dom: hang.length, ghi: _ghi()}};
    """, tep=TEP_F01, vo=VO_F01)
    assert r["mo"] == Y, r
    assert r["uv"] == [u[0] for u in uY], ("⛔ danh sách ⛔ phải của Y", r["uv"][:5])
    sai = [g for g in r["ghi"] if g[0] == f"/queue/{iX}/match"]
    assert not sai, f"⛔ GÁN itl mã của lệnh X kèm lệnh Y (cặp sai CÙNG tệ): {sai}"
    assert r["ghi"] == [[f"/queue/{iY}/match", {"pm_line_ids": [Y]}]], r["ghi"]


def test_kq050_SU_THAT_cua_ghi_NHAN_cap_sai_cung_te_trong_dung_sai(ca_tra):
    """`mong` = **200**: cửa ghi ⛔ biết ý người — cặp *(dòng tiền mã `FT50X…`,
    lệnh `Y`)* lệch 500 đ ≤ dung sai ⇒ nhận. Đó là lý do ① phải chặn ở **màn**.
    Đối chứng cùng lượt: cặp **đúng mã** *(dòng tiền `X`, lệnh `X`)* lệch
    1.500 đ ⇒ `422`. Dọn: `unmatch` mối nối vừa ghi *(kho TEST)*."""
    ca, _Dg, _TRA = ca_tra
    X, Y = ca["lenh"]["X"], ca["lenh"]["Y"]
    iX = ca["i"]["X"]
    with _may() as m:
        ma_dung, r_dung = _goi(m, f"{V}/queue/{iX}/match", pt="POST",
                               than={"pm_line_ids": [X], "reason": "KQ-050 doi chung"})
        ma_sai, r_sai = _goi(m, f"{V}/queue/{iX}/match", pt="POST",
                             than={"pm_line_ids": [Y], "reason": "KQ-050 cap sai"})
        if ma_sai == 200:
            _goi(m, f"{V}/queue/{iX}/unmatch", pt="POST",
                 than={"reason": "KQ-050 don ca"})
    assert ma_dung == 422, ("⛔ đối chứng: cặp đúng mã lệch 1.500 phải bị chặn",
                            ma_dung, r_dung)
    assert ma_sai == 200, ("cửa ghi ĐÃ chặn cặp sai trong dung sai — sự thật "
                           "đổi, khai lại bài này", ma_sai, r_sai)
