---
title: verifactu xsd: SistemaFacturacion.xsd (404) — usar SuministroInformacion.xsd + SuministroLR.xsd
date: 2026-06-28
source: claude-code-session
tags: [verifactu, aeat, xml, namespace]
---
La URL `SistemaFacturacion.xsd` usada en código legacy da **404**. Los schemas reales son dos:

- `SuministroInformacion.xsd` — targetNamespace confirmado con xmllint. Define `RegistroAlta`,
  `RegistroAnulacion`, `CabeceraType` y todos los elementos de datos del registro.
- `SuministroLR.xsd` — define el wrapper SOAP: `RegFactuSistemaFacturacion`, `RegistroFactura`.

Fix inmediato: cambiar `NS` a `SuministroInformacion.xsd`. Validar con:
`xmllint --schema SuministroInformacion.xsd registro.xml --noout`

Sin acceso al WSDL no se puede confirmar si el envelope SOAP acepta NS único o exige split
LR (wrapper) / SI (datos). Validar en smoke PRE con cert real antes de activar a ningún cliente.

Fuente: xmllint contra XSD oficial + inspección directa de ambos schemas en agenciatributaria.gob.es.
