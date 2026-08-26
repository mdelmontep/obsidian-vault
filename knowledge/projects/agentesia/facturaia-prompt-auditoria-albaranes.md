---
title: encargo de auditoría del área de albaranes (TuFacturaIA)
date: 2026-08-26
source: facturaia
tags: [facturaia, albaranes, auditoria, prompt]
---


Audita de arriba abajo el módulo de albaranes: si hace lo que dice, si está
conectado en todos los sitios donde debería estarlo, y si lo que ve y toca el
usuario está a la altura del resto del producto. Repo `~/Projects/facturaia`,
rama base `origin/main`. El área es nueva: entró el 26-ago-2026 con el PR #2209
y la migración 754, así que casi nada de esto ha pasado por uso real.

## Fase 0 — documéntate antes de opinar

No arranques por el código. Abre primero, con Read explícito (nada de "creo
recordar"), y en este orden:

1. `docs/decisions/ADR-029-el-albaran-mueve-el-stock-y-la-factura-que-lo-agrupa-no-lo-vuelve-a-mover.md`
2. `supabase/migrations/754_albaranes_documento_propio.sql` entera, y su
   `supabase/tests/754_*.validate.sql` si existe
3. `docs/architecture/gotchas.md` — secciones Auth, OCR, Storage, Notificaciones,
   Truncado silencioso de PostgREST, El cuerpo de un error
4. `.claude/rules/inviolables-frontend.md` y `.claude/rules/migraciones-y-schema.md`
5. `docs/architecture/copy-humano.md` antes de juzgar un solo texto de pantalla
6. `git log origin/main -20 -- src/lib/albaranes src/components/albaranes supabase/migrations/754*`
   para saber qué se decidió y qué se corrigió después

Cuando algo del código contradiga al ADR o a un gotcha, gana el código como
descripción de la realidad y el ADR como descripción de la intención: el hallazgo
es exactamente esa diferencia.

## La superficie que tienes que cubrir

Datos y reglas (mig 754): tablas `albaranes`, `albaran_lineas`,
`albaran_factura_lineas`; vista `albaranes_facturacion`; funciones
`albaran_validar`, `albaran_eliminar`, `albaran_factura_lineas_guard`,
`albaran_lineas_bloqueo_validado`, `aplicar_movimientos_stock`,
`aplicar_movimientos_lotes`, `linea_albaran_ya_asentada_por_factura`,
`linea_factura_ya_asentada_por_albaran`, `recibida_eliminar`.

Servidor: `src/lib/albaranes/*` (`albaranes-db`, `listado-db`, `casacion`,
`casacion-db`, `estados`, `albaran-http`, `ocr-entrada`, `nombres-catalogo`) y
`src/lib/api/with-albaranes-auth.ts`.

HTTP: `src/app/api/albaranes/{route,[id]/route,[id]/validar/route,casacion/route}.ts`,
más los que hablan de lo mismo desde otro sitio: `src/app/api/obras/albaranes/**`,
`src/app/api/v1/obras/albaranes/route.ts`.

Pantallas: `src/app/(dashboard)/albaranes/**`, `src/components/albaranes/*`,
`src/components/obras/albaran-recepcion-modal.tsx`, y el panel injertado dentro
del modal de una recibida (`casacion-albaranes-panel.tsx`).

Otras bocas que crean o tocan albaranes: copiloto
(`src/lib/copiloto/tools/recepcionarAlbaran.ts` y el registry), OCR de WhatsApp
(`src/app/api/internal/whatsapp/ocr-process/_parts/ocr-process/albaran.ts`),
ingesta (`src/components/ingesta/*`), MCP (`services/mcp-server/obras.ts`,
`src/lib/mcp/tools-manifest.ts`), stock (`src/app/api/stock/drift/route.ts`,
`src/lib/facturas/movimientos-sin-partida.ts`).

## Lo que la auditoría tiene que responder

**1. ¿El invariante se sostiene?** El género entra una vez. Busca activamente el
camino que lo rompe: aprobar la factura antes de cruzar y después de cruzar,
cruzar y luego eliminar la recibida, validar parcial y facturar el resto, editar
líneas entre medias, dos usuarios a la vez. Los guardarraíles viven en las
funciones de Postgres, no en los endpoints: comprueba que ninguna boca (copiloto,
v1, OCR, Obras legacy) llega al ledger por un camino que los esquive.

**2. ¿Los dos ejes están de verdad separados en todas partes?** El eje de
facturación se deriva de la vista y nunca es una columna. Verifica que nadie lo
persiste, lo cachea ni lo recalcula por su cuenta, y que el espejo TS
`src/lib/albaranes/estados.ts` sigue cuadrando con el CHECK y la vista de la 754.

**3. ¿Está conectado donde debe?** Por cada boca de la lista de arriba: ¿puede
crear un albarán?, ¿respeta el gate de acceso (`withAlbaranesAuth`: feature
`stock` o sector Obras, 404 y no 403)?, ¿escribe auditoría (`logAgentAction`)?,
¿emite notificación cuando toca? Y al revés: sitios donde el usuario esperaría
ver el albarán y no aparece (inventario, cashflow, informes, conciliación,
fiscal, buscador global, calendario, la ficha del proveedor, la del pedido de
obra). Un hueco aquí vale más que tres nits de estilo.

**4. ¿La pantalla está a la altura?** Recorre la UI de verdad, con
`agent-browser` sobre una org sandbox de producción, en claro y en oscuro y a
ancho de móvil. Mira: componentes compartidos de `src/components/ui` en vez de
controles a mano, estados vacíos, error visible cuando la API falla, foco y
teclado, textos según `copy-humano.md`, qué pasa con 500 albaranes y con cero.
Los datos que enseña, ¿son los que la persona reconoce? Un guion donde debería
ir un nombre es un fallo, no un detalle.

**5. ¿Qué falta para que esto sea un módulo terminado?** Export, impresión del
albarán, edición de líneas, adjuntar el papel escaneado, filtro por obra,
albarán de salida, aviso de entrega sin facturar a los N días. No inventes hoja
de ruta: nombra solo lo que un cliente pediría la primera semana, con una línea
de por qué.

## Hilos ya observados — verifícalos, no los des por buenos

- Coexisten `/api/albaranes/*` (nuevo) y `/api/obras/albaranes/*` (anterior), más
  `/api/v1/obras/albaranes`. ¿Comparten los mismos guardarraíles y el mismo
  estado, o hay dos verdades?
- En el listado, los albaranes que vienen de un pedido de obra salen con el
  proveedor vacío.
- El motor de casación solo mira entregas del mismo proveedor y anteriores a la
  factura, con ventana de 60 días. ¿Es la regla correcta para quien recibe hoy y
  factura a mes vencido?
- El panel de casación vive injertado dentro del modal de la recibida, que tiene
  sus propios tests. Un fallo suyo no puede tumbar la factura.
- Hay un fallo ya corregido en la rama `fix/albaran-detalle-concepto-del-catalogo`
  (el detalle enseñaba `—` en Concepto cuando la línea salía del catálogo).
  Úsalo como calibre del tipo de defecto que hay que encontrar, y comprueba si
  el mismo patrón se repite en otras pantallas del área.

## Cómo se verifica aquí

Nada se afirma sin evidencia, y la evidencia es de tres clases: `fichero:línea`
del código que lo demuestra, una corrida que se puede repetir, o una consulta a
producción.

- Producción se lee con `psql` y **siempre** `BEGIN READ ONLY` (ver
  `docs/architecture/` y la nota de acceso a BD). Nunca DDL, nunca escritura.
- Lo que ve el cliente se comprueba conduciendo el navegador con `agent-browser`,
  no con `curl` ni con una fila correcta en Postgres.
- Si un test es la prueba de que algo funciona, muta la línea que debería
  romperlo (`~/.claude/bin/mutate`) y confirma que el test cae. Un test que no
  discrimina no es evidencia.
- Escribe solo en organizaciones `is_test`, y deja limpio lo que crees.

## Qué entregas

Un informe en `docs/architecture/AUDITORIA-albaranes-<fecha>.md`, ordenado por
gravedad, donde cada hallazgo cabe en un párrafo: qué falla, dónde
(`fichero:línea`), cómo se reproduce, y qué se hace. Ajusta la longitud a lo que
haya de verdad: sin resumen ejecutivo, sin secciones de relleno, sin repetir el
hallazgo en tres formatos. Si el área está sana en un frente, una línea diciéndolo
vale más que tres páginas describiéndolo.

Reporta todo lo que encuentres, con su gravedad al lado; el filtrado lo hago yo
leyendo el informe.

Después del informe, y solo entonces:

- **Aplica** las correcciones que sean claras y de bajo riesgo (un fallo de
  presentación, un guardarraíl que falta, un texto que engaña), en una rama y un
  PR, con `npm run gate` en verde antes de commitear. Nada de refactors ni de
  features no pedidas.
- **Propón, numeradas, sin tocar código**, las que cambien diseño, esquema o
  contrato, cada una con su alternativa y su coste. Espera OK.

Entrega el alcance pedido. Si crees que el enfoque de la auditoría está mal
planteado, dilo en una frase y sigue con lo pedido.

## Ejecución

Effort alto para decidir y sintetizar. Si repartes trabajo, hazlo solo en frentes
grandes e independientes (datos y SQL · servidor y contratos · UI y UX · las
otras bocas), **máximo cuatro subagentes en paralelo**, buscando a effort medio y
sintetizando tú. Nada de subagentes para revisar tu propio trabajo, ni para lo
que cierras en cuatro tool calls.

Narra poco: una frase antes de arrancar, un aviso solo si encuentras algo gordo o
cambias de rumbo, y al cerrar, que la primera frase sea el resultado.

Cuando el informe esté escrito y el PR de correcciones abierto, cierra con
`/code-review` sobre el diff completo.
