---
title: fine-grained PAT no puede apuntar a repo de org si la cuenta es colaborador externo
date: 2026-06-16
source: claude-code-session
tags: [github, pat, auth, bot]
---

Para una cuenta bot que es **colaborador externo** de un repo de organización (no
miembro de la org), un **fine-grained PAT** NO sirve: solo puede scopear a repos cuyo
*resource owner* sea la propia cuenta o una org de la que es miembro; el repo de la org
no aparece en el selector. El picker solo muestra los repos propios del bot.

Soluciones:
- **Token classic con scope `repo`** (funciona para cualquier repo al que la cuenta
  tenga acceso, incl. como colaborador externo). Es más amplio, pero si el bot solo
  tiene acceso a 1 repo el radio es mínimo. ← usado en Resolver-con-Claude.
- O meter al bot como **miembro de la org** + habilitar fine-grained a nivel org +
  resource owner = la org (expone el bot a más repos de la org → peor aislamiento).

Para que el bot NO pueda mergear (solo abrir PR): no hay scope que separe push de merge;
el candado es **infra** (ruleset en `main` con el bot fuera del bypass), no el token.
