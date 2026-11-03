# -*- coding: utf-8 -*-
"""`KQ-021` — kiểm `BG-020` *(`WO-008` **vòng 2**: năm ca của nút `Bỏ gán`
trên màn ghép, `BA-06` **v4.10** mục ⓔ)*.

⭐ Ba loại bài trong tệp này:

ⓐ **XANH — lấp lỗ phủ của bộ bài hiện có.** `fls-test` chạy **11** đột biến
   của riêng mình *(khác `M1`…`M17` của Dev)* trên worktree tạm; **6** sống
   sót qua **34** bài *(Dev vòng 1 + vòng 2 + `kq019 --runxfail`)*:
     `T1` Thôi xong cờ khoá ⛔ trả ⇒ nút `Bỏ gán` khoá **vĩnh viễn**
     `T2` cửa lỗi xong cờ khoá ⛔ trả ⇒ ⛔ thử lại được
     `T4` `gd` ⛔ cập nhật ⇒ bảng view ① vẫn in giao dịch vừa gỡ như **đã gán**
     `T6` lệnh còn dòng tiền khác vẫn bị đổi sang `Chưa gán`
     `T17` kéo người về lệnh vừa bỏ gán *(⛔ có bài ở đây — spec ⛔ nói)*
     `T18` dòng lỗi cũ ⛔ xoá khi bấm lại thành công
   Mã hôm nay **đúng** ở cả sáu — đây là bài canh để nó **còn** đúng.

ⓑ **XANH — sổ THẬT qua hàm THẬT.** Mọi lệnh đã gán của sổ thật *(hàm đọc
   `doc_lenh_da_gan` + `khuon_the_lenh`, chùm qua `chum_cua_dong_tien` —
   **chính** các hàm cửa gọi)* đi qua `bo_gan` thật + `hop_thoai.js` thật:
   ca ① ⇒ hộp báo đúng `N`, ca ② ⇒ hộp hỏi đúng `N` + đủ tên. Đo **quan hệ**,
   ⛔ hằng số *(sổ trôi thì bài vẫn đúng)*; mẫu số mỗi ca ≠ 0 *(`Đ3`)*.

ⓒ **`xfail(strict=True)` — phát hiện mới của `KQ-021`**, ĐỎ trên mã hôm nay
   *(`929fbd2`)*, đo thật bằng Chrome trên máy `8099` *(kho TEST, phím thật
   `Input.dispatchKeyEvent`)*:
     `F-1` `Esc` trên hộp hỏi đóng hộp **và** đóng luôn lệnh *(`BA-06` §4.5:
           *"`Esc` phải bóc từng lớp một"*)*; `j`/`k` khi hộp đang mở **đổi
           lệnh sau lưng hộp*.
     `F-2` `Esc` trong lúc `Gỡ cả N` đang chờ cửa ⇒ hộp đóng ⇒ cửa lỗi ⇒ câu
           lỗi viết vào **hộp đã đóng** — màn ⛔ một chữ.
"""
from __future__ import annotations

import json

import pytest

from fls.db.kho import dsn_that, noi_chi_doc
from fls.repo import lenh_cho as lc
from fls.repo import man_ghep as mg
from fls.repo.doc_bao_cao import TRANG_TOI_DA
from fls.repo.pham_vi import chi_nap_that
from tests.nghiem_thu.test_kq019_bo_gan_man_ghep_va_nhat_ky import TEP, VO
from tests.web.khung_node import _chay, can_node

