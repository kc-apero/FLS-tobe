"""Chung minh bo cham DUNG truoc khi tin no (cong phai thay DO):
  ① ghep chinh dap_an thanh mot cau tra loi dung dinh dang -> phai ra 100%
  ② lam hong co chu y 6 cho (loi thuong gap) -> phai < 100% va bat dung tung khoi bi hong
⛔ Tep tao ra o kiem_cham/ CHUA dap an — khong bao gio gui cho model.
"""
import csv
import io
import json
from pathlib import Path

from cham_full import KHOI_RA, cham

GOC = Path(__file__).parent
DA = GOC / "dap_an"
TEP = {"A2_LEDGER": "a2_ledger.csv", "A2_GHEP": "a2_ghep.csv", "A3_ITL": "a3_itl_adjust.csv",
       "A3_HANG_CHO": "a3_hang_cho.csv", "R1_SO_DU": "r1_so_du.csv", "R2_CF": "r2_cf.csv", "R3_PL": "r3_pl.csv"}


def tra_loi(sua=None) -> str:
    phan = []
    for ten in KHOI_RA:
        if ten == "A1_KIEM_NGUON":
            body, lang = (DA / "a1_kiem_nguon.json").read_text(encoding="utf-8"), "json"
        elif ten == "A4_AUDIT":
            body, lang = (DA / "a4_audit.json").read_text(encoding="utf-8"), "json"
        else:
            body, lang = (DA / TEP[ten]).read_text(encoding="utf-8"), "csv"
        if sua and ten in sua:
            body = sua[ten](body)
        phan.append(f"### {ten}\n```{lang}\n{body.strip()}\n```\n")
    return "\n".join(phan)


def sua_csv(fn):
    def f(body):
        rows = list(csv.DictReader(io.StringIO(body)))
        rows = fn(rows)
        out = io.StringIO()
        w = csv.DictWriter(out, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
        return out.getvalue()
    return f


def hong_itl(rows):
    for r in rows:                 # loi kinh dien: MID = S khi T rong -> khong anh huong V; loi that: mac dinh svc
        if r["svc_start_T"] == "Input here":
            r["svc_start_V"] = ""
            break
    for r in rows:                 # doan hd thay vi day nguoi
        if r["work_status"] == "UNMAPPED":
            r["hd_V"] = "SC | Server Cost"
            break
    return rows


def main():
    out = GOC / "kiem_cham"
    out.mkdir(exist_ok=True)
    (out / "dap_an_dang_tra_loi.md").write_text(tra_loi(), encoding="utf-8")
    sai = {
        "A2_GHEP": sua_csv(lambda rr: [dict(r, hinh="A") if r["hinh"] == "D" else r for r in rr]),
        "A3_ITL": sua_csv(hong_itl),
        "A3_HANG_CHO": sua_csv(lambda rr: rr[1:]),
        "R1_SO_DU": sua_csv(lambda rr: [dict(r, ccr_go=r["cuoi_ky"], dif="0") for r in rr]),
        "R3_PL": sua_csv(lambda rr: [dict(r, **{"2026-10-07": "0"}) if r["dong"] == "FI" else r for r in rr]),
        "A4_AUDIT": lambda b: json.dumps({"loi": json.loads(b)["loi"][1:]}),
    }
    (out / "sai_co_chu_y.md").write_text(tra_loi(sai), encoding="utf-8")
    d1, d2 = cham((out / "dap_an_dang_tra_loi.md").read_text(encoding="utf-8")), cham((out / "sai_co_chu_y.md").read_text(encoding="utf-8"))
    print(f"{'khoi':16s} {'dap an':>8} {'sai co y':>9}")
    for k in KHOI_RA:
        print(f"{k:16s} {d1[k]['diem']:8.1%} {d2[k]['diem']:9.1%}")
    print(f"{'TONG':16s} {d1['TONG']:8.1%} {d2['TONG']:9.1%}")
    assert d1["TONG"] == 1.0, "dap an phai 100%"
    hong = {"A2_GHEP", "A3_ITL", "A3_HANG_CHO", "R1_SO_DU", "R3_PL", "A4_AUDIT"}
    for k in KHOI_RA:
        assert (d2[k]["diem"] < 1.0) == (k in hong), f"bo cham bat sai khoi {k}"
    print("OK: dap an = 100%; 6 khoi lam hong deu bi bat, 3 khoi con lai van 100%.")


if __name__ == "__main__":
    main()
