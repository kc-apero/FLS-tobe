# -*- coding: utf-8 -*-
"""`WO-045` · `BA-06` v4.19 `§4.5 ⓦ` ① *(lượt **mới nhất** thắng ở mọi màn)* ·
② *(chế độ chỉ đọc khoá **chỉ** thao tác GHI)* · `ⓥ` ⑤ *(nút `Thử lại` `②b`)*.

⛔⛔ Lỗi gốc *(`BG-044` `(d)` — Dev đọc mã 05/10; `fls-ba` đọc lại)*: **16 / 21**
hàm `await` cửa rồi ghi trạng thái chung **⛔ hỏi** *"mình còn là lượt mới
nhất ⛔"*. Nặng nhất *(①)*: `F01G` `mo_lenh` đặt `ST.mo = ma` **trước** `await`
rồi gán `ST.ung_vien` **sau** ⇒ ứng viên của lệnh **trước** hiện dưới lệnh
**đang mở**; `gan` gửi `itl_id` lấy từ chính danh sách ấy kèm `ma_lenh` đang
mở — chỗ **duy nhất** trong 21 đứng sát một cú **GHI** của vòng ghép thật.

⭐ Luật của tệp:
  · thân cửa lấy từ **cửa HTTP thật** trên **kho TEST** *(ca
    `tests/web/ca_wo045.py`, `assert current_database() = 'fls_test'`)*, đưa
    **nguyên văn** vào `_TRA` *(`tests/web/khung_giu.py`)*;
  · độ trễ **có kiểm soát**: cửa giả **giữ** lượt gọi tới khi kịch bản thả —
    thứ tự về do **bài** quyết *(⛔ "bấm nhanh rồi mong")*;
  · bấm đi đúng đường người bấm *(nút / liên kết thật của màn, `disabled` ⛔
    nhận cú bấm — `_bam`)*.

⭐ Mỗi bài ghi **chiều ĐỎ** đã chạy trên mã `HEAD` khi nhận phiếu *(`14a4b72`,
mã `fls/**` = `db0adae`)* — xem `BG` của phiếu.
"""
from __future__ import annotations

import json

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.api.test_cua_chup_pg import _chup, _nguon_day_du, _o
from tests.web.ca_wo032 import goi_ok
from tests.web.ca_wo045 import SO_KHONG, dung_ca_wo045
from tests.web.khung_giu import CUA_GIU, ma_uri, nap
from tests.web.khung_node import TEP_F04, VO_F04, _chay, can_node
from tests.web.test_vong_f02_pg import _may
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = [pytest.mark.pg, can_node]

#: ⭐ Câu `405` của **hai** màn *(`man_f01.js:41` · `man_f01_lenh.js:64`)* —
#: chép **nguyên văn** từ mã khi nhận *(`ⓦ` ②: "⛔ đổi câu `405`")*.
CAU_405 = ("⛔ Cửa đang chạy ở chế độ CHỈ ĐỌC. Mọi thao tác ghi bị trả 405. "
           "Khởi động lại máy chủ với --cho-ghi (nó sửa SỔ THẬT).")

CHI_DOC = {"actor": "lan@apero.vn", "cho_ghi": False}
CO_GHI = {"actor": "lan@apero.vn", "cho_ghi": True}


# ══ Ca + thân cửa thật ═════════════════════════════════════════════════════

def _duong(ca: dict, c1: int, c2: int) -> dict:
    """Mọi đường **màn** gọi trong tệp này *(đúng chuỗi màn dựng)*."""
    L, doc = ca["lenh"], ca["doc"]
    A, B = L["A"], L["B"]
    return {
        # F01G — chip `Chưa gán` *(`CHIP_CUA` · `_duong`)* + ứng viên + toàn sổ
        "g_nguoi": "/queue/lenh-cho?ro=nguoi&limit=500",
        "g_may": "/queue/lenh-cho?ro=may&tu_chung=0&limit=500",
        "uv_A": f"/queue/lenh/{A}/itl-candidates",
        "uv_B": f"/queue/lenh/{B}/itl-candidates",
        "so_B_qA": f"/queue/lenh/{B}/so?q={doc['A']}",
        "so_B_qB": f"/queue/lenh/{B}/so?q={doc['B']}",
        # F01L — băng + rổ + lưới `limit=50` + hộp Tìm tiền
        "l_ro": "/queue/lenh-cho/ro",
        "l_tom": "/queue/lenh-cho/summary",
        "l_may": "/queue/lenh-cho?limit=50&ro=may&tu_chung=0",
        "l_nguoi": "/queue/lenh-cho?limit=50&ro=nguoi",
        "l_khong": "/queue/lenh-cho?limit=50&ro=khong",
        "du_B": f"/queue/lenh/{B}",
        # F01 — lằn dòng tiền
        "t_tom": "/queue/summary",
        "t_lo": "/queue/tu-chung",
        "t_vnd": "/queue?curr=VND&limit=50",
        "t_usd": "/queue?curr=USD&limit=50",
        "t_vnd50": "/queue?curr=VND&den_pct=50&limit=50",
        # F04 — hai ảnh chụp
        "f_nguon": "/sources",
        "f_doc": "/chup?lan=Bank&limit=10",
        "c1": f"/chup/{c1}?limit=50", "c1_tt": f"/chup/{c1}/thu-tu",
        "c2": f"/chup/{c2}?limit=50", "c2_tt": f"/chup/{c2}/thu-tu",
    }


