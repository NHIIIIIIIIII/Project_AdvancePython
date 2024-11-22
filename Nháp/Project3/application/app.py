from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import get_db_connection, insert_data, delete_data, update_data,get_data
from forms import LoginForm

app = Flask(__name__)
app.secret_key = 'VLU@!#@HSJ'

# Các thông tin cơ sở dữ liệu
db_name = 'dbbooks'
user = 'postgres'
password = '123456'
host = 'localhost'
port = '5432'
table_name = 'books'
users_table = 'users'

# Route Trang Chủ (Hiển thị sách)
'''@app.route('/')
def index():
    conn = get_db_connection(db_name, user, password, host, port)
    if conn:
        books = get_data(conn, table_name)
        conn.close()
        return render_template('index.html', books=books)
    else:
        flash("Không thể kết nối đến cơ sở dữ liệu.")
        return render_template('index.html', books=[])'''
# Route Đăng Nhập
@app.route('/', methods=['GET', 'POST'])
def login():
    # try excpet của Nhi sẽ hk run đc đâu , đa số trường hợp thì try excpect sẽ chả ảnh hưởng hay có tác dụng j đó Bi bt hk =.=
    # vaanggg ngoan
    form = LoginForm()
    if form.validate_on_submit():
        try: 
            session['db_name'] = form.db_name.data
            session['user'] = form.user.data
            session['password'] = form.password.data
            session['host'] = form.host.data
            session['port'] = form.port.data
            conn = get_db_connection(form.db_name.data, form.user.data, form.password.data, form.host.data, form.port.data)
            # conn là mình hiểu Bi dùng để kb dn , hàm get_db+connection là hàm Bi đã làm từ tr đk nè
            # Bi xem hàm đó trả về gì
            # Bi thấy nó trả về 2 giá trị là conn(giá trị connection) hoặc None ( hiểu là rỗng )
            # Vậy nên nếu nó conn được thì chắc chắn ko None phải hog, mình viết điều kiện ktra xem conn nó ok ko , nếu ko ok buộc phải login lại
            # Nếu biến conn của Bi ko None (nghĩa là connect được) thì mình cho nó vào, ngược lại ( biến None) thì ko cho
            # Bi ổn đoạn này hk 
            # R đó chỉ đơn giản v thôi -.- , tại của Bi sai đúng j cx conn , Bi khi nào cái này phải xem ở ternimal nó hiện cái j để mà bt check nha
            if conn is not None:
                flash('Connected to database successfully.')
                return redirect(url_for('index'))
            else:
                # Đó Bi thấy lỗi chưa, lỗi thì nó ko cho qua index
                flash(f'Error connecting to database: {e}')
        except Exception as e:
            flash(f'Error connecting to database: {e}')
    return render_template('login.html', form=form)
# Route Đăng Xuất

@app.route('/logout')
def logout():
    session.clear()  # Xóa tất cả các thông tin trong session
    flash('Bạn đã đăng xuất thành công.')
    return redirect(url_for('login'))  # Chuyển hướng về trang đăng nhập

@app.route('/index')
def index():
    conn = get_db_connection(db_name, user, password, host, port)
    if conn:
        books = get_data(conn, table_name)
        conn.close()
        return render_template('index.html', books=books)
    else:
        flash("Không thể kết nối đến cơ sở dữ liệu.")
        return render_template('index.html', books=[])
# Route Thêm Sách
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        masach = request.form['masach']
        tensach = request.form['tensach']
        mota = request.form['mota']
        ngayxuatban = request.form['ngayxuatban']
        # Lý do bạn gặp lỗi có thể là ở đây. Kiểm tra lại khi gửi form.
        conn = get_db_connection(db_name, user, password, host, port)
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
    conn = get_db_connection(db_name, user, password, host, port)
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
    conn = get_db_connection(db_name, user, password, host, port)
    if conn:
        delete_data(conn, table_name, book_id)
        flash('Sách đã được xóa thành công!')
        conn.close()
    else:
        flash('Không thể kết nối đến cơ sở dữ liệu.')

    return redirect(url_for('index'))


# Đảm bảo ứng dụng Flask chạy
if __name__ == "__main__":
    app.run(debug=True,port=5000)
