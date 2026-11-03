# -*- coding: utf-8 -*-
"""SINH ban do KIEN TRUC THEO TANG tu chinh ban khai `fls/db/schema.py`.

    python tools/sinh_ban_do_tang.py            # sinh + bom vao BA-05
    python tools/sinh_ban_do_tang.py --kiem     # CHI kiem, ⛔ khong ghi (cong)

⛔⛔⛔ **Vi sao ban do nay phai duoc SINH RA, ⛔ khong ve tay.**

`ERD-CONTRACT.mmd` sinh tu `schema.py` va co cong `G-ERD-1` canh ⇒ no ⛔
**khong bao gio gia**. Nhung no la mot `erDiagram` **PHANG**: 23 bang nam
canh nhau, ⛔ khong noi duoc **cai nao dung truoc cai nao**, va owner doc
xong van ⛔ khong thay duoc **kien truc**.

⇒ Tep nay them **DUNG MOT** chieu doc — `tang` — va no cung la **mot truong
  cua ban khai**, ⛔ khong phai mot tep ve tay thu hai.

★ **Bay TANG, va moi tang tra loi MOT cau:**

    ① anh      — *"to giay luc ay ghi gi"*        chi-THEM, ⛔ khong ai sua
    ② nap      — *"dong nao vao so, dong nao BI LOAI va vi sao"*
    ③ so       — *"so ke toan"*                    append-only (`INV-I08`)
    ④ ghep     — *"dong tien nay chi theo lenh nao"*
    ⑤ viec     — *"NGUOI con phai lam gi"*
    ⑥ sua      — *"ai da go gi, luc nao, vi sao"*
    ⑦ ha tang  — sổ di tru

⚠ **`tang` ⛔ KHONG doi mot dong DDL nao.** Hai bang cung tang ⛔ khong co gi
   chung o Postgres; chung chung **cau hoi ma chung tra loi**. ⇒ No la mot
   phep **DOC**, va vi the no phai **do duoc** chu ⛔ khong duoc la cam tinh:
   cong duoi day doi **moi bang** khai tang, va doi ban ve **khop** ban khai.

⛔⛔ **Xanh tren tap RONG = CHUA DO.** ⛔ Khong doc duoc bang nao ⇒ NO.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys

GOC = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(GOC))

from fls.db import schema  # noqa: E402

MMD = GOC / "ERD-TANG.mmd"
MMD_KHAU = GOC / "ERD-KHAU.mmd"
DOC = GOC / "docs" / "ITL" / "02_BA" / "05_DATA_DICTIONARY_ERD.md"
# ⭐ Trang owner MO RA. Sinh tu **cung mot ban khai** — ⛔ khong ve tay mot
#   ban thu ba, vi ban thu ba se la ban ⛔ khong ai canh.
HTM = (GOC / "docs" / "ITL" / "02_BA" / "Artifacts"
       / "Ban-do-Kien-truc-7-Tang.html")
KHOI = re.compile(r"```mermaid\s*\nflowchart .*?```", re.S)
# ⭐ Khoi KHAU co **moc rieng** chu ⛔ khong dung `KHOI`: hai khoi cung la
#   `flowchart`, nen mot phep thay *"khop cai dau tien"* se **ghi de nham**
#   ngay lan dau hai khoi doi cho cho nhau. Moc thi ⛔ khong nham duoc.
MOC_DAU = "<!-- SINH-KHAU:BAT-DAU -->"
MOC_CUOI = "<!-- SINH-KHAU:KET-THUC -->"
KHOI_KHAU = re.compile(re.escape(MOC_DAU) + r".*?" + re.escape(MOC_CUOI), re.S)

# Ten doc duoc + cau hoi cua tung tang. ⛔ Thu tu o day LA thu tu tren ban ve.
TANG: tuple[tuple[str, str, str], ...] = (
    ("1-anh", "① ẢNH CHỤP",
     "tờ giấy lúc ấy ghi gì — chỉ-THÊM, ⛔ không ai sửa"),
    ("2-nap", "② NẠP",
     "dòng nào vào sổ, dòng nào BỊ LOẠI và vì sao"),
    ("3-so", "③ SỔ KẾ TOÁN",
     "append-only (INV-I08) + hai danh mục nó tra tới"),
    ("4-ghep", "④ GHÉP LỆNH CHI",
     "dòng tiền này chi theo lệnh nào"),
    ("5-viec", "⑤ VIỆC CỦA NGƯỜI",
     "người còn phải làm gì"),
    ("6-sua", "⑥ SỬA & VẾT",
     "ai đã gõ gì, lúc nào, vì sao"),
    ("7-ha-tang", "⑦ HẠ TẦNG", "sổ di trú"),
)

# ⭐⭐⭐ KHAU NGHIEP VU — truc THU HAI, them 17/09 theo yeu cau owner:
#     *"sap xep cho toi theo flow chinh: nap data → ghep lenh chi → adjust ITL.
#       Toi muon biet cac entity thuoc cac module nghiep vu nao"*
#
# ⛔⛔ **Thu tu khai o day LA thu tu dong chay tren ban ve** — ba khau dau
#    doc trai→phai; hai khau sau la **CAT NGANG**, ⛔ khong nam trong chuoi.
#
# ⛔ Ten lay lai tu `01_Orchestrator/09_MILESTONES_HAI_TAC_VU` (moc `A` · tac
#   vu ① · tac vu ②) — ⛔ khong dat ten thu tu cho mot thu da co ten.
KHAU: tuple[tuple[str, str, str, str], ...] = (
    ("A-nap", "Ⓐ NẠP DATA", "chuoi",
     "sao kê · lệnh chi vào kho — mốc `A`, đường LẤY dữ liệu"),
    ("B-ghep", "Ⓑ GHÉP LỆNH CHI", "chuoi",
     "dòng tiền này chi theo lệnh nào — tác vụ ①"),
    ("C-sua", "Ⓒ SỬA ITL", "chuoi",
     "kế toán gõ 7 trường, máy giữ vết — tác vụ ②"),
    ("S-so", "SỔ & DANH MỤC", "nen",
     "trục chung — cả ba khâu đều chạm"),
    ("V-viec", "VIỆC CỦA NGƯỜI", "ngang",
     "cắt ngang Ⓑ và Ⓒ — người còn phải làm gì"),
    ("H-ha-tang", "HẠ TẦNG", "ngoai", "sổ di trú"),
)

# ⭐⭐⭐ TU DIEN TEN — them 2026-09-17, owner chot *"dung TEN TAC VU"*.
#
# ⛔⛔ **Mot khau dang mang BA BO TEN, va ⛔ khong cho nao noi chung la MOT.**
#   Day la phan con lai cua `D1` sau khi cau *"tai lieu chua bao gio doc ten
#   tep"* bi bac: ten tep **CO** trong tai lieu *(`BA-05:39`+`:130`)*, ⛔ nhung
#   ⛔ khong mot dong nao noi `File 1_2` **la** cai ma `09_MILESTONES` goi la
#   *"moc `A`"*. Nguoi doc phai tu noi — va do la cho drift sinh ra.
#
# ⛔ Luat: **ten CHUAN la ten TAC VU** *(owner 17/09)*; hai bo kia la **BI
#   DANH**. ⇒ ⛔ **Khong doi ten tep** `09_MILESTONES_HAI_TAC_VU.md`.
#
# ⚠ **Mot ten co the tro toi NHIEU khau, va do la su that ⛔ khong duoc lam
#   tron.** «ITL (1/2)» la mot **TEP**, ⛔ khong phai mot buoc: trong no co ca
#   `Transaction Original` *(Ⓐ)* lan `Transaction Mapping L1` *(Ⓑ)*. Chinh vi
#   the owner tra loi `Q1` la *"no la mot BUOC"*, ⛔ khong phai module thu tu.
TU_DIEN_TEN: tuple[tuple[str, str, tuple[str, ...], str], ...] = (
    # (ten dang luu hanh, xuat xu cua ten, cac khau no tro toi, ghi chu)
    ("mốc `A`", "tài liệu ⭐ CHUẨN", ("A-nap",), "`09_MILESTONES` §1"),
    ("tác vụ ①", "tài liệu ⭐ CHUẨN", ("B-ghep",), "mapping PM ↔ Transaction"),
    ("tác vụ ②", "tài liệu ⭐ CHUẨN", ("C-sua",), "adjust thông tin ITL"),
    ("nạp data", "owner 17/09", ("A-nap",), ""),
    ("ghép lệnh chi", "owner 17/09", ("B-ghep",), "PM & Transaction Reference"),
    ("ITL adjust (2/2)", "owner 17/09", ("C-sua",), ""),
    ("ITL (1/2)", "owner 17/09", ("A-nap", "B-ghep"),
     "⚠ là một **TỆP**, ⛔ không phải một bước — nó chứa cả hai khâu"),
    ("`P100 _ Bank Transactions` · `P100 _ Cash Ledger`", "AS-IS tệp",
     ("A-nap",), "`60` tab `R |` + `8` nguồn quỹ"),
    ("`A _ PAY100 _ PM11 Entry Data`", "AS-IS tệp", ("A-nap",),
     "`PE_Unpivot` · `PI_Unpivot` · `PM_Unpivot`"),
    ("`ITL … File 1_2 (RAW)`", "AS-IS tệp", ("A-nap", "B-ghep"),
     "tab `Transaction Original` ⇒ Ⓐ · `Transaction Mapping L1` ⇒ Ⓑ"),
    ("`ITL … File 2_2 (ADJUSTED)`", "AS-IS tệp", ("C-sua",), "tab `ITL Ledge`"),
    ("`A-nap` · `B-ghep` · `C-sua`", "mã nguồn", ("A-nap", "B-ghep", "C-sua"),
     "`fls/db/schema.py` — trường `khau`"),
)

# ⭐⭐⭐ TU DIEN THUC THE — them 2026-09-17, owner hoi *"ma ten cua Giao dich
#     (transaction) la `fls_itl` da dung khai niem, ten file excel, ggsheet
#     chua?"*
#
# ⛔⛔ **Vi sao mot hang RIENG chu ⛔ khong noi dai `TU_DIEN_TEN`.** Hai hang
#   tra loi HAI cau: `TU_DIEN_TEN` noi ve **KHAU** *(mot viec cua nguoi)*,
#   hang nay noi ve **THUC THE** *(mot bang trong kho)*. Gop lai thi cot
#   `Khau` cua bang sinh ra mang hai nghia, va cong `T3` — von hoi *"moi khau
#   chuoi co du ba xuat xu chua"* — se duoc **tra loi ho** boi cac dong thuc
#   the. Do dung lop loi ma chinh bai `test_ITL_1_tren_2_trai_DUNG_HAI_khau`
#   da bat: mot dong khac tra loi ho thi cong **XANH GIA**.
#   *(Cung mot luat voi `SAU_TRUONG` vs `TRUONG_HOP_LE` o `adapters/sao_ke`:
#     ⛔ dung gop hai khai niem vao mot hang.)*
#
# ⛔⛔ **Cau tra loi cho owner, ghim o day chu ⛔ khong de trong van xuoi:**
#   `ITL` = *Input Transaction Ledger* = ten **SO**, con bang giu **DONG** ⇒
#   `schema.py` khai `erd_entity="ITL_ROW"`. Ten vat ly mang ten SO, thuc the
#   la DONG — **lech mot bac**, va no **duoc GIU** vi mot ly do cua owner:
#   *"owner ⛔ khong dat ra ten moi, owner **doc ten he dang chay**"*. Doi
#   sang `itl_transaction` la di nguoc chinh nguyen tac ay.
#   ⇒ Cai phai chua ⛔ khong phai CAI TEN, ma la **CAU NOI** — va no o day.
#
# ⛔ Con `Ledge` thi CO Y ⛔ khong mang sang: tab that ten `ITL Ledge`
#   *(thieu chu `r`)*. `R-A2` buoc chep nguyen van loi chinh ta **trong tai
#   lieu**, ⛔ nhung bê no vao **ten bang** thi loi ay song mai trong moi cau
#   SQL. ⇒ Tai lieu giu `ITL Ledge`, kho dung `fls_itl`.
FLS_DUNG_MOI = "⛔ FLS dựng mới"

TU_DIEN_THUC_THE: tuple[tuple[str, str, str, str], ...] = (
    # (bang trong kho, khai niem nghiep vu, ten o AS-IS, ghi chu)
    ("fls_adjustment", "bút toán điều chỉnh",
     "`ITL Ledge` vùng ADJUSTMENT", "7 khối × 4 cột"),
    ("fls_chup", "một lần đọc Sheets", FLS_DUNG_MOI,
     "`QĐ-ITL-110` — AS-IS đọc thẳng, ⛔ không lưu lại ảnh"),
    ("fls_chup_dong", "một dòng vùng CHUẨN", FLS_DUNG_MOI, ""),
    ("fls_chup_nguon", "một nguồn trong một lần đọc", FLS_DUNG_MOI,
     "nguồn ra `0` dòng vẫn phải CÓ MẶT"),
    ("fls_da_xong", "việc đã xong", FLS_DUNG_MOI, "khung xem"),
    ("fls_itl", "giao dịch",
     "`ITL Ledge` *(File 2_2)* · `Transaction Mapping L1` *(File 1_2)*",
     "⭐ `ITL` = *Input Transaction Ledger* = tên **SỔ**; bảng giữ **DÒNG** ⇒ "
     "`erd_entity` là `ITL_ROW`. Lệch một bậc, và **giữ** — xem khối chú "
     "thích ở `sinh_ban_do_tang.py`"),
    ("fls_journal", "nhật ký sửa", "2 sheet `Log`",
     "`302.259` dòng ở AS-IS"),
    ("fls_khai_cot", "bản khai ánh xạ cột", "dòng 1 mỗi tab `R |`",
     "`68/68` tab khai đủ 6 trường trên `19` bố cục"),
    ("fls_le", "pháp nhân", "`Transaction Mapping L1` cột `P`",
     "⚠ danh mục **SUY từ giá trị** — AS-IS ⛔ không có tab danh mục riêng; "
     "`GAP-LE-01`: thiếu tên cho `24/29` mã"),
    ("fls_mapping_master", "danh mục quyết định phân bổ",
     "tab `Mapping Master` *(file RAW)*", "`73` mã — `QĐ-ITL-70`"),
    ("fls_migration", "sổ di trú", FLS_DUNG_MOI, "hạ tầng"),
    ("fls_moi_noi", "mối nối đang hiệu lực", FLS_DUNG_MOI,
     "khung xem — `fls_pm_link` **trừ** `fls_pm_unlink`"),
    ("fls_nguon_dai", "dải nhãn thô ↔ danh mục",
     "`Range_Condition`/`Debit`/`Credit` ở danh mục",
     "⚠ bản khai **THỨ HAI** — script `Run` của trang tính đọc nó, FLS thì "
     "đọc dòng 1 *(`GAP-KHAI-01`)*"),
    ("fls_pm_line", "dòng lệnh chi *(PM)*", "`PM_Unpivot`",
     "ẢNH CHỤP một lần nạp — `run_id` nằm **trong** khoá chính"),
    ("fls_pm_link", "mối nối tiền ↔ lệnh chi",
     "`Transaction Mapping L1` nhóm LINK", "AS-IS ghép bằng `VLOOKUP`"),
    ("fls_pm_unlink", "bỏ ghép", FLS_DUNG_MOI,
     "bỏ ghép là **THÊM** một dòng, ⛔ không xoá"),
    ("fls_queue_event", "việc của người", FLS_DUNG_MOI,
     "AS-IS giao việc bằng **người bàn giao cho người**"),
    ("fls_queue_reason_weekly", "lý do theo tuần", FLS_DUNG_MOI, "khung xem"),
    ("fls_queue_state", "trạng thái hàng chờ", FLS_DUNG_MOI, "khung xem"),
    ("fls_reject", "dòng bị loại", FLS_DUNG_MOI,
     "⭐ AS-IS ⛔ **không giữ** dòng bị loại — đó chính là lỗ tầng ② vá"),
    ("fls_run", "lô nạp", "`RAW ITLData Management` · `Export Log`",
     "⚠ sổ đăng ký nguồn AS-IS **đang hỏng** — phần lớn ô `#REF!`"),
    ("fls_source", "dòng chảy sao kê", "`60` tab `R |` + `8` nguồn quỹ",
     "⭐ một nguồn ⛔ **không** phải một tài khoản *(`QĐ-ITL-106`)*"),
    ("fls_sua_tay", "ô người gõ", "`ITL Ledge` ô `Manual input`",
     "khung xem — `6.843` ô ở AS-IS"),
    ("fls_dien_giai", "diễn giải sao kê", "`R \|` cột `Description`",
     "⭐ khung xem — dữ liệu **đã có** trong ảnh chụp, chỉ chưa ai nối "
     "*(`QĐ-ITL-145`)*; ⛔ ⛔ không ghi vào sổ *(`INV-I08`)*"),
    ("fls_may_goi_y", "ô máy gợi ý", "`ITL Ledge` cột `Classifying`",
     "⭐ khung xem — **máy suy, NGƯỜI chốt** *(`QĐ-ITL-143`)*; ⛔ ⛔ không "
     "lẫn vào `fls_sua_tay`"),
)

# ⛔ Ba XUAT XU phai co du cho MOI khau chuoi — thieu mot la mot bo ten
#   ⛔ khong noi duoc ve khau nao.
XUAT_XU_BAT_BUOC: tuple[str, ...] = ("tài liệu ⭐ CHUẨN", "owner 17/09",
                                     "AS-IS tệp")

# Chuoi dong chay: chi CAC KHAU nay noi tiep nhau. ⛔ `S`/`V`/`H` ⛔ khong
# nam trong chuoi — ve chung nhu mot mat xich la noi doi ve thu tu.
_CHUOI = tuple(m for m, _, loai, _ in KHAU if loai == "chuoi")


def doc_bang() -> list:
    """Moi `Table` trong `schema.py`. ⛔ Khong go tay mot danh sach thu hai."""
    ra = [v for v in vars(schema).values()
          if hasattr(v, "columns") and hasattr(v, "tang")
          and hasattr(v, "name")]
    return sorted(ra, key=lambda b: b.name)


def canh(bang: list) -> list[tuple[str, str, str]]:
    """`(tu, den, cot)` — **MOI** khoa ngoai, doc tu chinh ban khai.

    ⛔⛔⛔ **Ban dau ham nay loc `den != b.name`, va no am tham nuot mat
       quan he QUAN TRONG NHAT cua ca kho:**

           fls_adjustment.reversal_of  →  fls_adjustment.adj_id

       Mot but toan **DAO** tro ve but toan no dao. Do chinh la co che thay
       cho `DELETE` — `INV-I08` noi so **chi THEM**, nen *"xoa"* trong TO-BE
       la *"them mot dong tro nguoc lai"*. Loc no di la ve mot cai kho trong
       do **⛔ khong the dao duoc gi**.

    ⇒ Bai hoc: mot phep loc viet cho *"cho ban ve gon"* la mot phep loc
      **xoa mat su that**, va no ⛔ khong bao gio tu bao. Gio tu-tro duoc
      **giu va danh dau rieng**.
    """
    ten = {b.name for b in bang}
    ra = []
    for b in bang:
        for c in b.columns:
            if c.fk and c.fk.split(".")[0] in ten:
                ra.append((b.name, c.fk.split(".")[0], c.name))
    return ra


def _nut(b) -> str:
    """Mot nut. View ve KHAC bang — chung la hai thu khac nhau that."""
    la_view = getattr(b, "kind", "table") == "view"
    nhan = b.name + ("<br><i>khung xem</i>" if la_view else "")
    return (f'    {b.name}["{nhan}"]:::view' if la_view
            else f'    {b.name}["{nhan}"]')


def sinh() -> str:
    bang = doc_bang()
    if not bang:
        raise SystemExit(
            "⛔ ⛔ KHONG doc duoc bang nao tu `schema.py`. Phep trich da hong "
            "— va mot ban ve 'rong ma xanh' la mot ban ve NOI DOI.")
    thieu = [b.name for b in bang if not b.tang]
    if thieu:
        raise SystemExit(
            f"⛔ {len(thieu)} bang ⛔ KHONG khai `tang`: {', '.join(thieu)}\n"
            "⇒ Them mot bang ma quen khai tang thi no se **vo hinh** tren ban "
            "do kien truc — va ⛔ khong ai thay no bien mat.")
    khai = {t for t, _, _ in TANG}
    la = sorted({b.tang for b in bang} - khai)
    if la:
        raise SystemExit(
            f"⛔ tang ⛔ khong khai trong `TANG`: {', '.join(la)}")

    d = ["flowchart TB"]
    for ma, ten, cau in TANG:
        trong = [b for b in bang if b.tang == ma]
        if not trong:
            continue
        d.append(f'  subgraph {ma.replace("-", "_")}["{ten} — {cau}"]')
        d.append("    direction LR")
        d += [_nut(b) for b in trong]
        d.append("  end")
    d.append("")
    for tu, den, cot in canh(bang):
        d.append(f"  {tu} -->|{cot}| {den}")
    d.append("")
    d.append("  classDef view stroke-dasharray: 5 3;")
    return "\n".join(d) + "\n"


# ═══════════════════════════ TRUC THU HAI — KHAU NGHIEP VU ═══════════════
def _kiem_khau(bang: list) -> None:
    """⛔ Moi bang phai khai `khau`, va `khau` phai nam trong ban khai."""
    thieu = [b.name for b in bang if not getattr(b, "khau", "")]
    if thieu:
        raise SystemExit(
            f"⛔ {len(thieu)} bang ⛔ KHONG khai `khau`: {', '.join(thieu)}\n"
            "⇒ Them mot bang ma quen khai khau thi owner ⛔ khong biet no "
            "phuc vu VIEC nao — va ⛔ khong ai thay no thieu.")
    khai = {m for m, _, _, _ in KHAU}
    la = sorted({b.khau for b in bang} - khai)
    if la:
        raise SystemExit(f"⛔ khau ⛔ khong khai trong `KHAU`: {', '.join(la)}")


def _sg(ma: str) -> str:
    return ma.replace("-", "_")


def sinh_khau() -> str:
    """Ban ve DONG CHAY: Ⓐ nap ⇒ Ⓑ ghep ⇒ Ⓒ sua, + hai lan cat ngang.

    ⛔⛔ **Mui ten o day la DONG CHAY NGHIEP VU, ⛔ KHONG phai khoa ngoai.**
    Khoa ngoai song o `ERD-CONTRACT.mmd` va o ban do TANG. Tron hai loai mui
    ten tren mot ban ve la cach chac chan nhat de nguoi doc tin mot quan he
    ⛔ khong ton tai.

    ⭐ **Vi sao ban ve nay ⛔ KHONG mang canh FK.** Ban do tang ve canh FK, va
    FK tro tu **con** len **cha** — nguoc chieu dong chay. Mermaid xep hang
    theo canh, nen ban do tang render ra **⑦ o goc tren, ① o duoi cung**:
    dung ve quan he, ⛔ nhung doc nguoc hoan toan voi cach owner hoi. O day chi
    co canh **cung mot chieu** ⇒ thu tu Ⓐ→Ⓑ→Ⓒ la **chac chan**, ⛔ khong phu
    thuoc bo xep hang.
    """
    bang = doc_bang()
    if not bang:
        raise SystemExit("⛔ ⛔ KHONG doc duoc bang nao — ban ve rong ma xanh "
                         "la ban ve NOI DOI.")
    _kiem_khau(bang)

    d = ["flowchart LR"]
    for ma, ten, _loai, cau in KHAU:
        trong = [b for b in bang if b.khau == ma]
        if not trong:
            continue
        d.append(f'  subgraph {_sg(ma)}["{ten} — {cau}"]')
        d.append("    direction TB")
        d += [_nut(b) for b in trong]
        d.append("  end")
    d.append("")
    for a, b in zip(_CHUOI, _CHUOI[1:]):
        d.append(f"  {_sg(a)} ==> {_sg(b)}")
    for m in _CHUOI:
        d.append(f"  {_sg(m)} -.-> {_sg('S-so')}")
    # ⚠ Chieu la `khau ⇢ VIEC`, ⛔ khong nguoc lai. Hai ly do, va ca hai deu
    #   that: ⓐ nghia — Ⓑ va Ⓒ **day viec vao** hang cho; ⓑ xep hang — mot
    #   canh `V ⇢ B` lam `V` xep **TRUOC** Ⓑ, tuc ban ve tu noi doi ve thu tu.
    for m in ("B-ghep", "C-sua"):
        d.append(f"  {_sg(m)} -.-> {_sg('V-viec')}")
    d.append("")
    d.append("  classDef view stroke-dasharray: 5 3;")
    return "\n".join(d) + "\n"


def bang_khau_md(bang: list) -> str:
    """Bang `thuc the -> khau`. MOI o deu suy tu ban khai, ⛔ khong go tay."""
    r = ["| Khâu | Thực thể | Kiểu | Tầng | Cột | Khoá chính |",
         "|---|---|:--:|---|--:|---|"]
    ten_tang = {m: t for m, t, _ in TANG}
    for ma, ten, _loai, _cau in KHAU:
        trong = [b for b in bang if b.khau == ma]
        for i, b in enumerate(trong):
            pk = [c.name for c in b.columns if c.pk] or list(b.pk_cols)
            r.append(
                f"| {'**' + ten + '**' if i == 0 else ''} "
                f"| `{b.name}` "
                f"| {'khung xem' if b.kind == 'view' else 'bảng'} "
                f"| {ten_tang.get(b.tang, b.tang)} "
                f"| {len(b.columns)} "
                f"| {'`' + ' + '.join(pk) + '`' if pk else '—'} |")
    return "\n".join(r) + "\n"


def tu_dien_ten_md() -> str:
    """Bang `ten dang luu hanh -> khau`. ⛔ Suy tu `TU_DIEN_TEN`, ⛔ khong go.

    ⛔⛔ **Vi sao bang nay ton tai.** Mot khau dang mang **ba bo ten** *(tai
    lieu · loi owner · ten tep AS-IS)* va ⛔ khong cho nao noi chung la MOT.
    Ten tep **CO** trong tai lieu *(`BA-05:39`+`:130`)* — cai thieu la **cau
    noi**, va thieu cau noi thi moi nguoi tu noi lay, moi nguoi mot kieu.
    """
    # ⛔⛔ Dau `|` TRAN trong o lam VO CA BANG, va mat thuong ⛔ khong thay —
    #   bang van trong nhu bang, chi la cac o **dich sang mot cot**. Lop loi
    #   nay da can that `8` dong o `06_ORCHESTRATOR_DASHBOARD` (`R | …`), va
    #   vua can lai **o chinh bang nay**, cung vi chuoi `R |`. ⇒ Thoat o CHO
    #   SINH, ⛔ khong doi noi dung cho vua phep do.
    def _o(v: object) -> str:
        return str(v).replace("|", r"\|").replace("\n", " ")

    ten_khau = {m: t for m, t, _, _ in KHAU}
    r = ["| Tên đang lưu hành | Xuất xứ | Khâu | |",
         "|---|---|---|---|"]
    for ten, xx, khaus, ghi in TU_DIEN_TEN:
        nhan = " + ".join(ten_khau.get(k, k) for k in khaus)
        r.append(f"| {_o(ten)} | {_o(xx)} | {_o(nhan)} | {_o(ghi)} |")
    return "\n".join(r) + "\n"


def tu_dien_thuc_the_md() -> str:
    """Bang `bang trong kho -> khai niem -> ten AS-IS`. ⛔ Suy tu ban khai.

    ⛔⛔ **Vi sao bang nay ton tai.** `TU_DIEN_TEN` bac cau cho **KHAU**, va no
    ⛔ **khong** bac cau cho **THUC THE**: cau *"`fls_itl` co dung ten cua
    Giao dich khong"* ⛔ khong mot cong nao tra loi duoc — phai doc tay. Va
    mot cau phai doc tay la mot cau **se duoc tra loi khac nhau** moi lan.
    """
    def _o(v: object) -> str:
        return str(v).replace("|", r"\|").replace("\n", " ")

    r = ["| Bảng trong kho | Khái niệm nghiệp vụ | Tên ở AS-IS | |",
         "|---|---|---|---|"]
    for b, kn, asis, ghi in TU_DIEN_THUC_THE:
        r.append(f"| `{_o(b)}` | {_o(kn)} | {_o(asis)} | {_o(ghi)} |")
    return "\n".join(r) + "\n"


def ma_tran_md(bang: list) -> str:
    """Ma tran `tang × khau` — chỗ HAI TRUC LECH nhau la cho dang nhin nhat."""
    ten_khau = [(m, t) for m, t, _, _ in KHAU]
    r = ["| Tầng \\ Khâu | " + " | ".join(t for _, t in ten_khau) + " | Σ |",
         "|---|" + ":--:|" * (len(ten_khau) + 1)]
    for ma, ten, _ in TANG:
        hang = [b for b in bang if b.tang == ma]
        if not hang:
            continue
        o = []
        for mk, _ in ten_khau:
            n = sum(1 for b in hang if b.khau == mk)
            o.append(str(n) if n else "·")
        r.append(f"| **{ten}** | " + " | ".join(o) + f" | **{len(hang)}** |")
    tong = []
    for mk, _ in ten_khau:
        tong.append(str(sum(1 for b in bang if b.khau == mk)))
    r.append("| **Σ** | " + " | ".join(f"**{x}**" for x in tong)
             + f" | **{len(bang)}** |")
    return "\n".join(r) + "\n"


_CSS = """
:root{--paper:#F7F8F5;--surface:#fff;--ink:#1B2420;--ink-2:#5A6661;
 --ink-3:#84908A;--rule:#D2DAD3;--accent:#0F5C4A;--accent-soft:#E1EDE7;
 --amber:#87680F;--amber-soft:#F5EEDA;--plate:#F1F4EE;--plate-rule:#C7D1C6}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]){
 --paper:#0F1412;--surface:#161C18;--ink:#E7EDE5;--ink-2:#AAB6AF;
 --ink-3:#77837C;--rule:#2A332C;--accent:#66C4A4;--accent-soft:#17271F;
 --amber:#D9B455;--amber-soft:#2A2213;--plate:#1B221D;--plate-rule:#2A332C}}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);
 font:400 15px/1.6 "Be Vietnam Pro",system-ui,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:38px 24px 80px}
