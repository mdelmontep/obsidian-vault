---
title: TuFacturaIA — Centro fiscal IA (módulo Pro add-on)
date: 2026-05-19
source: chat análisis + 4 agentes revisión (arquitectura/legal/producto/research AEAT)
tags: [facturaia, fiscal, aeat, modelo-303, verifactu, roadmap, next]
---

# Centro fiscal IA — Spec completa para implementación

> **Estado**: NEXT — no iniciado. Toda la información para arrancar Sprint 1 desde cero.
> **Decisiones congeladas el 2026-05-19**. Ver §Decisiones al final si se quiere refrescar.
> **Naming v1**: "Centro fiscal IA". Se renombrará a "Agente fiscal" en v3 cuando sí presente telemáticamente.
> **Catálogo**: ya existe entrada `id: 'fiscal'` en `src/lib/modules/catalog.ts:148` con `implemented: false`. Reescribir según §Catálogo.

## Posicionamiento

**Promesa v1**: "Tus modelos AEAT cuadrados y listos para presentar. Tú o tu asesor, en 1 clic."

NO presentamos telemáticamente en v1. AEAT no expone API pública para 303/111/347 con cert de tercero salvo SII (no aplica a target PYME). Estrategia escalonada:

| Fase | Promesa | Entregable AEAT |
|---|---|---|
| **v1 — Cuadre + Export** | "Llegas al portal AEAT con todo cuadrado" | TXT BOE pre-relleno + PDF justificativo + libro registro IVA XLSX + export A3/Holded asesor |
| **v2 — Pre-validación** | "Te avisamos si algo no cuadra" | Validación contra PRE-Exteriores AEAT + diagnóstico IA del rechazo (patrón `ai-validate.ts` Verifactu) |
| **v3 — Presentación con cert** | "Presentamos por ti" | Colaborador social RD 1065/2007 con cert TuFacturaIA + apoderamiento del cliente |
| **v4 — SII** | Grandes empresas | Aprovechar infra Verifactu + envío SII (extensión natural) |

**Renombrado** "Agente fiscal" → "Centro fiscal IA" en v1. Razón: "agente" induce a esperar que presente, lo cual NO hacemos hasta v3. Volver a "Agente fiscal" cuando v3 esté activa.

## Pricing / packaging

**Add-on comprable sobre Pro** (no incluido por defecto):
- `plan_features` row: `feature_id='fiscal'`, `plan='pro'`, `enabled=false`, `addon_purchasable=true`, `addon_price_eur=9` (o 12-15 según validación).
- Gating ya implementado: `await orgHasFeature(orgId, 'fiscal')` envuelve todos los endpoints `/api/fiscal/*`.
- **Un solo add-on** que crece de capacidades (v1 cuadre, v3 presenta, v4 SII). NO crear tiers separados — fricción comercial.
- Trial recomendado: 1 trimestre gratis para que prueben con su 303 real.
- Descuento anual: 12 → 10 meses.

Comparativa orientativa (verificar antes de fijar precio): Quipu ~22€/mes (con presentación), Contasimple ~13€/mes, Holded Pro ~25€/mes sin presentación.

## Modelos AEAT cubiertos

| Modelo | Fase | Bloqueante para | Notas |
|---|---|---|---|
| **303** IVA trimestral | v1 S1-3 | Todos | Nueva casilla 112 (hidrocarburos) en 2026 |
| **390** resumen anual IVA | v1 S1-3 | No-SII | Exonerados SII |
| **130** pago fraccionado IRPF EDN/EDS | v1 S1-2 | **Autónomo estimación directa** | Crítico — sin esto el módulo es inútil para ~80% autónomos |
| **131** módulos IRPF | v1.5 | Autónomo módulos (minoría) | |
| **115 + 180** retenciones alquileres | v1 S4 | Quien paga local | Requiere flag `proveedor.es_arrendador` + referencia catastral |
| **111** retenciones profesionales | v1 S4 | Empresarios | **Solo profesionales** — nóminas explícitamente fuera con disclaimer |
| **190** resumen anual 111 | v2 | Quien presenta 111 | Carry interest novedad 2026 |
| **347** operaciones con terceros >3005,06€ | v1 S4 | No-SII | **Vigente confirmado 2026** (NO derogado por Verifactu) |
| **349** intracom | v1.5 | Si hay clientes UE | Mensual >50k€/trim, trimestral resto |
| **Libro IVA XLSX** | v1 S1 | **PYME con asesor** | Kill switch para 60-70% del target Pro |
| **Export A3/Holded asesor** | v1 S3-4 | PYME con asesor | CSV import asesoría |

