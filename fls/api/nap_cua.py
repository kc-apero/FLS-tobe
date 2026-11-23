# -*- coding: utf-8 -*-
"""Nhóm **NẠP** — ba tuyến của `BA-07` §4b *(`CR#11` task `4`)*.

⛔⛔ **Trước hôm nay nhóm này ⛔ KHÔNG TỒN TẠI.** Đo được: **0/17** tuyến là cửa
   nạp — 8 `GET` + 9 `POST`, và **mọi `POST` đều SỬA một dòng ĐÃ CÓ**. Đường duy
   nhất đưa dữ liệu vào kho là `tools/nap_that.py`, **một lệnh dòng lệnh đọc
   Google Sheets**. ⇒ Bỏ Google Sheets mà ⛔ không dựng nhóm này thì **⛔ không
   còn đường nào vào**.

★ **Ba tuyến, và một đường ống dùng lại TOÀN BỘ những gì đã dựng:**

    ① ghi bản khai   →  `repo.khai_cot.ghi_khai`      *(task `2`)*
    ② xem trước      →  đọc khai → `sao_ke.chuyen` → 7 luật → **⛔ KHÔNG GHI**
    ③ nạp            →  y hệt ②, rồi `repo.nap_lo`   *(task `5`)*

⭐⭐ **Vì sao XEM TRƯỚC là một TUYẾN RIÊNG, ⛔ không phải một cờ** *(`BA-07` §4b
   ⓶)*: hai việc **khác nhau về HẬU QUẢ** thì ⛔ không được khác nhau bằng **một
   chữ trong thân yêu cầu**. Một cờ `?that=true` gõ thiếu là **ghi thật khi định
   thử**. Hai đường riêng thì gõ nhầm đường **⛔ không mất gì** — nó chỉ soát.

⛔⛔ **Luật `S8` ở đường này được cưỡng chế bằng CHÍNH CÁI CỬA, ⛔ không phải bị
   bỏ.** `S8` hỏi *"nguồn đang nạp có trong danh mục ⛔ không?"*. Ở đường HTTP,
   nguồn **là** `source_id` của `fls_source` — ⛔ không có thì cửa trả **404
   `FLS-NGUON-LA`** và ⛔ **không có gì để nạp**. ⇒ Biên bản khai thẳng điều ấy
   *(`s8_o_cua`)*, ⛔ **không** bịa một luật đỏ giả — một luật `da_do=0` đỏ
   thường trực sẽ **cắm cờ lên MỌI dòng của MỌI lô**, và từ đó hàng chờ thành
   rác *(đúng điều `QĐ-ITL-71` cảnh báo)*.

⚠ **Thân yêu cầu mang DÒNG ĐÃ TÁCH, ⛔ không mang tệp.** Đọc `.xlsx`/`.csv` là
  việc của **màn hình** *(nó đã cầm tệp trong tay người dùng)*; nhét một bộ
  giải mã tệp vào tầng cửa là mở một bề mặt tấn công mới cho một việc ⛔ không
  ai đòi. ⇒ Cửa nhận `{"dong": [[...], ...]}`.
"""
from __future__ import annotations

from typing import Any, NamedTuple, Sequence

from fls.adapters.sao_ke import (KHAI_ANH_CHUP, BanKhaiHong, chuyen,
                                 hang_tu_o)
from fls.api.xu_ly import LoiCua, YeuCau, _bat_buoc_int, _chu
from fls.kiem import soat_nap as sn
from fls.kiem import thu_tu_ngay as ttn
from fls.ledger.build import NgucCanh
from fls.repo import anh_pm, chup
from fls.repo import khai_cot as kc
from fls.repo import nap_lo as nl
from fls.repo import nguon_dai as nd


def than_co(than: dict[str, Any], khoa: str) -> bool:
    """⭐ *"Có khoá ấy"*, ⛔ **KHÔNG** phải *"khoá ấy có giá trị thật"*.

    ⛔⛔ Dùng `than.get(khoa)` ở đây là một lỗi im lặng: `{"dong": []}` là một
       yêu cầu **hợp lệ và có nghĩa** *(một lô rỗng)*, mà `[]` thì **falsy** ⇒
       nó sẽ bị đọc thành *"⛔ không đưa `dong`"* và trả về một thông báo nói
       người dùng thiếu thứ họ **đã đưa**.
    """
    return khoa in than


# ⛔ Trần thân yêu cầu — ⛔ không để một lô vô hạn kéo sập máy.
TRAN_DONG = 50_000


def _nguon(conn, source_id: int) -> str:
    """`source_key` của một nguồn. ⛔ Không có nguồn ⇒ **404**, ⛔ không 409."""
    with conn.cursor() as cur:
        cur.execute("SELECT source_key FROM fls_source WHERE source_id = %s",
                    (source_id,))
        r = cur.fetchone()
    if r is None:
        raise LoiCua("FLS-NGUON-LA",
                     "⛔ ⛔ không có nguồn `source_id=%s`" % source_id)
    return r[0]


def _dong_cua_than(than: dict[str, Any]) -> list[Sequence[Any]]:
    d = than.get("dong")
    if not isinstance(d, list):
        raise LoiCua("FLS-BAD-REQUEST",
                     "thân yêu cầu phải có `dong` là một danh sách các dòng")
    return _tran(d)


def _tran(d: list) -> list[Sequence[Any]]:
    if len(d) > TRAN_DONG:
        raise LoiCua("FLS-TOO-LARGE",
                     "lô %d dòng, trần %d" % (len(d), TRAN_DONG))
    for i, h in enumerate(d):
        if not isinstance(h, list):
            raise LoiCua("FLS-BAD-REQUEST",
                         "dòng %d ⛔ không phải một danh sách ô" % (i + 1))
    return d


def s8_o_cua(khoa: str) -> sn.KetQuaSoat:
    """`S8` ở đường HTTP — **CỬA đã cưỡng chế**, ⛔ không phải bỏ qua.

    ⛔ Khai ra thành **một dòng của biên bản**, để màn hình hiện đủ **8** luật.
    Giấu nó đi thì biên bản còn 7 dòng và ⛔ không ai biết dòng thứ 8 đâu.
    """
    return sn.KetQuaSoat(
        ten="S8 · xuất xứ có trong danh mục", hang=sn.CO_, dat=True, da_do=1,
        thong_diep="cửa đã cưỡng chế: `%s` có trong `fls_source`, "
                   "⛔ không có thì tuyến trả 404 và ⛔ không nạp gì" % khoa)


def s10_o_cua(khoa: str, khai: dict[str, int],
              dai: "nd.BanDai | None") -> sn.KetQuaSoat:
    """`S10` cho **một** nguồn — hai bản khai của chính nguồn đang nạp.

    ⛔⛔ **Chưa thu dải thì phải nói THẲNG là CHƯA ĐO, ⛔ không im.** Một biên
       bản có 8 dòng xanh và **thiếu hẳn dòng thứ 9** đọc y hệt một biên bản
       ⛔ không có luật ấy — và người đọc ⛔ không có cách nào biết.

    ⚠ Ở cửa này `S10` chỉ so được **một** nguồn. Phép so **cả 68 nguồn** là
      việc của `tools/nap_nguon_dai.py`, và nó bắt được thứ cửa ⛔ không thấy:
      một nguồn **⛔ chưa ai nạp lần nào** vẫn có thể đã lệch hai bản khai.
    """
    if dai is None:
        return sn.KetQuaSoat(
            "S10 · hai ban khai tro CUNG mot cot", sn.CHAN, False, 0,
            "⛔ ⛔ chua thu dai doc cua `%s` — chay "
            "`tools/nap_nguon_dai.py --that`" % khoa)
    return sn.s10_hai_ban_khai_cung_cot({khoa: khai}, {khoa: dai.cot})


def _soat(khoa: str, ra: list[list], thong_ke,
          s10: sn.KetQuaSoat) -> list[sn.KetQuaSoat]:
    """Bảy luật đo được trên một lô + `S8` và `S10` do cửa cưỡng chế."""
    theo = {khoa: (thong_ke.vao, thong_ke.ra, thong_ke.rong, thong_ke.loi)}
    return [
        sn.s1_ba_duong_can(theo),
        sn.s2_co_tien_thi_phai_co_ma(ra),
        sn.s3_moi_dong_phai_co_tien(ra),
        sn.s4_moi_dong_phai_co_tien_te(ra),
        sn.s5_ma_khong_bi_ha_kieu(ra),
        sn.s6_mot_sheet_mot_kieu_ngay(ra),
        sn.s7_dong_trung_hoan_toan(ra),
        s8_o_cua(khoa),
        s10,
    ]


