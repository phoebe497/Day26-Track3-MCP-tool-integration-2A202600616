import asyncio
import sys
import json

# Chống lỗi font chữ tiếng Việt trên Windows
sys.stdout.reconfigure(encoding='utf-8')

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    # Khởi động server thông qua subprocess (stdio)
    params = StdioServerParameters(command=sys.executable, args=["mcp_server.py"])

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            print("=== 1. TESTING RESOURCES (Schema) ===")
            res = await session.read_resource("schema://table/students")
            print(res.contents[0].text)
            print("-" * 40)

            print("=== 2. TESTING TOOLS (Valid Requests) ===")
            
            # 2.1 Search
            print("\n[+] Action: Search all students in cohort 'A1'")
            res = await session.call_tool("search", {"table": "students", "filter_col": "cohort", "filter_val": "A1"})
            print("Result:", res.content[0].text)

            # 2.2 Insert
            print("\n[+] Action: Insert a new student")
            insert_data = json.dumps({"name": "Phan Thi E", "cohort": "A4"})
            res = await session.call_tool("insert", {"table": "students", "data_json": insert_data})
            print("Result:", res.content[0].text)

            # 2.3 Aggregate
            print("\n[+] Action: Aggregate COUNT students")
            res = await session.call_tool("aggregate", {"table": "students", "column": "*", "func": "COUNT"})
            print("Result:", res.content[0].text)

            print("\n=== 3. TESTING TOOLS (Invalid Requests / Security) ===")
            
            # 3.1 Invalid table
            print("\n[-] Action: Search on missing table 'hackers'")
            res = await session.call_tool("search", {"table": "hackers"})
            print("Result:", res.content[0].text)

            # 3.2 SQL Injection attempt (Invalid column)
            print("\n[-] Action: SQL Injection attempt on column name")
            res = await session.call_tool("search", {"table": "students", "filter_col": "1=1; DROP TABLE students;", "filter_val": "1"})
            print("Result:", res.content[0].text)
            
            # 3.3 Invalid aggregate function
            print("\n[-] Action: Invalid aggregate function")
            res = await session.call_tool("aggregate", {"table": "students", "column": "name", "func": "DELETE"})
            print("Result:", res.content[0].text)

if __name__ == "__main__":
    asyncio.run(main())
