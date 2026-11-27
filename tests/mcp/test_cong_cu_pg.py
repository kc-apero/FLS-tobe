"""AC-2 · AC-5 · AC-6 — client MCP THẬT (SDK `mcp.client.Client`) gọi TỪNG công cụ vào máy chủ (trong tiến trình)
trên kho TEST đã nạp mẫu ⇒ con số khớp phép đếm TRỰC TIẾP; nhật ký đủ trường, ⛔ nội dung; trần tốc độ.
"""
from __future__ import annotations

import json

import anyio
import psycopg
import pytest

from fls.api import bang_tuyen
from fls.api.xu_ly import HAM, YeuCau, pham_vi_cua_yeu_cau
from fls.mcp import may_chu
from fls.mcp.cong_cu import CauHinh, CongCu, LoiCongCu, bam_sql
from tests.mcp.conftest import mo_doc_vai

pytestmark = pytest.mark.pg

SAU_CONG_CU = ["liet_ke_bang", "mo_ta_bang", "truy_van_doc", "liet_ke_tuyen", "goi_tuyen", "cong"]


def _goi_sdk(cc: CongCu, *lich: tuple[str, dict]) -> tuple[list[str], list]:
    from mcp.client import Client
    may = may_chu.tao_may(cc, nguoi=lambda: "bai-thu@fls")
    ra: list = []

    async def chay():
        async with Client(may) as c:
            ten = [t.name for t in (await c.list_tools()).tools]
            for t, a in lich:
                r = await c.call_tool(t, a)
                ra.append(r)
            return ten
    return anyio.run(chay), ra


def _sc(r) -> dict:
    """Nội dung công cụ = MỘT khối văn bản JSON (cái Claude đọc)."""
    assert not r.is_error, r.content
    assert len(r.content) == 1 and r.content[0].type == "text"
    return json.loads(r.content[0].text)


def test_sdk_thay_DUNG_sau_cong_cu_va_moi_cai_CHI_DOC(cong_cu):
    from mcp.client import Client
    may = may_chu.tao_may(cong_cu, nguoi=lambda: "x")

    async def chay():
        async with Client(may) as c:
            return (await c.list_tools()).tools
    tools = anyio.run(chay)
    assert [t.name for t in tools] == SAU_CONG_CU
    assert all(t.annotations.read_only_hint is True and t.annotations.destructive_hint is False for t in tools)


def test_liet_ke_bang_khop_dem_TRUC_TIEP(cong_cu, kho_mcp):
    _, (r,) = _goi_sdk(cong_cu, ("liet_ke_bang", {}))
    bang = {b["ten"]: b for b in _sc(r)["bang"]}
    with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
        so_bang = c.execute("select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace"
                            " where n.nspname='public' and c.relkind in ('r','p','v','m')").fetchone()[0]
        for t in ("fls_itl", "fls_run", "fls_pm_line", "fls_moi_noi"):
            assert bang[t]["so_dong"] == c.execute(f"select count(*) from {t}").fetchone()[0], t
    assert so_bang > 0 and len(bang) == so_bang
    assert bang["fls_itl"]["so_dong"] >= 3 and bang["fls_moi_noi"]["loai"] == "view"


def test_mo_ta_bang_dung_cot_va_TU_CHOI_bang_la(cong_cu, kho_mcp):
    _, (r, r2) = _goi_sdk(cong_cu, ("mo_ta_bang", {"ten": "fls_pm_line"}),
                          ("mo_ta_bang", {"ten": "pg_authid"}))
    d = _sc(r)
    with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
        mong = [x for (x,) in c.execute("select column_name from information_schema.columns where "
                                         "table_schema='public' and table_name='fls_pm_line' order by ordinal_position")]
    assert [x["ten"] for x in d["cot"]] == mong and len(mong) == 18
    assert {x["ten"]: x["kieu"] for x in d["cot"]}["tho"] == "json"
    assert r2.is_error and "KHONG_CO_BANG" in r2.content[0].text


def test_truy_van_doc_TIEN_la_CHUOI_va_dung_so(cong_cu, kho_mcp):
    sql = (f"select doc_no, curr, ps_no from fls_itl where run_id = '{kho_mcp['run']}' order by source_row")
    _, (r,) = _goi_sdk(cong_cu, ("truy_van_doc", {"sql": sql}))
    d = _sc(r)
    assert d["cot"] == ["doc_no", "curr", "ps_no"]
    assert d["dong"] == [["FT-MCP-0", "VND", "1500000.00"], ["FT-MCP-1", "USD", "2500.50"],
                         ["FT-MCP-2", "VND", "700000.00"]]
    assert (d["so_dong"], d["bi_cat"]) == (3, False)


