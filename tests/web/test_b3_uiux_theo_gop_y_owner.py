# -*- coding: utf-8 -*-
"""`B3` — bay gop y UIUX cua owner (`23/09`), do bang bai thu.

Owner mo man that va noi bay dieu. Bay dieu ay ⛔ khong phai "y thich": moi
dieu la mot cho man **noi kho hon muc can thiet**. Bai nay giu chung lai.

  `1.1` bo cot `Bac` o bang so
  `1.2` mot THANG CO CHU — man dang co **10** co chu khac nhau
  `1.3` bo dai nhac `GAP-SPEC-01` khoi dau trang
  `2.1` khoi *"Xem du truong"* xep **nhieu cot**, dung ban dung
  `2.2` cot lenh chi ⛔ khong toan mau den
  `2.3` keo duoc be rong rail
  `2.4` bang giao dich co **hang tieu de**
"""
from __future__ import annotations

import io
import json
import pathlib
import re

from tests.web.khung_node import _chay
from tests.web.test_khong_ma_mau_go_tay import _bo_ghi_chu

GOC = pathlib.Path(__file__).resolve().parents[2]
TEP_CSS = GOC / "fls" / "web" / "tep" / "hinh.css"
TEP_TOKEN = GOC / "fls" / "web" / "tep" / "tokens.css"
TEP_JS = GOC / "fls" / "web" / "tep" / "man_f01_ghep.js"
TEP_HTML = GOC / "fls" / "web" / "tep" / "index.html"

VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
man.className = 'screen on';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

D_NGUOI = "/queue/lenh-cho?ro=nguoi&limit=500"
D_MAY = "/queue/lenh-cho?ro=may&tu_chung=0&limit=500"


#: ⚠ Ten CO Y la chu cai dau — tep nay la mot **ban se ra ngoai kho**.
def _the(ma, **doi):
    t = {"ma_lenh": ma, "ngay": "18/09", "trang_thai": "chua_gan",
         "trang_thai_nhan": "Chưa gán", "trang_thai_mau": "",
         "loai_phieu": "Regular", "noi_dung": "TT " + ma, "so_tien": "990.00",
         "curr": "USD", "nguoi_nhan": "S. INC.", "so_chung_tu": "CT88213",
         "phap_nhan": "SGO2", "ngan_hang": "OCBC", "tai_khoan": "••4001",
         "cdt": "CVL | VisionLab",
         "nhom_du_truong": [
             {"ten": "Lập lệnh", "o": [["Timestamp", "12/03/2025 18:54"],
                                       ["Chi nhánh", "OCBC"]]},
             {"ten": "Chứng từ", "o": [["Status_Final", "Approve"]]},
             {"ten": "Đường dẫn phiếu", "o": [["ID PMSlip", "PM1"]]},
         ]}
    t.update(doi)
    return t


def _uv(i=0, **doi):
    u = {"itl_id": 100 + i, "doc_no": "CT8821" + str(i),
         "doc_date": "18/09/2026", "dien_giai": "FUNDS TRF TT 1OR6061",
         "amount": "990.00", "curr": "USD", "chieu": "co", "bac": "ma",
         "lech": None, "khoa_to": [],
         "nguon": {"tk": "••4001", "bank": "OCBC", "curr": "USD",
                   "le": "SGO2"}}
    u.update(doi)
    return u


def _dat(rows) -> str:
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": rows, "next_cursor": None}},
            ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = " + json.dumps(
            {"data": {"rows": [], "next_cursor": None}}) + ";")


def _mo_mot_lenh(ma="PM1-1", uv=None):
    """Mo `ma` ra ban lam viec, voi danh sach ung vien `uv`."""
    ds = uv if uv is not None else [_uv(0), _uv(1)]
    return (_dat([_the(ma), _the("PM2-1")])
            + "_TRA['/queue/lenh/" + ma + "/itl-candidates'] = "
            + json.dumps({"data": {"ung_vien": ds}}, ensure_ascii=False) + ";"
            "_TRA['/queue/lenh/" + ma + "/so'] = {data: {ung_vien: []}};"
            " await F01G.mo_man(); await F01G.mo_lenh('" + ma + "');")


