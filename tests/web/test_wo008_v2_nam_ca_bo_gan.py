# -*- coding: utf-8 -*-
"""`WO-008` **vòng 2** — năm ca của nút `Bỏ gán` trên màn ghép *(`KQ-019`
`F-1`…`F-4`)*.

Spec: `BA-06` **v4.10** §4.5 mục ⓔ — đoạn ⭐⭐ *"NĂM ca của nút `Bỏ gán`"*
*(bảng ①…⑤ + bảng 5 trạng thái)*.

⛔⛔ **Vì sao tệp này nạp `hop_thoai.js` THẬT và ⛔ thay hàm `HT` nào.**
Bài vòng 1 *(`test_wo008_chu_man_sau_bo_ghep.py`)* dựng bẫy `BAY_HOP` **tự
định nghĩa** `HT.hoi` — một hàm `hop_thoai.js` ⛔ bao giờ xuất *(nó trả đúng
`{ mo, dong, loi_trong_hop }`)*. Bẫy trả `true` ⇒ mọi bài nhánh chùm xanh,
trong khi trên trình duyệt thật cú bấm chết ở `TypeError: HT.hoi is not a
function` — **0** hộp, **0** lượt `/unmatch` *(`KQ-019 F-1`, máy `8099`)*. Đó
là đúng lớp lỗi *"khuôn thử tự nhét"* của `11` §6. ⇒ Ở đây `HT.mo` chỉ bị
**bọc để đếm** *(gọi xuyên xuống hàm thật)*, và mọi nút trong hộp được bấm
bằng **chính `onclick`** mà `hop_thoai.js` gắn vào phần tử trong `#dlg-f`.

⭐ Mỗi bài đếm **mẫu số ≠ 0** trước khi kết luận *(`Đ3`)*; chiều ĐỎ ghi ở
docstring và đã **chạy thật** trên mã `124a067` *(`BG` vòng 2)*.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from fls.repo.man_ghep import khuon_the_lenh
from tests.web.khung_node import _chay, can_node
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

GOC = Path(__file__).resolve().parents[2]

#: ⭐ Bọc `HT.mo` THẬT để đếm — ⛔ thay. Gọi xuyên ⇒ `#scrim` / `#dlg-*` là
#: của hàm thật dựng ra.
DEM_HOP = """
  globalThis._HOP = [];
  const _mo_that = HT.mo;
  HT.mo = function (t, b, n) {
    _HOP.push({t, b, n: (n || []).map(x => x[0])});
    return _mo_that(t, b, n);
  };
  globalThis._nut_man = function (chu) {
    const ra = [];
    (function di(e) {
      if (e.tagName === 'BUTTON' && e.textContent.trim() === chu) ra.push(e);
      e.children.forEach(di);
    })(document.getElementById('ghep-goc'));
    return ra;
  };
  globalThis._nut_hop = chu => document.getElementById('dlg-f').children
    .filter(b => b.textContent === chu)[0];
  globalThis._dem = re => _GOI.filter(g => re.test(g[1])).length;
  globalThis._hop = function () {
    const s = document.getElementById('scrim');
    return {mo: s.classList.contains('on'),
            t: document.getElementById('dlg-t').textContent,
            b: document.getElementById('dlg-b').textContent,
            nut: document.getElementById('dlg-f').children.map(x => x.textContent),
            lop: document.getElementById('dlg-f').children.map(x => x.className)};
  };
  globalThis._man = () => document.getElementById('ghep-goc').textContent;
  globalThis._ngu = ms => new Promise(r => setTimeout(r, ms));