#: ⭐ Bọc `HT.mo` THẬT để đếm — gọi **xuyên**, ⛔ thay. Nút trong hộp bấm bằng
#: **chính** `onclick` mà `hop_thoai.js` gắn; nút trên màn bằng trình nghe
#: `click` thật của phần tử.
CONG_CU = """
  globalThis._HOP = [];
  const _mo0 = HT.mo;
  HT.mo = function (t, b, n) { _HOP.push(t); return _mo0(t, b, n); };
  globalThis._ngu = ms => new Promise(r => setTimeout(r, ms));
  globalThis._man = () => document.getElementById('ghep-goc').textContent;
  globalThis._dem = re => _GOI.filter(g => re.test(g[1])).length;
  globalThis._hop = function () {
    const s = document.getElementById('scrim');
    return {mo: s.classList.contains('on'),
            t: document.getElementById('dlg-t').textContent,
            b: document.getElementById('dlg-b').textContent,
            nut: document.getElementById('dlg-f').children.map(x => x.textContent)};
  };
  globalThis._nut = function (chu) {
    const ra = [];
    (function di(e) {
      if (e.tagName === 'BUTTON' && e.textContent.trim() === chu) ra.push(e);
      e.children.forEach(di);
    })(document.getElementById('ghep-goc'));
    return ra;
  };
  globalThis._bam = function (chu) {
    const b = _nut(chu);
    if (b.length !== 1) throw new Error('⛔ không đo được: ' + b.length + ' nút ' + chu);
    if (b[0].disabled) return 'KHOA';
    (b[0]._nghe.click || []).forEach(f => f());
    return 'bam';
  };
  globalThis._bam_hop = chu => document.getElementById('dlg-f').children
    .filter(b => b.textContent === chu)[0].onclick();
"""


def _lenh(ma: str, itl: list[int], dien_giai: str = "") -> dict:
    """Lệnh đã gán — bộ ba lấy từ **hàm thật** `khuon_the_lenh`."""
    k = mg.khuon_the_lenh({"pm_line_id": ma, "itl_da_gan": itl})
    gd = [{"itl_id": i, "bac": "tien", "doc_no": "FT-%d" % i,
           "amount": "5000000.00", "curr": "VND", "doc_date": "2026-09-01",
           "dien_giai": dien_giai or "GD-%d" % i, "da_gan": True} for i in itl]
    return {"ma_lenh": ma, "noi_dung": "chi " + ma, "so_tien": "5000000.00",
            "curr": "VND", "loai_phieu": "PM", "itl_da_gan": list(itl),
            "nhom_du_truong": [], "gd_ds": gd, "gd": gd[0] if gd else None,
            "trang_thai": k["trang_thai"], "trang_thai_nhan": k["trang_thai_nhan"],
            "trang_thai_mau": k["trang_thai_mau"]}


def _than(da_bo: list[str]) -> dict:
    return {"itl_id": 4242, "evt_id": 9, "ve_hang_cho": True,
            "da_bo": [{"pm_line_id": m, "amount": "1.00", "hinh": "T", "lan": 1,
                       "link_id": 1} for m in da_bo],
            "but_toan_dao": [], "bo_qua": []}


CHUM1 = {"itl_id": 4242, "can_hoi": False, "so_dong": 1, "dong_lenh": []}
CHUM2 = {"itl_id": 4242, "can_hoi": True, "so_dong": 2, "dong_lenh": [
    {"pm_line_id": "PWB-1", "amount": "3000000.00", "curr": "VND"},
    {"pm_line_id": "PWB-2", "amount": "2000000.00", "curr": "VND"}]}


def _ghep(kich_ban: str, *, dong: list[dict], tra: dict, mo: str | None = None) -> dict:
    t = ["_TRA[%s] = %s;" % (json.dumps(k), json.dumps(
        v if isinstance(v, dict) and "no" in v else {"data": v}, ensure_ascii=False))
         for k, v in tra.items()]
    for d in dong:
        k = "/queue/lenh/%s/itl-candidates" % d["ma_lenh"]
        if k not in tra:
            t.append("_TRA[%s] = {data: {ung_vien: [{itl_id: 7, bac: 'tien', "
                     "amount: '1.00', curr: 'VND'}]}};" % json.dumps(k))
    return _chay(CONG_CU + "\n".join(t) + """
      F01G.ST.dong = %s;
      await F01G.mo_lenh(%s);
    """ % (json.dumps(dong, ensure_ascii=False), json.dumps(mo or dong[0]["ma_lenh"]))
        + kich_ban, tep=TEP, vo=VO)


