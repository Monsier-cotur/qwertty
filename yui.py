from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db = SQLAlchemy(app)



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)


# @app.route("/")
# def hello():
#     return render_template("index.html")
#
#
# @app.route("/about")
# def about():
#     Team_name="Cptuer"
#     age = 190
#     return "<h1>About</h1> <p>Team name =</p> "+Team_name + "<p>Age =</p>" +str(age)
#
#
# @app.route("/contact")
# def contact():
#     return '''
#     <i>Alua</i>
#     <i>Bakhyt</i>
#     <i>14</i>
#     '''
#
# @app.route("/login")
# def login():
#     return '''
#     <input>name</input>
#     <input>password</input>
#     '''
#
# @app.route("/404")
# def r():
#     return "<h1>ERROR404</h1>"
#
# @app.route("/blol")
# def blol():
#     return '''
#     <h1>Cho vi hotite</h1>
#     <h3>Тег input является одним из разносторонних элементов формы и позволяет создавать разные элементы интерфейса и обеспечить взаимодействие с пользователем. Главным образом input предназначен для создания текстовых полей, различных кнопок, переключателей и флажков. Хотя элемент input не требуется помещать внутрь контейнера <form>, определяющего форму, но если введенные пользователем данные должны быть отправлены на сервер, где их обрабатывает серверная программа, то указывать <form> обязательно. То же самое обстоит и в случае обработки данных с помощью клиентских приложений, например, скриптов на языке JavaScript.</h3>
#     '''
#
# @app.route("/yy")
# def sd():
#     return '''
# <i>fff</i>
# '''
#
# @app.route("/gallery")
# def gallery():
#     return render_template("gallery.html")
#
# @app.route("/blog")
# def blog():
#     return render_template("blog.html")
#
# @app.route("/app_contact")
# def app_contact():
#     name="Alua"
#     age="14"
#     return render_template("contact.html", name=name, age=age)
#
@app.route("/posts")
def post_list():
    posts = Post.query.all()
    return render_template("post_list.html", posts=posts, title = "tyui")

if __name__ == "__main__":
    app.run(debug=True)
