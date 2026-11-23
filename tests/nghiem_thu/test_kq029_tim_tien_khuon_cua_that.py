# -*- coding: utf-8 -*-
"""`KQ-029` *(kiểm `BG-027` + `BG-028` — `WO-022`)* · hộp **"Tìm tiền"** `F01L`
nuôi bằng **thân CỬA THẬT** `GET /queue/lenh/{id}/itl-candidates`.

⛔⛔ **Phát hiện `F-1`** *(đo Chrome thật máy `8099`, kho TEST, tích chuột thật
02/10)*: hộp *Tìm tiền* in cột `Tiền` **`—`**, cột `Lệch` **`—`**, và câu
*"lệch ⛔ không tính được ⇒ ⛔ VƯỢT dung sai — cửa ghi sẽ TỪ CHỐI"* cho **MỌI**
ứng viên — kể cả ứng viên bậc `tiền khớp` *(đúng từng đồng)*. Gốc: cửa đã nắn
về **khuôn `⓵`** của `BA-07 §4h` từ `23/09` *(`GAP-API-10`: `amount` · `lech`
· `dien_giai` …)*, còn `man_f01_lenh.js::_drawer_tim_tien` vẫn đọc **khoá hàng
thô** `u.tien` · `u.lech_tuyet_doi` · `u.memo`. Đo khoá thật trả về *(8088 sổ
thật + 8099 kho TEST)*: `itl_id · doc_date · doc_no · dien_giai · amount ·
chieu · curr · nguon · bac · lech · khoa_to` — ⛔ có `tien`.

⛔⛔ **Vì sao bộ bài `WO-022` xanh mà màn sai.** Bài `AC-6`/`AC-14` của Dev
*(`test_wo022_tien_theo_tien_te.py:462`, `test_wo022_v2_…:306`)* **tự nhét** thân
cửa `{tien: '1234.16', lech_tuyet_doi: '0.40'}` — đúng khuôn người viết
**tưởng**, ⛔ khuôn cửa trả. Lớp lỗi `11` §6 *"khuôn thử tự nhét che chỗ thiếu"*
và `GAP-API-10` *(40/40 tuyến xanh mà khuôn sai)*. Bài ở đây lấy thân **từ cửa
thật** trên kho TEST rồi đưa nguyên vào hàm vẽ thật.

`WO-022` Phạm vi (c) **gọi tên** đúng chỗ này *(`man_f01_lenh.js` `:653`–`:654`
— tiền lệnh ↔ tiền bank · lệch)*; §5b ⓕ ví dụ *"`1234.56` vs `1234.16` ⇒ lệch
`0,40 USD`"* ⛔ bao giờ hiện được trên hộp này với cửa thật.

ⓐ **XANH** — canh khuôn cửa *(`BA-07 §4h ⓵`)*: thân thật mang `amount`/`lech`,
   ⛔ `tien`/`lech_tuyet_doi`. Sửa `F-1` bằng cách **lùi cửa** về hàng thô là
   phá hợp đồng ⇒ bài này ĐỎ.
ⓑ ~~`xfail(strict=True)`~~ — `F-1`, ĐỎ trên `959b75e`. ⭐ **`KQ-031` gỡ dấu**
   *(02/10)*: `BG-030` @ `e0d2a96` vá ⇒ hai bài `XPASS(strict)`; `fls-test` chạy
   lại trên **JS `a69ee92`** *(worktree)* ⇒ `XFAIL` ×2 đúng lý do *(cột Tiền
   `—`, lệch *"⛔ không tính được"*)* ⇒ gỡ dấu là **đúng lý do**, ⛔ "sửa cho xanh".

⭐ **`KQ-031` — tiền NGẪU NHIÊN** *(`BG-030` yếu #7)*: bản đầu dựng tiền cố
định `1234.56`/`1234.16`. Ứng viên sắp theo `(bậc, lệch, itl_id)` trong
`limit=50` ⇒ kho TEST giữ lại dòng `1234.56` của lượt khác *(đo 02/10: **3**
dòng `1234.56` USD còn trong `fls_test`)* thì dòng của lượt này có thể rơi ra
ngoài trang ⇒ bài ĐỎ *"không đo được"* vì **kho**, ⛔ vì mã. Nay phần nguyên
`<N>` ngẫu nhiên mỗi lượt; **lo của bài ⛔ đổi** *(xu `.56`/`.16` ⇒ lệch
`0,40`; khớp đúng xu ⇒ trong dung sai)*.
"""
from __future__ import annotations

import json
import random

import pytest

from tests.repo.test_wo003_ghep_tay_la_goi_y_pg import (_dong_bank, _lenh,  # noqa: F401
                                                        _ma, _run, conn)
from tests.web.khung_node import _chay, can_node
from tests.web.test_vong_f02_pg import V, _goi, may  # noqa: F401
from tests.web.test_wo008_chu_man_sau_bo_ghep import TEP_F01, VO_F01

pytestmark = pytest.mark.pg


