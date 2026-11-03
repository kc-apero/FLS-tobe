"""BANG CHUNG cho `GAP-REC-01` — doi soat so ITL voi SO KE TOAN TONG HOP.

★ Vi sao file nay quan trong hon mot phep thu. No sua mot con so da di vao tai
lieu va vao dau moi nguoi: *"2.310 dong lech thoi diem bat dau dung dich vu"*.

Do lai, tai hien DUNG ca nam con so `FALSE` cua sheet, roi tach ra:

    phep kiem       FALSE   chenh THAT   CHI la dinh dang
    HD Code           552          552                  0
    Loai giao dich    146          146                  0
    Bat dau DV      2.310          165              2.145
    Ket thuc DV     2.308          168              2.140
    ID Vendor          39           39                  0
    ------------------------------------------------------
    TONG            5.355        1.070              4.285

⇒ Hai cot thoi diem dich vu: **165 va 168 chenh THAT**, ⛔ khong phai 2.310 va
2.308. **4.285 o** chi la mot ben luu ky dang CHU, ben kia dang SO:
`GL='202412'` (text) vs `Ledge=202412.0` (number). Cung gia tri, khac kieu — va
`=` cua Google tra FALSE.

⚠ Ba phep con lai (`hd`, `pay_type`, `id_payee`) thi **0 o** thuoc lop dinh dang
— lech cua chung la lech THAT, khong duoc lay ket luan cua hai cot dich vu ma
suy rong ra.

★★ Va lop benh dinh dang TU LIEN trong FLS: `svc_start`/`svc_end` khai kieu
`date` trong `fls_itl`, nen ca hai ben deu la ngay co kieu. **4.285 o** nay het
duong sinh ra — bien mat bang CAU TRUC, khong phai bang cong.

★★★ HUONG CUA SU THAT — owner chot 2026-08-26, `QD-ITL-52`:
  `Report I General Ledger`  = ban THUONG NGUON, gia tri TRUOC khi ke toan sua
  `ITL Ledge` (file ADJUSTED) = **BAN FINAL**, la so co tham quyen

⇒ Doi so tay hoan toan: lech giua hai ben **KHONG phai loi**. No do **khoi luong
  ke toan da sua**, khong do cai gi sai. Con so 7.026 o dong duoi day la mot
  con so BINH THUONG, ⛔ khong phai bao dong.
⇒ `GAP-REC-02` DONG. Va `GAP-REC-01` (bang doi soat) **thu hep manh**: khong can
  doi soat voi so nay. Neu sau nay can doi soat, la voi HE THONG KE TOAN THAT
  (MISA), mot viec khac han va ngoai pham vi hien tai.
⇒ Va day la XAC NHAN cho thuoc chuan: `ITL Ledge` dung la dich phai doc — dung
  cai ma `fls/oracle/` dang lam.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
from collections import Counter

import pytest

F = pathlib.Path(__file__).resolve().parents[1] / "fixture" / "doi_soat_gl.json"
CHECKSUM = "2756446d27669253"
DONG_GOC = 9219
FALSE_SHEET = {"hd": 552, "pay_type": 146, "svc_start": 2310,
               "svc_end": 2308, "id_payee": 39}


@pytest.fixture(scope="module")
def goi():
    return json.loads(F.read_text(encoding="utf-8"))


def test_hien_vat_khong_bi_sua(goi):
    tinh = hashlib.sha256(json.dumps(goi["cap"], ensure_ascii=False,
                                     separators=(",", ":")).encode()).hexdigest()[:16]
    assert tinh == CHECKSUM == goi["checksum_noi_dung"]
    assert goi["dong_goc"] == DONG_GOC


def _dem(goi, ben: int) -> tuple[Counter, Counter, Counter]:
    """ben=1 -> so voi Classifying · ben=2 -> so voi Final."""
    lech, kieu, gia_tri = Counter(), Counter(), Counter()
    for khoi, gl, cls, fin, n in goi["cap"]:
        ta = (cls, fin)[ben - 1]
        if gl == ta:
            continue
        lech[khoi] += n
        (kieu if gl[1] != ta[1] else gia_tri)[khoi] += n
    return lech, kieu, gia_tri


def test_TAI_HIEN_dung_nam_con_so_FALSE_cua_sheet(goi):
    """★ Neu phep do khong tai hien duoc so cua chinh sheet thi moi ket luan
    rut ra tu no deu vo nghia. Day la phep thu phai xanh TRUOC."""
    lech, _, _ = _dem(goi, 1)
    assert dict(lech) == FALSE_SHEET


def test_bon_phan_nam_lech_la_KHAC_KIEU_chu_khong_phai_chenh_that(goi):
    """★★ Sua con so 2.310 da di vao tai lieu."""
    nghiem, _, _ = _dem(goi, 1)
    that = _dem_bo_kieu(goi, 1)
    chi_dinh_dang = {k: nghiem[k] - that[k] for k in FALSE_SHEET}

    # hai cot thoi diem dich vu: phan lon chi la dinh dang
    assert (that["svc_start"], chi_dinh_dang["svc_start"]) == (165, 2145)
    assert (that["svc_end"], chi_dinh_dang["svc_end"]) == (168, 2140)
    # ⛔ ba phep con lai: 0 o thuoc lop dinh dang — lech la lech THAT
    for k in ("hd", "pay_type", "id_payee"):
        assert chi_dinh_dang[k] == 0, k
        assert that[k] == FALSE_SHEET[k]
    assert sum(nghiem.values()) == 5355
    assert sum(that.values()) == 1070
    assert sum(chi_dinh_dang.values()) == 4285


def _dem_bo_kieu(goi, ben: int) -> Counter:
    """So sau khi BO khac biet kieu — de ket luan ve GIA TRI khong bi lop benh
    kieu lam mo. `202412` (text) va `202412.0` (so) coi la bang nhau."""
    def z(v):
        x = v[0]
        if x is None:
            return ""
        if isinstance(x, float) and x.is_integer():
            return str(int(x))
        return str(x).strip()
    lech: Counter = Counter()
    for khoi, gl, cls, fin, n in goi["cap"]:
        if z(gl) != z((cls, fin)[ben - 1]):
            lech[khoi] += n
    return lech


def test_GL_mang_ban_TRUOC_KHI_SUA__da_duoc_owner_XAC_NHAN(goi):
    """★ Phep thu nay gio la BANG CHUNG cho `QD-ITL-52`, khong con la bao dong.

    Do that cho thay `Report I General Ledger` khop `Classifying` (ban tho) sat
    hon `Final` (ban da sua) RAT NHIEU. Owner xac nhan: dung, so do la ban
    thuong nguon; ban final la chinh `ITL Ledge`.

    Do ca hai cach, ca hai deu cung ket luan:

        cach so             theo Classifying   theo Final
        nghiem ngat                5.355        40.755
        bo khac biet kieu          1.070        35.878

    ★ Ro nhat o hai cot thoi diem dich vu, sau khi bo lop benh kieu:
        theo Classifying   165 / 168      <- gan nhu khop
        theo Final       7.026 / 7.024    <- lech 76% so

    ⇒ Nen con so 7.026 duoi day **do khoi luong da sua**, ⛔ khong do loi. Neu
      no TIEN VE 0 thi moi dang lo — nghia la ke toan thoi sua, hoac ban sua
      dang bi ghi de bang ban tho.
    """
    nghiem_cls, _, _ = _dem(goi, 1)
    nghiem_fin, _, _ = _dem(goi, 2)
    bo_cls = _dem_bo_kieu(goi, 1)
    bo_fin = _dem_bo_kieu(goi, 2)

    for k in FALSE_SHEET:                      # ca hai cach do, moi khoi
        assert nghiem_fin[k] > nghiem_cls[k], k
        assert bo_fin[k] > bo_cls[k], k

    assert sum(nghiem_cls.values()) == 5355
    assert sum(bo_cls.values()) == 1070
    # sau khi bo lop benh kieu, hai cot dich vu gan nhu khop voi Classifying
    assert (bo_cls["svc_start"], bo_cls["svc_end"]) == (165, 168)
    assert (bo_fin["svc_start"], bo_fin["svc_end"]) == (7026, 7024)


def test_lop_benh_dinh_dang_KHONG_tu_bien_mat__toi_da_viet_SAI():
    """⛔ TOI DA VIET SAI, va lan nap THAT lat lai.

    Cau cu cua toi: *"`svc_start`/`svc_end` khai kieu `date` — khong con chuyen
    'mot ben chu mot ben so'. 4.285 o thuoc lop nay het duong sinh ra."*

    Nghe rat gon. Nhung no dua tren mot gia dinh CHUA DO: rang hai cot do la
    NGAY. Lan nap that dau tien (2026-08-26) do thang vao so:

        svc_start  39 gia tri khac nhau ·  9 loai KHONG phai YYYYMM
        svc_end    57 gia tri khac nhau · 10 loai KHONG phai YYYYMM
        that su co trong so: 'thang 5' · 'Thang 4' · 'TPCI' · '2025.07'
                             '20509' · '252512' · '2027' · '45962'

    Va don vi la KY (thang), khong phai ngay — kieu `date` buoc phai bia mot
    ngay trong thang ma nguon khong he co (`INV-I16`). ⇒ `text` (migration 0005).

    ★ Nen dieu ma FLS thuc su chua duoc KHONG phai "lop benh nay bien mat".
    La: no khong con IM LANG nua. Cu the, ba cai khac nhau:
      ① gia tri duoc chep NGUYEN VAN ⇒ parity 100% tung o, khong ai "sua cho
         dung kieu" roi mat duong quay ve;
      ② `*_thyt` NULL o cho may tu bia ⇒ mot cho tuong minh de noi "o nay la
         may gan, khong phai nguoi go" (`QD-ITL-35`);
      ③ lech kieu vs hop dong duoc KHAI ra, dem duoc, va co CR dang mo
         (`LECH_HOP_DONG_V1`) — thay vi mot chu 'date' sua lang le.

    ⚠ Cai KHONG duoc chua: neu ke toan go 'thang 5' thi FLS van luu 'thang 5'.
    Do la dung — nhung no la mot mon no NGHIEP VU (chuan hoa danh muc ky), ⛔
    khong phai mot mon no ky thuat da tra xong.
    """
    from fls.contract.itl_contract import LECH_HOP_DONG_V1
    from fls.db.schema import TABLES
    cot = {c.name: c.type for c in TABLES["fls_itl"].columns}
    assert cot["svc_start"] == "text" and cot["svc_end"] == "text"
    assert cot["hd"] == "text" and cot["id_payee"] == "text"
    # va cai lech phai duoc KHAI, khong duoc bo qua
    assert {l[0] for l in LECH_HOP_DONG_V1} == {"svc_start", "svc_end"}