def _bien_ban(luat: Sequence[sn.KetQuaSoat], thong_ke) -> dict[str, Any]:
    """Khuôn biên bản của `BA-07` §4b ⓷.

    ⛔⛔ **`da_do` ⛔ KHÔNG được vắng mặt.** Luật nền của cả hai cổng: **đo được
    `0` thứ ⇒ ⛔ KHÔNG ĐẠT**. Một biên bản chỉ nói *"đạt"* mà ⛔ không nói **đã
    đo bao nhiêu** là một biên bản **⛔ không đọc được**.
    """
    chan = sn.chan_lai(luat)
    return {
        "so_dong_vao": thong_ke.vao,
        "so_dong_ra": thong_ke.ra,
        "rong": thong_ke.rong,
        "loi": thong_ke.loi,
        "luat": [{"ten": k.ten, "hang": k.hang, "dat": k.dat,
                  "da_do": k.da_do, "thong_diep": k.thong_diep}
                 for k in luat],
        "chan": [k.ten for k in chan],
        "co": [k.ten for k in luat if not k.xanh and k not in chan],
    }


def _hang_dua_vao(yc: YeuCau, source_id: int, khai: kc.BanKhai
                  ) -> tuple[list, dict[str, int]]:
    """⭐⭐⭐ `chup_id` **XOR** `dong` — hai đường vào, chỉ MỘT là đường thật.

    ⛔⛔ **Cả hai, hay ⛔ không cái nào ⇒ 400.** ⛔ Không có mặc định *"⛔ không
       nói thì lấy ảnh chụp mới nhất"*: một lô tiền nạp vào **ảnh chụp nào**
       ⛔ không được là thứ máy tự đoán — đoán đúng 59 lần rồi sai lần thứ 60
       là nạp lại **dữ liệu của hôm khác**.

    | Khoá | Vai |
    |---|---|
    | `chup_id` | ⭐ **đường THẬT** — đường màn `F04` đi *(`QĐ-ITL-110`)* |
    | `dong` | ⛔ **CHỈ** cho test và phép đo đối chứng, ⛔ **không** phải một
                đường vận hành *(cùng lời khai với `nap_sao_ke.nap(khai_theo=)`)*.
                Nó ở lại vì **31 bài test hiện hành** chứng minh 9 luật soát đi
                qua nó — vứt nó là vứt phép chứng minh |

    ⭐ Trả về cả **bản khai đã dùng**, vì hai đường đọc **hai khuôn khác nhau**:
      `dong` mang dòng theo bản khai **CỦA NGUỒN**; ảnh chụp mang ô theo **tên
      trường** nên đọc bằng `sao_ke.KHAI_ANH_CHUP`.
    """
    co_chup = than_co(yc.than, "chup_id")
    co_dong = than_co(yc.than, "dong")
    if co_chup and co_dong:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "thân yêu cầu mang CẢ `chup_id` LẪN `dong` — ⛔ không được: hai "
            "đường vào cho cùng một lô là hai chỗ để chúng lệch nhau, và biên "
            "bản sẽ nói về thứ ⛔ không phải thứ được ghi. Chọn MỘT.")
    if not co_chup and not co_dong:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "thân yêu cầu phải có `chup_id` (đường thật — `QĐ-ITL-110`) HAY "
            "`dong` (⛔ chỉ dùng cho test/đối chứng). ⛔ ⛔ Không có mặc định: "
            "máy ⛔ không tự chọn ảnh chụp cho một lô tiền.")

    if co_dong:
        return _dong_cua_than(yc.than), khai.cot

    cid = _bat_buoc_int(yc.than, "chup_id")
    try:
        anh = chup.doc_chup(yc.conn, cid)
    except chup.KhongCoChup as e:
        raise LoiCua("FLS-CHUP-KHONG-CO", str(e)) from e

    trong = {n.source_id: n for n in anh.nguon}
    if source_id not in trong:
        # ⛔ **409, ⛔ KHÔNG 404** — cùng luật `FLS-KHAI-KHONG-CO`: ảnh chụp
        #   **có**, nguồn **có**, chỉ là ảnh ấy ⛔ không hề đọc nguồn này.
        raise LoiCua(
            "FLS-CHUP-KHONG-NGUON",
            "ảnh chụp `%d` ⛔ KHÔNG đọc nguồn `source_id=%d` — nó đọc %d nguồn "
            "khác. Chụp lại rồi nạp, ⛔ đừng nạp từ một ảnh ⛔ không có nguồn ấy"
            % (cid, source_id, anh.so_nguon))

    # ⚠ **Khai của ảnh chụp ⛔ có thể KHÁC khai hiện hiệu lực** — và đó là
    #   chuyện BÌNH THƯỜNG, ⛔ không phải lỗi: ảnh chụp tuần trước đọc bằng
    #   `v1`, hôm nay nguồn đã lên `v2`. ⇒ Khai ra trong biên bản chứ ⛔ không
    #   chặn, và ⛔ không lặng lẽ áp `v2` lên dữ liệu đọc bằng `v1`.
    hang = [hang_tu_o(o) for _s, _d, o in
            chup.doc_dong(yc.conn, cid, source_id=source_id)]
    return _tran(hang), KHAI_ANH_CHUP


def _khai_anh(yc: YeuCau, source_id: int) -> tuple[int, int] | None:
    """`(chup_id, khai_version)` của ảnh đang nạp — `None` nếu đi đường `dong`."""
    if not than_co(yc.than, "chup_id"):
        return None
    cid = _bat_buoc_int(yc.than, "chup_id")
    anh = chup.doc_chup(yc.conn, cid)
    for n in anh.nguon:
        if n.source_id == source_id:
            return cid, n.khai_version
    return None


def _dung_lo(yc: YeuCau) -> tuple[str, list[list], Any,
                                  list[sn.KetQuaSoat], kc.BanKhai]:
    """Đọc khai → dựng lô → soát. **Dùng chung** cho xem-trước và nạp.

    ⭐ Chính vì dùng chung mà câu *"xem trước cho ra đúng thứ nạp sẽ ghi"* là
      **thật**, ⛔ không phải một lời hứa. Hai đường tính riêng là hai chỗ để
      chúng lệch nhau — và người dùng sẽ tin cái họ vừa nhìn thấy.
    """
    sid = _bat_buoc_int(yc.than, "source_id")
    khoa = _nguon(yc.conn, sid)
    try:
        khai = kc.doc_khai(yc.conn, sid)
    except kc.KhongCoKhai as e:
        # ⚠ **409, ⛔ KHÔNG 404**: nguồn **có tồn tại**, chỉ là ⛔ chưa ai khai
        #    cách đọc nó. Hai câu trả lời dẫn người dùng đi **hai đường sửa
        #    khác nhau** (`BA-07` §4b ⓺).
        raise LoiCua("FLS-KHAI-KHONG-CO", str(e)) from e

    hang, khai_dung = _hang_dua_vao(yc, sid, khai)
    try:
        ra, tk = chuyen(khoa, khai_dung, hang)
    except BanKhaiHong as e:
        raise LoiCua("FLS-KHAI-THIEU", str(e)) from e

    # ⭐ Bản khai THỨ HAI (`GAP-KHAI-01`). ⛔ Chưa thu ⇒ `S10` báo **chưa đo**,
    #   ⛔ không phải vắng mặt khỏi biên bản.
    s10 = s10_o_cua(khoa, khai.cot, nd.doc_dai(yc.conn, sid))
    # ⭐ Trả CẢ `khai` — `nap` cần `khai.thu_tu` để dựng `NgucCanh`
    #   *(`QĐ-ITL-113`)*. ⛔ Đọc bản khai **lần thứ hai** ở `nap` là mở đường
    #   cho xem-trước và nạp đọc **hai bản khai khác nhau** *(một cú khai chen
    #   vào giữa)* — tức phá đúng lời hứa mà hàm này tồn tại để giữ.
    return khoa, ra, tk, _soat(khoa, ra, tk, s10), khai


