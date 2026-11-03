# -*- coding: utf-8 -*-
"""⛔⛔ Khoá ngoại lệ **`them_vao_so`** — điều kiện ⓒ, quét MÃ NGUỒN cả `fls/`.

Ngày 08/09 bảng tuyến lần đầu cho **một** tuyến ghi vào `fls_itl`: `POST /nap`.
Cho tới hôm ấy luật là *"⛔ không tuyến nào được ghi vào sổ"* — và nó **đúng**,
vì lúc ấy ⛔ **không tuyến nào NẠP**: mọi `POST` đều **sửa một dòng ĐÃ CÓ**.

⭐ `INV-I08` đọc nguyên văn là *"chỉ **THÊM**, ⛔ không **SỬA**"* — nên phép
  **THÊM** chính là thứ bất biến ấy **cho phép**. Một cổng ⛔ không phân biệt
  được hai việc sẽ **cấm luôn cái nó sinh ra để bảo vệ**.

⛔⛔ **Nhưng một ngoại lệ chỉ an toàn khi nó CHỨNG MINH ĐƯỢC.** Bảng tuyến đã
   siết hai điều kiện *(phải `POST` · phải ghi `fls_run`)*; điều kiện thứ ba ⛔
   **không thể** kiểm bằng một bản khai — nó phải nhìn vào **mã thật**:

       ⛔ Cả `fls/` ⛔ KHÔNG được chứa một câu `UPDATE`/`DELETE` nào nhắm
          `fls_itl`.

   Có nó thì `them_vao_so` ⛔ **không thể** lặng lẽ biến thành *"sửa sổ"* — vì
   ⛔ không có câu lệnh nào để làm việc đó, ở bất cứ đâu trong mã chạy việc.
"""
from __future__ import annotations

import ast
import pathlib

from fls.api.bang_tuyen import BANG_TUYEN, SO

GOC = pathlib.Path(__file__).resolve().parents[2] / "fls"
_DONG_TU_SUA = ("update", "delete from")


def _cau_sql(cay: ast.AST) -> list[tuple[int, str]]:
    """Mọi HẰNG CHUỖI trong mã. ⛔ Không đọc ghi chú — một cổng báo động vì
    đọc đúng cái ghi chú nói *"việc này bị cấm"* là một cổng sắp bị gỡ ra."""
    ra: list[tuple[int, str]] = []
    for n in ast.walk(cay):
        if isinstance(n, ast.Constant) and isinstance(n.value, str):
            ra.append((n.lineno, n.value))
        elif isinstance(n, ast.JoinedStr):
            ra.append((n.lineno, "".join(
                v.value for v in n.values
                if isinstance(v, ast.Constant) and isinstance(v.value, str))))
    return ra


def test_CA_fls_KHONG_co_cau_SUA_hay_XOA_nham_fls_itl():
    """⛔ Điều kiện ⓒ của `them_vao_so`."""
    xau: list[str] = []
    for f in sorted(GOC.rglob("*.py")):
        cay = ast.parse(f.read_text(encoding="utf-8"), filename=str(f))
        for dong, s in _cau_sql(cay):
            c = " ".join(s.lower().split())
            if any(c.startswith(f"{tu} {SO}") for tu in _DONG_TU_SUA):
                xau.append(f"{f.relative_to(GOC)}:{dong}")
    assert xau == [], (
        "⛔ ma chay viec co cau SUA/XOA nham `%s`: %s. `them_vao_so` chi an "
        "toan khi ⛔ KHONG co cau lenh nao lam duoc viec do, o BAT CU dau."
        % (SO, " · ".join(xau)))


def test_phep_quet_nay_THAT_SU_do_duoc_gi():
    """⛔ Cổng chung #7: quét trên **0 tệp** thì tất nhiên ⛔ không thấy lỗi."""
    n = len(list(GOC.rglob("*.py")))
    assert n >= 30, f"⛔ chi quet duoc {n} tep — phep quet nay dang do qua it"


