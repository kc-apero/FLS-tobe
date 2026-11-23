/* ═══════════════════════════════════════════════════════════════════════
   dom_gia.js — MOT CAI DOM TOI THIEU, du de chay THAT tam hanh vi cua luoi.

   ⛔⛔ **Doc ky phan nay truoc khi tin mot bai kiem nao dua tren no.**

   Day ⛔ **khong** phai mot trinh duyet. No lam duoc dung nhung gi `man_f02.js`
   cham toi: cay the, `classList`, `textContent`, `dataset`, `tBodies/rows/
   cells`, va **hai duong su kien** *(`keydown`, `paste`)*. Nho vay tam hanh vi
   §1 duoc **chay that**, ⛔ khong phai doc bang mat.

   ⛔ **Nhung thu no ⛔ KHONG kiem duoc, va vi the van con nam o `B7 · UAT`:**
     · **Dong cung** tieu de + hai cot khoa — do la `position:sticky`, mot
       chuyen cua **trinh bay**, ⛔ khong phai cua ma.
     · **346px co du khong** — mot cau hoi ve **mat nguoi**, ⛔ khong ve pixel.
     · **Cam giac khi go** — do tre khi ve 200 dong tren may ke toan.
   ⇒ Mot bai o day xanh nghia la **co che dung**, ⛔ khong phai *"man hinh da
     tot"*. Cong so **8** cua `DEV-12` khai thang dieu do.
   ═══════════════════════════════════════════════════════════════════════ */
'use strict';

