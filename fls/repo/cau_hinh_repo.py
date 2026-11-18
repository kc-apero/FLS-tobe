# -*- coding: utf-8 -*-
"""Chỗ DUY NHẤT ghi/đọc **kho config chỉ-thêm có phiên bản** *(`C5` · `WO-142` ·
di trú `0027`)*.

⛔⛔ **Hai bảng `fls_cau_hinh_ban` / `fls_cau_hinh_dong` lưu CONFIG theo PHIÊN BẢN —
   ⛔ KHÔNG lưu số.** `IX.FX` *(tỷ giá tháng)* · `IX.HD` *(cây hợp đồng)* ·
   `IX.HD · IX.ORG` *(Mapping Master)* tới nay đọc từ **ảnh TĨNH đi cùng gói**; từ
   `C5` đọc từ **KHO**. Tuyến `/config/fx` · `/config/hd` ⛔ đổi hợp đồng — chỉ đổi
   **nguồn** *(F4 dùng lại nguyên)*.

★ **Bốn luật — chép khuôn `fls/repo/khai_cot.py` *(di trú `0016`)*:**

  ⓐ ⛔ **CHỈ-THÊM.** Nạp lại = ghi một `phien_ban` **MỚI**, ⛔ sửa bản cũ. Một dòng
    nạp tháng trước phải giải thích được bằng **config hiệu lực LÚC ẤY** — sửa đè là
    **viết lại lịch sử** *(`INV-I08`)*. Kho cưỡng chế bằng trigger
    `BEFORE UPDATE OR DELETE` + `BEFORE TRUNCATE` *(di trú `0027`)*.

  ⓑ ⛔ **ĐỦ cả cụm hoặc ⛔ KHÔNG GHI GÌ** — kiểm **trước** khi chạm kho *(ảnh qua
    `fx.kiem` / `hd.kiem`)*, rồi `fls_cau_hinh_ban` + mọi dòng trong **MỘT giao
    dịch**. Ghi một phần là **mất khoá trong im lặng**.

  ⓒ ⛔ **`luc` do MÁY đặt** *(`DEFAULT now()`)*, ⛔ người gọi ⛔ truyền vào được — ⛔
    thì `phien_ban` cao nhất và mốc mới nhất có thể ⛔ cùng chỉ về một bản.

  ⓓ ⛔ **⛔ Có bản MẶC ĐỊNH.** `bang` hợp lệ mà ⛔ ai nạp ⇒ `ChuaKhai`, ⛔ rơi về
    ảnh tĩnh, ⛔ đoán. Một mặc định im lặng là cơ chế đẻ ra lỗi *"⛔ ai thấy"*.

⚠ **`BangLa` *(nguồn lạ)* và `ChuaKhai` *(chưa khai)* là HAI câu khác nhau** *(cùng
  `khai_cot.NguonLa`/`KhongCoKhai`)*: *"⛔ có bảng config ấy"* ≠ *"có bảng, nhưng ⛔
  chưa ai nạp nó"*. Hai câu dẫn người dùng đi **hai đường sửa khác nhau**.

⭐ Tầng này ở `fls/repo/` *(hợp đồng `.importlinter` 10: kho config chỉ-thêm là việc
  CỦA đây, ⛔ của gói `fls.cau_hinh`)*. Dùng lại `fx.kiem`/`hd.kiem` để kiểm ảnh —
  ⛔ viết lại một bản kiểm thứ hai *(hai bản kiểm là hai chỗ để lệch)*.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from fls.cau_hinh import fx, hd

BANG_FX = fx.BANG                 # "IX.FX"
BANG_HD = hd.BANG                 # "IX.HD"
BANG_MM = hd.BANG_MM             # "IX.HD · IX.ORG" — ảnh Mapping Master

# ⭐ Danh mục `bang` config HỢP LỆ *(AP: IX.FX · IX.HD · IX.ORG · IX.PER · IX.VEN ·
#   IX.DRV · IX.ALR · IX.PL · IX.TMP — `.importlinter` khối `C5`)*. Một `bang` ⛔ ở
#   đây là **nguồn lạ** `BangLa`, ⛔ *"chưa khai"*. `C5` chỉ nạp THẬT ba cái đầu;
#   phần còn lại là các bước sau — nhưng chúng là `bang` CÓ THẬT, nên hỏi chúng khi
#   chưa nạp phải ra `ChuaKhai`, ⛔ `BangLa`.
BANG_HOP_LE: frozenset[str] = frozenset({
    "IX.FX", "IX.HD", "IX.ORG", "IX.PER", "IX.VEN", "IX.DRV",
    "IX.ALR", "IX.PL", "IX.TMP",
    BANG_MM,                     # ảnh MM mang CẢ `IX.HD` lẫn `IX.ORG`
})

# ⛔ Khoá META *(⛔ phải khoá dữ liệu)* — bắt đầu bằng `@`, ⛔ trùng `yyyymm`/mã HD.
_THANG_DAU = "@thang_dau"


class LoiCauHinh(Exception):
    """Gốc mọi lỗi tầng này. Mang `ma` để tầng cửa dịch ra HTTP."""

    ma = "FLS-CAUHINH-THIEU"


class BangLa(LoiCauHinh):
    """⛔ `bang` ⛔ trong danh mục config — **404** *(cùng `khai_cot.NguonLa`)*."""

    ma = "FLS-CAUHINH-BANG-LA"


class ChuaKhai(LoiCauHinh):
    """⛔ `bang` **có**, nhưng ⛔ chưa ai nạp — **409**, ⛔ 404 *(cùng `KhongCoKhai`)*."""

    ma = "FLS-CAUHINH-CHUA-KHAI"


@dataclass(frozen=True)
class BanCauHinh:
    """Một lần nạp *(một `phien_ban`)* của một `bang`, kèm các dòng theo thứ tự ghi."""

    bang: str
    phien_ban: int
    nguon: str
    checksum: str
    luc: datetime
    actor: str
    # ⭐ `True` khi checksum trùng phiên bản liền trước ⇒ nạp lại CÙNG nội dung
    #   *(vẫn là một `phien_ban` MỚI — chỉ-thêm — chỉ KHÔNG đổi nội dung)*.
    khong_doi: bool
    dong: tuple[tuple[str, Any], ...]


def _checksum(bang: str, cap: Iterable[tuple[str, Any]]) -> str:
    """sha256 nội dung CHUẨN HOÁ *(⛔ phụ thuộc thứ tự dòng)* — nạp lại cùng ảnh ⇒
    cùng checksum ⇒ `khong_doi`."""
    items = sorted(cap, key=lambda kv: kv[0])      # khoá DUY NHẤT ⇒ ⛔ so `gia_tri`
    noi = json.dumps([bang, [[k, v] for k, v in items]],
                     sort_keys=True, ensure_ascii=False,
                     separators=(",", ":"), default=str)
    return hashlib.sha256(noi.encode("utf-8")).hexdigest()


def _soi_bang(bang: str) -> None:
    if bang not in BANG_HOP_LE:
        raise BangLa(
            "⛔ `bang=%r` ⛔ trong danh mục config %s — nguồn lạ, ⛔ phải "
            "*'chưa khai'*" % (bang, sorted(BANG_HOP_LE)))


def nap(conn, bang: str, cap: list[tuple[str, Any]], *,
        nguon: str, actor: str) -> BanCauHinh:
    """Ghi một phiên bản MỚI của `bang`. ⛔ Sửa bản cũ *(trigger chặn)*.

    ⭐ `pg_advisory_xact_lock` theo `bang` **xếp hàng** phép cấp `phien_ban` cho
      riêng `bang` ấy *(cùng vai `SELECT … FOR UPDATE` của `khai_cot.ghi_khai`)*:
      ⛔ có khoá thì hai người nạp cùng lúc cùng đọc `max(phien_ban)`, và
      `UNIQUE(bang, phien_ban)` chặn người thứ hai bằng **lỗi trùng khoá** khó đọc.
    """
    _soi_bang(bang)
    if not str(actor or "").strip():
        raise LoiCauHinh(
            "⛔ thiếu `actor`. Nạp config là **hành vi của người** — một bản nạp "
            "⛔ ai đứng tên thì ⛔ ai giải thích được vì sao config lại đổi")

    checksum = _checksum(bang, cap)
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(hashtext(%s)::bigint)",
                        (bang,))
            cur.execute(
                "SELECT coalesce(max(phien_ban), 0) FROM fls_cau_hinh_ban "
                "WHERE bang = %s", (bang,))
            ver = int(cur.fetchone()[0]) + 1
            cur.execute(
                "SELECT checksum FROM fls_cau_hinh_ban WHERE bang = %s "
                "ORDER BY phien_ban DESC LIMIT 1", (bang,))
            r = cur.fetchone()
            ck_truoc = r[0] if r else None

            cur.execute(
                "INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, "
                "actor) VALUES (%s,%s,%s,%s,%s) RETURNING ban_id, luc",
                (bang, ver, nguon, checksum, actor))
            ban_id, luc = cur.fetchone()
            # ⛔ ⛔ `psycopg.types.json.Json` *(import mức module)*: nó kéo `psycopg`
            #    vào đồ thị ⇒ `fls.api → fls.repo.cau_hinh_repo → psycopg` phá hợp
            #    đồng `.importlinter` 1 *(mọi repo khác ⛔ import `psycopg`, chỉ nhận
            #    `conn` TRUYỀN VÀO)*. ⇒ `json.dumps` + ép `::jsonb` ở SQL, ⛔ chạm
            #    `psycopg`. Đọc lại thì `jsonb` tự về Python — ⛔ cần Json.
            cur.executemany(
                "INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) "
                "VALUES (%s,%s,%s::jsonb)",
                [(ban_id, k, json.dumps(v, ensure_ascii=False)) for k, v in cap])

    return BanCauHinh(bang=bang, phien_ban=ver, nguon=nguon, checksum=checksum,
                      luc=luc, actor=actor,
                      khong_doi=ck_truoc is not None and ck_truoc == checksum,
                      dong=tuple(cap))


def _doc_ban(conn, bang: str) -> BanCauHinh:
    """Phiên bản **mới nhất** của `bang`. `BangLa` ⇒ 404, `ChuaKhai` ⇒ 409."""
    _soi_bang(bang)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT ban_id, phien_ban, nguon, checksum, actor, luc "
            "FROM fls_cau_hinh_ban WHERE bang = %s "
            "ORDER BY phien_ban DESC LIMIT 1", (bang,))
        r = cur.fetchone()
        if r is None:
            raise ChuaKhai(
                "⛔ `bang=%r` ⛔ CHƯA có phiên bản nào trong kho config. ⛔ "
                "Không rơi về ảnh tĩnh — nạp bằng `fls.repo.cau_hinh_repo.nap`"
                % bang)
        ban_id, ver, nguon, checksum, actor, luc = r
        cur.execute(
            "SELECT khoa, gia_tri FROM fls_cau_hinh_dong WHERE ban_id = %s "
            "ORDER BY dong_id", (ban_id,))
        dong = tuple((k, v) for k, v in cur.fetchall())
    return BanCauHinh(bang=bang, phien_ban=ver, nguon=nguon, checksum=checksum,
                      luc=luc, actor=actor, khong_doi=False, dong=dong)


# ── IX.FX — tỷ giá tháng ──────────────────────────────────────────────────────
def nap_ix_fx(conn, duong: str, *, actor: str, thang_dau: int,
              nguon: str | None = None) -> BanCauHinh:
    """Nạp ảnh `ix_fx.json` *(DT2, đường TRUYỀN VÀO)* ⇒ phiên bản mới của `IX.FX`.

    ⛔ Ảnh DT2 khoá bằng cột `Month` ⇒ **ánh xạ `Month → yyyymm`** *(Q3: C5 ánh
      xạ)*, bỏ `thu_tu`, rồi **kiểm bằng CHÍNH `fx.kiem` của C1** *(⛔ bản chép)*.
    """
    van = Path(duong).read_text(encoding="utf-8")
    anh = json.loads(van)
    dong = [{"yyyymm": r["Month"], **{te: r[te] for te in fx.TIEN_TE}}
            for r in anh["dong"]]
    b = fx.kiem(dong, thang_dau=thang_dau, nguon=nguon or duong)
    if b.trung:
        raise LoiCauHinh(
            "⛔ ảnh có tháng TRÙNG %s — kho lưu theo khoá `yyyymm` nên ⛔ nhận "
            "hai dòng cùng tháng *(sửa ảnh ở C1/DT2)*" % list(b.trung))
    cap: list[tuple[str, Any]] = [(_THANG_DAU, int(thang_dau))]
    cap += [(str(d.yyyymm), {te: str(d.ty_gia[te]) for te in fx.TIEN_TE})
            for d in b.ky]
    return nap(conn, BANG_FX, cap, nguon=nguon or duong, actor=actor)


def doc_fx(conn) -> fx.BangFX:
    """`IX.FX` phiên bản mới nhất, dựng lại **qua `fx.kiem`** *(kiểm cả lúc ĐỌC —
    khuôn `khai_cot.doc_khai`)*. `ChuaKhai` nếu kho rỗng."""
    ban = _doc_ban(conn, BANG_FX)
    thang_dau: int | None = None
    dong: list[Mapping[str, Any]] = []
    for khoa, gt in ban.dong:
        if khoa == _THANG_DAU:
            thang_dau = int(gt)
        else:
            dong.append({"yyyymm": int(khoa), **gt})
    return fx.kiem(dong, thang_dau=thang_dau, nguon=ban.nguon)


# ── IX.HD — cây hợp đồng (ATL) ────────────────────────────────────────────────
def nap_ix_hd(conn, duong: str, *, actor: str,
              nguon: str | None = None) -> BanCauHinh:
    """Nạp ảnh ATL `atl_cay.json` *(DT3, đường TRUYỀN VÀO)* ⇒ phiên bản mới của
    `IX.HD`. Kiểm bằng CHÍNH `hd.doc_van_ban`/`hd.kiem` của C4."""
    van = Path(duong).read_text(encoding="utf-8")
    cay = hd.doc_van_ban(van, nguon=nguon or duong)
    cap = [(n.ma, {"ten": n.ten, "cha": n.cha, "cap": n.cap, "nhom": n.nhom,
                   "dong_sheet": n.dong_sheet, "thu_tu": n.thu_tu})
           for n in cay.nut]
    return nap(conn, BANG_HD, cap, nguon=nguon or duong, actor=actor)


def doc_hd(conn) -> hd.CayHD:
    """`IX.HD` phiên bản mới nhất, dựng lại **qua `hd.kiem`**. `ChuaKhai` nếu rỗng."""
    ban = _doc_ban(conn, BANG_HD)
    dong = [{"ma": k, "ten": v["ten"], "cha": v["cha"], "cap": v["cap"],
             "nhom": v["nhom"], "dong_sheet": v["dong_sheet"],
             "thu_tu": v["thu_tu"]}
            for k, v in ban.dong]
    return hd.kiem(dong, nguon=ban.nguon)


# ── IX.HD · IX.ORG — Mapping Master ───────────────────────────────────────────
def nap_mapping_master(conn, duong: str, *, actor: str,
                       nguon: str | None = None) -> BanCauHinh:
    """Nạp ảnh Mapping Master *(DT3, đường TRUYỀN VÀO)* ⇒ phiên bản mới của
    `IX.HD · IX.ORG`.

    ⛔⛔ **Kho CHỈ lưu khoá cần cho tuyến *(`hd_code`)*** *(AC-6b)*: ảnh gói mang
       bảng phụ `tho` *(84 hàng, 51 hàng có chuỗi ≥ 6 chữ số)* mà tuyến ⛔ đọc ⇒
       ⛔ một ô nào của `tho` lọt vào kho. Kiểm bằng CHÍNH `hd.doc_mm_van_ban`
       *(73 mã, ⛔ trùng)*."""
    van = Path(duong).read_text(encoding="utf-8")
    ma = hd.doc_mm_van_ban(van, nguon=nguon or duong)      # kiểm: 73 mã, ⛔ trùng
    anh = json.loads(van)
    raw: dict[str, tuple[str, int]] = {}
    for i, r in enumerate(anh["dong"], start=1):
        c, _ = hd._chu(r.get("hd_code"))
        if c:
            raw[hd._ma_mm(c)] = (c, i)
    cap = [(m, {"hd_code": raw[m][0], "thu_tu": raw[m][1]}) for m in ma]
    return nap(conn, BANG_MM, cap, nguon=nguon or duong, actor=actor)


@dataclass(frozen=True)
class KhoMM:
    """Mapping Master đọc từ kho: `nguon` *(truy nguồn)* + `ma` *(mã HD, thứ tự ảnh)*."""

    nguon: str
    ma: tuple[str, ...]


def doc_mm(conn) -> KhoMM:
    """Mã HD của Mapping Master *(phiên bản mới nhất, theo thứ tự ảnh)* — `C4` DÙNG
    để LIỆT KÊ chênh với ATL. `ChuaKhai` nếu rỗng."""
    ban = _doc_ban(conn, BANG_MM)
    xep = sorted(ban.dong, key=lambda kv: int(kv[1].get("thu_tu", 0)))
    return KhoMM(nguon=ban.nguon, ma=tuple(k for k, _ in xep))
