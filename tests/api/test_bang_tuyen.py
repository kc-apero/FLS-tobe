"""Cong quet BANG TUYEN — cong chinh cua `P4` (`03_Dev/03` §5.8).

⛔ Cong nay chi co nghia vi co MOT bang tuyen de quet. Neu duong nam rai rac
trong cac `if path == ...` thi cong phai doc ma nguon de doan, va mot cong phai
doan la mot cong se sai.
"""
from __future__ import annotations

import pytest

from fls.api import bang_tuyen as bt
from fls.api.xu_ly import HAM


# ── cong ──────────────────────────────────────────────────────────────────
def test_bang_tuyen_that_khong_vi_pham():
    assert bt.kiem_bang_tuyen() == []


def test_KHONG_duong_nao_GHI_vao_so():
    """⛔⛔ Bat bien SONG QUA `P5`, va no thay bai cu.

    Ban `P4` co bai `test_P4_CHI_DOC_khong_mot_duong_ghi_nao` — *"khong tuyen
    nao la `POST`"*. Bai do **dung luc do nhung sai luat**: no khoa mot **trang
    thai tam thoi** (chua co duong ghi) thay vi khoa mot **bat bien** (⛔ khong
    duong nao duoc sua so). Den `P5` no bat buoc phai xoa — va mot bai bi xoa de
    tinh nang moi di qua la mot bai chua tung bao ve gi.

    ⇒ Bai nay khoa dieu **khong bao gio doi**: `fls_itl` la append-only
    (`INV-I08`), nen ⛔ khong tuyen nao — du phuong thuc gi — duoc GHI vao no.

    ── ⛔⛔ 2026-09-08 · VA CHINH BAI NAY DA ROI VAO CAI BAY NO VUA TA ────────

    Doan tren viet: *"bai `P4` dung luc do nhung SAI LUAT — no khoa mot trang
    thai TAM THOI thay vi mot BAT BIEN"*. Bai nay **lam y het the**, chi tinh
    vi hon: `INV-I08` doc nguyen van la *"chi **THEM**, ⛔ khong **SUA**"*, ma
    cau khang dinh o day lai la *"⛔ khong ai duoc **GHI**"*. **THEM cung la
    ghi.** ⇒ No khoa *"⛔ chua tuyen nao NAP"* — dung, vi cho toi 08/09 duong
    duy nhat dua du lieu vao kho la mot **lenh dong lenh**, va moi `POST` deu
    SUA mot dong DA CO.

    `CR#11` dung `POST /nap` (`BA-07` §4b) — tuyen **DAU TIEN THEM** dong vao
    so. Cong cu se cam **chinh cai phep ma `INV-I08` cho phep**.

    ⚠ **Noi thang: day LA noi long tren MOT truc** — truoc: `0` tuyen ghi
      duoc; nay: `1`. ⛔ Khong giau bang cach goi no la "lam ro". Doi lai, cho
      duy nhat ay bi siet bang **BON** dieu kien, va ba trong so do ⛔ khong he
      ton tai truoc do:
        ⓐ phai khai `them_vao_so` — mot **ngoai le CO TEN**, dem duoc;
        ⓑ phai la `POST` *(`PUT`/`DELETE`/`PATCH` len so van cam TUYET DOI)*;
        ⓒ phai ghi ca `fls_run` *(dong so ⛔ khong co lan nap = mat lineage)*;
        ⓓ ca `fls/` ⛔ khong duoc chua mot cau `UPDATE`/`DELETE` nao nham
           `fls_itl` — **quet ma nguon**, `tests/api/test_them_vao_so.py`.
      ⇒ Phep **SUA** so — thu `INV-I08` that su cam — nay bi chan o **ba** lop:
        trigger kho (`INV-I03`), bang tuyen, va quet ma nguon.

    ⭐ Bai nay ⛔ **KHONG bi xoa**. No van khoa ve *"moi tuyen KHAC"*, va no
      giu nguyen loi canh bao o tren — de nguoi sau doc duoc **ca hai lan** mot
      cau khang dinh tuong nhu bat bien hoa ra chi la mot trang thai.
    """
    xau = [f"{t.phuong_thuc} {t.duong}" for t in bt.BANG_TUYEN
           if bt.SO in t.bang_ghi and not t.them_vao_so]
    assert xau == [], f"co tuyen khai GHI vao {bt.SO}: {xau}"


