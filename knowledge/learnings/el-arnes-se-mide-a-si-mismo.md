---
title: el arnés se mide a sí mismo
date: 2026-08-19
source: facturaia
tags: [arnes, testing, gates, mocks]
---
Siete casos en dos días, en dos sesiones distintas, y son la misma familia: **lo verde no era el
sistema, era el espejo.**

- Un gate que **construye la orden** en vez de ejecutarla: comparaba cadenas de argumentos de ffmpeg,
  así que daba verde con un `{DUR}` sin sustituir, `drawtext` sin fuente y un `%` que hacía que no se
  dibujara nada saliendo con éxito.
- Un **mock que declara una cadena** que la implementación ya no usa: cerraba en `.in()` cuando el
  código pasó a `.in().order().range()`. Y su variante peor — un `.range()` de adorno que devuelve el
  lote entero da verde sobre una implementación que recorta en silencio.
- Un **check que solo corre cuando alguien se acuerda**: `gen:types:check` no estaba en hooks ni en CI,
  y el prompt de continuación lo presumía como parte del gate.
- Un gate que comprueba que el fixture **LEE** el CSS, no que lo **INSERTE** en la página: quitando
  el `<style>${boton}</style>` y dejando la lectura intacta seguía verde, con la maqueta midiendo
  chrome nativo. Medir la intención en vez del efecto. Lo cazó `mutate`, no releerlo — y lo escribí
  yo cuatro horas antes de que me lo cazara.
- Un **default que nadie ejecutó nunca**: el motor de composición cableado por defecto no componía.

**Regla**: un arnés solo vale si en algún momento se ejecuta **la cosa real** — renderizar el vídeo,
correr la suite entera, aplicar la migración y mirar el catálogo. Y el mock tiene que poder distinguir
la implementación buena de la mala: si no reproduce el límite que causa el bug (el recorte a 1.000 de
PostgREST), no es un gate.

- **Dos gates que aseveraban sobre la FUENTE en vez del comportamiento**: comprobaban que el guard
  ESTUVIERA escrito, así que poniéndolo a `if (false)` seguían verdes. Los dos los escribí yo el mismo
  día. Fix: extraer el predicado a una función y probarlo por comportamiento; al test de fuente le
  queda medir el CABLEADO, que es lo único que sabe medir.

**Y el arnés E2E de este repo tiene la misma forma a otra escala**: comprueba que *algo* responde en
`baseURL`, no que responda *tu* checkout. Con `.env.test` fijando el puerto 3002 y cinco worktrees
vivos, toda la suite medía el código de otra rama sin que nada lo dijera, porque lo que anota el setup
(`baseURL`, `puerto`, `pids`) no incluye de qué checkout es el servidor.

Eje distinto del de [[una-suite-en-verde-no-prueba-el-camino-real]], que va del entorno; este va de
**qué se mide**. Y de [[verificar-la-conclusion-no-solo-la-evidencia]], que va de a quién se cree.
