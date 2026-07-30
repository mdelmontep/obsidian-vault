---
title: un guard de drift bidireccional acopla las PRs de sus dos lados — y añadirle la excepción lo destruye
date: 2026-07-30
source: claude-code-session agh-iberica
tags: [tests, arquitectura, colaboracion, metodo]
---
Un test afirmaba las dos direcciones entre el prompt del LLM y el registro de capacidades: *todo lo que
el prompt anuncia existe* **y** *todo lo registrado está anunciado*. La segunda mitad es la que se
olvida al planificar, y tiene una consecuencia que no es de código: **acopla las PRs**. El plan daba por
hecho «una PR para los tools, otra para el prompt»; con ese guard, la primera **pone el gate en rojo**
sola, porque registra algo que el prompt no nombra.

Y la salida fácil es la trampa: añadir una allowlist «registrado, pendiente de declarar» **debilita el
único test que caza esa asimetría, precisamente para crear esa asimetría**. Si te encuentras
excepcionando un guard para hacer justo lo que el guard vigila, la respuesta no es la excepción.

Salida buena: **partir por donde el guard no mira.** Entregar los tools escritos y probados **sin
registrarlos** — el guard solo inspecciona el registro, así que pasa; nada inalcanzable se despliega; y
la PR del otro lado (registro + prompt + evals) queda mínima y en el carril de quien la puede correr.

Corolarios:
- Al planificar, **enumera los guards bidireccionales** antes de partir el trabajo en PRs. Un guard así
  define la unidad mínima de entrega, y eso no se ve leyendo el issue.
- Si esa mitad promete una capacidad al usuario (un menú de «esto sé hacer»), **no la anuncies todavía**:
  prometer antes de ser alcanzable es una promesa rota, peor que la capacidad ausente.
- Superficie sin caller ni verificación es el mismo anti-patrón, venga de un tool no registrado o de un
  cableado cuyo consumidor aún no existe. Ver [[guard-de-clasificacion-explicita-en-vez-de-uniformidad]].
