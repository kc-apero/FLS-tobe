# -*- coding: utf-8 -*-
"""Nhóm **NẠP CẢ LÔ** *(`QĐ-ITL-111` + `112`)* CHẠY THẬT qua HTTP.

⛔⛔ **Ba bài ở đây ⛔ KHÔNG kiểm *"cửa có chạy ⛔ không"* — chúng kiểm ba thứ
   mà một cú vá ngây thơ sẽ làm sai TRONG IM LẶNG:**

  ⓐ `test_HAI_NGUON_dong_Y_HET_deu_VAO_SO` — bẫy `content_key`. `source_sheet`
    là **của cả lô**, nên nối 60 nguồn thành một danh sách phẳng dưới **một**
    `NgucCanh` thì dòng của **hai bank khác nhau** bị đếm là **TRÙNG rồi bỏ
    đi trong im lặng**. ⛔ Bài này là **lý do duy nhất** khiến vòng lặp phải
    nằm trong cửa, ⛔ không phải ở lời hứa trong tài liệu.

  ⓑ `test_row_count_cua_fls_run_la_TONG_ca_lo` — `mo_run` có `ON CONFLICT DO
    NOTHING`, nên gọi 58 lần cùng một `run_id` thì `row_count` **staging** là
    của **nguồn ĐẦU TIÊN**. Nó đúng chỉ vì `dong_run` **ĐẾM TỪ BẢNG** sau mỗi
    nguồn. ⇒ Ghim đúng tính chất ấy, ⛔ không tin vào suy luận.

  ⓒ `test_nguon_RONG_KHONG_lam_ca_lo_DO_OAN` — 10/60 nguồn thật đọc ra **0
    dòng**, và với chúng `S2`…`S7` trả `dat=False, da_do=0`. Gộp bằng
    `all(dat)` thì **6/9 luật của cả lô đỏ** vì 10 tài khoản rỗng. Một báo
    động **đỏ oan** là một báo động **sẽ bị bỏ qua**.
"""
from __future__ import annotations

import psycopg
import pytest

from fls.db.kho import dsn_test
from tests.api.test_cua_nap_pg import V, _goi, _hex, _may, may  # noqa: F401
from tests.api.test_cua_chup_pg import (_chup, _khai_du,  # noqa: F401
                                        _nguon_day_du, _o)

pytestmark = pytest.mark.pg

LO = V + "/nap/lo"
XEM = V + "/nap/lo/xem-truoc"


def _rid() -> str:
    return "NAP-2026-09-08-LO" + _hex(4)


def _dem(run_id: str) -> int:
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl WHERE run_id = %s", (run_id,))
        return int(cur.fetchone()[0])


# ═════════════════════════ ⓐ bẫy `content_key` ═════════════════════════
def test_HAI_NGUON_dong_Y_HET_deu_VAO_SO(may):
    """⭐⭐⭐ Bài đắt nhất của cả nhóm — và nó là **lý do** cửa phải lặp.

    Hai nguồn khác nhau, **cùng ngày · cùng mã · cùng số tiền**. Nếu cửa nối
    phẳng dưới một `NgucCanh` thì `content_key` của chúng **bằng nhau** ⇒
    dòng thứ hai bị `ON CONFLICT DO NOTHING` **bỏ đi trong im lặng**, và biên
    bản vẫn nói *"2 nguồn vào sổ"*.
    """
    a, ka = _nguon_day_du()
    b, kb = _nguon_day_du()
    o = _o(**{"Reference number": "FT-GIONG-NHAU"})
    cid = _chup({a: 1, b: 1}, [(a, 0, dict(o)), (b, 0, dict(o))])

    rid = _rid()
    ma, d = _goi(may, LO, than={"chup_id": cid, "source_ids": [a, b],
                                "run_id": rid})
    assert ma == 200, d
    assert d["data"]["so_nguon_vao"] == 2, d["data"]
    assert d["data"]["vao_so"] == 2, (
        "⛔⛔ chỉ %s dòng vào sổ cho HAI nguồn có dòng y hệt nhau ⇒ cửa đã "
        "NỐI PHẲNG dưới một `NgucCanh`, và `content_key` coi chúng là TRÙNG"
        % d["data"]["vao_so"])
    assert d["data"]["trung"] == 0, d["data"]
    assert _dem(rid) == 2

    # ⭐ Và hai dòng ấy phải mang **hai `source_sheet` KHÁC NHAU** — đó là
    #   thứ làm `content_key` của chúng khác nhau.
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT DISTINCT source_sheet FROM fls_itl"
                    " WHERE run_id = %s ORDER BY 1", (rid,))
        assert [r[0] for r in cur.fetchall()] == sorted([ka, kb])


