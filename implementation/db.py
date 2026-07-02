import sqlite3
import os
from typing import Dict, List, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "university.db")

def get_connection():
    # SQLite returns row results as dictionaries when using Row factory
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def validate_table(cursor: sqlite3.Cursor, table_name: str) -> bool:
    """Kiểm tra bảng có tồn tại trong CSDL không."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    return cursor.fetchone() is not None

def validate_columns(cursor: sqlite3.Cursor, table_name: str, columns: List[str]) -> bool:
    """Kiểm tra các cột có tồn tại trong bảng không."""
    cursor.execute(f"PRAGMA table_info({table_name})") # Safe vì table_name đã được validate trước đó
    valid_columns = [row["name"] for row in cursor.fetchall()]
    return all(col in valid_columns for col in columns)

def search_data(table: str, filter_col: Optional[str] = None, filter_val: Any = None) -> List[Dict[str, Any]]:
    """Tìm kiếm an toàn với filter."""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Validation bảo mật (Chống SQL Injection)
        if not validate_table(cursor, table):
            raise ValueError(f"Table '{table}' does not exist.")
            
        if filter_col:
            if not validate_columns(cursor, table, [filter_col]):
                raise ValueError(f"Column '{filter_col}' does not exist in table '{table}'.")
            
            # Parametrized query
            query = f"SELECT * FROM {table} WHERE {filter_col} = ?"
            cursor.execute(query, (filter_val,))
        else:
            query = f"SELECT * FROM {table}"
            cursor.execute(query)
            
        return [dict(row) for row in cursor.fetchall()]

def insert_data(table: str, data: Dict[str, Any]) -> str:
    """Thêm dòng mới vào bảng an toàn."""
    if not data:
        raise ValueError("Insert data cannot be empty.")
        
    with get_connection() as conn:
        cursor = conn.cursor()
        
        if not validate_table(cursor, table):
            raise ValueError(f"Table '{table}' does not exist.")
            
        columns = list(data.keys())
        if not validate_columns(cursor, table, columns):
            raise ValueError(f"One or more columns do not exist in table '{table}'.")
            
        placeholders = ", ".join(["?"] * len(columns))
        col_names = ", ".join(columns)
        values = tuple(data.values())
        
        query = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
        cursor.execute(query, values)
        conn.commit()
        return f"Successfully inserted 1 row into '{table}' with ID: {cursor.lastrowid}"

def aggregate_data(table: str, column: str, agg_func: str) -> float:
    """Tính toán aggregate an toàn (COUNT, AVG, SUM, MIN, MAX)."""
    allowed_funcs = ["COUNT", "AVG", "SUM", "MIN", "MAX"]
    agg_func = agg_func.upper()
    
    if agg_func not in allowed_funcs:
        raise ValueError(f"Unsupported aggregate function: {agg_func}")
        
    with get_connection() as conn:
        cursor = conn.cursor()
        
        if not validate_table(cursor, table):
            raise ValueError(f"Table '{table}' does not exist.")
            
        if column != "*" and not validate_columns(cursor, table, [column]):
            raise ValueError(f"Column '{column}' does not exist in table '{table}'.")
            
        query = f"SELECT {agg_func}({column}) as result FROM {table}"
        cursor.execute(query)
        row = cursor.fetchone()
        return row["result"] if row and row["result"] is not None else 0.0

def get_database_schema() -> str:
    """Lấy DDL schema của toàn bộ database làm Resource context."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name, sql FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = cursor.fetchall()
        
        schema = "Database Schema:\n\n"
        for row in tables:
            schema += f"-- Table: {row['name']}\n{row['sql']}\n\n"
        return schema

def get_table_schema(table: str) -> str:
    """Lấy schema của một bảng cụ thể làm Resource context."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name=?", (table,))
        row = cursor.fetchone()
        
        if not row:
            return f"Error: Table '{table}' not found."
            
        return f"-- Schema for {table}:\n{row['sql']}"
