# -*- coding: utf-8 -*-
"""`WO-022` **vòng 3** *(`KQ-029` `F-1`)* — hộp **"Tìm tiền"** `F01L` nuôi bằng
**thân CỬA THẬT**, và một cổng quét để lớp lỗi này ⛔ lặp ở cửa khác của `F01L`.

⛔⛔ **Lỗi ĐÃ ĐO, ⛔ không phải lo xa** *(`fls-test`, Chrome thật `8099` kho TEST
+ `8088` sổ thật, 02/10)*: cửa `GET /queue/lenh/{id}/itl-candidates` trả
**khuôn `⓵`** `BA-07 §4h` từ `23/09` *(`GAP-API-10` — `amount` · `lech` ·
`dien_giai`, nắn ở `fls/repo/man_ghep.py::khuon_ung_vien`)*, còn
`man_f01_lenh.js::_drawer_tim_tien` vẫn đọc **khoá hàng thô** `u.tien` ·
`u.lech_tuyet_doi` · `u.memo` ⇒ cột `Tiền`/`Lệch` in `—`, `Diễn giải` trống, và
câu *"⛔ VƯỢT dung sai — cửa ghi sẽ TỪ CHỐI"* cho **MỌI** ứng viên — kể cả ứng
viên khớp **đúng từng xu**, một cặp mà cửa ghi **nhận**.

⛔⛔ **Vì sao bộ bài `WO-022` vòng 1–2 xanh mà màn sai.** Bài `AC-6` hộp *Tìm
tiền* *(`test_wo022_tien_theo_tien_te.py`)* **tự nhét** thân cửa
`{tien: '1234.16', lech_tuyet_doi: '0.40'}` — đúng khuôn người viết **tưởng**,
⛔ khuôn cửa trả. Đây là **lần thứ hai** cùng lớp *"khuôn thử tự nhét state che
chỗ màn không đọc đúng cửa"* *(lần trước: `HT.hoi` ở `KQ-019`; bia ở `11` §6)*.
Bài cũ ⛔ có cách nào đỏ: nó đặt **cả** câu hỏi **lẫn** câu trả lời.

⭐ Tệp này làm ba việc:
  ⓐ **Khuôn dựng chung** `ca_cua_that` — dữ liệu thật trên **kho TEST** *(run
     `NAP-2000-01-01-…`, ⛔ kho thật)*, rồi gọi **cửa thật qua HTTP** cho mọi
     đường màn `F01L` cần *(danh sách lệnh · tóm tắt · ứng viên · nhìn đủ PM)*.
     ⛔ Một khoá nào trong thân do bài đặt. Bài `AC-6` viết lại *(`AC-17`)*
     dùng khuôn này.
  ⓑ **Bài hành vi** hộp *Tìm tiền* — ứng viên khớp đúng ⇒ *"trong dung sai"*,
     cột Tiền/Lệch/Diễn giải in đúng.
  ⓒ ⭐ **Cổng quét khoá** — đọc **mã nguồn** `man_f01_lenh.js`, gom mọi khoá
     mà hàm vẽ đọc từ thân cửa *(`u.<khoá>`, `d.<khoá>`, `x.<khoá>`)*, rồi đòi
     **mỗi** khoá có trong thân **cửa thật** trả trên kho TEST. Khuôn thử tự
     nhét ở **nơi khác** trong `tests/web/**` cho cùng cửa cũng phải ⊆ khoá
     cửa thật — vì đó chính là chỗ lỗi trốn.

⛔ Tiền của bài **ngẫu nhiên mỗi lần** *(phần nguyên)* — kho TEST **phình**
*(bia `fls-test-store-grows-unbounded`)*: ứng viên sắp theo `(bậc, lệch,
itl_id)`, nên một số cố định như `1234.56` mà các lần chạy trước để lại hàng
chục dòng sẽ đẩy dòng của lần này ra **ngoài** `limit=50` ⇒ bài đo trên tập
**không chứa** dòng của nó *(`Đ3`)*.
"""
from __future__ import annotations

import json
import os
import random
import re
import uuid
from decimal import Decimal as D

import pytest

from fls.web import phuc_vu as pv
from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import _lenh, _run, conn  # noqa: F401
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg

#: Diễn giải sao kê của hai dòng tiền — đi vào kho TEST qua **đúng đường** cửa
#: đọc *(`fls_chup_dong.o ->> 'Description'` ⇒ khung xem `fls_dien_giai`)*,
#: ⛔ nhét vào thân cửa.
DG_KHOP = "CK khop dung tung xu WO022V3"
DG_LECH = "CK lech bon muoi xu WO022V3"