# ─────────────────────────────────────────────────────────── ① ghi bản khai
def ghi_khai(yc: YeuCau):
    """Ghi **bản khai ánh xạ cột** — sinh `version` MỚI, ⛔ không sửa khai cũ."""
    sid = _bat_buoc_int(yc.tham, "source_id")
    cot = yc.than.get("cot")
    if not isinstance(cot, dict):
        raise LoiCua("FLS-BAD-REQUEST",
                     "thân yêu cầu phải có `cot` = {tên trường: chỉ số cột}")
    # ⭐⭐ `thu_tu` *(`QĐ-ITL-113`)* — **tuỳ chọn**, ⛔ nhưng ⛔ KHÔNG được
    #    lặng lẽ bỏ qua nếu sai. Kế toán bấm khai `dmy`, cửa ghi `NULL`, và
    #    ngày mơ hồ vẫn bị loại — mà trên màn thì **trông như đã khai xong**.
    #    ⇒ Có mặt mà lạ ⇒ **400**, ⛔ không `None` hoá.
    tt = yc.than.get("thu_tu")
    if than_co(yc.than, "thu_tu") and tt is not None:
        if not isinstance(tt, str) or tt not in kc.THU_TU_HOP_LE:
            raise LoiCua(
                "FLS-BAD-REQUEST",
                "`thu_tu=%r` ⛔ không hợp lệ — chỉ %s"
                % (tt, " hoặc ".join("`%s`" % x for x in kc.THU_TU_HOP_LE)))
    try:
        b = kc.ghi_khai(yc.conn, sid, cot, actor=yc.actor, thu_tu=tt)
    except kc.NguonLa as e:
        raise LoiCua("FLS-NGUON-LA", str(e)) from e
    except kc.LoiKhai as e:
        raise LoiCua("FLS-KHAI-THIEU", str(e)) from e
    return {"source_id": b.source_id, "version": b.version, "cot": b.cot,
            "thu_tu": b.thu_tu,
            "hieu_luc_tu": b.hieu_luc_tu, "actor": b.actor}, "flash"


# ───────────────────────────────────────────────────────────── ② xem trước
def xem_truoc(yc: YeuCau):
    """⭐ SOÁT mà ⛔ **KHÔNG GHI**. Tuyến này ⛔ không chạm một bảng ghi nào."""
    khoa, ra, tk, luat, khai = _dung_lo(yc)
    bb = _bien_ban(luat, tk)
    bb["nguon"] = khoa
    bb["se_ghi"] = not bb["chan"]
    # ⛔ Bien ban phai NOI RA no doc ngay bang thu tu nao. Mot bien ban im ve
    #    dieu do la mot bien ban ⛔ khong giai thich duoc vi sao 1.894 dong
    #    hoac vao so hoac bi loai.
    bb["thu_tu"] = khai.thu_tu
    return bb, "flash"


# ────────────────────────────────────────────────────────────────── ③ nạp
def nap(yc: YeuCau):
    """Nạp thật → `run_id` + **CÙNG một biên bản** với xem trước."""
    khoa, ra, tk, luat, khai = _dung_lo(yc)
    sid = _bat_buoc_int(yc.than, "source_id")
    anh = _khai_anh(yc, sid)
    # ⭐⭐ LINEAGE ghi thật — ⛔ không để một cột dựng ra rồi ⛔ không ai ghi.
    nc = NgucCanh(run_id=_chu(yc.than, "run_id"),
                  contract_version="v1.1", canon_version="v1.0",
                  mapping_version="v1.0",
                  source_system="P100", source_sheet=khoa,
                  chup_id=anh[0] if anh else None,
                  # ⭐⭐ `QĐ-ITL-113` — thu tu ngay do NGUON khai. `None` =
                  #    nguon chua khai ⇒ ngay mo ho VAN bi loai kem ly do,
                  #    ⛔ KHONG mac dinh `dmy`: do duoc 29/29 nguon la `mdy`.
                  thu_tu=khai.thu_tu)
    try:
        kq = nl.nap_lo(yc.conn, ra, nc, luat, actor=yc.actor)
    except nl.LoBiChan as e:
        # ⛔ **422** + biên bản ĐẦY ĐỦ đi kèm: nói *"bị chặn"* mà ⛔ không nói
        #    **chặn vì luật nào** là bắt người dùng đoán.
        raise LoiCua("FLS-SOAT-CHAN", str(e),
                     bien_ban=_bien_ban(luat, tk)) from e
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e

    bb = _bien_ban(luat, tk)
    bb.update({"nguon": khoa, "run_id": kq.nap.run_id,
               "vao_so": kq.nap.vao_so, "trung": kq.nap.bo_qua_trung,
               "loai": kq.nap.loai, "unmapped": kq.nap.unmapped,
               "vao_hang_cho": kq.vao_hang_cho})
    return bb, "flash"


# ─────────────────────────────────────────── ④ danh sách NGUỒN — trạng thái ①
def nguon_ds(yc: YeuCau):
    """**68 nguồn** + bản khai hiện hiệu lực + lần chụp cuối *(`QĐ-ITL-110`)*.

    ⛔⛔ **Trước 08/09 cửa này ⛔ KHÔNG TỒN TẠI**, và đó là chỗ `BA-06` §7 ①
       *("danh sách 68 nguồn, mặc định tick tất cả")* **⛔ không dựng được**.
       Không có nó thì màn phải **gõ tay 68 tên nguồn** — đúng thứ cổng #15
       `kiem_bang_cot` bắt ĐỎ *("tên cột phải truy được về nguồn; gõ tay đè lên
       nguồn thì ĐỎ")*.

    ⭐ `khai_version = null` là một **CÂU TRẢ LỜI**, ⛔ không phải thiếu dữ
      liệu: *"nguồn này ⛔ chưa ai khai cách đọc"* ⇒ màn phải hiện `—`, và nút
      `Soát` của nguồn ấy **tắt** *(`BA-06` §7 ⓷)*.

    ⛔ **⛔ KHÔNG có trạng thái `InActive`/`Closed`** — `fls_source` ⛔ không có
       cột ấy. `Account Status` *(`Closed` 10 · `InActive` 5)* chỉ sống ở sheet
       AS-IS. ⇒ `GAP-CHUP-02`, và cửa này **khai thẳng** bằng khoá
       `trang_thai_nguon: null` chứ ⛔ không im lặng bỏ trường — im lặng thì
       màn hình sẽ tưởng mọi nguồn đều `Active`.
    """
    with yc.conn.cursor() as cur:
        cur.execute(
            "SELECT s.source_id, s.source_key, s.src_type, s.last_seen_at,"
            "       s.lag_days, s.cutoff_date, s.txn_count,"
            "       k.version, c.doc_luc"
            "  FROM fls_source s"
            # ⭐ `version` LON NHAT — dung dinh nghia `doc_khai` dung
            #   (*"ban khai hieu luc"*), ⛔ khong phai dong ghi sau cung.
            "  LEFT JOIN (SELECT source_id, max(version) AS version"
            "               FROM fls_khai_cot GROUP BY source_id) k"
            "         ON k.source_id = s.source_id"
            # ⭐⭐ `LEFT JOIN`, ⛔ KHONG `INNER`: mot nguon **chua he duoc chup**
            #    phai co mat voi `chup_cuoi = null`. Loc no ra la lam *"chua
            #    chup"* va *"khong ton tai"* trong giong nhau.
            "  LEFT JOIN (SELECT n.source_id, max(h.doc_luc) AS doc_luc"
            "               FROM fls_chup_nguon n"
            "               JOIN fls_chup h ON h.chup_id = n.chup_id"
            "              GROUP BY n.source_id) c"
            "         ON c.source_id = s.source_id"
            " ORDER BY s.source_key")
        hang = cur.fetchall()
    return {"nguon": [{"source_id": r[0], "source_key": r[1],
                       "src_type": r[2],
                       "last_seen_at": r[3], "lag_days": r[4],
                       "cutoff_date": r[5], "txn_count": r[6],
                       "khai_version": r[7],
                       "chup_cuoi": r[8],
                       # ⛔ `GAP-CHUP-02` — khai thang chu ⛔ khong im lang.
                       "trang_thai_nguon": None}
                      for r in hang],
            "so_nguon": len(hang),
            "gap_trang_thai": "GAP-CHUP-02"}, "flash"


# ─────────────────────────────────────── ④ BẢN KHAI để XEM — trạng thái ③
def khai_cua_nguon(yc: YeuCau):
    """Bản khai **hiện hiệu lực** + **cả dãy `version`** của một nguồn.

    ⭐ `BA-06` §7 ⓷ đòi *"ánh xạ trường → cột kèm `version` · người khai · mốc
      hiệu lực"*, và ⓶b nói rõ đây là **để XEM**, ⛔ không để sửa. Cửa này chỉ
      đọc; đường sửa vẫn là `POST …/khai-cot` *(sinh `version` mới)*.

    ⛔ Trả **cả dãy**, ⛔ không chỉ bản mới nhất: câu *"vì sao dòng nạp tháng
       trước đọc cột khác"* chỉ trả lời được nếu thấy được **các bản cũ**.
    """
    sid = _bat_buoc_int(yc.tham, "source_id")
    khoa = _nguon(yc.conn, sid)
    with yc.conn.cursor() as cur:
        cur.execute(
            "SELECT version, truong, cot, hieu_luc_tu, actor, thu_tu"
            "  FROM fls_khai_cot WHERE source_id = %s"
            " ORDER BY version DESC, truong", (sid,))
        hang = cur.fetchall()
    if not hang:
        # ⚠ **409, ⛔ KHÔNG 404** — nguồn **có**, chỉ là ⛔ chưa ai khai cách
        #   đọc nó. Cùng luật `_dung_lo` (`BA-07` §4b ⓺).
        raise LoiCua("FLS-KHAI-KHONG-CO",
                     "nguồn `%s` (`source_id=%d`) ⛔ chưa có bản khai nào"
                     % (khoa, sid))
    ban: dict[int, dict] = {}
    for v, truong, cot, tu, actor, thu_tu in hang:
        b = ban.setdefault(v, {"version": v, "cot": {}, "hieu_luc_tu": tu,
                               "actor": actor, "thu_tu": None})
        b["cot"][truong] = cot
        # ⛔ `thu_tu` chi dau tren dong `Date` ⇒ lay TU DUNG dong ay. Mot phep
        #    `or` cho moi dong se vot len bat ky gia tri lac cho — tuc **che
        #    mat** dung khuyet tat ma `fls_khai_cot_thu_tu_ck` dung ra de chan.
        if truong == kc.TRUONG_MANG_THU_TU:
            b["thu_tu"] = thu_tu
    day = [ban[v] for v in sorted(ban, reverse=True)]
    return {"source_id": sid, "source_key": khoa,
            "hieu_luc": day[0], "dai_version": day}, "flash"


