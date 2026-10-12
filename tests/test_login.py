# -*- coding: utf-8 -*-
import re

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestLoginWithoutRecaptcha(HttpCase):
    def test_should_not_captcha_login(self):
        self.assertFalse(self.env["res.users"]._should_captcha_login({"type": "password"}))

    def test_login_without_token_with_recaptcha_configured(self):
        """S nastavenými klíči reCAPTCHA a bez tokenu ve formuláři se přihlášení povede."""
        icp = self.env["ir.config_parameter"].sudo()
        # Odoo 20 zrušilo set_param/get_param, parametry mají typové metody set_str/set_bool.
        icp.set_str("recaptcha_public_key", "dummy-public-key")
        icp.set_str("recaptcha_private_key", "dummy-private-key")
        icp.set_bool("enable_recaptcha", True)

        page = self.url_open("/web/login")
        csrf_token = re.search(r'name="csrf_token"\s+value="([^"]+)"', page.text).group(1)
        response = self.url_open(
            "/web/login",
            data={"login": "admin", "password": "admin", "csrf_token": csrf_token},
            allow_redirects=False,
        )
        alert = re.search(r'class="alert[^"]*"[^>]*>\s*(.*?)\s*</', response.text, re.S)
        self.assertEqual(
            response.status_code, 303,
            "Přihlášení neprošlo: %s" % (alert.group(1) if alert else response.text[:300]),
        )
        self.assertNotIn("reCAPTCHA", response.text)
