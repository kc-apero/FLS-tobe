"""Mốc `A3` — NẠP một ảnh LỆNH CHI mới. `QĐ-ITL-119`.

⛔⛔⛔ **Cổng ra thật của `A3` ⛔ KHÔNG phải *"nạp được dữ liệu vào ⛔ không"* —
   nó là *"có dịch được một dòng nào ⛔ không"*.**

Đo 09/09: **3.703 dòng lệnh chi, tất cả từ MỘT lượt ngày 27/08** — đóng băng
**13 ngày**, và ⛔ không cổng nào nói lên điều đó vì ⛔ không gì trong kho ghi
*"ảnh này đọc lúc nào, ai đọc"*. ⇒ Lằn nạp này chở **bốn thứ** mà một câu
`INSERT` ⛔ không chở: `doc_luc` · `actor` · `giay` · `spreadsheet_id`, cộng
`fls_run.chup_id` *(vết truy `QĐ-ITL-115` đòi)*.

★ Và bốn bài dưới đây canh bốn cách nó **hỏng trong im lặng**:
  ⓐ ⛔ ảnh RỖNG ⇒ NỔ *(một dấu thời điểm ⛔ không đo được gì)*;
  ⓑ ⛔ không một số nào lưu **hai lần** *(`fls_chup_dong` phải RỖNG)*;
  ⓒ `so_dong` của ảnh phải **ĐO** được, ⛔ không báo `0` khi kho có 3 dòng;
  ⓓ nạp **lại** cùng tệp ⇒ `so_ma_moi = 0` *(chuyện thường)*, và ảnh cũ
    ⛔ không đổi một ô.
"""
from __future__ import annotations

import uuid
from decimal import Decimal as D

import psycopg
import pytest

from fls.adapters.pm_join import PM_KHAI_VERSION, DongPM, canon_ref
from fls.db.kho import dsn_test
from fls.repo import chup as ch
from fls.repo.anh_pm import anh_pm_hieu_luc
from fls.repo.chay_nap import nap_anh_pm
from fls.repo.doc_bao_cao import ung_vien_pm
from fls.repo.pham_vi import chi_nap_that

pytestmark = pytest.mark.pg

SID = "1md85t-BAI-KIEM"


def _hex(n: int = 6) -> str:
    return uuid.uuid4().hex[:n].upper()


@pytest.fixture()
def conn():
    with psycopg.connect(dsn_test(), autocommit=True) as c:
        yield c


@pytest.fixture()
def nguon_pm(conn):
    """Một `fls_source` kiểu **`PM`** — ⛔ không phải một sheet sao kê."""
    return conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s, %s) RETURNING source_id",
        ("PM_Unpivot bai kiem " + _hex(8), ch.LAN_PM_SRC)).fetchone()[0]


def _lenh(ref: str, tien: str, tt: str, line: str, dong: int = 3) -> DongPM:
    """⚠ `dong` = `source_row`, va `fls_pm_line` co khoa DUY NHAT
    `(run_id, source_row)` ⇒ moi dong phai co mot so RIENG. Dung `3` cho moi
    dong la dung mot kho bai ⛔ khong the nap qua mot dong."""
    return DongPM(dong, line.split("-")[0], line, D(tien), tt, "Approve",
                  canon_ref(ref), "HD-1", "CDT-1", ref_tho=ref)


# ── ⓐ ảnh RỖNG ⇒ NỔ ─────────────────────────────────────────────────────
def test_anh_RONG_thi_NO__khong_ghi_mot_dau_thoi_diem_gia(conn, nguon_pm):
    truoc = conn.execute("SELECT count(*) FROM fls_chup WHERE lan='PM'"
                         ).fetchone()[0]
    with pytest.raises(ValueError) as e:
        nap_anh_pm(conn, [], spreadsheet_id=SID, actor="cron",
                   source_id=nguon_pm)
    assert "KHÔNG ghi một ảnh lệnh chi RỖNG" in str(e.value)
    assert conn.execute("SELECT count(*) FROM fls_chup WHERE lan='PM'"
                        ).fetchone()[0] == truoc


def test_nguon_KHONG_phai_kieu_PM_thi_NO(conn):
    """⛔ Chụp lằn `PM` vào một nguồn **sao kê** là trộn hai lằn khác khuôn RA.

    ⚠ Và nó ⛔ không phải một lỗi lý thuyết: `fls_source` ⛔ **không có `CHECK`**
      trên `src_type`, nên chỗ duy nhất chặn được là tầng ghi này.
    """
    bank = conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s,'Bank') RETURNING source_id",
        ("R | bai kiem " + _hex(8),)).fetchone()[0]
    with pytest.raises(ch.LoiChup) as e:
        nap_anh_pm(conn, [_lenh("FT-1", "100.00", "VND", "PMX-1")],
                   spreadsheet_id=SID, actor="cron", source_id=bank)
    assert "src_type" in str(e.value)


