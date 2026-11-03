# -*- coding: utf-8 -*-
"""`B3` — vong gop y UIUX thu HAI cua owner (`23/09`, sau khi da sua vong 1).

  `1` khoi *"Xem du truong"* chiem het man ⇒ **lop phu**, ⛔ khong day gi
  `2` khi cuon: the PM **dung yen**, chi danh sach giao dich cuon
  `3` cac cot giao dich ⛔ khong thang hang ⇒ luoi **tien doan duoc**

⭐⭐ `3` ⛔ **khong phai loi can le**. `.cand-cols` ket thuc bang mot cot
   `auto`, ma **hang tieu de va tung dong la nhung LUOI RIENG** ⇒ `auto` va
   `1fr` tinh lai **theo noi dung tung dong**: dong `2.037 USD Co` duoc cot
   cuoi rong hon dong `19 USD Co`, phan du don nguoc vao `1fr`. Mot ban khai
   luoi, **muoi bon ket qua khac nhau**.
"""
from __future__ import annotations

import io
import re

from tests.web.khung_node import _chay
from tests.web.test_b3_uiux_theo_gop_y_owner import (
    TEP, TEP_CSS, VO, _css_f01, _mo_mot_lenh, _uv)

TEP_JS = "fls/web/tep/man_f01_ghep.js"


def _khoi(css: str, chon: str) -> str:
    """Than cua mot khoi CSS, tim theo dung chuoi mo `chon`."""
    i = css.find(chon)
    assert i >= 0, "⛔ ⛔ không tìm thấy khối `%s`" % chon.rstrip("{")
    return css[i:css.find("}", i)]


# ══ `1` khoi "Xem du truong" = LOP PHU ══════════════════════════════════

def test_DU_TRUONG_la_LOP_PHU_chu_KHONG_day_danh_sach_xuong():
    """Owner `1`: *"khu vuc Xem du truong dai ⇒ chiem het man hinh, user
    ⛔ khong xem duoc danh sach"*.

    ⭐⭐ Khoi ay phuc vu **NIEM TIN VAO DU LIEU** (`QĐ-ITL-144 ⓐ`), ⛔ **khong**
      phuc vu viec ghep. Mot phep **TRA CUU** ⛔ khong duoc doi cho voi cong
      viec chinh — no **noi len tren**, va dong lai la moi thu ve dung cho cu,
      ⛔ khong mot pixel nao dich.
    """
    css = _css_f01()
    t = _khoi(css, ".more{")
    assert "position:absolute" in t, (
        "⛔ `.more` vẫn nằm trong luồng ⇒ nó **đẩy** `.cands` xuống dưới màn")
    assert "z-index" in t, "⛔ lớp phủ ⛔ không khai `z-index` — nó sẽ nằm DƯỚI"
    assert "max-height" in t and "overflow" in t, (
        "⛔ Lớp phủ ⛔ không có trần chiều cao — một thẻ `27` trường sẽ chạy "
        "**quá đáy màn hình** và phần cuối ⛔ không ai với tới được")
    assert "position:relative" in _khoi(css, ".wh{"), (
        "⛔ `.wh` ⛔ chưa là mốc neo — lớp phủ sẽ neo vào một tổ tiên bất kỳ")


def test_ESC_dong_lop_phu():
    """⛔⛔ Mot lop phu ⛔ KHONG co duong ra bang ban phim la mot cai bay
    (`INV-I20` · `NFR-I24`). Man nay von da dung `Esc` cho viec khac, nen
    `Esc` **khi lop phu dang mo** phai dong lop phu **truoc**."""
    r = _chay(_mo_mot_lenh()
              + " F01G.ST.du_truong = true; F01G.ve();"
              " const co = document.querySelectorAll('.more').length;"
              " F01G.phim({key: 'Escape', preventDefault(){}});"
              " return {co, sau: document.querySelectorAll('.more').length,"
              "         co_ST: F01G.ST.du_truong};",
              tep=TEP, vo=VO)
    assert r["co"] == 1, "⛔ lớp phủ ⛔ không mở được"
    assert r["sau"] == 0 and r["co_ST"] is False, (
        "⛔ `Esc` ⛔ không đóng lớp phủ — người ta bị kẹt trong một lớp che "
        "mất đúng thứ họ đang làm")


