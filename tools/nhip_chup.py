# -*- coding: utf-8 -*-
"""`A1`+`A2`+`A3` — MOT LUOT CUA NHIP: chup · nap lenh chi · don anh cu.

    python tools/nhip_chup.py                  # CHI DO — ⛔ khong ghi gi
    python tools/nhip_chup.py --that           # chay THAT tren kho THAT
    python tools/nhip_chup.py --that --kho-test

⛔⛔ **MOT LUOT, roi THOAT — ⛔ khong mot vong lap thuong tru.** Nhip do bo hen
gio cua he dieu hanh giu, ⛔ khong do mot tien trinh Python giu:

  ⓐ mot tien trinh thuong tru **chet cung may**, va no chet **im lang** — nhip
    dung, ⛔ khong ai biet, va con so *"anh moi gio"* trong bao cao van dung
    vi ⛔ khong ai dem lai;
  ⓑ mot luot roi thoat thi **moi lan chay la mot lan do duoc**: `can_chup` tra
    ve quyet dinh **kem LY DO**, va ly do ay vao dau ra ⇒ doc lai duoc.

★ Dang ky nhip *(viec cua NGUOI VAN HANH, ⛔ khong phai cua tep nay)*:

    schtasks /Create /TN "FLS nhip chup" /SC HOURLY /ST 08:00 ^
      /TR "C:\\Users\\0_Apero Project\\FLS\\.venv\\Scripts\\python.exe ^
           C:\\Users\\0_Apero Project\\FLS\\tools\\nhip_chup.py --that"

⛔ Tep nay **⛔ KHONG tu dang ky** bo hen gio: dat mot viec dinh ky vao may cua
  nguoi khac la mot hanh vi **ra ngoai**, va no phai la mot cu bam cua ho.

⚠ Bo hen gio **moi gio** cu bang no; `can_chup` la thu giu dung cua so
  `8h`–`19h` **gio Viet Nam** va chan cu ban thu hai trong cung mot gio. ⇒ Dat
  nhip mot gio mot lan la du, va dat 15 phut mot lan cung ⛔ khong sai — chi ton
  4 cu goi bo di.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import psycopg  # noqa: E402

from fls.db.kho import dsn_test, dsn_that  # noqa: E402
from fls.repo import chup as ch  # noqa: E402
from fls.repo.chay_nap import nap_anh_pm  # noqa: E402
from fls.repo.don_chup import don_anh_chup, do_don  # noqa: E402
from fls.repo.nhip_chup import (ACTOR_NHIP, ACTOR_TAY,  # noqa: E402
                                can_chup, gio_viet_nam)
from fls.oracle.nguon import BAN_SAO_RAW  # noqa: E402
from tools.do_bat_bien_ngam import BANK  # noqa: E402
from tools.do_hinh_dang import token  # noqa: E402
from tools.nap_sao_ke import (TRUONG_MAC_DINH, doc_vung_chuan,  # noqa: E402
                              khai_day_du, ten_sheet_r)
from tools.nap_that import doc_pm  # noqa: E402

# ⛔ `src_type = 'PM'` — nguon cua lan lenh chi. **MOT** dong, va tep nay
#   ⛔ khong tu tao no: mot nguon moi la mot dong danh muc, va no phai duoc
#   khai mot lan bang `--tao-nguon` de ⛔ khong sinh ra hai dong trung y nghia.
KHOA_NGUON_PM = "[Importrange]PM_Unpivot"


def _nguon_pm(conn, tao: bool) -> int | None:
    r = conn.execute("SELECT source_id FROM fls_source WHERE source_key = %s",
                     (KHOA_NGUON_PM,)).fetchone()
    if r:
        return int(r[0])
    if not tao:
        return None
    return int(conn.execute(
        "INSERT INTO fls_source (source_key, src_type)"
        " VALUES (%s, %s) RETURNING source_id",
        (KHOA_NGUON_PM, ch.LAN_PM_SRC)).fetchone()[0])


CAT_TEN_RONG = 10


def khai_rong(rong: list[str], cat: int = CAT_TEN_RONG) -> dict:
    """`nguon_ra_0_dong` — DEM **va** GOI TEN, kem phep cat duoc KHAI.

    ⛔⛔⛔ **Vi sao ham nay ton tai.** Bao cao nhip in `nguon_ra_0_dong: 14`
      suot tu 09/09, va **⛔ khong ai hanh dong duoc tren mot con so dem**:
      no noi *"co chuyen"* ma ⛔ khong noi *"di xem cai NAO"*. Toi da viet
      *"lan Bank chay duoc"* trong khi `4` sheet vua khai ra `0` dong — va
      con so `14` nam **ngay tren man hinh** luc toi viet cau ay.

    ⚠ Cat o `10`, va **noi ro con bao nhieu**: mot danh sach `64` ten se bi
      cuon qua, va luc ay no lai thanh mot con so dem. ⛔ Phep cat phai
      **khai ra** *(`con_nua`)* — mot danh sach bi cat trong im lang la cach
      bien `40` thanh `10` ma ⛔ khong gi bao.
    """
    return {"nguon_ra_0_dong": len(rong),
            "ten_nguon_ra_0_dong": rong[:cat],
            "con_nua": max(0, len(rong) - cat)}


def _chup_bank(conn, tok: str, that: bool, dsn: str,
               actor: str) -> dict:
    """Lan `Bank` — dung lai **dung** duong doc cua `tools/chup_sao_ke.py`.

    ⛔ `o_theo` khoa theo **TEN SHEET**, ⛔ khong theo `source_id` — nen phep
      doi ten→`source_id` phai di qua `khai` *(dung nhu `chup_sao_ke` lam)*.
      Doc `o_theo` nhu the no khoa theo `source_id` la mot loi **im lang**: no
      cho mot anh chup **rong** ma ⛔ khong bao gi.
    """
    t0 = time.time()
    ten_r = ten_sheet_r(BANK, tok)
    khai = khai_day_du(ten_r, dsn)
    o_theo, _ = doc_vung_chuan(BANK, tok, ten_r, TRUONG_MAC_DINH,
                               {t: b.cot for t, b in khai.items()})
    giay = round(time.time() - t0, 2)
    nguon = {khai[t].source_id: khai[t].version for t in ten_r}
    dong = [(khai[t].source_id, j, o)
            for t in ten_r for j, o in enumerate(o_theo[t])]
    rong = sorted(t for t in ten_r if not o_theo[t])
    ten_rong = khai_rong(rong)
    if not that:
        return {"lan": "Bank", "se_ghi": len(dong), "so_nguon": len(nguon),
                **ten_rong, "giay": giay}
    a = ch.ghi_chup(conn, spreadsheet_id=BANK, lan="Bank", actor=actor,
                    nguon=nguon, dong=dong, giay=giay)
    return {"lan": "Bank", "chup_id": a.chup_id, "so_dong": a.so_dong,
            "so_nguon": len(a.nguon), **ten_rong, "giay": giay}


def _chup_pm(conn, tok: str, that: bool, tao_nguon: bool,
             actor: str) -> dict:
    """Lan `PM` — moc `A3`. ⛔ Day la lan **⛔ CHUA TUNG** co nhip nao."""
    sid = _nguon_pm(conn, tao_nguon)
    if sid is None:
        return {"lan": "PM", "bo_qua": (
            f"⛔ ⛔ khong co nguon `{KHOA_NGUON_PM}` trong `fls_source`. "
            f"Chay mot lan voi `--tao-nguon` de khai no")}
    t0 = time.time()
    pm = doc_pm(tok)
    giay = round(time.time() - t0, 2)
    if not that:
        return {"lan": "PM", "se_ghi": len(pm), "giay": giay}
    # ⛔⛔ `BAN_SAO_RAW`, ⛔ KHONG `BANK`: `doc_pm` doc tab
    #    `[Importrange]PM_Unpivot` cua **ban sao RAW**, con `BANK` la mot
    #    workbook KHAC. Ghi nham `spreadsheet_id` la ghi mot dau xuat xu
    #    **tro sai tep** — va no ⛔ khong bao gio no, chi lam cau *"anh nay doc
    #    workbook nao"* tra loi sai mai mai.
    kq = nap_anh_pm(conn, pm, spreadsheet_id=BAN_SAO_RAW.spreadsheet_id,
                    actor=actor, source_id=sid, giay=giay)
    return dict(kq, lan="PM", giay=giay)


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--that", action="store_true", help="ghi vao kho")
    p.add_argument("--kho-test", action="store_true")
    p.add_argument("--tao-nguon", action="store_true",
                   help="khai nguon `PM` mot lan (⛔ chi lan dau)")
    # ⭐⭐⭐ Co nay la thu **phan biet mot luot TU CHAY voi mot luot GO TAY**,
    #    va no la dieu kien de cong `A1` co nghia — xem `fls/repo/nhip_chup.py`.
    #    ⛔ Bo hen gio PHAI duoc dang ky kem co nay.
    p.add_argument("--tu-bo-hen-gio", action="store_true",
                   help="⭐ chi BO HEN GIO dung co nay — mot luot go tay "
                        "⛔ KHONG duoc mang no (cong `A1` dem theo `actor`)")
    p.add_argument("--bo-qua-gio", action="store_true",
                   help="⛔ CHAY NGOAI GIO — chi de thu tay, ⛔ khong dat vao nhip")
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    dsn = dsn_test() if a.kho_test else dsn_that()
    # ⛔⛔⛔ **Co `--tu-bo-hen-gio` la mot LOI KHAI, va toi da tu di qua chinh
    #    cai lo nay** — luot thu tep boc `nhip_chup.cmd` mang co ay, nen no
    #    ghi `actor = nhip@fls` **du toi go tay**. ⇒ Them mot lop MAY kiem:
    #    mot luot chay co **man hinh dinh vao** thi ⛔ **KHONG** duoc mang co.
    #
    # ⚠ Va no ⛔ **khong kin**: `nhip_chup.cmd` chuyen dau ra vao tep log nen
    #   `isatty()` cung la `False` khi go tay tep boc. ⇒ Lop nay chan **luot
    #   go tay TRUC TIEP** *(cai de xay ra nhat)*, ⛔ khong chan het.
    #   Bang chung THAT rang bo hen gio da ban la ban ghi cua **chinh bo hen
    #   gio** (`schtasks /Query … /V` → *Last Run Time* + *Last Result*),
    #   ⛔ khong phai mot dong trong kho.
    if a.tu_bo_hen_gio and sys.stdout.isatty():
        raise SystemExit(
            "⛔ `--tu-bo-hen-gio` ⛔ KHONG duoc dung khi go tay: co man hinh "
            "dinh vao tien trinh nay.\n"
            "   Co ay danh RIENG cho bo hen gio, va cong `A1` dem theo "
            "`actor` ⇒ mang no vao mot luot go tay la **tu bam cho cong "
            "xanh**.\n"
            "   Muon thu tay thi bo co di — luot ay se ghi "
            f"`actor = {ACTOR_TAY}` va cong `A1` ⛔ khong dem no.")
    actor = ACTOR_NHIP if a.tu_bo_hen_gio else ACTOR_TAY

    ra: dict[str, object] = {"luc": gio_viet_nam().isoformat(),
                             "actor": actor,
                             "kho": "test" if a.kho_test else "that",
                             "that": a.that, "lan": []}
    loi: list[str] = []
    with psycopg.connect(dsn, autocommit=True) as conn:
        tok = None
        for lan in ("Bank", "PM"):
            co, ly_do = can_chup(conn, lan, None)
            if not co and not a.bo_qua_gio:
                ra["lan"].append({"lan": lan, "chup": False, "ly_do": ly_do})
                continue
            if tok is None:
                tok = token()
            # ⛔⛔ **MOI LAN CHAY DOC LAP** — mot lan hong ⛔ khong duoc keo ca
            #    nhip xuong. Cung luat voi man `F03`: *"hai cua goi DOC LAP:
            #    mot cua hong ⛔ khong duoc keo ca man xuong"*.
            #
            # ⭐ Va no ⛔ khong phai mot lo xa: luot chay kho dau tien (09/09)
            #   NO ngay o lan `Bank` vi sheet song co **2 sheet ACB moi**
            #   ⛔ chua ai khai (`R | 721916_ACB VND_Coretap` va
            #   `R | 723916_ACB USD_Coretap`). Neu hai lan dinh nhau thi mot
            #   sheet bank ⛔ chua khai se **chan ca lan PM** — dung cai moc
            #   `A3` duoc dat ra de mo, va nhip se DO **moi gio** cho den khi
            #   ai do khai xong hai sheet ay.
            #
            # ⛔ Va no van **DO TO**, ⛔ khong bo qua im lang: loi vao bao cao
            #   kem ten lenh phai chay. Bo qua im lang thi hai sheet ay
            #   ⛔ khong bao gio duoc khai.
            try:
                d = (_chup_bank(conn, tok, a.that, dsn, actor)
                     if lan == "Bank"
                     else _chup_pm(conn, tok, a.that, a.tao_nguon, actor))
                ra["lan"].append(dict(d, chup=True, ly_do=ly_do))
            except (Exception, SystemExit) as e:         # noqa: BLE001
                ra["lan"].append({
                    "lan": lan, "chup": False, "ly_do": ly_do,
                    "loi": f"{type(e).__name__}: {e}"})
                loi.append(lan)

        # ── `A2` — don. ⛔ Chay **sau** khi chup: mot anh vua chup xong la mot
        #    anh CON MOI, nen no ⛔ khong bi cu don nay cham toi.
        ra["don"] = (don_anh_chup(conn, actor=actor) if a.that
                     else do_don(conn))

    if a.json:
        print(json.dumps(ra, ensure_ascii=False, default=str, indent=1))
        return 0

    print("NHIP CHUP ·", ra["luc"], "· kho", ra["kho"],
          "·", "GHI THAT" if a.that else "⛔ CHI DO")
    for d in ra["lan"]:
        print(f"\n── lan {d['lan']}")
        print("  ", d["ly_do"])
        for k, v in sorted(d.items()):
            if k not in ("lan", "chup", "ly_do", "se_xoa"):
                print(f"     {k:28s} {v}")
    dn = ra["don"]
    print(f"\n── DON (giu {dn['giu_ngay']} ngay)")
    print(f"     giu vi DA NAP              {dn['giu_vi_da_nap']}")
    print(f"     giu vi CON MOI             {dn['giu_vi_con_moi']}")
    print(f"     {'da xoa' if a.that else 'SE xoa':26s} "
          f"{dn.get('so_da_xoa', dn['so_se_xoa'])}")
    if dn["se_xoa"]:
        print("     anh:", ", ".join(str(x["chup_id"])
                                     for x in dn["se_xoa"][:10]))
    if loi:
        # ⛔ Ma tra ve KHAC 0 ⇒ bo hen gio bao su co. Mot lan chay co lan HONG
        #   ⛔ khong duoc bao la thanh cong chi vi cac lan khac chay duoc.
        print()
        print(f"⛔ {len(loi)} lan HONG: {loi} — xem `loi` o tren")
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
