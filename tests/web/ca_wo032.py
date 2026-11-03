# -*- coding: utf-8 -*-
"""`WO-032` — **một** ca dựng chung trên **kho TEST**, và thân **cửa thật** của
mọi đường hai màn ghép `F01L` / `F01G` đọc.

⛔⛔ **Vì sao có tệp này** *(`BA-07` v3.7 §4h ⓵ — luật bài thử)*: lớp lỗi *"khuôn
thử tự nhét"* đã sống sót **ba lần** *(`KQ-019` `HT.hoi` · `KQ-029 F-1`
`u.tien` · `KQ-031 F-3` `khoa_to`)*. Cả ba lần bài **tự đặt** khoá nó muốn màn
đọc ⇒ bài đặt **cả** câu hỏi **lẫn** câu trả lời ⇒ ⛔ có cách nào đỏ. Ở đây
mọi thân dùng để vẽ màn đi ra từ **cửa HTTP thật** chạy trên kho TEST; bài
⛔ đặt một khoá nào *(trừ thao tác DOM của khung hộp — như `KQ-029`/`KQ-031`)*.

⭐ Bốn lệnh trong **một** lần nạp *(ảnh PM mới nhất ⇒ ảnh hiệu lực của máy thử)*:

  `A` VND `<a>`   ↔ dòng tiền VND `<a>+1.000.000`, ĐÚNG số CT  ⇒ bậc `ma`, lệch `1.000.000`
                    *(nguồn đúng khuôn, ⛔ chụp ⇒ `dien_giai = null` ⇒ `dien_giai_vi_sao`)*
  `B` VND `<b>`   ↔ dòng tiền VND `<b>+500`, ĐÚNG số CT — **ĐÃ GÁN** qua `ghep_lenh` thật
                    *(lệch `500` ≤ dung sai ghép tay)*; nguồn **sai khuôn** ⇒ `loi_nguon`;
                    có chụp ⇒ diễn giải **chứa số CT** ⇒ `khoa_to` ∋ số CT
  `X` VND `<n>`   ↔ dòng tiền **USD** `<n>.00`, ĐÚNG số CT ⇒ bậc `ma`, **khác tiền tệ**
                    *(`AC-1` — đúng hình `PM00329-1` của sổ thật)*
  `Y` VND `<y>`   ↔ dòng tiền **USD** `<y>.00` — mối nối **khác tiền tệ** chèn như bộ
                    nạp `chay_nap.chen_moi_noi` *(cửa ghi tay ⛔ cho; sổ thật hôm nay
                    **0 / 2.262** — đây là ca biên cho `gd_ds`, ⛔ ca thường)*

Tiền **ngẫu nhiên** mỗi lần *(kho TEST phình — bia `fls-test-store-grows-unbounded`)*.
"""
from __future__ import annotations

import json
import random
import uuid
from decimal import Decimal as D

from fls.adapters.pm_join import DongPM, canon_ref
from fls.ledger.build import NgucCanh
from fls.repo import ghi_tay as gt
from fls.repo.chay_nap import chen_dong_pm
from fls.repo.pham_vi import mot_lan_nap
from tests.web.test_vong_f02_pg import V, _goi

ACTOR = "fls-dev@apero.vn"

#: ⭐ Hàng THÔ của lệnh *(khoá theo tên cột `PM_Unpivot`)* — để thẻ `the` có đủ
#: trường **và** khối *"Xem đủ trường"* `nhom_du_truong` ⛔ rỗng *(cổng quét
#: `AC-9` đòi mẫu số > 0 ở mọi đường — `Đ3`)*. ⛔ `Email Address`: cấm vào kho.
THO = {"Tên tài khoản": "CONG TY WOTHIRTYTWO",
       "Pháp nhân thanh toán": "K32", "Ngân hàng": "VPB",
       "Số tài khoản": "123456789",
       "Nội dung giao dịch nhập khi lập lệnh ở bank": "TT WO032",
       "Loại giao dịch (Payment Type)": "Thanh toán (Regular)",
       "Timestamp": 46091.42265217593, "Chi nhánh": "HN",
       "Status_Final": "Approve", "Budget Code (HDCode)": "HD-K32"}


def _tien(conn, run: str, khoa: str, so: int, tien: str, curr: str,
          doc: str) -> int:
    return conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_no, work_status, period_state)"
        " VALUES (%s,'RAW',%s,%s,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,'UNMAPPED','open') RETURNING itl_id",
        (uuid.uuid4().hex, khoa, so, run, doc, curr, D(tien))).fetchone()[0]


