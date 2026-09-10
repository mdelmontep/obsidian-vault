---
title: el dev server local con `.env.local` de producción convierte cada clic de QA en escritura real
date: 2026-09-10
source: agency-portal
tags: [qa, seguridad, produccion, browser]
---
`npm run dev` en localhost:3000 no significa datos de mentira. En agency-portal el
`.env.local` apunta al Supabase de PRODUCCIÓN, así que inspeccionar visualmente un
tablero con drag&drop escribe en la BD real: el 10-sep dos clics mal puestos dejaron
un proyecto en «Entregado» y otro archivado, con sus filas en `/agency/audit` — que
no se pueden borrar.

- Antes de tocar nada en un dev local, mirar a dónde apunta su env.
- La inspección con navegador sobre ese servidor es **solo lectura**: navegar por
  URL y medir con `javascript_tool`, nunca clicar controles que mutan.
- Reparar por la UI, jamás por SQL: el arreglo debe dejar su propia fila de
  auditoría. Un `update` a mano borra la huella de que hubo un fallo.

Ver [[la-ventana-del-navegador-de-inspeccion-no-reflowa-aunque-resize-diga-ok]] · [[agentesia]].
