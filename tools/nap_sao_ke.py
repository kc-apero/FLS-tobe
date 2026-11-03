# -*- coding: utf-8 -*-
"""**MỘT** đường nạp 60 sheet `R |` — dùng chung cho mọi công cụ `F04`.

⭐⭐ **Vì sao tách ra.** Chặng 1 *(`dung_lai_bank_transactions.py`)* và chặng 2
   *(`soat_nap_sao_ke.py`)* đều phải nạp **cùng một thứ theo cùng một cách**.
   Chép đoạn nạp sang tệp thứ hai là tạo **bản sao thứ hai của một luật** —
   đúng cái bệnh mà `fls/canon/o_loi.py` ra đời để chữa *(bốn bản sao của luật
   *"ô lỗi"* ⇒ dòng bị loại ở tầng này, được giữ ở tầng kia)*. Hai đường nạp
   lệch nhau thì **chặng 2 sẽ soát một thứ ⛔ không phải thứ chặng 1 đã chứng
   minh** — và cái lệch ấy sẽ im lặng.

⛔⛔ **`QĐ-ITL-92` — mặc định ⛔ KHÔNG đọc `Description`.** Đó là trường duy nhất
   có thể mang thông tin cá nhân, và ⛔ **không phép đo nào của `F04` cần nó**.
   ⇒ `TRUONG_MAC_DINH` chỉ có **5/6**. Muốn đọc đủ 6 thì phải **nói ra**, ⛔
   không lấy được bằng cách quên.

⛔ Tệp này ⛔ **KHÔNG GHI** vào bất cứ trang tính nào.
"""
from __future__ import annotations

import sys
from collections import Counter

sys.path.insert(0, __file__.rsplit("tools", 1)[0])

import psycopg  # noqa: E402

from fls.adapters.sao_ke import (KHAI_ANH_CHUP, TRUONG_DOC_DUOC,  # noqa: E402
                                 chuyen, hang_tu_o)
from fls.db.kho import dsn_that  # noqa: E402
from fls.repo.khai_cot import KhongCoKhai, doc_khai  # noqa: E402
from tools.do_chenh_lech import doc_cot  # noqa: E402
from tools.do_hinh_dang import meta  # noqa: E402

# ⛔⛔ `dong_dau` va `doc_ban_khai` DA BI GO KHOI TEP NAY (`CR#11` task `3`).
#
# Chung la duong doc **dong 1 cua sheet**. Giu chung lai o day — du chi la mot
# dong `import` khong ai goi — la giu **mot canh cua con he he mo**: lan sau ai
# do gap loi "thieu ban khai trong kho" se thay chung nam san day va noi lai
# trong ba dong. Va luc do cu cat day coi nhu chua tung xay ra, ma cong van
# xanh `8.338/8.338`.
#
# ⇒ Co bai `test_duong_nap_KHONG_CON_doc_dong_1` quet **ma nguon** tep nay.

# ⭐ 6/6 tu `QĐ-ITL-128` (17/09) — `QĐ-ITL-92` DA DUOC MO LAI, `Description`
#    DUOC DOC. ⛔ Khoi nhan su `9`…`14` van CAM (`QĐ-ITL-107`). Khai o `sao_ke`, ⛔ khong
#    go lai o day: bai `test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he` da bat
#    duoc **ba** ban sao cua dung danh sach nay.
TRUONG_MAC_DINH: tuple[str, ...] = TRUONG_DOC_DUOC


def ten_sheet_r(sid: str, tok: str) -> list[str]:
    return sorted(s["properties"]["title"] for s in meta(sid, tok)["sheets"]
                  if s["properties"]["title"].startswith("R |"))


def khai_tu_kho(ten_r: list[str], dsn: str | None = None
                ) -> dict[str, dict[str, int]]:
    """`{tên sheet: bản khai}` — đọc từ **`fls_khai_cot`**, ⛔ không từ dòng 1.

    ⭐⭐ **Đây là cú CẮT DÂY của `CR#11`** *(task `3`)*. Từ đây đường nạp
      ⛔ **không còn đọc dòng 1 của bất cứ sheet nào** — bản khai đến từ kho.

    ⛔⛔ **Và nó ⛔ KHÔNG có đường lùi về sheet.** Một nhánh *"⛔ không thấy
      trong kho thì đọc dòng 1"* nghe rất hiền, nhưng nó làm **cổng của task
      này mất hết ý nghĩa**: kho rỗng thì mọi thứ vẫn chạy, vẫn ra
      `8.338/8.338`, và ⛔ **không ai biết cú cắt dây chưa hề xảy ra**.
      ⇒ Thiếu bản khai là **NỔ**, và nổ **nêu tên sheet** + lệnh chạy lại.

    ⚠ Khoá tra là **`fls_source.source_key` = ĐÚNG tên sheet** *(task `7`)* —
      ⛔ không tiền tố, ⛔ không một phép dịch nào.
    """
    return {t: b.cot for t, b in khai_day_du(ten_r, dsn).items()}