# ─────────────────────────────────────── ④ ẢNH CHỤP — trạng thái ②
def _dau_anh(a: chup.Chup, dong=None) -> dict[str, Any]:
    ra = {"chup_id": a.chup_id, "doc_luc": a.doc_luc,
          "spreadsheet_id": a.spreadsheet_id, "lan": a.lan,
          "giay": a.giay, "actor": a.actor,
          # ⭐ Hai con số này **ĐẾM TỪ BẢNG DÒNG**, ⛔ không đọc một cột lưu
          #   sẵn — bảng đầu CỐ Ý ⛔ không giữ chúng (`BA-07` §4c ⓷).
          "so_nguon": a.so_nguon, "so_dong": a.so_dong,
          "nguon": [{"source_id": n.source_id, "source_key": n.source_key,
                     "khai_version": n.khai_version, "so_dong": n.so_dong}
                    for n in a.nguon]}
    if dong is not None:
        ra["dong"] = [{"source_id": s, "dong_so": d, "o": o}
                      for s, d, o in dong]
    return ra


def chup_ds(yc: YeuCau):
    """Danh sách ảnh chụp, **mới nhất trước**."""
    lan = (yc.q.get("lan") or "").strip() or None
    if lan is not None and lan not in chup.LAN:
        raise LoiCua("FLS-BAD-REQUEST",
                     "`lan=%r` lạ — chỉ %s" % (lan, list(chup.LAN)))
    ds = chup.liet_ke(yc.conn, lan=lan,
                      gioi_han=int(yc.q.get("limit") or 50))
    return {"chup": [_dau_anh(a) for a in ds], "so": len(ds)}, "flash"


def chup_mot(yc: YeuCau):
    """Một ảnh chụp: đầu + từng nguồn + `?limit` dòng đầu để **xem trước**.

    ⛔ `limit` **mặc định 50**, ⛔ không phải *"tất cả"*: một ảnh chụp có
       **8.365 dòng**, và trạng thái ② của `F04` chỉ cần **lưới xem trước**.
       Một cửa mặc định trả cả lô là một cửa sẽ được gọi nhầm một lần rồi
       không ai gọi nữa.
    """
    cid = _bat_buoc_int(yc.tham, "chup_id")
    try:
        a = chup.doc_chup(yc.conn, cid)
        gh = int(yc.q.get("limit") or 50)
        dong = chup.doc_dong(yc.conn, cid, gioi_han=max(0, min(gh, 500)))
    except chup.KhongCoChup as e:
        raise LoiCua("FLS-CHUP-KHONG-CO", str(e)) from e
    return _dau_anh(a, dong), "flash"


# ────────────────────── ⑦ BẰNG CHỨNG thứ tự ngày — `QĐ-ITL-113`
def thu_tu_ds(yc: YeuCau):
    """Bằng chứng thứ tự ngày của **từng nguồn** trong một ảnh chụp.

    ⛔⛔⛔ **Cửa này ⛔ KHÔNG QUYẾT ĐỊNH gì — nó ĐẾM.** `QĐ-ITL-113` đặt quyền
       ấn định kỳ kế toán **ở NGƯỜI**: máy **đề xuất kèm bằng chứng**, kế toán
       **bấm khai**. ⇒ Khoá trả về là `de_xuat`, ⛔ **không** phải `thu_tu`.

    ⭐ Và nó trả về **`cau`** — một câu **có con số**. Một cái nút kèm lời
      khuyên mà ⛔ không kèm phép đo là một cái nút sẽ được bấm mà ⛔ **không
      ai đọc**, và lúc ấy *"người ấn định"* chỉ còn là một câu trong tài liệu.

    ⛔ `can_khai` phân biệt hai thứ **⛔ không được lẫn**: *"nguồn này ⛔ chưa
       khai"* ≠ *"nguồn này **cần** khai"*. Đo được **21/50** nguồn toàn
       ngày-số ⇒ `thu_tu` của chúng **⛔ vô nghĩa**, và đòi kế toán khai là bắt
       họ trả lời một câu **⛔ không tồn tại**.
    """
    cid = _bat_buoc_int(yc.tham, "chup_id")
    try:
        a = chup.doc_chup(yc.conn, cid)
        theo = chup.doc_o_ngay(yc.conn, cid)
    except chup.KhongCoChup as e:
        raise LoiCua("FLS-CHUP-KHONG-CO", str(e)) from e

    # ⛔ `thu_tu` ĐÃ khai của từng nguồn — đọc **một** lượt, ⛔ không N+1.
    da_khai = _thu_tu_da_khai(yc.conn)

    ra = []
    for n in a.nguon:
        bc = ttn.do_mot_nguon(theo.get(n.source_id, []))
        ra.append({
            "source_id": n.source_id, "source_key": n.source_key,
            # ⭐ `da_khai` — thứ tự kế toán ĐÃ ấn định. `None` = ⛔ chưa khai.
            "da_khai": da_khai.get(n.source_id),
            "can_khai": bc.can_khai,
            "de_xuat": bc.de_xuat,
            "mau_thuan": bc.mau_thuan,
            "cau": ttn.cau_bang_chung(bc),
            # ⛔ Mọi ô của bằng chứng, **kể cả ô `0`** — cùng luật `da_do` của
            #    biên bản 9 luật: nói *"đề xuất `mdy`"* mà ⛔ không nói **đã
            #    soi bao nhiêu dòng** là một bằng chứng ⛔ không đọc được.
            "bang_chung": {"so_dong": bc.so_dong, "o_so": bc.o_so,
                           "o_chuoi": bc.o_chuoi, "chac_dmy": bc.chac_dmy,
                           "chac_mdy": bc.chac_mdy, "mo_ho": bc.mo_ho},
        })
    can = [x for x in ra if x["can_khai"]]
    return {"chup_id": a.chup_id, "doc_luc": a.doc_luc, "nguon": ra,
            "so_nguon": len(ra),
            "so_can_khai": len(can),
            # ⛔ Đếm *"cần khai mà CHƯA khai"* — con số kế toán thật sự phải
            #    hành động. `so_can_khai` một mình ⛔ không nói được điều đó:
            #    khai xong rồi thì nó **vẫn** là 29.
            "so_con_thieu": sum(1 for x in can if x["da_khai"] is None),
            "so_dong_mo_ho": sum(x["bang_chung"]["mo_ho"] for x in ra)}, "flash"


