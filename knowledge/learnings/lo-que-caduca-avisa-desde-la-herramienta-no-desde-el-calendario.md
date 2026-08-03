---
title: lo que caduca tiene que avisar desde la herramienta, no desde el calendario
date: 2026-08-03
source: claude-code-session
tags: [harness, secretos, operaciones, metodo]
---
Al montar el service account de 1Password (token a 90 días) el reflejo fue "apúntalo en
`top-of-mind` / ponme un recordatorio". Las dos cosas fallan por el mismo motivo: **el síntoma de una
caducidad no dice "caducado"**. Vuelve el sign-in en todo de golpe, o el deploy falla, y se investiga
otra cosa durante media hora. Un recordatorio a 3 meses se lee cuando ya no significa nada.

Patrón: el aviso va **dentro de la herramienta que consume lo que caduca**, disparado por uso, no por
fecha. En `~/.local/bin/opsa` son 12 líneas: constante `OPSA_TOKEN_EXPIRES`, aviso por **stderr**
desde 21 días antes y mensaje distinto si ya venció.

Detalles que lo hacen usable y no un estorbo:
- **stderr, nunca stdout** — si no, `VAR=$(opsa read …)` se lleva el aviso dentro del secreto.
- **Ventana, no aviso permanente** — fuera de los 21 días no imprime nada, o se vuelve ruido que se
  ignora justo cuando empieza a importar.
- **Silenciable** (`OPSA_NO_EXPIRY_WARN=1`) para scripts que parsean.
- **La fecha se mueve al renovar**: si no, el aviso miente y deja de creerse.

Aplica igual a certificados TLS, API keys rotables y trials que apagan features al vencer
(caso vivo: GitHub Advanced Security en TuFacturaIA).

Ver [[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]] ·
[[service-account-de-1password-exige-vault-explicito-en-item-get]]
