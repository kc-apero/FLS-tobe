# 05 — ROLES & HANDOFF: vai trò, RACI, hợp đồng bàn giao

**Version:** v0.2 | **Chủ sở hữu:** COO-CFO

---

## 1. Vai trò con người (nghiệp vụ)

| Vai | Người | Trách nhiệm trong dự án ITL |
|---|---|---|
| Orchestrator / PO | COO-CFO (kiêm) | Giữ trạng thái, quyết cổng, chủ trì value review |
| Diễn đàn quản trị | CEO chủ trì + COO + CFO + đại diện BU luân phiên | Duyệt CR chạm hợp đồng/chạm tiền, phân xử tranh chấp |
| Org master data owner | **ThanhNC** | Duy trì danh mục tổ chức (LE/CDT/HD) — một cửa duy nhất; ký `MAPPING-MASTER` |
| Kế toán trưởng | `???` | Nghiệm thu `IM1`, `IM2`, `IM5`, `IM6`, `IM7`; ký chốt số; có quyền từ chối ký kèm lý do |
| Thủ quỹ | `???` | Nghiệm thu `IM2` (đối soát tiền, balance theo ngày/tài khoản) |
| PIC vùng ADJUSTMENT | **Lan · Thương** (`OP-07`, `OP-08`) | Chủ hiện tại của ~6.843 dòng nhập tay; nghiệm thu `IM6`; là người biết *lý do* mỗi khối điều chỉnh — nguồn tri thức không nằm trong file nào |
| HR C&B owner (H1000) | `???` | Nghiệm thu `IM3` |
| Chủ sở hữu báo cáo platform | `???` | Nghiệm thu `IM4` |
| Tech Lead | `???` (AI-assisted) | Sở hữu `ITL-CONTRACT`; reverse-engineer reader engine; nghiệm thu `IM0` |

> 5 ô `???` là **quyết định của con người** (R-A1). Không phiên AI nào được tự điền tên vào.
>
> ✅ **Tên đã xác định được từ bằng chứng trong file** (G6, `_GUIDE_09`): **ThomHT · AnhMC** nạp sổ bank trước 11h · **LAN · THƯƠNG** vùng ADJUSTMENT · **ThuongCT** kiểm kê & ký quỹ cuối tháng · **Hoài** giữ script cập nhật. Đây là *người đang làm việc đó*, **chưa phải** người được chỉ định vai chính thức — vẫn cần owner xác nhận.

## 2. Ranh giới hệ thống AS-IS đang là **con người** — và phải thay bằng interface

`NGUỒN-ASIS` §04 chỉ ra một điểm yếu ít ai để ý: trong luồng hiện tại, ranh giới giữa các hệ thống **không phải interface mà là người bàn giao cho người**. Đây là bảng phải khai báo rồi thay dần — mỗi dòng là một nợ kiến trúc.

| Mắt xích AS-IS do người giữ | Hiện trạng | TO-BE thay bằng | IM |
|---|---|---|---|
| Data → nhập/kéo dữ liệu nguồn (**ThomHT, AnhMC** — nạp sổ bank **trước 11h**) | thao tác tay + Importrange | Adapter A–E, node DAG idempotent | IM1–IM4 |
| SHQ1 / SHQ2 → chuẩn hoá & mapping | Gscript + tay | `MAPPING-MASTER` versioned + engine áp luật | IM1, IM6 |
| HR → ledger lương + allocate | file 108 sheet, audit balance còn `Doing` | Adapter D + audit balance tự động | IM3 |
| Lan · Thương → vùng ADJUSTMENT | ~6.843 dòng gõ tay | Bút toán có luật (phần suy được) + UI maker-checker (phần không suy được) | IM6 |
| Kế toán → "nhấn nút" chạy bước (**Hoài** giữ script; `0. CCR Flow-use` có 2 bước `Run`) | 62% bước (72/116) là thao tác tay/Gscript | DAG có thứ tự, tự chạy theo lịch | IM7 |
| Thủ quỹ → kiểm kê + **ký xác nhận quỹ** ngày cut-off (**ThuongCT**) | biên bản chốt quỹ/tháng, lưu PDF | vẫn là người ký — nhưng số liệu tự lên | IM2 |

**Luật:** mỗi milestone phải nêu rõ nó **xoá mắt xích người nào**. Milestone không xoá được mắt xích nào là milestone đáng nghi (`P-02`).

## 3. Vai trò phiên AI (kỹ thuật)

| Vai phiên | Input bắt buộc | Output | Cấm |
|---|---|---|---|
| BA session | `NGUỒN-*` + file BA liên quan | Spec điền, `GAP_REPORT` | Tự điền `???` |
| Dev session | `BA-05`, `BA-09`, `BA-10`, `BA-11` + 1 task từ `DEV-03` | Code + test + changelog | Làm quá 1 task; chế spec thiếu |
| Test session | Spec + `TEST-01..02` | Test case/code test | Sửa test cho pass |
| Critic session | Spec + test case, **KHÔNG xem code** | `GAP_REPORT` | Xem code; đóng GAP |
| Reviewer session | Diff + spec | Findings | Tự sửa code |

## 4. RACI rút gọn

| Việc | R | A | C | I |
|---|---|---|---|---|
| `ITL-CONTRACT` (hợp đồng đầu ra) | Tech Lead | **COO-CFO** | Kế toán trưởng | Diễn đàn QT |
| `ITL-CANON` (36 cột canonical) | BA session + Tech Lead | COO-CFO | Kế toán trưởng | — |
| `MAPPING-MASTER` (reference data) | Người nghiệp vụ (SHQ1/SHQ2) | **ThanhNC** | Kế toán trưởng | Toàn đội |
| Luật vùng ALLOCATE | CFO chuẩn bị | **Diễn đàn QT** | PIC ADJUSTMENT | Toàn công ty |
| Chốt spec BA từng IM | BA session + COO-CFO | COO-CFO | Kế toán trưởng | Diễn đàn QT |
| Nghiệm thu từng IM | Team build | **Người vận hành** (`03` §2) | COO-CFO | Diễn đàn QT |
| Cutover `IM7` | Team build | **Kế toán trưởng + COO-CFO** | Tech Lead | Toàn công ty |

## 5. Hợp đồng bàn giao giữa phiên AI

Mỗi handoff ghi vào `06` dạng: `[ngày] [vai phiên] [task] [input version] [output + đường dẫn] [GAP mở]`.

Phiên sau đọc `06` + file được trỏ, **không đọc lại hội thoại phiên trước** (`P-07`).

**Trước khi tin một handoff — 3 việc bắt buộc verify:**
1. Trạng thái git/file thật (branch nào, commit nào, file có tồn tại không).
2. Version của 3 hợp đồng đang hiệu lực (`02` §3) — code cũ đọc hợp đồng cũ là lỗi âm thầm.
3. Nếu handoff nói "đã chạy/đã khớp": xem lại **brick/run id** cụ thể, không tin câu chữ.

## Changelog
- v0.2 (2026-08-18): Bổ sung tên người thực thi lấy từ bằng chứng file (G6): ThomHT/AnhMC · LAN/THƯƠNG · ThuongCT · Hoài. Thêm 1 mắt xích người vào §2.
- v0.1 (2026-08-18): Khởi tạo — thêm §2 bảng "ranh giới hệ thống đang là con người" (5 mắt xích) làm nợ kiến trúc phải xoá theo milestone; RACI đổi trục sang 3 hợp đồng. 5 ô `???` chờ chỉ định nhân sự.
