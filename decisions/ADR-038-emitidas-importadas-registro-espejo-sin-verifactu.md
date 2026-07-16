---
title: "Facturas emitidas importadas de otro SIF: registro espejo (sin VeriFactu)"
date: 2026-07-17
status: aceptada
tags: [facturaia, fiscal, verifactu, adr]
---

## Contexto
Un cliente puede querer traer a TuFacturaIA (SIF VeriFactu) facturas que EMITIÓ en OTRA
plataforma (Holded/Factusol/Excel…) y verlas como emitidas.

## Decisión
Se registran como **espejo contable, SIN VeriFactu**: sin huella, sin envío AEAT,
conservan su número/serie original (serie reservada `EXT`, no consumen el contador
propio) vía un núcleo hermano `importarEmitidaExterna()` (NO `createDocument`). Cuentan
en libros / IVA repercutido / 303 / informes. Flag BD `facturas.registro_externo`; los
triggers de huella hacen early-exit por él.

## Alternativas descartadas
- **Re-emitir como SIF** (numerar + registrar en AEAT): duplicaría el registro AEAT y
  rompería la cadena de huellas → riesgo fiscal real.
- **Dejar elegir al usuario** (registro-only vs re-emitir): expone a error fiscal; fuera de v1.

## Consecuencias
Toda importada necesita ≥1 línea (el motor 303 descarta facturas sin líneas) → línea
sintética si el OCR no las trae. No se puede anular en la app (anular en el SIF de origen).
Dependencia de despliegue: la migración del flag va a prod ANTES del código que lo lee.
Estado del trabajo: memoria de agente `project_importar_facturas_externas` (rama
`feat/importar-facturas-externas`, no mergeada).