# ═══ ⓐ XANH — lỗ phủ ═══════════════════════════════════════════════════════
@can_node
def test_T1_THOI_tren_hop_hoi__nut_Bo_gan_MO_lai__bam_lai_HOI_lai():
    """Trạng thái **tải** chỉ sống **trong lúc chờ** *(`BA-06` v4.10 bảng 5
    trạng thái)*. Bấm `Thôi` xong mà nút còn khoá là người **⛔ bỏ gán được
    nữa** cho tới khi tải lại trang.

    Chứng minh ĐỎ *(`KQ-021` `T1`, worktree)*: bỏ dòng trả cờ trước `HT.mo`
    ⇒ nút `KHOA`, `/chum` **1** ⇒ ĐỎ."""
    r = _ghep("""
      const a = _bam('Bỏ gán'); await _ngu(30);
      const h1 = _hop();
      await _bam_hop('Thôi'); await _ngu(30);
      const h2 = _hop();
      const b = _bam('Bỏ gán'); await _ngu(30);
      return {a, b, h1, h2, h3: _hop(), chum: _dem(/\\/chum$/), unmatch: _dem(/\\/unmatch$/),
              khoa: F01G.ST.dang_bo_gan};
    """, dong=[_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242])],
        tra={"/queue/4242/chum": CHUM2})
    assert r["a"] == "bam" and r["h1"]["mo"], f"⛔ không đo được: hộp hỏi ⛔ mở {r}"
    assert r["h2"]["mo"] is False, "⛔ Thôi ⛔ đóng hộp"
    assert r["b"] == "bam", f"⛔ sau Thôi nút Bỏ gán còn KHOÁ: {r}"
    assert r["khoa"] is False, r
    assert r["chum"] == 2 and r["h3"]["mo"], f"⛔ bấm lại ⛔ hỏi lại: {r}"
    assert r["unmatch"] == 0, r


@can_node
def test_T2_cua_LOI__nut_MO_lai__bam_lai_GOI_cua_lan_HAI():
    """Ca ⑤ nói *"Bỏ gán **chưa** xảy ra"* — tức người được **thử lại**.
    Nút khoá sau lỗi là câu ấy thành lời hứa suông.

    Chứng minh ĐỎ *(`T2`)*: bỏ `ST.dang_bo_gan = false` trong `_loi_bo_gan`
    ⇒ cú thứ hai `KHOA`, `/unmatch` **1** ⇒ ĐỎ."""
    r = _ghep("""
      _TRA['/queue/4242/unmatch'] = {no: new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'Failed to fetch')};
      await F01G.bo_gan(F01G.ST.dong[0]); await _ngu(30);
      const man1 = _man();
      const b = _bam('Bỏ gán'); await _ngu(30);
      return {man1, b, unmatch: _dem(/\\/unmatch$/), khoa: F01G.ST.dang_bo_gan};
    """, dong=[_lenh("PWB-1", [4242])], tra={"/queue/4242/chum": CHUM1})
    assert "Bỏ gán chưa xảy ra" in r["man1"], "⛔ không đo được: ca ⑤ ⛔ hiện"
    assert r["b"] == "bam", f"⛔ sau lỗi cửa nút Bỏ gán còn KHOÁ: {r}"
    assert r["unmatch"] == 2, f"⛔ thử lại ⛔ gọi cửa: {r}"
    assert r["khoa"] is False, r


@can_node
def test_T18_loi_roi_THANH_CONG__dong_loi_cu_BIEN_MAT():
    """Lỗi rồi thử lại **thành công** ⇒ màn ⛔ được nói cùng lúc *"chưa xảy
    ra"* và *"Đã bỏ gán"*. Đo thật Chrome `8099` *(lệnh `#48`, cắt mạng rồi
    thả)*: dòng lỗi biến mất — bài canh để nó **còn** biến mất.

    Chứng minh ĐỎ *(`T18`)*: bỏ `ST.loi_bo_gan = null` đầu `bo_gan` ⇒ ĐỎ."""
    r = _ghep("""
      _TRA['/queue/4242/unmatch'] = {no: new FLS.LoiCua('FLS-INTERNAL', 0, 'x')};
      await F01G.bo_gan(F01G.ST.dong[0]); await _ngu(30);
      const man1 = _man();
      _TRA['/queue/4242/unmatch'] = {data: %s};
      await F01G.bo_gan(F01G.ST.dong[0]); await _ngu(60);
      return {man1, man2: _man(), unmatch: _dem(/\\/unmatch$/)};
    """ % json.dumps(_than(["PWB-1"])), dong=[_lenh("PWB-1", [4242])],
        tra={"/queue/4242/chum": CHUM1})
    assert "Bỏ gán chưa xảy ra" in r["man1"], "⛔ không đo được: lần 1 ⛔ lỗi"
    assert r["unmatch"] == 2, r
    assert "Đã bỏ gán khỏi giao dịch #4242" in r["man2"], r["man2"]
    assert "Bỏ gán chưa xảy ra" not in r["man2"], \
        "⛔ sổ đã ghi mà màn vẫn nói 'Bỏ gán chưa xảy ra'"


