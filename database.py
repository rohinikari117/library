import sqlite3
from werkzeug.security import generate_password_hash
from datetime import datetime

DATABASE = 'library.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    
    # Users Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            is_admin BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    
    # Books Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            regulation TEXT NOT NULL,
            branch TEXT NOT NULL,
            year INTEGER NOT NULL,
            semester INTEGER NOT NULL,
            type TEXT NOT NULL,
            file_path TEXT,
            description TEXT,
            cover_image TEXT
        )
    ''')
    
    # IssuedBooks Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS issued_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            issue_date DATE NOT NULL,
            return_date DATE,
            status TEXT NOT NULL DEFAULT 'Issued',
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    # Bookmarks Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS bookmarks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')
    
    # Reviews Table
    c.execute('''
        CREATE TABLE IF NOT EXISTS reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            book_id INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            review_text TEXT,
            date_posted DATE NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (book_id) REFERENCES books (id)
        )
    ''')

    # Add default admin if not exists
    c.execute("SELECT * FROM users WHERE email = 'admin@college.edu'")
    admin = c.fetchone()
    if not admin:
        hashed_pw = generate_password_hash('admin123')
        c.execute("INSERT INTO users (name, email, password, is_admin) VALUES (?, ?, ?, ?)",
                  ('Admin User', 'admin@college.edu', hashed_pw, 1))

    # Add sample books if empty
    c.execute("SELECT COUNT(*) as count FROM books")
    if c.fetchone()['count'] == 0:
        sample_books = [
            ('Data Structures', 'Mark Allen Weiss', 'R20', 'CSE', 2, 3, 'Textbook', '', 'Comprehensive guide to DS', ''),
            ('Electronic Devices', 'Boylestad', 'R20', 'ECE', 2, 3, 'Textbook', '', 'Intro to electronics', ''),
            ('Python Programming', 'John Zelle', 'R23', 'CSE', 1, 1, 'Textbook', '', 'Beginner friendly python', ''),
            ('Digital Logic Design', 'Morris Mano', 'R20', 'CSE', 2, 3, 'Textbook', '', 'Digital circuits', '')
        ]
        c.executemany('''
            INSERT INTO books (title, author, regulation, branch, year, semester, type, file_path, description, cover_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_books)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
