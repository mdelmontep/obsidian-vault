---
title: una observación pierde su fuente al copiarse a un documento derivado
date: 2026-09-06
source: mandadm
tags: [documentacion, verificacion, metodo]
---
«Para recibir webhooks la app debe estar publicada» estaba en tres ficheros del plan. Otra sesión los
auditó contra `docs/meta/`, no la encontró en ninguna de las 18 páginas oficiales y me la reportó como
afirmación sin fuente. **Solo dos de las tres lo eran.**

El original, `ESTADO.md:27`, dice «**el panel avisa** de que…»: es una observación del App Dashboard,
con su testigo, escrita por la sesión que estaba dentro creando la app. Que no esté en `docs/meta/` es
lo esperado — no es documentación, es un aviso de interfaz. Las copias (`TRACKS.md`,
`RUNBOOK-HUMANO.md`) se llevaron la frase y dejaron atrás el «el panel avisa», y a partir de ahí se
leen como hecho documentado y «suspenden» cualquier auditoría contra las fuentes.

Dos reglas:
- **Al copiar una afirmación a un documento derivado, la fuente viaja con ella.** Si no cabe, va un
  puntero al original.
- **Al auditar, lee el ORIGINAL antes de declarar sin fuente a toda la familia** — y no confundas
  «no está en la documentación» con «nadie lo vio»: una observación es una fuente, solo que distinta.
Ver [[la-suposicion-de-un-agente-escrita-en-indicativo-se-lee-como-decision]]
