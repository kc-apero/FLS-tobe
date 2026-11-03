"""Kiem THE (token) — **fail-closed**: khong chung minh duoc thi tu choi.

`BA-07` §1: *"JWT ngan han fail-closed; `actor` lay TU TOKEN, khong tu khai"*.
Ly do rieng cua FLS: `QĐ-ITL-27` khai tu vai nguoi hau kiem, nen **nhat ky la
cho kiem soat duy nhat con lai**. Mot nhat ky ma `actor` do nguoi goi tu khai
thi no khong con la nhat ky.

⛔⛔ **Tu viet phep kiem JWT thi phai chan dung ba cai bay da tung ha nhieu he:**

  ⓐ **doi thuat toan** — the khai `alg: "none"` roi khong mang chu ky nao. ⇒ o
    day `alg` phai **dung bang** `"HS256"`, ban TRANG, khong phai ban den.
  ⓑ **so sanh chu ky bang `==`** — ro thoi gian. ⇒ `hmac.compare_digest`.
  ⓒ **the khong co han** — mot the ro ra la ro vinh vien. ⇒ **bat buoc** co
    `exp`, thieu la tu choi (⛔ khong phai "coi nhu khong han").

⛔ Va cai thu tu: **khong co chia khoa thi cua khong mo**. Bien
`FLS_JWT_SECRET` trong thi may **tu choi chay**, ⛔ khong chay o che do "tam
thoi cho qua het" — che do do la che do se song mai.

⚠ Vi sao khong dung thu vien: kho nay dang co **ba** goi phu thuoc
(`psycopg`/`pytest`/`import-linter`) va khong co mang luc dung. Doi lai: phep
kiem o day **hep hon** mot thu vien that — no chi biet HS256, ⛔ khong biet
RS256/EdDSA. Neu ve sau can khoa cong khai thi ⛔ dung noi rong file nay, hay
lay thu vien.
"""
from __future__ import annotations

import base64
import binascii
import hashlib
import hmac
import json
import os
import time
from dataclasses import dataclass

BIEN_KHOA = "FLS_JWT_SECRET"

# Ban TRANG mot phan tu. ⛔ Them vao day la mo them mot duong tan cong.
ALG = "HS256"

# The dai qua la the bi nhoi. 8 KB du cho moi the that.
DAI_TOI_DA = 8192


class TheKhongHopLe(Exception):
    """⛔ Mot ly do duy nhat ra ngoai: *khong hop le*.

    Ly do CHI TIET (het han? sai chu ky? sai thuat toan?) di vao `chi_tiet` cho
    log noi bo — ⛔ khong tra ra ngoai HTTP. Noi cho nguoi go the biet ho sai o
    dau la giup ho do the.
    """

    def __init__(self, chi_tiet: str) -> None:
        super().__init__("the khong hop le")
        self.chi_tiet = chi_tiet


@dataclass(frozen=True)
class Nguoi:
    """Ai dang goi. `actor` LAY TU THE — ⛔ khong tu than yeu cau."""

    actor: str
    het_han: int
    vai: tuple[str, ...] = ()


def khoa() -> bytes:
    """⛔ NO neu khong co chia khoa. Khong co che do "tam cho qua"."""
    k = os.environ.get(BIEN_KHOA, "")
    if not k:
        raise RuntimeError(
            f"⛔ thieu {BIEN_KHOA} — cua doc ⛔ khong chay khi khong kiem duoc "
            f"the. Mot che do 'tam thoi cho qua het' la che do se song mai.")
    if len(k) < 32:
        raise RuntimeError(
            f"⛔ {BIEN_KHOA} chi dai {len(k)} ky tu — HS256 can >= 32. Khoa "
            f"ngan la khoa do duoc.")
    return k.encode()


def _b64(s: str) -> bytes:
    """Giai base64url. ⛔ NO neu co ky tu la — ⛔ khong bo qua am tham."""
    try:
        return base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    except (binascii.Error, ValueError) as e:
        raise TheKhongHopLe(f"base64 sai: {e}") from e


