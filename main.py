# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import flash

from instance.config import DevelopmentConfig

from flask_wtf.csrf import CSRFProtect
from app.controllers import forms

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.route('/', methods = ['GET', 'POST'])
def index():
    login_form = forms.LoginForm(request.form)
    username = login_form.username.data
    password = login_form.password.data

    if username and password is not None:
            success_message = f"Bienvenido {username}"
            flash(success_message, 'success')

    else:
        error_message= 'Usuario o password no validos!'
        flash(error_message, 'error')

    return render_template('index.html', form = login_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    username = login_form.username.data
    password = login_form.password.data

    if username and password is not None:
            success_message = f"Bienvenido {username}"
            flash(success_message, 'success')

    else:
        error_message= 'Usuario o password no validos!'
        flash(error_message, 'error')

    return render_template('login.html', form = login_form)

if __name__ == '__main__':
    csrf.init_app(app)

    app.run(port=8000)