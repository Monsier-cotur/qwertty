from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.db"
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    passward = db.Column(db.String, nullable=True)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String, nullable=False)

with app.app_context():
    db.create_all()

    user=User(username = 'tyuippiodoi', content = 'jhfjhjdbjvb')
    db.session.add(user)
    db.session.commit()

    post1 = Post(title = "Lesson1", content = "dsfdsggfgf")

    post1.content = 'Updated poiun'
    db.session.add(post1)
    db.session.commit()
    # posts = Post.query.all()
    # for post in posts:
    #     print(post.title)

    post1 = Post.query.first()
    print(post1.title)
    post1.title = 'Updated Lesson1'
    db.session.commit()
    posts = Post.query.all()
    for post in posts:
        print(post.id, post.title)

    users = User.query.all()
    for user in users:
        print(user.username)
    #
    # user = User.query.filter_by(username='Jane').first()
    # user.username = 'Jane'
    # db.session.commit()
    # print(user.username)
    #
    # user = User.query.filter_by(username='Jane').first()
# db.session.delete(post)
# db.session.commit()








# conn.execute('DROP TABLE teachers')
# conn.execute('''CREATE TABLE teachers (
#   id INTEGER PRIMARY KEY,
#   name VARCHAR(50)
# ); ''')

# conn.execute('ALTER TABLE teachers ADD COLUMN subjects VARCHAR(15)')
# conn.commit()
# conn.execute('INSERT INTO teachers (name, id, subjects) VALUES ("ALUA", 301, "math")')
# conn.commit()
# conn.execute('INSERT INTO teachers (name, id, subjects) VALUES ("ASDF", 102, "tyu")')
# conn.commit()
#
#
# result = conn.execute('SELECT * FROM teachers')
#
# for row in result:
#     print(row)
#
# conn.close()
# conn.execute('DROP TABLE tyu')
# conn.execute('''CREATE TABLE tyu (
#   id INTEGER PRIMARY KEY,
#   name VARCHAR(50)
# ); ''')

# conn.execute('INSERT INTO tyu (name, id) VALUES ("ALUA", 301);')
# conn.execute('INSERT INTO tyu (name, id) VALUES ("ASDF", 102);')
# conn.commit()
# conn.execute('UPDATE tyu SET name="SAI" WHERE id = 101;')
# conn.commit()
# conn.execute('DELETE FROM tyu WHERE id = 1')
# conn.commit()

# result = conn.execute('SELECT * FROM tyu')
#
# for row in result:
#     print(row)
#
# conn.close()

# conn = sqlite3.connect("test.db")

# conn.execute('''CREATE TABLE students (
#   id INTEGER PRIMARY KEY,
#   name VARCHAR(50),
#   age INTEGER
# ); ''')

# conn.execute('DROP TABLE students')
# conn.execute('INSERT INTO students (name, age) VALUES ("ALUA", 14)')
# conn.commit()
# conn.execute('INSERT INTO students (name, age) VALUES ("QWERTY", 19)')
# conn.commit()
# conn.execute('INSERT INTO students (name, age) VALUES ("ASD", 89)')
# conn.commit()
# conn.execute('UPDATE students SET name="SAI" WHERE id = 16;')
# conn.commit()
# conn.execute('DELETE FROM students WHERE id = 14;')
# conn.commit()

#
# result = conn.execute('SELECT * FROM students')
# for row in result:
#     print(row)
#
# conn.close()