def khai_day_du(ten_r: list[str], dsn: str | None = None):
    """`{tên sheet: BanKhai}` — **bản khai ĐẦY ĐỦ**, ⛔ không chỉ `cot`.

    ⭐⭐ Thêm 08/09 *(`QĐ-ITL-110`)*: lằn ẢNH CHỤP phải ghim **`version`** của
       bản khai đã dùng *(`fls_chup_nguon.khai_version`)*, mà `khai_tu_kho`
       thì chỉ trả `cot`. ⇒ Hàm này là chỗ đọc kho **duy nhất**, và
       `khai_tu_kho` **rút gọn từ nó** — ⛔ không mở một đường đọc thứ hai cho
       cùng một bảng.

    ⚠ Kèm cả `source_id`, vì tầng kho ghi theo `source_id` chứ ⛔ không theo tên.
    """
    ra: dict = {}
    thieu: list[str] = []
    with psycopg.connect(dsn or dsn_that()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT source_key, source_id FROM fls_source"
                " WHERE source_key = ANY(%s)", (list(ten_r),))
            sid_theo = dict(cur.fetchall())
        for t in ten_r:
            if t not in sid_theo:
                thieu.append(t)
                continue
            try:
                ra[t] = doc_khai(conn, sid_theo[t])
            except KhongCoKhai:
                thieu.append(t)
    if thieu:
        raise RuntimeError(
            "⛔ %d sheet ⛔ KHÔNG có bản khai trong kho: %s%s"
            " · ⛔ Đường nạp ⛔ KHÔNG lùi về dòng 1 — lùi thì cổng của task"
            " `3` xanh mà cú cắt dây chưa hề xảy ra."
            " ⇒ Chạy: python tools/nap_nguon_va_khai.py --that"
            % (len(thieu), sorted(thieu)[:5], "…" if len(thieu) > 5 else ""))
    return ra


def doc_vung_chuan(sid: str, tok: str, ten_r: list[str] | None = None,
                   truong: tuple[str, ...] = TRUONG_MAC_DINH,
                   khai_theo: dict[str, dict[str, int]] | None = None
                   ) -> tuple[dict[str, list[dict]], dict[str, dict[str, int]]]:
    """⭐⭐⭐ **PHÉP ĐỌC — và nó là phép đọc DUY NHẤT của cả lằn `F04`.**

    → `({sheet: [{tên trường: ô NGUYÊN VĂN}]}, khai_theo đã dùng)`.

    ⛔⛔ **Vì sao tách ra khỏi `nap()` ngày 08/09 (`QĐ-ITL-110`).** Lằn ẢNH CHỤP
       cần **ô nguyên văn TRƯỚC `chuyen()`**; `nap()` thì trả khuôn RA **sau**
       `chuyen()`. Nếu công cụ chụp tự gọi `doc_cot` một lần nữa thì lằn này có
       **đường đọc THỨ HAI** — đúng cái bệnh mà docstring đầu tệp này ra đời để
       chữa *(*"hai đường nạp lệch nhau thì chặng 2 sẽ soát một thứ ⛔ không
       phải thứ chặng 1 đã chứng minh — và cái lệch ấy sẽ IM LẶNG"*)*.

    ⇒ Nay **`nap()` cũng đi qua hàm này**, nên con số `8.338/8.338` của chặng 1
      đo **chính đường mà `F04` sẽ đi**, ⛔ không phải một đường song song.

    ⭐ Ô về **nguyên văn**: số là số, chuỗi là chuỗi *(`UNFORMATTED_VALUE`)*.
      ⛔ Ép về chuỗi ở đây là dựng lại cái bẫy đã cắn hai lần — sê-ri ngày
      thành `"45586"` *(`QĐ-ITL-102` ⓶)*, mã 16 số thành `1.23e+15`.
    """
    ten_r = ten_r if ten_r is not None else ten_sheet_r(sid, tok)
    khai_theo = khai_theo if khai_theo is not None else khai_tu_kho(ten_r)

    # ⭐⭐ **MOT lot goi gop cho CA 60 sheet**, ⛔ khong phai 60 lot goi.
    #    ⛔ Ban dau toi goi `doc_cot` **trong vong lap** ⇒ 60 lot goi API cho
    #    dung cai viec ma `doc_cot` **da biet gop 60 vung mot lot**. Ket qua:
    #    **can han muc that** — `429` van no sau khi lui-va-thu-lai het 4 lan.
    #    ⇒ Gom **moi vung cua moi sheet** roi goi mot the: ~300 vung ⇒ ~5 lot,
    #    giam **12 lan**. ⚠ Han muc doc la **tai nguyen dung CHUNG voi owner**
    #    dang mo chinh file do — tieu hoang o day lam cham may cua nguoi khac.
    can_theo: dict[str, dict[str, int]] = {}
    dai: list[tuple[str, int]] = []
    for t in ten_r:
        khai = khai_theo[t]
        # ⛔ Chi doc cot DA KHAI va DUOC PHEP (`QĐ-ITL-92`).
        lay = {k: khai[k] for k in truong if k in khai}
        if not lay:
            raise RuntimeError("%s: ⛔ khong khai truong nao doc duoc" % t)
        can_theo[t] = lay
        dai += [(t, i) for i in sorted(set(lay.values()))]

    # ⭐⭐⭐ `tho=True` — **BAT BUOC**, va no la mot cu VA do bang phep DO.
    #
    # ⛔⛔ Do tren mot anh chup THAT ngay 08/09 *(8.368 dong)*: **100% o la
    #    `str`**, ke ca voi `render="UNFORMATTED_VALUE"`. Nguyen nhan o
    #    `doc_cot`: mot dong `str(x).strip()` **vo dieu kien**. ⇒ Cau
    #    *"bay `doc_cot` ep o ve chuoi — da va tan noi"* cua `QĐ-ITL-102` ⓶
    #    chi dung voi **trieu chung** (ky hieu khoa hoc), ⛔ khong voi
    #    **nguyen nhan**.
    #
    # ⇒ Anh chup ma ep kieu thi no ⛔ **khong con la anh chup** — se-ri ngay
    #   thanh `"45586"`, va ca lap luan *"luu `jsonb` de giu kieu"* thanh rong.
    c = doc_cot(sid, dai, tok, render="UNFORMATTED_VALUE", tho=True)

    ra: dict[str, list[dict]] = {}
    for t in ten_r:
        lay = can_theo[t]
        n = max((len(c[(t, i)]) for i in set(lay.values())), default=0)
        ra[t] = [{k: (c[(t, i)][j] if j < len(c[(t, i)]) else "")
                  for k, i in lay.items()} for j in range(n)]
    return ra, khai_theo


