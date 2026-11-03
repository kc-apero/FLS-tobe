# -*- coding: utf-8 -*-
"""`A1` — SOI BO HEN GIO. Doc ban ghi cua **chinh no**, ⛔ khong cua kho.

    python tools/soi_nhip.py
    python tools/soi_nhip.py --json

⛔⛔⛔ **Vi sao cong cu nay ton tai, va vi sao no ⛔ KHONG the la mot cau SQL.**

Cong `A1` hoi: *"he TU CHAY chua"*. Phep do trong `kiem_so_song` dem
`fls_chup` co bao nhieu anh mang `actor = 'nhip@fls'` — va **do la mot phep do
CO THE TU BAM DUOC**: `tools/nhip_chup.py --that --tu-bo-hen-gio` ghi dung
`actor` ay **du ai goi no**. Toi da tu di qua chinh cai lo ay ngay 09/09 khi
thu tep boc `nhip_chup.cmd`: hai anh vao kho mang `nhip@fls`, va chung la
**hai luot GO TAY**.

⇒ Bang chung THAT rang bo hen gio dang song ⛔ khong nam trong kho — no nam
  trong **ban ghi cua bo hen gio**: viec co ton tai ⛔ khong · dang bat ⛔ khong ·
  **chay lan cuoi luc nao** · **ma tra ve la gi** · lan ke tiep khi nao.

★ Nen cong cu nay doc `Get-ScheduledTaskInfo`, roi **doi chieu** voi kho:

    · bo hen gio noi *"chay luc T, ma 0"*
    · kho noi *"anh gan nhat luc T'"*

  Neu bo hen gio chay ma kho ⛔ khong co anh moi thi **⛔ khong phai loi** —
  `can_chup` bo luot khi gio ay da co anh. Nhung neu bo hen gio ⛔ **chua bao
  gio chay** ma kho **co** anh `nhip@fls` thi day la mot **anh go tay dang
  doi lot anh cua nhip**, va cong cu nay noi thang ra dieu do.

⛔ Windows-only, va do la ly do no ⛔ **khong** nam trong `kiem_so_song`: mot
  cong chay tren may khac se **do vi thieu `schtasks`** thay vi vi mot con so
  lech — mot cai cong do vi ly do khac se bi tat.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

TEN_VIEC = "FLS nhip chup"

# ⭐ `267011` = *"task ⛔ chua bao gio chay"*. ⛔ Khai ten cho no: mot ma so tran
#   trong bao cao se duoc doc thanh **mot loi**, trong khi no la trang thai
#   binh thuong cua mot viec vua duoc dang ky.
MA_CHUA_CHAY = 267011
MOC_CHUA_CHAY = "1999-11-30"

_PS = (
    "$ErrorActionPreference='Stop';"
    "$t = Get-ScheduledTask -TaskName '{ten}';"
    "$i = Get-ScheduledTaskInfo -TaskName '{ten}';"
    "$o = [ordered]@{{"
    " ten = $t.TaskName; trang_thai = [string]$t.State;"
    " chay_lenh = $t.Actions[0].Execute;"
    " thu_muc = $t.Actions[0].WorkingDirectory;"
    " bat_dau = [string]$t.Triggers[0].StartBoundary;"
    " lap_moi = [string]$t.Triggers[0].Repetition.Interval;"
    " lap_trong = [string]$t.Triggers[0].Repetition.Duration;"
    " chay_lan_cuoi = [string]$i.LastRunTime;"
    " ma_lan_cuoi = $i.LastTaskResult;"
    " lan_ke_tiep = [string]$i.NextRunTime;"
    " so_luot_hut = $i.NumberOfMissedRuns;"
    # ⛔⛔⛔ BA CAI DAT QUYET DINH *"he co TU CHAY khong"*, va toi ⛔ KHONG he
    #   khai chung khi dang ky viec — chung dang o MAC DINH cua PowerShell:
    #     · `WakeToRun=False`         ⇒ may ngu thi nhip ⛔ KHONG chay
    #     · `DisallowStartIfOnBatteries=True` ⇒ rut dien thi ⛔ KHONG chay
    #     · `StopIfGoingOnBatteries=True`     ⇒ dang chay ma rut dien thi BI GIET
    #   ⇒ Mot cai *"nhip moi gio"* thuc chat la *"moi gio, NEU may thuc VA
    #     dang cam dien"*. Do la mot cau KHAC, va no phai doc ra duoc.
    " danh_thuc_may = $t.Settings.WakeToRun;"
    " chay_khi_pin = -not $t.Settings.DisallowStartIfOnBatteries;"
    " giet_khi_rut_dien = $t.Settings.StopIfGoingOnBatteries;"
    " chay_bu_khi_hut = $t.Settings.StartWhenAvailable }};"
    "$o | ConvertTo-Json -Compress"
)


def doc_bo_hen_gio(ten: str = TEN_VIEC) -> dict | None:
    """Ban ghi cua bo hen gio. `None` = **viec ⛔ khong ton tai**.

    ⛔ `None` va *"co viec nhung chua chay"* la **hai cau tra loi khac nhau**,
      va gop chung lai la de nguoi doc tuong nhip da duoc dang ky.
    """
    r = subprocess.run(
        ["powershell", "-NoProfile", "-NonInteractive", "-Command",
         _PS.format(ten=ten)],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    tho = (r.stdout or "").strip()
    if r.returncode != 0 or not tho:
        return None
    try:
        return json.loads(tho)
    except json.JSONDecodeError:
        return None


def doc_kho() -> dict:
    """Anh trong kho: tong · do NHIP · do GO TAY · gio dong ho khac nhau."""
    import psycopg                                          # noqa: PLC0415

    from fls.db.kho import dsn_that                          # noqa: PLC0415
    from fls.repo.nhip_chup import (ACTOR_NHIP, ACTOR_TAY,  # noqa: PLC0415
                                    do_gio_trong)

    with psycopg.connect(dsn_that(), connect_timeout=5) as c:
        def q(sql, *ts):
            return c.execute(sql, ts).fetchone()

        tong, = q("select count(*) from fls_chup")
        nhip, gio, muon = q(
            "select count(*), count(distinct date_trunc('hour', doc_luc)),"
            " max(doc_luc) from fls_chup where actor = %s", ACTOR_NHIP)
        tay, = q("select count(*) from fls_chup where actor = %s", ACTOR_TAY)
        # ⭐⭐⭐ `A1` ve THAT — do tu KHO, ⛔ khong tu API cua he dieu hanh.
        #   `so_luot_hut` cua bo hen gio noi *"toi ⛔ khong chay"*; con so
        #   nay noi *"kho ⛔ KHONG CO ANH"* — va do moi la thu `A1` hoi.
        #   ⚠ Hai ve nay CO THE lech: bo hen gio chay ma `can_chup` bo luot
        #     thi `so_luot_hut = 0` va `gio_trong = 0`; con may ngu thi CA
        #     HAI keu. Giu ca hai vi chung do HAI thu khac nhau.
        trong = {l: do_gio_trong(c, l) for l in ("Bank", "PM")}
    return {"anh_tong": tong, "anh_nhip": nhip, "anh_nhip_gio": gio,
            "anh_go_tay": tay, "anh_nhip_muon_nhat": muon,
            "gio_trong": {l: d["gio_trong"] for l, d in trong.items()},
            "gio_trong_chi_tiet": trong}


def _chua_chay(bhg: dict) -> bool:
    return (int(bhg.get("ma_lan_cuoi") or 0) == MA_CHUA_CHAY
            or MOC_CHUA_CHAY in str(bhg.get("chay_lan_cuoi") or ""))


def do_khong_chac(bhg: dict, kho: dict | None = None) -> list[str]:
    """Nhung ly do khien *"moi gio"* ⛔ KHONG con dung. Rong = chac chan.

    ⛔⛔⛔ **Vi sao ham nay phai ton tai.** Ban dau cong cu nay **IN** con so
      `so_luot_hut` roi in ngay ben duoi mot dong `✅ Bo hen gio CO CHAY` —
      tuc no **da co** con so noi *"nhip bo 3 luot"* va van tra ma `0`. Do la
      dung mot con so nam canh mot ket luan ⛔ khong doc no: cai lop loi ca du
      an nay dung ra de chan, va toi de no ngay trong cong cu **soi cong**.

    ⚠ Ba cai dat duoi day toi ⛔ **khong he khai** khi dang ky viec — chung o
      **mac dinh cua PowerShell**. Nen *"nhip moi gio"* thuc chat la *"moi
      gio, NEU may thuc VA dang cam dien"*. ⛔ Doi chung la doi cach may cua
      chu may xu su ⇒ ⛔ **khong tu quyet** (`R-A4`), chi **doc ra**.
    """
    ly: list[str] = []
    # ⭐⭐⭐ Ve do TU KHO, dat TRUOC ba cai dat: no la **HAU QUA**, con ba cai
    #   dat kia la **NGUYEN NHAN**. Nguoi doc can thay hau qua truoc — *"kho
    #   thieu N gio anh"* la cau ma owner quan tam, ⛔ khong phai ten mot co
    #   trong PowerShell.
    for lan, n in sorted((kho or {}).get("gio_trong", {}).items()):
        if n:
            ly.append(f"lan `{lan}`: **{n}** GIO TRONG trong khung chup — "
                      f"kho ⛔ KHONG CO ANH cho nhung gio ay")
    hut = int(bhg.get("so_luot_hut") or 0)
    if hut:
        ly.append(f"**{hut}** luot HUT — bo hen gio ⛔ khong he chay nhung "
                  f"luot ay, nen ⛔ khong co ai bo luot va cung ⛔ khong co "
                  f"anh nao")
    if bhg.get("danh_thuc_may") is False:
        ly.append("`WakeToRun=False` ⇒ may NGU thi nhip ⛔ KHONG chay")
    if bhg.get("chay_khi_pin") is False:
        ly.append("`DisallowStartIfOnBatteries=True` ⇒ RUT DIEN thi nhip ⛔ "
                  "KHONG chay")
    if bhg.get("giet_khi_rut_dien") is True:
        ly.append("`StopIfGoingOnBatteries=True` ⇒ dang chup ma rut dien thi "
                  "luot ay BI GIET giua duong")
    return ly


def main() -> int:
    bhg = doc_bo_hen_gio()
    kho = doc_kho()
    ra = {"bo_hen_gio": bhg, "kho": kho}

    if "--json" in sys.argv:
        print(json.dumps(ra, ensure_ascii=False, default=str, indent=1))
        return 0 if bhg else 3

    print("=" * 72)
    print("SOI NHIP CHUP — ban ghi cua BO HEN GIO, doi chieu voi kho")
    print("=" * 72)
    if bhg is None:
        print(f"  ⛔⛔ BO HEN GIO: ⛔ KHONG CO viec ten `{TEN_VIEC}`.")
        print("     ⇒ Cong `A1` ⛔ KHONG DAT, du kho co bao nhieu anh")
        print("       mang `actor` cua nhip — chung la anh GO TAY.")
    else:
        for k, v in bhg.items():
            print(f"  {k:16s} {v}")
        if _chua_chay(bhg):
            print("  ⇒ ⚠ Viec DA DUOC DANG KY nhung ⛔ CHUA BAO GIO CHAY")
        elif int(bhg["ma_lan_cuoi"]) != 0:
            print(f"  ⇒ ⛔ Lan chay cuoi tra ma **{bhg['ma_lan_cuoi']}** "
                  f"(⛔ khong phai 0) — xem `.nhip/nhip_chup.log`")
        else:
            print("  ⇒ ✅ Bo hen gio CO CHAY, va lan cuoi tra ma **0**")

    print()
    print("  -- kho --")
    for k, v in kho.items():
        if k == "gio_trong_chi_tiet":
            continue
        print(f"  {k:20s} {v}")

    # ⭐⭐⭐ `A1` ve THAT: gio TRONG trong khung chup. ⛔ Mot con so dem noi
    #   *"co chuyen"*; mot DANH SACH noi *"di xem cai nay"*.
    print()
    print("  -- GIO TRONG trong khung chup (`A1` ve THAT) --")
    for l, d in kho["gio_trong_chi_tiet"].items():
        print(f"  {l:5s} tu {d['anh_dau_tien']}  ·  phai co "
              f"{d['gio_phai_co']:>3} · co {d['gio_co_anh']:>3} · "
              f"⛔ TRONG {d['gio_trong']:>3}")
        if d["trong_gan_nhat"]:
            print(f"        {', '.join(d['trong_gan_nhat'][:6])}")

    print()
    if bhg is None or _chua_chay(bhg):
        if kho["anh_nhip"]:
            print(f"⛔⛔ **{kho['anh_nhip']} anh trong kho mang `actor` cua "
                  f"NHIP, ma bo hen gio ⛔ CHUA BAO GIO CHAY.**")
            print("   ⇒ Chung la anh **GO TAY dang doi lot anh cua nhip**. "
                  "Cong `A1`")
            print("     doc tu kho se XANH SAI. Day la ly do cong cu nay "
                  "ton tai.")
        return 3
    print("⭐ Doc hai ve canh nhau:")
    print(f"   bo hen gio chay lan cuoi : {bhg['chay_lan_cuoi']} "
          f"(ma {bhg['ma_lan_cuoi']})")
    print(f"   anh `nhip@fls` moi nhat  : {kho['anh_nhip_muon_nhat']}")
    print("   ⚠ Bo hen gio chay ma kho ⛔ khong co anh moi la **⛔ khong "
          "phai loi**:")
    print("     `can_chup` bo luot khi gio dong ho ay da co anh.")

    # ⭐ MA 4, ⛔ khong phai 3 — hai cau tra loi KHAC NHAU:
    #     `3` = *"nhip ⛔ CHUA BAO GIO chay"* / ⛔ khong co viec
    #     `4` = *"nhip CO chay, nhung *moi gio* ⛔ khong dung"*
    #   Gop chung vao mot ma la de nguoi doc tuong hai tinh huong ay giong
    #   nhau, va chung ⛔ khong giong nhau chut nao.
    ly = do_khong_chac(bhg, kho)
    if ly:
        print()
        print("⛔⛔ **`moi gio` ⛔ KHONG dung — day la vi sao:**")
        for x in ly:
            print(f"   · {x}")
        print("   ⇒ Cong `A1` xanh tren KHO *(co ≥2 anh, ≥2 gio, actor dung)*")
        print("     nhung cau HOI cua `A1` la *\"ke toan ⛔ khong can Dev\"* —")
        print("     va cau tra loi hom nay la **CAN**. ⛔ Toi ⛔ khong tu doi")
        print("     ba cai dat kia: do la cach MAY CUA CHU MAY xu su (`R-A4`).")
        return 4
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
