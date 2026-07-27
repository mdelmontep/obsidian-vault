---
title: una cuota medida en tokens no se le enseña al usuario como "consultas"
date: 2026-07-28
source: claude-code-session
tags: [ux, copy, llm, billing, facturaia]
---

El modal de límite del Copiloto decía: *"Has consumido 519152 de 500000 **consultas** permitidas
este mes"*. La org había enviado **13 mensajes**. La cuota real era `copiloto_tokens_mes` y cada
turno manda un contexto grande, así que la cifra era **cierta y a la vez inservible**: nadie sabe
cuántos tokens gasta un mensaje suyo, y medio millón de "consultas" solo consigue alarmar.

- Una métrica interna (tokens, filas, bytes) no se traduce a una unidad de usuario cambiándole el
  nombre. O se convierte a algo que reconozca (mensajes, documentos) o **no se enseña la cifra**:
  "Has agotado el uso del Copiloto de este mes en tu plan actual."
- Señal de alarma en un modal parametrizable por recurso: la copy trae `unidad` en plural y alguien
  la rellenó con el sustantivo que sonaba bien, no con lo que cuenta el contador. Cotejar la copy
  contra la `limit_key` de la cuota, no contra el nombre del módulo.
- De rebote: con esa cuota agotada el módulo queda inutilizable hasta el día 1 del mes siguiente,
  así que en un entorno de test hay que subir el tope (`org_limits`), no esperar.

Ver [[coste-derivado-de-tokens-mensaje-vs-columna-tool-calls-vacia]] · [[facturaia]]
