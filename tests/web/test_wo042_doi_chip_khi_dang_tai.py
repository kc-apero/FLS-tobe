# -*- coding: utf-8 -*-
"""`WO-042 (a)` · `BA-06` v4.18 `§4.5 ⓥ` — đổi chip `②b` khi danh sách
**đang tải**: lượt **MỚI NHẤT** thắng.

⛔ Lỗi gốc *(`KQ-041 F-3` `NANG`, có từ `9ed4d4a` 22/09)*: mỗi cú bấm chip mở
một lượt tải, gán `ST.dong = []` **mới**, trong khi lượt cũ vẫn đang `await`
rồi `push` vào **mảng của lượt mới**. 8088 sổ thật chỉ đọc *(`KQ-041`)*: chip
`Đã gán` in **2955** = 2.219 ＋ 736; bấm lại chip đang chọn ⇒ **1.472** = 736 × 2.

⭐⭐ **Vì sao bộ cũ ⛔ thấy:** cửa giả `khung_node` trả lời **ngay** — lần thứ
tư của lớp *"khuôn thử nhanh hơn đời thật"*. Bài `kq041` dùng cửa giả chậm
**40 ms** theo đồng hồ; bài này đi xa hơn một bước: cửa giả **⛔ bao giờ tự trả
lời** — mỗi lượt gọi nằm trong hàng `_HANG` cho tới khi **kịch bản** thả nó
*(`_tra` / `_no`)*. Thứ tự về của từng lượt do bài **quyết**, ⛔ do đồng hồ máy
— luật `ⓥ`: *"⛔ một bài 'bấm nhanh rồi mong'"*.

Mỗi hàng mang mã **theo số thứ tự lượt gọi** *(`G<k>-<i>`)* ⇒ một hàng của lượt
cũ lọt vào danh sách là **thấy được tên nó**, ⛔ chỉ thấy tổng lệch.
"""
from __future__ import annotations

import pytest

from tests.web.khung_node import _chay, can_node

pytestmark = can_node

_VO = """
const man = d.document.createElement('section'); man.id = 'man-ghep';
const goc = d.document.createElement('div'); goc.id = 'ghep-goc';
const tim = d.document.createElement('input'); tim.id = 'ghep-tim';
d.body.appendChild(man); d.body.appendChild(goc); d.body.appendChild(tim);
"""
_TEP = ["thanh_phan.js", "goi_cua.js", "man_f01_ghep.js"]

#: ⭐ Cửa giả **giữ** mọi lượt gọi tới khi kịch bản thả. `_tra(mau, n, tt)`
#: thả lượt **đầu tiên còn chờ** có đường chứa `mau` với `n` hàng trạng thái
#: `tt`; `_no(mau, loi)` thả nó bằng một lỗi; `_cho()` cho mọi `await` đang
#: dở chạy tới chỗ dừng kế tiếp. `_tra` ném nếu ⛔ có lượt nào chờ khớp mẫu —
#: một kịch bản thả nhầm là **⛔ đo được** *(`Đ5`)*, ⛔ lặng lẽ xanh.
_CUA_GIU = """
globalThis._HANG = [];
FLS.doc = function (duong) {
  _GOI.push(['doc', duong]);
  const k = _GOI.filter(g => g[0] === 'doc').length;
  return new Promise((ok, no) => _HANG.push({duong, k, ok, no, xong: false}));
};
globalThis._cho = async () => {
  for (let i = 0; i < 30; i++) await Promise.resolve();
  await new Promise(r => setTimeout(r, 0));
};
globalThis._tim = (mau) => _HANG.find(h => !h.xong && h.duong.indexOf(mau) >= 0);
globalThis._tra = async (mau, n, tt) => {
  const h = _tim(mau);
  if (!h) throw new Error('⛔ không đo được: không có lượt chờ khớp ' + mau
                          + ' — ' + JSON.stringify(_HANG.map(x => [x.duong, x.xong])));
  h.xong = true;
  const rows = [];
  for (let i = 0; i < n; i++) {
    const ma = 'G' + h.k + '-' + i;
    rows.push({pm_line_id: ma, the: {ma_lenh: ma, trang_thai: tt}});
  }
  h.ok({data: {rows, next_cursor: null}, meta: {}});
  await _cho();
};
globalThis._no = async (mau, loi) => {
  const h = _tim(mau);
  if (!h) throw new Error('⛔ không đo được: không có lượt chờ khớp ' + mau);
  h.xong = true; h.no(loi); await _cho();
};
globalThis._nhin = () => {
  const goc = document.querySelector('#ghep-goc');
  const dem = goc.querySelector('.dem');
  const d = F01G.ST.dong;
  return {chip: F01G.ST.chip, n: d.length,
          khac: new Set(d.map(x => x.ma_lenh)).size,
          ma: d.map(x => x.ma_lenh),
          da_gan: d.filter(x => x.trang_thai === 'da_gan').length,
          chua_gan: d.filter(x => x.trang_thai === 'chua_gan').length,
          dang_tai: F01G.ST.dang_tai, loi: F01G.ST.loi,
          dem: dem ? dem.textContent : null,
          chu: goc.textContent,
          goi: _GOI.filter(g => g[0] === 'doc').map(g => g[1]),
          con_cho: _HANG.filter(h => !h.xong).map(h => h.duong)};
};
"""

