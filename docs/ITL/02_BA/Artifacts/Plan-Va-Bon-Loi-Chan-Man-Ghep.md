# Plan vá BỐN lỗi CHẶN của màn Gán lệnh chi — `SCR-F01`

> **Cho người thực thi:** dùng `superpowers:subagent-driven-development` *(khuyến nghị)* hoặc `superpowers:executing-plans`. Các bước dùng ô đánh dấu `- [ ]`.

**Version:** v0.2 · **Ngày:** 2026-09-22 · **Chủ sở hữu:** BA/PO + Dev

> ⛔⛔ **`v0.2` sửa một lỗi của chính `v0.1`.** Bản đầu dựng `đủ ↓` bằng một `<button>` **nằm trong** `<button class="cand">` — **nút lồng nút là HTML ⛔ không hợp lệ**, và trình duyệt thật ⛔ không xử lý được nút trong. ⭐ Bản dựng đã giải đúng chỗ ấy: `<span class="mo" role="button" tabindex="0" data-mo=…>` ＋ bắt click ở **nút ngoài** qua `ev.target.closest('[data-mo]')`. ⚠ Và bài thử `v0.1` **⛔ không bắt được**: DOM giả ⛔ không biết HTML hợp lệ hay ⛔ không — nó cho `button` lồng `button` chạy ngon lành. ⇒ Chặng `3` thêm một cổng đo đúng điều ấy.

**Mục tiêu:** Làm cho ba đường đi **⛔ không dùng được** của màn ghép trở thành dùng được *(bàn phím · ô tìm · bỏ gán)*, và trả lại cho cột **Diễn giải** hai lớp bảo vệ mà hợp đồng thiết kế đòi *(`đủ ↓` ＋ `<mark>`)*.

**Kiến trúc:** ⛔ Không dựng gì mới. Bốn lỗi đều là **mối nối bị thiếu**, ⛔ không phải tính năng thiếu: hàm `phim()` đã viết đủ 9 phím mà ⛔ không ai đăng ký; `#ghep-tim` đã có trong vỏ mà ⛔ không ai nghe; `bo_gan()` đã viết đủ mà đọc một khoá **⛔ không ai sinh**. Mỗi chặng vì thế là *(một bài thử ĐO cái CHẠY → nối dây → cổng canh)*. Chặng cuối tổng quát hoá phép đo để lớp lỗi này ⛔ không quay lại.

**Bộ công cụ:** Python 3.12 ＋ pytest · JS thuần *(⛔ không framework)* · PostgreSQL 16 · khung DOM giả `tests/web/dom_gia.js` ＋ `tests/web/khung_node.py`.

**Đặc tả:** `docs/ap-src/Man gán lệnh chỉ/thiet-ke-man-gan-lenh-chi.md` *(hợp đồng)* ＋ `docs/ap-src/Man gán lệnh chỉ/ban-dung/fls-gan-lenh-chi_10.html` *(bản dựng chạy được)* ＋ `BA-06 §4.5`/`§4.6` · `BA-07 §4h` · `BA-13 §A8`.

---

## Ràng buộc toàn cục

Mọi chặng **đều** chịu các ràng buộc sau. ⛔ Không chặng nào được miễn.

| Ràng buộc | Giá trị chính xác |
|---|---|
| Chữ ký commit | dòng cuối: `Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>` |
| Nhánh | `feat/p2-oracle-parity` · đẩy lên `origin` sau mỗi chặng |
| **Cổng chạy TRƯỚC commit** | ⛔ không phải sau |
| Mã màu | **⛔ KHÔNG** một `#rrggbb`／`rgb(`／`hsl(` nào ngoài `fls/web/tep/tokens.css` — cổng `tests/web/test_khong_ma_mau_go_tay.py` |
| Tên token | mọi `var(--x)` phải có nơi khai — cổng `tests/web/test_moi_token_deu_duoc_khai.py` |
| Bản khai tuyến | thêm tuyến ⇒ khai ở `fls/api/bang_tuyen.py` **và** mọi bảng nó chạm phải có trong `BANG_CHO_PHEP` — cổng `tools/soi_bang_tuyen.py` |
| Bản khai tệp | thêm tệp trong `fls/web/tep/` ⇒ khai ở `BANG_TEP` *(`fls/web/phuc_vu.py`)*, ⛔ không thì **⛔ không bao giờ được phục vụ** |
| Số sống | sửa mã ⇒ chạy `tools/dong_bo_so_song.py --ghi` rồi `tools/kiem_so_song.py` |
| Cổng tài liệu | `docs/ITL/_tools/kiem_tai_lieu.py` — `K1`…`K6` |
| Che dữ liệu cá nhân | tên người → chữ cái đầu · số tài khoản → 4 số cuối, **chỉ cho hiện vật xuất RA NGOÀI kho** *(gồm chính tệp plan này và mọi bài thử)*. Trên màn thì `nguoi_nhan` hiện **NGUYÊN** — `QĐ-ITL-148 ②` |
| ⛔ Hoãn | mọi việc dính **FPS** |
| Môi trường | `./.venv/Scripts/python.exe` · `PYTHONIOENCODING=utf-8` · `PYTHONPATH=.` · kho `postgresql://fls:fls@localhost:5433/fls` |

**Chạy cả bộ:** `PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest -q` — nền hiện tại **`1.810` xanh**.

---

## Cấu trúc tệp

| Tệp | Trách nhiệm | Chặng |
|---|---|---|
| `fls/web/tep/man_f01_ghep.js` | màn — thêm `_noi_ban_phim()`, `_noi_o_tim()`, `danh_dau()`, `soat_cat()` | `1`·`2`·`3`·`4` |
| `fls/web/tep/hinh.css` | kiểu — `.dg.clamp` · `.mo` · `.cand.rong` | `3` |
| `fls/repo/man_ghep.py` | luật đọc — `TU_RAC`, `khoa_bang_chung()`, `itl_da_gan()` | `3`·`4` |
| `fls/repo/lenh_cho.py` | câu SQL đọc lệnh **ĐÃ GÁN** | `4` |
| `fls/api/bang_tuyen.py` | khai tuyến **40** | `4` |
| `fls/api/xu_ly.py` | tay nắm `lenh_da_gan` | `4` |
| `tests/web/test_b3_ban_phim_noi_that.py` | **MỚI** — bắn phím thật vào DOM giả | `1` |
| `tests/web/test_b3_o_tim_song.py` | **MỚI** | `2` |
| `tests/web/test_b3_bang_chung_va_du_xuong.py` | **MỚI** | `3` |
| `tests/repo/test_b1_khoa_bang_chung.py` | **MỚI** | `3` |
| `tests/api/test_b2_cua_lenh_da_gan.py` | **MỚI** | `4` |
| `tests/web/test_moi_o_nhap_deu_co_nguoi_nghe.py` | **MỚI** — cổng tổng quát | `5` |

---

## ⭐⭐⭐ Vì sao bốn lỗi này sống qua **ba** cổng

| Cổng | Nó hỏi gì | Nó **⛔ không** hỏi gì |
|---|---|---|
| `test_b3_fe_bam_thiet_ke.py` | *"mã có chứa `'ArrowDown'` ⛔ không"* | *"ai gọi khi người thật gõ"* |
| `test_b3_man_ghep_chay_duoc.py` | gọi thẳng `F01G.phim({key:'Enter'})` | *(cùng câu trên)* |
| `test_b3_man_ghep_tu_nap_danh_sach.py` | *"màn có tự gọi cửa ⛔ không"* | chỉ hỏi cho **danh sách** |

⭐⭐ **Bài thử với tay VÀO gọi thứ mà sản phẩm phải với tay RA nối.** Đây là **lần thứ ba** cùng một hình dạng *(① nhét `ST.dong` · ② gọi thẳng `phim` · ③ gọi thẳng `tim_focus`)*.

⇒ Mọi bài thử mới trong plan này **⛔ KHÔNG** được gọi thẳng một tay nắm. Chúng **bắn sự kiện** *(`_ban('keydown', …)`, `_ban('input', …)`)* và đo phản ứng. Khung `tests/web/dom_gia.js:206` đã có sẵn đường ấy — `hop._ban = d.ban` *(`khung_node.py:131`)*.

---

## Chặng 1 · Nối bàn phím

**Tệp:**
- Sửa: `fls/web/tep/man_f01_ghep.js` *(thêm `_noi_ban_phim`, gọi từ `mo_man`)*
- Tạo: `tests/web/test_b3_ban_phim_noi_that.py`

**Giao diện:**
- Dùng: `phim(e)` · `ST` · `ve()` — đã có
- Sinh ra: `_noi_ban_phim()` *(⛔ không xuất ra ngoài — gọi từ `mo_man()`)*; `F01G` thêm khoá `da_noi_ban_phim: () => boolean` cho bài thử

⭐ Theo đúng khuôn `man_f02.js:683` `_noi_ban_phim()` — **một cờ `_da_noi`**, đăng ký trên `document`, và **tự chặn** khi màn ⛔ không bật.

- [ ] **Bước 1 · Viết bài thử ĐỎ**

Tạo `tests/web/test_b3_ban_phim_noi_that.py`:

```python
# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ Ban phim co NOI vao `document` that ⛔ khong.

⛔⛔⛔ **Ba cong da xanh trong khi `0/9` phim dung duoc tren trinh duyet.**
   `phim()` cai du 9 phim, dung hanh vi — va `F01G.phim` chi duoc goi tu
   **hai dong cua chinh bo test**. Trong ca `fls/web/` ⛔ khong mot
   `addEventListener('keydown', ...)` nao tro toi no.

⭐⭐ **Bai thu voi tay VAO goi thu ma san pham phai voi tay RA noi.** ⇒ Bai
   nay **⛔ KHONG goi `F01G.phim`**. No **BAN mot su kien** qua `_ban`
   *(`khung_node.py:131`)* va do phan ung — dung duong mot nguoi go phim di.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

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


def _hang(ma, tien="1000.00"):
    return {"pm_line_id": ma, "the": {
        "ma_lenh": ma, "trang_thai": "chua_gan", "trang_thai_nhan": "Chưa gán",
        "trang_thai_mau": "", "loai_phieu": "Regular", "noi_dung": "TT " + ma,
        "so_tien": tien, "curr": "USD", "nguoi_nhan": "S. INC.",
        "so_chung_tu": None, "phap_nhan": "SGO2", "ngan_hang": "OCBC",
        "tai_khoan": "••4001", "cdt": "CVL | VisionLab", "nhom_du_truong": []}}


def _dat():
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": [_hang("PM1-1"), _hang("PM2-1"), _hang("PM3-1")],
                      "next_cursor": None}}, ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};')


def test_MUI_XUONG_di_chuyen_con_tro_khi_NGUOI_go_phim():
    """⛔ ⛔ Khong goi `F01G.phim` — ban mot `keydown` that."""
    r = _chay(_dat()
              + " await F01G.mo_man();"
              " const truoc = F01G.ST.tro;"
              " _ban('keydown', {key: 'ArrowDown'});"
              " return {truoc, sau: F01G.ST.tro};",
              tep=TEP, vo=VO)
    assert r["truoc"] == 0
    assert r["sau"] == 1, (
        "⛔⛔ Go `↓` mà con trỏ ⛔ KHÔNG nhúc nhích — bàn phím ⛔ chưa nối vào "
        "`document`. Hàm `phim()` có tồn tại ⛔ không phải là nó có chạy.")


def test_MUI_PHAI_mo_lenh_dang_tro():
    r = _chay(_dat()
              + "_TRA['/queue/lenh/PM1-1/itl-candidates'] = {data: {ung_vien: []}};"
              "_TRA['/queue/lenh/PM1-1/so'] = {data: {ung_vien: []}};"
              " await F01G.mo_man();"
              " _ban('keydown', {key: 'ArrowRight'});"
              " await new Promise(r => setTimeout(r, 0));"
              " return F01G.ST.mo;",
              tep=TEP, vo=VO)
    assert r == "PM1-1", f"⛔ `→` ⛔ không mở lệnh đang trỏ, ST.mo = {r!r}"


def test_phim_KHONG_an_vao_man_khac_dang_bat():
    """⛔⛔ Mot listener tren `document` nghe **moi** phim cua **moi** man.

    `man_f02.js:719` da phai dat dung phep chan nay. Thieu no thi go `j` o
    man `F02` se **doi lenh chi** o mot man ⛔ khong ai dang nhin.
    """
    vo_tat = VO.replace("man.className = 'screen on';",
                        "man.className = 'screen';")
    r = _chay(_dat()
              + " await F01G.mo_man();"
              " const truoc = F01G.ST.tro;"
              " _ban('keydown', {key: 'ArrowDown'});"
              " return {truoc, sau: F01G.ST.tro};",
              tep=TEP, vo=vo_tat)
    assert r["sau"] == r["truoc"], (
        "⛔⛔ Màn ⛔ KHÔNG bật mà vẫn ăn phím — nó đang cướp bàn phím của màn khác")


def test_noi_DUNG_MOT_lan_du_mo_man_nhieu_luot():
    """⛔ `mo_man` chay moi lan doi tab ⇒ ⛔ khong co co thi moi luot them mot
    listener, va mot cu go `↓` se nhay **n** buoc."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_man(); await F01G.mo_man();"
              " F01G.ST.tro = 0;"
              " _ban('keydown', {key: 'ArrowDown'});"
              " return F01G.ST.tro;",
              tep=TEP, vo=VO)
    assert r == 1, f"⛔ nối {r} lần — một cú `↓` nhảy {r} bước"
```

- [ ] **Bước 2 · Chạy để chắc nó ĐỎ**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_b3_ban_phim_noi_that.py -q
```

Chờ: **4 ĐỎ**. Bài đầu báo `sau == 0` *(con trỏ ⛔ không nhúc nhích)*.

- [ ] **Bước 3 · Nối dây**

Trong `fls/web/tep/man_f01_ghep.js`, thêm **ngay trên** `function tim_focus()`:

```js
  /* ⛔⛔⛔ **`phim()` da viet du 9 phim tu `21/09` va ⛔ KHONG AI GOI NO.**
     Ba cong deu xanh: hai cong quet chu thay day du 9 chuoi phim, cong chay
     ma thi **tu goi thang** `F01G.phim({key:'Enter'})`. ⛔ Khong cong nao hoi
     *"ai goi no khi nguoi that go"*.

     ⭐ Theo dung khuon `man_f02.js:683` — mot co, mot listener tren
       `document`, va **tu chan** khi man ⛔ khong bat. */
  let _da_noi = false;

  function _noi_ban_phim() {
    if (_da_noi) return;
    _da_noi = true;
    document.addEventListener('keydown', function (e) {
      /* ⛔⛔ Mot listener tren `document` nghe phim cua **MOI** man. Thieu
         phep chan nay thi go `j` o `F02` se doi lenh chi o mot man ⛔ khong
         ai dang nhin — `man_f02.js:719` da phai dat dung phep chan ay. */
      const man = document.querySelector('#man-ghep');
      if (!man || !man.classList.contains('on')) return;
      /* ⭐ Chan cuon trang cho phim DIEU HUONG. ⛔ Khong chan `Enter`/`Escape`:
         chung ⛔ khong cuon, va chan bua la cuop mat hanh vi mac dinh cua o
         nhap. */
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', '/']
          .indexOf(e.key) >= 0 && e.preventDefault) e.preventDefault();
      phim(e);
    });
  }
```

Trong `mo_man()`, thêm **dòng đầu tiên** của thân hàm:

```js
  async function mo_man() {
    _noi_ban_phim();
    ve();
```

Và trong khối `return {…}` cuối tệp, thêm khoá:

```js
           da_noi_ban_phim: () => _da_noi,
```

- [ ] **Bước 4 · Chạy để chắc nó XANH**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_b3_ban_phim_noi_that.py -q
```

Chờ: **4 XANH**.

- [ ] **Bước 5 · Diễn tập phá** *(`NFR-I15` — cổng chưa từng thấy đỏ là cổng chưa biết có sống)*

Tạm đổi `_noi_ban_phim();` trong `mo_man` thành `/* pha */`, chạy lại — chờ **≥ 2 ĐỎ**. Khôi phục, chạy lại — chờ **4 XANH**.

- [ ] **Bước 6 · Cả bộ ＋ cổng**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest -q
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/dong_bo_so_song.py --ghi
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/kiem_so_song.py
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe docs/ITL/_tools/kiem_tai_lieu.py
```

Chờ: `1.814` xanh · số sống `109/109` · tài liệu `6/6`.

- [ ] **Bước 7 · Commit**

```bash
git add tests/web/test_b3_ban_phim_noi_that.py fls/web/tep/man_f01_ghep.js docs/
git commit -F- <<'EOF'
fix(ghep): noi ban phim — 9 phim viet du tu 21/09 va khong ai goi

`phim()` cai du 9 phim, dung hanh vi, va `F01G.phim` chi duoc goi tu hai
dong cua chinh bo test. Trong ca `fls/web/` khong mot addEventListener
('keydown') nao tro toi no => 0/9 phim dung duoc tren trinh duyet.

Ba cong deu xanh: hai cong quet chu thay du 9 chuoi phim; cong chay ma tu
goi thang F01G.phim(...). Khong cong nao hoi "ai goi no khi nguoi that go".

Bai thu moi KHONG goi tay nam — no BAN mot keydown that qua `_ban` va do
phan ung. Kem phep chan "man khong bat thi khong an phim" (khuon
man_f02.js:719) va co `_da_noi` chong noi nhieu lan.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
git push origin feat/p2-oracle-parity
```

---

## Chặng 2 · Nối ô tìm giao dịch

**Tệp:**
- Sửa: `fls/web/tep/man_f01_ghep.js` *(thêm `_noi_o_tim`, sửa `tai_toan_so`)*
- Tạo: `tests/web/test_b3_o_tim_song.py`

**Giao diện:**
- Dùng: `ST.tim` · `tai_toan_so(ma)` · `ve()` — đã có
- Sinh ra: `_noi_o_tim()`; `F01G` thêm `TRE_TIM` *(số mili-giây chờ, `250`)*

⭐⭐ **Quyết định:** gõ vào ô tìm **bật Toàn sổ**. Lý do đo được: danh sách ứng viên máy đề xuất đã nhỏ và cố định *(`SO_MAC_DINH = 50`)*, nên lọc trong đó ⛔ không trả lời được câu *"tiền của tôi nằm ở đâu khác"* — mà đó đúng là lý do người ta gõ. Việc này cũng trả lại **lối bật Toàn sổ bằng tay** mà hợp đồng `§8` đòi và màn hiện ⛔ không có *(`ST.toan_so` chỉ tự bật khi `ung_vien.length === 0`)*.

- [ ] **Bước 1 · Viết bài thử ĐỎ**

Tạo `tests/web/test_b3_o_tim_song.py`:

```python
# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐ O tim giao dich co SONG ⛔ khong.

⛔⛔ `#ghep-tim` co trong vo tu `21/09` *(`index.html:132`)* va trong ca
   `fls/web/` no xuat hien dung **hai** cho: dong khai ay, va `tim_focus()`
   nhay vao no. ⛔ Khong mot `oninput` nao ⇒ `ST.tim` vinh vien `''`, va
   cua `/queue/lenh/{pm}/so?q=` — da cai day du o `man_ghep.py:270` —
   **⛔ chua bao gio duoc goi voi mot chu nao**.

⭐ Bai nay ban su kien `input` that, ⛔ khong gan thang `ST.tim`.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

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

UV = {"itl_id": 42, "doc_date": "2026-09-18", "doc_no": "1026946429",
      "dien_giai": "Card charge OPENAI", "amount": "1000.00", "chieu": "co",
      "curr": "USD", "nguon": {"tk": "PO2", "bank": "OCBC", "curr": "USD",
                               "le": "SGO2"}, "bac": "ma", "lech": None}


def _hang(ma):
    return {"pm_line_id": ma, "the": {
        "ma_lenh": ma, "trang_thai": "chua_gan", "trang_thai_nhan": "Chưa gán",
        "trang_thai_mau": "", "loai_phieu": "Regular", "noi_dung": "TT " + ma,
        "so_tien": "1000.00", "curr": "USD", "nguoi_nhan": "S. INC.",
        "so_chung_tu": None, "phap_nhan": "SGO2", "ngan_hang": "OCBC",
        "tai_khoan": "••4001", "cdt": "CVL | VisionLab", "nhom_du_truong": []}}


def _dat():
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": [_hang("PM1-1")], "next_cursor": None}},
            ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};'
        "_TRA['/queue/lenh/PM1-1/itl-candidates'] = "
        "  {data: {ung_vien: " + json.dumps([UV]) + "}};"
        "_TRA['/queue/lenh/PM1-1/so?q=OPENAI'] = "
        "  {data: {ung_vien: " + json.dumps([UV]) + "}};")


def test_GO_vao_o_tim_thi_cua_SO_duoc_goi_kem_chu():
    r = _chay(_dat()
              + " await F01G.mo_man();"
              " await F01G.mo_lenh('PM1-1');"
              " const t = document.querySelector('#ghep-tim');"
              " t.value = 'OPENAI';"
              " _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 40));"
              " return {tim: F01G.ST.tim,"
              "         duong: _GOI.filter(g => g[0] === 'doc').map(g => g[1])};",
              tep=TEP, vo=VO)
    assert r["tim"] == "OPENAI", (
        f"⛔⛔ Gõ vào ô tìm mà `ST.tim` vẫn {r['tim']!r} — ô tìm ⛔ chưa nối")
    assert "/queue/lenh/PM1-1/so?q=OPENAI" in r["duong"], (
        f"⛔ cửa tra sổ ⛔ không được gọi kèm chữ. Đã gọi: {r['duong']}")