@pytest.fixture(scope="module")
def ca_tra():
    """`(ca, D, TRA)` — `D` tên ⇒ đường màn gọi; `TRA` đường ⇒ phong bì cửa
    thật. Hai ảnh chụp **mới nhất** của kho TEST *(`c1` 1 nguồn · 2 dòng;
    `c2` 2 nguồn · 5 dòng — bốn ô đầu khác nhau)*."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca_wo045(c)
    s1, _ = _nguon_day_du()
    s2, _ = _nguon_day_du()
    s3, _ = _nguon_day_du()
    c1 = _chup({s1: 1}, [(s1, i, _o()) for i in range(2)])
    c2 = _chup({s2: 1, s3: 1},
               [(s2, i, _o()) for i in range(3)] + [(s3, i, _o()) for i in range(2)])
    ca["chup"] = (c1, c2)
    D = _duong(ca, c1, c2)
    with _may() as m:
        TRA = {d: goi_ok(m, _pham_vi_ca(d, ca)) for d in D.values()}
        # trang KẾ của rổ `khong` *(F01L)* và của lằn tiền VND *(F01)* — con
        # trỏ do **cửa** cấp
        nx = TRA[D["l_khong"]]["data"]["next_cursor"]
        assert nx, ("⛔ không đo được: rổ khong ⛔ có trang kế",
                    len(TRA[D["l_khong"]]["data"]["rows"]))
        D["l_khong_2"] = D["l_khong"] + "&cursor=" + ma_uri(nx)
        TRA[D["l_khong_2"]] = goi_ok(m, D["l_khong_2"])
        nv = TRA[D["t_vnd"]]["data"]["next_cursor"]
        assert nv, "⛔ không đo được: lằn tiền VND ⛔ có trang kế"
        D["t_vnd_2"] = "/queue?curr=VND&cursor=" + ma_uri(nv) + "&limit=50"
        TRA[D["t_vnd_2"]] = goi_ok(m, _pham_vi_ca(D["t_vnd_2"], ca))
    return ca, D, TRA


def _pham_vi_ca(duong: str, ca: dict) -> str:
    """⭐ `WO-023` `(j)` *(`KQ-050 F-4`)*: lằn **dòng tiền** `F01` *(`/queue…`
    ⛔ `/queue/lenh…`)* đọc phạm vi `chi_nap_that` = **mọi** lần nạp
    `NAP-yyyy-mm-dd-…` của kho TEST ⇒ phân bố tiền `VND` mà `AC-7` tự chứng
    *(`50%` cắt ít hàng hơn trang đầu)* là của **cả kho**, ⛔ của ca — một ca
    khác dựng thêm dòng `VND` chạy trước là bài **ĐỎ** oan *(`KQ-050` đo: thêm
    **một** lần `dung_ca_wo045` ⇒ `1 failed`; `BG-055` đo lại: `pytest` toàn bộ
    sau bài `wo023` ⇒ `⛔ không đo được: 50% ⛔ khác tất cả`)*. ⇒ Hỏi **cửa thật**
    với `?run_id=<lần nạp của ca>` *(`xu_ly.pham_vi_cua_yeu_cau` — `mot_lan_nap`,
    giao với bản trắng)* rồi đặt thân dưới **đúng** đường màn gọi *(màn ⛔ gửi
    `run_id`)*. Thân vẫn là cửa HTTP thật; chỉ phạm vi là của ca. Phân bố của
    ca *(55 dòng `Q` 1–9 triệu + `B` + `T`)* ⇒ `50%` cắt ≤ **~29** hàng ⛔ bất kể
    kho còn gì. ⛔ Áp cho cửa `F01L`/`F01G`/`F04` *(⛔ phải lằn tiền)*."""
    if not (duong == "/queue" or duong.startswith("/queue?")
            or duong == "/queue/summary" or duong == "/queue/tu-chung"):
        return duong
    return duong + ("&" if "?" in duong else "?") + "run_id=" + ca["run"]


def _ids_uv(env: dict) -> list:
    return [u["itl_id"] for u in (env["data"] or {}).get("ung_vien") or []]


def _js(tra: dict, kich_ban: str, **kw) -> dict:
    return _chay(CUA_GIU + nap(tra) + kich_ban, tep=kw.pop("tep", TEP_F01),
                 vo=kw.pop("vo", VO_F01), **kw)


# ══ ① F01G · `mo_lenh` · `tai_toan_so` ═════════════════════════════════════

_NHIN_G = """
  const uv = F01G.ST.ung_vien.map(u => u.itl_id);
  const hang = document.querySelectorAll('.cands .cand');
  return {mo: F01G.ST.mo, uv, tim: F01G.ST.tim, toan_so: F01G.ST.toan_so,
          dom: hang.length, dom_ct: hang.map(h => h.textContent),
          chu: document.querySelector('#ghep-goc').textContent,
          goi: _doc('/itl-candidates').concat(_doc('/so?')), ghi: _ghi()};
"""


def _tap_roi(D: dict, TRA: dict) -> tuple[set, set]:
    a, b = set(_ids_uv(TRA[D["uv_A"]])), set(_ids_uv(TRA[D["uv_B"]]))
    assert b, "⛔ không đo được: cửa trả 0 ứng viên cho B"
    assert a - b, ("⛔ không đo được: ứng viên A ⊆ B — ca vô nghĩa", a, b)
    return a - b, b


def test_AC1_doi_lenh_A_sang_B_luot_A_ve_SAU_ung_vien_la_cua_B(ca_tra):
    """`mo_lenh(A)` rồi `mo_lenh(B)` khi `A` chưa về; `B` về trước, `A` về sau.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: lượt `A` ghi `ST.ung_vien` **sau** ⇒ danh sách
    của `A` *(USD)* nằm dưới thẻ `B` *(VND)*."""
    ca, D, TRA = ca_tra
    chi_A, tap_B = _tap_roi(D, TRA)
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates');
      const pa = F01G.mo_lenh({A!r}); await _cho();
      const pb = F01G.mo_lenh({B!r}); await _cho();
      await _tha('/lenh/{B}/itl-candidates');
      await _tha('/lenh/{A}/itl-candidates');
      await pa; await pb;
    """ + _NHIN_G)
    assert r["mo"] == B, r["mo"]
    lot = sorted(set(r["uv"]) & chi_A)
    assert not lot, f"⛔ ứng viên của lệnh A dưới lệnh B: {lot}"
    assert r["uv"] == _ids_uv(TRA[D["uv_B"]]), r["uv"]
    assert r["dom"] == len(tap_B), (r["dom"], len(tap_B))


