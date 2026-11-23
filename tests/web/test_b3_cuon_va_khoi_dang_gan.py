# -*- coding: utf-8 -*-
"""`B3` — hai gop y `23/09` (vong ba):

  `1` bam mot giao dich ⇒ **danh sach nhay ve dau**
  `2` lenh **da gan** phai hien **giao dich no dang gan voi** *(`C4 .mblock`)*

⭐⭐ `1` la mot lỗi **toi gay ra**: `ve()` dung lai **toan bo** cay DOM moi
   lan, nen `scrollTop` cua moi hop cuon ve `0`. No ⛔ khong lo ra suot ba
   vong vi **truoc `23/09` hop ⛔ khong tu cuon** — ca trang cuon, va trinh
   duyet tu giu vi tri trang. Toi vua cho `.cands` cuon rieng *(vong 2)*, va
   **ngay do** sinh ra lỗi nay. Mot phep sua mo ra mot lỗi moi ⇒ phai co mot
   bai thu moi di kem.

⛔⛔ `2` la khoi `C4` cua hop dong *(`BA-06 §4 C4`)* — **⛔ chua bao gio duoc
   lam**. Man hien `Da gan` tren the, ⛔ nhung ⛔ khong noi **gan voi dong
   tien NAO** ⇒ ke toan mo mot lenh da xong ma van phai doan.
"""
from __future__ import annotations

import io
import json

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.web.ca_wo032 import dung_ca, goi_ok
from tests.web.khung_node import _chay
from tests.web.test_vong_f02_pg import _may
from tests.web.test_b3_uiux_theo_gop_y_owner import TEP, VO, _the, _css_f01
from tests.web.test_b3_uiux_vong_hai import TEP_JS, _khoi, _uv

D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"

#: ⭐ Mot giao dich DA GAN, dung khuon `khuon_ung_vien` cua cua.
#: ⛔⛔ `WO-032` (c) *(`KQ-031 F-3`)*: khuôn này **từng** mang một khoá tô bằng
#:    chứng do bài **tự đặt** *(`["LUONG"]`)* — trong khi `the.gd` của cửa thật
#:    ⛔ bao giờ trả khoá ấy *(sổ thật **0 / 768**)* ⇒ khối *"Đang gán"* ⛔ bao
#:    giờ tô `<mark>` mà bài vẫn xanh: **lần thứ ba** của lớp *"khuôn thử tự
#:    nhét"*. Đã gỡ; bài tô bằng chứng bên dưới lấy thân từ **cửa thật**.
GD = {"itl_id": 28338, "doc_date": "2025-02-19", "doc_no": "FT25050099388714",
      "dien_giai": "TT LUONG THANG 1.2025 ID 515", "amount": "29211750.00",
      "curr": "VND", "chieu": "co", "bac": "ma", "lech": None,
      "nguon": {"tk": "••0305", "bank": "VPB", "curr": "VND",
                "le": "VISIONLAB"},
      "da_gan": True}


def _the_da_gan(ma, ds=None, gd_ds=None, **doi):
    t = _the(ma, trang_thai="da_gan", trang_thai_nhan="Đã gán",
             trang_thai_mau="good", **doi)
    t["itl_da_gan"] = ds if ds is not None else [28338]
    t["gd"] = dict(GD)
    t["gd_ds"] = gd_ds if gd_ds is not None else [dict(GD)]
    return t


def _dat(rows, duong=D_NGUOI):
    return ("_TRA[" + json.dumps(duong) + "] = " + json.dumps(
        {"data": {"rows": rows, "next_cursor": None}}, ensure_ascii=False)
        + ";_TRA[" + json.dumps(D_MAY) + "] = "
        + json.dumps({"data": {"rows": [], "next_cursor": None}}) + ";")


