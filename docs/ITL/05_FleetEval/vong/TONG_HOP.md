# Fleet eval nhiều vòng — A2.04 ghép theo nội dung · 2026-11-23

Bể: **ca DỰNG trong repo (⛔ dữ liệu thật)** · `12` ca · checksum bể `7bf678fcb945d5cc` · sinh bởi `python tools/fleet_eval_voi.py --ghi` (⛔ sửa tay).

⚠ Mọi vòng dưới đây chạy mô hình **GIẢ** trên bể **DỰNG** — chạy thử bộ máy, ⛔ số đo mô hình thật.

| vòng | phiên bản | nối | sai | tỉ lệ nối sai | recall phải-nối | ca phải-để-người bị nối | điểm TB (0–2) | phán |
|---|---|---|---|---|---|---|---|---|
| 1 | `v0-ma-tat-dinh` | 0 | 0 | None | 0.0 | 0 | 1.4167 | ĐẠT bar |
| 2 | `v1-gia-tat-noi-dung` | 2 | 0 | 0.0 | 0.2857 | 0 | 1.5833 | ĐẠT bar |
| 3 | `v1-gia-bat-noi-dung` | 6 | 0 | 0.0 | 0.8571 | 0 | 1.9167 | ĐẠT bar |

Heatmap đơn vị × phiên bản (điểm TB 0–2):

| đơn vị | `v0-ma-tat-dinh` | `v1-gia-tat-noi-dung` | `v1-gia-bat-noi-dung` |
|---|---|---|---|
| phai_noi | 1.0 | 1.2857 | 1.8571 |
| phai_nguoi | 2.0 | 2.0 | 2.0 |
