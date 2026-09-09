# Přihlášení bez reCAPTCHA (`login_without_recaptcha`)

Odoo 19 ověřuje Google reCAPTCHA u **každého přihlášení heslem**
(`res.users._should_captcha_login`). Když se uživatel přihlašuje přes adresu,
která není u klíče v Google konzoli povolená (třeba IP adresa v místní síti),
skončí to chybou „Suspicious activity detected by google reCAPTCHA“ a nepřihlásí se.

Tento modul vrací chování Odoo 18: přihlašovací formulář reCAPTCHA neověřuje.
Webové formuláře (kontakt, newsletter, e-shop) zůstávají chráněné modulem
`google_recaptcha` beze změny, klíče ani nastavení se nemění.

## Instalace

Složku modulu nakopírovat do addons, Aplikace → Aktualizovat seznam aplikací →
„Přihlášení bez reCAPTCHA“ → Instalovat. Žádné nastavení.

## Test

```
odoo -d <db> -i login_without_recaptcha --test-enable --test-tags /login_without_recaptcha --stop-after-init
```

LGPL-3, autor Matouš Čmelík.
