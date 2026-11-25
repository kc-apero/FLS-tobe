"""ĐĂNG NHẬP FLS cho staging sau Google IAP — MỘT tài khoản chung cho nhóm test · WO-363 (bổ sung theo chủ 24/11 ~03:45).

    printf '%s' "$MK" | python tools/staging/app/dang_nhap.py --bam --ten HondurasGesha   # in BẢN GHI băm (JSON) — ⛔ mật khẩu

Hai lớp: Google IAP (ai được vào link) → màn `/login` này (biết mật khẩu chung). Lớp này nằm trong `cong_iap.py`
(⛔ trong cửa): cửa `chay_cua.py` · màn hình `fls/web/tep` · luật `GAP-WEB-01` ⛔ đổi. `phien.js` (nơi màn hình nhận
thẻ `ke_toan`) chỉ ra được SAU đăng nhập — cổng chặn MỌI đường trừ `/login` · `/logout` khi chưa có phiên.

⭐ Băm = **scrypt** (`hashlib.scrypt`, RFC 7914) — chọn vì: ① có sẵn trong thư viện chuẩn Python (ảnh chạy chỉ
   có `psycopg` — ⛔ thêm `argon2-cffi`/`bcrypt` cần biên dịch/bánh xe nhị phân vào ảnh và vào `requirements.txt`);
   ② tốn BỘ NHỚ (N=2^14, r=8 ⇒ 16 MiB/lần) nên đoán mật khẩu bằng GPU đắt — cùng nhóm với argon2, hơn bcrypt;
   ③ OWASP Password Storage Cheat Sheet liệt kê scrypt là lựa chọn hợp lệ khi ⛔ có argon2id. Muối 16 byte ngẫu nhiên.
⭐ So khớp THỜI GIAN HẰNG: `hmac.compare_digest` cho cả tên lẫn băm; tên SAI vẫn chạy scrypt (⛔ lộ "tên đúng" qua thời gian).
⭐ Khoá tạm: `SAI_TOI_DA` lần sai trong `CUA_SO_GIAY` ⇒ khoá `KHOA_GIAY` — đếm theo EMAIL IAP (một người gõ sai ⛔ khoá
   người khác) **VÀ** toàn cục `SAI_TOAN_CUC` lần sai của MỌI email ⇒ khoá chung (`STG-WEB-R1-07`: nhiều tài khoản
   Google ⛔ nhân hạn mức đoán). Đang khoá ⇒ ⛔ chạy so khớp (429).
⭐ Phiên: cookie `__Host-fls_phien` = `v2.<thế hệ>.<hết hạn>.<email b64>.<HMAC-SHA256>` — HttpOnly · Secure ·
   SameSite=Strict · Path=/ · Max-Age = `PHIEN_GIAY` (8 giờ = tuổi thẻ cửa phát). Gắn với EMAIL IAP.
⭐⭐ TRẠNG THÁI BỀN (`STG-WEB-R1-02` · `-06`, R1 `KQ-365`): bản đầu giữ thu hồi + bộ đếm sai trong BỘ NHỚ instance ⇒ Cloud
   Run scale-về-0 / dựng lại thì cookie đã `/logout` HỢP LỆ LẠI và khoá tạm về 0; và khoá HMAC suy từ bản ghi băm ⇒ ai
   đọc được `fls-staging-login` rèn được cookie. Nay trạng thái nằm ở bí mật RIÊNG `fls-staging-phien` (JSON
   `{"khoa", "the_he", "sai", "khoa_toi"}`): khoá HMAC = 32 byte NGẪU NHIÊN (08 sinh, đổi mật khẩu ⇒ khoá mới ⇒ mọi
   phiên cũ mất); `the_he[email]` = thế hệ phiên — `/logout` TĂNG nó ⇒ mọi cookie cũ của email ấy mất, KỂ CẢ sau khởi
   động lại; bộ đếm sai + mốc khoá cũng ghi vào đó. Mỗi lần ghi = MỘT phiên bản bí mật mới, phiên bản vừa đọc bị huỷ.
   Đọc giữ `GIU_TRANG_THAI` giây; ghi thì đọc MỚI rồi mới ghi (⛔ đè lần xoay khoá của 08). Đọc hỏng ⇒ ⛔ ai vào (ĐÓNG);
   ghi hỏng ⇒ vẫn áp ở bộ nhớ instance + nhật ký `⛔ DANG_NHAP_GHI_LOI`.
⛔ Mật khẩu ⛔ in · ⛔ ghi nhật ký · ⛔ argv · ⛔ trong bản ghi (chỉ băm). Nhật ký chỉ: `DANG_NHAP email=… dung|sai n/5|khoa`.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import hmac
import html
import json
import os
import sys
import threading
import time

SCRYPT_N, SCRYPT_R, SCRYPT_P, SCRYPT_DK = 2 ** 14, 8, 1, 32
SCRYPT_N_TOI_DA = 2 ** 20                      # bản ghi lạ đòi N khổng lồ ⇒ từ chối (⛔ để một bí mật hỏng làm treo cổng)
SAI_TOI_DA, CUA_SO_GIAY, KHOA_GIAY = 5, 15 * 60, 15 * 60
PHIEN_GIAY = 8 * 3600
COOKIE = "__Host-fls_phien"
MK_NGAN_NHAT = 12


def _b64(b: bytes) -> str:
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def _unb64(s: str) -> bytes:
    return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))


def bam(mk: str, muoi: bytes | None = None) -> str:
    muoi = os.urandom(16) if muoi is None else muoi
    h = hashlib.scrypt(mk.encode("utf-8"), salt=muoi, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P,
                       maxmem=2 ** 26, dklen=SCRYPT_DK)
    return f"scrypt${SCRYPT_N}${SCRYPT_R}${SCRYPT_P}${_b64(muoi)}${_b64(h)}"


def khop(mk: str, ban_ghi: str) -> bool:
    try:
        ten, n, r, p, muoi, h = ban_ghi.split("$")
        n, r, p, muoi, h = int(n), int(r), int(p), _unb64(muoi), _unb64(h)
    except (ValueError, TypeError):
        return False
    if ten != "scrypt" or not (2 <= n <= SCRYPT_N_TOI_DA and n & (n - 1) == 0 and 1 <= r <= 16 and 1 <= p <= 4) \
            or len(h) < 16 or len(muoi) < 8:
        return False
    tinh = hashlib.scrypt(mk.encode("utf-8"), salt=muoi, n=n, r=r, p=p, maxmem=2 ** 27, dklen=len(h))
    return hmac.compare_digest(tinh, h)


_BAM_MOI = bam(_b64(os.urandom(24)))   # tính SẴN lúc nạp: tên SAI cũng đúng MỘT lần scrypt (⛔ thêm lần đầu)
SAI_TOAN_CUC = 20
GIU_TRANG_THAI = 30


def _bam_moi() -> str:
    return _BAM_MOI


def kiem_dang_nhap(ten: str, mk: str, tk: dict) -> bool:
    """So tên + mật khẩu THỜI GIAN HẰNG: luôn đúng MỘT lần scrypt (tên sai ⇒ so với bản ghi mồi), cả hai so bằng
    `hmac.compare_digest` (`STG-WEB-R1-04`: bài đếm số lần scrypt + cấm `==`)."""
    ten_dung = hmac.compare_digest(ten.encode("utf-8"), str(tk["ten"]).encode("utf-8"))
    mk_dung = khop(mk, tk["bam"] if ten_dung else _BAM_MOI)
    return ten_dung & mk_dung


# ══ tài khoản (đọc từ Secret Manager qua hàm truyền vào; giữ 60 giây) ═════════════════════════════════════
class TaiKhoan:
    def __init__(self, doc_bi_mat, giu_giay: float = 60):
        self.doc, self.giu, self.luc, self.gt, self._kh = doc_bi_mat, giu_giay, 0.0, None, threading.Lock()

    def lay(self) -> dict | None:
        """`{"ten": …, "bam": "scrypt$…"}` hoặc None (chưa đặt / hỏng). Đọc lại sau `giu_giay` ⇒ chủ chạy
        `08_dat_dang_nhap.sh` thì ≤ 1 phút sau có hiệu lực, ⛔ cần dựng lại service."""
        with self._kh:
            if time.time() - self.luc > self.giu or self.gt is None:
                try:
                    o = json.loads(self.doc() or "")
                    self.gt = o if isinstance(o, dict) and o.get("ten") and str(o.get("bam", "")).startswith("scrypt$") else None
                except (ValueError, TypeError, SystemExit, OSError):
                    self.gt = None
                self.luc = time.time()
            return self.gt


# ══ trạng thái phiên BỀN (bí mật `fls-staging-phien`) ════════════════════════════════════════════════════
def trang_thai_moi() -> dict:
    return {"khoa": _b64(os.urandom(32)), "the_he": {}, "sai": {}, "khoa_toi": {}}


def _dung_hinh(o) -> bool:
    try:
        return (isinstance(o, dict) and len(_unb64(o["khoa"])) >= 32
                and all(isinstance(o.get(k), dict) for k in ("the_he", "sai", "khoa_toi")))
    except (KeyError, TypeError, ValueError):
        return False


class TrangThai:
    """`doc()` ⇒ chuỗi JSON (hỏng ⇒ ngoại lệ/rỗng) · `ghi(chuỗi)` ⇒ ghi phiên bản mới (hỏng ⇒ ngoại lệ)."""

    def __init__(self, doc, ghi, giu_giay: float = GIU_TRANG_THAI, dong_ho=time.time):
        self.doc, self.ghi, self.giu, self.t = doc, ghi, giu_giay, dong_ho
        self.gt, self.luc, self._kh = None, -1e18, threading.RLock()

    def _doc_moi(self):
        try:
            o = json.loads(self.doc() or "")
        except (ValueError, TypeError, SystemExit, OSError):
            return None
        return o if _dung_hinh(o) else None

    def lay(self) -> dict | None:
        with self._kh:
            if self.gt is None or self.t() - self.luc > self.giu:
                self.gt, self.luc = self._doc_moi(), self.t()
            return self.gt

    def sua(self, f) -> bool:
        """Đọc MỚI → `f(st)` → ghi. Trả False nếu ghi hỏng (đã áp vào bản trong bộ nhớ — vẫn có hiệu lực ở instance này)."""
        with self._kh:
            st = self._doc_moi() or self.gt
            if st is None:
                return False
            f(st)
            self.gt, self.luc = st, self.t()
            try:
                self.ghi(json.dumps(st, separators=(",", ":"), sort_keys=True))
                return True
            except (OSError, ValueError, SystemExit) as e:
                print(f"⛔ DANG_NHAP_GHI_LOI {type(e).__name__}", file=sys.stderr, flush=True)
                return False


def con_khoa(st: dict, ai: str, now: float) -> int:
    toi = max(float(st["khoa_toi"].get(ai, 0)), float(st["khoa_toi"].get("*", 0)))
    return max(0, int(toi - now + 0.999))


def ghi_sai(st: dict, ai: str, now: float) -> int:
    """Một lần sai cho `ai` và cho bộ đếm toàn cục `*`; trả số lần sai của `ai` trong cửa sổ."""
    n = 0
    for k, tran in ((ai, SAI_TOI_DA), ("*", SAI_TOAN_CUC)):
        ds = [x for x in st["sai"].get(k, []) if now - x < CUA_SO_GIAY] + [now]
        if len(ds) >= tran:
            st["khoa_toi"][k] = now + KHOA_GIAY
            ds = []
        st["sai"][k] = ds
        if k == ai:
            n = len(ds) or tran
    st["khoa_toi"] = {k: v for k, v in st["khoa_toi"].items() if v > now}
    return n


def xoa_sai(st: dict, ai: str) -> None:
    st["sai"].pop(ai, None)


def dang_xuat(st: dict, email: str) -> None:
    st["the_he"][email] = int(st["the_he"].get(email, 0)) + 1


def _ky(st: dict, than: str) -> bytes:
    return hmac.new(_unb64(st["khoa"]), than.encode(), hashlib.sha256).digest()


def tao_phien(st: dict, email: str, now: float) -> str:
    than = f"v2.{int(st['the_he'].get(email, 0))}.{int(now) + PHIEN_GIAY}.{_b64(email.encode())}"
    return than + "." + _b64(_ky(st, than))


def phien_hop_le(the: str | None, email: str, st: dict | None, now: float) -> bool:
    if not the or st is None or the.count(".") != 4:
        return False
    than, ky = the.rsplit(".", 1)
    try:
        dung = hmac.compare_digest(_unb64(ky), _ky(st, than))
        _, the_he, het, em = than.split(".")
        the_he, het, em = int(the_he), int(het), _unb64(em).decode()
    except (ValueError, TypeError, UnicodeDecodeError):
        return False
    return (dung and het > now and hmac.compare_digest(em.encode(), email.encode())
            and the_he == int(st["the_he"].get(email, 0)))


def doc_cookie(chuoi: str | None) -> str | None:
    for phan in (chuoi or "").split(";"):
        k, _, v = phan.strip().partition("=")
        if k == COOKIE:
            return v
    return None


def cookie_dat(the: str) -> str:
    return f"{COOKIE}={the}; Path=/; Max-Age={PHIEN_GIAY}; HttpOnly; Secure; SameSite=Strict"


def cookie_xoa() -> str:
    return f"{COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Strict"


def trang(thong_bao: str = "", loai: str = "") -> bytes:
    """Màn `/login` — tự chứa (⛔ tệp ngoài, ⛔ script). `thong_bao` do MÃ đặt (⛔ phản chiếu chữ người gõ) và vẫn được thoát."""
    tb = f'<p class="tb {loai}">{html.escape(thong_bao)}</p>' if thong_bao else ""
    return f"""<!doctype html>
