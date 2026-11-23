"""`KQ-002 · F-2` — cổng mốc `B` ⛔ được đếm sự kiện của MÁY là cú bấm của NGƯỜI.

⛔⛔⛔ **Đo được 01/10/2026 trên kho THẬT** *(chỉ đọc)*:

    fls_queue_event  evt_type <> 'reason'                        2.221
      ├─ actor = 'may@fls'  (may_ghep.MAY · `goi_y_lai` 18/09)   2.219   ← MÁY
      └─ actor = 'khanhcq@apero.vn' · reason 'UAT 01/10 …'          2   ← UAT

`tools/kiem_so_song.py::_cong_moc_b` lấy `su_kien_cho_nguoi` =
`count(*) … where evt_type <> 'reason'` với tiền đề *"`match`/`unmatch`/… chỉ
sinh từ một cú bấm có ý trong `F01`"*. ⛔ Tiền đề ấy **vỡ ngày 18/09**:
`QĐ-ITL-143` cho máy tự ghép ghi **2.219** sự kiện `match` mang `actor='may@fls'`.
⇒ `B2`·`B3`·`B5` **lật ĐẠT từ 18/09** mà ⛔ 0 kế toán nào bấm — và chính
`06_ORCHESTRATOR_DASHBOARD.md:121` in *"MÁY ĐẾM: `4` đạt"* ngay cạnh câu
*"`B2`·`B3`·`B5` **CHƯA** … `evt_type <> 'reason'` = **`0`**"*. Số đúng (máy
sinh), câu sai — và docstring của `_cong_moc_b` đã tự báo trước: *"giây phút
con số ấy lên `1`, phép đếm này thành quá thô … phải siết lại"*.

⭐ Bài này lấy **chính câu SQL** của cổng *(đọc bằng `ast` từ mã nguồn — ⛔ chép
tay; `Đ5`: khớp 0 hay ≥2 chỗ là ĐỎ)* rồi chạy nó trên một bảng `fls_queue_event`
**giả bằng CTE** *(che bảng thật cùng tên trong câu lệnh — ⛔ ghi gì, kể cả kho
test)*.

⚠ **Ngoài phạm vi bài này:** UAT của owner có tính là *"người thật"* không
*(`11_BOI_CANH_TU_MEMORY` §7: ⚠ "đừng tính nó là cổng `B5` ĐẠT")* — đó là câu
của **BA/owner** *(F-2b)*, ⛔ bài này ⛔ đoán thay.
"""
from __future__ import annotations

import ast
import pathlib

import psycopg
import pytest

from fls.db.kho import dsn_test
from fls.repo.may_ghep import MAY

pytestmark = pytest.mark.pg

GOC = pathlib.Path(__file__).resolve().parents[2]


def _sql_cong() -> str:
    cay = ast.parse((GOC / "tools" / "kiem_so_song.py").read_text(encoding="utf-8"))
    tim = [v for n in ast.walk(cay) if isinstance(n, ast.Dict)
           for k, v in zip(n.keys, n.values)
           if isinstance(k, ast.Constant) and k.value == "su_kien_cho_nguoi"]
    assert len(tim) == 1, f"⛔ không đo được: khoá `su_kien_cho_nguoi` khớp {len(tim)} chỗ"
    v = tim[0]
    assert (isinstance(v, ast.Call) and v.args
            and isinstance(v.args[0], ast.Constant)), "⛔ không đo được: khuôn `dem(<chuỗi>)` đã đổi"
    return v.args[0].value


def _dem(dong: list[tuple[str, str, str]]) -> int:
    # ⚠ Hằng nhúng bằng `sql.Literal`, ⛔ KHÔNG truyền tham số: cổng gọi
    #   `execute(sql)` trần, nên câu của nó được phép mang `%` (vd. `LIKE
    #   'may@%'`) — truyền tham số ở đây sẽ làm bài NỔ vì một bản vá đúng.
    from psycopg import sql as S
    with psycopg.connect(dsn_test()) as c:
        L = lambda x: S.Literal(x).as_string(c)            # noqa: E731
        gia = ", ".join(
            f"({i}::bigint, 1::bigint, {L(loai)}, {L(ly_do)}, NULL::date,"
            f" {L(actor)}, now())"
            for i, (loai, actor, ly_do) in enumerate(dong))
        cau = ("WITH fls_queue_event(evt_id, itl_id, evt_type, reason,"
               " defer_until, actor, at) AS (VALUES " + gia + ") " + _sql_cong())
        return int(c.execute(cau).fetchone()[0])


# ⭐ Gỡ dấu `xfail(strict)` 01/10 tối (`KQ-010`, kiểm `BG-009` @ `6e98796`):
#   `WO-001 T1a` vá — XPASS đúng lý do *(đột biến bỏ vạch actor / lệch hằng
#   `MAY` trên worktree ⇒ bài này ĐỎ lại; trả nguyên ⇒ xanh)*.
def test_su_kien_cua_MAY_tu_ghep_KHONG_lam_cong_moc_B_nhay():
    n = _dem([("match", MAY, "may tu ghep 1 dong lenh (PM00001-1)"),
              ("match", MAY, "may tu ghep 1 dong lenh (PM00002-1)"),
              ("reason", "dung-lai-so@apero.vn", "S7 · dong trung")])
    assert n == 0, (
        f"⛔⛔ cổng mốc B đếm {n} sự kiện của MÁY (`{MAY}`) là cú bấm của NGƯỜI "
        "⇒ B2·B3·B5 ĐẠT mà ⛔ chưa kế toán nào bấm")


def test_DOI_CHUNG_mot_cu_bam_NGUOI_that_thi_cong_DEM_duoc():
    """⭐ Chiều ngược (`Đ5`): vá bằng cách đếm `0` mãi thì cũng ĐỎ."""
    assert _dem([("match", "ke-toan@apero.vn", "ghep tay tu man F01"),
                 ("reason", "dung-lai-so@apero.vn", "S7 · dong trung")]) == 1
