import unittest
import sys
import os

# Trỏ path ra thư mục implementation để import db
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import db

class TestDatabaseMCP(unittest.TestCase):
    
    def test_valid_search(self):
        """Test tìm kiếm hợp lệ trên bảng có thật"""
        results = db.search_data("students", "cohort", "A1")
        self.assertTrue(isinstance(results, list))
        
    def test_invalid_table(self):
        """Test chặn truy vấn vào bảng không tồn tại"""
        with self.assertRaises(ValueError) as context:
            db.search_data("hackers")
        self.assertTrue("does not exist" in str(context.exception))

    def test_sql_injection_column(self):
        """Test chặn SQL Injection qua việc điền tên cột bậy bạ"""
        with self.assertRaises(ValueError) as context:
            db.search_data("students", "1=1; DROP TABLE students;", "1")
        self.assertTrue("does not exist in table" in str(context.exception))

    def test_invalid_aggregate(self):
        """Test chặn hàm aggregate không được phép"""
        with self.assertRaises(ValueError) as context:
            db.aggregate_data("students", "*", "DELETE")
        self.assertTrue("Unsupported aggregate function" in str(context.exception))

    def test_schema_generation(self):
        """Test resource schema được tạo đúng"""
        schema = db.get_database_schema()
        self.assertTrue("CREATE TABLE students" in schema)

if __name__ == '__main__':
    unittest.main()
