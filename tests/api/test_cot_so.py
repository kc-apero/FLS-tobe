"""⛔ Cong: bang cot cua luoi `F02` phai KHOP cua that va KHOP nguon ten.

⛔⛔ **Ba lop lech ma bai nay chan, va ca ba deu IM LANG:**

  ⓐ **Cua tra mot truong ma bang ⛔ khong khai** ⇒ luoi **giau** no. ⛔ Khong
    mot thong bao nao; ke toan chi ⛔ khong bao gio thay cot do, va ⛔ khong ai
    biet no dang thieu.
  ⓑ **Bang khai mot cot ma cua ⛔ khong tra** ⇒ mot cot **rong suot doi**,
    trong y het mot cot *"chua co du lieu"*.
  ⓒ **Ten cot troi khoi nguon.** So doi ten mot cot, man hinh giu ten cu — ke
    toan doc ten cu roi doi chieu voi so mang ten moi. Day la lop lech **⛔
    khong bao gio no ra**, no chi lam hai ben noi chuyen lech nhau.

★ Va theo luat so mot cua du an: moi phep kiem o day deu co mot ban **DO CO Y**
di kem, de chung minh cong nay **da tung thay do**.
"""
from __future__ import annotations

import json

import pytest

from fls.api import cot_so as cs
from fls.repo.doc_bao_cao import _COT_SO, CANON_RA_LUOI, TRUONG_ALLOC


def _truong_cua() -> tuple[str, ...]:
    """Tap truong `GET /ledger` THAT tra ve — doc tu cau SQL, ⛔ khong go tay.

    ⚠ Doc o `tests/` chu ⛔ khong o `fls/api/`: rang buoc `import-linter` so 7
    cam tang cua biet tang kho. Cong nay dung o **ngoai** ca hai tang, nen no
    duoc nhin ca hai.
    """
    # ⭐ `TRUONG_ALLOC` la nam truong `doc_so` THEM vao ngoai cau SQL (vung
    # PHAN BO, suy o may chu). ⛔ Quen chung o day thi cong nay se bao *"bang
    # khai cot ma cua khong tra"* — mot cong DO GIA, va cach "chua" de nhat la
    # go hai cot phan bo khoi luoi.
    # ⭐ `canon` ⛔ KHONG di ra nguyen mang: `_gan_canon` **bung** no thanh 27
    #   truong `canon_<chu cai>` roi **bo mang goc**. ⇒ Tap truong cua that tra
    #   phai phan anh dung phep bung ay, ⛔ khong phai cau SQL tho.
    tho = tuple(x.split(".", 1)[1] for x in _COT_SO if x != "i.canon")
    return tho + TRUONG_ALLOC + tuple("canon_" + x for x in CANON_RA_LUOI)


# ── ⓐⓑ hai chieu voi cua that ─────────────────────────────────────────────
def test_bang_cot_KHOP_dung_cua_that():
    assert cs.kiem_bang_cot(truong_cua=_truong_cua()) == []


def test_cong_DO_khi_cua_them_mot_truong_ma_bang_khong_khai():
    """⓵ Lop lech im lang nhat: cot moi bi **giau**."""
    loi = cs.kiem_bang_cot(truong_cua=_truong_cua() + ("cot_moi_toanh",))
    assert any("GIAU chung trong im lang" in x for x in loi), loi


def test_cong_DO_khi_bang_khai_mot_cot_cua_khong_tra():
    """⓶ Cot **rong suot doi** — trong y het "chua co du lieu"."""
    bang = cs.BANG_COT + (cs.Cot("khong_he_co", "chu", nhan="Ma",
                                 vi_sao="bia ra de thu cong"),)
    loi = cs.kiem_bang_cot(bang=bang, truong_cua=_truong_cua())
    assert any("cua ⛔ khong tra" in x for x in loi), loi


