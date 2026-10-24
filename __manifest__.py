# -*- coding: utf-8 -*-
{
    "name": "Přihlášení z místní sítě bez reCAPTCHA",
    "summary": "Z místní sítě (server zadaný privátní IP) se reCAPTCHA neověřuje, přes veřejnou doménu beze změny",
    "description": """
Přihlášení z místní sítě bez reCAPTCHA
======================================

Odoo 19 i 20 ověřují Google reCAPTCHA u každého přihlášení heslem. Když se uživatel
přihlašuje přes adresu, která není u klíče v Google konzoli povolená (například
IP adresa serveru v místní síti), přihlášení skončí chybou „Suspicious activity
detected by google reCAPTCHA“. Bez internetu se nepřihlásí vůbec.

Modul reCAPTCHA vynechá u požadavků z místní sítě: server je v prohlížeči zadaný
privátní IP adresou nebo jako ``localhost`` a klient i adresy v ``X-Forwarded-For`` jsou privátní. Stránka
pak nenačítá skript Googlu a přihlášení (třeba na pokladně) funguje i při výpadku
internetu. Přihlášení a formuláře přes veřejnou doménu chrání reCAPTCHA dál.
""",
    "version": "20.0.2.0.1",
    "category": "Hidden/Tools",
    "author": "Matouš Čmelík",
    "website": "https://github.com/cmeldas/login_without_recaptcha",
    "license": "LGPL-3",
    "depends": ["google_recaptcha"],
    "installable": True,
    "application": False,
    "auto_install": False,
}
