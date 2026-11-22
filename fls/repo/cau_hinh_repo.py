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
from dataclasses import dataclass, replace
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

from fls.cau_hinh import ban_ky, dong_pl, fx, hd, ky, luat_pb, to_chuc, vendor
from fls.repo import ghi_tay

BANG_FX = fx.BANG                 # "IX.FX"
BANG_HD = hd.BANG                 # "IX.HD"
BANG_MM = hd.BANG_MM             # "IX.HD · IX.ORG" — ảnh Mapping Master
BANG_PER = ky.BANG               # "IX.PER" — lịch kỳ (`C6`)
BANG_VEN = vendor.BANG           # "IX.VEN" — vendor · network · cách tính (`C9`)
BANG_ORG = to_chuc.BANG          # "IX.ORG" — CDT Correct + TK→LE (`C8`)
BANG_PL = dong_pl.BANG           # "IX.PL" — dòng PL là biểu thức trên cây HD (`C12`)
BANG_ALR = luat_pb.BANG          # "IX.ALR" — luật phân bổ hiệu lực theo kỳ + cờ (`C11`)
BANG_KY_FX = "IX.FX · KY"        # bản KÝ tháng của IX.FX (`C7`) — mỗi bản = mọi chữ ký tới lúc ấy

# ⭐ Danh mục `bang` config HỢP LỆ *(AP: IX.FX · IX.HD · IX.ORG · IX.PER · IX.VEN ·
#   IX.DRV · IX.ALR · IX.PL · IX.TMP — `.importlinter` khối `C5`)*. Một `bang` ⛔ ở
#   đây là **nguồn lạ** `BangLa`, ⛔ *"chưa khai"*. `C5` chỉ nạp THẬT ba cái đầu;
#   phần còn lại là các bước sau — nhưng chúng là `bang` CÓ THẬT, nên hỏi chúng khi
#   chưa nạp phải ra `ChuaKhai`, ⛔ `BangLa`.
BANG_HOP_LE: frozenset[str] = frozenset({
    "IX.FX", "IX.HD", "IX.ORG", "IX.PER", "IX.VEN", "IX.DRV",
    "IX.ALR", "IX.PL", "IX.TMP", BANG_KY_FX,
    BANG_MM,                     # ảnh MM mang CẢ `IX.HD` lẫn `IX.ORG`
})

# ⛔ Khoá META *(⛔ phải khoá dữ liệu)* — bắt đầu bằng `@`, ⛔ trùng `yyyymm`/mã HD.
_THANG_DAU = "@thang_dau"
_CDT1 = "@cdt1"          # `IX.VEN`: danh mục 7 CDT1 (meta, ⛔ khoá dữ liệu)


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


def _ven_tu_cap(cap: Iterable[tuple[str, Any]], nguon: str) -> vendor.BangVen:
    cdt1: Any = None
    dong: list[Any] = []
    for khoa, gt in cap:
        if khoa == _CDT1:
            cdt1 = gt
        elif isinstance(gt, Mapping):
            dong.append({"dong_sheet": khoa, **gt})
        else:
            dong.append(gt)                       # ⛔ Mapping ⇒ vendor.kiem bắt "⛔ đối tượng"
    return vendor.kiem(dong, cdt1=cdt1 if isinstance(cdt1, list) else [], nguon=nguon)


def _alr_tu_cap(cap: Iterable[tuple[str, Any]], nguon: str) -> luat_pb.BangALR:
    dong: list[Any] = []
    for khoa, gt in cap:
        dong.append({"khoa": khoa, **gt} if isinstance(gt, Mapping) else gt)
    return luat_pb.kiem(dong, nguon=nguon)       # ⛔ Mapping ⇒ kiem bắt "⛔ đối tượng"


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


