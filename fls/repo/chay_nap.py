"""Chay nap THAT: nguon -> canon -> lop so -> `fls_itl`. Va cong ba duong.

Day la lan dau kho co du lieu that thay vi vai tram dong test. Nen module nay
mang mot yeu cau khac cac module truoc: **khong dong nao duoc roi im lang**
(cong chung #3). Ba duong PHAI can:

    dong vao = vao so + vao fls_reject + dong trong cua sheet + bo qua vi trung khoa

⛔ Neu khong can thi ham NO, va ⛔ khong ghi mot dong nao — mot lan nap lech ma
van commit thi tu day tro di khong ai biet so thieu bao nhieu.

★ `seq_trung` phai do NGUOI GOI tinh, khong de DB tu xu. `content_key` la
hash(nguon, sheet, ngay, PS No, PS Co, so chung tu, seq_trung) va so that co
**281 dong trung noi dung** + **103 dong khong co so chung tu**. Neu khong danh
seq thi 281 dong do dung mot khoa ⇒ `ON CONFLICT DO NOTHING` bo im lang gan het,
va con so "bo qua" se bi doc thanh "nap lai lan hai" thay vi "MAT DU LIEU".

⛔ Module nay KHONG ghi mot o nao ve file ke toan (`QD-ITL-34`) va KHONG cham
`fps_*`/P100 (`QD-ITL-45`). No chi doc lat tho da duoc doc san va ghi vao `fls_*`.

★★ MOT CHO LECH SPEC, khai ra chu khong am tham. `DEV-10` `T-JOIN-03` doi:
*"phieu 3 dong, Σ = tien bank ⇒ **3 dong ITL**"*. Module nay **khong** lam the,
va day la ly do:

Tach mot dong bank thanh N dong so lam **vo the 1-1 giua so va nguon** — thu ma
moi cong doi soat cua ca he dang dua vao (`vao = so + loai + rong + trung`).
Doi lai duoc gi: **27 dong** (hinh `B`). Doi lai mat gi: cong bon duong tro
thanh mot cong co ngoai le, va cong co ngoai le la cong sap chet.

⇒ Ca ba hinh ghep duoc (`A` 2.256 · `B` 27 · `C` 394 dong) dau vao **bang noi**
`fls_pm_link(itl_id, pm_line_id, amount, hinh)` — **mot dong so, N moi noi**, ma
so dong `fls_itl` ⛔ khong doi. `GAP-JOIN-03` **da dong 27/08** (migration 0007).

★ Va moi noi chi con **MOT cho**: cot `fls_itl.pm_line_id` DA BO. Giu ca cot lan
bang la hai ban su that cho cung mot viec — dung cai benh ma ca khuon `fls/db/`
nay dung ra de chua.

⛔ Cong Σ di kem, va no la cong chu khong phai bao cao: voi moi dong so co moi
noi, **Σ tien cac moi noi PHAI bang tien dong bank**. Thieu cong nay thi phep
chia tien cua hinh `B` co the bia ra hay lam mat tien ma khong ai thay — va
"khong ai thay" la dung cai ca he nay dung ra de chan.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any, Sequence

from fls.adapters.bank import nap
from fls.adapters.pm_join import (DongBank, DongPM, canon_ref, moi_noi,
                                  xep_ca_lat)
from fls.canon.le import ma_le, ten_le
from fls.canon.row import CanonRow
from fls.canon.validate import parse_ngay, parse_so, validate
from fls.ledger.build import NgucCanh, dung_dong
from fls.ledger.classifying import khoi_tu_canon
from fls.repo.itl_repo import chen_bo_qua_trung

_NGAY, _SO_CT, _CURR, _NO, _CO, _LE_PAYER = 0, 1, 3, 4, 5, 11


@dataclass(frozen=True)
class KetQuaNap:
    """Bon duong + hai con so trang thai. `can()` la cong, khong phai bao cao."""
    run_id: str
    vao: int
    vao_so: int
    loai: int
    rong: int
    bo_qua_trung: int
    unmapped: int
    ok: int
    ghep_pm: int = 0
    # ★ Anh chup dong lenh chi (`fls_pm_line`) — ⛔ KHONG nam trong phep can bon
    # duong: no dem ben PM, con bon duong dem ben BANK. Gop hai truc vao mot
    # phep can la lam phep can do thu ma no khong do.
    dong_pm: int = 0
    ly_do_loai: dict[str, int] = field(default_factory=dict)

    def tong(self) -> int:
        return self.vao_so + self.loai + self.rong + self.bo_qua_trung

    def can(self) -> bool:
        return self.tong() == self.vao and self.unmapped + self.ok == self.vao_so

    def bao(self) -> str:
        g = f" · ghep PM {self.ghep_pm}" if self.ghep_pm else ""
        g += f" · anh chup PM {self.dong_pm} dong" if self.dong_pm else ""
        return (f"run {self.run_id}: vao {self.vao} = so {self.vao_so} + loai "
                f"{self.loai} + rong {self.rong} + trung {self.bo_qua_trung}"
                f"  ·  trong so: ok {self.ok} · UNMAPPED {self.unmapped}{g}")


def danh_seq_trung(hang: Sequence[tuple[int, CanonRow]], nc: NgucCanh) -> list[int]:
    """Danh `seq_trung` cho tung dong theo dung bo khoa cua `content_key`.

    Thu tu la thu tu DOC — nen chay lai cung lat cho cung ket qua (cong #4).
    """
    dem: Counter = Counter()
    ra: list[int] = []
    for _dong, row in hang:
        k = (nc.source_system, nc.source_sheet,
             parse_ngay(row.at(_NGAY)), parse_so(row.at(_NO)),
             parse_so(row.at(_CO)), row.at(_SO_CT))
        ra.append(dem[k])
        dem[k] += 1
    return ra


def _bank_tu_canon(hang, nc: NgucCanh) -> list[DongBank]:
    """Canon -> `DongBank` cho phep ghep. Ma tham chieu = cot B "So chung tu".

    ⚠ Do la khoa ma `VLOOKUP` cua AS-IS dung — nhin thay trong chinh loi cua no:
    `#N/A (Did not find value '4.36619E+15' in VLOOKUP evaluation)`.
    """
    ra = []
    for dong, row in hang:
        no = parse_so(row.at(_NO)) or 0
        co = parse_so(row.at(_CO)) or 0
        ra.append(DongBank(dong, canon_ref(row.at(_SO_CT)),
                           Decimal(str(no)) + Decimal(str(co)),
                           str(row.at(_CURR) or "").strip()))
    return ra


def ghep_pm(hang, nc: NgucCanh, pm: Sequence[DongPM]
            ) -> tuple[dict[int, list[tuple[str, Decimal, str]]], dict[str, str], Any]:
    """Tra (dong_sheet -> [(line_id, tien, hinh), ...]), + ly do, + thong ke.

    ⭐ Ca ba hinh ghep duoc deu ra day, ke ca `B` (1 bank × N PM): mot `dong_sheet`
    co the mang **NHIEU** moi noi. Truoc 27/08 ham nay tra mot cap `(line, hinh)`
    nen `B` khong dau duoc va 27 dong phai vao hang cho.

    ⛔ Hinh `D`/`E`/`F` van vao `ly_do` — chung ⛔ khong ghep duoc, do la co y:
    `D` co nhieu cach chia deu cong dung, `E` khac tien te, `F` lech Σ.
    """
    bank = _bank_tu_canon(hang, nc)
    nhom, tk = xep_ca_lat(bank, pm)
    noi: dict[int, list[tuple[str, Decimal, str]]] = {}
    ly_do: dict[str, str] = {}
    for n in nhom:
        if n.ghep_duoc:
            for dong, line, tien in moi_noi(n):
                noi.setdefault(dong, []).append((line, tien, n.hinh))
        else:
            ly_do[n.ref] = f"hinh {n.hinh}: {n.ly_do}" if n.ly_do else f"hinh {n.hinh}"
    return noi, ly_do, tk


def kiem_tong_moi_noi(noi: dict[int, list[tuple[str, Decimal, str]]],
                      tien_bank: dict[int, Decimal]) -> list[str]:
    """⛔ Σ tien moi noi cua mot dong so PHAI bang tien dong bank. Rong = khop.

    Day la cong chan phep chia tien cua hinh `B` bia ra hay lam mat tien. Voi
    `A`/`C` no la mot phep dong nghia (mot moi noi mang tron ven so tien), nhung
    van kiem — mot cong chi kiem truong hop kho la cong khong biet minh con song.
    """
    ra: list[str] = []
    for dong, ms in sorted(noi.items()):
        tong = sum((t for _l, t, _h in ms), Decimal(0))
        that = tien_bank.get(dong)
        if that is None:
            ra.append(f"dong {dong}: co {len(ms)} moi noi ma KHONG co dong bank")
        elif tong != that:
            ra.append(f"dong {dong}: Σ moi noi {tong} != tien bank {that} "
                      f"(lech {tong - that}, {len(ms)} moi noi hinh "
                      f"{ms[0][2] if ms else '?'})")
    return ra


def chen_moi_noi(conn, nc: NgucCanh,
                 moi: list[tuple[int, str, Decimal, str]]) -> int:
    """Chen vao `fls_pm_link`. Tra so moi noi THUC SU chen.

    ⛔ `ON CONFLICT DO NOTHING`: chay lai lan hai thi moi noi da co, bo qua —
    ⛔ khong DELETE, ⛔ khong UPDATE (cung tinh than `INV-I08`).
    """
    if not moi:
        return 0
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO fls_pm_link (itl_id, pm_line_id, amount, hinh, run_id) "
            "VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING",
            [(i, l, t, h, nc.run_id) for i, l, t, h in moi])
    return int(conn.execute(
        "select count(*) from fls_pm_link where run_id=%s", (nc.run_id,)).fetchone()[0])


def chen_dong_pm(conn, nc: NgucCanh, pm: Sequence[DongPM]) -> int:
    """Chen ANH CHUP dong lenh chi vao `fls_pm_line`. Tra so dong CO THAT trong kho.

    ★★ Vi sao anh chup nay ton tai: xem `fls/db/schema.py` mo ta `_FLS_PM_LINE`
    va migration `0011`. Tom lai — bo nap doc dong lenh **luc chay roi khong luu**,
    nen thao tac ghep tay o man `F01` ⛔ khong the co danh sach ung vien.

    ⛔ `ON CONFLICT DO NOTHING` theo khoa `(run_id, pm_line_id)`: chay lai cung
    mot lan nap thi bo qua — ⛔ khong UPDATE, ⛔ khong DELETE. Nap LAI nguon la
    mot `run_id` KHAC, tuc **anh chup moi nam canh anh cu**, khong de len nhau.

    ⛔ Dong THIEU dinh danh (`line` rong) bi BO va DEM RIENG, ⛔ khong duoc am
    tham bo: mot dong lenh khong co ma dong thi ⛔ khong ghep vao dau duoc, nhung
    "co bao nhieu dong nhu the" la con so nguoi doc can biet (`INV-I16`).

    ⚠ Tra ve **so dong co that trong kho cua lan nap nay**, ⛔ khong phai so dong
    vua chen: hai con so khac nhau khi chay lai, va bao con so thu hai thi lan
    chay lai nao cung noi "chen 0" trong khi kho van du. Cung luat voi
    `chen_moi_noi`.
    """
    if not pm:
        return 0
    tot = [x for x in pm if (x.line or "").strip()]
    if len(tot) != len(pm):
        # ⛔ Khong im lang. In ra ngay day vi ham nay chay TRONG mot giao dich —
        # nem loi la huy ca lan nap chi vi mot dong lenh thieu ma.
        print(f"⚠ anh chup PM: BO {len(pm) - len(tot)} dong khong co `ID PMLine` "
              f"(⛔ khong ghep vao dau duoc)")
    with conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO fls_pm_line (run_id, pm_line_id, pm_slip_id, ref_tho,"
            " ref_canon, amount, curr, status, hd, cdt1, source_row)"
            " VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            " ON CONFLICT (run_id, pm_line_id) DO NOTHING",
            [(nc.run_id, x.line.strip(), (x.slip or "").strip(), x.ref_tho,
              x.ref, x.tien, x.cur, x.status or None, x.hd, x.cdt1,
              x.dong_sheet) for x in tot])
    return int(conn.execute(
        "select count(*) from fls_pm_line where run_id=%s",
        (nc.run_id,)).fetchone()[0])


def mo_run(conn, nc: NgucCanh, tong_dong: int | None = None) -> None:
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO fls_run (run_id, contract_version, canon_version,"
            " mapping_version, row_count, state) VALUES (%s,%s,%s,%s,%s,'staged')"
            " ON CONFLICT (run_id) DO NOTHING",
            (nc.run_id, nc.contract_version, nc.canon_version,
             nc.mapping_version, tong_dong))


def dong_run(conn, run_id: str, trang_thai: str = "mapped") -> int:
    """Chot run. `row_count` DEM TU BANG, ⛔ khong lay so dong vua chen.

    ⚠ Ban dau ham nay nhan `so_dong = len(da_vao)`. Chay lan hai (bo qua het) thi
    `row_count` bi ghi thanh **0** trong khi so co 9.973 dong — mot lan chay
    khong lam gi lai xoa mat con so cua lan chay that.
    """
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM fls_itl WHERE run_id = %s", (run_id,))
        n = cur.fetchone()[0]
        cur.execute("UPDATE fls_run SET row_count = %s, state = %s WHERE run_id = %s",
                    (n, trang_thai, run_id))
    return n


def them_le(conn, tai: Sequence[dict[str, Any]]) -> int:
    """Bo sung ma phap nhan QUAN SAT DUOC vao `fls_le`. Tra so ma moi.

    ⚠ Vi sao phai co buoc nay. `fls_itl.le` va `le_payer` FK toi `fls_le`, va
    `fls_le` **rong**. Lan nap that dau tien do ngay tai day:

        ForeignKeyViolation … Key (le)=(VVOT) is not present in table "fls_le"

    Danh muc nay la danh muc **quan sat duoc**, ⛔ khong phai danh muc duoc soan:
    ten lay tu nguon khi nguon co noi ('VGOH - APERO HQ'), NULL khi khong
    (`GAP-LE-01`), va `is_entity` de mac dinh — ⛔ khong tu gan false cho
    'Cash Treasury' du no gan chac khong phai phap nhan, vi NGUON KHONG NOI.
    """
    ma: dict[str, str | None] = {}
    for p in tai:
        for k in ("le", "le_payer"):
            if p[k]:
                ma.setdefault(p[k], None)
    # ten: lay tu chuoi goc trong canon (vi tri L = 11) neu co dang 'MA - Ten'
    for p in tai:
        t = ten_le((p["canon"] or [None] * 38)[_LE_PAYER])
        m = ma_le((p["canon"] or [None] * 38)[_LE_PAYER])
        if t and m in ma and ma[m] is None:
            ma[m] = t
    if not ma:
        return 0
    with conn.cursor() as cur:
        cur.execute("SELECT le_code FROM fls_le")
        da_co = {r[0] for r in cur.fetchall()}
        moi = {k: v for k, v in ma.items() if k not in da_co}
        for k, v in sorted(moi.items()):
            cur.execute("INSERT INTO fls_le (le_code, le_name) VALUES (%s,%s)"
                        " ON CONFLICT (le_code) DO NOTHING", (k, v))
    return len(moi)


def _chen_reject(conn, nc: NgucCanh, loai: list[tuple[int, list[str]]]) -> int:
    """Ghi dong bi loai. Tra so dong THAT SU them moi.

    ⚠ `WHERE NOT EXISTS` chu khong phai chen thang. Bon lan chay `nap_that.py`
    trong mot buoi de lai **76 dong** trong `fls_reject` cho **19 dong bi loai**
    that — moi lan chay lai nhan them mot ban. Con so "so dong bi loai" la con
    so ma nguoi ta doc de biet nguon co bao nhieu lo; nhan bon lan thi no thanh
    mot con so vo nghia, va no vo nghia trong IM LANG.

    ⛔ KHONG dung DELETE de "don truoc khi ghi": mot ham don duoc `fls_reject`
    la mot ham co the xoa bang chung. Chan bang dieu kien, khong bang xoa.

    ⚠ CHUA CO rang buoc UNIQUE(run_id, source_row) o tang DB (`fls/db/model.py`
    chua ho tro khoa nhieu cot) ⇒ `GAP-DB-P0-03`. Dieu kien nay la lop chan duy
    nhat, nen no co test.
    """
    if not loai:
        return 0
    n = 0
    with conn.cursor() as cur:
        for dong, ly_do in loai:
            cur.execute(
                "INSERT INTO fls_reject (run_id, source_system, source_sheet,"
                " source_row, reason)"
                " SELECT %s,%s,%s,%s,%s WHERE NOT EXISTS ("
                "   SELECT 1 FROM fls_reject WHERE run_id = %s AND source_row = %s)",
                (nc.run_id, nc.source_system, nc.source_sheet, dong,
                 " | ".join(ly_do), nc.run_id, dong))
            n += cur.rowcount
    return n


def chay(conn, tho: Sequence[Sequence[Any]], nc: NgucCanh,
         header: Sequence[Any] | None = None,
         pm: Sequence[DongPM] | None = None) -> KetQuaNap:
    """Nap ca lat vao so. ⛔ Ba duong khong can thi NO va khong ghi gi."""
    so_moi_noi = 0
    so_dong_pm = 0
    hang, loai, tk = nap(tho, header=header)
    if not tk.can():
        raise AssertionError("adapter tra ba duong khong can: " + str(tk))

    seq = danh_seq_trung(hang, nc)
    noi_pm: dict[int, list[tuple[str, Decimal, str]]] = {}
    tk_ghep = None
    if pm:
        noi_pm, _ly_do_ghep, tk_ghep = ghep_pm(hang, nc, pm)
        # ⛔ Cong Σ DUNG TRUOC khi ghi. Lech thi NO va khong ghi mot dong nao:
        # ghi roi moi phat hien tien lech thi cong chi con la bao cao.
        lech = kiem_tong_moi_noi(
            noi_pm, {b.dong_sheet: b.tien for b in _bank_tu_canon(hang, nc)})
        if lech:
            raise AssertionError("⛔ Σ moi noi != tien bank, KHONG ghi gi: "
                                 + " | ".join(lech[:5]))
    tai: list[dict[str, Any]] = []
    them_loai: list[tuple[int, list[str]]] = []
    for (dong, row), s in zip(hang, seq):
        kq = validate(row)
        if kq.loai:                       # lop so tu choi -> fls_reject, CO LY DO
            them_loai.append((dong, kq.loai))
            continue
        ms = noi_pm.get(dong)
        tai.append(dung_dong(row, dong, nc, khoi=khoi_tu_canon(row),
                             seq_trung=s, pm=ms[0][2] if ms else None))

    loai = loai + them_loai
    ly_do = dict(Counter(x.split(" la o loi")[0].split(":")[0]
                         for _d, l in loai for x in l))

    # ⛔ Cong DUNG TRUOC khi ghi: bon duong phai can khi chua co dong nao trung.
    if len(tai) + len(loai) + tk.rong != tk.vao:
        raise AssertionError(
            f"⛔ bon duong khong can, KHONG ghi gi: vao {tk.vao} != so {len(tai)}"
            f" + loai {len(loai)} + rong {tk.rong}")

    # ⛔ MOT giao dich cho ca lan nap. Ban dau ham nay ghi tung buoc voi
    # `autocommit=True`, va hai lan nap that DAU TIEN deu NO giua duong (FK
    # `fls_le` rong, roi kieu `date` cua svc_*) — moi lan de lai mot phan dong
    # DA COMMIT trong so: 394 dong. Cong bon duong khong the go cai da commit,
    # nen cong chi con la mot bao cao, khong con la cong.
    with conn.transaction():
        mo_run(conn, nc, tk.vao)
        them_le(conn, tai)
        _chen_reject(conn, nc, loai)
        ket = chen_bo_qua_trung(conn, tai)
        # Moi noi can `itl_id`, nen no phai chen SAU — nhung TRONG cung mot
        # giao dich: mot lan nap de lai dong so ma thieu moi noi la mot lan nap
        # nua vao "so co ma khong ai biet ghep the nao".
        # ⚠ Dong bi BO QUA vi trung noi dung thi moi noi cua no DA CO tu lan
        # nap truoc (khoa `(itl_id, pm_line_id)`), nen ⛔ khong chen lai.
        can_chen: list[tuple[int, str, Decimal, str]] = []
        for p, itl_id in zip(tai, ket):
            if itl_id is None:
                continue
            for line, tien, hinh in noi_pm.get(p["source_row"], ()):
                can_chen.append((itl_id, line, tien, hinh))
        so_moi_noi = chen_moi_noi(conn, nc, can_chen)
        # ★ Anh chup dong lenh chi ghi TRONG cung giao dich voi moi noi. Neu
        # tach ra ngoai thi co the ket thuc o trang thai "co moi noi ma khong co
        # dong lenh nao de tra" — dung cai trang thai lam man `F01` khong the
        # ghep tay, tuc dung cai lo `GAP-API-04` sinh ra de bit.
        so_dong_pm = chen_dong_pm(conn, nc, pm or ())

    # ⚠ Dem `work_status` CHI tren dong THUC SU vao so. Dem tren `tai` thi moi
    # lan nap lai (bo qua het) se bao "9.000 dong UNMAPPED" ma so khong tang.
    da_vao = [p for p, i in zip(tai, ket) if i is not None]
    unmapped = sum(1 for p in da_vao if p["work_status"] == "UNMAPPED")
    kq = KetQuaNap(
        run_id=nc.run_id, vao=tk.vao, vao_so=len(da_vao), loai=len(loai),
        rong=tk.rong, bo_qua_trung=len(tai) - len(da_vao),
        unmapped=unmapped, ok=len(da_vao) - unmapped, ly_do_loai=ly_do,
        ghep_pm=so_moi_noi if pm else 0, dong_pm=so_dong_pm)
    if not kq.can():
        raise AssertionError("⛔ bon duong khong can sau khi ghi: " + kq.bao())
    dong_run(conn, nc.run_id)
    return kq
