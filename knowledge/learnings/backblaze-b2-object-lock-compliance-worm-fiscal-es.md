---
name: backblaze-b2-object-lock-compliance-worm-fiscal-es
description: Backblaze B2 Object Lock Compliance — WORM legal para fiscal ES sin coste extra vs S3 (3-4× más caro).
date: 2026-05-22
source: claude-code-session
tags: [worm, backblaze, fiscal, compliance, storage]
---

**Problema**: RD 1619/2012 art 8.1 + LGT art 66 exigen "garantía de integridad" durante 6 años para documentación tributaria. Supabase Storage NO sirve (service-role puede borrar). S3 Object Lock Frankfurt ~21€/TB/mes.

**Solución barata**: Backblaze B2 región Amsterdam con Object Lock modo **Compliance** (no Governance — Governance permite delete con permiso, no es WORM real). $6.95/TB/mes pay-as-you-go, Object Lock **incluido sin coste extra**. 50 orgs ~160MB/año = <0,01€/mes total.

**Inviolables del setup**:
- Bucket creado con File Lock = ON antes del primer upload
- Retención **6 años + 1 mes = 2222 días** desde upload (cubre LGT 4a + CCom 30 6a + margen)
- IAM Application Key SIN `deleteFiles` ni `bypassGovernance`
- Header obligatorio: `X-Bz-File-Retention-Mode: compliance` + `X-Bz-File-Retention-Retain-Until-Timestamp: <epoch ms>`
- Server-side encryption: `X-Bz-Server-Side-Encryption: AES256`

**Endpoint proxy desde Next.js, NO signed URL al cliente** (anti-tamper pre-upload). El cliente NUNCA debe poder elegir el contenido subido por el proxy.

**Alternativa soberanía FR**: Scaleway Paris Multi-AZ €0,0146/GB/mes (más caro pero misma capacidad legal). Evitar OVH 2026 (Object Lock aún no GA).

Aplicable a cualquier obligación de inmutabilidad legal: fiscal, sanitaria, gambling, financiera.
