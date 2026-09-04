---
title: dig ns vacío no significa dominio libre — usar rdap
date: 2026-08-02
source: claude-code-session
tags: [dns, dominios]
---
Un dominio registrado pero aparcado sin DNS delegado devuelve `dig +short NS` vacío. Comprobar
disponibilidad así da falsos libres: `charlia.com` y `clientia.com` salían "libres" y estaban registrados
desde 2007 y 2002.

Fiable, en este orden:
- `curl -s -o /dev/null -w "%{http_code}" https://rdap.org/domain/<d>` → **404 = libre**, 200 = registrado
  (y devuelve fechas y registrador en JSON, parseable).
- `whois <d> | grep -ciE "^(No match|NOT FOUND)"` como respaldo; su formato varía por TLD y en `.es` no es
  interpretable con fiabilidad.
- 5-sep: un envoltorio de `whois` dijo «LIBRE» para `holi.com`, registrado desde 1998 (RDAP lo dio
  en un segundo). Dar un dominio por libre solo con RDAP 404, nunca con whois ni dig.