# ═════════════════════════ ⓑ `run_id` của cả lô ════════════════════════
def test_row_count_cua_fls_run_la_TONG_ca_lo(may):
    """⛔ `mo_run` có `ON CONFLICT DO NOTHING` ⇒ staging là của nguồn ĐẦU."""
    a, _ = _nguon_day_du()
    b, _ = _nguon_day_du()
    cid = _chup({a: 1, b: 1},
                [(a, 0, _o()), (a, 1, _o()), (b, 0, _o())])   # 2 + 1
    rid = _rid()
    ma, d = _goi(may, LO, than={"chup_id": cid, "source_ids": [a, b],
                                "run_id": rid})
    assert (ma, d["data"]["vao_so"]) == (200, 3), d

    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*), max(row_count) FROM fls_run"
                    " WHERE run_id = %s", (rid,))
        so_dong_run, row_count = cur.fetchone()
    assert so_dong_run == 1, "⛔ một lô phải sinh ĐÚNG một dòng `fls_run`"
    assert row_count == 3, (
        "⛔ `row_count` = %s ⛔ không phải 3 ⇒ nó đang là số của nguồn ĐẦU "
        "TIÊN, ⛔ không phải tổng của lô" % row_count)


# ══════════════════ ⓒ nguồn RỖNG ⛔ không làm cả lô đỏ oan ═══════════════
def test_nguon_RONG_KHONG_lam_ca_lo_DO_OAN(may):
    """⭐⭐⭐ Đo thật: **10/60** nguồn đọc ra 0 dòng — ⛔ không phải khuyết tật.

    Với chúng `S2`…`S7` trả `dat=False, da_do=0` *(đúng luật nền "xanh trên
    tập RỖNG là CHƯA ĐO")*. ⇒ Gộp bằng `all(dat)` thì cả lô đỏ **6/9 luật**
    trong khi mọi nguồn có dữ liệu đều đạt.
    """
    a, _ = _nguon_day_du()          # co dong
    b, kb = _nguon_day_du()         # RONG
    cid = _chup({a: 1, b: 1}, [(a, 0, _o()), (a, 1, _o())])

    ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b]})
    assert ma == 200, d
    theo = {k["ten"]: k for k in d["data"]["luat"]}
    s3 = next(k for t, k in theo.items() if t.startswith("S3"))
    assert s3["dat"] is True, (
        "⛔⛔ `S3` đỏ vì một nguồn RỖNG ⇒ báo động ĐỎ OAN, và một báo động "
        "đỏ oan là một báo động sẽ bị bỏ qua: %s" % s3["thong_diep"])
    assert s3["da_do"] == 2, s3
    # ⭐ Nhưng nguồn rỗng **⛔ không bị GIẤU** — nó hiện ở một ô RIÊNG.
    assert s3["nguon_chua_do"] == [kb], s3
    assert s3["so_nguon_chua_do"] == 1
    assert s3["nguon_khong_dat"] == []


