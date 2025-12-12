import unittest
from tests import FlaskAppTestCase, FlaskAppTestCaseWithDB
from app.users.models import User
from app import db


class UserBlueprintTestCase(FlaskAppTestCase):
    def test_greetings_page(self):
        """Тест маршруту /hi/<name>."""
        response = self.client.get("/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        """Тест маршруту /admin, який перенаправляє."""
        response = self.client.get("/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"45", response.data)

    def test_login_page(self):
        """Тест маршруту /login."""
        response = self.client.get("/login")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login", response.data)

    def test_register_page(self):
        """Тест маршруту /register."""
        response = self.client.get("/register")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Register", response.data)

    def test_account_page_redirects_when_not_authenticated(self):
        """Тест перенаправлення на сторінку входу при спробі доступу до account без аутентифікації"""
        response = self.client.get("/account")
        self.assertEqual(response.status_code, 302)

    def test_users_list_page_redirects_when_not_authenticated(self):
        """Тест перенаправлення на сторінку входу при спробі доступу до списку користувачів без аутентифікації"""
        response = self.client.get("/users")
        self.assertEqual(response.status_code, 302)


class UserRegistrationTestCase(FlaskAppTestCaseWithDB):
    """Тести для тестування збереження користувача у БД при реєстрації"""

    def test_user_registration_success(self):
        """Тест успішної реєстрації користувача та збереження у БД"""
        response = self.client.post("/register", data={
            "username": "testuser",
            "email": "test@example.com",
            "password": "Pass123",
            "confirm_password": "Pass123"
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Registration successful", response.data)

        with self.app.app_context():
            user = User.query.filter_by(username="testuser").first()
            self.assertIsNotNone(user)
            self.assertEqual(user.username, "testuser")
            self.assertEqual(user.email, "test@example.com")
            self.assertNotEqual(user.password_hash, "Pass123")
            self.assertTrue(user.check_password("Pass123"))

class UserLoginLogoutTestCase(FlaskAppTestCaseWithDB):
    """Тести для тестування входу і виходу користувача на сайті"""

    def setUp(self):
        """Створюємо тестового користувача перед кожним тестом"""
        super().setUp()
        with self.app.app_context():
            user = User(username="loginuser", email="login@example.com", password="Pass123")
            db.session.add(user)
            db.session.commit()

    def test_user_login_success(self):
        """Тест успішного входу користувача"""
        response = self.client.post("/login", data={
            "username": "loginuser",
            "password": "Pass123",
            "remember_me": False
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successful", response.data)
        self.assertIn(b"loginuser", response.data)

    def test_user_login_wrong_password(self):
        """Тест входу з неправильним паролем"""
        response = self.client.post("/login", data={
            "username": "loginuser",
            "password": "Wrong123",
            "remember_me": False
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incorrect username or password", response.data)

    def test_user_login_nonexistent_user(self):
        """Тест входу з неіснуючим користувачем"""
        response = self.client.post("/login", data={
            "username": "nonexistent",
            "password": "Pass1234",
            "remember_me": False
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Incorrect username or password", response.data)

    def test_user_login_with_remember_me(self):
        """Тест входу з опцією 'Запам'ятати мене'"""
        response = self.client.post("/login", data={
            "username": "loginuser",
            "password": "Pass123",
            "remember_me": True
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Login successful", response.data)
        self.assertIn(b"remembered after closing", response.data)

    def test_user_logout(self):
        """Тест виходу користувача"""
        self.client.post("/login", data={
            "username": "loginuser",
            "password": "Pass123",
            "remember_me": False
        })

        response = self.client.get("/logout", follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Logout successful", response.data)

    def test_access_account_after_login(self):
        """Тест доступу до сторінки account після входу"""
        self.client.post("/login", data={
            "username": "loginuser",
            "password": "Pass123",
            "remember_me": False
        })

        response = self.client.get("/account")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"User Account", response.data)
        self.assertIn(b"loginuser", response.data)

    def test_redirect_to_account_when_already_logged_in(self):
        """Тест перенаправлення на account при спробі увійти, коли вже увійшли"""
        self.client.post("/login", data={
            "username": "loginuser",
            "password": "Pass123",
            "remember_me": False
        })

        response = self.client.get("/login")

        self.assertEqual(response.status_code, 302)  # Redirect
        self.assertTrue(response.location.endswith("/account"))


if __name__ == "__main__":
    unittest.main()