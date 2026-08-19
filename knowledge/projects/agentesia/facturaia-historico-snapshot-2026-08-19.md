---
title: facturaia — snapshot 2026-08-19 (track de contenido, spec #1908)
date: 2026-08-19
source: facturaia
tags: [cliente, facturaia, historico, contenido, marketing]
---

Detalle retirado del NOW del hub el 19-ago. El hub vivo es [[facturaia]].

## Spec #1908 — gate humano, calendario, aprendizaje y motor de edición

Nueve tickets (#1909-#1917) en dos PRs: **#1926** (`0464ee0fb`, el candado y la tabla del plan) y
**#1929** (`9a32b5020`, los otros ocho). Migraciones **713-720** aplicadas y verificadas por catálogo.
Gates finales: 1.279 ficheros, 13.332 tests, cero rojos. Deploy confirmado por comportamiento: el
`/api/health` de prod reportó `build-2026-08-19T11:18:42Z`, que es el del merge.

Qué quedó montado:

- **Gate humano pieza a pieza.** El `planificador_produccion` escribe el prompt de cada slide y de cada
  escena (fotograma y movimiento por separado) con coste estimado, y nada se genera hasta aprobarlo. El
  candado vive en `marketing_claim_next_run`, no en el panel, así que «Generar ahora» tampoco lo rodea.
  Los productores dejaron de escribir prompts: leen el plan o reciben un 409 `plan_no_aprobado`.
- **Editar y aprobar.** El `origen: humano` de un prompt lo decide el servidor comparando con lo
  guardado; el que llega del navegador se ignora, o bastaría mentir en el payload.
- **Calendario editorial.** Cuarta vista. NO se creó `fecha_objetivo`: es `scheduled_for` (mig 673), y
  la 715 solo añade índice y COMMENT. `scheduled_at` (compromiso) manda sobre `scheduled_for`
  (intención). Huecos sugeridos martes/jueves/sábado; ninguno en el pasado.
- **Rúbrica y ejemplos de oro.** Marca, realismo y gancho de 1 a 5 al aprobar, sin valores precargados.
  Lo corregido a mano pesa más que lo solo aprobado. Si el guardado de la rúbrica falla, la aprobación
  no se deshace.
- **Reglas del analista** con evidencia obligatoria (≥3 piezas). Señales por tipo y pilar; un grupo sin
  valorar sale «sin datos», no cero.
- **Compositor y motor conmutable** (ffmpeg / revideo), con override por pieza. Rótulo «Hecho con IA»
  no parametrizable.
- **Explorador de herramientas**: propuestas con licencia, coste, mejora y fuente; caducan a 90 días.

## Lo que apareció al renderizar de verdad

El compositor **no componía nada**. Cuatro fallos que la suite daba por verdes porque comparaba cadenas
de argumentos de ffmpeg en vez de ejecutarlo. Detalle técnico en
[[drawtext-de-ffmpeg-no-dibuja-nada-con-un-porcentaje-literal]]; el patrón, en
[[el-arnes-se-mide-a-si-mismo]]. Y el motor **por defecto era el que no compone**: Revideo estaba
cableado como default sin estar en ningún `package.json`, sin composición por plantilla, y con
`projectFile` recibiendo el NOMBRE de la plantilla. Se cambió a ffmpeg.

Remotion se descartó por licencia y coste: 0,01 $/render con **mínimo 100 $/mes** en cuanto la empresa
pasa de tres personas o el uso cuenta como automatización, más del triple del tope de vídeo entero.
El montaje NO cuesta ~3 €/reel como estimaba `docs/research/montaje-automatico-reels.md`: se renderiza
en el contenedor, coste marginal cero.

## Cabos, en #1959

- **Nadie transcribe**, así que no hay subtítulos: es la única historia de usuario de la spec sin
  cumplir. El interruptor está armado y en reposo. Dos caminos: proveedor de transcripción (coste
  nuevo, entra en el tope) o generar el `.srt` del guion con los tiempos de escena (gratis, menos
  exacto).
- **Cablear Revideo**: `@revideo/renderer` + Chromium en la imagen y una composición por plantilla.

## Rozaduras del día, no del track

`dependency-graph.svg` costó **cinco merges**: fichero generado de 79.000 líneas que choca en todo PR.
El propio `pre-push` ya había concluido que «nadie revisa» ese diff y a la vez manda commitearlo →
issue **#1954**. Y main estuvo en rojo por un mock ajeno (#1937): se avisó al dueño en vez de mergear
encima.