def test_AC1_luot_A_ve_TRUOC_khi_B_dang_tai_KHONG_ve_danh_sach_A(ca_tra):
    """Thứ tự ngược: `A` về **trước** khi `B` xong ⇒ trong lúc `B` đang tải màn
    ⛔ in ứng viên `A` dưới thẻ `B`; sau khi `B` về ⇒ chỉ ứng viên `B`."""
    ca, D, TRA = ca_tra
    chi_A, tap_B = _tap_roi(D, TRA)
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates');
      const pa = F01G.mo_lenh({A!r}); await _cho();
      const pb = F01G.mo_lenh({B!r}); await _cho();
      await _tha('/lenh/{A}/itl-candidates'); await pa;
      F01G.ve();
      const giua = {{uv: F01G.ST.ung_vien.map(u => u.itl_id),
                     dom: document.querySelectorAll('.cands .cand').length}};
      await _tha('/lenh/{B}/itl-candidates'); await pb;
      const r = (() => {{ {_NHIN_G} }})();
      r.giua = giua; return r;
    """)
    assert not set(r["giua"]["uv"]) & chi_A, ("⛔ đang tải B mà ST.ung_vien "
                                              "mang ứng viên A", r["giua"])
    assert r["giua"]["dom"] == 0, r["giua"]
    assert r["mo"] == B and r["uv"] == _ids_uv(TRA[D["uv_B"]]), r


def test_AC1_dang_tai_lenh_moi_ST_ung_vien_KHONG_con_cua_lenh_truoc(ca_tra):
    """⭐ Ca **⛔ cần** lượt nào về muộn: `A` đã mở xong, bấm `j` sang `B`, `B`
    đang bay. `ST.mo` đã là `B` — `ST.ung_vien` ⛔ được còn danh sách `A`
    *(một cú bấm hàng ứng viên + `Gán` lúc này sẽ gửi `itl_id` của `A` kèm
    `B`)*. Màn: khung *"Đang hỏi sổ…"* *(trạng thái **tải** `WO-045` bảng Màn
    hình — "giữ khung chờ tới khi lượt của lệnh đang mở xong")*.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `mo_lenh` ⛔ xoá ⇒ `ST.ung_vien` = ứng viên A."""
    ca, D, TRA = ca_tra
    chi_A, _ = _tap_roi(D, TRA)
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      await F01G.mo_lenh({A!r}); await _cho();
      _GIU.push('/itl-candidates');
      const i = F01G.ST.dong.findIndex(d => d.ma_lenh === {B!r});
      F01G.ST.tro = i - 1;
      document.querySelector('#man-ghep').classList.add('on');   // tab ② đang mở
      _ban('keydown', {{key: 'j'}}); await _cho();
      F01G.ve();
      const giua = {{mo: F01G.ST.mo, uv: F01G.ST.ung_vien.map(u => u.itl_id),
                     dom: document.querySelectorAll('.cands .cand').length,
                     chu: document.querySelector('#ghep-goc').textContent}};
      await _tha('/lenh/{B}/itl-candidates'); await _cho();
      return {{giua, cuoi: F01G.ST.ung_vien.map(u => u.itl_id)}};
    """)
    g = r["giua"]
    assert g["mo"] == B, f"⛔ không đo được: phím j ⛔ sang B: {g['mo']}"
    assert not set(g["uv"]) & chi_A, f"⛔ ST.ung_vien còn ứng viên A: {g['uv'][:5]}"
    assert g["dom"] == 0 and "Đang hỏi sổ…" in g["chu"], g
    assert r["cuoi"] == _ids_uv(TRA[D["uv_B"]]), r["cuoi"]


def test_AC1_loi_luot_A_CU_KHONG_hien_loi_luot_B_MOI_thi_hien(ca_tra):
    """Trạng thái **lỗi** *(`WO-045` bảng Màn hình — "lỗi của lượt mới nhất,
    lỗi lượt cũ ⛔ hiện")*: ⓐ `A` lỗi **sau** khi `B` đã về ⇒ ⛔ câu lỗi, danh
    sách `B` giữ nguyên; ⓑ lượt `B` *(mới nhất)* lỗi ⇒ vùng ứng viên in
    `⛔ Cửa lỗi: <câu>` *(⛔ "Sổ không có dòng tiền nào")*, lỗi vẫn ném cho
    người gọi như nay."""
    ca, D, TRA = ca_tra
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates');
      const L = (e) => new FLS.LoiCua('FLS-INTERNAL', 500, e);
      let pa = F01G.mo_lenh({A!r}).catch(e => 'ném: ' + e.message); await _cho();
      let pb = F01G.mo_lenh({B!r}).catch(e => 'ném: ' + e.message); await _cho();
      await _tha('/lenh/{B}/itl-candidates');
      await _no('/lenh/{A}/itl-candidates', L('cũ'));
      const a = {{ra: [await pa, await pb], uv: F01G.ST.ung_vien.length,
                  chu: document.querySelector('#ghep-goc').textContent}};
      pa = F01G.mo_lenh({A!r}).catch(e => 'ném: ' + e.message); await _cho();
      await _no('/lenh/{A}/itl-candidates', L('mới'));
      const b = {{ra: await pa, uv: F01G.ST.ung_vien.length, mo: F01G.ST.mo,
                  chu: document.querySelector('#ghep-goc').textContent}};
      return {{a, b}};
    """)
    a, b = r["a"], r["b"]
    assert a["ra"] == [None, None], a["ra"]
    assert "Cửa lỗi" not in a["chu"] and a["uv"] == len(_ids_uv(TRA[D["uv_B"]])), a
    assert b["mo"] == A and b["uv"] == 0, b
    assert "⛔ Cửa lỗi: Máy gặp lỗi bên trong." in b["chu"], b["chu"][-300:]
    assert "Sổ không có dòng tiền nào" not in b["chu"], b["chu"][-300:]
    assert b["ra"] == "ném: Máy gặp lỗi bên trong.", b["ra"]


_GAN = """
  const hang = document.querySelectorAll('.cands .cand');
  if (!hang.length) return {loi: 'không có hàng ứng viên trên màn', ghi: _ghi()};
  _bam(hang[0]); await _cho();
  for (let k = 0; k < 2 && !_ghi().length; k++) {
    const g = document.querySelectorAll('.act button')[0];
    _bam(g); await _cho();
  }
  return {ghi: _ghi(), mo: F01G.ST.mo};