def _kiem_org(cap: Iterable[tuple[str, Any]]) -> None:
    """`IX.ORG` ⇒ mỗi khoá `cdt:…` mang `{cdt1}`, `tk:…` mang `{le}`; ⛔ khoá khác."""
    loi: list[str] = []
    for k, v in cap:
        truong = ("cdt1" if k.startswith(to_chuc.TIEN_TO_CDT)
                  else "le" if k.startswith(to_chuc.TIEN_TO_TK) else None)
        if truong is None or not isinstance(v, Mapping) or set(v) != {truong} \
                or not str(v.get(truong) or "").strip():
            loi.append("%r: khoá phải `cdt:`/`tk:` với gia_tri {cdt1}/{le} ⛔ rỗng" % k)
    if loi:
        raise LoiCauHinh("⛔ bản IX.ORG sai hình:\n  - " + "\n  - ".join(loi))


def _pl_tu_cap(cap: Iterable[tuple[str, Any]]) -> dict[str, str]:
    dn: dict[str, str] = {}
    for k, v in cap:
        bt = v.get("bieu_thuc") if isinstance(v, Mapping) else None
        dn[k] = bt if isinstance(bt, str) else ""       # "" ⇒ `PL_CU_PHAP` (rỗng)
    return dn


def _kiem_pl(cap: Iterable[tuple[str, Any]], cay: hd.CayHD | None = None) -> None:
    """`IX.PL`: kiểm bằng CHÍNH `dong_pl.kiem_dinh_nghia`; lỗi CÓ TÊN `PL_*` đi vào câu."""
    try:
        dong_pl.kiem_dinh_nghia(_pl_tu_cap(cap), cay)
    except dong_pl.LoiPL as e:
        raise LoiCauHinh("⛔ bản IX.PL sai: %s" % e) from e


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
    elif bang == BANG_VEN:
        _ven_tu_cap(cap, nguon="(kiem truoc khi ghi)")
    elif bang == BANG_ORG:
        _kiem_org(cap)
    elif bang == BANG_ALR:
        _alr_tu_cap(cap, nguon="(kiem truoc khi ghi)")    # `LoiLuatPB` CÓ TÊN, ⛔ bọc lại
    elif bang == BANG_PER:
        ky.kiem(dict(cap), nguon="(kiem truoc khi ghi)")   # `LoiKy` CÓ TÊN, ⛔ bọc lại
    elif bang == BANG_PL:
        _kiem_pl(cap)


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


# ── IX.PL — dòng PL (biểu thức trên cây HD) ──────────────────────────────────
def nap_ix_pl(conn, *, actor: str, dinh_nghia: Mapping[str, str] | None = None,
              cay: hd.CayHD | None = None) -> BanCauHinh:
    """Nạp định nghĩa dòng PL *(mặc định `dong_pl.DINH_NGHIA`)* ⇒ phiên bản mới `IX.PL`.
    Kiểm cú pháp TRƯỚC khi ghi; có `cay` thì kiểm luôn mã ∈ cây HD *(`PL_MA_LA`)*."""
    dn = dong_pl.DINH_NGHIA if dinh_nghia is None else dinh_nghia
    cap = [(pl, {"bieu_thuc": bt}) for pl, bt in dn.items()]
    _kiem_pl(cap, cay)
    return nap(conn, BANG_PL, cap, nguon="fls.cau_hinh.dong_pl", actor=actor)


def doc_pl(conn) -> dict[str, str]:
    """`IX.PL` mới nhất ⇒ `{PLn: biểu thức}`. Bản BẨN ⇒ `BanHong` có tên."""
    ban = _doc_ban(conn, BANG_PL)
    dn = _pl_tu_cap(ban.dong)
    try:
        dong_pl.kiem_dinh_nghia(dn)
    except dong_pl.LoiPL as e:
        raise BanHong("⛔ bản `IX.PL` phiên bản %s ⛔ đọc được: %s"
                      % (ban.phien_ban, e)) from e
    return dn


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


