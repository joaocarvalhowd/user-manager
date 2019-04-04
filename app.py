from flask import Flask, request, redirect, url_for, render_template
from user import User
from flask_modus import Modus
from datetime import datetime

app = Flask(__name__)
modus = Modus(app)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date, fmt=None):
    return '{0:%d/%m/%Y %H:%M:%S}'.format(date) if date != '' else ''


users = [User('Marco Luiz Gonzaga', 'marco', 'Dev', 'tecnico', datetime(2019, 4, 1))]
access_levels = ['visitante', 'usuario',
    'administrativo', 'tecnico', 'super-usuario']


def find_user(nickname):
    return [user for user in users if user.nickname == nickname][0]


def find_super_users():
    return [user for user in users if user.access_level == 'super-usuario']


def find_by_nickname(nickname):
    return [user for user in users if user.nickname == nickname]


def find_by_access_level(access_level):
    return [user for user in users if user.access_level == access_level]


def find_by_last_access(last_access):
    return [user for user in users if user.last_access != '' and '{0:%Y-%m-%d}'.format(user.last_access) == last_access]


@app.route('/')
def root():
   return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            found_user = find_user(request.form['nickname'])
            found_user.last_access = datetime.now()
            return redirect(url_for('admin_users'))
        except IndexError:
            return render_template('login.html', error='Usuário não encontrado!')

    return render_template('login.html')


@app.route('/users', methods=['GET', 'POST'])
def admin_users():
    error = None

    if request.method == 'POST':
        try:
            find_user(request.form['nickname'])
            error = 'Já existe um usuário com esse nome curto: ' + request.form['nickname']
        except IndexError:
            new_user = User(
                request.form['fullname'],
                request.form['nickname'],
                request.form['role'],
                request.form['access_level'],
                request.form['last_access']
            )
            users.append(new_user)

            return redirect(url_for('admin_users'))

    search_param = request.args.get('search')
    access_level_param = request.args.get('access_level')
    last_access_param = request.args.get('last_access')
    search_value = search_param if search_param != None and search_param.strip() != '' else None
    access_level_value = access_level_param if access_level_param != None and access_level_param.strip() != '' else None
    last_access_value = last_access_param if last_access_param != None and last_access_param.strip() != '' else None

    users_filtered = users

    if (search_value != None):
        users_filtered = find_by_nickname(search_value)

    if (access_level_value != None):
        users_filtered = find_by_access_level(access_level_value)

    if (last_access_value != None):
        users_filtered = find_by_last_access(last_access_value)

    return render_template(
        'index.html',
        users=users_filtered,
        error=error,
        total_super_users=len(find_super_users()),
        search_value=search_value,
        access_levels=access_levels,
        access_level_value=access_level_value,
        last_access_value=last_access_value
    )

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
   return render_template('show.html', user=found_user, access_levels=access_levels)

if __name__ == '__main__':
   app.run(debug=True, port=3000)
