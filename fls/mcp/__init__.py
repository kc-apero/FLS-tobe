"""Cổng MCP của FLS — tài khoản Claude của CHỦ đọc kho qua giao thức MCP (`WO-371`).

⭐ Vì sao là MỘT gói trong `fls/` *(⛔ `tools/mcp_fls/`)*: nó dùng lại ĐÚNG các tuyến ĐỌC của cửa
`fls.api` *(`goi_tuyen` gọi `fls.api.xu_ly.HAM` — ⛔ viết lại logic)*, nên nó là một TẦNG như `fls.api`
và phải chịu cùng luật tầng: `import-linter` hợp đồng 1 *(⛔ `psycopg`)* + bài AST
`tests/mcp/test_mcp_tang.py` *(⛔ `fls.db` · `fls.repo` · `fls.web`)*. Kết nối kho được TRUYỀN VÀO
từ `tools/chay_mcp.py` — y khuôn `tools/chay_cua.py` ↔ `fls.api.cua`.

Ba mô-đun:
  `chan_sql`  — lớp chặn ỨNG DỤNG cho `truy_van_doc` (thuần, ⛔ kho).
  `cong_cu`   — lõi công cụ CHỈ ĐỌC + lớp chặn KHO (giao dịch READ ONLY · `statement_timeout` · trần dòng)
                + nhật ký + trần tốc độ.
  `xac_thuc`  — máy chủ uỷ quyền OAuth 2.1 của chính FLS, đăng nhập uỷ cho Google, danh sách cho phép.
  `may_chu`   — ráp `MCPServer` (SDK `mcp` 2.x): stdio *(Claude Code cục bộ)* + Streamable HTTP *(connector claude.ai)*.
"""