def test_GO_bat_san_TOAN_SO():
    """⭐ Đây cũng là **lối bật Toàn sổ bằng tay** mà hợp đồng `§8` đòi và màn
    hiện ⛔ không có — `ST.toan_so` chỉ tự bật khi `ung_vien.length === 0`."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const truoc = F01G.ST.toan_so;"
              " const t = document.querySelector('#ghep-tim');"
              " t.value = 'OPENAI'; _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 40));"
              " return {truoc, sau: F01G.ST.toan_so};",
              tep=TEP, vo=VO)
    assert r["truoc"] is False and r["sau"] is True


def test_GO_NHANH_chi_goi_cua_MOT_lan():
    """⛔⛔ ⛔ Khong cho tre thi go `OPENAI` = **6** luot goi cua, va luot ve
    sau co the tra loi TRUOC luot ve truoc ⇒ danh sach nhap nhay rồi **dừng ở
    một kết quả của chuỗi chữ CŨ**."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const t = document.querySelector('#ghep-tim');"
              " const n0 = _GOI.length;"
              " for (const c of ['O','OP','OPE','OPEN','OPENA','OPENAI']) {"
              "   t.value = c; _ban('input', {target: t}); }"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 60));"
              " return _GOI.slice(n0).filter(g => g[1].indexOf('/so') >= 0).length;",
              tep=TEP, vo=VO)
    assert r == 1, f"⛔ gõ 6 ký tự ⇒ **{r}** lượt gọi cửa, phải là **1**"


def test_XOA_HET_chu_thi_ve_lai_ung_vien_MAY_de_xuat():
    """⛔ Xoá hết mà vẫn ở Toàn sổ là **⛔ không có đường lùi**."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const t = document.querySelector('#ghep-tim');"
              " t.value = 'OPENAI'; _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 40));"
              " t.value = ''; _ban('input', {target: t});"
              " await new Promise(r => setTimeout(r, F01G.TRE_TIM + 40));"
              " return {tim: F01G.ST.tim, toan_so: F01G.ST.toan_so};",
              tep=TEP, vo=VO)
    assert r["tim"] == "" and r["toan_so"] is False
```

- [ ] **Bước 2 · Chạy để chắc nó ĐỎ**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_b3_o_tim_song.py -q
```

Chờ: **4 ĐỎ** *(bài đầu: `ST.tim` là `''`)*.

- [ ] **Bước 3 · Nối dây**

Trong `man_f01_ghep.js`, thêm hằng cạnh `TRAN_DONG`:

```js
  /* ⭐ Cho **250ms** sau phim cuoi roi moi hoi cua. ⛔ Khong cho thi go
     `OPENAI` = **6** luot goi, va luot ve sau co the ve TRUOC luot ve truoc
     ⇒ danh sach dung lai o ket qua cua mot chuoi chu **da cu**. */
  const TRE_TIM = 250;
```

Thêm **ngay dưới** `_noi_ban_phim()`:

```js
  let _hen_tim = null;

  /* ⛔⛔ `#ghep-tim` co trong vo tu `21/09` va trong ca `fls/web/` no xuat
     hien dung **hai** cho: dong khai, va `tim_focus()` nhay vao no. ⇒ Mot o
     nhap **⛔ khong ai nghe**, va cua `?q=` da cai day du thi ⛔ chua bao gio
     duoc goi voi mot chu nao. */
  function _noi_o_tim() {
    const t = document.querySelector('#ghep-tim');
    if (!t || t._da_noi || !t.addEventListener) return;
    t._da_noi = true;
    t.addEventListener('input', function () {
      const chu = String(t.value || '').trim();
      if (_hen_tim) clearTimeout(_hen_tim);
      _hen_tim = setTimeout(async function () {
        ST.tim = chu;
        /* ⭐⭐ Go chu = **bat Toan so**. Danh sach may de xuat toi da `50`
           dong va co dinh, nen loc trong no ⛔ khong tra loi duoc cau
           *"tien cua toi nam o dau khac"* — dung cau khien nguoi ta go.
           ⭐ Day cung la **loi bat Toan so bang tay** ma `§8` doi va man
             ⛔ chua co: `ST.toan_so` moi chi TU bat khi `ung_vien` rong. */
        ST.toan_so = chu !== '';
        ST.ung_vien_chon = null; ST.xac_nhan = false;
        if (!ST.mo) { ve(); return; }
        if (chu) await tai_toan_so(ST.mo);
        else await mo_lenh(ST.mo);   /* ⛔ xoa het ⇒ co duong LUI */
        ve();
      }, TRE_TIM);
    });
  }
```

Trong `mo_man()`, thêm ngay sau `_noi_ban_phim();`:

```js
    _noi_o_tim();
```

Thêm `TRE_TIM` vào khối `return {…}`.

- [ ] **Bước 4 · Chạy để chắc nó XANH**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_b3_o_tim_song.py -q
```

Chờ: **4 XANH**.

- [ ] **Bước 5 · Diễn tập phá**

Đổi `TRE_TIM` thành `0` — chờ `test_GO_NHANH_chi_goi_cua_MOT_lan` **ĐỎ** *(6 lượt)*. Khôi phục `250`.

- [ ] **Bước 6 · Cả bộ ＋ cổng** *(y như Chặng 1 bước 6)*

Chờ `1.818` xanh.

- [ ] **Bước 7 · Commit**

```bash
git add tests/web/test_b3_o_tim_song.py fls/web/tep/man_f01_ghep.js docs/
git commit -F- <<'EOF'
fix(ghep): noi o tim — cua `?q=` cai day du va chua bao gio duoc goi

`#ghep-tim` co trong vo tu 21/09; trong ca fls/web/ no xuat hien dung hai
cho: dong khai, va tim_focus() nhay vao no. Khong mot oninput nao => ST.tim
vinh vien '' va cua /queue/lenh/{pm}/so?q= chua bao gio nhan mot chu.

Go chu = bat Toan so. Danh sach may de xuat toi da 50 dong va co dinh nen
loc trong no khong tra loi duoc cau "tien cua toi nam o dau khac" — dung
cau khien nguoi ta go. Viec nay cung tra lai LOI BAT TOAN SO BANG TAY ma
hop dong §8 doi va man chua co.

Tre 250ms: khong co thi go "OPENAI" = 6 luot goi cua, va luot ve sau co the
ve truoc luot ve truoc => danh sach dung o ket qua cua chuoi chu da cu.
Xoa het chu => ve lai ung vien may de xuat (co duong lui).

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
git push origin feat/p2-oracle-parity
```

---

## Chặng 3 · Trả lại hai lớp bảo vệ cho cột Diễn giải

**Tệp:**
- Sửa: `fls/repo/man_ghep.py` *(thêm `TU_RAC`, `khoa_bang_chung()`)*
- Sửa: `fls/web/tep/man_f01_ghep.js` *(thêm `danh_dau()`, `soat_cat()`, sửa `ve_ung_vien`)*
- Sửa: `fls/web/tep/hinh.css` *(thêm `.dg.clamp`, `.mo`, `.cand.rong`, `mark`)*
- Tạo: `tests/repo/test_b1_khoa_bang_chung.py` · `tests/web/test_b3_bang_chung_va_du_xuong.py`

**Giao diện:**
- Dùng: `TRUONG_UNG_VIEN` · `khuon_the_lenh` — đã có
- Sinh ra:
  - `man_ghep.TU_RAC: frozenset[str]`
  - `man_ghep.khoa_bang_chung(lenh: dict, uv: dict) -> list[str]` — các chuỗi đáng tô, **dài trước ngắn sau**
  - JS: `danh_dau(chu, khoa) -> string` *(HTML đã thoát, có `<mark>`)*, `soat_cat()`, `ST.dg_mo: number|null`

⭐⭐ **Vì sao bộ khoá tính ở TẦNG ĐỌC, ⛔ không ở JS.** Bộ **từ rác** là một **luật nghiệp vụ** *(từ nào là tên pháp lý vô nghĩa khi đối chiếu)*, ⛔ không phải một mẹo hiển thị. Để nó ở JS thì ⛔ không bài thử Python nào chạm tới, và nó sẽ lệch với mọi phép đối chiếu khác của hệ.

- [ ] **Bước 1 · Viết bài thử ĐỎ phía Python**

Tạo `tests/repo/test_b1_khoa_bang_chung.py`:

```python
# -*- coding: utf-8 -*-
"""`B1` — ⭐⭐ Khoa BANG CHUNG: to cai gi trong dien giai sao ke.

⭐ Dien giai la **bang chung duy nhat** cua `4.145/8.387` = **49%** cuon so
  *(nhanh nuoc ngoai, `DT-I13 ⓑ`)*. Hop dong `§6` doi to **ba** thu: so
  chung tu **chi khi trung dung**, so tien **khi khop tuyet doi**, va ten
  vendor — sau khi loc **tu rac** de ⛔ khong to nhieu.

⛔⛔ **Bo tu rac la mot LUAT NGHIEP VU, ⛔ khong phai meo hien thi.** De no o
   JS thi ⛔ khong mot bai thu Python nao cham toi, va no se lech voi moi
   phep doi chieu khac cua he.