h1{font:700 28px/1.22 Bitter,serif;margin:0 0 6px;letter-spacing:-.015em}
.lede{color:var(--ink-2);font:400 18.5px/1.5 Bitter,serif;margin:0 0 4px}
.meta{color:var(--ink-3);font:12.5px/1.5 "IBM Plex Mono",monospace}
code,.mono{font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:.9em}
.note{border:1px solid var(--rule);background:var(--surface);border-radius:7px;
 padding:11px 14px;margin:18px 0;font-size:13.5px}
.note.amb{border-color:var(--amber);background:var(--amber-soft)}
/* mot TANG = mot bang ngang */
.tang{display:grid;grid-template-columns:210px minmax(0,1fr);gap:0;
 border:1px solid var(--plate-rule);border-radius:10px;margin:0 0 14px;
 overflow:hidden;background:var(--plate)}
@media(max-width:820px){.tang{grid-template-columns:1fr}}
.tang>.dau{padding:13px 15px;background:var(--surface);
 border-right:1px solid var(--plate-rule)}
.tang>.dau b{font:600 14px/1.3 Bitter,serif;display:block;margin-bottom:3px}
.tang>.dau span{font-size:12px;color:var(--ink-2);line-height:1.45}
.tang>.than{padding:12px 14px;display:flex;flex-wrap:wrap;gap:8px;
 align-items:flex-start;align-content:flex-start}
