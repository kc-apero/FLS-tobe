# -*- coding: utf-8 -*-
"""`B0` — in MAU SO cua tac vu ① + doi chieu hai cau *"chua ghep"*.

    python tools/do_mau_so.py            # bang chu
    python tools/do_mau_so.py --json     # cho `kiem_so_song` doc

⛔⛔ **Cong cu nay ⛔ KHONG mang mot con so nao cua rieng no.** Moi phep dem o
day goi `fls.repo.do_mau_so` — cung ham ma cua ghep LO goi. Neu no tu dung mot
cau SQL rieng thi ta lai co **hai ban su that**, va lan nay la hai ban ve dung
cai tap ma mot cu bam se ghep.
"""
from __future__ import annotations

import json
import sys

sys.path.insert(0, ".")
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from fls.db.kho import dsn_that, noi_chi_doc                 # noqa: E402
from fls.repo.do_mau_so import LY_DO_KHONG_TU_CHUNG, do_mau_so   # noqa: E402
from fls.repo.doc_bao_cao import do_phu_hang_cho    # noqa: E402
from fls.repo.pham_vi import chi_nap_that                   # noqa: E402


def _vn(n) -> str:
    """So kieu tai lieu: dau cham ngan hang nghin.

    ⛔⛔ `int()` truoc khi dinh dang — ⛔ **khong** de nguyen `Decimal`. Tien
    trong kho la `numeric`, va `f"{Decimal('302262754.04'):,}"` cho
    `302,262,754.04` ⇒ sau khi doi dau phay thanh dau cham no thanh
    **`302.262.754.04`**, doc y het *"302 ty"* trong khi that la **302 trieu**.
    Da in ra dung nhu the mot lan hom 09/09 truoc khi sua.
    """
    return f"{int(n):,}".replace(",", ".")


