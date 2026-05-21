---
title: NIF España es paraguas (DNI/NIE/CIF) desde RD 1065/2007
date: 2026-05-21
source: claude-code-session
tags: [fiscal, espana, validacion, copy]
---

Hasta 2008: CIF (empresas) vs DNI (personas) vs NIE (extranjeros) eran etiquetas distintas. Desde RD 1065/2007 art 18 (vigencia 2008): AEAT eliminó "CIF" y unificó todo bajo "NIF". El formato sigue siendo distinto:

- **DNI** (persona física ES): 8 dígitos + letra control (módulo 23 sobre `TRWAGMYFPDXBNJZSQVHLCKE`).
- **NIE** (persona física extranjera): X|Y|Z + 7 dígitos + letra (X→0, Y→1, Z→2 + módulo 23).
- **CIF** (persona jurídica): letra inicial [ABCDEFGHJNPQRSUVW] + 7 dígitos + control (dígito o letra según inicial: PQRSNW→letra obligatoria, ABEH→dígito, CDFGJUV→ambos).

Coloquialmente B2B sigue diciendo "CIF" al NIF de empresa. Aceptar los 3 algoritmos bajo misma interfaz `validateSpanishTaxId()`. Copy en SaaS: "NIF" genérico cubre los 3 sin sonar técnico. "CIF/NIF" si B2B explícito.

Implementación referencia: `facturaia/src/lib/validation/spanish-tax-id.ts` + helper replicado en n8n calc-totals (cambio aquí refleja allí).