"""
from __future__ import annotations

from fls.repo import man_ghep as mg

LENH = {"ma_lenh": "PM1-1", "so_tien": "1000.00", "curr": "USD",
        "so_chung_tu": "1026946429", "nguoi_nhan": "SENSORTOWER, INC."}
UV = {"itl_id": 42, "doc_no": "1026946429", "amount": "1000.00",
      "curr": "USD", "dien_giai": "SENSORTOWER INC 1026946429 1000.00"}


def test_so_chung_tu_CHI_to_khi_TRUNG_DUNG():
    assert "1026946429" in mg.khoa_bang_chung(LENH, UV)
    khac = dict(UV, doc_no="9999999999")
    assert "1026946429" not in mg.khoa_bang_chung(LENH, khac)


def test_so_tien_CHI_to_khi_khop_TUYET_DOI():
    assert "1000.00" in mg.khoa_bang_chung(LENH, UV)
    lech = dict(UV, amount="987.60")
    assert "1000.00" not in mg.khoa_bang_chung(LENH, lech)
    te_khac = dict(UV, curr="VND")
    assert "1000.00" not in mg.khoa_bang_chung(LENH, te_khac)


def test_TU_RAC_bi_loai_khoi_ten_vendor():
    """⛔⛔ ⛔ Khong loc thi `INC` to **moi** dong co chu `inc` — va luc ay
    mau danh dau thoi mang nghia."""
    k = mg.khoa_bang_chung(LENH, UV)
    assert "SENSORTOWER" in k
    for rac in ("INC", "inc", "COMPANY", "TNHH"):
        assert rac not in k, f"⛔ `{rac}` la tu rac ma van lot vao khoa"


def test_tu_NGAN_hon_BA_ky_tu_bi_loai():
    """⭐ Mot chuoi `2` ky tu se to **rai rac khap** moi dien giai."""
    l = dict(LENH, nguoi_nhan="AB CD SENSORTOWER")
    assert all(len(x) >= 3 for x in mg.khoa_bang_chung(l, UV))


def test_khoa_xep_DAI_TRUOC_de_khong_to_LONG_nhau():
    """⛔⛔ To `1026946429` roi to tiep `102` ben trong no se ra `<mark>`
    **long nhau** va HTML vo. ⇒ Quet **mot luot** bang regex hop nhat, va
    thu tu dai-truoc bao dam mieng dai thang."""
    k = mg.khoa_bang_chung(LENH, UV)
    assert k == sorted(k, key=len, reverse=True)


def test_KHONG_khoa_TRUNG_nhau():
    l = dict(LENH, nguoi_nhan="SENSORTOWER SENSORTOWER")
    k = mg.khoa_bang_chung(l, UV)
    assert len(k) == len(set(x.lower() for x in k))
```

- [ ] **Bước 2 · Chạy để chắc nó ĐỎ**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/repo/test_b1_khoa_bang_chung.py -q
```

Chờ: **6 ĐỎ** — `AttributeError: module 'fls.repo.man_ghep' has no attribute 'khoa_bang_chung'`.

- [ ] **Bước 3 · Viết luật đọc**

Thêm vào cuối `fls/repo/man_ghep.py`:

```python
# ── ⓙ khoa BANG CHUNG — to cai gi trong dien giai ───────────────────────

#: ⭐ Tu RAC — tu phap ly／chung chung, to chung len thi mau **thoi mang
#: nghia**. Lay nguyen tu ban dung (`fls-gan-lenh-chi_10.html:459-461`).
#: ⚠ So sanh bang **chu thuong**, nen moi muc o day phai la chu thuong.
TU_RAC: frozenset[str] = frozenset("""
thanh toan toán công ty tnhh cong cty chi phi phí joint stock company corp
corporation inc incorporated ltd limited pte plc llc gmbh group holding
holdings services service trading trade quoc te quốc tế viet nam việt và and
the for bank
""".split())

#: ⛔ Chuoi ngan hon nguong nay se to **rai rac khap** moi dien giai.
DAI_TOI_THIEU = 3


def khoa_bang_chung(lenh: dict[str, Any], uv: dict[str, Any]) -> list[str]:
    """Cac chuoi dang to trong dien giai — ⭐ **dai truoc, ngan sau**.

    Hop dong `§6` doi **ba** nguon, moi nguon mot dieu kien rieng:
      ⓐ `so_chung_tu` — **CHI khi trung dung** so cua lenh chi;
      ⓑ `so_tien` — **CHI khi khop tuyet doi** *(ca so LAN don vi tien)*;
      ⓒ ten ben nhan — sau khi **loc tu rac**.

    ⛔⛔ Thu tu **dai truoc** ⛔ khong phai cho dep: to `1026946429` roi to
       tiep `102` nam **ben trong** no se ra `<mark>` **long nhau** va HTML
       vo. Quet **mot luot** bang mot regex hop nhat, mieng dai thang.
    """
    ra: list[str] = []
    ct = lenh.get("so_chung_tu")
    if ct and str(ct).strip() and str(uv.get("doc_no") or "") == str(ct):
        ra.append(str(ct))
    tien = lenh.get("so_tien")
    if (tien is not None
            and str(uv.get("curr")) == str(lenh.get("curr"))
            and _bang_so(uv.get("amount")) == _bang_so(tien)):
        ra.append(str(tien))
    for tu in re.split(r"[\s,._\-/()]+", str(lenh.get("nguoi_nhan") or "")):
        if len(tu) >= DAI_TOI_THIEU and tu.lower() not in TU_RAC:
            ra.append(tu)
    thay: set[str] = set()
    sach: list[str] = []
    for k in ra:
        t = k.lower()
        if len(k) < DAI_TOI_THIEU or t in thay:
            continue
        thay.add(t)
        sach.append(k)
    return sorted(sach, key=len, reverse=True)


def _bang_so(x: Any) -> Decimal | None:
    try:
        return Decimal(str(x))
    except (InvalidOperation, TypeError, ValueError):
        return None
```

Thêm vào đầu tệp *(cạnh các `import` sẵn có)*:

```python
from decimal import Decimal, InvalidOperation
```

⚠ Kiểm `import re` và `from typing import Any` đã có ở đầu tệp — nếu chưa thì thêm.

- [ ] **Bước 4 · Chạy để chắc nó XANH**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/repo/test_b1_khoa_bang_chung.py -q
```

Chờ: **6 XANH**.

- [ ] **Bước 5 · Cho cửa trả bộ khoá**

Trong `fls/api/xu_ly.py`, hàm `ung_vien_tien` *(tay nắm của `/queue/lenh/{pm_line_id}/itl-candidates`)*, sau khi dựng danh sách `ung_vien`, thêm khoá `khoa_to` cho **từng** ứng viên:

```python
    # ⭐⭐ Bo khoa **BANG CHUNG** tinh o tang doc, ⛔ khong o JS: bo tu rac la
    #   mot LUAT NGHIEP VU, va mot ban thu hai bang JS se lech.
    the = mg.khuon_the_lenh(dong_lenh)
    for u in ra["ung_vien"]:
        u["khoa_to"] = mg.khoa_bang_chung(the, u)
```

⚠ Đọc `fls/api/xu_ly.py` quanh `def ung_vien_tien` để lấy đúng tên biến đang giữ hàng lệnh và danh sách trả về. Cập nhật `BA-07 §4h` khai thêm trường `khoa_to` *(trường thứ **11** của `ung_vien[]`)*.

- [ ] **Bước 6 · Viết bài thử ĐỎ phía màn**

Tạo `tests/web/test_b3_bang_chung_va_du_xuong.py`:

```python
# -*- coding: utf-8 -*-
"""`B3` — ⭐⭐⭐ Hai lop bao ve cua cot **Dien giai**.

⛔⛔ Hop dong `§6.2` viet thang: ***"⛔ Khong dung tooltip lam loi duy nhat"***.
   Truoc ban va nay, tooltip **la** loi duy nhat: `white-space:nowrap` ＋
   `title`, ⛔ khong `đủ ↓`, ⛔ khong `<mark>`, va token `--evi-bg` khai o
   `tokens.css` roi **dung 0 lan** trong ca kho.

⭐ Dien giai la bang chung duy nhat cua **49%** cuon so.
"""
from __future__ import annotations

import json

from tests.web.khung_node import _chay

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
THE = {"ma_lenh": "PM1-1", "trang_thai": "chua_gan",
       "trang_thai_nhan": "Chưa gán", "trang_thai_mau": "",
       "loai_phieu": "Regular", "noi_dung": "TT S.", "so_tien": "1000.00",
       "curr": "USD", "nguoi_nhan": "S. INC.", "so_chung_tu": "1026946429",
       "phap_nhan": "SGO2", "ngan_hang": "OCBC", "tai_khoan": "••4001",
       "cdt": "CVL | VisionLab", "nhom_du_truong": []}

UV = {"itl_id": 42, "doc_date": "2026-09-18", "doc_no": "1026946429",
      "dien_giai": "CARD 1026946429 S. 1000.00 THANH TOAN",
      "amount": "1000.00", "chieu": "co", "curr": "USD",
      "nguon": {"tk": "PO2", "bank": "OCBC", "curr": "USD", "le": "SGO2"},
      "bac": "ma", "lech": None,
      "khoa_to": ["1026946429", "1000.00"]}


def _dat(uv=None):
    return (
        "_TRA[" + json.dumps(D_NGUOI) + "] = " + json.dumps(
            {"data": {"rows": [{"pm_line_id": "PM1-1", "the": THE}],
                      "next_cursor": None}}, ensure_ascii=False) + ";"
        "_TRA[" + json.dumps(D_MAY) + "] = "
        '{"data": {"rows": [], "next_cursor": null}};'
        "_TRA['/queue/lenh/PM1-1/itl-candidates'] = "
        "  {data: {ung_vien: " + json.dumps(uv or [UV], ensure_ascii=False) + "}};")


def test_BANG_CHUNG_duoc_TO_trong_dien_giai():
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const dg = document.querySelectorAll('.dg')[0];"
              " return dg.innerHTML;",
              tep=TEP, vo=VO)
    assert "<mark>1026946429</mark>" in r, (
        f"⛔ số chứng từ trùng ⛔ không được tô. innerHTML = {r!r}")
    assert "<mark>1000.00</mark>" in r, "⛔ số tiền khớp tuyệt đối ⛔ không được tô"


def test_KHONG_co_khoa_thi_KHONG_to_gi():
    uv = dict(UV, khoa_to=[])
    r = _chay(_dat([uv])
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " return document.querySelectorAll('.dg')[0].innerHTML;",
              tep=TEP, vo=VO)
    assert "<mark" not in r


def test_dien_giai_duoc_THOAT_truoc_khi_to():
    """⛔⛔ `dien_giai` la chu **tu sao ke ngan hang**, tuc chu ⛔ khong ai
    kiem soat. Ghep thang vao `innerHTML` la mo mot duong chen the."""
    uv = dict(UV, dien_giai="<img src=x onerror=1> 1026946429")
    r = _chay(_dat([uv])
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " return document.querySelectorAll('.dg')[0].innerHTML;",
              tep=TEP, vo=VO)
    assert "<img" not in r, f"⛔⛔ thẻ lạ lọt nguyên vào màn: {r!r}"
    assert "&lt;img" in r


def test_DU_XUONG_hien_khi_BI_CAT_va_AN_khi_khong():
    """⛔⛔ Hop dong doi do `scrollHeight` **sau khi da dan trang**, ⛔ khong
    doan theo so ky tu — be rong cot doi theo man."""
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const d0 = document.querySelectorAll('.dg')[0];"
              " d0._scrollHeight = 40; d0._clientHeight = 18;"
              " F01G.soat_cat();"
              " const bi_cat = document.querySelectorAll('.mo')[0].style.display;"
              " d0._scrollHeight = 18; F01G.soat_cat();"
              " const vua = document.querySelectorAll('.mo')[0].style.display;"
              " return {bi_cat, vua};",
              tep=TEP, vo=VO)
    assert r["bi_cat"] == "inline-block", "⛔ bị cắt mà ⛔ không mời `đủ ↓`"
    assert r["vua"] == "none", (
        "⛔ ⛔ không bị cắt mà vẫn mời `đủ ↓` — một lời mời vô nghĩa dạy người "
        "ta thôi tin mọi lời mời")


def test_bam_DU_XUONG_thi_dong_CAO_THEM_va_hien_NGUYEN_VAN():
    r = _chay(_dat()
              + " await F01G.mo_man(); await F01G.mo_lenh('PM1-1');"
              " const dong = document.querySelectorAll('.cand')[0];"
              " const nut = document.querySelectorAll('.mo')[0];"
              /* ⭐ Ban su kien qua NUT NGOAI — dung duong mot cu bam that di,
                 vi `.mo` ⛔ khong co listener rieng (no la mot `span`). */
              " dong._nghe.click[0]({target: nut});"
              " const d0 = document.querySelectorAll('.dg')[0];"
              " return {lop_dg: d0.className,"
              "         lop_dong: document.querySelectorAll('.cand')[0].className,"
              "         nhan: document.querySelectorAll('.mo')[0].textContent};",
              tep=TEP, vo=VO)
    assert "clamp" not in r["lop_dg"], "⛔ bấm `đủ ↓` mà chữ vẫn bị kẹp một dòng"
    assert "rong" in r["lop_dong"], "⛔ dòng ⛔ không cao thêm"
    assert "thu gọn" in r["nhan"]


def test_KHONG_co_NUT_nao_nam_TRONG_mot_NUT():
    """⛔⛔⛔ **Nut long nut la HTML ⛔ KHONG hop le** — trinh duyet that ⛔ khong
    xu ly duoc nut trong, con DOM gia thi cho chay ngon lanh.

    ⭐⭐ Day dung la lop loi ma mot khuon thu **⛔ KHONG THE** bat: no ⛔ khong
       phan tich HTML, no chi dung cay the. ⇒ Do o **ma nguon**, va do bang
       cach dem — `.cand` la mot `<button>`, nen moi `TP.el('button', …)` ben
       trong no la mot loi.

    ⭐ Ban dung da giai dung cho nay: `<span class="mo" role="button"
      tabindex="0" data-mo=…>` ＋ bat click o **nut ngoai** qua `closest`.
    """
    import io
    import pathlib
    import re
    js = (pathlib.Path(__file__).resolve().parents[2]
          / "fls" / "web" / "tep" / "man_f01_ghep.js")
    ma = io.open(js, encoding="utf-8").read()
    ma = re.sub(r"/\*[\s\S]*?\*/", "", ma)
    ma = re.sub(r"(?m)^\s*//.*$", "", ma)
    # ⭐ Trong `ve_ung_vien` — than cua mot `<button class="cand">`.
    than = ma[ma.index("function ve_ung_vien"):]
    than = than[:than.index("\n  function ")]
    xau = re.findall(r"""['"]button['"]""", than)
    assert xau == [], (
        f"⛔⛔ `ve_ung_vien` dung **{len(xau)}** the `button` ben trong mot "
        "`<button class=\"cand\">` — HTML ⛔ khong hop le. Dung `span` kem "
        "`role=\"button\"` ＋ `tabindex` va bat click o nut NGOAI qua `closest`.")