#: đường của chip `Chưa gán` *(hai cửa)* và `Đã gán` *(một cửa)* — `CHIP_CUA`
NGUOI, MAY, DA = "ro=nguoi", "ro=may", "lenh-da-gan"


def _chay_giu(kich_ban: str) -> dict:
    return _chay(_CUA_GIU + kich_ban, tep=_TEP, vo=_VO)


# ═══ AC-1 · luật ① — đổi sang chip KHÁC khi đang tải ═══════════════════════

def test_AC1_doi_sang_DA_GAN_khi_CHUA_GAN_dang_tai_luot_cu_ve_SAU():
    """Đúng ca 8088: lượt `Chưa gán` trả **sau** lượt `Đã gán`.
    Mã hôm nay *(đỏ)*: lượt cũ `push` 5 ＋ 2 hàng `chua_gan` vào mảng của lượt
    mới ⇒ `n = 10`, chip in `10 dòng` — bản thu nhỏ của `2955 = 2219 + 736`."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _tra({DA!r}, 3, 'da_gan');           // lượt MỚI xong trước
      await _tra({NGUOI!r}, 5, 'chua_gan');       // lượt CŨ về sau
      if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      await a; await b;
      return _nhin();""")
    assert r["chip"] == "da_gan", r
    assert r["chua_gan"] == 0, f"⛔ chip 'Đã gán' mang hàng rổ cũ: {r['ma']}"
    assert r["n"] == r["khac"] == r["da_gan"] == 3, r
    assert r["dem"] == "3 dòng", f"⛔ chip in sai số: {r['dem']!r}"
    assert not r["dang_tai"] and r["loi"] is None, r


def test_AC1_doi_chip_luot_cu_ve_TRUOC_van_chi_mot_ro():
    """Thứ tự ngược: lượt cũ về **trước** khi lượt mới xong — kết quả của nó
    vẫn ⛔ vào `ST.dong`."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _tra({NGUOI!r}, 5, 'chua_gan');
      if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      await _tra({DA!r}, 3, 'da_gan');
      await a; await b;
      return _nhin();""")
    assert r["chip"] == "da_gan" and r["chua_gan"] == 0, r
    assert r["n"] == 3 and r["dem"] == "3 dòng", r


def test_AC1_luot_bi_thay_KHONG_xin_trang_ke_tiep():
    """⭐ Cách làm của Dev *(⛔ spec đòi)*: lượt đã bị thay dừng ở lần `await`
    kế tiếp — ⛔ hỏi thêm cửa thứ hai *(`ro=may`)* cho một kết quả sẽ bị bỏ.
    Tổng `GET` = 1 *(lượt cũ, đang bay khi bị thay)* ＋ 1 *(lượt mới)*."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _tra({NGUOI!r}, 5, 'chua_gan');
      await _tra({DA!r}, 3, 'da_gan');
      await a; await b;
      return _nhin();""")
    assert r["goi"] == ["/queue/lenh-cho?ro=nguoi&limit=500",
                        "/queue/lenh-da-gan?limit=500"], r["goi"]
    assert r["con_cho"] == [], r


# ═══ AC-2 · luật ② — bấm lại chip ĐANG CHỌN khi đang tải ═══════════════════

