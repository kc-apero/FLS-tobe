"""Sao luu so THAT + chung minh so **dung lai duoc tu nguon**.

    python tools/sao_luu_kho.py                    # chup so THAT ra tep
    python tools/sao_luu_kho.py --so-sanh <tep>    # so kho hien tai voi ban chup

⛔⛔ **Cong cu nay ⛔ KHONG xoa gi, ⛔ KHONG bo kho.** Do la co y.

`INV-I08`: `fls_itl` la **append-only** — ⛔ khong UPDATE khong DELETE. Nen don
1.204 dong dau test ⛔ khong duoc lam bang `DELETE FROM fls_itl WHERE run_id
LIKE 'T-%'`: cau do don duoc dung cho, nhung **de lai mot duong xoa so trong
ma nguon**, va lan sau khi can don thu khac thi duong do da co san. Duong dung
la **DDL** — bo ca kho roi dung lai rong + nap lai tu NGUON.

★ Phep do chi an toan vi so **dung lai duoc**: nguon that la Gsheet cua ke
toan, FLS la ha nguon. `--so-sanh` la buoc **chung minh** dieu do — checksum
NOI DUNG cua so dung lai phai trung ban chup. ⚠ Chua ai kiem tinh chat nay
bao gio, nen ⛔ dung coi no la dieu hien nhien.

⚠ Bo kho la viec **khong lui duoc** ⇒ lenh do ⛔ khong nam trong tep nay,
no duoc IN RA de nguoi quyet chay.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import sys
from datetime import datetime, timezone

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

import psycopg                                                    # noqa: E402

from fls.db.kho import TEN_THAT, dsn_that, ten_kho                # noqa: E402
from fls.repo.kho_sach import kiem, la_run_that                   # noqa: E402

THU_MUC = pathlib.Path(__file__).resolve().parent.parent / "sao_luu"

# ⛔⛔ Cot la DAU VET LUC NAP, ⛔ KHONG phai noi dung cua dong so. Phai loai khoi
# checksum, khong thi cong "so dung lai duoc" **khong bao gio co the xanh**:
#   `itl_id`     — SEQUENCE, cap lai moi lan nap
#   `created_at` — `now()`, doi 100% moi lan nap
# ★ Bat duoc 27/08 TRUOC khi bo kho: neu de `created_at` trong checksum thi lech
# se ra "9.973 dong doi" va toi da ket luan SAI rang so khong dung lai duoc.
COT_DAU_VET: frozenset[str] = frozenset({"itl_id", "created_at"})


def _cot(conn, bang: str) -> list[str]:
    return [r[0] for r in conn.execute(
        "select column_name from information_schema.columns "
        "where table_name=%s order by ordinal_position", (bang,))]


def checksum_noi_dung(cot: list[str], dong: list[tuple]) -> str:
    """Checksum theo NOI DUNG. ⛔ Bo `COT_DAU_VET` (`itl_id`, `created_at`).

    Doc lap thu tu doc: sap theo `content_key` truoc khi bam. Neu khong bo dau
    vet luc nap va khong sap, checksum se doi moi lan nap **du du lieu y nguyen**,
    va luc do no khong con do duoc gi — mot cong luon do la mot cong vo dung.
    """
    i_ck = cot.index("content_key")
    bo = {k for k, ten in enumerate(cot) if ten in COT_DAU_VET}
    h = hashlib.sha256()
    for r in sorted(dong, key=lambda x: str(x[i_ck])):
        h.update("|".join("" if v is None else str(v)
                          for k, v in enumerate(r) if k not in bo).encode())
    return h.hexdigest()[:16]


def _lay_dong_that(conn) -> tuple[list[str], list[tuple], int]:
    cot = _cot(conn, "fls_itl")
    tat_ca = conn.execute(f"select {','.join(cot)} from fls_itl").fetchall()
    i_run = cot.index("run_id")
    dong = [r for r in tat_ca if la_run_that(r[i_run])]
    return cot, dong, len(tat_ca) - len(dong)


def chup() -> int:
    dsn = dsn_that()
    ten = ten_kho(dsn)
    print(f"kho THAT: {ten!r}")
    if ten != TEN_THAT:
        print(f"⛔ PG_DSN tro vao {ten!r}, khong phai kho THAT {TEN_THAT!r}")
        return 1

    with psycopg.connect(dsn, autocommit=True) as c:
        px = kiem(c)
        cot, dong, bo = _lay_dong_that(c)

    if not dong:
        print("⛔ khong co dong nao cua lan nap THAT — ⛔ khong chup gi")
        return 1

    THU_MUC.mkdir(exist_ok=True)
    ck = checksum_noi_dung(cot, dong)
    i_run = cot.index("run_id")
    dau = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    p = THU_MUC / f"so_that_{dau}_{ck}.json"
    p.write_text(json.dumps({
        "luc": dau, "checksum": ck, "so_dong": len(dong), "cot": cot,
        "run": sorted({r[i_run] for r in dong}),
        "dong": [[None if v is None else str(v) for v in r] for r in dong],
    }, ensure_ascii=False), encoding="utf-8")

    print(f"  chup {len(dong)} dong THAT · BO QUA {bo} dong dau test")
    print(f"  -> sao_luu/{p.name}")
    print(f"  checksum NOI DUNG = {ck}")

    if px.dat:
        print("\n✅ kho da sach — ⛔ khong can dung lai.")
        return 0

    print("\n" + px.bao())
    print(f"""