# ── IX.VEN — vendor · network · cách tính (`C9`) ──────────────────────────────
def nap_ix_ven(conn, duong: str, *, duong_cdt1: str, actor: str,
               nguon: str | None = None) -> BanCauHinh:
    """Nạp ảnh DT8 `ix_ven.json` + danh mục CDT1 *(lấy từ ảnh `cdt_correct.json` — các
    `cdt1_chuan` KHÁC NHAU, ⛔ gõ cứng; cả hai đường TRUYỀN VÀO)* ⇒ phiên bản mới của `IX.VEN`.
    Khoá kho = `dong_sheet`; kiểm bằng CHÍNH `vendor.kiem`."""
    def chu(o: Any) -> Any:
        return o.get("chu") if isinstance(o, Mapping) else o
    anh = json.loads(Path(duong).read_text(encoding="utf-8"))
    cdt_anh = json.loads(Path(duong_cdt1).read_text(encoding="utf-8"))
    cdt1 = sorted({chu(r["cdt1_chuan"]) for r in cdt_anh["dong"]})
    cap: list[tuple[str, Any]] = [(_CDT1, cdt1)]
    for r in anh["dong"]:
        cap.append((str(r["dong_sheet"]), {
            "thu_tu": r["thu_tu"], "No": chu(r["No"]), "vendor": chu(r["vendor"]),
            "network": chu(r["network"]), "account": chu(r["account"]),
            "pct": chu(r["pct"]), "cashin_month": chu(r["cashin_month"]),
            "cashin_day": chu(r["cashin_day"]), "cach_tinh": chu(r["cach_tinh"]),
            "so": chu(r.get("so", "GI"))}))      # DT9b: ảnh DT8 cũ ⛔ có `so` ⇒ GI
    return nap(conn, BANG_VEN, cap, nguon=nguon or duong, actor=actor)


def doc_ven(conn, so: str | None = None) -> vendor.BangVen:
    """`IX.VEN` mới nhất, dựng lại **qua `vendor.kiem`**. `ChuaKhai` nếu rỗng; bản BẨN ⇒
    `BanHong` CÓ TÊN. ⭐ DT9b: `so=None` ⇒ MỌI sổ *(GI · OMC · SC · PS)*; `so="GI"` ⇒ chỉ dòng sổ ấy
    *(engine H9/H10 — `theo_so`; sổ lạ/0 dòng ⇒ `LoiVen`)*."""
    ban = _doc_ban(conn, BANG_VEN)
    try:
        b = _ven_tu_cap(ban.dong, ban.nguon)
    except vendor.LoiVen as e:
        raise BanHong(
            "⛔ bản `IX.VEN` phiên bản %s trong kho ⛔ ĐỌC ra được *(⛔ qua `nap`?)*"
            % ban.phien_ban) from e
    return b if so is None else b.theo_so(so)
# ── IX.ORG — CDT Correct + TK→LE (`C8` · `WO-176`) ───────────────────────────
def nap_ix_org(conn, duong_cdt: str, duong_mm: str, *, actor: str,
               nguon: str | None = None) -> BanCauHinh:
    """Nạp ảnh `cdt_correct.json` + Mapping Master `tho` ⇒ phiên bản mới của `IX.ORG`
    *(kiểm bằng CHÍNH `to_chuc.doc_anh`; kho CHỈ giữ TK pháp nhân — ⛔ TK cá nhân)*."""
    van_cdt = Path(duong_cdt).read_text(encoding="utf-8")
    van_mm = Path(duong_mm).read_text(encoding="utf-8")
    ten = nguon or f"{duong_cdt} + {duong_mm}"
    cdt = to_chuc.doc_cdt_correct(van_cdt, nguon=ten)
    tk = to_chuc.doc_tk_le(van_mm, nguon=ten)
    cap: list[tuple[str, Any]] = [(to_chuc.TIEN_TO_CDT + n, {"cdt1": c}) for n, c in cdt]
    cap += [(to_chuc.TIEN_TO_TK + t, {"le": le}) for t, le in tk]
    return nap(conn, BANG_ORG, cap, nguon=ten, actor=actor)


def doc_org(conn) -> to_chuc.ToChuc:
    """`IX.ORG` mới nhất. `ChuaKhai` nếu kho chưa nạp — ⛔ rơi về `SHQ2`."""
    ban = _doc_ban(conn, BANG_ORG)
    try:
        cdt = tuple((k[len(to_chuc.TIEN_TO_CDT):], v["cdt1"]) for k, v in ban.dong
                    if k.startswith(to_chuc.TIEN_TO_CDT))
        tk = tuple((k[len(to_chuc.TIEN_TO_TK):], v["le"]) for k, v in ban.dong
                   if k.startswith(to_chuc.TIEN_TO_TK))
    except (KeyError, TypeError) as e:
        raise BanHong("⛔ bản `IX.ORG` phiên bản %s trong kho ⛔ ĐỌC ra được"
                      % ban.phien_ban) from e
    return to_chuc.dung(cdt, tk, nguon=ban.nguon)


