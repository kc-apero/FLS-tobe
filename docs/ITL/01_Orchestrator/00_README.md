# 00 — README: Orchestrator Kit ITL (lớp điều phối)

**Dự án:** ITL — Input Transaction Ledger (P100 → ITL Ledge) | **Phiên bản bộ:** v0.1 | **Chủ sở hữu (Orchestrator/PO):** COO-CFO

Bộ này đứng TRÊN ba bộ kia (BA / Dev / Testing) và điều phối chúng. Ba bộ kia trả lời *cái gì, như thế nào, đúng chưa*; bộ này trả lời *khi nào, theo thứ tự nào, ai chốt, phiên bản nào khớp phiên bản nào*. Nó là bộ nhớ trạng thái và luật chơi của dự án — thứ mà mỗi phiên AI (vốn không nhớ gì giữa các lần) không tự giữ được.

Quy ước tham chiếu: `BA-xx`, `DEV-xx`, `TEST-xx` = file trong ba bộ tương ứng; số trần (`01`) = file nội bộ bộ này. Bộ tài liệu ITL **độc lập** với bộ chương trình FIN ERP (`QĐ-ITL-04`) — xem `../00_MASTER_INDEX.md` §5 về chốt kế thừa.

---

## 1. Cấu trúc bộ (8 file)

| File | Vai trò |
|---|---|
| `01_PRINCIPLES.md` | Hiến pháp dự án — nguyên tắc điều phối bất biến, ưu tiên cao hơn mọi bộ khác |
| `02_VERSION_ORCHESTRATION.md` | Giữ version đồng bộ; **trục chính = ITL Ledge Output Contract**; giao thức đóng băng; manifest mỗi `IM` |
| `03_PRODUCT_LIFECYCLE.md` | `IM0–IM7` + cổng chuyển milestone (cổng = **đối soát với oracle**, không phải "ship xong") |
| `04_DEVELOPMENT_LOOP.md` | Vòng lặp phát triển — vòng ngoài theo milestone, vòng trong **theo adapter** |
| `05_ROLES_HANDOFF.md` | Vai trò, RACI, hợp đồng bàn giao giữa các phiên AI; **ranh giới AS-IS đang là con người** |
| `06_ORCHESTRATOR_DASHBOARD.md` | Bảng điều khiển duy nhất: trạng thái, version, GAP, cổng |
| `07_CHANGE_CONTROL.md` | Quy trình một thay đổi từ lúc phát sinh tới lúc lan hết ba bộ; 4 loại thay đổi |
| `08_MIGRATION_ROADMAP.md` | Bản đồ di trú `Brainstorming/` + `AS-IS system/` vào kit này |

## 2. Mô hình điều phối cốt lõi

```
                 ┌──────────────────────────────────┐
                 │   ORCHESTRATOR (bộ này)          │
                 │ giữ trạng thái + luật + version  │
                 └───────────────┬──────────────────┘
        điều phối / cổng         │        báo cáo trạng thái
      ┌──────────────┬───────────┼────────────┬─────────────────┐
      ▼              ▼           ▼            ▼                 ▼
   BA Kit    →    Dev Kit  →  Testing Kit →  cutover IM7   →  Operate
   (spec)        (build)      (verify)       engine trỏ        (DAG tự
                                             ITL mới,          chạy, còn
                                             sổ Gsheet         maker-checker)
                                             ngưng
```

**Khác chương trình FIN ERP hai điểm:**

1. **Cổng không phải "release" mà là "khớp oracle".** Dự án này có lợi thế hiếm: `ITL RAW` và `ITL ADJUSTED` cũ vẫn tồn tại ⇒ mọi milestone nghiệm thu bằng **đối chiếu từng dòng với sổ thật**, không phải "tin là đúng". Xem `03` §3.
2. **Cổng cuối là cutover có điều kiện lùi được.** Sổ Gsheet chuyển read-only rồi mới ngưng, **không xoá ngay** — giữ để check chéo (`03` IM7).

## 3. Ba nguyên lý nền (chi tiết trong `01`)

- **Contract-first.** Việc số 0 là đóng băng hợp đồng đầu ra của `ITL Ledge`; mọi milestone sau khớp hợp đồng đó ⇒ ngày cutover engine không phải sửa dòng code nào (`P-ITL-01`).
- **Con người giữ trạng thái, AI làm công việc.** Trạng thái dự án sống trong `06`, không sống trong hội thoại (`P-07`).
- **Mọi cổng đều là human gate** — người gác cổng nghiệm thu là **người vận hành** (kế toán trưởng, PIC vùng ADJUSTMENT, thủ quỹ), không phải team build (`P-02`).

## Changelog
- v0.1 (2026-08-18): Khởi tạo cho dự án ITL — thay toàn bộ nội dung bản copy chương trình; Orchestrator 8 file (thêm `08_MIGRATION_ROADMAP`).
