"""Ghep prompt gui model: CHI dung input/ — ⛔ khong bao gio doc dap_an/.

Ra:  prompt/system.md        (= he_thong.md)
     prompt/user.md          (toan bo tep input, moi tep mot khoi)
     prompt/prompt_mot_tep.md (system + user trong mot tep, cho giao dien khong co o system prompt)
"""
from pathlib import Path

GOC = Path(__file__).parent
THU_TU = ["danh_muc_sheet.csv", "ban_khai_cot.csv", "bank_S1.csv", "bank_S2.csv", "bank_S3.csv", "bank_S4.csv",
          "so_du_dau.csv", "ccr_so_du_go_tay.csv", "pe_lines.csv", "pi_lines.csv", "pm_lines.csv", "h1000.csv",
          "plt.csv", "mapping_master.csv", "lich_su_vendor.csv", "ty_gia.csv"]


def main():
    vao = GOC / "input"
    co = sorted(p.name for p in vao.glob("*.csv"))
    assert sorted(THU_TU) == co, f"tep input khong khop danh sach: {co}"
    he = (GOC / "he_thong.md").read_text(encoding="utf-8")
    phan = ["Dưới đây là bộ dữ liệu kỳ 01/10/2026 – 07/10/2026. Hãy chạy đủ 4 agent theo system prompt "
            "và trả về đúng 9 khối kết quả.\n"]
    for t in THU_TU:
        phan.append(f"=== FILE: {t} ===\n{(vao / t).read_text(encoding='utf-8').rstrip()}\n")
    user = "\n".join(phan)
    ra = GOC / "prompt"
    ra.mkdir(exist_ok=True)
    (ra / "system.md").write_text(he, encoding="utf-8")
    (ra / "user.md").write_text(user, encoding="utf-8")
    (ra / "prompt_mot_tep.md").write_text(he + "\n\n---\n\n# DỮ LIỆU\n\n" + user, encoding="utf-8")
    print(f"system {len(he):,} ky tu · user {len(user):,} ky tu -> {ra}")


if __name__ == "__main__":
    main()