#: ⭐ Moc mo khoi `SCR-F01`. Ca tep `hinh.css` phuc vu **nam** man; phien nay
#: chi dung den mot man, va mot cong vo ca tep se **doi sua bon man ⛔ khong
#: ai xin sua** — do la cach nhanh nhat de mot cong bi tat.
MOC_F01 = "MAN GAN LENH CHI (`SCR-F01`)"


def _css() -> str:
    """Toan bo `hinh.css`, da bo ghi chu."""
    with io.open(TEP_CSS, encoding="utf-8") as f:
        return _bo_ghi_chu(f.read())


def _css_f01() -> str:
    """CHI khoi `SCR-F01` — tu moc den cuoi tep.

    ⛔⛔ Cat **TRUOC**, bo ghi chu **SAU**: moc nam trong mot ghi chu, nen neu
       bo ghi chu truoc thi moc bien mat va phep cat ⛔ khong con gi de bam.
    """
    with io.open(TEP_CSS, encoding="utf-8") as f:
        tho = f.read()
    i = tho.find(MOC_F01)
    assert i >= 0, "⛔ ⛔ không tìm thấy mốc khối `SCR-F01` trong `hinh.css`"
    return _bo_ghi_chu(tho[i:])


# ── `1.1` bo cot `Bac` ────────────────────────────────────────────────────

def test_BANG_KHONG_con_cot_BAC():
    """Owner `1.1`. ⭐ Bac ⛔ **khong bien mat khoi man** — no van la `①②③④`
    tren tung dong ung vien, **dung cho nguoi dang chon**. O bang so no la
    mot cot chiem cho ma ⛔ khong ai dung de quet."""
    r = _chay(_dat([_the("PM1-1")])
              + " await F01G.mo_man();"
              " return {khai: F01G.COT_BANG.length,"
              "         ten: F01G.COT_BANG.map(c => c[1]),"
              "         dau: document.querySelector('.mhead').children.length,"
              "         o: document.querySelectorAll('.mtable .mrow')[0]"
              "             .children.length};",
              tep=TEP, vo=VO)
    assert "Bậc" not in r["ten"], "⛔ Cột `Bậc` vẫn còn ở bảng sổ"
    assert r["khai"] == 11, f"⛔ khai **{r['khai']}** cột, phải **11**"
    assert r["dau"] == 11, f"⛔ hàng tiêu đề có **{r['dau']}** ô"
    assert r["o"] == 11, (
        f"⛔⛔ Một dòng có **{r['o']}** ô mà tiêu đề có **11** — lưới sẽ "
        "**trượt cột** và mọi con số đọc sang nhãn bên cạnh")


def test_BAC_VAN_CON_tren_dong_ung_vien():
    """⛔ Bo cot o bang ⛔ KHONG duoc lam mat bac o cho no dang lam viec."""
    r = _chay(_mo_mot_lenh()
              + " return document.querySelectorAll('.cand .tg').length;",
              tep=TEP, vo=VO)
    assert r == 2, f"⛔ Bậc `①②③④` mất khỏi dòng ứng viên (**{r}**)"


# ── `1.2` mot THANG CO CHU ────────────────────────────────────────────────

CO_CHU = re.compile(r"font(?:-size)?\s*:[^;{}]*?(\d+(?:\.\d+)?)px")


def test_MOT_THANG_CO_CHU_chu_KHONG_MUOI_lan_chon_rieng():
    """Owner `1.2`: *"phong chu va co chu chua deu, roi mat"*.

    ⭐ Do `23/09` **truoc** khi sua: khoi `SCR-F01` co **10** co chu khac nhau
      (`10 · 10,5 · 11 · 11,5 · 12 · 12,5 · 13 · 13,5 · 14 · 15px`). Do ⛔
      khong phai mot thang — do la **muoi lan chon rieng le**, va mat nguoi
      doc thay dung cai do.

    ⇒ Moi co chu phai den tu mot **bien da dat ten**. Mot so `px` go thang vao
      `font:` la mot bac thang ⛔ khong ai dat ten, va bac sau se lech tiep."""
    css = _css_f01()
    kho = CO_CHU.findall(css)
    assert not kho, (
        "⛔ Còn **%d** cỡ chữ gõ thẳng vào `hinh.css`: %s\n"
        "   ⇒ dùng `var(--fs-*)` đã khai ở `tokens.css`"
        % (len(kho), ", ".join(sorted(set(kho), key=float))))