# ── ⓒ ten phai den TU NGUON ───────────────────────────────────────────────
def test_moi_ten_cot_deu_truy_duoc_ve_mot_nguon():
    """⛔ Khong mot tieu de nao duoc la chu go tay khong ai giai thich."""
    for c in cs.BANG_COT:
        nhan = cs.nhan_cua(c)
        assert nhan, f"{c.truong} co tieu de RONG"
        if not (c.ledge or c.canon):
            assert c.vi_sao.strip(), (
                f"{c.truong} dat ten rieng {nhan!r} ma ⛔ khong noi vi sao")


def test_ten_lay_tu_ITL_Ledge_dung_bang_ten_cua_so_that():
    """⭐ Doc **nguoc lai** tu `COT_LUU` — ⛔ khong tin ban khai o `cot_so`."""
    from fls.oracle.ledge_spec import COT_LUU

    theo_truong = {c.di_dau: c for c in COT_LUU}
    n = 0
    for c in cs.BANG_COT:
        if not c.ledge:
            continue
        g = theo_truong[c.truong]
        assert g.letter == c.ledge, (
            f"{c.truong}: ban khai noi Ledge cot {c.ledge}, `COT_LUU` noi "
            f"{g.letter}")
        assert cs.nhan_cua(c) == g.name
        n += 1
    assert n >= 14, f"chi {n} cot lay ten tu Ledge — nghi ban khai da troi"


def test_cong_DO_khi_ten_bi_go_de_len_nguon():
    """⓷ Ban go tay mot ten khac voi ten cua so ⇒ cong phai DO."""
    bang = tuple(cs.Cot(c.truong, c.kieu, ledge=c.ledge, canon=c.canon,
                        nhan="Tên tôi tự đặt" if c.truong == "hd" else c.nhan,
                        vi_sao=c.vi_sao, go=c.go, khoa=c.khoa)
                 for c in cs.BANG_COT)
    loi = cs.kiem_bang_cot(bang=bang, truong_cua=_truong_cua())
    assert any("⛔ khong go lai ten da co nguon" in x for x in loi), loi


def test_cong_DO_khi_tieu_de_dat_NHAM_DONG():
    """⛔⛔ Lay ten cua cot `V` *(Budget Code)* dat len truong `cdt1`.

    Day la lop loi te nhat cua ca bang: tieu de **dung**, du lieu **dung**,
    nhung chung ⛔ khong phai cua nhau — va man hinh trong hoan toan binh
    thuong.
    """
    bang = tuple(cs.Cot(c.truong, c.kieu,
                        ledge="V" if c.truong == "cdt1" else c.ledge,
                        canon=c.canon, nhan=c.nhan, vi_sao=c.vi_sao,
                        go=c.go, khoa=c.khoa)
                 for c in cs.BANG_COT)
    loi = cs.kiem_bang_cot(bang=bang, truong_cua=_truong_cua())
    assert any("tieu de dat nham cho" in x for x in loi), loi


# ── o go duoc ─────────────────────────────────────────────────────────────
def test_dung_NAM_o_go_duoc_tren_luoi_va_HAI_o_o_drawer():
    """⭐ `QĐ-ITL-64` ha 10 → **7** truong; nhung cua `GET /ledger` chi tra
    **5** trong so do ⇒ luoi co 5 o go, drawer co 2 o con lai.

    ⛔ Doc `TRUONG_GHI` cua tang ghi de con so 7 ⛔ khong bao gio la mot con so
    go tay o day.
    """
    from fls.repo.ghi_tay import TRUONG_GHI

    tren_luoi = [c.truong for c in cs.BANG_COT if c.go]
    assert sorted(tren_luoi) == sorted(cs.GO_TREN_LUOI)
    assert sorted(cs.GO_TREN_LUOI + cs.GO_O_DRAWER) == sorted(TRUONG_GHI)
    assert set(cs.GO_O_DRAWER).isdisjoint(_truong_cua()), (
        "hai o drawer nay BAY GIO da co trong `GET /ledger` — dua chung len "
        "luoi di, va sua ca cau giai thich tren man")


