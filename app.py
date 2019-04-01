from flask import Flask, request, redirect, url_for, render_template
from user import User
from flask_modus import Modus

app = Flask(__name__)
modus = Modus(app)

#users = []
users = [User('Marco Luiz Gonzaga', 'marco', 'Dev', 'técnico', '100')]
access_levels = ['visitante', 'usuario', 'administrativo', 'tecnico', 'super-usuario']


def find_user(nickname):
   return [user for user in users if user.nickname == nickname][0]


@app.route('/')
def root():
   return redirect(url_for('index'))


@app.route('/users', methods=['GET', 'POST'])
def index():
   error = None
   if request.method == 'POST':
      try:
         found_user = find_user(request.form['nickname'])
         error = 'Já existe um usuário com esse nome curto: ' + request.form['nickname']
      except IndexError:
         new_user = User(request.form['fullname'], request.form['nickname'], request.form['role'], request.form['access_level'], request.form['last_access'])
         users.append(new_user)
         return redirect(url_for('index'))
   return render_template('index.html', users=users, error=error)

@app.route('/users/new')
def new():
   return render_template('new.html', access_levels=access_levels)


@app.route('/users/<nickname>', methods=["GET", "PATCH", "DELETE"])
def show(nickname):
   found_user = find_user(nickname)
   if request.method == b'PATCH':
      found_user.fullname = request.form['fullname']
      found_user.nickname = request.form['nickname']
      found_user.role = request.form['role']
      found_user.access_level = request.form['access_level']
      found_user.last_access = request.form['last_access']
      return redirect(url_for('index'))
   if request.method == b'DELETE':
      users.remove(found_user)
      return redirect(url_for('index'))
   return render_template('show.html', user=found_user)


@app.route('/users/<nickname>/edit')
def edit(nickname):
   found_user = find_user(nickname)
   return render_template('edit.html', user=found_user)


if __name__ == '__main__':
   app.run(debug=True, port=3000)