@can_node
def test_T6_chum__lenh_con_DONG_TIEN_KHAC__van_Da_gan_chi_con_dong_ay():
    """`BA-06` v4.10 ③ⓐ: bỏ `itl_id` vừa gỡ khỏi `itl_da_gan`/`gd_ds`;
    **`itl_da_gan` hết** ⇒ mới đổi bộ ba. Lệnh `PWB-2` nằm trong chùm `#4242`
    **và** còn gắn `#5000` *(sổ thật có hình này: lệnh ≥ 2 dòng tiền **23**)*
    ⇒ sau `Gỡ cả 2` phải **vẫn** `Đã gán` *(bộ ba = `khuon_the_lenh([5000])`)*,
    và chỉ còn `#5000`. Đo thật Chrome `8099` ca **N**: đúng như vậy.

    Chứng minh ĐỎ *(`T6`)*: đổi bộ ba vô điều kiện ⇒ `PWB-2` thành `Chưa gán`
    ⇒ ĐỎ."""
    r = _ghep("""
      _bam('Bỏ gán'); await _ngu(30);
      await _bam_hop('Gỡ cả 2'); await _ngu(80);
      const d = F01G.ST.dong;
      return {unmatch: _dem(/\\/unmatch$/),
              a: [d[0].trang_thai, d[0].itl_da_gan],
              b: {tt: [d[1].trang_thai, d[1].trang_thai_nhan, d[1].trang_thai_mau],
                  da: d[1].itl_da_gan, ds: (d[1].gd_ds || []).map(g => g.itl_id),
                  gd: d[1].gd && d[1].gd.itl_id}};
    """, dong=[_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242, 5000])],
        tra={"/queue/4242/chum": CHUM2,
             "/queue/4242/unmatch": _than(["PWB-1", "PWB-2"])})
    assert r["unmatch"] == 1, f"⛔ không đo được: ⛔ ghi {r}"
    con = mg.khuon_the_lenh({"pm_line_id": "PWB-2", "itl_da_gan": [5000]})
    het = mg.khuon_the_lenh({"pm_line_id": "PWB-1", "itl_da_gan": []})
    assert r["a"] == [het["trang_thai"], []], r
    assert r["b"]["tt"] == [con["trang_thai"], con["trang_thai_nhan"],
                            con["trang_thai_mau"]], r["b"]
    assert r["b"]["da"] == [5000] and r["b"]["ds"] == [5000] and r["b"]["gd"] == 5000, r["b"]