def test_LOP_PHU_co_NUT_DONG_nhin_thay_duoc():
    """⛔ `Esc` la duong ra cua nguoi BIET no ton tai. Phai co mot nut."""
    r = _chay(_mo_mot_lenh()
              + " F01G.ST.du_truong = true; F01G.ve();"
              " const n = document.querySelector('.more .dong');"
              " return {co: !!n, nhan: n ? n.getAttribute('aria-label') : null};",
              tep=TEP, vo=VO)
    assert r["co"], "⛔ lớp phủ ⛔ không có nút đóng"
    assert r["nhan"], "⛔ nút đóng ⛔ không có tên cho trình đọc màn hình"


# ══ `2` the PM DUNG YEN, chi danh sach cuon ═════════════════════════════

def test_BAN_LAM_VIEC_dung_yen_chi_DANH_SACH_cuon():
    """Owner `2`. ⭐ Rail **da** lam dung the nay tu truoc (`sticky` ＋ cuon
    rieng); ban lam viec thi ⛔ chua — nen cuon xuong dong thu `40` la the PM
    **bien mat**, va nguoi ta ⛔ khong con biet minh dang ghep cho lenh nao.

    ⛔⛔ Va `.cands` phai co `min-height:0`: mot muc flex mac dinh **⛔ khong
       co nho hon noi dung cua no**, nen thieu dong ay thi `overflow:auto`
       ⛔ khong bao gio kich hoat — hop cu **phinh ra** va ca trang lai cuon.
    """
    css = _css_f01()
    w = _khoi(css, ".work{")
    assert "position:sticky" in w and "max-height" in w, (
        "⛔ `.work` ⛔ không dính — cuộn xuống là thẻ PM biến mất")
    c = _khoi(css, ".cands{")
    assert "overflow:auto" in c, (
        "⛔ `.cands` ⛔ không tự cuộn ⇒ cả trang cuộn, và thẻ PM đi theo")
    assert "min-height:0" in c, (
        "⛔⛔ Thiếu `min-height:0` — một mục flex mặc định ⛔ không co nhỏ hơn "
        "nội dung, nên `overflow:auto` **⛔ không bao giờ kích hoạt**")


def test_TIEU_DE_giao_dich_DINH_trong_hop_cuon():
    """⛔ Cuon `50` dong ma mat ten cot la quay lai dung cho `23/09`."""
    assert "position:sticky" in _khoi(_css_f01(), ".cands .chead{"), (
        "⛔ Hàng tiêu đề ⛔ không dính — cuộn xuống là mất tên cột")


# ══ `3` luoi TIEN DOAN DUOC ════════════════════════════════════════════

def test_LUOI_giao_dich_KHONG_con_cot_AUTO():
    """⛔⛔⛔ Goc that su cua *"cac cot ⛔ khong thang hang"*.

    `.chead` va **moi** `.cand` la nhung **luoi RIENG BIET**. Mot vet `auto`
    *(hoac `min-content`/`max-content`)* tinh theo **noi dung cua chinh luoi
    ay** ⇒ dong `2.037 USD Co` ra mot be rong, dong `19 USD Co` ra be rong
    khac, phan du don nguoc vao `1fr` ⇒ **moi dong lech mot chut**.

    ⭐ Chua duy nhat: moi vet phai **tien doan duoc** — mot con so co dinh
      hoac mot phan `fr`. Luc ay `14` luoi rieng cho ra `14` ket qua **y het
      nhau**, va do chinh la dinh nghia cua *"thang hang"*.
    """
    t = _khoi(_css_f01(), ".cand-cols{")
    m = re.search(r"grid-template-columns:([^;]+)", t)
    assert m, "⛔ `.cand-cols` ⛔ không khai lưới"
    vet = m.group(1).split()
    xau = [v for v in vet
           if v in ("auto", "min-content", "max-content")
           or "auto" in v or "-content" in v]
    assert not xau, (
        "⛔⛔ Còn **%d** vệt ⛔ không tiên đoán được: %s\n"
        "   ⇒ mỗi dòng là một lưới riêng, nên vệt ấy tính lại theo nội dung "
        "TỪNG DÒNG và mọi cột lệch nhau" % (len(xau), ", ".join(xau)))
    assert sum(1 for v in vet if "fr" in v) == 1, (
        "⛔ Phải có **đúng một** vệt `fr` *(cột diễn giải)* — nó là chỗ duy "
        "nhất được phép co giãn, và cũng là cột ⛔ không bao giờ bị hy sinh")