def test_THANG_CO_CHU_duoc_KHAI_o_tokens():
    with io.open(TEP_TOKEN, encoding="utf-8") as f:
        tok = _bo_ghi_chu(f.read())
    thieu = [t for t in ("--fs-nhan", "--fs-phu", "--fs-than", "--fs-manh",
                         "--fs-to") if ("%s:" % t) not in tok]
    assert not thieu, "⛔ Thang cỡ chữ chưa khai: %s" % ", ".join(thieu)


def test_MONO_chi_dung_cho_thu_CAN_SO_COT():
    """⭐⭐ Luat mot cau: **`--mono` danh cho thu can so cot theo ky tu** — ma,
    so tien, ngay, so chung tu. Mot CAU VAN trong `--mono` doc nhu mot ban in
    may, va do la mot nua cua cam giac *"roi mat"*.

    ⛔ `.goi-phim` la mot cau huong dan; `.more dd` la **gia tri du truong**,
    phan lon la chu (`Approve` · `VPBANK` · `Danh sach nhan vien...`)."""
    css = _css_f01()
    for lop in (".goi-phim{", ".more dd{"):
        i = css.find(lop)
        assert i >= 0, "⛔ ⛔ không tìm thấy `%s`" % lop
        than = css[i:css.find("}", i)]
        assert "var(--mono)" not in than, (
            "⛔ `%s` vẫn dùng `--mono` — đó là chữ để ĐỌC, ⛔ không phải số "
            "để SO CỘT" % lop.rstrip("{"))


# ── `1.3` bo dai nhac `GAP-SPEC-01` ──────────────────────────────────────

def test_KHONG_con_dai_nhac_GAP_SPEC_01_o_dau_trang():
    """Owner `1.3`. ⭐ Cau ay noi ve **tinh trang du an**, ⛔ khong ve viec ke
    toan dang lam. No nam tren **moi** man, doc **moi** lan mo — mot loi nhac
    doc hoai thi thanh mot vet ban, ⛔ khong con la mot loi nhac.

    ⚠ `GAP-SPEC-01` **⛔ khong bi xoa khoi so**: no van o `06_ORCHESTRATOR`."""
    with io.open(TEP_HTML, encoding="utf-8") as f:
        html = f.read()
    assert "GAP-SPEC-01" not in html, (
        "⛔ Dải nhắc `GAP-SPEC-01` vẫn ở `index.html`")
    assert 'class="hint"' not in html, "⛔ `<p class=\"hint\">` vẫn còn"


# ── `2.1` khoi "Xem du truong" xep NHIEU COT ─────────────────────────────

def test_XEM_DU_TRUONG_xep_NHIEU_COT_dung_ban_dung():
    """Owner `2.1`: *"toi muon layout nhu wireframe"*.

    ⛔ Ban `22/09` xep **doc**: `h4` roi `dl`, roi `h4` roi `dl`… ⇒ bam *"Xem
    du truong"* la day toan bo phan duoi man xuong **mot man hinh**.
    ⭐ Ban dung: `.more2 .cols` = `repeat(auto-fit,minmax(230px,1fr))` — moi
      nhom la **mot khoi rieng**, xep canh nhau."""
    r = _chay(_mo_mot_lenh()
              + " F01G.ST.du_truong = true; F01G.ve();"
              " const c = document.querySelector('.more .cols');"
              " return {co_cols: !!c,"
              "         nhom: c ? c.children.length : 0,"
              "         h4_trong_nhom: c && c.children[0]"
              "            ? c.children[0].querySelectorAll('h4').length : 0,"
              "         dl_trong_nhom: c && c.children[0]"
              "            ? c.children[0].querySelectorAll('dl').length : 0};",
              tep=TEP, vo=VO)
    assert r["co_cols"], (
        "⛔ ⛔ không có `.more .cols` — các nhóm vẫn xếp dọc thành một cột dài")
    assert r["nhom"] == 3, (
        f"⛔ `.cols` có **{r['nhom']}** khối con, thẻ có **3** nhóm")
    assert r["h4_trong_nhom"] == 1 and r["dl_trong_nhom"] == 1, (
        "⛔⛔ Một khối phải bọc ĐÚNG một `h4` ＋ một `dl`. Nếu `h4` và `dl` "
        "nằm rời nhau trong lưới, `auto-fit` sẽ tách **tiêu đề khỏi bảng "
        "của nó** — tên nhóm đứng ở cột này, giá trị ở cột kia")


