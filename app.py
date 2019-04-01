from flask import Flask, request, redirect, url_for, render_template
from user import User
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)

users = []
access_levels = ['visitante', 'usuário', 'administrativo', 'técnico', 'super-usuário']
users = [User('Marco Luiz Gonzaga', 'marco', 'Dev', 'técnico', '100')]

def find_user(nickname):
   return [user for user in users if user.nickname == nickname][0]

@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/users', methods=['GET', 'POST'])
def index():
    return render_template('index.html', users=users)


@app.route('/users/new')
def new():
    return render_template('new.html', access_levels=access_levels)

@app.route('/users/<nickname>', methods=["GET", "PATCH", "DELETE"])
def show(nickname):
   found_user = find_user(nickname)
 
   return render_template('show.html', user = found_user)

@app.route('/users/<nickname>/edit')
def edit(nickname):
   found_user = find_user(nickname)
   return render_template('edit.html', user=found_user)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