def test_DUNG_HAI_tuyen_duoc_khai_them_vao_so():
    """⛔⛔ Một ngoại lệ **CÓ TÊN** thì phải **đếm được**, và con số phải nhỏ.

    ⭐ Bài này ⛔ **không** khoá *tên* tuyến — khoá tên thì đổi đường dẫn cũng
      đỏ, và người ta sẽ gỡ cổng. Nó khoá **SỐ LƯỢNG**: thêm một tuyến thứ hai
      ghi vào sổ là một **quyết định**, và nó phải đi qua chỗ này.

    ⭐⭐ **`1 → 2` ngày 2026-09-08 (`QĐ-ITL-111`), và đây là quyết định:**
       `POST /nap/lo` thêm dòng vào sổ **cho cả lô**. Nó ⛔ **không** phải một
       cơ chế ghi thứ hai — nó gọi **đúng** `nap_lo` → `chay_nap.chay()` mà
       tuyến `POST /nap` gọi, chỉ **lặp theo từng nguồn** trong **MỘT** giao
       dịch. Ba thứ ⛔ không được có bản sao *(chống trùng `content_key` · cổng
       bốn đường · một giao dịch)* vẫn nằm **đúng một chỗ**.

    ⛔⛔ **Vì sao vẫn phải là một tuyến RIÊNG chứ ⛔ không nhồi vào `POST
       /nap`:** khuôn **TRẢ VỀ** khác hẳn *(biên bản GỘP mang
       `so_nguon_vao`/`so_nguon_chua`, mỗi luật mang danh sách nguồn ⛔ không
       đạt)*. Một tuyến trả **hai khuôn** là một tuyến mà người gọi ⛔ **không
       biết mình đang đọc khuôn nào**.

    ⇒ Con số **2** là trần cho hôm nay. Cái thứ ba phải đọc lại đoạn này.
    """
    them = [t for t in BANG_TUYEN if t.them_vao_so]
    assert len(them) == 2, (
        "⛔ co %d tuyen khai `them_vao_so` (mong doi 2): %s. Them mot tuyen ghi "
        "vao so la mot QUYET DINH — sua con so nay CO Y de phai doc doan nay."
        % (len(them), [t.duong for t in them]))
    assert all(t.phuong_thuc == "POST" for t in them), them
    # ⛔ Ca hai PHAI ghi `fls_run` — mot dong so ⛔ khong co lan nap la mot
    #    dong **mat lineage** (`INV-I05`/`I12`), dung thu `GAP-ERD-P0-01` da
    #    dong bang mot FK. Day la dieu kien ⓑ cua `them_vao_so`.
    for t in them:
        assert "fls_run" in t.bang_ghi, t.duong
    # ⭐ Va ca hai PHAI di qua CUNG mot ham ghi: neu mot ngay nao do `lo_nap`
    #   tu viet cau `INSERT` rieng thi bai `test_CA_fls_KHONG_co_cau_SUA...`
    #   o tren van xanh (no chi canh SUA/XOA) ⇒ ghim o day.
    import fls.api.nap_cua as _nc
    import inspect
    for ten in ("nap", "lo_nap"):
        ma = inspect.getsource(getattr(_nc, ten))
        assert "nl.nap_lo(" in ma, (
            "⛔ `%s` ⛔ KHONG goi `nap_lo` ⇒ no dang co mot duong ghi RIENG, "
            "va luc ay ba thu chong-trung/bon-duong/mot-giao-dich co **hai "
            "ban**" % ten)


# ⚠ Phep kiem *"moi tuyen KHAC van bi cam ghi vao so"* ⛔ KHONG dat o day —
# no da song o `tests/api/test_bang_tuyen.py::test_KHONG_duong_nao_GHI_vao_so`,
# cung voi **loi canh bao lich su** giai thich vi sao cau khang dinh ay tung bi
# hieu sai HAI lan. Chep no sang day la tao **ban thu hai cua mot luat**, va ban
# thu hai bao gio cung la ban se troi.


def test_cong_bang_tuyen_CAN_that_neu_bo_dieu_kien_hep():
    """⭐⭐ Chứng minh ba điều kiện hẹp **cắn thật**, ⛔ không phải chữ trang trí.

    Dựng lại ba hiện trường sai và đòi cổng PHẢI đỏ ở **từng** cái.
    """
    from dataclasses import replace

    from fls.api.bang_tuyen import kiem_bang_tuyen

    goc = next(t for t in BANG_TUYEN if t.them_vao_so)
    khac = tuple(t for t in BANG_TUYEN if not t.them_vao_so)

    # ⓐ ⛔ không phải POST
    assert kiem_bang_tuyen(khac + (replace(goc, phuong_thuc="PUT"),)), \
        "⛔ cong ⛔ khong bat duoc `them_vao_so` tren mot phuong thuc KHAC POST"
    # ⓑ ⛔ không ghi `fls_run`
    khong_run = replace(goc, bang_ghi=tuple(
        b for b in goc.bang_ghi if b != "fls_run"))
    assert kiem_bang_tuyen(khac + (khong_run,)), \
        "⛔ cong ⛔ khong bat duoc dong so ⛔ khong co lan nap (mat lineage)"
    # ⓒ khai ngoại lệ mà ⛔ không dùng
    khong_dung = replace(goc, bang_ghi=tuple(
        b for b in goc.bang_ghi if b != SO), ghi=True)
    assert kiem_bang_tuyen(khac + (khong_dung,)), \
        "⛔ cong ⛔ khong bat duoc mot ngoai le KHAI ma ⛔ KHONG DUNG DEN"