def ghi_thu_tu(yc: YeuCau):
    """Khai **CHỈ** thứ tự ngày — sinh `version` MỚI, giữ nguyên `cot`.

    ⭐⭐⭐ **Vì sao một cửa RIÊNG chứ ⛔ không dùng `POST …/khai-cot`.** Bản
       khai là **chỉ-THÊM**: một `version` mới phải chở **đủ 6 trường**. Nên
       nếu màn hình muốn khai `thu_tu` qua cửa kia, nó phải **đọc `cot` hiện
       hành rồi gửi lại** — tức một chu trình **đọc-sửa-ghi**, và giữa hai
       lượt ấy có một khe: ai khai `cot` mới trong khoảng đó sẽ bị **cú ghi
       sau đè lại bằng `cot` CŨ**, mà `version` thì vẫn tăng ⇒ ⛔ **không cổng
       nào thấy** vì mọi dòng riêng lẻ đều hợp lệ.

    ⇒ Cửa này đọc `cot` và ghi `version` mới **trong CÙNG một giao dịch**.

    ⛔ Và nó nói đúng việc nó làm: *"khai thứ tự"*, ⛔ không phải *"khai lại
      cả bản"* — hai câu ấy dẫn tới hai kỳ vọng khác nhau về những gì vừa đổi.
    """
    sid = _bat_buoc_int(yc.tham, "source_id")
    tt = yc.than.get("thu_tu")
    # ⛔⛔ Ở cửa này `thu_tu` là **BẮT BUỘC**, ⛔ không tuỳ chọn: gọi *"khai
    #    thứ tự"* mà ⛔ không đưa thứ tự thì ⛔ không có việc gì để làm — và
    #    lặng lẽ ghi `NULL` là **xoá** thứ tự người ta đã khai trước đó.
    if not isinstance(tt, str) or tt not in kc.THU_TU_HOP_LE:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "thân yêu cầu phải có `thu_tu` = %s (nhận %r)"
            % (" hoặc ".join("`%s`" % x for x in kc.THU_TU_HOP_LE), tt))
    try:
        with yc.conn.transaction():
            cu = kc.doc_khai(yc.conn, sid)
            b = kc.ghi_khai(yc.conn, sid, cu.cot, actor=yc.actor, thu_tu=tt)
    except kc.NguonLa as e:
        raise LoiCua("FLS-NGUON-LA", str(e)) from e
    except kc.KhongCoKhai as e:
        # ⚠ **409** — nguồn **có**, nhưng ⛔ chưa ai khai `cot`. ⛔ Không tự
        #   dựng một bản khai rỗng để có chỗ đậu `thu_tu`: đoán vị trí cột là
        #   thứ `sao_ke` cấm thẳng vì *"đoán ⛔ không phải kém chính xác — nó
        #   là **sai tiền**"*.
        raise LoiCua("FLS-KHAI-KHONG-CO", str(e)) from e
    except kc.LoiKhai as e:
        raise LoiCua("FLS-KHAI-THIEU", str(e)) from e
    return {"source_id": b.source_id, "version": b.version, "cot": b.cot,
            "thu_tu": b.thu_tu, "hieu_luc_tu": b.hieu_luc_tu,
            "actor": b.actor}, "flash"


# ── ⭐⭐⭐ `QĐ-ITL-117` — khai thứ tự CẢ LÔ, **CHỈ** nguồn TỰ CHỨNG ─────────
#
# ⛔⛔ **Vì sao cửa này ⛔ KHÔNG nhận `thu_tu` từ người gọi.** Đó là cả điểm
#    của nó. `POST /sources/{id}/thu-tu` là cửa *"người ấn định"* — nó **phải**
#    nhận `thu_tu`. Cửa lô này là cửa *"dữ liệu tự ấn định"*: nó **đo lại** bằng
#    chứng ở phía máy chủ rồi ghi **đúng cái nó đo ra**. ⇒ Một màn hình ⛔
#    **không có đường nào** khai `dmy` cho 27 nguồn bằng một cú bấm.
#
# ⛔⛔ **Và nó TỪ CHỐI CẢ LÔ, ⛔ không khai phần đo được rồi bỏ qua phần còn
#    lại.** Một lô khai *"thành công 25/27"* là đúng lớp lỗi cả bộ này chống:
#    người bấm thấy xanh, hai nguồn kia lặng lẽ ở lại `NULL`, và ⛔ không cổng
#    nào đỏ vì mỗi dòng bản khai đều hợp lệ.
def _ds_source_ids(than: dict[str, Any]) -> list[int]:
    """`source_ids` → danh sách số nguyên, đã bỏ trùng. ⛔ NỔ nếu rỗng.

    ⛔ ⛔ Không có mặc định *"⛔ không nói thì lấy hết"*: máy ⛔ không tự chọn
    nguồn nào cho một lô tiền, và ⛔ cũng không tự chọn nguồn nào để **ấn định
    kỳ kế toán**.
    """
    ds = than.get("source_ids")
    if not isinstance(ds, list) or not ds:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "thân yêu cầu phải có `source_ids` là danh sách ⛔ KHÔNG rỗng. "
            "⛔ ⛔ Không có mặc định lấy-hết: máy ⛔ không tự chọn nguồn cho "
            "một lô tiền")
    sid: list[int] = []
    for i, x in enumerate(ds):
        if isinstance(x, bool) or not isinstance(x, int):
            raise LoiCua("FLS-BAD-REQUEST",
                         "`source_ids[%d]` = %r ⛔ không phải số nguyên"
                         % (i, x))
        if x not in sid:
            sid.append(x)
    return sid


def _thu_tu_da_khai(conn) -> dict[int, str | None]:
    """`{source_id: thu_tu}` của bản khai **đang hiệu lực**. Một lượt, ⛔ không N+1."""
    with conn.cursor() as cur:
        cur.execute(
            "SELECT k.source_id, k.thu_tu FROM fls_khai_cot k"
            "  JOIN (SELECT source_id, max(version) v FROM fls_khai_cot"
            "         GROUP BY source_id) m"
            "    ON m.source_id = k.source_id AND m.v = k.version"
            " WHERE k.truong = %s", (kc.TRUONG_MANG_THU_TU,))
        return {r[0]: r[1] for r in cur.fetchall()}


