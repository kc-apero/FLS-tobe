# -*- coding: utf-8 -*-
"""`fls/repo/nap_lo.py` trên PG THẬT — nạp một lô sao kê.

⭐ **CỔNG CỦA TASK 5** *(`DEV-03` §2b)*: nạp **hai lần cùng một tệp** ⇒ `trùng: N`
   và ⛔ **0 dòng nhân đôi** — `test_NAP_HAI_LAN_cung_tep_KHONG_nhan_doi`.
"""
import os

import psycopg
import pytest

from fls.adapters.sao_ke import I_CO, I_MA, I_NGAY, I_NO, I_TE, KHUON_RA
from fls.db.kho import dsn_test
from fls.kiem.soat_nap import CANH, CHAN, CO_, KetQuaSoat
from fls.ledger.build import NgucCanh
from fls.repo.nap_lo import LoBiChan, nap_lo

pytestmark = pytest.mark.pg

# ⛔ Kho TEST, ⛔ KHÔNG phải kho thật.
DSN = dsn_test()


@pytest.fixture()
def conn():
    with psycopg.connect(DSN, autocommit=True) as c:
        yield c


def _hang(ngay="2026-01-05", ma="FT001", no=1000, co="", te="VND"):
    r = [""] * len(KHUON_RA)
    r[I_NGAY], r[I_MA], r[I_NO], r[I_CO], r[I_TE] = ngay, ma, no, co, te
    return r


def _nc(tag: str | None = None) -> NgucCanh:
    # ⛔ `run_id` phải đúng hình BẢN TRẮNG `NAP-yyyy-mm-dd-NGUON` — sai hình
    #    thì dòng vào sổ được mà ⛔ không cửa đọc nào thấy.
    tag = (tag or os.urandom(4).hex()).upper()
    return NgucCanh(run_id="NAP-2026-01-05-" + tag, contract_version="v1.1",
                    canon_version="v1.0", mapping_version="v1.0",
                    source_system="P100", source_sheet="R | Thu" + tag)


def _luat(hang: str = CANH, dat: bool = True, da_do: int = 3,
          dong_xau: tuple[int, ...] = ()) -> KetQuaSoat:
    """⭐ `dong_xau` = chỉ số **0-based** các dòng luật này chỉ đích danh.

    ⛔ Mặc định `()` — ⛔ **không** phải *"không dòng nào xấu"* mà là ***"luật
    này ⛔ không chỉ ra được dòng"*** (`S1`/`S6`/`S8`/`S10` đo ở mức sheet).
    Một luật như thế ⇒ ⛔ **0** sự kiện lý do. Xem `GAP-NAP-01`.
    """
    return KetQuaSoat(ten="S-thu", hang=hang, dat=dat, da_do=da_do,
                      thong_diep="thu", dong_xau=dong_xau)


def _dem_so(conn, run_id: str) -> int:
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl WHERE run_id = %s", (run_id,))
        return int(cur.fetchone()[0])


# ─────────────────────────────────────────────────── đường đi được, trước hết
def test_nap_mot_lo_vao_so(conn):
    nc = _nc()
    kq = nap_lo(conn, [_hang(ma="A"), _hang(ma="B")], nc, [_luat()],
                actor="thanh")
    assert kq.nap.vao == 2 and kq.nap.vao_so == 2
    assert kq.nap.can(), "⛔ bốn đường ⛔ không cân: " + kq.nap.bao()
    assert _dem_so(conn, nc.run_id) == 2


def test_dong_KHONG_co_ngay_la_RONG_chu_khong_phai_LOI(conn):
    """⛔ Đệm của trang tính ⛔ không phải một giao dịch — nhưng nó **vẫn phải
    được đếm**, nếu không thì cổng bốn đường ⛔ không bao giờ cân."""
    nc = _nc()
    kq = nap_lo(conn, [_hang(), _hang(ngay=""), _hang(ngay="   ")], nc,
                [_luat()], actor="thanh")
    assert (kq.nap.vao, kq.nap.vao_so, kq.nap.rong) == (3, 1, 2)
    assert kq.nap.can()


def test_o_LOI_o_cot_khoa_thi_LOAI_co_ly_do_CO_TEN(conn):
    nc = _nc()
    kq = nap_lo(conn, [_hang(), _hang(ma="#REF!")], nc, [_luat()],
                actor="thanh")
    assert (kq.nap.vao_so, kq.nap.loai) == (1, 1)
    assert kq.nap.ly_do_loai, "⛔ dòng bị loại mà ⛔ không có lý do CÓ TÊN"
    assert kq.nap.can()


