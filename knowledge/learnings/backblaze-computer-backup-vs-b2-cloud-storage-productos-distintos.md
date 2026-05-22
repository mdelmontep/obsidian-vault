---
name: backblaze-computer-backup-vs-b2-cloud-storage-productos-distintos
description: Backblaze tiene 2 productos separados — Computer Backup (Mac/PC backup automático) vs B2 Cloud Storage (S3-like con Object Lock). Panel distinto.
date: 2026-05-23
source: claude-code-session
tags: [backblaze, onboarding, gotcha, storage]
---

**Gotcha onboarding**: al login en `https://secure.backblaze.com` por defecto entras al panel de **Computer Backup** (7€/mes producto consumer, backup automático Mac/PC). El menú lateral muestra "Computer Backup / Overview / View/Restore Files / My Restores / etc". **No aparece "Buckets" ni "App Keys"** porque ese panel es del producto de backup, NO de B2 Cloud Storage.

**B2 Cloud Storage** (lo que necesitas para WORM Object Lock, integración S3-compatible, API REST) es un producto **separado** dentro de la misma cuenta. Requisitos para acceder:
1. **2FA habilitado** (Settings → Two-Factor Authentication). Sin 2FA, Backblaze oculta B2 desde 2023.
2. **B2 activado explícitamente** la primera vez (banner "Enable B2 Cloud Storage" o URL directa `https://secure.backblaze.com/b2_buckets.htm`).
3. Tras activar aparece sección lateral "B2 Cloud Storage" con `Buckets`, `App Keys`, `Cloud Replication`, `Browse Files`, `Reports`.

**Síntoma típico**: tarda 5-10 min averiguar que estás en el producto equivocado. El error "Account trouble" al intentar usar B2 API sin 2FA tampoco lo dice claro.

**Acción**: si compartes runbooks Backblaze con devs nuevos, especificar "B2 Cloud Storage (NO Computer Backup)" + recordar 2FA prerequisite. Aplicable a cualquier onboarding con cuenta Backblaze nueva.
