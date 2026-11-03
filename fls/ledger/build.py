"""Lop so mong: canon + ngu canh run -> payload de repo ghi vao fls_itl.

Dung "mong" theo nghia 01_TECH_DESIGN §2: 6 phep chep + 1 phep danh so
+ 5 cau if giong nhau + 1 phep join. ⛔ Khong luat phan loai nao o day —
luat phan loai thuoc adapter (thuong nguon).

Phep danh so KHONG nam trong module nay: itl_id do SEQUENCE cua DB cap
(INV-I04a). Lop so tu danh so la cach tai lap dung loi AS-IS.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from typing import Any

from fls.canon.le import ma_le
from fls.canon.row import CanonRow
from fls.canon.validate import parse_ngay, parse_so, validate
from fls.ledger.final_rule import (BAY_KHOI, TEN_BAY_KHOI, TEN_KHOI,
                                   dung_khoi)

# Vi tri trong khuon CANON (⛔ khong phai cua ITL Ledge — xem spec.py)
_NGAY, _SO_CT, _MEMO, _CURR, _NO, _CO, _ACCT = 0, 1, 2, 3, 4, 5, 6
_LE = 32            # AG · "LE" — ⛔ KHONG dung AH-AK (4 cot trung ten)
_LE_PAYER = 11      # L  · "Phap nhan thanh toan"
_PM_LINE = 13       # N  · "ID PMLine" — lineage phai song sot (QD-ITL-20/CR#1)


@dataclass(frozen=True)
class NgucCanh:
    run_id: str
    contract_version: str
    canon_version: str
    mapping_version: str
    source_system: str
    source_sheet: str
    # ⭐⭐⭐ LINEAGE của lần nạp — thêm 2026-09-08 *(`QĐ-ITL-110`)*.
    #
    # ⛔ `None` được, và đó là `R-A1`: lô `NAP-2026-08-27-RAW` *(10.030 dòng
    #   đang nằm trong kho)* có **TRƯỚC** bảng ảnh chụp ⇒ một lô đi đường
    #   `dong` *(test/đối chứng)* **phải hiện ra** là `chup_id = NULL`.
    #
    # ⛔⛔ **VÀ ĐÂY LÀ CHỖ PHẢI ĐỌC KỸ — vì sao ⛔ KHÔNG có `khai_id` ở đây.**
    #
    # Cột `fls_run.khai_id` sinh ra ở task `1` *(migration `0016`)*, và
    # `fls/db/erd_policy.py` khai hẳn một **đường lineage** dựa vào nó:
    #
    #     fls_itl.run_id → fls_run.khai_id → fls_khai_cot.source_id → fls_source
    #
    # Quét mã ngày 08/09: **⛔ KHÔNG một câu `INSERT`/`UPDATE` nào set cột
    # ấy** — nó `NULL` ở **100%** dòng. Phản xạ đầu tiên của tôi là *"quên nối
    # dây, nối vào"*. ⛔ **Sai.**
    #
    # ⭐ Đo tiếp thì lý do sâu hơn: `fls_khai_cot` giữ **MỘT DÒNG MỖI TRƯỜNG**
    #   *(khoá `(source_id, version, truong)` — **6 dòng** cho một bản khai)*.
    #   Nên `khai_id` là danh tính của **một trường**, ⛔ không của **một bản
    #   khai**. ⇒ ⛔ **Không tồn tại** một `khai_id` mang nghĩa *"bản khai mà
    #   lô này đã dùng"*; chọn bừa một trong 6 là **bịa một nghĩa**.
    #
    # ⇒ Cột ấy **⛔ không phải quên nối — nó SAI MÔ HÌNH** *(`GAP-CHUP-04`)*, và
    #   ⛔ tôi ⛔ không vá bằng cách nhồi một giá trị trông có nghĩa vào.
    #
    # ⭐⭐ Lineage THẬT đi qua ảnh chụp, và nó **đủ**:
    #
    #     fls_itl.run_id → fls_run.chup_id → fls_chup_nguon
    #                    (source_id, khai_version) → fls_khai_cot
    #
    #   đọc ra tiếng Việt: *"dòng sổ này thuộc lô này, lô đọc ảnh chụp này, ảnh
    #   chụp đọc nguồn này bằng bản khai `version` này"* — và nó neo vào
    #   **`(source_id, version)`**, đúng thứ định danh một bản khai.
    chup_id: int | None = None

    # ⭐⭐ `QĐ-ITL-113` — THỨ TỰ NGÀY do nguồn khai (`fls_khai_cot.thu_tu`).
    #
    # ⛔⛔ **Vì sao ở đây chứ ⛔ không ở adapter.** Cả `sao_ke.chuyen()` lẫn
    #    `sao_ke_canon.dung_canon()` khai thẳng trong mã: *"⛔ KHÔNG làm sạch
    #    giá trị"* — vì mọi phép đổi ở tầng ấy là một chỗ đối soát có thể đỏ
    #    vì **lỗi của ta**, ⛔ không phải lỗi của sổ. ⇒ Ngày trở thành `date`
    #    ở **tầng sổ**, đúng nơi `parse_ngay` sống.
    #
    # ⭐ Và chính `parse_ngay` đã viết sẵn cách vá trong thông điệp lỗi của
    #   nó: *"Gọi `parse_ngay(..., thu_tu='dmy'|'mdy')` theo khai báo của
    #   nguồn"* — thiết kế lường trước, ⛔ tôi ⛔ không phát minh đường mới.
    #
    # ⛔ `None` = *"nguồn ⛔ chưa khai"*, ⛔ **không** = *"coi như `dmy`"*.
    thu_tu: str | None = None


def content_key(source_system: str, source_sheet: str, doc_date: date | None,
                ps_no: Any, ps_co: Any, doc_no: str | None,
                seq_trung: int) -> str:
    """Khoa DOI SANH (INV-I04b). ⛔ KHONG phai danh tinh — danh tinh la itl_id.

    ⛔ KHONG chua vi tri dong: 281 dong trung noi dung + 103 dong khong co so
    chung tu, nen khoa noi dung mot minh khong du lam danh tinh; `seq_trung` la
    tham so TUONG MINH do goi truyen vao, khong phai may tu doan.
    """
    thanh_phan = "".join((
        str(source_system), str(source_sheet),
        doc_date.isoformat() if doc_date else "",
        "" if ps_no is None else repr(ps_no),
        "" if ps_co is None else repr(ps_co),
        "" if doc_no is None else str(doc_no),
        str(seq_trung),
    ))
    return hashlib.sha256(thanh_phan.encode("utf-8")).hexdigest()


def dung_dong(row: CanonRow, source_row: int, nc: NgucCanh,
              khoi: dict[str, tuple[str | None, str | None]] | None = None,
              seq_trung: int = 0,
              pm: str | None = None) -> dict[str, Any]:
    """Dung payload mot dong fls_itl. Dong bi LOAI thi NO, khong am tham dung."""
    kq = validate(row, nc.thu_tu)
    if kq.loai:
        raise ValueError("khong the dung dong, phai vao fls_reject: "
                         + " | ".join(kq.loai))

    sai = set(khoi or {}) - TEN_BAY_KHOI
    if sai:
        raise ValueError(f"khoi khong thuoc 7 khoi cua so: {sorted(sai)}")

    ngay = parse_ngay(row.at(_NGAY), nc.thu_tu)
    ps_no, ps_co = parse_so(row.at(_NO)), parse_so(row.at(_CO))

    d: dict[str, Any] = {
        # 6 phep chep BASE + tai khoan
        "doc_date": ngay,
        "doc_no": row.at(_SO_CT),
        "memo": row.at(_MEMO),
        "curr": row.at(_CURR),
        "ps_no": ps_no,
        "ps_co": ps_co,
        "acct": row.at(_ACCT),
        # 1 phep join: phap nhan. `ma_le` cat phan ten: nguon mang HAI hinh cho
        # cung mot phap nhan ('VGOH' o cot AG, 'VGOH - APERO HQ' o cot L) va ca
        # hai cot deu FK toi `fls_le.le_code`. ⛔ Khong mat gi: `canon` jsonb giu
        # nguyen van. Xem `fls/canon/le.py`.
        "le": ma_le(row.at(_LE)),
        "le_payer": ma_le(row.at(_LE_PAYER)),
        # lineage + run (INV-I05 / INV-I12) — khong bao gio NULL
        "source_system": nc.source_system,
        "source_sheet": nc.source_sheet,
        "source_row": source_row,
        "run_id": nc.run_id,
        "contract_version": nc.contract_version,
        "canon_version": nc.canon_version,
        "mapping_version": nc.mapping_version,
        # khoa doi sanh
        "content_key": content_key(nc.source_system, nc.source_sheet, ngay,
                                   ps_no, ps_co, row.at(_SO_CT), seq_trung),
        # 36 truong nguyen van theo VI TRI (38 o, ke ca 2 o trong)
        "canon": row.as_jsonb_list(),
        # moi noi voi lenh chi PM. `pm` = HINH ghep ('A'|'B'|'C') hoac None.
        # ⛔ `pm_line_id` DA BO khoi dong so (migration 0007): mot cot giu duoc
        # mot moi noi, ma hinh `B` la mot dong so tro toi N dong lenh. Moi noi
        # nay o `fls_pm_link` — MOT cho duy nhat.
        # ⛔ KHONG suy tu cot `ID PMLine` go tay trong sheet (vi tri 13, day
        # `#N/A`): phep ghep la viec cua `fls/adapters/pm_join.py`, va no phai
        # qua CONG Σ. Doc mot cot go tay o day la bo qua cong do.
        "pm_hinh": pm,
    }

    # 5 cau if giong nhau (7 khi tinh ca khoi 6-7 ngoai hop dong P&L).
    # Moi khoi nhan (Classifying, Manual input) va TUY CHON MID cua so:
    # co MID => che do oracle (dam bao parity); khong co => tu suy.
    co_bia = False
    chua_tra_loi: list[str] = []      # khoi DUOC HOI ma khong ra duoc dap an
    for ten, ten_thyt in BAY_KHOI:
        v = (khoi or {}).get(ten)
        if v is None:
            # nguon nay KHONG MANG khoi do — khac han voi "mang ma chua ai tra loi"
            d[ten] = d[ten_thyt] = None
            continue
        cls, man, mid = (v + (None,))[:3] if len(v) < 3 else v
        r = dung_khoi(ten, cls, man, mid=mid)
        d[ten], d[ten_thyt] = r.parity, r.thyt
        co_bia = co_bia or r.may_tu_bia
        if r.parity is None:
            chua_tra_loi.append(ten)

    # ★★ `INV-I16`: "truong nao may khong suy duoc thi mang trang thai UNMAPPED
    # VA CO MAT TRONG HANG CHO". Ban dau o day chi xet `co_bia` (may tu gan mac
    # dinh) — tuc chi mot nua cua bat bien. Lan nap THAT dau tien do ra cai nua
    # con lai: 9.973 dong vao so, **6.634 dong khong co `hd`**, va hang cho
    # dem duoc **0**. Man F01 se hien "khong co viec gi lam" trong khi hai phan
    # ba so chua ai tra loi.
    #
    # ⚠ Mot quyet dinh CO CHU Y o day, va no la quyet dinh cua NGHIEP VU:
    # chi 5 khoi P&L (`NAM_KHOI` = dung 5 truong cua ITL-CONTRACT) day dong vao
    # hang cho. Khoi 6-7 (`id_payee`/`invoice`) NGOAI hop dong P&L va thieu tren
    # 95,7% dong — de chung day hang cho thi hang cho luon dai 9.500 dong va
    # khong ai doc nua. Chung van duoc DEM RIENG (`thieu_ngoai_pnl`) de owner doi
    # duong ke neu muon, ⛔ khong bi xoa.
    cho_pnl = [x for x in chua_tra_loi if x in TEN_KHOI]
    d["work_status"] = "UNMAPPED" if (co_bia or kq.cho or cho_pnl) else "ok"
    return d
