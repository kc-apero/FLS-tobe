# -*- coding: utf-8 -*-
"""⛔⛔ **CỔNG RA CỦA `P7` TASK `6`** — màn `F04` chạy THẬT trên một DOM.

`DEV-03` §2b khai cổng của task này bằng đúng hai câu:

    · hạng `CHẶN` ⇒ nút `Nhận` **TẮT**
    · mỗi luật hiện **`đã đo`**

⇒ Nên bài này ⛔ **không đọc mã bằng mắt**. Nó nạp **đúng tệp màn thật**
  *(`fls/web/tep/man_f04.js`)* vào một DOM tối thiểu, thay cửa bằng **cửa
  giả**, rồi soi cái màn vẽ ra.

★ Cửa được **giả lập** — bài này hỏi *"màn hình làm đúng ⛔ không"*, ⛔ không
  phải *"cửa trả đúng ⛔ không"*: câu sau là việc của
  `tests/api/test_cua_chup_pg.py`, chạy trên kho THẬT qua HTTP THẬT.

⛔ **Ba thứ bài này ⛔ KHÔNG kiểm được** *(và vì thế còn nằm ở `B7 · UAT`)*:
   thời gian vẽ trên máy kế toán · lưới xem trước có **đủ rộng** ⛔ không ·
   cảm giác khi bấm. Xem đầu `dom_gia.js`.
"""
from __future__ import annotations

import json

from tests.web.khung_node import TEP_F04, VO_F04, _chay, can_node

_NGUON = [
    {"source_id": 11, "source_key": "R | AAA_MSB VND_CN", "src_type": "Bank",
     "last_seen_at": None, "lag_days": None, "cutoff_date": None,
     "txn_count": 120, "khai_version": 1,
     "chup_cuoi": "2026-09-08T08:24:30+00:00", "trang_thai_nguon": None},
    {"source_id": 12, "source_key": "R | BBB_TCB USD_VGOH", "src_type": "Bank",
     "last_seen_at": None, "lag_days": None, "cutoff_date": None,
     "txn_count": 8, "khai_version": None,          # ⭐ CHUA ai khai
     "chup_cuoi": None, "trang_thai_nguon": None},
    {"source_id": 13, "source_key": "R | VND_HotBonus", "src_type": "Cash",
     "last_seen_at": None, "lag_days": None, "cutoff_date": None,
     "txn_count": 15, "khai_version": 3,
     "chup_cuoi": "2026-09-08T08:27:40+00:00", "trang_thai_nguon": None},
]

_CHUP_DS = {"chup": [
    {"chup_id": 23719, "doc_luc": "2026-09-08T08:27:40+00:00",
     "spreadsheet_id": "SID", "lan": "Bank", "giay": 3.19, "actor": "may",
     "so_nguon": 2, "so_dong": 3, "nguon": []},
], "so": 1}

_CHUP_MOT = {
    "chup_id": 23719, "doc_luc": "2026-09-08T08:27:40+00:00",
    "spreadsheet_id": "SID", "lan": "Bank", "giay": 3.19, "actor": "may",
    "so_nguon": 2, "so_dong": 3,
    "nguon": [
        {"source_id": 11, "source_key": "R | AAA_MSB VND_CN",
         "khai_version": 1, "so_dong": 2},
        # ⭐ Nguon doc ra **0 dong** — phai HIEN RA, ⛔ khong bien mat.
        {"source_id": 12, "source_key": "R | BBB_TCB USD_VGOH",
         "khai_version": 1, "so_dong": 0},
    ],
    "dong": [
        {"source_id": 11, "dong_so": 0,
         "o": {"Date": 45586, "Currency": "VND", "Debit": 1240000000,
               "Credit": "", "Reference number": 1234567890123456}},
        {"source_id": 11, "dong_so": 1,
         "o": {"Date": "25/08/2026", "Currency": "USD", "Debit": "",
               "Credit": 66923.25, "Reference number": "FT26217B4K9"}},
    ],
}


def _luat(ten, hang, dat, da_do, td="x", khong_dat=(), chua_do=()):
    """⭐ `nguon_khong_dat`/`nguon_chua_do` — hai ô của phép GỘP.

    ⛔ Thiếu chúng thì màn vẽ ô *"Nguồn dính"* thành `—` ở mọi dòng, và bài
      kiểm sẽ xanh trên một màn **⛔ không bung được nguồn nào**.
    """
    return {"ten": ten, "hang": hang, "dat": dat, "da_do": da_do,
            "thong_diep": td,
            "nguon_khong_dat": list(khong_dat),
            "so_nguon_khong_dat": len(khong_dat),
            "nguon_chua_do": list(chua_do),
            "so_nguon_chua_do": len(chua_do)}


def _nguon_bb(khoa, bi_chua=False, chua_vi=(), thu_tu="mdy"):
    return {"source_id": 11, "source_key": khoa, "bi_chua": bi_chua,
            "chua_vi": list(chua_vi), "so_dong_vao": 3, "so_dong_ra": 2,
            "rong": 1, "loi": 0, "thu_tu": thu_tu,
            "khai_version": 1, "khai_version_anh": 1}


def _bb(chan=(), co=(), luat=None, nguon=None, so_nguon_chua=0):
    """Khuôn biên bản **GỘP** — `QĐ-ITL-112`.

    ⛔⛔ Bản trước là khuôn **một nguồn** *(`nguon` là một CHUỖI)*. Đổi nó ở
       đây chứ ⛔ không thêm một khuôn thứ hai: hai khuôn trong cùng bộ test
       là hai chỗ để bộ test **nói về hai màn hình khác nhau** mà cả hai đều
       xanh — đúng lý do `khung_node.py` được tách ra.
    """
    ng = nguon if nguon is not None else [_nguon_bb("R | AAA_MSB VND_CN")]
    return {"chup_id": 23719, "doc_luc": "2026-09-08T08:27:40+00:00",
            "so_nguon": len(ng),
            "so_nguon_vao": len(ng) - so_nguon_chua,
            "so_nguon_chua": so_nguon_chua,
            "so_dong_vao": 3, "so_dong_ra": 2, "rong": 1, "loi": 0,
            "luat": luat or [_luat("S%d · x" % i, "CO", True, 8338)
                             for i in range(1, 10)],
            "chan": list(chan), "co": list(co), "nguon": ng,
            "se_ghi": not chan}