# ──────────────────────────────────────── ⭐ CỔNG CỦA TASK 5 — chống trùng
def test_NAP_HAI_LAN_cung_tep_KHONG_nhan_doi(conn):
    """⭐⭐ **CỔNG CỦA TASK 5.**

    ⛔⛔ Và điều đáng nói ⛔ không phải *"có chống trùng"* — mà là **⛔ KHÔNG
    dựng cơ chế chống trùng THỨ HAI** *(`BA-07` §4b ⓹)*. `content_key` đã
    `NOT NULL` từ migration `0001`; lằn `F04` **dùng lại đúng nó**, qua đúng
    `chay_nap.chay()`. Hai cơ chế chống trùng là **hai chỗ để chúng lệch nhau**.
    """
    nc = _nc()
    lo = [_hang(ma="A"), _hang(ma="B"), _hang(ma="C")]

    lan1 = nap_lo(conn, lo, nc, [_luat()], actor="thanh")
    assert (lan1.nap.vao_so, lan1.nap.bo_qua_trung) == (3, 0)

    lan2 = nap_lo(conn, lo, nc, [_luat()], actor="thanh")
    assert lan2.nap.bo_qua_trung == 3, "⛔ lần 2 phải BỎ QUA cả 3 dòng"
    assert lan2.nap.vao_so == 0, "⛔ lần 2 ⛔ không được ghi thêm dòng nào"
    assert lan2.nap.can(), "⛔ bốn đường ⛔ không cân ở lần 2"
    assert _dem_so(conn, nc.run_id) == 3, "⛔ SỔ ĐÃ NHÂN ĐÔI"


def test_dong_TRUNG_NOI_DUNG_trong_CUNG_mot_lo_van_vao_DU(conn):
    """⛔⛔ Trùng **nội dung** ⛔ KHÔNG phải trùng **lần nạp**.

    Sổ thật có **281 dòng trùng nội dung** *(cùng ngày, cùng tiền, cùng số
    chứng từ)* — chúng là **giao dịch THẬT khác nhau**. `seq_trung` sinh ra để
    giữ chúng; ⛔ không có nó thì `ON CONFLICT DO NOTHING` **nuốt gần hết**, và
    con số *"bỏ qua"* sẽ bị đọc thành *"nạp lại lần hai"* thay vì **MẤT DỮ
    LIỆU**.
    """
    nc = _nc()
    kq = nap_lo(conn, [_hang(ma="X"), _hang(ma="X"), _hang(ma="X")], nc,
                [_luat()], actor="thanh")
    assert kq.nap.vao_so == 3, "⛔ 3 giao dịch thật bị nuốt thành 1"
    assert kq.nap.bo_qua_trung == 0


# ─────────────────────────────────────────────── hạng CHẶN ⇒ ⛔ 0 dòng
def test_luat_hang_CHAN_do_thi_KHONG_ghi_MOT_DONG_NAO(conn):
    nc = _nc()
    with pytest.raises(LoBiChan) as e:
        nap_lo(conn, [_hang(), _hang(ma="B")], nc,
               [_luat(hang=CHAN, dat=False)], actor="thanh")
    assert e.value.ma == "FLS-SOAT-CHAN"
    assert _dem_so(conn, nc.run_id) == 0, "⛔ CHẶN đỏ mà VẪN ghi vào sổ"


def test_luat_CHAN_do_do_duoc_0_THU_cung_la_CHAN(conn):
    """⛔ Luật nền: **đo được `0` thứ ⇒ ⛔ KHÔNG ĐẠT**. Một luật `dat=True` mà
    `da_do=0` là *"chưa đo"*, ⛔ không phải *"đạt"*."""
    nc = _nc()
    with pytest.raises(LoBiChan):
        nap_lo(conn, [_hang()], nc, [_luat(hang=CHAN, dat=True, da_do=0)],
               actor="thanh")
    assert _dem_so(conn, nc.run_id) == 0


# ─────────────────────────────── hạng CỜ ⇒ VẪN ghi + vào hàng chờ có lý do
def test_hang_CO_do_thi_VAN_GHI_va_dong_vao_HANG_CHO_CO_LY_DO(conn):
    """⭐⭐ `CỜ` là khuyết tật **có sẵn trong sổ kế toán**, ⛔ không phải lỗi FLS.

    Chặn ở đây nghĩa là FLS **⛔ không bao giờ nạp được gì** — mà những dòng ấy
    là **TIỀN THẬT**. ⇒ Vào sổ, **mang một lý do**, và **có người phải trả lời**.
    """
    nc = _nc()
    kq = nap_lo(conn, [_hang(ma="A"), _hang(ma="B")], nc,
                [_luat(hang=CO_, dat=False, dong_xau=(0, 1))], actor="thanh")
    assert kq.nap.vao_so == 2, "⛔ hạng CỜ ⛔ không được chặn — đó là tiền thật"
    assert kq.vao_hang_cho == 2
    with conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM fls_queue_event q JOIN fls_itl i"
            " ON i.itl_id = q.itl_id WHERE i.run_id = %s AND q.evt_type='reason'",
            (nc.run_id,))
        assert int(cur.fetchone()[0]) == 2


