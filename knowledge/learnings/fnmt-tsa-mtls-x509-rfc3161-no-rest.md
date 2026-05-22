---
name: fnmt-tsa-mtls-x509-rfc3161-no-rest
description: FNMT Time Stamp Authority NO es REST JSON — es RFC 3161 binario DER sobre HTTPS con mTLS X.509.
date: 2026-05-22
source: claude-code-session
tags: [eidas, fnmt, criptografia, integracion]
---

**Gotcha**: muchos asumen que FNMT TS@ expone REST API JSON. NO. Es RFC 3161 puro: `TimeStampReq` ASN.1 DER por POST con `Content-Type: application/timestamp-query`, response `TimeStampResp` DER. Requiere mTLS con certificado X.509 cliente admitido por FNMT (convenio bilateral `comercial.ceres@fnmt.es`).

**Endpoints producción 2026** (verificado DPC v1.8 FNMT TSA, sep-2025):
- `qets2025.cert.fnmt.es` ECDSA P-256, clave privada vigente hasta 15-dic-2029
- `qets2023.cert.fnmt.es` RSA 3072, clave privada vigente hasta 14-dic-2025 (fallback)

**OID política**: `0.4.0.2023.1.1` (ETSI EN 319 421). Hashes aceptados: SHA-256/384/512.

**Coste**: ~0,002€/sello vía CERES (volumen). Sello cualificado eIDAS art 42 UE 910/2014 da presunción legal de exactitud temporal (vs hash sha256 interno que es prueba simple impugnable).

**Implementación TS**: `node-rfc3161-timestamp` o construir `TimeStampReq` con `asn1.js`. Verifica nonce anti-replay (8 bytes random en req, debe coincidir en resp). Cliente HTTPS con `https.Agent({ cert, key, requestCert: true, rejectUnauthorized: true })`. Cert path desde env, nunca hardcoded.

Aplicable a cualquier integración eIDAS QTSP (Uanataca, Logalty, Camerfirma también RFC 3161).

**Gotcha proceso 2026**: NO existe sandbox FNMT TSA público. Para probar el servicio en CUALQUIER capacidad (incluso dev) hay que firmar convenio bilateral con CERES → 2-6 semanas (formularios + acuerdo + emisión cert X.509 admitido + whitelist IP origen). No se puede testear en local antes de tener convenio. Alternativa con alta más rápida: **Uanataca** (otro QTSP cualificado UE en Trusted List ES) alta 2-3 semanas + API REST moderna + ~0,03€/sello vs ~0,002€ FNMT. **Migración FNMT↔Uanataca = cambio env vars URL + cert** (código TS RFC 3161 estándar funciona con ambos sin cambios). Plantilla email solicitud convenio FNMT: ver `docs/runbooks/fnmt-tsa-email-solicitud-convenio.md` repo facturaia.