⛔ CON {bo} DONG DAU TEST TRONG SO THAT. Don duoc, nhung buoc do
   **khong lui duoc** nen no ⛔ khong nam trong cong cu — CAN NGUOI QUYET.

   Ba lenh, theo dung thu tu:

     1) bo kho roi dung lai rong  (DDL — ⛔ KHONG mot cau DELETE nao len so)
        docker exec fls-pg-1 psql -U fls -d postgres -c \\
          'DROP DATABASE fls WITH (FORCE); CREATE DATABASE fls;'

     2) ap lai di tru + nap lai tu NGUON
        python -m fls.db.pg_migrate && python tools/nap_that.py --that

     3) CHUNG MINH so dung lai dung khong mat dong nao
        python tools/sao_luu_kho.py --so-sanh sao_luu/{p.name}
        python tools/kiem_kho.py

   ⚠ Buoc 3 la buoc dang gia nhat: no kiem mot tinh chat **chua ai kiem** —
   so nay co dung lai duoc tu nguon hay khong.""")
    return 1


def _diff_theo_cot(cot: list[str], cu: list[list], moi: list[tuple]
                   ) -> tuple[dict[str, int], int, int]:
    """So TUNG O theo khoa `content_key`. Tra (dem lech theo cot, chi-cu, chi-moi).

    ⛔ Bo `itl_id` — so ay cap lai moi lan nap nen no LUON khac, va mot cot luon
    khac se lam moi dong trong nhu da doi.
    """
    i_ck = cot.index("content_key")
    bo = {k for k, ten in enumerate(cot) if ten in COT_DAU_VET}

    d_cu = {r[i_ck]: r for r in cu}
    d_moi = {str(r[i_ck]): r for r in moi}
    dem: dict[str, int] = {}
    for ck, a in d_cu.items():
        b = d_moi.get(ck)
        if b is None:
            continue
        for k, ten in enumerate(cot):
            if k in bo:
                continue
            x = "" if a[k] is None else str(a[k])
            y = "" if b[k] is None else str(b[k])
            if x != y:
                dem[ten] = dem.get(ten, 0) + 1
    return dem, len(set(d_cu) - set(d_moi)), len(set(d_moi) - set(d_cu))


def so_sanh(duong: str) -> int:
    goc = json.loads(pathlib.Path(duong).read_text(encoding="utf-8"))
    with psycopg.connect(dsn_that(), autocommit=True) as c:
        cot, dong, bo = _lay_dong_that(c)
    ck = checksum_noi_dung(cot, dong)

    print(f"ban chup : {goc['so_dong']:6d} dong · checksum {goc['checksum']}")
    print(f"kho nay  : {len(dong):6d} dong · checksum {ck}"
          + (f" · con {bo} dong dau test" if bo else ""))

    if cot != goc["cot"]:
        them = set(cot) - set(goc["cot"])
        mat = set(goc["cot"]) - set(cot)
        print(f"⛔ CO CAU COT DA DOI (them={sorted(them)} mat={sorted(mat)}) "
              f"⇒ checksum ⛔ khong so sanh duoc truc tiep")
        return 1
    if ck == goc["checksum"]:
        print("✅ TRUNG KHIT — so **dung lai duoc tu nguon**, khong mat mot dong.")
        return 0

    print("⛔ LECH — nhung ⛔ dung dung lai o day. Lech O DAU moi la thong tin:")
    dem, chi_cu, chi_moi = _diff_theo_cot(cot, goc["dong"], dong)
    print(f"   dong chi co o BAN CHUP : {chi_cu}")
    print(f"   dong chi co o KHO NAY  : {chi_moi}")
    if dem:
        print("   o LECH theo tung cot (tren cac dong co mat o CA HAI ben):")
        for ten, n in sorted(dem.items(), key=lambda x: -x[1]):
            print(f"     {ten:22s} {n:6d} dong")
    else:
        print("   ⛔ 0 o lech tren cac dong trung khoa — vay lech nam o SO DONG")

    print("\n   Ba kha nang, ⛔ dung doan, phai phan biet duoc:")
    print("   ⓐ DUNG NHU DU DOAN  — lan nap moi lam duoc them viec (vd hinh `B`")
    print("      nay dau duoc nen `pm_hinh` doi NULL->'B'). Lech nay la TIEN BO.")
    print("   ⓑ NGUON da doi giua hai lan doc (ke toan them/sua dong)")
    print("   ⓒ LAN DOC thieu gia tri im lang (cong doc-du: mot lat HOP LE van")
    print("      tung thieu 257 gia tri ma 4 cong deu khong bao gi)")
    print("   ⇒ Neu lech chi nam o dung nhung cot va dung so dong DA DU DOAN")
    print("     TRUOC khi chay, thi la (ⓐ). Ngoai ra thi phai truy.")
    return 1


def main() -> int:
    if "--so-sanh" in sys.argv:
        i = sys.argv.index("--so-sanh")
        if i + 1 >= len(sys.argv):
            print("⛔ thieu duong dan tep ban chup")
            return 1
        return so_sanh(sys.argv[i + 1])
    return chup()


if __name__ == "__main__":
    sys.exit(main())