def test_SO_TIEN_thang_cot_chu_KHONG_thang_theo_chu_CO():
    """⛔ `2.037 USD Co` / `106 USD Co` / `19 USD Co` — can phai o **chu `Co`**
    thi cac CON SO le tung bac. Ma con so moi la thu nguoi ta so."""
    t = _khoi(_css_f01(), ".cand .amt{")
    assert "display:grid" in t, (
        "⛔ `.amt` còn là `flex` ⇒ số tiền bị `Có`/`Nợ` đẩy lệch từng dòng")
    css = _css_f01()
    assert "grid-column" in _khoi(css, ".cand .amt .chieu{"), (
        "⛔ `Có`/`Nợ` ⛔ không có ô cố định của nó")


def test_SO_TIEN_ve_du_SO_va_CHIEU():
    """⛔ Can thang ⛔ khong duoc lam mat mot phan nao: **so** ＋ **chieu**.

    ⚠ Ban dau bai nay doi **BA** phan *(them huy hieu `Δ`)*. Phep do `23/09`
      cho thay `Δ` la mot **ham cua bac** — `97,1%` dong co no, va bac da noi
      dung dieu do ⇒ no bi bo khoi dong va chuyen sang **cau xac nhan**.
      Xem `test_HUY_HIEU_DELTA_da_BO_vi_no_lap_lai_BAC` va
      `test_DO_LECH_KHONG_bi_vut_no_len_CAU_XAC_NHAN`."""
    r = _chay(_mo_mot_lenh(uv=[_uv(0, lech="10.00"), _uv(1)])
              + " const a = document.querySelectorAll('.cand .amt');"
              " return {n: a.length, p0: a[0].children.length,"
              "         p1: a[1].children.length,"
              "         chu: a[0].textContent};",
              tep=TEP, vo=VO)
    assert r["n"] == 2
    assert r["p0"] == r["p1"] == 2, (
        "⛔ Ô `Số tiền` phải **luôn** đúng **2** phần — một ô co giãn theo "
        "dòng là một cột ⛔ không thẳng hàng (**%s** ／ **%s**)"
        % (r["p0"], r["p1"]))
    assert "Có" in r["chu"], r["chu"]


# ══ ⓐ loi CHAN lo ra khi do `3` ════════════════════════════════════════

def test_HAI_CUA_ung_vien_deu_phai_nan_KHUON():
    """⛔⛔⛔ Loi CHAN, ⛔ **khong** nam trong ba cau hoi cua owner.

    `/itl-candidates` — **duong chinh, ung vien do MAY de xuat** — tra **hang
    THO** tu SQL: `tien` · `ps_no` · `ps_co` · `source_sheet`. Man thi doc
    `uv.amount` · `uv.chieu` · `uv.nguon` ⇒ **hai cot rong**, va
    `khop_dung_tien` so `Number(undefined)` ⇒ **MOI ung vien deu thanh
    "lech"** ⇒ nut `Gan` luon di duong canh bao. Mot phep khop DUNG duoc
    trinh bay nhu mot phep khop SAI.

    ⭐ Anh chup cua owner ⛔ khong lo ra vi man luc ay o che do **Toan so** —
      cua KIA, va cua kia **da** nan khuon.

    ⚠ Bai nay do o tang **cua**, ⛔ khong o tang man: `tests/api/
    test_cua_lenh_cho_pg.py::test_UNG_VIEN_TIEN_tra_dung_KHUON_HOP_DONG…`.
    O day chi giu lai dieu MAN se lam khi cua tra thieu — no phai noi ra,
    ⛔ khong im lang in mot gach ngang."""
    r = _chay(_mo_mot_lenh(uv=[{"itl_id": 7, "doc_no": "CT1",
                                "dien_giai": "X", "curr": "USD",
                                "bac": "ma", "khoa_to": []}])
              + " const a = document.querySelector('.cand .amt');"
              " return a.textContent;",
              tep=TEP, vo=VO)
    assert "undefined" not in r and "NaN" not in r, (
        "⛔⛔ Màn in `%s` — một giá trị của **máy** lọt lên màn của **người** "
        "(`UI-F8`). Thiếu thì phải nói là thiếu." % r)


# ══ `4` KE TOAN PHAI DOC DUOC — do truoc, khai sau ═════════════════════

