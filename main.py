# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import session
from flask import redirect
from flask import json

from flask_socketio import SocketIO, send

from instance.config import DevelopmentConfig

from app.models.model import db
from app.models.model import User
from app.models.model import Post
from app.models.model import Comment

from flask_wtf.csrf import CSRFProtect
from app.controllers import forms

from app.controllers.helper import date_format

from sqlalchemy import func

from flask_humanize import Humanize

app = Flask(__name__, template_folder='app/templates', static_folder='app/static')
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()
humanize = Humanize()
socketio = SocketIO()

def create_session(username = '', user_id = ''):
    session['username'] = username
    session['user_id'] = user_id

@humanize.localeselector
def get_locale():
    return 'en'

@app.errorhandler(404)
def page_not_found(e):
   return render_template('404.html'), 404

@app.before_request
def before_request():
    if 'username' not in session and request.endpoint in ['posts', 'search_post']:
        return redirect(url_for('login'))

    elif 'username' in session and request.endpoint in ['login', 'sing_up', 'index']:
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
            
            return redirect(url_for('user_page'))
            
        else:
            error_message= 'Usuario o password no validos!'
            print(User.query.filter_by(username = username).first())
            flash(error_message)

            return redirect(url_for('login'))
            
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

            return redirect(url_for('login'))
            
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

@app.route('/search_post', methods=['GET', 'POST'])
def search_post(page=1):
    posts_list = Post.query.join(User).add_columns(
                    User.username, 
                    Post.title,
                    Post.id,
                    Post.text,
                    Post.created_date).paginate(
                                        page, 
                                        app.config['POSTS_PER_PAGE'], 
                                        False)


    return render_template('main_posts.html', 
                            posts = posts_list,
                            date_format = date_format)

@app.route('/new_post', methods = ['GET', 'POST'])
def posts():
    post_form = forms.PostForm(request.form)
    if request.method == 'POST' and post_form.validate():
        
        user_id = session['user_id']
        post = Post(user_id = user_id, 
                    title = post_form.title.data,
                    text = post_form.content.data)
        
        db.session.add(post)
        db.session.commit()

        success_message = 'Post agregado!'
        flash(success_message)
        return redirect(url_for('search_post'))

    title = "Posts"
    return render_template('posts.html', title = title, form = post_form)

@app.route('/reviews/<int:post_id>', methods=['GET', 'POST'])
def reviews(post_id = Post.id):
    comment_form = forms.CommentForm(request.form)
    if request.method == 'POST' and comment_form.validate():
        
        user_id = session['user_id']
        comment = Comment(user_id = user_id,
                            post_id = post_id,
                            text = comment_form.comment.data)

        db.session.add(comment)
        db.session.commit()

        success_message = 'Comentario agregado!'
        flash(success_message)

    num = post_id
    posts = db.session.query(Post).filter_by(id=num).first()
    comment = db.session.query(Comment).filter(Comment.post_id==num).all()
    comment_len = len(comment)
    
    return render_template('reviews.html',
                            post = posts,
                            form = comment_form,
                            comment_len = comment_len,
                            comments = comment,
                            date_format = date_format)

@app.route('/users', methods=['GET'])
def users():
    m.reflect(engine)
    for table in m.values():
        print(username)
        for column in table.c:
            print(column.name)

    return render_template('users.html', users=user)

@app.route('/chatroom')
def chat():
   return render_template('chat.html')

if __name__ == '__main__':
    humanize.init_app(app)
    csrf.init_app(app)
    db.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        db.create_all()

    app.run(port=8000)