@can_node
def test_T4_sau_bo_gan__VIEW1_khong_in_giao_dich_vua_go_nhu_DA_GAN():
    """Cột *"Giao dịch đã gán"* của bảng view ① đọc `d.gd`. Sau bỏ gán `200`
    lệnh đã `Chưa gán` mà cột vẫn in giao dịch vừa gỡ *(⛔ tiền tố "đề xuất:")*
    là **hai ô cùng hàng nói hai điều ngược nhau** *(`INV-I16`; cửa
    `_gan_gd`: *"đã chốt"* ≠ *"máy đề xuất"* ⛔ được trông giống nhau)*.
    Đo thật `8099` ca **L**: cột in *"— chưa chọn"*.

    Mẫu số: **trước** cú bấm, view ① in giao dịch ấy *(`Đ3`)*.
    Chứng minh ĐỎ *(`T4`)*: bỏ dòng cập nhật `d.gd` ⇒ ĐỎ."""
    r = _ghep("""
      F01G.ST.mo = null; F01G.ve();
      const truoc = _man();
      await F01G.mo_lenh('PWB-1');
      _bam('Bỏ gán'); await _ngu(60);
      F01G.ST.mo = null; F01G.ve();
      return {truoc, sau: _man(), tt: F01G.ST.dong[0].trang_thai, unmatch: _dem(/\\/unmatch$/)};
    """, dong=[_lenh("PWB-1", [4242], dien_giai="GD-VUA-GO-K21")],
        tra={"/queue/4242/chum": CHUM1, "/queue/4242/unmatch": _than(["PWB-1"])})
    assert "GD-VUA-GO-K21" in r["truoc"], "⛔ không đo được: view ① ⛔ in giao dịch"
    assert r["unmatch"] == 1 and r["tt"] == "chua_gan", r
    assert "GD-VUA-GO-K21" not in r["sau"], \
        "⛔ lệnh đã Chưa gán mà view ① vẫn in giao dịch vừa gỡ"


# ═══ ⓑ XANH — sổ THẬT qua hàm THẬT ════════════════════════════════════════
def _lenh_so_that() -> tuple[list[dict], dict[int, list[dict]]]:
    """Mọi lệnh đã gán của sổ thật qua **hàm đọc thật** `doc_lenh_da_gan` +
    khuôn thẻ thật; chùm qua **hàm thật** `chum_cua_dong_tien`.

    ⭐ Chỉ hỏi chùm cho dòng tiền mà **>1** lệnh đang gắn *(đếm từ chính
    `itl_da_gan` của hàm đọc)* — hàm chùm tốn ~0,18 s/lượt, hỏi cả **2.196**
    dòng là ~6,5 phút. ⇒ Đối chiếu chéo: số lệnh hàm chùm trả **=** số đếm ấy.
    ⛔ Kho tắt ⇒ bài ĐỎ *(`Đ5`)*."""
    with noi_chi_doc(dsn_that()) as c:
        pv = chi_nap_that()
        dong: list[dict] = []
        ct = None
        while True:
            t = lc.doc_lenh_da_gan(c, pv, con_tro=ct, limit=TRANG_TOI_DA)
            dong.extend(t.dong)
            ct = t.con_tro
            if not ct:
                break
        dem: dict[int, int] = {}
        for d in dong:
            for i in d.get("itl_da_gan") or []:
                dem[i] = dem.get(i, 0) + 1
        chum: dict[int, list[dict]] = {}
        for i, n in dem.items():
            if n > 1:
                ds = mg.chum_cua_dong_tien(c, pv, i)
                assert len(ds) == n, f"⛔ itl {i}: hàm chùm {len(ds)} ≠ {n} lệnh gắn"
                chum[i] = [{"pm_line_id": x["pm_line_id"],
                            "amount": str(x.get("amount")), "curr": x.get("curr")}
                           for x in ds]
    the = []
    for d in dong:
        k = mg.khuon_the_lenh(d)
        the.append({"ma_lenh": k["ma_lenh"], "trang_thai": k["trang_thai"],
                    "trang_thai_nhan": k["trang_thai_nhan"],
                    "trang_thai_mau": k["trang_thai_mau"],
                    "so_tien": str(k["so_tien"]), "curr": k["curr"],
                    "itl_da_gan": sorted(d.get("itl_da_gan") or [])})
    return the, chum


