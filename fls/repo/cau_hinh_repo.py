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
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from fls.cau_hinh import fx, hd, ky

BANG_FX = fx.BANG                 # "IX.FX"
BANG_HD = hd.BANG                 # "IX.HD"
BANG_MM = hd.BANG_MM             # "IX.HD · IX.ORG" — ảnh Mapping Master
BANG_PER = ky.BANG               # "IX.PER" — lịch kỳ (`C6`)

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


class BanHong(LoiCauHinh):
    """Một bản config trong kho **⛔ ĐỌC ra được** *(thiếu trường · sai hình)* — **500
    CÓ TÊN**, ⛔ `KeyError`/`FLS-INTERNAL` trần *(`C5-R1-04`)*.

    ⛔ xảy ra qua `nap` *(nay kiểm nội dung TRƯỚC khi ghi — kho chỉ-thêm ⛔ có đường
    lùi)*; chỉ tới khi có bản ghi **THẲNG SQL** ⛔ qua `nap`. Phục hồi = nạp một bản
    TỐT kế tiếp *(bản mới nhất thắng)*. Tuyến dịch mã này ⇒ người dựng hệ biết đây là
    **dữ liệu kho hỏng**, ⛔ một lỗi máy ngẫu nhiên."""

    ma = "FLS-CAUHINH-BAN-HONG"


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


# ── Dựng lại ĐỐI TƯỢNG miền từ `cap` đã lưu — DÙNG CHUNG cho ① `nap` *(kiểm TRƯỚC khi
#    ghi — kho chỉ-thêm ⛔ có đường lùi)* và ② `doc_fx`/`doc_hd` *(kiểm cả lúc ĐỌC —
#    khuôn `khai_cot.doc_khai`)*. MỘT lõi, ⛔ hai bản kiểm *(docstring tệp)*. `.get()` ⇒
#    bản thiếu trường ra `LoiFX`/`LoiHD` CÓ TÊN, ⛔ `KeyError` trần *(`C5-R1-04`)*.
def _fx_tu_cap(cap: Iterable[tuple[str, Any]], nguon: str) -> fx.BangFX:
    thang_dau: Any = None
    dong: list[Any] = []
    for khoa, gt in cap:
        if khoa == _THANG_DAU:
            thang_dau = gt                        # fx.kiem tự kiểm (None ⇒ LoiFX)
        elif isinstance(gt, Mapping):
            dong.append({"yyyymm": khoa, **gt})
        else:
            dong.append(gt)                       # ⛔ Mapping ⇒ fx.kiem bắt "⛔ đối tượng"
    return fx.kiem(dong, thang_dau=thang_dau, nguon=nguon)


def _hd_tu_cap(cap: Iterable[tuple[str, Any]], nguon: str) -> hd.CayHD:
    dong: list[Any] = []
    for k, v in cap:
        if not isinstance(v, Mapping):
            dong.append(v)                        # ⛔ Mapping ⇒ hd.kiem bắt "⛔ đối tượng"
            continue
        r = {"ma": k, "ten": v.get("ten"), "cha": v.get("cha"),
             "cap": v.get("cap"), "nhom": v.get("nhom"),
             "dong_sheet": v.get("dong_sheet")}
        if "thu_tu" in v:                         # `thu_tu` TÙY CHỌN ở `hd.kiem`
            r["thu_tu"] = v["thu_tu"]
        dong.append(r)
    return hd.kiem(dong, nguon=nguon)


def _kiem_mm(cap: Iterable[tuple[str, Any]]) -> None:
    """MM ⛔ có lõi `kiem` dựng-lại riêng *(`hd.doc_mm_van_ban` ăn VĂN BẢN)* ⇒ kiểm HÌNH
    đã lưu: mỗi `gia_tri` ĐÚNG tập khoá `{hd_code, thu_tu}`, `hd_code` ⛔ rỗng, `thu_tu`
    là số *(AC-6b: ⛔ ô bảng phụ `tho` lọt vào kho)*."""
    loi: list[str] = []
    for m, v in cap:
        if not isinstance(v, Mapping) or set(v) != {"hd_code", "thu_tu"}:
            loi.append("%r: `gia_tri` phải đúng {hd_code, thu_tu}, đo %r"
                       % (m, sorted(v) if isinstance(v, Mapping) else type(v).__name__))
            continue
        if not str(v.get("hd_code") or "").strip():
            loi.append("%r: hd_code rỗng" % m)
        try:
            int(v["thu_tu"])
        except (TypeError, ValueError):
            loi.append("%r: thu_tu ⛔ số: %r" % (m, v.get("thu_tu")))
    if loi:
        raise LoiCauHinh("⛔ ảnh Mapping Master sai hình:\n  - " + "\n  - ".join(loi))


