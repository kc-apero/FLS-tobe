# -*- coding: utf-8 -*-
"""ẢNH CHỤP vùng CHUẨN — chỗ ở của dữ liệu sao kê *(`QĐ-ITL-110`)*.

⛔⛔ **Module này sinh ra vì một PHÉP ĐO, ⛔ không vì một ý tưởng.** Soi màn
   `F04` xuống bảng tuyến thật ngày 08/09 *(**20** tuyến)*: màn cần **5 cửa**
   và **3 cửa ⛔ KHÔNG TỒN TẠI**. Nặng hơn: **hai cửa CÓ vẫn ⛔ không chạy
   được**, vì cả `POST /nap/xem-truoc` lẫn `POST /nap` đòi người gọi **đưa sẵn
   `dong`** — tiền đề *"màn hình đã cầm tệp trong tay người dùng"* của
   `QĐ-ITL-105` ⓷, thứ mà `QĐ-ITL-109` **đã lật**.
   ⇒ Trình duyệt ⛔ không đọc được Sheets, cửa ⛔ không tự đọc
     ⇒ **⛔ KHÔNG CÓ đường nào đưa dữ liệu thật vào kho.**

★ **Ba bảng, và ⛔ KHÔNG một con số nào lưu hai lần:**

    `fls_chup`        một LẦN ĐỌC        — `doc_luc` · workbook · lằn · `giay`
    `fls_chup_nguon`  một NGUỒN/lần đọc  — + `khai_version` **đã dùng**
    `fls_chup_dong`   một DÒNG vùng CHUẨN — ô để `jsonb` theo **tên trường**

⭐⭐ **Vì sao `fls_chup_nguon` phải là một bảng riêng thay vì suy từ bảng
   dòng:** một nguồn đọc ra **0 dòng** thì nó **biến mất** khỏi bảng dòng —
   đúng điểm mù mà `S8` từng tự lộ ra *("sheet ra 0 dòng biến mất khỏi chính
   phép kiểm sinh ra để tìm nó")*. Bảng này làm nó **CÓ MẶT**.

⛔⛔ **⛔ KHÔNG lưu `so_dong`/`so_nguon` ở bảng đầu.** Cả hai **suy được**, và
   một cái đầu ghi `so_dong = 8.365` cạnh một bảng dòng **RỖNG** là **một lời
   nói dối mà ⛔ không cổng nào thấy** — đúng luật nền *"đo được 0 thứ ⇒ ⛔
   KHÔNG ĐẠT"*. `giay` thì **giữ**, vì nó ⛔ không suy được từ đâu.

⛔ **CHỈ-THÊM.** Chụp lại ⇒ **`chup_id` MỚI**; ảnh cũ ⛔ không đổi một ô. Luật
   ấy được **cưỡng chế ở tầng MÃ NGUỒN** *(cổng quét cấm mọi `UPDATE`/`DELETE`
   trong tệp này)*, ⛔ không chỉ là một lời hứa trong docstring — cùng thang
   thuốc `khai_cot.py` và `ghi_tay.py`.

⛔ **`Description` ⛔ KHÔNG BAO GIỜ vào đây** *(`QĐ-ITL-92`/`107`)*. Chặn ở
   **tầng GHI**, ⛔ không ở tầng đọc: chặn lúc đọc thì dữ liệu cá nhân **đã nằm
   trong kho rồi**, và giữa hai lúc ấy nó đã đi vào mọi bản sao lưu.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Mapping, Sequence

from fls.adapters.sao_ke import (TRUONG_DOC_DUOC, TRUONG_NGAY,
                                 truong_cam_doc)

# ⭐ BA lằn. Khuôn RA của chúng **khác số cột** *(`GAP-CANON-02`: bank 10,
#   quỹ 11)* nên một ảnh chụp lẫn hai lằn là một ảnh chụp ⛔ không đọc lại được
#   bằng một khuôn nào.
#
# ⭐⭐ `PM` — lằn thứ **BA**, thêm 09/09 *(`QĐ-ITL-119`, mốc `A3`)*.
#
# ⛔⛔ **Vì sao lệnh chi phải đi qua CHÍNH lằn ảnh chụp này, ⛔ không một đường
# riêng.** Trước 09/09 lệnh chi vào kho bằng **một lệnh dòng lệnh của Dev**
# *(`tools/nap_that.py`)* ⇒ ⛔ không `fls_chup` nào, ⛔ không bản khai cột,
# ⛔ không biên bản soát, và ⛔ không ai biết **ảnh đó đọc lúc nào**. Đo thật:
# **3.703 dòng lệnh, tất cả từ MỘT lượt ngày 27/08** — đóng băng **13 ngày**,
# và ⛔ không cổng nào nói lên điều đó.
#
# ⇒ Dùng lại **nguyên** lằn đã có: ảnh chụp → bản khai → soát → nạp lô. Đổi lại
#   được bốn thứ **miễn phí**: `doc_luc` *(tuổi của ảnh)* · `actor` *(ai đọc)* ·
#   `giay` *(nó mất bao lâu)* · và `fls_run.chup_id` *(vết truy ⛔ không đứt)*.
#
# ⚠ Khuôn RA của lằn `PM` **khác cả hai lằn kia** *(dòng lệnh chi ⛔ không có
#   `Debit`/`Credit`; nó có `amount` + `status` + `ID PMLine`)* — đúng lý lẽ
#   *"một ảnh chụp lẫn hai lằn ⛔ không đọc lại được"* ở trên, nên nó là một
#   **lằn riêng**, ⛔ không nhét vào `Bank`.
LAN: tuple[str, ...] = ("Bank", "Cash", "PM")


class LoiChup(Exception):
    """Gốc của mọi lỗi tầng này."""

    ma = "FLS-CHUP-HONG"


class KhongCoChup(LoiChup):
    """⛔ ⛔ Không có ảnh chụp ấy. ⛔ Không được lẫn với *"có mà rỗng"*."""

    ma = "FLS-CHUP-KHONG-CO"


@dataclass(frozen=True)
class NguonTrongChup:
    source_id: int
    source_key: str
    khai_version: int
    so_dong: int            # ⭐ ĐẾM TỪ BẢNG DÒNG, ⛔ không đọc một cột lưu sẵn


@dataclass(frozen=True)
class Chup:
    chup_id: int
    doc_luc: datetime
    spreadsheet_id: str
    lan: str
    giay: float | None
    actor: str
    nguon: tuple[NguonTrongChup, ...]

    @property
    def so_nguon(self) -> int:
        return len(self.nguon)

    @property
    def so_dong(self) -> int:
        return sum(n.so_dong for n in self.nguon)


# ── GHI ───────────────────────────────────────────────────────────────────
def _soi_o(source_id: int, dong_so: int, o: Mapping[str, Any]) -> dict[str, Any]:
    """⛔ Một ô hợp lệ, hoặc **NỔ**. ⛔ Không có đường *"làm sạch rồi cho qua"*.

    ⭐⭐ **Phép soi này là chỗ luật `QĐ-ITL-92`/`107` thành MÁY.** Nó ⛔ không
      hỏi *"ô này có trông giống dữ liệu cá nhân ⛔ không"* — câu ấy ⛔ không
      trả lời được. Nó hỏi **TÊN TRƯỜNG**, và tên trường thì đã có một từ vựng
      đóng.

    ⛔⛔ **HAI lệnh cấm, HAI căn cứ — và ⛔ KHÔNG được gộp chúng.** Bài
      `test_o_mang_Description_thi_NO...` bắt được đúng chỗ này: vị từ
      `sao_ke.truong_cam_doc("Description")` trả **`False`**, nên thông báo
      đầu tiên tôi viết ⛔ **không nói được VÌ SAO** `Description` bị chặn.

      ⚠ Và cách chữa **⛔ KHÔNG phải** mở rộng `RE_TRUONG_CAM` cho khớp — làm
        thế thì `_soi_khai` sẽ **chặn mọi bản khai của cả 68 nguồn**, vì
        `SAU_TRUONG` **có** `Description` và `kiem_ban_khai` đòi **đủ 6
        trường**. Hai vị từ trả lời hai câu khác nhau:

          `truong_cam_doc`   — *"tên này có được phép xuất hiện trong một BẢN
                               KHAI ⛔ không?"* → `Description` **được**;
                               khối nhân sự **⛔ không**.
          từ vựng ở đây      — *"ô này có được phép vào KHO ⛔ không?"*
                               → ⭐ `Description` **ĐƯỢC, từ `QĐ-ITL-128`**
                               *(17/09 — owner mở lại `QĐ-ITL-92`)*; khối
                               nhân sự **⛔ VẪN KHÔNG** *(`QĐ-ITL-107` là một
                               quyết định KHÁC và ⛔ không bị mở theo)*.

      ⇒ Nêu **đúng căn cứ theo từng trường**, ⛔ không nêu một căn cứ cho cả lô.
    """
    la = sorted(set(o) - set(TRUONG_DOC_DUOC))
    if la:
        # ⛔ Nhanh `Description` da BO 17/09 (`QĐ-ITL-128`): no nay nam
        #   trong `TRUONG_DOC_DUOC` nen ⛔ khong bao gio roi vao `la` nua.
        vi = []
        hr = [t for t in la if truong_cam_doc(t)]
        if hr:
            vi.append("%s (`QĐ-ITL-107` — khối nhân sự `9`…`14`)" % hr)
        raise LoiChup(
            "⛔ nguồn %s dòng %s: ô ảnh chụp có trường ⛔ KHÔNG được phép %s"
            " · cho phép đúng %s%s"
            % (source_id, dong_so, la, list(TRUONG_DOC_DUOC),
               " · ⛔⛔ MANG DỮ LIỆU CÁ NHÂN: " + " · ".join(vi) if vi else ""))
    return dict(o)


def ghi_chup(conn, *, spreadsheet_id: str, lan: str, actor: str,
             nguon: Mapping[int, int],
             dong: Sequence[tuple[int, int, Mapping[str, Any]]],
             giay: float | None = None) -> Chup:
    """Ghi **một lần đọc** — một giao dịch, chỉ-THÊM.

    `nguon` — `{source_id: khai_version}`, **mọi nguồn ĐÃ ĐỌC**, kể cả nguồn
              ra **0 dòng**.
    `dong`  — `[(source_id, dong_so, {tên trường: ô})]`.

    ⛔⛔ **Ba thứ làm NỔ, và cả ba đều là *"⛔ không ghi một ảnh chụp nói dối"*:**

      ⓐ `nguon` **rỗng** ⇒ NỔ. Một ảnh chụp ⛔ không đọc nguồn nào là một dấu
         thời điểm ⛔ không nói gì — và nó sẽ được `F04` hiện ra như *"đã đọc
         lúc 15:02"*. Xanh trên tập rỗng là **chưa đo**.
      ⓑ Một dòng có `source_id` ⛔ **không** nằm trong `nguon` ⇒ NỔ. Ngược lại
         thì bảng dòng chứa dữ liệu của một nguồn mà bảng nguồn nói ⛔ chưa hề
         đọc — **hai bảng kể hai câu chuyện**.
      ⓒ Ô mang trường ⛔ không được phép ⇒ NỔ *(`_soi_o`)*.
    """
    if lan not in LAN:
        raise LoiChup("⛔ `lan=%r` lạ — chỉ %s. Hai lằn khác khuôn RA "
                      "(`GAP-CANON-02`) nên ⛔ không được lẫn vào nhau"
                      % (lan, list(LAN)))
    if not str(spreadsheet_id or "").strip():
        raise LoiChup("⛔ thiếu `spreadsheet_id` — một ảnh chụp ⛔ không nói nó "
                      "đọc workbook NÀO thì ⛔ không đối chiếu được với gì")
    if not str(actor or "").strip():
        raise LoiChup("⛔ thiếu `actor` — chụp là một HÀNH VI, phải có tên")
    if not nguon:
        raise LoiChup(
            "⛔ ⛔ KHÔNG ghi một ảnh chụp ⛔ không đọc nguồn nào. Nó sẽ hiện ra "
            "trên `F04` như một dấu thời điểm thật, trong khi nó ⛔ không đo "
            "được gì — *đo được 0 thứ ⇒ ⛔ KHÔNG ĐẠT*")

    la_nguon = sorted({s for s, _d, _o in dong} - set(nguon))
    if la_nguon:
        raise LoiChup(
            "⛔ %d dòng thuộc nguồn %s mà `nguon` ⛔ không khai đã đọc — bảng "
            "dòng và bảng nguồn sẽ kể HAI câu chuyện khác nhau"
            % (sum(1 for s, _d, _o in dong if s in set(la_nguon)), la_nguon))

    hang = [(s, d, json.dumps(_soi_o(s, d, o), ensure_ascii=False, default=str))
            for s, d, o in dong]

    with conn.transaction():
        with conn.cursor() as cur:
            # ⛔ Khoá nguồn TRƯỚC khi ghi: một nguồn bị xoá giữa hai câu lệnh
            #   thì FK sẽ nổ ở câu thứ hai, và thông báo của kho ⛔ không nói
            #   được nguồn nào.
            cur.execute("SELECT source_id FROM fls_source"
                        " WHERE source_id = ANY(%s) FOR SHARE",
                        (sorted(nguon),))
            co = {r[0] for r in cur.fetchall()}
            thieu = sorted(set(nguon) - co)
            if thieu:
                raise LoiChup("⛔ ⛔ không có nguồn `source_id` %s trong "
                              "`fls_source`" % thieu)

            cur.execute(
                "INSERT INTO fls_chup (spreadsheet_id, lan, giay, actor)"
                " VALUES (%s, %s, %s, %s) RETURNING chup_id",
                (spreadsheet_id, lan, giay, actor))
            cid = cur.fetchone()[0]

            cur.executemany(
                "INSERT INTO fls_chup_nguon (chup_id, source_id, khai_version)"
                " VALUES (%s, %s, %s)",
                [(cid, s, v) for s, v in sorted(nguon.items())])

            if hang:
                cur.executemany(
                    "INSERT INTO fls_chup_dong (chup_id, source_id, dong_so, o)"
                    " VALUES (%s, %s, %s, %s)",
                    [(cid, s, d, o) for s, d, o in hang])

    ra = doc_chup(conn, cid)
    return ra


def ghi_chup_pm(conn, *, spreadsheet_id: str, actor: str, source_id: int,
                khai_version: int, giay: float | None = None) -> Chup:
    """Ảnh chụp lằn **`PM`** — **CHỈ dấu xuất xứ**, ⛔ KHÔNG một dòng nào.

    ⛔⛔⛔ **Vì sao lằn này ⛔ KHÔNG ghi vào `fls_chup_dong`, và đó là điều
       quan trọng nhất của cả hàm.**

    Docstring đầu tệp đặt một luật: *"ba bảng, và ⛔ KHÔNG một con số nào lưu
    hai lần"*. Với lằn `Bank`/`Cash`, `fls_chup_dong` là chỗ **duy nhất** giữ ô
    thô. Nhưng lằn `PM` **đã có bảng dòng của nó rồi**: `fls_pm_line` mang
    `run_id` · `read_at` · `source_row` — nó **CHÍNH LÀ** một ảnh chụp. Chép
    3.703 dòng ấy sang `fls_chup_dong` là lưu **cùng những con số** ở hai chỗ,
    và hai chỗ ấy **sẽ lệch**.

    ⇒ Nên ảnh chụp `PM` chở đúng bốn thứ mà `fls_pm_line` ⛔ **không** có:
      `doc_luc` *(ảnh già bao lâu)* · `actor` *(AI đọc)* · `giay` *(mất bao
      lâu)* · `spreadsheet_id` *(đọc workbook nào)*. Trước 09/09 lệnh chi vào
      kho bằng một lệnh dòng lệnh của Dev, nên **⛔ không thứ nào trong bốn thứ
      ấy tồn tại** — và ⛔ không cổng nào nói được rằng dữ liệu đã đóng băng
      **13 ngày**.

    ⚠ `fls_chup_nguon` **vẫn có một dòng**: luật ⓐ của `ghi_chup` *(⛔ không ghi
      một ảnh ⛔ không đọc nguồn nào)* đúng cả ở đây, và nó là chỗ ghi
      `khai_version` — câu trả lời cho *"ảnh này đọc theo bố trí cột NÀO"*
      *(`pm_join.PM_KHAI_VERSION`)*.

    ⭐ Và `so_dong` của lằn này được **ĐO từ `fls_pm_line`** *(xem `_dung`)*,
      ⛔ không lưu — nên nó ⛔ không thể nói dối.
    """
    if not str(spreadsheet_id or "").strip():
        raise LoiChup("⛔ thiếu `spreadsheet_id` — một ảnh chụp ⛔ không nói nó "
                      "đọc workbook NÀO thì ⛔ không đối chiếu được với gì")
    if not str(actor or "").strip():
        raise LoiChup("⛔ thiếu `actor` — chụp là một HÀNH VI, phải có tên")
    if int(khai_version) < 1:
        raise LoiChup("⛔ `khai_version` phải >= 1 — nó trả lời câu *'ảnh này "
                      "đọc theo bố trí cột nào'*, và `0` ⛔ không trả lời gì")

    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT source_id, src_type FROM fls_source"
                        " WHERE source_id = %s FOR SHARE", (source_id,))
            r = cur.fetchone()
            if r is None:
                raise LoiChup("⛔ ⛔ không có nguồn `source_id=%s` trong "
                              "`fls_source`" % source_id)
            if (r[1] or "").strip() != LAN_PM_SRC:
                raise LoiChup(
                    "⛔ nguồn `source_id=%s` có `src_type=%r`, ⛔ không phải "
                    "%r. Chụp lằn `PM` vào một nguồn sao kê là trộn hai lằn "
                    "khác khuôn RA (`GAP-CANON-02`)"
                    % (source_id, r[1], LAN_PM_SRC))

            cur.execute(
                "INSERT INTO fls_chup (spreadsheet_id, lan, giay, actor)"
                " VALUES (%s, 'PM', %s, %s) RETURNING chup_id",
                (spreadsheet_id, giay, actor))
            cid = cur.fetchone()[0]
            cur.execute(
                "INSERT INTO fls_chup_nguon (chup_id, source_id, khai_version)"
                " VALUES (%s, %s, %s)", (cid, source_id, int(khai_version)))
    return doc_chup(conn, cid)


# ── ĐỌC ───────────────────────────────────────────────────────────────────
_DAU = ("chup_id", "doc_luc", "spreadsheet_id", "lan", "giay", "actor")

# ⭐ `src_type` của nguồn lằn `PM`. Cùng khuôn với `Mapping` — một *"nguồn"*
#   ⛔ không phải sao kê. Xem `fls/db/schema.py::_FLS_SOURCE`.
LAN_PM_SRC = "PM"

# ⛔⛔ Câu ĐO số dòng của một ảnh lằn `PM`. Nó đi qua `fls_run.chup_id` — sợi
#    dây lineage — nên nó chỉ trả về số dòng của **đúng lần nạp dùng ảnh này**.
#
# ⚠ `LEFT JOIN` + `count(l.pm_line_id)`: một ảnh **đã chụp mà ⛔ chưa nạp** phải
#   hiện `so_dong = 0`, ⛔ không biến mất. Cùng lý lẽ với `LEFT JOIN` ở `_dung`.
_SQL_SO_DONG_PM = """
SELECT count(l.pm_line_id)
  FROM fls_run r
  LEFT JOIN fls_pm_line l ON l.run_id = r.run_id
 WHERE r.chup_id = %s
