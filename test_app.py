import unittest
from init import app, db
import routes  # noqa: F401 #
from werkzeug.security import generate_password_hash
from models import Article, User


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
app.config["TESTING"] = True


class TestViews(unittest.TestCase):
    def setUp(self):
        db.create_all()
        self.user = User(login='login',
                         password=generate_password_hash('password')
                         )
        db.session.add(self.user)
        db.session.commit()
        self.new_user = User.query.filter_by(login='login').first()

    def test_register(self):
        tester = app.test_client(self)
        response = tester.post(
            '/register',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode = response.status_code
        assert statuscode == 200

    def test_change(self):
        tester = app.test_client(self)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        response = tester.post(
            '/change',
            data=dict(
                login='login', password='password', new_login='login',
                new_password='password'
            ),
            follow_redirects=True
        )
        statuscode = response.status_code
        assert statuscode == 200

    def test_incorrect_login(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(login="wrong", password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'Login or password is not correct', response.data)

    def test__login_is_not_full(self):
        tester = app.test_client(self)
        response = tester.post(
            '/login',
            data=dict(password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'please fill all fields', response.data)

    def test__register_is_not_full(self):
        tester = app.test_client(self)
        response = tester.post(
            '/register',
            data=dict(password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'please fill all fields', response.data)

    def test__change_is_not_full(self):
        tester = app.test_client(self)
        response = tester.post(
            '/change',
            data=dict(password="wrong"),
            follow_redirects=True
        )
        self.assertIn(b'please fill all fields', response.data)

    def test_change1(self):
        tester = app.test_client(self)
        response = tester.get('/change')
        statuscode = response.status_code
        assert statuscode == 200

    def test_register_get(self):
        tester = app.test_client(self)
        response = tester.get('/register')
        statuscode = response.status_code
        assert statuscode == 200

    def test_user(self):
        tester = app.test_client(self)
        response = tester.get(f'/post/{self.user}')
        statuscode = response.status_code
        assert statuscode == 200

    def test_post(self):
        tester = app.test_client(self)
        response = tester.get('/post')
        statuscode = response.status_code
        assert statuscode == 200

    def test_logout(self):
        tester = app.test_client(self)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        response = tester.get('/logout')
        statuscode = response.status_code
        assert statuscode == 302

    def test_posts(self):
        tester = app.test_client(self)
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text',
            user=self.new_user
        )
        db.session.add(article)
        db.session.commit()
        response = tester.get(f'/post/{article.id}')
        statuscode = response.status_code
        assert statuscode == 200

    def test_posts_del(self):
        tester = app.test_client(self)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text',
            user=self.new_user
        )
        db.session.add(article)
        db.session.commit()
        response = tester.get(f'/post/{article.id}/del')
        statuscode = response.status_code
        assert statuscode == 302

    def test_update1(self):
        tester = app.test_client(self)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        article = Article(
            title='test_title',
            intro='test_intro',
            text='test_text',
            user=self.new_user
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
            text='test_text',
            user=self.new_user
        )
        db.session.add(article)
        db.session.commit()
        db.session.refresh(article)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        response = tester.post(
            f'/post/{article.id}/update',
            data=dict(
                title='test_title', intro='test_intro', text='test_text',
                user=self.new_user
            ),
            follow_redirects=True
        )
        statuscode = response.status_code
        assert statuscode == 200

    def test_create(self):
        tester = app.test_client(self)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        response = tester.post(
            '/create',
            data=dict(
                title='test_title', intro='test_intro', text='test_text',
                user=self.new_user
            ),
            follow_redirects=True
        )
        statuscode = response.status_code
        assert statuscode == 200

    def test_create_get(self):
        tester = app.test_client(self)
        response1 = tester.post(
            '/login',
            data=dict(
                login='login', password='password'
            ),
            follow_redirects=True
        )
        statuscode1 = response1.status_code
        assert statuscode1 == 200
        response = tester.get('/create')
        statuscode = response.status_code
        assert statuscode == 200

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
