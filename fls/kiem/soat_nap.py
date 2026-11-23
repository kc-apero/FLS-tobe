# -*- coding: utf-8 -*-
"""`F04` chặng 2 · **SOÁT MỘT LẦN NẠP** — thuần, ⛔ không dùng mạng.

⭐⭐ **Chặng 1 tra lời *"FLS dựng ra có ĐÚNG không?"* — 8.338/8.338. Chặng 2
   tra lời một câu KHÁC:** *"FLS bắt được gì mà chặng `Run` của trang tính
   ⛔ KHÔNG bắt?"* ⇒ Tám luật dưới đây **⛔ không phải do tôi nghĩ ra** — chúng
   sinh từ `tools/do_soat_nap.py`, đo trên **một lần nạp thật 8.338 dòng**.

⛔⛔ **BA HẠNG, và việc phân hạng ⛔ KHÔNG PHẢI nới cổng cho xanh** *(`R-A5`)*.
   Nó tra lời một câu khác hẳn: **khuyết tật này là của AI?**

     `CHAN` — **lỗi của FLS.** Nạp sai, mất dòng. ⇒ ĐỎ, và **chặn**.
     `CO`   — **khuyết tật có sẵn trong dữ liệu kế toán.** ⇒ ĐỎ, **báo to**,
              nhưng ⛔ **không chặn**: chặn ở đây nghĩa là FLS ⛔ không bao giờ
              nạp được gì, và **những dòng ấy là TIỀN THẬT** — vứt chúng đi thì
              vi phạm *"⛔ 0 dòng rơi im lặng"*. Chúng phải vào **hàng chờ có
              lý do**, ⛔ không bị bỏ.
     `CANH` — **hiện SẠCH.** Giữ để bắt trôi về sau. ⛔ Không được lặng lẽ bỏ
              chỉ vì nó đang xanh.

⭐⭐⭐ **Phát hiện lớn nhất của chặng 2 nằm ở `S5`.** Chặng 1 đếm **31** mã bị
   hạ xuống kiểu `float` ở `Bank Transactions`. Đo lại ở **nguồn** `R |`:
   **0 / 8.338**. ⇒ ⛔ **Thủ phạm là chính chặng `Run` của trang tính**, và
   FLS ⛔ không tái tạo lỗi ấy. Đây là **giá trị đo được** của việc thay cú đẩy,
   ⛔ không phải một lời hứa.

⛔ **Luật chung, kế thừa `nguon_song`: ĐO ĐƯỢC 0 THỨ ⇒ ⛔ KHÔNG ĐẠT.**
   Xanh trên tập rỗng là **chưa đo**, ⛔ không phải **đạt**.
"""
from __future__ import annotations

import re
from collections import Counter
from typing import NamedTuple, Sequence

# ⭐ **MOT** ban khai vi tri cot — **import** tu `sao_ke`, ⛔ khong tra lai
#    bang chuoi o day. Ban dau toi go `_I["Reference number"]`… va bai
#    `test_CHI_MOT_BAN_KHAI_ANH_XA_trong_ca_he` **do ngay** — dung nhu y muon:
#    no ⛔ khong phan biet duoc "tra cuu" voi "khai lai", va **⛔ khong nen**,
#    vi ca hai deu tao mot cho de lech.
from fls.adapters.sao_ke import (I_CO, I_MA, I_NGAY, I_NO, I_TE,  # noqa: F401
                                 I_XUAT_XU)

NGAY, TE, NO, CO, MA, XUAT_XU = I_NGAY, I_TE, I_NO, I_CO, I_MA, I_XUAT_XU

CHAN, CO_, CANH = "CHAN", "CO", "CANH"

_RE_MA_FLOAT = re.compile(r"^\d+\.0+$")
_RE_SERI = re.compile(r"^\d+(\.0+)?$")
_RE_NGAY_CHUOI = re.compile(r"^\d{1,2}/\d{1,2}/\d{4}$")