def cdt_cua_ghi(conn, itl_id: int, cdt_nguon: str, *, actor: str) -> to_chuc.KetQuaCDT:
    """CDT1 của `cdt_nguon` theo `IX.ORG` trong kho. CDT **lạ** ⇒ MỘT sự kiện hàng chờ
    `evt_type='CDT_LA'` gắn dòng `itl_id` *(⛔ trả `SHQ2`)*; gọi lại cùng `(itl_id, CDT)`
    ⛔ ghi thêm. ⛔ `reason` *(sổ ⛔ trộn việc máy vào cú bấm người — `danh_muc_actor`)*."""
    if not str(actor or "").strip():
        raise LoiCauHinh("⛔ thiếu `actor` cho sự kiện CDT_LA")
    r = to_chuc.cdt_cua(doc_org(conn), cdt_nguon)
    if r.la:
        ly_do = "CDT lạ %r — ⛔ có trong CDT Correct, ⛔ mặc định SHQ2" % (cdt_nguon,)
        with conn.transaction():
            ghi_tay.ghi_cdt_la(conn, itl_id=itl_id, ly_do=ly_do, actor=actor)
    return r


# ── IX.ALR — luật phân bổ hiệu lực theo kỳ + cờ TẮT (`C11` · `WO-180`) ───────────────
def nap_ix_alr(conn, duong_mm: str, *, tu_ky: int, actor: str,
               nguon: str | None = None) -> BanCauHinh:
    """Nạp luật phân bổ từ ảnh Mapping Master DT3 `mapping_master_cfg.json` *(đường TRUYỀN VÀO;
    bảng `fls_mapping_master` của cụm đo 0 dòng ⇒ ⛔ nguồn)* ⇒ phiên bản mới của `IX.ALR`.

    `tu_ky` *(`yyyymm`)* là **GIÁ TRỊ CẤU HÌNH do người gọi khai** *(⛔ gõ cứng ở mã)*: luật hiệu
    lực từ kỳ ấy; các lần nạp TÍCH LUỸ *(`C11-R1-01`: bản mới = bản trước + mốc mới)*, đọc theo kỳ
    bằng `luat_cua`. Mọi luật `bat = false` *(D2)*. Kiểm bằng CHÍNH `luat_pb.dung_tu_mm`/`kiem`."""
    def chu(o: Any) -> Any:
        return o.get("chu") if isinstance(o, Mapping) else o
    anh = json.loads(Path(duong_mm).read_text(encoding="utf-8"))
    mm = [{"hd_code": chu(r.get("hd_code")), "need_cfa2": chu(r.get("need_cfa2")),
           "method_cfa2": chu(r.get("method_cfa2"))} for r in anh["dong"]]
    moi = [(luat_pb.khoa_cua(r["hd"], r["tu_ky"]), dict(r))
           for r in luat_pb.dung_tu_mm(mm, tu_ky=tu_ky)]     # `tu_ky` hỏng ⇒ `kiem` trong `nap`
    # ⭐ `C11-R1-01` — hiệu lực theo kỳ TÍCH LUỸ: mỗi phiên bản là bản ĐẦY ĐỦ = dòng của bản liền
    #    trước *(giữ `hd@tu_ky` cũ, ⛔ mất mốc)* + dòng lần này *(cùng `hd@tu_ky` ⇒ bản mới thắng,
    #    ⛔ nhân đôi)*. Kho vẫn chỉ-thêm *(⛔ sửa bản cũ)*; bản liền trước ĐỌC KHÔNG ra *(⛔ qua
    #    `nap`)* thì ⛔ chở theo — nó vẫn nằm nguyên trong kho, bản tốt kế tiếp thắng.
    try:
        truoc = _doc_ban(conn, BANG_ALR)
        _alr_tu_cap(truoc.dong, truoc.nguon)
        cap_d = dict(truoc.dong)
    except (ChuaKhai, luat_pb.LoiLuatPB):
        cap_d = {}
    # ⭐ vòng sửa R1 `H12`: dòng ĐÃ KÝ *(mang `ky` — `ky_bat_ix_alr`)* ⛔ bị đường nạp ghi đè ở CÙNG khoá
    #    *(vd `HCC@202501`)* — nạp lại Mapping Master ⛔ được lặng lẽ GỠ chữ ký; gỡ là một tệp ký mới.
    cap_d.update((k, v) for k, v in moi
                 if not (isinstance(cap_d.get(k), Mapping) and luat_pb.COT_KY in cap_d[k]))
    cap = list(cap_d.items())
    return nap(conn, BANG_ALR, cap, nguon=nguon or duong_mm, actor=actor)


