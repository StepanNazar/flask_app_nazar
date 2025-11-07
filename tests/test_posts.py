import unittest

from app import db
from app.posts.models import Post
from tests import FlaskAppTestCaseWithDB


class PostsBlueprintTestCase(FlaskAppTestCaseWithDB):
    def test_create_post(self):
        with self.app.app_context():
            response = self.client.post("/posts/create", data={
                "title": "My first post",
                "content": "This is TDD!",
                "category": "news",
            }, follow_redirects=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post &#39;My first post&#39; has been added!", response.data)

            post = db.session.query(Post).filter_by(title="My first post").first()
            self.assertIsNotNone(post)
            self.assertEqual(post.content, "This is TDD!")

    def test_read_post(self):
        with self.app.app_context():
            self.client.post(
                "/posts/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD!",
                    "category": "news",
            })
            response = self.client.get("/posts/read/1", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"My first post", response.data)
            self.assertIn(b"This is TDD!", response.data)

    def test_edit_post(self):
        with self.app.app_context():
            self.client.post(
                "/posts/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD!",
                    "category": "news",
                },
                follow_redirects=True,
            )
            response = self.client.post(
                "/posts/edit/1",
                data={
                    "title": "My first edited post",
                    "content": "This is TDD!",
                    "category": "news",
                },
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post &#39;My first edited post&#39; has been edited!", response.data)

    def test_delete_post(self):
        with self.app.app_context():
            self.client.post(
                "/posts/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD!",
                    "category": "news",
                },
                follow_redirects=True,
            )
            response = self.client.post("/posts/delete/1", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"Post &#39;My first post&#39; has been deleted!", response.data)

    def test_get_all_posts(self):
        with self.app.app_context():
            self.client.post(
                "/posts/create",
                data={
                    "title": "My first post",
                    "content": "This is TDD!",
                    "category": "news",
                },
                follow_redirects=True,
            )
            self.client.post(
                "/posts/create",
                data={
                    "title": "My second post",
                    "content": "This is TDD again!",
                    "category": "tech",
                },
                follow_redirects=True,
            )
            response = self.client.get("/posts/", follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn(b"My first post", response.data)
            self.assertIn(b"My second post", response.data)

if __name__ == "__main__":
    unittest.main()