<html lang="vi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>FLS · đăng nhập staging</title>
<style>
:root{{--nen:#f6f7f9;--the:#fff;--chu:#1b1f24;--phu:#5b6470;--vien:#d5dae1;--nhan:#1f5fbf;--loi:#b3261e}}
@media (prefers-color-scheme:dark){{:root{{--nen:#14171b;--the:#1d2127;--chu:#e8eaed;--phu:#a3acb8;--vien:#363c45;--nhan:#7fb0ff;--loi:#ff8a80}}}}
body{{margin:0;min-height:100vh;display:grid;place-items:center;background:var(--nen);color:var(--chu);font:16px/1.5 system-ui,sans-serif}}
form{{background:var(--the);border:1px solid var(--vien);border-radius:10px;padding:28px 24px;width:min(360px,calc(100vw - 32px));box-sizing:border-box}}
h1{{font-size:20px;margin:0 0 4px}} .phu{{color:var(--phu);font-size:13px;margin:0 0 18px}}
label{{display:block;font-size:14px;margin:12px 0 4px}}
input{{width:100%;box-sizing:border-box;padding:9px 10px;border:1px solid var(--vien);border-radius:6px;background:transparent;color:inherit;font:inherit}}
button{{margin-top:18px;width:100%;padding:10px;border:0;border-radius:6px;background:var(--nhan);color:#fff;font:inherit;cursor:pointer}}
.tb{{margin:12px 0 0;font-size:14px}} .tb.loi{{color:var(--loi)}}
</style></head><body>
<form method="post" action="/login" autocomplete="on">
<h1>FLS · staging</h1>
<p class="phu">Tài khoản chung của nhóm test. Mọi chữ ký trên staging mang tên người chủ khai khi dựng (⛔ tên bạn).</p>
<label for="ten">Tên đăng nhập</label><input id="ten" name="ten" autocomplete="username" required>
<label for="mat_khau">Mật khẩu</label><input id="mat_khau" name="mat_khau" type="password" autocomplete="current-password" required>
<button type="submit">Đăng nhập</button>{tb}
</form></body></html>""".encode("utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="In BẢN GHI băm (JSON) từ mật khẩu ở stdin — ⛔ nhận mật khẩu qua argv.")
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--bam", action="store_true")
    g.add_argument("--trang-thai-moi", action="store_true", help="in trạng thái phiên MỚI (khoá ngẫu nhiên) — 08 dùng")
    ap.add_argument("--ten")
    a = ap.parse_args(argv)
    if a.trang_thai_moi:
        print(json.dumps(trang_thai_moi()))
        return 0
    if not a.ten:
        print("⛔ --bam đòi --ten", file=sys.stderr)
        return 2
    mk = sys.stdin.read()
    if mk.endswith("\n"):
        mk = mk[:-1]
    if len(mk) < MK_NGAN_NHAT:
        print(f"⛔ mật khẩu ngắn hơn {MK_NGAN_NHAT} ký tự", file=sys.stderr)
        return 2
    if mk == a.ten:
        print("⛔ mật khẩu trùng tên đăng nhập", file=sys.stderr)
        return 2
    print(json.dumps({"ten": a.ten, "bam": bam(mk)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