def _mo(ma, rows, uv=None):
    ds = uv if uv is not None else [_uv(0), _uv(1), _uv(2)]
    return (_dat(rows)
            + "_TRA['/queue/lenh/" + ma + "/itl-candidates'] = "
            + json.dumps({"data": {"ung_vien": ds}}, ensure_ascii=False) + ";"
            "_TRA['/queue/lenh/" + ma + "/so'] = {data: {ung_vien: []}};"
            " await F01G.mo_man(); await F01G.mo_lenh('" + ma + "');")


# ══ `1` bam mot giao dich ⇒ danh sach ⛔ KHONG duoc nhay ve dau ═════════

def test_BAM_mot_giao_dich_thi_danh_sach_DUNG_YEN():
    """Owner `23/09`: *"nhan chon 1 Transaction, danh sach bi scroll ve dau"*.

    ⛔⛔ `ve()` dung lai **toan bo** cay DOM ⇒ `scrollTop` ve `0`. Ke toan
       cuon xuong dong thu `40`, bam chon, va **mat cho minh dang dung** —
       roi phai cuon lai tu dau de tim tiep. Voi `1.800` ung vien Toan so
       thi do ⛔ khong phai mot phien toai, do la **⛔ khong dung duoc**.
    """
    r = _chay(_mo("PM1-1", [_the("PM1-1"), _the("PM2-1")])
              + " const ds = document.querySelector('.cands');"
              " ds.scrollTop = 420;"
              # ⛔ `_ban()` chi toi duoc listener o **`document`**; dong ung
              #   vien nghe o **chinh phan tu** ⇒ goi qua `_nghe`, dung cach
              #   `test_b3_bang_chung_va_du_xuong` da dung.
              " const d1 = document.querySelectorAll('.cand')[1];"
              " d1._nghe.click[0]({target: d1});"
              " return {sau: document.querySelector('.cands').scrollTop,"
              "         chon: F01G.ST.ung_vien_chon};",
              tep=TEP, vo=VO)
    assert r["chon"] == 1, "⛔ cú bấm ⛔ không chọn được ứng viên"
    assert r["sau"] == 420, (
        "⛔⛔ Danh sách nhảy về **%s** — kế toán mất chỗ mình đang đứng"
        % r["sau"])


def test_RAIL_cung_DUNG_YEN_khi_doi_lenh():
    """⛔ Rail cung cuon rieng tu truoc — cung mot lỗi, cung mot phep sua.
    ⚠ Doi lenh thi rail **giu cho**, vi nguoi ta dang lam doc theo danh sach
    ay; nhay ve dau la bat ho tim lai dong vua bam."""
    rows = [_the("PM%d-1" % i) for i in range(1, 6)]
    r = _chay(_mo("PM1-1", rows)
              + " document.querySelector('.rail').scrollTop = 260;"
              " F01G.ve();"
              " return document.querySelector('.rail').scrollTop;",
              tep=TEP, vo=VO)
    assert r == 260, f"⛔ rail nhảy về **{r}**"


def test_BANG_SO_cung_giu_cho_khi_ve_lai():
    r = _chay(_dat([_the("PM1-1"), _the("PM2-1")])
              + " await F01G.mo_man();"
              " document.querySelector('.tablescroll').scrollTop = 900;"
              " F01G.ve();"
              " return document.querySelector('.tablescroll').scrollTop;",
              tep=TEP, vo=VO)
    assert r == 900, f"⛔ bảng sổ nhảy về **{r}**"