def test_LY_DO_phai_NEU_TEN_LUAT_chu_khong_phai_mot_chu_chung(conn):
    """⛔ Một hàng chờ mà mọi dòng mang cùng câu *"cần xem lại"* là hàng chờ
    ⛔ **không ai đọc** — và `US-045` đếm chính cột lý do ấy."""
    nc = _nc()
    nap_lo(conn, [_hang()], nc,
           [KetQuaSoat(ten="S2 · có tiền thì phải có mã", hang=CO_, dat=False,
                       da_do=1, thong_diep="7 dòng", dong_xau=(0,))],
           actor="thanh")
    with conn.cursor() as cur:
        cur.execute(
            "SELECT q.reason FROM fls_queue_event q JOIN fls_itl i"
            " ON i.itl_id = q.itl_id WHERE i.run_id = %s", (nc.run_id,))
        ly_do = [r[0] for r in cur.fetchall()]
    assert ly_do and "S2" in ly_do[0], ly_do


def test_luat_XANH_HET_thi_KHONG_ai_vao_hang_cho(conn):
    """⛔ Cổng chung #7 — chứng minh bài trên ⛔ **không xanh vì luôn gắn**."""
    nc = _nc()
    kq = nap_lo(conn, [_hang(), _hang(ma="B")], nc, [_luat()], actor="thanh")
    assert kq.vao_hang_cho == 0
    with conn.cursor() as cur:
        cur.execute(
            "SELECT count(*) FROM fls_queue_event q JOIN fls_itl i"
            " ON i.itl_id = q.itl_id WHERE i.run_id = %s", (nc.run_id,))
        assert int(cur.fetchone()[0]) == 0


def test_actor_RONG_thi_NO_va_KHONG_ghi_gi(conn):
    """⛔ Một lô nạp là **hành vi của người bấm `Nhận`**."""
    nc = _nc()
    with pytest.raises(ValueError, match="actor"):
        nap_lo(conn, [_hang()], nc, [_luat()], actor="  ")
    assert _dem_so(conn, nc.run_id) == 0


# ────────────────────────────── ⛔ KHÔNG dựng cơ chế chống trùng THỨ HAI
def test_nap_lo_KHONG_co_cau_INSERT_nao():
    """⛔⛔ Quét MÃ NGUỒN: `nap_lo.py` ⛔ không được tự ghi.

    Nó phải đi qua `chay_nap.chay()` *(chống trùng + cổng bốn đường + một giao
    dịch)* và `ghi_tay.ghi_ly_do()` *(nhật ký — lớp kiểm soát cuối cùng)*. Một
    câu `INSERT` ở đây là **một đường vòng qua cả hai**.
    """
    import ast
    import pathlib

    f = pathlib.Path(__file__).resolve().parents[2] / "fls" / "repo" / "nap_lo.py"
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    xau = [n.value for n in ast.walk(cay)
           if isinstance(n, ast.Constant) and isinstance(n.value, str)
           and " ".join(n.value.lower().split()).startswith(
               ("insert into", "update ", "delete from"))]
    assert xau == [], "⛔ nap_lo.py tu ghi: " + " · ".join(x[:60] for x in xau)


def test_nap_lo_THAT_SU_goi_hai_duong_da_khai():
    """⛔ Cổng chung #7: nếu nó ⛔ không gọi gì thì bài trên xanh mà ⛔ không
    bảo vệ gì."""
    import ast
    import pathlib

    f = pathlib.Path(__file__).resolve().parents[2] / "fls" / "repo" / "nap_lo.py"
    cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
    goi = {n.func.id for n in ast.walk(cay)
           if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)}
    assert "chay" in goi, "⛔ ⛔ không gọi `chay_nap.chay()`"
    assert "ghi_ly_do" in goi, "⛔ ⛔ không gọi `ghi_tay.ghi_ly_do()`"


def test_run_id_SAI_HINH_thi_NO_TRUOC_khi_ghi(conn):
    """⛔⛔ Một lô nạp bằng `run_id` sai hình sẽ **vào sổ được** nhưng ⛔ **không
    cửa đọc nào thấy** — vì mọi cửa lọc theo `PhamVi`, và `PhamVi` là **bản
    TRẮNG** *(`run_id ~ NAP-yyyy-mm-dd-NGUON`)*.

    ⇒ Một lần nạp **im lặng rơi vào hư không**, và ⛔ không cổng nào báo gì.

    ⚠ Lỗ này tự lộ ra khi viết bài test *(đường ghi lý do nổ `NgoaiPhamVi`)* —
      nhưng nó **CHỈ** nổ khi lô **có cờ**. Lô sạch thì đi qua **êm ru**. Nên
      phép kiểm phải đứng riêng, ⛔ không dựa vào việc một đường khác tình cờ
      nổ hộ. Bài này khoá đúng chỗ đó: **lô SẠCH, và vẫn phải NỔ**.
    """
    xau = NgucCanh(run_id="lo-tam-bay", contract_version="v1.1",
                   canon_version="v1.0", mapping_version="v1.0",
                   source_system="P100", source_sheet="R | Thu")
    with pytest.raises(ValueError, match="hư không"):
        nap_lo(conn, [_hang()], xau, [_luat()], actor="thanh")
    assert _dem_so(conn, xau.run_id) == 0


