# -*- coding: utf-8 -*-
"""Nhóm **ẢNH CHỤP** *(`BA-07` §4c, `QĐ-ITL-110`)* CHẠY THẬT qua HTTP.

⛔⛔ **Bốn cửa này sinh ra vì một phép đo, ⛔ không vì một ý tưởng:** soi màn
   `F04` xuống bảng tuyến ngày 08/09 thì màn cần **5 cửa** và **3 cửa ⛔ KHÔNG
   TỒN TẠI**; hai cửa **có** thì cả hai đòi người gọi **đưa sẵn `dong`** — tiền
   đề *"màn hình đã cầm tệp"* của `QĐ-ITL-105` ⓷ mà `QĐ-ITL-109` **đã lật**.

⭐ **Bài đắt nhất ở đây ⛔ KHÔNG phải bài gọi-rồi-đọc.** Nó là
   `test_NAP_tu_ANH_CHUP_ghi_dung_chup_id_vao_fls_run`: cột `fls_run.chup_id`
   mà ⛔ không ai ghi thì nó y hệt cột `khai_id` — **một cột dựng ra để trả lời
   một câu hỏi mà ⛔ không bao giờ có giá trị** *(`GAP-CHUP-04`)*.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo import chup as ch
from fls.repo.nguon_dai import ghi_dai
from tests.api.test_cua_nap_pg import (V, _goi, _hex,  # noqa: F401
                                       _may, may)

pytestmark = pytest.mark.pg


# ⛔⛔ **`25`, ⛔ KHÔNG `05` — và con số ấy là một BÀI HỌC, ⛔ không phải tuỳ ý.**
#
# Bản đầu của tệp này dùng `"05/08/2026"`. Hai bài `nap` **ĐỎ THẬT** với
# `400 · "ngay mo ho, khong doan"`: `05/08` đọc được **hai** cách, và tầng sổ
# **từ chối đoán** *(`QĐ-ITL-17`: **93%** dòng sổ thật bị hoán ngày↔tháng,
# ~**181 tỷ** sai kỳ ⇒ đoán ở đây là đoán TIỀN)*.
#
# ⭐⭐ Nên hai bài ấy vừa **diễn lại `GAP-NAP-02` trên đường thật**: hành vi
#    lúc ấy là **giết CẢ LÔ**, và với lô **8.365 dòng** thì kế toán ⛔ không có
#    đường nào đi tiếp.
#
# ✅ **`GAP-NAP-02` ĐÃ ĐÓNG 2026-09-08 (`QĐ-ITL-113`)** — và ⛔ **không** phải
#    bằng một mặc định. Hai nửa:
#      ⓐ dòng mơ hồ vào `fls_reject` **kèm lý do**, lô **đi tiếp**
#         *(lỗi THỨ TỰ ở `chay_nap.danh_seq_trung` — nó chạy TRƯỚC vòng loại)*;
#      ⓑ nguồn **khai `thu_tu`** thì 1.894 dòng ấy **vào sổ** — bản khai
#         quyết định, ⛔ không phép đoán nào.
#
# ⚠ Ranh giới vẫn đứng và vẫn đáng ghi: `xem-truoc` **ĐI QUA** ngày mơ hồ mà
#   ⛔ không kêu *(9 luật soát ⛔ không phân tích ngày)*. ⇒ Một biên bản **9
#   luật xanh** vẫn có thể đi kèm một lô mà **một phần dòng sẽ vào
#   `fls_reject`**. Biên bản nay trả thêm `thu_tu` để nói ra điều đó.
def _o(**doi):
    o = {"Date": "25/08/2026", "Currency": "VND", "Debit": 1000,
         "Credit": "", "Reference number": "FT" + _hex(6)}
    o.update(doi)
    return o


def _khai_du() -> dict[str, int]:
    from fls.adapters.sao_ke import SAU_TRUONG
    return {t: i for i, t in enumerate(SAU_TRUONG)}


def _nguon_day_du(khai: bool = True, dai: bool = True) -> tuple[int, str]:
    """Một nguồn RIÊNG, có bản khai + dải đọc — ⛔ không dùng chung với bài khác."""
    khoa = "R | Chup" + _hex()
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        with c.cursor() as cur:
            cur.execute("INSERT INTO fls_source (source_key, src_type)"
                        " VALUES (%s,'Bank') RETURNING source_id", (khoa,))
            sid = cur.fetchone()[0]
        if khai:
            from fls.repo.khai_cot import ghi_khai
            ghi_khai(c, sid, _khai_du(), actor="test")
        if dai:
            ghi_dai(c, sid, {"Date": "!A2:A", "Debit": "!D2:D",
                             "Credit": "!E2:E"}, danh_muc="BankAccountList")
    return sid, khoa


def _chup(nguon: dict[int, int], dong) -> int:
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        return ch.ghi_chup(c, spreadsheet_id="SID-TEST", lan="Bank",
                           actor="test", nguon=nguon, dong=dong).chup_id


# ═════════════════════════════════════════════ ① GET /sources — trạng thái ①
def test_GET_sources_tra_nguon_kem_khai_version_va_chup_cuoi(may):
    sid, khoa = _nguon_day_du()
    _chup({sid: 1}, [(sid, 0, _o())])

    ma, d = _goi(may, f"{V}/sources", pt="GET")
    assert ma == 200, d
    theo = {n["source_id"]: n for n in d["data"]["nguon"]}
    assert sid in theo, "⛔ nguồn vừa tạo ⛔ không có trong danh sách"
    n = theo[sid]
    assert n["source_key"] == khoa
    assert n["khai_version"] == 1
    assert n["chup_cuoi"] is not None, "⛔ ⛔ không nói nguồn này chụp lần cuối khi nào"
    assert d["data"]["so_nguon"] == len(d["data"]["nguon"])


def test_nguon_CHUA_AI_KHAI_van_CO_MAT_voi_khai_version_null(may):
    """⭐ `khai_version = null` là một **CÂU TRẢ LỜI**, ⛔ không phải thiếu dữ liệu.

    ⛔ Lọc nguồn chưa khai ra khỏi danh sách là làm *"⛔ chưa ai khai"* và
      *"⛔ không tồn tại"* trông **giống hệt nhau** — và kế toán sẽ đi tìm một
      sheet họ đang có trong tay.
    """
    sid, _khoa = _nguon_day_du(khai=False, dai=False)
    _ma, d = _goi(may, f"{V}/sources", pt="GET")
    theo = {n["source_id"]: n for n in d["data"]["nguon"]}
    assert sid in theo, "⛔ nguồn CHƯA khai bị LỌC RA — hai câu bị gộp làm một"
    assert theo[sid]["khai_version"] is None
    assert theo[sid]["chup_cuoi"] is None


def test_GET_sources_KHAI_THANG_rang_KHONG_co_trang_thai_nguon(may):
    """⛔⛔ `GAP-CHUP-02` — và cửa phải **NÓI RA**, ⛔ không im lặng bỏ trường.

    `BA-06` §7 ① đòi nguồn `InActive`/`Closed` hiện **mờ**. `fls_source` ⛔
    **không có cột trạng thái** *(7 cột, ⛔ không cột nào là nó)*. ⇒ Bỏ trường
    đi trong im lặng thì màn hình sẽ **tưởng mọi nguồn đều `Active`** — đúng
    lớp lỗi *"mặc định im lặng"* đã đẻ ra **6.843 ô `Input here`** của AS-IS.
    """
    _ma, d = _goi(may, f"{V}/sources", pt="GET")
    assert d["data"]["gap_trang_thai"] == "GAP-CHUP-02"
    assert all(n["trang_thai_nguon"] is None for n in d["data"]["nguon"])


# ════════════════════════════════════ ② GET .../khai-cot — trạng thái ③
def test_GET_khai_cot_tra_CA_DAY_version(may):
    """⛔ Trả **cả dãy**, ⛔ không chỉ bản mới nhất.

    Câu *"vì sao dòng nạp tháng trước đọc cột khác"* chỉ trả lời được nếu
    thấy được **các bản cũ** — đó là cả lý do bảng khai là **chỉ-THÊM**.
    """
    sid, khoa = _nguon_day_du()
    _goi(may, f"{V}/sources/{sid}/khai-cot",
         than={"cot": dict(_khai_du(), Credit=9)})          # ⇒ `version` 2

    ma, d = _goi(may, f"{V}/sources/{sid}/khai-cot", pt="GET")
    assert ma == 200, d
    assert d["data"]["source_key"] == khoa
    assert d["data"]["hieu_luc"]["version"] == 2
    assert d["data"]["hieu_luc"]["cot"]["Credit"] == 9
    assert [b["version"] for b in d["data"]["dai_version"]] == [2, 1]
    # ⭐ Bản `v1` ⛔ KHÔNG đổi một ô — luật chỉ-THÊM đọc được từ chính cửa.
    assert d["data"]["dai_version"][1]["cot"]["Credit"] == 4
    assert d["data"]["hieu_luc"]["actor"], "⛔ bản khai ⛔ không nói AI khai"


def test_GET_khai_cot_nguon_CHUA_KHAI_tra_409_chu_KHONG_404(may):
    """⚠ Nguồn **có**, chỉ là ⛔ chưa ai khai cách đọc — hai câu khác nhau."""
    sid, _ = _nguon_day_du(khai=False, dai=False)
    ma, d = _goi(may, f"{V}/sources/{sid}/khai-cot", pt="GET")
    assert ma == 409, (ma, d)
    assert d["error"]["code"] == "FLS-KHAI-KHONG-CO"


def test_GET_khai_cot_nguon_LA_tra_404(may):
    ma, d = _goi(may, f"{V}/sources/{2 ** 40}/khai-cot", pt="GET")
    assert ma == 404 and d["error"]["code"] == "FLS-NGUON-LA"


# ═══════════════════════════════════════ ③ GET /chup — trạng thái ②
def test_GET_chup_mot_anh_hien_CA_nguon_ra_0_DONG(may):
    """⭐⭐ Toàn bộ lý do `fls_chup_nguon` tồn tại, đọc được **qua cửa**.

    Suy tập nguồn từ **dữ liệu** thì sheet ra `0` dòng **biến mất** — đúng điểm
    mù `S8` từng tự lộ. Nếu cửa cũng suy như thế thì màn `F04` sẽ hiện *"đọc
    được 59 nguồn"* trong khi nó đã đọc **60**.
    """
    a, _ = _nguon_day_du()
    b, _ = _nguon_day_du()
    cid = _chup({a: 1, b: 1}, [(a, 0, _o()), (a, 1, _o())])

    ma, d = _goi(may, f"{V}/chup/{cid}", pt="GET")
    assert ma == 200, d
    assert d["data"]["so_nguon"] == 2
    assert d["data"]["so_dong"] == 2
    theo = {n["source_id"]: n["so_dong"] for n in d["data"]["nguon"]}
    assert theo == {a: 2, b: 0}
    assert d["data"]["giay"] is None or isinstance(d["data"]["giay"], float)


def test_GET_chup_mot_anh_gioi_han_dong_MAC_DINH_50(may):
    """⛔ Mặc định **50**, ⛔ không phải *"tất cả"* — một ảnh có **8.365** dòng."""
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, i, _o()) for i in range(60)])

    _ma, d = _goi(may, f"{V}/chup/{cid}", pt="GET")
    assert len(d["data"]["dong"]) == 50
    # ⭐ Nhưng `so_dong` vẫn nói **SỰ THẬT** — ⛔ không phải độ dài trang.
    assert d["data"]["so_dong"] == 60, (
        "⛔ `so_dong` bị ghi bằng số dòng ĐÃ TRẢ ⇒ màn sẽ nói ảnh này có 50 dòng")


def test_GET_chup_ANH_KHONG_CO_tra_404(may):
    ma, d = _goi(may, f"{V}/chup/{2 ** 40}", pt="GET")
    assert ma == 404 and d["error"]["code"] == "FLS-CHUP-KHONG-CO"


def test_GET_chup_liet_ke_moi_nhat_TRUOC(may):
    a, _ = _nguon_day_du()
    c1 = _chup({a: 1}, [(a, 0, _o())])
    c2 = _chup({a: 1}, [(a, 0, _o())])
    _ma, d = _goi(may, f"{V}/chup?limit=5", pt="GET")
    ids = [x["chup_id"] for x in d["data"]["chup"]]
    assert ids.index(c2) < ids.index(c1), "⛔ ⛔ không xếp mới nhất trước"


def test_GET_chup_lan_LA_tra_400(may):
    ma, d = _goi(may, f"{V}/chup?lan=Quy", pt="GET")
    assert ma == 400 and d["error"]["code"] == "FLS-BAD-REQUEST"


# ═══════════════════════════ ④ `chup_id` XOR `dong` trên hai cửa nạp
def test_XEM_TRUOC_tu_ANH_CHUP_ra_bien_ban_9_luat(may):
    a, khoa = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o()), (a, 1, _o())])

    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": a, "chup_id": cid})
    assert ma == 200, d
    bb = d["data"]
    assert bb["nguon"] == khoa
    assert len(bb["luat"]) == 9, "⛔ biên bản ⛔ không đủ 9 luật"
    assert all("da_do" in k for k in bb["luat"]), (
        "⛔ có luật ⛔ không nói ĐÃ ĐO BAO NHIÊU — *đo được 0 thứ ⇒ ⛔ KHÔNG ĐẠT*")
    assert bb["so_dong_vao"] == 2 and bb["so_dong_ra"] == 2
    assert bb["se_ghi"] is True


def test_CA_HAI_chup_id_va_dong_thi_400(may):
    """⛔⛔ Hai đường vào cho **cùng một lô** là hai chỗ để chúng lệch nhau."""
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o())])
    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": a, "chup_id": cid, "dong": [[]]})
    assert ma == 400 and d["error"]["code"] == "FLS-BAD-REQUEST"
    assert "CẢ" in d["error"]["detail"]


def test_KHONG_CO_ca_hai_thi_400_va_KHONG_co_mac_dinh(may):
    """⛔ ⛔ Không có mặc định *"⛔ không nói thì lấy ảnh mới nhất"*.

    Đoán đúng 59 lần rồi sai lần thứ 60 là **nạp lại dữ liệu của hôm khác**.
    """
    a, _ = _nguon_day_du()
    _chup({a: 1}, [(a, 0, _o())])          # ⭐ CÓ một ảnh — máy vẫn ⛔ không lấy
    ma, d = _goi(may, f"{V}/nap/xem-truoc", than={"source_id": a})
    assert ma == 400 and d["error"]["code"] == "FLS-BAD-REQUEST"
    assert "⛔ không có mặc định" in d["error"]["detail"].lower() or \
           "không có mặc định" in d["error"]["detail"].lower()


def test_LO_RONG_dong_bang_rong_VAN_la_mot_yeu_cau_HOP_LE(may):
    """⛔⛔ `{"dong": []}` là **có khoá**, ⛔ không phải *"⛔ không đưa gì"*.

    Nếu tầng cửa hỏi `than.get("dong")` thì `[]` **falsy** ⇒ nó trả về một
    thông báo nói người dùng **thiếu thứ họ đã đưa**. Đó là lý do `than_co`
    hỏi `khoa in than`.
    """
    a, _ = _nguon_day_du()
    ma, d = _goi(may, f"{V}/nap/xem-truoc", than={"source_id": a, "dong": []})
    assert ma == 200, (ma, d)
    assert d["data"]["so_dong_vao"] == 0
    # ⭐ Và `S1` phải nói **ĐÃ ĐO 1 sheet** chứ ⛔ không im.
    s1 = next(k for k in d["data"]["luat"] if k["ten"].startswith("S1"))
    assert s1["da_do"] == 1


def test_ANH_CHUP_KHONG_doc_nguon_dang_chon_thi_409(may):
    """⚠ Ảnh **có**, nguồn **có**, chỉ là ảnh ấy ⛔ không đọc nguồn này.

    ⛔ Gộp câu này với `404` thì người dùng gõ lại **đúng cái `chup_id` vừa
      thất bại** — một cửa bắt người ta thử lại cái vừa không chạy.
    """
    a, _ = _nguon_day_du()
    b, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o())])
    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": b, "chup_id": cid})
    assert ma == 409, (ma, d)
    assert d["error"]["code"] == "FLS-CHUP-KHONG-NGUON"


def test_chup_id_LA_thi_404(may):
    a, _ = _nguon_day_du()
    ma, d = _goi(may, f"{V}/nap/xem-truoc",
                 than={"source_id": a, "chup_id": 2 ** 40})
    assert ma == 404 and d["error"]["code"] == "FLS-CHUP-KHONG-CO"


# ═════════════════════ ⑤ LINEAGE — cột dựng ra thì PHẢI có ai ghi
def test_NAP_tu_ANH_CHUP_ghi_dung_chup_id_vao_fls_run(may):
    """⭐⭐⭐ **Bài đắt nhất của tệp này.**

    ⛔⛔ Cột `fls_run.khai_id` sinh ra ở task `1` và `erd_policy` khai hẳn một
       **đường lineage** dựa vào nó — mà quét mã ngày 08/09: **⛔ KHÔNG một câu
       `INSERT`/`UPDATE` nào set nó**. Cổng ERD ⛔ không thấy, vì nó canh **FK
       đã KHAI**, ⛔ không canh **cột có được GHI**.

    ⇒ Bài này là cổng để `chup_id` ⛔ **không** thành cột thứ hai như thế.
    """
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o()), (a, 1, _o())])
    rid = "NAP-2026-09-08-CHUP" + _hex(4)

    ma, d = _goi(may, f"{V}/nap",
                 than={"source_id": a, "chup_id": cid, "run_id": rid})
    assert ma == 200, d
    assert d["data"]["run_id"] == rid

    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT chup_id FROM fls_run WHERE run_id = %s", (rid,))
        assert cur.fetchone()[0] == cid, (
            "⛔ `fls_run.chup_id` ⛔ KHÔNG được ghi ⇒ nó là cột thứ hai dựng ra "
            "để trả lời một câu hỏi mà ⛔ không bao giờ có giá trị (GAP-CHUP-04)")


def test_NAP_bang_duong_dong_thi_chup_id_la_NULL_chu_KHONG_bia(may):
    """⭐ `R-A1` — một lô ⛔ không có ảnh chụp **phải HIỆN RA** là `NULL`.

    ⛔ Khai `NOT NULL` là buộc phải **bịa** một ảnh chụp cho mọi lô test, tức
      làm bẩn đúng cái cột dựng ra để nói thật.
    """
    a, _ = _nguon_day_du()
    rid = "NAP-2026-09-08-DONG" + _hex(4)
    ma, d = _goi(may, f"{V}/nap",
                 than={"source_id": a, "run_id": rid,
                       "dong": [["25/08/2026", "", "VND", 1000, "",
                                 "FT" + _hex(6)]]})
    assert ma == 200, d
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT chup_id FROM fls_run WHERE run_id = %s", (rid,))
        assert cur.fetchone()[0] is None


# ══════════════════════════════════ ⑥ GET /chup/{id}/thu-tu — `QĐ-ITL-113`
def test_BANG_CHUNG_thu_tu_dem_dung_va_KHONG_QUYET_gi(may):
    """⭐⭐⭐ Cửa trả **bằng chứng**, ⛔ không trả một kết luận.

    ⛔ Khoá phải là `de_xuat`, ⛔ **không** phải `thu_tu` — quyền ấn định kỳ
      kế toán ở **người**. Bài này ghim đúng cái tên ấy: đổi nó thành `thu_tu`
      là đổi **ai quyết**, mà một cú đổi tên thì ⛔ không cổng nào khác thấy.
    """
    sid, khoa = _nguon_day_du()
    cid = _chup({sid: 1}, [
        (sid, 0, _o(**{"Date": "08/25/2026"})),      # chac chan `mdy`
        (sid, 1, _o(**{"Date": "08/03/2026"})),      # mo ho
        (sid, 2, _o(**{"Date": 45586})),             # seri — ⛔ khong mo ho
    ])
    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    assert ma == 200, d
    n = next(x for x in d["data"]["nguon"] if x["source_id"] == sid)

    assert "de_xuat" in n and "thu_tu" not in n, (
        "⛔ cửa này ⛔ KHÔNG được trả khoá `thu_tu` — đó là thứ NGƯỜI khai")
    assert n["de_xuat"] == "mdy"
    assert n["da_khai"] is None, "⛔ chưa ai khai ⇒ phải hiện ra là chưa"
    assert n["can_khai"] is True
    assert n["bang_chung"] == {"so_dong": 3, "o_so": 1, "o_chuoi": 2,
                               "chac_dmy": 0, "chac_mdy": 1, "mo_ho": 1}
    # ⭐ Câu phải mang CON SỐ, ⛔ không chỉ mang lời khuyên.
    assert "1" in n["cau"] and "mdy" in n["cau"], n["cau"]
    assert d["data"]["so_dong_mo_ho"] >= 1


def test_nguon_TOAN_ngay_SO_thi_KHONG_CAN_khai(may):
    """⛔ Đòi khai một nguồn ⛔ không mơ hồ = bắt trả lời câu ⛔ không tồn tại.

    Đo 08/09: **21/50** nguồn thật toàn ngày-số ⇒ `thu_tu` của chúng vô nghĩa.
    """
    sid, _ = _nguon_day_du()
    cid = _chup({sid: 1}, [(sid, i, _o(**{"Date": 45586 + i}))
                           for i in range(3)])
    _ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    n = next(x for x in d["data"]["nguon"] if x["source_id"] == sid)
    assert (n["can_khai"], n["de_xuat"]) == (False, None)
    assert "⛔ không cần khai" in n["cau"], n["cau"]
    assert d["data"]["so_can_khai"] == 0


def test_MAU_THUAN_thi_cua_KHONG_de_xuat_gi(may):
    """⛔⛔ Nguồn có CẢ hai bằng chứng ⇒ ⛔ không thứ tự nào đúng cho cả nguồn."""
    sid, _ = _nguon_day_du()
    cid = _chup({sid: 1}, [
        (sid, 0, _o(**{"Date": "25/08/2026"})),      # chac `dmy`
        (sid, 1, _o(**{"Date": "08/25/2026"})),      # chac `mdy`
        (sid, 2, _o(**{"Date": "03/01/2026"})),      # mo ho
    ])
    _ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    n = next(x for x in d["data"]["nguon"] if x["source_id"] == sid)
    assert n["mau_thuan"] is True and n["de_xuat"] is None
    assert "MÂU THUẪN" in n["cau"], n["cau"]


def test_DA_KHAI_thi_hien_ra__va_so_con_thieu_TUT(may):
    """⭐⭐ `so_can_khai` một mình ⛔ KHÔNG nói được việc còn phải làm.

    Khai xong rồi thì `so_can_khai` **vẫn** là 29 — nên cửa phải trả thêm
    `so_con_thieu` *(cần khai mà CHƯA khai)*. Một con số ⛔ không tụt khi việc
    đã xong là một con số ⛔ không dùng để theo dõi được.
    """
    sid, _ = _nguon_day_du()
    cid = _chup({sid: 1}, [(sid, 0, _o(**{"Date": "08/25/2026"})),
                           (sid, 1, _o(**{"Date": "08/03/2026"}))])
    _ma, a = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    truoc = a["data"]["so_con_thieu"]
    assert truoc >= 1

    ma, k = _goi(may, f"{V}/sources/{sid}/khai-cot",
                 than={"cot": _khai_du(), "thu_tu": "mdy"})
    assert ma == 200, k

    _ma, b = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    n = next(x for x in b["data"]["nguon"] if x["source_id"] == sid)
    assert n["da_khai"] == "mdy"
    assert n["can_khai"] is True, "⛔ khai rồi thì `can_khai` VẪN đúng"
    assert b["data"]["so_con_thieu"] == truoc - 1, (truoc, b["data"])
    assert b["data"]["so_can_khai"] == a["data"]["so_can_khai"]


def test_BANG_CHUNG_soi_MOI_dong__khong_dung_50_dong_dau(may):
    """⭐⭐⭐ ⛔ Bằng chứng tính trên 50 dòng đầu sẽ **đề xuất SAI trong im lặng**.

    `GET /chup/{id}` mặc định trả **50** dòng *(đúng cho một lưới xem trước)*.
    Bài này dựng một nguồn có **60 dòng mơ hồ** rồi **một** dòng làm chứng ở
    **cuối** — nếu phép đo dùng cùng đường ấy, nó sẽ thấy `de_xuat = None`.
    """
    sid, _ = _nguon_day_du()
    dong = [(sid, i, _o(**{"Date": "08/03/2026"})) for i in range(60)]
    dong.append((sid, 60, _o(**{"Date": "08/25/2026"})))     # bang chung o CUOI
    cid = _chup({sid: 1}, dong)
    _ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    n = next(x for x in d["data"]["nguon"] if x["source_id"] == sid)
    assert n["bang_chung"]["so_dong"] == 61, n["bang_chung"]
    assert n["de_xuat"] == "mdy", (
        "⛔ đề xuất `None` ⇒ phép đo đã dừng ở 50 dòng đầu và ⛔ KHÔNG thấy "
        "dòng làm chứng — một nguồn 2.168 dòng sẽ bị đọc sai y như thế")


def test_o_ngay_GIU_NGUYEN_KIEU_qua_jsonb(may):
    """⛔⛔ `o ->> 'Date'` sẽ hạ **4.175 ô seri** thành chuỗi `"45586"`.

    Lúc ấy phép đo báo *"⛔ không có ô số nào"* và **mọi** nguồn thành *"cần
    khai"*. ⛔ Đúng cái bẫy `doc_cot` đã cắn một lần *(`QĐ-ITL-102` ⓶)*.
    """
    sid, _ = _nguon_day_du()
    cid = _chup({sid: 1}, [(sid, 0, _o(**{"Date": 45586})),
                           (sid, 1, _o(**{"Date": 46000.5}))])
    _ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", pt="GET")
    n = next(x for x in d["data"]["nguon"] if x["source_id"] == sid)
    assert n["bang_chung"]["o_so"] == 2, n["bang_chung"]
    assert n["bang_chung"]["o_chuoi"] == 0


def test_thu_tu_cua_anh_chup_KHONG_CO_thi_404(may):
    ma, d = _goi(may, f"{V}/chup/99999999/thu-tu", pt="GET")
    assert ma == 404 and d["error"]["code"] == "FLS-CHUP-KHONG-CO", d


# ══════════════════════ ⑦ POST /sources/{id}/thu-tu — `QĐ-ITL-113`
def test_GHI_thu_tu_sinh_version_MOI_va_GIU_NGUYEN_cot(may):
    """⭐⭐⭐ Cửa này tồn tại để **⛔ không có** chu trình đọc-sửa-ghi ở màn.

    ⛔⛔ Bản khai là **chỉ-THÊM**: `version` mới phải chở **đủ 6 trường**. Nếu
       màn phải *"đọc `cot` rồi gửi lại"* qua `POST …/khai-cot`, thì ai khai
       `cot` mới trong khe giữa hai lượt sẽ bị **đè lại bằng `cot` CŨ** — mà
       `version` vẫn tăng ⇒ ⛔ **không cổng nào thấy**, vì mọi dòng riêng lẻ
       đều hợp lệ.
    """
    sid, _ = _nguon_day_du()
    # ⓐ khai `cot` v2 co mot cot LECH — de chung minh no duoc GIU
    ma, _ = _goi(may, f"{V}/sources/{sid}/khai-cot",
                 than={"cot": dict(_khai_du(), Credit=9)})
    assert ma == 200

    ma, d = _goi(may, f"{V}/sources/{sid}/thu-tu", than={"thu_tu": "mdy"})
    assert ma == 200, d
    assert d["data"]["version"] == 3, d["data"]
    assert d["data"]["thu_tu"] == "mdy"
    # ⭐ `cot` cua v2 di NGUYEN sang v3 — ⛔ khong tut ve ban goc.
    assert d["data"]["cot"]["Credit"] == 9, (
        "⛔ `cot` bị đặt lại về bản gốc ⇒ cửa này đã **đè** bản khai của "
        "người khác, đúng cái nó sinh ra để chặn")

    # ⓑ va doc lai qua cua XEM: ca day con du, ⛔ khong ai sua khai cu
    _ma, k = _goi(may, f"{V}/sources/{sid}/khai-cot", pt="GET")
    assert [b["version"] for b in k["data"]["dai_version"]] == [3, 2, 1]
    assert k["data"]["hieu_luc"]["thu_tu"] == "mdy"
    assert k["data"]["dai_version"][1]["thu_tu"] is None, (
        "⛔ bản khai CŨ bị sửa — luật chỉ-THÊM vỡ")


def test_GHI_thu_tu_KHONG_co_thu_tu_thi_400__khong_am_tham_xoa(may):
    """⛔ Gọi *"khai thứ tự"* mà ⛔ không đưa thứ tự = ⛔ không có việc gì làm.

    ⛔⛔ Và lặng lẽ ghi `NULL` là **XOÁ** thứ tự người ta đã khai trước đó —
       một cú xoá đi qua một cửa mang tên *"khai"*.
    """
    sid, _ = _nguon_day_du()
    for than in ({}, {"thu_tu": None}, {"thu_tu": "DMY"}, {"thu_tu": ""},
                 {"thu_tu": 1}):
        ma, d = _goi(may, f"{V}/sources/{sid}/thu-tu", than=than)
        assert ma == 400, (than, ma, d)


def test_GHI_thu_tu_khi_CHUA_KHAI_cot_thi_409__KHONG_tu_dung_ban_khai_rong(may):
    """⛔⛔ ⛔ Không tự dựng một bản khai rỗng để có chỗ đậu `thu_tu`.

    Đoán vị trí cột là thứ `sao_ke` cấm thẳng: *"đoán ⛔ không phải kém chính
    xác — nó là **sai tiền**"*.
    """
    sid, _ = _nguon_day_du(khai=False, dai=False)
    ma, d = _goi(may, f"{V}/sources/{sid}/thu-tu", than={"thu_tu": "mdy"})
    assert ma == 409 and d["error"]["code"] == "FLS-KHAI-KHONG-CO", d
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_khai_cot WHERE source_id=%s",
                    (sid,))
        assert cur.fetchone()[0] == 0, "⛔ bị từ chối mà VẪN ghi một dòng"


def test_GHI_thu_tu_nguon_LA_thi_404(may):
    ma, d = _goi(may, f"{V}/sources/{2 ** 40}/thu-tu", than={"thu_tu": "mdy"})
    assert ma == 404 and d["error"]["code"] == "FLS-NGUON-LA", d