def test_MOI_nguon_RONG_thi_ca_lo_CHUA_DO(may):
    """⛔ Luật nền **vẫn đứng ở tầng lô**: `da_do` gộp = 0 ⇒ ⛔ KHÔNG ĐẠT.

    Một nguồn rỗng trong 60 ⛔ không làm cả lô thành *chưa đo*; **60 nguồn
    rỗng thì CÓ**.
    """
    a, _ = _nguon_day_du()
    b, _ = _nguon_day_du()
    cid = _chup({a: 1, b: 1}, [])
    _ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b]})
    s3 = next(k for k in d["data"]["luat"] if k["ten"].startswith("S3"))
    assert (s3["dat"], s3["da_do"]) == (False, 0), s3
    assert "CHƯA ĐO" in s3["thong_diep"], s3["thong_diep"]


# ══════════════════════ ⓓ `111` — chừa nguồn `CHẶN` ═════════════════════
def test_nguon_CHAN_bi_CHUA__nguon_sach_VAN_VAO_SO(may):
    """⭐⭐⭐ Câu chứng minh của `QĐ-ITL-111`.

    Nguồn ⛔ **chưa thu dải đọc** ⇒ `S10` hạng `CHẶN` đỏ ⇒ **bị chừa**. Nguồn
    còn lại **vẫn vào sổ**, và biên bản **nêu rõ luật nào** chừa nó.
    """
    a, _ = _nguon_day_du()                      # sach
    b, kb = _nguon_day_du(dai=False)            # ⛔ thieu dai ⇒ S10 CHAN
    cid = _chup({a: 1, b: 1}, [(a, 0, _o()), (b, 0, _o())])

    rid = _rid()
    ma, d = _goi(may, LO, than={"chup_id": cid, "source_ids": [a, b],
                                "run_id": rid})
    assert ma == 200, d
    dd = d["data"]
    assert (dd["so_nguon"], dd["so_nguon_vao"], dd["so_nguon_chua"]) == (2, 1, 1)
    assert dd["vao_so"] == 1, dd
    assert _dem(rid) == 1

    bi = next(n for n in dd["nguon"] if n["bi_chua"])
    assert bi["source_key"] == kb
    assert bi["chua_vi"] and bi["chua_vi"][0].startswith("S10"), (
        "⛔ chừa mà ⛔ KHÔNG nói vì LUẬT NÀO thì kế toán ⛔ không có đường "
        "nào sửa — và cú bỏ tick lại quay về ⛔ không để lại vết")
    # ⛔ Ba đường cộng theo nguồn SẼ VÀO, ⛔ không gộp cả nguồn bị chừa.
    assert dd["so_dong_vao"] == 1, dd


def test_CA_LO_deu_CHAN_thi_422_KEM_bien_ban(may):
    """⛔ Nói *"⛔ không nạp được gì"* mà ⛔ không nói **nguồn nào, luật nào**
    là bắt người ta đoán."""
    a, _ = _nguon_day_du(dai=False)
    b, _ = _nguon_day_du(dai=False)
    cid = _chup({a: 1, b: 1}, [(a, 0, _o()), (b, 0, _o())])
    rid = _rid()
    ma, d = _goi(may, LO, than={"chup_id": cid, "source_ids": [a, b],
                                "run_id": rid})
    assert ma == 422 and d["error"]["code"] == "FLS-SOAT-CHAN", d
    bb = d["error"]["bien_ban"]
    assert bb["so_nguon_vao"] == 0 and bb["so_nguon_chua"] == 2
    assert all(n["chua_vi"] for n in bb["nguon"]), bb["nguon"]
    assert _dem(rid) == 0, "⛔ bị từ chối mà VẪN ghi một phần"


