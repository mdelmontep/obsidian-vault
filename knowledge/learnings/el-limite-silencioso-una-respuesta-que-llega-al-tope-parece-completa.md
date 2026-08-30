---
title: el límite silencioso — una respuesta que llega justo al tope es indistinguible de una completa
date: 2026-08-30
source: facturaia
tags: [learning, datos, herramientas, gh, postgrest, verificacion]
---

Una consulta acotada que devuelve **exactamente** el número de filas que pediste
no ha respondido a tu pregunta: ha respondido al tope. No hay error, ni aviso, ni
una lista sospechosamente corta — hay un resultado plausible y falso.

Tres puertas distintas del mismo patrón, las tres el 30-ago-2026 en `facturaia`:

- **PostgREST** recorta a 1.000 filas por `db-max-rows` (ver
  [[postgrest-max-rows-trunca-silencioso-in-revienta-url]]).
- **`gh pr list --limit 1000`**: clasifiqué 50 ramas remotas cruzándolas contra
  ese volcado. El repo iba por el PR #2316, así que todo PR anterior al ~#1316
  caía fuera y salía como «sin PR ninguno». Marqué como huérfana una rama con el
  **#610 abierto**. Lo cazó otra sesión, no yo.
- **Una lista literal de directorios** donde buscar hallazgos: las filas de una
  ola nueva no contaban, y el recuento salía verde.

**Cómo se detecta:** si `len(resultado) == límite_que_pediste`, trátalo como
truncado hasta demostrar lo contrario. Y si la pregunta es «¿existe X?», no la
respondas con un volcado paginado: pregunta por X directamente
(`gh api ...pulls?head=owner:rama&state=all`, una llamada por candidato).

**El coste asimétrico es lo que decide:** aquí el falso «no tiene PR» iba a
borrar la única copia de un trabajo. Cuando la acción que sigue es destructiva,
un listado que *parece* completo no basta como prueba.

Primo hermano, mismo día y mismo repo: un chequeo de salud que solo conoce una
forma de estar sano (`main, nav, table, [data-testid]`) declaraba caída la
pantalla de onboarding, que vive fuera del shell. **Un criterio incompleto no da
error: da un veredicto.**

Relacionado: [[internal-fetch-res-ok-silencioso]],
[[pipeline-async-solo-notifica-camino-feliz-deja-fallo-silencioso]].
