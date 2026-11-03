"""Than cua cac tep SINH — dung chung cho moi bai dung mot may phuc vu.

⛔⛔ **Vi sao co tep nay thay vi mot gia tri mac dinh trong `phuc_vu.py`.**
`lam_nguoi_phuc_vu` **⛔ khong duoc** tu di lay than cua `cot.js`: lam vay la
`fls.web` phai `import fls.api.cot_so`, va tu do voi xuong `fls.canon` +
`fls.oracle` — dung ba tang ma **luat thu tam** cua `import-linter` cam. ⇒ Than
duoc **dua vao**, va moi noi dung may deu phai noi ro no phuc vu cai gi.

⚠ Cai gia phai tra la moi bai kiem phai goi ham nay. Do la gia **dung**: mot
bai dung may ma ⛔ khong noi no phuc vu bang cot nao la mot bai kiem mot may
khac voi may that.
"""
from __future__ import annotations

from fls.api.cot_so import than_js


def than_sinh() -> dict[str, bytes]:
    """⚠ `danh_muc.js` o day co than **RONG co chu y**.

    Bo test ⛔ khong co kho de doc `fls_mapping_master`, va mot danh sach gia
    se lam bai *"danh muc RONG thi man phai NOI RA rang cua ⛔ khong kiem
    duoc"* mat y nghia. Bai nao can mot danh muc that thi **tu dat**
    `window.FLS_DM_HD` trong kich ban cua no.
    """
    return {"cot.js": than_js(),
            "danh_muc.js": b"window.FLS_DM_HD = [];\n"}