**Fuera de scope v1 (con disclaimer explícito)**:
- 100 (renta), 200/202 (IS), 232 (vinculadas — minoría), 165 (donaciones), 368 (OSS digital UE), 714.
- **Régimen criterio de caja** (art 163 LIVA decies): ~5-8% adopción, fuera v1 con aviso onboarding.
- **Nóminas para 111**: solo profesionales auto; nóminas a mano post-export.

## Arquitectura técnica

### Capa de cálculo (calculador versionado e inmutable)

```
src/lib/fiscal/
  periodo.ts                       # T1=ene-mar Madrid TZ, COALESCE(fecha_operacion, fecha)
  iva.ts                           # agrupador 303 por tipo 0/4/10/21 + RE 0.5/1.4/1.75/5.2
  irpf.ts                          # 111/115/180/190/130/131
  cruces.ts                        # 347, 349, VIES
  cuadres.ts                       # 10+ validadores (ver §Cuadres)
  calculadores/
    v1/
      303.ts                       # versión inicial
      390.ts
      130.ts
      111.ts
      115.ts
      180.ts
      190.ts
      347.ts
      349.ts
    # v2/, v3/... cuando cambien fórmulas AEAT futuras
  export/
    aeat-txt.ts                    # formato posicional BOE
    aeat-pdf.ts                    # Puppeteer reusa infra render-invoice
    libro-iva-xlsx.ts              # libro registro emitidas + recibidas
    a3-holded-csv.ts               # export asesor
  presentar/
    validate-aeat.ts               # v2 — PRE-Exteriores
    soap-presentaciones.ts         # v3 — colaborador social
    sii-soap.ts                    # v4
```

**Principios inviolables**:
- Cálculos puros `(facturas[]) → Modelo`. Test unitario con fixtures fijas.
- Periodificación por `COALESCE(facturas.fecha_operacion, facturas.fecha)` — RD 1619/2012 art 6.1.i + mig 087 ya existente. **NUNCA filtrar solo por `fecha`**.
- Cálculo en **enteros céntimos** (`base_x100 BIGINT`), no float. Evita drift IVA mixto análogo a fix `CuotaTotal` Verifactu (gotchas:116).
- Calculador versionado: una declaración apunta a su versión. Recalcular = nueva fila, NUNCA mutar. Análogo a Verifactu que no recalcula huellas históricas (gotchas:123).

### Persistencia — migración nueva

> ⚠️ **Las migraciones tendrán los números que toquen** cuando se empiece (actualmente repo está en `104_fix_check_num_solo_emitidas.sql`). Aquí uso `NNN` como placeholder. Verificar `supabase/migrations/` antes de crear.

