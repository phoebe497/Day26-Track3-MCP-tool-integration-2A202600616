# Database MCP Server using FastMCP and SQLite (Lab 26 - Track 3)

## 🎯 Overview
This project implements a FastMCP server that connects to a SQLite database. It securely exposes database schemas as MCP resources and provides tools for interacting with the data. 

**Mục tiêu đạt được**: Server cung cấp cầu nối cho các AI (Claude, Gemini, Antigravity) hiểu được cấu trúc Database và thực thi các lệnh CRUD một cách an toàn, chống 100% rủi ro SQL Injection.

---

## 🛠️ Features & Tools

### 1. Context Resources (Cung cấp bối cảnh cho AI)
- `schema://database`: Trả về toàn bộ DDL (cấu trúc bảng) của Database.
- `schema://table/{table_name}`: Trả về DDL của một bảng cụ thể.

### 2. Action Tools (Công cụ hành động)
- **`search(table, filter_col, filter_val)`**: Truy vấn dữ liệu có điều kiện.
- **`insert(table, data_json)`**: Thêm một dòng dữ liệu mới vào bảng thông qua chuỗi JSON.
- **`aggregate(table, column, func)`**: Thực hiện các phép toán tổng hợp (`COUNT`, `SUM`, `AVG`, `MIN`, `MAX`).

### 3. Security (Bảo mật)
- **Zero SQL Injection**: Mọi tham số đầu vào (tên bảng, tên cột) đều được đối chiếu (validate) trực tiếp với `sqlite_master` và `PRAGMA table_info` trước khi ghép vào chuỗi SQL. Bất kỳ cột/bảng lạ nào cũng bị từ chối ngay lập tức.

---

## 🚀 Setup Instructions

1. **Khởi tạo môi trường ảo và cài thư viện**:
```bash
uv venv
uv pip install mcp fastmcp pydantic
```

2. **Khởi tạo Database và nạp Seed Data**:
```bash
cd implementation
..\.venv\Scripts\python init_db.py
```
Lệnh này sẽ tạo ra file `university.db` với 3 bảng: `students`, `courses`, `enrollments` kèm dữ liệu mẫu.

---

## 🧪 Testing & Verification

Dự án cung cấp 3 cách để kiểm thử tính năng và bảo mật:

### Cách 1: Automated Script Test (E2E)
Chạy script tự động (gọi Server qua luồng stdio) để test cả tác vụ đúng lẫn các nỗ lực tấn công phá hoại:
```bash
cd implementation
..\.venv\Scripts\python verify_server.py
```

### Cách 2: Security Unit Tests
Chạy bộ Unit Test chuyên dụng để kiểm tra lớp Database Layer (`db.py`):
```bash
cd implementation
..\.venv\Scripts\python -m unittest tests/test_server.py
```

### Cách 3: MCP Inspector (UI)
Sử dụng công cụ Inspector của giao thức MCP để test trực quan trên trình duyệt:
```bash
cd implementation
npx @modelcontextprotocol/inspector ..\.venv\Scripts\python mcp_server.py
```

---

## 🤖 Client Configuration Example

### 1. Gemini CLI
Để kết nối MCP Server này vào Gemini CLI, chạy lệnh sau (nhớ thay bằng đường dẫn tuyệt đối trên máy bạn):
```bash
gemini mcp add sqlite-lab /ABSOLUTE/PATH/TO/.venv/Scripts/python /ABSOLUTE/PATH/TO/implementation/mcp_server.py --timeout 10000
```
Sau đó kiểm tra danh sách Tool:
```bash
gemini mcp list
```

### 2. Claude Code
Thêm cấu hình sau vào file `.mcp.json` của Claude:
```json
{
  "mcpServers": {
    "sqlite-lab": {
      "command": "/ABSOLUTE/PATH/TO/.venv/Scripts/python",
      "args": ["/ABSOLUTE/PATH/TO/implementation/mcp_server.py"]
    }
  }
}
```

---
*Hoàn thành bởi: Nguyễn Như Yến Phương - 2A202600616*