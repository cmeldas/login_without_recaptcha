# Přihlášení z místní sítě bez reCAPTCHA (`login_without_recaptcha`)

Odoo 19 i 20 ověřují Google reCAPTCHA u **každého přihlášení heslem**
(`res.users._should_captcha_login` → `ir.http._verify_request_recaptcha_token('login')`).
Když se uživatel přihlašuje přes adresu, která není u klíče v Google konzoli povolená
(IP adresa serveru v místní síti), skončí to chybou „422: Suspicious activity detected by
google reCAPTCHA“. Při výpadku internetu se nepřihlásí vůbec.

Modul vynechá reCAPTCHA **jen u požadavků z místní sítě**. Přihlášení i formuláře přes
veřejnou doménu chrání reCAPTCHA dál beze změny.

## Co je „místní síť“

Obě podmínky zároveň:

1. server je v prohlížeči zadaný **privátní IP adresou** (`http://192.168.100.9:8069`), ne
   doménou;
2. klient (`remote_addr`) i všechny adresy v `X-Forwarded-For` jsou privátní nebo loopback.

Přístup přes doménu (reverse proxy) má jako hostitele doménu, takže reCAPTCHA zůstane, i když
je klient doma. Reverse proxy navíc připíše do `X-Forwarded-For` veřejnou IP návštěvníka.
Podvrhnout jde jen adresy před ní, takže ani podvržená hlavička `X-Forwarded-Host` reCAPTCHA
nevypne.

Pro stránku z místní sítě modul:

- nedá do session klíč reCAPTCHA (`_add_public_key_to_session_info`): stránka nenačítá
  skript Googlu a formuláře se odešlou bez tokenu;
- neověřuje token (`_verify_request_recaptcha_token`), pro přihlášení ani formuláře.

Přihlášení na pokladně přes IP adresu serveru tak funguje i bez internetu.

## Nasazení za reverse proxy

V `odoo.conf` musí být `proxy_mode = True` a proxy před Odoo musí posílat `X-Forwarded-Host`
(adresu, kterou zadal prohlížeč) a `X-Forwarded-For` s **připsanou** adresou klienta
(`$proxy_add_x_forwarded_for`), ne převzatou od klienta. Bez `proxy_mode` vidí Odoo adresy
přímo a modul funguje taky.

## Instalace

Složku modulu nakopírovat do addons, Aplikace → Aktualizovat seznam aplikací →
„Přihlášení z místní sítě bez reCAPTCHA“ → Instalovat. Žádné nastavení.

## Test

```
odoo -d <db> -i website,login_without_recaptcha --test-enable --test-tags /login_without_recaptcha --stop-after-init
```

Testy nastaví klíče reCAPTCHA a ověření u Googlu nahradí odpovědí „robot“. Kontrolují
přihlášení z LAN (`Host: 192.168.100.9:8069`) a z localhostu bez tokenu, a že přes doménu
a s veřejnou IP v `X-Forwarded-For` přihlášení skončí chybou 422.

## Historie

- `20.0.2.0.0`: reCAPTCHA se vynechává jen z místní sítě, přes veřejnou doménu zůstává.
  Modul závisí na `google_recaptcha` (dřív `web`) a přepisuje `ir.http` místo `res.users`.
- `20.0.1.0.0` (a `19.0`): přihlašovací formulář reCAPTCHA neověřoval nikdy (chování Odoo 18).

LGPL-3, autor Matouš Čmelík.