def ky_bat_ix_alr(conn, duong_tep: str, *, actor: str) -> BanCauHinh:
    """**Bật/tắt cờ CÓ KÝ** *(vòng sửa R1 `H12` — `KQ-293`; quyết của chủ 22/11 ~10:05 UTC)*: tệp ký config có
    phiên bản *(`luat_pb.dung_tu_tep_ky`)* ⇒ một phiên bản MỚI của `IX.ALR` = bản hiện hành + dòng đã ký
    *(cùng khoá `hd@tu_ky` ⇒ dòng ký thắng — bản cũ NGUYÊN trong kho, ⛔ sửa)*.

    `actor` = người ký ghi trong tệp *(⛔ người khác nạp hộ chữ ký của người khác; ⛔ email)*. Kho chưa có
    `IX.ALR` ⇒ `ChuaKhai` *(⛔ ký trên rỗng)*; bản hiện hành BẨN ⇒ `BanHong`."""
    tep = json.loads(Path(duong_tep).read_text(encoding="utf-8"))
    ky_tep = tep.get("ky") if isinstance(tep, Mapping) else None
    nguoi = ky_tep.get("nguoi_ky") if isinstance(ky_tep, Mapping) else None
    if not str(actor or "").strip() or "@" in str(actor) or actor != nguoi:
        raise LoiCauHinh(
            "⛔ `actor` %r ≠ người ký %r của tệp — bật cờ là chữ ký CỦA NGƯỜI ẤY *(TÊN, ⛔ email)*"
            % (actor, nguoi))
    truoc = _doc_ban(conn, BANG_ALR)                     # `ChuaKhai` ⇒ ⛔ ký trên rỗng
    try:
        hien = _alr_tu_cap(truoc.dong, truoc.nguon)
    except luat_pb.LoiLuatPB as e:
        raise BanHong("⛔ bản `IX.ALR` phiên bản %s ⛔ đọc ra được ⇒ ⛔ ký lên nó" % truoc.phien_ban) from e
    moi = luat_pb.dung_tu_tep_ky(tep, hien)              # `LoiLuatPB` CÓ TÊN
    cap_d = dict(truoc.dong)
    cap_d.update((luat_pb.khoa_cua(r["hd"], r["tu_ky"]), r) for r in moi)
    return nap(conn, BANG_ALR, list(cap_d.items()),
               nguon="ky:%s#v%s" % (Path(duong_tep).name, tep.get("phien_ban_tep")), actor=actor)


def doc_alr(conn) -> luat_pb.BangALR:
    """`IX.ALR` mới nhất, dựng lại **qua `luat_pb.kiem`**. `ChuaKhai` nếu kho chưa nạp; bản BẨN
    ⇒ `BanHong` CÓ TÊN *(⛔ `LoiLuatPB` trần lọt tuyến thành `500 FLS-INTERNAL`)*."""
    ban = _doc_ban(conn, BANG_ALR)
    try:
        return _alr_tu_cap(ban.dong, ban.nguon)
    except luat_pb.LoiLuatPB as e:
        raise BanHong(
            "⛔ bản `IX.ALR` phiên bản %s trong kho ⛔ ĐỌC ra được *(⛔ qua `nap`?)*"
            % ban.phien_ban) from e