# ⭐⭐ Bang chung thu tu ngay — **hinh dang cua nguon that**, ⛔ khong bia:
#    `R | PO2_OCBC USD_SGO2` do duoc 905 dong mo ho · 1.263 dong chac `mdy` ·
#    ⛔ 0 dong chac `dmy`. Bo bot con so cho gon la lam bai kiem ⛔ khong con
#    kiem duoc cai no sinh ra de kiem: *"cau bang chung co CON SO"*.
_THU_TU = {
    "chup_id": 23719, "doc_luc": "2026-09-08T08:27:40+00:00",
    "so_nguon": 3, "so_can_khai": 2, "so_con_thieu": 2, "so_dong_mo_ho": 964,
    "nguon": [
        {"source_id": 1, "source_key": "R | PO2_OCBC USD_SGO2",
         "da_khai": None, "can_khai": True, "de_xuat": "mdy",
         "mau_thuan": False,
         "cau": "1263 dong chac chan `mdy` · 0 dong chac chan `dmy`",
         "bang_chung": {"so_dong": 2168, "o_so": 0, "o_chuoi": 2168,
                        "chac_dmy": 0, "chac_mdy": 1263, "mo_ho": 905}},
        {"source_id": 2, "source_key": "R | Tron_hai_kieu",
         "da_khai": None, "can_khai": True, "de_xuat": None,
         "mau_thuan": True,
         "cau": "MAU THUAN: 4 dong chac chan `dmy` VA 6 dong chac chan `mdy`",
         "bang_chung": {"so_dong": 69, "o_so": 0, "o_chuoi": 69,
                        "chac_dmy": 4, "chac_mdy": 6, "mo_ho": 59}},
        {"source_id": 3, "source_key": "R | Toan_ngay_so",
         "da_khai": None, "can_khai": False, "de_xuat": None,
         "mau_thuan": False,
         "cau": "120/120 dong co o `Date` la SO (seri) ⇒ khong can khai",
         "bang_chung": {"so_dong": 120, "o_so": 120, "o_chuoi": 0,
                        "chac_dmy": 0, "chac_mdy": 0, "mo_ho": 0}},
    ]}


def _tra(**them) -> str:
    """Khuôn `_TRA` của cửa giả — ⛔ khai ĐỦ mọi đường màn sẽ gọi.

    ⛔ Thiếu một đường thì cửa giả trả `data: null`, và màn sẽ vẽ **trạng thái
      RỖNG** — một bài test đọc trạng thái rỗng thành *"màn ⛔ không vẽ gì"* là
      một bài **báo oan**.
    """
    m = {"/sources": {"nguon": _NGUON, "so_nguon": len(_NGUON),
                      "gap_trang_thai": "GAP-CHUP-02"},
         "/chup?lan=Bank&limit=10": _CHUP_DS,
         "/chup/23719?limit=50": _CHUP_MOT,
         # ⭐ `QĐ-ITL-113` — cua BANG CHUNG thu tu ngay. Thieu duong nay thi
         #    khoi ②b ve **trang thai RONG**, va mot bai doc trang thai rong
         #    thanh *"man ⛔ khong ve gi"* la mot bai **bao oan**.
         "/chup/23719/thu-tu": _THU_TU}
    m.update(them)
    return "".join("_TRA[%s] = {data: %s};\n"
                   % (json.dumps(k), json.dumps(v, ensure_ascii=False))
                   for k, v in m.items())


def _f04(kich_ban: str, **them):
    return _chay(_tra(**them) + "\n" + kich_ban, tep=TEP_F04, vo=VO_F04)


# ── ① chọn phạm vi ───────────────────────────────────────────────────────
@can_node
def test_MAC_DINH_tick_TAT_CA_nguon():
    """⭐ `BA-06` §7 ⓶ ①: mặc định **tick tất cả**.

    ⛔ Đổi mặc định là bắt kế toán làm thêm một việc họ ⛔ **chưa từng phải
      làm** — nút `Run` hôm nay cũng gom cả lô một lượt.
    """
    ra = _f04("""
      await F04.ve();
      const t = document.querySelectorAll('#nap-chon input');
      return {so: t.length, tick: t.filter(x => x.checked).length,
              chon: F04._S.chon.size};
    """)
    assert ra["so"] == 3
    assert ra["tick"] == 3, "⛔ ⛔ không tick sẵn tất cả"
    assert ra["chon"] == 3


@can_node
def test_nguon_CHUA_AI_KHAI_thi_nut_ban_khai_TAT():
    """⭐ `khai_version = null` là một CÂU TRẢ LỜI, và màn phải **chặn** ở đó.

    ⛔ Máy ⛔ không đoán vị trí cột *(`BA-06` §7 ⓷)*: đoán đúng **59/60** vẫn là
      **sai tiền ở tài khoản thứ 60**.
    """
    ra = _f04("""
      await F04.ve();
      const tr = [...document.querySelectorAll('[data-sid]')];
      return tr.map(r => ({sid: r.dataset.sid,
                           tat: r.cells[5].children[0].disabled,
                           khai: r.cells[2].textContent}));
    """)
    theo = {r["sid"]: r for r in ra}
    assert theo["12"]["tat"] is True, "⛔ nguồn chưa khai mà nút vẫn bấm được"
    assert "chưa khai" in theo["12"]["khai"]
    assert theo["11"]["tat"] is False


@can_node
def test_man_NOI_RA_rang_kho_KHONG_co_trang_thai_nguon():
    """⛔⛔ `GAP-CHUP-02` — màn phải **nói ra**, ⛔ không im lặng.

    Im lặng thì kế toán đọc danh sách thành *"cả 68 nguồn đều đang chạy"*, và
    một nguồn ra `0` dòng vì **tài khoản đã đóng** trông giống hệt một nguồn
    ra `0` dòng vì **thiếu sheet**. Đó đúng lớp lỗi *"mặc định im lặng"* đã đẻ
    ra **6.843** ô `Input here` của AS-IS.
    """
    ra = _f04("""
      await F04.ve();
      return document.querySelector('#nap-chon').textContent;
    """)
    assert "GAP-CHUP-02" in ra
    assert "chưa phân biệt được nguồn đã đóng" in ra


# ── ② FLS đọc ────────────────────────────────────────────────────────────
@can_node
def test_man_NOI_RA_rang_no_CHUA_TU_DOC_LAI_duoc():
    """⛔⛔ `GAP-CHUP-01`. ⛔ Dựng sẵn một nút *"Đọc lại"* chưa có đường chạy là
    **mời người bấm rồi chờ mãi** — cùng luật với nút `Xuất báo cáo tuần` của
    `F03` *(một nút im lặng là một nút người ta bấm lại lần nữa)*."""
    ra = _f04("""
      await F04.ve();
      const o = document.querySelector('#nap-doc');
      return {chu: o.textContent,
              nut: [...o.querySelectorAll('button')].map(b => b.textContent)};
    """)
    assert "GAP-CHUP-01" in ra["chu"]
    assert "chưa tự đọc lại được" in ra["chu"]
    assert not any("Đọc lại" in x for x in ra["nut"]), (
        "⛔ có nút Đọc lại mà ⛔ chưa có đường chạy")


