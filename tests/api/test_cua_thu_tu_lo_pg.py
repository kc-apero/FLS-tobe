# -*- coding: utf-8 -*-
"""`POST /chup/{id}/thu-tu` — khai thứ tự ngày CẢ LÔ *(`QĐ-ITL-117`)*.

⭐⭐⭐ **Phép đo mở cửa này, ⛔ không một ý tưởng tiện tay.** Trên ảnh `23719`
   *(8.368 dòng thật)*: **34/34** nguồn có ngày CHUỖI **tự chứng minh bằng dữ
   liệu của chính nó** — mỗi nguồn có ≥1 dòng phần-sau `> 12` *(tổng **2.296**
   dòng)*, và `chac_dmy` = **0** ở khắp **60** nguồn. Đếm trên **4.187** ô
   chuỗi: phần **trước** dấu `/` lớn nhất là **12** *(0 lần `>12`)*, phần
   **sau** lớn nhất **31** *(2.296 lần `>12`)*.

⇒ Máy đề xuất `mdy` **34 lần** và **34 lần một đáp án**. Bắt kế toán bấm **27**
  cú *(29 cần khai − 2 đã khai)* để trả lời một câu mà dữ liệu đã tự trả lời là
  bắt họ **đọc 27 lần rồi bấm theo phản xạ** — và một cú bấm theo phản xạ ⛔
  **không phải** *"người ấn định"* như `QĐ-ITL-113` viết, nó chỉ **trông** như.

⛔⛔ **Nên ranh giới của cửa này là TỰ CHỨNG, ⛔ không phải "cả lô".** Ba bài
   đắt nhất ở đây đều canh đúng chỗ ấy:
     ⓐ `test_than_mang_thu_tu_thi_400…` — cửa lô ⛔ **không có đường nào** để
        khai `dmy` cho 27 nguồn bằng một cú bấm;
     ⓑ `test_nguon_KHONG_TU_CHUNG_thi_TU_CHOI_CA_LO…` — ⛔ không khai phần đo
        được rồi bỏ qua phần còn lại *(đó là "xanh trên tập con")*;
     ⓒ `test_BAT_DONG…` — ⛔ không đè bản khai của người bằng phép đo của máy.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.api.test_cua_chup_pg import _chup, _khai_du, _nguon_day_du, _o
from tests.api.test_cua_nap_pg import V, _goi, _hex, may  # noqa: F401

pytestmark = pytest.mark.pg


# ── ba khuôn ô `Date`, và mỗi khuôn có một VIỆC ────────────────────────────
#   `_CHUNG`  phần sau `> 12` ⇒ **tự nói ra** là `mdy`, ⛔ không cần ai khai
#   `_MO_HO`  cả hai phần `<= 12` ⇒ ⛔ **không đọc được** nếu nguồn chưa khai
#   `_SERI`   Sheets đã hiểu là ngày ⇒ `thu_tu` ⛔ **không bao giờ được đọc**
_CHUNG, _MO_HO, _SERI = "08/25/2026", "08/03/2026", 45586


def _dem_khai(sid: int) -> int:
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_khai_cot WHERE source_id = %s",
                    (sid,))
        return cur.fetchone()[0]


def _thu_tu_dang_dung(sid: int):
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute(
            "SELECT thu_tu FROM fls_khai_cot WHERE source_id = %s"
            " AND truong = 'Date' ORDER BY version DESC LIMIT 1", (sid,))
        r = cur.fetchone()
        return r[0] if r else None


def _dem_ngay(khoa: str, ngay: str) -> int:
    """Số dòng của nguồn `khoa` **vào sổ** đúng ngày `ngay` *(ISO)*."""
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl WHERE source_sheet = %s"
                    " AND doc_date = %s", (khoa, ngay))
        return cur.fetchone()[0]


def _nguon_tu_chung() -> tuple[int, str, int]:
    """Nguồn **tự chứng** `mdy`: 1 dòng làm chứng + 1 dòng mơ hồ. `(sid, khoá, ảnh)`."""
    sid, khoa = _nguon_day_du()
    cid = _chup({sid: 1}, [(sid, 0, _o(**{"Date": _CHUNG})),
                           (sid, 1, _o(**{"Date": _MO_HO}))])
    return sid, khoa, cid


# ════════════════════════════════════════════════ ① cửa LÀM ĐÚNG việc của nó
def test_khai_LO_ghi_dung_de_xuat_cho_TUNG_nguon_va_GIU_NGUYEN_cot(may):
    """⭐ Một cú bấm ⇒ N bản khai, mỗi bản theo bằng chứng **của nguồn đó**.

    ⛔ *"Cả lô một `thu_tu`"* là một cửa khác hẳn: nó sẽ đúng ở ảnh `23719`
      *(34/34 đều `mdy`)* và **sai im lặng** ở ảnh đầu tiên có một nguồn `dmy`.
      Bài này ghim rằng giá trị ghi ra là **của từng nguồn**.
    """
    a, khoa_a = _nguon_day_du()
    b, khoa_b = _nguon_day_du()
    cid = _chup({a: 1, b: 1},
                [(a, 0, _o(**{"Date": _CHUNG})), (a, 1, _o(**{"Date": _MO_HO})),
                 (b, 0, _o(**{"Date": _CHUNG})), (b, 1, _o(**{"Date": _MO_HO}))])

    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [a, b]})
    assert ma == 200, d
    assert d["data"]["so_nguon_khai_moi"] == 2, d["data"]
    assert _thu_tu_dang_dung(a) == "mdy"
    assert _thu_tu_dang_dung(b) == "mdy"

    # ⛔ `cot` PHẢI y nguyên — cửa này khai *"thứ tự"*, ⛔ không *"cả bản"*.
    theo = {n["source_id"]: n for n in d["data"]["nguon"]}
    assert theo[a]["source_key"] == khoa_a and theo[b]["source_key"] == khoa_b
    assert {n["version"] for n in d["data"]["nguon"]} == {2}
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT truong, cot FROM fls_khai_cot"
                    " WHERE source_id = %s AND version = 2", (a,))
        assert dict(cur.fetchall()) == _khai_du(), (
            "⛔ bản khai mới ⛔ KHÔNG chở đủ 6 trường y như bản cũ")


def test_moi_nguon_tra_ve_mot_CAU_co_CON_SO__khong_chi_mot_chu_mdy(may):
    """⛔⛔ Một cửa khai hộ mà ⛔ không nói **đã soi bao nhiêu dòng** là một
       cửa ⛔ không kiểm lại được: `mdy` trên 2.296 dòng làm chứng và `mdy`
       đoán từ hư không **⛔ trông y hệt nhau** trong bản ghi.
    """
    sid, _k, cid = _nguon_tu_chung()
    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [sid]})
    assert ma == 200, d
    n = d["data"]["nguon"][0]
    assert any(ch.isdigit() for ch in n["cau"]), n["cau"]
    # ⭐ Hai ô của cả lô — và ô thứ hai là **hậu quả**, ⛔ không phải trang trí.
    assert d["data"]["so_dong_lam_chung"] == 1, d["data"]
    assert d["data"]["so_dong_mo_ho"] == 1, (
        "⛔ ⛔ không nói bản khai vừa ghi CỨU được bao nhiêu dòng ⇒ ⛔ không ai "
        "biết cú bấm ấy có hậu quả gì: %s" % d["data"])


def test_khai_LO_roi_NAP_thi_dong_MO_HO_VAO_SO_chu_KHONG_bi_LOAI(may):
    """⭐⭐⭐ **Cửa này có HẬU QUẢ đo được** — ⛔ không chỉ ghi một chữ vào bảng.

    ⛔⛔ Đây là bài duy nhất chứng minh cú bấm gộp **thay thế được** 27 cú bấm
       lẻ: dòng `08/03/2026` *(cả hai phần `<= 12`)* trước khi khai thì **bị
       loại kèm lý do**; sau khi khai thì **vào sổ**. Thiếu bài này thì cả
       `QĐ-ITL-117` chỉ là một cửa ghi chữ.
    """
    sid, _k, cid = _nguon_tu_chung()

    # ⓐ nạp TRƯỚC khi khai — dòng mơ hồ bị loại, và lô **vẫn đi tiếp**
    ma, d = _goi(may, f"{V}/nap/lo",
                 than={"chup_id": cid, "source_ids": [sid],
                       "run_id": "NAP-2026-09-09-TRUOC" + _hex(4)})
    assert ma == 200, d
    # ⛔⛔ Đo `vao_so`/`loai`, ⛔ **KHÔNG** `so_dong_ra`: `so_dong_ra` = số dòng
    #    **đọc ra khỏi sheet** *(vẫn là 2)*, và bài này hỏi *"có vào SỔ ⛔
    #    không"*. Vấp đúng chỗ này một lần: bài xanh/đỏ theo một con số ⛔
    #    không nói về câu nó hỏi.
    assert (d["data"]["vao_so"], d["data"]["loai"]) == (1, 1), (
        "⛔ dòng mơ hồ phải BỊ LOẠI kèm lý do khi nguồn chưa khai, và lô "
        "**vẫn đi tiếp**: %s" % d["data"])
    assert _dem_ngay(_k, "2026-08-03") == 0

    # ⓑ khai gộp, rồi nạp lại ⇒ dòng ấy vào sổ
    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [sid]})
    assert ma == 200, d
    ma, d = _goi(may, f"{V}/nap/lo",
                 than={"chup_id": cid, "source_ids": [sid],
                       "run_id": "NAP-2026-09-09-SAU" + _hex(4)})
    assert ma == 200, d
    assert d["data"]["loai"] == 0, (
        "⛔ dòng mơ hồ VẪN bị loại sau khi khai — bản khai ⛔ không tới được "
        "tầng sổ: %s" % d["data"])
    # ⭐ Dòng `08/25` đã vào sổ ở lượt ⓐ ⇒ lượt này nó là `trung`. Chỉ dòng mơ
    #   hồ là **mới** — và đó đúng là thứ bản khai vừa mở đường cho.
    assert (d["data"]["vao_so"], d["data"]["trung"]) == (1, 1), d["data"]
    assert _dem_ngay(_k, "2026-08-03") == 1, (
        "⛔ `08/03/2026` ⛔ KHÔNG vào sổ như 3/8 ⇒ bản khai `mdy` vừa ghi ⛔ "
        "không được tầng sổ đọc")
    assert _dem_ngay(_k, "2026-03-08") == 0, (
        "⛔⛔ vào sổ như 8/3 ⇒ HOÁN ngày↔tháng, đúng lớp lỗi `QĐ-ITL-17` "
        "(~181 tỷ sai kỳ)")


# ═══════════════════════════════ ② ba cái NỔ — và đây là giá trị của cửa này
def test_than_mang_thu_tu_thi_400__cua_LO_khong_de_NGUOI_an_dinh(may):
    """⭐⭐⭐ **Cả điểm của `QĐ-ITL-117` nằm ở bài này.**

    `POST /sources/{id}/thu-tu` là cửa *"NGƯỜI ấn định"* ⇒ nó **phải** nhận
    `thu_tu`. Cửa lô là cửa *"DỮ LIỆU tự ấn định"* ⇒ nó **đo lại** rồi ghi
    đúng cái nó đo ra.

    ⛔⛔ Nếu cửa lô nhận `thu_tu`, nó thành **cỗ máy khai `dmy` cho 27 nguồn
       bằng một cú bấm** — tức đúng cái `QĐ-ITL-113` dựng ra để chặn, chỉ
       nhanh hơn 27 lần. Và biên bản sẽ trông **hoàn toàn bình thường**.
    """
    sid, _k, cid = _nguon_tu_chung()
    truoc = _dem_khai(sid)
    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu",
                 than={"source_ids": [sid], "thu_tu": "dmy"})
    assert ma == 400, d
    assert "sources/{source_id}/thu-tu" in d["error"]["detail"], (
        "⛔ NỔ mà ⛔ không chỉ ra cửa ĐÚNG để tự ấn định ⇒ người gọi sẽ đi tìm "
        "một cách lách: %s" % d["error"])
    assert _dem_khai(sid) == truoc, "⛔ NỔ rồi mà vẫn ghi"


def test_nguon_KHONG_TU_CHUNG_thi_TU_CHOI_CA_LO__khong_khai_PHAN_do_duoc(may):
    """⛔⛔⛔ Một lô khai *"thành công 1/2"* là đúng lớp lỗi cả bộ này chống.

    Người bấm thấy xanh; nguồn kia lặng lẽ ở lại `NULL`; và ⛔ **không cổng nào
    đỏ** vì mọi dòng `fls_khai_cot` đều hợp lệ. ⇒ Nổ CẢ LÔ, và nguồn ⛔ không
    tự chứng phải đi qua cửa một-nguồn nơi có đúng **một người** chịu trách
    nhiệm.
    """
    tot, _k1, _c = _nguon_tu_chung()
    mu, khoa_mu = _nguon_day_du()
    # ⛔ Nguồn này **toàn dòng mơ hồ** ⇒ ⛔ không có bằng chứng nào của riêng nó
    cid = _chup({tot: 1, mu: 1},
                [(tot, 0, _o(**{"Date": _CHUNG})),
                 (tot, 1, _o(**{"Date": _MO_HO})),
                 (mu, 0, _o(**{"Date": _MO_HO})),
                 (mu, 1, _o(**{"Date": "01/02/2026"}))])
    truoc = (_dem_khai(tot), _dem_khai(mu))

    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu",
                 than={"source_ids": [tot, mu]})
    assert ma == 422, d
    assert d["error"]["code"] == "FLS-THU-TU-KHONG-TU-CHUNG", d["error"]
    assert khoa_mu in d["error"]["detail"], (
        "⛔ NỔ mà ⛔ không nêu TÊN nguồn nào bị vướng: %s" % d["error"])
    assert (_dem_khai(tot), _dem_khai(mu)) == truoc, (
        "⛔⛔ đã khai nguồn TỰ CHỨNG rồi mới nổ ⇒ lô khai NỬA VỜI, và ⛔ không "
        "ai kiểm lại trạng thái ấy")


def test_BAT_DONG_voi_ban_khai_cua_NGUOI_thi_NO__khong_DE_LAI(may):
    """⛔⛔ Người bảo `dmy`, dữ liệu bảo `mdy` — đó là **một bất đồng THẬT**.

    Lặng lẽ ghi theo máy ở đây là **xoá một câu trả lời của người**, và xoá nó
    bằng một `version` mới trông y hệt mọi `version` khác. ⇒ NỔ kèm **cả hai**
    giá trị, để người đọc thấy mình đang phải chọn giữa cái gì và cái gì.
    """
    sid, khoa, cid = _nguon_tu_chung()
    ma, _d = _goi(may, f"{V}/sources/{sid}/thu-tu", than={"thu_tu": "dmy"})
    assert ma == 200
    truoc = _dem_khai(sid)

    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [sid]})
    assert ma == 422, d
    for phai_co in (khoa, "dmy", "mdy"):
        assert phai_co in d["error"]["detail"], (
            "⛔ câu nổ thiếu %r ⇒ ⛔ không đọc được bất đồng: %s"
            % (phai_co, d["error"]))
    assert _dem_khai(sid) == truoc and _thu_tu_dang_dung(sid) == "dmy", (
        "⛔⛔ bản khai `dmy` của NGƯỜI bị máy đè")


# ═════════════════════════════ ③ ba cái KHÔNG GHI — và chúng ⛔ không phải lỗi
def test_bam_LAN_HAI_thi_KHONG_sinh_version_Y_HET_ban_cu(may):
    """⛔ Sổ chỉ-thêm ⛔ không **cấm** một `version` y hệt — nhưng một cú bấm
      lần hai ⛔ không được **trông như** N lần khai mới.

    ⚠ Và con số phải nói ra sự thật: `khai_moi = 0`, `da_dung = 1`.
    """
    sid, _k, cid = _nguon_tu_chung()
    ma, _d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [sid]})
    assert ma == 200
    sau_lan_mot = _dem_khai(sid)

    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [sid]})
    assert ma == 200, d
    assert d["data"]["so_nguon_khai_moi"] == 0, d["data"]
    assert d["data"]["so_nguon_da_dung"] == 1, d["data"]
    assert d["data"]["nguon"][0]["ket_qua"] == "da_dung"
    assert _dem_khai(sid) == sau_lan_mot, "⛔ bấm lần hai vẫn ghi thêm một bản"


def test_nguon_TOAN_NGAY_SO_thi_KHONG_GHI__thu_tu_cua_no_VO_NGHIA(may):
    """⛔⛔ `parse_ngay` chỉ hỏi `thu_tu` khi **cả hai** phần `<= 12`.

    ⇒ Với nguồn toàn ngày sê-ri, `thu_tu` **⛔ không bao giờ được đọc**. Ghi
      vào là dựng một bản khai **gợi ý rằng nó có tác dụng** — và lần sau ai
      đó sẽ **sửa nó để chữa một dòng ⛔ không liên quan**. Đo được **16/60**
      nguồn thuộc loại này *(và 5 nguồn nữa toàn chuỗi nhưng `mo_ho` = 0)*.
    """
    sid, _khoa = _nguon_day_du()
    cid = _chup({sid: 1}, [(sid, 0, _o(**{"Date": _SERI})),
                           (sid, 1, _o(**{"Date": _SERI}))])
    truoc = _dem_khai(sid)

    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than={"source_ids": [sid]})
    assert ma == 200, d
    assert d["data"]["so_nguon_khong_can"] == 1, d["data"]
    assert d["data"]["so_nguon_khai_moi"] == 0, d["data"]
    assert _dem_khai(sid) == truoc, "⛔ ghi một `thu_tu` ⛔ không ai đọc"


def test_source_ids_RONG_thi_400__KHONG_co_mac_dinh_LAY_HET(may):
    """⛔ Cùng luật với cửa nạp lô: máy ⛔ **không tự chọn** nguồn nào để **ấn
      định kỳ kế toán**. *"⛔ Không nói thì lấy hết"* đúng 59 lần rồi sai lần
      thứ 60 — và lần ấy nó khai cho một nguồn ⛔ không ai xem.
    """
    _sid, _k, cid = _nguon_tu_chung()
    for than in ({}, {"source_ids": []}, {"source_ids": "tat_ca"}):
        ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu", than=than)
        assert ma == 400, (than, d)
        assert "source_ids" in d["error"]["detail"], d["error"]


def test_nguon_NGOAI_anh_chup_thi_NO_ca_lo__khong_am_tham_bo_qua(may):
    """⛔ Bỏ qua trong im lặng thì `so_nguon_khai_moi` **nhỏ hơn** số nguồn màn
      hình đã hiện, mà ⛔ không ai được nói vì sao.
    """
    sid, _k, cid = _nguon_tu_chung()
    la, _khoa_la = _nguon_day_du()
    ma, d = _goi(may, f"{V}/chup/{cid}/thu-tu",
                 than={"source_ids": [sid, la]})
    assert ma == 422, d
    assert str(la) in d["error"]["detail"], d["error"]
    assert _thu_tu_dang_dung(sid) is None, "⛔ nổ rồi mà vẫn khai nguồn kia"


def test_anh_chup_KHONG_CO_thi_404(may):
    ma, d = _goi(may, f"{V}/chup/999888777/thu-tu",
                 than={"source_ids": [1]})
    assert ma == 404, d
    assert d["error"]["code"] == "FLS-CHUP-KHONG-CO", d["error"]