```sql
-- NNN_fiscal_declaraciones.sql
CREATE TABLE fiscal_declaraciones (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL REFERENCES organizations,
  modelo TEXT NOT NULL CHECK (modelo IN ('303','390','111','115','180','190','347','349','130','131')),
  ejercicio INT NOT NULL,
  periodo TEXT NOT NULL,             -- '1T','2T','3T','4T','01'..'12','0A' (anual)
  estado TEXT NOT NULL DEFAULT 'borrador'
    CHECK (estado IN ('borrador','cuadrado','exportado','presentado','aceptado','rechazado','rectificada')),
  version_calculador SMALLINT NOT NULL,
  datos JSONB NOT NULL,              -- snapshot casillas + resumen (render cache, NO fuente de verdad)
  cuadres JSONB,                     -- [{ tipo, severidad, mensaje, ids_afectados[] }]
  fichero_aeat_path TEXT,            -- storage WORM: org/{org}/fiscal/{modelo}-{ej}-{per}-{hash}.txt
  pdf_path TEXT,
  hash_calculo TEXT NOT NULL,        -- sha256 sobre snapshot completo + versión
  presentada_en TIMESTAMPTZ,
  resultado_aeat JSONB,              -- v3
  sello_tiempo_eidas JSONB,          -- timestamp cualificado FNMT/Uanataca
  created_by UUID,
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE (org_id, modelo, ejercicio, periodo)
);

-- Tabla join con SNAPSHOT inmutable de cada factura incluida.
-- ESTA es la fuente de auditoría AEAT, no el jsonb datos.
CREATE TABLE fiscal_declaracion_snapshot (
  declaracion_id UUID NOT NULL REFERENCES fiscal_declaraciones ON DELETE RESTRICT,
  factura_id UUID NOT NULL REFERENCES facturas ON DELETE RESTRICT,
  base_x100 BIGINT NOT NULL,         -- céntimos enteros, sin drift
  cuota_x100 BIGINT NOT NULL,
  iva_pct NUMERIC(5,2) NOT NULL,
  tipo_factura TEXT,
  fecha_operacion DATE,
  exencion_codigo TEXT,
  PRIMARY KEY (declaracion_id, factura_id)
);
-- ON DELETE RESTRICT: una factura ya declarada NO se puede borrar (paralelo a presupuesto convertido, gotchas:129).

CREATE TABLE fiscal_plazos (
  modelo TEXT,
  ejercicio INT,
  periodo TEXT,
  fecha_limite DATE,
  fecha_limite_domiciliacion DATE,
  PRIMARY KEY (modelo, ejercicio, periodo)
);

CREATE TABLE fiscal_avisos (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  org_id UUID NOT NULL,
  declaracion_id UUID,
  modelo TEXT,
  ejercicio INT,
  periodo TEXT,
  tipo TEXT,           -- 'plazo_30d','plazo_15d','plazo_7d','plazo_2d','plazo_1d','cuadre_roto','factura_borrador'
  enviado_en TIMESTAMPTZ DEFAULT now(),
  canal TEXT           -- 'in_app','email','whatsapp'
);

-- RLS OBLIGATORIA (inviolable CLAUDE.md):
ALTER TABLE fiscal_declaraciones ENABLE ROW LEVEL SECURITY;
-- policy: org_id = active org, rol IN ('propietario','admin','contable')
-- NO 'solo_lectura' para escribir, NO 'comercial'
-- mismo patrón para fiscal_declaracion_snapshot, fiscal_avisos
-- fiscal_plazos: lectura todos, escritura service-role
```

### Concurrencia anti-race A-fiscal análoga

Al marcar declaración como `presentada`, envolver en RPC con `pg_advisory_xact_lock(hashtext('fiscal:'||org||':'||modelo||':'||periodo))` + recheck del set de facturas vs snapshot antes de transición de estado. Riesgo: factura con `fecha_operacion` dentro del periodo entrando entre cálculo y cierre (RD 1619/2012 permite hasta día 16 mes siguiente). Patrón paralelo a A-fiscal #2 documentado en `docs/architecture/gotchas.md:114`.

### Inmutabilidad legal (Sprint 1)

- **WORM Object Lock**: migrar Storage de declaraciones a S3 Compliance mode o Backblaze B2 Object Lock. Supabase Storage **no tiene WORM** — service-role puede borrar. Razón: RD 1619/2012 art 8.1 exige garantía de integridad 6 años (LGT art 66).
- **Sello de tiempo cualificado eIDAS**: integración FNMT TS@ (~1 día dev). Coste ~0,01-0,05€/sello, despreciable. Aporta valor probatorio frente a AEAT en inspección (Reglamento UE 910/2014 art 42).
- Hash sha256 interno NO basta como evidencia legal (circular).

### Endpoints

Todos con `withApiAuth` + `effectiveOrgId(request)` (acepta `?org_id=` para superadmin, NO cookie `impersonate_org` que el middleware borra — inviolable CLAUDE.md):

