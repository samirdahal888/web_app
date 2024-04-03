from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime,timezone
my_todo_list=Flask(__name__)


my_todo_list.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db=SQLAlchemy(my_todo_list)

class Todo(db.Model):
    sn=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime, default=datetime.now(timezone.utc))

@my_todo_list.route('/',methods=['GET','POST'])
def homepage():
    if request.method=='POST':
        head=request.form['title']
        foot=request.form['desc']
        data=Todo(title=head,desc=foot)
        db.session.add(data)
        db.session.commit()
    alltodo=Todo.query.all()
    # print(alltodo.title)
    return render_template('index.html',all=alltodo)

@my_todo_list.route('/delet/<int:sn>')
def delet(sn):
    todo=Todo.query.filter_by(sn=sn).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@my_todo_list.route('/update/<int:sn>',methods=['GET','POST'])
def update(sn):
      if request.method=='POST':
          title=request.form['title']
          desc=request.form['desc']
          todo=Todo.query.filter_by(sn=sn).first()
          todo.title=title
          todo.desc=desc
          db.session.add(todo)
          db.session.commit()
          

          return redirect('/')
      
      todo=Todo.query.filter_by(sn=sn).first()
      
      return render_template('update.html',todo=todo)



if __name__=='__main__':
    my_todo_list.run(debug=True)