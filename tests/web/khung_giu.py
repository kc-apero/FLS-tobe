# -*- coding: utf-8 -*-
"""`WO-045` — **cửa giả GIỮ** cho bài *"lượt mới nhất thắng"* trên **mọi** màn
*(`BA-06` v4.19 `§4.5 ⓦ` ①)*, nuôi bằng **thân cửa thật** *(kho TEST)*.

⛔⛔ Vì sao ⛔ dùng lại `_CUA_GIU` của `test_wo042_doi_chip_khi_dang_tai.py`:
bản ấy **tự bịa** hàng *(`G<k>-<i>`)* — đúng cho câu *"hàng của lượt nào"*,
nhưng phiếu này đòi thân **cửa thật** *(`WO-045` giao việc: "thân từ cửa thật
kho TEST" — luật bài thử `BA-07` §4h ⓵, lớp *"khuôn thử tự nhét"* đã sống sót
ba lần)*. Ở đây bài **⛔ đặt** một hàng nào: `_TRA[<đường>]` là **nguyên văn**
phong bì `{data, meta}` cửa HTTP thật trả cho **đúng** đường ấy.

⭐ Hai chế độ cho mỗi lượt gọi `FLS.doc`:
  · đường khớp một mẫu trong `_GIU` ⇒ **giữ** tới khi kịch bản thả *(`_tha`)* —
    thứ tự về do **bài quyết**, ⛔ do đồng hồ *(`ⓥ`: ⛔ "bấm nhanh rồi mong")*;
  · còn lại ⇒ trả **ngay** thân thật của đường ấy.
⛔ Đường ⛔ có thân ⇒ lượt ấy **ném** *(và `_tha` ném trong bài)* — một kịch bản
gọi nhầm đường là **⛔ đo được** *(`Đ5`)*, ⛔ lặng lẽ xanh trên thân rỗng.

Khoá đường dựng **đúng** cách `goi_cua.js` dựng URL *(`searchParams.set` bỏ
`null`/`undefined`/`''`)* — để `F01` *(`FLS.doc('/queue', {curr, …})`)* và
`F01L` *(chuỗi `?…` tự ghép)* cùng một khoá với đường Python đã gọi cửa thật.
"""
from __future__ import annotations

import json
from urllib.parse import quote

CUA_GIU = r"""
globalThis._HANG = [];
globalThis._GIU = [];
globalThis._khoa = function (duong, q) {
  if (!q) return duong;
  const p = [];
  Object.keys(q).forEach(function (k) {
    const v = q[k];
    if (v !== null && v !== undefined && v !== '') p.push(k + '=' + encodeURIComponent(v));
  });
  return p.length ? duong + (duong.indexOf('?') >= 0 ? '&' : '?') + p.join('&') : duong;
};
globalThis._than = function (k) {
  const t = _TRA[k];
  if (!t) throw new Error('⛔ không đo được: bài thiếu thân cửa thật cho ' + k);
  return {data: t.data, meta: t.meta || {}};
};
FLS.doc = function (duong, q) {
  const k = _khoa(duong, q);
  _GOI.push(['doc', k]);
  if (_GIU.some(m => k.indexOf(m) >= 0))
    return new Promise((ok, no) => _HANG.push({k, ok, no, xong: false}));
  try { return Promise.resolve(_than(k)); } catch (e) { return Promise.reject(e); }
};
FLS.ghi = function (duong, than) {
  _GOI.push(['ghi', duong, than]);
  return Promise.resolve({data: {}, meta: {}});
};
globalThis._cho = async () => {
  for (let i = 0; i < 30; i++) await Promise.resolve();
  await new Promise(r => setTimeout(r, 0));
};
globalThis._tim = (mau) => _HANG.find(h => !h.xong && h.k.indexOf(mau) >= 0);
globalThis._tha = async (mau) => {
  const h = _tim(mau);
  if (!h) throw new Error('⛔ không đo được: không có lượt chờ khớp ' + mau
                          + ' — ' + JSON.stringify(_HANG.map(x => [x.k, x.xong])));
  h.xong = true;
  h.ok(_than(h.k));
  await _cho();
};
globalThis._no = async (mau, loi) => {
  const h = _tim(mau);
  if (!h) throw new Error('⛔ không đo được: không có lượt chờ khớp ' + mau);
  h.xong = true; h.no(loi); await _cho();
};
globalThis._doc = (mau) => _GOI.filter(g => g[0] === 'doc' && g[1].indexOf(mau) >= 0)
                               .map(g => g[1]);
globalThis._ghi = () => _GOI.filter(g => g[0] === 'ghi').map(g => [g[1], g[2]]);
/* ⭐ Bấm như trình duyệt: nút `disabled` ⛔ nhận cú bấm. Trả `true` ⇔ đã bấm. */
globalThis._bam = function (b) {
  if (!b || b.disabled) return false;
  if (b.onclick) { b.onclick({preventDefault() {}, target: b}); return true; }
  const n = (b._nghe || {}).click || [];
  n.forEach(f => f({preventDefault() {}, target: b}));
  return n.length > 0;
};
globalThis._nut = (goc, chu) => goc.querySelectorAll('button')
                                   .filter(b => b.textContent === chu);
"""


def ma_uri(s: str) -> str:
    """`encodeURIComponent` của JS — để đường Python gọi cửa thật **=** khoá
    màn dựng *(con trỏ trang mang ký tự phải thoát)*."""
    return quote(s, safe="-_.!~*'()")


def nap(tra: dict) -> str:
    """Nạp phong bì `{data, meta}` cửa thật vào `_TRA` theo **đúng** đường."""
    return ("const TRA = %s;\n"
            "for (const k of Object.keys(TRA)) _TRA[k] = TRA[k];\n"
            % json.dumps(tra, ensure_ascii=False, default=str))
