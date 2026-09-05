import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
from database import get_db

app = Flask(__name__)
app.secret_key = 'super_secret_key_for_library'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.before_request
def make_session_permanent():
    session.permanent = True

# --- Utility Functions ---
def get_current_user():
    if 'user_id' in session:
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE id = ?', (session['user_id'],)).fetchone()
        conn.close()
        return user
    return None

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or not user['is_admin']:
            flash('Admin access required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


# --- Authentication Routes ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        conn = get_db()
        user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['is_admin'] = user['is_admin']
            flash('Logged in successfully!', 'success')
            if user['is_admin']:
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password', 'danger')
            
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            flash('Passwords do not match!', 'danger')
            return redirect(url_for('register'))
            
        hashed_pw = generate_password_hash(password)
        
        conn = get_db()
        try:
            conn.execute('INSERT INTO users (name, email, password) VALUES (?, ?, ?)', (name, email, hashed_pw))
            conn.commit()
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('login'))
        except conn.IntegrityError:
            flash('Email already registered!', 'warning')
        finally:
            conn.close()
            
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# --- Student Routes ---
@app.route('/')
def index():
    user = get_current_user()
    return render_template('index.html', user=user)

@app.route('/books', methods=['GET', 'POST'])
def books():
    user = get_current_user()
    conn = get_db()
    
    query = "SELECT * FROM books WHERE 1=1"
    params = []
    
    if request.method == 'POST' or request.args:
        req_data = request.form if request.method == 'POST' else request.args
        regulation = req_data.get('regulation')
        branch = req_data.get('branch')
        year = req_data.get('year')
        semester = req_data.get('semester')
        search = req_data.get('search')
        
        if regulation:
            query += " AND regulation = ?"
            params.append(regulation)
        if branch:
            query += " AND branch = ?"
            params.append(branch)
        if year:
            query += " AND year = ?"
            params.append(year)
        if semester:
            query += " AND semester = ?"
            params.append(semester)
        if search:
            query += " AND (title LIKE ? OR author LIKE ?)"
            params.extend(['%'+search+'%', '%'+search+'%'])
            
    books_list = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('books.html', books=books_list, user=user)