def test_COLS_xep_theo_auto_fit_chu_KHONG_so_cot_CUNG():
    """⭐ `auto-fit` cho so cot tu do theo be rong THAT. Mot so cot cung (`3`)
    se vo o man hep — va ban lam viec da bi rail an mat mot phan roi."""
    css = _css_f01()
    i = css.find(".more .cols{")
    assert i >= 0, "⛔ ⛔ chưa khai `.more .cols`"
    than = css[i:css.find("}", i)]
    assert "auto-fit" in than and "minmax(" in than, (
        "⛔ `.more .cols` phải dùng `repeat(auto-fit,minmax(…))`, ⛔ không "
        "một số cột cứng — bàn làm việc đã bị rail ăn mất một phần bề ngang")


# ── `2.2` cot lenh chi ⛔ khong toan mau den ──────────────────────────────

def test_RAIL_co_MAU_phan_biet_chu_KHONG_toan_DEN():
    """Owner `2.2`: *"text toan mau den"*.

    ⭐ Ma `PM…` la thu nguoi ta **quet mat doc qua** de tim dong. No phai
      **bat ra** khoi cau noi dung. Cung the o bang so."""
    css = _css_f01()
    for lop in (".rrow .pm{", ".mtable .pm{"):
        i = css.find(lop)
        assert i >= 0, "⛔ ⛔ không tìm thấy `%s`" % lop
        than = css[i:css.find("}", i)]
        assert "color:var(--" in than, (
            "⛔ `%s` ⛔ chưa đặt màu — mã PM chìm trong khối chữ đen"
            % lop.rstrip("{"))


def test_RAIL_ve_du_BA_MUC_co_mau_khac_nhau():
    """⛔ Ba muc `ngay` · `ma` · `chu du toan` phai la **ba lop khac nhau** —
    neu chung dung chung mot lop thi ⛔ khong the to khac nhau."""
    r = _chay(_mo_mot_lenh()
              + " const x = document.querySelector('.rrow');"
              " return {d: x.querySelectorAll('.d').length,"
              "         pm: x.querySelectorAll('.pm').length,"
              "         cdt: x.querySelectorAll('.cdt').length};",
              tep=TEP, vo=VO)
    assert r == {"d": 1, "pm": 1, "cdt": 1}, "⛔ rail thiếu mục: %s" % r


# ── `2.3` keo duoc be rong rail ──────────────────────────────────────────

def test_CO_TAY_KEO_giua_rail_va_ban_lam_viec():
    """Owner `2.3`. ⭐ Noi dung lenh chi dai ngan **rat khac nhau** giua cac
    ro; mot be rong cham chet (`clamp(300px,26vw,380px)`) dung cho ro nay se
    cat cut ro kia."""
    r = _chay(_mo_mot_lenh()
              + " return {keo: document.querySelectorAll('.keo').length,"
              "         vai: (document.querySelector('.keo')||{})"
              "               .getAttribute ? document.querySelector('.keo')"
              "               .getAttribute('role') : null};",
              tep=TEP, vo=VO)
    assert r["keo"] == 1, "⛔ ⛔ không có tay kéo `.keo` giữa rail và bàn"
    assert r["vai"] == "separator", (
        "⛔ Tay kéo phải là `role=separator` — ⛔ không thì người dùng bàn "
        "phím ⛔ không biết nó tồn tại")


def test_BE_RONG_KEO_duoc_GIU_LAI_qua_moi_lan_ve():
    """⛔⛔ `ve()` dung lai **toan bo** cay DOM moi lan. Mot be rong dat thang
    vao phan tu se bi xoa ngay o lan `ve()` ke tiep — tuc keo xong, bam mot
    cai la **nhay ve cu**. ⇒ No phai song trong `ST`."""
    r = _chay(_mo_mot_lenh()
              + " F01G.ST.rail_w = 520; F01G.ve();"
              " const t = document.querySelector('.than');"
              " return t.getAttribute('style') || '';",
              tep=TEP, vo=VO)
    assert "520px" in r, (
        "⛔ `ST.rail_w` ⛔ không vào được `.than` sau `ve()` — kéo xong bấm "
        "một cái là nhảy về cũ (style=%r)" % r)