def test_MO_MOT_LENH_KHAC_thi_danh_sach_giao_dich_VE_DAU():
    """⭐⭐ Giu cho la dung — ⛔ **nhung ⛔ khong phai luon luon**. Doi sang
    mot lenh KHAC thi danh sach ung vien la **mot danh sach khac han**; giu
    `scrollTop = 420` o day se mo ra giua mot danh sach moi, va nguoi ta
    ⛔ khong biet minh dang o dau.

    ⇒ Luat: giu cho khi **ve lai cung mot canh**, ve dau khi **doi canh**."""
    r = _chay(_mo("PM1-1", [_the("PM1-1"), _the("PM2-1")])
              + "_TRA['/queue/lenh/PM2-1/itl-candidates'] = "
              + json.dumps({"data": {"ung_vien": [_uv(3), _uv(4)]}}) + ";"
              "_TRA['/queue/lenh/PM2-1/so'] = {data: {ung_vien: []}};"
              " document.querySelector('.cands').scrollTop = 420;"
              " await F01G.mo_lenh('PM2-1');"
              " return document.querySelector('.cands').scrollTop;",
              tep=TEP, vo=VO)
    assert r == 0, (
        "⛔ Đổi sang lệnh khác mà danh sách vẫn ở **%s** — mở ra giữa một "
        "danh sách hoàn toàn khác" % r)


# ══ `2` khoi `C4` — lenh DA GAN phai noi no gan voi giao dich NAO ═══════

def test_LENH_DA_GAN_hien_KHOI_DANG_GAN():
    """Owner `23/09`: *"toi muon cac PM da gan khi bam vao co hien thong tin
    Transaction da map"*. Do la **`C4`** cua hop dong (`BA-06 §4`), va no
    **⛔ chua bao gio duoc lam**.

    ⛔⛔ Truoc do man chi hien chip `Da gan` tren the — tuc no noi *"viec nay
       xong roi"* ma ⛔ **khong noi xong bang gi**. Ke toan mo mot lenh da
       gan ra thi thay mot danh sach `20` ung vien do may de xuat, va ⛔
       khong mot dau hieu nao chi ra dong nao trong so do *(hoac dong nao
       ⛔ ngoai so do)* dang duoc gan."""
    r = _chay(_mo("PM1-1", [_the_da_gan("PM1-1"), _the("PM2-1")])
              + " const m = document.querySelector('.mblock');"
              " return {co: !!m, chu: m ? m.textContent : '',"
              "         bo: !!(m && m.querySelector('.mh button'))};",
              tep=TEP, vo=VO)
    assert r["co"], "⛔ ⛔ không có khối `C4` cho lệnh đã gán"
    # ⛔ DOM gia tra ca the `<mark>` trong `textContent` — bo chung ra, phep
    #   to bang chung da co bai rieng.
    chu = r["chu"].replace("<mark>", "").replace("</mark>", "")
    r["chu"] = chu
    for phai in ("Đang gán với giao dịch", "TT LUONG THANG 1.2025",
                 "FT25050099388714", "VPB", "29.211.750", "VND",
                 "2025-02-19"):
        assert phai in r["chu"], (
            "⛔ Khối `C4` thiếu **%r** — hợp đồng `§4 C4` đòi: bậc · diễn "
            "giải nguyên văn · ngày · nguồn · số CT · số tiền" % phai)
    assert r["bo"], "⛔ ⛔ không có nút `bỏ gán` ngay trên khối"


