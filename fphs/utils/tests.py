from http import HTTPStatus

from django.test import TestCase


class RobotsTxtTests(TestCase):
    def test_get_robot_txt(self):
        self._assert_robot_txt_by_domain("firstpickhomeschool.com", "Disallow: /admin")

    def test_get_robot_txt_subdomain(self):
        self._assert_robot_txt_by_domain("test.firstpickhomeschool.com", "Disallow: /")

    def test_post_robot_txt_disallowed(self):
        response = self.client.post("/robots.txt")

        self.assertEqual(HTTPStatus.METHOD_NOT_ALLOWED, response.status_code)

    def _assert_robot_txt_by_domain(self, host, disallowed):
        response = self.client.get("/robots.txt", HTTP_HOST=host)
        lines = response.content.decode().splitlines()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response["content-type"], "text/plain")
        self.assertEqual(lines[0], "User-Agent: *")
        self.assertEqual(lines[1], disallowed)
