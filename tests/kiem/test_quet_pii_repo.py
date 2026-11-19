"""WO-234 · máy quét số tài khoản CÁ NHÂN trên MỌI tệp đã theo dõi (`git ls-files`).

Số giả dưới đây được SINH TỪ ghép chuỗi lúc chạy — ⛔ không phải số thật, ⛔ không in ra.
  ca phá (Đ5)  · mẫu thật phải ĐỎ trên văn bản có số giả
  mẫu số (Đ3)  · quét repo phải duyệt > 1000 tệp, ⛔ xanh trên tập rỗng
  cổng         · repo hiện hành = 0 số TK cá nhân (tái phạm ⇒ ĐỎ ở bài này)
"""
import io
import re
import subprocess
import sys
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(GOC / "tools"))
import quet_pii_repo as q  # noqa: E402

SO14 = "9" * 3 + "1" * 11          # số giả 14 chữ số
SO8 = "7" * 8


def test_phu_dinh_khoa_R_CN_bi_bat():
    van = f"| R | {SO14}_MSB VND_CN | x |"
    assert [m.mau for m in q.quet_van_ban(van)] == ["khoa_R_CN"]


def test_ca_pha_ba_dang_khac_cung_bi_bat():
    assert [m.mau for m in q.quet_van_ban(f'{{"tk":"{SO8}","bank":"ACB","le":"CN"}}')] == ["tk_json_CN"]
    assert [m.mau for m in q.quet_van_ban(f"{SO14}-010125-CK 5/1 cho A")] == ["dien_giai_CK"]
    assert [m.mau for m in q.quet_van_ban(f"R \\| {SO14}_MSB USD_CN")] == ["khoa_R_CN"]


def test_khong_bat_nham_so_tien_ma_hoac_tk_phap_nhan():
    for van in (
        "R | AAA_MSB VND_CN",                         # giữ chỗ test
        f"R | {SO14}_MSB VND_VGO9",                   # TK pháp nhân — ngoài phạm vi WO-234
        "số tiền 123456789012 VND",                   # số tiền
        "R | TK_CA_NHAN_1_MSB VND_CN",                # mã che
        f'{{"tk":"{SO8}","bank":"ACB","le":"VGOH"}}', # pháp nhân
    ):
        assert q.quet_van_ban(van) == [], van


def test_che_khong_dao_duoc_va_gom_cung_so_ve_cung_ma():
    van = f"R | {SO14}_MSB VND_CN ; mô tả {SO14}-010125-CK 1/1 ; R | {SO8}_ACB VND_CN"
    ma = {}
    moi = q.che_van_ban(van, ma)
    assert SO14 not in moi and SO8 not in moi
    assert moi.count("TK_CA_NHAN_1") == 2 and moi.count("TK_CA_NHAN_2") == 1
    assert q.quet_van_ban(moi) == []
    assert list(ma.values()) == [1, 2]


def test_quet_repo_mau_so_khong_rong_va_dat_0():
    kq = q.quet_repo(GOC)
    assert kq.so_tep > 1000, kq.so_tep                  # Đ3: mẫu số
    assert kq.so_mau == 3                               # Đ5: số mẫu khai
    assert kq.theo_tep == {}, {t: len(v) for t, v in kq.theo_tep.items()}


def test_cli_do_khi_co_tep_ban(tmp_path):
    """Ca phá cấp CLI: repo tạm có MỘT tệp mang số giả ⇒ thoát 1; xoá nó ⇒ thoát 0."""
    sh = lambda *a: subprocess.run(a, cwd=tmp_path, check=True, capture_output=True)
    sh("git", "init", "-q")
    (tmp_path / "a.md").write_text(f"R | {SO14}_MSB VND_CN\n", encoding="utf-8")
    sh("git", "add", "a.md")
    kq = subprocess.run([sys.executable, str(GOC / "tools" / "quet_pii_repo.py"), "--goc", str(tmp_path)],
                        capture_output=True, text=True)
    assert kq.returncode == 1 and SO14 not in kq.stdout + kq.stderr
    (tmp_path / "a.md").write_text("sạch\n", encoding="utf-8")
    kq = subprocess.run([sys.executable, str(GOC / "tools" / "quet_pii_repo.py"), "--goc", str(tmp_path)],
                        capture_output=True, text=True)
    assert kq.returncode == 1 and "ĐỎ" in kq.stdout       # tập 1 tệp < mẫu số tối thiểu ⇒ ĐỎ (Đ3)


