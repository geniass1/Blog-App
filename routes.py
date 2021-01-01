from flask import render_template, request, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from init import app, db
from models import Article, User


@app.route('/login', methods=['POST', 'GET'])
def login_page():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        user = User.query.filter_by(login=login).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect('/post')
        else:
            flash('Login or password is not correct')
            return render_template('login.html'), 401
    else:
        if request.method == 'POST':
            flash('please fill all fields')

    return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    login = request.form.get('login')
    password = request.form.get('password')
    if request.method == 'POST':
        if not login or not password:
            flash("please fill all fields")
        else:
            hash_ps = generate_password_hash(password)
            new_user = User(login=login, password=hash_ps)
            db.session.add(new_user)
            db.session.commit()

            return redirect('/login')

    return render_template('register.html')


@app.route('/change', methods=['POST', 'GET'])
def change():
    login = request.form.get('login')
    password = request.form.get('password')
    new_password = request.form.get('new_password')
    if request.method == 'POST':
        if not login or not password:
            flash("please fill all fields")
        user = User.query.filter_by(login=login).first()
        if user is None:
            flash("User dosent exist")
        else:
            if user and check_password_hash(user.password, password):
                hash_ps = generate_password_hash(new_password)
                user.login = request.form.get('new_login')
                user.password = hash_ps
                db.session.commit()
                return redirect('/login')
    return render_template('change_login.html')


@app.route('/post/<user>')
def user_page(user):
    articales = Article.query.order_by(Article.date.desc())
    return render_template('user_page.html', articales=articales,
                           page_user=user)


@app.route('/logout', methods=['POST', 'GET'])
@login_required
def logout():
    logout_user()
    return redirect('/post')


@app.route('/')
@app.route('/post')
def index():
    articales = Article.query.order_by(Article.date.desc()).all()
    return render_template('post.html', articales=articales)


@app.route('/post/<int:id>')
def posts(id):
    article = Article.query.get(id)
    return render_template(
        'posts.html', article=article, current_user=current_user
    )


@app.route('/post/<int:id>/del')
@login_required
def posts_del(id):
    article = Article.query.get_or_404(id)
    db.session.delete(article)
    db.session.commit()
    return redirect('/post')


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
@login_required
def update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('update.html', article=article)


@app.route('/create', methods=['POST', 'GET'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']
        article = Article(
            title=title, intro=intro, text=text, user=current_user
        )
        db.session.add(article)
        db.session.commit()
        return redirect('/post')
    else:
        return render_template('create.html')