"""


def test_AC2_GAN_sau_khi_doi_lenh_chi_gui_itl_id_cua_B(ca_tra):
    """⭐ Cú GHI. Cùng kịch bản `AC-1` *(`A` về sau)*, rồi bấm hàng ứng viên đầu
    + nút `Gán` *(hai lần nếu lệch tiền — bước xác nhận)* ⇒ đúng **một**
    `FLS.ghi('/queue/{X}/match', {pm_line_ids: [B]})` với `X` ∈ ứng viên `B`.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `X` = ứng viên **của `A`** *(USD)* kèm mã `B`."""
    ca, D, TRA = ca_tra
    chi_A, tap_B = _tap_roi(D, TRA)
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      _GIU.push('/itl-candidates');
      const pa = F01G.mo_lenh({A!r}); await _cho();
      const pb = F01G.mo_lenh({B!r}); await _cho();
      await _tha('/lenh/{B}/itl-candidates');
      await _tha('/lenh/{A}/itl-candidates');
      await pa; await pb;
    """ + _GAN)
    assert len(r["ghi"]) == 1, r
    duong, than = r["ghi"][0]
    x = int(duong.split("/")[2])
    assert duong == f"/queue/{x}/match", duong
    assert x not in chi_A, f"⛔ GÁN itl_id {x} của lệnh A kèm lệnh B"
    assert x in tap_B, (x, sorted(tap_B)[:5])
    assert than == {"pm_line_ids": [B]}, than


def test_AC2_GAN_luc_lenh_moi_DANG_TAI_KHONG_gui_itl_id_lenh_truoc(ca_tra):
    """Ca ⛔ cần lượt muộn *(bài thứ ba của `AC-1`)*: `A` mở xong, `j` sang `B`
    đang bay; người bấm hàng ứng viên đầu **đang hiện** rồi `Gán` ⇒ **0** cú
    ghi mang `itl_id` của `A`.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: màn vẫn vẽ ứng viên `A`; hàng đầu được chọn,
    nút `Gán` *(vẽ lại với `ST.mo = B`)* gửi `itl_id` của `A` kèm mã `B`."""
    ca, D, TRA = ca_tra
    chi_A, _ = _tap_roi(D, TRA)
    A, B = ca["lenh"]["A"], ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      await F01G.mo_lenh({A!r}); await _cho();
      _GIU.push('/itl-candidates');
      const i = F01G.ST.dong.findIndex(d => d.ma_lenh === {B!r});
      F01G.ST.tro = i - 1;
      document.querySelector('#man-ghep').classList.add('on');   // tab ② đang mở
      _ban('keydown', {{key: 'j'}}); await _cho();
      const mo = F01G.ST.mo;     // ⚠ đọc TRƯỚC Gán — gán xong màn tự sang lệnh kế
      const hang = document.querySelectorAll('.cands .cand');
      if (hang.length) {{ _bam(hang[0]); await _cho(); }}
      for (let k = 0; k < 2; k++) {{
        const g = document.querySelectorAll('.act button')[0];
        _bam(g); await _cho();
      }}
      return {{ghi: _ghi(), mo}};
    """)
    assert r["mo"] == B, r
    sai = [g for g in r["ghi"] if int(g[0].split("/")[2]) in chi_A]
    assert not sai, f"⛔ cú GÁN mang itl_id của lệnh A kèm lệnh B: {sai}"


def test_AC3_o_tim_hai_chu_luot_chu_CU_ve_SAU_ung_vien_la_cua_chu_MOI(ca_tra):
    """Gõ `q1` *(số CT dòng tiền của `A`)*, chờ quá `TRE_TIM`, gõ `q2` *(của
    `B`)*, chờ quá `TRE_TIM` ⇒ hai lượt `/so?q=` cùng bay *(đúng ca chú thích
    `man_f01_ghep.js:129-132` tự nêu)*; `q2` về trước, `q1` về sau.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `ST.ung_vien` = kết quả **`q1`**."""
    ca, D, TRA = ca_tra
    q1, q2 = ca["doc"]["A"], ca["doc"]["B"]
    k1, k2 = set(_ids_uv(TRA[D["so_B_qA"]])), set(_ids_uv(TRA[D["so_B_qB"]]))
    assert k1 and k2 and not k1 & k2, ("⛔ không đo được: hai kết quả tìm "
                                        "rỗng hoặc chồng", k1, k2)
    B = ca["lenh"]["B"]
    r = _js(TRA, f"""
      await F01G.mo_man(); await _cho();
      await F01G.mo_lenh({B!r}); await _cho();
      _GIU.push('/so?');
      const go = async (q) => {{
        _ban('input', {{target: {{id: 'ghep-tim', value: q}}}});
        await new Promise(r => setTimeout(r, F01G.TRE_TIM + 80)); await _cho();
      }};
      await go({q1!r}); await go({q2!r});
      const bay = _doc('/so?');
      await _tha('q={q2}'); await _tha('q={q1}');
      const r = (() => {{ {_NHIN_G} }})(); r.bay = bay; return r;
    """)
    assert len(r["bay"]) == 2, f"⛔ không đo được: hai lượt ⛔ cùng bay {r['bay']}"
    assert r["tim"] == q2 and r["toan_so"] is True, r
    assert r["uv"] == _ids_uv(TRA[D["so_B_qB"]]), (r["uv"], sorted(k1))
    assert r["dom"] == len(k2), r["dom"]


# ══ ② F01L · lưới rổ · `Xem thêm` · chế độ chỉ đọc ═════════════════════════

_VE_L = """
  const vo = document.querySelector('#than-f01');
  F01L.ve(vo); await _cho();
  const lam = () => vo.querySelectorAll('td.lam').length;
  const nhin = () => ({ro: F01L.ST.ro, ma: F01L.ST.dong.map(r => r.pm_line_id),
                       ro_hang: F01L.ST.dong.map(r => r.ro), dom: lam(),
                       goi: _doc('/queue/lenh-cho?limit=50')});