def test_cong_BAT_duong_POST_ghi_vao_so():
    """⛔⛔ Lo THAT cua ban `P4`: cong cu chi kiem theo PHUONG THUC.

    `P5` ghi bang `POST`, nen mot `POST .../adjust` ghi thang vao `fls_itl` se
    **di qua cong cu trong im lang** — va do dung la duong de nhat, vi `BA-07`
    §3 con viet *"truong hop-dong cap nhat `*_thyt`"*.
    """
    xau = (bt.Tuyen("POST", f"{bt.TIEN_TO}/ledger/{{itl_id}}/adjust", "sua",
                    ("fls_itl", "fls_journal"),
                    bang_ghi=("fls_itl", "fls_journal"),
                    ghi=True, ghi_nhat_ky=True),)
    loi = bt.kiem_bang_tuyen(xau)
    assert any("khai GHI vao fls_itl" in x for x in loi), loi
    # ⛔ Va chung minh cong CU khong bat duoc no:
    assert not any("`INV-I08` cam: sua chi" in x for x in loi), (
        "phep kiem theo phuong thuc lai bat duoc POST — bai nay mat y nghia")


def test_moi_duong_ghi_deu_de_lai_VET():
    """`AUD-1`: sau `QĐ-ITL-27`, vet la lop kiem soat DUY NHAT con lai."""
    for t in bt.BANG_TUYEN:
        if t.ghi:
            assert set(t.bang_ghi) & bt.BANG_CO_VET, (
                f"{t.duong} ghi ma khong de lai vet: {t.bang_ghi}")


def test_bang_ghi_va_co_ghi_khong_duoc_mau_thuan():
    for t in bt.BANG_TUYEN:
        assert bool(t.ghi) == bool(t.bang_ghi), t.duong
        assert t.ghi_nhat_ky == ("fls_journal" in t.bang_ghi), t.duong


def test_cong_BAT_duong_PUT_nham_vao_so():
    """⛔ Bai chung minh cong con song. `INV-I08`: sua chi bang but toan moi."""
    xau = (*bt.BANG_TUYEN,
           bt.Tuyen("PUT", f"{bt.TIEN_TO}/ledger/{{itl_id}}", "sua",
                    ("fls_itl",), ghi=True, ghi_nhat_ky=True))
    loi = bt.kiem_bang_tuyen(xau)
    assert any("PUT" in x and "fls_itl" in x for x in loi), loi


@pytest.mark.parametrize("pt", sorted(bt.PHUONG_THUC_CAM_LEN_SO))
def test_cong_BAT_ca_ba_phuong_thuc_sua_so(pt):
    xau = (bt.Tuyen(pt, f"{bt.TIEN_TO}/ledger/{{itl_id}}", "x", ("fls_itl",)),)
    assert any("fls_itl" in x for x in bt.kiem_bang_tuyen(xau))


def test_cong_BAT_duong_ghi_ma_khong_de_lai_VET():
    """`AUD-1`: vet la cho kiem soat DUY NHAT con lai (`QĐ-ITL-27`).

    ⚠ Ban dau cong nay doi MOI duong ghi phai cham `fls_journal`. Do la mot cong
    **do GIA**: duong ghi ly do/hoan cham `fls_queue_event`, ma bang do **cung
    mang vet** (`actor`/`at`/`reason`). Mot cong do gia thi nguoi ta go cong chu
    khong sua ma. ⇒ Cong nay hoi *"co de lai VET khong"*, ⛔ khong hoi *"co cham
    dung mot bang cu the khong"*.
    """
    xau = (bt.Tuyen("POST", f"{bt.TIEN_TO}/ledger/{{itl_id}}/adjust", "sua",
                    ("fls_adjustment",), bang_ghi=("fls_adjustment",),
                    ghi=True),)
    assert any("de lai VET" in x for x in bt.kiem_bang_tuyen(xau))