@can_node
def test_XEM_TRUOC_hien_DAU_THOI_DIEM_va_nguon_ra_0_DONG():
    """⭐⭐ Hai thứ `BA-06` §7 ⓶ ② đòi, và cái thứ hai là điểm mù `S8`.

    ⛔ Suy tập nguồn từ **dữ liệu** thì sheet ra `0` dòng **biến mất** — và màn
      sẽ nói *"đọc được 1 nguồn"* trong khi lần đọc ấy đọc **2**.
    """
    ra = _f04("""
      await F04.ve();
      await F04._S, null;
      document.querySelector('[data-chup]').cells[4].children[0].onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      const o = document.querySelector('#nap-xem');
      /* ⛔⛔ Cho doi **PHAI tinh trong JS**, ⛔ khong go tay mot chuoi gio.
         Man hien gio cua **may ke toan** *(dung cho nguoi dung o Viet Nam)*,
         nen mot chuoi go tay se do tren may o mui gio khac — mot bai test do
         vi **cho ngoi** thi ⛔ khong do gi ca. */
      const d = new Date('2026-09-08T08:27:40+00:00');
      const h = x => String(x).padStart(2, '0');
      const mong = h(d.getDate()) + '/' + h(d.getMonth() + 1) + ' '
                 + h(d.getHours()) + ':' + h(d.getMinutes()) + ':'
                 + h(d.getSeconds());
      return {chu: o.textContent, mong: mong,
              chup: F04._S.chup && F04._S.chup.chup_id};
    """)
    assert ra["chup"] == 23719
    assert ra["mong"] in ra["chu"], "⛔ ⛔ không hiện dấu thời điểm đọc"
    assert "dấu thời điểm, không phải tuổi" in ra["chu"]
    assert "1 nguồn đọc ra 0 dòng" in ra["chu"], (
        "⛔ nguồn ra 0 dòng biến mất khỏi màn — đúng điểm mù S8")
    assert "R | BBB_TCB USD_VGOH" in ra["chu"]


@can_node
def test_LUOI_XEM_TRUOC_du_SAU_cot_va_cot_Description_DUOC_DOC():
    """⛔⛔ **`QĐ-ITL-128` trên màn hình** *(mở lại `QĐ-ITL-92`, 17/09)*.

    ⭐ Bài này TỪNG ghim điều **ngược lại** — *"lưới giữ cột `Description`
      nhưng nói thẳng nó ⛔ không được đọc"* — và nó ⛔ **không bị xoá**, nó bị
      **đảo chiều**. Nỗi lo gốc *(«cấm đọc» và «quên đọc» trông giống hệt
      nhau)* nay đổi vế: một cột **đã mở** mà màn vẫn vẽ như **bị chặn** thì
      kế toán sẽ ⛔ không bao giờ đi tìm giá trị trong đó.

    ⛔ Tên cột + cờ `doc_duoc` đến từ `window.FLS_TRUONG_CHUAN` — **SINH** từ
      `sao_ke.SAU_TRUONG`/`TRUONG_DOC_DUOC`, ⛔ không gõ tay ở tầng màn
      *(cổng #15)*. ⇒ Bài này đo **cờ** và **lớp CSS**, ⛔ **không** đo giá
      trị ô: dữ liệu ở đây là mẫu giả, nên một ô rỗng nói về **mẫu**, ⛔ không
      nói về **quyền đọc** *(`Đ4` — một phép đo phải biết nó đo gì)*.
    """
    ra = _f04("""
      await F04.ve();
      document.querySelector('[data-chup]').cells[4].children[0].onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      const t = document.querySelector('#nap-xem table');
      const th = t.children.filter(c => c.tagName === 'THEAD')[0];
      const b = t.tBodies[0];
      return {cot: th.rows[0].cells.map(c => c.textContent),
              d0: b.rows[0].cells.map(c => c.textContent),
              lop0: b.rows[0].cells.map(c => c.className)};
    """)
    # ⛔ Con so nay ⛔ khong go tay: 1 cot `Nguon` + do dai `SAU_TRUONG`.
    from fls.adapters.sao_ke import SAU_TRUONG, TRUONG_DOC_DUOC
    assert len(ra["cot"]) == len(SAU_TRUONG) + 1 == 7
    assert ra["cot"][0] == "Nguồn"
    for t in SAU_TRUONG:
        assert any(t in c for c in ra["cot"]), "⛔ thiếu cột %s" % t
    mo_ta = [c for c in ra["cot"] if c.startswith("Description")][0]
    # ⭐⭐⭐ `QĐ-ITL-128` *(17/09)* — owner mo lai `QĐ-ITL-92`. Bai nay TUNG
    #   ghim dieu NGUOC LAI *("cot phai NOI ra rang no bi cam doc")* va no
    #   ⛔ khong bi xoa: no bi **dao chieu**. ⛔ Nhan man ⛔ khong go tay —
    #   `man_f04.js` suy tu co `doc_duoc`, ma co ay suy tu `TRUONG_DOC_DUOC`
    #   ⇒ mot nguon, va bai nay canh dung cho noi.
    assert "không đọc" not in mo_ta, (
        "⛔ cột `Description` nay ĐƯỢC đọc (`QĐ-ITL-128`) — nhãn cũ nói ngược")
    assert "Description" in TRUONG_DOC_DUOC
    # ⭐ Lop `faint` la DAU CUA O BI CHAN. Mat no = man ⛔ khong con ve
    #   `Description` nhu mot o bi cam.
    i = ra["cot"].index(mo_ta)
    assert ra["lop0"][i] != "faint", (
        f"⛔ ô `Description` vẫn mang lớp của ô BỊ CHẶN "
        f"({ra['lop0'][i]!r}) dù `QĐ-ITL-128` đã mở")
    # ⭐ Hanh vi Sheets #7 — o TIEN mang lop `num` (so kieu ke toan).
    assert ra["lop0"][ra["cot"].index("Debit")] == "num"


def test_co_doc_duoc_cua_Description_SINH_tu_ban_khai_va_nay_la_TRUE():
    """⭐⭐ Cờ `doc_duoc` là **một nguồn**: `sao_ke.TRUONG_DOC_DUOC`.

    ⛔ Gõ tay cờ này ở tầng màn là tạo **bản khai thứ hai** — bài
    `test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he` đã bắt **ba** bản sao trong
    một phiên. Bài này canh **giá trị** của cờ, ⛔ không canh cách vẽ.
    """
    from fls.adapters.sao_ke import SAU_TRUONG, TRUONG_DOC_DUOC
    assert set(TRUONG_DOC_DUOC) == set(SAU_TRUONG), (
        "⛔ `QĐ-ITL-128` mở CẢ 6/6 trường — lệch là một trường bị bỏ quên")
    assert "Description" in TRUONG_DOC_DUOC


# ── ④ BIÊN BẢN — hai cổng ra của task `6` ────────────────────────────────
_MO_ANH = """
  await F04.ve();
  document.querySelector('[data-chup]').cells[4].children[0].onclick();
  await new Promise(r => setTimeout(r, 0));
  await new Promise(r => setTimeout(r, 0));
  F04._S.chon = new Set([11]);
  F04._cap_nhat_nut();
  await F04._soat();
"""