def _dong_tien(conn, run: str, sid_key: str, dong_so: int, tien: str) -> int:  # noqa: F811
    """Một dòng `fls_itl` USD chưa nối — `source_sheet`/`source_row` trỏ đúng
    dòng chụp mang `Description`, để cửa nối ra `dien_giai` **thật**."""
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW',%s,%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " 'FT-V3','USD',%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, sid_key, dong_so, run, D(tien))).fetchone()[0]


def dung_ca(conn) -> dict:  # noqa: F811
    """Dựng một ca trên **kho TEST** và trả số liệu để gọi cửa.

    Lệnh USD `<N>.56` · hai dòng tiền USD chưa nối: `<N>.56` *(khớp đúng)* và
    `<N>.16` *(lệch `0,40`)* · lệnh thứ hai cùng phiếu *(để cửa "nhìn đủ PM"
    trả `ca_phieu` — `_panel_pm` đọc nó)*. ⛔ Ghi gì vào kho THẬT: bài assert
    `current_database()`."""
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ khuôn này chỉ được dựng trên kho TEST, gặp {db!r}"
    n = random.randint(100_000, 899_999)
    run = _run(conn)
    khoa = "R | WO022V3 " + uuid.uuid4().hex[:8]
    sid = conn.execute("INSERT INTO fls_source (source_key, src_type)"
                       " VALUES (%s,'Bank') RETURNING source_id",
                       (khoa,)).fetchone()[0]
    cid = conn.execute("INSERT INTO fls_chup (spreadsheet_id, lan, actor)"
                       " VALUES ('SS-WO022V3','Bank','fls-dev@apero.vn')"
                       " RETURNING chup_id").fetchone()[0]
    for so, dg in ((0, DG_KHOP), (1, DG_LECH)):
        conn.execute("INSERT INTO fls_chup_dong (chup_id, source_id, dong_so, o)"
                     " VALUES (%s,%s,%s,%s::jsonb)",
                     (cid, sid, so, json.dumps({"Description": dg})))
    khop = _dong_tien(conn, run, khoa, 0, f"{n}.56")
    lech = _dong_tien(conn, run, khoa, 1, f"{n}.16")
    ma = "PW" + uuid.uuid4().hex[:6].upper()
    _lenh(conn, run, (ma + "-1", f"{n}.56", "USD", "Approve", "HD-V3", "C-V3"),
          (ma + "-2", "10.00", "USD", "Approve", "HD-V3", "C-V3"))
    return {"n": n, "ma": ma + "-1", "khop": khop, "lech": lech}


def goi_cua(may, ca: dict) -> dict:  # noqa: F811
    """Gọi **cửa thật** cho mọi đường `F01L` đọc khi mở hộp *Tìm tiền*.

    ⭐ Trả `{đường màn gọi: thân 'data' cửa trả}` — đúng khoá `_TRA` của khung
      node, để kịch bản đưa **nguyên** thân vào hàm vẽ thật."""
    ma = ca["ma"]
    duong = {
        "/queue/lenh-cho/summary": f"{V}/queue/lenh-cho/summary",
        "/queue/lenh-cho?limit=50&curr=USD":
            f"{V}/queue/lenh-cho?limit=50&curr=USD",
        f"/queue/lenh/{ma}/itl-candidates":
            f"{V}/queue/lenh/{ma}/itl-candidates?limit=50",
        f"/queue/lenh/{ma}": f"{V}/queue/lenh/{ma}",
    }
    ra = {}
    for k, url in duong.items():
        ok, r = _goi(may, url)
        assert ok == 200, (url, r)
        ra[k] = r["data"]
    ids = [u["itl_id"] for u in ra[f"/queue/lenh/{ma}/itl-candidates"]["ung_vien"]]
    # ⛔ `Đ3`: tập ứng viên phải CHỨA đúng hai dòng của bài — ⛔ đo trên tập rỗng
    assert ca["khop"] in ids and ca["lech"] in ids, (
        f"⛔ không đo được: cửa ⛔ trả hai dòng tiền của bài "
        f"({ca['khop']}, {ca['lech']}) trong {len(ids)} ứng viên")
    dong = [x for x in ra["/queue/lenh-cho?limit=50&curr=USD"]["rows"]
            if x.get("pm_line_id") == ma]
    assert len(dong) == 1, f"⛔ cửa danh sách lệnh ⛔ trả đúng một dòng {ma}: {dong}"
    ra["_dong"] = dong[0]
    return ra