def test_token_evi_bg_duoc_DUNG_that():
    """⛔ Mot token khai ma dung `0` lan la mot token ⛔ khong ton tai."""
    import io
    import pathlib
    css = (pathlib.Path(__file__).resolve().parents[2]
           / "fls" / "web" / "tep" / "hinh.css")
    assert "--evi-bg" in io.open(css, encoding="utf-8").read(), (
        "⛔ `--evi-bg` khai ở `tokens.css` mà ⛔ không dùng ở đâu")
```

⚠ Bài `test_DU_XUONG_…` cần DOM giả trả `scrollHeight`／`clientHeight`. Trước khi viết mã màn, thêm vào `tests/web/dom_gia.js` trong hàm `tao()`:

```js
      get scrollHeight() { return e._scrollHeight || 0; },
      get clientHeight() { return e._clientHeight || 0; },
```

Và bài `test_bam_DU_XUONG_…` chạm `_nghe.click[0]` — đường đã có sẵn *(`dom_gia.js:70`)*.

- [ ] **Bước 7 · Chạy để chắc nó ĐỎ**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_b3_bang_chung_va_du_xuong.py -q
```

Chờ: **7 ĐỎ**.

- [ ] **Bước 8 · Viết mã màn**

Trong `man_f01_ghep.js`, thêm cạnh `gon`:

```js
  const THOAT_HTML = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' };
  const thoat = t => String(t == null ? '' : t)
    .replace(/[&<>"]/g, c => THOAT_HTML[c]);

  /* ⭐⭐ To **bang chung** trong dien giai. Bo khoa do **tang doc** tinh
     (`man_ghep.khoa_bang_chung`) — bo tu rac la mot luat nghiep vu.
     ⛔⛔ **Thoat TRUOC, to SAU.** `dien_giai` la chu tu sao ke ngan hang,
        tuc chu ⛔ khong ai kiem soat; ghep thang vao `innerHTML` la mo mot
        duong chen the.
     ⭐ Quet **MOT luot** bang mot regex hop nhat — to lan luot tung khoa se
       sinh `<mark>` **long nhau** va HTML vo. */
  function danh_dau(chu, khoa) {
    const s = thoat(chu);
    if (!khoa || !khoa.length) return s;
    const mau = khoa.map(k => String(k).replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
    return s.replace(new RegExp('(' + mau.join('|') + ')', 'gi'), '<mark>$&</mark>');
  }

  /* ⭐⭐⭐ Chi moi `đủ ↓` khi dien giai **THAT SU bi cat** — do `scrollHeight`
     **sau khi da dan trang**, ⛔ khong doan theo so ky tu: be rong cot doi
     theo man, nen mot nguong ky tu se vua sai ca hai chieu.
     ⛔ Mot loi moi hien ra khi ⛔ khong co gi de mo la mot loi moi day nguoi
       ta **thoi tin moi loi moi**. */
  function soat_cat() {
    const ds = document.querySelectorAll('.cand');
    for (let i = 0; i < ds.length; i++) {
      const dg = ds[i].querySelector('.dg');
      const nut = ds[i].querySelector('.mo');
      if (!dg || !nut) continue;
      if (dg.className.indexOf('clamp') < 0) { nut.style.display = 'inline-block'; continue; }
      nut.style.display = dg.scrollHeight > dg.clientHeight + 1 ? 'inline-block' : 'none';
    }
  }
```

Trong `ve_ung_vien`, thay khối dựng diễn giải:

```js
    let chu, lop;
    if (uv.dien_giai) { chu = gon(uv.dien_giai); lop = 'dg'; }
    else if (uv.dien_giai_vi_sao === 'chua_noi_duoc') {
      chu = '⛔ chưa đọc được nội dung — cột này chưa nối được với sổ';
      lop = 'dg chua_doc';
    } else { chu = '— giao dịch này không có nội dung'; lop = 'dg trong'; }
    const mo_rong = ST.dg_mo === i;
    const boc = TP.el('div', 'dgw');
    const dg = TP.el('div', lop + (mo_rong ? '' : ' clamp'));
    dg.innerHTML = uv.dien_giai ? danh_dau(chu, uv.khoa_to) : thoat(chu);
    dg.setAttribute('title', chu);
    boc.appendChild(dg);
    /* ⛔⛔⛔ `span`, ⛔ **KHONG** `button`: `.cand` DA la mot `<button>`, va
       **nut long nut la HTML ⛔ khong hop le** — trinh duyet that ⛔ khong xu
       ly duoc nut trong. ⚠ DOM gia thi cho chay ngon lanh, nen cho nay
       **⛔ khong the** do bang mot bai chay; no duoc do bang
       `test_KHONG_co_NUT_nao_nam_TRONG_mot_NUT`.
       ⭐ `role` ＋ `tabindex` giu lai phan tro nang ma the `button` von cho. */
    const nut_mo = o('span', 'mo', mo_rong ? 'thu gọn ↑' : 'đủ ↓');
    nut_mo.setAttribute('role', 'button');
    nut_mo.setAttribute('tabindex', '0');
    nut_mo.dataset.mo = String(i);
    boc.appendChild(nut_mo);
    r.appendChild(boc);
```

Trong `ve_ung_vien`, **sửa listener click của dòng** — thêm khối này làm **việc đầu tiên** trong thân `r.addEventListener('click', …)`, và đổi `() =>` thành `e =>`:

```js
    if (!chi_doc) r.addEventListener('click', e => {
      /* ⭐ Một cú bấm vào `đủ ↓` là một cú bấm vào **nút ngoài** — ủy quyền
         qua `closest`, đúng khuôn bản dựng. ⛔ Bấm mở/thu gọn **⛔ không**
         được kéo theo đổi ứng viên đang chọn. */
      if (e && e.target && e.target.closest && e.target.closest('[data-mo]')) {
        ST.dg_mo = ST.dg_mo === i ? null : i;
        ve();
        return;
      }
      ST.ung_vien_chon = chon ? null : i;
      ST.xac_nhan = false;
      ve();
    });
```

Trong `ST`, thêm `dg_mo: null,`. Trong `ve_ung_vien`, dòng dựng `r` thêm lớp `rong` khi mở:

```js
    const r = TP.el(chi_doc ? 'div' : 'button',
                    'cand' + (chon ? ' chon' : '') + (b.m ? ' ' + b.m : '')
                    + (ST.dg_mo === i ? ' rong' : ''));
```

Cuối `ve()`, ngay trước `goc.appendChild(than);`, thêm:

```js
    soat_cat();   /* ⭐ do SAU khi da dan trang */
```

Thêm `danh_dau`, `soat_cat` vào khối `return {…}`.

- [ ] **Bước 9 · Viết kiểu**

Trong `fls/web/tep/hinh.css`, thêm vào khối `SCR-F01`:

```css
/* ── ⭐⭐⭐ Dien giai: kep MOT dong ＋ loi mo `đủ ↓` ────────────────────── */
.cand .dgw{min-width:0;display:flex;align-items:baseline;gap:6px}
/* ⭐ `-webkit-line-clamp` chu ⛔ KHONG `nowrap`: khi mo rong, dong phai cao
   them va chu phai xuong hang — `nowrap` thi ⛔ khong bao gio xuong. */
.cand .dg.clamp{display:-webkit-box;-webkit-line-clamp:1;-webkit-box-orient:vertical;
  overflow:hidden}
/* ⭐ `span`, ⛔ KHONG `button` — xem ghi chu o `ve_ung_vien`. */
.cand .mo{flex:none;cursor:pointer;font:600 10.5px/1 var(--sans);
  color:var(--accent);padding:1px 3px;white-space:nowrap}
.cand .mo:hover{color:var(--accent-hi);text-decoration:underline}
.cand .mo:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
/* ⭐ Cao **36px co dinh**, **mo rong moi cao them** — hop dong `C3`. */
.cand.rong{height:auto;min-height:var(--row-ghep);padding-top:6px;padding-bottom:6px}
.cand.rong .dgw{align-items:flex-start}

/* ── ⭐⭐ BANG CHUNG duoc danh dau ──────────────────────────────────────── */
/* ⛔ To **ba** thu va chi ba: so CT khi trung dung · so tien khi khop tuyet
   doi · ten vendor sau khi loc tu rac. To rong hon thi mau **thoi mang
   nghia**, va cot nay la bang chung duy nhat cua **49%** cuon so. */
.cand mark{background:var(--evi-bg);color:inherit;font-weight:600;
  border-radius:2px;padding:0 1px}
```

- [ ] **Bước 10 · Chạy để chắc nó XANH**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_b3_bang_chung_va_du_xuong.py tests/repo/test_b1_khoa_bang_chung.py -q
```

Chờ: **12 XANH**.

- [ ] **Bước 11 · Diễn tập phá**

Đổi `nut.style.display = dg.scrollHeight > …` thành `nut.style.display = 'inline-block';` — chờ `test_DU_XUONG_…` **ĐỎ**. Khôi phục.

- [ ] **Bước 12 · Cả bộ ＋ cổng** *(thêm `tools/soi_bang_tuyen.py` vì đã sửa `xu_ly.py`)*

Chờ `1.830` xanh · bảng tuyến `39/39`.

- [ ] **Bước 13 · Commit**

```bash
git add tests/ fls/ docs/
git commit -F- <<'EOF'
feat(ghep): tra lai hai lop bao ve cho cot Dien giai

