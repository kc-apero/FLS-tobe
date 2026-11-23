# -*- coding: utf-8 -*-
"""`WO-023` `(d)` · `BA-06` **v4.11** `ⓕ4` · `BA-07` **v3.5** §5 — nợ `409` trả
xong: **mỗi chuyện một mã**.

⛔⛔ Lỗi gốc *(mã khi nhận `7e67a09`)*: `FLS-CONFLICT-SOURCE` bị **bốn** lớp lỗi
dùng chung *(`fls/repo/ghi_tay.py` — `KhacNguon` · `DaGhep` · `ChuaXong` ·
`KhongCoMoiNoi`)* ⇒ `goi_cua.js` dịch cả bốn thành *"Giá trị bạn gõ khác với
giá trị nguồn đang có."* — đúng cho **một**, sai cho **ba** *(`KQ-021` ca **K**:
người khác bỏ gán trước ⇒ màn nói "giá trị bạn gõ khác…")*.

⭐ Đo qua **cửa HTTP thật** trên **kho TEST** *(`dung_ca_wo023` — `assert
current_database() = 'fls_test'`)*. Mẫu số *(`Đ3`)*: **4** ca, **4** mã khác
nhau, cùng `409`.
"""
from __future__ import annotations

import re
import uuid
from decimal import Decimal as D
from pathlib import Path

import psycopg
import pytest

from fls.api import bao
from fls.db.kho import dsn_test
from tests.web.ca_wo023 import dung_ca_wo023
from tests.web.test_vong_f02_pg import V, _goi, _may

pytestmark = pytest.mark.pg

GOC = Path(__file__).resolve().parents[2]


@pytest.fixture(scope="module")
def ca():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo023(c)
        # ⭐ một dòng **có nguồn** `hd` *(ca `KhacNguon` — `US-025`)* trong
        #   cùng lần nạp *(phạm vi `lan nap that`)*
        ca["co_nguon"] = c.execute(
            "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
            " source_row, run_id, contract_version, canon_version,"
            " mapping_version, raw_frozen, canon, curr, ps_co, work_status, hd)"
            " VALUES (%s,'RAW','L1',99,%s,'v1.0','v1.0','v1.0',false,'{}',"
            " 'VND',%s,'UNMAPPED','HD-NGUON-23') RETURNING itl_id",
            (uuid.uuid4().hex, ca["run"], D("1000"))).fetchone()[0]
    return ca


def test_AC4_BON_ca_409_BON_ma_qua_cua_that(ca):
    """`match` dòng **đã** ghép ⇒ `FLS-DA-GHEP` · `unmatch` dòng ⛔ mối nối ⇒
    `FLS-KHONG-CON-MOI-NOI` · `reopen` dòng chưa xong ⇒ `FLS-CHUA-XONG` ·
    `/adjust` khác nguồn ⇒ `FLS-CONFLICT-SOURCE` *(giữ `khac`)*.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: ba ca đầu ra `FLS-CONFLICT-SOURCE`."""
    i, L, L2 = ca["i"], ca["lenh"], ca["lenh2"]
    ra = {}
    with _may() as m:
        st, r = _goi(m, f"{V}/queue/{i['M2']}/match", pt="POST",
                     than={"pm_line_ids": [L]})
        assert st == 200, ("⛔ không đo được: ghép lần đầu ⛔ vào", st, r)
        ra["da_ghep"] = _goi(m, f"{V}/queue/{i['M2']}/match", pt="POST",
                             than={"pm_line_ids": [L2]})
        ra["khong_moi_noi"] = _goi(m, f"{V}/queue/{i['M3']}/unmatch",
                                   pt="POST", than={})
        ra["chua_xong"] = _goi(m, f"{V}/queue/{i['M3']}/reopen", pt="POST",
                               than={"reason": "thu WO-023 (d)"})
        ra["khac_nguon"] = _goi(m, f"{V}/ledger/{ca['co_nguon']}/adjust",
                                pt="POST", than={"field": "hd", "value": "HD-KHAC",
                                                 "reason": "thu"})
    ma = {k: (st, (r.get("error") or {}).get("code")) for k, (st, r) in ra.items()}
    assert {st for st, _ in ma.values()} == {409}, ma
    assert ma == {"da_ghep": (409, "FLS-DA-GHEP"),
                  "khong_moi_noi": (409, "FLS-KHONG-CON-MOI-NOI"),
                  "chua_xong": (409, "FLS-CHUA-XONG"),
                  "khac_nguon": (409, "FLS-CONFLICT-SOURCE")}, ma
    assert len({c for _, c in ma.values()}) == 4
    # ⭐ khuôn thân ⛔ đổi: `DaGhep` vẫn mang `khac.moi_noi`; `KhacNguon` `khac.nguon`
    assert (ra["da_ghep"][1]["error"].get("khac") or {}).get("moi_noi"), ra["da_ghep"]
    assert ra["khac_nguon"][1]["error"]["khac"] == {"nguon": "HD-NGUON-23"}


def test_AC4_BA_ma_moi_khai_409_trong_MA_LOI():
    for ma in ("FLS-DA-GHEP", "FLS-KHONG-CON-MOI-NOI", "FLS-CHUA-XONG"):
        assert bao.MA_LOI.get(ma, (None,))[0] == 409, ma


def test_AC4_ghi_tay_CHI_con_MOT_lop_mang_CONFLICT_SOURCE():
    """`grep -c 'ma = "FLS-CONFLICT-SOURCE"' fls/repo/ghi_tay.py` = **1**
    *(hôm nay **4**)*."""
    s = (GOC / "fls" / "repo" / "ghi_tay.py").read_text(encoding="utf-8")
    assert len(re.findall(r'ma = "FLS-CONFLICT-SOURCE"', s)) == 1
