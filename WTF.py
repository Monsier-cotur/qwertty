from flask import Flask, render_template, redirect, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'docx', 'png', 'jpg'}  # Разрешенные расширения файлов
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    age = db.Column(db.Integer)
    password = db.Column(db.String(80), nullable=False)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class  ProfileEditForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Save')

class CalcForm(FlaskForm):
    a = IntegerField ("A = ")
    b = IntegerField ("B = ")

    submit = SubmitField('Save')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash('Username already exists! Please choose a different one.', 'danger')
            return redirect('/register')
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! You can now log in.', 'success')
        return redirect('/')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            flash('Login successful!', 'success')
            return redirect('/')
        else:
            flash('Invalid username or password. Please try again.', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route('/')
@login_required
def home():
    user = {
    "id" : 1,
    "username" :current_user.username,
    "email" : current_user.email

    }
    return render_template("index.html", user = user)

@app.route('/users')
def users():
    users = User.query.all()
    return render_template ("users.html", users = users)

@app.route('/data', methods = ['GET'])
def get_data():
    data  = {"name" : "ALUA",
             "age" : 14}
    return jsonify(data)

@app.errorhandler(404)
def not_found_error(error):
    error_message = {"message":"Page not found"}
    return jsonify(error_message), 404



@app.route("/profile", methods=['GET','POST'])

def profile():

    form = ProfileEditForm()

    if form.validate_on_submit():
        existing_user = User.query.filter_by(id=current_user.id).first()
        if not existing_user:
            return ""
        existing_user.username = form.username.data
        existing_user.email = form.email.data
        db.session.commit()
        flash('Edit success', 'success')
        return redirect('/profile')
    return render_template('profile.html', form=form)



@app.route("/calc", methods=['GET','POST'])
def plus():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        result = a+b
        flash("Result = " +str(result))
        redirect('/calc')
    return render_template('calc.html', form=form)

@app.route("/res", methods=['GET','POST'])
def res():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        result = a * b
        flash("Result = " + str(result))
        redirect('/calc')
    return render_template('calc.html', form=form)

@app.route("/minus", methods=['GET','POST'])
def minus():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        result = a - b
        flash("Result = " + str(result))
        redirect('/minus')
    return render_template('calc.html', form=form)

@app.route("/ras", methods=['GET','POST'])
def ras():
    form = CalcForm()
    if form.validate_on_submit():
        a = form.a.data
        b = form.b.data
        result = a / b
        flash("Result = " + str(result))
        redirect('/ras')
    return render_template('calc.html', form=form)

@app.errorhandler(500)
def not_found_error(error):
    error_message = {"message":"Page not found"}
    return render_template("error500.html")

@app.route('/users/add',methods=["POST","GET"])
def users_add():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        age = request.form['age']
        password = "password"
        new_user = User(username=username,email=email,age=age,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/users')
    return render_template('useradd.html' )

@app.route('/users/edit/<int:id>',methods=["POST","GET"])
def users_edit(id):
    user = User.query.get_or_404(id)
    if request.method == "POST":
        user.username = request.form['username']
        user.email = request.form['email']
        user.age = request.form['age']
        db.session.commit()
        return redirect('/users')
    return render_template('users_edit.html', user=user)

@app.route('/users/delete/<int:id>',methods=["POST"])
def users_delete(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/read/<int:id>',methods=["GET"])
def users_read(id):
    user = User.query.get_or_404(id)
    return render_template("users_read.html", user = user)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/ind')
def index():
    # Получение списка имен загруженных файлов
    filenames = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('image.html', filenames=filenames)


@app.route('/upload', methods=['POST'])
def upload_file():
    # Получение загруженного файла из запроса
    file = request.files['file']


    # Проверка, что файл был отправлен и имеет допустимое расширение
    if file and allowed_file(file.filename):
        # Безопасное сохранение файла с учетом его имени
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Получение списка имен загруженных файлов
        filenames = os.listdir(app.config['UPLOAD_FOLDER'])
        return render_template('image.html', filenames=filenames)
    else:
        return 'Недопустимый файл. <a href="/">Вернуться</a>'


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
