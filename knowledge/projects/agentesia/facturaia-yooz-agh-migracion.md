---
title: TuFacturaIA como sustituto de Yooz para AGH Ibérica — plan
date: 2026-08-30
source: facturaia, agh-iberica
tags: [facturaia, agh, yooz, cegid, migracion, plan]
---

# TuFacturaIA como sustituto de Yooz para AGH Ibérica

Plan vivo. Sustituye a la versión conversacional del 30-ago; se actualiza aquí.

## 1. Punto de partida verificado en el tenant de AGH

Explorado en `eu1.getyooz.com` con la sesión de Giuliana Gandolfo, solo lectura salvo la
creación de `TRA_PRUEBA` (copia de la exportación, borrable).

- **Es un piloto aparcado.** El backlog de compras de enero-2026 se subió a mano el 11-12 de
  marzo de 2026. Después solo hubo dos episodios: una prueba el 26/06/2026 y cuatro capturas
  sueltas el 03/07/2026 (RENFE, Edenred y dos más). Nada más en cinco meses.
- **39 de 46 documentos siguen en estado «registro»** — sin codificar.
- **La captura por correo no está configurada.** El único canal usado fue la subida manual.
- **Nunca se ha ejecutado una sola exportación.** Cero ficheros generados desde marzo.
- Hay **un documento preparado desde el 26/06/2026** (factura de compra 20260566605, DKV,
  base 2.033,48 €) que lleva dos meses en la cola sin salir.
- Solo hay **4 usuarios**, todos `@agh-consulting.com`. **Mazars no es usuario del tenant**:
  el fichero no les llega por Yooz.
- **Coste de cambio hoy ≈ 0.** No hay histórico coherente que preservar dentro de Yooz.

### Configuración de la exportación a Mazars (`TRA_MAZARS`)

```
Adaptador ............ Yourcegid CommunicationsSx TRA
Servicio ............. Exportación Contable
CEGID version ........ V9        File origin ..... Expert
Movement type ........ Accounting entry
Codificación ......... Latin1    Saltos de línea . CRLF (Windows)
Agregación ........... ninguna   Divisa .......... solo euro
Field Ref externe .... Numéro de pièce comptable
Champ Ref interne .... Numéro du document
Fill section field ... Third code     Pdf prefix ... .\
Estrategia ........... un archivo por organización (+ código de sociedad en el nombre)
Add yooz number in ref lib field ....... ON
Add document date in DATEREFEXTERNE .... ON
Exclude dimension(s) from final export .. VACÍO
Numeración de pieza contable ........... DESACTIVADA
Frecuencia ........... Una vez al día
Destinatarios ........ Daniela ESCALONA; Giuliana Gandolfo
```

Hay una segunda exportación, `YZ_GENERIC_V2` (Yooz Standard CSV, frecuencia *Manualmente*),
que es la única con cola viva. La pantalla «Mis exportaciones» solo lista colas manuales, y
Yooz prepara cada documento para las exportaciones **existentes en el momento de la
preparación** — por eso una copia creada hoy no ve documentos ya preparados.

## 2. Formato `.TRA` — resuelto, sin dependencia de Mazars

Fuente: `CegidUniverselAdapter.pdf` (*CEGID V9 and Y2 / XRP Sprint — Adapter Specification*,
V1.0, 22/03/2024, 33 pp.), descargado del propio tenant vía ⋮ → «Descarga la documentación».

- **Ancho fijo, sin separadores.** Cada campo con posición y longitud (`at=`, `length=`);
  se trunca si excede.
- **Cabecera obligatoria de 147 bytes**: `***` + `S5` + origen (`CLI`/`EXP`) + `JRL` + `ETE` +
  huecos + `009` (V9) + `ddMMyyyyhhmm` + `YOOZ` + rellenos. El filler que lleva a 150 es solo Y2.
- **Números**: 2 decimales, separador decimal `;`, alineados a la derecha con blancos a la
  izquierda. **Fechas** `ddMMyyyy`. **Booleanos** `X` / `–`.