def test_truy_van_doc_TRAN_dong_va_bi_cat(cong_cu, kho_mcp):
    sql = f"select itl_id from fls_itl where run_id = '{kho_mcp['run']}'"
    _, (r1, r2) = _goi_sdk(cong_cu, ("truy_van_doc", {"sql": sql, "gioi_han": 2}),
                           ("truy_van_doc", {"sql": "select generate_series(1, 5000)", "gioi_han": 99999}))
    assert (_sc(r1)["so_dong"], _sc(r1)["bi_cat"], _sc(r1)["ly_do_cat"]) == (2, True, "tran_dong")
    assert (_sc(r2)["so_dong"], _sc(r2)["gioi_han"], _sc(r2)["bi_cat"]) == (1000, 1000, True)


def test_truy_van_doc_TRAN_byte(kho_mcp, nhat_ky):
    cc = CongCu(mo_doc_vai(kho_mcp["dsn_doc"]), CauHinh(tran_byte=200, toc_do_phut=1000), ghi_nhat_ky=nhat_ky.append)
    d = cc.truy_van_doc("x", "select repeat('a', 50) from generate_series(1, 20)")
    assert d["bi_cat"] and d["ly_do_cat"] == "tran_byte" and 0 < d["so_dong"] < 20


def test_truy_van_doc_HET_HAN_bi_huy(cong_cu):
    """Lớp 1 chặn `pg_sleep` theo TÊN; hạn giờ vẫn phải cắn câu chậm KHÔNG mang tên ấy."""
    with pytest.raises(LoiCongCu) as e:
        cong_cu.truy_van_doc("x", "select count(*) from generate_series(1, 300000000)")
    assert e.value.ma == "KHO_TU_CHOI" and "57014" in e.value.chi_tiet


def test_liet_ke_tuyen_DUNG_cac_tuyen_doc_cua_cua(cong_cu):
    _, (r,) = _goi_sdk(cong_cu, ("liet_ke_tuyen", {}))
    mong = [t for t in bang_tuyen.BANG_TUYEN if t.phuong_thuc == "GET" and not t.ghi]
    ten = [x["ten"] for x in _sc(r)["tuyen"]]
    assert len(ten) == len(set(ten)) == len(mong) == 31          # tên hàm DUY NHẤT ⇒ khoá được
    assert "sua" not in ten and "ghep" not in ten                 # tuyến GHI ⛔ lộ


def test_goi_tuyen_TRA_DUNG_ham_cua_cua(cong_cu, kho_mcp):
    """⛔ viết lại logic: dữ liệu = gọi THẲNG `HAM[...]` của cửa trên cùng kho."""
    itl = kho_mcp["itl"][1]
    q = {"run_id": kho_mcp["run"]}
    _, (r1, r2, r3) = _goi_sdk(cong_cu, ("goi_tuyen", {"ten": "mot_dong", "tham_so": {"itl_id": str(itl), **q}}),
                               ("goi_tuyen", {"ten": "hang_cho_tom", "tham_so": q}),
                               ("goi_tuyen", {"ten": "sua", "tham_so": {"itl_id": str(itl)}}))
    from fls.api import bao
    for r, ten, tham in ((r1, "mot_dong", {"itl_id": str(itl)}), (r2, "hang_cho_tom", {})):
        with mo_doc_vai(kho_mcp["dsn_doc"])() as conn:
            data, _ = HAM[ten](YeuCau(conn=conn, pv=pham_vi_cua_yeu_cau(q), q=q, tham=tham, actor="x"))
        mong = json.loads(bao.dong_goi(data, bao.meta("x")))["data"]
        assert _sc(r)["data"] == mong, ten
    assert _sc(r1)["data"]["itl_id"] == itl
    assert r3.is_error and "KHONG_CO_TUYEN" in r3.content[0].text


def test_cong_la_tuyen_gates(cong_cu):
    _, (r,) = _goi_sdk(cong_cu, ("cong", {}))
    ma = [c["ma"] for c in _sc(r)["data"]["cong"]]
    assert "KHO_SACH" in ma and len(ma) >= 5


