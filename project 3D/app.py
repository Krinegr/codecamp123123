from flask import Flask, render_template, redirect, url_for, request, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import hashlib
from functools import wraps
import requests

app = Flask(__name__)
app.secret_key = 'labubu'

@app.route('/sign.html', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if password != confirm_password:
            flash('Пароли не совпадают!', 'danger')
            return redirect(url_for('register'))

        try:
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            if c.fetchone():
                flash('Пользователь с таким именем уже существует', 'danger')
                return redirect(url_for('register'))

            # Добавление нового пользователя
            c.execute('INSERT INTO users (username, password) VALUES (?, ?)',
                      (username, hashed_password))

            conn.commit()
            flash('Регистрация успешна! Теперь вы можете войти.', 'success')
            return redirect(url_for('admin_login'))

        except Exception as e:
            flash(f'Ошибка при регистрации: {str(e)}', 'danger')
            return redirect(url_for('register'))

        finally:
            conn.close()

    return render_template('sign.html')


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('is_admin'):
            flash('Требуется авторизация администратора', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin_panel')
@login_required
def admin_panel():
    return render_template('admin.html')


@app.route('/')
def home():
    return render_template('base2.html')

@app.route('/orderform.html')
def order():
    return render_template('orderform.html')


# логин в админ-панель
@app.route('/login.html', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        try:
            conn = sqlite3.connect('database.db')
            c = conn.cursor()

            # Получаем пользователя из базы
            c.execute('SELECT * FROM users WHERE username = ?', (username,))
            user = c.fetchone()

            if user:
                stored_password = user[2]  # Пароль находится в третьем столбце
                # Проверяем хеш пароля
                input_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()

                if input_hash == stored_password:
                    session['logged_in'] = True
                    session['username'] = username
                    session['is_admin'] = True
                    flash('Вы успешно вошли в систему!', 'success')
                    return redirect(url_for('admin_panel'))

            flash('Неверное имя пользователя или пароль', 'danger')

        except Exception as e:
            flash(f'Ошибка при входе: {str(e)}', 'danger')

        finally:
            conn.close()

    return render_template('login.html')


# Страница админ панели
@app.route('/admin_panel')
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in') or not session.get('is_admin'):
            flash('Требуется авторизация администратора', 'danger')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/orderform.html', methods=['GET', 'POST'])
def handle_order():
    if request.method == 'POST':
        # Получаем данные из формы
        name = request.form.get('names')
        house = request.form.get('house')
        figure = request.form.get('order')

        try:
            connn = sqlite3.connect('orders.db')
            c = connn.cursor()

            # Вставляем данные в таблицу orders
            c.execute('INSERT INTO orders (name, house, figure) VALUES (?, ?, ?)',
                     (name, house, figure))

            connn.commit()
            flash('Ваш заказ успешно оформлен!', 'success')
            return redirect(url_for('home'))

        except Exception as e:
            flash(f'Ошибка при оформлении заказа: {str(e)}', 'danger')
            return redirect(url_for('order'))

        finally:
            connn.close()

    return redirect(url_for('order'))

# Выход из системы
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('username', None)
    flash('Вы вышли из системы')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True, port=8080)