@pytest.mark.pg
def test_KHOI_DANG_GAN_TO_BANG_CHUNG_nhu_dong_ung_vien():
    """⭐ Cung mot *"bang chung"* thi phai **trong giong nhau** o moi cho no
    xuat hien — ⛔ khong mot kieu o danh sach, mot kieu o khoi da gan.

    ⭐ *(`WO-032` (c) — viết lại, **giữ nguyên lo gốc**)*: bản cũ dựng thân
      bằng `GD` tự nhét khoá tô `["LUONG"]` ⇒ xanh suốt khi cửa thật ⛔ trả
      khoá ấy *(`KQ-031 F-3`)*. Nay thân lấy từ **cửa thật** `lenh-da-gan`
      trên kho TEST *(ca `tests/web/ca_wo032.py`: lệnh `B` đã gán, diễn giải
      sao kê chứa số CT)*; ⛔ một khoá do bài đặt. ⛔ Chiều ĐỎ *(`a718142`)*:
      `gd` ⛔ mang khoá tô ⇒ ⛔ `<mark>`."""
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        ca = dung_ca(c)
    ma = ca["lenh"]["B"]
    duong = ["/queue/lenh-da-gan?limit=500", "/queue/lenh/%s/itl-candidates" % ma]
    with _may() as m:
        tra = {d: goi_ok(m, d)["data"] for d in duong}
    r = _chay("const TRA = %s; for (const k of Object.keys(TRA))"
              " _TRA[k] = {data: TRA[k]};" % json.dumps(tra, default=str)
              + " await F01G.doi_chip('da_gan'); await F01G.mo_lenh(%s);"
              % json.dumps(ma)
              + " const m = document.querySelector('.mblock .mdg');"
              " return m ? m.innerHTML : '';",
              tep=TEP, vo=VO)
    assert "<mark>" in r, (
        "⛔ Diễn giải trong khối `C4` ⛔ không tô bằng chứng: %r" % r[:90])
    assert ("<mark>%s</mark>" % ca["doc"]["B"]) in r, r


def test_KHOI_DANG_GAN_KHONG_hien_voi_lenh_CHUA_GAN():
    """⛔ Mot khoi *"dang gan voi"* hien tren mot lenh **chua gan** la mot
    cau **noi doi** — va no noi doi o dung cho ke toan tin nhat."""
    r = _chay(_mo("PM1-1", [_the("PM1-1")])
              + " return document.querySelectorAll('.mblock').length;",
              tep=TEP, vo=VO)
    assert r == 0, f"⛔ hiện **{r}** khối trên một lệnh chưa gán"


def test_CHUM_hien_DU_moi_dong_tien_chu_KHONG_chi_dong_dau():
    """⭐⭐ Do `23/09` tren `2.219` lenh da gan: **`23` (`1,0%`)** gan nhieu
    hon mot dong tien, nhieu nhat **`7`**.

    ⛔⛔ Mot `1,0%` **⛔ khong phai co de bo qua** — no la co de **⛔ khong
       bay hop thoai xac nhan** *(`QĐ-ITL-148 ⓔ`)*, ⛔ khong phai co de
       **giau mat sau dong tien**. Hien dong dau va im ve `6` dong con lai
       thi man dang **noi sai** ve mot phep gan that."""
    hai = [dict(GD), dict(GD, itl_id=28339, doc_no="FT25050099388715",
                          dien_giai="TT LUONG THANG 2.2025 ID 516",
                          amount="12000000.00")]
    r = _chay(_mo("PM1-1", [_the_da_gan("PM1-1", ds=[28338, 28339],
                                        gd_ds=hai)])
              + " return {n: document.querySelectorAll('.mblock').length,"
              "         chu: document.querySelector('.work').textContent};",
              tep=TEP, vo=VO)
    assert r["n"] == 2, f"⛔ chùm **2** dòng tiền mà chỉ vẽ **{r['n']}** khối"
    assert "FT25050099388715" in r["chu"], "⛔ thiếu dòng tiền thứ hai"


def test_CUA_cho_DU_moi_dong_tien_da_gan_chu_KHONG_chi_dong_dau():
    """⛔⛔ Man ⛔ khong the ve thu ma cua ⛔ khong cho. `_gan_gd` xua chi lay
    `ds[0]` ⇒ voi mot chum `7` dong, cua noi ve **mot**.

    ⚠ Bai nay do o tang MA — no chi hoi *"cua co gui `gd_ds` ⛔ khong"*; phep
    do that nam o `tests/api/test_cua_lenh_cho_pg.py`."""
    ma = io.open("fls/api/xu_ly.py", encoding="utf-8").read()
    assert "gd_ds" in ma, (
        "⛔ Cửa ⛔ không gửi `gd_ds` — màn ⛔ không có gì để vẽ cho một chùm")