def test_KEO_KHONG_duoc_bop_rail_xuong_duoi_muc_doc_duoc():
    """⭐ Mot rail `120px` thi ⛔ khong con doc duoc ma lenh nao — keo phai co
    **chan duoi** va **tran tren**, ⛔ khong tu do tuyet doi."""
    js = io.open(TEP_JS, encoding="utf-8").read()
    assert "RAIL_MIN" in js and "RAIL_MAX" in js, (
        "⛔ ⛔ chưa có chặn `RAIL_MIN`/`RAIL_MAX` cho tay kéo")
    r = _chay(_mo_mot_lenh()
              + " return [F01G.chan_rail(50), F01G.chan_rail(9000),"
              "         F01G.chan_rail(430)];",
              tep=TEP, vo=VO)
    assert r[0] >= 260, f"⛔ bóp được rail xuống **{r[0]}px**"
    assert r[1] <= 720, f"⛔ kéo được rail tới **{r[1]}px**"
    assert r[2] == 430, "⛔ bề rộng hợp lệ bị đổi"


# ── `2.4` bang giao dich co HANG TIEU DE ─────────────────────────────────

def test_BANG_GIAO_DICH_co_HANG_TIEU_DE():
    """Owner `2.4`. ⭐⭐ Sau cot ⛔ khong mot cai ten: `CT88210` la so chung tu
    hay ma gi? `18/09/2026` la ngay giao dich hay ngay nap? `OCBC · ••4001 ·
    SGO2` la cai gi? Ke toan **doan** — va doan thi co luc doan sai.

    ⛔ Va hang tieu de phai dung **cung mot luoi** voi dong: neu no la mot
    luoi khac, nhan se **truot sang cot ben canh** va noi doi mot cach rat
    thuyet phuc."""
    r = _chay(_mo_mot_lenh()
              + " const h = document.querySelector('.cands .chead');"
              " const c = document.querySelector('.cands .cand');"
              " return {co: !!h, o: h ? h.children.length : 0,"
              "         o_dong: c ? c.children.length : 0,"
              "         lop_h: h ? h.className : '',"
              "         ten: h ? Array.from(h.children)"
              "                 .map(x => x.textContent) : []};",
              tep=TEP, vo=VO)
    assert r["co"], "⛔ Bảng giao dịch ⛔ không có hàng tiêu đề"
    assert r["o"] == r["o_dong"] == 7, (
        f"⛔⛔ Tiêu đề **{r['o']}** ô ／ dòng **{r['o_dong']}** ô — lưới lệch, "
        "mọi nhãn đọc sang cột bên cạnh")
    assert "cand-cols" in r["lop_h"], (
        "⛔⛔ Tiêu đề phải mang **đúng lớp lưới** của dòng (`cand-cols`). Hai "
        "lưới rời nhau sẽ trượt khỏi nhau ở đúng chỗ ⛔ không ai nhìn lại")
    assert [t for t in r["ten"] if t] == [
        "Bậc", "Số CT", "Diễn giải sao kê", "Ngày", "Nguồn", "Số tiền"], (
        "⛔ Tên cột sai: %r" % (r["ten"],))


def test_TIEU_DE_VA_DONG_dung_CHUNG_mot_khai_bao_luoi():
    """⛔⛔ Cot ⛔ khong duoc khai **hai lan**. Ban `22/09` khai luoi thang
    trong `.cand{}`; neu tieu de khai rieng thi hai ban su that ve *"bang nay
    co may cot"* se lech — va no lech **im lang**."""
    css = _css_f01()
    i = css.find(".cand-cols{")
    assert i >= 0, "⛔ ⛔ chưa tách lớp lưới dùng chung `.cand-cols`"
    than = css[i:css.find("}", i)]
    assert "grid-template-columns" in than, "⛔ `.cand-cols` ⛔ không khai lưới"
    j = css.find(".cand{")
    assert j >= 0
    assert "grid-template-columns" not in css[j:css.find("}", j)], (
        "⛔⛔ `.cand` VẪN khai lưới riêng — giờ có **hai** bản khai cho cùng "
        "một câu hỏi *"
        "\"bảng này có mấy cột\"*, và chúng sẽ lệch")
