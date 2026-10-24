# -*- coding: utf-8 -*-
import ipaddress
from urllib.parse import urlsplit

from odoo import api, models
from odoo.http import request


def _is_private_ip(address):
    try:
        ip = ipaddress.ip_address(address.strip())
    except ValueError:
        return False
    ip = getattr(ip, "ipv4_mapped", None) or ip
    return ip.is_private or ip.is_loopback


def _host_name(host):
    try:
        return urlsplit("//" + host).hostname or ""
    except ValueError:
        return ""


def _is_local_host(host):
    name = _host_name(host)
    return name == "localhost" or _is_private_ip(name)


def is_lan_request():
    """Požadavek z místní sítě na adresu serveru v místní síti.

    Server je v prohlížeči zadaný privátní IP adresou (``192.168.100.9:8069``) nebo jako
    ``localhost``, ne doménou, a klient i všechny adresy v ``X-Forwarded-For`` jsou privátní.
    Přístup přes veřejnou doménu tím neprojde: hostitel je doména a reverse proxy připíše do
    ``X-Forwarded-For`` veřejnou IP návštěvníka (podvrhnout se dají jen adresy před ní).
    """
    if not request:
        return False
    httprequest = request.httprequest
    forwarded = filter(None, map(str.strip, httprequest.headers.get("X-Forwarded-For", "").split(",")))
    return _is_local_host(httprequest.host) and all(
        map(_is_private_ip, [httprequest.remote_addr or "", *forwarded])
    )


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @api.model
    def _add_public_key_to_session_info(self, session_info):
        """Stránka otevřená z místní sítě nedostane klíč reCAPTCHA: nenačítá skript Googlu
        a formuláře (i přihlašovací) se odešlou bez tokenu, takže fungují i bez internetu."""
        if is_lan_request():
            return session_info
        return super()._add_public_key_to_session_info(session_info)

    @api.model
    def _verify_request_recaptcha_token(self, action):
        """Z místní sítě se reCAPTCHA neověřuje, přes veřejnou doménu beze změny."""
        if is_lan_request():
            return
        return super()._verify_request_recaptcha_token(action)