@can_node
def test_CONG_moi_luat_PHAI_hien_DA_DO():
    """⛔⛔ **CỔNG RA #2 của task `6`.**

    Một luật nói *"đạt"* mà ⛔ không nói **đã đo bao nhiêu** là một luật
    **chưa đo**. Luật nền ấy đã **cứu thật một lần**: `L6` của cổng #17 báo
    đo `0` ⇒ ĐỎ; ⛔ không có nó thì cổng **xanh giả** trên một phép đo ⛔ chưa
    từng chạy.
    """
    ra = _f04(_MO_ANH + """
      const t = document.querySelector('#nap-bb table');
      const th = t.children.filter(c => c.tagName === 'THEAD')[0];
      return {cot: th.rows[0].cells.map(c => c.textContent),
              dong: t.tBodies[0].rows.length,
              da_do: t.tBodies[0].rows.map(r => r.cells[3].textContent)};
    """, **{"/nap/lo/xem-truoc": _bb()})
    assert "Đã đo" in ra["cot"], "⛔ lưới biên bản ⛔ không có cột `Đã đo`"
    assert ra["dong"] == 9, "⛔ biên bản ⛔ không đủ 9 luật"
    assert all(x.strip() for x in ra["da_do"]), "⛔ có luật để trống `đã đo`"


@can_node
def test_luat_do_duoc_0_THU_hien_CHUA_DO_chu_KHONG_hien_so_0():
    """⭐⭐ `da_do = 0` ⛔ **KHÔNG** được trông như một con số bình thường.

    Cùng luật với ô `dat = null` của `F03`: **một cổng xanh vì ⛔ không đo gì
    thì nguy hơn một cổng đỏ**.
    """
    luat = [_luat("S%d · x" % i, "CO", True, 8338) for i in range(1, 9)]
    luat.append(_luat("S10 · hai ban khai", "CHAN", False, 0,
                      "chua thu dai doc"))
    ra = _f04(_MO_ANH + """
      const t = document.querySelector('#nap-bb table');
      const r = t.tBodies[0].rows[8];
      return {da_do: r.cells[3].textContent};
    """, **{"/nap/lo/xem-truoc": _bb(chan=["S10 · hai ban khai"], luat=luat)})
    assert "chưa đo" in ra["da_do"], (
        "⛔ `da_do = 0` hiện như số 0 bình thường: %r" % ra["da_do"])
    assert ra["da_do"].strip() != "0"


@can_node
def test_CONG_hang_CHAN_do_thi_nut_NHAN_TAT():
    """⛔⛔ **CỔNG RA #1 của task `6`** — câu duy nhất `DEV-03` §2b đòi."""
    luat = [_luat("S1 · ba duong can", "CHAN", False, 60, "lech 48 dong")]
    luat += [_luat("S%d · x" % i, "CO", True, 8338) for i in range(2, 10)]
    ra = _f04(_MO_ANH + """
      return {tat: document.querySelector('#nap-nut-nhan').disabled,
              vi_sao: document.querySelector('#nap-vi-sao').textContent,
              chu: document.querySelector('#nap-bb').textContent};
    """, **{"/nap/lo/xem-truoc": _bb(chan=["S1 · ba duong can"], luat=luat)})
    assert ra["tat"] is True, "⛔⛔ có luật hạng CHẶN đỏ mà nút Nhận vẫn BẬT"
    assert "chặn" in ra["vi_sao"], (
        "⛔ nút tắt mà màn ⛔ không nói VÌ SAO nó tắt: %r" % ra["vi_sao"])
    assert "Không một dòng nào sẽ vào sổ" in ra["chu"]


@can_node
def test_hang_CO_do_thi_nut_NHAN_VAN_BAT():
    """⭐⭐ Hạng `CỜ` **⛔ KHÔNG chặn**, và đó ⛔ không phải nới cổng.

    Nó trả lời một câu **khác**: *khuyết tật này là của AI?* Hạng `CỜ` vẫn
    **ĐỎ**, chỉ ⛔ không chặn — vì những dòng ấy là **tiền thật**, và vứt
    chúng đi là vi phạm *"⛔ 0 dòng rơi im lặng"*.
    """
    luat = [_luat("S1 · ba duong can", "CHAN", True, 60)]
    luat += [_luat("S2 · co tien phai co ma", "CO", False, 8338, "7 dong")]
    luat += [_luat("S%d · x" % i, "CO", True, 8338) for i in range(3, 10)]
    ra = _f04(_MO_ANH + """
      return {tat: document.querySelector('#nap-nut-nhan').disabled,
              chu: document.querySelector('#nap-bb').textContent};
    """, **{"/nap/lo/xem-truoc": _bb(co=["S2 · co tien phai co ma"], luat=luat)})
    assert ra["tat"] is False, "⛔ hạng CỜ mà đã chặn nút Nhận"
    assert "vẫn bật" in ra["chu"]
    assert "tiền thật" in ra["chu"]


@can_node
def test_CHUA_SOAT_thi_nut_NHAN_TAT_va_man_noi_ro_vi_sao():
    """⛔ *"Chưa soát"* và *"soát xong, có chặn"* đều làm nút tắt — nhưng
    chúng là **hai câu khác nhau**, và màn phải nói câu nào."""
    ra = _f04("""
      await F04.ve();
      return {tat: document.querySelector('#nap-nut-nhan').disabled,
              soat: document.querySelector('#nap-nut-soat').disabled,
              vi_sao: document.querySelector('#nap-vi-sao').textContent};
    """)
    assert ra["tat"] is True and ra["soat"] is True
    assert "bước 2" in ra["vi_sao"], ra["vi_sao"]


@can_node
def test_chon_NHIEU_nguon_thi_soat_DUNG_SO_nguon_da_TICK():
    """⭐⭐⭐ `GAP-SCR-15` **ĐÓNG** — và mối lo gốc của bài này vẫn được canh.

    ⛔⛔ Bản trước ghim hành vi *"nút `Soát` TẮT khi chọn >1 nguồn"*, vì cửa
       soát chỉ nhận **MỘT** `source_id`. Lo gốc: ⛔ **không lặng lẽ soát một
       nguồn rồi để người tưởng đã soát cả 60** — tức *"báo cáo một phép đo
       ⛔ chưa chạy"*.

    ⭐ `QĐ-ITL-111`/`112` mở cửa lô, nên hành vi đúng nay là **soát cả lô**.
      Nhưng lo gốc ⛔ **không mất** — nó chỉ đổi hình: bài này đòi thân yêu
      cầu mang **ĐÚNG số nguồn đã tick**. Gửi thiếu một nguồn cũng là *"báo
      cáo một phép đo ⛔ chưa chạy"*, chỉ khó thấy hơn.
    """
    ra = _f04(_MO_ANH + """
      const g = _GOI.filter(x => x[0] === 'ghi'
                                 && x[1] === '/nap/lo/xem-truoc');
      return {so_goi: g.length, than: g[0] ? g[0][2] : null,
              soat_tat: document.querySelector('#nap-nut-soat').disabled,
              vi_sao: document.querySelector('#nap-vi-sao').textContent};
    """, **{"/nap/lo/xem-truoc": _bb()})
    assert ra["soat_tat"] is False, "⛔ tick nguồn rồi mà nút Soát vẫn tắt"
    assert ra["so_goi"] == 1, (
        "⛔ soát cả lô phải là **MỘT** lượt gọi, ⛔ không phải N lượt: %s"
        % ra["so_goi"])
    assert ra["than"]["chup_id"] == 23719, ra["than"]
    # ⛔⛔ Đây là chỗ canh lo GỐC: **đúng số nguồn đã tick**, ⛔ không phải 1.
    assert ra["than"]["source_ids"] == [11], ra["than"]
    assert "GAP-SCR-15" not in ra["vi_sao"], (
        "⛔ màn vẫn nói GAP-SCR-15 trong khi nó đã đóng")


