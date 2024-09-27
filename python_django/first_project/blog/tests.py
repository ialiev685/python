from django.test import TestCase, SimpleTestCase

from django.template.response import TemplateResponse
from django.urls import reverse

# Create your tests here.


class HomePageTest(SimpleTestCase):
    def test_url_exists(self):
        response: TemplateResponse = self.client.get("/")

        self.assertEquals(response.status_code, 200)

    def test_url_exists_by_name(self):
        response: TemplateResponse = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_template_correct_name(self):
        response: TemplateResponse = self.client.get(reverse("index"))
        self.assertTemplateUsed(response, "blog/index.html")

    def test_template_content(self):
        response: TemplateResponse = self.client.get(reverse("index"))
        self.assertContains(response, "Index")


class AboutPageTest(SimpleTestCase):
    def test_url_exists(self):
        response: TemplateResponse = self.client.get("/about/")

        self.assertEquals(response.status_code, 200)

    def test_url_exists_by_name(self):
        response: TemplateResponse = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_template_correct_name(self):
        response: TemplateResponse = self.client.get(reverse("about"))
        self.assertTemplateUsed(response, "blog/about.html")

    def test_template_content(self):
        response: TemplateResponse = self.client.get(reverse("about"))
        self.assertContains(response, "О нас")