"""


def _ma(env: dict) -> list:
    return [x["pm_line_id"] for x in env["data"]["rows"]]


@pytest.mark.parametrize("cu_ve", ["sau", "truoc"])
def test_AC4_doi_ro_khi_luoi_dang_tai_luoi_CHI_hang_ro_dang_chon(ca_tra, cu_ve):
    """Lưới đang tải rổ `may` *(liên kết `Xem <c> dòng`)*, bấm `Bắt đầu tra`
    *(rổ `nguoi`)*. `cu_ve` = lượt `may` về **sau** / **trước** lượt `nguoi`.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `_ve_luoi` **nối** `ST.dong` ⇒ lưới trộn hai rổ
    *(về trước ⇒ trộn trên **màn**; về sau ⇒ trộn trong `ST.dong`)*."""
    ca, D, TRA = ca_tra
    mong = _ma(TRA[D["l_nguoi"]])
    assert mong and _ma(TRA[D["l_may"]]), "⛔ không đo được: rổ rỗng"
    thu_tu = (["ro=nguoi", "ro=may"] if cu_ve == "sau"
              else ["ro=may", "ro=nguoi"])
    r = _js(TRA, _VE_L + f"""
      _GIU.push('/queue/lenh-cho?limit=50');
      _bam(document.querySelector('#f01l-lech')) || document.querySelector('#f01l-lech')
        .onclick({{preventDefault() {{}}}});
      await _cho();
      _bam(_nut(vo, 'Bắt đầu tra')[0]); await _cho();
      await _tha({thu_tu[0]!r}); await _tha({thu_tu[1]!r});
      return nhin();""")
    assert r["ro"] == "nguoi", r["ro"]
    assert set(r["ro_hang"]) == {"nguoi"}, f"⛔ lưới trộn rổ: {r['ro_hang']}"
    assert r["ma"] == mong and r["dom"] == len(mong), r


def test_AC4_QUAY_LAI_khi_luoi_dang_tai_luot_cu_KHONG_do_hang(ca_tra):
    """`Xem <c> dòng` *(rổ `may`, đang tải)* rồi `← Quay lại toàn bộ` ⇒ lượt
    `may` về sau ⛔ đổ hàng vào `ST.dong` *(⛔ còn rổ nào đang chọn)*."""
    ca, D, TRA = ca_tra
    r = _js(TRA, _VE_L + """
      _GIU.push('/queue/lenh-cho?limit=50');
      document.querySelector('#f01l-lech').onclick({preventDefault() {}});
      await _cho();
      _bam(_nut(vo, '← Quay lại toàn bộ')[0]); await _cho();
      await _tha('ro=may');
      return nhin();""")
    assert r["ro"] is None and r["ma"] == [] and r["dom"] == 0, r


def test_AC5_XEM_THEM_bam_hai_lan_khi_luot_dau_con_bay_MOT_GET_khong_hang_lap(ca_tra):
    """Rổ `khong` *(**55** lệnh ⇒ hai trang `limit=50`)*: bấm `Xem thêm` hai lần
    khi lượt đầu còn bay ⇒ **một** `GET` trang kế; `pm_line_id` ⛔ trùng.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: hai `GET` cùng con trỏ ⇒ **60** hàng, 5 lặp."""
    ca, D, TRA = ca_tra
    assert len(_ma(TRA[D["l_khong"]])) == 50, "⛔ không đo được: trang 1 ≠ 50"
    r = _js(TRA, _VE_L + """
      _bam(_nut(vo, 'Xem vì sao')[0]); await _cho();
      _GIU.push('cursor=');
      const b1 = _nut(vo, 'Xem thêm')[0];
      const bam1 = _bam(b1); await _cho();
      const bam2 = _bam(_nut(vo, 'Xem thêm')[0] || b1); await _cho();
      const cursor = _doc('cursor=');
      while (_tim('cursor=')) await _tha('cursor=');
      const r = nhin(); r.cursor = cursor; r.bam1 = bam1;
      r.con_xem_them = _nut(vo, 'Xem thêm').length; return r;""")
    assert r["bam1"], "⛔ không đo được: nút Xem thêm ⛔ bấm được"
    assert len(r["cursor"]) == 1, f"⛔ mở lượt thứ hai: {r['cursor']}"
    assert len(r["ma"]) == len(set(r["ma"])), "⛔ hàng lặp trên lưới"
    tong = _ma(TRA[D["l_khong"]]) + _ma(TRA[D["l_khong_2"]])
    assert r["ma"] == tong and len(tong) >= SO_KHONG, (len(r["ma"]), len(tong))
    assert r["dom"] == len(tong) and r["con_xem_them"] == 0, r


def test_AC6_CHI_DOC_xem_them_CHAY_den_het(ca_tra):
    """`cho_ghi = false`: `Xem thêm` ⛔ `disabled`; bấm ⇒ `GET` trang kế, lưới
    tăng tới **hết** rổ.

    ⛔ Chiều ĐỎ *(mã khi nhận — `_nut` ⇒ `_chan_ghi`)*: nút `disabled` + câu
    `405` ⇒ lưới dừng ở **50**."""
    ca, D, TRA = ca_tra
    r = _js(TRA, _VE_L + """
      _bam(_nut(vo, 'Xem vì sao')[0]); await _cho();
      const b = _nut(vo, 'Xem thêm')[0];
      const tt = {co: !!b, disabled: b ? !!b.disabled : null, title: b ? b.title : null};
      _bam(b); await _cho();
      const r = nhin(); r.nut = tt; return r;""", phien=CHI_DOC)
    assert r["nut"] == {"co": True, "disabled": False, "title": ""}, r["nut"]
    tong = _ma(TRA[D["l_khong"]]) + _ma(TRA[D["l_khong_2"]])
    assert r["ma"] == tong and r["dom"] == len(tong), len(r["ma"])


_HOP = """
  _bam(document.querySelector('#f01l-lech')) || document.querySelector('#f01l-lech')
    .onclick({preventDefault() {}});
  await _cho();
  // ⚠ hàng in **số chứng từ** (`ref_tho`), ⛔ in `pm_line_id`
  const hang = vo.querySelectorAll('tr').find(t => t.textContent.includes(%(doc)s));
  const nut = hang ? hang.querySelectorAll('td.lam')[0].querySelectorAll('button')[0] : null;
  const tt = {co: !!nut, chu: nut ? nut.textContent : null,
              disabled: nut ? !!nut.disabled : null, title: nut ? nut.title : null};
  _bam(nut); await _cho();
  const f = [...document.querySelectorAll('#dlg-f button')];
  return {nut: tt, tieu_de: document.querySelector('#dlg-t').textContent,
          than: document.querySelector('#dlg-b').innerHTML,
          hop: f.map(b => ({chu: b.textContent, disabled: !!b.disabled, title: b.title})),
          goi: _doc('/queue/lenh/')};