- **Nombre**: `export_${codigoOrganizacion}_${yyyyMMdd_HHmmssms}.tra`
- **Orden estricto de líneas por documento**: RIB → tercero → GED → líneas de gasto (importe
  agregado) → líneas analíticas (cada una **inmediatamente detrás** de su línea de gasto) →
  líneas de IVA.
- **Tipo de pieza**: `FF` compra, `AF` abono de compra, `FC` venta, `AC` abono de venta.
- El adaptador soporta además BAP (pasado a pago), tesorería (remesas) y FNP (facturas a
  recibir). AGH no usa ninguno.

## 3. Fase 0 — extraer los datos de AGH que ya viven en Yooz

Tres vías, de menor a mayor fricción:

1. **Descarga directa desde la UI** (hoy, sin pedir nada a nadie):
   Configuración → Datos Maestros →
   - `Plan general de cuentas` — **236 elementos**
   - `Proveedor` — **41 elementos** (con su cuenta contable asignada)
   - `Perfil fiscal` — **4 elementos** (tipos de IVA)
   Más la exportación `YZ_GENERIC_V2` (CSV) para los documentos, y los PDF originales
   adjuntos a cada uno.
2. **API pública Yooz Rising**, OAuth 2.0 (authorization code y resource-owner). Requiere
   credenciales que hay que pedir a Yooz. Solo merece la pena si el volumen crece.
3. **Cláusula de reversibilidad del contrato**: Yooz entrega a petición «todas las imágenes
   originales con sus índices en formato CSV». Es la vía formal y completa para el histórico
   entero, y está incluida en el contrato. **Es la que hay que ejercer antes de dar de baja.**

Con (1) ya se monta la cuenta de AGH en TuFacturaIA con datos reales: catálogo de cuentas,
maestro de proveedores codificados, tipos de IVA, sociedades y los 46 documentos con su PDF.

## 3.bis Lo que dicen los catálogos reales de AGH (descargados 30-ago-2026)

Tres ficheros **TSV** (tabulados, no comas), UTF-8, con dos líneas de cabecera:
`Yooz Rising` y el nombre de la tabla (`ACCOUNTANT_PLAN_TAB`, `SUPPLIER_TAB`, `TAX_TAB`).
Todas las filas llevan la acción `CREATE` y el código de sociedad `2401`.

**Plan contable — 235 cuentas, de cuatro tipos**, no solo de mayor:

| Tipo | Filas | Qué es |
|---|---|---|
| `YZ_ENTRY` | 120 | cuentas de mayor |
| `YZ_SUPPLIER` | 97 | cuentas de proveedor (`410…`) |
| `YZ_CUSTOMER` | 16 | cuentas de cliente |
| `YZ_BANK` | 3 | bancos (`572…`) |

**Perfiles de IVA — 4**: `IVA0`, `IVA10`, `IVA21` (todos contra `47200000000`) e `IRPF15`
(contra `47510000001`).

**Proveedores — 40**, con CIF, IBAN, dirección postal, contacto, email y condición de pago
`PAYMENT_DUE`.

### Cinco cosas que rompen supuestos del plan y hay que corregir en la F1

1. **Las cuentas son de 11 dígitos**, no de 8. Los defaults de `asientos-contables.ts`
   (`60000000`, `47200000`) no sirven: la longitud tiene que ser libre por organización.
2. **El catálogo mezcla mayor, proveedor, cliente y banco.** La tabla de cuentas necesita una
   columna de tipo; no es un catálogo de cuentas de gasto.
3. **Los proveedores van a `410` (acreedores), no a `400`.** Los ocho valores de
   `asientos-contables.ts:60-67` ya son configurables por organización vía la config del
   módulo (`pgc_cuenta_proveedores_base` y compañía), así que esto no obliga a tocar código
   — pero sí a poblar esa config al dar de alta a AGH, y a documentarlo.
4. **El IRPF de AGH va a `4751`**, que es el `pgc_cuenta_irpf_repercutido` de FacturaIA
   (default `47510000`), no el soportado `473`. La cuenta correcta ya existe en el modelo; lo
   que no encaja es la **longitud**: 8 dígitos frente a los 11 de AGH.
