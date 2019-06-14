"""
Desenvolvedores: BRUNO CAOE FERREIRA SPERA e JOÃO VICTOR BARBOSA DE CARVALHO
"""

from flask import Flask, request, redirect, url_for, render_template
from user import User
from flask_modus import Modus
from datetime import datetime
import json

app = Flask(__name__)
modus = Modus(app)


@app.template_filter('strftime')
def _jinja2_filter_datetime(date):
    return datetime.strptime(date, "%Y-%m-%d %H:%M:%S") if date != '' else ''


access_levels = ['visitante', 'usuario',
                 'administrativo', 'tecnico', 'super-usuario']


def load_users():
    with open('users.json', 'r') as f:
        json_str = f.read()
        data = json.loads(json_str)

        users = User.schema().load(data, many=True)

    return users


def add_user(user: User):
    users = load_users()
    users.append(user)

    f = open('users.json', 'w')
    f.write(User.schema().dumps(users, many=True, indent=2))
    f.close()


def remove_user(user: User):
    users = load_users()
    users.remove(user)

    f = open('users.json', 'w')
    f.write(User.schema().dumps(users, many=True, indent=2))
    f.close()


def update_user(nickname, data):
    users = load_users()

    found_user = [user for user in users if user.nickname == nickname][0]

    found_user.fullname = data.form['fullname']
    found_user.nickname = data.form['nickname']
    found_user.role = data.form['role']
    found_user.access_level = data.form['access_level']
    found_user.last_access = data.form['last_access']

    f = open('users.json', 'w')
    f.write(User.schema().dumps(users, many=True, indent=2))
    f.close()


def update_last_access(nickname):
    users = load_users()

    found_user = [user for user in users if user.nickname == nickname][0]
    found_user.last_access = f"{datetime.now():%Y-%m-%d %H:%M:%S}"

    f = open('users.json', 'w')
    f.write(User.schema().dumps(users, many=True, indent=2))
    f.close()


def find_user(nickname):
    users = load_users()

    return [user for user in users if user.nickname == nickname][0]


def find_super_users():
    users = load_users()

    return [user for user in users if user.access_level == 'super-usuario']


def find_by_nickname(nickname):
    users = load_users()

    return [user for user in users if user.nickname.find(nickname) >= 0]


def find_by_access_level(access_level):
    users = load_users()

    return [user for user in users if user.access_level == access_level]


def find_by_last_access(last_access):
    users = load_users()

    return [user for user in users if
            user.last_access != '' and user.last_access.find(last_access) >= 0]


@app.route('/')
def root():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            update_last_access(request.form['nickname'])
            return redirect(url_for('admin_users'))
        except IndexError:
            return render_template('login.html', error='Usuario nao encontrado!')

    return render_template('login.html')


@app.route('/users', methods=['GET', 'POST'])
def admin_users():
    error = None

    if request.method == 'POST':
        try:
            find_user(request.form['nickname'])
            error = 'Ja existe um usuario com esse nome curto: ' + request.form['nickname']
        except IndexError:
            new_user = User(
                request.form['fullname'],
                request.form['nickname'],
                request.form['role'],
                request.form['access_level'],
                request.form['last_access']
            )
            add_user(new_user)

            return redirect(url_for('admin_users'))

    search_param = request.args.get('search')
    access_level_param = request.args.get('access_level')
    last_access_param = request.args.get('last_access')
    search_value = search_param if search_param is not None and search_param.strip() != '' else None
    access_level_value = access_level_param if access_level_param is not None and access_level_param.strip() != '' else None
    last_access_value = last_access_param if last_access_param is not None and last_access_param.strip() != '' else None

    users_filtered = load_users()

    if search_value is not None:
        users_filtered = find_by_nickname(search_value)

    if access_level_value is not None:
        users_filtered = find_by_access_level(access_level_value)

    if last_access_value is not None:
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
    try:
        if request.method == b'PATCH':
            update_user(nickname, request)
            return redirect(url_for('admin_users'))

        if request.method == b'DELETE':
            found_user = find_user(nickname)
            remove_user(found_user)
            return redirect(url_for('admin_users'))

        found_user = find_user(nickname)
        return render_template('show.html', user=found_user, access_levels=access_levels)
    except IndexError:
        return redirect(url_for('admin_users'))


if __name__ == '__main__':
    app.run(debug=True, port=3000)