class KetQuaSoat(NamedTuple):
    ten: str
    hang: str           # CHAN | CO | CANH
    dat: bool
    da_do: int          # ⛔ 0 ⇒ ⛔ KHONG dat, du ⛔ khong thay loi nao
    thong_diep: str
    # ⭐⭐⭐ CHI SO (0-based) cua nhung dong LAM luat nay do — them 11/09,
    #   dong `GAP-NAP-01`.
    #
    # ⛔⛔ **Vi sao truong nay phai co.** Truoc no, `nap_lo` chi biet *"luat nao
    #   trot"* chu ⛔ khong biet *"dong nao lam trot"*, nen no gan **cau ly do
    #   cua CA LO** cho **moi** dong. Do that tren so 11/09:
    #
    #     `S3 · moi dong phai co TIEN` gan cho 2.596 dong — 2.596 dong ay
    #        **DEU CO TIEN**. Bao oan **100%**.
    #     `S7 · dong trung HOAN TOAN`  gan cho 5.952 dong — chi **66** that su
    #        trung. Bao oan **98,9%**.
    #
    # ⇒ Ke toan mo hang cho va doc mot cau **sai** ve dong dang o truoc mat.
    #   Mot hang cho nhu the ⛔ khong ai doc lan thu hai.
    #
    # ⚠ `()` ⛔ KHONG co nghia *"khong dong nao xau"* — no co nghia ***"luat nay
    #   ⛔ khong chi ra duoc dong"***. Bon luat `S1`/`S6`/`S8`/`S10` do o muc
    #   SHEET hay muc BAN KHAI, chung **that su** ⛔ khong co dong de chi. Hai
    #   nghia ay phai phan biet duoc o noi dung, va `nap_lo` phan biet.
    dong_xau: tuple[int, ...] = ()

    @property
    def xanh(self) -> bool:
        return self.dat and self.da_do > 0


def _rong(ten: str, hang: str, gi: str) -> KetQuaSoat:
    return KetQuaSoat(ten, hang, False, 0,
                      "⛔ do duoc 0 %s — xanh tren tap RONG la CHUA DO, "
                      "⛔ khong phai dat" % gi)


def _o(hang_dl: Sequence, i: int) -> str:
    return str(hang_dl[i]).strip() if i < len(hang_dl) else ""


def _co_tien(hang_dl: Sequence) -> bool:
    return any(v and v not in ("0", "0.0")
               for v in (_o(hang_dl, NO), _o(hang_dl, CO)))


def _hinh_ngay(v: str) -> str:
    if _RE_SERI.match(v):
        return "seri"
    if _RE_NGAY_CHUOI.match(v):
        return "chuoi"
    return "khac"


# ── S1 · CHAN ──────────────────────────────────────────────────────────────
def s1_ba_duong_can(theo_sheet: dict[str, tuple[int, int, int, int]]
                    ) -> KetQuaSoat:
    """`{sheet: (vao, ra, rong, loi)}` — `ra+rong+loi` PHAI bang `vao`.

    ⛔ Lech la **dong roi IM LANG**, va do la loi cua FLS ⇒ hang `CHAN`.
    """
    ten = "S1 · ba duong can — ⛔ 0 dong roi im lang"
    if not theo_sheet:
        return _rong(ten, CHAN, "sheet")
    hong = {s: t for s, t in theo_sheet.items() if t[1] + t[2] + t[3] != t[0]}
    if hong:
        vd = "; ".join("%s vao %d ≠ ra %d+rong %d+loi %d" % (s, *t)
                       for s, t in sorted(hong.items())[:3])
        return KetQuaSoat(ten, CHAN, False, len(theo_sheet),
                          "⛔ %d/%d sheet ⛔ khong can — %s"
                          % (len(hong), len(theo_sheet), vd))
    n = sum(t[0] for t in theo_sheet.values())
    return KetQuaSoat(ten, CHAN, True, len(theo_sheet),
                      "%d sheet · %d dong vao, ba duong can het" % (len(theo_sheet), n))


# ── S2 · CO ────────────────────────────────────────────────────────────────
def s2_co_tien_thi_phai_co_ma(rows: list[Sequence]) -> KetQuaSoat:
    """Dong CO TIEN ma ⛔ khong co ma ⇒ ⛔ khong truy nguoc ve sao ke duoc.

    ⛔ Hang `CO`: day la **tien that** trong so ke toan. Chan lai la vut tien.
    """
    ten = "S2 · co tien thi phai co MA"
    if not rows:
        return _rong(ten, CO_, "dong")
    xau = [i for i, r in enumerate(rows) if _co_tien(r) and not _o(r, MA)]
    if xau:
        return KetQuaSoat(ten, CO_, False, len(rows),
                          "⛔ %d/%d dong co tien ma ⛔ KHONG co ma — "
                          "⛔ khong ghep PM duoc, phai vao hang cho"
                          % (len(xau), len(rows)), tuple(xau))
    return KetQuaSoat(ten, CO_, True, len(rows),
                      "%d dong, dong nao co tien deu co ma" % len(rows))