def khai_thu_tu_lo(yc: YeuCau):
    """Khai thứ tự ngày cho **nhiều** nguồn — mỗi nguồn theo bằng chứng CỦA NÓ.

    ⭐⭐⭐ **Phép đo mở cửa này.** Trên ảnh `23719`: **34/34** nguồn có ngày
       CHUỖI đều **tự chứng minh bằng dữ liệu của chính nó** — mỗi nguồn có ít
       nhất một dòng phần-sau `> 12` *(tổng **2.296** dòng)*, và `chac_dmy` =
       **0** ở khắp **60** nguồn. ⇒ Máy đề xuất `mdy` **34 lần** và **34 lần
       một đáp án**. Bắt kế toán bấm **27** cú để trả lời một câu mà dữ liệu đã
       tự trả lời là bắt họ **đọc 27 lần rồi bấm theo phản xạ** — và một cú bấm
       theo phản xạ ⛔ **không phải** *"người ấn định"*, nó chỉ **trông** như.

    ⛔⛔ **Nên ranh giới nằm ở TỰ CHỨNG, ⛔ không ở "cả lô".** Nguồn nào ⛔
       không có bằng chứng riêng *(`de_xuat is None` — hết chứng, hay **mâu
       thuẫn**)* thì cửa này ⛔ **không khai hộ**: nó **NỔ**, và nguồn ấy phải
       đi qua cửa một-nguồn nơi có đúng một người chịu trách nhiệm.

    ⛔ Nó cũng ⛔ **không đè** bản khai của người: `da_khai` khác `de_xuat` là
      một **bất đồng thật** *(người bảo `dmy`, dữ liệu bảo `mdy`)* ⇒ NỔ kèm
      tên nguồn. Lặng lẽ ghi theo máy ở đây là **xoá một câu trả lời của người**.
    """
    cid = _bat_buoc_int(yc.tham, "chup_id")
    if "thu_tu" in yc.than:
        raise LoiCua(
            "FLS-BAD-REQUEST",
            "cửa lô ⛔ KHÔNG nhận `thu_tu` — nó đo lại bằng chứng rồi ghi đúng "
            "cái nó đo ra. Muốn tự ấn định thứ tự thì dùng "
            "`POST /sources/{source_id}/thu-tu` cho TỪNG nguồn")
    sid = _ds_source_ids(yc.than)
    try:
        anh = chup.doc_chup(yc.conn, cid)
        theo = chup.doc_o_ngay(yc.conn, cid)
    except chup.KhongCoChup as e:
        raise LoiCua("FLS-CHUP-KHONG-CO", str(e)) from e
    trong = {n.source_id: n for n in anh.nguon}
    da_khai = _thu_tu_da_khai(yc.conn)

    ngoai: list[int] = []
    khong_chung: list[str] = []
    bat_dong: list[str] = []
    khong_can: list[dict[str, Any]] = []
    da_dung: list[dict[str, Any]] = []
    se_ghi: list[tuple[Any, ttn.BangChung]] = []
    for s in sid:
        n = trong.get(s)
        if n is None:
            ngoai.append(s)
            continue
        bc = ttn.do_mot_nguon(theo.get(s, []))
        o = {"source_id": s, "source_key": n.source_key,
             "cau": ttn.cau_bang_chung(bc)}
        # ⛔⛔ **THỨ TỰ BỐN NHÁNH NÀY LÀ MỘT KHUYẾT TẬT ĐÃ VẤP, ⛔ đừng đổi.**
        #    Bản đầu để `de_xuat is None` **lên trước** `can_khai` ⇒ một nguồn
        #    **toàn ngày sê-ri** *(16/60 nguồn thật)* bị xếp vào *"⛔ không tự
        #    chứng"* và làm **NỔ CẢ LÔ** — trong khi nó ⛔ **không cần khai
        #    gì**. Bộ test bắt được: `…TOAN_NGAY_SO…` đỏ với `422`.
        #    ⇒ *"⛔ không có bằng chứng"* chỉ là một vấn đề khi **có câu hỏi
        #      cần trả lời** (`can_khai`).
        if bc.de_xuat is None and bc.can_khai:
            khong_chung.append("%s (%s)" % (n.source_key,
                                            ttn.cau_bang_chung(bc)))
        elif (bc.de_xuat is not None and da_khai.get(s) is not None
                and da_khai[s] != bc.de_xuat):
            bat_dong.append(
                "%s: đã khai `%s` mà bằng chứng nói `%s` — %s"
                % (n.source_key, da_khai[s], bc.de_xuat,
                   ttn.cau_bang_chung(bc)))
        elif not bc.can_khai:
            # ⛔ `thu_tu` của nguồn này ⛔ **không bao giờ được đọc**: `mo_ho`
            #    = 0 ⇒ mọi ô tự phân giải *(`parse_ngay` chỉ hỏi `thu_tu` khi
            #    **cả hai** phần `<= 12`)*. Ghi vào là dựng một bản khai gợi ý
            #    rằng nó có tác dụng — và lần sau ai đó sẽ **sửa nó để chữa
            #    một dòng ⛔ không liên quan**.
            khong_can.append(dict(o, ket_qua="khong_can"))
        elif da_khai.get(s) == bc.de_xuat:
            # ⛔ ⛔ Không sinh một `version` **y hệt bản cũ**: sổ chỉ-thêm ⛔
            #    không cấm, nhưng một cú bấm lần hai ⛔ không được **trông như**
            #    27 lần khai mới.
            da_dung.append(dict(o, ket_qua="da_dung", thu_tu=da_khai[s]))
        else:
            se_ghi.append((n, bc))

    if ngoai or khong_chung or bat_dong:
        raise LoiCua(
            "FLS-THU-TU-KHONG-TU-CHUNG",
            "⛔ TỪ CHỐI CẢ LÔ (⛔ không khai phần đo được rồi bỏ qua phần "
            "còn lại). " + " · ".join(x for x in (
                "%d nguồn ngoài ảnh chụp: %s" % (len(ngoai), ngoai)
                if ngoai else "",
                "%d nguồn ⛔ KHÔNG tự chứng ⇒ phải khai TỪNG nguồn: %s"
                % (len(khong_chung), "; ".join(khong_chung))
                if khong_chung else "",
                "%d nguồn BẤT ĐỒNG với bản khai của người: %s"
                % (len(bat_dong), "; ".join(bat_dong)) if bat_dong else "",
            ) if x))

    ra: list[dict[str, Any]] = []
    try:
        # ⛔ **MỘT** giao dịch cho cả lô — cùng lý do với `lo_nap`: một lô khai
        #   nửa vời là một trạng thái ⛔ không ai kiểm lại.
        with yc.conn.transaction():
            for n, bc in se_ghi:
                cu = kc.doc_khai(yc.conn, n.source_id)
                b = kc.ghi_khai(yc.conn, n.source_id, cu.cot,
                                actor=yc.actor, thu_tu=bc.de_xuat)
                ra.append({"source_id": n.source_id,
                           "source_key": n.source_key,
                           "ket_qua": "khai_moi", "thu_tu": b.thu_tu,
                           "version": b.version,
                           "cau": ttn.cau_bang_chung(bc)})
    except kc.NguonLa as e:
        raise LoiCua("FLS-NGUON-LA", str(e)) from e
    except kc.KhongCoKhai as e:
        raise LoiCua("FLS-KHAI-KHONG-CO", str(e)) from e
    except kc.LoiKhai as e:
        raise LoiCua("FLS-KHAI-THIEU", str(e)) from e

    chung = sum(bc.chac_dmy + bc.chac_mdy for _, bc in se_ghi)
    mo_ho = sum(bc.mo_ho for _, bc in se_ghi)
    return {"chup_id": cid, "doc_luc": anh.doc_luc,
            "so_nguon_yeu_cau": len(sid),
            "so_nguon_khai_moi": len(ra),
            "so_nguon_da_dung": len(da_dung),
            "so_nguon_khong_can": len(khong_can),
            # ⭐ Hai con số này là **bằng chứng của cả lô**, và chúng phải ở
            #   ngay cạnh nhau: `so_dong_lam_chung` = số dòng **tự nói ra**
            #   thứ tự; `so_dong_mo_ho` = số dòng **nhờ** bản khai vừa ghi mà
            #   đọc được. Nói cái thứ nhất mà ⛔ không nói cái thứ hai là báo
            #   một phép đo ⛔ không có hậu quả.
            "so_dong_lam_chung": chung,
            "so_dong_mo_ho": mo_ho,
            "nguon": ra + da_dung + khong_can}, "flash"


# ═══════════════════ ⑧ NẠP CẢ LÔ — `QĐ-ITL-111` + `112` ═══════════════════
#
# ⛔⛔ **Vì sao TUYẾN RIÊNG chứ ⛔ không thêm một khoá vào `xem-truoc`/`nap`.**
#    ⛔ Không phải vì *"lô to hơn"* — mà vì **khuôn TRẢ VỀ khác hẳn**: một biên
#    bản gộp mang `so_nguon_vao`/`so_nguon_chua` và mỗi luật mang **danh sách
#    nguồn ⛔ không đạt**. Một tuyến trả **hai khuôn** là một tuyến mà người gọi
#    ⛔ **không biết mình đang đọc khuôn nào** — và lúc ấy mọi phép đọc đều
#    phải đoán.
#
# ⛔⛔ **VÀ MỘT BẪY MÃ PHẢI NÓI TRƯỚC:** `NgucCanh.source_sheet` là **của cả
#    lô**, và nó nằm trong `content_key` *(khoá chống trùng)*. ⇒ Nối 60 nguồn
#    thành **một danh sách phẳng** dưới **một** `NgucCanh` thì mọi dòng mang
#    **cùng một `source_sheet`**, và dòng của **hai bank khác nhau** sẽ **bị
#    đếm là TRÙNG rồi bỏ đi trong im lặng**. ⇒ Lô này **lặp theo từng nguồn**,
#    mỗi nguồn một `NgucCanh` riêng, tất cả trong **MỘT giao dịch**.


class NguonTrongLo(NamedTuple):
    """Kết quả soát **một** nguồn trong lô. ⛔ Chưa ghi gì."""

    source_id: int
    source_key: str
    ra: list
    tk: Any
    luat: list
    khai: kc.BanKhai
    khai_version_anh: int

    @property
    def chan(self) -> list:
        return sn.chan_lai(self.luat)

    @property
    def bi_chua(self) -> bool:
        """⭐ `QĐ-ITL-111` — nguồn có luật hạng `CHẶN` đỏ thì **bị chừa**.

        ⛔ Và lô **đi tiếp**: phương án *"chặn cả lô"* **tụt về chính phương
          án này** — kế toán sẽ tự **bỏ tick** nguồn hỏng, mà một cú bỏ tick
          ⛔ **không để lại vết nào** ⇒ máy **mất hẳn** thông tin *"nguồn này
          bị chừa vì luật X"*.
        """
        return bool(self.chan)


def _soat_mot_nguon(yc: YeuCau, cid: int, trong_anh: dict,
                    source_id: int) -> NguonTrongLo:
    """Đọc khai → dựng → soát **một** nguồn từ ảnh chụp. ⛔ Không ghi gì."""
    khoa = _nguon(yc.conn, source_id)
    if source_id not in trong_anh:
        raise LoiCua(
            "FLS-CHUP-KHONG-NGUON",
            "ảnh chụp `%d` ⛔ KHÔNG đọc nguồn `%s` (`source_id=%d`)"
            % (cid, khoa, source_id))
    try:
        khai = kc.doc_khai(yc.conn, source_id)
    except kc.KhongCoKhai as e:
        raise LoiCua("FLS-KHAI-KHONG-CO", str(e)) from e

    hang = [hang_tu_o(o) for _s, _d, o in
            chup.doc_dong(yc.conn, cid, source_id=source_id)]
    try:
        ra, tk = chuyen(khoa, KHAI_ANH_CHUP, _tran(hang))
    except BanKhaiHong as e:
        raise LoiCua("FLS-KHAI-THIEU", str(e)) from e

    s10 = s10_o_cua(khoa, khai.cot, nd.doc_dai(yc.conn, source_id))
    return NguonTrongLo(
        source_id=source_id, source_key=khoa, ra=ra, tk=tk,
        luat=_soat(khoa, ra, tk, s10), khai=khai,
        khai_version_anh=trong_anh[source_id].khai_version)


