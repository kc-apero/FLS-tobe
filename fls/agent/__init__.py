# -*- coding: utf-8 -*-
"""Gói agent VẬN HÀNH Voi (`WO-329`) — 4 agent gọi API: A1 RI · A2 PR + SI.MAP · A3 SI.ITL · A4 Auditor.

⭐ Bản đồ (đọc thẻ trước: `docs/ITL/06_Agent/A1_RI.md` … `A4_AUDITOR.md`):
  che.py        bộ che `NFR-I13` — DANH SÁCH TRẮNG, chạy TRƯỚC mọi lời gọi mô hình
  mo_hinh.py    giao diện nhà cung cấp (⛔ cứng một hãng) · PHÁT LẠI (mặc định) · GIẢ · THẬT có chốt ba lớp
  skill.py      đọc bộ skill có số thứ tự (`fls/agent/skill/<agent>/NN_*.md`), checksum prompt
  cong_skill.py cổng ra của từng skill (khai `mong`, Đ5)
  doi_chieu.py  phép so ô agent ↔ máy đã đo (lõi tất định của A4)
  chuoi.py      chạy A1 → A2 → A3 → A4; skill n+1 chỉ khi cổng n ĐẠT; agent k+1 chỉ khi A4 cho k ĐẠT
  report.py     report MỘT trang HTML tĩnh

⛔ Gói này ⛔ biết kho (`psycopg` · `fls.db` · `fls.repo`) và ⛔ biết tuyến (`fls.api` · `fls.web`):
   công cụ FLS mà agent gọi được TIÊM vào từ `tools/chay_agent_voi.py` — y khuôn `conn` của `fls.api`.
   Canh bởi `.importlinter` hợp đồng 1 (psycopg) + `tests/agent/test_tang_agent.py` (fls.db/repo/api/web).
"""
