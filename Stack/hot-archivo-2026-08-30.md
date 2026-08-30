---
title: hot cache — archivo 2026-08-30
date: 2026-08-30
source: facturaia
tags: [stack, index, archivo]
---

# Hot cache — lo movido el 2026-08-30

Catorce entradas del bloque de arriba de `Stack/hot.md`, las más antiguas que quedaban sin reincidir.
**Ninguna está mal ni caducada**: conservan su `[[wikilink]]`, que es lo que las hace recuperables
navegando. Salen del hot porque el hot se lee en CADA sesión sin disparador, y ese coste solo lo
justifica lo que va a volver a pasar esta quincena. Anteriores → [[hot-archivo-2026-08-18]] · [[hot-archivo-2026-08-01]].

- **Cuenta los motores que calculan el mismo número antes de arreglar uno** — una función SQL y su espejo TS divergen en silencio; el issue nombraba 1 de 2 mitades y 1 de 3 patas. Ver [[cuenta-los-motores-que-calculan-el-mismo-numero-antes-de-arreglar-uno]]
- **«¿Existe X?» se busca por la LLAMADA, no por el módulo** — la carpeta esperada contesta otra pregunta. Ver [[buscar-una-capacidad-por-su-llamada-no-por-el-modulo-donde-crees-que-vive]]
- **Un guard que mide un sustituto bloquea sin que nadie pruebe el hecho** — si aborta ANTES de intentar la operación, el error nunca aparece (once días parados). Comprueba el RESULTADO al final, no el permiso al principio. Ver [[un-guard-que-mide-un-sustituto-bloquea-sin-que-nadie-pruebe-el-hecho]]
- **Acotar una API por scopes no la acota** — rutas distintas comparten scope: allowlist de endpoints en el wrapper, así una ruta nueva nace fuera. Ver [[acotar-una-api-por-scopes-no-la-acota-usa-allowlist-de-endpoints]]
- **Borrar una rama es un paso APARTE, al final** — encadenado con `&&` corre aunque el merge falle y **cierra la PR sin reabrirla**. Ver [[el-borrado-de-rama-nunca-va-encadenado-al-merge]] · [[gh-pr-merge-delete-branch-no-borra-la-rama-si-falla-su-checkout-local]]
- **Un grep negativo por el nombre del origen es ciego a un renombrado en la frontera** — probaba que el identificador no está, no que el dato no llegue: cruzaba con otro nombre. Persíguelo desde el PRODUCTOR. Ver [[un-grep-negativo-por-el-nombre-del-origen-es-ciego-a-un-renombrado-en-la-frontera]]
- **Un barrido devuelve cero sin decir que no midió** — `git grep -E` sin `\s`, zsh sin word-splitting, `:t` modificador. Control en las dos direcciones. Ver [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]]
- **Un agente muerto deja un motor desacoplado vivo** — sube por `ppid`; `TaskStop` no vale. Ver [[un-agente-muerto-puede-dejar-un-motor-desacoplado-vivo]]
- **Aseverar el `import` no asevera la llamada** — `toContain("import { X")` sigue verde si otra función ocupa el sitio de `X`; asevera el USO. Ver [[aseverar-sobre-el-import-no-asevera-sobre-la-llamada]]
- **Probar la aritmética no prueba el cableado** — 5 tests de la función pura en verde con el DTO pasándole un `0`; cubre también quién le pasa los argumentos. Ver [[probar-la-aritmetica-no-prueba-el-cableado-que-la-invoca]]
- **Rojo de la suite + máquina saturada ≠ regresión** — 3 corridas, 3 conjuntos de rojos sin solape; pasan aislados. Mira la duración antes que el nombre (123 s vs 11.780 s). No solapes gates. Ver [[la-suite-completa-bajo-paralelismo-no-distingue-regresion-de-saturacion]]
- **Vitest descarta la salida de los tests que PASAN** — todo reporte de un arnés que no falla (gaps conocidos, ramas que se comparan entre corridas) se pierde: `process.stdout.write`, y compruébalo con una corrida real. Ver [[un-gap-que-no-se-lee-es-un-gap-que-nadie-cierra]]
- **Dos capturas idénticas byte a byte no son un tema oscuro: es que el tema no cambió** — si la app lleva el tema en `dataset.theme` (no en `prefers-color-scheme`), `emulateMedia` no toca nada: siembra la precondición y **asevérala**. Ver [[dos-capturas-identicas-byte-a-byte-es-que-el-tema-no-cambio]]
- **Un permiso concedido midiendo caduca con la medición** — el mismo `null` dice «no abras» y «no cierres». Ver [[un-gate-abierto-con-la-metrica-caducada-no-vuelve-a-cerrarse]]
