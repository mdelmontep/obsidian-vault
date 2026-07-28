---
title: no midas cls contra next dev — strictmode desmonta un nodo ya pintado
date: 2026-07-28
source: claude-code-session
tags: [next, react, performance, cls, medicion]
---

`reactStrictMode` está ACTIVO por defecto en `next dev`, así que los efectos corren dos veces:
montar → efecto → cleanup → efecto otra vez.

Un componente con este patrón —muy común— se **desmonta después de haberse pintado**:

```ts
useEffect(() => { load() }, [dep])        // load() empieza con setLoading(true)
if (loading || !datos) return null        // ← el 2º efecto lo devuelve a null
```

Secuencia en dev: pinta con datos (540 px) → el 2º efecto hace `setLoading(true)` → `null` → vuelve.
En la atribución por `sources` eso sale como `540 → 0`, un salto **hacia arriba** que en producción
no existe, y con un valor enorme. Me pasé un buen rato buscando por qué el nodo "desaparecía"
cuando el bug real era el contrario (aparecer de la nada sin hueco reservado).

Reglas:
- El CLS se mide contra `next build && next start`. El dev server sirve para **señalar al culpable**
  por `sources`, no para dar una cifra.
- Y tampoco con la máquina ocupada: la contención de CPU infla el número igual de bien.

Ver [[cero-mientras-carga-no-es-cero-vacio-y-provoca-cls]] ·
[[ssr-seed-contra-cls-de-client-fetch-en-app-router]] · [[medir-cwv-autenticado-sin-lighthouse]] · [[facturaia]]