.o{border:1px solid var(--plate-rule);background:var(--surface);
 border-radius:6px;padding:6px 10px;font:500 12px/1.4 "IBM Plex Mono",monospace}
.o.view{border-style:dashed;color:var(--ink-2)}
.o em{display:block;font:400 10.5px/1.3 "Be Vietnam Pro",sans-serif;
 color:var(--ink-3);font-style:normal}
.mui{text-align:center;color:var(--ink-3);font-size:18px;margin:-6px 0 8px}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:13.5px}
th,td{text-align:left;padding:7px 9px;border-bottom:1px solid var(--rule);
 vertical-align:top}
th{font:600 12.5px/1.4 "Be Vietnam Pro",sans-serif;color:var(--ink-2);
 background:var(--accent-soft)}
td.c{text-align:center}
.scroll{overflow-x:auto}
h2{font:600 21px/1.3 Bitter,serif;margin:44px 0 12px;padding-top:18px;
 border-top:1px solid var(--rule)}
h3{font:600 12.5px/1.4 "IBM Plex Mono",monospace;margin:26px 0 8px;
 text-transform:uppercase;letter-spacing:.08em;color:var(--accent)}
/* mot THUC THE = mot the */
.tt{border:1px solid var(--rule);border-radius:9px;background:var(--surface);
 margin:14px 0;overflow:hidden}
