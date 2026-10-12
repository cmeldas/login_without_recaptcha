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

Druhý test má smysl jen v databázi s modulem `google_recaptcha` (instaluje ho `website`),
bez něj se reCAPTCHA neověřuje vůbec a test projde i bez tohoto modulu.

## Odoo 20

Větev `20.0`, verze `20.0.1.0.0`. Odoo 20 ověřuje reCAPTCHA při přihlášení stejně jako 19:
`web_login` volá `res.users._should_captcha_login(credential)` a pro heslo vrací `True`,
`auth_signup` ho dál obchází kontextem `SKIP_CAPTCHA_LOGIN`. Kód modulu se proto nemění.

- Test: Odoo 20 zrušilo `ir.config_parameter.set_param`/`get_param`, parametry mají typové
  metody (`set_str`, `set_bool`, `get_bool` …). Test proto klíče nastavuje přes `set_str`
  a `set_bool`. Modul `google_recaptcha` je čte přes `get_bool('enable_recaptcha', True)`.
- Migrace dat: žádná. Modul nemá vlastní data ani pole, na produkci (Odoo 19) je
  odinstalovaný a reCAPTCHA je tam vypnutá (`enable_recaptcha = False`).

LGPL-3, autor Matouš Čmelík.