def test_cong_DO_khi_mot_truong_go_duoc_bi_khai_thanh_chi_doc():
    """⛔ O go duoc ma trong nhu o chi-doc = dung lop loi owner bat trong 30
    giay o mui thu 27/08."""
    bang = tuple(cs.Cot(c.truong, c.kieu, ledge=c.ledge, canon=c.canon,
                        nhan=c.nhan, vi_sao=c.vi_sao,
                        go=False if c.truong == "cdt1" else c.go,
                        khoa=c.khoa)
                 for c in cs.BANG_COT)
    loi = cs.kiem_bang_cot(bang=bang, truong_cua=_truong_cua())
    assert any("⛔ khong ai biet no go duoc" in x for x in loi), loi


# ── cot dong cung ─────────────────────────────────────────────────────────
def test_hai_cot_dong_cung_la_hai_cot_DAU_TIEN():
    """⛔ CSS neo chung bang `left:0` va `left:var(--khoa-1)`. Neu chung
    ⛔ khong nam dau bang thi hai cot se **de len nhau** khi cuon."""
    assert [cs.BANG_COT[0].khoa, cs.BANG_COT[1].khoa] == [1, 2]
    assert cs.BANG_COT[0].truong == "itl_id"
    assert cs.BANG_COT[1].truong == "memo"


def test_cong_DO_khi_cot_dong_cung_bi_day_xuong_giua():
    bang = (cs.BANG_COT[2],) + (cs.BANG_COT[0], cs.BANG_COT[1]) \
        + cs.BANG_COT[3:]
    loi = cs.kiem_bang_cot(bang=bang, truong_cua=_truong_cua())
    assert any("hai cot dong cung phai la hai cot DAU TIEN" in x
               for x in loi), loi


# ── tep sinh ──────────────────────────────────────────────────────────────
def test_cot_js_doc_nguoc_lai_duoc():
    """⭐ Phep kiem THAT: cat lay phan JSON roi `json.loads`. Neu phep thoat
    sai o bat cu dau *(ten cot co dau tieng Viet, co `·`)* thi bai NO."""
    chu = cs.than_js().decode("utf-8")
    cot = json.loads(chu.split("window.FLS_COT = ", 1)[1]
                     .split(";\nwindow.FLS_CANON", 1)[0])
    assert len(cot) == len(cs.BANG_COT)
    assert cot[0]["truong"] == "itl_id" and cot[0]["khoa"] == 1
    assert all(c["nhan"] for c in cot)
    canon = json.loads(chu.split("window.FLS_CANON = ", 1)[1]
                       .split(";\nwindow.FLS_GO_DRAWER", 1)[0])
    assert len(canon) == 38, "khuon canon co 38 VI TRI (ke ca 2 o trong Z, AA)"
    assert [c["letter"] for c in canon][:3] == ["A", "B", "C"]


def test_cot_js_NO_khi_bang_hong(monkeypatch):
    """⛔ Mot bang cot hong ⛔ khong duoc di ra trinh duyet: man se ve mot luoi
    thieu cot **ma trong nhu day du**."""
    monkeypatch.setattr(cs, "BANG_COT", cs.BANG_COT + (
        cs.Cot("bia", "chu"),))
    with pytest.raises(RuntimeError, match="bang cot vi pham"):
        cs.than_js()


def test_kieu_o_la_thi_cong_DO():
    loi = cs.kiem_bang_cot(bang=(cs.Cot("x", "mau_gi_do", nhan="X",
                                        vi_sao="thu"),))
    assert any("chua khai trong KIEU_O" in x for x in loi), loi