5. **El catálogo viene sucio: 11 filas de 235 (~5%)** son basura —
   `GASTO (test)`, códigos `0/1/2/3` con nombre de persona o proveedor (`DHL`,
   `José Luis Rodriguez`, `Uoter Limpiezas`, `Kamen Danailov`), y cinco localizadores de vuelo
   de Iberia (`IBEBUXS02`, `IBEOVH999`…) usados como código de cuenta. Más dos cuentas de
   9 dígitos (`572000000`, `477000000`) frente a las de 11.
   **La importación tiene que validar y reportar, no tragar.** Es el mismo argumento de
   ADR-021 llevado al catálogo.

El plan de gasto de AGH es muy a medida —doce subcuentas colgando de `629`: notas de gasto,
software, gasolina, comidas, mensajería, formación, plataformas de empleo, gastos matriz—
y ahí es exactamente donde el aprendizaje por proveedor de la F1 rinde.

## 3.ter Preguntas cerradas contra el tenant (30-ago-2026)

Resueltas mirando la ficha del documento DKV (`#/document/7663943`) y el listado de los 46.

- **Una sola sociedad**: `AGH IB (2401)`. Los 46 documentos cuelgan de ella. Una organización
  en TuFacturaIA, no varias.
- **Diario**: la cabecera contable del asiento dice `Libro = Compras`. Es el único visto.
- **Ejes analíticos: DOS, no uno — `CANAL` y `DEPARTAMENTO`.** Valores tipo `IBEHOFDRH` y
  `IBEBUXC44`. **Esto invalida la F4 tal y como estaba escrita**: una sola dimensión
  configurable no cubre a AGH; hacen falta N dimensiones por organización.
- **El circuito de aprobación existe y tiene tres etapas**, visibles en la columna de tarea de
  los 46 documentos:
  1. `Registrar` — destinatarios por **rol**: Contable extendido, Contable, Administrador (30+
     documentos, todos marcados «Con retraso»).
  2. `Aprobación` — destinatario **nominal + rol**: `Daniela ESCALONA (Usuario)` y
     `Aprobador(a) (Rol)` (6 documentos).
  3. `Pendiente de la confirmación del pago (feedback)` — `Usuario del sistema` (1 documento,
     el de DKV).
  Existe por tanto un rol **`Aprobador(a)`** que no está en el `OrgRole` de FacturaIA. Lo que
  **no** se ve en el tenant son los umbrales por importe: eso sigue siendo pregunta para Carlos.
- **Solo compras.** No hay maestro de clientes en Datos Maestros y el panel es «Facturas
  recibidas». Las 16 cuentas `YZ_CUSTOMER` del plan contable son solo eso, cuentas.
- **Modo de pago** es un catálogo aparte: el DKV va con `Débito bancario (PRE)`.
- **El asiento se puede leer sin exportar.** La ficha del documento tiene dos pestañas,
  `Asiento [Yourcegid CommunicationsSx TRA]` y `Asiento [Yooz Standard CSV]`, que muestran el
  asiento ya calculado. **Es el banco de pruebas del exportador de la F2**: se compara contra
  esa vista sin tocar nada del tenant.

### El asiento real del único documento «listo»

```
Cabecera: Libro=Compras · Divisa=EUR · Cambio=1,000000 · Fecha contable=01/01/2026
          Nº documento=20260566605

 # | Fecha      | Ref pieza   | Ref línea   | Cuenta                       | Etiqueta    | Debe    | Haber   | CANAL     | DEPARTAMENTO
 1 | 01/01/2026 | 20260566605 | IVA0        | Alta automática (12900000000)| 41000000009 | 2033,48 |         | IBEHOFDRH | IBEBUXC44
 2 | 01/01/2026 | 20260566605 | 41000000009 |                              | 41000000009 |         | 2033,48 |           |
```

**Ese asiento es contablemente incorrecto**: carga la `129` (resultado del ejercicio) contra la
`410` del proveedor, porque la línea nunca se codificó y quedó en la cuenta comodín «Alta
automática». Es el único documento que Yooz considera exportable, y su asiento no vale. Confirma
el diagnóstico: el cuello de botella de AGH es la codificación, no la herramienta ni el canal.

### Incoherencia entre catálogos

Dos códigos de tercero tienen **nombre distinto** en el plan contable y en el maestro de
proveedores:

| Código | Plan contable | Maestro de proveedores |
|---|---|---|
| `IBEBUXS02` | Kamen | Casa Lampazas Madrid |
| `IBEOVH999` | DHL | Uoter Limpiezas SL |

Y `1`, `2`, `3` (José Luis Rodriguez, Uoter Limpiezas, Kamen Danailov) existen como cuenta de
proveedor en el plan pero **no** en el maestro. El importador tiene que conciliar los dos
ficheros y denunciar las divergencias, no elegir uno en silencio.

## 4. Fases de producto

**F1 — Plan de cuentas y codificación contable.**
Catálogo de cuentas por organización + asignación de cuenta a proveedor y a línea. Se expone
como **pestaña propia al estilo de Inventario**, no como sección de Ajustes.
Aprendizaje: tabla **nueva** `cuenta_reglas_aprendidas`, clonando el molde de
`categoria_reglas_aprendidas` (mig 372). No se generaliza la existente: hay que conservar la
FK contra el catálogo que exige ADR-021, y no tocar la conciliación en producción.
La F1 debe producir exactamente seis datos por línea, ni uno más: **código de diario, fecha
contable, tipo de pieza, cuenta contable, código de tercero, importe.**

**F2 — Exportador Cegid TRA.**
Añadir `'cegid'` a `ExportContableFormato` (`src/lib/fiscal/export/build-export-response.ts:15`)
y una entrada en el menú «Exportar para gestoría»
(`src/components/fiscal/_parts/header-acciones/export-gestoria-menu.tsx`). Generador de ancho
fijo según §2. Sin incógnitas de formato.

**F3 — Circuito de aprobación.**
Tablas de tareas + rutas. En v1, **tareas nominales** sobre los roles existentes
(`propietario|admin|contable|comercial|gestor_externo|solo_lectura`), sin inventar roles
`aprobador`/`controlador`. Decisión pendiente de confirmar con Carlos.

**F4 — Dimensiones analíticas (en plural).**
AGH usa **dos ejes**, `CANAL` y `DEPARTAMENTO`, y el TRA emite una línea analítica por eje
detrás de cada línea de gasto. Lo que hay que construir es un catálogo de dimensiones por
organización, con sus valores, y la imputación en la línea de la factura — no un campo único.
La F3 y la F4 se tocan: la codificación analítica se hace en el mismo gesto que la contable.

## 5. Invariantes acordados

- **Feature flag por organización, apagado por defecto.** Con el flag apagado el
  comportamiento debe ser **byte a byte** el de hoy. Es la condición para no arriesgar al
  resto de clientes.
- Espejo TS ↔ CHECK de SQL en el mismo PR para cualquier enum nuevo, como el resto del repo.
- Nada de tocar `categoria_reglas_aprendidas` ni la conciliación existente.

## 6. Abierto

- **Umbrales de aprobación por importe.** Única pregunta que sigue siendo de Carlos, junto con
  si Mazars aceptaría otro formato que no fuera Cegid.
- **De Mazars o de la config del adaptador**: código ERP de 3 chars del diario «Compras»,
  códigos de 2 chars del campo `Axe` para CANAL y DEPARTAMENTO, `Etablissement` de 3 chars
  (`2401` no cabe), y si el `.TRA` viaja solo o en ZIP con los PDFs. Ninguno bloquea F1/F3/F4.
- Borrar `TRA_PRUEBA` del tenant cuando se termine de trastear.
- Sacar un `.TRA` real ya **no hace falta**: la pestaña «Asiento [Yourcegid CommunicationsSx
  TRA]» de cada documento enseña el asiento calculado, y sirve de banco de pruebas.
- **No se solicita** la exportación contractual de reversibilidad a Yooz (decisión del 30-ago:
  estamos integrando, no rescindiendo).

## 7. Plan de implementación (30-ago-2026) — diseño CERRADO, código sin arrancar

`facturaia/docs/architecture/PLAN-agh-contabilidad-cegid.md` (328 líneas) y su prompt de
lanzamiento `PROMPT-agh-contabilidad-cegid.md`. Salió de un arquitecto Fable y está
**verificado contra el repo**, con tres correcciones aplicadas: el maestro tiene 40
proveedores y no 41; los importes van en `numeric` y no en céntimos `bigint` (convención de
`facturas.base`/`total` en `database.types.ts`); la última migración de `main` es la 775.