# ── IX.FX · KÝ THÁNG (`C7`, `WO-212`, D1) ─────────────────────────────────────
class DaKy(LoiCauHinh):
    """Tháng ĐÃ ký với đúng tỷ giá hiện hành — ký lại ⇒ **409** *(⛔ huỷ ký: ngoài WO-212)*."""

    ma = "FLS-CAUHINH-DA-KY"


class ThangKhongCo(LoiCauHinh):
    """Tháng ⛔ có trong `IX.FX` ⇒ ⛔ có gì để niêm phong — **404**."""

    ma = "FLS-NOT-FOUND"


@dataclass(frozen=True)
class KyFX:
    yyyymm: int
    actor: str
    ky_luc: str          # ISO, do MÁY đặt (`luc` của bản ký)
    dau_van_tay: str


def doc_ky_fx(conn) -> dict[int, KyFX]:
    """Chữ ký tháng của bản KÝ mới nhất. Kho ⛔ có bản ký nào ⇒ `{}` *(⛔ `ChuaKhai`: chưa
    ai ký là trạng thái THƯỜNG, ⛔ lỗi)*."""
    try:
        ban = _doc_ban(conn, BANG_KY_FX)
    except ChuaKhai:
        return {}
    return {int(k): KyFX(int(k), v["actor"], v["ky_luc"], v["dau_van_tay"])
            for k, v in ban.dong}


def ky_fx(conn, yyyymm: Any, *, actor: str) -> KyFX:
    """Niêm phong tháng `yyyymm` của `IX.FX` hiện hành. `actor` do TẦNG CỬA lấy TỪ THẺ.

    Thêm MỘT bản ký mới = mọi chữ ký cũ + chữ ký này *(kho chỉ-thêm — ⛔ sửa bản cũ)*;
    `ky_luc` = `luc` do MÁY đặt. Cùng khoá `advisory` như `nap` ⇒ hai người ký cùng
    tháng cùng lúc: một người 201, người kia `DaKy`.
    """
    if not str(actor or "").strip():
        raise LoiCauHinh("⛔ thiếu `actor` — ký tháng là hành vi của người, phải có tên")
    m, ly = fx._thang(yyyymm)
    if m is None:
        raise fx.LoiFX([f"yyyymm={yyyymm!r} {ly}"])
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(hashtext(%s)::bigint)",
                        (BANG_KY_FX,))
        dong = [d for d in doc_fx(conn).ky if d.yyyymm == m]
        if not dong:
            raise ThangKhongCo(f"⛔ tháng {m} ⛔ có trong {BANG_FX} hiện hành — "
                               f"⛔ có số để niêm phong")
        dv = fx.dau_van_tay(dong[0])
        cu = doc_ky_fx(conn)
        if m in cu and cu[m].dau_van_tay == dv:
            raise DaKy(f"⛔ tháng {m} ĐÃ ký bởi {cu[m].actor} lúc {cu[m].ky_luc}")
        with conn.cursor() as cur:
            cur.execute("SELECT coalesce(max(phien_ban), 0) FROM fls_cau_hinh_ban "
                        "WHERE bang = %s", (BANG_KY_FX,))
            ver = int(cur.fetchone()[0]) + 1
            cur.execute("SELECT now()")
            luc = cur.fetchone()[0]
            moi = {k: {"actor": v.actor, "ky_luc": v.ky_luc,
                       "dau_van_tay": v.dau_van_tay} for k, v in cu.items()}
            moi[m] = {"actor": actor, "ky_luc": luc.isoformat(), "dau_van_tay": dv}
            cap = [(str(k), v) for k, v in sorted(moi.items())]
            cur.execute(
                "INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor, luc) "
                "VALUES (%s,%s,%s,%s,%s,%s) RETURNING ban_id",
                (BANG_KY_FX, ver, fx.KY_FX, _checksum(BANG_KY_FX, cap), actor, luc))
            ban_id = cur.fetchone()[0]
            cur.executemany(
                "INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) "
                "VALUES (%s,%s,%s::jsonb)",
                [(ban_id, k, json.dumps(v, ensure_ascii=False)) for k, v in cap])
    return KyFX(m, actor, luc.isoformat(), dv)