@can_node
def test_SO_THAT__moi_lenh_ca_1_ca_2__bo_gan_THAT_mo_DUNG_hop():
    """`BA-06` v4.10 ① / ② trên **toàn bộ** lệnh đã gán của sổ thật.

    Đo `KQ-021` *(02/10, Chrome trên 8088 chỉ đọc, chuột + `Esc` thật)*:
    **88 / 88** đúng hộp *(ca ① 23 · ca ② 65)*, `/chum` đúng **65**, `POST` **0**.
    Bài này đo cùng quan hệ bằng hàm thật, ⛔ chép 88/23/65.

    Chứng minh ĐỎ: mã `124a067` *(gọi `HT.hoi`)* ⇒ `TypeError` ⇒ ĐỎ; đổi
    tiêu đề ca ① ⇒ ĐỎ *(`KQ-021`, worktree)*."""
    the, chum = _lenh_so_that()
    ca = []
    for k in the:
        n = len(k["itl_da_gan"])
        if n >= 2:
            ca.append({"k": k, "t": "Lệnh này đang gắn %d giao dịch" % n,
                       "nut": ["Đã hiểu"], "c": None})
        elif n == 1 and k["itl_da_gan"][0] in chum:
            m = len(chum[k["itl_da_gan"][0]])
            ca.append({"k": k, "t": "Bỏ gán sẽ gỡ CẢ %d lệnh chi" % m,
                       "nut": ["Thôi", "Gỡ cả %d" % m], "c": k["itl_da_gan"][0]})
    so1 = sum(1 for x in ca if x["c"] is None)
    so2 = len(ca) - so1
    assert so1 > 0 and so2 > 0, f"⛔ không đo được: ca ① {so1} · ca ② {so2} (Đ3)"
    sai: list = []
    chum_goi = unmatch = 0
    for i in range(0, len(ca), 25):          # ⚠ dòng lệnh Windows ≤ 32K ký tự
        lo = ca[i:i + 25]
        cm = {x["c"]: {"itl_id": x["c"], "dong_lenh": chum[x["c"]],
                       "so_dong": len(chum[x["c"]]), "can_hoi": True}
              for x in lo if x["c"] is not None}
        r = _chay(CONG_CU + """
          const CA = %s, CM = %s;
          for (const k in CM) _TRA['/queue/' + k + '/chum'] = {data: CM[k]};
          const sai = []; let chum_goi = 0;
          for (const x of CA) {
            F01G.ST.dong = [x.k];
            const c0 = _dem(/chum$/);
            _HOP.length = 0;
            try { await F01G.bo_gan(x.k); }
            catch (e) { sai.push([x.k.ma_lenh, 'NEM ' + String(e && e.message || e)]); continue; }
            await _ngu(0);
            const h = _hop(), dc = _dem(/chum$/) - c0;
            chum_goi += dc;
            const ten = x.c ? CM[x.c].dong_lenh.map(d => d.pm_line_id) : [];
            const thieu = ten.filter(t => !h.b.includes(t));
            if (!h.mo || h.t !== x.t || JSON.stringify(h.nut) !== JSON.stringify(x.nut)
                || _HOP.length !== 1 || thieu.length || dc !== (x.c ? 1 : 0))
              sai.push([x.k.ma_lenh, h.t, h.nut, _HOP.length, thieu, dc]);
            HT.dong();
          }
          return {sai, chum_goi, unmatch: _dem(/unmatch$/)};
        """ % (json.dumps(lo, ensure_ascii=False), json.dumps(cm, ensure_ascii=False)),
                 tep=TEP, vo=VO)
        sai += r["sai"]
        chum_goi += r["chum_goi"]
        unmatch += r["unmatch"]
    assert sai == [], f"⛔ {len(sai)}/{len(ca)} lệnh sai hộp: {sai[:5]}"
    assert chum_goi == so2, (chum_goi, so2)
    assert unmatch == 0, "⛔ ca ①/② ghi sổ trước khi người bấm"


