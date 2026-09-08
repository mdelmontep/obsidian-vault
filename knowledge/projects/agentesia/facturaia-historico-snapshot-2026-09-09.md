---
title: facturaia — snapshot de poda del NOW, 9-sep-2026
date: 2026-09-09
source: facturaia
tags: [cliente, facturaia, historico, snapshot]
---

Poda del 9-sep al cerrar la horda del backlog de hallazgos: **13 entradas 🟢 retiradas del NOW**
del hub ([[facturaia]]). Todas cerradas y en prod; lo que seguía pendiente de Manu se quedó
arriba, condensado en una línea. Índice: [[facturaia-historico-detallado]].

- 🟢 **Etapa de integración y sus doce cabos: CERRADO (8-sep, en prod)** — solo sigue abierto **#2538**, esperando a José hasta el 19-sep. **Tuyo**: ¿`SUPABASE_ACCESS_TOKEN` en Dokploy? Sin él el vigía no vigila. → [[facturaia-historico-eventos]] · [[core-hookspath-absoluto-hace-que-todo-worktree-corra-el-hook-del-principal]]
- 🟢 **Horda del backlog de hallazgos: CERRADA (9-sep)** — las 35 originales más 14 de arrastre; el rango ≥2590 queda a cero. Autoría en paralelo y **gate/merge en SERIE**, que era la parte no negociable. Dos de las 14 **ya estaban arregladas y solo les faltaba el cierre**: #2599 (el PR decía «Cierra», no `Closes` → [[keywords-de-cierre-de-github-solo-funcionan-en-ingles]]) y el hook del recordatorio, que diagnostiqué mal leyendo el checkout principal 211 commits por detrás → [[core-hookspath-absoluto-hace-que-todo-worktree-corra-el-hook-del-principal]]. Los cuatro arneses tocados (`pre-commit` ×2, `pre-push` ×2) **se ejercieron a sí mismos**: el hook modificado es el que corrió sobre su propio commit. → [[postgrest-mas-viejo-que-su-base-da-502-intermitentes]] · [[mutate-toma-una-custom-property-css-por-un-comentario-sql]] · [[un-marcador-de-sesion-en-git-dir-se-escribe-una-vez-por-worktree]]
- 🟢 **FacturaDirecta: el cursor deja de adelantar a lo que falló (5-sep, #2518, en prod)** — **Tuyo**: el código de impuesto de esas dos líneas, en FacturaDirecta. → [[un-cursor-incremental-que-avanza-sobre-lo-que-fallo-pierde-el-documento]] · [[dedup-key-no-debe-incluir-contenido-volatil]]
- 🟢 **Tickets 166/167/168 (2/3-sep, en prod)** — queda **#2416** (agente). → [[un-registro-que-estampa-head-vale-solo-con-el-arbol-limpio]]
- 🟢 **El reel se previsualiza con el mismo dibujo que se quema (3-sep, #2423)** — **queda**: la costura PNG→ffmpeg sin test y el choque cierre/subtítulos sin medir. → [[iframe-sandbox-vacio-deja-el-documento-en-origen-opaco]]
- 🟢 **Los slides del carrusel ya salen maquetados (2-sep, #2379, en prod)** — **queda**: lo dispara un botón; el runner todavía no maqueta solo.
- 🟢 **Tickets 125-132 de IET respondidos, el 126 corregido de raíz (1/2-sep, mig 792, ADR-069)** — **Tuyo**: la huérfana de `docs/plan/cierres.json` y el catálogo a 500k del 125. → ADR-069 · [[catch-best-effort-sin-senal-persistente-fallo-parece-no-disparo]]

- 🟢 **Ticket 169 (Chivite): cerrado y contestado (8-sep, #2639)** — el resumen semanal le mandaba al cliente el CÓDIGO del motivo. Los 302,64 € los autorizó José y están aplicados; smokes borrados. **Falta que él suba los albaranes 73059495, 73059620 y 73059582.** → [[el-texto-que-vas-a-publicar-puede-contener-el-disparador-que-dice-no-llevar]]
- 🟢 **Ticket 171 (Chivite): cerrado, cero tareas de código (7-sep)** — el cliente es **JOSÉ**, no Borja. Solo falta que diga **qué día contó** (plazo **19-sep**, issue #2538); si calla, se anota en `notas_internas` y **no se ajusta nada** — cuadrar a mano sería inventar su inventario. Detalle en [[facturaia-historico-detallado]]. → [[una-verificacion-corrida-antes-del-cambio-destructivo-prueba-el-esquema-que-vas-a-borrar]]
- 🟢 **Abono parcial: los SIETE PRs en prod y el paraguas #2426 cerrado (7-sep); ticket #170 resuelto** — de auditar esa área salió la pregunta de en qué escala se enseña la deuda: **ADR-086 mergeado el 8-sep (#2632)**, con el coste en euros ya medido en prod y con Holded de contraste. **Tuyo**: la decisión de negocio del ADR (más abajo) y si `disputada` vuelve a `pendiente`. → [[facturaia-historico-eventos]]
- 🟢 **El cobro con tarjeta ya está en el catálogo (1-sep, #2369-#2372, mig 791)** — en **borrador y sin precio**: el recorrido no cobra todavía. **Tuyo**: Backblaze (abajo) y SOCIAL MEDIA CLOUD SOLUTIONS. → [[si-lo-unico-que-frena-algo-es-un-campo-sin-rellenar-no-hay-decision]] · [[un-alcance-calculado-contra-la-rama-base-se-vacia-al-mergear]]
- 🟢 **Quién abre una ficha de cliente deja rastro, y el DPA existe (1-sep, ADR-067)** — **Tuyo**: DPA al despacho, borrar `SUPERADMIN_EMAILS` e `IA_OPS_SHOW_TRANSCRIPTS` de Dokploy, quitar superadmin a 4 de las 8 cuentas. → ADR-067 §16
