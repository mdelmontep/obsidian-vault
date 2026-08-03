---
title: ADR-046 — los secretos se leen con service account, no se vuelcan a .env en claro
date: 2026-08-03
status: accepted
tags: [adr, seguridad, 1password, harness]
---

## Contexto
`op` pedía Touch ID en cada lectura y la shell del agente no puede pintar el prompt biométrico
(cuelgues de 60 s, `account is not signed in`). La fricción empujaba a la salida fácil: volcar todas
las credenciales de todos los proyectos a un `.env` por proyecto.

## Opciones consideradas
- **A — `.env` con los valores en claro** — cero fricción, pero secretos en disco sin rotación,
  auditoría ni caducidad, replicados en backups/copias, y a un `git add -f` de acabar en el historial.
- **B — `.env` con referencias `op://` + `op run --env-file`** — el fichero es publicable y sirve de
  `.env.example` real, pero sigue pasando por `op` interactivo: la huella no desaparece.
- **C — service account + wrapper `opsa`, y hook que bloquee el `op` de lectura** — sin huella y sin
  sesión, alcance acotado y auditable; a cambio, solo lectura, token con caducidad y ciego a las
  bóvedas personales.

## Decisión
**C**, con **B** como forma de los `.env` que hagan falta. La huella no era el problema a resolver
sino el síntoma: lo que hacía falta era una identidad no-interactiva con alcance limitado. Volcar los
valores (A) cambia una molestia recurrente por una fuga permanente.

## Consecuencias
Nos compromete a renovar el token el **2026-11-01** (al caducar, el sign in vuelve de golpe en todo y
el síntoma no dirá "caducado"). Escribir en 1Password y leer de `my.1password.com` /
`Private`/`Employee`/`Shared` siguen exigiendo `op` con huella — el hook los deja pasar a propósito.
Un secreto que quiera ser automatizable tiene que vivir en una bóveda de `agentesialab.1password.eu`,
lo que convierte "¿dónde guardo esto?" en una decisión con consecuencias, no en un detalle.
Cerramos la opción de tener credenciales en claro en el repo o junto a él.
Ver [[service-account-de-1password-exige-vault-explicito-en-item-get]] ·
[[un-wrapper-nuevo-no-se-adopta-si-no-barres-los-call-sites-escritos]]
