# -*- coding: utf-8 -*-
"""DT1b — vòng sửa sau R2 (`KQ-098`): bài cho 2 NÊN SỬA + GHI NHẬN rẻ, đưa vào `tests/du_lieu/`.

ISP 3.1.2 · Step 5 · DT1b · `BG-096` · `KQ-098` · sổ `SO_PHAT_HIEN_ISP-3.1_DT1b.md` (`DT1b-R2-01…05`).

Hai nhóm (giữ phân biệt như R1):
  · `test_R2_DE_XUAT_*` — ĐỎ trên mã R2 (`4a45173`), XANH sau khi sửa mã theo khuyến nghị. Chính là
    phát hiện `DT1b-R2-01` (trần độ lớn lá số) · `DT1b-R2-03` (git ⛔ chạy được ⇒ TỪ CHỐI). RED-first
    chứng minh ở `KQ-099`/tin nhắn phiên.
  · `test_R2_*` (còn lại) — XANH trên mã đúng, ĐỎ trên ĐỘT BIẾN BIÊN mà bộ bài cũ ⛔ bắt (`DT1b-R2-02`
    nhánh phan_xu / R8 · `-04` mẫu hex16 + sorted · `-05` lech tien_te). ⛔ đổi hành vi, chỉ KHOÁ hành
    vi đúng đang có — mỗi bài ghi đột biến nó GIẾT.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from tests.du_lieu import test_phan_loai_ly_do as g


def _t():
    return g._tool()


MONG = dict(g.MONG_TONG_HOP)


# ═══ DT1b-R2-01 · R7 đóng ĐỘ LỚN của lá số, ⛔ chỉ KIỂU (ĐỎ trên 4a45173) ═════════════════════════
SO_CT_INT = 4366191234567890            # Số CT 16 chữ số dạng SỐ NGUYÊN (tổng hợp — int, ⛔ str)

LA_SO = [
    ("so_dong_l1", lambda d: d["mau_so"].update(so_dong_l1=SO_CT_INT)),
    ("khoa_hong.SO", lambda d: d["mau_so"]["khoa_hong"].update(SO=SO_CT_INT)),
    ("khoa_hong.L1", lambda d: d["mau_so"]["khoa_hong"].update(L1=SO_CT_INT)),
    ("dang_khoa_hoc.SO", lambda d: d["mau_so"]["dang_khoa_hoc"].update(SO=SO_CT_INT)),
    ("dang_khoa_hoc.L1", lambda d: d["mau_so"]["dang_khoa_hoc"].update(L1=SO_CT_INT)),
]


@pytest.mark.parametrize("ten, pha", LA_SO, ids=[x[0] for x in LA_SO])
def test_R2_DE_XUAT_la_so_nguyen_co_tran_do_lon(tmp_path, monkeypatch, capsys, ten, pha):
    """DT1b-R2-01 — 4 lá số (`so_dong_l1`, `khoa_hong.SO/L1`, `dang_khoa_hoc.SO/L1`) chỉ kiểm `type is int`
    ⇒ Số CT 16 chữ số DẠNG INT lọt ở chế độ cổng `--tep`. Trần `< TRAN_DEM` chặn. Câu lỗi ⛔ in giá trị."""
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    d = json.loads(goc)
    pha(d)
    sao = tmp_path / "ban_sao.json"
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)
    assert "/mau_so/" in err, err
    assert str(SO_CT_INT) not in err, err      # cổng riêng tư ⛔ in LẠI giá trị vừa bắt (DT1b-R1-04)


def test_R2_tran_do_lon_dung_nguong(tmp_path, monkeypatch, capsys):
    """DT1b-R2-01/-04 — trần đúng ở `10**DAI_TOI_THIEU`: lá số = ngưỡng ⇒ ĐỎ (chặn ép 6→8 và `<`→`<=`);
    = ngưỡng − 1 ⇒ trần ⛔ cắn (số đếm hợp lệ). `so_dong_l1` ⛔ bị MONG ghim ⇒ cô lập được trần."""
    tool = _t()
    nguong = 10 ** tool.DAI_TOI_THIEU
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    # ① đúng ngưỡng ⇒ ĐỎ
    d = json.loads(goc)
    d["mau_so"]["so_dong_l1"] = nguong
    tren = tmp_path / "tren.json"
    tren.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma1, out1, err1 = g._kiem_tep(monkeypatch, capsys, tren, tmp_path)
    assert ma1 == 1, out1
    assert "/mau_so/so_dong_l1" in err1, err1
    # ② ngay dưới ngưỡng ⇒ trần ⛔ cắn (so_dong_l1 ⛔ có MONG ⇒ qua)
    d2 = json.loads(goc)
    d2["mau_so"]["so_dong_l1"] = nguong - 1
    duoi = tmp_path / "duoi.json"
    duoi.write_text(json.dumps(d2, ensure_ascii=False), encoding="utf-8")
    ma2, out2, err2 = g._kiem_tep(monkeypatch, capsys, duoi, tmp_path)
    assert ma2 == 0, err2


# ═══ DT1b-R2-02 · ba nhánh của chính bản sửa R1 chưa có bài (đột biến BIÊN SỐNG) ══════════════════
def test_R2_phan_bo_ghim_van_tay_nhan_None_la_ma_4(tmp_path, monkeypatch, capsys):
    """DT1b-R2-02 (a) — nhánh `mong_vt is None` của `phan_xu`: chỉ `phan_bo_nhan` ghim, `van_tay_nhan`
    CHƯA ghim ⇒ mã 4 (⛔ 0 — kịch bản `DT1b-R1-05` quay lại). Đột biến `or mong_vt is None` → bỏ (chỉ
    `mong is None`) CHẾT ở đây."""
    tool = _t()
    monkeypatch.setitem(tool.MONG, "phan_bo_nhan", dict(MONG))      # ghim phân bố
    # van_tay_nhan GIỮ None (mặc định) — khác lượt phan_bo ⇒ chưa đủ để ĐẠT
    van_ban, _, _ = g._dung(7)
    p = g._ghi_csv(tmp_path, van_ban)
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(p), "--ghi", ra=ra, mong_nhan="giu")
    assert ma == 4, (out, err)
    assert "CHƯA GHIM" in out and "vân tay danh tính nhãn" in out, out
    assert ra.exists()                                             # đo trọn, cấu trúc đạt ⇒ ghi để owner gửi về


def _repo_git(tmp_path):
    """Repo giả có `.gitignore hien_vat/` + bản đọc tổng hợp ở gốc (⛔ bị ignore)."""
    repo = tmp_path / "repo_gia"
    (repo / "hien_vat").mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-q"], check=True)
    (repo / ".gitignore").write_text("hien_vat/\n", encoding="utf-8")
    van_ban, _, _ = g._dung(7)
    (repo / "dt1b_khoa.csv").write_text(van_ban, encoding="utf-8")
    return repo


def test_R2_R8_duong_TUONG_DOI_trong_repo_khong_ignore_bi_tu_choi(tmp_path, monkeypatch, capsys):
    """DT1b-R2-02 (b) — R8 với đường TƯƠNG ĐỐI: `.resolve()` trước `relative_to(GOC)` là bắt buộc. Đột
    biến bỏ `.resolve()` ⇒ `Path('dt1b_khoa.csv').relative_to(GOC tuyệt đối)` ném ValueError ⇒ lọt. CHẾT."""
    tool = _t()
    repo = _repo_git(tmp_path)
    monkeypatch.setattr(tool, "GOC", repo)
    monkeypatch.chdir(repo)
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", "dt1b_khoa.csv", "--ghi", ra=ra,
                                 mong_nhan=dict(MONG))
    assert ma == 2, (out, err)
    assert "bị .gitignore" in err and not ra.exists()


def test_R2_R8_khong_phai_git_repo_tra_128_van_tu_choi(tmp_path, monkeypatch, capsys):
    """DT1b-R2-02 (c) — thư mục TRONG `GOC` mà ⛔ phải git repo ⇒ `git check-ignore` trả 128 ⇒ returncode≠0
    ⇒ fail-đóng (mã 2). Đột biến `r.returncode != 0` → `== 1` (128 lọt) CHẾT ở đây."""
    tool = _t()
    repo = tmp_path / "khong_git"           # ⛔ git init ⇒ check-ignore fatal (128)
    repo.mkdir()
    van_ban, _, _ = g._dung(7)
    (repo / "dt1b_khoa.csv").write_text(van_ban, encoding="utf-8")
    monkeypatch.setattr(tool, "GOC", repo)
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(repo / "dt1b_khoa.csv"), "--ghi",
                                 ra=ra, mong_nhan=dict(MONG))
    assert ma == 2, (out, err)
    assert "bị .gitignore" in err and not ra.exists()


# ═══ DT1b-R2-03 · git ⛔ chạy được ⇒ TỪ CHỐI (OSError ⇒ mã 2) — ĐỎ trên 4a45173 (Đ5) ═══════════════
def test_R2_DE_XUAT_git_khong_chay_duoc_la_TU_CHOI(tmp_path, monkeypatch, capsys):
    """DT1b-R2-03 — `git` ⛔ chạy được (PATH ⛔ có git) ⇒ ⛔ chứng minh được `.gitignore` che ⇒ fail-đóng
    (mã 2), ⛔ để tệp TRONG repo lọt (Đ5). `except OSError: return False` → `return True`."""
    tool = _t()
    repo = _repo_git(tmp_path)
    monkeypatch.setattr(tool, "GOC", repo)
    monkeypatch.setenv("PATH", "/nonexistent")       # git ⛔ chạy được ⇒ OSError
    ra = tmp_path / "ra.json"
    ma, out, err = g._chay_trong(monkeypatch, capsys, "--khoa", str(repo / "dt1b_khoa.csv"), "--ghi",
                                 ra=ra, mong_nhan=dict(MONG))
    assert ma == 2, (out, err)
    assert "bị .gitignore" in err and not ra.exists()


# ═══ DT1b-R2-04 · mỗi NGƯỠNG / MẪU của chốt riêng tư một bài hai bên biên ══════════════════════════
@pytest.mark.parametrize("ten, bam", [("17_ky_tu", "a" * 16 + "b"), ("chu_HOA", "A" * 16)],
                         ids=["17_ky_tu", "chu_HOA"])
def test_R2_khoa_bam_MAU_hex16_neo_hai_dau(tmp_path, monkeypatch, capsys, ten, bam):
    """DT1b-R2-04 — `MAU_HEX16` neo HAI đầu `^…$`, ⛔ `re.I`: khoa_bam 17 ký tự (bỏ `$`) · hex chữ HOA
    (thêm `re.I`) ⇒ ĐỎ. Đột biến tương ứng CHẾT."""
    goc = g._ban_hop_le(tmp_path, monkeypatch, capsys)
    d = json.loads(goc)
    d["dong_thieu"][0]["khoa_bam"] = bam
    sao = tmp_path / "ban_sao.json"
    sao.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    ma, out, err = g._kiem_tep(monkeypatch, capsys, sao, tmp_path)
    assert ma == 1, (ten, out)
    assert "khoa_bam" in err, err


def test_R2_van_tay_nhan_doc_lap_thu_tu_dong():
    """DT1b-R2-04 — `_van_tay_nhan` phải ĐỘC LẬP thứ tự dòng (có `sorted`): đảo thứ tự `dong_thieu` ⇒ CÙNG
    vân tay. Đột biến bỏ `sorted` CHẾT. (K13 ⛔ được phụ thuộc vị trí dòng trong tệp.)"""
    tool = _t()
    dong = [{"dong_sheet": 10, "nhan": "KHAC", "lech": [], "ghi_chu": "KHOP_KHI_GHEP_LAI"},
            {"dong_sheet": 20, "nhan": "KHOA_LECH", "lech": ["ps_no"], "ghi_chu": None},
            {"dong_sheet": 30, "nhan": "TRUNG_SEQ", "lech": [], "ghi_chu": None}]
    assert tool._van_tay_nhan(dong) == tool._van_tay_nhan(list(reversed(dong)))


# ═══ DT1b-R2-05 · mỗi CỘT của khoá ghép một ca lệch riêng (bộ dựng ⛔ có ca lệch `tien_te`) ═════════
def test_R2_KHOA_LECH_truong_tien_te():
    """DT1b-R2-05 — `lech` quét `range(5)` (đủ 5 cột). Hai khoá chỉ khác `tien_te` cùng Số CT ⇒
    `lech == ['tien_te']`. Đột biến `range(4)` (bỏ `tien_te`) CHẾT."""
    t = _t()
    K = ("CT1", "100", "0", "1121", "VND")
    KL = ("CT1", "100", "0", "1121", "USD")          # chỉ khác tien_te
    nh, _ = t.phan_loai({1: K}, {101: KL}, [1])
    assert (nh[1]["nhan"], nh[1]["lech"]) == ("KHOA_LECH", ["tien_te"])
