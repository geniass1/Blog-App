import unittest
from app import app, db, Article


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["TESTING"] = True


class TestViews(unittest.TestCase):
    def setUp(self):
        db.create_all()

    def test_index(self):
        tester = app.test_client(self)
        response = tester.get('/')
        statuscode = response.status_code
        assert statuscode == 200

    def test_lox(self):
        tester = app.test_client(self)
        response = tester.get('/lox')
        statuscode = response.status_code
        assert statuscode == 200

    def test_post(self):
        tester = app.test_client(self)
        response = tester.get('/post')
        statuscode = response.status_code
        assert statuscode == 200

    def test_posts(self):
        tester = app.test_client(self)
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text'
        )
        db.session.add(article)
        db.session.commit()
        response = tester.get(f'/post/{article.id}')
        statuscode = response.status_code
        assert statuscode == 200

    def test_posts_del(self):
        tester = app.test_client(self)
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text'
        )
        db.session.add(article)
        db.session.commit()
        response = tester.get(f'/post/{article.id}/del')
        statuscode = response.status_code
        assert statuscode == 302

    def test_update1(self):
        tester = app.test_client(self)
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text'
        )
        db.session.add(article)
        db.session.commit()
        response = tester.get(f'/post/{article.id}/update')
        statuscode = response.status_code
        assert statuscode == 200

    def test_update2(self):
        tester = app.test_client(self)
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text'
        )
        db.session.add(article)
        db.session.commit()
        response = tester.post(
            f'/post/{article.id}/update',
            data=dict(
                title='test_title', intro='test_intro', text='test_text'
            ),
            follow_redirects=True
        )
        statuscode = response.status_code
        assert statuscode == 200

    def test_create(self):
        tester = app.test_client(self)
        response = tester.post(
            '/create',
            data=dict(
                title='test_title', intro='test_intro', text='test_text'
            ),
            follow_redirects=True
        )
        statuscode = response.status_code
        assert statuscode == 200

    def test_create_get(self):
        tester = app.test_client(self)
        response = tester.get('/create')
        statuscode = response.status_code
        assert statuscode == 200

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