"""


def _bo_ba(itl_da_gan: list[int]) -> dict:
    """⭐ Bộ ba trạng thái lấy từ **hàm thật** `khuon_the_lenh` — ⛔ chép hằng
    *(`WO-008` Rủi ro vòng 2 ①: hai bản bộ ba lệch im lặng)*."""
    k = khuon_the_lenh({"pm_line_id": "X", "itl_da_gan": itl_da_gan})
    return {x: k[x] for x in ("trang_thai", "trang_thai_nhan", "trang_thai_mau")}


def _lenh(ma: str, itl: list[int]) -> dict:
    return dict(
        {"ma_lenh": ma, "noi_dung": "chi " + ma, "so_tien": "5000000.00",
         "curr": "VND", "loai_phieu": "PM", "itl_da_gan": list(itl),
         "nhom_du_truong": [],
         "gd_ds": [{"itl_id": i, "bac": "tien", "doc_no": "FT-%d" % i,
                    "amount": "5000000.00", "curr": "VND",
                    "doc_date": "2026-09-01", "da_gan": True} for i in itl]},
        **_bo_ba(itl))


#: Thân `unmatch` dạng cửa thật *(`fls/repo/ghi_tay.py::bo_ghep`)*.
def _than(da_bo: list[str], bo_qua: list | None = None) -> dict:
    return {"itl_id": 4242, "evt_id": 9, "ve_hang_cho": True,
            "da_bo": [{"pm_line_id": m, "amount": "1.00", "hinh": "A",
                       "lan": 1, "link_id": 1} for m in da_bo],
            "but_toan_dao": [{"field": "cdt1"}, {"field": "hd"}],
            "bo_qua": bo_qua or []}


BO_QUA_HD = [{"field": "hd", "nguon": "sua_tay", "value_after": "HD-NGUOI-B2",
              "adj_id": 20}]

CHUM2 = {"can_hoi": True, "so_dong": 2, "dong_lenh": [
    {"pm_line_id": "PWB-1", "amount": "3000000.00", "curr": "VND"},
    {"pm_line_id": "PWB-2", "amount": "2000000.00", "curr": "VND"}]}
CHUM1 = {"can_hoi": False, "so_dong": 1, "dong_lenh": []}


def _chay_ghep(kich_ban: str, *, dong: list[dict], tra: dict) -> dict:
    """Mở lệnh `dong[0]` trên màn ghép THẬT rồi chạy `kich_ban`.

    `tra` = `{đường: thân | {"no": lỗi}}` cho cửa giả. Ứng viên của mọi lệnh
    mặc định **một** dòng *(màn ⛔ bật Toàn sổ)*."""
    t = ["_TRA[%s] = %s;" % (json.dumps(k), json.dumps(
        v if isinstance(v, dict) and "no" in v else {"data": v},
        ensure_ascii=False)) for k, v in tra.items()]
    for d in dong:
        k = "/queue/lenh/%s/itl-candidates" % d["ma_lenh"]
        if k not in tra:
            t.append("_TRA[%s] = {data: {ung_vien: [{itl_id: 7, bac: 'tien', "
                     "amount: '1.00', curr: 'VND'}]}};" % json.dumps(k))
    return _chay(DEM_HOP + "\n".join(t) + """
      F01G.ST.dong = %s;
      await F01G.mo_lenh(%s);
      globalThis._TRUOC = _man();
    """ % (json.dumps(dong, ensure_ascii=False),
           json.dumps(dong[0]["ma_lenh"])) + kich_ban, tep=TEP_F01, vo=VO_F01)


# ═══ AC-7 · ca ② CHÙM — hộp HỎI dựng bằng `HT.mo` thật ══════════════════
DONG_CHUM = [_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242]),
             _lenh("PWB-3", [5000])]


@can_node
def test_AC7_chum__HOP_HOI_that_mo__Thoi_Go_ca_2__chua_ghi_truoc_khi_bam():
    """⛔ Chiều ĐỎ: gọi lại `HT.hoi` ⇒ `TypeError` ⇒ hộp ⛔ mở ⇒ ĐỎ; gọi
    `/unmatch` trước khi bấm ⇒ `unmatch` = 1 ⇒ ĐỎ."""
    r = _chay_ghep("""
      let loi = null;
      await F01G.bo_gan(F01G.ST.dong[0]).catch(e => { loi = String(e); });
      await _ngu(30);
      return {hop: _hop(), loi, chum: _dem(/\\/chum$/),
              unmatch: _dem(/\\/unmatch$/), so_hop: _HOP.length};
    """, dong=DONG_CHUM, tra={"/queue/4242/chum": CHUM2,
                             "/queue/4242/unmatch": _than(["PWB-1", "PWB-2"])})
    assert r["chum"] == 1, "⛔ không đo được: màn ⛔ hỏi cửa /chum"
    assert r["loi"] is None, r["loi"]
    h = r["hop"]
    assert r["so_hop"] == 1 and h["mo"] is True, r
    assert "CẢ 2" in h["t"], h["t"]
    assert "PWB-1" in h["b"] and "PWB-2" in h["b"], h["b"]
    assert h["nut"] == ["Thôi", "Gỡ cả 2"], h["nut"]
    assert "danger" in h["lop"][1] and "danger" not in h["lop"][0], h["lop"]
    assert r["unmatch"] == 0, "⛔ ghi trước khi người bấm Gỡ cả 2"


@can_node
def test_AC7_chum__bam_THOI__khong_ghi_hop_dong():
    """⛔ Chiều ĐỎ: `Thôi` mang hàm ghi ⇒ `unmatch` = 1 ⇒ ĐỎ."""
    r = _chay_ghep("""
      await F01G.bo_gan(F01G.ST.dong[0]);
      const mo_truoc = _hop().mo;
      await _nut_hop('Thôi').onclick();
      await _ngu(30);
      return {mo_truoc, hop: _hop(), unmatch: _dem(/\\/unmatch$/),
              tt: F01G.ST.dong.map(d => d.trang_thai)};
    """, dong=DONG_CHUM, tra={"/queue/4242/chum": CHUM2,
                             "/queue/4242/unmatch": _than(["PWB-1", "PWB-2"])})
    assert r["mo_truoc"] is True, "⛔ không đo được: hộp ⛔ mở trước khi bấm"
    assert r["unmatch"] == 0, r
    assert r["hop"]["mo"] is False, r["hop"]
    assert r["tt"] == ["da_gan", "da_gan", "da_gan"], r["tt"]


@can_node
def test_AC7_chum__bam_GO_CA_2__mot_luot_ghi__CA_HAI_the_ve_Chua_gan():
    """Ca ② ⇒ ca ③: mọi lệnh trong `da_bo[]` đổi tại chỗ; lệnh **ngoài**
    `da_bo` *(`PWB-3`, đối chứng)* giữ nguyên. Dòng tín hiệu nói *"gỡ cả 2
    lệnh chi"*.

    ⛔ Chiều ĐỎ: đổi thẻ theo `lenh` đang mở thay vì `da_bo[]` ⇒ `PWB-2`
    vẫn `da_gan` ⇒ ĐỎ."""
    r = _chay_ghep("""
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _nut_hop('Gỡ cả 2').onclick();
      await _ngu(80);
      return {hop: _hop(), unmatch: _dem(/\\/unmatch$/), man: _man(),
              dong: F01G.ST.dong.map(d => [d.ma_lenh, d.trang_thai,
                                           d.trang_thai_nhan, d.itl_da_gan])};
    """, dong=DONG_CHUM, tra={"/queue/4242/chum": CHUM2,
                             "/queue/4242/unmatch": _than(["PWB-1", "PWB-2"])})
    assert r["unmatch"] == 1, r
    chua = _bo_ba([])
    assert r["dong"][0] == ["PWB-1", chua["trang_thai"], chua["trang_thai_nhan"], []]
    assert r["dong"][1] == ["PWB-2", chua["trang_thai"], chua["trang_thai_nhan"], []]
    assert r["dong"][2][1] == "da_gan" and r["dong"][2][3] == [5000], r["dong"]
    assert "Đã bỏ gán khỏi giao dịch #4242" in r["man"], r["man"]
    assert "gỡ cả 2 lệnh chi" in r["man"], r["man"]
    assert r["hop"]["mo"] is False, r["hop"]


@can_node
def test_AC7_chum_bo_qua_CO__hop_hoi_DONG_roi_hop_Da_bo_ghep_MO():
    """Chùm **và** `bo_qua` ⛔ rỗng: hộp *"Đã bỏ ghép"* dùng **chính** `#scrim`
    của hộp hỏi. Ca ③ phải chạy **SAU** khi hộp hỏi đóng — chạy trước thì
    `dong()` của hộp hỏi đóng luôn hộp báo vừa mở.

    ⛔ Chiều ĐỎ: gọi `_sau_bo_gan` trực tiếp *(⛔ `setTimeout`)* trong hàm nút,
    với lượt đọc lại ứng viên chậm hơn `60ms` ⇒ hộp báo bị đóng ⇒ ĐỎ."""
    r = _chay_ghep("""
      const doc0 = FLS.doc;
      FLS.doc = async function (d, q) {
        if (/itl-candidates/.test(d)) await _ngu(120);   // đọc lại CHẬM
        return doc0(d, q);
      };
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _nut_hop('Gỡ cả 2').onclick();
      await _ngu(400);
      return {hop: _hop(), dem: _HOP.map(h => h.t), man: _man(),
              unmatch: _dem(/\\/unmatch$/)};
    """, dong=DONG_CHUM, tra={"/queue/4242/chum": CHUM2,
                             "/queue/4242/unmatch": _than(["PWB-1", "PWB-2"], BO_QUA_HD)})
    assert r["unmatch"] == 1, r
    assert r["dem"] == ["Bỏ gán sẽ gỡ CẢ 2 lệnh chi", "Đã bỏ ghép"], r["dem"]
    assert r["hop"]["mo"] is True and r["hop"]["t"] == "Đã bỏ ghép", r["hop"]
    assert "HD-NGUOI-B2" in r["hop"]["b"], r["hop"]["b"]
    assert "gỡ cả 2 lệnh chi" in r["man"], r["man"]


@can_node
@pytest.mark.parametrize("ma,cau", [
    ("FLS-MAT-KET-NOI", "Không nối được tới máy chủ FLS."),
    ("FLS-INTERNAL", "Máy gặp lỗi bên trong."),
])
def test_AC7_chum__GO_CA_2_cua_LOI__hop_O_NGUYEN__loi_TRONG_hop(ma, cau):
    """⛔ Chiều ĐỎ: nuốt lỗi *(⛔ `return false`)* ⇒ hộp đóng ⇒ ĐỎ; lỗi ra
    ngoài ⇒ `#dlg-b` ⛔ có câu ⇒ ĐỎ."""
    r = _chay_ghep("""
      _TRA['/queue/4242/unmatch'] = {no: new FLS.LoiCua(%s, 0, 'chi tiet may')};
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _nut_hop('Gỡ cả 2').onclick();
      await _ngu(30);
      return {hop: _hop(), unmatch: _dem(/\\/unmatch$/),
              tt: F01G.ST.dong.map(d => d.trang_thai)};
    """ % json.dumps(ma), dong=DONG_CHUM, tra={"/queue/4242/chum": CHUM2})
    assert r["unmatch"] == 1, "⛔ không đo được: nút ⛔ gọi cửa"
    assert r["hop"]["mo"] is True, r["hop"]
    assert cau in r["hop"]["b"], r["hop"]["b"]
    assert r["tt"] == ["da_gan", "da_gan", "da_gan"], r["tt"]


# ═══ AC-8 · ca ① lệnh ≥ 2 dòng tiền — hộp BÁO, 0 lượt ghi ═══════════════
@can_node
def test_AC8_lenh_HAI_giao_dich__hop_BAO_mot_nut__khong_chum_khong_unmatch():
    """⛔ Chiều ĐỎ: gọi `/chum` hay `/unmatch` ở ca ① ⇒ ĐỎ; gọi `HT.hoi` ⇒
    hộp ⛔ mở ⇒ ĐỎ."""
    r = _chay_ghep("""
      let loi = null;
      await F01G.bo_gan(F01G.ST.dong[0]).catch(e => { loi = String(e); });
      await _ngu(30);
      return {hop: _hop(), loi, so_hop: _HOP.length, chum: _dem(/\\/chum$/),
              unmatch: _dem(/\\/unmatch$/)};
    """, dong=[_lenh("PWB-1", [4242, 4243])], tra={})
    assert r["loi"] is None, r["loi"]
    h = r["hop"]
    assert r["so_hop"] == 1 and h["mo"] is True, r
    assert "2 giao dịch" in h["t"] + h["b"], h
    assert "Sổ ITL" in h["b"], h["b"]
    assert h["nut"] == ["Đã hiểu"], h["nut"]
    assert r["chum"] == 0 and r["unmatch"] == 0, r


def _dem_mau(goc: Path, mau: re.Pattern, duoi: str) -> dict[str, int]:
    ra: dict[str, int] = {}
    for p in sorted(goc.rglob("*" + duoi)):
        n = len(mau.findall(p.read_text(encoding="utf-8")))
        if n:
            ra[str(p.relative_to(GOC))] = n
    return ra


def test_AC8_KHONG_con_HT_hoi__ca_cho_goi_lan_cho_dinh_nghia_bay():
    """`AC-8 ⓒ`: `grep HT.hoi fls/web/tep` = **0** · định nghĩa `HT.hoi` trong
    `tests/web/**` = **0**. Mẫu số: chính phép quét **tìm thấy** `HT.mo` *(hàm
    thật)* ở cả hai nơi ⇒ mẫu ⛔ hỏng *(`Đ3`)*.

    ⛔ Chiều ĐỎ: thêm lại một chỗ gọi `HT.hoi(` hay một bẫy gán hàm ấy ⇒ ĐỎ.
    ⚠ Mẫu dựng từ **mảnh** để chính tệp này ⛔ tự khớp."""
    ten = "HT" + r"\." + "hoi"
    goi = re.compile(ten + r"\b")
    dinh_nghia = re.compile(ten + r"\s*=(?!=)")
    mo = re.compile("HT" + r"\." + "mo" + r"\b")
    tep_web = GOC / "fls" / "web" / "tep"
    tep_bai = GOC / "tests" / "web"
    assert _dem_mau(tep_web, mo, ".js"), "⛔ không đo được: quét ⛔ thấy HT.mo"
    assert _dem_mau(tep_bai, mo, ".py"), "⛔ không đo được: quét ⛔ thấy HT.mo"
    assert _dem_mau(tep_web, goi, ".js") == {}, "⛔ màn còn gọi một hàm hộp ⛔ có"
    assert _dem_mau(tep_bai, dinh_nghia, ".py") == {}, \
        "⛔ bài tự định nghĩa một hàm hộp mà hop_thoai.js ⛔ xuất"


# ═══ AC-9 · ca ③ bỏ gán XONG — thẻ đổi TẠI CHỖ + một dòng tín hiệu ══════
@can_node
def test_AC9_bo_gan_200_bo_qua_RONG__the_ve_Chua_gan__dong_tin_hieu__0_hop():
    """⛔ Chiều ĐỎ: bỏ bước cập nhật thẻ ⇒ *"Đang gán"* còn ⇒ ĐỎ; bỏ dòng tín
    hiệu ⇒ ĐỎ; gọi `tai_danh_sach` ⇒ lượt `lenh-da-gan`/`lenh-cho` > 0 ⇒ ĐỎ;
    nhảy sang lệnh kế ⇒ `ST.mo` ≠ `PWB-1` ⇒ ĐỎ."""
    dong = [_lenh("PWB-1", [4242]), _lenh("PWB-9", [])]
    r = _chay_ghep("""
      F01G.ST.chip = 'da_gan';
      const so_doc0 = _dem(/lenh-da-gan|lenh-cho/);
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _ngu(120);
      return {truoc: _TRUOC, man: _man(), so_hop: _HOP.length, mo: F01G.ST.mo,
              thu_tu: F01G.ST.dong.map(d => d.ma_lenh),
              doc_ds: _dem(/lenh-da-gan|lenh-cho/) - so_doc0,
              unmatch: _dem(/\\/unmatch$/),
              gan: _nut_man('Gán').length,
              bo: _nut_man('Bỏ gán').length + _nut_man('bỏ gán').length};
    """, dong=dong, tra={"/queue/4242/chum": CHUM1,
                         "/queue/4242/unmatch": _than(["PWB-1"])})
    assert "Đang gán với giao dịch" in r["truoc"], \
        "⛔ không đo được: màn ⛔ vẽ khối Đang gán trước cú bấm"
    assert r["unmatch"] == 1, r
    assert "Đang gán với giao dịch" not in r["man"], r["man"]
    assert ("↩ Đã bỏ gán khỏi giao dịch #4242 — lệnh về "
            + _bo_ba([])["trang_thai_nhan"]) in r["man"], r["man"]
    assert "Sổ giữ lịch sử." in r["man"], r["man"]
    assert "gỡ cả" not in r["man"], "⛔ ca một lệnh mà nói như chùm"
    assert r["so_hop"] == 0, "⛔ bo_qua rỗng mà vẫn mở hộp (BA-06 v4.8)"
    assert r["gan"] == 1 and r["bo"] == 0, r
    assert r["mo"] == "PWB-1" and r["thu_tu"] == ["PWB-1", "PWB-9"], r
    assert r["doc_ds"] == 0, "⛔ tải lại CẢ danh sách"


@can_node
def test_AC9_bo_ba_trang_thai_sau_bo_gan__TRUNG_khuon_the_lenh_THAT():
    """⭐ Đo **quan hệ**: bộ ba màn đặt sau bỏ gán ≡ bộ ba **hàm thật**
    `khuon_the_lenh` trả cho lệnh ⛔ gán; chip trên thẻ in đúng nhãn ấy.
    Mẫu số: bộ ba **trước** cú bấm ≡ `khuon_the_lenh` cho lệnh **đã** gán, và
    hai bộ **khác nhau** *(⛔ so hai thứ y hệt)*.

    ⛔ Chiều ĐỎ: đổi nhãn trong JS khác Python ⇒ ĐỎ."""
    r = _chay_ghep("""
      const bo_ba = d => ({trang_thai: d.trang_thai,
                           trang_thai_nhan: d.trang_thai_nhan,
                           trang_thai_mau: d.trang_thai_mau});
      const truoc = bo_ba(F01G.ST.dong[0]);
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _ngu(30);
      const chip = [];
      (function di(e) {
        if ((e.className || '').split(' ').includes('chip')) chip.push(e.textContent);
        e.children.forEach(di);
      })(document.querySelector('.wh1') || document.body);
      return {truoc, sau: bo_ba(F01G.ST.dong[0]), chip};
    """, dong=[_lenh("PWB-1", [4242])],
        tra={"/queue/4242/chum": CHUM1, "/queue/4242/unmatch": _than(["PWB-1"])})
    assert r["truoc"] == _bo_ba([4242]), r["truoc"]
    assert _bo_ba([4242]) != _bo_ba([]), "⛔ không đo được: hai bộ ba y hệt"
    assert r["sau"] == _bo_ba([]), (r["sau"], _bo_ba([]))
    assert _bo_ba([])["trang_thai_nhan"] in r["chip"], r["chip"]


@can_node
def test_AC9_bo_qua_CO__them_hop_Da_bo_ghep_MOT_lan():
    """`AC-4` giữ: `bo_qua` ⛔ rỗng ⇒ hộp *"Đã bỏ ghép"* **1** lần, *cộng*
    dòng tín hiệu."""
    r = _chay_ghep("""
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _ngu(150);
      return {so: _HOP.filter(h => h.t === 'Đã bỏ ghép').length, hop: _hop(),
              man: _man()};
    """, dong=[_lenh("PWB-1", [4242])],
        tra={"/queue/4242/chum": CHUM1,
             "/queue/4242/unmatch": _than(["PWB-1"], BO_QUA_HD)})
    assert r["so"] == 1 and r["hop"]["mo"] is True, r
    assert "HD-NGUOI-B2" in r["hop"]["b"] and r["hop"]["nut"] == ["Đã hiểu"], r
    assert "Đã bỏ gán khỏi giao dịch #4242" in r["man"], r["man"]


# ═══ AC-10 · tải — nút khoá, hai cú bấm = MỘT lượt ghi ══════════════════
@can_node
def test_AC10_hai_cu_bam_khi_cua_CHUA_tra__mot_luot_unmatch__nut_khoa():
    """Cửa `/unmatch` **treo** *(Promise chưa resolve)*. Bấm **nút thật** trên
    màn, rồi bấm lại cái nút vẽ lại — và gọi `bo_gan` lần nữa.

    ⛔ Chiều ĐỎ: bỏ khoá ⇒ **2** lượt ⇒ ĐỎ."""
    r = _chay_ghep("""
      let mo_khoa;
      const ghi0 = FLS.ghi;
      FLS.ghi = function (duong, than) {
        if (/unmatch$/.test(duong)) {
          _GOI.push(['ghi', duong, than]);
          return new Promise(r => { mo_khoa = () => r({data: %s, meta: {}}); });
        }
        return ghi0(duong, than);
      };
      const nut0 = _nut_man('Bỏ gán');
      if (nut0.length !== 1) return {loi: 'không đo được: ' + nut0.length + ' nút'};
      nut0[0]._nghe.click[0]();
      await _ngu(20);
      const dang = _nut_man('Bỏ gán').concat(_nut_man('bỏ gán'));
      const khoa = dang.map(b => !!b.disabled);
      dang.forEach(b => (b._nghe.click || []).forEach(f => f()));
      F01G.bo_gan(F01G.ST.dong[0]);
      await _ngu(20);
      const giua = _dem(/\\/unmatch$/);
      mo_khoa();
      await _ngu(60);
      return {khoa, giua, cuoi: _dem(/\\/unmatch$/), tt: F01G.ST.dong[0].trang_thai};
    """ % json.dumps(_than(["PWB-1"]), ensure_ascii=False),
        dong=[_lenh("PWB-1", [4242])], tra={"/queue/4242/chum": CHUM1})
    assert "loi" not in r, r
    assert r["khoa"] and all(r["khoa"]), f"⛔ nút ⛔ khoá khi chờ: {r['khoa']}"
    assert r["giua"] == 1 and r["cuoi"] == 1, r
    assert r["tt"] == _bo_ba([])["trang_thai"], r


# ═══ AC-11 · ca ⑤ cửa LỖI ngoài hộp — chữ trên màn, 0 Uncaught ══════════
@can_node
@pytest.mark.parametrize("ma,cau", [
    ("FLS-MAT-KET-NOI", "Không nối được tới máy chủ FLS."),
    ("FLS-INTERNAL", "Máy gặp lỗi bên trong."),
])
@pytest.mark.parametrize("cua", ["unmatch", "chum"])
def test_AC11_cua_LOI__Bo_gan_chua_xay_ra__the_giu_Da_gan__promise_RESOLVE(
        cua, ma, cau):
    """Promise của `bo_gan` **resolve** = đại diện **0** `Uncaught` *(trình
    nghe `click` ⛔ bọc gì)*. `/chum` lỗi ⇒ `/unmatch` **0**.

    ⛔ Chiều ĐỎ: bỏ `try/catch` ⇒ promise reject ⇒ ĐỎ; chỉ `console.error`
    ⇒ chữ ⛔ có trên màn ⇒ ĐỎ."""
    tra = {"/queue/4242/chum": CHUM1, "/queue/4242/unmatch": _than(["PWB-1"])}
    r = _chay_ghep("""
      _TRA['/queue/4242/%s'] = {no: new FLS.LoiCua(%s, 0, 'chi tiet may 42')};
      let reject = null;
      await F01G.bo_gan(F01G.ST.dong[0]).catch(e => { reject = String(e && (e.cau || e.message) || e); });
      await _ngu(120);
      return {reject, man: _man(), so_hop: _HOP.length,
              tt: F01G.ST.dong[0].trang_thai, unmatch: _dem(/\\/unmatch$/),
              chum: _dem(/\\/chum$/), lam_gi: new FLS.LoiCua(%s).lam_gi};
    """ % (cua, json.dumps(ma), json.dumps(ma)), dong=[_lenh("PWB-1", [4242])],
        tra=tra)
    assert r["chum"] == 1, "⛔ không đo được: màn ⛔ hỏi /chum"
    assert r["unmatch"] == (1 if cua == "unmatch" else 0), r
    assert r["reject"] is None, f"⛔ lỗi rơi ra trình nghe click: {r['reject']}"
    assert "Bỏ gán chưa xảy ra — Cửa lỗi: " + cau in r["man"], r["man"]
    assert "chi tiet may 42" in r["man"], r["man"]
    if r["lam_gi"]:
        assert r["lam_gi"] in r["man"], (r["lam_gi"], r["man"])
    assert r["tt"] == "da_gan", r["tt"]
    assert "Đang gán với giao dịch" in r["man"], "⛔ cửa lỗi mà thẻ thôi nói Đang gán"
    assert r["so_hop"] == 0, "⛔ cửa lỗi mà mở hộp"


# ═══ AC-12 · ca ④ đọc lại ứng viên LỖI — ③ vẫn xảy ra, TRƯỚC ═════════════
@can_node
def test_AC12_doc_lai_ung_vien_LOI__hop_bo_qua_VAN_mo__tin_hieu_va_dong_loi_doc():
    """⛔ Chiều ĐỎ: đặt `await mo_lenh` **trước** hộp + thẻ *(như vòng 1)* ⇒
    hộp ⛔ mở ⇒ ĐỎ; báo *"chưa xảy ra"* khi sổ đã ghi ⇒ ĐỎ."""
    r = _chay_ghep("""
      _TRA['/queue/lenh/PWB-1/itl-candidates'] = {no: new FLS.LoiCua('FLS-INTERNAL', 500)};
      let reject = null;
      await F01G.bo_gan(F01G.ST.dong[0]).catch(e => { reject = String(e); });
      await _ngu(150);
      return {reject, hop: _hop(), man: _man(), tt: F01G.ST.dong[0].trang_thai};
    """, dong=[_lenh("PWB-1", [4242])],
        tra={"/queue/4242/chum": CHUM1,
             "/queue/4242/unmatch": _than(["PWB-1"], BO_QUA_HD)})
    assert r["reject"] is None, r["reject"]
    assert r["hop"]["mo"] is True and "HD-NGUOI-B2" in r["hop"]["b"], r["hop"]
    assert "Đã bỏ gán khỏi giao dịch #4242" in r["man"], r["man"]
    assert "Chưa tải lại được giao dịch gợi ý: Máy gặp lỗi bên trong." in r["man"], r["man"]
    assert "Bỏ gán chưa xảy ra" not in r["man"], r["man"]
    assert r["tt"] == _bo_ba([])["trang_thai"], r


@can_node
def test_AC9_dong_tin_hieu_MAT_khi_mo_lenh_KHAC():
    """`BA-06` v4.10 ③ⓑ: *"mất khi mở lệnh khác"*. Mẫu số: dòng có mặt ngay
    sau cú bỏ gán."""
    r = _chay_ghep("""
      await F01G.bo_gan(F01G.ST.dong[0]);
      await _ngu(30);
      const co = _man().includes('Đã bỏ gán khỏi giao dịch');
      await F01G.mo_lenh('PWB-9');
      const khac = _man().includes('Đã bỏ gán khỏi giao dịch');
      await F01G.mo_lenh('PWB-1');
      return {co, khac, lai: _man().includes('Đã bỏ gán khỏi giao dịch')};
    """, dong=[_lenh("PWB-1", [4242]), _lenh("PWB-9", [])],
        tra={"/queue/4242/chum": CHUM1, "/queue/4242/unmatch": _than(["PWB-1"])})
    assert r["co"] is True, "⛔ không đo được: dòng tín hiệu ⛔ hiện"
    assert r["khac"] is False and r["lai"] is False, r