"""


def test_AC6_CHI_DOC_TIM_TIEN_mo_hop_xem_ung_vien_GHEP_khoa_cau_405(ca_tra):
    """`cho_ghi = false`: nút việc của hàng `B` *(rổ `may` ⛔ tự chứng ⇒ chữ
    `Mở để chia` — `G5` ②)* ⛔ `disabled`; bấm ⇒ hộp `Tìm tiền cho lệnh B` mở,
    ứng viên hiện *(`itl_id` cửa trả)*; nút **`Ghép`** trong hộp `disabled` +
    `title` câu `405`; `Thôi` bấm được.

    ⛔ Chiều ĐỎ: ⓐ mã khi nhận ⇒ nút hàng `disabled` ⇒ hộp ⛔ mở; ⓑ mở khoá
    `Ghép` ở chỉ đọc ⇒ `disabled false`."""
    ca, D, TRA = ca_tra
    B = ca["lenh"]["B"]
    uv = _ids_uv(TRA[D["uv_B"]])
    r = _js(TRA, _VE_L + _HOP % {"doc": json.dumps(ca["doc"]["B"])}, phien=CHI_DOC)
    assert r["nut"]["co"] and r["nut"]["disabled"] is False, r["nut"]
    assert r["tieu_de"] == f"Tìm tiền cho lệnh {B}", r["tieu_de"]
    assert f">{uv[0]}<" in r["than"], "⛔ hộp ⛔ hiện ứng viên cửa trả"
    hop = {b["chu"]: b for b in r["hop"]}
    assert hop["Ghép"] == {"chu": "Ghép", "disabled": True, "title": CAU_405}, hop
    assert hop["Thôi"]["disabled"] is False, hop


def test_AC6_CO_GHI_tim_tien_va_GHEP_nhu_nay(ca_tra):
    """`cho_ghi = true` ⇒ như nay: nút hàng + `Ghép` trong hộp bấm được."""
    ca, D, TRA = ca_tra
    B = ca["lenh"]["B"]
    r = _js(TRA, _VE_L + _HOP % {"doc": json.dumps(ca["doc"]["B"])}, phien=CO_GHI)
    assert r["nut"]["disabled"] is False, r["nut"]
    hop = {b["chu"]: b for b in r["hop"]}
    assert hop["Ghép"]["disabled"] is False and hop["Ghép"]["title"] == "", hop


_F01 = """
  const o = document.querySelector('#than-f01');
  F01.ST.curr = 'VND'; F01.ST.den_pct = '';
  F01.ve(o); await _cho();
  const lo = document.querySelector('#lo-nut-ghep');
  const hang = o.querySelectorAll('tbody tr');
  const nut = hang.length ? hang[0].querySelectorAll('button') : [];
  return {lo: lo ? {chu: lo.textContent, disabled: !!lo.disabled, title: lo.title} : null,
          n_hang: hang.length,
          nut: nut.map(b => ({chu: b.textContent, disabled: !!b.disabled, title: b.title}))};
"""


@pytest.mark.parametrize("phien", ["chi_doc", "co_ghi"])
def test_AC6_F01_nut_GHI_khoa_dung_che_do(ca_tra, phien):
    """Hồi quy chiều ngược *(`ⓦ` ② bảng: `Ghép N dòng tự chứng` · `Lý do` ·
    `Hoãn` · `Ghép` · `Xong` **khoá** + câu `405` ở chỉ đọc)*; `cho_ghi = true`
    ⇒ bấm được. ⛔ Chiều ĐỎ: mở khoá một nút GHI ở chỉ đọc."""
    ca, D, TRA = ca_tra
    tc = (TRA[D["t_lo"]]["data"] or {}).get("tu_chung") or []
    assert tc, "⛔ không đo được: 0 dòng tự chứng — nút lô khoá vì lý do khác"
    r = _js(TRA, _F01, phien=CHI_DOC if phien == "chi_doc" else CO_GHI)
    assert r["n_hang"] > 0 and r["lo"], r
    khoa = phien == "chi_doc"
    assert r["lo"]["disabled"] is khoa, r["lo"]
    assert {b["chu"] for b in r["nut"]} >= {"Lý do", "Hoãn", "Ghép", "Xong"}, r["nut"]
    for b in r["nut"] + [r["lo"]]:
        assert b["disabled"] is khoa, b
        assert b["title"] == (CAU_405 if khoa else ""), b


# ══ ③ F01 · hàng chờ dòng tiền · `ve_luoi` · `_xem_them` ═══════════════════

def _itl(env: dict) -> list:
    return [x["itl_id"] for x in env["data"]["rows"]]


_NHIN_T = """
  const nhin = () => ({curr: F01.ST.curr, den: F01.ST.den_pct,
                       itl: F01.ST.dong.map(r => r.itl_id), tro: F01.ST.con_tro,
                       dom: o.querySelectorAll('tbody tr').length,
                       goi: _doc('/queue?curr=')});