def test_KHOI_DANG_GAN_dung_MOT_luat_mau_voi_chip_da_gan():
    """⛔ Khoi nay la *"viec da xong"* ⇒ nen `good`, ⛔ khong `warn`. Man da
    co mot luat mau cho *"da chot"* ／ *"de xuat"* (`§6.3`) — bia them mot
    mau thu ba la lam moi cai cu mat nghia."""
    t = _khoi(_css_f01(), ".mblock{")
    assert "--good" in t, (
        "⛔ Khối `C4` ⛔ không dùng màu `good` — mà nó là *đã chốt*")


# ══ `3` CHUM: bac tung dong noi SAI ve ca chum ═════════════════════════

def test_CHUM_noi_TONG_va_no_co_KHOP_hay_khong():
    """⭐⭐⭐ Do `23/09` tren cua that, `PM00001-1`:

        itl_da_gan = [28338, 28339]
        29.211.750 ＋ 40.513.971 = **69.725.721**  ≡ so tien lenh

    ⇒ Chum ay la mot phep khop **chinh xac o TONG**. ⛔⛔ Nhung `_bac` tinh
      **tung dong mot**, nen ca hai deu ra `cung_tien_te` — **bac yeu nhat**.
      Man ve hai khoi `④` canh nhau thi ke toan doc duoc *"hai phep gan yeu"*,
      trong khi su that la *"mot phep gan khop dung den tung dong"*.

    ⭐ Sua **⛔ khong phai o `_bac`** — bac cua mot dong tien so voi mot dong
      lenh van dung nhu the. Sua o cho **noi ra cai ma tung dong ⛔ khong noi
      duoc**: mot dong TONG, va mot cau *"khop"* / *"lech"*.
    """
    hai = [dict(GD, amount="29211750.00"),
           dict(GD, itl_id=28339, doc_no="FT25050099388715",
                dien_giai="VISIONLAB TT CP bao hiem PTI", amount="40513971.00")]
    r = _chay(_mo("PM1-1", [_the_da_gan("PM1-1", ds=[28338, 28339],
                                        gd_ds=hai,
                                        so_tien="69725721.00", curr="VND")])
              + " const t = document.querySelector('.mtong');"
              " return t ? t.textContent : null;",
              tep=TEP, vo=VO)
    assert r, "⛔ Chùm ⛔ không có dòng TỔNG"
    assert "69.725.721" in r, f"⛔ tổng sai: {r!r}"
    assert "khớp" in r.lower(), (
        "⛔ ⛔ Không nói tổng ấy **có khớp số tiền lệnh hay không** — mà đó "
        "đúng là điều bậc từng dòng ⛔ không nói được: %r" % r)


def test_MOT_giao_dich_thi_KHONG_ve_dong_TONG():
    """⛔ Tong cua **mot** so la chinh no. Mot dong *"Tong: 29.211.750"* duoi
    dung con so `29.211.750` la mot dong **⛔ khong noi gi**, va no day khoi
    nay xuong mot dong o **99,0%** so lenh."""
    r = _chay(_mo("PM1-1", [_the_da_gan("PM1-1")])
              + " return document.querySelectorAll('.mtong').length;",
              tep=TEP, vo=VO)
    assert r == 0, f"⛔ vẽ **{r}** dòng tổng cho một giao dịch duy nhất"


def test_TONG_LECH_thi_noi_LECH_bao_nhieu():
    hai = [dict(GD, amount="1000.00"), dict(GD, itl_id=9, amount="2000.00")]
    r = _chay(_mo("PM1-1", [_the_da_gan("PM1-1", ds=[28338, 9], gd_ds=hai,
                                        so_tien="5000.00", curr="VND")])
              + " return document.querySelector('.mtong').textContent;",
              tep=TEP, vo=VO)
    assert "3.000" in r and ("lệch" in r.lower()), r
    assert "2.000" in r, f"⛔ ⛔ không nói lệch bao nhiêu: {r!r}"
