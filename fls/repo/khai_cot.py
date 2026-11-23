# -*- coding: utf-8 -*-
"""Chỗ DUY NHẤT ghi/đọc **bản khai ánh xạ cột** *(`DD-I10`, migration `0016`)*.

⛔⛔ **Bảng này ⛔ KHÔNG lưu dữ liệu — nó lưu CÁCH ĐỌC dữ liệu.** Kế toán đã tự
giải bài *"60+ định dạng sao kê"* ở **dòng 1 của mỗi sheet `R |`**; `QĐ-ITL-105`
bỏ Google Sheets khỏi đường nạp, nên bản khai ấy phải có **chỗ ở trong kho** —
nếu không FLS sẽ phải **đoán vị trí cột**, thứ `fls/adapters/sao_ke.py` cấm
thẳng vì *"đoán ⛔ không phải kém chính xác — nó là **sai tiền**"*.

★ **Bốn luật của tầng này:**

  ⓐ ⛔ **CHỈ-THÊM.** ⛔ Không một câu `UPDATE`/`DELETE` nào. Sửa khai = ghi một
    `version` **MỚI**. Một dòng nạp tháng trước phải giải thích được bằng **bản
    khai hiệu lực LÚC ẤY** — sửa đè là **viết lại lịch sử** *(`INV-I08`)*.

  ⓑ ⛔ **ĐỦ 6 TRƯỜNG hoặc ⛔ KHÔNG GHI GÌ.** Kiểm **trước** khi chạm kho, rồi 6
    dòng vào trong **MỘT giao dịch**. Ghi một phần là **mất cột trong im lặng**,
    và cột mất có thể là cột **tiền**.
    ⭐ Và phép kiểm ấy ⛔ **không viết lại ở đây** — nó gọi
    `sao_ke.kiem_ban_khai`, đúng hàm mà đường đọc sheet đang dùng. Hai bản kiểm
    là hai chỗ để chúng lệch nhau.

  ⓒ ⛔ **`hieu_luc_tu` do MÁY đặt, ⛔ người gọi ⛔ không truyền vào được.**
    Nếu truyền được thì `version` cao nhất và mốc mới nhất có thể **⛔ không
    cùng chỉ về một bản khai** ⇒ câu *"bản khai nào đang hiệu lực"* có **hai**
    câu trả lời. ⛔ Không mở cửa ấy thì hai thứ tự **⛔ không bao giờ cãi nhau**.

  ⓓ ⛔ **⛔ Không có bản khai MẶC ĐỊNH.** Nguồn chưa ai khai ⇒ `KhongCoKhai`,
    ⛔ không đoán. Một mặc định im lặng chính là cơ chế đẻ ra **6.843 ô
    *"Input here"*** của AS-IS *(`GAC-Other`/`Headquarters2`)* — sai mà ⛔ không
    ai thấy.

⚠ **`FLS-NGUON-LA` (404) và `FLS-KHAI-KHONG-CO` (409) là HAI câu khác nhau**
  *(`BA-07` §4b ⓺)*: *"⛔ không có nguồn ấy"* ≠ *"có nguồn, nhưng ⛔ chưa ai khai
  cách đọc nó"*. Hai câu dẫn người dùng đi **hai đường sửa khác nhau**, nên
  `doc_khai()` soi nguồn **trước**, ⛔ không gộp cả hai vào một lỗi.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Mapping

from fls.adapters.sao_ke import (SAU_TRUONG, TRUONG_HOP_LE, TRUONG_NGAY,
                                 TRUONG_THEM_QUY, BanKhaiHong,
                                 kiem_ban_khai, truong_cam_doc)

# Thứ tự cột dùng cho câu `INSERT` — khai MỘT lần.
_COT = ("source_id", "version", "truong", "cot", "actor", "thu_tu")

# ⭐⭐ `QĐ-ITL-113` — hai cách đọc ngày, và ⛔ **KHÔNG có cách thứ ba**.
#
# ⛔ `None` = *"nguồn ⛔ CHƯA khai"*, ⛔ **không** = *"coi như `dmy`"*. Đo
#   08/09 trên ảnh chụp thật: **1.894/8.368 dòng (22,6%)** có ngày mơ hồ, trải
#   **29/60 nguồn** — và **29/29** nguồn ấy là **`mdy`**, ⛔ **0** nguồn `dmy`
#   *(OCBC Singapore · TCB USD — sao kê nước ngoài)*. ⇒ Một mặc định *"vì đây
#   là Việt Nam"* sẽ **hoán ngày↔tháng trên 1.894 dòng**, đúng lớp `QĐ-ITL-17`.
# ⛔ ⛔ **⛔ KHÔNG khai lại ở đây.** Miền giá trị này sống ở
#    `fls.kiem.thu_tu_ngay` — nơi phép ĐO bằng chứng dùng nó. Hai bản khai là
#    hai chỗ để chúng trôi khỏi nhau, và lúc ấy kho sẽ nhận một giá trị mà
#    phép đề xuất ⛔ không bao giờ đề xuất *(hay ngược lại)*.
from fls.kiem.thu_tu_ngay import THU_TU_HOP_LE  # noqa: E402

# ⛔ `thu_tu` CHỈ có nghĩa trên trường ngày — kho cũng cưỡng chế bằng
#    `fls_khai_cot_thu_tu_ck`. Khai tên ở đây MỘT lần, ⛔ không gõ lại `'Date'`.
TRUONG_MANG_THU_TU = TRUONG_NGAY


class LoiKhai(Exception):
    """Gốc của mọi lỗi tầng này. Mang sẵn `ma` để tầng cửa dịch ra HTTP."""

    ma = "FLS-KHAI-THIEU"


class NguonLa(LoiKhai):
    """⛔ `source_id` ⛔ không có trong `fls_source` — **404**."""

    ma = "FLS-NGUON-LA"


class KhongCoKhai(LoiKhai):
    """⛔ Nguồn **có**, nhưng ⛔ chưa ai khai cách đọc nó — **409**, ⛔ không 404."""

    ma = "FLS-KHAI-KHONG-CO"


@dataclass(frozen=True)
class BanKhai:
    """Một bản khai ĐỦ 6 trường của một nguồn, tại một `version`.

    ⭐ `cot` cố ý mang **đúng khuôn** `sao_ke.doc_ban_khai()` trả về
    *(`{tên trường: chỉ số cột}`)*, để task `3` thay nguồn bản khai
    *(dòng 1 → kho)* mà ⛔ **không phải dịch một khuôn nào** — mọi phép dịch
    giữa hai khuôn là một chỗ để lệch len vào.
    """

    source_id: int
    version: int
    cot: dict[str, int]
    hieu_luc_tu: datetime
    actor: str
    # ⭐ `QĐ-ITL-113` — thứ tự ngày, `None` = nguồn ⛔ CHƯA khai *(⛔ không phải
    #   "mặc định `dmy`")*. Nó đi kèm bản khai vì nó **là** một phần của bản
    #   khai: `cot` nói *đọc cột nào*, `thu_tu` nói *đọc thế nào*.
    thu_tu: str | None = None


def _soi_khai(khai: Mapping[str, int]) -> dict[str, int]:
    """Kiểm bản khai **trước khi chạm kho**. Trả bản đã chuẩn hoá kiểu.

    ⛔ Tên lạ thì **NỔ**, ⛔ không lặng lẽ bỏ qua. Bỏ qua thì một lỗi gõ
    *(`Credit ` thừa dấu cách)* biến thành *"thiếu trường `Credit`"*, và thông
    báo sẽ chỉ người ta đi sửa **nhầm chỗ**.
    """
    # ⛔⛔ **Kiểm CẤM trước kiểm LẠ** — và đây ⛔ không phải thứ tự tuỳ ý.
    #    Cả hai phép đều chặn được hôm nay, nhưng chúng nói **hai câu khác
    #    hẳn**. *"Tên lạ"* dẫn người ta đi **thêm tên vào `SAU_TRUONG`** —
    #    đúng việc phải ⛔ KHÔNG BAO GIỜ làm với `Số CMND/CCCD/Passport`.
    #    ⇒ Thông báo phải nói thẳng **cấm**, ⛔ không nói **lạ**.
    cam = sorted(t for t in khai if truong_cam_doc(t))
    if cam:
        raise LoiKhai(
            "⛔ trường %s mang DỮ LIỆU CÁ NHÂN — ⛔ không được đưa vào kho, "
            "và ⛔ không được thêm vào `SAU_TRUONG` để đi qua chỗ này "
            "(`QĐ-ITL-92` mở rộng 08/09; xem `GAP-PII-01`)" % cam)

    # ⭐ Từ vựng = **6 bắt buộc + 2 tuỳ chọn của lằn quỹ** (`QĐ-ITL-108`).
    #   ⛔ Phép kiểm *"đủ 6"* vẫn ở `_kiem_du_sau()` — hai việc khác nhau:
    #   *"tên này có hợp lệ ⛔ không"* ≠ *"đã khai đủ ⛔ chưa"*.
    la = sorted(set(khai) - set(TRUONG_HOP_LE))
    if la:
        raise LoiKhai(
            "⛔ tên trường lạ %s — chỉ nhận %d tên: %s (6 bắt buộc) + %s "
            "(tuỳ chọn, lằn quỹ)"
            % (la, len(TRUONG_HOP_LE), list(SAU_TRUONG),
               list(TRUONG_THEM_QUY)))

    ra: dict[str, int] = {}
    for t, c in khai.items():
        # ⛔ `bool` là con của `int` trong Python: `True` sẽ lọt thành cột 1.
        if isinstance(c, bool) or not isinstance(c, int):
            raise LoiKhai(
                "⛔ `%s`: chỉ số cột phải là SỐ NGUYÊN, nhận %r (%s)"
                % (t, c, type(c).__name__))
        if c < 0:
            raise LoiKhai("⛔ `%s`: chỉ số cột âm (%d) — cột 0-based" % (t, c))
        ra[t] = c
    return ra


def _kiem_du_sau(ten: str, cot: Mapping[str, int]) -> None:
    """Luật ⓑ — và nó gọi **đúng hàm** của đường đọc sheet, ⛔ không viết lại.

    ⭐ MỘT chỗ đổi `BanKhaiHong` *(ngôn ngữ của tầng adapter)* sang `LoiKhai`
      *(mang mã HTTP cho tầng cửa)*. Đổi ở **hai** chỗ thì sớm muộn một đường
      quên đổi, và tầng cửa sẽ ném ra `500` cho một lỗi của **người dùng**.
      ⛔ Giữ NGUYÊN câu chữ của `sao_ke` — hai câu cho cùng một lỗi là hai thứ
      để lệch.
    """
    try:
        kiem_ban_khai(ten, dict(cot), cho="kho")
    except BanKhaiHong as e:
        raise LoiKhai(str(e)) from e


def ghi_khai(conn, source_id: int, khai: Mapping[str, int], *,
             actor: str, thu_tu: str | None = None) -> BanKhai:
    """Ghi một bản khai MỚI cho `source_id`. ⛔ Không sửa khai cũ.

    ⭐ `thu_tu` *(`QĐ-ITL-113`)* — `'dmy'` | `'mdy'` | `None`. Nó **chỉ** đậu
      trên dòng `Date`; kho cũng cưỡng chế bằng `fls_khai_cot_thu_tu_ck`.

    ⛔⛔ **Kiểm ở đây DÙ kho đã có `CHECK`.** Một `CheckViolation` bật lên từ
       tầng kho đọc ra là *"vi phạm ràng buộc `fls_khai_cot_thu_tu_ck`"* — câu
       ấy ⛔ **không nói cho kế toán biết phải sửa gì**. Hàng rào của kho là để
       ⛔ không ai **lách được**; thông điệp đọc được là việc của tầng này.

    ⭐ Câu `SELECT … FROM fls_source … FOR UPDATE` làm **hai** việc bằng một
      lượt: ⓐ trả lời *"nguồn này có thật không"* *(`NguonLa`)* và ⓑ **xếp
      hàng** phép cấp `version` cho riêng nguồn ấy. ⛔ Không có khoá đó thì hai
      người khai cùng lúc cùng đọc ra `max(version)` giống nhau; khoá duy nhất
      `(source_id, version, truong)` sẽ chặn người thứ hai, nhưng chặn bằng một
      **lỗi trùng khoá** thì người dùng đọc ⛔ không hiểu — còn ở đây họ chỉ đơn
      giản nhận `version` kế tiếp.
    """
    if not str(actor or "").strip():
        raise LoiKhai(
            "⛔ thiếu `actor`. Bản khai là **hành vi của người** — một bản khai "
            "⛔ không ai đứng tên thì ⛔ không ai giải thích được vì sao cột "
            "tiền lại nằm ở đó")

    if thu_tu is not None and thu_tu not in THU_TU_HOP_LE:
        raise LoiKhai(
            "⛔ `thu_tu=%r` ⛔ không hợp lệ — chỉ %s. ⛔ Không nhận `DMY`, ⛔ "
            "không nhận `d/m/y`: một trường tự do là một trường sẽ có **ba "
            "cách viết cho một ý**, và lúc ấy phép so sẽ lệch mà ⛔ không ai "
            "thấy" % (thu_tu, " hoặc ".join("`%s`" % x for x in THU_TU_HOP_LE)))

    sach = _soi_khai(khai)
    _kiem_du_sau("nguồn #%s" % source_id, sach)

    if thu_tu is not None and TRUONG_MANG_THU_TU not in sach:
        raise LoiKhai(
            "⛔ khai `thu_tu` mà bản khai ⛔ không có trường `%s` — ⛔ không "
            "có chỗ nào để đậu" % TRUONG_MANG_THU_TU)

    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute(
                "SELECT source_id FROM fls_source WHERE source_id = %s"
                " FOR UPDATE", (source_id,))
            if cur.fetchone() is None:
                raise NguonLa(
                    "⛔ ⛔ không có nguồn `source_id=%s` trong `fls_source`"
                    % source_id)

            cur.execute(
                "SELECT coalesce(max(version), 0) + 1 FROM fls_khai_cot"
                " WHERE source_id = %s", (source_id,))
            ver = int(cur.fetchone()[0])

            # ⛔⛔ **Ghi theo `sach`, ⛔ KHÔNG theo `SAU_TRUONG`.**
            #    Bản trước lặp `for t in SAU_TRUONG` — đúng chừng nào bản khai
            #    **chỉ** có 6 trường. `QĐ-ITL-108` cho lằn quỹ khai thêm
            #    `Legal Entity`/`CDT` ⇒ hai trường ấy **rơi mất trong im lặng**
            #    lúc ghi, trong khi hàm **vẫn trả về đủ 8**.
            #
            #    ⭐⭐ Và cái hỏng thật ⛔ không phải *"mất hai trường"* — nó là
            #    **một vòng lặp vô hạn**: người gọi so `doc_khai()` *(6)* với
            #    bản khai vừa trích *(8)*, thấy **khác**, ghi `version` mới
            #    *(vẫn 6)*, rồi lần chạy sau **lại thấy khác**. Mỗi lần chạy
            #    một `version` rác, mãi mãi, và ⛔ không cổng nào báo vì mỗi
            #    dòng riêng lẻ đều hợp lệ.
            cur.executemany(
                "INSERT INTO fls_khai_cot (%s) VALUES (%s)"
                % (", ".join(_COT), ", ".join(["%s"] * len(_COT))),
                # ⛔ `thu_tu` CHỈ trên dòng `Date` — 5 dòng còn lại `NULL`.
                #    Rải nó ra mọi dòng thì kho chặn *(`CHECK`)*, và đúng ra
                #    nó phải chặn: `thu_tu` của `Debit` ⛔ không có nghĩa gì.
                [(source_id, ver, t, c, actor,
                  thu_tu if t == TRUONG_MANG_THU_TU else None)
                 for t, c in sorted(sach.items())])

            # ⭐ Đọc lại mốc thay vì tự đặt `datetime.now()` ở Python: mốc phải
            #   là mốc **của kho**, ⛔ không phải của máy gọi (lệch múi giờ /
            #   lệch đồng hồ là một chỗ hỏng ⛔ không ai ngờ tới).
            cur.execute(
                "SELECT DISTINCT hieu_luc_tu FROM fls_khai_cot"
                " WHERE source_id = %s AND version = %s", (source_id, ver))
            moc = cur.fetchall()

    # ⛔ `now()` của PostgreSQL là mốc **đầu giao dịch**, nên **mọi** dòng của
    #    một bản khai PHẢI dùng chung MỘT mốc. Nếu ⛔ không, một phép đọc rơi
    #    vào **giữa** sẽ trả về một bản khai **thiếu trường** — tức
    #    `BanKhaiHong` trên một cái kho hoàn toàn lành. Kiểm ngay tại đây vì
    #    đó là chỗ duy nhất biết.
    assert len(moc) == 1, (
        "⛔ %d dòng của một bản khai mang %d mốc khác nhau — một phép đọc rơi "
        "vào giữa sẽ thấy bản khai THIẾU trường" % (len(sach), len(moc)))
    return BanKhai(source_id=source_id, version=ver, cot=sach,
                   hieu_luc_tu=moc[0][0], actor=actor, thu_tu=thu_tu)


def doc_khai(conn, source_id: int, *, tai: datetime | None = None) -> BanKhai:
    """Bản khai **đang hiệu lực tại `tai`** *(mặc định: bây giờ)*.

    ⭐ *"Hiệu lực tại một mốc"* ⛔ không phải là chuyện hàn lâm: nó là thứ làm
      cho câu *"dòng nạp 27/08 đọc bằng bản khai nào"* **có câu trả lời** sau
      khi ngân hàng đổi mẫu sao kê. ⛔ Không có nó thì mọi dòng cũ lặng lẽ được
      giải thích bằng bản khai của **hôm nay**.

    ⛔ **Vẫn kiểm đủ 6 trường lúc ĐỌC**, dù `ghi_khai()` đã ghi cả cụm trong một
      giao dịch. Một phép kiểm chỉ tin vào chính người ghi của nó là một phép
      kiểm ⛔ không đo gì: bản khai có thể vào kho bằng một đường khác *(nạp
      tay, khôi phục dở dang)*, và cái nó thiếu có thể là **cột tiền**.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT source_id FROM fls_source WHERE source_id = %s",
                    (source_id,))
        if cur.fetchone() is None:
            # ⚠ 404, ⛔ KHÔNG phải 409 — xem khối đầu tệp.
            raise NguonLa(
                "⛔ ⛔ không có nguồn `source_id=%s` trong `fls_source`"
                % source_id)

        cur.execute(
            "SELECT max(version) FROM fls_khai_cot"
            " WHERE source_id = %s AND hieu_luc_tu <= coalesce(%s, now())",
            (source_id, tai))
        r = cur.fetchone()
        if r is None or r[0] is None:
            raise KhongCoKhai(
                "⛔ nguồn `source_id=%s` ⛔ CHƯA có bản khai nào%s. ⛔ Không "
                "đoán vị trí cột — đo trên kho: **68 dòng chảy · 19 bố cục "
                "cột** (`DD-I10`)"
                % (source_id, "" if tai is None else " tại mốc %s" % tai))
        ver = int(r[0])

        cur.execute(
            "SELECT truong, cot, hieu_luc_tu, actor, thu_tu FROM"
            " fls_khai_cot WHERE source_id = %s AND version = %s",
            (source_id, ver))
        hang = cur.fetchall()

    cot = {h[0]: int(h[1]) for h in hang}
    _kiem_du_sau("nguồn #%s (khai v%d)" % (source_id, ver), cot)
    # ⛔ `thu_tu` chỉ đậu trên dòng `Date` ⇒ lấy TỪ ĐÚNG dòng ấy, ⛔ không
    #    `max()`/`any()` cho qua: một `thu_tu` lạc sang dòng khác là một khuyết
    #    tật phải hiện ra, ⛔ không phải thứ để lặng lẽ vớt lên.
    tt = [h[4] for h in hang if h[0] == TRUONG_MANG_THU_TU]
    return BanKhai(source_id=source_id, version=ver, cot=cot,
                   hieu_luc_tu=hang[0][2], actor=hang[0][3],
                   thu_tu=tt[0] if tt else None)