Hop dong §6.2 viet thang: "khong dung tooltip lam loi duy nhat". Truoc ban
va nay tooltip LA loi duy nhat — white-space:nowrap + title, khong `du xuong`,
khong <mark>, va token --evi-bg khai o tokens.css roi dung 0 lan.

Dien giai la bang chung duy nhat cua 4.145/8.387 = 49% cuon so.

- khoa_bang_chung() o TANG DOC: bo tu rac la mot LUAT NGHIEP VU, khong phai
  meo hien thi; de o JS thi khong bai thu Python nao cham toi.
- so CT chi to khi TRUNG DUNG; so tien chi to khi khop TUYET DOI (ca so lan
  don vi tien); ten vendor sau khi loc 43 tu rac.
- khoa xep DAI TRUOC + quet MOT luot: to lan luot tung khoa sinh <mark>
  long nhau va HTML vo.
- THOAT truoc, TO sau: dien_giai la chu tu sao ke, tuc chu khong ai kiem
  soat; ghep thang vao innerHTML la mo mot duong chen the.
- `du xuong` do scrollHeight SAU khi dan trang, khong doan theo so ky tu:
  be rong cot doi theo man nen mot nguong ky tu sai ca hai chieu.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
git push origin feat/p2-oracle-parity
```

---

## Chặng 4 · Cửa lệnh ĐÃ GÁN — và `itl_id_da_gan` phải là **danh sách**

**Tệp:**
- Sửa: `fls/repo/lenh_cho.py` *(thêm `_SQL_LENH_DA_GAN`, `doc_lenh_da_gan`)*
- Sửa: `fls/repo/man_ghep.py` *(`khuon_the_lenh` sinh `itl_da_gan[]`)*
- Sửa: `fls/api/bang_tuyen.py` *(tuyến **40**)* · `fls/api/xu_ly.py` *(tay nắm)*
- Sửa: `fls/web/tep/man_f01_ghep.js` *(`CHIP_CUA.da_gan`, `bo_gan`)*
- Tạo: `tests/api/test_b2_cua_lenh_da_gan.py`

**Giao diện:**
- Sinh ra:
  - `lenh_cho.doc_lenh_da_gan(conn, pv, *, con_tro=None, limit=None) -> Trang`
  - `GET /api/fls/v1/queue/lenh-da-gan` → cùng khuôn hàng với `lenh-cho`, **thêm** `itl_da_gan: list[int]`
  - `khuon_the_lenh` sinh `itl_da_gan: list[int]` *(⛔ **không** `itl_id_da_gan` số ít)*

### ⛔⛔⛔ Một số **⛔ không đủ chỗ** — đo được

`bo_gan()` đọc `lenh.itl_id_da_gan` *(số ít)*. Đo `22/09` trên kho thật:

| Đếm | Con số |
|---|---|
| Lệnh chi **đã gán** | **2.219** |
| Lệnh chi **chưa gán** | **1.553** |
| ⭐ Lệnh chi gắn **nhiều hơn một** dòng tiền | **23** = **1,0%** |

⇒ Một khoá số ít sẽ **im lặng bỏ mất** mối nối thứ hai ở **23** lệnh. ⭐ Và **1,0%** đúng bằng bậc độ lớn của `1,1%` ca có chùm — cùng một sự thật *(tiền và lệnh là quan hệ **nhiều ↔ nhiều**)* nhìn từ hai phía. ⇒ Trường phải là **danh sách**, và màn phải **hỏi bỏ cái nào** khi có nhiều hơn một.

- [ ] **Bước 1 · Viết bài thử ĐỎ**

Tạo `tests/api/test_b2_cua_lenh_da_gan.py`:

```python
# -*- coding: utf-8 -*-
"""`B2` — ⭐⭐ Cua lenh chi **DA GAN** (tuyen 40) — `GAP-API-08`.

⛔⛔ `/queue/lenh-cho` loc cung `NOT EXISTS (fls_moi_noi)` ⇒ no **chi** tra
   dong **chua noi**. Suot chang `B3`, `khuon_the_lenh` doc `r["da_gan"]` ma
   ⛔ khong cua nao sinh khoa ay ⇒ `trang_thai` **vinh vien** `'chua_gan'`,
   va ca nua *"da gan"* cua man chet theo day chuyen: nhan *"Doi sang giao
   dich da chon"* ⛔ khong bao gio hien, nut *"Bo gan"* ⛔ khong bao gio bat,
   `.mrow.da_gan` la CSS chet, `lenh_ke_tiep` ⛔ khong bo qua duoc dong nao.

⭐⭐⭐ Va `itl_id_da_gan` **so it** la SAI: do `22/09` tren kho that,
   **23/2.219 = 1,0%** lenh chi gan **nhieu hon mot** dong tien.
"""
from __future__ import annotations

import pytest

from fls.repo import lenh_cho as lc
from fls.repo import man_ghep as mg


def test_khuon_the_sinh_DANH_SACH_chu_KHONG_mot_so():
    r = {"pm_line_id": "PM1-1", "amount": "40.00", "curr": "EUR",
         "cdt1": "COR | X", "ref_tho": None, "tho": {},
         "itl_da_gan": [42, 77]}
    t = mg.khuon_the_lenh(r)
    assert t["itl_da_gan"] == [42, 77], (
        "⛔⛔ Mot khoa SO IT bo mat moi noi thu hai o **23** lenh chi")
    assert t["trang_thai"] == "da_gan"
    assert "itl_id_da_gan" not in t, (
        "⛔ ten so it phai bien mat han — giu ca hai la giu hai ban su that")


def test_chua_gan_thi_danh_sach_RONG_chu_KHONG_thieu_khoa():
    """⭐ `[]` la mot **cau tra loi** *(⛔ chua gan gi)*; thieu khoa la
    *"FLS ⛔ khong biet"*. Hai cau khac nhau — `INV-I16`."""
    t = mg.khuon_the_lenh({"pm_line_id": "PM1-1", "tho": {}})
    assert t["itl_da_gan"] == [] and t["trang_thai"] == "chua_gan"


@pytest.mark.pg
def test_cua_tra_dung_SO_LENH_DA_GAN(conn_pg, pv_that):
    """⛔ Do tren kho THAT: **2.219** da gan ＋ **1.553** chua gan = **3.772**."""
    t = lc.doc_lenh_da_gan(conn_pg, pv_that, limit=500)
    assert t.dong, "⛔ cua tra **0** dong — kho co 2.219 lenh da gan"
    for d in t.dong[:20]:
        assert d["itl_da_gan"], f"⛔ {d['pm_line_id']} trong ro DA GAN ma rong"


@pytest.mark.pg
def test_HAI_ro_KHONG_giao_nhau_va_KHEP_ve_tong(conn_pg, pv_that):
    """⛔⛔ Hai ro chong nhau thi mot dong hien **hai lan** o chip `Tat ca`,
    va **khong ai cong duoc**."""
    da = set()
    ct = None
    while True:
        t = lc.doc_lenh_da_gan(conn_pg, pv_that, con_tro=ct, limit=500)
        da |= {d["pm_line_id"] for d in t.dong}
        ct = t.con_tro
        if not ct:
            break
    chua = set()
    ct = None
    while True:
        t = lc.doc_lenh_cho(conn_pg, pv_that, con_tro=ct, limit=500)
        chua |= {d["pm_line_id"] for d in t.dong}
        ct = t.con_tro
        if not ct:
            break
    assert not (da & chua), f"⛔⛔ **{len(da & chua)}** dong nam o CA HAI ro"
    assert len(da) == 2219, len(da)
    assert len(chua) == 1553, len(chua)


@pytest.mark.pg
def test_co_lenh_gan_NHIEU_dong_tien_va_cua_tra_DU(conn_pg, pv_that):
    """⭐ **23** lenh — day la ly do khoa phai la danh sach."""
    nhieu = 0
    ct = None
    while True:
        t = lc.doc_lenh_da_gan(conn_pg, pv_that, con_tro=ct, limit=500)
        nhieu += sum(1 for d in t.dong if len(d["itl_da_gan"]) > 1)
        ct = t.con_tro
        if not ct:
            break
    assert nhieu == 23, f"⛔ do duoc **{nhieu}** lenh gan nhieu dong tien, cho 23"
```

⚠ Đọc một bài `@pytest.mark.pg` sẵn có *(ví dụ `tests/repo/test_b1_chum_moi_noi_pg.py`)* để lấy **đúng tên** các fixture kết nối／phạm vi; thay `conn_pg`／`pv_that` cho khớp.

- [ ] **Bước 2 · Chạy để chắc nó ĐỎ**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/api/test_b2_cua_lenh_da_gan.py -q
```

Chờ: **5 ĐỎ**.

- [ ] **Bước 3 · Viết câu SQL ＋ hàm đọc**

Trong `fls/repo/lenh_cho.py`, thêm sau `_SQL_LENH_CHO`:

```python
# ⭐⭐ Ro **DA GAN** — bu cua `_CTE_LENH_CHO`, va hai ro phai **KHEP ve tong**:
#    2.219 ＋ 1.553 = 3.772 (do 22/09). Hai ro chong nhau thi mot dong hien
#    hai lan o chip `Tat ca` va ⛔ khong ai cong duoc.
#
# ⛔ `fls_moi_noi`, ⛔ KHONG `fls_pm_link` — cung ly do da ghi o `_COT_LENH`:
#   bang goc con giu ca moi noi DA BO.
#
# ⭐ `array_agg` chu ⛔ KHONG `min(itl_id)`: **23/2.219 = 1,0%** lenh gan
#   **nhieu hon mot** dong tien, va mot con so se **im lang bo mat** phan con
#   lai — dung o cho nguoi ta bam `Bo gan`.
_SQL_LENH_DA_GAN = """
SELECT {cot}, COALESCE(l.amount, 0) AS tien,
       (SELECT array_agg(DISTINCT m.itl_id ORDER BY m.itl_id)
          FROM fls_moi_noi m WHERE m.pm_line_id = l.pm_line_id) AS itl_da_gan
  FROM fls_pm_line l
 WHERE l.run_id = %(run_pm)s
   AND EXISTS (SELECT 1 FROM fls_moi_noi m WHERE m.pm_line_id = l.pm_line_id)
   {them}
 ORDER BY l.pm_line_id
 LIMIT %(n)s"""


def doc_lenh_da_gan(conn, pv: PhamVi, *, con_tro: str | None = None,
                    limit: int | None = None) -> Trang:
    """Dong lenh chi **DA tim duoc tien** — `GAP-API-08`.

    ⛔⛔ **Vi sao mot tuyen RIENG chu ⛔ khong mot co tren `/queue/lenh-cho`.**
       Ten `lenh-cho` co nghia *"dang cho"*; cho no tra dong da noi la de mot
       cai ten **noi doi**, va moi nguoi doc ma sau nay se tin cai ten.

    ⭐ Con tro la `pm_line_id` — khoa DON, vi thu tu o day la `(pm_line_id)`.
      ⚠ ⛔ Khong dung `(curr, hang)` nhu `doc_lenh_cho`: ro nay ⛔ khong co
        thu hang theo tien *(no ⛔ khong phai mot hang doi viec)*.
    """
    n = _trang(limit)
    ts: dict[str, Any] = {"run_pm": anh_pm_hieu_luc(conn, pv), "n": n + 1}
    them: list[str] = []
    if con_tro:
        them.append("AND l.pm_line_id > %(ct)s")
        ts["ct"] = con_tro
    sql = _SQL_LENH_DA_GAN.format(cot=", ".join(_COT_LENH),
                                  them=" ".join(them))
    with conn.cursor() as cur:
        cur.execute(sql, ts)
        dong = _dong(cur)
    con = dong[n - 1]["pm_line_id"] if len(dong) > n else None
    return Trang(dong=dong[:n], con_tro=con, pham_vi=pv.mo_ta())
```