| Endpoint | Función |
|---|---|
| `GET /api/fiscal/[modelo]/[ej]/[per]` | Calcula on-demand si no existe; cachea por `hash_calculo` |
| `POST /api/fiscal/[modelo]/[ej]/[per]/recalcular` | Forzar |
| `POST /api/fiscal/[modelo]/[ej]/[per]/marcar-cuadrado` | Bloquea recálculo auto |
| `POST /api/fiscal/[modelo]/[ej]/[per]/marcar-presentada` | RPC con advisory lock + recheck |
| `GET /api/fiscal/[modelo]/[ej]/[per]/aeat.txt` | Descarga TXT BOE |
| `GET /api/fiscal/[modelo]/[ej]/[per]/pdf` | PDF resumen |
| `GET /api/fiscal/[ej]/libro-iva.xlsx` | Libro registro emitidas + recibidas |
| `GET /api/fiscal/[ej]/export-asesor` | CSV A3/Holded |
| `GET /api/fiscal/calendario` | Próximos plazos con estado |
| `POST /api/internal/fiscal-avisos` | Cron diario 08:00 Madrid, revisa plazos. Notifica vía `notify_upsert_function` (mig 051), respeta `notification_preferences` (mig 068) |
| `POST /api/internal/fiscal-recalcular-borrador` | Cron nocturno: recalcula si snapshot cambió |

Crons con `pg_try_advisory_lock` (patrón Verifactu worker) o tabla `cron_locks` si se crea. Registrar en `cron_runs` (mig 063).

### Frontend

- **Modal estándar de agentes**: mantener 5 tabs estándar del patrón (`docs/architecture/modules-system.md`). NO añadir tab "Modelos" — rompe overrides `module_metadata`. El modal solo expone CTA "Abrir Centro fiscal" que navega a la ruta dedicada.
- **Ruta dedicada** `/fiscal/[ejercicio]` (calendario + estado por modelo) y `/fiscal/[ejercicio]/[modelo]/[periodo]` (vista detalle).
- **Vista detalle** 3 columnas:
  - **Casillas** — tabla AEAT con drill-down a facturas
  - **Cuadres** — checklist verde/ámbar/rojo (ver §Cuadres)
  - **Facturas incluidas** — virtualizada, filtros por tipo IVA
- Header con estado (badge), plazo restante (countdown rojo si <7d), botones [Recalcular] [Exportar TXT] [Descargar PDF] [Marcar cuadrado] [Marcar presentada].
- **Sin emojis Unicode** — `<Icon>` de `src/components/layout/icon.tsx`. Colores `#3D7BF5` / `#1B2B4B` / `#f5425a` (inviolable frontend).

### Wizard onboarding fiscal (Sprint 2)

Antes de calcular nada, el cliente configura su perfil fiscal:
- Régimen IVA (general / RE / criterio caja / simplificado / REAGP)
- Periodicidad IVA (trimestral / mensual REDEME/gran empresa)
- Sujeto recargo equivalencia (sí/no)
- Estimación IRPF (directa normal / directa simplificada / módulos / exonerado)
- Tiene profesionales con retención (sí/no) — habilita 111
- Tiene locales en alquiler (sí/no) — habilita 115/180
- Tiene clientes UE (sí/no) — habilita 349
- Está en SII (sí/no) — exonera 390/347

Sin este wizard el módulo da números mal el día 1. Se relanza si cambia algo mid-year.

## Cuadres — el valor diferencial

10+ validadores guardados en `fiscal_declaraciones.cuadres` (jsonb) + emisión `module_event` (`feature_id='fiscal'`, `tipo='cuadre_roto'`) para activity feed:

| Cuadre | Severidad | Lógica |
|---|---|---|
| Borradores en periodo | 🔴 | `facturas.num IS NULL AND fecha entre [periodo]` — borradores Holded-style mig 099 |
| Verifactu rechazadas | 🔴 | `verifactu_estado='rechazada' OR 'error'` en periodo |
| Verifactu pendientes | 🟡 | Declarar antes de aceptación AEAT crea inconsistencia |
| `fecha_operacion` cae en periodo anterior | 🟡 | Declarar en ese periodo, no en el de `fecha` |
| Anuladas sin abono espejo | 🟡 | Mig 097 garantiza único; detectar huérfanas |
| Recargo equivalencia inconsistente | 🟡 | Cliente con RE pero factura sin RE |
| Régimen caja: factura emitida pero no cobrada | 🟡 | Si `regimen_caja=true`, no entra hasta cobro |
| Conciliación bancaria divergente | 🟡 | Mig 061/101: factura cobrada con importe ≠ movimiento |
| Proveedor sin NIF en factura recibida | 🔴 si 347 | Bloquea declaración 347 |
| Cliente UE sin VIES validado | 🟡 | E5 intracom requiere NIF-IVA en VIES |
| IVA mixto riesgo redondeo | 🟡 | Facturas con >1 tipo IVA + cadena Verifactu (gotchas:116) |
| Sucesor en cadena Verifactu sin huella recalculada | 🔴 | Cross-check con `verifactu_huella` tabla |
| Multi-empresa: ¿declaración por NIF? | ℹ️ | Una por org (cada org tiene su NIF) |