def dung_ca(conn) -> dict:
    """Dựng ca trên **kho TEST**. ⛔ Ghi gì vào kho THẬT: assert `current_database()`."""
    db = conn.execute("SELECT current_database()").fetchone()[0]
    assert db == "fls_test", f"⛔ ca này chỉ dựng trên kho TEST, gặp {db!r}"
    h = uuid.uuid4().hex[:8].upper()
    run = "NAP-2000-01-01-T32" + h[:6]
    conn.execute("INSERT INTO fls_run (run_id, contract_version, canon_version,"
                 " mapping_version) VALUES (%s,'v1.0','v1.0','v1.0')", (run,))
    a = random.randint(1_000, 8_999) * 1000
    b = random.randint(1_000, 8_999) * 1000
    n = random.randint(1_000, 8_999) * 100
    y = random.randint(1_000, 8_999) * 100
    doc = {k: "FT" + k + h for k in "ABXY"}
    nguon_vnd = "R | 123456789_VPB VND_K32" + h
    nguon_usd = "R | 987654321_OCBC USD_K32" + h
    nguon_hong = "R | K32HONG " + h          # ⛔ sai khuôn ⇒ `loi_nguon`
    dg_b = "CK thanh toan " + doc["B"] + " WO032 bang chung"

    # ⭐ Diễn giải của `B` đi vào kho qua **đúng đường** cửa đọc
    #   *(`fls_chup_dong.o ->> 'Description'` ⇒ khung xem `fls_dien_giai`)*.
    sid = conn.execute("INSERT INTO fls_source (source_key, src_type)"
                       " VALUES (%s,'Bank') RETURNING source_id",
                       (nguon_hong,)).fetchone()[0]
    cid = conn.execute("INSERT INTO fls_chup (spreadsheet_id, lan, actor)"
                       " VALUES ('SS-WO032','Bank',%s) RETURNING chup_id",
                       (ACTOR,)).fetchone()[0]
    conn.execute("INSERT INTO fls_chup_dong (chup_id, source_id, dong_so, o)"
                 " VALUES (%s,%s,2,%s::jsonb)",
                 (cid, sid, json.dumps({"Description": dg_b})))

    i_a = _tien(conn, run, nguon_vnd, 1, f"{a + 1_000_000}.00", "VND", doc["A"])
    i_b = _tien(conn, run, nguon_hong, 2, f"{b + 500}.00", "VND", doc["B"])
    i_x = _tien(conn, run, nguon_usd, 3, f"{n}.00", "USD", doc["X"])
    i_y = _tien(conn, run, nguon_usd, 4, f"{y}.00", "USD", doc["Y"])
    lenh = {k: "P" + k + h[:6] + "-1" for k in "ABXY"}
    tien = {"A": a, "B": b, "X": n, "Y": y}
    chen_dong_pm(conn, NgucCanh(run, "v1.0", "v1.0", "v1.0", "RAW", "L1"), [
        DongPM(3 + i, lenh[k].split("-")[0], lenh[k], D(f"{tien[k]}.00"), "VND",
               "Approve", canon_ref(doc[k]), "HD-K32", "C-K32", ref_tho=doc[k],
               tho=THO)
        for i, k in enumerate("ABXY")])
    gt.ghep_lenh(conn, mot_lan_nap(run), i_b, [lenh["B"]], actor=ACTOR,
                 reason="WO-032 bai thu - kho TEST")
    # ⚠ Mối nối khác tiền tệ — đúng câu `chay_nap.chen_moi_noi` *(bộ nạp tự
    #   ghép)*; cửa ghi tay ném `KhacTienTe` nên ⛔ đi đường ấy được.
    conn.execute("INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh,"
                 " run_id) VALUES (%s,%s,%s,'A',%s)",
                 (i_y, lenh["Y"], D(f"{y}.00"), run))
    return {"run": run, "h": h, "doc": doc, "lenh": lenh, "tien": tien,
            "i_a": i_a, "i_b": i_b, "i_x": i_x, "i_y": i_y, "dg_b": dg_b}


def goi_ok(may, duong: str) -> dict:
    ok, r = _goi(may, V + duong)
    assert ok == 200, (duong, r)
    return r