"""


def _dung(conn, dau: Sequence[Any]) -> Chup:
    with conn.cursor() as cur:
        # ⭐⭐ `LEFT JOIN` + `count(d.dong_so)`, ⛔ KHÔNG `INNER JOIN`: nguồn
        #    đọc ra **0 dòng** phải hiện ra với `so_dong = 0`, ⛔ không biến
        #    mất. Đây là toàn bộ lý do `fls_chup_nguon` tồn tại.
        cur.execute(
            "SELECT n.source_id, s.source_key, n.khai_version,"
            "       count(d.dong_so) AS so_dong"
            "  FROM fls_chup_nguon n"
            "  JOIN fls_source s ON s.source_id = n.source_id"
            "  LEFT JOIN fls_chup_dong d"
            "         ON d.chup_id = n.chup_id AND d.source_id = n.source_id"
            " WHERE n.chup_id = %s"
            " GROUP BY n.source_id, s.source_key, n.khai_version"
            " ORDER BY s.source_key", (dau[0],))
        ng = tuple(NguonTrongChup(source_id=r[0], source_key=r[1],
                                  khai_version=r[2], so_dong=int(r[3]))
                   for r in cur.fetchall())

        # ⭐⭐ Lằn `PM`: `so_dong` **ĐO từ `fls_pm_line`**, ⛔ không từ
        #    `fls_chup_dong` *(lằn ấy ⛔ không ghi vào đó — xem `ghi_chup_pm`)*.
        #
        # ⛔⛔ Thiếu đoạn này thì một ảnh `PM` đã nạp **3.703 dòng** sẽ báo
        #    `so_dong = 0`, và `F04` hiện nó như *"đã đọc lúc 15:02 · 0 dòng"*
        #    — đúng lời nói dối mà docstring đầu tệp dựng ra để chặn, chỉ theo
        #    **chiều ngược lại**: ở kia là một con số lưu sẵn nói quá, ở đây là
        #    một phép đo **đo sai bảng** nên nói thiếu.
        if dau[3] == "PM" and ng:
            cur.execute(_SQL_SO_DONG_PM, (dau[0],))
            n = int(cur.fetchone()[0])
            ng = (NguonTrongChup(source_id=ng[0].source_id,
                                 source_key=ng[0].source_key,
                                 khai_version=ng[0].khai_version,
                                 so_dong=n),)
    return Chup(chup_id=dau[0], doc_luc=dau[1], spreadsheet_id=dau[2],
                lan=dau[3], giay=float(dau[4]) if dau[4] is not None else None,
                actor=dau[5], nguon=ng)


def doc_chup(conn, chup_id: int) -> Chup:
    """Một ảnh chụp. ⛔ **NỔ** nếu ⛔ không có — ⛔ không trả một vỏ rỗng.

    ⛔ *"⛔ Không có ảnh chụp `7`"* và *"ảnh chụp `7` đọc được 0 dòng"* là **hai
      câu khác nhau**, và chúng dẫn người dùng đi **hai đường sửa khác nhau**.
      Trả `None` cho cả hai là gộp chúng lại.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT %s FROM fls_chup WHERE chup_id = %%s"
                    % ", ".join(_DAU), (chup_id,))
        r = cur.fetchone()
    if r is None:
        raise KhongCoChup("⛔ ⛔ không có ảnh chụp `chup_id=%s`" % chup_id)
    return _dung(conn, r)


