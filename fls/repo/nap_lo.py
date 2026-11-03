# -*- coding: utf-8 -*-
"""Nạp **một lô sao kê** — nối biên bản 8 luật vào phép ghi *(`CR#11` task `5`)*.

⭐⭐ **Module này ⛔ KHÔNG tự ghi một dòng nào vào sổ.** Nó gọi
   `chay_nap.chay()` — chỗ **duy nhất** giữ ba thứ ⛔ không được có bản sao:

     ⓐ chống trùng bằng `content_key` *(`BA-07` §4b ⓹)*;
     ⓑ cổng **bốn đường** *(`vào = sổ + loại + rỗng + trùng`)*, kiểm **TRƯỚC** ghi;
     ⓒ **MỘT giao dịch** cho cả lần nạp.

★ **Việc riêng của module này đúng hai thứ, và cả hai đều là QUYẾT ĐỊNH:**

  ⓵ ⛔ **Hạng `CHẶN` đỏ ⇒ ⛔ KHÔNG ghi một dòng nào.** `CHẶN` là *"lỗi của
    **FLS**"* — dòng rơi im lặng. Nạp tiếp là **cố ý ghi một lô đã biết là
    hỏng**.

  ⓶ ⭐ **Hạng `CỜ` đỏ ⇒ VẪN ghi, và dòng bị cờ vào HÀNG CHỜ CÓ LÝ DO.** `CỜ` là
    khuyết tật **có sẵn trong sổ kế toán** *(đo sống: **5/8** luật đang cờ)*.
    Chặn ở đây nghĩa là FLS **⛔ không bao giờ nạp được gì** — mà những dòng ấy
    là **TIỀN THẬT**: vứt chúng là vi phạm ***"⛔ 0 dòng rơi im lặng"***.
    ⇒ Chúng vào sổ, **mang một lý do**, và **có người phải trả lời**.

⛔⛔ **Và lý do ⛔ KHÔNG được ghi thẳng bằng `INSERT`.** `fls_queue_event` là
   một trong **bốn bảng chỉ-một-chỗ-ghi** *(`tests/repo/test_chi_mot_cho_ghi_tay
   .py`)*: sau khi `QĐ-ITL-16` bỏ bước duyệt và `QĐ-ITL-27` khai tử vai người
   hậu kiểm, **nhật ký là lớp kiểm soát DUY NHẤT còn lại**. ⇒ Module này đi qua
   `ghi_tay.ghi_ly_do()`, ⛔ không viết câu SQL nào.

⚠ **`actor` phải đến TỪ NGƯỜI**, ⛔ không phải một hằng trong tệp này. Một lô
  nạp là **hành vi của người bấm `Nhận`** — nếu máy tự đứng tên thì cột `actor`
  của cả hàng chờ mất nghĩa ngay từ lô đầu tiên.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from fls.adapters.sao_ke_canon import nap as nap_sao_ke
from fls.kiem.soat_nap import KetQuaSoat, chan_lai
from fls.repo.chay_nap import KetQuaNap, NgucCanh, chay
from fls.repo.ghi_tay import ghi_ly_do
from fls.repo.kho_sach import HINH_RUN_THAT
from fls.adapters.pm_join import DongPM
from fls.repo.pham_vi import PhamVi


class LoBiChan(Exception):
    """⛔ Có luật hạng `CHẶN` đỏ ⇒ ⛔ **không ghi một dòng nào**.

    `BA-07` §4b ⓸: **422** `FLS-SOAT-CHAN`.
    """

    ma = "FLS-SOAT-CHAN"

    def __init__(self, thong_diep: str, luat: Sequence[KetQuaSoat] = ()) -> None:
        super().__init__(thong_diep)
        self.luat = tuple(luat)


@dataclass(frozen=True)
class KetQuaLo:
    """Kết quả một lô = kết quả ghi **+** biên bản soát. Hai thứ, ⛔ không một.

    ⛔ Gộp chúng thành một chữ *"OK"* là làm mất đúng thứ màn `SCR-F04` tồn tại
    để hiện: *bao nhiêu dòng vào sổ · bao nhiêu vào hàng chờ · **vì sao***.
    """

    nap: KetQuaNap
    luat: tuple[KetQuaSoat, ...]
    vao_hang_cho: int = 0
    ly_do_hang_cho: dict[str, int] = field(default_factory=dict)

    @property
    def co_do(self) -> tuple[KetQuaSoat, ...]:
        """Các luật ĐỎ mà ⛔ **không** chặn — vẫn phải hiện đỏ trên màn."""
        return tuple(k for k in self.luat if not k.xanh and k not in chan_lai(self.luat))

    def bao(self) -> str:
        return "%s · hàng chờ %d dòng" % (self.nap.bao(), self.vao_hang_cho)


def nap_lo(conn, tho: Sequence[Sequence[Any]], nc: NgucCanh,
           luat: Sequence[KetQuaSoat], *, actor: str,
           pv: PhamVi | None = None,
           pm: Sequence[DongPM] | None = None) -> KetQuaLo:
    """Soát → *(nếu qua)* ghi **+ ghép lệnh chi** → dòng bị cờ vào hàng chờ.

    ⛔ **Thứ tự này ⛔ KHÔNG đảo được.** Soát **sau khi** ghi thì `CHẶN` chỉ còn
      là một bản báo cáo về một cái sổ **đã hỏng** — đúng cái bẫy mà migration
      `0015` và cổng Σ mối nối đều dựng ra để tránh.

    ⭐⭐⭐ **`pm` — thêm 2026-09-10, và nó vá một lỗ IM LẶNG.** Trước đó cửa này
      gọi `chay()` **⛔ không truyền `pm`**, nên mọi dòng nạp qua màn `F04` vào
      sổ với **⛔ 0 mối noi**. Trong khi ấy **2.745 mối nối** đang có trong kho
      thật là do `tools/nap_that.py` sinh — một đường **khác**, đọc PM sống từ
      Sheets. ⇒ Dựng lại sổ bằng cửa lô sẽ **đổi 2.745 mối nối MÁY ghép thành
      2.745 cú bấm TAY**, và ⛔ không cổng nào nói ra.

      ⛔ `None` ⛔ **không** có nghĩa *"không ghép"* một cách im lặng — người
      gọi phải **cố ý** truyền `None` *(vd bộ test chỉ đo đường ghi)*. Đường
      thật lấy nó bằng `anh_pm.doc_dong_pm(conn, anh_pm_hieu_luc(conn, pv))`.
    """
    if not str(actor or "").strip():
        raise ValueError(
            "⛔ thiếu `actor`. Một lô nạp là **hành vi của người bấm Nhận** — "
            "máy tự đứng tên thì cột `actor` của cả hàng chờ mất nghĩa")

    # ⛔⛔ **BẢN TRẮNG: `run_id` phải đúng hình `NAP-yyyy-mm-dd-NGUON`.**
    #
    # Kiểm ở ĐÂY, **trước khi ghi** — ⛔ không để nó nổ muộn. Mọi cửa đọc lọc
    # theo `PhamVi`, và `PhamVi` là **bản TRẮNG**: `run_id` sai hình thì dòng
    # **vào sổ được** nhưng ⛔ **không màn hình nào nhìn thấy nó, MÃI MÃI** —
    # một lần nạp **im lặng rơi vào hư không**.
    #
    # ⚠ Lỗ này đã tự lộ ra khi viết bài test: đường ghi lý do nổ `NgoaiPhamVi`
    #   vì `run_id` của test sai hình. Nhưng nó CHỈ nổ khi lô **có cờ** — lô
    #   sạch thì đi qua êm ru. ⇒ Phải có phép kiểm riêng, ⛔ không dựa vào việc
    #   một đường khác tình cờ nổ hộ.
    if not HINH_RUN_THAT.match(nc.run_id or ""):
        raise ValueError(
            "⛔ `run_id=%r` ⛔ KHÔNG đúng hình `NAP-yyyy-mm-dd-NGUON`. Dòng nạp "
            "bằng một `run_id` sai hình sẽ vào sổ được nhưng ⛔ KHÔNG cửa đọc "
            "nào thấy — một lần nạp rơi vào hư không mà ⛔ không cổng nào báo."
            % nc.run_id)

    chan = chan_lai(luat)
    if chan:
        raise LoBiChan(
            "⛔ %d luật hạng CHẶN đỏ ⇒ ⛔ KHÔNG ghi một dòng nào: %s"
            % (len(chan), " · ".join("%s (%s)" % (k.ten, k.thong_diep)
                                     for k in chan)), chan)

    # ⛔ `pm_trong_kho=True`: `pm` den TU KHO (`anh_pm.doc_dong_pm`), ⛔ khong
    #   phai doc song tu Sheets ⇒ ⛔ KHONG duoc chep lai vao `fls_pm_line`.
    kq = chay(conn, tho, nc, bo_nap=nap_sao_ke, pm=pm, pm_trong_kho=True)

    # ── dòng bị CỜ → hàng chờ có lý do ────────────────────────────────────
    #
    # ⛔ Đi qua `ghi_tay.ghi_ly_do()`, ⛔ không một câu `INSERT` nào ở đây:
    #    `fls_queue_event` là bảng **chỉ-một-chỗ-ghi**, và chỗ ấy sinh nhật ký.
    co = tuple(k for k in luat if not k.xanh)
    vao_hc = 0
    dem: dict[str, int] = {}
    # ⛔ Phạm vi hẹp ĐÚNG lô này (`mot_lan_nap`) — ⛔ không `ca_kho`.
    pv = pv or PhamVi(kieu="mot_lan_nap", run_id=nc.run_id)
    for itl_id, ly_do in _ly_do_tung_dong(conn, nc, co).items():
        ghi_ly_do(conn, pv, itl_id, reason=ly_do, actor=actor)
        vao_hc += 1
        dem[ly_do] = dem.get(ly_do, 0) + 1
    return KetQuaLo(nap=kq, luat=tuple(luat), vao_hang_cho=vao_hc,
                    ly_do_hang_cho=dem)


def _ly_do_tung_dong(conn, nc: NgucCanh,
                     co: Sequence[KetQuaSoat]) -> dict[int, str]:
    """`itl_id` → câu lý do **đúng của DÒNG ẤY**. Đóng `GAP-NAP-01`.

    ⛔⛔⛔ **Đây là chỗ `GAP-NAP-01` từng sống, và nó sống 15 ngày.** Bản cũ
       tính **một** câu từ danh sách luật trượt rồi đóng dấu câu ấy lên **mọi**
       dòng `UNMAPPED` của lô. Đo trên sổ thật 11/09:

         `S3 · moi dong phai co TIEN`  gắn 2.596 dòng · đúng **0** ⇒ oan **100%**
         `S7 · dong trung HOAN TOAN`   gắn 5.952 dòng · đúng **66** ⇒ oan **98,9%**

       ⇒ Kế toán mở hàng chờ và đọc một câu **sai** về dòng trước mặt.

    ★ **Ba nhóm, và chúng ⛔ không được đối xử như nhau:**

      ⓐ Dòng **bị một luật mức DÒNG chỉ đích danh** ⇒ mang tên đúng các luật ấy.
      ⓑ Dòng **⛔ không luật nào chạm** ⇒ ⛔ **KHÔNG ghi một sự kiện nào**.
      ⓒ Luật mức **SHEET/BẢN KHAI** (`S1`·`S6`·`S8`·`S10`, `dong_xau` rỗng)
        ⇒ ⛔ **KHÔNG** gắn cho dòng nào. Chúng trượt vì cả *sheet* hỏng, và
        đóng dấu chúng lên từng dòng là tái lập đúng lỗi vừa vá. Chúng vẫn
        **đỏ trong biên bản** — chỗ của chúng là ở đó.

    ⛔⛔⛔ **Vì sao ⓑ ⛔ KHÔNG được gán một câu "chưa ghép lệnh chi".** Bản vá
       đầu của tôi làm đúng thế — và **bài `test_luat_XANH_HET_thi_KHONG_ai_
       vao_hang_cho` đỏ ngay**, đúng thứ nó sinh ra để canh. Đọc lại
       `_SQL_HANG_CHO`: **thành viên** hàng chờ đến từ `work_status =
       'UNMAPPED'`, còn `fls_queue_state` chỉ được **`LEFT JOIN`** vào để lấy
       câu lý do. ⇒ Dòng ⓑ **vẫn ở trong hàng chờ**, chỉ là cột lý do **trống**
       — và trống là **câu trả lời đúng**: ⛔ không luật nào nói gì về nó.

       Gán một câu cho ⓑ nghĩa là ghi **8.387 sự kiện** chỉ để lấp một ô, tức
       là làm lại **đúng** khuyết tật vừa vá, chỉ bằng chữ dễ nghe hơn.

    ⚠ `source_row` là **chỉ số 1-based trong lô** *(`sao_ke_canon.nap`)*, và
      `dong_xau` là **chỉ số 0-based trong cùng list ấy** ⇒ `+1`. Hai con số
      này ⛔ không được suy từ thứ tự `itl_id`: dòng bị loại và dòng trùng
      `content_key` làm thứ tự ấy **thủng**, im lặng.
    """
    theo_dong: dict[int, list[str]] = {}
    for k in co:
        for i in k.dong_xau:              # ⓒ `()` ⇒ vòng này ⛔ không chạy
            theo_dong.setdefault(i + 1, []).append(k.ten)
    if not theo_dong:
        return {}

    with conn.cursor() as cur:
        cur.execute(
            "SELECT itl_id, source_row FROM fls_itl"
            " WHERE run_id = %s AND source_sheet = %s"
            "   AND work_status = 'UNMAPPED' AND source_row = ANY(%s)"
            " ORDER BY itl_id",
            (nc.run_id, nc.source_sheet, sorted(theo_dong)))
        dong = cur.fetchall()

    return {itl_id: " · ".join(theo_dong[sr]) for itl_id, sr in dong}


