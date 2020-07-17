# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import session
from flask import redirect

from instance.config import DevelopmentConfig

from app.models.model import db
from app.models.model import User
from app.models.model import Comment

from flask_wtf.csrf import CSRFProtect
from app.controllers import forms

from app.controllers.helper import date_format

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

def create_session(username = '', user_id = ''):
    session['username'] = username
    session['user_id'] = user_id

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['comments', 'reviews']:
        return redirect(url_for('login'))

    elif 'username' in session and request.endpoint in ['login', 'register']:
        return redirect(url_for('user_page'))

@app.route('/', methods = ['GET', 'POST'])
def index():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        
        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            
            session['username'] = username
            session['user_id'] = user.id
            
            return redirect( url_for('user_page') )
            
        else:
            error_message= 'Usuario o password no validos!'
            print(User.query.filter_by(username = username).first())
            flash(error_message)
            
        session['username'] = login_form.username.data
    return render_template('index.html', form = login_form)

@app.route('/register', methods=['GET', 'POST'])
def sing_up():
    create_form = forms.CreateForm(request.form)
    if request.method == 'POST' and create_form.validate():
        user = User(username = create_form.username.data,
                    password = create_form.password.data,
                    email = create_form.email.data)
        db.session.add(user)
        db.session.commit()
        
        # @copy_current_request_context
        # def send_message(email, username):
        #     send_email(email, username)

        # sender = threading.Thread(name = 'mail_sender',
        #                         target = send_message,
        #                         args = (user.email, user.username))

        # sender.start()

        success_message = 'Usuario registrado en la base de datos'
        flash(success_message)
    
    title = "Create"
    return render_template('create.html', form = create_form, title = title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = forms.LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data
        
        user = User.query.filter_by(username = username).first()
        if user is not None and user.verify_password(password):
            success_message = 'Bienvenido {}'.format(username)
            flash(success_message)
            
            session['username'] = username
            session['user_id'] = user.id
            
            return redirect( url_for('user_page') )
            
        else:
            error_message= 'Usuario o password no validos!'
            print(User.query.filter_by(username = username).first())
            flash(error_message)
            
        session['username'] = login_form.username.data

    return render_template('login.html', form = login_form)

@app.route('/user', methods=['GET', 'POST'])
def user_page():
   return render_template('index_session.html')

@app.route('/logout')
def logout():
    if 'username' in session:
       session.pop('username')
    return redirect(url_for('index'))

@app.route('/comments', methods = ['GET', 'POST'])
def comments():
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        
        user_id = session['user_id']
        comment = Comment(user_id = user_id, 
                        text = comment_form.comment.data,)
        
        db.session.add(comment)
        db.session.commit()

        success_message = 'Comentario agregado!'
        flash(success_message)

    title = "Comment"
    return render_template('comments.html', title = title, form = comment_form)

@app.route('/reviews', methods = ['GET'])
@app.route('/reviews/<int:page>', methods=['GET'])
def reviews(page=1):
    comment_list = Comment.query.join(User).add_columns(
                    User.username, 
                    Comment.text,
                    Comment.created_date).paginate(
                        page,
                        app.config['POSTS_PER_PAGE'],
                        False)
        
    return render_template('reviews.html',
        comments = comment_list,
        date_format = date_format)

if __name__ == '__main__':
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(port=5000)