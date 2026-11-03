"""Doc tich luy tang dan, co retry, va MOT khoi loi khong pha ca luot doc.

Do that tren so song: mot luot chi lay duoc 4/7 khoi, co khoi truot 3/3 lan ke
ca khi cat lat 1.500 dong. Nen thiet ke "doc mot phat, loi thi bo het" khong
dung duoc voi so nay — phai tich luy va bao ro cai gi truot.

`lay` la ham duoc TIEM VAO (nhan mot khoang, tra du lieu). Nho vay module nay
la ham thuan, test khong can mang, va tang mang thay duoc ma khong sua o day.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable

MAC_DINH_LAN_THU = 3


def doc_dan(lay: Callable[[str], Any], khoang: Iterable[str],
            lan_thu: int = MAC_DINH_LAN_THU
            ) -> tuple[dict[str, Any], list[str]]:
    """Tra (`duoc`, `truot`). `truot` mang ly do bang chu cho tung khoang.

    ⛔ Khoang trung nhau bi chan: doc hai lan cung mot cho vua ton quota vua
    nguy — hai lan doc cach nhau co the ra hai gia tri khac nhau.
    """
    ds = list(khoang)
    trung = {k for k in ds if ds.count(k) > 1}
    if trung:
        raise ValueError(f"khoang trung nhau: {sorted(trung)}")

    duoc: dict[str, Any] = {}
    truot: list[str] = []
    for k in ds:
        loi_cuoi = ""
        for _ in range(max(1, lan_thu)):
            try:
                duoc[k] = lay(k)
                break
            except Exception as e:              # noqa: BLE001 — bao het, khong lua
                loi_cuoi = f"{type(e).__name__}: {e}"
        else:
            truot.append(f"{k} truot sau {lan_thu} lan: {loi_cuoi}")
    return duoc, truot