"""


@pytest.mark.parametrize("cu_ve", ["sau", "truoc"])
def test_AC7_doi_TIEN_TE_khi_luoi_dang_tai_luoi_la_loc_CUOI(ca_tra, cu_ve):
    """Lưới VND đang tải, bấm `Xem` ở thẻ **USD** ⇒ lưới = USD *(`ST.dong`,
    `ST.con_tro`, hàng trên màn)*.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: lượt VND về sau ghi `ST.dong` + `ST.con_tro`
    ⇒ `Xem thêm` kế tiếp lật trang **VND** dưới bộ lọc USD."""
    ca, D, TRA = ca_tra
    usd = _itl(TRA[D["t_usd"]])
    assert usd and _itl(TRA[D["t_vnd"]]), "⛔ không đo được: lằn rỗng"
    thu_tu = ["curr=USD", "curr=VND"] if cu_ve == "sau" else ["curr=VND", "curr=USD"]
    r = _js(TRA, _NHIN_T.replace("o.query", "document.querySelector('#than-f01').query")
            + f"""
      const o = document.querySelector('#than-f01');
      F01.ST.curr = 'VND'; F01.ST.den_pct = '';
      _GIU.push('/queue?curr=');
      F01.ve(o); await _cho();
      const the = o.querySelectorAll('button').find(b => b.parentNode
        && String(b.parentNode.innerHTML).indexOf('>USD<') >= 0);
      if (!the) return {{loi: 'không có thẻ USD'}};
      _bam(the); await _cho();
      await _tha({thu_tu[0]!r}); await _tha({thu_tu[1]!r});
      return nhin();""")
    assert r.get("curr") == "USD", r
    assert r["itl"] == usd, f"⛔ lưới mang hàng VND: {len(r['itl'])}"
    assert r["tro"] == TRA[D["t_usd"]]["data"]["next_cursor"], r["tro"]
    assert r["dom"] == len(usd), r["dom"]


def test_AC7_doi_MUC_PHU_khi_luoi_dang_tai_luoi_la_loc_CUOI(ca_tra):
    """Cùng luật trên trục `den_pct`: `tất cả` đang tải, bấm `50%` ⇒ lưới = cửa
    trả cho `den_pct=50`; lượt `tất cả` về sau ⛔ đè."""
    ca, D, TRA = ca_tra
    mong = _itl(TRA[D["t_vnd50"]])
    assert mong and len(mong) < len(_itl(TRA[D["t_vnd"]])), \
        "⛔ không đo được: 50% ⛔ khác tất cả"
    r = _js(TRA, f"""
      const o = document.querySelector('#than-f01');
      {_NHIN_T}
      F01.ST.curr = 'VND'; F01.ST.den_pct = '';
      _GIU.push('/queue?curr=');
      F01.ve(o); await _cho();
      _bam(_nut(o, '50%')[0]); await _cho();
      await _tha('den_pct=50'); await _tha('curr=VND&limit');
      return nhin();""")
    assert r["den"] == "50" and r["itl"] == mong and r["dom"] == len(mong), r


def test_AC7_XEM_THEM_F01_hai_lan_MOT_GET_khong_hang_trung(ca_tra):
    """`Xem thêm` lằn tiền bấm hai lần khi lượt đầu còn bay ⇒ **một** `GET`
    trang kế, `itl_id` ⛔ trùng. ⛔ Chiều ĐỎ *(mã khi nhận)*: hai `GET`."""
    ca, D, TRA = ca_tra
    r = _js(TRA, f"""
      const o = document.querySelector('#than-f01');
      {_NHIN_T}
      F01.ST.curr = 'VND'; F01.ST.den_pct = '';
      F01.ve(o); await _cho();
      _GIU.push('cursor=');
      const b1 = _nut(o, 'Xem thêm')[0];
      const bam1 = _bam(b1); await _cho();
      _bam(_nut(o, 'Xem thêm')[0] || b1); await _cho();
      const cursor = _doc('cursor=');
      while (_tim('cursor=')) await _tha('cursor=');
      const r = nhin(); r.cursor = cursor; r.bam1 = bam1; return r;""")
    assert r["bam1"], "⛔ không đo được: ⛔ có nút Xem thêm"
    assert len(r["cursor"]) == 1, f"⛔ mở lượt thứ hai: {r['cursor']}"
    assert len(r["itl"]) == len(set(r["itl"])), "⛔ hàng trùng"
    mong = _itl(TRA[D["t_vnd"]]) + _itl(TRA[D["t_vnd_2"]])
    assert r["itl"] == mong and r["dom"] == len(mong), (len(r["itl"]), len(mong))


# ══ ④ F04 · `_mo_chup` · `_ve_thu_tu` ═════════════════════════════════════

_F04 = """
  _GIU.push('/chup/');
  F04.ve(); await _cho();
  const nut = (cid) => document.querySelectorAll('#nap-doc tr')
    .filter(t => t.dataset.chup === String(cid))
    .map(t => t.querySelectorAll('button')[0])[0];
  const b1 = nut(%(c1)s), b2 = nut(%(c2)s);
  if (!b1 || !b2) return {loi: 'không có hai hàng ảnh'};
  _bam(b1); await _cho();
  _bam(b2); await _cho();
  %(tha)s
  const S = F04._S;
  const o = document.querySelector('#nap-xem');
  // ⚠ ô dựng bằng `innerHTML` — DOM giả ⛔ phân tích HTML ⇒ đọc chuỗi `.v`
  const v = o.querySelectorAll('.card').map(x => String(x.innerHTML))
    .map(h => (h.match(/class="v num">([^<]*)</) || [])[1]).filter(x => x !== undefined);
  return {chup: S.chup ? S.chup.chup_id : null,
          thu_tu: S.thu_tu ? (S.thu_tu.nguon || []).map(n => n.source_id) : null,
          o4: v.slice(0, 2),
          nap_thu_tu: document.querySelector('#nap-thu-tu').textContent,
          goi: _doc('/chup/')};