def _soat_lo(yc: YeuCau) -> tuple[int, Any, list]:
    """`(chup_id, ảnh, [NguonTrongLo])`. **Dùng chung** xem-trước ↔ nạp.

    ⭐ Chính vì dùng chung mà lời hứa *"xem trước cho ra đúng thứ nạp sẽ
      ghi"* là **thật** ở cả đường lô, ⛔ không chỉ ở đường một nguồn.
    """
    cid = _bat_buoc_int(yc.than, "chup_id")
    # ⛔⛔ **⛔ KHÔNG có mặc định "⛔ không nói thì lấy hết"**. Cùng luật với
    #    `chup_id` XOR `dong`: **máy ⛔ không tự chọn nguồn nào cho một lô
    #    tiền**. Đúng 59 lần rồi sai lần thứ 60 là nạp **dữ liệu ⛔ không ai
    #    yêu cầu**, và biên bản sẽ trông hoàn toàn bình thường.
    sid = _ds_source_ids(yc.than)

    try:
        anh = chup.doc_chup(yc.conn, cid)
    except chup.KhongCoChup as e:
        raise LoiCua("FLS-CHUP-KHONG-CO", str(e)) from e
    trong = {n.source_id: n for n in anh.nguon}
    return cid, anh, [_soat_mot_nguon(yc, cid, trong, s) for s in sid]


# ── ⭐⭐⭐ `QĐ-ITL-112` — GỘP 9 luật, ⛔ không 540 ô ─────────────────────────
def _gop_luat(nguon: list) -> list[dict[str, Any]]:
    """60 nguồn × 9 luật = **540 ô** → **9 dòng**, mỗi dòng bung ra nguồn dính.

    ⛔⛔ **VÀ ĐÂY LÀ CHỖ MỘT PHÉP GỘP NGÂY THƠ SẼ BÁO OAN.** Đo trên ảnh chụp
       thật: **10/60 nguồn đọc ra 0 dòng** *(tài khoản đã mở mà chưa dùng —
       ⛔ không phải khuyết tật)*. Với chúng, `S2`…`S7` trả `dat=False,
       da_do=0` — **đúng theo luật nền** *"xanh trên tập RỖNG là CHƯA ĐO"*.
       ⇒ Gộp bằng `all(dat)` thì **6/9 luật của cả lô đỏ** chỉ vì 10 tài khoản
       rỗng, trong khi 50 nguồn thật **đều đạt**. Và một báo động **đỏ oan** là
       một báo động **sẽ bị bỏ qua** — lúc ấy cả biên bản mất tác dụng.

    ⇒ Nên phép gộp phân biệt **HAI** thứ mà một cột `dat` ⛔ không tách được:

       | | |
       |---|---|
       | `nguon_khong_dat` | nguồn **đo được** *(`da_do > 0`)* mà **⛔ không đạt** ⇒ khuyết tật THẬT |
       | `nguon_chua_do` | nguồn `da_do = 0` ⇒ ⛔ **không có gì để đo**, ⛔ không phải lỗi |

    ⭐ Và luật nền **vẫn đứng ở tầng lô**: `da_do` gộp = `0` ⇒ ⛔ **KHÔNG
      ĐẠT**. Một nguồn rỗng trong 60 nguồn ⛔ không làm cả lô thành *chưa đo*;
      nhưng **60 nguồn rỗng thì có**.
    """
    if not nguon:
        return []
    thu_tu_ten = [k.ten for k in nguon[0].luat]
    nang = {sn.CHAN: 3, sn.CO_: 2, sn.CANH: 1}
    ra: list[dict[str, Any]] = []
    for ten in thu_tu_ten:
        cac = [(n, k) for n in nguon for k in n.luat if k.ten == ten]
        da_do = sum(k.da_do for _n, k in cac)
        # ⛔⛔⛔ **HANG `CHAN` ⛔ KHONG BAO GIO duoc mien bang "chua do" —
        #    va day la mot khuyet tat THAT ma chinh bo test nay bat duoc.**
        #
        #    Ban dau: `khong_dat = [... if k.da_do > 0 and not k.dat]`. Nhung
        #    `s10_o_cua` khi ⛔ chua thu dai tra `(CHAN, dat=False, da_do=0)`
        #    ⇒ nguon ay roi vao `chua_do`, va phep gop bao **`S10` DAT** —
        #    TRONG KHI `S10` dang **CHUA chinh nguon do**.
        #
        #    ⇒ Mot bien ban noi *"luat nay dat"* ben canh mot nguon bi chua
        #      **VI chinh luat ay** la mot bien ban **⛔ khong doc duoc**, va
        #      no che dung thu no sinh ra de phoi. Dung lop `QĐ-ITL-103`: mot
        #      con so DUNG nam trong mot cau SAI.
        #
        #    ⭐ Phan biet dung: `da_do = 0` **⛔ khong** phan biet duoc *"⛔
        #      khong co gi de do"* (nguon 0 dong, hang `CO`) voi *"co thu de
        #      do ma ⛔ khong do duoc"* (thieu ban khai thu hai, hang `CHAN`).
        #      **HANG** thi phan biet duoc: `CHAN` la thu lam nguon **bi
        #      chua** ⇒ no la khuyet tat THAT, du `da_do = 0`.
        khong_dat = [n.source_key for n, k in cac
                     if not k.xanh and (k.hang == sn.CHAN or k.da_do > 0)]
        chua_do = [n.source_key for n, k in cac
                   if k.da_do == 0 and k.hang != sn.CHAN]
        # ⛔ Hạng = **nặng nhất** trong lô. ⛔ Không lấy hạng của nguồn đầu:
        #    hai nguồn có thể cho cùng một luật hai hạng khác nhau (`S10`).
        hang = max((k.hang for _n, k in cac), key=lambda h: nang.get(h, 0))
        dat = (not khong_dat) and da_do > 0
        ra.append({
            "ten": ten, "hang": hang, "dat": dat, "da_do": da_do,
            "so_nguon_khong_dat": len(khong_dat),
            "nguon_khong_dat": khong_dat,
            "so_nguon_chua_do": len(chua_do),
            "nguon_chua_do": chua_do,
            "thong_diep": _cau_gop(ten, len(cac), da_do, khong_dat, chua_do),
        })
    return ra


def _cau_gop(ten: str, so_nguon: int, da_do: int,
             khong_dat: list, chua_do: list) -> str:
    """Một câu cho NGƯỜI, và nó phải mang **con số**, ⛔ không chỉ đỏ/xanh."""
    if da_do == 0:
        return ("⛔ đo được 0 trên cả %d nguồn — xanh trên tập RỖNG là CHƯA "
                "ĐO, ⛔ không phải đạt" % so_nguon)
    p = ["đã đo %d trên %d nguồn" % (da_do, so_nguon)]
    if khong_dat:
        p.append("⛔ %d nguồn ⛔ không đạt" % len(khong_dat))
    else:
        p.append("⛔ 0 nguồn ⛔ không đạt")
    if chua_do:
        p.append("%d nguồn ⛔ không có gì để đo" % len(chua_do))
    return " · ".join(p)