def test_AC2_bam_lai_chip_dang_chon_KHONG_mo_luot_moi():
    """Mã hôm nay *(đỏ)*: **4** `GET` *(mỗi đường hai lần)*, mỗi lệnh hiện hai
    lần — bản thu nhỏ của `1472 = 736 × 2`. Mong: **2** `GET` = số trang của
    **một** lượt *(hai cửa × một trang)*, `n` = số hàng cửa trả."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('chua_gan'); await _cho();
      while (_tim({NGUOI!r}) || _tim({MAY!r})) {{
        if (_tim({NGUOI!r})) await _tra({NGUOI!r}, 4, 'chua_gan');
        if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      }}
      await a; await b;
      return _nhin();""")
    assert len(r["goi"]) == 2, f"⛔ mở lượt thứ hai: {r['goi']}"
    assert r["n"] == r["khac"] == 6, f"⛔ mỗi lệnh hiện hai lần: {r}"
    assert r["dem"] == "6 dòng", r


def test_AC2_mo_man_khi_dang_tai_KHONG_mo_luot_moi():
    """Cùng luật ② ở cửa vào thứ hai: vỏ gọi `mo_man()` *(quay lại tab
    `②`)* trong lúc lượt đầu chưa xong — `ST.dong` vẫn rỗng nên điều kiện cũ
    `!ST.dong.length` mở thêm một lượt cùng chip."""
    r = _chay_giu(f"""
      const a = F01G.mo_man(); await _cho();
      const b = F01G.mo_man(); await _cho();
      while (_tim({NGUOI!r}) || _tim({MAY!r})) {{
        if (_tim({NGUOI!r})) await _tra({NGUOI!r}, 4, 'chua_gan');
        if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      }}
      await a; await b;
      return _nhin();""")
    assert len(r["goi"]) == 2, f"⛔ mở lượt thứ hai: {r['goi']}"
    assert r["n"] == r["khac"] == 6 and r["dem"] == "6 dòng", r


# ═══ AC-3 · luật ③ — trạng thái là của lượt MỚI NHẤT ═══════════════════════

def test_AC3_luot_cu_xong_khi_luot_moi_dang_tai_man_VAN_dang_tai():
    """Mã hôm nay *(đỏ)*: `finally` của lượt cũ đặt `ST.dang_tai = false` ⇒
    màn rời khung *"Đang hỏi sổ…"* và in số dòng của một danh sách chưa về."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _tra({NGUOI!r}, 5, 'chua_gan');
      if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      await a; F01G.ve();
      const giua = _nhin();
      await _tra({DA!r}, 3, 'da_gan'); await b;
      return {{giua, cuoi: _nhin()}};""")
    g = r["giua"]
    assert g["dang_tai"] is True, f"⛔ lượt cũ tắt cờ tải: {g}"
    assert "Đang hỏi sổ…" in g["chu"] and g["dem"] is None, g
    assert r["cuoi"]["n"] == 3 and r["cuoi"]["dem"] == "3 dòng", r["cuoi"]


def test_AC3_luot_cu_LOI_KHONG_hien_duoi_chip_moi():
    """Mã hôm nay *(đỏ)*: `catch` của lượt cũ đặt `ST.loi` ⇒ chip `Đã gán`
    đã tải xong lại hiện *"Cửa lỗi"* của chip trước."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _tra({DA!r}, 3, 'da_gan');
      await _no({NGUOI!r}, new FLS.LoiCua('FLS-INTERNAL', 500, 'lượt cũ'));
      await a; await b; F01G.ve();
      return _nhin();""")
    assert r["loi"] is None, f"⛔ lỗi lượt cũ hiện dưới chip mới: {r['loi']!r}"
    assert "Cửa lỗi" not in r["chu"], r["chu"][:200]
    assert r["n"] == 3 and r["dem"] == "3 dòng", r


def test_AC3_luot_MOI_loi_thi_hien_loi_va_luot_cu_KHONG_de_len():
    """Lượt **mới** lỗi ⇒ câu lỗi như cũ *(`banner crit`)*; lượt cũ về sau với
    dữ liệu ⇒ ⛔ đổ hàng vào `ST.dong` *(mã hôm nay: đổ 5 ＋ 2 — đỏ)*."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _no({DA!r}, new FLS.LoiCua('FLS-INTERNAL', 500, 'lượt mới'));
      await _tra({NGUOI!r}, 5, 'chua_gan');
      if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      await a; await b; F01G.ve();
      return _nhin();""")
    assert r["loi"] == "Máy gặp lỗi bên trong.", r
    assert "Cửa lỗi: Máy gặp lỗi bên trong." in r["chu"], r["chu"][:200]
    assert r["n"] == 0 and not r["dang_tai"], f"⛔ lượt cũ đổ hàng: {r}"


