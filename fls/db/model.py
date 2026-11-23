"""SSOT của schema fls_*. Khai báo MỘT lần, sinh ra cả DDL lẫn ERD.

Vì sao không dùng dict[str, str] DDL thô như FPS: không sinh được ERD từ chuỗi SQL
mà không viết bộ phân tích SQL, và drift ERD là rủi ro số một (03_IMPLEMENTATION_PLAN §1).
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Column:
    name: str
    type: str
    null: bool = True
    default: str | None = None
    fk: str | None = None          # "bang.cot"
    pk: bool = False
    unique: bool = False
    generated: str | None = None   # biểu thức của GENERATED ALWAYS AS ... STORED
    # ⭐⭐ `CHECK` mức cột — thêm 2026-09-08 *(`QĐ-ITL-113`, cột
    # `fls_khai_cot.thu_tu`)*. Sinh ra một ràng buộc **CÓ TÊN** ở mức bảng
    # *(`<bảng>_<cột>_ck`)*, ⛔ không phải một `CHECK` nội dòng khuyết danh —
    # vì `pg_verify` đối chiếu **theo tên**, và một ràng buộc Postgres tự đặt
    # tên là một ràng buộc ⛔ không cổng nào gọi đúng được.
    #
    # ⚠ Đo 08/09 trước khi thêm: kho THẬT có **0** ràng buộc `CHECK` ⇒ đây là
    #   cái đầu tiên, và `pg_verify` được mở rộng **cùng lượt** để canh nó.
    #   ⛔ Một trường khai mà cổng ⛔ không đọc là một dòng khai vô hình.
    check: str | None = None
    comment: str = ""


@dataclass(frozen=True)
class Table:
    name: str
    columns: tuple[Column, ...]
    kind: str = "table"            # "table" | "view"
    erd_entity: str = ""           # tên entity tương ứng trên ERD của BA
    # ⭐⭐⭐ `tang` — TẦNG KIẾN TRÚC, thêm 2026-09-15.
    #
    # ⛔⛔ **Vì sao nó nằm ở ĐÂY chứ ⛔ không ở một bản vẽ riêng.** `ERD-CONTRACT.mmd`
    # sinh từ chính tệp này và có cổng `G-ERD-1` canh — nên nó ⛔ **không bao giờ
    # già**. Một bản đồ tầng vẽ tay trong một tệp `.html` thì ⛔ **không có cổng
    # nào**, và nó sẽ già **im lặng** đúng như `BA-03` đã già ba lần.
    #
    # ⇒ Tầng là **một trường của bản khai**, và `tools/sinh_ban_do_tang.py` sinh
    #   bản vẽ ra từ đó. Thêm một bảng mà quên khai tầng ⇒ cổng **NO**.
    #
    # ⚠ `tang` ⛔ **không** đổi một dòng DDL nào — nó thuần tuý là cách **đọc**
    #   kho. Hai bảng cùng tầng ⛔ không có gì chung ở Postgres; chúng chung
    #   **câu hỏi mà chúng trả lời**.
    tang: str = ""
    # ⭐⭐⭐ `khau` — KHÂU NGHIỆP VỤ, thêm 2026-09-17 *(owner: "sắp xếp theo
    # flow chính: nạp data → ghép lệnh chi → adjust ITL. Tôi muốn biết các
    # entity thuộc các module nghiệp vụ nào")*.
    #
    # ⛔⛔ **`khau` ⛔ KHÔNG phải `tang` đổi tên.** Hai trục trả lời hai câu:
    #     `tang` → *"nó nằm ở đâu trong đường đi của DỮ LIỆU"*
    #     `khau` → *"nó phục vụ VIỆC nào của người"*
    #   Chúng **giao nhau chứ ⛔ không lồng nhau**, và chỗ hai trục **lệch**
    #   nhau là chỗ đáng nhìn nhất — ví dụ `fls_pm_line` do khâu `A` **GHI**
    #   nhưng tồn tại để khâu `B` **DÙNG**.
    #
    # ⭐ **Luật gán: theo VIỆC NÓ PHỤC VỤ, ⛔ không theo ai ghi nó.** Thiếu
    #   luật này thì phép gán thành cảm tính — `fls_queue_event` sẽ rơi vào
    #   `A` *(máy ghi `108.128` sự kiện lúc nạp)* trong khi nó là **bảng việc
    #   của NGƯỜI**.
    #
    # ⛔ Tên khâu **lấy lại từ bộ tài liệu**, ⛔ không đặt tên mới: mốc `A`
    #   *(đường LẤY dữ liệu)* · tác vụ ① *(mapping PM ↔ Transaction)* · tác vụ
    #   ② *(adjust thông tin ITL)* — `01_Orchestrator/09_MILESTONES_HAI_TAC_VU`.
    #   Đặt tên thứ tư cho một thứ đã có tên là cách đẻ ra `GAP-ITL-02`.
    khau: str = ""
    island_reason: str = ""        # lý do KHÔNG có FK về fls_itl (G-ERD-3)
    view_sql: str = ""
    # Khoá NHIỀU CỘT — thêm 2026-08-27, đóng `GAP-DB-P0-03`.
    # ⛔ Trước đó khuôn này chỉ khai được khoá MỘT cột, nên `fls_reject` không có
    # `UNIQUE(run_id, source_row)` ở tầng kho: lớp chặn trùng duy nhất là điều
    # kiện trong câu `INSERT`. Và `fls_pm_link` (một dòng sổ → N dòng lệnh) thì
    # KHÔNG THỂ khai nổi nếu không có khoá hai cột.
    pk_cols: tuple[str, ...] = ()
    unique_keys: tuple[tuple[str, ...], ...] = ()


def kiem_khai_bao(t: Table) -> list[str]:
    """Lỗi tự-mâu-thuẫn trong một bản khai. Rỗng = sạch.

    ⛔ Hai chỗ khai CÙNG một khoá là đúng cái bệnh cả khuôn này chữa — nên
    khai khoá ở cả cột lẫn bảng là LỖI, không phải "ghi cho chắc".
    """
    ra: list[str] = []
    ten = {c.name for c in t.columns}
    pk_cot = [c.name for c in t.columns if c.pk]

    if t.pk_cols and pk_cot:
        ra.append(f"{t.name}: khoá chính khai HAI CHỖ — cột {pk_cot} và bảng "
                  f"{list(t.pk_cols)}. Chọn một chỗ.")
    for c in t.pk_cols:
        if c not in ten:
            ra.append(f"{t.name}: pk_cols có {c!r} mà bảng không có cột đó")
    if len(set(t.pk_cols)) != len(t.pk_cols):
        ra.append(f"{t.name}: pk_cols có cột lặp {list(t.pk_cols)}")
    for k in t.unique_keys:
        if not k:
            ra.append(f"{t.name}: unique_keys có một khoá RỖNG")
        for c in k:
            if c not in ten:
                ra.append(f"{t.name}: unique_keys có {c!r} mà bảng không có cột đó")
        if len(k) == 1:
            ra.append(f"{t.name}: unique_keys {list(k)} chỉ MỘT cột — khai "
                      f"`unique=True` ngay ở cột đó, đừng tạo chỗ khai thứ hai")
    if t.kind == "view" and (t.pk_cols or t.unique_keys):
        ra.append(f"{t.name}: là VIEW mà khai khoá — view không có ràng buộc")
    return ra