# ───────────────────────── vòng sửa sau R1 (KQ-239) ─────────────────────────
def _git_repo(tmp_path, tep: dict):
    sh = lambda *a: subprocess.run(a, cwd=tmp_path, check=True, capture_output=True)
    sh("git", "init", "-q")
    for ten, nd in tep.items():
        (tmp_path / ten).write_bytes(nd if isinstance(nd, bytes) else nd.encode("utf-8"))
        sh("git", "add", ten)


def _zip(**tep) -> bytes:
    b = io.BytesIO()
    with zipfile.ZipFile(b, "w", zipfile.ZIP_DEFLATED) as z:
        for ten, nd in tep.items():
            z.writestr(ten.replace("__", "/"), nd)
    return b.getvalue()


def test_R1_01_quet_doc_ruot_zip(tmp_path):
    """PII-R1-01: số giả CHỈ nằm trong ruột zip ⇒ máy quét ⛔ im; tệp ảo tên `zip!ruột`."""
    _git_repo(tmp_path, {"a.zip": _zip(ban__x_html=f"R | {SO14}_MSB VND_CN\n"), "b.md": "sạch\n"})
    kq = q.quet_repo(tmp_path)
    assert list(kq.theo_tep) == ["a.zip!ban/x_html"], kq.theo_tep


def test_R1_01_che_zip_giu_cau_truc_va_doi_dung_cho_che():
    """Nén lại CÙNG cấu trúc (tên · thứ tự · ngày · kiểu nén); khác bản gốc CHỈ ở số→nhãn."""
    goc = _zip(a__tep1=f"R | {SO14}_MSB VND_CN\ndòng 2\n", b__tep2=f"{SO14}-010125-CK x\n", c__sach="không có gì\n")
    ma = {SO14: 3}                                   # nhãn có sẵn (3) ⇒ dùng lại, ⛔ đánh số mới
    moi, dem = q.che_zip(goc, ma)
    zg, zm = zipfile.ZipFile(io.BytesIO(goc)), zipfile.ZipFile(io.BytesIO(moi))
    assert [i.filename for i in zg.infolist()] == [i.filename for i in zm.infolist()]
    assert [(i.date_time, i.compress_type) for i in zg.infolist()] == [(i.date_time, i.compress_type) for i in zm.infolist()]
    for i in zg.infolist():
        a, b = zg.read(i).decode(), zm.read(i.filename).decode()
        assert b == re.sub(SO14, "TK_CA_NHAN_3", a), i.filename
    assert dem == {"a/tep1": 1, "b/tep2": 1} and ma == {SO14: 3}


def test_R1_04_do_khi_khong_doc_duoc_tep_van_ban(tmp_path, monkeypatch):
    """PII-R1-04 (M2): `_doc` luôn None ⇒ so_doc = 0 ⇒ ĐỎ (trước: 6/6 bài xanh)."""
    _git_repo(tmp_path, {f"f{i}.md": "sạch\n" for i in range(3)})
    monkeypatch.setattr(q, "_doc", lambda goc, t: None)
    kq = q.quet_repo(tmp_path)
    assert kq.so_doc == 0 and len(kq.khong_doc) == 3
    monkeypatch.setattr(q, "MONG_TOI_THIEU_DOC", 1)
    assert q.danh_gia(kq)[0] is True                  # do=True


def test_R1_04_nhi_phan_khai_theo_duoi_co_ten_con_lai_la_do(tmp_path):
    _git_repo(tmp_path, {"a.png": b"\x89PNG\xff\xfe\x00", "c.dat": b"\xff\xfe\xfd", **{f"b{i}.md": "sạch\n" for i in range(40)}})
    kq = q.quet_repo(tmp_path)
    assert kq.khong_doc_co_y == ["a.png"] and kq.khong_doc_la == ["c.dat"]      # c.dat ⛔ khai ⇒ đỏ
    assert q.danh_gia(kq, toi_thieu=1)[0] is True
    (tmp_path / "c.dat").write_text("chữ\n", encoding="utf-8")
    assert q.danh_gia(q.quet_repo(tmp_path), toi_thieu=1)[0] is False


def test_R1_05_bien_chu_so_o_buoc_che():
    """PII-R1-05 (M9): số cần che DÍNH trong chuỗi số dài hơn ⇒ ⛔ bị thay."""
    dai = "5" + SO14 + "5"
    van = f"R | {SO14}_MSB VND_CN ; số khác {dai} ; trước {SO14}x"
    moi = q.che_van_ban(van, {})
    assert dai in moi                                  # chuỗi dài hơn còn nguyên
    assert moi.count("TK_CA_NHAN_1") == 2


