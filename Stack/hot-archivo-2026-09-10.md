---
title: hot archivo 2026-09-10
date: 2026-09-10
tags: [stack, index, archivo]
---

# Hot — archivado el 10-sep-2026

Salieron de [[hot]] por antigüedad (>2 semanas, 17–26 de agosto). Siguen vivas: el wikilink de
cada una lleva a su learning completo.

- **Un cero solo discrimina si el evento PUDO ocurrir** — y una ventana anclada al arranque caduca con cada merge (autodeploy recrea el contenedor, incluso en un merge solo-docs ajeno): ancla al EVENTO. Ver [[una-ventana-de-observacion-anclada-al-arranque-caduca-con-cada-merge]]
- **Un check rojo que muere en 3 s sin pasos es la plataforma** — mira si `main` también falla antes de depurar la rama. Ver [[un-check-que-muere-en-segundos-sin-ejecutar-pasos-es-la-plataforma]]
- **La vía que nadie recorre se pudre sin ruido** — webhook a cero tapado por el cron: la proporción entre las dos fuentes es señal de salud. Ver [[una-verificacion-que-nadie-ejerce-puede-llevar-meses-rota]]
- **Sesión de app Supabase sin password ni Node** — `generate_link` → `curl -w '%{redirect_url}'` → cookie `base64-`+b64url a mano; el action_link no inicia sesión en apps code-flow. Ver [[cookie-de-supabase-ssr-a-mano-para-smokes-sin-node]]
- **La frescura del evento solo decide revivir, nunca limpiar el error** — con crons que reprocesan timestamps fijos, condicionar la limpieza a "evento nuevo" deja el error pintado días. Ver [[la-frescura-del-evento-solo-decide-revivir-nunca-limpiar-el-error]]
- **El orden del `||` decide el copy, no quién lo revisó** — `detail || error || 'frase'` tapa el texto del cliente con el error interno. Ver [[el-detail-tecnico-se-pinta-antes-que-la-frase-humana-y-la-tapa]]
- **Un push que falla pasa por éxito** — se verifica por SHA (`ls-remote` == `rev-parse`), nunca por exit code. Van dos veces. Ver [[push-que-falla-por-red-imprime-everything-up-to-date-al-final]]
- **Una pestaña instrumentada da por inerte una app sana** — antes de declarar caída, reprodúcelo en un navegador limpio. Ver [[pestana-instrumentada-da-inerte-lo-que-esta-sano]]
- **Un fallo transitorio que ESCRIBES se lee luego como veredicto** — enum con el porqué + barrido que lo deshiele, y el catálogo del tercero se PREGUNTA (no se declara). Ver [[un-fallo-transitorio-guardado-en-una-columna-se-lee-como-veredicto]]
- **«SIN VÍCTIMA» tiene CUATRO lecturas** — hueco de test, mutante equivalente, **guard equivocado**, o el barrido saltó los tests relevantes (mira el conteo de skips del control ANTES de creerlo). Ver [[un-mutante-sin-victima-tambien-puede-ser-un-guard-equivocado]] · [[el-barrido-que-salta-los-tests-relevantes-dice-sin-victima]]
- **Un trinquete que mide por FICHERO absuelve al que ya importa el helper** — anclar en la OCURRENCIA, no en el import. Ver [[un-trinquete-por-fichero-absuelve-al-que-ya-importa-el-helper]]
- **El coste de Claude Code está en el tamaño de sesión, no en el CLAUDE.md** — 77 % es cache-read y el 91 % se gasta por encima de 200k. Y un `paths:` de rules dispara con `Read`, **no con Bash**. Ver [[donde-se-va-el-coste-de-claude-code-no-es-el-claude-md]]
- **Un hook que resuelve git en el cwd de la SESIÓN juzga otro checkout** — y renunciar (`exit 0` al ver un `cd`) lo deja decorativo justo donde importa. Ver [[hook-que-resuelve-git-en-el-cwd-de-la-sesion-juzga-el-repo-equivocado]]
- **Un control que afirmas a un cliente necesita REGISTRO con fecha** — una afirmación de control no la caza ningún test, solo una auditoría. Ver [[un-control-que-un-documento-cliente-facing-afirma-necesita-registro]]
