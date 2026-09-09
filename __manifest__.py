# -*- coding: utf-8 -*-
{
    "name": "Přihlášení bez reCAPTCHA",
    "summary": "Přihlášení heslem neověřuje Google reCAPTCHA (chování Odoo 18), webové formuláře zůstávají chráněné",
    "description": """
Přihlášení bez reCAPTCHA
========================

Odoo 19 ověřuje Google reCAPTCHA u každého přihlášení heslem. Když se uživatel
přihlašuje přes adresu, která není u klíče v Google konzoli povolená (například
IP adresa v místní síti), přihlášení skončí chybou „Suspicious activity detected
by google reCAPTCHA“.

Modul vrací chování Odoo 18: přihlašovací formulář reCAPTCHA neověřuje. Ochrana
webových formulářů (kontakt, newsletter, e-shop) modulem ``google_recaptcha``
zůstává beze změny.
""",
    "version": "19.0.1.0.0",
    "category": "Hidden/Tools",
    "author": "Matouš Čmelík",
    "website": "https://github.com/cmeldas/login_without_recaptcha",
    "license": "LGPL-3",
    "depends": ["web"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
