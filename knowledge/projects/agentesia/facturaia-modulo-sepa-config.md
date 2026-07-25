---
title: Módulo SEPA — configuración y endurecimiento del fichero
date: 2026-07-25
source: claude-code-session
tags: [facturaia, sepa, modulos-ia, pain008, pain001]
---

Spec de la PR #1201, rama `feat/sepa-modulo-config`, worktree `~/Projects/facturaia-sepa`.

## Punto de partida

La pestaña Configuración del módulo Domiciliación SEPA salía vacía y las Métricas caían al fallback genérico "Eventos (30d)". Al abrirlo aparecieron cuatro defectos que ya afectaban a ficheros reales enviados al banco.

Plan revisado antes de escribir código por tres auditorías paralelas (dominio SEPA/banca, arquitectura/datos, UX/frontend). Descartes que salieron de ahí:

- **`conciliar_auto` fuera.** Su OFF no aporta seguridad (la conciliación solo actúa con match único y exacto y pasa por `asignar_manual`, idempotente) y el cron cubre también remesas de **pago**, así que el toggle silenciaría algo fuera del alcance del módulo.
- **`{cliente}` y `{fecha}` fuera** del concepto: exigen tocar `RemesaSourceLine` y multiplican la superficie de charset para valor marginal.
- **Tab de configuración custom fuera.** Se arregló el renderer genérico, que beneficia a los 12 módulos, en vez de duplicar un `overrideTab` como el de cobros (que viola los inviolables él mismo: `<input type="time">` nativo, radiogroup a mano, validación duplicada).

## Los cuatro bugs de producción

1. **`getModuleConfig` era fail-open.** Ignoraba `error` de supabase-js, que no lanza en fallo de query, devuelve `{data:null,error}`. Un blip de BD aplicaba los defaults del catálogo como si el cliente no hubiera configurado nada, sin traza. Ahora loguea, y existe `getModuleConfigStrict` que lanza `ModuleConfigError`, obligatoria en los paths de dinero.
2. **Cero saneado al juego de caracteres SEPA** (EPC217-08: `a-zA-Z0-9/-?:().,'+` y espacio). Escapar XML no lo cubre: `&amp;` es XML bien formado pero sigue llevando un `&` que el EPC no admite. Afectaba a `Cdtr/Nm` y `Dbtr/Nm` en pain.008 **y** pain.001. Tres tests consagraban el comportamiento incorrecto.
3. **`Cdtr/Nm` (pain.008) y `Dbtr/Nm` (pain.001) sin límite de 70**, que el nombre del deudor sí tenía. Razón social larga = fichero rechazado.
4. **Fecha de cargo solo validada por regex.** Una fecha pasada o un sábado se persistían con su XML en `sepa_remesas.xml`, que es inmutable.

## Los 6 ajustes (sin migración)

`org_module_config` existe desde mig 045 y `'sepa'` está en `features` desde mig 379.

| Clave | Default | Consumidor |
|---|---|---|
| `dias_antelacion_cargo` | 2 | prefill en `remesas-view`, vía `GET /api/sepa/config` bajo clave anidada `config` |
| `concepto_remesa` | `Documento {numero}` | `RmtInf/Ustrd`, parámetro de `assemblePain008Input` |
| `apunte_agrupado` | **true** | `BtchBookg` |
| `esquema_defecto` | CORE | solo preselección en alta de mandato |
| `importe_maximo_adeudo` | 0 | guard en `generarRemesa` |
| `importe_maximo_remesa` | 0 | guard en `generarRemesa` |

## Lo que hay que recordar

- **`esquema_defecto` NUNCA se lee desde `remesa.ts`.** La verdad del esquema es `sepa_mandatos.esquema`, que refleja un documento legal firmado. Esta clave solo decide qué viene preseleccionado en el formulario de alta.
- **El default del concepto es el literal histórico** (`Documento {numero}`), así que a ninguna org que no lo toque le cambia el fichero.
- **`apunte_agrupado` SÍ cambia el fichero de todos.** Estaba fijo en `false`, que pide al banco un apunte por adeudo, justo lo contrario del lump-sum que asume `findUniqueMovimiento`. Ver [[btchbookg-false-contradice-la-autoconciliacion-lump-sum]].
- **Los topes abortan con la lista de facturas que exceden, nunca filtran en silencio**, y se comparan en céntimos.
- **`assemblePain008Input` sigue siendo pura**: la plantilla entra por parámetro, no se lee config dentro.
- La tasa de devolución se calcula por **cohorte de 90 días**, no 30d/30d: una devolución llega 5-8 semanas después del cargo (CORE da 8 semanas de reembolso sin justificar), así que dividir dos ventanas de 30 días mezcla cohortes e infraestima siempre.

## Coordinación

`issues/modia-015` (PRD `issues/PRD-modulos-ia-config.md`, 27 slices, sesión paralela del 2026-07-25) declara conflicto duro con esta rama y está **bloqueado esperando este merge** para absorber `preview` y `maxLength` en su reescritura de `ModuloConfig`. Su PRD cubre además cosas que esta PR dejó fuera a propósito: el contrato PATCH que mergea en vez de reemplazar, el toggle de conciliación y los campos placebo.

`/polish` del tab de Configuración va **después** de que aterrice modia-015, no antes: reescribe la función entera.

## Verificación

`lint`, `typecheck` y `build` limpios. 7.004 tests pasan (los 2 fallos de `obras/unidades-obra` son preexistentes en main).

Fichero real generado por el código con datos ruidosos: `Construcciones Muñoz & Hijos SL` → `Construcciones Munoz + Hijos SL`, `Peláez & Asociados S.L.` → `Pelaez + Asociados S.L.`, plantilla resuelta, `BtchBookg` a `true`. 122 nodos de texto, ninguno fuera del juego EPC, cero no-ASCII.

## Fallo posterior: mezclar relojes

Auditando el merge apareció que `hoyIso()` calculaba con `toISOString()` (UTC) mientras `remesas-view` calculaba su mínimo en hora local. Entre las 00:00 y las 02:00 de España UTC marca aún el día anterior: el servidor aceptaba un cargo el mismo día, y con `dias_antelacion_cargo=1` la UI proponía un valor por debajo de su propio mínimo, así que el campo nacía inválido y el botón de generar salía bloqueado sin que el usuario tocara nada.

Arreglado en **#1204** (`22bf05ec`): `hoyIso()` devuelve el día del calendario LOCAL, el cálculo del día de la semana se queda en UTC (que una fecha caiga en sábado es un hecho absoluto), y `minFechaCargo()` es fuente única del mínimo, equivalente por construcción a la propuesta a 1 día. El test que lo fija es un invariante sobre varias fechas de partida, no un caso con fecha fija.

Mergeado a main en `143cf3cf` + `22bf05ec` (2026-07-25). Smoke de navegador pendiente, ver hub §Smoke tests pendientes.