def _bien_ban_gop(cid: int, anh: Any, nguon: list,
                  nap: dict | None = None) -> dict[str, Any]:
    """Khuôn biên bản GỘP — `QĐ-ITL-112`.

    ⛔⛔ **Dải đầu phải nói `so_nguon_chua` TRƯỚC mọi con số dòng.** Câu kế
       toán hỏi là *"lô này vào được ⛔ không, cái gì cản"* — một biên bản mở
       đầu bằng *"8.365 dòng"* mà để *"2 nguồn bị chừa"* ở cuối là một biên
       bản **trả lời đúng câu ⛔ không ai hỏi**.
    """
    chua = [n for n in nguon if n.bi_chua]
    vao = [n for n in nguon if not n.bi_chua]
    luat = _gop_luat(nguon)
    bb: dict[str, Any] = {
        "chup_id": cid, "doc_luc": anh.doc_luc,
        "so_nguon": len(nguon),
        "so_nguon_vao": len(vao),
        "so_nguon_chua": len(chua),
        # ⛔ Ba đường cộng **theo nguồn SẼ VÀO**, ⛔ không theo cả lô: một con
        #    số gộp cả nguồn bị chừa sẽ ⛔ không khớp số dòng thật vào sổ.
        "so_dong_vao": sum(n.tk.vao for n in vao),
        "so_dong_ra": sum(n.tk.ra for n in vao),
        "rong": sum(n.tk.rong for n in vao),
        "loi": sum(n.tk.loi for n in vao),
        "luat": luat,
        "chan": [k["ten"] for k in luat
                 if k["hang"] == sn.CHAN and not k["dat"]],
        "co": [k["ten"] for k in luat
               if k["hang"] != sn.CHAN and not k["dat"]],
        # ⭐⭐ Từng nguồn — **kể cả nguồn bị chừa, và NÊU RÕ luật nào chừa
        #    nó**. `QĐ-ITL-111`: chừa mà ⛔ không nói vì sao thì kế toán ⛔
        #    không có đường nào sửa, và cú bỏ tick lại quay về ⛔ không vết.
        "nguon": [{
            "source_id": n.source_id, "source_key": n.source_key,
            "bi_chua": n.bi_chua,
            "chua_vi": [k.ten for k in n.chan],
            "so_dong_vao": n.tk.vao, "so_dong_ra": n.tk.ra,
            "rong": n.tk.rong, "loi": n.tk.loi,
            "thu_tu": n.khai.thu_tu,
            "khai_version": n.khai.version,
            # ⚠ Khai của **ẢNH** có thể khác khai **hiện hiệu lực** — chuyện
            #   BÌNH THƯỜNG *(ảnh tuần trước đọc bằng `v1`)*. Khai ra chứ ⛔
            #   không chặn, và ⛔ không lặng lẽ áp `v2` lên dữ liệu đọc `v1`.
            "khai_version_anh": n.khai_version_anh,
        } for n in nguon],
    }
    # ⛔⛔⛔ **BAT BIEN CHEO — cong chong dung lop loi da can that o tren.**
    #
    #    Neu mot nguon bi chua vi luat `X` ma dong gop cua `X` lai noi **DAT**,
    #    thi bien ban dang **che dung thu no sinh ra de phoi**. Phep kiem nay
    #    ⛔ khong the do bang mat: no doi soi CA HAI TRUC cua 540 o.
    #
    #    ⇒ NO ngay tai day chu ⛔ khong tra ve mot bien ban noi doi. Day la
    #      khuyet tat cua **CHUNG TA**, ⛔ khong cua du lieu — nen no phai on.
    theo_ten = {k["ten"]: k for k in luat}
    for n in chua:
        for ten in (k.ten for k in n.chan):
            g = theo_ten.get(ten)
            assert g is not None and not g["dat"], (
                "⛔⛔ bien ban gop noi luat `%s` DAT trong khi nguon `%s` bi "
                "CHUA vi chinh luat ay" % (ten, n.source_key))
            assert n.source_key in g["nguon_khong_dat"], (
                "⛔⛔ nguon `%s` bi CHUA vi `%s` ma ⛔ khong co trong "
                "`nguon_khong_dat` cua dong gop ⇒ bam vao luat do se ⛔ khong "
                "thay nguon nay" % (n.source_key, ten))
    if nap is not None:
        bb.update(nap)
    return bb


def lo_xem_truoc(yc: YeuCau):
    """SOÁT cả lô mà ⛔ **KHÔNG GHI**. ⛔ Không chạm một bảng ghi nào."""
    cid, anh, nguon = _soat_lo(yc)
    bb = _bien_ban_gop(cid, anh, nguon)
    # ⛔ `se_ghi` ở tầng lô = *"có nguồn nào vào được ⛔ không"*, ⛔ **không**
    #    = *"cả lô sạch"*. `QĐ-ITL-111`: một nguồn `CHẶN` ⛔ không chặn 59
    #    nguồn còn lại.
    bb["se_ghi"] = bb["so_nguon_vao"] > 0
    return bb, "flash"


def lo_nap(yc: YeuCau):
    """Nạp cả lô: nguồn sạch **vào sổ**, nguồn `CHẶN` **bị chừa**.

    ⛔⛔ **MỘT giao dịch cho CẢ LÔ.** Nguồn thứ 40 nổ giữa đường thì **⛔ không
       nguồn nào vào sổ** — một lô nửa-commit là đúng thảm hoạ đã xảy ra thật
       *(`chay_nap`: hai lần nạp đầu tiên để lại **394 dòng ĐÃ COMMIT** trong
       sổ)*, và cổng bốn đường **⛔ không gỡ được cái đã commit**.

    ⭐ **Một `run_id` cho cả lô.** `mo_run` có `ON CONFLICT DO NOTHING` nên
      đầu lô chỉ sinh **một** dòng `fls_run`; `row_count` do `dong_run` **ĐẾM
      TỪ BẢNG** sau mỗi nguồn ⇒ số cuối là **tổng của cả lô**, ⛔ không phải
      của nguồn đầu tiên. *(Có bài ghim đúng tính chất này.)*
    """
    cid, anh, nguon = _soat_lo(yc)
    rid = _chu(yc.than, "run_id")
    vao = [n for n in nguon if not n.bi_chua]
    if not vao:
        # ⛔ **422 kèm biên bản ĐẦY ĐỦ** — nói *"⛔ không nạp được gì"* mà ⛔
        #    không nói **nguồn nào bị chừa vì luật nào** là bắt người ta đoán.
        raise LoiCua("FLS-SOAT-CHAN",
                     "⛔ cả %d nguồn đều có luật hạng CHẶN đỏ ⇒ ⛔ KHÔNG ghi "
                     "một dòng nào" % len(nguon),
                     bien_ban=_bien_ban_gop(cid, anh, nguon))

    # ⭐⭐⭐ **Ảnh lệnh chi HIỆU LỰC — đọc MỘT lần cho cả lô** *(10/09)*.
    #
    # ⛔⛔ Trước đây cửa này ⛔ **không** truyền `pm` ⇒ mọi dòng vào sổ qua màn
    #    `F04` có **⛔ 0 mối nối**, trong khi **2.745** mối nối đang có trong kho
    #    thật do `tools/nap_that.py` sinh *(một đường KHÁC, đọc PM sống)*. ⇒ Dựng
    #    lại sổ bằng cửa này **đổi 2.745 mối nối MÁY ghép thành 2.745 cú bấm
    #    TAY**, và ⛔ không cổng nào nói ra.
    #
    # ⭐ Đọc **NGOÀI** vòng lặp: 59 nguồn × một phép đọc ảnh là 59 lần đọc cùng
    #   một thứ, và tệ hơn — nếu một nhịp chụp PM chen vào giữa lô thì **các
    #   nguồn đầu ghép theo ảnh cũ, các nguồn sau theo ảnh mới**. Một lô phải
    #   thấy **đúng một** ảnh.
    #
    # ⛔ `None` *(chưa ai nạp dòng lệnh nào)* ⛔ **không** bị nuốt thành 0 mối
    #   nối im lặng — nó vào **biên bản** ở khoá `nap.anh_pm` (`None` = ⛔ chưa
#   ai nạp dòng lệnh nào), nên màn hình nói được ra điều đó.
    rid_pm = anh_pm.anh_pm_hieu_luc(yc.conn, yc.pv)
    dong_pm = anh_pm.doc_dong_pm(yc.conn, rid_pm) if rid_pm else None

    tong = {"vao_so": 0, "trung": 0, "vao_hang_cho": 0, "loai": 0,
            "unmapped": 0, "ghep_pm": 0}
    try:
        with yc.conn.transaction():
            for n in vao:
                nc = NgucCanh(run_id=rid, contract_version="v1.1",
                              canon_version="v1.0", mapping_version="v1.0",
                              source_system="P100",
                              # ⭐ MỖI nguồn một `source_sheet` RIÊNG — xem
                              #   khối chú thích đầu mục ⑧.
                              source_sheet=n.source_key,
                              chup_id=cid, thu_tu=n.khai.thu_tu)
                kq = nl.nap_lo(yc.conn, n.ra, nc, n.luat,
                               actor=yc.actor, pm=dong_pm)
                tong["vao_so"] += kq.nap.vao_so
                tong["trung"] += kq.nap.bo_qua_trung
                tong["vao_hang_cho"] += kq.vao_hang_cho
                tong["loai"] += kq.nap.loai
                tong["unmapped"] += kq.nap.unmapped
                tong["ghep_pm"] += kq.nap.ghep_pm
    except nl.LoBiChan as e:
        # ⛔ Tới đây thì `_soat_lo` đã lọc hết nguồn `CHẶN` ⇒ nhánh này nghĩa
        #    là **hai phép soát ⛔ không đồng ý với nhau**. Nói thẳng, ⛔ không
        #    nuốt: đó là một khuyết tật của CHÍNH TA, ⛔ không của dữ liệu.
        raise LoiCua("FLS-SOAT-CHAN",
                     "⛔⛔ soát lô nói SẠCH mà `nap_lo` nói CHẶN — hai phép "
                     "soát ⛔ không đồng ý: %s" % e,
                     bien_ban=_bien_ban_gop(cid, anh, nguon)) from e
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e

    return _bien_ban_gop(cid, anh, nguon,
                         nap=dict(tong, run_id=rid,
                                  anh_pm=rid_pm)), "flash"
