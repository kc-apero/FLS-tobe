"""Nạp config `IX.*` ĐÃ KÝ vào kho config chỉ-thêm — trình ĐIỀU PHỐI mỏng cho `04_nap_du_lieu.sh` · `WO-325` AC-3.

    PG_DSN=… PGPASSWORD=… FLS_CHO_GHI_THAT=1 python tools/staging/nap_cau_hinh_ix.py --nguoi-nap <tên.người>
    PG_DSN=… python tools/staging/nap_cau_hinh_ix.py --kiem            # CHỈ ĐỌC: bảng nào đã có phiên bản nào

⭐ **Vì sao có tệp này** *(Đ1 — đo cả hai nơi 23/11: `grep -rn "nap_ix_" tools/ docs/ fls/`)*: hàm nạp từng bảng đã CÓ ở
   `fls/repo/cau_hinh_repo.py` *(C5…C12)*, nhưng ⛔ không công cụ dòng lệnh nào gọi chúng — các bài thử `tests/oracle/`
   tự ghép chuỗi nạp. Kho staging rỗng ⇒ mọi gói HD2 *(`tools/do_hd2.py --goi …`)* dừng `ChuaKhai: ⛔ bang='IX.…' ⛔ CHƯA có
   phiên bản nào trong kho config` *(đo 23/11: 7/7 gói cần kho)*. ⇒ cần MỘT chỗ gọi đúng chuỗi, ⛔ viết lại công cụ nạp:
   tệp này CHỈ gọi `cau_hinh_repo.nap_*` / `ky_bat_ix_alr`, với ĐÚNG ảnh đã commit và đúng tham số mà `tests/oracle/` +
   `tools/do_hd2_c5a.py` đang dùng.

⛔ Luật:
  · GHI đòi `FLS_CHO_GHI_THAT=1` *(cùng cổng `tools/dung_lai_so.py`)*; không có ⇒ từ chối, exit 2.
  · ⛔ nạp chồng: bảng ĐÃ có phiên bản ⇒ BỎ QUA (kho chỉ-thêm; nạp lại cùng nội dung vẫn đẻ một `phien_ban` mới). Muốn đổi
    config = việc của người ký, ⛔ của bước dựng này.
  · `actor` = `--nguoi-nap` *(ghi vào cột `actor` — hành vi của NGƯỜI)*; ⛔ email; riêng bản KÝ bật cờ `IX.ALR` actor = người
    ký trong chính tệp ký *(`ix_alr_2025_bat.json` · `KhanhCQ`)*.
  · ⛔ ảnh nào ngoài `tests/fixture/cau_hinh/` ; ⛔ `Email Address` / `sao_luu/` / `hien_vat/` (không đường nào tới đó).
  · KHÔNG ghi `fls_itl` — chỉ `fls_cau_hinh_ban` / `fls_cau_hinh_dong` (⇒ `fls_ghi` ghi được, ⛔ cần quyền sổ).

BÁO CÁO: số dòng THẬT trong kho từng bảng, có `mong` *(Đ5 — hai chiều)* và MẪU SỐ ≠ 0 *(Đ3)*; `KẾT: ĐẠT/ĐỎ`, exit 1 khi ĐỎ.
`mong` đo 23/11 bằng chính chuỗi nạp này trên kho trắng, rồi đối chiếu với tài liệu *(IX.HD 74 nút · Mapping Master 73 mã ·
IX.FX 37 dòng · IX.DRV 21 + 146 + 304 dòng · IX.PL 7 dòng PL2…PL8)*; bài `tests/staging/test_04_nap_du_lieu.py` ghim chúng.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC))

ANH = GOC / "tests" / "fixture" / "cau_hinh"
NGUON = "staging-04 · ảnh đã ký (tests/fixture/cau_hinh)"
BIEN_CHO_GHI = "FLS_CHO_GHI_THAT"

# Thứ tự = thứ tự phụ thuộc: IX.ALR cần Mapping Master; bản KÝ bật cờ cần IX.ALR; IX.ORG cần cdt_correct + MM.
BANG_THU_TU = ("IX.FX", "IX.HD", "IX.PL", "IX.HD · IX.ORG", "IX.PER", "IX.VEN", "IX.ORG", "IX.ALR", "IX.DRV")

# `mong` số dòng `fls_cau_hinh_dong` của bản MỚI NHẤT mỗi bảng sau khi nạp — ĐO 23/11 trên kho trắng, rồi đối chiếu:
#   IX.FX 38 = 37 tháng (ảnh `ix_fx.json` · `so_dong` 37) + 1 dòng `@thang_dau` · IX.VEN 360 = 359 + 1 dòng `@cdt1` ·
#   IX.HD 74 nút (tài liệu) · Mapping Master 73 mã (tài liệu) · IX.DRV 471 = 21 + 146 + 304 (docstring `nap_ix_drv`) ·
#   IX.PL 7 = PL2…PL8 · IX.PER 2 (ngày đầu + luật) · IX.ORG 72 (TK pháp nhân, ⛔ TK cá nhân) ·
#   IX.ALR 38 = bản KÝ bật cờ (bản nền 17 luật `@202501` + dòng đã ký đè — bản nền v1 vẫn NGUYÊN: 17 dòng).
MONG_DONG = {"IX.FX": 38, "IX.HD": 74, "IX.PL": 7, "IX.HD · IX.ORG": 73, "IX.PER": 2, "IX.VEN": 360,
             "IX.ORG": 72, "IX.ALR": 38, "IX.DRV": 471}
# `mong` số PHIÊN BẢN: 1 mỗi bảng, riêng IX.ALR 2 (bản nền cờ TẮT + bản KÝ bật cờ).
MONG_PHIEN_BAN = {b: 1 for b in BANG_THU_TU} | {"IX.ALR": 2}


def _nap_het(conn, actor: str) -> dict[str, str]:
    """Gọi đúng các hàm nạp sẵn có. Trả `{bảng: 'nạp'|'có rồi vN'}`."""
    from fls.repo import cau_hinh_repo as chc

    def co_san(bang: str) -> int:
        with conn.cursor() as cur:
            cur.execute("SELECT coalesce(max(phien_ban),0) FROM fls_cau_hinh_ban WHERE bang = %s", (bang,))
            return int(cur.fetchone()[0])

    kq: dict[str, str] = {}
    buoc = {
        "IX.FX": lambda: chc.nap_ix_fx(conn, str(ANH / "ix_fx.json"), actor=actor, thang_dau=202401, nguon=NGUON),
        "IX.HD": lambda: chc.nap_ix_hd(conn, str(ANH / "atl_cay.json"), actor=actor, nguon=NGUON),
        "IX.PL": lambda: chc.nap_ix_pl(conn, actor=actor),
        "IX.HD · IX.ORG": lambda: chc.nap_mapping_master(conn, str(ANH / "mapping_master_cfg.json"), actor=actor, nguon=NGUON),
        "IX.PER": lambda: chc.nap_ix_per(conn, actor=actor, ngay_dau="2024-10-21", luat="A",
                                         nguon="staging-04 · IX.PER kho = 21/10/2024 (C6, quyết chủ)"),
        "IX.VEN": lambda: chc.nap_ix_ven(conn, str(ANH / "ix_ven.json"), duong_cdt1=str(ANH / "cdt_correct.json"),
                                         actor=actor, nguon=NGUON),
        "IX.ORG": lambda: chc.nap_ix_org(conn, str(ANH / "cdt_correct.json"), str(ANH / "mapping_master_cfg.json"),
                                         actor=actor, nguon=NGUON),
        "IX.ALR": lambda: _nap_alr(chc, conn, actor),
        "IX.DRV": lambda: chc.nap_ix_drv(conn, str(ANH / "ix_drv.json"), actor=actor, nguon=NGUON),
    }
    for bang in BANG_THU_TU:
        v = co_san(bang)
        # ⭐ `STG-R1-07`: IX.ALR là HAI việc liền (bản nền v1 → bản KÝ v2). Chết GIỮA hai việc ⇒ kho chỉ-THÊM giữ v1 mà
        #   "có rồi ⇒ bỏ qua" khoá luôn bước KÝ ⇒ chạy lại ⛔ tự lành. Tự lành THEO TỪNG BƯỚC: v == 0 ⇒ nền + KÝ · 0 < v < mong ⇒ chỉ KÝ ·
        #   v ≥ mong ⇒ bỏ qua. Các bảng khác 1 việc ⇒ giữ nguyên "có rồi ⇒ bỏ qua".
        if bang == "IX.ALR" and 0 < v < MONG_PHIEN_BAN[bang]:
            _ky_alr(chc, conn)
            kq[bang] = f"có rồi v{v} · KÝ nốt"
            continue
        if v:
            kq[bang] = f"có rồi v{v}"
            continue
        buoc[bang]()
        kq[bang] = "nạp"
    return kq


def _nap_alr(chc, conn, actor: str) -> None:
    """Bản nền (17 luật từ kỳ 202501, cờ TẮT — D2) rồi bản KÝ bật cờ 2025 (quyết chủ 22/11; người ký ghi trong tệp)."""
    chc.nap_ix_alr(conn, str(ANH / "mapping_master_cfg.json"), tu_ky=202501, actor=actor, nguon=NGUON)
    _ky_alr(chc, conn)


def _ky_alr(chc, conn) -> None:
    """Bước KÝ riêng (tách ra để chạy lại sau khi chết giữa hai việc — `STG-R1-07`)."""
    tep = ANH / "ix_alr_2025_bat.json"
    nguoi_ky = json.loads(tep.read_text(encoding="utf-8"))["ky"]["nguoi_ky"]
    chc.ky_bat_ix_alr(conn, str(tep), actor=nguoi_ky)


def do_kho(conn) -> dict[str, tuple[int, int, int]]:
    """`{bảng: (số phiên bản, số dòng của bản mới nhất, mẫu số = số bản của bảng)}`."""
    ra: dict[str, tuple[int, int, int]] = {}
    with conn.cursor() as cur:
        for bang in BANG_THU_TU:
            cur.execute("SELECT count(*), coalesce(max(phien_ban),0) FROM fls_cau_hinh_ban WHERE bang = %s", (bang,))
            n, vmax = cur.fetchone()
            dong = 0
            if n:
                cur.execute("SELECT count(*) FROM fls_cau_hinh_dong d JOIN fls_cau_hinh_ban b USING (ban_id) "
                            "WHERE b.bang = %s AND b.phien_ban = %s", (bang, vmax))
                dong = cur.fetchone()[0]
            ra[bang] = (int(n), int(dong), int(n))
    return ra


def bao_cao(do: dict, kq: dict[str, str], che_do: str) -> int:
    print(f"\nBÁO CÁO nạp config IX.* (⛔ chứa mật khẩu/khoá) — chế độ: {che_do}")
    tong_ban = sum(v[0] for v in do.values())
    sai = 0
    for bang in BANG_THU_TU:
        n, dong, _ = do[bang]
        mong_n, mong_d = MONG_PHIEN_BAN[bang], MONG_DONG[bang]
        ok_n = n == mong_n
        ok_d = dong == mong_d
        sai += (not ok_n) + (not ok_d)
        gt_mong = str(mong_d)
        print(f"   [{'ĐẠT' if ok_n else 'ĐỎ'}] {bang:16} phiên bản = {n!r:4} (mong {mong_n!r})   "
              f"[{'ĐẠT' if ok_d else 'ĐỎ'}] dòng bản mới nhất = {dong!r:5} (mong {gt_mong})   {kq.get(bang, '')}")
    ok_mau = tong_ban >= len(BANG_THU_TU)
    sai += not ok_mau
    print(f"   [{'ĐẠT' if ok_mau else 'ĐỎ'}] MẪU SỐ — tổng phiên bản config trong kho = {tong_ban} (mong ≥ {len(BANG_THU_TU)}; "
          f"0 ⇒ kho trắng, ⛔ xanh trên tập rỗng)")
    print(f"\n══ KẾT: {'ĐẠT' if sai == 0 else f'ĐỎ — {sai} mục khác mong'}")
    return 1 if sai else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--kiem", action="store_true", help="CHỈ ĐỌC: đo kho, ⛔ nạp")
    ap.add_argument("--nguoi-nap", help="tên người nạp (cột `actor`); ⛔ email")
    a = ap.parse_args()
    dsn = os.environ.get("PG_DSN")
    if not dsn:
        print("⛔ thiếu PG_DSN", file=sys.stderr)
        return 2
    if not a.kiem:
        if os.environ.get(BIEN_CHO_GHI) != "1":
            print(f"⛔ nạp config là GHI vào kho — đòi {BIEN_CHO_GHI}=1", file=sys.stderr)
            return 2
        if not a.nguoi_nap or "@" in a.nguoi_nap or not a.nguoi_nap.strip():
            print("⛔ cần --nguoi-nap <tên.người> (⛔ rỗng, ⛔ email)", file=sys.stderr)
            return 2
    import psycopg

    with psycopg.connect(dsn, autocommit=True) as conn:
        kq = {} if a.kiem else _nap_het(conn, a.nguoi_nap.strip())
        return bao_cao(do_kho(conn), kq, "--kiem (chỉ đọc)" if a.kiem else "nạp")


if __name__ == "__main__":
    raise SystemExit(main())
