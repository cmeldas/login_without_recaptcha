# -*- coding: utf-8 -*-
import re

from odoo.tests import HttpCase, tagged

PUBLIC_KEY = "dummy-public-key"
LAN = {"Host": "192.168.100.9:8069", "X-Forwarded-For": "192.168.100.20"}


@tagged("post_install", "-at_install")
class TestLoginWithoutRecaptcha(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        icp = cls.env["ir.config_parameter"].sudo()
        # Odoo 20 zrušilo set_param/get_param, parametry mají typové metody set_str/set_bool.
        icp.set_str("recaptcha_public_key", PUBLIC_KEY)
        icp.set_str("recaptcha_private_key", "dummy-private-key")
        icp.set_bool("enable_recaptcha", True)

    def setUp(self):
        super().setUp()
        # Session s databází testu: bez ní Odoo hledá databázi podle dbfilter a na serveru
        # s více databázemi přesměruje na výběr databáze.
        self.authenticate(None, None)
        # Google se v testu nevolá, každý ověřovaný token je od robota.
        self.patch(type(self.env["ir.http"]), "_verify_recaptcha_token", lambda *args, **kwargs: "is_bot")

    def _login(self, headers):
        # requests páruje cookie podle hlavičky Host, session proto posíláme ručně
        cookies = {"session_id": self.session.sid}
        page = self.url_open("/web/login", headers=headers, cookies=cookies)
        csrf_token = re.search(r'name="csrf_token"\s+value="([^"]+)"', page.text).group(1)
        response = self.url_open(
            "/web/login",
            data={"login": "admin", "password": "admin", "csrf_token": csrf_token},
            headers=headers,
            cookies=cookies,
            allow_redirects=False,
        )
        return page, response

    def _assert_logged_in(self, response):
        alert = re.search(r'class="alert[^"]*"[^>]*>\s*(.*?)\s*</', response.text, re.S)
        self.assertEqual(
            response.status_code, 303,
            "Přihlášení neprošlo: %s" % (alert.group(1) if alert else response.text[:300]),
        )

    def test_lan_login_without_recaptcha(self):
        """Server zadaný IP v místní síti: stránka bez klíče a přihlášení bez tokenu projde."""
        page, response = self._login(LAN)
        self.assertNotIn(PUBLIC_KEY, page.text)
        self._assert_logged_in(response)

    def test_localhost_login_without_recaptcha(self):
        page, response = self._login({})
        self.assertNotIn(PUBLIC_KEY, page.text)
        self._assert_logged_in(response)

    def test_localhost_name_login_without_recaptcha(self):
        """Server zadaný jako localhost (Odoo v Dockeru na vlastním PC, klient je brána Dockeru)."""
        page, response = self._login({"Host": "localhost:8089", "X-Forwarded-For": "172.18.0.1"})
        self.assertNotIn(PUBLIC_KEY, page.text)
        self._assert_logged_in(response)

    def test_public_domain_keeps_recaptcha(self):
        """Přes doménu (reverse proxy) se reCAPTCHA ověřuje dál, i když je klient v LAN."""
        page, response = self._login({"Host": "nasamotach.cz", "X-Forwarded-For": "192.168.100.20"})
        self.assertIn(PUBLIC_KEY, page.text)
        self.assertEqual(response.status_code, 422)
        self.assertIn("reCAPTCHA", response.text)

    def test_public_client_keeps_recaptcha(self):
        """Veřejná IP v X-Forwarded-For (připsaná proxy za podvržené adresy) znamená internet."""
        _page, response = self._login(dict(LAN, **{"X-Forwarded-For": "192.168.100.20, 8.8.8.8"}))
        self.assertEqual(response.status_code, 422)