@pytest.fixture()
def ca_tim_tien(conn, may):  # noqa: F811
    """Lệnh USD `<N>.56` · hai dòng tiền USD chưa nối: `<N>.56` *(khớp đúng)*
    và `<N>.16` *(lệch `0,40`)*. Trả `(mã lệnh, thân cửa THẬT, id khớp, id
    lệch, N)` — `N` ngẫu nhiên mỗi lượt *(`KQ-031`)*."""
    n = random.randint(100_000, 899_999)
    run = _run(conn)
    khop = _dong_bank(conn, run, f"{n}.56", "USD")
    lech = _dong_bank(conn, run, f"{n}.16", "USD")
    ma = _ma()
    _lenh(conn, run, (ma, f"{n}.56", "USD", "Approve", "HD-K29", "C-K29"))
    ok, r = _goi(may, f"{V}/queue/lenh/{ma}/itl-candidates?limit=50")
    assert ok == 200, r
    ids = [u["itl_id"] for u in r["data"]["ung_vien"]]
    # ⛔ `Đ3`: tập ứng viên phải CHỨA đúng hai dòng của bài — ⛔ đo trên tập rỗng
    assert khop in ids and lech in ids, (
        f"⛔ không đo được: cửa ⛔ trả hai dòng tiền của bài ({khop}, {lech}) "
        f"trong {len(ids)} ứng viên")
    return ma, r["data"], khop, lech, n


def _usd(n: int, xu: str) -> str:
    """Chuỗi in theo §5b ⓐ — `.` nghìn, `,` thập phân."""
    return f"{n:,}".replace(",", ".") + "," + xu


def _hop(ma: str, than: dict, i_chon: int, n: int) -> dict:
    """Đưa NGUYÊN thân cửa thật vào `F01L._drawer_tim_tien` thật, chọn ứng viên
    `i_chon` *(sự kiện `change` như trình duyệt)*; trả HTML hộp + câu `#sig-l`."""
    return _chay("""
      const MA = %s;
      _TRA['/queue/lenh/' + MA + '/itl-candidates'] = {data: %s};
      _TRA['/queue/lenh/' + MA] = {no: {cau: 'x'}};
      const s = document.createElement('div'); s.id = 'sig-l';
      document.body.appendChild(s);
      await F01L._drawer_tim_tien({pm_line_id: MA, amount: %s,
                                   curr: 'USD'});
      const b = document.getElementById('dlg-b');
      const c = document.createElement('input');
      c.type = 'radio'; c.name = 'uv'; c.checked = true; c.dataset.i = '%d';
      b.appendChild(c);
      (b._nghe.change || []).forEach(f => f({target: b}));
      return {hop: b.innerHTML, sig: s.innerHTML};
    """ % (json.dumps(ma), json.dumps(than, ensure_ascii=False, default=str),
           json.dumps(f"{n}.56"), i_chon), tep=TEP_F01, vo=VO_F01)


# ═══ ⓐ XANH — khuôn cửa đúng hợp đồng `BA-07 §4h ⓵` ════════════════════════
def test_khuon_CUA_THAT_itl_candidates_la_khuon_1_amount_lech(ca_tim_tien):
    """Thân thật mang `amount` + `lech` *(khuôn `⓵`)*, ⛔ khoá hàng thô `tien` /
    `lech_tuyet_doi`. ⛔ Chiều ĐỎ: lùi cửa về hàng thô *(trước `23/09`)*."""
    _ma_lenh, than, khop, lech, n = ca_tim_tien
    uv = {u["itl_id"]: u for u in than["ung_vien"]}
    for i in (khop, lech):
        assert "amount" in uv[i] and "lech" in uv[i], sorted(uv[i])
        assert "tien" not in uv[i] and "lech_tuyet_doi" not in uv[i], sorted(uv[i])
    assert str(uv[khop]["amount"]).startswith(f"{n}.56"), uv[khop]
    assert str(uv[lech]["amount"]).startswith(f"{n}.16"), uv[lech]


# ═══ ⓑ PHÁT HIỆN F-1 — ĐỎ hôm nay ═════════════════════════════════════════
@can_node
def test_F1_tim_tien_THAN_CUA_THAT_lech_0_40_in_ra_va_VUOT(ca_tim_tien):
    """Chọn dòng `<N>.16` ⇒ hộp in `<N>,16` ở cột Tiền, câu `#sig-l` in
    `lệch <b>0,40</b>` + `VƯỢT dung sai` *(USD dung sai `0` — `QĐ-ITL-62`)*.
    ⛔ Chiều ĐỎ *(đã chạy, `KQ-031`)*: JS `a69ee92` ⇒ cột Tiền `—` ⇒ ĐỎ."""
    ma, than, _khop, lech, n = ca_tim_tien
    i = [u["itl_id"] for u in than["ung_vien"]].index(lech)
    r = _hop(ma, than, i, n)
    assert _usd(n, "16") in r["hop"], r["hop"][:600]
    assert "không tính được" not in r["sig"], r["sig"]
    assert "lệch <b>0,40</b>" in r["sig"], r["sig"]
    assert "VƯỢT dung sai" in r["sig"], r["sig"]


@can_node
def test_F1_tim_tien_THAN_CUA_THAT_khop_DUNG_tien_la_TRONG_dung_sai(ca_tim_tien):
    """Chọn dòng `<N>.56` *(bậc `tien` — khớp đúng xu)* ⇒ `lệch <b>0,00</b>` +
    *"trong dung sai"*; ⛔ câu *"cửa ghi sẽ TỪ CHỐI"* cho một cặp cửa ghi
    **nhận**. ⛔ Chiều ĐỎ *(đã chạy, `KQ-031`)*: JS `a69ee92` ⇒ *"TỪ CHỐI"*."""
    ma, than, khop, _lech, n = ca_tim_tien
    i = [u["itl_id"] for u in than["ung_vien"]].index(khop)
    r = _hop(ma, than, i, n)
    assert "TỪ CHỐI" not in r["sig"], r["sig"]
    assert "lệch <b>0,00</b>" in r["sig"], r["sig"]
    assert "trong dung sai" in r["sig"], r["sig"]