Contiene el mapeo campo a campo del `.TRA` ya extraído del PDF (cabecera de 18 campos/147 B,
registro de movimiento de ~60 campos/1317 chars + CRLF), once tablas nuevas con su lista
explícita de «qué NO tocar», el importador de dos fases con siete clases de incidencia, y
diez riesgos. Tres que no habían salido antes: el campo `Tva` mide 3 chars y los códigos de
AGH miden 5-6 (`IVA21`→`IVA`, `IVA10`→`IVA`: colisionan los tres IVAs); Latin1 no codifica
el en-dash que la spec usa como booleano falso; y regenerar líneas de una recibida
`sin_aprobar` borra su codificación por CASCADE sin aviso.

### 7.bis Lo que la sesión de arquitectura cerró encima (30-ago-2026)

El plan se sometió a un grilling con dos auditorías en paralelo (contra los ADRs y contra los
invariantes del repo) y salió con **quince decisiones firmadas** en
`facturaia/docs/decisions/ADR-033-las-quince-decisiones-de-la-contabilidad-analitica-de-agh.md`.
Las cinco que cambian el plan:

- La tabla es **`catalogo_cuentas`**, no `cuentas_contables` (choca con `proveedores.cuenta_contable`,
  la subcuenta autoasignada de 8 dígitos, que es otra cosa) ni `plan_cuentas` (`plan_` ya significa
  plan de suscripción aquí). El glosario de los dos conceptos vive en el `CONTEXT.md` del repo.
- La feature se declara **sin `addon_purchasable`**: la mig 701 borró esa columna al ejecutar
  ADR-013. Tal cual estaba, la migración del plan habría reventado.
- La dependencia es solo `contabilidad → recibidas`. **`fiscal` NO**: su trigger solo evalúa con
  `plan_features.enabled=true`, y `fiscal` es un complemento con `enabled=false` en los tres planes,
  así que el candado sería decorativo y estallaría en `23514` más tarde.
- **La exportación a Cegid BLOQUEA** si queda algo sin codificar del periodo — excepción justificada
  a ADR-028 (el motor fiscal declara, no bloquea), con contrapartida obligatoria: la pantalla enseña
  el recuento sin codificar ANTES del botón.
- El **riesgo 5 del plan (regenerar líneas borra la codificación) NO existe**: un barrido no encontró
  ninguna vía que reescriba las líneas de una recibida viva. La única que hace `DELETE FROM
  lineas_factura` exige `tipo='emitida'` + `estado='borrador'`. La restricción de UI que el plan
  proponía se retiró.

Spec **#2295** y **trece tickets #2296-#2308** publicados en GitHub con sus aristas de bloqueo, todos
`ready-for-agent`. Cogibles sin esperar a nadie: **#2296** (patrones PGC) y **#2297** (fundaciones del
catálogo). Panel de progreso vivo:
`claude.ai/code/artifact/dbb95570-48cb-4387-9db4-a250c49e9af4`.

Tres cuestionarios escritos y **pendientes de mandar** (Manu): Giuliana (catálogos sucios, qué es cada
eje, si emiten ventas), Carlos (qué factura necesita aprobación y con qué umbral), Mazars (diario,
ejes, establecimiento, códigos de impuesto de 3 chars, y si aceptarían otro formato). **Ninguno
bloquea el primer bloque de tickets.**

Aprendizajes que salieron de esta fase:
[[el-documento-listo-del-sistema-legado-valida-estructura-nunca-criterio]] ·
[[un-pattern-mas-estrecho-que-el-dato-del-cliente-bloquea-el-alta-antes-del-codigo]] ·
[[dos-catalogos-exportados-del-mismo-saas-pueden-contradecirse]] ·
[[verificado-contra-el-repo-no-ve-la-columna-que-un-adr-mando-borrar]] ·
[[un-subagente-cita-el-mecanismo-no-el-guard-que-lo-cierra]]

Relacionado: [[facturaia-integracion-api-v1-portal]] · [[agh-iberica]]
