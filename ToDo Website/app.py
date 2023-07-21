from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    duration = db.Column(db.String(100), nullable=False)
	

    def _init_(self, title, desc, duration):
        self.title = title
        self.desc = desc
        self.duration = duration

    def _repr_(self) -> str:
        s = self.title + self.desc
        return s

with app.app_context():
	db.create_all()


@app.route('/', methods=['GET', 'POST'])
def myTodo():
    if request.method=='POST' :
        title = request.form['title']
        desc = request.form['desc']
        duration = request.form['duration']
        todo = Todo(title=title, desc=desc, duration=duration)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/delete/<int:sno>') 
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=['GET', 'POST']) 
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        duration = request.form['duration']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        todo.duration = duration
        db.session.add(todo)
        db.session.commit()
        return redirect('/')

    todo=Todo.query.filter_by(sno=sno).first()
    db.session.commit()
    return render_template('update.html', todo=todo)

@app.route('/show')
def show():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'show'


if __name__ == '__main__':
    app.run(debug=True)