def test_AC3_luot_MOI_mat_ket_noi_va_luot_cu_loi_khac_KHONG_de_cau():
    """Lượt **mới** mất kết nối *(`FLS-MAT-KET-NOI`)*; lượt cũ lỗi **khác**
    về sau ⇒ màn giữ câu của lượt mới *(mã hôm nay: câu lượt cũ đè — đỏ)*."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _no({DA!r}, new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'Failed to fetch'));
      await _no({NGUOI!r}, new FLS.LoiCua('FLS-INTERNAL', 500, 'lượt cũ'));
      await a; await b; F01G.ve();
      return _nhin();""")
    assert r["loi"] == "Không nối được tới máy chủ FLS.", r
    assert "Máy gặp lỗi bên trong." not in r["chu"], r["chu"][:200]


def test_AC3_sau_loi_bam_lai_chip_THI_tai_lai():
    """Luật ② chỉ chặn khi **đang tải**. Hết tải *(kể cả lỗi)* bấm lại chip
    đang chọn = tải lại — đó là đường **thử lại** duy nhất của danh sách hôm
    nay *(`F01G` ⛔ có nút `Thử lại` riêng — xem `HOI-043`)*."""
    r = _chay_giu(f"""
      await (async () => {{ const a = F01G.doi_chip('da_gan'); await _cho();
        await _no({DA!r}, new FLS.LoiCua('FLS-MAT-KET-NOI', 0, 'x')); await a; }})();
      const b = F01G.doi_chip('da_gan'); await _cho();
      await _tra({DA!r}, 3, 'da_gan'); await b;
      return _nhin();""")
    assert len(r["goi"]) == 2 and r["loi"] is None, r
    assert r["n"] == 3 and r["dem"] == "3 dòng", r


# ═══ AC-4 · luật ④ — đổi chip nhiều lần liên tiếp ══════════════════════════

def test_AC4_doi_nhanh_CHUA_DA_CHUA_cuoi_cung_dung_chip_cuoi():
    """`Chưa gán → Đã gán → Chưa gán` khi lượt đầu chưa xong; thả **mọi** lượt
    theo thứ tự đến *(FIFO)* cho tới khi hết. Mong: chip `chua_gan`, chỉ hàng
    của lượt **thứ ba** *(mã `G<k>` với `k` là lượt gọi của nó)*, **0** `da_gan`."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip('da_gan'); await _cho();
      const c = F01G.doi_chip('chua_gan'); await _cho();
      for (let vong = 0; vong < 10 && _HANG.some(h => !h.xong); vong++) {{
        const h = _HANG.find(h => !h.xong);
        const da = h.duong.indexOf({DA!r}) >= 0;
        await _tra(h.duong, da ? 3 : 4, da ? 'da_gan' : 'chua_gan');
      }}
      await a; await b; await c;
      const r = _nhin();
      r.k_luot3 = _HANG.filter(h => h.k >= 3).map(h => 'G' + h.k);
      return r;""")
    assert r["chip"] == "chua_gan", r
    assert r["da_gan"] == 0, f"⛔ hàng chip trước còn trên màn: {r['ma']}"
    assert r["n"] == r["khac"] == 8, r
    assert {m.split("-")[0] for m in r["ma"]} <= set(r["k_luot3"]), r
    assert r["dem"] == "8 dòng", r


@pytest.mark.parametrize("cuoi", ["tat_ca"])
def test_AC4_doi_sang_chip_CHUA_CO_CUA_khi_dang_tai_bo_luot_cu(cuoi):
    """Chip ⛔ có cửa *(`Tất cả` — `GAP-SCR-26`)* cũng là một lượt **mới**:
    lượt cũ về sau ⛔ được đổ hàng, ⛔ tắt khung *"chưa có cửa"*."""
    r = _chay_giu(f"""
      const a = F01G.doi_chip('chua_gan'); await _cho();
      const b = F01G.doi_chip({cuoi!r}); await _cho();
      await _tra({NGUOI!r}, 5, 'chua_gan');
      if (_tim({MAY!r})) await _tra({MAY!r}, 2, 'chua_gan');
      await a; await b; F01G.ve();
      return Object.assign(_nhin(), {{thieu: F01G.ST.thieu_cua}});""")
    assert r["thieu"] is True and r["n"] == 0 and not r["dang_tai"], r
    assert "Chưa có cửa cho bộ lọc này" in r["chu"], r["chu"][:200]