@app.route('/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def book_detail(book_id):
    user = get_current_user()
    conn = get_db()
    
    if request.method == 'POST':
        # Handle review submission
        rating = request.form.get('rating')
        review_text = request.form.get('review_text')
        date_posted = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        conn.execute('INSERT INTO reviews (user_id, book_id, rating, review_text, date_posted) VALUES (?, ?, ?, ?, ?)',
                     (user['id'], book_id, rating, review_text, date_posted))
        conn.commit()
        flash('Review submitted successfully!', 'success')
        return redirect(url_for('book_detail', book_id=book_id))
    
    book = conn.execute('SELECT * FROM books WHERE id = ?', (book_id,)).fetchone()
    reviews = conn.execute('''
        SELECT r.*, u.name 
        FROM reviews r 
        JOIN users u ON r.user_id = u.id 
        WHERE r.book_id = ? 
        ORDER BY r.date_posted DESC
    ''', (book_id,)).fetchall()
    
    is_bookmarked = conn.execute('SELECT 1 FROM bookmarks WHERE user_id = ? AND book_id = ?', (user['id'], book_id)).fetchone()
    
    conn.close()
    
    if not book:
        flash('Book not found.', 'danger')
        return redirect(url_for('books'))
        
    return render_template('book_detail.html', book=book, reviews=reviews, user=user, is_bookmarked=bool(is_bookmarked))

@app.route('/dashboard')
@login_required
def dashboard():
    user = get_current_user()
    conn = get_db()
    
    issued = conn.execute('''
        SELECT i.*, b.title, b.author 
        FROM issued_books i 
        JOIN books b ON i.book_id = b.id 
        WHERE i.user_id = ?
    ''', (user['id'],)).fetchall()
    
    bookmarks = conn.execute('''
        SELECT b.* 
        FROM bookmarks bm 
        JOIN books b ON bm.book_id = b.id 
        WHERE bm.user_id = ?
    ''', (user['id'],)).fetchall()
    
    conn.close()
    return render_template('dashboard.html', user=user, issued=issued, bookmarks=bookmarks)

@app.route('/issue/<int:book_id>')
@login_required
def issue_book(book_id):
    user = get_current_user()
    conn = get_db()
    
    # Check if already issued
    existing = conn.execute('SELECT * FROM issued_books WHERE user_id = ? AND book_id = ? AND status = "Issued"', (user['id'], book_id)).fetchone()
    if existing:
        flash('You have already issued this book.', 'warning')
    else:
        issue_date = datetime.now().strftime('%Y-%m-%d')
        conn.execute('INSERT INTO issued_books (user_id, book_id, issue_date) VALUES (?, ?, ?)',
                     (user['id'], book_id, issue_date))
        conn.commit()
        flash('Book issued successfully!', 'success')
        
    conn.close()
    return redirect(request.referrer or url_for('books'))

@app.route('/bookmark/<int:book_id>')
@login_required
def toggle_bookmark(book_id):
    user = get_current_user()
    conn = get_db()
    
    existing = conn.execute('SELECT * FROM bookmarks WHERE user_id = ? AND book_id = ?', (user['id'], book_id)).fetchone()
    if existing:
        conn.execute('DELETE FROM bookmarks WHERE id = ?', (existing['id'],))
        flash('Removed from bookmarks.', 'info')
    else:
        conn.execute('INSERT INTO bookmarks (user_id, book_id) VALUES (?, ?)', (user['id'], book_id))
        flash('Added to bookmarks.', 'success')
        
    conn.commit()
    conn.close()
    return redirect(request.referrer or url_for('book_detail', book_id=book_id))

@app.route('/download/<path:filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)


# --- Admin Routes ---
@app.route('/admin')
@admin_required
def admin_dashboard():
    user = get_current_user()
    conn = get_db()
    
    total_books = conn.execute('SELECT COUNT(*) FROM books').fetchone()[0]
    total_users = conn.execute('SELECT COUNT(*) FROM users WHERE is_admin = 0').fetchone()[0]
    total_issued = conn.execute('SELECT COUNT(*) FROM issued_books WHERE status = "Issued"').fetchone()[0]
    
    recent_issues = conn.execute('''
        SELECT i.*, b.title, u.name 
        FROM issued_books i 
        JOIN books b ON i.book_id = b.id 
        JOIN users u ON i.user_id = u.id 
        ORDER BY i.issue_date DESC LIMIT 5
    ''').fetchall()
    
    conn.close()
    return render_template('admin/dashboard.html', user=user, stats={'books': total_books, 'users': total_users, 'issued': total_issued}, recent_issues=recent_issues)

@app.route('/admin/books', methods=['GET', 'POST'])
@admin_required
def manage_books():
    user = get_current_user()
    conn = get_db()
    
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        regulation = request.form['regulation']
        branch = request.form['branch']
        year = request.form['year']
        semester = request.form['semester']
        book_type = request.form['type']
        description = request.form.get('description', '')
        
        file_path = ''
        if 'pdf_file' in request.files:
            file = request.files['pdf_file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file_path = filename

        conn.execute('''
            INSERT INTO books (title, author, regulation, branch, year, semester, type, file_path, description, cover_image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (title, author, regulation, branch, year, semester, book_type, file_path, description, ''))
        conn.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('manage_books'))
        
    books = conn.execute('SELECT * FROM books').fetchall()
    conn.close()
    return render_template('admin/manage_books.html', user=user, books=books)

@app.route('/admin/books/delete/<int:book_id>')
@admin_required
def delete_book(book_id):
    conn = get_db()
    conn.execute('DELETE FROM books WHERE id = ?', (book_id,))
    conn.commit()
    conn.close()
    flash('Book deleted successfully.', 'success')
    return redirect(url_for('manage_books'))

@app.route('/admin/users')
@admin_required
def manage_users():
    user = get_current_user()
    conn = get_db()
    users = conn.execute('SELECT * FROM users WHERE is_admin = 0').fetchall()
    issued = conn.execute('''
        SELECT i.*, b.title, u.name 
        FROM issued_books i 
        JOIN books b ON i.book_id = b.id 
        JOIN users u ON i.user_id = u.id
    ''').fetchall()
    conn.close()
    return render_template('admin/manage_users.html', user=user, users=users, issued=issued)

@app.route('/admin/issue/return/<int:issue_id>')
@admin_required
def return_book(issue_id):
    conn = get_db()
    return_date = datetime.now().strftime('%Y-%m-%d')
    conn.execute('UPDATE issued_books SET status = "Returned", return_date = ? WHERE id = ?', (return_date, issue_id))
    conn.commit()
    conn.close()
    flash('Book marked as returned.', 'success')
    return redirect(url_for('manage_users'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