def goi_ca(may, ca: dict, duong: str) -> dict:
    """`goi_ok` với phạm vi **của chính ca** *(`?run_id=<ca.run>` — cửa thật,
    `xu_ly.pham_vi_cua_yeu_cau` ⇒ `mot_lan_nap`, giao với bản trắng)*.

    ⛔⛔ **Vì sao** *(`WO-051` `AC-10` — `KQ-061` lượt 4: **9** đỏ ở 4 tệp, xanh
    khi chạy riêng)*: phía lệnh của các cửa `lenh-cho` / `lenh-da-gan` /
    `itl-candidates` đọc **ảnh PM hiệu lực** = ảnh có `max(read_at)` **của cả
    phạm vi** *(`anh_pm.py:65`)*. Không gửi `run_id` ⇒ phạm vi `chi_nap_that`
    = **mọi** lần nạp của kho TEST ⇒ ảnh của ca chỉ "hiệu lực" **khi không ai
    nạp ảnh nào mới hơn** sau khi ca dựng. Một tiến trình khác ghi `fls_test`
    giữa lượt *(máy 8099 / kịch bản Chrome dựng ca — đúng điều `KQ-061` nghi)*
    là đủ: cửa trả `0 hàng` / `⛔ không có trong ảnh chụp hiệu lực`. Tái hiện
    có kiểm soát 06/10 *(`BG-064`)*: chèn **một** ảnh PM mới hơn vào kho TEST
    rồi chạy 4 tệp ⇒ **13** đỏ *(chứa cả 7 bài cửa của `KQ-061`)*; bản dùng
    hàm này, **cùng** trạng thái kho ⇒ xanh.
    ⭐ Thân vẫn từ **cửa HTTP thật**; chỉ phạm vi là của ca *(khuôn `WO-023`
    `(j)` — `test_wo045_…::_pham_vi_ca`)*."""
    return goi_ok(may, duong + ("&" if "?" in duong else "?")
                  + "run_id=" + ca["run"])


#: Đường màn gọi ⇒ đường gọi cửa *(⛔ đổi tham số: màn `F01G` gọi `limit=500`)*.
def duong_cua(ca: dict) -> dict[str, str]:
    L = ca["lenh"]
    return {
        "/queue/lenh-cho/summary": "/queue/lenh-cho/summary",
        "/queue/lenh-cho/ro": "/queue/lenh-cho/ro",
        "LUOI_VND": "/queue/lenh-cho?limit=50&curr=VND",
        "GHEP_MAY": "/queue/lenh-cho?limit=500&ro=may&tu_chung=0",
        # ⭐ `WO-037`: chip `Chưa gán` gọi **cả** `ro=nguoi` *(`CHIP_CUA`)*. Trước
        #   02/10 bản đồ chỉ có `ro=may` — lệnh `X` *(VND khớp mã chỉ dòng USD)*
        #   nằm ở `may` nên ⛔ ai thấy lỗ; nay `X` sang `nguoi` ⇒ cổng quét đỏ
        #   đúng chỗ thiếu đường.
        "GHEP_NGUOI": "/queue/lenh-cho?limit=500&ro=nguoi",
        "GHEP_DA_GAN": "/queue/lenh-da-gan?limit=500",
        "UV_A": f"/queue/lenh/{L['A']}/itl-candidates?limit=50",
        "UV_X": f"/queue/lenh/{L['X']}/itl-candidates?limit=50",
        "SO_A": f"/queue/lenh/{L['A']}/so?q={ca['h']}",
        "SO_X": f"/queue/lenh/{L['X']}/so?q={ca['h']}",
        "PM_A": f"/queue/lenh/{L['A']}",
        "CHUM_B": f"/queue/{ca['i_b']}/chum",
    }


def goi_het(may, ca: dict) -> dict:
    """`{khoá: thân 'data' cửa trả}` cho mọi đường trong `duong_cua`."""
    return {k: goi_ok(may, d)["data"] for k, d in duong_cua(ca).items()}


def hang(than: dict, ma: str) -> dict:
    """Hàng lệnh `ma` trong thân cửa danh sách. ⛔ Thấy ⇒ ĐỎ *(`Đ3`)*."""
    for x in than.get("rows") or []:
        if x.get("pm_line_id") == ma or (x.get("the") or {}).get("ma_lenh") == ma:
            return x
    raise AssertionError(f"⛔ không đo được: cửa ⛔ trả lệnh {ma} "
                         f"({len(than.get('rows') or [])} hàng)")