def main() -> int:
    # ⛔ Ket noi CHI-DOC: phep do ⛔ khong duoc ghi mot o nao, va
    #    PostgreSQL tu cuong che dieu do (⛔ khong phai loi hua).
    with noi_chi_doc(dsn_that()) as c:
        d = do_mau_so(c, chi_nap_that())
        # ⛔ Goi HAM THAT — `do_phu_hang_cho` la chinh phep xep ma man `F01`
        #   dung, nen con so o day va con so tren man **⛔ khong the lech**.
        phu = do_phu_hang_cho(c, chi_nap_that(), 90)

    if "--json" in sys.argv:
        print(json.dumps(dict(d, viec_nguoi_xem=phu),
                         ensure_ascii=False, default=str))
        return 0

    print("PHAM VI:", d["pham_vi"], "· tong", _vn(d["tong_dong"]), "dong")
    print()
    print("== ⓐ MAU SO theo VE cua so ==")
    print("%-14s %8s %8s %9s %8s" % ("ve", "so dong", "da noi", "chua noi",
                                     "ty le"))
    for r in d["ve"]:
        print("%-14s %8s %8s %9s %8s" % (
            r["ve"], _vn(r["so_dong"]), _vn(r["da_noi"]), _vn(r["chua_noi"]),
            (r["ty_le_noi_pct"] or "khong do duoc") + "%"
            if r["ty_le_noi_pct"] else "⛔ khong do duoc"))
    print()
    print("== ⓑ BON O `work_status` x `co moi noi` — moi o mot TEN ==")
    for r in d["nhan"]:
        print("  %-28s %8s" % (r["ma"], _vn(r["so_dong"])))
        print("      %s" % r["ly_do"])
    L = d["lech"]
    print()
    print("== ⓒ Cau tra loi cho \"lech 353\" ==")
    print("  hieu hai phep dem      :", _vn(L["hieu_hai_phep_dem"]))
    print("  da noi ma nhan UNMAPPED:", _vn(L["da_noi__nhan_con_UNMAPPED"]))
    print("  du phan loai ma chua noi:", _vn(L["du_phan_loai__chua_noi"]))
    print("  ⇒ TONG dong bi che     :", _vn(L["tong_dong_bi_che"]))
    print("  ", L["ket_luan"])
    print()
    print("== ⓓ VI SAO chua noi duoc (bon nhom, PHU HET) ==")
    print("%-26s %9s %9s" % ("nhom", "ca so", "ve PS Co"))
    for r in d["vi_sao"]:
        print("%-26s %9s %9s" % (r["ma"], _vn(r["so_dong"]),
                                 _vn(r["so_dong_ps_co"])))
    print()
    print("== ⓔ TU CHUNG — cua ghep LO nhan duoc NGAY ==")
    print("  tu chung:", _vn(d["tu_chung"]), "dong")
    for k, n in sorted(d["khong_tu_chung"].items(), key=lambda x: -x[1]):
        print("  ⛔ %-26s %6s   %s" % (k, _vn(n), LY_DO_KHONG_TU_CHUNG[k]))

    # ══ ⭐⭐⭐ `B1` — TRAN CUNG + VIEC NGUOI XEM (them 09/09) ══
    #
    # ⛔⛔⛔ **Vi sao HAI muc nay o CUNG mot cong cu voi mau so.**
    # `31,1%` doc mot minh nghe nhu that bai, va nguoi doc se ket luan *"con
    # 69% viec"*. Hai con so chua no lai:
    #   ⓕ **tran** — `47,4%` la **gioi han vat lieu**, nen phan viec da lam
    #     that ra la `65,6%` cua nhung gi lam duoc;
    #   ⓖ **viec nguoi xem** — `799` dong phu **90% tien**, tuc viec that
    #     ⛔ khong phai `5.684` cu bam.
    # ⇒ Tach chung ra ba cong cu thi ⛔ khong ai doc ca ba, va con so bi doc
    #   mot minh la con so **noi sai**.
    t = d["tran"]
    print()
    print("== ⓕ TRAN CUNG — gioi han VAT LIEU, ⛔ khong phai muc tieu ==")
    print("  anh lenh chi hieu luc    :", t["anh_pm"])
    print("  dong lenh trong anh      :", _vn(t["dong_lenh_trong_anh"]))
    print("  trong do DA duoc dung    :", _vn(t["dong_lenh_da_dung"]))
    print("  con RANH                 :", _vn(t["dong_lenh_con_ranh"]))
    print("  ⇒ TOI DA noi duoc        :", _vn(t["toi_da_noi_duoc"]),
          f"= {t['tran_pct']}% ve `PS Co`")
    print("  ⭐ DO PHU TREN TRAN       :",
          (t["phu_tren_tran_pct"] + "%") if t["phu_tren_tran_pct"]
          else "⛔ khong do duoc")
    print("  ", t["ket_luan"])

    # ⛔ Cau hoi KHAC: hang cho tinh tren `work_status='UNMAPPED'` CA HAI VE,
    #   ⛔ khong chi `PS Co` ⇒ so dong o day **⛔ khong** bang `5.684`, va do
    #   la dung. In ca hai ma ⛔ khong noi ro thi nguoi doc se tru chung.
    print()
    print("== ⓖ VIEC NGUOI XEM — bao nhieu dong phu 90% TIEN, tung tien te ==")
    print("%-8s %10s %22s %13s %9s" % (
        "tien te", "dong cho", "tien cho", "phu 90%", "pct that"))
    tong_cho = tong_phu = 0
    for r in phu:
        tong_cho += r["so_dong_cho"]
        n = r["so_dong_phu"]
        tong_phu += n or 0
        print("%-8s %10s %22s %13s %9s" % (
            r["curr"] or "?", _vn(r["so_dong_cho"]), _vn(r["tien_cho"]),
            _vn(n) if n is not None else "⛔ khong do duoc",
            r["pct_that"] or "-"))
    if tong_cho:
        print("  ⇒ %s / %s dong hang cho = %.1f%% SO DONG, phu 90%% TIEN"
              " trong TUNG tien te"
              % (_vn(tong_phu), _vn(tong_cho), 100.0 * tong_phu / tong_cho))
        print("  ⚠ Hang cho dem CA HAI VE (`work_status='UNMAPPED'`), nen"
              " %s ⛔ KHONG bang so dong chua noi ve `PS Co`" % _vn(tong_cho))
    print("  ⛔ Phep xep nay ⛔ khong noi dong nao *khong can lenh chi* —"
          " `QĐ-ITL-56`: ⛔ khong co quy dinh nao. No chi noi XEM CAI NAY"
          " TRUOC")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
