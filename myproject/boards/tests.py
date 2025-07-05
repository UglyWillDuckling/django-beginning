from django.test import TestCase
from django.urls import reverse
from django.urls import resolve

from .views import home, board_topics

from .models import Board


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
        board_topics_url = reverse("board_topics", kwargs={"pk": 1})
        response = self.client.get(board_topics_url)
        self.assertContains(response, 'href="{0}"'.format(reverse("home")))
