# ap-src — bộ sinh Architecture Pack FLS

Sinh `docs/architecturepack_FLS_v<N>_*.html` theo khuôn build-ap (§A.1–§A.18, FIN-ERP authoring-kit).

- `apgen.py` — shell (CSS/JS lấy **nguyên văn** từ AP FPA-T4 qua đường dẫn `FPA` ở đầu tệp), mục lục có chấm trạng thái, `data-st` + băm thân mục, §0.B sinh tự động, tiện ích bảng (`T` bắt buộc colgroup = 100 %).
- `c_s0.py … c_s9_13.py` — nội dung từng §; `HEADER_ROWS` ở `c_s0.py`.
- `erd7tang_static.svg` — SVG 7 tầng từ `Ban-do-Kien-truc-7-Tang.html`, biến màu đổi sang bảng màu tài liệu.
- `build.py` — dựng + cổng cấu trúc (class CSS chưa định nghĩa, colgroup, tag). Đường ra `OUT` tuyệt đối — đổi khi bump version.

Chạy (Windows):

```
cd docs/ap-src
PYTHONUTF8=1 PYTHONIOENCODING=utf-8 python build.py
PYTHONUTF8=1 python ../ap-status-check.py ../architecturepack_FLS_v1.0.0_current-state_2026-09-17.html
```

Luật §A.16: mỗi lần sửa nội dung là **một tệp mới** (bump version trong `HEADER_ROWS`, `build.py::OUT`, `title`); tệp cũ đóng băng. Diff hash từng mục giữa hai bản bằng `units()` của `ap-status-check.py`.

Trạng thái `approved` chỉ chủ sở hữu đặt: `python ../ap-status-check.py <AP> --stamp s7-5=approved`.