# ══════════════════════ ⓔ `112` — biên bản GỘP ══════════════════════════
def test_bien_ban_GOP_dung_9_dong__khong_phai_9_nhan_N(may):
    """⛔ Câu kế toán hỏi là *"lô này vào được ⛔ không"* — **9 dòng** trả lời
    được, `9 × N` dòng thì ⛔ không."""
    a, _ = _nguon_day_du()
    b, _ = _nguon_day_du()
    c, _ = _nguon_day_du()
    cid = _chup({a: 1, b: 1, c: 1},
                [(a, 0, _o()), (b, 0, _o()), (c, 0, _o())])
    _ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b, c]})
    assert len(d["data"]["luat"]) == 9, len(d["data"]["luat"])
    assert len(d["data"]["nguon"]) == 3
    # ⭐ `da_do` phải là **Σ**, ⛔ không phải của nguồn đầu tiên.
    s3 = next(k for k in d["data"]["luat"] if k["ten"].startswith("S3"))
    assert s3["da_do"] == 3, s3


def test_hang_gop_la_NANG_NHAT__khong_phai_cua_nguon_dau(may):
    """⛔ Hai nguồn có thể cho **cùng một luật hai hạng khác nhau** (`S10`)."""
    a, _ = _nguon_day_du()                      # S10 hang CO, xanh
    b, _ = _nguon_day_du(dai=False)             # S10 hang CHAN, do
    cid = _chup({a: 1, b: 1}, [(a, 0, _o()), (b, 0, _o())])
    _ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b]})
    s10 = next(k for k in d["data"]["luat"] if k["ten"].startswith("S10"))
    assert s10["hang"] == "CHAN", s10
    assert s10["dat"] is False and s10["so_nguon_khong_dat"] == 1, s10


def test_XEM_TRUOC_lo_KHONG_ghi_mot_dong_nao(may):
    """⭐ Tuyến xem-trước chạy trên **kết nối bị kho CHẶN GHI**."""
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o()), (a, 1, _o())])
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl")
        truoc = cur.fetchone()[0]
    ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a]})
    assert (ma, d["data"]["se_ghi"]) == (200, True), d
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl")
        assert cur.fetchone()[0] == truoc, "⛔ xem trước mà GHI vào sổ"


# ══════════════════════ ⓕ ⛔ KHÔNG mặc định lấy-hết ═════════════════════
@pytest.mark.parametrize("than_them", [
    {},                                  # ⛔ thieu `source_ids`
    {"source_ids": []},                  # ⛔ rong
    {"source_ids": "12"},                # ⛔ chuoi
    {"source_ids": [True]},              # ⛔ `bool` la con cua `int`
    {"source_ids": ["12"]},              # ⛔ chuoi trong danh sach
])
def test_source_ids_LA_thi_400__KHONG_am_tham_lay_het(may, than_them):
    """⛔⛔ Máy ⛔ **KHÔNG** tự chọn nguồn nào cho một lô tiền.

    Đúng 59 lần rồi sai lần thứ 60 là nạp **dữ liệu ⛔ không ai yêu cầu**, và
    biên bản sẽ trông **hoàn toàn bình thường**.
    """
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o())])
    ma, d = _goi(may, XEM, than=dict({"chup_id": cid}, **than_them))
    assert ma == 400, (than_them, ma, d)


def test_source_ids_TRUNG_LAP_chi_soat_MOT_lan(may):
    """⛔ Gửi cùng một nguồn hai lần ⛔ không được nạp nó hai lần."""
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o())])
    _ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, a, a]})
    assert d["data"]["so_nguon"] == 1, d["data"]


def test_nguon_KHONG_trong_anh_chup_thi_409(may):
    a, _ = _nguon_day_du()
    b, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o())])          # ⛔ anh ⛔ khong co `b`
    ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b]})
    assert ma == 409 and d["error"]["code"] == "FLS-CHUP-KHONG-NGUON", d


def test_lo_NAP_ghi_dung_chup_id_vao_fls_run(may):
    """⭐ Truy vết: `fls_itl.run_id` → `fls_run.chup_id` → ảnh chụp."""
    a, _ = _nguon_day_du()
    cid = _chup({a: 1}, [(a, 0, _o())])
    rid = _rid()
    ma, _d = _goi(may, LO, than={"chup_id": cid, "source_ids": [a],
                                 "run_id": rid})
    assert ma == 200
    with psycopg.connect(dsn_test()) as c, c.cursor() as cur:
        cur.execute("SELECT chup_id FROM fls_run WHERE run_id = %s", (rid,))
        assert cur.fetchone()[0] == cid