"""


def test_AC8_mo_hai_anh_chup_anh_DAU_ve_SAU_man_la_anh_CUOI(ca_tra):
    """Bấm `Xem trước` ảnh `c1` rồi `c2` *(hàng thật của `#nap-doc`)*; `c2` +
    thứ tự ngày của `c2` về trước, `c1` về sau.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `S.chup` = `c1`, bốn ô của `c1`, `_ve_thu_tu(c1)`
    chạy và đè `S.thu_tu`."""
    ca, D, TRA = ca_tra
    c1, c2 = ca["chup"]
    d2 = TRA[D["c2"]]["data"]
    assert (d2["so_nguon"], d2["so_dong"]) != (TRA[D["c1"]]["data"]["so_nguon"],
                                               TRA[D["c1"]]["data"]["so_dong"])
    tha = f"""
      await _tha('/chup/{c2}?limit'); await _tha('/chup/{c2}/thu-tu');
      await _tha('/chup/{c1}?limit');
      if (_tim('/chup/{c1}/thu-tu')) await _tha('/chup/{c1}/thu-tu');
    """
    r = _js(TRA, _F04 % {"c1": c1, "c2": c2, "tha": tha}, tep=TEP_F04, vo=VO_F04)
    assert r.get("chup") == c2, r
    assert r["o4"] == [str(d2["so_nguon"]), str(d2["so_dong"])], r["o4"]
    tt2 = [n["source_id"] for n in TRA[D["c2_tt"]]["data"]["nguon"]]
    assert r["thu_tu"] == tt2, (r["thu_tu"], tt2)


def test_AC8_thu_tu_ngay_luot_CU_ve_SAU_KHONG_de_S_thu_tu(ca_tra):
    """Cả hai ảnh mở xong theo thứ tự *(c1 rồi c2)*, nhưng lượt **thứ tự ngày**
    của `c1` còn bay khi `c2` đã vẽ ⇒ về sau ⛔ đè `S.thu_tu` / `#nap-thu-tu`.

    ⛔ Chiều ĐỎ *(mã khi nhận)*: `_ve_thu_tu` ⛔ kiểm lượt ⇒ `S.thu_tu` của `c1`."""
    ca, D, TRA = ca_tra
    c1, c2 = ca["chup"]
    tha = f"""
      await _tha('/chup/{c1}?limit');
      await _tha('/chup/{c2}?limit'); await _tha('/chup/{c2}/thu-tu');
      if (_tim('/chup/{c1}/thu-tu')) await _tha('/chup/{c1}/thu-tu');
    """
    r = _js(TRA, _F04 % {"c1": c1, "c2": c2, "tha": tha}, tep=TEP_F04, vo=VO_F04)
    tt1 = [n["source_id"] for n in TRA[D["c1_tt"]]["data"]["nguon"]]
    tt2 = [n["source_id"] for n in TRA[D["c2_tt"]]["data"]["nguon"]]
    assert tt1 != tt2, "⛔ không đo được: hai thân thứ tự ngày như nhau"
    assert r.get("chup") == c2 and r["thu_tu"] == tt2, r


# ══ `(e)` · `②b` · nút `Thử lại` ═════════════════════════════════════════

@pytest.mark.parametrize("ma,cau", [
    ("FLS-INTERNAL", "Máy gặp lỗi bên trong."),
    ("FLS-MAT-KET-NOI", "Không nối được tới máy chủ FLS."),
])
def test_AC9_loi_danh_sach_co_nut_THU_LAI_bam_tai_lai_MOT_luot(ca_tra, ma, cau):
    """`②b` cửa lỗi ⇒ dưới `banner crit` có nút `Thử lại` *(lớp `b tiny`)*; bấm
    **hai** lần ⇒ đúng **một** lượt tải chip đang chọn *(hai cửa của chip
    `Chưa gán`, mỗi cửa một `GET`)*; lượt ấy xanh ⇒ danh sách hiện, câu lỗi mất.

    ⛔ Chiều ĐỎ: ⓐ mã khi nhận ⇒ ⛔ có nút; ⓑ bấm hai lần mở hai lượt."""
    ca, D, TRA = ca_tra
    n = len(TRA[D["g_nguoi"]]["data"]["rows"]) + len(TRA[D["g_may"]]["data"]["rows"])
    assert n > 0, "⛔ không đo được: chip Chưa gán rỗng"
    r = _js(TRA, f"""
      _GIU.push('/queue/lenh-cho?');
      const a = F01G.doi_chip('chua_gan'); await _cho();
      await _no('ro=nguoi', new FLS.LoiCua({ma!r}, 0, 'x')); await a;
      const goc = document.querySelector('#ghep-goc');
      const ban = goc.querySelectorAll('.banner').map(x => [x.className, x.textContent]);
      const nut = _nut(goc, 'Thử lại');
      const tt = nut.map(b => b.className);
      const truoc = _doc('/queue/lenh-cho?').length;
      _bam(nut[0]); await _cho(); _bam(nut[0]); await _cho();
      // ⚠ hai cửa của chip đi **nối tiếp** ⇒ đếm SAU khi thả hết
      while (_tim('/queue/lenh-cho?')) await _tha('/queue/lenh-cho?');
      const luot = _doc('/queue/lenh-cho?').slice(truoc);
      return {{ban, nut: tt, luot, n: F01G.ST.dong.length, loi: F01G.ST.loi,
               chu: goc.textContent}};""")
    assert r["ban"] == [["banner crit", "⛔ Cửa lỗi: " + cau]], r["ban"]
    assert r["nut"] == ["b tiny"], f"⛔ ⛔ có nút Thử lại: {r['nut']}"
    assert sorted(r["luot"]) == sorted([D["g_nguoi"], D["g_may"]]), r["luot"]
    assert r["loi"] is None and "Cửa lỗi" not in r["chu"], r
    assert r["n"] == n, (r["n"], n)