def moi_nhat(conn, lan: str) -> Chup | None:
    """Ảnh chụp **mới nhất** của một lằn. `None` = ⛔ chưa chụp lần nào."""
    if lan not in LAN:
        raise LoiChup("⛔ `lan=%r` lạ — chỉ %s" % (lan, list(LAN)))
    with conn.cursor() as cur:
        cur.execute("SELECT %s FROM fls_chup WHERE lan = %%s"
                    " ORDER BY doc_luc DESC, chup_id DESC LIMIT 1"
                    % ", ".join(_DAU), (lan,))
        r = cur.fetchone()
    return None if r is None else _dung(conn, r)


def liet_ke(conn, *, lan: str | None = None, gioi_han: int = 50) -> list[Chup]:
    """Danh sách ảnh chụp, **mới nhất trước**."""
    if lan is not None and lan not in LAN:
        raise LoiChup("⛔ `lan=%r` lạ — chỉ %s" % (lan, list(LAN)))
    with conn.cursor() as cur:
        cur.execute(
            "SELECT %s FROM fls_chup"
            " WHERE (%%s::text IS NULL OR lan = %%s::text)"
            " ORDER BY doc_luc DESC, chup_id DESC LIMIT %%s"
            % ", ".join(_DAU), (lan, lan, max(1, min(int(gioi_han), 500))))
        dau = cur.fetchall()
    return [_dung(conn, r) for r in dau]


