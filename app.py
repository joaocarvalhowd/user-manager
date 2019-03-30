from flask import Flask, request, redirect, url_for, render_template
from user import User

app = Flask(__name__)

users = []
access_levels = ['visitante', 'usuário', 'administrativo', 'técnico', 'super-usuário']

@app.route('/')
def root():
    return redirect(url_for('index'))


@app.route('/users', methods=['GET', 'POST'])
def index():
    return render_template('index.html', users=users)


@app.route('/users/new')
def new():
    return render_template('new.html', access_levels=access_levels)


if __name__ == '__main__':
    app.run(debug=True, port=3000)