## Mapping casillas 303 (referencia rápida)

Asumiendo schema `lineas_factura(iva_pct, base_imponible, exencion_codigo, ...)` + `facturas(tipo_factura, regimen_iva, recargo_equivalencia, ...)` + `clientes(pais)`:

| Condición línea | Base | Cuota |
|---|---|---|
| Emitida ES iva=0 sin exención | 150 | 152 |
| Emitida ES iva=4 | 01 | 03 |
| Emitida ES iva=10 | 04 | 06 |
| Emitida ES iva=21 | 07 | 09 |
| Emitida RE 0.5% | 168 | 170 |
| Emitida RE 1.4% | 19 | 21 |
| Emitida RE 1.75% | 156 | 158 |
| Emitida RE 5.2% | 22 | 24 |
| Emitida ISP (inversión sujeto pasivo) | 12 | 13 |
| Emitida cliente UE bienes (exención art 25) | informativa | — |
| Emitida cliente UE servicios | informativa | — |
| Emitida no-UE (export) | 60 | — |
| Recibida bienes/servicios corrientes interiores | 28 | 29 |
| Recibida bienes inversión interiores | 30 | 31 |
| Recibida import bienes corrientes | 32 | 33 |
| Recibida import bienes inversión | 34 | 35 |
| Recibida intracom corrientes | 10 + 36 | 11 + 37 (devengado Y deducible) |
| Recibida intracom inversión | 10 + 38 | 11 + 39 |
| Rectificativa emitida | 14 (con signo) | 15 |
| Rectificativa recibida | 40 (con signo) | 41 |

**Liquidación**: 71 = 69 − 70 + 109 + 112, donde 69 = 66 − 67 + 68, 66 = 64 × 65/100, 64 = 46 + 58, 46 = 27 − 45.

**NOVEDAD 2026 (Orden HAC/27/2026 BOE 26-ene-2026)**: casilla **112** pago a cuenta entregas gasolinas/gasóleos/biocarburantes. Estructura TXT antigua sin 112 = rechazo AEAT.

## Plazos AEAT 2026 (seed inicial `fiscal_plazos`)

| Modelo | Periodo | Fecha teórica | Día | Efectivo |
|---|---|---|---|---|
| 303/111/115/130 | 4T 2025 | 30-ene-2026 | viernes | 30-ene-2026 |
| 180/190 | anual 2025 | 31-ene-2026 | sábado | **2-feb-2026** |
| 390 | ej. 2025 | 30-ene-2026 | viernes | 30-ene-2026 |
| 347 | anual 2025 | 28-feb-2026 | sábado | **2-mar-2026** |
| 303 | 1T 2026 | 20-abr-2026 | lunes | 20-abr-2026 |
| 303 | 2T 2026 | 20-jul-2026 | lunes | 20-jul-2026 |
| 303 | 3T 2026 | 20-oct-2026 | martes | 20-oct-2026 |
| 303/etc | 4T 2026 | 30-ene-2027 | sábado | **1-feb-2027** |

Domiciliación corta plazo 5 días (303: día 15 en vez de 20). Festivos a vigilar 2026: 6-ene, 2/3-abr, 1-may, 15-ago, 12-oct, 6/8-dic, 25-dic. Cruzar con festivos CCAA del domicilio fiscal del cliente (art 30.5 Ley 39/2015).

## Avisos (curva)

Cron diario 08:00 Madrid emite avisos a 30/15/7/2/1 días del plazo:
- in-app siempre
- email según `notification_preferences` (mig 068)
- WhatsApp opcional con quiet hours (mig 068)
- 0 días: aviso "PLAZO HOY" rojo + bloqueo de edición de facturas del periodo si declaración en estado `cuadrado`

## Vías de presentación electrónica (v3+)

**Decisión congelada**: colaborador social RD 1065/2007 arts. 79-81.