def _ky(dau: str, k: bytes) -> bytes:
    return hmac.new(k, dau.encode(), hashlib.sha256).digest()


def kiem(the: str, k: bytes | None = None, bay_gio: int | None = None) -> Nguoi:
    """Tra `Nguoi` neu the hop le, ⛔ nem `TheKhongHopLe` neu khong.

    ⛔ Khong co duong nao tra ve "chua ro" — moi duong hoac tra `Nguoi`, hoac nem.
    """
    k = k if k is not None else khoa()
    if not the or len(the) > DAI_TOI_DA:
        raise TheKhongHopLe(f"the rong hay dai qua ({len(the or '')})")
    phan = the.split(".")
    if len(phan) != 3:
        raise TheKhongHopLe(f"the co {len(phan)} phan, phai co 3")
    b_dau, b_than, b_chu_ky = phan

    try:
        dau = json.loads(_b64(b_dau))
        than = json.loads(_b64(b_than))
    except json.JSONDecodeError as e:
        raise TheKhongHopLe(f"JSON sai: {e}") from e
    if not isinstance(dau, dict) or not isinstance(than, dict):
        raise TheKhongHopLe("dau hay than khong phai doi tuong JSON")

    # ⓐ ban TRANG thuat toan — chan `alg: none` va chan doi sang thuat toan khac
    if dau.get("alg") != ALG:
        raise TheKhongHopLe(f"alg={dau.get('alg')!r}, chi nhan {ALG!r}")

    # ⓑ so sanh hang thoi gian
    if not hmac.compare_digest(_ky(f"{b_dau}.{b_than}", k), _b64(b_chu_ky)):
        raise TheKhongHopLe("chu ky khong khop")

    # ⓒ bat buoc co han
    exp = than.get("exp")
    if not isinstance(exp, int):
        raise TheKhongHopLe(f"thieu `exp` hay `exp` khong phai so nguyen "
                            f"({exp!r}) — the khong han la the ro vinh vien")
    t = int(bay_gio if bay_gio is not None else time.time())
    if exp <= t:
        raise TheKhongHopLe(f"het han {t - exp}s truoc")
    nbf = than.get("nbf")
    if isinstance(nbf, int) and nbf > t:
        raise TheKhongHopLe(f"chua toi luc dung ({nbf - t}s nua)")

    sub = than.get("sub")
    if not isinstance(sub, str) or not sub.strip():
        raise TheKhongHopLe("thieu `sub` — khong biet ai goi thi nhat ky vo nghia")

    vai = than.get("vai") or than.get("roles") or []
    if not isinstance(vai, list) or any(not isinstance(v, str) for v in vai):
        raise TheKhongHopLe("`vai` phai la danh sach chuoi")
    return Nguoi(actor=sub, het_han=exp, vai=tuple(vai))


def tu_dau_de(gia_tri: str | None) -> str:
    """Boc the tu de `Authorization: Bearer <the>`. ⛔ Chi nhan `Bearer`."""
    if not gia_tri:
        raise TheKhongHopLe("khong co de Authorization")
    phan = gia_tri.split(None, 1)
    if len(phan) != 2 or phan[0].lower() != "bearer":
        raise TheKhongHopLe("de Authorization khong phai dang `Bearer <the>`")
    return phan[1].strip()


def dong_the(than: dict, k: bytes, dau: dict | None = None) -> str:
    """⚠ **Chi dung trong bo test va cong cu phat the.**

    De trong ma nguon vi mot phep kiem khong co cach dong the tuong ung la mot
    phep kiem khong bai nao do duoc. Ham nay ⛔ khong duoc goi tu duong xu ly
    yeu cau — co bai quet ma nguon chan `cua.py` nhac ten no.
    """
    def e(o: dict) -> str:
        return base64.urlsafe_b64encode(
            json.dumps(o, separators=(",", ":")).encode()).rstrip(b"=").decode()

    p = f"{e(dau or {'alg': ALG, 'typ': 'JWT'})}.{e(than)}"
    return p + "." + base64.urlsafe_b64encode(_ky(p, k)).rstrip(b"=").decode()