# ── ⓑ+ⓒ một số ⛔ KHÔNG lưu hai lần, và `so_dong` phải ĐO được ──────────
def test_KHONG_mot_so_nao_luu_HAI_LAN__va_so_dong_van_DO_duoc(conn, nguon_pm):
    """⭐⭐⭐ Hai điều **cùng lúc**, và chúng kéo nhau ngược chiều.

    ⛔ `fls_chup_dong` phải **RỖNG** *(`fls_pm_line` CHÍNH LÀ bảng dòng của lằn
      này — chép sang là lưu cùng những con số ở hai chỗ, và hai chỗ ấy sẽ
      lệch)*. ⛔ **Nhưng** `so_dong` của ảnh vẫn phải nói **3**, ⛔ không phải
      `0` — nếu ⛔ không thì `F04` hiện nó như *"đã đọc lúc 15:02 · 0 dòng"*,
      đúng lời nói dối mà `chup.py` dựng ra để chặn, chỉ theo chiều ngược lại.
    """
    tt = "P" + _hex(5)
    ds = [_lenh("FT-A-" + _hex(), "100.00", tt, "PMA-1", 3),
          _lenh("FT-B-" + _hex(), "200.00", tt, "PMA-2", 4),
          _lenh("FT-C-" + _hex(), "300.00", tt, "PMA-3", 5)]
    kq = nap_anh_pm(conn, ds, spreadsheet_id=SID, actor="cron@fls",
                    source_id=nguon_pm, giay=3.2)

    assert kq["so_dong_doc"] == 3 and kq["so_dong_vao"] == 3
    assert kq["so_dong_bo_qua"] == 0
    # ⛔ RỖNG — ⛔ không một dòng nào vào bảng dòng của lằn sao kê
    assert conn.execute("SELECT count(*) FROM fls_chup_dong WHERE chup_id=%s",
                        (kq["chup_id"],)).fetchone()[0] == 0
    # ⭐ Mà `so_dong` vẫn ĐO được — qua `fls_run.chup_id`
    anh = ch.doc_chup(conn, kq["chup_id"])
    assert anh.lan == "PM" and anh.so_dong == 3
    assert anh.actor == "cron@fls" and anh.giay == 3.2
    assert anh.nguon[0].khai_version == PM_KHAI_VERSION
    # ⭐ Vết truy ⛔ không đứt
    assert conn.execute("SELECT chup_id FROM fls_run WHERE run_id=%s",
                        (kq["run_id"],)).fetchone()[0] == kq["chup_id"]


def test_anh_da_CHUP_ma_CHUA_NAP_thi_so_dong_la_0_chu_khong_bien_mat(conn,
                                                                     nguon_pm):
    """⭐ Cùng lý lẽ với `LEFT JOIN` của lằn sao kê: *"nguồn đọc ra 0 dòng phải
    HIỆN RA với `so_dong = 0`, ⛔ không biến mất"*."""
    anh = ch.ghi_chup_pm(conn, spreadsheet_id=SID, actor="dev",
                         source_id=nguon_pm, khai_version=PM_KHAI_VERSION)
    assert anh.lan == "PM" and anh.so_dong == 0
    assert len(anh.nguon) == 1


# ── ⓓ nạp LẠI cùng tệp ──────────────────────────────────────────────────
def test_nap_LAI_cung_tep__so_ma_moi_la_0_va_anh_CU_khong_doi_mot_o(conn,
                                                                    nguon_pm):
    """⭐⭐ Nạp lại cùng một tệp là **chuyện thường** *(nhịp mỗi giờ,
    `QĐ-ITL-114`)*, và nó **phải** cho `so_ma_moi = 0`.

    ⛔⛔ Nhưng nó ⛔ **không** cho *"0 dòng vào kho"*: mỗi ảnh là một `run_id`
      MỚI nằm **cạnh** ảnh cũ, ⛔ không đè lên *(`chen_dong_pm`, `INV-I08`)*.
      Hai con số ấy trả lời **hai câu khác nhau**, và gộp chúng lại sẽ làm một
      nhịp mỗi giờ trông như *"12 lần nạp mới mỗi ngày"*.
    """
    tt = "Q" + _hex(5)
    ds = [_lenh("FT-LAP-" + _hex(), "500.00", tt, "PMB-1")]
    k1 = nap_anh_pm(conn, ds, spreadsheet_id=SID, actor="cron",
                    source_id=nguon_pm)
    k2 = nap_anh_pm(conn, ds, spreadsheet_id=SID, actor="cron",
                    source_id=nguon_pm)

    assert k1["run_id"] != k2["run_id"] and k1["chup_id"] != k2["chup_id"]
    assert k2["anh_truoc"] == k1["run_id"]
    assert k2["so_ma_moi_so_voi_anh_truoc"] == 0
    # ⛔ Ảnh CŨ ⛔ không đổi một ô — chỉ-THÊM
    assert conn.execute("SELECT count(*) FROM fls_pm_line WHERE run_id=%s",
                        (k1["run_id"],)).fetchone()[0] == 1
    # ⭐ Và ảnh **hiệu lực** là ảnh MỚI
    assert anh_pm_hieu_luc(conn, chi_nap_that()) == k2["run_id"]


