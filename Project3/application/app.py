from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import connect_db, get_data, insert_data, delete_data, update_data

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Các thông tin cơ sở dữ liệu
db_name = 'dbbooks'
user = 'postgres'
password = '123456'
host = 'localhost'
port = '5432'
table_name = 'books'
users_table = 'users'

# Route Trang Chủ (Hiển thị sách)
@app.route('/')
def index():
    conn = connect_db(db_name, user, password, host, port)
    if conn:
        books = get_data(conn, table_name)
        conn.close()
        return render_template('index.html', books=books)
    else:
        flash("Không thể kết nối đến cơ sở dữ liệu.")
        return render_template('index.html', books=[])

# Route Đăng Nhập
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db(db_name, user, password, host, port)
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user_data = cursor.fetchone()
            cursor.close()
            conn.close()

            if user_data:
                session['username'] = username
                flash('Đăng nhập thành công!')
                return redirect(url_for('index'))
            else:
                flash('Thông tin đăng nhập không hợp lệ, vui lòng thử lại.')
        else:
            flash('Không thể kết nối đến cơ sở dữ liệu.')
    
    return render_template('login.html')

# Route Đăng Xuất
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Bạn đã đăng xuất.')
    return redirect(url_for('index'))

# Route Thêm Sách
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        masach = request.form['masach']
        tensach = request.form['tensach']
        mota = request.form['mota']
        ngayxuatban = request.form['ngayxuatban']
        # Lý do bạn gặp lỗi có thể là ở đây. Kiểm tra lại khi gửi form.
        conn = connect_db(db_name, user, password, host, port)
        if conn:
            insert_data(conn, table_name, (masach, tensach, mota, ngayxuatban))
            flash('Sách đã được thêm thành công!')
            conn.close()
            return redirect(url_for('index'))
        else:
            flash('Không thể kết nối đến cơ sở dữ liệu.')
    return render_template('add_book.html')

# Route Sửa Sách
@app.route('/edit_book/<string:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    conn = connect_db(db_name, user, password, host, port)
    if request.method == 'POST':
        masach = request.form['masach']
        tensach = request.form['tensach']
        mota = request.form['mota']
        ngayxuatban = request.form['ngayxuatban']

        if conn:
            update_data(conn, table_name, (masach, tensach, mota, ngayxuatban, book_id))
            flash('Sách đã được cập nhật thành công!')
            conn.close()
            return redirect(url_for('index'))
        else:
            flash('Không thể kết nối đến cơ sở dữ liệu.')
    
    if conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT masach, tensach, mota, ngayxuatban FROM {table_name} WHERE masach=%s", (book_id,))
        book = cursor.fetchone()
        cursor.close()
        conn.close()
        return render_template('edit_book.html', book=book)
    else:
        flash('Không thể kết nối đến cơ sở dữ liệu.')
        return redirect(url_for('index'))

# Route Xóa Sách
@app.route('/delete_book/<string:book_id>', methods=['POST'])
def delete_book(book_id):
    conn = connect_db(db_name, user, password, host, port)
    if conn:
        delete_data(conn, table_name, book_id)
        flash('Sách đã được xóa thành công!')
        conn.close()
    else:
        flash('Không thể kết nối đến cơ sở dữ liệu.')

    return redirect(url_for('index'))


# Đảm bảo ứng dụng Flask chạy
# Để tắt khi nó đang run termail thì Ctrl C giống linux nhé ng đẹp
if __name__ == "__main__":
    app.run(debug=True,port=8080)