# ═════ ⓖ ⭐⭐⭐ bài ghim đúng khuyết tật mà chính bộ này bắt được ═════
def test_luat_CHUA_mot_nguon_thi_KHONG_BAO_GIO_bao_DAT(may):
    """⛔⛔⛔ Khuyết tật THẬT, bắt được 08/09 trong chính lượt viết phép gộp.

    Bản đầu của `_gop_luat` xếp *"⛔ không đạt"* theo `da_do > 0`. Nhưng
    `s10_o_cua` khi ⛔ chưa thu dải trả `(CHAN, dat=False, **da_do=0**)` ⇒
    nguồn ấy rơi vào ô `chua_do`, và phép gộp báo **`S10` ĐẠT** — **trong khi
    `S10` đang CHỪA chính nguồn đó**.

    ⭐ `da_do = 0` **⛔ không** phân biệt được hai thứ khác hẳn nhau:
      *"⛔ không có gì để đo"* *(nguồn 0 dòng, hạng `CO`)* và *"có thứ để đo
      mà ⛔ không đo được"* *(thiếu bản khai thứ hai, hạng `CHAN`)*. **Hạng**
      thì phân biệt được.

    ⇒ Bài này canh **cả hai vế** cùng lúc, và nó là **chỗ duy nhất** phát
      biểu tính chất *"bấm vào một luật đỏ thì thấy được nguồn bị chừa"*.
    """
    a, _ = _nguon_day_du()
    b, kb = _nguon_day_du(dai=False)        # ⛔ S10 CHAN · da_do = 0
    cid = _chup({a: 1, b: 1}, [(a, 0, _o()), (b, 0, _o())])
    _ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b]})
    dd = d["data"]

    bi = next(n for n in dd["nguon"] if n["bi_chua"])
    assert bi["source_key"] == kb and bi["chua_vi"], bi
    for ten in bi["chua_vi"]:
        g = next(k for k in dd["luat"] if k["ten"] == ten)
        assert g["dat"] is False, (
            "⛔⛔ luật `%s` báo ĐẠT trong khi nó đang CHỪA nguồn `%s` — biên "
            "bản đang che đúng thứ nó sinh ra để phơi" % (ten, kb))
        assert kb in g["nguon_khong_dat"], (
            "⛔ bấm vào luật `%s` sẽ ⛔ KHÔNG thấy nguồn `%s`" % (ten, kb))
        assert kb not in g["nguon_chua_do"], (
            "⛔ hạng CHẶN bị miễn bằng *chưa đo* — đúng khuyết tật đã cắn")


def test_da_do_0_hang_CO_thi_VAN_la_chua_do__khong_bi_ke_thanh_loi(may):
    """⛔ Chiều NGƯỢC của bài trên: đừng vá quá tay thành *"đỏ hết"*.

    Nguồn 0 dòng làm `S2`…`S7` *(hạng `CO`)* trả `da_do=0`. Chúng **phải** ở
    ô `chua_do` — kể chúng thành lỗi là quay về **báo oan**, mà 10/60 nguồn
    thật đọc ra 0 dòng.
    """
    a, _ = _nguon_day_du()
    b, kb = _nguon_day_du()                 # RONG
    cid = _chup({a: 1, b: 1}, [(a, 0, _o())])
    _ma, d = _goi(may, XEM, than={"chup_id": cid, "source_ids": [a, b]})
    for k in d["data"]["luat"]:
        if k["ten"].startswith(("S2", "S3", "S4", "S5", "S7")):
            assert kb in k["nguon_chua_do"], (k["ten"], k)
            assert kb not in k["nguon_khong_dat"], (k["ten"], k)
            assert k["dat"] is True, (k["ten"], k["thong_diep"])