def test_ma_MOI_duoc_DEM__day_la_con_so_duy_nhat_noi_lan_nap_MANG_VE_GI(conn,
                                                                        nguon_pm):
    """⚠ Nếu con số này `0` **mãi mãi** thì lằn nạp đang ⛔ **không mang về gì**
    — và đó là thứ ⛔ không cổng nào thấy nếu ⛔ không ai đo."""
    tt = "R" + _hex(5)
    cu = _lenh("FT-CU-" + _hex(), "100.00", tt, "PMC-1")
    k1 = nap_anh_pm(conn, [cu], spreadsheet_id=SID, actor="cron",
                    source_id=nguon_pm)
    assert k1["so_ma_moi_so_voi_anh_truoc"] >= 1

    moi = _lenh("FT-MOI-" + _hex(), "200.00", tt, "PMC-2", 4)
    k2 = nap_anh_pm(conn, [cu, moi], spreadsheet_id=SID, actor="cron",
                    source_id=nguon_pm)
    assert k2["so_ma_moi_so_voi_anh_truoc"] == 1


# ── ⭐⭐⭐ CỔNG RA THẬT: có dịch được một dòng nào ⛔ không ───────────────
def test_lenh_chi_VUA_NAP_thanh_ung_vien_cho_dong_tien_CU(conn, nguon_pm):
    """⭐⭐⭐ **Đây là cổng ra thật của `A3`.**

    Một dòng tiền nạp **trước đó** *(một `run_id` khác hẳn)* phải thấy được
    lệnh chi **vừa nạp**. Trước `QĐ-ITL-119` bài này DO — và nó do theo hướng
    tệ nhất: `0` ứng viên, ⛔ không lỗi, chỉ là **⛔ không có gì xảy ra**.
    """
    tt = "S" + _hex(5)
    ref = "FT-NOI-" + _hex()
    r_so = "NAP-2000-01-01-SO" + _hex()
    conn.execute("INSERT INTO fls_run (run_id, contract_version,"
                 " canon_version, mapping_version)"
                 " VALUES (%s,'v1.0','v1.0','v1.0')", (r_so,))
    i = conn.execute(
        "INSERT INTO fls_itl (content_key, source_system, source_sheet,"
        " source_row, run_id, contract_version, canon_version, mapping_version,"
        " raw_frozen, canon, doc_no, curr, ps_co, work_status)"
        " VALUES (%s,'RAW','L1',7,%s,'v1.0','v1.0','v1.0',false,'{}'::jsonb,"
        " %s,%s,%s,'UNMAPPED') RETURNING itl_id",
        (uuid.uuid4().hex, r_so, ref, tt, D("900000.00"))).fetchone()[0]

    assert ung_vien_pm(conn, chi_nap_that(), i, n=20)["ung_vien"] == []

    nap_anh_pm(conn, [_lenh(ref, "900000.00", tt, "PMD-1")],
               spreadsheet_id=SID, actor="cron", source_id=nguon_pm)

    d = ung_vien_pm(conn, chi_nap_that(), i, n=20)
    assert [x["bac"] for x in d["ung_vien"]] == ["ma"], \
        "⛔ lệnh chi VỪA NẠP ⛔ không thành ứng viên ⇒ `A3` vô nghĩa"


# ── hợp đồng cột PM ─────────────────────────────────────────────────────
def test_doi_PM_COT_thi_PHAI_bump_PM_KHAI_VERSION():
    """⛔⛔ `fls_chup_nguon.khai_version` trả lời câu *"ảnh này đọc theo bố trí
    cột NÀO"*. Nếu `PM_COT` đổi mà con số ấy ⛔ không đổi thì **hai ảnh đọc
    theo hai bố trí khác nhau sẽ mang CÙNG một `khai_version`** — và câu trả
    lời ấy thành vô nghĩa, **im lặng**.

    ⭐ Nên cổng này ghim **nội dung** của hợp đồng cột, ⛔ không ghim con số:
      đổi `PM_COT` ⇒ ĐỎ ⇒ người sửa buộc phải bump.
    """
    import hashlib
    import json

    from fls.adapters.pm_join import PM_COT, PM_TIEU_DE_MONG_DOI

    bam = hashlib.sha256(json.dumps(
        {"cot": PM_COT, "tieu_de": {str(k): v
                                    for k, v in PM_TIEU_DE_MONG_DOI.items()}},
        sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:16]
    assert (PM_KHAI_VERSION, bam) == (2, "2feae46097be3816"), (
        "⛔ `PM_COT`/`PM_TIEU_DE_MONG_DOI` vừa ĐỔI ⇒ phải bump "
        "`PM_KHAI_VERSION` VÀ cập nhật dấu bằm ở đây. Dấu bằm mới: " + bam)