def test_R1_02_03_so_da_biet_CN_bat_ca_dang_chu_tu_do():
    """Số đã CHẮC là cá nhân (có khoá `CN`) mà lặp ở dạng tự do ⇒ bắt + che cả ba dạng."""
    tu_do = [f"1/1 cho {SO14}-Nguyen Van A", f"{SO14}-Ref 6194ABC-CK 24/7", f"tài khoản {SO14} của", f"nhãn {SO14}_MSB VND_VGO1"]
    cn = {SO14}
    for d in tu_do:
        assert [m.mau for m in q.quet_van_ban(d, da_biet=cn)] == ["so_da_biet_CN"], d
        assert q.quet_van_ban(d) == [], d              # chưa biết số ⇒ ⛔ đoán
    ma = {}
    moi = q.che_van_ban(f"R | {SO14}_MSB VND_CN\n" + "\n".join(tu_do), ma)
    assert SO14 not in moi and moi.count("TK_CA_NHAN_1") == 5


def test_R1_02_03_so_la_trong_chu_tu_do_GIU_va_DEM(tmp_path):
    """Pháp nhân/không rõ: ⛔ che; chỉ ĐẾM (`so_giu_dang_tu_do`)."""
    _git_repo(tmp_path, {"a.md": f"cho {SO8}-APERO HQ x\n{SO8}-Ref 1-CK\ntài khoản {SO8}\n"})
    kq = q.quet_repo(tmp_path)
    assert kq.theo_tep == {} and kq.giu_tu_do == {"cho": 1, "ref": 1, "tk": 1}


def test_R1_02_che_repo_xu_ly_tep_chi_co_so_da_biet(tmp_path):
    """-02: tệp KHÔNG có mẫu `CN` nhưng mang số đã biết ở nơi khác ⇒ che_repo vẫn xử lý."""
    _git_repo(tmp_path, {"a.md": f"R | {SO14}_MSB VND_CN\n", "b.md": f"mô tả cho {SO14}-Nguyen Van A\n"})
    dem = q.che_repo(tmp_path)
    assert dem == {"a.md": 1, "b.md": 1}
    assert SO14 not in (tmp_path / "b.md").read_text(encoding="utf-8")


def test_R1_02_so_vua_CN_vua_phap_nhan_GIU_va_DEM(tmp_path):
    """Chủ 19/11 08:30: ⛔ CHẮC cá nhân (có cả khoá pháp nhân) ⇒ GIỮ + ĐẾM, ⛔ che."""
    _git_repo(tmp_path, {"a.md": f"{SO14}-010125-CK x\n", "b.md": f"R | {SO14}_MSB VND_VGO1\nR | {SO14}_MSB VND_VGO1\n"})
    kq = q.quet_repo(tmp_path)
    assert kq.xung_dot == 3 and kq.so_da_biet == 0
    assert list(kq.theo_tep) == ["a.md"]                 # chỉ mẫu CK (còn là mẫu cá nhân), ⛔ hai dòng VGO1
    q.che_repo(tmp_path)
    assert SO14 in (tmp_path / "b.md").read_text(encoding="utf-8")


def test_R1_04_do_khi_ty_le_doc_duoc_thap(tmp_path):
    """Đa số mục là nhị phân khai theo đuôi (dù đã khai) ⇒ phép đo ⛔ đáng tin ⇒ ĐỎ (ty lệ < 95 %)."""
    _git_repo(tmp_path, {"b.md": "sạch\n", **{f"i{k}.png": b"\xff\xfe" for k in range(5)}})
    kq = q.quet_repo(tmp_path)
    assert kq.so_doc == 1 and len(kq.khong_doc_co_y) == 5 and not kq.khong_doc_la
    assert q.danh_gia(kq, toi_thieu=1)[0] is True


def test_R1_nhan_danh_so_theo_thu_tu_gap_khong_phu_thuoc_bam():
    """`so_cn` trả danh sách THEO THỨ TỰ GẶP (⛔ set: băm ngẫu nhiên ⇒ nhãn lệch giữa các lần chạy)."""
    so = [str(k) * 8 for k in range(1, 9)]
    van = "\n".join(f"R | {s}_MSB VND_CN" for s in so)
    assert q.so_cn(van) == so
    ma = {}
    q.che_van_ban(van, ma)
    assert list(ma.items()) == [(s, i + 1) for i, s in enumerate(so)]