- Convenio TuFacturaIA ↔ AEAT (contacto `comunicacion.sepri@correo.aeat.es`).
- Cliente otorga apoderamiento en registro AEAT (vía Cl@ve PIN o cert).
- TuFacturaIA presenta con SU certificado en nombre del cliente.
- Es la vía estándar de Quipu, Declarando, Holded Asesor, A3.
- **Tiempo estimado**: 2-4 meses convenio activo. **Coste**: 0€ + cert empresa FNMT ~50€/año (ya lo tenéis para Verifactu).
- **Acción pendiente**: arrancar gestión convenio en paralelo al desarrollo v1, no se puede empezar v3 sin convenio activo.

**Descartadas explícitamente**:
- AutoFirma local: UX nefasta en 2026 (handler nativo `afirma://`, instalación previa por usuario, abandono alto). Solo viable para usuarios técnicos.
- Cargar cert del cliente en nuestro servidor: rompe eIDAS 910/2014 (clave privada bajo control exclusivo del firmante). Inviable legalmente.

## Cumplimiento legal — checklist

- ✅ Disclaimer "no es asesoramiento fiscal" en footer PDF y cabecera TXT (texto en §Texto legal).
- ✅ Conservación 6 años inmutable (WORM + sello eIDAS).
- ⚠️ **DPA específico para datos fiscales de terceros** (NIFs proveedores/profesionales/arrendadores en 347/180/190 que NO son clientes de TuFacturaIA). Contrato encargado de tratamiento art 28 RGPD actualizado listando subencargados (Supabase, Hetzner, OpenAI). **Bloqueante antes de GA.**
- ⚠️ **OpenAI/LLM en cálculos**: LLM solo para explicación/copiloto, NO para los números que van al BOE. Confirmar DPA OpenAI vigente.
- ⚠️ **Contrato de servicio** con cláusula limitación responsabilidad (tope = importe anual pagado, exclusión lucro cesante y sanciones AEAT). Revisado por abogado. Cláusulas abusivas B2C nulas (TRLGDCU art 86).
- ✅ Plazos AEAT en tabla actualizable + festivos CCAA del domicilio fiscal.
- ⚠️ **Beta privada 2 trimestres** con 20-30 orgs voluntarias antes de GA. Bug en TXT = thread Twitter "TuFacturaIA me hizo presentar mal el 303".
- ⚠️ **Auditoría fiscal externa** ~2k€ antes de GA (asesor fiscal colegiado valida cálculos contra casos reales).

## Texto legal mínimo (para outputs)

**Footer PDF (cada página)**:
> Documento generado automáticamente por TuFacturaIA a partir de los datos registrados por el usuario. No constituye asesoramiento fiscal ni declaración presentada ante la AEAT. La responsabilidad sobre la veracidad, integridad y presentación de la declaración corresponde exclusivamente al obligado tributario (art. 179 LGT). Se recomienda revisión por asesor fiscal colegiado antes de su presentación. Hash de cálculo: {sha256} · Generado: {ts UTC} · Versión motor: {v}

**Cabecera TXT export**:
```
; TuFacturaIA v{x.y} - Modelo {NNN} ejercicio {YYYY} periodo {PP}
; Generado {ISO8601} - Hash {sha256}
; Documento de apoyo NO presentado. Validar en sede.agenciatributaria.gob.es antes de envío.
```

## Catálogo — entrada actualizada

Sobrescribir `src/lib/modules/catalog.ts:148`:

```ts
{
  id: 'fiscal',
  nombre: 'Centro fiscal IA',
  descripcion: 'Modelos 303, 390, 130, 111, 115, 180, 190, 347 cuadrados y listos para presentar.',
  tagline: 'Tus modelos AEAT cuadrados. Tú o tu asesor, en 1 clic.',
  descripcionLarga:
    'Calcula los modelos del trimestre con los datos de tus facturas, valida cuadres y avisa antes del plazo de presentación. Exporta TXT BOE-ready para subir al portal AEAT, libro IVA para tu asesor, o presenta tú mismo.',
  acciones: [
    'Modelos 303, 390, 130, 111, 115, 180, 190 y 347',
    'Cuadres trimestrales y anuales con drill-down',
    'Libro registro IVA XLSX para tu asesor',
    'Avisos a 30/15/7/2/1 días del plazo',
    'Exportación AEAT-ready (TXT BOE + PDF justificativo)',
    'Pre-validación contra esquemas AEAT (v2)',
  ],
  iaPrompt: '¿Cuánto IVA pago este trimestre y por qué? ¿Qué tengo pendiente para el 303?',
  categoria: 'modulo_ia',
  color: '#7BADF7',
  planIncluido: 'pro',          // pero addon_purchasable=true, NO viene por defecto
  esBackend: true,
  docSlug: 'centro-fiscal',
  configSchemaDefault: [
    { key: 'aviso_dias_antes', label: 'Recordar antes del plazo (días)', type: 'number', default: 7, implemented: true },
    { key: 'periodicidad_iva', label: 'Periodicidad IVA', type: 'select', options:[{value:'trimestral',label:'Trimestral'},{value:'mensual',label:'Mensual (REDEME/gran empresa)'}], default: 'trimestral', implemented: true },
    { key: 'regimen_iva', label: 'Régimen IVA', type: 'select', options:[{value:'general',label:'General'},{value:'re',label:'Recargo equivalencia'},{value:'caja',label:'Criterio de caja'}], default: 'general', implemented: true },
    { key: 'estimacion_irpf', label: 'Estimación IRPF', type: 'select', options:[{value:'directa_normal'},{value:'directa_simplificada'},{value:'modulos'},{value:'no_aplica'}], default: 'directa_simplificada', implemented: true },
    { key: 'modelo_303', type: 'boolean', default: true, implemented: true },
    { key: 'modelo_130', type: 'boolean', default: true, implemented: true },
    { key: 'modelo_111', type: 'boolean', default: false, implemented: true },
    { key: 'modelo_115', type: 'boolean', default: false, implemented: true },
    { key: 'modelo_347', type: 'boolean', default: true, implemented: true },
    { key: 'modelo_349', type: 'boolean', default: false, implemented: true },
    { key: 'auto_recalcular', label: 'Recalcular al editar facturas del periodo', type: 'boolean', default: true, implemented: true },
  ],
},
```

## Top-10 preguntas reales del copiloto (tools IA)

El "Pregúntale a tu IA" debe responder a estas 10, no a casillas técnicas:

1. "¿Cuánto IVA pago este trimestre y por qué tanto?"
2. "¿Puedo desgravarme esta comida con cliente?"
3. "¿Esta factura de Amazon me la puedo meter?"
4. "¿Por qué el 303 me sale a devolver/pagar?"
5. "Me falta una factura del proveedor X de marzo — ¿qué hago?"
6. "¿Cuándo y cuánto pago de IRPF este trimestre?" (130)
7. "Mi asesor me pide el libro IVA — ¿cómo se lo mando?"
8. "¿Tengo que hacer el 347 este año?"
9. "Mi cliente francés — ¿lleva IVA?" (intracom, ROI)
10. "Si emito un abono ahora, ¿afecta al 303 del trimestre pasado?"

Tools del agente leen `fiscal_declaraciones` + `facturas` + `lineas_factura` + reglas hardcoded (deducibilidad, ISP, intracom). Patrón paralelo a `copiloto` existente (mig 062).

## Roadmap por sprints

| Sprint | Dur | Contenido |
|---|---|---|
| **S1** | 2 sem | Mig fiscal (declaraciones + snapshot enteros céntimos + plazos seed 2026 + RLS) · `calculadores/v1/{303,130}.ts` · `fecha_operacion` correcta · tests fixtures · Libro IVA XLSX · **WORM Object Lock** · **Sello eIDAS FNMT integración** |
| **S2** | 2 sem | Cuadres (10+ validadores) · Wizard "perfil fiscal" onboarding · UI ruta `/fiscal/...` + modal CTA · Cron `fiscal-recalcular-borrador` con lock |
| **S3** | 2 sem | Export TXT BOE 303/390/130 (formato posicional Orden HAC/27/2026) · PDF Puppeteer · Pre-validación PRE-Exteriores (descarga TXT validado, sin SOAP) |
| **S4** | 2 sem | 111 profesionales · 115/180 (req ref catastral) · 347 (detección umbral 3005,06€ + flag SII) · Export A3/Holded asesor |
| **S5** | 1 sem | Cron avisos curva 30/15/7/2/1 · Tools IA copiloto (top-10 preguntas) · Notif email + WhatsApp respetando `notification_preferences` |
| **S6** | 2 sem | 349 + VIES · 190 (carry interest 2026) · 131 |
| **Pre-GA** | — | Beta privada 2 trimestres (20-30 orgs) + auditoría fiscal externa ~2k€ |
| **v2** | tbd | Diagnóstico IA rechazos AEAT (patrón `ai-validate.ts`) |
| **v3** | tbd | Presentación colaborador social — REQUIERE convenio AEAT firmado (gestión arrancada en paralelo a S1) |
| **v4** | tbd | SII para grandes (aprovecha infra Verifactu) |

