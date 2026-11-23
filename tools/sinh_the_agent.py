# -*- coding: utf-8 -*-
"""Sinh 4 THẺ agent (`docs/ITL/06_Agent/A*.md`) + 4 GÓI zip để chủ đọc/đánh giá từng agent.

    python tools/sinh_the_agent.py          # ghi 4 thẻ + README
    python tools/sinh_the_agent.py --zip    # + 4 zip ở docs/ITL/06_Agent/goi/

⭐ Thẻ là nơi chủ đọc trước khi cho chạy (mục tiêu: ≤ 10 phút cho cả 4). Checksum prompt trong thẻ do MÁY
   tính lúc sinh; `tests/agent/test_skill_tang.py` ĐỎ khi prompt đổi mà thẻ chưa sinh lại.
⭐ Một zip = thẻ + `00_he_thong.md` + mọi skill `NN_*.md` (đúng thứ tự chạy) + bản phát lại + thẻ fleet eval
   liên quan. Chủ sửa ngay trong tệp skill rồi gửi lại; Dev chép về `fls/agent/skill/<agent>/`, chạy
   `--gia --ghi-phat-lai`, sinh lại thẻ, chạy cổng.
"""
from __future__ import annotations

import argparse
import sys
import zipfile
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(GOC))

from fls.agent.chuoi import AGENT, can_mo_hinh  # noqa: E402
from fls.agent.skill import THU_MUC, checksum_prompt, nap_bo  # noqa: E402

TM = GOC / "docs" / "ITL" / "06_Agent"
EVAL = GOC / "docs" / "ITL" / "05_FleetEval" / "eval-cards"