# ═══ ⓒ PHÁT HIỆN — ĐỎ hôm nay, `xfail(strict)` ════════════════════════════
#: Trình nghe `Esc` của `hop_thoai.js` chỉ gắn khi `HT._khung` **tự dựng**
#: `#scrim`; vỏ thử dựng sẵn `#scrim` *(DOM giả ⛔ phân tích `innerHTML`)* ⇒
#: gắn lại **đúng** trình nghe ấy, **sau** `_noi_ban_phim` — cùng thứ tự với
#: trình duyệt *(màn mở trước, hộp đầu tiên dựng `#scrim` sau)*.
#:
#: ⭐⭐ *(`KQ-061`, 05/10 — `WO-023` Rủi ro 1, `BG-054` mục "đã đổi trình nghe
#: thế nào")*: mã @ `f52dafe` cho `HT` **tự** gắn trình nghe `keydown`
#: *(capture)* + `click` nền ở lần `HT.mo` **đầu tiên**, kể cả khi `#scrim`
#: có sẵn ⇒ **bản chép bỏ đi**. Giữ bản chép là để một trình nghe **của
#: bài** làm việc thay mã thật: `HT` quên gắn trình nghe thì bài vẫn xanh.
#: Bỏ bản chép ⇒ bài chỉ xanh khi **chính `hop_thoai.js`** nghe `Esc`.
#: ~~`document.addEventListener('keydown', e => { if (e.key === 'Escape' &&
#: #scrim.on) HT.dong(); })`~~ *(bản chép cũ — bia)*.
NGHE_ESC_HOP = """
  await F01G.mo_man();
"""
#: ⚠ *(`KQ-061`)* Riêng bài `F-2` **giữ** bản chép, đổi vai: nó đóng vai
#: **một nơi gọi `HT.dong()` công khai** *(trình nghe `Esc` của trình duyệt
#: thật trên mã cũ — ở đó `#scrim` do `_khung` tự dựng nên trình nghe CÓ)*.
#: Đo 05/10: bỏ bản chép thì `F-2` **XANH cả trên `7e67a09`** *(DOM giả ⛔ có
#: trình nghe `Esc` nào ⇒ hộp tự nhiên ở nguyên)* — bài mất chiều đỏ. Giữ
#: bản chép ⇒ trên mã mới bài đòi `dong()` **từ chối** khi lượt ghi còn bay
#: *(`ⓕ2`)*, trên mã cũ `dong()` đóng ⇒ đỏ.
NGHE_ESC_HOP_CHEP = """
  await F01G.mo_man();
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && document.getElementById('scrim').classList.contains('on')) HT.dong();
  });
"""


@can_node
# ✅ *(`KQ-061`, 05/10)* dấu `xfail(strict)` GỠ — XPASS đúng lý do: xanh @ `d1cea7c`, đỏ @ `7e67a09` (`Esc ⛔ đóng hộp — HT chưa nghe Esc khi #scrim có sẵn`). Lý do cũ: KQ-021 F-1: Esc trên hộp hỏi đóng hộp VÀ  đóng luôn lệnh (phim() ⛔ nhường hộp đang mở) — BA-06 §4.5  'Esc phải bóc từng lớp một'
def test_F1_ESC_tren_hop_hoi__chi_DONG_HOP__lenh_VAN_MO():
    """Đo thật Chrome `8099` ca **I** + **F2** *(`Input.dispatchKeyEvent`)*:
    hộp đóng **và** `ST.mo` → `null` *(về bảng)*. Ca ② `/unmatch` vẫn **0** —
    phần ấy đúng."""
    r = _ghep(NGHE_ESC_HOP + """
      _bam('Bỏ gán'); await _ngu(30);
      const h1 = _hop();
      _ban('keydown', {key: 'Escape'}); await _ngu(30);
      return {h1, h2: _hop(), mo: F01G.ST.mo, unmatch: _dem(/\\/unmatch$/)};
    """, dong=[_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242])],
        tra={"/queue/4242/chum": CHUM2})
    assert r["h1"]["mo"], "⛔ không đo được: hộp hỏi ⛔ mở"
    assert r["unmatch"] == 0
    assert r["h2"]["mo"] is False, "⛔ Esc ⛔ đóng hộp"
    assert r["mo"] == "PWB-1", f"⛔ Esc bóc HAI lớp: hộp + lệnh (ST.mo = {r['mo']!r})"