def nap(sid: str, tok: str, ten_r: list[str] | None = None,
        truong: tuple[str, ...] = TRUONG_MAC_DINH,
        khai_theo: dict[str, dict[str, int]] | None = None):
    """→ `(rows, theo_sheet, dem_ma)`.

    `rows`      — mọi dòng theo `KHUON_RA`, **xuyên cả 60 sheet**.
    `theo_sheet`— `{sheet: (vao, ra, rong, loi)}`, đầu vào của luật `S1`.
    `dem_ma`    — bộ đếm `Num`, **dùng chung** cho cả 60 sheet *(mã lặp giữa
                  các tài khoản, nên đếm riêng từng sheet là SAI luật `Num`)*.

    ⭐⭐ **`khai_theo` mặc định = ĐỌC TỪ KHO** *(`CR#11` task `3`, 08/09)*.
      Trước 08/09 hàm này gọi `dong_dau(...)` rồi `doc_ban_khai(...)` — tức
      **đường nạp phụ thuộc vào Google Sheets cho CÁCH ĐỌC**, ⛔ không chỉ cho
      dữ liệu. Nay bản khai đến từ `fls_khai_cot`, và **dòng 1 ⛔ không còn
      được đọc trong đường này** *(một lượt gọi API ít đi)*.

    ⚠ Truyền `khai_theo` tường minh **CHỈ** dùng cho phép đo đối chứng
      *(sheet ↔ kho)* và cho test — ⛔ **không** phải một đường lùi.
    """
    ten_r = ten_r if ten_r is not None else ten_sheet_r(sid, tok)
    o_theo, _khai = doc_vung_chuan(sid, tok, ten_r, truong, khai_theo)

    dem: Counter = Counter()
    rows: list[list] = []
    theo: dict[str, tuple[int, int, int, int]] = {}
    for t in ten_r:
        # ⭐ Đi qua **cùng** bản khai ảnh chụp mà tầng kho dùng
        #   (`sao_ke.KHAI_ANH_CHUP` / `hang_tu_o`) ⇒ con số đối chiếu của
        #   chặng 1 đo **chính đường `F04` sẽ đi**, ⛔ không một đường song song.
        ra, st = chuyen(t, KHAI_ANH_CHUP,
                        [hang_tu_o(o) for o in o_theo[t]], dem)
        rows += ra
        theo[t] = (st.vao, st.ra, st.rong, st.loi)

    return rows, theo, dem
