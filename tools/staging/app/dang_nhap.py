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
⭐ Khoá tạm: `SAI_TOI_DA` lần sai trong `CUA_SO_GIAY` ⇒ khoá `KHOA_GIAY` — đếm theo EMAIL IAP (mỗi người test một
   tài khoản Google; một người gõ sai ⛔ khoá người khác). Đang khoá ⇒ ⛔ chạy so khớp (429).
⭐ Phiên: cookie `__Host-fls_phien` = `v1.<hết hạn>.<email b64>.<HMAC-SHA256>` — HttpOnly · Secure · SameSite=Strict ·
   Path=/ · Max-Age = `PHIEN_GIAY` (8 giờ = tuổi thẻ cửa phát). Gắn với EMAIL IAP (đem cookie sang tài khoản Google
   khác ⇒ vô hiệu). Khoá HMAC suy từ BẢN GHI băm ⇒ đổi mật khẩu = mọi phiên cũ mất. `/logout` thu hồi phiên (bộ
   nhớ của instance) + xoá cookie. Phiên ⛔ lưu ở máy chủ ⇒ Cloud Run scale-về-0 rồi dậy lại vẫn giữ.
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


_BAM_MOI = None


def _bam_moi() -> str:
    """Bản ghi băm của một chuỗi ngẫu nhiên — để tên SAI vẫn tốn đúng một lần scrypt (thời gian hằng)."""
    global _BAM_MOI
    if _BAM_MOI is None:
        _BAM_MOI = bam(_b64(os.urandom(24)))
    return _BAM_MOI


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


class KhoaSai:
    def __init__(self, dong_ho=time.time):
        self.t, self.sai, self.khoa_toi, self._kh = dong_ho, {}, {}, threading.Lock()

    def con_khoa(self, ai: str) -> int:
        with self._kh:
            return max(0, int(self.khoa_toi.get(ai, 0) - self.t() + 0.999))

    def ghi_sai(self, ai: str) -> int:
        """Ghi một lần sai; trả số lần sai trong cửa sổ (đạt `SAI_TOI_DA` ⇒ khoá)."""
        with self._kh:
            now = self.t()
            ds = [x for x in self.sai.get(ai, []) if now - x < CUA_SO_GIAY] + [now]
            self.sai[ai] = ds
            if len(ds) >= SAI_TOI_DA:
                self.khoa_toi[ai] = now + KHOA_GIAY
                self.sai[ai] = []
            return len(ds)

    def xoa(self, ai: str) -> None:
        with self._kh:
            self.sai.pop(ai, None)


class Phien:
    def __init__(self, dong_ho=time.time):
        self.t, self.thu_hoi, self._kh = dong_ho, {}, threading.Lock()

    @staticmethod
    def _khoa(ban_ghi_bam: str) -> bytes:
        return hashlib.sha256(b"fls-phien-v1|" + ban_ghi_bam.encode()).digest()

    def tao(self, email: str, ban_ghi_bam: str) -> str:
        than = f"v1.{int(self.t()) + PHIEN_GIAY}.{_b64(email.encode())}"
        return than + "." + _b64(hmac.new(self._khoa(ban_ghi_bam), than.encode(), hashlib.sha256).digest())

    def hop_le(self, the: str | None, email: str, ban_ghi_bam: str) -> bool:
        if not the or the.count(".") != 3:
            return False
        than, ky = the.rsplit(".", 1)
        try:
            dung = hmac.compare_digest(_unb64(ky), hmac.new(self._khoa(ban_ghi_bam), than.encode(), hashlib.sha256).digest())
            _, het, em = than.split(".")
            het, em = int(het), _unb64(em).decode()
        except (ValueError, TypeError, UnicodeDecodeError):
            return False
        with self._kh:
            thu_hoi = the in self.thu_hoi
        return dung and het > self.t() and hmac.compare_digest(em.encode(), email.encode()) and not thu_hoi

    def thu_hoi_the(self, the: str | None) -> None:
        if not the:
            return
        with self._kh:
            now = self.t()
            self.thu_hoi = {k: v for k, v in self.thu_hoi.items() if v > now}
            self.thu_hoi[the] = now + PHIEN_GIAY


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
    ap.add_argument("--bam", action="store_true", required=True)
    ap.add_argument("--ten", required=True)
    a = ap.parse_args(argv)
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
