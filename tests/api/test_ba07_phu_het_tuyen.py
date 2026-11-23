# -*- coding: utf-8 -*-
"""⛔ Cổng PHỦ TUYẾN: mọi cửa THẬT phải có mặt trong `BA-07 API CONTRACT`.

⛔⛔ **Vì sao cổng này tồn tại — nó sinh ra từ một phép đo, ⛔ không từ một ý
   thích ngăn nắp.** Ngày 09/09, đo `BANG_TUYEN` *(29 tuyến)* đối chiếu `BA-07`:
   **2 tuyến ⛔ KHÔNG có mặt** — `POST /nap/lo` và `POST /nap/lo/xem-truoc`,
   tức **cả lằn nạp CẢ LÔ** *(`QĐ-ITL-111`/`112`)*, thứ mà màn `F04` nay
   **LUÔN** đi qua và đã chạy thật trên **60 nguồn · 8.368 dòng**.

⛔⛔ **Và nó vô hình với mọi cổng đang có.** `kiem_so_song` ghim **SỐ** *(và nó
   xanh: 67/67)*; `kiem_tai_lieu` canh bảng markdown + ngày; `soi_bang_tuyen`
   đối chiếu bản khai tuyến với **SQL thật**. ⛔ Không cổng nào hỏi câu *"tài
   liệu hợp đồng có NÓI tới cửa này ⛔ không"* ⇒ một lằn cửa mới có thể sống
   trọn một đợt mà hợp đồng ⛔ không biết nó tồn tại.

⭐ Cổng bắt **HAI CHIỀU**, và chiều thứ hai mới là chiều dễ dối lòng:
     ⓐ cửa THẬT mà tài liệu ⛔ không nói  ⇒ người đọc hợp đồng ⛔ không biết
        cửa ấy có, nên họ ⛔ không dùng — hay tệ hơn, họ dựng cửa thứ hai;
     ⓑ tài liệu nói một đường **⛔ chưa tồn tại** mà ⛔ không đánh dấu `⬜`
        ⇒ người đọc tưởng nó có rồi. Đo 09/09: `§4` *(nhóm CHẠY)* liệt **3**
        đường `runs/*` ⛔ **không** đánh dấu gì, và cả **3 đều ⛔ chưa tồn
        tại** — trong khi `§2`/`§3` thì dùng `✅`/`⬜` đúng luật.
"""
from __future__ import annotations

import io
import os
import re

import fls.api.xu_ly  # noqa: F401  — nạp `HAM` trước, tránh vòng nhập
from fls.api import bang_tuyen as bt

BA07 = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "docs", "ITL", "02_BA", "07_API_CONTRACT.md")

# ⛔ Dấu *"⛔ chưa xây"* mà `BA-07` đang dùng thật *(`§2`/`§3`/`§4b`)*.
DAU_KE_HOACH = ("⬜", "chưa xây", "chưa dựng", "KẾ HOẠCH")


def _doc() -> str:
    with io.open(BA07, encoding="utf-8") as f:
        return f.read()


def _duoi(duong: str) -> str:
    """Bỏ tiền tố phiên bản — tài liệu viết cả hai lối.

    ⛔⛔ Đo bằng **đường ĐẦY ĐỦ** là một phép đo **báo oan**: lượt đầu nó kêu
       **5** tuyến thiếu, mà 3 trong số đó *(`queue/{itl_id}/done` · `reopen` ·
       `unmatch`)* tài liệu **CÓ** nói — chỉ là nói dạng `POST /queue/…`, ⛔
       không kèm `/api/fls/v1`. ⇒ Đúng bài học *"đo QUAN HỆ thì gọi hàm thật"*:
       một phép quét dựng lại bằng tay sẽ **báo oan cùng lượt**.
    """
    return duong.replace(bt.TIEN_TO, "")


def test_moi_tuyen_THAT_deu_co_mat_trong_BA07():
    thieu = [(t.phuong_thuc, t.duong) for t in bt.BANG_TUYEN
             if _duoi(t.duong) not in _doc()]
    assert len(bt.BANG_TUYEN) > 0, "⛔ đo được 0 tuyến ⇒ phép đo này CHƯA CHẠY"
    assert thieu == [], (
        "⛔ %d/%d tuyến THẬT mà `BA-07` ⛔ không nói tới: %s. Người đọc hợp "
        "đồng ⛔ không biết cửa ấy có ⇒ họ ⛔ không dùng nó, hay dựng cửa thứ "
        "hai làm đúng việc ấy."
        % (len(thieu), len(bt.BANG_TUYEN), thieu))


def test_duong_BA07_noi_ma_CHUA_TON_TAI_phai_duoc_DANH_DAU():
    """⛔ Một đường **⛔ chưa có** mà nằm trơn trong bảng thì nó đọc y hệt một
      đường **đã có** — và người đọc sẽ đi gọi nó.
    """
    chu = _doc()
    that = {_duoi(t.duong) for t in bt.BANG_TUYEN}
    # ⛔ Chỉ soi các đường có TIỀN TỐ đầy đủ: dạng viết ngắn `POST /queue/…`
    #   trùng hình với văn xuôi, và một cổng bắt cả văn xuôi là một cổng sẽ
    #   bị tắt trong ba tuần.
    xau, da_do = [], 0
    for dong in chu.splitlines():
        # ⛔ Sau tiền tố PHẢI có ít nhất một đoạn đường thật: bản đầu để
        #   `[A-Za-z0-9_{}/-]+` nên nó vớt luôn chữ `/api/fls/v1/` trong **văn
        #   xuôi** *(câu "Prefix: …")* và báo oan 2 lần.
        for duong in re.findall(
                re.escape(bt.TIEN_TO) + r"/[A-Za-z0-9_{}][A-Za-z0-9_{}/-]*",
                dong):
            if _duoi(duong) in that:
                continue
            da_do += 1
            if not any(d in dong for d in DAU_KE_HOACH):
                xau.append((duong, dong.strip()[:110]))
    assert da_do > 0, (
        "⛔ đo được 0 đường-chưa-tồn-tại ⇒ hoặc tài liệu ⛔ không còn nêu kế "
        "hoạch nào, hoặc phép đo này đã mù. Kiểm lại trước khi tin nó XANH")
    assert xau == [], (
        "⛔ %d đường ⛔ CHƯA TỒN TẠI mà ⛔ không mang dấu %s ⇒ đọc y hệt một "
        "cửa đã có: %s" % (len(xau), DAU_KE_HOACH, xau))