VAI = {
 "A1_RI": dict(
  hop="AP Voi v3.1.2 §4.1 — RI.BANK · RI.PAY (PARTIAL) · §4.5 RI.HR · RI.PLT (PROPOSED)",
  vao="ảnh đóng băng 4 nguồn raw: Bank (`tests/fixture/pm_join.json` bank + `itl_ledge_adjustment.json` sổ AS-IS) · "
      "FPS (`pm_join.json` pm) · H1000 (`dau_vao/hr_ledger_2024/2025.json`) · PLT (`dau_vao/gi_cfa1.json` + "
      "`dap_an/{omc,sc,ps}_mid1.json`)",
  ra="ô `nguon:<nguồn>.so_dong · dem_dong · van_tay` (+ `fps.co_ref`) — 9 ảnh",
  cong_cu="`nguon_bank` · `nguon_fps` · `nguon_h1000` · `nguon_plt` = đếm dòng + đọc vân tay ảnh (`tools/chay_agent_voi.py:dem_nguon`)",
  eval="chưa có thẻ riêng (Voi: `a1-khai-chup.eval.lech-cot-ngay` PROPOSED)", the_eval=(),
  thong_minh="Hôm nay chỉ đếm + vân tay. Đề xuất G1 (Voi roadmap 01/03): đề xuất bản khai cho sheet mới · báo đổi bố cục cột."),
 "A2_PR_MAP": dict(
  hop="AP Voi v3.1.2 §4.2 PR.BANK · PR.PAY · §4.3.1 SI.MAP (PARTIAL)",
  vao="ảnh của A1 (bank · PM line) — engine FLS chạy trên ảnh đóng băng",
  ra="ô `voi:theo_ky.*.{co,chay,map_fls,pm_noi,map_now,day_nguoi}` · `voi:bank_tong.dong_theo_hinh.A–F` · "
     "`voi:dat_hd1.theo_ky.*.thieu` · G0: `noi:<ca>.chon` + `ly_do`",
  cong_cu="`dong_chuan` · `ghep_ref` · `hang_cho` = `tools/do_voi_so_luong.do()` (gọi `pm_join.xep_ca_lat` · `moi_noi`) · "
          "`ung_vien_ghep` = bể ca (dựng trong repo / GIỮ RIÊNG qua `FLS_HELDOUT_NOI_DUNG`)",
  eval="`a3-1-ref.eval.ghep-sai` (rubric 0–2; bar: 0 ca phải-để-người bị nối) — vòng: `docs/ITL/05_FleetEval/vong/TONG_HOP.md`",
  the_eval=("_chung.md", "a3-1-ref.md"),
  thong_minh="Skill 04 ghép theo NỘI DUNG giao dịch (G0 bóng): mã PM trong nội dung đã che + tiền + tiền tệ + ngày; "
             "luật cứng chặn chọn ngoài ứng viên / lệch tiền / dùng lại PM line. Gửi nội dung TẮT mặc định — câu chủ C4."),
 "A3_SI_ITL": dict(
  hop="AP Voi v3.1.2 §4.3.2 SI.ITL (PARTIAL) + CALCULATE/ALLOCATE/REPORT (gói HD2 WP-C2…C5)",
  vao="sổ ITL đóng băng 23 kỳ + ảnh Manual input 2026-03 + kết quả 10 gói engine HD2",
  ra="ô `voi:theo_ky.*.{o_parity,hd_parity,o_go_that,o_mac_dinh}(_khop)` · `voi:khoi_theo_ky.*.*` · `voi:tu_sinh.*` · "
     "`hd2:<gói>.{khop,tong_o,lech_co_chu_dich}`",
  cong_cu="`final_7_khoi` · `vung_sua` · `tu_sinh` = `do_voi_so_luong.do()` (`final_rule.tinh_final` · `tu_soi.soi_mot_dong`) · "
          "`phan_bo_bao_cao` = số gói HD2 (`hd2_cong.json`, ghi bởi `tools/do_hd2.py`)",
  eval="`a3-2-luong` · `a3-3-nen-tang` (H1000 · nền tảng — PROPOSED)", the_eval=("a3-2-luong.md", "a3-3-nen-tang.md"),
  thong_minh="Hôm nay chép số engine. Đề xuất G0 (Voi roadmap 23/11): gợi ý ô vùng sửa khối 2 Loại GD + 7 Hoá đơn "
             "(ô máy ⛔ trả lời) — CHƯA dựng; cần ảnh Manual input 22 tháng."),
 "A4_AUDITOR": dict(
  hop="AP Voi v3.1.2 §4.4.1 KS.RI · KS.SI · KS.RP (PARTIAL)",
  vao="đầu ra A1–A3 + số máy đã đo (`voi_so_luong.json` · `hd2_cong.json` · đếm ảnh · cổng FLS)",
  ra="phán ĐẠT/TRƯỢT từng agent (MÃ) · ô `cong:HD1.*.dat` · `cong:HD2.*.dat` · `voi:dat_hd1.*` · `report.html`",
  cong_cu="`doi_chieu` (mã `fls/agent/doi_chieu.py`) · `cong_hd1` = `fls.repo.doc_bao_cao.doc_cong_tep_do` · "
          "`cong_hd2` = `doc_cong_hd2` · `report` (mã `fls/agent/report.py`)",
  eval="`a4-soat.eval.lot-chan` (chấm bằng họ khác: Claude Opus 5.5)", the_eval=("a4-soat.md",),
  thong_minh="MÃ THUẦN tới G1 (quyết chủ C2): phán và đọc cổng đều là mã, ⛔ lượt API. Đề xuất G0 (Voi 23/11–11/12): CHỈ THÊM cờ giải thích lệch, ⛔ bỏ cờ v0."),
}

CAM_CHUNG = ("⛔ gọi API thật khi thiếu chốt (`--that` + `FLS_CHO_GOI_API=1` + khoá + mô hình ghim)",
             "⛔ ghi kho · ⛔ sửa ảnh · ⛔ sửa engine/tuyến — chỉ GỌI công cụ được cấp",
             "⛔ tính lại / làm tròn / thêm ô / bịa ô — A4 so từng ô với máy",
             "⛔ gửi `Email Address` (`PM_COT_RIENG_TU`) — bộ che chạy trước mọi lời gọi; mặc định `mo` (chủ 23/11: nội dung · "
             "số TK · tên đi nguyên văn) ⇒ chạy thật đòi thêm chốt `FLS_ZDR_DA_BAT=1` (ZDR); `--che che_noi_dung`/`che_het` che lại")