- [ ] **Bước 4 · Sửa khuôn thẻ**

Trong `fls/repo/man_ghep.py`, hàm `khuon_the_lenh`, thay hai dòng:

```python
    da = list(r.get("itl_da_gan") or [])
```

và trong khối trả về:

```python
        "trang_thai": "da_gan" if da else "chua_gan",
        "trang_thai_nhan": "Đã gán" if da else "Chưa gán",
        "trang_thai_mau": "ok" if da else "",
        ...
        # ⭐⭐ **DANH SACH**, ⛔ khong mot so: **23/2.219 = 1,0%** lenh chi gan
        #   **nhieu hon mot** dong tien. Mot khoa so it se **im lang bo mat**
        #   moi noi thu hai — dung o cho nguoi ta bam `Bo gan`.
        # ⭐ `[]` la mot **cau tra loi** (*⛔ chua gan gi*); thieu khoa la
        #   *"FLS ⛔ khong biet"*. Hai cau khac nhau — `INV-I16`.
        "itl_da_gan": da,
```

Xoá dòng cũ `da_gan = bool(r.get("da_gan"))`.

- [ ] **Bước 5 · Khai tuyến 40**

Trong `fls/api/bang_tuyen.py`, ngay sau tuyến `lenh_cho_tom`:

```python
    # ⭐⭐ `GAP-API-08` — tuyen 40. Truoc no, **2/4** chip cua man ghep
    #    ⛔ khong goi duoc: `/queue/lenh-cho` loc cung `NOT EXISTS
    #    (fls_moi_noi)` nen ⛔ khong duong nao hoi *"lenh nao DA co tien"*.
    Tuyen("GET", f"{TIEN_TO}/queue/lenh-da-gan", "lenh_da_gan",
          ("fls_pm_line", "fls_moi_noi"),
          mo_ta="dong lenh chi **DA** tim duoc tien, kem `itl_da_gan[]` — "
                "⭐ MOT DANH SACH: 23/2.219 = 1,0% lenh gan NHIEU HON MOT "
                "dong tien. Bu cua `/queue/lenh-cho`; hai ro KHEP ve tong "
                "2.219 + 1.553 = 3.772"),
```

Trong `fls/api/xu_ly.py`:

```python
def lenh_da_gan(yc: YeuCau):
    """Dong lenh chi **DA** tim duoc tien — bu cua `/queue/lenh-cho`."""
    try:
        t = lc.doc_lenh_da_gan(
            yc.conn, yc.pv,
            con_tro=yc.q.get("cursor") or None,
            limit=_so_nguyen(yc.q, "limit"))
    except ValueError as e:
        raise LoiCua("FLS-BAD-REQUEST", str(e)) from e
    for d in t.dong:
        d["the"] = mg.khuon_the_lenh(d)
    return _trang_ra(t), "flash"
```

Và đăng ký trong khối `HAM.update({...})`: `"lenh_da_gan": lenh_da_gan,`.

⚠ Cập nhật con số tuyến **39 → 40** ở mọi nơi cổng số sống đang canh — chạy `tools/dong_bo_so_song.py --ghi` sẽ lo phần tài liệu; bài `tests/api/test_cua_lenh_cho_pg.py` có một **dây bẫy cố ý** đếm tuyến, phải sửa tay kèm lý do.

- [ ] **Bước 6 · Nối màn**

Trong `man_f01_ghep.js`, sửa `CHIP_CUA`:

```js
  const CHIP_CUA = {
    chua_gan: ['ro=nguoi', 'ro=may&tu_chung=0'],
    khong_gan_duoc: ['ro=khong'],
    da_gan: ['@da-gan'],     /* ⭐ tuyen 40 — xem `_duong()` */
    tat_ca: null,            /* ⛔ van chua co: no la HOP cua hai ro */
  };
```

Thêm cạnh `tai_danh_sach`:

```js
  /* ⭐ Hai ro nam o **hai tuyen**, nen mot chuoi truy van ⛔ khong du de goi
     ten duong. `@da-gan` la mot nhan, ⛔ khong phai mot bo loc. */
  function _duong(loc, con_tro) {
    const d = loc === '@da-gan' ? '/queue/lenh-da-gan?' : '/queue/lenh-cho?' + loc + '&';
    return d + 'limit=' + TRANG
         + (con_tro ? '&cursor=' + encodeURIComponent(con_tro) : '');
  }
