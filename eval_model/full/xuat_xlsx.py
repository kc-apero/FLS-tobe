"""Xuat hai workbook de NGUOI doc: input (gui model) va dap_an (giau). Chi doc CSV/JSON da sinh."""
import csv, json
from pathlib import Path
from openpyxl import Workbook
from openpyxl.styles import Font

GOC = Path(__file__).parent


def so(v):
    try:
        return int(v) if v.lstrip("-").isdigit() and len(v.lstrip("-")) < 16 else float(v) if any(c.isdigit() for c in v) and v.replace(".", "", 1).lstrip("-").isdigit() else v
    except Exception:
        return v


def them(wb, ten, rows):
    ws = wb.create_sheet(ten[:31])
    for i, r in enumerate(rows):
        ws.append([so(x) if i else x for x in r])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.freeze_panes = "A2"


def lam(thu_muc, ra):
    wb = Workbook(); wb.remove(wb.active)
    for p in sorted((GOC / thu_muc).iterdir()):
        if p.suffix == ".csv":
            them(wb, p.stem, list(csv.reader(p.open(encoding="utf-8"))))
        elif p.suffix == ".json":
            them(wb, p.stem, [["json"]] + [[l] for l in p.read_text(encoding="utf-8").splitlines()])
    wb.save(GOC / ra)
    print("->", ra)


lam("input", "FLS_dataset_INPUT.xlsx")
lam("dap_an", "FLS_dataset_DAP_AN.xlsx")