## Decisiones congeladas 2026-05-19

1. ✅ **130 añadido a v1 bloqueante** (autónomo estimación directa = ~80% target autónomo)
2. ✅ **Naming "Centro fiscal IA"** en v1; "Agente fiscal" reservado para v3
3. ✅ **Convenio colaborador social AEAT** — arrancar gestión en paralelo al desarrollo
4. ✅ **WORM + sello tiempo eIDAS** desde Sprint 1 (coste despreciable, riesgo legal alto si no)
5. ✅ **Add-on comprable sobre Pro** (`addon_purchasable=true`, precio inicial sugerido 9 €/mes — validar)

## Decisiones pendientes al arrancar

1. **Precio exacto add-on**: 9 / 12 / 15 €/mes. Trial 1 trimestre sí/no.
2. **WORM proveedor**: AWS S3 Object Lock vs Backblaze B2. Hetzner no soporta nativo.
3. **Sello tiempo proveedor**: FNMT TS@ (más barato, gestión estatal) vs Uanataca (más ágil B2B).
4. **Auditoría fiscal externa**: asesoría concreta. Presupuestar antes de Sprint 1.

## URLs oficiales de referencia (marcar permanentemente)

- [Sede AEAT — Diseños de registro](https://sede.agenciatributaria.gob.es/Sede/ayuda/disenos-registro.html) — descargar PDF por modelo, versión vigente 2026
- [Sede AEAT — Instrucciones 303 2026](https://sede.agenciatributaria.gob.es/Sede/todas-gestiones/impuestos-tasas/iva/modelo-303-iva-autoliquidacion_/instrucciones-2026.html)
- [Calendario AEAT 2026](https://sede.agenciatributaria.gob.es/Sede/Calendario_fecha_y_hora_oficial.html)
- [PRE-Exteriores pre-validador](https://preportal.aeat.es/PRE-Exteriores/)
- [VIES validación NIF-IVA intracom](https://ec.europa.eu/taxation_customs/vies/)
- [Verifactu FAQs desarrolladores (PDF dic 2025)](https://sede.agenciatributaria.gob.es/static_files/AEAT_Desarrolladores/EEDD/IVA/VERI-FACTU/FAQs-Desarrolladores.pdf)
- [Colaboración social presentación declaraciones](https://sede.agenciatributaria.gob.es/Sede/colaborar-agencia-tributaria/colaboracion-social-presentacion-declaraciones.html)
- [Manual 347 AEAT](https://sede.agenciatributaria.gob.es/Sede/ayuda/manuales-videos-folletos/manuales-practicos/folleto-actividades-economicas/8-declaraciones-informativas/8_2-declaracion-anual-operaciones-terceros-347.html)
- BOE — Orden HAC/27/2026 (modificaciones 303/390/SII 2026)
- BOE — Orden HAC/1431/2025 (modificaciones informativas 190/347 campaña 2026)

## Cross-refs

- Verifactu en prod desde Sprint 3 — coexiste con 303/347, NO los sustituye. Cross-check obligatorio.
- Conciliación bancaria (mig 061/101/103): cuadre de criterio caja se apoya en `movimientos_bancarios` matched.
- Borradores Holded-style mig 099: `num IS NULL` no entra en declaraciones.
- Abonos solo vía anulación (RD 1619/2012): facturas rectificativas casillas 14/15 con signo.
- `fecha_operacion` mig 087: dimensión obligatoria de periodificación.
- Multi-empresa mig 017: declaración por `org_id` (cada org un NIF).