def doc_dong(conn, chup_id: int, *, source_id: int | None = None,
             gioi_han: int | None = None
             ) -> list[tuple[int, int, dict[str, Any]]]:
    """`[(source_id, dong_so, ô)]` theo thứ tự. ⛔ **NỔ** nếu ⛔ không có ảnh.

    ⭐ Thứ tự `(source_id, dong_so)` là **thứ tự đã đọc**, và nó phải giữ
      nguyên: luật `Num` của AS-IS là *"thứ tự lần xuất hiện của mã"*
      *(đo **8.331/8.331 = 100,0%**)* ⇒ đọc lại theo thứ tự khác là **đổi
      `Num`**, tức làm sai một cột mà FLS đã chứng minh là dựng đúng.
    """
    doc_chup(conn, chup_id)          # ⛔ NỔ trước, đừng trả `[]` cho ảnh ⛔ không có
    with conn.cursor() as cur:
        cur.execute(
            "SELECT source_id, dong_so, o FROM fls_chup_dong"
            # ⚠ `::bigint` ⛔ KHÔNG phải trang trí: một `NULL` trần ở vế `IS
            #   NULL` làm PostgreSQL ⛔ không suy được kiểu tham số ⇒ nổ
            #   `IndeterminateDatatype`. Đã cắn thật lúc chạy thử đầu tiên.
            " WHERE chup_id = %s AND (%s::bigint IS NULL"
            "                          OR source_id = %s::bigint)"
            " ORDER BY source_id, dong_so"
            + (" LIMIT %s" if gioi_han is not None else ""),
            (chup_id, source_id, source_id)
            + ((max(0, int(gioi_han)),) if gioi_han is not None else ()))
        return [(r[0], r[1], r[2]) for r in cur.fetchall()]