def test_Email_Address_KHONG_co_trong_kho(cong_cu, kho_mcp):
    """`PM_COT_RIENG_TU` đo LẠI qua chính MCP — kèm MẪU SỐ (`Đ3`)."""
    d = cong_cu.truy_van_doc("x", (
        "select (select count(*) from information_schema.columns where table_schema='public') as so_cot,"
        " (select count(*) from information_schema.columns where table_schema='public' and column_name ilike"
        " '%email%') as cot_email,"
        " (select count(*) from fls_pm_line where tho is not null) as dong_tho,"
        " (select count(*) from fls_pm_line where tho::jsonb ? 'Email Address') as dong_email"))
    so_cot, cot_email, dong_tho, dong_email = d["dong"][0]
    assert so_cot > 100 and dong_tho >= 2                          # tập ⛔ rỗng
    assert (cot_email, dong_email) == (0, 0)


def test_nhat_ky_DU_truong_va_KHONG_noi_dung(cong_cu, nhat_ky, kho_mcp):
    sql = f"select doc_no from fls_itl where run_id = '{kho_mcp['run']}'"
    cong_cu.truy_van_doc("chu@vi.du", sql)
    with pytest.raises(LoiCongCu):
        cong_cu.truy_van_doc("chu@vi.du", "delete from fls_itl")
    a, b = nhat_ky[-2:]
    assert set(a) == {"ai", "cong_cu", "sql_bam", "so_dong", "ms", "ket_qua"}
    assert (a["ai"], a["cong_cu"], a["sql_bam"], a["so_dong"], a["ket_qua"]) == (
        "chu@vi.du", "truy_van_doc", bam_sql(sql), 3, "ok")
    assert b["ket_qua"] == "CHAN_SQL_KHONG_PHAI_SELECT"
    vet = json.dumps(nhat_ky, ensure_ascii=False)
    assert "FT-MCP" not in vet and "fls_itl" not in vet              # ⛔ nội dung trả về, ⛔ câu SQL


def test_TRAN_TOC_DO_theo_nguoi(kho_mcp, nhat_ky):
    gio = [1000.0]
    cc = CongCu(mo_doc_vai(kho_mcp["dsn_doc"]), CauHinh(toc_do_phut=3), ghi_nhat_ky=nhat_ky.append)
    cc.toc_do.dong_ho = lambda: gio[0]
    for _ in range(3):
        cc.liet_ke_tuyen("a")
    with pytest.raises(LoiCongCu) as e:
        cc.liet_ke_tuyen("a")
    assert e.value.ma == "QUA_NHANH" and nhat_ky[-1]["ket_qua"] == "QUA_NHANH"
    cc.liet_ke_tuyen("b")                                             # người KHÁC ⛔ bị liên luỵ
    gio[0] += 60
    cc.liet_ke_tuyen("a")                                             # hết cửa sổ ⇒ gọi lại được


def test_ket_noi_GHI_duoc_thi_chay_mcp_TU_CHOI_chay(kho_mcp, monkeypatch):
    """`tools/chay_mcp.py` kiểm `kiem_truoc_khi_mo` ⇒ một `PG_DSN` ghi được làm máy NỔ trước khi nghe."""
    import contextlib
    import tools.chay_mcp as cm

    @contextlib.contextmanager
    def mo_ghi():
        with psycopg.connect(kho_mcp["dsn"], autocommit=True) as c:
            yield c
    monkeypatch.setattr(cm, "mo_doc", lambda dsn: mo_ghi)
    with pytest.raises(RuntimeError, match="GHI duoc"):
        cm.main([])


def test_STDIO_tien_trinh_that_dung_lenh_cua_mcp_json(kho_mcp):
    """AC-1 · MỘT mã: tiến trình con `tools/chay_mcp.py` (đúng lệnh `.mcp.json`) nói MCP qua stdio — SDK client."""
    import os
    import sys
    from pathlib import Path
    from mcp.client import Client
    from mcp.client.stdio import StdioServerParameters

    goc = Path(__file__).resolve().parents[2]
    env = {**os.environ, "PG_DSN": kho_mcp["dsn_doc"], "PYTHONUTF8": "1", "FLS_MCP_NGUOI": "stdio-bai"}
    p = StdioServerParameters(command=sys.executable, args=["tools/chay_mcp.py"], env=env, cwd=str(goc))

    async def chay():
        async with Client(p) as c:
            r = await c.call_tool("truy_van_doc", {"sql": f"select count(*) from fls_itl where run_id = '{kho_mcp['run']}'"})
            return json.loads(r.content[0].text)
    assert anyio.run(chay)["dong"] == [[3]]