# ── S3 · CO ────────────────────────────────────────────────────────────────
def s3_moi_dong_phai_co_tien(rows: list[Sequence]) -> KetQuaSoat:
    ten = "S3 · moi dong phai co TIEN (No hoac Co)"
    if not rows:
        return _rong(ten, CO_, "dong")
    xau = [i for i, r in enumerate(rows) if not _co_tien(r)]
    if xau:
        return KetQuaSoat(ten, CO_, False, len(rows),
                          "⛔ %d/%d dong ⛔ khong co tien ca hai ve — "
                          "mot dong khong tien ⛔ khong phai giao dich"
                          % (len(xau), len(rows)), tuple(xau))
    return KetQuaSoat(ten, CO_, True, len(rows),
                      "%d dong deu co tien" % len(rows))


# ── S4 · CO ────────────────────────────────────────────────────────────────
def s4_moi_dong_phai_co_tien_te(rows: list[Sequence]) -> KetQuaSoat:
    """⛔ Thieu don vi tien te thi con so ⛔ khong co nghia — `1.000` la gi?"""
    ten = "S4 · moi dong phai co DON VI TIEN TE"
    if not rows:
        return _rong(ten, CO_, "dong")
    xau = [i for i, r in enumerate(rows) if not _o(r, TE)]
    if xau:
        return KetQuaSoat(ten, CO_, False, len(rows),
                          "⛔ %d/%d dong ⛔ khong co don vi tien te — "
                          "con so tran ⛔ khong quy doi duoc"
                          % (len(xau), len(rows)), tuple(xau))
    return KetQuaSoat(ten, CO_, True, len(rows),
                      "%d dong deu co don vi tien te" % len(rows))


# ── S5 · CANH ──────────────────────────────────────────────────────────────
def s5_ma_khong_bi_ha_kieu(rows: list[Sequence]) -> KetQuaSoat:
    """⭐⭐ Ma **⛔ khong duoc** mang duoi `.0`.

    ⭐⭐⭐ Do duoc: nguon `R |` **0/8.338**, trong khi `Bank Transactions` co
    **31**. ⇒ Chinh chang `Run` cua trang tinh la thu pham; FLS ⛔ khong tai
    tao loi ay. Giu luat nay de **neu FLS bao gio lam hong ma, no DO ngay**.
    """
    ten = "S5 · ma ⛔ khong bi ha xuong kieu `float`"
    if not rows:
        return _rong(ten, CANH, "dong")
    xau = [i for i, r in enumerate(rows) if _RE_MA_FLOAT.match(_o(r, MA))]
    if xau:
        return KetQuaSoat(ten, CANH, False, len(rows),
                          "⛔ %d/%d ma mang duoi `.0` — FLS dang LAM HONG ma, "
                          "dung cai loi ma no sinh ra de tranh"
                          % (len(xau), len(rows)), tuple(xau))
    return KetQuaSoat(ten, CANH, True, len(rows),
                      "%d dong, ⛔ 0 ma bi ha kieu" % len(rows))


# ── S6 · CANH ──────────────────────────────────────────────────────────────
def s6_mot_sheet_mot_kieu_ngay(rows: list[Sequence]) -> KetQuaSoat:
    """MOT sheet chi duoc dung MOT kieu ngay.

    ⚠ Do duoc: doi hinh chia doi **4.172 chuoi / 4.166 seri**, nhung **tung
    sheet thi nhat quan** *(0/60 tron)*. ⇒ Tron kieu **trong mot sheet** la
    dau hieu nguoi go tay lech khuon — bat duoc som thi re.
    """
    ten = "S6 · mot sheet chi mot kieu ngay"
    if not rows:
        return _rong(ten, CANH, "dong")
    theo: dict[str, set[str]] = {}
    for r in rows:
        theo.setdefault(_o(r, XUAT_XU), set()).add(_hinh_ngay(_o(r, NGAY)))
    tron = {s: k for s, k in theo.items() if len(k) > 1}
    if tron:
        vd = "; ".join("%s: %s" % (s, "+".join(sorted(k)))
                       for s, k in sorted(tron.items())[:3])
        return KetQuaSoat(ten, CANH, False, len(theo),
                          "⛔ %d/%d sheet TRON kieu ngay — %s"
                          % (len(tron), len(theo), vd))
    return KetQuaSoat(ten, CANH, True, len(theo),
                      "%d sheet, moi sheet mot kieu ngay" % len(theo))