def doc_o_ngay(conn, chup_id: int) -> dict[int, list[Any]]:
    """`{source_id: [giá trị ô ngày, …]}` — **TOÀN BỘ** dòng, ⛔ không giới hạn.

    ⭐⭐ **Vì sao một hàm riêng chứ ⛔ không dùng `doc_dong()`.** Phép đo bằng
       chứng thứ tự ngày *(`QĐ-ITL-113`)* phải soi **mọi dòng**: nguồn nặng
       nhất đo được có **905** dòng mơ hồ trong **2.168** dòng, và bằng chứng
       quyết định *(dòng có phần > 12)* có thể nằm ở **dòng cuối**. Còn
       `doc_dong()` thì **mặc định 50 dòng** và trần 500 — đúng cho một lưới
       xem trước, và **sai hoàn toàn** cho một phép đo.

    ⛔⛔ Và đây đúng lớp lỗi *"xanh vì chưa đo hết"*: một bằng chứng tính trên
       50 dòng đầu sẽ **im lặng đề xuất sai** cho một nguồn mà 50 dòng đầu
       toàn mơ hồ — mà 29/29 nguồn thật đều có ít nhất một dòng mơ hồ.

    ⭐ Chỉ rút **một khoá** trong `jsonb` (`o -> 'Date'`), ⛔ không chở cả 6
      trường của 8.368 dòng về Python cho một phép đếm.
    """
    doc_chup(conn, chup_id)          # ⛔ NỔ trước, đừng trả `{}` cho ảnh ⛔ không có
    ra: dict[int, list[Any]] = {}
    with conn.cursor() as cur:
        # ⛔ `o -> %s` giữ NGUYÊN KIỂU (số vẫn là số) — `->>` sẽ hạ mọi thứ về
        #    chuỗi, và lúc ấy **4.175 ô seri** biến thành `"45586"` ⇒ phép đo
        #    sẽ báo *"⛔ không có ô số nào"*. Đúng cái bẫy `doc_cot` đã cắn.
        cur.execute(
            "SELECT source_id, o -> %s FROM fls_chup_dong"
            " WHERE chup_id = %s ORDER BY source_id, dong_so",
            (TRUONG_NGAY, chup_id))
        for sid, v in cur.fetchall():
            ra.setdefault(sid, []).append(v)
    return ra