# ── ⑤ đã nhận ────────────────────────────────────────────────────────────
@can_node
def test_DA_NHAN_hien_run_id_va_NOI_RA_rang_chua_sang_A_CCR():
    """⛔⛔ Màn PHẢI nói ra rằng nó **dừng ở đây**.

    Im lặng thì kế toán tưởng đã xong việc, rồi vẫn phải chép tay sang
    `A-CCR` mà ⛔ **không ai nói trước** — và khâu đó đang **trễ 19 ngày**.
    """
    nap = dict(_bb(), run_id="NAP-2026-09-08-F04", vao_so=2, trung=0,
               loai=0, unmapped=2, vao_hang_cho=2)
    ra = _f04(_MO_ANH + """
      await F04._nhan();
      const o = document.querySelector('#nap-nhan');
      return {chu: o.textContent,
              nut: [...o.querySelectorAll('button')].map(b => b.textContent)};
    """, **{"/nap/lo/xem-truoc": _bb(), "/nap/lo": nap})
    assert "NAP-2026-09-08-F04" in ra["chu"]
    assert "chưa sang A-CCR" in ra["chu"]
    assert "GAP-PLAN-05" in ra["chu"]
    assert any("hàng chờ" in x for x in ra["nut"]), (
        "⛔ ⛔ không có đường sang hàng chờ để xử dòng vừa vào")


@can_node
def test_co_hang_CHAN_thi_goi__nhan_KHONG_gui_mot_yeu_cau_nao():
    """⭐⭐ Nút tắt là **hình thức**; chặn ở **hàm** mới là cơ chế.

    ⛔ Một màn chỉ tắt nút thì mọi đường khác *(gõ phím, gọi lại hàm, một lỗi
      vẽ lại)* vẫn ghi được. ⇒ `_nhan()` tự **từ chối**, ⛔ không dựa vào việc
      cái nút có bấm được ⛔ không.
    """
    luat = [_luat("S1 · ba duong can", "CHAN", False, 60)]
    luat += [_luat("S%d · x" % i, "CO", True, 8338) for i in range(2, 10)]
    ra = _f04(_MO_ANH + """
      await F04._nhan();
      return {goi: _GOI.filter(g => g[1] === '/nap').length};
    """, **{"/nap/lo/xem-truoc": _bb(chan=["S1 · ba duong can"], luat=luat)})
    assert ra["goi"] == 0, "⛔⛔ có hạng CHẶN mà màn VẪN gọi cửa `/nap`"


# ── ⛔ ba thứ màn CỐ Ý không có ───────────────────────────────────────────
@can_node
def test_man_KHONG_co_mot_O_NHAP_nao_cho_du_lieu_giao_dich():
    """⛔⛔ **`QĐ-ITL-109` trên màn hình, đo bằng MÁY.**

    `F04` ⛔ **không phải màn dán**: cử chỉ `Ctrl+V` ở lại Google Sheets. ⇒ Ô
    nhập duy nhất được phép là **ô tick chọn phạm vi**; ⛔ không một
    `input[type=text]` / `textarea` / ô `contenteditable` nào.

    ⚠ Đây là lớp lỗi mà **bản vẽ đã mắc hai lần** *(`GAP-SCR-12`)* — nên nó
      phải có **máy** canh, ⛔ không phải một lời hứa trong tài liệu.
    """
    ra = _f04(_MO_ANH + """
      await F04._nhan();
      const o = document.querySelector('#man-f04');
      return {tat_ca: o.querySelectorAll('input').map(x => x.type),
              van: o.querySelectorAll('textarea').length};
    """, **{"/nap/lo/xem-truoc": _bb(),
            "/nap/lo": dict(_bb(), run_id="R", vao_so=2, trung=0, loai=0,
                         unmapped=0, vao_hang_cho=0)})
    la = [t for t in ra["tat_ca"] if t != "checkbox"]
    assert la == [], (
        "⛔⛔ màn nạp có ô nhập ⛔ KHÔNG phải ô tick: %s — `QĐ-ITL-109` chốt "
        "cử chỉ dán ở lại Google Sheets" % la)
    assert ra["van"] == 0


@can_node
def test_man_KHONG_co_nut_day_sang_A_CCR():
    """⛔ Chặng 3 **chặn ở owner** *(`GAP-PLAN-05`)*.

    Dựng sẵn một nút chưa được phép bấm là **mời người bấm nhầm** — và cú ấy
    là một phép ghi vào **sổ kế toán đang sống**, **khó đảo**.
    """
    ra = _f04(_MO_ANH + """
      await F04._nhan();
      return document.querySelector('#man-f04')
        .querySelectorAll('button').map(b => b.textContent);
    """, **{"/nap/lo/xem-truoc": _bb(),
            "/nap/lo": dict(_bb(), run_id="R", vao_so=2, trung=0, loai=0,
                         unmapped=0, vao_hang_cho=0)})
    xau = [b for b in ra if "A-CCR" in b or "Đẩy" in b or "Gửi" in b]
    assert xau == [], "⛔ có nút đẩy sang A-CCR mà owner ⛔ chưa cho phép: %s" % xau


# ── ②b thứ tự ngày — `QĐ-ITL-113` ───────────────────────────────────────
_MO_TT = """
  await F04.ve();
  document.querySelector('[data-chup]').cells[4].children[0].onclick();
  await new Promise(r => setTimeout(r, 0));
  await new Promise(r => setTimeout(r, 0));
  await new Promise(r => setTimeout(r, 0));
"""


@can_node
def test_man_HIEN_HAI_NUT_va_nut_MAY_DE_XUAT_duoc_danh_dau():
    """⭐⭐⭐ **Hai** nút, ⛔ không phải một — và nút máy nghiêng về được đánh dấu.

    ⛔⛔ Một nút duy nhất *"Khai theo đề xuất"* là **máy quyết**, chỉ khoác áo
       một cú bấm của người. Hai nút thì **người chọn**, và họ vẫn thấy máy
       nghiêng về đâu. `QĐ-ITL-113` đặt quyền ấn định kỳ kế toán **ở người**.
    """
    ra = _f04(_MO_TT + """
      const tr = document.querySelector('[data-tt]');
      return {nut: tr.cells[3].children.map(b => [b.textContent,
                                                  b.className,
                                                  b.dataset.chon])};
    """)
    assert len(ra["nut"]) == 2, ra["nut"]
    theo = {x[2]: x for x in ra["nut"]}
    assert set(theo) == {"dmy", "mdy"}, ra["nut"]
    # ⭐ `mdy` la de xuat cua may ⇒ no mang lop nhan manh; `dmy` thi ⛔ khong.
    assert theo["mdy"][1] == "b", ra["nut"]
    assert theo["dmy"][1] != "b", ra["nut"]
    # ⛔ Nhan phai la TIENG VIET doc duoc, ⛔ khong phai ma `dmy`/`mdy`.
    assert "ngày/tháng" in theo["dmy"][0] and "tháng/ngày" in theo["mdy"][0]