```

Trong vòng lặp của `tai_danh_sach`, thay dòng dựng `q` bằng `const q = _duong(loc, con_tro);` và `FLS.doc(q)`.

Sửa `bo_gan` để xử lý **danh sách**:

```js
  async function bo_gan(lenh) {
    /* ⭐⭐ **DANH SACH**, ⛔ khong mot so — `23/2.219 = 1,0%` lenh chi gan
       nhieu hon mot dong tien. Ban truoc doc `lenh.itl_id_da_gan` *(so it)*,
       mot khoa **⛔ khong ai sinh ra**, nen URL thanh `/queue/undefined/chum`. */
    const ds = lenh.itl_da_gan || [];
    if (!ds.length) return;
    let itl = ds[0];
    if (ds.length > 1) {
      /* ⛔ Bo dai mot cai la doan thay nguoi. */
      const ok = await HT.hoi(
        'Lệnh này đang gắn ' + ds.length + ' giao dịch',
        'FLS ⛔ không tự chọn hộ. Hãy bỏ gán từ màn Sổ ITL, nơi xem được '
        + 'từng giao dịch.', 'Đã hiểu');
      return;
    }
    const chum = (await FLS.doc('/queue/' + itl + '/chum')).data || {};
    ...
```

*(phần còn lại của `bo_gan` giữ nguyên)*

- [ ] **Bước 7 · Chạy để chắc nó XANH**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/api/test_b2_cua_lenh_da_gan.py -q
```

Chờ: **5 XANH**.

- [ ] **Bước 8 · Cả bộ ＋ cổng** *(bắt buộc có `tools/soi_bang_tuyen.py` — tuyến mới)*

Chờ `1.835` xanh · bảng tuyến **`40/40`** khớp SQL · import-linter `9/9`.

- [ ] **Bước 9 · Commit**

```bash
git add tests/ fls/ docs/
git commit -F- <<'EOF'
feat(cua): tuyen 40 lenh-da-gan — va itl_da_gan phai la DANH SACH

GAP-API-08. /queue/lenh-cho loc cung NOT EXISTS (fls_moi_noi) nen khong
duong nao hoi "lenh chi nao DA co tien". Suot chang B3, khuon_the_lenh doc
r["da_gan"] ma khong cua nao sinh khoa ay => trang_thai vinh vien
'chua_gan', va ca nua "da gan" cua man chet theo day chuyen.

Do 22/09 tren kho that: 2.219 da gan + 1.553 chua gan = 3.772, va 23 lenh
chi (1,0%) gan NHIEU HON MOT dong tien. => itl_id_da_gan so it la SAI: no
im lang bo mat moi noi thu hai, dung o cho nguoi ta bam Bo gan. Truong
thanh itl_da_gan[] va man HOI thay vi doan khi co nhieu hon mot.

1,0% dung bang bac do lon cua 1,1% ca co chum — cung mot su that (tien va
lenh la quan he nhieu<->nhieu) nhin tu hai phia.

Mot tuyen RIENG chu khong mot co tren lenh-cho: ten "lenh-cho" nghia la
"dang cho"; cho no tra dong da noi la de mot cai ten noi doi.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
git push origin feat/p2-oracle-parity
```

---

## Chặng 5 · Cổng tổng quát ＋ đồng bộ tài liệu

**Tệp:**
- Tạo: `tests/web/test_moi_o_nhap_deu_co_nguoi_nghe.py`
- Sửa: `docs/ITL/02_BA/06_SCREEN_SPEC.md` · `07_API_CONTRACT.md` · `13_THUYET_MINH_MAN_HINH.md` · `docs/ITL/01_Orchestrator/06_ORCHESTRATOR_DASHBOARD.md` · `Artifacts/Plan-Test-Dev-Man-Ghep.md`

⭐⭐⭐ Bốn chặng trên vá **bốn ca cụ thể**. Chặng này vá **lớp lỗi**: *"một thứ có trong vỏ mà ⛔ không ai nối"*.

- [ ] **Bước 1 · Viết cổng**

Tạo `tests/web/test_moi_o_nhap_deu_co_nguoi_nghe.py`:

```python
# -*- coding: utf-8 -*-
"""⛔ Cong: moi O NHAP trong vo deu phai co **nguoi nghe**.

⛔⛔⛔ **Bon lo cung mot hinh dang trong ba ngay**, va ⛔ khong cong nao bat:

  ① `ST.dong` — ⛔ khong ai goi cua nap danh sach *(khuon thu tu nhet vao)*
  ② `F01G.phim` — 9 phim viet du, ⛔ khong ai dang ky `keydown`
  ③ `#ghep-tim` — o nhap co trong vo, ⛔ khong ai nghe `input`
  ④ `itl_id_da_gan` — doc mot khoa ⛔ khong ai sinh

⭐⭐ Goc chung: **bai thu voi tay VAO goi thu ma san pham phai voi tay RA
   noi.** Cong nay do chieu con lai — mot phan tu **ton tai trong vo** thi
   phai co it nhat **mot** doan ma cham toi no.

⛔ Cong nay **⛔ khong** thay duoc cong CHAY *(no van la mot phep quet chu)*.
  No la **luoi thua**: bat cho **quen han**, con cho *"noi nhung noi sai"*
  thi phai la mot bai chay — nhu `test_b3_ban_phim_noi_that.py`.
"""
from __future__ import annotations

import io
import os
import re

from fls.web import phuc_vu as pv

VO = os.path.join(pv.THU_MUC, "index.html")

#: ⭐ Chi soi the NHAN TUONG TAC. Mot `<div id=…>` la mot cai neo de ve vao,
#: ⛔ khong phai mot thu doi phan ung.
THE_TUONG_TAC = re.compile(
    r"<(input|select|textarea)\b[^>]*\bid=[\"']([^\"']+)[\"']", re.I)

#: ⭐ Ban TRANG. Them mot ten vao day la khai *"o nay CO Y ⛔ khong ai nghe"*,
#: va no phai co ly do viet ngay canh.
MIEN_TRU: dict[str, str] = {}


def _js() -> str:
    ra = []
    for ten in sorted(os.listdir(pv.THU_MUC)):
        if ten.endswith(".js"):
            ra.append(io.open(os.path.join(pv.THU_MUC, ten),
                              encoding="utf-8").read())
    return "\n".join(ra)


def test_moi_o_nhap_trong_vo_deu_co_ma_cham_toi():
    chu = io.open(VO, encoding="utf-8").read()
    js = _js()
    mo_coi = []
    for _, ma in THE_TUONG_TAC.findall(chu):
        if ma in MIEN_TRU:
            continue
        if ma not in js:
            mo_coi.append(ma)
    assert mo_coi == [], (
        "⛔⛔ O nhap co trong vo ma ⛔ KHONG mot dong JS nao cham toi — no se "
        "hien ra, go duoc, va ⛔ khong lam gi:\n  " + "\n  ".join(mo_coi))


def test_o_nhap_KHONG_duoc_chi_duoc_FOCUS_ma_KHONG_duoc_NGHE():
    """⛔⛔ Dung lo cua `#ghep-tim`: no duoc `focus()` boi `/` va **⛔ khong ai
    nghe** ⇒ nhay vao duoc, go duoc, va ⛔ khong gi xay ra. Mot o nhap chi
    duoc nhay vao ma ⛔ khong duoc doc **te hon** mot o ⛔ khong co: no **moi**
    nguoi ta go."""
    chu = io.open(VO, encoding="utf-8").read()
    js = _js()
    xau = []
    for _, ma in THE_TUONG_TAC.findall(chu):
        if ma in MIEN_TRU or ma not in js:
            continue
        # ⭐ Co ai nghe `input`/`change`/`keydown`, hay doc `.value` cua no?
        gan = re.search(
            r"['\"]#?" + re.escape(ma) + r"['\"][\s\S]{0,600}?"
            r"(addEventListener\s*\(\s*['\"](?:input|change|keydown|keyup)|"
            r"\.oninput|\.onchange|\.value\b)", js)
        if not gan:
            xau.append(ma)
    assert xau == [], (
        "⛔ O nhap ⛔ khong ai NGHE va ⛔ khong ai DOC gia tri:\n  "
        + "\n  ".join(xau))


# ── ⛔⛔ PHA CO CHU DICH ───────────────────────────────────────────────────

def test_cong_DO_khi_mot_o_nhap_mo_coi():
    gia_vo = '<input id="o-khong-ai-nghe" placeholder="x">'
    assert THE_TUONG_TAC.findall(gia_vo) == [("input", "o-khong-ai-nghe")]
    assert "o-khong-ai-nghe" not in _js()
```

- [ ] **Bước 2 · Chạy**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest tests/web/test_moi_o_nhap_deu_co_nguoi_nghe.py -q
```

Chờ: **3 XANH** *(vì Chặng 2 đã vá `#ghep-tim`)*. ⚠ Nếu **ĐỎ** ⇒ còn ô nhập mồ côi khác — sửa nó hoặc ghi vào `MIEN_TRU` **kèm lý do**, ⛔ không im lặng bỏ qua.

- [ ] **Bước 3 · Diễn tập phá**

Tạm thêm `<input id="o-thu-pha">` vào `fls/web/tep/index.html`, chạy lại — chờ **1 ĐỎ** chỉ đúng tên ấy. Gỡ ra.

- [ ] **Bước 4 · Đồng bộ tài liệu**

| Tệp | Sửa gì |
|---|---|
| `06_SCREEN_SPEC.md` | bump **v4.2**; `§4.5` thêm `ⓜ` — *bốn lỗi CHẶN và vì sao ba cổng đều xanh*; `§4.6` đánh dấu `đủ ↓` ＋ `<mark>` đã làm |
| `07_API_CONTRACT.md` | bump **v3.2**; khai tuyến **40** `/queue/lenh-da-gan` ＋ `itl_da_gan[]` *(danh sách — 23/2.219)* ＋ trường thứ **11** `khoa_to` của `ung_vien[]`; ghi `GAP-API-08` **ĐÓNG một nửa** *(chip `Tất cả` vẫn chưa có — nó là **hợp** của hai rổ)* |
| `13_THUYET_MINH_MAN_HINH.md` | `§A8` thêm: nút `đủ ↓`／`thu gọn ↑`, ô tìm bật Toàn sổ, hộp thoại *"lệnh gắn N giao dịch"* |
| `06_ORCHESTRATOR_DASHBOARD.md` | `GAP-API-08` → **ĐÓNG một nửa**; mở **`GAP-SCR-26`** *(chip `Tất cả` chưa có cửa)*; ghi lớp lỗi *"có trong vỏ mà ⛔ không ai nối"* ＋ cổng mới |
| `Artifacts/Plan-Test-Dev-Man-Ghep.md` | thêm `§6d` — kết quả kiểm độc lập ＋ bốn chặng vá |

⚠ **`K1`**: mọi bump version phải sửa **cả** dòng header **và** thêm mục changelog — cổng canh cả hai.

- [ ] **Bước 5 · Cổng cuối**

```bash
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m pytest -q
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/dong_bo_so_song.py --ghi
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/kiem_so_song.py
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe docs/ITL/_tools/kiem_tai_lieu.py
PYTHONIOENCODING=utf-8 ./.venv/Scripts/python.exe docs/ITL/_tools/khop_owner.py
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/soi_bang_tuyen.py
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/kiem_thuyet_minh.py
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe tools/sinh_ban_do_tang.py --kiem
PYTHONIOENCODING=utf-8 PYTHONPATH=. ./.venv/Scripts/python.exe -m importlinter.cli lint
```

Chờ: `~1.838` xanh · số sống `109/109` · tài liệu `6/6` · tuyến `40/40` · thuyết minh đủ · import-linter `9/9`.

- [ ] **Bước 6 · Mở máy thật và tự xem**

```bash
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 PYTHONPATH=. FLS_JWT_SECRET=$(./.venv/Scripts/python.exe -c 'import base64,os;print(base64.b64encode(os.urandom(48)).decode())') ./.venv/Scripts/python.exe tools/chay_cua.py --cho-web --cho-ghi --actor dungtt1@apero.vn
```

Mở `http://127.0.0.1:8088/` → tab **②b Gán lệnh chi**. Kiểm tay: `↓` di chuyển · `→` mở · gõ `/` rồi gõ chữ ⇒ Toàn sổ · `đủ ↓` chỉ hiện ở dòng bị cắt · số CT trùng được tô.

⚠ **`NFR-I10` vẫn CHƯA ĐO** cho tới khi một **người thật** *(kế toán)* mở nó. Một lần tôi tự xem ⛔ không phải một lần nghiệm thu.

- [ ] **Bước 7 · Commit**

```bash
git add tests/ docs/ fls/
git commit -F- <<'EOF'
test(ghep): cong canh lop loi "co trong vo ma khong ai noi" + dong bo tai lieu

Bon lo cung mot hinh dang trong ba ngay, khong cong nao bat:
  (1) ST.dong    — khong ai goi cua nap danh sach
  (2) F01G.phim  — 9 phim viet du, khong ai dang ky keydown
  (3) #ghep-tim  — o nhap co trong vo, khong ai nghe input
  (4) itl_id_da_gan — doc mot khoa khong ai sinh

Goc chung: bai thu voi tay VAO goi thu ma san pham phai voi tay RA noi.
Cong moi do chieu con lai — mot phan tu ton tai trong vo thi phai co it
nhat mot doan ma cham toi no, va o NHAP thi phai co ai NGHE hoac DOC gia
tri cua no. Mot o nhap chi duoc nhay vao ma khong duoc doc te hon mot o
khong co: no MOI nguoi ta go.

Cong nay khong thay duoc cong CHAY (no van la phep quet chu). No la luoi
thua: bat cho QUEN HAN; cho "noi nhung noi sai" phai la mot bai chay.

Co-Authored-By: Claude Opus 5 (1M context) <noreply@anthropic.com>
EOF
git push origin feat/p2-oracle-parity
```

---

## Ngoài phạm vi plan này — ⛔ nói thẳng

Kiểm độc lập tìm **`14` mục ĐÁNG SỬA** ＋ **`4` NHẸ**. Plan này vá **`4` mục CHẶN**. Còn lại, xếp theo mức:

| Còn nợ | Vì sao ⛔ chưa vào plan |
|---|---|
| `C4` khối `.mblock` *(lệnh đã gán đang gắn giao dịch nào)* | Cần tuyến **40** *(Chặng 4)* xong trước; là một component mới, ⛔ không phải một mối nối thiếu |
| Nền tối *(`data-theme` ＋ `prefers-color-scheme`)* | Chạm **cả 5 màn**; `GAP-NFR-01` đòi **đo tương phản** trước |
| Chip `Tất cả` | Là **hợp** của hai rổ ⇒ cần quyết *(gọi hai cửa rồi trộn, hay mở tuyến thứ ba)* — `GAP-SCR-26` |
| Số đếm trên chip · dải số việc `3` con số · rail `6` mục | Đều là *"thêm trường"*, ⛔ không phải *"sửa lỗi"* |
| Bảng sổ `12` cột khi chưa mở lệnh | Đổi bố cục gốc; dính `GAP-SCR-24` |
| `.cands` tự cuộn | Dính `GAP-SCR-24` — quyết một lần cho cả vỏ |
| `aria-current` mang **hai** nghĩa | ⛔ Không chặn, nhưng là một lỗi trợ năng thật — gộp vào lượt `GAP-NFR-01` |

---

## Tự soát

**Phủ đặc tả:** `§6.2` *(`đủ ↓` ＋ `scrollHeight`)* → Chặng 3 · `§6` *(`<mark>` ＋ từ rác)* → Chặng 3 · `§7` *(bàn phím)* → Chặng 1 · `§8` *(Toàn sổ bật tay)* → Chặng 2 · `C4`／`C5`／`C6`／`C9`／nền tối → **⛔ không có chặng**, đã ghi rõ ở *"Ngoài phạm vi"*.

**Nhất quán kiểu:** `khoa_bang_chung(lenh, uv) -> list[str]` *(Chặng 3)* → cửa gắn `u["khoa_to"]` → JS đọc `uv.khoa_to` ✔. `itl_da_gan: list[int]` dùng **cùng một tên** ở `lenh_cho.py` → `khuon_the_lenh` → `bo_gan` ✔; tên số ít `itl_id_da_gan` **bị xoá hẳn**, có bài thử canh ✔. `soat_cat()` gọi trong `ve()` và trong bài thử cùng tên ✔.

**⚠ Hai chỗ người thực thi PHẢI tự đọc mã trước khi gõ** *(⛔ tôi không đoán hộ)*: tên fixture `@pytest.mark.pg` *(Chặng 4 bước 1)*, và tên biến trong `xu_ly.py::ung_vien_tien` *(Chặng 3 bước 5)*.
