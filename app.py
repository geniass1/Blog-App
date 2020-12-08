from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/lox')
def lox():
    return render_template('lox.html')


@app.route('/post')
def post():
    articales = Article.query.order_by(Article.date.desc()).all()
    return render_template('post.html', articales=articales)


@app.route('/post/<int:id>')
def posts(id):
    article = Article.query.get(id)
    return render_template('posts.html', article=article)


@app.route('/post/<int:id>/del')
def posts_del(id):
    article = Article.query.get_or_404(id)
    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/post')
    except ValueError:
        return 'Error'


@app.route('/post/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    article = Article.query.get(id)
    if request.method == 'POST':
        article.title = request.form['title']
        article.intro = request.form['intro']
        article.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/post')
        except ValueError:
            return 'Error'
    else:
        return render_template('update.html', article=article)


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, intro=intro, text=text)
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/post')
        except ValueError:
            return 'Error'
    else:
        return render_template('create.html')
    return render_template('create.html')


@app.route('/user/<string:name>/<int:id>')
def user(name, id):
    return f'Lox {name} {id}'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080, debug=True)