@can_node
def test_man_hien_CAU_BANG_CHUNG_co_CON_SO():
    """⛔ Một cái nút kèm lời khuyên mà ⛔ không kèm phép đo sẽ được bấm mà
    ⛔ không ai đọc — lúc ấy *"người ấn định"* chỉ là một câu trong tài liệu."""
    ra = _f04(_MO_TT + """
      return document.querySelector('[data-tt]').cells[2].innerHTML;
    """)
    assert "1263" in ra and "mdy" in ra, ra


@can_node
def test_CHUA_KHAI_hien_chu_CHUA_KHAI__khong_hien_o_TRONG():
    """⛔⛔ Một ô trống đọc y hệt một ô *"⛔ không áp dụng"*.

    Cùng luật với `da_do = 0` của biên bản và ô `dat = null` của `F03`.
    """
    ra = _f04(_MO_TT + """
      return document.querySelector('[data-tt]').cells[1].innerHTML;
    """)
    assert "chưa khai" in ra and "crit" in ra, ra


@can_node
def test_MAU_THUAN_thi_man_NOI_RA_rang_may_KHONG_de_xuat_duoc():
    """⛔ Nguồn có CẢ hai bằng chứng ⇒ ⛔ không thứ tự nào đúng cho cả nguồn.

    ⛔ Lặng lẽ ⛔ không đánh dấu nút nào thì kế toán ⛔ không có cách nào phân
      biệt *"máy ⛔ không đề xuất được"* với *"máy chưa đo"*.
    """
    ra = _f04(_MO_TT + """
      const tr = document.querySelectorAll('[data-tt]')[1];
      /* DOM gia ⛔ khong phan tich `innerHTML` ⇒ o dung `appendChild` la
         RONG. Doc tung con.                                              */
      return {o: tr.cells[3].children
                   .map(c => (c.textContent || '') + (c.innerHTML || ''))
                   .join(' | '),
              nut: tr.cells[3].children.map(b => b.className)};
    """)
    assert "không đề xuất được" in ra["o"], ra
    assert "b" not in ra["nut"], (
        "⛔ mâu thuẫn mà VẪN đánh dấu một nút ⇒ máy đang đề xuất thứ nó vừa "
        "nói là ⛔ không đề xuất được")


@can_node
def test_nguon_KHONG_CAN_KHAI_van_co_mat__nhung_KHONG_bi_doi_khai():
    """⛔ Đòi khai một nguồn ⛔ không mơ hồ = bắt trả lời câu ⛔ không tồn tại.

    ⛔ Nhưng lọc nó khỏi bảng thì kế toán ⛔ không có cách nào biết máy **đã
      soi** nguồn ấy — đúng lớp lỗi nguồn-ra-0-dòng của `fls_chup_nguon`.
    """
    ra = _f04(_MO_TT + """
      const t = document.querySelectorAll('[data-tt]');
      return {so_dong_bang: t.length,
              ten: t.map(tr => tr.cells[0].innerHTML).join(' | '),
              ghi_chu: document.querySelector('#nap-thu-tu')
                .children.map(c => c.innerHTML).join(' | ')};
    """)
    # ⛔ Bang CHI chua nguon can khai — 21 dong noi *"khong can"* la nhieu.
    assert ra["so_dong_bang"] == 2, ra["so_dong_bang"]
    assert "Toan_ngay_so" not in ra["ten"], ra["ten"]
    # ⭐ Nhung no PHAI hien o mot ghi chu rieng — cung khuon *"nguon doc ra
    #   0 dong"* o tren. Loc hoan toan thi ke toan ⛔ khong co cach nao biet
    #   may **da soi** nguon ay.
    assert "1 nguồn không cần khai" in ra["ghi_chu"], ra["ghi_chu"][:400]
    assert "Toan_ngay_so" in ra["ghi_chu"], ra["ghi_chu"][:400]


@can_node
def test_man_noi_HE_QUA_bang_CON_SO__khong_canh_bao_chung_chung():
    """⭐⭐ *"Có thể một số dòng sẽ bị loại"* ⛔ KHÔNG giúp ai quyết định gì.

    Màn phải nói **đúng bao nhiêu dòng** của **lần đọc này** sẽ vào hàng loại
    nếu nạp mà chưa khai — `905 + 59 = 964`.
    """
    ra = _f04(_MO_TT + """
      /* DOM gia ⛔ khong phan tich `innerHTML`, nen `innerHTML` cua mot
         thung dung bang `appendChild` la RONG. ⇒ doc tung con.          */
      return document.querySelector('#nap-thu-tu')
        .children.map(c => c.innerHTML).join(' | ');
    """)
    assert "964" in ra, ra[:600]
    assert "2 nguồn chưa khai" in ra, ra[:600]
    # ⛔ Va phai noi ro cac dong CON LAI VAN vao so — ⛔ khong de nguoi doc
    #    tuong ca lo bi chan (dung hanh vi ma `QĐ-ITL-113` vua LAT).
    assert "vẫn vào sổ" in ra, ra[:600]


@can_node
def test_BAM_khai_goi_dung_cua_RIENG__khong_goi_khai_cot():
    """⛔⛔ Gọi `POST …/khai-cot` từ màn là mở một chu trình **đọc-sửa-ghi**.

    Ai khai `cot` mới trong khe giữa hai lượt sẽ bị **đè lại bằng `cot` CŨ**,
    mà `version` vẫn tăng ⇒ ⛔ không cổng nào thấy.
    """
    ra = _f04(_MO_TT + """
      const tr = document.querySelector('[data-tt]');
      const b = tr.cells[3].children.filter(x => x.dataset.chon === 'mdy')[0];
      b.onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return _GOI.filter(g => g[0] === 'ghi');
    """)
    assert len(ra) == 1, ra
    assert ra[0][1] == "/sources/1/thu-tu", ra
    assert ra[0][2] == {"thu_tu": "mdy"}, ra


