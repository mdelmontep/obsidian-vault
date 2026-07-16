---
title: verifactu — la huella hashea 8 campos (incl. fechahorahuso, en mayúsculas), el WS exige mTLS y la respuesta no tiene codigorespuesta
date: 2026-07-16
source: claude-code-session
tags: [verifactu, aeat, facturaia, cumplimiento]
---
Bugs que rompían el 100% de envíos (auditoría A-Z contra docs oficiales AEAT):

- **Huella**: la cadena a hashear son 8 campos y CIERRA con `&FechaHoraHusoGenRegistro=`
  (no termina en `&Huella=`). Salida hex en MAYÚSCULAS. Y el timestamp debe ser
  ÚNICO: el mismo valor en el hash y en el XML → persistirlo al calcular la huella,
  no regenerarlo al enviar. Validar SIEMPRE contra el ejemplo firmado oficial
  (AnexosEjemplosFirmaRegFact) con un SHA-256 en Python: debe reproducir la huella exacta.
- **Transporte**: el WS exige TLS mutuo (mTLS) con certificado cualificado en el CANAL
  (`node:https` con cert/key del P12), no `fetch` plano. En modo VERI*FACTU NO se firma
  el registro (XAdES solo para no-VERI*FACTU; Espec. firma §2/§5).
- **Respuesta**: NO existe `CodigoRespuesta`/`0000`. Se lee `EstadoEnvio` +
  `RespuestaLinea/EstadoRegistro` (Correcto/AceptadoConErrores/Incorrecto) +
  `CodigoErrorRegistro`. Duplicado = 3000. 2xxx = AceptadoConErrores (registrado, a subsanar).
- **SIF (declaración responsable)**: autodeclaración del fabricante, GRATIS, NO se presenta
  a la AEAT (no hay registro/censo). `IdSistemaInformatico` lo elige el fabricante (≤2 chars).
  `IndicadorMultiplesOT` es DINÁMICO por cuenta (S si ≥2 empresas, N si 1), no constante.
- **QR**: al principio de la factura, «QR tributario:» encima, 30-40 mm, leyenda VERI*FACTU debajo.

QA de PDF sin pipeline: `renderToStaticMarkup` + Puppeteer screenshot. Validar XML con `xmllint --schema`.
Ver [[verifactu-xsd-namespace-suministroinfo-vs-sistemafacturacion]], [[verifactu-aplazado-2027-rdl-15-2025]].