# ── S7 · CO ────────────────────────────────────────────────────────────────
def s7_dong_trung_hoan_toan(rows: list[Sequence]) -> KetQuaSoat:
    """Trung **hoan toan** = cung xuat xu + ngay + ma + No + Co.

    ⛔⛔ **`Num` CO Y ⛔ khong nam trong khoa.** `Num` do chinh FLS sinh ra, nen
    dua no vao khoa thi moi dong deu khac nhau va phep kiem **⛔ khong bao gio
    do duoc**. Mot phep kiem tu lam minh xanh la mot cong da chet.

    ⚠ Hang `CO`, ⛔ khong phai `CHAN`: hai lan chuyen y het nhau trong mot ngay
    **co the la that**. Day la co **cho NGUOI xem**, ⛔ khong phai ket luan.
    """
    ten = "S7 · dong trung HOAN TOAN (⛔ khong tinh `Num`)"
    if not rows:
        return _rong(ten, CO_, "dong")
    khoa = [(_o(r, XUAT_XU), _o(r, NGAY), _o(r, MA), _o(r, NO), _o(r, CO))
            for r in rows]
    dem = Counter(khoa)
    trung = {k: v for k, v in dem.items() if v > 1}
    if trung:
        # ⭐ Chi so cua **chinh nhung dong trung** — ⛔ khong phai ca lo.
        #   Do 11/09: ban cu gan cau nay cho **5.952** dong trong khi chi
        #   **66** that su trung *(bao oan 98,9%)*.
        xau = tuple(i for i, k in enumerate(khoa) if k in trung)
        return KetQuaSoat(ten, CO_, False, len(rows),
                          "⛔ %d khoa trung · %d/%d dong lien quan — "
                          "can NGUOI xem, ⛔ khong tu ket luan"
                          % (len(trung), sum(trung.values()), len(rows)), xau)
    return KetQuaSoat(ten, CO_, True, len(rows),
                      "%d dong, ⛔ 0 dong trung hoan toan" % len(rows))


# ── S8 · CO ────────────────────────────────────────────────────────────────
def s8_xuat_xu_co_trong_danh_muc(nguon: set[str],
                                 danh_muc: set[str]) -> KetQuaSoat:
    """Moi sheet DA NAP phai co trong `BankAccountList`.

    ⛔⛔ **`nguon` la tap sheet DA NAP, ⛔ KHONG suy tu `rows` — va do la lan
    sua thu HAI cua luat nay.** Ban dau toi lay `{xuat xu cua tung dong}`.
    Chay that: no bao **1** sheet la, trong khi phep do rieng chi ra **2**.
    Chenh o dau? Sheet thu hai ra **0 dong** ⇒ ⛔ khong co dong nao mang ten
    no ⇒ no **bien mat khoi chinh phep kiem sinh ra de tim no**.
    ⭐ Cung mot lop loi voi vu *"khoa dict bang TEN tai khoan"* o cong #17:
    **suy mot tap tu DU LIEU thay vi lay tu DAU VAO DA KHAI** thi cai vang
    mat se vang mat lan thu hai, trong im lang.

    ⛔⛔ **Hang nay tung la `CHAN`, va do la loi cua TOI — sua sau khi DO.**
    Ly do cu: *"tien vao so ma ⛔ khong ai biet thuoc ve dau"*. Nhung lan chay
    that dau tien cho ra **dung hai** truong hop, va ca hai la **danh muc GO
    NHAM MOT KY TU** *(danh muc thua `'1'` · thua `'7'`, giong 98%)* — tuc
    khuyet tat cua **ke toan**, ⛔ **khong** phai cua FLS. Ma dinh nghia `CHAN`
    do chinh toi viet la *"loi cua FLS"* ⇒ xep `CHAN` la **tu mau thuan**.

    ⭐⭐⭐ Va cai gia tri that o day: **`L9` cua cong #17 nhin dau KIA cua CUNG
    mot khuyet tat** *(*"tai khoan `Active` ⛔ khong co sheet"*)* va ket luan
    **SAI** — no bao **thieu 2 sheet**, trong khi ca hai sheet **DEU TON TAI
    va DEU co du lieu**. Hai dau nhin vao nhau moi doc ra duoc *"go nham"*.
    ⇒ ⛔ Mot cong nhin **mot chieu** thi chan doan duoc **trieu chung**, ⛔ khong
    chan doan duoc **benh**.

    ⚠ ⛔ Van la DO, va van phai **sach truoc khi day** *(chang 3)*: mot sheet
    la trong danh sach nap la tien **⛔ khong doi soat duoc**.
    """
    ten = "S8 · xuat xu phai co trong danh muc"
    if not nguon or not danh_muc:
        return _rong(ten, CO_, "sheet nap/muc danh muc")
    la = sorted(nguon - danh_muc)
    if la:
        return KetQuaSoat(ten, CO_, False, len(nguon),
                          "⛔ %d/%d sheet nap ⛔ KHONG co trong danh muc — %s"
                          % (len(la), len(nguon), ", ".join(la[:3])))
    return KetQuaSoat(ten, CO_, True, len(nguon),
                      "%d sheet nap, deu co trong danh muc" % len(nguon))


