# -*- coding: utf-8 -*-
from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _should_captcha_login(self, credential):
        """Přihlášení heslem bez ověření reCAPTCHA (chování Odoo 18).

        Odoo 19 vrací True pro každé přihlášení heslem a ``web_login`` pak volá
        ``ir.http._verify_request_recaptcha_token('login')``. Webové formuláře
        používají jinou cestu (``_verify_request_recaptcha_token`` s vlastní akcí),
        těch se tato změna netýká.
        """
        return False