@can_node
# ✅ *(`KQ-061`, 05/10)* dấu `xfail(strict)` GỠ — XPASS đúng lý do: xanh @ `d1cea7c`, đỏ @ `7e67a09` (`j đổi lệnh sau lưng hộp: ST.mo = 'PWB-2'`). Lý do cũ: KQ-021 F-1: j/k khi hộp hỏi đang mở đổi  lệnh SAU LƯNG hộp
def test_F1_phim_J_khi_hop_MO__KHONG_doi_lenh_sau_lung_hop():
    """Đo thật `8099` ca **I**: hộp *"Bỏ gán sẽ gỡ CẢ 2 lệnh chi"* (#24) còn
    mở, gõ `j` ⇒ `ST.mo` `PTE5FA3-1` → `PT1262C-1` — màn sau lưng là lệnh
    khác, nút `Gỡ cả 2` vẫn gỡ chùm #24."""
    r = _ghep(NGHE_ESC_HOP + """
      _bam('Bỏ gán'); await _ngu(30);
      const h1 = _hop();
      _ban('keydown', {key: 'j'}); await _ngu(30);
      return {h1, mo: F01G.ST.mo};
    """, dong=[_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242]), _lenh("PWB-3", [5000])],
        tra={"/queue/4242/chum": CHUM2})
    assert r["h1"]["mo"], "⛔ không đo được: hộp hỏi ⛔ mở"
    assert r["mo"] == "PWB-1", f"⛔ j đổi lệnh sau lưng hộp: ST.mo = {r['mo']!r}"


@can_node
# ✅ *(`KQ-061`, 05/10)* dấu `xfail(strict)` GỠ — XPASS đúng lý do: xanh @ `d1cea7c`, đỏ @ `7e67a09` (`cửa lỗi mà người ⛔ thấy chữ nào (hộp đã đóng, màn im)`). Lý do cũ: KQ-021 F-2: Esc khi 'Gỡ cả N' đang chờ cửa  ⇒ cửa lỗi ghi vào hộp ĐÃ ĐÓNG — màn ⛔ một chữ
def test_F2_ESC_khi_GO_CA_N_dang_cho__cua_LOI__nguoi_VAN_THAY_loi():
    """`BA-06` v4.10 ②: lỗi cửa trong hộp ⇒ *"hộp ở nguyên, lỗi hiện trong
    hộp"*; ⑤: lỗi ⛔ được chỉ ra console. Đo thật Chrome `8099` ca **G**
    *(`/unmatch` treo bằng `Fetch`, `Esc` thật, rồi `failRequest`)*: hộp đóng
    lúc `Esc`, câu *"Không nối được tới máy chủ FLS."* nằm trong `#dlg-b` của
    hộp **đã đóng**, `#ghep-goc` ⛔ có *"Bỏ gán chưa xảy ra"*, 0 `Uncaught`.
    Gốc: `hop_thoai.js` cho `Esc`/bấm ra ngoài đóng hộp **cả khi** hàng nút
    đang khoá chờ cửa *(luật ⓒ chỉ tính tới lúc chưa bấm)*."""
    r = _ghep(NGHE_ESC_HOP_CHEP + """
      let tha;
      const ghi0 = FLS.ghi;
      FLS.ghi = function (duong, than) {
        if (/unmatch$/.test(duong)) {
          _GOI.push(['ghi', duong, than]);
          return new Promise((ok, no) => { tha = () => no(new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'Failed to fetch')); });
        }
        return ghi0(duong, than);
      };
      _bam('Bỏ gán'); await _ngu(30);
      const p = _bam_hop('Gỡ cả 2'); await _ngu(20);
      _ban('keydown', {key: 'Escape'}); await _ngu(20);
      tha(); await p; await _ngu(60);
      const h = _hop();
      return {unmatch: _dem(/\\/unmatch$/), hop_mo: h.mo, hop_b: h.b, man: _man()};
    """, dong=[_lenh("PWB-1", [4242]), _lenh("PWB-2", [4242])],
        tra={"/queue/4242/chum": CHUM2})
    assert r["unmatch"] == 1, "⛔ không đo được: ⛔ gọi cửa"
    cau = "Không nối được tới máy chủ FLS."
    thay = (r["hop_mo"] and cau in r["hop_b"]) or (cau in r["man"])
    assert thay, "⛔ cửa lỗi mà người ⛔ thấy chữ nào (hộp đã đóng, màn im)"