#: ⭐ Do `23/09` tren cua that, `200` ung vien cua mot lenh ＋ `1.761` ung vien
#: cua `30` lenh. Con so o day la **so ky tu**, va be rong cot phai chua duoc
#: chung — ⛔ khong phai mot con so *"trong cho vua"*.
#:   `doc_no`      p50 **12** · max **36** *(co ca UUID)*
#:   `nguon` ghep  p50 **19** · max **25**  `Airwallex · ••2651 · HGO2`
#:   `so tien`     p50  **7** · max **17**  `1.150.000.000 VND`
DO_KY_TU = {"nguon": 25, "so_tien": 17, "doc_no": 12}
#: ⭐ Be rong mot ky tu `--mono` o `--fs-than` (12.5px) ~ `7.5px`.
PX_MOI_KY_TU = 7.5


def _vet(css: str) -> list[str]:
    import re as _re
    t = _khoi(css, ".cand-cols{")
    m = _re.search(r"grid-template-columns:([^;]+)", t)
    assert m, "⛔ `.cand-cols` ⛔ không khai lưới"
    return m.group(1).split()


def test_COT_NGUON_du_rong_cho_chu_DAI_NHAT_da_do():
    """Owner `23/09`: *"ke toan can nhin ro khu vuc nay, cac thong tin trong
    cot nguon"*.

    ⛔⛔ Anh chup cho thay `SUPE…` · `ASTR…` · `TERA…` — **phap nhan bi cat**.
       Ma `bank · tk · le` la ba manh cua **mot** cau tra loi *"dong tien nay
       tu dau"*; cat mat mot manh thi hai manh con lai ⛔ khong con tra loi
       duoc gi.

    ⭐⭐ Loi cua toi o vong truoc: toi co dinh be rong **de cot thang hang**,
      va **⛔ khong do thu phai nam vua trong do**. Thang hang ma ⛔ khong doc
      duoc thi ⛔ khong sua duoc gi — chi doi mot loi lay mot loi."""
    import re as _re
    v = _vet(_css_f01())
    nguon = v[5]
    px = _re.match(r"^(\d+)px$", nguon)
    assert px, f"⛔ vệt `Nguồn` phải là một số px cố định (**{nguon}**)"
    can = DO_KY_TU["nguon"] * PX_MOI_KY_TU
    assert int(px.group(1)) >= can, (
        "⛔ Cột `Nguồn` **%spx** mà chuỗi dài nhất đã đo cần **~%.0fpx** "
        "(`%d` ký tự) ⇒ pháp nhân bị cắt"
        % (px.group(1), can, DO_KY_TU["nguon"]))


def test_COT_SO_TIEN_du_rong_cho_SO_LON_NHAT():
    """⛔⛔ Anh chup: `15.000.000…` — **con so bi cat**. Day la man ke toan
    **doi chieu tien**; mot con so bi cat la mot con so ⛔ **khong dung duoc**,
    va no con te hon mot o trong vi no **trong nhu mot cau tra loi**."""
    import re as _re
    v = _vet(_css_f01())
    px = _re.match(r"^(\d+)px$", v[6])
    assert px, f"⛔ vệt `Số tiền` phải cố định (**{v[6]}**)"
    can = DO_KY_TU["so_tien"] * PX_MOI_KY_TU + 22   # ＋ o `Nợ/Có`
    assert int(px.group(1)) >= can, (
        "⛔ Cột `Số tiền` **%spx** mà `1.150.000.000 VND` ＋ `Nợ/Có` cần "
        "**~%.0fpx**" % (px.group(1), can))


