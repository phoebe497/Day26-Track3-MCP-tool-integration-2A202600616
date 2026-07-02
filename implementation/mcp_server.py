from mcp.server.fastmcp import FastMCP
import json
import db

# Khởi tạo FastMCP server
mcp = FastMCP("sqlite-lab")

# ==========================================
# RESOURCES (Bối cảnh cho AI)
# ==========================================

@mcp.resource("schema://database")
def get_db_schema() -> str:
    """Provides the full database schema."""
    return db.get_database_schema()

@mcp.resource("schema://table/{table_name}")
def get_table_schema(table_name: str) -> str:
    """Provides the schema for a specific table."""
    return db.get_table_schema(table_name)

# ==========================================
# TOOLS (Hành động cho AI)
# ==========================================

@mcp.tool()
def search(table: str, filter_col: str = None, filter_val: str = None) -> str:
    """Search for records in a database table with an optional filter.
    
    Args:
        table: Name of the table (e.g., 'students')
        filter_col: Optional column name to filter by
        filter_val: Optional value to match the filter column
    """
    try:
        results = db.search_data(table, filter_col, filter_val)
        return json.dumps(results, indent=2, ensure_ascii=False)
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def insert(table: str, data_json: str) -> str:
    """Insert a new record into a table.
    
    Args:
        table: Name of the table (e.g., 'students')
        data_json: A JSON string representing the dictionary of data to insert (e.g., '{"name": "Alice", "cohort": "A1"}')
    """
    try:
        # Chuyển đổi JSON string thành Python Dictionary vì MCP truyền dữ liệu qua JSON text
        data = json.loads(data_json)
        return db.insert_data(table, data)
    except json.JSONDecodeError:
        return "Error: data_json must be a valid JSON string."
    except Exception as e:
        return f"Error: {str(e)}"

@mcp.tool()
def aggregate(table: str, column: str, func: str) -> str:
    """Calculate an aggregate function on a table column.
    
    Args:
        table: Name of the table
        column: Name of the column (use '*' for COUNT)
        func: The aggregate function to use (COUNT, AVG, SUM, MIN, MAX)
    """
    try:
        result = db.aggregate_data(table, column, func)
        return f"{func}({column}) on {table} = {result}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    # Khởi chạy server qua stdio (mặc định)
    mcp.run()
