"""WO-234 · máy quét số tài khoản CÁ NHÂN trên MỌI tệp đã theo dõi (`git ls-files`).

Số giả dưới đây được SINH TỪ ghép chuỗi lúc chạy — ⛔ không phải số thật, ⛔ không in ra.
  ca phá (Đ5)  · mẫu thật phải ĐỎ trên văn bản có số giả
  mẫu số (Đ3)  · quét repo phải duyệt > 1000 tệp, ⛔ xanh trên tập rỗng
  cổng         · repo hiện hành = 0 số TK cá nhân (tái phạm ⇒ ĐỎ ở bài này)
"""
import subprocess
import sys
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
