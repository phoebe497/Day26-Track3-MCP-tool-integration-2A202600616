import sqlite3
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

DB_PATH = os.path.join(os.path.dirname(__file__), "university.db")

def init_db():
    print(f"Khởi tạo cơ sở dữ liệu tại: {DB_PATH}")
    
    # Xoá db cũ nếu tồn tại để reset
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tạo bảng students
    cursor.execute('''
        CREATE TABLE students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            cohort TEXT NOT NULL
        )
    ''')

    # Tạo bảng courses
    cursor.execute('''
        CREATE TABLE courses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            credits INTEGER NOT NULL
        )
    ''')

    # Tạo bảng enrollments
    cursor.execute('''
        CREATE TABLE enrollments (
            student_id INTEGER NOT NULL,
            course_id INTEGER NOT NULL,
            score REAL,
            FOREIGN KEY(student_id) REFERENCES students(id),
            FOREIGN KEY(course_id) REFERENCES courses(id),
            PRIMARY KEY(student_id, course_id)
        )
    ''')

    # Chèn dữ liệu mẫu (Seed Data)
    students_data = [
        ("Nguyễn Khánh An", "A1"),
        ("Trần Ngọc Linh", "A1"),
        ("Lê Văn Cương", "A2"),
        ("Hoàng Kim Anh", "A3"),
    ]
    cursor.executemany("INSERT INTO students (name, cohort) VALUES (?, ?)", students_data)

    courses_data = [
        ("Python Basics", 3),
        ("Machine Learning", 4),
        ("Database Systems", 3),
    ]
    cursor.executemany("INSERT INTO courses (title, credits) VALUES (?, ?)", courses_data)

    enrollments_data = [
        (1, 1, 9.5), # Nguyễn Khánh An học Python (9.5)
        (1, 3, 8.0), # Nguyễn Khánh An học Database (8.0)
        (2, 1, 7.5), # Trần Ngọc Linh học Python (7.5)
        (3, 2, 8.5), # Lê Văn Cương học Machine Learning (8.5)
    ]
    cursor.executemany("INSERT INTO enrollments (student_id, course_id, score) VALUES (?, ?, ?)", enrollments_data)

    conn.commit()
    conn.close()
    print("Khởi tạo và nạp dữ liệu thành công! ✅")

if __name__ == "__main__":
    init_db()
