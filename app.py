import sqlite3
import os
from flask import Flask, render_template, request, g, url_for, flash, redirect, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from UserLogin import UserLogin

# конфигурация
DATABASE = f"{os.getcwd()}/data/mysite.db"
DEBUG = True
SECRET_KEY = "2ff6cac84a3406ecd3087e5c0bb438ba"

app = Flask(__name__)
app.config.from_object(__name__)
# !--

# работа с Flask Login
login_manager = LoginManager(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    print("load_user") # проверка вызова
    user = exe(f"SELECT * FROM users WHERE id = {user_id};")[0]
    return UserLogin().fromDB(user)
# !--

# работа с БД
def connect_db():
    '''Установка соединения с БД. Вспомогательная функция'''
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    '''Создание таблиц БД'''
    db = connect_db()
    with app.open_resource("data/script.sql", 'r') as script:
        db.cursor().executescript(script.read())
    db.commit()
    db.close()

def get_db():
    '''Соединение с БД в рамках контекста приложения'''
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db

def exe(query):
    '''Исполнение запроса в рамках контекста приложения.
    Возвращает результат в виде строки'''
    db = get_db()
    cursor = db.cursor()
    try:
        cursor.execute(query)
        if "SELECT" in query.upper():
            result = cursor.fetchall() #  возвращает список кортежей
        else:
            db.commit()
            result = "Success"
    except:
        db.rollback()
        result = "An error has occured"
    return result

@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно установлено'''
    if hasattr(g, "link_db"):
        g.link_db.close()

# !--

# Валидация
def isspecial(string):
    '''Проверяет имеет ли следующая строка спецсимволы'''
    special = ('.', ',', '!', '?', ':', '"', '\'', '@', '#', '-',\
    '$', '%', '&', '*', '^', '\\', '/', '|', '~', '{', '}', '[', ']')
    for char in string:
        if char in special:
            return True
    return False

def usernameValidation(username):
    '''Аргумент – логин. Возвращает кортеж с результатом проверки
    логина в формате кортежа и сообщением о результате. Пример (False, "Some error") '''
    error = ()    
    for char in username:
        if not ('A' <= char <= 'Z' or 'a' <= char <= 'z' or char == '_'):
            error += (" Invalid characters in username",)
            break
    if len(username) < 6:
        error += (" Username must be at least 6 characters",)
    if error != '':
        return (True, "Success") 
    else:
        return (False, error)
        
def emailValidation(email):
    '''Аргумент – почта. Возвращает кортеж с результатом проверки
    почты в формате кортежа и сообщением о результате. Пример (False, "Some error") '''    
    if email[0:email.find('@')] != '' or email[0:email.find('@')] != ' ': # !!! поправить
        return (True, "Success") 
    else:
        return (False, 'Incorrect email')

def passwordValidation(password):
    if password != None and len(password) >= 8:
        digit = 0
        uppercase = 0
        lowercase = 0
        special = 0
        for char in password:
            if char.isdigit() == True:
                digit = 1
            if char.isupper() == True:
                uppercase = 1
            if char.islower() == True:
                lowercase = 1
            if isspecial(char) == True:
                special = 1
        if digit == 1 and uppercase == 1 and lowercase == 1\
            and special == 1:
            return (True, "Success")
        else:
            return (False, "Password should contain various symbols")
    else:
        return (False, "Password lenth must be at least 8 characters")
#  !--

@app.route("/")
def main():
    if current_user.is_authenticated:
        return render_template("logged.html", username = current_user.get_username())
    else:
        return render_template("index.html")

    
@app.route("/login", methods = ("post", "get"))
def login():
    if current_user.is_active: # если активна сессия пользователя, то перенаправляем его на свою страницу
        return redirect(url_for("profile", username = current_user.get_username()))
    else:
        if request.method == "POST": # регистр запроса важен
            username = request.form.get("login")
            psw = request.form.get("psw")
            if exe(f"SELECT COUNT(*) FROM users WHERE username = '{username}';")[0][0] != 0: # [0][0] т.к. функция exe возвращает список кортежей
                psw_hash = exe(f"SELECT password FROM users WHERE username = '{ username }';")[0][0]
                if check_password_hash(psw_hash, psw):
                    user = exe(f"SELECT * FROM users WHERE username = '{username}';")[0]
                    userlogin = UserLogin().create(user)
                    login_user(userlogin)
                    return redirect(url_for("main"))
                else:
                    flash("Wrong password. Try again", category="error")
            else:
                flash("This user doesn't exist", category="error")
        return render_template("login.html")
        

data = () #
@app.route("/register", methods = ("post", "get")) # здесь регистр не важен
def register():
    global data #
    if request.method == "POST": # регистр запроса важен
        username = request.form.get("login")
        email = request.form.get("email")
        psw = request.form.get("psw")
        re_psw = request.form.get("psw_control")
        data += (username, email, psw, re_psw) #
        print(data) #
        if usernameValidation(username)[0] == True and emailValidation(email)[0] == True\
                                and passwordValidation(psw)[0] == True and psw == re_psw:
            psw_hash = generate_password_hash(psw)
            if exe(f"SELECT COUNT(*) FROM users WHERE username = '{username}' OR email = '{email}';")[0][0] == 0:
                exe(f"INSERT INTO users(username, email, password) VALUES ('{username}', '{email}', '{psw_hash}');")
                flash("Пользователь добавлен", category="sucess")
            else:
                flash("Такие логин и/или пароль уже используются", category="error")
        else:
            data += ('неудача валид',)
            if usernameValidation(username)[0] == False:
                flash(usernameValidation(username)[1], category="error")
            if emailValidation(email)[0] == False:
                flash(emailValidation(email)[1], category="error")
            if passwordValidation(psw)[0] == False:
                flash(passwordValidation(psw)[1], category="error")
            if psw != re_psw:
                flash("Passwords are different", category="error")
        print(data)
    return render_template("register.html")

@app.route("/profile/<username>") # for test purposes
@login_required
def profile(username):
    if username == current_user.get_username():
        return render_template("profile.html", username = current_user.get_username())
    else:
        return redirect(url_for("profile", username = current_user.get_username()))

@app.route("/shop")
def shop():
    if current_user.is_active:
        return render_template("shop_auth.html", username = current_user.get_username())
    else:
        return render_template("shop.html")

@app.route("/cart")
@login_required
def cart():
    return render_template("cart.html", username = current_user.get_username())

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main"))

@app.route("/img/<int:img_id>")
def render_image(img_id):
    '''Выгрузка изображения из БД по id'''
    db_resp = exe(f"SELECT image FROM books WHERE id = {img_id};")
    image = db_resp[0][0]
    resp = make_response(image)
    resp.headers["Content-Type"] = "image/jpg"
    return resp
    
@app.errorhandler(404)
def pageNotFound(error):
    return render_template("page404.html"), 404

if __name__ == "__main__":
    create_db()
    app.run(port = 80)
    