# ── `GAP-NAP-01` — ly do phai DUNG VE DONG NO CHI ────────────────────────
def _ly_do_theo_dong(conn, run_id: str) -> dict[int, str]:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT i.source_row, q.reason FROM fls_queue_event q"
            "  JOIN fls_itl i ON i.itl_id = q.itl_id"
            " WHERE i.run_id = %s AND q.evt_type = 'reason'", (run_id,))
        return {int(r[0]): r[1] for r in cur.fetchall()}


def test_LY_DO_chi_gan_cho_DONG_BI_CHI_chu_KHONG_ca_lo(conn):
    """⛔⛔⛔ **`GAP-NAP-01`: cau ly do tung dung cho CA LO, va no SAI.**

    Do tren so THAT 11/09, truoc khi va:

        `S3 · moi dong phai co TIEN` gan **2.596** dong — ca 2.596 **DEU CO
           TIEN**  ⇒ bao oan **100%**
        `S7 · dong trung HOAN TOAN`  gan **5.952** dong — chi **66** that su
           trung ⇒ bao oan **98,9%**

    Ke toan mo hang cho va doc mot cau **sai** ve dong dang o truoc mat. Mot
    hang cho nhu the ⛔ khong ai doc lan thu hai.

    ⇒ Bai nay dung ba dong, luat chi **dong giua**. Chi dong giua duoc gan.
    """
    nc = _nc()
    nap_lo(conn, [_hang(ma="A"), _hang(ma="B"), _hang(ma="C")], nc,
           [_luat(hang=CO_, dat=False, dong_xau=(1,))], actor="thanh")
    assert _ly_do_theo_dong(conn, nc.run_id).keys() == {2}, (
        "⛔ luat chi dong thu 2 (`dong_xau=(1,)` ⇒ `source_row=2`) ma su kien "
        "lai roi sang dong khac — dung cai loi `GAP-NAP-01` vua va")


def test_LUAT_MUC_SHEET_khong_dong_dau_len_dong_nao(conn):
    """⛔⛔ **Ve KIA cua cung mot cai va, va no de bi bo quen nhat.**

    `S1`/`S6`/`S8`/`S10` do o muc **sheet** hay **ban khai** — chung that su
    ⛔ khong co dong de chi (`dong_xau = ()`). Neu ban va chi lo *"gan dung
    dong"* ma van coi `()` la *"gan het"* thi ⛔ khong sua duoc gi ca.

    ⇒ `()` phai co nghia ***"luat nay ⛔ khong chi ra duoc dong"***, va luat
      nhu the sinh **0** su kien. No van **DO trong bien ban** — cho cua no la
      o do, ⛔ khong phai tren tung dong.
    """
    nc = _nc()
    kq = nap_lo(conn, [_hang(ma="A"), _hang(ma="B")], nc,
                [_luat(hang=CO_, dat=False)], actor="thanh")
    assert kq.vao_hang_cho == 0
    assert _ly_do_theo_dong(conn, nc.run_id) == {}
    # ⛔ Nhung no VAN phai do trong bien ban — bai nay ⛔ khong duoc lam luat
    #   muc sheet BIEN MAT.
    assert any(not k.xanh for k in kq.luat), (
        "⛔ luat muc sheet vua bi lam cho im lang — no phai VAN DO")


def test_HAI_LUAT_cung_cham_mot_dong_thi_cau_ly_do_NEU_CA_HAI(conn):
    """⛔ Mot dong hong hai kieu ma chi bao mot kieu thi nguoi sua no se sua
    mot nua roi tuong da xong."""
    nc = _nc()
    nap_lo(conn, [_hang(ma="A"), _hang(ma="B")], nc,
           [_luat(hang=CO_, dat=False, dong_xau=(0,)),
            KetQuaSoat(ten="S7 · dong trung", hang=CO_, dat=False, da_do=2,
                       thong_diep="thu", dong_xau=(0,))], actor="thanh")
    ly_do = _ly_do_theo_dong(conn, nc.run_id)
    assert list(ly_do) == [1]
    assert "S-thu" in ly_do[1] and "S7" in ly_do[1], ly_do
