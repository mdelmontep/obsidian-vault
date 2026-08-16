---
title: una protección incidental parece un hueco ya cerrado
date: 2026-08-16
source: claude-code-session
tags: [llm, grounding, presenter, seguridad, metodo]
---

Un issue describía un agujero real (un LLM que reformula un lead puede sustituir un filtro y
dejar una frase plausible y falsa). Al medirlo, **el caso descrito no podía ocurrir**: el
empty-state no llegaba al presenter y el token iba **entrecomillado**, así que caía en la regla
de «etiquetas citadas» del verificador de grounding.

Dos conclusiones opuestas, las dos malas:
- «la premisa es falsa, cierro» → pero la protección era **incidental**: vive de que la copia
  siga poniendo comillas. Un cambio de *copy* que nadie asociaría con esto la evapora **sin
  mover un test**.
- «entra tal cual, era un bug» → la PR miente sobre lo que arregla.

Lo correcto: entrar por su valor real (protección **declarada** en vez de incidental, y ahorrarse
la llamada al modelo, porque el verificador ya rechazaba incluso las reformulaciones honestas de
esa lectura) **declarando en la PR que la premisa era falsa**.

👉 Y al medir por qué el caso no ocurre, **barre los tokens hermanos del mismo lead**: ahí estaba
el que sí estaba expuesto — el *estado* (`abiertas`→`ganadas`) no es cifra, ni polaridad, ni
etiqueta citada, y ninguna fila del cuerpo lo desmentía.
Ver [[presenter-grounded-conservar-items-verbatim-no-aflojar-verificador]].
