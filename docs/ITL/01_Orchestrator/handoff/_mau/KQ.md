# KQ-NNN — biên bản kiểm `BG-NNN`

| | |
|---|---|
| **Thuộc** | `BG-NNN` · `WO-NNN` |
| **Kiểm bởi** | `fls-test` · YYYY-MM-DD |
| **Phán quyết** | `ĐẠT` / `TRƯỢT` / `⛔ KHÔNG ĐO ĐƯỢC` *(tính như TRƯỢT)* |

## Cổng chạy lại *(Test tự chạy — so với `BG`)*
| Lệnh | `BG` nói | Test đo | Khớp |
|---|---|---|:-:|
| `python -m pytest` | … | … | ✅/⛔ |

## Bảng AC
| AC | Mong | Đo được *(có nhãn · mẫu số)* | Phán quyết |
|---|---|---|---|
| AC-1 | … | … | ĐẠT / TRƯỢT / ⛔ KHÔNG ĐO ĐƯỢC |

## Ba lăng kính
| Lăng kính | Kết luận | Căn cứ |
|---|---|---|
| **Logic** *(spec + bất biến `BA-11`)* | … | … |
| **Dữ liệu** *(kho thật, chỉ đọc)* | … | `SQL …` ⇒ `…` |
| **Màn hình** *(trạng thái · thiết kế · phím · NFR)* | … | … |

## Phát hiện
| F | Mức | Nơi | Tái hiện | Gửi |
|---|---|---|---|---|
| F-1 | `CHAN` / `NANG` / `NHE` | `<tệp:dòng>` / `<màn + thao tác>` | … | `DEV` / `BA` |

## Bài thử mới *(`tests/nghiem_thu/`)*
| Bài | Đã chứng minh ĐỎ bằng cách | Xanh sau |
|---|---|---|
| `tests/nghiem_thu/…::…` | … | ✅ |