.tt>.dau{padding:10px 14px;background:var(--accent-soft);
 border-bottom:1px solid var(--rule);display:flex;gap:10px;
 align-items:baseline;flex-wrap:wrap}
.tt>.dau b{font:600 14px/1.3 "IBM Plex Mono",monospace;color:var(--accent)}
.tt>.dau .vt{font-size:12px;color:var(--ink-2)}
.tt table{margin:0;font-size:12.5px}
.tt th{background:transparent;border-bottom:1px solid var(--rule)}
.tt td{border-bottom:1px solid var(--rule);padding:6px 10px}
.tt tr:last-child td{border-bottom:0}
.k{display:inline-block;font:600 10px/1.5 "IBM Plex Mono",monospace;
 padding:0 5px;border-radius:3px;border:1px solid;margin-right:4px;
 white-space:nowrap}
.k.pk{color:#8A5A00;background:var(--amber-soft);border-color:var(--amber)}
.k.fk{color:var(--accent);background:var(--accent-soft);border-color:var(--accent)}
.k.u{color:var(--ink-2);border-color:var(--rule)}
.k.bb{color:var(--ink-2);border-color:var(--rule)}
.vs{color:var(--ink-2);font-size:12px;line-height:1.5}
.ty{font:500 11.5px/1.5 "IBM Plex Mono",monospace;color:var(--ink-3)}
/* ── mau cua BAN VE SVG ────────────────────────────────────────────── */
.ve{--nen:var(--paper);--vien:var(--plate-rule);--nhan:var(--ink);
 --phu:var(--ink-2);--o:var(--surface);--o-vien:var(--plate-rule);
 --o-dau:var(--accent-soft);--o-chu:var(--accent);--pk:#8A5A00;
 --fk:var(--accent);--ten:var(--ink-3);--tenx:#A32B23;
 --dai0:var(--plate);--dai1:transparent;
 margin:18px 0;overflow-x:auto}
@media(prefers-color-scheme:dark){:root:not([data-theme=light]) .ve{
 --pk:#D9B455;--tenx:#E9897C}}
.chu-giai{display:flex;gap:16px;flex-wrap:wrap;font-size:12px;
 color:var(--ink-2);margin:8px 0 0}
.chu-giai i{font-style:normal;font-family:"IBM Plex Mono",monospace;
 font-weight:600}
""".strip()


# ══ BAN VE SVG — tu chua, ⛔ khong CDN, ⛔ khong JS ══════════════════════
#
# ⛔⛔ **Vi sao SVG chu ⛔ khong mermaid o day.** Trang nay owner mo bang cach
#    **nhap doi mot tep** — mermaid can mot `<script>` tu CDN, nghia la mot
#    ban ve **chi doc duoc khi co mang**. Mot ban do kien truc ⛔ khong duoc
#    phu thuoc vao duong truyen.
#
# ⚠ Doi lai: bo tri nam o day, va no phai **tinh duoc**, ⛔ khong duoc la mot
#   mo hinh vat ly ngau nhien — hai lan sinh phai ra **hai tep giong het**,
#   neu khong thi cong `--kiem` se bao lech mot cach vo nghia.
_RONG = 1320           # be ngang khung ve
_LE_NHAN = 158         # dai nhan tang ben trai
_CAO_DONG = 15         # mot dong khoa trong o
_CAO_DAU = 25          # phan dau o (ten thuc the)
_DEM_O = 26            # khoang giua hai o cung hang
_DEM_TANG = 40         # khoang giua hai tang


def _khoa_cua_o(b) -> list[tuple[str, str]]:
    """Cac dong hien TRONG o — chi cot KHOA. ⛔ Khong do ca 182 cot ra hinh."""
    ra = []
    pkc = set(getattr(b, "pk_cols", ()))
    for c in b.columns:
        if c.pk or c.name in pkc:
            ra.append(("PK", c.name))
        elif c.fk:
            ra.append(("FK", c.name))
    return ra


def _do_o(b) -> tuple[float, float, list]:
    k = _khoa_cua_o(b)
    dai = max([len(b.name)] + [len(t) + len(n) + 2 for t, n in k])
    return max(148.0, dai * 7.1 + 26), _CAO_DAU + len(k) * _CAO_DONG + 7, k


def _bo_tri(bang: list) -> tuple[dict, list, float]:
    """`{ten: (x, y, w, h, khoa)}` · dai tang · chieu cao khung.

    ⛔ Thuan tat dinh: cung mot ban khai ⇒ cung mot toa do.
    """
    o, bang_tang, y = {}, [], 58.0
    rong_noi = _RONG - _LE_NHAN - 34
    for ma, ten, cau in TANG:
        trong = [b for b in bang if b.tang == ma]
        if not trong:
            continue
        kt = [(b, *_do_o(b)) for b in trong]
        # ⭐⭐ XUONG HANG khi mot tang khong con vua BE NGANG khung.
        #
        # ⛔⛔ Ban dau ham nay xep ca tang tren MOT hang, va cong hinh hoc
        #    `test_HINH_HOC_khong_TRAN_khung` bat no ngay lan them thuc the
        #    thu 25 (`fls_dien_giai`, `QĐ-ITL-145`) — `fls_source` tran khung
        #    phai. ⇒ Mot ban ve **chi dung cho den lan them tiep theo** thi
        #    cong ay la mot day vap, ⛔ khong phai mot phep do.
        # ⇒ Sua GOC: chia thanh cac hang vua khung, moi hang tu can giua.
        hang: list[list] = [[]]
        rong_hang = 0.0
        for k in kt:
            them = k[1] + (_DEM_O if hang[-1] else 0)
            if hang[-1] and rong_hang + them > rong_noi:
                hang.append([k])
                rong_hang = k[1]
            else:
                hang[-1].append(k)
                rong_hang += them
        cao_tang = 0.0
        for h_i, hg in enumerate(hang):
            tong = sum(k[1] for k in hg) + _DEM_O * (len(hg) - 1)
            x = _LE_NHAN + 17 + max(0.0, (rong_noi - tong) / 2)
            cao = max(k[2] for k in hg)
            for b, w, h, khoa in hg:
                o[b.name] = (x, y + cao_tang + (cao - h) / 2, w, h, khoa)
                x += w + _DEM_O
            cao_tang += cao + (_DEM_O if h_i < len(hang) - 1 else 0)
        bang_tang.append((ma, ten, cau, y - 13, cao_tang + 26))
        y += cao_tang + _DEM_TANG
    return o, bang_tang, y - _DEM_TANG + 24


def _cat_bien(x1, y1, x2, y2, w, h) -> tuple[float, float]:
    """Diem cat cua doan (tam→tam) voi bien mot o. Giu mui ten **cham vien**,
    ⛔ khong dam vao giua chu."""
    dx, dy = x2 - x1, y2 - y1
    if dx == 0 and dy == 0:
        return x1, y1
    tx = abs(w / 2 / dx) if dx else float("inf")
    ty = abs(h / 2 / dy) if dy else float("inf")
    t = min(tx, ty)
    return x1 + dx * t, y1 + dy * t


def sinh_svg(bang: list) -> str:
    from html import escape
    o, bang_tang, cao = _bo_tri(bang)
    tang_cua = {b.name: b.tang for b in bang}
    thu = {ma: i for i, (ma, _, _) in enumerate(TANG)}
    la_view = {b.name: getattr(b, "kind", "table") == "view" for b in bang}

    d = [f'<svg viewBox="0 0 {_RONG} {cao:.0f}" width="100%" '
         f'style="max-width:{_RONG}px" xmlns="http://www.w3.org/2000/svg" '
         f'font-family="ui-monospace,\'IBM Plex Mono\',monospace" '
         f'role="img" aria-label="Bản đồ kiến trúc kho FLS theo 7 tầng">',
         '<defs>',
         '<marker id="mt" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7"'
         ' markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0 0 L8 4 L0 8 z" fill="var(--ten)"/></marker>',
         '<marker id="mtx" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7"'
         ' markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0 0 L8 4 L0 8 z" fill="var(--tenx)"/></marker>',
         '</defs>']

    # ── dai tang ──────────────────────────────────────────────────────
    for i, (ma, ten, cau, y, h) in enumerate(bang_tang):
        d.append(f'<rect x="10" y="{y:.0f}" width="{_RONG - 20}" '
                 f'height="{h:.0f}" rx="10" fill="var(--dai{i % 2})" '
                 f'stroke="var(--vien)"/>')
        d.append(f'<text x="26" y="{y + 25:.0f}" font-size="13" '
                 f'font-weight="700" fill="var(--nhan)">{escape(ten)}</text>')
        for j, ph in enumerate(_ngat(cau, 21)):
            d.append(f'<text x="26" y="{y + 42 + j * 13:.0f}" font-size="10" '
                     f'fill="var(--phu)">{escape(ph)}</text>')

    # ── canh: ve TRUOC o de ⛔ khong de len chu ────────────────────────
    for tu, den, cot in canh(bang):
        if tu == den:                                   # tu tham chieu
            x, y, w, h, _ = o[tu]
            d.append(f'<path d="M{x + w:.0f} {y + 12:.0f} '
                     f'c 26 -13 26 26 0 13" fill="none" stroke="var(--tenx)" '
                     f'stroke-width="1.6" marker-end="url(#mtx)"/>')
            d.append(f'<text x="{x + w + 31:.0f}" y="{y + 22:.0f}" '
                     f'font-size="9.5" fill="var(--tenx)">{escape(cot)}</text>')
            continue
        x1, y1, w1, h1, _ = o[tu]
        x2, y2, w2, h2, _ = o[den]
        c1 = (x1 + w1 / 2, y1 + h1 / 2)
        c2 = (x2 + w2 / 2, y2 + h2 / 2)
        a = _cat_bien(*c1, *c2, w1, h1)
        b2 = _cat_bien(*c2, *c1, w2, h2)
        # vong nhe theo phuong vuong goc ⇒ hai canh song song ⛔ khong chong
        mx, my = (a[0] + b2[0]) / 2, (a[1] + b2[1]) / 2
        dx, dy = b2[0] - a[0], b2[1] - a[1]
        n = (dx * dx + dy * dy) ** 0.5 or 1
        k = min(34.0, n * 0.16)
        cx, cy = mx - dy / n * k, my + dx / n * k
        xuong = thu[tang_cua[den]] > thu[tang_cua[tu]]
        mau = "--tenx" if xuong else "--ten"
        d.append(f'<path d="M{a[0]:.0f} {a[1]:.0f} Q{cx:.0f} {cy:.0f} '
                 f'{b2[0]:.0f} {b2[1]:.0f}" fill="none" stroke="var({mau})" '
                 f'stroke-width="1.5" opacity=".8" '
                 f'marker-end="url(#{"mtx" if xuong else "mt"})"/>')
        d.append(f'<text x="{cx:.0f}" y="{cy - 4:.0f}" font-size="9.5" '
                 f'text-anchor="middle" fill="var({mau})" '
                 f'style="paint-order:stroke;stroke:var(--nen);'
                 f'stroke-width:3px">{escape(cot)}</text>')

    # ── o thuc the ────────────────────────────────────────────────────
    for b in bang:
        if b.name not in o:
            continue
        x, y, w, h, khoa = o[b.name]
        v = la_view[b.name]
        d.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" '
                 f'height="{h:.0f}" rx="7" fill="var(--o)" '
                 f'stroke="var(--o-vien)" stroke-width="1.3"'
                 + (' stroke-dasharray="5 3"' if v else '') + '/>')
        d.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" '
                 f'height="{_CAO_DAU}" rx="7" fill="var(--o-dau)"/>')
        d.append(f'<rect x="{x:.0f}" y="{y + _CAO_DAU - 7:.0f}" '
                 f'width="{w:.0f}" height="7" fill="var(--o-dau)"/>')
        d.append(f'<text x="{x + 10:.0f}" y="{y + 17:.0f}" font-size="11.5" '
                 f'font-weight="600" fill="var(--o-chu)">{escape(b.name)}'
                 + ('  ◇' if v else '') + '</text>')
        for i, (loai, ten) in enumerate(khoa):
            yy = y + _CAO_DAU + 11 + i * _CAO_DONG
            d.append(f'<text x="{x + 10:.0f}" y="{yy:.0f}" font-size="9.5" '
                     f'fill="var(--{"pk" if loai == "PK" else "fk"})">'
                     f'{loai}</text>')
            d.append(f'<text x="{x + 30:.0f}" y="{yy:.0f}" font-size="9.5" '
                     f'fill="var(--phu)">{escape(ten)}</text>')
    d.append('</svg>')
    return "\n".join(d)


def _ngat(s: str, n: int) -> list[str]:
    """Ngat dong theo TU, ⛔ khong cat giua tu."""
    ra, d = [], ""
    for t in s.split():
        if len(d) + len(t) + 1 > n and d:
            ra.append(d)
            d = t
        else:
            d = (d + " " + t).strip()
    if d:
        ra.append(d)
    return ra[:4]


def _khoa(b, c) -> str:
    """Nhan khoa cua mot cot — doc tu ban khai, ⛔ khong suy dien."""
    from html import escape
    ra = []
    if c.pk or c.name in getattr(b, "pk_cols", ()):
        ra.append('<span class="k pk">PK</span>')
    if c.fk:
        ra.append(f'<span class="k fk">FK → {escape(c.fk)}</span>')
    if c.unique or any(c.name in k and len(k) == 1
                       for k in getattr(b, "unique_keys", ())):
        ra.append('<span class="k u">DUY NHẤT</span>')
    if not c.null:
        ra.append('<span class="k bb">bắt buộc</span>')
    if c.generated:
        ra.append('<span class="k u">máy tính</span>')
    if c.check:
        ra.append('<span class="k u">CHECK</span>')
    return "".join(ra) or '<span class="ty">—</span>'


def _the_thuc_the(b) -> str:
    """Mot thuc the: khoa, tung cot, va **vi sao** cua cot ay."""
    from html import escape
    la_view = getattr(b, "kind", "table") == "view"
    ra = [f'<div class="tt"><div class="dau"><b>{escape(b.name)}</b>',
          f'<span class="vt">{escape(b.erd_entity or "—")}</span>',
          f'<span class="vt">{len(b.columns)} cột</span>',
          # ⭐ Hai truc doc duoc **ngay tren the** — de nguoi doc ⛔ khong phai
          #   cuon nguoc len hai ban ve de biet mot thuc the dung o dau.
          f'<span class="vt">khâu '
          f'{escape(dict((m, t) for m, t, _, _ in KHAU).get(b.khau, b.khau))}'
          f'</span>']
    if la_view:
        ra.append('<span class="k u">KHUNG XEM — ⛔ không lưu gì</span>')
    # ⚠ `pk_cols` MOT cot ⛔ khong phai "khoa ghep" — `fls_pm_link` khai
    #   `('link_id',)` chi de dung duong khai o muc BANG. Goi no la ghep la
    #   noi sai ve kho.
    pkc = getattr(b, "pk_cols", ())
    if len(pkc) > 1:
        ra.append('<span class="k pk">PK GHÉP ('
                  + escape(" + ".join(pkc)) + ')</span>')
    elif len(pkc) == 1:
        ra.append(f'<span class="k pk">PK ({escape(pkc[0])})</span>')
    for k in getattr(b, "unique_keys", ()):
        ra.append('<span class="k u">DUY NHẤT ('
                  + escape(" + ".join(k)) + ')</span>')
    if getattr(b, "island_reason", ""):
        ra.append(f'<span class="vt">⛔ ⛔ không có FK về <code>fls_itl</code>: '
                  f'{escape(b.island_reason)}</span>')
    ra.append('</div><div class="scroll"><table>')
    ra.append('<tr><th style="width:21%">Cột</th><th style="width:12%">Kiểu</th>'
              '<th style="width:26%">Khoá · ràng buộc</th>'
              '<th>Vì sao nó tồn tại</th></tr>')
    for c in b.columns:
        ra.append(f'<tr><td class="mono">{escape(c.name)}</td>'
                  f'<td class="ty">{escape(c.type)}</td>'
                  f'<td>{_khoa(b, c)}</td>'
                  f'<td class="vs">{escape(c.comment) if c.comment else "—"}</td></tr>')
    ra.append('</table></div></div>')
    return "\n".join(ra)


_KM = 24               # le
_KW = 385              # be ngang mot lan khau trong chuoi
_KG = 58               # khe giua hai lan — cho mui ten `⇒`
_KCH = 24              # cao mot chip thuc the
_KHD = 38              # cao phan dau mot dai


def _chip(x: float, y: float, b) -> tuple[str, float]:
    """Mot chip thuc the. Tra `(svg, be ngang)`."""
    w = len(b.name) * 7.0 + 18
    la_view = b.kind == "view"
    nen, vien = ("#FFFFFF", "#9AA6A1") if la_view else ("#EEF2EF", "#5A6661")
    nhac = ' stroke-dasharray="4 3"' if la_view else ""
    return (
        f'<g><rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{_KCH}" '
        f'rx="5" fill="{nen}" stroke="{vien}"{nhac}/>'
        f'<text x="{x + w / 2:.0f}" y="{y + 16:.0f}" text-anchor="middle" '
        f'font-family="IBM Plex Mono,monospace" font-size="11" fill="#1B2420">'
        f'{b.name}</text></g>', w)


def _dai(x, y, w, h, ma, ten, cau, bang, doc: bool) -> str:
    """Mot DAI khau. `doc=True` xep chip theo cot, `False` theo hang."""
    from html import escape
    trong = [b for b in bang if b.khau == ma]
    o = [f'<rect x="{x:.0f}" y="{y:.0f}" width="{w:.0f}" height="{h:.0f}" '
         f'rx="10" fill="#F7F8F5" stroke="#C7D0CB"/>',
         f'<text x="{x + 14:.0f}" y="{y + 22:.0f}" font-family="Bitter,serif" '
         f'font-size="13" font-weight="700" fill="#1B2420">{escape(ten)}</text>',
         f'<text x="{x + 14:.0f}" y="{y + 34:.0f}" font-family="Be Vietnam Pro,'
         f'sans-serif" font-size="9.5" fill="#5A6661">{escape(cau)}</text>']
    if doc:
        for i, b in enumerate(trong):
            o.append(_chip(x + 14, y + _KHD + i * 32, b)[0])
    else:
        cx = x + 14
        for b in trong:
            s, bw = _chip(cx, y + _KHD, b)
            o.append(s)
            cx += bw + 12
    return "".join(o)


def sinh_svg_khau(bang: list) -> str:
    """Ban ve DONG CHAY — ⛔ KHONG mot canh noi nao.

    ⛔⛔ **Vi sao ⛔ khong ve mui ten tu `V`/`S` len ba lan kia.** Y nghia can
    noi la *"cat ngang"* va *"ca ba deu cham"* — do la mot phat bieu ve
    **PHAM VI**, ⛔ khong phai ve mot duong di. Ve no bang **be rong cua dai**
    thi no ⛔ khong the render sai; ve bang mui ten thi no vua roi vao dung
    cai bay da lam ban do tang doc nguoc.
    """
    from html import escape
    _kiem_khau(bang)
    n_max = max(sum(1 for b in bang if b.khau == m) for m in _CHUOI)
    h1 = _KHD + n_max * 32 + 10
    y1 = 64
    xs = {m: _KM + i * (_KW + _KG) for i, m in enumerate(_CHUOI)}
    phai = _KM + 3 * _KW + 2 * _KG          # bien phai cua chuoi
    y2 = y1 + h1 + 34
    h_ngang = _KHD + _KCH + 14
    y3 = y2 + h_ngang + 22
    y4 = y3 + h_ngang + 22
    cao = y4 + h_ngang + 26
    ten = {m: (t, c, loai) for m, t, loai, c in KHAU}

    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_RONG} '
         f'{cao:.0f}" width="100%" role="img" aria-label="Bản đồ ba khâu '
         f'nghiệp vụ theo dòng chảy">',
         '<defs><marker id="mk" viewBox="0 0 10 10" refX="9" refY="5" '
         'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
         '<path d="M0,1 L9,5 L0,9 z" fill="#A34E1E"/></marker></defs>',
         f'<rect width="{_RONG}" height="{cao:.0f}" fill="#FFFFFF"/>',
         f'<text x="{_KM}" y="30" font-family="Bitter,serif" font-size="15" '
         f'font-weight="700" fill="#1B2420">DÒNG CHẢY CHÍNH — '
         f'nạp data ⇒ ghép lệnh chi ⇒ adjust ITL</text>',
         f'<text x="{_KM}" y="48" font-family="Be Vietnam Pro,sans-serif" '
         f'font-size="10.5" fill="#5A6661">Bề rộng dải = phạm vi. '
         f'Hai dải dưới KHÔNG nằm trong chuỗi — chúng cắt ngang.</text>']
    for m in _CHUOI:
        t, c, _ = ten[m]
        o.append(_dai(xs[m], y1, _KW, h1, m, t, c, bang, True))
    for a, b in zip(_CHUOI, _CHUOI[1:]):
        x0 = xs[a] + _KW + 10
        x1 = xs[b] - 10
        ym = y1 + h1 / 2
        o.append(f'<line x1="{x0:.0f}" y1="{ym:.0f}" x2="{x1:.0f}" '
                 f'y2="{ym:.0f}" stroke="#A34E1E" stroke-width="3" '
                 f'marker-end="url(#mk)"/>')
    # ⭐ `V` chi trai DUOI Ⓑ va Ⓒ — be rong LA phat bieu "cat ngang hai khau".
    xv = xs["B-ghep"]
    t, c, _ = ten["V-viec"]
    o.append(_dai(xv, y2, phai - xv, h_ngang, "V-viec", t,
                  c + " · dải chỉ trải dưới Ⓑ và Ⓒ", bang, False))
    t, c, _ = ten["S-so"]
    o.append(_dai(_KM, y3, phai - _KM, h_ngang, "S-so", t,
                  c + " · dải trải dưới CẢ BA khâu", bang, False))
    t, c, _ = ten["H-ha-tang"]
    o.append(_dai(_KM, y4, 300, h_ngang, "H-ha-tang", t, c, bang, False))
    o.append(f'<text x="{_KM + 320}" y="{y4 + 26:.0f}" font-family="Be Vietnam '
             f'Pro,sans-serif" font-size="10.5" fill="#5A6661">'
             f'{escape("⛔ Không nằm trong chuỗi nghiệp vụ — và đó là đúng.")}'
             f'</text>')
    o.append("</svg>")
    return "".join(o)


def sinh_html(bang: list) -> str:
    """Trang HTML — sinh tu **cung ban khai**, ⛔ khong phai mot ban ve tay."""
    from html import escape
    cn = canh(bang)
    ra = [
        '<!doctype html>', '<html lang="vi">', '<head>',
        '<meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        '<title>Bản đồ kiến trúc — 7 tầng · 3 khâu</title>',
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        'family=Bitter:wght@600;700&family=Be+Vietnam+Pro:wght@400;500;600'
        '&family=IBM+Plex+Mono:wght@400;500&display=swap">',
        f'<style>{_CSS}</style>', '</head><body><div class="wrap">',
        '<h1>Bản đồ kiến trúc kho <span class="mono">FLS</span> — 7 tầng</h1>',
        '<p class="lede">Mỗi tầng trả lời <strong>một câu</strong>. '
        'Mũi tên là <strong>khoá ngoại thật</strong>, đọc từ bản khai.</p>',
        f'<p class="meta">Trang này do <code>tools/sinh_ban_do_tang.py</code> '
        f'SINH RA từ <code>fls/db/schema.py</code> — ⛔ đừng sửa tay. '
        f'{len(bang)} bảng · {len(cn)} khoá ngoại.</p>',
        '<div class="note amb">⛔⛔ <strong>Vì sao trang này được SINH chứ '
        '⛔ không vẽ tay.</strong> Một bản đồ vẽ tay ⛔ không có cổng nào canh, '
        'và nó sẽ già <strong>im lặng</strong>. Ở đây <code>tầng</code> là '
        '<strong>một trường của bản khai</strong>; thêm một bảng mà quên khai '
        'tầng thì cổng <code>--kiem</code> <strong>NO</strong>.<br>⚠ '
        '<code>tầng</code> ⛔ <strong>không</strong> đổi một dòng <code>DDL</code> '
        'nào — hai bảng cùng tầng ⛔ không có gì chung ở PostgreSQL; chúng chung '
        '<strong>câu hỏi mà chúng trả lời</strong>.</div>',
    ]
    # ── ⭐ BAN VE: o thuc the + khoa + mui ten THAT ───────────────────
    ra += ['<div class="ve">', sinh_svg(bang), '</div>',
           '<div class="chu-giai">'
           '<span><i style="color:#8A5A00">PK</i> khoá chính</span>'
           '<span><i style="color:var(--accent)">FK</i> khoá ngoại</span>'
           '<span><i>◇</i> khung xem — ⛔ không lưu gì</span>'
           '<span><i style="color:var(--ink-3)">→</i> trỏ LÊN tầng trên '
           '<em>(hay cùng tầng)</em></span>'
           '<span><i style="color:#A32B23">→</i> trỏ XUỐNG · tự tham chiếu</span>'
           '</div>',
           '<div class="note">⭐ <strong>Hai mũi tên ĐỎ là hai chỗ đáng nhìn '
           'nhất của cả bản đồ:</strong>'
           '<br>ⓐ <code>fls_adjustment.reversal_of → fls_adjustment</code> — '
           'một bút toán <strong>ĐẢO</strong> trỏ về bút toán nó đảo. Đó là cơ chế '
           'thay cho <code>DELETE</code>: <code>INV-I08</code> nói sổ <strong>chỉ '
           'THÊM</strong>, nên «xoá» trong TO-BE là «thêm một dòng trỏ ngược lại».'
           '<br>ⓑ <code>fls_pm_unlink.evt_id → fls_queue_event</code> — mũi tên '
           '<strong>duy nhất đi XUỐNG</strong>. <em>Ai bỏ ghép và vì sao</em> sống ở '
           'tầng <strong>VIỆC</strong>, ⛔ <strong>không</strong> nhân bản sang tầng ghép '
           '— <strong>một chỗ, ⛔ không hai</strong>.</div>']

    # ── ⭐⭐ TRUC THU HAI: KHAU NGHIEP VU (17/09) ──────────────────────
    dem_k = {m: sum(1 for b in bang if b.khau == m) for m, _, _, _ in KHAU}
    ra += ['<h2>Trục thứ hai — <strong>ba khâu nghiệp vụ</strong></h2>',
           '<p class="lede">Bản đồ trên trả lời <em>«nó nằm ở đâu trên đường đi '
           'của <strong>dữ liệu</strong>»</em>. Bản đồ dưới trả lời một câu '
           'khác: <em>«nó phục vụ <strong>việc</strong> nào của người»</em>.</p>',
           '<div class="note amb">⛔⛔ <strong><code>khâu</code> ⛔ KHÔNG phải '
           '<code>tầng</code> đổi tên.</strong> Hai trục <strong>giao nhau chứ '
           '⛔ không lồng nhau</strong> — và chỗ chúng <strong>lệch</strong> là '
           'chỗ đáng nhìn nhất.<br>⭐ <strong>Luật gán: theo VIỆC NÓ PHỤC VỤ, '
           '⛔ không theo ai ghi nó.</strong> Thiếu luật ấy thì '
           '<code>fls_queue_event</code> rơi vào khâu Ⓐ <em>(máy ghi 108.128 sự '
           'kiện lúc nạp)</em> trong khi nó là <strong>bảng việc của NGƯỜI</strong>.'
           '<br>⛔ Tên ba khâu <strong>lấy lại</strong> từ <code>ORC-09</code> '
           '<em>(mốc <code>A</code> · tác vụ ① · tác vụ ②)</em> — ⛔ không đặt '
           'tên thứ tư cho một thứ đã có tên.</div>',
           '<div class="ve">', sinh_svg_khau(bang), '</div>',
           '<div class="chu-giai">'
           + "".join(f'<span><i>{escape(t)}</i> {dem_k[m]} thực thể</span>'
                     for m, t, _, _ in KHAU)
           + '</div>',
           '<div class="note">⭐⭐ <strong>Ba chỗ hai trục ⛔ không trùng — đọc '
           'ba dòng này là hiểu cả bản đồ:</strong>'
           '<br>ⓐ <code>fls_pm_line</code> — tầng <strong>④ GHÉP</strong>, khâu '
           '<strong>Ⓑ</strong>, ⛔ <strong>nhưng khâu Ⓐ là thứ GHI nó</strong>. '
           'Sửa đường nạp mà quên rằng người hưởng là màn ghép là cách làm hỏng '
           'Ⓑ <em>từ</em> Ⓐ.'
           '<br>ⓑ <code>fls_queue_event</code> — một bảng phục vụ <strong>hai '
           'việc</strong> ⇒ mọi phép đếm phải nói rõ <strong>đang đếm việc nào</strong>. '
           'Đây đúng là <code>GAP-ERD-30</code> nhìn từ trục khâu.'
           '<br>ⓒ <code>fls_itl</code> — <strong>trục chung</strong>, ⛔ không '
           'thuộc riêng khâu nào. Gán nó vào Ⓐ <em>(vì Ⓐ ghi)</em> hay Ⓒ '
           '<em>(vì Ⓒ sửa)</em> đều làm mất một nửa sự thật.</div>',
           '<h2>Tóm tắt theo tầng</h2>']
    dau = True
    for ma, ten, cau in TANG:
        trong = [b for b in bang if b.tang == ma]
        if not trong:
            continue
        if not dau:
            ra.append('<div class="mui">↓</div>')
        dau = False
        ra.append('<div class="tang"><div class="dau">'
                  f'<b>{escape(ten)}</b><span>{escape(cau)}</span></div>'
                  '<div class="than">')
        for b in trong:
            v = getattr(b, "kind", "table") == "view"
            ra.append(f'<div class="o{" view" if v else ""}">'
                      f'{escape(b.name)}'
                      + ('<em>khung xem</em>' if v else
                         f'<em>{len(b.columns)} cột</em>') + '</div>')
        ra.append('</div></div>')

    tang_cua = {b.name: b.tang for b in bang}
    ten_tang = {ma: ten for ma, ten, _ in TANG}
    ra += ['<h2 style="font:600 20px/1.3 Bitter,serif;margin:34px 0 10px">'
           'Mũi tên — khoá ngoại thật</h2>', '<div class="scroll"><table>',
           '<tr><th>Từ</th><th>Cột</th><th>Tới</th>'
           '<th class="c">Vượt tầng</th></tr>']
    for tu, den, cot in cn:
        vt = tang_cua[tu] != tang_cua[den]
        nhan = (f'{ten_tang[tang_cua[tu]].split(" ")[0]} → '
                f'{ten_tang[tang_cua[den]].split(" ")[0]}' if vt else '—')
        ra.append(f'<tr><td class="mono">{escape(tu)}</td>'
                  f'<td class="mono">{escape(cot)}</td>'
                  f'<td class="mono">{escape(den)}</td>'
                  f'<td class="c">{nhan}</td></tr>')
    ra += ['</table></div>']

    # ── QUAN HE — doc theo CAU, ⛔ khong theo ky hieu ──────────────────
    ra += ['<h2>Quan hệ giữa các thực thể — đọc thành câu</h2>',
           '<p class="vs">⛔ Bảng dưới đọc <strong>ngược chiều mũi tên</strong>: một dòng '
           'ở bảng <em>bên phải</em> có <strong>nhiều</strong> dòng ở bảng <em>bên trái</em>. '
           'Cột <strong>Bắt buộc</strong> nói khoá ấy có được để rỗng ⛔ không — và một khoá '
           '<strong>được phép rỗng</strong> là một quan hệ <strong>có thể ⛔ không tồn tại</strong>.</p>',
           '<div class="scroll"><table>',
           '<tr><th style="width:44%">Câu</th><th style="width:16%">Qua cột</th>'
           '<th class="c" style="width:12%">Bắt buộc</th>'
           '<th class="c">Vượt tầng</th></tr>']
    cot_cua = {(b.name, c.name): c for b in bang for c in b.columns}
    for tu, den, cot in cn:
        c = cot_cua[(tu, cot)]
        vt = tang_cua[tu] != tang_cua[den]
        nhan = (f'{ten_tang[tang_cua[tu]].split(" ")[0]} → '
                f'{ten_tang[tang_cua[den]].split(" ")[0]}' if vt else '—')
        cau = (f'⭐ một <code>{escape(tu)}</code> trỏ về <strong>một '
               f'<code>{escape(tu)}</code> KHÁC</strong> — <em>tự tham chiếu</em>'
               if tu == den else
               f'một <code>{escape(den)}</code> có <strong>nhiều</strong> '
               f'<code>{escape(tu)}</code>')
        ra.append(
            f'<tr><td>{cau}</td>'
            f'<td class="mono">{escape(cot)}</td>'
            f'<td class="c">{"có" if not c.null else "⛔ không"}</td>'
            f'<td class="c">{nhan}</td></tr>')
    ra.append('</table></div>')

    # ── CHI TIET TUNG THUC THE, nhom theo tang ────────────────────────
    ra += ['<h2>Chi tiết từng thực thể — khoá, cột, và <em>vì sao</em></h2>',
           '<p class="vs">⭐ Cột <strong>«Vì sao nó tồn tại»</strong> là phần đắt nhất: nó '
           'lấy thẳng <code>comment</code> của bản khai, nơi mỗi cột nói ra <strong>bất biến '
           'nào</strong> hay <strong>sự cố nào</strong> đã sinh ra nó. '
           f'<strong>{sum(1 for b in bang for c in b.columns if c.comment)}'
           f'/{sum(len(b.columns) for b in bang)}</strong> cột có câu ấy.</p>']
    for ma, ten, cau in TANG:
        trong = [b for b in bang if b.tang == ma]
        if not trong:
            continue
        ra.append(f'<h3>{escape(ten)} — {escape(cau)}</h3>')
        ra += [_the_thuc_the(b) for b in trong]

    ra += ['</div></body></html>', '']
    return "\n".join(ra)


def bom(ve: str) -> bool:
    """Thay khoi `flowchart` trong BA-05. ⛔ Khong tim thay ⇒ NO TO."""
    txt = DOC.read_text(encoding="utf-8")
    moi = "```mermaid\n" + ve.rstrip("\n") + "\n```"
    if not KHOI.search(txt):
        raise SystemExit(
            f"⛔ ⛔ KHONG tim thay khoi 'mermaid + flowchart' trong {DOC.name}. "
            "⛔ Tu them am tham la dung cai `INV-I16` cam.")
    # ⛔⛔ Hai khoi cung la `flowchart`. `count=1` an cai DAU TIEN, nen phai
    #   chung minh cai dau tien **⛔ khong phai** khoi KHAU — ⛔ khong gia dinh.
    m = KHOI.search(txt)
    i_khau = txt.find(MOC_DAU)
    if i_khau != -1 and m.start() > i_khau:
        raise SystemExit(
            "⛔ ⛔ Khoi `flowchart` dau tien nam TRONG vung KHAU ⇒ phep thay "
            "khoi TANG se ghi de nham. Ban ve tang phai dung TRUOC moc "
            f"`{MOC_DAU}` trong {DOC.name}.")
    ra = KHOI.sub(lambda _: moi, txt, count=1)
    if ra == txt:
        return False
    DOC.write_text(ra, encoding="utf-8", newline="\n")
    return True


def khoi_khau_md(bang: list, ve: str) -> str:
    """Ca khoi KHAU trong `BA-05` — van xuoi + ban ve + hai bang, SINH RA het."""
    return "\n".join([
        MOC_DAU,
        "## ⭐⭐⭐ BẢN ĐỒ NGHIỆP VỤ — **ba khâu theo dòng chảy**",
        "",
        "> **Câu bản đồ này trả lời:** *«mỗi thực thể phục vụ VIỆC nào, và ba "
        "việc ấy nối nhau theo thứ tự nào»* — owner hỏi `17/09`.",
        "",
        "⛔⛔ **`khâu` ⛔ KHÔNG phải `tầng` đổi tên.** Hai trục trả lời hai câu "
        "khác nhau, và chúng **giao nhau chứ ⛔ không lồng nhau**:",
        "",
        "| Trục | Câu nó trả lời | Bản vẽ |",
        "|---|---|---|",
        "| `tầng` | *«nó nằm ở đâu trên đường đi của **DỮ LIỆU**»* | bản đồ "
        "**bảy tầng** ở trên |",
        "| `khâu` | *«nó phục vụ **VIỆC** nào của người»* | bản đồ này |",
        "",
        "⭐ **Luật gán khâu: theo VIỆC NÓ PHỤC VỤ, ⛔ không theo ai ghi nó.** "
        "Thiếu luật ấy thì phép gán thành cảm tính — `fls_queue_event` sẽ rơi "
        "vào khâu Ⓐ *(máy ghi `108.128` sự kiện **lúc nạp**)* trong khi nó là "
        "**bảng việc của NGƯỜI**.",
        "",
        "⛔ Tên ba khâu **lấy lại từ bộ tài liệu**, ⛔ không đặt tên mới: mốc "
        "`A` *(đường LẤY dữ liệu)* · tác vụ ① *(mapping `PM ↔ Transaction`)* · "
        "tác vụ ② *(adjust thông tin ITL)* — "
        "[`ORC-09`](../01_Orchestrator/09_MILESTONES_HAI_TAC_VU.md). Đặt tên "
        "thứ tư cho một thứ đã có tên là cách đẻ ra `QĐ-ITL-02` lần nữa.",
        "",
        "⛔⛔ **Mũi tên trên bản vẽ này là DÒNG CHẢY NGHIỆP VỤ, ⛔ KHÔNG phải "
        "khoá ngoại.** Khoá ngoại sống ở `ERD-CONTRACT.mmd` và ở bản đồ tầng. "
        "⭐ Và đó cũng là lý do bản vẽ này **đọc đúng thứ tự** còn bản đồ tầng "
        "thì ⛔ không: `FK` trỏ từ **con** lên **cha** — **ngược chiều dòng "
        "chảy** — nên bộ xếp hàng đẩy `⑦` lên góc trên và `①` xuống đáy. Ở đây "
        "mọi cạnh **cùng một chiều** ⇒ thứ tự `Ⓐ→Ⓑ→Ⓒ` là **chắc chắn**.",
        "",
        "```mermaid",
        ve.rstrip("\n"),
        "```",
        "",
        "*(khối trên do máy sinh — ⛔ đừng sửa tay)*",
        "",
        "### ⭐⭐⭐ TỪ ĐIỂN TÊN — một khâu, **ba bộ tên**",
        "",
        "> ⭐ **Tên CHUẨN là tên TÁC VỤ** *(owner chốt `17/09`)*; hai bộ kia "
        "là **bí danh**. ⇒ ⛔ **Không đổi tên tệp** `09_MILESTONES_HAI_TAC_VU"
        ".md` — nó đang đúng.",
        "",
        "⛔⛔ Cái thiếu suốt ⛔ **không phải** *«tài liệu chưa đọc tên tệp»* "
        "*(nó có đọc — `BA-05:39`+`:130`)*. Cái thiếu là **CÂU NỐI**: ⛔ không "
        "một dòng nào nói `File 1_2` **là** cái mà `09_MILESTONES` gọi là "
        "*«mốc `A`»*. Thiếu câu nối thì mỗi người tự nối lấy — và đó là chỗ "
        "drift sinh ra.",
        "",
        tu_dien_ten_md().rstrip("\n"),
        "",
        "⚠ **Một tên có thể trỏ tới NHIỀU khâu, và đó là sự thật ⛔ không "
        "được làm tròn.** «ITL (1/2)» là một **TỆP**, ⛔ không phải một bước: "
        "trong nó có cả `Transaction Original` *(Ⓐ)* lẫn `Transaction "
        "Mapping L1` *(Ⓑ)*. Chính vì thế owner trả lời `Q1` là *«nó là một "
        "BƯỚC»*, ⛔ không phải module thứ tư.",
        "",
        "### ⭐⭐⭐ TỪ ĐIỂN THỰC THỂ — một bảng, **ba cách gọi**",
        "",
        "> **Câu bảng này trả lời:** *«`fls_itl` có đúng là cái mà kế toán gọi "
        "là **giao dịch**, và nó ứng với tab nào của ggsheet»* — owner hỏi "
        "`17/09`.",
        "",
        "⛔⛔ **`ITL` = *Input Transaction Ledger* = tên của một cái SỔ**, còn "
        "bảng thì giữ **DÒNG** — chính `schema.py` khai `erd_entity=\"ITL_ROW"
        "\"`. ⇒ Tên vật lý **lệch một bậc** so với thực thể, và nó **được "
        "GIỮ**: owner ⛔ không đặt tên mới, owner *đọc tên hệ đang chạy*. Cái "
        "phải chữa ⛔ không phải cái tên — mà là **câu nối**, và nó ở ngay "
        "bảng dưới.",
        "",
        "⚠ Riêng chữ `Ledge` thì **cố ý ⛔ không mang sang**: tab thật tên "
        "`ITL Ledge` *(thiếu chữ `r`)*. `R-A2` buộc chép nguyên văn lỗi chính "
        "tả **trong tài liệu**, ⛔ nhưng bê nó vào **tên bảng** thì lỗi ấy "
        "sống mãi trong mọi câu `SQL`.",
        "",
        tu_dien_thuc_the_md().rstrip("\n"),
        "",
        "⭐ **`⛔ FLS dựng mới` là một LỜI KHAI, ⛔ không phải một ô trống.** "
        "Nó nói *«AS-IS ⛔ không có thứ này»* — và ba trong số đó là **lý do "
        "dự án tồn tại**: `fls_reject` *(AS-IS ⛔ không giữ dòng bị loại)* · "
        "`fls_chup` *(AS-IS đọc thẳng, ⛔ không lưu ảnh)* · `fls_pm_unlink` "
        "*(AS-IS xoá đè, ⛔ không để lại vết)*.",
        "",
        "### Thực thể thuộc khâu nào — cả `23`",
        "",
        bang_khau_md(bang).rstrip("\n"),
        "",
        "### Ma trận `tầng × khâu` — chỗ HAI TRỤC LỆCH nhau",
        "",
        ma_tran_md(bang).rstrip("\n"),
        "",
        "⭐⭐ **Ba ô đáng nhìn nhất, và cả ba là chỗ hai trục ⛔ không trùng:**",
        "",
        "| Chỗ lệch | Đọc thế nào |",
        "|---|---|",
        "| `fls_pm_line` · tầng **④ GHÉP** · khâu **Ⓑ** — ⛔ nhưng khâu **Ⓐ "
        "GHI nó** | Đường nạp `lo_nap` viết bảng này; nó **tồn tại để** khâu Ⓑ "
        "dùng. ⇒ Sửa đường nạp mà quên rằng *người hưởng* là màn ghép là cách "
        "làm hỏng Ⓑ từ Ⓐ |",
        "| `fls_queue_event` · tầng **⑤** · khâu **V**, **cắt ngang Ⓑ và Ⓒ** | "
        "Một bảng phục vụ **hai** việc ⇒ mọi phép đếm phải nói rõ **đang đếm "
        "việc nào**. Đây đúng là `GAP-ERD-30` nhìn từ trục khâu |",
        "| `fls_itl` · tầng **③** · khâu **S**, cả ba khâu đều chạm | Sổ là "
        "**trục chung**, ⛔ không thuộc riêng khâu nào. Gán nó vào Ⓐ *(vì Ⓐ "
        "ghi)* hay Ⓒ *(vì Ⓒ sửa)* đều làm mất một nửa sự thật |",
        "",
        MOC_CUOI,
    ]) + "\n"


def bom_khau(khoi: str) -> bool:
    """Thay — hay CHEN LAN DAU — vung KHAU trong `BA-05`."""
    txt = DOC.read_text(encoding="utf-8")
    if KHOI_KHAU.search(txt):
        ra = KHOI_KHAU.sub(lambda _: khoi.rstrip("\n"), txt, count=1)
    else:
        neo = "## ERD (rút gọn)"
        if txt.count(neo) != 1:
            raise SystemExit(
                f"⛔ ⛔ KHONG chen duoc vung KHAU: neo `{neo}` khop "
                f"{txt.count(neo)} lan trong {DOC.name} (can dung 1).")
        ra = txt.replace(neo, khoi + "\n---\n\n" + neo, 1)
    if ra == txt:
        return False
    DOC.write_text(ra, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser()
    p.add_argument("--kiem", action="store_true",
                   help="CHI kiem ban ve co khop ban khai, ⛔ khong ghi")
    a = p.parse_args()
    ve = sinh()
    bang = doc_bang()
    ve_khau = sinh_khau()
    print(f"bang doc tu `schema.py` : {len(bang)}")
    for ma, ten, _ in TANG:
        n = sum(1 for b in bang if b.tang == ma)
        print(f"  {ten:18s} {n}")
    print(f"khoa ngoai ve duoc      : {len(canh(bang))}")
    print("khau nghiep vu          :")
    for ma, ten, loai, _ in KHAU:
        n = sum(1 for b in bang if b.khau == ma)
        print(f"  {ten:18s} {n}   ({loai})")

    trang = sinh_html(bang)
    khoi_k = khoi_khau_md(bang, ve_khau)

    if a.kiem:
        # ⛔ CA BON ban phai khop — ban ⛔ khong ai canh la ban se muc.
        lech = []
        if (MMD.read_text(encoding="utf-8") if MMD.exists() else "") != ve:
            lech.append(MMD.name)
        if ((MMD_KHAU.read_text(encoding="utf-8") if MMD_KHAU.exists() else "")
                != ve_khau):
            lech.append(MMD_KHAU.name)
        if (HTM.read_text(encoding="utf-8") if HTM.exists() else "") != trang:
            lech.append(HTM.name)
        txt = DOC.read_text(encoding="utf-8")
        if "```mermaid\nflowchart" not in txt:
            lech.append(f"{DOC.name} (mat khoi `flowchart`)")
        m = KHOI_KHAU.search(txt)
        if not m:
            lech.append(f"{DOC.name} (mat vung KHAU)")
        elif m.group(0).rstrip("\n") != khoi_k.rstrip("\n"):
            lech.append(f"{DOC.name} (vung KHAU lech ban khai)")
        if lech:
            print(f"\n⛔ {len(lech)} ban ⛔ KHONG khop ban khai:")
            for x in lech:
                print(f"     ⛔ {x}")
            print("\n⇒ Doi `schema.py` ma quen sinh lai ban do la cach ban do "
                  "gia TRONG IM LANG. Chay:")
            print("     python tools/sinh_ban_do_tang.py")
            return 1
        print("\n✅ BAN DO KHOP ban khai — ca 4 ban (tang + khau)")
        return 0

    MMD.write_text(ve, encoding="utf-8", newline="\n")
    MMD_KHAU.write_text(ve_khau, encoding="utf-8", newline="\n")
    HTM.write_text(trang, encoding="utf-8", newline="\n")
    print(f"\n✅ da ghi {MMD.name}")
    print(f"✅ da ghi {MMD_KHAU.name}")
    print(f"✅ da ghi {HTM.name}")
    print(f"{'✅ da bom TANG vao' if bom(ve) else '(TANG ⛔ khong doi)'} "
          f"{DOC.name}")
    print(f"{'✅ da bom KHAU vao' if bom_khau(khoi_k) else '(KHAU ⛔ khong doi)'} "
          f"{DOC.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