def fx_cua(conn, yyyymm: Any) -> Mapping[str, Any]:
    """Tỷ giá tháng cho ENGINE: chỉ khi tháng đã ký, ⛔ thì `fx.FxChan` có tên tháng.
    *(Engine H4…H9 ⛔ nối ở bước này — xem BG-213.)*"""
    return fx.fx_cua(yyyymm, doc_fx(conn),
                     {m: k.dau_van_tay for m, k in doc_ky_fx(conn).items()})


# ── IX.TMP · BẢN BÁO CÁO KÝ CÓ PHIÊN BẢN (`C13`, `WO-257`) ────────────────────
# Dùng LẠI bảng `0027` *(⛔ di trú mới)*. Kho chỉ-thêm ⇒ MỖI SỰ KIỆN là một bản config
# `bang='IX.TMP'` — ⛔ sửa dòng nào:
#   · đưa bản : `nguon='ban:{ky}'` · `checksum` = checksum nội dung · `actor` = người/engine đưa
#               · dòng `so_ban` (phiên bản 1,2,… TRONG kỳ) + `noi_dung` (JSON ô)
#   · ký      : `nguon='ky:{ky}'`  · `checksum` = của bản được ký · `actor` = người ký (TỪ THẺ)
#               · `luc` do MÁY · dòng `so_ban`
# Phiên bản `n` là `da_ky` ⇔ có sự kiện ký mang `so_ban = n`.
@dataclass(frozen=True)
class BanKy:
    ky: int
    phien_ban: int
    checksum: str
    trang_thai: str            # 'chua_ky' | 'da_ky'
    nguoi_dua: str
    dua_luc: str
    actor: str | None = None   # người ký (chỉ khi da_ky)
    ky_luc: str | None = None
    khong_doi: bool = False    # True ⇒ lần `dua_ban_ky` này TRÙNG bản mới nhất (⛔ sinh bản)


def _sk_ban_ky(conn, ky: int) -> list[BanKy]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT b.nguon, b.checksum, b.actor, b.luc, "
            "(SELECT d.gia_tri FROM fls_cau_hinh_dong d "
            "  WHERE d.ban_id = b.ban_id AND d.khoa = 'so_ban') "
            "FROM fls_cau_hinh_ban b WHERE b.bang = %s AND b.nguon IN (%s, %s) "
            "ORDER BY b.phien_ban", (ban_ky.BANG, f"ban:{ky}", f"ky:{ky}"))
        rows = cur.fetchall()
    ban: dict[int, BanKy] = {}
    for nguon, ck, actor, luc, so in rows:
        n = int(so)
        if nguon.startswith("ban:"):
            ban[n] = BanKy(ky, n, ck, "chua_ky", actor, luc.isoformat())
        elif n in ban and ban[n].trang_thai == "chua_ky":
            ban[n] = replace(ban[n], trang_thai="da_ky", actor=actor,
                             ky_luc=luc.isoformat())
    return [ban[n] for n in sorted(ban)]


def doc_ban_ky(conn, ky: Any) -> list[BanKy]:
    """Mọi phiên bản của kỳ, cũ → mới. Kỳ chưa có bản ⇒ `[]` *(trạng thái THƯỜNG)*;
    `ky` hỏng ⇒ `ban_ky.LoiBanKy`."""
    return _sk_ban_ky(conn, ban_ky.kiem_ky(ky))


def doc_noi_dung_ban_ky(conn, ky: Any, phien_ban: int) -> dict:
    """Nội dung JSON ô của một phiên bản *(⛔ có tuyến trả — chỉ bài/engine đọc)*."""
    k = ban_ky.kiem_ky(ky)
    with conn.cursor() as cur:
        cur.execute(
            "SELECT d.gia_tri FROM fls_cau_hinh_ban b "
            "JOIN fls_cau_hinh_dong d ON d.ban_id = b.ban_id AND d.khoa = 'noi_dung' "
            "JOIN fls_cau_hinh_dong s ON s.ban_id = b.ban_id AND s.khoa = 'so_ban' "
            "WHERE b.bang = %s AND b.nguon = %s AND s.gia_tri = %s::jsonb",
            (ban_ky.BANG, f"ban:{k}", json.dumps(int(phien_ban))))
        r = cur.fetchone()
    if r is None:
        raise ThangKhongCo(f"⛔ kỳ {k} chưa có phiên bản {phien_ban}")
    return r[0]