function lam_dom() {
  const theo_id = new Map();
  const nghe = { keydown: [], paste: [], click: [] };

  function _lop(e) {
    return (e.className || '').split(/\s+/).filter(Boolean);
  }

  function tao(ten) {
    const e = {
      tagName: ten.toUpperCase(),
      className: '',
      children: [],
      parentNode: null,
      style: {},
      dataset: {},
      _txt: '',
      _html: '',
      title: '',
      disabled: false,
      value: '',
      placeholder: '',
      // ⭐⭐ Hai so DAN TRANG — mac dinh `0` ca hai, tuc *"⛔ khong bi cat"*.
      //
      // ⛔⛔ Mot DOM gia ⛔ khong dan trang duoc, nen no ⛔ **KHONG** the tu
      //    sinh hai so nay. Bai thu phai **tu dat** *(`e._scrollHeight = 40`)*
      //    — va do la mot gioi han **phai noi ra**, ⛔ khong phai mot phep do.
      // ⭐ Cai do duoc o day la **LUAT**: *"chi moi `đủ ↓` khi
      //   `scrollHeight > clientHeight`"*. Con **con so that** thi chi trinh
      //   duyet that tra loi duoc (`NFR-I10`).
      // ⭐ `scrollTop` la mot so GHI DUOC that — khac hai so tren. Man
      //   phai **nho va tra lai** no qua moi lan `ve()`, va do la mot luat
      //   do duoc bang DOM gia: dung `ve()` xoa het cay thi no ve `0`.
      scrollTop: 0,
      _scrollHeight: 0,
      _clientHeight: 0,
      get scrollHeight() { return e._scrollHeight; },
      get clientHeight() { return e._clientHeight; },
      scrollIntoView() { },
      focus() { e._focus = true; },
      setSelectionRange() { },
      appendChild(c) { c.parentNode = e; e.children.push(c); return c; },
      insertBefore(c) { c.parentNode = e; e.children.unshift(c); return c; },
      removeChild(c) {
        e.children = e.children.filter(x => x !== c); return c;
      },
      closest(sel) {
        let x = e;
        while (x) { if (khop(x, sel)) return x; x = x.parentNode; }
        return null;
      },
      setAttribute(k, v) { e[k] = v; },
      getAttribute(k) { return e[k]; },
      querySelector(s) { return tim(e, s)[0] || null; },
      querySelectorAll(s) { return tim(e, s); },
      // ⭐ `addEventListener` tren TUNG the — them 09/09.
      //
      // ⛔⛔ Truoc no, `hop_thoai.js` NO ngay dong dau (`s.addEventListener is
      // not a function`) ⇒ **⛔ khong bai nao thu duoc mot hop thoai**, ke ca
      // hop thoai cua mot cu bam GHI. Do ⛔ khong phai mot han che co chu y —
      // `document` da co ham nay, chi TUNG THE la thieu.
      // ⚠ Ghi vao mot so ghi RIENG cua the (⛔ khong noi bot lan len cay): bo
      //    bai goi tay `_nghe` khi can, va mot phep noi bot GIA se lam bai tin
      //    rang mot cu bam **da lan** trong khi that ra ⛔ khong.
      addEventListener(ten, f) {
        (e._nghe[ten] = e._nghe[ten] || []).push(f);
      },
      removeEventListener(ten, f) {
        e._nghe[ten] = (e._nghe[ten] || []).filter(x => x !== f);
      },
      // ⭐ `insertAdjacentHTML` — them 05/10 *(`WO-045`)*. `man_f01.js` goi
      // no o **hai** cho *(`_thanh_loc` khi CHI DOC · chan luoi khi het
      // trang)* ⇒ truoc no, **⛔ bai nao** ve duoc lan tien o che do chi doc
      // — dung che do `ⓦ` ② doi kiem. ⛔ Van ⛔ phan tich HTML *(luat dau
      // tep)*: chuoi vao MOT the con, giu nguyen van de doi chieu chuoi.
      insertAdjacentHTML(_vi_tri, html) {
        const c = tao('span');
        c.innerHTML = html;
        e.appendChild(c);
      }
    };
    e._nghe = {};
    e.classList = {
      add(...c) {
        const l = _lop(e);
        c.forEach(x => { if (!l.includes(x)) l.push(x); });
        e.className = l.join(' ');
      },
      remove(...c) {
        e.className = _lop(e).filter(x => !c.includes(x)).join(' ');
      },
      contains(c) { return _lop(e).includes(c); },
      toggle(c, buoc) {
        const co = buoc === undefined ? !_lop(e).includes(c) : !!buoc;
        if (co) e.classList.add(c); else e.classList.remove(c);
        return co;
      }
    };
    Object.defineProperty(e, 'id', {
      get() { return e._id || ''; },
      set(v) { e._id = v; theo_id.set(v, e); }
    });
    Object.defineProperty(e, 'textContent', {
      get() {
        if (e.children.length) return e.children.map(c => c.textContent).join('');
        return e._txt;
      },
      set(v) { e.children = []; e._txt = String(v); }
    });
    Object.defineProperty(e, 'innerHTML', {
      get() { return e._html; },
      // ⛔ ⛔ Khong PHAN TICH HTML — bai kiem nao can cau truc that thi phai
      // dung `createElement`. Giu nguyen van de con doi chieu chuoi.
      set(v) { e.children = []; e._html = String(v); e._txt = String(v); }
    });
    // Bang: `tBodies` · `rows` · `cells` · `rowIndex` · `cellIndex`
    Object.defineProperty(e, 'tBodies', {
      get() { return e.children.filter(c => c.tagName === 'TBODY'); }
    });
    Object.defineProperty(e, 'rows', {
      get() { return e.children.filter(c => c.tagName === 'TR'); }
    });
    Object.defineProperty(e, 'cells', {
      get() {
        return e.children.filter(c => c.tagName === 'TD' || c.tagName === 'TH');
      }
    });
    Object.defineProperty(e, 'rowIndex', {
      // ⚠ Nhu DOM that: dem CA dong tieu de. `man_f02.js` tru 1 de ve chi so
      // trong than — chep sai cho nay la lech mot dong tren MOI phep dieu huong.
      get() {
        let b = e.parentNode;           // thead / tbody
        if (!b) return -1;
        const t = b.parentNode;
        if (!t) return -1;
        let n = 0;
        for (const k of t.children) {
          for (const r of k.rows) { if (r === e) return n; n++; }
        }
        return -1;
      }
    });
    Object.defineProperty(e, 'cellIndex', {
      get() { return e.parentNode ? e.parentNode.cells.indexOf(e) : -1; }
    });
    return e;
  }

  /* Bo chon rat nho: `#id` · `tag` · `.lop` · `tag.lop` · `[data-x]` ·
     `#id tag` (mot cap). Du cho nhung gi `man_f02.js` dung, ⛔ khong hon —
     mot bo chon day du la mot thu vien, va do la thu du an nay tu choi. */
  function khop(e, sel) {
    return sel.split(',').some(function (p) {
      p = p.trim();
      if (!p) return false;
      const cap = p.split(/\s+/);
      if (cap.length === 2) {
        if (!khop(e, cap[1])) return false;
        let x = e.parentNode;
        while (x) { if (khop(x, cap[0])) return true; x = x.parentNode; }
        return false;
      }
      if (p.startsWith('#')) return e.id === p.slice(1);
      /* ⚠⚠ Chi `[a-z-]` — mot khoa `data-` co **gach duoi** se ⛔
         KHONG khop mau nay, roi roi xuong nhanh tag/lop va khop **⛔
         khong gi**. ⛔ Va no ⛔ khong bao loi: bai kiem nhan `[]` va
         doc thanh *"man hinh ⛔ khong ve"*. Da can that 08/09
         (`[data-sid_bb]`). ⇒ Dat ten neo bang **mot tu**. */
      const m = p.match(/^\[([a-z-]+)\]$/);
      if (m) {
        const k = m[1].replace(/^data-/, '')
          .replace(/-([a-z])/g, (_, c) => c.toUpperCase());
        return e.dataset[k] !== undefined;
      }
      const bit = p.split('.');
      const tag = bit.shift();
      if (tag && e.tagName !== tag.toUpperCase()) return false;
      return bit.every(l => _lop(e).includes(l));
    });
  }

  function tim(goc, sel) {
    const ra = [];
    (function di(e) {
      e.children.forEach(function (c) {
        if (khop(c, sel)) ra.push(c);
        di(c);
      });
    })(goc);
    return ra;
  }

  const body = tao('body');
  const document = {
    body: body,
    readyState: 'complete',
    createElement: tao,
    getElementById: id => theo_id.get(id) || null,
    querySelector(s) {
      if (s.startsWith('#') && !s.includes(' ')) return theo_id.get(s.slice(1)) || null;
      return tim(body, s)[0] || null;
    },
    querySelectorAll: s => tim(body, s),
    addEventListener(ten, f) { (nghe[ten] = nghe[ten] || []).push(f); }
  };
  body.contains = function (x) {
    let e = x;
    while (e) { if (e === body) return true; e = e.parentNode; }
    return false;
  };

  /* ── ban su kien ────────────────────────────────────────────────────── */
  function ban(ten, sk) {
    sk.preventDefault = sk.preventDefault || function () { };
    sk.stopPropagation = sk.stopPropagation || function () { };
    (nghe[ten] || []).forEach(f => f(sk));
  }

  return {
    document: document,
    body: body,
    ban: ban,
    phim: (k, tuy) => ban('keydown', Object.assign({ key: k }, tuy || {})),
    dan: (txt, o) => ban('paste', {
      clipboardData: { getData: () => txt }, target: o
    })
  };
}

export { lam_dom };