def s10_hai_ban_khai_cung_cot(
        khai: dict[str, dict[str, int]],
        dai: dict[str, dict[str, int | None]]) -> KetQuaSoat:
    """⛔⛔ **HAI bản khai của cùng một phép ánh xạ phải trỏ CÙNG một cột.**

    ⭐ Đây là luật **duy nhất** trong bộ này ⛔ **không** nhìn vào dữ liệu — nó
      nhìn vào **hai bản khai**:

        ⓐ **dòng 1** của sheet `R |`                    → FLS đọc
        ⓑ `Range_Condition/Debit/Credit` ở danh mục      → **script `Run` đọc**

    ⛔⛔ **Vì sao phải có, và vì sao ⛔ không luật nào khác thay được.** Sửa dòng
       1 mà quên danh mục *(hoặc ngược lại)* thì FLS và trang tính **đọc hai cột
       khác nhau**, và **cả hai vẫn chạy bình thường**:

         · ⛔ không câu lệnh nào lỗi;
         · ⛔ không dòng nào rơi — **`S1` vẫn CÂN**;
         · số tổng vẫn **trông hợp lý**.

       ⇒ Lớp khuyết tật này ⛔ **không phép kiểm nào trên MỘT phía bắt được**.
         Nó chỉ lộ ra khi có người đối chiếu **từng dòng** với sao kê gốc — tức
         là ⛔ **không bao giờ**.

    ⭐ **Hạng `CHẶN`, và ở đây hạng ấy ĐÚNG** *(khác `S8`, chỗ tôi từng xếp sai)*:
      hai bản khai lệch nghĩa là **FLS đang đọc sai cột**, tức **lỗi của FLS**,
      ⛔ không phải khuyết tật có sẵn của kế toán.

    ⛔ **Trường nào ⛔ không suy được cột thì đếm là CHƯA ĐO, ⛔ không đếm là
       KHỚP.** Đo 08/09: `R | CNC` và `R | Pingpong` có **6 ô `Range_*` RỖNG**.
       Cộng chúng vào vế *"khớp"* là **tự cho điểm trên tập rỗng**.
    """
    ten = "S10 · hai ban khai tro CUNG mot cot"
    chung = sorted(set(khai) & set(dai))
    if not chung:
        return _rong(ten, CHAN, "nguon co CA HAI ban khai")

    khop = lech = chua_do = 0
    xau: list[str] = []
    for s in chung:
        for t, c in sorted(dai[s].items()):
            k = khai[s].get(t)
            if c is None or k is None:
                chua_do += 1
            elif k == c:
                khop += 1
            else:
                lech += 1
                if len(xau) < 3:
                    xau.append("%s·%s: dong1=%d danh muc=%d" % (s, t, k, c))

    if khop == 0:
        return _rong(ten, CHAN, "phep so doc duoc (moi o deu ⛔ khong suy duoc)")
    if lech:
        return KetQuaSoat(
            ten, CHAN, False, khop + lech,
            "⛔ %d/%d phep so LECH — FLS va trang tinh dang doc HAI COT KHAC "
            "NHAU, va ca hai deu 'chay binh thuong': %s"
            % (lech, khop + lech, " · ".join(xau)))
    return KetQuaSoat(
        ten, CHAN, True, khop,
        "%d phep so, 0 lech tren %d nguon%s"
        % (khop, len(chung),
           " (⚠ %d o ⛔ khong suy duoc dai — CHUA DO, ⛔ khong tinh la khop)"
           % chua_do if chua_do else ""))


def chan_lai(kq: list[KetQuaSoat]) -> list[KetQuaSoat]:
    """Chi hang `CHAN` moi **chan** lan nap. Hang `CO`/`CANH` bao to, ⛔ khong chan."""
    return [k for k in kq if k.hang == CHAN and not k.xanh]