def _them_su_kien(cur, nguon: str, ck: str, actor: str, so: int, them=()) -> None:
    cur.execute("SELECT coalesce(max(phien_ban), 0) FROM fls_cau_hinh_ban WHERE bang = %s",
                (ban_ky.BANG,))
    ver = int(cur.fetchone()[0]) + 1
    cur.execute(
        "INSERT INTO fls_cau_hinh_ban (bang, phien_ban, nguon, checksum, actor) "
        "VALUES (%s,%s,%s,%s,%s) RETURNING ban_id", (ban_ky.BANG, ver, nguon, ck, actor))
    ban_id = cur.fetchone()[0]
    cap = [("so_ban", so), *them]
    cur.executemany(
        "INSERT INTO fls_cau_hinh_dong (ban_id, khoa, gia_tri) VALUES (%s,%s,%s::jsonb)",
        [(ban_id, k, json.dumps(v, ensure_ascii=False)) for k, v in cap])


def dua_ban_ky(conn, ky: Any, noi_dung: Mapping[str, Any], *, actor: str) -> BanKy:
    """Đưa MỘT bản báo cáo vào kỳ `ky` *(engine H14 gọi sau này; ⛔ tuyến)*.

    Checksum khác bản MỚI NHẤT ⇒ phiên bản mới `chua_ky`. TRÙNG checksum bản mới nhất ⇒
    ⛔ phiên bản mới, trả bản ấy với `khong_doi=True` *(đã ký thì vẫn `da_ky`)*.
    ⚠ So với bản MỚI NHẤT, ⛔ với mọi bản: đổi rồi quay lại số cũ là phiên bản mới.
    """
    k = ban_ky.kiem_ky(ky)
    ck = ban_ky.checksum(noi_dung)
    if not str(actor or "").strip():
        raise LoiCauHinh("⛔ thiếu `actor` — đưa bản vào kỳ là hành vi có người/engine đứng tên")
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(hashtext(%s)::bigint)", (ban_ky.BANG,))
        cu = _sk_ban_ky(conn, k)
        if cu and cu[-1].checksum == ck:
            return replace(cu[-1], khong_doi=True)
        n = len(cu) + 1
        with conn.cursor() as cur:
            _them_su_kien(cur, f"ban:{k}", ck, actor, n,
                          [("noi_dung", json.loads(ban_ky.chuan_hoa(noi_dung)))])
    return _sk_ban_ky(conn, k)[-1]


def ky_ban(conn, ky: Any, *, actor: str) -> BanKy:
    """Ký phiên bản MỚI NHẤT của kỳ. `actor` do TẦNG CỬA lấy TỪ THẺ. Kỳ chưa có bản ⇒
    `ThangKhongCo` · bản mới nhất đã ký ⇒ `DaKy` · bản cũ đã ký ⛔ đụng."""
    k = ban_ky.kiem_ky(ky)
    if not str(actor or "").strip():
        raise LoiCauHinh("⛔ thiếu `actor` — ký bản là hành vi của người, phải có tên")
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("SELECT pg_advisory_xact_lock(hashtext(%s)::bigint)", (ban_ky.BANG,))
        cu = _sk_ban_ky(conn, k)
        if not cu:
            raise ThangKhongCo(f"⛔ kỳ {k} chưa có bản báo cáo nào để ký")
        m = cu[-1]
        if m.trang_thai == "da_ky":
            raise DaKy(f"⛔ phiên bản {m.phien_ban} của kỳ {k} ĐÃ ký bởi {m.actor} "
                       f"lúc {m.ky_luc}")
        with conn.cursor() as cur:
            _them_su_kien(cur, f"ky:{k}", m.checksum, actor, m.phien_ban)
    return _sk_ban_ky(conn, k)[-1]