def the(ag) -> str:
    v = VAI[ag.ma]
    bo = nap_bo(ag.ma)
    m = ag.mo_hinh
    dong = [f"# {ag.ten}", "",
            f"> Sinh bởi `python tools/sinh_the_agent.py` — ⛔ sửa tay (sửa prompt ở `fls/agent/skill/{ag.ma}/`, rồi sinh lại).",
            "", "| | |", "|---|---|",
            f"| **Vai** | {VAI[ag.ma]['hop']} |",
            f"| **Đầu vào** | {v['vao']} |",
            f"| **Đầu ra** | {v['ra']} |",
            f"| **Công cụ được gọi** *(CHỈ hàm FLS có sẵn)* | {v['cong_cu']} |",
            (f"| **Mô hình ghim** | `{m.ma}` · họ `{m.ho}` · {'ghim — **CHƯA gọi thật** (bản phát lại do mô hình GIẢ sinh)' if m.ghim else '**CHƯA ghim**'} · **phương án A — chủ chốt 23/11** |"
             if can_mo_hinh(ag.ma) else
             f"| **Mô hình** | **MÃ THUẦN tới G1** (quyết chủ C2) — ⛔ gọi mô hình, ⛔ dựng nhà cung cấp · dự kiến G1: `{m.ma}` họ `{m.ho}` "
             f"({'ghim' if m.ghim else 'CHƯA ghim'}) |"),
            "| **Dữ liệu & lưu giữ** *(chủ 23/11)* | agent đọc TOÀN BỘ nội dung giao dịch + số TK + tên (chỉ bỏ `Email Address`) · "
            "vận hành: Messages API dưới **ZDR** (bật theo tổ chức qua Anthropic) · fleet eval: **gửi theo lô** (Batches API — "
            "Anthropic giữ 29 ngày, đổi lấy −50 % giá; chủ chấp nhận) |",
            f"| **Phiên bản** | checksum prompt `{checksum_prompt(ag.ma)}` + mô hình ghim + checksum tham chiếu (tệp số máy đã đo) |",
            f"| **Bước thông minh** | {v['thong_minh']} |",
            f"| **Fleet eval** | {v['eval']} |",
            "", "## Bộ skill — chạy TUẦN TỰ (skill n+1 chỉ khi cổng skill n ĐẠT)", "",
            "| # | skill | loại | công cụ | cổng ra |", "|---|---|---|---|---|"]
    for s in bo:
        dong.append(f"| {s.so:02d} | [{s.ten}](../../../fls/agent/skill/{ag.ma}/{s.ma}.md) | {s.loai} | "
                    f"`{s.cong_cu}` | `{s.cong}` |")
    dong += ["", "Loại: `lam` = mô hình làm, A4 so 100 % với máy · `bong` = G0 bóng, so với đáp án giữ riêng, ⛔ ghi · "
             "`ma` = mã tất định, ⛔ mô hình.", "", "## Cổng ra của agent", "",
             "A4 (mã `fls/agent/doi_chieu.py`) so MỌI ô skill `lam` (và skill `ma` có công cụ) với số máy đã đo — mong: lệch 0 · ⛔ đo được 0 · "
             "thiếu 0 · thừa 0. Khác ⇒ agent TRƯỢT, chuỗi DỪNG, agent sau ⛔ chạy.", "", "## ⛔ Không được làm", ""]
    dong += [f"- {x}" for x in CAM_CHUNG]
    return "\n".join(dong) + "\n"


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--zip", action="store_true")
    a = p.parse_args(argv)
    TM.mkdir(parents=True, exist_ok=True)
    for ag in AGENT:
        (TM / f"{ag.ma}.md").write_text(the(ag), encoding="utf-8")
    if a.zip:
        tm_goi = TM / "goi"
        tm_goi.mkdir(exist_ok=True)
        for ag in AGENT:
            z = tm_goi / f"{ag.ma}.zip"
            with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as f:
                f.write(TM / f"{ag.ma}.md", f"{ag.ma}/00_THE_AGENT.md")
                for p_ in sorted((THU_MUC / ag.ma).glob("*.md")):
                    f.write(p_, f"{ag.ma}/skill/{p_.name}")
                pl = TM / "phat_lai" / f"{ag.ma}.json"
                if pl.exists():
                    f.write(pl, f"{ag.ma}/phat_lai/{pl.name}")
                for e in VAI[ag.ma]["the_eval"]:
                    f.write(EVAL / e, f"{ag.ma}/fleet_eval/{e}")
                if ag.ma == "A2_PR_MAP":
                    for p_ in sorted((GOC / "docs" / "ITL" / "05_FleetEval" / "vong").glob("*")):
                        f.write(p_, f"{ag.ma}/fleet_eval/vong/{p_.name}")
                if ag.ma == "A4_AUDITOR":
                    f.write(TM / "report.html", f"{ag.ma}/report.html")
            print(f"  {z.relative_to(GOC)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