@pytest.fixture()
def ca_cua_that(conn, may):  # noqa: F811
    """`(ca, thân cửa thật theo đường)` — ⭐ khuôn dựng chung của vòng 3."""
    ca = dung_ca(conn)
    return ca, goi_cua(may, ca)


def tien_usd(n: int, xu: str) -> str:
    """Chuỗi mong in theo §5b ⓐ — `.` nghìn, `,` thập phân."""
    return f"{n:,}".replace(",", ".") + "," + xu


#: Kịch bản node: đưa NGUYÊN thân cửa thật vào `_TRA`, mở hộp *Tìm tiền* bằng
#: **chính dòng** cửa danh sách lệnh trả, chọn ứng viên `i` *(sự kiện `change`
#: như trình duyệt)*.
KICH_BAN_HOP = """
  const TRA = %(tra)s;
  for (const k of Object.keys(TRA)) if (k[0] === '/') _TRA[k] = {data: TRA[k]};
  const s = document.createElement('div'); s.id = 'sig-l';
  document.body.appendChild(s);
  await F01L._drawer_tim_tien(TRA._dong);
  const b = document.getElementById('dlg-b');
  const c = document.createElement('input');
  c.type = 'radio'; c.name = 'uv'; c.checked = true; c.dataset.i = '%(i)d';
  b.appendChild(c);
  (b._nghe.change || []).forEach(f => f({target: b}));
  return {hop: b.innerHTML, sig: s.innerHTML,
          tom: globalThis._tom || null};
"""


def mo_hop(ca: dict, tra: dict, itl_id: int, kich_truoc: str = "") -> dict:
    """Mở hộp thật với thân cửa thật, chọn dòng tiền `itl_id`."""
    ma = ca["ma"]
    i = [u["itl_id"] for u in
         tra[f"/queue/lenh/{ma}/itl-candidates"]["ung_vien"]].index(itl_id)
    return _chay(kich_truoc + KICH_BAN_HOP % {
        "tra": json.dumps(tra, ensure_ascii=False, default=str), "i": i},
        tep=TEP_F01, vo=VO_F01)


# ═══ ⓑ hành vi — ứng viên KHỚP ĐÚNG ⇒ trong dung sai ═════════════════════
@can_node
def test_AC16_tim_tien_THAN_CUA_THAT_khop_DUNG_xu_la_TRONG_dung_sai(ca_cua_that):
    """Chọn dòng `<N>.56` *(bậc `tien` — khớp đúng xu)* trên thân **cửa thật** ⇒
    `lệch <b>0,00</b>` + *"trong dung sai"*; cột `Tiền` in `<N>,56`, cột
    `Diễn giải` in diễn giải sao kê thật.

    ⛔ Chiều ĐỎ *(đã chạy trên `a69ee92`)*: màn đọc `u.tien` ⇒ `TP.xu(undefined)`
    ⇒ `null` ⇒ *"lệch ⛔ không tính được ⇒ VƯỢT dung sai — cửa ghi sẽ TỪ
    CHỐI"* ⇒ ĐỎ; đọc `u.memo` ⇒ diễn giải trống ⇒ ĐỎ."""
    ca, tra = ca_cua_that
    r = mo_hop(ca, tra, ca["khop"])
    assert "TỪ CHỐI" not in r["sig"] and "không tính được" not in r["sig"], r["sig"]
    assert "lệch <b>0,00</b>" in r["sig"], r["sig"]
    assert "trong dung sai" in r["sig"], r["sig"]
    assert ("tiền bank <b>" + tien_usd(ca["n"], "56") + "</b>") in r["sig"], r["sig"]
    assert tien_usd(ca["n"], "56") in r["hop"], r["hop"][:800]
    assert DG_KHOP in r["hop"] and DG_LECH in r["hop"], r["hop"][:800]


