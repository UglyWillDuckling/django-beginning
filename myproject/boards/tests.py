from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from .views import home, board_topics, new_topic

from .models import Board, Post, Topic


class HomeTests(TestCase):
    def setUp(self) -> None:
        self.board = Board.objects.create(name="Django", description="Django board.")
        url = reverse("home")
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse("home")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_home_resolves_view(self):
        view = resolve("/")
        self.assertEqual(view.func, home)

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse("board_topics", kwargs={"pk": self.board.pk})
        self.assertContains(
            self.response, 'href="{0}"'.format(board_topics_url)
        )  # this will insert board_topics_url at {0}


class BoardTopicsTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django Board.")

    def test_board_topics_view_success_status_code(self):
        url = reverse("board_topics", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_board_topics_view_not_found_statu_code(self):
        url = reverse("board_topics", kwargs={"pk": 99})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve("/boards/1/")
        self.assertEqual(view.func, board_topics)

    def test_board_topics_view_contains_link_back_to_homepage(self):
        home_url = reverse("home")
        new_topic_url = reverse("new_topic", kwargs={"pk": 1})

        response = self.client.get(reverse("board_topics", kwargs={"pk": 1}))
        self.assertContains(response, 'href="{0}"'.format(home_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTests(TestCase):
    def setUp(self):
        Board.objects.create(name="Django", description="Django board.")
        self.url = reverse("new_topic", kwargs={"pk": 1})

    def test_new_topic_view_success_code(self):
        url = reverse("new_topic", kwargs={"pk": 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_not_found_code(self):
        url = reverse("new_topic", kwargs={"pk": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_url_resolve_new_topic_view(self):
        view = resolve("/boards/1/new/")
        self.assertEqual(view.func, new_topic)

    def test_contains_link_back_to_board_topics(self):
        new_topic_url = reverse("new_topic", kwargs={"pk": 1})
        board_topics_url = reverse("board_topics", kwargs={"pk": 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))

    def test_csrf(self):
        response = self.client.get(self.url)
        self.assertContains(response, "csrfmiddlewaretoken")

    def test_new_topic_valid_post_data(self):
        data = {"subject": "Test title", "message": "Lorem"}
        self.client.post(self.url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())

    def test_new_topic_invalid_data(self):
        """
        Invalid post data should not redirect.
        """
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, 200)

    def test_with_empty_fields(self):
        """Invalid data should not redirect."""
        data = {"subject": "", "message": ""}
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.Post.objects.exists())