def test_HUY_HIEU_DELTA_da_BO_vi_no_lap_lai_BAC():
    """⭐⭐⭐ Do `23/09` tren `1.761` ung vien may de xuat — anh xa **mot-mot**:

        bac `cung_tien_te` ④ → Δ **khac 0**   `1.664`
        bac `ma`          ① → Δ **vang**        `51`
        bac `tien`        ② → Δ **= 0**         `46`

    ⇒ `Δ` la mot **ham cua bac**: no ⛔ **khong mang mot chut tin nao moi**
      (`UI-F9` — mot su that, mot cho hien). Va no co mat o **97,1%** dong,
      tuc **⛔ khong con la mot dau hieu** *(mot bao dong chi dang gia bang do
      HIEM cua no)*.

    ⛔⛔ Cai gia: `34px` giu cho ＋ toi `90px` khi hien *(`Δ 1550304.54`)* —
       lay dung cua cot **So tien** va **Nguon** ma ke toan phai doc. Va
       `1550304.54` la **khuon cua may** *(⛔ khong dau phan cach)* lot len
       man cua nguoi (`UI-F8`).

    ⭐ Con so ay ⛔ **khong bi vut**: no chuyen sang **dung luc no doi mot
      quyet dinh** — cau xac nhan khi ke toan chon mot ung vien lech."""
    js = io.open(TEP_JS, encoding="utf-8").read()
    assert "'lech', 'Δ '" not in js and '"lech", "Δ "' not in js, (
        "⛔ Huy hiệu `Δ` vẫn vẽ trên từng dòng")
    r = _chay(_mo_mot_lenh(uv=[_uv(0, lech="13676.35"), _uv(1)])
              + " const a = document.querySelectorAll('.cand .amt');"
              " return {p0: a[0].children.length, chu: a[0].textContent};",
              tep=TEP, vo=VO)
    assert r["p0"] == 2, f"⛔ ô `Số tiền` vẫn có **{r['p0']}** phần"
    assert "Δ" not in r["chu"], r["chu"]


def test_DO_LECH_KHONG_bi_vut_no_len_CAU_XAC_NHAN():
    """⛔ Bo mot con so khoi man ma ⛔ khong cho no mot cho khac la **vut**,
    ⛔ khong phai **don**. Do lech doi mot quyet dinh o dung **mot** thoi
    diem: luc ke toan bam gan mot ung vien ⛔ khong dung tien."""
    r = _chay(_mo_mot_lenh(uv=[_uv(0, lech="13676.35", tien="1.00")])
              + " F01G.ST.ung_vien_chon = 0; F01G.ST.xac_nhan = true;"
              " F01G.ve();"
              " return document.querySelector('.act').textContent;",
              tep=TEP, vo=VO)
    assert "13676.35" in r or "13.676" in r, (
        "⛔ Câu xác nhận ⛔ không nói **lệch bao nhiêu** — mà đó đúng là "
        "điều người ta cần biết trước khi bấm: %r" % r)


def test_LUAT_HY_SINH_COT_dung_CUNG_ban_khai_luoi():
    """⛔⛔⛔ Loi **toi de lai** o vong truoc: cac khoi `@container` van khai
    luoi tren `.cand` voi ban **CU** *(con vet `auto`)*. Hai bo chon co cung
    do dac hieu, va khoi `@container` nam **sau** trong tep ⇒ no **THANG**
    ⇒ o moi man hep hon `860px` thi vet `auto` **quay lai**, va moi thu vua
    sua lai lech — im lang.

    ⛔⛔ Te hon: no `display:none` dung cot **`Nguon`** — cai owner vua noi
       la phai nhin ro."""
    css = _css_f01()
    i = 0
    xau = []
    while True:
        i = css.find("@container", i)
        if i < 0:
            break
        j = css.find("\n}", i)
        khoi = css[i:j if j > 0 else len(css)]
        if ".cand{" in khoi:
            xau.append("khai lưới trên `.cand` thay vì `.cand-cols`")
        if ".nguon{display:none" in khoi.replace(" ", ""):
            xau.append("giấu cột `Nguồn`")
        i += 10
    assert not xau, (
        "⛔ Luật hy sinh cột còn sai: %s" % " ／ ".join(sorted(set(xau))))


def test_KHI_CHAT_thi_hy_sinh_NGAY_va_SO_CT_chu_KHONG_PHAI_NGUON():
    """⭐ Thu tu hy sinh la mot **quyet dinh ve thong tin**, ⛔ khong phai mot
    tien nghi CSS. `Nguon` ＋ `So tien` ＋ `Dien giai` la ba thu ke toan doi
    chieu; `Ngay` co tren the PM, va `So CT` co khi la mot **UUID 36 ky tu**
    ⛔ khong ai doc."""
    css = _css_f01()
    assert "@container work" in css, "⛔ ⛔ không còn luật hy sinh cột nào"
    assert ".ngay{display:none" in css.replace(" ", ""), (
        "⛔ Màn chật phải bỏ `Ngày` trước — nó đã có trên thẻ PM")
    assert ".nguon{display:none" not in css.replace(" ", ""), (
        "⛔⛔ `Nguồn` ⛔ KHÔNG BAO GIỜ bị giấu — owner `23/09` nói thẳng")
