---
title: facturaia — compliance legal PSD2 antes del cutover live
date: 2026-09-10
source: facturaia
tags: [facturaia, psd2, compliance, legal]
---

Extraído del hub [[facturaia]] el 10-sep-2026: son diez líneas de checklist que no orientan un arranque de sesión y se pagaban en cada una. **PSD2 está diferido por coste** (0 consentimientos activos, 0 movimientos por sync: es decisión, no avería), así que nada de esto es urgente — pero es lo que hay que tener firmado el día que se abra la conexión bancaria al público. Acción de Manu con Dani, no de desarrollo.

- **[IMPORTANTE PSD2 — pre-cutover live] Compliance legal con Dani antes de abrir conexión bancaria al público** _(verificado 2026-06-22: la integración TÉCNICA está COMPLETA y probada — Tink + TrueLayer, 24 consents en 3 orgs internas, todos revoked/pending/expired → NO abierto al público. El bloqueo es 100% legal, lo de abajo)_. **2026-07-01: se suma Salt Edge como 3er provider** (PR #610 draft, ver NEXT) — el mismo gate legal (DPA/Privacy Notice/DPIA por encargado del tratamiento) aplica también a Salt Edge antes de exponerlo a usuarios:
    - Revisar `docs/decisions/ADR-002-psd2-data-retention.md` y archivar (base legal retención 7 años Ley 58/2003 + Ley 11/2021 + Código Comercio art 30). Sin esto, frente a inspección AEPD o derecho al olvido GDPR art 17 vamos a defender ad hoc.
    - **Privacy Notice** del producto debe mencionar: (a) "Procesamos datos bancarios PSD2 via Tink AB (Visa, Suecia) y TrueLayer Limited (UK + EU passport) como encargados del tratamiento art 28 GDPR"; (b) "Retención 7 años por obligación fiscal"; (c) "Email para ejercer derechos: privacy@tufacturaia.com (endpoint art 15 disponible en /api/conciliacion/banks/[id]/access-report)". **Sin esto el consentimiento al tratamiento está viciado**.
    - **DPA art 28 GDPR** firmado con Tink AB (template estándar suyo, ~10 min). Lo mismo TrueLayer.
    - **T&C de TuFacturaIA** mencionan "banca abierta PSD2" + "solo lectura, no operativa".
    - **DPIA art 35 GDPR** (Data Protection Impact Assessment) — obligatoria para "tratamiento sistemático a gran escala de datos financieros sensibles". Plantilla AEPD, 4-8h redacción. Sin esto, infracción objetiva GDPR (multa hasta 10M€ o 2% facturación). Necesario antes de >100 orgs con banca conectada.
    - **Pentest** del flow PSD2 antes de cutover live (~3-5k€ outsourced o 2-3d con OWASP ZAP / Burp si in-house).
    - **Solicitar app live Tink** en console.tink.com (proceso self-service standard tier; pueden pedir info corporativa + Privacy Notice + DPA firmado).
    - **App live TrueLayer** si la mantenemos como fallback (más farragoso que Tink, pueden pedir review humana de la app — 3-5 días).