# ── ⭐ canon: bon cot TRUNG TEN phai con chu cai de phan biet ──────────────
def test_drawer_mang_CHU_CAI_vi_bon_cot_canon_trung_ten_nhau():
    """⛔⛔ `AH..AK` deu ten *"MID I DoubleCheck LE"*, va `W/X` trung `AB/AC`.

    Neu drawer chi hien TEN thi bon o giong het nhau, va ⛔ khong ai biet o nao
    la o nao — dung khuyet tat so 1 ma `fls/canon/spec.py` canh.
    """
    chu = cs.than_js().decode("utf-8")
    canon = json.loads(chu.split("window.FLS_CANON = ", 1)[1]
                       .split(";\nwindow.FLS_GO_DRAWER", 1)[0])
    ten = [c["nhan"] for c in canon]
    trung = {t for t in ten if t and ten.count(t) > 1}
    assert trung, "khuon canon phai CON cac cot trung ten — neu het thi doc lai"
    for c in canon:
        assert c["letter"], "moi vi tri canon phai mang CHU CAI"


# ── ⭐⭐ 27 VI TRI CANON RA LUOI (owner chot 2026-09-03) ───────────────────
def test_hai_ban_khai_CANON_ra_luoi_KHONG_duoc_lech():
    """⛔⛔ Danh sach chu cai ton tai **hai ban**: `cot_so.CANON_LEN_LUOI` *(khai
    cot)* va `doc_bao_cao.CANON_RA_LUOI` *(bung du lieu)*.

    Hai ban vi `import-linter` luat 7 cam tang kho biet tang cua. ⇒ Chung
    ⛔ khong the dung chung mot hang so, nen phai co **mot phep so**. Lech thi
    luoi se co mot cot **rong suot doi** hay mot truong bi **giau** — ca hai
    deu im lang.
    """
    from fls.repo.doc_bao_cao import CANON_RA_LUOI

    assert cs.CANON_LEN_LUOI == CANON_RA_LUOI


def test_KHONG_lay_lai_chin_vi_tri_da_co_cot_nen():
    """⛔ `A·B·C·D·E·F·G·L·AG` la chinh cac cot nen da co tren luoi *(ngay, so
    CT, dien giai, tien te, PS No, PS Co, tai khoan, phap nhan tra, LE)*.

    Lay them mot lan nua la **hai cot cung mot du lieu** ⇒ ke toan se hoi *"cai
    nao dung"* — mot cau hoi man hinh **tu tao ra**.
    """
    trung = {"A", "B", "C", "D", "E", "F", "G", "L", "AG"}
    assert trung.isdisjoint(cs.CANON_LEN_LUOI)
    # ⛔ Va hai o TRONG co y (`Z`/`AA`) cung ⛔ khong len luoi: mot cot ⛔ khong
    #   bao gio co gia tri la mot cot chiem cho.
    assert "Z" not in cs.CANON_LEN_LUOI and "AA" not in cs.CANON_LEN_LUOI


def test_luoi_du_52_cot_va_ca_27_cot_canon_deu_MANG_CHU_CAI():
    """⭐ **52** — va con so ay den tu mot phep dem, ⛔ khong phai tu `DEV-12`.

    ⛔⛔ Bon cot `AH..AK` TRUNG TEN het nhau, `W/X` trung `AB/AC`. Neu `cot.js`
    ⛔ khong cho chu cai di theo thi bon tieu de giong het nhau tren luoi va
    ⛔ khong ai biet cot nao la cot nao (`GAP-SPEC-03` ghi *"52 cot"* nhung
    ⛔ khong ai do — nay do duoc, va bang mot duong khac).
    """
    assert len(cs.BANG_COT) == 52
    chu = cs.than_js().decode("utf-8")
    cot = json.loads(chu.split("window.FLS_COT = ", 1)[1]
                     .split(";\nwindow.FLS_CANON", 1)[0])
    ca = [c for c in cot if c["truong"].startswith("canon_")]
    assert len(ca) == 27
    assert all(c["canon"] for c in ca), "⛔ co cot canon ⛔ khong mang chu cai"
    trung = [c["nhan"] for c in ca if c["nhan"] == "MID I DoubleCheck LE"]
    assert len(trung) == 4, "⛔ bon cot TRUNG TEN phai con nguyen — ⛔ khong sua"