def test_cong_KHONG_do_gia_voi_duong_ghi_su_kien_hang_cho():
    """`fls_queue_event` la bang mang vet ⇒ ⛔ khong duoc bao do."""
    tot = (bt.Tuyen("POST", f"{bt.TIEN_TO}/queue/{{itl_id}}/reason", "ly_do",
                    ("fls_itl", "fls_queue_event"),
                    bang_ghi=("fls_queue_event",), ghi=True),)
    assert bt.kiem_bang_tuyen(tot) == []


def test_cong_BAT_bang_ngoai_fls():
    """`QĐ-ITL-45`: FLS chi doc kho rieng, `fps_*`/P100 di qua adapter."""
    xau = (bt.Tuyen("GET", f"{bt.TIEN_TO}/pm", "x", ("fps_pm_line",)),)
    assert any("fps_pm_line" in x for x in bt.kiem_bang_tuyen(xau))


def test_cong_BAT_tien_to_la():
    xau = (bt.Tuyen("GET", "/api/voi/ledger", "x", ("fls_itl",)),)
    assert any("/api/fls/v1" in x for x in bt.kiem_bang_tuyen(xau))


def test_cong_BAT_duong_khong_khai_bang_nao():
    xau = (bt.Tuyen("GET", f"{bt.TIEN_TO}/x", "x", ()),)
    assert any("khong khai bang nao" in x for x in bt.kiem_bang_tuyen(xau))


def test_cong_BAT_trung_tuyen():
    t = bt.Tuyen("GET", f"{bt.TIEN_TO}/ledger", "so", ("fls_itl",))
    assert any("trung tuyen" in x for x in bt.kiem_bang_tuyen((t, t)))


# ── khop duong ────────────────────────────────────────────────────────────
def test_tham_so_duong_KHONG_an_dau_gach():
    """⛔ `{itl_id}` an ca `/` thi `/ledger/{itl_id}` khop `/ledger/1/nhat-ky`
    va tra ve du lieu cua duong khac — mot loi dinh tuyen IM LANG."""
    t = next(x for x in bt.BANG_TUYEN if x.duong.endswith("{itl_id}"))
    assert t.khop(f"{bt.TIEN_TO}/ledger/42") == {"itl_id": "42"}
    assert t.khop(f"{bt.TIEN_TO}/ledger/42/nhat-ky") is None
    assert t.khop(f"{bt.TIEN_TO}/ledger") is None


def test_khop_dung_tuyen_khong_lay_tuyen_dai_hon():
    t, p = bt.tim("GET", f"{bt.TIEN_TO}/queue")
    assert t.ham == "hang_cho" and p == {}
    t, p = bt.tim("GET", f"{bt.TIEN_TO}/queue/summary")
    assert t.ham == "hang_cho_tom"


def test_duong_khong_co_thi_None():
    assert bt.tim("GET", f"{bt.TIEN_TO}/khong-co") is None
    assert not bt.duong_ton_tai(f"{bt.TIEN_TO}/khong-co")


def test_duong_co_ma_phuong_thuc_khong_thi_phan_biet_duoc_405_va_404():
    assert bt.tim("PUT", f"{bt.TIEN_TO}/ledger") is None
    assert bt.duong_ton_tai(f"{bt.TIEN_TO}/ledger")


# ── bang tuyen ↔ ham: hai chieu ───────────────────────────────────────────
def test_moi_tuyen_co_ham_va_moi_ham_co_tuyen():
    """⛔ Kiem HAI CHIEU. Mot chieu (tuyen → ham) bo sot ham chet: mot ham con
    trong `HAM` ma khong tuyen nao goi la ma khong ai chay, va ma khong ai chay
    la ma khong ai kiem."""
    tuyen = {t.ham for t in bt.BANG_TUYEN}
    assert tuyen - set(HAM) == set(), "tuyen tro toi ham khong ton tai"
    assert set(HAM) - tuyen == set(), "ham khong tuyen nao goi"
