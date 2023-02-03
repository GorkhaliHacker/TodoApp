from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///anujaya.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


class User(db.Model):
    sn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self):
        return f"{self.sn} - {self.description}"


@app.route('/', methods=['GET', 'POST'])
def add():  # put application's code here
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        qry = User(title=title, description=description)
        db.session.add(qry)
        db.session.commit()

    todo = User.query.all()
    return render_template('index.html', todo=todo)
    # return 'Hello World!'


@app.route('/update/<int:sn>', methods=['GET', 'POST'])
def update(sn):
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        upd = User.query.filter_by(sn=sn).first()
        upd.title = title
        upd.description = description
        upd.date = datetime.now()
        db.session.add(upd)
        db.session.commit()
        return redirect("/")

    upd = User.query.filter_by(sn=sn).first()
    return render_template('update.html', todo=upd)


@app.route('/Delete/<int:sn>')
def delete(sn):
    todel = User.query.filter_by(sn=sn).first()
    db.session.delete(todel)
    db.session.commit()
    return redirect("/")


@app.route('/aboutme')
def about():
    return render_template('aboutme.html')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