@can_node
def test_nut_GOP_gui_dung_nguon_TU_CHUNG__va_KHONG_gui_thu_tu():
    """⭐⭐⭐ `QĐ-ITL-117` — và mối lo gốc của bài này **vẫn được canh nguyên**.

    ⛔⛔ Bản trước ghim *"màn ⛔ KHÔNG có nút khai tất cả"*, lý lẽ là: *"một nút
       gộp là một nút được bấm mà ⛔ không ai đọc"*. Lo ấy **đúng** và ⛔ không
       mất — nó chỉ đổi hình sau một phép đo: **34/34** nguồn chuỗi của ảnh
       `23719` **tự chứng minh** thứ tự bằng dữ liệu của chính nó *(0 nguồn
       `dmy`, 0 mâu thuẫn)* ⇒ máy đề xuất **34 lần một đáp án**. Bắt người bấm
       27 cú để trả lời một câu dữ liệu đã tự trả lời là bắt họ **bấm theo phản
       xạ** — tức đúng cái lo cũ, chỉ tốn thêm 26 cú.

    ⇒ Nút gộp được phép tồn tại, nhưng **hai điều kiện là bất di dịch**, và
      bài này ghim cả hai:
        ⓐ thân yêu cầu **⛔ KHÔNG mang `thu_tu`** — nếu nó mang, màn trở thành
           cỗ máy khai `dmy` cho 27 nguồn bằng một cú bấm *(cửa cũng NỔ 400,
           nhưng một cổng ở tầng màn thì thấy sớm hơn một cổng ở tầng cửa)*;
        ⓑ nó gửi **chỉ** nguồn tự chứng — nguồn `Tron_hai_kieu` *(mâu thuẫn:
           4 dòng `dmy` **và** 6 dòng `mdy`)* ⛔ **không được** có trong lô.
    """
    ra = _f04(_MO_TT + """
      const b = document.querySelector('#nap-nut-thu-tu-lo');
      b.onclick();
      await new Promise(r => setTimeout(r, 0));
      await new Promise(r => setTimeout(r, 0));
      return {nhan: b.textContent,
              ghi: _GOI.filter(g => g[0] === 'ghi')};
    """)
    assert len(ra["ghi"]) == 1, ra["ghi"]
    duong, than = ra["ghi"][0][1], ra["ghi"][0][2]
    assert duong == "/chup/23719/thu-tu", duong
    assert "thu_tu" not in than, (
        "⛔⛔ màn gửi `thu_tu` trong cú bấm gộp ⇒ nó đang CHỌN HỘ thứ tự cho "
        "27 nguồn: %s" % than)
    assert than == {"source_ids": [1]}, (
        "⛔ lô phải chứa ĐÚNG nguồn tự chứng — nguồn mâu thuẫn (id 2) ⛔ không "
        "được vào, nguồn ⛔ không cần khai (id 3) cũng ⛔ không: %s" % than)
    assert "1 nguồn" in ra["nhan"], (
        "⛔ nhãn nút ⛔ không nói nó sắp khai bao nhiêu nguồn: %r" % ra["nhan"])


@can_node
def test_nut_GOP_mang_BA_con_so__khong_phai_mot_loi_moi_tron():
    """⛔⛔ *"Khai theo bằng chứng"* một mình là một cái nút **⛔ không kiểm lại
       được**: `mdy` dựa trên 1.263 dòng làm chứng và `mdy` đoán từ hư không
       **⛔ trông y hệt nhau** trên mặt nút.

    ⇒ Khối phải nói cả ba: bao nhiêu **nguồn** · bao nhiêu dòng **tự nói ra**
      thứ tự · bao nhiêu dòng mơ hồ **nhờ** bản khai ấy mà vào sổ. Con số thứ
      ba là **hậu quả** — thiếu nó thì cú bấm ⛔ không có lý do đọc được.
    """
    ra = _f04(_MO_TT + """
      return document.querySelector('#nap-thu-tu')
        .children.map(c => c.innerHTML).join(' | ');
    """)
    assert "1 nguồn tự chứng" in ra, ra[:800]
    assert "1.263 dòng" in ra, (
        "⛔ ⛔ không nói ĐÃ SOI bao nhiêu dòng làm chứng: %s" % ra[:800])
    assert "905 dòng" in ra, (
        "⛔ ⛔ không nói cú bấm ấy CỨU được bao nhiêu dòng: %s" % ra[:800])


@can_node
def test_nguon_KHONG_TU_CHUNG_bi_NOI_TEN_va_o_NGOAI_cu_bam_gop():
    """⛔ Nguồn mâu thuẫn vắng mặt khỏi lô gộp **trong im lặng** thì con số
      trên nút nhỏ hơn số nguồn đang chờ khai, mà ⛔ không ai được nói vì sao.
    """
    ra = _f04(_MO_TT + """
      return document.querySelector('#nap-thu-tu')
        .children.map(c => c.innerHTML).join(' | ');
    """)
    assert "1 nguồn không tự chứng" in ra, ra[:900]
    assert "Tron_hai_kieu" in ra, ra[:900]
    assert "từng nguồn" in ra, (
        "⛔ ⛔ không chỉ ra đường ĐI TIẾP cho nguồn ấy: %s" % ra[:900])


# ── ④b biên bản GỘP — `QĐ-ITL-112` ──────────────────────────────────────
_BB_GOP = _bb(
    co=["S7 · x"],
    luat=[_luat("S1 · ba duong can", "CHAN", True, 60),
          _luat("S2 · co tien thi phai co MA", "CO", True, 8365),
          _luat("S3 · moi dong phai co TIEN", "CO", True, 8365,
                chua_do=["R | Rong1", "R | Rong2"]),
          _luat("S4 · moi dong phai co TIEN TE", "CO", True, 8365),
          _luat("S5 · ma khong bi ha kieu", "CANH", True, 8365),
          _luat("S6 · mot sheet mot kieu ngay", "CANH", True, 50),
          _luat("S7 · dong trung HOAN TOAN", "CO", False, 8365,
                khong_dat=["R | Trung1", "R | Trung2", "R | Trung3"]),
          _luat("S8 · xuat xu co trong danh muc", "CO", True, 60),
          _luat("S10 · hai ban khai tro CUNG mot cot", "CHAN", False, 3,
                khong_dat=["R | ThieuDai"])],
    nguon=[_nguon_bb("R | AAA_MSB VND_CN"),
           _nguon_bb("R | ThieuDai", bi_chua=True,
                     chua_vi=["S10 · hai ban khai tro CUNG mot cot"]),
           _nguon_bb("R | ChuaKhaiNgay", thu_tu=None)],
    so_nguon_chua=1)


def _f04_gop(kich_ban):
    return _f04(_MO_ANH + kich_ban, **{"/nap/lo/xem-truoc": _BB_GOP})


@can_node
def test_DAI_DAU_noi_NGUON_truoc_moi_con_so_DONG():
    """⛔⛔ Câu kế toán hỏi là *"lô này vào được ⛔ không, cái gì cản"*.

    Một biên bản mở đầu bằng *"8.365 dòng"* mà để *"1 nguồn bị chừa"* ở cuối
    là một biên bản **trả lời đúng câu ⛔ không ai hỏi** *(`QĐ-ITL-112`)*.
    """
    ra = _f04_gop("""
      return document.querySelector('#nap-bb')
        .children.map(c => c.innerHTML).join(' | ');
    """)
    assert "2 nguồn vào sổ" in ra and "1 nguồn bị chừa" in ra, ra[:400]
    # ⭐ Và nó phải nói các nguồn còn lại VẪN vào — ⛔ không để người đọc
    #   tưởng cả lô bị chặn (đúng hành vi mà `QĐ-ITL-111` vừa LẬT).
    assert "vẫn vào" in ra, ra[:400]