def _kiem_noi_dung(bang: str, cap: list[tuple[str, Any]]) -> None:
    """⛔ GHI một bản RỖNG/BẨN — kiểm **TRƯỚC** khi chạm kho *(khuôn ⓑ; kho chỉ-thêm
    ⛔ có đường lùi ⇒ một bản ghi sai là **vĩnh viễn** và thành bản MỚI NHẤT ⛔ xoá
    được)*. Dùng lại CHÍNH `fx.kiem`/`hd.kiem` *(⛔ một bản kiểm thứ hai)*; `bang` khác
    chỉ kiểm HÌNH chung *(rỗng · khoá rỗng · khoá trùng)*."""
    if not cap:
        raise LoiCauHinh(
            "⛔ nạp bản RỖNG cho %r — kho chỉ-thêm ⛔ nhận bản 0 dòng *(nó sẽ thành bản "
            "mới nhất, một mặc định im lặng ⛔ xoá được — khuôn ⓓ)*" % bang)
    khoa = [k for k, _ in cap]
    if any(not str(k or "").strip() for k in khoa):
        raise LoiCauHinh("⛔ có khoá RỖNG trong bản nạp %r" % bang)
    trung = sorted({k for k in khoa if khoa.count(k) >= 2})
    if trung:
        raise LoiCauHinh(
            "⛔ khoá TRÙNG %s trong một bản %r — hai câu trả lời cho một câu hỏi "
            "*(cùng luật `UNIQUE(ban_id, khoa)`)*" % (trung, bang))
    if bang == BANG_FX:
        _fx_tu_cap(cap, nguon="(kiem truoc khi ghi)")
    elif bang == BANG_HD:
        _hd_tu_cap(cap, nguon="(kiem truoc khi ghi)")
    elif bang == BANG_MM:
        _kiem_mm(cap)
    elif bang == BANG_PER:
        ky.kiem(dict(cap), nguon="(kiem truoc khi ghi)")   # `LoiKy` CÓ TÊN, ⛔ bọc lại


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
    # ⛔⛔ Kho chỉ-thêm ⛔ có đường lùi ⇒ KIỂM nội dung TRƯỚC khi chạm kho *(`C5-R1-04`:
    #    `nap` công khai từng nhận bản rỗng/bẩn ⇒ bản mới nhất ⛔ xoá được, rồi `doc_*`
    #    nổ `KeyError`/`500` lúc đọc)*. Dùng lại `fx.kiem`/`hd.kiem`.
    _kiem_noi_dung(bang, cap)

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
    khuôn `khai_cot.doc_khai`)*. `ChuaKhai` nếu kho rỗng; bản BẨN ⇒ `BanHong` CÓ TÊN
    *(⛔ `LoiFX` trần lọt tuyến thành `500 FLS-INTERNAL` — `C5-R1-04`)*."""
    ban = _doc_ban(conn, BANG_FX)
    try:
        return _fx_tu_cap(ban.dong, ban.nguon)
    except fx.LoiFX as e:
        raise BanHong(
            "⛔ bản `IX.FX` phiên bản %s trong kho ⛔ ĐỌC ra được *(⛔ qua `nap`?)*"
            % ban.phien_ban) from e


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
    """`IX.HD` phiên bản mới nhất, dựng lại **qua `hd.kiem`**. `ChuaKhai` nếu rỗng; bản
    BẨN *(thiếu trường)* ⇒ `BanHong` CÓ TÊN *(⛔ `KeyError: 'cha'` ⇒ `500 FLS-INTERNAL`
    — `C5-R1-04`)*."""
    ban = _doc_ban(conn, BANG_HD)
    try:
        return _hd_tu_cap(ban.dong, ban.nguon)
    except hd.LoiHD as e:
        raise BanHong(
            "⛔ bản `IX.HD` phiên bản %s trong kho ⛔ ĐỌC ra được *(⛔ qua `nap`?)*"
            % ban.phien_ban) from e


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
    try:
        xep = sorted(ban.dong, key=lambda kv: int(kv[1]["thu_tu"]))
        ma = tuple(k for k, _ in xep)
    except (KeyError, TypeError, ValueError, AttributeError) as e:
        raise BanHong(
            "⛔ bản Mapping Master phiên bản %s trong kho ⛔ ĐỌC ra được "
            "*(⛔ qua `nap`?)*" % ban.phien_ban) from e
    return KhoMM(nguon=ban.nguon, ma=ma)


# ── IX.PER — lịch kỳ (`C6` · `WO-152`) ────────────────────────────────────────
def nap_ix_per(conn, *, actor: str, ngay_dau: "str | date", luat: str = ky.LUAT_A,
               nguon: str) -> BanCauHinh:
    """Nạp `IX.PER` ⇒ phiên bản mới. `ngay_dau` là **GIÁ TRỊ CẤU HÌNH do người gọi khai**
    *(⛔ gõ cứng ở mã; `nguon` ⛔ rỗng — truy được số đến từ đâu)*. Kiểm bằng CHÍNH
    `ky.kiem` TRƯỚC khi ghi: luật `B` ⇒ `LoiKy LUAT_CHUA_KY`, ngày hỏng ⇒ `PER_HONG`."""
    if not str(nguon or "").strip():
        raise LoiCauHinh("⛔ thiếu `nguon` cho `IX.PER` — ngày đầu phải truy được nguồn")
    ngay = ngay_dau.isoformat() if isinstance(ngay_dau, date) else ngay_dau
    cap: list[tuple[str, Any]] = [(ky.KHOA_NGAY_DAU, {"ngay": ngay}),
                                  (ky.KHOA_LUAT, {"ma": luat})]
    return nap(conn, BANG_PER, cap, nguon=nguon, actor=actor)


def doc_per(conn) -> ky.LichKy:
    """`IX.PER` phiên bản mới nhất, dựng lại **qua `ky.kiem`**. `ChuaKhai` nếu kho chưa nạp;
    bản bẩn ⇒ `BanHong` CÓ TÊN; luật `B` trong kho ⇒ `LoiKy LUAT_CHUA_KY` *(⛔ nuốt)*."""
    ban = _doc_ban(conn, BANG_PER)
    try:
        return ky.kiem(dict(ban.dong), nguon=ban.nguon)
    except ky.LoiKy as e:
        if e.ma == ky.LUAT_CHUA_KY:
            raise
        raise BanHong(
            "⛔ bản `IX.PER` phiên bản %s trong kho ⛔ ĐỌC ra được: %s" % (ban.phien_ban, e)
        ) from e