# ═══ ⓒ CỔNG QUÉT KHOÁ — màn đọc gì thì cửa thật phải trả nấy ═══════════════
#: ⭐ Mỗi hàng: *(hàm trong `man_f01_lenh.js`, {biến trong hàm: (đường màn
#: gọi, đường vào thân)})*. Đường `()` = gốc `data`; `("ung_vien",)` = từng phần
#: tử của mảng ấy. ⛔ Đây ⛔ phải danh sách miễn trừ — nó là **bản đồ** biến ⇒
#: cửa; khoá được đọc lấy từ **mã nguồn**, khoá được trả lấy từ **cửa thật**.
#: ⚠ `r` của `_drawer_tim_tien` là **dòng cửa danh sách lệnh** *(nút `Duyệt`
#: truyền nguyên dòng lưới)* ⇒ đo trên cửa ấy.
#: ⚠ Một hàm mới của `F01L` gọi cửa theo một lệnh ⇒ thêm một hàng *(bài
#: `test_AC16_moi_ham_goi_cua…` đỏ cho tới khi thêm)*.
_UV_DUONG = "/queue/lenh/{ma}/itl-candidates"
_LUOI_DUONG = "/queue/lenh-cho?limit=50&curr=USD"
BAN_DO = [
    ("_drawer_tim_tien", {"d": (_UV_DUONG, ()),
                          "u": (_UV_DUONG, ("ung_vien",)),
                          "r": (_LUOI_DUONG, ("rows",))}),
    ("_panel_pm", {"d": ("/queue/lenh/{ma}", ()),
                   "x": ("/queue/lenh/{ma}", ("ca_phieu",))}),
]

TEP_F01L = os.path.join(pv.THU_MUC, "man_f01_lenh.js")


def _than_ham(nguon: str, ten: str) -> str:
    """Thân một hàm theo **đếm ngoặc** *(⛔ regex tới `}` đầu tiên — thân có
    hàm lồng `_tinh`)*. Mẫu `function <ten>(` phải gặp **đúng một** lần."""
    mau = re.compile(r"function\s+" + re.escape(ten) + r"\s*\(")
    gap = list(mau.finditer(nguon))
    assert len(gap) == 1, f"⛔ không đo được: `function {ten}(` gặp {len(gap)} lần"
    i = nguon.index("{", gap[0].end())
    sau, j = 0, i
    while True:
        c = nguon[j]
        sau += (c == "{") - (c == "}")
        j += 1
        if sau == 0:
            return nguon[i:j]


def khoa_man_doc(than: str, bien: str) -> set[str]:
    """Mọi khoá `bien.<k>` / `bien['k']` trong thân hàm — ⛔ tính chú thích."""
    sach = re.sub(r"/\*.*?\*/", "", than, flags=re.S)
    sach = re.sub(r"(?m)//.*$", "", sach)
    return (set(re.findall(r"(?<![\w.$])" + re.escape(bien) + r"\.(\w+)", sach))
            | set(re.findall(r"(?<![\w.$])" + re.escape(bien)
                             + r"\[['\"](\w+)['\"]\]", sach)))


def khoa_cua_tra(than, duong: tuple) -> set[str]:
    """Hợp mọi khoá ở `duong` trong thân cửa. ⛔ Mảng rỗng ⇒ ĐỎ *(`Đ3`)*."""
    if not duong:
        assert isinstance(than, dict), than
        return set(than)
    ds = than.get(duong[0]) or []
    assert ds, f"⛔ không đo được: cửa trả `{duong[0]}` rỗng — ⛔ đo trên tập rỗng"
    return set().union(*(set(x) for x in ds))