@can_node
def test_moi_luat_bung_ra_NGUON_DINH__khong_chi_mot_con_so():
    """⛔ Một dòng nói *"3 nguồn ⛔ không đạt"* mà ⛔ không nói **nguồn nào**
    thì kế toán ⛔ không có bước kế tiếp nào để làm."""
    ra = _f04_gop("""
      const tr = document.querySelectorAll('[data-hang]');
      const s7 = tr.filter(x => x.cells[1].innerHTML.indexOf('S7') >= 0)[0];
      const b = s7.cells[4].children[0];
      b.onclick();
      const bung = s7.parentNode.children
        .filter(x => x.dataset && x.dataset.bung_cua)
        .map(x => x.cells[0].innerHTML).join(' ');
      return {nut: b.textContent, bung: bung};
    """)
    assert ra["nut"] == "3 nguồn", ra["nut"]
    for x in ("Trung1", "Trung2", "Trung3"):
        assert x in ra["bung"], (x, ra["bung"][:300])


@can_node
def test_nguon_CHUA_DO_hien_RIENG__khong_ke_thanh_khong_dat():
    """⛔⛔ 10/60 nguồn thật đọc ra 0 dòng — ⛔ **không phải khuyết tật**.

    Kể chúng thành *"⛔ không đạt"* là **báo oan**, và một báo động đỏ oan là
    một báo động **sẽ bị bỏ qua**.
    """
    ra = _f04_gop("""
      const tr = document.querySelectorAll('[data-hang]');
      const s3 = tr.filter(x => x.cells[1].innerHTML.indexOf('S3') >= 0)[0];
      return {ket_qua: s3.cells[2].innerHTML, dinh: s3.cells[4].innerHTML};
    """)
    assert "đạt" in ra["ket_qua"] and "không đạt" not in ra["ket_qua"], ra
    assert "2 chưa đo" in ra["dinh"], ra["dinh"]


@can_node
def test_bang_TUNG_NGUON_neu_RO_luat_nao_chua_nguon_nao():
    """⭐⭐⭐ `QĐ-ITL-111`: chừa mà ⛔ không nói vì sao thì kế toán ⛔ không có
    đường nào sửa — và cú bỏ tick lại quay về **⛔ không để lại vết**."""
    ra = _f04_gop("""
      const t = document.querySelectorAll('[data-ngbb]');
      return t.map(tr => [tr.cells[0].innerHTML, tr.cells[1].innerHTML,
                          tr.cells[3].innerHTML, tr.cells[4].innerHTML]);
    """)
    assert len(ra) == 3, ra
    chua = [r for r in ra if "bị chừa" in r[1]]
    assert len(chua) == 1, ra
    assert "ThieuDai" in chua[0][0]
    assert "S10" in chua[0][3], (
        "⛔ nguồn bị chừa mà ⛔ KHÔNG nói luật nào chừa nó")
    # ⛔ `thu_tu` rỗng hiện **thành chữ**, ⛔ không hiện ô trống.
    ck = [r for r in ra if "ChuaKhaiNgay" in r[0]][0]
    assert "chưa khai" in ck[2], ck


@can_node
def test_NHAN_goi_cua_LO_kem_source_ids__khong_goi_cua_mot_nguon():
    """⛔ Hai đường (một-nguồn / cả-lô) là **hai chỗ để chúng lệch nhau**, và
    cái lệch ấy hiện ra dưới dạng *"soát thấy 9 luật xanh, nạp ra số khác"*."""
    nap = dict(_BB_GOP, run_id="NAP-2026-09-08-F04", vao_so=2, trung=0,
               loai=0, unmapped=0, vao_hang_cho=1)
    ra = _f04(_MO_ANH + """
      await F04._nhan();
      return _GOI.filter(x => x[0] === 'ghi').map(x => [x[1], x[2]]);
    """, **{"/nap/lo/xem-truoc": _BB_GOP, "/nap/lo": nap})
    duong = [x[0] for x in ra]
    assert "/nap/lo" in duong, duong
    assert "/nap" not in duong and "/nap/xem-truoc" not in duong, duong
    than = [x[1] for x in ra if x[0] == "/nap/lo"][0]
    assert than["source_ids"] == [11], than
    assert than["chup_id"] == 23719 and than["run_id"].startswith("NAP-"), than


# ── ⑧ THU TU TREN MAN — do bang mat NGUOI DUNG, 08/09 ───────────────────
@can_node
def test_nut_NHAN_dung_SAU_bien_ban__khong_dung_TRUOC(tmp_path=None):
    """⭐⭐⭐ Một nút phải đứng **SAU** cái nó phụ thuộc.

    ⛔⛔ Trước 08/09 `Soát` và `Nhận` nằm **cạnh nhau, TRÊN** Bước 3. Muốn
       `Nhận` thì phải đọc biên bản *(bên dưới)* rồi **cuộn NGƯỢC LÊN** để
       bấm — với 60 nguồn đó là một cuộn dài, và **cú bấm phải cuộn ngược
       lại đúng là cú ghi vào sổ kế toán**.

    ⇒ Bài này đo **thứ tự trong tài liệu HTML**, ⛔ không đo pixel: `Soát`
      phải **trước** `#nap-bb` *(nó **sinh ra** biên bản)*, `Nhận` phải
      **sau** *(nó **tiêu thụ** biên bản)*.
    """
    import pathlib
    h = (pathlib.Path(__file__).resolve().parents[2]
         / "fls" / "web" / "tep" / "index.html").read_text(encoding="utf-8")
    i_soat = h.index('id="nap-nut-soat"')
    i_bb = h.index('id="nap-bb"')
    i_nhan = h.index('id="nap-nut-nhan"')
    assert i_soat < i_bb, "⛔ nút Soát phải đứng TRƯỚC biên bản nó sinh ra"
    assert i_bb < i_nhan, (
        "⛔⛔ nút Nhận đứng TRƯỚC biên bản ⇒ người dùng phải cuộn xuống đọc "
        "rồi cuộn NGƯỢC LÊN để bấm — và cú bấm ấy ghi vào sổ")


@can_node
def test_so_BUOC_la_MOT_DAY_lien_tuc__khong_nhay_khong_thieu():
    """⛔ `1 · (không số) · 2 · (không số) · 2b · 3 · 4` ⛔ không phải một dãy.

    ⭐ Bộ này đã bị cắn đúng lớp lỗi ấy: *"hai dòng cùng số `17`"* ở
      `06 §6.-1` ⇒ **số thứ tự ⛔ không tự nó là danh tính**. Một người đếm
      *"màn này mấy bước"* phải có câu trả lời.

    ⇒ Panel *(bản khai · xem trước · cách đọc ngày)* **⛔ không được** mang
      số bước — chúng là bảng mở ra khi cần, ⛔ không phải một chặng.
    """
    import pathlib
    import re
    h = (pathlib.Path(__file__).resolve().parents[2]
         / "fls" / "web" / "tep" / "index.html").read_text(encoding="utf-8")
    i = h.index('id="man-f04"')
    k = h.find('id="man-f06"', i)
    so = re.findall(r"<h3>Bước ([^ ·]+)", h[i:k if k > 0 else len(h)])
    assert so == ["1", "2", "3", "4"], (
        "⛔ số bước ⛔ không phải một dãy liên tục: %s" % so)
