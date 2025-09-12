from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5

app = Flask(__name__)

bootstrap = Bootstrap5(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(1000))
    complete = db.Column(db.Boolean)

@app.route('/')
def index():
    #show all todos
    todo_list = Todo.query.all()
    return render_template('index.html', todo_list=todo_list)

@app.route('/add', methods=['POST'])
def add():
    #add a new todo
    title = request.form['title']
    description = request.form['description']
    complete= False # new tasks are incomplete by default
    
    new_todo = Todo(title=title, description=description, complete=complete)
    
    #add to the database
    db.session.add(new_todo)
    db.session.commit()
    
    #redirects to homepage
    return redirect(url_for('index'))

@app.route('/update/<int:todo_id>')
def update():
    #edit a todo
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete # opposite value
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)