def test_AC16_MOI_khoa_F01L_doc_tu_than_cua_DEU_CO_trong_CUA_THAT(ca_cua_that):
    """⭐⭐ Cổng **quét**: mọi khoá hàm vẽ `F01L` đọc từ thân cửa phải nằm trong
    tập khoá **cửa thật** trả *(kho TEST, HTTP)*.

    ⛔⛔ Vì sao quét **mã nguồn** thay vì liệt kê tay: một danh sách gõ tay sẽ
       **trôi** khỏi màn, và lúc ấy cổng canh một màn ⛔ còn tồn tại *(tiền lệ
       `test_ten_truong_man_F02_doc_deu_CO_THAT`)*.

    ⛔ Chiều ĐỎ *(đã chạy trên `a69ee92`)*: `_drawer_tim_tien` đọc `u.tien` ·
    `u.lech_tuyet_doi` · `u.memo` ⇒ ba khoá ⛔ có trong cửa ⇒ ĐỎ. Phá thử: thêm
    `u.so_tien` vào hàm ⇒ ĐỎ; đổi `x.da_noi` thành `x.noi` ở `_panel_pm` ⇒ ĐỎ."""
    ca, tra = ca_cua_that
    nguon = open(TEP_F01L, encoding="utf-8").read()
    thieu, dem = [], 0
    for ham, bien in BAN_DO:
        than_ham = _than_ham(nguon, ham)
        for b, (duong, vao) in bien.items():
            than_cua = tra[duong.format(ma=ca["ma"])]
            doc = khoa_man_doc(than_ham, b)
            # ⛔ `Đ3`: một biến khai trong bản đồ mà hàm ⛔ đọc khoá nào ⇒ bản đồ
            #   đã trôi khỏi mã ⇒ ĐỎ, ⛔ coi là "không thiếu".
            assert doc, f"⛔ không đo được: `{ham}` ⛔ đọc khoá nào qua `{b}.`"
            co = khoa_cua_tra(than_cua, vao)
            dem += len(doc)
            print(f"WO-022 v3 · {ham} · {b}{list(vao)} đọc {sorted(doc)}")
            thieu += [f"{ham}: {b}.{k} ({duong})" for k in sorted(doc - co)]
    assert dem >= 15, f"⛔ không đo được: chỉ gom được {dem} khoá"
    assert not thieu, ("⛔ màn F01L đọc khoá cửa THẬT ⛔ trả — ô sẽ in `—` / "
                       "phép so ra `null`:\n  " + "\n  ".join(thieu))


def test_AC16_moi_ham_goi_cua_theo_MOT_lenh_DA_CO_ban_do():
    """Mọi hàm của `man_f01_lenh.js` gọi `FLS.doc('/queue/lenh/' …` *(cửa theo
    MỘT lệnh — chỗ thân cửa được đọc sâu ngoài khung `TT.chay`)* phải có hàng
    trong `BAN_DO` *(`_panel_pm` ⛔ tự gọi cửa — nó nhận thân từ
    `_drawer_tim_tien` — nên có hàng riêng mà ⛔ bị bài này đòi)*. ⛔ Chiều ĐỎ: thêm một hàm mới `FLS.doc('/queue/lenh/' + …)`
    mà ⛔ thêm hàng ⇒ ĐỎ."""
    nguon = open(TEP_F01L, encoding="utf-8").read()
    ham = sorted(set(re.findall(r"function\s+(\w+)\s*\(", nguon)))
    # ⚠ Tên trùng *(hàm lồng cùng tên ở hai chỗ)* ⇒ `_than_ham` ĐỎ ⇒ cổng
    #   ⛔ đo được — đúng luật `Đ5`, ⛔ bỏ qua im lặng.
    co_cua = [h for h in ham
              if "FLS.doc('/queue/lenh/'" in _than_ham(nguon, h)]
    assert co_cua, "⛔ không đo được: 0 hàm gọi cửa theo một lệnh"
    ten = {h for h, _b in BAN_DO}
    assert set(co_cua) <= ten, sorted(set(co_cua) - ten)


def test_AC16_KHUON_THU_tu_nhet_cho_itl_candidates_CUNG_phai_la_khuon_cua_that(
        ca_cua_that):
    """⛔⛔ Lỗi trốn ở **khuôn thử**, ⛔ ở màn: bài nào trong `tests/web/**` tự
    nhét thân `itl-candidates` thì khoá mỗi ứng viên phải ⊆ khoá cửa thật.

    Đo hai khuôn Python đang nuôi `F01L` *(`test_man_f01_lenh_dom._UV` ·
    `test_wo022_v2…UV_V2`)*. ⛔ Chiều ĐỎ *(đã chạy trên `a69ee92`)*: `_UV` mang
    `tien` · `lech_tuyet_doi` · `memo` · `le` · `work_status` ⇒ ĐỎ."""
    from tests.web.test_man_f01_lenh_dom import _UV
    from tests.web.test_wo022_v2_o_tien_va_mot_luat_so_le import UV_V2

    ca, tra = ca_cua_that
    co = khoa_cua_tra(tra[f"/queue/lenh/{ca['ma']}/itl-candidates"], ("ung_vien",))
    sai = {}
    for ten, k in (("test_man_f01_lenh_dom._UV", _UV), ("UV_V2", UV_V2)):
        assert k["ung_vien"], f"⛔ không đo được: `{ten}` ⛔ có ứng viên"
        thua = sorted(set().union(*(set(u) for u in k["ung_vien"])) - co)
        if thua:
            sai[ten] = thua
    assert not sai, f"⛔ khuôn thử tự nhét khoá cửa thật ⛔ trả: {sai}"
